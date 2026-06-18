# CORPUS_BASELINE

This is the first factual baseline for the fresh lab. It does not decide the publishable denominator. It makes the corpus legible enough to choose better slices, better probes, and better architecture tests.

## Current corpus surfaces

| Corpus | Window | Events | Observed days | Sources | Role in lab |
|---|---|---:|---:|---:|---|
| `NE-1` | `2025-08-20 -> 2026-03-16` | `318,088` | `152` | `11` | exploratory mother corpus |
| `Golden Gate` | `2026-01-17 -> 2026-02-22` | `89,240` | `37` | `4` | candidate clean replay slice |

Primary metadata sources:
- `_internal/syke-replay-lab/datasets/ne1.meta.json`
- `_internal/syke-replay-lab/datasets/golden-gate.meta.json`
- `_internal/syke-replay-lab/datasets/ne1.db`
- `_internal/syke-replay-lab/datasets/golden-gate.db`

## What NE-1 actually is

NE-1 is not a conversation benchmark and not even one stable harness history.

It is a mixed operator trace with:
- early `chatgpt` activity (`2025-08-20 -> 2025-12-19`)
- a long `codex` arc (`2025-08-20 -> 2026-02-18`)
- an `opencode` arc (`2025-12-24 -> 2026-03-16`)
- a `claude-code` arc (`2025-12-25 -> 2026-03-16`)
- a short but important `hermes` arc (`2026-02-27 -> 2026-03-15`)
- late `manual` observations (`2026-02-25 -> 2026-03-16`)
- thin but meaningful `github` activity across the span

That means the object already contains:
- source migration
- overlapping harnesses
- mixed machine/human traces
- explicit manual corrections
- changing runtime assumptions over time

## Top-line structural facts

### Source mix

Top source counts in NE-1:
- `opencode`: `122,326`
- `codex`: `110,383`
- `claude-code`: `82,308`
- `hermes`: `2,390`
- `github`: `416`

### Event-shape mix

Largest event-type buckets are not just human turns:
- `codex turn`: `70,264`
- `opencode tool_call`: `43,146`
- `opencode turn`: `37,702`
- `opencode tool_result`: `35,980`
- `claude-code turn`: `30,347`
- `claude-code tool_call`: `25,858`
- `codex tool_call`: `23,931`
- large `ingest.error` volumes on both `claude-code` and `codex`

Immediate implication:
this is not a clean message-only corpus. It is a mixed trace where tool behavior, filtered outputs, session boundaries, and runtime artifacts are part of the memory object.

## Burstiness and non-uniformity

Top NE-1 days by event volume:
- `2026-03-14`: `45,974`
- `2026-03-15`: `12,643`
- `2026-03-13`: `12,433`
- `2026-03-16`: `12,272`
- `2025-12-24`: `11,692`
- `2026-02-15`: `10,917`
- `2026-02-17`: `10,465`
- `2025-12-23`: `9,945`
- `2026-03-11`: `9,769`
- `2026-02-19`: `9,624`

Largest day-to-day jumps:
- `2026-03-13 -> 2026-03-14`: `12,433 -> 45,974` (`+33,541`)
- `2026-03-14 -> 2026-03-15`: `45,974 -> 12,643` (`-33,331`)
- `2025-12-24 -> 2025-12-25`: `11,692 -> 111` (`-11,581`)
- `2026-02-14 -> 2026-02-15`: `1,422 -> 10,917` (`+9,495`)
- `2025-12-22 -> 2025-12-23`: `1,436 -> 9,945` (`+8,509`)

Immediate implication:
any memory design that assumes smooth session-local accumulation will miss the real pressure. The corpus is bursty, cliff-like, and phase-shifted.

## High-overlap days

Days with the richest multi-source overlap are especially valuable because they expose cross-harness continuity pressure.

Examples:
- `2026-02-25`: `7` sources / `9,603` events
  - dominant: `opencode`
  - also: `claude-code`, `github`, `manual`, plus singleton system traces
- `2026-03-13`: `5` sources / `12,433` events
  - `claude-code` + `opencode` + `hermes` + `manual` + `github`
- `2026-03-14`: `5` sources / `45,974` events
  - huge `claude-code` burst plus `opencode`, `hermes`, `manual`, `github`
- `2026-03-15`: `5` sources / `12,643` events
- `2026-02-28`: `5` sources / `5,899` events

Immediate implication:
these are strong candidate slices for testing native-memory limits, provider-memory limits, and federated continuity designs.

## First real reading of the corpus

NE-1 already looks unlike benchmark memory objects in at least six ways:

1. **The trace is mixed human/system, not message-pure.**
2. **The active source changes over time.** `chatgpt` disappears; `codex` peaks and ends earlier; `opencode` and `claude-code` take over; `hermes` arrives late.
3. **The corpus has phase changes, not just long conversations.**
4. **The same operator intent is routed through multiple harnesses on the same day.**
5. **Manual observations appear late and selectively, acting like explicit repair or anchoring points.**
6. **Tool-call and session-lifecycle rows are part of the practical object, not incidental noise.**

## Why this matters for the lab

This baseline supports the lab's main direction:
- `NE-1` should be mined, not simplified away
- candidate slices should be derived from actual transitions and pathologies
- probe design should include mixed-trace, cross-harness, and resumption cases
- architecture comparisons must be run against the same evidence, not just the same question wording

## Immediate next moves

1. build `SLICE_ATLAS_V0.md` from the actual high-signal windows below
2. turn those slices into the first probe seeds
3. connect the slices to practical-value surfaces and architecture cases
