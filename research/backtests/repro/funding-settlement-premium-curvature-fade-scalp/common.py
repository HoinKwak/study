"""공통 데이터 로딩·지표 계산 — 펀딩정산 프리미엄인덱스 곡률(2차회귀) 페이드 스캘프."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

WORKTREE = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(WORKTREE / "src"))
from crypto_trader.signals import indicators as _ind  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

ROUND_TRIP_COST = 0.0014  # 왕복 수수료+슬리피지


def _load(symbol: str, kind: str, tf: str) -> pd.DataFrame:
    fn = DATA / f"{symbol}_{kind}_{tf}.parquet"
    df = pd.read_parquet(fn)
    # ⚠️ ms/us 함정: pandas 3.0.5 에서 datetime64[ms] + Timedelta 가 조용히 us 로 업캐스트되어
    # searchsorted/merge_asof 가 어긋난다. ns 로 명시 통일해 원천 차단.
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).astype(
        "datetime64[ns, UTC]")
    df = df.set_index("open_time").sort_index()
    df = df[~df.index.duplicated(keep="first")]
    for c in ["open", "high", "low", "close"]:
        df[c] = df[c].astype(float)
    return df


def load_symbol(symbol: str) -> dict:
    """symbol -> {prem_1m, price_15m} 원본 프레임(전체 이력)."""
    prem_1m = _load(symbol, "premiumIndexKlines", "1m")
    price_15m = _load(symbol, "klines", "15m")
    return {"prem_1m": prem_1m, "price_15m": price_15m}


def atr14_15m(price_15m: pd.DataFrame) -> pd.Series:
    """프레임워크 `indicators.atr`(Wilder ewm) 그대로 재사용."""
    return _ind.atr(price_15m, period=14)


def pf_r(series: pd.Series) -> float:
    pos = series[series > 0].sum()
    neg = -series[series < 0].sum()
    if neg == 0:
        return float("inf") if pos > 0 else float("nan")
    return pos / neg


def t_stat(series: pd.Series) -> float:
    n = len(series)
    if n < 2:
        return float("nan")
    sd = series.std(ddof=1)
    if sd == 0:
        return float("nan")
    return series.mean() / (sd / np.sqrt(n))


def split_is_oos(df: pd.DataFrame, is_start=IS_START, is_end=IS_END,
                  oos_start=OOS_START, oos_end=OOS_END, tcol: str = "entry_time"):
    if len(df) == 0:
        return df, df, df
    t = df[tcol]
    is_df = df[(t >= is_start) & (t <= is_end)]
    oos_df = df[(t >= oos_start) & (t <= oos_end)]
    full_df = df[(t >= is_start) & (t <= oos_end)]
    return is_df, oos_df, full_df


def win_rate(series: pd.Series) -> float:
    n = len(series)
    if n == 0:
        return float("nan")
    return float((series > 0).sum()) / n
