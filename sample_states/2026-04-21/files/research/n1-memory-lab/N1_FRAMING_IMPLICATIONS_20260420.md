# N=1 Framing Implications — 2026-04-20

Status: design-layer reflection on the 5-iteration loop. Not a re-summary of findings.
Scope: what the iterations say about the **environment formalism** (`I_t = (t, q_t, E_t, r_t)`, latent `s_t`), not about the judge.
Companion to: `FORMALISM_LAYER_SEPARATION_20260420.md` (layer split) and `COUNCIL_FORMALISM_20260420.md` (frozen benchmark object).

Thesis in one line: the council formalism under-specified the environment in four places, and the iterations expose each of them as a different failure mode. The n=1 memory claim survives, but only for a narrower slice of the probe space than NE-1.3 currently contains.

Positions taken below are stated without hedging. Where a section ends with a design move, it is a re-definition of the environment or probe schema, not a request for more runs. More runs on the current packet cannot resolve any of these — each pathology is a property of how the packet was constructed.

---

## 1. `E_t` is not bounded — the operational packet is the filesystem

### Finding

Tool-policy leakage audit (iteration 4): 32 of 38 `zero`-condition cells issued at least one `rg`/`cat`/`read` directly against the slice filesystem. 469 slice-directed calls across the audit. Every non-leaking cell failed; every high-verdict cell rode on ≥17 slice calls. The `zero` workspace is MEMEX-injected but the harness never sandboxed the slice path, so the agent's effective evidence surface is MEMEX ∪ `slices/**` in every condition. R15/zero reached its load-bearing figures (`546 passed`, `128,902 total events`) via three `rg` calls into `harnesses/**/*.jsonl`, not from memory.

### Environment-level implication

`E_t` as written — "bounded evidence packet available by `t`" — is a **policy claim**, not a property of the packet. The formalism implicitly assumed `E_t` is set-valued and enumerable; in practice it's whatever the agent successfully reads before returning `r_t`, which is a function of its tool policy at inference time. That collapses the partial-observability framing: `s_t` is not hidden from the agent — it's hidden from the *intended control condition*. The agent restores full observability on demand. What we called a POMDP is, at the agent's option, a fully observed MDP with a small behavioral prior nudging it toward MEMEX.

This is worse than a sandbox leak. It means the formal `E_t` and the operational `E_t` are **not the same type of object**. The formal one is a projection the experimenter defines. The operational one is a trajectory the agent *chooses* inside a permissive tool surface. The latter is what the judge scores. So the partial-observability claim, as currently implemented, is **unfalsifiable**: there is no condition in the packet that actually realizes it.

### Next design move

Stop defining `E_t` by MEMEX content. Define it by **filesystem-level read receipts**: `E_t = {f : agent opened f with a read-type tool during ask execution} ∪ MEMEX_projection`. Record this at runtime. Then a condition is not "MEMEX-only" (a prompt claim) but "MEMEX ∪ agent's actual read-set, where the read-set is empty" (an enforced invariant). Concretely, wrap the harness in a read sandbox whose allowlist is `{MEMEX_dir}` for zero, `{MEMEX_dir, syke.db}` for syke, `{slice/**}` for pure, `{slice/**, syke.db}` for production. Reject and requeue any cell whose trace shows out-of-allowlist reads. This makes `E_t` a **post-hoc observable**, which is what the formalism always quietly assumed.

The deeper move is to stop treating `E_t` as an input to the agent at all. It's an output of the agent's tool-policy given a permissive environment. The formal object the experimenter actually controls is the **allowlist** `A_t ⊆ Filesystem`; the object the judge scores against is the **used-set** `U_t ⊆ A_t`; the partial-observability claim lives in the difference `A_t \ U_t`. Under that redefinition, a `zero` cell where the agent leaked is not invalid — it is a cell whose `U_t` exceeded the intended `A_t`, and the allowlist shape was wrong. Both types of facts are recoverable from the trace.

---

## 2. For retrieval-degenerate probes, the task is `grep`, not memory

### Finding

Retrieval-degeneracy audit (iteration 3) on the 9 agreed-pass cells: every load-bearing phrase in the answer appeared ≥46 times (often >200, max 1497) in the slice. Drop cells where any load-bearing phrase >50 hits and agreed-pass falls from n=9 → n=0. Separately, R08 is the only probe whose prompt (`okay where are we now`) provides no entity to grep, and it is the only probe where both agents stayed tool-obedient in zero.

### Environment-level implication

For a probe to test memory in the POMDP sense, the answer must be **reconstructively cheaper than retrieval** from `E_t` at the limit of `E_t` that we actually permit. If the load-bearing claims are copy-pastable from the slice in a five-line grep, then the optimal policy is retrieval, not reconstruction — and measuring memory on that probe is measuring search quality. The task label `memory` doesn't hold; it's just an information-retrieval benchmark with a thematic prompt.

This matters more than it first appears. Under the council formalism, `s_t` is the latent operative state. If every load-bearing piece of `s_t` has a stable surface realization in `E_t` that survives a trivial keyword lookup, then `s_t` is not actually latent with respect to the agent — it's latent only with respect to a hypothetical constrained agent we never instantiate. The "reconstruction of the closest correct operative state" claim is only meaningful for probes where the gap between retrieved text and the operative state is **substantive**: where what sits in the slice is raw, contradictory, or non-load-bearing, and the work of composing an answer is the thing being evaluated.

### Next design move

Reclassify probes into two environment-types and keep them separate: **search probes** (answer has a canonical surface phrase appearing densely in the slice; success = retrieve + cite) and **reconstruction probes** (answer requires disambiguating contradictory traces, synthesizing across sessions, or naming state that has no canonical surface string). A precondition for admitting a probe to the reconstruction class: run the same phrase-density check used in iteration 3 before the eval, auto-flag any load-bearing phrase >50 hits, and either rewrite the probe or route it to the search set. NE-1.3 as it stands is roughly 70% search, 30% reconstruction; the n=1 memory claim should only draw on the reconstruction slice.

---

## 3. There is no single `s_t` — there are at least two

### Finding

Structural-bias anatomy (iteration 2): on the three full-band opus=pass/gpt=fail cells, gpt-judge's operative-state reading is "latest unresolved observation in the freshest surface" (the tip); opus-judge's reading is "latest committed/verifiable artifact + the landscape around it." Both are internally coherent and defensible. They disagree on which surface is canonical (open issues vs committed artifacts) and on how freshness is measured (unresolved state vs closed artifact). The iteration-3 retroactive tip-anchor rule (tip gates, landscape differentiates) resolves R03 and R05 in gpt-judge's direction but leaves R19 under-determined.

### Environment-level implication

The formalism treats `s_t` as a single latent. The iterations show it isn't. At any reference time, there are at least two distinct operative-state readings for the same user:

1. **Tip state**: "what is in flight, unresolved, currently being touched." Pointer into the open set.
2. **Landscape state**: "what is the committed, verifiable frame within which the tip lives." Snapshot of the closed set.

These are not noise around a single ground truth; they are two different ground truths, and the prompt does not always specify which is being asked for. A judge (or agent) picks one implicitly via a prior about what "operative" means. When priors differ, verdicts diverge — not because the judge is noisy but because the **task is underspecified at the level of `s_t`**.

This breaks the POMDP framing cleanly. Standard POMDPs have one latent; observation models differ but the belief distribution converges on the same hidden state as `t → ∞`. Here, two agents with identical observations of `E_t` can reach two stable, non-converging readings of `s_t`, because `s_t` is not one object. The formalism needs to index: `s_t^tip` and `s_t^landscape`, each with its own reconstruction target.

### Next design move

Make the probe schema declare a `target_slice ∈ {tip, landscape, both}` field, required. A probe with `target_slice = tip` has its answer graded against the most-recent-unresolved anchor only; `landscape` grades against the frame; `both` requires tip-as-gate + landscape-as-differentiator (the iteration-3 rule). Surface-agnostic prompts like R19 are rewritten or split into a tip-version and a landscape-version. The judge no longer has to guess which reading `q_t` wants; the probe spec commits to one. This doesn't resolve all `s_t` ambiguity, but it collapses the two coexisting latents into an indexed pair the judge can score separately.

---

## 4. R08 is the probe family — `q_t` must be under-specified on retrieval handles

### Finding

R08 (`okay where are we now`, 4 words) is un-fakeable because the prompt names no entity: zero tool-calls in `zero` mode because there is nothing to grep. It is also the only probe where both agents stay MEMEX-obedient. It is simultaneously rubric-ambiguous — opus-judge's intra-rater sequence on R08/pure is `fail/fail/partial/fail`. The answer text is stable across reps; the verdict drifts because the judge cannot resolve referent (memory-system vs user live work) or completeness bar.

### Environment-level implication

R08 is the only cell in NE-1.3 where the operational and formal `E_t` converge — the agent genuinely works from memory because retrieval buys nothing. That contradicts the council formalism's implicit assumption that `q_t` is arbitrary (any plausible user ask). Actually, for the environment to realize its partial-observability premise, `q_t` must be **deliberately under-specified on retrieval handles**: no named artifact, no named thread, no time window, no deliverable. The moment the probe gives any of those, the agent's rational move is to `rg` for it, and we fall back to the failure mode of section 1.

This is a design principle, not an alignment problem: "ask what the user would ask" and "ask what the agent can't fake" are two different design goals, and the current NE-1.3 set mixes them. Most probes chase realism and in doing so give the agent enough handles that the retrieval shortcut dominates. R08 chases un-fakeability and in doing so produces the one honest measurement of reconstruction, at the cost of rubric ambiguity the judge has no hope of resolving consistently.

### Next design move

Build a probe family **R08-type**: prompts stripped of named entities, times, threads, or deliverables. Accept that these will be rubric-ambiguous and offset that by pairing each R08-type prompt with an **experimenter-authored reference state** — a short text the experimenter commits *before* seeing any agent output, naming the tip + one level of landscape at time `t`. Score the agent's answer against that reference text via constrained edit distance on named-entity sets, not via an open judge. This makes un-fakeability and rubric-stability compatible by moving the ground truth outside the agent's evidence surface. The realism loss (users *do* ask specific questions) is real; absorb it by running R08-types as the reconstruction benchmark and the named-entity probes as the search benchmark, and stop averaging them.

The design principle worth promoting: **probe-handle parsimony**. `q_t` should contain exactly as many retrieval handles as the experimenter wants the agent to use, and no more. A probe with zero handles measures reconstruction; a probe with one handle (a named artifact) measures targeted retrieval; a probe with several handles measures synthesis over known targets. Each of these is a different task, and the environment formalism should index them — not hide them under a single `q_t`. The current NE-1.3 set has probes ranging from one handle (R01, R18) to seven (R05), graded with the same rubric and reported under one heading.

---

## 5. `state_transition_tracking` is not a primitive — it's a correlation trap

### Finding

Reduced-schema R² ablation (iteration 1): `state_transition_tracking` alone reaches R²=0.606 (gpt-judge) / R²=0.731 (opus-judge) against the 12-axis verdict. It is load-bearing in every rubric fit both judges produce. When an opus verdict flips, `state_transition_tracking` flips 15/19 times — the highest of any sub-axis.

### Environment-level implication

Three hypotheses, ordered most to least flattering:

- **(a) Rubric artifact.** The 12-axis schema was authored with a narrative theory where state-transition *is* the supervisory axis, and the judge prompt reflects that; the other axes are differentially-weighted skins. R² is high because the judge implicitly defines the verdict as a threshold on this axis. Evidence for: the 12-axis adj-R² actually improves under pruning for opus; the lockstep flip pattern (iteration 1) where nearly all sub-axes move together when the verdict moves.
- **(b) Genuine primitive.** n=1 memory over time is fundamentally about *tracking what changed between `t-1` and `t`*; other axes (grounding, salience, boundedness) are downstream. Evidence for: the load-bearing status replicates across both judges with different axis preferences, which is not what you'd expect from pure rubric artifact; the cross-pack validation finding (iteration 5) that R14/R07/R08 always-flip replicates on ab07 suggests the underlying signal is stable.
- **(c) Accidental operationalization overlap.** Both judges happen to operationalize "did the answer track the transition" as "did it name the right tip + mention the right prior state," which is close to what passes as a pass/fail decision anyway. The correlation is high because both paths compute approximately the same thing, not because the thing is primitive.

The iterations cannot distinguish these. But (a) and (c) are both rubric-internal; only (b) is an environment claim. Treating `state_transition_tracking` as a primitive right now is premature — the environment formalism doesn't license it, and a simpler schema might reveal it as one of two or three equally-good collapses of the same coarse verdict.

### Next design move

Run the ablation in reverse: **drop** `state_transition_tracking` from the rubric and see if the remaining 11 axes re-assemble a comparably good predictor from a different primitive. If yes, then (a)/(c) dominate — the axis is absorbing variance that lives elsewhere. If no (R² collapses below ~0.4), then (b) has real support and the environment formalism should index `s_t` transitions explicitly, e.g., `s_t = (s_t^static, Δ(s_{t-1} → s_t))` with the delta as a scored object. Either outcome tightens the story; the current "it's load-bearing, we don't know why" is the worst resting place.

A stronger falsifier: take two probes matched on every other rubric axis and differing only in whether the correct answer requires naming a state transition. If state-transition probes show the same verdict spread as the non-transition probes after controlling for length and artifact density, the axis is a rubric artifact. If they don't, the axis is tracking a real environmental property. NE-1.3 does not currently support this split, but a small follow-on probe set could.

---

## 6. What survives the packet, and what doesn't

### Finding (summary across iterations)

- Agreed-pass anchor cells after degeneracy audit: **n=0**.
- `zero` as a memory-only control: **invalid** (84% leakage).
- Architectural ranking of `production` vs `pure` vs `zero` on the current corpus: **unsupported** at n=0 surviving agreed-pass.
- `state_transition_tracking` as a load-bearing axis: **holds**, cause unknown.
- R08 as the cleanest diagnostic probe: **holds**, but only one probe.
- Tip-vs-landscape as a real structural disagreement (not judge noise): **holds**.
- Judge-identity as a first-order confound: **holds**.
- Cross-pack replication of always-flip probe set (R07/R08/R14): **partial** (replicates on ab07 at probe level, not at cell level).

### What is defensible to claim about n=1 memory from this packet

Three things, narrowly:

1. **The n=1 memory problem has at least two coexisting latent states** (tip, landscape) and the probe must commit to which one it targets. This is a structural claim about the task, not about any architecture.
2. **On under-specified prompts (R08-type), architectures have no retrieval shortcut and genuinely diverge on their ability to reconstruct from MEMEX-equivalent state.** This is a single-probe result; it justifies expanding the R08-type family but does not yet rank architectures.
3. **On handle-rich prompts, the architecture comparison collapses into a retrieval quality comparison**, and "which MEMEX" matters less than "which retrieval policy the agent runs at ask time." The environment conflates these in NE-1.3.

### What must be deferred until the environment is tightened

Everything else. Specifically:

- Any claim about `production` > `pure` > `zero` or any permutation of condition ranking. The zero leakage plus the retrieval-degenerate agreed-pass set together invalidate the current 2×2.
- Any claim that a specific rubric primitive (transition tracking, thread selection, etc.) is a *memory* primitive rather than a *rubric* primitive. The R² ablation has not been inverted.
- Any psychometric claim about σ_ε or inter-judge κ as a property of the memory task. These are properties of the measurement, and the iteration-1 separation note already says this — but we should stop reporting them under memory-claim headers.
- Any architecture ranking at all from NE-1.3 as it stands. The one honest ranking would need: (i) sandboxed `E_t`, (ii) reconstruction-only probe subset, (iii) declared `target_slice`. None of the three hold in the current packet.

### Net

The n=1 memory problem is **real**, but the current packet measures a blend of search, reconstruction, judge priors, and tool-policy slippage, with the first and the last dominating. The environment formalism — as an object worth pursuing — is fine. The environment **realization** in NE-1.3 is not. The fix is upstream of the judge: define `E_t` as a post-hoc observable, partition probes by target slice, build the R08-type family, and only then return to architecture ranking.

The productive framing shift: stop treating the current packet as a benchmark-in-progress that needs more judge calibration, and start treating it as a **diagnostic probe of the environment formalism itself**. Every iteration in the 5-iteration loop found a way the formalism's assumptions broke against the data. That's not failure; that's the work. Tightening the environment is the prerequisite for any memory claim, and the iterations have now enumerated what tightening means: sandbox the filesystem, partition probe types, declare target slices, invert the R² ablation. Do those four things and the n=1 claim has a shot. Skip them and the next packet will reproduce the same four pathologies in a slightly different arrangement.
