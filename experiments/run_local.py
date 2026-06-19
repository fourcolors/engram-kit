#!/usr/bin/env python3
"""Local ENGRAM eval runner for the agent-memory submission (NOT part of it).

Builds memory by running `run.sh update` over every sample state in chronological
order, then runs `run.sh answer` for each sample question (choosing the state dir
whose date matches the question's reference_time). Dumps answers + a copy of the
final MEMORY.md for inspection.

Examples:
    python experiments/run_local.py                       # full run, sonnet
    python experiments/run_local.py --max-states 2 --only Q001   # smoke
    python experiments/run_local.py --skip-update --model opus    # re-answer only
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]            # engram-kit/
DEFAULT_SUB = REPO / "submissions" / "agent-memory"


def sorted_states(kit: Path) -> list[Path]:
    return sorted(p for p in (kit / "sample_states").iterdir() if p.is_dir())


def state_for_reference(kit: Path, reference_time: str, states: list[Path]) -> Path:
    try:
        date = datetime.fromisoformat(reference_time).date().isoformat()
    except ValueError:
        date = str(reference_time)[:10]
    candidate = kit / "sample_states" / date
    return candidate if candidate.exists() else states[-1]


def mem_lines(mem: Path) -> int:
    f = mem / "MEMORY.md"
    return len(f.read_text(encoding="utf-8").splitlines()) if f.exists() else 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kit", default=str(REPO))
    ap.add_argument("--submission", default=str(DEFAULT_SUB))
    ap.add_argument("--out", default=str(REPO / "experiments" / "out"))
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--mode", default="adapted", choices=["stock", "adapted"],
                    help="answer-pass behavior; memory build is identical for both")
    ap.add_argument("--verify", default="off", choices=["auto", "always", "off"],
                    help="heavy verify pass (ENGRAM_VERIFY); v2 experiment, net-negative")
    ap.add_argument("--repair", default="off", choices=["on", "off"],
                    help="surgical false-unavailable repair (ENGRAM_REPAIR); v3 experiment, net-neutral")
    ap.add_argument("--tag", default="", help="answers subdir suffix (default = mode)")
    ap.add_argument("--max-states", type=int, default=0, help="0 = all states")
    ap.add_argument("--only", default="", help="comma-separated question ids")
    ap.add_argument("--timeout", type=int, default=300)
    ap.add_argument("--skip-update", action="store_true",
                    help="reuse existing memory dir; answer only")
    args = ap.parse_args()

    kit, sub, out = Path(args.kit), Path(args.submission), Path(args.out)
    run_sh = sub / "run.sh"
    mem = out / "memory"
    tag = args.tag or args.mode
    ans_dir = out / f"answers_{tag}"
    out.mkdir(parents=True, exist_ok=True)
    ans_dir.mkdir(parents=True, exist_ok=True)

    env = dict(os.environ)
    env["ENGRAM_MODEL"] = args.model
    env["ENGRAM_MODE"] = args.mode
    env["ENGRAM_VERIFY"] = args.verify
    env["ENGRAM_REPAIR"] = args.repair

    states = sorted_states(kit)
    if args.max_states:
        states = states[: args.max_states]

    if not args.skip_update:
        if mem.exists():
            shutil.rmtree(mem)
        mem.mkdir(parents=True)
        print(f"== building memory over {len(states)} states (model={args.model}) ==")
        for s in states:
            t = time.time()
            p = subprocess.run(
                [str(run_sh), "update", str(s), str(mem)],
                cwd=str(sub), text=True, capture_output=True,
                timeout=args.timeout, env=env,
            )
            if p.returncode != 0:
                print(f"  update {s.name} FAILED ({p.returncode})\n{p.stderr[-1800:]}")
                return 1
            print(f"  update {s.name:12} {time.time() - t:5.1f}s  mem_lines={mem_lines(mem)}")
        if (mem / "MEMORY.md").exists():
            shutil.copy(mem / "MEMORY.md", out / "MEMORY.snapshot.md")

    questions = json.loads((kit / "sample_questions.json").read_text())["questions"]
    only = {q for q in args.only.split(",") if q}
    all_states = sorted_states(kit)
    print(f"== answering questions (model={args.model}, mode={args.mode}) ==")
    failures = 0
    for q in questions:
        if only and q["id"] not in only:
            continue
        sd = state_for_reference(kit, str(q["reference_time"]), all_states)
        qf = out / f"_q_{q['id']}.json"
        qf.write_text(json.dumps(q), encoding="utf-8")
        af = ans_dir / f"{q['id']}.json"
        t = time.time()
        p = subprocess.run(
            [str(run_sh), "answer", str(sd), str(mem), str(qf), str(af)],
            cwd=str(sub), text=True, capture_output=True,
            timeout=args.timeout, env=env,
        )
        ok = p.returncode == 0 and af.exists()
        print(f"  {q['id']} [{sd.name}] {time.time() - t:5.1f}s {'ok' if ok else 'FAIL'}")
        if not ok:
            failures += 1
            print(p.stderr[-1800:])
    print(f"\nanswers in {ans_dir}  (memory snapshot: {out / 'MEMORY.snapshot.md'})")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
