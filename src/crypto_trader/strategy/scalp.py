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
                 vol_lookback: int = 20, vol_spike_mult: float | None = None,
                 strong_body_frac: float = 0.6, min_body_atr: float | None = None,
                 min_tp_frac: float = 0.0012,
                 reward_risk_ratio: float | None = None,
                 squeeze_pctile: float | None = -1.0,
                 squeeze_lookback: int = 50,
                 require_regime: bool | None = None):
        self.s = settings
        self.bb_period = bb_period
        self.bb_std = bb_std
        self.vol_lookback = vol_lookback
        # 라이브 튜닝: 명시 인자 없으면 .env(settings)의 SCALP_* 값을 기본으로 사용
        self.vol_spike_mult = (vol_spike_mult if vol_spike_mult is not None
                               else getattr(settings, "scalp_vol_spike_mult", 3.0))
        self.strong_body_frac = strong_body_frac  # 몸통이 전체 레인지의 이 비율 이상이면 '강봉'
        # 몸통이 ATR 의 이 배수 이상이어야 유의미
        self.min_body_atr = (min_body_atr if min_body_atr is not None
                             else getattr(settings, "scalp_min_body_atr", 0.7))
        self.min_tp_frac = min_tp_frac            # 최소 익절 거리 (가격 대비). 테이커 진입 시
                                                  # 왕복 수수료 0.1% 를 넘겨야 하므로 0.12% 기본
        self.rr = reward_risk_ratio if reward_risk_ratio is not None else settings.reward_risk_ratio
        # 볼린저 스퀴즈 전제: 신호봉 직전 밴드폭이 최근 N봉 분포의 하위 pctile% 이하일
        # 때만 진입 허용. 밴드 확장 후의 늦은 돌파(대부분 되돌림)를 차단.
        # (None=비활성, 100=사실상 비활성). 명시 없으면 .env 값 사용.
        self.squeeze_pctile = (squeeze_pctile if squeeze_pctile != -1.0
                               else getattr(settings, "scalp_squeeze_pctile", 45.0))
        self.squeeze_lookback = squeeze_lookback
        # 확인 TF 추세 게이트(횡보장 진입 금지). 완화하려면 False.
        self.require_regime = (require_regime if require_regime is not None
                               else getattr(settings, "scalp_require_regime", True))
        # 횡보 전환 청산 시 모멘텀 꺾임 확인 봉수(0=RANGE 즉시 청산).
        self.chop_confirm_bars = int(getattr(settings, "scalp_chop_confirm_bars", 2))
        # SL 거리 배수: 신호봉 시가 기준 손절거리(entry-open)를 이 배수만큼 넓힌다.
        # 1.0=신호봉 시가(기존), >1 이면 더 멀리(노이즈 손절 완화). 리스크기준 사이징에선
        # 손절이 멀수록 포지션이 작아진다(건당 리스크 일정).
        self.stop_mult = float(getattr(settings, "scalp_stop_mult", 1.0))

    def _momentum_faded(self, df: pd.DataFrame, direction: Direction) -> bool:
        """모멘텀 꺾임 판정 — 최근 N봉이 신고가/신저가를 못 만들고 마지막 봉이 역방향.

        chop_confirm_bars=0 이면 항상 True(=RANGE 즉시 청산, 기존 동작).
        데이터가 부족하면 보수적으로 True(청산 허용).
        """
        n = self.chop_confirm_bars
        if n <= 0:
            return True
        if len(df) < n + 2:
            return True
        recent = df.iloc[-n:]
        last_c = float(recent["close"].iloc[-1])
        last_o = float(recent["open"].iloc[-1])
        if direction is Direction.LONG:
            prior_high = float(df["high"].iloc[-(n + 1)])
            no_new_high = all(float(recent["high"].iloc[i]) <= prior_high for i in range(n))
            return no_new_high and last_c < last_o   # 신고가 실패 + 마지막 음봉
        prior_low = float(df["low"].iloc[-(n + 1)])
        no_new_low = all(float(recent["low"].iloc[i]) >= prior_low for i in range(n))
        return no_new_low and last_c > last_o         # 신저가 실패 + 마지막 양봉

    def decide(self, symbol: str, df: pd.DataFrame,
               oi_delta: float | None = None,
               current_direction: Direction | None = None,
               confirm_regime: Regime | None = None) -> ScalpDecision:
        if len(df) < self.bb_period + 2:
            return ScalpDecision(Action.HOLD, Direction.FLAT, reason="데이터 부족")

        # --- 보유 중: 횡보장 전환 시 청산 (모멘텀이 실제로 꺾였을 때만) ---
        if current_direction is not None:
            if confirm_regime is Regime.RANGE and self._momentum_faded(df, current_direction):
                return ScalpDecision(Action.CLOSE, Direction.FLAT, reason="횡보장 전환 청산")
            return ScalpDecision(Action.HOLD, Direction.FLAT, reason="추세 유지")

        # --- 진입 판단: 마지막 확정봉 ---
        _mid, upper, lower = ind.bollinger_bands(df["close"], self.bb_period, self.bb_std)

        # [스퀴즈 필터] 밴드폭(정규화)이 하위 분위 이하일 때만 돌파를 신뢰
        if self.squeeze_pctile is not None:
            bw = (upper - lower) / _mid.replace(0.0, float("nan"))
            valid = bw.dropna()
            if len(valid) < self.squeeze_lookback + 2:
                return ScalpDecision(Action.HOLD, Direction.FLAT, reason="스퀴즈 데이터 부족")
            bw_prev = float(bw.iloc[-2])  # 신호봉 '직전' 봉 기준
            dist = bw.iloc[-(self.squeeze_lookback + 1):-1].dropna()
            threshold = float(dist.quantile(self.squeeze_pctile / 100.0))
            if not (bw_prev <= threshold):
                return ScalpDecision(Action.HOLD, Direction.FLAT, reason="스퀴즈 아님")

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

        # 확인 TF 추세 필터. require_regime=True(엄격): 추세 일치할 때만 진입.
        # False(완화): 횡보(RANGE)도 허용하되 명확한 역추세만 차단 → 진입 빈도↑.
        if self.require_regime:
            long_regime_ok = confirm_regime is None or confirm_regime is Regime.TREND_UP
            short_regime_ok = confirm_regime is None or confirm_regime is Regime.TREND_DOWN
        else:
            long_regime_ok = confirm_regime is not Regime.TREND_DOWN
            short_regime_ok = confirm_regime is not Regime.TREND_UP

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
            stop = entry - self.stop_mult * (entry - o)   # 신호봉 시가 기준, 배수만큼 확장
            risk = max(entry - stop, 1e-9)
            tp = max(h, entry + self.rr * risk, entry + min_tp_dist)
            action = Action.OPEN_LONG
        else:
            stop = entry + self.stop_mult * (o - entry)
            risk = max(stop - entry, 1e-9)
            tp = min(l, entry - self.rr * risk, entry - min_tp_dist)
            action = Action.OPEN_SHORT
        return ScalpDecision(action, direction, entry_ref=entry, stop_price=stop,
                             take_profit=tp, signal_high=h, signal_low=l, use_twap=True,
                             reason="볼린저 이탈 강봉+거래량 급증", detail=detail)
