#!/usr/bin/env python3
"""Parallel, N-run answer generation for noise-controlled evaluation.

Generates `--repeat` independent answer sets for one config, in parallel, reusing
the prebuilt MEMORY_DIR. Output: experiments/out/eval/<tag>/r<k>/<qid>.json.
Run once per config (e.g. v4 = --rel off, v5 = --rel on), then judge with the
eval-judge workflow and average across repeats to see signal past the noise.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SUB = REPO / "submissions" / "agent-memory"
MEM = REPO / "experiments" / "out" / "memory"


def state_for(rt: str) -> Path:
    states = sorted(p for p in (REPO / "sample_states").iterdir() if p.is_dir())
    try:
        d = datetime.fromisoformat(rt).date().isoformat()
    except ValueError:
        d = str(rt)[:10]
    p = REPO / "sample_states" / d
    return p if p.exists() else states[-1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tag", required=True)
    ap.add_argument("--repeat", type=int, default=3)
    ap.add_argument("--concurrency", type=int, default=5)
    ap.add_argument("--mode", default="adapted")
    ap.add_argument("--rel", default="on")
    ap.add_argument("--struct", default="on")
    ap.add_argument("--pdf", default="off")
    ap.add_argument("--repair", default="off")
    ap.add_argument("--verify", default="off")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--budget", default="", help="ENGRAM_DIGEST_BUDGET override")
    ap.add_argument("--maxfull", default="", help="ENGRAM_DIGEST_MAXFULL override")
    ap.add_argument("--questions", default=str(REPO / "sample_questions.json"))
    ap.add_argument("--timeout", type=int, default=300)
    a = ap.parse_args()

    qs = json.loads(Path(a.questions).read_text())["questions"]
    env = dict(os.environ)
    env.update({"ENGRAM_MODEL": a.model, "ENGRAM_MODE": a.mode, "ENGRAM_REL": a.rel,
                "ENGRAM_STRUCT": a.struct, "ENGRAM_PDF": a.pdf,
                "ENGRAM_REPAIR": a.repair, "ENGRAM_VERIFY": a.verify})
    if a.budget:
        env["ENGRAM_DIGEST_BUDGET"] = a.budget
    if a.maxfull:
        env["ENGRAM_DIGEST_MAXFULL"] = a.maxfull
    run_sh = SUB / "run.sh"
    outroot = REPO / "experiments" / "out" / "eval" / a.tag

    tasks = [(k, q) for k in range(1, a.repeat + 1) for q in qs]

    def do(k, q):
        rd = outroot / f"r{k}"
        rd.mkdir(parents=True, exist_ok=True)
        qf = rd / f"_q_{q['id']}.json"
        qf.write_text(json.dumps(q), encoding="utf-8")
        af = rd / f"{q['id']}.json"
        t = time.time()
        p = subprocess.run([str(run_sh), "answer", str(state_for(str(q["reference_time"]))),
                            str(MEM), str(qf), str(af)],
                           cwd=str(SUB), text=True, capture_output=True,
                           timeout=a.timeout, env=env)
        ok = p.returncode == 0 and af.exists()
        return (k, q["id"], ok, time.time() - t, "" if ok else p.stderr[-300:])

    print(f"generating {len(tasks)} answers for '{a.tag}' "
          f"(mode={a.mode} rel={a.rel} pdf={a.pdf} repair={a.repair} verify={a.verify}) "
          f"conc={a.concurrency}")
    t0, fails = time.time(), 0
    with ThreadPoolExecutor(max_workers=a.concurrency) as ex:
        for fut in as_completed([ex.submit(do, k, q) for k, q in tasks]):
            k, qid, ok, dt, err = fut.result()
            if not ok:
                fails += 1
                print(f"  FAIL r{k} {qid} ({dt:.0f}s): {err}")
    print(f"'{a.tag}' done in {time.time() - t0:.0f}s — {len(tasks) - fails}/{len(tasks)} ok")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
