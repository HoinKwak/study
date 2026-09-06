"""공통 데이터 로딩·지표 계산 — 펀딩ΔF ApEn 레짐 게이트 + BTC 추세추종."""
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


def load_funding_btc() -> pd.DataFrame:
    """BTC fundingRate 원본 — calc_time floor(1h)로 지터 정리(CUSUM 스펙과 동일 함정 선제 처리),
    interval_hours==8 인 정규 정산만 남긴다(비8h 예외 배제, 배제비율은 diag_freq에서 실측)."""
    df = pd.read_parquet(DATA / "BTCUSDT_fundingRate.parquet")
    df["calc_time"] = pd.to_datetime(df["calc_time"], unit="ms", utc=True).astype(
        "datetime64[ns, UTC]").dt.floor("1h")
    df = df.rename(columns={"last_funding_rate": "rate", "funding_interval_hours": "interval_hours"})
    df = df.set_index("calc_time").sort_index()
    df = df[~df.index.duplicated(keep="first")]
    df["rate"] = df["rate"].astype(float)
    n0 = len(df)
    f8 = df[df["interval_hours"] == 8].copy()
    excluded_frac = 1.0 - (len(f8) / n0 if n0 else 0.0)
    return f8[["rate"]], excluded_frac


_KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
               "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


def _read_kline_csv(f: Path) -> pd.DataFrame:
    """⚠️자체발견: 2021년분 월간 덤프는 헤더가 없다(2022+만 헤더 있음 — markPriceKlines 등
    다른 덤프에서 이미 알려진 것과 같은 패턴). 헤더 유무를 첫 줄로 자동판별하지 않으면
    read_csv가 첫 데이터행을 컬럼명으로 삼켜 해당 월 전체가 NaN(→ 인덱스 NaT 1건으로
    뭉개짐, concat 시 다른 달과 컬럼명이 안 맞아 조용히 소실)되는 사고가 난다."""
    with open(f) as fh:
        first = fh.readline()
    if first.startswith("open_time"):
        return pd.read_csv(f)
    return pd.read_csv(f, header=None, names=_KLINE_COLS)


def load_klines_4h(symbol: str) -> pd.DataFrame:
    """data/klines_4h/<SYM>-4h-YYYY-MM.csv 전량을 이어붙임(캐시된 CSV, 2021년분은 헤더 없음)."""
    files = sorted(DATA.glob(f"klines_4h/{symbol}-4h-*.csv"))
    frames = [_read_kline_csv(f) for f in files]
    df = pd.concat(frames, ignore_index=True)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).astype(
        "datetime64[ns, UTC]")
    df = df.set_index("open_time").sort_index()
    df = df[~df.index.duplicated(keep="first")]
    for c in ["open", "high", "low", "close"]:
        df[c] = df[c].astype(float)
    return df[["open", "high", "low", "close"]]


def ema_pair(price_4h: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.DataFrame:
    ema_fast = _ind.ema(price_4h["close"], fast)
    ema_slow = _ind.ema(price_4h["close"], slow)
    return pd.DataFrame({"ema_fast": ema_fast, "ema_slow": ema_slow}, index=price_4h.index)


def atr14_4h(price_4h: pd.DataFrame, period: int = 14) -> pd.Series:
    return _ind.atr(price_4h, period=period)


def adx14_4h(price_4h: pd.DataFrame, period: int = 14):
    return _ind.adx(price_4h, period=period)


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


def win_rate(series: pd.Series) -> float:
    n = len(series)
    if n == 0:
        return float("nan")
    return float((series > 0).sum()) / n


def split_is_oos(df: pd.DataFrame, is_start=IS_START, is_end=IS_END,
                  oos_start=OOS_START, oos_end=OOS_END, tcol: str = "entry_time"):
    if len(df) == 0:
        return df, df, df
    t = df[tcol]
    is_df = df[(t >= is_start) & (t <= is_end)]
    oos_df = df[(t >= oos_start) & (t <= oos_end)]
    full_df = df[(t >= is_start) & (t <= oos_end)]
    return is_df, oos_df, full_df
