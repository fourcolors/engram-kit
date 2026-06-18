# Formalism — simplified after three-paper read

**Draft — user has not confirmed. Do not cite as settled.**

**Compiled 2026-04-22 late (~23:00-23:15), after a 20-min auto-loop reading Autorubric, Yeadon, Zhang directly from `/tmp/syke-paper-text/` and cross-reading with two parallel subagents. Follows Codex's formalism critique + the user's three-paper synthesis + the user's explicit directive: "keep it simple, do not complexify."**

## Headline

The current Math tab (v0.2.16) plus Codex's proposed 9-term variance model over-specifies what our n=109 data can support. Both subagents converged independently on the same cut: **drop λ_π, χ_{j,c}, and per-criterion `k` indexing on every term**. Collapse the 12 sub-axes to **3 axes × 3 sub-criteria = 9 criteria**, each with an explicit atomic/holistic flag. Treat CANNOT_ASSESS as first-class. Report per-criterion κ as a diagnostic, not as a variance term.

That is the whole structural change.

---

## 1. What we cut from Codex's proposal — and why

| Codex term | Status | Reason for cut / keep |
|---|---|---|
| `μ_k` | keep (global `μ`) | k-indexing adds noise without signal at n=109 |
| `τ_{c,k}` (condition effect per criterion) | **keep as `τ_c` only** | The condition IS the experiment. Load-bearing. But we cannot estimate τ_c × k interactions at current n. |
| `α_{q,k}` (probe variance) | keep as `α_q` | Standard G-theory. Blocked on more n before per-criterion split. |
| `(τα)_{q,c,k}` (probe×condition) | **drop** | Can't estimate stably at n=109. Lump into ε. |
| `β_{m,k}` (agent family) | keep as `β_m` | Load-bearing future term. Current n too low. |
| `δ_r` (generation replicate) | keep as spec, **pending data** | Blocked on JCB-030 fresh re-generations. |
| `λ_{π,q,c,k}` (packet/protocol effect) | **drop as variance term; treat as experimental condition** | Yeadon treats mark-scheme presence as an experimental condition, not a variance component. Zhang treats prompt variants as stability checks. Packet design is researcher-controlled — not a random effect. |
| `γ_{j,k}` (judge × criterion) | keep as `γ_j` only | σ_γ = +0.51 structural, locked. Per-criterion split overfits. |
| `χ_{j,c,k}` (judge × condition interaction) | **drop** | 2 judges × 3 conditions × 9 criteria = 54 parameters on 109 cells. CyclicJudge lumps all interactions into σ_ε; we do the same until n grows. |
| `ε` | keep | absorbs everything we dropped |

**Simplified variance model (replaces §M3):**

`y_{q,c,m,j} = μ + τ_c + α_q + β_m + γ_j + ε`

Five terms. Per-criterion κ is **reported** as a validity diagnostic (Autorubric's per-criterion κ), not fit as a variance component. When n grows (more probes + replicates), we can re-introduce the dropped terms one at a time with explicit power-per-parameter justification.

## 2. The 3×3 rubric skeleton — atomic/holistic split

Both subagents independently proposed the same ratio: **6 atomic / 3 holistic**, matching Autorubric's default rhythm. Specific proposal (subject to human sign-off on names):

### Axis A — Factual anchoring (3 atomic, binary)

The referenceable zone. These are plot-marking shaped (Yeadon): features in the packet can be verified by the judge.

- **A1. Named-entity recall** — did the agent reproduce specific files, projects, tools the user was in? Binary MET / UNMET.
- **A2. Timestamp / ordering correctness** — did the agent get dates, commit order, state transitions right? Binary.
- **A3. Artefact identifier accuracy** — commits, PR numbers, document titles. Binary.

*Per Autorubric CHARM-100: binary criteria reach κ = 0.642–0.679 at Default config. Target for us: κ ≥ 0.5 with stronger judges (opus, gpt-5.4).*

### Axis B — Causal reconstruction (2 ordinal atomic, 1 holistic)

The middle band. Ordinal with 3 levels and behavioral anchors per Autorubric §2.

- **B1. "Why is the user doing this?"** — 3-level ordinal: {miss / partial / correct}. Atomic.
- **B2. "What's the open decision?"** — 3-level ordinal. Atomic.
- **B3. Internal consistency** (holistic) — does the reconstruction hang together? Single LLM call evaluates the whole answer.

*Per Autorubric CHARM-100 ordinal: 38–58% exact, 85–93% adjacent, quadratic-weighted κ 0.549–0.719. Adjacent accuracy is the primary metric, not exact.*

### Axis C — Completeness (1 atomic, 2 holistic)

**The Zhang-critical axis.** Self-decomposing atomic judges fail here (−14.5 to −33.0pp on `partially_supported`). The fix is holistic completeness + one enumerable atomic check.

- **C1. Enumerable-thread coverage** (atomic, binary) — "did the reconstruction mention every load-bearing thread that was evidenced in the packet?" This is the QAMPARI-style atomic where atomic actually works.
- **C2. Global-omission / completeness** (holistic) — Zhang's "does it miss a load-bearing thread" call. Must be holistic per Zhang §4.
- **C3. User-recognition** (holistic) — "would the user recognize this as their day?" This is Yeadon's essay wall proxy; we tolerate low ρ here, but it's worth measuring.

### Negative-weight penalty (Autorubric Eq 1)

- **P. Fabrication penalty** (holistic, negative weight) — fires when the answer asserts something not in the packet. Autorubric Eq 1 excludes negative weights from the denominator, so clean responses score 1 even with this criterion dormant.

**Total: 9 sub-criteria + 1 penalty. 6 atomic / 3 holistic + 1 holistic penalty.**

## 3. Typed CANNOT_ASSESS (first-class)

Per Autorubric, `⊥` is a native verdict. Per Codex's extension, typed:

- `INSUFFICIENT_PACKET` — evidence not in the packet (zero-condition default).
- `NOT_REFERENCEABLE` — criterion-referenceability per Yeadon is low for this criterion × cell.
- `AMBIGUOUS_TIME` — reference time anchor is unclear.
- `OUT_OF_SCOPE` — criterion doesn't apply to this probe type.
- `JUDGE_UNCERTAIN` — genuine uncertainty despite evidence.

Under §M4b (new), scores are reported as intervals [S_min, S_max] when CANNOT_ASSESS fires, plus coverage ratio. No silent skip that inflates scores.

## 4. Where our task sits (confirmed from data)

- **310-ask corpus: 117 hard_only (37.7%), 11 semantic_only (3.5%), rest mixed.** Most of our task is middle-band ResearcherBench territory, not essay territory.
- **19-probe set: 6 high / 9 medium / 4 low referenceability** — already tagged in `probe_metadata.json` (unplumbed to the judge).
- **R08, R11, R13, R18 are low-referenceability** — Yeadon essay territory. They produce distributional noise regardless of rubric. R08 pooled mean 0.38 is the lowest probe — exact Yeadon essay signature.
- **All disputed cells in our 30-cell triage are Zhang's `partially_supported` class** — locally true, globally incomplete. σ_γ = +0.51 is exactly this disagreement mechanism.

## 5. The ask-sampling gap list (concrete, from `ASK_SAMPLING_20260421.md`)

The 19-probe set skews **73.7% toward 0-1 handle asks** vs 32.2% in the corpus. High-handle (artifact-rich) asks are under-represented.

**Missing demand-tags in R01-R19:** `META_HANDOFF`, `CONFIG_CHECK`, `GAP_ANALYSIS`, `DOC_SYNTH`, `PROVENANCE_AUDIT`.

**Priority gaps for probe expansion:**
- `DOC_SYNTH` shape: "Read X, then answer Y" — 0/19 coverage, ~15 corpus hits.
- `GAP_ANALYSIS` / pattern-discovery: "what is still missing / what patterns have I not seen" — 0/19 coverage, ~6 corpus hits, highly recurrent in late-window asks.
- **High-handle referenceable asks** to exercise Axis A — closing the handle-density skew.
- Paired-time asks (same question revisited at t and t+Δ) — enables continuity axis that currently has 0 probe coverage.
- Budget-framed asks ("quickly", "don't read everything") — enables efficiency-personal.
- "Forget X, focus on Y" instruction-taking — 0 current coverage.

**Asks we already have that stress-test Axis C (completeness):**
- R08, R09, R19 already expose global-omission failures (the partially_supported zone).

## 6. The n=1 narrative — three concrete failure modes from our actual data

These are detectable *only* because of longitudinal single-user context. A cross-population benchmark structurally cannot test them:

1. **R08/zero meta-vs-work mismatch** — agent reported DB/adapter state instead of the user's actual March 14 work (observe subsystem dev, stash-pop forensics, health.py staged). "Wrong world-model" only identifiable because we know *this user's* actual March 14 trajectory.

2. **R19 Syke-cleanup vs LM-Studio thread fork** — both threads are true; which counts as "the real last thing" depends on what the user cares about. Opus picks LM Studio; GPT rejects it as stale. No external ground truth — only the user's own sense of their trajectory. This is σ_γ being structural, not judge-model preference.

3. **R09 fabricated UUIDs / thread links** — the only way to detect fabrication is against *this user's* actual memex. A generic plausibility judge would accept the invented UUIDs because they look right.

## 7. The feedback loop, concretely mapped

1. **Real data** — the existing 19 probes × 3 conditions × 2 agents × 2 judges tensor (228 cells, 224 valid). Lives in `results/`.
2. **Packet design** — wire `probe_metadata.json` into the judge packet (target_slice, referenceability, probe_type are already tagged and currently invisible to the judge). Bound cumulative slice (R18/R19 see 28× R01's files).
3. **Rubric design** — the 3×3 skeleton above. Human names axes + weights + penalty signs + 5-shot calibration examples. Agent drafts sub-criterion wording + atomic/holistic flag proposals under typed failure feedback.
4. **Test** — run on 30-cell calibration subset (already prepared). Compute: schematic R², factor-collapse correlation matrix, Autorubric per-criterion κ, 4-category disagreement typology on top-10 disagreement cells.
5. **Loop terminates** on: all three diagnostics pass (R² distributed / max ρ < 0.85 / per-criterion κ ≥ 0.4) — promote; OR typed rejection (criterion is low-referenceability per Yeadon → drop or flag as CANNOT_ASSESS default).

Budget: 3-4 revision rounds before rejecting a candidate rubric.

## 8. The open experiment — paper-abstract sentence

Zhang explicitly says (2603.28005, lines 88, 100, 184, 517, 552, 570): "atomic pipelines with externally supplied decompositions or multi-stage extract-then-verify [...] remain untested." Yeadon confirms essays are a wall. Autorubric achieves κ ≥ 0.64 on referenceable binary tasks.

**The untested question Syke's rubric-v2 answers:**

> "For a task between plot-marking and essay-marking — reconstructing an individual's live working state from bounded evidence — does a designer-time atomic rubric over referenceable sub-criteria, combined with a holistic shell for global-omission detection and a negative-weight fabrication penalty, recover per-criterion κ ≥ 0.5 under a locked judge-bias σ_γ that pure holistic rubrics cannot?"

That's a falsifiable n=1 result and a paper abstract in one sentence.

## 9. The one simplification to bet on

If we pick one thing: **collapse 12 sub-axes to 3 axes × 3 sub-criteria with explicit atomic/holistic flag per criterion + CANNOT_ASSESS first-class.**

Argument: our current diagnosis is "one axis eats 73% of R²." That is not a 12-axis rubric; it is a 1-axis rubric with 11 noise carriers. Refining the noise carriers with weights and calibration examples gives precisely-calibrated numbers on a biased latent — §08's "scariest failure mode." Going FEWER axes with explicit typing is the structural fix Zhang + Autorubric + Yeadon collectively endorse.

## 10. Smallest next move (sequenced)

**Tonight / tomorrow (15 min, user):**
- Do ζ — hand-classify R08/zero as "answer quality" vs "rubric ambiguity under zero packet." Decides whether the 4-category triage typology holds.

**This week (2-3 hours, user + agent):**
- Hand-score 10 existing transcripts on the 6 proposed **atomic** sub-criteria (A1, A2, A3, B1, B2, C1). Compute per-criterion κ against both judges.
- If κ on the 4 binary criteria (A1-A3, C1) is ≥ 0.5, the split is right and we proceed to rubric-v2 drafting.
- If κ < 0.5, the criterion definitions need reworking before any code.
- This is the minimum viable test of the whole proposed formalism.

**Next session (1-2 hours, agent):**
- Draft the 6 atomic criteria as Autorubric-shaped binary/ordinal prompts.
- Draft the 3 holistic criteria + 1 penalty as holistic Zhang-safe prompts.
- Draft 3-shot verdict-balanced calibration examples per criterion (user sign-off required).

**When all three Feuer diagnostics pass on rubric-v2:**
- Promote. Only then is architecture ranking on the table.

---

## What this supersedes

- §M3 variance model in the Math tab (v0.2.16): replace 4-term with this 5-term, drop per-criterion indexing.
- Codex's 9-term proposal: specified which terms we cut and why.
- The implicit assumption that 12 sub-axes with refinement will pass validity: rejected. Three axes is the move.

## What remains open (honest gaps)

- **Per-criterion κ** still unmeasured. The hand-score this week is the first measurement.
- **σ_α, σ_β** still unmeasured. Need more probes + fresh re-generations.
- **Packet hygiene** (bound slice, wire probe_metadata.json, identity-mask) still partially done.
- **Few-shot calibration** — biggest single Autorubric mitigation (for strong judges: +1-4pp; for weak: +15pp). Not yet tried.

## What this file is not

- Not a commit to the 3-axis names or weights — those are user decisions.
- Not an edit to the Math tab — that happens after user sign-off on the simplification.
- Not a plan expansion — the four-line plan stays at four lines.

## Future-Claude binding

Before citing any claim in this file as settled, re-read the header. This is the post-three-paper-read simplification proposal. Pending user sign-off before any HTML or code change.
