# NE-1.3 Month Map V1

Scope: roughly `2026-03-07 -> 2026-04-10`

Purpose:

- keep the eval set from overfitting to the Mar 13-16 burst
- track how the continuity burden changes shape across the month
- identify where local git materially changes truthfulness

## 1. Mar 7 -> Mar 12

Dominant burden:

- current-state truth
- active work recovery
- roadmap / what is live
- memory-vs-reality verification

Harness shape:

- mostly `claude-code + opencode`
- `codex` effectively absent

Good ask shapes here:

- what is the current state
- what am I working on
- what is active
- what is stale vs real

## 2. Mar 13 -> Mar 16

Dominant burden:

- timeline reconstruction
- thread-map recovery
- handoff recovery
- live-vs-residue discrimination
- resumption after interruption

Harness shape:

- still `claude-code + opencode`
- huge Claude burst on Mar 14
- still no meaningful Codex presence

Good ask shapes here:

- where are we now
- remember all the threads from yesterday
- what happened in the last session
- what stayed live after the burst
- can we get back to the previous thread

## 3. Mar 17 -> Mar 20

Dominant burden:

- architecture/state codification
- synthesis correctness
- what the system now is
- canonical docs / benchmark / architecture truth

Harness shape:

- Claude + OpenCode still primary
- Codex begins to enter around Mar 20

Good ask shapes here:

- what architecture/state has actually been established
- what is the current synthesis/replay structure
- what changed from the earlier continuity story

## 4. Mar 20 -> Mar 25

Dominant burden:

- harness-mix shift
- implementation-state truth
- baseline / ablation / eval thinking
- same ask shape, different right answer

Harness shape:

- `codex` becomes real
- object becomes less purely Claude/OpenCode

Good ask shapes here:

- what changed now that Codex is part of the object
- what is true in code vs still only discussed

## 5. Mar 26 -> Apr 3

Dominant burden:

- runtime/productization truth
- what the current contract is
- setup / daemon / state ownership truth

Harness shape:

- Codex becomes substantial
- local git matters much more

Good ask shapes here:

- what is Syke now
- what is the runtime contract now
- what setup actually does
- what shipped vs what is still live

## 6. Apr 7 -> Apr 10

Dominant burden:

- replay/eval self-audit
- old-architecture residue vs current runtime truth
- benchmark / sandbox correctness

Harness shape:

- code-state-heavy
- local git strongly informative

Good ask shapes here:

- what does the current system really do
- what is stale narrative residue
- what replay/eval claims are actually true

## Key month-scale point

The continuity burden changes shape across NE-1.3.

So a good `50` should include:

- repeated ask shapes across time
- asks where the same shape has a different right answer later
- early continuity asks
- burst/resumption asks
- later code-state and runtime-truth asks
