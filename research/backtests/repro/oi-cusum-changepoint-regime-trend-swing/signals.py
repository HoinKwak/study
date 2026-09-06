"""심볼별 신호 세트 구성 — 4h klines + OI(5m→4h) + OI CUSUM + EMA20/50 + ATR14."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import pandas as pd

from common import load_klines_4h, load_metrics_5m, oi_4h_from_5m, ema_4h, atr14_4h
from cusum import build_oi_cusum


@dataclass
class Signals:
    symbol: str
    df: pd.DataFrame          # 4h klines (open/high/low/close/volume)
    oi: pd.Series
    oi_5m_count: pd.Series
    oi_growth: pd.Series
    z: pd.Series
    s_pos: pd.Series
    s_neg: pd.Series
    s_pos_pre: pd.Series
    s_neg_pre: pd.Series
    cp_up: pd.Series
    cp_down: pd.Series
    ema_fast: pd.Series
    ema_slow: pd.Series
    atr14: pd.Series


@lru_cache(maxsize=None)
def build_signals(symbol: str, z_window_days: int = 90, k: float = 0.5, h: float = 5.0,
                  ema_fast_n: int = 20, ema_slow_n: int = 50) -> Signals | None:
    df = load_klines_4h(symbol)
    if df.empty:
        return None
    m5 = load_metrics_5m(symbol)
    if m5.empty:
        return None
    oi4h = oi_4h_from_5m(m5)
    df = df.join(oi4h, how="left")
    cusum = build_oi_cusum(df["oi"], z_window_days=z_window_days, k=k, h=h)
    ema = ema_4h(df, ema_fast_n, ema_slow_n)
    atr14 = atr14_4h(df)
    return Signals(
        symbol=symbol, df=df[["open", "high", "low", "close", "volume"]],
        oi=df["oi"], oi_5m_count=df["oi_5m_count"],
        oi_growth=cusum["oi_growth"], z=cusum["z"],
        s_pos=cusum["s_pos"], s_neg=cusum["s_neg"],
        s_pos_pre=cusum["s_pos_pre"], s_neg_pre=cusum["s_neg_pre"],
        cp_up=cusum["cp_up"], cp_down=cusum["cp_down"],
        ema_fast=ema["ema_fast"], ema_slow=ema["ema_slow"], atr14=atr14)
