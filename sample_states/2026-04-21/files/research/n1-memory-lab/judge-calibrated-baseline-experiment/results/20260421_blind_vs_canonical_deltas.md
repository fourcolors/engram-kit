# Blind-Packet vs Canonical Deltas — 2026-04-21

Paired comparison: same Apr 20 answers, rejudged once with the full identity packet (canonical) and once with SYKE_BLIND_PACKET=1 (double-blind).

## Per-arm shift

| Arm | n | Shift (blind − canon) | 3-level κ | Any flip | Full-band |
|---|---|---|---|---|---|
| gpt-ans-gpt-judge | 57 | -0.0351 | 0.587 | 10/57 | 0 |
| gpt-ans-opus-judge | 53 | +0.0189 | 0.6179 | 13/53 | 0 |
| opus-ans-opus-judge | 56 | -0.1607 | 0.6523 | 14/56 | 1 |
| opus-ans-gpt-judge | 56 | -0.3036 | 0.3948 | 19/56 | 0 |

## σ_γ comparison (opus-judge minus gpt-judge on SAME gpt-agent answers)

- Canonical (identity visible): **0.5** (n=54)
- Blind (identity masked):     **0.5273** (n=55)
- Attributable to identity leak: **-0.0273**

## The 22/54 asymmetry under blind

- Opus-higher cells: 26 / 55 (was 22/54)
- GPT-higher cells:  0 / 55 (was 0/54)
- Ties/mixed:        29 / 55 (was 32/54)