#!/bin/bash
# 후보 알트 풀(밈코인 제외) 1d klines monthly zip 다운로드 (2021-10~2026-06)
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi_orig
SYMS="MATICUSDT DOTUSDT LTCUSDT LINKUSDT AVAXUSDT ATOMUSDT UNIUSDT FILUSDT ETCUSDT XLMUSDT ICPUSDT NEARUSDT TRXUSDT BCHUSDT VETUSDT ALGOUSDT AAVEUSDT SANDUSDT MANAUSDT AXSUSDT FTMUSDT GRTUSDT EOSUSDT XTZUSDT THETAUSDT EGLDUSDT GALAUSDT CHZUSDT DYDXUSDT RUNEUSDT LDOUSDT INJUSDT APTUSDT ARBUSDT OPUSDT SUIUSDT WLDUSDT SEIUSDT TIAUSDT ORDIUSDT JUPUSDT RENDERUSDT FETUSDT ONDOUSDT PYTHUSDT HBARUSDT TONUSDT"
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
  [ -L "$out" ] && return
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
for sym in $SYMS; do
  for mo in "${months[@]}"; do
    jobs+=("$sym $mo")
  done
done
echo "총 요청 수: ${#jobs[@]}"
printf "%s\n" "${jobs[@]}" | xargs -P 24 -I{} bash -c 'fetch_one {}'
echo done
