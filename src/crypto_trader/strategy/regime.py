"""시장 레짐(추세장/횡보장) 감지 — ADX + DI 기반.

- ADX < range_th        → RANGE (횡보): 평균회귀(RSI) 우위
- ADX ≥ trend_th, +DI>-DI → TREND_UP (상승추세): 추세추종(MACD/ADX) 우위
- ADX ≥ trend_th, -DI>+DI → TREND_DOWN (하락추세)
- 그 사이는 직전 성향을 약하게 반영하는 NEUTRAL
"""
from __future__ import annotations

from enum import Enum

import pandas as pd

from ..signals import indicators as ind


class Regime(str, Enum):
    RANGE = "range"
    TREND_UP = "trend_up"
    TREND_DOWN = "trend_down"
    NEUTRAL = "neutral"

    @property
    def is_trend(self) -> bool:
        return self in (Regime.TREND_UP, Regime.TREND_DOWN)


def detect_regime(df: pd.DataFrame, adx_period: int = 14,
                  range_th: float = 20.0, trend_th: float = 25.0) -> tuple[Regime, float]:
    """(레짐, ADX값) 반환."""
    if len(df) < adx_period + 5:
        return Regime.NEUTRAL, 0.0
    adx_s, plus_di, minus_di = ind.adx(df, adx_period)
    adx_val = float(adx_s.iloc[-1])
    pdi = float(plus_di.iloc[-1])
    mdi = float(minus_di.iloc[-1])

    if adx_val < range_th:
        return Regime.RANGE, adx_val
    if adx_val >= trend_th:
        return (Regime.TREND_UP if pdi >= mdi else Regime.TREND_DOWN), adx_val
    return Regime.NEUTRAL, adx_val
