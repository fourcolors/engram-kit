"""Thin wrapper around the local `claude` CLI (headless -p mode).

We use the user's existing Claude Code auth — no API key needed. Tools are
disabled so each call is a pure text transformation (observe / reflect / answer)
that returns in a single turn.
"""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

CLAUDE_BIN = shutil.which("claude") or "claude"

# Disable every tool: these passes are pure generation, no file/network actions.
_DISALLOWED = [
    "Bash", "Edit", "Write", "Read", "Glob", "Grep",
    "WebFetch", "WebSearch", "Task", "TodoWrite", "NotebookEdit",
]


class ClaudeError(RuntimeError):
    pass


def run_claude(
    prompt: str,
    *,
    model: str = "sonnet",
    timeout: int = 240,
    cwd: Path | None = None,
) -> str:
    """Run `claude -p` with the given prompt on stdin; return stdout text."""
    cmd = [
        CLAUDE_BIN, "-p",
        "--model", model,
        "--output-format", "text",
        "--disallowed-tools", *_DISALLOWED,
    ]
    try:
        proc = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(cwd) if cwd else None,
        )
    except subprocess.TimeoutExpired as exc:
        raise ClaudeError(f"claude -p timed out after {timeout}s") from exc
    if proc.returncode != 0:
        raise ClaudeError(f"claude -p exit {proc.returncode}: {proc.stderr[-1500:]}")
    return proc.stdout.strip()
