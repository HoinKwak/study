"""동어반복 점검: revert_ratio(실제 게이트 변수) vs ΔOI%·Kyle λ 근사·실현변동성·ATR 상관.
종목별·전체구간 AND 트리거(충격) 시점 한정 둘 다 계산(pandas.corr() pairwise)."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as c
import engine


def build_factor_frame(symbol: str, sd: c.SymbolData, cfg: engine.Config) -> pd.DataFrame:
    h1 = sd.h1
    atr1h = sd.atr1h
    oi = sd.oi1h.reindex(h1.index)
    n = len(h1)
    w = cfg.reversion_window
    idx = h1.index
    open_ = h1["open"]
    close_ = h1["close"]
    volume_ = h1["volume"]
    atr_ = atr1h
    oi_ = oi

    log_ret = np.log(close_ / close_.shift(1))
    realized_vol24 = log_ret.rolling(24).std()
    kyle_lambda = (close_ - open_).abs() / volume_.replace(0, np.nan)

    rows = []
    for t in range(20, n - w):
        a = atr_.iloc[t]
        if not np.isfinite(a) or a <= 0 or t - 3 < 0:
            continue
        pre_vals = oi_.iloc[t - 3:t].to_numpy()
        oi_shock = oi_.iloc[t]
        oi_now = oi_.iloc[t + w]
        if np.any(~np.isfinite(pre_vals)) or not np.isfinite(oi_shock) or not np.isfinite(oi_now):
            continue
        oi_pre = float(np.mean(pre_vals))
        denom = abs(oi_shock - oi_pre)
        if denom <= 0:
            continue
        ratio = abs(oi_now - oi_pre) / denom
        delta_oi_pct = (oi_now - oi_pre) / oi_pre * 100.0 if oi_pre != 0 else np.nan
        body = abs(close_.iloc[t] - open_.iloc[t])
        is_shock = body >= cfg.shock_atr_mult * a
        rows.append(dict(
            symbol=symbol, t=idx[t], revert_ratio=ratio, delta_oi_pct=delta_oi_pct,
            kyle_lambda=kyle_lambda.iloc[t], realized_vol24=realized_vol24.iloc[t],
            atr1h=a, is_shock=is_shock,
        ))
    return pd.DataFrame(rows)


def main():
    data = c.load_all()
    cfg = engine.Config()
    frames = []
    for sym, sd in data.items():
        frames.append(build_factor_frame(sym, sd, cfg))
    allf = pd.concat(frames, ignore_index=True)

    print("=== 전체구간(충격 무관 모든 봉) 상관 — pandas.corr() pairwise ===")
    for sym in c.SYMBOLS:
        d = allf[allf["symbol"] == sym][["revert_ratio", "delta_oi_pct", "kyle_lambda",
                                        "realized_vol24", "atr1h"]]
        corr = d.corr(numeric_only=True)["revert_ratio"].drop("revert_ratio")
        print(f"  {sym}: " + " ".join(f"{k}={v:+.3f}" for k, v in corr.items()))

    print("\n=== 트리거(충격) 시점 한정 상관 ===")
    for sym in c.SYMBOLS:
        d = allf[(allf["symbol"] == sym) & (allf["is_shock"])][
            ["revert_ratio", "delta_oi_pct", "kyle_lambda", "realized_vol24", "atr1h"]]
        if len(d) < 5:
            print(f"  {sym}: n={len(d)} (표본부족)")
            continue
        corr = d.corr(numeric_only=True)["revert_ratio"].drop("revert_ratio")
        print(f"  {sym}: n={len(d)} " + " ".join(f"{k}={v:+.3f}" for k, v in corr.items()))

    print("\n=== 풀링(전 종목) 전체구간 vs 트리거시점 비교 ===")
    corr_all = allf[["revert_ratio", "delta_oi_pct", "kyle_lambda", "realized_vol24", "atr1h"]].corr(
        numeric_only=True)["revert_ratio"].drop("revert_ratio")
    print("  전체구간:", " ".join(f"{k}={v:+.3f}" for k, v in corr_all.items()))
    d2 = allf[allf["is_shock"]][["revert_ratio", "delta_oi_pct", "kyle_lambda", "realized_vol24", "atr1h"]]
    corr_trig = d2.corr(numeric_only=True)["revert_ratio"].drop("revert_ratio")
    print("  트리거시점:", " ".join(f"{k}={v:+.3f}" for k, v in corr_trig.items()))


if __name__ == "__main__":
    main()
