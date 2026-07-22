"""Read/write the single MEMORY.md observational log under MEMORY_DIR."""
from __future__ import annotations

import re
from pathlib import Path

from util import read_text

_DATE_HDR = re.compile(r"^Date:\s*(\d{4}-\d{2}-\d{2})")

HEADER = "# Observational memory\n"


def memory_path(memory_dir: Path) -> Path:
    return memory_dir / "MEMORY.md"


def read_memory(memory_dir: Path) -> str:
    return read_text(memory_path(memory_dir))


def read_memory_asof(memory_dir: Path, ref_date_iso: str) -> str:
    """No-hindsight read: keep only `Date:` sections dated <= ref_date_iso.

    Lines before the first Date header (the title) are always kept. Bullets under
    a header newer than the reference date are dropped, preventing future-state
    knowledge from leaking into an as-of-date answer.
    """
    text = read_memory(memory_dir)
    if not ref_date_iso:
        return text
    out: list[str] = []
    keep = True
    for line in text.splitlines():
        m = _DATE_HDR.match(line.strip())
        if m:
            keep = m.group(1) <= ref_date_iso
        if keep:
            out.append(line)
    return "\n".join(out)


def append_dated(memory_dir: Path, date_iso: str, bullets: str) -> None:
    """Append a new `Date: <iso>` section with the given bullet lines."""
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = memory_path(memory_dir)
    existing = read_text(path) if path.exists() else HEADER
    section = f"Date: {date_iso}\n\n{bullets.strip()}\n"
    new_text = existing.rstrip() + "\n\n" + section
    path.write_text(new_text, encoding="utf-8")


def write_memory(memory_dir: Path, text: str) -> None:
    memory_path(memory_dir).write_text(text.rstrip() + "\n", encoding="utf-8")
