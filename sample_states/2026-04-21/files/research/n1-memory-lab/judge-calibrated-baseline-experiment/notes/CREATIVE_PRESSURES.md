# Creative Pressures

Status: pressure-test lenses for keeping the experiment ambitious and honest.

Use these before interpreting any baseline result as architecture evidence.
The goal is to stress the measurement instrument, not to pick the best memory
design prematurely.

## Skeptic Lens: What Would Make This Result Meaningless?

Questions:

- Could a `pass` reflect prompt compliance, judge generosity, or task easiness
  rather than useful memory?
- Could a `fail` reflect judge brittleness, ambiguous expected behavior, or
  packet formatting rather than memory absence?
- Does the bounded `zero` condition prove anything, or only establish that the
  task can be completed without the synthesis/control layer?
- Are `pass/partial/fail` labels being treated as truth instead of noisy
  observations?

Design effects:

- Add judge-disagreement notes and failure taxonomy beside scores.
- Preserve raw judge rationale, not just labels.
- Compare outcomes against `zero`, but do not assume nonzero improvement means
  architecture superiority.
- Require repeated or variant trials before claiming an effect.

## Falsifiability Lens: What Would Convince Us The Instrument Is Bad?

Questions:

- What result pattern would invalidate the checklist or judge rubric?
- If all systems score similarly, is that because memory does not matter, or
  because tasks do not discriminate?
- If `zero` performs well, what hypothesis does that falsify?
- If memory-heavy runs perform worse, can the instrument distinguish harmful
  memory from judge noise?

Design effects:

- Define pre-registered instrument-concern triggers, such as high instability,
  unstable repeated judgments, or no separation between intentionally degraded
  and enriched packets.
- Include negative controls where memory should not help.
- Include positive controls where a specific memory fact should clearly help.
- Treat surprising results as calibration findings first, product findings
  second.

## Ambition Lens: Is This Measuring The Thing We Actually Care About?

Questions:

- Does the experiment test memory as recall, or memory as better agency over
  time?
- Are we rewarding shallow fact insertion when the real goal is continuity,
  judgment, and prioritization?
- Does the benchmark capture scientific/creative work, or only neat assistant
  behavior?
- Would a powerful future Syke system look better under this checklist, or
  merely different?

Design effects:

- Add tasks where useful memory changes strategy, not just wording.
- Include longitudinal scenarios with evolving constraints.
- Score whether memory improves framing, prioritization, and avoidance of
  stale assumptions.
- Keep architecture ranking out of scope until the instrument can detect these
  higher-order effects.

## Product Lens: Would This Matter To A Real User?

Questions:

- Would the observed improvement reduce user repetition, prevent a mistake, or
  accelerate work?
- Is the memory useful at the right time, or merely present?
- Does the system respect bounded context and avoid dragging in irrelevant
  history?
- Does a partial pass correspond to an acceptable user experience?

Design effects:

- Annotate each test with user-visible value: saves repetition, preserves
  preference, catches constraint, maintains continuity, avoids regression.
- Separate technically recalled from productively used.
- Add nuisance penalties for irrelevant memory, overconfident personalization,
  or stale-context contamination.
- Treat `partial` as an observation requiring diagnosis, not a midpoint score
  with automatic meaning.

## Memory Maximalist Lens: What If Memory Should Be Much More Aggressive?

Questions:

- Are we under-testing memory because packets are too small, too clean, or too
  conservative?
- Would richer autobiographical/project memory produce qualitatively better
  answers?
- Are we penalizing ambitious memory use because the rubric favors minimalism?
- Where should the system infer unstated continuity from prior work?

Design effects:

- Include a maximal helpful memory variant with richer packet context.
- Add cases where synthesizing multiple memories is necessary.
- Score legitimate inference separately from hallucinated personalization.
- Compare bounded minimal memory against richer memory to learn where extra
  context starts helping or hurting.

## Benchmark Pessimist Lens: How Will This Benchmark Get Gamed?

Questions:

- Are examples too synthetic, making systems optimize for rubric cues?
- Can a model pass by pattern-matching expected judge language?
- Does the benchmark ignore rare but severe memory failures?
- Are we compressing memory quality into labels that erase important
  differences?

Design effects:

- Keep adversarial and messy cases in the suite.
- Rotate task phrasing while preserving underlying memory requirement.
- Log qualitative failure modes alongside labels.
- Avoid a single aggregate score during calibration; prefer slices and
  diagnostic dashboards.

## Judge Calibration Lens: Can We Trust The Observer?

Questions:

- Does the judge distinguish memory use from generally good reasoning?
- Are thresholds stable across semantically equivalent answers?
- Does the judge overvalue explicit mention of memory facts?
- Does the judge underrate subtle memory-informed behavior?

Design effects:

- Add judge anchor examples for `pass`, `partial`, `fail`, and
  `cannot_determine`.
- Use paired comparisons where only memory availability changes.
- Include blinded review where possible: judge should not know condition
  labels.
- Track judge rationales for evidence quality, not just final verdicts.

## Architecture Humility Lens: Are We Ranking Systems Too Early?

Questions:

- Are we interpreting measurement noise as architecture signal?
- Does the current suite validate the evaluator before testing retrieval,
  summarization, or storage designs?
- Which observed differences are large enough to justify architecture
  conclusions?
- What must be true before we compare designs?

Design effects:

- State explicitly: current goal is measurement-instrument validation.
- Treat architecture differences as provisional diagnostic signals only.
- Require calibration controls to behave as expected before ranking systems.
- Report confidence bands or repeated-trial stability before any design
  recommendation.

