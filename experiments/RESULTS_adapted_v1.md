# Adapted v1 vs stock — results

Same memory (151-line MEMORY.md, observer/update pass unchanged), Sonnet 4.6,
same 20-Opus adversarial judging. Adapted v1 changed only the **answer** side:
relevance-ranked digest with full bodies of question-relevant files (#1),
date-filtered no-hindsight memory (#2), prompt that bans false "unavailable" +
separates memory from evidence (#4).

## Scorecard

| Metric | Stock | Adapted v1 | Δ |
|---|---|---|---|
| Responsiveness | 3.50 | **4.90** | +1.40 |
| Groundedness | 2.60 | **4.40** | +1.80 |
| Uncertainty calibration | 2.30 | **4.10** | +1.80 |
| **Overall** | **2.60** | **4.40** | **+1.80** |
| Hindsight leaks | 1 major | **0** | fixed |
| Hallucinated evidence paths | 0/50 | 0/47 | held |
| Max answer latency | 96s | 47s | under 60s |

Per-question overall (stock → v1): apr08 4→5, apr10 2→4, apr13 4→5,
**apr14 1→5**, apr17 5→5, apr18 2→2, apr19 2→5, apr20 3→3,
apr21_instrument 2→5, **apr21_probe 1→5**. No regressions; 7 perfect 5s.

- Both catastrophic refusals (apr14, apr21_probe) recovered to 5 — the full-body
  relevance digest + false-unavailable ban fixed the dominant stock failure.
- apr10 hindsight leak closed by date-filtering; reached the boundary verdict
  from reference-time evidence alone.

## Remaining weaknesses (concentrated in 2 high-fan-out states)

- **apr18 (overall 2):** attribution errors — claims the TSV "first" introduced
  R## (already in canonical V2.yaml); misattributes the 2026-03-09 window start.
  The false-unavailable hedge **resurfaced in the uncertainty field** (claimed
  two present files "not reproduced"), masking the error.
- **apr20 (overall 3):** wrong lead aggregate — "all 80 files approximate→exact"
  when changes.txt shows 23 approx→exact, 57 unavailable→exact, 22 deleted; and
  the same false-unavailable hedge on 4 present files.
- Minor: phantom `MEMORY.md` in memory_refs (apr10/13/14/20) — harmless but a
  non-existent workspace path.

## Ranked v2 adaptations

1. **Kill the residual false-unavailable hedge at the root** — hard post-check:
   forbid any "unavailable/not shown/inferred" phrase about a file whose name is
   in the provided manifest. (Highest leverage; through-line of every sub-4.)
2. **Attribution/aggregation verify pass** — re-ground every "X stated in FILE",
   count, and transition-aggregate before finalizing; for transition questions
   report the changes.txt breakdown, not one aggregate.
3. **"First/novel/introduced" claims require a prior-state check.**
4. **Surface in-corpus conflicts** instead of resting on one boundary.
5. **Tighten relevance digest on large states** — raise body budget and/or always
   include the full present-file manifest so "not in my digest" ≠ "not in workspace".
6. **Strip phantom MEMORY.md from memory_refs.**

Net: v1 is a decisive win (+1.8 overall, zero leaks, both refusals recovered).
The agent-memory observer pass (unchanged) is strong; the gains came from fixing
answer-side retrieval. Last blockers are 2 high-fan-out states; fix #1 is the
single most leveraged remaining change.
