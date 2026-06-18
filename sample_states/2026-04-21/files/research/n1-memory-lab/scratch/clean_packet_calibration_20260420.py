"""
Trusted-packet judge calibration summary for 2026-04-20.

This script only uses the surviving runs that are still licensed for analysis:

- gpt-5.4 ask / gpt-5.4 judge baseline
- claude-opus-4-6 ask / claude-opus-4-6 judge baseline
- gpt-5.4 answers re-judged by claude-opus-4-6
- claude-opus-4-6 answers re-judged by gpt-5.4-mini
- three additional claude-opus-4-6 intra-rater judge-only repeats

It intentionally excludes deleted / invalid GPT-full reruns and marks the GPT-mini
side-material as judge-family evidence rather than full gpt-5.4 intra-rater evidence.
"""

from __future__ import annotations

import json
import statistics as st
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
RUNS = {
    "gpt_final": ROOT / "runs/ne13-real-15d-gpt54-final-20260420T071500Z",
    "opus_final": ROOT / "runs/ne13-real-15d-opus46-final-20260420T071500Z",
    "gptask_opusjudge": ROOT / "runs/ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z",
    "opusask_gptmini": ROOT / "runs/ne13-real-15d-opusask-gpt54judge-20260420T144210Z",
    "opus_rep1": ROOT / "runs/ne13-real-15d-opusask-opusjudge-intrarater-20260420T200314Z",
    "opus_rep2": ROOT / "runs/ne13-real-15d-opus46-intrarater-rep2-20260420T222645Z",
    "opus_rep3": ROOT / "runs/ne13-real-15d-opus46-intrarater-rep3-20260420T222645Z",
    "gptmini_rep2": ROOT / "runs/ne13-real-15d-gpt54-rep2-20260420T144210Z",
    "gptask_gptmini": ROOT / "runs/ne13-real-15d-gpt54ask-gpt54judge-intrarater-20260420T200314Z",
    "gptminiask_opusjudge": ROOT / "runs/ne13-real-15d-gpt54rep2-opusjudge-20260420T200314Z",
}

VERDICT_MAP = {"fail": 0, "partial": 1, "pass": 2}
VERDICT_LABELS = {0: "fail", 1: "partial", 2: "pass"}


def load_config(run_key: str) -> dict:
    return json.loads((RUNS[run_key] / "config.json").read_text())


def load_verdicts(run_key: str) -> dict[tuple[str, str], int]:
    rows = json.loads((RUNS[run_key] / "results.json").read_text())
    out: dict[tuple[str, str], int] = {}
    for item in rows:
        verdict = item.get("verdict")
        if verdict in VERDICT_MAP:
            out[(item["condition"], item["probe_id"])] = VERDICT_MAP[verdict]
    return out


def linear_weighted_kappa(a: list[int], b: list[int]) -> float:
    n = len(a)
    observed = [[0, 0, 0] for _ in range(3)]
    for x, y in zip(a, b):
        observed[x][y] += 1
    row = [sum(r) for r in observed]
    col = [sum(observed[i][j] for i in range(3)) for j in range(3)]
    expected = [[row[i] * col[j] / n for j in range(3)] for i in range(3)]

    def weight(i: int, j: int) -> float:
        return abs(i - j) / 2

    num = sum(weight(i, j) * observed[i][j] for i in range(3) for j in range(3)) / n
    den = sum(weight(i, j) * expected[i][j] for i in range(3) for j in range(3)) / n
    return 1 - num / den if den else float("nan")


def compare(run_a: str, run_b: str) -> dict:
    a = load_verdicts(run_a)
    b = load_verdicts(run_b)
    keys = sorted(set(a) & set(b))
    av = [a[k] for k in keys]
    bv = [b[k] for k in keys]
    deltas = [y - x for x, y in zip(av, bv)]
    binary_matches = [int(x > 0) == int(y > 0) for x, y in zip(av, bv)]
    table = Counter((x, y) for x, y in zip(av, bv))
    return {
        "n": len(keys),
        "exact": sum(x == y for x, y in zip(av, bv)) / len(keys),
        "linear_weighted_kappa": linear_weighted_kappa(av, bv),
        "mean_delta": sum(deltas) / len(deltas),
        "std_delta": st.pstdev(deltas),
        "binary_useful_exact": sum(binary_matches) / len(binary_matches),
        "contingency": {
            VERDICT_LABELS[i]: {VERDICT_LABELS[j]: table[(i, j)] for j in range(3)}
            for i in range(3)
        },
    }


def summarize_opus_panel() -> dict:
    keys = ["opus_final", "opus_rep1", "opus_rep2", "opus_rep3"]
    verdict_dicts = [load_verdicts(key) for key in keys]
    shared = sorted(set.intersection(*(set(d) for d in verdict_dicts)))
    rows = [[d[k] for d in verdict_dicts] for k in shared]
    sigma_eps = sum(st.pstdev(row) for row in rows) / len(rows)
    unanimous = sum(len(set(row)) == 1 for row in rows) / len(rows)
    binary_unanimous = (
        sum(len(set(int(v > 0) for v in row)) == 1 for row in rows) / len(rows)
    )
    return {
        "n_all_four": len(shared),
        "sigma_epsilon_ordinal": sigma_eps,
        "all_four_exact": unanimous,
        "all_four_binary_useful_exact": binary_unanimous,
    }


def print_run_inventory() -> None:
    print("Trusted run inventory")
    print("====================")
    for key in [
        "gpt_final",
        "opus_final",
        "gptask_opusjudge",
        "opusask_gptmini",
        "opus_rep1",
        "opus_rep2",
        "opus_rep3",
    ]:
        cfg = load_config(key)
        print(
            f"- {key}: ask_model={cfg.get('ask_model')} "
            f"judge_model={cfg.get('judge_model')} "
            f"judge_only_from={cfg.get('judge_only_from')}"
        )
    print()


def print_comparison(name: str, result: dict) -> None:
    print(name)
    print("-" * len(name))
    print(
        f"n={result['n']}  exact={result['exact']:.4f}  "
        f"weighted_kappa_linear={result['linear_weighted_kappa']:.4f}  "
        f"mean_delta={result['mean_delta']:+.4f}  std_delta={result['std_delta']:.4f}  "
        f"binary_useful_exact={result['binary_useful_exact']:.4f}"
    )
    for row_name, row in result["contingency"].items():
        print(f"  {row_name}: {row}")
    print()


if __name__ == "__main__":
    print_run_inventory()

    print_comparison(
        "gpt-5.4 answers: gpt-5.4 judge vs opus judge",
        compare("gpt_final", "gptask_opusjudge"),
    )
    print_comparison(
        "opus answers: opus judge vs gpt-5.4-mini judge",
        compare("opus_final", "opusask_gptmini"),
    )
    print_comparison(
        "opus intra-rater: baseline vs rep1",
        compare("opus_final", "opus_rep1"),
    )
    print_comparison(
        "opus intra-rater: baseline vs rep2",
        compare("opus_final", "opus_rep2"),
    )
    print_comparison(
        "opus intra-rater: baseline vs rep3",
        compare("opus_final", "opus_rep3"),
    )

    panel = summarize_opus_panel()
    print("Opus 4-call panel")
    print("-----------------")
    print(
        f"n_all_four={panel['n_all_four']}  "
        f"sigma_epsilon_ordinal={panel['sigma_epsilon_ordinal']:.4f}  "
        f"all_four_exact={panel['all_four_exact']:.4f}  "
        f"all_four_binary_useful_exact={panel['all_four_binary_useful_exact']:.4f}"
    )
