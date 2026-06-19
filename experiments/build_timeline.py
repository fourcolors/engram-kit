#!/usr/bin/env python3
"""Build timeline.json over all sample states into out/memory (deterministic, no LLM).

Lets us measure the memory-side change without re-running the 14-state LLM observer:
the timeline is pure parsing of changes.txt + manifest.tsv, identical to what the
incremental observer would produce.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "submissions" / "agent-memory" / "src"))

from timeline import update_timeline, timeline_asof  # noqa: E402


def main() -> int:
    mem = REPO / "experiments" / "out" / "memory"
    tl = mem / "timeline.json"
    if tl.exists():
        tl.unlink()
    states = sorted(p for p in (REPO / "sample_states").iterdir() if p.is_dir())
    for s in states:
        update_timeline(s, mem)
        print(f"  folded {s.name}")
    print(f"\ntimeline.json written to {tl}")
    asof = timeline_asof(mem, "2026-04-13")
    print(f"\nsanity — files present as of 2026-04-13: {len(asof.splitlines()) if asof else 0}")
    asof21 = timeline_asof(mem, "2026-04-21")
    print(f"sanity — files present as of 2026-04-21: {len(asof21.splitlines()) if asof21 else 0}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
