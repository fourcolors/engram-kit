# Submission Format

Submit one folder.

```text
my-submission/
  README.md
  run.sh
  requirements.txt      # optional
  src/                  # optional
```

`run.sh` is the only required executable entrypoint.

```bash
./run.sh update STATE_DIR MEMORY_DIR
./run.sh answer STATE_DIR MEMORY_DIR QUESTION_JSON ANSWER_JSON
```

## `README.md`

Explain:

- what memory system you built;
- what it stores in `MEMORY_DIR`;
- whether it uses a model, network, daemon, database, or external service;
- how to install dependencies;
- how to reset/export its memory;
- known limitations.

## `run.sh`

Requirements:

- accepts `update` and `answer`;
- exits nonzero on failure;
- writes `ANSWER_JSON` during answer;
- does not require manual steps during a run.

## Dependencies

Keep dependencies boring where possible. If your system needs a service,
database, model API, hosted account, GPU, or broader network access, declare it.

ENGRAM may reject or rerun submissions whose resource needs do not fit the
event environment.

## Local Check

From `engram-kit/`:

```bash
python3 check_submission.py --submission path/to/my-submission
```

This runs update over the sample states, asks one sample question, and validates
that `ANSWER_JSON` has the required shape.
