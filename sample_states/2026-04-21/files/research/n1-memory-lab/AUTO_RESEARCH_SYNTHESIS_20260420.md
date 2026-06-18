# Auto Research Synthesis — 2026-04-20

Companion to `AUTO_RESEARCH_LOOP_20260420.md`. Six iterations, no new runs, audience: the next Claude session and codex, picking this up cold.

---

## 1. Headline

The 285-verdict 2×2 opus/gpt packet cannot support any architectural claim. Three independent contamination modes stack across conditions — retrieval-degeneracy in `pure`, tool-policy leakage in `zero`, SHA confabulation in `production` — and strip-cleaning them leaves n=2 surviving `zero` cells and the production/pure gap inside noise. What the packet does support is a cleanly decomposed judge-noise model: σ_ε is structured (adjacent-band pass↔partial flicker on short clean-grounded answers, with all 3 top-level rubric axes moving in lockstep), σ_γ is a stable cross-packet +0.49 opus-over-gpt shift driven by a definitional tip-vs-landscape split on `s_state`, and the two are statistically independent (Fisher p≈0.5–1.0, OR≈1.0–1.5). The judge's 12-axis rubric is over-specified: `state_transition_tracking` alone explains R²≈0.73 (opus) / 0.61 (gpt) of verdict variance, and the a-priori TOP-5 axis picks diverge from the empirical |β| ranking. Code gates (`d_time`, `d_artifact`, `d_committed`) do real work — they nearly double cross-judge κ on gpt-agent answers (0.151 → 0.298) and resolve one of three P↔F structural-bias disagreements — but have nothing to say where the residual disagreement lives.

---

## 2. Corrections to prior notes

### `CALIBRATION_STACK_20260420.md`
- **σ_ε status.** σ_ε is measured on this packet: 0.329 (pooled SD across 4 reps, 0–2 scale), κ_pairwise ≈ 0.65, flip rate 42% (19/45 cells). Drift is adjacent-band only, never pass↔fail — this is new relative to the calibration stack's treatment of σ_ε as an open variable. Iteration 1, `σ_ε flip structure`; replicated on ab07 (σ_ε=0.405, κ=0.673) in Iteration 5, `Cross-pack validation`.
- **Architecture-claim gate.** The stack's implicit assumption that one day's 285-verdict surface can gate architecture claims must be retracted. Iteration 3, `Retrieval-degeneracy audit` + `Code-gate D_t replay` + Iteration 4, `Tool-policy leakage audit`: after strict cleaning, agreed-pass count drops to 0 and the `zero` condition effectively disappears (n=2/38 surviving).

### `JUDGE_MINING_SYNTHESIS_20260420.md`
- **Agreed-pass count.** Prior note said 6; actual is **9 pre-cleaning** (R01/pure-gpt, R04/prod-gpt, R12/prod-gpt, R13/pure-gpt, R15/zero-gpt, R02/prod-opus, R11/pure-opus, R13/prod-opus, R13/pure-opus). Iteration 1, `Agreed-pass anchor cells`. The 6 figure was pre-invalid-exclusion or diagonal-only. Post-R13 demotion → 6; post-retrieval-degeneracy audit → 0.
- **Architectural ordering.** "production > zero > pure" working assumption is not supported. Raw anchor = `production ≈ pure > zero`; after R13 retrieval-demote = `production > pure > zero` (Iteration 2, `R13 anomaly dive`); after strict contamination cleaning = no defensible ordering (Iteration 5, `Reward asymmetry`).

### `COUNCIL_FORMALISM_20260420.md`
- **What the packet supports.** Supports the framing that the 12-axis rubric is measuring one latent verdict (lockstep-axis finding, 10/19 flipped cells move all 3 top-level axes together; Iteration 1, `σ_ε flip structure`). Supports the D_t vs S_t split for the structural-bias locus (P↔F disagreements are `s_state` disagreements, not D_t disagreements; Iteration 2, `Structural-bias anatomy`). **Does not** support any claim that writing the contract is sufficient to unify judges — the Iteration 3 retroactive s_state rule application moved binary κ from +0.59 to +0.42 (got worse) because per-judge rubric scores already encode the disagreement one level deeper.

### `FORMALISM_LAYER_SEPARATION_20260420.md`
- **Stayed true.** The D_t / S_t separation is load-bearing: D_t items (d_time, d_artifact, d_committed) are deterministic code-gate work, S_t items (s_state, s_restart) are genuinely semantic (Iteration 3, `Code-gate D_t replay`). Moving fabrication detection to pre-LLM code filters is strictly correct.
- **Needs revision.** The writeup implies S_t is ambiguity the LLM resolves; Iteration 4 `Judge-independent tip-anchor schema` shows S_t needs an upstream `unresolved_state_inventory.json` artifact (derivable mechanically from slice, 60–70% coverage today, full coverage needs `issues_snapshot.json`). Without it, S_t judges import private priors via `active_thread_selection`.

---

## 3. Noise decomposition — current best read

| component | what it is | measured value | dominant fix |
|---|---|---|---|
| σ_α (probe) | Variance from probe-intrinsic difficulty and retrieval-vs-reconstruction character | Not cleanly isolated; contaminated by retrieval-degeneracy (R13 grep-hits 195+ in slice, R11 1497×, R04 1012×) | Preflight grep-density check; retire any probe whose load-bearing phrase hits >50× in slice |
| σ_β (agent) | Variance between ask-agents on the same probe/condition/judge | Not cleanly measured — only 1 clean rep per (agent, config) exists; 3 gpt-5.4-mini reps are contaminated (wrong model) | Run ≥2 clean agent reps per config on a fresh packet; register as protocol step |
| σ_γ (judge identity) | Cross-judge verdict shift on the same frozen answers | **+0.487 opus-over-gpt** on 0–2 scale (ab07 gpt-agent, replicates Apr 20 opus-agent +0.49 to within 0.01); κ 3-level 0.15–0.27, κ binary 0.41 (gpt-agent) / 0.71 (opus-agent) | Judge-independent tip-anchor schema (`unresolved_state_inventory.json`) + written `s_state` contract |
| σ_ε (judge stochasticity) | Same judge rejudging same frozen answers | **0.329 pooled SD (0–2); κ_pairwise ≈ 0.65; flip rate 42%; all adjacent-band**. Flips concentrate on pure (50%), short answers (Q1 58% vs Q4 27%), and R07/R08/R14 always-flip | Collapse to `useful = pass ∪ partial vs fail` (σ_ε drops 3.2× to 0.029, κ → 0.86, 93% zero-variance); keep 3-level only for internal calibration |
| contamination (confound on σ_α) | Fabrication (SHA confabulation) + leakage (filesystem bypass in zero) + retrieval-degeneracy (slice eats its own answer) | 12/228 codegate flips (5.3%); 32/38 zero cells leak (84%); 6 of 6 non-R13 agreed-pass cells retrieval-degenerate | Code-gate pre-filter; drop `rg/grep/find/cat/ls` from zero tool surface; grep-density preflight |

σ_ε and fabrication are orthogonal (Iteration 4, `σ_ε × fabrication correlation`: Fisher p=0.54–1.00, OR 1.0–1.5). Rulers-style extract-then-score targets σ_γ, not σ_ε.

---

## 4. What the existing packet can and cannot support

**CAN (with flagged caveats):**
- σ_ε measured (0.329, κ 0.65, flip structure characterized).
- σ_γ direction (+0.49 opus>gpt, stable across packets) and locus (`active_thread_selection` sub-axis).
- Fabrication density per cell (12/228 codegate flips; opus×production = worst offender, 4/4 slip past both LLM judges).
- R² of rubric schema (gpt 0.754, opus 0.862; TOP-3 axes for opus recover 0.851).
- Length → σ_ε effect (β₁ = −0.33 log-odds per e-fold length; short answers flip ~2×).
- Judge-independent tip-anchor feasibility map (13/19 probes resolvable mechanically from current slice format).
- Replication of judge-side noise structure on older ab07 (Apr 18) + ne13_15d_timefix (Apr 16) packets.

**CANNOT:**
- Any architectural ordering claim (`production` vs `pure` vs `zero`). Strict-clean n collapses; agreed-pass n = 0.
- A clean `zero` condition. 84% of zero cells bypass MEMEX-only via `rg`/`grep`; every non-leaking zero cell fails.
- A clean σ_β. No config has >1 uncontaminated agent rep.
- A real zero control. "MEMEX-only" as implemented is "MEMEX in system prompt + full filesystem access."
- Inferential weight on anything — n per cell is 17–19, pair-cells ≤114, rubric fit at ~9.5 obs/predictor.

---

## 5. The three distinct judge problems

Iteration 4's σ_ε × fabrication correlation established these are orthogonal.

1. **Fabrication (feeds σ_γ via LLM-miss).** Example: R13/prod-opus cites six SHAs, zero in the 200-commit anchor; both LLM judges rate it pass. Fix: code gates (`d_time`, `d_artifact`, `d_committed`) as hard pre-LLM filter. Removes ~5.3% of verdicts from LLM-judged space. Iteration 3, `Code-gate D_t replay`.
2. **Definitional `s_state` disagreement.** gpt-judge: tip = latest unresolved observation in freshest surface. opus-judge: tip = latest committed/verifiable artifact + landscape around it. Flows through `active_thread_selection` sub-axis (flips 3/3 P↔F cells). Fix: judge-independent `unresolved_state_inventory.json` artifact built mechanically at judge-time, with codified surface-priority tie-break. A written `s_state` contract alone is insufficient (Iteration 3 retroactive rule application made binary κ worse). Iteration 2, `Structural-bias anatomy`; Iteration 4, `Judge-independent tip-anchor schema`.
3. **Rubric boundary noise (σ_ε).** Pass↔partial flicker on short clean-grounded answers; all sub-axes move in lockstep, so scale expansion (5-pt, sub-axis median) does not help. Fix: collapse headline metric to `useful = pass ∪ partial vs fail` (σ_ε drops 3.2×, κ → 0.86). Note: `S1_binary_pass` (pass vs everything-else) is *worse* than 3-level because the pass/not-pass cut slices through the flicker band. Keep 3-level for internal calibration only. Iteration 5, `Scale granularity sanity`.

---

## 6. Next-benchmark readiness checklist

Before any new benchmark runs produce useful data:

1. **Drop `rg`, `grep`, `find`, `cat`, `ls`, `head`, `tail`, `sed`, `awk`, `wc`, `fd`, `stat`, `xargs` from zero-condition tool surface.** Read-sandbox must block `slices/**`. Currently 84% of zero cells leak.
2. **Run grep-density preflight on every probe.** Any load-bearing phrase ≥50 hits in slice → flag `grep-degenerate`, exclude from architectural claims (keep as retrieval-floor baseline).
3. **Implement code-gate (`d_time`, `d_artifact`, `d_committed`) as a hard pre-LLM filter.** If the answer cites a SHA not in `local_git_anchor.json`, the verdict is FAIL before the LLM judge sees the cell. Reproducer lives at `scratch/code_gate_dt_replay_20260420.py` and runs stdlib-only.
4. **Build `unresolved_state_inventory.json` for NE-1.3.** 60–70% coverage achievable now from `slice JSONL + git anchor + memex`. Full coverage (especially R05-class open-issues probes and surface-agnostic R01/R08/R19) requires adding `issues_snapshot.json` to the slice format and committing to an explicit surface-priority ordering.
5. **Collapse verdict to `useful` vs `not_useful` for the headline metric.** Keep 3-level for internal calibration. Do *not* use `S1_binary_pass` (pass vs rest) — it runs through the flicker band.
6. **Register σ_β measurement as a protocol step.** ≥2 clean agent reps per config on a fresh packet; never re-use a gpt-5.4-mini-labelled run as gpt-5.4.

---

## 7. Open questions the packet can't close

*All out of scope for current data — require fresh runs or slice-format changes.*

1. **σ_β magnitude.** Does agent-side variance (between reps of same model, same config) rival σ_γ? No clean data — only contaminated gpt-5.4-mini reps exist.
2. **Does the opus×production confabulation pattern persist once code gates are deployed pre-LLM?** Is it a compensation reflex for tight retrieval, or intrinsic model behavior?
3. **Do the 3 always-flip probes (R07, R08, R14) remain always-flip under a `useful` collapse?** Or is flicker purely on the pass↔partial line that the collapse ignores?
4. **Agent-identity σ_γ residual.** Specificity and hedge do not mediate opus-agent's +0.13 binary-agreement advantage over gpt-agent. What agent property does? Needs content-feature extractor beyond length/hedge.
5. **Clean `zero` ordering.** With the tool surface actually restricted, does `production > pure > zero` hold, or does pure leapfrog production? Requires a re-run on a read-sandbox.
6. **Rulers extract-then-score viability.** Predicted to reduce σ_ε on R07/R14 cells and *worsen* σ_γ (the tip disagreement moves into Stage 1). Needs extractor-only rerun stability test on the 19 flipped cells (76 extract calls, no new agent runs — cheap, but no data yet).

---

## 8. Key evidence pointers

### 4 canonical 2×2 run dirs
- `runs/ne13-real-15d-opus46-final-20260420T071500Z` (opus-agent × opus-judge, diagonal)
- `runs/ne13-real-15d-gpt54-final-20260420T071500Z` (gpt-agent × gpt-judge, diagonal)
- `runs/ne13-real-15d-opusask-gpt54judge-20260420T144210Z` (opus-agent × gpt-judge, cross)
- `runs/ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z` (gpt-agent × opus-judge, cross)

### 3 opus intra-rater rep dirs (all `judge_only_from` the opus-opus baseline)
- `runs/ne13-real-15d-opusask-opusjudge-intrarater-20260420T200314Z` (rep1)
- `runs/ne13-real-15d-opus46-intrarater-rep2-20260420T222645Z` (rep2)
- `runs/ne13-real-15d-opus46-intrarater-rep3-20260420T222645Z` (rep3)

### Codegate JSON + scripts under `scratch/`
- `research/n1-memory-lab/scratch/code_gate_dt_replay_20260420.py`
- `research/n1-memory-lab/scratch/code_gate_dt_replay_20260420.json` (per-cell dump, 228 cells, auditable)
- `research/n1-memory-lab/scratch/fabrication_density_20260420.py`
- `research/n1-memory-lab/scratch/clean_packet_calibration_20260420.py`
- `research/n1-memory-lab/scratch/reward_asymmetry_cleaning_20260420.py`

### Iteration reproducer scripts
- Iter 1 σ_ε structure: `scratch/sigma_eps_flip_structure_20260420.py`
- Iter 1 rubric ablation: `scratch/schematic_adherence_ablation_20260420.py`
- Iter 3 retroactive s_state rule: `scratch/retro_sstate_rule_20260420.py`
- Iter 4 σ_ε × fabrication: `scratch/sigma_eps_fab_correlation_20260420.py`
- Iter 5 scale granularity: `scratch/sigma_eps_scale_granularity_20260420.py`
- Iter 4 tool-policy leakage: `/tmp/audit_zero_leakage.py` → `/tmp/audit_zero_leakage_results.json` (not in scratch — rerun if needed)
- Iter 3 specificity/hedge mediation: `/tmp/specificity_hedge_mediation.py` (not in scratch — rerun if needed)
- Iter 5 cross-pack validation: `/tmp/cross_pack_validation.py` (not in scratch — rerun if needed)

### `research/n1-memory-lab/AUTO_RESEARCH_LOOP_20260420.md` section anchors
- Iter 1: `## Binary useful-vs-fail inter-judge stability`, `## σ_ε flip structure in opus intra-rater`, `## Agreed-pass anchor cells`, `## Reduced-schema R² ablation`, `## Iteration 1 consolidation`
- Iter 2: `## Rulers-style extract-then-score sketch`, `## R13 anomaly dive`, `## Length × disagreement — mediation analysis`, `## Structural-bias anatomy + s_state operational definition`
- Iter 3: `## Specificity and hedge as mediators`, `## Retroactive s_state rule application`, `## Retrieval-degeneracy audit of agreed-pass anchors`, `## Code-gate D_t replay on 285 verdicts`, `## Iteration 3 consolidation`
- Iter 4: `## Judge-independent tip-anchor schema`, `## Fabrication density per (agent × condition)`, `## σ_ε × fabrication correlation`, `## Tool-policy leakage audit in zero-condition`, `## R08 mystery`
- Iter 5: `## Reward asymmetry — architectural ranking under contamination cleaning`, `## Cross-pack validation on older runs`, `## Scale granularity sanity — σ_ε under different scales`
