# ENGRAM Contract

ENGRAM calls your program in chronological order.

```bash
./run.sh update STATE_DIR MEMORY_DIR
./run.sh answer STATE_DIR MEMORY_DIR QUESTION_JSON ANSWER_JSON
```

`STATE_DIR` is the current bounded workspace state. `MEMORY_DIR` is your
system's persistent writable memory. `QUESTION_JSON` is the current question.
`ANSWER_JSON` is the file your system must write.

## Update

```bash
./run.sh update sample_states/2026-04-09 memory/
```

Your program should:

- read `STATE_DIR`;
- update its own memory under `MEMORY_DIR`;
- exit `0` on success.

Your program may create any files under `MEMORY_DIR`: SQLite databases, vector
indexes, Markdown notes, JSONL logs, graph stores, retrieved snippets, summaries,
or native backend exports.

## Answer

```bash
./run.sh answer sample_states/2026-04-09 memory/ question.json answer.json
```

Your program should:

- read `STATE_DIR`;
- read `MEMORY_DIR`;
- read `QUESTION_JSON`;
- write `ANSWER_JSON`;
- exit `0` on success.

## Boundary Rules

- You only get states that have been released so far.
- You do not get future states.
- You do not get private evaluation data.
- You do not get judge packets, answer keys, rubrics, or reference sets.
- You do not get other candidates' memory.
- You must treat `MEMORY_DIR` as the only durable benchmark-visible memory.
- If your system uses an external service, model API, cache, or daemon, document
  it in your submission README.

## What ENGRAM Measures

ENGRAM is not testing whether you installed a particular memory backend.

It is testing whether your system can:

- ingest changing workspace states over time;
- preserve useful memory across ticks;
- distinguish current, stale, rejected, and uncertain information;
- cite evidence;
- answer without hindsight.
