# Failure Atlas Examples (JCB-060)

Date: 2026-04-21

Status: examples-first artifact compiled before aggregate reporting.

## answer_wrong
- Cell: `R03/pure` (gpt-5.4)
- Example: last work as CLI/onboarding/model-resolution cleanup (`verified`); Codex-first + claude-login warning (`verified`); `--yes` path + memory-ID prefix lookup (`verified`); synthesis mostly shipped (`inferred`). Failure: slightly too confident on synthesis closure. Human-review question: should the handoff keep the validation caveat explicit?

## contradicted_evidence
- Cell: `R03/zero` (opus-4.6)
- Example: `finalize_memex` rewrite had landed (`contradicted`); HEAD pinned to mid-day `b609bcf` (`contradicted`); later onboarding/provider commits ignored (`contradicted`); synthesis not actually closed (`verified`). Failure: stale mid-day snapshot plus wrong landed-status. Human-review question: why does the answer stop before later 18:49Z and 23:24Z state?

## reference_ambiguous
- Cell: `R07/production` (gpt-5.4)
- Example: Hephaestus/stash-pop forensic thread + memex routing/pointer invention (`verified`); Mar 13 -> Mar 14 arc from research spiral to Observe implementation (`verified/inferred`); real-time distribution was next priority (`verified`); big counts like 40 threads / 150 sessions / 100+ subagents are `uncheckable`. Failure: overprecision on counts. Human-review question: can we drop co

## stale_state_selection
- Cell: `R03/pure` (opus-4.6)
- Example: `finalize_memex` + Stop hook rewrite (`verified`); bug1 closed, bug2 still pending validation (`verified/inferred`); onboarding/provider strategy was latest active work (`verified`); Codex proxy model question remained open (`verified`). Failure: underplays later live synthesis/debug thread. Human-review question: should the status foreground still-open validation work?

## unsupported_inference
- Cell: `R07/pure` (gpt-5.4)
- Example: memorix, architecture route, emergent pointer, Hermes gap, compaction/handoff threads (`verified`); yesterday/today split into 5 active memories + 3 links (`uncheckable`); Observe implementation later active thread (`verified/inferred`); UUIDs presented as recovered memories (`unsupported`). Failure: fabricated recovery shape and overtrusted IDs. Human-review question: should U

## wrong_restart_risk
- Cell: `R07/zero` (gpt-5.4)
- Example: `syke.db` sparse / MEMEX-only framing (`partly uncheckable`); "no accessible session traces" and "no recoverable threads" (`contradicted` by corpus); future-dated MEMEX references correctly ignored (`verified`); answer not restart-capable. Failure: wrong evidence surface and false no-traces premise. Human-review question: why not use accessible transcript corpus and git anchor?

This atlas is descriptive and supports examples-before-aggregates workflow.
