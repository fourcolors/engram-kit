# 2026-04-21 Judge-Family Sensitivity (JCB-058)

Scope: descriptive judge-calibration diagnostics from existing artifacts only; no architecture ranking.

## Inputs Used

- `results/20260421_measurement_audit.json`
- `results/20260421_calibration_cell_matrix.json`
- `results/20260421_exploration_counts.json`
- `notes/MATH_ONE_PAGER_20260421.md`

## Clean vs Confounded Comparisons

`pass/partial/fail` is treated as a noisy ordinal scale (`fail=0, partial=1, pass=2`).

| arm | comparison | overlap | mean delta (cross - same) | mean delta (same - cross) | exact | weighted kappa | useful exact | adjacent disagreement rate | full-band disagreement rate | sigma-scaled shift |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| clean | `gpt_answers__gpt_judge_vs_opus_judge` | 54 | +0.500 | -0.500 | 0.481 | 0.239 | 0.870 | 0.500 | 0.019 | 2.67x (`|0.500| / sigma_eps_opus=0.187`) |
| confounded | `opus_answers__opus_judge_vs_gpt_mini_judge` | 57 | -0.491 | +0.491 | 0.509 | 0.340 | 0.912 | 0.456 | 0.035 | 2.35x (`|0.491| / sigma_eps_proxy=0.209`) |

Clean-arm interpretation: on the same GPT answers, Opus judge scores higher than GPT judge by +0.500 ordinal points on average.

Confounded-arm interpretation: on the same Opus answers, Opus judge scores higher than GPT-family (mini) judge by +0.491 ordinal points on average (`same - cross`), but this arm entangles family effect and judge-tier effect (`gpt-5.4-mini` vs `claude-opus-4-6`).

## Effect-Size Style Cross-Arm Deltas

| metric | confounded - clean |
|---|---:|
| exact agreement | +0.027 |
| weighted kappa (linear) | +0.101 |
| useful exact (pass/partial vs fail) | +0.042 |
| binary kappa (pass/partial vs fail) | +0.301 |

## JCB-019 Linkage: Same-Family/Self-Preference Proxy

JCB-019 asks for same-family/self-preference. Using the two swap arms as a proxy:

- clean arm same-family effect (`same - cross`) = `-0.500`
- confounded arm same-family effect (`same - cross`) = `+0.491`
- proxy swing (`confounded - clean`) = `+0.991`

This sign flip is the quantified proxy effect linking JCB-058 to JCB-019: direction changes from anti-same-family (clean) to pro-same-family (confounded), with an almost one-band swing on the 0-2 ordinal scale. Because the Opus-answer arm uses `gpt-5.4-mini` as cross-family judge, treat this as a sensitivity proxy, not an isolated causal estimate of family preference.

Context anchor from `MATH_ONE_PAGER_20260421.md`: prior binary proxy note says Opus agent receives `+0.13` binary-agreement advantage from Opus judge.

## Supporting Subset Signal (Descriptive Only)

From `20260421_exploration_counts.json` (descriptive subset, not denominator-of-record):

- GPT-answer pair categories: `exact=13`, `adjacent=14`, `full_band=1`, `invalid_or_missing=2`
- Opus-answer pair categories: `exact=19`, `adjacent=9`, `full_band=2`

These subset counts are directionally consistent with the family-sensitive pattern but are not used as the calibration denominator.
