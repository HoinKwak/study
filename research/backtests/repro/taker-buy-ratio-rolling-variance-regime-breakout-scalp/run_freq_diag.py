"""빈도·결합확률·동어반복 진단(스펙 §결합확률 실측/전제일관성/동어반복 점검 대응).
⚠️최우선 확인사항: tvr_std 와 가격 RV·BBW·OI변화stdev·거래량z 의 상관을 전체구간+트리거시점
한정 둘 다 계산(스카우트 최우선 의심점 — "테이커비율 저분산=가격 레인지 스퀴즈의 재서술" 위험)."""
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
    tvr_p = sig.tvr_std_pctile
    rv_p = sig.rv15_pctile
    bbw_p = sig.bbw_pctile
    oi_std = sig.oi_change_stdev
    vol_z = sig.vol_z
    tvr_mean = sig.tvr_mean_window.to_numpy(float)

    valid = np.isfinite(u) & np.isfinite(lo) & np.isfinite(c) & tvr_p.notna().to_numpy()
    n_valid = valid.sum()
    long_break = valid & (c > u)
    short_break = valid & (c < lo)
    both = long_break & short_break
    long_break = long_break & ~both
    short_break = short_break & ~both
    n_break = long_break.sum() + short_break.sum()

    tvr30 = (tvr_p <= 30.0).to_numpy() & valid
    n_tvr30_uncond = tvr30.sum()

    # tvr<=30 조건부(브레이크아웃 시점 한정)
    break_mask = long_break | short_break
    n_tvr30_given_break = (tvr30 & break_mask).sum()
    rate_tvr30_given_break = n_tvr30_given_break / n_break if n_break else float("nan")
    rate_tvr30_uncond = n_tvr30_uncond / n_valid if n_valid else float("nan")

    # 방향 일치(테이커매수비율 평균 vs 브레이크아웃 방향), 브레이크아웃 시점 한정
    dir_match_long = long_break & (tvr_mean > 1.0)
    dir_match_short = short_break & (tvr_mean < 1.0)
    n_dirmatch = dir_match_long.sum() + dir_match_short.sum()
    rate_dirmatch_given_break = n_dirmatch / n_break if n_break else float("nan")

    # 결합조건(tvr30 AND dirmatch), 브레이크아웃 시점 한정
    joint_long = long_break & tvr30 & (tvr_mean > 1.0)
    joint_short = short_break & tvr30 & (tvr_mean < 1.0)
    n_joint = joint_long.sum() + joint_short.sum()
    rate_joint_given_break = n_joint / n_break if n_break else float("nan")
    indep_expect_given_break = rate_tvr30_given_break * rate_dirmatch_given_break

    n_days = (df.index.max() - df.index.min()).days
    yr = n_days / 365.25

    rows.append(dict(symbol=sym, n_valid=n_valid, n_break=n_break, break_per_yr=n_break / yr,
                     n_joint=n_joint, joint_per_yr=n_joint / yr,
                     rate_tvr30_uncond=rate_tvr30_uncond * 100,
                     rate_tvr30_given_break=rate_tvr30_given_break * 100,
                     rate_dirmatch_given_break=rate_dirmatch_given_break * 100,
                     rate_joint_given_break=rate_joint_given_break * 100,
                     indep_expect_given_break=indep_expect_given_break * 100,
                     ratio_joint_vs_indep=(rate_joint_given_break / indep_expect_given_break
                                          if indep_expect_given_break else float("nan"))))

    # --- 동어반복 상관: 전체구간 vs 트리거(브레이크아웃) 시점 한정, pandas.corr()(pairwise) ---
    # tvr_std(원값)·rv15·bbw·oi_change_stdev·vol_z 원값끼리 상관도 함께 본다(스카우트 지시:
    # "분산 지표와 레인지/ATR/실현변동성/거래량 z 의 상관을 ①전체구간 ②트리거시점 한정").
    d = pd.DataFrame({"tvr_std": sig.tvr_std, "rv15": sig.rv15, "bbw": sig.bbw,
                      "oi_std": oi_std, "vol_z": vol_z})
    corr_all = d.corr()
    trig_idx = df.index[break_mask]
    d_trig = d.loc[trig_idx]
    corr_trig = d_trig.corr()
    corr_rows.append(dict(symbol=sym,
                          corr_tvr_rv_all=corr_all.loc["tvr_std", "rv15"],
                          corr_tvr_rv_trig=corr_trig.loc["tvr_std", "rv15"],
                          corr_tvr_bbw_all=corr_all.loc["tvr_std", "bbw"],
                          corr_tvr_bbw_trig=corr_trig.loc["tvr_std", "bbw"],
                          corr_tvr_oistd_all=corr_all.loc["tvr_std", "oi_std"],
                          corr_tvr_oistd_trig=corr_trig.loc["tvr_std", "oi_std"],
                          corr_tvr_volz_all=corr_all.loc["tvr_std", "vol_z"],
                          corr_tvr_volz_trig=corr_trig.loc["tvr_std", "vol_z"]))

freq_df = pd.DataFrame(rows)
corr_df = pd.DataFrame(corr_rows)
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)
print("=== 빈도·결합확률 ===")
print(freq_df.to_string(index=False))
print("\n=== 동어반복/전제일관성 상관(전체구간 vs 트리거시점 한정, tvr_std 원값 기준) ===")
print(corr_df.to_string(index=False))

freq_df.to_csv(f"{common.SP}/freq_diag.csv", index=False)
corr_df.to_csv(f"{common.SP}/corr_diag.csv", index=False)
