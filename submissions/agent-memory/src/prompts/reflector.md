You are running the REFLECTOR PASS on an agent's MEMORY.md, which has grown
close to the size cap. Compress it to <= <<TARGET>> lines while preserving the
highest-value memories.

KEEP:
- All 🔴 hard constraints, gotchas, and root causes.
- 🟡 facts that name file paths, statuses (exact/approximate), or what a file
  decides/contains — these are expensive to re-derive.
- Anything recording a supersession or archival (X replaced/archived Y), with
  its date.
- Recent ✅ confirmations (the last several days).

MERGE / DROP:
- Merge repeated observations of the same fact across dates into the most recent
  statement.
- Drop 🟢 noise and stale bookkeeping. Newer statements win over older.

Preserve the `Date:` headers and date grouping. Output ONLY the rewritten
MEMORY.md content — no prose, no code fences.

CURRENT MEMORY.md:
<<MEMORY>>
