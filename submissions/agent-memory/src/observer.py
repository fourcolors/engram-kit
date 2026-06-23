"""The OBSERVER PASS (and reflector) — the `update` phase.

Stock subagent-memory discipline: at the end of each "invocation" (here, each
daily snapshot) extract 1-5 dated observation bullets and append them. When the
file approaches the 200-line cliff, compress with a reflector pass.
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

from claude_client import run_claude
from memory import append_dated, read_memory, write_memory
from pdf_index import update_pdf_index
from relationships import relationship_bullets
from state_digest import digest_update
from timeline import update_timeline
from util import cap_lines, count_lines, render

PROMPTS = Path(__file__).resolve().parent / "prompts"
REFLECT_AT = 195   # lines; mirrors the harness injection cliff
REFLECT_TO = 100   # target after compression
NO_OBS = "<no-new-observations/>"


def _state_date(state_dir: Path) -> str:
    """Prefer the directory name (YYYY-MM-DD); it is the observation's date."""
    return state_dir.name


def run_observer(state_dir: Path, memory_dir: Path, *, model: str = "sonnet") -> int:
    date_iso = _state_date(state_dir)

    # Deterministic structured memory: fold today's changes.txt + manifest into
    # the per-file timeline (first_seen / status history / deletions). No LLM.
    update_timeline(state_dir, memory_dir)

    # PageIndex-style PDF trees (deterministic, 0 LLM). Opt-in via ENGRAM_PDF.
    if os.environ.get("ENGRAM_PDF", "off") != "off":
        try:
            update_pdf_index(state_dir, memory_dir)
        except Exception as exc:  # never let PDF indexing fail an update
            print(f"pdf index skipped: {exc}", file=sys.stderr)

    existing = cap_lines(read_memory(memory_dir), 200) or "(empty — this is the first day)"
    digest = digest_update(state_dir)

    prompt = render(
        (PROMPTS / "observer.md").read_text(encoding="utf-8"),
        EXISTING_MEMORY=existing,
        DATE=date_iso,
        STATE_DIGEST=digest,
    )
    out = run_claude(prompt, model=model).strip()

    # Deterministic relationship facts (🔗) live as plain text in the observational
    # memory alongside the LLM's observations — no separate JSON edge store.
    rels = relationship_bullets(state_dir)
    obs = _clean(out) if (out and NO_OBS not in out) else ""
    section = "\n".join(s for s in (obs, "\n".join(rels)) if s).strip()
    if section:
        append_dated(memory_dir, date_iso, section)

    _maybe_reflect(memory_dir, model=model)
    return 0


def _clean(text: str) -> str:
    """Drop accidental code fences / stray Date headers the model may emit."""
    lines = [ln for ln in text.splitlines() if not ln.strip().startswith("```")]
    lines = [ln for ln in lines if not ln.strip().lower().startswith("date:")]
    return "\n".join(lines).strip()


def _dates(text: str) -> set[str]:
    return set(re.findall(r"^Date:\s*(\d{4}-\d{2}-\d{2})", text, re.M))


def _links(text: str) -> set[str]:
    return {ln.strip() for ln in text.splitlines() if ln.strip().startswith("🔗")}


def reflection_is_safe(before: str, after: str) -> bool:
    """30-day guarantee: reflection may compress, but must NOT (a) drop any Date
    header (else date-filtering / no-hindsight breaks) or (b) lose any deterministic
    🔗 relationship fact. Enforced deterministically — not left to the LLM."""
    return _dates(before).issubset(_dates(after)) and _links(before).issubset(_links(after))


def _maybe_reflect(memory_dir: Path, *, model: str) -> None:
    text = read_memory(memory_dir)
    if count_lines(text) < REFLECT_AT:
        return
    prompt = render(
        (PROMPTS / "reflector.md").read_text(encoding="utf-8"),
        TARGET=str(REFLECT_TO),
        MEMORY=text,
    )
    compressed = run_claude(prompt, model=model).strip()
    compressed = "\n".join(
        ln for ln in compressed.splitlines() if not ln.strip().startswith("```")
    ).strip()
    # Accept only a genuine compression that PRESERVES every date header and every
    # deterministic relationship fact. Otherwise keep prior memory (fail-safe).
    if compressed and count_lines(compressed) < count_lines(text) \
            and reflection_is_safe(text, compressed):
        write_memory(memory_dir, compressed)
    else:
        print("reflection rejected (would drop a date header or 🔗 fact, or no gain); "
              "keeping prior memory", file=sys.stderr)
