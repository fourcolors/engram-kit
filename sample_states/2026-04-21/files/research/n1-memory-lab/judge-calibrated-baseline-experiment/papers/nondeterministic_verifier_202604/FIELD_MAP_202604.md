# Field Map — Non-Deterministically Verifiable LLM Judging (April 2026)

Scope: mining 2023–April-2026 literature for a judge design for *reconstructing hidden operative state `s_t` from a bounded evidence packet `o_{<=t}`*. Not a benchmark lookup; a position read.

Corpus: 33 PDFs in this directory. IDs verified (see section 8).

---

## 1. The Literature Term

The field does not yet have a single canonical term for the user's task class. Five competing terms are in active use, each from a different subfield:

| Term | Subfield | Who uses it | What it actually means |
|------|----------|-------------|------------------------|
| **non-verifiable domains / beyond-verifiable** | RLHF / reward modeling | Gunjal et al. 2025 (*Rubrics as Rewards*, 2507.17746); DeepSeek-GRM (2504.02495) | tasks where correctness has no programmatic check; judge signal is the reward |
| **open-ended generation / open-ended reasoning** | alignment & eval | *Self-Rewarding Rubric-Based RL* (2509.25534); *Reverse-Engineered Reasoning* (2509.06160) | generation with many valid outputs; no reference string |
| **reference-free evaluation** | NLG metrics lineage | Survey 2501.12011; G-Eval (2303.16634) | no gold-standard reference answer; typically the oldest term |
| **subjective / rubric-based evaluation** | HCI + LLM-judge | Prometheus (2310.08491); *Rethinking Rubric Generation* (2602.05125); RaR | judgment requires multi-criteria judgment not a bit of truth |
| **criterion-referenceable / construct-valid tasks** | psychometrics-meets-LLM | Yeadon et al. 2026 (2603.14732); Bean et al. 2025 (*Measuring what Matters*, 2511.04703) | tasks where observable features map cleanly to measurable criteria — the more specific framing |

**The closest term to what the Syke project is actually doing is "semi-verifiable / partially criterion-referenceable."** The Syke construct — reconstruct-for-continuation of a hidden operative state — is *partially* criterion-referenceable: some claims (time bounds, artifact existence, committed truth) are fully verifiable; some (live-thread selection, restart safety, operative adequacy) remain semantic. This hybrid is not a named literature term yet; it sits between Yeadon's "criterion-referenceable" (physics grading where the whole task is checkable) and the RLHF "non-verifiable domains" (where nothing is).

**Recommended naming move for the project:** use **"partially verifiable"** internally (explicit), tag individual claims `verified | inferred | speculative` (already in `JUDGE_DESIGN_LITERATURE_MAP_20260420.md` §4), and when writing externally cite "non-verifiable domains" (Gunjal) plus "criterion-referenceability" (Yeadon) as the two anchors. Do not overclaim a new category.

---

## 2. Papers Inventory

Surfaces: **MATH** = scoring math / reliability psychometrics; **PACKET** = evidence packet design / grounding; **PROMPT** = judge prompt / rubric structure; **AGENT** = judge architecture (panels, tools, abstention); **FOUNDATION** = task-class / construct-validity framing.

Files at `.../nondeterministic_verifier_202604/`.

| # | Cite | Title | arxiv | Surface | 1-sentence contribution | Downloaded |
|---|------|-------|-------|---------|-------------------------|-----------|
| 1 | Zheng+ 2023 | Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena | 2306.05685 | PROMPT + FOUNDATION | Established LLM-as-judge as paradigm; 80% GPT-4-to-human agreement as canonical baseline. | y |
| 2 | Liu+ 2023 | G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment | 2303.16634 | PROMPT | CoT + form-filling + probability-weighted summation for reference-free NLG scoring. | y |
| 3 | Kim+ 2023 | Prometheus: Inducing Fine-Grained Evaluation Capability | 2310.08491 | PROMPT + MATH | Open 13B evaluator LLM trained on 1K rubrics × 100K responses; matches GPT-4 correlation with humans. | y |
| 4 | Min+ 2023 | FActScore: Fine-grained Atomic Evaluation of Factual Precision | 2305.14251 | PACKET + PROMPT | Decompose long-form output into atomic claims; grade each against a knowledge source. Canonical claim-extraction paper. | y |
| 5 | Lightman+ 2023 | Let's Verify Step by Step | 2305.20050 | AGENT + MATH | Process reward over outcome reward; step-level verification beats final-answer check on reasoning. | y |
| 6 | Song+ 2024 | FineSurE: Fine-grained Summarization Evaluation | 2407.00908 | PROMPT + PACKET | Sentence-level fact-check + key-fact alignment; 86% balanced accuracy vs human at sentence level. | y |
| 7 | Verga+ 2024 | Replacing Judges with Juries (PoLL) | 2404.18796 | AGENT | A panel of smaller judges beats one big judge and is 7x cheaper; aggregation mitigates individual bias. | y |
| 8 | Jung+ 2024 | Trust or Escalate | 2407.18370 | AGENT + MATH | Cascaded selective evaluation with confidence-based escalation; provable human-agreement guarantees. | y |
| 9 | Tan+ 2024 | JudgeBench | 2410.12784 | FOUNDATION | Benchmark where preference = objective correctness, not crowd taste; GPT-4o barely beats random. | y |
| 10 | Zhuge+ 2024 | Agent-as-a-Judge | 2410.10934 | AGENT | Agent judges agent: tool-using, trajectory-reading judge with intermediate feedback, not just final-answer scoring. | y |
| 11 | Wu+ 2024 | LongMemEval | 2410.10813 | FOUNDATION | Multi-session chat memory benchmark with 5 capabilities incl. abstention and temporal updates; 30% drop vs short context. | y |
| 12 | Xie+ 2024 | OSWorld | 2404.07972 | FOUNDATION | Real-OS agent benchmark; humans 72%, best agent 12%; pure verifiable end-state checks. | y |
| 13 | Ye+ 2024 | Justice or Prejudice | 2410.02736 | AGENT + MATH | Quantifies 12 bias types in LLM judges; CALM automated bias audit framework. | y |
| 14 | Gu+ 2024 | A Survey on LLM-as-a-Judge | 2411.15594 | FOUNDATION | Canonical survey; organizes consistency, bias, and evaluation-of-evaluator literature. | y |
| 15 | Murugadoss+ 2024 | Evaluating the Evaluator | 2408.08781 | PROMPT | Detailed rubric prompts buy less than expected; perplexity can beat elaborate rubrics on some tasks. | y |
| 16 | Hashemi+ 2024 | LLM-Rubric | 2501.00274 | MATH + PROMPT | Multidimensional rubric + small NN that calibrates per-human-judge; 2x RMSE improvement. | y |
| 17 | Krumdick+ 2025 | No Free Labels | 2503.05061 | FOUNDATION + PACKET | Judges only work when they can answer the question; expert reference answers close the gap. | y |
| 18 | Liu+ 2025 | DeepSeek-GRM (Inference-Time Scaling for Generalist Reward Modeling) | 2504.02495 | AGENT + MATH | SPCT: train GRM to generate per-query principles + critiques; meta-RM vote scales reward at inference. | y |
| 19 | Gunjal+ 2025 | Rubrics as Rewards | 2507.17746 | MATH + PROMPT | Checklist-style rubrics as RL reward beyond verifiable domains; 31% gain on HealthBench over Likert. | y |
| 20 | Hu+ 2025 | MemoryAgentBench | 2507.05257 | FOUNDATION | Four core memory competencies (retrieval, test-time learning, long-range, selective forgetting); multi-turn format. | y |
| 21 | Feuer+ 2025 | When Judgment Becomes Noise | 2509.20293 | MATH + FOUNDATION | ~55% rubric variance unexplained; factor-wise rank corr >0.93 = dimensionality collapse; schematic adherence + psychometric validity diagnostics. | y |
| 22 | Sheng+ 2025 | Analyzing Uncertainty of LLM-as-a-Judge | 2509.18658 | MATH | First conformal-prediction framework for LLM judge scores with ordinal boundary adjustment; interval coverage guarantees. | y |
| 23 | Jacovi+ 2025 | FACTS Grounding Leaderboard | 2501.03200 | PACKET | Multi-judge leaderboard for grounding to 32k-token context; two-stage (eligibility then factuality) pipeline. | y |
| 24 | Bean+ 2025 | Measuring what Matters: Construct Validity in LLM Benchmarks | 2511.04703 | FOUNDATION | Systematic review of 445 benchmarks; many fail construct validity; 8 recommendations for new benchmarks. | y |
| 25 | Rao & Callison-Burch 2026 | Autorubric | 2603.00077 | MATH + PROMPT | Unified open-source rubric framework (binary/ordinal/nominal, ensemble, few-shot calibration, psychometric reliability). | y |
| 26 | Choi+ 2026 | Diagnosing LLM-as-Judge via Item Response Theory | 2602.00521 | MATH | GRM-IRT reliability framework separating intrinsic-consistency (prompt-variation stability) from human-alignment. | y |
| 27 | Hong+ 2026 | RULERS | 2601.08654 | PROMPT + PACKET | Locked rubrics as executable specs with deterministic evidence verification; smaller judges rival GPT-4. | y |
| 28 | Yeadon+ 2026 | Criterion-referenceability determines LLM-as-judge validity | 2603.14732 | FOUNDATION | Validity tracks criterion-referenceability; essay grading validity stays near zero regardless of instructions. | y |
| 29 | Zhu+ 2026 | CyclicJudge | 2603.01865 | MATH + AGENT | Variance decomposition (scenario/generation/judge/residual); round-robin judge assignment removes bias at single-judge cost. | y |
| 30 | He+ 2026 | MemoryArena | 2602.16313 | FOUNDATION | Interdependent multi-session agent-environment loop; LoCoMo winners collapse in agentic setting. | y |
| 31 | Cheng+ 2026 | LifeBench | 2603.03781 | FOUNDATION | Declarative + non-declarative (habitual, procedural) memory over real digital traces; SOTA memory 55%. | y |
| 32 | Badshah+ 2026 | SCOPE | 2602.13110 | MATH + AGENT | Bidirectional Preference Entropy for order-invariant pairwise judging; conformal coverage at 10% target error. | y |
| 33 | Zhang 2026 | Rethinking Atomic Decomposition for LLM Judges | 2603.28005 | PROMPT | Counter-evidence: holistic rubric matches or beats atomic-decomposed judges on 2/3 QA benchmarks. | y |

---

## 3. Convergences (>=3 papers agree)

**C1. Detailed prompts / bigger rubrics buy less than expected.** Murugadoss 2024; Feuer 2025 (factor collapse absorbs variance); Yeadon 2026 (validity tracks referenceability, not rubric detail). The binding constraint is *what the task lets you measure*, not *how many criteria you write*.

**C2. Judge reliability requires an external anchor (reference, evidence, criterion).** Krumdick 2025 (expert answers); Jacovi 2025 (context-grounded); Hong 2026 RULERS (evidence-anchored); Min 2023 FActScore (knowledge source); FineSurE 2024 (keyfact alignment). Free-form judges without anchors are unreliable, independent of model size.

**C3. Panels / cycling / ensembles beat single judges but do not fix rubric incoherence.** Verga 2024 PoLL; Zhu 2026 CyclicJudge; Ye 2024 CALM (bias quantification); Rao 2026 Autorubric (ensemble default). All four note the win is bias-reduction, not validity-creation; a broken rubric stays broken under a panel.

**C4. Rubric-based signals reduce judge-scale variance and stabilize small judges.** Gunjal 2025 RaR; Kim 2023 Prometheus; Liu 2025 DeepSeek-GRM (SPCT principles as dynamic rubrics); Hashemi 2024 LLM-Rubric. Rubric is a cheap stabilizer across judge scale.

**C5. Variance decomposition / psychometric diagnosis is now standard practice.** Feuer 2025 (schematic adherence + psychometric validity); Zhu 2026 CyclicJudge (variance components); Choi 2026 (IRT); Sheng 2025 (conformal); Rao 2026 (psychometric reliability metrics as first-class). The five *separately* claim the diagnostic stack as the right next move — convergent evidence that the field has left "just report accuracy" behind.

**C6. Open-ended / memory agent tasks collapse existing benchmarks.** Hu 2025 MemoryAgentBench; He 2026 MemoryArena ("LoCoMo winners perform poorly"); Cheng 2026 LifeBench ("SOTA 55%"); Wu 2024 LongMemEval (30% drop). Multi-session / interdependent memory is the visible frontier and *reconstruction-for-continuation* is where current benchmarks hit a wall.

---

## 4. Open Contradictions

**X1. Atomic decomposition: required or overrated?**
- **Pro:** FActScore (Min 2023), FineSurE (Song 2024), Autorubric (Rao 2026) — decompose into atomic units; grade each.
- **Against:** Zhang 2026 (*Rethinking Atomic Decomposition*) shows holistic rubric matches or beats atomic on 2/3 QA benchmarks, especially when incompleteness matters.
- **Reading:** atomic is necessary when claims are independent (factuality); it can underperform when the *holistic coherence* is part of the quality signal (reconstruction-for-continuation probably is). This directly matters for Syke.

**X2. Bigger judge vs jury of small judges.**
- **Pro-big:** Krumdick 2025 (judge must be able to answer); Zheng 2023 (GPT-4 > all).
- **Pro-jury:** Verga 2024 PoLL; Liu 2025 DeepSeek-GRM (inference-time scaling with multiple samples).
- **Reading:** for verifiable-ish tasks, strong single judge + reference beats a panel. For genuinely subjective tasks, diverse panels reduce bias more than more compute in one judge. Syke's task is in between — supports a *small cycled panel over reference-anchored claims* rather than either extreme.

**X3. Fine-grained scales vs coarse categories.**
- **Pro-fine:** LLM-Rubric (Hashemi 2024) 1–4 continuous calibrated to humans; DeepSeek-GRM pointwise.
- **Pro-coarse:** Feuer 2025 and the project's own observation that flicker concentrates at adjacent bands; Gunjal 2025 checklist beats Likert.
- **Reading:** coarse categorical (present/absent, pass/partial/fail) is more robust when rubric incoherence is the dominant noise source.

**X4. Rubric generation — human vs LLM vs hybrid.**
- **Human-only:** Prometheus's original Feedback Collection.
- **Synthetic (LLM-generated):** OpenRubrics (2510.07743); RaR 2025 builds a 10k-scale corpus.
- **Hybrid best:** 2602.05125 *Rethinking Rubric Generation* argues LLM-drafted rubrics lack coverage and conflate dimensions; humans must repair.
- **Reading:** fully synthetic rubrics are the field's recent bet, but coverage / collapse problems replicate the *When Judgment Becomes Noise* pathology.

---

## 5. Gaps Relative to the Syke N=1 Project

**G1. No literature object for "partially verifiable operative-state reconstruction."**
Closest: Yeadon 2026 (*criterion-referenceability* — the right construct-validity frame but defined per-subtask, not per-claim); Min 2023 FActScore (per-claim but factuality only, not operative-state adequacy). **Nothing** names the Syke hybrid where *some* primitives (`time_local_correctness`, `committed_state_fidelity`) are hard-verifiable and others (`wrong_restart_risk`, `live-thread selection`) remain semantic. The project can claim this hybrid as genuinely novel framing, backed by `verified|inferred|speculative` claim typing in its existing judge literature map §4.

**G2. No n=1 judge psychometrics.**
All the psychometric work (Feuer 2025, Choi 2026 IRT, Zhu 2026 CyclicJudge) assumes many asks × many models × many judges. The Syke packet is one user × many sessions × small item count. **No paper** adapts variance decomposition / IRT to this regime. Closest: Hashemi 2024 LLM-Rubric, which trains per-judge parameters but still requires judge population; not the same. This is a real gap the project could write into.

**G3. Bounded filesystem as evidence packet.**
Packet-design literature (Jacovi 2025 FACTS, Hong 2026 RULERS) treats the packet as a single long-context document or retrieved set. The Syke packet is a *bounded, structured filesystem with provenance*. No paper models packets this way. Closest: FACTS Grounding for the 32k-token bounded-context shape; OSWorld for the filesystem shape — but OSWorld's judge is end-state-deterministic, not reconstruction-based.

**G4. Continuity across sessions as a judge dimension.**
LongMemEval 2024 tests "multi-session reasoning" but grades final answer, not continuity per se. MemoryArena 2026 tests interdependent tasks but from agent-performance side, not judge side. The Syke "continuity" axis — stale-vs-live revision, object continuity across sessions — is **not** a named dimension in any judge rubric in this corpus.

**G5. Efficiency-as-compression as a judged construct.**
Efficiency in OSWorld / Agent-as-a-Judge is tracked (steps, cost) but not *judged* semantically. The Syke question "was this reconstruction compressed to its minimum sufficient scope?" is unnamed. Closest: FineSurE's conciseness metric (ratio of on-keyfact sentences). That's a summarization-specific proxy; no one has generalized it.

**G6. Reconstruction-for-continuation as a success criterion.**
All task-class papers use either (a) answer-correctness (JudgeBench, Wu 2024), (b) task-completion (OSWorld, Agent-as-a-Judge), or (c) preference (MT-Bench). **None** uses "does this reconstruction let the system resume safely?" as the success criterion. This is again where the Syke `wrong_restart_risk` primitive lives and has no prior art.

---

## 6. State of the Art — One Paragraph Each

**MATH.** The reliability stack has consolidated around four layers: (a) variance decomposition that separates task / generation / judge / residual contributions (CyclicJudge 2026, Feuer 2025); (b) psychometric validity — schematic adherence, factor collapse detection, discriminant validity (Feuer 2025, Rao 2026); (c) IRT-style graded response modeling for separating intrinsic judge consistency from human alignment (Choi 2026); (d) conformal prediction for per-instance uncertainty intervals with coverage guarantees (Sheng 2025, Badshah 2026 SCOPE). The move from "report Cohen's kappa" to "report variance components + coverage" is the clearest frontier shift since 2024.

**PACKET.** Evidence-packet design is the least mature surface. Current consensus is two-stage grounding: (1) eligibility gate (does the response address the prompt at all — Jacovi 2025 FACTS) and (2) claim-level verification against the supplied context (FActScore 2023, FineSurE 2024, RULERS 2026). The packet itself is still modeled as a blob of tokens; nobody treats it as a structured object with provenance graphs. The Syke filesystem+provenance packet is ahead of this.

**PROMPT.** Rubric-prompt design has shifted from "write detailed criteria" (G-Eval, Prometheus) to "executable checklist" (RaR, RULERS) to "per-criterion atomic grading with verdict typing" (Autorubric 2026). The surprising correction (Zhang 2026) is that atomic isn't always best — holistic matches atomic when coherence is the construct. Structured decoding / form-filling is now table stakes. Rubric-scale (binary/ordinal/nominal) is a first-class design choice not an afterthought.

**AGENT.** Judge-as-agent architectures are the fastest-moving layer. Single-call judges (MT-Bench lineage) have been overtaken by: panels (PoLL 2024), cycled panels (CyclicJudge 2026), cascaded selective judges with confidence-based escalation (Trust-or-Escalate 2024), tool-using trajectory-reading agent judges (Agent-as-a-Judge 2024), and generative reward models that produce principles + critiques and are scaled at inference time (DeepSeek-GRM 2025). The consensus primitive is *separable-stage judging* (claim-extraction, per-claim grading, aggregation) with abstention as a first-class output.

**FOUNDATION.** Construct validity is now the explicit frame (Bean 2025, Yeadon 2026). The field has named its failure mode: benchmarks measure proxy constructs, not intended ones; schematic incoherence hides behind aggregate scores (Feuer 2025). The multi-session memory cluster (MemoryArena, MemoryAgentBench, LifeBench, LongMemEval) has collectively shown that long-context LLM winners do *not* transfer to interdependent memory tasks. This is the cleanest opening for a new task class — which the Syke project is positioned to fill.

---

## 7. Recommendations for Next-Iteration Judge Design

**R1. Keep claim typing (`verified | inferred | speculative`) but make the typing a first-stage extractor, not a judge-side prompt slot.** Min 2023 (FActScore) and Rao 2026 (Autorubric) both show that per-claim atomic extraction before grading gives stable signal. Yeadon 2026 and Feuer 2025 jointly imply that the *verified* claims should get reference-grounded binary scoring and the *speculative* ones should get a separate ordinal-with-abstention track. Do not grade them on one rubric.

**R2. Replace the current 12-subcategory rubric with a small-primitive checklist scored binary/tri-state with an explicit abstention primitive.** Gunjal 2025 RaR shows checklist-style reward reduces variance for smaller judges; Feuer 2025 shows your current factor-collapse (one sub-axis absorbing 70% of variance) is exactly the failure mode a collapsed rubric predicts; the Syke 42% adjacent-band flip rate is the signature Autorubric's binary/ordinal separation targets. Move to 5–7 binary primitives + abstention, not 12 ordinal sub-categories.

**R3. Make the judge contract evidence-anchored: require the judge to cite a packet location for every affirmative claim.** RULERS (Hong 2026) operationalizes this; FACTS Grounding (Jacovi 2025) shows the two-stage eligibility→evidence pipeline. This is also what closes the GPT-vs-Opus divergence (project's own literature map §4): the judges disagree because neither is forced to cite. A required citation turns a semantic disagreement into a packet-lookup disagreement.

**R4. Rejudge the existing packet before collecting new data, and report variance components not κ alone.** Zhu 2026 CyclicJudge gives the decomposition formula (scenario / generation / judge / residual); Feuer 2025 gives schematic adherence; Rao 2026 gives the composite reliability metric. The project's current κ=0.24 + 42% flip is an uninterpretable scalar until variance is decomposed. *Run the decomposition, then decide whether to collect more.*

**R5. Use a cycled 2-judge panel (not a single judge, not a 5-judge PoLL) as the next-iteration protocol.** Verga 2024 (PoLL) is overkill for n=1 packet size; Zhu 2026 shows a round-robin assignment is optimal at single-judge cost; Jung 2024 (Trust-or-Escalate) provides the abstention/escalation scaffold for when the two disagree. This matches both the Syke budget and the project's own next-step sequence.

*(Deliberately not recommended yet: IRT parameter fitting, conformal intervals, fine-grained continuous scales, tournament/pairwise. The rubric must be coherent first. This agrees with the project's §5 "not yet" list.)*

---

## 8. Verification Ledger

Every entry: ID verified via arxiv landing page fetch (title+authors confirmed). Download = PDF present, >20KB, PDF header.

| arxiv ID | Verified | Downloaded | Filename |
|----------|----------|-----------|----------|
| 2306.05685 | y | y | 2023_zheng_mt-bench-llm-as-judge.pdf |
| 2303.16634 | y | y | 2023_liu_g-eval.pdf |
| 2310.08491 | y | y | 2023_kim_prometheus.pdf |
| 2305.14251 | y | y | 2023_min_factscore.pdf |
| 2305.20050 | y | y | 2024_lightman_lets-verify-step-by-step.pdf |
| 2407.00908 | y | y | 2024_song_finesure.pdf |
| 2404.18796 | y | y | 2024_verga_poll-panel.pdf |
| 2407.18370 | y | y | 2024_jung_trust-or-escalate.pdf |
| 2410.12784 | y | y | 2024_tan_judgebench.pdf |
| 2410.10934 | y | y | 2024_zhuge_agent-as-a-judge.pdf |
| 2410.10813 | y | y | 2024_wu_longmemeval.pdf |
| 2404.07972 | y | y | 2024_xie_osworld.pdf |
| 2410.02736 | y | y | 2024_ye_justice-or-prejudice.pdf |
| 2411.15594 | y | y | 2024_gu_survey-llm-as-judge.pdf |
| 2408.08781 | y | y | 2024_murugadoss_evaluating-evaluator.pdf |
| 2501.00274 | y | y | 2024_hashemi_llm-rubric.pdf |
| 2503.05061 | y | y | 2025_krumdick_no-free-labels.pdf |
| 2504.02495 | y | y | 2025_liu_deepseek-grm.pdf |
| 2507.17746 | y | y | 2025_gunjal_rubrics-as-rewards.pdf |
| 2507.05257 | y | y | 2025_hu_memoryagentbench.pdf |
| 2509.20293 | y | y | 2025_feuer_when-judgment-becomes-noise.pdf |
| 2509.18658 | y | y | 2025_sheng_conformal-judge.pdf |
| 2501.03200 | y | y | 2025_jacovi_facts-grounding.pdf |
| 2511.04703 | y | y | 2025_bean_measuring-what-matters.pdf |
| 2603.00077 | y | y | 2026_rao_autorubric.pdf |
| 2602.00521 | y | y | 2026_choi_irt-llm-judge.pdf |
| 2601.08654 | y | y | 2026_hong_rulers.pdf |
| 2603.14732 | y | y | 2026_yeadon_criterion-referenceability.pdf |
| 2603.01865 | y | y | 2026_zhu_cyclicjudge.pdf |
| 2602.16313 | y | y | 2026_he_memoryarena.pdf |
| 2603.03781 | y | y | 2026_cheng_lifebench.pdf |
| 2602.13110 | y | y | 2026_badshah_scope.pdf |
| 2603.28005 | y | y | 2026_zhang_rethinking-atomic-decomposition.pdf |

All 33 IDs from the project's existing `JUDGE_DESIGN_LITERATURE_MAP_20260420.md` were re-verified against arxiv landing pages during this pass. **No fabricated IDs were found** — every ID in the project's original list resolves to a paper whose title and abstract match the project's description. See `SEARCH_LOG_202604.md` for the raw search log.
