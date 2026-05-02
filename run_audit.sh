#!/usr/bin/env bash
# run_audit.sh — Runs 5 citation audit passes spaced 30 minutes apart.
# Usage: bash run_audit.sh
# Logs start/end time and exit status of each run to run_log.txt.

set -euo pipefail

BRAND="Indeed"
INDUSTRY="HR and recruiting software"
USE_CASE="evaluating and hiring full-time employees at a mid-sized company"
COMPETITORS="Greenhouse,Lever,Workday,Rippling,Gusto"
MODELS="openai,anthropic,perplexity"
BASE_DIR="./reports"
LOG_FILE="./run_log.txt"
TOTAL_RUNS=5
WAIT_SECONDS=1800   # 30 minutes

VENV_PYTHON=".venv/bin/citation-audit"

echo "AI Citation Audit — run script started" | tee -a "$LOG_FILE"
echo "Brand: $BRAND | Industry: $INDUSTRY" | tee -a "$LOG_FILE"
echo "Models: $MODELS | Runs: $TOTAL_RUNS | Interval: ${WAIT_SECONDS}s" | tee -a "$LOG_FILE"
echo "---" | tee -a "$LOG_FILE"

for RUN in $(seq 1 $TOTAL_RUNS); do
    RUN_DIR="${BASE_DIR}/run_${RUN}"
    START=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    echo "[run_${RUN}] START  $START" | tee -a "$LOG_FILE"

    if $VENV_PYTHON \
        --brand "$BRAND" \
        --industry "$INDUSTRY" \
        --use-case "$USE_CASE" \
        --competitors "$COMPETITORS" \
        --models "$MODELS" \
        --output-dir "$RUN_DIR"; then
        STATUS="OK"
    else
        STATUS="ERROR (exit $?)"
    fi

    END=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
    echo "[run_${RUN}] END    $END  status=$STATUS" | tee -a "$LOG_FILE"

    if [ "$RUN" -lt "$TOTAL_RUNS" ]; then
        echo "[run_${RUN}] Waiting ${WAIT_SECONDS}s before run_$((RUN + 1))..." | tee -a "$LOG_FILE"
        sleep "$WAIT_SECONDS"
    fi
done

echo "---" | tee -a "$LOG_FILE"
echo "All $TOTAL_RUNS runs complete." | tee -a "$LOG_FILE"
