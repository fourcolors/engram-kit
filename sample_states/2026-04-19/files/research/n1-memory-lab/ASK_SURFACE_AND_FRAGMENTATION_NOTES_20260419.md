# Ask Surface And Fragmentation Notes — 2026-04-19

This note captures the main result of the repeated analysis passes over the real
ask corpus and the harness/memory-surface fragmentation problem.

It is not the final benchmark claim.
It is the current best understanding of what the asks and environment are doing.

---

## 1. What The Real Ask Surface Is Probing

The real ask surface is primarily probing whether a memory system can maintain
and expose the user's changing operative state well enough for correct
continuation under interruption.

That is the center of gravity.

Across the 50 asks, four pressures keep recurring:

- **continuation under interruption**
  - where are we now
  - what was I last working on
  - what is active / unfinished / latest

- **bounded activity reconstruction**
  - yesterday / today
  - last session
  - last week
  - be exhaustive / how many

- **object continuity through change**
  - what was the vision/history/evolution of X
  - what patches existed, changed, reverted
  - what did we learn about this subsystem

- **auditability / provenance pressure**
  - how did you know
  - what did you read
  - what evidence supports this
  - is the implementation actually what we claim

This means the asks are not just “memory categories.”
They are different ways of stressing the same maintained state.

---

## 2. What Must Not Be Collapsed Too Early

The corpus should not be flattened into one neat benchmark category too early.

Important tensions:

- fast restart usefulness vs exhaustive accounting
- current live state vs historical lineage
- bounded time slices vs evolving object continuity
- practical continuation vs provenance traceability
- remembered discussion vs committed implementation/config truth
- cross-surface integration vs narrow single-surface precision

These tensions are part of the problem.

---

## 3. Minimal Environment Commitments

The smallest set of environment commitments that still preserves the real
object is:

1. **time-bounded partial observability**
   - only evidence available by `t`
   - hidden state larger than the observable packet

2. **real continuity breaks**
   - preserve session rotation / restarts / interruptions
   - do not flatten everything into one continuous transcript

3. **distinct evidence surfaces with no forced merge**
   - traces
   - artifact truth
   - memory surfaces
   - overlapping but not pre-resolved

4. **in-slice provenance path**
   - a claim must be traceable through the bounded environment and its read
     contract, not only plausible in prose

If any of these are removed, the problem collapses into something weaker:

- static retrieval
- long-context QA
- single-corpus summarization
- unsupported narrative synthesis

---

## 4. Working Center

Current best center:

- the environment is a fragmented multi-harness human-machine world
- the asks probe how well a memory process reorients and exposes useful state
  across that fragmentation

This is broader than “restart” alone,
but restart / interruption recovery is still the strongest recurring pressure in
the current corpus.

---

## 5. Open Parts

Still open:

- the final benchmark claim language
- how broad the canonical ask surface should be
- which late ask families belong in the headline benchmark versus extension
  tracks
- the final judge schema and which sub-axes should be conditional
