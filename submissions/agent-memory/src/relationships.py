"""Deterministic relationship + change facts (no LLM).

Relationships live as plain text — there is no JSON edge store. Two outputs, both
computed from changes.txt + manifest.tsv:

- change_summary(state_dir): an ANSWER-TIME summary for the reference snapshot —
  transition counts, relocations, files-under-archive, version supersession. It is
  computed from the state the question is asked against, so it is reflection-immune
  and no-hindsight by construction. Fixes "what changed / what superseded" miscounts.
- relationship_bullets(state_dir): dated 🔗 plain-text lines recording the
  relationships that became true THIS day, appended to the observational memory.
"""
from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

from util import read_text

ARCHIVE_MARKERS = ("/archive/", "benchmark-legacy", "/legacy/")
_VER = re.compile(r"_v(\d+)\b", re.I)


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


def _manifest_paths(state_dir: Path) -> list[tuple[str, str]]:
    out = []
    for i, line in enumerate(read_text(state_dir / "manifest.tsv").splitlines()):
        if i == 0 and line.startswith("path\t"):
            continue
        c = line.split("\t")
        if len(c) >= 4 and c[0].strip():
            out.append((c[0].strip(), c[3].strip()))
    return out


def _relocations(rows) -> list[tuple[str, str]]:
    """Same basename deleted at one path and (re)added at another on the same day."""
    deleted, added = defaultdict(list), defaultdict(list)
    for kind, _o, _n, p in rows:
        b = p.rsplit("/", 1)[-1]
        if kind.startswith("deleted"):
            deleted[b].append(p)
        elif kind.startswith("added"):
            added[b].append(p)
    relocs = []
    for b, dpaths in deleted.items():
        for dp in dpaths:
            for ap in added.get(b, []):
                if dp != ap:
                    relocs.append((dp, ap))
    return relocs


def _archive_subdirs(paths) -> Counter:
    counts: Counter = Counter()
    for p, _st in paths:
        for m in ARCHIVE_MARKERS:
            if m in p:
                key = m.strip("/")
                counts[key] += 1
                break
    return counts


def _version_supersessions(paths) -> list[tuple[str, list[str]]]:
    """Group filenames into version families; the canonical member supersedes the rest."""
    fam: dict[str, list[str]] = defaultdict(list)
    for p, _st in paths:
        b = p.rsplit("/", 1)[-1]
        stem = _VER.sub("", b)
        fam[stem].append(p)
    out = []
    for _stem, ps in fam.items():
        if len(ps) < 2 or not any(_VER.search(p.rsplit("/", 1)[-1]) for p in ps):
            continue  # need a real version difference to claim supersession

        def rank(p):
            b = p.rsplit("/", 1)[-1]
            m = _VER.search(b)
            ver = int(m.group(1)) if m else 999  # unnumbered = newest/canonical
            archived = any(mk in p for mk in ARCHIVE_MARKERS)
            return (not archived, ver, -p.count("/"))

        ordered = sorted(ps, key=rank, reverse=True)
        out.append((ordered[0], ordered[1:]))
    return out


def change_summary(state_dir: Path) -> str:
    """Deterministic, authoritative change/relationship facts for this reference state."""
    rows = _change_rows(state_dir)
    paths = _manifest_paths(state_dir)
    parts: list[str] = []

    counts = Counter((k, o, n) for k, o, n, _p in rows)
    if counts:
        parts.append("Transition counts this state — "
                     + "; ".join(f"{k} {o}→{n}: {c}" for (k, o, n), c in
                                 sorted(counts.items(), key=lambda x: -x[1])))
    relocs = _relocations(rows)
    if relocs:
        shown = "; ".join(f"{d} → {a}" for d, a in relocs[:6])
        parts.append(f"Relocations ×{len(relocs)} (basename deleted then re-added): {shown}"
                     + (" …" if len(relocs) > 6 else ""))
    arch = _archive_subdirs(paths)
    if arch:
        parts.append("Files under archive paths (path-level signal) — "
                     + "; ".join(f"{k}: {c}" for k, c in arch.most_common()))
    sup = _version_supersessions(paths)
    if sup:
        shown = "; ".join(f"{c.rsplit('/', 1)[-1]} supersedes {', '.join(o.rsplit('/', 1)[-1] for o in os)}"
                          for c, os in sup[:6])
        parts.append(f"Version supersession (by filename lineage): {shown}")

    if not parts:
        return ""
    return ("## deterministic change & relationship facts (computed from changes.txt + "
            "manifest.tsv — AUTHORITATIVE for counts, relocations, archival, supersession)\n"
            + "\n".join("- " + p for p in parts))


def relationship_bullets(state_dir: Path) -> list[str]:
    """🔗 dated plain-text relationship lines for the observational memory (this day)."""
    rows = _change_rows(state_dir)
    paths = _manifest_paths(state_dir)
    added_today = {p for k, _o, _n, p in rows if k.startswith("added")}
    bullets: list[str] = []

    for d, a in _relocations(rows)[:3]:
        bullets.append(f"🔗 relocated `{d}` → `{a}` (same basename deleted then re-added) — old path now stale")
    arch_today = [p for p in added_today if any(m in p for m in ARCHIVE_MARKERS)]
    if arch_today:
        bullets.append(f"🔗 {len(arch_today)} file(s) entered archive/legacy paths today")
    for canon, others in _version_supersessions(paths):
        if canon in added_today:
            bullets.append(f"🔗 `{canon.rsplit('/', 1)[-1]}` supersedes "
                           f"`{', '.join(o.rsplit('/', 1)[-1] for o in others)}` (version lineage)")
    return bullets[:5]
