# v4 — memory-side structured timeline (NEW BEST)

v4 = v1 config + a **deterministic per-file timeline** in memory. The observer
folds each day's `changes.txt` + `manifest.tsv` into `timeline.json` (first_seen,
status history, deletions) — **no LLM, no extra call**. The answer pass reads a
date-filtered view as the AUTHORITATIVE source for first-appearance /
current-vs-archived / existence facts, so it never re-derives them.

## Scorecard — v4 is the best config

| Config | Resp | Grnd | Unc | Overall | Leaks | Latency |
|---|---|---|---|---|---|---|
| stock | 3.50 | 2.60 | 2.30 | 2.60 | 1 major | — |
| v1 (relevance digest + date filter) | 4.90 | 4.40 | 4.10 | 4.40 | 0 | fast |
| v2 (heavy verify pass) | 4.90 | 4.30 | 3.80 | 4.30 | 0 | 5× slow |
| v3 (surgical repair pass) | 5.00 | 4.40 | 4.00 | 4.40 | 1 minor | slow |
| **v4 (structured timeline)** | **5.00** | **4.70** | **4.30** | **4.60** | **0** | **fast** |

Per-question vs v1: apr10 **4→5**, apr18 **2→3**, apr20 **3→4** (three laggards
up), apr17 5→4 (one dip), the rest held at 5. All answers 24–52s (under the 60s
limit); no extra LLM calls (timeline is computed, not generated).

## Why v4 worked where v2/v3 didn't
v2 (verify) and v3 (repair) were *answer-side post-hoc patches* — they fixed a
target and broke something else (point-shuffling), netting ≤ v1. v4 moves the fix
to the **memory layer**: the answer looks facts up instead of re-deriving them, so
there's nothing to patch and no settled answer to re-litigate. It produced the
first genuine net lift (+0.20 over v1) with **zero leaks**.

## What still blocks 5.0 (per judges)
- **Answer-side (highest leverage):** an uncertainty-calibration bug — the answer
  sometimes calls a present file *body* "unavailable / not shown" when it's just
  not in the relevance digest (hits apr17, half of apr18). Fix: bound the digest
  better / forbid "unavailable" for any file in the timeline.
- **Memory-side (two small wins):**
  - apr20: expose explicit **transition-kind counts** (approximate→exact vs
    unavailable→exact vs deleted) in the timeline view, so the answer reports the
    breakdown instead of a blanket "all flipped."
  - apr18: add **intra-file value→source attribution** (which file a date/value
    came from) — the one genuinely memory-shaped residual.

## Status
v4 is the **canonical/default config** (observer builds timeline; answer reads it;
ENGRAM_REPAIR/ENGRAM_VERIFY default off). Arc: stock 2.60 → v1 4.40 (answer-side
retrieval) → v4 4.60 (memory-side structure). The memory system was both the
strong part AND the right place for the winning improvement.
