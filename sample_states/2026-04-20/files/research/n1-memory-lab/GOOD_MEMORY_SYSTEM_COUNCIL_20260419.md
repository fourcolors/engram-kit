# Good Memory System Council — 2026-04-19

Status: working convergence note
Scope: environment + ask-surface interpretation only
Source mode: local corpus-first synthesis from council passes, not final paper language

---

## 1. What We Are Actually Trying To Say

The cleanest benchmark-safe center is not:

- recall
- retrieval
- long-context QA
- full self/world modeling
- restart alone

The center is:

**A good memory system in this environment uses only evidence available by time `t` to recover and expose the minimum correct, ask-relevant work state needed for safe continuation under interruption.**

That keeps the claim:

- stronger than recall
- narrower than full self/world modeling
- grounded in the real ask surface

---

## 2. Keep These Three Surfaces Separate

### Full corpus

- `NE-1.3` has `50` real asks across `2026-03-08` to `2026-04-10`
- later asks broaden into provenance, governance, method, and meta-benchmark pressure

### First 15-day slice

- the first 15 calendar days are `R01-R24`
- this is the main corpus used in the latest council pass here
- it already contains more than restart alone:
  - orientation
  - time-window reconstruction
  - evolving object history
  - committed-truth pressure

### Headline benchmark-safe claim

- keep the claim narrower than the full corpus
- safest center remains early continuity / interruption / bounded reconstruction pressure
- do not let later meta asks silently redefine the benchmark headline

---

## 3. Minimal Capability Set

These are the irreducible capabilities repeatedly supported by the ask slice and
the latest council pass.

### A. Operative-state recovery

The system must recover what is active, latest, open, unfinished, and most worth
resuming now.

Why it matters:

- this is the center of the ask surface
- without it, the system cannot support practical continuation

### B. Time-bounded activity reconstruction

The system must reconstruct what happened within a bounded window such as
yesterday, today, last session, last week, or a named date.

Why it matters:

- many asks are date-local rather than generic
- time drift causes wrong continuation

### C. Object continuity through change

The system must preserve the identity and evolution of a named thing across
patches, reversals, design changes, and thread splits.

Why it matters:

- many real asks are about one changing subsystem, idea, or patch lineage
- snapshot summaries lose the object

### D. Bounded evidence anchoring

The system must stay anchored to evidence available by time `t` and avoid
plausible but stale synthesis.

Why it matters:

- without this, all other capabilities degrade into confident narrative
- this is what keeps the benchmark from collapsing into style or vibe

---

## 4. Real But Conditional Capabilities

These matter, but they should not be universal obligations on every ask.

### A. Enumeration completeness

Fire when the ask demands:

- everything
- entire day
- be exhaustive
- how many
- full timeline

### B. Cross-surface integration

Fire when the ask genuinely spans more than one harness or evidence surface.

### C. Committed-state fidelity

Fire when the answer depends on code, config, docs, git state, runtime artifacts,
or implementation truth rather than discussion continuity alone.

### D. Provenance / derivation traceability

Fire when the user asks how the answer was derived or when the ask is
audit-sensitive.

---

## 5. Computational Language That Actually Fits

These terms fit the current environment and ask surface better than old benchmark
language:

- `state estimation under partial observability`
- `belief-state representation`
- `binding across time`
- `source attribution`
- `object continuity through change`
- `operative state`
- `wrong-restart risk`

These terms are too weak or too misleading if used as the main story:

- `recall`
- `retrieval`
- `long-context QA`
- `single-corpus summarization`
- `full self/world model`

Use of `coherence` should also be careful:

- as a universal top-level axis, it is currently overweight
- as a conditional demand on some asks, it remains real

---

## 6. What A Good Memory System Is Doing Here

The system is not mainly storing answers.

It is maintaining a compact, updateable, evidence-bounded operative model of the
user's changing work from fragmented traces, then exposing enough of that model
for the user or another agent to continue correctly after interruption.

That means it must:

- recover the live thread
- separate current state from stale residue
- reconstruct bounded time windows without drift
- preserve object history through changes
- expose proof or uncertainty when the ask demands it

---

## 7. What To Avoid Overclaiming

Do not headline the current benchmark as testing:

- full self/world modeling
- generic continuity of the whole person
- universal cross-harness coherence on every ask
- restart as the only memory function

The first overclaims.
The last underclaims.

The better compression is:

**bounded, time-local, ask-relevant operative state for safe continuation**

---

## 8. Implications For Judge Redesign

This convergence supports a judge shaped like:

### Universal

- bounded support
- time-local correctness
- operative-state adequacy
- wrong-restart risk

### Conditional

- enumeration completeness
- object continuity through change
- cross-surface integration
- committed-state fidelity
- provenance / derivation traceability

This is cleaner than forcing one static subcategory block across every probe.

---

## 9. Immediate Next Move

Before further theory expansion:

1. tighten the environment and benchmark wording around `ask-relevant operative state`
2. keep the full corpus, 15-day slice, and headline benchmark claim explicitly separate
3. redesign judge subcategories from these universal vs conditional primitives

---

## 10. Main Source Notes

- [`NE_1_3_REAL_ASK_EVAL_SET.yaml`](./NE_1_3_REAL_ASK_EVAL_SET.yaml)
- [`ASK_PRESSURE_MATRIX_NE13_15D_20260419.md`](./ASK_PRESSURE_MATRIX_NE13_15D_20260419.md)
- [`ASK_SURFACE_AND_FRAGMENTATION_NOTES_20260419.md`](./ASK_SURFACE_AND_FRAGMENTATION_NOTES_20260419.md)
- [`JUDGE_PRIMITIVES_NOTES_20260419.md`](./JUDGE_PRIMITIVES_NOTES_20260419.md)
- [`WORKING_FORMALIZATION_NOTES_20260419.md`](./WORKING_FORMALIZATION_NOTES_20260419.md)
- [`NEURO_FOUNDATIONS_V1.md`](./NEURO_FOUNDATIONS_V1.md)
- [`ASK_DEMAND_TAXONOMY_NE13_20260418.md`](./ASK_DEMAND_TAXONOMY_NE13_20260418.md)
