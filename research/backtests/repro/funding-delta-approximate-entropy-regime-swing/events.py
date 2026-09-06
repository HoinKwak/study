"""종목별 진입신호 탐지 — 저ApEn 레짐(BTC 펀딩) AND BTC EMA20/50 방향 AND 대상종목 눌림목 재진입.

설계 판단(스펙 원문이 정확한 수식을 안 줘서 문자 그대로 구현 — §해석 참조):
  "종가가 EMA20 상향 재접촉 후 이탈" = 최근 `pullback_lookback`봉 내에 종가가 EMA20 이하로
  한 번 이상 닿았다가(눌림목), 당일 봉에서 종가가 다시 EMA20 위로 올라오고 직전 봉보다
  종가가 높다(이탈/재상승) — 롱 기준. 숏은 부호 대칭.
  이 해석의 파라미터 민감도는 pullback_lookback 스윕(3~8, run_sweeps.py)으로 점검한다.

전부 causal: 신호는 bar i의 **닫힌** 데이터로 판정하고, engine.py 에서 체결은 bar i+1 시가로
지연한다(프레임워크 shift(1) 요건).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from common import load_klines_4h, ema_pair, atr14_4h
from signals import build_btc_apen, build_btc_price_regime, map_settlement_to_bars


def build_universe(apen_window=30, apen_m=2, apen_r_mult=0.2, apen_lo_pctile=30,
                    apen_hi_pctile=85, pullback_lookback=5, ema_fast=20, ema_slow=50,
                    atr_period=14, pctile_window_days=90) -> dict:
    """심볼별 frame 딕셔너리 — 신호 계산에 필요한 전체 시계열을 미리 계산해둔다."""
    apen_d = build_btc_apen(apen_window, apen_m, apen_r_mult, pctile_window_days)
    btc_reg = build_btc_price_regime(ema_fast, ema_slow, atr_period)

    btc_price = btc_reg["price"]
    apen_pctile_bar = map_settlement_to_bars(apen_d["apen_pctile"], btc_price.index)
    gate_active = apen_pctile_bar <= apen_lo_pctile
    regime_breakdown = apen_pctile_bar >= apen_hi_pctile
    btc_long_regime = btc_reg["ema"]["ema_fast"] > btc_reg["ema"]["ema_slow"]
    btc_short_regime = btc_reg["ema"]["ema_fast"] < btc_reg["ema"]["ema_slow"]

    from common import SYMBOLS
    universe = {}
    for sym in SYMBOLS:
        price = load_klines_4h(sym) if sym != "BTCUSDT" else btc_price
        ema = ema_pair(price, ema_fast, ema_slow) if sym != "BTCUSDT" else btc_reg["ema"]
        atr = atr14_4h(price, atr_period) if sym != "BTCUSDT" else btc_reg["atr"]
        # 공통 4h 그리드(모든 심볼이 바이낸스 네이티브 4h)에 BTC 레짐 시리즈 재정렬
        gate_al = gate_active.reindex(price.index)
        breakdown_al = regime_breakdown.reindex(price.index)
        long_reg_al = btc_long_regime.reindex(price.index)
        short_reg_al = btc_short_regime.reindex(price.index)
        universe[sym] = {
            "price": price, "ema": ema, "atr": atr,
            "gate_active": gate_al, "regime_breakdown": breakdown_al,
            "btc_long_regime": long_reg_al, "btc_short_regime": short_reg_al,
        }
    return {"universe": universe, "apen": apen_d, "btc_reg": btc_reg,
            "apen_pctile_bar": apen_pctile_bar, "gate_active": gate_active,
            "regime_breakdown": regime_breakdown, "pullback_lookback": pullback_lookback}


def detect_signals(frame: dict, pullback_lookback: int = 5) -> pd.DataFrame:
    """단일 심볼 frame 에서 롱/숏 신호가 서는 bar 인덱스(bar i, 닫힌 데이터 기준)를 반환.

    반환 컬럼: signal_time(bar i 의 open_time), direction(1/-1), atr_entry(bar i 의 ATR).
    """
    price = frame["price"]
    close = price["close"].to_numpy()
    ema20 = frame["ema"]["ema_fast"].to_numpy()
    atr = frame["atr"].to_numpy()
    gate = frame["gate_active"].to_numpy()
    long_reg = frame["btc_long_regime"].to_numpy()
    short_reg = frame["btc_short_regime"].to_numpy()
    n = len(price)

    touched_below = close <= ema20  # 종가가 EMA20 이하(눌림목 접촉)
    touched_above = close >= ema20  # 종가가 EMA20 이상(숏 눌림목 접촉)

    rows = []
    for i in range(pullback_lookback, n):
        if not (np.isfinite(ema20[i]) and np.isfinite(atr[i]) and atr[i] > 0):
            continue
        if not gate[i]:
            continue
        window = slice(i - pullback_lookback, i)  # [i-lookback, i-1]
        close_i, close_im1, ema_i = close[i], close[i - 1], ema20[i]
        if long_reg[i] and close_i > ema_i and close_i > close_im1 and touched_below[window].any():
            rows.append({"signal_time": price.index[i], "direction": 1, "atr_entry": float(atr[i])})
        elif short_reg[i] and close_i < ema_i and close_i < close_im1 and touched_above[window].any():
            rows.append({"signal_time": price.index[i], "direction": -1, "atr_entry": float(atr[i])})
    return pd.DataFrame(rows)
