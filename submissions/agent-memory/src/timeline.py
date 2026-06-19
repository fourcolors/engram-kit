"""Deterministic per-file timeline, built from changes.txt + manifest.tsv.

No LLM. Each `update` folds the day's structured signals into a running index:
per path — first_seen, status history, present/deleted. The answer pass reads a
date-filtered view as the AUTHORITATIVE source for first-appearance, status-as-of,
and existence facts — so it never has to re-derive them (the root cause of the
attribution/hedge failures the answer-side patches couldn't fix).
"""
from __future__ import annotations

import json
from pathlib import Path

from util import read_text

TIMELINE = "timeline.json"


def _manifest_status(state_dir: Path) -> dict:
    """path -> status (exact|approximate) from manifest.tsv."""
    out: dict[str, str] = {}
    for i, line in enumerate(read_text(state_dir / "manifest.tsv").splitlines()):
        if i == 0 and line.startswith("path\t"):
            continue
        cols = line.split("\t")
        if len(cols) >= 4 and cols[0].strip():
            out[cols[0].strip()] = cols[3].strip()
    return out


def _change_rows(state_dir: Path) -> list[tuple[str, str, str, str]]:
    rows, started = [], False
    for line in read_text(state_dir / "changes.txt").splitlines():
        if line.startswith("change_kind"):
            started = True
            continue
        if not started:
            continue
        c = line.split("\t")
        if len(c) >= 4 and c[3].strip():
            rows.append((c[0], c[1], c[2], c[3].strip()))
    return rows


def update_timeline(state_dir: Path, memory_dir: Path) -> None:
    """Fold one day's snapshot into MEMORY_DIR/timeline.json (deterministic)."""
    memory_dir.mkdir(parents=True, exist_ok=True)
    path = memory_dir / TIMELINE
    data = json.loads(read_text(path)) if path.exists() else {"files": {}}
    files = data["files"]
    date = state_dir.name

    status = _manifest_status(state_dir)
    for fp, st in status.items():
        rec = files.setdefault(fp, {"first_seen": date, "status_history": [], "events": []})
        rec["present"] = True
        rec.pop("deleted", None)
        rec["last_seen"] = date
        if not rec["status_history"] or rec["status_history"][-1][1] != st:
            rec["status_history"].append([date, st])

    present = set(status)
    for kind, old, new, fp in _change_rows(state_dir):
        rec = files.setdefault(fp, {"first_seen": date, "status_history": [], "events": []})
        rec["events"].append([date, kind, old, new])
        if kind.startswith("deleted") and fp not in present:
            rec["present"] = False
            rec["deleted"] = date

    path.write_text(json.dumps(data, indent=1, sort_keys=True), encoding="utf-8")


def timeline_asof(memory_dir: Path, ref_date: str) -> str | None:
    """Compact, date-filtered view of files present as of ref_date.

    One line per file: path — first seen DATE; status S [archived]. No file that
    first appears after ref_date, and no file deleted on/before ref_date, is shown.
    """
    path = memory_dir / TIMELINE
    if not path.exists():
        return None
    data = json.loads(read_text(path))
    lines: list[tuple[str, str]] = []
    for fp, rec in data["files"].items():
        if rec.get("first_seen", "9999") > ref_date:
            continue
        hist = [(d, s) for d, s in rec.get("status_history", []) if d <= ref_date]
        if not hist:
            continue
        deleted = rec.get("deleted")
        if deleted and deleted <= ref_date:
            continue
        archived = "/archive/" in fp or "benchmark-legacy" in fp
        tag = " [archive path]" if archived else ""
        lines.append((rec["first_seen"], f"files/{fp} — first seen {rec['first_seen']}; status {hist[-1][1]}{tag}"))
    lines.sort()
    return "\n".join(line for _, line in lines) if lines else None
