# Open Questions

## Instrument Questions

- What is the smallest rubric that preserves discriminative power?
- Does `state_transition_tracking` survive reverse ablation?
- Which cells should be `cannot_determine` rather than `partial`?
- How much same-judge instability is tolerable before a judge is unusable?
- Which judge families share errors despite nominal diversity?

## Packet Questions

- Which probes are high criterion-referenceability?
- Which probes are search tasks, reconstruction tasks, or mixed tasks?
- Which probes need explicit `target_slice = tip | landscape | both`?
- Is the bounded packet too rich for a memory claim, or correctly rich for the
  condition being tested?

## Calibration Questions

- How small can the human-reviewed calibration subset be while still catching
  obvious judge failures?
- Do paraphrase variants preserve verdicts where they should?
- Does a correct reference improve discrimination, or only distribution match?
- What does a base-rate judge score on this packet?

## Future Method Questions

- When is CyclicJudge worth the extra orchestration?
- Can conformal intervals be justified despite temporal clustering?
- Can an IRT-style item model handle ordinal/noisy judge observations?
- Should adaptive rubrics be task-family-specific but frozen before scoring?

