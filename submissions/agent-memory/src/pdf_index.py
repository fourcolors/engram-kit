"""PageIndex-style PDF subsystem (v1) — vectorless tree index + reasoning retrieval.

Adopts PageIndex's data model (a hierarchical node tree: node_id / title /
start_index / end_index / nodes) and its retrieval *concept* (show the LLM the
tree titles, let it pick node_ids, then fetch only those pages). Drops PageIndex's
LLM-heavy *construction*: trees are built deterministically (0 LLM calls) from the
PDF's embedded outline, else a heading regex, else fixed page windows.

- Build (update): update_pdf_index() — per-PDF tree, cached by content sha1 under
  MEMORY_DIR/pdf_index/. Deterministic, idempotent.
- Answer: select_and_extract() — rank PDFs by question relevance, ONE LLM nav call
  to pick sections, extract only those pages, return a budgeted context block.

No vectors, no embeddings, no network. Gated by ENGRAM_PDF at the call sites.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path

from claude_client import run_claude
from util import read_text, render

PROMPTS = Path(__file__).resolve().parent / "prompts"
PDF_DIR = "pdf_index"
WINDOW = 4

_SECTION_RE = re.compile(
    r"^\s*(?:\d+(?:\.\d+)*\.?\s+)?"
    r"(abstract|introduction|background|related work|preliminaries|method(?:s|ology)?|"
    r"approach|model|setup|experiment(?:s|al setup)?|results?|evaluation|analysis|"
    r"ablation[\w \-]*|discussion|limitations?|conclusions?|future work|references|"
    r"acknowledge?ments?|appendix[\w \-:]*)\s*$", re.I)

_STOP = {"the", "and", "for", "what", "which", "does", "with", "from", "this",
         "that", "are", "was", "how", "why", "its", "into", "use", "used"}


# ---------------------------------------------------------------- extraction
def _pdftotext_pages(pdf: Path) -> list[str]:
    try:
        out = subprocess.run(["pdftotext", "-q", str(pdf), "-"],
                             capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return []
    if out.returncode != 0 or not out.stdout:
        return []
    pages = out.stdout.split("\x0c")
    if pages and pages[-1].strip() == "":
        pages = pages[:-1]
    return pages


def _reader(pdf: Path):
    try:
        from PyPDF2 import PdfReader
        return PdfReader(str(pdf))
    except Exception:
        return None


def extract_pages(pdf: Path) -> list[str]:
    if shutil.which("pdftotext"):
        pages = _pdftotext_pages(pdf)
        if pages:
            return pages
    r = _reader(pdf)
    if r is not None:
        try:
            return [(_p.extract_text() or "") for _p in r.pages]
        except Exception:
            return []
    return []


# ---------------------------------------------------------------- tree build
def build_tree(pdf: Path) -> dict:
    pages = extract_pages(pdf)
    reader = _reader(pdf)
    try:
        npages = len(reader.pages) if reader is not None else len(pages)
    except Exception:
        npages = len(pages)
    npages = max(npages, len(pages), 1)

    nodes, mode = _outline_tree(reader), "A"
    if len(_flatten(nodes)) < 2:
        nodes, mode = _heading_tree(pages), "B"
    if len(_flatten(nodes)) < 2:
        nodes, mode = _window_tree(npages), "C"

    _assign_ends(nodes, npages - 1)
    _assign_ids(nodes, [0])
    return {"pages": npages, "mode": mode, "nodes": nodes}


def _outline_tree(reader) -> list:
    if reader is None:
        return []
    try:
        outline = reader.outline
    except Exception:
        return []

    def walk(items):
        res: list = []
        for it in items:
            if isinstance(it, list):
                if res:
                    res[-1].setdefault("nodes", []).extend(walk(it))
                continue
            try:
                pg = reader.get_destination_page_number(it)
            except Exception:
                pg = None
            if pg is None:
                continue
            title = (getattr(it, "title", "") or "").strip() or f"p.{int(pg) + 1}"
            res.append({"title": title[:120], "start_index": int(pg)})
        return res

    try:
        return walk(outline)
    except Exception:
        return []


def _heading_tree(pages: list[str]) -> list:
    nodes: list = []
    for i, txt in enumerate(pages):
        for line in txt.splitlines():
            s = line.strip()
            if 2 <= len(s) <= 60 and _SECTION_RE.match(s):
                if not (nodes and nodes[-1]["start_index"] == i):
                    nodes.append({"title": s, "start_index": i})
                break
    return nodes


def _window_tree(npages: int) -> list:
    nodes, s = [], 0
    while s < npages:
        e = min(s + WINDOW - 1, npages - 1)
        nodes.append({"title": f"pp. {s + 1}-{e + 1}", "start_index": s})
        s = e + 1
    return nodes


def _flatten(nodes: list) -> list:
    out = []
    for n in nodes:
        out.append(n)
        out += _flatten(n.get("nodes", []))
    return out


def _assign_ends(nodes: list, parent_end: int) -> None:
    for i, n in enumerate(nodes):
        nxt = nodes[i + 1]["start_index"] if i + 1 < len(nodes) else parent_end + 1
        n["end_index"] = max(n["start_index"], nxt - 1)
        if n.get("nodes"):
            _assign_ends(n["nodes"], n["end_index"])


def _assign_ids(nodes: list, counter: list) -> None:
    for n in nodes:
        n["node_id"] = str(counter[0]).zfill(4)
        counter[0] += 1
        if n.get("nodes"):
            _assign_ids(n["nodes"], counter)
        elif "nodes" in n:
            del n["nodes"]


# ---------------------------------------------------------------- update phase
def update_pdf_index(state_dir: Path, memory_dir: Path) -> None:
    """Build/refresh per-PDF trees for the PDFs in this state. Deterministic, idempotent."""
    files_root = state_dir / "files"
    if not files_root.exists():
        return
    idx_dir = memory_dir / PDF_DIR
    idx_dir.mkdir(parents=True, exist_ok=True)
    idx_file = idx_dir / "index.json"
    idx = json.loads(read_text(idx_file)) if idx_file.exists() else {"by_path": {}, "built": {}}
    date = state_dir.name

    for pdf in sorted(files_root.rglob("*.pdf")):
        rel = str(pdf.relative_to(files_root))
        try:
            sha1 = hashlib.sha1(pdf.read_bytes()).hexdigest()
        except OSError:
            continue
        if sha1 not in idx["built"]:
            try:
                tree = build_tree(pdf)
            except Exception:
                continue
            tf = f"{sha1}.tree.json"
            (idx_dir / tf).write_text(json.dumps(tree), encoding="utf-8")
            idx["built"][sha1] = tf
        prev = idx["by_path"].get(rel)
        idx["by_path"][rel] = {
            "sha1": sha1,
            "tree_file": idx["built"][sha1],
            "first_seen": prev["first_seen"] if prev else date,
        }
    idx_file.write_text(json.dumps(idx), encoding="utf-8")


# ---------------------------------------------------------------- answer phase
def _tok(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9_]{3,}", text.lower()) if t not in _STOP}


def _extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text[text.find("\n") + 1:] if "\n" in text else text
    i, j = text.find("{"), text.rfind("}")
    if i == -1 or j == -1:
        raise ValueError("no JSON object")
    return json.loads(text[i:j + 1])


def _load_or_build(pdf: Path, memory_dir: Path) -> dict | None:
    try:
        sha1 = hashlib.sha1(pdf.read_bytes()).hexdigest()
    except OSError:
        return None
    tf = memory_dir / PDF_DIR / f"{sha1}.tree.json"
    if tf.exists():
        raw = read_text(tf)
        if raw:
            try:
                return json.loads(raw)
            except Exception:
                pass
    try:
        return build_tree(pdf)
    except Exception:
        return None


def _render_tree(nodes: list, depth: int = 0) -> str:
    lines = []
    for n in nodes:
        lines.append("  " * depth + f"[{n['node_id']}] {n['title']} "
                     f"(pp.{n['start_index'] + 1}-{n['end_index'] + 1})")
        if n.get("nodes"):
            lines.append(_render_tree(n["nodes"], depth + 1))
    return "\n".join(lines)


def select_and_extract(state_dir: Path, memory_dir: Path, question: str, *,
                       model: str = "sonnet", top_n: int = 3,
                       char_budget: int = 30000) -> str:
    """Rank PDFs, navigate their trees in one LLM call, return page-scoped extracts.

    No-hindsight is automatic: only PDFs physically present in this state_dir (the
    reference-time snapshot) are considered.
    """
    files_root = state_dir / "files"
    pdfs = sorted(files_root.rglob("*.pdf")) if files_root.exists() else []
    if not pdfs:
        return ""

    qtoks = _tok(question)
    mentioned = {m.lower() for m in re.findall(r"[\w./-]+\.pdf", question.lower())}
    cand = []
    for pdf in pdfs:
        rel = str(pdf.relative_to(files_root))
        base = pdf.name.lower()
        tree = _load_or_build(pdf, memory_dir)
        if not tree or not tree.get("nodes"):
            continue
        titles = " ".join(n["title"] for n in _flatten(tree["nodes"])).lower()
        score = 0.0
        if base in mentioned or any(base in m for m in mentioned):
            score += 1000
        for tok in qtoks:
            if tok in base:
                score += 40
            if tok in rel.lower():
                score += 6
            if tok in titles:
                score += 4
        cand.append((score, rel, pdf, tree))

    cand.sort(key=lambda x: -x[0])
    cand = [c for c in cand if c[0] > 0][:top_n]
    if not cand:
        return ""

    trees_block = "\n\n".join(
        f"### files/{rel}  ({tree['pages']}pp, mode {tree['mode']})\n{_render_tree(tree['nodes'])}"
        for _, rel, _, tree in cand)
    nav_prompt = render((PROMPTS / "pdf_nav.md").read_text(encoding="utf-8"),
                        QUESTION=question, TREES=trees_block)
    try:
        selections = (_extract_json(run_claude(nav_prompt, model=model)) or {}).get("selections") or []
    except (ValueError, json.JSONDecodeError):
        selections = []

    by_rel = {rel: (pdf, tree) for _, rel, pdf, tree in cand}
    if not selections:  # fallback: first couple of nodes of the top doc
        _, rel0, _, tree0 = cand[0]
        selections = [{"doc": rel0, "node_ids": [n["node_id"] for n in _flatten(tree0["nodes"])[:2]]}]

    out, budget = [], char_budget
    for sel in selections[:3]:
        doc = str(sel.get("doc", ""))
        match = next((v for r, v in [(r, (r, p, t)) for r, (p, t) in by_rel.items()]
                      if r == doc or r.endswith("/" + doc) or Path(r).name == Path(doc).name), None)
        if not match:
            continue
        rel, pdf, tree = match
        pages = extract_pages(pdf)
        nodemap = {n["node_id"]: n for n in _flatten(tree["nodes"])}
        for nid in (sel.get("node_ids") or [])[:6]:
            n = nodemap.get(str(nid))
            if not n:
                continue
            txt = "\n".join(pages[n["start_index"]:n["end_index"] + 1]).strip()
            if not txt:
                continue
            block = (f"#### files/{rel}  §{n['title']} "
                     f"(pp.{n['start_index'] + 1}-{n['end_index'] + 1})\n{txt}")
            out.append(block[:budget])
            budget -= len(block)
            if budget <= 0:
                break
        if budget <= 0:
            break

    if not out:
        return ""
    return ("## relevant PDF sections (selected by tree navigation; page-scoped extracts)\n"
            + "\n\n".join(out))
