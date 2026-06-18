"""
Revise cross-judge kappa with clean gpt-5.4 (NOT gpt-5.4-mini).

Earlier we had:
  - +0.49 opus-over-gpt mean shift (clean arm: gpt-5.4 judge on GPT-agent answers)
  - -0.491 on the confounded arm (opus → gpt-5.4-mini on Opus-agent answers)

Now that we have clean gpt-5.4 heavy reps, we can compare against clean Opus reps
to get a clean same-answers cross-judge read.

Shared answer set: the Apr 20 canonical GPT-agent final run.
- GPT intra-rater reps (gpt-5.4): original + rep1 + rep2 + rep3
- Opus intra-rater reps: they judged a different answer set (Opus-agent answers)

So the cleanest comparison is the existing ne13-real-15d-gpt54ask-opusjudge cross run
vs the new gpt-heavy intra-rater reps — all judging the SAME GPT-agent answers,
but with different judges.
"""
from __future__ import annotations
import json
import itertools
from pathlib import Path
from collections import Counter
from statistics import pstdev

BASE = Path("/Users/saxenauts/Documents/personal/syke-replay-lab/runs")

# All reps judging the same Apr 20 gpt-agent answers:
GPT_ON_GPT = [
    ("gpt-orig",  "ne13-real-15d-gpt54-final-20260420T071500Z"),
    ("gpt-heavy-rep1",  "ne13-15d-gpt54heavy-intrarater-rep1-20260421T185347Z"),
    ("gpt-heavy-rep2",  "ne13-15d-gpt54heavy-intrarater-rep2-20260421T185347Z"),
    ("gpt-heavy-rep3",  "ne13-15d-gpt54heavy-intrarater-rep3-20260421T185347Z"),
]
OPUS_ON_GPT = [
    ("opus-cross", "ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z"),
]

SCORE = {"fail": 0, "partial": 1, "pass": 2}


def load(run_dir: Path) -> dict[tuple[str, str], str]:
    p = run_dir / "results.json"
    out = {}
    for item in json.loads(p.read_text()):
        verdict = item.get("verdict") or item.get("judge_result", {}).get("overall_verdict")
        if verdict in ("pass", "partial", "fail"):
            out[(item["probe_id"], item["condition"])] = verdict
    return out


def weighted_kappa(pairs, linear=True):
    if not pairs:
        return None
    cats = [0, 1, 2]
    n = len(pairs)
    marg_a = Counter(a for a, _ in pairs)
    marg_b = Counter(b for _, b in pairs)
    if linear:
        w = lambda i, j: 1 - abs(i - j) / 2
    else:
        w = lambda i, j: 1 - ((i - j) / 2) ** 2
    p_obs = sum(w(a, b) for a, b in pairs) / n
    p_exp = sum((marg_a[i] / n) * (marg_b[j] / n) * w(i, j)
                for i in cats for j in cats)
    return (p_obs - p_exp) / (1 - p_exp) if p_exp < 1 else None


def cohen_kappa(pairs):
    """Unweighted binary κ for useful-vs-fail."""
    if not pairs:
        return None
    n = len(pairs)
    p_obs = sum(1 for a, b in pairs if a == b) / n
    ma = Counter(a for a, _ in pairs)
    mb = Counter(b for _, b in pairs)
    p_exp = sum((ma[k] / n) * (mb[k] / n) for k in set(ma) | set(mb))
    return (p_obs - p_exp) / (1 - p_exp) if p_exp < 1 else None


def main() -> None:
    gpt_reps = {label: load(BASE / run) for label, run in GPT_ON_GPT}
    opus_reps = {label: load(BASE / run) for label, run in OPUS_ON_GPT}
    opus_data = opus_reps["opus-cross"]

    common = set(opus_data.keys())
    for d in gpt_reps.values():
        common &= set(d.keys())
    n = len(common)
    print(f"Cells common to all GPT reps + opus cross: {n}")
    print()

    # Compute cross-judge shift and κ, clean gpt-5.4 vs opus-4.6,
    # averaging across the 4 GPT reps so judge noise doesn't bias the γ estimate.
    print("CROSS-JUDGE (Opus judge on GPT-agent answers, compared against each clean gpt-5.4 rep)")
    print(f"  scale: 0=fail, 1=partial, 2=pass   shift = opus − gpt-rep")
    print()
    print(f"  {'vs':20s}  {'mean_shift':>10s}  {'w_kappa':>10s}  {'exact':>8s}  {'binary_exact':>12s}  {'binary_kappa':>12s}")

    shift_vals = []
    wk_vals = []
    for g_label in sorted(gpt_reps.keys()):
        gdata = gpt_reps[g_label]
        pairs_3 = [(SCORE[opus_data[c]], SCORE[gdata[c]]) for c in common]
        pairs_bin = [(1 if opus_data[c] != "fail" else 0, 1 if gdata[c] != "fail" else 0) for c in common]

        mean_shift = sum(a - b for a, b in pairs_3) / len(pairs_3)
        wk = weighted_kappa(pairs_3)
        exact = sum(1 for a, b in pairs_3 if a == b) / n
        bin_exact = sum(1 for a, b in pairs_bin if a == b) / n
        bin_k = cohen_kappa(pairs_bin)

        shift_vals.append(mean_shift)
        wk_vals.append(wk)
        print(f"  {g_label:20s}  {mean_shift:+10.4f}  {wk:10.4f}  {exact:8.4f}  {bin_exact:12.4f}  {bin_k:12.4f}")

    print()
    print(f"  mean clean-arm shift (opus - gpt-5.4, avg over 4 reps):  {sum(shift_vals)/len(shift_vals):+.4f}")
    print(f"  mean clean-arm weighted κ:                                {sum(wk_vals)/len(wk_vals):.4f}")
    print()

    # Verdict ordering — is opus systematically higher?
    opus_higher = sum(1 for c in common
                      if SCORE[opus_data[c]] > max(SCORE[gpt_reps[l][c]] for l in gpt_reps))
    gpt_higher = sum(1 for c in common
                      if min(SCORE[gpt_reps[l][c]] for l in gpt_reps) > SCORE[opus_data[c]])
    print(f"Cells where opus > every gpt-rep: {opus_higher}/{n}")
    print(f"Cells where every gpt-rep > opus: {gpt_higher}/{n}")
    print()

    dump = {
        "source": {
            "gpt_reps": [r for _, r in GPT_ON_GPT],
            "opus_run": OPUS_ON_GPT[0][1],
            "answer_set": "Apr 20 canonical gpt-agent final",
            "computed_on": "2026-04-21",
            "note": "Clean cross-judge read. Replaces the retracted gpt-5.4-mini-confounded arm.",
        },
        "common_cells": n,
        "per_rep_shift_opus_minus_gpt": {
            label: round(sum(SCORE[opus_data[c]] - SCORE[gpt_reps[label][c]] for c in common) / n, 4)
            for label in gpt_reps
        },
        "mean_clean_arm_shift_opus_minus_gpt54": round(sum(shift_vals)/len(shift_vals), 4),
        "per_rep_weighted_kappa": {
            label: round(weighted_kappa(
                [(SCORE[opus_data[c]], SCORE[gpt_reps[label][c]]) for c in common]
            ), 4)
            for label in gpt_reps
        },
        "mean_clean_arm_weighted_kappa": round(sum(wk_vals)/len(wk_vals), 4),
        "opus_strictly_higher_cells": opus_higher,
        "gpt_strictly_higher_cells": gpt_higher,
    }
    out = Path("/Users/saxenauts/Documents/personal/syke-replay-lab/research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_cross_judge_clean_gpt54.json")
    out.write_text(json.dumps(dump, indent=2))
    print(f"Dumped: {out}")


if __name__ == "__main__":
    main()
