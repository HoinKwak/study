#!/bin/bash
# 밈코인 3종 — Binance 선물 계약명이 1000배 표기(1000SHIBUSDT 등)임을 HTTP 200/404로 실측 확인 후
# 그 이름으로 1d klines monthly zip 다운로드.
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi_orig
SYMS="1000SHIBUSDT 1000PEPEUSDT 1000BONKUSDT"
mkdir -p $SP/data/klines_1d
months=()
for y in 2021; do for m in 10 11 12; do months+=("$y-$m"); done; done
for y in 2022 2023 2024 2025; do for m in $(seq -w 1 12); do months+=("$y-$m"); done; done
for m in $(seq -w 1 06); do months+=("2026-$m"); done
fetch_one() {
  sym=$1; mo=$2
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi_orig
  out="$SP/data/klines_1d/${sym}-1d-${mo}.csv"
  [ -f "$out" ] && return
  url="https://data.binance.vision/data/futures/um/monthly/klines/$sym/1d/${sym}-1d-${mo}.zip"
  tmpzip="$SP/data/klines_1d/${sym}-1d-${mo}.zip"
  code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
  if [ "$code" == "200" ]; then
    unzip -p "$tmpzip" > "$out" 2>/dev/null
    rm -f "$tmpzip"
  else
    rm -f "$tmpzip"
    echo "MISS $sym $mo ($code)" >> "$SP/data/klines_pool_missing.log"
  fi
}
export -f fetch_one
jobs=()
for sym in $SYMS; do for mo in "${months[@]}"; do jobs+=("$sym $mo"); done; done
printf "%s\n" "${jobs[@]}" | xargs -P 16 -I{} bash -c 'fetch_one {}'
echo done
