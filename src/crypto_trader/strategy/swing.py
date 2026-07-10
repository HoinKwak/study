"""중장기(swing) 전략 — RSI 역추세 → 슈퍼트렌드 피라미딩 → Fib+CVD 익절.

1단계 (역추세 초기 진입):
  - RSI ≤ rsi_os(20) → LONG, RSI ≥ rsi_ob(80) → SHORT
  - 초기 슬리브 예산의 stage1_init(30%) 진입, 시계열 TWAP 로 stage1_max(60%)까지 증량
  - SL: 최근 스윙 저/고점(구조) 기준
2단계 (추세 확인 피라미딩):
  - 1단계 SL 미도달 + 가격이 목표 방향으로 반전 + 슈퍼트렌드가 진입 방향 확인
  - 슬리브 예산의 stage2_max(100%)까지 추가, SL 을 슈퍼트렌드 라인으로 재설정
익절(TP):
  - 직전 스윙 고/저점 기준 피보나치 되돌림(기본 0.618) + CVD 모멘텀으로 목표 조정

배분 비율은 '슬리브 예산' 기준(슬리브=계좌 50% → 30/60/100% = 계좌 15/30/50%).
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ..config import Settings
from ..signals import indicators as ind
from ..signals.base import Direction
from .strategy import Action


@dataclass
class SwingPosition:
    direction: Direction
    stage: int
    alloc_frac: float     # 누적 사용 비율(슬리브 예산 대비)
    avg_entry: float
    stop_price: float


@dataclass
class SwingDecision:
    action: Action
    direction: Direction
    target_frac: float = 0.0   # 목표 누적 비율(슬리브 예산 대비)
    stage: int = 1
    stop_price: float = 0.0
    take_profit: float = 0.0
    reason: str = ""

    def summary(self) -> str:
        if self.action in (Action.OPEN_LONG, Action.OPEN_SHORT, Action.ADD):
            return (f"{self.action.value} {self.direction.value} →{self.target_frac:.0%} "
                    f"stage{self.stage} SL {self.stop_price:.4f} TP {self.take_profit:.4f} "
                    f"({self.reason})")
        return f"{self.action.value} ({self.reason})"


class SwingStrategy:
    def __init__(self, settings: Settings,
                 rsi_os: float = 20.0, rsi_ob: float = 80.0,
                 stage1_init: float = 0.30, stage1_max: float = 0.60,
                 stage2_max: float = 1.00,
                 st_period: int = 10, st_mult: float = 3.0,
                 sl_swing_lookback: int = 20, sl_buffer_atr: float = 1.5,
                 fib_ratio: float = 0.618, swing_lookback: int = 60,
                 require_rsi_turn: bool = True):
        self.s = settings
        self.rsi_os = rsi_os
        self.rsi_ob = rsi_ob
        self.stage1_init = stage1_init
        self.stage1_max = stage1_max
        self.stage2_max = stage2_max
        self.st_period = st_period
        self.st_mult = st_mult
        self.sl_swing_lookback = sl_swing_lookback
        self.sl_buffer_atr = sl_buffer_atr
        self.fib_ratio = fib_ratio
        self.swing_lookback = swing_lookback
        self.require_rsi_turn = require_rsi_turn

    def decide(self, symbol: str, df: pd.DataFrame,
               confirm_df: pd.DataFrame | None = None,
               position: SwingPosition | None = None) -> SwingDecision:
        if len(df) < max(self.swing_lookback, 40):
            return SwingDecision(Action.HOLD, Direction.FLAT, reason="데이터 부족")

        price = float(df["close"].iloc[-1])
        rsi_series = ind.rsi(df["close"])
        rsi_val = float(rsi_series.iloc[-1])
        rsi_prev = float(rsi_series.iloc[-2]) if len(rsi_series) > 1 else rsi_val
        atr_val = float(ind.atr(df).iloc[-1])
        st_line, st_dir = ind.supertrend(confirm_df if confirm_df is not None else df,
                                         self.st_period, self.st_mult)
        st_direction = int(st_dir.iloc[-1])
        st_value = float(st_line.iloc[-1])

        # ---------------- 신규 진입 (역추세) ----------------
        # require_rsi_turn: RSI 가 극단에서 '돌아서는' 것을 확인하고 진입
        # (떨어지는 칼날/천장 돌파 추격 방지)
        if position is None:
            long_trigger = (rsi_val <= self.rsi_os and
                            (not self.require_rsi_turn or rsi_val > rsi_prev))
            short_trigger = (rsi_val >= self.rsi_ob and
                             (not self.require_rsi_turn or rsi_val < rsi_prev))
            if long_trigger:
                stop = self._swing_stop(df, Direction.LONG, atr_val)
                tp = self._fib_cvd_tp(df, Direction.LONG, price)
                return SwingDecision(Action.OPEN_LONG, Direction.LONG, self.stage1_init, 1,
                                     stop, tp, f"RSI {rsi_val:.0f} 과매도 반등 롱")
            if short_trigger:
                stop = self._swing_stop(df, Direction.SHORT, atr_val)
                tp = self._fib_cvd_tp(df, Direction.SHORT, price)
                return SwingDecision(Action.OPEN_SHORT, Direction.SHORT, self.stage1_init, 1,
                                     stop, tp, f"RSI {rsi_val:.0f} 과매수 반락 숏")
            return SwingDecision(Action.HOLD, Direction.FLAT, reason="RSI 극단/전환 아님")

        # ---------------- 보유 중 ----------------
        d = position.direction
        favorable = (price > position.avg_entry) if d is Direction.LONG else (price < position.avg_entry)
        st_confirms = (st_direction > 0 and d is Direction.LONG) or \
                      (st_direction < 0 and d is Direction.SHORT)

        if position.stage == 1:
            # 2단계 전환: 반전 + 슈퍼트렌드 확인 → 피라미딩 & SL 재설정
            if favorable and st_confirms and position.alloc_frac < self.stage2_max:
                new_stop = self._trail_stop(d, st_value, position.stop_price)
                tp = self._fib_cvd_tp(df, d, position.avg_entry)
                return SwingDecision(Action.ADD, d, self.stage2_max, 2, new_stop, tp,
                                     "슈퍼트렌드 확인 피라미딩(2단계)")
            # 1단계 TWAP 증량 (최대 stage1_max)
            if position.alloc_frac < self.stage1_max - 1e-9:
                tp = self._fib_cvd_tp(df, d, position.avg_entry)
                return SwingDecision(Action.ADD, d, self.stage1_max, 1,
                                     position.stop_price, tp, "1단계 TWAP 증량")
            return SwingDecision(Action.HOLD, Direction.FLAT, reason="1단계 유지")

        # 2단계: 슈퍼트렌드 라인으로 트레일링 SL 갱신하며 보유
        if position.stage >= 2:
            new_stop = self._trail_stop(d, st_value, position.stop_price)
            if new_stop != position.stop_price:
                tp = self._fib_cvd_tp(df, d, position.avg_entry)
                return SwingDecision(Action.ADD, d, position.alloc_frac, 2, new_stop, tp,
                                     "트레일링 SL 갱신")
            return SwingDecision(Action.HOLD, Direction.FLAT, reason="2단계 유지")

        return SwingDecision(Action.HOLD, Direction.FLAT, reason="유지")

    # -------------------------------------------------------- 헬퍼

    def _swing_stop(self, df: pd.DataFrame, direction: Direction, atr_val: float) -> float:
        lb = self.sl_swing_lookback
        buf = self.sl_buffer_atr * atr_val
        if direction is Direction.LONG:
            return float(df["low"].iloc[-lb:].min()) - buf
        return float(df["high"].iloc[-lb:].max()) + buf

    @staticmethod
    def _trail_stop(direction: Direction, st_value: float, current_stop: float) -> float:
        """슈퍼트렌드 라인 방향으로만 SL 을 조인다(되돌리지 않음)."""
        if direction is Direction.LONG:
            return max(current_stop, st_value)
        return min(current_stop, st_value) if current_stop > 0 else st_value

    def _fib_cvd_tp(self, df: pd.DataFrame, direction: Direction, entry: float) -> float:
        """직전 스윙 고/저 기준 피보나치 되돌림 + CVD 모멘텀으로 TP 산정."""
        lb = self.swing_lookback
        swing_high = float(df["high"].iloc[-lb:].max())
        swing_low = float(df["low"].iloc[-lb:].min())
        span = swing_high - swing_low
        if span <= 0:
            return entry * (1.02 if direction is Direction.LONG else 0.98)

        # CVD 모멘텀: 최근 상승/하락 압력으로 되돌림 목표를 확장/축소
        cvd = ind.cvd_proxy(df)
        cvd_slope = float(cvd.iloc[-1] - cvd.iloc[-min(len(cvd), 10)])
        ratio = self.fib_ratio
        if direction is Direction.LONG and cvd_slope > 0:
            ratio = min(0.786, ratio + 0.168)   # 매수압력 강하면 더 멀리
        elif direction is Direction.SHORT and cvd_slope < 0:
            ratio = min(0.786, ratio + 0.168)

        if direction is Direction.LONG:
            tp = swing_low + ratio * span
            return max(tp, entry * 1.005)       # 최소한 진입가 위
        tp = swing_high - ratio * span
        return min(tp, entry * 0.995)
