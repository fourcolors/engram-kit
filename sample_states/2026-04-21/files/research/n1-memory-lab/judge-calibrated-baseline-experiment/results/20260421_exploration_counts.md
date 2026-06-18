# 2026-04-21 Exploration Counts

Scope: descriptive exploration only. No decisions, no architecture ranking.

Cells in calibration subset: `30`
Answer observations: `60`

## Metadata Counts

### Criterion Referenceability

- `medium`: 12
- `high`: 9
- `low`: 9

### Target Slice

- `both`: 3
- `landscape`: 6
- `historical`: 9
- `tip`: 12

### Retrieval Character

- `search-like`: 21
- `reconstruction-like`: 9

## Judge Pair Categories By Answer Source

- `gpt-5.4` / `adjacent`: 14
- `gpt-5.4` / `exact`: 13
- `gpt-5.4` / `full_band`: 1
- `gpt-5.4` / `invalid_or_missing`: 2
- `opus-4.6` / `adjacent`: 9
- `opus-4.6` / `exact`: 19
- `opus-4.6` / `full_band`: 2

## Triage Likely Cause Counts

- `answer quality`: 16
- `rubric ambiguity`: 11
- `packet insufficiency`: 3

## Claim Type Counts In High-Priority Audit

- `verified`: 50
- `inferred`: 14
- `contradicted`: 16
- `uncheckable`: 7
- `unsupported`: 10
- `speculative`: 1

## Phrase Counts In Claim Audit

- `unsupported`: 13
- `contradicted`: 20
- `uncheckable`: 14
- `stale`: 9
- `wrong thread`: 1
- `storage state`: 1
- `work state`: 3
- `uuid`: 6
- `counts`: 12
- `timeout`: 3
- `syke.db`: 7
- `memex`: 15

## Full-Band Or Invalid Examples

- `R03/pure` gpt-5.4: gpt-5.4_judge=fail vs opus-4.6_judge=pass (full_band)
- `R05/production` opus-4.6: opus-4.6_judge=pass vs gpt-family_judge=fail (full_band)
- `R19/zero` opus-4.6: opus-4.6_judge=pass vs gpt-family_judge=fail (full_band)
- `R14/production` gpt-5.4: gpt-5.4_judge=partial vs opus-4.6_judge=invalid (invalid_or_missing)
- `R14/zero` gpt-5.4: gpt-5.4_judge=partial vs opus-4.6_judge=invalid (invalid_or_missing)
