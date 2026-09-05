#!/bin/bash
# gen_metrics_jobs.py 가 생성한 "symbol day" 목록(인자 $1)을 받아 OI metrics(5분, 일별 zip)
# 다운로드. 이미 존재/심볼릭링크된 파일은 건너뜀(기존 7종목 캐시 재사용).
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi_orig
mkdir -p $SP/data/metrics

fetch_one() {
  sym=$1; day=$2
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi_orig
  out="$SP/data/metrics/${sym}-metrics-${day}.csv"
  [ -f "$out" ] && return
  [ -L "$out" ] && return
  url="https://data.binance.vision/data/futures/um/daily/metrics/$sym/${sym}-metrics-${day}.zip"
  tmpzip="$SP/data/metrics/${sym}-metrics-${day}.zip.tmp$$"
  code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
  if [ "$code" == "200" ]; then
    unzip -p "$tmpzip" > "$out" 2>/dev/null
    rm -f "$tmpzip"
  else
    rm -f "$tmpzip"
    echo "MISS $sym $day ($code)" >> "$SP/data/metrics_pool_missing.log"
  fi
}
export -f fetch_one
cat "$1" | xargs -P 32 -I{} bash -c 'fetch_one {}'
echo done
