#!/bin/bash
# 1h/15m klines monthly zip 다운로드 (2021-09 ~ 2026-06, phi_window=30d+pctile_window=90d
# 워밍업 확보를 위해 IS_START(2022-01-01)보다 앞서 2021-09부터 수신, OOS_END=2026-06-30 커버)
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiar1hl
SYMS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"
TFS="1h 15m"
mkdir -p $SP/data/klines_1h $SP/data/klines_15m

months=()
for y in 2021; do
  for m in 09 10 11 12; do months+=("$y-$m"); done
done
for y in 2022 2023 2024 2025; do
  for m in $(seq -w 1 12); do months+=("$y-$m"); done
done
for m in $(seq -w 1 06); do months+=("2026-$m"); done

fetch_one() {
  sym=$1; tf=$2; mo=$3
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiar1hl
  dirn="klines_1h"; [ "$tf" == "15m" ] && dirn="klines_15m"
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
