"""Turn a STATE_DIR into a compact text digest for the LLM passes.

The two structured files in every state — `changes.txt` (status transitions)
and `manifest.tsv` (provenance: exact/approximate, evidence, notes) — are the
highest-signal inputs, so they always go in full(ish). File *contents* are
budgeted, because the final states have hundreds of files.

Two answer-side digests:
  - digest_answer_state         (STOCK): small files first to a 45 KB budget.
  - digest_answer_state_relevant (ADAPTED): rank files by relevance to the
    question (filename mentions are decisive) and include FULL bodies of the
    top-K. Fixes the stock baseline's "content unavailable" refusals, which were
    caused by the large, question-relevant files never reaching the model.
"""
from __future__ import annotations

import re
from pathlib import Path

from util import cap_lines, read_text

TEXT_EXTS = {".md", ".txt", ".tsv", ".csv", ".json", ".yaml", ".yml"}

STOPWORDS = {
    "the", "and", "for", "are", "what", "which", "should", "from", "this", "that",
    "with", "have", "has", "had", "not", "but", "its", "was", "were", "will",
    "why", "how", "when", "where", "who", "does", "did", "these", "those", "their",
    "there", "than", "into", "about", "some", "any", "can", "could", "would",
    "using", "use", "used", "treat", "treated", "found", "find", "open", "opened",
    "look", "looking", "inside", "new", "appears", "appear", "actually", "changed",
    "change", "define", "defines", "clear", "clearest", "versus", "etc", "per",
    "also", "make", "made", "here", "now", "what's", "i'm", "i", "am", "be", "as",
    "at", "by", "to", "of", "in", "on", "an", "or", "do", "is", "it",
}


def _changed_rows(changes_text: str) -> list[tuple[str, str, str, str]]:
    rows: list[tuple[str, str, str, str]] = []
    started = False
    for line in changes_text.splitlines():
        if line.startswith("change_kind"):
            started = True
            continue
        if not started:
            continue
        cols = line.split("\t")
        if len(cols) >= 4 and cols[3].strip():
            rows.append((cols[0], cols[1], cols[2], cols[3].strip()))
    return rows


def _iter_files(files_root: Path) -> list[Path]:
    if not files_root.exists():
        return []
    return sorted(p for p in files_root.rglob("*") if p.is_file())


def digest_update(state_dir: Path, *, char_budget: int = 14000) -> str:
    """Compact view of one day's snapshot for the observer pass."""
    files_root = state_dir / "files"
    changes = read_text(state_dir / "changes.txt")
    parts: list[str] = []
    parts.append("## state_meta.json\n" + read_text(state_dir / "state_meta.json"))
    parts.append("## changes.txt (status transitions since the previous day)\n"
                 + (changes or "(no changes file)"))
    parts.append("## manifest.tsv (path / status exact|approximate / evidence / notes)\n"
                 + cap_lines(read_text(state_dir / "manifest.tsv"), 130))

    previews: list[str] = []
    budget = max(0, char_budget - sum(len(p) for p in parts))
    for kind, old, new, rel in _changed_rows(changes):
        path = files_root / rel
        if path.suffix.lower() not in TEXT_EXTS or not path.is_file():
            continue
        head = read_text(path, limit=700)
        block = f"### files/{rel}  [{kind}: {old}→{new}]\n{head}"
        if len(block) > budget:
            break
        budget -= len(block)
        previews.append(block)
    if previews:
        parts.append("## previews of changed files (truncated)\n" + "\n\n".join(previews))

    return "\n\n".join(parts)


def digest_answer_state(state_dir: Path, *, char_budget: int = 45000) -> str:
    """STOCK answer-side view: small text files first until budget."""
    files_root = state_dir / "files"
    files = _iter_files(files_root)
    tree = "\n".join(f"files/{p.relative_to(files_root)}" for p in files) or "(no files)"
    parts: list[str] = [
        "## current file tree (state-relative paths usable as evidence_paths)\n" + tree,
        "## manifest.tsv\n" + cap_lines(read_text(state_dir / "manifest.tsv"), 260),
        "## changes.txt (most recent transitions)\n"
        + (read_text(state_dir / "changes.txt") or "(none)"),
    ]
    budget = max(0, char_budget - sum(len(p) for p in parts))
    bodies: list[str] = []
    for path in sorted((p for p in files if p.suffix.lower() in TEXT_EXTS),
                       key=lambda p: p.stat().st_size):
        rel = path.relative_to(files_root)
        block = f"### files/{rel}\n{read_text(path)}"
        if len(block) > budget:
            continue
        budget -= len(block)
        bodies.append(block)
    if bodies:
        parts.append("## file contents (small files; larger ones are listed in the tree only)\n"
                     + "\n\n".join(bodies))
    return "\n\n".join(parts)


def _tokenize(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9_]{3,}", text.lower()) if t not in STOPWORDS}


def _mentioned_files(question: str) -> set[str]:
    """Filename-like tokens the question explicitly names (e.g. ASK_SAMPLING_20260421.md)."""
    return {m.lower() for m in re.findall(r"[A-Za-z0-9_./-]+\.[A-Za-z0-9]{1,6}", question)}


def digest_answer_state_relevant(
    state_dir: Path, question: str, *, char_budget: int = 80000, max_full: int = 16,
) -> str:
    """ADAPTED answer-side view: full bodies of the files most relevant to the question.

    Scoring: an explicit filename mention is decisive; then filename-stem and
    directory-name mentions; then query-keyword overlap in path/content; then a
    bump for files that changed into this state.
    """
    files_root = state_dir / "files"
    all_files = _iter_files(files_root)
    text_files = [p for p in all_files if p.suffix.lower() in TEXT_EXTS]

    qlower = question.lower()
    qtoks = _tokenize(question)
    mentioned = _mentioned_files(question)
    dir_tokens = {t for t in re.findall(r"[a-z0-9-]{4,}", qlower) if t not in STOPWORDS}
    changed = {rel for _, _, _, rel in _changed_rows(read_text(state_dir / "changes.txt"))}

    scored: list[tuple[float, int, str, str]] = []
    for p in text_files:
        rel = str(p.relative_to(files_root))
        rell = rel.lower()
        base = p.name.lower()
        content = read_text(p)
        cl = content.lower()
        score = 0.0
        if base in mentioned or any(m.endswith("/" + base) or m == base for m in mentioned):
            score += 1000
        stem = base.rsplit(".", 1)[0]
        if len(stem) >= 5 and stem in qlower:
            score += 400
        for t in dir_tokens:
            if t in rell:
                score += 8
        for t in qtoks:
            if t in rell:
                score += 6
            if t in cl:
                score += 3
        if rel in changed:
            score += 4
        scored.append((score, len(content), rel, content))

    scored.sort(key=lambda x: (-x[0], x[1]))  # best first; smaller wins ties so more fit

    tree = "\n".join(f"files/{p.relative_to(files_root)}" for p in all_files) or "(no files)"
    parts = [
        "## current file tree (state-relative paths usable as evidence_paths)\n" + tree,
        "## manifest.tsv\n" + cap_lines(read_text(state_dir / "manifest.tsv"), 300),
        "## changes.txt (transitions into this state)\n"
        + (read_text(state_dir / "changes.txt") or "(none)"),
    ]
    budget = char_budget
    included: list[str] = []
    for score, length, rel, content in scored:
        if score <= 0 and included:
            continue
        block = f"### files/{rel}\n{content}"
        if len(included) >= max_full or len(block) > budget:
            continue
        budget -= len(block)
        included.append(block)
    if included:
        parts.append("## relevant file contents (full bodies, ranked by relevance to the question)\n"
                     + "\n\n".join(included))
    return "\n\n".join(parts)
