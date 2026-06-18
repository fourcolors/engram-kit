# Sample-size sentences — 2026-04-22

**Draft — user has not confirmed. Do not cite as settled. σ_ε = 0.30 is itself provisional — it was estimated from 2-run pair disagreements on 110 cells, not from the full CyclicJudge cycled-panel protocol. The direction of the correction (upward from 0.18) is robust; the exact value should not be quoted as final.**

Plain-English version of the sample-size picture, using the corrected σ_ε ≈ 0.30. No math for the reader — one sentence per n-row. Tables are at the bottom for the curious; skip them.

---

## The headline, in four sentences

1. **Our 30-cell calibration subset is plenty** for detecting a rubric-v2 change that meaningfully reduces σ_γ — anything at the ±0.21 scale or larger shows cleanly above noise.
2. **Our 109-cell pooled data (canon + blind) sees σ_γ = +0.51** five times above its noise floor. That's why it reads as "locked."
3. **Fine-grained calibration — detecting shifts at the ±0.10 scale** — needs n ≈ 125 cells. We don't have that, and pursuing it now would be fake precision.
4. **The σ_ε correction from 0.18 → 0.30 does not break anything.** Earlier sample-size prescriptions using σ_ε = 0.18 were optimistic by a factor of ~1.7. At σ_ε = 0.30, the concrete effect is: same-judge-rerun noise has a floor of ±0.11 at n=30. Anything smaller is flicker.

---

## For cross-judge differences (the σ_γ family of claims)

Paired cells — same question, two judges. What's the smallest shift we can tell apart from noise?

Using the observed SD of paired differences (≈ 0.58, measured from the 109-cell pooled data):

| cell count | smallest reliably-detectable shift | plain reading |
|---|---|---|
| n = 13 | ±0.315 | One-cell pilots — only gross shifts show |
| n = 30 | **±0.208** | **Our calibration subset.** Clean for substantive rubric-v2 moves |
| n = 50 | ±0.161 | Still within reach with a modest rerun |
| n = 109 | ±0.109 | **What we actually have pooled.** The +0.51 σ_γ is ~5× this floor |
| n = 200 | ±0.080 | Would require ~2× our current data |

**Concrete framing for rubric-v2 planning:**

- If rubric-v2 *halves* σ_γ (from +0.51 to +0.25 — a shift of 0.26): **n ≥ ~19 cells detects it.** Our 30-cell subset more than suffices.
- If rubric-v2 gets σ_γ down to +0.35 (a shift of 0.16): **n ≥ ~50 cells.** Need a modest rerun.
- If rubric-v2 gets σ_γ down to +0.10 (a shift of 0.41): **n ≥ ~8 cells.** Trivially detectable.

**Reverse reading:** a new rubric whose σ_γ only differs from the old one by ±0.10 or less is **indistinguishable from the current rubric at our available n.** Don't claim fine-grained improvements.

---

## For same-judge rerun (the σ_ε family of claims)

Same judge, same cell, re-run. What mean shift can we distinguish from ordinary judge-flicker?

Using σ_ε ≈ 0.30 (the corrected value):

| cell count | detectable shift |
|---|---|
| n = 30 | ±0.107 |
| n = 50 | ±0.083 |
| n = 100 | ±0.059 |

**Concrete framing:** The full-session opus-ans × gpt-judge blind-canon shift of −0.304 at n=56 is ~4.5 σ above this floor — genuinely not noise. The σ_γ canon→blind shift of +0.027 at n=109 is ~0.2 σ — comfortably noise.

---

## What this sheet does *not* do

- It does not commit us to any specific n target. That's a user decision driven by the rubric-v2 roadmap, which isn't defined yet.
- It does not say the σ_ε = 0.30 value is final. It's a two-run estimate; real CyclicJudge-style multi-rep estimation would give a tighter number. For now, treat 0.30 as "the honest working value."
- It does not re-derive `SAMPLE_SIZE_DEBATE_20260421.md`. That memo's decision-tree shape is still correct; its numeric prescriptions are the part that needs the 1.7× uplift.

---

## Future-Claude binding

Before quoting any number in this sheet, re-read the header. σ_ε = 0.30 is provisional. The *direction* of the correction (upward) is robust; the *exact value* is pending replication. Use these sentences to set expectations; do not use them to anchor claims.

---

## The method, for the curious

Noise floor formula used throughout: **1.96 × SD / √n** (two-sided, p < 0.05). For a reader who wants the number at n you care about: take SD of the relevant quantity, divide by √n, multiply by 2. That's your "can't-tell-from-noise" floor.

- For paired cross-judge shifts: SD ≈ 0.58 (observed in pooled data).
- For single-judge rerun means: SD = σ_ε ≈ 0.30.

80%-power versions would use the factor 2.8 instead of 1.96. That would shrink the table ns by ~40% at the same effect size — larger n required. The 1.96 version is the lower bound on "detectable." If you want to plan for 80%-power rubric-v2 experiments, multiply the ns above by ~2.
