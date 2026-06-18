# Experiment Checklist

Status: active operating checklist.

This checklist is the working plan for designing a judge-calibrated baseline for
Syke. It preserves the paper sweep and the local correction that `zero` is a
valid bounded-packet condition, not a no-tool condition.

## Non-Negotiable Premise

`pass`, `partial`, and `fail` are noisy ordinal observations. They are not
truth labels.

The observed score is:

```text
Y = Judge(r_t, q_t, E_t, rubric, model, scale, prompt_order, stochasticity)
```

The experiment validates `Y` before using it for architecture rankings.

## Full Checklist

### Construct And Packet Definition

1. Define the benchmark construct before the judge.
   - Required wording: "This eval measures bounded reconstruction of the
     closest correct operative state at time `t` for useful continuation."

2. Define each packet as data, not prose.
   - Required fields: `t`, `q_t`, `E_t`, `r_t`, condition, model, prompt,
     judge model, rubric version, source IDs, evidence packet path,
     retrieval/tool policy, temperature, ordering, run ID.

3. Separate condition semantics from tool behavior.
   - Required flags: `packet_bound`, `tool_allowed`, `retrieval_allowed`,
     `source_visibility`, `memex_visible`, `synthesis_visible`.

4. Keep `zero` valid.
   - Rule: `zero` is not "no tools." It is a bounded condition without the
     synthesis/control layer. If tools read inside the bounded packet, that is
     condition behavior, not leakage.

5. Declare the target state type.
   - Required field: `target_slice = tip | landscape | both | historical |
     provenance`.

6. Partition probe types.
   - Required labels: `search`, `reconstruction`, `temporal_update`,
     `object_continuity`, `cross_surface`, `committed_truth`, `provenance`,
     `abstention`.

7. Decide criterion-referenceability per probe.
   - Mark each probe as `high`, `medium`, or `low` referenceability before
     judging.

8. Build a tiny verified reference subset.
   - Minimum: hand-label enough cells to calibrate obvious judge errors,
     same-family/self-preference, and `cannot_determine`.

### Evidence And Rubric Contract

9. Use deterministic checks as evidence, not the whole verdict.
   - Checks: time-locality, named artifact existence, commit/session/file
     support, direct contradiction, unsupported absence claims.

10. Force claim typing.
    - Claim types: `verified`, `inferred`, `speculative`, `unsupported`,
      `contradicted`, `uncheckable`.

11. Lock the baseline rubric.
    - Rule: baseline rubric is frozen, versioned, and hashed. Adaptive rubrics
      can suggest future axes but cannot mutate the baseline mid-run.

12. Use atomic criteria.
    - Rule: one construct per criterion. Prefer binary or 3-level criteria
      unless calibration proves a finer scale works.

13. Keep criteria separate from final verdict.
    - Output fields: per-criterion score, evidence, rationale, confidence,
      final verdict, escalation flag.

14. Add explicit non-verdict outcomes.
    - Required labels: `cannot_determine`, `insufficient_evidence`,
      `packet_insufficient`, `rubric_ambiguous`, `needs_human_review`.

15. Run minimal-rubric and full-rubric A/B.
    - Calculation: compare agreement with gold subset and stability under
      reruns. More rubric text must earn its keep.

### Rubric Diagnostics

16. Measure schema adherence.
    - Calculation:

```text
verdict ~ criterion_scores
R2, adjusted R2, bootstrap CI
```

17. Measure factor collapse.
    - Calculation:

```text
corr(axis_i, axis_j)
```

18. Run reverse ablation.
    - Specific next test: remove `state_transition_tracking` and recompute
      `R2`. If `R2` survives, that axis is not uniquely primitive.

19. Measure intra-rater reliability first.
    - Calculation: rerun same judge, same answer, same packet. Report exact
      agreement, weighted kappa, Krippendorff alpha if applicable, flip type,
      per-probe instability.

20. Treat `pass/partial/fail` as ordinal language.
    - Rule: do not treat `pass=2`, `partial=1`, `fail=0` as metric except as
      a crude descriptive statistic.

21. Use stable binary collapse only as a diagnostic.
    - Candidate collapse: `useful = pass | partial`, `not_useful = fail`.
      It is a stability view, not the whole benchmark truth.

### Judge Bias And Reliability

22. Counterbalance pairwise order.
    - Rule: every pairwise comparison must run `A/B` and `B/A`, then average
      or flag position sensitivity.

23. Measure judge identity effect.
    - Calculation:

```text
Delta_judge = score_judgeA(same answer) - score_judgeB(same answer)
weighted kappa
exact agreement
McNemar on useful/fail
```

24. Measure same-family/self-preference.
    - Calculation: compare overestimation for judge's own model family versus
      unrelated model family.

25. Measure correlated judge errors.
    - Calculation: on gold subset, estimate pairwise wrong-wrong overlap, not
      just disagreement.

26. Do not treat consensus as truth.
    - Rule: panel agreement is evidence of stability, not correctness. Keep
      disagreement distributions.

27. Add abstention and escalation.
    - Rule: low-confidence or high-disagreement cells should route to human
      review or stronger judge, not be forced into `pass/partial/fail`.

28. Track coverage separately from accuracy.
    - Required metrics: accepted-set accuracy, coverage, abstention rate,
      escalation rate.

### Calibration And Robustness

29. Measure calibration if probabilities exist.
    - Calculations: Brier score, Brier Skill Score, expected calibration error,
      reliability curve.

30. Use base-rate baselines.
    - Rule: compare against always-base-rate / majority-class / trivial judge.
      If judge does not beat base rate, stop.

31. Run paraphrase robustness.
    - Rule: semantically equivalent asks should not radically change verdict
      unless ambiguity is real.

32. Run reference perturbations.
    - Conditions: no reference, correct reference, self-generated reference,
      corrupted reference, random reference.

33. Separate retrieval quality from answer quality.
    - Required fields: evidence found, evidence used, answer claims, supported
      claims, unsupported claims.

34. Include unsupported/false-premise probes.
    - Rule: a valid memory system must say "not enough evidence" when
      appropriate.

### Variance Decomposition

35. Track generation variance separately.
    - Calculation:

```text
same model, same condition, same probe, repeated answer generations
```

36. Track judge stochasticity separately.
    - Calculation:

```text
same answer, same judge, repeated judge calls
```

37. Track judge identity separately.
    - Calculation:

```text
same answer, different judges
```

38. Track probe difficulty separately.
    - Calculation:

```text
per-probe instability and success distribution across conditions/judges
```

### Later Methods Gate

39. Delay CyclicJudge until rubric is stable.
    - Rule: use CyclicJudge only after schema adherence, factor collapse, and
      intra-rater reliability pass minimum gates.

40. Delay conformal intervals until calibration assumptions hold.
    - Requirements: held-out calibration set, fixed judge/prompt/version,
      exchangeability plausible, ordinal score distribution available.

41. Delay IRT until labels are stable.
    - Requirements: anchor items, repeated model responses, stable item bank,
      binary or modeled ordinal outcomes, enough observations.

42. Preserve examples before aggregates.
    - Reporting order: examples, disagreement matrix, per-probe instability,
      rubric diagnostics, then aggregate scores.

43. Publish failure attribution.
    - Failure labels: answer wrong, packet insufficient, reference ambiguous,
      judge error, rubric ambiguous, unsupported inference, contradicted
      evidence, stale-state selection.

44. Keep memory-task neighbors in scope.
    - Design pressure from MemoryArena, LongMemEval, and LifeBench:
      multi-session, time-stamped, cross-source, update-aware,
      abstention-capable tasks.

45. Keep executable checks where possible.
    - Design pressure from OSWorld: if a claim can be checked by
      state/script/artifact, do that before asking an LLM judge.

## Use Now

- Packet schema and condition flags.
- Criterion-referenceability labels.
- Locked small rubric.
- Evidence attribution.
- Same-judge repeats.
- Same-answer judge swaps.
- Order swaps for pairwise comparisons.
- Schema adherence `R2`.
- Factor-collapse correlations.
- Reverse ablation for `state_transition_tracking`.
- Useful/fail collapse as diagnostic.
- Small human-reviewed calibration subset.
- Failure attribution table.

## Use Later

- CyclicJudge panel rotation.
- IRT / PSN-IRT / fixed-parameter calibration.
- Conformal intervals.
- Bias-bounded guarantees.
- Brier Skill Score, unless probabilistic or binary labels exist.
- Adaptive rubrics as baseline, unless generated rubrics are frozen per task
  family.
- Large scalar architecture rankings.

## Immediate Calculation Plan

1. Recompute denominators: expected cells, valid cells, missing cells, invalid
   cells per run.
2. Compute same-answer judge swap: exact agreement, weighted kappa, ordinal
   shift, useful/fail McNemar.
3. Compute same-judge repeat: exact agreement, weighted kappa, flip type,
   per-probe instability.
4. Compute schema adherence: `verdict ~ subaxis_scores`.
5. Compute factor collapse: subaxis correlation matrix.
6. Compute reverse ablation: remove `state_transition_tracking`, compare `R2`.
7. Compute criterion-referenceability proxy: claim support rate, artifact
   citation rate, uncheckable-claim rate.
8. Compute judge self/family preference if answer model and judge model
   families overlap.
9. Compute robustness: paraphrase a small probe subset and compare verdict
   movement.
10. Build a calibration subset with human labels for 20-40 cells before
    claiming more.

## Break And Recalibration Rule

Every major calculation batch should end with:

- What changed?
- What broke?
- Which assumptions were falsified?
- Which checklist items should be promoted, demoted, or rewritten?
- Is the next step more data, better labels, better rubric, or a pause?



## Foundations And MEMEX Extension (Exploration Only)

- Keep benchmark scaffolding separate from product architecture claims.
- Add temporal-first normalization before retrieval/scoring on freshness asks.
- Add explicit provenance-lineage audit for claim -> artifact mapping.
- Reclassify retrieval-degenerate cells as construct-validity confounds.
- Keep zero-condition interpretation fixed: bounded packet, tool use allowed inside packet.
- Split retrieval-surface access from reconstruction quality in reporting.
- Track batch-dynamic map behavior (pointer emergence, compression drift) as descriptive signals.
- Keep architecture ranking out of scope until alpha/beta/gamma/epsilon are estimable with clean labels.
