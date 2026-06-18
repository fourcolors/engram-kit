# ARCHITECTURE_CASES_V0

This file ties the abstract architecture comparison to concrete real-world cases that already exist in the local corpus or repo evidence.

## Why this exists

Abstract comparison is not enough. We need concrete cases where native memory, provider/plugin memory, and federated continuity would likely behave differently.

## Case A — Same repo, different reading
- **Source:** `docs/MEMEX_IN_USE.md`
- **Observed fact:** same repo, same filesystem, different interpretation depending on whether Syke context routing was present
- **Why it matters:** this is the cleanest concrete case that files alone do not solve the memory problem
- **Likely architecture contrast:**
  - native memory: may stay locally useful but scoped to one harness
  - provider/plugin memory: may inject richer context but still through one harness-local control plane
  - federated continuity: best chance of carrying the broader strategic layer across tools

## Case B — No adapter, no bridge
- **Source:** `docs/MEMEX_IN_USE.md`
- **Observed fact:** OpenCode without Syke adapter had zero context injection and could not see user history
- **Why it matters:** absence makes the continuity layer visible
- **Likely architecture contrast:**
  - native memory: whatever the harness already has locally
  - provider/plugin memory: only helps where installed and surfaced by that harness
  - federated continuity: explicit bridge layer is the object under test

## Case C — Forgotten-plan resumption
- **Source slice:** `2026-02-23`
- **Observed fact:** user returns, asks what happened, then says the system forgot prior data-backed analysis
- **Why it matters:** this is a clean day-to-day failure of resumption and analysis continuity
- **Likely architecture contrast:**
  - native memory: likely answer latest visible state but miss prior justification
  - provider/plugin memory: may retrieve some prior thread but still struggle to reconstruct the active contract
  - federated continuity: should surface both the plan and the fact that it was already evidence-backed

## Case D — Memex evolution / consolidation work
- **Source slice:** `2026-02-25 -> 2026-02-26`
- **Observed fact:** explicit work to extract memex snapshots, create `MEMEX_EVOLUTION.md`, and reduce narrative clutter
- **Why it matters:** this is memory creating practical value through organization and canonicalization, not just answering questions
- **Likely architecture contrast:**
  - native memory: often weak on shared canonical routes across tools
  - provider/plugin memory: can retrieve/summarize but may not create a stable shared map
  - federated continuity: directly optimized for route maintenance and shared map surfaces

## Case E — Hermes enters the trace
- **Source slice:** `2026-02-27 -> 2026-03-01`
- **Observed fact:** Hermes appears late in the corpus alongside opencode, claude-code, manual notes, and github traces
- **Why it matters:** this gives the lab an actual period where provider/plugin-style memory can be compared against the broader continuity object
- **Likely architecture contrast:**
  - native memory: still bounded per harness
  - Hermes/provider memory: stronger plugin/provider story but still harness-centered
  - federated continuity: should be evaluated as the layer binding the harnesses together

## Case F — Cross-harness recall under pressure
- **Source slice:** `2026-03-13 -> 2026-03-14`
- **Observed fact:** multiple harnesses are explicitly asked to remember all the threads from yesterday/today; syke skill is used; volume spikes massively
- **Why it matters:** this is one of the clearest `n=1` continuity-pressure cases in the corpus
- **Likely architecture contrast:**
  - native memory: likely partial and harness-local
  - provider/plugin memory: improved retrieval within one runtime, but may still flatten the multi-harness picture
  - federated continuity: strongest candidate to reconstruct the cross-day, cross-harness graph

## What to do with these cases

Use these cases to drive:
1. slice selection
2. probe selection
3. architecture-comparison experiments
4. practical-value evaluation

The lab should prefer cases where the predicted architecture differences are large enough to falsify weak designs.
