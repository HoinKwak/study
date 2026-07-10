"""중기(mid) 전략 — 상위 TF 추세 + 하위 TF 눌림목 진입.

15m 시그널 / 1h 확인:
  - 1h 슈퍼트렌드로 추세 방향 확정
  - 15m MACD 히스토그램이 추세 방향으로 0선을 교차(모멘텀 재개)할 때 진입
    (RSI 과열/과매도 구간이 아닐 때만)
청산:
  - 1h 추세 반전, 또는 15m MACD 역전 교차 → CLOSE
  - SL/TP 는 리스크 매니저(ATR)가 관리
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
                 rsi_long_cap: float = 70.0, rsi_short_floor: float = 30.0,
                 min_hist_frac: float = 0.0003):
        self.s = settings
        self.st_period = st_period
        self.st_mult = st_mult
        self.rsi_long_cap = rsi_long_cap
        self.rsi_short_floor = rsi_short_floor
        # MACD 히스토그램이 가격 대비 이 비율보다 커야 유효 교차로 인정(휩쏘 필터)
        self.min_hist_frac = min_hist_frac

    def decide(self, symbol: str, df: pd.DataFrame,
               confirm_df: pd.DataFrame | None = None,
               current_direction: Direction | None = None) -> Decision:
        regime, _ = detect_regime(df)
        if len(df) < 40 or confirm_df is None or len(confirm_df) < 20:
            return Decision(Action.HOLD, Direction.FLAT, 0.0, regime, "데이터 부족")

        # 상위 TF 추세
        _st, st_dir = ind.supertrend(confirm_df, self.st_period, self.st_mult)
        trend_up = int(st_dir.iloc[-1]) > 0

        # 하위 TF 모멘텀(MACD 히스토그램 0선 교차)
        _m, _sig, hist = ind.macd(df["close"])
        h_now, h_prev = float(hist.iloc[-1]), float(hist.iloc[-2])
        price = float(df["close"].iloc[-1])
        # 교차가 유의미한 크기여야 인정 (미세 진동 휩쏘 제거)
        significant = abs(h_now) >= self.min_hist_frac * price
        cross_up = h_prev <= 0 < h_now and significant
        cross_down = h_prev >= 0 > h_now and significant

        rsi_val = float(ind.rsi(df["close"]).iloc[-1])
        score = clamp((1.0 if trend_up else -1.0) * min(1.0, abs(h_now) * 50))
        comp = [SignalResult("mid", score, {"trend_up": trend_up, "rsi": round(rsi_val, 1),
                                            "macd_hist": round(h_now, 5)})]

        # --- 청산 판단 ---
        if current_direction is Direction.LONG:
            if not trend_up or cross_down:
                return Decision(Action.CLOSE, Direction.FLAT, score, regime, "추세 반전/모멘텀 역전", comp)
            return Decision(Action.HOLD, Direction.FLAT, score, regime, "롱 유지", comp)
        if current_direction is Direction.SHORT:
            if trend_up or cross_up:
                return Decision(Action.CLOSE, Direction.FLAT, score, regime, "추세 반전/모멘텀 역전", comp)
            return Decision(Action.HOLD, Direction.FLAT, score, regime, "숏 유지", comp)

        # --- 진입 판단 ---
        if trend_up and cross_up and rsi_val < self.rsi_long_cap:
            return Decision(Action.OPEN_LONG, Direction.LONG, score, regime, "상승추세 눌림목 롱", comp)
        if (not trend_up) and cross_down and rsi_val > self.rsi_short_floor:
            return Decision(Action.OPEN_SHORT, Direction.SHORT, score, regime, "하락추세 반등 숏", comp)
        return Decision(Action.HOLD, Direction.FLAT, score, regime, "관망", comp)
