# BATCH_C_SUBAXIS_FIRING

**Date:** 2026-04-20  
**Basis:** 4 cells (gpt-ask×gpt-judge, opus-ask×opus-judge, gpt-ask×opus-judge, opus-ask×gpt-judge)  
**Total cells:** 114 gpt-asks (57×2), 111 opus-asks (57+54)  
**Encoding:** strong=2, partial=1, missed=0

---

## Table 1: Sub-axis Score Distribution by Judge

**GPT Judge (n=114 cells)**

| Axis | Strong | Partial | Missed | Strong% | Var | Signal |
|---|---|---|---|---|---|---|
| continuity.active_thread_selection | 48 | 36 | 30 | 42% | 0.659 | **HIGH** |
| continuity.salience_relevance | 47 | 47 | 20 | 41% | 0.532 | MOD |
| coherence.cross_harness_braid | 29 | 66 | 19 | 25% | 0.413 | MOD |
| factual_grounding.boundedness | 9 | 83 | 22 | 8% | 0.259 | **LOW** |
| factual_grounding.support | 24 | 79 | 11 | 21% | 0.294 | **LOW** |
| (others) | — | — | — | 10–32% | 0.33–0.66 | MOD |

**Opus Judge (n=111 cells)**

| Axis | Strong | Partial | Missed | Strong% | Var | Signal |
|---|---|---|---|---|---|---|
| continuity.salience_relevance | 84 | 16 | 11 | 76% | 0.423 | MOD |
| coherence.cross_session_consistency | 72 | 30 | 9 | 65% | 0.408 | MOD |
| continuity.continuation_value | 74 | 28 | 9 | 67% | 0.405 | MOD |
| (all others) | 39–79 | 19–66 | 6–14 | 35–71% | 0.31–0.48 | MOD |

**Key:** GPT defaults to partial (71–90% partial); Opus skews strong (35–76% strong).

---

## Table 2: High Correlations (|r| > 0.70)

**Opus Judge: Near-Collapse Cluster**

| Axis 1 | Axis 2 | r |
|---|---|---|
| continuity.active_thread_selection | continuity.continuation_value | **0.911** |
| continuity.active_thread_selection | continuity.salience_relevance | 0.855 |
| continuity.continuation_value | continuity.salience_relevance | 0.876 |

**Factor-collapse alert:** Opus' 3-way continuity collapse (r > 0.85). Also coherence.cross_session_consistency bleeds into continuity (r ≥ 0.79 with all three continuity axes).

**GPT Judge:** 7 pairs with r ∈ [0.71, 0.84]; no r > 0.93.  
**Opus Judge:** 20 pairs with r ≥ 0.70; highest 0.911 (below 0.93 threshold but actionable).

---

## Table 3: Within-Partial-Band Variance (n_partial: GPT=80, Opus=44)

| Axis | GPT Std | Opus Std | Discriminative? |
|---|---|---|---|
| continuity.active_thread_selection | 0.673 | 0.622 | YES (both) |
| factual_grounding.boundedness | **0.289** | 0.417 | **NO (GPT only)** |
| (all others) | 0.34–0.53 | 0.44–0.59 | YES |

**Finding:** `boundedness` has zero discriminative power in GPT's partial band (std < 0.3 = loss threshold). All other 11 axes discriminate. Opus has no vacuous axes.

---

## Table 4: Cross-Judge Agreement (same answers, n=54 GPT-asks)

| Axis | Exact Match % | Off-by-1 % | Strength |
|---|---|---|---|
| continuity.active_thread_selection | 57% | 35% | MOD (best) |
| coherence.cross_harness_braid | 54% | 44% | MOD |
| continuity.salience_relevance | 54% | 41% | MOD |
| coherence.artifact_routing_consistency | 41% | 56% | WEAK |
| coherence.contradiction_handling | 39% | 54% | WEAK |
| continuity.state_transition_tracking | 35% | 59% | WEAK |

**Finding:** Max agreement 57%; coherence axes weakest (39–41%). No axis well-defined across judges.

---

## Synthesis

- **Independent signal (real axes):** `continuity.active_thread_selection` (highest variance both judges, 57% agreement, high partial-band discrimination). `continuity.salience_relevance` (76% Opus strong, 54% agreement).

- **Vacuous:** `factual_grounding.boundedness` (var=0.259 GPT, std=0.289 in partial band). **Retire or merge into `support`.**

- **Factor-collapse risk:** Opus continuity 3-way (r ≥ 0.85: active_thread ↔ continuation_value ↔ salience). **Merge to 1–2 axes in Opus schema.** No pairs exceed 0.93; closest is 0.911 (borderline).

- **Schema incoherence:** GPT defaults partial → low verdict-variance explained by axes. Opus splits strong/partial → high explanatory power. **GPT schema underspecified.**

- **Subjectivity:** Coherence axes (artifact_routing, contradiction_handling) have weak cross-judge agreement (39–41%) → either redefine or accept subjectivity.

**Action:** Retire boundedness; collapse Opus continuity 3-way; redefine or de-weight coherence axes; GTX (gpt-judge) schema needs refinement.

