#!/bin/bash
# metrics 일별 zip 다운로드 (2021-10-01 ~ 2026-06-30). daily 파일 형식만 존재.
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi
SYMS="BTCUSDT ETHUSDT BNBUSDT SOLUSDT XRPUSDT DOGEUSDT ADAUSDT"
mkdir -p $SP/data/metrics

fetch_one() {
  sym=$1; day=$2
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi
  out="$SP/data/metrics/${sym}-metrics-${day}.csv"
  [ -f "$out" ] && return
  url="https://data.binance.vision/data/futures/um/daily/metrics/$sym/${sym}-metrics-${day}.zip"
  tmpzip="$SP/data/metrics/${sym}-metrics-${day}.zip"
  code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
  if [ "$code" == "200" ]; then
    unzip -p "$tmpzip" > "$out" 2>/dev/null
    rm -f "$tmpzip"
  else
    rm -f "$tmpzip"
    echo "MISS $sym $day ($code)" >> "$SP/data/metrics_missing.log"
  fi
}
export -f fetch_one

python3 -c "
import datetime
d = datetime.date(2021,10,1)
end = datetime.date(2026,6,30)
days = []
while d <= end:
    days.append(d.isoformat())
    d += datetime.timedelta(days=1)
print('\n'.join(days))
" > $SP/days.txt

jobs=()
for sym in $SYMS; do
  while read -r day; do
    jobs+=("$sym $day")
  done < $SP/days.txt
done
printf "%s\n" "${jobs[@]}" | xargs -P 24 -I{} bash -c 'fetch_one {}'
echo done
