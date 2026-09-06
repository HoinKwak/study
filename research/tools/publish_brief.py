#!/usr/bin/env python3
"""머지된 스테이징을 research/futures/brief.json 으로 발행한다.

사용: publish_brief.py <merged.json> <ts>

스키마(ts/market/cex/dex/themes)와 주식화 토큰 혼입만 확인하고 그대로 쓴다.
수치 검증은 발행 후 futures_check.py 가 맡는다.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

DST = Path(__file__).resolve().parents[1] / "futures" / "brief.json"
EQUITY = set("""NVDA SPY SOXL MU SNDK SKHYNIX SKHY TSLA AAPL AMZN META MSFT GOOG GOOGL COIN MSTR
HOOD PLTR AMD INTC NFLX QQQ IWM DIA GLD SLV USO UNG XAU XAG XAUUSD XAGUSD GOLD SILVER OIL WTI
BRENT NDX SPX DJI VIX EUR GBP JPY
SPCX CRCL TEAM MRVL AVGO GPRO SAMSUNG DELL BZ ORCL CRM ADBE UBER ABNB SHOP SQ PYPL BABA NKE
DIS BA JPM GS V MA WMT COST KO PEP XOM CVX LLY UNH JNJ PFE""".split())

# ⚠️(2026-09-06) build_digest와 같은 결함이 이 도구에도 있었다 — `SPX`를 S&P500
#   지수로 보고 발행을 막았는데 실제로는 $0.57짜리 밈코인 SPX6900이었다.
#   지수와 자릿수가 다른 티커는 가격 밴드로 갈라낸다(build_digest의 AMBIG_MIN과 동일).
AMBIG_MIN = {"SPX": 100.0, "NDX": 100.0, "DJI": 100.0, "VIX": 5.0}


def _eq(sym: str, px=None) -> bool:
    s = (sym or "").upper().split(":")[-1].lstrip("K")
    if s in AMBIG_MIN and px is not None:
        try:
            if float(px) < AMBIG_MIN[s]:
                return False
        except (TypeError, ValueError):
            pass
    return s in EQUITY



def main() -> int:
    d = json.loads(Path(sys.argv[1]).read_text())
    ts = sys.argv[2]
    d["ts"] = ts
    bad = [k for k in ("ts", "market", "cex", "dex", "themes") if k not in d]
    if bad:
        print(f"❌ 스키마 키 누락: {bad}")
        return 1
    eq = [e.get("symbol") for e in d["cex"] + d["dex"]
          if _eq((e.get("symbol") or ""), e.get("px") or e.get("price"))]
    if eq:
        print(f"❌ 주식화/상품 토큰 혼입: {eq}")
        return 1
    dup = {}
    for e in d["cex"] + d["dex"]:
        k = (e.get("symbol"), e.get("venue") or e.get("protocol"))
        dup[k] = dup.get(k, 0) + 1
    if any(v > 1 for v in dup.values()):
        print(f"❌ (심볼,벤뉴) 중복 {sum(v - 1 for v in dup.values() if v > 1)}건")
        return 1
    DST.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    print(f"발행 완료 · ts {ts} · cex {len(d['cex'])} · dex {len(d['dex'])} → {DST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
