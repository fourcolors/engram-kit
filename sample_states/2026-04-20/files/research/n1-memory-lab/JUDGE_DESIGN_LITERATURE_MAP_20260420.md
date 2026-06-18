# Judge Design Literature Map — 2026-04-20

Status: working synthesis for the next judge redesign  
Scope: semi-verifiable, open-ended judge design for bounded operative-state reconstruction

This note consolidates the broad literature pass that started from:

- `CyclicJudge` ([2603.01865](https://arxiv.org/abs/2603.01865))
- `LLM-as-a-Verifier` (repo lineage; no strong formal citation trail yet)
- `When Judgment Becomes Noise` ([2509.20293](https://arxiv.org/abs/2509.20293))

and then widened to the most relevant neighboring work on:

- judge validity
- criterion-referenceability
- reference-grounded judging
- abstention / escalation
- panel / jury judging
- open-ended memory / partial-observability task shape

The question is not "what is a good benchmark in general?"  
It is:

**What math, protocol, and task assumptions actually transfer to a judge for bounded, partially verifiable reconstruction of the closest correct operative state at time `t` from fragmented evidence?**

---

## 1. Ranked Relevance

### Immediate order

1. **When Judgment Becomes Noise**
2. **CyclicJudge**
3. **LLM-as-a-Verifier**

### Why

- `When Judgment Becomes Noise` is the paper for **rubric coherence**
  - schema incoherence
  - factor collapse
  - aggregation masking

- `CyclicJudge` is the paper for **judge identity as a confound**
  - same answers
  - different judges
  - fixed-budget collection design

- `LLM-as-a-Verifier` is the paper for **artifact-grounded and repeated verification**
  - useful mostly as a protocol pattern
  - not as a task template

This is the sequence to use them in.

---

## 2. The Closest Neighboring Works

### Judge validity / grounding

- **No Free Labels** ([2503.05061](https://arxiv.org/abs/2503.05061))
  - Agreement without grounded references is weak evidence.
  - Best warning against trusting judge agreement on correctness-heavy tasks.

- **Criterion-referenceability determines LLM-as-a-judge validity** ([2603.14732](https://arxiv.org/abs/2603.14732))
  - Strongest current framing for what part of a task is legitimately judgeable.
  - Distinguishes absolute agreement from discriminative validity.

- **Evaluating the Evaluator / adherence line** ([2408.08781](https://arxiv.org/abs/2408.08781))
  - Judge prompt detail often buys less than expected.
  - Useful as a warning against overcomplicating rubric language.

### Protocol / panels / abstention

- **Trust or Escalate** ([2407.18370](https://arxiv.org/abs/2407.18370))
  - Best protocol for selective trust / abstention / escalation.
  - Useful because our task is semi-verifiable, not fully judgeable.

- **RULERS** ([2601.08654](https://arxiv.org/abs/2601.08654))
  - Best nearby protocol for locked rubric + evidence-anchored scoring.
  - Strong candidate pattern for our next judge contract.

- **Replacing Judges with Juries / PoLL** ([2404.18796](https://arxiv.org/abs/2404.18796))
  - Strong practical baseline for multi-judge aggregation.
  - Useful later, after rubric cleanup.

- **SCOPE** ([2602.13110](https://arxiv.org/abs/2602.13110))
  - Good later-stage selective judging paper.
  - Conformal/selective protocol is promising, but too heavy for the next iteration.

### Task-shape neighbors

- **MemoryArena** ([2602.16313](https://arxiv.org/abs/2602.16313))
  - Best structural neighbor: memory as part of a multi-session agent-environment loop.
  - Useful for the loop formalism, not as a direct benchmark template.

- **LongMemEval** ([2410.10813](https://arxiv.org/abs/2410.10813))
  - Useful for temporal correctness, updates, and abstention.
  - Too dialogue-memory-centric to define our whole object.

- **LifeBench** ([2603.03781](https://arxiv.org/abs/2603.03781))
  - Useful because it expands memory beyond explicit declarative recall.
  - Good neighbor for procedural / multi-source pressure.

- **OSWorld** ([2404.07972](https://arxiv.org/abs/2404.07972))
  - Useful as a partial-observability foil.
  - Misleading if imported as a task-completion template.

---

## 3. The Smallest Defensible Task Object

We can responsibly freeze only this much:

- there is a hidden operative state at time `t`
- the system only sees a bounded observation packet up to `t`
- the answer is an estimate of that hidden state
- some parts are directly checkable
- some parts remain semantic
- success is reconstruction-for-continuation, not external-task completion

In symbols:

- hidden state: `s_t`
- bounded observations: `o_{<=t}`
- answer / reconstruction: `r_t`

This is enough.

Do **not** freeze yet:

- full POMDP control language as if the task were primarily action optimization
- a symbolic world model with clean closure
- trajectory elegance as part of the main object
- a broad self/world-model claim

---

## 4. The Smallest Defensible Judge

### Universal primitives

- `bounded_support`
- `time_local_correctness`
- `operative_state_adequacy`
- `wrong_restart_risk`

### Conditional primitives

- `enumeration_completeness`
- `cross_surface_integration`
- `committed_state_fidelity`
- `object_continuity`
- `provenance_traceability`

### Claim typing

Every judged claim should be forced into:

- `verified`
- `inferred`
- `speculative`

This is the cleanest answer to the GPT-vs-Opus divergence:

- GPT penalizes unsupported breadth
- Opus tolerates narrative inference unless contradicted

The contract should decide that distinction, not the judges.

---

## 5. What the Packet Justifies Now

The current packet supports only a **small** quantitative stack.

### Run now

1. Paired contingency tables on same-answer judge swaps
2. Weighted Cohen's kappa on `fail / partial / pass`
3. Binary `useful = pass + partial` vs `fail` plus McNemar
4. Mean paired ordinal shift (`fail=0, partial=1, pass=2`)
5. Per-probe instability rates

### Do not run yet

- full CyclicJudge ANOVA / variance-component claims
- IRT / discriminability modeling
- conformal intervals
- fine-grained token-score scales
- pairwise tournament selection
- larger psychometric stacks

The packet is good enough for **reliability-first math**, not for mature psychometrics.

---

## 6. What To Steal From Each Paper

### From `When Judgment Becomes Noise`

Use now:

- ask whether factor scores actually explain verdicts
- check for factor collapse
- distrust aggregate scalar summaries when they mask disagreement

This is the first gate.

### From `CyclicJudge`

Use later:

- judge identity is a first-class variable
- ask-fixed cross-judge comparisons should be planned, not ad hoc
- panel rotation is the right next collection protocol after rubric cleanup

But only **after** the rubric is coherent.

### From `LLM-as-a-Verifier`

Use narrowly:

- a few focused criteria
- repeated verification
- artifact-grounded prompts

Do **not** import:

- trajectory tournament framing
- external task-completion criteria
- benchmark-native verifier ontology

---

## 7. What Not To Do Next

1. Do not recalibrate the current big rubric.
2. Do not collect more judged data under the old judge contract.
3. Do not publish any single-judge architecture ranking.
4. Do not add more score granularity yet.
5. Do not import Terminal-Bench / SWE-bench verifier criteria.
6. Do not move to pairwise/tournament machinery yet.
7. Do not turn trajectory beauty into a hidden target.
8. Do not overclaim psychometric validity from a small, heterogeneous packet.

---

## 8. The Ordered Next-Step Sequence

1. Freeze the task object:
   bounded reconstruction of the closest correct operative state at time `t`

2. Rewrite the judge around the small primitive set above.

3. Make deterministic checks primary:
   - time bounds
   - artifact existence
   - committed truth
   - explicit contradiction
   - provenance when applicable

4. Keep only a narrow semantic residual:
   - live-thread selection
   - stale-vs-live revision
   - restart safety

5. Rejudge the **existing packet** with the simplified contract.

6. Evaluate only:
   - schema coherence
   - factor collapse
   - binary usefulness stability
   - per-probe instability

7. If unstable, simplify the rubric again.
   - no new data first

8. Once one clean rubric exists:
   - add ask-fixed cross-judge scoring by design
   - then true same-judge repeats

9. Only after that:
   - cyclic multi-judge rotation
   - richer statistical layers
   - uncertainty intervals / selective escalation

---

## 9. Shortest Bottom Line

The literature says the next move is **not**:

- more runs
- more judges
- more categories
- more math

The next move is:

- **fix the rubric**
- **ground it in artifacts**
- **rejudge the packet**
- **prove the schema is coherent**
- **then** calibrate judge identity

That is the most defensible path for our semi-verifiable open-ended judge design.
