#!/usr/bin/env bash
# 선물 브리핑 원자료 수신 — 6개 벤뉴 9개 피드.
# ⚠️2026-09-03 컨테이너 재시작으로 스크래치패드가 통째로 비워지면서 이 파이프라인
#   전체가 유실됐다(저장소에 없었기 때문). 그래서 이번부터 research/tools/ 에 둔다.
# 빌더가 기대하는 파일명으로 직접 저장한다(과거에 파일명이 어긋나 빌더가 직전 회차
#   파일을 읽어 chg24가 통째로 동결된 사고가 있었다).
set -u
OUT="${1:-$(pwd)}"; mkdir -p "$OUT"; ok=0; fail=0
# ⚠️2026-09-03: JSON 파싱만으로는 부족하다. CoinGecko가 429(rate limit)를 반환하면
#   그것도 유효한 JSON이라 "OK"로 통과했고, Aster 60종목이 통째로 빠진 채 다이제스트가
#   만들어졌다. 그래서 기대 필드(`want`)가 실제로 있는지까지 확인하고, 없으면 재시도한다.
_get () { # url outfile [post-data] [기대 필드]
  local u="$1" f="$2" d="${3:-}" want="${4:-}"
  for i in 1 2 3 4; do
    if [ -n "$d" ]; then curl -sS -m 40 -X POST "$u" -H 'Content-Type: application/json' -d "$d" -o "$OUT/$f"
    else curl -sS -m 40 "$u" -H 'User-Agent: curl/8' -o "$OUT/$f"; fi
    if python3 - "$OUT/$f" "$want" <<'PYV' 2>/dev/null
import json,sys
d=json.load(open(sys.argv[1])); want=sys.argv[2]
if want:
    v=d.get(want) if isinstance(d,dict) else None
    sys.exit(0 if v else 1)
sys.exit(0)
PYV
    then echo "  $f OK"; ok=$((ok+1)); return; fi
    sleep $((i*5))
  done
  echo "  $f 실패(기대 필드 '$want' 없음 — rate limit 가능)"; fail=$((fail+1))
}
echo "[1/9] OKX 티커";      _get "https://www.okx.com/api/v5/market/tickers?instType=SWAP" okx_raw.json '' data
echo "[2/9] OKX OI";        _get "https://www.okx.com/api/v5/public/open-interest?instType=SWAP" okx_oi.json '' data
echo "[3/9] Binance(CG)";   _get "https://api.coingecko.com/api/v3/derivatives/exchanges/binance_futures?include_tickers=all" cg_binance_futures.json '' tickers
echo "[4/9] Bybit(CG)";     _get "https://api.coingecko.com/api/v3/derivatives/exchanges/bybit?include_tickers=all" cg_bybit.json '' tickers
echo "[5/9] Aster(CG)";     _get "https://api.coingecko.com/api/v3/derivatives/exchanges/aster?include_tickers=all" cg_aster.json '' tickers
echo "[6/9] Hyperliquid";   _get "https://api.hyperliquid.xyz/info" hl_raw.json '{"type":"metaAndAssetCtxs"}'
echo "[7/9] HyENA";         _get "https://api.hyperliquid.xyz/info" hyna_raw.json '{"type":"metaAndAssetCtxs","dex":"hyna"}'
echo "[8/9] dYdX";          _get "https://indexer.dydx.trade/v4/perpetualMarkets" dydx_raw.json '' markets
echo "[9/9] OKX 펀딩(개별 조회)"
python3 - "$OUT" <<'PY'
import json,sys,urllib.request,time
out=sys.argv[1]
t=json.load(open(out+'/okx_raw.json')).get('data',[])
ids=[x['instId'] for x in t if x['instId'].endswith('-USDT-SWAP')]
# ⚠️volCcy24h는 코인 수량이라 이것만으로 정렬하면 SATS·PEPE·SHIB 같은 저가 코인이
#   상위를 차지하고 BTC·ETH가 60위 밖으로 밀린다(9/3 실제 발생). last를 곱해 달러로 정렬한다.
_v={x['instId']:float(x.get('volCcy24h') or 0)*float(x.get('last') or 0) for x in t}
ids=sorted(ids,key=lambda i:-_v.get(i,0))[:60]
res={}
for i in ids:
    try:
        u=f"https://www.okx.com/api/v5/public/funding-rate?instId={i}"
        d=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'curl/8'}),timeout=15))
        if d.get('data'): res[i]=d['data'][0]
    except Exception: pass
    time.sleep(0.05)
json.dump(res,open(out+'/okx_funding.json','w'))
print(f"  OKX 펀딩 {len(res)}/{len(ids)} 확보")
PY
echo "수신 성공 $ok · 실패 $fail"
echo "--- 신선도 ---"
for f in okx_raw okx_oi okx_funding cg_binance_futures cg_bybit cg_aster hl_raw hyna_raw dydx_raw; do
  [ -f "$OUT/$f.json" ] && echo "  $f $(date -u -r "$OUT/$f.json" +%H:%M:%SZ)"
done
