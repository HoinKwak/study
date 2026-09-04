#!/bin/bash
# 1d/4h klines monthly zip 다운로드 (2022-01 ~ 2026-06, OOS_END=2026-06-30 23:59:59 커버)
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/altoibeta
SYMS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"

months=()
for y in 2022 2023 2024 2025; do
  for m in $(seq -w 1 12); do months+=("$y-$m"); done
done
for m in $(seq -w 1 06); do months+=("2026-$m"); done

fetch_one() {
  sym=$1; tf=$2; mo=$3
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/altoibeta
  out="$SP/data/klines${tf}/${sym}-${tf}-${mo}.csv"
  [ -f "$out" ] && return
  url="https://data.binance.vision/data/futures/um/monthly/klines/${sym}/${tf}/${sym}-${tf}-${mo}.zip"
  tmpzip="$SP/data/klines${tf}/${sym}-${tf}-${mo}.zip"
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

for sym in $SYMS; do
  for tf in 1d 4h; do
    for mo in "${months[@]}"; do
      echo "$sym $tf $mo"
    done
  done
done | xargs -P 16 -I{} bash -c 'set -- {}; fetch_one "$1" "$2" "$3"' _ {}
echo done
