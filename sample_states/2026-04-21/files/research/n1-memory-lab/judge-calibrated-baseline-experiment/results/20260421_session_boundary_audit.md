# Session-Boundary Preservation Audit (JCB-054)

Date: 2026-04-21

Status: completed from existing packets/cell-matrix/claim-audit artifacts only.

Inputs:
- `results/20260421_calibration_subset_packets.json`
- `results/20260421_calibration_cell_matrix.json`
- `results/20260421_high_priority_claim_audit.md`
- `datasets/probe_metadata.json`

Output dataset:
- `datasets/session_boundary_checks.json`

## Method

Declared a boundary-sensitive probe rule from metadata:
- include probes where `probe_types` contains any of `time_window`, `temporal_update`, `last_thread`, or `search`.

In this calibration subset, that rule selects `R03`, `R07`, `R13`, `R14`, `R15`, `R19` (18 cells, 36 answer rows). Pair-category and verdict signals are taken from the existing matrix. Claim-audit boundary flags are parsed only where high-priority markdown rows exist.

## Headline Numbers

- Boundary-sensitive cells: 18
- Boundary-sensitive answer rows: 36
- Pair categories: exact 18, adjacent 14, full_band 2, invalid_or_missing 2
- Non-exact rate: 16/36 (0.444)

By condition:
- Production: non-exact 5/12 (0.417), invalid_or_missing 1
- Pure: non-exact 4/12 (0.333), invalid_or_missing 0
- Zero: non-exact 7/12 (0.583), invalid_or_missing 1

By condition + answer source:
- `zero|opus-4.6`: non-exact 5/6 (0.833)
- `zero|gpt-5.4`: non-exact 2/6 (0.333)
- `production|gpt-5.4`: non-exact 3/6 (0.500)
- `production|opus-4.6`: non-exact 2/6 (0.333)
- `pure|gpt-5.4`: non-exact 2/6 (0.333)
- `pure|opus-4.6`: non-exact 2/6 (0.333)

Claim-audit boundary caveat counts (high-priority rows only):
- Evaluated rows: 24
- Boundary-flagged rows: 12 (0.500)
- Flag categories: stale/wrong-thread 7, session-or-timeline blur 5, evidence-surface miss 1

## Caveats

- Boundary-sensitive classification is rule-based from probe metadata and does not change ground-truth labels.
- Claim-audit boundary flags are null outside the high-priority markdown subset.
- This is descriptive and keeps architecture ranking out of scope.

