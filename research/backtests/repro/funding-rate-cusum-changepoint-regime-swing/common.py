"""공통 데이터 로딩·지표 계산 — 펀딩레이트 CUSUM 체인지포인트 레짐전환 추세추종."""
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


def load_funding(symbol: str) -> pd.DataFrame:
    """calc_time(ns, UTC) 인덱스, 컬럼 rate/interval_hours. 원본 그대로(필터링은 events.py).

    ⚠️ 자체발견 정합 이슈: 원본 `calc_time`(ms epoch)이 정시 경계에서 항상 +0~31ms 지터(거래소
    기록시각의 미세 오차, 실측 7종목 전부 min=0/max=31ms, 절대 음수 없음)를 갖고 있어 4h 캔들
    `open_time`과 밀리초 단위로는 거의 일치하지 않는다(예: BTC 00:00:00.006 vs 봉의 00:00:00.000).
    이를 floor 없이 그대로 쓰면 진입/EMA 게이트 조회가 `in index` 정확매칭에 실패해 전체 이벤트의
    약 40%가 원인불명으로 조용히 누락된다(자체발견, BTC 300건 중 118건). 지터가 항상 양수·31ms
    이내이므로 정시로 **floor**해도 다른 시간대로 잘못 스냅될 위험이 없어 여기서 정정한다.
    """
    df = pd.read_parquet(DATA / f"{symbol}_fundingRate.parquet")
    df["calc_time"] = pd.to_datetime(df["calc_time"], unit="ms", utc=True).astype(
        "datetime64[ns, UTC]").dt.floor("1h")
    df = df.rename(columns={"last_funding_rate": "rate", "funding_interval_hours": "interval_hours"})
    df = df.set_index("calc_time").sort_index()
    df = df[~df.index.duplicated(keep="first")]
    df["rate"] = df["rate"].astype(float)
    return df[["rate", "interval_hours"]]


def load_klines_4h(symbol: str) -> pd.DataFrame:
    df = pd.read_parquet(DATA / f"{symbol}_klines.parquet")
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).astype(
        "datetime64[ns, UTC]")
    df = df.set_index("open_time").sort_index()
    df = df[~df.index.duplicated(keep="first")]
    for c in ["open", "high", "low", "close"]:
        df[c] = df[c].astype(float)
    return df


def load_symbol(symbol: str) -> dict:
    return {"funding": load_funding(symbol), "price_4h": load_klines_4h(symbol)}


def ema_4h(price_4h: pd.DataFrame, fast: int = 20, slow: int = 60) -> pd.DataFrame:
    ema_fast = _ind.ema(price_4h["close"], fast)
    ema_slow = _ind.ema(price_4h["close"], slow)
    return pd.DataFrame({"ema_fast": ema_fast, "ema_slow": ema_slow}, index=price_4h.index)


def atr14_4h(price_4h: pd.DataFrame) -> pd.Series:
    return _ind.atr(price_4h, period=14)


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
