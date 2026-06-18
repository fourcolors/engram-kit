# Open-Ended Memory Eval Council — 2026-04-19

Status: working synthesis from 3-agent / 5-round web council
Scope: 2026 landscape for open-ended, non-fully-verifiable memory/agent evaluation

---

## 1. Bottom Line

The 2026 field is not treating open-ended eval as "one static rubric over one final answer" anymore.

The serious pattern is:

- environment-coupled tasks
- full-trajectory retention
- deterministic checks where possible
- LLM/human judging only for the residual semantic part
- explicit judge calibration and repeatability work

For memory specifically, the frontier is moving from:

- recall-only QA

toward:

- memory-in-action
- evolving truth over time
- multi-session dependence
- fragmented hidden-state reconstruction

But most published memory work is still cleaner and more curated than truly messy
real traces.

---

## 2. What The Field Is Actually Doing In 2026

### A. Hybrid scoring is the serious default

- executable / deterministic checks when the benchmark can support them
- bounded semantic judgment only for the residual

This shows up across:

- agent benchmarks like `OSWorld`
- trajectory eval papers like `TRAJECT-Bench` and `ATBench`
- platform practice in `Braintrust`, `LangSmith`, `Langfuse`

### B. Judge quality is now part of benchmark validity

The field is explicitly studying:

- judge identity variance
- self-preference bias
- bias-bounded evaluation
- imperfect verifier usefulness
- adversarial judge failure

So "use GPT as judge once" is no longer methodologically serious on its own.

### C. Trajectory is replacing answer-only evaluation

Credible agent evaluation increasingly retains:

- the whole trace
- intermediate tool steps
- session/thread context
- artifacts used by the agent

This is especially relevant for memory because many failures do not appear in the
final answer alone.

### D. Memory benchmarks are moving, but not finished

The new direction is clearly:

- multi-session
- memory used later in action
- state changes over time
- implicit or procedural memory pressures

But most benchmarks still stop short of full messy real-world fragmentation.

---

## 3. What Makes A Benchmark Credible Here

### Methodological non-negotiables

- formal environment contract
- explicit hidden state / observation boundary / contamination rules
- trajectory-coupled tasks, not answer-only tasks
- memory ablations with fixed base model and runtime
- deterministic verification core larger than the soft semantic residual
- judge-validity protocol with repeatability and sampled human audit
- separated failure classes
- discriminative power beyond generic base-model strength

### Operational non-negotiables

- immutable probe bundles
- hard time-bounded replay in execution, not just in the prompt
- full trace capture and retention
- versioned environment truth and replay artifacts
- conditional evaluator activation by ask type
- judge-calibration suite and re-baselining
- repeat trials on frozen bundles
- failure promotion from live traces into versioned offline corpora

### Anti-gaming non-negotiables

- repeated latent ask families over changing truth
- multi-surface partial observability with unresolved fragments
- style/judge perturbation testing
- derivation-path auditing
- uncertainty/abstention scoring
- mode-balanced tracks
- write-path stress, not just read-time answering

---

## 4. What Would Actually Be Ahead

What would be ahead is not saying "memory is more than recall."

The field already knows that.

What would be ahead is operationalizing all of this at once:

- bounded real traces
- repeated asks whose truth changes
- fragmented evidence surfaces
- useful continuation as the success object
- explicit separation of memory failure from runtime/agent/judge failure
- mostly deterministic scoring core with tightly residual semantic judgment
- evidence that rankings differ from recall-only or answer-only benchmarks

That would be a real methodological advance, not just different wording.

---

## 5. Where Future Systems Will Game 2026-Style Benchmarks

Frontier systems will solve the benchmark interface first.

Most likely shortcuts:

- plausible stale summaries that sound correct but restart the wrong branch
- judge-optimized rhetoric and provenance theater
- packaging heuristics instead of hidden-state reconstruction
- overfitting to dominant ask families
- benchmark-specific retrieval/update policies
- exploiting unmeasured write-path debt

So the benchmark should not reward:

- style over derivation
- recency-only success
- one-shot answer quality without update quality

---

## 6. The Best Difficulty-Increasing Move

The strongest future-proofing move per unit complexity is:

**repeated latent ask families over real evolving traces, with changing truth and surface-diverse evidence packaging**

Why this is so strong:

- breaks cached summaries
- breaks stale-memory reuse
- breaks shallow retrieval heuristics
- raises the value of actual state maintenance
- remains grounded in real traces rather than synthetic trick design

---

## 7. What Would Make The Benchmark Unserious

- no formal environment contract
- prompt-bounded rather than execution-bounded replay
- LLM judge as the primary truth source
- answer-only grading with no retained trajectory
- no judge calibration / no variance reporting
- no memory attribution under fixed base model/runtime
- tasks solvable from the final local context alone

---

## 8. Most Relevant Sources

### Research and benchmarks

- [OSWorld](https://arxiv.org/abs/2404.07972)
- [LoCoMo](https://arxiv.org/abs/2402.17753)
- [LongMemEval](https://arxiv.org/abs/2410.10813)
- [MemoryArena](https://arxiv.org/abs/2602.16313)
- [LifeBench](https://arxiv.org/abs/2603.03781)
- [Mem2ActBench](https://arxiv.org/abs/2601.19935)
- [Memory for Autonomous LLM Agents](https://arxiv.org/abs/2603.07670)
- [Survey on Evaluation of LLM-based Agents](https://arxiv.org/abs/2503.16416)
- [TRAJECT-Bench](https://arxiv.org/abs/2510.04550)
- [ATBench](https://arxiv.org/abs/2604.02022)

### Judge / verifier validity

- [CyclicJudge](https://arxiv.org/abs/2603.01865)
- [Bias-Bounded Evaluation](https://arxiv.org/abs/2603.05485)
- [Self-Preference Bias in Rubric-Based Evaluation](https://arxiv.org/abs/2604.06996)
- [Judging the Judges](https://arxiv.org/abs/2406.07791)
- [An Imperfect Verifier is Good Enough](https://arxiv.org/abs/2604.07666)
- [Gaming the Judge](https://arxiv.org/abs/2601.14691)
- [A Coin Flip for Safety](https://arxiv.org/abs/2603.06594)
- [ADVERSA](https://arxiv.org/abs/2603.10068)

### Practice / frameworks

- [Braintrust evaluate](https://www.braintrust.dev/docs/evaluate)
- [Braintrust score production traces](https://www.braintrust.dev/docs/observe/score-online)
- [LangSmith evaluation](https://docs.langchain.com/langsmith/evaluation)
- [LangSmith trajectory evals](https://docs.langchain.com/langsmith/trajectory-evals)
- [Langfuse evaluation core concepts](https://langfuse.com/docs/evaluation/core-concepts)
- [OpenAI trace grading](https://developers.openai.com/api/docs/guides/trace-grading)
- [OpenAI frontier-evals / PaperBench](https://github.com/openai/frontier-evals/blob/main/project/paperbench/README.md)
