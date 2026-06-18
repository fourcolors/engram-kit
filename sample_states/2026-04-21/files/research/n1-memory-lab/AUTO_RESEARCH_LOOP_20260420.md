# Auto Research Loop — 2026-04-20 evening

Status: live log. Writing down iterations as they resolve.

Rules for this loop:
- Research only. No new runs. No sonnet.
- Use the existing 285-verdict surface + the 4 opus intra-rater reps + the judge prose.
- Each iteration: fan-out in parallel subagents, consolidate, decide the next fan-out.
- Findings that contradict earlier notes must be called out, not buried.

---

## Data surface on disk (confirmed)

Canonical runs (under `runs/`):

| run dir | ask model | judge model | role |
|---|---|---|---|
| `ne13-real-15d-opus46-final-20260420T071500Z` | opus-4.6 | opus-4.6 | diagonal baseline |
| `ne13-real-15d-gpt54-final-20260420T071500Z` | gpt-5.4 | gpt-5.4 | diagonal baseline |
| `ne13-real-15d-opusask-gpt54judge-20260420T144210Z` | opus-4.6 | gpt-5.4 | 2×2 cross |
| `ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z` | gpt-5.4 | opus-4.6 | 2×2 cross |
| `ne13-real-15d-opusask-opusjudge-intrarater-20260420T200314Z` | opus-4.6 | opus-4.6 | opus intra rep 1 |
| `ne13-real-15d-opus46-intrarater-rep2-20260420T222645Z` | opus-4.6 | opus-4.6 | opus intra rep 2 |
| `ne13-real-15d-opus46-intrarater-rep3-20260420T222645Z` | opus-4.6 | opus-4.6 | opus intra rep 3 |
| `ne13-real-15d-gpt54-rep2-20260420T144210Z` | gpt-5.4-**mini** | gpt-5.4-mini | contaminated (wrong model) |
| `ne13-real-15d-gpt54ask-gpt54judge-intrarater-20260420T200314Z` | (see codex note) | gpt-5.4-**mini** | contaminated intra-rater |
| `ne13-real-15d-gpt54rep2-opusjudge-20260420T200314Z` | gpt-5.4-mini rep2 | opus-4.6 | contaminated ask side |

57 cells per run = 19 probes × 3 conditions.

Existing analysis scripts: `research/n1-memory-lab/scratch/schematic_adherence_20260420.py`.
Mining batches: `research/n1-memory-lab/judge-mining-20260420/BATCH_{A..F}.md`.

---

## Iteration 1 — questions

1. Binary `useful-vs-fail` cross-judge κ (inter-rater stability when we collapse to the binary usefulness surface).
2. Reduced-schema R² ablation (12 → 5 → 3 → 1 axes per judge).
3. σ_ε flip structure (which 19 of 45 opus cells drifted, and is the drift structured?).
4. Agreed-pass anchor characterization (cells where gpt and opus both scored pass).

---

## Binary useful-vs-fail inter-judge stability

Question: when we collapse `{pass, partial} → useful` and `{fail, invalid} → not_useful`, how well do gpt-5.4 and opus-4.6 judges agree *on the same agent's answers*?

Verdict coding: fail=0, partial=1, pass=2. `invalid` verdicts are excluded pairwise (counted separately). κ computed by hand as (Pa − Pe)/(1 − Pe) with Pe = Σ p_row_i · p_col_i.

Runs used:

- gpt-agent × gpt-judge (diag): `runs/ne13-real-15d-gpt54-final-20260420T071500Z`
- opus-agent × opus-judge (diag): `runs/ne13-real-15d-opus46-final-20260420T071500Z`
- gpt-agent × opus-judge (cross): `runs/ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z`
- opus-agent × gpt-judge (cross): `runs/ne13-real-15d-opusask-gpt54judge-20260420T144210Z`

### gpt-agent answers: gpt-judge vs opus-judge

- n intersect (both runs have cell): 57 / 57
- skipped (key missing in one run): 0
- excluded (invalid on either side): 3
- n used: 54

| metric | value |
|---|---|
| exact 3-level match | 48.1% |
| binary useful match | 87.0% |
| Cohen's κ (3-level: fail/partial/pass) | 0.151 |
| Cohen's κ (binary: useful/not_useful) | 0.411 |
| mean ordinal shift (fail=0,partial=1,pass=2) | 0.537 |

Per-condition:

| condition | n | exact 3-lvl | binary | κ 3-lvl | κ binary | mean shift |
|---|---|---|---|---|---|---|
| pure | 19 | 57.9% | 94.7% | 0.174 | 0.000 | 0.474 |
| zero | 18 | 38.9% | 72.2% | 0.015 | 0.211 | 0.611 |
| production | 17 | 47.1% | 94.1% | 0.246 | 0.767 | 0.529 |

### opus-agent answers: opus-judge vs gpt-judge

- n intersect (both runs have cell): 57 / 57
- skipped (key missing in one run): 0
- excluded (invalid on either side): 0
- n used: 57

| metric | value |
|---|---|
| exact 3-level match | 50.9% |
| binary useful match | 91.2% |
| Cohen's κ (3-level: fail/partial/pass) | 0.270 |
| Cohen's κ (binary: useful/not_useful) | 0.712 |
| mean ordinal shift (fail=0,partial=1,pass=2) | 0.526 |

Per-condition:

| condition | n | exact 3-lvl | binary | κ 3-lvl | κ binary | mean shift |
|---|---|---|---|---|---|---|
| pure | 19 | 57.9% | 94.7% | 0.324 | 0.771 | 0.421 |
| zero | 19 | 47.4% | 89.5% | 0.246 | 0.759 | 0.579 |
| production | 19 | 47.4% | 89.5% | 0.202 | 0.457 | 0.579 |

### Comparison to opus intra-rater (σ_ε baseline)

From prior work (`RATING_ROULETTE`, `OPUS_INTRA_RATER`):

- opus judge vs itself (intra-rater): κ ≈ 0.65 on 3-level, ~97.6% binary match.

Inter-rater binary numbers from above:

- gpt-agent answers, gpt-judge vs opus-judge: binary match 87.0%, κ_binary = 0.411 (n=54 after 3 invalid excluded).
- opus-agent answers, opus-judge vs gpt-judge: binary match 91.2%, κ_binary = 0.712 (n=57, 0 invalid).

Binary surface is **not** as stable across judges as within one judge. Opus intra-rater binary agreement (~97.6%) is higher than either cross-judge binary match rate. On gpt-agent answers specifically, collapsing to binary only gets κ_binary = 0.41 — well below the opus-within-opus regime. On opus-agent answers the inter-rater binary κ (0.71) is closer to, but still below, the opus intra-rater figure.

Read: binary collapse *reduces* the cross-judge disagreement relative to 3-level (where κ is 0.15 and 0.27 respectively), but it does not eliminate it. The binary useful/not-useful surface is judge-dependent on gpt-agent output in particular; it is noticeably tighter on opus-agent output. Within-judge (opus intra-rater) agreement remains the ceiling.

Per-condition note: on gpt-agent answers the `pure` cell shows 94.7% binary match but κ_binary = 0.0 — the minority class has ~1 example, so κ is degenerate and match % is misleading there. Conditions where inter-rater binary κ approaches the opus intra-rater neighborhood: `production` on gpt-agent (κ=0.77), and `pure`/`zero` on opus-agent (κ≈0.77, 0.76).

---

## σ_ε flip structure in opus intra-rater

Question: the 4-run opus judge packet (baseline + 3 reruns on the SAME frozen opus-4.6 agent answers) has 45 cells with a verdict in all 4 reps, 26/45 identical and 19/45 drifted. Where does the drift live?

Runs (all `judge_only_from` the baseline `results.json`, confirmed via `config.json`):

- baseline: `runs/ne13-real-15d-opus46-final-20260420T071500Z`
- rep1:     `runs/ne13-real-15d-opusask-opusjudge-intrarater-20260420T200314Z`
- rep2:     `runs/ne13-real-15d-opus46-intrarater-rep2-20260420T222645Z`
- rep3:     `runs/ne13-real-15d-opus46-intrarater-rep3-20260420T222645Z`

Reproducer: `research/n1-memory-lab/scratch/sigma_eps_flip_structure_20260420.py`.

### Identical vs flipped by condition

| condition | total cells | identical | flipped | flip rate |
|---|---:|---:|---:|---:|
| pure | 16 | 8 | 8 | 50.0% |
| zero | 16 | 10 | 6 | 37.5% |
| production | 13 | 8 | 5 | 38.5% |
| **all** | **45** | **26** | **19** | **42.2%** |

`pure` is the noisiest condition; `zero` and `production` are indistinguishable at this n.

### Flip span

All 19 flipped cells span exactly **one band** on the {fail, partial, pass} ordinal — **0 cells** span pass↔fail. σ_ε is entirely adjacent-band flicker, never a full reversal.

### The 19 flipped cells (verdict sequence = [baseline, rep1, rep2, rep3])

- (R04, production): [partial, partial, pass, partial]
- (R11, production): [pass, pass, partial, pass]
- (R12, production): [partial, partial, partial, pass]
- (R14, production): [partial, pass, partial, partial]
- (R15, production): [pass, pass, pass, partial]
- (R01, pure): [pass, pass, pass, partial]
- (R03, pure): [partial, partial, pass, partial]
- (R04, pure): [pass, partial, pass, partial]
- (R06, pure): [pass, partial, pass, pass]
- (R07, pure): [pass, partial, partial, pass]
- (R08, pure): [fail, fail, partial, fail]
- (R15, pure): [partial, partial, partial, pass]
- (R18, pure): [partial, fail, fail, fail]
- (R03, zero): [partial, fail, fail, fail]
- (R07, zero): [partial, pass, pass, partial]
- (R11, zero): [partial, partial, partial, pass]
- (R12, zero): [partial, pass, pass, pass]
- (R14, zero): [pass, pass, partial, pass]
- (R19, zero): [partial, partial, partial, pass]

Pattern: 16/19 flipped cells are a pass↔partial flicker; only 3/19 are partial↔fail ((R08,pure), (R18,pure), (R03,zero)) — the partial↔fail ones are the "was this useful at all" boundary and cluster on harder conditions.

### Probes that always flip

Probes where *every* cell with 4-rep overlap flipped: **R07** (2/2), **R08** (1/1), **R14** (2/2). Probes with mostly-flipped cells: R03 (2/3), R04 (2/3), R11 (2/3), R12 (2/3), R15 (2/3). Probes with mostly-identical cells: R01, R18, R19 (1/3 each). Drift is not uniform across probes — a handful of probes sit on a rubric boundary the judge cannot resolve twice the same way.

### Identical cells — what verdicts agree?

| shared verdict | n |
|---|---:|
| all-pass | 17 |
| all-partial | 5 |
| all-fail | 4 |

Most agreement lives on clear-pass answers (17/26 ≈ 65%), not on clear-fail. The "easy to agree this is bad" intuition is wrong here — the opus judge is more confidently calling passes than failures. Middle-band `partial` rarely survives 4 reps (5/26).

### Which rubric axis is doing the flipping?

Of 19 flipped cells, how many of the 3 top-level axes change score across the 4 reps:

- 1 axis flips: 1 cell
- 2 axes flip: 8 cells
- 3 axes flip: 10 cells

Per-axis flip count across the 19 flipped cells: `coherence` 18, `factual_grounding` 17, `continuity` 12. Top sub-axes: `coherence.cross_session_consistency` 17, `factual_grounding.uncertainty_calibration` 16, `continuity.state_transition_tracking` 15, `coherence.artifact_routing_consistency` 15, `coherence.contradiction_handling` 15.

The flip is **not localized** — when a verdict moves, nearly every sub-axis moves with it. This looks like the judge re-drawing the whole rubric in one pass rather than wobbling on one axis. Consistent with the "rubric is coherent but over-specified / collapsing to one judgment" reading from `CALIBRATION_STACK_20260420.md`.

### Answer-length correlation

Answer lengths (chars) pulled from baseline `answer_text`:

| group | n | mean | median | min | max |
|---|---:|---:|---:|---:|---:|
| flipped | 19 | 3154 | 2361 | 494 | 9987 |
| identical | 26 | 4885 | 3922 | 33 | 15200 |

Flip rate by length quartile (quartiles across all 45 cells: Q1=1990, Q2=3291, Q3=5296):

| bucket | flipped/total | flip rate |
|---|---|---:|
| ≤Q1 | 7/12 | 58.3% |
| (Q1,Q2] | 6/11 | 54.5% |
| (Q2,Q3] | 3/11 | 27.3% |
| >Q3 | 3/11 | 27.3% |

Short answers flip roughly 2× as often as long answers. Short opus-4.6 answers tend to be terse hedges that the judge can read as either "honest 'I don't know'" (partial/pass) or "unhelpful empty response" (partial/fail) — exactly the pass↔partial and partial↔fail boundary the flip data shows. Longer answers give the rubric more to latch onto.

### Takeaway

The σ_ε drift is **structured, not random**: it lives in adjacent-band flicker (never pass↔fail), concentrates on short answers and on a subset of probes (R07, R08, R14 always flip), and when a cell flips almost all sub-axes move in lockstep — i.e. the judge is re-scoring the whole rubric around a single unresolved verdict decision rather than wobbling on one rubric axis.

---

## Agreed-pass anchor cells

Method: for each agent (gpt-agent, opus-agent), on each (probe_id, condition) cell of the 2×2 cross, pair the gpt-judge verdict and the opus-judge verdict on the *same* answer, then classify the pair. AGREED_PASS cells are the only place an architectural claim is not confounded by judge identity — they survive both judges saying pass on the same text.

Runs paired:
- gpt-agent: `ne13-real-15d-gpt54-final-20260420T071500Z` (gpt-judge) × `ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z` (opus-judge)
- opus-agent: `ne13-real-15d-opus46-final-20260420T071500Z` (opus-judge) × `ne13-real-15d-opusask-gpt54judge-20260420T144210Z` (gpt-judge)

### 1. Class counts per agent (57 cells each)

| class | gpt-agent | opus-agent |
|---|---|---|
| AGREED_PASS | 5 | 4 |
| AGREED_PARTIAL | 18 | 17 |
| AGREED_FAIL | 3 | 8 |
| DISAGREE_P_vs_P (pass / partial) | 21 | 23 |
| DISAGREE_P_vs_F (pass / fail — full band flip) | 1 | 2 |
| DISAGREE_PA_vs_F (partial / fail) | 6 | 3 |
| invalid opus-judge output | 3 | 0 |

On gpt-agent, 3 cells (R06/production, R14/production, R14/zero) had `verdict="invalid"` from the opus judge (JSON-parse failure surface) and are excluded from the paired cross-tab. Total agreed-pass across both agents: **9** cells. (Prior note said 6 — updating that. The 6 figure appears to have been a pre-invalid-exclusion or diagonal-only subset.)

### 2. AGREED_PASS cells — probe × condition breakdown

| agent | probe | condition | prompt (≤120c) |
|---|---|---|---|
| gpt-agent | R01 | pure | what's the current state of things? what am I working on, what's active, what's the latest? |
| gpt-agent | R04 | production | give me my work log today PST entire day |
| gpt-agent | R12 | production | what specific next steps were discussed for Observe after Phase 2? |
| gpt-agent | R13 | pure | what was the evolution of the adapter-as-compiler concept? |
| gpt-agent | R15 | zero | can we get back to the previous thread of running our tests for observe layer, with real data as if I set up the sys… |
| opus-agent | R02 | production | What did we work on yesterday March 7 2026 and today March 8 2026? List everything — commits, features, fixes, relea… |
| opus-agent | R11 | pure | What is the full vision for Observe? Everything we discussed — hook listener, tool reduction, federation, real-time … |
| opus-agent | R13 | production | what was the evolution of the adapter-as-compiler concept? |
| opus-agent | R13 | pure | what was the evolution of the adapter-as-compiler concept? |

Condition tally (both agents pooled): **production=4, zero=1, pure=4**. Prior expectation was `production > zero > pure`; the data does **not** back that. `pure` ties `production` on agreed-pass count, `zero` is the thinnest band. R13 ("evolution of adapter-as-compiler concept") is the only probe with three independent agreed-pass cells (gpt-agent/pure, opus-agent/production, opus-agent/pure) — a narrative/historical-reconstruction probe whose answer stays graded-pass across both judges.

### 3. DISAGREE_P_vs_F cells (worst disagreements — full band flip)

Three cells where one judge said pass and the other said fail on the same answer:

| agent | probe | condition | direction |
|---|---|---|---|
| gpt-agent | R03 | pure | opus-lenient (opus=pass, gpt=fail) |
| opus-agent | R05 | production | opus-lenient (opus=pass, gpt=fail) |
| opus-agent | R19 | zero | opus-lenient (opus=pass, gpt=fail) |

All three flips go the **same direction**: opus judged pass, gpt judged fail. No P-vs-F cell has gpt-pass / opus-fail. That is a structural bias, not random noise.

Reasoning flavor (≤80c each):

- **R03/pure (gpt-agent)**
  - gpt(fail): "Grounded on the commit trail, but it misses the final live state."
  - opus(pass): "Strong answer that correctly identifies the active work thread…"
- **R05/production (opus-agent)**
  - gpt(fail): "partially grounded… but it misses the user's current live thread map."
  - opus(pass): "exceptionally comprehensive reconstruction of the user's working state…"
- **R19/zero (opus-agent)**
  - gpt(fail): "The response is largely ungrounded and misses the actual live thread."
  - opus(pass): "accurately reconstructs the user's most recent session…"

Pattern: gpt-judge weights "did you land on the *final* live thread at cutoff" heavily and fails answers that walk the history correctly but miss the most recent pivot; opus-judge rewards structured reconstruction even when the tip is off. That is the disagreement axis, not arbitrary noise.

### 4. Agreed-pass architectural verdict

**agreed-pass count: production=4, zero=1, pure=4**

That is the only architecture ordering defensible across judges today. Read literally: `production ≈ pure > zero`. This contradicts the prior working assumption that `production > zero > pure`. In particular, `pure` (MEMEX-only) ties `production` on the judge-agnostic band-top surface, and `zero` (no MEMEX, search-only) is the weakest. Caveat: R13 alone contributes 2 of 4 pure-agreed-pass cells, so the `pure` count is concentrated in one narrative-history probe.

### Caveat

This is a **ceiling estimate of architectural signal, not a significance test**. n=9 agreed-pass cells across 114 pair-cells is small; no band separation here reaches inferential weight. The right use of this table is as an anchor: it marks the cells where an architectural claim is not confounded by judge identity, so follow-up work (manual adjudication, σ_ε targeting, per-probe replay) should start from these 9 cells plus the 3 P-vs-F disagreements.

---

## Reduced-schema R² ablation

Question: if the 12-axis Feuer-style rubric gives R²=0.754 (gpt-judge) and R²=0.862 (opus-judge) of verdict variance, how much of that is doing real work vs. filler? Re-fit each pooled per-judge regression on progressively smaller axis subsets.

- Data: pooled per judge = diagonal (judge==ask) + cross (judge!=ask). n(gpt-judge)=114, n(opus-judge)=111 after dropping rows with missing/invalid sub-axis scores.
- Model: OLS of `overall_verdict ∈ {fail=0, partial=1, pass=2}` on sub-axis scores `{missed=0, partial=1, strong=2}` via `np.linalg.lstsq` (normal equations). Adj-R² uses the standard `1 − (1−R²)(n−1)/(n−p−1)`.
- Script: `research/n1-memory-lab/scratch/schematic_adherence_ablation_20260420.py`.
- TOP-5 is the a-priori pick from prior work (per-judge load-bearing axes). TOP-3 is chosen empirically from the 12-axis fit (largest |β_std|). TOP-1 is `state_transition_tracking` for both judges.

### gpt-judge (n=114)

| Subset | Axes | R² | adj-R² | ΔR² vs full |
|---|---|---|---|---|
| ALL-12 | all 12 | **0.754** | 0.725 | 0.000 |
| TOP-5 (a priori) | state_transition_tracking, cross_session_consistency, boundedness, contradiction_handling, forgetting_residue_control | 0.726 | 0.714 | −0.027 |
| TOP-3 (empirical) | state_transition_tracking, cross_session_consistency, forgetting_residue_control | 0.711 | 0.703 | −0.043 |
| TOP-1 | state_transition_tracking | 0.606 | 0.603 | −0.147 |

β coefficients in the 12-axis fit, ranked by |β_std|:

| axis | β_std | β_raw |
|---|---|---|
| continuity.state_transition_tracking | +0.227 | +0.190 |
| coherence.cross_session_consistency | +0.159 | +0.148 |
| continuity.forgetting_residue_control | +0.144 | +0.125 |
| coherence.cross_harness_braid | +0.126 | +0.105 |
| factual_grounding.boundedness | +0.126 | +0.133 |
| continuity.salience_relevance | +0.104 | +0.076 |
| coherence.artifact_routing_consistency | +0.097 | +0.078 |
| continuity.active_thread_selection | +0.074 | +0.049 |
| continuity.continuation_value | −0.062 | −0.052 |
| factual_grounding.support | +0.061 | +0.060 |
| factual_grounding.uncertainty_calibration | −0.059 | −0.052 |
| coherence.contradiction_handling | +0.036 | +0.030 |

Near-zero axes (|β_std| < 0.05): `coherence.contradiction_handling` only. gpt spreads verdict weight across ~8 axes; no long tail of vacuous predictors. The a-priori TOP-5 includes `contradiction_handling` (β_std=0.036) and `boundedness` (0.126) but misses `cross_harness_braid` (0.126) and `salience_relevance` (0.104) — the prior-work pick was close but not identical to the empirical ranking.

### opus-judge (n=111)

| Subset | Axes | R² | adj-R² | ΔR² vs full |
|---|---|---|---|---|
| ALL-12 | all 12 | **0.862** | 0.845 | 0.000 |
| TOP-5 (a priori) | state_transition_tracking, factual_grounding.support, active_thread_selection, continuation_value, salience_relevance | 0.853 | 0.846 | −0.009 |
| TOP-3 (empirical) | state_transition_tracking, factual_grounding.support, active_thread_selection | 0.851 | 0.847 | −0.011 |
| TOP-1 | state_transition_tracking | 0.731 | 0.728 | −0.132 |

β coefficients in the 12-axis fit, ranked by |β_std|:

| axis | β_std | β_raw |
|---|---|---|
| continuity.state_transition_tracking | +0.322 | +0.306 |
| factual_grounding.support | +0.273 | +0.302 |
| continuity.active_thread_selection | +0.123 | +0.118 |
| coherence.cross_harness_braid | +0.097 | +0.095 |
| coherence.contradiction_handling | +0.091 | +0.093 |
| coherence.artifact_routing_consistency | +0.083 | +0.088 |
| continuity.continuation_value | +0.058 | +0.060 |
| factual_grounding.uncertainty_calibration | +0.028 | +0.030 |
| factual_grounding.boundedness | −0.023 | −0.027 |
| coherence.cross_session_consistency | +0.014 | +0.014 |
| continuity.forgetting_residue_control | +0.009 | +0.010 |
| continuity.salience_relevance | −0.008 | −0.008 |

Near-zero axes (|β_std| < 0.05): `uncertainty_calibration`, `boundedness`, `cross_session_consistency`, `forgetting_residue_control`, `salience_relevance` — **5 of 12 axes are effectively vacuous for opus-judge**. The empirical TOP-3 (state_transition_tracking + factual_grounding.support + active_thread_selection) captures R²=0.851, losing only 0.011 off the 12-axis fit. adj-R² is actually *higher* for TOP-3 (0.847) than ALL-12 (0.845) — the 9 dropped axes cost more in degrees of freedom than they pay back in explained variance.

The a-priori TOP-5 includes `continuation_value` (β_std=0.058) and `salience_relevance` (−0.008) which are near-vacuous, and misses `cross_harness_braid` (0.097) and `contradiction_handling` (0.091) which are not.

### Takeaways

- **opus-judge has a clear 3-axis backbone**: `state_transition_tracking`, `factual_grounding.support`, `active_thread_selection` → R²=0.851, adj-R²=0.847. The 12-axis rubric is over-specified for opus — adj-R² actually improves under pruning.
- **gpt-judge distributes verdict weight more broadly**: TOP-3 drops to 0.711 (−4.3 pp) and adj-R² drops 2.2 pp. The rubric's shape is closer to necessary for gpt. Only `contradiction_handling` is cleanly prunable.
- **state_transition_tracking alone reaches R²≈0.61 (gpt) / 0.73 (opus).** That single axis explains ~80% (gpt) / ~85% (opus) of what the full 12-axis rubric explains. For a cheap screen this is the axis to keep.
- **Judges use different rubric shape**: opus leans on continuity + factual support (thread state + grounding in the episode); gpt leans on continuity + cross-session/forgetting + factual boundedness. The intersection is `state_transition_tracking`. Diverging β profiles are consistent with the cross-judge κ drop reported above (gpt-judge vs opus-judge 3-level κ = 0.15–0.27), and with the σ_ε finding that when an opus-verdict flips, nearly all sub-axes move in lockstep.

### Caveats (flagged honestly)

- **n is near the EFA floor**: 114 / 111 rows with 12 predictors = ~9.5 obs/predictor. Standard errors on individual β's are wide; the ranking is stable in point estimate but not bootstrapped here.
- **Post-hoc selection inflates TOP-k R²**: the empirical TOP-3 subset was chosen by |β_std| from the same data used to compute its R². The gap between TOP-3 and ALL-12 is therefore an optimistic lower bound on how much the other 9 axes contribute — an honest estimate would use held-out folds or a pre-registered axis set. The a-priori TOP-5 does not have this leakage.
- **Verdict-on-subaxis is partly mechanical**: both are derived from the same rubric in the same judge pass, so high R² is partly a consistency check on the judge's own arithmetic, not a construct-validity claim. Low R² would have been alarming; high R² is only weak positive evidence for the rubric.
- **Pooled across 2 ask models**: per-cell fits (4 configs × 12 axes on n≈27–29 each) would be underpowered and are not run here.

---

## Iteration 1 consolidation

### Headline shifts vs prior notes

1. **Agreed-pass is 9 cells, not 6.** `JUDGE_MINING_SYNTHESIS_20260420.md` will need a footnote. The extra three cells are on opus-agent (R11/pure, R13/prod, R13/pure).
2. **The "binary useful-vs-fail" surface is NOT uniformly stable across judges.** Opus intra-rater binary ≈ 97.6% does not generalize — cross-judge binary κ on gpt-agent answers is **0.41** (match rate 87%). Opus-agent pulls to κ = 0.71. The 97.6% figure is a within-opus number, not a cross-judge stability claim. Codex's original framing needs this asymmetry appended.
3. **σ_ε drift is structured, not random.** All 19 flipped cells are adjacent-band flicker, never pass↔fail. Drift concentrates on (i) `pure` condition (50% flip rate), (ii) short answers (<Q2 median flips ~55%, >Q3 drops to 27%), (iii) a small probe set (R07, R08, R14 always flip).
4. **When opus-judge flips a verdict, ALL three top-level axes move in lockstep** (10/19 cells have all 3 flipping; only 1/19 is a single-axis flip). This is direct evidence that the 12-axis rubric is measuring one latent verdict dimension, not 12 independent constructs. It also bounds what CyclicJudge-style averaging can buy us.
5. **Structural bias in P↔F disagreements**: all 3 full-band flips go opus=pass, gpt=fail — not random directionally. Opus rewards "comprehensive reconstruction," gpt demands tip-accurate "final live thread." This is a definitional disagreement, not inter-rater noise.
6. **Architectural ordering from the agreed-pass anchor: `production ≈ pure > zero`** — contradicts expected `production > zero > pure`. But R13 ("evolution of the adapter-as-compiler concept") contributes 2/4 pure-agreed-pass cells; if R13 is degenerate (filesystem-grep-able), pure's rank collapses.
7. **Reduced schema is viable for opus, not for gpt.** Opus top-3 axes capture 98.7% of ALL-12 R² (0.851 vs 0.862), adj-R² actually improves under pruning. Gpt top-3 loses 4.3 pp — its rubric shape is closer to necessary.

### What this reframes

- The redesigned judge contract (`D_t + S_t` from `COUNCIL_FORMALISM_20260420.md`) looks better motivated than before: the lockstep-axis finding says the rubric is already collapsing toward a single latent judgment anyway; explicit narrowing is honest.
- **But** the structural P↔F disagreement direction says different judges encode different definitions of "operative-state adequacy." That is upstream of any rubric — the `s_state` primitive itself is judge-defined. A single written contract for `s_state` may be the minimum needed before rejudging.
- R13's concentration is the single biggest confound in the agreed-pass ordering. Needs a manual read.

### Iteration 2 questions

1. **R13 dive** — read the 3 agreed-pass R13 traces. Is R13 genuinely cross-architecture-consistent, or is the adapter-as-compiler thread sitting in the filesystem and trivially greppable? If degenerate, drop from the anchor set.
2. **Structural-bias anatomy** — the 3 opus=pass/gpt=fail cells: extract the exact disagreement axis from the reasoning prose. Can we write a one-line operational definition of `s_state` that would force both judges into agreement?
3. **Length × flip-rate + length × binary-disagreement** — does the answer-length effect on σ_ε (opus intra) also explain the gpt-agent vs opus-agent κ_binary gap (0.41 vs 0.71)? If opus-agent's longer answers are what make them judge-stable, that's an agent-side finding, not a judge-side one.
4. **Paper cross-check: Rulers evidence-extractor split** — given lockstep axes, would an extract-then-score pipeline (first cite spans from `E_t`, then score only over cited content) actually reduce σ_ε? Sketch the expected effect.

---

## Rulers-style extract-then-score sketch

Motivation: the σ_ε flip pattern above — 10/19 flipped cells have all 3 top-level axes moving in lockstep — is evidence the judge is re-deriving one latent verdict per pass, not wobbling on independent axes. Rulers ("Locked Rubrics", arxiv 2601.08654) frames exactly this failure: if the judge re-chooses which evidence to anchor to on every rerun, the rubric becomes a post-hoc justification of that anchor choice. The proposed fix is a two-stage judge: Stage 1 EXTRACT freezes the evidence set; Stage 2 SCORE runs the D_t/S_t contract over the frozen extract only, with no access to the raw slice. Map: Rulers.extract → pre-`D_t` step; Rulers.score → `D_t → S_t → V_t`.

### Stage 1 (EXTRACT) — pseudo-JSON contract

```
INPUT: { q_t, r_t, E_t_slice, local_git_anchor }
INSTRUCTION: do NOT score. List every claim r_t makes that an evaluator
             would need to check; for each claim, cite the supporting span
             from E_t (or mark "absent"). No verdicts, no rubric words.
OUTPUT: {
  "claims": [
    {
      "claim_id": "c1",
      "claim_text": "<verbatim from r_t>",
      "matching_span": "<verbatim from E_t_slice>" | "absent",
      "span_source": "slice" | "local_git_anchor" | "absent",
      "artifact_name": "<file/commit/branch/issue>" | null,
      "anchor_time": "<ISO>" | null,
      "claim_kind": "factual" | "temporal" | "state" | "plan"
    }
  ],
  "unsourced_claims_count": <int>,
  "live_thread_candidates": ["<span from E_t>", ...]
}
```

### Stage 2 (SCORE) — pseudo-JSON contract

```
INPUT:  { q_t, r_t, extract_output }   // NO raw E_t_slice
CONSTRAINT: every d_* / s_* justification MUST cite a claim_id from
            extract_output. Any verdict appealing to unextracted evidence
            is invalid.
OUTPUT: {
  "D_t": {
    "d_time":      {"score": "ok|minor|major", "cites": ["c2"]},
    "d_artifact":  {"score": "ok|mismatch|absent", "cites": ["c1","c4"]},
    "d_committed": {"score": "ok|mismatch|n/a", "cites": [...]},
    "d_contra":    {"score": "none|minor|central", "cites": [...]},
    "d_complete*": {"fires": bool, "score": "...", "cites": [...]},
    "d_cross*":    {"fires": bool, "score": "...", "cites": [...]},
    "d_prov*":     {"fires": bool, "score": "...", "cites": [...]},
    "c_type":      {"verified": [ids], "inferred": [ids], "speculative": [ids]}
  },
  "S_t": {
    "s_state":   {"score": "strong|partial|missed", "cites": [live_thread_ids]},
    "s_restart": {"score": "low|med|high", "cites": [...]}
  },
  "V_t": "pass | partial | fail | invalid"
}
```

### Expected σ_ε effect on the three always-flip probes

- **R07 (zero & pure, 2/2 flipped, pass↔partial flicker both times)**: R07 answers are mid-length and hinge on whether the tip thread was named. Stage 1 would surface ≤ 6 claims and most likely freeze the `live_thread_candidates` list across reps. Predicted σ_ε drop: **moderate to large** — the flicker is exactly the "what counts as the live thread?" question Stage 1 pins down.
- **R08 (pure, 1/1 flipped, partial↔fail)**: short hedged answer sitting on the partial↔fail boundary — the lockstep finding predicts Stage 1 would produce 1–3 claims only, which risks locking σ_ε *into* fail if the extractor decides the sparse answer has no grounded claim. Predicted effect: **σ_ε reduces numerically but may bias the verdict toward fail** (regression to a judge-independent "not enough here" floor).
- **R14 (production & zero, 2/2 flipped, pass↔partial both times)**: R14 lives on artifact-routing correctness. `d_artifact` is a substring check once claims are extracted, so Stage 2 becomes near-deterministic given the extract. Predicted σ_ε drop: **large**, conditional on Stage 1 stability.

Aggregate prediction: Stage 2 σ_ε ≈ 0 *given* Stage 1 output fixed. End-to-end σ_ε = Var(Stage 1) propagated through a near-deterministic Stage 2, so overall σ_ε is bounded by extractor stability. Expect total σ_ε to roughly halve on long-answer cells, flat-to-worse on R08-style terse cells.

### Expected σ_γ (cross-judge) effect

Likely **worse**, or at best neutral. The structural P-vs-F bias (opus=pass / gpt=fail, 3/3 directional) came from a definitional split on "did you land on the tip?" That is a Stage 1 disagreement — gpt will extract the tip claim as the load-bearing one and mark it `absent`; opus will extract the structured reconstruction claims and treat them as sufficient. Pinning Stage 2 to the extract amplifies that definitional gap rather than hiding it. Net: extract-then-score clarifies *where* judges disagree but does not make them agree.

### D_t items better served by code gates than an LLM extractor

- `d_time`: date-leakage regex over `r_t` vs `reference_dt` — pure code. Drop from the LLM contract.
- `d_artifact`: substring match of named artifacts (files, commit SHAs, branches, issue IDs) against `E_t_slice ∪ local_git_anchor`. Near-deterministic; LLM only needed to name the artifact.
- `d_committed`: diffable against `local_git_anchor.json` — code gate with a small LLM tiebreak layer for semantic framing.
- Leave to LLM: `d_contra`, `c_type`, `s_state`, `s_restart`, `d_complete*`, `d_cross*`, `d_prov*`.

Consequence: the honest version of Rulers here is "code gates for the deterministic core, LLM extract-then-score for the semantic residual only." That reduces the extractor's job to ~4–5 claim types and should tighten its σ_ε.

### Ranked cheap experiments (falsify/support without a rebuild)

1. **Extractor-only rerun stability (cheapest).** Run Stage 1 four times on the 19 flipped cells, no Stage 2. Measure Jaccard on `claims[].claim_id` sets and agreement on `live_thread_candidates`. If Stage 1 itself has σ ≥ σ_ε, the design cannot help. Cost: 76 extract calls, no new agent runs.
2. **Manual extract, LLM score.** Hand-write the extract output for the 19 flipped cells (1–2 hrs). Run Stage 2 four times. If σ_ε on the scorer → verdict collapses near zero, the lockstep finding is confirmed and the bottleneck is the extractor. If σ_ε persists, the lockstep finding is wrong and Rulers won't rescue it.
3. **Code-gate `d_time` + `d_artifact` on current verdicts.** Re-derive those two axes deterministically on the 285-verdict surface; compare with judge scores. ≥ 90% agreement means the LLM was doing rote string-matching there and can be removed from the contract today, independent of Rulers.
4. **Cross-judge extract diff.** Run Stage 1 with gpt-judge and opus-judge on the same 9 agreed-pass + 3 P-vs-F cells. Diff the claim sets. This directly measures whether σ_γ will get worse under Rulers — near-identical extracts → σ_γ won't regress; divergence on the tip-thread claim → the structural bias moves into Stage 1 and Rulers is cosmetic.
5. **Short-answer ablation.** On R08-type cells (≤ Q1 length), force Stage 1 to emit ≥ 1 claim even if "absent." Check whether σ_ε is genuinely locked or just biased to fail.

Experiments 1 and 3 are runnable against current artifacts with no new agent calls. Experiment 2 is the single most decisive test of the whole design.

---

## R13 anomaly dive

### Probe text
`"what was the evolution of the adapter-as-compiler concept?"` — NE-1.3, `reference_dt=2026-03-15`. The "evolution" spans roughly Mar 14 evening → Mar 15 early morning (one long authoring session `ses_312659280ffewl5WrvUq6FW7QN` starting 2026-03-14T18:27) plus ~30 hours of follow-on sessions and ~5 git commits (`80acb6c`, `4d3f4c0`, `0195a8b`, `2a9b29d`, `7afd378`, `a982758`). Not a single-cycle probe — it's multi-day, multi-session, with the concept crystallization concentrated in a ~1-hour window.

### One-sentence summary of each agreed-pass answer
- **gpt-agent / pure**: 8-phase timeline naming memory-IDs (`069b6006` → `069b6022` → `069b6052` → `069b613d` → `069b64e9`) and tracking the arc from JSON-blob → hot-field promotion → compiler target → federation → descriptor-first protocol.
- **opus-agent / pure**: 4-phase narrative (JSON blob → known-vs-emergent correction → compiler crystallization → implementation) with approximate timestamps (Mar 14 ~5:42–6:02 PM) and the three-layer stack (raw capture / canonical trace facts / derived learning labels).
- **opus-agent / production**: 6-commit timeline (`80acb6c` → `4d3f4c0` → `0195a8b` → `2a9b29d` → `7afd378` → `a982758`) with verbatim docstring quotes and direct commit-subject quotation.

All three converge on the same conceptual arc (monolithic/JSON-blob → correction about "let structure emerge" scope → adapters-as-compilers / events-as-IR → federation/protocol). Artifacts differ: gpt-agent leans on memory IDs, opus-agent/pure leans on session timestamps, opus-agent/production leans on git commit SHAs. Three independent surface routes to the same claim.

### Filesystem-grep test
Grep-hits on the slice `NE-1.3__R13/` (3,139 JSONL files, 82k lines) for the load-bearing phrases:

| Phrase | File hits | Total occurrences |
|---|---|---|
| `adapter(s)?-as-compiler\|Adapters are COMPILERS\|let structure emerge` (case-insens.) | 50+ files | **195+** |
| `the event is the universal primitive\|events table is the IR\|the adapter is the compiler` | 37 files | **90** |
| `CODE IS GENERATION NOW` | 13 files | **21** |

Every defining slogan in the three answers is a verbatim substring in the slice, repeated dozens-to-hundreds of times across many session files. The single session `ses_312659280ffewl5WrvUq6FW7QN` alone contains 24 hits on the compiler-phrase regex and 12 on the IR-phrase regex. A fresh agent can locate the answer with one `grep -l` against the slice root and read the decisive lines from the top hit. This is not a reconstruction — it's a retrieval.

### Comparison to R13/zero (MEMEX-only, no slice access)
- **opus-agent / zero**: **pass** (judge verdict: strong on all three axes; the answer correctly names `ses_312659280ffewl5WrvUq6FW7QN` as the origin session and reconstructs the paradigm-shift recording at 00:49, i.e. opus-agent's MEMEX already carries the compiler slogan verbatim — the reconstruction is driven by memex content that was itself synthesized from the same heavily-duplicated slice text).
- **gpt-agent / zero**: **partial** (judge: factual-grounding partial; minute-by-minute timestamps slightly off, but the four-phase arc is essentially correct).

So zero does **not** cleanly fail — opus/zero passes, gpt/zero partials. This is weaker evidence than the task brief anticipated; the MEMEX-only condition does not cleanly break the probe. That said: the reason zero also succeeds on opus-agent is that the MEMEX itself is a compressed copy of the same heavily-repeated slogans. Either the agent greps the slice directly or it reads the memex — both routes bypass any reconstruction.

### Judge reasoning pattern
Every pass verdict on R13 cites "Quoted docstrings ('Let structure emerge', 'mechanical extraction functions') appear in multiple session files in the slice", or "the exact user quotes ... paradigm shift observations ... implementation commits ... all verified against session data and git history." The judges explicitly grade this as *grounded in slice* rather than *reconstructed from memory*. That is the definition of a retrieval probe, not a reconstruction probe, under any reasonable taxonomy.

### Verdict: **DEMOTE**

R13 is a retrieval/grep probe dressed up as a narrative-reconstruction probe. The "evolution" is a concept crystallized in one session with a uniquely memorable slogan ("adapter is the compiler", "event is the universal primitive", "CODE IS GENERATION NOW") that was then re-quoted across 195+ lines in 50+ slice files and embedded verbatim in the MEMEX projection. Both architectures and both judges find this easy because there is nothing to reconstruct — the answer is literally in the bytes. It does not exercise memory-reconstruction capability; it exercises filesystem and memex read-through.

Keeping R13 in the agreed-pass anchor double-counts a single trivial probe into the pure-condition column, inflating pure's architectural standing.

### Recomputed architectural ordering on agreed-pass minus R13

Original agreed-pass tally (both agents pooled, n=9): `production=4, zero=1, pure=4`.

R13 contributes: 1 to opus/production, 1 to opus/pure, 1 to gpt/pure → remove 3 cells.

**Revised tally (n=6): `production=3, zero=1, pure=2`**

The ordering flips to **`production > pure > zero`**, which is consistent with the prior working assumption that operational memory (full MEMEX+search) dominates pure search-only, which dominates MEMEX-only. Pure no longer ties production. The n=6 residual is small enough that no strong significance claim survives, but the direction now matches the a-priori expectation instead of contradicting it.

### Follow-through
- Mark R13 as "trivially-retrievable" in `NE_1_3_REAL_ASK_EVAL_SET.yaml` (or equivalent tag field) so it is excluded from architectural claims but retained as a retrieval-floor sanity check.
- Re-audit the remaining 6 agreed-pass cells (R03, R05, R11, R14, R17, R18 approx — need a separate pass) for similar degeneracy; any probe whose key slogan grep-hits ≥ ~50 times in-slice is suspect.
- Update `JUDGE_MINING_SYNTHESIS_20260420.md` footnote from "agreed-pass is 9 cells" to "agreed-pass is 6 cells after R13 demotion (retrieval-degenerate)".

---

## Length × disagreement — mediation analysis

Hypothesis: answer length is a common driver of (a) σ_ε flip rate in opus intra-rater and (b) the gpt-agent vs opus-agent cross-judge binary-κ gap (0.41 → 0.71). If short/hedged answers sit on the useful/fail boundary and long/specific answers commit hard, some of the "judge-stability gap" is upstream of the judge — it's an agent property. Stdlib-only analysis on the 4 canonical 2×2 runs + 3 opus intra-rater judge reps.

### 1. Answer length per agent per condition (chars)

| agent | condition | n | mean | median |
|-------|-----------|---|------|--------|
| gpt-agent  | production | 19 | 5 245 | 4 743 |
| gpt-agent  | zero       | 19 | 5 396 | 3 737 |
| gpt-agent  | pure       | 19 | 6 582 | 4 235 |
| gpt-agent  | **ALL**    | 57 | **5 741** | **4 235** |
| opus-agent | production | 19 | 3 118 | 2 558 |
| opus-agent | zero       | 19 | 4 245 | 2 361 |
| opus-agent | pure       | 19 | 4 335 | 3 280 |
| opus-agent | **ALL**    | 57 | **3 899** | **2 558** |

**Surprise:** opus-agent answers are *shorter* than gpt-agent (3 899 vs 5 741 mean; 2 558 vs 4 235 median). The working assumption in iteration 1's question ("opus produces longer answers by tendency") was wrong for this corpus. Gpt-agent is the verbose one.

### 2. Binary cross-judge agreement by length quartile

Per-agent cells rejoined self-judge vs cross-judge, `invalid` verdicts dropped. `useful = pass∪partial`, `not-useful = fail`.

**gpt-agent** (n=54, overall binary-agree = 0.870; Q1≤2001, Q2≤4442, Q3≤7706 chars):

| quartile | n  | mean_len | binary_agree |
|----------|----|----------|--------------|
| Q1 | 14 | 1 522  | 0.714 |
| Q2 | 14 | 3 316  | 0.857 |
| Q3 | 13 | 6 233  | **1.000** |
| Q4 | 13 | 13 083 | 0.923 |

**opus-agent** (n=57, overall binary-agree = 0.912; Q1≤1902, Q2≤2558, Q3≤4778 chars):

| quartile | n  | mean_len | binary_agree |
|----------|----|----------|--------------|
| Q1 | 15 | 1 373 | 0.933 |
| Q2 | 14 | 2 300 | 0.857 |
| Q3 | 14 | 3 912 | 0.929 |
| Q4 | 14 | 8 192 | 0.929 |

Gpt-agent shows a clear monotonic length→agreement rise (Q1 71% → Q3/Q4 ~95%). Opus-agent is essentially flat at ~86–93% with no length signal. The length effect on cross-judge binary agreement is present in gpt-agent only.

### 3. Opus intra-rater flip rate by length quartile

Flip = any disagreement across 3 opus-judge reps on opus-agent answers (`rep1=final`, `intrarater-rep2`, `intrarater-rep3`). Cells with any `invalid` dropped → n=47, overall flip rate 0.383.

| quartile | n  | mean_len | flip_rate |
|----------|----|----------|-----------|
| Q1 | 12 | 1 446 | 0.500 |
| Q2 | 12 | 2 490 | 0.583 |
| Q3 | 12 | 4 206 | **0.167** |
| Q4 | 11 | 8 690 | 0.273 |

Reproduces iteration 1: short answers flip ~2× more than long ones. The break is between Q2 and Q3 (~3–4 k chars), not a smooth slope.

Logistic regression, P(flip=1) = σ(β₀ + β₁·log(len)), Newton-Raphson, stdlib:
- **β₀ = +2.16, β₁ = −0.33** (log chars)
- Sign: **negative** — longer answers flip less, consistent with the quartile table. Effect size: each e-fold of length lowers log-odds of flip by 0.33 (≈28% odds reduction per e-fold). Single covariate, no CI computed (n=47).

### 4. Crude mediation decomposition

Pool both agents' cross-judge cells, split at pooled median (3 478 chars):
- short_rate (≤median) = 0.839 binary-agree
- long_rate  (>median) = 0.945 binary-agree
- gpt-agent short-share = 0.407 (gpt-agent is mostly in the long bucket)
- opus-agent short-share = 0.596 (opus-agent is mostly in the short bucket)
- Predicted binary-agree rate if length were the only driver:
  - gpt-agent: 0.407·0.839 + 0.593·0.945 = **0.902**
  - opus-agent: 0.596·0.839 + 0.404·0.945 = **0.882**
- **Predicted gap: −0.020** (opus < gpt by length alone)
- **Observed gap: +0.042** (opus − gpt, in overall binary-agree rate)

Length predicts gpt-agent should be *more* cross-judge-stable, not less, because gpt-agent produces the longer answers and long answers agree more. The direction is **opposite** the observed gap. Length does **not** mediate the agent-level κ-binary gap in this corpus. The iteration-1 premise "opus produces longer answers by tendency" is the load-bearing bad assumption — it's false here.

### 5. Condition × length × agreement interaction

| agent | condition | n | mean_len | binary_agree |
|-------|-----------|---|----------|--------------|
| gpt-agent  | production | 17 | 5 446 | 0.941 |
| gpt-agent  | **zero**   | 18 | 5 621 | **0.722** |
| gpt-agent  | pure       | 19 | 6 582 | 0.947 |
| opus-agent | **production** | 19 | 3 118 | 0.895 |
| opus-agent | zero       | 19 | 4 245 | 0.895 |
| opus-agent | pure       | 19 | 4 335 | 0.947 |

gpt-agent/zero (worst cell) is **not** the shortest — it's 5 621 chars, longer than gpt-agent/production (5 446) with 94% agreement. opus-agent/production (worst for opus) **is** the shortest (3 118) but its agreement (89.5%) matches zero. Condition, not length, dominates the within-agent cell ranking. The hypothesis "bad cells = short cells" fails for gpt-agent and is weak for opus-agent.

### Does length explain the judge-stability gap?

**No.** Length explains σ_ε flip rate within opus intra-rater (β₁ < 0, Q1→Q3 flip rate roughly halves) but the crude mediation predicts the **opposite** direction for the cross-agent κ-binary gap, because opus-agent answers are shorter than gpt-agent on this corpus (3 899 vs 5 741 mean). The judge-stability gap is therefore not upstream of the judge via an answer-length channel — some other agent property (commitment style, hedging, specificity independent of verbosity) is the likely driver.

### Caveats

- **n thin**: ~57 cells per 2×2 corner, 47 usable opus intra-rater cells after `invalid` drops. Logistic β₁ not bootstrapped; quartile cells are 11–15 each.
- **Length is a crude proxy**: chars measure volume, not commitment/specificity/hedging, which are the hypothesized mechanisms. A content-feature extractor (named-entity density, numeric-span count, quote count) is the honest next step.
- **Binary collapses information**: partial→useful lumping hides where flips actually live (pass↔partial vs partial↔fail). Iteration 1's all-adjacent-band finding suggests binary is slightly too coarse to capture the full length effect.
- **gpt-agent/zero is the 0.722 outlier** and drives its overall score; the monotonic length trend for gpt-agent holds only because Q1/Q2 rows pool across conditions.

---


## Structural-bias anatomy + s_state operational definition

Iteration 2, task 2. Pulled the full `judge_result` block for the 3 full-band opus=pass/gpt=fail cells from both judge runs. Raw files:

- R03/pure (gpt-agent): `runs/ne13-real-15d-gpt54-final-20260420T071500Z/results.json` (gpt), `runs/ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z/results.json` (opus)
- R05/production (opus-agent): `runs/ne13-real-15d-opus46-final-20260420T071500Z/results.json` (opus), `runs/ne13-real-15d-opusask-gpt54judge-20260420T144210Z/results.json` (gpt)
- R19/zero (opus-agent): same pattern.

### Side-by-side sub-axis scores (reasoning clipped to <=100 char)

| cell | judge | active_thread | state_transition | continuation_value | factual.support |
|---|---|---|---|---|---|
| R03/pure | opus | strong: "CLI/setup/model-resolution as most recent work (commit 853fc78 at 18:49:49)" | strong: "4fddf40 -> bc2673a -> docs -> config/auth -> provider picker -> setup overhaul" | strong: "commit-level specificity, open issue tracking, 'where you left off' frame" | strong: "every commit SHA, message, tech detail verifiable in git anchor" |
| R03/pure | gpt | missed: "active thread NOT CLI/setup; it was synthesis debugging - Azure/Kimi, finalize_memex" | partial: "tracks earlier transition, misses later return to synthesis validation" | partial: "helps recover history but not optimally resume the live problem" | strong: "commit refs and architectural claims backed by local_git_anchor" |
| R05/prod | opus | strong: "10 open threads, federation gap prioritized, observe layer blocked, bugs captured" | partial: "transitions tracked but version wrong - should show v0.4.6 not older marker" | strong: "high restart capability: thread statuses, constraints, next steps, priority" | strong: "vast majority corroborated by session events and memex content" |
| R05/prod | gpt | missed: "misses highest-salience threads - ask timeout #14, filesystem #12; substitutes older" | missed: "fails to reflect v0.4.6 / 286 tests / issues #15/#14/#12/#10/#9/#8/#7" | partial: "research-vector section helps a bit; insufficient to continue live threads" | partial: "support for research vectors; major thread claims not directly supported" |
| R19/zero | opus | strong: "correctly identifies session 3287f523 (Mar 21 PDT eve) - local LLM inference M2 Max" | strong: "Mar 17 discussion -> ambient computing -> model landscape -> Qwen 35B -> M5 Max" | strong: "enough to restart: Qwen 3.5 35B download, M2 vs M5 comparison, library expansion" | strong: "all major claims verified in session JSONL data and subagent outputs" |
| R19/zero | gpt | missed: "wrong thread - local inference/LM Studio vs latest sandbox/replay, Sandbox-rename" | missed: "does not track transition to Mar 21/22 sandbox/replay; treats older theme as current" | missed: "wrong active task -> user following it would restart the wrong investigation" | missed: "Qwen 3.5 35B MoE / 9B / gpt-oss-120b / M5 tok/s formula unsupported by slice" |

### Identified axis of disagreement

Not a single sub-axis - three of the four flip in lockstep on R05 and R19, two of four flip on R03. The consistent locus is `continuity.active_thread_selection` (flips `strong`<->`missed` on all 3 cells, largest magnitude). `state_transition_tracking` flips 3/3, `continuation_value` flips 3/3 at smaller magnitude. `factual_grounding.support` only flips on R05 and R19; on R03 both judges call it `strong`. **The primary disagreement locus is `active_thread_selection`, and factual-grounding gets dragged along when the judges disagree about which evidence surface is canonical for the thread.**

The iteration-1 "tip vs landscape" hypothesis is directionally right but imprecise. Reasoning text shows a **surface-weighting disagreement**, not just a granularity one:

- **gpt-judge: tip = "latest unresolved observation in the freshest surface."** R03 -> 19:39Z `finalize_memex` failure note, not 18:49Z commit. R05 -> open GitHub issues #14/#12/#15. R19 -> sandbox/replay cleanup commit.
- **opus-judge: tip = "latest committed/verifiable artifact + landscape around it."** R03 -> 18:49Z commit. R05 -> accepts landscape completeness even with stale v0.4.6 marker. R19 -> accepts session-level reconstruction.

Both are defensible operationalizations; they differ on **which surface is canonical** and **how freshness is measured** (unresolved state vs closed artifact).

### Probe-prompt ambiguity

All three probes are upstream-ambiguous between "latest tip" and "landscape":

- R03: *"what was I last working on and what's the current status of synthesis modernization?"* - "last working on" implies tip; "current status" admits either reading.
- R05: *"what are all my current open threads, priorities, and unfinished work? include: research vectors (ACE, GEPA, sleep/dream, filesystem), open bugs, hackathon plans, memory system studies, continual learning research"* - explicitly asks for landscape ("all"); gpt-judge still penalizes landscape-complete answers for missing *currently-hot* items within it.
- R19: *"what happened last? what was I working on most recently?"* - unambiguously tip-focused, yet opus-judge passes a different tip than gpt-judge.

R05 is the most diagnostic: the probe literally asks for comprehensive landscape, and gpt-judge still penalizes landscape over tip-currency. gpt-judge's `s_state` prior overrides the prompt.

### Proposed `s_state` operational definition

> `s_state(answer | slice, t)` is adequate iff the answer reconstructs **both** the active-thread tip AND at least one level of landscape context around it, where the tip is defined as *the most recent unresolved work-state in the evidence surface the probe explicitly names, resolved by timestamp across all surfaces when the probe is surface-agnostic*. Tip-currency is a **gating** condition on `pass`; landscape-completeness differentiates `pass` from `partial`.

Decision rules a judge can apply mechanically:

- **Tip rule.** Identify the single most recent (by timestamp) unresolved work-state across `{commits, traces, slice_events, open_issues}`. If the answer names that tip OR a co-temporal sibling (within 6h and same thread), tip-condition passes. Otherwise cap the verdict at `partial` regardless of landscape quality.
- **Landscape rule.** Given tip-condition satisfied, count probe-named dimensions (or top-3 highest-volume threads if unnamed) reconstructed with at least one verifiable anchor. `pass` requires >=ceil(2/3); `partial` otherwise.
- **Surface-preference rule.** Named surface ("synthesis modernization" -> commits+traces; "open threads" -> issues+transcripts) resolves tip on that surface. Surface-agnostic ("what happened last") resolves on freshest wall-clock - ties broken toward the surface with unresolved state, not the one with closed artifacts.

### Verdict check on the 3 cells

- **R03/pure.** Probe names "synthesis modernization" -> surface = commits+traces. Tip = 19:39Z `finalize_memex` failure note (unresolved synthesis). Answer picked 18:49Z CLI/setup. **Tip-condition fails -> cap at `partial` -> `fail` given weak landscape. Matches gpt-judge; opus was wrong to pass.**
- **R05/prod.** Probe is landscape-explicit. Tip = open issue #14 (freshest high-sev unresolved). Answer substituted older threads. **Tip fails -> `partial`. gpt-judge `fail` is harsh but directionally right; opus `pass` overstates.**
- **R19/zero.** Surface-agnostic. Tip candidates = sandbox/replay commit (gpt) vs session 3287f523 local-inference (opus), both within ~24h on different surfaces. Tie-breaker (surface with unresolved state) picks whichever was in-flight at t; current slice does not unambiguously resolve it. **Rule output: ambiguous - needs explicit tie-break anchor the probe does not supply.**

**Local consistency:** rule produces `fail / partial / ambiguous`. It resolves R03 and R05 in the same direction (gpt-judge's) and exposes R19 as under-determined rather than forcing either verdict. Better than either judge's categorical call.

### Implication

The opus=pass/gpt=fail bias is **not 50/50 defensible** once `s_state` is pinned down. gpt-judge is closer to the operational definition on R03 and R05; opus-judge is systematically over-generous on tip-currency when the answer is landscape-rich. This inverts the naive read of the intra-rater finding - opus-judge's higher self-consistency does **not** imply better `s_state` calibration; it means it consistently applies a laxer tip criterion. Next rejudge pass: bake the tip-gate rule into the judge contract and check whether kappa on the P<->F band recovers.

---

## Specificity and hedge as mediators

*Iteration 3 — 2026-04-20. Follow-up to the length-non-mediation finding. Question: does artifact-density (specificity) or probabilistic hedging explain why opus-agent's cross-judge binary stability beats gpt-agent's (kappa_binary 0.71 vs 0.41)? Analysis script: `/tmp/specificity_hedge_mediation.py`.*

### Proxy definitions

- **Specificity density** (hits per 1000 chars) = unique char-spans matching filenames (`\b[\w-]+\.(py|md|json|...)\b`), ISO dates, month-day dates, 7-40 hex commit hashes, numbers >=3 digits, two-word capitalized phrases, CamelCase, snake_case (>=2 segments), or quoted strings. Sub-spans contained in another span are dropped.
- **Hedge density** (hedges per 1000 tokens) = count of whole-word matches against `{may, might, could, possibly, likely, perhaps, seems, appears, suggests, probably, about, roughly, maybe, unclear, potentially, apparently, i think, i believe, not sure, may have, might have, could have}` (case-insensitive).
- Binary agreement per cell = 1 iff same-agent baseline verdict and cross-judge verdict both map to `{pass,partial}` or both to `{fail,invalid}`. gpt-agent cells use the gpt54ask-opusjudge cross; opus-agent cells use the opusask-gpt54judge cross. n = 57 + 57 = 114.

### Per-agent table

| agent | n | mean length | mean spec density | mean hedge density | binary agree rate |
|---|---:|---:|---:|---:|---:|
| gpt-agent | 57 | 5740.9 | 6.16 | 2.83 | 0.825 |
| opus-agent | 57 | 3899.0 | 10.08 | 1.78 | 0.912 |

**Direction:** opus-agent is denser in artifact-like tokens (+64%) and less hedgy (-37%) despite being ~32% shorter. Both proxies align with the intuition for why opus-agent might look more stable to a cross-judge.

### Per-agent x condition

| agent | condition | n | mean length | spec density | hedge density | agree rate |
|---|---|---:|---:|---:|---:|---:|
| gpt | production | 19 | 5244.8 | 6.25 | 2.98 | 0.842 |
| gpt | pure       | 19 | 6582.1 | 5.59 | 2.65 | 0.947 |
| gpt | zero       | 19 | 5395.9 | 6.64 | 2.85 | 0.684 |
| opus | production | 19 | 3117.8 | 11.19 | 1.21 | 0.895 |
| opus | pure       | 19 | 4334.5 | 9.55 | 2.03 | 0.947 |
| opus | zero       | 19 | 4244.6 | 9.49 | 2.09 | 0.895 |

The spec/hedge gap is consistent across all three conditions (opus denser and less hedgy in every cell). The agreement-rate gap is largest on `zero` (0.684 vs 0.895, d=0.21), smallest on `pure` (0.947 vs 0.947, d=0.00).

### Correlation check (all 114 cells)

| pair | Pearson r |
|---|---:|
| spec density vs is_opus | +0.429 |
| hedge density vs is_opus | -0.200 |
| log(length) vs is_opus | -0.195 |
| spec density vs binary agree | -0.031 |
| hedge density vs binary agree | -0.093 |
| log(length) vs binary agree | +0.146 |
| is_opus vs binary agree | +0.130 |

Spec/hedge track agent identity strongly, but neither tracks binary agreement at the cell level.

### Logistic regression (stdlib GD, standardized continuous predictors, L2=1e-3)

| model | intercept | log_len_z | spec_z | hedge_z | is_opus |
|---|---:|---:|---:|---:|---:|
| A: agent only | +1.537 | -- | -- | -- | **+0.785** |
| B: log_len only | +1.922 | +0.379 | -- | -- | -- |
| C: log_len + agent | +1.513 | +0.468 | -- | -- | **+0.992** |
| D: spec only | +1.874 | -- | -0.087 | -- | -- |
| E: hedge only | +1.893 | -- | -- | -0.242 | -- |
| F: log_len + spec + hedge | +1.955 | +0.444 | +0.040 | -0.282 | -- |
| G: full | +1.531 | +0.449 | -0.122 | -0.258 | **+0.998** |

### Mediation verdict

**Neither specificity nor hedge density mediates the agent effect.** Going from model A -> model G, the `is_opus` coefficient moves from +0.785 to +0.998 (it grows by ~27%, it does not shrink). Classical mediation requires the agent coefficient to attenuate toward 0 when the proposed mediator is introduced; the opposite happens here. Spec even flips sign once agent is partialled out (+0.040 -> -0.122), and hedge's standalone effect (-0.242) is only marginally changed by agent (-0.258). The signal that survives is `log(length)` (+0.38 alone, stable at ~+0.45 in the multivariate models) and an agent-identity residual that none of the three proxies captures.

One-sentence verdict: opus-agent really is denser in artifacts and less hedgy, but those surface features do not explain its cross-judge stability advantage -- the agent-identity effect is unmediated by any of {length, specificity, hedge} individually or jointly.

### Caveats

- Proxy lexicons are crude. "specificity" conflates code-like tokens with dates and proper nouns; "hedge" list is small and English-only and includes `about` which collides with non-hedge usages ("about 40 commits").
- n = 114 is thin; standard errors not bootstrapped. The standalone hedge coefficient (-0.24) is the strongest non-agent effect but not demonstrably non-zero at this sample size.
- Binary agreement collapses the pass<->partial band that iteration 1 showed is where most disagreement lives -- mediators of the ordinal gap may differ from mediators of the binary gap.
- The unmediated `is_opus` effect is consistent with iteration 2's structural-bias finding: cross-judge stability is driven by *which surface the agent anchors on* (tip vs landscape, which is a structural property of the agent's retrieval plan), not by per-answer stylistic features.

---

## Retroactive s_state rule application

Iteration-3 task. Apply the iteration-2 tip-currency gate retroactively to every (probe, condition) pair-cell across the 2x2 cross using only the existing judge prose -- no new LLM calls. Proxy map: `continuity.active_thread_selection.score` -> tip_hit (strong=1.0, partial=0.5, missed=0.0); `continuity.salience_relevance.score` -> landscape_hit same scale. Major-mismatch demotion flag fires iff `coherence.contradiction_handling` OR `coherence.artifact_routing_consistency` is `missed`. Rule: tip>=1.0 AND land>=0.5 -> pass; tip>=1.0 AND land<0.5 -> partial; tip=0.5 -> partial (capped); tip=0 -> partial, demoted to fail only if major-mismatch fires.

Script: `research/n1-memory-lab/scratch/retro_sstate_rule_20260420.py`.

### 1. Usable pair-cells

Of the 114 nominal cells (57 x 2 agents), 3 on gpt-agent had `verdict="invalid"` from the opus judge (JSON-parse failure; already excluded in the iteration-1 analysis) and drop out for lack of a usable continuity block. **111 pair-cells rejudged** (gpt-agent=54, opus-agent=57). Of those, 56 were originally 3-level mismatched.

### 2. Cross-pair kappa before vs after

| surface | kappa (orig) | kappa (rejudge) | delta |
|---|---:|---:|---:|
| 3-level (pass/partial/fail) | +0.216 | +0.233 | +0.017 |
| binary (useful / not-useful) | +0.592 | +0.422 | **-0.171** |

Exact-match rate: 3-level 49.5% -> 53.2% (+3.7 pp); binary 89.2% -> 84.7% (-4.5 pp). The tip gate buys ~2 kappa points on the 3-level surface and actively *hurts* binary agreement -- it creates new partial<->fail disagreements by demoting tip-missed cells that both judges previously agreed were `partial` on the useful band.

### 3. Directional shift on the 56 originally-mismatched cells

| shift | n | % |
|---|---:|---:|
| rejudged agrees with gpt-original | 1 | 1.8% |
| rejudged agrees with opus-original | 27 | 48.2% |
| rejudged agrees with neither original | 0 | 0.0% |
| rejudged still disagrees between judges | 28 | 50.0% |

The rule moves mass toward **opus's original verdict**, not gpt's -- opposite the iteration-2 P<->F anatomy which argued gpt-judge was closer to the operational `s_state` definition. Mechanism: opus-judge rates `active_thread_selection=strong` far more often (opus rejudged pass=79 vs gpt rejudged pass=46, ~70% higher pass rate). So when the rule says "tip=strong -> pass" it inherits opus's lenient tip prior wholesale. The rule is only as disciplined as its per-judge tip proxy; since the two judges already disagree on what counts as a strong `active_thread_selection`, the rule cannot manufacture agreement -- it just ratifies whichever judge was more lenient. Per-agent: on gpt-agent (n=28) 1 toward-gpt / 17 toward-opus / 10 still-split; on opus-agent (n=28) 0 toward-gpt / 10 toward-opus / 18 still-split.

### 4. Rejudged verdict distribution

Pooled across both judges x 111 cells = 222 verdicts: **pass 125 (56.3%), partial 64 (28.8%), fail 33 (14.9%)**. Per-judge: gpt-judge rejudged {46 pass, 40 partial, 25 fail}; opus-judge rejudged {79 pass, 24 partial, 8 fail}. Opus's rejudged pass rate is 1.7x gpt's -- same structural-bias asymmetry the iteration-1 raw verdict surface shows, untouched by the rule.

### 5. Rule-ambiguous cells (both judges tip=partial)

**7 cells.** These are exactly the cases the rule cannot resolve, because both judges flagged `active_thread_selection=partial` and the rule's tip=0.5 branch caps everything at `partial`:

- gpt-agent: R09/production, R11/zero, R12/zero, R16/pure
- opus-agent: R09/pure, R18/pure, R18/zero

In 6 of 7 the rejudged verdict is `partial/partial` (agreed) -- but the rule "works" here only by erasing information: original verdicts on these cells spanned {fail, partial} and the rule collapses both sides to partial without touching the underlying disagreement about whether the answer was useful at all. This is rule imprecision, not resolution.

### 6. Agreed-pass anchor check

The pre-R13 agreed-pass anchor (9 cells) survives **9/9** under the rule -- both judges' rejudged verdicts remain pass on every cell, with tip=1.0 and land=1.0 on both sides. The post-R13 anchor (6 cells) survives **6/6**. The rule does not destroy genuine agreement where it already existed; it only moves mass on the pass<->partial and partial<->fail boundaries.

### 7. Honest answer

**No -- a principled s_state rule does not resolve the structural bias.** It lifts 3-level kappa by a negligible +0.017, degrades binary kappa by -0.171, and simply re-expresses the opus-lenient / gpt-strict split through the `active_thread_selection` sub-axis instead of the overall verdict; the underlying disagreement about what counts as "the tip" lives one level deeper than any rule wired to per-judge rubric scores can reach.

---

## Retrieval-degeneracy audit of agreed-pass anchors

Question: R13 was demoted as retrieval-degenerate (key slogans grep-hit 195+ in slice). Apply the same test to the other 6 unique agreed-pass cells to separate genuine memory-reconstruction from retrieval-from-slice.

Method per cell: pull `answer_text` from the run's `results.json`; run `grep -r -F -c` against the cell's `slices/NE-1.3__<probe_id>/` root for 5+ load-bearing phrases (named artifacts, commit SHAs, specific numbers, distinctive quoted strings); sum occurrences. Threshold: any phrase >50 occurrences -> DEGENERATE; 10-50 -> RETRIEVAL-ASSISTED; <10 or thin distribution -> RECONSTRUCTION. Slice dirs confirmed on disk at `/Users/saxenauts/.syke-lab/<runset>/slices/NE-1.3__<probe_id>/`.

### Per-cell probed phrases and counts

| cell | agent | load-bearing phrases (occurrences in slice) | max | verdict |
|---|---|---|---:|---|
| R01 / pure | gpt | `BRAINSTORM.md`=82, `FOUNDATIONS.md`=9, `test-and-monitor.sh`=189, `286 passed`=24, `LiteLLM`=241, `Azure`=213 | 241 | **DEGENERATE** |
| R04 / production | gpt | `MEMEX_EVOLUTION.md`=566, `syke ask`=1012, `GEPA`=647, `Mastra`=457, `roadmap-internal.md`=142, `issue #14`=48 | 1012 | **DEGENERATE** |
| R12 / production | gpt | `Real-time Distribution`=189, `PreToolUse`=250, `external_id`=998, `Observe Phase 3`=8, `hook-based capture`=13 | 998 | **DEGENERATE** |
| R15 / zero | gpt | `546 passed`=22, `128,902`=30, `3,736`=46, `5,173`=16, `SYKE_PROVIDER=zai`=18, `1,320`=15, `1,597`=17 | 46 | **ASSISTED (tool-contaminated, see below)** |
| R02 / production | opus | `63cc4a5`=28, `d719f3f`=24, `UserProfile`=299, `LiteLLM`=241, `ANTHROPIC_BASE_URL`=136, `CONFIG_REFERENCE.md`=81, `293 tests`=37 | 299 | **DEGENERATE** |
| R11 / pure | opus | `SKILL.md`=1497, `watchdog`=652, `OBSERVE-PRINCIPLES.md`=317, `Sense Intelligence`=150, `Fluid Intelligence`=107, `hook listener`=80, `Adapters are compilers`=54, `observe-rt`=49 | 1497 | **DEGENERATE** |

### R15 / zero -- special case: the `zero` condition is not a memory-only control

The `zero` mode is defined as "no MEMEX tools available, search-only." The R15/zero answer names very specific figures (`546 passed, 12 skipped`, `128,902 total events`, etc.). I checked two things:

1. **The MEMEX projection injected into the ask prompt** (`evidence/zero/R15/ask_prompt.txt`, 1,389 chars inside `<memex>`). Zero hits for any of `546 passed`, `128,902`, `120,675`, `3,736`, `1,320`, `5,173`, `SYKE_PROVIDER=zai`, `ADAPTERS_DIR`, `fresh scratch`. The MEMEX is clean -- generic bootstrap memories only, no leakage of the answer's load-bearing numbers.
2. **The `ask_trace.json` tool-call log.** The zero-mode agent issued 11 tool calls, of which 3 (#5, #6, #10) are direct `rg` greps against `/Users/saxenauts/.syke-lab/.../slices/NE-1.3__R15/harnesses/**/*.jsonl` -- i.e. the agent bypassed the MEMEX-only constraint by reading the slice via bash. All load-bearing numbers sit in 2 opencode/claude-code session files (`ses_307e0d6dbffeqa6wtRVOVHHDaR.jsonl`, `ses_3116df434ffeBN2y4vnoSNQmVL.jsonl`) that the agent grepped.

So R15/zero is **not a MEMEX contamination**. It is a **tool-policy contamination**: the "zero" condition as executed did not isolate the agent from the slice filesystem, only from the `syke` CLI. In-slice phrase counts for R15 are below the 50-hit degenerate threshold, but the pass verdict is still retrieval-assisted rather than reconstructive, and it does not exercise memory-only behavior.

### Ranking by degeneracy (worst -> least)

1. R11/pure (opus) -- max phrase 1497
2. R04/production (gpt) -- max 1012
3. R12/production (gpt) -- max 998
4. R02/production (opus) -- max 299
5. R01/pure (gpt) -- max 241
6. R15/zero (gpt) -- max 46, plus tool-policy bypass

### Revised agreed-pass tally after dropping DEGENERATE + tool-contaminated

Pre-audit agreed-pass count (iteration 1): `production=4, zero=1, pure=4`, n=9.
After R13 demotion (iteration 2): `production=3, zero=1, pure=2`, n=6.
After this audit: drop R01/pure, R04/prod, R12/prod, R15/zero, R02/prod, R11/pure.

**Post-audit agreed-pass: n=0.** All 9 cells where both judges said pass on the same answer are either slice-retrievable (phrases copy-pastable from >50 grep-hits in slice) or reached via a tool-policy bypass of the condition's intended isolation. Per-condition: `production=0, zero=0, pure=0`.

### Is `zero` still a clean memory-only control?

**No, not systematically.** The MEMEX projection itself is clean on R15 -- generic bootstrap content, zero hits for the answer's load-bearing numbers. The contamination is not in the MEMEX; it is in the agent's permitted tool surface. In `zero` mode the agent retains bash+rg+read and used them to read the slice directly. Any probe whose answer is grep-reachable from the slice is reachable in `zero` mode too. This is a condition-definition leak, not a projection leak: "MEMEX-only" as implemented means "MEMEX injected into system prompt" and does not remove filesystem access. Until the `zero` condition is re-run with a read sandbox that blocks `slices/**`, all `zero` passes on retrievable probes are alternate-retrieval-route passes, not memory-only passes.

### Honest one-sentence read

At n=0 surviving agreed-pass cells, the 2x2 judge cross does **not** yield any architecture-level claim about `production` vs `pure` vs `zero` on this corpus; every cell where both judges independently said pass is explainable by direct slice retrieval (either by phrase density or by tool-call bypass), and the apparent `production >= pure > zero` ordering from iteration 1 is an artifact of which probes happen to have their answers duplicated heavily in the slice, not of architectural capability.

---

## Code-gate D_t replay on 285 verdicts

*Iteration 3 -- 2026-04-20. Stdlib-only replay of `d_time` / `d_artifact` / `d_committed` as deterministic checks over the 4 canonical 2x2 runs (228 verdict cells; the 285 figure includes the 3 opus intra-rater judge replays which share the same answer_text and are not re-graded here). Codegate rule: if any `d_*` returns FAIL, verdict becomes `fail`; otherwise keep LLM verdict. Reproducer: `research/n1-memory-lab/scratch/code_gate_dt_replay_20260420.py`; cell-level dump: `scratch/code_gate_dt_replay_20260420.json`.*

### Implementation notes

- **d_time**: regex `\b(20\d{2})[-/](\d{2})[-/](\d{2})\b` over `answer_text`; any parsed date strictly greater than `reference_dt` -> FAIL.
- **d_artifact**: top-5 most-frequent distinctive tokens in `answer_text` from {file-path regex `\b[\w./\-]+\.(py|md|ts|tsx|jsonl?|yaml|yml|sh|html|css|toml|cfg)\b`, issue regex `#\d{1,5}`}. Stopword list drops `readme.md`, `config.json`, `results.json`, etc. Each token must appear (substring, lowercase) in the slice blob or in a file path within the slice tree. Basename fallback for paths. **Git-SHA-looking tokens are intentionally routed to `d_committed`, not `d_artifact`** -- the slice is a harness/adapter subset and does not mirror the git tree, so substring-matching SHAs against slice content would be unsound.
- **d_committed**: only fires when the answer frames a hex-7-40 token as a git artifact (nearby context word `commit|sha|ref|git|revision|merge` within 80 chars). Otherwise NA -- avoids false positives on memex/memory-ID hex tokens like `069b20b6`. Check: each framed SHA prefix must match some commit's SHA prefix in `local_git_anchor.json`.
- **Slice resolution**: `cell['artifacts']['slice_dir']` points at `~/.syke-lab/<run>/slices/NE-1.3__R<probe>/` and exists for all 228 cells (slice is per-probe, shared across conditions via symlink from `runs/<run>/evidence/<cond>/<probe>/slice`). No path-skew or missing slices. Slice blob per probe is ~350 MB (JSONL harness traces); loaded once per probe, cached across conditions and judges.
- **Git anchor**: `runs/<run>/evidence/<cond>/<probe>/local_git_anchor.json` present for all 228 cells. 182-200 commits spanning ~Feb 23 -> `reference_dt`+23:59:59.

**Resolvable N = 228/228** (100% slice + anchor + ref_dt coverage on the 4 canonical runs).

### Codegate flip counts per run

| run | axis FAIL (d_time / d_artifact / d_committed) | total flipped | pass->fail | partial->fail | invalid->fail |
|---|---|---:|---:|---:|---:|
| opus-agent x opus-judge | 1 / 2 / 2 | 3 | 2 | 1 | 0 |
| opus-agent x gpt-judge  | 1 / 2 / 2 | 2 | 1 | 1 | 0 |
| gpt-agent x gpt-judge   | 0 / 3 / 1 | 3 | 0 | 3 | 0 |
| gpt-agent x opus-judge  | 0 / 3 / 1 | 4 | 3 | 1 | 0 |
| **all 4 runs pooled**   |           | **12** | **6** | **6** | **0** |

12 / 228 = 5.3% of cells flip verdict under the codegate rule. All flips go toward `fail` (no rule can raise a verdict). `d_committed` is the sharpest gate: it independently identifies 3 distinct cells where agents cite SHAs absent from the anchor. Note per-agent parity: opus-agent produces the same fail pattern under both judges (same answer_text), and same for gpt-agent -- as expected for a deterministic gate keyed on the answer.

### Unique failing cells (pooled across judges, deduped by (agent, probe, condition))

| agent | probe | condition | axis | detail |
|---|---|---|---|---|
| opus | R01 | zero | d_artifact | cites `REFERENCE_TIME.md`, `PSYCHE.md` (absent from slice surface; may exist in repo root outside harness slice) |
| opus | R05 | production | d_committed | cites `508b4e1` as commit; not in anchor (182 commits Feb 23 -> Mar 13) |
| opus | R06 | zero | d_time | answer contains `2026-04-16`; ref_dt=2026-03-13 -> 34-day future leak |
| opus | R13 | production | d_committed | cites `80acb6c, 4d3f4c0, 0195a8b, 2a9b29d, 7afd378, a982758` as commits; **zero of six in the 200-commit anchor** |
| opus | R18 | pure | d_artifact | cites `REFERENCE_TIME.md` |
| gpt  | R02 | production | d_committed | cites `7eb35c8` as commit; not in anchor |
| gpt  | R08 | zero | d_artifact | cites `REFERENCE_TIME.md`, `PSYCHE.md` |
| gpt  | R16 | zero | d_artifact | cites `db5cb6db...jsonl` (stylized ellipsis shorthand; actual UUID file is in slice -- this is a codegate false-positive from regex) |
| gpt  | R18 | pure | d_artifact | cites `memex/vNNN.md` (placeholder "NNN", not a real path -- judge tolerated this as rhetorical) |

### Does codegate flip any AGREED-PASS cell?

**Yes: 1 of 9 agreed-pass cells falls under codegate -- R13/production (opus-agent).** The opus-4.6 agent cited six distinct commit SHAs (`80acb6c -> 4d3f4c0 -> 0195a8b -> 2a9b29d -> 7afd378 -> a982758`) as the evolution of the adapter-as-compiler story. None of the six appear in the 200-commit `local_git_anchor.json` that covers Feb 23 -> Mar 15. Both gpt-judge and opus-judge graded this cell `pass` based on the plausibility of the narrative and verbatim docstring quotes; neither caught that the SHA backbone of the answer is fabricated. That is exactly the grounded contradiction the iteration-2 note predicted code gates would surface.

Iteration-2's "R13 is retrieval-degenerate" finding is strengthened, not undermined: the *slogan-level* text (`adapters are compilers`, `let structure emerge`) is copy-pastable from the slice and the judges latched onto that; the *commit-SHA* spine the agent uses to date-stamp the narrative is an invented scaffolding the judges waved through. This is a second independent mode of R13 failure on top of retrieval-leak.

Surviving agreed-pass after codegate: **8 of 9** (the 1 demotion is R13/production-opus). R13/pure survives both on gpt-agent and opus-agent; those answers cite slogans and session-IDs (not git SHAs) and pass the codegate trivially -- consistent with iteration-2's read that R13 is answerable by phrase retrieval.

### Does codegate resolve the 3 P<->F structural-bias cells?

Partially. Summary:

| cell | LLM (judgeA / judgeB) | CG (judgeA / judgeB) | codegate resolution |
|---|---|---|---|
| R03/pure (gpt-agent) | fail / pass | fail / pass | **no change** -- `d_committed=NA`, `d_artifact=NA`, `d_time=PASS`. Codegate has nothing to say. |
| R05/production (opus-agent) | pass / fail | fail / fail | **resolves to fail agreement** -- the opus-pass verdict is overturned; both judges now agree on fail because the answer cites `508b4e1` as a commit and that SHA is absent from the anchor. Codegate surfaces a grounded contradiction opus-judge missed. |
| R19/zero (opus-agent) | pass / fail | pass / fail | **no change** -- all three gates NA (no files, no SHAs, no date leak). The disagreement is `s_state` (tip vs landscape), which codegate by design leaves to the LLM. |

**1 of 3 structural-bias cells resolves** (R05/production). That is the one where gpt-judge was calling fail on "misses the hot threads" grounds while opus-judge called pass on "comprehensive reconstruction"; the codegate reveals a *third* grounded contradiction (fake SHA) that both had overlooked, and it happens to land in gpt-judge's direction. The other two cells remain semantic disagreements outside the code-gate surface.

### Cross-judge kappa (3-level) before / after

| agent-side | LLM n / exact / kappa | CG n / exact / kappa |
|---|---|---|
| gpt-agent   | 54 / 48.1% / **0.151** | 54 / 55.6% / **0.298** |
| opus-agent  | 57 / 50.9% / **0.270** | 57 / 52.6% / **0.307** |

Kappa rises on both sides: gpt-agent +0.147 (nearly doubles), opus-agent +0.037 (marginal). The asymmetry is informative -- the gpt-agent gain comes from the codegate's hard-fails overriding the judges' partial/pass disagreements into agreement-on-fail, while opus-agent gains little because opus-agent's grounded contradictions (R05, R13) affect cells where both judges were already mostly concordant. Neither run reaches the opus intra-rater ceiling (kappa ~0.65) -- codegate tightens the ground-truth floor but does not close the semantic (`s_state`) gap that drives the remaining disagreement.

### Caveats and honest noise sources

- `REFERENCE_TIME.md`, `PSYCHE.md`, `adapters/codex.md` are cited by multiple agents but are **outside the slice surface** (they live in the repo root / `memory-research/` scope). Flagging them as d_artifact FAIL is technically correct ("not in E_t as constructed") but may be a slice-scope vs repo-scope boundary issue rather than a hallucination. Two of the five `d_artifact` fails are of this kind.
- `db5cb6db...jsonl` (gpt/R16) and `memex/vNNN.md` (gpt/R18) are rhetorical shorthand (ellipsis, placeholder) that regex-matches as filenames but are not actually fabricated references. Both are codegate false-positives from a lenient file regex.
- `d_committed` depends on anchor completeness. The R05/production `508b4e1` and R02/production `7eb35c8` cases could in principle be real commits that fell outside the anchor's 200-commit window -- but both anchors reach back ~3 weeks pre-ref_dt, well beyond any plausible operative-thread horizon, so the likelihood of "real but missing" is low. R13/production's 6-of-6 miss is unambiguous.
- Per-cell granularity is preserved in `scratch/code_gate_dt_replay_20260420.json`; every FAIL cell's token list is auditable.

### One-sentence honest read

Code gates do real work -- they catch one fabricated-SHA cell that both LLM judges agreed was `pass`, resolve one of the three P<->F structural-bias disagreements in gpt-judge's favor, and nearly double cross-judge kappa on gpt-agent answers -- but the remaining cross-judge disagreement is concentrated where the codegate has nothing to say (`s_state` tip-vs-landscape, NA on `d_artifact`/`d_committed`), so codegates move the noise floor without closing the semantic gap.

---

## Iteration 3 consolidation

### The packet is more compromised than we thought

Three independent audits converge on one conclusion: **the existing 2×2 packet cannot support any architectural claim.** Each failure mode is distinct but they stack:

1. **Retrieval-degeneracy in pure**: 5 of 6 non-R13 agreed-pass cells have load-bearing phrases appearing 241–1497× in their slice. The answers are not reconstructed from memory — they are compressed quotations. The slice file list *is* the answer key. Pure "wins" because pure has the filesystem.
2. **Tool-policy leakage in zero**: R15/zero's agent ran `rg` 3 times against the slice directory. Zero was supposed to be MEMEX-only (no filesystem). It isn't. This is a condition-definition leak (tool surface), not a MEMEX projection leak. Probably applies to more cells than just R15.
3. **Fabrication in production**: R13/production-opus cited six commit SHAs, **zero** present in `local_git_anchor.json`. Both LLM judges passed it. Code-gate `d_committed` catches it. If this is representative, the "production wins" side is partly inflated by confabulated grounding that the LLM judges accept.

All three defects touch different conditions. `pure` eats its slice. `zero` isn't `zero`. `production` confabulates grounding.

### What survives

- **state_transition_tracking is the one load-bearing axis** (both judges, R² ≈ 0.73 opus / 0.61 gpt alone).
- **Code gates work on the parts they can reach**: d_time (date leakage), d_artifact (substring-in-slice), d_committed (anchor match via hex-7-40 regex). Cross-judge κ on gpt-agent doubles under code-gate (0.151 → 0.298). 1 of 3 P↔F structural disagreements resolves.
- **The residual `s_state` disagreement is not in any measurable axis.** It lives inside judges' *interpretation* of `active_thread_selection` — opus rewards landscape+committed, gpt demands tip+unresolved. Neither a rubric reshuffle nor a per-judge proxy rule fixes this, because both proxies inherit the disagreement.

### Design implications (for future runs, not this session)

1. **Move fabrication detection into code.** `d_time`, `d_artifact`, and `d_committed` should fire BEFORE the LLM judge sees the cell — as hard preflight gates. If the answer cites a SHA not in the anchor, the verdict is FAIL; the LLM judge doesn't get a vote. This cheaply removes ~5% of verdicts from LLM-judged space.
2. **Tighten the `zero` condition.** Remove `rg`, `grep`, `find`, `cat`, `ls` from the agent's tool surface in zero mode. Force MEMEX-only. Audit R01–R19 for existing zero-condition slice reads.
3. **A judge-independent tip anchor is the only thing that can resolve s_state disagreement.** Candidate: derive at judge-time an `unresolved_state_inventory.json` from the slice — open issues, in-flight commits, latest-wall-clock thread per surface — and hand it to both judges. Then `s_state` becomes "did the answer name the item at the top of the inventory" — testable, not opinion.
4. **Retire retrieval-degenerate probes.** R13 is the worst offender but others may also be. Run a systematic grep-density check on all 24 NE-1.3 probes before the next benchmark; anything with a load-bearing phrase >50× in its slice gets flagged as `grep-degenerate` and is excluded from architectural claims (or kept as a retrieval baseline).

### Iteration 4 questions (emergent)

1. **Tool-policy leakage audit**: how many zero-condition cells show the agent running `rg / grep / find / cat / ls` against the slice? Systemic or local?
2. **Fabrication density per (agent × condition)**: of the 12 code-gate flips, what's the distribution? Does one agent confabulate more? One condition?
3. **Judge-independent tip-anchor schema**: design the `unresolved_state_inventory.json` schema and check which of the 19 probes it would resolve.
4. **σ_ε × fabrication correlation**: are the 19 intra-rater-flipped cells the same cells the codegate flagged? If yes, σ_ε is partly a fabrication-detection signal, not rubric noise.

---

## Judge-independent tip-anchor schema

*Iteration 4 -- 2026-04-20. Design-only. No LLM calls, no re-judge. Goal: materialize a deterministic per-cell artifact that pins the `s_state` tip so both judges reference the same ground truth instead of importing private priors through `active_thread_selection`.*

### Schema (pseudo-JSON)

```jsonc
{
  "reference_dt": "2026-03-15T23:59:59Z",
  "probe_id": "R13",
  "surfaces": {
    "<surface_name>": {                      // codex | claude-code | opencode | git | issues | syke-db | memex
      "latest_event": {
        "kind": "commit|msg|tool_call|issue_edit|memex_write",
        "timestamp": "ISO-8601",
        "summary": "<=120 char",
        "artifact_ref": "sha|path#Lx|issue#N|session_id"
      },
      "open_items": [                        // not closed/committed/resolved at t
        {"kind": "...", "opened_at": "...", "last_touched": "...",
         "artifact_ref": "...", "status": "open|wip|blocked|draft"}
      ],
      "in_flight_artifacts": [               // uncommitted files, draft PRs, WIP branches
        {"kind": "uncommitted_file|draft_pr|wip_branch", "path_or_ref": "...",
         "last_touched": "..."}
      ]
    }
  },
  "cross_surface_threads": [
    {"thread_id": "synthesis-modernization",
     "surfaces": ["git","claude-code","issues"],
     "last_touch": "2026-03-11T19:39Z",
     "status": "unresolved",
     "mentions_last_24h": 14}
  ],
  "global_tip": {
    "surface": "claude-code",
    "event_ref": "ses_...#L3892",
    "timestamp": "2026-03-11T19:39Z",
    "unresolved": true,
    "tie_breaker_applied": "max(last_touched) -> max(mentions_last_24h) -> surface_priority[git>issues>claude-code>opencode>memex]"
  }
}
```

Construction is mechanical: walk `slice_dir/` JSONL, `local_git_anchor.json`, slice-embedded `issues/*.json`, `memex/*.md` frontmatter, union-sort by timestamp, filter `closed/committed/resolved=false`, rank.

### Per-probe feasibility (R01..R19)

| probe | prompt summary | tip/landscape | inventory resolves? | note |
|---|---|---|---|---|
| R01 | "current state, what's active, latest" | both | yes | surface-agnostic; global_tip direct |
| R02 | "work yesterday+today, exhaustive" | landscape | partial | needs date-window, not tip; inventory lists items in range |
| R03 | "last working on + synthesis-modernization status" | both | yes | surface=git+traces named; tip = 19:39Z finalize_memex |
| R04 | "work log today PST entire day" | landscape | partial | date-window, not tip |
| R05 | "all open threads, priorities, unfinished work (+list)" | landscape | yes | open_items per surface + cross_surface_threads |
| R06 | "last working on in syke, left to do, recent decisions" | both | yes | global_tip + open_items |
| R07 | "threads yesterday + map today/yesterday" | landscape | partial | date-window |
| R08 | "where are we now" | tip | yes | global_tip is exactly this |
| R09 | "updated thread map now" | landscape | yes | cross_surface_threads at t |
| R10 | "memory tools landscape study: what did we learn" | neither | no | historical recall, not operative-state |
| R11 | "full vision for Observe" | neither | no | aspirational/design recall |
| R12 | "next steps for Observe after Phase 2" | tip | maybe | depends if "next steps" is in memex open_items |
| R13 | "evolution of adapter-as-compiler concept" | neither | no | historical narrative |
| R14 | "what happened in last session" | tip | yes | global_tip = latest session close |
| R15 | "get back to previous observe-layer testing thread" | tip | yes | open_items filter kind=test-thread |
| R16 | "yesterday's work (topic-scoped)" | landscape | partial | date+topic window |
| R17 | "last one week, all platforms, all sessions" | landscape | partial | 7-day window, not tip |
| R18 | "sandbox+replay harness design, dataset, date-range" | neither | no | design-doc recall |
| R19 | "what happened last, working on most recently" | tip | yes | global_tip direct |

**Tie risk:** R01, R08, R19 are surface-agnostic; inventory construction must apply `surface_priority` tie-break when `last_touched` values fall within the 6h co-temporal window. That's mechanical (fixed priority list) but editorial -- the priority ordering is a design choice baked into the schema, not derived from the slice.

### Prediction on the 3 P<->F cells

- **R05/production (opus-agent).** Already resolved to `fail` by `d_committed` (fabricated `508b4e1`). Inventory is redundant but would confirm via `open_items.issues[#14,#12,#15]` absent from answer -> tip-miss -> `fail`. **Resolves.**
- **R03/pure (gpt-agent).** Tip under inventory = 19:39Z `finalize_memex` failure (unresolved on claude-code + git surfaces); answer picked 18:49Z closed commit. Global_tip unambiguous if surface_priority[git>...] ties to the unresolved-state filter. **Resolves to fail.**
- **R19/zero (opus-agent).** Two candidates within 24h on different surfaces (sandbox/replay commit vs session 3287f523 local-inference). Tie-breaker = `unresolved=true` -> sandbox/replay (committed but thread open) wins over closed local-inference session. **Resolves to fail** IF the tie-breaker is codified; **remains ambiguous** if the inventory records both as "unresolved" equally.

Expected κ impact: all 3 P<->F cells move to fail-agreement -> +3 to agreed-fail count on the 57-cell opus-agent band. Cross-judge binary κ on opus-agent rises from **0.71 -> ~0.82** (rough estimate; iteration-1 P<->F cells are the dominant remaining disagreement source). Cross-judge 3-level κ likely closes ~40-50% of the gap to the intra-rater ceiling (0.65), landing around **0.45-0.50** pooled across both agent-sides -- materially better than codegate's 0.30/0.31.

### Cost of construction (one cell)

| field | source | derivable? |
|---|---|---|
| `surfaces.git.latest_event` | `local_git_anchor.json` | yes, mechanical |
| `surfaces.git.open_items` | anchor diff vs HEAD + uncommitted-file scan | yes |
| `surfaces.claude-code.latest_event` | slice JSONL last tool_result timestamp | yes |
| `surfaces.claude-code.open_items` | slice events with no closing `tool_result` at t | yes (heuristic on pending assistant turns) |
| `surfaces.issues.open_items` | slice-embedded `issues/*.json` if present | yes when present; gap otherwise |
| `surfaces.memex.latest_event` | memex frontmatter + write-time | yes |
| `cross_surface_threads` | thread-id tagging via commit-msg regex + session-title match | **heuristic**; LLM-free but lossy |
| `global_tip` | argmax(last_touched) + surface_priority + unresolved filter | yes, deterministic once rules fixed |
| `mentions_last_24h` | token-count on thread-id across surfaces | yes |

**LLM-requiring fields:** none, if thread-identity is accepted as "commit-msg regex cluster" quality. If we require semantic thread clustering (e.g., "Observe Phase 2" spans commits with no shared token), an LLM pass is needed upstream at slice-build time, not judge-time.

**Gap:** the current slice format has `session JSONL + git anchor + memex` but **no explicit issues snapshot**. 3 of 19 probes (R05, R06, R09) hinge on open-issues; without an issues export at `reference_dt`, those surfaces default empty and the inventory under-counts.

### One-sentence honest read

Tractable for NE-1.3 at the 60-70% level with the current slice format -- `git`, `claude-code`, `memex` surfaces are mechanically extractable and handle 13/19 probes cleanly -- but full coverage (especially R05-class issue-centric landscape probes and the 3 surface-agnostic tie-prone probes R01/R08/R19) requires extending the slice to include an `issues_snapshot.json` and committing to an explicit surface-priority ordering before the rejudge run, which is a slice-format extension, not a new slice.

---


## Fabrication density per (agent × condition)

*Derived from `scratch/code_gate_dt_replay_20260420.json` — 228 cells (4 runs × 57). Each cell contributes up to 2 agent observations (same agent, two judges); so per-agent fail counts below count judge-collapsed cell-events.*

### Cross-tab A: codegate FAILs by reason axis × (agent × condition)

| agent | condition | n_cells | d_time FAIL | d_artifact FAIL | d_committed FAIL | any-axis FAIL cells |
|---|---|---:|---:|---:|---:|---:|
| opus | zero | 38 | 2 | 2 | 0 | 4 |
| opus | pure | 38 | 0 | 2 | 0 | 2 |
| opus | production | 38 | 0 | 0 | 4 | 4 |
| gpt | zero | 38 | 0 | 4 | 0 | 4 |
| gpt | pure | 38 | 0 | 2 | 0 | 2 |
| gpt | production | 38 | 0 | 0 | 2 | 2 |

### Cross-tab B: LLM judge let-throughs later caught by code gate

Cells where `llm_verdict ∈ {pass, partial}` but `codegate_verdict = fail`:

| judge | agent | LLM-good cells | codegate-caught | rate |
|---|---|---:|---:|---:|
| opus | opus | 49 | 3 | 0.061 |
| opus | gpt | 51 | 4 | 0.078 |
| gpt | opus | 44 | 2 | 0.045 |
| gpt | gpt | 47 | 3 | 0.064 |

### SHA fabrication (d_committed FAIL)

| agent | cond | probe | judge | llm_verdict | d_committed_note |
|---|---|---|---|---|---|
| opus | production | R05 | opus | pass | 1/1 shas not in anchor: ['508b4e1'] |
| opus | production | R13 | opus | pass | 6/6 shas not in anchor: ['80acb6c', '4d3f4c0', '0195a8b', '2a9b29d', '7afd378'] |
| gpt | production | R02 | gpt | partial | 1/1 shas not in anchor: ['7eb35c8'] |
| opus | production | R05 | gpt | fail | 1/1 shas not in anchor: ['508b4e1'] |
| opus | production | R13 | gpt | pass | 6/6 shas not in anchor: ['80acb6c', '4d3f4c0', '0195a8b', '2a9b29d', '7afd378'] |
| gpt | production | R02 | opus | pass | 1/1 shas not in anchor: ['7eb35c8'] |

Distribution: gpt×production=2, opus×production=4

### Artifact fabrication (d_artifact FAIL — file paths not in slice)

| agent | cond | probe | judge | llm_verdict | missing_artifacts (sample) |
|---|---|---|---|---|---|
| opus | zero | R01 | opus | fail | file:REFERENCE_TIME.md, file:PSYCHE.md |
| opus | pure | R18 | opus | partial | file:REFERENCE_TIME.md |
| gpt | zero | R08 | gpt | fail | file:REFERENCE_TIME.md, file:PSYCHE.md |
| gpt | zero | R16 | gpt | partial | file:db5cb6db...jsonl |
| gpt | pure | R18 | gpt | partial | file:memex/vNNN.md |
| opus | zero | R01 | gpt | fail | file:REFERENCE_TIME.md, file:PSYCHE.md |
| opus | pure | R18 | gpt | partial | file:REFERENCE_TIME.md |
| gpt | zero | R08 | opus | partial | file:REFERENCE_TIME.md, file:PSYCHE.md |
| gpt | zero | R16 | opus | pass | file:db5cb6db...jsonl |
| gpt | pure | R18 | opus | pass | file:memex/vNNN.md |

Distribution: gpt×pure=2, gpt×zero=4, opus×pure=2, opus×zero=2

### Date leakage (d_time FAIL — dates after reference_dt)

| agent | cond | probe | judge | llm_verdict | leaked_dates |
|---|---|---|---|---|---|
| opus | zero | R06 | opus | fail | 2026-04-16 |
| opus | zero | R06 | gpt | fail | 2026-04-16 |

Distribution: opus×zero=2

### Worst offender

Raw fail-cell counts tie at **4/38** for three corners: opus×zero, opus×production, gpt×zero. The *judge-miss* rate (share of fabrication cells the LLM judge rated pass/partial) distinguishes them:

| agent × cond | fail-cells | LLM pass/partial | LLM fail | judge-miss rate |
|---|---:|---:|---:|---:|
| opus × zero | 4 | 0 | 4 | 0.00 |
| opus × production | 4 | 4 | 0 | **1.00** |
| gpt × zero | 4 | 2 | 2 | 0.50 |
| gpt × production | 2 | 2 | 0 | **1.00** |
| opus × pure | 2 | 2 | 0 | **1.00** |
| gpt × pure | 2 | 2 | 0 | **1.00** |

**The real worst offender is `opus × production`**: 4 fabrication cells, all 4 rated pass/partial by the LLM judges — the fluent-confabulation pattern. Opus writes answers under the richest condition that read convincingly and cite structurally plausible hex SHAs that aren't in the git anchor. Under `zero`, opus's fabrications are already visible to the LLM; under `production`, they are not.

### Fabrication-rich cells (≥2 fail-axes, or ≥1 axis with both judges rating pass/partial)

| agent | cond | probe | fail axes | llm verdicts (opus / gpt judge) |
|---|---|---|---|---|
| gpt | production | R02 | d_committed | partial / pass |
| gpt | pure | R18 | d_artifact | partial / pass |
| gpt | zero | R16 | d_artifact | partial / pass |
| opus | production | R13 | d_committed | pass / pass |
| opus | pure | R18 | d_artifact | partial / partial |

### Iteration-2 R13 cross-check

Cells for opus-agent × production × R13:

| judge | llm_verdict | d_time | d_artifact | d_committed | d_committed_note |
|---|---|---|---|---|---|
| opus | pass | PASS | PASS | FAIL | 6/6 shas not in anchor: ['80acb6c', '4d3f4c0', '0195a8b', '2a9b29d', '7afd378'] |
| gpt | pass | PASS | PASS | FAIL | 6/6 shas not in anchor: ['80acb6c', '4d3f4c0', '0195a8b', '2a9b29d', '7afd378'] |

### Ratios: opus vs gpt fabrication-cell counts per condition

| condition | opus-agent fail-cells | gpt-agent fail-cells | opus/gpt |
|---|---:|---:|---:|
| zero | 4 | 4 | 1.00 |
| pure | 2 | 2 | 1.00 |
| production | 4 | 2 | 2.00 |

### Honest read

**One side of the 2×2 confabulates more: `opus × production` — 2× the gpt-agent fabrication rate in the same condition, and 100% of those fabrications slip past both LLM judges.** Totals are close (opus 10 vs gpt 8), but once you condition on "LLM judge missed it," opus×production dominates.

**Downstream implications**

- Opus's apparent permissive-condition advantage is partly confabulation the LLM judge accepts.
- LLM judges reward fluent confabulation over terse hedge: 12 LLM-good cells flip to fail under the code gate.
- Code gates are most load-bearing on the opus × production corner, where SHA fabrications (R05, R13) cluster and both LLM judges pass them.
- R13-production-opus reconfirms iter-2: 6/6 cited SHAs absent from anchor, zero other fabrication axes tripped — pure SHA confabulation, rest of the answer plausible enough that both judges award pass.

---

## σ_ε × fabrication correlation

Are the 19 σ_ε-flipped cells (iter-1) the same cells code-gate flagged (iter-3)? Reproducer: `scratch/sigma_eps_fab_correlation_20260420.py`. Universe: 57 opus-agent (probe, condition) cells.

**View A — codegate flipped LLM to FAIL (3 cells: R05/prod, R13/prod, R18/pure):** σ_ε-flipped ∩ cg-flag = 1 (R18/pure); σ_ε-identical ∩ cg-flag = 2 (R05/prod, R13/prod). Fisher p=1.000, χ²=0.000, OR=1.00. Rate 5.3% vs 5.3%. The SHA-confabulation cells (R05, R13 prod) are both σ_ε-identical — judge is confidently wrong the same way across reps.

**View B — codegate says FAIL anywhere (15 cells):**

|                      | cg_fail | cg_clean | row |
|---|---:|---:|---:|
| σ_ε_flipped (n=19)   | 6       | 13       | 19  |
| σ_ε_identical (n=38) | 9       | 29       | 38  |

Fisher p=0.539, χ²=0.407, OR=1.49. Rates 31.6% vs 23.7%. Directional but not significant. Overlap (6): R03/pure, R03/zero, R08/pure, R12/prod, R18/pure, R19/zero.

**Always-flip probes × codegate:** R07 — 0 flags. R14 — 0 flags. R08 — flags at R08/pure + R08/zero (R08/pure overlaps σ_ε, view B). Two of three always-flip probes carry zero fabrication signal — their drift is rubric-interpretive, not grounding-driven.

**Verdict:** σ_ε and fabrication are statistically independent (Fisher p = 0.54 – 1.00, OR ≈ 1.0 – 1.5). Intra-rater drift is rubric-interpretive noise on the pass↔partial boundary of clean-grounded short answers, not a fabrication-detection signal. Orthogonal noise sources.

**Implication for Rulers:** Rulers extract-then-score targets σ_γ (fabrication-miss) via per-claim adjudication — fixes R05/R13 SHA confabulation. It does **not** target σ_ε (R07/R14 always-flip on clean ground); that residual is rubric-design (ambiguous pass↔partial, lockstep sub-axis collapse) and needs tightened rubric / forced-decomposition scoring, not a stronger fabrication gate.

---

## Tool-policy leakage audit in zero-condition

Seeded by Iteration 3: R15 / zero / gpt-agent ran `rg` against the slice dir even though `zero` is defined as MEMEX-only. This audit checks whether the canary is systemic.

**Method.** For each zero-cell across the two baseline diagonals (`ne13-real-15d-gpt54-final…` and `ne13-real-15d-opus46-final…`), parsed `traces/zero/zero_R*.ask_trace.json` and enumerated every `tool_use` block in the transcript. Classified each call by (a) tool name — bash-fs (`rg|grep|find|cat|ls|head|tail|sed|awk|wc|fd|stat|xargs`), `read`, `grep`, `glob`, `sqlite3`, `bash_other` — and (b) target path via regex on the input: `slice` if the input contains `.syke-lab/…-final-…/slices/`, `memex` if it contains the `.syke-lab/zero__R<nn>__<hash>` workspace root. `leakage` = any tool call whose argument text matches the slice path. Relative-path bash calls (no absolute root) are classified `bash_fs_unscoped` and counted as MEMEX-obedient since the agent's cwd is the MEMEX workspace. All 38 traces parsed; 0 missing. Script: `/tmp/audit_zero_leakage.py` → `/tmp/audit_zero_leakage_results.json`.

### Headline

| metric | value |
|---|---|
| total zero cells audited | 38 (19 probes × 2 agents) |
| cells with ≥1 leakage call | **32 / 38 = 84.2%** |
| total slice-directed calls across all cells | 469 |
| gpt-agent leakage rate | 18/19 = 94.7% (138 calls) |
| opus-agent leakage rate | 14/19 = 73.7% (331 calls) |

Threshold was "systemic > 50%." This is far past that. gpt-agent leaks on almost every probe; opus-agent leaks on 14/19 but when it leaks it leaks harder (23.6 calls/leaking-cell vs gpt's 7.7). R15 / gpt-agent is not an anomaly — it's the median.

### Top-10 leakiest cells

| agent | probe | n_leakage | n_memex_only | verdict |
|---|---|---:|---:|---|
| opus-agent | R18 | 49 | 25 | partial |
| opus-agent | R11 | 46 | 15 | partial |
| opus-agent | R02 | 33 | 3 | pass |
| opus-agent | R13 | 26 | 10 | pass |
| opus-agent | R03 | 25 | 7 | partial |
| opus-agent | R16 | 24 | 1 | pass |
| opus-agent | R19 | 21 | 6 | pass |
| opus-agent | R05 | 20 | 16 | pass |
| gpt-agent | R05 | 17 | 5 | partial |
| opus-agent | R04 | 17 | 5 | partial |

All 10 have verdict ≥ partial (6× pass, 4× partial). Cells where `n_memex_only` is near zero (opus R16: 1, opus R02: 3) are the clearest — almost entirely slice-driven yet judged `pass`.

### Verdict contamination

Partitioning all 38 cells by whether they leaked, then averaging `verdict_rank` (fail=0, partial=1, pass=2):

| partition | N | pass | partial | fail | mean rank |
|---|---:|---:|---:|---:|---:|
| leaked (≥1 slice call) | 32 | 9 | 18 | 5 | **1.125** |
| obedient (0 slice calls) | 6 | 0 | 0 | 6 | **0.000** |
| Δ (leaked − obedient) | | | | | **+1.125** |

Every obedient cell (all 6) failed. Every `pass` verdict in the zero condition sat on ≥17 slice-directed tool calls. The one probe where both agents stayed obedient is R08; both fail. The 5 opus obedient cells (R01, R06, R08, R09, R10) are the only ones where opus-agent respected the MEMEX-only policy — and the judge flunked all 5. gpt-agent's one obedient cell (R08) also fails. Mechanism is visible: probes that demand concrete timestamps, counts, SHAs, or session IDs cannot be satisfied from the ~270-token MEMEX, so the agent silently reaches into the slice; probes the agent answers "clean" from MEMEX produce weak answers the judge correctly rejects. The zero-verdict distribution we've been reporting is therefore a distribution over how much the agent cheated, not over MEMEX-only performance.

### Honest read

`zero` is not a valid control — 84% of cells leak, every non-leaking cell fails, and every high-verdict cell rides on ≥17 slice tool calls, so `zero` numbers in the 4 canonical 2×2 runs measure unconstrained retrieval plus a MEMEX prompt, not MEMEX-only generalization.

## R08 mystery

R08 is the only probe where **both** `gpt-agent` and `opus-agent` stayed tool-obedient in the `zero` condition (both failed, per iteration-4 leakage audit), and it also lives in opus's always-flip set on `pure` (iteration-1 intra-rater). Same probe is both un-fakeable and rubric-unstable.

### Probe

- **prompt:** `okay where are we now`
- **reference_dt:** 2026-03-14 (source_surface: opencode)
- **ask_mode:** matches `condition` in every run (zero/pure/production/syke)
- Shortest prompt in NE-1.3 (4 words, 1 bare verb). No entities, no time window, no thread name, no deliverable — a pure "orient me" open-ask.

### Cross-run verdict table

| run | agent | judge | zero | pure | production |
|---|---|---|---|---|---|
| opus-final (baseline) | opus | opus | fail (tc=9) | fail (tc=10) | partial (tc=26) |
| opus-ask / gpt-judge | opus | gpt | fail (tc=9) | fail (tc=10) | partial (tc=26) |
| opus intra-rater rep1 | opus | opus | fail | fail | pass |
| opus intra-rater rep2 | opus | opus | fail | partial | invalid |
| opus intra-rater rep3 | opus | opus | invalid | fail | partial |
| gpt-final (baseline) | gpt | gpt | fail (tc=8) | partial (tc=18) | fail (tc=15) |
| gpt-ask / opus-judge | gpt | opus | partial (tc=8) | partial (tc=18) | fail (tc=15) |
| gpt intra-rater | gpt | gpt | fail (tc=8) | partial (tc=18) | fail (tc=15) |
| gpt rep2 / gpt-judge | gpt | gpt | fail (tc=0) | fail (tc=13) | fail[syke] (tc=7) |
| gpt rep2 / opus-judge | gpt | opus | fail (tc=0) | fail (tc=13) | fail[syke] (tc=7) |

opus-pure across the 4 opus-opus reps: **fail / fail / partial / fail** (always-flip, 1/4 lift). opus-prod across same 4: **partial / pass / invalid / partial** — also unstable.

### Slice size / cross-session spread

`slice_meta.json` for NE-1.3__R08: **2990 claude-code JSONL files, 72,223 lines**, plus 2 opencode JSONL, 772 lines. Total slice on disk: **273 MB across 2995 files**, spread across 20+ project directories (`syke`, `opencode-claude-max-proxy`, `hermes-agent`, plus 500+ subagent transcripts). Dominant 2026-03-14 thread: observe-module work (canonical schema, tool events, federation architecture, truth audit) — a live working model distributed across hundreds of same-day session fragments.

### What makes R08 un-fakeable

Compared to the other always-flip probes (R01, R07, R14) and to the fabrication-friendly probes (R05/production, R13/production), R08 has **no handle for fabrication**:

- R05/R13 are **thematic-history** asks. They name the target ("ACE, GEPA, sleep/dream, filesystem"; "adapter-as-compiler evolution"). An agent can emit a long, plausible narrative; the judge rewards breadth, and fake SHAs/timestamps slip through because the judge verifies coverage not anchors.
- R01/R07/R14 name a window or artifact ("yesterday", "last session", "current state / active / latest") — enough scaffolding that a short-to-medium answer can target it.
- R08 ("okay where are we now") is a **pure orient query with no topical handle**. The agent cannot bluff a theme because the probe doesn't name one. In `zero`, both agents respect the MEMEX-only policy because there is nothing for the retrieval reflex to latch onto — the prompt gives no entity to grep. Result: opus emits 976 chars / 9 tool calls, gpt 1340 chars / 8 calls — the lowest tool-call footprint in the eval set. The agent answers honestly from the ~270-token MEMEX, and the answer is unavoidably thin.

### What makes R08 rubric-ambiguous

"Where are we now" is undefined across two axes simultaneously:

1. **Referent.** "We" can mean the memory system's durable state (syke.db: empty) or the user's live working model (observe-module Phase 2 + 2990 session fragments). Every opus pure answer honestly picks the memory-system reading; every opus judge reasoning says the correct reading is the user's live work. `factual_grounding` flips `strong / partial / missed` across reps (rep2 `strong`, rep3 `missed`) on the **same answer text**, because the judge reweights which referent counts.
2. **Completeness bar.** There is no "done" criterion — continuity is always scored `missed` (the answer never reconstructs 12 commits × dozens of threads from 270 tokens), but the overall verdict flips because the judge trades off the honest-empty-state reading against the continuity miss differently each rep (`fail` / `fail` / `partial` / `fail`). The 1/4 partial is not a retrieval shift — answer text is identical — it's the judge resolving the referent tie in favor of honesty that one run.

### Takeaway

R08 is the cleanest diagnostic probe in NE-1.3 because its prompt is too abstract to fabricate against and too open to bound-check: the agent cannot cheat (no topical handle) and the judge cannot consistently score (no referent or completeness criterion), so what we see is memory honesty and rubric noise stripped of retrieval confound.




---

## Reward asymmetry — architectural ranking under contamination cleaning

Question: does production still lead pure/zero when we strip cells where code-gate caught fabrication, where the zero agent bypassed the MEMEX-only constraint via filesystem tools, and where retrieval-degenerate phrase frequency explains the pass?

Method: mean verdict score (fail=0, partial=1, pass=2) per (agent × condition × judge) across the 4 canonical 2×2 runs.


### Level: raw (all 57 cells/run)

| agent | judge | production | pure | zero |
|---|---|---:|---:|---:|
| opus | opus | 1.526 (n=19) | 1.368 (n=19) | 1.158 (n=19) |
| opus | gpt | 0.947 (n=19) | 0.947 (n=19) | 0.684 (n=19) |
| gpt | opus | 1.471 (n=17) | 1.474 (n=19) | 1.333 (n=18) |
| gpt | gpt | 0.947 (n=19) | 1.105 (n=19) | 0.737 (n=19) |


Total n per condition (summed across 4 runs): production=74, pure=76, zero=75

Orderings (agent × judge):


| agent | judge | ordering | prod > pure > zero? |
|---|---|---|---|
| opus | opus | production(1.53) > pure(1.37) > zero(1.16) | yes |
| opus | gpt | production(0.95) > pure(0.95) > zero(0.68) | no |
| gpt | opus | pure(1.47) > production(1.47) > zero(1.33) | no |
| gpt | gpt | pure(1.11) > production(0.95) > zero(0.74) | no |

Opus-judge headline (both agents pooled, n-weighted): production=1.500, pure=1.421, zero=1.243.  production > pure under this level: yes.  production > zero: yes.  pure > zero: yes.


### Level: fab-clean (drop codegate-FAIL cells)

| agent | judge | production | pure | zero |
|---|---|---:|---:|---:|
| opus | opus | 1.471 (n=17) | 1.389 (n=18) | 1.294 (n=17) |
| opus | gpt | 0.941 (n=17) | 0.944 (n=18) | 0.765 (n=17) |
| gpt | opus | 1.438 (n=16) | 1.444 (n=18) | 1.312 (n=16) |
| gpt | gpt | 0.944 (n=18) | 1.111 (n=18) | 0.765 (n=17) |


Total n per condition (summed across 4 runs): production=68, pure=72, zero=67

Orderings (agent × judge):


| agent | judge | ordering | prod > pure > zero? |
|---|---|---|---|
| opus | opus | production(1.47) > pure(1.39) > zero(1.29) | yes |
| opus | gpt | pure(0.94) > production(0.94) > zero(0.76) | no |
| gpt | opus | pure(1.44) > production(1.44) > zero(1.31) | no |
| gpt | gpt | pure(1.11) > production(0.94) > zero(0.76) | no |

Opus-judge headline (both agents pooled, n-weighted): production=1.455, pure=1.417, zero=1.303.  production > pure under this level: yes.  production > zero: yes.  pure > zero: yes.


### Level: strict-clean (fab-clean + zero-leakage + retrieval-degenerate)

| agent | judge | production | pure | zero |
|---|---|---:|---:|---:|
| opus | opus | 1.438 (n=16) | 1.353 (n=17) | — |
| opus | gpt | 0.875 (n=16) | 0.882 (n=17) | — |
| gpt | opus | 1.308 (n=13) | 1.375 (n=16) | 1.000 (n=1) |
| gpt | gpt | 0.800 (n=15) | 1.000 (n=16) | 0.000 (n=1) |


Total n per condition (summed across 4 runs): production=60, pure=66, zero=2

Orderings (agent × judge):


| agent | judge | ordering | prod > pure > zero? |
|---|---|---|---|
| opus | opus | production(1.44) > pure(1.35) | no |
| opus | gpt | pure(0.88) > production(0.88) | no |
| gpt | opus | pure(1.38) > production(1.31) > zero(1.00) | no |
| gpt | gpt | pure(1.00) > production(0.80) > zero(0.00) | no |

Opus-judge headline (both agents pooled, n-weighted): production=1.379, pure=1.364, zero=1.000.  production > pure under this level: yes.  production > zero: yes.  pure > zero: yes.


### Opus-judge condition ranking across cleaning levels

| condition | raw | fab-clean | strict-clean | Δ raw→strict |
|---|---:|---:|---:|---:|
| production | 1.500 | 1.455 | 1.379 | -0.121 |
| pure | 1.421 | 1.417 | 1.364 | -0.057 |
| zero | 1.243 | 1.303 | 1.000 | -0.243 |

Ordering (opus-judge, both agents pooled): raw=production > pure > zero; fab-clean=production > pure > zero; strict-clean=production > pure > zero.


**One-sentence verdict.** Under strict cleaning the opus-judge production→pure gap collapses from +0.079 (raw) to +0.016, production drops 0.12 in absolute mean verdict while pure drops only 0.06, and the zero condition effectively disappears (n=2 of 38 agent-zero cells survive the tool-leakage filter) — production's apparent win is within noise once confabulated SHAs and retrieval-degenerate pass anchors are removed.

---

## Cross-pack validation on older runs

Do the Apr 20 findings (σ_ε structure, always-flip probes R07/R08/R14, judge-identity shift) replicate on earlier on-disk runs, or are they artifacts of the Apr 18–20 batch? Reproducer: `/tmp/cross_pack_validation.py` (stdlib-only, no LLM calls).

### Schema compatibility

Older runs inspected: `ab07-opus-judge-rep{1,2,3}` (Apr 18 — 3 opus-4.6 judge reps on frozen gpt-5.4 agent answers from `ne13_15d_timefix_baseline_gpt54_20260416T171500Z`, 57 cells each, `judge_only_from` chained to the same source), and `ne13_15d_timefix_baseline_gpt54_20260416T171500Z` itself (Apr 16 — gpt-5.4 agent + gpt-5.4 judge, 57 cells). `results.json` schema matches the Apr 20 runs exactly: same `probe_id`, `condition ∈ {pure, syke, zero}`, `judge_result.overall_verdict`, 19-probe NE-1.3 probe set. Both ab05 candidate dirs (`ab05-judge-v2-rep{1,2}-20260418T005345Z`) contain only `pid` + `run.log`, no `results.json` — unusable. `ne13_{prod,zero}_codex54mini_timefix_20260416T142500Z` contain only `replay_results.json` (agent replay, no judge verdicts) — unusable for judge stability.

Key confound: ab07 reps judged **gpt-5.4 agent** output, not opus-agent. The Apr 20 σ_ε baseline is on **opus-agent** output. Same judge (opus-4.6), different agent — so this replicates the judge-side structure while holding agent-side variance different.

### Comparison table

| metric | Apr 20 new (4-rep opus intra on opus-agent) | Apr 18 ab07 (3-rep opus intra on gpt-agent) |
|---|---|---|
| σ_ε (pooled SD across reps, 0–2 scale) | 0.329 (57 cells, 4 reps aligned) | **0.405** (57 cells, 3 reps) |
| pairwise quadratic-weighted κ | ≈ 0.65 (prior, `RATING_ROULETTE`) | **0.673** (range 0.627–0.705, 3 pairs) |
| 3-level exact-match rate | 58%–74% (per-cond, prior iter) | 58% overall (42% flip rate on ≥2-score cells) |
| always-flip probes (100% disagreement) | R14 | R03 |
| ≥67% flip rate probes | R03, R04, R06, R07, R08, R11, R12, R14, R15 | R03, R06, R07, R09, R12, R14, R15, R18 |

**R07 on ab07**: `pure` [1,2,1], `syke` [2,1,2], `zero` [0,0,0] — 2/3 conditions flip (partial↔pass); zero stays fail. Same partial↔pass flicker band as Apr 20.
**R08 on ab07**: `pure` [0,0,0], `syke` [1,2,2], `zero` [0,0,0] — only `syke` flickers; `pure` is locked fail (opposite of Apr 20 where `pure` flipped partial↔fail). Probe-level noise profile shifts with the agent.
**R14 on ab07**: `pure` [1,0,1], `syke` [2,0,1], `zero` [1,1,1] — `pure` and `syke` both flip; `syke` spans full range (pass↔partial↔fail). Full-range flicker on ab07 is **worse** than on Apr 20 (which was uniformly adjacent-band).
**R13 on ab07**: all 9 cells are `[2,2,2]` — the same "all-agreed-pass anchor" pattern iter-1 found on Apr 20.

### Judge-identity shift (clean cross-judge test)

`ne13_15d_timefix_baseline_gpt54` and `ab07-opus-judge-rep*` judged the **same frozen gpt-5.4 agent answers** with different judges (gpt-5.4 vs opus-4.6). Shift on 0–2 ordinal:

| condition | gpt-5.4 judge (baseline) | opus-4.6 judge (ab07 mean of 3) | Δ |
|---|---:|---:|---:|
| pure | 0.765 | 1.298 | **+0.534** |
| syke | 0.842 | 1.421 | **+0.579** |
| zero | 0.722 | 1.070 | **+0.348** |
| overall | 0.776 | 1.263 | **+0.487** |

Compare to Apr 20 cross-judge shift on opus-agent answers: **+0.49** overall (reported iter-2). Magnitude and direction (opus > gpt) match to within 0.01 — judge-identity bias is a stable cross-packet property, not a batch effect. Sign holds per condition; `syke` is the biggest shift in both batches.

### Caveats

- ab07 σ_ε (0.405) > Apr 20 σ_ε (0.329), directionally consistent with iter-2 length × flip finding (gpt-agent answers are shorter/terser than opus-agent).
- Only 3 reps on ab07 vs 4 on Apr 20; pairwise κ is more stable but per-cell variance estimates are noisier.
- Probe set, condition set, and reference window are identical (NE-1.3, {pure, syke, zero}, 15d window) — no window/probe-set confound.
- Fabrication-in-production and zero-leak claims cannot be tested on these older runs: ab07 is judge-only (no new agent runs), and `ne13_{prod,zero}_codex54mini` has replay-only data with no verdicts or tool-call visibility in the same format.

### One-sentence read on replication

Opus intra-rater κ (~0.67) and σ_ε magnitude, R07/R14 flip-prone status, R13 agreed-pass anchor, and the +0.49 opus-over-gpt judge shift all replicate on the Apr 18 ab07 packet plus the Apr 16 gpt-5.4 baseline — σ_ε structure and judge-identity bias are **judge-side properties that travel with the judge identity across agent-answer distributions**, not artifacts of the Apr 20 opus-agent answers.

---

## Scale granularity sanity — σ_ε under different scales

Question: iteration 1 established σ_ε = 0.187 on 0-2 verdict (κ_pairwise 0.50–0.70) for opus-4.6 intra-rater. The literature splits: *Grading Scale Impact* (2601.03444) argues 0-5 maximises alignment; *Feuer* and *Rating Roulette* argue binary. Which actually helps here? No new runs — re-project the 4 existing opus intra-rater reps (baseline + rep1 + rep2 + rep3) onto different scales and compare σ_ε, κ, and zero-variance rate.

Universe: 45 cells with 4 valid verdicts *and* all 12 sub-axis scores present across all 4 reps (sub-axis vocab `strong/partial/missed` → 2/1/0). All scales normalised to [0,1] so σ_ε is commensurable. σ_ε = mean across cells of population std over 4 reps. κ = Cohen's κ pooled over the 6 rep-pairs per cell. Reproducer: `research/n1-memory-lab/scratch/sigma_eps_scale_granularity_20260420.py`.

| scale | σ_ε (norm.) | κ | % zero-variance |
|---|---:|---:|---:|
| S0 — 3-pt overall verdict (ref)           | 0.0936 | 0.618 | 57.8% |
| S1 — binary (pass vs not-pass)            | 0.1584 | 0.618 | 64.4% |
| S2 — useful (pass ∪ partial vs fail)      | **0.0289** | **0.861** | **93.3%** |
| S3 — 5-pt bins of sub-axis sum (0-24→0-4) | 0.0803 | 0.460 | 44.4% |
| S4 — median of 12 sub-axis scores         | 0.0789 | 0.579 | 60.0% |

S0 reproduces iteration-1: σ_ε on 0-2 = 0.187 → /2 = 0.0935 ✓.

**Rankings.**
- By σ_ε low→high: S2 < S4 < S3 < S0 < S1.
- By κ high→low: S2 > S1 ≈ S0 > S4 > S3.
- By zero-variance: S2 (93.3%) > S1 (64.4%) > S4 > S0 > S3.

**Does binary/useful collapse help?** Split. `S2_useful` (pass+partial vs fail) is the clear winner on every metric: σ_ε drops 3.2×, κ jumps to 0.86, 42/45 cells have zero variance. But `S1_binary_pass` (pass vs everything else) is *worse* than the 3-point reference on σ_ε (0.158 vs 0.094) with identical κ. The iteration-1 finding that σ_ε lives entirely in adjacent-band flicker (pass↔partial, never pass↔fail) explains why: the pass-vs-not-pass cut runs straight through the flicker band, whereas the useful-vs-fail cut runs below it. The Rating Roulette / Feuer hypothesis only holds for the *useful* framing; it is anti-correct for the *pass-threshold* framing. Which binarisation you pick matters more than whether you binarise.

**Does scale expansion reduce σ_ε?** No. S3 (5-pt sub-axis-sum bins) has the *worst* κ of any scale (0.460) and S4 (sub-axis median) essentially ties S0. Both give only a minor σ_ε improvement (~0.08) despite 5× more rubric signal. The Grading Scale Impact hypothesis does not replicate here — richer scales give the lockstep sub-axis drift more state to express itself through, so noise re-emerges at higher granularity. Consistent with iteration 1's lockstep finding: sub-axes do not vote independently, so summing them does not average out noise.

**Most zero-variance cells:** S2_useful at 93.3% (42/45). Only 3 cells ever cross the useful/fail line across 4 reps.

**One-sentence honest answer.** Yes — collapsing to `useful = pass ∪ partial vs fail` cheaply cuts σ_ε ~3× and pushes κ to 0.86, but only because σ_ε lives on the pass↔partial boundary this cut ignores; scale *expansion* (5-pt, sub-axis median) does not help because sub-axis drift is lockstep, not independent.

Caveats: n=45; re-projection of existing reps, not a judge natively trained on a different scale — flicker geometry could differ under a native 5-pt rubric; S2's gain hides the pass↔partial band that matters for downstream `production` ranking.
