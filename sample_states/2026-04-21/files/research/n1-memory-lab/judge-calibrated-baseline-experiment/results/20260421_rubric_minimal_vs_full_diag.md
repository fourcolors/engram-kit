# Minimal-vs-Full Rubric Diagnostic (JCB-059)

Date: 2026-04-21

Status: first-pass A/B proxy using existing pooled rubric diagnostics. No new judge calls.

| Judge group | Full R2 | Drop state_transition R2 | One-axis R2 | Full-drop delta | Full-one-axis delta |
|---|---|---|---|---|---|
| gpt_judge_pooled | 0.754 | 0.738 | 0.606 | 0.016 | 0.147 |
| opus_judge_pooled | 0.862 | 0.840 | 0.731 | 0.022 | 0.132 |

Read:
- Dropping `state_transition_tracking` causes only a small R2 decrease, so full-rubric signal is substantially recoverable from correlated criteria.
- A one-axis minimal rubric still carries high signal but not full signal.
- This is a diagnostic proxy, not a full prompt-level A/B re-judge experiment.
