"""게이트 변형 빌더 — 스펙 원안(OI가중 vs 등가중 스프레드) + 대조군(BTC 단독 변동성·등가중 단독).

모두 동일한 임계값(short_th=1.5, long_th=-1.0)과 동일한 90h 롤링 z-score 방식을 공유해,
"게이트가 실제로 정보를 담는지"만 순수하게 비교할 수 있게 한다.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as C


def _zscore(s: pd.Series, window: int) -> pd.Series:
    m = s.rolling(window).mean()
    sd = s.rolling(window).std(ddof=0)
    z = (s - m) / sd
    return z.where(sd > 1e-12)


def build_gate_oiweighted(symbols: list[str] = C.SYMBOLS,
                          spread_z_window: int = C.SPREAD_Z_WINDOW,
                          short_th: float = C.SPREAD_Z_SHORT_TH,
                          long_th: float = C.SPREAD_Z_LONG_TH,
                          udata: C.UniverseData | None = None) -> tuple[pd.Series, pd.DataFrame]:
    """스펙 원안 게이트: spread_z = zscore_90(rv_ow - rv_ew)."""
    if udata is None:
        udata = C.build_universe_data(symbols)
    spread_df = C.compute_spread(udata, symbols, spread_z_window)
    gate = C.gate_from_spread_z(spread_df["spread_z"], short_th, long_th)
    return gate, spread_df


def build_gate_btc_solo(spread_z_window: int = C.SPREAD_Z_WINDOW,
                        short_th: float = C.SPREAD_Z_SHORT_TH,
                        long_th: float = C.SPREAD_Z_LONG_TH) -> pd.Series:
    """대조군: BTC 단독 실현변동성의 z-score(OI가중·등가중 구성 전혀 없음, 순수 BTC 자기 변동성
    레짐). '스프레드가 정보를 더하는가'를 검정하는 핵심 대조군."""
    btc1h = C.load_klines_1h(C.BTC)
    rv = C.realized_vol_1h(btc1h)
    z = _zscore(rv, spread_z_window)
    return C.gate_from_spread_z(z, short_th, long_th)


def build_gate_ew_solo(symbols: list[str] = C.SYMBOLS,
                       spread_z_window: int = C.SPREAD_Z_WINDOW,
                       short_th: float = C.SPREAD_Z_SHORT_TH,
                       long_th: float = C.SPREAD_Z_LONG_TH,
                       udata: C.UniverseData | None = None) -> pd.Series:
    """대조군: 등가중 실현변동성(rv_ew) 자체의 z-score(OI가중 없이 유니버스 평균 변동성 레짐만).
    'OI 가중이 등가중 대비 부가가치가 있는가'를 검정."""
    if udata is None:
        udata = C.build_universe_data(symbols)
    rv = udata.rv[symbols]
    rv_ew = rv.mean(axis=1, skipna=True).where(rv.notna().sum(axis=1) > 0)
    z = _zscore(rv_ew, spread_z_window)
    return C.gate_from_spread_z(z, short_th, long_th)


def gate_duty_cycle(gate_1h: pd.Series) -> dict:
    vc = gate_1h.value_counts(dropna=True)
    n = vc.sum()
    return {k: float(vc.get(k, 0)) / n for k in ["short_only", "long_only", "neutral"]}
