# Evidence Lineage Completeness Audit (JCB-055)

Date: 2026-04-21

Status: first-pass lineage audit over the high-priority claim-audit subset.

Inputs:
- `results/20260421_high_priority_claim_audit.md`
- `results/20260421_calibration_subset_packets.json`
- `datasets/claim_audit_template.json`

Output matrix: `results/20260421_claim_lineage_matrix.csv`.

## Tag Distribution (Parsed Claim Statuses)

- verified: 66 (0.493)
- inferred: 29 (0.216)
- speculative: 1 (0.007)
- unsupported: 10 (0.075)
- contradicted: 19 (0.142)
- uncheckable: 9 (0.067)

## Per-Answer Lineage Quality (Audited Subset)

- Answer observations parsed: 32
- Mean supported-tag rate (`verified+inferred`): 0.696
- Mean unsupported-bundle rate (`unsupported+contradicted+uncheckable`): 0.296

## Template Completeness (Calibration Packets)

- Answers with empty `review_template.claim_audit`: 60/60 (1.000)
- Answers with null `review_template.target_state`: 60/60 (1.000)

## First-Pass Read

- Narrative claim-status tags provide useful signal, but machine `claim_audit` fields remain empty in current packets.
- Next calibration pass should write explicit `claim_text -> evidence_ids` rows per answer in the packet template, not only markdown prose.
- This is a lineage instrumentation audit, not a correctness claim.
