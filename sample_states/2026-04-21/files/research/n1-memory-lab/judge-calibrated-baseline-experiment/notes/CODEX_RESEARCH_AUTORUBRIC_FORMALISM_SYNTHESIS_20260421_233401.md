# Codex Research Note: Autorubric + Criterion-Referenceability + Atomic/Holistic Formalism

Date: 2026-04-21 23:34:01 PDT
Author: Codex
Status: research synthesis for updating `WHERE_WE_ARE_20260421.html`
Scope: n=1 memory benchmark rubric/formalism design

## Purpose

This note synthesizes three papers for the Syke n=1 memory benchmark formalism:

- Autorubric: `2603.00077`, "Autorubric: Unifying Rubric-based LLM Evaluation"
- Yeadon et al.: `2603.14732`, "Criterion-referenceability determines LLM-as-a-judge validity across physics assessment formats"
- Zhang: `2603.28005`, "A Matched Holistic Rubric Rivals Self-Decomposing Atomic Judges for Benchmark-Style Reference-Support Classification"

The goal is to guide a revision of the math/formalism tab in `WHERE_WE_ARE_20260421.html`.

## Core Thesis

LLM judge reliability is mostly determined by the match between task structure and scoring architecture.

The judge model matters, but second-order. The decisive variables are:

```text
criterion-referenceability
x decomposition mode
x evidence packet quality
x rubric type
x calibration / abstention policy
```

For Syke, the question is not "atomic or holistic?" The question is:

```text
Which parts of memory reconstruction are criterion-referenceable enough to atomize,
and which parts are inherently global continuity judgments?
```

## Paper 1: Autorubric

Autorubric is more than Eq. 1. It is an operational answer to: if we already know what we want to measure, how do we execute that measurement cleanly?

Its real claims:

- A rubric is not a prompt. It is a structured scoring instrument.
- Each criterion should measure one construct.
- Each criterion gets its own LLM call.
- Criterion type matters: binary, ordinal, and nominal behave differently.
- `CANNOT_ASSESS` is a first-class verdict.
- Negative weights encode anti-patterns.
- Few-shot calibration helps, but only if there are examples.
- Per-criterion disagreement is more useful than aggregate disagreement.
- Caching, seeds, manifests, items logs, cost, latency, and checkpointing are part of scientific method, not engineering garnish.

The most important Autorubric mechanism for Syke is:

```text
N judges x M criteria = N x M independent LLM calls
```

That is how Autorubric attacks criterion conflation. It does not trust one LLM call to fill many axes independently. It forces independence by architecture.

This reframes Syke's current rubric collapse. The collapse may not only mean "bad rubric wording." It may mean:

```text
single-call multi-axis scoring is the wrong scoring architecture
```

So rubric-v2 probably requires scoring-architecture-v2.

### Autorubric Case Study Lessons

RiceChem:

- Binary criterion entailment works best when the criterion is concrete.
- Near-integer weights can be recovered when rubric criteria actually explain score.
- Partial-credit criteria can go negative in kappa.
- Holistic human overrides break criterion-level truth.

For Syke:

- Avoid mushy "partial continuity" style criteria unless they have hard behavioral anchors.

ResearcherBench:

- Open-ended deep research can be converted into weighted binary coverage criteria.
- Judges may agree on which questions are hard while disagreeing on who wins.
- Top systems are hardest to judge consistently.
- Critical-analysis criteria cause more disagreement than concrete mention/enumeration criteria.

For Syke:

- Criterion failure analysis is likely more stable than architecture ranking.
- Report "where memory failed" before "which memory won."

CHARM-100:

- Mixed criterion types are valuable.
- Binary is strongest.
- Ordinal exact accuracy is weak, but adjacent accuracy can be high.
- Nominal categories can hide asymmetric recall.
- The dataset deliberately creates cross-criterion conflict so the judge cannot use one global latent.

For Syke:

- Build CHARM-style calibration cells where criteria conflict.

Examples:

```text
correct artifact, wrong live thread
right live thread, stale state
complete but bloated
concise but restart-unsafe
well-cited but not useful
useful but weakly supported
```

This is how to test whether criteria are genuinely distinct.

## Paper 2: Criterion-Referenceability

Yeadon et al. supply the missing empirical law:

```text
judge validity tracks criterion-referenceability, not model strength
```

Structured questions work because the features that justify a mark are visible and mappable.

Scientific plots work because visual/code features are countable and constrained.

Essays fail because the construct is holistic, weakly referenceable, and even humans do not agree reliably.

The key result is not just that essays fail. It is that adding schemes and exemplars improves distributional alignment without recovering discriminative validity.

That means a judge can learn to match the average shape of human marks while still failing to rank individual items correctly.

For Syke, this matters because a memory answer can look calibrated to the general style of "good reconstruction" while still failing the actual user-continuation need. Distributional match is not enough.

### Syke's Position On The Spectrum

Syke is not RiceChem. It is not a pure essay either.

It is partially-referenceable operative-state reconstruction.

Some parts are highly referenceable:

- Did the answer cite the right artifact?
- Did it identify the active thread?
- Did it avoid stale thread resurrection?
- Did it mention the current blocker?
- Did it preserve the latest decision?
- Did it avoid claiming completed work that is not complete?

Some parts are holistic:

- Would this let an agent safely resume?
- Is the answer sufficient but not bloated?
- Did it preserve continuity of the user's working intent?
- Did it integrate cross-session state without flattening it?

Therefore Syke needs a hybrid judge design.

## Paper 3: Atomic vs Holistic

Zhang supplies the correction to "atomic is always better."

The important distinction:

```text
inference-time self-decomposition != designer-time atomic criteria
```

Zhang tests a self-decomposing judge: the LLM breaks an answer into claims on the fly, then verifies them. That fails on completeness-heavy tasks.

Autorubric uses designer-time atomic criteria: humans predefine the criteria, and each one gets scored separately. Zhang does not refute that.

But Zhang shows something crucial:

```text
completeness is often a global property
```

Self-decomposition verifies local claims and misses omissions. The answer can be locally true but globally incomplete.

That is exactly a Syke failure mode.

A memory reconstruction can contain only true statements and still be useless because it omits the live thread, next action, or transition point.

So the lesson is:

- Use atomic criteria for local, checkable properties.
- Use holistic criteria for global completeness / continuation.
- Do not let the judge invent its own decomposition at inference time.
- Do not atomize away the global property the benchmark cares about.

## Unified Design Principle

The three papers together imply this rule:

```text
If the criterion is locally observable, atomize it.
If the criterion is global completeness or continuation, keep it holistic but behaviorally anchored.
If the criterion is not referenceable from the packet, do not force a verdict.
```

## Rubric Shape For Syke

The rubric should not be all atomic or all holistic. Use three criterion classes.

### Class A: Atomic Binary Checks

These are Autorubric-friendly.

Examples:

```text
active_thread_identified
latest_decision_preserved
stale_state_not_asserted
artifact_citation_present
current_blocker_named
condition_identity_not_used
```

Scoring:

```text
MET / UNMET / CANNOT_ASSESS
```

Metrics:

```text
raw agreement
Cohen kappa
prevalence
abstention rate
```

### Class B: Holistic Continuation Criteria

These are Zhang-sensitive.

Examples:

```text
restart_safety
operative_state_sufficiency
cross_session_coherence
global_omission_risk
```

These should be one criterion each, not decomposed into many local checks.

Scoring:

```text
unsafe / partial / safe
```

Report:

```text
adjacent accuracy
weighted kappa
confusion matrix
human eye-read examples
```

Do not pretend exact ordinal agreement will be clean.

### Class C: Nominal Failure Typing

For each bad or disputed answer, classify failure mode:

```text
WRONG_THREAD
STALE_STATE
UNSUPPORTED_CLAIM
PACKET_INSUFFICIENT
TIME_AMBIGUOUS
OVERBROAD_SUMMARY
UNDERCOMPLETE_RESTART
HALLUCINATED_ARTIFACT
JUDGE_UNCERTAIN
```

This is not the score. It is the diagnostic label. It may become the most useful output.

Metrics:

```text
nominal kappa
per-class recall
confusion matrix
```

CHARM's nominal lesson matters here: nominal categories can have asymmetric recall, so report per-class recall, not only accuracy.

## Revised Formalism

Start with:

```text
q in Q              real user probe / ask
c in C              memory condition: zero, pure, syke, etc.
pi in Pi            packet protocol
P_pi(q,c)           evidence packet produced by protocol pi
m in M              answering model family
r in R              answer replicate
k in K              rubric criterion
j in J              judge family
l in L              judge replicate
```

Answer:

```text
a_q,c,m,r = A_m(q, P_pi(q,c), seed_r)
```

Criterion-level verdict:

```text
z_q,c,m,r,k,j,l in Omega_k union {bottom}
```

Where:

```text
bottom = CANNOT_ASSESS
```

Each criterion has schema:

```text
criterion k = {
  id,
  construct,
  type: binary | ordinal | nominal,
  mode: atomic | holistic,
  options,
  value_map,
  weight,
  polarity: reward | penalty,
  referenceability: high | medium | low,
  applicability: universal | conditional,
  abstention_types,
  citation_contract,
  prompt_template
}
```

Only then convert to numeric:

```text
y_q,c,m,r,k,j,l =
  value_map_k(z_q,c,m,r,k,j,l) if z != bottom
  missing                      if z = bottom
```

Aggregate per criterion first:

```text
yhat_q,c,m,r,k = Agg_k({y_q,c,m,r,k,j,l})
```

Then score:

```text
S = clamp(sum_k yhat_k w_k / sum_{w_k > 0} w_k, 0, 1)
```

With abstention, report interval:

```text
S_min = score if all unassessed positive criteria are 0
S_max = score if all unassessed positive criteria are 1

coverage = observed_positive_weight / total_positive_weight
```

Output:

```text
{
  score_interval: [S_min, S_max],
  coverage,
  criterion_vector,
  abstention_vector,
  failure_type_vector,
  judge_vote_distributions
}
```

The scalar score is last, not first.

## Revised Variance Model

The current model is missing the condition effect. Use:

```text
y_q,c,m,r,k,j,l =
  mu_k
  + tau_c,k
  + alpha_q,k
  + (tau_alpha)_q,c,k
  + beta_m,k
  + delta_r,k
  + lambda_pi,q,c,k
  + gamma_j,k
  + chi_j,c,k
  + epsilon_q,c,m,r,k,j,l
```

Meaning:

- `tau_c,k`: memory condition effect. This is the target.
- `alpha_q,k`: probe difficulty.
- `(tau_alpha)_q,c,k`: condition helps on some probes more than others.
- `beta_m,k`: answer model family.
- `delta_r,k`: answer generation stochasticity.
- `lambda_pi,q,c,k`: packet protocol effect.
- `gamma_j,k`: judge family bias.
- `chi_j,c,k`: judge x condition bias / identity halo.
- `epsilon`: residual flicker.

The benchmark claim eventually becomes:

```text
tau_syke - tau_pure
```

Only over validated criteria and with uncertainty from all terms above.

## The Key Open Experiment

The missing experiment across all three papers is:

```text
externally-defined designer-time atomic criteria
+ explicit holistic completeness criterion
+ negative omission penalty
+ typed abstention
```

applied to:

- ASQA/QAMPARI partially-supported cases
- Durham essay-like holistic tasks
- Syke operative-state reconstruction

Hypothesis:

A hybrid rubric beats both pure holistic judging and inference-time self-decomposition, because it preserves global completeness while giving the judge concrete handles.

For Syke:

```text
atomic checks for referenceable state facts
+ holistic continuation criterion for restart safety
+ negative penalties for stale/wrong-thread/unsupported claims
+ nominal failure typing
```

This is likely the right rubric-v2 shape.

## What Claude Should Change In `WHERE_WE_ARE_20260421.html`

1. Replace scalar-verdict formalism with criterion-level tensor formalism.
2. Add criterion schema: binary / ordinal / nominal, atomic / holistic, referenceability, abstention.
3. Add score interval and coverage, not silent `CANNOT_ASSESS` skipping.
4. Add condition effect `tau_c,k` as the target estimand.
5. Add packet protocol effect `lambda_pi,q,c,k`.
6. Add judge-condition interaction `chi_j,c,k`.
7. Add scoring architecture validity: separate per-criterion LLM calls may be required to avoid rubric collapse.
8. Add three criterion classes:
   - atomic binary state checks
   - holistic continuation / completeness criteria
   - nominal failure-mode labels
9. Add the unified three-paper spectrum:
   - high referenceability -> atomic works
   - medium completeness -> holistic or hybrid
   - low referenceability essay-like -> current judge methods fail
10. Add the open experiment: hybrid externally-defined atomic + holistic completeness + omission penalties.

## Final Thesis

```text
Memory reconstruction is partially referenceable.

It contains local facts that should be judged atomically,
global continuation properties that must be judged holistically,
and failure modes that should be typed nominally.

The evidence packet determines which of these are judgeable.
The rubric determines how they are scored.
The judge architecture determines whether criteria remain independent.
The variance model determines whether a condition effect is real.

Only after all four layers are valid can we compare memory systems.
```

