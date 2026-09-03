"""1차 진단: 결합확률(정렬비율) 실측, 신호빈도, NaN매핑비율, 재포장 점검(RSI/ROC/ATR/실현변동성 상관,
레벨+게이트변수+트리거시점), 종목간 신호상관(평균+위기국면)."""
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
    print("=== 결합확률(15m/1h/4h 방향정렬 비율) + 신호빈도 + NaN매핑률 ===")
    rows = []
    for sym in common.SYMBOLS:
        sig = engine.build_signals(sym, cfg)
        c15, c1h, c4h, vok = sig.clv15, sig.clv1h_at15, sig.clv4h_at15, sig.vol_ok
        valid = np.isfinite(c15) & np.isfinite(c1h) & np.isfinite(c4h)
        long_15 = c15 >= cfg.clv15_th_long
        short_15 = c15 <= cfg.clv15_th_short
        long_all = valid & long_15 & (c1h >= cfg.clv1h_th_long) & (c4h >= cfg.clv4h_th_long)
        short_all = valid & short_15 & (c1h <= cfg.clv1h_th_short) & (c4h <= cfg.clv4h_th_short)
        n_bars = len(c15)
        years = n_bars * 15 / 60 / 24 / 365.25
        trades = engine.run_symbol(sym, sig, cfg)
        n_tr = len(trades)
        print(f"{sym:10s} 15m단독long%={long_15.mean()*100:.3f} 15m단독short%={short_15.mean()*100:.3f} "
              f"3TF정렬long%={long_all.mean()*100:.4f} 3TF정렬short%={short_all.mean()*100:.4f} "
              f"vol_ok%={np.nanmean(vok)*100:.1f} nan1h={sig.nan_frac_1h*100:.3f}% "
              f"nan4h={sig.nan_frac_4h*100:.3f}%")
        print(f"           n_bars={n_bars} years={years:.2f} n_trades(vol필터포함)={n_tr} "
              f"trades/year={n_tr/years:.1f}")
        rows.append(dict(symbol=sym, n_trades=n_tr, years=years))
    return rows


def diag_repackaging():
    print("\n=== 동어반복 점검: CLV_15m(게이트변수) vs RSI14/ROC/ATR%/실현변동성 상관(레벨+트리거시점) ===")
    for sym in common.SYMBOLS:
        sig = engine.build_signals(sym, cfg)
        h15 = sig.h15
        rsi14 = ind.rsi(h15["close"], 14).to_numpy(float)
        roc5 = h15["close"].pct_change(5).to_numpy(float)
        atr_pct = (sig.atr15 / h15["close"].to_numpy(float))
        rv20 = h15["close"].pct_change().rolling(20).std().to_numpy(float)

        c15 = sig.clv15

        def corr(a, b, mask=None):
            aa, bb = a.copy(), b.copy()
            m = np.isfinite(aa) & np.isfinite(bb)
            if mask is not None:
                m = m & mask
            if m.sum() < 30:
                return float("nan"), int(m.sum())
            return float(pd.Series(aa[m]).corr(pd.Series(bb[m]))), int(m.sum())

        c_rsi, n1 = corr(c15, rsi14)
        c_roc, n2 = corr(c15, roc5)
        c_atr, n3 = corr(c15, atr_pct)
        c_rv, n4 = corr(c15, rv20)

        trades = engine.run_symbol(sym, sig, cfg)
        trig_idx = np.array([t.entry_idx - 1 for t in trades if t.entry_idx - 1 >= 0])
        trig_mask = np.zeros(len(c15), dtype=bool)
        if len(trig_idx):
            trig_mask[trig_idx[trig_idx < len(trig_mask)]] = True

        c_rsi_t, n1t = corr(c15, rsi14, trig_mask)
        c_roc_t, n2t = corr(c15, roc5, trig_mask)
        c_atr_t, n3t = corr(c15, atr_pct, trig_mask)
        c_rv_t, n4t = corr(c15, rv20, trig_mask)

        print(f"{sym}: 전구간 corr(CLV15,RSI14)={c_rsi:.4f}(n={n1}) corr(,ROC5)={c_roc:.4f}(n={n2}) "
              f"corr(,ATR%%)={c_atr:.4f}(n={n3}) corr(,RV20)={c_rv:.4f}(n={n4})")
        print(f"        트리거시점 corr(,RSI14)={c_rsi_t:.4f}(n={n1t}) corr(,ROC5)={c_roc_t:.4f}(n={n2t}) "
              f"corr(,ATR%%)={c_atr_t:.4f}(n={n3t}) corr(,RV20)={c_rv_t:.4f}(n={n4t})")


def diag_cross_symbol_corr():
    print("\n=== 종목간 신호 상관(평균 — 동시진입일 비율) ===")
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

    print("\n=== 종목간 신호 상관(위기국면 — BTC 절대일수익률 상위5%일에 한정) ===")
    btc15 = common.load_klines("BTCUSDT", "15m")
    btc_daily_close = btc15["close"].resample("1D").last()
    btc_ret = btc_daily_close.pct_change().abs()
    thresh = btc_ret.quantile(0.95)
    crisis_days = set(btc_ret[btc_ret >= thresh].index.floor("D"))
    print(f"위기국면일수(BTC |일수익률| 상위5%%)={len(crisis_days)} 임계={thresh*100:.2f}%")
    cnt_crisis = Counter()
    for d in crisis_days:
        n_sym = sum(1 for s in common.SYMBOLS if d in all_trades[s])
        cnt_crisis[n_sym] += 1
    print("위기국면일 동시진입 종목수 분포:", dict(sorted(cnt_crisis.items())))
    normal_days = [d for d in days_union if d not in crisis_days]
    cnt_normal = Counter()
    for d in normal_days:
        n_sym = sum(1 for s in common.SYMBOLS if d in all_trades[s])
        cnt_normal[n_sym] += 1
    avg_n_normal = np.mean([sum(1 for s in common.SYMBOLS if d in all_trades[s]) for d in normal_days]) if normal_days else float("nan")
    avg_n_crisis = np.mean([sum(1 for s in common.SYMBOLS if d in all_trades[s]) for d in crisis_days]) if crisis_days else float("nan")
    print(f"평시 평균 동시진입종목수={avg_n_normal:.3f}  위기국면 평균 동시진입종목수={avg_n_crisis:.3f}")


if __name__ == "__main__":
    diag_agreement_and_freq()
    diag_repackaging()
    diag_cross_symbol_corr()
