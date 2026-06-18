# Simple Memory Example

This is a minimal ENGRAM submission.

It stores one JSONL record per update in `MEMORY_DIR/memory.jsonl`. At answer
time, it searches the current state files for simple keywords and writes an
answer JSON.

It is intentionally weak. It proves the two-command interface only.

Run it from the kit root:

```bash
python3 check_submission.py --submission examples/simple_memory
```
