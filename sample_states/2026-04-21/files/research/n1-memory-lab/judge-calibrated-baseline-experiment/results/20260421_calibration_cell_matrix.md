# Calibration Cell Matrix

Descriptive matrix only. No decisions.

| probe | cond | target | ref | char | GPT pair | Opus pair |
|---|---|---|---|---|---|---|
| R03 | production | both | medium | search-like | partial→pass (adjacent) | pass→partial (adjacent) |
| R03 | pure | both | medium | search-like | fail→pass (full_band) | partial→fail (adjacent) |
| R03 | zero | both | medium | search-like | partial→partial (exact) | partial→fail (adjacent) |
| R05 | production | landscape | medium | search-like | partial→pass (adjacent) | pass→fail (full_band) |
| R05 | pure | landscape | medium | search-like | partial→partial (exact) | partial→partial (exact) |
| R05 | zero | landscape | medium | search-like | partial→pass (adjacent) | pass→partial (adjacent) |
| R07 | production | historical | high | search-like | partial→pass (adjacent) | partial→partial (exact) |
| R07 | pure | historical | high | search-like | partial→partial (exact) | pass→partial (adjacent) |
| R07 | zero | historical | high | search-like | fail→fail (exact) | partial→partial (exact) |
| R08 | production | tip | low | reconstruction-like | fail→fail (exact) | partial→partial (exact) |
| R08 | pure | tip | low | reconstruction-like | partial→partial (exact) | fail→fail (exact) |
| R08 | zero | tip | low | reconstruction-like | fail→partial (adjacent) | fail→fail (exact) |
| R09 | production | landscape | medium | search-like | fail→partial (adjacent) | partial→partial (exact) |
| R09 | pure | landscape | medium | search-like | pass→partial (adjacent) | partial→partial (exact) |
| R09 | zero | landscape | medium | search-like | fail→partial (adjacent) | fail→fail (exact) |
| R13 | production | historical | low | reconstruction-like | partial→pass (adjacent) | pass→pass (exact) |
| R13 | pure | historical | low | reconstruction-like | pass→pass (exact) | pass→pass (exact) |
| R13 | zero | historical | low | reconstruction-like | partial→pass (adjacent) | pass→partial (adjacent) |
| R14 | production | tip | high | search-like | partial→invalid (invalid_or_missing) | partial→partial (exact) |
| R14 | pure | tip | high | search-like | partial→pass (adjacent) | partial→partial (exact) |
| R14 | zero | tip | high | search-like | partial→invalid (invalid_or_missing) | pass→partial (adjacent) |
| R15 | production | tip | high | search-like | partial→partial (exact) | pass→partial (adjacent) |
| R15 | pure | tip | high | search-like | partial→partial (exact) | partial→partial (exact) |
| R15 | zero | tip | high | search-like | pass→pass (exact) | pass→partial (adjacent) |
| R18 | production | historical | low | reconstruction-like | partial→partial (exact) | partial→partial (exact) |
| R18 | pure | historical | low | reconstruction-like | partial→pass (adjacent) | partial→partial (exact) |
| R18 | zero | historical | low | reconstruction-like | partial→pass (adjacent) | partial→partial (exact) |
| R19 | production | tip | medium | search-like | fail→fail (exact) | fail→fail (exact) |
| R19 | pure | tip | medium | search-like | partial→partial (exact) | partial→partial (exact) |
| R19 | zero | tip | medium | search-like | fail→partial (adjacent) | pass→fail (full_band) |
