"""심볼별 신호 세트 구성 — 4h klines(quote_volume) + OI(5m→4h) + 롤링 그레인저 레짐 + EMA20/50 + ATR14."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
import pandas as pd

from common import load_klines_4h, load_metrics_5m, oi_4h_from_5m, ema_4h, atr14_4h
from granger import rolling_granger_pvalues, classify_regime


@dataclass
class Signals:
    symbol: str
    df: pd.DataFrame          # 4h klines (open/high/low/close/volume/quote_volume)
    oi: pd.Series
    oi_5m_count: pd.Series
    dqv: pd.Series            # diff(log(quote_volume))
    doi: pd.Series            # diff(log(oi))
    p_qv2oi: pd.Series
    p_oi2qv: pd.Series
    regime: pd.Series         # 'qv_lead'/'oi_lead'/'none'
    transition_qv: pd.Series  # bool: 직전봉 oi_lead -> 이번봉 qv_lead
    ret4h: pd.Series          # log(close_t/close_{t-1})
    ema_fast: pd.Series
    ema_slow: pd.Series
    atr14: pd.Series


@lru_cache(maxsize=None)
def build_signals(symbol: str, gc_window: int = 60, gc_lag: int = 4,
                  p_sig: float = 0.05, p_insig: float = 0.10,
                  ema_fast_n: int = 20, ema_slow_n: int = 50) -> Signals | None:
    df = load_klines_4h(symbol)
    if df.empty:
        return None
    m5 = load_metrics_5m(symbol)
    if m5.empty:
        return None
    oi4h = oi_4h_from_5m(m5)
    df = df.join(oi4h, how="left")

    qv = df["quote_volume"].astype(float)
    oi = df["oi"].astype(float)
    # log-diff: 0 이하 값은 NaN 처리(데이터 결측/이상치 방어) 후 diff(log(.))
    qv_safe = qv.where(qv > 0)
    oi_safe = oi.where(oi > 0)
    dqv = np.log(qv_safe).diff()
    doi = np.log(oi_safe).diff()

    p_qv2oi_arr, p_oi2qv_arr = rolling_granger_pvalues(
        doi.to_numpy(), dqv.to_numpy(), window=gc_window, lag=gc_lag)
    p_qv2oi = pd.Series(p_qv2oi_arr, index=df.index)
    p_oi2qv = pd.Series(p_oi2qv_arr, index=df.index)
    regime_arr = classify_regime(p_qv2oi_arr, p_oi2qv_arr, p_sig=p_sig, p_insig=p_insig)
    regime = pd.Series(regime_arr, index=df.index)
    prev_regime = regime.shift(1)
    transition_qv = (prev_regime == "oi_lead") & (regime == "qv_lead")

    ret4h = np.log(df["close"]).diff()
    ema = ema_4h(df, ema_fast_n, ema_slow_n)
    atr14 = atr14_4h(df)

    return Signals(
        symbol=symbol, df=df[["open", "high", "low", "close", "volume", "quote_volume"]],
        oi=df["oi"], oi_5m_count=df["oi_5m_count"],
        dqv=dqv, doi=doi, p_qv2oi=p_qv2oi, p_oi2qv=p_oi2qv,
        regime=regime, transition_qv=transition_qv, ret4h=ret4h,
        ema_fast=ema["ema_fast"], ema_slow=ema["ema_slow"], atr14=atr14)
