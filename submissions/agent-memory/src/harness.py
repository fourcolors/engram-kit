#!/usr/bin/env python3
"""ENGRAM two-command entry point for the agent-memory submission.

    run.sh update STATE_DIR MEMORY_DIR
    run.sh answer STATE_DIR MEMORY_DIR QUESTION_JSON ANSWER_JSON

Model is `sonnet` by default; override with ENGRAM_MODEL (e.g. opus, haiku).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from answerer import run_answer  # noqa: E402
from observer import run_observer  # noqa: E402

USAGE = (
    "usage: run.sh update STATE_DIR MEMORY_DIR | "
    "run.sh answer STATE_DIR MEMORY_DIR QUESTION_JSON ANSWER_JSON"
)


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        raise SystemExit(USAGE)
    phase = argv[1]
    model = os.environ.get("ENGRAM_MODEL", "sonnet")

    if phase == "update" and len(argv) == 4:
        return run_observer(Path(argv[2]), Path(argv[3]), model=model)
    if phase == "answer" and len(argv) == 6:
        return run_answer(
            Path(argv[2]), Path(argv[3]), Path(argv[4]), Path(argv[5]), model=model
        )
    raise SystemExit(f"invalid ENGRAM command: {' '.join(argv[1:])}\n{USAGE}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
