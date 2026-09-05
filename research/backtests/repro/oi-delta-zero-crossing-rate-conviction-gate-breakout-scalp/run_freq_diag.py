"""빈도·결합확률·동어반복 진단(스펙 §결합확률 실측/전제일관성/동어반복 점검 대응)."""
import pickle

import numpy as np
import pandas as pd

import common

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

rows = []
corr_rows = []
for sym, sig in sigs.items():
    df = sig.df15m
    u = sig.donch_upper.to_numpy(float)
    lo = sig.donch_lower.to_numpy(float)
    c = df["close"].to_numpy(float)
    zcr_p = sig.zcr_pctile
    vol_p = sig.vol_z_pctile
    oi_std = sig.oi_change_stdev
    atr_roc = sig.atr_roc
    rv15 = sig.rv15
    cumsum = sig.oi_cumsum_window.to_numpy(float)

    valid = np.isfinite(u) & np.isfinite(lo) & np.isfinite(c) & zcr_p.notna().to_numpy()
    n_valid = valid.sum()
    long_break = valid & (c > u)
    short_break = valid & (c < lo)
    both = long_break & short_break
    long_break = long_break & ~both
    short_break = short_break & ~both
    n_break = long_break.sum() + short_break.sum()

    zcr30 = (zcr_p <= 30.0).to_numpy() & valid
    n_zcr30_uncond = zcr30.sum()

    # zcr<=30 조건부(브레이크아웃 시점 한정)
    break_mask = long_break | short_break
    n_zcr30_given_break = (zcr30 & break_mask).sum()
    rate_zcr30_given_break = n_zcr30_given_break / n_break if n_break else float("nan")
    rate_zcr30_uncond = n_zcr30_uncond / n_valid if n_valid else float("nan")

    # 방향 일치(OI 누적방향 vs 브레이크아웃 방향), 브레이크아웃 시점 한정
    dir_match_long = long_break & (cumsum > 0)
    dir_match_short = short_break & (cumsum < 0)
    n_dirmatch = dir_match_long.sum() + dir_match_short.sum()
    rate_dirmatch_given_break = n_dirmatch / n_break if n_break else float("nan")

    # 결합조건(zcr30 AND dirmatch), 브레이크아웃 시점 한정
    joint_long = long_break & zcr30 & (cumsum > 0)
    joint_short = short_break & zcr30 & (cumsum < 0)
    n_joint = joint_long.sum() + joint_short.sum()
    rate_joint_given_break = n_joint / n_break if n_break else float("nan")
    # 독립기대: P(zcr30)*P(dirmatch) (둘 다 브레이크아웃 조건부 실측확률로 계산, 곱은 "독립 가정시" 기대)
    indep_expect_given_break = rate_zcr30_given_break * rate_dirmatch_given_break

    n_days = (df.index.max() - df.index.min()).days
    yr = n_days / 365.25

    rows.append(dict(symbol=sym, n_valid=n_valid, n_break=n_break, break_per_yr=n_break / yr,
                     n_joint=n_joint, joint_per_yr=n_joint / yr,
                     rate_zcr30_uncond=rate_zcr30_uncond * 100,
                     rate_zcr30_given_break=rate_zcr30_given_break * 100,
                     rate_dirmatch_given_break=rate_dirmatch_given_break * 100,
                     rate_joint_given_break=rate_joint_given_break * 100,
                     indep_expect_given_break=indep_expect_given_break * 100,
                     ratio_joint_vs_indep=(rate_joint_given_break / indep_expect_given_break
                                          if indep_expect_given_break else float("nan"))))

    # --- 동어반복 상관: 전체구간 vs 트리거(브레이크아웃) 시점 한정, pandas.corr()(pairwise) ---
    d = pd.DataFrame({"zcr_p": zcr_p, "vol_p": vol_p, "oi_std": oi_std, "atr_roc": atr_roc,
                      "rv15": rv15})
    corr_all = d.corr()
    trig_idx = df.index[break_mask]
    d_trig = d.loc[trig_idx]
    corr_trig = d_trig.corr()
    corr_rows.append(dict(symbol=sym,
                          corr_zcr_volz_all=corr_all.loc["zcr_p", "vol_p"],
                          corr_zcr_volz_trig=corr_trig.loc["zcr_p", "vol_p"],
                          corr_zcr_oistd_all=corr_all.loc["zcr_p", "oi_std"],
                          corr_zcr_oistd_trig=corr_trig.loc["zcr_p", "oi_std"],
                          corr_zcr_atrroc_all=corr_all.loc["zcr_p", "atr_roc"],
                          corr_zcr_atrroc_trig=corr_trig.loc["zcr_p", "atr_roc"],
                          corr_zcr_rv15_all=corr_all.loc["zcr_p", "rv15"],
                          corr_zcr_rv15_trig=corr_trig.loc["zcr_p", "rv15"]))

freq_df = pd.DataFrame(rows)
corr_df = pd.DataFrame(corr_rows)
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
print("=== 빈도·결합확률 ===")
print(freq_df.to_string(index=False))
print("\n=== 동어반복 상관(전체구간 vs 트리거시점 한정) ===")
print(corr_df.to_string(index=False))

freq_df.to_csv(f"{common.SP}/freq_diag.csv", index=False)
corr_df.to_csv(f"{common.SP}/corr_diag.csv", index=False)
