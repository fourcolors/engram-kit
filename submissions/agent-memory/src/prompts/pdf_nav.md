You are navigating document outlines to find the sections that answer a question.
You are given the table-of-contents TREE of each candidate PDF — titles and page
ranges only, no body text. Pick the few sections whose pages most likely contain
the answer (reason from the section titles, like using a book's contents page).

QUESTION:
<<QUESTION>>

CANDIDATE DOCUMENT TREES:
<<TREES>>

Return ONLY a JSON object — no prose, no code fences:
{"selections":[{"doc":"<the exact files/... path from a ### header>","node_ids":["0007","0008"]}]}

Pick at most 2 documents and at most 3 node_ids each — only the most relevant
sections. If nothing looks relevant, return {"selections":[]}.
