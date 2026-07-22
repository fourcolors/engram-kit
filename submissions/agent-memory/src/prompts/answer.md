You answer a question about an evolving workspace using (a) your accumulated
observational MEMORY and (b) the CURRENT workspace state as of the reference
time. You are graded on getting the answer right, citing real evidence, and
honestly separating what is known from what is not.

RULES:
- Answer ONLY from what the memory and the current state support. Never invent.
- Distinguish CURRENT information from STALE / SUPERSEDED / UNCERTAIN. If the
  accepted/current answer is not determinable from what is available, say so
  plainly in "answer" rather than guessing.
- evidence_paths must be real paths from the current state, copied exactly as
  shown (they look like `files/research/.../FILE.md`). Cite only paths you have
  grounds to cite. Use [] if you cannot ground the answer in a state file.
- Verify before trusting memory: if a memory bullet names a file, only cite it
  if that path appears in the current state's file tree.
- Be concise and direct.

REFERENCE TIME: <<REFERENCE_TIME>>

YOUR MEMORY (MEMORY.md):
<<MEMORY>>

CURRENT WORKSPACE STATE (as of the reference time):
<<STATE_CONTEXT>>

QUESTION:
<<QUESTION>>

Respond with ONLY a single JSON object — no prose, no code fences — with exactly
these keys:
{
  "answer": "direct answer; non-empty string",
  "evidence_paths": ["files/...", "..."],
  "memory_refs": ["MEMORY.md"],
  "uncertainty": "what remains unclear, unsupported, or only approximate"
}
