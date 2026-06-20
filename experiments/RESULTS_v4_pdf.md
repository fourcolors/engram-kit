# v4 + PDF (ENGRAM_PDF on) — regression check

Same memory/indexes (timeline.json + pdf_index/), v4 config, PDF retrieval ON,
re-judged by the same 20 Opus agents.

## Scorecard

| Metric | v4 | v4 + PDF |
|---|---|---|
| Responsiveness | 5.00 | 5.00 |
| Groundedness | 4.70 | 4.50 |
| Uncertainty calibration | 4.30 | 4.10 |
| **Overall** | **4.60** | **4.50** |
| Hindsight leaks | 0 | 0 |

Per-question overall (v4 → v4+PDF): apr17 **4→5** ↑ (only Q that used a PDF),
apr18 3→4 ↑, apr10 5→4 ↓, apr20 4→3 ↓, apr21_probe 5→4 ↓, rest unchanged.

## Reading

- **No PDF-caused regression.** Only **apr17** injected a PDF
  (`KAGGLE_CROSS_HARNESS_WRITEUP.pdf`, present from Apr 17) — and it improved
  4→5, leak-free. The three −1 moves are on questions where **no PDF was
  injected**, so they are run-to-run judge/answer noise, not PDF effects.
- All answers 0 hallucinated paths, all <60s.
- The feature is correctly selective: 1 of 10 questions had a topically-relevant
  in-state PDF; the 34 academic papers scored 0 for the lab-specific questions and
  were not used.

## Calibration note (important)
Identical-config reruns swing individual borderline questions ±1 (apr17 has scored
both 4 and 5 across runs). So **±0.1 overall is noise.** 4.60 vs 4.50 is a tie.
This confirms v2 (4.30) and v3 (4.40) were genuinely net-neutral, and that v4's
**+0.20** (three laggards up together) is the one delta large enough to be signal.

## Decision
**Keep `ENGRAM_PDF` default OFF (opt-in).** It only helps when a question depends
on an in-state document; on the 9 lab-specific questions it's a relevance pass for
no gain. Turn it on for document-dependent question sets. The capability is proven
(see the MemoryAgentBench demo in RESEARCH_pageindex_pdf.md / earlier run).
