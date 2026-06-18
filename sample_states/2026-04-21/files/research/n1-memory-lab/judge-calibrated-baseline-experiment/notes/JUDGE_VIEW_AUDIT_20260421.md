# What the Judge Actually Sees — Per-Probe Audit

Run universe sampled: `ne13-real-15d-gpt54-final-20260420T071500Z` and
`ne13-real-15d-opus46-final-20260420T071500Z` (the two "own-judge" canonical
runs), with spot checks of the two cross runs
(`ne13-real-15d-gpt54ask-opusjudge-*`, `ne13-real-15d-opusask-gpt54judge-*`)
and one fresh Apr 21 rep (`ne13-15d-gpt54heavy-intrarater-rep1-*`). Coverage
per judge = 19 probes × 3 conditions (production / pure / zero) = 57 cells,
i.e. 114 judge rollouts across the two primary judges. All numbers below come
from real files on disk, not from re-execution.

## 1. Packet structure, in code and in practice

`benchmark_runner._build_real_ask_packet` (lines 689–728) declares exactly five
top-level keys:

```
packet = {
  "probe":        { probe_id, question, family, reference_dt,
                    reference_ts_local, reference_cutoff_iso,
                    source_surface, source_ref },
  "answer":       { text, metadata },
  "raw_context":  { slice_dir, slice_summary, replay_state },
  "local_git_set":{ available, path },
  "judge_brief":  { object, useful_means, partial_means, fail_means },
}
```

Checked against `evidence/production/R01/packet.json` and spot-checked against
`R19`, `opus-final R01`, both cross runs, and `heavy-rep1 R01`: every packet on
disk has exactly those five keys, in that order. No drift.

Inside each block:
- `probe`. `reference_ts_local` is consistently empty string; the judge only
  ever sees `reference_cutoff_iso` (e.g. `2026-03-08T23:59:59-07:00`) as the
  time anchor. `source_ref` points at a user-side transcript path and line
  (e.g. `/Users/saxenauts/.claude/transcripts/ses_334d16f7d…jsonl#L4`). This is
  a live filesystem path to the user's host, not a slice-relative path; on R01
  gpt-judge, the judge noticed and tried to `ls`/`wc -l` that path directly
  (tool call [4]).
- `answer.metadata`. Backend/provider/model/cost/latency/token counts and
  `tool_calls` / `num_turns`. This is the only place model identity is
  surfaced to the judge; the judge-brief says "do not score efficiency" but
  the metadata is still present. E.g. R01 production (gpt5.4 agent) has
  `backend=pi, provider=openai-codex, model=gpt-5.4`.
- `raw_context.slice_summary`. `cycle`, `bundle` (always `ne-1.3`), and per
  source counts: `jsonl_files`, `jsonl_lines`, `db_rows`. Codex/opencode
  frequently report zero counts — the slice itself *does* contain codex and
  opencode files for later probes, but `slice_summary.sources.codex` is
  reported zero even when `slice/harnesses/codex/…` has content. See §2.
- `raw_context.replay_state`. Just three fields: `condition`, `ask_mode`,
  `memex_chars`. `memex_chars` is the char count of the MEMEX the agent *was
  given*, which means the judge is told how much memory the agent had.
- `local_git_set`. Boolean `available` + `path` pointing at the judge
  workspace's own copy (e.g. `/var/folders/.../syke-judge-x6pgv4k9/local_git_anchor.json`).
  On canonical runs this is always `available: true`.
- `judge_brief`. Identical object on every probe in every run (confirmed with
  `p['judge_brief']==p19['judge_brief']` across R01/R19). It is not a
  probe-scoped rubric; it is a constant boilerplate embedded in `_build_judge_brief`
  (lines 666–686).

Nothing in the packet tells the judge the *probe's intended target slice*,
probe type, ambiguity notes, or expected evidence surfaces — all of that lives
in `datasets/probe_metadata.json` and is *not* surfaced to the judge.

## 2. Slice accumulation question

**Slices are strictly cumulative by wall-clock cutoff** (monotonically
non-decreasing), and **shared verbatim across probes that share a
`reference_dt`** (identical symlink target). Concretely:

| probe | reference_dt | slice files | slice bytes |
|-------|--------------|-------------|-------------|
| R01, R02 | 2026-03-08 | 150 | 39M |
| R03 | 2026-03-11 | 406 | 85M |
| R04 | 2026-03-12 | 529 | 107M |
| R05, R06 | 2026-03-13 | 801 | 162M |
| R07–R10 | 2026-03-14 | 2,995 | 279M |
| R11–R13 | 2026-03-15 | 3,144 | 331M |
| R14, R15 | 2026-03-16 | 3,368 | 355M |
| R16 | 2026-03-19 | 3,664 | 404M |
| R17 | 2026-03-20 | 3,759 | 424M |
| R18, R19 | 2026-03-21 | 4,245 | 474M |

`evidence/production/R*/slice` are symlinks into
`/Users/saxenauts/.syke-lab/<run>/slices/NE-1.3__R<n>/`. Each new probe's
slice strictly contains the union of whatever the previous cutoff had plus
what was added up to the new cutoff. A probe at 2026-03-21 is looking at the
full 4,245-file union; a probe at 2026-03-08 sees 150 files. The judge
therefore has a *bigger haystack* the later the probe, but this is a property
of the slice, not a carry-over of prior judge state.

One packet-level weirdness: `slice_summary.sources` for R01 reports only
`claude-code`: 147 files / 9,589 lines (codex and opencode report zero), which
matches what's on disk for 2026-03-08 (no codex activity yet). But for later
probes, codex and opencode directories appear under the slice while
`slice_summary` in the packet still under-reports. E.g. R07 shows 2,992 files
in the summary but disk has 2,995 files. Small (±3), but the summary is not
a perfect index — useful to know the judge can't trust it as a file count.

**The judge's own context is NOT cumulative.** Every probe is a fresh
runtime: `runtime.runtime_reused == False` for all 19 R01–R19 entries in the
gpt judge production trace, and each probe has a unique
`runtime_status.workspace` (e.g. `production_R01__52e268b0/workspace` vs
`production_R02__eca36735/workspace`). The judge transcript starts from scratch
every probe. So "the agent for the judge at each moment keeps increasing" is
**false at the conversation level**, but **true at the slice-evidence level**.
The user's mental model is half right.

## 3. Per-probe snapshot, 19 entries

Format: Q (first 100 chars) · cutoff · packet bytes (prod/pure/zero) ·
slice_summary (files/lines/sources) · answer lengths (prod/pure/zero) ·
gpt-judge tool-call totals (prod/pure/zero) · opus-judge totals · notes.

### R01 — "what's the current state of things?"
- cutoff: `2026-03-08T23:59:59-07:00`
- packet bytes: 5,344 / 5,859 / 8,039
- slice: 147 jsonl / 9,589 lines, claude-code only
- answers: prod 2,636 / pure 3,163 / zero 5,215 chars
- gpt-judge: 14 / 19 / 21 calls. opus-judge: 22 / 39 / 13
- judge spent most of its budget re-checking `local_git_anchor.json` (read 4x)
  and trying to read `/Users/saxenauts/.claude/transcripts/…jsonl` directly
  from the host because `source_ref` pointed there.

### R02 — "What did we work on yesterday March 7 and today March 8? List everything..."
- cutoff: `2026-03-08T23:59:59-07:00`
- packet bytes: 14,437 / 20,360 / 18,867 — **the answer itself is big**
  (prod 11,201 / pure 16,890 / zero 15,342 chars), so the packet balloons.
- slice: same 147 / 9,589 as R01
- gpt-judge: 20 / 7 / 14. opus-judge: 38 / 27 / 31
- The exhaustive "list everything" framing → packet dominated by the answer
  text. Judge verifies against local git anchor + transcript.

### R03 — "what was I last working on and what's the current status of synthesis modernization?"
- cutoff: `2026-03-11T23:59:59-07:00`
- packet bytes: 4,507 / 5,861 / 4,208
- slice: 403 files / 21,733 lines (codex now appears)
- answers: 1,784 / 3,044 / 1,506
- gpt-judge: 15 / 14 / 25. opus-judge: 25 / 40 / 22
- First probe where the slice has codex content. Judge has to decide
  "synthesis" claims against messy cross-source evidence.

### R04 — "give me my work log today PST entire day"
- cutoff: `2026-03-12T23:59:59-07:00`
- packet bytes: 10,431 / 13,049 / 10,796
- slice: 526 / 27,804
- answers: 7,493 / 9,763 / 7,706
- gpt-judge: 19 / 28 / 29. opus-judge: 26 / 39 / 28
- Day-window probe. Heavy tool use on both sides — timestamp filtering.

### R05 — "what are all my current open threads, priorities... (ACE, GEPA, sleep/dream, filesystem)..."
- cutoff: `2026-03-13T23:59:59-07:00`
- packet: 10,438 / 13,220 / 11,055
- slice: 798 / 36,251
- answers: 7,306 / 9,926 / 7,868
- gpt-judge: 14 / 21 / 19. opus-judge: 23 / 26 / 38
- Landscape probe — many named concepts the judge greps for by name.

### R06 — "what was I last working on in syke? what was left to do?"
- cutoff: `2026-03-13T23:59:59-07:00` (same slice as R05)
- packet: 9,454 / 7,117 / 8,657
- answers: 6,488 / 4,235 / 5,730
- gpt-judge: 23 / 28 / 16. opus-judge: 48 / 25 / 34
- opus-judge production was a high-tool-call outlier (48). Same slice as R05
  but different question framing leads to different verification paths.

### R07 — "remember all the threads we made yesterday and map the timeline"
- cutoff: `2026-03-14T23:59:59-07:00`
- packet: 9,002 / 7,417 / 4,272
- slice: 2,992 / 72,995 (first big jump: 3.7× files vs R06)
- answers: 6,134 / 4,525 / 1,638
- gpt-judge: 24 / 16 / 14. opus-judge: 40 / 25 / 35
- Two-day timeline recall.

### R08 — "okay where are we now"
- cutoff: `2026-03-14T23:59:59-07:00` (same slice as R07)
- packet: 3,504 / 6,517 / 3,891 — smallest packet so far
- answers: 967 / 3,866 / 1,340 — prod answer was terse (967 chars)
- gpt-judge: 15 / 19 / 22 (twice emitted verdict, count=2 in prod). opus-judge: 28 / 18 / 15
- Minimal-ask probe. Judge still has to work the full 2,995-file slice.

### R09 — "what is the updated thread map now"
- cutoff: `2026-03-14T23:59:59-07:00`
- packet: 4,185 / 7,330 / 5,795
- answers: 1,612 / 4,500 / 3,161
- gpt-judge: 19 / 15 / 16. opus-judge: 26 / 19 / 10
- Near-duplicate question framing vs R08; judge workload similar.

### R10 — "What was the memory tools landscape study? ... memorix, claude-mem..."
- cutoff: `2026-03-14T23:59:59-07:00`
- packet: 7,803 / 15,599 / 10,025
- answers: 4,743 / 12,319 / 6,885
- gpt-judge: 15 / 30 / 20. opus-judge: 40 / 14 / 16
- Concept-recall probe with named external tools. Judge greps for literal
  names.

### R11 — "What is the full vision for Observe? ... hook listener, federation..."
- cutoff: `2026-03-15T23:59:59-07:00`
- packet: 16,877 / 15,436 / 14,671
- slice: 3,141 / 83,189
- answers: 13,350 / 12,006 / 11,254 (largest packets in run so far)
- gpt-judge: 21 / 20 / 37. opus-judge: 32 / 29 / 37
- Vision probe — long answer, judge spends time verifying many named sub-ideas.

### R12 — "what specific next steps were discussed for Observe after Phase 2?"
- cutoff: `2026-03-15T23:59:59-07:00`
- packet: 4,004 / 4,323 / 4,055 (very tight)
- answers: 1,408 / 1,714 / 1,445
- gpt-judge: 27 / 21 / 13. opus-judge: 36 / 40 / 36
- Small answer but opus judge still ran ~36 tool calls — the judge searches
  the whole slice for the phrase "next step" regardless of answer size.

### R13 — "what was the evolution of the adapter-as-compiler concept?"
- cutoff: `2026-03-15T23:59:59-07:00`
- packet: 5,560 / 6,267 / 5,781
- answers: 2,856 / 3,485 / 3,034
- gpt-judge: 18 / 24 / 17. opus-judge: 18 / 31 / 31
- Concept-evolution probe. Low variance across conditions.

### R14 — "check it what happened in the last session don't forget it please"
- cutoff: `2026-03-16T23:59:59-07:00`
- slice: 3,365 / 91,363
- packet: 3,152 / 4,419 / 3,946 (smallest prod packet)
- answers: 589 / 1,826 / 1,336
- gpt-judge: 20 / 21 / 22. opus-judge: 17 / 45 / 34
- Tiny-answer probe in prod (589 chars). Opus-judge on pure escalated to 45
  calls.

### R15 — "can we get back to the previous thread of running our tests for observe layer..."
- cutoff: `2026-03-16T23:59:59-07:00`
- packet: 4,790 / 5,610 / 4,756
- answers: 2,084 / 2,840 / 2,001
- gpt-judge: 23 / 18 / 21. opus-judge: 17 / 30 / 23
- Specific thread-recovery probe.

### R16 — "what did I work on yesterday March 18... architecture, skill files, tool reduction..."
- cutoff: `2026-03-19T23:59:59-07:00`
- slice: 3,661 / 110,097
- packet: 8,707 / 6,747 / 6,638
- answers: 5,775 / 3,836 / 3,737
- gpt-judge: 41 / 18 / 12 — **gpt-judge prod blew up to 41 calls** (max in
  gpt-judge set). opus-judge: 35 / 58 / 44 — opus-pure hit 58 (the max across
  the whole audit).
- Yesterday-window probe with many named topics — judge greps for each.

### R17 — "What happened in the last one week? ... all platforms, all sessions"
- cutoff: `2026-03-20T23:59:59-07:00`
- slice: 3,756 / 116,700
- packet: 17,653 / 25,223 / 17,435 — **largest packets in the run**
- answers: 14,417 / 21,529 / 14,208
- gpt-judge: 26 / 25 / 27. opus-judge: 37 / 38 / 39
- Week-window exhaustive probe. Packets dominated by giant answers.

### R18 — "what was the design for the syke sandbox and replay harness?"
- cutoff: `2026-03-21T23:59:59-07:00`
- slice: 4,242 / 131,966 (largest)
- packet: 10,746 / 7,359 / 10,583
- answers: 7,631 / 4,442 / 7,383
- gpt-judge: 22 / 18 / 28. opus-judge: 33 / 37 / 38
- Meta-probe (the design of *this* benchmark). Judge's slice contains the
  lab's own conversations.

### R19 — "what happened last? what was I working on most recently?"
- cutoff: `2026-03-21T23:59:59-07:00`
- packet: 3,871 / 3,847 / 4,431
- answers: 1,178 / 1,150 / 1,733 — opus prod was **33 chars** (timeout) and
  got "fail" verdict. GPT all completed.
- gpt-judge: 21 / 23 / 23. opus-judge: 3 / 36 / 30 — the opus production R19
  case is the only 3-call trace: judge read packet, `ls`d the slice, declared
  "No answer was produced due to timeout. There are zero factual claims to
  evaluate." Rational short-circuit behavior.

## 4. Noise in the judge's input

Concrete items I'd flag as probably-not-load-bearing for scoring:

1. **`judge_brief` is 100% boilerplate.** Identical across all 19 probes and
   all 5 run configs sampled. It describes what "useful / partial / fail"
   mean in abstract English. The judge's system prompt (transcript[0])
   already restates the rubric more concretely with the schema, so the
   `judge_brief` block mostly duplicates purpose without adding per-probe
   criteria.

2. **`answer.metadata` leaks agent identity and cost.** `provider=openai-codex`,
   `model=gpt-5.4`, `cost_usd=0.02691`, `duration_ms=143358`, `num_turns=13`.
   The judge is told not to score efficiency, yet sees efficiency metrics
   *and* the identity of the model being judged. This is at minimum a
   contamination risk for blind-judge setups; whether it matters empirically
   is a separate question I'm not scoring here.

3. **Redundant slice reporting.** `raw_context.slice_dir` gives an absolute
   path to the *source* slice in `~/.syke-lab/...`; `raw_context.slice_summary`
   restates what is in `slice/slice_meta.json` which the judge can also read
   directly; and the judge workspace symlinks `slice/` anyway. Three surfaces
   pointing at the same evidence.

4. **`source_ref` is a host path.** E.g. R01 has
   `/Users/saxenauts/.claude/transcripts/ses_334d16f7dffepp0fpzQhpVSxN4.jsonl#L4`.
   In practice the judge for R01 tried to `ls` that path on the host
   (call [4]) — which *does* succeed because the lab runs on the user's own
   machine, but would be an authority-leak in any setting where the judge
   isn't supposed to trust the host FS.

5. **`raw_context.replay_state.memex_chars`** tells the judge how much memory
   the agent had. Useful for post-hoc analysis but non-ideal as a signal the
   judge sees while scoring. E.g. zero-condition R01 has `memex_chars=1081`
   vs production's `125` — the judge can draw inferences about which
   condition this is even though condition is *also* stated explicitly in
   the same block.

6. **`local_git_set.path` is a judge-tempdir path** (e.g.
   `/var/folders/.../syke-judge-x6pgv4k9/local_git_anchor.json`). Carrying
   the full `/var/folders/kc/...` path makes the packet noisy to read and
   isn't useful after the rollout — it's only meaningful inside the judge
   sandbox.

7. **`raw_context.slice_summary.total_elapsed_sec`** (e.g. `0.685`). This is
   how long the slice build took. No plausible bearing on scoring.

## 5. Load-bearing signal in the judge's input

What the judge actually references during scoring (read from traces and
verdict reasoning):

- **`probe.question` + `probe.reference_cutoff_iso`**. These anchor every
  verification bash call. Judges repeatedly cite the cutoff when deciding
  "stale vs current".
- **`answer.text`**. The judge extracts named claims (project names,
  commit subjects, test counts, file paths, version strings) and greps
  them against the slice. This is the dominant loop.
- **`slice/harnesses/{claude-code,codex,opencode}/...jsonl` files**. Every
  judge trace `find`s the slice tree early, then does targeted `rg`
  searches for literal claim strings.
- **`local_git_anchor.json.commits[]`**. Heavily used for verifying version,
  branch, test-pass claims. E.g. R01 gpt-judge verified `v0.4.5`, TCC fixes,
  config-file work by citing commit subjects.
- **Adapter markdowns** (`slice/adapters/claude-code.md`,
  `slice/adapters/codex.md`). Lightly used — the R17 judge read both as
  schema reference.
- **`judge_brief.partial_means` / `fail_means`**. Verdict summaries
  frequently echo these phrases ("stale residue", "overclaiming", "generic
  rather than restart-capable"). Boilerplate language propagates into
  verdicts even though it is not probe-specific.

Noticeably underused: `probe.source_ref`, `probe.family`,
`raw_context.replay_state.*`, `answer.metadata.*`. Judges tend to ignore
these in their reasoning.

## 6. Patterns across probes

- **Tool-call budget scales weakly with slice size, not packet size.** R08
  (2,995-file slice, 967-char answer) still gets 15–28 judge tool calls
  because the slice is big and the judge `find`s + `rg`s widely. R01
  (147-file slice) gets ~14–22 calls. The bigger the haystack, the more
  shell time.
- **Opus-judge calls more bash, almost never uses `read`.** Opus averages ~30
  bash + 1 read + 1 submit. GPT-5.4 judge averages ~14 bash + 5 read + 1–2
  submit. Same packet, very different instrument behavior.
- **Multi-submit on gpt-judge.** ~10 of 57 gpt-judge cells call
  `submit_judge_verdict` twice (R08, R09, R12, R14, R16, R17, R18, R19 in
  production; more in pure/zero). Each second call has a nearly identical
  verdict body — looks like a retry/echo in the Pi tool-call protocol. Opus
  judge submits exactly once in every cell sampled.
- **Concept-recall probes (R10, R11, R13) cause name-grep storms.** R17's
  24-call judge run had 4 consecutive `rg -n 'foo|bar|baz|...'` calls, each
  with 10–20 OR'd project names.
- **Short probes don't get less judge work, only less answer to verify.**
  R08 ("okay where are we now", 967 chars) produced the same judge trace
  shape as R06 (6,488 chars). The judge mostly tests the *slice*, not the
  *answer*.
- **Packet sizes track answer size, not probe importance.** R17's 25 KB
  pure-condition packet vs R14's 3.1 KB production packet is almost entirely
  answer-length driven (21.5k vs 0.6k chars).
- **R19 opus-production degenerate case is informative.** Agent timed out
  with 33-char answer; judge short-circuited to 3 calls and a "fail". The
  judge correctly refuses to over-invest on an empty target. No other opus
  judge cell went below 13 calls.
- **zero-condition answers run long.** E.g. R01 zero 5,215 chars vs prod
  2,636. With no MEMEX to constrain, the agent writes more; the judge then
  has more surface to check. This shows up as larger packets in zero cells
  for shorter probes.

## 7. UI recommendations

Three views that would let the user browse this cleanly in an extension to
`eval_viz.html`:

1. **Probe × condition grid (the overview sheet).** Rows = R01…R19, columns =
   production / pure / zero, two judge sub-columns each. Each cell shows:
   verdict (color chip), packet bytes, answer length, judge tool-call total,
   answer/slice file count. Clicking a cell expands the full packet view
   (§2 below). Filter controls: judge (gpt54/opus/cross), run id, verdict
   (pass/partial/fail), slice-size bucket. Surfaced fields:
   `probe_id`, `condition`, `verdict`, `packet_bytes`, `answer_len`,
   `judge_tool_calls.<judge>.total`, `slice_summary.sources.*.jsonl_lines`.

2. **Packet inspector (per cell).** Render `packet.json` as a structured
   panel, not a blob. Four fold-open sections: `probe`, `answer`,
   `raw_context`, `judge_brief`. Inline the *full* `answer.text` as
   rendered markdown (not JSON), with its metadata as a side chip. Under
   `raw_context`, show a live file-tree of the slice (lazy-loaded from
   `slice/slice_meta.json` + `find`) and a one-click jump to
   `local_git_anchor.json.commits[]` rendered as a commit log. Highlight
   the "noise" fields from §4 with a subdued style so the user can see what
   the judge-brief is vs what the actual claims-to-check are.

3. **Judge-trace timeline (per cell).** Render `judge_trace.json` as a
   top-to-bottom call log: `[i] tool_name — first 200 chars of input → first
   200 chars of output` with expand-on-click for each call. Alongside, show
   the judge's `thinking[]` stream as a collapsible sidebar. Color bash vs
   read vs submit_judge_verdict differently. This is the single most useful
   view for understanding what the judge actually did — it directly answers
   "did the judge find the evidence, or just the packet?". Filter: "only
   calls that cite `local_git_anchor`", "only calls that `rg`/`grep` the
   slice", "only calls that `read` files from slice".

Cross-cutting, a *noise-vs-signal diff* tool that lets you pick two cells
(e.g. R01 production vs R01 zero, or R01 gpt-judge vs R01 opus-judge) and
shows side-by-side: what differs in the packet, what differs in the
tool-call sequence, what differs in the verdict reasoning. Useful for the
"what actually moved the needle" question that keeps coming up elsewhere in
the lab.

Companion dataset for all of these: `datasets/judge_view_per_probe_20260421.json`.
