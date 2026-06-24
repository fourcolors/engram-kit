"""Deterministic summaries for large structured data files (JSON/CSV/TSV).

Big record-array files (e.g. 79 KB psyche_asks_all.json) don't fit the answer
digest, so the model used to hedge "contents not shown". Instead we compute — in
stdlib Python, at answer time — a compact summary: schema + EXACT per-field
aggregates + a stratified sample + an honest note. Counts/diffs are computed, never
left to the LLM. Plus a cross-file set-difference for "what got dropped/filtered"
questions. No new deps; no-hindsight (reads the live current-state file).
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from pathlib import Path

from util import read_text

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}")
_DIFF_TRIGGERS = (
    "drop", "dropped", "filter", "filtered", "difference", "removed", "remove",
    "exclude", "excluded", "missing", "added", "subset", "superset", "versus", " vs ",
)


def _short(v, n: int = 60) -> str:
    s = str(v).replace("\n", " ").strip()
    return s if len(s) <= n else s[:n] + "…"


def load_records(path: Path):
    """Return (records, fields, extra_scalars) for a uniform record file, else None."""
    suf = path.suffix.lower()
    if suf in (".tsv", ".csv"):
        delim = "\t" if suf == ".tsv" else ","
        with path.open(encoding="utf-8", errors="replace", newline="") as f:
            recs = list(csv.DictReader(f, delimiter=delim))
        fields = list(recs[0].keys()) if recs else []
        if len(recs) < 2 or not fields:
            return None
        return recs, fields, {}

    data = json.loads(read_text(path))
    extra: dict = {}
    if isinstance(data, list):
        recs = data
    elif isinstance(data, dict):
        best = None
        for k, v in data.items():
            if isinstance(v, list) and v and all(isinstance(x, dict) for x in v[:20]):
                if best is None or len(v) > len(data[best]):
                    best = k
            elif not isinstance(v, (list, dict)):
                extra[k] = v
        if best is None:
            return None
        recs = data[best]
    else:
        return None

    recs = [r for r in recs if isinstance(r, dict)]
    if len(recs) < 2:
        return None
    keyc: Counter = Counter()
    for r in recs[:1000]:
        keyc.update(r.keys())
    n = min(len(recs), 1000)
    fields = [k for k, c in keyc.items() if c >= n * 0.6]
    return (recs, fields, extra) if fields else None


def _stratum_field(recs, fields) -> str | None:
    best, best_card = None, 0
    for f in fields:
        card = len({str(r.get(f)) for r in recs})
        if 2 <= card <= 25 and card > best_card:
            best, best_card = f, card
    return best


def summarize_structured(path: Path, rel: str) -> str | None:
    try:
        res = load_records(path)
    except Exception:
        return None
    if not res:
        return None
    recs, fields, extra = res
    n = len(recs)
    out = [f"### files/{rel}  [STRUCTURED SUMMARY — deterministic, computed over all {n} records]"]
    if extra:
        out.append("top-level: " + ", ".join(f"{k}={_short(v, 40)}" for k, v in list(extra.items())[:6]))
    out.append(f"records: {n}; schema (fields present in ≥60%): {', '.join(fields)}")

    for f in fields:
        vals = [r.get(f) for r in recs if r.get(f) not in (None, "")]
        distinct = {str(v) for v in vals}
        if not vals:
            continue
        if len(distinct) <= 25:
            vc = Counter(str(v) for v in vals).most_common(12)
            out.append(f"  {f} — value_counts: " + "; ".join(f"{_short(k, 40)}={c}" for k, c in vc))
        elif all(_DATE.match(str(v)) for v in vals[:50]):
            out.append(f"  {f} — date range: {min(str(v) for v in vals)} .. {max(str(v) for v in vals)} ({len(distinct)} distinct)")
        else:
            out.append(f"  {f} — {len(distinct)} distinct (high cardinality); e.g. " +
                       "; ".join(_short(v, 40) for v in list(distinct)[:3]))

    sf = _stratum_field(recs, fields)
    sample = []
    if sf:
        by: dict = {}
        for r in recs:
            by.setdefault(str(r.get(sf)), []).append(r)
        for _val, group in list(by.items())[:10]:
            sample.append(group[0])
            if len(group) > 1 and len(sample) < 12:
                sample.append(group[-1])
    else:
        sample = recs[:4] + recs[-2:]
    out.append(f"sample ({'stratified by ' + sf if sf else 'head+tail'}, {min(len(sample), 12)} of {n}):")
    for r in sample[:12]:
        out.append("  {" + ", ".join(f"{k}={_short(r.get(k), 50)}" for k in fields) + "}")
    out.append("NOTE: summary of the FULL file (all records read); counts/ranges are EXACT; "
               "individual non-sampled rows are not shown verbatim — the file is present, not unavailable.")
    return "\n".join(out)


def crossfile_diffs(question: str, specs: list[tuple[str, Path]]) -> str:
    """For set-relation questions: exact A−B / B−A over same-schema structured files."""
    ql = question.lower()
    if not any(t in ql for t in _DIFF_TRIGGERS):
        return ""
    loaded = []
    for rel, p in specs:
        try:
            res = load_records(p)
        except Exception:
            res = None
        if res:
            loaded.append((rel, res[0], tuple(sorted(res[1]))))
    blocks = []
    for i in range(len(loaded)):
        for j in range(i + 1, len(loaded)):
            relA, recA, sigA = loaded[i]
            relB, recB, sigB = loaded[j]
            if sigA != sigB or not sigA:
                continue
            kf = list(sigA)

            def key(r):
                return tuple(str(r.get(k, "")) for k in kf)

            a = {key(r): r for r in recA}
            b = {key(r): r for r in recB}
            onlyA = [a[k] for k in a.keys() - b.keys()]
            onlyB = [b[k] for k in b.keys() - a.keys()]
            if not onlyA and not onlyB:
                continue
            blk = [f"## structured set-difference: {relA} ({len(recA)}) vs {relB} ({len(recB)}) "
                   f"— keyed on full record {kf}, computed over both full files"]
            for label, only, other in ((relA, onlyA, relB), (relB, onlyB, relA)):
                blk.append(f"in {label} but NOT {other}: {len(only)}")
                if only:
                    sf = _stratum_field(only, kf) if len(only) > 3 else None
                    if sf:
                        bc = Counter(str(r.get(sf)) for r in only).most_common()
                        blk.append("  by " + sf + ": " + "; ".join(f"{_short(k, 30)}={c}" for k, c in bc))
                    for r in only[:25]:
                        blk.append("    {" + ", ".join(f"{k}={_short(r.get(k), 45)}" for k in kf) + "}")
                    if len(only) > 25:
                        blk.append(f"    …(+{len(only) - 25} more)")
            blocks.append("\n".join(blk))
    return "\n\n".join(blocks[:2])
