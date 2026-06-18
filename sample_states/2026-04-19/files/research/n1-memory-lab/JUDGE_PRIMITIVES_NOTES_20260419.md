# Judge Primitives Notes — 2026-04-19

This note turns the repeated ask-surface and fragmentation analysis into the
next judge-design question:

**What should the judge always test, and what should it test only when the ask actually demands it?**

This is not the final schema.
It is the next disciplined step before changing the judge contract.

---

## 1. Why We Need Primitives

The current top-level axes are directionally useful:

- `factual_grounding`
- `continuity`
- `coherence`

But the subcategory structure beneath them is still too static for the real ask
surface.

The ask analysis now shows:

- some pressures are present on almost every real ask
- others are real but only conditional
- some late ask families are likely extension tracks, not canonical benchmark
  center

So the judge should be rebuilt around **primitives** first, and only then
assembled into a schema.

---

## 2. Universal Judge Primitives

These should be present on nearly every canonical continuity ask.

### A. Bounded support

Question:

- is the answer supported by what was actually available in the bounded packet
  by time `t`?

Why universal:

- every ask still depends on evidence-boundedness
- without this, the benchmark becomes narrative plausibility

Current relatives:

- `factual_grounding.support`
- `factual_grounding.boundedness`

### B. Time-local correctness

Question:

- did the answer stay correct for the reference moment rather than drifting to
  earlier or later state?

Why universal:

- all canonical asks are historical asks at time `t`
- even “what happened last?” is still indexed to `t`

Current relatives:

- parts of `continuity`
- parts of `factual_grounding.boundedness`

### C. Operative state adequacy

Question:

- did the answer recover enough relevant operative state for the user to
  continue correctly?

Why universal:

- this is the center of the ask surface
- current state, last thread, bounded history, object continuity, and next-step
  asks all rely on recovering the right state, not just stating facts

Current relatives:

- `continuity.active_thread_selection`
- `continuity.salience_relevance`
- `continuity.continuation_value`

### D. Wrong-restart risk

Question:

- would this answer send the user down the wrong branch, revive stale residue,
  or hide the necessary next move?

Why universal:

- the ask surface repeatedly stresses interruption recovery and restart utility
- broad but wrong summaries are dangerous

This is not explicit enough in the current schema and should become first-class.

---

## 3. Conditional Judge Primitives

These are real, but should only fire when the ask demands them.

### A. Enumeration completeness

Question:

- for asks that demand exhaustive coverage, did the answer include enough of the
  in-scope state?

Fire when:

- the ask explicitly demands “everything,” “entire day,” “all platforms,” “how
  many,” “full timeline,” etc.

Why:

- current schema under-measures this
- omission is itself a failure on these asks

### B. Cross-surface integration

Question:

- when the ask actually spans multiple harnesses or evidence surfaces, did the
  answer braid them into one coherent state?

Fire when:

- the ask is truly cross-harness or cross-surface

Why:

- this pressure is real but not universal
- scoring it on every ask creates vacuous noise

Current relative:

- `coherence.cross_harness_braid`

### C. Object continuity through change

Question:

- for asks about one evolving object, did the answer preserve the identity and
  meaningful evolution of that object rather than flattening it to one snapshot?

Fire when:

- the ask is about the history, evolution, or design of a named thing

Why:

- these asks are common and important in the corpus
- they are not equivalent to simple recency or bounded time windows

### D. Committed-state fidelity

Question:

- when the ask depends on repo/config/doc/runtime truth, did the answer match
  that committed external reality rather than remembered intent?

Fire when:

- config, docs, repo state, or implementation truth are part of the ask

Why:

- conversationally plausible but stale answers are especially dangerous here

### E. Provenance / derivation traceability

Question:

- when the ask challenges how the answer was derived, can the answer expose the
  path of evidence and method clearly enough?

Fire when:

- the user asks how context was obtained, what was read, or why a claim/count is
  justified

Why:

- this becomes real in the later corpus
- it should not contaminate every canonical continuity ask by default

---

## 4. Things To Keep Out Of The Canonical Judge For Now

These may matter later, but should not be forced into the next schema too
quickly:

- broad self/world-model scoring
- personal identity fidelity
- generic preference-memory scoring
- social/relationship continuity
- open-ended governance/meta-handoff families as if they were the same as
  continuity asks

These are not yet clearly exercised by the current canonical benchmark surface.

---

## 5. Working Shape

If the judge were rebuilt from these notes, the likely structure would be:

### Universal

- bounded support
- time-local correctness
- operative state adequacy
- wrong-restart risk

### Conditional

- enumeration completeness
- cross-surface integration
- object continuity through change
- committed-state fidelity
- provenance / derivation traceability

That is the cleanest next direction so far.

---

## 6. Immediate Next Step

Before changing code:

1. mark the canonical ask set with which conditional primitives are actually in
   play
2. re-read a clean result surface with those primitives in mind
3. then rewrite the judge schema/tool contract accordingly
