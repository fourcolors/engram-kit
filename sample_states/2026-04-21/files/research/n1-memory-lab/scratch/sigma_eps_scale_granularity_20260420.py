#!/usr/bin/env python3
"""Scale-granularity sanity: does changing verdict scale reduce sigma_eps?

Uses the 4 opus intra-rater reps (baseline + rep1 + rep2 + rep3).
Only considers cells with 4 valid verdicts in {fail, partial, pass}.

Simulations:
  S0 (reference): 3-point overall verdict, normalized to [0,1]
  S1 (binary pass):     v=1 if pass else 0
  S2 (useful):          v=1 if pass or partial, 0 if fail
  S3 (5-point, sub-axis sum): 0..24 from summed sub-axis scores, binned to 0..4 -> /4
  S4 (sub-axis median): median of 12 sub-axis scores in {0,1,2}, normalized /2

For each simulation:
  - sigma_eps = mean over cells of std across 4 reps (sample std, ddof=0)
  - kappa    = Cohen's kappa on pairwise rep comparisons (pooled across
               all C(4,2)=6 pairs and all cells). For continuous scales
               (S3 sum, S4 median), kappa is computed on the ordinal level
               values present (0..4 for S3, 0..2 for S4). S1,S2 are 0/1.
  - % zero-variance cells: fraction where all 4 reps give identical value

Stdlib only.
"""

import json
import os
import math
from statistics import median

ROOT = "/Users/saxenauts/Documents/personal/syke-replay-lab"
RUNS = [
    ("baseline", f"{ROOT}/runs/ne13-real-15d-opus46-final-20260420T071500Z"),
    ("rep1",     f"{ROOT}/runs/ne13-real-15d-opusask-opusjudge-intrarater-20260420T200314Z"),
    ("rep2",     f"{ROOT}/runs/ne13-real-15d-opus46-intrarater-rep2-20260420T222645Z"),
    ("rep3",     f"{ROOT}/runs/ne13-real-15d-opus46-intrarater-rep3-20260420T222645Z"),
]

VERDICT_ORD = {"fail": 0, "partial": 1, "pass": 2}
# Sub-axis vocab in this corpus is strong/partial/missed; keep "hit" as alias-safe.
SUB_ORD = {"missed": 0, "partial": 1, "strong": 2, "hit": 2}
AXES = ["factual_grounding", "continuity", "coherence"]


def load_run(path):
    with open(os.path.join(path, "results.json")) as f:
        rows = json.load(f)
    return {(r["probe_id"], r["condition"]): r for r in rows}


def subaxis_scores(jr):
    """List of 12 sub-axis ordinals (0/1/2). Returns None if missing/short."""
    if not isinstance(jr, dict):
        return None
    vals = []
    for ax in AXES:
        node = jr.get(ax)
        if not isinstance(node, dict):
            return None
        subs = node.get("subcategories") or {}
        for sk, sv in subs.items():
            if isinstance(sv, dict):
                s = sv.get("score")
                if s not in SUB_ORD:
                    return None
                vals.append(SUB_ORD[s])
    if not vals:
        return None
    return vals


def std_pop(xs):
    n = len(xs)
    if n == 0:
        return 0.0
    mu = sum(xs) / n
    return math.sqrt(sum((x - mu) ** 2 for x in xs) / n)


def cohen_kappa_pairs(pair_vals):
    """pair_vals: list of (a,b) tuples of discrete labels. Cohen's kappa."""
    if not pair_vals:
        return float("nan")
    labels = sorted({v for ab in pair_vals for v in ab})
    n = len(pair_vals)
    # agreement
    agree = sum(1 for a, b in pair_vals if a == b) / n
    # marginals (pooled over both slots)
    total_slots = 2 * n
    counts = {}
    for a, b in pair_vals:
        counts[a] = counts.get(a, 0) + 1
        counts[b] = counts.get(b, 0) + 1
    pe = sum((counts[lab] / total_slots) ** 2 for lab in labels)
    if pe >= 1.0:
        return 1.0 if agree >= 1.0 else 0.0
    return (agree - pe) / (1 - pe)


def bin_sum(total, n_bins=5, lo=0, hi=24):
    """Map integer in [lo,hi] to bin 0..n_bins-1."""
    # equal-width bins
    width = (hi - lo + 1) / n_bins
    b = int((total - lo) / width)
    if b >= n_bins:
        b = n_bins - 1
    if b < 0:
        b = 0
    return b


def main():
    runs = [(tag, load_run(p)) for tag, p in RUNS]

    # Cells present in all 4 with valid verdict and valid 12 sub-axes
    keys = sorted(runs[0][1].keys())
    cells = []
    for key in keys:
        verdicts = []
        subs_per_rep = []
        ok = True
        for _, run in runs:
            r = run.get(key)
            if r is None:
                ok = False
                break
            v = r.get("verdict")
            if v not in VERDICT_ORD:
                ok = False
                break
            subs = subaxis_scores(r.get("judge_result"))
            if subs is None or len(subs) != 12:
                ok = False
                break
            verdicts.append(v)
            subs_per_rep.append(subs)
        if not ok:
            continue
        cells.append({
            "key": key,
            "verdicts": verdicts,
            "subs": subs_per_rep,
        })

    n = len(cells)
    print(f"n cells with 4 valid reps and 12 sub-axes: {n}")

    # Build scaled vectors per simulation
    sims = {}

    # S0: 3-point verdict / 2 in [0,1]
    s0 = [[VERDICT_ORD[v] / 2.0 for v in c["verdicts"]] for c in cells]
    sims["S0_overall3pt"] = {
        "reps": s0,
        "discrete": [[VERDICT_ORD[v] for v in c["verdicts"]] for c in cells],
    }

    # S1: binary pass-vs-not
    s1 = [[1 if v == "pass" else 0 for v in c["verdicts"]] for c in cells]
    sims["S1_binary_pass"] = {"reps": s1, "discrete": s1}

    # S2: useful (pass or partial) vs fail
    s2 = [[1 if v in ("pass", "partial") else 0 for v in c["verdicts"]] for c in cells]
    sims["S2_useful"] = {"reps": s2, "discrete": s2}

    # S3: sub-axis sum binned to 5-point
    s3_cont = [[sum(subs) / 24.0 for subs in c["subs"]] for c in cells]
    s3_bin = [[bin_sum(sum(subs), n_bins=5, lo=0, hi=24) for subs in c["subs"]] for c in cells]
    # Normalize discrete bin to [0,1]: b/4
    s3_norm = [[b / 4.0 for b in row] for row in s3_bin]
    sims["S3_5pt_subaxis_sum"] = {"reps": s3_norm, "discrete": s3_bin}

    # S4: sub-axis median, normalized /2
    s4_disc = []
    s4_norm = []
    for c in cells:
        disc_row = []
        norm_row = []
        for subs in c["subs"]:
            m = median(subs)  # median of ints in {0,1,2}; may be 0.5/1.5
            disc_row.append(m)
            norm_row.append(m / 2.0)
        s4_disc.append(disc_row)
        s4_norm.append(norm_row)
    sims["S4_subaxis_median"] = {"reps": s4_norm, "discrete": s4_disc}

    # Compute per-sim metrics
    results = {}
    for name, d in sims.items():
        reps = d["reps"]          # floats in [0,1]
        disc = d["discrete"]      # discrete labels for kappa
        # sigma_eps: mean over cells of population std across 4 reps
        stds = [std_pop(r) for r in reps]
        sigma_eps = sum(stds) / len(stds)
        # zero-variance rate: all 4 reps identical on discrete scale
        zv = sum(1 for r in disc if len(set(r)) == 1) / len(disc)
        # kappa: pooled over all 6 pairs per cell
        pair_vals = []
        for row in disc:
            for i in range(4):
                for j in range(i + 1, 4):
                    pair_vals.append((row[i], row[j]))
        k = cohen_kappa_pairs(pair_vals)
        results[name] = {
            "sigma_eps": sigma_eps,
            "kappa": k,
            "zero_var": zv,
            "n_cells": len(reps),
        }

    print("\n--- results (normalized to [0,1] for sigma_eps) ---")
    hdr = f"{'scale':<28}{'sigma_eps':>11}{'kappa':>9}{'zero_var%':>12}{'n':>5}"
    print(hdr)
    for name, r in results.items():
        print(f"{name:<28}{r['sigma_eps']:>11.4f}{r['kappa']:>9.3f}{r['zero_var']*100:>11.1f}%{r['n_cells']:>5}")

    # Ranking by lowest sigma_eps
    print("\n--- ranking by sigma_eps (low=better) ---")
    ranked = sorted(results.items(), key=lambda kv: kv[1]["sigma_eps"])
    for i, (name, r) in enumerate(ranked, 1):
        print(f"  {i}. {name}: sigma_eps={r['sigma_eps']:.4f}")

    print("\n--- ranking by kappa (high=better) ---")
    rankedk = sorted(results.items(), key=lambda kv: -kv[1]["kappa"])
    for i, (name, r) in enumerate(rankedk, 1):
        print(f"  {i}. {name}: kappa={r['kappa']:.3f}")

    print("\n--- ranking by zero-variance (high=better) ---")
    rankedz = sorted(results.items(), key=lambda kv: -kv[1]["zero_var"])
    for i, (name, r) in enumerate(rankedz, 1):
        print(f"  {i}. {name}: zero_var={r['zero_var']*100:.1f}%")

    return results


if __name__ == "__main__":
    main()
