# Autorubric Math — What's Actually Useful for LLM-Only Memory Judging

> **2026-04-21 note:** the 9-primitive set that some passages in this doc reference
> (e.g. `wrong_restart_risk`, `operative_state_adequacy`, `cross_surface_integration`) has been
> retired by the author. Treat primitive names below as historical illustrations of
> atomic-vs-holistic split reasoning, not as a live design target.

One page. No essay. Read sections §1–§3 of the paper.

## The one equation that matters

```
  score = max(0, min(1, Σ v_i·w_i / Σ_{w_i>0} w_i))
```

- `v_i` = per-criterion verdict (1 = MET, 0 = UNMET, or value for nominal).
- `w_i` = criterion weight. **Can be negative** — negative weights are penalties for anti-patterns (fabrication, stale-state, wrong-thread). Negatives excluded from the denominator so a clean response scores 1.
- Clamped to [0,1].

This is their whole aggregation. Transparent, auditable, one line.

## The five failure-mode → mitigation map (their real contribution)

| failure mode | Autorubric's move | why it matters for us |
|---|---|---|
| **position bias** | option shuffling, value-based scoring | removes a known LLM-judge bias |
| **low reliability** | ensemble judging, N × M grid of independent LLM calls (N judges × M criteria) | each criterion gets its own LLM call → prevents halo / axis-collapse by design |
| **criterion conflation** | atomic decomposition | one LLM call per criterion. *this is where Zhang 2026 pushes back — some primitives should stay holistic* |
| **uncertainty** | explicit `CANNOT_ASSESS` verdict with configurable strategies (SKIP / ZERO / PARTIAL / FAIL) | first-class abstention. huge for partially-verifiable reconstruction |
| **opacity** | mandatory `reason` field per verdict | audit trail, not executive summary |

## How the math handles noise (what pushes the limits)

- **Per-criterion κ and weighted κ**, not a single overall κ. You see *which* criterion is noisy.
- **Verdict-balanced few-shot calibration.** Few-shot examples pre-balanced across MET / UNMET / CANNOT_ASSESS so the judge doesn't imitate the corpus prior. Empirically: 0-shot 77% → 3-shot 79% → 5-shot 80% on RiceChem.
- **Narrow ordinal scales with behavioral anchors** (3–5 levels, never continuous). LLMs have documented central-tendency bias on broad scales; narrow + anchored fights it.
- **Continuous scores intentionally excluded.** They say: LLMs don't calibrate well on unbounded numeric. Use binary or narrow ordinal or nominal.
- **Negative weights encode anti-patterns.** Fabrication, stale-state, overclaiming — these become penalty criteria with negative w, not rubric gaps.

## What transfers to our task

Four moves, all LLM-only:

1. **Eq 1 aggregation.** Replace the current 3-axis ordinal roll-up with a weighted sum with explicit penalty criteria. Fabrication = negative weight.
2. **N × M grid with separate LLM calls per criterion.** This structurally solves the rubric-collapse finding (one axis eating 70% R²) — independent calls can't collapse into one latent.
3. **`CANNOT_ASSESS` abstention, first-class.** For claims the packet doesn't support and that are too speculative to judge — explicit abstention beats forced verdict.
4. **Per-criterion κ tracked as a reliability signal.** If one criterion's κ stays poor under ensemble + calibration, the criterion itself is the problem, not the model.

## What does NOT transfer (why we don't just adopt it)

- Autorubric's benchmarks (RiceChem chemistry, ResearcherBench, CHARM-100) test **reference-anchored entailment** — the judge has gold-standard references. We don't have gold for memory continuity.
- **Atomic-only is the wrong default for our primitives.** Zhang 2026 shows holistic matches or beats atomic when coherence is the construct. Our `wrong_restart_risk`, `operative_state_adequacy`, `cross_surface_integration` are coherence-shaped. Make 1–2 of our primitives deliberately holistic — evaluated over the whole packet in one pass, not atomized.
- Autorubric assumes flat `(prompt, submission)` input. No packet provenance, no structured filesystem, no session boundaries. Everything about *what the judge sees* is upstream of Autorubric and stays our engineering.
- No multi-step judge agent built in. Single-pass per criterion. If we want a judge *agent* (plan → read packet → score → revisit), we build that around Autorubric, not from it.

## One-line bottom

**Take Eq 1 + the N×M independent-call structure + abstention + per-criterion κ. Leave atomic-everywhere behind. Keep the judge an agent, and keep the rubric primitives the same across all probes — which is consistent with what you want.**

## Source

- Rao & Callison-Burch 2026 (arxiv 2603.00077), `2026_rao_autorubric.pdf` in same directory. §§1–3 for the math; §4 for benchmarks; Appendix B for code patterns.
