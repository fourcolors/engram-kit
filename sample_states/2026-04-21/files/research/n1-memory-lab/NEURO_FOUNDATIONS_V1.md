# Neuro Foundations V1 — notes for environment/eval design

Status: working document, accumulating batch-by-batch through 2026-04-17+ discussion.
Purpose: ground the replay-lab environment + judge design in computational neuroscience
literature that a reviewer in 2026 would recognize, not ad-hoc taxonomy.

## Scope guardrails

- FEP / active inference belongs to **Syke the architecture**, not the eval environment.
- The eval environment must be neutral so Native / Hermes-provider / Syke / future substrates
  can be tested fairly.
- New primitives must subsume old benchmark primitives (recall, factual grounding, temporal
  ordering), not replace them.
- N=1: real human life, laptop-mediated. Both parts matter.

## Batch 1 — "one computation" framings (the brain model of psyche)

User's belief: what's called "memory" is one underlying computation whose outputs we
bucket into psychological categories after the fact. The reviewers will accept this if
the citation base is respected. Three camps, ordered by acceptance in 2026:

1. **Predictive Processing (PP)** — Andy Clark, Jakob Hohwy
   - Core claim: the brain is fundamentally a prediction machine. Perception, memory,
     action, attention are all expressions of the same hierarchical prediction-error
     minimization.
   - Status in 2026: **most widely accepted** "one-framework" brain theory. Less
     mathematically committed than FEP, so less vulnerable to the Colombo/Bruineberg
     2024 critiques.
   - Citeable refs: Clark *Surfing Uncertainty* 2016; Clark *The Experience Machine* 2023;
     Hohwy *The Predictive Mind* 2013; Hohwy 2020 "New directions in predictive
     processing."

2. **Bayesian Brain Hypothesis** — Knill, Pouget, Tenenbaum, Griffiths
   - Core claim: cognition is approximate Bayesian inference over a generative model of
     the world. Memory recall = posterior sampling; perception = likelihood; action =
     decision under uncertainty. Same machinery, different conditioning sets.
   - Status: dominant in computational cognitive science. Respected.
   - Citeable refs: Knill & Pouget 2004 *Trends in Neurosciences* "The Bayesian brain";
     Tenenbaum, Kemp, Griffiths, Goodman 2011 *Science* "How to grow a mind."
   - Specifically for memory-as-inference:
     - Hemmer & Steyvers 2009 "Integrating episodic memories and prior knowledge"
     - Nagy, Kurth-Nelson, Behrens 2020 — memory recall as generative reconstruction
     - Bays 2015 — working memory as Bayesian resource allocation

3. **Active Inference / Free Energy Principle (FEP)** — Friston, Parr, Pezzulo
   - Core claim: self-organizing systems minimize variational free energy. Perception +
     action + learning are one update rule over a generative model.
   - Status in 2026: **mathematically committed, philosophically contested**.
     - Alive and respected in EEG/BCI (Pezzulo; Parr 2024), motor control, neurorehab.
     - 2024 critiques argue FEP is underconstrained as empirical theory
       (Colombo & Wright, Bruineberg et al., Andrews).
     - Safe to use as lingua franca describing Syke's computation; **unsafe** as the
       sole justification for the eval environment.

### How to use these three in writing

- Most defensible framing for the "one computation" claim:
  > "Consistent with predictive-processing accounts of cognition (Clark 2016, 2023;
  > Hohwy 2013), we treat what is conventionally called 'memory' as one surface of a
  > single inferential process. On this view, recall, recognition, and schema retrieval
  > are distinct observables of the same underlying posterior-update dynamic (Hemmer &
  > Steyvers 2009; Nagy et al. 2020)."

- Why this is strictly safer than leading with FEP: PP is the broad umbrella, FEP is
  one formal commitment within it. Reviewers who reject FEP typically still accept PP.

## Batch 2 — "laptop-mediated real human life" as a world-model problem

User's intuition: active inference is used in BCI/EEG (headset + brain); what we have is
"me and a laptop" — so we need the laptop-mediated analog, not the neural one. This is
real and there is a citable lineage.

1. **POMDP formalism as the mathematical backbone**
   - Kaelbling, Littman, Cassandra 1998 *Artificial Intelligence* "Planning and acting in
     partially observable stochastic domains"
   - Canonical formal spec: an agent acts on an environment whose full state is hidden;
     it maintains a belief over that state from observations.
   - Still the standard reference for "hidden state + partial observation" in 2026.

2. **World Models in ML**
   - Ha & Schmidhuber 2018 "World Models" NeurIPS — the agent learns a compressed latent
     model of the environment and plans inside it.
   - Hafner et al. Dreamer V1/V2/V3 (2019/2021/2023) — scaled world-model RL. V3 is
     current SOTA reference for world-model-based agents.
   - The N=1 relevant reframe: the latent the memory system must infer is *the user*,
     not physics.

3. **Laptop-mediated digital life stream**
   - Reeves, Ram, Robinson et al. Stanford **Screenome Project** — 2020 principled data
     model for "digital life stream," continued 2021–24. Screen-capture based behavior
     modeling. Closest existing formal spec for exactly what the user is: a human plus
     their laptop, over time. This is the right citation for "real human life with
     something happening on the laptop too."
   - MyLifeBits (Bell, Gemmell, Microsoft 2006) — historical, lessons still hold: raw
     capture is easy; useful retrieval is the hard problem.

4. **Active inference in BCI/EEG — justifying the user's intuition**
   - Pezzulo et al. 2024 — active inference for motor control and neurorehabilitation.
   - Millán and collaborators — active inference in BCI decoding.
   - This grounds the move "inference over hidden neural state" as real engineering.
     Our laptop-analog is: *inference over hidden user-cognitive state from observed
     digital traces*. Same structure, different observation channel.

### The framing we can defend

> "We model the environment as a non-stationary partially-observed Markov decision
> process (Kaelbling et al. 1998) whose hidden state is the user's cognitive state
> and active project graph. This positions the memory system as performing approximate
> state inference from a heterogeneous observation stream, analogous to the
> laptop-mediated setting of the Screenome project (Reeves et al. 2020) and the
> world-model framing of Ha & Schmidhuber 2018 / Dreamer (Hafner et al. 2023). Unlike
> the BCI setting where the observation channel is neural (Pezzulo et al. 2024),
> the channel here is the user's fragmented cross-harness digital trace."

## Batch 3 — what the "six-slot environment spec" actually is

This was confusing. It's just the standard RL/agent environment interface that's been
in the OpenAI Gym / Gymnasium API since ~2016. Not novel, not load-bearing theory. It's
only useful because it is the boundary at which a memory system plugs into an
environment — once we commit to it, any architecture can be tested.

The six slots, with plain-English meaning:

1. **State** — everything that's true about the world at a moment. Includes things the
   agent can't see. For us: the user's actual cognitive state, fatigue, priorities.
2. **Observation function** — what the agent does see. For us: the slice (harness
   transcripts, git state, workspace files, timestamps).
3. **Action space** — what the agent is allowed to do. For memory systems:
   record, retrieve, compose-context, emit-answer.
4. **Dynamics** — how state evolves on its own. For us: the user works, time passes,
   projects change, whether or not the memory system does anything.
5. **Goals** — what the agent is asked. For us: the real-ask corpus, anchored at
   time `t`.
6. **Evaluation** — the judge function. Separate from goals.

Why it matters: keeping these six separate is what lets you swap architectures in/out
without rewriting the harness. Gym did this for games. CoALA (Sumers et al. 2024)
applies the same cut to language agents explicitly.

- Citeable refs: Brockman et al. 2016 "OpenAI Gym"; Towers et al. 2024 Gymnasium;
  Sumers, Yao, Narasimhan, Griffiths 2024 *TMLR* "Cognitive Architectures for Language
  Agents."

## Batch 4 — backwards compatibility: new primitives must subsume old

User requirement: new primitives must not replace recall/factual-grounding/temporal —
they must subsume them.

Mapping table (computational primitive → classical benchmark primitive it subsumes):

- `pattern_completion` → classical **recall** (vague cue → referent)
- `source_attribution` → classical **temporal/provenance recall**
- `interference_resistance` → classical **factual grounding under distractors**
- `binding_across_time` → classical **long-context retrieval**, LongMemEval lag series
- `pattern_separation` → classical **disambiguation**, LoCoMo-style near-duplicate tasks
- `relational_inference` → classical **multi-hop reasoning**
- `schema_integration` → no clean classical match — this is the novel axis
- `replay_consolidation` → no clean classical match — this is the novel axis
- `prospective_retrieval` → closest to **memory-augmented planning** benchmarks
- `generalization_from_sparse` → classical **few-shot transfer**

Important: the first six strictly contain their classical counterparts. The last four
either have partial mapping or extend the primitives the field currently measures.
This is the shape the writeup should take: *"we subsume, then extend."*

## Batch 5 — Screenomics citation network and comp-neuro gap

The named cluster in this neighborhood is tight. Use these citations.

**Data-originators (Stanford + Penn State)**
- Reeves, Ram, Robinson — Stanford Communication / Stanford Psych + Penn State HDFS / Stanford Pediatrics. 20+ papers 2020–2026 on screenomics.stanford.edu/publications.
- Brinberg (Penn State) — junior lead, "Screenertia" 2023 Communication Research, "Idiosyncrasies of Everyday Digital Lives" 2020 Computers & Human Behavior 114:106570.

**Modeling extensions (Stanford HCI) — the load-bearing computational follow-ups**
- **GUM** (UIST 2025 best-paper honorable mention) — Shaikh, Sapkota, Rizvi, Horvitz (MSR), Park, Yang, Bernstein. arXiv 2505.10831. "Creating General User Models from Computer Use." Screen observations → confidence-weighted natural-language propositions about user beliefs / knowledge / preferences. Structurally close to Syke's memex.
- **LongNAP** (2026) — Shaikh, Teutschbein (Hasso Plattner), Gandhi, Chi, Haber, Robinson, Ram, Reeves, S. Yang (Stanford+NYU), Bernstein, D. Yang. arXiv 2603.05923. "Learning Next Action Predictors from HCI." 170M Screenomics screenshots from 257 users. Retrieval + GRPO RL + LLM-as-judge reward. Most direct computational extension of Screenomics.

**Industry-lab tie**
- Eric Horvitz (Microsoft Research) — co-author on GUM. Only frontier-lab tie. Long Bayesian-user-modeling history.

**Notable absence from Screenomics citation network (confirmed via targeted search)**
- DeepMind, Anthropic, OpenAI, Meta — no published direct engagement.
- Comp-neuro community (Friston, Parr, Pezzulo, Clark, Hohwy, Behrens, Whittington, Momennejad, Gershman, Griffiths, Tenenbaum) — zero citations. The comp-neuro ↔ digital-life-stream bridge is unbuilt.
- This is an opportunity, not a lateness. The space is occupiable.

**Parallel tradition — digital phenotyping (sensor/metadata, not screen-content)**
- Torous (Harvard/Beth Israel Deaconess) — coined "digital phenotyping" 2016 JMIR Mental Health with Kiang, Lorme, Onnela.
- Onnela (Harvard Chan) — Beiwe platform. HMM-style state-space models on sensor data.
- Mohr (Northwestern CBITs) — behavioral intervention technology.
- Insel (formerly NIMH / Mindstrong) — clinical translation.
- Communities rarely cross-cite. Opportunity to be one of the first bridges.

**First published critique of Screenomics**
- Chen 2025 (Meta-Research Center) — "Are we measuring too much in Experience Sampling Methodology?" Privacy, analytic-payoff, tech-dependence. First real external critique.

## Batch 6 — POMDP math and the 2024–2026 alternatives

### The standard tuple

A POMDP is a 7-tuple `⟨S, A, T, R, Ω, O, γ⟩`:

- `S` — hidden states (for us: user's cognitive state + project graph)
- `A` — actions (for memory systems: record / retrieve / compose-context / emit-answer)
- `T(s' | s, a)` — transition dynamics (world moves; mostly user-driven, not agent-driven for us)
- `R(s, a)` — reward (judge evaluation)
- `Ω` — observation space (traces, slice, git, timestamps)
- `O(o | s, a)` — observation function (what the agent sees from the hidden state)
- `γ` — discount factor (not essential for one-shot ask eval)

### The key object: the belief state

An agent in a POMDP cannot see `s`. It maintains a belief `b_t(s) = P(s_t | o_{1:t}, a_{1:t-1})` — a distribution over hidden states.

**Belief update (Bayes):**
```
b_{t+1}(s') ∝ O(o_{t+1} | s', a_t) · Σ_s T(s' | s, a_t) · b_t(s)
```

Read: new belief ∝ (how likely is this obs under s') × (how likely did we arrive at s' given past belief and action).

**For us:** the memex *is* the belief state representation. Every architecture we test maintains a belief somehow; they just use different representations.

### Why vanilla POMDP doesn't quite fit us

Three breaks from textbook POMDP:
1. **Non-Markov** — long-horizon dependencies are the whole point.
2. **Agent barely influences dynamics** — the user works whether or not the memory system acts. Our actions mostly change *belief*, not world state. This breaks the decision-theoretic framing.
3. **Non-stationary** — the user's priorities drift. Standard POMDP assumes fixed `T`.

### The 2024–2026 alternatives worth knowing

What "belief representation" each approach uses:

| approach | belief representation | reference |
|---|---|---|
| **Kalman filter** | Gaussian `(μ, Σ)`, linear dynamics | classical, 1960 |
| **Particle filter** | N weighted samples | Gordon 1993; classical non-parametric |
| **HMM** | discrete posterior, no actions | Rabiner 1989 |
| **Deep state-space models (DSSM)** | learned neural latent | Krishnan, Shalit, Sontag 2017 |
| **RSSM (Recurrent State Space Model)** | deterministic + stochastic latent, in a learned world model | Hafner et al. 2019 PlaNet; Dreamer V3 2023 (*Nature*) |
| **Structured State Space Models — S4 / S5 / Mamba** | long-range convolutional latent, linear-time | Gu, Goel, Ré 2022 *ICLR*; Gu & Dao 2023 Mamba |
| **LLM context window** | the text itself *is* the belief | de facto standard in LLM agents |
| **JEPA / V-JEPA** | non-generative predictive embeddings | LeCun 2022; Meta 2024–25 |

### Mapping architectures to belief representations (for our eval)

- **Native harness memory (Claude/Codex local context):** belief = current context window. Hard cap. Resets on session.
- **Hermes / provider / plugin memory:** belief = injected retrieved chunks + current context. Externalized store + retrieval.
- **Syke:** belief = memex (compact LLM-generated projection) + pointer index + adapter-raw backing. Structured long-horizon.
- **Hypothetical future substrate (Mamba-style SSM over a life stream):** belief = SSM hidden state over the trace. Unexplored.

This is the clean frame: every architecture we test is a different **belief representation choice**. The eval scores how well each representation supports query-answering about hidden user state.

### What to cite in a paper

- Kaelbling, Littman, Cassandra 1998 *AI* — POMDP definition
- Hafner et al. 2019/2023 — RSSM / Dreamer (the ML-native version of POMDP belief modeling)
- Gu, Goel, Ré 2022 *ICLR* "Efficiently Modeling Long Sequences with Structured State Spaces" (S4)
- Gu & Dao 2023 "Mamba: Linear-Time Sequence Modeling with Selective State Spaces"
- Sumers et al. 2024 *TMLR* "Cognitive Architectures for Language Agents" (CoALA) — for the agent-environment cut applied to language agents

### What this gives us operationally

Our replay sandbox + judge is a **belief-quality eval**. Each architecture proposes a belief representation; we probe that belief with real asks at time `t`; the judge scores how well the belief supported the answer. The math backing this is the standard POMDP-belief-eval framing — we don't invent the formalism, we just commit to it.

---

## Open questions for next batches

- How specifically does Screenome operationalize its digital-life-stream state? Do we
  align our slice format with theirs?
- Which of the 10 primitives is *too much* for a first pass? The first six subsume
  classical — maybe we ship with those six and earn the other four.
- Where does DMN / narrative-self literature give us the "coherence" framing that
  doesn't collapse to TEM/relational-inference?
- What does Pezzulo 2024 specifically say about active-inference in non-neural
  observation channels (engineering analogs)?

## Batch 7 — Language as computational substrate (GEPA + TextGrad + DSPy)

**The load-bearing move:** a reasoning LLM operating under meta-instructions is a legitimate agent/policy even without in-loop gradient descent or scalar loss — because language itself is a computational substrate in which optimization, reflection, and state update genuinely occur.

### GEPA (the strongest single citation)

- **Paper:** Agrawal, Tan, Soylu, Ziems, Khare, Opsahl-Ong, Singhvi, Shandilya, Ryan, Jiang, **Potts, Sen, Dimakis, Stoica, Klein, Zaharia**, Khattab — *"GEPA: Reflective Prompt Evolution Can Outperform Reinforcement Learning"* — arXiv 2507.19457, July 2025 (revised Feb 2026). Stanford NLP + Berkeley Sky Computing + Databricks.
- **Quote (load-bearing):** *"the interpretable nature of language often provides a much richer learning medium for LLMs, compared to policy gradients derived from sparse, scalar rewards."*
- **Results:** +6% avg over GRPO (up to +20%); **35× fewer rollouts**; +12% over MIPROv2 on AIME-2025.
- **Mechanism:** sample trajectories → reflect in natural language → propose prompt updates → Pareto-select across diverse attempts.
- **Implication for Syke:** the synthesis cycle is structurally one GEPA iteration. Adding (a) reflection over ask-answer-judge tuples and (b) Pareto selection across synthesis-prompt variants turns Syke's synthesis into a self-improving language-agent policy.

### TextGrad

- **Paper:** Yuksekgonul, Bianchi, Li, Zou — *"TextGrad: Automatic Differentiation via Text"* — Stanford 2024, published *Nature* 2025.
- **Quote:** *"TextGrad backpropagates textual feedback provided by LLMs to improve individual components of a compound AI system."*
- **Mechanism:** LLM-generated critique is treated as a gradient; backward pass is a textual gradient; forward pass is system execution.
- **Implication:** language-as-gradient is now a published, Nature-accepted formalization.

### DSPy

- **Paper/system:** Khattab, Singhvi, Maheshwari, et al. — DSPy framework. Stanford 2023–24.
- **Tagline:** *"Programming — not prompting — foundation models."*
- **Mechanism:** modules + signatures + teleprompters compose LLM pipelines declaratively; compile-time optimization over prompt-space.

### Why this is the right framing move for Syke

Prior framework-hunting (POMDP, FEP, world-models) was looking for the formalism in which Syke is an agent under scalar-loss optimization. GEPA/TextGrad/DSPy supply a *different* formalism: Syke is an agent under language-level optimization. This is:

- Defensible (top-tier authors, peer-reviewed, empirical)
- Mechanistically honest (language IS what Syke's synthesis uses)
- Operationally actionable (the concrete upgrade path is a GEPA-loop over the synthesis prompt against real ask-answer-judge data)

### Concrete upgrade path to self-improving Syke

1. **Rollouts = real-ask/answer/judge tuples** from the current eval pipeline (ab07, ab08, future).
2. **Reflection = LLM reading failure cases** and diagnosing against Codex's named failure modes (memex-bias / stale-route / overcompression / frozen-checkpoint / overcompleteness / totalizing-backlog).
3. **Prompt updates = mutations to `pi_synthesis.md`** generated by the reflection LLM.
4. **Pareto frontier = diverse synthesis variants** across failure-mode axes (not just highest-mean-judge-score).

This is the concrete "add in-loop optimization without touching model weights" move.

---

Last updated: 2026-04-18 (batch 7 added; detour closed)
