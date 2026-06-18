# Judge Disagreement Forensics: Opus 4.6 vs GPT-5.4

## Headline Count Table

Across 57 opus-ask items with matching gpt-judge verdicts:

| Category | Count | % of Disagreements |
|----------|-------|-------------------|
| Opus upgraded (pass/partial vs partial/fail) | 27 | 96% |
| Opus downgraded (partial→pass, fail→partial) | 1 | 4% |
| Full agreement | 29 | 51% of total items |

**Key finding:** Opus skews +0.49 scale-points by defaulting toward generosity on reconstruction answers that mix grounded facts with narrative inference.

---

## Disagreement Archetypes with Direct Quotes

### Archetype 1: "Opus Promotes Partial → Pass"

**Pattern:** Opus accepts answers with minor factual errors or unsupported claims as complete; GPT flags them for unverified reconstruction.

#### Example 1: `[R01 production]` — Strong facts + minor timestamp drift

**Opus verdict: PASS** | **GPT verdict: PARTIAL**

> **Opus factual_grounding:** "Nearly every claim in the answer is directly verifiable in the slice data. v0.4.5 version, 286 tests, 7-commit UserProfile cleanup chain with specific model/file deletions, Azure integration quote, LiteLLM evaluation details, 546-line codex proxy, zai provider, OhMyOpenCode tooling, 141 sessions, 0 Codex sessions — all confirmed. The only minor issue is calling the LiteLLM decision 'not fully locked yet' when the memory system itself marked it CLOSED, but the broader multi-provider question (Azure) was indeed still open, making this a reasonable characterization." [R01 production factual_grounding opus]

> **GPT factual_grounding:** "Several concrete claims are supported by the frozen surface: v0.4.5/release cleanup appears in local_git_anchor, the UserProfile/ActiveThread/VoicePattern hard-delete is real, and the slice summary does show zero Codex JSONL files. But the answer also asserts active work like Azure integration, workflow standardization, and AGENTS/internal-doc work without clear support in the slice for that timepoint, so it mixes grounded facts with unsupported reconstruction." [R01 production factual_grounding gpt]

**Axis divergence:** Opus treats partial verification (Azure is "indeed still open") as passing tolerance for narrative flow. GPT demands slice-bounded evidence for claim assertions.

#### Example 2: `[R01 pure]` — Session-verified facts + unsupported extrapolation

**Opus verdict: PASS** | **GPT verdict: PARTIAL**

> **Opus coherence:** "The answer maintains internal consistency across all claims. The profile cleanup chain, docs overhaul, provider architecture, and tooling details all form a coherent picture that matches the cross-session evidence." [R01 pure coherence opus]

> **GPT coherence:** "The answer is internally readable and mostly consistent, but it blends evidence from different times and surfaces without clearly separating what is current, completed, or merely inferred. That weakens cross-session and cross-artifact coherence." [R01 pure coherence gpt]

**Axis divergence:** Opus rewards narrative coherence even when claim grounding is uncertain. GPT requires explicit source bounding to accept coherence.

---

### Archetype 2: "Opus Promotes Fail → Partial"

**Pattern:** When answers contain critical errors (false state claims, missed latest commits), Opus credits partial recovery via correct identification of *threads* while GPT flags the false current-state as disqualifying.

#### Example 1: `[R03 zero]` — Wrong synthesis state but correct session IDs

**Opus verdict: PARTIAL** | **GPT verdict: FAIL**

> **Opus factual_grounding:** "The answer correctly identifies real sessions and their content (synthesis research, LiteLLM work), but makes a critical factual error: it claims finalize_memex was never committed ('No code changes landed yet'), when git anchor shows commit 4fddf402 'feat(synthesis): rewrite pipeline with finalize_memex tool contract and Stop hook enforcement' at 16:24:50 PDT on Mar 11. It also misidentifies HEAD as b609bcf when actual HEAD is 853fc780 with ~7 later commits. The answer presents a mid-day snapshot as the final state." [R03 zero factual_grounding opus]

> **GPT factual_grounding:** "The answer contains some slice-supported elements (e.g. the March 11 focus on Syke work and the existence of LiteLLM/multi-provider research), but it also states several current-state claims that conflict with the frozen evidence. Most notably, local_git_anchor.json shows a synthesis rewrite commit (`4fddf402... feat(synthesis): rewrite pipeline with finalize_memex tool contract and Stop hook enforcement`) already landed before the cutoff, so 'no code changes landed yet' is wrong. It also treats an earlier research thread as current even though later March 11 sessions in the slice move on to OpenCode/OmO context-file auditing and CLAUDE.md compatibility." [R03 zero factual_grounding gpt]

> **Opus continuity:** "The answer identifies relevant work threads (LiteLLM, synthesis modernization, architecture docs) but gets the current state of the most important thread wrong. The synthesis modernization was DONE, not pending. This undermines continuation value significantly." [R03 zero continuity opus]

> **GPT continuity:** "The answer fails to restore the live working model at cutoff. The actual latest thread in the slice is the OpenCode/OmO audit about files agents use for trajectories and removing CLAUDE.md baggage, not the Syke synthesis/diagram thread it foregrounds. It also misses the transition in synthesis modernization from research into a landed finalize_memex/Stop-hook implementation." [R03 zero continuity gpt]

**Axis divergence:** Opus assigns partial credit for identifying *which sessions exist*; GPT treats false state-of-completion (missed a landed commit) as a fundamental reconstruction failure because a restarting user would execute wrong next steps.

#### Example 2: `[R05 production]` — Stale version + invented threads

**Opus verdict: PASS** | **GPT verdict: FAIL**

> **Opus factual_grounding:** "Most claims are well-supported by slice evidence (ACE, GEPA, OMEGA, ALMA, Hopfield, observe layer, stash, 93% gap, UserProfile deletion, Pi removal, multi-provider, research vectors). However, the answer states 'v0.4.5 released' in Recently Resolved when the git anchor clearly shows v0.4.6 was released on Mar 12 — the day before the reference date. The orphan events commit '508b4e1' is not verifiable in the git anchor. These are minor but concrete factual errors." [R05 production factual_grounding opus]

> **GPT factual_grounding:** "The answer is not purely fabricated: it correctly reflects some broad research vectors and historical context (ACE/GEPA/sleep/filesystem, memory-systems landscape, some resolved items). But it is not well grounded in the frozen slice for the cutoff date: it states stale status markers like v0.4.5 and 293 tests when the slice shows v0.4.6 and 286 tests, and it invents a 10-thread inventory that does not match the validated open issue set or memex state. Several current threads in the slice (#14 ask timeout, #12 filesystem FDA, #8 harness adapters) are omitted while older/stale residue is presented as current." [R05 production factual_grounding gpt]

**Axis divergence:** Opus tolerates version staleness ("minor") and unverifiable commits if the research landscape is "broadly correct." GPT rejects answers where the state at cutoff is systematically stale and the thread inventory is invented.

---

### Archetype 3: "Opus Downgrades Pass → Partial" (Rare Reverse)

**Pattern:** Opus penalizes answers that have strong factual grounding and correct thread identification but miss an active implementation thread not in the session traces GPT examines.

#### Example: `[R12 zero]` — Factually correct but continuation-incomplete

**Opus verdict: PARTIAL** | **GPT verdict: PASS**

> **Opus continuity:** "The answer correctly identifies the Observe post-Phase 2 planning thread and extracts detailed discussion content. However, it misses the most significant active thread: the 'Sense Intelligence' initiative that was being actively BUILT on March 15, as evidenced by 10+ git commits (file watcher with watchdog, JsonlTailer, SenseWriter, HealingLoop, LLM-powered adapter generator, harness discovery, format analyzer, adapter sandbox, Sense Intelligence protocol). This was the actual implementation work happening that day." [R12 zero continuity opus]

> **GPT continuity:** "The answer restores the right live thread: what remained after Observe Phase 2. It prioritizes the actual next workstreams discussed in-session rather than drifting into unrelated memories. It is restart-capable because it names the concrete threads and the intended sequencing." [R12 zero continuity gpt]

> **Opus factual_grounding:** "Nearly all specific claims in the answer are directly verifiable in session ses_3105cd222ffeZmCFtCQw3aG3yp: PreToolUse, SubagentStart, PostToolUseFailure, Adapter Droid (40 occurrences), 20 TOML harness descriptors (25 occurrences), 4-tier architecture with exact latency numbers, transport-agnostic dedup via external_id, 220 events silently truncated at 50K, Thread 12, Dolt-style provenance, CLI-first/skill-second, universal session ontology marked 'not yet', 5 working adapters, 151K events." [R12 zero factual_grounding opus]

**Axis divergence:** Opus checks completeness against git evidence (hence the Sense Intelligence penalty); GPT checks only against session/slice truth surface, allowing answers that miss out-of-scope implementation.

---

### Archetype 4: "Axis-Split" — Same Verdict, Different Drivers

**Pattern:** Both judges assign PASS, but disagree sharply on which axis drives the verdict and with what confidence. Reveals different rubric weights.

#### Example: `[R02 zero]` — Both PASS, but axis confidence mismatch

**Opus verdict: PASS** | **GPT verdict: PASS** ✓ **[Same verdict, axis split]**

Opus axis scores: factual_grounding=strong, continuity=strong, coherence=strong  
GPT axis scores: factual_grounding=partial, continuity=partial, coherence=partial

> **Opus factual_grounding:** "The answer's commit list matches the git anchor extremely well - correct SHAs, subjects, and approximate timestamps for ~20 commits. LiteLLM research, TCC protection, profile cleanup, issues, and Oh-My-OpenCode/Sisyphus references are all confirmed in session data. The session count of ~75 matches exactly. Minor inaccuracies: v0.4.5 described as 'shipped during Mar 7' when it was committed Mar 6." [R02 zero factual_grounding opus]

> **GPT factual_grounding:** "Most of the core timeline is backed by the local git anchor and harness traces: the March 7 TCC fix, the docs overhaul, the March 8 cleanup commits, and the LiteLLM/claude-agent-sdk research all appear in the slice. However, the answer also makes claims that are not directly supported on the bounded evidence surface, such as the push assertions and the exact session/commit totals." [R02 zero factual_grounding gpt]

> **Opus continuity:** "The answer provides an exceptionally detailed reconstruction of two days of work, organized by theme and timeline. It identifies the active threads (cleanup, docs, architecture research, OmO setup), tracks state transitions well, and provides clear continuation value. This was done from a 'zero' memex condition, making the reconstruction quality remarkable." [R02 zero continuity opus]

> **GPT continuity:** "The answer restores the main live threads for continuation: multi-provider/provider-picker setup, config.toml, TCC/LaunchAgent protection, docs overhaul, LiteLLM vs claude-agent-sdk, dead-code/profile cleanup, and OmO/.sisyphus instruction-file work. That is useful for re-entry, but some active threads from the slice are not explicitly surfaced, and the timeline is a bit fuzzy." [R02 zero continuity gpt]

**Axis divergence:** Opus credits "strong" across all three axes, treating exact SHAs and detailed reconstruction as sufficient; GPT caps each axis at "partial," reserving "strong" only for claims directly verifiable on bounded surface without extrapolation.

---

## Judge Value Lexicon

### Opus Rewards

1. **Narrative coherence over source certainty** — "The answer maintains internal consistency across all claims...all form a coherent picture" even if some underlying claims lack slice support. Single quote: _"The answer maintains a consistent world model across the single harness (claude-code) and git evidence."_ [R01 pure coherence opus]

2. **Thread identification over state accuracy** — Gives partial credit for correctly naming threads (synthesis, LiteLLM, AGENTS work) even if the status is stale or wrong. Quote: _"The answer correctly identifies real sessions and their content (synthesis research, LiteLLM work)"_ despite claiming synthesis was not committed when it was. [R03 zero factual_grounding opus]

3. **Broad landscape knowledge** — Credits answers that reflect correct research vectors or historical context without pinning each claim to slice evidence. Quote: _"Most claims are well-supported by slice evidence (ACE, GEPA, OMEGA, ALMA...)"_ treats category correctness as grounding sufficiency. [R05 production factual_grounding opus]

4. **Detail density** — Rewards answers with specific numbers, timestamps, and cross-references as signals of knowledge even when some are unverifiable. Quote: _"The answer's commit list matches the git anchor extremely well - correct SHAs, subjects, and approximate timestamps for ~20 commits."_ [R02 zero factual_grounding opus]

5. **Reconstruction effort** — Credits _reconstruction quality_ from zero memex as a compensatory factor for minor inaccuracies. Quote: _"This was done from a 'zero' memex condition, making the reconstruction quality remarkable."_ [R02 zero continuity opus]

### GPT Rewards

1. **Slice-bounded verification** — All claims must be traceable to frozen surface (git_anchor, session traces, memex snapshots). Refuses extrapolation. Quote: _"But the answer also asserts active work like Azure integration...without clear support in the slice for that timepoint."_ [R01 production factual_grounding gpt]

2. **Accurate current state** — False claims about what is "done" or "released" are disqualifying, even if supporting context is correct. Quote: _"it states stale status markers like v0.4.5 and 293 tests when the slice shows v0.4.6 and 286 tests."_ [R05 production factual_grounding gpt]

3. **Continuation fidelity** — Answers must restore the live working model such that a restarting user executes correct next steps; missing an active implementation is a failure. Quote: _"The answer fails to restore the live working model at cutoff. The actual latest thread in the slice is the OpenCode/OmO audit...not the Syke synthesis/diagram thread it foregrounds."_ [R03 zero continuity gpt]

4. **Explicit source attribution** — Separates "current" from "completed" from "planned" and grounds each claim type in specific evidence. Quote: _"it blends evidence from different times and surfaces without clearly separating what is current, completed, or merely inferred."_ [R01 pure coherence gpt]

5. **Conservative axis assignment** — Reserves "strong" scores only for claims directly verifiable without extrapolation; caps most answers at "partial" to signal room for improvement. Quote: _"However, the answer also makes claims that are not directly supported on the bounded evidence surface...such as the push assertions and the exact session/commit totals."_ [R02 zero factual_grounding gpt]

---

## Calibration-Actionable Observations

1. **State-of-completion claims require current-state lockdown:** The rubric must explicitly require answers to declare which claims are "as of cutoff" vs. "historical context" vs. "inferred from threads." Opus tolerates stale version markers (v0.4.5 when v0.4.6 is live) as "minor," while GPT rejects them as false state. The next judge contract should mandate a "timestamp claim" rule: any past-tense assertion about what exists/does not exist must cite a specific git/session timestamp or be marked speculative.

2. **Continuation precedence over narrative coherence:** When an answer reconstructs a coherent narrative but misses an active implementation thread (R12: Opus saw Observe planning, missed Sense Intelligence builds), the penalty should scale with whether the answer claims to be "completeness-sufficient." Opus downgrades for omission; GPT upgrades for providing actionable session-grounded threads despite the omission. The rubric should define: _continuity tracks whether the user can restart; coherence tracks internal self-consistency._ If they conflict, continuity wins.

3. **Exact metrics (session counts, test counts, commit SHAs) are overweighted by Opus:** Both judges agree exact SHAs verify grounding, but Opus treats "approximately correct session counts" (75 sessions ≈ 75 correct) as strong factual_grounding, while GPT caps it at partial. Next judge should distinguish between _verifiable exact facts_ (commit SHAs, specific error messages) and _derived aggregate counts_ (session totals, test runs), capping confidence on aggregates unless explicitly enumerated in slice.

4. **Reconstruction from zero memex does NOT warrant generosity on state accuracy:** Opus applies a "quality" bonus for successful reconstruction from scratch, which inflates verdicts on answers that correctly name threads but get current state wrong. GPT ignores reconstruction difficulty. The rubric should clarify: _difficulty is not a truth modifier._ An answer that reconstructs 80% of threads correctly but claims the most active one is not done should fail continuity, not earn a partial pass.

5. **Thread inventory must match slice-bounded open set:** R05 exemplifies this: Opus accepts "10-thread inventory" as "broad knowledge," GPT flags it as invented. Next contract should define a "thread inventory rule": if the answer lists specific open work items, each must correspond to a named issue, session thread, or memex entry in the frozen slice. Unverifiable inventions drop the score by ≥ 1 level.

---

_Generated April 20, 2026 from opus-ask × gpt-judge vs opus-ask × opus-judge disagreement set (n=28 disagreements, 57 total items)._
