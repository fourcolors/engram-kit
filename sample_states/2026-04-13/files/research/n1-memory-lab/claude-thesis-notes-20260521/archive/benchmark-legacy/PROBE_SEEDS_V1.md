# PROBE_SEEDS_V1

Validated probe set for the n=1 memory lab. This revision reorganizes the original 50-probe set by dataset, drops 6 probes that tested the probe set itself rather than user continuity, rewrites 25 probes to use natural user-perspective prompts, and adds 11 new probes (P51-P61) covering NE-1.1 windows and failure modes extracted from P49.

Total active probes: **55** (8 kept verbatim + 11 kept as-is + 25 rewritten + 11 new)

## Probe seed schema

Each seed below includes:
- `id`
- `family`
- `source`
- `prompt sketch`
- `what it stresses`
- `likely naive-system failure`
- `why it matters in real use`

---

## 1. NE-1.1 probes (Jan 9 - Feb 8)

Sources available: codex, opencode, hermes. No Claude Code data.

### P03
- **family:** decision archaeology
- **source:** `S01` (`2025-12-23 -> 2025-12-24`)
- **prompt sketch:** "What was the actual push around the golden set / benchmark work in this period?"
- **what it stresses:** benchmark-related decision tracing under dense codex activity
- **likely naive-system failure:** summarizes the repo work but misses the underlying decision pressure
- **why it matters in real use:** many later architectural choices depend on these early eval decisions

### P04
- **family:** multi-agent reconstruction
- **source:** `S02` (`2026-01-29`)
- **prompt sketch:** "What was happening across all those parallel sessions that day, and what was the shared objective?"
- **what it stresses:** reconstructing a multi-session, multi-agent day as one coherent line of work
- **likely naive-system failure:** reports one session well but loses the global thread
- **why it matters in real use:** this is closer to actual agentic work than single-thread recall

### P05
- **family:** architecture-comparison retrieval
- **source:** `S02`
- **prompt sketch:** "Which competitor or architecture constraints were being investigated across those research threads?"
- **what it stresses:** retrieval across distributed research lanes
- **likely naive-system failure:** collapses many targeted subquestions into one vague competitor summary
- **why it matters in real use:** architecture decisions are often distributed across many micro-investigations

### P36
- **family:** uncertainty calibration
- **source:** `S02` + `S06`
- **prompt sketch:** "Where are the gaps in my work history from January through March? Which periods are well-recorded and which are thin?"
- **what it stresses:** calibrated confidence in partial reconstruction
- **likely naive-system failure:** presents a smooth but overconfident narrative even where the evidence is thin or mixed
- **why it matters in real use:** useful continuity includes uncertainty boundaries, especially in multi-session or multi-harness reconstruction

### P43
- **family:** perspective shift
- **source:** `S02` + `S05`
- **prompt sketch:** "Explain this period once as a product-memory story and once as an operations/release story. What stays the same and what changes?"
- **what it stresses:** answering from the right viewpoint without losing core facts
- **likely naive-system failure:** gives one blended answer that is neither operationally useful nor conceptually clear
- **why it matters in real use:** the same trace often has to support different tasks, and memory needs viewpoint control

### P51
- **family:** evidence-provenance
- **source:** NE11-W1 (`2026-01-29 -> 2026-01-30`)
- **prompt sketch:** "Which claims in the eval report from late January are directly supported by artifacts, and which are inference?"
- **what it stresses:** distinguishing evidence from inference in an audit context
- **likely naive-system failure:** treats all claims as equally supported
- **why it matters in real use:** provenance discipline is central to the n=1 thesis

### P52
- **family:** resumption-after-gap
- **source:** NE11-W2 (`2026-01-31 -> 2026-02-03`)
- **prompt sketch:** "What was the last completed eval run, and what is the current live task?"
- **what it stresses:** simple local-state recovery from a single harness
- **likely naive-system failure:** confuses completed runs with in-progress runs
- **why it matters in real use:** the simplest possible resumption test -- L1 difficulty baseline

### P53
- **family:** priority-extraction
- **source:** NE11-W2 (`2026-01-31 -> 2026-02-03`)
- **prompt sketch:** "Which finding from the release-eval review is highest severity, and what artifact supports it?"
- **what it stresses:** extracting priority from a set of findings with evidence backing
- **likely naive-system failure:** lists findings without ranking or picks recency over severity
- **why it matters in real use:** memory should help users focus, not just remember

### P54
- **family:** architecture-boundary
- **source:** NE11-W3 (`2026-02-04 -> 2026-02-05`)
- **prompt sketch:** "What is the difference between the eval harness codepaths and the production codepaths? Where do they diverge?"
- **what it stresses:** distinguishing test infrastructure from production code
- **likely naive-system failure:** collapses eval and production into one description
- **why it matters in real use:** architectural boundaries are a real source of confusion in complex codebases

### P55
- **family:** resumption-after-gap
- **source:** NE11-W4 (`2026-02-06 -> 2026-02-08`)
- **prompt sketch:** "Figure out what we were working on last session and what the current state is."
- **what it stresses:** cold-start resumption from session traces
- **likely naive-system failure:** gives a generic summary instead of recovering the specific working state
- **why it matters in real use:** this exact prompt was found verbatim in the NE11-W4 traces

### P56
- **family:** causal-diagnosis
- **source:** NE11-W4 (`2026-02-06 -> 2026-02-08`)
- **prompt sketch:** "Build a causal model separating prompt failure, tool-loop failure, and data failure in the BEAM regressions."
- **what it stresses:** structured causal diagnosis from trace evidence
- **likely naive-system failure:** attributes all failures to one cause or gives a vague "it's complex"
- **why it matters in real use:** memory should support causal reasoning, not just recall

### P57
- **family:** priority-extraction
- **source:** NE11-W4 (`2026-02-06 -> 2026-02-08`)
- **prompt sketch:** "What is the smallest next experiment that would reduce uncertainty the most?"
- **what it stresses:** converting diagnostic knowledge into an actionable next step
- **likely naive-system failure:** suggests the largest or most recent experiment instead of the most informative one
- **why it matters in real use:** memory should help users choose experiments, not just list them

### P58
- **family:** evidence-provenance
- **source:** NE11-W1+W4 (`2026-01-29 -> 2026-01-30` + `2026-02-06 -> 2026-02-08`)
- **prompt sketch:** "Reconstruct the minimum evidence chain needed to defend the eval report to a skeptical reviewer."
- **what it stresses:** constructing a defensible evidence chain from distributed sources
- **likely naive-system failure:** restates claims without tracing them to artifacts
- **why it matters in real use:** the benchmark must prove its own claims are grounded -- this tests that recursively

---

## 2. NE-1.2 probes (Feb 8 - Mar 6)

### P01
- **family:** resumption-after-gap
- **source:** `S03` (`2026-02-23`)
- **prompt sketch:** "I just came back. What happened since I left, and what plan were we already using?"
- **what it stresses:** resumption + prior-plan recovery
- **likely naive-system failure:** gives only latest visible state; forgets that a plan was already discussed and justified earlier
- **why it matters in real use:** this is exactly the cost users pay every morning or after a context gap

### P02
- **family:** forgotten-analysis recovery
- **source:** `S03`
- **prompt sketch:** "You forgot we already analyzed this with data. What earlier analysis are you missing?"
- **what it stresses:** memory of prior evidence, not just prior conclusion
- **likely naive-system failure:** paraphrases the issue generically without recovering the earlier data-backed reasoning
- **why it matters in real use:** decision quality collapses if every session re-derives from scratch

### P06
- **family:** practical-value / doc hygiene
- **source:** `S04` (`2026-02-25 -> 2026-02-26`)
- **prompt sketch:** "Why did the memex-evolution doc matter, and what operational value was it trying to unlock?"
- **what it stresses:** practical-value interpretation, not just file creation recall
- **likely naive-system failure:** answers with "it documented snapshots" and misses why that reduces confusion and re-explanation
- **why it matters in real use:** memory value often appears as reduced clutter and clearer routes, not explicit QA wins

### P07
- **family:** latent constraint retrieval
- **source:** `S04`
- **prompt sketch:** "What was the real goal behind requesting the memex-evolution doc?"
- **what it stresses:** surfacing the implicit need for readable canonicalization and day-by-day legibility
- **likely naive-system failure:** only reports the doc request literally
- **why it matters in real use:** many durable rules begin as throwaway formatting or consolidation requests

### P08
- **family:** source migration
- **source:** `S05` (`2026-02-27 -> 2026-03-01`)
- **prompt sketch:** "What changed in the memory situation when Hermes entered the trace?"
- **what it stresses:** source arrival as architecture signal, not just new events
- **likely naive-system failure:** treats Hermes as another source row rather than a new memory regime entering the scene
- **why it matters in real use:** source changes alter what continuity means

### P09
- **family:** routing under noise
- **source:** `S05`
- **prompt sketch:** "What memory-layer failures were observed across harnesses in late February?"
- **what it stresses:** architecture-aware routing
- **likely naive-system failure:** gives a generic answer detached from the actual slice properties
- **why it matters in real use:** the value of memory depends on choosing the right surface, not just any surface

### P14
- **family:** search entropy reduction
- **source:** `S03` + `S04`
- **prompt sketch:** "Around late February, what was the single most important artifact that would help resume work without searching?"
- **what it stresses:** narrowing the search space using memory rather than broad summary
- **likely naive-system failure:** dumps a long recap instead of surfacing the one high-leverage object
- **why it matters in real use:** this is one of the most direct practical value surfaces in the lab

### P16
- **family:** contradiction detection
- **source:** `S03`
- **prompt sketch:** "On February 23, I'd already discussed a plan with evidence. Did the system lose track of it later that day?"
- **what it stresses:** noticing that the problem is not ignorance but contradiction with already-discussed evidence
- **likely naive-system failure:** restates the current answer without checking whether it conflicts with prior analysis
- **why it matters in real use:** users lose trust faster when the system confidently contradicts an established plan than when it simply says it is unsure

### P17a
- **family:** tool-chain explanation
- **source:** `S04`
- **prompt sketch:** "What was the replay work around Feb 25-26?"
- **what it stresses:** reconstructing a multi-step workflow rather than isolated artifacts
- **likely naive-system failure:** lists the files or actions separately and never explains the pipeline they formed
- **why it matters in real use:** memory is more useful when it can explain how artifacts and tools fit together, not just that they existed

### P17b
- **family:** tool-chain explanation
- **source:** `S04`
- **prompt sketch:** "How did memex evolution connect to routing-table work?"
- **what it stresses:** reconstructing a multi-step workflow rather than isolated artifacts
- **likely naive-system failure:** lists the files or actions separately and never explains the pipeline they formed
- **why it matters in real use:** memory is more useful when it can explain how artifacts and tools fit together, not just that they existed

### P18
- **family:** canonicalization retrieval
- **source:** `S04`
- **prompt sketch:** "If the user wanted one readable canonical place to understand that window, what object should the system point to first and why?"
- **what it stresses:** identifying the canonical artifact inside a noisy documentation/consolidation slice
- **likely naive-system failure:** gives a broad summary of everything instead of selecting the one route-setting object
- **why it matters in real use:** coherent work depends on knowing which artifact supersedes the rest
- **note:** stress-test probe -- high tool-call count expected

### P19
- **family:** coherence maintenance
- **source:** `S04` + `PRACTICAL_VALUE`
- **prompt sketch:** "On February 25-26, you updated the memex eight times and ran a coherence audit. Was this cleanup, or was the system's memory drifting from reality?"
- **what it stresses:** recognizing decision alignment, naming cleanup, and route maintenance as memory work
- **likely naive-system failure:** treats the slice as passive documentation rather than active coherence repair
- **why it matters in real use:** much of memory's practical value is preventing drift between docs, decisions, and current intent

### P20
- **family:** architecture trust-boundary
- **source:** `S05`
- **prompt sketch:** "When Hermes joined the workflow in late February, what information could only be recovered by looking across tools, not from Hermes alone?"
- **what it stresses:** distinguishing which questions exceed the scope of a single memory layer
- **likely naive-system failure:** over-trusts the newest provider memory surface and ignores cross-tool release/research overlap
- **why it matters in real use:** users need to know when a local memory looks complete but is actually missing the real cross-surface object

### P21
- **family:** scope-assumption trap
- **source:** `S05`
- **prompt sketch:** "If you only had Claude Code's view of the hermes-agent project in early March, you'd think it was stalled. What does the Hermes trace show instead?"
- **what it stresses:** exposure of hidden scope errors during memory-architecture change
- **likely naive-system failure:** describes the period accurately inside one tool but misses that the evaluation target has changed across tools
- **why it matters in real use:** many bad memory answers are locally plausible yet globally wrong because the scope boundary was misdrawn

### P22
- **family:** release-vs-research disentangling
- **source:** `S05`
- **prompt sketch:** "Separate the release/branch work from the memory-architecture research work in this window. Which threads belonged to which lane?"
- **what it stresses:** thread disentangling inside a mixed operational slice
- **likely naive-system failure:** merges release chores and architecture investigation into one generic progress report
- **why it matters in real use:** if memory cannot separate lanes, it cannot help a user resume the right one

### P25
- **family:** routing correction under noise
- **source:** `S05` + `S06`
- **prompt sketch:** "In late February and early March, I was juggling memory architecture, release prep, and research. Which one was actually driving the others?"
- **what it stresses:** routing discipline under overlapping and distractor-heavy context
- **likely naive-system failure:** answers everything at once or picks the loudest recent thread instead of the one that matches the user's real need
- **why it matters in real use:** routing quality is often the difference between immediate traction and another hour of drift
- **note:** may need narrower scoping

### P33
- **family:** timeline anchoring
- **source:** `S03` + `S04`
- **prompt sketch:** "Between February 23 and February 25-26, did the work change direction? What was the shift?"
- **what it stresses:** temporal anchoring and phase separation across nearby slices
- **likely naive-system failure:** merges the windows into one generic 'memory work' period and loses the before/after shift
- **why it matters in real use:** continuity requires knowing not just what happened, but when the object of work changed

### P35
- **family:** evidence provenance
- **source:** `S03` + `S07`
- **prompt sketch:** "Find a specific case between February and March where earlier analysis was available in the traces but was not surfaced when needed."
- **what it stresses:** provenance-aware recall rather than unsupported memory tone
- **likely naive-system failure:** says 'we discussed this before' without grounding the claim in a recoverable evidence source
- **why it matters in real use:** users trust remembered answers more when the system can show where the memory came from

### P41
- **family:** external-constraint carryover
- **source:** `S05` + rare-source traces
- **prompt sketch:** "Which external constraints or platform realities entered during this window and should keep shaping later decisions even after the local task changes?"
- **what it stresses:** carry-forward of constraints that outlive the moment they first appear
- **likely naive-system failure:** remembers the task but drops the constraint once the visible surface changes
- **why it matters in real use:** many repeated mistakes happen because systems forget the constraint and only remember the action

### P47
- **family:** contradiction repair
- **source:** `S03` + contradiction cases surfaced in `P16`
- **prompt sketch:** "On February 23, the system drifted away from an earlier plan. What specifically should have been preserved?"
- **what it stresses:** recovery behavior after contradiction detection, not just detection itself
- **likely naive-system failure:** apologizes vaguely or doubles down instead of rethreading the earlier evidence and restored plan
- **why it matters in real use:** users need repair, not just admission that drift happened

---

## 3. NE-1.3 probes (Mar 6 - Mar 16)

### P10
- **family:** cross-harness recall
- **source:** `S07` (`2026-03-13 -> 2026-03-14`)
- **prompt sketch:** "Map the threads we were trying to build yesterday and today across the different harnesses."
- **what it stresses:** same-user, many-harness continuity reconstruction
- **likely naive-system failure:** answers from one harness only or loses the cross-day merge
- **why it matters in real use:** this is one of the closest things to the real `n=1` problem statement in the corpus

### P11
- **family:** contract preservation
- **source:** `S07`
- **prompt sketch:** "On March 13-14 you asked the system to maintain many threads and keep going autonomously. What specifically was promised, and did it deliver?"
- **what it stresses:** preserving the implied contract to remember and reorganize the active work graph
- **likely naive-system failure:** answers with content, not obligation
- **why it matters in real use:** many continuity failures are broken contracts, not missing facts

### P13
- **family:** burst carryover
- **source:** `S08` (`2026-03-15 -> 2026-03-16`)
- **prompt sketch:** "A lot happened around March 14. What's still worth tracking and what can I ignore now?"
- **what it stresses:** post-spike stabilization and currentness
- **likely naive-system failure:** over-preserves everything or over-prunes everything
- **why it matters in real use:** memory quality after bursts matters more than memory quality on calm days

### P23
- **family:** medium-density coherence
- **source:** `S06` (`2026-03-07 -> 2026-03-12`)
- **prompt sketch:** "What was I actually working on during March 7-12, across all my tools? Was there a pattern forming?"
- **what it stresses:** maintaining coherence in a medium-density braid rather than only at obvious extreme spikes
- **likely naive-system failure:** ignores the corridor and jumps straight to the largest burst day, losing the setup arc
- **why it matters in real use:** real continuity depends on remembering buildup phases, not just headline events

### P26
- **family:** cross-harness disagreement reconciliation
- **source:** `S07`
- **prompt sketch:** "On March 13-14, I was using both claude-code and opencode. What was each one doing, and were they duplicating work or covering different ground?"
- **what it stresses:** reconciliation of partial but overlapping harness narratives
- **likely naive-system failure:** picks one harness as authoritative and silently discards the other's threads
- **why it matters in real use:** users often care about the merged work graph, not which runtime happened to say it better

### P27
- **family:** live-thread naming
- **source:** `S07` + `S08`
- **prompt sketch:** "Name the threads that deserved to stay live after the Mar 14 burst rather than becoming archived residue."
- **what it stresses:** preserving thread identity across a burst boundary
- **likely naive-system failure:** summarizes in vague categories and loses the concrete thread names or objectives that should carry forward
- **why it matters in real use:** users resume named work threads, not generic summaries like 'some architecture tasks'

### P28
- **family:** promise carry-forward
- **source:** `S07`
- **prompt sketch:** "On March 13 you asked the system to remember all the threads from yesterday and map the timeline. What threads should it have recovered, and which did it actually surface?"
- **what it stresses:** contract preservation across an explicit continuity request
- **likely naive-system failure:** repeats the timeline request but never operationalizes what a successful next-turn carry-forward would look like
- **why it matters in real use:** memory should preserve obligations, not just content blobs

### P30
- **family:** post-spike compaction
- **source:** `S08`
- **prompt sketch:** "What should a good memory system compress from the Mar 14 spike into a compact handoff for Mar 15-16, and what should it leave out?"
- **what it stresses:** selective compaction into a usable restart artifact
- **likely naive-system failure:** either reproduces a bloated recap or compresses so aggressively that the surviving live issues disappear
- **why it matters in real use:** the practical test is whether the day after a spike feels manageable without erasing the real work graph

### P31
- **family:** stale-summary rejection
- **source:** `S08`
- **prompt sketch:** "If I only read my March 14 summary, what would I get wrong about the state of things on March 16?"
- **what it stresses:** currentness judgments and recognition that summaries can go stale across just one or two days
- **likely naive-system failure:** treats the biggest prior summary as permanently canonical even when the live priorities have shifted
- **why it matters in real use:** memory should reduce wrong-direction work, not preserve yesterday's emphasis after it stops being useful

### P44
- **family:** priority extraction
- **source:** `S08`
- **prompt sketch:** "Out of everything alive after the Mar 14 spike, what were the top three priorities that most deserved attention next?"
- **what it stresses:** extracting actionable priority from a saturated work graph
- **likely naive-system failure:** returns a large unordered list or confuses importance with recency
- **why it matters in real use:** good memory should help users choose, not just remember more

### P45
- **family:** abandoned-thread detection
- **source:** `S06` + `S08`
- **prompt sketch:** "What was I working on in early-to-mid March that I ended up dropping? Which threads died?"
- **what it stresses:** distinguishing unfinished from still-relevant
- **likely naive-system failure:** keeps every unresolved thread in the live set forever
- **why it matters in real use:** stale-live threads create cognitive debt and make restart packets noisy

### P59
- **family:** system-health
- **source:** `S07` + `S08`
- **prompt sketch:** "After a large burst of work, did the memex actually advance with new information, or did synthesis stall?"
- **what it stresses:** detecting when the memory system itself fails to incorporate new information
- **likely naive-system failure:** reports the memex content as if it's current without checking if synthesis actually ran
- **why it matters in real use:** a memory system that stops learning is worse than one that never started

### P60
- **family:** reconstruction-completeness
- **source:** `S07`
- **prompt sketch:** "Reconstruct the full timeline of March 13-14 across all tools. Is the picture complete or are there gaps?"
- **what it stresses:** completeness of cross-harness reconstruction under high-volume conditions
- **likely naive-system failure:** returns a partial timeline from one tool and presents it as complete
- **why it matters in real use:** users need to know when their view is partial

### P61
- **family:** compaction-quality
- **source:** `S08`
- **prompt sketch:** "The March 14 spike generated massive amounts of trace data. What survived into the next day's working memory, and was anything important lost?"
- **what it stresses:** whether compaction preserves signal or drops important threads
- **likely naive-system failure:** keeps everything (no compaction) or drops too aggressively (loses signal)
- **why it matters in real use:** compaction under pressure is where memory systems fail in practice

---

## 4. Cross-dataset probes

These probes span two or more dataset windows.

### P24
- **family:** harness-braid explanation
- **source:** `S06`
- **prompt sketch:** "How were opencode and claude-code relating to each other in that Mar 7-12 period: duplicate effort, handoff, or complementary lanes?"
- **what it stresses:** explaining the relationship between parallel harness traces
- **likely naive-system failure:** either collapses the harnesses together or describes them as unrelated streams
- **why it matters in real use:** continuity breaks when the system cannot tell whether two traces are the same job, a handoff, or two different jobs

### P29
- **family:** rare-event recovery
- **source:** `S04` + `S07` + `S08`
- **prompt sketch:** "Which low-volume sources in these overlap-heavy slices were easy to flatten away but still changed the right interpretation of the work?"
- **what it stresses:** preserving rare but high-signal traces such as manual notes or github activity amid dominant harness traffic
- **likely naive-system failure:** ignores small-source traces because they are numerically tiny compared with opencode or claude bursts
- **why it matters in real use:** rare sources often contain the only explicit decision, correction, or external constraint that the big traces assume implicitly

### P34
- **family:** supersession tracking
- **source:** `S04` + `S08`
- **prompt sketch:** "Between late February and mid March, which documents or plans got replaced? What took their place?"
- **what it stresses:** recognizing that memory objects can become obsolete and need replacement pointers
- **likely naive-system failure:** preserves every prior artifact as equally live, forcing the user to decide what is stale
- **why it matters in real use:** a good memory system should reduce stale branching, not multiply it

### P38
- **family:** user-intent inference
- **source:** `S04` + `S07`
- **prompt sketch:** "When I kept asking about memory stuff in February and March, what was I actually trying to get to? What was the real goal?"
- **what it stresses:** recovering latent objective from superficially different requests
- **likely naive-system failure:** treats each request literally and misses the stable user preference underneath
- **why it matters in real use:** continuity systems should preserve what the user cares about, not only what they happened to type

### P39
- **family:** plan-vs-status separation
- **source:** `S03` + `S08`
- **prompt sketch:** "Separate what had already been decided as the plan from what had merely happened recently. Which items belong to plan, and which belong only to status?"
- **what it stresses:** distinction between durable intent and transient activity
- **likely naive-system failure:** treats the most recent activity as the plan, even when it was just execution noise or residue
- **why it matters in real use:** resumption quality depends on carrying the right durable object forward

### P40
- **family:** interrupt recovery
- **source:** `S06` + `S07`
- **prompt sketch:** "If the user was interrupted mid-braid and came back cold, what is the smallest restart packet that would let them re-enter without rereading the whole trace?"
- **what it stresses:** compact restart construction under ongoing multi-thread work
- **likely naive-system failure:** either gives an exhaustive recap or omits the key live branches and next-step hooks
- **why it matters in real use:** the restart packet is one of the most concrete tests of usable memory

### P42
- **family:** alias / naming resolution
- **source:** `S04` + `S06` + `S07`
- **prompt sketch:** "Were there things between February and March that I called by different names but were actually the same project?"
- **what it stresses:** thread identity resolution across renamings and local shorthand
- **likely naive-system failure:** either splits one thread into many names or merges separate threads because the vocabulary overlaps
- **why it matters in real use:** memory fails when it cannot track identity through normal human renaming behavior

### P43
- **family:** perspective shift
- **source:** `S02` + `S05`
- **prompt sketch:** "Explain this period once as a product-memory story and once as an operations/release story. What stays the same and what changes?"
- **what it stresses:** answering from the right viewpoint without losing core facts
- **likely naive-system failure:** gives one blended answer that is neither operationally useful nor conceptually clear
- **why it matters in real use:** the same trace often has to support different tasks, and memory needs viewpoint control

### P46
- **family:** handoff readiness
- **source:** `S04` + `S08`
- **prompt sketch:** "If a different agent had to take over after this window, what minimum handoff would preserve intent, constraints, and next step without replaying the whole archive?"
- **what it stresses:** transfer-ready summarization instead of owner-specific recall
- **likely naive-system failure:** preserves facts but drops the rationale, constraints, or next-step shape needed for takeover
- **why it matters in real use:** real memory systems often support handoff, not just self-resumption

### P48
- **family:** comparative routing diagnosis
- **source:** `S05` + `S07` + `S08`
- **prompt sketch:** "If someone needed to catch up on what happened from late February through mid March, what single thing should they read first?"
- **what it stresses:** comparative diagnosis of routing choices instead of one-surface endorsement
- **likely naive-system failure:** names a preferred surface without analyzing failure modes of the alternatives
- **why it matters in real use:** routing advice becomes stronger when it explains the cost of the wrong route

---

## 5. DROPPED probes

| ID | Reason |
|----|--------|
| P12 | Probe-set architecture question, not user continuity |
| P15 | Calibration question about slice redundancy, S01 also outside frozen bundles |
| P32 | Researcher causal-chain tracing, not user need |
| P37 | Epistemological caution -- valuable findings but belongs as calibration notes, not a scored probe |
| P49 | Pure benchmark engineering -- failure modes extracted into new probes P51-P53 |
| P50 | Portfolio analysis of the probe set itself, not user continuity |

---

## Summary

### Counts by dataset

| Dataset | Probes | Count |
|---------|--------|-------|
| NE-1.1 (Jan 9 - Feb 8) | P03, P04, P05, P36, P43, P51-P58 | 13 |
| NE-1.2 (Feb 8 - Mar 6) | P01, P02, P06, P07, P08, P09, P14, P16, P17a, P17b, P18, P19, P20, P21, P22, P25, P33, P35, P41, P47 | 20 |
| NE-1.3 (Mar 6 - Mar 16) | P10, P11, P13, P23, P26, P27, P28, P30, P31, P44, P45, P59, P60, P61 | 14 |
| Cross-dataset | P24, P29, P34, P38, P39, P40, P42, P43, P46, P48 | 10 |
| DROPPED | P12, P15, P32, P37, P49, P50 | 6 |
| **Total active** | | **55** |

Note: P43 appears in both NE-1.1 and Cross-dataset (source spans S02+S05). Counted once toward total.

### Counts by family

| Family | Probes | Count |
|--------|--------|-------|
| resumption-after-gap | P01, P52, P55 | 3 |
| forgotten-analysis recovery | P02 | 1 |
| decision archaeology | P03 | 1 |
| multi-agent reconstruction | P04 | 1 |
| architecture-comparison retrieval | P05 | 1 |
| practical-value / doc hygiene | P06 | 1 |
| latent constraint retrieval | P07 | 1 |
| source migration | P08 | 1 |
| routing under noise | P09 | 1 |
| cross-harness recall | P10 | 1 |
| contract preservation | P11 | 1 |
| burst carryover | P13 | 1 |
| search entropy reduction | P14 | 1 |
| contradiction detection | P16 | 1 |
| tool-chain explanation | P17a, P17b | 2 |
| canonicalization retrieval | P18 | 1 |
| coherence maintenance | P19 | 1 |
| architecture trust-boundary | P20 | 1 |
| scope-assumption trap | P21 | 1 |
| release-vs-research disentangling | P22 | 1 |
| medium-density coherence | P23 | 1 |
| harness-braid explanation | P24 | 1 |
| routing correction under noise | P25 | 1 |
| cross-harness disagreement reconciliation | P26 | 1 |
| live-thread naming | P27 | 1 |
| promise carry-forward | P28 | 1 |
| rare-event recovery | P29 | 1 |
| post-spike compaction | P30 | 1 |
| stale-summary rejection | P31 | 1 |
| timeline anchoring | P33 | 1 |
| supersession tracking | P34 | 1 |
| evidence provenance | P35, P51, P58 | 3 |
| uncertainty calibration | P36 | 1 |
| user-intent inference | P38 | 1 |
| plan-vs-status separation | P39 | 1 |
| interrupt recovery | P40 | 1 |
| external-constraint carryover | P41 | 1 |
| alias / naming resolution | P42 | 1 |
| perspective shift | P43 | 1 |
| priority extraction | P44, P53, P57 | 3 |
| abandoned-thread detection | P45 | 1 |
| handoff readiness | P46 | 1 |
| contradiction repair | P47 | 1 |
| comparative routing diagnosis | P48 | 1 |
| architecture-boundary | P54 | 1 |
| causal-diagnosis | P56 | 1 |
| system-health | P59 | 1 |
| reconstruction-completeness | P60 | 1 |
| compaction-quality | P61 | 1 |
| **Total families** | | **43** |
