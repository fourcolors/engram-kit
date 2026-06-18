#!/usr/bin/env python3
"""Descriptive exploration counts for the 20-minute analysis pass.

No decisions, no architecture ranking.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


EXP_ROOT = Path(__file__).resolve().parents[1]
PACKETS = EXP_ROOT / "results" / "20260421_calibration_subset_packets.json"
CLAIM_AUDIT = EXP_ROOT / "results" / "20260421_high_priority_claim_audit.md"
TRIAGE = EXP_ROOT / "results" / "20260421_calibration_subset_triage.md"
OUT_JSON = EXP_ROOT / "results" / "20260421_exploration_counts.json"
OUT_MD = EXP_ROOT / "results" / "20260421_exploration_counts.md"

ORD = {"fail": 0, "partial": 1, "pass": 2}


def verdict_pair_stats(a: str | None, b: str | None) -> str:
    if a not in ORD or b not in ORD:
        return "invalid_or_missing"
    delta = abs(ORD[a] - ORD[b])
    if delta == 0:
        return "exact"
    if delta == 1:
        return "adjacent"
    return "full_band"


def main() -> None:
    packets = json.loads(PACKETS.read_text(encoding="utf-8"))
    cells = packets["cells"]
    by_answer_pair = Counter()
    by_referenceability = Counter()
    by_target = Counter()
    by_character = Counter()
    disagreement_examples: list[dict[str, Any]] = []
    invalid_examples: list[dict[str, Any]] = []

    for cell in cells:
        meta = cell.get("probe_metadata") or {}
        ref = meta.get("criterion_referenceability") or "unknown"
        target = meta.get("target_slice") or "unknown"
        character = meta.get("retrieval_character") or "unknown"
        by_referenceability[ref] += 1
        by_target[target] += 1
        by_character[character] += 1
        for answer in cell["answers"]:
            judges = answer["judges"]
            verdicts = [
                (label, brief.get("verdict") if brief else None)
                for label, brief in judges.items()
            ]
            if len(verdicts) != 2:
                continue
            (label_a, verdict_a), (label_b, verdict_b) = verdicts
            category = verdict_pair_stats(verdict_a, verdict_b)
            by_answer_pair[(answer["answer_source"], category)] += 1
            record = {
                "probe_id": cell["probe_id"],
                "condition": cell["condition"],
                "answer_source": answer["answer_source"],
                "referenceability": ref,
                "target_slice": target,
                "retrieval_character": character,
                "judge_a": label_a,
                "verdict_a": verdict_a,
                "judge_b": label_b,
                "verdict_b": verdict_b,
                "category": category,
            }
            if category in {"adjacent", "full_band"}:
                disagreement_examples.append(record)
            if category == "invalid_or_missing":
                invalid_examples.append(record)

    claim_text = CLAIM_AUDIT.read_text(encoding="utf-8")
    triage_text = TRIAGE.read_text(encoding="utf-8")
    claim_type_counts = Counter(
        token.strip("`")
        for token in re.findall(
            r"`(verified|inferred|speculative|unsupported|contradicted|uncheckable)`",
            claim_text,
        )
    )
    likely_cause_counts = Counter(
        match.strip().lower()
        for match in re.findall(
            r"\|\s*(answer quality|packet insufficiency|rubric ambiguity|judge bias)\s*\|",
            triage_text,
            flags=re.IGNORECASE,
        )
    )
    priority_counts = Counter(
        match.strip().lower()
        for match in re.findall(r"\|\s*(high|medium|medium-low|medium-low|low)\s*\|", triage_text)
    )
    failure_phrase_counts = {
        phrase: claim_text.lower().count(phrase)
        for phrase in [
            "unsupported",
            "contradicted",
            "uncheckable",
            "stale",
            "wrong thread",
            "storage state",
            "work state",
            "uuid",
            "counts",
            "timeout",
            "syke.db",
            "memex",
        ]
    }
    output = {
        "generated_at": "2026-04-21T10:54:10-07:00",
        "scope": "descriptive exploration only; no decisions",
        "cell_count": len(cells),
        "answer_observation_count": sum(len(cell["answers"]) for cell in cells),
        "metadata_counts": {
            "criterion_referenceability": dict(by_referenceability),
            "target_slice": dict(by_target),
            "retrieval_character": dict(by_character),
        },
        "judge_pair_categories_by_answer_source": {
            f"{source}:{category}": count
            for (source, category), count in by_answer_pair.items()
        },
        "disagreement_examples": disagreement_examples,
        "invalid_examples": invalid_examples,
        "claim_type_counts_in_high_priority_audit": dict(claim_type_counts),
        "triage_likely_cause_counts": dict(likely_cause_counts),
        "triage_priority_counts": dict(priority_counts),
        "failure_phrase_counts": failure_phrase_counts,
    }
    OUT_JSON.write_text(json.dumps(output, indent=2), encoding="utf-8")

    lines = [
        "# 2026-04-21 Exploration Counts",
        "",
        "Scope: descriptive exploration only. No decisions, no architecture ranking.",
        "",
        f"Cells in calibration subset: `{len(cells)}`",
        f"Answer observations: `{output['answer_observation_count']}`",
        "",
        "## Metadata Counts",
        "",
        "### Criterion Referenceability",
        "",
    ]
    for key, value in by_referenceability.items():
        lines.append(f"- `{key}`: {value}")
    lines += ["", "### Target Slice", ""]
    for key, value in by_target.items():
        lines.append(f"- `{key}`: {value}")
    lines += ["", "### Retrieval Character", ""]
    for key, value in by_character.items():
        lines.append(f"- `{key}`: {value}")

    lines += ["", "## Judge Pair Categories By Answer Source", ""]
    for (source, category), count in sorted(by_answer_pair.items()):
        lines.append(f"- `{source}` / `{category}`: {count}")

    lines += ["", "## Triage Likely Cause Counts", ""]
    for key, value in likely_cause_counts.items():
        lines.append(f"- `{key}`: {value}")

    lines += ["", "## Claim Type Counts In High-Priority Audit", ""]
    for key, value in claim_type_counts.items():
        lines.append(f"- `{key}`: {value}")

    lines += ["", "## Phrase Counts In Claim Audit", ""]
    for key, value in failure_phrase_counts.items():
        lines.append(f"- `{key}`: {value}")

    lines += ["", "## Full-Band Or Invalid Examples", ""]
    for record in disagreement_examples + invalid_examples:
        if record["category"] in {"full_band", "invalid_or_missing"}:
            lines.append(
                f"- `{record['probe_id']}/{record['condition']}` {record['answer_source']}: "
                f"{record['judge_a']}={record['verdict_a']} vs "
                f"{record['judge_b']}={record['verdict_b']} ({record['category']})"
            )

    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_MD}")


if __name__ == "__main__":
    main()

