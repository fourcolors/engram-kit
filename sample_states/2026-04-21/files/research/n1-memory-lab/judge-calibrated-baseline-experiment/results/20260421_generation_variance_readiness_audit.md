# Generation Variance Readiness Audit (JCB-030)

Date: 2026-04-21

Status: blocked after readiness audit; clean generation-variance estimation is not currently possible from available runs.

Blocking reasons:
- available repeats are judge-repeat runs over reused answers, not clean repeated answer generations per cell
- gpt-side repeat artifacts involve gpt-5.4-mini judge config and contaminated rep lanes, not clean gpt-5.4 generation repeats
- no paired repeated generation set available across both ask models with fixed packet and fixed judge config

Next data required to execute JCB-030 directly:
- collect >=2 clean answer generations per probe/condition for gpt-5.4 ask model
- collect >=2 clean answer generations per probe/condition for claude-opus-4-6 ask model
- freeze judge config for downstream variance separation
