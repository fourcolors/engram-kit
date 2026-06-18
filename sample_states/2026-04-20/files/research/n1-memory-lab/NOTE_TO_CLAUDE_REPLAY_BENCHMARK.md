# Note to Claude — Replay + Benchmark Alignment

You are working on the replay lab alignment to `0.5.2`. That work is useful and necessary. But there is one critical research constraint you must preserve while finishing it:

## 1. Do not accidentally benchmark the old packaging

The product architecture has moved.

Current live assumption:
- **raw harness traces are the real evidence object**
- adapter markdowns tell the runtime how to read each harness directly
- `syke.db` is the single mutable learned-memory store
- `MEMEX.md` is the routed projection
- there is **no separate product ontology built around `events.db`**

So if replay still uses a frozen normalized trace bundle for reproducibility, that is acceptable **only as a derived evaluation transport format**.

Do **not** let the benchmark language imply that the normalized replay DB is the true memory object.

Use this exact framing:
- **raw harness traces are the primary object**
- **frozen replay bundles are derived artifacts for reproducible evaluation**
- the benchmark claims are about the underlying raw trace object, not about the convenience packaging layer

## 2. What the benchmark is actually trying to test

Not: generic retrieval on synthetic corpora.

It is trying to test whether a memory system preserves the right live working model of one changing person across:
- time
- harnesses
- interruptions
- reversals
- architecture shifts
- noisy tool traces

That means the benchmark must include three kinds of evaluation:

### A. Probe Track
Direct prompts against real slices.
This historical probe-seed surface now lives in `research/n1-memory-lab/archive/benchmark-legacy/PROBE_SEEDS_V1.md`.

### B. Practical Task Track
Tasks that measure day-to-day value beyond explicit QA:
- resume the active work graph
- identify the canonical artifact to read first
- recover what is still live after a burst
- choose the right memory layer to trust
- reduce search entropy
- preserve continuity contracts

### C. Architecture Replay Track
Same frozen slice, different memory architecture:
- native harness memory
- Hermes/provider/plugin memory
- Syke/federated continuity
- retrieval-only / static-summary / evolving-memex baselines as needed

The key empirical object is:
**same data, different memory architecture, different continuity outcome**

## 3. Current strongest slices in the lab

Use the current lab artifacts instead of inventing new denominator logic.

Current strongest slices are:
- `S03` — forgotten-plan / return-after-gap
- `S04` — memex evolution / doc hygiene / practical value
- `S05` — native/Hermes/Syke transition surface
- `S07` — cross-harness recall under pressure
- `S08` — post-burst stabilization

Files:
- `research/n1-memory-lab/CORPUS_BASELINE.md`
- `research/n1-memory-lab/SLICE_ATLAS_V0.md`
- `research/n1-memory-lab/SLICE_CARDS_V1.md`
- `research/n1-memory-lab/SLICE_SCORECARD_V0.md`

## 4. Critical benchmark comparisons already exist

Do not restart these from scratch.

Existing lab memos:
- `research/n1-memory-lab/REAL_VS_BENCHMARK_V0.md`
- `research/n1-memory-lab/S03_VS_LONGMEMEVAL.md`
- `research/n1-memory-lab/S07_VS_LOCOMO_LIFEBENCH.md`
- `research/n1-memory-lab/ARCHITECTURE_COMPARISON.md`
- `research/n1-memory-lab/ARCHITECTURE_EXPERIMENT_MATRIX_V1.md`
- `research/n1-memory-lab/BENCHMARK_V0.md`
- `research/n1-memory-lab/BENCHMARK_PACK_V1.md`
- `research/n1-memory-lab/BENCHMARK_ITEMS_SPEC_V1.md`
- `research/n1-memory-lab/BENCHMARK_SCORING_RUBRIC_V1.md`
- `research/n1-memory-lab/BENCHMARK_EXECUTION_PROTOCOL_V1.md`

> **Superseded:** The old BENCHMARK_* inventory has now been archived. The active path is the canonical real-ask set `research/n1-memory-lab/NE_1_3_REAL_ASK_EVAL_SET.yaml`, the active runsets in `_internal/syke-replay-lab/probes/REAL_ASK_RUNSETS.yaml`, `research/n1-memory-lab/SCORING_METHOD_V3.md`, and the rewritten `benchmark_runner.py`. Do not reference the archived inventory for new work.

These are the current research line. Preserve and build on them.

## 5. What you should do next

### Replay substrate side
Yes, finish the replay alignment to `0.5.2`.
That includes:
- `syke.db`-based replay workspace
- adapter-driven workspace init
- no stale `events.db` assumptions
- a reproducible frozen-bundle workflow

### Research/benchmark side
Then wire replay into the benchmark in this order:

1. **Freeze one or two first benchmark slices**
   - prefer using the existing slice cards, not ad hoc windows
   - keep denominator language provisional unless the evidence truly earns a lock

2. **Instantiate executable benchmark items**
   - convert the 50 probe seeds into machine-readable benchmark items
   - preserve raw-source provenance and slice IDs per item

3. **Add the practical task track**
   - do not reduce the benchmark to direct QA only

4. **Run architecture-parity comparisons**
   - same slice bundle
   - same prompt family where applicable
   - different memory architecture conditions

5. **Report profile, not leaderboard fantasy**
   - family scores
   - slice scores
   - architecture scores
   - practical-value outcomes
   - failure gallery

## 6. Claims you must not accidentally make

Do **not** imply:
- the replay bundle is the true ontological object
- one user generalizes to the population
- one prompt variant is the final memory architecture
- benchmark work is useless
- the benchmark is “solved” because a retrieval baseline looks good on a few direct questions

Do say:
- current benchmarks remain useful, but are under-complete for the `n=1` object
- raw harness traces are structurally different from benchmark corpora
- the benchmark uses frozen replay bundles as reproducible derived artifacts
- same-data / different-architecture comparisons are the key empirical surface

## 7. Immediate acceptance criteria for your next pass

Your next benchmark/replay pass should leave behind:
- replay language fully aligned to `syke.db` / adapter / raw-trace-first architecture
- one explicit note in the benchmark/replay docs that the replay bundle is derived, not the primary object
- executable benchmark item schema for at least the first slice family
- a plan for practical task-track items, not probes only
- one clear first runnable benchmark bundle

## 8. The co-author line

The paper/benchmark is strongest if it says:

> Personal memory is not just retrieval over a fixed corpus. It is the maintenance of a coherent working model of one changing person across tools and time. The replay bundle is only the frozen evaluation transport. The real object is the raw cross-harness trace.

Build toward that line.
