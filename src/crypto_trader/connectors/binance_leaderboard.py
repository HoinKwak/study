"""바이낸스 스마트머니(신 리더보드) 상위 트레이더 커넥터 — 공개 데이터 전용.

2026-07 개편으로 선물 리더보드가 'smart-money'로 바뀌었다. **목록/프로필은 공개(비인증)**로
통산 PnL·ROI·계좌자산(assets)·MDD·구독자·PnL곡선(chart)을 주지만, **현재 포지션 상세
(query-positions)는 로그인 필요(HTTP 401 "Please log in first")**라 비인증으로는 못 가져온다.
→ 이 커넥터는 '포지션 없는 상위 트레이더 실적 카드'만 제공한다(포지션은 온체인 공개인
Hyperliquid에서 확인). 대시보드 두 패널(상위/라이징스타)에 맞춰 top·rising 두 리스트를 준다.

- 목록: GET bapi/futures/v1/friendly/future/smart-money/top-trader/list?timeRange=&rankingType=&...
  값은 선택 창(예: 30D) 기준 — **통산(lifetime)이 아니라 최근 창 실적**임에 주의.
- ⚠️ 개발 컨테이너는 바이낸스 지역차단(451)이라 로컬 대시보드에서만 동작(서버 모드).
"""
from __future__ import annotations

import json
import urllib.request

_LIST = "https://www.binance.com/bapi/futures/v1/friendly/future/smart-money/top-trader/list"
# 비인증 최소 헤더(진단으로 HTTP 200 확인). 로그인 쿠키 미사용.
_H = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Accept": "*/*",
      "clienttype": "web", "content-type": "application/json", "lang": "en", "bnc-location": "KR"}

MIN_ACCOUNT = 10_000.0   # 계좌자산(assets) 하한 — 먼지계좌·고ROI 눈속임 배제
TIME_RANGE = "30D"       # 스마트머니는 창(window) 기준 실적. 30D 확인됨.
TOP_LIMIT = 20           # 좌측(상위=PnL 상위)
RISING_LIMIT = 12        # 우측(라이징스타=ROI 상위)
MAJORS = ("BTC", "ETH", "SOL", "XRP", "BNB")


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers=_H)
    with urllib.request.urlopen(req, timeout=25) as r:  # noqa: S310
        return json.load(r)


def fetch_list(ranking: str = "PNL", time_range: str = TIME_RANGE, rows: int = 60) -> list[dict]:
    """스마트머니 목록(공개). ranking: PNL|ROI. time_range 창 기준 실적."""
    qs = (f"?page=1&rows={rows}&timeRange={time_range}&rankingType={ranking}"
          f"&onlyShowSharingPosition=false&onlyShowSignalEnabled=false&order=DESC")
    d = _get(_LIST + qs)
    data = d.get("data") or {}
    return (data.get("rows") or []) if isinstance(data, dict) else []


def _trader(r: dict) -> dict:
    """목록 행 → 대시보드 트레이더 dict(포지션 없음). chart.items → pnl_history(스파크라인)."""
    items = (r.get("chart") or {}).get("items") or []
    hist = [[int(ts), float(v)] for ts, v in items] if len(items) >= 2 else None
    mdd = r.get("mdd")
    return {
        "addr": str(r.get("topTraderId") or ""),
        "name": r.get("traderName") or r.get("accountName"),
        "pnl": float(r.get("pnl") or 0.0), "roi": float(r.get("roi") or 0.0),
        "account_value": float(r.get("assets") or 0.0),
        "mdd": float(mdd) if mdd is not None else None,
        "subscribers": r.get("subscribers"),
        "position_status": r.get("positionStatus"),
        "pnl_history": hist,
        "positions": [],            # 포지션 상세 = 로그인 필요(비공개)
        "net_side": None, "max_lev": None, "recent_pnl": None,
        "profile_url": None,        # 신 스마트머니 공개 프로필 URL 불확실 → 이름만 표시
    }


def _rank(ranking: str, limit: int) -> list[dict]:
    """랭킹별 상위 트레이더(계좌자산≥MIN_ACCOUNT·PnL>0). 지역차단 등 실패 시 빈 리스트."""
    try:
        rows = fetch_list(ranking=ranking)
    except Exception:  # noqa: BLE001  (지역차단 451 등)
        return []
    out: list[dict] = []
    for r in rows:
        if float(r.get("assets") or 0.0) < MIN_ACCOUNT or float(r.get("pnl") or 0.0) <= 0:
            continue
        out.append(_trader(r))
        if len(out) >= limit:
            break
    return out


def build_bundle(top_limit: int = TOP_LIMIT, rising_limit: int = RISING_LIMIT) -> dict:
    """공개 목록으로 top(최근 PnL 상위)·rising(최근 ROI 상위) 두 리스트. 포지션은 비공개."""
    top = _rank("PNL", top_limit)
    rising = _rank("ROI", rising_limit)
    return {
        "source": "binance",
        "summary": [],   # 포지션 비공개 → 코인별 집계 없음
        "filter": {
            "window": TIME_RANGE, "min_account": MIN_ACCOUNT, "coins": list(MAJORS),
            "note": "스마트머니는 창(window) 실적 기준 · 포지션 상세는 로그인 필요로 비공개",
        },
        "top": top, "rising": rising,
        "count": len(top) + len(rising),
        "traders": top,   # 하위호환
    }


if __name__ == "__main__":
    b = build_bundle()
    print(f"[Binance smart-money] top {len(b['top'])} · rising {len(b['rising'])} (지역차단 환경이면 0)")
    for t in b["top"][:5]:
        print(f"  {(t.get('name') or t['addr'])[:18]:18} PnL ${t['pnl']:,.0f} "
              f"ROI {t['roi']*100:.0f}% 자산 ${t['account_value']:,.0f} {t['position_status']}")
