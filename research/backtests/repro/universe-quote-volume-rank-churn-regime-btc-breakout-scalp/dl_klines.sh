#!/bin/bash
# 데이터 다운로드: 1h klines(7종목, 순위churn 계산용) + 15m klines(BTC만, 진입/청산용)
# monthly zip: 2022-01 ~ 2026-06 (OOS 상한 2026-06-30 23:59:59 확보 위해 06월까지)
SP=${RANKCHURN_SCRATCH:-/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/rankchurn}
BASE="https://data.binance.vision/data/futures/um/monthly/klines"
SYMS_1H="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"
SYMS_15M="BTCUSDT"
mkdir -p "$SP"/data/klines1h "$SP"/data/klines15m

months=()
for y in 2022 2023 2024 2025; do
  for m in $(seq -w 1 12); do months+=("$y-$m"); done
done
for m in $(seq -w 1 07); do months+=("2026-$m"); done

fetch_one() {
  sym=$1; tf=$2; mo=$3; outdir=$4
  SP=${RANKCHURN_SCRATCH:-/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/rankchurn}
  BASE="https://data.binance.vision/data/futures/um/monthly/klines"
  out="$SP/data/$outdir/${sym}-${tf}-${mo}.csv"
  [ -f "$out" ] && return
  url="$BASE/$sym/$tf/${sym}-${tf}-${mo}.zip"
  tmpzip="$SP/data/$outdir/${sym}-${tf}-${mo}.zip"
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
for sym in $SYMS_1H; do
  for mo in "${months[@]}"; do
    jobs+=("$sym|1h|$mo|klines1h")
  done
done
for sym in $SYMS_15M; do
  for mo in "${months[@]}"; do
    jobs+=("$sym|15m|$mo|klines15m")
  done
done

printf "%s\n" "${jobs[@]}" | xargs -P 16 -I{} bash -c '
  IFS="|" read -r sym tf mo outdir <<< "{}"
  fetch_one "$sym" "$tf" "$mo" "$outdir"
'
echo done
