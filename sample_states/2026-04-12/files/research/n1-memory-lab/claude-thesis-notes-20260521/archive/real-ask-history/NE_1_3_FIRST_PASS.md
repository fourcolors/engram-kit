# NE-1.3 First Pass

This is the smallest honest first experiment for the current `n=1` lane.

The goal is not to define a new benchmark category.
The goal is to test whether a Syke continuity substrate improves continuity
and reduces reconstruction waste in the same environment.

## Fixed

- same NE-1.3 frozen slice
- same eval panel
- same model/runtime
- same sandbox
- same judge protocol

## Variable

Only the continuity substrate changes:

1. `pure`
   - no Syke memex
   - no Syke prompt framing
   - minimal generic prompt over the same sliced data
2. `syke_zero`
   - Syke memory substrate built from the `zero` replay condition
   - same ask path as production Syke
3. `syke_prod`
   - current production Syke substrate

## What we measure

### Continuity

Agentic judge verdict:

- `pass`
- `partial`
- `fail`

Primary score:

- **UAR** = `(pass + partial) / judged`

### Efficiency

Deterministic trace metrics:

- zero-search yes/no
- tool-call count
- cost

## Comparison rule

- compare useful vs not-useful with paired McNemar
- if continuity ties, prefer the lower-waste condition

## First NE-1.3 panel (8)

1. `P10` — map threads across harnesses
2. `P13` — what is worth tracking vs ignoring
3. `P23` — what was I actually working on across tools
4. `P26` — did claude-code and opencode duplicate or complement
5. `P30` — compact handoff from the Mar 14 spike
6. `P31` — what does the Mar 14 summary get wrong by Mar 16
7. `P44` — top priorities after the spike
8. `P61` — what survived compaction and what was lost

## Why these evals

They cover the main NE-1.3 continuity pressures:

- cross-harness braid
- burst carryover
- compaction
- stale-summary rejection
- currentness

## What this first pass should support

Bounded claim:

> On NE-1.3, Syke improves continuity and reduces reconstruction waste
> over a no-Syke baseline in the same environment.

## What this first pass should not support

- broad benchmark-category claims
- universal memory-system superiority claims
- RL or self-observation claims
- paper-level external claims
