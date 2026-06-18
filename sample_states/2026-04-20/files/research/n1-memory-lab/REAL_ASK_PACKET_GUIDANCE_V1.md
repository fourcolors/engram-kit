# Real Ask Packet Guidance V1

This is the packet shape for real-ask continuity evals.

It is intentionally richer than the current benchmark packet because the judge
is agentic and should not have to rediscover every surface from scratch.

## Core rule

For each eval at time `t`, build a contained eval set with:

1. the real ask
2. the answer to judge
3. raw continuity evidence around `t`
4. a time-contained local git set up to `t`

The local git set is a **truth anchor** for code/work-state reality.
It is not the full coherence surface.

## Packet contents

### Required

- `probe`
  - `probe_id`
  - `question`
  - `family`
  - `reference_ts_local`
- `answer`
  - `text`
  - optional answer metadata
- `raw_context`
  - contained harness evidence around the ask time
- `local_git_set`
  - contained local git state up to that time
- `judge_brief`
  - what the answer needed to accomplish
  - what useful/partial/fail mean for this ask

### Optional later

- `externalized_state`
  - e.g. GitHub issue / PR / release anchors
  - useful but secondary to local git for now

## How the judge should use the local git set

The local git set helps answer:

- what code existed by time `t`
- what changed by time `t`
- what had already crossed from discussion into code
- what was reverted
- what was still only local and not externalized

It should **not** be treated as:

- the whole continuity object
- the whole rationale surface
- the only source of truth for user priorities or handoff quality

## Time containment

The local git set must be bounded at `t`.

No future commits.
No future tags.
No present-day branch assumptions injected into a past eval.

If historical branch-tip reconstruction is not trustworthy, omit it.
Use only the parts of local git that can be made time-safe.

## Practical implication

The packet should be strong enough that an agentic judge can:

- verify truthfulness against real code history
- compare that against the raw continuity slice
- still decide usefulness in terms of restoring the right live model

without being tricked into treating code history as the whole object.
