"""OI ΔOI 왜도 레짐 게이트 + Donchian 추세추종 스윙 — 공통 데이터 로더 + 지표 계산.

스펙: research/strategies/oi-delta-skewness-regime-donchian-trend-swing.md
"""
from __future__ import annotations

import bisect
import sys
from collections import deque
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

# 원래 이 백테스트는 격리 git worktree(oiskew_wt)에서 실행했다. 재현 시 REPO_SRC 환경변수로
# 저장소 src 경로를 지정하거나, 기본값(이 파일 기준 repo 루트의 src)을 사용한다.
import os  # noqa: E402
_repo_src = os.environ.get(
    "OISKEW_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))  # .../research/backtests/repro/<slug>/common.py -> repo/src
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

# 원본 데이터(klines/metrics CSV, ~11,900개 파일)는 scratchpad 에 있으며 git 에는 포함되지
# 않는다(대용량). 재현 시 OISKEW_DATA_DIR 환경변수로 재다운로드한 데이터 디렉터리를 지정하거나
# dl_klines.sh / dl_metrics.sh 를 다시 실행해 받는다.
SP = Path(os.environ.get(
    "OISKEW_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiskew"))
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
def load_klines_4h(symbol: str) -> pd.DataFrame:
    files = sorted(DATA.glob(f"klines/{symbol}-4h-*.csv"))
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
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    return out[["open", "high", "low", "close", "volume", "quote_volume"]]


@lru_cache(maxsize=None)
def load_metrics_5m(symbol: str) -> pd.DataFrame:
    """metrics 5분 원본 로드. create_time 은 날짜 문자열 → 명시적 format 파싱(단위 사고 회피)."""
    files = sorted(DATA.glob(f"metrics/{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "symbol", "sum_open_interest",
                          "count_toptrader_long_short_ratio",
                          "sum_toptrader_long_short_ratio"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    # create_time: "YYYY-MM-DD HH:MM:SS" 문자열 → 명시적 format 지정(us/ms 단위사고 회피)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    return out


def oi_4h_from_5m(m5: pd.DataFrame) -> pd.DataFrame:
    """5분 OI → 4h 봉 마감시점 값(resample('4h').last()) + 빈 bin count(데이터 품질 확인용).

    ⚠️ resample('4h').last() 는 빈 bin 에 대해 NaN 을 반환한다(직전값 forward-fill 아님) —
    스펙 본문의 "resample last() 가 직전 유효값을 쓴다"는 서술은 이 pandas 버전(3.0.5)에서는
    실측 결과 사실이 아님을 이번 라운드에서 확인했다(§부록 참고). ffill 을 명시적으로 하지 않는 한
    빈 4h bin 은 NaN 으로 남고, 그 결과 ΔOI(diff)도 NaN → 롤링 왜도 계산에서 자동 배제된다.
    """
    if m5.empty:
        return pd.DataFrame()
    s = m5["sum_open_interest"]
    last = s.resample("4h", label="left", closed="left").last()
    cnt = s.resample("4h", label="left", closed="left").count()
    out = pd.DataFrame({"oi": last, "oi_5m_count": cnt})
    return out


# ------------------------------------------------------------------ 지표 계산

def rolling_skew_biased(x: np.ndarray, window: int) -> np.ndarray:
    """scipy.stats.skew(bias=True, 기본값) 방식 롤링 왜도. NaN 이 하나라도 있는 창은 NaN.

    O(n) 증분식 3차 모멘텀(합-기반) 계산 — window별 재정렬 없이 빠르게 계산.
    """
    n = len(x)
    out = np.full(n, np.nan)
    s1 = s2 = s3 = 0.0
    nan_ct = 0
    buf: deque[float] = deque()
    for i in range(n):
        v = x[i]
        buf.append(v)
        is_nan = not np.isfinite(v)
        if is_nan:
            nan_ct += 1
        else:
            s1 += v; s2 += v * v; s3 += v ** 3
        if len(buf) > window:
            old = buf.popleft()
            if not np.isfinite(old):
                nan_ct -= 1
            else:
                s1 -= old; s2 -= old * old; s3 -= old ** 3
        if len(buf) == window and nan_ct == 0:
            m = s1 / window
            var = s2 / window - m * m
            if var <= 0:
                out[i] = 0.0
            else:
                m3 = s3 / window - 3 * m * (s2 / window) + 2 * m ** 3
                out[i] = m3 / (var ** 1.5)
    return out


def rolling_percentile_rank(x: np.ndarray, window: int) -> np.ndarray:
    """x[i] 가 [i-window+1, i] 구간(window 개)에서 차지하는 백분위(0~100).
    창에 NaN 이 하나라도 있으면 NaN. 정의: pct = (창 내 <= x[i] 인 개수) / window * 100.
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


def donchian(df: pd.DataFrame, period: int) -> tuple[np.ndarray, np.ndarray]:
    """직전(shift 1봉) period 봉 고점/저점(현재봉 미포함, 룩어헤드 방지)."""
    hi = df["high"].rolling(period).max().shift(1).to_numpy(float)
    lo = df["low"].rolling(period).min().shift(1).to_numpy(float)
    return hi, lo


def realized_vol(df: pd.DataFrame, window: int = 20) -> pd.Series:
    ret = np.log(df["close"] / df["close"].shift(1))
    return ret.rolling(window).std()


@dataclass
class Signals:
    df: pd.DataFrame           # 4h klines
    delta_oi: pd.Series
    skew_oi: pd.Series
    pctile_skew: pd.Series
    don_hi: np.ndarray
    don_lo: np.ndarray
    atr14: pd.Series
    oi_5m_count: pd.Series
    oi_pct_change: pd.Series   # ΔOI% (동어반복 점검용)
    realized_vol20: pd.Series
    adx14: pd.Series


def build_signals(symbol: str, doi_window: int = 60, pctile_window_days: int = 180,
                  donchian_period: int = 20) -> Signals | None:
    df = load_klines_4h(symbol)
    if df.empty:
        return None
    m5 = load_metrics_5m(symbol)
    if m5.empty:
        return None
    oi4h = oi_4h_from_5m(m5)
    # 룩어헤드 방지: 4h 봉 자신의 index(open_time=bin 시작)에 그 bin 마감시점 OI 값을 붙임.
    # oi4h 의 index 는 klines 와 동일한 4h 경계(둘 다 UTC epoch 앵커 resample)이므로 직접 정렬.
    df = df.join(oi4h, how="left")
    delta_oi = df["oi"].diff()
    skew_arr = rolling_skew_biased(delta_oi.to_numpy(float), doi_window)
    skew_oi = pd.Series(skew_arr, index=df.index)
    pctile_window_bars = pctile_window_days * 6  # 4h 봉 = 하루 6개
    pctile_arr = rolling_percentile_rank(skew_oi.to_numpy(float), pctile_window_bars)
    pctile_skew = pd.Series(pctile_arr, index=df.index)
    don_hi, don_lo = donchian(df, donchian_period)
    atr14 = ind.atr(df, 14)
    oi_pct_change = df["oi"].pct_change()
    rv20 = realized_vol(df, 20)
    _plus, _minus, adx14 = ind.adx(df, 14)
    return Signals(df=df, delta_oi=delta_oi, skew_oi=skew_oi, pctile_skew=pctile_skew,
                   don_hi=don_hi, don_lo=don_lo, atr14=atr14,
                   oi_5m_count=df["oi_5m_count"], oi_pct_change=oi_pct_change,
                   realized_vol20=rv20, adx14=adx14)
