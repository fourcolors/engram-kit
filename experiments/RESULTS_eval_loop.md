# Noise-controlled evaluation loop — final

Harness: `experiments/eval.py` (parallel N-run generation) + `experiments/judge_eval.js`
(judges every config×repeat×question, aggregates mean per config). Built to beat the
answer+judge noise floor (single runs swing borderline questions ±3). Each config:
3 runs × 10 questions = 30 answers, each judged once (overall 0–5).

## Scoreboard (N=3 averaged)

| Config | Mean | Run-means | false-"unavail" | Verdict |
|---|---|---|---|---|
| v4 — relationships OFF, Sonnet | 4.57 | 4.4–4.7 | 4/30 | baseline |
| v5 — relationships ON, Sonnet | 4.70 | 4.5–4.8 | 5–6/30 | rel = real +0.13 |
| b1 — v5 + bigger digest (140k/30) | 4.50 | 4.3–4.7 | 5/30 | **rejected (worse)** |
| v5 — relationships ON, **Opus** | 4.80–4.83 | 4.8–4.9 | 3–4/30 | strong |
| v6 — Opus + discipline prompt | 4.80–4.83 | 4.7–4.9 | 3–4/30 | = Opus (neutral) |
| **v7 — Opus + structured data handling** | **4.83** | 4.8–4.9 | **2/30** | **BEST — apr17 4→5, false-unavail halved** |

## What moved the score (and what didn't)
1. **Relationships ON: +0.13** (4.57→4.70). Real, isolated to apr10 + apr20 (the
   supersession/transition questions). Confirmed past noise by averaging.
2. **Opus answer model: +0.13–0.17** (4.70→4.83) — the single biggest lever, and it
   *collapsed the variance* (run-means flat at 4.8–4.9 vs Sonnet's 4.5–4.8). Fixed the
   hard reasoning question apr18 (3.3→4.3+).
3. **Bigger digest: −0.20 (rejected).** More context diluted focus; weak spots are
   reasoning, not retrieval-starvation.
4. **Discipline prompt: ~0 (neutral).** Kept (harmless, good practice) but not a win.

## Best config: relationships ON + structured ON + Opus ≈ 4.83 / 5
**apr17 SOLVED (4.0 → 5.0)** by the structured-data handler (`structured.py`): big
`.json/.tsv/.csv` files are rendered as schema + EXACT value-counts + stratified
sample + a computed cross-file set-difference ("23 dropped"), instead of being dumped
or skipped. false-"unavailable" halved (4→2 / 30), no new deps, stdlib only, ~3 ms.
The only remaining sub-5 is **apr18 ≈ 3.67–4.33** — a hard *reasoning* question (model
over-reaches on "why not the final taxonomy"); near the model's ceiling, not a tooling
gap. (apr17's old description below is now historical.)

## Key methodological lesson
Single-run scoreboards are unreliable here: the same v5 answer set scored 4.30 and 4.70
on different judgings. Only N≥3 averaging separated signal (relationships, Opus) from
noise (everything ±0.1). The eval harness is the durable asset.

## Recommended config
- `ENGRAM_REL=on` (default), relationships layer + 30-day reflection guard.
- `ENGRAM_MODEL=opus` for max score (≈4.83); `sonnet` (≈4.70) if the 60s/command limit
  or cost matters — Opus answers are slower. Declare model choice in the submission README.
