"""The ANSWER PASS — the `answer` phase.

ENGRAM_MODE selects behavior:
  - stock   : whole MEMORY.md (200-line cap, no date filter) + small-files-first
              digest. The measured baseline.
  - adapted : no-hindsight memory (date-filtered <= reference date) + a
              relevance-ranked digest that includes full bodies of the files the
              question targets, with a prompt that bans false "unavailable"
              refusals and keeps memory separate from evidence. (default)
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

from claude_client import run_claude
from memory import read_memory, read_memory_asof
from pdf_index import select_and_extract
from relationships import change_summary
from state_digest import digest_answer_state, digest_answer_state_relevant
from timeline import timeline_asof
from util import cap_lines, read_text, render

_FILE_RE = re.compile(r"[A-Za-z0-9_./-]+\.[A-Za-z0-9]{1,6}")
_HEDGE = (
    "not available", "not shown", "not reproduced", "not included", "not provided",
    "cannot be determined", "cannot determine", "can't determine", "unavailable",
    "not readable", "not in the provided", "not visible", "are not shown",
    "is not shown", "not present in the provided",
)

PROMPTS = Path(__file__).resolve().parent / "prompts"

# Phrases that signal a draft may be falsely refusing or hedging on present files.
_RED_FLAGS = (
    "not available", "not shown", "not reproduced", "not included", "not provided",
    "cannot be determined", "cannot determine", "can't determine", "unavailable",
    "not readable", "inferred from memory", "no observation", "not in the provided",
    "not visible", "is not present in the provided",
)


def _ref_date(reference_time: str) -> str:
    try:
        return datetime.fromisoformat(reference_time).date().isoformat()
    except ValueError:
        return str(reference_time)[:10]


def _needs_verify(payload: dict, policy: str) -> bool:
    if policy == "off":
        return False
    if policy == "always":
        return True
    blob = (payload.get("answer", "") + " " + payload.get("uncertainty", "")).lower()
    return any(flag in blob for flag in _RED_FLAGS)


def run_answer(
    state_dir: Path,
    memory_dir: Path,
    question_json: Path,
    answer_json: Path,
    *,
    model: str = "sonnet",
) -> int:
    mode = os.environ.get("ENGRAM_MODE", "adapted")
    question = json.loads(question_json.read_text(encoding="utf-8"))
    qtext = str(question.get("question", ""))
    reference_time = str(question.get("reference_time", ""))

    if mode == "stock":
        memory = cap_lines(read_memory(memory_dir), 200) or "(no memory recorded)"
        state_ctx = digest_answer_state(state_dir)
        template = (PROMPTS / "answer.md").read_text(encoding="utf-8")
    else:
        ref_date = _ref_date(reference_time)
        memory = read_memory_asof(memory_dir, ref_date).strip() \
            or "(no memory recorded as of the reference time)"
        state_ctx = digest_answer_state_relevant(state_dir, qtext)
        timeline = timeline_asof(memory_dir, ref_date) or "(no structured timeline available)"
        relations = change_summary(state_dir) or "(no deterministic change/relationship facts for this state)"
        # PageIndex-style PDF retrieval (opt-in): append page-scoped extracts of the
        # PDF sections the model navigates to. No-hindsight is automatic (state_dir
        # is the reference-time snapshot).
        if os.environ.get("ENGRAM_PDF", "off") != "off":
            pdf_ctx = select_and_extract(state_dir, memory_dir, qtext, model=model)
            if pdf_ctx:
                state_ctx = state_ctx + "\n\n" + pdf_ctx
        template = (PROMPTS / "answer_adapted.md").read_text(encoding="utf-8")

    prompt = render(
        template,
        REFERENCE_TIME=reference_time,
        MEMORY=memory,
        TIMELINE=(timeline if mode != "stock" else ""),
        RELATIONS=(relations if mode != "stock" else ""),
        STATE_CONTEXT=state_ctx,
        QUESTION=qtext,
    )
    raw = run_claude(prompt, model=model)
    try:
        payload = _coerce(_extract_json(raw))
    except (ValueError, json.JSONDecodeError) as exc:
        return _safe_fallback(answer_json, f"unparseable model output: {exc}")

    # SURGICAL REPAIR (adapted, default on): deterministic trigger — only fires
    # when the draft hedges that a file is "unavailable" while that file is
    # actually present in the state. Feeds ONLY those files' bodies to a small,
    # cheap repair call. Fast (tiny context) and safe (requires a provable false
    # hedge, so it can't re-litigate correct answers). ENGRAM_REPAIR=off to skip.
    if mode != "stock" and os.environ.get("ENGRAM_REPAIR", "off") != "off":
        hedged = _false_hedged_files(payload, _present_index(state_dir))
        if hedged:
            payload = _repair(payload, hedged, state_dir, qtext, reference_time, model)

    # v2 verify/repair pass (heavy, opt-in). Measured net-negative (4.40->4.30)
    # and ~5x slower; default OFF. Opt in with ENGRAM_VERIFY=auto|always.
    verify_policy = os.environ.get("ENGRAM_VERIFY", "off")
    if mode != "stock" and _needs_verify(payload, verify_policy):
        payload = _verify(payload, state_ctx, qtext, reference_time, model)

    answer_json.parent.mkdir(parents=True, exist_ok=True)
    answer_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


def _present_index(state_dir: Path) -> dict:
    """basename(lower) -> path for every file present in the state."""
    root = state_dir / "files"
    idx: dict[str, Path] = {}
    if root.exists():
        for p in root.rglob("*"):
            if p.is_file():
                idx.setdefault(p.name.lower(), p)
    return idx


def _false_hedged_files(payload: dict, present: dict) -> list:
    """Files the draft names while hedging 'unavailable' — but that ARE present."""
    blob = payload.get("answer", "") + " \n " + payload.get("uncertainty", "")
    if not any(h in blob.lower() for h in _HEDGE):
        return []
    out, seen = [], set()
    for m in _FILE_RE.findall(blob):
        base = m.split("/")[-1].lower()
        if base in present and base not in seen:
            seen.add(base)
            out.append(present[base])
    return out


def _repair(payload: dict, files: list, state_dir: Path, qtext: str,
            reference_time: str, model: str) -> dict:
    root = state_dir / "files"
    blocks, budget = [], 35000
    for p in files[:8]:
        block = f"### files/{p.relative_to(root)}\n{read_text(p)}"
        blocks.append(block[:budget])
        budget -= len(block)
        if budget <= 0:
            break
    prompt = render(
        (PROMPTS / "repair.md").read_text(encoding="utf-8"),
        REFERENCE_TIME=reference_time,
        QUESTION=qtext,
        FILES="\n\n".join(blocks),
        DRAFT=json.dumps(payload, indent=2),
    )
    try:
        return _coerce(_extract_json(run_claude(prompt, model=model)))
    except (ValueError, json.JSONDecodeError):
        return payload


def _verify(payload: dict, state_ctx: str, qtext: str, reference_time: str, model: str) -> dict:
    prompt = render(
        (PROMPTS / "verify.md").read_text(encoding="utf-8"),
        REFERENCE_TIME=reference_time,
        STATE_CONTEXT=state_ctx,
        QUESTION=qtext,
        DRAFT=json.dumps(payload, indent=2),
    )
    try:
        return _coerce(_extract_json(run_claude(prompt, model=model)))
    except (ValueError, json.JSONDecodeError):
        return payload  # keep the draft if the verify pass misbehaves


def _extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("\n") + 1:] if "\n" in text else text
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("no JSON object in model output")
    return json.loads(text[start:end + 1])


def _coerce(payload: dict) -> dict:
    def as_list(v):
        return v if isinstance(v, list) else ([] if v in (None, "") else [str(v)])

    answer = payload.get("answer")
    if not isinstance(answer, str) or not answer.strip():
        answer = "Cannot determine from the released state."
    refs = as_list(payload.get("memory_refs")) or ["MEMORY.md"]
    return {
        "answer": answer,
        "evidence_paths": as_list(payload.get("evidence_paths")),
        "memory_refs": refs,
        "uncertainty": str(payload.get("uncertainty", "")),
    }


def _safe_fallback(answer_json: Path, reason: str) -> int:
    print(f"answer pass fell back: {reason}", file=sys.stderr)
    answer_json.parent.mkdir(parents=True, exist_ok=True)
    answer_json.write_text(json.dumps({
        "answer": "Cannot determine from the released state.",
        "evidence_paths": [],
        "memory_refs": ["MEMORY.md"],
        "uncertainty": f"Answer pass failed: {reason}",
    }, indent=2) + "\n", encoding="utf-8")
    return 0
