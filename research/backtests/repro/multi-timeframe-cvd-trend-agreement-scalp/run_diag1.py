"""1차 진단: 결합확률(부호 합치율) 실측, 신호빈도, 재포장 점검(기존지표 상관), 종목간 신호상관."""
from __future__ import annotations
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine
from crypto_trader.signals import indicators as ind

cfg = engine.RunConfig()


def diag_agreement_and_freq():
    print("=== 결합확률(부호 합치율) + 신호빈도 ===")
    rows = []
    for sym in common.SYMBOLS:
        sig = engine.build_signals(sym, cfg)
        s5, s1h = sig.sign5m, sig.sign1h
        valid = np.isfinite(s5) & np.isfinite(s1h)
        agree = (s5[valid] == s1h[valid]).mean()
        n_bars = len(s5)
        years = n_bars * 15 / 60 / 24 / 365.25
        trades = engine.run_symbol(sym, sig, cfg)
        n_tr = len(trades)
        print(f"{sym:10s} agree={agree*100:.2f}% valid_frac={valid.mean()*100:.2f}% "
              f"n_bars={n_bars} years={years:.2f} n_trades={n_tr} trades/year={n_tr/years:.1f}")
        rows.append(dict(symbol=sym, agree=agree, n_trades=n_tr, years=years))
    return rows


def diag_repackaging():
    print("\n=== 재포장 점검: CVD slope vs 기존지표(ROC, 거래량가중모멘텀, ADX) 상관 ===")
    for sym in ["BTCUSDT", "ETHUSDT", "XRPUSDT"]:
        sig = engine.build_signals(sym, cfg)
        h15 = sig.h15
        roc = h15["close"].pct_change(cfg.slope_lookback)
        # 거래량가중 모멘텀(단순): (close-close.shift(lb)) * 최근 lb봉 평균 quote_volume
        vwm = (h15["close"] - h15["close"].shift(cfg.slope_lookback)) * \
            h15["quote_volume"].rolling(cfg.slope_lookback).mean()
        adx15, plus_di, minus_di = ind.adx(h15, 14)
        adx_dir = (plus_di - minus_di)  # 부호 있는 방향성 ADX 대용

        s1h_val = sig.slope1h_at15
        roc_a = roc.to_numpy(float)
        vwm_a = vwm.to_numpy(float)
        adxdir_a = adx_dir.to_numpy(float)

        def corr(a, b, mask=None):
            aa, bb = a.copy(), b.copy()
            m = np.isfinite(aa) & np.isfinite(bb)
            if mask is not None:
                m = m & mask
            if m.sum() < 30:
                return float("nan"), int(m.sum())
            return float(np.corrcoef(aa[m], bb[m])[0, 1]), int(m.sum())

        # 전 구간 상관(CVD_1h slope vs ROC15/VWM/ADXdir, 같은 15m 그리드)
        c_roc, n1 = corr(s1h_val, roc_a)
        c_vwm, n2 = corr(s1h_val, vwm_a)
        c_adx, n3 = corr(s1h_val, adxdir_a)

        # 트리거 시점만(신호 발생한 봉만)
        trades = engine.run_symbol(sym, sig, cfg)
        trig_idx = np.array([t.entry_idx - 1 for t in trades if t.entry_idx - 1 >= 0])  # 신호봉=체결 전 봉
        trig_mask = np.zeros(len(s1h_val), dtype=bool)
        trig_mask[trig_idx[trig_idx < len(trig_mask)]] = True

        c_roc_t, n1t = corr(s1h_val, roc_a, trig_mask)
        c_vwm_t, n2t = corr(s1h_val, vwm_a, trig_mask)
        c_adx_t, n3t = corr(s1h_val, adxdir_a, trig_mask)

        print(f"{sym}: 전구간 corr(CVD1h_slope,ROC{cfg.slope_lookback})={c_roc:.4f}(n={n1}) "
              f"corr(,VWM)={c_vwm:.4f}(n={n2}) corr(,ADXdir)={c_adx:.4f}(n={n3})")
        print(f"        트리거시점 corr(,ROC)={c_roc_t:.4f}(n={n1t}) "
              f"corr(,VWM)={c_vwm_t:.4f}(n={n2t}) corr(,ADXdir)={c_adx_t:.4f}(n={n3t})")


def diag_cross_symbol_corr():
    print("\n=== 종목간 신호 상관(동시진입일 비율) ===")
    all_trades = {}
    for sym in common.SYMBOLS:
        sig = engine.build_signals(sym, cfg)
        trades = engine.run_symbol(sym, sig, cfg)
        df = pd.DataFrame([{"entry_time": t.entry_time} for t in trades])
        if len(df):
            df["day"] = df["entry_time"].dt.floor("D")
            all_trades[sym] = set(df["day"])
        else:
            all_trades[sym] = set()
    days_union = set()
    for s in all_trades.values():
        days_union |= s
    days_union = sorted(days_union)
    from collections import Counter
    cnt = Counter()
    for d in days_union:
        n_sym = sum(1 for s in common.SYMBOLS if d in all_trades[s])
        cnt[n_sym] += 1
    print("동시진입 종목수 분포(일단위):", dict(sorted(cnt.items())))
    total_days = len(days_union)
    seven = cnt.get(7, 0)
    print(f"고유일수={total_days}, 7종목 전부 동시진입일={seven} ({seven/total_days*100:.2f}%)")


if __name__ == "__main__":
    diag_agreement_and_freq()
    diag_repackaging()
    diag_cross_symbol_corr()
