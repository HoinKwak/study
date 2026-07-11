#!/usr/bin/env bash
# 로컬 상시 구동용 — 크래시/네트워크 오류로 죽으면 자동 재시작.
# 사용: bash scripts/run_local.sh [슬리브]
#   예) bash scripts/run_local.sh scalp
# 종료: Ctrl+C
set -u

SLEEVES="${1:-scalp}"
cd "$(dirname "$0")/.." || exit 1

# venv 활성화 (있으면)
if [ -d ".venv" ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

mkdir -p logs
echo "[run_local] 시작 — 슬리브=$SLEEVES (Ctrl+C 로 종료)"

while true; do
  echo "[run_local] $(date '+%Y-%m-%d %H:%M:%S') 프로세스 기동"
  python -m scripts.run_portfolio --sleeves "$SLEEVES" 2>&1 | tee -a logs/paper_scalp.log
  code=${PIPESTATUS[0]}
  echo "[run_local] $(date '+%Y-%m-%d %H:%M:%S') 프로세스 종료(code=$code) — 10초 후 재시작"
  sleep 10
done
