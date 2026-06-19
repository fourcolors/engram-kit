# agent-memory — ENGRAM submission

An ENGRAM memory system built on the **agent-memory** observational discipline
(the `subagent-memory` skill): a single `MEMORY.md` of dated observation bullets,
maintained by an LLM-run **observer pass** on each daily state and read back by
an **answer pass** for each question.

This is the **stock-first baseline**: it applies the unmodified observer /
reflector discipline so we can measure how the memory substrate performs on
ENGRAM before adapting it (e.g. adding no-hindsight date-filtering at answer
time).

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
