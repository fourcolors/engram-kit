# 2026-04-21 Abstention and False-Premise Calibration (JCB-057)

Status: first-pass deterministic proxy calibration using existing artifacts only (no new model calls, no architecture ranking).

Inputs:

- `results/20260421_calibration_subset_triage.md`
- `results/20260421_high_priority_claim_audit.md`
- `results/20260421_calibration_cell_matrix.json`
- `datasets/claim_audit_template.json`

## Proxy Abstention Criteria (Explicit)

Cell unit: `probe_id + condition`.

`audit_false_premise_signal` is true when the claim audit for a cell contains at least one `contradicted` tag or explicit false-premise cues:

- wrong world-model
- false no-traces premise
- invented
- wrong evidence surface
- no recoverable threads
- wrong-thread
- misframes

`triage_false_premise_signal` is true when triage disagreement/focus contains strong false-premise markers:

- wrong world-model
- empty/meta-state
- fabricated/invented UUID-thread links
- meta-report instead of thread map
- wrong-thread
- no-traces

`matrix_severe_disagreement_signal` is true when at least one answer in the cell is `full_band` or `invalid_or_missing`.

Final proxy rule:

- `abstain_or_escalate_proxy = audit_false_premise_signal OR triage_false_premise_signal OR matrix_severe_disagreement_signal`
- `accepted_proxy = NOT abstain_or_escalate_proxy`

## Headline Results

- Cells total: `30`
- Acceptance rate: `13/30 = 0.4333`
- Abstention/escalation proxy rate: `17/30 = 0.5667`

## Coverage and Accepted-Set Metrics (JCB-022 / JCB-023 Support)

- Accepted answer coverage: `26/60 = 0.4333`
- Abstained answer coverage: `34/60 = 0.5667`
- Accepted-set answer exact-rate: `0.5385`
- Accepted-set answer non-exact rate: `0.4615`
- Accepted-set cell both-exact rate: `0.3077`
- Accepted-set audited false-premise leak rate: `0.0` (0 leaked out of 10 audited false-premise cells)

## Disagreement Concentration in Abstained Cells

- Cell-level disagreement concentration in abstained cells: `12/21 = 0.5714`
- Answer-level non-exact disagreement concentration in abstained cells: `16/28 = 0.5714`
- Severe disagreement concentration (`full_band` or `invalid_or_missing`) in abstained cells: `5/5 = 1.0`

## False-Premise Capture

- Audited cells with false-premise signal: `10`
- Audited false-premise cells abstained: `10`
- Audited false-premise capture rate: `1.0`
- Triage false-premise cells: `6`
- Triage false-premise cells abstained: `6`

## Notes

- This is a proxy calibration, not human-labeled abstention ground truth.
- Some abstained cells are false-premise catches despite exact judge-pair agreement, which is expected under this proxy.

Changed file paths:

- `/Users/saxenauts/Documents/personal/syke-replay-lab/research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_abstention_false_premise_audit.md`
- `/Users/saxenauts/Documents/personal/syke-replay-lab/research/n1-memory-lab/judge-calibrated-baseline-experiment/datasets/abstention_false_premise_cells.json`
- `/Users/saxenauts/Documents/personal/syke-replay-lab/research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_abstention_coverage_metrics.json`
