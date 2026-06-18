# Judge Salvage Notes — 2026-04-17

Working note for understanding what is salvageable and real from the recent
judge experiments.

## Run Inventory

- `ab04-judge-v2-smoke`
  - early smoke only
- `ab05-judge-v2-rep1-live`
  - partial / abandoned
- `ab05-judge-v2-rep2-live`
  - partial / abandoned
- `ab06-judge-only-rep1`
  - completed but contaminated by provider flip mid-run
- `ab06-judge-only-rep2`
  - completed but contaminated by provider flip mid-run
- `ab06-judge-only-rep3`
  - completed but contaminated by provider flip mid-run
- `ab07-opus-judge-rep1`
  - live Azure Opus judge-only rerun
- `ab07-opus-judge-rep2`
  - live Azure Opus judge-only rerun
- `ab07-opus-judge-rep3`
  - live Azure Opus judge-only rerun

## ab06 Salvage

Use `ab06` as a judge-behavior pilot only, not as a benchmark.

What survived:

- `ab06-rep1`: `14` valid / `43` invalid
- `ab06-rep2`: `15` valid / `42` invalid
- `ab06-rep3`: `15` valid / `42` invalid

The common valid overlap across all 3 reps is `14` cells:

- `pure`: `R01`, `R02`, `R03`, `R04`, `R05`
- `syke`: `R01`, `R02`, `R03`, `R04`
- `zero`: `R01`, `R02`, `R03`, `R04`, `R05`

Stable across all 3:

- `pure/R01 = fail`
- `pure/R02 = fail`
- `pure/R04 = fail`
- `pure/R05 = partial`
- `syke/R03 = partial`
- `syke/R04 = fail`
- `zero/R02 = fail`
- `zero/R03 = partial`
- `zero/R04 = fail`
- `zero/R05 = partial`

Unstable across all 3:

- `pure/R03 = pass / fail / pass`
- `syke/R01 = partial / partial / fail`
- `syke/R02 = partial / fail / fail`
- `zero/R01 = fail / partial / fail`

What the judge is already distinguishing in the clean prefix:

- stale thread vs latest thread
- wrong day / wrong cutoff
- unsupported state assertions
- useful but not restart-capable
- stale residue not reconciled with fresher git truth

So `ab06` is worth keeping as:

- pilot notes on judge behavior
- early stability hints
- examples of failure-shape separation

And not worth using for:

- headline success rate
- full 19-probe baseline comparison
- any comparison with `ab07`

## ab07 Live Opus

`ab07-opus-judge-rep{1,2,3}` is the first clean Azure Opus judge-only batch.

Current read:

- the runs are healthy and progressing
- they are slower than the old Codex path but structurally cleaner
- the new judge outputs are real and detailed

What is populating well:

- `factual_grounding`
  - `support`
  - `boundedness`
  - `uncertainty_calibration`
- `continuity`
  - `active_thread_selection`
  - `salience_relevance`
  - `state_transition_tracking`
  - `forgetting_residue_control`
  - `continuation_value`

Examples:

- `ab07-opus-judge-rep1 / pure / R01`
  - `pass`
  - strong grounding
  - strong continuity
  - clear evidence-backed reasoning

- `ab07-opus-judge-rep1 / pure / R03`
  - `partial`
  - useful but not exact on the latest thread

- `ab07-opus-judge-rep3 / zero / R03`
  - `pass`
  - `continuity = strong`
  - `factual_grounding = partial`
  - explicitly captures memex/git tension

Main schema wrinkle:

- `coherence` is semantically promising
- but is inconsistently emitted
- when present, it is often serialized as a JSON string rather than a parsed object

So `ab07` is the first run family that is actually worth treating as the clean baseline candidate.

## Claude Trace Notes

The most relevant Claude-side trace was not “latest modified file” in the naive sense, but the active repo-scoped session where Claude:

- opened the verifier paper’s actual code
- inspected a live `ab07` `judge_result.json`
- confirmed that the 3-axis / 12-subcategory structure was being populated
- correctly identified the `ab06` invalid tail as a provider/model-routing problem rather than a judge-schema problem

This is a useful note for Psyche itself:

- recency-on-disk is not the same as topic-relevant latest state
- cross-harness memory should choose relevance over naive mtime when reconstructing the “latest” thing
