import pickle
import common, stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

df_net = results[("zcr_lo", True)]
is_df, oos_df, full_df = su.split_is_oos(df_net)

print("symbol,period,n,PF_R,mean_R,t,winrate,sum_R")
for period_name, d in [("IS", is_df), ("OOS", oos_df), ("FULL", full_df)]:
    for sym, g in d.groupby("symbol"):
        s = su.summary(g, sym)
        print(f"{sym},{period_name},{s['n']},{s['pf_r']:.3f},{s['mean_r']:+.4f},{s['t']:+.3f},{s['win_rate']:.1f},{s['sum_r']:+.2f}")
