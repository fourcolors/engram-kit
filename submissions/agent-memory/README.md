# agent-memory — ENGRAM submission

An ENGRAM memory system built on the **agent-memory** observational discipline:
an **observer pass** turns each daily state into dated `MEMORY.md` notes + a
deterministic per-file timeline (first-seen / status / supersession), and an
**answer pass** answers each question from a relevance-ranked, no-hindsight
(date-filtered) view of memory + the current state — citing evidence. It also
reads PDFs (PageIndex-style) and summarizes large data files deterministically.

> ⚠️ **RUNTIME REQUIREMENT — please read before running.**
> This submission calls a **Claude model at runtime** via the local `claude` CLI
> (Claude Code), using the host's existing Claude Code auth. **There is no
> API-key fallback.** To run it, the evaluation environment must provide **Claude
> model access** — either the `claude` CLI authenticated on `PATH`, or an
> equivalent the operator wires in. It needs **no** vector DB, GPU, database, or
> (apart from the model call) network. If your environment can't provide Claude
> access, please reach out — the model call is isolated in `src/claude_client.py`
> and can be repointed.

## Interface

```
./run.sh update STATE_DIR MEMORY_DIR
./run.sh answer STATE_DIR MEMORY_DIR QUESTION_JSON ANSWER_JSON
```

## Architecture

- **update (observer pass)** — `src/observer.py` builds a compact digest of the
  day's state (`state_meta.json`, `changes.txt` status transitions,
  `manifest.tsv` provenance, and previews of changed files), then asks the model
  to emit 1–5 dated observation bullets (🔴/🟡/🟢/✅), appended under a
  `Date: <YYYY-MM-DD>` header in `MEMORY.md`. When the file nears the 200-line
  cliff a **reflector pass** compresses it to ~100 lines.
- **answer (answer pass)** — `src/answerer.py` reads `MEMORY.md` (capped at 200
  lines) plus a digest of the *current* state, and asks the model to produce the
  ENGRAM answer JSON, citing real `evidence_paths` and stating `uncertainty`.

## What is stored in MEMORY_DIR

- `MEMORY.md` — the entire durable memory: date-grouped observation bullets.
  Nothing else. It is human-readable; reset = delete it, export = copy it.

## Models / networks / services

- **Model access required.** Uses the local `claude` CLI (`claude -p`,
  Claude Code) for the observer / reflector / answer passes. Default model
  `sonnet`; override with the `ENGRAM_MODEL` env var (`opus`, `haiku`, ...).
- **Recommended for max accuracy: `ENGRAM_MODEL=opus`.** In noise-controlled
  evaluation (3-run averaged, 20-judge), the best config scored ≈4.83/5 with Opus
  (relationships on) vs ≈4.70 with Sonnet — and Opus is far more consistent. Use
  Sonnet if the per-command time budget or cost matters (Opus answers are slower).
- **Feature flags:** `ENGRAM_REL` (relationship layer, default on), `ENGRAM_PDF`
  (PageIndex PDF reading, default off — turn on for document-content questions),
  `ENGRAM_VERIFY` / `ENGRAM_REPAIR` (answer-side passes, default off, measured
  net-neutral). The 30-day reflection-safety guard is always on.
- No database, daemon, GPU, or external API key. The `claude` CLI uses the host's
  existing Claude Code auth. All tools are disabled per call — each invocation is
  a single-turn text transformation.

## Dependencies

- Python 3 (standard library only — no `requirements.txt` needed).
- The `claude` CLI on `PATH`.

## Known limitations (stock baseline)

- **No-hindsight is not yet enforced.** The answer pass reads the whole
  `MEMORY.md`, which by answer time contains bullets dated *after* the question's
  reference time. Date-filtering is the first planned adaptation.
- The reflector's "newer statement wins" rule can erase older as-of-date detail.
- A single `claude -p` call may exceed ENGRAM's default 60s/command limit on the
  largest states; local runs set a generous timeout.
