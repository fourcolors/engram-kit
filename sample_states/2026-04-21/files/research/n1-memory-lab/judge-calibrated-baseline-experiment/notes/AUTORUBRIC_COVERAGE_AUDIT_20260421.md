# Autorubric Coverage Audit — Does it Give Us Everything?

*A build-vs-buy inventory for the Syke n=1 memory benchmark, reading Rao & Callison-Burch 2026 (arxiv 2603.00077) line-by-line against our measured pathologies and hard constraints. Integrates Zhang 2026 (arxiv 2603.28005) on atomic-vs-holistic. Extends `AUTORUBRIC_REVIEW_20260421.md`; where that review was conservative I sharpen; where it was optimistic I push back.*

Date: 2026-04-21.

---

## 1. The question, sharp

The user is not asking "can Autorubric score one of our submissions?" That answer is trivially yes — serialize the packet to a string, author some criteria, call `rubric.grade()`, get a number. The actual question is harder:

**Can Autorubric be the measurement instrument for a benchmark whose primary deliverable is instrument-validity itself?**

What we are computing is *not* a leaderboard score. It is:

1. A **variance decomposition** of an LLM-judge measurement of operative-state reconstruction: `X = μ + α + β + γ + ε` across four identified noise sources (probe, agent, judge-identity, judge-flicker) — per `MATH_ONE_PAGER §2`.
2. A **schematic adherence** diagnostic: does the rubric predict the overall verdict, and does any single axis eat the signal? (R² = 0.862 all-12 vs 0.851 top-3 on Opus; `state_transition_tracking` alone = 0.731.)
3. A **judge-identity bias** report: +0.500 mean delta Opus-over-GPT in the clean arm, 22/54 cells strictly Opus-higher vs 0/54 reverse (per the user's constraints block).
4. A **binary-collapse** calibration: showing the useful-vs-fail collapse recovers κ = 0.86–0.91 while the 3-level κ stays at 0.24–0.34.
5. A **construct-validity confound** flag for retrieval-degenerate probes (R13/R11/R04) — `EVIDENCE_PACKET_LENS §4`.
6. Ultimately: a **reusable instrument** for partially verifiable operative-state reconstruction under hard constraints (LLM-only, agent judge, same rubric across probes).

Autorubric is a general rubric-scoring framework that produces a scalar score and a psychometric report per submission. The question is how much of *that list* it delivers versus how much is bespoke math we must still write.

---

## 2. Needs inventory

Needs are labeled N1–N17. Provenance in parentheses cites our docs or the measurement record.

- **N1. Per-criterion atomic scoring with weights.** (`AUTORUBRIC_REVIEW §3 R2`; `FIELD_MAP §7 R2`.)
- **N2. Holistic scoring for whole-answer constructs.** (`FIELD_MAP §4 X1`; Zhang 2026.)
- **N3. Abstention verdict (`CANNOT_ASSESS`).** (`FIELD_MAP §7 R1`; hard constraint — some packet claims are outside verifiable envelope.)
- **N4. Aggregation equation (score from criteria + weights).** (Autorubric Eq. 1 / §2; our Eq. 1 equivalent is `benchmark_scorer.py` weighted mean.)
- **N5. Negative-weight penalty criteria** for anti-patterns (fabrication, wrong-restart risk). (`JUDGE_DESIGN_LITERATURE_MAP §4` primitive `wrong_restart_risk`.)
- **N6. Per-criterion reliability metric (κ per criterion).** (`MATH_ONE_PAGER §3`; our measured 3-level κ = 0.24/0.34.)
- **N7. Schematic adherence (rubric → verdict R²).** (`MATH_ONE_PAGER §4`; our measured 0.754/0.862.)
- **N8. Factor collapse detection (cross-axis correlation / dominant-axis ablation).** (`MATH_ONE_PAGER §4`; our 0.862 → 0.851 top-3 finding.)
- **N9. Variance decomposition over four sources (σ_α probe, σ_β agent, σ_γ judge-identity, σ_ε judge-flicker).** (`MATH_ONE_PAGER §2`; CyclicJudge lineage.)
- **N10. Small-n psychometrics.** 57 cells × 4 judge reps, not 1240 responses. (User constraints block; `MATH_ONE_PAGER §6`.)
- **N11. Structured-packet-as-context.** Filesystem + provenance + slice_summary, not `(prompt, submission)`. (`EVIDENCE_PACKET_LENS §1`.)
- **N12. Multi-step judge-agent integration** (judge makes tool calls against the slice). (User constraints; `EVIDENCE_PACKET_LENS §3.2`.)
- **N13. Cross-criterion consistency / non-independence.** Primitives are not independent — e.g., object-continuity failure breaks time-local-correctness. (`AUTORUBRIC_REVIEW §4`.)
- **N14. Judge-identity bias measurement** (σ_γ estimation across panel members). (`MATH_ONE_PAGER §2`; +0.57 opus-over-gpt, 22/54 strict.)
- **N15. Judge-flicker measurement** (σ_ε intra-rater under rejudge). (`MATH_ONE_PAGER §2`; our σ_ε^cell = 0.187 / σ_ε^pooled = 0.329.)
- **N16. Rubric-quality validation** — is the rubric itself measuring the intended construct? (`FIELD_MAP §4 C1`; Feuer 2025 schematic-adherence.)
- **N17. Same-rubric-across-probes with per-probe applicability gating.** Hard constraint: no per-probe primitive customization, but some primitives don't apply to some asks. (User constraints; retired per-probe `expected_primitives` per `EVIDENCE_PACKET_LENS` header.)

---

## 3. Coverage matrix

Coverage tags: **GREEN** = Autorubric provides it, works for us. **YELLOW** = partial; the shape is right, magnitudes or assumptions don't fit. **RED** = Autorubric does not cover this; we must author.

| Need | Autorubric coverage | What Autorubric provides (if partial/full) | What's missing |
|---|---|---|---|
| **N1** Per-criterion atomic scoring with weights | **GREEN** | §2 "Criterion types" p.2; Listings 1–3 p.15; binary/ordinal/nominal `Criterion` with `weight`. | Nothing — this is the core drop-in. |
| **N2** Holistic scoring for whole-answer constructs | **YELLOW** | Framework does *not* forbid it: a single criterion seeing the whole submission is an allowed `Criterion`. But Autorubric is explicit that it "adopts analytic rubrics as the default" (§2 p.2) and §8 (p.9) says "holistic scores cannot drive targeted improvement because they collapse the criterion-level signal" — i.e., holistic is deprecated in the framework's voice. Figure 5 (p.14) shows "Holistic" as grayed-out / "not yet implemented". | First-class holistic API; any guidance on composing atomic + holistic into one score (hybrid aggregation). Atomic is the defended default; holistic is tolerated. |
| **N3** Abstention verdict (`CANNOT_ASSESS`) | **GREEN** | §3 "Uncertainty" p.4; Listing 8 p.18; four strategies (`SKIP`, `ZERO`, `PARTIAL`, `FAIL`); Default `SKIP` (Table 5 p.22). System prompt (Listing 12 p.21) explicitly tells judge "Use only when you genuinely cannot determine…" | Nothing for the primitive itself. The trigger policy — *what* should cause CANNOT_ASSESS — is still ours to decide. |
| **N4** Aggregation equation | **GREEN** | Eq. 1 p.3: `score = max(0, min(1, Σᵢ vᵢ·wᵢ / Σ_{wᵢ>0} wᵢ))`. Clamps to [0,1]; excludes negative weights from denominator so perfect-response scores 1.0. Verified against hand-computed examples (Appendix B.6 p.22; 400+ tests). | Nothing for the standard case. Hybrid atomic+holistic composition is not in Eq. 1; that's ours. |
| **N5** Negative-weight penalty criteria | **GREEN** | §2 "Weighting" p.3: "Negative criteria serve as penalties for anti-patterns, counteracting the leniency bias documented in LLM judges." Listing 3 p.15 shows `weight: -15.0` for hallucinated citations. The Industrial-Revolution sample report (Listing 14 p.24) shows a -15.0 "Errors" criterion scored and passing. | Nothing. |
| **N6** Per-criterion reliability (κ per criterion) | **GREEN** | Listing 10 p.19 computes κ, quadratic-weighted κ, Spearman, Kendall, Pearson, RMSE, bootstrap CIs. Table 12 p.28 reports per-criterion κ on RiceChem (27 criteria, individual κ from -0.385 to 0.932). Table 21 p.33 reports per-weight-band κ on ResearcherBench. | Nothing — substrate is strictly more than we currently report. Small-n validity (N10) is where this becomes suspect. |
| **N7** Schematic adherence (R²) | **RED** | Autorubric does not compute rubric→verdict R². The closest thing is the **weight-inference R²** in Appendix D.4 (Eq. 2 p.26, Table 13 p.28: 0.542–0.994) which fits weights *from* student-score data — a different quantity than what we compute. The framework's overall-score is a deterministic weighted sum (Eq. 1), so "R² of rubric predicting score" = 1.0 by construction. Nothing analogous to our "does the 12-subcategory rubric predict the overall_verdict field" R². | Schematic-adherence regression: fit `overall_verdict ~ subcategories`, report R² and adjusted R², report drop when the dominant axis is removed. This is ours to write. §8 p.9 is explicit: "Rubric quality assessment at scale remains the primary open problem." |
| **N8** Factor collapse detection | **RED** | The paper reports inter-criterion disagreement structure (Table 22 p.34: disagreement rate by rubric construct type, 14–37%) and notes in §4.3 (p.5) that "disagreements concentrate in subjective constructs (27.9%) rather than factual ones (14–15%)". But it does **not** compute cross-criterion Spearman/Pearson to detect dimensionality collapse, nor dominant-axis ablation, nor any analog of the Feuer 2025 "factor-wise rank-correlation > 0.93 = collapse" signal. | Cross-axis correlation matrix; rank-correlation threshold test; dominant-axis ablation (re-fit on remaining axes; report R² delta). These are ours. |
| **N9** Variance decomposition (α/β/γ/ε) | **RED** | Autorubric stores per-item, per-criterion, per-judge verdicts in `items.jsonl` (§B.3 p.19) — the raw data is shaped correctly to fit a components model on top. But the paper itself does *no* variance decomposition: it reports mean-bias (§4.3 p.5, +0.170 on CHARM-100; §E.9 p.34, +0.133 Gemini-over-Sonnet on ResearcherBench), not variance components. No σ² estimates, no G-coefficient, no ANOVA with judge-identity term. | Everything. The CyclicJudge-style ANOVA / generalizability G-study is entirely our math. |
| **N10** Small-n psychometrics | **RED** | The three reported benchmarks are 1240 / 5586 / 600 judgments. κ bootstrap CIs use N=10,000 resamples (Table 11 p.28). Autorubric's reliability stack **assumes** enough data for the limit theorems to apply. For 57 cells × 4 reps, pooled κ stops being a calibrated estimate. The framework will cheerfully compute it anyway (this is a known failure mode; §Limitations #4 p.10 flags ensemble-gain being below noise for strong judges — a small-n signature, but the paper doesn't generalize). | Small-n specific adjustments: exact-permutation CIs for κ at N≈50, Fisher-transform CIs for σ_γ shifts, explicit power-analysis for detecting architecture effects given measured noise floor. |
| **N11** Structured-packet-as-context | **RED** | Listing 4 p.16: `rubric.grade(to_grade=response, query=prompt)`. Both are strings. RiceChem = chem question + ~120 word essay; ResearcherBench = research question + long-form answer; CHARM-100 = single-turn chatbot. None is a structured filesystem with provenance. **The framework has no first-class concept of packet structure.** Adaptation path: serialize our packet into a string with explicit markers. | Packet serialization schema; provenance-preserving tags; per-claim citation grammar; tool-surface for judge-agent to re-read the slice. |
| **N12** Multi-step judge-agent integration | **RED** | Autorubric issues N × M *concurrent, independent* LLM calls (Fig. 1 p.2). Each call is single-pass; no tool loop, no agent framework, no MCP, no filesystem access from inside the grader. The `ThinkingConfig(level="HIGH")` in Listing 6 p.17 enables extended thinking *tokens*, not tool use. Judge-as-tool-using-agent is entirely outside the framework's architecture. | The whole agentic-judge harness. Autorubric assumes the judge is a sealed `LLMConfig` call. We need Agent-as-a-Judge (Zhuge 2024) as a wrapper around each criterion evaluation. |
| **N13** Cross-criterion consistency / interdependence | **RED** | §2 p.3 explicitly designs *against* this: "Each criterion is evaluated in a separate LLM call to prevent halo effects (Lee et al. 2025; Wei et al. 2025)." The halo-prevention is architectural — it *cannot* see a failure in criterion X while judging criterion Y. So for our interdependent primitives (object-continuity → time-local-correctness cascade), the framework will report the cascade as two independent failures or, worse, will mark the downstream criterion "MET" because it accepted the broken upstream assumption in isolation. | A cross-criterion coherence check stage (post-hoc second pass) or a gated-criterion mechanism (criterion Y is only evaluated if criterion X was MET). Neither is in Autorubric. |
| **N14** Judge-identity bias measurement | **YELLOW** | The paper *reports* judge-identity bias as observations: §4.3 p.6 "positive bias (+0.170)"; §E.9 p.34 "calibration differences, +0.133 Gemini-Flash over Sonnet"; §E.7 Table 21 p.33 per-weight-band κ between Sonnet-4.5 and Gemini-3-Flash; 452 of 600 disagreements are Gemini-MET + Sonnet-UNMET (75% asymmetric — a *direct* analog of our +0.57 Opus-over-GPT). The cross-family ensemble ablation (Table 4 p.6: 57.1% accuracy, the *worst* row) is implicit evidence that judge-identity bias is load-bearing. But the paper does not estimate σ_γ as a variance component. | σ_γ as a variance component (not a shift); Fisher-CI on the shift; explicit judge-identity diagnostic report (who agrees with whom on what kinds of criteria). The weight-band table (Table 21) is the closest existing substrate; we extend from there. |
| **N15** Judge-flicker measurement | **YELLOW** | The framework supports `mean_agreement` as a reliability indicator (§2 p.3) and the `items.jsonl` shape lets us rerun. §Limitations #4 p.10 explicitly says same-model ensembles reduce variance (good for us — this is σ_ε). But the paper reports no σ_ε estimate for intra-rater repeats; the three benchmarks are single-run. The `master seed` infrastructure (§B.3 p.19) is for reproducibility, not for intra-rater flicker study. | An intra-rater rerun protocol (which Autorubric *supports* but does not *recipe*); the cell-wise vs pooled σ_ε distinction we already measured; adjacent-band-flip taxonomy. |
| **N16** Rubric-quality validation | **RED** | §8 p.9 is the cleanest admission in the paper: "While Autorubric covers a lot of ground in offering researchers an ergonomically valid framework for their rubric-based evaluation workflows, situated in best practices, **rubric quality assessment at scale remains the primary open problem**: consistency is necessary but not sufficient, as judges can agree on scores from a poorly written rubric. Open directions include automated rubric quality measurement…" The authors explicitly disclaim this. | Everything. Rubric-quality checks (factor-collapse, construct-validity, criterion-referenceability audit) are precisely where our benchmark's scientific contribution lives — and Autorubric punts on them. |
| **N17** Same-rubric-across-probes w/ applicability gating | **YELLOW** | One-dataset-one-rubric is the standard API pattern (RiceChem has four *different* rubrics for its four questions; ResearcherBench has a per-question rubric). A single fixed rubric across probes is fine — the framework allows it. Applicability gating maps naturally onto `CANNOT_ASSESS` + `SKIP`: when the primitive doesn't apply, the judge abstains and the denominator adjusts. | Explicit contract for *what triggers* CANNOT_ASSESS in the applicability sense (not the uncertainty sense). Autorubric conflates "judge can't tell" with "criterion doesn't apply"; we need to disambiguate. |

### Summary count (17 needs)

- **GREEN (full)**: N1, N3, N4, N5, N6 — **5**
- **YELLOW (partial)**: N2, N14, N15, N17 — **4**
- **RED (missing)**: N7, N8, N9, N10, N11, N12, N13, N16 — **8**

Of the 17 needs, Autorubric fully covers 5, partially covers 4, and misses 8. Crucially, the **RED cluster is exactly the benchmark's scientific contribution**: schematic adherence, factor collapse, variance decomposition, small-n psychometrics, structured-packet handling, agent judging, cross-criterion coherence, and rubric-quality validation. The GREEN cluster is the *scoring plumbing*: weighted criteria, abstention, penalty criteria, aggregation equation, per-criterion κ. Autorubric gives us the plumbing; it does not give us the physics.

---

## 4. What Autorubric does well, concretely

**A. The criterion data model is a near-perfect fit for the R2 primitive set.** `Criterion(weight, requirement, scale_type ∈ {binary, ordinal, nominal})` with positive or negative weight (Listings 1–3, p.15) is exactly the object we would have designed. The binary default with a 1–2 sentence explanation field and evidence citation (Listing 12 p.21: "Cite specific text from the submission as evidence for your verdict") is the R3 citation contract with zero adaptation needed.

**B. `CANNOT_ASSESS` is architecturally first-class, not bolted on.** The system prompt (Listing 12 p.21) hard-codes abstention into the judge's output schema — `{"criterion_status": "MET|UNMET|CANNOT_ASSESS", "explanation": "..."}` — and the aggregation equation (Eq. 1, p.3) has the denominator adjustment baked in for `SKIP`. This is the single most faithful implementation of Trust-or-Escalate's abstention primitive (Jung 2024) we have seen.

**C. Score aggregation is mathematically unambiguous.** Eq. 1 p.3: clamping to [0,1], excluding negative weights from the denominator. Correctness-verified against hand-computed examples (§B.6, p.22) with a 400+ test suite in the repo. Relative to our `benchmark_scorer.py` weighted-mean aggregation, Eq. 1 is *tighter*: ours doesn't handle negative weights cleanly.

**D. Weight-band stratification is a perfect substrate for the universal-vs-conditional primitive split.** §E.7 p.33 reports per-weight-band κ on ResearcherBench: W=1 (nice-to-have) κ=0.477, W=2 (supporting) κ=0.566, W=3 (core) κ=0.532. Figure 10 p.34 shows this per-system. If we map our "universal primitives" to W=3 and "conditional primitives" to W=1–2, the framework already emits the exact diagnostic we want.

**E. The default prompt is fewer-trained-priors than any custom prompt we would write.** Listing 12 p.21 includes `EVALUATION RULES`, `IMPLICIT SATISFACTION`, and `RESPONSE FORMAT` sections tuned across three benchmarks. Inheriting it and *overriding only the citation clause* (to require packet-path citations) is strictly safer than rolling our own.

**F. The response-caching + checkpointing + master-seed machinery (§B.3 p.19, Listing 11 p.20) is exactly what we need for rejudge experiments.** Rerunning the same seed gives bit-identical non-LLM randomness; only the LLM stochasticity (`σ_ε`) varies. This is the correct tooling for σ_ε isolation.

**G. The ResearcherBench cross-judge analysis (§E.5–E.9 pp.32–34) is a blueprint for our judge-identity work.** The paper explicitly reports: 57% top-ranking agreement across judges; Spearman 0.54–0.82 on per-question scores; 75% asymmetric disagreement (Gemini-MET when Sonnet-UNMET). This is *structurally identical* to our 22/54 cells Opus-strictly-higher, 0/54 reverse — and Autorubric demonstrates the diagnostic pipeline that gets from raw verdicts to that report. We can copy the analysis pattern; the scoring substrate supports it.

---

## 5. Where Autorubric's assumptions break for us

**1. Atomic-only default and the Zhang tension (N2).** §2 p.2 "adopts analytic rubrics as the default" and §8 p.9 "holistic scores cannot drive targeted improvement because they collapse the criterion-level signal" — these are normative claims. The paper's architectural choice to run each criterion in a *separate* LLM call (§2 p.3) makes holistic criteria technically possible (just run one criterion that sees the whole submission) but forfeits the halo-prevention justification. Zhang 2026 on completeness-sensitive tasks shows holistic matches or beats atomic on 2/3 QA benchmarks (Table 1 p.4 of Zhang: ASQA +15.5pp, QAMPARI +7pp for holistic). Our task is completeness-sensitive (reconstruction-for-continuation must integrate across sessions — Zhang's `partially_supported` failure mode is our `wrong_restart_risk`). See §6 for the resolution.

**2. Gold-reference assumption (N10, N16).** Every Autorubric reliability metric (§B.2 p.18) is computed **against a reference annotation**. RiceChem has 819 TA-assigned scores; ResearcherBench has 5586 expert-curated criterion labels; CHARM-100 has 100 × 6 = 600 ground-truth labels with 92% mean normalized entropy (§F.6 p.39). Footnote 6 p.6: *"All κ values in this paper are computed between the LLM judge's predictions and the reference annotation."* **We do not have such a reference**, and generating one at n=1 packet scale is the whole problem we're trying to avoid. Autorubric's reliability framing collapses to "judge vs reference"; ours is "judge vs judge (σ_γ)" and "judge vs itself (σ_ε)", which the framework *can* compute (the `mean_agreement` indicator) but neither reports nor defends as a primary metric.

**3. Flat `(prompt, submission)` input (N11).** Listing 4 p.16 sets the API. There is no first-class type for filesystem context, provenance, slice summaries, or session boundaries. RiceChem packets are ~120 words; ResearcherBench packets can be longer-form but are still text. Our packet is a filesystem with `packet.json`, `slice/`, `local_git_anchor.json`, `slice_summary`, `replay_state` — all of which `EVIDENCE_PACKET_LENS §1` enumerates as the judge's actual input surface. Serializing this into a string with XML-like tags is *possible* but gives us zero framework support for maintaining provenance pointers from judge citations back to packet locations.

**4. Independent criteria (N13).** This is the deepest architectural break. The halo-prevention design (§2 p.3) is the same mechanism that forbids cross-criterion reasoning. Our primitives (per `JUDGE_DESIGN_LITERATURE_MAP §4`) are **not** independent: object-continuity failure propagates into time-local-correctness; wrong-thread selection propagates into cross-surface integration. Autorubric will under-detect cascading failures or double-count them inconsistently. No built-in fix exists.

**5. No session / packet provenance (N11, N16).** Rubric-quality validation in our regime requires checking that criterion wording references packet locations (file paths, session ids) in a way that a re-running judge could verify. Autorubric's `requirement` field is free-text natural language; there is no schema for structured evidence pointers. Related: the paper's §8 admission on rubric-quality-at-scale being unsolved maps onto our factor-collapse finding directly — Autorubric would have scored our current 12-subcategory rubric without flagging the collapse.

**6. Single-pass judges (N12).** The whole agent-judge branch of the 2024 literature (Zhuge 2024 Agent-as-a-Judge; parts of DeepSeek-GRM 2025) is absent from Autorubric. `ThinkingConfig` extends compute-per-call but does not add tool use. Our judge is a multi-step agent with bash/grep/sqlite access to `slice/` and `local_git_anchor.json` — that mode is outside Autorubric's architecture.

**7. Implicit many-item assumption (N10).** The three validation benchmarks (1240, 931, 600 judgments) are large enough for bootstrap CIs, McNemar tests (RiceChem p=0.023 on 819 paired observations, §4.1 p.5), and paired permutation tests (9999 perms, §E.6 p.33). Our 57 cells × 4 reps is at least an order of magnitude smaller. The framework will compute these statistics anyway; their interpretability is our problem.

---

## 6. The Zhang tension, reconciled

Zhang 2026 attacks "self-decomposing single-prompt atomic judges" (§3.1 p.3 of Zhang) — a specific architectural pattern where one LLM call is asked to *both* decompose the candidate into atomic claims *and* verify each against the reference. Autorubric does not do this. Autorubric's decomposition is **author-time**: the rubric criteria *are* the decomposition, supplied in the `Rubric` object, and each criterion is evaluated in its own dedicated call. This is in the "externally supplied decomposition" class that Zhang explicitly marks as *untested* (Zhang §7 "Scope and conditionality" p.8: "atomic pipelines with externally supplied decompositions or multi-stage extract-then-verify architectures remain untested and may behave differently").

**So Zhang is not a refutation of Autorubric.** It is a warning about a pattern Autorubric does not use. But Zhang's *mechanism* (§7 "Mechanism and isolation" p.9: "self-decomposition may fragment completeness reasoning across claims, making it harder to detect global omissions; the holistic rubric's explicit completeness dimension may better direct attention to missing information") transfers to *any* atomic architecture, including Autorubric's author-time one — if the rubric's criteria are all local, the completeness dimension has nowhere to live.

**Does Autorubric forbid holistic criteria?** No. It deprecates them in voice and default (§2 p.2, §8 p.9; Fig. 5 p.14 shows "Holistic" grayed as "not yet implemented" though the API doesn't actually block it). A single criterion with a rich `requirement` string scored against the *whole* submission is a legal `Criterion` object. The halo-prevention argument is structurally undermined for such a criterion (it *is* the halo), but the framework does not block it.

**Resolution for our task.** Keep Autorubric's per-criterion architecture for the *local* primitives (`time_local_correctness`, `bounded_support`, artifact existence — the Zhang-TruthfulQA regime where atomic is competitive). **Add** one or two deliberately holistic criteria for the *global* primitives (`operative_state_adequacy`, `wrong_restart_risk`, `cross_surface_integration` — the Zhang-ASQA/QAMPARI regime where holistic wins). This is 5–7 atomic + 1–2 holistic — a hybrid that neither framework endorses cleanly but neither forbids. **The hybrid aggregation equation (how to compose atomic and holistic scores into one number) is ours to write**; see §9 below. This is a rubric-authoring move that uses Autorubric as substrate and does not violate its API.

---

## 7. Build vs buy — four options, tradeoffs

### Option A: Adopt Autorubric wholesale

- **Cost:** Low. Pip-installable (authors say MIT + `autorubric.org`, §8 p.9). Author 5–7 `Criterion` objects, serialize packets to strings, call `rubric.grade()`, ingest `items.jsonl`, use the built-in report (Listing 14 p.24 shows the output shape).
- **Speed:** Fast. Could produce first results in days.
- **What we lose:** All 8 RED needs (N7–N13 + N16). Specifically: no schematic-adherence R² regression; no factor-collapse detection; no variance decomposition; no small-n psychometric adjustments; no packet-structuring; no agent judge; no cross-criterion coherence; no rubric-quality validation. We'd ship Autorubric's reliability report as our benchmark result — and the report would obscure exactly the pathologies (dimensionality collapse, large σ_γ) that our benchmark is supposed to diagnose.
- **Signature we could claim:** "N=1 memory benchmark scored with Autorubric." Provides nothing new. This is a *consumer* of the framework, not a scientific contribution.

### Option B: Adopt apparatus (Eq 1, per-criterion κ, abstention) but wrap in our own pipeline

- **Cost:** Moderate. Import Autorubric as a dependency; use `Rubric`, `Criterion`, `CriterionGrader`, `CannotAssessConfig`, and the per-criterion metric functions. Wrap in our own packet-serializer, agent-judge harness, schematic-adherence regression, variance-decomposition layer, and rubric-quality checks.
- **Speed:** Medium. Weeks, not days.
- **What we lose:** Some flexibility (e.g., non-string submissions would require hacking around the API). Some of Autorubric's infrastructure (checkpointing, caching) assumes `rubric.grade` is the top-level call; if we wrap, we re-author some of that.
- **What we keep:** Strong scoring substrate, proven abstention, verified Eq. 1, free per-criterion κ, the report template. Our math layers *on top*.
- **Signature we could claim:** "An instrument-validity benchmark for partially verifiable operative-state reconstruction, built on Autorubric's scoring substrate, with bespoke small-n variance decomposition and factor-collapse diagnostics." — this is publishable, cites Autorubric honestly, claims the specific diagnostics as the contribution.

### Option C: Steal the math, reimplement in our idiom, add what we need

- **Cost:** Medium-high. Write our own `Rubric`/`Criterion`/`Eq.1` from scratch (they are not algorithmically hard; 400 LOC at most). Add everything we need natively: packet structure, agent judge loop, variance decomposition, schematic adherence, rubric-quality checks.
- **Speed:** Slow initially (2–3 weeks to match Autorubric feature parity on the GREEN needs) but fast afterwards because every extension is in our idiom.
- **What we lose:** 400+ tests, the `cookbook` of 20 recipes, the community credibility of "we use Autorubric", the free per-provider rate limiting and cost tracking.
- **What we gain:** Full freedom on packet schema, judge architecture, and hybrid atomic+holistic aggregation. No need to hack around string-based APIs.
- **Signature we could claim:** "A first-principles measurement instrument for n=1 partially verifiable memory reconstruction, validated against Autorubric on shared equations (Eq. 1, per-criterion κ)." Academically respectable. Risks: "why didn't you just use Autorubric?" question from reviewers.

### Option D: Write our own framework from scratch, citing Autorubric as precedent

- **Cost:** High. Everything Option C has, plus original contributions we'd have to justify (e.g., a new aggregation rule, a new abstention semantics).
- **Speed:** Slow.
- **What we lose:** Everything. Option C is the strictly-better version of D unless we have a scoring innovation that Autorubric prevents.
- **Signature we could claim:** "A new framework." We do not have a framework-level scoring innovation. We have *math layers missing from an existing framework*. Option D would be overclaiming.

---

## 8. Honest recommendation

**Option B. Adopt Autorubric's apparatus — `Rubric`, `Criterion`, Eq. 1, `CannotAssessConfig`, per-criterion κ reporting, the default system prompt with a citation-format override — as the scoring substrate, and author our own layer on top for the eight RED needs.** This is the only option that *stops* us from re-deriving Eq. 1 and 400 tests we don't need to own, while *forcing* us to write the math that is our actual scientific contribution: schematic adherence, factor-collapse detection, small-n variance decomposition, structured-packet handling, agent-judge integration, cross-criterion coherence, and rubric-quality validation. Option A abandons the science; Option C reinvents `Criterion`; Option D pretends we have a framework contribution we don't. Option B names what is borrowed (plumbing), names what is ours (diagnostics), and lands honestly: the contribution is *what we measure*, not *how we sum weighted verdicts*. The 4 YELLOW needs (N2 holistic, N14 σ_γ, N15 σ_ε, N17 applicability-vs-uncertainty) are best addressed as thin extensions to the Autorubric substrate rather than reimplementations, and each has a clean path (hybrid atomic-plus-holistic rubric per Zhang; Fisher-transformed σ_γ on top of Autorubric's raw `items.jsonl`; intra-rater rerun protocol using the master-seed infrastructure; a second abstention flag `NOT_APPLICABLE` distinct from `CANNOT_ASSESS`).

---

## 9. Bespoke equations we'd need even if we adopt Autorubric

These are the equations Autorubric does not supply. They are our math even under Option B.

**Eq. S1 — Schematic-adherence R².** Given per-submission rubric vectors `c ∈ ℝᴷ` (K = 12 currently, or 5–7 under R2) and overall verdict `y ∈ {0, 0.5, 1}` (fail / partial / pass), fit `y = β·c + e` and report `R²` and `adjusted R²`. Extend: refit on `c \ {k*}` where `k*` is the dominant axis (identified by per-axis R²); report ΔR². This is our `schematic_adherence_ablation_20260420.py` formalized.

**Eq. S2 — Factor-collapse threshold.** Compute Spearman ρ over all pairs of criterion columns in `items.jsonl`. If max off-diagonal ρ > 0.85 on `N ≥ 3` axis pairs, flag collapse (Feuer 2025 threshold; we use 0.85, Feuer uses 0.93 — our threshold is *stricter*, defensible for small K). Companion: dominant-axis ablation from Eq. S1.

**Eq. S3 — Four-source variance decomposition.** Random-effects ANOVA over `verdict_{probe, agent, judge, rep}`:
`X = μ + α_{probe} + β_{agent|probe} + γ_{judge} + ε_{rep}`, estimate `σ²_α, σ²_β, σ²_γ, σ²_ε` via REML; compute generalizability coefficient `G = σ²_true / (σ²_true + σ²_error)`. CyclicJudge provides the algebra; Autorubric provides the raw data.

**Eq. S4 — Fisher-transformed σ_γ CI.** For N=57 cells × 2 judges, the raw between-judge correlation has a skewed sampling distribution. Compute `z = atanh(r)`, CI on z, back-transform. This gives a calibrated small-n CI on σ_γ that Autorubric's 10,000-resample bootstrap does not.

**Eq. S5 — Packet-provenance-aware claim extraction.** Pre-judge extractor that splits the answer text into `{verified | inferred | speculative}` claim lists with packet-location pointers. Inspired by FActScore (Min 2023) but with file-path-aware citation grammar. Not a single equation — a pipeline — but the grammar itself is ours to define.

**Eq. S6 — Hybrid atomic-plus-holistic aggregation.** Eq. 1 handles one scale. For the hybrid we need:
`score = w_atomic · Σ(vᵢ · wᵢ) / Σwᵢ  + (1 - w_atomic) · v_holistic`
with `w_atomic ∈ [0, 1]` as a design choice. Defensible starting point: `w_atomic = 0.7` (Zhang's atomic advantage on local-fact benchmarks is on the order of 1–2% while holistic advantage on completeness is 15–30%; weighting 70/30 underweights the holistic dimension relative to its empirical size but preserves the atomic diagnostic signal). This is our call.

**Eq. S7 — Dual-abstention semantics.** Two separate abstention flags:
`NOT_APPLICABLE` (criterion doesn't apply to this probe) → denominator adjustment only, no contribution to reliability stats.
`CANNOT_ASSESS` (judge genuinely can't tell) → contribution to reliability stats as missing data; raises a data-quality flag if the rate > 20% for a criterion.
Autorubric conflates these under `CannotAssessStrategy.SKIP`.

**Eq. S8 — Judge-identity shift diagnostic.** Per-criterion mean shift `Δ_k = mean_{cells}(v^{opus}_k - v^{gpt}_k)` with sign-test, Bonferroni over K criteria, reported alongside per-criterion κ. This is the direct analog of Autorubric's Table 21 weight-band analysis, but stratified by *criterion* and reported as a signed shift rather than a scalar κ.

**Eq. S9 — Intra-rater adjacent-band structure.** For cell `(probe, agent, judge, rep)` with 3-level ordinal scores, report: adjacent-flip rate (between-band moves ≤ 1), critical-flip rate (pass↔fail, across the useful-fail boundary), and structure ratio (adjacent / critical). Our current measurement: flip rate 42.2%, zero pass↔fail flips, all flips adjacent. Autorubric reports exact κ and quadratic-weighted κ but not this structure.

These nine are the actual bespoke math. They are what the benchmark contributes.

---

## 10. What Autorubric the tool actually gives us if we run it today

Reading the paper directly (autorubric.org is mentioned §8 p.9 and footnote 1 p.1 says "URL withheld for blind review" — so the repo is promised, and footnote 11 acknowledges the LLM Data Company's open-source `rubric` project at `github.com/The-LLM-Data-Company/rubric` as the data-model starting point).

**What the paper promises ship:**

- Open-source Python library, MIT licensed (§8 p.9).
- `Rubric`, `Criterion`, `RubricDataset`, `CriterionGrader`, `LLMConfig`, `JudgeSpec`, `FewShotConfig`, `CannotAssessConfig`, `EvalRunner`, `EvalConfig`, `ThinkingConfig` — these are the importable objects (Listings 1–11, pp.15–20).
- `evaluate()` function that takes dataset + grader and returns `result.compute_metrics()` with κ, mean_kappa, Spearman, Kendall, Pearson, RMSE, MAE, bootstrap CIs, mean-bias analysis, per-judge breakdown, per-criterion breakdown (Listing 10 p.19).
- Default system prompts for binary and multi-choice criteria (Listings 12–13 p.21).
- Response caching keyed on (model, prompt, generation params) (§B.3 p.19).
- Checkpoint-based resumable evaluation (§B.3 p.19).
- Per-provider rate limiting via semaphores (§B.3 p.19).
- Per-call / per-criterion / per-item / per-run cost tracking via LiteLLM's `completion_cost()` (§B.3 p.19).
- Latency tracking via `time.perf_counter()` (§B.3 p.19).
- `items.jsonl` per-item output; `manifest.json` per-run output (§B.3 p.19).
- 400+ unit tests (§B.6 p.22).
- Three validation datasets bundled: RiceChem (converted), ResearcherBench (imported), CHARM-100 (authors' own, ~100 samples, mixed criterion types, §F, pp.36–40).
- A "cookbook" with 20 recipes (§8 p.9).

**What the paper does NOT claim to ship (important for our decision):**

- No standalone reporting harness (beyond Listing 14's text summary).
- No rubric-quality validator — the paper explicitly punts (§8 p.9).
- No packet-schema / structured-context handler.
- No agent-judge / tool-using judge.
- No variance-decomposition analysis.
- No schematic-adherence regression.
- No hybrid atomic+holistic aggregation.
- No provenance-preserving citation grammar.
- No small-n statistical adjustments.
- Prompts and dataset docs are English-only (§Limitations #7 p.10).

**The practical distillation:** Autorubric is a well-engineered **scoring and reliability-reporting library** with validated defaults and three reference benchmarks. It is not an analysis framework, not a measurement-instrument-validation framework, and not a rubric-design framework. For our task, we treat it as a scoring primitive — import, wrap, layer — and write the rest.

---

## References

- Rao & Callison-Burch 2026. Autorubric: Unifying Rubric-based LLM Evaluation. arxiv 2603.00077. Specific citations: §§1–8 main text; Eq. 1 p.3; Table 1 p.3; Table 2 p.4; Table 3 p.5; Fig. 2 p.6; Table 4 p.6; Fig. 3 p.7; Fig. 4 p.8; §Limitations pp.9–10; Appendices B (pp.14–22), C (pp.23–24), D (pp.25–30), E (pp.31–35), F (pp.36–40).
- Zhang 2026. A Matched Holistic Rubric Rivals Self-Decomposing Atomic Judges. arxiv 2603.28005. §§1–8 pp.1–9; Table 1 p.4; Table 4 p.6; §7 "Scope and conditionality" p.8.
- `MATH_ONE_PAGER_20260421.md` (variance decomposition, measured numbers).
- `EVIDENCE_PACKET_LENS_20260421.md` (judge input surface, packet structure).
- `AUTORUBRIC_REVIEW_20260421.md` (prior review; extended here).
- `FIELD_MAP_202604.md` §§3, 4, 7 (convergences, contradictions, recommendations).
- `JUDGE_DESIGN_LITERATURE_MAP_20260420.md` §4 (primitive set, now retired — referenced historically).

*Every claim about Autorubric's coverage is grounded in a specific listing, figure, table, or section. Where the paper is silent, this audit says "does not specify." No features have been inferred into existence.*
