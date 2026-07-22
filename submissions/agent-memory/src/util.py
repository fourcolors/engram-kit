"""Small shared helpers for the agent-memory ENGRAM adapter."""
from __future__ import annotations

from pathlib import Path


def read_text(path: Path, limit: int | None = None) -> str:
    """Read a file as text, tolerating bad bytes. Returns '' if unreadable."""
    try:
        data = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""
    return data[:limit] if limit is not None else data


def cap_lines(text: str, n: int) -> str:
    """Keep the first n lines (mirrors the harness MEMORY.md injection cliff)."""
    lines = text.splitlines()
    return "\n".join(lines[:n])


def count_lines(text: str) -> int:
    return len(text.splitlines())


def render(template: str, **tokens: str) -> str:
    """Replace <<TOKEN>> placeholders. Avoids str.format brace collisions with JSON."""
    out = template
    for key, value in tokens.items():
        out = out.replace(f"<<{key}>>", value)
    return out
