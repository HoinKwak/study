"""폐기조건(a): 충격봉 vs 무작위(비충격) 1h봉에서 OI 복귀율(reversion) 비율 배경분포 비교."""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy import stats as sstats

import common as c
import engine


def classify_all_bars(symbol: str, sd: c.SymbolData, cfg: engine.Config) -> pd.DataFrame:
    """충격 여부와 무관하게 '모든' 1h봉에 대해 동일한 OI 분류식을 적용(배경분포용)."""
    h1 = sd.h1
    atr1h = sd.atr1h
    oi = sd.oi1h.reindex(h1.index)
    n = len(h1)
    w = cfg.reversion_window
    idx = h1.index
    open_ = h1["open"].to_numpy()
    close_ = h1["close"].to_numpy()
    atr_ = atr1h.to_numpy()
    oi_ = oi.to_numpy()
    rows = []
    warmup = 20
    for t in range(warmup, n - w):
        a = atr_[t]
        if not np.isfinite(a) or a <= 0:
            continue
        if t - 3 < 0:
            continue
        pre_vals = oi_[t - 3:t]
        oi_shock = oi_[t]
        oi_now = oi_[t + w]
        if np.any(~np.isfinite(pre_vals)) or not np.isfinite(oi_shock) or not np.isfinite(oi_now):
            continue
        oi_pre = float(np.mean(pre_vals))
        denom = abs(oi_shock - oi_pre)
        if denom <= 0:
            continue
        ratio = abs(oi_now - oi_pre) / denom
        branch = "reversion" if ratio <= cfg.revert_pct else "persistence"
        body = abs(close_[t] - open_[t])
        is_shock = body >= cfg.shock_atr_mult * a
        rows.append(dict(symbol=symbol, shock_time=idx[t], branch=branch, revert_ratio=ratio,
                          is_shock=is_shock))
    return pd.DataFrame(rows)


def main():
    data = c.load_all()
    cfg = engine.Config()
    all_rows = []
    for sym, sd in data.items():
        all_rows.append(classify_all_bars(sym, sd, cfg))
    allb = pd.concat(all_rows, ignore_index=True)
    allb["period"] = allb["shock_time"].apply(c.period_of)
    allb = allb[allb["period"].isin(["IS", "OOS"])]

    shock = allb[allb["is_shock"]]
    bg = allb[~allb["is_shock"]]

    shock_rev_rate = (shock["branch"] == "reversion").mean()
    bg_rev_rate = (bg["branch"] == "reversion").mean()
    print(f"충격봉(n={len(shock)}) 복귀율: {shock_rev_rate*100:.2f}%")
    print(f"배경(비충격, n={len(bg)}) 복귀율: {bg_rev_rate*100:.2f}%")

    # 2-표본 비율 z검정(정규근사) — proportions_ztest 수동구현
    n1, n2 = len(shock), len(bg)
    x1, x2 = int((shock["branch"] == "reversion").sum()), int((bg["branch"] == "reversion").sum())
    p1, p2 = x1 / n1, x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p1 - p2) / se if se > 0 else float("nan")
    p_val = 2 * (1 - sstats.norm.cdf(abs(z)))
    print(f"\n비율차 z검정: z={z:.4f} p={p_val:.6f}")
    print("→", "배경과 통계적으로 구분됨(폐기조건(a) 미해당)" if p_val < 0.05 else
          "배경과 구분 불가 → 정의결함으로 폐기조건(a) 충족")

    # revert_ratio 분포 자체(연속값) KS검정도 병행
    ks = sstats.ks_2samp(shock["revert_ratio"].to_numpy(), bg["revert_ratio"].to_numpy())
    print(f"\nrevert_ratio 분포 KS검정: stat={ks.statistic:.4f} p={ks.pvalue:.6f}")

    # 종목별로도 확인
    print("\n종목별 충격 vs 배경 복귀율:")
    for sym in c.SYMBOLS:
        s = shock[shock["symbol"] == sym]
        b = bg[bg["symbol"] == sym]
        if len(s) == 0 or len(b) == 0:
            continue
        print(f"  {sym}: shock n={len(s)} rate={100*(s['branch']=='reversion').mean():.1f}%  "
             f"bg n={len(b)} rate={100*(b['branch']=='reversion').mean():.1f}%")


if __name__ == "__main__":
    main()
