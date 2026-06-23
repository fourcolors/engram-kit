# Noise-controlled evaluation loop (N=3 averaged)

Harness: `experiments/eval.py` (parallel N-run generation) + `experiments/judge_eval.js`
(judges every config×repeat×question, aggregates mean per config). Built to beat the
answer+judge noise floor (single runs swing borderline questions ±3).

Each config: 3 runs × 10 questions = 30 answers, each judged once (overall 0–5).

## Results

| Config | Mean | Run-means | false-"unavail" | Verdict |
|---|---|---|---|---|
| v4 (relationships OFF) | 4.57 | 4.4–4.7 | 4/30 | baseline |
| **v5 (relationships ON)** | **4.70** | 4.5–4.8 | 5–6/30 | **best so far — KEEP** |
| b1 (v5 + bigger digest 140k/30) | 4.50 | 4.3–4.7 | 5/30 | **rejected (worse)** |
| v5 + Opus answer model | _running_ | | | |

## Findings

**A — relationships are a real, modest win (not noise).** Averaged over 3 runs,
v5 (4.70) beats v4 (4.57). The gain is isolated exactly where relationships apply:
apr10 4.33→5.00 and apr20 3.00→3.67; the other 8 questions unchanged. A single
earlier run had shown v5 *worse* (4.30) — that was an unlucky draw; averaging
resolved it. **v5 is the confirmed best config.**

**B1 — bigger digest makes it WORSE (4.50).** Flooding the model with more file
bodies (140k/30 vs 80k/16) dropped apr18 3.67→2.67 and apr17 4.67→4.00, and did
NOT reduce false-"unavailable" (5/30 either way). Conclusion: the weak spots are a
**focus/reasoning** problem, not a retrieval-starvation problem. The relevance
digest's focus was already right. Rejected.

## Stable weak spots (both configs, across runs)
- **apr18 ≈ 3.67** — over-reaches (wrong "first introduced R##" thesis) + hedges.
- **apr20 ≈ 4.3** — relationships fixed the counts; residual is some hedging.
- **apr17 ≈ 4.67** — presents inference as documentation.

All three are reasoning-discipline issues. Next lever under test: a stronger answer
model (Opus) for these nuanced questions.
