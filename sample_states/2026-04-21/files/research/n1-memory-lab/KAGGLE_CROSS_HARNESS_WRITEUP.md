# Cross-Harness Contextual Reconstruction: A Real-World Evaluation Direction for Personal AI Memory

### Team
Syke — independent research

### Problem Statement

When a person actually uses AI tools throughout their day, a specific memory problem emerges that existing benchmarks do not touch: **contextual reconstruction across harnesses.** A user works in Claude Code, switches to Codex, uses OpenCode for one thing, queries Hermes for research. Each tool has a session. Each session is blind to the others. Every time the user wants to pick up where they left off — in *any* tool — the underlying memory system has to reconstruct the relevant slice of their cognitive state from traces scattered across tools, time, and formats.

This is not retrieval. There is no pre-stored "answer." The correct answer is assembled on demand from partial, asynchronous, differently-formatted observations — about real work that was evolving while it was happening. Current memory benchmarks test recall on stored content. What personal AI memory actually does is **inference over fragmented multi-source observations about a non-stationary subject.** The two tasks don't transfer.

This submission proposes reconstruction as the evaluation primitive, describes the environment and the agent's interface, and outlines deterministic evaluation directions we are actively pursuing. The goal is methodological: a real-usage benchmark surface that the field can build on.

### Task & Benchmark Construction

A reconstruction task has this shape:

- **Environment**: a user with multiple AI harnesses active. Each writes a trace (JSONL, SQLite, message log). Traces are partial, asynchronous, redundant in places, silent in others.
- **Memory system**: reads traces on a cycle, maintains durable state (memories + sparse links + a compressed projection the user and agents both consume).
- **Reference cutoff**: a timestamp `t` at which the reconstruction is evaluated.
- **Ask**: a natural question about the user's state at `t` — "what are my open threads?", "what did Codex do after my last Claude Code session?", "what did I decide about X?"
- **Slice**: the frozen multi-harness data up to `t`.
- **Evaluation**: does the answer reconstruct the user's actual state at `t`, grounded in the slice, appropriately hedged on claims the slice doesn't support?

We did not design tasks. Six weeks of one user's real cross-harness usage produced 310 naturally-occurring asks. Clustering by structure: cross-harness binding (21%), decision provenance (8%), research context (8%), temporal delta (7%), state recovery (6%), active threads (5%), causal reconstruction (4%). Each is a reconstruction task by construction.

### The Environment, Precisely

What the agent receives at query time:

- A natural-language question
- Access to the slice (raw harness data up to reference cutoff)
- A compressed durable-state projection (~4000 tokens) — itself the output of prior reconstructions
- The option to query the sparse relational graph of memories directly
- Cycle metadata (synthesis history, last pass time)

What the agent does NOT receive:

- A canonical pre-stored answer
- Labels on observation streams
- External help or human oversight at query time

This is the realistic interface any personal memory agent has. Reconstruction is the task of producing, from these inputs alone, an answer that a ground-truth observer (here: the user) would recognize as faithful.

### Deterministic Evaluation Direction

The harder question: how do you score reconstruction quality reproducibly? Five directions we are actively pursuing:

1. **Reference existence** — for claims naming files, commits, memory IDs, dates, check whether those references exist in the slice. Programmatic per-claim.
2. **Temporal fidelity** — parse every date/time in the answer; check against reference cutoff. Bounded.
3. **Cross-harness binding** — for binding asks, verify answer references sources from each required harness. Binary.
4. **Belief stability** — rerun with temperature=0, compute output distance across reruns. Directly measures model + judge noise.
5. **Held-out predictive compression** — at time `t` snapshot memory state; at `t+k` measure how much that state compresses incoming observations. Information-theoretic; MDL principle applied directly to the log.

Axes that genuinely require semantic judgment (we don't pretend otherwise):

- **Actionability** — would the answer let the user resume work?
- **Epistemic calibration** — did the answer hedge on unverified claims?

These use an LLM judge as auxiliary calibrator with explicit variance reporting (ensemble judging, temperature=0, rubric-gated). The deterministic layer is primary; semantic judgment is the residual.

### Inspirations, Not Claims

We draw on several theoretical traditions, not reinventing them:

- **POMDP belief state** (Kaelbling et al.; He et al. 2026 for MemoryArena) — memory as sufficient statistics for a hidden-state posterior given observations.
- **Free energy principle** (Friston) — the synthesis cycle as a step of variational inference minimizing F = KL[q(s)‖p(s|o)] − accuracy.
- **Markov blankets** — a memory process maintains a statistical boundary between internal state (memories, projection) and external observations (raw traces). Private state is, by construction, the interior of a Markov blanket.
- **Hippocampal indexing** (Teyler & Rudy) — consolidation from episodic traces into semantic structure.
- **Autobiographical continuity** (Bluck et al.) — narrative self across discontinuous experience.

The claim is not a new theory. The claim is that **cross-harness contextual reconstruction is the ecologically valid evaluation primitive**, current benchmarks do not measure it, and the mathematics needed to formalize evaluation already exists in these traditions. The engineering work is the path toward that formalization.

### Privacy as a Cognitive Axis

The data that makes reconstruction hard is, by nature, private — health context, financial context, business context, relationships, unreleased work. Public benchmarks cannot contain this content without violating the property being measured. Privacy sits on the cognitive side of the problem, not the deployment side:

- Personal memory lives inside a Markov blanket. Evaluating it requires respecting that blanket.
- Alignment of personal AI requires auditing behavior on data the auditor cannot see — a problem current methodology does not solve.
- A benchmark that requires disclosing the corpus shifts the task to a domain where the failure modes we care about disappear.

Methodology proposal: evaluation runs locally on private corpora; only aggregate per-axis distributions are shared publicly. Consistent with arxiv 2502.09316 (judge-free benchmarking) and 2604.07666 (imperfect-verifier tolerance) as current field direction.

### What Else the Benchmark Should Measure

Reconstruction is the first primitive. A mature personal-memory benchmark would also cover:

- **Self-observation** — can the memory system detect recurring patterns in its own ask history and pre-compute anticipated reconstructions? This is procedural memory; active research direction.
- **Architectural variation** — how reconstruction quality depends on prompt structure, synthesis frequency, graph topology. Hyperagent architectures where the memory system modifies its own observation schedule open a new axis.
- **Efficiency per unit of reconstructed state** — tool calls, token cost, latency. Approximates the complexity term in the free-energy decomposition; implicit state-machine telemetry currently in active instrumentation.

These are directional, not contributions of this submission.

### Dataset

- 310 real asks over 6 weeks across 4 harnesses (Claude Code, Codex, OpenCode, Hermes), with naturalistic taxonomy
- Sample redacted slices demonstrating variability (cross-harness binding, temporal delta, decision provenance) — structure preserved, content stripped
- Methodology documentation for equivalent task generation on any user's own multi-harness data
- Aggregate per-axis score distributions from the private corpus

Full corpus is not public: the content contains third-party personal information (health context, business relationships, financial state) that we do not have the right to release. Methodology is fully reproducible on any user's own data.

### Technical Details

Scoring pipeline: three-axis, separating deterministic programmatic checks (reference existence, temporal fidelity, binding, stability) from semantic LLM-judged axes (actionability, calibration). Judge hardening in active development: temperature=0, per-probe rubric gates enforced as hard constraints (not advisory context), failure-bucket decomposition (runtime / refusal / reconstruction-fail separated), ensemble judging across multiple judge models to reduce single-judge variance below 15%. Fast numerical checks are bounded-cost and bit-reproducible given slice and output.

### Results and Insights

Early runs surfaced two signals worth reporting: (1) without calibration as an explicit axis, single-axis grounding judges can rank systems that hedge honestly below systems that confidently assert — a calibration-blindness failure mode. (2) Without temperature control, LLM judges on naturalistic reconstruction tasks can flip 30%+ of verdicts across identical reruns. Both are specifically fixed by the judge hardening described above; results from the hardened run are forthcoming.

### Organizational Affiliations

Syke — independent research on personal cross-harness AI memory.

### References & Citations

- He et al. 2026, MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks (arxiv 2602.16313)
- Du 2026, Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers (arxiv 2603.07670)
- DeepMind 2026, Measuring Progress Toward AGI: A Cognitive Framework
- Kaelbling, Littman, Cassandra 1998, Planning and acting in partially observable stochastic domains
- Friston 2010, The free-energy principle: a unified brain theory?
- Teyler & Rudy, The hippocampal indexing theory of memory
- Bluck et al., Autobiographical continuity and the narrative self
- arxiv 2604.07666 (April 2026), Imperfect verifier is good enough
- arxiv 2505.20854, SE-Jury ensemble judge
- arxiv 2502.09316, Judge-free benchmarking