"""중기(mid) 전략 v2 — 상위 TF 추세 방향의 볼린저 밴드 눌림목 평균회귀.

v1(15m MACD 0선 교차)은 백테스트에서 엣지 없음이 확인되어 재설계 (docs/BACKTEST_RESULTS.md).

로직 (15m 시그널 / 1h 확인):
  - 1h 슈퍼트렌드로 추세 방향 확정
  - 상승추세: 15m 종가가 볼린저 하단 부근(밴드 하위 25% 이내) + RSI < 40 → LONG
  - 하락추세: 15m 종가가 볼린저 상단 부근(밴드 상위 25% 이내) + RSI > 60 → SHORT
  - TP: 볼린저 중심선(SMA20) — 평균회귀 목표
  - SL: 진입가 - sl_atr_mult × ATR (숏은 반대)
청산:
  - 1h 추세 반전 시 CLOSE (TP/SL 은 리스크/거래소 관리)
"""
from __future__ import annotations

import pandas as pd

from ..config import Settings
from ..signals import indicators as ind
from ..signals.base import Direction, SignalResult, clamp
from .regime import detect_regime
from .strategy import Action, Decision


class MidStrategy:
    def __init__(self, settings: Settings,
                 st_period: int = 10, st_mult: float = 3.0,
                 bb_period: int = 20, bb_std: float = 2.0,
                 band_zone: float = 0.25,
                 rsi_long_max: float = 40.0, rsi_short_min: float = 60.0,
                 sl_atr_mult: float = 1.5):
        self.s = settings
        self.st_period = st_period
        self.st_mult = st_mult
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.band_zone = band_zone          # 밴드폭 하위/상위 몇 % 구간을 '눌림목'으로 볼지
        self.rsi_long_max = rsi_long_max
        self.rsi_short_min = rsi_short_min
        self.sl_atr_mult = sl_atr_mult

    def decide(self, symbol: str, df: pd.DataFrame,
               confirm_df: pd.DataFrame | None = None,
               current_direction: Direction | None = None) -> Decision:
        regime, _ = detect_regime(df)
        if len(df) < self.bb_period + 10 or confirm_df is None or len(confirm_df) < 20:
            return Decision(Action.HOLD, Direction.FLAT, 0.0, regime, "데이터 부족")

        # 상위 TF 추세
        _st, st_dir = ind.supertrend(confirm_df, self.st_period, self.st_mult)
        trend_up = int(st_dir.iloc[-1]) > 0

        price = float(df["close"].iloc[-1])
        mid_band, upper, lower = ind.bollinger_bands(df["close"], self.bb_period, self.bb_std)
        mid_v = float(mid_band.iloc[-1])
        up_v = float(upper.iloc[-1])
        low_v = float(lower.iloc[-1])
        width = up_v - low_v
        rsi_val = float(ind.rsi(df["close"]).iloc[-1])
        atr_val = float(ind.atr(df).iloc[-1])

        if width <= 0 or atr_val <= 0:
            return Decision(Action.HOLD, Direction.FLAT, 0.0, regime, "밴드/ATR 무효")

        # 밴드 내 위치 (0=하단, 1=상단)
        band_pos = (price - low_v) / width
        score = clamp((0.5 - band_pos) * 2 * (1.0 if trend_up else -1.0))
        comp = [SignalResult("mid", score, {
            "trend_up": trend_up, "band_pos": round(band_pos, 3),
            "rsi": round(rsi_val, 1), "bb_mid": round(mid_v, 4),
        })]

        # --- 청산: 상위 추세 반전 ---
        if current_direction is Direction.LONG and not trend_up:
            return Decision(Action.CLOSE, Direction.FLAT, score, regime, "1h 추세 하방 반전", comp)
        if current_direction is Direction.SHORT and trend_up:
            return Decision(Action.CLOSE, Direction.FLAT, score, regime, "1h 추세 상방 반전", comp)
        if current_direction is not None:
            return Decision(Action.HOLD, Direction.FLAT, score, regime, "포지션 유지", comp)

        # --- 진입: 추세 방향 눌림목 ---
        if trend_up and band_pos <= self.band_zone and rsi_val <= self.rsi_long_max:
            d = Decision(Action.OPEN_LONG, Direction.LONG, score, regime,
                         f"상승추세 밴드하단 눌림(pos={band_pos:.2f})", comp)
            d.stop_price = price - self.sl_atr_mult * atr_val
            d.take_profit = mid_v                     # 평균회귀 목표: 중심선
            return d
        if (not trend_up) and band_pos >= 1.0 - self.band_zone and rsi_val >= self.rsi_short_min:
            d = Decision(Action.OPEN_SHORT, Direction.SHORT, score, regime,
                         f"하락추세 밴드상단 반등(pos={band_pos:.2f})", comp)
            d.stop_price = price + self.sl_atr_mult * atr_val
            d.take_profit = mid_v
            return d
        return Decision(Action.HOLD, Direction.FLAT, score, regime, "관망", comp)
