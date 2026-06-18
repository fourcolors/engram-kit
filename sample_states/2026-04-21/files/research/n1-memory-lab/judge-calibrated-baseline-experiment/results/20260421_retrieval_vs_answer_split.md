# Retrieval-vs-Answer Split Report (JCB-056)

Date: 2026-04-21

Status: first-pass split using retrieval proxies (tool calls), judge disagreement categories, and claim-quality tags where audited.

## Dataset Coverage

- Calibration matrix observations: 60 (30 cells x 2 answer sources)
- Joined with claim-lineage rows: 32

## Retrieval Load vs Non-Exact Judge Outcome

- low_retrieval_tools_0_14: non-exact 4/9 (0.444), mean length 1413.4
- mid_retrieval_tools_15_29: non-exact 14/31 (0.452), mean length 3199.4
- high_retrieval_tools_30_plus: non-exact 10/20 (0.500), mean length 3722.2

## Claim-Quality Overlay (Audited Subset Join)

- Non-exact rate in joined subset: 15/32 (0.469)
- Answers with unsupported-bundle rate > 0.25: 12/32 (0.375)

## First-Pass Read

- Retrieval effort and answer quality are separable axes and should stay separated in reporting.
- Lineage-tag burden varies across answers and is not reducible to retrieval volume alone.
- This split is diagnostic only and keeps architecture ranking out of scope.
