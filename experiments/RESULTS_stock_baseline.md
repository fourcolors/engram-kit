# Stock agent-memory baseline on ENGRAM — results

Model: Sonnet 4.6 (observer + answer passes). 14 states, 10 questions.
Judged by 20 adversarial Opus agents (quality + hindsight per answer) + synthesis.

## Mechanical results
- Updates: 14/14 ok. Memory 13 → 151 lines (never hit 195 → reflector never fired).
- Answers: 10/10 schema-valid. 50 evidence paths cited, **0 hallucinated/invalid** (all exist in their reference-time state).
- Latency: updates 10–39s; answers 20–96s (**apr17 = 96s, over ENGRAM's 60s default**).

## Judged scorecard (0–5)
| Metric | Avg |
|---|---|
| Responsiveness | 3.50 |
| Groundedness | 2.60 |
| Uncertainty calibration | 2.30 |
| **Overall** | **2.60** |

Distribution: 3 strong (≥4), 1 mid (3), 6 weak (≤2). Hindsight leaks: **9 none, 1 major** (apr10).

## Dominant failure (NOT hindsight): false "content unavailable" refusals
The answer pass repeatedly declared a cited file unreadable/absent, then refused or
substituted weaker reasoning — when the file was fully present in the reference-time
state. Root cause is on the adapter side: `digest_answer_state` includes *small files
first* up to a 45 KB budget, so the large, information-dense files the questions target
(S07_VS_LOCOMO 15 KB, V2.yaml 30 KB, ASK_SAMPLING 19 KB, calibration files) are left as
tree-listing only — the model sees the name but not the body.

- apr14 (overall 1): refused on the 333-line file that *was the single file added that day*.
- apr21_probe_coverage_gaps (overall 1, calib 0): cited the exact file, said "any answer would be fabrication."
- apr19 (overall 2): fabricated "missing content" for JUDGE_PRIMITIVES; fell back to a wrong count-based proxy.
- apr13 (overall 4, calib 2): hedged V2.yaml "not readable" when it had a `status: canonical` header.
- apr20 (overall 3): claimed 3 calibration files "not readable" when all present + exact.

## Secondary issues
- **Hindsight leak (apr10, major):** used real-ask-history/ (Apr 12) + ask_demands (Apr 18) + a fabricated "superseded" memory label (term first appears Apr 20) in an Apr-10 answer.
- **Fabrication when starved:** apr10 invented a "2026-04-09 memory record"; apr18 said "all claude-code" reading only the R01–R06 preview (TSV is 1/3 opencode); apr21 fabricated "P## and R## IDs" (experiment uses only R01–R19).
- **MEMORY.md cited as corpus evidence** (apr10, apr14) — conflating own memory with workspace files.

## What works (do not regress)
- Reference-time discipline is genuinely strong (9/10 no leak); "verify evidence against current state" self-excludes future files.
- When it reads the file, answers are excellent (apr17 = 5, apr08 = 4); counts/byte-deltas verify cleanly.
- Honest hedging style; correct top-line conclusions even on weak answers (the failures are in supporting evidence, not the verdict).

## Ranked adaptations (from synthesis)
1. **Force full-body reads of cited files; ban "unavailable" when file is in-state.** Highest impact; fixes both 1s + several. Est. overall 2.6 → ~3.4+.
2. **Date-filtered no-hindsight retrieval** (cut at reference date). Fixes the apr10 leak.
3. **Reflector verify-against-source pass** (anti-fabrication; read whole file, not preview). Fixes apr18/apr10/apr21 groundedness.
4. **Exclude MEMORY.md from evidence selection** (memory is a hint, not corpus).
5. **Calibration: penalize false under-confidence**, only allow "cannot determine" after a confirmed failed read.
6. **Raise answer timeout >60s** (one answer hit 96s; reads add latency).
