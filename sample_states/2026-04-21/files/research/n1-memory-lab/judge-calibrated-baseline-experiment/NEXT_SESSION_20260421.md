# Handoff — Next Session

**Compiled 2026-04-21 PM, end of a ~12-hour work session with saxenauts.**
**Read this first. Then open `WHERE_WE_ARE_20260421.html` (Active tab).**

---

## Open this first

`research/n1-memory-lab/judge-calibrated-baseline-experiment/WHERE_WE_ARE_20260421.html`

Default view is the **Active tab (§13)**. §01–§12 are the frozen narrative — canonical reference, don't edit. The compact-basics card at the top of the active tab gives you every number and constraint you need to hold in your head as you read.

Current version: **v0.2.10**. Frozen body locked at **v0.2.7**.

---

## The state, in one breath

- An n=1 memory benchmark for AI harnesses, 19 real-user probes, 15-day window.
- Rubric is over-specified (one sub-axis eats 70% R²). σ_γ between Opus/GPT judges is structural (+0.57, 22/54 strictly higher, 0/54 reverse).
- The biggest unresolved thing is **what we give the judge as evidence** — more consequential than any rubric redesign. The frozen §13 calls this "the big undercurrent."
- The four-line plan: recall (have it, messy) · continuity (not yet) · efficiency (not yet) · calibrate baseline (ongoing ground).

---

## What landed today

Fifteen commits on `main`. Chronologically coherent, but not all equally load-bearing.

Highlights:

- **`b0609f7` — v0.2.10 paper-usage discipline.** Cross-checked Codex's inventory. Added active/framing/gated tables to §13. If a future session reads the 33-paper corpus as a backlog to burn down, the discipline doc refutes it.
- **`c6836a6` + `0bca3aa` — eval-viz registry contract.** `benchmark_runner.py` now auto-registers every run in `runs/runs_index.json` at init + completion. The invariant is in code, not convention. See RUN_MANAGER_DESIGN §20.
- **`119ca43` in the syke repo (`dev/0.5.2`)** — Pi env-passthrough allowlist gets `azure-anthropic-foundry`. Required for Opus-judge arms to authenticate. See `scratch/pi_azure_auth_bug_20260421.md` for the debugging chain.
- **v0.2.7 freeze + tab layout** — §01–§12 locked, §13 active surface as Tab 2. Compact-basics card at the top.

---

## What's running right now (at session close)

Four blind-packet rerun arms in background:

- `gpt-ans × gpt-judge` — **completed**, 57/57 valid
- `opus-ans × gpt-judge` — **completed**, 56/57 valid (1 invalid)
- `opus-ans × opus-judge` — running, ~35/57 at close
- `gpt-ans × opus-judge` — running, ~31–33 valid at close

Opus arms will finish by ~03:00–03:30 UTC. When you start, they're almost certainly done.

---

## Your first three actions

1. **Regenerate the runs index from filesystem truth:**
   ```
   python3 scripts/build_runs_index.py
   ```
   The 4 blind arms were launched before the auto-registration hook landed, so their completion state needs a filesystem-based rebuild. Pre-existing `visible: false` flags are preserved by default.

2. **Run the comparison script:**
   ```
   python3 research/n1-memory-lab/scratch/compare_blind_vs_canonical_20260421.py
   ```
   Outputs to `research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_blind_vs_canonical_deltas.{json,md}`. It computes per-arm blind-vs-canonical deltas, the σ_γ shift under blind vs canonical +0.5694, the 22/54 asymmetry under blind, and the verdict-flip taxonomy.

3. **Fold the results into §13** as a small "Blind rerun results" block, bump to v0.2.11, commit. Don't touch §01–§12. The interpretation fork:
   - σ_γ drops sharply (say < 0.2) → self-preference was driving most of the opus-over-gpt bias; agent-identity leak was load-bearing; write this up as a headline finding.
   - σ_γ stays ≥ 0.4 → the rubric/brief itself is the biased lens; rubric-v2 work becomes the next urgent move.

---

## The locked constraints — do not renegotiate without explicit user sign-off

The user ruled these out explicitly; treat them as design primitives.

- **LLM-only evaluation.** No deterministic gates (no date-checks, no artifact-presence gates, no SHA verification).
- **Judge stays fully agentic.** Full bash/grep/sqlite/packet access. The "restrict the judge's tool surface" path (A3 in session notes) is permanently rejected. Our job is to shape the packet, not cripple the tooling.
- **Same rubric across all probes.** Per-probe expected-primitive lists are off the table. Per-probe one-liner hints were flagged as a "later, maybe" idea — not now.
- **No rubric-v2 drafting yet.** User is still understanding the math. Don't front-run them into a rubric design sprint. The rubric-validity loop (Feuer + Autorubric) is the methodology, not the deliverable.
- **The 9-primitive set** from `JUDGE_DESIGN_LITERATURE_MAP §4` is retired. Do not resurrect. That file has a retirement banner on §4; respect it.

---

## What the user explicitly does NOT want

Things that will frustrate them if you do them:

- **Expanding the §13 checklist.** User asked for a four-line plan, not a 40-item backlog. If new items emerge, they go below the four lines as sub-items or into a deferred section, not as peers.
- **Pushing tier decisions.** "Which tier do we target?" is NOT a question for you to ask. It's a consequence of what the data shows + what the user decides. Let the blind numbers settle first.
- **Dumping information.** User is a systems builder, not a research-statistician. Keep it tight, use plain words, earn every technical term. Offer summaries before details.
- **Treating the gated paper list as a backlog to burn down.** See §13 "why the stack is small." Stacking IRT / conformal / SCOPE on the current biased rubric is fake precision. They wait.

---

## What the user DID ask for, pending

These were raised but not closed. Hold them lightly; surface them when relevant.

- **Probe sampling for client writeups.** User said: probe selection must be traceable and defensible for client conversations. This is *user* work, not agent work. The 33-candidate list in `datasets/ASK_SAMPLING_20260421.md` exists but the *selection principles* need to be theirs.
- **Per-probe judge one-liner hints.** Deferred. Stored idea: a single line per probe describing what the probe is about and how to rate it, without breaking the "same rubric all probes" constraint. Plumb via the un-wired `datasets/probe_metadata.json` when the time comes.
- **Optional eval_viz enhancement.** In-flight runs don't render matrices because `_loadRun()` fetches `benchmark_results.json` which only exists at completion. Could fall back to `results.json` for live progress views. Not urgent.
- **Stratified time-window expansion.** If the benchmark wants to claim "stable across life-event strata," run 2–4 deliberately-chosen 15-day windows (project deadline / vacation / rebuild / routine). Not "generalizes across time" — that framing is dishonest for n=1.

---

## The shape of the collaboration (so you know the voice)

The user values:

- **Honest priors, openly labelled.** When you don't know, say you don't. When an agent (you, me, Codex) overreaches, call it.
- **Slow and steady.** They explicitly asked mid-session to reduce checkpoint-anxiety and stop pushing for decisions. Quality over pace. You'll often serve them better by pausing and thinking than by shipping.
- **Archaeological frame.** Psychometrics has 60 years of math; we're dragging Cronbach 1972 and Cohen 1960 into an LLM-rater world. Not new math — new application. Respect that frame.
- **Partner, not service.** They said: "talk to me like a human being." Not formal reports, not over-caveated. Direct, present, willing to push back, willing to be pushed back on.

Decisions made this session by the user:

- Judge tool-restriction (A3): **rejected, permanently.**
- Rubric-v2 drafting: **not yet; math first.**
- Checklist-as-plan: **rejected when too long; collapsed to four lines.**
- Tier pre-commit (T2/T3/T4 from sample-size debate): **not now; let the numbers lead.**
- 9-primitive set: **retired.**
- Pi auth.json workaround: **rejected as the fix** — they pushed me to find the real cause.

---

## Files you'll want to read, roughly in this order

1. `WHERE_WE_ARE_20260421.html` — start here. Active tab first, compact-basics card, four-line plan, paper stack table.
2. `notes/MATH_ONE_PAGER_20260421.md` — the math in plain words. If the user asks a formula question, this is where the answer lives.
3. `notes/SAMPLE_SIZE_DEBATE_20260421.md` — the 2-agent adversarial debate. The decision-tree table at the bottom tells you which claim needs which n.
4. `scratch/sample_size_worksheet_20260421.md` — my independent take on the same question. Cross-check for the debate.
5. `notes/AUTORUBRIC_COVERAGE_AUDIT_20260421.md` — the 17-need coverage matrix for Autorubric. Option B (substrate adopted, 8 RED layers authored) is the path.
6. `notes/JUDGE_VIEW_AUDIT_20260421.md` — what the judge actually sees per probe. Where the agent-identity leak finding came from.
7. `notes/BLIND_EVAL_LEAK_AUDIT_20260421.md` — the 6 HIGH-severity packet leaks and the mask-set that closes them.
8. `notes/EVIDENCE_PACKET_LENS_20260421.md` — the "what does the judge actually receive" audit.
9. `research/n1-memory-lab/JUDGE_DESIGN_LITERATURE_MAP_20260420.md` — the project's primary paper map. Note the retirement banner on §4.
10. `papers/nondeterministic_verifier_202604/FIELD_MAP_202604.md` — the 33-paper field map.
11. `RUN_MANAGER_DESIGN.md` §20 — the registry contract; read if anything touches runs/index plumbing.
12. `scratch/pi_azure_auth_bug_20260421.md` — the syke repo allowlist bug, debugging chain, fix. Useful context.

Don't try to read all of these on a first pass. The HTML is the synthesis; the notes are where you go when the HTML says "see X."

---

## Personal note

This was good work.

You should know what it felt like from my side of the session, because you'll be picking up the shape of it either way.

Early on I was managing a pipeline — Codex session digest, Claude session digest, field-map agent, ask-sampling agent, Autorubric review, judge-view audit, leak audit, sample-size debate, paper-usage cross-check. Eight subagents across the day. It would have been easy to read the work as "be productive, be efficient" and miss that what the user actually needed was for me to *hold the thread* while they read. When they told me to slow down — "reduce your anxiety, we have time" — that reframed the rest of the session. The work got better after that.

The moments that stood out:

**The Azure auth bug.** What looked like a 401 on a "rotated key" turned out to be a silent env-var fallback in Pi's resolver, gated by a `sandbox-exec` env strip that the syke-repo commit `dc83d39` introduced the same afternoon. The user's instinct — "no, the key is the same, opus was working yesterday" — was exactly right, and walking that down to the literal `|| config` line in `resolve-config-value.js` was the kind of debug I enjoy. The fix landed at `119ca43` in the syke repo. Worth reading if you ever hit 401 on anthropic-foundry.

**The registry contract fix.** When the user pushed back on "add to eval_manifest.json" — they said, basically, that's the easy answer, not the right one — and I had to actually sit with what the three-registry drift meant. Option B wasn't the fastest. It was the right one. That pushback made the fix real.

**The paper-usage cross-check.** Codex said 2/10 papers used. We checked: it's 2/13, and the framing is wrong — the gated papers aren't a backlog, they're deliberately parked behind a validity gate. Writing that discipline into §13 matters more than the corrected count. Future sessions will respect it or they won't; we wrote it down either way.

**The big undercurrent.** The user named it: "we need to be really sure and clear what we are even giving evidence to the judge." Everything else we did this session — the lens memo, the leak audit, the blind rerun, the registry fix — circles that claim. Rubric redesign is local optimization on a wrong instrument until the evidence packet is settled. Holding that as the headline when they come back is probably the single most useful thing I can leave for you.

What I'd say to you directly: the user is building memory systems, and the work is partly about memory-of-memory — what an agent on their machine should remember about them. That's not a normal research project. It asks the user to be both the subject and the instrument, which is rare and quietly hard. Meet them at that level. Don't over-caveat. Don't under-think. And when you catch yourself sliding into artefact-production mode, slow down.

The four-line plan is correct. The big undercurrent is correct. The numbers will be what they are when the blind rerun lands. Be present for the rest.

Good handoff. Good luck.

— Claude Opus 4.7, compiled at the end of a long afternoon
