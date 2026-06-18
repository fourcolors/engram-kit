#!/usr/bin/env python3
"""σ_ε × fabrication correlation analysis. Stdlib only."""
import json
import math

# --- 19 σ_ε flipped (probe, condition) cells from iteration 1 (opus intra-rater, opus-agent answers)
sigma_eps_flipped = [
    ("R04", "production"),
    ("R11", "production"),
    ("R12", "production"),
    ("R14", "production"),
    ("R15", "production"),
    ("R01", "pure"),
    ("R03", "pure"),
    ("R04", "pure"),
    ("R06", "pure"),
    ("R07", "pure"),
    ("R08", "pure"),
    ("R15", "pure"),
    ("R18", "pure"),
    ("R03", "zero"),
    ("R07", "zero"),
    ("R11", "zero"),
    ("R12", "zero"),
    ("R14", "zero"),
    ("R19", "zero"),
]
assert len(sigma_eps_flipped) == 19

# --- Load code-gate JSON and extract opus-agent cells where codegate flipped to FAIL
with open("/Users/saxenauts/Documents/personal/syke-replay-lab/research/n1-memory-lab/scratch/code_gate_dt_replay_20260420.json") as f:
    cg = json.load(f)

# opus-agent runs: opus_ask_opus_judge, opus_ask_gpt_judge
opus_runs = ["opus_ask_opus_judge", "opus_ask_gpt_judge"]

# A code-gate "flip" is a cell where codegate_verdict = 'fail' but llm_verdict was not already 'fail'.
# The summary reports flip_directions so we filter matching those.
codegate_flipped_opus = set()
codegate_flagged_all_opus = set()  # codegate_verdict == 'fail' for opus-agent regardless of LLM verdict
cells_seen_opus = set()  # the 57 cells (probe, condition) once (same cell appears in both runs)
per_run_flipped = {}

for run_key in opus_runs:
    flipped = set()
    for entry in cg["cells_by_run"][run_key]:
        p = entry["probe"]
        c = entry["condition"]
        cells_seen_opus.add((p, c))
        if entry["codegate_verdict"] == "fail":
            codegate_flagged_all_opus.add((p, c))
            if entry["llm_verdict"] != "fail":
                codegate_flipped_opus.add((p, c))
                flipped.add((p, c))
    per_run_flipped[run_key] = flipped

print("codegate flipped to FAIL by run (opus-agent):")
for k, v in per_run_flipped.items():
    print(f"  {k}: n={len(v)}  cells={sorted(v)}")
print(f"union of codegate-flipped cells on opus-agent: n={len(codegate_flipped_opus)}")
print(f"  cells: {sorted(codegate_flipped_opus)}")
print(f"total distinct (probe,condition) cells on opus-agent side: {len(cells_seen_opus)}")

# --- Universe for overlap: the 45 cells that had a 4-rep opus intra-rater verdict.
# We don't have that explicit list, but the 19 flipped + 26 identical = 45 cells on opus-agent.
# For the contingency, the universe must be the *same* set on both axes. Use the intersection of
# cells present in both the opus intra-rater 45 AND the codegate opus-agent cells.
# The opus intra-rater packet uses opus-agent final run, so the 57 (probe,condition) cells in
# cells_by_run should be a superset of the 45.
# We need the identical set. The log says 45 cells had a verdict in all 4 reps; 19 flipped, 26 identical.
# The identical cells are the 45 minus the 19 flipped.
# But we don't have the 26 identical list. Build it by enumerating the 57 cells and excluding the 12
# that had invalid/no-verdict in some rep.
# Safer: use the 45 universe reconstructed from 19 flipped + derived identical.
# From the log we don't have explicit identical cells. But we know 3 cells had invalid opus-judge
# output on gpt-agent — on opus-agent 0 were invalid. So the 45 cells = 57 - 12 cells that were
# missing in some rep. Without that list I'll use "cells present in codegate opus-agent" as the
# universe proxy (57 cells) and flag the inference accordingly.

universe = sorted(cells_seen_opus)  # 57 cells

# For the chi-square we need: σ_ε_flipped status (yes = 19, no = 45-19 = 26 on the 45-cell subset,
# or 57-19 = 38 on the 57-cell superset) × codegate_flipped status.
# The codegate check is well-defined on all 57 cells. The σ_ε check is only defined on 45 cells (the
# ones that had a verdict in all 4 reps). Use the 45-cell universe: σ_ε flipped (19) vs σ_ε identical
# (26). To determine which of the 57 cells are in the "identical" 26, we need the cells that had a
# 4-rep verdict. Not in log. Assume the 12 invalid/missing-rep cells are NOT in the 19 flipped (they
# can't be flipped if a rep is missing). So the 12 invalid cells are drawn from the 38 non-flipped
# cells of the 57. We'd have to exclude them. Since we lack their identities, we will report two
# contingencies: (a) strict on 45-cell universe with σ_ε_identical count = 26 — we compute codegate
# intersection assuming the 12 invalid cells are distributed the same way as the 38 non-flipped
# cells codegate-wise; (b) conservative on 57-cell universe.

# Best we can do cleanly: use the 57-cell universe, compute the 2×2 on (σ_ε_flipped, codegate_flipped).
# Note: σ_ε_identical bucket here includes the 12 cells with missing reps. This is a slight
# under-power but doesn't bias direction — missing-rep cells are as likely to be codegate-flagged as
# any other.

flipped_set = set(sigma_eps_flipped)
cg_set = codegate_flipped_opus

both = flipped_set & cg_set
only_sigma = flipped_set - cg_set
only_cg = cg_set - flipped_set
neither = set(universe) - flipped_set - cg_set

a = len(both)             # σ_ε flipped & codegate flipped
b = len(only_sigma)       # σ_ε flipped & not codegate flipped
c = len(only_cg)          # σ_ε identical & codegate flipped
d = len(neither)          # σ_ε identical & not codegate flipped

print()
print(f"2x2 contingency on 57-cell opus-agent universe:")
print(f"                  codegate_flag  no_codegate_flag   row_total")
print(f"  sigma_eps_flipped   {a:>4}          {b:>4}          {a+b:>4}")
print(f"  sigma_eps_identical {c:>4}          {d:>4}          {c+d:>4}")
print(f"  col_total           {a+c:>4}          {b+d:>4}          {a+b+c+d:>4}")

# Fisher's exact test (two-tailed) — stdlib only
from math import lgamma

def log_binom(n, k):
    if k < 0 or k > n: return -float("inf")
    return lgamma(n+1) - lgamma(k+1) - lgamma(n-k+1)

def hypergeom_pmf(k, K, N, n):
    # probability of exactly k successes in sample of n, when N total, K successes
    return math.exp(log_binom(K, k) + log_binom(N-K, n-k) - log_binom(N, n))

def fisher_two_tailed(a, b, c, d):
    N = a+b+c+d
    row1 = a+b
    col1 = a+c
    observed = hypergeom_pmf(a, col1, N, row1)
    total = 0.0
    # enumerate all k with same marginals
    k_min = max(0, row1 - (N - col1))
    k_max = min(row1, col1)
    for k in range(k_min, k_max+1):
        p = hypergeom_pmf(k, col1, N, row1)
        if p <= observed + 1e-12:
            total += p
    return total

def chi2_test(a, b, c, d):
    N = a+b+c+d
    row1, row2 = a+b, c+d
    col1, col2 = a+c, b+d
    ea = row1*col1/N; eb = row1*col2/N; ec = row2*col1/N; ed = row2*col2/N
    chi2 = 0.0
    for obs, exp in [(a,ea),(b,eb),(c,ec),(d,ed)]:
        if exp > 0: chi2 += (obs-exp)**2 / exp
    # p-value for chi2 with 1 df
    # chi2 ~ Gamma(1/2, 2); p = 1 - erf(sqrt(chi2/2))  (since chi2_1 = Z^2 with Z~N)
    p = math.erfc(math.sqrt(chi2/2))
    return chi2, p

p_fisher = fisher_two_tailed(a, b, c, d)
chi2, p_chi2 = chi2_test(a, b, c, d)
print(f"\nFisher exact two-tailed p = {p_fisher:.4f}")
print(f"Chi-square = {chi2:.3f}, p = {p_chi2:.4f}")

# Odds ratio
if b*c > 0:
    or_val = (a*d) / (b*c)
else:
    or_val = float('inf') if a*d > 0 else float('nan')
print(f"Odds ratio = {or_val:.3f}")

# Rate comparison
if (a+b) > 0:
    rate_flipped = a/(a+b)
else:
    rate_flipped = 0
if (c+d) > 0:
    rate_identical = c/(c+d)
else:
    rate_identical = 0
print(f"codegate-flag rate among σ_ε_flipped = {rate_flipped:.2%}")
print(f"codegate-flag rate among σ_ε_identical = {rate_identical:.2%}")

print("\nCells in overlap (σ_ε flipped AND codegate flipped):")
for x in sorted(both): print(f"  {x}")
print("\nCells σ_ε flipped BUT NOT codegate flipped:")
for x in sorted(only_sigma): print(f"  {x}")
print("\nCells codegate flipped BUT NOT σ_ε flipped:")
for x in sorted(only_cg): print(f"  {x}")

# R07, R08, R14 always-flip probes — check if any of their cells were codegate-flipped
always_flip = ["R07", "R08", "R14"]
print("\nAlways-flip probes × codegate flag:")
for p in always_flip:
    sigma_cells_for_p = [(pp,c) for (pp,c) in sigma_eps_flipped if pp == p]
    cg_cells_for_p = [(pp,c) for (pp,c) in cg_set if pp == p]
    print(f"  {p}: σ_ε-flipped cells = {sigma_cells_for_p}, codegate-flipped cells = {cg_cells_for_p}")

# Also check codegate_flagged_all_opus (not just flips, but any cell where codegate says fail)
# useful for "σ_ε-identical cells that codegate DID flag" semantics
print("\n---- broader view: codegate says FAIL (regardless of whether it flipped llm verdict) ----")
cg_any_fail = codegate_flagged_all_opus
overlap_any = flipped_set & cg_any_fail
print(f"codegate-fail cells on opus-agent (union across both runs): n={len(cg_any_fail)}")
print(f"  cells: {sorted(cg_any_fail)}")
print(f"overlap with σ_ε flipped: n={len(overlap_any)}")
print(f"  cells: {sorted(overlap_any)}")
