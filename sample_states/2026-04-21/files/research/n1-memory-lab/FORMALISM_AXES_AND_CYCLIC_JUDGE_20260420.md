# Formalism — Computational-Memory Axes + CyclicJudge

Status: working formalism. Not yet implemented. Ready for paper-grounded expansion.

Combines two tracks: (1) universal-scope computational-memory primitives as the measurement axes, (2) CyclicJudge as the judge-protocol that filters systematic bias from the scoring.

---

## 1. Measurement object

At reference time `t`:

- Hidden operative state `s_t` — user's actual live work state across all harnesses (never fully observable).
- Bounded observation packet `o_{≤t}` — fragmented multi-harness traces available by `t`.
- Agent reconstruction `r_t = A(o_{≤t}, question)` — the answer under evaluation.
- In-packet ground-truth surfaces: `slice/`, `local_git_anchor.json`, `slice_meta.json`.

The benchmark measures how `r_t` relates to `s_t` along computational-memory primitives, given only `o_{≤t}`.

---

## 2. Primitive axes

Cardinal scale, 1-5, required by the ANOVA decomposition.

### Universal primitives (every probe)

| symbol | primitive | measures |
|---|---|---|
| `P₁` | persistent-state fidelity | is `r_t` anchored to the right persistent operative state at `t` |
| `P₂` | belief updating under POMDP | does `r_t` reflect newest bounded evidence, not stale priors |
| `P₃` | temporal binding | are events/decisions/object-states correctly bound to their moments |
| `P₄` | state revision | are live-vs-stale distinctions correctly resolved |
| `P₅` | interference resistance | are similar/competing threads kept distinct |

### Conditional primitives (fire when ask-demand matrix flags)

| symbol | primitive | fires when |
|---|---|---|
| `C₁` | pattern completion | ask provides partial cue, needs continuation object reconstructed |
| `C₂` | pattern separation | ask is about multi-thread state with near-duplicates |
| `C₃` | consolidation quality | ask demands compression with retention of function |
| `C₄` | cross-surface binding | ask genuinely spans >1 harness/surface |
| `C₅` | provenance traceability | ask is audit-sensitive or explicitly asks "how do you know" |
| `C₆` | stability-plasticity balance | ask is change-history; system should reflect change without overwriting identity |

### Per-probe verdict

Non-compensatory aggregation. Hard gates (temporal boundedness on `P₃`, anchor-to-`t` on `P₁`) can veto. Otherwise weighted combination of primitive scores. Primitive vector reported before any pass/partial/fail collapse.

---

## 3. CyclicJudge applied

Specialized ANOVA model:

X_{ijkℓ} = μ_{P_k} + α_i + β_{ij} + γ_ℓ + ε_{ijkℓ}

- `i` = probe (R01..R24)
- `j` = agent generation (rep)
- `k` = primitive axis
- `ℓ` = judge identity
- `γ_ℓ` = fixed judge bias, centered: Σ_ℓ γ_ℓ = 0

Benchmark-mean variance:

Var(X̄) = σ_α²/n + σ_β²/(nm) + σ_ε²/(nmK) + (σ_γ²/K) · (K_tot − K)/(K_tot − 1)

At K = K_tot, the finite-population-correction vanishes. Systematic judge bias cancels exactly.

---

## 4. Concrete protocol

Judge pool (K_tot = 5):

| ℓ | judge |
|---|---|
| 1 | GPT-5.4-mini |
| 2 | Claude Opus 4.6 |
| 3 | Claude Sonnet 4.6 |
| 4 | Gemini 3 Flash |
| 5 | Qwen 2.5 72B / Llama 3.3 70B |

Design:
- n = 24 scenarios (canonical 15-day slice R01-R24)
- m = 5 agent generations per scenario (divisible by K_tot)
- Judge assignment: ℓ(j) = (j mod K_tot) + 1
- Per cell: 1 judge call (same unit cost as current single-judge)
- Per scenario: 5 judge calls total, one from each judge; systematic bias cancels exactly

Cost: n × m × K = 24 × 5 × 1 = 120 judge calls per condition. Same as current 5-rep setup, stronger guarantee.

---

## 5. Reporting

### Per primitive P_k

1. Grand mean μ̂_{P_k} with Var(X̄).
2. ANOVA F-test for judge main effect (F-stat + p-value). Large F + small p ⇒ primitive is judge-bias-loaded.
3. Variance components: σ̂_α² (probe difficulty), σ̂_β² (generation noise), σ̂_γ² (judge bias), σ̂_ε² (residual).
4. Self-preference matrix: X(agent=judge) − X(agent≠judge) on overlapping cells.

### Per probe i

Primitive vector (X̄_{i,P₁}, ..., X̄_{i,P₅}, [C_k active]), aggregated via non-compensatory rule into verdict interval, not point estimate.

### Per condition (pure / zero / syke)

Benchmark mean with confidence interval, tested against no-memory baseline, variance structure made explicit.

---

## 6. What this solves vs what remains

### Solved

- Judge bias: cancelled exactly at K = K_tot.
- Scope mismatch: conditional primitives fire only on probes that demand them.
- Noise attribution: verdict flip-rate decomposes into judge-bias / generation / probe-difficulty / residual.
- Verdict collapse: primitive vector reported before aggregation.
- 2026 judge-validity bar: per-primitive variance and F-test explicit.

### Not solved

- Residual noise σ̂_ε² — idiosyncratic per-cell disagreement stays. CyclicJudge averages systematic bias, not noise.
- Rubric calibration drift — CyclicJudge assumes scoring question is well-posed; can't fix malformed rubric.
- Real hidden-state access — we never see `s_t`; structural, not fixable.
- Cross-primitive independence — ANOVA assumes separability; primitives correlate (interference ↔ state revision). Paper's Limitations; GLMM more correct but loses closed-form.

---

## 7. One-line version

A memory system is scored at reference time `t` on a vector of universal + conditional computational-memory primitives, each primitive measured by a cyclic-rotated judge panel whose fixed bias cancels exactly, with variance decomposed into probe / generation / judge / residual components and reported per-primitive.

---

## 8. Immediate open questions

- **Rubric wording** for each P_k / C_k — what does a 1 vs 3 vs 5 concretely look like, with anchor examples from R01-R24?
- **Baseline set** — what's the no-memory null against which discriminative power is measured?
- **Conditional-primitive activation rule** — currently driven by ask-demand matrix; needs to be frozen before evaluation (not post hoc).
- **Judge pool size sensitivity** — is K_tot = 5 enough, or does adding Gemini 3 Pro / Llama 4 move the bias term measurably?
- **Per-primitive ε² floors** — what's the intrinsic residual noise on each primitive, and does it vary?

---

## 9. Sources

- [CyclicJudge](https://arxiv.org/abs/2603.01865) — ANOVA decomposition, cyclic rotation, FPC theorem
- [Bias-Bounded Evaluation](https://arxiv.org/abs/2603.05485) — formal guarantees under measurable bias
- [Self-Preference Bias in Rubric-Based Evaluation](https://arxiv.org/abs/2604.06996) — rubric alone doesn't remove bias
- [Imperfect Verifier is Good Enough](https://arxiv.org/abs/2604.07666) — noise-modeled imperfect verifiers
- [JUDGE_PRIMITIVES_NOTES_20260419.md](./JUDGE_PRIMITIVES_NOTES_20260419.md) — prior primitive proposal
- [NEURO_FOUNDATIONS_V1.md](./NEURO_FOUNDATIONS_V1.md) — computational-memory primitive derivation
- [ASK_PRESSURE_MATRIX_NE13_15D_20260419.md](./ASK_PRESSURE_MATRIX_NE13_15D_20260419.md) — conditional activation driver
