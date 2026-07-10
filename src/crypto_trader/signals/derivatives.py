"""바이낸스 네이티브 파생 데이터 시그널.

입력: BinanceDerivativesData.snapshot() 결과 dict.
  - funding_rate          : 펀딩비 (양수 = 롱 과열)
  - oi_change_pct         : OI 변화율(%)
  - global_ls_ratio       : 일반 계좌 롱숏 비율 (군중)
  - top_trader_ls_ratio   : 상위 트레이더 포지션 롱숏 비율 (스마트머니)
  - taker_buy_sell_ratio  : 테이커 매수/매도 비율 (청산 데이터 대체)

전략 방향성:
  * 펀딩비 과열 → 역추세 (군중 반대). 펀딩 매우 높으면 숏, 매우 낮(음수)으면 롱.
  * 일반 계좌 롱숏도 역추세 (군중은 종종 틀림).
  * 상위 트레이더 롱숏은 순추세 (스마트머니 추종).
  * 테이커 매수/매도는 순추세 (실제 시장가 압력).
  * OI 변화는 방향 강화 필터로만 사용(단독 방향성 약함) → detail 로 노출.
"""
from __future__ import annotations

from .base import SignalResult, clamp

# 서브 지표 가중치 (합 1.0)
SUB_WEIGHTS = {
    "funding": 0.30,
    "global_ls": 0.25,
    "top_trader_ls": 0.25,
    "taker": 0.20,
}


class DerivativesSignals:
    def __init__(self,
                 funding_hot: float = 0.0005,   # 8h 기준 0.05% 이상이면 과열
                 ls_neutral: float = 1.0):
        self.funding_hot = funding_hot
        self.ls_neutral = ls_neutral

    def compute(self, snap: dict[str, float | None]) -> SignalResult:
        parts: dict[str, float] = {}
        weights_used = 0.0
        total = 0.0

        funding = snap.get("funding_rate")
        if funding is not None:
            s = self._funding_score(funding)
            parts["funding"] = round(s, 3)
            total += SUB_WEIGHTS["funding"] * s
            weights_used += SUB_WEIGHTS["funding"]

        g_ls = snap.get("global_ls_ratio")
        if g_ls is not None:
            s = self._contrarian_ls_score(g_ls)
            parts["global_ls"] = round(s, 3)
            total += SUB_WEIGHTS["global_ls"] * s
            weights_used += SUB_WEIGHTS["global_ls"]

        t_ls = snap.get("top_trader_ls_ratio")
        if t_ls is not None:
            s = self._trend_ls_score(t_ls)
            parts["top_trader_ls"] = round(s, 3)
            total += SUB_WEIGHTS["top_trader_ls"] * s
            weights_used += SUB_WEIGHTS["top_trader_ls"]

        taker = snap.get("taker_buy_sell_ratio")
        if taker is not None:
            s = self._taker_score(taker)
            parts["taker"] = round(s, 3)
            total += SUB_WEIGHTS["taker"] * s
            weights_used += SUB_WEIGHTS["taker"]

        # 사용 가능한 지표 가중치로 정규화
        score = total / weights_used if weights_used > 0 else 0.0

        detail = {
            "parts": parts,
            "oi_change_pct": snap.get("oi_change_pct"),
            "coverage": round(weights_used, 2),
        }
        return SignalResult("derivatives", clamp(score), detail)

    # ------------------------------------------------------------- 서브 점수

    def _funding_score(self, funding: float) -> float:
        """펀딩 과열 역추세. +펀딩(롱 과열)=숏(-), -펀딩(숏 과열)=롱(+)."""
        return clamp(-funding / self.funding_hot)

    def _contrarian_ls_score(self, ratio: float) -> float:
        """일반 계좌 롱숏 역추세. 롱 쏠림(>1)=숏, 숏 쏠림(<1)=롱."""
        # ratio 1.0 = 중립, 2.0 이상이면 강한 롱 쏠림
        deviation = ratio - self.ls_neutral
        return clamp(-deviation)

    def _trend_ls_score(self, ratio: float) -> float:
        """상위 트레이더 순추세. 롱 우세(>1)=롱(+)."""
        return clamp(ratio - self.ls_neutral)

    def _taker_score(self, ratio: float) -> float:
        """테이커 매수/매도 순추세. 매수 우세(>1)=롱(+)."""
        return clamp(ratio - 1.0)
