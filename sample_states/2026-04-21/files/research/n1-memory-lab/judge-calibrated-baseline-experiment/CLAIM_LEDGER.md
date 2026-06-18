# Claim Ledger

Status: claims must earn promotion from hypothesis to result.

| Claim | Status | Evidence Needed | Falsifier | Confidence |
|---|---|---|---|---|
| `pass/partial/fail` are noisy observations, not truth labels. | accepted premise | same-judge repeats, judge swaps | none; this is a modeling stance | high |
| `zero` is a valid bounded-packet condition, not no-tool. | accepted correction | condition schema and packet flags | protocol defines zero as no-tool | high |
| The current packet supports judge/rubric calibration more than architecture ranking. | working claim | reliability tables, judge identity effects, rubric diagnostics | stable architecture separation after calibration | medium |
| `state_transition_tracking` is load-bearing. | observed | regression and ablation tables | reverse ablation leaves R2 unchanged | medium |
| `state_transition_tracking` is a real memory primitive. | open | controlled probes isolating transition tracking | R2 reassembles from other axes | low |
| Useful-vs-fail is more stable than pass-vs-not-pass. | working claim | same-judge repeat scale analysis | larger sample reverses stability pattern | medium |
| More rubric detail will not automatically improve judging. | working claim | minimal vs full rubric A/B | full rubric improves reliability and calibration | medium |
| Diverse judge panels help. | conditional | gold subset with multiple judges | shared-error correction shows no gain | low |
| Conformal intervals are useful here. | later hypothesis | calibration set and exchangeability checks | intervals fail coverage or exchangeability invalid | low |
| IRT is useful here. | later hypothesis | stable anchor items and repeated labels | item parameters drift or labels unstable | low |

| Zero-condition bounded-packet behavior is empirically active (non-empty tool use in all zero rows of calibration subset). | observed | zero smoke test counts | future zero cells show no tool activity despite same packet setup | medium |
| Boundary-sensitive probes (`R03/R07/R13/R14/R15/R19`) carry elevated disagreement in zero condition. | observed | session-boundary audit by condition | larger set reverses condition ordering | medium |
| Proxy abstention catches all audited false-premise cells in current subset while reducing accepted-set coverage. | observed | abstention_false_premise_audit + coverage metrics | human-labeled review shows substantial false-premise leakage in accepted set | medium |
| Judge-family sensitivity shows large clean-vs-confounded swing, so family effects and judge-tier effects must stay separated. | observed | judge_family_sensitivity report | clean matched-model-family reruns nullify swing | medium |

## Promotion Rule

A claim can move to `result` only when:

- source data is named;
- script/notebook or manual method is reproducible;
- assumptions are stated;
- at least one falsifier is named;
- examples are inspected, not only aggregates.

