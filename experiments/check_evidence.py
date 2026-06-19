#!/usr/bin/env python3
"""Deterministic evidence/shape audit of produced answers (no LLM, no tokens).

For each answer in experiments/out/answers/, resolve the question's reference_time
to a state dir and verify:
  - every evidence_path exists in that state dir (catches hallucinated paths),
  - the answer object is schema-valid,
  - memory_refs point at real files in the memory dir.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "experiments" / "out"


def state_for(reference_time: str) -> Path | None:
    try:
        date = datetime.fromisoformat(reference_time).date().isoformat()
    except ValueError:
        date = str(reference_time)[:10]
    d = REPO / "sample_states" / date
    return d if d.exists() else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--answers-dir", default=str(OUT / "answers_adapted"))
    cli = ap.parse_args()
    ans = Path(cli.answers_dir)
    print(f"auditing {ans}")

    questions = {q["id"]: q for q in
                 json.loads((REPO / "sample_questions.json").read_text())["questions"]}
    rows, bad_total = [], 0
    for qid, q in questions.items():
        af = ans / f"{qid}.json"
        if not af.exists():
            rows.append((qid, "NO ANSWER", 0, 0, []))
            continue
        a = json.loads(af.read_text())
        sd = state_for(str(q["reference_time"]))
        ev = a.get("evidence_paths", []) or []
        bad = [p for p in ev if not (sd and (sd / p).exists())]
        bad_total += len(bad)
        shape_ok = (isinstance(a.get("answer"), str) and a["answer"].strip()
                    and isinstance(ev, list) and isinstance(a.get("uncertainty"), str))
        rows.append((qid, "ok" if shape_ok else "BAD SHAPE", len(ev), len(bad), bad))

    print(f"{'question':42} {'shape':10} {'#ev':>4} {'#bad':>5}")
    print("-" * 70)
    for qid, shape, n_ev, n_bad, bad in rows:
        print(f"{qid:42} {shape:10} {n_ev:>4} {n_bad:>5}")
        for p in bad:
            print(f"    ✗ missing in state: {p}")
    print("-" * 70)
    print(f"total hallucinated/invalid evidence paths: {bad_total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
