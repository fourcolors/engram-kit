# Evidence-Packet Lens — What the Judge Actually Sees, vs What We Think We Asked

> **2026-04-21 update:** the user has retired the 9-primitive set from
> `JUDGE_DESIGN_LITERATURE_MAP §4` and also the per-probe `expected_primitives` idea I
> proposed in §7. Same rubric across all probes is the new constraint. §7 items 3 and 4
> are **obsolete**. Items 1 (strip condition leak) and 2 (per-probe `target_slice`) still
> stand. Rubric redesign will start from the data, not from this proposal.

Status: diagnostic memo, 2026-04-21.
Prompt: "look at existing assumptions and math and rubric design from the lens of (what are we even presenting as evidence to the judge)."
Scope: read the actual judge prompt path (`benchmark_runner.py:954–1006`, `_build_judge_brief` at 666–686, `_build_real_ask_packet` at 689–728, JUDGE_SCHEMA at 60–135). Everything below is traceable to those lines.

---

## 1. The judge's full input surface, enumerated

1. **System prompt** (`_build_judge_prompt`, ~50 lines). Fixed across all probes. Tells the judge: you're verifying a memory system's answer; read `packet.json`, `slice/`, `local_git_anchor.json`; use bash/sqlite3/grep to verify; score three axes; efficiency is out of scope; fill every subcategory.
2. **`packet.json`** — the per-probe object:
   - `probe`: probe_id, question, family, reference_dt, reference_ts_local, reference_cutoff_iso, source_surface, source_ref.
   - `answer`: text + metadata (tool_calls, cost, duration, tokens).
   - `raw_context`: slice_dir path, slice_summary (sources with jsonl_files/lines/db_rows), replay_state (condition, ask_mode, memex_chars).
   - `local_git_set`: {available, path}.
   - `judge_brief`: **identical boilerplate for every probe** — generic `object`, `useful_means`, `partial_means`, `fail_means` arrays.
3. **Filesystem:** `./slice/` (same data the agent used — Codex JSONL, opencode.db, adapter markdowns) + `local_git_anchor.json` (time-contained git truth).
4. **Output schema:** `factual_grounding` + `continuity` + `coherence`, each with 3–5 subcategories scored `strong / partial / missed`, plus `overall_verdict` (pass/partial/fail) and `summary`.

## 2. What is NOT in the judge's input (and probably should be)

1. **Per-probe target-slice hint.** Nothing in the packet tells the judge whether this ask targets tip state, landscape state, or both. The judge resolves it implicitly — and we have measured the result: `σ_γ = +0.49` opus-over-gpt, driven by the `active_thread_selection` sub-axis, because the two judges pick different priors when the target is unspecified.
2. **Per-probe criterion-referenceability.** No per-claim metadata saying which parts of the expected answer are hard-verifiable (`d_time`, `d_artifact`, `d_committed`) vs semantic. The judge has to decide this on the fly per claim, inconsistently across judges.
3. **Claim-typing structure in the answer.** The answer is one prose blob. There's no `verified | inferred | speculative` split. So every claim is graded on the same rubric regardless of whether it's grep-verifiable or narratively inferred.
4. **Explicit index of the slice.** `slice_summary` gives counts, not structure. The judge doesn't know what's in the slice until it issues grep/cat/sqlite calls — which makes its scoring tool-policy-dependent.
5. **Baseline expectation for "good."** The `useful_means` list is generic. There's no per-probe "a good answer should name X, and may omit Y." Without that, "strong" vs "partial" is a judge-prior.
6. **A per-probe expected-primitive-set.** The project's own literature map (`JUDGE_DESIGN_LITERATURE_MAP §4`) defines universal primitives (`bounded_support`, `time_local_correctness`, `operative_state_adequacy`, `wrong_restart_risk`) and conditional primitives (`enumeration_completeness`, `cross_surface_integration`, `committed_state_fidelity`, `object_continuity`, `provenance_traceability`). **None** of these appear in the judge prompt or the packet. The 3-axis × 12-subcategory rubric is a different ontology than the project's stated primitive set.

## 3. What IS in the judge's input that shouldn't be (and why)

1. **`replay_state.condition`** — the judge is told whether the probe ran under `production`, `pure`, or `zero`. **This is a condition-identity leak.** Any prior the judge has about condition ordering enters the verdict. Standard experimental practice in blind evaluation is to strip condition identity. This should be removed or masked.
2. **Full filesystem access to `./slice/`.** The judge has bash/grep over the same raw harness data the agent read. This turns the judge into a secondary retrieval agent — and its verdicts become tool-policy-dependent. It also is exactly why retrieval-degenerate probes score inconsistently: the judge can re-grep the load-bearing phrase and then grade "support" based on whether the phrase exists in the slice, which is a grep test, not an answer-quality test.

## 4. The causal chain from packet design to measured noise

This is the part that matters. The four noise sources we've been labelling as instrument problems are **consequences of the packet design**, not just stochasticity of the LLM:

- **`σ_γ` (cross-judge bias, +0.49).** Comes from §2.1: packet does not disambiguate tip vs landscape. Two judges resolve the ambiguity from different priors. **Fix: add `target_slice` to the packet per-probe.**
- **`σ_ε` (judge-flicker, 0.33 pooled / 0.19 cell).** Comes from §2.5: the `useful_means` list is generic, so the judge uses its own prior on "what counts as strong" per cell. Short answers amplify this because there's less text to pin the prior. **Fix: per-probe expected-primitive-set or anchor examples.**
- **`σ_α` confound (retrieval-degenerate probes).** Comes from §3.2: the judge has full grep access to the slice, so on R13/R11/R04 it can re-verify by phrase-existence, which is retrieval, not reconstruction judgment. **Fix: restrict the judge's tool surface, or mark probes search-like and score them on a separate track.**
- **Rubric over-specification (R² of one axis = 0.73).** Comes from §1.1: the `judge_brief.useful_means` list — "re-enter the right live thread," "identify what changed and what is still live," "surface the right artifact or restart path" — is dominated by **state-transition-tracking language**. The judge is reading a brief that already encodes one latent, so all 12 subcategories correlate with that latent. **Fix: rewrite the brief around the project's actual primitive set, not around narrative flow.**

**The math isn't wrong.** The math is measuring exactly what the packet design produces. If you change the packet, the math will change — but so will what it's measuring. The order of operations is: **fix the evidence packet first, then remeasure the noise.**

## 5. What the three-axis rubric is and isn't measuring, given the packet

Given what actually gets fed in:

- **`factual_grounding` (3 sub).** Should be the hard-verifiable axis. **Actually measures:** "did claims the judge chose to spot-check exist in the slice." The judge picks which claims to check; different judges pick differently. This is also where `boundedness` lives (did the answer stay within the packet's time window) — which is a `d_time` check that could be a deterministic pre-filter, not an LLM judgment.
- **`continuity` (5 sub).** Supposed to measure state-transition tracking. **Actually measures:** the `useful_means` list translated into ordinal scores. Since the useful_means list is state-transition-flavored, this axis inevitably eats most of the R² — and its 5 subcategories move in lockstep (measured).
- **`coherence` (4 sub).** Cross-source, cross-session, artifact routing, contradiction handling. **Actually measures:** whatever the judge decides "coherent" means at the time of scoring. Lowest criterion-referenceability of the three, highest flicker susceptibility.

The project already has a cleaner primitive set written down (`JUDGE_DESIGN_LITERATURE_MAP §4`). The deployed rubric is not that set.

## 6. Implications for "does a new judge category make sense"

You asked how we'd know. The lens says: **a new judge category is legitimate if, and only if, the evidence packet contains something the current packet doesn't that the category can score against.** Otherwise it's just a re-partition of the same latent the existing rubric already eats.

Concretely:

- **Continuity as a new cross-session category.** Requires packet-level evidence that the current packet does not carry: pairs of asks at different times referencing the same state. Without that, continuity stays a within-answer rubric axis, not a memory-system property.
- **Efficiency as a judged category.** Requires a reference cost baseline inside the packet — what a "carry-everything" system would cost on this ask. Without that, efficiency stays a runner-metadata report, not a judgment.
- **Restart-safety / wrong-restart-risk as a category.** Requires a reference "if the user resumed from this answer, would they re-do or miss work?" ground-truth. This might be derivable from the slice at `t+Δ`, but no such field exists today.
- **Construct-validity claim typing (`verified | inferred | speculative`).** The cheapest of the four — requires pre-judge claim extraction, not new packet evidence. Adoptable now; the rest require packet schema changes.

## 7. The minimum set of packet-schema changes to make a new judge category testable

In rough priority order:

1. **Strip `replay_state.condition` from the judge input.** Remove the condition-identity leak. One-line change, immediate signal.
2. **Add `target_slice ∈ {tip, landscape, both, historical}` per probe** (Codex already proposed this; not yet wired).
3. **Add per-probe `expected_primitives` list** drawn from `JUDGE_DESIGN_LITERATURE_MAP §4` universal + conditional set. This replaces the generic `useful_means` for that probe.
4. **Add per-probe `hard_verifiable_claims` list** — the subset of expected content that can be checked by `d_time` / `d_artifact` / `d_committed` gates before the LLM judge runs.
5. **Add answer-side claim extraction** (Autorubric / FActScore pattern) — a pre-judge stage that splits `answer.text` into (verified | inferred | speculative) claim lists. Each claim typed is scored on its own track.
6. **Restrict judge tool surface on retrieval-degenerate probes** — flag probes with phrase-density > 50 in slice and score them on a "search-like" track with deterministic gates only, not LLM judgment.
7. **(Later) Add a `continuity_pair` schema** to link ask at `t₁` to a follow-up ask at `t₂` on the same state. Requires corpus work, not just schema.

Items 1–4 are schema-only and reversible — they can be added to the packet without new runs. Items 5–6 are judge-pipeline changes. Item 7 is a corpus-design change.

## 8. What this memo does NOT do

- Does not propose a specific rubric-v2. User explicitly declined that.
- Does not propose a specific Autorubric adoption plan — separate review is running.
- Does not propose new ask samples — separate review is running.
- Does not recommend running anything. It recommends **reading the current instrument as a packet-design artifact**, because the math we've been arguing about is a consequence of that design and will keep looking the same until the design changes.

## 9. One-sentence summary

The judge is being asked to score a 3-axis × 12-subcategory ordinal rubric over a packet whose `judge_brief` already encodes a single latent, whose condition identity leaks, whose target-slice is unspecified, whose claim types are unspecified, and whose retrieval-degenerate probes make "factual grounding" a grep test — so the math is telling a true story about that setup, and the instrument won't improve by adding axes or more data until the packet changes.

---

## Provenance

- `benchmark_runner.py:60–135` — rubric schema.
- `benchmark_runner.py:666–686` — `_build_judge_brief` (the generic, non-per-probe brief).
- `benchmark_runner.py:689–728` — `_build_real_ask_packet` (what goes into `packet.json`).
- `benchmark_runner.py:954–1006` — `_build_judge_prompt` (the system-level judge instructions).
- `research/n1-memory-lab/JUDGE_DESIGN_LITERATURE_MAP_20260420.md` §4 — the primitive set the project defined but did not deploy.
- `research/n1-memory-lab/judge-calibrated-baseline-experiment/papers/nondeterministic_verifier_202604/FIELD_MAP_202604.md` — literature context.
