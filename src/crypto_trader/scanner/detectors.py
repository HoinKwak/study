"""이벤트 감지 순수 함수 — 숫자 시계열만 받아 판정한다(네트워크/상태 없음).

각 함수는 조건 미충족 시 None, 충족 시 (대표수치, 상세문자열) 튜플을 반환한다.
값 해석은 호출부(MarketScanner)가 ScanEvent 로 감싼다. 테스트하기 쉽게 순수 유지.
"""
from __future__ import annotations


def price_move(closes: list[float], window: int, threshold_pct: float
               ) -> tuple[float, str] | None:
    """최근 `window` 캔들 동안의 종가 변동률. |변동%| ≥ 임계면 반환.

    반환 (변동%, 상세). 양수=급등, 음수=급락.
    """
    if window < 1 or len(closes) < window + 1:
        return None
    old = closes[-1 - window]
    cur = closes[-1]
    if old <= 0:
        return None
    pct = (cur - old) / old * 100.0
    if abs(pct) < threshold_pct:
        return None
    return pct, f"{pct:+.2f}% ({window}캔들)"


def volume_spike(volumes: list[float], lookback: int, mult: float
                 ) -> tuple[float, str] | None:
    """직전(마지막) 캔들 거래량 / 그 이전 lookback 평균 ≥ mult 이면 반환.

    반환 (배수, 상세). 호출부는 마지막 원소가 '닫힌 캔들'이 되도록 넘겨야 한다.
    """
    if lookback < 2 or len(volumes) < lookback + 1:
        return None
    baseline = volumes[-1 - lookback:-1]
    avg = sum(baseline) / len(baseline)
    if avg <= 0:
        return None
    ratio = volumes[-1] / avg
    if ratio < mult:
        return None
    return ratio, f"평균 대비 {ratio:.1f}배"


def capitulation(volumes: list[float], closes: list[float], lookback: int,
                 mult: float, min_drawdown_pct: float
                 ) -> tuple[float, str] | None:
    """바닥급 대형 캐피출레이션: 거래량 급증(≥mult배) + 하락 국면(최근 고점比 ≥임계%↓).

    바닥 캐피출레이션의 공통특징(리서치): 15m 선물 거래량이 평상시의 수십 배로 튀며
    가격은 최근 고점 대비 크게 밀린 상태. 일반 거래량 급증(vol_spike)보다 훨씬 높은
    배수 + 하락국면 조건을 함께 요구해 '바닥/투매 정점'만 잡는다.
    마지막(-1) 원소가 '닫힌 캔들'이어야 한다(호출부에서 진행 중 캔들 제외).
    반환 (거래량배수, 상세). 조건 미충족이면 None.
    """
    if lookback < 2 or len(volumes) < lookback + 1 or len(closes) < lookback + 1:
        return None
    baseline = volumes[-1 - lookback:-1]
    avg = sum(baseline) / len(baseline)
    if avg <= 0:
        return None
    ratio = volumes[-1] / avg
    if ratio < mult:
        return None
    recent_high = max(closes[-lookback:])
    dd = (recent_high - closes[-1]) / recent_high if recent_high > 0 else 0.0
    if dd * 100 < min_drawdown_pct:
        return None
    return ratio, f"거래량 평균 대비 {ratio:.1f}배 · 최근고점比 {dd * 100:.1f}%↓"


def oi_move(oi_series: list[float], lookback: int, threshold_pct: float
            ) -> tuple[float, str] | None:
    """OI 시계열에서 최근 lookback 구간 변동률. |변동%| ≥ 임계면 반환.

    반환 (변동%, 상세). 양수=급증, 음수=급감.
    """
    if lookback < 1 or len(oi_series) < lookback + 1:
        return None
    old = oi_series[-1 - lookback]
    cur = oi_series[-1]
    if old <= 0:
        return None
    pct = (cur - old) / old * 100.0
    if abs(pct) < threshold_pct:
        return None
    return pct, f"OI {pct:+.2f}%"


def funding_extreme(funding_rate: float | None, threshold_abs: float
                    ) -> tuple[float, str] | None:
    """|펀딩비| ≥ 임계면 반환. 반환 (펀딩비, 상세)."""
    if funding_rate is None:
        return None
    if abs(funding_rate) < threshold_abs:
        return None
    return funding_rate, f"펀딩 {funding_rate * 100:+.3f}%"
