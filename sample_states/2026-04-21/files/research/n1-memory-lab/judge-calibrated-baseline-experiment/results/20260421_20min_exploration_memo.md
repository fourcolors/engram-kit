# 2026-04-21 Timed Exploration Memo

Status: descriptive exploration only. No decisions. No architecture ranking.

Window started: `2026-04-21 10:54:10 PDT`.

Inputs:

- [20260421_calibration_subset_packets.json](./20260421_calibration_subset_packets.json)
- [20260421_calibration_subset_triage.md](./20260421_calibration_subset_triage.md)
- [20260421_high_priority_claim_audit.md](./20260421_high_priority_claim_audit.md)
- [20260421_exploration_counts.md](./20260421_exploration_counts.md)

## Scope

This pass explored existing artifacts. It did not change the protocol or make
architecture claims.

## Descriptive Counts

Calibration subset:

- `30` cells.
- `60` answer observations.
- Criterion referenceability: `medium=12`, `high=9`, `low=9`.
- Target slices: `tip=12`, `historical=9`, `landscape=6`, `both=3`.
- Retrieval character: `search-like=21`, `reconstruction-like=9`.

Judge-pair categories:

- GPT answers: `exact=13`, `adjacent=14`, `full_band=1`,
  `invalid_or_missing=2`.
- Opus answers: `exact=19`, `adjacent=9`, `full_band=2`.

Triage likely causes:

- `answer quality`: `16`.
- `rubric ambiguity`: `11`.
- `packet insufficiency`: `3`.

Claim-type mentions in the high-priority audit:

- `verified`: `50`.
- `contradicted`: `16`.
- `inferred`: `14`.
- `unsupported`: `10`.
- `uncheckable`: `7`.
- `speculative`: `1`.

## Cross Tabs

Referenceability vs judge-pair category:

- `high`: `exact=10`, `adjacent=6`, `invalid_or_missing=2`.
- `medium`: `exact=10`, `adjacent=11`, `full_band=3`.
- `low`: `exact=12`, `adjacent=6`.

Target slice vs judge-pair category:

- `tip`: `exact=15`, `adjacent=6`, `full_band=1`,
  `invalid_or_missing=2`.
- `historical`: `exact=11`, `adjacent=7`.
- `landscape`: `exact=5`, `adjacent=6`, `full_band=1`.
- `both`: `exact=1`, `adjacent=4`, `full_band=1`.

Condition vs judge-pair category:

- `production`: `exact=11`, `adjacent=7`, `full_band=1`,
  `invalid_or_missing=1`.
- `pure`: `exact=14`, `adjacent=5`, `full_band=1`.
- `zero`: `exact=7`, `adjacent=11`, `full_band=1`,
  `invalid_or_missing=1`.

## Length And Tool-Use Observations

Within this selected subset:

- Adjacent-disagreement answers are longer on average than exact-agreement
  answers: `3711` vs `2790` chars.
- Full-band disagreements are not simply short-output artifacts: mean length
  `3261` chars.
- Opus answers use more tools on average than GPT answers: `33.7` vs `20.2`.
- Higher tool use is not automatically higher agreement.

These are descriptive observations from the selected subset only.

## Full-Band / Invalid Examples

Full-band:

- `R03/pure`, GPT answer: GPT judge `fail`, Opus judge `pass`.
- `R05/production`, Opus answer: Opus judge `pass`, GPT-family judge `fail`.
- `R19/zero`, Opus answer: Opus judge `pass`, GPT-family judge `fail`.

Invalid/missing:

- `R14/production`, GPT answer: GPT judge `partial`, Opus judge `invalid`.
- `R14/zero`, GPT answer: GPT judge `partial`, Opus judge `invalid`.

## Exact Agreement Is Not Correctness

There are `9` cells where both answer families have exact paired-judge
agreement:

- `R05/pure`
- `R07/zero`
- `R08/production`
- `R08/pure`
- `R13/pure`
- `R15/pure`
- `R18/production`
- `R19/production`
- `R19/pure`

This is useful because some of these cells still appear in the high-priority
claim audit. For example:

- `R08/production` has exact agreement within each answer family, but the
  exploration pass still flags storage-state vs work-state confusion.
- `R19/production` has exact paired observations, but one answer source is a
  generation timeout and the other appears stale-thread selected.

Descriptive read: exact judge agreement is a stability observation, not a
correctness guarantee.

## R08 Exploration

The strongest live evidence surface points toward active Observe/repo work, not
only a static bootstrap store:

- The memex snapshot references `Observe Phase 2`, `Observe = pure capture`,
  and OpenCode as a missing adapter gap.
- The git-state surface shows active repo changes: branch ahead by commits,
  staged `syke/health.py`, and modifications in `syke/cli.py`, `syke/db.py`,
  `syke/memory/synthesis.py`, and `tests/test_persistence.py`.
- The bootstrap reading is supported only by the local store-count angle. It is
  weak as a description of the live work state.

Exploratory interpretation: R08 exposes storage-state vs work-state confusion.
It also shows why a handle-poor prompt can be valuable: the answer must choose
what "where are we now" means rather than searching for a named object.

## R03 Exploration

The `R03` full-band disagreement is partly explained by source priority:

- Git anchor latest commits before cutoff point to CLI/onboarding/provider-model
  resolution work at `17:20-18:49 PDT`.
- The `finalize_memex` rewrite appears earlier at `16:24 PDT`.
- Some judge reasoning foregrounds the later CLI/git evidence.
- Other judge reasoning foregrounds synthesis validation/live debugging status
  from transcript evidence.

Exploratory interpretation: `R03` is not just "which answer is better." It is a
source-priority conflict between committed recency and live validation state.

## R19 Exploration

R19 has split evidence surfaces:

- One surface supports an LM Studio / local LLM inference thread around Mac
  models and benchmarking.
- Another surface supports Syke sandbox/replay work: full-pipeline sandbox,
  empty-state replay, real-data ingest, synthesis cycles, and budget controls.

Exploratory interpretation: R19 is not a simple correctness cell. It is a
target-state ambiguity cell. The question asks "what happened last / most
recently," but available surfaces point to different plausible "last" threads
depending on source, time boundary, and direct-vs-background activity.

## R18 Exploration

R18 answers often reconstruct a plausible sandbox/replay design, but exact
dataset/date/count claims drift:

- Some answers distinguish observe/sense sandbox from memory replay sandbox.
- Some infer from directory names and run labels rather than direct evidence.
- Judges disagree around planned-vs-actual dataset and ablation setup detail.

Exploratory interpretation: R18 is low referenceability in the current packet.
It can support broad design recall better than exact numeric reconstruction.

## Slice Shape Check

Raw slice size for selected ambiguous probes:

- `R08`: `2995` files, including `2992` JSONL files, `2990` Claude Code files,
  `2` opencode files, and `2` adapter markdowns.
- `R18`: `4245` files, including `4242` JSONL files, `4238` Claude Code files,
  `3` opencode files, and `2` adapter markdowns.
- `R19`: `4245` files, including `4242` JSONL files, `4238` Claude Code files,
  `3` opencode files, and `2` adapter markdowns.

Descriptive read: these packets are not "thin" by raw file count. When the memo
uses "packet insufficiency," the issue appears to be evidence organization,
target ambiguity, or lack of a compact reference state, not simple absence of
raw traces.

R18 and R19 have the same slice shape because they share the same reference
date/window. This makes them useful as a contrast: different asks over the same
evidence surface can produce different ambiguity patterns.

## Phrase-Density Check

Simple substring counts across JSONL/markdown slice files:

| term | R08 hits / files | R18 hits / files | R19 hits / files |
|---|---:|---:|---:|
| `Observe Phase 2` | `1942 / 66` | `2487 / 130` | `2487 / 130` |
| `LM Studio` | `42 / 7` | `1100 / 34` | `1100 / 34` |
| `sandbox` | `1094 / 155` | `29595 / 564` | `29595 / 564` |
| `replay harness` | `0 / 0` | `852 / 80` | `852 / 80` |
| `finalize_memex` | `5519 / 222` | `15704 / 726` | `15704 / 726` |
| `adapter-as-compiler` | `39 / 9` | `40 / 10` | `40 / 10` |
| `where are we now` | `5 / 5` | `11 / 8` | `11 / 8` |

Descriptive read: several answer handles are extremely dense in the raw slice.
This supports separating retrieval/search surface from reconstruction quality
when interpreting these cells.

## Pattern Buckets

Rough overlapping buckets from triage and claim audit:

- Stale or wrong latest-thread selection: roughly a dozen cells.
- Numeric overprecision/count drift: roughly 6-7 cells.
- Unsupported durable-memory/persistence claims: roughly 5-6 cells.
- Packet insufficiency or non-reconstructable slices: roughly 4-5 cells.
- Storage-state vs work-state conflation: roughly 4-5 cells.
- Invented identifiers or overtrusted handles: roughly 3-4 cells.
- Generation timeout: one clear outlier.
- Boundary ambiguity: widespread across borderline rows.

## Repeat-Flip Overlap

Same-judge repeat flip counts overlap with the selected calibration cells:

- Opus four-call repeats: `R03`, `R04`, `R07`, `R11`, `R12`, `R14`, and
  `R15` each flipped in two condition cells.
- GPT-mini available repeats: `R03`, `R05`, `R11`, `R12`, `R13`, `R14`, and
  `R15` each flipped in two condition cells.
- Older `ab07` Opus repeats: `R03` flipped in three condition cells; `R07`,
  `R09`, `R14`, `R15`, and `R18` each flipped in two.

Descriptive read: the selected subset is not arbitrary. Several selected cells
come from probes that also show same-judge repeat instability.

## Unresolved Questions

- For R08, should "now" primarily mean live work state, durable store state, or
  a compound answer that names both?
- For R19, how should direct work, background automation, and adjacent personal
  project work be ordered?
- For R18, are exact dataset/date/count claims checkable enough from this packet
  to support more than `partial`?
- Across cells, when does overprecision become a factual failure versus a
  localized defect in an otherwise useful answer?
