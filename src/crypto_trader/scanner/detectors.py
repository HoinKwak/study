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
