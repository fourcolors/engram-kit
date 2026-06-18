# Calibration Subset Packets

These packets are for judge/rubric calibration, not architecture ranking.

| probe | condition | target | ref | character | GPT judges | Opus judges |
|---|---|---|---|---|---|---|
| R03 | production | both | medium | search-like | gpt-5.4_judge:partial, opus-4.6_judge:pass | opus-4.6_judge:pass, gpt-family_judge:partial |
| R03 | pure | both | medium | search-like | gpt-5.4_judge:fail, opus-4.6_judge:pass | opus-4.6_judge:partial, gpt-family_judge:fail |
| R03 | zero | both | medium | search-like | gpt-5.4_judge:partial, opus-4.6_judge:partial | opus-4.6_judge:partial, gpt-family_judge:fail |
| R05 | production | landscape | medium | search-like | gpt-5.4_judge:partial, opus-4.6_judge:pass | opus-4.6_judge:pass, gpt-family_judge:fail |
| R05 | pure | landscape | medium | search-like | gpt-5.4_judge:partial, opus-4.6_judge:partial | opus-4.6_judge:partial, gpt-family_judge:partial |
| R05 | zero | landscape | medium | search-like | gpt-5.4_judge:partial, opus-4.6_judge:pass | opus-4.6_judge:pass, gpt-family_judge:partial |
| R07 | production | historical | high | search-like | gpt-5.4_judge:partial, opus-4.6_judge:pass | opus-4.6_judge:partial, gpt-family_judge:partial |
| R07 | pure | historical | high | search-like | gpt-5.4_judge:partial, opus-4.6_judge:partial | opus-4.6_judge:pass, gpt-family_judge:partial |
| R07 | zero | historical | high | search-like | gpt-5.4_judge:fail, opus-4.6_judge:fail | opus-4.6_judge:partial, gpt-family_judge:partial |
| R08 | production | tip | low | reconstruction-like | gpt-5.4_judge:fail, opus-4.6_judge:fail | opus-4.6_judge:partial, gpt-family_judge:partial |
| R08 | pure | tip | low | reconstruction-like | gpt-5.4_judge:partial, opus-4.6_judge:partial | opus-4.6_judge:fail, gpt-family_judge:fail |
| R08 | zero | tip | low | reconstruction-like | gpt-5.4_judge:fail, opus-4.6_judge:partial | opus-4.6_judge:fail, gpt-family_judge:fail |
| R09 | production | landscape | medium | search-like | gpt-5.4_judge:fail, opus-4.6_judge:partial | opus-4.6_judge:partial, gpt-family_judge:partial |
| R09 | pure | landscape | medium | search-like | gpt-5.4_judge:pass, opus-4.6_judge:partial | opus-4.6_judge:partial, gpt-family_judge:partial |
| R09 | zero | landscape | medium | search-like | gpt-5.4_judge:fail, opus-4.6_judge:partial | opus-4.6_judge:fail, gpt-family_judge:fail |
| R13 | production | historical | low | reconstruction-like | gpt-5.4_judge:partial, opus-4.6_judge:pass | opus-4.6_judge:pass, gpt-family_judge:pass |
| R13 | pure | historical | low | reconstruction-like | gpt-5.4_judge:pass, opus-4.6_judge:pass | opus-4.6_judge:pass, gpt-family_judge:pass |
| R13 | zero | historical | low | reconstruction-like | gpt-5.4_judge:partial, opus-4.6_judge:pass | opus-4.6_judge:pass, gpt-family_judge:partial |
| R14 | production | tip | high | search-like | gpt-5.4_judge:partial, opus-4.6_judge:invalid | opus-4.6_judge:partial, gpt-family_judge:partial |
| R14 | pure | tip | high | search-like | gpt-5.4_judge:partial, opus-4.6_judge:pass | opus-4.6_judge:partial, gpt-family_judge:partial |
| R14 | zero | tip | high | search-like | gpt-5.4_judge:partial, opus-4.6_judge:invalid | opus-4.6_judge:pass, gpt-family_judge:partial |
| R15 | production | tip | high | search-like | gpt-5.4_judge:partial, opus-4.6_judge:partial | opus-4.6_judge:pass, gpt-family_judge:partial |
| R15 | pure | tip | high | search-like | gpt-5.4_judge:partial, opus-4.6_judge:partial | opus-4.6_judge:partial, gpt-family_judge:partial |
| R15 | zero | tip | high | search-like | gpt-5.4_judge:pass, opus-4.6_judge:pass | opus-4.6_judge:pass, gpt-family_judge:partial |
| R18 | production | historical | low | reconstruction-like | gpt-5.4_judge:partial, opus-4.6_judge:partial | opus-4.6_judge:partial, gpt-family_judge:partial |
| R18 | pure | historical | low | reconstruction-like | gpt-5.4_judge:partial, opus-4.6_judge:pass | opus-4.6_judge:partial, gpt-family_judge:partial |
| R18 | zero | historical | low | reconstruction-like | gpt-5.4_judge:partial, opus-4.6_judge:pass | opus-4.6_judge:partial, gpt-family_judge:partial |
| R19 | production | tip | medium | search-like | gpt-5.4_judge:fail, opus-4.6_judge:fail | opus-4.6_judge:fail, gpt-family_judge:fail |
| R19 | pure | tip | medium | search-like | gpt-5.4_judge:partial, opus-4.6_judge:partial | opus-4.6_judge:partial, gpt-family_judge:partial |
| R19 | zero | tip | medium | search-like | gpt-5.4_judge:fail, opus-4.6_judge:partial | opus-4.6_judge:pass, gpt-family_judge:fail |
