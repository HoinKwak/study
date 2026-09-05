#!/bin/bash
# BTC 전용 metrics 일별 zip 추가 다운로드 (2021-01-01 ~ 2021-09-30, 365일 정규화 창 버퍼용)
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oisign
SYM=BTCUSDT
mkdir -p $SP/data/metrics_own

fetch_one() {
  day=$1
  SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oisign
  SYM=BTCUSDT
  out="$SP/data/metrics_own/${SYM}-metrics-${day}.csv"
  [ -f "$out" ] && return
  url="https://data.binance.vision/data/futures/um/daily/metrics/$SYM/${SYM}-metrics-${day}.zip"
  tmpzip="$SP/data/metrics_own/${SYM}-metrics-${day}.zip"
  code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
  if [ "$code" == "200" ]; then
    unzip -p "$tmpzip" > "$out" 2>/dev/null
    rm -f "$tmpzip"
  else
    rm -f "$tmpzip"
    echo "MISS $SYM $day ($code)" >> "$SP/data/metrics_own_missing.log"
  fi
}
export -f fetch_one

python3 -c "
import datetime
d = datetime.date(2021,1,1)
end = datetime.date(2021,9,30)
days = []
while d <= end:
    days.append(d.isoformat())
    d += datetime.timedelta(days=1)
print('\n'.join(days))
" > $SP/days_extra.txt

printf "%s\n" $(cat $SP/days_extra.txt) | xargs -P 24 -I{} bash -c 'fetch_one {}'
echo done
