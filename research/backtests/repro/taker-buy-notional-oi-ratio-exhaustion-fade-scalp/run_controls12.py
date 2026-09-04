"""핵심 대조군 ①②: 분자를 총거래대금으로/분모를 24h거래대금으로 바꾼 버전과 net PF 비교
+ 부트스트랩(구분 불가 여부, 사전 폐기조건 (b))."""
import pickle

import numpy as np

import common
import engine
import stats_utils as su

with open(common.SP / "sigs_200.pkl", "rb") as f:
    sigs = pickle.load(f)

with open(common.SP / "results_main.pkl", "rb") as f:
    results = pickle.load(f)
base_net = results[(False, True)]
_, base_oos, _ = su.split_is_oos(base_net)

out = {}
for mode, label in [("total_vol", "①총거래대금 분자"), ("vol24h_buy_sell", "②24h거래대금 분모")]:
    for fee_on in (True, False):
        cfg = engine.RunConfig(mode=mode, reverse=False, fee_on=fee_on)
        trades = engine.run_all(sigs, cfg)
        all_trades = [t for lst in trades.values() for t in lst]
        df = su.trades_df(all_trades)
        is_df, oos_df, full_df = su.split_is_oos(df)
        out[(mode, fee_on)] = df
        print(f"{label:16s} fee_on={fee_on!s:5s}")
        print("  " + su.print_summary(su.summary(is_df, "IS")))
        print("  " + su.print_summary(su.summary(oos_df, "OOS")))

with open(common.SP / "results_controls12.pkl", "wb") as f:
    pickle.dump(out, f)

print("\n### 부트스트랩: base vs 대조군①②(net, OOS) — 사전 폐기조건 (b): 둘 다 p>0.10 이면 무가치 ###")
for mode, label in [("total_vol", "①"), ("vol24h_buy_sell", "②")]:
    _, ctl_oos, _ = su.split_is_oos(out[(mode, True)])
    bd = su.bootstrap_diff_test(base_oos["r"].to_numpy(), ctl_oos["r"].to_numpy())
    print(f"대조군{label} vs base: {bd}")

print("\n### base ⊆ pool 중복도(대조군②, OI z_buy 상관 매우 높았으므로 트리거 시점 중복 확인) ###")
for mode, label in [("total_vol", "①"), ("vol24h_buy_sell", "②")]:
    _, ctl_oos, _ = su.split_is_oos(out[(mode, True)])
    ip = su.independent_pair_diff(base_oos, ctl_oos)
    print(f"대조군{label}: {ip}")
