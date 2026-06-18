# Zero-Condition Bounded-Packet Smoke Test (JCB-052)

Date: 2026-04-21

Status: completed from existing artifacts only (no new LLM calls).

Inputs:
- `results/20260421_calibration_subset_packets.json`
- `results/20260421_calibration_cell_matrix.json`
- `results/20260421_high_priority_claim_audit.md`
- `datasets/probe_metadata.json`

Output dataset:
- `datasets/zero_condition_cells.json`

## Method

Filtered the 30-cell calibration matrix to `condition=zero` and joined probe-level packet metadata plus high-priority claim-audit excerpts. This is a bounded-packet smoke test only; no architecture ranking and no relabeling of truth.

## Headline Numbers

- Zero-condition cells: 10
- Zero-condition answer rows: 20
- Tool calls in zero rows: 525 total, mean 26.25, min 8, max 75
- Rows with tool calls > 0: 20/20 (1.000)
- Cross-judge pair categories (zero): exact 7, adjacent 11, full_band 1, invalid_or_missing 1
- Non-exact rate (zero): 12/20 (0.600)
- Combined judge verdict counts (zero): partial 18, pass 10, fail 11, invalid 1

Cross-condition comparison from the same matrix:
- Production non-exact: 8/20 (0.400), mean tools 26.4
- Pure non-exact: 6/20 (0.300), mean tools 28.25
- Zero non-exact: 12/20 (0.600), mean tools 26.25

## Caveats

- Scope is the current 30-cell calibration subset, not a full-condition estimate.
- One zero row (`R14`, `gpt-5.4`) is `invalid_or_missing`, so agreement-based interpretation has a known hole.
- High-priority zero rows include stale-snapshot and wrong-evidence-surface failures; these are carried as caveats, not rejudged here.

