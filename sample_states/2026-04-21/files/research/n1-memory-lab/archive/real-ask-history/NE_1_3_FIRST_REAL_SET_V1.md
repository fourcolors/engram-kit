# NE-1.3 First Real Set V1

This is the first compact real-ask eval set for NE-1.3.

Use it as the default first serious continuity/coherence set.

## Selected asks

1. **Where are we now?**
   Live-state recovery.

2. **Remember all the threads from yesterday and map yesterday/today**
   Temporal reconstruction and carry-forward across interruption.

3. **What is the updated thread map now?**
   Changed-state tracking instead of stale-state replay.

4. **What happened in the last session, and what must not be forgotten?**
   Handoff recovery and restart fidelity.

5. **What stayed live after the burst, and what is residue?**
   Entropy reduction under burst pressure.

6. **Can we get back to the previous thread?**
   Exact-thread resumption rather than decent recap.

## Why this set

This is the smallest set that still covers the main continuity burden:

- currentness
- temporal reconstruction
- state updates
- handoff fidelity
- live-vs-residue discrimination
- exact-thread resumption

It avoids overfitting to narrow implementation trivia while staying much more
real than the old benchmark-style probe surface.

## Judge packet reminder

For each item, the judge should get:

- `eval.json`
- `raw_evidence/`
- `git_anchor/`
- `run_traces/`

`TIMEBOX` and light orientation should live inside `eval.json`, not as
separate files.
