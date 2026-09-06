"""1단계 검증(스펙 필수): 게이트 없이 λ_gap 부호별(gap_pctile>=80 vs <=20)로, 트리거(3봉 누적 |sv|
상위 15%ile) 발생 이후 sv3 부호 방향으로 N봉 순방향 지속 승률을 집계 — 가설 방향(숏: gap 높음+
sv3<0, 롱: gap 낮음+sv3>0)이 실제로 성립하는지 확인. 반대로 나오면 방향을 뒤집어야 한다."""
import pickle

import numpy as np
import pandas as pd

import common

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

N_LIST = [4, 8, 16]  # 1h/2h/4h(15m 기준)

rows = []
for sym, sig in sigs.items():
    df = sig.df15m
    close = df["close"].to_numpy(float)
    n = len(close)
    gap_p = sig.gap_pctile.to_numpy(float)
    trig_p = sig.sv3_abs_pctile.to_numpy(float)
    sv3 = sig.sv3.to_numpy(float)

    trigger = trig_p > common.SV_TRIGGER_PCTILE
    hi = trigger & (gap_p >= common.GAP_HI_PCTILE) & np.isfinite(sv3) & (sv3 < 0)   # 가설: 숏
    lo = trigger & (gap_p <= common.GAP_LO_PCTILE) & np.isfinite(sv3) & (sv3 > 0)   # 가설: 롱

    for N in N_LIST:
        fwd = np.full(n, np.nan)
        fwd[: n - N] = close[N:] - close[: n - N]

        # 숏 가설: fwd < 0 이면 "가설방향 지속"(가격이 계속 밀림)
        hi_idx = np.where(hi & np.isfinite(fwd))[0]
        hi_hit = (fwd[hi_idx] < 0).mean() if len(hi_idx) else float("nan")
        # 롱 가설: fwd > 0 이면 "가설방향 지속"
        lo_idx = np.where(lo & np.isfinite(fwd))[0]
        lo_hit = (fwd[lo_idx] > 0).mean() if len(lo_idx) else float("nan")

        rows.append(dict(symbol=sym, N=N, n_hi=len(hi_idx), hi_hitrate=hi_hit * 100 if len(hi_idx) else float("nan"),
                         n_lo=len(lo_idx), lo_hitrate=lo_hit * 100 if len(lo_idx) else float("nan")))

res = pd.DataFrame(rows)
pd.set_option("display.width", 200)
print("=== 방향 사전검증(게이트 없이, 가설방향 지속 승률 — 50% 초과해야 가설 지지) ===")
print(res.to_string(index=False))

print("\n=== N별 합산(전 종목 풀링, 단순평균) ===")
for N in N_LIST:
    sub = res[res["N"] == N]
    w_hi = (sub["n_hi"] * sub["hi_hitrate"]).sum() / sub["n_hi"].sum() if sub["n_hi"].sum() else float("nan")
    w_lo = (sub["n_lo"] * sub["lo_hitrate"]).sum() / sub["n_lo"].sum() if sub["n_lo"].sum() else float("nan")
    print(f"N={N:3d}: 숏가설(gap>=80&sv3<0) n={sub['n_hi'].sum():6d} 가설방향지속률={w_hi:.2f}%   "
         f"롱가설(gap<=20&sv3>0) n={sub['n_lo'].sum():6d} 가설방향지속률={w_lo:.2f}%")

res.to_csv(f"{common.SP}/direction_precheck.csv", index=False)
