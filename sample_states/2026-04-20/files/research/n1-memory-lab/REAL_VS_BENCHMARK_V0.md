# REAL_VS_BENCHMARK_V0

This memo compares the first real NE-1 slice families against the assumptions built into major memory benchmarks. The point is not to say the benchmarks are useless. The point is to identify where real operator traces stop being the same object.

Sources:
- `research/omocon-talk/benchmark-data-notes.md`
- `research/memory-eval-landscape-2026.md`
- `research/n1-memory-lab/CORPUS_BASELINE.md`
- `research/n1-memory-lab/SLICE_ATLAS_V0.md`
- `_internal/syke-replay-lab/datasets/ne1.db`

## Benchmark assumptions worth naming directly

Across LoCoMo, LongMemEval, BEAM, PersonaMem, and LifeBench, the recurring assumptions are:
- the memory object is bounded enough to define clean tasks against
- the primary unit is still close to message/question style interaction
- updates and temporal changes are explicitly testable inside a designed frame
- the system is mostly judged on retrieval, ordering, contradiction handling, preference recovery, or summarization
- the evaluation surface is not a day-to-day operator continuity surface

These are good assumptions for benchmark memory.
They are not obviously the right assumptions for NE-1 slices.

## Slice-family comparison

| Slice family | Real property | Which benchmark assumption it strains |
|---|---|---|
| `S01` benchmark/eval work | dense tool-heavy benchmark-building work, not just benchmark-answering | the model is part of benchmark creation and interpretation, not only benchmark completion |
| `S02` multi-agent swarm day | many parallel sessions and sub-lanes on one day | one-thread / one-user / one-assistant framing |
| `S03` forgotten-plan resumption | the problem is not missing fact recall but recovering prior analysis and current plan | memory = answer retrieval from visible history |
| `S04` memex evolution / doc hygiene | practical value comes from canonicalization and reducing narrative clutter | benchmark success = right answer only |
| `S05` architecture transition surface | the memory regime itself changes when Hermes/manual/provider signals enter | stable architecture / stable source assumptions |
| `S07` cross-harness recall under pressure | multiple harnesses try to reconstruct yesterday+today across one user graph | bounded conversation object with one surface of truth |
| `S08` post-burst stabilization | memory must decide what stays live after an extreme activity spike | static or uniformly-scored context objects |

## The sharpest contrasts so far

### 1. Resumption is different from recall

`S03` is not primarily a factual lookup problem.
The hard part is that the user says, in effect:
- we already discussed this
- we already analyzed it with data
- why are you acting as if this is new?

That stresses:
- prior reasoning recovery
- current-plan recovery
- justification recovery

Benchmark nearest neighbors:
- LongMemEval multi-session and knowledge-update

But the NE-1 slice is still different because the failure is practical continuity loss, not just wrong answer selection.

### 2. Cross-harness recall is different from long-context QA

`S07` asks for reconstruction across yesterday/today and across multiple harnesses.
The operator pressure is:
- merge threads
- reconcile active work
- recover continuity through a tool braid

Benchmark nearest neighbors:
- LoCoMo multi-hop
- LongMemEval multi-session
- LifeBench multi-source

But the NE-1 slice is still different because the sources are actual harnesses with overlapping and partially incompatible perspectives, not a designed benchmark package.

### 3. Practical value is not the same as answer correctness

`S04` is a strong reminder that some memory value is:
- clearer routes
- less repeated searching
- canonical docs
- easier future resumption

Benchmark nearest neighbors:
- BEAM summarization

But benchmark summarization still under-specifies the operational value of a memory surface that reduces clutter and stabilizes the route map for future sessions.

### 4. Architecture shifts are themselves part of the object

`S05` shows new source families entering late (`hermes`, `manual`) and changing what memory has to reconcile.

This is not just "new evidence."
It is a change in the memory ecology.

Most benchmark designs do not test what happens when the memory regime itself changes midstream.

## The provisional conclusion

The current slice families suggest that NE-1 pressure is hardest exactly where benchmark assumptions are thinnest:
- cross-harness continuity
- resumption after practical gaps
- route-map and canonicalization value
- architecture changes inside the trace
- deciding what remains live after bursts and reversals

That does not invalidate benchmark work.
It does show that the object under study in NE-1 slices is not reducible to benchmark-style retrieval, ordering, or preference recovery.

## Next comparison step

The next real step should be one dedicated family-vs-benchmark pass:
1. take `S03` and map it against LongMemEval categories exactly
2. take `S07` and map it against LoCoMo / LifeBench assumptions exactly
3. note where the benchmark task frame still fails to express the real continuity burden
