# Paper Map

Status: collected from the April 2026 paper sweep and agent review batches.

Each source below should map to at least one checklist item in
[EXPERIMENT_CHECKLIST.md](./EXPERIMENT_CHECKLIST.md).

## Core Judge And Rubric Papers

| Paper | Source | Transfer To Syke |
|---|---|---|
| When Judgment Becomes Noise, `2509.20293` | [arXiv](https://arxiv.org/abs/2509.20293) | Schema adherence, factor collapse, aggregation masking. Use to test whether rubric axes explain verdicts. |
| Rethinking Rubric Generation / RRD, `2602.05125` | [arXiv](https://arxiv.org/abs/2602.05125) | Recursively decompose broad rubrics, prune redundant criteria, weight by residual/correlation-aware signal. |
| RULERS, `2601.08654` | [arXiv](https://arxiv.org/abs/2601.08654) | Locked rubric, evidence extraction, schema-constrained scoring, calibration. |
| Evaluating the Evaluator, `2408.08781` | [arXiv](https://arxiv.org/abs/2408.08781) | More rubric text is not automatically better. Compare minimal vs full rubric. |
| Autorubric, `2603.00077` | [arXiv](https://arxiv.org/abs/2603.00077) | Atomic analytic criteria, separate criterion calls, explicit unassessable path. |
| AdaRubric, `2603.21362` | [arXiv](https://arxiv.org/abs/2603.21362) | Task-specific dimensions for heterogeneous agent tasks. Use diagnostically unless frozen. |
| Rubric-Conditioned Grading, `2601.08843` | [arXiv](https://arxiv.org/abs/2601.08843) | Coarser labels, consensus threshold, deferral, robustness perturbations. |
| LLM-Rubric, `2501.00274` | [arXiv](https://arxiv.org/abs/2501.00274), [ACL](https://aclanthology.org/2024.acl-long.745/) | Per-dimension rubric scoring and judge-specific calibration heads. |

## Judge Reliability, Bias, And Panels

| Paper | Source | Transfer To Syke |
|---|---|---|
| Rating Roulette, `2510.27106` | [arXiv](https://arxiv.org/abs/2510.27106) | Same-judge reruns are mandatory; report intra-rater reliability. |
| CyclicJudge, `2603.01865` | [arXiv](https://arxiv.org/abs/2603.01865) | Judge identity as a variance term; round-robin judge assignment after rubric is stable. |
| Bias-Bounded Evaluation, `2603.05485` | [arXiv](https://arxiv.org/abs/2603.05485) | Local sensitivity bounds under explicit perturbation families. Later method. |
| Replacing Judges with Juries / PoLL, `2404.18796` | [arXiv](https://arxiv.org/abs/2404.18796) | Diverse judge panels help, but are heuristic without calibration. |
| SCOPE, `2602.13110` | [arXiv](https://arxiv.org/abs/2602.13110) | Pairwise selective judging with calibrated abstention and accepted-set risk. |
| Trust or Escalate, `2407.18370` | [arXiv](https://arxiv.org/abs/2407.18370) | Calibrated abstention/escalation instead of forced verdicts. |
| Correlated Errors in LLMs, `2506.07962` | [arXiv](https://arxiv.org/abs/2506.07962) | Different judges are not independent by default; measure shared error. |
| Beyond Consensus, `2510.11822` | [arXiv](https://arxiv.org/abs/2510.11822) | Agreeableness bias; majority vote is not truth. Estimate TPR/TNR where labels exist. |
| Self-Preference Bias, `2604.06996` | [arXiv](https://arxiv.org/abs/2604.06996) | Same-family/self preference persists under rubrics; measure overestimation. |
| Imperfect Verifier, `2604.07666` | [arXiv](https://arxiv.org/abs/2604.07666) | Perfect verification is not required; precision matters more than recall. Transfer carefully. |
| LLM-as-a-Verifier project | [GitHub](https://github.com/llm-as-a-verifier/llm-as-a-verifier) | Repeated checks, criteria, pairwise wins. Protocol pattern, not a formal paper in this pass. |

## Scale, Distribution, And Calibration

| Paper | Source | Transfer To Syke |
|---|---|---|
| Grading Scale Impact, `2601.03444` | [arXiv](https://arxiv.org/abs/2601.03444) | Scale choice changes alignment; do not assume pass/partial/fail is optimal. |
| Likert or Not, `2505.19334` | [arXiv](https://arxiv.org/abs/2505.19334) | Pointwise ordinal scoring can beat listwise complexity; scale should be empirical. |
| Judgment Distribution, `2503.03064` | [arXiv](https://arxiv.org/abs/2503.03064), [ACL](https://aclanthology.org/2025.findings-emnlp.1259/) | Use score-token distributions and expected score if logprobs are available. |
| Conformal Judge Intervals, `2509.18658` | [arXiv](https://arxiv.org/abs/2509.18658) | Later: calibrated ordinal intervals if calibration data and exchangeability hold. |
| KalshiBench, `2512.16030` | [arXiv](https://arxiv.org/abs/2512.16030) | Brier score, Brier Skill Score, explicit probability calibration against base rate. |

## Benchmark Validity And Item Quality

| Paper | Source | Transfer To Syke |
|---|---|---|
| Criterion-Referenceability, `2603.14732` | [arXiv](https://arxiv.org/abs/2603.14732) | Judge validity depends on observable criteria, not model strength. Gate tasks by referenceability. |
| No Free Labels, `2503.05061` | [arXiv](https://arxiv.org/abs/2503.05061) | Without verified references, agreement is weak evidence. Human/verified references matter. |
| PSN-IRT / Lost in Benchmarks, `2505.15055` | [arXiv](https://arxiv.org/abs/2505.15055) | Item difficulty, discriminability, guessing, feasibility, Fisher information. Later once labels are stable. |
| Construct Validity, `2511.04703` | [arXiv](https://arxiv.org/abs/2511.04703) | Define construct, sampling, contamination, uncertainty, error analysis. |
| Robustness/Reliability, `2509.04013` | [arXiv](https://arxiv.org/abs/2509.04013) | Paraphrase robustness and rank stability checks. |
| Growing Pains / Fixed Parameter IRT, `2604.12843` | [arXiv](https://arxiv.org/abs/2604.12843) | Fixed anchors to keep scores comparable as benchmark grows. Later. |

## Memory And Environment Neighbors

| Paper | Source | Transfer To Syke |
|---|---|---|
| MemoryArena, `2602.16313` | [arXiv](https://arxiv.org/abs/2602.16313), [project](https://memoryarena.github.io/) | Memory should be evaluated in multi-session action loops, not isolated recall. |
| LongMemEval, `2410.10813` | [arXiv](https://arxiv.org/abs/2410.10813), [project](https://xiaowu0162.github.io/long-mem-eval/) | Timestamped long-term memory, retrieval-vs-answer separation, false-premise abstention. |
| LifeBench, `2603.03781` | [arXiv](https://arxiv.org/abs/2603.03781), [repo](https://github.com/1754955896/LifeBench) | Multi-source long-horizon traces and non-declarative inference. |
| OSWorld, `2404.07972` | [arXiv](https://arxiv.org/abs/2404.07972), [project](https://os-world.github.io/) | Executable/state-based checks where possible. |

## Paper Conflicts To Remember

- Fixed criterion-referenceability conflicts with adaptive rubrics. Freeze the
  baseline rubric; use adaptive rubrics only as diagnostic suggestions.
- Panels reduce variance but can amplify shared bias. Preserve disagreement and
  measure wrong-wrong overlap.
- Fine scales can help some retrieval-style tasks, but coarse labels are often
  more reliable. Treat scale as empirical.
- Verifier outputs are evidence, not final verdicts.
- Event logs ground facts but not salience or utility by themselves.
- Memory benchmark papers evaluate downstream utility; this packet mostly
  evaluates measurement reliability.

