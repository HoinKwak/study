"""진입 신호 생성 — 브레이크아웃 모드 / 페이드 모드 (스펙 §진입 규칙).

두 모드는 서로 다른 가설(추세추종 vs 평균회귀)이라 별도 서브셋으로 나눠 신호를 낸다
(혼합 풀 금지 — 스펙 명시).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import compute_indicators


def build_signals(df: pd.DataFrame, *, rv_window: int = 42, ou_window: int = 180,
                   dev_breakout: float = -1.5, dev_fade: float = 2.0,
                   hl_min: float = 8, hl_max: float = 40,
                   body_mult: float = 1.5) -> pd.DataFrame:
    """indicators 계산 후 브레이크아웃/페이드 원신호(raw, shift 전) 반환.

    반환 컬럼: dev, half_life, phi, ema20, atr14, close, open, high, low,
    raw_breakout_dir(1/-1/0), raw_fade_dir(1/-1/0).
    신호는 봉 t 종가 확정시점 기준(그 봉의 close/EMA/ATR 사용) — 실제 거래 진입은
    호출측에서 shift(1) 적용(다음 봉 시가 근사).
    """
    ind = compute_indicators(df, rv_window=rv_window, ou_window=ou_window)

    hl_ok = (ind["half_life"] >= hl_min) & (ind["half_life"] <= hl_max)

    # --- 브레이크아웃: dev <= dev_breakout AND hl_ok AND EMA20 상단 돌파(롱)/하단 이탈(숏) ---
    cross_up = (ind["close"].shift(1) <= ind["ema20"].shift(1)) & (ind["close"] > ind["ema20"])
    cross_dn = (ind["close"].shift(1) >= ind["ema20"].shift(1)) & (ind["close"] < ind["ema20"])
    brk_cond = (ind["dev"] <= dev_breakout) & hl_ok
    raw_breakout_dir = pd.Series(0, index=ind.index, dtype="int64")
    raw_breakout_dir = raw_breakout_dir.where(~(brk_cond & cross_up), 1)
    raw_breakout_dir = raw_breakout_dir.where(~(brk_cond & cross_dn), -1)

    # --- 페이드: dev >= dev_fade AND hl_ok AND |body| >= ATR14*body_mult, 반대방향 진입 ---
    body_ok = ind["body"].abs() >= ind["atr14"] * body_mult
    fade_cond = (ind["dev"] >= dev_fade) & hl_ok & body_ok
    raw_fade_dir = pd.Series(0, index=ind.index, dtype="int64")
    # body>0(양봉) -> 반대(숏,-1) / body<0(음봉) -> 반대(롱,+1)
    raw_fade_dir = raw_fade_dir.where(~(fade_cond & (ind["body"] > 0)), -1)
    raw_fade_dir = raw_fade_dir.where(~(fade_cond & (ind["body"] < 0)), 1)

    ind["raw_breakout_dir"] = raw_breakout_dir
    ind["raw_fade_dir"] = raw_fade_dir
    ind["hl_ok"] = hl_ok
    return ind
