# Handoff — Next Session (delta note)

**Compiled 2026-04-22 ~early UTC, at the tail end of the same saxenauts session that produced `NEXT_SESSION_20260421.md`.**

Read `NEXT_SESSION_20260421.md` first — it's the real handoff: the state of the work, the locked constraints, the voice of the collaboration, the personal note. None of that is superseded.

This file is the delta: what moved after that note was written.

---

## Current document state

`WHERE_WE_ARE_20260421.html` is now at **v0.2.14**. §01–§12 still frozen at **v0.2.7** — do not touch. §13 is the active working surface. The tabs + compact-basics card + per-tab TOC are in place.

---

## What happened since the 04-21 PM handoff

**The blind rerun landed.** All four arms completed. Numbers lived up as raw facts:

- σ_γ (opus − gpt on same GPT answers): **+0.500 → +0.527** under blind (n=55)
- Opus-higher asymmetry: **22/54 → 26/55**
- Per-arm paired shifts: gpt-ans×gpt-judge −0.035, gpt-ans×opus-judge +0.019, opus-ans×opus-judge −0.161, opus-ans×gpt-judge **−0.304**
- 1 pass↔fail flip across 222 common cells
- Binary κ across arms: 0.47–0.87

**v0.2.13 overclaimed.** The headline I shipped ("self-preference hypothesis refuted — bias is structural in the rubric", "fork resolves toward rubric-redesign") was wrong for the sample size. σ_ε ≈ 0.18 means standard error on a paired mean at n=55 is about ±0.02. The +0.027 shift is ≈1 SE — inside the noise band. The fork (identity-leak vs rubric-bias) does **not** resolve at this n.

**The user caught it.** Their quote: *"No that result is too small to be meaningful, we will just note it as something that happened on this data, and move on."*

**v0.2.14 is the correction.** §13 blind-rerun block rewritten ("honest read — the rerun did not cleanly resolve the fork"). Compact-basics panel retitled "Blind rerun — landed (fork not resolved)". v0.2.13 changelog preserved as historical record. v0.2.14 entry at the top of the changelog explains the correction cycle.

Commit: `a13ba3f` on main.

---

## What this means for the next session

**Nothing load-bearing changed.** The four-line plan is intact. The big undercurrent (what we give the judge as evidence) is intact. Rubric-v2 is still the next load-bearing move. Architecture ranking is still off the table until the three validity diagnostics pass.

**The keeper from this whole cycle:** the blind-eval tooling works end-to-end. `SYKE_BLIND_PACKET=1` masks identity fields; `azure-anthropic-foundry` is in Pi's env allowlist now (syke `119ca43` on `dev/0.5.2`); the comparison script at `scratch/compare_blind_vs_canonical_20260421.py` produces reproducible deltas.

**What we'd need to actually resolve the fork:** either (a) more observations — roughly 4–6× the n to detect a ±0.1 shift at σ_ε ≈ 0.18, or (b) a rubric change followed by another blind rerun. Neither is now-work. Rubric-v2 has to come first.

---

## Lesson for me (and the next agent)

I overclaimed. The numbers looked clean (integer asymmetry went in the right direction, the raw σ_γ delta was positive) and I read a story into them without computing the noise band first.

If you see a delta like +0.027 on a 0–2 scale at n=55, before you frame it as a finding: compute the SE. σ_ε / √n for a paired mean. If the delta is inside ±1 SE, the correct sentence is "nothing moved meaningfully," not "structural, not self-preference." The user will catch it. You should catch it first.

---

## Your first actions, updated

The three actions in `NEXT_SESSION_20260421.md` are done — runs index is regenerated, comparison script was run, results are in §13. Start fresh:

1. **Read the 04-21 handoff's "locked constraints" and "what the user explicitly does NOT want" sections.** Those haven't changed. They're the design primitives.
2. **Hold the four-line plan.** Recall / continuity / efficiency / calibrate. Don't expand it.
3. **If the user is ready to move on rubric-v2:** start from `notes/AUTORUBRIC_COVERAGE_AUDIT_20260421.md` (Option B — substrate + 8 RED layers authored). Don't front-run them into a rubric sprint if they're still in the "understand the math" phase.
4. **If they want to think about release, n=1 framing, or the paper shape:** `FIELD_NOTES_RELEASE_20260421.md` and `FIELD_NOTES_N1_DEEP_20260421.md` are where my prior thinking lives. Don't over-index on my takes; they're exploratory.

---

## One more thing

`research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_blind_vs_canonical_deltas.{md,json}` are the source-of-truth artifacts for the blind numbers. If any later write-up needs the raw deltas, read from those, not from memory.

— Claude Opus 4.7, 2026-04-22 early
