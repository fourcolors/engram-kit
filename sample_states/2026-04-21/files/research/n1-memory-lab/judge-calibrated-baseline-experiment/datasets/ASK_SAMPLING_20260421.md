# Ask Sampling and Coverage - 2026-04-21

Diagnostic pass. Not a rubric revision. Not a judge redesign. This maps what kinds of asks we do not yet have in the 19-probe canonical set and which of those might expose the judge's current blind spots.

## 1. Corpora scanned

| Corpus | File | Observed count |
|---|---|---:|
| All captured asks | `research/n1-memory-lab/psyche_asks_all.json` | 310 |
| Real, non-PI filtered | `research/n1-memory-lab/psyche_asks_real_non_pi.json` | 203 |
| Strict real-ask filter | `research/n1-memory-lab/psyche_asks_real_strict.json` | 180 |
| Canonical 19-probe judge slice | `benchmark_questions.json` (YAML source `NE_1_3_REAL_ASK_EVAL_SET.yaml`, items R01-R19) | 19 |

Discrepancy with prompt framing: the prompt cited corpus sizes of `1559 / 1020 / 905`. The on-disk files carry `total` fields `310 / 203 / 180` and `len(asks)` matches. All distributions below are computed against the observed 310 in `psyche_asks_all.json`. If a larger corpus exists elsewhere, this pass did not reach it.

Classification heuristics (reproducible):
- `count_handles(q)` = dedup set of: capitalised tokens len>=3, path-like tokens, file-extension matches, backticked or quoted substrings, project-vocabulary regex (`syke|memex|litellm|proxy|adapter|observe|opencode|claude-code|codex|hermes|persona|gepa|ace|kimi|azure|gpt|sonnet|opus|haiku|omx|omo|sisyphus|karpathy|pi|ohmyopencode|mcp`), and date/month tokens.
- Target slice: `tip | historical | landscape | both | unclassified`, keyword-based.
- Verifiability: `hard_only | semantic_only | mixed | neither` against the two regex families noted in the inline script.
- Retrieval character: `search-like | reconstruction-like | mixed`, handle-count plus synthesis-verb heuristics.

Scripts inlined in this pass (ephemeral) operated on the three JSON files and the YAML eval set.

## 2. Coverage of the current 19-probe set

Cross-checked against `datasets/probe_metadata.json` (authoritative for R01-R19) and `ASK_DEMAND_TAXONOMY_NE13_20260418.md` (authoritative for demand tags).

### Target slice (R01-R19)

| slice | n |
|---|---:|
| tip | 6 (R01, R08, R12, R14, R15, R19) |
| historical | 6 (R02, R04, R07, R11, R13, R18) |
| landscape | 5 (R05, R09, R10, R16, R17) |
| both | 2 (R03, R06) |

Source: `probe_metadata.json.summary.target_slice_counts`.

### Criterion-referenceability (R01-R19)

| level | n |
|---|---:|
| high | 6 |
| medium | 9 |
| low | 4 |

### Retrieval character (R01-R19)

| character | n |
|---|---:|
| search-like | 13 |
| reconstruction-like | 6 |

### Handle density (R01-R19, computed here)

| bucket | n | probes |
|---|---:|---|
| 0 handles | 7 | R01, R03, R07, R08, R09, R14, R19 |
| 1 handle | 7 | R04, R06, R10, R13, R15, R17, R18 |
| 2 handles | 1 | R12 |
| 3-5 | 2 | R05, R11 |
| 6+ | 2 | R02, R16 |

### Handle density (whole 310-corpus)

| bucket | n | share |
|---|---:|---:|
| 0 | 55 | 17.7% |
| 1 | 45 | 14.5% |
| 2 | 45 | 14.5% |
| 3-5 | 113 | 36.5% |
| 6+ | 52 | 16.8% |

The 19-probe set is skewed low-handle (73.7% in 0-1 buckets) versus the corpus (32.2%). High-handle, artifact-rich asks are materially under-represented.

### Demand-tag load in R01-R19 (from `ASK_DEMAND_TAXONOMY_NE13_20260418.md`)

Missing entirely from R01-R19 (appear at R20+): `META_HANDOFF`, `CONFIG_CHECK`, `GAP_ANALYSIS`, `DOC_SYNTH`, `PROVENANCE_AUDIT`.

Counts inside R01-R19: CONCEPT_RECALL 8, TIME_WINDOW 5, LAST_THREAD 4, COMMITTED_STATE 4, NEXT_STEPS 4, QUANT 4, STATE_NOW 3, THREAD_MAP 3, DECISION 3, DELTA 3, CROSS_SOURCE 3, CHANGE_HISTORY 1.

## 3. Gaps

### Corpus-wide R08-type (zero-handle, under-specified, orientation-only)

Detection regex: orientation verbs (`where are we | whats up | status | current state | left off | pick up | get a sense | what happened last | what am i working on`) + word_count <= 18 + handle_count <= 2.

Result: 12 asks in the 310-corpus, of which R01, R08, R09, R14, R19 already cover 5 of the shape. The remaining 7 novel R08-shape candidates are in section 5.

### Pure hard-verifiable (every primitive is time/artifact/commit checkable)

Corpus-wide `hard_only` (heuristic): 117 / 310 (37.7%). Five representative quotes:
1. `[2026-03-12T07:29:02]` what did we push to Persona today, what are the SOTA benchmark results?
2. `[2026-03-22T07:56:45]` what happened on March 21 2026? what runs did we do, how many synthesis cycles, what was the activity that caused 72 million input tokens?
3. `[2026-03-24T19:35:07]` what did opencode change in litellm_proxy.py today? specifically the patches for thinking, _azure_translate_patched, _azure_process_event_patched flags, and the reordering of patches before litellm imports. check the opencode events from the last 3 hours
4. `[2026-04-07T02:20:43]` Read MEMEX.md. What are my top 3 active projects right now? Be brief.
5. `[2026-04-14T22:54:14]` Codex reports the 15-day zero replay is over. Confirm: did the 15-day zero replay complete? Full cycle count, final artifact location, any errors or interrupts, and what is the current state of the 19-item benchmark smoke?

### Pure semantic (no primitive hard-verifiable)

Heuristic `semantic_only`: 11 / 310. Five representatives:
1. `[2026-03-28T15:00:12]` what is the omocon talk about? what's the current state of the deck, any recent feedback or changes?
2. `[2026-04-07T03:25:01]` what am I working on?
3. `[2026-04-07T03:25:02]` what am I working on right now in syke?
4. `[2026-04-07T07:42:20]` what should I be working on right now?
5. `[2026-04-10T00:19:46]` Is there a connection between the February 23 forgotten-plan episode and the March 13-14 cross-harness work?

### Partially verifiable (project's actual frame)

The heuristic's `mixed + neither + classified-hard-with-semantic` coverage is most of the corpus. Five representatives:
1. `[2026-03-15T01:32:40]` What projects is the user actively working on? Which ones are old/inactive/abandoned? Specifically give me the status of: syke, syke-deli, syke-memory-research, syke-repo, vibes-cli, hermes-vibes-lab, lifeOS, vak, ...
2. `[2026-03-22T08:41:57]` what is the history of the reasoning_content / thinking traces problem with LiteLLM proxy and Kimi/Azure? what patches did we make, what bugs did we file, what was the status?
3. `[2026-03-31T18:29:32]` what's the current state of the repo and research? what are my latest instructions and open loops? what branch am I on and what's dirty?
4. `[2026-04-07T02:11:09]` Read MEMEX.md in the workspace. What are my active projects and what am I working on?
5. `[2026-04-14T22:48:30]` what is the current state of pi_ask.py rework and what is the uncommitted work trying to solve? Also confirm: is the 19-item Azure-mini benchmark smoke still running, did the race fix hold, and what is the latest on MEMEX projection leak?

### Headline gaps relative to the 19-probe set

1. **Zero DOC_SYNTH coverage** (0 / 19). The `Read X, then answer Y` shape (section 4 candidates 12, 22, 23, 39 of the larger YAML) has ~15 corpus hits.
2. **Zero GAP_ANALYSIS / PATTERN-DISCOVERY coverage**. The `what is still missing / what patterns have I not seen / what did I reverse` shape has ~6 corpus hits and is highly recurrent in late-window asks.
3. **Zero CONFIG_CHECK / COMMITTED_STATE_FIDELITY coverage**. The `what branch am I on / is omo updated / what does the config actually say now` shape has ~13 corpus hits.
4. **Zero PROVENANCE_AUDIT coverage**. `How did you know / what did you read / trace the chain / show the route across tools` has ~3 sharp hits plus many implicit demands (April 9-10 Pi asks).
5. **High-handle artifact-rich asks under-represented**. Only 2 / 19 probes carry 6+ handles, vs 16.8% of corpus (52 / 310).
6. **Sub-day / sub-hour temporal windows under-represented**. R04 uses a whole day; no probe uses a rolling-hour window, yet this shape is common (`last 3 hours`, `last hour or two`).
7. **Short under-specified paraphrases of R01/R08/R09 are thin**. Only R08 truly stands alone at <= 6 words. The ultra-terse forms (`what's going on?`, `what am I working on?`) are absent.

## 4. 30 candidate asks to extend the set

All pulled verbatim from `psyche_asks_all.json`. Structured data in `ask_sampling_20260421.json`.

| # | ts | ask (verbatim, truncated for table) | axis gap filled | verifiability | primitives | paraphrase |
|---:|---|---|---|---|---|---|
| 1 | 2026-03-22T18:15 | where were we? what was the last session working on? | under_specification | partial | last-session close; session top-line | R08 |
| 2 | 2026-04-07T03:23 | what's going on? | under_specification | semantic | tip-state; active-thread list | R08 |
| 3 | 2026-04-07T03:25 | what am I working on? | handle_density | semantic | active-project list; recent focus | R08 |
| 4 | 2026-04-07T03:25 | what am I working on right now in syke? | handle_density | semantic | scoped active-project; recent commits | R01 |
| 5 | 2026-04-07T07:42 | what should I be working on right now? | under_specification | semantic | open-loops; priority signals | new |
| 6 | 2026-04-08T07:02 | what are my active threads right now? | target_slice | partial | thread-board snapshot | R09 |
| 7 | 2026-04-07T03:23 | what was my last claude-code session about? | target_slice | partial | harness-scoped last-session | R14 |
| 8 | 2026-04-07T06:07 | what was the last thing recorded about the april 6-7 session? what open loops were flagged? | criterion_referenceability | partial | date-bounded session; open-loop tags | new |
| 9 | 2026-03-22T07:56 | what happened on March 21 2026? ...how many synthesis cycles, what was the activity that caused 72 million input tokens? | criterion_referenceability | hard | date; run-count; cycle-count; token metric | new |
| 10 | 2026-03-23T07:38 | What do the logs show about actual syke synthesis usage? Token counts, costs, duration, how many turns per cycle, prompt sizes... | criterion_referenceability | hard | log metrics | new |
| 11 | 2026-03-24T07:37 | Give me the full list of all architectural loops in syke... closed/open/broken. Check events DB, memex, everything. | criterion_referenceability | partial | loop-list seed; per-loop status | R05 |
| 12 | 2026-04-07T02:21 | Read the adapter markdown at ~/.syke/data/saxenauts/adapters/claude-code/adapter.md. Then check what claude-code data exists at the paths it describes. How many sessions do I have? | retrieval_vs_reconstruction | hard | file read; session count | new |
| 13 | 2026-03-31T18:29 | what's the current state of the repo and research? what are my latest instructions and open loops? what branch am I on and what's dirty? | criterion_referenceability | partial | git branch; dirty; open-loops; instruction recall | R01 |
| 14 | 2026-04-14T22:48 | what is the current state of pi_ask.py rework and what is the uncommitted work trying to solve? Also confirm: is the 19-item Azure-mini benchmark smoke still running... | criterion_referenceability | partial | uncommitted diff; running-process; race fix commit; leak metric | new |
| 15 | 2026-04-14T22:54 | Codex reports the 15-day zero replay is over. Confirm: did the 15-day zero replay complete? Full cycle count, final artifact location... | criterion_referenceability | hard | run-flag; cycle count; artifact path; error log; leak count | new |
| 16 | 2026-04-12T11:10 | What is the latest OMX feedback or conversation? Any recent omx sessions, artifacts, or plans? | target_slice | partial | latest omx session; artifact list | new |
| 17 | 2026-04-13T22:10 | What new docs or changes did codex create in the last hour or two? Check _internal/analysis/... | criterion_referenceability | partial | file mtime window; new-file list; latest thread | new |
| 18 | 2026-04-08T17:44 | list every open loop, unfinished task, known bug, next step, and unresolved question across all routes — be exhaustive | retrieval_vs_reconstruction | partial | enumeration across categories | R05 |
| 19 | 2026-04-09T08:39 | What have we been able to do with the NE-1 / N=1 benchmark thesis so far... what is left to finish? | retrieval_vs_reconstruction | partial | delivered artifacts; bundle list; remaining gaps | new |
| 20 | 2026-04-10T00:20 | On February 23, was there a case where current state contradicted what had been established earlier? | target_slice | partial | date slice; contradiction detection | new |
| 21 | 2026-04-06T22:51 | Look at my work over the past month across all harnesses... Are there decisions I made and then reversed? Threads I started and abandoned? | retrieval_vs_reconstruction | semantic | reversal pairs; abandoned threads; recurring themes | new |
| 22 | 2026-04-07T02:11 | Read MEMEX.md in the workspace. What are my active projects and what am I working on? | retrieval_vs_reconstruction | partial | file parse; alignment with slice | R01 |
| 23 | 2026-04-07T02:20 | Read MEMEX.md. What are my top 3 active projects right now? Be brief. | criterion_referenceability | hard | top-3 exact match; brevity | R01 |
| 24 | 2026-03-21T05:04 | what is the history of hacks and patches in this codebase? ...LiteLLM proxy, Kimi middleware, technical debt... | target_slice | partial | patch timeline; debt-tag list | R13 |
| 25 | 2026-03-24T19:35 | what did opencode change in litellm_proxy.py today? ...check the opencode events from the last 3 hours | criterion_referenceability | hard | scoped diff; named symbols; 3h event window | new |
| 26 | 2026-04-06T22:51 | Did I decide to use Docker for Syke's sandboxing or not? ...I want to know if there was a decision and whether it changed over time. | retrieval_vs_reconstruction | partial | decision events; change timeline; cross-harness | new |
| 27 | 2026-03-31T18:33 | what are the user's exact latest instructions and perspective they just gave in codex? ...Include their exact quotes and instructions verbatim where possible. | criterion_referenceability | hard | latest codex-user messages; verbatim fidelity | new |
| 28 | 2026-04-06T23:12 | Using adapters at ~/.syke/adapters/, trace the 'sandbox design' thread across ALL harnesses. Show me the chain... | target_slice | partial | topic-scoped session list; cross-harness timestamps; link edges | R07 |
| 29 | 2026-04-06T22:51 | What was I doing on April 4th, 2026? Check all harnesses... Reconstruct the day — what happened, in what order, across which tools. | target_slice | hard | date slice; per-harness ordered events | R04 |
| 30 | 2026-04-10T00:19 | Is there a connection between the February 23 forgotten-plan episode and the March 13-14 cross-harness work? | retrieval_vs_reconstruction | semantic | distant-date retrieval; semantic-linkage claim | new |
| 31 | 2026-04-13T16:42 | Debug the current mismatch: why do some NE-1.3 evals expect cross-harness evidence at dates where the slice is Claude-only? | retrieval_vs_reconstruction | partial | bundle history; probe creation; dataset change log; bug-vs-design | new |
| 32 | 2026-04-09T23:29 | What papers and research have we studied on LLM-as-judge design, eval scoring, RSI evaluation... | handle_density | partial | paper list; arxiv refs; framework crosscheck | new |
| 33 | 2026-03-28T15:21 | we compiled a huge list of memory systems and competitors... find that full list from recent sessions. it was for the omocon talk landscape. | retrieval_vs_reconstruction | partial | artifact recall; session window; entry count | new |

Landed: 33 candidates (target was 30). Candidates were kept rather than culled because several map to distinct task-shape categories (DOC_SYNTH vs CONFIG_CHECK vs CROSS_SURFACE) that the current 19-probe set does not test at all.

## 5. R08-type representatives (the reconstruction-only class)

Ten quoted asks from the 310-corpus matching R08-type (orientation-only, zero- or low-handle, under-specified):

1. `[2026-03-21T04:33:41]` what happened last — recent sessions, last activity, what was I working on
2. `[2026-03-21T04:34:08]` what happened last? what was I working on most recently?
3. `[2026-03-22T18:15:29]` where were we? what was the last session working on?
4. `[2026-03-29T09:10:04]` what's my current status — what am I working on, what's recent, anything broken?
5. `[2026-04-07T03:23:40]` what's going on?
6. `[2026-04-07T03:23:42]` what was my last claude-code session about?
7. `[2026-04-07T03:25:01]` what am I working on?
8. `[2026-04-07T03:25:02]` what am I working on right now in syke?
9. `[2026-04-07T07:42:20]` what should I be working on right now?
10. `[2026-04-08T07:02:57]` what are my active threads right now?

Of these, only candidate 3 (2026-03-22) and candidate 10 (2026-04-08) are strictly isomorphic to R08's `okay where are we now`. The others extend into narrower demands (which harness / which time / which status). All ten are well-formed eval fodder for paraphrase robustness and for testing whether zero-handle reconstruction generalises.

## 6. What the corpus tells us about new judge categories

The 19-probe set cannot test the following demand families because they are absent or vestigial (n=0 to n<=1):

1. **DOC_SYNTH-plus-reconciliation**. Asks of the form `Read FILE.md, then answer with slice-grounded claims`. Candidates 12, 22, 23 in this sampling. Reconciling claims to (a) the file and (b) the slice is a two-source fidelity check the current 19-probe probes never exercise. Paper analogue: grounded-summarisation evals (RAGTruth, FActScore).

2. **CONFIG_CHECK / COMMITTED_STATE_FIDELITY**. Asks of the form `what branch am I on, what's dirty, is X up-to-date, what does the config actually say right now`. Candidates 13, 14, 15, 25. These demand a fidelity check against git/filesystem/process-list truth, not only against the transcript slice. Distinct failure mode: stale-narrative drift (agent repeats what it was told a week ago instead of checking the repo).

3. **GAP_ANALYSIS / PATTERN_DISCOVERY**. Asks of the form `what is still missing`, `what patterns am I not seeing`, `what decisions did I reverse`. Candidates 19, 21, 31. Demands an analytic layer on top of reconstruction. Current `continuity.continuation_value` sub-axis drifts into this territory without being scored for it.

4. **PROVENANCE_AUDIT / TRACE_THE_CHAIN**. Asks of the form `show the chain, how did this idea move between tools, how did you know`. Candidates 10, 15, 27, 28, 32. Forces the agent to produce a provenance path rather than a conclusion. Cross-harness version especially valuable: R07 asks for timeline, candidate 28 asks for causal edges — different outputs, different failure modes.

5. **VERBATIM_QUOTATION / INSTRUCTION_FIDELITY**. Candidate 27 asks for exact user words, no summarisation. This inverts the usual paraphrase-tolerance expectation and tests a fidelity property orthogonal to reconstruction. META_HANDOFF adjacent.

Two smaller categories also surface but are narrower:
- **FACT_CHECK_CLAIM** (candidate 15): user asserts something, agent confirms/refutes from slice + artifact truth. Flips the normal retrieval direction.
- **LONG_RANGE_CAUSAL_LINK** (candidate 30): connect two non-adjacent time windows. Tests retrieval over non-contiguous slices, which the current 19 do not.

Whether any of these become headline benchmark categories is a downstream decision. What the corpus shows is that the 19-probe set measures one narrow slice of the ask surface (tip-state + CONCEPT_RECALL + TIME_WINDOW), and that at least five demand families with consistent corpus presence are not being probed at all.
