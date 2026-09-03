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
EQUITY = set("""NVDA SPY SOXL MU SNDK SKHYNIX TSLA AAPL AMZN META MSFT GOOG GOOGL COIN MSTR
HOOD PLTR AMD INTC NFLX QQQ IWM DIA GLD SLV USO UNG XAU XAG XAUUSD XAGUSD GOLD SILVER OIL WTI
BRENT NDX SPX DJI VIX EUR GBP JPY""".split())


def main() -> int:
    d = json.loads(Path(sys.argv[1]).read_text())
    ts = sys.argv[2]
    d["ts"] = ts
    bad = [k for k in ("ts", "market", "cex", "dex", "themes") if k not in d]
    if bad:
        print(f"❌ 스키마 키 누락: {bad}")
        return 1
    eq = [e.get("symbol") for e in d["cex"] + d["dex"]
          if (e.get("symbol") or "").upper().split(":")[-1].lstrip("K") in EQUITY]
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
