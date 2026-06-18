# S03 vs. LongMemEval

This memo compares `S03` (`2026-02-23`, the forgotten-plan resumption window) against **LongMemEval** using only local research artifacts.

Sources used:
- `research/n1-memory-lab/SLICE_CARDS_V1.md`
- `research/n1-memory-lab/SLICE_ATLAS_V0.md`
- `research/n1-memory-lab/REAL_VS_BENCHMARK_V0.md`
- `research/n1-memory-lab/SLICE_SCORECARD_V0.md`
- `research/omocon-talk/benchmark-data-notes.md`
- `research/memory-eval-landscape-2026.md`
- `research/internal-docs/history/REPLAY_SANDBOX.md`

## What S03 is, concretely

From the local slice docs, `S03` is a `2026-02-23` return-after-gap window with `6,899` events across `3` sources, dominated by `opencode`. Two anchor turns define the slice:
- `I just came back, what happened since then ?`
- `You forgot we discussed this and analyzed with data...`

That matters because the user is not merely asking for a buried fact. The user is asserting that:
1. prior work already exists,
2. prior work already included analysis and evidence,
3. the assistant should resume from that already-earned state rather than restart from scratch.

So the failure mode is not just recall failure. It is **continuity failure**: loss of the active plan, loss of the justification behind it, and loss of the user's expectation that this work was already in progress.

## What LongMemEval captures

Per the local benchmark notes, LongMemEval is a long-context memory benchmark built around one simulated user talking to one assistant over months. At the high level it tests five ability families, operationalized here as six scored categories plus abstention:
- `single-session-user` (`70` questions)
- `single-session-assistant` (`56` questions)
- `single-session-preference` (`30` questions)
- `multi-session` (`133` questions)
- `temporal-reasoning` (`133` questions)
- `knowledge-update` (`78` questions)
- plus `30` abstention questions

At a high level, that benchmark captures whether a system can:
- extract facts from long dialogue,
- recover what the user or assistant said,
- combine facts across sessions,
- reason about time and ordering,
- return the latest value after explicit updates,
- and refuse when the answer was never discussed.

That is real memory pressure. It is also the closest existing benchmark family to parts of `S03`.

## Precise mapping: S03 against LongMemEval categories

| LongMemEval category | What the benchmark captures | Relevance to `S03` | What `S03` still adds beyond it |
|---|---|---|---|
| `single-session-user` | recover a user-stated fact from one session | **Low-to-medium**. `S03` includes user statements like “I just came back...” and “you forgot...”, but those statements are not the main object. | In `S03`, the important thing is not the literal text of the latest user turn. It is the missing prior work state that the latest turn points back to. |
| `single-session-assistant` | recover something the assistant previously said | **Medium**. Resumption may require recalling a prior assistant conclusion or summary. | In `S03`, recalling prior assistant output is not enough; the assistant must recover whether that prior output reflected an already-adopted plan and evidence-backed analysis. |
| `single-session-preference` | recall explicit user preferences from one session | **Low**. Preference is not the central burden here. | `S03` is about plan continuity, not taste or standing preference recall. Treating it as preference would under-model the slice. |
| `multi-session` | combine facts from multiple sessions | **High**. The user returns after a gap and expects continuity across earlier work. | `S03` needs recovery of a *live analytic thread*, not just combination of facts. The system must identify what was settled, what remains open, and what the current task should resume from. |
| `temporal-reasoning` | when something happened, ordering, sometimes latestness | **Medium-to-high**. “What happened since then?” requires some before/after structure. | `S03` is not just about ordering events. It requires identifying the relevant cut point, then summarizing the delta while preserving older conclusions that should still stand. |
| `knowledge-update` | explicit state change: old value replaced by new value | **Medium**. Some of the user's expectation is “do not act as if earlier analysis never happened.” | Benchmark updates are usually clean overwrite tasks. `S03` instead involves implicit continuity state: a plan became live, analysis already existed, and that status should persist unless contradicted. |
| `abstention` | refuse when the answer was never discussed | **Necessary but not sufficient**. A safe answer to “what happened since then?” should avoid inventing unseen events. | Even perfect abstention does not solve the slice. The hard part is recovering the right prior thread without fabricating or flattening it. |

## What LongMemEval gets right for S03

LongMemEval is not the wrong comparison. It captures several real sub-skills that `S03` absolutely depends on:
- **cross-session recall**: the user expects the system to remember prior sessions;
- **temporal partitioning**: “since then” requires a boundary between earlier and later events;
- **latest-state handling**: the assistant must not answer from stale state if something changed;
- **safety via abstention**: the assistant should not invent events or claim analysis that never happened.

So an agent that fails LongMemEval badly will likely struggle on `S03` too.

## What S03 adds beyond LongMemEval

`S03` adds at least five burdens that are only weakly expressed, or not expressed at all, by benchmark-style QA.

### 1. The memory object is a **plan**, not just a fact

The user is effectively asking: *what was already in flight, what was already analyzed, and what should we continue now?*

That is different from retrieving:
- a name,
- a date,
- a latest scalar value,
- or a stored preference.

The missing object is an **active work state**.

### 2. The system must recover **justification**, not only conclusion

The slice card explicitly says the user objects that prior work was already “analyzed with data.” That means successful resumption must recover not just the answer, but the fact that the answer had already been justified.

A benchmark answer can be correct while still failing this requirement. Example:
- benchmark-style success: return the right latest value;
- real `S03` failure: return a plausible next step while omitting that the same conclusion was already reached from prior evidence.

From the user's perspective, that is still a costly failure because they must re-explain or re-verify.

### 3. The system must preserve the **continuity contract**

The user is not asking a cold question. The user is asserting an expectation: *you should already know where we were.*

So the assistant has to infer and honor a contract:
- this is a resumption turn,
- earlier work remains binding unless overturned,
- the correct default is continuation, not re-discovery.

LongMemEval mostly evaluates answer selection from history. `S03` evaluates whether the assistant recognizes that the conversation has resumed in medias res.

### 4. The hard part is **search-entropy reduction**

In practice the user cost here is not “the model gave one wrong fact.” It is that the user now has to:
- restate the context,
- regrep earlier work,
- restitch prior analysis,
- and re-establish what was already decided.

That operational burden is central in `S03`. It is mostly outside benchmark scoring, which usually collapses success to question-answer correctness.

### 5. The state change is often **implicit**, not a clean overwrite

LongMemEval knowledge-update questions are usually structured like: old fact in session 0, new fact in session 1, answer with the latest fact.

`S03` is tougher in a different way. The important update is often implicit:
- a discussion happened,
- analysis was completed,
- a plan became active,
- the user left and came back,
- the assistant should still treat that plan as live.

That is not a simple key-value overwrite. It is a continuity judgment.

## Why the real continuity burden is not reducible to retrieval/update tasks

A reductionist view would say: `S03` is just a bundle of benchmark subproblems — retrieve old facts, find the latest update, order the events, answer safely.

That decomposition is partly true but incomplete.

To succeed on `S03`, the system must do all of the following **together**:
1. detect that this is a resumption request rather than a fresh task,
2. identify the relevant prior thread,
3. recover the prior plan,
4. recover the evidence-backed reasoning behind that plan,
5. distinguish settled conclusions from still-open questions,
6. summarize the delta since the user's absence,
7. avoid inventing steps that did not occur,
8. respond in a way that lets work continue immediately.

Each step uses retrieval. But the total task is not equivalent to retrieval.

A system can retrieve the right snippets and still fail if it:
- surfaces the wrong thread,
- loses the fact that analysis was already completed,
- treats settled work as open,
- or gives a generic recap instead of a continuation-ready state.

That is why `S03` is better described as a **coherence and resumption** problem than a plain long-context recall problem.

## Adversarial-safe conclusion

The careful claim is not that LongMemEval is useless or irrelevant. The careful claim is narrower:

1. **LongMemEval captures real sub-skills that `S03` needs**, especially multi-session recall, temporal partitioning, latest-state handling, and abstention.
2. **LongMemEval does not fully specify the success condition for `S03`**, because `S03` turns on plan recovery, justification recovery, and continuity-contract preservation.
3. **Therefore the real burden in `S03` is not reducible to benchmark-style retrieval/update tasks**, even though those tasks are necessary components.

A benchmark can tell us whether a system remembers facts across long history.
`S03` asks a harder operational question:

> Can the system resume a live, already-analyzed thread after interruption in a way that saves the user from re-deriving the work?

That is the continuity burden the slice exposes.
