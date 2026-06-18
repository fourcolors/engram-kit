"""
Compare blind-packet 4-arm rerun vs the Apr 20 canonical numbers.

Computes deltas on the headline quantities:
- Cross-judge σ_γ mean shift (blind vs non-blind)
- Cross-judge weighted κ
- Cross-judge binary exact / binary κ
- Verdict flip structure (how many cells shift pass↔partial, partial↔fail, pass↔fail)
- The 22/54 opus-strictly-higher asymmetry — does it hold under blind?

Writes results to:
  research/n1-memory-lab/judge-calibrated-baseline-experiment/results/
    20260421_blind_vs_canonical_deltas.json
    20260421_blind_vs_canonical_deltas.md

Expects all 4 blind-packet arms to exist under runs/ne13-blind-packet-*-<stamp>/.
"""
from __future__ import annotations
import json
import itertools
from pathlib import Path
from collections import Counter
from statistics import pstdev

BASE = Path("/Users/saxenauts/Documents/personal/syke-replay-lab/runs")

# Canonical (non-blind) source runs
CANON = {
    "gpt-ans-gpt-judge":   "ne13-real-15d-gpt54-final-20260420T071500Z",
    "gpt-ans-opus-judge":  "ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z",
    "opus-ans-opus-judge": "ne13-real-15d-opus46-final-20260420T071500Z",
    "opus-ans-gpt-judge":  "ne13-real-15d-opusask-gpt54judge-20260420T144210Z",
}

SCORE = {"fail": 0, "partial": 1, "pass": 2}


def load(run_name: str) -> dict[tuple[str, str], str]:
    p = BASE / run_name / "results.json"
    out = {}
    for item in json.loads(p.read_text()):
        v = item.get("verdict") or item.get("judge_result", {}).get("overall_verdict")
        if v in ("pass", "partial", "fail"):
            out[(item["probe_id"], item["condition"])] = v
    return out


def find_blind(arm: str) -> str | None:
    """Find the newest blind-packet run dir for an arm."""
    matches = sorted(BASE.glob(f"ne13-blind-packet-{arm}-*"))
    return matches[-1].name if matches else None


def weighted_kappa(pairs, linear=True):
    if not pairs:
        return None
    cats = [0, 1, 2]
    n = len(pairs)
    ma = Counter(a for a, _ in pairs)
    mb = Counter(b for _, b in pairs)
    w = (lambda i, j: 1 - abs(i - j) / 2) if linear else (lambda i, j: 1 - ((i - j) / 2) ** 2)
    p_obs = sum(w(a, b) for a, b in pairs) / n
    p_exp = sum((ma[i] / n) * (mb[j] / n) * w(i, j) for i in cats for j in cats)
    return (p_obs - p_exp) / (1 - p_exp) if p_exp < 1 else None


def cohen_kappa_binary(pairs):
    if not pairs:
        return None
    n = len(pairs)
    p_obs = sum(1 for a, b in pairs if a == b) / n
    ma = Counter(a for a, _ in pairs)
    mb = Counter(b for _, b in pairs)
    p_exp = sum((ma[k] / n) * (mb[k] / n) for k in set(ma) | set(mb))
    return (p_obs - p_exp) / (1 - p_exp) if p_exp < 1 else None


def main() -> None:
    results = {}

    for arm, canon_run in CANON.items():
        blind_run = find_blind(arm)
        if blind_run is None:
            print(f"[{arm}] no blind run found yet")
            results[arm] = {"status": "not_found"}
            continue
        try:
            canon = load(canon_run)
            blind = load(blind_run)
        except Exception as e:
            print(f"[{arm}] load error: {e}")
            results[arm] = {"status": "error", "error": str(e)}
            continue

        common = set(canon) & set(blind)
        n = len(common)
        if n == 0:
            print(f"[{arm}] zero common cells")
            results[arm] = {"status": "no_overlap"}
            continue

        # Paired verdict shift — blind vs canonical on same cells
        pairs_3 = [(SCORE[canon[c]], SCORE[blind[c]]) for c in common]
        pairs_bin = [(1 if canon[c] != "fail" else 0, 1 if blind[c] != "fail" else 0) for c in common]

        mean_shift = sum(b - a for a, b in pairs_3) / n  # positive = blind scored higher
        exact_3 = sum(1 for a, b in pairs_3 if a == b) / n
        wk = weighted_kappa(pairs_3)
        bin_exact = sum(1 for a, b in pairs_bin if a == b) / n
        bin_k = cohen_kappa_binary(pairs_bin)

        # Verdict flip taxonomy
        same = sum(1 for c in common if canon[c] == blind[c])
        pass_to_lower = sum(1 for c in common if canon[c] == "pass" and blind[c] != "pass")
        fail_to_higher = sum(1 for c in common if canon[c] == "fail" and blind[c] != "fail")
        partial_to_pass = sum(1 for c in common if canon[c] == "partial" and blind[c] == "pass")
        partial_to_fail = sum(1 for c in common if canon[c] == "partial" and blind[c] == "fail")
        full_band = sum(
            1 for c in common
            if (canon[c] == "pass" and blind[c] == "fail") or (canon[c] == "fail" and blind[c] == "pass")
        )

        results[arm] = {
            "status": "ok",
            "canon_run": canon_run,
            "blind_run": blind_run,
            "n_common": n,
            "mean_shift_blind_minus_canon": round(mean_shift, 4),
            "exact_agreement_3level": round(exact_3, 4),
            "weighted_kappa_3level": round(wk, 4) if wk is not None else None,
            "binary_exact": round(bin_exact, 4),
            "binary_kappa": round(bin_k, 4) if bin_k is not None else None,
            "flips": {
                "same": same,
                "any_flip": n - same,
                "full_band_pass_fail": full_band,
                "pass_to_lower": pass_to_lower,
                "fail_to_higher": fail_to_higher,
                "partial_to_pass": partial_to_pass,
                "partial_to_fail": partial_to_fail,
            },
        }
        wk_s = f"{wk:.4f}" if wk is not None else "n/a"
        bk_s = f"{bin_k:.4f}" if bin_k is not None else "n/a"
        print(f"[{arm}] n={n}  shift={mean_shift:+.4f}  3L-κ={wk_s}  bin-κ={bk_s}")

    # Cross-judge σ_γ comparison: opus-on-gpt-answers minus gpt-on-gpt-answers
    # Non-blind reference: +0.5694 (from the heavy rerun)
    try:
        canon_gpt_on_gpt = load(CANON["gpt-ans-gpt-judge"])
        canon_opus_on_gpt = load(CANON["gpt-ans-opus-judge"])
        blind_gpt_on_gpt = load(find_blind("gpt-ans-gpt-judge")) if find_blind("gpt-ans-gpt-judge") else {}
        blind_opus_on_gpt = load(find_blind("gpt-ans-opus-judge")) if find_blind("gpt-ans-opus-judge") else {}

        def shift(opus, gpt):
            common = set(opus) & set(gpt)
            if not common:
                return None
            return sum(SCORE[opus[c]] - SCORE[gpt[c]] for c in common) / len(common), len(common)

        canon_shift = shift(canon_opus_on_gpt, canon_gpt_on_gpt)
        blind_shift = shift(blind_opus_on_gpt, blind_gpt_on_gpt) if blind_opus_on_gpt and blind_gpt_on_gpt else None

        results["cross_judge_sigma_gamma"] = {
            "canon_shift_opus_minus_gpt_on_gpt_answers": {
                "value": round(canon_shift[0], 4) if canon_shift else None,
                "n": canon_shift[1] if canon_shift else 0,
                "note": "Apr 20 canonical — +0.500 in v0.1, +0.5694 in v0.2 (averaged over 4 reps)",
            },
            "blind_shift_opus_minus_gpt_on_gpt_answers": {
                "value": round(blind_shift[0], 4) if blind_shift else None,
                "n": blind_shift[1] if blind_shift else 0,
                "note": "Blind-packet rerun — measures sigma_gamma after double-blinding",
            },
            "self_preference_attributable_delta": (
                round(canon_shift[0] - blind_shift[0], 4)
                if canon_shift and blind_shift else None
            ),
        }

        # Asymmetry — 22/54 originally. Recompute under blind.
        if blind_opus_on_gpt and blind_gpt_on_gpt:
            common = set(blind_opus_on_gpt) & set(blind_gpt_on_gpt)
            opus_higher = sum(1 for c in common if SCORE[blind_opus_on_gpt[c]] > SCORE[blind_gpt_on_gpt[c]])
            gpt_higher = sum(1 for c in common if SCORE[blind_gpt_on_gpt[c]] > SCORE[blind_opus_on_gpt[c]])
            results["asymmetry_under_blind"] = {
                "opus_higher": opus_higher,
                "gpt_higher": gpt_higher,
                "ties": len(common) - opus_higher - gpt_higher,
                "n_common": len(common),
                "note": "Non-blind was 22 opus-higher / 0 gpt-higher / 32 mixed out of 54.",
            }
    except Exception as e:
        results["cross_judge_sigma_gamma_error"] = str(e)

    out_json = Path("/Users/saxenauts/Documents/personal/syke-replay-lab/research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_blind_vs_canonical_deltas.json")
    out_json.write_text(json.dumps(results, indent=2))
    print(f"\nWrote: {out_json}")

    # Human-readable memo
    lines = ["# Blind-Packet vs Canonical Deltas — 2026-04-21\n"]
    lines.append("Paired comparison: same Apr 20 answers, rejudged once with the full identity packet (canonical) and once with SYKE_BLIND_PACKET=1 (double-blind).\n")
    lines.append("## Per-arm shift\n")
    lines.append("| Arm | n | Shift (blind − canon) | 3-level κ | Any flip | Full-band |")
    lines.append("|---|---|---|---|---|---|")
    for arm in ("gpt-ans-gpt-judge", "gpt-ans-opus-judge", "opus-ans-opus-judge", "opus-ans-gpt-judge"):
        r = results.get(arm, {})
        if r.get("status") != "ok":
            lines.append(f"| {arm} | — | pending/missing | | | |")
            continue
        f = r["flips"]
        lines.append(f"| {arm} | {r['n_common']} | {r['mean_shift_blind_minus_canon']:+.4f} | {r['weighted_kappa_3level']} | {f['any_flip']}/{r['n_common']} | {f['full_band_pass_fail']} |")
    lines.append("")
    if "cross_judge_sigma_gamma" in results:
        s = results["cross_judge_sigma_gamma"]
        lines.append("## σ_γ comparison (opus-judge minus gpt-judge on SAME gpt-agent answers)\n")
        lines.append(f"- Canonical (identity visible): **{s['canon_shift_opus_minus_gpt_on_gpt_answers']['value']}** (n={s['canon_shift_opus_minus_gpt_on_gpt_answers']['n']})")
        lines.append(f"- Blind (identity masked):     **{s['blind_shift_opus_minus_gpt_on_gpt_answers']['value']}** (n={s['blind_shift_opus_minus_gpt_on_gpt_answers']['n']})")
        lines.append(f"- Attributable to identity leak: **{s['self_preference_attributable_delta']}**")
    if "asymmetry_under_blind" in results:
        a = results["asymmetry_under_blind"]
        lines.append("\n## The 22/54 asymmetry under blind\n")
        lines.append(f"- Opus-higher cells: {a['opus_higher']} / {a['n_common']} (was 22/54)")
        lines.append(f"- GPT-higher cells:  {a['gpt_higher']} / {a['n_common']} (was 0/54)")
        lines.append(f"- Ties/mixed:        {a['ties']} / {a['n_common']} (was 32/54)")

    out_md = Path("/Users/saxenauts/Documents/personal/syke-replay-lab/research/n1-memory-lab/judge-calibrated-baseline-experiment/results/20260421_blind_vs_canonical_deltas.md")
    out_md.write_text("\n".join(lines))
    print(f"Wrote: {out_md}")


if __name__ == "__main__":
    main()
