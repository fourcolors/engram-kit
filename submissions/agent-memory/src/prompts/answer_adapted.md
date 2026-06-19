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
