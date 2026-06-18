# NE_TIMELINE_V1

## Three-month benchmark arc

```text
Jan 2026                           Feb 2026                                Mar 2026                                Apr 2026
|----------------------------------|---------------------------------------|---------------------------------------|---------------|
Jan 09                         Feb 08 Feb 09                        Mar 08 Mar 09                        Apr 08
NE-1.1                           | NE-1.2                                  | NE-1.3                                  |
```

## Dataset windows

| Dataset | Start | End | What it is for |
|---|---:|---:|---|
| `NE-1.1` | 2026-01-09 | 2026-02-08 | early benchmark/eval pressure, local-memory control, early continuity drift |
| `NE-1.2` | 2026-02-09 | 2026-03-08 | main fragmentation threshold and strongest cross-harness continuity pressure |
| `NE-1.3` | 2026-03-09 | 2026-04-08 | post-burst and current-era raw-harness continuation regime |

## Important slices in this arc

| Slice | Window | Lives inside |
|---|---:|---|
| `S01` | 2025-12-23 -> 2025-12-24 | pre-arc control evidence, still useful as historical control |
| `S03` | 2026-02-23 | `NE-1.2` |
| `S04` | 2026-02-25 -> 2026-02-26 | `NE-1.2` |
| `S05` | 2026-02-27 -> 2026-03-01 | `NE-1.2` |
| `S07` | 2026-03-13 -> 2026-03-14 | `NE-1.2` |
| `S08` | 2026-03-15 -> 2026-03-16 | boundary of `NE-1.2` / `NE-1.3` |

## Reading the arc

- `NE-1` should tell us where local or control-like memory is still enough and where the drift begins.
- `NE-1.2` is the most important dataset right now because it contains the strongest current benchmark slices.
- `NE-1.3` is the forward-facing dataset where the modern raw-harness system and replay stack should be evaluated.
