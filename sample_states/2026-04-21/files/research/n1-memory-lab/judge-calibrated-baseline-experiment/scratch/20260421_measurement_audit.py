#!/usr/bin/env python3
"""Initial measurement audit for the judge-calibrated baseline experiment.

Outputs:
- ../results/20260421_measurement_audit.json
- ../results/20260421_measurement_audit.md

Stdlib-only. This script treats pass/partial/fail as ordinal observations for
diagnostics, not as ground truth.
"""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


LAB_ROOT = Path(__file__).resolve().parents[4]
EXP_ROOT = Path(__file__).resolve().parents[1]
OUT_JSON = EXP_ROOT / "results" / "20260421_measurement_audit.json"
OUT_MD = EXP_ROOT / "results" / "20260421_measurement_audit.md"

RUNS = {
    "gpt_final": "ne13-real-15d-gpt54-final-20260420T071500Z",
    "opus_final": "ne13-real-15d-opus46-final-20260420T071500Z",
    "gpt_answers_opus_judge": "ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z",
    "opus_answers_gpt_judge": "ne13-real-15d-opusask-gpt54judge-20260420T144210Z",
    "opus_intra_rep1": "ne13-real-15d-opusask-opusjudge-intrarater-20260420T200314Z",
    "opus_intra_rep2": "ne13-real-15d-opus46-intrarater-rep2-20260420T222645Z",
    "opus_intra_rep3": "ne13-real-15d-opus46-intrarater-rep3-20260420T222645Z",
    "gpt_mini_intra_rep1": "ne13-real-15d-gpt54ask-gpt54judge-intrarater-20260420T200314Z",
    "gpt_mini_intra_rep5": "ne13-real-15d-gpt54ask-gpt54judge-intrarater-rep5-20260421T051720Z",
    "gpt_mini_intra_rep6": "ne13-real-15d-gpt54ask-gpt54judge-intrarater-rep6-20260421T051720Z",
    "gpt_mini_contaminated_diag": "ne13-real-15d-gpt54-rep2-20260420T144210Z",
    "gpt_mini_answers_opus_judge": "ne13-real-15d-gpt54rep2-opusjudge-20260420T200314Z",
    "old_gpt_baseline": "ne13_15d_timefix_baseline_gpt54_20260416T171500Z",
    "old_opus_rep1": "ab07-opus-judge-rep1",
    "old_opus_rep2": "ab07-opus-judge-rep2",
    "old_opus_rep3": "ab07-opus-judge-rep3"
}

SUBAXES = [
    ("factual_grounding", "support"),
    ("factual_grounding", "boundedness"),
    ("factual_grounding", "uncertainty_calibration"),
    ("continuity", "active_thread_selection"),
    ("continuity", "salience_relevance"),
    ("continuity", "state_transition_tracking"),
    ("continuity", "forgetting_residue_control"),
    ("continuity", "continuation_value"),
    ("coherence", "cross_harness_braid"),
    ("coherence", "cross_session_consistency"),
    ("coherence", "artifact_routing_consistency"),
    ("coherence", "contradiction_handling"),
]

AXIS_NAMES = [f"{axis}.{sub}" for axis, sub in SUBAXES]
VERDICT_SCORE = {"fail": 0, "partial": 1, "pass": 2}
SUBAXIS_SCORE = {"missed": 0, "partial": 1, "strong": 2, "hit": 2}


def load_run(run_name: str) -> dict[str, Any]:
    path = LAB_ROOT / "runs" / run_name / "benchmark_results.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["_path"] = str(path)
    payload["_run_name"] = run_name
    return payload


def item_key(item: dict[str, Any]) -> tuple[str, str]:
    return (str(item.get("probe_id")), str(item.get("condition")))


def valid_verdict(item: dict[str, Any]) -> str | None:
    verdict = item.get("verdict")
    return str(verdict) if verdict in VERDICT_SCORE else None


def binary_useful(verdict: str) -> str:
    return "useful" if verdict in {"pass", "partial"} else "fail"


def denominator(run_key: str, run: dict[str, Any]) -> dict[str, Any]:
    items = list(run.get("items") or [])
    counts = Counter(str(item.get("verdict") or "missing") for item in items)
    valid = sum(counts[v] for v in VERDICT_SCORE)
    conditions = Counter(str(item.get("condition")) for item in items)
    probes = {str(item.get("probe_id")) for item in items}
    config = run.get("config") or {}
    return {
        "run_key": run_key,
        "run_name": run["_run_name"],
        "path": run["_path"],
        "expected_cells": 57 if len(probes) == 19 and len(conditions) == 3 else len(items),
        "items": len(items),
        "valid": valid,
        "invalid": counts.get("invalid", 0),
        "missing": max(0, 57 - len(items)) if len(probes) <= 19 else 0,
        "counts": dict(counts),
        "conditions": dict(conditions),
        "probe_count": len(probes),
        "config": {
            "ask_model": config.get("ask_model"),
            "judge_model": config.get("judge_model"),
            "ask_provider": config.get("ask_provider"),
            "judge_provider": config.get("judge_provider"),
            "judge_only_from": config.get("judge_only_from"),
        },
    }


def weighted_kappa(pairs: list[tuple[int, int]], *, levels: int = 3) -> float | None:
    if not pairs:
        return None
    n = len(pairs)
    observed = 0.0
    for a, b in pairs:
        observed += abs(a - b) / (levels - 1)
    observed /= n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    expected = 0.0
    for i in range(levels):
        for j in range(levels):
            expected += (ca[i] / n) * (cb[j] / n) * (abs(i - j) / (levels - 1))
    if expected == 0:
        return 1.0 if observed == 0 else None
    return 1.0 - observed / expected


def nominal_kappa(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    labels = sorted({value for pair in pairs for value in pair})
    n = len(pairs)
    pa = sum(1 for a, b in pairs if a == b) / n
    ca = Counter(a for a, _ in pairs)
    cb = Counter(b for _, b in pairs)
    pe = sum((ca[label] / n) * (cb[label] / n) for label in labels)
    if pe == 1.0:
        return 1.0 if pa == 1.0 else None
    return (pa - pe) / (1.0 - pe)


def judge_swap(name: str, run_a: dict[str, Any], run_b: dict[str, Any]) -> dict[str, Any]:
    a_items = {item_key(item): item for item in run_a.get("items") or []}
    b_items = {item_key(item): item for item in run_b.get("items") or []}
    keys = sorted(set(a_items) & set(b_items))
    ordinal_pairs: list[tuple[int, int]] = []
    binary_pairs: list[tuple[str, str]] = []
    deltas: list[int] = []
    full_band = 0
    adjacent = 0
    for key in keys:
        va = valid_verdict(a_items[key])
        vb = valid_verdict(b_items[key])
        if va is None or vb is None:
            continue
        sa, sb = VERDICT_SCORE[va], VERDICT_SCORE[vb]
        ordinal_pairs.append((sa, sb))
        binary_pairs.append((binary_useful(va), binary_useful(vb)))
        deltas.append(sb - sa)
        if abs(sb - sa) == 2:
            full_band += 1
        elif abs(sb - sa) == 1:
            adjacent += 1
    n = len(ordinal_pairs)
    exact = sum(1 for a, b in ordinal_pairs if a == b)
    binary_exact = sum(1 for a, b in binary_pairs if a == b)
    return {
        "name": name,
        "overlap": n,
        "exact": exact / n if n else None,
        "weighted_kappa_linear": weighted_kappa(ordinal_pairs),
        "mean_delta_b_minus_a": sum(deltas) / n if n else None,
        "binary_useful_exact": binary_exact / n if n else None,
        "binary_kappa": nominal_kappa(binary_pairs),
        "adjacent_disagreements": adjacent,
        "full_band_disagreements": full_band,
    }


def repeat_group(name: str, runs: list[dict[str, Any]]) -> dict[str, Any]:
    item_maps = [{item_key(item): item for item in run.get("items") or []} for run in runs]
    keys = sorted(set.intersection(*(set(m) for m in item_maps)))
    common_valid: list[tuple[tuple[str, str], list[int]]] = []
    pairwise: list[dict[str, Any]] = []
    for i in range(len(runs)):
        for j in range(i + 1, len(runs)):
            pairs: list[tuple[int, int]] = []
            binary_pairs: list[tuple[str, str]] = []
            for key in sorted(set(item_maps[i]) & set(item_maps[j])):
                vi = valid_verdict(item_maps[i][key])
                vj = valid_verdict(item_maps[j][key])
                if vi is None or vj is None:
                    continue
                pairs.append((VERDICT_SCORE[vi], VERDICT_SCORE[vj]))
                binary_pairs.append((binary_useful(vi), binary_useful(vj)))
            n = len(pairs)
            pairwise.append({
                "a": runs[i]["_run_name"],
                "b": runs[j]["_run_name"],
                "overlap": n,
                "exact": sum(1 for a, b in pairs if a == b) / n if n else None,
                "weighted_kappa_linear": weighted_kappa(pairs),
                "binary_useful_exact": sum(1 for a, b in binary_pairs if a == b) / n if n else None,
                "binary_kappa": nominal_kappa(binary_pairs),
            })
    for key in keys:
        scores: list[int] = []
        ok = True
        for mapping in item_maps:
            verdict = valid_verdict(mapping[key])
            if verdict is None:
                ok = False
                break
            scores.append(VERDICT_SCORE[verdict])
        if ok:
            common_valid.append((key, scores))
    flip_cells = [entry for entry in common_valid if len(set(entry[1])) > 1]
    full_band = sum(1 for _, scores in flip_cells if max(scores) - min(scores) == 2)
    adjacent = sum(1 for _, scores in flip_cells if max(scores) - min(scores) == 1)
    per_probe = Counter(key[0] for key, _ in flip_cells)
    sigmas = []
    for _, scores in common_valid:
        mu = sum(scores) / len(scores)
        sigmas.append(math.sqrt(sum((score - mu) ** 2 for score in scores) / len(scores)))
    return {
        "name": name,
        "run_names": [run["_run_name"] for run in runs],
        "common_valid_cells": len(common_valid),
        "all_reps_exact_cells": len(common_valid) - len(flip_cells),
        "flip_cells": len(flip_cells),
        "flip_rate": len(flip_cells) / len(common_valid) if common_valid else None,
        "adjacent_flip_cells": adjacent,
        "full_band_flip_cells": full_band,
        "mean_cell_sigma": sum(sigmas) / len(sigmas) if sigmas else None,
        "per_probe_flip_counts": dict(per_probe),
        "pairwise": pairwise,
    }


def subaxis_vector(item: dict[str, Any]) -> list[int] | None:
    result = item.get("judge_result") or {}
    values: list[int] = []
    for axis, subaxis in SUBAXES:
        score = (
            result.get(axis, {})
            .get("subcategories", {})
            .get(subaxis, {})
            .get("score")
        )
        if score not in SUBAXIS_SCORE:
            return None
        values.append(SUBAXIS_SCORE[score])
    return values


def mat_transpose(matrix: list[list[float]]) -> list[list[float]]:
    return [list(col) for col in zip(*matrix, strict=False)]


def solve_linear_system(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    aug = [row[:] + [b_i] for row, b_i in zip(a, b, strict=True)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            aug[col][col] += 1e-9
            pivot = col
        aug[col], aug[pivot] = aug[pivot], aug[col]
        div = aug[col][col]
        if abs(div) < 1e-12:
            continue
        aug[col] = [value / div for value in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            aug[row] = [rv - factor * cv for rv, cv in zip(aug[row], aug[col], strict=True)]
    return [aug[i][-1] for i in range(n)]


def ols_r2(rows: list[tuple[list[int], int]], indexes: list[int]) -> dict[str, Any]:
    if not rows:
        return {"n": 0, "p": len(indexes), "r2": None, "adjusted_r2": None}
    x = [[1.0] + [float(features[i]) for i in indexes] for features, _ in rows]
    y = [float(target) for _, target in rows]
    xt = mat_transpose(x)
    xtx = [[sum(xt_i[k] * x_j[k] for k in range(len(x))) for x_j in xt] for xt_i in xt]
    xty = [sum(xt_i[k] * y[k] for k in range(len(y))) for xt_i in xt]
    beta = solve_linear_system(xtx, xty)
    preds = [sum(beta_j * x_ij for beta_j, x_ij in zip(beta, row, strict=True)) for row in x]
    mu = sum(y) / len(y)
    ss_res = sum((obs - pred) ** 2 for obs, pred in zip(y, preds, strict=True))
    ss_tot = sum((obs - mu) ** 2 for obs in y)
    r2 = 1.0 - ss_res / ss_tot if ss_tot else 0.0
    p = len(indexes)
    n = len(y)
    adjusted = 1.0 - (1.0 - r2) * (n - 1) / (n - p - 1) if n - p - 1 > 0 else None
    return {"n": n, "p": p, "r2": r2, "adjusted_r2": adjusted}


def rubric_rows(runs: list[dict[str, Any]]) -> list[tuple[list[int], int]]:
    rows: list[tuple[list[int], int]] = []
    for run in runs:
        for item in run.get("items") or []:
            verdict = valid_verdict(item)
            vector = subaxis_vector(item)
            if verdict is not None and vector is not None:
                rows.append((vector, VERDICT_SCORE[verdict]))
    return rows


def pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) != len(ys) or len(xs) < 2:
        return None
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    vx = sum((x - mx) ** 2 for x in xs)
    vy = sum((y - my) ** 2 for y in ys)
    if vx == 0 or vy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys, strict=True)) / math.sqrt(vx * vy)


def factor_collapse(rows: list[tuple[list[int], int]]) -> dict[str, Any]:
    if not rows:
        return {"n": 0, "top_abs_correlations": []}
    cols = list(zip(*(features for features, _ in rows), strict=False))
    pairs = []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            corr = pearson([float(x) for x in cols[i]], [float(y) for y in cols[j]])
            if corr is not None:
                pairs.append({
                    "a": AXIS_NAMES[i],
                    "b": AXIS_NAMES[j],
                    "r": corr,
                    "abs_r": abs(corr),
                })
    pairs.sort(key=lambda row: row["abs_r"], reverse=True)
    return {"n": len(rows), "top_abs_correlations": pairs[:15]}


def main() -> None:
    runs = {key: load_run(name) for key, name in RUNS.items()}
    denominators = {key: denominator(key, run) for key, run in runs.items()}
    swaps = [
        judge_swap("gpt_answers__gpt_judge_vs_opus_judge", runs["gpt_final"], runs["gpt_answers_opus_judge"]),
        judge_swap("opus_answers__opus_judge_vs_gpt_mini_judge", runs["opus_final"], runs["opus_answers_gpt_judge"]),
        judge_swap("old_gpt_answers__gpt_judge_vs_ab07_opus_rep1", runs["old_gpt_baseline"], runs["old_opus_rep1"]),
    ]
    repeats = [
        repeat_group("opus_answers__opus_judge_4_calls", [
            runs["opus_final"],
            runs["opus_intra_rep1"],
            runs["opus_intra_rep2"],
            runs["opus_intra_rep3"],
        ]),
        repeat_group("gpt_answers__gpt_mini_judge_available_calls", [
            runs["gpt_mini_intra_rep1"],
            runs["gpt_mini_intra_rep5"],
            runs["gpt_mini_intra_rep6"],
        ]),
        repeat_group("old_gpt_answers__ab07_opus_3_calls", [
            runs["old_opus_rep1"],
            runs["old_opus_rep2"],
            runs["old_opus_rep3"],
        ]),
    ]
    gpt_judge_rows = rubric_rows([runs["gpt_final"], runs["opus_answers_gpt_judge"]])
    opus_judge_rows = rubric_rows([runs["opus_final"], runs["gpt_answers_opus_judge"]])
    all_indexes = list(range(len(SUBAXES)))
    drop_state_transition = [
        i for i, name in enumerate(AXIS_NAMES) if name != "continuity.state_transition_tracking"
    ]
    state_transition_only = [AXIS_NAMES.index("continuity.state_transition_tracking")]
    rubric = {
        "gpt_judge_pooled": {
            "full": ols_r2(gpt_judge_rows, all_indexes),
            "drop_state_transition_tracking": ols_r2(gpt_judge_rows, drop_state_transition),
            "state_transition_only": ols_r2(gpt_judge_rows, state_transition_only),
            "factor_collapse": factor_collapse(gpt_judge_rows),
        },
        "opus_judge_pooled": {
            "full": ols_r2(opus_judge_rows, all_indexes),
            "drop_state_transition_tracking": ols_r2(opus_judge_rows, drop_state_transition),
            "state_transition_only": ols_r2(opus_judge_rows, state_transition_only),
            "factor_collapse": factor_collapse(opus_judge_rows),
        },
    }
    result = {
        "generated_at": "2026-04-21",
        "notes": [
            "pass/partial/fail treated as noisy ordinal observations",
            "gpt_mini_intra_* runs are available same-judge repeats but are gpt-5.4-mini judge config, not clean full gpt-5.4 judge repeats",
            "old ab07 runs are older-packet replication checks, not canonical Apr 20 architecture evidence",
        ],
        "runs": RUNS,
        "denominator_audit": denominators,
        "same_answer_judge_swaps": swaps,
        "same_judge_repeats": repeats,
        "rubric_diagnostics": rubric,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")

    lines = [
        "# 2026-04-21 Measurement Audit",
        "",
        "Pass/partial/fail are treated as noisy ordinal observations, not truth labels.",
        "",
        "## Denominator Highlights",
        "",
        "| run | items | valid | invalid | pass | partial | fail |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for key in [
        "gpt_final",
        "opus_final",
        "gpt_answers_opus_judge",
        "opus_answers_gpt_judge",
        "opus_intra_rep1",
        "opus_intra_rep2",
        "opus_intra_rep3",
        "gpt_mini_intra_rep1",
        "gpt_mini_intra_rep5",
        "gpt_mini_intra_rep6",
    ]:
        row = denominators[key]
        counts = row["counts"]
        lines.append(
            f"| {key} | {row['items']} | {row['valid']} | {row['invalid']} | "
            f"{counts.get('pass', 0)} | {counts.get('partial', 0)} | {counts.get('fail', 0)} |"
        )
    lines += ["", "## Same-Answer Judge Swaps", "", "| comparison | overlap | exact | weighted kappa | mean delta | useful exact |", "|---|---:|---:|---:|---:|---:|"]
    for row in swaps:
        lines.append(
            f"| {row['name']} | {row['overlap']} | {row['exact']:.3f} | "
            f"{row['weighted_kappa_linear']:.3f} | {row['mean_delta_b_minus_a']:.3f} | "
            f"{row['binary_useful_exact']:.3f} |"
        )
    lines += ["", "## Same-Judge Repeats", "", "| group | common valid | flip rate | adjacent flips | full-band flips | mean cell sigma |", "|---|---:|---:|---:|---:|---:|"]
    for row in repeats:
        lines.append(
            f"| {row['name']} | {row['common_valid_cells']} | {row['flip_rate']:.3f} | "
            f"{row['adjacent_flip_cells']} | {row['full_band_flip_cells']} | "
            f"{row['mean_cell_sigma']:.3f} |"
        )
    lines += ["", "## Rubric Diagnostics", "", "| judge pool | full R2 | drop state-transition R2 | state-transition-only R2 | max abs axis corr |", "|---|---:|---:|---:|---:|"]
    for key, row in rubric.items():
        max_corr = row["factor_collapse"]["top_abs_correlations"][0]["abs_r"]
        lines.append(
            f"| {key} | {row['full']['r2']:.3f} | "
            f"{row['drop_state_transition_tracking']['r2']:.3f} | "
            f"{row['state_transition_only']['r2']:.3f} | {max_corr:.3f} |"
        )
    lines += [
        "",
        "## Caveats",
        "",
        "- GPT intrarater repeat rows currently available here are gpt-5.4-mini judge-config repeats, not clean full gpt-5.4 repeats.",
        "- Old ab07 rows are useful replication checks, not canonical Apr 20 architecture evidence.",
        "- OLS uses a stdlib normal-equation solver and should be treated as an audit calculation, not final psychometrics.",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")


if __name__ == "__main__":
    main()

