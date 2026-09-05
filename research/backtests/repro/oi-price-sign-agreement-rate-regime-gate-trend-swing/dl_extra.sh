#!/bin/bash
# BTC 전용 추가 버퍼: 2021-01~2021-09 (365일 정규화 창을 IS 시작 시점부터 온전히 확보하기 위함)
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oisign
mkdir -p $SP/data/klines_4h_own $SP/data/metrics_own
SYM=BTCUSDT

for m in 01 02 03 04 05 06 07 08 09; do
  mo="2021-$m"
  out="$SP/data/klines_4h_own/${SYM}-4h-${mo}.csv"
  if [ ! -f "$out" ]; then
    url="https://data.binance.vision/data/futures/um/monthly/klines/$SYM/4h/${SYM}-4h-${mo}.zip"
    tmpzip="$SP/data/klines_4h_own/tmp_${mo}.zip"
    code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
    if [ "$code" == "200" ]; then
      unzip -p "$tmpzip" > "$out" 2>/dev/null
      rm -f "$tmpzip"
    else
      rm -f "$tmpzip"
      echo "MISS klines $mo ($code)"
    fi
  fi
done

for m in 01 02 03 04 05 06 07 08 09; do
  mo="2021-$m"
  out="$SP/data/metrics_own/${SYM}-metrics-${mo}.csv"
  if [ ! -f "$out" ]; then
    url="https://data.binance.vision/data/futures/um/monthly/metrics/$SYM/${SYM}-metrics-${mo}.zip"
    tmpzip="$SP/data/metrics_own/tmp_${mo}.zip"
    code=$(curl -s -o "$tmpzip" -w "%{http_code}" "$url")
    if [ "$code" == "200" ]; then
      unzip -p "$tmpzip" > "$out" 2>/dev/null
      rm -f "$tmpzip"
    else
      rm -f "$tmpzip"
      echo "MISS metrics-monthly $mo ($code)"
    fi
  fi
done
echo done
