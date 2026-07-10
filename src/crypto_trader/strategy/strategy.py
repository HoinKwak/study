"""전략 결정 로직 — 시그널 + 레짐 + 현재 포지션 → 행동(Action).

엔진(라이브)과 백테스터가 이 클래스를 공유해 결과 일관성을 보장한다.

결정 규칙:
  1) 레짐 감지 → 레짐별 기술지표 가중치 적용
  2) 기술 + 파생 시그널을 가중 합산
  3) 포지션 없음:
       - |score| ≥ entry_threshold → OPEN_LONG/OPEN_SHORT
       - 아니면 HOLD
  4) 포지션 보유 중:
       - 시그널이 반대로 강하게 뒤집힘(|반대 score| ≥ exit_flip_threshold) → CLOSE
       - 아니면 HOLD (SL/TP 는 리스크/엔진이 별도로 관리)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

import pandas as pd

from ..config import Settings
from ..signals import DerivativesSignals, SignalAggregator, TechnicalSignals
from ..signals.base import Direction, SignalResult
from .regime import Regime, detect_regime


class Action(str, Enum):
    OPEN_LONG = "open_long"
    OPEN_SHORT = "open_short"
    CLOSE = "close"
    HOLD = "hold"


@dataclass
class Decision:
    action: Action
    direction: Direction          # 진입 목표 방향(HOLD/CLOSE 시 FLAT)
    score: float
    regime: Regime
    reason: str = ""
    components: list[SignalResult] = field(default_factory=list)

    def summary(self) -> str:
        comp = ", ".join(f"{c.name}={c.score:+.2f}" for c in self.components)
        return (f"score={self.score:+.3f} regime={self.regime.value} "
                f"→ {self.action.value} [{comp}] {self.reason}")


class Strategy:
    def __init__(self, settings: Settings,
                 aggregator: SignalAggregator | None = None,
                 exit_flip_threshold: float | None = None):
        self.s = settings
        self.tech = TechnicalSignals()
        self.deriv = DerivativesSignals()
        self.aggregator = aggregator or SignalAggregator(
            entry_threshold=settings.entry_score_threshold)
        # 포지션 반대 시그널이 이 강도 이상이면 조기 청산
        self.exit_flip_threshold = (
            exit_flip_threshold if exit_flip_threshold is not None
            else settings.exit_flip_threshold)

    def decide(self, symbol: str, df: pd.DataFrame,
               deriv_snap: dict | None = None,
               current_direction: Direction | None = None) -> Decision:
        regime, _adx = detect_regime(df)
        tech_sig = self.tech.compute(df, regime.value)
        deriv_sig = self.deriv.compute(deriv_snap or {})
        agg = self.aggregator.aggregate(symbol, [tech_sig, deriv_sig])
        score = agg.score
        components = [tech_sig, deriv_sig]

        # --- 포지션 보유 중: 반전 청산 우선 판단 ---
        if current_direction is Direction.LONG:
            if score <= -self.exit_flip_threshold:
                return Decision(Action.CLOSE, Direction.FLAT, score, regime,
                                "시그널 하방 반전", components)
            return Decision(Action.HOLD, Direction.FLAT, score, regime, "롱 유지", components)
        if current_direction is Direction.SHORT:
            if score >= self.exit_flip_threshold:
                return Decision(Action.CLOSE, Direction.FLAT, score, regime,
                                "시그널 상방 반전", components)
            return Decision(Action.HOLD, Direction.FLAT, score, regime, "숏 유지", components)

        # --- 포지션 없음: 진입 판단 ---
        if agg.direction is Direction.LONG:
            return Decision(Action.OPEN_LONG, Direction.LONG, score, regime,
                            "롱 진입 시그널", components)
        if agg.direction is Direction.SHORT:
            return Decision(Action.OPEN_SHORT, Direction.SHORT, score, regime,
                            "숏 진입 시그널", components)
        return Decision(Action.HOLD, Direction.FLAT, score, regime, "관망", components)
