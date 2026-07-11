#!/usr/bin/env bash
# 시장 스캐너 로컬 상시 구동 — 죽으면 자동 재시작.
# 사용: bash scripts/run_scanner_local.sh
# 종료: Ctrl+C
set -u

cd "$(dirname "$0")/.." || exit 1

if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

mkdir -p logs
echo "[scanner] 시작 (Ctrl+C 로 종료)"

while true; do
  echo "[scanner] $(date '+%Y-%m-%d %H:%M:%S') 프로세스 기동"
  python -m scripts.run_scanner 2>&1 | tee -a logs/scanner.log
  echo "[scanner] $(date '+%Y-%m-%d %H:%M:%S') 프로세스 종료 — 10초 후 재시작"
  sleep 10
done
