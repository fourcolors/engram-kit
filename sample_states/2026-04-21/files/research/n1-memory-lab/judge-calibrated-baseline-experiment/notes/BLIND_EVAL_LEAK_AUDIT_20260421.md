# Blind-Eval Leak Audit — What the Judge Must Not See

Scope: every identity- or condition-carrying signal the Pi judge can observe
via `packet.json`, its workspace, the `slice/` symlink, or `local_git_anchor.json`.
Evidence: `benchmark_runner.py` + four real cells across `runs/`.

Sampled packets:
- `runs/ne13-real-15d-gpt54-final-20260420T071500Z/evidence/production/R01/packet.json`
- `runs/ne13-real-15d-gpt54-final-20260420T071500Z/evidence/production/R01/index.json`
- `runs/ne13-real-15d-opus46-final-20260420T071500Z/evidence/pure/R08/packet.json`
- `runs/ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z/evidence/zero/R05/packet.json`
- `runs/ne13-real-15d-gpt54-final-20260420T071500Z/evidence/production/R01/slice/adapters/claude-code.md`

## 1. Summary table

| # | Candidate | Status | Severity | Evidence | Mask |
|---|---|---|---|---|---|
| 1 | `raw_context.replay_state.condition` | SAFE (masked if env set) | — | `benchmark_runner.py:720` | already `[MASKED]` under `SYKE_BLIND_CONDITION=1` |
| 2 | `raw_context.replay_state.ask_mode` | SAFE (masked if env set) | — | `benchmark_runner.py:721` | same env as (1) |
| 3 | `answer.metadata.provider` | **LEAKS** | HIGH | `production/R01/packet.json` line: `"provider": "openai-codex"`; `pure/R08/packet.json` line: `"provider": "azure-anthropic-foundry"` | replace with `"[MASKED]"` |
| 4 | `answer.metadata.model` | **LEAKS** | HIGH | `production/R01/packet.json`: `"model": "gpt-5.4"`; `pure/R08/packet.json`: `"model": "claude-opus-4-6"` | replace with `"[MASKED]"` |
| 5 | `answer.metadata.backend` | **LEAKS** (weak) | MED | `"backend": "pi"` in every packet; harmless in practice but identifies the stack; trivial to mask | replace with `"[MASKED]"` |
| 6 | `answer.metadata.cost_usd` | **LEAKS** | HIGH | R01 prod `0.02691`, R05 zero `0.09643`, R08 pure `0`. $0 is the Azure/foundry signature; $0.09 is OpenAI | OMIT field |
| 7 | `answer.metadata.duration_ms` | **LEAKS** | MED | R01 `143358`, R08 `24455`, R05 `293165` — latency fingerprint per model | OMIT field |
| 8 | `answer.metadata.input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `tool_calls`, `num_turns` | **LEAKS** | MED | R08 `input_tokens=1`, `cache_write_tokens=745` (opus/foundry signature); R05 `input_tokens=8461`, `cache_write_tokens=0`, `num_turns=26` (codex signature). `tool_calls` + `num_turns` are per-model tactical fingerprints. | OMIT all 6 fields |
| 9 | `answer.metadata.transport` | SAFE | LOW | constant `"benchmark"` everywhere; not discriminative | keep |
| 10 | `answer.metadata.error` | SAFE | LOW | null in sampled cells; surfaces actual failures the judge needs to see | keep (but consider masking model-specific error strings) |
| 11 | `raw_context.replay_state.memex_chars` | **LEAKS** | HIGH | R01 prod `125`, R08 pure `0`, R05 zero `1262`. Zero for `pure`, nonzero for others — a near-perfect condition discriminator. | OMIT field |
| 12 | `raw_context.slice_dir` | **LEAKS** | HIGH | `/Users/saxenauts/.syke-lab/ne13-real-15d-gpt54-final-20260420T071500Z/slices/NE-1.3__R01` — run slug contains `gpt54` vs `opus46` vs `gpt54ask-opusjudge` | replace with `"[MASKED]"` (slice already reachable via local `./slice/` symlink in the judge workspace) |
| 13 | `local_git_set.path` | **LEAKS** (indirectly) | LOW | tmpdir path like `/var/folders/.../syke-judge-x6pgv4k9/local_git_anchor.json`; doesn't contain the run slug but is noisy. `_judge_probe` passes `local_git_anchor path: {...}` into the judge prompt at `benchmark_runner.py:1007` where it IS a tmpdir with no slug. Verify: yes, tmpdir is `tempfile.TemporaryDirectory(prefix="syke-judge-")` at `:1135` — **no slug leak here.** | replace packet field with `"local_git_anchor.json"` (relative) for cleanliness |
| 14 | `slice/adapters/claude-code.md` (copied into judge workspace; visible via `./slice/adapters/`) | **LEAKS** | HIGH | File body contains run slug: `/Users/saxenauts/.syke-lab/ne13-real-15d-gpt54-final-20260420T071500Z/slices/NE-1.3__R01/harnesses/...` and similarly `ne13-real-15d-opus46-final-...` in the opus run. See `evidence/production/R01/slice/adapters/claude-code.md` lines ~7-8 and parallel file in `opus46-final` run. Judge reads adapters. | rewrite "Where" paths to slug-free relative paths at slice build time, OR mask at copy time |
| 15 | `answer.text` self-identification | SAFE in sampled cells | LOW | R01/R08/R05 answers do not self-identify as Claude/GPT. But this is content we cannot guarantee — noted in §6. | cannot mask without destroying the answer |
| 16 | Trace files (`traces/<condition>/*.response.txt`, `*.judge_trace.json`, `*.ask_*.*`) | SAFE | — | `trace_dir = output_dir / "traces" / condition` at `:1647`/`:1808`/`:1923`/`:2065`. Judge runs in a separate `tmpdir` + `judge_workspace` under `~/.syke-lab/<scope>/judges/<run_id>__<uuid>/workspace/`. The `runs/<slug>/traces/` tree is **not** bind-mounted or symlinked into the judge workspace. Confirmed: only `packet.json`, `judge_schema.json`, `slice/` symlink, `local_git_anchor.json` (tmpdir copy), and workspace files (`syke.db`, `REFERENCE_TIME.md`, `.pi/extensions/...`, `.time-sandbox/bin/date`, `adapters/*.md`) exist in the judge view. | no action — already isolated |
| 17 | `judge_workspace` path — `~/.syke-lab/{judge_scope}/judges/{run_id}__{uuid}/workspace` | **LEAKS (via pwd/cwd)** | HIGH | `benchmark_runner.py:1179`: `judge_scope = trace_dir.parent.parent.name` → full run slug (e.g. `ne13-real-15d-gpt54-final-20260420T071500Z`). Workspace path is bound as cwd via `temporary_workspace_binding` at `:1228`. If judge runs `pwd`, `echo $PWD`, `ls ~/..`, or any tool that logs cwd, slug is visible. `run_id = f"{condition}_{probe_id}"` at `:1133` — also leaks condition. | use a hashed / UUID-only scope path; drop slug and condition from `judge_workspace` and `run_id` |
| 18 | `REFERENCE_TIME.md` | SAFE | — | `benchmark_runner.py:760-767` writes only time info. No identity. | keep |
| 19 | `local_git_anchor.json` body | SAFE (user-approved content) | — | Contains user's commits + `author_email: saxenauts@gmail.com`. Identifies the user, not the agent/condition. Identical across arms for the same `reference_dt`. Not a blinding concern. | keep |
| 20 | `judge_schema.json` | SAFE | — | Constant `JUDGE_SCHEMA`; no identity metadata. | keep |
| 21 | `.pi/extensions/judge_determinism.ts` | **LEAKS (indirectly)** | MED | `benchmark_runner.py:1017-1031`: when `judge_provider == "anthropic"`, file contains `"{ ...event.payload, temperature: 0 }"`; otherwise `"event.payload"`. Tells the judge *which provider it itself is running on* (self-identification via workspace file). Doesn't identify the agent being judged, but breaks judge-blinding. | write both branches identically, or place file outside `judge_workspace` |
| 22 | `adapters/codex.md` (second adapter file copied to workspace) | needs inspection (likely same slug leak) | HIGH | Same `shutil.copy2` loop at `:1201-1203` copies both `claude-code.md` and `codex.md`. Slug likely in both. | same fix as (14) |
| 23 | `probe.source_ref` | SAFE for blinding | — | e.g. `/Users/saxenauts/.claude/transcripts/ses_334d16f7dffepp0fpzQhpVSxN4.jsonl#L4` — identifies the *probe source*, not the agent or condition. Same across arms for the same probe. | keep (already called out as a host-path concern in `JUDGE_VIEW_AUDIT_20260421.md` §4.4, separate issue) |
| 24 | `raw_context.slice_summary.total_elapsed_sec` | SAFE for blinding | — | Slice-build time, not agent-run time; per-probe, not per-condition. | keep |
| 25 | Slice JSONL harness files | SAFE for blinding | — | `grep -c "claude-opus\|gpt-5"` on a sample `ne13-...-opus46-...` slice JSONL returned 0. Slice content is user's prior activity, not the agent-under-test's. | keep |

## 2. Confirmed leaks, ranked by severity

### HIGH

**L1 — `answer.metadata.model` and `.provider`** (`_build_real_ask_packet` writes `answer_metadata` as-is at `benchmark_runner.py:712`). Real values observed:
- `"provider": "openai-codex", "model": "gpt-5.4"` (gpt54 arm)
- `"provider": "azure-anthropic-foundry", "model": "claude-opus-4-6"` (opus46 arm)

This is the **primary self-preference vector**: an Opus judge seeing `model: "claude-opus-4-6"` can bias toward same-family answers; a GPT judge can do the reverse.

**L2 — `answer.metadata.cost_usd`** (same code path, same line). `cost_usd=0` is a near-certain Azure/Foundry signature (R08 pure: 0; R01 prod gpt54: 0.02691). The judge can reconstruct the provider even if model/provider fields are stripped.

**L3 — `raw_context.replay_state.memex_chars`** (`benchmark_runner.py:722`). `memex_chars=0` ⇒ `pure` with near certainty; non-zero ⇒ `production` or `zero`. Paired with the masked `condition` field, this field alone almost fully de-masks.

**L4 — `raw_context.slice_dir`** (`benchmark_runner.py:714`). Full absolute path including the run slug (`ne13-real-15d-gpt54-final-...` vs `...-opus46-final-...` vs `...-gpt54ask-opusjudge-...`). Direct agent-identity leak.

**L5 — Slice adapter markdowns** (`slice/adapters/claude-code.md`, `codex.md`; copied at `benchmark_runner.py:1201-1203` and also reachable via `./slice/adapters/` symlink). The "Where" section lists absolute paths embedding the run slug. Example lines 7-8 of the sampled adapter:
```
/Users/saxenauts/.syke-lab/ne13-real-15d-gpt54-final-20260420T071500Z/slices/NE-1.3__R01/harnesses/claude-code/projects/**/*.jsonl
```
The opus run's adapter has the identical structure with `-opus46-` substituted. Per `JUDGE_VIEW_AUDIT_20260421.md` §5, adapter markdowns *are* read by judges (R17 in particular), so this is an exercised surface.

**L6 — Judge workspace cwd path** (`benchmark_runner.py:1179-1187`). `judge_scope = trace_dir.parent.parent.name` is the run slug. `run_id = f"{condition}_{probe_id}"` at `:1133` embeds the condition. The workspace becomes `~/.syke-lab/ne13-real-15d-gpt54-final-20260420T071500Z/judges/production_R01__<uuid>/workspace`. Any `pwd` / `realpath .` / `ls ~/.syke-lab/` from the judge reveals both the agent arm (run slug) and the condition (in `run_id`).

### MED

**L7 — `answer.metadata.duration_ms`, `input_tokens`, `output_tokens`, `cache_read_tokens`, `cache_write_tokens`, `tool_calls`, `num_turns`** (all under `metadata` dict, line `:712`). Latency + token-count distributions are near-unique per model. R08 pure with `input_tokens=1` and `cache_write_tokens=745` is an instantly recognizable anthropic-foundry signature.

**L8 — `.pi/extensions/judge_determinism.ts`** (`benchmark_runner.py:1022-1031`). File body varies by `judge_provider`. A judge that reads its own workspace sees which provider it's running on — breaks judge-side blinding, not agent-side. Still an L2-style audit hole.

**L9 — `answer.metadata.backend`** (`:712`). Always `"pi"` today; only weak signal, but costs nothing to mask.

### LOW / indirect

**L10 — `local_git_set.path`** (`benchmark_runner.py:727`). Carries a tempdir path; no slug (tmpdir uses `prefix="syke-judge-"`). Recommend replacing with a relative `"local_git_anchor.json"` just for cleanliness; not a real leak.

## 3. Confirmed safe

- `probe.*` fields (probe_id, question, family, reference_dt, reference_cutoff_iso, source_surface, source_ref) — probe identity, identical across arms for the same probe.
- `answer.text` — sampled cells do not self-identify the model. (Content-level risk: see §6.)
- `judge_brief` — constant boilerplate; identical across all 19 probes × 3 conditions (see `JUDGE_VIEW_AUDIT_20260421.md` §1, §4.1).
- `local_git_anchor.json` body — user-level, identical across arms.
- `REFERENCE_TIME.md` — time-only.
- `judge_schema.json` — schema-only.
- `.time-sandbox/bin/date` — frozen-time binary; identical across arms.
- `traces/` directory under `runs/<slug>/` — not visible from the judge workspace. Judge tmpdir + `~/.syke-lab/<scope>/judges/...` are the only paths reachable.
- Slice JSONL content — user's prior activity; does not name the agent-under-test.

## 4. Unknown — needs inspection

- **`syke.db`** (`benchmark_runner.py:1207`). Created empty by `SykeDB(db_path)`. If its schema or any auto-inserted rows reference the agent or provider, that would leak. Quick check: the constructor creates tables only. Marking likely-safe but unverified.
- **`probe.source_ref` host transcripts**. Separately discussed in `JUDGE_VIEW_AUDIT_20260421.md`; a judge dereferencing the host path sees the user's live transcript. Not a blinding concern (same path across arms), but orthogonal hygiene issue.
- **`adapters/codex.md`** content not inspected in this audit; `claude-code.md` has the slug, and the copy loop at `:1201-1203` is uniform, so codex.md almost certainly does too.
- **Judge tool sandbox** — does the Pi judge ever receive `os.environ` dumps or process-env from the host? If so, env vars set in `_temporary_env` (`:1233-1244`) like `SYKE_PROVIDER=<judge_provider>` and `TZ=...` might surface. Agent-under-test env is different scope; this is judge-side only.

## 5. Proposed `SYKE_BLIND_PACKET` env-var expansion

When `SYKE_BLIND_PACKET=1`, `_build_real_ask_packet` and `_judge_probe` should apply all of:

Packet-level (in `_build_real_ask_packet`):
- `answer.metadata.backend` → `"[MASKED]"`
- `answer.metadata.provider` → `"[MASKED]"`
- `answer.metadata.model` → `"[MASKED]"`
- `answer.metadata.cost_usd` → OMIT
- `answer.metadata.duration_ms` → OMIT
- `answer.metadata.input_tokens` → OMIT
- `answer.metadata.output_tokens` → OMIT
- `answer.metadata.cache_read_tokens` → OMIT
- `answer.metadata.cache_write_tokens` → OMIT
- `answer.metadata.tool_calls` → OMIT
- `answer.metadata.num_turns` → OMIT
- `answer.metadata.transport` → keep (`"benchmark"`)
- `answer.metadata.error` → keep (null or short literal)
- `raw_context.slice_dir` → `"[MASKED]"`
- `raw_context.replay_state.memex_chars` → OMIT (or coarse bucket `"0"` / `"nonzero"` if diagnostic access needed)
- `local_git_set.path` → `"local_git_anchor.json"` (relative, strip tmpdir)

Workspace-level (in `_judge_probe`):
- `judge_scope` → replace `trace_dir.parent.parent.name` with a blinded token (e.g. `sha256(run_slug)[:8]` or constant `"run"`). Effect: workspace becomes `~/.syke-lab/run/judges/<uuid>/workspace`.
- `run_id` → replace `f"{condition}_{probe_id}"` with `f"{probe_id}__{uuid.uuid4().hex[:8]}"` (strip `condition`). Downstream trace filenames under `runs/<slug>/traces/<condition>/` are outside the judge view, so the runner can still use `condition` there.
- Slice adapters copied to `judge_workspace/adapters/` → scrub slug substrings from file body before `shutil.copy2` (regex on `ne13-real-15d-*-final-*` + any run-slug pattern), or rewrite `"Where"` paths to `./slice/harnesses/...`.
- `.pi/extensions/judge_determinism.ts` → write a single provider-agnostic body, or move outside `judge_workspace` and install via env.

Runner-level (orthogonal to env var, but needed for true blinding):
- When slice is built, embed slug-free relative paths in `adapters/*.md` so the same slice is reusable across arms.

## 6. Things we can't blind, and how to handle them

- **Answer length, phrasing, markdown idiom, emoji usage, bullet structure.** Claude-family and GPT-family outputs have stylistic fingerprints (header depth, sentence rhythm, use of `**bold**` vs `##` headers, em-dash frequency). Masking destroys the answer. Document as a residual confound; mitigate by paired-judge reruns (each judge scores both families under identical mask) rather than by redaction.
- **Self-identification in the answer text.** Sampled cells do not self-identify, but a future answer could include "As Claude, I would..." or "ChatGPT here...". Add a post-hoc detector (regex against known model/brand names in `answer.text`) that flags contaminated cells for exclusion from blind analyses, rather than silently rewriting the answer.
- **`cost_usd == 0` inference from latency alone.** Even if every cost/token field is stripped, the Azure-foundry cost=0 pattern correlates with long `cache_write_tokens` signatures in log streams outside `packet.json`. Since those streams are not in the judge's view, this is contained — but worth a note.
- **Slice-size × answer-length joint distribution.** Longer answers in `zero` vs `production` (see `JUDGE_VIEW_AUDIT_20260421.md` §6: "zero-condition answers run long") is an emergent signal the judge could learn if trained. For single-shot judges this is unlikely to matter but deserves a footnote in the blinding limitations.
- **`local_git_anchor.json` author/email**. `"author_email": "saxenauts@gmail.com"` identifies the user, not the agent; this is the same value in every arm and is not a blinding concern, only a privacy one. Left unchanged.

End of audit.
