"""부트스트랩(c)(d) 검정 + LOO + top-N 대칭 + 셔플 + 룩어헤드 절단 검증."""
import pickle
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd

import common
import engine
import stats_utils as su

with open(common.SP / "results_main.pkl", "rb") as f:
    results = pickle.load(f)

is_df, oos_df, full_df = su.split_is_oos(results["base"])
_is_c, oos_c, _full_c = su.split_is_oos(results["ctrl_c_h1only"])
_is_d, oos_d, _full_d = su.split_is_oos(results["ctrl_d_h4d1"])
_is_r, oos_r, _full_r = su.split_is_oos(results["reverse"])

print("=== 사전 폐기조건 (c): base vs 1h단독 게이트, OOS net mean(R) 비교 ===")
res_c = su.bootstrap_diff_indep(oos_df["r"].to_numpy(), oos_c["r"].to_numpy(), n_boot=5000)
print(f"mean(base)={res_c['mean_a']:.4f} mean(h1only)={res_c['mean_b']:.4f} "
     f"P(mean_base<=mean_h1only)={res_c['p_a_le_b']:.4f}")
res_c_mn = su.bootstrap_matched_n_diff(oos_c["r"].to_numpy(), oos_df["r"].to_numpy(), n_boot=5000)
print(f"[표본수 맞춤] base(n={res_c_mn['n']}) mean={res_c_mn['base_mean']:.4f} vs "
     f"h1only pool 재표집 분포평균={res_c_mn['pool_dist_mean']:.4f} base 백분위={res_c_mn['pctile']:.1f}")

print("\n=== 사전 폐기조건 (d): base(삼중) vs 4h+1d(1h 제거), OOS net mean(R) 비교 ===")
res_d = su.bootstrap_diff_indep(oos_df["r"].to_numpy(), oos_d["r"].to_numpy(), n_boot=5000)
print(f"mean(base)={res_d['mean_a']:.4f} mean(h4d1)={res_d['mean_b']:.4f} "
     f"P(mean_base<=mean_h4d1)={res_d['p_a_le_b']:.4f}")

print("\n=== 정방향 vs 반전, OOS net mean(R) 비교(표본수 다름 -> 독립 부트스트랩) ===")
res_rev = su.bootstrap_diff_indep(oos_df["r"].to_numpy(), oos_r["r"].to_numpy(), n_boot=5000)
print(f"mean(정방향)={res_rev['mean_a']:.4f} mean(반전)={res_rev['mean_b']:.4f} "
     f"P(정방향<=반전)={res_rev['p_a_le_b']:.4f}")

print("\n=== 부호 무작위화 셔플(100회, base OOS net) ===")
sh = su.sign_shuffle_test(oos_df, n_shuffle=100)
print(sh)

print("\n=== LOO(symbol) — base OOS net, 종목 하나씩 제외 ===")
for sym in common.SYMBOLS:
    d = oos_df[oos_df["symbol"] != sym]
    print(su.fmt(su.summary(d, f"제외:{sym}")))

print("\n=== top-N 대칭 제거(base OOS net) ===")
d = oos_df.sort_values("r", ascending=False).reset_index(drop=True)
n = len(d)
for k in [1, 3, 5, 10, 20]:
    if k * 2 >= n:
        break
    remove_top = d.iloc[k:]
    print(su.fmt(su.summary(remove_top, f"최대이익 top-{k} 제거")))
    remove_bot = d.iloc[:-k]
    print(su.fmt(su.summary(remove_bot, f"최대손실 top-{k} 제거")))

print("\n=== 대조군(c)/(d)/reverse LOO 요약(최소값만) ===")
for label, dd in [("ctrl_c", oos_c), ("ctrl_d", oos_d)]:
    worst = None
    for sym in common.SYMBOLS:
        s = su.summary(dd[dd["symbol"] != sym], sym)
        if worst is None or s["t"] < worst["t"]:
            worst = s
    print(label, "최소 t(LOO):", su.fmt(worst))
