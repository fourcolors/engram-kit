# Search Log — Non-Deterministically Verifiable Judging Literature Scan (April 2026)

Session: 2026-04-21.
Purpose: harvest the frontier of LLM-as-judge for semi-verifiable / reconstruction tasks, verify every arxiv ID, download PDFs, produce a Field Map.

## Searches Run (WebSearch)

1. `"LLM-as-judge" "non-verifiable" OR "reference-free" rubric reliability 2025` — canonical term sweep.
2. `"reward hacking" "non-verifiable" reward RLHF judge 2025` — non-verifiable reward frame.
3. `arxiv 2509.20293 "When Judgment Becomes Noise"` — verify project ID.
4. `arxiv 2603.01865 CyclicJudge` — verify project ID.
5. `"claim extraction" "per-claim" grading LLM judge arxiv 2025` — PROMPT surface.
6. `"verifier agent" OR "judge agent" tool use LLM evaluation arxiv 2025` — AGENT surface.
7. `"IRT" "item response theory" LLM-as-judge arxiv 2025 2026` — MATH surface.
8. `Prometheus fine-grained rubric LLM judge arxiv` — classic PROMPT.
9. `"G-Eval" NLG evaluation chain-of-thought GPT-4 arxiv` — classic PROMPT.
10. `MT-Bench chatbot arena "LLM-as-a-judge" Zheng 2023 arxiv` — classic FOUNDATION.
11. `"reward model" "rubric reward" "rubric-based reward" RLHF open-ended arxiv 2025` — MATH / PROMPT crossover.
12. `Autorubric unifying rubric meta-evaluation arxiv 2603.00077` — verify new.
13. `"construct validity" LLM evaluation benchmark measurement arxiv 2025` — FOUNDATION.
14. `"reference-free" evaluation "open-ended" generation reliability arxiv 2025` — term sweep.
15. `"FActScore" factuality long-form generation claim-level arxiv` — classic PACKET.
16. `"FineSurE" rubric faithfulness factuality summarization LLM judge arxiv` — classic PACKET.
17. `"DeepSeek" "GRM" generative reward model rubric arxiv 2025` — AGENT scaling.
18. `"scalable oversight" debate critique evaluation open-ended arxiv 2024 2025` — term sweep.
19. `"judge bias" position bias verbosity bias LLM evaluator arxiv 2025` — MATH biases.
20. `"process reward model" "PRM" verification long-form reasoning arxiv 2025` — MATH / AGENT.
21. `"grounded" "reference answer" judge context evidence LLM evaluation arxiv 2025` — PACKET.
22. `"multi-session" agent memory benchmark evaluation arxiv 2025 2026` — FOUNDATION task-class.
23. `"conformal prediction" LLM-as-judge uncertainty coverage arxiv 2025` — MATH.
24. `"subjective tasks" evaluation LLM open-ended rubric reliability 2025` — term sweep.
25. `"JudgeBench" "judge benchmark" "verifier benchmark" arxiv` — FOUNDATION.
26. `"Rubrics as Rewards" reinforcement learning beyond verifiable arxiv 2507.17746` — term anchor.
27. `"abstention" "I don't know" selective prediction LLM evaluation arxiv 2025` — AGENT.
28. `"atomic claim" decomposition evaluation LLM long-form reliability arxiv 2025` — PROMPT.
29. `"anchor examples" "calibrated" rubric judge few-shot arxiv 2024 2025` — PROMPT.

## Verification Fetches (WebFetch)

Verified 24 arxiv landing pages directly (title+author+abstract check): 2509.20293, 2603.01865, 2503.05061, 2603.14732, 2407.18370, 2601.08654, 2404.18796, 2602.13110, 2602.16313, 2410.10813, 2603.03781, 2404.07972, 2408.08781, 2603.00077, 2602.00521, 2511.04703, 2507.17746, 2410.12784, 2410.10934, 2509.18658, 2411.15594, 2410.02736, 2507.05257, 2504.02495, 2501.03200, 2501.00274, 2603.28005. All resolved to the claimed papers.

## Failed Retrievals

None. All 33 PDFs downloaded from `arxiv.org/pdf/{ID}` on first attempt, each >200KB with a valid PDF header.

## Project-Map IDs Flagged

**None.** Every arxiv ID in the project's existing `JUDGE_DESIGN_LITERATURE_MAP_20260420.md` (2603.01865 CyclicJudge, 2509.20293 When Judgment Becomes Noise, 2503.05061 No Free Labels, 2603.14732 Criterion-Referenceability, 2408.08781 Evaluating the Evaluator, 2407.18370 Trust or Escalate, 2601.08654 RULERS, 2404.18796 PoLL, 2602.13110 SCOPE, 2602.16313 MemoryArena, 2410.10813 LongMemEval, 2603.03781 LifeBench, 2404.07972 OSWorld) was verified. The user's worry about fabricated 2026 IDs did not materialize — the 2603.xxxxx IDs are legitimate late-February / March 2026 arxiv submissions, not model hallucinations.

## Papers Considered But Not Downloaded

Deliberately excluded to avoid bloat:
- OpenRubrics (2510.07743): overlaps with RaR 2507.17746 on synthetic rubric generation.
- Self-Rewarding Rubric RL (2509.25534): overlaps with RaR 2507.17746 and DeepSeek-GRM.
- "When AIs Judge AIs" (2508.02994): survey-style; Agent-as-a-Judge (2410.10934) is the primary source.
- "From Generation to Judgment" (2411.16594): secondary survey; Gu 2024 (2411.15594) is the chosen survey.
- Rubrics to Tokens (2604.02795) and Chasing the Tail (2509.21500): token-level rubric RL; too far from judge design for this scan.
- AbstentionBench (2506.09038): orthogonal — about policies abstaining, not judges.
- LLMs-as-Judges Comprehensive Survey (2412.05579): redundant with Gu 2024.

## Things Not Found (Genuine Gaps in the Literature)

- No paper on **partially verifiable operative-state reconstruction** under that or adjacent names.
- No paper on **n=1 judge psychometrics** (one-user-many-sessions regime).
- No paper treating **a bounded filesystem-with-provenance** as the evidence packet object.
- No **"continuity across sessions"** as a first-class judged rubric axis.
- No **reconstruction-for-continuation** as success criterion (as opposed to task-completion or answer-correctness).

See FIELD_MAP §5 for the full gap analysis.

## Time

Approximately 25 minutes of searching + 2 minutes of PDF downloads + writing. 29 web searches, 27 verification fetches, 33 PDFs downloaded.
