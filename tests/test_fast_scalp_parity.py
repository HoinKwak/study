"""fast_scalp(벡터화 사전계산) 경로가 기존 ScalpStrategy.decide 경로와 트레이드 완전동일 보장.

백테스터 최적화(봉별 pandas 제거)가 결과를 절대 바꾸지 않도록 회귀 가드.
실데이터 3종목·4조합에서 0 불일치 검증됨 — 이 테스트는 합성 데이터로 CI 가드.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from crypto_trader.config import Settings
from crypto_trader.backtest import SleeveBacktester


def _synthetic_df(n=900, seed=7):
    """스퀴즈→거래량급증 돌파가 간헐 발생하도록 만든 합성 15m OHLCV."""
    rng = np.random.default_rng(seed)
    price = 100.0
    rows = []
    idx = pd.date_range("2024-01-01", periods=n, freq="15min", tz="UTC")
    for i in range(n):
        # 저변동 구간과 간헐적 강한 추세봉 섞기
        drift = rng.normal(0, 0.15)
        if i % 37 == 0:                       # 주기적 강봉(돌파 유발)
            drift = rng.choice([-1, 1]) * rng.uniform(1.5, 3.0)
            vol = rng.uniform(40, 80)         # 거래량 급증
        else:
            vol = rng.uniform(5, 12)
        o = price
        c = price + drift
        h = max(o, c) + abs(rng.normal(0, 0.1))
        l = min(o, c) - abs(rng.normal(0, 0.1))
        rows.append((o, h, l, c, vol))
        price = c
    df = pd.DataFrame(rows, columns=["open", "high", "low", "close", "volume"], index=idx)
    return df


def _run(df, fast, sl_rule, regime, exit_mode="scale3_band"):
    s = Settings(binance_api_key="", binance_api_secret="",
                 scalp_vol_spike_mult=5.0, scalp_squeeze_pctile=35.0,
                 scalp_min_body_atr=1.3, scalp_require_regime=regime,
                 scalp_chop_confirm_bars=2, position_margin_pct=10.0)
    bt = SleeveBacktester(s, "scalp", confirm_tf="1h", starting_equity=10_000.0,
                          taker_fee=0.0005, maker_fee=0.0002, slippage=0.0002,
                          maker_entry=True, leverage=10, scalp_exit_mode=exit_mode,
                          scalp_sl_rule=sl_rule, fast_scalp=fast)
    return bt.run("SYN/USDT", df)


def test_fast_equals_slow_scale3():
    df = _synthetic_df()
    for regime in (False, True):
        for sl in ("initial", "be_after_tp1", "be_after_tp2"):
            slow = _run(df, False, sl, regime)
            fast = _run(df, True, sl, regime)
            ps = [round(t.pnl, 9) for t in slow.trades if t.pnl is not None]
            pf = [round(t.pnl, 9) for t in fast.trades if t.pnl is not None]
            assert ps == pf, f"fast≠slow (regime={regime}, sl={sl}): {len(ps)} vs {len(pf)}"


def test_fast_equals_slow_momentum_modes():
    """다른 청산모드에서도 fast 경로가 동일한지."""
    df = _synthetic_df(seed=11)
    for mode in ("momentum", "momentum_split", "momentum_trail"):
        slow = _run(df, False, "initial", False, exit_mode=mode)
        fast = _run(df, True, "initial", False, exit_mode=mode)
        ps = [round(t.pnl, 9) for t in slow.trades if t.pnl is not None]
        pf = [round(t.pnl, 9) for t in fast.trades if t.pnl is not None]
        assert ps == pf, f"fast≠slow ({mode}): {len(ps)} vs {len(pf)}"
