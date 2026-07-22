# Mastra memory — research + relationship verdict

4 web agents + verification against mastra.ai docs and github mastra-ai/mastra.
Question: how does Mastra handle relationships, and should we pull anything in?

## What Mastra's memory is (4 tiers)
1. **Message History** — raw thread log (last-N messages).
2. **Working Memory** — a persistent structured block per *resource* (user): markdown
   template (replace semantics) OR Zod/JSON schema (deep-merge: object merge, array
   replace, `null`=delete). A mutable "current state" profile, scoped resource/thread.
3. **Semantic Recall** — vector RAG over past messages (needs vector store + embedder;
   off by default).
4. **Observational Memory** (launched **Feb 2026**) — an **Observer + Reflector** pair:
   Observer extracts structured observations; Reflector compresses old raw history into
   a dense prioritized observation log. **No vector DB, prompt-cacheable. 94.87% on
   LongMemEval (gpt-5-mini), SOTA at launch.**

Scoping = two flat string keys (Resource = user, Thread = session). 12 storage + 17
vector backends. TypeScript/Node only.

## Relationships: they deliberately DON'T model them
Verified bottom line: **Mastra does not model entity relationships at all.** Every tier
is flat — no entity extraction, no typed edges, no graph traversal, no knowledge graph.
Their blog says it outright: *"Down with knowledge graphs. Roon was right. Text is the
universal interface."* `Resource`/`Thread` decide *where* data lives, not *how things
relate*. GraphRAG (`@mastra/rag`) is chunk-to-chunk cosine similarity (not entities),
ephemeral (issue #3926 open). `@mastra/mem0` wires only Mem0's vector layer, not its
graph. For real entity-relationship graphs you'd bolt on external Graphiti/Zep — no
official integration.

## Two takeaways for us

**1. Strong validation of our design.** Mastra independently built the *same*
observational-memory pattern we use — Observer + Reflector, dated/compressed
observations, no vectors, prompt-cacheable — and hit SOTA on LongMemEval. We're on the
right architecture. (We also have two things their memory lacks: a **deterministic,
no-LLM temporal index** (`timeline.py`) and **no-hindsight date filtering**.)

**2. Nothing to pull in for relationships — they have none to give.** Mastra is the
wrong place to look for the relationship capability; they reject it on principle.

## Verdict: SKIP Mastra for relationships; build our own minimal edge layer
Borrow at most the *concept* of a merge-semantics structured store — no code (TS-only,
@mastra/core peer dep, vector stack; nothing portable to stdlib Python).

**Build `edges.json`, a structured SEMANTIC sibling to `timeline.py`:**
- Store `{date, kind, src, dst, note}`, kind ∈ `supersedes | derived-from | references`.
- **Deterministic first:** `changes.txt` rename/replace rows and version-numbered
  filenames (V1→V2→unnumbered-canonical) yield `supersedes` edges with 0 LLM — likely
  fixes **apr20** ("what got superseded").
- **LLM-assisted:** promote the supersession the observer already writes in prose into
  0–3 structured `src kind dst` triples/day (parsed from a fenced block).
- **Query:** `edges_asof(ref_date)` → date-filtered edge view injected next to
  `<<TIMELINE>>` in `answer_adapted.md`. Gives apr18 ("first introduced") an
  authoritative lineage chain instead of re-derivation.
- **No-hindsight free:** edges carry a date, filtered `<= ref_date`.

~1 module + ~15 lines in observer/answerer + a prompt section. Deterministic-first,
offline, single-store, date-filtered — targets the apr18/apr20 laggards and the on-rubric
"distinguish current/stale/superseded".

## Nuance worth holding
Mastra bets "text beats graphs." Our data partly agrees (flat prose memory got us to
4.60) — but the *specific* questions where flat prose wobbles are exactly the
relationship/attribution ones (apr18/apr20). The pragmatic middle: not a full knowledge
graph, just a **minimal deterministic edge layer** (like the timeline did for temporal).

Sources: mastra.ai/docs/memory, mastra.ai/blog/observational-memory + /research/observational-memory, github.com/mastra-ai/mastra.
