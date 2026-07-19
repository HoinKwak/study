"""Hyperliquid 리더보드 상위 트레이더 현재 포지션 커넥터.

공개 API(키 불필요)로 리더보드를 받아 필터(lifetime PnL·ROI + 최근 거래·수익성)를 통과한
상위 트레이더를 뽑고, 각자의 현재 열린 포지션을 조회한다. 대시보드 '리더보드 포지션' 섹션이 사용.

- 리더보드: https://stats-data.hyperliquid.xyz/Mainnet/leaderboard (windowPerformances=day/week/month/allTime)
- 포지션:   POST https://api.hyperliquid.xyz/info  {"type":"clearinghouseState","user":addr}
프록시: HTTPS_PROXY 환경변수를 urllib가 자동 사용.
"""
from __future__ import annotations

import json
import urllib.request

_LB_URL = "https://stats-data.hyperliquid.xyz/Mainnet/leaderboard"
_INFO_URL = "https://api.hyperliquid.xyz/info"
_UA = {"User-Agent": "leaderboard-positions/0.1", "Content-Type": "application/json"}

# 필터 기본값 (사장님 결정: lifetime PnL≥$100K, ROI≥50%, 최근 거래·수익성, 지갑≥$10K)
MIN_PNL = 100_000.0
MIN_ROI = 0.50
MIN_ACCOUNT = 10_000.0   # 현재 계좌가치 최소($2~3 청산계좌 배제)


def _get(url: str) -> dict | list:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310
        return json.load(r)


def _post(url: str, payload: dict) -> dict:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=_UA)
    with urllib.request.urlopen(req, timeout=20) as r:  # noqa: S310
        return json.load(r)


def _window(perfs: list, name: str) -> dict:
    """windowPerformances 리스트에서 특정 창(day/week/month/allTime) dict 반환."""
    for w, v in perfs:
        if w == name:
            return {"pnl": float(v["pnl"]), "roi": float(v["roi"]), "vlm": float(v["vlm"])}
    return {"pnl": 0.0, "roi": 0.0, "vlm": 0.0}


def fetch_leaderboard() -> list[dict]:
    """리더보드 원본 행 리스트."""
    d = _get(_LB_URL)
    return d["leaderboardRows"] if isinstance(d, dict) else list(d)


def screen(
    rows: list[dict],
    min_pnl: float = MIN_PNL,
    min_roi: float = MIN_ROI,
    min_account: float = MIN_ACCOUNT,
    require_active: bool = True,
) -> list[dict]:
    """1차 필터(리더보드만으로): lifetime PnL·ROI + 지갑사이즈 + 최근 거래활동. PnL 상위 정렬.

    require_active=True 이면 최근 한 달 실거래(month vlm>0)도 요구('최근 거래').
    최근 '수익성'(3개월)은 리더보드에 3M 창이 없어 여기서 못 걸러 — 2차(portfolio)에서 90일 PnL로.
    """
    out: list[dict] = []
    for r in rows:
        perfs = r.get("windowPerformances") or []
        allt = _window(perfs, "allTime")
        month = _window(perfs, "month")
        acct = float(r.get("accountValue") or 0.0)
        if allt["pnl"] < min_pnl or allt["roi"] < min_roi:
            continue
        if acct < min_account:          # 지갑 사이즈 최소
            continue
        if require_active and month["vlm"] <= 0:
            continue
        out.append({
            "addr": r["ethAddress"],
            "name": r.get("displayName"),
            "account_value": float(r.get("accountValue") or 0.0),
            "pnl": allt["pnl"], "roi": allt["roi"],
            "month_pnl": month["pnl"], "month_vlm": month["vlm"],
        })
    out.sort(key=lambda x: -x["pnl"])
    return out


def pnl_over_days(addr: str, days: int = 90) -> float | None:
    """portfolio allTime 누적 pnlHistory에서 최근 `days`일 PnL(=누적 최신−누적 days일전)."""
    try:
        d = _post(_INFO_URL, {"type": "portfolio", "user": addr})
    except Exception:  # noqa: BLE001
        return None
    wins = dict(d) if isinstance(d, list) else {}
    hist = (wins.get("allTime") or {}).get("pnlHistory") or []
    if len(hist) < 2:
        return None
    last_ts, last_v = hist[-1][0], float(hist[-1][1])
    cut = last_ts - days * 86400 * 1000
    prior = [p for p in hist if p[0] <= cut]
    base = float(prior[-1][1]) if prior else float(hist[0][1])
    return last_v - base


def fetch_positions(addr: str) -> dict:
    """주소의 현재 계좌·열린 포지션."""
    d = _post(_INFO_URL, {"type": "clearinghouseState", "user": addr})
    ms = d.get("marginSummary", {})
    positions = []
    for ap in d.get("assetPositions", []):
        p = ap.get("position", {})
        szi = float(p.get("szi") or 0.0)
        if szi == 0:
            continue
        positions.append({
            "coin": p.get("coin"),
            "side": "long" if szi > 0 else "short",
            "size": abs(szi),
            "entry": float(p["entryPx"]) if p.get("entryPx") else None,
            "notional": float(p.get("positionValue") or 0.0),
            "upnl": float(p.get("unrealizedPnl") or 0.0),
            "leverage": (p.get("leverage") or {}).get("value"),
            "roe": float(p["returnOnEquity"]) if p.get("returnOnEquity") else None,
        })
    positions.sort(key=lambda x: -x["notional"])
    return {
        "account_value": float(ms.get("accountValue") or 0.0),
        "total_notional": float(ms.get("totalNtlPos") or 0.0),
        "positions": positions,
    }


def top_traders_with_positions(
    limit: int = 25, scan: int = 100, recent_days: int = 90, **kw
) -> list[dict]:
    """필터 통과 상위에서 (최근 `recent_days`일 수익성>0) & (열린 포지션 있음) 트레이더 limit개까지.

    scan: 2차 조회 최대 스캔 수(API 호출 상한). 3개월 수익성은 하락장 감안해 기본 90일.
    """
    cand = screen(fetch_leaderboard(), **kw)
    out: list[dict] = []
    for t in cand[:scan]:
        rp = pnl_over_days(t["addr"], days=recent_days)
        if rp is None or rp <= 0:          # 최근 수익성(3개월) 필터
            continue
        try:
            pos = fetch_positions(t["addr"])
        except Exception:  # noqa: BLE001
            continue
        if not pos["positions"]:           # 현재 열린 포지션 있는 트레이더만
            continue
        out.append({**t, **pos, "recent_pnl": rp, "recent_days": recent_days})
        if len(out) >= limit:
            break
    return out


def build_bundle(limit: int = 25, recent_days: int = 90) -> dict:
    """대시보드용 묶음: 필터 조건 + 상위 트레이더 포지션."""
    traders = top_traders_with_positions(limit=limit, recent_days=recent_days)
    return {
        "source": "hyperliquid",
        "filter": {
            "min_pnl": MIN_PNL, "min_roi": MIN_ROI, "min_account": MIN_ACCOUNT,
            "recent_trading": True, "recent_profit_days": recent_days,
        },
        "count": len(traders),
        "traders": traders,
    }


if __name__ == "__main__":
    b = build_bundle(limit=10)
    print(f"[Hyperliquid] 필터(PnL≥$100K·ROI≥50%·최근거래·90일수익성>0)·포지션보유 상위 {b['count']}명\n")
    for t in b["traders"]:
        print(f"{t['addr'][:10]}… PnL ${t['pnl']:,.0f} ROI {t['roi']*100:.0f}% "
              f"90d ${t['recent_pnl']:,.0f} | 계좌 ${t['account_value']:,.0f} | 포지션 {len(t['positions'])}개")
        for p in t["positions"][:4]:
            print(f"    {p['coin']:7} {p['side']:5} ${p['notional']:,.0f} "
                  f"진입 {p['entry']} uPnL ${p['upnl']:,.0f} {p['leverage']}x")
