# N=1 Memory Research Lab

Personal memory is an n=1 problem: one changing person, across time and tools, whose work shifts form because the user, the tools, and the models all keep changing.

Existing benchmarks test retrieval over static corpora. This lab tests whether a memory system preserves continuity for a real user.

## The eval set

There are now two important layers here:

- the older mixed benchmark probe set
- the newer canonical `NE-1.3` real-ask set

The canonical `NE-1.3` set is `50` real asks only, sampled to preserve the month's lived temporal shape instead of flattening it into benchmark coverage buckets.

## The datasets

Three frozen monthly windows from one real user's multi-harness activity:

| Dataset | Window | Sources |
|---------|--------|---------|
| NE-1.1 | Jan 9 - Feb 8, 2026 | codex, opencode, hermes |
| NE-1.2 | Feb 9 - Mar 8, 2026 | claude-code, codex, opencode, hermes |
| NE-1.3 | Mar 9 - Apr 8, 2026 | claude-code, codex, opencode, hermes |

NE-1.1 has no Claude Code data (rotated before bundle creation). NE-1.3 is the densest window.

## The judge

An agentic judge over a bounded evidence pack. It verifies the answer against the contained raw slice and related evidence surfaces.

Judge-scored axes: factual grounding and continuity. Efficiency is reported from runner telemetry, not treated as a free-form LLM score.

## The scoring

**Success Rate / Pass@1** = `pass / total_judged`.

Reported as a fraction: "18/43 successes (42%)".

System comparison uses McNemar's exact test on paired binary outcomes.

Efficiency is reported separately from telemetry: cost per success, tool calls per success, and zero-search success rate.

The failure gallery is mandatory. A benchmark that only shows wins is marketing.

## Files in this lab

### Core eval
- `JUDGE_METHOD_V1.md` — judge design, prompt, and output schema
- `SCORING_METHOD_V3.md` — scoring method and reporting requirements
- `NE_1_3_REAL_ASK_EVAL_SET.yaml` — canonical `NE-1.3` real-ask eval set
- `NE_1_3_REAL_ASK_EVAL_SET.md` — sampling shape, judge contract, and measurement surfaces

Historical probe-seed and mixed benchmark files now live under:

- `research/n1-memory-lab/archive/benchmark-legacy/`

### Datasets and evidence
- `NE_DATASET_ARCHITECTURE_V1.md` — dataset design
- `NE_1_1_EVAL_CANDIDATES_V1.md` — observer evidence for NE-1.1
- `NE_1_2_EVAL_CANDIDATES_V1.md` — observer evidence for NE-1.2
- `NE_1_3_EVAL_CANDIDATES_V1.md` — observer evidence for NE-1.3
- `NE_TIMELINE_V1.md` — timeline of the three datasets
- `CORPUS_BASELINE.md` — corpus statistics

### Research positioning
- `S03_VS_LONGMEMEVAL.md` — comparison with LongMemEval
- `S07_VS_LOCOMO_LIFEBENCH.md` — comparison with LoCoMo and LifeBench
- `REAL_VS_BENCHMARK_V0.md` — how real traces differ from existing benchmarks
- `PRACTICAL_VALUE.md` — what practical value means for memory
- `ARCHITECTURE_CASES_V0.md` — architecture case studies
- `ARCHITECTURE_COMPARISON.md` — architecture comparison framework
- `ARCHITECTURE_EXPERIMENT_MATRIX_V1.md` — controlled experiment design

### Governance
- `LAB_CHARTER.md` — guardrails
- `CRITIQUE_CONSTRAINTS_V1.md` — what not to overclaim
- `NOTE_TO_CLAUDE_REPLAY_BENCHMARK.md` — replay alignment constraints

## Limitations

This is one user's traces. Results do not generalize to other users. The benchmark is n=1 by design — that is the thesis, not a bug.
