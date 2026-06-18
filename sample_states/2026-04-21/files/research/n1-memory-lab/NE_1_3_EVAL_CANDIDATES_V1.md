# NE_1_3_EVAL_CANDIDATES_V1

NE-1.3 is still under-itemized. These are the strongest late-window candidates for closing that gap without drifting back to middle-month slices.

Grounding used:
- `_internal/syke-replay-lab/bundles/ne-1.3/dataset.meta.json`
- `_internal/syke-replay-lab/bundles/pure-syke/meta.json`
- `_internal/syke-replay-lab/bundles/s07-cross-harness/meta.json`
- `_internal/syke-replay-lab/bundles/s08-post-spike/meta.json`
- `_internal/syke-replay-lab/runs/azure_smoke/replay_results.json`
- `_internal/syke-replay-lab/runs/b1_production/replay_results.json`
- `research/n1-memory-lab/NOTE_TO_CLAUDE_REPLAY_BENCHMARK.md`
- `research/n1-memory-lab/SLICE_CARDS_V1.md`
- `research/n1-memory-lab/ARCHITECTURE_EXPERIMENT_MATRIX_V1.md`
- `research/n1-memory-lab/BENCHMARK_ITEMS_PUBLIC_V1.yaml`
- `research/n1-memory-lab/BENCHMARK_REGIMES_V2.md`
- `research/n1-memory-lab/BENCHMARK_PACK_V2.md`

The late-period pattern is:
- raw traces are primary
- frozen replay bundles are derived transport
- the hard cases are currentness, reconstruction, and architecture-boundary routing
Use the `NE13-W*` IDs below when mapping public eval items back to observer provenance.

## 1) 2026-03-13 -> 2026-03-16
- **Window ID:** `NE13-W1`

What was happening:
- `S07` cross-harness recall under pressure, then `S08` post-spike stabilization
- explicit “remember all the threads” pressure, followed by the live-vs-residue problem

Why it matters:
- this is the cleanest burst pair in the late arc
- it tests reconstruction first, then compaction and currentness
- it is the best place to separate “same data” from “same architecture”

Regime: `R2`
Claim type: `hybrid` / `stress`

Eval prompts:
- “Map the threads we were trying to build yesterday and today across the different harnesses.”
- “After the giant Mar 14 burst, what should still be considered live and what should be treated as residue?”
- “How does the forgotten-plan window connect to the later cross-harness remember-all-the-threads window?”

## 2) 2026-03-23 -> 2026-03-25
- **Window ID:** `NE13-W2`

What was happening:
- pure-syke bundle bootstrap
- replay bundle materializer work
- raw-first copying / file-format mapping across Claude Code, Codex, Opencode, and Hermes
- then the first dense follow-through days in the pure-syke run, where the route map begins to carry the NE-1 research lab strand too

Why it matters:
- this is the cleanest current-era raw-first bundle story
- it tests whether the system can tell the difference between primary raw evidence and replay transport
- it also catches “what do I open first?” routing behavior on the new bundle surface

Regime: `R1 -> R2`
Claim type: `operational` / `hybrid`

Eval prompts:
- “What is the primary object here: raw harness trace or frozen replay bundle? Explain why.”
- “What should I open first if I want to resume this current raw-first bundle work?”
- “Which memory layer should be trusted first in this bundle, and what should it be trusted for?”

## 3) 2026-03-29 -> 2026-04-01
- **Window ID:** `NE13-W3`

What was happening:
- Syke repo work shifts toward runtime stabilization: self-observation/tracing, sandbox/workspace/daemon lifecycle, ask-vs-synthesis separation, memex/cycle bookkeeping, replay-sandbox integration, and docs alignment
- the route map now has to distinguish lab work, runtime work, and deployment-adjacent work

Why it matters:
- this is an architecture-boundary window, not just more events
- it is where the memory system has to route by scope instead of by recency
- it is a good test for “which thread is actually live?” when the stack itself is changing

Regime: `R2`
Claim type: `hybrid`

Eval prompts:
- “Separate the runtime/daemon work from the memory-research work in this window.”
- “Which memory layer should be trusted first here, and for what scope?”
- “What is the canonical restart artifact for this period, and why is it that object rather than a summary dump?”

## 4) 2026-04-02 -> 2026-04-08
- **Window ID:** `NE13-W4`

What was happening:
- late pure-syke continuation
- current-era raw-harness bundle sealing
- NE-1.3 stays raw-first: 6,698 files, 5.17GB, with reconstructed Claude only where raw is missing
- pure-syke itself runs 2026-03-23 -> 2026-04-07, so this is the last stretch of the current-era bundle story

Why it matters:
- this is the best currentness / stale-summary test in the late arc
- it checks whether the system preserves the live map without preserving every burst residue
- it is where replay honesty matters most: derived transport must stay labeled derived

Regime: `R2`
Claim type: `hybrid` / `stress`

Eval prompts:
- “What is live now versus residue from the earlier spike?”
- “Why are frozen replay bundles derived transport rather than the primary object?”
- “Which threads were superseded by later route-map changes, and what replaced them as the best restart point?”

## Practical reading

If I had to prioritize the next NE-1.3 additions, I would do them in this order:
1. `S07` / `S08` burst pair
2. pure-syke bootstrap window
3. runtime-stabilization / replay-sandbox window
4. late currentness / bundle-seal window

That gives the benchmark:
- a cross-harness stress case
- a raw-first replay-alignment case
- an architecture-boundary case
- a late currentness / compaction case

That is enough to make NE-1.3 feel like a real late-period dataset instead of a thin tail on the middle-month slices.
