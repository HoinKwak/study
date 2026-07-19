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
MAJORS = ("BTC", "ETH", "SOL", "XRP", "BNB")   # 포지션 표시 대상(5대 메이저만)
DIRECTIONAL_MIN = 0.85   # 지배방향 비중 하한(미만=양방향/헤지 북 → 제외)
MAX_LEV = 25.0           # 포지션 최대 레버리지 상한(초과=고배율 ROI 눈속임 → 제외)


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
        if allt["pnl"] < min_pnl or allt["roi"] < min_roi:
            continue
        # 지갑 사이즈(min_account)는 리더보드 accountValue가 스테일할 수 있어 여기서 안 거르고
        # 2차(clearinghouseState 실시간 계좌가치)에서 엄격 적용 — top_traders_with_positions 참조.
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


def fetch_portfolio(addr: str, days: int = 90, max_points: int = 60) -> dict | None:
    """portfolio allTime 누적 pnlHistory에서 최근 `days`일 PnL + 역대 시계열(다운샘플).

    반환 {"pnl_recent": 최근days일 PnL, "history": [[ts_ms, 누적PnL], ...]}.
    """
    try:
        d = _post(_INFO_URL, {"type": "portfolio", "user": addr})
    except Exception:  # noqa: BLE001
        return None
    wins = dict(d) if isinstance(d, list) else {}
    hist = (wins.get("allTime") or {}).get("pnlHistory") or []
    if len(hist) < 2:
        return None
    series = [[int(ts), float(v)] for ts, v in hist]
    last_ts, last_v = series[-1]
    cut = last_ts - days * 86400 * 1000
    prior = [p for p in series if p[0] <= cut]
    base = prior[-1][1] if prior else series[0][1]
    if len(series) > max_points:   # 스파크라인용 다운샘플
        step = len(series) / max_points
        series = [series[int(i * step)] for i in range(max_points)] + [series[-1]]
    return {"pnl_recent": last_v - base, "history": series}


def fetch_positions(addr: str, only: tuple | None = None) -> dict:
    """주소의 현재 계좌·열린 포지션. only 지정 시 해당 코인만(예: 5대 메이저)."""
    d = _post(_INFO_URL, {"type": "clearinghouseState", "user": addr})
    ms = d.get("marginSummary", {})
    positions = []
    for ap in d.get("assetPositions", []):
        p = ap.get("position", {})
        coin = p.get("coin")
        szi = float(p.get("szi") or 0.0)
        if szi == 0 or (only and coin not in only):
            continue
        positions.append({
            "coin": coin,
            "side": "long" if szi > 0 else "short",
            "size": abs(szi),
            "entry": float(p["entryPx"]) if p.get("entryPx") else None,
            "notional": float(p.get("positionValue") or 0.0),
            "upnl": float(p.get("unrealizedPnl") or 0.0),
            "leverage": (p.get("leverage") or {}).get("value"),
            "roe": float(p["returnOnEquity"]) if p.get("returnOnEquity") else None,
            "liquidation": float(p["liquidationPx"]) if p.get("liquidationPx") else None,
            "entry_ts": None,  # entry_times()로 채움
        })
    positions.sort(key=lambda x: -x["notional"])
    return {
        "account_value": float(ms.get("accountValue") or 0.0),
        "total_notional": float(ms.get("totalNtlPos") or 0.0),
        "positions": positions,
    }


def entry_times(addr: str, positions: list[dict]) -> None:
    """userFills(체결이력)로 각 포지션이 '현재 방향으로 열린 시점'을 역산해 entry_ts(ms) 채움.

    체결을 최신→과거로 되짚어 포지션이 0/반대에서 현재 부호로 넘어간 체결의 시각 = 진입시점.
    최근 2000체결 밖(오래 보유)이면 못 찾아 None 유지.
    """
    if not positions:
        return
    try:
        fills = _post(_INFO_URL, {"type": "userFills", "user": addr})
    except Exception:  # noqa: BLE001
        return
    if not isinstance(fills, list):
        return
    by_coin: dict[str, list] = {}
    for f in fills:
        by_coin.setdefault(f.get("coin"), []).append(f)
    for pos in positions:
        fs = by_coin.get(pos["coin"])
        if not fs:
            continue
        # 현재 부호 있는 사이즈(롱=+, 숏=-)
        cur = pos["size"] if pos["side"] == "long" else -pos["size"]
        fs.sort(key=lambda x: -(x.get("time") or 0))  # 최신→과거
        after = cur
        for f in fs:
            sz = float(f.get("sz") or 0.0)
            delta = sz if f.get("side") == "B" else -sz   # B=매수(+), A=매도(-)
            before = after - delta
            # 이 체결 이전이 flat이거나 반대부호면, 이 체결이 현재 방향을 연 것
            if before == 0 or (before > 0) != (cur > 0):
                pos["entry_ts"] = f.get("time")
                break
            after = before


def top_traders_with_positions(
    limit: int = 25, scan: int = 200, recent_days: int = 90, **kw
) -> list[dict]:
    """필터 통과 상위에서 (최근 `recent_days`일 수익성>0) & (열린 포지션 있음) 트레이더 limit개까지.

    scan: 2차 조회 최대 스캔 수(API 호출 상한). 3개월 수익성은 하락장 감안해 기본 90일.
    """
    cand = screen(fetch_leaderboard(), **kw)
    out: list[dict] = []
    for t in cand[:scan]:
        port = fetch_portfolio(t["addr"], days=recent_days)
        if not port or port["pnl_recent"] <= 0:   # 최근 수익성(3개월) 필터
            continue
        try:
            pos = fetch_positions(t["addr"], only=MAJORS)   # 5대 메이저 포지션만
        except Exception:  # noqa: BLE001
            continue
        if pos["account_value"] < MIN_ACCOUNT:   # ★실시간 계좌가치로 지갑사이즈 필터(스테일값 아님)★
            continue
        ps = pos["positions"]
        if not ps:                          # 메이저 포지션 보유 트레이더만
            continue
        # 양방향(헤지) 제외: 지배방향 비중 < DIRECTIONAL_MIN 이면 델타뉴트럴/헤지 북으로 보고 제외
        long_ntl = sum(p["notional"] for p in ps if p["side"] == "long")
        short_ntl = sum(p["notional"] for p in ps if p["side"] == "short")
        gross = long_ntl + short_ntl
        if gross <= 0 or max(long_ntl, short_ntl) / gross < DIRECTIONAL_MIN:
            continue
        # 고배율 ROI 눈속임 제외: 포지션 최대 레버리지 > MAX_LEV
        max_lev = max((p.get("leverage") or 0) for p in ps)
        if max_lev > MAX_LEV:
            continue
        try:
            entry_times(t["addr"], ps)                      # 진입 시각 역산
        except Exception:  # noqa: BLE001
            pass
        out.append({
            **t, **pos,
            "net_side": "long" if long_ntl >= short_ntl else "short",
            "max_lev": max_lev,
            "recent_pnl": port["pnl_recent"], "recent_days": recent_days,
            "pnl_history": port["history"],                 # 역대 PnL 그래프용
        })
        if len(out) >= limit:
            break
    return out


def coin_summary(traders: list[dict]) -> list[dict]:
    """선별 트레이더들의 코인별 집계: 순롱/순숏 포지션 수·규모·청산가 범위(롱/숏 분리)."""
    agg: dict[str, dict] = {c: {
        "coin": c, "long_count": 0, "short_count": 0,
        "long_notional": 0.0, "short_notional": 0.0,
        "liq_long": [], "liq_short": [],
    } for c in MAJORS}
    for t in traders:
        for p in t.get("positions", []):
            a = agg.get(p["coin"])
            if not a:
                continue
            if p["side"] == "long":
                a["long_count"] += 1
                a["long_notional"] += p["notional"]
                if p.get("liquidation"):
                    a["liq_long"].append(p["liquidation"])
            else:
                a["short_count"] += 1
                a["short_notional"] += p["notional"]
                if p.get("liquidation"):
                    a["liq_short"].append(p["liquidation"])
    out = []
    for c in MAJORS:
        a = agg[c]
        a["liq_long_range"] = [min(a["liq_long"]), max(a["liq_long"])] if a["liq_long"] else None
        a["liq_short_range"] = [min(a["liq_short"]), max(a["liq_short"])] if a["liq_short"] else None
        del a["liq_long"], a["liq_short"]
        out.append(a)
    return out


def build_bundle(limit: int = 25, recent_days: int = 90) -> dict:
    """대시보드용 묶음: 필터 조건 + 코인별 집계 + 상위 트레이더 포지션."""
    traders = top_traders_with_positions(limit=limit, recent_days=recent_days)
    return {
        "source": "hyperliquid",
        "summary": coin_summary(traders),
        "filter": {
            "min_pnl": MIN_PNL, "min_roi": MIN_ROI, "min_account": MIN_ACCOUNT,
            "recent_trading": True, "recent_profit_days": recent_days,
            "coins": list(MAJORS),
            "directional_min": DIRECTIONAL_MIN, "max_leverage": MAX_LEV,
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
