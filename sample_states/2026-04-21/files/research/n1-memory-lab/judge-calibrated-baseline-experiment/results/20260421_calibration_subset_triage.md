# 2026-04-21 Calibration Subset Triage

Status: agent-assisted first pass. This is not human ground truth.

Rule preserved: `zero` is a valid bounded-packet condition. `pass`, `partial`,
and `fail` are noisy observations.

Source packet:

- [20260421_calibration_subset_packets.json](./20260421_calibration_subset_packets.json)
- [20260421_calibration_subset_packets.md](./20260421_calibration_subset_packets.md)

## R03-R09

| Probe/condition | Main judge disagreement pattern | Likely cause | Priority | Claim-audit focus |
|---|---|---|---|---|
| R03 / production | `pass` vs `partial` on whether latest live state is current enough | answer quality | medium | Was onboarding/provider strategy actually latest, or was synthesis debugging still live? |
| R03 / pure | `pass` / `partial` / `fail`; commit-trail reconstruction vs latest-live-state split | rubric ambiguity | high | Did the answer need live cutoff state, not just commit evidence? |
| R03 / zero | Mostly `partial`, one `fail`; shipped vs still-open `finalize_memex` status | packet insufficiency | medium | Was Bug 1 truly closed in the bounded packet, or only partially validated? |
| R05 / production | `pass` / `partial` / `fail`; subjective prioritization under stale-memex risk | rubric ambiguity | medium | Were Observe-Map-Ask and session-model architecture really the top same-day threads? |
| R05 / pure | Unanimous `partial`; mostly staleness on bug-status calls | answer quality | low | Which bug statuses were already fixed vs still open at cutoff? |
| R05 / zero | Mostly `pass`, some `partial`; ordering/currentness threshold differs | rubric ambiguity | low | Was the March 13 priority stack reconstructed in the right order? |
| R07 / production | Mostly `partial`, one `pass`; precision threshold on source-authority ordering | rubric ambiguity | medium | Did the live thread shift into concrete Observe implementation on Mar 14? |
| R07 / pure | Same `partial`/`pass` split; useful but overprecise | rubric ambiguity | medium-low | Was the March 14 Observe implementation shift the terminal active thread? |
| R07 / zero | `fail` / `partial`; reconstruction possible vs impossible | answer quality | high | Can Mar 13-14 live threads be reconstructed from session traces + git anchors? |
| R08 / production | `fail` / `partial`; live Observe/git-state context missed entirely | answer quality | high | Did the live state include staged/unstaged Observe work and stash-pop forensics? |
| R08 / pure | `partial` / `fail`; self-bounded but wrong world-model | answer quality | high | Was the actual context Observe Phase 2 development with canonical-schema/tool work? |
| R08 / zero | Mostly `fail`; empty/meta-state claim vs live repo evidence | answer quality | high | What did the frozen repo and transcript corpus show about the real live work state? |
| R09 / production | `fail` / `partial`; fabricated UUID/thread links vs useful thematic map | answer quality | high | Do the claimed UUIDs and thread links exist, or were they invented? |
| R09 / pure | `pass` / `partial`; useful map, but freshness/omission threshold differs | rubric ambiguity | medium | What late-day corrections or extra threads were omitted from the map? |
| R09 / zero | `fail` / `partial` / `fail`; storage-health meta-report instead of thread map | answer quality | high | Did the answer recover the actual CLOSED/NEXT/ACTIVE/UNDERCURRENT thread map? |

## R13-R19

| Probe/condition | Main judge disagreement pattern | Likely cause | Priority | Claim-audit focus |
|---|---|---|---|---|
| R13 / production | Mostly agree it is good; one judge trims GPT answer for overclaiming and unsupported memory-update claims | answer quality | low | Verify commit chain behind adapter-as-compiler and drop unsupported `syke.db` / MEMEX update claims. |
| R13 / pure | No material disagreement; both answers broadly pass/pass | rubric ambiguity | low | Spot-check cited memory IDs and commit-to-claim mapping. |
| R13 / zero | Strong overall; one judge stricter on timestamp precision | rubric ambiguity | low | Check exact March 15 turning-point timestamps and the 2026-02-17 inference. |
| R14 / production | Both candidates partially grounded; split is stale-thread recovery vs unsupported saved-to-MEMEX style claims | answer quality | high | Confirm true latest interactive session before cutoff and whether any `syke.db` / MEMEX save is evidenced. |
| R14 / pure | Same recency problem, extra disagreement over unsupported detail tolerance | answer quality | high | Separate March 16 observe-layer test thread from replay/Kimi blockage; verify claimed test counts. |
| R14 / zero | Bounded packet does not fix stale-thread issue; judges differ mainly on penalty severity | answer quality | high | Audit exact March 16 end state and any `finalize_memex` / replay claims. |
| R15 / production | Broadly aligned on thread, but judges split on invented commands and exact count splits | answer quality | medium | Verify sandbox command shape and any `33/27` or `17-cycle` style stats. |
| R15 / pure | Same as production, with more visible numeric drift | answer quality | medium | Confirm test totals, event counts, and whether synthesis stats belong to this slice. |
| R15 / zero | Near-consensus pass; minor precision hedge remains | rubric ambiguity | low | Check exact two-week filter and timing for the fresh-sandbox run. |
| R18 / production | Disagreement centers on replay-harness detail density: planned vs actual dataset and ablation setup blur | packet insufficiency | medium | Confirm canonical frozen dataset size/date range and actual ablation conditions. |
| R18 / pure | Same replay drift, with count/date mismatches more obvious than core structure | packet insufficiency | medium | Audit `128,904` vs `128,902`, `Mar 17` vs `Mar 21`, and source completeness. |
| R18 / zero | Judges split on whether answer cleanly separates planned simulation from actual replay data | rubric ambiguity | medium | Separate planned Mar 1-15 sim from actual frozen dataset and 3-condition ablation design. |
| R19 / production | Clear wrong-thread recovery; both judges reject answer as stale and misdirecting | answer quality | high | Verify what was actually last before cutoff and whether March 21 Syke cleanup / parallel runs are in scope. |
| R19 / pure | Still stale, but answer partially recovers Syke cleanup thread | answer quality | high | Check clean-slate commit order versus fresh-run order, plus missing latest interaction. |
| R19 / zero | Sharp split: one judge passes LM Studio thread, another rejects it as stale | rubric ambiguity | high | Identify true last interactive session on March 21 and whether it outranks replay cleanup thread. |

## High-Priority Human Review Queue

- `R03 / pure`
- `R07 / zero`
- `R08 / production`
- `R08 / pure`
- `R08 / zero`
- `R09 / production`
- `R09 / zero`
- `R14 / production`
- `R14 / pure`
- `R14 / zero`
- `R19 / production`
- `R19 / pure`
- `R19 / zero`

## Emerging Pattern

Most triage labels are not pure judge-bias cases. They cluster into:

- answer quality failures;
- freshness/current-state target ambiguity;
- packet insufficiency for design/replay-history probes;
- rubric ambiguity around how much unsupported detail to tolerate.

This supports the next step: claim-level audit before any architecture ranking.

