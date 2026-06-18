#!/usr/bin/env python3
"""Prepare the 30-cell calibration subset for review.

The subset is probe x condition. For each selected cell this script includes
both available answer families and their paired judge observations:

- GPT answer with GPT judge and Opus judge.
- Opus answer with Opus judge and GPT-family judge.

Outputs:
- ../results/20260421_calibration_subset_packets.json
- ../results/20260421_calibration_subset_packets.md
- ../datasets/claim_audit_template.json
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


LAB_ROOT = Path(__file__).resolve().parents[4]
EXP_ROOT = Path(__file__).resolve().parents[1]

SUBSET_PATH = EXP_ROOT / "datasets" / "human_calibration_subset.json"
PROBE_META_PATH = EXP_ROOT / "datasets" / "probe_metadata.json"
OUT_JSON = EXP_ROOT / "results" / "20260421_calibration_subset_packets.json"
OUT_MD = EXP_ROOT / "results" / "20260421_calibration_subset_packets.md"
TEMPLATE_JSON = EXP_ROOT / "datasets" / "claim_audit_template.json"

RUNS = {
    "gpt_answer__gpt_judge": "ne13-real-15d-gpt54-final-20260420T071500Z",
    "gpt_answer__opus_judge": "ne13-real-15d-gpt54ask-opusjudge-20260420T144210Z",
    "opus_answer__opus_judge": "ne13-real-15d-opus46-final-20260420T071500Z",
    "opus_answer__gpt_family_judge": "ne13-real-15d-opusask-gpt54judge-20260420T144210Z",
}

AXES = ("factual_grounding", "continuity", "coherence")


def load_results(run_name: str) -> dict[tuple[str, str], dict[str, Any]]:
    path = LAB_ROOT / "runs" / run_name / "benchmark_results.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return {
        (str(item.get("probe_id")), str(item.get("condition"))): item
        for item in data.get("items", [])
    }


def axis_scores(judge_result: dict[str, Any]) -> dict[str, str | None]:
    scores: dict[str, str | None] = {}
    for axis in AXES:
        value = judge_result.get(axis)
        if isinstance(value, dict):
            scores[axis] = value.get("score")
        else:
            scores[axis] = None
    return scores


def judge_brief(item: dict[str, Any] | None) -> dict[str, Any] | None:
    if not item:
        return None
    result = item.get("judge_result")
    if not isinstance(result, dict):
        result = {}
    return {
        "verdict": item.get("verdict"),
        "summary": result.get("summary"),
        "axis_scores": axis_scores(result),
        "judge_error": result.get("error"),
        "artifacts": item.get("artifacts"),
    }


def answer_record(
    *,
    answer_source: str,
    primary: dict[str, Any] | None,
    paired: dict[str, Any] | None,
    primary_label: str,
    paired_label: str,
) -> dict[str, Any]:
    answer_text = str((primary or paired or {}).get("answer_text") or "")
    metadata = (primary or paired or {}).get("answer_metadata") or {}
    return {
        "answer_source": answer_source,
        "answer_text": answer_text,
        "answer_excerpt": answer_text[:1200],
        "answer_model": metadata.get("model"),
        "tool_calls": (primary or paired or {}).get("tool_calls"),
        "cost_usd": (primary or paired or {}).get("cost_usd"),
        "judges": {
            primary_label: judge_brief(primary),
            paired_label: judge_brief(paired),
        },
        "review_template": {
            "target_state": None,
            "claim_audit": [],
            "overall_observation": None,
            "failure_attribution": [],
            "wrong_restart_risk": None,
            "reviewer_notes": None,
        },
    }


def main() -> None:
    subset = json.loads(SUBSET_PATH.read_text(encoding="utf-8"))
    probe_meta = {
        row["probe_id"]: row
        for row in json.loads(PROBE_META_PATH.read_text(encoding="utf-8"))["probes"]
    }
    runs = {label: load_results(name) for label, name in RUNS.items()}

    cells = []
    for cell in subset["cells"]:
        key = (cell["probe_id"], cell["condition"])
        gpt_gpt = runs["gpt_answer__gpt_judge"].get(key)
        gpt_opus = runs["gpt_answer__opus_judge"].get(key)
        opus_opus = runs["opus_answer__opus_judge"].get(key)
        opus_gpt = runs["opus_answer__gpt_family_judge"].get(key)
        cell_record = {
            "probe_id": key[0],
            "condition": key[1],
            "probe_metadata": probe_meta.get(key[0]),
            "answers": [
                answer_record(
                    answer_source="gpt-5.4",
                    primary=gpt_gpt,
                    paired=gpt_opus,
                    primary_label="gpt-5.4_judge",
                    paired_label="opus-4.6_judge",
                ),
                answer_record(
                    answer_source="opus-4.6",
                    primary=opus_opus,
                    paired=opus_gpt,
                    primary_label="opus-4.6_judge",
                    paired_label="gpt-family_judge",
                ),
            ],
        }
        cells.append(cell_record)

    payload = {
        "version": 1,
        "created_at": "2026-04-21",
        "purpose": "Review packets for the initial 30-cell human calibration subset.",
        "caveats": [
            "gpt-family judge on Opus answers is gpt-5.4-mini in available artifacts, not clean full gpt-5.4.",
            "These review packets are for judge/rubric calibration, not architecture ranking.",
        ],
        "cells": cells,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    template = {
        "claim_audit_item": {
            "claim_text": "",
            "type": "verified|inferred|speculative|unsupported|contradicted|uncheckable",
            "evidence_ids": [],
            "check_method": "deterministic|judge_semantic|human_review",
            "notes": ""
        },
        "overall_observation_values": [
            "pass",
            "partial",
            "fail",
            "cannot_determine",
            "packet_insufficient",
            "rubric_ambiguous"
        ],
        "failure_attribution_values": [
            "answer_wrong",
            "packet_insufficient",
            "reference_ambiguous",
            "judge_error",
            "rubric_ambiguous",
            "unsupported_inference",
            "contradicted_evidence",
            "stale_state_selection",
            "wrong_restart_risk"
        ],
    }
    TEMPLATE_JSON.write_text(json.dumps(template, indent=2), encoding="utf-8")

    lines = [
        "# Calibration Subset Packets",
        "",
        "These packets are for judge/rubric calibration, not architecture ranking.",
        "",
        "| probe | condition | target | ref | character | GPT judges | Opus judges |",
        "|---|---|---|---|---|---|---|",
    ]
    for cell in cells:
        meta = cell.get("probe_metadata") or {}
        gpt_answer = cell["answers"][0]
        opus_answer = cell["answers"][1]
        gpt_judges = ", ".join(
            f"{label}:{brief.get('verdict') if brief else 'missing'}"
            for label, brief in gpt_answer["judges"].items()
        )
        opus_judges = ", ".join(
            f"{label}:{brief.get('verdict') if brief else 'missing'}"
            for label, brief in opus_answer["judges"].items()
        )
        lines.append(
            f"| {cell['probe_id']} | {cell['condition']} | {meta.get('target_slice')} | "
            f"{meta.get('criterion_referenceability')} | {meta.get('retrieval_character')} | "
            f"{gpt_judges} | {opus_judges} |"
        )
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")
    print(f"wrote {TEMPLATE_JSON}")


if __name__ == "__main__":
    main()

