"""공통 데이터 로딩·지표 계산 — 거래대금-OI 롤링 그레인저 인과방향 전환 레짐.

스펙: research/strategies/quote-volume-oi-rolling-granger-causality-regime-swing.md
"""
from __future__ import annotations

import os
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
WORKTREE = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(WORKTREE / "src"))
from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "GRQV_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/granger_oiqv"))
DATA = SP / "data"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

ROUND_TRIP_COST = 0.0014  # 왕복 수수료+슬리피지 (0.05% 테이커 x2 + 0.02% 슬리피지 x2)


@lru_cache(maxsize=None)
def load_klines_4h(symbol: str) -> pd.DataFrame:
    """4h klines, open_time(ns UTC) 인덱스. klines open_time 은 정수 ms epoch."""
    df = pd.read_parquet(DATA / "klines" / f"{symbol}_4h.parquet")
    df = df.copy()
    df["dt"] = pd.to_datetime(df["open_time"].astype("int64"), unit="ms", utc=True)
    df = df.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        df[c] = df[c].astype(float)
    return df[["open", "high", "low", "close", "volume", "quote_volume"]]


@lru_cache(maxsize=None)
def load_metrics_5m(symbol: str) -> pd.DataFrame:
    """metrics 5분 원본 로드. ⚠️`create_time`은 날짜 문자열이라 unit 미지정 시 pandas가
    us 로 추론(klines 는 ms) — 명시적 format 지정으로 단위사고를 원천 차단한다(반복된 사고).
    """
    files = sorted((DATA / "metrics").glob(f"{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns or "sum_open_interest" not in df.columns:
            continue
        parts.append(df[["create_time", "sum_open_interest"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    return out[["sum_open_interest"]]


def oi_4h_from_5m(m5: pd.DataFrame) -> pd.DataFrame:
    """5분 OI → 4h 봉(마감시점, 즉 그 4h 구간 마지막 관측치). 빈 bin 은 NaN(ffill 안 함).

    resample('4h', label='left', closed='left').last() 은 klines open_time(4h UTC 앵커, 정시
    0/4/8/12/16/20 UTC)과 동일한 경계를 쓰므로 직접 join 가능.
    """
    if m5.empty:
        return pd.DataFrame()
    s = m5["sum_open_interest"]
    last = s.resample("4h", label="left", closed="left").last()
    cnt = s.resample("4h", label="left", closed="left").count()
    return pd.DataFrame({"oi": last, "oi_5m_count": cnt})


def ema_4h(price_4h: pd.DataFrame, fast: int = 20, slow: int = 50) -> pd.DataFrame:
    ema_fast = ind.ema(price_4h["close"], fast)
    ema_slow = ind.ema(price_4h["close"], slow)
    return pd.DataFrame({"ema_fast": ema_fast, "ema_slow": ema_slow}, index=price_4h.index)


def atr14_4h(price_4h: pd.DataFrame) -> pd.Series:
    return ind.atr(price_4h, period=14)


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


def split_is_oos(df: pd.DataFrame, tcol: str = "entry_time"):
    if len(df) == 0:
        return df, df, df
    t = df[tcol]
    is_df = df[(t >= IS_START) & (t <= IS_END)]
    oos_df = df[(t >= OOS_START) & (t <= OOS_END)]
    full_df = df[(t >= IS_START) & (t <= OOS_END)]
    return is_df, oos_df, full_df
