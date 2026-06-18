# ENGRAM Kit Checklist

Use this before sharing the participant kit.

## Public Package

- [x] README explains ENGRAM as a time-sequence memory challenge.
- [x] Contract is two commands: `update` and `answer`.
- [x] Sample states are real first-two-week daily ENGRAM states.
- [x] Sample questions are candidate-visible first-two-week questions with
  private answers, reference sets, and rubrics stripped.
- [x] Example submission runs locally.
- [x] Checker validates the example submission.
- [x] Private data, answers, judge packets, rubrics, QEMU details, dashboard
  internals, atlas/tracks artifacts, and provider credentials are absent.

## Researcher Instructions

- [x] Researchers can use any memory architecture.
- [x] `STATE_DIR` is defined as a full bounded state, not a diff.
- [x] `MEMORY_DIR` persists across the whole run.
- [x] `answer` happens after chronological `update` calls.
- [x] Answer JSON includes answer, evidence paths, optional memory refs, and
  uncertainty.
- [x] Future-state access, hidden judge material, and private data access are
  forbidden.
- [x] Network/model-provider requirements must be declared by the participant.

## Still Needed Before A Public Link

- [ ] Add final public repo URL.
- [ ] Add Discord or submission channel.
- [ ] Add QR code or short URL for the presentation.
- [ ] Decide public resource limits: timeout, disk, RAM, and network/model mode.
- [ ] Decide whether submissions arrive as PRs, zipped folders, or form uploads.
- [ ] Decide whether the public checker should run in CI.

## Operator-Only Follow-Up

- [ ] Keep private evaluation on the ENGRAM runtime side.
- [ ] Keep judge packets and private rubrics out of the kit.
- [ ] Map this two-command facade to the internal QEMU runner.
- [ ] Return results with scores, logs, and selected safe failure notes.
