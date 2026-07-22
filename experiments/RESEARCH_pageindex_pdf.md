# PageIndex — how it works, and how to apply it to our PDFs

Research (4 web agents) + adversarial verification against the primary repo
(github.com/VectifyAI/PageIndex, MIT, ~33k stars as of 2026-06) + a design pass
that read our code and probed the real corpus. NOT yet implemented.

## How PageIndex works (verified)

PageIndex is **"vectorless," reasoning-based RAG**: instead of chunk + embed +
similarity-search, it turns each document into a **hierarchical JSON tree** (a
machine-navigable table of contents) and lets an LLM **navigate** that tree to the
right sections — like a human using a book's contents page.

**Two phases:**
1. **Index construction** — parse the PDF to per-page text; detect or derive a
   TOC; assign each section its physical page range; emit a recursive tree. Three
   modes converge on one node schema: (1) TOC *with* page numbers (offset-correct
   to physical pages), (2) TOC *without* page numbers (LLM fuzzy-matches titles to
   pages), (3) *no* TOC (LLM synthesizes an outline). Oversized sections recurse
   into sub-trees. A verification loop checks titles actually appear on their pages.
2. **Reasoning-based retrieval** — the LLM agent gets three tools: `get_document`
   (metadata), `get_document_structure` (the tree, **titles/summaries only, no body
   text**), `get_page_content(node_id)` (raw pages for a node). It reads the tree,
   reasons about which `node_id`s are relevant, then fetches only those pages.

**Node schema (verbatim):**
```json
{ "node_id": "0007", "title": "Experiments",
  "start_index": 6, "end_index": 9, "summary": "...", "nodes": [ ... ] }
```
`node_id` = zero-padded depth-first; `start_index`/`end_index` = 0-based physical
page indices (inclusive); `summary` = LLM-generated (optional); leaves omit `nodes`.

**Deps:** PyPDF2 (default) or PyMuPDF; litellm; an LLM (default gpt-4o) for TOC
detection / summaries / no-TOC generation. **No vector DB, ever** — that's the point.

### Myths the verification corrected (so we don't copy them)
- The "5-step iterative retrieval loop" is **blog prose, not code** — the OSS
  retrieval is a free-form LLM agent with 3 tools; behavior is emergent.
- PyMuPDF "font/layout detection" is **not in the repo** (it's an unmerged issue).
- LLM-call-count figures (~260/doc) come from an **unmerged community issue**, not
  an official measurement. MCTS retrieval is cloud-marketing, not in OSS.
- Best-fit evidence is **FinanceBench only** (claimed 98.7%); no other public eval.

## Our corpus reality (measured)
- 38 PDFs; target = **33 academic papers** under
  `…/papers/nondeterministic_verifier_202604/`, all appearing **2026-04-21**.
- **23/33 have embedded hierarchical bookmarks** (real Intro/Method/Results trees);
  10 have none. **All are true-text (not scanned).**
- `pdftotext`/`pdfinfo` (poppler) on PATH; `PyPDF2==3.0.1` importable; no pymupdf.
- **Extracting text for ALL 33 PDFs ≈ 3s.** Deterministic build fits one `update`.

> The corpus is **ideal for the deterministic half of PageIndex and hostile to the
> LLM half**: structure is mostly free (embedded outlines), but 38 docs landing on
> one date means per-doc LLM tree-gen/summaries would blow the 60s `update` budget.

## Design: adopt the data model + retrieval concept, drop the LLM-heavy construction

| PageIndex concept | Decision |
|---|---|
| Two-phase build/retrieve | **Adopt** (maps to update/answer) |
| Tree schema (`node_id/start_index/end_index/nodes`) | **Adopt verbatim** |
| LLM TOC detection + offset + verify | **Drop** — PyPDF2 outline gives real page numbers free (23/33) |
| LLM tree-gen when no TOC | **Replace** with deterministic heading regex (academic section vocab) |
| LLM node summaries | **Skip in v1** (titles are enough); optional rationed upgrade later |
| Recursive large-node split | **Replace** with fixed page-window leaves (docs ≤64pp) |
| Reasoning retrieval (tree → pick node_ids → fetch pages) | **Adopt, single call** (no iterative loop) |
| Vector embeddings | **Never** |
| Corpus-level file tree | **Reuse our existing `digest_answer_state_relevant` scorer** |
| Store section text in tree | **Don't** — re-extract pages on demand (~0.1s/doc) |
| gpt-4o / separate retrieve model | **Use local `claude -p sonnet`** |

**Build (`update`):** new `update_pdf_index(state_dir, memory_dir)` after
`update_timeline` — deterministic, **0 LLM calls**. Extract per-page text
(`pdftotext`, PyPDF2 fallback); build the tree (Mode A: walk PyPDF2 outline; Mode
B: heading regex; Mode C: page windows). Store **hash-keyed** (build each distinct
PDF once) in `MEMORY_DIR/pdf_index/{index.json, <sha1>.tree.json}`. Cost ≈ 3–5s
once on 2026-04-21, ~0s other days.

**Answer:** rank PDFs (existing scorer, gated by `timeline_asof` for no-hindsight)
→ render top-N trees as title-only outlines → **one** `run_claude` nav call returns
`node_id`s → extract only those pages (`pdftotext -f -l`) → append a budgeted
"relevant PDF sections" block to `STATE_CONTEXT`. Evidence paths carry the page
range (`…paper.pdf#p10`). Net: **+1 LLM call** vs today; fits 60s.

**No-hindsight:** reuse `timeline_asof(ref_date)` as the single gate — a tree built
on 2026-04-21 can't leak into an earlier-dated question. No new machinery.

**Deps to declare:** poppler `pdftotext` (optional, `shutil.which` gate + PyPDF2
fallback) and `PyPDF2`. No vector/embedding/LLM/GPU/network deps added.

**Risks:** 10 no-outline docs (→ regex/window fallback); extra nav-call latency
(→ env-gate `ENGRAM_PDF=on`, like ENGRAM_REPAIR, so it can't regress the baseline
until proven); poppler missing on grader (→ PyPDF2 fallback); invalid node_ids
(→ strict filter + deterministic fallback, `_coerce` philosophy).

## v1 (smallest useful change)
1. New `src/pdf_index.py`: `extract_pages`, `build_tree` (A/B/C), `update_pdf_index`
   (hash-keyed, idempotent), `select_and_extract` (rank → title-only trees → 1 nav
   call → page extract → budgeted block).
2. `observer.py`: one line — `update_pdf_index(...)` after `update_timeline(...)`.
3. `answerer.py` (adapted, `ENGRAM_PDF=on`): append `select_and_extract(...)` to
   `state_ctx`. No prompt/schema change.

Env-gated so the measured 4.60 baseline is untouched until v1 proves net-positive.

Sources: github.com/VectifyAI/PageIndex (repo + page_index.py), deepwiki.com/VectifyAI/PageIndex, official blog (alphasignal/marktechpost write-ups).
