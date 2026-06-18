# Judge-Mining Calibration Anchors: BATCH B

## 1. Agreement Count Table

| Verdict | Opus-Ask | GPT-Ask | Total |
|---------|----------|---------|-------|
| **Pass** | 4 | 5 | 9 |
| **Partial** | 17 | 18 | 35 |
| **Fail** | 8 | 3 | 11 |

**Total agreed cells:** 55 of ~114 evaluated (48% agreement rate)

---

## 2. Pass Anchors

### A. R02 (production) — Opus-Ask
**Prompt:** "What did we work on yesterday March 7 2026 and today March 8 2026? List everything — commits, features, fixes, releases, any work at all. Be exhaustive..."

**Answer excerpt:** Exhaustive breakdown of March 7–8 work including 3 verified commits (correct SHAs), 4 verified issues (#10-#13 via gh-issue-create JSONL commands), 7 UserProfile cleanup commits, and 7 additional March 8 commits with LiteLLM evaluation.

**Opus-judge consensus:** "Excellent exhaustive reconstruction of two days of work. All 3 March 7 commits verified with correct SHAs; all 4 issues (#10-#13) verified via JSONL gh-issue-create commands; 7 UserProfile cleanup commits and 7 additional March 8 commits verified against git anchor."

**GPT-judge consensus:** "The answer is strongly grounded in the frozen harness data and restores the correct live work model for March 7–8, 2026. It accurately captures the release/daemon fixes, docs audit, UserProfile hard-delete cleanup, and the LiteLLM/Codex decision thread, with only minor uncertainty around some reconstructions."

**What both praise:** Complete artifact enumeration with verifiable SHA/ID grounding; multi-surface cross-validation (git, JSONL, issue commands); exhaustive temporal coverage spanning both days.

---

### B. R11 (pure) — Opus-Ask
**Prompt:** "What is the full vision for Observe? Everything we discussed — hook listener, tool reduction, federation, real-time capture, what adapters need to exist..."

**Answer excerpt:** Comprehensive reconstruction of Observe vision including 4-layer architecture, two runtimes, Sense Intelligence protocol, SKILL.md standard, adapter federation, and self-observation with strong evidence from git commits and JSONL sessions.

**Opus-judge consensus:** "Exceptional reconstruction of the Observe vision. The answer covers all major architectural components (4-layer architecture, two runtimes, Sense Intelligence protocol, SKILL.md standard, adapter federation, self-observation) with strong evidence backing from git commits and JSONL sessions."

**GPT-judge consensus:** "The answer substantially reconstructs the live Observe model from the frozen harness data: deterministic capture, raw evidence preservation, handoff over compaction, tool reduction, federation, real-time capture, adapter coverage, and completion criteria. It is mostly grounded, continuity-preserving."

**What both praise:** Holistic architectural vision synthesis from distributed evidence; layered component coverage; evidence binding to session/commit records; architectural coherence across subsystems.

---

### C. R01 (pure) — GPT-Ask
**Prompt:** "what's the current state of things? what am I working on, what's active, what's the latest?"

**Answer excerpt:** High-quality reconstruction of user's working state at cutoff, noting BRAINSTORM→FOUNDATIONS rename, test results (286 passed/3 skipped), LiteLLM rejection, Azure local-only stance, and branch discipline with direct JSONL session and git commit support.

**GPT-judge consensus:** "The answer provides a high-quality reconstruction of the user's working state at cutoff. All major claims are directly supported by JSONL session data and git commits: the BRAINSTORM→FOUNDATIONS rename, test results (286 passed/3 skipped), LiteLLM rejection, Azure local-only stance."

**Opus-judge consensus:** "Useful and mostly well-grounded reconstruction. It correctly centers the live late-day threads (Azure/provider architecture and AGENTS/workflow/private foundations docs) and accurately identifies the latest concrete action as the BRAINSTORM.md → FOUNDATIONS.md rename plus AGENTS/.gitignore updates."

**What both praise:** State-of-mind alignment with frozen slice; artifact/decision traceability to concrete sources; correct threading of active decision contexts (Azure, foundations architecture); accurate temporal orientation.

---

### D. R04 (production) — GPT-Ask
**Prompt:** "give me my work log today PST entire day..."

**Answer excerpt:** Exceptionally detailed reconstruction of full day's work on 2026-03-12 PST, time-blocked with 13 git commits spanning the day, 57-58 sessions, and cross-surface consistency mapping.

**GPT-judge consensus:** "The answer provides an exceptionally detailed and accurate reconstruction of the full day's work on 2026-03-12 PST. Key claims are corroborated by git commits (13 commits spanning the day), session timestamps (57-58 sessions), and session content samples."

**Opus-judge consensus:** "Pass: the answer reconstructs the day's real working model well enough for useful continuation, with strong support for the major threads and good cross-surface consistency."

**What both praise:** Comprehensive temporal coverage spanning full operational day; multi-session aggregation with verifiable commit/trace counts; working-model utility for immediate continuation.

---

## 3. Fail Anchors

### A. R01 (zero) — Opus-Ask
**Prompt:** "what's the current state of things? what am I working on, what's active, what's the latest?"

**Answer excerpt:** Claims 'clean slate' with no active work, no harness traces, empty sessions, only 1 memory (MEMEX text copy), 0 links.

**Opus-judge verdict:** "The answer claims a 'clean slate' with no active work, no harness traces, and empty sessions. The slice contains 147 JSONL files (9589 lines) showing rich activity: a docs audit sprint with 4 parallel fix agents, v0.4.5 shipped to PyPI, Issue #13 Codex proxy queued, CLI onboarding research, and the git anchor shows 10+ commits on March 8."

**GPT-judge verdict:** "The answer is not aligned with the frozen harness data. The slice shows many Claude Code transcripts, an active repo-investigation thread, and recent git activity, while the answer incorrectly claims an empty workspace and no active work. It is overconfident, misses the live thread, and is not restart-capable."

**What both penalize:** Hallucinated emptiness contradicted by observable slice content; failure to detect live activity in JSONL/session corpus; overconfident false negatives on workspace state.

---

### B. R06 (zero) — Opus-Ask
**Prompt:** "what was I last working on in syke? what was left to do? what were the most recent threads and decisions?"

**Answer excerpt:** Describes benchmark's internal zero-condition memory system state (cycle #7, empty syke.db) instead of user's actual development work.

**Opus-judge verdict:** "The answer fundamentally misidentifies the user's work. Instead of reconstructing the active development state (v0.4.6 release, Observe-Map-Ask architecture design, memory evolution research, CLI improvements, synthesis pipeline, LLM provider integration), it describes the benchmark's internal zero-condition memory system state."

**GPT-judge verdict:** "The answer partially captures the broad Syke theme but fails the benchmark because it misses the actual live threads at the cutoff and introduces unsupported/future-state claims, especially the April-dated Codex traces and zero-state DB assertions."

**What both penalize:** Contextual misidentification (meta-system vs. user state); conflation of benchmark scaffold with actual work; unsupported future-state claims.

---

### C. R08 (zero) — Opus-Ask
**Prompt:** "okay where are we now..."

**Answer excerpt:** Diagnoses syke.db meta-state (1 memory, 0 links, MEMEX references unresolved) but completely misses actual live work context.

**Opus-judge verdict:** "The answer diagnoses syke.db meta-state (empty DB, MEMEX references not resolving) but completely misses the user's actual live work context. On 2026-03-14, the user was deep in Observe Phase 2 development with 10+ git commits, had a rich thread map (Thread 12 real-time promoted to killer feature, Thread 14 multi-agent writers, Thread 33 SOTA research)."

**GPT-judge verdict:** "The answer is not trustworthy for continuation. It asserts an empty sessions/DB world that is contradicted by the frozen slice, the transcript corpus, and the git anchor. The live state at the time was a dirty syke repository on main with a staged new file and several unstaged edits."

**What both penalize:** Focus on false meta-diagnostics; systematic blindness to actual work threads despite rich slice evidence; failure to distinguish system state from user work state.

---

## 4. Partial Anchors

### A. R02 (pure) — Opus-Ask
**Prompt:** "What did we work on yesterday March 7 2026 and today March 8 2026? List everything..."

**Answer excerpt:** Comprehensive work log capturing March 7–8 cleanup, UserProfile, OmO, and LiteLLM activity with breadth but date misattributions on releases (v0.4.4, v0.4.5).

**Opus-judge:** "The answer is remarkably comprehensive and captures all major work items from the period, with strong detail on commits, decisions, and cleanup efforts. However, it has a significant date misattribution problem: v0.4.4, v0.4.5, and all associated pre-release work are backdated."

**GPT-judge:** "The response captures many real March 7–8 workstreams, especially the March 8 cleanup/UserProfile/OmO/LiteLLM activity and the March 7 docs/daemon work, but it misdates releases, leaks prior-day setup/config material into the target window, and overstates exhaustiveness."

**Agreed partial meaning:** Strong topical recovery with artifact enumeration, but systematic temporal/attributional errors that prevent full confidence; useful broad model with localized failure modes.

---

### B. R04 (production) — Opus-Ask
**Prompt:** "give me my work log today PST entire day..."

**Answer excerpt:** Impressively detailed reconstruction of 526 claude-code sessions identifying major threads (README rewrite, v0.4.6 release, Observe design) but contains factual errors on numerics.

**Opus-judge:** "The answer provides an impressively detailed reconstruction of an extremely active 24-hour work day from 526 claude-code sessions, correctly identifying major threads... However, it contains factual errors: overcounting on some thread details."

**GPT-judge:** "The answer reconstructs the correct March 12 workstream mix and is useful for continuation, but it overclaims certainty on a few numeric and summary details, so it is not fully strongly grounded."

**Agreed partial meaning:** Strong structural recovery and thread mapping with useful continuation utility, but numeric precision overstated; reliable for direction-setting but not micro-level planning.

---

### C. R04 (zero) — Opus-Ask
**Prompt:** "give me my work log today PST entire day..."

**Answer excerpt:** Captures ~57 sessions with accurate topic identification (GEPA, ACE, RLM research, issue #14, observability, Mastra), but timezone conversions and chronology muddled; Mar 11 sessions misattributed to Mar 12.

**Opus-judge:** "The answer demonstrates impressive breadth in capturing a massive workday (~57 sessions) with accurate identification of most activity topics... However, significant timezone conversions and some chronological issues."

**GPT-judge:** "The answer recovers many real Syke work threads and is directionally useful, but it is not a reliable day-long work log: the chronology is muddled, time zones are mishandled, and several Mar 11 local sessions are presented as Mar 12 work."

**Agreed partial meaning:** Topic recovery sound despite temporal/timezone errors; useful for research vector identification but unreliable for hour-by-hour timeline; continuable for thematic work but not for time-locked decisions.

---

### D. R05 (pure) — Opus-Ask
**Prompt:** "what are all my current open threads, priorities, and unfinished work? include: research vectors (ACE, GEPA, sleep/dream, filesystem), open bugs..."

**Answer excerpt:** Comprehensive thread reconstruction from 797 JSONL files covering research vectors (Hopfield, GEPA, ACE, ALMA), architecture threads (observe layer, compaction), and engineering state, but mislabels fixed bugs (#14, #15) as open.

**Opus-judge:** "Exceptionally comprehensive thread reconstruction from 797 JSONL files with strong coverage of research vectors (Hopfield/GEPA/ACE/ALMA), architecture threads (observe layer, compaction invisibility), engineering state (stash, pointer emergence), and competitive positioning."

**GPT-judge:** "Useful but stale. The answer correctly recovers the main requested research vectors and several open issues, but it mislabels already-fixed bugs (#14, #15) as open and omits other live threads visible in the slice."

**Agreed partial meaning:** Comprehensive knowledge base synthesis with strong thematic coverage but outdated bug/issue classification; useful for research continuity but hazardous for action items without re-verification.

---

### E. R07 (production) — Opus-Ask
**Prompt:** "remember all the threads we made yesterday and map the timeline for today and yesterday..."

**Answer excerpt:** Strong structural reconstruction of Mar 13–14 working arc with correct research-to-implementation progression and observe-phase2 branch identification, but overstates precision on counts, timings, and memory-commit outcomes.

**Opus-judge:** "The answer provides a strong structural reconstruction of the Mar 13-14 working arc, correctly identifying the research-to-implementation progression and the observe-phase2 branch as the terminal active thread. Core topics, branches, and artifacts are well-grounded."

**GPT-judge:** "The response correctly restores the broad Mar 13–14 Syke/observe arc and matches the live observe-phase2 implementation transition, with supporting evidence in the Claude Code session traces and the git anchor. But it overstates precision on counts, timings, and memory-commit outcomes."

**Agreed partial meaning:** Arc trajectory and phase mapping accurate; terminal-state branch identification correct; but quantitative precision not warranted; useful for conceptual continuation but not for event-count decisions.

---

## 5. Three-Way Distillation

### Canonical Pass Criteria
Every agreed pass includes: (1) **temporal grounding with verifiable artifacts** — specific commit SHAs, issue IDs, session counts that can be cross-checked against git/JSONL anchors; (2) **topical exhaustiveness within scope** — no claimed "clean slate" or false negatives; (3) **multi-surface consistency** — reconciliation across git history, session transcripts, and issue records showing the same narrative; (4) **specificity of decision context** — accurate identification of active threads (e.g., "Azure provider architecture," "BRAINSTORM→FOUNDATIONS rename") that match the slice's actual decision surface. Passes reward *grounded, verifiable, scope-appropriate completeness*.

### Canonical Fail Criteria
Every agreed fail exhibits: (1) **systematic factual contradiction** — claims (empty workspace, no active threads) directly falsified by observable slice evidence (147 JSONL files, 10+ commits); (2) **contextual misidentification** — confuses meta-system state (syke.db internal scaffold) with user work state, or asserts future/past claims unsupported by evidence; (3) **overconfident false negatives** — asserts absence without evidence of searching, missing live activity in rich corpus; (4) **non-restart-capable state models** — user cannot safely resume work from the reconstructed state. Fails penalize *contradiction, context-blindness, and unsafe continuity*.

### Canonical Partial Signature
Every agreed partial exhibits: (1) **strong topical/structural recovery with localized failure modes** — captures major threads, correct architectures, research vectors, but makes systematic errors in one dimension (dates, counts, bug status, timezone conversions); (2) **utility-appropriate uncertainty** — useful for direction-setting and thematic continuation but explicitly unreliable for micro-level actions (exact timing, numeric precision, outdated bug lists); (3) **recoverable via human verification** — the error is *human-checkable* (did we really do that on that date?) rather than requiring oracle knowledge; (4) **knowledge-base vs. state distinction** — either encyclopedic (recovers research vectors, design rationale) but stale (bugs marked open are now closed), or contemporaneous (accurate topics) but imprecise (chronology muddled). Partials reward *informed incompleteness*.

---

## 6. Rubric-Anchor Observations

1. **Grounding-by-artifact is the canonical pass requirement.** Every agreed pass includes specific, cross-verifiable artifacts (commit SHAs, issue IDs, session counts, file names). Answers that name only broad themes ("docs work," "architecture design") without supporting IDs are consistently downgraded to partial or fail. The rubric should require: "Every claim must reference a checkable artifact (commit, issue, file, session) or be marked as inference."

2. **Absence claims are high-risk without evidence of search.** R01/R06/R08 (zero condition) fails all claim "no work," "empty workspace," or "clean slate" without explicitly stating what was searched and found empty. Passed answers always acknowledge what evidence was available. Rubric fix: "Absence claims require explicit statement of search scope (e.g., 'searched 147 JSONL files across dates X-Y, found no commits on Z')."

3. **Temporal precision is asymmetric: dates are load-bearing, counts are supplementary.** R02/R04 partials misdated releases (v0.4.4 backdated) or misattributed sessions (Mar 11 → Mar 12), downgrading passes to partials. But count errors (57 vs 56 sessions) don't trigger fail if direction and threads are right. Rubric: "Dates must be explicit and verifiable to the session/commit record. Session/commit counts may be approximate if major threads are correctly identified."

4. **Context-switching failure is a fail signature.** Fails consistently confuse user work state with system meta-state (syke.db cycles, MEMEX scaffolding) or past/future work with present threads. Passes and partials stay laser-focused on the *user's actual working model at cutoff*. Rubric: "Every response must distinguish between (a) user work state, (b) system memory state, (c) historical context, (d) projected future work. Conflating these is a fail."

5. **Multi-surface cross-validation is what elevates comprehensive-but-imprecise to pass.** R02 (production) and R11 (pure) passes both cite git commits + JSONL sessions + issue records in the same breath. R04 production-pass cites "526 sessions, 13 commits, cross-surface consistency." Partials cite only one or two surfaces, or cite conflicting surfaces. Rubric: "Pass-level grounding requires reconciliation across at least two surfaces (git + sessions, or sessions + issues, or commits + decision threads)."

6. **"Useful but stale" is the agreed-partial sweet spot.** R05 partial is accurate on research vectors and architecture but flags closed bugs as open. It's trustworthy for "what are we researching?" but hazardous for "what should I fix next?" Passes make no such trade-offs. Rubric: "Partials are acceptable when (a) the knowledge domain is correctly recovered and (b) the answer explicitly notes which elements require re-verification before action (e.g., 'research vectors are solid; bug list needs refresh')."

