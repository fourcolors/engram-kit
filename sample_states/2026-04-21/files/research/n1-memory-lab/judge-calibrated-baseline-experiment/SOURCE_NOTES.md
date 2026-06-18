# Source Notes

Status: detailed paper-batch notes. Compact links live in
[PAPER_MAP.md](./PAPER_MAP.md).

These notes preserve what each source contributes to Syke's
judge-calibrated-baseline experiment.

## When Judgment Becomes Noise, `2509.20293`

Source: [arXiv](https://arxiv.org/abs/2509.20293)

- Core thesis: LLM judge benchmarks can look stable while measuring noise if
  the rubric weakly ties to the verdict, factors collapse, or aggregation hides
  variance.
- Math: schema adherence regresses overall verdict on factor scores and uses
  `max(R2_linear, R2_poly)`.
- Transfer: run schema adherence and factor-collapse diagnostics before trusting
  aggregate verdicts.
- Caveat: numeric thresholds are not universal laws.

## Rethinking Rubric Generation / RRD, `2602.05125`

Source: [arXiv](https://arxiv.org/abs/2602.05125)

- Core thesis: broad open-ended rubrics should be recursively decomposed,
  filtered for misalignment/redundancy, and weighted with correlation awareness.
- Math: misclassification bound uses `Delta_m = w^T mu` and
  `V_m = w^T Sigma w`; whitened-uniform weights use
  `w_wu proportional to Sigma^(-1/2) 1`.
- Transfer: decompose, prune redundant axes, and avoid naive averaging.

## CyclicJudge, `2603.01865`

Source: [arXiv](https://arxiv.org/abs/2603.01865)

- Core thesis: judge bias is a separate variance term; round-robin cycling can
  cancel fixed judge bias at fixed call budget.
- Model: `X_ijL = mu + alpha_i + beta_ij + gamma_L + epsilon_ijL`.
- Transfer: use later as panel collection design after rubric stability.
- Caveat: not a truth guarantee.

## Bias-Bounded Evaluation, `2603.05485`

Source: [arXiv](https://arxiv.org/abs/2603.05485)

- Core thesis: define local average bias-boundedness for a fixed context and
  perturbation generator.
- Math: estimate RMS sensitivity over neighbors, then add calibrated Gaussian
  noise for a local `(tau, delta)` guarantee.
- Transfer: later sensitivity wrapper for explicit perturbation families.
- Caveat: local guarantee only; does not prove correctness.

## Criterion-Referenceability, `2603.14732`

Source: [arXiv](https://arxiv.org/abs/2603.14732)

- Core thesis: judge validity tracks how criterion-referenceable the task is,
  not raw judge model strength.
- Protocol: compare blind, correct-reference, and corrupted-reference
  conditions; report calibration and rank-order metrics.
- Transfer: label each Syke probe by referenceability and do not trust low
  referenceability cells as objective labels.

## No Free Labels, `2503.05061`

Source: [arXiv](https://arxiv.org/abs/2503.05061)

- Core thesis: without verified references, judge agreement is high mainly on
  questions the judge can already answer.
- Protocol: compare no reference, self reference, human reference, wrong
  reference, and random reference; swap pairwise order.
- Transfer: build verified references for a calibration subset; do not trust
  self-generated references without checks.

## RULERS, `2601.08654`

Source: [arXiv](https://arxiv.org/abs/2601.08654)

- Core thesis: lock the rubric, force evidence-grounded scoring, and calibrate
  output scale.
- Protocol: compile immutable rubric bundle, emit checklist decisions plus
  verbatim evidence, string-check quotes, normalize checklist scores, calibrate
  distributions with human labels.
- Transfer: strongest immediate protocol pattern for Syke.

## Trust or Escalate, `2407.18370`

Source: [arXiv](https://arxiv.org/abs/2407.18370)

- Core thesis: estimate confidence, abstain or escalate when confidence is low,
  and calibrate the threshold.
- Protocol: selective evaluation with calibration-set threshold selection;
  cascaded stronger judges when earlier judges abstain.
- Transfer: add `needs_human_review` / escalation instead of forcing verdicts.

## Rating Roulette, `2510.27106`

Source: [arXiv](https://arxiv.org/abs/2510.27106)

- Core thesis: same LLM judge can be materially self-inconsistent.
- Protocol: repeat same judge on same items; report chance-corrected agreement
  such as Krippendorff alpha.
- Transfer: same-judge repeats are mandatory before inter-judge claims.

## Grading Scale Impact, `2601.03444`

Source: [arXiv](https://arxiv.org/abs/2601.03444)

- Core thesis: grading scale changes human-LLM alignment; 0-5 worked best in
  their setting.
- Transfer: treat scale as a calibration variable; do not assume
  `pass/partial/fail` is optimal.

## Conformal Judge Intervals, `2509.18658`

Source: [arXiv](https://arxiv.org/abs/2509.18658)

- Core thesis: judge should return calibrated prediction intervals, not only
  point scores.
- Protocol: extract rating-token probabilities, fit split conformal on held-out
  calibration data, snap interval endpoints to legal ordinal scores.
- Transfer: later, once calibration data and exchangeability are plausible.

## Judgment Distribution, `2503.03064`

Sources: [arXiv](https://arxiv.org/abs/2503.03064),
[ACL](https://aclanthology.org/2025.findings-emnlp.1259/)

- Core thesis: use the full score-token distribution; mean decoding can beat
  greedy/mode.
- Math: `E[score] = sum_k k * p(k | prompt)`.
- Transfer: preserve logprobs if possible; avoid reducing too early to argmax.

## PSN-IRT / Lost in Benchmarks, `2505.15055`

Source: [arXiv](https://arxiv.org/abs/2505.15055)

- Core thesis: benchmarks saturate and fail to separate strong models; IRT can
  estimate item quality and model ability.
- Protocol: estimate ability, discriminability, difficulty, guessing, and
  feasibility; use Fisher information / headroom for item selection.
- Transfer: later, for anchor item quality once labels are stable.

## Construct Validity, `2511.04703`

Source: [arXiv](https://arxiv.org/abs/2511.04703)

- Core thesis: benchmark validity depends on precise construct definition,
  representative sampling, contamination control, uncertainty, and error
  analysis.
- Transfer: outer checklist for the whole experiment.

## LLM-Rubric, `2501.00274`

Sources: [arXiv](https://arxiv.org/abs/2501.00274),
[ACL](https://aclanthology.org/2024.acl-long.745/)

- Core thesis: single overall LLM score is too blunt; use per-question rubric
  distributions and calibrate to judges.
- Protocol: train a small feed-forward calibration net with judge-specific and
  shared parameters; decode by calibrated mean.
- Transfer: judge-specific calibration, not raw averaging.

## Likert or Not, `2505.19334`

Source: [arXiv](https://arxiv.org/abs/2505.19334)

- Core thesis: pointwise ordinal scoring can be competitive with listwise
  ranking when the scale is appropriate.
- Transfer: start simple with pointwise scoring; require evidence before
  switching to listwise/tournament judging.

## Autorubric, `2603.00077`

Source: [arXiv](https://arxiv.org/abs/2603.00077)

- Core thesis: analytic rubrics with atomic criteria are more auditable than a
  holistic score.
- Math: `score = clamp(0,1, sum(v_i w_i) / sum(w_i > 0))`.
- Transfer: one construct per criterion, separate criterion calls, explicit
  `CANNOT_ASSESS`.

## AdaRubric, `2603.21362`

Source: [arXiv](https://arxiv.org/abs/2603.21362)

- Core thesis: agent tasks may require task-specific orthogonal rubric
  dimensions.
- Protocol: task-conditioned rubric dimensions, 1-5 anchors, per-step scores
  and confidence, weighted aggregation.
- Transfer: useful for heterogeneous future task families, but baseline rubrics
  must be frozen before scoring.

## Rubric-Conditioned Grading, `2601.08843`

Source: [arXiv](https://arxiv.org/abs/2601.08843)

- Core thesis: explicit rubric prompts, repeated judgments, consensus
  thresholds, and deferral improve reliability; fine granularity can hurt.
- Transfer: add deferral and perturbation robustness tests.

## Correlated Errors in LLMs, `2506.07962`

Source: [arXiv](https://arxiv.org/abs/2506.07962)

- Core thesis: LLM errors are correlated even across providers/families.
- Transfer: judge diversity must be measured, not assumed.

## KalshiBench, `2512.16030`

Source: [arXiv](https://arxiv.org/abs/2512.16030)

- Core thesis: calibration is distinct from accuracy.
- Metrics: Brier score, Brier Skill Score, ECE, MCE, overconfidence.
- Transfer: use if Syke judge emits probabilities over binary/verifiable labels.

## Robustness And Reliability, `2509.04013`

Source: [arXiv](https://arxiv.org/abs/2509.04013)

- Core thesis: fixed benchmark wording overstates capability.
- Transfer: paraphrase robustness and rank stability checks.

## Growing Pains / Fixed Parameter IRT, `2604.12843`

Source: [arXiv](https://arxiv.org/abs/2604.12843)

- Core thesis: freeze calibrated item parameters and calibrate new items against
  anchors to keep scores comparable over time.
- Transfer: later, once Syke has a stable anchor set.

## Beyond Consensus, `2510.11822`

Source: [arXiv](https://arxiv.org/abs/2510.11822)

- Core thesis: LLM judges can be biased toward saying "valid"; majority vote is
  weak.
- Math: estimate generator precision and validator TPR/TNR.
- Transfer: track false-positive/false-negative bias, not only agreement.

## Self-Preference Bias, `2604.06996`

Source: [arXiv](https://arxiv.org/abs/2604.06996)

- Core thesis: judges favor own or same-family outputs even under rubrics.
- Transfer: measure self/family overestimation.

## Imperfect Verifier, `2604.07666`

Source: [arXiv](https://arxiv.org/abs/2604.07666)

- Core thesis: imperfect verifiers can still be useful; precision matters more
  than recall.
- Transfer: do not wait for oracle-perfect verification; measure noise and keep
  high-precision gates.

## PoLL / Juries, `2404.18796`

Source: [arXiv](https://arxiv.org/abs/2404.18796)

- Core thesis: panels of diverse judges can be cheaper and more robust than one
  big judge.
- Transfer: useful after measuring shared bias; not truth by itself.

## SCOPE, `2602.13110`

Source: [arXiv](https://arxiv.org/abs/2602.13110)

- Core thesis: pairwise judges should abstain when uncertain; conformal
  calibration bounds accepted-set error under assumptions.
- Transfer: future pairwise risk-control method with calibration labels.

## MemoryArena, `2602.16313`

Sources: [arXiv](https://arxiv.org/abs/2602.16313),
[project](https://memoryarena.github.io/)

- Core thesis: memory should be evaluated in multi-session action loops.
- Transfer: test whether earlier memory changes future decisions.

## LongMemEval, `2410.10813`

Sources: [arXiv](https://arxiv.org/abs/2410.10813),
[project](https://xiaowu0162.github.io/long-mem-eval/)

- Core thesis: long-term memory needs retrieval, updating, temporal reasoning,
  and abstention.
- Transfer: separate retrieval quality from answer quality and include
  unsupported-question abstention.

## LifeBench, `2603.03781`

Sources: [arXiv](https://arxiv.org/abs/2603.03781),
[repo](https://github.com/1754955896/LifeBench)

- Core thesis: long-horizon memory benchmarks should include multi-source and
  non-declarative inference over traces.
- Transfer: include long-horizon, cross-source, update-aware probes.

## OSWorld, `2404.07972`

Sources: [arXiv](https://arxiv.org/abs/2404.07972),
[project](https://os-world.github.io/)

- Core thesis: agent benchmarks should use real environment setup and
  execution-based evaluation when possible.
- Transfer: use executable/state-based checks before LLM judgment when possible.

## Evaluating the Evaluator, `2408.08781`

Source: [arXiv](https://arxiv.org/abs/2408.08781)

- Core thesis: more rubric text often helps less than expected.
- Transfer: compare minimal-prompt and full-rubric judge variants before
  expanding rubric detail.

## LLM-as-a-Verifier Project

Source: [GitHub](https://github.com/llm-as-a-verifier/llm-as-a-verifier)

- Status: official project/repo lineage found; no formal paper found in this
  pass.
- Transfer: verifier protocol pattern: criteria decomposition, repeated checks,
  pairwise wins.

