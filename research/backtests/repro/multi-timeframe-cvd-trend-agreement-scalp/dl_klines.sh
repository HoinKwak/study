#!/bin/bash
# 멀티TF CVD 추세합치 스캘프 — 5m/15m/1h 선물 klines 다운로드(월별 zip, data.binance.vision).
# 스펙: research/strategies/multi-timeframe-cvd-trend-agreement-scalp.md
# (참고용 — 실제로는 run_prefetch.py 가 requests 로 동일한 파일을 병렬 다운로드한다.)
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/mtfcvd
BASE="https://data.binance.vision/data/futures/um/monthly/klines"
SYMS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"
TFS="5m 15m 1h"

months=()
for y in 2022 2023 2024 2025; do
  for m in $(seq -w 1 12); do months+=("$y-$m"); done
done
for m in $(seq -w 1 06); do months+=("2026-$m"); done

fetch_one() {
  sym=$1; tf=$2; mo=$3
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/mtfcvd
  BASE="https://data.binance.vision/data/futures/um/monthly/klines"
  mkdir -p "$SP/data/klines_$tf"
  out="$SP/data/klines_$tf/${sym}-${tf}-${mo}.csv"
  [ -f "$out" ] && return
  url="$BASE/$sym/$tf/${sym}-${tf}-${mo}.zip"
  tmpzip="$SP/data/klines_$tf/${sym}-${tf}-${mo}.zip"
  code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
  if [ "$code" == "200" ]; then
    unzip -p "$tmpzip" > "$out" 2>/dev/null
    rm -f "$tmpzip"
  else
    rm -f "$tmpzip"
    echo "MISS $sym $tf $mo ($code)" >> "$SP/data/klines_missing.log"
  fi
}
export -f fetch_one

for tf in $TFS; do
  for sym in $SYMS; do
    for mo in "${months[@]}"; do
      fetch_one "$sym" "$tf" "$mo" &
      while [ $(jobs -r | wc -l) -ge 12 ]; do wait -n; done
    done
  done
done
wait
echo done
