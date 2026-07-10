"""단타(scalp) 전략 — 볼린저밴드 이탈 + 거래량 급증 + OI 증감.

1분봉 종가 확정 시:
  진입: 거래량 급증 + 볼린저밴드 이탈하는 강한 양봉/음봉 (OI 동반 증가 시 강화)
        양봉 → LONG, 음봉 → SHORT
  SL  : 신호 봉의 시가(open)
  TP  : max/min( 손익비 기반 목표,  신호 봉의 고가/저가 )
  청산: 확인 TF(5m) 레짐이 RANGE(횡보) 로 전환되면 종료
        (SL/TP 도달은 리스크/거래소가 별도 관리)

체결은 워커가 use_twap=True 를 보고 다음 N분간 TWAP 분할 진입한다.
"""
from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from ..config import Settings
from ..signals import indicators as ind
from ..signals.base import Direction
from .regime import Regime
from .strategy import Action


@dataclass
class ScalpDecision:
    action: Action
    direction: Direction
    entry_ref: float = 0.0       # 참조 진입가(신호봉 종가)
    stop_price: float = 0.0
    take_profit: float = 0.0
    signal_high: float = 0.0     # 신호봉 고가 (모멘텀 청산 기준)
    signal_low: float = 0.0      # 신호봉 저가
    use_twap: bool = False
    reason: str = ""
    detail: dict | None = None

    def summary(self) -> str:
        if self.action in (Action.OPEN_LONG, Action.OPEN_SHORT):
            return (f"{self.action.value} entry~{self.entry_ref:.4f} "
                    f"SL {self.stop_price:.4f} TP {self.take_profit:.4f} ({self.reason})")
        return f"{self.action.value} ({self.reason})"


class ScalpStrategy:
    def __init__(self, settings: Settings,
                 bb_period: int = 20, bb_std: float = 2.0,
                 vol_lookback: int = 20, vol_spike_mult: float = 4.0,
                 strong_body_frac: float = 0.6, min_body_atr: float = 1.0,
                 min_tp_frac: float = 0.0008,
                 reward_risk_ratio: float | None = None):
        self.s = settings
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.vol_lookback = vol_lookback
        self.vol_spike_mult = vol_spike_mult
        self.strong_body_frac = strong_body_frac  # 몸통이 전체 레인지의 이 비율 이상이면 '강봉'
        self.min_body_atr = min_body_atr          # 몸통이 ATR 의 이 배수 이상이어야 유의미
        self.min_tp_frac = min_tp_frac            # 최소 익절 거리 (가격 대비, 0.0008=0.08%)
        self.rr = reward_risk_ratio if reward_risk_ratio is not None else settings.reward_risk_ratio

    def decide(self, symbol: str, df: pd.DataFrame,
               oi_delta: float | None = None,
               current_direction: Direction | None = None,
               confirm_regime: Regime | None = None) -> ScalpDecision:
        if len(df) < self.bb_period + 2:
            return ScalpDecision(Action.HOLD, Direction.FLAT, reason="데이터 부족")

        # --- 보유 중: 횡보장 전환 시 청산 ---
        if current_direction is not None:
            if confirm_regime is Regime.RANGE:
                return ScalpDecision(Action.CLOSE, Direction.FLAT, reason="횡보장 전환 청산")
            return ScalpDecision(Action.HOLD, Direction.FLAT, reason="추세 유지")

        # --- 진입 판단: 마지막 확정봉 ---
        _mid, upper, lower = ind.bollinger_bands(df["close"], self.bb_period, self.bb_std)
        bar = df.iloc[-1]
        o, h, l, c = float(bar["open"]), float(bar["high"]), float(bar["low"]), float(bar["close"])
        up_band = float(upper.iloc[-1])
        low_band = float(lower.iloc[-1])
        rng = h - l
        if rng <= 0:
            return ScalpDecision(Action.HOLD, Direction.FLAT, reason="레인지 0")

        # 거래량 급증
        vol = df["volume"]
        avg_vol = float(vol.iloc[-(self.vol_lookback + 1):-1].mean())
        vol_spike = avg_vol > 0 and float(bar["volume"]) >= self.vol_spike_mult * avg_vol

        # 강봉: 몸통 비율 + 절대 크기(ATR 대비) 둘 다 요구
        body = abs(c - o)
        body_frac = body / rng
        atr_val = float(ind.atr(df).iloc[-1]) if len(df) >= 15 else 0.0
        strong = (body_frac >= self.strong_body_frac
                  and (atr_val <= 0 or body >= self.min_body_atr * atr_val))

        # 볼린저 이탈 + 방향
        bull_breakout = c > up_band and c > o
        bear_breakout = c < low_band and c < o

        # OI 동반 증가 확인(있으면). None 이면 통과, 있으면 증가 요구.
        oi_ok = (oi_delta is None) or (oi_delta > 0)

        # 확인 TF(5m) 추세 필터: 횡보장(RANGE)에선 진입 금지,
        # 추세장에선 돌파 방향이 추세와 일치할 때만 진입.
        # (1m 돌파는 무추세 구간에서 대부분 되돌림 → 백테스트로 확인됨)
        long_regime_ok = confirm_regime is None or confirm_regime is Regime.TREND_UP
        short_regime_ok = confirm_regime is None or confirm_regime is Regime.TREND_DOWN

        detail = {
            "vol_spike": vol_spike, "body_frac": round(body_frac, 3),
            "up_band": round(up_band, 4), "low_band": round(low_band, 4),
            "oi_delta": oi_delta,
            "confirm_regime": confirm_regime.value if confirm_regime else None,
        }

        if vol_spike and strong and oi_ok and bull_breakout and long_regime_ok:
            return self._entry(Direction.LONG, o, h, l, c, detail)
        if vol_spike and strong and oi_ok and bear_breakout and short_regime_ok:
            return self._entry(Direction.SHORT, o, h, l, c, detail)

        return ScalpDecision(Action.HOLD, Direction.FLAT, reason="진입 조건 미충족", detail=detail)

    def _entry(self, direction: Direction, o: float, h: float, l: float, c: float,
               detail: dict) -> ScalpDecision:
        entry = c  # 참조 진입가(실제는 TWAP 평균)
        min_tp_dist = entry * self.min_tp_frac    # 최소 익절 거리(수수료를 이겨야 함)
        if direction is Direction.LONG:
            stop = o                          # 신호봉 시가
            risk = max(entry - stop, 1e-9)
            tp = max(h, entry + self.rr * risk, entry + min_tp_dist)
            action = Action.OPEN_LONG
        else:
            stop = o
            risk = max(stop - entry, 1e-9)
            tp = min(l, entry - self.rr * risk, entry - min_tp_dist)
            action = Action.OPEN_SHORT
        return ScalpDecision(action, direction, entry_ref=entry, stop_price=stop,
                             take_profit=tp, signal_high=h, signal_low=l, use_twap=True,
                             reason="볼린저 이탈 강봉+거래량 급증", detail=detail)
