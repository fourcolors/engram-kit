# Run Prep Notes — 2026-04-20

Status: execution note before new benchmark runs

## What is frozen for this batch

- Use the current repaired replay sources:
  - `_internal/syke-replay-lab/runs/ne13_prod_codex54mini_timefix_20260416T142500Z`
  - `_internal/syke-replay-lab/runs/ne13_zero_codex54mini_timefix_20260416T142500Z`
- Keep the current benchmark item source:
  - `research/n1-memory-lab/NE_1_3_REAL_ASK_EVAL_SET.yaml`
- Keep the current canonical runset file:
  - `_internal/syke-replay-lab/probes/REAL_ASK_RUNSETS.yaml`
- Treat this batch as empirical pressure, not final judge-science.
- Do not redesign scoring again before fresh runs exist.

## Corpus / denominator reminder

- `310 / 203 / 180` = exploration corpora
- `50` = current canonical benchmark sample
- `19` = current shipped 15-day runset in `REAL_ASK_RUNSETS.yaml`

## What this batch is for

- verify the repaired replay + ask + judge path still behaves on fresh benchmark work
- get new empirical pressure on the current benchmark contract
- produce concrete traces for the next scoring redesign pass

## Operational sequence

1. submit a small smoke run
2. if the smoke starts cleanly, queue the 15-day batch
3. use the resulting traces and verdicts to decide what to change next

## 2026-04-20 execution notes

- First smoke + 15-day submissions completed immediately but were junk:
  `labctl` inherited the wrong Python interpreter and benchmark workers died on
  `ModuleNotFoundError: uuid_extensions`.
- Fixed at launcher level in `_internal/syke-replay-lab/labctl.py`:
  prefer repo `.venv/bin/python` (or `SYKE_LAB_PYTHON`) instead of blindly
  inheriting the caller interpreter.
- Added regression coverage in
  `_internal/syke-replay-lab/tests/test_labctl.py`.
- Fresh active batch after the fix:
  - smoke:
    `benchmark-ne13-real-smoke-fixed-20260420t053624z-20260420T053624Z-2b4e47`
  - queued 15-day:
    `benchmark-ne13-real-15d-fixed-20260420t053624z-20260420T053625Z-4c701f`
