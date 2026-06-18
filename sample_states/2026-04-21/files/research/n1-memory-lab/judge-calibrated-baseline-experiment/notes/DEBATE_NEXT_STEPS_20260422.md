# Debate: what is the right next step? — 2026-04-22

Three-round adversarial debate, preserved for lineage. User requested: figure out the simplest next move for better calibration, given σ_ε correction + existing triage + fried user + "keep it simple" posture.

## Starting positions (my initial three)

- **α (lineage-loop):** Draft rubric-v2 now targeting factor collapse; run §08 Part-C loop on the 30-cell calibration subset.
- **β (reality-mine first):** Don't write rubric v0 yet; read the 30-cell subset traces, extract primitives from observed failure modes, *then* loop.
- **γ (math-first-but-small):** Neither — first compute "at σ_ε = 0.30 with various n, what can we detect?" Decide n before any rubric work.

## Round 1 — adversary surfaced position δ

**δ (trace-triage-only):** Read R08/R19/R09 disagreement cells (floor probes, 72 cells total), classify σ_γ disagreements into 3 types. No rubric, no math. 2–3 hour deliverable.

Key round-1 critiques I accepted:
- α: generative task with no anchor — worst for fried brain.
- γ: decision-theater without a target construct.
- β-as-written: too open-ended, generative trap.
- δ is the cleanest form of β: constrained input (3 specific probes), constrained output (typed list).

Also from round 1: the paper remap can be 4 rows, 90 minutes, done.

## Round 2 — I pushed back with found material

Half of δ's work is already done. The `20260421_calibration_subset_triage.md` file exists with:
- a 30-cell subset (R03 ceiling through R19 floor) already selected
- a **4-category typology** of disagreement causes (answer quality / freshness ambiguity / packet insufficiency / rubric ambiguity)
- a **13-cell high-priority review queue**

I proposed **ε:** claim-audit the 13-cell queue, type-map the 4 categories to rubric-v2 moves. Adversary shot it down:
- ε is another deferral artifact built on a typology one agent wrote.
- "Answer quality" bucket is suspect — e.g., R08/zero and R09/production are labeled "answer quality" but under zero-packet, a wrong answer is *definitionally* a rubric question ("does zero-packet license abstention or punish fabrication?"). The typology collapses "answer was wrong" into one bucket without asking "wrong in a way the rubric told it to be wrong, or wrong in a way the rubric is silent about."
- Per-cell rubric fragments risk smuggling in per-probe hints, violating a locked constraint.
- ε ignores σ_ε = 0.30.
- §08 Part-C loop IS missing a step ("read disagreements by eye before scoring"); ε is the step *after* that, and it's the optional one.

Adversary proposed **ζ:** pick ONE cell (R08/zero); user reads answer + packet and writes one paragraph: is the disagreement "answer quality" or "rubric ambiguity under zero packet"? 90 minutes. If typology survives, ε earns its place later. If not, rewrite the typology first.

Round 2 accepted: ζ is right as the user action.

## Round 3 — synthesis

I proposed **η:** ζ as the *only* user action + three separable Claude-side draft sheets that cover the three things user explicitly asked for but ζ alone doesn't answer:

- (A) §13 loop patch — insert the missing "read disagreements by eye before scoring" step.
- (B) Paper remap — 4-row sheet, Feuer / Autorubric / Cronbach / CyclicJudge.
- (C) σ_ε = 0.30 sample-size sentences — plain English, no math for user.

All three marked "Draft — user has not confirmed. Do not cite as settled." User ignores all three if they want; nothing becomes load-bearing without sign-off.

Round 3 verdict: **η accepted with two mods.**

1. (C) gets the σ_ε-provisional caveat in the header, not footer.
2. Each sheet opens with a binding line for future-Claude: "Draft — user has not confirmed. Do not cite as settled."

Ordering: **ζ first, (A) second, (C) third, (B) last.** (B) can wait longest without rotting.

Adversary's closing test for "genuinely separable, not prerequisites in disguise": would A/B/C change if ζ comes back "rubric ambiguity" vs "answer quality"? Answer: no for any of them. That's the tell they're context, not gates.

## The single sentence for the user

> Next: read R08/zero (answer + packet), write one paragraph on whether the disagreement is answer-quality or rubric-ambiguity-under-zero-packet; three Claude-side draft sheets (loop patch, paper remap, sample-size table) are in the repo as context, not as decisions.

## Positions considered but not taken (for completeness)

- **α / β / γ** — my starting three, all superseded.
- **δ** — trace-triage-only. Superseded by the existence of the 04-21 triage.
- **ε** — claim-audit the 13-cell queue. Premature until ζ validates the typology.

## What could change this

If the user writes the ζ paragraph and says "actually this is answer quality, the typology holds" — ε is back on the table next session.

If the user writes "this is rubric ambiguity" — the 4-category typology needs a rewrite, and the "answer quality" bucket specifically gets re-examined. The 13-cell priority queue gets a re-labeling pass before any claim-audit.

If the user writes "both, or something else" — we talk. That itself is signal about whether our typology language is right.

---

*Preserved for thread lineage. The simplification posture (primitive-first, mine-reality-first, small-but-audit-worthy-subset, math-you-can-read) was the north star throughout the debate.*
