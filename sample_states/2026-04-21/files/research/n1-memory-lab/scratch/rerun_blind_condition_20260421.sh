#!/usr/bin/env bash
# Blind-condition rejudge (A1) — mask replay_state.condition from the judge's
# input packet and re-score the Apr 20 canonical answers with both judges.
#
# Why: the judge_brief packet currently leaks which experimental arm
# (production / pure / zero) is being scored. Blind-evaluation hygiene says this
# leak biases verdicts. This rerun tests whether stripping the label changes the
# cross-judge σ_γ shift (+0.57) or the rubric collapse finding.
#
# The benchmark_runner.py has a minimal env-var gate (SYKE_BLIND_CONDITION=1)
# that replaces `replay_state.condition` and `replay_state.ask_mode` with
# `[MASKED]` in the packet the judge reads.
#
# Four rerun arms, each judge_only from a canonical Apr 20 source:
#   1. gpt-answers   × gpt-5.4 judge
#   2. gpt-answers   × opus-4.6 judge
#   3. opus-answers  × opus-4.6 judge
#   4. opus-answers  × gpt-5.4 judge
#
# All 4 use the SAME answer set — only the condition label is masked on the
# rejudge. Direct paired comparison with the non-blind Apr 20 runs.
#
# Usage:
#   bash research/n1-memory-lab/scratch/rerun_blind_condition_20260421.sh [arm]
# where [arm] is one of: gpt-gpt | gpt-opus | opus-opus | opus-gpt | all
#
# Safety: this touches the Pi stack. Make sure ~/.syke/pi-agent/models.json
# has both gpt-5.4 and claude-opus-4-6 configured before running.

set -euo pipefail
cd "$(dirname "$0")/../../.."

# Use the syke venv where benchmark-running deps (uuid_extensions, pi stack,
# syke.db, syke.llm.*) are actually installed.
PYBIN="${PYBIN:-/Users/saxenauts/Documents/personal/syke/.venv/bin/python}"

ARM="${1:-all}"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
GPT_SRC="runs/ne13-real-15d-gpt54-final-20260420T071500Z"
OPUS_SRC="runs/ne13-real-15d-opus46-final-20260420T071500Z"

run_arm() {
  local arm_name="$1"
  local source="$2"
  local judge_model="$3"
  local out="runs/ne13-blind-condition-${arm_name}-${STAMP}"
  echo "[blind-rerun] arm=${arm_name} source=${source} judge=${judge_model}"
  echo "[blind-rerun] out=${out}"
  SYKE_BLIND_CONDITION=1 \
    "${PYBIN}" benchmark_runner.py \
      --judge-only-from "${source}" \
      --all-items \
      --judge-model "${judge_model}" \
      --output-dir "${out}"
  echo "[blind-rerun] done: ${out}"
}

case "$ARM" in
  gpt-gpt)   run_arm "gpt-answers-gpt-judge"   "$GPT_SRC"  "gpt-5.4" ;;
  gpt-opus)  run_arm "gpt-answers-opus-judge"  "$GPT_SRC"  "claude-opus-4-6" ;;
  opus-opus) run_arm "opus-answers-opus-judge" "$OPUS_SRC" "claude-opus-4-6" ;;
  opus-gpt)  run_arm "opus-answers-gpt-judge"  "$OPUS_SRC" "gpt-5.4" ;;
  all)
    run_arm "gpt-answers-gpt-judge"   "$GPT_SRC"  "gpt-5.4"
    run_arm "gpt-answers-opus-judge"  "$GPT_SRC"  "claude-opus-4-6"
    run_arm "opus-answers-opus-judge" "$OPUS_SRC" "claude-opus-4-6"
    run_arm "opus-answers-gpt-judge"  "$OPUS_SRC" "gpt-5.4"
    ;;
  *)
    echo "Unknown arm: $ARM" >&2
    echo "Usage: $0 {gpt-gpt|gpt-opus|opus-opus|opus-gpt|all}" >&2
    exit 2
    ;;
esac
