# The Math, In Plain Words — 2026-04-21 (revised)

> **2026-04-21 update:** the 9-primitive set from `JUDGE_DESIGN_LITERATURE_MAP §4`
> referenced in this doc has been **retired** by the author. Rubric design will start
> from scratch, driven by observed failures + rubric-validity tests. Passages below
> that cite "the project's own primitive set" should be read as historical context, not
> as a live design target.

One-pager for the builder. Revised after reading both the Codex research session (21-19-44) and the Claude research session (f7b267ee), and cross-checking against the project's own `JUDGE_DESIGN_LITERATURE_MAP_20260420.md`.

Every claim is either:
- (a) a primary reference verified in the project's canonical paper map, or
- (b) standard psychometric literature with a real citation, or
- (c) a measurement taken on our actual packet (sources noted), or
- (d) an inference from (a+b+c).

One honesty flag you'll see below:
- `[ESTIMATOR-LABEL]` — places where two different statistics of the same thing have different numerical values, and you must name which you mean.

(The project's arxiv ID set was re-verified against arxiv landing pages on 2026-04-21 — all 33 IDs resolve correctly. Earlier `[UNVERIFIED-ARXIV]` flags have been removed.)

---

## 1. What we are trying to measure — in one sentence

**Is this memory system better than that memory system at reconstructing the closest correct operative state at time `t` from a bounded observation packet?**

Project's canonical formalization (from `JUDGE_DESIGN_LITERATURE_MAP_20260420.md`):
- hidden state: `s_t`
- bounded observations: `o_{≤t}`
- answer / reconstruction: `r_t`

Success is **reconstruction-for-continuation**, not external task completion.

We don't measure this directly. We measure what a judge says about it. That's where all the noise lives.

---

## 2. The four sources of noise

Every number from the benchmark is some mixture of four kinds of variation. If you can't pull them apart, you can't tell architecture quality from instrument noise.

| Name | In English | What it means | What it is on our packet |
|------|-----------|---------------|-------------------------|
| **Probe variance** (`σ_α`) | Different questions are different difficulties | Some probes are harder; some are grep-able from the slice in one call | **Not computed.** Codex's variance decomposition wrote `α` in the equation but never estimated it. Separately, a construct-validity confound exists: some probes are retrieval-degenerate (R13/R11/R04 — load-bearing phrases appear 200–1500× in slice). On those probes the task is search, not memory reconstruction. |
| **Agent variance** (`σ_β`) | Same probe + same memory + same model — call twice, answers differ | The LLM answering is stochastic | **Not computed.** Needs ≥2 clean agent reps per config. We have 1, because gpt-5.4-mini contaminated the gpt-5.4 column (see memory `069e6a39…`). Codex named `β` in the equation but never estimated it either. |
| **Judge-identity variance** (`σ_γ`) | Opus-judge vs GPT-judge disagree systematically on the same answers | Judge identity is a bias source | **Estimated as a mean shift, not a variance.** Two arms: clean arm (GPT-answers scored by GPT vs Opus judges) = **+0.500** mean delta, weighted κ 0.239, binary exact 0.870. Confounded arm (Opus-answers scored by Opus vs GPT-**mini** judges) = **−0.491** mean delta, weighted κ 0.340, binary exact 0.912. Direction replicates cleanly; magnitude in the confounded arm partly reflects gpt-5.4 vs gpt-5.4-mini model-size, not pure judge-identity. |
| **Judge-flicker variance** (`σ_ε`) | Same judge, called 4× on same answers, disagrees with itself | Pure judge stochasticity | Two estimators, different numbers, not interchangeable: `σ_ε^cell = 0.1873` (cell-wise ordinal pstdev on 0–2, averaged over cells) and `σ_ε^pooled = 0.329` (pooled/raw SD across all verdicts). Label which one you mean. Both are measured on the 4-rep Opus intra-rater set (45 common valid cells). Flip rate 42.2% (19/45), **zero pass↔fail flips**, all flips adjacent-band. Under useful-vs-fail collapse: `σ_ε^collapsed ≈ 0.029`, binary κ ≈ 0.86, ~93% zero-variance cells. `[ESTIMATOR-LABEL]` |

**The math fact that makes this worth bothering with.** Any observed difference between two architectures is

```
  observed = true_effect + α_effect + β_effect + γ_effect + ε_effect
```

An architecture claim is credible only when `true_effect` is **larger than the combined noise terms**. Right now, on this packet, `α` and `β` are literally uncomputed. We know `γ` and `ε` are large. So: no architecture claim.

**Where this frame comes from:**
- **Project-canonical primary:** *CyclicJudge* (arxiv [2603.01865](https://arxiv.org/abs/2603.01865)) — judge identity as a first-class variance term; ANOVA with judge-identity term; fixed-budget collection design. This is the paper the project's literature map anchors the decomposition to.
- **Classical foundation:** generalizability theory, originally Cronbach, Gleser, Nanda & Rajaratnam (1972), *The Dependability of Behavioral Measurements*. Codex calls the decomposition "basically generalizability theory" but **never cites Cronbach by name**; this is the missing foundational grounding if you publish.

---

## 3. κ (kappa), plainly

**The problem κ solves.** Two judges agree 70% of the time — impressive? Not if 70% is what chance gives you. κ strips out the chance baseline.

```
  κ = (p_observed − p_chance) / (1 − p_chance)
```

**Interpretation bands** (Landis & Koch 1977, *Biometrics* 33(1):159–174):
- κ = 0 → chance. κ ≈ 0.2–0.4 → slight/fair. κ ≈ 0.4–0.6 → moderate. κ ≈ 0.6–0.8 → substantial. κ ≈ 0.8–1.0 → almost perfect.

These are conventions, not law.

**On our packet:**
- **Opus rejudging itself**, same config, 4 reps: pairwise exact 0.755–0.811, weighted κ 0.663–0.751. Substantial. The instrument is stable with itself.
- **Opus vs GPT on same answers**, 3-level: weighted κ 0.239 (clean arm) or 0.340 (confounded arm). **Poor to slight.** They're not measuring the same thing on 3-level.
- **Opus vs GPT, binary useful-vs-fail**: 0.87 exact (clean arm), 0.91 exact (confounded arm). **The collapse to binary buys most of the agreement back.**

**K (capital K) vs κ (kappa).** In JCB notes, "K" is the *number of raters*, not kappa. "K ≥ 3 calibration" = "want 3 judges to anchor the instrument." Unrelated to kappa.

**κ as a formula — Codex did not write it out.** Codex used weighted κ as a standard primitive without deriving it. If you publish, the formula needs to be on the page and the weighting scheme (linear vs quadratic) has to be specified. Current scripts: `scratch/sigma_eps_*.py`. Verify before publication.

**Source for κ itself:** Cohen (1960), *A coefficient of agreement for nominal scales*, Educational and Psychological Measurement 20(1):37–46. Weighted-κ: Cohen (1968), *Psychological Bulletin* 70(4):213–220. Neither is currently cited in project docs.

---

## 4. The rubric — what it actually is, and what R² tells us about it

**The rubric structure, verified from `benchmark_runner.py` / `benchmark_scorer.py`:**

It is **not** a flat 12-axis list. It is **3 top-level axes × 12 subcategories**, each scored `strong / partial / missed` ordinal:

1. **`factual_grounding`** (3 sub): `support`, `boundedness`, `uncertainty_calibration`
2. **`continuity`** (5 sub): `active_thread_selection`, `salience_relevance`, `state_transition_tracking`, `forgetting_residue_control`, `continuation_value`
3. **`coherence`** (4 sub): `cross_harness_braid`, `cross_session_consistency`, `artifact_routing_consistency`, `contradiction_handling`

Overall verdict (`pass / partial / fail`) is a **separate field**, not a composition of the 12.
Efficiency is **not** in the rubric — it's handled separately by the runner (see §8).

**What R² measures here.** "How much of the overall verdict can you predict from the 12 subcategory scores?" R² = 1.0 → fully determined; R² = 0 → unrelated.

**Numbers on our packet (pooled across conditions):**
- 12-axis full fit: R² = **0.754** (GPT-judge, adj 0.725, n=114) / **0.862** (Opus-judge, adj 0.845, n=111).
- `continuity.state_transition_tracking` alone: R² = **0.606** (GPT) / **0.731** (Opus).
- Top-3-axes for Opus: R² = **0.851** vs all-12 = 0.862. **Dropping 9 axes costs 0.011.**
- Reverse ablation (drop `state_transition_tracking`, refit on remaining 11): R² = **0.738** (GPT) / **0.840** (Opus). The axis is **not uniquely necessary** — its variance is recoverable from the other axes.

**Plain-words read.** One subcategory does ~70–80% of the work. The other 11 together add ~0.02 more. The rubric is over-specified; it's measuring one latent verdict through 12 highly-correlated surfaces.

**Three hypotheses, now with direct evidence:**
1. **Rubric artifact** — the schema was authored with state-transition as the target and the other axes are correlated skins. **Now live.** The reverse ablation shows the other 11 re-assemble a comparably good predictor.
2. **Genuine primitive** — recall really *is* "did you track what changed." **Now weakened.** If it were uniquely necessary, dropping it would crater R². It didn't.
3. **Accidental operationalization overlap** — both judges compute roughly the same thing two ways. **Consistent with the ablation.**

**Earlier draft of this doc said the falsifier "hasn't been run."** That was wrong — Codex ran it (see session 21-19-44, line 1683). Correction applied here.

**Where this frame comes from:**
- **Project-canonical primary:** *When Judgment Becomes Noise* (arxiv [2509.20293](https://arxiv.org/abs/2509.20293)) — schema incoherence, factor collapse, aggregation masking. The "distrust aggregate scalar summaries when they mask disagreement" move.
- **Load-bearing concern.** The entire rubric-prune logic hangs on this one paper. If you go to publication, cross-check with at least one independent rubric-validity source before citing.

---

## 5. What Codex got right

Codex's frame is **variance decomposition of an LLM-judge measurement**, anchored to CyclicJudge and *When Judgment Becomes Noise*. That's the right frame. Specifically:
- It names the noise sources so you can target them individually.
- It makes "our judge is reliable" (`σ_ε` small) testable separately from "our judges agree" (`σ_γ` small).
- It lets you compute the minimum effect size you'd need to claim A > B given measured noise — a power analysis.

Codex's numerical work on the packet is solid: denominator audit, κ computations, R² ablation, flip structure taxonomy, code-gate pre-filter design, retrieval-degeneracy audit. The actual numbers are consistent across the four 2×2 arms and replicate on the older ab07 packet.

---

## 6. Where the prior analysis is running ahead of the data

**Ranked by severity:**

1. **Variance decomposition written as if fit, but only `γ` and `ε` estimated.** Codex writes `X = μ + α + β + γ + ε` repeatedly and calls the frame "generalizability theory." But in this packet, `α` (probe) and `β` (agent) are **never computed**. No mixed-effects model is fit. No G-coefficient. The decomposition is a conceptual scaffold being spoken about as a fit model. Any architecture claim leaning on the full decomposition is leaning on two uncomputed terms.

2. **`σ_β` literally missing because of model-mix contamination.** We need ≥2 clean agent reps per cell. The gpt-5.4-mini runs contaminated the gpt-5.4 column. An earlier "60% / κ ≈ 0.05 GPT intra-rater" result has been retracted. Without clean reps, architecture comparisons cannot be attributed to architecture vs agent stochasticity.

3. **`σ_α` not measured; retrieval-degenerate probes are a construct-validity confound, not a variance-term contamination.** Some probes (R13/R11/R04) measure search quality — the answer's load-bearing phrases appear 200–1500× in the slice. That's a *different type of problem* than variance: those probes don't measure the named construct ("memory reconstruction") at all. Earlier framing called this "contamination of `σ_α`." Better framing: it's a **construct-validity confound**, to be handled by probe reclassification (retrieval-like vs reconstruction-like), not by variance estimation.

4. **2026-dated arxiv IDs in Codex's paper list were written from memory — but have since been verified.** Codex produced a 28+ paper list (session 21-19-44, lines 797, 1169, 2429) with specific arxiv IDs. Many are 2026-dated (`2602.xxx`, `2603.xxx`, `2604.xxx`, `2512.xxx`). Codex made **no web-search calls** in that session. A follow-up verification pass on 2026-04-21 (see `papers/nondeterministic_verifier_202604/FIELD_MAP_202604.md` §8) confirmed every arxiv ID in the project's paper map resolves correctly — no fabricated IDs were found. The discipline for future paper lists from model memory: always verify before quoting.

5. **"Papers as justification" without result-level citation.** Codex tags each method to 1–2 papers but **never quotes a specific result** from any cited paper. The citations function as method-name labels. If the user publishes, each `[CODEX-REF]` needs either (a) a quoted result that anchors the method, or (b) a classical psychometric source that pre-dates the arxiv ID and is textbook-stable.

6. **Claude's session (f7b267ee) had its own oversubscription pattern** — not the same as Codex's. Specifically:
   - Heavy `"memex said"` authority-lean: two consolidating summaries (lines 1319, 1321 of f7b267ee) are prefaced *"Memex added the arc I missed"* / *"Memex corrects me"*, using persistent memory as the load-bearing evidence without re-derivation. This is the pattern the benchmark is supposed to catch — and the project is enacting it.
   - Confident "rubric over-specified and factor-collapsed" framing based on a "schematic-adherence regression" whose R² numbers, predictor set, and fit are **not shown in-session**. The only numeric anchor offered is a loose "~25–35% variance explained." The specific R² = 0.73–0.86 numbers this doc cites **come from Codex's session and the scratch scripts, not from Claude's narrative.**
   - The +0.49 judge-effect gets treated as "the strongest durable claim" in the Apr 21 restatement (line 2292) despite the same-session caveats that `β` is contaminated and intra-rater GPT variance is missing.

7. **The 285-vs-228 denominator puzzle.** 4 runs × 57 cells = 228 verdicts. A prior note says "285." Unresolved whether an extra run was quietly included. Sanity-check before quoting 285.

**None of this means the math is wrong.** It means the math is honest on what it measured (`γ`, `ε`, some κ's, some R²'s) and the *presentation* has been running ahead of that — both agents, in different ways.

---

## 7. The literature — project-canonical, annotated

Copied and condensed from `JUDGE_DESIGN_LITERATURE_MAP_20260420.md`, cross-checked against the 2026-04-21 verification pass in `papers/nondeterministic_verifier_202604/FIELD_MAP_202604.md`. All IDs below resolve correctly to arxiv landing pages.

**Primary (immediate use):**
- **CyclicJudge** — [2603.01865](https://arxiv.org/abs/2603.01865). Judge identity as a variance term. Where we get the ANOVA-style decomposition frame.
- **When Judgment Becomes Noise** — [2509.20293](https://arxiv.org/abs/2509.20293). Schema incoherence, factor collapse, aggregation masking. Where we get the rubric-prune logic.
- **LLM-as-a-Verifier** — repo lineage; no formal citation trail yet. Used narrowly for artifact-grounded, repeated verification.

**Judge validity / grounding:**
- **No Free Labels** — [2503.05061](https://arxiv.org/abs/2503.05061). Agreement without grounded references is weak evidence.
- **Criterion-referenceability determines LLM-as-a-judge validity** — [2603.14732](https://arxiv.org/abs/2603.14732). What part of a task is legitimately judgeable.
- **Evaluating the Evaluator / adherence line** — [2408.08781](https://arxiv.org/abs/2408.08781). Judge prompt detail often buys less than expected.

**Protocol / panels / abstention:**
- **Trust or Escalate** — [2407.18370](https://arxiv.org/abs/2407.18370). Selective trust / abstention / escalation.
- **RULERS** — [2601.08654](https://arxiv.org/abs/2601.08654). Locked rubric + evidence-anchored scoring.
- **Replacing Judges with Juries / PoLL** — [2404.18796](https://arxiv.org/abs/2404.18796). Multi-judge aggregation baseline.
- **SCOPE** — [2602.13110](https://arxiv.org/abs/2602.13110).

**Task-shape neighbors:**
- **MemoryArena** — [2602.16313](https://arxiv.org/abs/2602.16313). Structural neighbor for multi-session agent-environment.
- **LongMemEval** — [2410.10813](https://arxiv.org/abs/2410.10813). Temporal correctness, updates, abstention.
- **LifeBench** — [2603.03781](https://arxiv.org/abs/2603.03781). Memory beyond declarative recall.
- **OSWorld** — [2404.07972](https://arxiv.org/abs/2404.07972). Partial-observability foil.

**Classical foundations — NOT currently in project docs, should be added before publication:**
- Cronbach, Gleser, Nanda & Rajaratnam (1972). *The Dependability of Behavioral Measurements.* Generalizability theory — the tradition behind the variance decomposition.
- Brennan (2001). *Generalizability Theory.* Modern treatment.
- Cohen (1960). *A coefficient of agreement for nominal scales.* EPM 20(1):37–46. κ itself.
- Cohen (1968). *Weighted kappa.* Psychological Bulletin 70(4):213–220.
- Landis & Koch (1977). *The measurement of observer agreement for categorical data.* Biometrics 33(1):159–174.
- Shrout & Fleiss (1979). *Intraclass correlations.* Psychological Bulletin 86(2):420–428.

**LLM-as-judge bias literature, replicated on our packet:**
- Length bias — short answers flip ~2× more often than long ones. Documented in Zheng et al. (2023), *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, arxiv [2306.05685](https://arxiv.org/abs/2306.05685).
- Self-preference — opus-agent gets +0.13 binary-agreement advantage from opus-judge. Documented widely in the MT-Bench line.
- Position bias — Wang et al. (2023), *Large Language Models are not Fair Evaluators*, arxiv [2305.17926](https://arxiv.org/abs/2305.17926).

---

## 8. The three axes of the benchmark — real status

You named accuracy + continuity + efficiency. Honest read:

### Accuracy (= recall / state reconstruction)
- **Operationally formalized.** The 3-axis × 12-subcategory rubric above is the accuracy-proxy currently scored.
- **Noise decomposed on two of four terms** (`γ`, `ε`). The other two (`α`, `β`) are uncomputed.
- **Rubric is over-specified.** R² drops ~0.011 when 9 of 12 subcategories are removed. One axis (`state_transition_tracking`) carries 70–80% of the signal.
- **Publication-ready?** *No.* Ship the instrument-noise decomposition and the rubric-collapse finding as a *diagnostic artifact*. The axis itself is not ready to ship as a leaderboard metric. Prior draft said "ready to ship" — retract.

### Continuity
- **Partially formalized.** The *word* continuity is already one of the three rubric axes, with 5 subcategories. That means it's operationally judged, but as an LLM-judge rubric, not as a formal scoring function.
- **What's missing:** a definition *separable from* the pass/partial/fail verdict. Right now, continuity-as-rubric-axis is just a lens on the same verdict the other axes also predict. A distinct continuity score would measure something like: *does state persist across session boundaries in a way the agent can pick up later*, which is a property of the *system*, not of a single answer.
- **Minimum formalization needed:** (i) a probe form that tests cross-session state preservation (answer at `t₁`, ask again at `t₂`, does state survive), (ii) a scoring function that is not a judge verdict on a single answer.

### Efficiency
- **Operationally tracked, not axiomatically scored.** The runner records per-probe `tool_calls`, `cost_usd`, `duration_ms`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `num_turns`. Rolled up to per-condition totals as efficiency ratios. The judge prompt **explicitly says** "Efficiency is handled separately from answer metadata by the runner. Do not score it here."
- **What's missing:** a composite metric that trades accuracy for cost, and a shared cost unit across architectures. The interesting claim is compression — how much less does the system need to carry to answer the same ask — which requires a "carry everything" baseline to compare against.
- **Minimum formalization:** a shared cost unit (probably `bytes-of-state-retained × ask-compute`), and an accuracy-per-unit-cost function.

**Honest read.** Accuracy has a formalization (contested rubric) and partial noise decomposition. Continuity has a fuzzy axis and no scoring function. Efficiency has real numbers and no composite. None of the three is publication-ready today; accuracy is closest, but only as an *instrument-diagnostic* artifact, not as a comparison result.

---

## 9. The smallest honest public claim, right now

From `JUDGE_DESIGN_LITERATURE_MAP`, §9: the next move is **not** more runs, more judges, more categories, or more math. It is:
1. Fix the rubric (prune toward the `small defensible judge` primitive set).
2. Ground it in artifacts (code-gates as pre-LLM filters).
3. Rejudge the existing packet with the simplified contract.
4. Prove the schema is coherent (R² on the pruned rubric, factor-collapse check).
5. Only then calibrate judge identity (cyclic panels, intra-rater reps).

**What you can credibly release now:**

> Here is an n=1 bounded-packet memory benchmark on real user traces. The packet, the asks, and the formalization are released. The judge instrument has been partially calibrated: judge-identity effect (+0.500 on the clean arm), judge-flicker (`σ_ε^cell = 0.187` / `σ_ε^pooled = 0.329`), and the binary useful-vs-fail collapse (κ = 0.86) are measured and reported. The 12-subcategory rubric is shown to be over-specified: a 3-axis reduction recovers R² within 0.011. Architecture comparisons are **not** released because (i) agent-level variance is not yet clean, (ii) some probes are retrieval-degenerate (construct-validity confound), and (iii) continuity and efficiency axes are not yet formalized as scoring functions.

That is a scientific contribution. It is the **ground** a leaderboard would stand on, not the leaderboard itself.

---

## 10. Words to retire, words to keep

**Retire:**
- "12-axis rubric" — it is 3 axes × 12 subcategories; the flat phrasing hides structure.
- "architecture ranking" on the current packet — say *diagnostic comparison* until `σ_β` is measured.
- "production > pure > zero" — retracted after contamination cleaning.
- "`state_transition_tracking` is a load-bearing primitive" — reverse ablation shows it is not uniquely necessary.
- "accuracy is ready to ship" — it isn't; what's ready is the instrument-diagnostic artifact.
- "`σ_ε = 0.329`" without a label — say `σ_ε^cell = 0.187` or `σ_ε^pooled = 0.329`.
- "σ_α is contaminated by retrieval-degenerate probes" — that's a *construct-validity confound*, not a variance-term issue.
- "memex said" as load-bearing evidence — always re-derive or cite a file.

**Keep:**
- "environment-first" / "bounded operative-state reconstruction" — accurate.
- "n=1 memory" — narrow, specific, publishable.
- "useful vs fail" — the collapsed metric we trust.
- "construct validity" — the right word for the retrieval-degenerate confound.
- "schema adherence" — the right word for the rubric-collapse diagnostic.

---

## 11. Open questions for the builder

1. **Continuity's scoring function.** Do you want continuity formalized as a cross-session property (`answer_t₁ → ask_t₂` state preservation) separate from the current rubric axis, or stay with the rubric-axis framing?
2. **Efficiency composite.** Shared cost unit: bytes-retained × compute, or something simpler?
3. **Publication target.** Public open release vs. first conversation with a specific lab? The framing tightens if we know.
4. **Reverse ablation re-report.** Codex ran the falsifier. Should we add the result to the public write-up as a positive finding ("rubric is over-specified, here's the fit"), or keep it internal while we redesign?
5. **2026 arxiv IDs.** Should we web-verify Codex's full paper list now, or prune to the `JUDGE_DESIGN_LITERATURE_MAP` set for anything public?

---

## Provenance of this doc

- **Primary literature map:** `research/n1-memory-lab/JUDGE_DESIGN_LITERATURE_MAP_20260420.md`
- **Formalization neighbors:** `research/n1-memory-lab/FORMALISM_AXES_AND_CYCLIC_JUDGE_20260420.md`, `COUNCIL_FORMALISM_20260420.md`, `FORMALISM_LAYER_SEPARATION_20260420.md`
- **Numerical source files:** `research/n1-memory-lab/scratch/sigma_eps_*_20260420.py`, `schematic_adherence_ablation_20260420.py`, `code_gate_dt_replay_20260420.py`, `fabrication_density_20260420.py`, `retro_sstate_rule_20260420.py`, `reward_asymmetry_cleaning_20260420.py`
- **Rubric source:** `benchmark_runner.py`, `benchmark_scorer.py`
- **JCB artifacts:** `research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_*`
- **Session digests informing this revision:**
  - Codex session 21-19-44 (research lane; produced the numbers)
  - Claude session f7b267ee (narrated the numbers via memex; did not derive)
  - Codex session 17-19-17 (release-engineering; no research content)
