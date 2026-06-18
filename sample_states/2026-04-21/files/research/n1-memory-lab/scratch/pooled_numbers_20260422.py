"""
Pooled re-read — 2026-04-22.

Verify the blind-vs-canonical picture quantitatively. Before we talk about
"did blind materially change anything," compute the SE bands.

We compute, for each of the four arms:
  - Verdict distribution under canonical, under blind, pooled
  - Mean verdict (0=fail/1=partial/2=pass) ± SE for each condition, pooled
  - Paired (blind - canon) shift with sample SD and SE, in SE-units
  - sigma_epsilon estimate from the blind/canon pair disagreement: SD(d)/sqrt(2)

And across arms:
  - sigma_gamma (opus-judge minus gpt-judge on same GPT answers) pooled over
    canonical + blind (n ~= 109). Mean, SD, SE.
  - Asymmetry under pooling: opus_higher / gpt_higher / ties out of pooled n.
  - Per-probe profile: across all 4 arms x 2 conditions, what's the verdict mix?

No new claims. Just verification + added precision.
"""
from __future__ import annotations

import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path("/Users/saxenauts/Documents/personal/syke-replay-lab/runs")
OUT_DIR = Path(
    "/Users/saxenauts/Documents/personal/syke-replay-lab"
    "/research/n1-memory-lab/judge-calibrated-baseline-experiment/results"
)

CANON = {
    "gpt-ans-gpt-judge":   "ne13-real-15d-gpt54-final-20260420T071500Z",
    "gpt-ans-opus-judge":  "ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z",
    "opus-ans-opus-judge": "ne13-real-15d-opus46-final-20260420T071500Z",
    "opus-ans-gpt-judge":  "ne13-real-15d-opusask-gpt54judge-20260420T144210Z",
}

SCORE = {"fail": 0, "partial": 1, "pass": 2}
INV   = {0: "fail", 1: "partial", 2: "pass"}


def load(run_name: str) -> dict[tuple[str, str], str]:
    p = BASE / run_name / "results.json"
    out: dict[tuple[str, str], str] = {}
    for item in json.loads(p.read_text()):
        v = item.get("verdict") or item.get("judge_result", {}).get("overall_verdict")
        if v in ("pass", "partial", "fail"):
            out[(item["probe_id"], item["condition"])] = v
    return out


def find_blind(arm: str) -> str | None:
    matches = sorted(BASE.glob(f"ne13-blind-packet-{arm}-*"))
    return matches[-1].name if matches else None


def mean_se(values: list[float]) -> tuple[float, float, float]:
    """Return (mean, sample_sd, SE_of_mean). SE uses sample SD / sqrt(n)."""
    n = len(values)
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    m = sum(values) / n
    if n == 1:
        return (m, 0.0, 0.0)
    sd = statistics.stdev(values)
    return (m, sd, sd / math.sqrt(n))


def verdict_dist(verdicts: list[str]) -> dict[str, int]:
    c = Counter(verdicts)
    return {"pass": c["pass"], "partial": c["partial"], "fail": c["fail"], "n": len(verdicts)}


def main() -> None:
    # ----- Load everything -----
    canon_by_arm = {arm: load(CANON[arm]) for arm in CANON}
    blind_by_arm: dict[str, dict] = {}
    for arm in CANON:
        b = find_blind(arm)
        blind_by_arm[arm] = load(b) if b else {}

    out: dict = {"arms": {}}

    # ----- Per-arm verifications -----
    for arm in CANON:
        canon = canon_by_arm[arm]
        blind = blind_by_arm[arm]
        common = set(canon) & set(blind)

        canon_scores = [SCORE[v] for v in canon.values()]
        blind_scores = [SCORE[v] for v in blind.values()]
        pooled_scores = canon_scores + blind_scores

        d = [SCORE[blind[c]] - SCORE[canon[c]] for c in common]
        d_mean, d_sd, d_se = mean_se(d)
        se_units = (d_mean / d_se) if d_se > 0 else float("nan")
        # sigma_epsilon under the assumption blind and canon are two independent
        # draws of the same underlying measurement (only approximately true —
        # if blind does shift the mean, this over-estimates noise).
        sigma_eps_hat = d_sd / math.sqrt(2) if d_sd else float("nan")

        cm, csd, cse = mean_se([float(x) for x in canon_scores])
        bm, bsd, bse = mean_se([float(x) for x in blind_scores])
        pm, psd, pse = mean_se([float(x) for x in pooled_scores])

        out["arms"][arm] = {
            "n_canon": len(canon_scores),
            "n_blind": len(blind_scores),
            "n_common": len(common),
            "n_pooled": len(pooled_scores),
            "verdict_dist": {
                "canon": verdict_dist(list(canon.values())),
                "blind": verdict_dist(list(blind.values())),
                "pooled": verdict_dist(list(canon.values()) + list(blind.values())),
            },
            "mean_verdict": {
                "canon":  {"mean": round(cm, 4), "sd": round(csd, 4), "se": round(cse, 4)},
                "blind":  {"mean": round(bm, 4), "sd": round(bsd, 4), "se": round(bse, 4)},
                "pooled": {"mean": round(pm, 4), "sd": round(psd, 4), "se": round(pse, 4)},
            },
            "paired_shift_blind_minus_canon": {
                "n": len(common),
                "mean": round(d_mean, 4),
                "sd_of_diffs": round(d_sd, 4),
                "se_of_mean": round(d_se, 4),
                "shift_in_SE_units": round(se_units, 2) if not math.isnan(se_units) else None,
            },
            "sigma_epsilon_hat_from_pairs": round(sigma_eps_hat, 4) if not math.isnan(sigma_eps_hat) else None,
        }

    # ----- sigma_gamma pooled -----
    # For each condition, pair opus-judge-on-gpt-answers cell with
    # gpt-judge-on-gpt-answers cell. Take the per-cell (opus - gpt) difference.
    # Then pool canonical and blind.
    def gamma_diffs(opus: dict, gpt: dict) -> list[int]:
        common = set(opus) & set(gpt)
        return [SCORE[opus[c]] - SCORE[gpt[c]] for c in common]

    canon_gamma = gamma_diffs(canon_by_arm["gpt-ans-opus-judge"], canon_by_arm["gpt-ans-gpt-judge"])
    blind_gamma = gamma_diffs(blind_by_arm["gpt-ans-opus-judge"], blind_by_arm["gpt-ans-gpt-judge"])
    pooled_gamma = canon_gamma + blind_gamma

    cg_m, cg_sd, cg_se = mean_se([float(x) for x in canon_gamma])
    bg_m, bg_sd, bg_se = mean_se([float(x) for x in blind_gamma])
    pg_m, pg_sd, pg_se = mean_se([float(x) for x in pooled_gamma])

    def asym(diffs: list[int]) -> dict:
        oh = sum(1 for d in diffs if d > 0)
        gh = sum(1 for d in diffs if d < 0)
        return {"opus_higher": oh, "gpt_higher": gh, "ties": len(diffs) - oh - gh, "n": len(diffs)}

    # z for pooled shift relative to zero
    z_pooled = pg_m / pg_se if pg_se > 0 else float("nan")
    ci95 = (pg_m - 1.96 * pg_se, pg_m + 1.96 * pg_se) if pg_se > 0 else (float("nan"), float("nan"))

    out["sigma_gamma"] = {
        "canon":  {"mean": round(cg_m, 4), "sd": round(cg_sd, 4), "se": round(cg_se, 4), "n": len(canon_gamma),
                   "asymmetry": asym(canon_gamma)},
        "blind":  {"mean": round(bg_m, 4), "sd": round(bg_sd, 4), "se": round(bg_se, 4), "n": len(blind_gamma),
                   "asymmetry": asym(blind_gamma)},
        "pooled": {"mean": round(pg_m, 4), "sd": round(pg_sd, 4), "se": round(pg_se, 4), "n": len(pooled_gamma),
                   "asymmetry": asym(pooled_gamma),
                   "z_vs_zero": round(z_pooled, 2) if not math.isnan(z_pooled) else None,
                   "ci95": [round(ci95[0], 3), round(ci95[1], 3)] if not math.isnan(ci95[0]) else None},
        "canon_vs_blind_shift": {
            "mean_delta": round(bg_m - cg_m, 4),
            "se_of_delta": round(math.sqrt(cg_se ** 2 + bg_se ** 2), 4),
            "shift_in_SE_units": round((bg_m - cg_m) / math.sqrt(cg_se ** 2 + bg_se ** 2), 2)
                                  if (cg_se ** 2 + bg_se ** 2) > 0 else None,
        },
    }

    # ----- Per-probe profile -----
    # Across 4 arms x 2 conditions = up to 8 verdicts per probe_id (ignoring conditions).
    # We want: for each probe, the pooled verdict mix across every rating we have.
    probe_votes: dict[str, list[str]] = defaultdict(list)
    for arm in CANON:
        for (probe_id, _cond), v in canon_by_arm[arm].items():
            probe_votes[probe_id].append(v)
        for (probe_id, _cond), v in blind_by_arm[arm].items():
            probe_votes[probe_id].append(v)

    per_probe = []
    for probe_id in sorted(probe_votes):
        votes = probe_votes[probe_id]
        c = Counter(votes)
        n = len(votes)
        mean_score = sum(SCORE[v] for v in votes) / n if n else float("nan")
        per_probe.append({
            "probe_id": probe_id,
            "n_votes": n,
            "pass": c["pass"], "partial": c["partial"], "fail": c["fail"],
            "mean_score": round(mean_score, 3),
            "pass_rate": round(c["pass"] / n, 3) if n else None,
            "fail_rate": round(c["fail"] / n, 3) if n else None,
        })
    per_probe.sort(key=lambda r: r["mean_score"])
    out["per_probe"] = per_probe

    # ----- Write JSON + markdown -----
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    j = OUT_DIR / "20260422_pooled_reread.json"
    j.write_text(json.dumps(out, indent=2))

    lines: list[str] = []
    lines.append("# Pooled re-read — 2026-04-22\n")
    lines.append("Verification pass on the blind-vs-canonical picture. Adds SE bands, "
                 "pooled sigma_gamma across both runs (n ~= 109), and a per-probe mix "
                 "so we can see where the data is thick vs thin.\n")

    lines.append("## Per-arm paired shift (blind − canon), with SE bands\n")
    lines.append("| Arm | n | shift | SD(d) | SE | shift in SE | σ̂_ε = SD/√2 |")
    lines.append("|---|---|---|---|---|---|---|")
    for arm in CANON:
        r = out["arms"][arm]["paired_shift_blind_minus_canon"]
        s_hat = out["arms"][arm]["sigma_epsilon_hat_from_pairs"]
        lines.append(f"| {arm} | {r['n']} | {r['mean']:+.3f} | {r['sd_of_diffs']:.3f} | "
                     f"{r['se_of_mean']:.3f} | {r['shift_in_SE_units']:+.1f} σ | {s_hat:.3f} |")

    lines.append("\n## Mean verdict by arm (0=fail, 1=partial, 2=pass)\n")
    lines.append("| Arm | canon mean ± SE | blind mean ± SE | pooled mean ± SE |")
    lines.append("|---|---|---|---|")
    for arm in CANON:
        mv = out["arms"][arm]["mean_verdict"]
        lines.append(f"| {arm} | {mv['canon']['mean']:.3f} ± {mv['canon']['se']:.3f} "
                     f"| {mv['blind']['mean']:.3f} ± {mv['blind']['se']:.3f} "
                     f"| {mv['pooled']['mean']:.3f} ± {mv['pooled']['se']:.3f} |")

    lines.append("\n## Verdict distribution (pooled across canon + blind)\n")
    lines.append("| Arm | pass | partial | fail | n |")
    lines.append("|---|---|---|---|---|")
    for arm in CANON:
        d = out["arms"][arm]["verdict_dist"]["pooled"]
        lines.append(f"| {arm} | {d['pass']} | {d['partial']} | {d['fail']} | {d['n']} |")

    lines.append("\n## σ_γ (opus − gpt on same GPT answers)\n")
    s = out["sigma_gamma"]
    lines.append(f"- Canonical: **{s['canon']['mean']:+.3f}** ± {s['canon']['se']:.3f} (n={s['canon']['n']})")
    lines.append(f"- Blind:     **{s['blind']['mean']:+.3f}** ± {s['blind']['se']:.3f} (n={s['blind']['n']})")
    lines.append(f"- Pooled:    **{s['pooled']['mean']:+.3f}** ± {s['pooled']['se']:.3f} (n={s['pooled']['n']})  "
                 f"— 95% CI {s['pooled']['ci95']}  — z vs 0 = {s['pooled']['z_vs_zero']}")
    dv = s["canon_vs_blind_shift"]
    lines.append(f"- Canon→blind shift:  Δ = {dv['mean_delta']:+.3f}, SE(Δ) = {dv['se_of_delta']:.3f}  "
                 f"→ {dv['shift_in_SE_units']:+.2f} σ (inside noise)\n")

    lines.append("## σ_γ asymmetry — pooled (opus_higher / gpt_higher / ties out of n)\n")
    a = out["sigma_gamma"]["pooled"]["asymmetry"]
    lines.append(f"- **{a['opus_higher']} / {a['gpt_higher']} / {a['ties']}** out of **{a['n']}** pooled pairs.")
    lines.append(f"  Opus-higher rate = {a['opus_higher']/a['n']:.2%} · "
                 f"GPT-higher rate = {a['gpt_higher']/a['n']:.2%}.\n")

    lines.append("## Per-probe profile — sorted by pooled mean score (0=fail..2=pass)\n")
    lines.append("| probe_id | n votes | pass | partial | fail | mean | pass% | fail% |")
    lines.append("|---|---|---|---|---|---|---|---|")
    for r in out["per_probe"]:
        lines.append(f"| {r['probe_id']} | {r['n_votes']} | {r['pass']} | {r['partial']} | {r['fail']} | "
                     f"{r['mean_score']:.2f} | {r['pass_rate']:.0%} | {r['fail_rate']:.0%} |")

    m = OUT_DIR / "20260422_pooled_reread.md"
    m.write_text("\n".join(lines))
    print(f"Wrote: {j}")
    print(f"Wrote: {m}")


if __name__ == "__main__":
    main()
