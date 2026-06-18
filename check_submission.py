#!/usr/bin/env python3
"""Local checker for the simplified ENGRAM participant facade."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any


KIT_ROOT = Path(__file__).resolve().parent


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AssertionError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise AssertionError(f"{path} must contain a JSON object")
    return payload


def run_command(args: list[str], *, cwd: Path, timeout_seconds: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )


def validate_answer(path: Path) -> None:
    payload = read_json(path)
    for field in ("answer", "evidence_paths", "uncertainty"):
        if field not in payload:
            raise AssertionError(f"{path} missing required field: {field}")
    if not isinstance(payload["answer"], str) or not payload["answer"].strip():
        raise AssertionError(f"{path} field 'answer' must be a non-empty string")
    if not isinstance(payload["evidence_paths"], list):
        raise AssertionError(f"{path} field 'evidence_paths' must be a list")
    if not isinstance(payload["uncertainty"], str):
        raise AssertionError(f"{path} field 'uncertainty' must be a string")
    if "memory_refs" in payload and not isinstance(payload["memory_refs"], list):
        raise AssertionError(f"{path} field 'memory_refs' must be a list when present")


def state_dir_for_reference_time(reference_time: str, sample_states: list[Path]) -> Path:
    try:
        date = datetime.fromisoformat(reference_time).date().isoformat()
    except ValueError:
        date = reference_time[:10]
    state_dir = KIT_ROOT / "sample_states" / date
    return state_dir if state_dir.exists() else sample_states[-1]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a simplified ENGRAM submission.")
    parser.add_argument("--submission", required=True, help="Path to a folder containing run.sh")
    parser.add_argument("--timeout-seconds", type=int, default=60)
    parser.add_argument("--keep", action="store_true", help="Keep the temporary run directory")
    args = parser.parse_args()

    submission = Path(args.submission).resolve()
    run_sh = submission / "run.sh"
    if not run_sh.exists():
        raise SystemExit(f"missing run.sh: {run_sh}")

    sample_states = sorted((KIT_ROOT / "sample_states").iterdir())
    sample_states = [path for path in sample_states if path.is_dir()]
    if not sample_states:
        raise SystemExit("no sample states found")
    questions = read_json(KIT_ROOT / "sample_questions.json").get("questions", [])
    if not questions:
        raise SystemExit("no sample questions found")

    temp_root = Path(tempfile.mkdtemp(prefix="engram-kit-check-"))
    try:
        memory_dir = temp_root / "memory"
        answer_json = temp_root / "answer.json"
        question_json = temp_root / "question.json"
        memory_dir.mkdir(parents=True, exist_ok=True)

        for state_dir in sample_states:
            result = run_command(
                [str(run_sh), "update", str(state_dir), str(memory_dir)],
                cwd=submission,
                timeout_seconds=args.timeout_seconds,
            )
            if result.returncode != 0:
                raise AssertionError(
                    f"update failed for {state_dir.name}: exit={result.returncode}\n{result.stderr[-2000:]}"
                )

        question = questions[0]
        question_json.write_text(json.dumps(question, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        answer_state = state_dir_for_reference_time(str(question["reference_time"]), sample_states)
        result = run_command(
            [str(run_sh), "answer", str(answer_state), str(memory_dir), str(question_json), str(answer_json)],
            cwd=submission,
            timeout_seconds=args.timeout_seconds,
        )
        if result.returncode != 0:
            raise AssertionError(f"answer failed: exit={result.returncode}\n{result.stderr[-2000:]}")

        validate_answer(answer_json)
        print("ENGRAM simplified submission check passed")
        if args.keep:
            print(f"temp_dir={temp_root}")
            print(f"answer_json={answer_json}")
        else:
            print("temp_dir=cleaned")
        return 0
    finally:
        if not args.keep:
            shutil.rmtree(temp_root, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
