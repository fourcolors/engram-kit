# NE_1_1_EVAL_CANDIDATES_V1

NE-1.1 window: `2026-01-09 -> 2026-02-08`.

Selection bias: favor defensible early-arc eval windows that have real operational value, not just the later fragmentation-heavy spikes.
Regimes here are the lab shorthand from `BENCHMARK_REGIMES_V2.md`: `R0` = local-memory control, `R1` = fragmentation threshold.
Use the `NE11-W*` IDs below when mapping public eval items back to observer provenance.

## 1) 2026-01-29 -> 2026-01-30 — benchmark/eval audit braid
- **Window ID:** `NE11-W1`
- **What was going on:** multi-agent benchmark/eval review work. Jan 29 is the S02 neighborhood; Jan 30 continues the audit with a more balanced codex/claude-code/opencode mix.
- **Evidence anchors:** `3010` events, `197` sessions, `3` sources across the two-day window. Explicit phrases include “review of claims of persona eval results with the standards of a HN post” and “Here’s a rigorous, HN-standard audit of the report against the actual on-disk artifacts, plus SOTA context.”
- **Why it matters:** this is a clean early `R1` slice: the object is already split across report text, artifacts, and competing context, so provenance matters more than local recall.
- **Likely regime:** `R1`
- **Type:** hybrid
- **Candidate eval prompts:**
  - Which claims in the eval report are directly supported by artifacts, and which are inference?
  - Reconstruct the minimum evidence chain needed to defend the report to a skeptical reviewer.
  - What context should stay out of the public summary because it is background noise rather than evidence?

## 2) 2026-01-31 -> 2026-02-03 — release-eval + architecture hardening
- **Window ID:** `NE11-W2`
- **What was going on:** mostly codex-local continuation work that cross-checked release-eval claims against docs, run data, and code paths. The session language includes “Active eval runs: 0,” “Last completed eval run,” and “I split this into three parallel tracks (docs audit, run-data audit, code-path review).”
- **Evidence anchors:** `10,223` events, `37` sessions, `4` sources. The recurring theme is BEAM event-ordering / release-eval review with findings captured back into local notes.
- **Why it matters:** this is the best early `R0` control candidate: the task is still basically local-state recovery and claim checking, but with enough real review pressure to be useful.
- **Likely regime:** `R0`
- **Type:** operational / hybrid
- **Candidate eval prompts:**
  - What was the last completed eval run, and what is the current live task?
  - Which finding is highest severity, and what artifact supports it?
  - Split the report into claims backed by docs, run data, and code-path review.

## 3) 2026-02-04 -> 2026-02-05 — harness/codepath separation and BEAM docs
- **Window ID:** `NE11-W3`
- **What was going on:** eval-side architecture auditing. One opencode thread asks to “Find evaluation harness code for Persona/PersonaMem/Beam evals and how ingestion differs across them”; another asks how working-memory context is assembled; another searches BEAM benchmark docs/code and expected protocol.
- **Evidence anchors:** `3,354` events, `48` sessions, `3` sources. This window is the cleanest boundary test for benchmark logic vs production logic.
- **Why it matters:** strong early `R1` slice for architecture discrimination. It is practical, but it also exposes whether the benchmark object changes once ingestion and harness boundaries are made explicit.
- **Likely regime:** `R1`
- **Type:** hybrid
- **Candidate eval prompts:**
  - Map eval-only codepaths and their production analogs.
  - Explain how ingestion differs across Persona, PersonaMem, and BEAM.
  - Identify the canonical source of truth for protocol vs implementation.

## 4) 2026-02-06 -> 2026-02-08 — BEAM failure analysis and tool-loop divergence
- **Window ID:** `NE11-W4`
- **What was going on:** sustained opencode-heavy analysis of BEAM failure modes, tool-loop behavior, and the path to stronger results. Prompts include “Figure out what we were working on last session today,” “Analyze why prompt and tool-loop behavior diverge over long sessions,” and “Act as a skeptical reviewer and build a causal model for observed regressions/improvements.”
- **Evidence anchors:** `5,425` events, `66` sessions, `2` sources. This is the stress edge of the NE-1.1 bucket, but still inside it.
- **Why it matters:** this is the best stress-style example in the window: it tests resumption, causal diagnosis, and experiment prioritization without leaving early-arc evidence.
- **Likely regime:** `R1`
- **Type:** stress
- **Candidate eval prompts:**
  - Build a causal model separating prompt failure, tool-loop failure, and data failure.
  - Summarize the current live state from the last session without dragging in stale artifacts.
  - What is the smallest next experiment that would reduce uncertainty the most?

## Short read
The early NE-1.1 bucket is already useful without leaning on the later fragmentation spikes:
- `2026-01-29 -> 2026-01-30`: evidence/provenance audit
- `2026-01-31 -> 2026-02-03`: local restart + release-eval hardening
- `2026-02-04 -> 2026-02-05`: harness boundary / ingestion separation
- `2026-02-06 -> 2026-02-08`: BEAM failure diagnosis / tool-loop stress
