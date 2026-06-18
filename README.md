# ENGRAM Kit

ENGRAM is a small challenge for memory systems in evolving workspaces.

Your program receives dated workspace states in chronological order. It may
write anything it wants into its own memory directory. When ENGRAM asks a
question, your program answers from the current state plus that memory.

The contract is two commands:

```bash
./run.sh update STATE_DIR MEMORY_DIR
./run.sh answer STATE_DIR MEMORY_DIR QUESTION_JSON ANSWER_JSON
```

This kit is the public participant facade. It does not contain private
evaluation data, judge packets, answer keys, rubrics, QEMU details, dashboard
internals, atlas/tracks artifacts, or provider credentials.

Public repo:

```text
https://github.com/saxenauts/engram-kit
```

Direct zip download:

```text
https://github.com/saxenauts/engram-kit/releases/download/v0.1-real-first-two-weeks/engram-kit.zip
```

## Files

```text
CHECKLIST.md              readiness checklist before sharing
CONTRACT.md               the two-command interface
STATE_FORMAT.md           what STATE_DIR contains
QUESTION_FORMAT.md        question and answer JSON
SUBMISSION_FORMAT.md      required submission folder shape
PRESENTATION_PLACEMENT.md where this belongs in the deck
sample_states/            real first-two-week daily ENGRAM states
sample_questions.json     candidate-visible first-two-week questions
examples/simple_memory/   minimal working submission
check_submission.py       local contract checker
```

## Quick Start

Check the included example:

```bash
python3 check_submission.py --submission examples/simple_memory
```

Then build your own submission folder with a `run.sh` that supports:

```bash
./run.sh update STATE_DIR MEMORY_DIR
./run.sh answer STATE_DIR MEMORY_DIR QUESTION_JSON ANSWER_JSON
```

Passing `check_submission.py` only proves that your package speaks the interface.
It is not benchmark evidence and it does not predict private-eval score.

## What To Build

Build any memory system you want: a graph, vector index, Markdown memory,
SQLite store, local agent loop, wrapped open-source backend, or custom pipeline.

ENGRAM only requires that your system can:

- read dated workspace states;
- maintain persistent memory under `MEMORY_DIR`;
- answer from current state plus prior memory;
- cite evidence paths;
- handle stale, current, superseded, and uncertain information;
- run without manual intervention through the two-command interface.
