# Task-Axis Taxonomy: Recall vs Beyond-Recall

Date: 2026-04-21

This matrix keeps classic memory benchmarks on a recall axis while extending Syke evaluation into continuity/routing/provenance failure classes from real asks.

## Recall Axis

- Definition: fixed-evidence retrieval/update tasks where evidence surface is explicit and checkable
- External neighbors: LongMemEval, BEAM-like recall suites, LoCoMo, PersonaMem
- Subtypes: single-hop fact recall, multi-session recall, temporal ordering, preference recall, abstention on unsupported asks

## Beyond-Recall Axes

| Axis | Example probes | Observed failure modes |
|---|---|---|
| live_state_restart | R01, R03, R08, R19 | stale latest-thread selection, storage-state vs work-state confusion |
| bounded_history_enumeration | R02, R04, R17, R20 | omissions, count drift |
| object_continuity_change_history | R10, R11, R13, R21 | flattened evolution narrative, wrong transition linking |
| committed_truth_config_check | R29, R30, R31, R32 | stale defaults, config/docs divergence |
| cross_surface_provenance_audit | R07, R14, R17, R42 | invented handles, cross-harness provenance braid failures |
| gap_analysis_doc_synthesis | R38, R39, R40 | generic summary replacing unresolved-gap analysis |
| meta_handoff_judge_design_compliance | R44, R45, R46 | drift into ranking claims, method non-compliance |

Rule: Each axis stands on its own with dedicated failure attribution and judge-calibration math before any aggregate claim.
