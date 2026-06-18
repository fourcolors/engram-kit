# NE_DATASET_ARCHITECTURE_V1

Public note:
Use this as a canonical dataset-definition doc.
Older slice/regime docs are internal observer material and not the public benchmark surface.

This is the canonical dataset architecture for the benchmark.

The benchmark should not be built around disconnected slices plus ad hoc bundle names. It should be built around three chronological benchmark datasets.

## Canonical benchmark datasets

### NE-1.1
- **Window:** `2026-01-09 -> 2026-02-08`
- **Role:** first month of the three-month arc
- **Purpose:** establishes the early regime: local benchmark/eval pressure, early continuity drift, and the start of the transition toward fragmentation

### NE-1.2
- **Window:** `2026-02-09 -> 2026-03-08`
- **Role:** second month of the arc
- **Purpose:** captures the strongest fragmentation-threshold and multi-harness pressure period, including forgotten-plan resumption, memex evolution, native/Hermes/Syke transition, and the Mar 13-15 cross-harness burst

### NE-1.3
- **Window:** `2026-03-09 -> 2026-04-08`
- **Role:** third month of the arc
- **Purpose:** captures the post-burst and current-era period, including the newer raw-harness work and the modern replay / benchmark substrate

## The full immutable arc

Taken together, these three datasets define the benchmark's immutable three-month continuity arc:
- **start:** `2026-01-09`
- **end:** `2026-04-09`

## Data policy

These datasets are **raw-first, hybrid where needed**.

That means:
- raw harness traces are primary when still available
- reconstructed raw-ish Claude Code files are allowed where the original JSONL was rotated away
- normalized replay transport is allowed only as explicit derived support, never as the claimed primary object

## Benchmark relationship

These datasets are the benchmark's top-level units.

- datasets define the long continuity scenarios
- observer windows are internal analytical subwindows inside those datasets
- bundles are frozen transport packages for running replay and evaluation
- benchmark items are scored continuity obligations anchored inside datasets, with observer windows kept only as reviewer receipts

## What this replaces

This architecture replaces:
- temporary `NE-1 / NE-2 / NE-3` naming
- `continuity-1m / continuity-2m / continuity-3m`

Those names are superseded and should not appear in the benchmark-facing docs.

## Why this is cleaner

This gives us:
- one simple chronology
- one simple naming scheme
- one simple benchmark story
- less confusion between corpus / bundle / benchmark

The benchmark should now refer to:
- the **NE dataset family**
- the **continuity templates** built over it
- the **frozen bundle transport** used for execution
