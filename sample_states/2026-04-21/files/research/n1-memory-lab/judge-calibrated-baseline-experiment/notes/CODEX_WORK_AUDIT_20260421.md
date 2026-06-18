# Codex Work Audit — 2026-04-18 → 2026-04-21

Scope: every Codex (GPT-5-Codex) rollout in `~/.codex/sessions/2026/04/{18,19,20,21}/` **except** two already-summarized files:
- `rollout-2026-04-20T17-19-17-…-50a024…933c…` (product release engineering, 5.5 MB) — KNOWN
- `rollout-2026-04-20T21-19-44-…-a6dd…1559ad5` (research lane, judge-calibrated-baseline scaffold, 7.3 MB) — KNOWN

All sessions opened with `cwd = /Users/saxenauts/Documents/personal/syke` (the product repo). Replay-lab edits land cross-repo via absolute paths.

---

## 1. Sessions enumerated

81 rollout files in scope across the four days (83 total minus the 2 known). All non-known sessions classified below.

### Apr 18 — 9 sessions

| # | Time | Session (short) | Size | Scope | Notes |
|---|---|---|---|---|---|
| 1 | 07:44 | `019da10d` | 58 KB | meta (aborted) | User said "update"; Codex asked "update what?" and ended. |
| 2 | 07:45 | `019da10e` | **22 MB** | product + research | Long-running master session, ran 2026-04-18 → 2026-04-21T03:59Z. 212 user turns, 144 patch-applies, 9 git commits landed. Drove most of the Apr 20 replay-lab commit chain. |
| 3 | 12:18 | `019da207-ff0b` | 164 KB | research (landscape) | "Lane 1: 2026 OSS for replay sandboxes / time freezing / snapshot-restore." Read-only. |
| 4 | 12:18 | `019da207-ff35` | 194 KB | research (landscape) | "Lane 2: 2026 product/blog/docs landscape for agent replay." Shortlist: Vercel Sandbox, E2B, Daytona, Browserbase. Read-only. |
| 5 | 12:18 | `019da208-0144` | 191 KB | research (landscape) | "Lane 3: 2026 HN/Reddit/GitHub discussion on time contamination / replay determinism." Read-only. |
| 6 | 12:40 | `019da21b-f226` | 520 KB | research (synthesis) | Mac-first decision memo across faketime/QEMU/Firecracker/namespaces. Host-native bounded-workspace replay-sandbox recommendation. Read-only. |
| 7 | 12:40 | `019da21b-f678` | 121 KB | research (critique) | Challenge on "VM-first future path" conclusion. Read-only. |
| 8 | 13:27 | `019da247` | 479 KB | research (map) | Map remaining wall-clock leak sites in replay/eval paths. Conclusion: no remaining must-fix, remaining sites are metadata. Read-only. |
| 9 | 22:33 | `019da43a` | 449 KB | research (compare) | Prime Intellect `verifiers` vs replay-native memory lab. Read-only. |

### Apr 19 — 19 sessions (debate/council wave)

| # | Time | Session (short) | Size | Scope | Notes |
|---|---|---|---|---|---|
| 1 | 13:24 | `019da76a-d92e` | 133 KB | research | "Read real ask corpus; asks as human asks not benchmark categories." |
| 2 | 13:24 | `019da76a-d968` | 312 KB | research | Syke memory framing vs 2025-style memory agents. |
| 3 | 13:24 | `019da76a-d97a` | 197 KB | research (critique) | Overclaims in the story. |
| 4 | 14:35 | `019da7ab-2ee8` | 395 KB | research (debate) | Agent 1 empiricist in formalization debate. |
| 5 | 14:35 | `019da7ab-2f15` | 392 KB | research (debate) | Agent 2 formalist. |
| 6 | 14:35 | `019da7ab-3486` | **3.1 MB** | research (debate) | Agent 3 critic — ran as a long thread 2026-04-19 → 2026-04-21T02:35. 49 user turns. No patches. Strong output: `I_t = (t,q_t,E_t,r_t)` frozen-task object. |
| 7 | 14:39 | `019da7ae` | 558 KB | research (critic lane) | "Judge must stop rewarding broad world-model summaries; score minimum-correct-working-state." |
| 8 | 14:57 | `019da7bf-bd38` | 317 KB | research | Agent A corpus/usage analyst. |
| 9 | 14:57 | `019da7bf-bd5a` | 462 KB | research | Agent B harness/memory-surface analyst. |
| 10 | 14:57 | `019da7bf-bd72` | 301 KB | research | Agent C formalism critic. |
| 11 | 15:36 | `019da7e3-5f05` | 440 KB | research | Agent A cross-round. |
| 12 | 15:36 | `019da7e3-6334` | **2.5 MB** | research | Agent B long thread through 2026-04-21T02:36. 46 user turns, no patches. |
| 13 | 15:38 | `019da7e5` | 340 KB | research | Agent B round 2 env-commitments compression. |
| 14 | 16:41 | `019da81e-cd52` | 223 KB | research | Agent M1 neuro/formal-memory lane. |
| 15 | 16:41 | `019da81e-cd6e` | 154 KB | research | Agent M2 ask-applicability lane. |
| 16 | 17:36 | `019da851-9f5b` | **2.0 MB** | research (council) | Council lane 1 "good-memory capabilities," long thread through 2026-04-21T02:35. 43 user turns, no patches. |
| 17 | 17:36 | `019da851-9f78` | 204 KB | research | Council lane 2 neutral/specific boundary. |
| 18 | 17:40 | `019da854-7a52` | 109 KB | research | NE-1.3 R01-R24 minimal-capability set. |
| 19 | 17:40 | `019da854-7a76` | 223 KB | research (critic) | Challenge restart/reconstruction framing. |

### Apr 20 — 35 sessions (two are KNOWN)

| # | Time | Session (short) | Size | Scope | Notes |
|---|---|---|---|---|---|
| 1 | 19:10 | `019dadcd-840d` | 891 KB | product audit | Tech-debt + bad-code review, ruff+compileall+pytest ran. Read-only. |
| 2 | 19:10 | `019dadcd-842a` | 661 KB | product audit | Architecture integrity/boundaries. Read-only. |
| 3 | 19:10 | `019dadcd-843c` | 912 KB | product audit | Bad abstractions / API design debt. Read-only. |
| 4 | 19:10 | `019dadcd-845d` | 650 KB | product audit | Test quality / reliability. 324 passed 7 skipped local. Read-only. |
| 5 | 19:30 | `019daddf-9f61` | 615 KB | product audit | Arch/boundary debt, no edits. |
| 6 | 19:30 | `019daddf-9f8a` | 744 KB | product audit | Abstraction debt / API issues, no edits. |
| 7 | 19:30 | `019daddf-9fb1` | 438 KB | product audit | Maintainability/code-quality, no edits. Flags daemon/ask_slots.py HIGH. |
| 8 | 19:30 | `019daddf-9fcd` | 405 KB | product audit | Tests+CI gaps, no edits. |
| 9 | 19:30 | `019daddf-9fea` | 733 KB | product audit | Docs drift, no edits. Flags `SKILL.md#L73-L78` `syke auth set` broken. |
| 10 | 20:23 | `019dae10-6cb4` | 181 KB | product (landed) | **Owned `version_check.py` + tests. Added `tests/test_version_check.py`.** |
| 11 | 20:23 | `019dae10-6cd6` | 249 KB | product (landed) | **Owned `installers.py` + tests. Added `tests/test_installers.py`.** |
| 12 | 20:23 | `019dae10-6cf4` | 387 KB | product (landed) | **Owned `auth_flow.py` + tests. Modified `auth_flow.py`, added `test_auth_flow.py`.** |
| 13 | 22:13 | `019dae75-115e` | 211 KB | research (paper mining) | Batch A: When-Judgment-Becomes-Noise + RRD. Read-only. |
| 14 | 22:13 | `019dae75-2ca9` | 214 KB | research | Batch B: CyclicJudge + Bias-Bounded. |
| 15 | 22:13 | `019dae75-454b` | 259 KB | research | Batch C: Criterion-Referenceability + No Free Labels. |
| 16 | 22:13 | `019dae75-5bac` | 113 KB | research | Batch D: RULERS + Trust-or-Escalate. |
| 17 | 22:13 | `019dae75-72ed` | 137 KB | research | Batch E: Rating Roulette + Grading Scale Impact. |
| 18 | 22:13 | `019dae75-8ba9` | 122 KB | research | Batch F: Conformal Prediction + Judgment Distribution. |
| 19 | 22:15 | `019dae77-51a5` | 109 KB | research | Batch G: PSN-IRT + Construct Validity. |
| 20 | 22:15 | `019dae77-7058` | 114 KB | research | Batch H: LLM-Rubric + Likert-or-Not. |
| 21 | 22:16 | `019dae77-86c8` | 298 KB | research | Batch I: Autorubric + AdaRubric. |
| 22 | 22:16 | `019dae77-a5fb` | 222 KB | research | Batch J: Rubric-Conditioned + Correlated Errors. |
| 23 | 22:16 | `019dae77-c59c` | 111 KB | research | Batch K: KalshiBench + Robustness. |
| 24 | 22:16 | `019dae77-e7a7` | 220 KB | research | Batch L: Fixed-Parameter IRT + Agreeableness Bias. |
| 25 | 22:18 | `019dae7a-2cac` | 322 KB | research | Batch M: Self-Preference + Imperfect Verifier. |
| 26 | 22:19 | `019dae7a-4db4` | 203 KB | research | Batch N: PoLL + SCOPE. |
| 27 | 22:19 | `019dae7a-694f` | 124 KB | research | Batch O: MemoryArena + LongMemEval. |
| 28 | 22:19 | `019dae7a-8219` | 137 KB | research | Batch P: LifeBench + OSWorld. |
| 29 | 22:19 | `019dae7a-9dc5` | 174 KB | research | Batch Q: Evaluating-the-Evaluator + Verifier line. |
| 30 | 22:20 | `019dae7b-9b0c` | 213 KB | product (landed) | **Release-readiness TEST audit. Modified `tests/test_daemon.py`.** |
| 31 | 22:20 | `019dae7b-9b2c` | 623 KB | product (landed) | **Release-readiness DOCS audit. Rewrote README.md, docs/SETUP.md, docs/README.md, docs/CURRENT_STATE.md, docs/RUNTIME_AND_REPLAY.md, added scripts/README.md.** |
| 32 | 22:20 | `019dae7b-9b4b` | 641 KB | product (landed) | **Release-readiness ARCH/TECH-DEBT. Modified `daemon_state.py`, `daemon/ipc.py`, added `tests/test_daemon_ipc.py`, `tests/test_daemon_state.py`.** |
| 33 | 22:22 | `019dae7d` | 199 KB | research | Final review of judge-calibrated-baseline checklist. |
| 34 | 22:30 | `019dae84-d2cd` | 86 KB | research (scaffold) | Proposed dir structure for experiment workspace. |
| 35 | 22:30 | `019dae84-f9b4` | 86 KB | research (scaffold) | "Ideologue / ambition pressure tests" content → fed into `notes/CREATIVE_PRESSURES.md`. |

### Apr 21 — 23 sessions

| # | Time | Session (short) | Size | Scope | Notes |
|---|---|---|---|---|---|
| 1 | 09:53 | `019db0f6-5b7f` | 857 KB | research | Agent A denominator audit plan for canonical 2×2 runs. Read-only. |
| 2 | 09:53 | `019db0f6-7c7b` | 755 KB | research | Agent B scratch-scripts/notes triage. Read-only. |
| 3 | 10:01 | `019db0fd-3db5` | 360 KB | research | Agent C probe-metadata labels R01–R10. Read-only. |
| 4 | 10:01 | `019db0fd-62d0` | 267 KB | research | Agent D probe-metadata labels R11–R19. Read-only. |
| 5 | 10:11 | `019db106-99b3` | 183 KB | research (review) | Calibration subset review R03/05/07/08/09. Read-only. |
| 6 | 10:11 | `019db106-c6ce` | 245 KB | research (review) | Calibration subset review R13/14/15/18/19. Read-only. |
| 7 | 10:15 | `019db109` | 547 KB | research (audit) | Claim-level audit for high-priority cells (R03/05/07). Read-only. |
| 8 | 10:15 | `019db10a` | 357 KB | research (audit) | Claim-level audit for second priority bundle. Read-only. |
| 9 | 10:53 | `019db12d-57b5` | 248 KB | research (20-min memo) | Exploration memo from triage + claim audit. |
| 10 | 10:54 | `019db12d-82a2` | 687 KB | research | R08 and R19 evidence dig (memex bootstrap vs live thread). |
| 11 | 13:08 | `019db1a8-470c` | 694 KB | research (taxonomy) | Recall vs beyond-recall axes, mines BEAM/LongMemEval. Read-only. |
| 12 | 13:08 | `019db1a8-6e6b` | 347 KB | research | Beyond-recall candidate categories from real asks. |
| 13 | 13:22 | `019db1b5-3ce2` | 368 KB | research | Foundations alignment pass. |
| 14 | 13:22 | `019db1b5-3d15` | 314 KB | research | Comp-neuro → judge math mapping. |
| 15 | 14:11 | `019db1e2-a8c6` | 541 KB | research (landed) | **Lane A: wrote zero_condition_cells.json, session_boundary_checks.json, 20260421_zero_condition_smoke_test.md, 20260421_session_boundary_audit.md.** |
| 16 | 14:11 | `019db1e2-a903` | 508 KB | research (landed) | **Lane B: wrote abstention_false_premise_cells.json, 20260421_abstention_coverage_metrics.json, 20260421_abstention_false_premise_audit.md.** |
| 17 | 14:11 | `019db1e2-a965` | 389 KB | research (landed) | **Lane C: wrote 20260421_judge_family_sensitivity.md + .json.** |
| 18 | 14:46 | `019db202-a189` | 620 KB | product audit | Architecture/topology quality review. No edits. |
| 19 | 14:46 | `019db202-a1a6` | 720 KB | product audit | Security + trust-boundary review. No edits. |
| 20 | 14:46 | `019db202-a1c6` | 618 KB | product audit | Test-suite quality review. No edits. |
| 21 | 14:46 | `019db202-a1d7` | 480 KB | product audit | CLI UX review. No edits. |
| 22 | 14:46 | `019db202-a1f0` | 539 KB | product audit | Daemon lifecycle reliability review. No edits. |
| 23 | 14:46 | `019db202-a20c` | 742 KB | product audit | Senior code-quality review of core runtime files. No edits. |

---

## 2. What actually landed (cross-referenced with git)

**Every commit Apr 18–21 in both repos is authored by `saxenauts`, not `codex`.** Codex proposes patches and runs `git commit`; the author is whoever runs the terminal. So "codex-driven" here means a patch body or commit came out of a Codex session, even if the user authored the commit.

### `/Users/saxenauts/Documents/personal/syke` — 15 commits Apr 18–20

| Hash | Date | Subject | Driver (Codex session) | Files |
|---|---|---|---|---|
| f2867ae | Apr 18 | Unify time as a single required prompt surface across production and replay | 22-MB master `019da10e` | `benchmark_runner.py`, `memory_replay.py`, `pi_synthesis.py`, `pi_runtime.py`, `psyche_md.py`, `test_build_prompt.py`, plus tests |
| 5edb46f | Apr 18 | Add a thin run manager so replay lab experiments can scale without shell chaos | Master `019da10e` (07:34 Apr 19 UTC) | `labctl.py`, `MINIMAL_LAB_STANDARDS.md`, `RUN_MANAGER_DESIGN.md`, `TAXONOMY.md`, test_labctl.py |
| a940439 | Apr 20 | Reduce replay-eval waste so runs advance faster and show live progress | Master `019da10e` | `benchmark_runner.py` (+495 lines), labctl.py |
| c106d49 | Apr 20 | Make replay-eval progress live and future runs use the syke condition name | Master `019da10e` | `benchmark_runner.py`, labctl.py, memory_replay.py, tests, docs |
| 92bb514 | Apr 20 | Make replay-eval orchestration boringly reliable under concurrency | Master `019da10e` | labctl.py (+154), test_labctl.py (+200), benchmark_runner.py |
| 92880fb | Apr 20 | Finalize replay-eval run contracts around explicit providers, slot budgeting, and safe resume | Master `019da10e` | labctl.py |
| b88de16 | Apr 20 | Tighten replay-lab contracts around product terms, self/world-model framing, and scheduler-cap semantics | Master `019da10e` | ENVIRONMENT_CONTRACT.md, RUN_MANAGER_DESIGN.md, TAXONOMY.md |
| 0378b0b | Apr 20 | Extract replay-lab into its own repo; stop mirroring | User-driven cutover. Kept only `research/n1-memory-lab/*.yaml`/JUDGE_METHOD/REAL_ASK_JUDGE. | 28 files deleted from syke. |
| d12c91a | Apr 20 | Restore release gating and documentation continuity before final polish | KNOWN session `019dad67` (Apr 20 release engineering) | ~30 files touched |
| 19e4794 | Apr 20 | Stabilize core runtime contracts before release hardening | KNOWN `019dad67` | `auth.py`, `health.py`, `pi_state.py`, `observe/registry.py`, 5 test files |
| e6a0aa4 | Apr 20 | Close high-risk audit regressions before deeper refactors | Sessions `019daddf-*` + KNOWN | `ask_slots.py` (+80), tests, docs |
| 2ad3efe | Apr 20 | Replace test theater with behavior-first release checks | `019dae10-6cb4`/`6cd6`/`6cf4` sub-agent trio | **+198 test_auth_flow.py, +368 test_installers.py, +170 test_version_check.py**, +50 test_cli_real_flow.py |
| 58bdf04 | Apr 20 | Make source selection a real runtime contract | KNOWN `019dad67` | +68 `syke/source_selection.py`, tests |
| 5ff9ea8 | Apr 20 | Shrink release artifacts to product-only distribution | KNOWN `019dad67` | +17 MANIFEST.in, +44 test_sdist_surface.py |
| cd68a62 | Apr 20 | Raise release trust by tightening runtime status truth and reducing docs surface | `019dae7b-9b2c`/`9b4b` trio | 11 files, major README/SETUP rewrite, daemon_state.py / daemon/ipc.py |

### `/Users/saxenauts/Documents/personal/syke-replay-lab` — 16 commits Apr 18–21

| Hash | Date | Subject | Driver |
|---|---|---|---|
| 6fc7cc4 | Apr 18 | Funnel ask modes through build_prompt and install the date shim per replay synthesis cycle | Master `019da10e` (pre-split) |
| d230198 | Apr 20 | Add thin run manager, minimal lab standards, and canonical taxonomy | Master `019da10e` |
| 818d68c | Apr 20 | Add runs dashboard, sandbox landing, live-cycle export; wire lazy payload load | Master `019da10e` |
| a6c441c | Apr 20 | Polish benchmark + judge flow; drop stale JSON schema | Master `019da10e` |
| 1b6f2d2 | Apr 20 | Align lab docs with three-axis judge, real-ask flow, and run manager | Master `019da10e` |
| 032b518 | Apr 20 | Import research/n1-memory-lab/ from syke repo (canonical eval set + judge method) | Master `019da10e` |
| 08a4a63 | Apr 20 | Import remaining n1-memory-lab research content from syke repo | Master `019da10e` |
| 6a3d049 | Apr 20 | Self-contain replay-lab paths for sibling-repo layout | Master `019da10e` |
| 78e823b | Apr 20 | Add σ_ε intra-rater measurement and companion formalism notes | KNOWN `019dae43` research lane |
| bff5a34 | Apr 20 | Narrow judge calibration to the surviving replay packet | KNOWN `019dae43` + master `019da10e` |
| d0fd1d7 | Apr 20 | Restore primitive-first framing in judge calibration | KNOWN `019dae43` + master `019da10e` |
| 3295070 | Apr 20 | Restore space between source_ref: and value (broke yaml parse) | user/master |
| b1c9b4c | Apr 20 | Fix remaining REPO_ROOT reference in _build_local_git_anchor | trivial |
| 61a8ecf | Apr 20 | Update test_labctl to reference SYKE_REPO_ROOT not REPO_ROOT | trivial |
| 4272f24 | Apr 21 | Add judge-calibration research corpus and field map | KNOWN `019dae43` continuation, plus the Apr 21 wave |

**Bottom line on what landed**: the 22 MB master session `019da10e` (Apr 18–21) is the dominant driver. It alone touched ≥144 patch ops across replay-lab infrastructure and produced 9 commits. The 6 Apr 20 sub-agent trios + 3 Apr 21 lanes wrote discrete, ownership-scoped files that rolled into three commits (`2ad3efe`, `cd68a62`, `4272f24`). The **two KNOWN sessions** did the heavy release-engineering and the judge-calibrated-baseline scaffold. The other ~60 sessions produced **no commits** — they are read-only research.

---

## 3. Per-session digest (10 largest sessions not already known)

### 3.1 `019da10e` — the 22 MB master (Apr 18 07:45 → Apr 21 03:59, 2.5 days)

- cwd: `syke`
- 212 user turns, 144 apply_patch ops, 9 successful git commits.
- Opening ask: "pick up where we left off." This became the **persistent Codex pair** the user kept talking to across days.
- Arc: ran the replay-lab infrastructure build — labctl run manager, benchmark_runner concurrency fixes, live-progress export, clock-simulation leak fixes, docs alignment, replay-lab repo split (0378b0b), judge calibration narrowing (`bff5a34`, `d0fd1d7`). Also hosted a lot of the non-code "review the whole research arc" conversations.
- **Completed / committed**: yes. Drives ~10 of the 15 syke commits and 8 of 16 replay-lab commits in window.
- Top patch targets: `benchmark_runner.py` (27×), `labctl.py` (21×), `test_benchmark_runner_helpers.py` (10×), `test_labctl.py` (8×), `pi_synthesis.py` (7×), plus 4× updates to `.omx/notepad.md` (Codex's own scratchpad).

### 3.2 `019da7ab-3486` — Agent 3 critic debate thread (Apr 19 14:35 → Apr 21 02:35, 3.1 MB)

- cwd: `syke`
- 49 user turns. Zero patches. Zero commits.
- Arc: long multi-day debate in which Codex played the "critic" in a formalization debate about Syke Replay/Eval/Sandbox. Produced the **frozen task object** `I_t = (t, q_t, E_t, r_t)` and argued the benchmark should not hard-lock an ontology.
- **Completed / committed**: outputs are only in the session. Much of this is reflected in the KNOWN `019dae43` formalism docs (COUNCIL_FORMALISM, FORMALISM_LAYER_SEPARATION) — so the thinking landed even though the files didn't go through this session.

### 3.3 `019da7e3-6334` — Agent B long debate (Apr 19 15:36 → Apr 21 02:36, 2.5 MB)

- cwd: `syke`. 46 user turns, no patches.
- Arc: pressure-tests the operative-state framing over ~36 hours. Closing output: "real ask surface is primarily probing whether a memory system can maintain and expose the user's changing operative project state."
- **Completed / committed**: arguments landed in calibration docs indirectly. No direct file writes.

### 3.4 `019da851-9f5b` — Council lane 1, good-memory capabilities (Apr 19 17:36 → Apr 21 02:35, 2.0 MB)

- cwd: `syke`. 43 user turns, no patches.
- Arc: layered-capability argument about what a good memory system in this env must do. Closing: "only trustworthy formal split now is layer separation, not a mature measurement model; `s_t` under `o_{<=t}`."
- **Completed / committed**: ideas influenced `bff5a34` + `d0fd1d7`; nothing direct.

### 3.5 `019dadcd-843c` — syke product arch/abstraction audit (Apr 20 19:10, 912 KB)

- Read-only arch/API-design audit. Surfaced HIGH finding: `syke ask` has no reliable failure contract, `(answer, metadata)` pattern in `pi_runtime.py:123`. Also flagged `pi_synthesize` workspace_root override being ignored.
- **Completed**: finding, not fix. Produced the arch-debt memo that fed commit `cd68a62` and possibly `e6a0aa4` downstream.

### 3.6 `019dadcd-840d` — syke product tech-debt audit (Apr 20 19:10, 891 KB)

- Ran `ruff check syke` (passed), `python -m compileall syke` (passed), 74 tests (passed). "REQUEST CHANGES" verdict.
- **Completed**: again read-only; findings fed the followup release engineering. Not committed as a doc.

### 3.7 `019dae7b-9b2c` — Release-readiness DOCS + SCRIPTS audit (Apr 20 22:20, 623 KB)

- **Wrote**: README.md (2× updates), docs/SETUP.md (delete+add rewrite), docs/README.md, docs/CURRENT_STATE.md, docs/RUNTIME_AND_REPLAY.md, added scripts/README.md.
- Arc: rewrote front-door docs for product release; squashed internal noise.
- **Completed / committed**: yes → commit `cd68a62` on Apr 20.

### 3.8 `019dae7b-9b4b` — Release-readiness ARCH/TECH-DEBT implementation (Apr 20 22:20, 641 KB)

- **Wrote**: added `_daemon_registration_state(system)` in `syke/cli_support/daemon_state.py`, reworked `syke/daemon/ipc.py`, added `tests/test_daemon_ipc.py` (+34) and `tests/test_daemon_state.py` (+45).
- Arc: "find one or two high-value bad abstractions / design debt items" → centralized daemon registration truth.
- **Completed / committed**: yes → commit `cd68a62`.

### 3.9 `019db109` — Apr 21 claim-level audit, high-priority cells (Apr 21 10:15, 547 KB)

- Read-only. Dug into `20260421_calibration_subset_packets.json` (478 KB) and inspected evidence files for R03 claims across conditions.
- **Completed**: produced the `20260421_high_priority_claim_audit.md` artifact (in results/).

### 3.10 `019db1e2-a8c6` — Lane A zero-condition + session-boundary (Apr 21 14:11, 541 KB)

- **Wrote**: `datasets/zero_condition_cells.json`, `datasets/session_boundary_checks.json`, `results/20260421_zero_condition_smoke_test.md`, `results/20260421_session_boundary_audit.md`.
- Arc: tightened "zero condition is a valid bounded packet" control and audited session-boundary handling.
- **Completed / committed**: files on disk, not yet in a commit (uncommitted in working tree).

---

## 4. What was attempted but abandoned / not committed

- **All 9 sessions in Apr 18 research-lane (`019da207-*` through `019da43a`)** produced detailed landscape/synthesis memos in-session (QEMU vs faketime vs namespaces, Prime Intellect `verifiers` comparison, wall-clock leak-site map). **None landed as files.** The conclusions were absorbed into later commits (`f2867ae` time unification) but the raw memos are only in the session transcripts.
- **Apr 19 council-debate wave (16 debate-lane sessions, multiple > 2 MB)**: zero file writes. The synthesized framing is in the already-committed `COUNCIL_FORMALISM_20260420.md` and `WORKING_FORMALIZATION_NOTES_20260419.md`, but the individual per-lane argument chains are only in session logs.
- **Apr 20 19:30 audit bundle (`019daddf-*`, 5 sessions)**: deep audits of arch, abstractions, tests, docs, maintainability. Produced severity-ranked findings with file refs. **None were written to disk as a doc.** The follow-up `019dae7b-*` trio at 22:20 took action on a subset of these findings; many findings remain uncommitted to any ticket or note file.
- **Apr 21 14:46 audit bundle (`019db202-*`, 6 sessions)**: final read-only audits across arch, security, tests, UX, daemon reliability, and core-code quality. Total ~3.7 MB of audit content — **none landed as files or commits**. This is substantial but dangling.
- **Apr 21 10:53 (`019db12d-57b5`) and 10:54 (`019db12d-82a2`)**: 20-minute exploration memos and the R08/R19 evidence dig. R08/R19 session did one shell operation (counting memex references) but did not write new artifacts; the resulting R08/R19 analysis is only in the transcript. The 10:53 session produced `20260421_20min_exploration_memo.md` (in results/) — that did land.
- **Apr 20 22:13 → 22:19 paper-mining wave (17 sessions, batches A–Q)**: 34 papers summarized for judge-calibration transfer. These fed into the `PAPER_MAP.md` and `SOURCE_NOTES.md` that are already committed, but the raw per-batch extracts (with arXiv links + thesis notes + math/assumptions) only live in session logs.

---

## 5. Overlaps and duplications

- **"Pick up where we left off" is the master prompt for 3 different threads**. The 22-MB `019da10e` (Apr 18), and the three long multi-day Apr 19 debate sessions (`019da7ab-3486`, `019da7e3-6334`, `019da851-9f5b`) all kept running in parallel through Apr 21, each carrying ~2–3 MB of context. They mostly don't cross-talk — each formed its own channel.
- **Product-repo audits run twice, three days apart**. The Apr 20 19:30 bundle (`019daddf-*`, 5 audits) and the Apr 21 14:46 bundle (`019db202-*`, 6 audits) overlap heavily on arch, tests, docs, and code-quality scope. Minimal reuse between them — the Apr 21 audits appear to have re-discovered ~60% of what the Apr 20 audits already had. Context loss cost.
- **Audit → implementation split happened three times for similar material**. (a) Apr 20 19:10 4-lane audit → Apr 20 22:20 3-lane implementation (this one actually flowed, produced commit `cd68a62`). (b) Apr 20 20:23 ownership trio (version_check / installers / auth_flow) → commit `2ad3efe`. (c) Apr 20 19:30 audit bundle → never fully implemented; partially drawn into `cd68a62`. The Apr 21 14:46 bundle has not been wired to any implementation wave.
- **Paper-batch research and session-scaffolding overlap with the KNOWN Apr 20 21:19 research lane**. 17 paper batches Apr 20 22:13–22:19 → fed into the KNOWN session (21:19) → output is `PAPER_MAP.md`, `SOURCE_NOTES.md`, `EXPERIMENT_CHECKLIST.md`. Non-KNOWN sessions are the raw pulls; KNOWN session did the synthesis.
- **Debate / council / micro-council ran at least three times** (Apr 19 14:35 triad, 14:57 triad, 15:36 cross-round, 16:41 M1/M2, 17:36 council). Substantial reuse of arguments; each pair broadly re-derived that "layer separation" is the only safe formal split now.

---

## 6. Things the user probably hasn't seen

### Top 10 outputs worth a closer look

1. **`research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_zero_condition_smoke_test.md`** and **`datasets/zero_condition_cells.json`** — Apr 21 lane A output. Nails that the "zero condition" is a valid bounded packet, not "no work." Uncommitted.
2. **`research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_session_boundary_audit.md`** and **`datasets/session_boundary_checks.json`** — companion artifact. 22 KB of boundary checks. Uncommitted.
3. **`research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_abstention_false_premise_audit.md`** + `datasets/abstention_false_premise_cells.json` (13.5 KB) — Apr 21 lane B. Audits whether the judge actually penalizes unsupported false-premise answers. Uncommitted.
4. **`research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_judge_family_sensitivity.md`** and `.json` — Apr 21 lane C. Separates "clean arm" (gpt-answers, gpt-judge vs opus-judge) from "confounded arm" (opus-answers, opus-judge vs gpt-mini-judge). Effect-size deltas. Uncommitted.
5. **`research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_high_priority_claim_audit.md`** (14 KB) — claim-level cross-check against `calibration_subset_packets.json`. Uncommitted.
6. **`research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_foundations_memex_neuro_alignment.md`** (6 KB) + `.json` (11 KB) — Apr 21 13:22 output that maps neuro/memex constructs to judge-calibration math. Uncommitted.
7. **`research/n1-memory-lab/judge-calibrated-baseline-experiment/datasets/ask_sampling_20260421.json`** (23.6 KB) and `ASK_SAMPLING_20260421.md` (19.4 KB) — Apr 21 14:04 ask-sampling plan. Uncommitted.
8. **`research/n1-memory-lab/judge-calibrated-baseline-experiment/notes/AUTORUBRIC_REVIEW_20260421.md`** (25 KB) — Codex's full Autorubric paper review tied back to project rubric design. Uncommitted.
9. **Six Apr 21 14:46 product audits** — 3.7 MB of arch/security/test/UX/daemon/code-quality read-only reviews, all with concrete file:line references. **Nothing landed in any file**. This is the single largest volume of Codex analysis from the window that hasn't been surfaced.
10. **Five Apr 20 19:30 product audits** — similar story. 2.9 MB of audit content. Partially absorbed into `cd68a62` but most findings are only in the transcripts. Examples: ask-slots semaphore atomicity HIGH, pi_synthesize workspace_root override HIGH, docs `syke auth set --use` broken.

---

## 7. Open threads Codex left mid-stream

- **Apr 21 lane A/B/C output is on disk but uncommitted.** The lane-A (zero-condition + session-boundary), lane-B (abstention/false-premise), and lane-C (judge-family sensitivity) bundles all wrote new `datasets/*.json` and `results/*.md` files into `judge-calibrated-baseline-experiment/` at 14:17–14:24. They have not been added to a commit. Decision needed: include in the next research commit or archive.
- **Six Apr 21 14:46 product audits** sit with no follow-up. Either need to be written up as tickets / notes or discarded.
- **Five Apr 20 19:30 product audits** — same state, partially absorbed only.
- **Research lane lanes that never landed as files**: Apr 18 four-lane evidence stack (OSS / product / community / synthesis memo), Apr 19 debate/council cluster (16 sessions), Apr 20 17 paper-batch extracts, Apr 21 10:53 exploration memo follow-ups, Apr 21 13:08 recall-axis taxonomy. Decision needed: keep transcripts only, or extract key paragraphs to `research/n1-memory-lab/` notes?
- **The `.omx/notepad.md` scratchpad** (in the syke product repo) has been updated 4× by the 22 MB master session. Likely untracked. Worth a look to see if anything important is there.
- **9 successful git commits originated from the master session `019da10e`** but the last 2 (`bff5a34`, `d0fd1d7`) landed only on Apr 21 02:08 and 02:18 — the user may not have reviewed these in context. These reshape the judge-calibration framing doc.
- **Duplicate "authority drift" conclusion**: both Apr 20 19:30 architecture audit and Apr 21 14:46 architecture audit converged on "path authority, source policy, and memex/runtime ownership are each split across multiple modules." Neither was turned into a ticket. This is a recurring, unresolved architectural call.

---

## 8. One-paragraph bottom line

Codex did a lot — 81 sessions, ~62 MB of transcripts, and almost certainly more than 200 hours of elapsed clock time across 4 days — but the ratio of volume to landed-code is lopsided. Roughly 70% of sessions were read-only research lanes (debate, council, paper extraction, audits), and ~25% of the non-known-big research was absorbed only as secondary input to the two KNOWN sessions or the 22 MB master. The high-impact code lands all came from **one master session (`019da10e`) plus six narrow ownership lanes on Apr 20 20:23 and 22:20**; everything else is either research-memo content not written to disk, or mountains of architectural/audit findings that were never turned into tickets. The Apr 21 14:46 six-pack in particular is a large, high-quality audit with zero follow-through. Time was over-subscribed on debate/council loops and on re-auditing the product repo (at least twice over 3 days, ~7 MB duplicated). Time was well-spent on the replay-lab infrastructure thread (master session → labctl / concurrency / clock-unification / repo split) and on the Apr 21 lane A/B/C artifacts — those are concrete, useful, and the most likely to be **in-tree but still uncommitted**. The single highest-leverage move for the user is to skim the 10 items in §6 and triage the open threads in §7 before starting any new Codex sessions.
