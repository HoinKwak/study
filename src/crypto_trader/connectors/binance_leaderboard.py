"""바이낸스 선물 리더보드 상위 트레이더 현재 포지션 커넥터.

바이낸스 공개(비공식) 리더보드 API로 통산 PnL·ROI 상위 트레이더를 뽑고, 포지션 공유(sharer)
트레이더의 현재 포지션을 조회한다. Hyperliquid 커넥터와 동일한 bundle 구조로 대시보드가 사용.

⚠️ 이 개발 컨테이너에선 바이낸스가 지역차단(451/restricted)이라 **실행 검증 불가**.
   사장님 로컬 PC(대시보드 구동 환경)에선 정상 동작. 구조는 문서화된 비공식 API를 따름.

엔드포인트(POST, JSON):
- .../leaderboard/getLeaderboardRank  : 상위 트레이더(encryptedUid,nickName,pnl,roi,positionShared)
- .../leaderboard/getOtherPosition     : 특정 트레이더 현재 포지션(공유자만)
필터: 통산 PnL≥$100K & ROI≥50% (리더보드 제공값 그대로). 포지션은 5대 메이저만.
"""
from __future__ import annotations

import json
import urllib.request

_BASE = "https://www.binance.com/bapi/futures/v1/public/future/leaderboard"
_HDR = {"User-Agent": "Mozilla/5.0", "Content-Type": "application/json", "Accept": "*/*"}

MIN_PNL = 100_000.0
MIN_ROI = 0.50
DIRECTIONAL_MIN = 0.85
# 바이낸스 선물 심볼(5대 메이저)
MAJORS = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "XRPUSDT", "BNBUSDT")
_MAJOR_LABEL = {"BTCUSDT": "BTC", "ETHUSDT": "ETH", "SOLUSDT": "SOL", "XRPUSDT": "XRP", "BNBUSDT": "BNB"}


def _post(path: str, body: dict) -> dict:
    req = urllib.request.Request(_BASE + path, data=json.dumps(body).encode(), headers=_HDR)
    with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310
        return json.load(r)


def fetch_leaderboard(statistics: str = "PNL") -> list[dict]:
    """통산(ALL) 리더보드 상위 트레이더. statistics: PNL|ROI."""
    body = {"isShared": True, "isTrader": False, "periodType": "ALL",
            "statisticsType": statistics, "tradeType": "PERPETUAL"}
    d = _post("/getLeaderboardRank", body)
    return (d.get("data") or []) if isinstance(d, dict) else []


def screen(rows: list[dict], min_pnl: float = MIN_PNL, min_roi: float = MIN_ROI) -> list[dict]:
    out = []
    for r in rows:
        pnl = float(r.get("pnl") or 0.0)
        roi = float(r.get("roi") or 0.0)   # 바이낸스 roi는 소수(0.5=50%)
        if pnl < min_pnl or roi < min_roi:
            continue
        out.append({
            "uid": r.get("encryptedUid"), "name": r.get("nickName"),
            "pnl": pnl, "roi": roi, "shared": bool(r.get("positionShared")),
        })
    out.sort(key=lambda x: -x["pnl"])
    return out


def fetch_positions(uid: str, only: tuple = MAJORS) -> list[dict]:
    """공유 트레이더의 현재 포지션(5대 메이저만)."""
    d = _post("/getOtherPosition", {"encryptedUid": uid, "tradeType": "PERPETUAL"})
    data = d.get("data") or {}
    rows = data.get("otherPositionRetList") or []
    positions = []
    for p in rows:
        sym = p.get("symbol")
        amt = float(p.get("amount") or 0.0)
        if amt == 0 or (only and sym not in only):
            continue
        entry = float(p["entryPrice"]) if p.get("entryPrice") else None
        mark = float(p["markPrice"]) if p.get("markPrice") else None
        positions.append({
            "coin": _MAJOR_LABEL.get(sym, sym),
            "side": "long" if amt > 0 else "short",
            "size": abs(amt),
            "entry": entry,
            "notional": abs(amt) * (mark or entry or 0.0),
            "upnl": float(p.get("pnl") or 0.0),
            "leverage": p.get("leverage"),
            "liquidation": None,          # 리더보드 API 미제공
            "roe": float(p["roe"]) if p.get("roe") else None,
            "entry_ts": p.get("updateTimeStamp"),   # 공유 갱신시각(정확한 진입시각 아님)
        })
    positions.sort(key=lambda x: -x["notional"])
    return positions


def build_bundle(limit: int = 20) -> dict:
    """대시보드용 묶음(Hyperliquid와 동일 구조). 지역차단 환경에선 빈 결과."""
    traders = []
    try:
        cand = screen(fetch_leaderboard("PNL"))
    except Exception:  # noqa: BLE001  (지역차단 등)
        cand = []
    for t in cand:
        if not t["shared"]:
            continue
        try:
            ps = fetch_positions(t["uid"])
        except Exception:  # noqa: BLE001
            continue
        if not ps:
            continue
        long_ntl = sum(p["notional"] for p in ps if p["side"] == "long")
        short_ntl = sum(p["notional"] for p in ps if p["side"] == "short")
        gross = long_ntl + short_ntl
        if gross <= 0 or max(long_ntl, short_ntl) / gross < DIRECTIONAL_MIN:
            continue
        traders.append({
            "addr": t["uid"], "name": t.get("name"),
            "pnl": t["pnl"], "roi": t["roi"],
            "net_side": "long" if long_ntl >= short_ntl else "short",
            "account_value": None, "recent_pnl": None, "max_lev": None,
            "pnl_history": None, "positions": ps,
        })
        if len(traders) >= limit:
            break
    return {
        "source": "binance",
        "filter": {"min_pnl": MIN_PNL, "min_roi": MIN_ROI, "coins": [_MAJOR_LABEL[m] for m in MAJORS]},
        "count": len(traders), "traders": traders,
    }


if __name__ == "__main__":
    b = build_bundle(limit=10)
    print(f"[Binance] 통과 {b['count']}명 (지역차단 환경이면 0)")
    for t in b["traders"]:
        print(f"  {(t.get('name') or t['addr'])[:16]} PnL ${t['pnl']:,.0f} ROI {t['roi']*100:.0f}% 포지션 {len(t['positions'])}")
