"""캔들 패턴 인식. 각 함수는 마지막 캔들 기준 방향 점수(-1~+1)를 반환.

+ = 강세(bullish) 반전/지속, - = 약세(bearish).
"""
from __future__ import annotations

import pandas as pd


def _body(o: float, c: float) -> float:
    return abs(c - o)


def bullish_bearish_engulfing(df: pd.DataFrame) -> float:
    """장악형(engulfing). 강세 장악 +0.8, 약세 장악 -0.8."""
    if len(df) < 2:
        return 0.0
    prev, curr = df.iloc[-2], df.iloc[-1]
    po, pc = prev["open"], prev["close"]
    co, cc = curr["open"], curr["close"]

    prev_bear = pc < po
    curr_bull = cc > co
    if prev_bear and curr_bull and cc >= po and co <= pc:
        return 0.8  # 강세 장악

    prev_bull = pc > po
    curr_bear = cc < co
    if prev_bull and curr_bear and cc <= po and co >= pc:
        return -0.8  # 약세 장악
    return 0.0


def hammer_shooting_star(df: pd.DataFrame) -> float:
    """망치형(+0.6) / 유성형(-0.6)."""
    if len(df) < 1:
        return 0.0
    c = df.iloc[-1]
    o, h, l, cl = c["open"], c["high"], c["low"], c["close"]
    rng = h - l
    if rng <= 0:
        return 0.0
    body = _body(o, cl)
    upper = h - max(o, cl)
    lower = min(o, cl) - l

    # 망치형: 아래꼬리 길고 몸통 작음
    if lower >= 2 * body and upper <= body:
        return 0.6
    # 유성형: 위꼬리 길고 몸통 작음
    if upper >= 2 * body and lower <= body:
        return -0.6
    return 0.0


def doji(df: pd.DataFrame) -> float:
    """도지(방향성 없음, 관망). 중립 신호 → 0."""
    if len(df) < 1:
        return 0.0
    c = df.iloc[-1]
    rng = c["high"] - c["low"]
    if rng <= 0:
        return 0.0
    if _body(c["open"], c["close"]) <= 0.1 * rng:
        return 0.0  # 명시적 중립
    return 0.0


def aggregate_patterns(df: pd.DataFrame) -> float:
    """여러 패턴 점수를 합쳐 -1~+1 로 클램프."""
    total = bullish_bearish_engulfing(df) + hammer_shooting_star(df) + doji(df)
    return max(-1.0, min(1.0, total))
