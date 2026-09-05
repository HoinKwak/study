#!/bin/bash
# 1d/4h klines monthly zip 다운로드 (2021-10 ~ 2026-06)
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi
SYMS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"
TFS="1d 4h"
mkdir -p $SP/data/klines_1d $SP/data/klines_4h

months=()
for y in 2021; do
  for m in 10 11 12; do months+=("$y-$m"); done
done
for y in 2022 2023 2024 2025; do
  for m in $(seq -w 1 12); do months+=("$y-$m"); done
done
for m in $(seq -w 1 06); do months+=("2026-$m"); done

fetch_one() {
  sym=$1; tf=$2; mo=$3
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi
  dirn="klines_1d"; [ "$tf" == "4h" ] && dirn="klines_4h"
  out="$SP/data/$dirn/${sym}-${tf}-${mo}.csv"
  [ -f "$out" ] && return
  url="https://data.binance.vision/data/futures/um/monthly/klines/$sym/$tf/${sym}-${tf}-${mo}.zip"
  tmpzip="$SP/data/$dirn/${sym}-${tf}-${mo}.zip"
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

jobs=()
for sym in $SYMS; do
  for tf in $TFS; do
    for mo in "${months[@]}"; do
      jobs+=("$sym $tf $mo")
    done
  done
done
printf "%s\n" "${jobs[@]}" | xargs -P 16 -I{} bash -c 'fetch_one {}'
echo done
