#!/bin/bash
# metrics 일별 zip 다운로드 (2022-01-01 ~ 2026-06-30), 병렬 xargs.
# ⚠️ 이번 라운드는 실제로는 이 스크립트를 실행하지 않고, 이전 라운드(oiskew)가 이미 동일 필드·
#   동일 기간·동일 유니버스로 추출해둔 CSV 캐시(scratchpad/oiskew/data/metrics)를 읽기전용으로
#   재사용했다(common.py 의 OIRESID_METRICS_DIR). 캐시가 없으면 아래로 새로 받는다.
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiresid
BASE="https://data.binance.vision/data/futures/um/daily/metrics"
SYMS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"
mkdir -p $SP/data/metrics
> $SP/data/metrics_jobs.txt

python3 - <<'PY' >> $SP/data/metrics_jobs.txt
import datetime
d0 = datetime.date(2022,1,1)
d1 = datetime.date(2026,6,30)
d = d0
while d <= d1:
    print(d.isoformat())
    d += datetime.timedelta(days=1)
PY

fetch_one() {
  sym=$1; date=$2
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiresid
  out="$SP/data/metrics/${sym}-metrics-${date}.csv"
  [ -f "$out" ] && return
  url="https://data.binance.vision/data/futures/um/daily/metrics/${sym}/${sym}-metrics-${date}.zip"
  tmpzip="$SP/data/metrics/${sym}-metrics-${date}.zip"
  code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
  if [ "$code" == "200" ]; then
    unzip -p "$tmpzip" > "$out" 2>/dev/null
    rm -f "$tmpzip"
  else
    rm -f "$tmpzip"
    echo "MISS $sym $date ($code)" >> "$SP/data/metrics_missing.log"
  fi
}
export -f fetch_one

for sym in $SYMS; do
  cat $SP/data/metrics_jobs.txt | xargs -P 16 -I{} bash -c 'fetch_one "$1" "$2"' _ "$sym" {}
done
echo done
