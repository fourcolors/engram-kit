"""
Revise sigma_eps for the GPT judge using the fresh Apr 21 heavy-intrarater reps.

Previously we only had Opus intra-rater reps cleanly; the GPT intra-rater numbers
were confounded by a gpt-5.4 vs gpt-5.4-mini model-mix (retracted Apr 20).

This script computes, on the clean gpt-5.4 reps against the same canonical answers:
  - verdict flip rate across 4 judge reps (original + 3 heavy reps)
  - σ_ε^cell (cell-wise ordinal pstdev on 0–2)
  - σ_ε^pooled (pooled raw SD across verdicts)
  - Full-band vs adjacent-band flip breakdown
  - Per-probe, per-condition flip counts
  - Binary useful-vs-fail κ across reps

All outputs printed as plain text + dumped as JSON for the HTML field report.
"""
from __future__ import annotations
import json
import math
from pathlib import Path
from collections import Counter, defaultdict
from statistics import pstdev

BASE = Path("/Users/saxenauts/Documents/personal/syke-replay-lab/runs")
RUNS = [
    ("original", "ne13-real-15d-gpt54-final-20260420T071500Z"),
    ("rep1",     "ne13-15d-gpt54heavy-intrarater-rep1-20260421T185347Z"),
    ("rep2",     "ne13-15d-gpt54heavy-intrarater-rep2-20260421T185347Z"),
    ("rep3",     "ne13-15d-gpt54heavy-intrarater-rep3-20260421T185347Z"),
]

SCORE = {"fail": 0, "partial": 1, "pass": 2}


def load(run_dir: Path) -> dict[tuple[str, str], str]:
    """Return (probe_id, condition) -> verdict for a run."""
    p = run_dir / "results.json"
    out = {}
    for item in json.loads(p.read_text()):
        verdict = item.get("verdict") or item.get("judge_result", {}).get("overall_verdict")
        if verdict in ("pass", "partial", "fail"):
            out[(item["probe_id"], item["condition"])] = verdict
    return out


def main() -> None:
    rep_data = {label: load(BASE / run) for label, run in RUNS}

    # Restrict to cells valid in ALL 4 reps
    common = set.intersection(*[set(d.keys()) for d in rep_data.values()])
    total_cells = len(common)
    print(f"Cells valid across all 4 reps: {total_cells}/57")
    print()

    # Per-cell: list of 4 verdicts
    per_cell_verdicts = {
        cell: [rep_data[label][cell] for label, _ in RUNS]
        for cell in sorted(common)
    }

    # Flip analysis
    all_same = 0
    any_flip = 0
    adjacent_flip_cells = 0
    full_band_flip_cells = 0
    per_cell_sigma_sq = []
    pooled_scores = []
    for cell, verdicts in per_cell_verdicts.items():
        scores = [SCORE[v] for v in verdicts]
        pooled_scores.extend(scores)
        if len(set(verdicts)) == 1:
            all_same += 1
        else:
            any_flip += 1
            if max(scores) - min(scores) >= 2:
                full_band_flip_cells += 1
            else:
                adjacent_flip_cells += 1
        per_cell_sigma_sq.append(pstdev(scores))

    sigma_eps_cell = sum(per_cell_sigma_sq) / len(per_cell_sigma_sq)
    sigma_eps_pooled = pstdev(pooled_scores)

    print(f"All-same across 4 reps:    {all_same}/{total_cells} ({100*all_same/total_cells:.1f}%)")
    print(f"Any flip across 4 reps:    {any_flip}/{total_cells} ({100*any_flip/total_cells:.1f}%)")
    print(f"  adjacent-band flips:      {adjacent_flip_cells}")
    print(f"  full-band (pass↔fail):    {full_band_flip_cells}")
    print()
    print(f"σ_ε^cell   (mean per-cell pstdev, 0–2): {sigma_eps_cell:.4f}")
    print(f"σ_ε^pooled (pooled raw SD, 0–2):        {sigma_eps_pooled:.4f}")
    print()

    # Binary useful = pass ∪ partial vs fail
    def to_bin(v: str) -> int:
        return 1 if v in ("pass", "partial") else 0

    bin_same = 0
    bin_flip = 0
    bin_sigma_sq = []
    bin_pool = []
    for verdicts in per_cell_verdicts.values():
        b = [to_bin(v) for v in verdicts]
        bin_pool.extend(b)
        if len(set(b)) == 1:
            bin_same += 1
        else:
            bin_flip += 1
        bin_sigma_sq.append(pstdev(b))
    print(f"Binary useful-vs-fail same across 4:    {bin_same}/{total_cells} ({100*bin_same/total_cells:.1f}%)")
    print(f"Binary flip cells:                      {bin_flip}/{total_cells}")
    print(f"σ_ε^collapsed (cell-wise binary pstdev): {sum(bin_sigma_sq)/len(bin_sigma_sq):.4f}")
    print()

    # Pairwise exact agreement (how often does pair of reps agree on same cell)
    import itertools
    rep_labels = [lbl for lbl, _ in RUNS]
    print("Pairwise exact agreement (3-level):")
    for a, b in itertools.combinations(rep_labels, 2):
        agree = sum(1 for cell in common if rep_data[a][cell] == rep_data[b][cell])
        print(f"  {a:10s} vs {b:10s}: {agree}/{total_cells} = {100*agree/total_cells:.1f}%")
    print()

    # Pairwise weighted kappa, 3-level ordinal (linear weighting)
    def weighted_kappa_linear(pairs):
        """Linear weighted kappa for 0-1-2 ordinal scale."""
        if not pairs:
            return None
        cats = [0, 1, 2]
        n = len(pairs)
        marg_a = Counter(a for a, _ in pairs)
        marg_b = Counter(b for _, b in pairs)

        w = lambda i, j: 1 - abs(i - j) / 2
        p_obs = sum(w(a, b) for a, b in pairs) / n
        p_exp = sum(
            (marg_a[i] / n) * (marg_b[j] / n) * w(i, j)
            for i in cats for j in cats
        )
        if p_exp >= 1:
            return None
        return (p_obs - p_exp) / (1 - p_exp)

    print("Pairwise weighted κ (linear, 3-level):")
    kappa_values = []
    for a, b in itertools.combinations(rep_labels, 2):
        pairs = [(SCORE[rep_data[a][cell]], SCORE[rep_data[b][cell]]) for cell in common]
        k = weighted_kappa_linear(pairs)
        kappa_values.append(k)
        print(f"  {a:10s} vs {b:10s}: κ = {k:.4f}")
    print(f"  mean pairwise weighted κ: {sum(kappa_values)/len(kappa_values):.4f}")
    print()

    # Per-probe flip rate — which probes are most unstable for gpt-5.4 judge
    probe_flips = defaultdict(list)
    for (probe, cond), verdicts in per_cell_verdicts.items():
        probe_flips[probe].append(len(set(verdicts)) > 1)
    print("Per-probe flip rate (across 3 conditions × 4 reps):")
    for probe in sorted(probe_flips):
        flips = probe_flips[probe]
        rate = sum(flips) / len(flips)
        marker = " ←" if rate == 1.0 else ""
        print(f"  {probe}: {sum(flips)}/{len(flips)} cells flip  ({100*rate:.0f}%){marker}")
    print()

    # Per-condition flip rate
    cond_flips = defaultdict(list)
    for (probe, cond), verdicts in per_cell_verdicts.items():
        cond_flips[cond].append(len(set(verdicts)) > 1)
    print("Per-condition flip rate:")
    for cond in ["production", "pure", "zero"]:
        flips = cond_flips[cond]
        print(f"  {cond:11s}: {sum(flips)}/{len(flips)} = {100*sum(flips)/len(flips):.1f}%")
    print()

    # Build the JSON dump
    dump = {
        "source": {
            "reps": [run for _, run in RUNS],
            "judge_model": "gpt-5.4 (NOT gpt-5.4-mini)",
            "computed_on": "2026-04-21",
            "note": "Clean GPT intra-rater set. Supersedes the retracted Apr 20 GPT intra-rater (gpt-5.4 baseline vs gpt-5.4-mini rerun).",
        },
        "cells_common": total_cells,
        "flip_structure": {
            "all_same": all_same,
            "any_flip": any_flip,
            "adjacent_band": adjacent_flip_cells,
            "full_band": full_band_flip_cells,
        },
        "sigma_eps_3level": {
            "cell_wise_pstdev": round(sigma_eps_cell, 4),
            "pooled_raw_sd": round(sigma_eps_pooled, 4),
        },
        "binary_useful_vs_fail": {
            "same_cells": bin_same,
            "flip_cells": bin_flip,
            "sigma_eps_collapsed": round(sum(bin_sigma_sq)/len(bin_sigma_sq), 4),
        },
        "pairwise_kappa_weighted": {
            f"{a}__{b}": round(weighted_kappa_linear(
                [(SCORE[rep_data[a][cell]], SCORE[rep_data[b][cell]]) for cell in common]
            ), 4)
            for a, b in itertools.combinations(rep_labels, 2)
        },
        "per_probe_always_flip": [p for p, f in probe_flips.items() if all(f)],
        "per_condition_flip_rate": {
            cond: round(sum(cond_flips[cond])/len(cond_flips[cond]), 4)
            for cond in ["production", "pure", "zero"]
        },
    }

    out_path = Path("/Users/saxenauts/Documents/personal/syke-replay-lab/research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_sigma_eps_gpt_heavy_clean.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(dump, indent=2))
    print(f"Dumped: {out_path}")


if __name__ == "__main__":
    main()
