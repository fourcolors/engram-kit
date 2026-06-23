# v5 — deterministic relationship layer + 30-day safety (honest result)

v5 = v4 (memory timeline) + a deterministic relationship layer: at answer time a
computed change/relationship summary (transition counts, relocations, archived-by-path,
version supersession) from `changes.txt`+`manifest.tsv`; 🔗 plain-text relationship
facts written into `MEMORY.md` (no JSON edge store). Plus a hardened, **guarded** reflector.

## What is verified TRUE (deterministic — not subject to judge noise)
- **apr20 transition counts now correct:** `23 modified approximate→exact, 57 added
  unavailable→exact, 22 deleted` — injected verbatim from `changes.txt`; a judge
  independently recounted and confirmed. Fixes the old "all 80 approximate→exact" miss.
- **Relocations / archived / supersession** detected deterministically (e.g. the
  Apr-20 `claude-thesis-notes-20260521/archive/* → archive/*` restructure ×22; the
  `NE_1_3_REAL_ASK_EVAL_SET.yaml supersedes …V2.yaml` lineage).
- **30-day reflection safety — PROVEN.** A deterministic guard (`reflection_is_safe`)
  rejects any compression that drops a `Date:` header or a 🔗 fact. Real-reflector
  test on a synthetic 30-day memory: 154→65 lines, **30/30 dates + 2/2 🔗 preserved**,
  and an as-of-day-10 read correctly **excluded** day-28 facts (no-hindsight held).

## What the scoreboard says (and why it's inconclusive)

| | v4 | v5 |
|---|---|---|
| Overall | 4.60 | 4.30 |
| Leaks | 0 | 0 |

Full 10-Q re-judge: v5 = 4.30, *down* from v4's 4.60 (apr18 3→2, apr21_probe 5→4,
apr10 5→4). **But a controlled 2-question head-to-head on the SAME v5 answers scored
apr18=5 and apr20=5 (v5 wins both).** The same apr18 answer scored **5 and 2** across
two judgings.

**Conclusion: we are at the measurement noise floor.** Answer generation *and* judging
are nondeterministic; individual borderline questions swing ±3. A single run cannot
detect a ~0.2 feature effect. The 4.60→4.30 move is **not** evidence the relationship
layer regressed — and the head-to-head is **not** evidence it gained. Neither single
run is decisive.

## What actually still blocks 5.0 (unchanged, answer-side)
The sub-5 questions (apr18, apr21_probe, apr17) fail on the **false-"unavailable" /
content-availability** pattern — the answer hedges that a present file *body* isn't
shown, or presents inference as documentation. This is independent of relationships;
the relationship layer neither caused nor fixes it.

## Status / recommendation
- Relationship layer: built, gated `ENGRAM_REL` (default on), correct + on-rubric +
  cheap. The 30-day reflection guard is **always on** (pure safety).
- To actually measure the layer's effect, **average N=3–5 runs** of v4 vs v5 (the only
  way past the noise). Otherwise judge it on its deterministic merits (correct counts,
  30-day safety) rather than a noisy scoreboard.
- The real next score lever is the false-"unavailable" pattern, not relationships.
