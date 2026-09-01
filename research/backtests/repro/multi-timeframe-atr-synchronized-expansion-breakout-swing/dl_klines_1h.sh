#!/bin/bash
# 멀티 타임프레임 ATR% 동시확장 브레이크아웃 — 1h 선물 klines 다운로드(4h/1d는 코드에서 리샘플).
# 스펙: research/strategies/multi-timeframe-atr-synchronized-expansion-breakout-swing.md
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/mtfatr
BASE="https://data.binance.vision/data/futures/um/monthly/klines"
SYMS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"
mkdir -p $SP/data/klines_1h

months=()
for y in 2021; do
  for m in 10 11 12; do months+=("$y-$m"); done
done
for y in 2022 2023 2024 2025; do
  for m in $(seq -w 1 12); do months+=("$y-$m"); done
done
for m in $(seq -w 1 07); do months+=("2026-$m"); done

fetch_one() {
  sym=$1; mo=$2
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/mtfatr
  BASE="https://data.binance.vision/data/futures/um/monthly/klines"
  out="$SP/data/klines_1h/${sym}-1h-${mo}.csv"
  [ -f "$out" ] && return
  url="$BASE/$sym/1h/${sym}-1h-${mo}.zip"
  tmpzip="$SP/data/klines_1h/${sym}-1h-${mo}.zip"
  code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
  if [ "$code" == "200" ]; then
    unzip -p "$tmpzip" > "$out" 2>/dev/null
    rm -f "$tmpzip"
  else
    rm -f "$tmpzip"
    echo "MISS $sym $mo ($code)" >> $SP/data/klines_1h_missing.log
  fi
}
export -f fetch_one

for sym in $SYMS; do
  for mo in "${months[@]}"; do
    fetch_one "$sym" "$mo" &
    while [ $(jobs -r | wc -l) -ge 12 ]; do wait -n; done
  done
done
wait
echo done
