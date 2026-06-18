# Sample-Size Worksheet — 2026-04-21 (my first pass, pre-debate)

Written in parallel with the 2-agent debate. Quantitative bookkeeping. When the
debate returns, compare its prescription against this to sanity-check.

## The question, stated precisely

*What sample size is required for each claim we want to make, such that our
confidence interval is tight enough to matter, given measured noise?*

## Baseline: measured noise on the current packet

- σ_ε^cell = 0.184 (per-cell ordinal SD on 0–2 scale; judge-family invariant)
- σ_ε^pooled = 0.329–0.505 (pooled raw SD depending on arm)
- σ_γ shift (clean arm) = +0.5694 mean (Opus − gpt-5.4 on same answers, avg 4 reps)
- σ_γ asymmetry = 22/54 structural, 0/54 reverse
- σ_α = uncomputed (need probe-family structure to partition)
- σ_β = uncomputed (need ≥2 clean agent reps per cell)

## Standard-error formulas we'll use

- **Mean shift precision:** SE(Δ) = σ / √n
- **SD estimation precision:** SE(σ) ≈ σ / √(2(n−1))
- **R² precision (for n, p=12 predictors):** SE(R²) ≈ √((1−R²)²(1+2p/n)/n) — rough
- **Cohen's κ precision (Fleiss):** SE(κ) ≈ √((1−κ)²/n) when raters are 2 and cells binary
- **Power for detecting effect δ vs σ noise:** n ≈ (2.8·σ/δ)² for α=0.05, β=0.80

## Per-claim analysis

### Claim 1 — "σ_γ opus-over-gpt shift is non-zero and structural"

- Effect size observed: 0.57 (about 3× σ_ε)
- Precision at n=54 common cells: SE = 0.184 / √54 ≈ 0.025. CI = +0.57 ± 0.05.
- **Verdict: n=54 is SUFFICIENT** to claim the shift is >0 with overwhelming confidence.
- To shrink CI to ±0.02 (fine-grained comparison against future arms): n ≈ 85.
- The 22/54 asymmetry claim: binomial test with 22 successes, 0 reverses — p < 0.0001 at n=54.
  SUFFICIENT.

### Claim 2 — "σ_ε is ≈0.184, judge-family invariant"

- SD estimation at n=45 cells × 4 reps: SE ≈ 0.184 / √88 ≈ 0.020.
- CI on σ_ε: 0.184 ± 0.04.
- **Verdict: n=45 × 4 reps is SUFFICIENT.** We measured 0.184 (Opus) and 0.186 (GPT), CIs clearly overlap — "judge-family invariant" at this precision.

### Claim 3 — "Rubric is over-specified (schematic adherence R²=0.75 vs drop-axis R²=0.74)"

- Observed: 12-axis R² = 0.862 (Opus), drop-state R² = 0.840. Δ = 0.022.
- Per Feuer 2025 §4: detecting ΔR² of 0.02 requires n ≥ 200 with moderate certainty.
  At our n=111 (Opus common-cells), we're at ~55% power. Borderline.
- **Verdict: n=111 is MARGINAL.** The claim "one axis absorbs 70% R²" is robust (R²=0.73 on one axis, obvious). The claim "dropping it costs only 0.02" needs more data to be publication-robust.

### Claim 4 — "σ_β is not measurable"

- Degrees of freedom for σ_β: requires ≥2 agent reps per cell.
- We have 1 agent rep per (model, config) cell.
- **Verdict: n=0 for σ_β estimation.** Not a "we need more data" problem — it's a structural omission. Minimum fix: 2 reps × 19 probes × 3 conditions × 2 agents = 228 fresh agent runs.
- CI on σ_β at that n: SE ≈ σ_β / √(19·3·1) = σ_β / √57. For σ_β ≈ 0.2 (plausible a priori), CI ≈ ±0.026. Sufficient to detect σ_β > σ_ε.

### Claim 5 — "Probe-family coverage — each family needs its own noise characterization"

- We want to claim: "on continuity probes, opus and gpt agree at κ = X"
- Minimum for κ with reasonable CI: SE(κ) ≈ √((1-κ)²/n). For κ=0.5 target precision ±0.1: n ≥ 25.
- So **each family needs ≥25 verdicts = ~8 probes × 3 conditions**.
- Four families × 8 probes = 32 probes minimum. **We have 19.** INSUFFICIENT for per-family claims.
- To make the headline "our benchmark has 4 axes": we need to build 32+ probes partitioned by family, not 19 interchangeable probes.

### Claim 6 — "This generalizes across time (not just this specific 15-day window)"

- Currently: 1 window.
- To test generalization: run same probe-family structure on ≥2 non-overlapping 15-day windows.
- Minimum to claim stability across time: 2 windows. To characterize time-to-time variance: 3+ windows.
- **Verdict: n=1 window is UNDER-DETERMINED for generalization claims.** Two windows is a cheap way to get a huge credibility gain.
- Note: this is separate from probe count. Two windows × 32 probes × 3 conditions = 192 cells per agent.

### Claim 7 — "Architecture A > B" (the leaderboard claim)

- Combined noise assuming σ_α ≈ 0.2, σ_β ≈ 0.2, σ_γ ≈ 0.57, σ_ε ≈ 0.18:
  total noise ≈ √(0.2² + 0.2² + 0.57² + 0.18²) ≈ 0.66
- To detect architecture effect of 0.3 (moderate, 1σ of ε) with power 0.8:
  n ≈ (2.8·0.66/0.3)² ≈ 38 cells per arm.
- **Verdict: n=57 per arm is SUFFICIENT for the architecture claim**, IF σ_β is estimated (currently isn't) AND the rubric is valid (currently contested).

## The honest prescription (my draft — compare against debate)

| Claim | Min n | Our n | Status |
|---|---|---|---|
| σ_γ mean shift, CI ±0.05 | 54 | 54 | ✓ |
| σ_γ asymmetry (structural vs stochastic) | 30 | 54 | ✓ |
| σ_ε intra-rater, judge-family-invariant | 45×4 reps | 45×4 | ✓ |
| Rubric schematic adherence | 100 | 111 | ✓ marginal |
| Rubric ablation ΔR²=0.02 detection | 200 | 111 | ✗ underpowered |
| σ_β measurable | 114×2 reps | 114×1 | ✗ structural gap |
| Per-family claims (each of 4 families) | 25 verdicts/family | 0 partitioned | ✗ |
| Time generalization | 2 windows | 1 | ✗ |
| Architecture A > B, effect=0.3 | 38 per arm | 57 | ✓ if σ_β resolved |

## What this implies for the research plan

**Minimum additions to move from "recall rubric-diagnostic" to "n=1 memory benchmark":**

1. **+13 probes** to get to 32 total (8 per family × 4 families). Pull from the existing 310-ask corpus (ask-sampling memo already identified 33 candidates).
2. **+2 agent reps per cell** (one clean σ_β sweep). 228 fresh agent runs.
3. **+1 additional 15-day window.** Same probe structure replayed on Mar 1-15 or similar. Same 228 cells × 2 judges.

**Approximate compute budget:**
- New probes: no new runs, just re-run existing answer set with expanded probe list = 32 × 3 × 2 agents × 1 rep = 192 agent runs + 192 × 2 judges = 384 judge runs
- σ_β sweep: 228 new agent runs + 456 judge reruns
- Second time window: 228 new agent runs + 456 judge reruns

**Total: ~648 new agent runs + ~1296 judge runs** to get the benchmark to
"publishable n=1 memory claim" threshold. About 3-4 weeks of wall-clock if runs
are sequential, under a week if parallelized across cloud.

## What we do NOT need

- 12 time windows. Two is enough to claim time-stability; more is diminishing returns for a case study design.
- 100+ probes per family. Eight is the minimum; fifteen is better for psychometric stability; thirty is overkill for n=1.
- Multiple users. This is a *case study*. One user, rigorously measured, is the whole point.
- New model families beyond 2-3. σ_γ at 2 is estimable; 3 is for cross-validation; 5+ is for psychometric work beyond our claim scope.

## Bottom line

Not "we need 1000 probes." Not "19 is enough." The answer is **~32 probes (family-partitioned) × 2 time windows × 2 clean agent reps**, which is roughly 4× our current total verdict count. This is achievable in 1-2 weeks of focused run time, and after that we are *legitimately* doing an n=1 memory benchmark rather than a recall diagnostic.

This will be compared against the debate's prescription when it lands.
