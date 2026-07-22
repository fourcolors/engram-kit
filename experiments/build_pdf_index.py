#!/usr/bin/env python3
"""Build the PageIndex-style PDF index over all states into out/memory (deterministic).

Lets us test the PDF subsystem without a full LLM rebuild. Same as what the
ENGRAM_PDF observer would produce incrementally.
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "submissions" / "agent-memory" / "src"))

from pdf_index import update_pdf_index, _load_or_build, _render_tree  # noqa: E402


def main() -> int:
    mem = REPO / "experiments" / "out" / "memory"
    states = sorted(p for p in (REPO / "sample_states").iterdir() if p.is_dir())
    t0 = time.time()
    for s in states:
        update_pdf_index(s, mem)
    print(f"built pdf_index over {len(states)} states in {time.time() - t0:.1f}s")

    import json
    idx = json.loads((mem / "pdf_index" / "index.json").read_text())
    print(f"distinct PDFs indexed: {len(idx['built'])}; path entries: {len(idx['by_path'])}")
    # show one outline-derived tree as a sanity check
    sample = REPO / "sample_states/2026-04-21/files/research/n1-memory-lab/judge-calibrated-baseline-experiment/papers/nondeterministic_verifier_202604/2025_hu_memoryagentbench.pdf"
    if sample.exists():
        tree = _load_or_build(sample, mem)
        print(f"\n=== {sample.name}: mode {tree['mode']}, {tree['pages']}pp ===")
        print(_render_tree(tree["nodes"])[:1500])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
