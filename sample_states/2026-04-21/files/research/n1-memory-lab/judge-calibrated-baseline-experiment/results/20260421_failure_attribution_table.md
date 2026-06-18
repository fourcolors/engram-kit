# Failure Attribution Table (JCB-038)

Date: 2026-04-21

Status: first-pass attribution extracted from high-priority claim-audit failure narratives.

Output table: `results/20260421_failure_attribution_table.csv`.

Category counts:
- stale_state_selection: 15
- contradicted_evidence: 13
- reference_ambiguous: 12
- unsupported_inference: 12
- wrong_restart_risk: 5
- answer_wrong: 4

Notes:
- Categories are mapped via keyword rules from claim-audit "Failure:" lines.
- This is a diagnostic attribution table, not a gold-label error decomposition.
