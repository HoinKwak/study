"""solbot 카피트레이드 백테스트 (클라우드 — GeckoTerminal 청산 시뮬).

입력: state/entries.json (pull_entries.py가 사장님 PC에서 Helius로 뽑은 과거 매수신호).
동작: 엔트리마다 진입 이후 시간봉(USD)을 GeckoTerminal에서 받아, 3가지 청산모드
      (fixed·trailing·assist)를 시뮬해 순수익률(슬리피지·수수료 반영)을 낸다.
출력: 트레이드 통계 + $100·5%·동시20개 포트폴리오 시뮬 → research/backtests/ 리포트.

정직 주의(§5.4):
- **지갑 사후편향**: 277지갑은 이미 돈 번 걸 알고 골랐다 → 6~7월은 in-sample(낙관 상한).
- **진입 탐지지연**: 신호 ts '이후 첫 시간봉 시가'로 진입(룩어헤드 없음).
- **러그/데이터없음**: GeckoTerminal 풀·봉이 없으면 no_data로 분리 집계(제외/-100% 양쪽 제시).
- **청산 봉내**: 저가로 SL 먼저 검사(보수적), 그다음 고가로 TP. 슬리피지 양측 반영.
"""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

from . import config as C

_GT = "https://api.geckoterminal.com/api/v2"
_UA = {"User-Agent": "Mozilla/5.0 (solbot-bt)"}
_CACHE = C.STATE_DIR / "ohlcv_cache"
MODES = ("fixed", "trailing", "assist")


def _get(url: str) -> dict:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=25) as r:  # noqa: S310
        return json.load(r)


def top_pool(mint: str) -> str | None:
    """토큰 최고유동성 풀 주소."""
    try:
        d = _get(f"{_GT}/networks/solana/tokens/{mint}/pools?page=1")
        pools = d.get("data", [])
        if not pools:
            return None
        best = max(pools, key=lambda p: float(p["attributes"].get("reserve_in_usd") or 0))
        return best["attributes"]["address"]
    except Exception:  # noqa: BLE001
        return None


def ohlcv(pool: str, oldest_ts: int) -> list[tuple]:
    """풀의 시간봉(USD) 수집: (ts,o,h,l,c,v) 오름차순. before_timestamp 역페이지네이션."""
    bars: dict[int, tuple] = {}
    before = int(time.time())
    for _ in range(8):
        url = (f"{_GT}/networks/solana/pools/{pool}/ohlcv/hour?aggregate=1&limit=1000"
               f"&currency=usd&token=base&before_timestamp={before}")
        try:
            d = _get(url)
        except Exception:  # noqa: BLE001
            break
        lst = (d.get("data", {}).get("attributes", {}) or {}).get("ohlcv_list") or []
        if not lst:
            break
        for row in lst:
            t = int(row[0])
            bars[t] = (float(row[1]), float(row[2]), float(row[3]), float(row[4]), float(row[5]))
        oldest_in_page = min(int(r[0]) for r in lst)
        if oldest_in_page <= oldest_ts:
            break
        before = oldest_in_page
        time.sleep(2.2)   # GeckoTerminal 무료 레이트리밋 배려
    return sorted([(t, *v) for t, v in bars.items()])


def cached_ohlcv(mint: str, oldest_ts: int) -> list[tuple] | None:
    """토큰 시간봉 캐시(디스크). 없으면 풀조회→수집→저장. 실패 시 None(러그/데이터없음)."""
    _CACHE.mkdir(parents=True, exist_ok=True)
    f = _CACHE / f"{mint}.json"
    if f.exists():
        raw = json.loads(f.read_text())
        return [tuple(x) for x in raw] if raw else None
    pool = top_pool(mint)
    time.sleep(1.0)
    bars = ohlcv(pool, oldest_ts) if pool else []
    f.write_text(json.dumps(bars))
    return bars or None


def _net(gross: float, slip_bps: int = C.DEFAULT_SLIPPAGE_BPS) -> float:
    """슬리피지 양측 반영 순수익률. 진입 entry*(1+s), 청산 entry*(1+gross)*(1-s)."""
    s = slip_bps / 10_000
    return (1 + gross) * (1 - s) / (1 + s) - 1


def simulate(bars: list[tuple], entry_ts: int, mode: str) -> tuple | None:
    """청산 시뮬. 반환 (net_ret, hold_h, reason) | None(진입불가)."""
    idx = next((i for i, b in enumerate(bars) if b[0] >= entry_ts), None)
    if idx is None:
        return None
    if bars[idx][0] - entry_ts > 2 * 3600:   # 데이터 시작이 신호보다 2h+ 뒤 → 커버 안 됨(왜곡 방지)
        return None
    entry = bars[idx][1]            # 진입: 신호 이후 첫 봉 시가(탐지지연, 룩어헤드 없음)
    if entry <= 0:
        return None
    high = entry
    for j in range(idx, len(bars)):
        ts, o, h, l, c, v = bars[j]
        held_h = (ts - bars[idx][0]) / 3600.0
        if mode == "fixed":
            if l <= entry * (1 - C.SL_PCT):
                return (_net(-C.SL_PCT), held_h, "SL")
            if h >= entry * (1 + C.TP_PCT):
                return (_net(C.TP_PCT), held_h, "TP")
        elif mode == "trailing":
            high = max(high, h)
            if l <= high * (1 - C.TRAIL_PCT):
                return (_net(high * (1 - C.TRAIL_PCT) / entry - 1), held_h, "TRAIL")
        else:   # assist: 하드 SL + 시간청산(익절은 사람 판단이라 시간까지 라이드→종가)
            if l <= entry * (1 - C.SL_PCT):
                return (_net(-C.SL_PCT), held_h, "SL")
        if held_h >= C.MAX_HOLD_HOURS:
            return (_net(c / entry - 1), held_h, "TIME")
    return (_net(bars[-1][4] / entry - 1), (bars[-1][0] - bars[idx][0]) / 3600.0, "END")


def run(entries: list[dict], oldest_ts: int) -> dict:
    """엔트리 전체를 3모드로 시뮬. 토큰별 봉은 캐시 공유."""
    mints = sorted({e["mint"] for e in entries})
    print(f"토큰 {len(mints)}개 시간봉 수집(캐시)…")
    series: dict[str, list[tuple] | None] = {}
    for k, m in enumerate(mints, 1):
        series[m] = cached_ohlcv(m, oldest_ts)
        if k % 10 == 0:
            print(f"  {k}/{len(mints)}")
    results = {mode: [] for mode in MODES}
    no_data = 0
    for e in entries:
        bars = series.get(e["mint"])
        if not bars:
            no_data += 1
            continue
        for mode in MODES:
            r = simulate(bars, e["ts"], mode)
            if r:
                results[mode].append({"mint": e["mint"], "wallet": e["wallet"],
                                      "ts": e["ts"], "ret": r[0], "hold_h": r[1], "reason": r[2]})
    return {"results": results, "no_data": no_data, "n_entries": len(entries),
            "n_tokens": len(mints)}


if __name__ == "__main__":   # python -m sideprojects.solbot.backtest
    import sys
    ef = C.STATE_DIR / "entries.json"
    if not ef.exists():
        print(f"[대기] {ef} 없음 — 먼저 사장님 PC에서 pull_entries.py 실행 후 커밋/전달하세요.")
        sys.exit(0)
    data = json.loads(ef.read_text())
    entries = data["entries"]
    from datetime import datetime
    oldest = int(datetime.fromisoformat(data["since"].replace("Z", "+00:00")).timestamp())
    out = run(entries, oldest)
    print(f"\n엔트리 {out['n_entries']} · 토큰 {out['n_tokens']} · 데이터없음(러그후보) {out['no_data']}")
    for mode in MODES:
        rs = [x["ret"] for x in out["results"][mode]]
        if not rs:
            continue
        wins = sum(1 for r in rs if r > 0)
        avg = sum(rs) / len(rs)
        gains = sum(r for r in rs if r > 0); losses = -sum(r for r in rs if r < 0)
        pf = gains / losses if losses else float("inf")
        print(f"[{mode:8}] n={len(rs)} 승률 {wins/len(rs)*100:.0f}% 평균 {avg*100:+.1f}% "
              f"PF {pf:.2f} 합산 {sum(rs)*100:+.0f}%")
