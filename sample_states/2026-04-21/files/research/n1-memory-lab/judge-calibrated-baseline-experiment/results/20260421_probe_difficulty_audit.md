# Probe Difficulty Audit (JCB-033)

Date: 2026-04-21

Status: first-pass diagnostic based on disagreement patterns in the 30-cell calibration matrix.

Method: per-probe non-exact/full-band/invalid pair-category rates across both answer sources (`n=6` observations per probe).

| Probe | Slice | Ref | Character | Non-exact | Full-band | Invalid | Difficulty |
|---|---|---|---|---|---|---|---|
| R03 | both | medium | search-like | 5/6 (0.833) | 1 | 0 | high_difficulty |
| R05 | landscape | medium | search-like | 4/6 (0.667) | 1 | 0 | high_difficulty |
| R07 | historical | high | search-like | 2/6 (0.333) | 0 | 0 | lower_difficulty |
| R08 | tip | low | reconstruction-like | 1/6 (0.167) | 0 | 0 | lower_difficulty |
| R09 | landscape | medium | search-like | 3/6 (0.500) | 0 | 0 | medium_difficulty |
| R13 | historical | low | reconstruction-like | 3/6 (0.500) | 0 | 0 | medium_difficulty |
| R14 | tip | high | search-like | 4/6 (0.667) | 0 | 2 | medium_difficulty |
| R15 | tip | high | search-like | 2/6 (0.333) | 0 | 0 | lower_difficulty |
| R18 | historical | low | reconstruction-like | 2/6 (0.333) | 0 | 0 | lower_difficulty |
| R19 | tip | medium | search-like | 2/6 (0.333) | 1 | 0 | high_difficulty |

Summary buckets:
- high difficulty: 3
- medium difficulty: 3
- lower difficulty: 4

This is a calibration-priority diagnostic, not a correctness or architecture score.
