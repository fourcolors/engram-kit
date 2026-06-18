# Calibration Plan

Status: draft.

## Measurement Layers

1. Packet validity.
2. Rubric validity.
3. Judge reliability.
4. Judge bias.
5. Answer-generation variance.
6. Probe difficulty.
7. Architecture comparison.

Do not skip earlier layers.

## Core Quantities

```text
sigma_alpha: probe difficulty / scenario effect
sigma_beta: answer-generation variance
sigma_gamma: judge identity effect
sigma_epsilon: same-judge residual stochasticity
```

Treat these as organizing variables first. Do not claim a mature variance
decomposition until the design supports it.

## Required Calibration Tables

### Denominator Table

```text
run_id
expected_cells
completed_cells
valid_judge_cells
invalid_judge_cells
missing_cells
conditions
probes
```

### Same-Answer Judge Swap

```text
answer_run_id
judge_a
judge_b
overlap
exact_agreement
weighted_kappa
ordinal_shift
useful_fail_mcnemar
```

### Same-Judge Repeat

```text
judge_model
answer_run_id
repeat_count
overlap
exact_agreement
weighted_kappa
flip_rate
adjacent_flip_count
full_band_flip_count
per_probe_instability
```

### Rubric Diagnostics

```text
rubric_version
criteria_count
schema_adherence_r2
adjusted_r2
bootstrap_ci
max_axis_correlation
near_zero_axes
reverse_ablation_results
```

### Bias Diagnostics

```text
judge_model
answer_model
same_family
overestimation_rate
underestimation_rate
wrong_wrong_overlap
position_bias_delta
```

## Reliability Gates

Initial gates are deliberately conservative:

- no architecture ranking from single-judge scores;
- no architecture ranking without same-answer judge swaps;
- no architecture ranking without same-judge repeats;
- no architecture ranking from a rubric with unexplained collapse;
- no scalar headline without examples and disagreement distributions.

## Later Calibration Methods

Use later, after the packet supports them:

- CyclicJudge panel rotation.
- Conformal intervals.
- IRT / fixed-parameter calibration.
- Bias-bounded perturbation guarantees.
- Brier Skill Score for probabilistic binary labels.

