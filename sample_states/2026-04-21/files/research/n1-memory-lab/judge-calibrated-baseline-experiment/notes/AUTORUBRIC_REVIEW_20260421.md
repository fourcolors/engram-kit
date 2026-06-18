# Autorubric for Partially Verifiable Operative-State Reconstruction — A Fit Assessment

*Reviewing Rao & Callison-Burch 2026 (arxiv 2603.00077) against the Syke n=1 memory benchmark. Cross-referenced against Zhang 2026 (arxiv 2603.28005) for the atomic-decomposition question.*

Date: 2026-04-21.

---

## 1. One-paragraph TL;DR

**Yellow light.** Autorubric is a strong *framework contribution* — it consolidates rubric-based LLM evaluation into one library with opinionated defaults (binary/ordinal/nominal criteria, ensemble judging, few-shot calibration with verdict balancing, abstention primitive, psychometric reporting), and several of its components (abstention via `CANNOT_ASSESS`, verdict-balanced few-shot, per-criterion atomic grading, per-weight-band κ reporting) transfer cleanly to the Syke task class. But Autorubric assumes (i) a flat prompt+submission pair, not a structured filesystem packet with provenance; (ii) that all criteria are the same *kind* of claim (the framework has no notion of `verified`/`inferred`/`speculative` typing); and (iii) that rubric quality is an input, not a thing to be measured — the paper explicitly flags this as the unresolved "primary open problem" (§8, p.9). R1 (claim typing) and the structured-packet adaptation are genuinely *out of scope* for Autorubric as delivered; R2 (small-primitive rubric) and R4 (variance/psychometric reporting) are close to drop-in.

---

## 2. What Autorubric actually is

Autorubric is an **open-source Python framework** (MIT, `autorubric.org`) plus three validation benchmarks. It is deliberately positioned as a *consolidation* — not a new scoring method. Its contribution is bundling existing rubric-evaluation lessons (ensemble judging from PoLL, position-bias mitigation from Wang 2023, few-shot calibration, verdict-balanced sampling, abstention) behind one API with opinionated defaults (abstract §1 p.1; contributions list §2 p.2).

**Concrete components.**

- **Rubric data model** (Listings 1–3, pp.15). A `Rubric` is a list of `Criterion` objects, each with `weight`, `requirement` (natural-language), and `scale_type` ∈ {binary, ordinal, nominal}. Weights can be positive (reward) or negative (penalty for anti-patterns). Aggregation is a weighted sum clamped to [0,1] (Eq. 1, p.3). *Continuous-valued criteria are intentionally excluded* (p.3) because LLM calibration on unbounded numeric scales is poor.
- **Three scoring scales, one rubric.** Binary (MET/UNMET), ordinal (3–5 level Likert with behavioral anchors — narrow scales preferred to combat central-tendency bias, p.2–3), nominal (unordered categories, e.g. error types). Autorubric supports *heterogeneous mixtures* in a single rubric. This is validated on CHARM-100 (§4.3, p.5, a new 100-item dataset the paper introduces).
- **CriterionGrader**: issues N × M concurrent LLM calls (N judges × M criteria) with per-criterion prompts, option shuffling for position-bias mitigation, and response caching (Fig. 1, p.2). Each criterion is evaluated in a *separate LLM call* to prevent halo effects (p.3).
- **Ensemble & aggregation** (Listing 4, p.16). Supports single judge or diverse-model panels with majority / weighted / unanimous / any-vote aggregation. Default in reported experiments is *single judge* with verdict-balanced 3-shot calibration (Table 5 default hyperparameters, p.22).
- **Few-shot calibration** (Listing 5, p.16). Verdict-balanced sampling — equal MET/UNMET exemplars per criterion — to prevent base-rate prior inference (Hong 2026). On RiceChem, this lifts accuracy from 77.2% (zero-shot) to 80.0% (5-shot), with statistical significance via McNemar (p=0.023, Table 2 p.4).
- **Abstention primitive**: `CANNOT_ASSESS` verdict with configurable handling (`SKIP`, `ZERO`, `PARTIAL`, `FAIL`; Listing 8, p.18). Default is `SKIP` (adjusts denominator, doesn't penalize the submission for the judge's own uncertainty).
- **Mandatory explanation field** with citation — the default binary prompt (Listing 12, p.21) requires "Cite specific text from the submission as evidence for your verdict."
- **Psychometric reliability reporting** (Listing 10, p.19; sample report Listing 14, p.24). Cohen's κ, quadratic-weighted κ, intraclass correlation, Earth Mover's Distance, Spearman/Kendall/Pearson, bootstrap CIs, mean-bias analysis, per-criterion breakdown. The paper explicitly grounds this in McKeown & Lenarcic Biss 2018 and Comer 2009 psychometrics (§7, p.9; §B.2, pp.18–19).
- **Three benchmarks validated**: RiceChem (college chemistry, 1240 responses × 27 binary criteria, Gemini-3-Flash hits 80% with 5-shot, §4.1), ResearcherBench (deep-research systems, 931 criteria, 5586 criterion-judgments, §4.2), CHARM-100 (mixed-type chatbot eval, 87% binary accuracy κ=0.642, ordinal 38–58% exact / 85–93% adjacent, Fig. 2 p.6).
- **Two downstream applications**: agent skill improvement via per-criterion feedback loop (§5, raises peer-review agent from 0.47 → 0.85; Fig. 3 p.7) and RL with rubric-based rewards on AdvancedIF (§6, +0.039 Wilcoxon p=0.032, d=0.26; Fig. 4 p.8).

**What it is NOT.** Not a new judge model. Not a reference/evidence extraction system. Not a claim-typing system. Not a packet-structuring system. Not a rubric-quality validator — §8 p.9: "rubric quality assessment at scale remains the primary open problem."

---

## 3. Components that transfer cleanly

### R1 — Claim typing as pre-judge extractor stage: **NO, does not transfer.**

Autorubric has no claim-typing stage. Criteria are authored flat and evaluated flat. The mandatory explanation field (Listing 12, p.21) requires the judge to *cite evidence* but does not require the judge to classify the claim as `verified | inferred | speculative`. The paper's atomic decomposition (*per-criterion*, not *per-claim*) is upstream of the submission — it decomposes the *rubric*, not the *candidate answer*. FActScore-style claim extraction from the response is not in the framework. If the user wants R1, Autorubric supplies nothing on this axis; the user must build the typer separately and then use Autorubric to grade the typed claims (and even then — see §4 below — they'd need to author separate rubrics per claim type).

### R2 — Replace 12-subcategory rubric with 5–7 binary primitives + abstention: **YES, transfers directly.**

This is the single cleanest transfer. Autorubric's default binary criterion type (Listing 2, p.15) with `CANNOT_ASSESS` abstention (Listing 8, p.18) is *exactly* the shape R2 prescribes. The paper's §8 discussion (p.9) explicitly argues for binary where possible: "prefer binary criteria where possible, reserve ordinal scales for cases where gradation is essential." CHARM-100 validates this: factual accuracy (binary) hits κ=0.642 vs ordinal criteria at 0.549–0.625 (Fig. 2, p.6). RiceChem is *entirely binary* (27 criteria) and hits 80% accuracy. Verdict-balanced few-shot (Listing 5) and the `SKIP` default for unassessable items are opinionated in the same direction R2 wants. The weight-band analysis (Table 21, p.33) — reporting κ separately for weight=1 (nice-to-have), weight=2 (supporting), weight=3 (core) — also transfers: this is the substrate for the Syke "universal primitives vs conditional primitives" split in `JUDGE_DESIGN_LITERATURE_MAP_20260420.md`.

### R4 — Rejudge and report variance components, not κ alone: **PARTIAL.**

Autorubric reports a rich psychometric stack (Listing 10 p.19, sample report p.24): κ, weighted κ, ICC, EMD, Spearman, bootstrap CIs, mean-bias analysis, per-criterion breakdown. This is already more than the project's current κ-only reporting. *But* Autorubric does **not** implement the CyclicJudge-style variance decomposition (scenario / generation / judge / residual) that R4 really wants — Table 21 (p.33) does a *weight-band* disagreement analysis and Section 4.4 does a *mitigation ablation* (leave-one-out per mitigation), not a variance-components decomposition. The framework will give the user everything except the decomposition itself, which has to be layered on. Good news: since the framework stores per-criterion, per-judge verdicts in `items.jsonl` (§B.3, p.19), computing the decomposition on top is straightforward; the data shape is right.

---

## 4. Components that need adaptation

### Packet shape: structured filesystem vs blob prompt.

Autorubric's input is `(prompt, submission)` — a string prompt and a string submission (Listing 4, p.16: `rubric.grade(to_grade=response, query=prompt)`). None of the three validation benchmarks exercises a structured-provenance packet: RiceChem is a chemistry question + ~120-word response; ResearcherBench is a research question + long-form answer; CHARM-100 is a single-turn chatbot conversation. **The framework has no first-class concept of packet structure, provenance metadata, or session boundaries.** Adaptation: the user will need to serialize the packet into the submission string (injecting explicit `<path>...</path>` markers and `<provenance>...</provenance>` tags), and the rubric wording will need to explicitly direct the judge to cite file paths in its explanations. The default binary prompt (Listing 12) already says "Cite specific text from the submission as evidence" — the user can strengthen this to "cite file path + line range." This is a prompt-engineering adaptation, not a framework limitation, but the user gets zero help from Autorubric on the packet-structuring side.

### Claim typing by verifiability level.

As noted in §3 R1: Autorubric treats all criteria as the same kind of claim. In practice, the user wants *different judge behavior* for verified (exact match against artifact existence / SHA / timestamp), inferred (logical implication chain from evidence), and speculative (narrative — should abstain or be flagged). Autorubric's abstention mechanism (`CANNOT_ASSESS`) is single-axis — it captures "I can't tell", not "this claim is outside the verifiable envelope." The adaptation is to either (a) run three separate rubrics (one per claim type) and compose scores externally, or (b) encode claim type as nominal criterion (per Listing 2 p.15) that every claim must be tagged with before grading. Either way, the framework does not support this natively.

### Cross-criterion interdependence.

Autorubric evaluates each criterion *in a separate LLM call* (§2 p.3: "Each criterion is evaluated in a separate LLM call to prevent halo effects"). For Syke primitives this is mostly fine but problematic for interdependent pairs — e.g., `time_local_correctness` and `object_continuity` are not independent; a wrong object identification breaks temporal reasoning and vice versa. Autorubric's independence assumption will *underweight* cascading failures: the judge scores `object_continuity=UNMET` in one call and `time_local_correctness=MET` in another, even when the latter is only "MET" because it accepted the wrong object anchor from the former. This is a known Autorubric property (the halo-effect mitigation is the same mechanism that breaks interdependent scoring), and there is no built-in fix. Adaptation: either accept the conservatism, or layer a post-hoc "coherence check" step outside the framework.

### Ordinal scale handling.

Autorubric's ordinal handling is the weakest of its scales (CHARM-100 exact accuracy 38–58% vs 87% binary; Fig. 2, p.6). The paper's own guidance (§8 p.9) is to report *adjacent accuracy* and *rank correlation* rather than exact κ for ordinal — "the judge is usually within one step of ground truth but clusters toward scale extremes." For the Syke current 3-level ordinal rubric this is a direct warning: the 42% adjacent-band flip rate the project has already measured is the *expected pattern* Autorubric's own results replicate. Adaptation is straightforward — but in the direction of *abandoning ordinal* (R2), not rescuing it.

---

## 5. Components that do not transfer / are misleading

### "Autorubric's binary scoring is reliable" does not imply "binary scoring is reliable for operative-state reconstruction."

Autorubric's binary validation is on **rubric entailment** (RiceChem: does this student answer satisfy this criterion about Coulomb's Law?) and **coverage** (ResearcherBench: is this finding present?). Both task classes are *local, independent, reference-anchored* claims. The Syke task is *global, interdependent, packet-conditioned* reconstruction. Transferring Autorubric's binary-accuracy numbers would be wrong: 87% factual-accuracy binary κ on CHARM-100 is achieved on a dataset specifically designed for *"cross-criteria conflicts"* (§4.3, p.5) where factual accuracy is orthogonal to stylistic criteria. The Syke primitives are not orthogonal. Adopting binary without accounting for primitive interdependence (see §4 above) would inflate apparent reliability.

### Few-shot calibration transfer.

Verdict-balanced 3-shot calibration (Listing 5) transfers *syntactically* but requires a training split the Syke project does not have at n=1 packet scale. RiceChem uses an 80/10/10 train/val/test split with 992 training examples per criterion (Table 6 p.25: ~300 students × 27 criteria). The user cannot generate that from one packet. The paper's "cold-start" experiment (§D.7, Table 16 p.30) drops accuracy by ~15pp when few-shot examples come from different questions — so cross-packet few-shot transfer is degraded. **For n=1, the user should default to zero-shot with strong rubric wording, not attempt to mimic Autorubric's few-shot recipe.**

### Per-criterion scores as "optimization signals."

§5 and §6 (pp.7–8) are the paper's most confident claims — per-criterion signals drive skill improvement and RL rewards. For a *benchmark* (what the Syke project is building), these are mildly misleading: the skill-improvement loop works because the task (peer review) has a large generative-revision surface and the rubric is the loss signal. For an n=1 benchmark the analogous use would be "rubric signal drives packet revision / agent training" — a future use case, not a benchmark-construction concern. Do not confuse Autorubric's RL-reward framing with its benchmarking framing.

### Ensemble defaults.

The paper's *reported experiments* use a single judge by default (Table 5 p.22: `judges=1`). The framework supports ensembles but the paper's own ablation (Table 4 p.6) shows `+Ens(k=3, majority)` gives **zero accuracy gain on Gemini** (still 90.0% vs 90.0% single) and only marginally helps weaker models (GPT-5.4-nano: 72.5% → 72.5%; LLaMA: 68.8% → 67.5%). The paper's limitation statement (§Limitations, limitation 4, p.10) is blunt: *"same-model ensembles yield negligible accuracy gains for strong judges, limiting their practical value to variance reduction rather than systematic error correction."* For the Syke 2-judge panel (R5) this means: expect variance reduction, not accuracy gains; do not budget for ensembles to fix a broken rubric.

---

## 6. The atomic-decomposition tension

Zhang 2026 ("A Matched Holistic Rubric Rivals Self-Decomposing Atomic Judges for Benchmark-Style Reference-Support Classification", arxiv 2603.28005) is a controlled counterexample to the atomic-is-better heuristic that Autorubric implicitly embraces. Three facts matter:

**Fact 1: the comparison is scoped narrowly.** Zhang tests *self-decomposing single-prompt atomic judges* (the FActScore pattern: one prompt asks the model to decompose *and* verify) vs prompt-controlled holistic judges with a *similarly detailed rubric* (§3.1 p.3, §3.2 p.3). He explicitly does *not* test externally-supplied decompositions or multi-stage extract-then-verify architectures (§7 "Scope and conditionality" p.8; Limitation 1 p.9). Autorubric is closer to "externally supplied decomposition" — the rubric criteria *are* the decomposition, authored in advance — so Zhang's finding is not a direct refutation of Autorubric. It is a warning about one specific atomic pattern.

**Fact 2: the holistic advantage is localized to incompleteness detection.** On ASQA and QAMPARI (completeness-heavy benchmarks), holistic beats atomic on the `partially_supported` class by +14.5pp to +33.0pp (Table 4 p.6). On TruthfulQA (factuality-heavy, answer-local), atomic has a small edge. Zhang's proposed mechanism (§7 "Mechanism and isolation" p.9) is that self-decomposition *fragments completeness reasoning across claims*, making it harder to detect global omissions; the holistic judge's rubric keeps completeness in scope.

**Fact 3: the Syke task is more completeness-like than factuality-like.** Operative-state reconstruction must integrate across sessions, surfaces, and artifacts. A reconstruction that is locally correct on every cited artifact but omits the live thread is the Syke analog of `partially_supported` on ASQA. The primitives `enumeration_completeness`, `cross_surface_integration`, and `wrong_restart_risk` are explicitly global-coherence primitives. Zhang's finding predicts that *fully atomic* rubric decomposition will under-detect global failures on exactly these primitives.

**How Autorubric's atomic framework should be tempered.**

1. **Keep atomic for local claims** (`time_local_correctness`, `committed_state_fidelity`, `artifact existence`) — these match Zhang's TruthfulQA regime where atomic is competitive.
2. **Use a holistic-style rubric for global primitives** (`cross_surface_integration`, `wrong_restart_risk`, `operative_state_adequacy`) — a single criterion evaluated against the *whole* submission with a detailed behavioral-anchor description. Autorubric supports this: the framework imposes atomic decomposition on *criteria*, not on the submission — a global criterion is still one LLM call that sees the full packet.
3. **Do not self-decompose.** Zhang's specific warning is against one-prompt decompose-and-verify. Since Autorubric's author-time decomposition is a different pattern (the rubric is supplied), this is automatically avoided — but only if rubric authors resist the temptation to add criteria like "for each artifact, check X" that force judge-side decomposition.

Net: Zhang's paper supports keeping Autorubric's per-criterion architecture, but urges 1–2 of the 5–7 R2 primitives be explicitly global-coherence criteria rather than atomic checks. This is a rubric-authoring constraint, not a framework modification.

---

## 7. Concrete implementation path — decisions the user must make

If the user adopts Autorubric for R1 and R2 on the Syke task, Autorubric *leaves open* the following eight decisions:

1. **Packet serialization format.** How is the structured filesystem rendered into Autorubric's `to_grade` string? File-path-prefixed blocks? XML-ish tags? A single long-context JSON dump? Autorubric does not opine; the user must pick and document.
2. **Claim typer architecture.** Autorubric has no claim typer. Is the typer a separate upstream pass (FActScore-style) that emits typed claims, which are then graded by separate rubrics? Or is typing encoded as a nominal per-claim criterion? Autorubric supports the latter but the user must design the schema.
3. **Primitive-to-criterion mapping.** The 9 Syke primitives are not 1:1 with Autorubric `Criterion` objects. Are `bounded_support` and `time_local_correctness` one criterion each (simplest) or decomposed into multiple sub-criteria per primitive (as RiceChem does with 6–8 per question)? Autorubric's experience says more criteria ≠ better — the paper's §8 (p.9) guidance is "prefer binary, narrow scales."
4. **Conditional primitives gating.** Conditional primitives (`enumeration_completeness`, `committed_state_fidelity`, etc.) only apply to some asks. Autorubric's `CANNOT_ASSESS` + `SKIP` strategy is the right scaffold, but the user must decide what *triggers* a CANNOT_ASSESS — and whether it is judge-decided (fragile) or rubric-gated (requires an upstream classifier).
5. **Few-shot policy for n=1.** Zero-shot, or manually-authored synthetic exemplars per criterion? Cross-packet exemplars (Autorubric cold-start: expect -15pp)? Autorubric's verdict-balancing assumes a training split that does not exist.
6. **Citation contract.** Autorubric's default prompt asks for citation but does not enforce format. For Syke the citation must be *packet-location specific* (file path + optional line range). The user must customize the system prompt (override Listing 12).
7. **Ensemble composition and aggregation.** Autorubric's ablation shows same-family ensembles do not help; the paper's cross-family result (Table 4 p.6) is 57.1% accuracy — worse than single judge. For a 2-judge panel the user must pick two families (Gemini + Claude, per R5) and an aggregation rule; Autorubric defaults to majority but majority with n=2 is ill-defined (the user must pick a tie-breaker).
8. **Score aggregation across heterogeneous primitives.** If `verified` claims are binary, `inferred` are ordinal-with-abstention, and `speculative` are flag-or-skip, how is a single submission score computed? Autorubric's Eq. 1 (p.3) weighted-sum assumes a single scale. The user must either pick uniform scaling or report a vector of sub-scores (probably the latter).

---

## 8. What Autorubric does not address

Gaps specific to the Syke task class that Autorubric does not attempt to cover:

- **Packet provenance.** No provenance graph, no file-path awareness, no session-boundary awareness. All three validation benchmarks use flat prompts.
- **Handle-density variation across asks.** Autorubric assumes a fixed rubric across a dataset. RiceChem has per-question rubrics (8, 6, 7, 6 criteria) but they are pre-authored. The Syke question "which primitives apply to this ask?" is a rubric-selection problem Autorubric leaves to the user.
- **Restart safety as a construct.** No construct-validity discussion of continuation-oriented success. The paper's construct-validity section (§B.2, pp.18–19) cites educational measurement (McKeown & Lenarcic Biss 2018, Comer 2009) which is entirely about declarative knowledge assessment, not operative state.
- **Interdependent claim scoring.** Already flagged in §4. The halo-prevention design is a feature for independent criteria and a bug for interdependent ones. No mitigation.
- **Rubric quality validation.** §8 p.9 is explicit: "rubric quality assessment at scale remains the primary open problem." Autorubric will cheerfully score a submission against a factor-collapsed rubric (exactly the Syke project's current pathology) and produce high-confidence numbers. The framework has no diagnostic for the factor-collapse failure mode.
- **n=1 psychometrics.** All reliability metrics in Listing 10 assume multiple items. For one packet × one user the reported κ is not well-defined; Autorubric reports it anyway. The user must layer Feuer 2025-style within-rubric variance diagnostics externally.
- **Judge self-preference and cross-judge leniency offset.** The paper reports these as observations (Gemini-3-Flash is +0.170 more lenient than reference labels, CHARM-100; on ResearcherBench Gemini marks MET 75% of disagreements vs Sonnet — Table 21, p.33) but does not provide a calibration fix. For the Syke 2-judge panel this is an open diagnostic.
- **Continuous/temporal evaluation.** No first-class support for "was this reconstruction useful 5 steps later?" — the whole framework is single-shot grading.

---

## 9. Verdict

**Yellow light — adopt the framework, author the missing layers externally.** Autorubric is the best-in-class general rubric-evaluation library as of April 2026, and for R2 (small-primitive binary rubric with abstention) and the reliability-reporting component of R4 it is a clean adoption. For R1 (claim typing) Autorubric supplies nothing and the user must build the typer layer externally. For the Syke-specific demands — structured-filesystem packet, provenance-anchored citations, interdependent primitives, rubric-quality validation — Autorubric is silent and the user must layer these on top. The specific failure mode the Syke project needs to avoid is treating Autorubric's strong RiceChem/CHARM-100 numbers (80% accuracy, κ=0.642) as evidence that the framework will work at similar quality on operative-state reconstruction; those benchmarks test *local, independent, reference-anchored entailment*, which is a strictly easier task class than the Syke target. The right move is: use Autorubric as the grading substrate; author a small (5–7) binary rubric with 1–2 deliberately holistic global-coherence primitives (per Zhang 2026); require packet-location citations in the prompt override; store per-criterion judgments and compute CyclicJudge variance decomposition on top of `items.jsonl`; treat n=1 few-shot as not-available and default to zero-shot; and do not assume ensemble averaging buys accuracy — only variance reduction (per the paper's own ablation, Table 4 p.6).

---

*References cited by section/figure/table throughout — all from Rao & Callison-Burch 2026 (arxiv 2603.00077) and Zhang 2026 (arxiv 2603.28005). Where the paper does not address a question, this review says so explicitly; no speculation has been substituted.*
