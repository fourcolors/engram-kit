# NE-1.3 Real Ask Evals V1

These evals are derived from actual asks in raw Mar 13-16 usage.

They are meant to replace the old habit of treating NE-1.3 as a neat benchmark
panel. The point is to keep the eval object tied to real continuity pressure.

## Core rule

The ask is an indicator of real usage.
It does **not** mean the answer must already exist inside Syke at that exact
moment.

Judge against:

- the full raw slice around the ask
- the state of the person/work at that time
- whether the answer would actually help the user continue
- the time-contained local git set up to that time, as a truth anchor for
  code/work-state reality

Do **not** judge only:

- whether Syke had already serialized the answer
- whether one benchmark-style answer string was present

## Why these evals are different

These asks are not generic memory QA.
They are direct continuity burdens from the trace:

- recover the live thread map
- reconstruct yesterday and today
- know where we are now
- preserve corrections and contradictions
- recover the handoff
- get back to the previous thread
- know what is still live and what is residue

That is why the success metric must be framed around stabilization:

- does the answer restore the right working model?
- does it reduce entropy for the user?
- does it let work continue with low reconstruction cost?

## How to read pass / partial / fail

### Pass

The answer restores a usable model cleanly enough that the user can continue.
It recovers the right active work graph, points at the right artifact or next
step, and stays faithful to the relevant time-local reality.

### Partial

The answer is useful but incomplete.
It reduces entropy, but still leaves meaningful reconstruction work for the
user: maybe the live-vs-residue distinction is fuzzy, maybe the next artifact
is unclear, maybe the timeline is coarse, maybe some braid edges are missing.

### Fail

The answer does not restore a safe or useful working model.
It may flatten changing state, miss major live threads, confuse residue for
current work, or overclaim beyond what was knowable then.

## Why this helps later GEPA-style improvement

These evals should produce richer judge notes, not just verdicts.

The important thing for later prompt evolution is that the judge can explain,
in natural language, what entropy remained:

- was the time handling blurry?
- did the answer lose an active thread?
- did it confuse residue for live work?
- did it point at the wrong artifact?
- did it preserve the wrong state after a correction?

That should emerge from the notes, not from a hard-coded tag system.

## Ask vs judge separation

The ask side should stay simple.

- Syke ask or a baseline prompt should answer from its intended memory surface.
- The ask does not need special git logic.

The judge side gets the stronger anchors.

- The ask should answer from its intended memory surface.
- The judge can use the time-contained local git set to verify what had
  actually happened in code by that time.
- That is a judge/truth-anchor concern, not an ask-side concern.

## Current real-ask set

The YAML file defines:

- `P62` timeline + thread recovery
- `P63` live-state reentry
- `P64` updated thread map after edits
- `P65` contradiction-repair learning
- `P66` handoff recovery
- `P67` get back to the previous testing thread
- `P68` open work graph / priorities / unfinished work
- `P69` memory-tools study as actionable pattern extraction
- `P70` open Observe threads after burst, with live-vs-residue discrimination
- `P71` why Observe still does not feel complete

## Practical implication

If these work, the benchmark stops asking:
"did it remember the benchmark fact?"

and starts asking:
"did it restore the right live working model with low reconstruction waste?"
