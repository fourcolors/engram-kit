# Scoring Method

> Implementation copy: `_internal/syke-replay-lab/probes/SCORING_METHOD_V3.md`

## Headline metric

**Success Rate / Pass@1** = `pass / total_judged`

This is the public headline.

An invalid item is a benchmark assembly failure or judge-run failure.
It is excluded from the denominator.

## What is scored

There are three reporting surfaces:

1. **Factual grounding** — judge-scored
2. **Continuity** — judge-scored
3. **Efficiency** — runner-scored from telemetry

Do not force all three into one composite.

## Verdict reduction

Use this reduction:

- evidence pack invalid or judge failed → `invalid`
- `factual_grounding = missed` → `fail`
- `continuity = missed` → `fail`
- `factual_grounding = strong` and `continuity = strong` → `pass`
- otherwise → `partial`

This keeps the public outcome binary and standard.

## Efficiency panel

Efficiency should be reported from raw run metadata, not judged into existence.

Recommended metrics:

- `zero_search_success_rate`
- `tool_calls_per_success`
- `cost_per_success`
- optional raw totals for tool calls and cost

These make future A/B testing relevant:

did the system help more often, and at what cost?

## Comparing two systems

Use McNemar's exact test on paired binary outcomes:

- `success = pass`
- `not success = partial or fail`

Rows where either side is `invalid` are excluded from the paired denominator.

Report:

- the 2x2 table
- exact p-value
- direction

Then report efficiency deltas separately.

## What to report

### Table 1: Verdict summary

- pass
- partial
- fail
- invalid
- success rate

### Table 2: Paired comparison

- McNemar table
- p-value
- one-sentence interpretation

### Table 3: Failure gallery

Mandatory.
Every failed probe, with the judge summary.

### Table 4: Probe-level results

Per probe:

- verdict
- factual grounding
- continuity
- efficiency telemetry

## Limitations

1. `N=50` is still small.
2. The judge is still an LLM and therefore noisy.
3. This remains one-user evaluation.
4. `partial` remains important diagnostically even though the public headline is binary success.
