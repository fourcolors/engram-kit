# Formalism Layer Separation — 2026-04-20

Status: compact clarification note

Purpose:
- separate the layers we kept mixing
- explain why the judge framing narrowed without abandoning the partial-observability view

---

## 1. Environment formalism

This is still the broadest and most important layer.

At reference time `t`:

- latent operative state: `s_t`
- bounded observations up to `t`: `o_{<=t}`
- ask at time `t`: `q_t`
- answer / reconstruction: `r_t`

The environment claim is:

**one human, many harnesses, fragmented partial memory surfaces, and a memory process that must maintain enough correct operative state over time for useful continuation**

This is still a partial-observability framing.

What remains true here:
- the true user/work state is never fully visible
- the system only sees bounded traces
- the ask is answered from incomplete evidence
- the main failure is often wrong live-state selection, not simple fact omission

What we are **not** claiming yet:
- a fully specified state space
- a stable transition model
- a clean control-theoretic reward process
- a scored latent world model

So the environment can remain POMDP-like in spirit without pretending we have fully formalized the whole state machine.

---

## 2. Judge formalism

This is narrower than the environment on purpose.

The judge does **not** observe `s_t`.
The judge observes:

- bounded packet `E_t`
- ask `q_t`
- answer `r_t`

So the judge should score only what is defensibly accessible from that view.

That is why the judge got compressed toward:

- deterministic checks
- small semantic residual
- coarse verdict

The key reason for narrowing:

**the environment may be rich and partially observable, but the scored judge object is much smaller**

The judge is not yet in a position to reliably score a large latent-state ontology.

So the narrower judge is not a retreat from the environment formalism.
It is a refusal to overclaim what the current packet can support.

---

## 3. Reliability / benchmark math

This is a different layer again.

These factors are about whether the benchmark is measuring anything stably:

- probe difficulty
- judge identity
- judge stochasticity
- agent stochasticity

This is where the variance language belongs.

Why it matters:
- architecture claims are unsafe if judge and agent noise dominate
- cross-judge disagreement is a property of the measurement process, not of the environment definition
- same-answer judge swaps tell us about benchmark reliability, not about the user's memory problem directly

So the factor math was not wrong.
It was being mixed into the wrong layer.

Use it for:
- reliability gates
- calibration decisions
- deciding when rankings are trustworthy

Do not use it as the primary definition of the task itself.

---

## 4. Cognitive / computational-memory interpretation

This is the interpretive layer.

Here belong ideas like:

- updating
- temporal binding
- interference
- pattern completion
- pattern separation
- consolidation
- state revision

These are useful because they help explain what type of memory burden a real ask is imposing.

But right now they are better treated as:

- research lenses
- analysis vocabulary
- future stress-test families

not as the immediate scored contract.

Why:
- the current packet does not cleanly identify all of these as separate measurable judge dimensions
- if we score them too early, we will turn research vocabulary into fake precision

So this layer stays alive, but above the current judge contract.

---

## 5. What actually changed

What changed was not the deep story.

### What did **not** change

- partial observability still holds
- latent operative state still matters
- reconstruction still matters
- continuation utility is still the task center
- the real failure is still often wrong restart / wrong thread / stale branch

### What **did** change

- we stopped letting the judge pretend to score the whole richer theory directly
- we separated environment formalism from judge formalism
- we separated reliability math from both
- we separated cognitive-memory interpretation from the immediate scoring object

That is the real cleanup.

---

## 6. Why the phrase changed

Earlier language like:

- partially observable state-space reconstruction

is still directionally right, but too strong as the immediate scored claim.

Why it was softened:

1. `state-space` implies a cleaner modeled ontology than we currently have
2. the judge only sees bounded evidence and answer text
3. the real packet supports a smaller scored object than a full latent-state formalism

So the council compressed the judge-side wording toward:

**bounded reconstruction of the closest correct operative state at time `t`**

That wording keeps:
- boundedness
- time-locality
- reconstruction
- statefulness
- continuation utility

while avoiding:
- premature claims of a fully modeled state space
- scoring more latent structure than the packet can justify

---

## 7. Current best separation

If we keep the layers clean:

- **Environment**:
  latent operative state under partial observability across fragmented harnesses over time

- **Judge**:
  bounded evidence check + small residual judgment about operative adequacy and restart safety

- **Reliability math**:
  measure probe / judge / agent / residual noise before trusting rankings

- **Cognitive interpretation**:
  use computational-memory concepts to interpret asks and design future probes, not to over-specify the current judge

That is the most coherent form of the work so far.
