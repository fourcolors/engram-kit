# Working Formalization Notes — 2026-04-19

This note collects today's working understanding of the problem before any new
judge redesign.

It is not the final formal spec.
It is the current coherent place to work from.

---

## 1. What MemoryArena Is Actually Doing

MemoryArena is a benchmark for **multi-session Memory-Agent-Environment loops**.

Its core move is important:

- memory is not tested as isolated recall
- action is not tested in a single memoryless session
- instead, the agent interacts with an environment, distills experiences into
  memory, and then uses that memory to solve later subtasks

That is the useful formal contribution.

In plain language:

- memory is acquired during action
- memory is used in later action
- the task is spread across multiple sessions
- the environment matters

This is closer to the right shape than older memory benchmarks that mostly test
"can you remember a fact from a prior conversation?"

Sources:

- [MemoryArena paper](https://arxiv.org/abs/2602.16313)
- [MemoryArena site](https://memoryarena.github.io/)

---

## 2. Where MemoryArena Aligns With Syke Replay

The alignment is real:

- memory and action are coupled
- the environment matters
- later success depends on what was preserved earlier
- multi-session structure matters
- memory is not just a static store queried after the fact

This means MemoryArena is a useful neighboring formalism.

It helps justify language like:

- memory-agent-environment loop
- interdependent multi-session tasks
- memory used to guide future decisions

Those are good outer concepts for Syke Replay.

---

## 3. Where Syke Replay Is Different

Syke Replay is not just another MemoryArena-style task suite.

The important difference is the object being modeled.

MemoryArena:

- human-crafted interdependent tasks
- explicit subtasks and answers
- environment is structured around those tasks

Syke Replay:

- one human's evolving digital life
- many harnesses
- many partial memory surfaces
- asynchronous and asymmetric traces
- the important object is not pre-written in the environment
- it has to be inferred from fragments

So the environment is not "a task with subtasks."
It is "a fragmented world with partial observations."

That is why Syke Replay feels closer to state estimation than to ordinary task
solving.

---

## 4. Current Best Environment Definition

Current tight formulation:

**One human, many harnesses, many partial memory surfaces, and one memory process responsible for maintaining a coherent and useful externalized self/world model across them over time.**

This is better than just saying "reconstruction" because it implies:

- maintenance
- update
- continuity
- many memory surfaces already exist
- Syke is not the only memory in the world
- the hard problem is coherence across fragmented memories

Task version:

**At time `t`, using only the evidence available by then, the system should maintain and expose that externalized self/world model in a way that supports useful continuation.**

This is the current best simple statement.

---

## 5. What The Real Asks Are Doing

The asks are not abstract memory tasks.
They are natural human requests for continuity under interruption.

The strongest recurring patterns are:

- orientation
  - "where are we now"
  - "what's active / latest"

- recency / handoff
  - "what was I last working on"
  - "what happened last"

- time-bounded reconstruction
  - "what happened yesterday / today"
  - "give me my work log"
  - "what happened in the last week"

- evolving object recovery
  - "what is the full vision for Observe"
  - "what was the evolution of X"
  - "what did we learn about Y"

- continuation pressure
  - "what is left"
  - "what changed"
  - "what should happen next"

Late in the corpus, the asks shift again:

- they become about benchmark/governance/method itself
- provenance starts to matter explicitly
- the user tests whether the system is faking understanding

So the asks are best understood as **behavioral probes of continuity pressure**
rather than static benchmark categories.

---

## 6. What The Current Judge Gets Right

The current environment contract is already mostly right:

- bounded evidence
- explicit time `t`
- no future leakage
- no live global contamination
- useful continuation as the success condition

The current top-level judge axes are also directionally right:

- `factual_grounding`
- `continuity`
- `coherence`

They are trying to answer:

- was the answer bounded and true?
- did it restore the right live working model?
- did it keep the world-model coherent across surfaces?

That is much closer to the real problem than old recall-only memory benchmarks.

---

## 7. What The Current Judge Misses

The main problem is not that the judge is useless.
It is that the current subcategory design is still mismatched to the real ask
surface.

Most important mismatches from the local ask-demand analysis:

- exhaustive / quantitative asks are under-measured
  - there is no explicit completeness check

- cross-source coherence is over-scored
  - it fires on too many asks where it is vacuous

- some sub-axes are redundant
  - they split distinctions the asks do not actually demand separately

- different asks likely need different sub-axis activation
  - one static subcategory block for every probe is probably wrong

So the next redesign should likely be:

- ask-driven
- conditional
- simpler

not more elaborate.

---

## 8. Working Direction

The order should be:

1. keep the environment definition stable
2. treat the asks as probes of continuity pressure
3. redesign the judge from the asks upward
4. only then lock a new schema

That means:

- do not over-attach to the current subcategories
- do not over-attach to later ask-demand labels either
- use both as analysis tools
- keep the center on the environment and the asks

---

## 9. Compressed Version

MemoryArena gives the right outer idea:

- memory-agent-environment loops
- multi-session dependence
- memory guiding later action

Syke Replay is a more specific case:

- one human
- many harnesses
- many partial memory surfaces
- one memory process maintaining a useful externalized self/world model over time

The asks are natural probes of whether that model was preserved and exposed well
enough for continuation.

So the next work is:

- not more environment churn
- not more generic benchmark categories
- but a stricter, ask-driven judge redesign built on this environment.

---

## 10. Debate Resolution (5 rounds)

After a structured multi-agent debate over the local corpus, current runs, and
formal notes, the most defensible resolved position is:

### What is stable now

- The environment should stay fixed.
- The current canonical workflow remains:
  - one real ask at reference time `t`
  - one bounded historical packet
  - one condition-specific ask-visible state surface
  - one judged answer

### Narrow canonical benchmark claim

For the current canonical scored surface, the safest claim is:

**Syke Eval tests whether a memory architecture improves bounded reconstruction of the user's active project state at time `t` well enough to support interruption recovery and useful continuation.**

Why this is the right narrowing:

- it stays faithful to the asks in `R01-R19`
- it avoids overclaiming "full self/world model"
- it still captures the interesting object: continuation under interruption

### Canonical ask surface

Current recommendation:

- lock `R01-R19` as the canonical continuity benchmark surface

Reason:

- those asks are all genuine reconstruction pressure
- they stay close to continuity under interruption
- they do not yet drift into explicit benchmark governance

The corpus after that is still valuable, but should be treated as extension
families rather than folded unqualified into the headline benchmark claim.

### What the canonical surface actually covers

The canonical surface primarily probes:

- current-state orientation
- last-thread / recency recovery
- time-bounded work reconstruction
- open work / next-step recovery
- design-history recovery of project objects

It does **not** yet justify a broader claim about the user's full self/world
model in the strongest sense.

### Judge implication

The single most important shift for the next judge design is:

- stop rewarding broad world-model summaries
- score whether the answer reconstructs the minimum correct working state
  needed to safely resume the interrupted thread

Practical judge center:

- right active thread
- right current status
- right blocker / next step
- bounded evidence support
- low wrong-restart risk

### What stays open

Still open for redesign:

- the exact subcategory schema
- whether `coherence` remains a top-level universal axis or becomes more conditional
- how exhaustive / quantitative asks should be scored
- how later ask families (`R20+`) should be split into extension benchmark tracks
