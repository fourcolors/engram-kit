# Judge Granularity + Baseline Calibration — paper pull 2026-04-20

Status: reading list, paired with [`FORMALISM_AXES_AND_CYCLIC_JUDGE_20260420.md`](./FORMALISM_AXES_AND_CYCLIC_JUDGE_20260420.md).

Papers pulled specifically to extend the CyclicJudge + computational-memory-axes formalism with fine-grained rubric handling and baseline discriminative power.

---

## Lane A — Granularity in multi-axis / rubric judges

### LLM-Rubric (2501.00274, 2025)
Per-judge calibration via small feed-forward net combining judge-specific and judge-independent parameters over 9-dim 1-4 Likert rubric. 2x RMS improvement over uncalibrated averaging. Clearest published recipe for "judge A's 3 = judge B's 4" — train a calibration head per judge against human anchors.

### Likert or Not (2505.19334, 2025)
Pointwise-vs-pairwise gap **collapses when the Likert scale is large enough**. Pick scale size empirically.

### Judgment Distribution Inference (2503.03064, 2025)
Read the full next-token distribution over score tokens and take E[score] = Σ k · p(k | prompt). Improves calibration on ordinal scales; drop-in for sub-axis scoring, yields per-axis uncertainty.

### Rethinking Rubric Generation / RRD (2602.05125, 2026)
**Recursive Rubric Decomposition** with **correlation-aware weighting** — downweights correlated sub-axes before aggregation. Directly addresses our sub-axes-are-not-independent problem with a concrete weighting recipe (weights reflect residual, not raw, variance).

### Autorubric / AdaRubric (2603.00077 + 2603.21362, 2026)
Analytic (per-criterion, independent) vs holistic rubrics. Per-criterion scoring reduces halo effects and conflation. AdaRubric adds task-adaptive rubric instantiation. Lift: separate prompts per axis, no shared CoT.

### Rulers: Locked Rubrics + Evidence-Anchored Scoring (2601.08654, 2026)
Two-agent: extractor pulls evidence spans, scorer sees only locked rubric + spans. Turns scoring from stochastic generation into deterministic lookup. Direct fit for reconstruction-style evaluation.

### Rubric-Conditioned LLM Grading (2601.08843, 2026)
Expert alignment **degrades monotonically with rubric granularity** — warning against 1-7 or 1-10. Introduces **Trust Curve** (accuracy vs coverage as you defer low-confidence calls).

### Conformal Prediction Intervals for LLM-Judge (2509.18658, 2025)
Conformal-prediction wrapper around ordinal judge: **distribution-free prediction interval** with coverage guarantee, ordinal boundary adjustment for discrete ratings, midpoint estimator with lower bias than sampled score. **Most direct methodological upgrade to CyclicJudge's Gaussian approximation** — conformal is distribution-free on ordinal targets.

### Rating Roulette (2510.27106, 2025)
Quantifies intra-rater reliability across reruns of same judge on same item. Protocol: report intra-rater agreement alongside inter-judge agreement; if intra-rater is low, inter-rater is meaningless.

### Lost in Benchmarks / PSN-IRT (2505.15055, 2025)
IRT fits difficulty, discriminability, guessing-rate, feasibility per item; 11 benchmarks, 41,871 items. **Local Efficiency Headroom** and **Fisher information** per item diagnose low-quality items. Lift: fit IRT over items, drop ones with zero/negative discriminability before reporting rankings.

### Grading Scale Impact (2601.03444, 2026)
Head-to-head of 0-3, 0-5, 0-10, 0-100 scales. **0-5 maximizes human-LLM alignment.** Direct answer to "what scale."

### Correlated Errors in LLMs (2506.07962, 2025)
Models correlated error structure across LLM raters. Complement to RRD for handling non-independent judges.

---

## Lane B — Baseline calibration / discriminative power

### Construct Validity in LLM Benchmarks (2511.04703, 2025)
Systematic review of 445 benchmarks by 29 reviewers. Patterns that undermine convergent/discriminant validity. Eight actionable recommendations for benchmark builders. Canonical citation for "separate architecture-effect from base-model-effect."

### Criterion-Referenceability Determines LLM-Judge Validity (2603.14732, 2026)
LLM-judge discriminative validity tracks **criterion-referenceability** (how much task maps to observable features), not raw model capability. Numbers: structured tasks ρ > 0.6 blind / 0.88 with solutions; essays ρ ≈ 0.1 blind, ρ ≈ 0 with mark schemes even though distribution matches humans. **Central warning for Syke:** if memex-reconstruction tasks are not criterion-referenceable, judge agreement is a mirage.

### When Judgment Becomes Noise (2509.20293, 2025)
Three design failure modes with computable diagnostics:
- **Schema Incoherence** (unexplained variance > 90%)
- **Factor Collapse** (cross-axis correlation > 0.93)
- **Aggregation Masking** (ELO hides irreducible uncertainty)
Proposes **Schematic Adherence** and **Psychometric Validity** metrics — directly computable on existing judge logs.

### Robustness of Benchmark-Based LLM Evaluation (2509.04013, 2025)
34 LLMs; benchmarks lose discriminative power as base-model strength rises. Protocol for measuring remaining signal. Second citation alongside 2511.04703.

### KalshiBench / Brier Skill Score (2512.16030, 2025)
**Brier Skill Score** = 1 - BS_model / BS_baseline (baseline = always predict base rate). Only Claude Opus 4.5 beats base-rate baseline (BSS 0.057). Cleanest recent example of reporting against explicit uninformed baseline. **Directly liftable: report BSS on Likert scores vs base-rate predictor.**

### Growing Pains / Fixed Parameter IRT (2604.12843, 2026)
IRT with fixed item parameters so adding new items doesn't invalidate prior scores. Relevant if Syke Replay adds new items over time and wants architecture scores to remain comparable across versions.

### Beyond Consensus / Agreeableness Bias (2510.11822, 2025)
Judges converge toward agreement even when it's wrong. Different failure mode from self-preference.

---

## Recommended pulls for each specific Syke problem

### For sub-axis correlated-error problem
- 2602.05125 (RRD)
- 2509.20293 (When Judgment Becomes Noise — Factor Collapse metric)
- 2506.07962 (Correlated Errors)

### For ordinal/CLM upgrade to CyclicJudge Gaussian approximation
- 2509.18658 (conformal intervals, ordinal boundary adjustment)
- 2505.15055 (IRT with discriminability + Fisher info)
- 2503.03064 (judgment distribution expectation)

### For no-memory baseline methodology
- 2512.16030 (Brier Skill Score against base rate)
- 2511.04703 (construct validity)
- 2603.14732 (criterion-referenceability)

### For scale/rubric design choice
- 2601.03444 (0-5 maximizes alignment)
- 2505.19334 (pointwise-pairwise gap closes with scale)
- 2501.00274 (LLM-Rubric per-judge calibration)
- 2601.08654 (Rulers, locked-rubric evidence-anchored)

---

## What this changes about the formalism

The CyclicJudge-based formalism still stands, but these extensions layer on top:

1. **Judge head calibration** (2501.00274) before ANOVA. Fits per-judge adjustment against anchor items so `σ_γ²` is the post-calibration bias, not raw leniency drift.

2. **Ordinal replacement for Gaussian ANOVA** (2509.18658, 2505.15055). Conformal intervals give distribution-free coverage; IRT gives per-probe discriminability.

3. **Sub-axis correlation accounting** (2602.05125, 2509.20293). Report factor-collapse diagnostic; weight primitives by residual (not raw) variance.

4. **Baseline contract** (2512.16030). Define a base-rate predictor (e.g., "always answer 3"). Report BSS of each condition against it. If `syke` doesn't beat base-rate on primitives the ask genuinely demands, the memory architecture isn't separating from prior-only.

5. **Locked-rubric evidence extraction** (2601.08654). Before scoring, a judge pass extracts evidence spans from `r_t` + packet; scoring judge sees only the spans + rubric. Lower variance than current free-form judge.

6. **Scale pinned to 0-5** (2601.03444). Fits CyclicJudge's divisibility constraint (K_tot = 5).

7. **Intra-rater reliability reported alongside inter-judge** (2510.27106). If a single judge re-scored gives varying answers, the inter-judge panel can't stabilize that noise.

8. **Psychometric validity gate** (2509.20293). Before trusting any condition ranking, confirm Schema Incoherence < threshold and Factor Collapse < threshold.

---

## Open next steps

- Read `2509.18658` fully — does the conformal setup require calibration data we don't have?
- Read `2602.05125` fully — what's the exact weighting formula for residual variance?
- Read `2603.14732` fully — can we compute criterion-referenceability on our 15-day slice?
- Pull the RRD and When-Judgment-Becomes-Noise code if public; factor-collapse and schema-incoherence can be computed retroactively on ab07 judge logs.
