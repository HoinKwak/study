#!/bin/bash
# 진단 전용: 확장 유니버스(30종목 추가) 1h klines 다운로드 — n=7 degeneracy 가 유니버스 크기에
# 기인하는지 확인하는 보조 점검용(본 백테스트의 매매/게이트 산출에는 쓰지 않음).
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/rankchurn
mkdir -p "$SP"/data/klines1h_ext
SYMS="LTCUSDT LINKUSDT TRXUSDT MATICUSDT DOTUSDT AVAXUSDT UNIUSDT ATOMUSDT ETCUSDT FILUSDT NEARUSDT ALGOUSDT VETUSDT ICPUSDT FTMUSDT EOSUSDT XLMUSDT THETAUSDT EGLDUSDT XTZUSDT ZECUSDT DASHUSDT WAVESUSDT ONEUSDT HBARUSDT KSMUSDT RUNEUSDT SANDUSDT MANAUSDT GRTUSDT AAVEUSDT"

months=()
for y in 2022 2023 2024 2025; do
  for m in $(seq -w 1 12); do months+=("$y-$m"); done
done
for m in $(seq -w 1 07); do months+=("2026-$m"); done

fetch_one() {
  sym=$1; mo=$2
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/rankchurn
  BASE="https://data.binance.vision/data/futures/um/monthly/klines"
  out="$SP/data/klines1h_ext/${sym}-1h-${mo}.csv"
  [ -f "$out" ] && return
  url="$BASE/$sym/1h/${sym}-1h-${mo}.zip"
  tmpzip="$SP/data/klines1h_ext/${sym}-1h-${mo}.zip"
  code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
  if [ "$code" == "200" ]; then
    unzip -p "$tmpzip" > "$out" 2>/dev/null
    rm -f "$tmpzip"
  else
    rm -f "$tmpzip"
    echo "MISS $sym $mo ($code)" >> "$SP/data/klines1h_ext_missing.log"
  fi
}
export -f fetch_one
> "$SP/data/klines1h_ext_missing.log"

jobs=()
for sym in $SYMS; do
  for mo in "${months[@]}"; do
    jobs+=("$sym|$mo")
  done
done
printf "%s\n" "${jobs[@]}" | xargs -P 20 -I{} bash -c 'IFS="|" read -r sym mo <<< "{}"; fetch_one "$sym" "$mo"'
echo done
