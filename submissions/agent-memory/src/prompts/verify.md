You are a VERIFICATION pass on a DRAFT answer to a workspace question. Correct
ONLY genuine errors. If a claim is already correct, keep it verbatim — do not
soften or hedge correct statements. You have the full contents of the most
relevant files below; use them as the source of truth.

Fix these specific error types:

1. FALSE-UNAVAILABLE — Remove any claim that a file is "unavailable / not shown /
   not reproduced / not included / cannot be determined / inferred from memory"
   when that file's content appears below OR the file is listed in the file tree /
   manifest. Replace the hedge with the actual content. A file present in the tree
   is NOT absent.

2. ATTRIBUTION — Verify every "X is stated/defined in FILE", every version and
   date, and every "first / introduced / new / only" claim against the file
   contents. Fix misattributions. For a "first/new" claim, keep it ONLY if no
   earlier-dated file below already establishes that thing.

3. AGGREGATES — Recompute counts and state-transition totals from the data, not
   from impression. For "what changed" / transition questions, read changes.txt
   and report the breakdown by change kind (e.g. approximate→exact vs
   unavailable→exact vs deleted), not one sweeping total.

Keep evidence_paths pointing at real files present in this state. Keep
memory_refs as ["MEMORY.md"].

REFERENCE TIME: <<REFERENCE_TIME>>  (use only information knowable by this time)

WORKSPACE STATE (full relevant file contents + complete file tree + manifest):
<<STATE_CONTEXT>>

QUESTION:
<<QUESTION>>

DRAFT ANSWER (JSON):
<<DRAFT>>

Output ONLY the corrected JSON object — no prose, no code fences — with keys
answer, evidence_paths, memory_refs, uncertainty. If the draft is already
correct, output it unchanged.
