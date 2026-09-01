"""멀티 타임프레임(1h/4h/1d) ATR% 동시확장 동조 브레이크아웃 — 공통 데이터 로더 + 지표.

스펙: research/strategies/multi-timeframe-atr-synchronized-expansion-breakout-swing.md

⚠️ 시간 단위 함정: pandas 3.0.5 는 `to_datetime(unit="ms")` 가 `datetime64[ms]` 를 유지하고,
여기에 `pd.Timedelta` 를 더하면 조용히 `datetime64[us]` 로 업캐스트되어(값이 1000배로 벌어짐)
merge_asof 정렬이 깨진다(리뷰어가 과거 이 함정에 걸린 이력 있음). 이 모듈은 모든 DatetimeIndex 를
파싱 직후 `.astype("datetime64[ns]")` 로 명시 통일해 이 함정을 원천 차단한다.
"""
from __future__ import annotations

import bisect
import os
import sys
from collections import deque
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

_repo_src = os.environ.get(
    "MTFATR_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))  # .../research/backtests/repro/<slug>/common.py -> repo/src
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "MTFATR_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/mtfatr"))
DATA = SP / "data"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = (TAKER_FEE + SLIPPAGE) * 2  # 0.14%

_KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
               "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


# ------------------------------------------------------------------ 로더

@lru_cache(maxsize=None)
def load_klines_1h(symbol: str) -> pd.DataFrame:
    files = sorted(DATA.glob(f"klines_1h/{symbol}-1h-*.csv"))
    parts = []
    for p in files:
        with open(p) as f:
            first = f.readline()
        has_header = "open_time" in first
        df = pd.read_csv(p, header=0 if has_header else None,
                         names=_KLINE_COLS if not has_header else None)
        df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
        if df.empty:
            continue
        df["open_time"] = df["open_time"].astype("int64")
        parts.append(df)
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    # ns 명시 통일(ms 파싱 유지 dtype 함정 회피): 정수 ms epoch -> ns astype 후 to_datetime
    dt = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    dt = pd.DatetimeIndex(dt).astype("datetime64[ns, UTC]")
    out["dt"] = dt
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    return out[["open", "high", "low", "close", "volume", "quote_volume"]]


def resample_native(df1h: pd.DataFrame, rule: str) -> pd.DataFrame:
    """1h -> 상위 TF 리샘플. UTC 00:00 앵커(origin='start_day')로 경계 정렬."""
    out = pd.DataFrame({
        "open": df1h["open"].resample(rule, origin="start_day").first(),
        "high": df1h["high"].resample(rule, origin="start_day").max(),
        "low": df1h["low"].resample(rule, origin="start_day").min(),
        "close": df1h["close"].resample(rule, origin="start_day").last(),
        "volume": df1h["volume"].resample(rule, origin="start_day").sum(),
    }).dropna(subset=["open", "close"])
    out.index = out.index.astype("datetime64[ns, UTC]")
    return out


# ------------------------------------------------------------------ 지표: 롤링 백분위

def rolling_percentile_rank(x: np.ndarray, window: int) -> np.ndarray:
    """x[i] 가 [i-window+1, i] 구간(window 개, 자기 자신 포함)에서 차지하는 백분위(0~100).

    정의: pct = (창 내 <= x[i] 인 개수) / window * 100. 창에 NaN 있으면 NaN.
    현재 봉까지의 과거 데이터만 사용(룩어헤드 없음) — 창이 [i-window+1, i] 이고 i 는 '이미 닫힌 봉'.
    """
    n = len(x)
    out = np.full(n, np.nan)
    buf: deque[float] = deque()
    sorted_win: list[float] = []
    nan_ct = 0
    for i in range(n):
        v = x[i]
        buf.append(v)
        is_nan = not np.isfinite(v)
        if is_nan:
            nan_ct += 1
        else:
            bisect.insort(sorted_win, v)
        if len(buf) > window:
            old = buf.popleft()
            if not np.isfinite(old):
                nan_ct -= 1
            else:
                idx = bisect.bisect_left(sorted_win, old)
                sorted_win.pop(idx)
        if len(buf) == window and nan_ct == 0:
            idx = bisect.bisect_right(sorted_win, v)
            out[i] = idx / window * 100.0
    return out


def map_asof_available(target_close_time: pd.DatetimeIndex, source: pd.Series,
                       source_close_offset: pd.Timedelta) -> np.ndarray:
    """상위/하위 스케일 시리즈를 '그 봉이 닫혀 값이 확정된 시각'(avail_time) 기준으로
    target_close_time 에 backward asof 매핑한다. 미래 참조 불가(각 target 시각 <= avail_time
    인 값은 절대 안 씀 — merge_asof direction='backward' 는 target >= avail 인 가장 최근 값만 취함).
    """
    src = source.dropna()
    if src.empty:
        return np.full(len(target_close_time), np.nan)
    avail = (src.index + source_close_offset).astype("datetime64[ns, UTC]")
    order = np.argsort(avail.values)
    avail_sorted = avail[order]
    vals_sorted = src.to_numpy(float)[order]
    left = pd.DataFrame({"t": pd.DatetimeIndex(target_close_time).astype("datetime64[ns, UTC]")})
    right = pd.DataFrame({"avail": avail_sorted, "val": vals_sorted})
    merged = pd.merge_asof(left.sort_values("t"), right, left_on="t", right_on="avail",
                           direction="backward")
    # left 는 이미 정렬돼 들어오지만 방어적으로 원래 순서 복구
    merged = merged.set_index(left.sort_values("t").index).reindex(left.index)
    return merged["val"].to_numpy(float)


# ------------------------------------------------------------------ 시그널 빌드

@dataclass
class Signals:
    h1: pd.DataFrame     # 1h OHLC
    h4: pd.DataFrame     # 4h OHLC (native 1h->resample)
    d1: pd.DataFrame     # 1d OHLC (native 1h->resample)
    p1h_at4h: np.ndarray  # 4h 봉 close_time 기준 1h 백분위(asof)
    p4h_at4h: np.ndarray  # 4h 봉 자기 백분위
    p1d_at4h: np.ndarray  # 4h 봉 close_time 기준 1d 백분위(asof, 가장 최근 '닫힌' 1d 봉)
    atr22_4h_signal: np.ndarray   # SL 용: 신호봉(closed) 시점 ATR22(4h)
    atr22_4h_trail: np.ndarray    # 트레일용: 직전 봉까지의 ATR22(4h) (신규 진입 판단은 신호봉 기준)


def build_signals(symbol: str, pct_th: float = 0.6,
                  lookback_1h: int = 168, lookback_4h: int = 42, lookback_1d: int = 20
                  ) -> Signals | None:
    h1 = load_klines_1h(symbol)
    if h1.empty:
        return None
    h4 = resample_native(h1, "4h")
    d1 = resample_native(h1, "1D")

    atr1h = ind.atr(h1, 14)
    atr4h = ind.atr(h4, 14)
    atr1d = ind.atr(d1, 14)
    atrpct_1h = (atr1h / h1["close"]).replace([np.inf, -np.inf], np.nan)
    atrpct_4h = (atr4h / h4["close"]).replace([np.inf, -np.inf], np.nan)
    atrpct_1d = (atr1d / d1["close"]).replace([np.inf, -np.inf], np.nan)

    p1h = pd.Series(rolling_percentile_rank(atrpct_1h.to_numpy(float), lookback_1h), index=h1.index)
    p4h = pd.Series(rolling_percentile_rank(atrpct_4h.to_numpy(float), lookback_4h), index=h4.index)
    p1d = pd.Series(rolling_percentile_rank(atrpct_1d.to_numpy(float), lookback_1d), index=d1.index)

    close4h = (h4.index + pd.Timedelta(hours=4)).astype("datetime64[ns, UTC]")
    # p1h: 1h 봉의 avail_time = index+1h. 4h 봉 close_time 과 정확히 일치(같은 시각)하므로
    #      merge_asof backward 는 사실상 정확 일치 매핑(1h 데이터 결측 시엔 보수적으로 직전값).
    p1h_at4h = map_asof_available(pd.DatetimeIndex(close4h), p1h, pd.Timedelta(hours=1))
    # p4h: 자기 자신 스케일 -> 그대로(이미 그 4h 봉 close 시점에 확정된 값)
    p4h_at4h = p4h.reindex(h4.index).to_numpy(float)
    # p1d: 1d 봉의 avail_time = index+1일. 4h 봉 close_time 시점에 "가장 최근에 닫힌" 1d 봉만 사용.
    p1d_at4h = map_asof_available(pd.DatetimeIndex(close4h), p1d, pd.Timedelta(days=1))

    atr22_4h = ind.atr(h4, 22)
    # 신호봉(i, 방금 닫힌 4h 봉) 시점 ATR22 -> SL 계산에 사용(신호봉 자신의 값, 룩어헤드 아님)
    atr22_4h_signal = atr22_4h.to_numpy(float)
    # 트레일 갱신은 '직전까지 닫힌 봉'만 사용하도록 엔진에서 shift(1) 배열을 사용
    atr22_4h_trail = atr22_4h.shift(1).to_numpy(float)

    return Signals(h1=h1, h4=h4, d1=d1, p1h_at4h=p1h_at4h, p4h_at4h=p4h_at4h,
                   p1d_at4h=p1d_at4h, atr22_4h_signal=atr22_4h_signal,
                   atr22_4h_trail=atr22_4h_trail)
