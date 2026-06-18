# Run Log

## 2026-04-21

Created dedicated experiment space:

```text
research/n1-memory-lab/judge-calibrated-baseline-experiment/
```

Initial docs:

- `README.md`
- `EXPERIMENT_CHECKLIST.md`
- `PAPER_MAP.md`
- `PROTOCOL.md`
- `CALIBRATION.md`
- `THREATS_TO_VALIDITY.md`
- `GLOSSARY.md`
- `CLAIM_LEDGER.md`
- `OPEN_QUESTIONS.md`
- `SCRATCHPAD.md`
- `notes/CREATIVE_PRESSURES.md`

Key premise saved:

- `zero` is a valid bounded-packet condition, not a no-tool condition.
- `pass/partial/fail` are noisy observations, not truth labels.
- The current goal is measurement-instrument validation before architecture
  ranking.

Paper batches reviewed with subagents:

- rubric coherence and RRD;
- CyclicJudge and bias-bounded evaluation;
- criterion-referenceability and No Free Labels;
- RULERS and Trust/Escalate;
- Rating Roulette and grading scale;
- conformal intervals and judgment distribution;
- IRT and construct validity;
- LLM-Rubric and Likert;
- Autorubric and AdaRubric;
- rubric-conditioned grading and correlated errors;
- KalshiBench and robustness;
- fixed-parameter IRT and agreeableness bias;
- self-preference and imperfect verifier;
- PoLL and SCOPE;
- MemoryArena and LongMemEval;
- LifeBench and OSWorld;
- Evaluating the Evaluator and LLM-as-a-Verifier.

Next recommended work:

1. Denominator audit.
2. Same-answer judge-swap table.
3. Same-judge repeat table.
4. Schema-adherence recomputation.
5. Factor-collapse matrix.
6. Reverse ablation for `state_transition_tracking`.
7. Probe-level criterion-referenceability labels.

## 2026-04-21 Initial Measurement Audit

Created machine-readable tracker:

```text
TASKS.json
STATUS.json
```

Ran:

```text
scratch/20260421_measurement_audit.py
```

Artifacts:

```text
results/20260421_measurement_audit.json
results/20260421_measurement_audit.md
```

Completed task IDs:

- `JCB-010` denominator audit
- `JCB-011` same-answer judge-swap analysis
- `JCB-012` same-judge repeat analysis
- `JCB-013` schema adherence
- `JCB-014` factor collapse
- `JCB-015` reverse ablation for `state_transition_tracking`
- `JCB-017` useful/fail collapse diagnostic
- `JCB-031` judge stochasticity
- `JCB-032` judge identity

Headline results:

- Canonical GPT final: `57/57` valid.
- Canonical Opus final: `57/57` valid.
- GPT answers scored by Opus: `54/57` valid.
- Opus answers scored by GPT-mini: `57/57` valid.
- GPT answers, GPT judge vs Opus judge: overlap `54`, exact `0.481`,
  weighted kappa `0.239`, mean delta `+0.500`, useful exact `0.870`.
- Opus answers, Opus judge vs GPT-mini judge: overlap `57`, exact `0.509`,
  weighted kappa `0.340`, mean delta `-0.491`, useful exact `0.912`.
- Opus same-answer four-call repeat: `45` common-valid cells, flip rate
  `0.422`, `19` adjacent flips, `0` full-band flips, mean cell sigma `0.187`.
- Available GPT-mini same-judge repeat: `51` common-valid cells, flip rate
  `0.490`, `25` adjacent flips, `0` full-band flips, mean cell sigma `0.231`.
- GPT-judge pooled rubric diagnostics: full `R2=0.754`, drop
  `state_transition_tracking` `R2=0.738`, state-transition-only `R2=0.606`.
- Opus-judge pooled rubric diagnostics: full `R2=0.862`, drop
  `state_transition_tracking` `R2=0.840`, state-transition-only `R2=0.731`.

Caveats:

- Available GPT repeats are `gpt-5.4-mini` judge-config repeats, not clean full
  `gpt-5.4` intrarater repeats.
- Old `ab07` rows are replication checks, not canonical Apr 20 architecture
  evidence.
- OLS diagnostics are audit calculations, not final psychometrics.
- Architecture ranking remains out of scope.

Next recommended tasks:

1. `JCB-020` create probe metadata table.
2. `JCB-006` declare target state type per probe.
3. `JCB-007` partition probe types.
4. `JCB-008` assign criterion-referenceability labels.
5. `JCB-009` select 20-40 cell human-reviewed calibration subset.

## 2026-04-21 Probe Metadata And Calibration Subset

Created:

```text
datasets/probe_metadata.json
datasets/human_calibration_subset.json
```

Completed task IDs:

- `JCB-020` create probe metadata table.
- `JCB-006` declare target state type per probe.
- `JCB-007` partition probe types.
- `JCB-008` assign criterion-referenceability labels.
- `JCB-009` select 20-40 cell human-reviewed calibration subset.

Probe metadata summary for `R01-R19`:

- Target slices: `tip=6`, `historical=6`, `both=2`, `landscape=5`.
- Criterion-referenceability: `high=6`, `medium=9`, `low=4`.
- Retrieval character: `search-like=13`, `reconstruction-like=6`.

Human calibration subset:

- `30` cells selected.
- Probes: `R03`, `R05`, `R07`, `R08`, `R09`, `R13`, `R14`, `R15`,
  `R18`, `R19`.
- Conditions: `production`, `pure`, `zero`.
- Status: selected, not reviewed.

Next recommended tasks:

1. Human-review or agent-assisted first pass over the 30 selected cells.
2. Create a claim-audit template for each selected cell.
3. Extract concrete examples for the rubric diagnostics report.
4. Plan a small paraphrase robustness subset.

## 2026-04-21 Calibration Packets And Triage

Created:

```text
scratch/20260421_prepare_calibration_subset.py
results/20260421_calibration_subset_packets.json
results/20260421_calibration_subset_packets.md
datasets/claim_audit_template.json
datasets/paraphrase_robustness_plan.json
results/20260421_calibration_subset_triage.md
```

Completed task IDs:

- `JCB-046` prepare calibration subset packets.
- `JCB-047` agent-assisted first-pass triage of calibration subset.
- `JCB-048` plan paraphrase robustness subset.

First-pass triage is not human ground truth. It identified high-priority human
review cells:

- `R03/pure`
- `R07/zero`
- `R08/production`
- `R08/pure`
- `R08/zero`
- `R09/production`
- `R09/zero`
- `R14/production`
- `R14/pure`
- `R14/zero`
- `R19/production`
- `R19/pure`
- `R19/zero`

Emerging pattern:

- Most selected cells look like answer quality, freshness/current-state target
  ambiguity, packet insufficiency, or rubric ambiguity.
- There are few clean judge-bias-only cases.
- This supports claim-level audit before architecture ranking.

Next recommended tasks:

1. Run claim-level audit on the high-priority cells.
2. Extract concrete examples for the rubric diagnostics report.
3. Run or simulate the paraphrase robustness subset after claim audit.
4. Decide whether `R18` packet insufficiency needs packet repair before judging.

## 2026-04-21 High-Priority Claim Audit

Created:

```text
results/20260421_high_priority_claim_audit.md
```

Completed task ID:

- `JCB-049` agent-assisted claim-level audit of high-priority calibration cells.

Audited high-priority cells from:

- `R03`
- `R07`
- `R08`
- `R09`
- `R14`
- `R19`

Recurring failure modes:

- unsupported durable-memory persistence claims (`syke.db`, MEMEX refreshed);
- stale or wrong thread selection for tip-state asks;
- storage-state confused with work-state;
- invented identifiers or overtrusted UUID/thread handles;
- uncheckable or inflated numeric counts;
- packet insufficiency for replay-design history;
- generation timeout that should be classified separately from answer failure.

Next recommended tasks:

1. Extract concrete examples for the rubric diagnostics report.
2. Run or simulate paraphrase robustness subset after claim audit.
3. Decide whether `R18` packet insufficiency needs packet repair before judging.
4. Promote recurring failure modes into future rubric failure-attribution categories.

## 2026-04-21 Timed Exploration Pass

User requested a 20-minute exploration/analysis/research pass with no decisions.

Created:

```text
scratch/20260421_exploration_counts.py
results/20260421_exploration_counts.json
results/20260421_exploration_counts.md
results/20260421_calibration_cell_matrix.json
results/20260421_calibration_cell_matrix.csv
results/20260421_calibration_cell_matrix.md
results/20260421_failure_pattern_taxonomy.json
results/20260421_phrase_density.json
results/20260421_rubric_diagnostic_examples.md
results/20260421_length_tool_stats.json
results/20260421_length_tool_stats.md
results/20260421_20min_exploration_memo.md
```

Completed task ID:

- `JCB-050` timed exploration pass over calibration subset artifacts.

Exploration notes:

- Exact judge agreement is stability evidence, not correctness evidence.
- `R08` is dominated by storage-state vs work-state confusion.
- `R19` has split evidence surfaces between LM Studio/model work and
  sandbox/replay work.
- `R18` and `R19` share the same slice shape but ask different questions over
  it.
- Several answer handles are extremely dense in the raw slice, supporting
  separation of retrieval/search surface from reconstruction quality.


## 2026-04-21 Foundations + MEMEX + Neuroscience Alignment Pass

Delegated two parallel research passes:

- `Bacon` (foundations alignment against checklist/tracker).
- `Sagan` (computational-neuroscience construct-to-metric mapping).

Created artifacts:

```text
results/20260421_foundations_memex_neuro_alignment.md
results/20260421_foundations_memex_neuro_alignment.json
results/20260421_task_axis_taxonomy.md
results/20260421_task_axis_taxonomy.json
```

Completed task IDs:

- `JCB-061` foundations+MEMEX alignment synthesis.
- `JCB-062` neuroscience construct mapping synthesis.
- `JCB-063` recall-vs-beyond-recall taxonomy matrix.

Added long-horizon extension lane:

- `JCB-051` through `JCB-060` (construct validity, zero-condition smoke,
  temporal-first, session-boundary, provenance lineage, retrieval-vs-answer,
  abstention calibration, judge-family sensitivity, rubric compactness, failure atlas).

Scope guardrails retained:

- `zero` remains a valid bounded-packet condition.
- `pass/partial/fail` remain noisy ordinal observations.
- this pass makes no architecture-ranking claim.
- Syke record ID: `069e7dea`.


## 2026-04-21 Construct-Validity Reclassification (JCB-051 First Pass)

Created:

```text
results/20260421_construct_validity_audit.md
datasets/construct_validity_labels.json
```

Task update:

- `JCB-051` moved to `in_progress`.

First-pass method:

- metadata-based construct classification for all `R01-R19` probes;
- phrase-surface enrichment where available (`R08`, `R18`, `R19` only);
- explicit caveat that full phrase-density coverage is not yet complete.

No architecture comparison generated.


## 2026-04-21 Foundations Extension Tranche 1 (JCB-053/JCB-055/JCB-056)

Created:

```text
results/20260421_temporal_disambiguation_audit.md
results/20260421_provenance_lineage_audit.md
results/20260421_claim_lineage_matrix.csv
results/20260421_retrieval_vs_answer_split.md
```

Task updates:

- `JCB-053` completed (first pass).
- `JCB-055` completed (first pass).
- `JCB-056` completed (first pass).

Key first-pass numbers:

- Temporal audit (high-priority audited subset): 11/32 observations flagged for temporal ambiguity keywords.
- Lineage template completeness in calibration packets: empty `claim_audit` 60/60; null `target_state` 60/60.
- Retrieval-vs-answer split coverage: 60 observations in matrix, 32 joined with lineage rows.

Scope guardrail retained:

- no architecture ranking claim; descriptive calibration diagnostics only.


## 2026-04-21 End-to-End Execution Pass (Subagent + Local)

Executed and closed remaining executable tasks with two parallel subagent lanes plus local analyses.

Completed task IDs:

- JCB-019, JCB-022, JCB-023, JCB-026, JCB-027, JCB-028, JCB-029, JCB-033, JCB-037, JCB-038, JCB-041, JCB-051, JCB-052, JCB-054, JCB-057, JCB-058, JCB-059, JCB-060

Key artifacts added in this pass:

```text
results/20260421_zero_condition_smoke_test.md
datasets/zero_condition_cells.json
results/20260421_session_boundary_audit.md
datasets/session_boundary_checks.json
results/20260421_abstention_false_premise_audit.md
datasets/abstention_false_premise_cells.json
results/20260421_abstention_coverage_metrics.json
results/20260421_judge_family_sensitivity.md
results/20260421_judge_family_sensitivity.json
results/20260421_probe_difficulty_audit.md
results/20260421_probe_difficulty_audit.json
results/20260421_failure_attribution_table.md
results/20260421_failure_attribution_table.csv
results/20260421_rubric_minimal_vs_full_diag.md
results/20260421_rubric_minimal_vs_full_diag.json
results/20260421_failure_atlas_examples.md
results/20260421_unsupported_false_premise_probe_set.md
datasets/unsupported_false_premise_probe_set.json
results/20260421_retrieval_answer_axis_separation.md
results/20260421_paraphrase_robustness_proxy.md
results/20260421_paraphrase_robustness_proxy.json
results/20260421_reference_perturbation_proxy.md
datasets/reference_perturbation_cells.json
```

Open tasks after this pass:

- blocked: `JCB-021`
- deferred by design: `JCB-018`, `JCB-024`, `JCB-025`
- needs new clean data: `JCB-030`
- continuous maintenance: `JCB-043`, `JCB-044`, `JCB-045`

Guardrail retained: no architecture ranking claim.
- Syke record ID: `069e7ebd`.


## 2026-04-21 Generation Variance Readiness Gate (JCB-030)

Created:

```text
results/20260421_generation_variance_readiness_audit.md
results/20260421_generation_variance_readiness_audit.json
```

Task update:

- `JCB-030` moved from `pending` to `blocked` with explicit data requirements for clean generation-variance estimation.

- Syke record ID: `069e7ec2`.
