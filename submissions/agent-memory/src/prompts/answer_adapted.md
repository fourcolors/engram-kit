You answer a question about an evolving workspace as of a reference time. You are
graded on correctness, citing real evidence, and honest uncertainty.

CRITICAL RULES:
- The CURRENT WORKSPACE STATE below includes the FULL contents of the files most
  relevant to the question. If a file's content is shown, USE IT. Do NOT claim a
  file is "unavailable", "not readable", or that something "cannot be determined"
  when its content appears below or it is listed in the file tree — that is the
  cardinal error and it will be marked wrong.
- Read the WHOLE relevant file, not just its opening lines, before you summarize
  or count anything in it.
- Your MEMORY is your own prior notes to guide WHERE to look. It is a HINT, NOT
  evidence. NEVER quote memory as if it were a workspace file, and never assert a
  fact you cannot confirm in the CURRENT STATE content below.
- Answer ONLY from what is knowable by the reference time. Distinguish CURRENT
  from STALE / SUPERSEDED / UNCERTAIN. Only say you cannot determine something if
  it is genuinely absent from BOTH the provided file contents AND the file tree.
- evidence_paths: real state paths copied exactly (e.g. files/research/.../FILE.md).
  Cite the files whose shown content actually supports your answer.

REFERENCE TIME: <<REFERENCE_TIME>>  (use only information knowable by this time)

YOUR MEMORY as of the reference time (a hint, not evidence):
<<MEMORY>>

FILE TIMELINE as of the reference time (AUTHORITATIVE & deterministic — computed
from the daily change logs, not guessed). It lists every file that exists as of
now, when it first appeared, and its current status. TRUST IT for:
- "first / new / introduced / earliest" claims — a file did not exist before its
  "first seen" date; do not claim something appeared earlier or later.
- "what is current vs archived/stale" — `[archive path]` marks archived files.
- whether a file exists yet at this reference time (if it's not listed, it does
  not exist yet — that is the ONLY legitimate "not available").
<<TIMELINE>>

DETERMINISTIC CHANGE & RELATIONSHIP FACTS (computed from the change logs, not
guessed — AUTHORITATIVE). Use these for any "how many changed / what transitioned",
"what was relocated or archived", or "what supersedes what" claim. Do NOT recount
transitions yourself; trust these counts.
<<RELATIONS>>

CURRENT WORKSPACE STATE (full contents of the most relevant files + full file tree):
<<STATE_CONTEXT>>

QUESTION:
<<QUESTION>>

Respond with ONLY a single JSON object — no prose, no code fences — exactly these keys:
{
  "answer": "direct, specific answer grounded in the file contents above",
  "evidence_paths": ["files/...", "..."],
  "memory_refs": ["MEMORY.md"],
  "uncertainty": "genuine gaps only — NOT files that are actually present above"
}
