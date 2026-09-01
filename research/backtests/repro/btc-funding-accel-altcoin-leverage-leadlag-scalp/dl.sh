#!/bin/bash
# btc-funding-accel-altcoin-leverage-leadlag-scalp 데이터 다운로드
# klines 15m, 1h + fundingRate (BTC만) 2022-01~2026-06, 7종목
set -uo pipefail
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/btcfundleadlag
DATA="$SP/data"
mkdir -p "$DATA/klines15m" "$DATA/klines1h" "$DATA/funding"

SYMBOLS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"

months() {
  for y in 2022 2023 2024 2025 2026; do
    for m in 01 02 03 04 05 06 07 08 09 10 11 12; do
      if [ "$y" = "2026" ] && [ "$m" -gt "06" ]; then continue; fi
      echo "$y-$m"
    done
  done
}

fetch_one() {
  local url="$1" out="$2"
  if [ -s "$out" ]; then return 0; fi
  local code
  code=$(curl -sS -o "$out.tmp" -w "%{http_code}" "$url")
  if [ "$code" = "200" ]; then
    mv "$out.tmp" "$out"
  else
    rm -f "$out.tmp"
    echo "MISS $code $url" >> "$SP/dl_missing.log"
  fi
}

for sym in $SYMBOLS; do
  for ym in $(months); do
    fetch_one "https://data.binance.vision/data/futures/um/monthly/klines/$sym/15m/$sym-15m-$ym.zip" "$DATA/klines15m/$sym-15m-$ym.zip"
    fetch_one "https://data.binance.vision/data/futures/um/monthly/klines/$sym/1h/$sym-1h-$ym.zip" "$DATA/klines1h/$sym-1h-$ym.zip"
  done
done

for ym in $(months); do
  fetch_one "https://data.binance.vision/data/futures/um/monthly/fundingRate/BTCUSDT/BTCUSDT-fundingRate-$ym.zip" "$DATA/funding/BTCUSDT-fundingRate-$ym.zip"
done

echo "DONE"
