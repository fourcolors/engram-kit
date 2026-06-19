# Adapted v2 (verify pass) — NEGATIVE RESULT

v2 added an LLM **verify/repair pass** after the draft answer (re-ground claims,
kill false "unavailable", recompute counts/transition breakdowns) plus a larger
digest (full manifest, 110 KB / 22-file body budget). Same memory, same judges.

## Scorecard — v2 did NOT beat v1

| Metric | stock | v1 | v2 | v1→v2 |
|---|---|---|---|---|
| Responsiveness | 3.50 | 4.90 | 4.90 | 0.00 |
| Groundedness | 2.60 | 4.40 | 4.30 | −0.10 |
| Uncertainty calibration | 2.30 | 4.10 | 3.80 | **−0.30** |
| **Overall** | 2.60 | **4.40** | 4.30 | **−0.10** |
| Hindsight leaks | 1 major | 0 | 0 | — |

Per-question v1→v2: apr18 **2→3** (helped), apr17 **5→4** and apr21_instrument
**5→4** (regressed), apr20 3→3 (no change), rest unchanged.

## Why v2 lost
- The verify pass **partially fixed the target** (apr18 +1, apr20 +0) but
  **introduced a new false-"unavailable" hedge** on a previously-perfect answer
  (apr21_instrument: claimed present `STATUS.json`/`TASKS.json` "not shown") and
  failed to catch apr17's recompute errors ("14 = 10+4" mislabel) — net −0.1.
- **Latency exploded:** verify-fired answers took 130–250s (vs ~40s), far over
  ENGRAM's 60s/command limit. Unshippable as-is.

## Decision
Reverted: `ENGRAM_VERIFY` defaults to **off**; digest restored to the measured
v1 settings (80 KB / 16 files). **v1 (4.40) is the canonical config.** The verify
pass code remains, opt-in, for future experiments.

## The real remaining blocker (per judges)
A stubborn false-"unavailable" hedge on the 3 highest-fan-out states
(apr20, apr18, apr21_instrument) where some relevant file bodies don't make the
digest. It is **answer-side**, and the surgical fix is **deterministic, not an
LLM pass**: for every "unavailable / not shown" phrase about a named file, look
the path up in the manifest; if present, strike the hedge and re-ground from the
body. Projected to lift 4.30 → ~4.8 without the verify pass's cost or regressions.

Memory-side improvements (structured per-file timeline, lineage-preserving
reflection) remain valuable for **durability / long-horizon no-hindsight**, but
the judges are clear they won't move *this* sample much — the sample blocker is
answer-side hedging, not memory quality.
