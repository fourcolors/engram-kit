# Calibration Stack — 2026-04-20

Status: current judge-calibration state from the surviving packet only. Mixed-model dead runs and invalid GPT-full reruns are out.

Companion artifacts:
- [`scratch/clean_packet_calibration_20260420.py`](./scratch/clean_packet_calibration_20260420.py) — reproducible run-inventory + contingency + reliability summary
- [`scratch/schematic_adherence_20260420.py`](./scratch/schematic_adherence_20260420.py) — verdict-on-subaxis regression refresh
- [`JUDGE_DESIGN_LITERATURE_MAP_20260420.md`](./JUDGE_DESIGN_LITERATURE_MAP_20260420.md) — what parts of the literature transfer
- [`JUDGE_MINING_SYNTHESIS_20260420.md`](./JUDGE_MINING_SYNTHESIS_20260420.md) — wider mining pass and the earlier audit trail

## 1. Trusted packet

These are the only runs currently licensed for calibration claims.

| run | ask model | judge model | purpose |
|---|---|---|---|
| `ne13-real-15d-gpt54-final-20260420T071500Z` | `gpt-5.4` | `gpt-5.4` | canonical GPT baseline |
| `ne13-real-15d-opus46-final-20260420T071500Z` | `claude-opus-4-6` | `claude-opus-4-6` | canonical Opus baseline |
| `ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z` | reused GPT answers | `claude-opus-4-6` | cross-judge on GPT answers |
| `ne13-real-15d-opusask-gpt54judge-20260420T144210Z` | reused Opus answers | `gpt-5.4-mini` | cross-judge on Opus answers |
| `ne13-real-15d-opusask-opusjudge-intrarater-20260420T200314Z` | reused Opus answers | `claude-opus-4-6` | Opus intra-rater rep1 |
| `ne13-real-15d-opus46-intrarater-rep2-20260420T222645Z` | reused Opus answers | `claude-opus-4-6` | Opus intra-rater rep2 |
| `ne13-real-15d-opus46-intrarater-rep3-20260420T222645Z` | reused Opus answers | `claude-opus-4-6` | Opus intra-rater rep3 |

Important caveat:
- the surviving GPT-side cross run uses `gpt-5.4-mini`, not full `gpt-5.4`
- there is no clean surviving full-`gpt-5.4` intra-rater packet
- historical artifacts still say `production`; interpret that as the current `syke` condition

## 2. What the packet licenses now

### 2.1 Judge identity changes the ordinal verdict a lot

Same answers, different judges:

| comparison | valid overlap | exact | linear weighted κ | mean delta | binary useful-vs-fail exact |
|---|---:|---:|---:|---:|---:|
| GPT answers: `gpt-5.4` judge → Opus judge | 54 | 0.4815 | 0.2391 | +0.5000 | 0.8704 |
| Opus answers: Opus judge → `gpt-5.4-mini` judge | 57 | 0.5088 | 0.3398 | -0.4912 | 0.9123 |

Reading:
- the direction is robust: Opus is materially more lenient than GPT-family judging on the same answer sets
- the big movement is mostly inside `pass / partial / fail`, not inside `useful / fail`
- this is enough to say judge identity is a real confound
- this is **not** enough to claim a clean full `gpt-5.4` vs Opus judge-effect magnitude, because one arm is `gpt-5.4-mini`

### 2.2 Opus judge is stable enough to study

Baseline Opus run vs three same-judge repeats on the exact same Opus answers:

| comparison | valid overlap | exact | linear weighted κ | mean delta | std delta | binary useful-vs-fail exact |
|---|---:|---:|---:|---:|---:|---:|
| baseline vs rep1 | 55 | 0.8000 | 0.7416 | -0.0545 | 0.4439 | 0.9636 |
| baseline vs rep2 | 49 | 0.7551 | 0.6632 | 0.0000 | 0.4949 | 0.9388 |
| baseline vs rep3 | 53 | 0.8113 | 0.7507 | -0.0377 | 0.4327 | 0.9623 |

Across all four Opus judge calls together:

- overlap in all four reps: `45 / 57`
- ordinal `σ_ε` on the 0-2 verdict scale: `0.1873`
- all-four exact agreement: `57.8%`
- all-four binary useful-vs-fail agreement: `93.3%`

Reading:
- Opus is not deterministic at the 3-class boundary
- Opus is much more stable on the coarse catastrophe-vs-non-catastrophe cut than on the ordinal band split
- this is enough to keep using Opus for judge-design work

### 2.3 The current rubric is coherent but over-specified

From the refreshed verdict-on-subaxis regressions in [`scratch/schematic_adherence_20260420.py`](./scratch/schematic_adherence_20260420.py):

- per-config verdict reconstruction `R²` is `0.719` to `0.918`
- a single sub-axis alone explains `0.535` to `0.815` depending on config

Reading:
- the rubric is not random noise; judges are mostly doing what the rubric says
- the problem is not incoherence, it is collapse
- twelve sub-axes are too many for the signal actually being used

This is the main reason to simplify the judge contract rather than add more calibration machinery on top of the current one.

### 2.4 What this does and does not imply about scoring

The packet supports three different layers, and they should not be conflated:

1. **Primitive layer**: the real measurement object.
   - This is where we ask which memory functions worked:
     - bounded support
     - time-local correctness
     - operative-state adequacy
     - wrong-restart risk
     - plus conditional primitives when the ask genuinely demands them

2. **Aggregate verdict layer**: a compressed summary derived from the primitive vector.
   - This should be non-compensatory.
   - Hard failures on certain primitives can veto.
   - `pass / partial / fail` belongs here, if we keep it.

3. **Reliability-audit layer**: a coarse stability readout.
   - `catastrophic failure` vs `not catastrophic failure`
   - useful only because the packet shows this cut is more judge-stable than the 3-class split
   - not the benchmark object

So the finding is **not** "move the benchmark to binary."
The actual finding is:

- keep axes / primitives primary
- derive aggregate judgment from those axes
- use a coarse binary collapse only as a calibration diagnostic while the aggregate bands are still unstable

## 3. What the packet does not license

- clean full-`gpt-5.4` intra-rater reliability
- agent stochasticity `β`
- full CyclicJudge-style variance decomposition
- architecture-separation claims beyond coarse directional patterns
- any claim that the current 3-class scale is psychometrically mature

## 4. Calibration decisions right now

These are the evidence-grounded choices, not final theory.

1. Keep the environment fixed. The calibration target is the judge contract, not the replay environment.
2. Make the primitive vector the primary scored object.
3. Use aggregate verdicts only as derived summaries over that vector.
4. Treat the coarse binary collapse only as a reliability audit, not as the benchmark target.
5. Shrink the rubric to a few load-bearing primitives about the operative state at `t`, newest-evidence integration, and wrong-restart risk.
6. Force claim discipline in the judge prompt: `verified`, `inferred`, `speculative`.
7. Do judge-only rescoring on the current packet before any new architecture experiments.

## 5. Immediate next move

The next calibration iteration should do one thing well:

- rewrite the judge contract around the small primitive set from the earlier notes
- score universal primitives on every probe and conditional primitives only when the ask fires them
- derive the overall verdict from that primitive vector with hard vetoes where needed
- report the coarse binary collapse only as a stability readout on top of the aggregate verdict
- rescore the same surviving packet before collecting new model-condition runs

That is the shortest path from today's data to a cleaner judge.
