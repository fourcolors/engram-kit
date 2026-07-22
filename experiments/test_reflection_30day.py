#!/usr/bin/env python3
"""30-day reflection safety test.

Simulates a long (30-day) memory that crosses the reflection threshold, runs a
REAL reflector pass, and asserts the invariants that keep no-hindsight + relationships
intact at scale:
  1. reflection_is_safe() accepts safe compressions and rejects unsafe ones (unit).
  2. After a real reflector pass: every Date header survives, every 🔗 fact survives.
  3. No-hindsight holds THROUGH reflection: an as-of-early-date read excludes a
     fact that was only true on a later date.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "submissions" / "agent-memory" / "src"
sys.path.insert(0, str(SRC))

import observer  # noqa: E402
from memory import read_memory_asof  # noqa: E402


def _synthetic_memory() -> str:
    lines = ["# Observational memory", ""]
    for day in range(1, 31):
        d = f"2026-05-{day:02d}"
        lines += [f"Date: {d}", ""]
        lines.append(f"🟡 (day {day}) routine note about file_{day}.md status approximate")
        lines.append(f"🟢 (day {day}) minor ambient detail number {day} — low value noise")
        if day == 5:
            lines.append("🔗 `EVAL_SET_V2.yaml` supersedes `EVAL_SET_V1.yaml` (version lineage)")
        if day == 28:
            lines.append("🔴 (day 28) ARCHIVED: legacy/ benchmark moved; treat as historical machinery")
            lines.append("🔗 relocated `a/old.md` → `b/new.md` (same basename) — old path now stale")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    ok = True

    # 1. unit: the guard
    before = "Date: 2026-05-01\n🔗 x supersedes y\n🟢 noise\nDate: 2026-05-02\n🟡 fact"
    safe = "Date: 2026-05-01\n🔗 x supersedes y\nDate: 2026-05-02\n🟡 fact"     # dropped noise only
    drop_date = "Date: 2026-05-01\n🔗 x supersedes y\n🟡 fact"                    # lost a date
    drop_link = "Date: 2026-05-01\n🟢 noise\nDate: 2026-05-02\n🟡 fact"          # lost the 🔗
    assert observer.reflection_is_safe(before, safe) is True, "safe compression rejected"
    assert observer.reflection_is_safe(before, drop_date) is False, "dropped date accepted!"
    assert observer.reflection_is_safe(before, drop_link) is False, "dropped 🔗 accepted!"
    print("1. guard unit test: PASS (accepts safe, rejects dropped date / dropped 🔗)")

    # 2 + 3. real reflector pass on a 30-day memory that exceeds the threshold
    tmp = Path(tempfile.mkdtemp(prefix="engram-reflect-"))
    try:
        mem = tmp / "MEMORY.md"
        mem.write_text(_synthetic_memory(), encoding="utf-8")
        before_text = mem.read_text()
        n_before = len(before_text.splitlines())
        observer.REFLECT_AT, observer.REFLECT_TO = 120, 70  # force reflection
        observer._maybe_reflect(tmp, model="sonnet")
        after_text = mem.read_text()
        n_after = len(after_text.splitlines())

        dates_after = observer._dates(after_text)
        links_after = observer._links(after_text)
        reflected = n_after < n_before

        print(f"2. real reflector: {n_before} -> {n_after} lines "
              f"({'compressed' if reflected else 'kept (rejected unsafe / no gain)'})")
        print(f"   dates preserved: {len(dates_after)}/30   |   🔗 facts preserved: {len(links_after)}/2")
        if len(dates_after) != 30:
            ok = False; print("   FAIL: lost a Date header")
        if len(links_after) != 2:
            ok = False; print("   FAIL: lost a 🔗 relationship fact")

        # 3. no-hindsight through reflection: as-of day 10 must NOT see the day-28 archived fact
        asof10 = read_memory_asof(tmp, "2026-05-10")
        leak = "ARCHIVED" in asof10 or "2026-05-28" in asof10 or "b/new.md" in asof10
        print(f"3. no-hindsight (as-of 2026-05-10 excludes day-28 facts): "
              f"{'PASS' if not leak else 'FAIL — leak!'}")
        if leak:
            ok = False
        # and the day-5 supersession SHOULD be visible as of day 10
        has_early = "supersedes" in asof10
        print(f"   (sanity: day-5 supersession visible as-of day 10: {has_early})")
        if not has_early:
            ok = False; print("   FAIL: lost an in-window fact")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    print("\n" + ("ALL CHECKS PASS" if ok else "SOME CHECKS FAILED"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
