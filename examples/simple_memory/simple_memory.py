#!/usr/bin/env python3
"""Tiny ENGRAM two-command example."""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def iter_state_files(state_dir: Path) -> list[Path]:
    files_root = state_dir / "files"
    if not files_root.exists():
        return []
    return sorted(path for path in files_root.rglob("*") if path.is_file())


def update(state_dir: Path, memory_dir: Path) -> int:
    memory_dir.mkdir(parents=True, exist_ok=True)
    record = {
        "phase": "update",
        "state": state_dir.name,
        "files": [str(path.relative_to(state_dir)) for path in iter_state_files(state_dir)],
        "changes": read_text(state_dir / "changes.txt")[:1000],
        "recorded_at_utc": now_iso(),
    }
    with (memory_dir / "memory.jsonl").open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True) + "\n")
    return 0


def answer(state_dir: Path, memory_dir: Path, question_json: Path, answer_json: Path) -> int:
    question = json.loads(question_json.read_text(encoding="utf-8"))
    question_text = str(question.get("question", "")).lower()
    snippets: list[tuple[str, str]] = []
    for path in iter_state_files(state_dir):
        rel = str(path.relative_to(state_dir))
        text = read_text(path)
        snippets.append((rel, text))

    if "backend" in question_text:
        target = next((item for item in snippets if "backend" in item[0]), snippets[0] if snippets else ("", ""))
        answer_text = (
            "The sample says backend choice is open. Supermemory, SMFS, Cognee, Letta, "
            "graphs, vectors, SQLite, Markdown, or custom agents are strategies, not "
            "ENGRAM requirements."
        )
        evidence = [target[0]] if target[0] else []
    elif "direction" in question_text:
        target = next((item for item in snippets if "engram-direction" in item[0]), snippets[0] if snippets else ("", ""))
        answer_text = (
            "The sample direction is a small submission challenge: receive dated "
            "workspace states, maintain private memory, and answer from current state "
            "plus prior memory."
        )
        evidence = [target[0]] if target[0] else []
    else:
        answer_text = "Cannot determine from this simple example."
        evidence = []

    write_json(
        answer_json,
        {
            "answer": answer_text,
            "evidence_paths": evidence,
            "memory_refs": ["memory.jsonl"] if (memory_dir / "memory.jsonl").exists() else [],
            "uncertainty": "This is a keyword example, not a real memory architecture.",
        },
    )
    return 0


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        raise SystemExit(
            "usage: run.sh update STATE_DIR MEMORY_DIR | "
            "run.sh answer STATE_DIR MEMORY_DIR QUESTION_JSON ANSWER_JSON"
        )
    phase = argv[1]
    if phase == "update" and len(argv) == 4:
        return update(Path(argv[2]), Path(argv[3]))
    if phase == "answer" and len(argv) == 6:
        return answer(Path(argv[2]), Path(argv[3]), Path(argv[4]), Path(argv[5]))
    raise SystemExit(f"invalid ENGRAM command: {' '.join(argv[1:])}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
