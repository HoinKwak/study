"""Hyperliquid 리더보드 상위 트레이더 현재 포지션 커넥터.

공개 API(키 불필요)로 리더보드를 받아 필터(lifetime PnL·ROI + 최근 거래·수익성)를 통과한
상위 트레이더를 뽑고, 각자의 현재 열린 포지션을 조회한다. 대시보드 '리더보드 포지션' 섹션이 사용.

- 리더보드: https://stats-data.hyperliquid.xyz/Mainnet/leaderboard (windowPerformances=day/week/month/allTime)
- 포지션:   POST https://api.hyperliquid.xyz/info  {"type":"clearinghouseState","user":addr}
프록시: HTTPS_PROXY 환경변수를 urllib가 자동 사용.
"""
from __future__ import annotations

import json
import time
import urllib.error
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
# 라이징스타(우측 패널): 통산 상위(좌측)와 달리 '최근 한 달 실적·거래빈도' 기준.
# ※ Hyperliquid month roi는 초기자본 극소 계좌에서 분모왜곡(수백배)이 잦아 순위기준 부적합 →
#   왜곡 없는 '절대 한 달 PnL'로 정렬하고, 통산 상위와 겹치는 얼굴은 제외해 '신흥' 성격을 살린다.
FREQ_VLM_MULT = 3.0      # 거래빈도 하한: 최근 한 달 거래대금 ≥ 계좌 × 배수(회전율)
TOP_LIMIT = 20           # 좌측(상위 트레이더) 최대
RISING_LIMIT = 12        # 우측(라이징스타) 최대


def _request(req: urllib.request.Request, retries: int = 4):
    """레이트리밋(429)·일시적 5xx·타임아웃은 지수백오프로 재시도.

    ★중요★ 이 재시도가 없으면 검증 중 일시적 429/타임아웃이 예외로 새어나가 해당 후보가
    '조용히 스킵'되고, 그 결과 상위/라이징 목록 수가 리빌드마다 들쭉날쭉(예: 12→2)해진다.
    """
    delay = 1.0
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < retries - 1:
                ra = e.headers.get("Retry-After") if e.headers else None
                time.sleep(float(ra) if (ra and ra.replace(".", "", 1).isdigit()) else delay)
                delay = min(delay * 2, 8.0)
                continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries - 1:
                time.sleep(delay)
                delay = min(delay * 2, 8.0)
                continue
            raise
    raise RuntimeError("unreachable")  # pragma: no cover


def _get(url: str) -> dict | list:
    return _request(urllib.request.Request(url, headers=_UA))


def _post(url: str, payload: dict) -> dict:
    return _request(urllib.request.Request(url, data=json.dumps(payload).encode(), headers=_UA))


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


def screen_rising(
    rows: list[dict],
    min_account: float = MIN_ACCOUNT,
    freq_mult: float = FREQ_VLM_MULT,
) -> list[dict]:
    """라이징스타 후보: 최근 한 달 수익>0 + 거래빈도(회전율) 하한. **절대 한 달 PnL 내림차순**.

    통산 상위(screen)와 달리 lifetime PnL≥$100K를 요구하지 않는다 — '최근 한 달에 잘하는'
    트레이더가 목적. 한 달 실적은 (분모왜곡 잦은 roi 대신) 절대 PnL로 보고, 거래활발도는
    한 달 거래대금/계좌 회전율로 본다. (통산 상위가 고점 숏 후 장기보유라 단기 참고가 안 된다는
    판단에서 분리한 패널.) turnover(vlm/계좌)를 함께 실어 카드에 '거래빈도'로 표시한다.
    """
    out: list[dict] = []
    for r in rows:
        perfs = r.get("windowPerformances") or []
        allt = _window(perfs, "allTime")
        month = _window(perfs, "month")
        acct = float(r.get("accountValue") or 0.0)
        if month["pnl"] <= 0:
            continue
        if acct < min_account:   # 먼지계좌 사전제거. 실계좌는 검증(clearinghouseState)서 재확인
            continue
        if month["vlm"] < freq_mult * acct:   # 거래빈도(회전율) 하한
            continue
        out.append({
            "addr": r["ethAddress"], "name": r.get("displayName"),
            "account_value": acct, "pnl": allt["pnl"], "roi": allt["roi"],
            "month_pnl": month["pnl"], "month_vlm": month["vlm"],
            "turnover": month["vlm"] / acct,   # 한 달 회전율(거래빈도 대용)
        })
    out.sort(key=lambda x: -x["month_pnl"])
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


def _reconstruct_entries(positions: list[dict], fills: list) -> None:
    """체결이력(fills, 시간순 무관)으로 각 포지션 진입시각 역산해 entry_ts 채움(float 정밀도 보정)."""
    by_coin: dict[str, list] = {}
    for f in fills:
        by_coin.setdefault(f.get("coin"), []).append(f)
    for pos in positions:
        fs = by_coin.get(pos["coin"])
        if not fs:
            continue
        cur = pos["size"] if pos["side"] == "long" else -pos["size"]
        fs.sort(key=lambda x: -(x.get("time") or 0))   # 최신→과거
        after = cur
        for f in fs:
            sz = float(f.get("sz") or 0.0)
            delta = sz if f.get("side") == "B" else -sz
            before = after - delta
            if abs(before) < 1e-6 or (before > 0) != (cur > 0):   # float 오차 흡수
                pos["entry_ts"] = f.get("time")
                break
            after = before


def entry_times_deep(addr: str, positions: list[dict],
                     max_calls: int = 10, window_ms: int = 3 * 86_400_000) -> None:
    """2000체결 창을 넘어 과거까지 되짚어 진입시각을 찾는다(라이징스타용 정밀 추적).

    최근 userFills(최신 2000)로 앵커 후, userFillsByTime로 window_ms(기본 3일) 단위로 뒤로
    페이징하며 체결을 누적해 역산. 활발한 트레이더는 진입체결이 최근 2000건 밖으로 밀려 얕은
    entry_times로는 못 찾던 것을 여기서 보강. max_calls×window_ms(기본 30일) 밖이면 None 유지
    (진짜 장기보유). userFillsByTime: 시간범위 내 최대 2000건 반환.
    """
    if not positions:
        return
    all_fills: list = []
    try:
        recent = _post(_INFO_URL, {"type": "userFills", "user": addr})
        if isinstance(recent, list):
            all_fills.extend(recent)
    except Exception:  # noqa: BLE001
        pass
    end = min((int(f.get("time") or 0) for f in all_fills), default=int(time.time() * 1000))
    for _ in range(max_calls):
        start = max(0, end - window_ms)
        try:
            fills = _post(_INFO_URL, {"type": "userFillsByTime", "user": addr,
                                      "startTime": start, "endTime": end})
        except Exception:  # noqa: BLE001
            break
        if isinstance(fills, list) and fills:
            all_fills.extend(fills)
        end = start
        if start <= 0:
            break
        time.sleep(0.08)   # info endpoint 배려
    if all_fills:
        _reconstruct_entries(positions, all_fills)


def _validate_candidate(t: dict, recent_days: int, memo: dict) -> dict | None:
    """후보 1명 2차 검증: 실계좌·메이저 포지션·양방향/고배율 필터 통과 시 enriched dict, 아니면 None.

    memo[addr]에 조회결과 캐시(top/rising 겹치는 후보 재조회 방지). 값: enriched dict | False.
    반환은 후보의 랭킹필드(t: month_roi 등) + enriched(포지션·history)를 합친 것.
    """
    addr = t["addr"]
    if addr in memo:
        cached = memo[addr]
        return {**t, **cached} if cached else None
    port = fetch_portfolio(addr, days=recent_days)
    if not port or port["pnl_recent"] <= 0:   # 최근 수익성(3개월) 필터
        memo[addr] = False; return None
    try:
        pos = fetch_positions(addr, only=MAJORS)   # 5대 메이저 포지션만
    except Exception:  # noqa: BLE001
        memo[addr] = False; return None
    if pos["account_value"] < MIN_ACCOUNT:   # ★실시간 계좌가치로 지갑사이즈 필터(스테일값 아님)★
        memo[addr] = False; return None
    ps = pos["positions"]
    if not ps:                          # 메이저 포지션 보유 트레이더만
        memo[addr] = False; return None
    # 양방향(헤지) 제외: 지배방향 비중 < DIRECTIONAL_MIN 이면 델타뉴트럴/헤지 북으로 보고 제외
    long_ntl = sum(p["notional"] for p in ps if p["side"] == "long")
    short_ntl = sum(p["notional"] for p in ps if p["side"] == "short")
    gross = long_ntl + short_ntl
    if gross <= 0 or max(long_ntl, short_ntl) / gross < DIRECTIONAL_MIN:
        memo[addr] = False; return None
    # 고배율 ROI 눈속임 제외: 포지션 최대 레버리지 > MAX_LEV
    max_lev = max((p.get("leverage") or 0) for p in ps)
    if max_lev > MAX_LEV:
        memo[addr] = False; return None
    try:
        entry_times(addr, ps)                      # 진입 시각 역산
    except Exception:  # noqa: BLE001
        pass
    enriched = {
        **pos,
        "net_side": "long" if long_ntl >= short_ntl else "short",
        "max_lev": max_lev,
        "recent_pnl": port["pnl_recent"], "recent_days": recent_days,
        "pnl_history": port["history"],                 # 역대 PnL 그래프용
    }
    memo[addr] = enriched
    return {**t, **enriched}


def _collect(cand: list[dict], limit: int, recent_days: int, memo: dict, scan: int) -> list[dict]:
    """후보 리스트를 순서대로 2차 검증해 통과분 limit개까지 수집."""
    out: list[dict] = []
    for t in cand[:scan]:
        e = _validate_candidate(t, recent_days, memo)
        if e:
            out.append(e)
            if len(out) >= limit:
                break
    return out


def top_traders_with_positions(
    limit: int = 25, scan: int = 200, recent_days: int = 90, **kw
) -> list[dict]:
    """필터 통과 상위에서 (최근 `recent_days`일 수익성>0) & (열린 포지션 있음) 트레이더 limit개까지."""
    return _collect(screen(fetch_leaderboard(), **kw), limit, recent_days, {}, scan)


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


def build_bundle(
    top_limit: int = TOP_LIMIT, rising_limit: int = RISING_LIMIT,
    recent_days: int = 90, scan: int = 200,
) -> dict:
    """대시보드용 묶음: 좌 상위 트레이더(통산)·우 라이징스타(최근 한 달) + 코인별 집계.

    리더보드 1회 조회 후 두 후보군을 같은 memo로 검증(겹치는 후보 재조회 방지).
    """
    rows = fetch_leaderboard()
    memo: dict = {}
    top = _collect(screen(rows), top_limit, recent_days, memo, scan)
    top_addrs = {t["addr"] for t in top}
    # 라이징스타는 통산 상위와 겹치는 얼굴 제외 → '이번 달 신흥' 성격 유지
    rising_cand = [t for t in screen_rising(rows) if t["addr"] not in top_addrs]
    rising = _collect(rising_cand, rising_limit, recent_days, memo, scan)
    # 라이징스타만 진입시각 정밀 추적(2000체결 창 밖까지) — 활발한 트레이더라 얕은 역산으로는
    # 대부분 못 찾아 '장기'로 오표기되던 것을 보강. 상위 트레이더(장기보유)는 그대로 둔다.
    for t in rising:
        try:
            entry_times_deep(t["addr"], t.get("positions", []))
        except Exception:  # noqa: BLE001
            pass
    return {
        "source": "hyperliquid",
        "summary": coin_summary(top + rising),   # 겹침 없음(위에서 제외) → 그대로 합산
        "filter": {
            "min_pnl": MIN_PNL, "min_roi": MIN_ROI, "min_account": MIN_ACCOUNT,
            "recent_trading": True, "recent_profit_days": recent_days,
            "coins": list(MAJORS),
            "directional_min": DIRECTIONAL_MIN, "max_leverage": MAX_LEV,
            "rising_freq_mult": FREQ_VLM_MULT, "rising_rank": "month_pnl",
        },
        "top": top, "rising": rising,
        "count": len(top) + len(rising),
        "traders": top,   # 하위호환(옛 렌더가 d.traders 참조)
    }


if __name__ == "__main__":
    b = build_bundle(top_limit=8, rising_limit=6)
    for label, key in (("상위 트레이더(통산)", "top"), ("라이징스타(최근 한 달)", "rising")):
        print(f"\n[Hyperliquid] {label} {len(b[key])}명")
        for t in b[key]:
            extra = (f"한달 ${t['month_pnl']:,.0f} 회전 {t['turnover']:.1f}x" if key == "rising"
                     else f"90d ${t['recent_pnl']:,.0f}")
            print(f"  {t['addr'][:10]}… PnL ${t['pnl']:,.0f} ROI {t['roi']*100:.0f}% "
                  f"{extra} | 계좌 ${t['account_value']:,.0f} | 포지션 {len(t['positions'])}개")
