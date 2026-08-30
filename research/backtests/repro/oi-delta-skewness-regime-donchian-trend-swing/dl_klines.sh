#!/bin/bash
# 4h klines monthly zip 다운로드 (2022-01 ~ 2026-07, OOS 상한 확보 위해 07월도 포함)
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiskew
BASE="https://data.binance.vision/data/futures/um/monthly/klines"
SYMS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"
mkdir -p $SP/data/klines

months=()
for y in 2022 2023 2024 2025; do
  for m in $(seq -w 1 12); do months+=("$y-$m"); done
done
for m in $(seq -w 1 07); do months+=("2026-$m"); done

for sym in $SYMS; do
  for mo in "${months[@]}"; do
    out="$SP/data/klines/${sym}-4h-${mo}.csv"
    [ -f "$out" ] && continue
    url="$BASE/$sym/4h/${sym}-4h-${mo}.zip"
    tmpzip="$SP/data/klines/${sym}-4h-${mo}.zip"
    code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
    if [ "$code" == "200" ]; then
      unzip -p "$tmpzip" > "$out" 2>/dev/null
      rm -f "$tmpzip"
    else
      rm -f "$tmpzip"
      echo "MISS $sym $mo ($code)" >> $SP/data/klines_missing.log
    fi
  done
done
echo done
