# Reference Perturbation Proxy Run (JCB-027)

Date: 2026-04-21

Status: proxy run from lineage-tag burden (no new model calls).

| Probe | Ref | Mean unsupported bundle | Max unsupported bundle | Proxy sensitivity |
|---|---|---|---|---|
| R03 | medium | 0.125 | 0.750 | high |
| R07 | high | 0.261 | 0.667 | high |
| R08 | low | 0.312 | 0.500 | high |
| R09 | medium | 0.362 | 0.750 | high |
| R14 | high | 0.117 | 0.250 | lower |
| R19 | medium | 0.625 | 1.000 | high |

Recommended perturbation set per selected probe: `no_reference`, `correct_reference`, `corrupted_reference`, `random_reference`.
Caveat: explicit reruns are still needed for definitive perturbation effects.
