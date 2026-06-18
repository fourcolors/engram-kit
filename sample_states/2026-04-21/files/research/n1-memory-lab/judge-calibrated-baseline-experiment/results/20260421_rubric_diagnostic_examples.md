# 2026-04-21 Rubric Diagnostic Examples

Status: descriptive exploration only.

Source:

- [20260421_measurement_audit.json](./20260421_measurement_audit.json)

## Schema Adherence Snapshot

Pooled GPT-family judge:

- full 12-axis `R2 = 0.754`
- drop `continuity.state_transition_tracking`: `R2 = 0.738`
- `state_transition_tracking` only: `R2 = 0.606`

Pooled Opus judge:

- full 12-axis `R2 = 0.862`
- drop `continuity.state_transition_tracking`: `R2 = 0.840`
- `state_transition_tracking` only: `R2 = 0.731`

Descriptive read: `state_transition_tracking` carries substantial verdict
signal, but dropping it does not collapse the full model. This keeps open both
possibilities:

- it is a real load-bearing primitive;
- it is a high-correlation proxy for a broader continuity judgment.

No decision is made here.

## Factor-Collapse Examples

### GPT-family Judge

Top correlations:

- `continuity.active_thread_selection` vs `continuity.salience_relevance`:
  `r = 0.841`
- `continuity.salience_relevance` vs `continuity.continuation_value`:
  `r = 0.841`
- `continuity.active_thread_selection` vs `continuity.continuation_value`:
  `r = 0.718`
- `continuity.salience_relevance` vs `continuity.state_transition_tracking`:
  `r = 0.717`

Descriptive read: GPT-family judging clusters active-thread selection,
salience, continuation value, and state-transition tracking into a broad
continuity factor.

### Opus Judge

Top correlations:

- `continuity.active_thread_selection` vs `continuity.continuation_value`:
  `r = 0.911`
- `continuity.salience_relevance` vs `continuity.continuation_value`:
  `r = 0.876`
- `continuity.active_thread_selection` vs `continuity.salience_relevance`:
  `r = 0.855`
- `continuity.continuation_value` vs `coherence.cross_session_consistency`:
  `r = 0.845`

Descriptive read: Opus judging has an even stronger continuity cluster. It
appears to treat active thread, salience, and continuation value as nearly the
same judgment.

## Concrete Cells To Inspect Against The Rubric

- `R03/pure`: full-band judge disagreement on whether commit-trail evidence is
  enough when live cutoff state may have shifted.
- `R05/production`: full-band disagreement on broad priority/thread map
  reconstruction.
- `R19/zero`: full-band disagreement on which "latest" thread is authoritative.
- `R08/*`: storage-state vs work-state confusion, useful for checking whether
  active-thread criteria are doing the intended work.
- `R14/*`: unsupported durable-memory persistence claims and latest-session
  surface ambiguity.

These are example cells for further inspection, not adjudicated results.

