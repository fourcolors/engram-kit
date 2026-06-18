# State Format

Each state directory is a full bounded workspace state for one date or reference
time. It is not only a diff.

Example:

```text
sample_states/2026-04-09/
  README.md
  state_meta.json
  files/
  manifest.tsv
  git_log.txt
  changes.txt
```

## `files/`

The workspace files visible at this state.

Your system may read these files during `update` and `answer`. Later files and
later edits are not included.

## `manifest.tsv`

Tab-separated file inventory.

```text
path	size	sha256	status	source_class	evidence	notes
```

Fields:

- `path`: path relative to `files/`
- `size`: byte size
- `sha256`: content hash when known
- `status`: `exact` or `approximate` for present sample files
- `source_class`: source/recovery class from ENGRAM construction
- `evidence`: bounded evidence type for this file at this state
- `notes`: construction note

Use the manifest as file evidence, not as an answer key.

## `state_meta.json`

Machine-readable state summary: state id, date, reference time, cadence, visible
path counts, exact/approximate counts, and bounded Git counts.

## `git_log.txt`

Bounded commit/history evidence visible at this state, when available.

Commit subjects can help reconstruct work, but they are not guaranteed to be
truth. Treat them as workspace evidence, not an oracle.

## `changes.txt`

Human-readable summary of changes since the previous state.

This is convenience evidence. Your system should still be able to inspect
`files/` and `manifest.tsv` directly.

## `README.md`

Short state note with date, reference time, and public-export caveats.

The private ENGRAM environment may have richer internal metadata. The public
contract is only the state folder.
