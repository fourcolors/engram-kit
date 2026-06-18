# Council Formalism — 2026-04-20

Status: merged result from a 3-lane council over the current literature stack and packet notes.

Scope:
- environment-side formal object
- judge-side stable object
- packet-sized math only

This note is intentionally small.
It replaces larger next-step stories, not the historical record.

---

## 1. Frozen benchmark object

For one eval item at reference time `t`:

`I_t = (t, q_t, E_t, r_t)`

Where:
- `t` = reference time
- `q_t` = real ask at time `t`
- `E_t` = bounded evidence packet available by `t`
- `r_t` = answer / reconstruction

The hidden operative state exists conceptually, but is not a scored object:

- latent state: `s_t`

The benchmark claim is only:

**bounded reconstruction of the closest correct operative state at time `t`, from `E_t`, for useful continuation**

Do not expand this into:
- full self/world-model claims
- trajectory beauty
- external task-completion framing
- computational-memory ontology as the scored object

---

## 2. Stable judge machine

Score each item in three stages:

`I_t -> D_t -> S_t -> V_t`

### Stage D: deterministic core

Use only checks the packet can actually ground.

`D_t = (d_time, d_artifact, d_committed, d_contra, d_complete*, d_cross*, d_prov*, c_type)`

- `d_time`
  - claims stay local to the reference time `t`
  - no future leakage

- `d_artifact`
  - named artifacts, entities, files, commits, sessions, configs, issues, branches, or docs actually exist in `E_t`

- `d_committed`
  - when the ask depends on repo/config/doc/runtime truth, the answer matches the bounded anchor

- `d_contra`
  - no material contradiction with bounded evidence

- `d_complete*`
  - fires only when the ask is explicitly exhaustive or countable

- `d_cross*`
  - fires only when the ask genuinely spans multiple surfaces and requires linking them

- `d_prov*`
  - fires only when the ask is audit-sensitive or asks how the claim was derived

- `c_type`
  - claim typing for important answer claims:
    - `verified` = directly supported in `E_t`
    - `inferred` = follows from a short bounded chain inside `E_t`, with no contradiction
    - `speculative` = not supportable from `E_t`, or stated too strongly for the evidence

### Stage S: semantic residual

Keep the residual extremely small:

`S_t = (s_state, s_restart)`

- `s_state` = operative-state adequacy
  - did the answer recover the right live thread, object state, or active context?

- `s_restart` = wrong-restart risk
  - if the user acted on this answer, how likely is it to send them down the wrong branch or revive stale residue?

This is the smallest residual justified by the packet.

---

## 3. Verdict rule

Use a coarse verdict:

- `pass`
- `partial`
- `fail`
- `invalid`

And report a secondary binary collapse:

- `useful = pass + partial`
- `not_useful = fail`

### Hard-cap logic

Semantic strength cannot rescue:
- central speculative claims
- major time errors
- material artifact mismatch
- central contradiction
- severe wrong-restart risk

### Working class meaning

- `pass`
  - core claims are verified or tightly inferred
  - low restart risk
  - specific enough to continue safely

- `partial`
  - mostly right state, but localized or bounded errors remain
  - useful with verification

- `fail`
  - contradiction, context confusion, stale-branch selection, or unsafe restart model

---

## 4. Minimal packet-sized math

Trust now:

- paired same-answer contingency tables under judge swap
- weighted Cohen's kappa on `fail / partial / pass`
- binary `useful` vs `fail` agreement
- McNemar on the binary collapse
- mean paired ordinal shift with `fail=0, partial=1, pass=2`
- per-probe instability rates

Use only as an organizing frame, not as a full fitted model:

- probe effect
- judge effect
- agent effect
- residual noise

Do not treat the current packet as licensing:

- full CyclicJudge ANOVA claims
- exact variance-component estimates
- IRT
- conformal intervals
- calibration heads
- large judge panels as if already required by the data

---

## 5. What the current packet supports

The packet supports these claims:

- judge identity is a first-order confound
- the task is beyond simple recall
- dominant failures are wrong state selection and stale-branch reconstruction
- the old rubric is over-specified / factor-collapsed, not fully incoherent
- `pass vs partial` is less stable than `useful vs fail`
- hybrid judging is justified:
  - deterministic checks first
  - narrow semantic residual second

The packet does not yet support:

- mature architecture ranking
- broad psychometric stories
- a large computational-memory axis ontology

---

## 6. What to demote in the current stack

Demote from the immediate next-step layer:

- `P1..P5 / C1..C6` primitive-axis scoring as the next contract
- exact-cancellation CyclicJudge language as if it is the current method
- large future panel protocol as if it is required before rubric cleanup
- broken or weakly grounded feature math from Batch F
- any wording that says the old schema is simply incoherent

Prefer:

- one small item object
- one deterministic core
- one tiny semantic residual
- one coarse verdict
- one binary stability view

---

## 7. Ordered next move

1. Rewrite the judge contract around `D_t` and `S_t`.
2. Rejudge the existing packet with that smaller contract.
3. Check only:
   - coherence of the smaller schema
   - factor collapse
   - binary usefulness stability
   - per-probe instability
4. Only then decide whether judge rotation or same-judge repeats are needed next.

That is the smallest defensible path from this packet.
