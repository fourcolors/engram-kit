# Foundations + MEMEX + Neuroscience Alignment (Exploration)

Date: 2026-04-21

This pass adds a foundations-aligned and computational-neuroscience-style analysis lane to the judge-calibrated baseline. It is explicitly exploration-only and does not produce architecture ranking claims.

## Hard Constraints

- zero is a valid bounded-packet condition (not no-tool/no-retrieval)
- pass/partial/fail are noisy ordinal observations
- no architecture ranking in this phase

## Foundations -> Judge-Design Mapping

| Principles | Judge-design implication | Measurable signals |
|---|---|---|
| P2 Ledger, Not Disk, P5 Evidence != Inference | Score claim lineage against immutable artifacts and contradiction checks before verdict aggregation. | claim_support_rate, artifact_citation_rate, unsupported_claim_rate, contradicted_claim_rate, provenance_gap_rate |
| P6 Temporal First-Class | Normalize time and freshness target before retrieval/scoring. | stale_state_error_rate, freshness_target_accuracy, time_normalization_delta |
| P3 Session as Atomic Unit | Preserve packet/session boundaries and audit cross-session contamination. | packet_session_mismatch_rate, cross_session_contamination_rate |
| P4 Agent Crawls Text, P8 Fast + Deep | Separate search-surface access from reconstruction quality; do not collapse into one scalar. | search_vs_reconstruction_split, retrieval_degenerate_rate, evidence_found_vs_used_gap |
| P1 Memory IS Identity, P7 Static + Dynamic, P11 The Map Appears | Track map growth/drift dynamics across batches, not only one-shot verdicts. | coverage_growth, pointer_emergence_rate, batch_drift, routing_compression_delta |
| P9 Person + Agents Portable, P10 Accept Change | Treat judge/model-family and version effects as measured conditions; freeze rubric versions per run. | judge_family_shift, self_family_preference_gap, version_drift_delta |

## Computational-Neuroscience Construct Map

### consolidation
- Observable: memex version growth and route emergence over batches
- Candidate metrics: memory_yield_per_batch, pointer_density, chars_retained_per_event
- Minimal experiment: Run synthesis with and without memex pre-read on the same batch and compare route emergence.
- Caveat: Prompt framing can mimic consolidation effects.
- Anchors: ALMA 2602.07755, ACE 2510.04618, GEPA 2507.19457

### interference
- Observable: duplicate/contradictory memory behavior and rubric factor collapse
- Candidate metrics: contradiction_rate, duplicate_overlap, delta_r2_under_ablation
- Minimal experiment: Inject overlapping/conflicting event slices and measure merge vs split behavior.
- Caveat: Could reflect pruning policy instead of interference.
- Anchors: When Judgment Becomes Noise 2509.20293, RRD 2602.05125, CyclicJudge 2603.01865

### retrieval_cue_dependence
- Observable: pointer-led routing and memex-first retrieval behavior
- Candidate metrics: cue_follow_rate, retrieval_hop_count, latency_delta_with_cue_masking
- Minimal experiment: Mask pointer cues on matched asks and compare path + answer stability.
- Caveat: Cue availability can correlate with easier items.
- Anchors: RULERS 2601.08654, Criterion-Referenceability 2603.14732, No Free Labels 2503.05061

### recency_gradient
- Observable: older items compress while newer items retain detail
- Candidate metrics: age_slope_detail_retention, pointer_density_by_age_bucket
- Minimal experiment: Compare retention/pointer depth across age buckets.
- Caveat: Salience effects can confound recency effects.
- Anchors: LongMemEval 2410.10813, MemoryArena 2602.16313, LifeBench 2603.03781

### reconsolidation
- Observable: post-ask rewrites and pointer rewiring after new evidence
- Candidate metrics: post_query_revision_rate, pointer_rewiring_rate, before_after_edit_distance
- Minimal experiment: Ask -> add evidence -> ask again; compare memory rewrites and routing changes.
- Caveat: Generic summarization drift can appear as reconsolidation.
- Anchors: ACE 2510.04618, ALMA 2602.07755

### forgetting_residue_control
- Observable: decayed/archive behavior and stale reference residue
- Candidate metrics: stale_reference_rate, archived_item_residual_recall, pointer_half_life
- Minimal experiment: Stop reinforcement on a tracked set and probe residue over time.
- Caveat: Decay policy choices can dominate the signal.
- Anchors: LongMemEval 2410.10813, MemoryArena 2602.16313

### state_reinstatement_continuity
- Observable: state_transition_tracking behavior across session boundaries
- Candidate metrics: cross_session_state_consistency, axis_level_r2
- Minimal experiment: Probe before and after a state shift; score continuity of operative state.
- Caveat: Can collapse into style/length cues if not grounded.
- Anchors: When Judgment Becomes Noise 2509.20293, Criterion-Referenceability 2603.14732

### precision_gating
- Observable: judge shift/flicker plus stability gain under useful-collapse
- Candidate metrics: abstention_precision, low_confidence_disagreement_rate, calibration_error_when_available
- Minimal experiment: Apply abstain/escalate threshold and measure accepted-set reliability.
- Caveat: Probability calibration is blocked without human labels.
- Anchors: Trust or Escalate 2407.18370, Rating Roulette 2510.27106, KalshiBench 2512.16030

## Staged Math Sequence

Now:
- keep zero as a valid bounded-packet condition
- compute descriptive metrics for consolidation/interference/cue-dependence/recency/reconsolidation/forgetting/continuity
- keep judge diagnostics separated: gamma and epsilon observed, beta not clean
- partition probes by referenceability and retrieval-degeneracy
- keep architecture ranking out of scope

Later:
- collect human-reviewed calibration labels
- collect clean repeated answer generations for uncontaminated beta
- fit mixed-effects or G-theory alpha/beta/gamma/epsilon decomposition
- only after that, consider comparative architecture claims

## Tracker Delta

- Added task IDs: JCB-051 through JCB-063.
- Completed now: JCB-061, JCB-062, JCB-063.
- Remaining extension lane: JCB-051 through JCB-060.
