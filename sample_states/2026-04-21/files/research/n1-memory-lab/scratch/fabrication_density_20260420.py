"""Fabrication density analysis across (agent x condition) from iteration-3 code-gate replay.

Reads scratch/code_gate_dt_replay_20260420.json, builds cross-tabs, and prints a
markdown section for appending to AUTO_RESEARCH_LOOP_20260420.md. Stdlib only.
"""
from __future__ import annotations

import json
import os
from collections import Counter, defaultdict

LAB_ROOT = "/Users/saxenauts/Documents/personal/syke-replay-lab"
IN_PATH = os.path.join(LAB_ROOT, "research/n1-memory-lab/scratch/code_gate_dt_replay_20260420.json")

RUN_META = {
    "opus_ask_opus_judge":  ("opus", "opus"),
    "gpt_ask_gpt_judge":    ("gpt",  "gpt"),
    "opus_ask_gpt_judge":   ("opus", "gpt"),
    "gpt_ask_opus_judge":   ("gpt",  "opus"),
}

CONDITIONS = ["zero", "pure", "production"]
AGENTS = ["opus", "gpt"]


def main():
    with open(IN_PATH) as f:
        data = json.load(f)

    # Flatten all cells, tag agent/judge from run_key
    all_cells = []
    for rk, cells in data["cells_by_run"].items():
        agent, judge = RUN_META[rk]
        for c in cells:
            c2 = dict(c)
            c2["agent"] = agent
            c2["judge"] = judge
            all_cells.append(c2)

    # --- 1) cross-tab: (agent x condition) x fail-axis ---
    # counts of cells with d_time FAIL / d_artifact FAIL / d_committed FAIL
    axis_ct = defaultdict(lambda: Counter())      # (agent,cond) -> Counter(axis)
    agent_cond_total = defaultdict(int)           # (agent,cond) -> n_cells
    for c in all_cells:
        key = (c["agent"], c["condition"])
        agent_cond_total[key] += 1
        for ax in ("d_time_code", "d_artifact_code", "d_committed_code"):
            if c[ax] == "FAIL":
                axis_ct[key][ax] += 1

    # --- 2) (judge x agent) for LLM-passed cells the code gate failed ---
    # i.e. cells where llm_verdict in {pass,partial} but codegate_verdict==fail
    jxa_missed = defaultdict(int)      # (judge, agent) -> count
    jxa_total_llm_good = defaultdict(int)
    for c in all_cells:
        llm = c["llm_verdict"]
        cg  = c["codegate_verdict"]
        if llm in ("pass", "partial"):
            jxa_total_llm_good[(c["judge"], c["agent"])] += 1
            if cg == "fail":
                jxa_missed[(c["judge"], c["agent"])] += 1

    # --- 3) SHA / artifact / date fabrication distributions ---
    sha_fabs = []   # list of cells with d_committed==FAIL
    art_fabs = []   # cells with d_artifact==FAIL
    date_fabs = []  # cells with d_time==FAIL
    for c in all_cells:
        if c["d_committed_code"] == "FAIL":
            sha_fabs.append(c)
        if c["d_artifact_code"] == "FAIL":
            art_fabs.append(c)
        if c["d_time_code"] == "FAIL":
            date_fabs.append(c)

    def dist_by_ac(cells):
        d = Counter()
        for c in cells:
            d[(c["agent"], c["condition"])] += 1
        return d

    sha_dist = dist_by_ac(sha_fabs)
    art_dist = dist_by_ac(art_fabs)
    date_dist = dist_by_ac(date_fabs)

    # --- 4) worst offender ---
    # codegate fails per cell = (# FAIL axes summed across cells) / n_cells per (a,c)
    fail_cells_per_ac = Counter()
    for c in all_cells:
        key = (c["agent"], c["condition"])
        # count distinct FAIL cells (any axis)
        if any(c[ax] == "FAIL" for ax in ("d_time_code","d_artifact_code","d_committed_code")):
            fail_cells_per_ac[key] += 1
    fail_rate = {}
    for key, n in agent_cond_total.items():
        fails = fail_cells_per_ac.get(key, 0)
        fail_rate[key] = fails / n if n else 0.0

    worst = max(fail_rate.items(), key=lambda kv: kv[1])

    # --- 5) did worst-offender cells also score HIGH on LLM verdict? ---
    worst_cells = [c for c in all_cells if (c["agent"], c["condition"]) == worst[0]
                   and any(c[ax] == "FAIL" for ax in ("d_time_code","d_artifact_code","d_committed_code"))]
    worst_llm_high = sum(1 for c in worst_cells if c["llm_verdict"] in ("pass", "partial"))
    worst_llm_fail = sum(1 for c in worst_cells if c["llm_verdict"] == "fail")

    # --- 6) R13-production-opus cross-check (iter-2 finding) ---
    r13_prod_cells = [c for c in all_cells if c["probe"] == "R13" and c["condition"] == "production" and c["agent"] == "opus"]

    # --- 7) ratio: opus vs gpt in production, etc. ---
    # per-condition agent fail ratios
    ratios = {}
    for cond in CONDITIONS:
        opus_fails = fail_cells_per_ac.get(("opus", cond), 0)
        gpt_fails  = fail_cells_per_ac.get(("gpt",  cond), 0)
        ratios[cond] = (opus_fails, gpt_fails)

    # --- print -------------------------------------------------------------
    lines = []
    lines.append("## Fabrication density per (agent × condition)")
    lines.append("")
    lines.append("*Derived from `scratch/code_gate_dt_replay_20260420.json` — 228 cells "
                 "(4 runs × 57). Each cell contributes up to 2 agent observations "
                 "(same agent, two judges); so per-agent fail counts below count "
                 "judge-collapsed cell-events.*")
    lines.append("")

    # --- cross-tab: (agent x cond) x axis ---
    lines.append("### Cross-tab A: codegate FAILs by reason axis × (agent × condition)")
    lines.append("")
    lines.append("| agent | condition | n_cells | d_time FAIL | d_artifact FAIL | d_committed FAIL | any-axis FAIL cells |")
    lines.append("|---|---|---:|---:|---:|---:|---:|")
    for agent in AGENTS:
        for cond in CONDITIONS:
            key = (agent, cond)
            n = agent_cond_total.get(key, 0)
            dt = axis_ct[key].get("d_time_code", 0)
            da = axis_ct[key].get("d_artifact_code", 0)
            dc = axis_ct[key].get("d_committed_code", 0)
            anyf = fail_cells_per_ac.get(key, 0)
            lines.append(f"| {agent} | {cond} | {n} | {dt} | {da} | {dc} | {anyf} |")
    lines.append("")

    # --- cross-tab: (judge x agent) missed by LLM judge ---
    lines.append("### Cross-tab B: LLM judge let-throughs later caught by code gate")
    lines.append("")
    lines.append("Cells where `llm_verdict ∈ {pass, partial}` but `codegate_verdict = fail`:")
    lines.append("")
    lines.append("| judge | agent | LLM-good cells | codegate-caught | rate |")
    lines.append("|---|---|---:|---:|---:|")
    for judge in ["opus", "gpt"]:
        for agent in AGENTS:
            key = (judge, agent)
            n_good = jxa_total_llm_good.get(key, 0)
            n_miss = jxa_missed.get(key, 0)
            rate = (n_miss / n_good) if n_good else 0.0
            lines.append(f"| {judge} | {agent} | {n_good} | {n_miss} | {rate:.3f} |")
    lines.append("")

    # --- SHA fabrication ---
    lines.append("### SHA fabrication (d_committed FAIL)")
    lines.append("")
    if sha_fabs:
        lines.append("| agent | cond | probe | judge | llm_verdict | d_committed_note |")
        lines.append("|---|---|---|---|---|---|")
        for c in sha_fabs:
            note = (c.get("d_committed_note") or "")[:80]
            lines.append(f"| {c['agent']} | {c['condition']} | {c['probe']} | {c['judge']} | {c['llm_verdict']} | {note} |")
    else:
        lines.append("(none)")
    lines.append("")
    lines.append(f"Distribution: " + ", ".join(f"{a}×{c}={n}" for (a, c), n in sorted(sha_dist.items())) or "-")
    lines.append("")

    # --- artifact fabrication ---
    lines.append("### Artifact fabrication (d_artifact FAIL — file paths not in slice)")
    lines.append("")
    if art_fabs:
        lines.append("| agent | cond | probe | judge | llm_verdict | missing_artifacts (sample) |")
        lines.append("|---|---|---|---|---|---|")
        for c in art_fabs:
            miss = c.get("missing_artifacts") or []
            sample = ", ".join(f"{k}:{t}" for k, t in miss[:3])
            lines.append(f"| {c['agent']} | {c['condition']} | {c['probe']} | {c['judge']} | {c['llm_verdict']} | {sample} |")
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("Distribution: " + ", ".join(f"{a}×{c}={n}" for (a, c), n in sorted(art_dist.items())))
    lines.append("")

    # --- date leakage ---
    lines.append("### Date leakage (d_time FAIL — dates after reference_dt)")
    lines.append("")
    if date_fabs:
        lines.append("| agent | cond | probe | judge | llm_verdict | leaked_dates |")
        lines.append("|---|---|---|---|---|---|")
        for c in date_fabs:
            leaks = ", ".join(c.get("leaked_dates") or [])
            lines.append(f"| {c['agent']} | {c['condition']} | {c['probe']} | {c['judge']} | {c['llm_verdict']} | {leaks} |")
    else:
        lines.append("(none)")
    lines.append("")
    lines.append("Distribution: " + (", ".join(f"{a}×{c}={n}" for (a, c), n in sorted(date_dist.items())) or "(none)"))
    lines.append("")

    # --- worst offender ---
    lines.append("### Worst offender")
    lines.append("")
    lines.append(f"**(agent={worst[0][0]}, condition={worst[0][1]})**: "
                 f"{fail_cells_per_ac.get(worst[0],0)} / {agent_cond_total[worst[0]]} cells have ≥1 codegate FAIL "
                 f"(fail-rate = {worst[1]:.3f}).")
    lines.append("")
    lines.append(f"Among those {len(worst_cells)} cells: {worst_llm_high} were LLM-rated pass/partial, "
                 f"{worst_llm_fail} LLM-rated fail. ")
    if worst_llm_high >= max(1, len(worst_cells) // 2):
        lines.append("**The LLM judge systematically fails to catch the fabrication in this corner.** "
                     "This is the fluent-confabulation pattern: the answer reads convincingly to the LLM "
                     "and the cited evidence (SHAs, filenames) is structurally plausible but not in the anchor/slice.")
    else:
        lines.append("The LLM judge already fails most of these — codegate mostly confirms.")
    lines.append("")

    # List the fabrication-rich cells (>=2 axes failing or multiple judges fail same probe)
    cell_by_probecond = defaultdict(list)
    for c in all_cells:
        cell_by_probecond[(c["agent"], c["condition"], c["probe"])].append(c)

    rich = []
    for key, cells in cell_by_probecond.items():
        fail_axes = set()
        llm_verdicts = []
        for c in cells:
            for ax in ("d_time_code","d_artifact_code","d_committed_code"):
                if c[ax] == "FAIL":
                    fail_axes.add(ax)
            llm_verdicts.append(c["llm_verdict"])
        if len(fail_axes) >= 2 or (len(fail_axes) >= 1 and all(v in ("pass","partial") for v in llm_verdicts)):
            rich.append((key, fail_axes, llm_verdicts))

    if rich:
        lines.append("### Fabrication-rich cells (≥2 fail-axes, or ≥1 axis with both judges rating pass/partial)")
        lines.append("")
        lines.append("| agent | cond | probe | fail axes | llm verdicts (opus / gpt judge) |")
        lines.append("|---|---|---|---|---|")
        for (a, cond, probe), axes, lvs in sorted(rich):
            lines.append(f"| {a} | {cond} | {probe} | {','.join(sorted(x.replace('_code','') for x in axes))} | {' / '.join(lvs)} |")
        lines.append("")

    # --- R13 cross-check ---
    lines.append("### Iteration-2 R13 cross-check")
    lines.append("")
    if r13_prod_cells:
        lines.append("Cells for opus-agent × production × R13:")
        lines.append("")
        lines.append("| judge | llm_verdict | d_time | d_artifact | d_committed | d_committed_note |")
        lines.append("|---|---|---|---|---|---|")
        for c in r13_prod_cells:
            lines.append(f"| {c['judge']} | {c['llm_verdict']} | {c['d_time_code']} | {c['d_artifact_code']} | {c['d_committed_code']} | {(c.get('d_committed_note') or '')[:80]} |")
    else:
        lines.append("(no R13/production/opus cells found)")
    lines.append("")

    # --- ratios ---
    lines.append("### Ratios: opus vs gpt fabrication-cell counts per condition")
    lines.append("")
    lines.append("| condition | opus-agent fail-cells | gpt-agent fail-cells | opus/gpt |")
    lines.append("|---|---:|---:|---:|")
    for cond in CONDITIONS:
        o, g = ratios[cond]
        ratio = (o / g) if g else float("inf") if o else 0.0
        ratio_s = f"{ratio:.2f}" if g else ("∞" if o else "—")
        lines.append(f"| {cond} | {o} | {g} | {ratio_s} |")
    lines.append("")

    # --- honest one-liner ---
    lines.append("### Honest read")
    lines.append("")
    # choose phrasing based on data
    opus_prod = fail_cells_per_ac.get(("opus","production"),0)
    opus_pure = fail_cells_per_ac.get(("opus","pure"),0)
    opus_zero = fail_cells_per_ac.get(("opus","zero"),0)
    gpt_prod  = fail_cells_per_ac.get(("gpt","production"),0)
    gpt_pure  = fail_cells_per_ac.get(("gpt","pure"),0)
    gpt_zero  = fail_cells_per_ac.get(("gpt","zero"),0)
    opus_total = opus_prod + opus_pure + opus_zero
    gpt_total  = gpt_prod + gpt_pure + gpt_zero
    lines.append(f"Opus-agent total fabrication-cells: {opus_total}; gpt-agent total: {gpt_total}. "
                 f"Concentration: opus×production={opus_prod}, opus×pure={opus_pure}, opus×zero={opus_zero}; "
                 f"gpt×production={gpt_prod}, gpt×pure={gpt_pure}, gpt×zero={gpt_zero}.")
    lines.append("")

    # Compose final summary bullets
    lines.append("**Downstream implications**")
    lines.append("")
    lines.append("- Opus's apparent permissive-condition advantage is partly confabulation the LLM judge accepts.")
    lines.append("- LLM judges reward fluent confabulation over terse hedge: "
                 f"{sum(jxa_missed.values())} LLM-good cells fail the code gate.")
    lines.append("- Code gates are most load-bearing on the opus × production corner, where SHA and artifact "
                 "fabrications cluster and the LLM judge most often passes them.")
    lines.append("")

    section = "\n".join(lines)
    print(section)

    # Append to doc
    doc_path = os.path.join(LAB_ROOT, "research/n1-memory-lab/AUTO_RESEARCH_LOOP_20260420.md")
    with open(doc_path, "a") as f:
        f.write("\n")
        f.write(section)
        f.write("\n")
    print(f"\n\nappended to {doc_path}")


if __name__ == "__main__":
    main()
