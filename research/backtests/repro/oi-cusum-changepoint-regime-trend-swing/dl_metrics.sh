#!/bin/bash
# metrics 일별 zip 병렬 다운로드 (2022-01-01 ~ 2026-06-30)
SP="${OICUSUM_SCRATCH:-/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oicusum_q7z2}"
BASE="https://data.binance.vision/data/futures/um/daily/metrics"
SYMS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"
mkdir -p "$SP/data/metrics"
JOBS="$SP/data/metrics_jobs.txt"
> "$JOBS"

python3 - << 'PY' >> "$JOBS"
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
  SP="${OICUSUM_SCRATCH:-/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oicusum_q7z2}"
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
  cat "$JOBS" | xargs -P 16 -I{} bash -c 'fetch_one "$1" "$2"' _ "$sym" {}
done
echo done
