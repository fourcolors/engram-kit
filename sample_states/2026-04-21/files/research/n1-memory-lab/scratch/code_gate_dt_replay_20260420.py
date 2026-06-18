"""Code-gate D_t replay on the 4 canonical 2x2 runs (opus/gpt agent x opus/gpt judge).

Implements stdlib-only versions of:
  d_time      -- date-leakage regex vs reference_dt
  d_artifact  -- top-5 named artifacts (files, SHAs, #issues) must appear in slice
  d_committed -- if local_git_anchor.json present and answer names a commit-prefix,
                 that prefix must match a commit in the anchor at/before reference_dt

No LLM calls. Reports codegate-vs-LLM flip counts, agreed-pass survival,
P<->F resolution, and cross-judge kappa before/after.

Outputs summary JSON and per-cell table to stdout; prints the markdown section
appended to AUTO_RESEARCH_LOOP_20260420.md.
"""

from __future__ import annotations

import json
import os
import re
from collections import Counter, defaultdict
from datetime import date
from typing import Dict, List, Optional, Tuple

LAB_ROOT = "/Users/saxenauts/Documents/personal/syke-replay-lab"
RUNS = {
    "opus_ask_opus_judge":  "ne13-real-15d-opus46-final-20260420T071500Z",
    "gpt_ask_gpt_judge":    "ne13-real-15d-gpt54-final-20260420T071500Z",
    "opus_ask_gpt_judge":   "ne13-real-15d-opusask-gpt54judge-20260420T144210Z",
    "gpt_ask_opus_judge":   "ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z",
}
# Map back to (agent, judge)
RUN_META = {
    "opus_ask_opus_judge":  ("opus", "opus"),
    "gpt_ask_gpt_judge":    ("gpt",  "gpt"),
    "opus_ask_gpt_judge":   ("opus", "gpt"),
    "gpt_ask_opus_judge":   ("gpt",  "opus"),
}

DATE_RE  = re.compile(r"\b(20\d{2})[-/](\d{2})[-/](\d{2})\b")
FILE_RE  = re.compile(r"\b[\w./\-]+\.(?:py|md|ts|tsx|jsonl?|yaml|yml|sh|html|css|toml|cfg)\b", re.IGNORECASE)
SHA_RE   = re.compile(r"\b[0-9a-f]{7,40}\b")
ISSUE_RE = re.compile(r"#\d{1,5}\b")

# Common English words that match the SHA regex (7-40 hex chars) -- none by construction,
# but SHA regex will catch things like "decade" no (letters e,a only). 7-40 hex means
# only chars in [0-9a-f]; plenty of false positives possible (e.g. "abcdefa"). Keep as-is.

# Stop list for FILE regex: very common path noise we don't want to grade on
FILE_STOP = {
    "readme.md", "notes.md", "todo.md", "index.json", "config.json",
    "package.json", "package-lock.json", "results.json", "requirements.txt",
}


def _parse_date(s: str) -> Optional[date]:
    try:
        y, m, d = s.split("-") if "-" in s else s.split("/")
        return date(int(y), int(m), int(d))
    except Exception:
        return None


def _parse_reference_dt(ref: str) -> Optional[date]:
    if not ref:
        return None
    m = DATE_RE.search(ref)
    if m:
        y, mo, d = m.group(1), m.group(2), m.group(3)
        try:
            return date(int(y), int(mo), int(d))
        except Exception:
            return None
    return None


def extract_future_dates(answer: str, ref_dt: date) -> List[str]:
    out = []
    for m in DATE_RE.finditer(answer):
        y, mo, d = m.group(1), m.group(2), m.group(3)
        try:
            dt = date(int(y), int(mo), int(d))
        except Exception:
            continue
        if dt > ref_dt:
            out.append(m.group(0))
    return out


def top_artifacts(answer: str, k: int = 5) -> List[Tuple[str, str]]:
    """Return up to k (kind, token) distinctive artifacts ranked by mention count.

    Note: git-SHA-looking tokens are *not* treated as d_artifact candidates -
    they live under d_committed (anchor check). Slice doesn't mirror the git
    history; substring match against slice content would be unsound for SHAs."""
    cand: List[Tuple[str, str]] = []
    for m in FILE_RE.finditer(answer):
        tok = m.group(0)
        if tok.lower() in FILE_STOP:
            continue
        if len(tok) < 4:
            continue
        cand.append(("file", tok))
    for m in ISSUE_RE.finditer(answer):
        cand.append(("issue", m.group(0)))

    # rank by frequency, prefer longer tokens on ties, stable order
    count: Counter = Counter(cand)
    ranked = sorted(count.items(), key=lambda kv: (-kv[1], -len(kv[0][1]), kv[0][1]))
    out: List[Tuple[str, str]] = []
    seen_tokens = set()
    for (kind, tok), _ in ranked:
        t_norm = tok.lower()
        if t_norm in seen_tokens:
            continue
        seen_tokens.add(t_norm)
        out.append((kind, tok))
        if len(out) >= k:
            break
    return out


def find_slice_dir(cell: Dict, run_dir: str) -> Optional[str]:
    """Return slice dir. cell['artifacts']['slice_dir'] usually points at ~/.syke-lab/.../slices/NE-1.3__Rxx.
    Fallback: runs/<run>/evidence/<cond>/<probe>/slice (symlink)."""
    s = cell.get("artifacts", {}).get("slice_dir")
    if s and os.path.isdir(s):
        return s
    cond = cell.get("condition")
    probe = cell.get("probe_id")
    fb = os.path.join(run_dir, "evidence", cond, probe, "slice")
    if os.path.isdir(fb):
        return os.path.realpath(fb)
    return None


def find_git_anchor(cell: Dict, run_dir: str) -> Optional[str]:
    cond = cell.get("condition")
    probe = cell.get("probe_id")
    candidates = [
        os.path.join(run_dir, "evidence", cond, probe, "local_git_anchor.json"),
        # slice root sometimes holds one too
    ]
    s = cell.get("artifacts", {}).get("slice_dir")
    if s:
        candidates.append(os.path.join(s, "local_git_anchor.json"))
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


# -- Slice search cache: load each slice once per probe, concat into lowercase blob --
_SLICE_CACHE: Dict[str, str] = {}


def slice_blob(slice_dir: str) -> str:
    """Return a lowercase blob of slice contents AND file paths.

    Including file paths in the blob lets the d_artifact check match answers
    that cite filenames which exist as tree entries even when the content does
    not re-quote the filename."""
    if slice_dir in _SLICE_CACHE:
        return _SLICE_CACHE[slice_dir]
    pieces = []
    for root, _dirs, files in os.walk(slice_dir):
        for f in files:
            fp = os.path.join(root, f)
            pieces.append(fp)  # include full path (catches filenames cited in answers)
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                    pieces.append(fh.read())
            except OSError:
                continue
    blob = "\n".join(pieces).lower()
    _SLICE_CACHE[slice_dir] = blob
    return blob


def artifact_hits(blob: str, artifacts: List[Tuple[str, str]]) -> List[Tuple[Tuple[str, str], bool]]:
    out = []
    for kind, tok in artifacts:
        needle = tok.lower()
        if kind == "sha":
            # allow prefix match: 7-char min already; require exact substring presence
            hit = needle in blob
        elif kind == "issue":
            hit = needle in blob
        else:
            # file paths: either full substring, or basename substring
            hit = needle in blob
            if not hit:
                base = needle.rsplit("/", 1)[-1]
                if base and base != needle and len(base) >= 5:
                    hit = base in blob
        out.append(((kind, tok), hit))
    return out


COMMIT_CTX_RE = re.compile(
    r"(?i)\b(commit|sha|shas|ref|git|revision|merge)\b[^\n]{0,80}?\b([0-9a-f]{7,40})\b|"
    r"\b([0-9a-f]{7,40})\b[^\n]{0,40}?\b(commit|sha|ref|revision)\b"
)

def d_committed_check(answer: str, anchor_path: Optional[str], ref_dt: date) -> Tuple[str, str]:
    """Return (verdict in {PASS,FAIL,NA}, note).

    Only fires when the answer *frames* a hex token as a git commit (nearby
    keyword: commit/sha/ref/git/...). Memex/memory-ID hex tokens don't qualify.
    """
    if not anchor_path:
        return ("NA", "no anchor")
    try:
        with open(anchor_path) as f:
            anc = json.load(f)
    except Exception as e:
        return ("NA", f"anchor load error: {e}")
    commits = anc.get("commits") or []
    if not commits:
        return ("NA", "empty commits in anchor")
    anchor_shas = [c.get("sha", "").lower() for c in commits if c.get("sha")]

    # Collect only hex tokens framed as commits/shas/refs
    answer_shas: List[str] = []
    for m in COMMIT_CTX_RE.finditer(answer):
        tok = (m.group(2) or m.group(3) or "").lower()
        if tok and any(c.isdigit() for c in tok):
            answer_shas.append(tok)
    answer_shas = list(dict.fromkeys(answer_shas))
    if not answer_shas:
        return ("NA", "answer names no commit-framed hex token")

    missing = []
    for ash in answer_shas:
        if not any(full.startswith(ash) for full in anchor_shas):
            missing.append(ash)
    if missing:
        return ("FAIL", f"{len(missing)}/{len(answer_shas)} shas not in anchor: {missing[:5]}")
    return ("PASS", f"{len(answer_shas)} shas all present in anchor")


def load_run(run_key: str):
    run_dir = os.path.join(LAB_ROOT, "runs", RUNS[run_key])
    with open(os.path.join(run_dir, "results.json")) as f:
        rows = json.load(f)
    return run_dir, rows


def process_run(run_key: str) -> List[Dict]:
    run_dir, rows = load_run(run_key)
    cells = []
    for r in rows:
        probe = r["probe_id"]
        cond = r["condition"]
        ans = r.get("answer_text") or ""
        ref_dt_str = r.get("reference_dt")
        ref_dt = _parse_reference_dt(ref_dt_str)
        llm_verdict = (r.get("judge_result") or {}).get("overall_verdict") or r.get("verdict") or "invalid"

        # d_time
        if ref_dt:
            leaks = extract_future_dates(ans, ref_dt)
        else:
            leaks = []
        d_time = "FAIL" if leaks else "PASS"

        # d_artifact
        slice_dir = find_slice_dir(r, run_dir)
        arts = top_artifacts(ans, k=5)
        if slice_dir and arts:
            blob = slice_blob(slice_dir)
            hits = artifact_hits(blob, arts)
            missing = [(k, t) for (k, t), h in hits if not h]
            d_artifact = "FAIL" if missing else "PASS"
        elif not arts:
            d_artifact = "NA"
            hits = []
            missing = []
        else:
            d_artifact = "NA"
            hits = []
            missing = []

        # d_committed
        anchor_path = find_git_anchor(r, run_dir)
        d_committed, d_c_note = d_committed_check(ans, anchor_path, ref_dt) if ref_dt else ("NA", "no ref_dt")

        # codegate verdict: any FAIL -> fail; else keep LLM verdict
        fails = [x for x in (d_time, d_artifact, d_committed) if x == "FAIL"]
        codegate_verdict = "fail" if fails else llm_verdict

        cells.append({
            "run_key": run_key,
            "probe": probe, "condition": cond,
            "ref_dt": ref_dt_str,
            "llm_verdict": llm_verdict,
            "d_time_code": d_time,
            "d_artifact_code": d_artifact,
            "d_committed_code": d_committed,
            "d_committed_note": d_c_note,
            "leaked_dates": leaks,
            "top_artifacts": arts,
            "missing_artifacts": missing,
            "codegate_verdict": codegate_verdict,
            "slice_dir_resolved": slice_dir,
            "anchor_resolved": anchor_path,
        })
    return cells


def kappa_3level(a: List[str], b: List[str]) -> Tuple[int, float, float]:
    """Cohen's kappa on fail=0, partial=1, pass=2. Excludes invalid and missing."""
    order = {"fail": 0, "partial": 1, "pass": 2}
    pairs = [(order[x], order[y]) for x, y in zip(a, b) if x in order and y in order]
    n = len(pairs)
    if n == 0:
        return (0, 0.0, 0.0)
    exact = sum(1 for x, y in pairs if x == y) / n
    ra = Counter(x for x, _ in pairs)
    rb = Counter(y for _, y in pairs)
    pe = sum((ra[i] / n) * (rb[i] / n) for i in range(3))
    if pe >= 0.999999:
        return (n, exact, 1.0)
    k = (exact - pe) / (1 - pe)
    return (n, exact, k)


def main():
    all_cells: Dict[str, List[Dict]] = {}
    for rk in RUNS:
        all_cells[rk] = process_run(rk)

    # ---- codegate flip counts per run ----
    print("\n=== codegate flip counts per run ===")
    flip_summary = {}
    for rk, cells in all_cells.items():
        ctr = Counter()
        per_axis_fail = Counter()
        for c in cells:
            ctr[(c["llm_verdict"], c["codegate_verdict"])] += 1
            for ax in ("d_time_code", "d_artifact_code", "d_committed_code"):
                if c[ax] == "FAIL":
                    per_axis_fail[ax] += 1
        flip_summary[rk] = dict(ctr)
        print(f"\n{rk} (n={len(cells)})")
        print(f"  axis FAIL counts: {dict(per_axis_fail)}")
        # summarize directional flips: LLM -> codegate
        direction = Counter()
        for c in cells:
            if c["llm_verdict"] != c["codegate_verdict"]:
                direction[f"{c['llm_verdict']}->{c['codegate_verdict']}"] += 1
        print(f"  flips: {dict(direction)}  total flipped={sum(direction.values())}")

    # ---- Agreed-pass survival ----
    # Agreed-pass cells are from the 2x2 cross: one agent, both judges both say pass.
    # Pair agent-side runs: same agent x different judges.
    print("\n=== agreed-pass anchor survival ===")
    pairings = {
        "gpt_agent":  ("gpt_ask_gpt_judge",  "gpt_ask_opus_judge"),   # both on gpt-agent
        "opus_agent": ("opus_ask_opus_judge","opus_ask_gpt_judge"),    # both on opus-agent
    }
    agreed_pass_cells = []
    for agent, (rA, rB) in pairings.items():
        idxA = {(c["probe"], c["condition"]): c for c in all_cells[rA]}
        idxB = {(c["probe"], c["condition"]): c for c in all_cells[rB]}
        for key, a in idxA.items():
            b = idxB.get(key)
            if not b:
                continue
            if a["llm_verdict"] == "pass" and b["llm_verdict"] == "pass":
                # under codegate?
                a_pass_cg = a["codegate_verdict"] == "pass"
                b_pass_cg = b["codegate_verdict"] == "pass"
                survives = a_pass_cg and b_pass_cg
                agreed_pass_cells.append({
                    "agent": agent, "probe": key[0], "condition": key[1],
                    "a_cg": a["codegate_verdict"], "b_cg": b["codegate_verdict"],
                    "survives": survives,
                    "a_fail_axis": [ax for ax in ("d_time_code","d_artifact_code","d_committed_code") if a[ax] == "FAIL"],
                    "b_fail_axis": [ax for ax in ("d_time_code","d_artifact_code","d_committed_code") if b[ax] == "FAIL"],
                    "a_missing_art": a["missing_artifacts"],
                    "b_missing_art": b["missing_artifacts"],
                })
    n_pass = len(agreed_pass_cells)
    n_surv = sum(1 for c in agreed_pass_cells if c["survives"])
    print(f"agreed-pass cells (LLM): n={n_pass}, surviving under codegate={n_surv}")
    for c in agreed_pass_cells:
        print(f"  [{c['agent']}] {c['probe']}/{c['condition']}: a_cg={c['a_cg']} b_cg={c['b_cg']} survives={c['survives']}")
        if not c["survives"]:
            print(f"    a_fail={c['a_fail_axis']} a_missing={c['a_missing_art']}")
            print(f"    b_fail={c['b_fail_axis']} b_missing={c['b_missing_art']}")

    # ---- P<->F resolution (the 3 full-band disagreement cells from iter-1) ----
    print("\n=== P<->F structural-bias cells ===")
    pf_cells = [
        ("gpt_agent",  "R03", "pure",       "gpt_ask_gpt_judge",  "fail", "gpt_ask_opus_judge",  "pass"),
        ("opus_agent", "R05", "production", "opus_ask_opus_judge","pass", "opus_ask_gpt_judge",  "fail"),
        ("opus_agent", "R19", "zero",       "opus_ask_opus_judge","pass", "opus_ask_gpt_judge",  "fail"),
    ]
    for agent, probe, cond, rA, vA, rB, vB in pf_cells:
        cA = next(c for c in all_cells[rA] if c["probe"] == probe and c["condition"] == cond)
        cB = next(c for c in all_cells[rB] if c["probe"] == probe and c["condition"] == cond)
        print(f"\n[{agent}] {probe}/{cond}")
        print(f"  LLM:  {rA}={vA}  {rB}={vB}")
        print(f"  CG:   {rA}={cA['codegate_verdict']}  {rB}={cB['codegate_verdict']}")
        print(f"  axes {rA}: d_time={cA['d_time_code']} d_artifact={cA['d_artifact_code']} d_committed={cA['d_committed_code']}")
        print(f"  axes {rB}: d_time={cB['d_time_code']} d_artifact={cB['d_artifact_code']} d_committed={cB['d_committed_code']}")
        print(f"  missing_arts {rA}: {cA['missing_artifacts']}")
        print(f"  missing_arts {rB}: {cB['missing_artifacts']}")
        # resolution: did codegate agree where LLM disagreed?
        agree = cA['codegate_verdict'] == cB['codegate_verdict']
        print(f"  codegate AGREES: {agree}")

    # ---- Cross-judge kappa before/after (on both agent sides) ----
    print("\n=== cross-judge kappa (3-level) before/after codegate ===")
    for agent, (rA, rB) in pairings.items():
        idxA = {(c["probe"], c["condition"]): c for c in all_cells[rA]}
        idxB = {(c["probe"], c["condition"]): c for c in all_cells[rB]}
        keys = sorted(set(idxA) & set(idxB))
        vllm_a = [idxA[k]["llm_verdict"] for k in keys]
        vllm_b = [idxB[k]["llm_verdict"] for k in keys]
        vcg_a  = [idxA[k]["codegate_verdict"] for k in keys]
        vcg_b  = [idxB[k]["codegate_verdict"] for k in keys]
        n1, e1, k1 = kappa_3level(vllm_a, vllm_b)
        n2, e2, k2 = kappa_3level(vcg_a,  vcg_b)
        print(f"{agent}: LLM n={n1} exact={e1:.3f} kappa={k1:.3f} | CG n={n2} exact={e2:.3f} kappa={k2:.3f}")

    # --- resolvable N ---
    resolvable = {}
    for rk, cells in all_cells.items():
        n_slice = sum(1 for c in cells if c["slice_dir_resolved"])
        n_anchor = sum(1 for c in cells if c["anchor_resolved"])
        n_ref = sum(1 for c in cells if c["ref_dt"])
        resolvable[rk] = {"n_cells": len(cells), "slice_ok": n_slice, "anchor_ok": n_anchor, "ref_dt_ok": n_ref}
    print("\n=== resolvable coverage ===")
    for rk, v in resolvable.items():
        print(f"{rk}: {v}")

    # Dump full table
    out = {
        "all_cells": all_cells,
        "agreed_pass_codegate": agreed_pass_cells,
        "resolvable": resolvable,
    }
    # keep only small summary
    print("\n=== summary bundle saved ===")
    # Small: write to json next to script
    out_path = os.path.join(LAB_ROOT, "research/n1-memory-lab/scratch/code_gate_dt_replay_20260420.json")
    # Truncate overly large fields for the JSON dump
    def _slim(cells):
        slim = []
        for c in cells:
            sc = {k: v for k, v in c.items() if k not in ("slice_dir_resolved",)}
            slim.append(sc)
        return slim
    out_json = {
        "summary_by_run": {rk: {
            "n": len(all_cells[rk]),
            "axis_FAIL_counts": dict(Counter(
                ax for c in all_cells[rk] for ax in ("d_time_code","d_artifact_code","d_committed_code") if c[ax]=="FAIL"
            )),
            "flip_directions": dict(Counter(
                f"{c['llm_verdict']}->{c['codegate_verdict']}" for c in all_cells[rk] if c['llm_verdict']!=c['codegate_verdict']
            )),
        } for rk in all_cells},
        "cells_by_run": {rk: _slim(all_cells[rk]) for rk in all_cells},
        "agreed_pass": agreed_pass_cells,
        "resolvable": resolvable,
    }
    with open(out_path, "w") as f:
        json.dump(out_json, f, indent=2, default=str)
    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
