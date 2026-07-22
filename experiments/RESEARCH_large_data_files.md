# Handling large structured data files (JSON/CSV/TSV) — research + recommendation

4 web agents + verification vs primary sources + an assessment that read our code
and the actual apr17 files. Problem: large data files (e.g. `psyche_asks_*.json`,
47–79 KB, 180–310 records) don't fit the answer digest, so the model hedges
"contents not shown" (apr17 ≈ 4.0).

## The established techniques (verified)
- **In-context smart excerpt:** schema/field extraction; data-profiling/"data card"
  (per-field stats, value-counts, min/max, date range); head+tail and **stratified**
  sampling (uniform sampling misses rare strata); **precomputed aggregates** (inject
  results, not rows). Compact formats (TOON: schema-once + value-rows, ~30–60% fewer
  tokens for uniform arrays).
- **Query-time / tool-use:** text-to-SQL (NL2SQL), **DuckDB querying JSON/CSV/TSV in
  place** (offline, MIT, ~13–33 MB wheel, Python ≥3.10), pandas/code agents.
- **The load-bearing principle (across all sources):** *never let the LLM compute
  arithmetic/aggregates in-context — compute deterministically, inject only results.*
  NL2SQL silent-wrong-results are the hardest failure mode (even strong models ~86%
  on Spider 1.0, ~10% on real warehouses; verification corrected earlier overclaims).

## Recommendation: deterministic stdlib smart-excerpt at answer time. NOT DuckDB (yet).
- **Compute, don't dump.** The two ways big-file QA fails — exact aggregates and
  set-difference/rare-value reasoning — are exactly apr17's needs. Both vanish if we
  compute counts/diffs in Python and inject the *results* + a stratified sample.
- **DuckDB is the right pattern, wrong tier for v1.** Our needed aggregates (counts,
  by-source, date range, strict-vs-non_pi diff) are *known and enumerable* — no
  open-ended query surface. DuckDB would add a platform-dependent dep AND a new
  hallucination path (the model authoring SQL). Hold it in reserve, gated behind
  `import duckdb` availability, for genuinely ad-hoc cross-file analytics.
- **No write-time index.** Computing at answer time from the live current-state file
  is strictly no-hindsight-safe (no sidecar to leak/stale) and measured at **0.0033 s**
  for all three files — 4 orders of magnitude under the 60 s budget.

## Concrete design (plugs into `digest_answer_state_relevant`)
For a `.json/.tsv/.csv` file whose body exceeds a threshold (~12 KB), render
`digest_structured(path)` instead of dropping it:
- schema (keys + inferred dtypes + uniformity flag),
- **exact** computed aggregates (value-counts for low-cardinality fields, row-count
  cross-check, min/max of date/numeric fields),
- **stratified** sample (first+last per stratum, ~8–10 rows — guarantees rare values
  like the n=1 `hermes` source appear),
- an honest NOTE: "summary of the FULL file; counts exact; rows sampled" — which
  directly defuses the false-"unavailable" hedge.

Side benefit: a ~1–2 KB summary replaces a 79 KB body, *freeing* budget for other files.

## The apr17 set-difference, deterministically (verified by the agent)
"Which asks did the strict filter drop?" = `non_pi` (203) − `strict` (180), keyed on
the **full record tuple** `(ts, q, source)` (ts alone is unsafe — `all.json` has dup
timestamps). **Answer: exactly 23 dropped** (22 `claude-code/syke`, 1 personal); strict
⊂ non_pi (0 added). A cross-file diff detector fires when the question mentions a set
relation and ≥2 ranked files share a schema; it lists all 23 (they fit).

## Deps / safety / risk
- **New deps: none** (`json`, `csv`, `collections.Counter`, `statistics` — all stdlib).
- No-hindsight: ✓ (answer-time, live files). 60 s: ✓ (0.0033 s). 
- Risks (mitigated): non-uniform/nested JSON → fall back to schema-skeleton + head/tail
  text (don't fabricate a table); wrong diff key → key on all shared fields + report the
  key; malformed file → try/except → current text-truncation behavior.

## v1 vs fuller
- **v1:** `digest_structured()` + wire into the inclusion loop + cross-file diff detector.
  Stdlib only. Kills the apr17 hedge; answers "23 dropped" exactly.
- **Fuller (only if needed):** numeric profiling; N-way diff lattice; a **DuckDB SELECT-only
  escape hatch** for open-ended ad-hoc queries, gated behind runtime availability and
  treated as lower-confidence than the deterministic aggregates.

**Bottom line:** apr17 is a *representation* problem, not a token-budget one. Render big
uniform data files as deterministic structured summaries (schema + exact aggregates +
stratified sample) computed in stdlib at answer time; answer set-differences with Python
`set` ops. Keep DuckDB in reserve for queries we can't enumerate.

Sources: DuckDB docs; LlamaIndex (PandasQueryEngine / JSONalyze-experimental) & LangChain SQL/pandas agents; AutoDDG (arXiv 2502.01050); TiInsight; Spider 1.0/2.0 (ICLR 2025); TOON spec.
