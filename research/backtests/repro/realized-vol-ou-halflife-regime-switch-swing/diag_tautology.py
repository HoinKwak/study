"""동어반복 점검 — dev 가 볼린저밴드폭 z-score·ADX·GARCH류(EWMA) 예측분산의 재서술인지.

전체구간 상관과 "트리거 시점"(hl_ok AND (dev<=dev_breakout OR dev>=dev_fade)) 한정 상관을
둘 다 계산한다(과거 프리미엄인덱스 건에서 전체 0.246/트리거시점 0.928로 갈렸던 함정 경계).
사전 폐기조건(스펙 §최우선 의심점): |r|>0.85 면 재포장으로 간주.
"""
from __future__ import annotations

import json
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, ".")
from common import SYMBOLS, load_klines_4h
from signals import build_signals


def bollinger_bandwidth_z(close: pd.Series, bb_window: int = 20, z_window: int = 180) -> pd.Series:
    sma = close.rolling(bb_window).mean()
    std = close.rolling(bb_window).std()
    upper = sma + 2 * std
    lower = sma - 2 * std
    bw = (upper - lower) / sma
    z = (bw - bw.rolling(z_window).mean()) / bw.rolling(z_window).std()
    return z


def adx(df: pd.DataFrame, window: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    up_move = high.diff()
    down_move = -low.diff()
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    tr = pd.concat([(high - low), (high - close.shift(1)).abs(),
                    (low - close.shift(1)).abs()], axis=1).max(axis=1)
    atr_ = tr.ewm(alpha=1.0 / window, adjust=False, min_periods=window).mean()
    plus_di = 100 * pd.Series(plus_dm, index=df.index).ewm(
        alpha=1.0 / window, adjust=False, min_periods=window).mean() / atr_
    minus_di = 100 * pd.Series(minus_dm, index=df.index).ewm(
        alpha=1.0 / window, adjust=False, min_periods=window).mean() / atr_
    dx = 100 * (plus_di - minus_di).abs() / (plus_di + minus_di)
    return dx.ewm(alpha=1.0 / window, adjust=False, min_periods=window).mean()


def ewma_variance_forecast(logret: pd.Series, lam: float = 0.94) -> pd.Series:
    """RiskMetrics 식 EWMA 분산 — 완전한 GARCH(1,1) 모수적합의 단순 근사(proxy).
    var_t = lam*var_{t-1} + (1-lam)*r_{t-1}^2 (t-1 정보만 사용, 인과적)."""
    r2 = (logret ** 2).fillna(0.0)
    var = np.zeros(len(r2))
    v0 = r2.iloc[:30].mean() if len(r2) > 30 else r2.mean()
    var[0] = v0 if np.isfinite(v0) else 0.0
    for i in range(1, len(r2)):
        var[i] = lam * var[i - 1] + (1 - lam) * r2.iloc[i - 1]
    return pd.Series(var, index=logret.index)


def main():
    rows = []
    trig_frames = []
    full_frames = []
    for sym in SYMBOLS:
        df = load_klines_4h(sym)
        ind = build_signals(df)
        bbz = bollinger_bandwidth_z(ind["close"])
        adx14 = adx(ind)
        ewma_var = ewma_variance_forecast(ind["logret"])
        log_ewma_var = np.log(ewma_var.replace(0, np.nan))

        frame = pd.DataFrame({
            "dev": ind["dev"], "bbz": bbz, "adx": adx14, "log_ewma_var": log_ewma_var,
        })
        full_frames.append(frame)

        trig = ind["hl_ok"] & ((ind["dev"] <= -1.5) | (ind["dev"] >= 2.0))
        trig_frames.append(frame[trig])

        full_valid = frame.dropna()
        r_bbz_full = full_valid["dev"].corr(full_valid["bbz"])
        r_adx_full = full_valid["dev"].corr(full_valid["adx"])
        r_garch_full = full_valid["dev"].corr(full_valid["log_ewma_var"])

        trig_valid = frame[trig].dropna()
        r_bbz_trig = trig_valid["dev"].corr(trig_valid["bbz"]) if len(trig_valid) > 2 else np.nan
        r_adx_trig = trig_valid["dev"].corr(trig_valid["adx"]) if len(trig_valid) > 2 else np.nan
        r_garch_trig = trig_valid["dev"].corr(trig_valid["log_ewma_var"]) if len(trig_valid) > 2 else np.nan

        rows.append({
            "symbol": sym, "n_full": len(full_valid), "n_trig": len(trig_valid),
            "r_bbz_full": r_bbz_full, "r_bbz_trig": r_bbz_trig,
            "r_adx_full": r_adx_full, "r_adx_trig": r_adx_trig,
            "r_garch_full": r_garch_full, "r_garch_trig": r_garch_trig,
        })

    out = pd.DataFrame(rows)
    out.to_csv("out_diag_tautology.csv", index=False)
    print(out.to_string(index=False))
    maxabs = out[[c for c in out.columns if c.startswith("r_")]].abs().max().max()
    print("max |r| across all metrics/symbols/full+trigger:", maxabs)
    with open("out_diag_tautology.json", "w") as f:
        json.dump({"max_abs_r": float(maxabs), "kill_threshold": 0.85,
                    "killed": bool(maxabs > 0.85)}, f, indent=2)


if __name__ == "__main__":
    main()
