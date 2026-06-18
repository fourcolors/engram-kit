# Pooled re-read — 2026-04-22

Verification pass on the blind-vs-canonical picture. Adds SE bands, pooled sigma_gamma across both runs (n ~= 109), and a per-probe mix so we can see where the data is thick vs thin.

## Per-arm paired shift (blind − canon), with SE bands

| Arm | n | shift | SD(d) | SE | shift in SE | σ̂_ε = SD/√2 |
|---|---|---|---|---|---|---|
| gpt-ans-gpt-judge | 57 | -0.035 | 0.421 | 0.056 | -0.6 σ | 0.298 |
| gpt-ans-opus-judge | 53 | +0.019 | 0.500 | 0.069 | +0.3 σ | 0.353 |
| opus-ans-opus-judge | 56 | -0.161 | 0.532 | 0.071 | -2.3 σ | 0.376 |
| opus-ans-gpt-judge | 56 | -0.304 | 0.502 | 0.067 | -4.5 σ | 0.355 |

## Mean verdict by arm (0=fail, 1=partial, 2=pass)

| Arm | canon mean ± SE | blind mean ± SE | pooled mean ± SE |
|---|---|---|---|
| gpt-ans-gpt-judge | 0.930 ± 0.070 | 0.895 ± 0.060 | 0.912 ± 0.046 |
| gpt-ans-opus-judge | 1.426 ± 0.082 | 1.418 ± 0.092 | 1.422 ± 0.061 |
| opus-ans-opus-judge | 1.351 ± 0.095 | 1.196 ± 0.097 | 1.274 ± 0.068 |
| opus-ans-gpt-judge | 0.860 ± 0.073 | 0.554 ± 0.067 | 0.708 ± 0.051 |

## Verdict distribution (pooled across canon + blind)

| Arm | pass | partial | fail | n |
|---|---|---|---|---|
| gpt-ans-gpt-judge | 9 | 86 | 19 | 114 |
| gpt-ans-opus-judge | 55 | 45 | 9 | 109 |
| opus-ans-opus-judge | 49 | 46 | 18 | 113 |
| opus-ans-gpt-judge | 5 | 70 | 38 | 113 |

## σ_γ (opus − gpt on same GPT answers)

- Canonical: **+0.500** ± 0.078 (n=54)
- Blind:     **+0.527** ± 0.082 (n=55)
- Pooled:    **+0.514** ± 0.056 (n=109)  — 95% CI [0.404, 0.624]  — z vs 0 = 9.14
- Canon→blind shift:  Δ = +0.027, SE(Δ) = 0.113  → +0.24 σ (inside noise)

## σ_γ asymmetry — pooled (opus_higher / gpt_higher / ties out of n)

- **53 / 1 / 55** out of **109** pooled pairs.
  Opus-higher rate = 48.62% · GPT-higher rate = 0.92%.

## Per-probe profile — sorted by pooled mean score (0=fail..2=pass)

| probe_id | n votes | pass | partial | fail | mean | pass% | fail% |
|---|---|---|---|---|---|---|---|
| R08 | 24 | 1 | 7 | 16 | 0.38 | 4% | 67% |
| R19 | 24 | 3 | 7 | 14 | 0.54 | 12% | 58% |
| R09 | 24 | 3 | 10 | 11 | 0.67 | 12% | 46% |
| R07 | 24 | 2 | 15 | 7 | 0.79 | 8% | 29% |
| R10 | 23 | 5 | 10 | 8 | 0.87 | 22% | 35% |
| R03 | 24 | 6 | 11 | 7 | 0.96 | 25% | 29% |
| R01 | 24 | 5 | 15 | 4 | 1.04 | 21% | 17% |
| R18 | 23 | 4 | 16 | 3 | 1.04 | 17% | 13% |
| R06 | 22 | 5 | 13 | 4 | 1.04 | 23% | 18% |
| R14 | 21 | 4 | 15 | 2 | 1.09 | 19% | 10% |
| R02 | 24 | 6 | 17 | 1 | 1.21 | 25% | 4% |
| R04 | 24 | 7 | 15 | 2 | 1.21 | 29% | 8% |
| R11 | 24 | 6 | 17 | 1 | 1.21 | 25% | 4% |
| R05 | 24 | 8 | 15 | 1 | 1.29 | 33% | 4% |
| R12 | 24 | 11 | 10 | 3 | 1.33 | 46% | 12% |
| R15 | 24 | 8 | 16 | 0 | 1.33 | 33% | 0% |
| R17 | 24 | 8 | 16 | 0 | 1.33 | 33% | 0% |
| R16 | 24 | 10 | 14 | 0 | 1.42 | 42% | 0% |
| R13 | 24 | 16 | 8 | 0 | 1.67 | 67% | 0% |