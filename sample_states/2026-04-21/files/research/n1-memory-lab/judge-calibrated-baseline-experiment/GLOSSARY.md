# Glossary

## `I_t`

One evaluation item at reference time `t`:

```text
I_t = (t, q_t, E_t, r_t)
```

## `q_t`

The user ask at time `t`.

## `E_t`

The bounded evidence packet available to the answerer or judge.

## `r_t`

The answer or reconstruction being judged.

## Bounded Packet

A declared evidence surface with known source visibility and time boundary.

## Zero Condition

A bounded condition without the synthesis/control layer. It is not a no-tool
condition.

## Observation

The judge's emitted label or score. `pass`, `partial`, and `fail` are
observations, not truth labels.

## Criterion-Referenceability

How much the desired judgment maps to observable, checkable criteria.

## Schema Adherence

How well criterion scores explain final observations.

## Factor Collapse

The case where nominally distinct rubric criteria are highly correlated or move
together.

## `sigma_alpha`

Probe/scenario difficulty effect.

## `sigma_beta`

Answer-generation variance.

## `sigma_gamma`

Judge identity effect.

## `sigma_epsilon`

Same-judge residual stochasticity.

## Escalation

Routing a low-confidence or ambiguous cell to human review or stronger judging
instead of forcing a verdict.

