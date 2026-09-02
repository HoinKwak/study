"""룩어헤드 점검 — 데이터를 특정 시점에서 절단해도 그 이전 신호(rho15/regime15/트리거)가
바뀌지 않는지 확인. 바뀐다면 미래 데이터를 참조하는 결함.
BTC 외 ETH·ADA·XRP 로도 확장 절단(과거 라운드 관행).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine

CUTS = {
    "BTCUSDT": 50000,
    "ETHUSDT": 40000,
    "ADAUSDT": 30000,
    "XRPUSDT": 20000,
}


def check_symbol(symbol: str, cut: int) -> None:
    cfg = engine.RunConfig()
    full_sig = engine.build_signals(symbol, cfg)
    if full_sig is None:
        print(f"   {symbol}: 데이터 없음")
        return

    # 15m 데이터를 cut 지점에서 절단해 별도 캐시 키로 재로딩(원본 캐시 오염 방지 위해 별도 로더)
    h15_full = full_sig.h15
    if cut >= len(h15_full):
        print(f"   {symbol}: cut({cut}) >= len({len(h15_full)}), 스킵")
        return
    cut_time = h15_full.index[cut]

    # 1h 도 동일 시각 이하로 절단(레짐 계산이 그 시점 이후 1h 데이터를 못 보게)
    h1_full = common.load_klines(symbol, "1h")
    h15_trunc = h15_full.loc[:cut_time].iloc[:-1]  # cut_time 미포함(그 시점 봉 자체도 제외해 엄격 절단)
    h1_trunc = h1_full.loc[:cut_time]

    # build_signals 를 절단 데이터로 직접 재현(공용 함수가 symbol 로 캐시 로딩하므로 로컬 재구현)
    import indicators as racsr_ind
    from crypto_trader.signals import indicators as ind

    r1h = racsr_ind.log_returns(h1_trunc["close"])
    rho1h = racsr_ind.rolling_lag1_autocorr(r1h, engine.N_1H)
    regime1h = pd.Series(0, index=h1_trunc.index, dtype=int)
    regime1h[rho1h <= -cfg.rho_th] = -1
    regime1h[rho1h >= cfg.rho_th] = 1
    regime15_trunc = common.map_asof_backward(pd.DatetimeIndex(h15_trunc.index),
                                              regime1h.astype(float), 3600)
    regime15_trunc = np.nan_to_num(regime15_trunc, nan=0.0).astype(int)
    rho15_trunc = common.map_asof_backward(pd.DatetimeIndex(h15_trunc.index), rho1h, 3600)

    atr15_trunc = ind.atr(h15_trunc, 14).to_numpy(float)

    n_check = min(200, len(h15_trunc))
    idx_check = list(range(len(h15_trunc) - n_check, len(h15_trunc)))
    full_pos = {t: i for i, t in enumerate(h15_full.index)}

    mismatches_regime = 0
    mismatches_rho = 0
    mismatches_atr = 0
    for i in idx_check:
        t = h15_trunc.index[i]
        j = full_pos[t]
        if regime15_trunc[i] != full_sig.regime15[j]:
            mismatches_regime += 1
        rt, rf = rho15_trunc[i], full_sig.rho15[j]
        if not (np.isnan(rt) and np.isnan(rf)) and not np.isclose(rt, rf, equal_nan=True):
            mismatches_rho += 1
        at, af = atr15_trunc[i], full_sig.atr15[j]
        if not (np.isnan(at) and np.isnan(af)) and not np.isclose(at, af, equal_nan=True):
            mismatches_atr += 1

    print(f"   {symbol}: cut@{cut}({cut_time}) 확인봉수={n_check} "
         f"regime_mismatch={mismatches_regime} rho_mismatch={mismatches_rho} "
         f"atr_mismatch={mismatches_atr}")


def main() -> None:
    print("=== 룩어헤드 절단 재현 점검(절단 전 마지막 200봉의 regime15/rho15/ATR15 일치 확인) ===")
    for sym, cut in CUTS.items():
        check_symbol(sym, cut)


if __name__ == "__main__":
    main()
