# Protocol

Status: draft protocol for measurement-instrument validation.

## Experiment Type

This is a judge-calibrated baseline experiment. The first phase validates the
measurement instrument. Architecture ranking is out of scope until the
instrument passes reliability and validity gates.

## Unit Of Evaluation

```text
I_t = (t, q_t, E_t, r_t)
```

Required packet fields:

- `reference_time`
- `ask_text`
- `evidence_packet_id`
- `condition`
- `condition_flags`
- `answer_text`
- `answer_model`
- `answer_provider`
- `answer_trace_id`
- `judge_model`
- `judge_provider`
- `judge_prompt_version`
- `rubric_version`
- `judge_run_id`
- `prompt_order`
- `temperature`
- `source_ids`

## Condition Flags

Every condition must be explicit:

```yaml
condition_flags:
  packet_bound: bounded | none | full
  tool_allowed: true | false
  retrieval_allowed: true | false
  source_visibility:
    slice: true | false
    memex: true | false
    synthesis: true | false
    git_anchor: true | false
  judge_blinded_to_condition: true | false
```

## Zero Condition Rule

`zero` is valid if it reads inside its bounded packet. It is not a no-tool
condition. It should be compared as:

```text
bounded substrate without synthesis/control
```

not:

```text
memory absent and retrieval forbidden
```

## Judge Output Schema

Required judge result fields:

- `criteria[]`
- `claim_audit[]`
- `final_observation`
- `confidence`
- `cannot_determine_reason`
- `escalation_recommended`
- `failure_attribution`

Valid final observations:

- `pass`
- `partial`
- `fail`
- `cannot_determine`
- `invalid`

The first three are noisy ordinal observations, not ground-truth labels.

## Claim Audit Schema

Each important answer claim should be typed:

```yaml
claim:
  text: string
  type: verified | inferred | speculative | unsupported | contradicted | uncheckable
  evidence_ids: [string]
  check_method: deterministic | judge_semantic | human_review
  notes: string
```

## Phase 1 Gates

Proceed only if the current stage passes these gates:

1. Packet schema complete for all evaluated cells.
2. Rubric version frozen.
3. Same-judge repeat exists for at least a calibration subset.
4. Same-answer judge-swap exists for at least a calibration subset.
5. Criteria are visible separately from final observation.
6. `cannot_determine` is used when evidence is insufficient.
7. Failure attribution distinguishes answer, packet, rubric, and judge failures.

## Phase 2 Calculations

Use the calculation order in [EXPERIMENT_CHECKLIST.md](./EXPERIMENT_CHECKLIST.md):

1. Denominator audit.
2. Same-answer judge swap.
3. Same-judge repeat.
4. Schema adherence.
5. Factor collapse.
6. Reverse ablation.
7. Criterion-referenceability proxy.
8. Self/family preference.
9. Robustness.
10. Human calibration subset.

## Phase 3 Architecture Ranking Gate

Architecture ranking is allowed only after:

- rubric diagnostics are stable;
- repeated judge reliability is characterized;
- judge identity effects are reported;
- generation variance is measured;
- a verified calibration subset exists;
- packet/condition semantics are not ambiguous.

