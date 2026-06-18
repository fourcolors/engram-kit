# Ask-Demand Taxonomy — NE-1.3 real-ask corpus

Date: 2026-04-18
Related analyses (same data, different pass):
- `JUDGE_CALIBRATION_AB07_20260418.html` — top-down: stable-fail forensics, cross-judge calibration, sub-axis convergence proposal.
- This doc — bottom-up: every ask tagged by the operational demand it places on the memory system, then mapped to the existing judge schema to find coverage gaps.

## What this is

Every one of the 50 real asks in `NE_1_3_REAL_ASK_EVAL_SET.yaml` was read and tagged by the verb it actually asks the memory system to do — not by a pre-existing schema. The tag list was built inductively from the asks; the judge schema was only brought in afterwards to check mapping.

Raw per-ask tag data: [`ask_demands_ne13_20260418.tsv`](./ask_demands_ne13_20260418.tsv).

## Tag vocabulary (built bottom-up)

| tag | what the user is demanding |
|---|---|
| STATE_NOW | "where are we now / what's active / what's the latest" (present-tense restore) |
| LAST_THREAD | "what was I last on" (recency) |
| TIME_WINDOW | "what happened on day X to day Y" (enumerate in time) |
| THREAD_MAP | structured open-threads list |
| CONCEPT_RECALL | "what did we learn / build / design about X" (named area) |
| CHANGE_HISTORY | timeline of patches / evolution of a thing |
| NEXT_STEPS | "what's left / what were next steps" |
| GAP_ANALYSIS | find blind spots / contradictions |
| CONFIG_CHECK | actual vs recommended config; is X up-to-date |
| DOC_SYNTH | read named files, produce structured analysis |
| META_HANDOFF | directive / constraint-ack / handoff — **not reconstruction** |
| QUANT | exhaustive list / numerical totals ("be exhaustive", "how many") |
| CROSS_SOURCE | explicitly spans multiple harnesses |
| DELTA | "what changed" |
| DECISION | recall specific decisions / directives made |
| COMMITTED_STATE | claim must match code / git / config at t |

## Distribution across all 50 asks

| primary tag | n | all-tag load |
|---|---|---|
| CONCEPT_RECALL | 10 | 18 |
| LAST_THREAD | 8 | 10 |
| TIME_WINDOW | 7 | 7 |
| META_HANDOFF | 6 | 8 |
| STATE_NOW | 5 | 6 |
| CONFIG_CHECK | 5 | 5 |
| CHANGE_HISTORY | 3 | 3 |
| THREAD_MAP | 2 | 3 |
| DOC_SYNTH | 2 | 2 |
| NEXT_STEPS | 1 | 4 |
| GAP_ANALYSIS | 1 | 2 |

Other tags (always secondary): COMMITTED_STATE (13), QUANT (6), DECISION (5), DELTA (5), CROSS_SOURCE (4).

## Distribution restricted to R01-R19 (the ab07-scored set)

| tag | count in R01-R19 | which probes |
|---|---|---|
| META_HANDOFF | **0** | — |
| CONFIG_CHECK | **0** | — |
| GAP_ANALYSIS / DOC_SYNTH | **0** | — |
| QUANT | 4 | R02, R04, R05, R17 |
| CROSS_SOURCE | 3 | R07, R14, R17 |
| CONCEPT_RECALL | 8 | R03, R05, R10, R11, R12, R13, R15, R18 |
| TIME_WINDOW | 5 | R02, R04, R07, R16, R17 |
| LAST_THREAD | 4 | R03, R06, R14, R19 |
| COMMITTED_STATE | 4 | R02, R04, R15, R18 |
| NEXT_STEPS | 4 | R03, R06, R12, R15 |
| STATE_NOW | 3 | R01, R08, R09 |
| THREAD_MAP | 3 | R01, R05, R09 |
| DECISION | 3 | R06, R11, R16 |
| DELTA | 3 | R07, R09, R17 |
| CHANGE_HISTORY | 1 | R13 |

**Implication for the existing ab07 run**: all 19 probes are real reconstruction tasks. No META_HANDOFF drift, no GAP_ANALYSIS drift, no CONFIG_CHECK drift in the set we've already scored. Those categories first appear at R20+.

## Coverage audit — which judge sub-axes fire meaningfully, which are vacuous

Mapping each demand tag to the 12 current Opus judge sub-axes:

| demand | judge sub-axis that should fire | status |
|---|---|---|
| CONCEPT_RECALL (8 probes in R01-R19) | factual_grounding.support + coherence.cross_session_consistency | covered but split |
| COMMITTED_STATE (4 probes) | factual_grounding.support + coherence.artifact_routing_consistency | covered but leaky |
| LAST_THREAD (4 probes) | continuity.active_thread_selection + continuity.salience_relevance | covered redundantly |
| TIME_WINDOW (5 probes) | continuity.state_transition_tracking | partial — checks transitions, not enumeration |
| STATE_NOW (3 probes) | active_thread_selection + salience_relevance | covered |
| NEXT_STEPS (4 probes) | continuity.continuation_value | covered |
| THREAD_MAP (3 probes) | active_thread_selection | covered |
| DELTA (3 probes) | state_transition_tracking | covered |
| DECISION (3 probes) | continuation_value (drift) + support (drift) | leaky, no home |
| CHANGE_HISTORY (1 probe) | state_transition_tracking | covered |
| **QUANT (4 probes)** | **NONE** | **blind spot** — no enumeration-completeness check |
| **CROSS_SOURCE (3 probes)** | coherence.cross_harness_braid | covered, but scored on all 19 (16 cells are vacuity-scored) |

## The two blind spots that affect R01-R19 directly

### 1. QUANT has no judge coverage (4 probes: R02, R04, R05, R17)

The user explicitly asks "be exhaustive", "list everything", "how many cycles", "72 million tokens from what" on 4 of the 19 probes. The current judge schema checks "is each claim supported" (factual_grounding.support) but never checks "did you list everything in the slice you should have listed."

**Concrete missing axis**: `enumeration_completeness` — on a TIME_WINDOW or THREAD_MAP probe, sample the slice for items that match the probe's scope and check recall against that reference set. Falsifiable against the slice.

Across 3 Opus reps × 3 conditions × 4 QUANT probes = **36 of the 171 judged cells (21%) had this dimension unmeasured.**

### 2. CROSS_SOURCE scored on every cell (relevant to 3 of 19)

`coherence.cross_harness_braid` is scored on all 171 cells, but only 3 probes (R07, R14, R17) actually demand cross-harness reasoning. For the other 16 probes × 3 cond × 3 reps = **144 cells (84%), the cross_harness_braid score is vacuity**. It defaults to "strong" for "correctly focusing on the available harness", which is not coherence work.

This is the mechanism behind the 63-84% coherence-axis flip rate noted in JUDGE_CALIBRATION_AB07: the sub-axis is scored on cells that don't demand it, so judges assign it stochastically.

## What this means for the existing ab07 data

1. All 171 scored cells are on real reconstruction probes. The META_HANDOFF problem (which breaks 8/50 asks in the broader corpus) doesn't hit ab07.
2. 36/171 cells (the QUANT probes × conditions × reps) were judged without an enumeration-completeness check. Re-judging these with `enumeration_completeness` added would likely move some "pass" verdicts to "partial" on exhaustive-list probes.
3. 144/171 cells had `cross_harness_braid` scored on a demand that wasn't there. Retiring cross_harness_braid as a conditional-only sub-axis (fire only when CROSS_SOURCE tag is present) would cut 84% of the current coherence-axis noise.
4. `salience_relevance` and `artifact_routing_consistency` are redundant with `active_thread_selection` and `cross_session_consistency` on their respective probe buckets. Merging them is schema cleanup without loss.

## Proposed ask-driven judge schema (revised from the earlier convergence proposal)

Probe gets a primary type tag at load time. Sub-axes fire conditional on the tag, not on every cell.

| probe-type bucket | n/50 | n/19 | sub-axes |
|---|---|---|---|
| STATE/THREAD (STATE_NOW + LAST_THREAD + THREAD_MAP) | 24 | 10 | thread_selection, residue_control, support, boundedness |
| TIME_WINDOW + QUANT | 10 | 5 | **enumeration_completeness (NEW)**, support, boundedness, temporal_bounds |
| CONCEPT_RECALL + CHANGE_HISTORY + DECISION | ~16 | 9 | support, internal_consistency, contradiction_handling |
| CONFIG_CHECK | 5 | 0 | **committed_state_fidelity (NEW)**, support |
| META_HANDOFF | 8 | 0 | directive_acknowledgment, constraint_adherence, plan_quality (NEW family — reconstruction axes off) |
| GAP_ANALYSIS + DOC_SYNTH | 4 | 0 | structural_coverage, critique_specificity, source_grounding (NEW family — reconstruction axes off) |
| CROSS_SOURCE | 4 | 3 | adds cross_harness_braid to the bucket's scoring |

**Net schema deltas**:
- Add 3 sub-axes: `enumeration_completeness`, `committed_state_fidelity`, + the 3-sub-axis META_HANDOFF family
- Merge 2 pairs: `salience_relevance` into `thread_selection`; `artifact_routing_consistency` into `internal_consistency`
- Make `cross_harness_braid` conditional (fire only when probe carries CROSS_SOURCE tag)
- Add a separate critique family for GAP_ANALYSIS / DOC_SYNTH

## Two-pass validation before shipping

1. Tag every probe in the eval manifest with the primary demand type (`ask_demands_ne13_20260418.tsv` is ready to drive this).
2. Re-judge the existing ab07 traces with the ask-driven schema (prose reasoning in the current traces is rich enough to reconstruct most sub-axis scores retroactively).
3. Compare flip rate before/after. If coherence-axis flip drops from 63-84% to something lower without losing discriminator power on the pure-fail consensus set, the schema is better.
4. Only then run a fresh pass with the new schema wired into the Pi-native judge tool.

## Files

- [`NE_1_3_REAL_ASK_EVAL_SET.yaml`](./NE_1_3_REAL_ASK_EVAL_SET.yaml) — canonical ask set
- [`ask_demands_ne13_20260418.tsv`](./ask_demands_ne13_20260418.tsv) — per-ask demand tags (primary + all)
- [`JUDGE_CALIBRATION_AB07_20260418.html`](./JUDGE_CALIBRATION_AB07_20260418.html) — companion top-down analysis (calibration + stable-fail + convergence proposal)
