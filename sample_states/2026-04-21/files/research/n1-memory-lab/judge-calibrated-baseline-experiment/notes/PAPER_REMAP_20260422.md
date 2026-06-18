# Paper → math remap — 2026-04-22

**Draft — user has not confirmed. Do not cite as settled.**

One page. Four rows. Which inherited papers plug into which quantity we compute, and where that quantity lives in our current work.

This is not a paper audit. It is a "what math we use, from which paper, for which number" sheet. If a paper doesn't land in one of the four rows below, it's not operationally on-surface today.

---

## The four rows

| Paper | The quantity *they* define | Our equivalent | Where it plugs in today |
|---|---|---|---|
| **Feuer 2025** · *When Judgment Becomes Noise* · `2509.20293` | Rubric R² — fraction of verdict variance explained by the sub-scores | **Schematic-adherence R²** — already computed | §08 diagnostic 1. **Result: 0.75–0.86** (passes). But one sub-axis (`state_transition_tracking`) explains 0.73 on its own — over-specification. |
| **Autorubric** · Rao & Callison-Burch 2026 · `2603.00077` | Per-criterion κ — inter-judge agreement computed for each rubric dimension separately (not an aggregate) | **Per-sub-axis agreement across our two judges** | §08 diagnostic 3. **Not yet measured.** Would localise which of our 12 sub-axes is the noisy one. Cheap to compute from existing data. |
| **Cronbach et al. 1972** · Generalizability Theory | Variance decomposition: rater / item / interaction / residual | **σ_γ / σ_α / σ_β / σ_ε** — the four sigmas in the frozen §04 narrative | The "three σ-questions" framing in today's simplification posture: does a different judge change the score? does the same judge wobble? does the answer itself wobble? |
| **CyclicJudge** · Zhu 2026 · `2603.01865` | σ_γ + σ_ε estimation via cycled-panel rerun protocol | **σ_ε ≈ 0.30** — estimated today from blind/canon pair differences on the two gpt-ans arms (where blinding is a no-op) | Updates the working σ_ε from 0.18 → 0.30. Feeds into the sample-size sheet. Note: we did *not* run the full CyclicJudge protocol — we used their variance-decomposition formalism on a two-run comparison we already had. |

---

## What this replaces

The frozen §11 "Math-to-papers map" is a **12-row** reference table (every math primitive we reference → which paper). That remains the canonical legend.

This sheet is different: it's the **working subset** — the 4 rows that are actually computing numbers in the current work, *not* the full reference. When someone asks "what papers are we using right now," the honest answer is these four.

---

## What is *not* in this table and why

Three papers are close to the operational surface but don't compute a number here today:

- **Zhang 2026** (`2603.28005`) — *Rethinking Atomic Decomposition*. Shapes the atomic-vs-holistic decision for individual criteria. This is rubric-*structure* math, not instrument-*validity* math. Relevant when we draft rubric-v2; not relevant to today's calibration diagnostics.
- **Yeadon 2026** (`2603.14732`) — *Criterion Referenceability*. Gate test: "can this dimension be scored from observable features at all?" Used when we retire primitives. Not computing a number today.
- **Bean 2025** (`2511.04703`) — *Measuring What Matters*. The construct-validity frame. Shapes how we name what we measure. Not computing a number today.

Ten further papers (Choi IRT-Judge, Sheng Conformal, Badshah SCOPE, Hashemi LLM-Rubric, Gunjal RaR, Liu DeepSeek-GRM, Kim Prometheus, Lightman step-by-step, Ye CALM, Jung Trust-or-Escalate) are explicitly gated behind rubric-v2 validity and do not belong on this sheet. See §13 "Paper stack — *active vs framing vs gated*" in `WHERE_WE_ARE_20260421.html` for the full gating logic.

---

## The simplification this represents

We previously had a 33-paper corpus, a 13-paper MATH-surface subset, a 12-row math-to-papers map, an active / framing / gated three-table split, and multiple session memos on paper usage.

The working subset is **four rows.** Everything else is reference material — useful when you're writing prose about the frame, not necessary to compute the next number.

If this sheet lengthens beyond six rows, that's a signal that the scope of "what we compute" has crept. Pull it back to the four.

---

## Future-Claude binding

Before citing any row in this sheet as settled math, re-read the header line at the top of this file. This is a draft until saxenauts signs off on the shape.
