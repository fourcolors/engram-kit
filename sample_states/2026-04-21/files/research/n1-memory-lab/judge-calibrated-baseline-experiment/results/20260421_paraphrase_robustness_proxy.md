# Paraphrase Robustness Proxy Run (JCB-026)

Date: 2026-04-21

Status: proxy run from existing calibration matrix (no new model calls).

Selected probes from plan: R05, R08, R14, R19

| Probe | Obs | Baseline non-exact | Full-band | Invalid | Proxy risk |
|---|---|---|---|---|---|
| R05 | 6 | 0.667 | 0.167 | 0.000 | high |
| R08 | 6 | 0.167 | 0.000 | 0.000 | lower |
| R14 | 6 | 0.667 | 0.000 | 0.333 | high |
| R19 | 6 | 0.333 | 0.167 | 0.000 | high |

Caveat: this is a sensitivity prior. True paraphrase robustness still requires rerunning judge evaluations on paraphrased asks.
