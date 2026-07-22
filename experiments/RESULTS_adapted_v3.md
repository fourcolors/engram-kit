# Adapted v3 (surgical repair) — NET-NEUTRAL, reverted

v3 = v1 config + a **surgical repair pass**: a deterministic trigger detects when
the draft hedges "unavailable" about a file that is actually present, then feeds
ONLY those file bodies to a small repair call to strike the hedge and re-ground.
Intended to fix the laggards (apr18, apr20, apr21_instrument) without v2's cost.

## Scorecard — v3 ties v1 but adds a defect

| Metric | stock | v1 | v2 | v3 |
|---|---|---|---|---|
| Responsiveness | 3.50 | 4.90 | 4.90 | **5.00** |
| Groundedness | 2.60 | 4.40 | 4.30 | 4.40 |
| Uncertainty calibration | 2.30 | 4.10 | 3.80 | 4.00 |
| **Overall** | 2.60 | **4.40** | 4.30 | **4.40** |
| Hindsight leaks | 1 major | **0** | 0 | **1 minor** |

Per-question overall, v1 → v3: apr18 **2→4** ↑, apr20 **3→4** ↑, apr21_instrument
5→5, BUT apr17 **5→3** ↓, apr08 **5→4** ↓; apr10 gained a hallucinated
evidence_path (`NE_1_3_EVAL_CANDIDATES_V1.md`, first appears Apr 20) → 1 minor leak.

## Why v3 is not a win
Same pattern as v2: the repair pass **moves points around without netting up**.
It fixed its targets (apr18/apr20) but regressed previously-perfect answers
(apr17) and introduced a future-dated citation (apr10). Latency also returned to
110–170s on big states. Net overall = 4.40 (ties v1) with one new leak → strictly
worse than v1.

## Decision
Reverted: `ENGRAM_REPAIR` defaults **off**. **v1 (4.40, zero leaks, fast,
simplest) is the canonical config.** Repair code kept opt-in.

## The real conclusion (two failed answer-side patches)
v2 (heavy verify) and v3 (surgical repair) both failed to net-improve. **Post-hoc
answer-side patching has hit diminishing returns** — asking the model to re-open a
settled answer re-litigates the correct parts too. The recurring failures
(apr17/apr18/apr20: hedging or mis-deriving timeline facts about present files)
share one root: the answer pass must **re-derive timeline facts at answer time**.
The durable fix is to put those facts in the **memory** so they never need
re-deriving — which is the memory-side iteration (structured per-file timeline +
lineage-preserving reflection).
