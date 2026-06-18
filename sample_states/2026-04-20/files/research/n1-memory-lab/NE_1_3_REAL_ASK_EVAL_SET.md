# NE-1.3 Real Ask Eval Set

This is the canonical NE-1.3 eval-set design now.

The unit is not a neat benchmark question.
It is a real ask, tied to a real time, with real evidence surfaces.

## What changed

This replaces the half-finished split between:

- the `22`-item strict real-ask list
- the `10`-item real-ask eval draft
- and the older synthetic-style NE-1.3 probe set

The canonical set is:

- `50` real asks
- sampled to preserve the actual month shape
- still pruned for redundancy and contamination
- still bounded enough to judge carefully

## Temporal shape

The set keeps the lived NE-1.3 shape instead of flattening it.

| Window | Count |
|---|---:|
| `2026-03-07 -> 2026-03-12` | `4` |
| `2026-03-13 -> 2026-03-16` | `11` |
| `2026-03-17 -> 2026-03-22` | `9` |
| `2026-03-23 -> 2026-03-31` | `11` |
| `2026-04-01 -> 2026-04-10` | `15` |

This is deliberately tempered:

- not uniform by date
- not raw-frequency-slave
- not balanced by category

It keeps the early burst because that is where the core continuity pressure appears.
It also lets the later month dominate slightly, because real life and the object of work both moved there.

## Sampling stance

The sampler follows a few hard rules:

- keep raw user phrasing
- keep messy asks when they are real continuity burdens
- preserve repeated ask-shapes across time when the right answer changes later
- prune near-duplicates inside one local burst
- do not let local git choose the set
- do not force equal coverage buckets

The point is not neat coverage.
The point is life-like pressure with enough auditability to judge.

## Judge evidence

Every real-ask eval should be judged against:

- the raw slice around the ask
- the replay-time state at that moment
- the run traces
- the time-contained local git anchor

The git anchor is a judge-side truth surface.
It is not part of the ask-side sampling logic.

## What is measured

There are three reporting surfaces now.

### 1. Headline success

Use:

`Success Rate / Pass@1 = pass / total_judged`

`invalid` rows are excluded from the denominator.

This is the public headline.

### 2. Continuity quality

The judge reports two diagnostic axes:

- `factual_grounding`
- `continuity`

`continuity` intentionally absorbs:

- temporal correctness
- cross-source coherence
- practical continuation value

Those should not survive as separate headline-like fields.

### 3. Efficiency

The operational panel stays separate and telemetry-led:

- `zero_search_success_rate`
- `tool_calls_per_success`
- `cost_per_success`

That keeps A/B testing relevant:
did it succeed more often, and at what cost?

## Why this set is better

It captures the real object:

- current-state recovery
- thread-map recovery
- handoff and restart asks
- what changed since then
- concrete code/work-state truth asks
- replay/eval design asks where time containment itself becomes the issue

It also preserves the key NE-1.3 property:
the same shape of ask can have a different correct answer later.

That is not noise.
That is the memory problem.

## Canonical artifact

Use:

- `NE_1_3_REAL_ASK_EVAL_SET.yaml`

That file is the source of truth now.

Older iterative real-ask files have been moved under:

- `research/n1-memory-lab/archive/real-ask-history/`
