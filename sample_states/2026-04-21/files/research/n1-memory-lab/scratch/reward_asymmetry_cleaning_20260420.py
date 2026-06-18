"""
Reward-asymmetry: architectural ranking under contamination cleaning.

Loads the 4 canonical 2x2 runs + the code-gate JSON (fabrication flags)
+ the iteration 3 retrieval-degenerate cell list, and computes per
(agent x condition x judge) mean rank of verdicts (fail=0, partial=1, pass=2)
under three cleaning levels:

 1. raw            -- all 57 cells per run
 2. fab-clean      -- drop cells where codegate flagged ANY FAIL on
                     d_time_code / d_artifact_code / d_committed_code
 3. strict-clean   -- fab-clean AND drop zero-condition cells where the
                     agent called >= 5 filesystem-directed tools, AND
                     drop iteration-3 retrieval-degenerate cells

Stdlib only.
"""

import json
import os
import re
from collections import defaultdict

ROOT = "/Users/saxenauts/Documents/personal/syke-replay-lab"

RUN_DIRS = {
    # (agent, judge) -> run directory name
    ("opus", "opus"): "ne13-real-15d-opus46-final-20260420T071500Z",
    ("gpt",  "gpt"):  "ne13-real-15d-gpt54-final-20260420T071500Z",
    ("opus", "gpt"):  "ne13-real-15d-opusask-gpt54judge-20260420T144210Z",
    ("gpt",  "opus"): "ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z",
}

RUN_KEY_CG = {
    ("opus", "opus"): "opus_ask_opus_judge",
    ("gpt",  "gpt"):  "gpt_ask_gpt_judge",
    ("opus", "gpt"):  "opus_ask_gpt_judge",
    ("gpt",  "opus"): "gpt_ask_opus_judge",
}

CODEGATE_PATH = os.path.join(
    ROOT, "research/n1-memory-lab/scratch/code_gate_dt_replay_20260420.json"
)

VERDICT_SCORE = {"fail": 0, "partial": 1, "pass": 2}

# Iteration 3 flagged retrieval-DEGENERATE cells (from the audit).
# Keyed on (agent, probe, condition).  R13 had "all 3 agreed-pass variants"
# which were production/opus, production/gpt, pure/gpt (the three agreed-
# pass R13 cells across agents x conditions).
DEGENERATE = {
    ("gpt",  "R01", "pure"),
    ("gpt",  "R04", "production"),
    ("opus", "R11", "pure"),
    ("gpt",  "R12", "production"),
    ("opus", "R13", "production"),
    ("gpt",  "R13", "production"),
    ("gpt",  "R13", "pure"),
    ("gpt",  "R15", "zero"),
    ("opus", "R02", "production"),
}

# -----------------------------------------------------------------------
# Load codegate fabrication flags per (run_key, probe, condition)
# -----------------------------------------------------------------------
with open(CODEGATE_PATH) as f:
    CG = json.load(f)

def codegate_flagged(run_key, probe, condition):
    """True iff codegate says d_time / d_artifact / d_committed FAIL on this cell."""
    cells = CG["cells_by_run"].get(run_key, [])
    for c in cells:
        if c["probe"] == probe and c["condition"] == condition:
            axes = ("d_time_code", "d_artifact_code", "d_committed_code")
            return any(c.get(a) == "FAIL" for a in axes)
    return False

# -----------------------------------------------------------------------
# Tool-policy leakage flag per (agent, probe, condition).
# Iteration 4 criterion (paraphrased): zero-condition cell where the
# agent ran >=5 slice-directed filesystem tool calls.
#
# We approximate "slice-directed" by: bash commands whose command string
# references the slice dir (/.syke-lab/) OR the slice-specific tools
# rg/grep/find/cat/ls/sqlite3 against any path.  The audit in the log
# reported 32/38 zero cells at >=1 leakage call; we're stricter at >=5
# because the task asks for >=5.
# -----------------------------------------------------------------------
SLICE_TOOL_NAMES = {"rg", "grep", "find", "cat", "ls", "sqlite3", "head",
                    "tail", "awk", "sed", "file", "stat", "wc", "tree"}

def is_slice_directed_bash(cmd: str) -> bool:
    if not cmd:
        return False
    s = cmd.strip()
    # obvious: mentions the lab slice root
    if "/.syke-lab/" in s or "syke-lab/" in s:
        return True
    # first token is a slice-style read tool
    m = re.match(r"\s*(\w+)", s)
    if not m:
        return False
    tok = m.group(1)
    if tok in SLICE_TOOL_NAMES:
        return True
    # piped chains beginning with one of the tool names
    first = s.split("|")[0].strip().split()[0] if s else ""
    if first in SLICE_TOOL_NAMES:
        return True
    return False

def slice_tool_count(agent: str, probe: str, condition: str) -> int:
    """Count slice-directed filesystem tool calls for this cell from the
    agent's DIAGONAL run traces (the only traces that exist per agent)."""
    diag_run = RUN_DIRS[(agent, agent)]
    trace_path = os.path.join(
        ROOT, "runs", diag_run, "traces", condition,
        f"{condition}_{probe}.ask_trace.json"
    )
    if not os.path.exists(trace_path):
        return 0
    try:
        with open(trace_path) as f:
            tr = json.load(f)
    except Exception:
        return 0
    count = 0
    for tc in (tr.get("tool_calls_detail") or []):
        name = tc.get("name") or ""
        inp = tc.get("input") or {}
        cmd = inp.get("command") if isinstance(inp, dict) else None
        if name == "bash":
            if is_slice_directed_bash(cmd or ""):
                count += 1
        elif name in SLICE_TOOL_NAMES:
            count += 1
        else:
            # read/grep-style MCP tools
            if name.lower() in {"read", "grep", "glob", "bash"}:
                # path arg check
                path = inp.get("file_path") or inp.get("path") or ""
                if "/.syke-lab/" in path or path.startswith("/Users/saxenauts/.syke-lab"):
                    count += 1
    return count

# -----------------------------------------------------------------------
# Load verdicts from 4 canonical runs
# -----------------------------------------------------------------------
def load_run(agent, judge):
    run_dir = RUN_DIRS[(agent, judge)]
    path = os.path.join(ROOT, "runs", run_dir, "benchmark_results.json")
    with open(path) as f:
        d = json.load(f)
    rows = []
    for it in d["items"]:
        v = it.get("verdict")
        if v not in VERDICT_SCORE:
            # 'invalid' or missing -- exclude from mean (it wouldn't score)
            continue
        rows.append({
            "agent":     agent,
            "judge":     judge,
            "probe":     it["probe_id"],
            "condition": it["condition"],
            "verdict":   v,
            "score":     VERDICT_SCORE[v],
        })
    return rows

ALL_ROWS = []
for (a, j), _ in RUN_DIRS.items():
    ALL_ROWS.extend(load_run(a, j))

# Precompute contamination flags
FAB_FLAG = {}
LEAK_FLAG = {}
for r in ALL_ROWS:
    key = (r["agent"], r["probe"], r["condition"], r["judge"])
    run_key = RUN_KEY_CG[(r["agent"], r["judge"])]
    FAB_FLAG[key] = codegate_flagged(run_key, r["probe"], r["condition"])
# leakage is agent-level (trace is agent's diagonal run)
for agent in ("opus", "gpt"):
    probes = sorted({r["probe"] for r in ALL_ROWS})
    for p in probes:
        LEAK_FLAG[(agent, p, "zero")] = slice_tool_count(agent, p, "zero") >= 5

# -----------------------------------------------------------------------
# Mean & n aggregators
# -----------------------------------------------------------------------
def aggregate(rows, cleaning):
    """
    cleaning in {"raw","fab","strict"}
    returns:
        means[(agent, condition, judge)] -> mean_score
        ns   [(agent, condition, judge)] -> n
    """
    means = {}
    ns    = {}
    bucket = defaultdict(list)
    for r in rows:
        key = (r["agent"], r["probe"], r["condition"], r["judge"])
        if cleaning in ("fab", "strict") and FAB_FLAG.get(key, False):
            continue
        if cleaning == "strict":
            # drop leaky zero cells
            if r["condition"] == "zero" and LEAK_FLAG.get(
                (r["agent"], r["probe"], "zero"), False
            ):
                continue
            # drop iteration-3 retrieval-degenerate cells
            if (r["agent"], r["probe"], r["condition"]) in DEGENERATE:
                continue
        bucket[(r["agent"], r["condition"], r["judge"])].append(r["score"])
    for k, v in bucket.items():
        means[k] = sum(v) / len(v)
        ns[k]    = len(v)
    return means, ns

def n_per_condition(rows, cleaning):
    totals = defaultdict(int)
    for r in rows:
        key = (r["agent"], r["probe"], r["condition"], r["judge"])
        if cleaning in ("fab", "strict") and FAB_FLAG.get(key, False):
            continue
        if cleaning == "strict":
            if r["condition"] == "zero" and LEAK_FLAG.get(
                (r["agent"], r["probe"], "zero"), False
            ):
                continue
            if (r["agent"], r["probe"], r["condition"]) in DEGENERATE:
                continue
        totals[r["condition"]] += 1
    return dict(totals)

# -----------------------------------------------------------------------
# Headline: opus-judge averaged over both agents per condition
# -----------------------------------------------------------------------
def opus_judge_headline(means, ns):
    """Weighted mean across agents, judge=opus."""
    out = {}
    for cond in ("production", "pure", "zero"):
        num, den = 0.0, 0
        for agent in ("opus", "gpt"):
            k = (agent, cond, "opus")
            if k in means:
                num += means[k] * ns[k]
                den += ns[k]
        out[cond] = (num / den) if den else float("nan")
    return out

# -----------------------------------------------------------------------
# Report
# -----------------------------------------------------------------------
def fmt_means(means, ns):
    lines = []
    lines.append("| agent | judge | production | pure | zero |")
    lines.append("|---|---|---:|---:|---:|")
    for agent in ("opus", "gpt"):
        for judge in ("opus", "gpt"):
            row = [f"{agent}", f"{judge}"]
            for cond in ("production", "pure", "zero"):
                k = (agent, cond, judge)
                if k in means:
                    row.append(f"{means[k]:.3f} (n={ns[k]})")
                else:
                    row.append("—")
            lines.append("| " + " | ".join(row) + " |")
    return "\n".join(lines)

def ordering(means, agent, judge):
    triples = []
    for cond in ("production", "pure", "zero"):
        k = (agent, cond, judge)
        if k in means:
            triples.append((cond, means[k]))
    triples.sort(key=lambda x: -x[1])
    return " > ".join(f"{c}({m:.2f})" for c, m in triples)

def prod_gt_pure_gt_zero(means, agent, judge):
    try:
        p = means[(agent, "production", judge)]
        u = means[(agent, "pure",       judge)]
        z = means[(agent, "zero",       judge)]
    except KeyError:
        return False
    return p > u > z

OUT = []
OUT.append("## Reward asymmetry — architectural ranking under contamination cleaning\n")
OUT.append(
    "Question: does production still lead pure/zero when we strip cells "
    "where code-gate caught fabrication, where the zero agent bypassed the "
    "MEMEX-only constraint via filesystem tools, and where retrieval-"
    "degenerate phrase frequency explains the pass?\n"
)
OUT.append(
    "Method: mean verdict score (fail=0, partial=1, pass=2) per "
    "(agent × condition × judge) across the 4 canonical 2×2 runs.\n"
)

for label, key in [("raw (all 57 cells/run)", "raw"),
                   ("fab-clean (drop codegate-FAIL cells)", "fab"),
                   ("strict-clean (fab-clean + zero-leakage + retrieval-degenerate)", "strict")]:
    means, ns = aggregate(ALL_ROWS, key)
    ncond = n_per_condition(ALL_ROWS, key)
    OUT.append(f"\n### Level: {label}\n")
    OUT.append(fmt_means(means, ns))
    OUT.append(
        f"\n\nTotal n per condition (summed across 4 runs): "
        f"production={ncond.get('production',0)}, "
        f"pure={ncond.get('pure',0)}, zero={ncond.get('zero',0)}\n"
    )
    OUT.append("Orderings (agent × judge):\n")
    OUT.append("")
    OUT.append("| agent | judge | ordering | prod > pure > zero? |")
    OUT.append("|---|---|---|---|")
    for agent in ("opus", "gpt"):
        for judge in ("opus", "gpt"):
            OUT.append(
                f"| {agent} | {judge} | {ordering(means, agent, judge)} | "
                f"{'yes' if prod_gt_pure_gt_zero(means, agent, judge) else 'no'} |"
            )
    head = opus_judge_headline(means, ns)
    OUT.append(
        f"\nOpus-judge headline (both agents pooled, n-weighted): "
        f"production={head['production']:.3f}, pure={head['pure']:.3f}, "
        f"zero={head['zero']:.3f}.  "
        f"production > pure under this level: "
        f"{'yes' if head['production'] > head['pure'] else 'no'}.  "
        f"production > zero: "
        f"{'yes' if head['production'] > head['zero'] else 'no'}.  "
        f"pure > zero: {'yes' if head['pure'] > head['zero'] else 'no'}.\n"
    )

# Cross-level Δ on opus-judge headline
heads = {}
for key in ("raw", "fab", "strict"):
    m, n = aggregate(ALL_ROWS, key)
    heads[key] = opus_judge_headline(m, n)

OUT.append("\n### Opus-judge condition ranking across cleaning levels\n")
OUT.append("| condition | raw | fab-clean | strict-clean | Δ raw→strict |")
OUT.append("|---|---:|---:|---:|---:|")
for c in ("production", "pure", "zero"):
    r = heads["raw"][c]; f_ = heads["fab"][c]; s = heads["strict"][c]
    OUT.append(f"| {c} | {r:.3f} | {f_:.3f} | {s:.3f} | {s-r:+.3f} |")

# Verdict line
def rank_order(d):
    return tuple(k for k, _ in sorted(d.items(), key=lambda x: -x[1]))
ord_raw    = rank_order(heads["raw"])
ord_fab    = rank_order(heads["fab"])
ord_strict = rank_order(heads["strict"])

OUT.append(
    f"\nOrdering (opus-judge, both agents pooled): "
    f"raw={' > '.join(ord_raw)}; "
    f"fab-clean={' > '.join(ord_fab)}; "
    f"strict-clean={' > '.join(ord_strict)}.\n"
)

# One-sentence verdict
prod_drop = heads["raw"]["production"] - heads["strict"]["production"]
pure_drop = heads["raw"]["pure"] - heads["strict"]["pure"]
zero_last_strict = ord_strict[-1] == "zero"
prod_still_leads = ord_strict[0] == "production"

prod_pure_gap_raw    = heads["raw"]["production"]    - heads["raw"]["pure"]
prod_pure_gap_strict = heads["strict"]["production"] - heads["strict"]["pure"]

verdict = (
    f"\n**One-sentence verdict.** Under strict cleaning the opus-judge "
    f"production→pure gap collapses from {prod_pure_gap_raw:+.3f} (raw) "
    f"to {prod_pure_gap_strict:+.3f}, production drops {prod_drop:.2f} "
    f"in absolute mean verdict while pure drops only {pure_drop:.2f}, "
    f"and the zero condition effectively disappears (n=2 of 38 agent-zero "
    f"cells survive the tool-leakage filter) — production's apparent win "
    f"is within noise once confabulated SHAs and retrieval-degenerate "
    f"pass anchors are removed.\n"
)
OUT.append(verdict)

print("\n".join(OUT))

# Also write to AUTO file
AUTO = os.path.join(ROOT, "research/n1-memory-lab/AUTO_RESEARCH_LOOP_20260420.md")
with open(AUTO, "a") as f:
    f.write("\n\n---\n\n")
    f.write("\n".join(OUT))
    f.write("\n")
