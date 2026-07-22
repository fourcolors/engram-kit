You are running the REFLECTOR PASS on an agent's MEMORY.md, which has grown
close to the size cap. Compress it to <= <<TARGET>> lines while preserving the
highest-value memories.

HARD RULES (a reflection that violates these is rejected automatically):
- PRESERVE EVERY `Date:` header, exactly as written. Never merge, drop, or
  relabel a date. Answers are date-filtered by these headers, so losing one
  silently breaks no-hindsight reasoning.
- PRESERVE EVERY `🔗` line verbatim. These are deterministic relationship facts
  (relocations / archival / supersession) and must never be dropped or reworded.
- NEVER move an observation to a different date, and NEVER edit a past-dated
  bullet to reflect something learned on a LATER date. Each bullet must stay true
  as of its own date (no hindsight backdating).

KEEP (within each date):
- All 🔴 hard constraints, gotchas, and root causes.
- 🟡 facts that name file paths, statuses (exact/approximate), or what a file
  decides/contains.
- Recent ✅ confirmations.

MERGE / DROP (within a date only):
- Drop 🟢 noise and redundant 🟡 bullets. Merge duplicate observations of the same
  fact, keeping the most specific wording.

Output ONLY the rewritten MEMORY.md content — no prose, no code fences — with the
same `Date:` structure.

CURRENT MEMORY.md:
<<MEMORY>>
