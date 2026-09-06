"""빈도·결합확률·전제일관성·동어반복 진단(스펙 §결합확률 실측/전제일관성/동어반복 점검 대응).
⚠️최우선 확인: λ_gap 과 ①대칭(매수/매도 미분리) λ(lambda_all) ②taker_buy_ratio 레벨 자체
③OI-가격 탄력성(간이 프록시) 의 상관을 전체구간+트리거시점 한정 둘 다 계산."""
import pickle

import numpy as np
import pandas as pd

import common

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

freq_rows = []
corr_rows = []
sample_rows = []

for sym, sig in sigs.items():
    df = sig.df15m
    n = len(df)
    gap_p = sig.gap_pctile.to_numpy(float)
    trig_p = sig.sv3_abs_pctile.to_numpy(float)
    sv3 = sig.sv3.to_numpy(float)

    valid = np.isfinite(gap_p) & np.isfinite(trig_p) & np.isfinite(sv3)
    n_valid = valid.sum()

    trigger = valid & (trig_p > common.SV_TRIGGER_PCTILE)
    n_trigger = trigger.sum()

    gap_hi = valid & (gap_p >= common.GAP_HI_PCTILE)
    gap_lo = valid & (gap_p <= common.GAP_LO_PCTILE)
    rate_gap_hi = gap_hi.sum() / n_valid if n_valid else float("nan")
    rate_gap_lo = gap_lo.sum() / n_valid if n_valid else float("nan")
    rate_trigger = n_trigger / n_valid if n_valid else float("nan")

    entry_long = trigger & gap_hi & (sv3 < 0)   # base 채택안(페이드)
    entry_short = trigger & gap_lo & (sv3 > 0)
    n_entry = entry_long.sum() + entry_short.sum()
    indep_expect = (rate_trigger * rate_gap_hi * 0.5 + rate_trigger * rate_gap_lo * 0.5)  # sv3 부호는 대략 50/50 가정

    n_days = (df.index.max() - df.index.min()).days
    yr = n_days / 365.25

    freq_rows.append(dict(symbol=sym, n_valid=n_valid, n_trigger=n_trigger,
                          trigger_per_yr=n_trigger / yr, n_entry=n_entry, entry_per_yr=n_entry / yr,
                          rate_gap_hi=rate_gap_hi * 100, rate_gap_lo=rate_gap_lo * 100,
                          rate_trigger=rate_trigger * 100,
                          indep_expect_pct=indep_expect * 100,
                          ratio_vs_indep=(n_entry / n_valid) / indep_expect if indep_expect else float("nan")))

    # --- 표본크기 불안정 비율(사전 폐기조건 c): n_buy<50 or n_sell<50 인 비율 ---
    nb, ns = sig.n_buy, sig.n_sell
    valid_n = np.isfinite(nb) & np.isfinite(ns)
    insufficient = valid_n & ((nb < common.MIN_SAMPLES_PER_SIDE) | (ns < common.MIN_SAMPLES_PER_SIDE))
    frac_insufficient = insufficient.sum() / valid_n.sum() if valid_n.sum() else float("nan")
    sample_rows.append(dict(symbol=sym, frac_insufficient_pct=frac_insufficient * 100,
                            n_buy_min=np.nanmin(nb), n_sell_min=np.nanmin(ns)))

    # --- 동어반복/전제일관성 상관: 전체구간 vs 트리거시점 한정 ---
    lambda_all_s = pd.Series(sig.lambda_all, index=df.index)
    ratio_mean = sig.ratio_mean_window
    oi_change = sig.oi_change
    delta_close = df["close"].diff()
    # 간이 탄력성 프록시: ΔOI 를 Δprice 에 회귀(전체 봉, lambda_window 롤링) — oi-price-elasticity 대용
    dc_np = delta_close.to_numpy(float)
    oi_np = oi_change.to_numpy(float)
    all_mask = np.isfinite(dc_np) & np.isfinite(oi_np)
    elasticity, _ = common._masked_rolling_ols_slope(dc_np, oi_np, all_mask, common.LAMBDA_WINDOW, 30)
    elasticity_s = pd.Series(elasticity, index=df.index)

    d = pd.DataFrame({"lambda_gap": sig.lambda_gap, "lambda_all": lambda_all_s,
                      "ratio_mean": ratio_mean, "elasticity": elasticity_s})
    corr_all = d.corr()
    trig_idx = df.index[trigger]
    d_trig = d.loc[trig_idx]
    corr_trig = d_trig.corr()
    corr_rows.append(dict(symbol=sym,
                          corr_gap_all_all=corr_all.loc["lambda_gap", "lambda_all"],
                          corr_gap_all_trig=corr_trig.loc["lambda_gap", "lambda_all"],
                          corr_gap_ratio_all=corr_all.loc["lambda_gap", "ratio_mean"],
                          corr_gap_ratio_trig=corr_trig.loc["lambda_gap", "ratio_mean"],
                          corr_gap_elast_all=corr_all.loc["lambda_gap", "elasticity"],
                          corr_gap_elast_trig=corr_trig.loc["lambda_gap", "elasticity"]))

freq_df = pd.DataFrame(freq_rows)
corr_df = pd.DataFrame(corr_rows)
sample_df = pd.DataFrame(sample_rows)
pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 20)
print("=== 빈도·결합확률(채택안 base 기준) ===")
print(freq_df.to_string(index=False))
print("\n=== 표본크기 불안정 비율(사전 폐기조건 c: 30% 초과시 게이트 재검토) ===")
print(sample_df.to_string(index=False))
print("\n=== 동어반복/전제일관성 상관(전체구간 vs 트리거시점 한정) ===")
print(corr_df.to_string(index=False))

freq_df.to_csv(f"{common.SP}/freq_diag.csv", index=False)
corr_df.to_csv(f"{common.SP}/corr_diag.csv", index=False)
sample_df.to_csv(f"{common.SP}/sample_diag.csv", index=False)
