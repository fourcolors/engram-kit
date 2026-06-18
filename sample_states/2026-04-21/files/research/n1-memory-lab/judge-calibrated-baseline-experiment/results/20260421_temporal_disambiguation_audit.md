# Temporal-First Disambiguation Audit (JCB-053)

Date: 2026-04-21

Status: first-pass descriptive audit. No architecture ranking decisions.

Method: combines claim-audit temporal-keyword flags on high-priority cells with pair-category disagreement by target slice in the 30-cell calibration matrix.

## Temporal-Risk Summary (High-Priority Claim-Audit Subset)

- Audited answer observations: 32
- Temporal-flagged observations: 11 (0.344)

By target slice (claim-audit subset):
- both: 3/6 flagged (0.500)
- historical: 0/6 flagged (0.000)
- landscape: 2/4 flagged (0.500)
- tip: 6/16 flagged (0.375)

## Judge Disagreement By Target Slice (Calibration Matrix)

- both: non-exact 5/6 (0.833), full-band 1/6 (0.167)
- historical: non-exact 7/18 (0.389), full-band 0/18 (0.000)
- landscape: non-exact 7/12 (0.583), full-band 1/12 (0.083)
- tip: non-exact 9/24 (0.375), full-band 1/24 (0.042)

## Freshness-Sensitive Probe Proxy

- Freshness-sensitive probes (`R03`,`R08`,`R14`,`R19`): non-exact 12/24 (0.500)
- Other probes: non-exact 16/36 (0.444)

## First-Pass Read

- Temporal ambiguity appears frequent in audited high-priority cells, especially where 'latest' selection and chronology ordering are load-bearing.
- This supports a temporal-first normalization step before judging: explicit cutoff timestamp, explicit target surface (`tip` vs `landscape`), and explicit stale-thread penalty labeling.
- This is a diagnostic audit only; it does not resolve truth labels or architecture quality.
