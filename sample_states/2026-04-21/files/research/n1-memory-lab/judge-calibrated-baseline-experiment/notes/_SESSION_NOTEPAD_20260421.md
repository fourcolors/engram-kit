# Session Notepad — 2026-04-21

Small scratch file maintained across this session so context doesn't drift.

## Goal (do not lose this)

- n=1 personal-memory benchmark on real user traces. Push the limits of memory systems — real-life continuity, not state-space reconstruction.
- **LLM-only evaluation. No deterministic gates. No dates / artifact-presence / commit hashes as pre-filters.** Use LLMs, push statistics + psychometrics + rubric design.
- Judge is an **agent** (multi-step), not single-shot.
- **Same primitives across all probes.** (Per-probe one-liner *hints* may come later — stored, not acted on now.)
- Three conceptual axes: accuracy, continuity, efficiency. Accuracy partially formalized (3-axis × 12-sub rubric). Continuity and efficiency still unformalized.
- Business: sell benchmark to labs → fund psyche → keep psyche free for people.

## Hard constraints the user has set

- NO deterministic verifiers. No date/artifact/commit gates.
- NO per-probe primitive sets. Same rubric everywhere.
- NO rubric-v2 drafting yet (math understanding first).
- **NO restricting the judge's tool access.** Judge stays fully agentic — full bash/grep/sqlite/packet access. "A3 is never a thing." Our job is to give it what it needs, not to cripple it.
- Running new evals IS OK when it's a minimal, well-motivated change (like A1 blind-condition rejudge).
- Capacity is available for both GPT-5.4 and Opus reruns.
- CONDENSE output. The user cannot absorb long docs — deliver inline or very short files.

## Decisions locked 2026-04-21 PM

- A1 (blind-condition) — execute. Minimal code change, no design.
- A2 (judge-brief audit) — bg agent spawned; may add UI views later.
- A3 (tool-restricted judge) — **permanently rejected**.
- A4 (rubric-v2 pilot) — queued, after A1 lands.
- Category B (fresh agent reps) — queued.
- Autorubric-vs-our-own-math — bg agent spawned.

## What we know (committed)

- Commit `4272f24` has the research corpus + field map + one-pager + evidence-packet lens + Autorubric review + ask-sampling + Autorubric-math distillation.
- 33 papers verified. Project's canonical paper IDs re-verified.
- Rubric collapse measured: one sub-axis eats ~70% R². Four noise sources decomposed (σ_α and σ_β not computed; σ_γ = +0.49; σ_ε has two estimators 0.187 and 0.329).
- Packet design is the noise generator (evidence-packet lens memo).

## What the user has asked for, right now (2026-04-21 T ~17:00)

**User has RETIRED the 9-primitive set.** Thinks many are made up. Wants to start from scratch — from primitives that emerge from the data and the design, not from the lit map.

Three tasks:
1. **Clean up the 9 primitives in docs** — mark as retired, don't let future-Claude resurrect them.
2. **Spawn a background agent to audit ALL recent Codex work** (not just one session) — user doesn't know what's landed.
3. **Me: simplify the meta-question** — *how do we measure whether a rubric is right*, and how do we design rubrics that actually represent the construct. Inline. No new long doc.

## Earlier session threads (resolved)

- Zhang 2026 vs Autorubric atomic/holistic split → done inline.
- R² + rubric collapse tied to "one holistic latent routed through 12 atomic windows" → acknowledged.

## Active files to remember

- `research/n1-memory-lab/JUDGE_DESIGN_LITERATURE_MAP_20260420.md` — project's own primitive set (§4).
- `research/n1-memory-lab/judge-calibrated-baseline-experiment/papers/nondeterministic_verifier_202604/FIELD_MAP_202604.md` — literature map.
- `research/n1-memory-lab/judge-calibrated-baseline-experiment/notes/MATH_ONE_PAGER_20260421.md` — math one-pager.
- `research/n1-memory-lab/judge-calibrated-baseline-experiment/notes/EVIDENCE_PACKET_LENS_20260421.md` — packet-design lens.
- `research/n1-memory-lab/judge-calibrated-baseline-experiment/notes/AUTORUBRIC_REVIEW_20260421.md` — agent's Autorubric review.
- `research/n1-memory-lab/judge-calibrated-baseline-experiment/notes/AUTORUBRIC_MATH_FOR_LLM_ONLY_20260421.md` — distilled math.
- `research/n1-memory-lab/judge-calibrated-baseline-experiment/papers/nondeterministic_verifier_202604/2026_zhang_rethinking-atomic-decomposition.pdf` — Zhang, about to read.
