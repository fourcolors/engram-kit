# 2026-04-21 Measurement Audit

Pass/partial/fail are treated as noisy ordinal observations, not truth labels.

## Denominator Highlights

| run | items | valid | invalid | pass | partial | fail |
|---|---:|---:|---:|---:|---:|---:|
| gpt_final | 57 | 57 | 0 | 6 | 41 | 10 |
| opus_final | 57 | 57 | 0 | 28 | 21 | 8 |
| gpt_answers_opus_judge | 57 | 54 | 3 | 26 | 25 | 3 |
| opus_answers_gpt_judge | 57 | 57 | 0 | 5 | 39 | 13 |
| opus_intra_rep1 | 57 | 55 | 2 | 26 | 19 | 10 |
| opus_intra_rep2 | 57 | 49 | 8 | 27 | 15 | 7 |
| opus_intra_rep3 | 57 | 53 | 4 | 27 | 17 | 9 |
| gpt_mini_intra_rep1 | 57 | 57 | 0 | 9 | 43 | 5 |
| gpt_mini_intra_rep5 | 57 | 54 | 3 | 13 | 36 | 5 |
| gpt_mini_intra_rep6 | 57 | 54 | 3 | 10 | 38 | 6 |

## Same-Answer Judge Swaps

| comparison | overlap | exact | weighted kappa | mean delta | useful exact |
|---|---:|---:|---:|---:|---:|
| gpt_answers__gpt_judge_vs_opus_judge | 54 | 0.481 | 0.239 | 0.500 | 0.870 |
| opus_answers__opus_judge_vs_gpt_mini_judge | 57 | 0.509 | 0.340 | -0.491 | 0.912 |
| old_gpt_answers__gpt_judge_vs_ab07_opus_rep1 | 54 | 0.463 | 0.277 | 0.500 | 0.852 |

## Same-Judge Repeats

| group | common valid | flip rate | adjacent flips | full-band flips | mean cell sigma |
|---|---:|---:|---:|---:|---:|
| opus_answers__opus_judge_4_calls | 45 | 0.422 | 19 | 0 | 0.187 |
| gpt_answers__gpt_mini_judge_available_calls | 51 | 0.490 | 25 | 0 | 0.231 |
| old_gpt_answers__ab07_opus_3_calls | 57 | 0.456 | 25 | 1 | 0.221 |

## Rubric Diagnostics

| judge pool | full R2 | drop state-transition R2 | state-transition-only R2 | max abs axis corr |
|---|---:|---:|---:|---:|
| gpt_judge_pooled | 0.754 | 0.738 | 0.606 | 0.841 |
| opus_judge_pooled | 0.862 | 0.840 | 0.731 | 0.911 |

## Caveats

- GPT intrarater repeat rows currently available here are gpt-5.4-mini judge-config repeats, not clean full gpt-5.4 repeats.
- Old ab07 rows are useful replication checks, not canonical Apr 20 architecture evidence.
- OLS uses a stdlib normal-equation solver and should be treated as an audit calculation, not final psychometrics.
