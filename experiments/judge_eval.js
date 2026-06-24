// Averaging judge for noise-controlled eval. Judges every (config × repeat × question)
// answer once on quality (0-5), returns all scores; synthesis aggregates mean±range
// per config so we can see signal past the answer/judge noise.
// Invoke via Workflow({scriptPath: ".../experiments/judge_eval.js"}).
export const meta = {
  name: 'engram-eval-judge',
  description: 'Judge N-run eval answers across configs and aggregate mean±range per config',
  phases: [ { title: 'Judge' }, { title: 'Aggregate' } ],
}
const KIT = '/Users/fourcolors/Projects/3_open_source/engram-kit'
const EVAL = KIT + '/experiments/out/eval'
const CONFIGS = ['v6_opus_disc', 'v7_struct']     // edit per phase
const REPEATS = 3
const QS = [
  { id: 'ftw_v1_apr08_lab_object_boundaries', date: '2026-04-08', question: 'Cold-starting from the earliest lab files: what is this lab comparing, what is the object under study, and what is premature to conclude from the Apr 8 state?' },
  { id: 'ftw_v1_apr10_legacy_archive_boundary', date: '2026-04-10', question: 'Are BENCHMARK_ITEMS.yaml, BENCHMARK_RUNSETS.yaml, PROBE_SEEDS_V1.md under archive/benchmark-legacy current task source or historical machinery? Explain the boundary.' },
  { id: 'ftw_v1_apr13_real_ask_v2_lineage', date: '2026-04-13', question: 'Inside the archived real-ask-history folder, which artifact is canonical by Apr 13 and what sampling stance does it preserve?' },
  { id: 'ftw_v1_apr14_s07_denominator_fit', date: '2026-04-14', question: 'How is the S07 slice different from LoCoMo and LifeBench per the local comparison note, and what does that imply for evaluating memory?' },
  { id: 'ftw_v1_apr17_judge_salvage_and_real_asks', date: '2026-04-17', question: 'From the Apr 17 judge salvage note and the real-ask JSON files, what can be salvaged from the judge runs, and what does the ask corpus change about what memory should track?' },
  { id: 'ftw_v1_apr18_demand_tags_not_taxonomy', date: '2026-04-18', question: 'What did ask_demands_ne13_20260418.tsv add by Apr 18, and why should its labels not become the final benchmark taxonomy?' },
  { id: 'ftw_v1_apr19_environment_judge_primitives', date: '2026-04-19', question: 'From the Apr 19 environment, ask-surface, and judge-primitives notes, what is the clearest environment definition, and which judge obligations are universal vs conditional?' },
  { id: 'ftw_v1_apr20_calibration_boundary', date: '2026-04-20', question: 'On Apr 20, what actually changed: evidence confidence, archive/source roles, and judge-calibration stance? Do not turn it into a new architecture result.' },
  { id: 'ftw_v1_apr21_measurement_instrument_scope', date: '2026-04-21', question: 'Is the new judge-calibrated-baseline-experiment folder an architecture leaderboard? What unit and gates define the experiment before any ranking?' },
  { id: 'ftw_v1_apr21_probe_coverage_gaps', date: '2026-04-21', question: 'In ASK_SAMPLING_20260421.md, what is missing or underrepresented in the historical 19-probe judge slice, and why does it matter for rubric design?' },
]
const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['key', 'overall', 'false_unavailable', 'note'],
  properties: {
    key: { type: 'string' },
    overall: { type: 'integer', minimum: 0, maximum: 5 },
    false_unavailable: { type: 'boolean', description: 'did it falsely claim a present file/its content is unavailable?' },
    note: { type: 'string' },
  },
}

const items = []
for (const cfg of CONFIGS) for (let k = 1; k <= REPEATS; k++) for (const q of QS)
  items.push({ key: `${cfg}/r${k}/${q.id}`, cfg, k, q })

phase('Judge')
const verdicts = await pipeline(items, (it) => agent(
  `Score one ENGRAM answer 0-5 (correctness, grounding, honest uncertainty), verifying against the reference state. Be consistent and calibrated.
Use Bash (cat/grep, pdftotext) + Read on ABSOLUTE paths:
- Answer: ${EVAL}/${it.cfg}/r${it.k}/${it.q.id}.json
- Reference state: ${KIT}/sample_states/${it.q.date}/files/ , changes.txt , manifest.tsv
QUESTION (ref ${it.q.date}): ${it.q.question}
Verify cited evidence_paths exist; for any count/transition claim, recount from changes.txt. Set false_unavailable=true if the answer claims a present file or its content is "unavailable / not shown / cannot be determined" when it is actually in-state. overall 0-5. Return verdict with key="${it.key}".`,
  { schema: SCHEMA, phase: 'Judge', label: it.key }
))
const clean = verdicts.filter(Boolean)

phase('Aggregate')
const synthesis = await agent(
  `Aggregate a noise-controlled ENGRAM eval. Each config was run ${REPEATS}× over 10 questions; below are per-answer scores (key = config/rRUN/questionId, overall 0-5, false_unavailable flag).

SCORES (JSON): ${JSON.stringify(clean, null, 1)}

Compute and report:
1. Per config (v4 = relationships OFF, v5 = relationships ON): mean overall across all 30 answers, plus min/max run-mean (the noise band), and the per-question mean (averaged over the 3 runs).
2. Is v5 vs v4 a real difference or within the noise band? State it plainly.
3. false_unavailable rate per config, and which questions trigger it most (this is the known real blocker).
4. The per-question means that are clearly below 5 across BOTH configs (the genuine weak spots to fix next).
Be precise with the arithmetic. For the engineer.`,
  { phase: 'Aggregate', label: 'aggregate' }
)
return { scores: clean, synthesis }
