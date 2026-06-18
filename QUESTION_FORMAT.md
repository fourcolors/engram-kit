# Question Format

Questions are JSON objects.

```json
{
  "id": "Q001",
  "reference_time": "2026-04-09T23:59:59-07:00",
  "question": "Which file states the current ENGRAM event direction?"
}
```

Fields:

- `id`: stable question id
- `reference_time`: the state time for the question
- `question`: natural-language question

The public sample questions are real candidate-visible first-two-week ENGRAM
questions. Private fields are removed: answers, reference sets, and rubrics do
not appear in `sample_questions.json`.

## Answer Format

Your `answer` command must write `ANSWER_JSON`.

```json
{
  "answer": "Direct answer here.",
  "evidence_paths": ["files/notes/engram-direction.md"],
  "memory_refs": ["memory.jsonl"],
  "uncertainty": "What remains unclear or unsupported."
}
```

Required:

- `answer`: string
- `evidence_paths`: list of paths supporting the answer
- `uncertainty`: string

Optional:

- `memory_refs`: list of self-memory files, keys, logs, or notes used

Evidence paths should normally point into the current `STATE_DIR`. Memory refs
should point into your own `MEMORY_DIR`. Do not blur the two: workspace evidence
and self-created memory are different surfaces.

## Failure Answers

If the state does not support a confident answer, say that plainly:

```json
{
  "answer": "Cannot determine from the released state.",
  "evidence_paths": [],
  "memory_refs": ["memory.jsonl"],
  "uncertainty": "The relevant accepted decision is not visible yet."
}
```
