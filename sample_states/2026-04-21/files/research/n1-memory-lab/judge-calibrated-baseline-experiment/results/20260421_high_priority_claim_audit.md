# 2026-04-21 High-Priority Claim Audit

Status: agent-assisted first pass. Not human ground truth.

Rule preserved: `zero` is a valid bounded-packet condition. Store emptiness or
prompt minimalism is only correct when the slice supports it.

Source packet:

- [20260421_calibration_subset_packets.json](./20260421_calibration_subset_packets.json)
- [20260421_calibration_subset_triage.md](./20260421_calibration_subset_triage.md)

## R03

### R03 / pure

- `gpt-5.4`: last work as CLI/onboarding/model-resolution cleanup (`verified`);
  Codex-first + claude-login warning (`verified`); `--yes` path + memory-ID
  prefix lookup (`verified`); synthesis mostly shipped (`inferred`). Failure:
  slightly too confident on synthesis closure. Human-review question: should
  the handoff keep the validation caveat explicit?
- `opus-4.6`: `finalize_memex` + Stop hook rewrite (`verified`); bug1 closed,
  bug2 still pending validation (`verified/inferred`); onboarding/provider
  strategy was latest active work (`verified`); Codex proxy model question
  remained open (`verified`). Failure: underplays later live synthesis/debug
  thread. Human-review question: should the status foreground still-open
  validation work?

### R03 / production

- `gpt-5.4`: onboarding/provider strategy became latest active work
  (`verified`); Codex default + claude-login warning + `SKILL.md` rewrite +
  `--yes` (`verified`); memex short-ID lookup and Codex proxy model were
  adjacent investigations (`verified`); synthesis modernization shipped at
  pipeline level but still validating (`inferred`). Failure: too confident on
  "structurally shipped." Human-review question: should this say "shipped but
  still validating"?
- `opus-4.6`: synthesis modernization centered on `finalize_memex` + Stop hook
  (`verified`); bug1 closed, bug2 fix committed but awaiting validation
  (`verified/inferred`); later docs/model-resolution work was secondary
  (`verified`). Failure: slightly stale on tail-end onboarding/provider shift.
  Human-review question: should later CLI/setup commits be mentioned?

### R03 / zero

- `gpt-5.4`: latest work was onboarding/setup/provider strategy, not synthesis
  (`verified`); Codex first + claude-login warning + `--yes` path (`verified`);
  synthesis was "mostly shipped" with bug1 closed and bug2 open
  (`inferred`, stale); architecture/default-provider cleanup still open
  (`verified`). Failure: understates later real-profile `finalize_memex`
  regression. Human-review question: should "mostly shipped" become "shipped,
  then hit a fresh validation failure"?
- `opus-4.6`: `finalize_memex` rewrite had landed (`contradicted`); HEAD pinned
  to mid-day `b609bcf` (`contradicted`); later onboarding/provider commits
  ignored (`contradicted`); synthesis not actually closed (`verified`).
  Failure: stale mid-day snapshot plus wrong landed-status. Human-review
  question: why does the answer stop before later 18:49Z and 23:24Z state?

## R07

### R07 / production

- `gpt-5.4`: Hephaestus/stash-pop forensic thread + memex routing/pointer
  invention (`verified`); Mar 13 -> Mar 14 arc from research spiral to Observe
  implementation (`verified/inferred`); real-time distribution was next
  priority (`verified`); big counts like 40 threads / 150 sessions / 100+
  subagents are `uncheckable`. Failure: overprecision on counts. Human-review
  question: can we drop counts and keep only verified thread statuses?
- `opus-4.6`: Observe Phase 2 + memory research + tool reduction + tags debate
  arc (`verified`); research -> architecture -> implementation -> validation
  chronology (`verified`); 9 threads broadly backed, but counts uncheckable;
  timing bins approximate (`inferred`). Failure: numerical inflation and
  timeline compression. Human-review question: should timeline keep only
  verified statuses?

### R07 / pure

- `gpt-5.4`: memorix, architecture route, emergent pointer, Hermes gap,
  compaction/handoff threads (`verified`); yesterday/today split into 5 active
  memories + 3 links (`uncheckable`); Observe implementation later active
  thread (`verified/inferred`); UUIDs presented as recovered memories
  (`unsupported`). Failure: fabricated recovery shape and overtrusted IDs.
  Human-review question: should UUIDs be labeled reconstructed handles instead
  of recovered facts?
- `opus-4.6`: two-day timeline and thread set accurate at high level
  (`verified`); research spiral -> implementation arc right (`verified`);
  hour-by-hour specificity and counts uncheckable; invented UUID detail
  unsupported. Failure: overprecision around IDs. Human-review question: can
  invented IDs be stripped while keeping thread map?

### R07 / zero

- `gpt-5.4`: `syke.db` sparse / MEMEX-only framing (`partly uncheckable`);
  "no accessible session traces" and "no recoverable threads" (`contradicted`
  by corpus); future-dated MEMEX references correctly ignored (`verified`);
  answer not restart-capable. Failure: wrong evidence surface and false
  no-traces premise. Human-review question: why not use accessible transcript
  corpus and git anchor?
- `opus-4.6`: major Observe/memory threads present in slice (`verified`);
  answer too sparse / not restart-capable (`inferred`); overly cautious instead
  of restoring live thread (`unsupported`); timeline routing fuzzy
  (`uncheckable`). Failure: generic and under-reconstructed. Human-review
  question: should it surface concrete Observe and real-time-distribution
  threads instead of stopping at sparse memory?

## R08

### R08 / production

- `gpt-5.4`: bootstrap stub / 1 memory / 0 links framing (`unsupported`);
  Claude corpus present and Codex root absent (`verified`); almost no durable
  memory yet (`contradicted` by live Observe traces); asks to scan recent
  Claude sessions next (`inferred`). Failure: confuses storage state with live
  work state. Human-review question: should it switch from "bootstrap" to the
  actual Observe workstream?
- `opus-4.6`: Observe Phase 2 / architecture locked / real-time next
  (`verified`); Thread 12 promoted and Thread 33 active (`verified`);
  empty-durable-store framing wrong for work state (`contradicted`); restart
  value low because live thread ordering missed (`inferred`). Failure:
  misframes Observe as main active thread instead of capture done,
  distribution next. Human-review question: should Observe be reframed as
  closed capture with real-time distribution as live next thread?

### R08 / pure

- `gpt-5.4`: local db empty / no memories / no links (`uncheckable`); Observe
  Phase 2 foundation complete and capture semantics locked (`verified`);
  real-time distribution is killer feature and next priority (`verified`);
  Thread 12/14/15/17 updates correctly captured (`verified`). Failure: missing
  branch/commit/worktree detail needed for restart. Human-review question:
  should concrete branch/commit state be included?
- `opus-4.6`: blank-slate pure-condition framing (`verified` for replay state,
  incomplete for work state); no sessions/traces on disk (`contradicted` by
  slice corpus); Observe capture architecture and next-thread order right
  (`verified`); restart path too generic (`inferred`). Failure: correct about
  local zero-state, wrong about broader work surface. Human-review question:
  can it keep pure-state honesty without claiming no traces?

## R09

### R09 / production

- `gpt-5.4`: Observe vision / adapter protocol / migrations / memory
  architecture / proxy-interoperability are main themes (`verified`);
  events-as-unit and tool-calls-as-events (`verified`); `syke.db` updated to
  reflect map (`unsupported`); UUID-labeled thread map not grounded
  (`contradicted`). Failure: invented UUID threads and unverified db update.
  Human-review question: should map stick to named workstreams only?
- `opus-4.6`: aggregate totals and thread clustering plausible but not fully
  verified (`uncheckable`); per-project counts drift from anchor
  (`contradicted` in places); opencode and Documents coverage incomplete
  (`contradicted`); adapter protocol/path details stale relative to git
  (`inferred`). Failure: numeric drift plus missing project coverage.
  Human-review question: can structure be kept while replacing counts with
  git-anchored totals?

### R09 / pure

- `gpt-5.4`: Observe Phase 2 mostly closed / hardening (`verified/inferred`);
  real-time distribution promoted to next critical thread (`verified`); memory
  retrieval cutoff bug open (`verified`); persisted-map note stale relative to
  live trace (`contradicted`). Failure: stale persisted-map framing.
  Human-review question: should answer separate persisted-db state from
  live-trace-backed thread map?
- `opus-4.6`: Observe Phase 2 complete / hardening (`verified/inferred`);
  real-time distribution as killer feature and next priority (`verified`);
  thread-15 deprioritized and priority order right (`verified`); commit/test
  counts uncheckable and partly contradicted by anchor. Failure: overstates
  counts and misses late corrections. Human-review question: can it keep
  priority order while dropping unsupported counts?

## R14

### R14 / production

- `gpt-5.4`: latest claude-code synthesis run at 2026-03-16 23:54:19
  (`verified`); empty response (`verified`); no `finalize_memex` / stop-hook
  warning (`verified`); saved to `syke.db` + refreshed MEMEX (`unsupported`).
  Failure: right narrow session, but overclaims durable-memory writes and misses
  broader observe-layer live thread. Human-review question: was this right
  latest-session surface, or collapsed mix of adjacent threads?
- `opus-4.6`: observe-layer sandbox/replay (`verified/inferred`); 31 proofs + 2
  sync cycles (`inferred`); Kimi-on-Azure / LiteLLM blocker (`verified`);
  adapter redesign + cost fix (`inferred`). Failure: chronology overpacked and
  specifics embellished. Human-review question: do counts and thread ordering
  match slice exactly?

### R14 / pure

- `gpt-5.4`: observe/sandbox tests green (60; 546/12) (`verified`);
  uncommitted observe/sense refactor exists (`verified/inferred`); real-data
  replay still failing on `finalize_memex` (`verified`); saved into syke.db/MEMEX
  (`unsupported`). Failure: good core recall plus unverified persistence claim.
  Human-review question: is cold-start replay unresolved at cutoff, or only a
  later validation step?
- `opus-4.6`: resumed observe-layer work (`verified`); five pipeline gaps
  (`verified/inferred`); adapter rebuild / `build_llm_fn` / SQLite adapter work
  (`inferred`); Kimi-on-Azure rate-limit / wrong field / retries
  (`verified/inferred`). Failure: mostly right, but file-level detail may be
  embellished. Human-review question: do logs support exact adapter/file claims
  or only broader arc?

### R14 / zero

- `gpt-5.4`: green test state + uncommitted observe/sense work (`verified`);
  cold-start replay not settled / syke connect incomplete (`inferred`); SQLite
  harnesses may need separate handling (`speculative`); new memory + MEMEX
  projection (`unsupported`). Failure: mixes real architecture read with
  unverified durable-memory write. Human-review question: are architectural
  blockers evidence or model inference?
- `opus-4.6`: `ses_307e0d6d` Mar 16 evening -> Mar 17 (`verified`); observe
  tests + sandbox investigation + 5 gaps (`verified/inferred`); 17 successful
  synthesis cycles earlier that day (`verified/inferred`); Kimi-on-Azure failure
  spiral (`verified/inferred`). Failure: slight session blending, mostly
  grounded. Human-review question: are timestamps and 17-cycle claim anchored
  cleanly or stitched from adjacent logs?

## R19

### R19 / production

- `gpt-5.4`: most recent work = LM Studio/Qwen benchmarking (`contradicted`);
  Qwen3.5-35B-A3B main candidate (`contradicted/uncheckable`); Qwen3.5-9B
  downloaded + GUI scan limit (`contradicted/uncheckable`); updated syke.db/MEMEX
  (`unsupported`). Failure: stale thread selection from older LM Studio episode.
  Human-review question: is there any March 21 evidence for LM Studio here, or
  is this wholly older thread?
- `opus-4.6`: no substantive answer; timeout after 600s (`verified`); no claims
  to audit (`uncheckable`). Failure: generation timeout, not reasoning miss.
  Human-review question: should this cell be excluded from comparison because
  Opus never produced content?

### R19 / pure

- `gpt-5.4`: replay/eval sandbox clean slate (`verified`); `bb3706f` cleanup
  commit + UI rename (`verified`); fresh 5-prompt run (`chronology
  contradicted`); `minimal_exclude` prompt (`unsupported`). Failure: right
  thread, wrong ordering. Human-review question: did run happen before cleanup
  commit, and was `minimal_exclude` real?
- `opus-4.6`: fresh boot / empty syke.db (`unsupported`); late-night Mar 21
  architecture session (`contradicted`); Syke Sandbox / replay sandbox eval
  harness arc (`inferred`); misses later tool-stripping/operationalization
  (`contradicted`). Failure: stale-session selection plus embellished
  reconstruction. Human-review question: can cited session IDs/timestamps be
  reconciled with actual March 21 commits?

### R19 / zero

- `gpt-5.4`: background synthesis run at 23:57-23:59 with opencode ingestion
  (`uncheckable`); most recent direct work was Mar 20 interrupted Codex turn
  (`contradicted`); no later 3/21 direct work (`contradicted`). Failure: merges
  older interrupted chat with background automation and misses late-3/21 work.
  Human-review question: why does answer stop at Mar 20 interruption when anchor
  shows later March 21 activity?
- `opus-4.6`: local LLM setup/benchmarking on M2 Max (`verified/inferred`);
  Qwen3.5-35B-A3B + partial Qwen3.5-9B + GUI scan limit (`mostly verified`,
  partial-download overclaim); M5 Max benchmark / bandwidth formula / MLX
  advantage (`verified/inferred`); end time slightly off (`minor
  contradiction`). Failure: small timestamp drift and partial-download
  overstatement, thread itself may be right. Human-review question: does slice
  support this as latest work, or just nearest adjacent LM Studio session?

## Pattern Summary

The high-priority audit surfaces recurring failure modes:

- unsupported durable-memory persistence claims (`syke.db`, MEMEX refreshed);
- stale or wrong thread selection for tip-state asks;
- storage-state confused with work-state;
- invented identifiers or overtrusted UUID/thread handles;
- uncheckable or inflated numeric counts;
- packet insufficiency for replay-design history;
- generation timeout that should be classified separately from answer failure.

These should become explicit failure-attribution categories before any
architecture ranking.

