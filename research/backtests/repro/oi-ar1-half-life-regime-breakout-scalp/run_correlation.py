"""전제 일관성 + 동어반복 점검 — φ vs OI변화율stdev / φ vs ROC(oi_growth) / φ vs oi_z.
전체구간 상관(pandas.corr, pairwise)과 "트리거 시점 한정" 상관을 모두 계산한다.
"""
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiar1hl")
import common
import engine

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)
with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

phi_net = results[("phi_hi", True)]

print("### ①전제 일관성: φ vs OI변화율 rolling stdev(같은 30일 창) — 전체구간 상관 ###")
print("  (스펙 사전 폐기조건 c: |r|>=0.6 이면 동어반복 의심)")
full_rows = []
for sym, sig in sigs.items():
    df = pd.DataFrame({"phi": sig.phi, "stdev": sig.oi_change_stdev, "oi_growth": sig.oi_growth,
                       "oi_z": sig.oi_z}).dropna()
    if len(df) < 30:
        continue
    r_stdev = df["phi"].corr(df["stdev"])
    r_roc = df["phi"].corr(df["oi_growth"])
    r_oiz = df["phi"].corr(df["oi_z"])
    full_rows.append((sym, len(df), r_stdev, r_roc, r_oiz))
    print(f"  {sym:10s} n={len(df):6d}  r(phi,stdev)={r_stdev:+.4f}  r(phi,ROC)={r_roc:+.4f}  "
         f"r(phi,oi_z)={r_oiz:+.4f}")

print("\n### ②트리거 시점 한정 상관(phi_hi 게이트가 실제 발화한 신호 시점만) ###")
trig_rows = []
for sym, sig in sigs.items():
    sub = phi_net[phi_net["symbol"] == sym]
    if sub.empty:
        continue
    sig_idx = sub["signal_idx"].to_numpy()
    stdev_at = sig.oi_change_stdev.iloc[sig_idx].to_numpy()
    roc_at = sig.oi_growth.iloc[sig_idx].to_numpy()
    oiz_at = sig.oi_z.iloc[sig_idx].to_numpy()
    phi_at = sig.phi.iloc[sig_idx].to_numpy()
    d = pd.DataFrame({"phi": phi_at, "stdev": stdev_at, "roc": roc_at, "oiz": oiz_at}).dropna()
    if len(d) < 5:
        print(f"  {sym:10s} 트리거 n={len(d)} — 표본 부족(상관 생략)")
        continue
    r_stdev = d["phi"].corr(d["stdev"])
    r_roc = d["phi"].corr(d["roc"])
    r_oiz = d["phi"].corr(d["oiz"])
    trig_rows.append((sym, len(d), r_stdev, r_roc, r_oiz))
    print(f"  {sym:10s} 트리거 n={len(d):4d}  r(phi,stdev)={r_stdev:+.4f}  r(phi,ROC)={r_roc:+.4f}  "
         f"r(phi,oi_z)={r_oiz:+.4f}")

print("\n### ③φ 레짐 지속기간(상태전환) 분포 — '국면 이진 스위치' 우려 점검 ###")
for sym, sig in sigs.items():
    gate = (sig.phi_pctile >= common.PHI_PCTILE_TH).astype(int)
    gate = gate.dropna() if gate.isna().any() else gate
    g = gate.dropna()
    if len(g) < 100:
        continue
    changes = g.diff().fillna(0) != 0
    n_runs = int(changes.sum()) + 1
    avg_run_bars = len(g) / n_runs if n_runs > 0 else float("nan")
    on_frac = g.mean() * 100
    print(f"  {sym:10s} ON비율={on_frac:5.1f}%  상태전환횟수={n_runs:5d}  평균 지속={avg_run_bars:7.1f}봉"
         f"(={avg_run_bars*15/60/24:.1f}일)")
