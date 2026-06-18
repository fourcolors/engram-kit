# Judge Recalibration Notes — 2026-04-19

This note is for the next judge redesign pass.

It follows a stricter rule than previous notes:

- start from the environment definition
- inspect the real asks as lived asks
- inspect what the current judge actually measures
- only then decide what to change

It is not a final schema proposal.

---

## 1. Environment First

Current environment center:

**The system should maintain and expose a useful externalized self/world model for one human across many harnesses and time, so that asks at time `t` support useful continuation from the evidence available then.**

Implication for judging:

- the judge should not be asking "did it retrieve a fact?"
- it should be asking whether the answer exposed the right maintained state
  strongly enough for continuation

That means the environment already commits us to a small set of fundamental
requirements:

- boundedness to evidence at `t`
- relevance to the live working model
- update when facts or priorities changed
- coherence across partial memory surfaces
- continuation utility

---

## 2. What The Real Asks Look Like

The asks are not synthetic benchmark prompts.

They are compressed, situational, and often assume shared context.

Early period (`2026-03-08 -> 2026-03-16`):

- "what's the current state of things? what am I working on, what's active, what's the latest?"
- "What did we work on yesterday March 7 2026 and today March 8 2026? ... Be exhaustive."
- "what was I last working on in syke? what was left to do?"
- "remember all the threads we made yesterday and map the timeline for today and yesterday"
- "okay where are we now"

Middle period (`2026-03-19 -> 2026-03-31`):

- "what did I work on yesterday March 18 2026 about Syke Synthesis, Syke Map, architecture..."
- "What happened in the last one week? ... cover all platforms, all sessions, all projects."
- "what was the design for the syke sandbox and replay harness?"
- "what happened last? what was I working on most recently?"
- "what is the history of us adding and removing middleware patches in litellm_proxy.py?"

Late period (`2026-04-01 -> 2026-04-10`):

- "ask syke whats up"
- "Get a sense of where we are now. And get your update on the repo and our work"
- "Did you get the context from syke memex only or did you syke ask?"
- "we need to really know if our LLM as judge design is good"
- "Show me how replay loop is hardened and why the agent only sees until the simulated present"

The important point:

- the asks shift naturally from continuity under interruption
- to design-history and system-memory questions
- to explicit benchmark/method governance

This is still one environment.
The asks are different probes into the same maintained self/world model.

---

## 3. What The Current Ask-Demand Analysis Gives Us

The ask-demand note is useful as analysis, not as final ontology.

What it gives reliably:

- the current scored `R01-R19` set is all real reconstruction pressure
- `META_HANDOFF`, `DOC_SYNTH`, and `CONFIG_CHECK` do not dominate the current
  19-item set
- the major blind spots and vacuous judge sub-axes are visible

What it should not become too quickly:

- the benchmark's final category system

So the right use is:

- diagnostic lens
- not final ask ontology

---

## 4. What The Current Judge Gets Right

The current top-level axes are still directionally right:

- `factual_grounding`
- `continuity`
- `coherence`

They are trying to measure:

- whether the answer stayed bounded to evidence
- whether it restored the right live state
- whether it kept that state internally consistent across surfaces

That is much better than older memory benchmarks built around static recall.

We should preserve this direction unless the real data proves otherwise.

---

## 5. What The Current Judge Misses Or Over-Measures

### A. Missing: completeness pressure

Some asks are explicitly exhaustive:

- "List everything"
- "Be exhaustive"
- "what happened in the last one week ... cover all platforms"

The current judge has no explicit way to score whether the answer actually
enumerated enough of the relevant state.

So the judge can reward a bounded answer without checking whether it omitted
important in-scope items.

This is the strongest current missing pressure.

### B. Over-measured: cross-harness coherence

`cross_harness_braid` currently fires too often.

Only a minority of asks truly demand cross-harness integration.
On many other asks, scoring this sub-axis becomes vacuous and injects noise.

So the judge currently overstates coherence work on cells where the ask did not
actually demand it.

### C. Redundant splits

Some current sub-axes appear to be splitting one underlying thing into two:

- active thread selection vs salience relevance
- artifact routing consistency vs internal consistency

That may be useful analytically, but it may also create avoidable variance if
the asks do not force the distinction clearly.

### D. Weak handling of recency/last-thread asks

The ask analysis and ab07 stability both suggest:

- `LAST_THREAD`
- `STATE_NOW`

are among the noisiest regions.

That means the judge may not yet be sharp enough on:

- what counts as the live thread
- what counts as "most recent"
- how much stale residue is tolerable before continuation value collapses

---

## 6. What To Recalibrate First

First recalibration should be minimal:

1. keep the top-level 3-axis structure
2. re-think which sub-axes are conditional vs universal
3. add one explicit completeness mechanism for exhaustive asks
4. tighten the live-thread / recency interpretation

That means:

- do not redesign everything at once
- do not collapse back to one scalar score
- do not keep every current subcategory just because it exists

---

## 7. Practical Next Step

Before changing code, do one pass over the clean `R01-R19` set and answer:

- which asks truly require cross-harness reasoning?
- which asks truly require exhaustive enumeration?
- which asks are fundamentally recency/live-thread probes?
- which current sub-axes were actually doing useful work on those asks?

That is the immediate recalibration task.

Only after that should a new schema be wired into the judge tool.

---

## 8. Working Rule

The judge should be rebuilt from:

- the environment contract
- the real asks
- the actual failure patterns

not from inherited benchmark categories
and not from prior subcategory commitments alone.
