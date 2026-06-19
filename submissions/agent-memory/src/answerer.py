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
import sys
from datetime import datetime
from pathlib import Path

from claude_client import run_claude
from memory import read_memory, read_memory_asof
from state_digest import digest_answer_state, digest_answer_state_relevant
from util import cap_lines, render

PROMPTS = Path(__file__).resolve().parent / "prompts"


def _ref_date(reference_time: str) -> str:
    try:
        return datetime.fromisoformat(reference_time).date().isoformat()
    except ValueError:
        return str(reference_time)[:10]


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
        memory = read_memory_asof(memory_dir, _ref_date(reference_time)).strip() \
            or "(no memory recorded as of the reference time)"
        state_ctx = digest_answer_state_relevant(state_dir, qtext)
        template = (PROMPTS / "answer_adapted.md").read_text(encoding="utf-8")

    prompt = render(
        template,
        REFERENCE_TIME=reference_time,
        MEMORY=memory,
        STATE_CONTEXT=state_ctx,
        QUESTION=qtext,
    )
    raw = run_claude(prompt, model=model)
    try:
        payload = _coerce(_extract_json(raw))
    except (ValueError, json.JSONDecodeError) as exc:
        return _safe_fallback(answer_json, f"unparseable model output: {exc}")

    answer_json.parent.mkdir(parents=True, exist_ok=True)
    answer_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return 0


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
