"""기술지표 종합 시그널.

RSI(역추세) + MACD(모멘텀) + ADX/DI(추세) + 캔들패턴 을 각각 -1~+1 로 환산해
가중 평균한 뒤 하나의 technical 점수를 만든다.
"""
from __future__ import annotations

import pandas as pd

from . import indicators as ind
from . import patterns as pat
from .base import SignalResult, clamp

# 기본 서브 지표 가중치 (합 1.0)
SUB_WEIGHTS = {
    "rsi": 0.25,
    "macd": 0.30,
    "adx": 0.25,
    "pattern": 0.20,
}

# 레짐별 서브 가중치 — 추세장은 추세추종(MACD/ADX), 횡보장은 평균회귀(RSI) 우위.
REGIME_WEIGHTS = {
    "range": {"rsi": 0.45, "macd": 0.15, "adx": 0.10, "pattern": 0.30},
    "trend_up": {"rsi": 0.10, "macd": 0.40, "adx": 0.35, "pattern": 0.15},
    "trend_down": {"rsi": 0.10, "macd": 0.40, "adx": 0.35, "pattern": 0.15},
    "neutral": SUB_WEIGHTS,
}


class TechnicalSignals:
    def __init__(self, rsi_period: int = 14, adx_period: int = 14):
        self.rsi_period = rsi_period
        self.adx_period = adx_period

    def compute(self, df: pd.DataFrame, regime: str | None = None) -> SignalResult:
        """df: columns = [timestamp, open, high, low, close, volume].

        regime 지정 시 레짐별 서브 가중치를 적용(추세장/횡보장 특성 반영).
        """
        if len(df) < 30:
            return SignalResult("technical", 0.0, {"reason": "insufficient_data"})

        weights = REGIME_WEIGHTS.get(regime or "", SUB_WEIGHTS)

        rsi_score, rsi_val = self._rsi_score(df["close"])
        macd_score, macd_hist = self._macd_score(df["close"])
        adx_score, adx_val = self._adx_score(df)
        pattern_score = pat.aggregate_patterns(df)

        total = (
            weights["rsi"] * rsi_score
            + weights["macd"] * macd_score
            + weights["adx"] * adx_score
            + weights["pattern"] * pattern_score
        )

        return SignalResult(
            "technical",
            clamp(total),
            {
                "regime": regime or "default",
                "rsi": round(rsi_val, 2),
                "rsi_score": round(rsi_score, 3),
                "macd_hist": round(macd_hist, 5),
                "macd_score": round(macd_score, 3),
                "adx": round(adx_val, 2),
                "adx_score": round(adx_score, 3),
                "pattern_score": round(pattern_score, 3),
            },
        )

    # ------------------------------------------------------------- 서브 점수

    def _rsi_score(self, close: pd.Series) -> tuple[float, float]:
        """RSI 역추세: 과매도(<30) 롱, 과매수(>70) 숏. 30~70 은 선형 보간."""
        rsi_val = float(ind.rsi(close, self.rsi_period).iloc[-1])
        # 50 을 중심으로 대칭. 30 이하 = +1, 70 이상 = -1
        score = (50.0 - rsi_val) / 20.0
        return clamp(score), rsi_val

    def _macd_score(self, close: pd.Series) -> tuple[float, float]:
        """MACD 히스토그램 부호+기울기로 모멘텀 방향."""
        _, _, hist = ind.macd(close)
        h_now = float(hist.iloc[-1])
        h_prev = float(hist.iloc[-2]) if len(hist) > 1 else h_now
        # 부호(0.6) + 증가/감소 방향(0.4)
        sign = 1.0 if h_now > 0 else (-1.0 if h_now < 0 else 0.0)
        slope = 1.0 if h_now > h_prev else (-1.0 if h_now < h_prev else 0.0)
        score = 0.6 * sign + 0.4 * slope
        return clamp(score), h_now

    def _adx_score(self, df: pd.DataFrame) -> tuple[float, float]:
        """추세 강도(ADX)로 스케일한 방향(+DI vs -DI)."""
        adx_val, plus_di, minus_di = ind.adx(df, self.adx_period)
        a = float(adx_val.iloc[-1])
        pdi = float(plus_di.iloc[-1])
        mdi = float(minus_di.iloc[-1])
        direction = 1.0 if pdi > mdi else (-1.0 if mdi > pdi else 0.0)
        # ADX 20 미만 = 추세 약함(점수 축소), 40 이상 = 강한 추세(만점)
        strength = clamp((a - 20.0) / 20.0, 0.0, 1.0)
        return direction * strength, a
