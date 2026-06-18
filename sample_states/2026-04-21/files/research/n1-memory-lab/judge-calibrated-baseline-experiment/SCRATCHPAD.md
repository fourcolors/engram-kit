# Scratchpad

This file is for live thinking that is not yet a claim.

## Current Hypotheses

- The next useful result is not a new architecture run. It is a measurement
  validity report over existing judge artifacts.
- A small rubric with explicit `cannot_determine` may outperform the current
  larger rubric by reducing boundary flicker.
- The strongest next ablation is reverse-dropping `state_transition_tracking`.
- A human-reviewed calibration subset of 20-40 cells may be enough to identify
  the largest judge pathologies.
- Probe type should become a first-class variable before any ranking.

## Experimental Bias To Watch

- We may overfit to the current 19-probe slice.
- We may replace one overcomplicated rubric with another.
- We may let paper-method ambition outrun available data.
- We may confuse good artifact checking with good memory evaluation.

## Working Ideas

- Build a "measurement report" before a "system report."
- Keep `zero` as a bounded condition and add explicit source visibility.
- Report per-probe stories before per-condition means.
- Make failed/partial cells diagnostically rich enough for prompt/rubric
  evolution later.



## 2026-04-21 Recalibration After End-to-End Pass

- Executed most remaining calibration tasks using direct artifact analyses and proxy runs where reruns were unavailable.
- Open bottlenecks are now explicit: human labels (`JCB-021`) and clean repeated generations (`JCB-030`).
- Next quality lift is replacing proxy runs (`JCB-026/027/041`) with explicit reruns once execution budget/data windows are available.
- Continue to keep architecture ranking out of scope until alpha/beta terms are estimable.
