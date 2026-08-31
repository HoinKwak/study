"""공통 데이터 로딩·지표 계산 — 프리미엄인덱스 꼬리비율(wick ratio) 소진 반전 스윙."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

WORKTREE = Path(__file__).resolve().parents[4]  # .../premwick-wt
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
    # ⚠️ ms/us 함정: pd.to_datetime(unit="ms")는 pandas 3.0.5에서 datetime64[ms] 를 만들고
    # 여기에 pd.Timedelta 를 더하면 조용히 us 로 업캐스트돼 merge_asof 가 어긋난다.
    # ns 로 명시 통일해 원천 차단.
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).astype(
        "datetime64[ns, UTC]")
    df = df.set_index("open_time").sort_index()
    df = df[~df.index.duplicated(keep="first")]
    for c in ["open", "high", "low", "close"]:
        df[c] = df[c].astype(float)
    return df


def load_symbol(symbol: str) -> dict:
    """symbol -> {price_4h, price_1d, prem_4h} 원본 프레임(전체 이력)."""
    price_4h = _load(symbol, "klines", "4h")
    price_1d = _load(symbol, "klines", "1d")
    prem_4h = _load(symbol, "premiumIndexKlines", "4h")
    return {"price_4h": price_4h, "price_1d": price_1d, "prem_4h": prem_4h}


def wick_asym(df: pd.DataFrame) -> pd.Series:
    """(upper_wick - lower_wick) / range. range<=0 인 봉은 NaN."""
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    upper = h - np.maximum(o, c)
    lower = np.minimum(o, c) - l
    rng = h - l
    out = (upper - lower) / rng
    out[rng <= 0] = np.nan
    return out


def atr14(df_4h: pd.DataFrame) -> pd.Series:
    """프레임워크 `indicators.atr`(Wilder ewm) 그대로 재사용 — 자체 재구현 아님."""
    return _ind.atr(df_4h, period=14)


def ema20_1d(price_1d: pd.DataFrame) -> pd.Series:
    """프레임워크 `indicators.ema` 재사용."""
    return _ind.ema(price_1d["close"], period=20)


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
