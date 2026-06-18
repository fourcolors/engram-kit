# Judge Mining Synthesis — 2026-04-20

Cross-reads 6 parallel mining batches over 285 judge verdicts across a 2×2 ask×judge factorial on the NE-1.3 canonical 19-probe slice. Goal: concrete inputs for the next judge contract design, for open-ended, non-fully-verifiable reconstruction tasks.

Batch notes: `research/n1-memory-lab/judge-mining-20260420/BATCH_{A,B,C,D,E,F}.md`.

---

## Ground fact from the raw data

Same answers, different judge: opus upgrades 27 cells, downgrades 1. Mean rank shifts +0.49 on a 0-2 scale, replicated across both ask sets. **The judge identity is the dominant systematic confound in single-judge benchmarks.** Every downstream finding in this document is about what to do given that fact.

The ~55 cells where gpt-judge and opus-judge agree on the same answer are the only verdicts safely decoupled from judge identity. They are the only calibration-anchor class we have.

---

## Finding 1 — The current schema has structural problems, not just noise

From Batch C (sub-axis firing across 225 cells):

- **`factual_grounding.boundedness` is vacuous in GPT's partial band** (std = 0.289 inside partial cells). It contributes zero discriminative power once the top-level verdict is partial. Retire or fold into `factual_grounding.support`.
- **Opus has a 3-way continuity collapse cluster:** active_thread_selection ↔ continuation_value ↔ salience_relevance all at r ≥ 0.85 (max 0.911, just under the 0.93 factor-collapse threshold from 2509.20293). These three axes are effectively one axis under Opus. Merge to 1-2.
- **Coherence axes are the weakest cross-judge:** `cross_session_consistency` (40% agreement), `contradiction_handling` (39%), `state_transition_tracking` (35%). These axes either need redefinition or admission that they're subjective.
- **GPT defaults to partial (71-90% of subcategories);** Opus defaults to strong (35-76%). The two schemas aren't calibrated to each other — same rubric language, very different scoring distributions.

**Takeaway:** the existing 3-axis / 12-sub-axis rubric is not salvageable as-is. It has at least one vacuous axis, one collapsed cluster, and poorly-defined coherence.

---

## Finding 2 — The two judges use different criteria, not just different thresholds

From Batches A and D:

**GPT operates a "boundary violation" model.** Pet vocabulary: "overreaches," "invents artifacts," "unsupported," "without caveats." GPT requires slice-bounded evidence citation for every claim. Refuses extrapolation. Caps scoring at partial when any sub-claim lacks direct slice support.

**Opus operates a "logical contradiction" model.** Pet vocabulary: "directly contradicted," "does not integrate," "speculative." Opus allows narrative synthesis and inference as long as nothing in the answer is provably false. Penalizes only when a claim is directly contradicted by the evidence, or when cross-surface integration is absent.

**GPT penalizes breadth overflow. Opus penalizes depth insufficiency.** These aren't offsets on the same axis — they're orthogonal philosophies. This explains why the shift isn't uniform across probe types.

**Asymmetric findings:**
- GPT alone penalizes overconfident tone ("without caveats"). Opus never mentions confidence calibration. If we want this criterion, the rubric must force both judges to score it explicitly.
- Opus alone names temporal state reconciliation as an issue. GPT describes the same error without a vocabulary for it.
- GPT alone catches hallucinated specific artifacts (invented UUIDs, fake commands). Opus misses these unless they directly contradict a known fact.

---

## Finding 3 — The anchor cells tell us what canonical pass/fail/partial actually are

From Batch B (55 agreed cells):

**Canonical pass** (9 agreed cells):
- Temporal grounding with **verifiable artifacts** — specific commit SHAs, issue IDs, session counts cross-checkable against git/JSONL anchors
- **Topical exhaustiveness within scope** — no claims of "clean slate" or false negatives
- **Multi-surface consistency** — reconciliation across at least 2 surfaces (git + sessions, or sessions + issues)
- **Specificity of decision context** — named active threads that match the slice's actual decision surface

**Canonical fail** (11 agreed cells):
- **Systematic factual contradiction** — claims directly falsified by observable slice evidence (empty workspace when 147 JSONL files exist)
- **Contextual misidentification** — confuses meta-system state (syke.db internal scaffold) with user work state
- **Overconfident false negatives** — asserts absence without evidence of searching
- **Non-restart-capable state models** — user cannot safely resume from the reconstructed state

**Canonical partial** (35 agreed cells):
- **Strong topical/structural recovery + localized failure modes** — captures major threads but makes systematic errors in one dimension (dates misattributed, bug status stale, timezones muddled)
- **Utility-appropriate uncertainty** — useful for direction-setting, unreliable for micro-level actions
- **Recoverable via human verification** — the error is checkable (did we really do that on that date?) rather than requiring oracle knowledge

**Takeaway:** pass = artifact-verified specifics + multi-surface consistency. Fail = provably-contradicted claims + context confusion. Partial = right themes + local errors. These are the rubric anchors.

---

## Finding 4 — Judge stability is ask-type-dependent

From Batch E (7-pressure stratification on R01-R19):

| pressure | judge disagreement rate | N probes |
|---|---|---|
| **object_continuity** (evolution of X) | **37.5%** (most stable) | 8 |
| operative_state (current state) | 40% | 10 |
| bounded_history | 50% | 6 |
| completeness | 50% | 4 |
| committed_truth | 50% | 4 |
| **cross_surface** | **66.7%** (worst) | 3 |
| provenance_audit | — | 0 (undersampled) |

**The universal-rubric assumption doesn't hold.** Rubric granularity should be ask-type-conditional because some ask-types are inherently judge-stable (object_continuity has a clear narrative structure, judges agree on "is there a coherent timeline?") and others are not (cross_surface has no shared definition — is it a list, an integration, or a causal linkage?).

Multi-pressure probes (3+ tags) consistently show higher disagreement than single-pressure ones. The rubric needs an explicit precedence rule when pressures collide.

---

## Finding 5 — The task is partially criterion-referenceable

From Batch F:

- **Answer length has ρ = 0.40-0.62 with verdict** across all 4 judge configurations — not orthogonal to features.
- **~25-35% of verdict variance** is explainable by measurable answer features (length, tool calls, cost) in the production/pure conditions. Rises to ~40-50% in the zero condition.
- **~55-75% remains pure semantic judgment** — irreducibly LLM-judged.
- Cross-judge agreement on feature importance: high for length (both judges agree longer ≈ better), **divergent for tool calls** (GPT ρ = 0.2, Opus ρ = 0.5 — judges disagree on whether tool-use intensity should matter).

**Caveat:** Batch F's Table 1 showed `answer_length = 0` in all records, which contradicts the non-zero correlations reported in Tables 2-3. Likely the correlation computation used a different length variable than what was surfaced in the means table. The direction of the correlation (longer → higher verdict) is plausible and consistent with prior trace reads showing overreach-length sometimes rewarded, but the exact fraction of referenceable variance should be re-verified before acting on it.

**Takeaway:** hybrid scoring is licensed — part deterministic/rule-based, part semantic. Not pure rules (papers like 2502.09316 "judge-free" don't fully generalize to our task). Not pure LLM judgment either.

---

## What this says for the next judge contract

Eight concrete design decisions the data supports:

### 1. Retire vacuous axes and collapse clusters
- Drop `factual_grounding.boundedness` (vacuous in partial band); fold boundedness concept into `factual_grounding.support`.
- Merge Opus's 3-way continuity cluster (active_thread / salience / continuation_value) into one primitive — they measure the same thing under Opus's rubric.

### 2. Coherence needs redefinition or demotion
- `cross_harness_braid` and `cross_session_consistency` have 39-54% cross-judge agreement. Either define them operationally ("cross-surface means the answer names artifacts from ≥2 named surfaces AND ties them with causal/temporal linkage") or move coherence from universal to conditional (fires only when ask is tagged cross_surface).

### 3. Add `wrong-restart risk` as a universal axis
- Both judges penalize context-switching failures (meta-state vs user-state) and non-restart-capable state models. No current axis captures this directly. Per Batch B fail anchors, the signature is universal: context-confusion is always a fail.

### 4. Claim-typing rule to resolve the GPT/Opus divergence
- The "overreach" vs "contradiction" split is the core judge disagreement. Force answers (not judges) to type each claim as **verified** (cites artifact), **inferred** (derived from evidence chain), or **speculative** (explicitly marked). Verified claims must pass support check; inferred claims pass with stated evidence chain; speculative claims pass only if flagged.

### 5. Make enumeration completeness explicit and conditional
- Split "completeness" into two axes:
  - `enumeration`: countable "list everything" — fires only when ask demands it, scored against reference set size from slice_meta.
  - `narrative depth`: unbounded "explain how X connects to Y" — semantic only.
- Current schema conflates these, causing 50% judge disagreement on completeness cells.

### 6. Grounding-by-artifact as hard pass gate
- Every agreed pass cell cites specific artifacts. No agreed pass relies only on broad themes. Make this a rubric rule: **no claim may name a specific entity (file, commit, issue, session ID) without a verifiable reference to it in the slice**. Hallucinated specifics (invented UUIDs, fake pytest commands, nonexistent commits) are automatic partial-or-fail, regardless of narrative coherence.

### 7. Promote `object_continuity` to universal; keep `cross_surface` conditional with definition
- Object_continuity is the most judge-stable ask-type (37.5% disagreement). Elevate to a universal axis: "does the answer preserve the identity and evolution of a named object across sessions/time?"
- Cross_surface cannot be universal — 66.7% disagreement. Keep conditional with an operational definition: "fires when the ask tags >1 harness/surface AND the answer must explicitly link them via causal or temporal reasoning."

### 8. Confidence calibration is a separate axis, judge-elicited explicitly
- GPT spontaneously penalizes "overconfident tone without caveats." Opus never does. If the rubric wants this criterion, it must force both judges to score it explicitly. Otherwise it's judge-specific bias masquerading as a schema axis.

---

## What this does NOT support

- **Architecture ordering claims.** The judge-bias effect (+0.49 mean shift) dominates any architecture difference observed in single-judge data. Pure, zero, and production cannot be reliably ranked until cyclic-judge rotation is in place.
- **Generation-variance claims.** We still have N=2 reps on one config. Nothing there is trustworthy.
- **Sub-axis retirement beyond the two concrete cases** (boundedness; Opus's continuity cluster). Other axes have moderate problems but the sample size (57 cells per judge-ask combo, 114 per judge, 225 total) can only support a few actionable cuts before we're overfitting.

---

## Three immediate next moves

1. **Rewrite the judge tool contract** per the 8 decisions above. Structural schema change, not calibration tweak.
2. **Tag the 24-probe canonical slice with the universal+conditional axis activation rules** so the new judge fires the right criteria per probe.
3. **Register sonnet (or another 3rd judge identity) in `~/.syke/pi-agent/models.json`** before any new benchmark run. K=2 judges is not enough for CyclicJudge's bias cancellation — we need K=3 minimum to hit the FPC cancellation term meaningfully, K=5 ideally.

None of these require new benchmark runs. The new contract can be retroactively applied to existing 285 cells, and the cyclic-judge setup only runs after the new schema is live. **No more data collection until the judge is redesigned.**

---

## Sources

- [BATCH_A_DISAGREEMENT_FORENSICS](./judge-mining-20260420/BATCH_A_DISAGREEMENT_FORENSICS.md)
- [BATCH_B_AGREEMENT_ANCHORS](./judge-mining-20260420/BATCH_B_AGREEMENT_ANCHORS.md)
- [BATCH_C_SUBAXIS_FIRING](./judge-mining-20260420/BATCH_C_SUBAXIS_FIRING.md)
- [BATCH_D_LINGUISTIC_TRIGGERS](./judge-mining-20260420/BATCH_D_LINGUISTIC_TRIGGERS.md)
- [BATCH_E_ASK_TYPE_STRATIFICATION](./judge-mining-20260420/BATCH_E_ASK_TYPE_STRATIFICATION.md)
- [BATCH_F_ANSWER_FEATURES](./judge-mining-20260420/BATCH_F_ANSWER_FEATURES.md)
- [FORMALISM_AXES_AND_CYCLIC_JUDGE_20260420](./FORMALISM_AXES_AND_CYCLIC_JUDGE_20260420.md)
- [JUDGE_GRANULARITY_AND_BASELINES_PAPERS_20260420](./JUDGE_GRANULARITY_AND_BASELINES_PAPERS_20260420.md)

---

## Appendix — Schematic Adherence R² (Feuer et al. 2509.20293)

Added after batch synthesis. Batch C's factor-collapse call used pairwise Pearson correlations as a proxy. The paper's actual diagnostic is regression-based: fit `overall_verdict ≈ β₀ + Σ βⱼ · (sub-axis j score) + ε` per judge, report R². Low R² = schema incoherence (overall verdict not derivable from sub-axis scores). This appendix runs that regression on our data and records what it honestly supports.

### Computation

- Encoding: sub-axis scores {strong, partial, missed} → {2, 1, 0}; overall verdict {pass, partial, fail} → {2, 1, 0}.
- Model: ordinary least squares, linear only (polynomial with 90 features requires more cells than we have; skipped).
- Bootstrap: 1000 iterations for 95% CI.
- Data: all 4 (ask × judge) configurations, 54-57 cells per config.

### Results — per (ask × judge) configuration

| ask | judge | n | R² | adjusted R² | 95% CI |
|---|---|---|---|---|---|
| gpt | gpt | 57 | 0.72 | 0.64 | [0.63, 0.88] |
| opus | opus | 57 | 0.92 | 0.90 | [0.90, 0.98] |
| gpt | opus | 54 | 0.82 | 0.77 | [0.80, 0.96] |
| opus | gpt | 57 | 0.87 | 0.83 | [0.82, 0.97] |

### Results — pooled per judge

| judge | n | R² | adjusted R² | 95% CI | unexplained |
|---|---|---|---|---|---|
| gpt-judge | 114 | 0.754 | 0.725 | [0.682, 0.867] | 24.6% |
| opus-judge | 111 | 0.862 | 0.845 | [0.830, 0.931] | 13.8% |

Paper's flagged-incoherent benchmark (Arena-Hard Auto, DeepSeek-R1-32B no-reasoning) had R² = 0.095-0.126 (unexplained 87-90%). **Our R² is 0.75-0.86. Schema incoherence in the paper's sense is not our problem.**

### Regression coefficients (standardized β)

Which axes actually drive the overall verdict?

**opus-judge (n=111):**

| sub-axis | β_std | β_raw |
|---|---|---|
| continuity.state_transition_tracking | **+0.322** | +0.306 |
| factual_grounding.support | **+0.273** | +0.302 |
| continuity.active_thread_selection | +0.123 | +0.118 |
| coherence.cross_harness_braid | +0.097 | +0.095 |
| coherence.contradiction_handling | +0.091 | +0.093 |
| coherence.artifact_routing_consistency | +0.083 | +0.088 |
| continuity.continuation_value | +0.058 | +0.060 |
| factual_grounding.uncertainty_calibration | +0.028 | +0.030 |
| **factual_grounding.boundedness** | **−0.023** | **−0.027** |
| coherence.cross_session_consistency | +0.014 | +0.014 |
| **continuity.forgetting_residue_control** | **+0.009** | **+0.010** |
| **continuity.salience_relevance** | **−0.008** | **−0.008** |

**gpt-judge (n=114):**

| sub-axis | β_std | β_raw |
|---|---|---|
| continuity.state_transition_tracking | **+0.227** | +0.190 |
| coherence.cross_session_consistency | +0.159 | +0.148 |
| continuity.forgetting_residue_control | +0.144 | +0.125 |
| coherence.cross_harness_braid | +0.126 | +0.105 |
| factual_grounding.boundedness | +0.126 | +0.133 |
| continuity.salience_relevance | +0.104 | +0.076 |
| coherence.artifact_routing_consistency | +0.097 | +0.078 |
| continuity.active_thread_selection | +0.074 | +0.049 |
| continuity.continuation_value | −0.062 | −0.052 |
| factual_grounding.support | +0.061 | +0.060 |
| factual_grounding.uncertainty_calibration | −0.059 | −0.052 |
| coherence.contradiction_handling | +0.036 | +0.030 |

### Sanity check — single-axis baselines

Using only `continuity.state_transition_tracking` alone, no other axes:

| judge | best single-axis R² |
|---|---|
| gpt-judge | 0.61 (state_transition_tracking) |
| opus-judge | 0.73 (state_transition_tracking) |

Adding the other 11 axes lifts R² by only 14 points (gpt) / 13 points (opus). **The 12-axis rubric is doing the work of a 1-2 axis rubric.**

### What this changes in the headline findings

| earlier claim (Batch C / synthesis) | corrected claim (from regression) |
|---|---|
| "GPT schema is underspecified; explains little verdict variance" | **Wrong.** GPT's R² = 0.75 — substantial. Batch C confused sub-axis partial-band std with verdict-variance explanation. |
| "factual_grounding.boundedness is vacuous" | **Partially right.** Vacuous for opus (β_std = −0.023). Not vacuous for gpt (β_std = +0.126). Axis-judge-dependent, not axis-intrinsic. |
| "opus continuity 3-way factor collapse" | **Confirmed in a stronger form.** Salience_relevance (β ≈ 0), forgetting_residue_control (β ≈ 0), continuation_value (β = 0.06) all contribute near-nothing to opus's verdict. Not just correlated with other continuity axes — non-load-bearing. |
| "schema has structural problems" | **Shifted.** Problem is not incoherence; problem is over-specification / factor collapse. Judges compute verdicts from 1-3 load-bearing axes; the other 9-11 are decorative. |

### Axes confirmed vacuous by near-zero regression coefficient

**For opus-judge** (β_std < 0.05 magnitude — no influence on verdict):
- `factual_grounding.boundedness`
- `continuity.forgetting_residue_control`
- `continuity.salience_relevance`
- `coherence.cross_session_consistency`

**For gpt-judge** (β_std < 0.05):
- `coherence.contradiction_handling`
- `factual_grounding.uncertainty_calibration`

### Axes confirmed load-bearing

- **Universal (both judges, β_std > 0.2):** `continuity.state_transition_tracking`
- **Opus-specific:** `factual_grounding.support`
- **GPT-specific:** `coherence.cross_session_consistency`, `factual_grounding.boundedness` (moderate)

### What this supports in the 8 contract decisions

- **Decision 1 (retire boundedness):** Supported for opus. Equivocal for gpt.
- **Decision 1 (merge Opus's 3-way continuity cluster):** Fully supported — two of those three axes contribute ≈0 to opus's verdict.
- **Decision 2 (redefine or demote coherence):** Partially supported. Coherence matters for gpt (cross_session_consistency is the 2nd-highest β) but barely for opus.
- **Decision 3 (add wrong-restart risk as universal):** Consistent with the finding that `state_transition_tracking` carries most of the verdict weight — this axis is semantically adjacent to wrong-restart risk.
- **Decisions 4-8:** untouched by this regression.

### What I can NOT claim

- **Exact R² magnitudes.** CI widths are wide (0.63-0.88 at n=57 per config). Paper used n=500.
- **Polynomial R² with interactions.** Needs more data or regularization; skipped.
- **Cronbach's α / factor analysis / HTMT.** Needs either more cells per axis or continuous (not 3-point) scoring.
- **Inter-judge reliability (ICC).** Needs ≥3 judges. Sonnet blocked on registry; K=2 is all we have.
- **That single-axis dominance is pathological.** The judge prompt TELLS the judge to compute an overall verdict from sub-axis reasoning — some collapse is expected by design. What's diagnostic is which specific axes end up doing all the work and which end up as filler.

### One-paragraph honest reading

The judges are internally self-consistent: their overall verdicts ARE explained by their own sub-axis scores (R² = 0.75-0.86). The paper's "schema incoherence" diagnostic does not apply. What IS real is a milder but actionable problem: the 12-axis rubric behaves like a 1-3 axis rubric in practice. `state_transition_tracking` alone drives 60-73% of the verdict. Four axes for opus and two for gpt have near-zero regression coefficients — they get scored, but they don't matter. The next judge contract should cut to 3-5 load-bearing axes, frozen by regression evidence across more data, rather than try to calibrate 12 axes most of which are decorative.

### Appendix computation code

Preserved for reproducibility in `research/n1-memory-lab/scratch/schematic_adherence_20260420.py` (the `python3 << EOF` block that generated these tables). Re-run with any new judge data to refresh the numbers.

---

## Correction — model-mix-up in the gpt-side runs (2026-04-20 evening)

Codex audit caught that today's gpt-side experiments used **gpt-5.4-mini** as the judge in several runs where the original baseline used **gpt-5.4** (full model). This contaminates several claims in this document.

### Affected configurations

| run | ask | judge | issue |
|---|---|---|---|
| `gpt54-final` (baseline) | gpt-5.4 | gpt-5.4 | canonical |
| `gpt54-rep2` | **gpt-5.4-mini** | **gpt-5.4-mini** | not a "same-config fresh rep"; entirely different model |
| opus-ask × gpt-judge cross (in the 2×2 design) | opus-4.6 | **gpt-5.4-mini** | not opus-vs-gpt-5.4; it's opus-vs-gpt-5.4-mini |
| my "intra-rater" run | reused (gpt-5.4) | **gpt-5.4-mini** | not intra-rater; cross-model within gpt family |

### What claims are contaminated

- **The "+0.49 judge effect"** from the 2×2 mixed two shifts: opus-4.6 vs gpt-5.4-mini (two different-size models across two families), not opus-4.6 vs gpt-5.4. The direction stands (opus judges more leniently than gpt-family judges) but the exact magnitude is confounded with within-gpt-family model-size.
- **"Intra-rater κ = 0.051"** was not intra-rater. It was cross-model within gpt family (gpt-5.4 vs gpt-5.4-mini). The low κ does not support a claim of judge stochasticity per se. **Retracted.**
- **"Generation variance (gpt-rep2 vs rep1)"** — both reps used different models. The rep2 data is a rep2-of-a-different-config, not a fresh generation of the same config.

### What actually stands from today's data

- **Opus intra-rater** (Codex audited the config: judge_model = claude-opus-4-6 matches the baseline, so this IS intra-rater):
  - n = 41 valid cells so far (still running)
  - Exact match: 32/41 = **78%**
  - Cohen's κ = **0.650** (substantial agreement)
  - Mean delta: −0.024
  - Std delta: 0.468
  - Binary useful-vs-fail agreement: 97.6%
- **Opus judge looks reasonably self-consistent.** CyclicJudge's "fixed per-judge bias" assumption is not disproven.
- **The pass/partial/fail 3-class boundary is unstable; the coarse catastrophe-vs-non-catastrophe cut is much more stable.** On opus, 3-class κ = 0.65 but binary κ ≈ 0.95. This is a calibration finding about the aggregate layer, not a reason to replace primitive-axis scoring with binary scoring.
- **Schema adherence R² per config** — each config is internally computed, so the 0.72/0.82/0.87/0.92 R² numbers per (ask × judge) config are robust to the model mix-up. They just reflect different judges than I labelled.
- **Factor collapse / load-bearing axes** — still stand. Computed per-judge on real data.

### The corrected working model

1. Judge identity matters a lot — confirmed (direction stable, magnitude confounded).
2. Rubric is over-specified / factor-collapsed — confirmed.
3. Pass-vs-partial is the unstable class boundary; the coarse aggregate cut is more stable.
4. Opus judge is ~78% self-consistent (κ=0.65). gpt-5.4 self-consistency is **not yet measured** — a proper intra-rater (gpt-5.4 → gpt-5.4 rerun) was submitted after the audit and is queued.
5. The next judge redesign should simplify rubric, lock the primitive layer first, and treat any binary collapse only as a stability audit over the aggregate verdict rather than as the benchmark itself.

### Re-run queued

`judge_only-gpt54ask-gpt54judge-TRUE-intrarater-20260420t202***z` — gpt-5.4 (matching baseline) rerunning on gpt-5.4-ask answers. Will give the actual intra-rater number for gpt-5.4.

### Lesson

Check judge_model in config.json against baseline before labeling a judge-only run as "intra-rater" or "cross-judge." The labctl submit command doesn't validate that the judge_model matches what you intended to replicate.
