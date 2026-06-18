# S07 vs. LoCoMo and LifeBench

This memo compares `S07` (`2026-03-13 -> 2026-03-14`, the cross-harness recall-under-pressure slice) against **LoCoMo** and **LifeBench** using only local project files.

Sources used:
- `research/n1-memory-lab/SLICE_CARDS_V1.md`
- `research/n1-memory-lab/SLICE_ATLAS_V0.md`
- `research/n1-memory-lab/ARCHITECTURE_CASES_V0.md`
- `research/n1-memory-lab/archive/benchmark-legacy/PROBE_SEEDS_V1.md`
- `research/n1-memory-lab/REAL_VS_BENCHMARK_V0.md`
- `research/n1-memory-lab/CORPUS_BASELINE.md`
- `research/omocon-talk/benchmark-data-notes.md`
- `research/memory-eval-landscape-2026.md`
- `research/omocon-talk/honest-comparison-notes.md`

## What S07 is, concretely

From the local slice docs, `S07` is the `2026-03-13 -> 2026-03-14` window with `58,407` events across `5` sources.
By day:
- `2026-03-13`: `12,433` events
- `2026-03-14`: `45,974` events

Source mix:
- `claude-code 50,717`
- `opencode 6,402`
- `hermes 1,208`
- `manual 64`
- `github 16`

The slice card and atlas make three facts explicit:
1. both `claude-code` and `opencode` contain a direct request to remember the threads from yesterday/today,
2. the traces show explicit syke-skill usage,
3. the window is a massive burst with harness overlap rather than one bounded conversation.

So the target is not “answer one buried question from history.”
The target is: **reconstruct the active work graph across multiple harnesses while the operator is under continuity pressure**.

That means success requires at least:
- cross-day reconstruction,
- cross-harness merging,
- recovery of which threads are live versus residue,
- provenance awareness about which harness saw what,
- and a continuation-ready output that saves the user from re-briefing the system.

## What LoCoMo captures

Per the local benchmark notes, LoCoMo is a long-memory dialogue benchmark with:
- `10` simulated conversations,
- `272` sessions,
- `5,882` turns,
- about `182K` total tokens,
- `1,986` questions,
- `42%` multi-hop questions,
- `22.5%` adversarial questions,
- `16.2%` temporal questions,
- two simulated speakers per conversation,
- and an average of about `18K` tokens per conversation.

Operationally, LoCoMo captures whether a system can:
- recover facts from a long multi-session dialogue,
- combine information across sessions,
- reason about time/order,
- and avoid attribution mistakes such as confusing which speaker experienced an event.

That is real memory pressure.
It is also the closest benchmark denominator for the **dialogue-style** sub-skills inside `S07`.

## What LifeBench captures

Per the same local benchmark notes, LifeBench is a synthetic year-in-the-life benchmark with:
- `10` synthetic users,
- `2,003` questions,
- a full year per user,
- `9` data sources per user,
- about `4,878` daily events per user,
- multi-source questions that combine sources like SMS + notes + calendar,
- and `19%` of questions targeting habitual/procedural knowledge that is never explicitly stated.

Operationally, LifeBench captures whether a system can:
- integrate across multiple heterogeneous sources,
- recover events over longer temporal spans,
- infer routines or habits that are implicit rather than directly declared,
- and answer questions that no single source can answer alone.

Of the major benchmarks in the local notes, LifeBench is the closest denominator for the **multi-source** part of `S07`.

## Precise mapping: which benchmark abilities actually touch S07

| Ability | LoCoMo | LifeBench | Relevance to `S07` | What `S07` adds beyond the benchmark ability |
|---|---|---|---|---|
| Multi-hop / combine evidence | Strong (`42%` multi-hop) | Strong (cross-source questions) | **High** | `S07` needs not just combined evidence but a stitched **operator work graph** across harnesses. |
| Temporal reasoning | Present (`16.2%`) | Present | **High** | `S07` needs yesterday/today partitioning plus thread carryover judgments under a burst, not just event ordering. |
| Source / speaker attribution | Strong adversarial speaker attribution | Moderate via source-aware integration | **Medium-to-high** | In `S07`, provenance is about **which harness saw which thread** and whether one harness is reporting a local story as if it were global truth. |
| Cross-source integration | Absent | Core ability | **High** | `S07` sources are not passive modalities; they are active agent harnesses producing plans, tool traces, and memory attempts. |
| Non-declarative / habitual knowledge | Absent | Core ability (`19%`) | **Low-to-medium** | LifeBench tests a broader habit/routine object that `S07` does not fully cover. `S07` is not a substitute for that ability. |
| Abstention / adversarial safety | Strong | Weak/implicit | **Necessary but insufficient** | `S07` also needs safe handling of partial cross-harness visibility and explicit separation between known global state and one-harness inference. |
| Continuation-ready output | Not the benchmark target | Not the benchmark target | **Central in `S07`** | `S07` cares whether the answer actually helps resume work without re-briefing. |

## What LoCoMo gets right for S07

LoCoMo is relevant because `S07` absolutely depends on several of its tested sub-skills:
- **multi-session recall**,
- **multi-hop composition**,
- **temporal reasoning**,
- **attribution discipline**,
- and **adversarial restraint** when the evidence does not support a confident answer.

A system that fails LoCoMo badly is unlikely to do well on `S07` either.

### What S07 adds beyond LoCoMo

`S07` adds at least five burdens that LoCoMo does not really express.

### 1. One bounded dialogue becomes many overlapping harness views

LoCoMo assumes one conversation object with two speakers and one designed surface of truth.
`S07` instead contains `claude-code`, `opencode`, `hermes`, `manual`, and `github` traces inside one window.

That matters because the system must infer:
- which traces refer to the same underlying thread,
- which harnesses are duplicating the same continuity request,
- and where one harness has only a partial view.

That is not just “more multi-hop.”
It is a change in object type.

### 2. The required output is a work graph, not a QA answer

LoCoMo evaluates question answering over annotated ground truth.
`S07` asks for a map of “the threads we were trying to build yesterday and today.”

That means success depends on:
- surfacing active threads,
- grouping related work,
- separating live work from residue,
- and presenting a continuation-ready structure.

A system could answer many LoCoMo-style questions correctly and still fail this if it cannot organize the day into a usable work graph.

### 3. Provenance is not just speaker attribution

LoCoMo adversarial pressure often looks like “did Caroline do this or did Melanie do this?”
That is useful.

But `S07` provenance pressure is different:
- did this thread appear in `claude-code` only,
- did `opencode` independently ask the same continuity question,
- did `hermes` or `manual` add disambiguating evidence,
- and is the current answer global or merely harness-local?

That is closer to **scope attribution** than speaker attribution.

### 4. The traces are agentic, not just conversational

In LoCoMo, the conversation is the memory object.
In `S07`, the traces include skill usage and tool-heavy agent activity.
The harnesses are not passive recorders of a life story; they are active participants in the work.

So the system must sometimes reason over:
- prompts,
- tool traces,
- summaries generated inside harnesses,
- and explicit memory-surface usage.

That is qualitatively different from remembering who said what in a long friendship dialogue.

### 5. Architecture discrimination is part of the slice

The local slice docs repeatedly frame `S07` as a same-data comparison surface for:
- native memory,
- provider/plugin memory,
- and federated continuity.

LoCoMo does not directly test whether the failure came from a harness boundary versus a general recall limitation.
`S07` does.

That makes `S07` useful not just as a difficulty spike, but as an **architecture diagnostic**.

## What LifeBench gets right for S07

LifeBench is the better comparison if the question is: “which benchmark is closest to real multi-source continuity?”
It captures several things that matter for `S07`:
- **multi-source integration**,
- **temporal reasoning over a larger activity surface**,
- **questions whose answer is not contained in one source alone**,
- and the fact that memory can require reconstructing a life situation rather than extracting one sentence.

So if LoCoMo is the closest dialogue denominator, LifeBench is the closest source-integration denominator.

### What S07 adds beyond LifeBench

`S07` is still a different object from LifeBench in at least six concrete ways.

### 1. The sources are real harnesses, not synthetic life modalities

LifeBench sources are things like SMS, notes, calendar, contacts, photos, and health logs.
Those are heterogeneous, but they are mostly **observational**.

`S07` sources are AI harnesses plus manual/github traces.
These are partly observational and partly **interventional**:
- the harnesses are already trying to interpret the work,
- they may summarize or reshape the project state,
- and they can import their own local memory behavior into the trace.

That makes source fusion harder in a different way.

### 2. The task is cross-harness continuity, not general life reconstruction

LifeBench asks questions like what dinner topics were discussed, or what habits a synthetic user likely has.
That is broad and important.

`S07` asks a narrower but different question:
- what are the active project threads,
- across yesterday and today,
- across multiple AI work surfaces,
- in a way that supports immediate continuation.

So `S07` does **not** subsume LifeBench.
It stresses a different continuity object.

### 3. Ground truth is more open-ended

LifeBench is still benchmark-shaped:
- curated synthetic users,
- fixed sources,
- fixed questions,
- fixed answers.

`S07` has local replay facts, but the success condition is not reducible to one short canonical answer.
A good answer has to choose:
- what counts as a thread,
- what is actually live,
- how to merge duplicates,
- and how much uncertainty to preserve.

That makes evaluation more like structured reconstruction than closed-form QA.

### 4. Continuity obligation is explicit in S07

In LifeBench, the user does not directly pressure the system with “remember all the threads from yesterday and today.”
The benchmark asks the question from outside.

In `S07`, the continuity obligation is part of the trace itself.
That matters because the system is not merely being tested after the fact; it is being asked, in the moment, to preserve continuity under load.

### 5. Burst structure matters

The local corpus baseline shows a jump from `12,433` events on `2026-03-13` to `45,974` on `2026-03-14`.
That sharp burst is part of the slice.

LifeBench is temporally large, but it does not primarily test the question:
- can you recover the right live project graph the morning of or during a giant multi-harness spike?

That kind of overload-and-resume pressure is central in `S07`.

### 6. The evaluation target is reduced operator burden

LifeBench scores answer correctness.
`S07` also cares about whether the memory surface reduces search and re-brief burden.

A plausible answer that forces the user to restate the project map is still a practical failure in `S07`.
That practical-value criterion is only weakly represented in benchmark scoring.

## Where real cross-harness continuity remains a different object

The narrow claim is not “`S07` is simply harder than LoCoMo and LifeBench.”
That would be sloppy.

The better claim is that real cross-harness continuity remains a **different object of evaluation**.
Here is the precise difference.

### 1. The object is a shared work graph

Benchmarks mostly evaluate whether the system can answer a question from memory.
`S07` evaluates whether the system can recover a **shared, live project graph**.

That graph includes:
- threads,
- their relations,
- their current status,
- which harnesses touched them,
- and what should happen next.

### 2. Truth is distributed and partially perspective-bound

In LoCoMo and LifeBench, the benchmark designer ultimately defines the source package and answer key.
In `S07`, each harness has a local perspective and none is guaranteed to be the full picture.

So the system must distinguish:
- local evidence,
- cross-harness evidence,
- and inference that should be marked as uncertain.

### 3. The sources are themselves memory-bearing systems

This is the deepest object shift.
In `S07`, the sources are not just notes about a world.
They are other agent systems with their own memory surfaces, summaries, omissions, and routing behaviors.

So the system is not merely remembering across sources.
It is remembering across **competing partial reconstructions** of the same work.

### 4. Success is operational, not only factual

A benchmark answer can be correct and still operationally useless.
For `S07`, success means the user can continue work with less re-grepping, less re-briefing, and less risk of one-harness-local confusion being presented as the whole story.

### 5. Scope boundaries are part of the task

The slice docs explicitly contrast native, provider/plugin, and federated memory surfaces.
That means part of the real problem is knowing **which memory layer can legitimately answer which question**.

Benchmarks mostly treat memory as a single evaluated system.
`S07` exposes scope and routing as part of the object.

## Adversarial-safe conclusion

The careful conclusion is four-part.

1. **LoCoMo captures real sub-skills that `S07` needs**: multi-hop recall, temporal reasoning, attribution discipline, and adversarial restraint.
2. **LifeBench captures the closest benchmark sub-skills to `S07`'s multi-source burden**: cross-source integration and some implicit reconstruction from heterogeneous evidence.
3. **`S07` still adds something neither benchmark fully captures**: cross-harness reconstruction of a live operator work graph where the sources are themselves agentic, partial, and scope-bound memory surfaces.
4. **Therefore benchmark success is relevant but insufficient evidence for cross-harness continuity success**.

Just as important, the reverse is also true:
- `S07` does not replace LoCoMo's clean dialogue attribution tests,
- and it does not replace LifeBench's broader non-declarative, year-scale life-memory tests.

So the right claim is not benchmark supremacy.
The right claim is complementarity:

> LoCoMo and LifeBench measure necessary memory abilities. `S07` exposes a different continuity object: preserving and reconstructing the user's active cross-harness work graph under real operator pressure.
