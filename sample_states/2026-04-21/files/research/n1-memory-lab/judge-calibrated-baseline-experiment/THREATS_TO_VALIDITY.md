# Threats To Validity

Status: active threat register.

## Judge Threats

- Same judge gives different results on rerun.
- Different judges define "current state" differently.
- Same-family judges over-reward same-family answers.
- Judges agree because of shared bias, not correctness.
- Rubric wording induces halo effects.
- Judges overvalue explicit artifact citations even when the answer is not useful.
- Judges undervalue subtle memory-informed behavior.

## Rubric Threats

- Axis collapse: multiple axes are one latent verdict.
- Schema incoherence: criteria do not explain final observations.
- Over-granularity: scale noise dominates signal.
- Under-granularity: pass/partial/fail hides distinct failure modes.
- Adaptive rubric drift: task-specific rubrics change the measuring stick.

## Packet Threats

- Condition flags are ambiguous.
- `zero` is misread as no-tool/no-retrieval.
- Evidence packet is too rich and turns memory into search.
- Evidence packet is too sparse and makes judging impossible.
- Time boundary is unclear.
- Source IDs are missing or stale.

## Probe Threats

- Probe is too easy or retrieval-degenerate.
- Probe lacks a clear target state.
- Probe mixes tip-state and landscape-state without declaring which matters.
- Probe is low criterion-referenceability but treated like an objective item.
- Probe set is temporally clustered and not exchangeable.

## Analysis Threats

- Ordinal labels are treated as metric values.
- Consensus is mistaken for correctness.
- Same-judge noise is ignored.
- Judge identity effect is mistaken for architecture effect.
- Generation variance is not measured.
- Examples are discarded too early in favor of aggregate scores.

## Mitigations

- Freeze packet schema.
- Freeze rubric version.
- Add claim audits.
- Add same-answer judge swaps.
- Add same-judge repeats.
- Add human-reviewed calibration subset.
- Publish examples and disagreement before aggregates.
- Use `cannot_determine` and escalation as first-class outcomes.

