"""대조군 신호 — ①게이트없음(순수 EMA20 크로스 / 순수 과열캔들 페이드)
②더 단순한 대안(naive RV z-score, OU/half-life 적합 생략) ③반전(base 방향 반전, 신호는 base 재사용).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import compute_indicators


def gate_none_breakout(ind: pd.DataFrame) -> pd.Series:
    """dev·half_life 게이트 없이 순수 EMA20 크로스만으로 방향 결정."""
    cross_up = (ind["close"].shift(1) <= ind["ema20"].shift(1)) & (ind["close"] > ind["ema20"])
    cross_dn = (ind["close"].shift(1) >= ind["ema20"].shift(1)) & (ind["close"] < ind["ema20"])
    out = pd.Series(0, index=ind.index, dtype="int64")
    out = out.where(~cross_up, 1)
    out = out.where(~cross_dn, -1)
    return out


def gate_none_fade(ind: pd.DataFrame, body_mult: float = 1.5) -> pd.Series:
    """dev·half_life 게이트 없이 순수 '과열 캔들'(body>=ATR*mult)만으로 반대방향 페이드."""
    body_ok = ind["body"].abs() >= ind["atr14"] * body_mult
    out = pd.Series(0, index=ind.index, dtype="int64")
    out = out.where(~(body_ok & (ind["body"] > 0)), -1)
    out = out.where(~(body_ok & (ind["body"] < 0)), 1)
    return out


def naive_rv_z(df: pd.DataFrame, rv_window: int = 42, z_window: int = 180) -> pd.Series:
    """OU/half-life 적합을 생략한 단순 대안: log(rv) 를 직접 롤링 z-score."""
    logret = np.log(df["close"] / df["close"].shift(1))
    rv = logret.rolling(rv_window).std()
    log_rv = np.log(rv.replace(0, np.nan))
    z = (log_rv - log_rv.rolling(z_window).mean()) / log_rv.rolling(z_window).std()
    return z


def simple_alt_breakout(df: pd.DataFrame, ind: pd.DataFrame, rv_window: int = 42,
                         z_window: int = 180, dev_breakout: float = -1.5) -> pd.Series:
    """naive z(log(rv)) <= dev_breakout AND EMA20 크로스(half_life 조건 없음 — OU 생략)."""
    z = naive_rv_z(df, rv_window, z_window)
    cross_up = (ind["close"].shift(1) <= ind["ema20"].shift(1)) & (ind["close"] > ind["ema20"])
    cross_dn = (ind["close"].shift(1) >= ind["ema20"].shift(1)) & (ind["close"] < ind["ema20"])
    cond = z <= dev_breakout
    out = pd.Series(0, index=ind.index, dtype="int64")
    out = out.where(~(cond & cross_up), 1)
    out = out.where(~(cond & cross_dn), -1)
    return out


def simple_alt_fade(df: pd.DataFrame, ind: pd.DataFrame, rv_window: int = 42, z_window: int = 180,
                     dev_fade: float = 2.0, body_mult: float = 1.5) -> pd.Series:
    z = naive_rv_z(df, rv_window, z_window)
    body_ok = ind["body"].abs() >= ind["atr14"] * body_mult
    cond = (z >= dev_fade) & body_ok
    out = pd.Series(0, index=ind.index, dtype="int64")
    out = out.where(~(cond & (ind["body"] > 0)), -1)
    out = out.where(~(cond & (ind["body"] < 0)), 1)
    return out
