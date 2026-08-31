"""게이트없음 대조군(순수 Donchian+EMA, 스트릭게이트 없음) 비교.
- 표본수 맞춘 부트스트랩 100회 (base=gated, pool=ungated)
- base ⊆ pool 중첩 여부 확인 + 중복 없는 독립 Welch t검정 병행
short_mode: 'streak_down'(spec 기본, 표본 극소) / 'streak_up_alt'(스윕 대안, 표본 충분)
"""
import pickle
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import common
import engine
import stats_utils as su

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

for short_mode in ["streak_down", "streak_up_alt"]:
    print(f"\n############ short_mode={short_mode} ############")
    cfg_gated = engine.RunConfig(mode="gated", short_mode=short_mode)
    cfg_ungated = engine.RunConfig(mode="ungated", short_mode=short_mode)

    tg = engine.run_all(sigs, cfg_gated)
    tu = engine.run_all(sigs, cfg_ungated)
    dg = su.trades_df([t for lst in tg.values() for t in lst])
    du = su.trades_df([t for lst in tu.values() for t in lst])

    _, oos_g, _ = su.split_is_oos(dg)
    _, oos_u, _ = su.split_is_oos(du)
    print(f"gated OOS n={len(oos_g)} PF(R)={su.pf_r(oos_g):.3f} mean(R)={oos_g['r'].mean():.4f}")
    print(f"ungated OOS n={len(oos_u)} PF(R)={su.pf_r(oos_u):.3f} mean(R)={oos_u['r'].mean():.4f}")

    # base ⊆ pool 중첩 확인: 같은 symbol+entry_time 조합이 ungated 트레이드 집합에도 있는지
    key_g = set(zip(oos_g["symbol"], oos_g["entry_time"]))
    key_u = set(zip(oos_u["symbol"], oos_u["entry_time"]))
    overlap = key_g & key_u
    print(f"base(gated) ⊆ pool(ungated) 중첩: {len(overlap)}/{len(key_g)} "
         f"({len(overlap)/max(len(key_g),1)*100:.1f}%)")

    # 표본수 맞춘 부트스트랩 100회: pool=ungated(全), base=gated
    if len(oos_g) >= 3 and len(oos_u) >= 3:
        res = su.bootstrap_matched_n_diff(oos_u["r"].to_numpy(), oos_g["r"].to_numpy(), n_boot=100)
        print(f"매칭-N 부트스트랩(100회): base_mean={res['base_mean']:.4f} "
             f"pool_dist_mean={res['pool_dist_mean']:.4f} pctile={res['pctile']:.1f}")
    else:
        print("표본 부족으로 매칭-N 부트스트랩 생략")

    # 중복 없는 독립 검정: ungated 에서 gated 와 겹치는 트레이드 제외한 잔여표본
    mask_u_excl = ~oos_u.apply(lambda row: (row["symbol"], row["entry_time"]) in overlap, axis=1)
    oos_u_excl = oos_u[mask_u_excl]
    print(f"중복제외 ungated 잔여 n={len(oos_u_excl)}")
    if len(oos_g) >= 2 and len(oos_u_excl) >= 2:
        w = su.welch_independent(oos_g["r"].to_numpy(), oos_u_excl["r"].to_numpy())
        print(f"독립 Welch(gated vs 중복제외 ungated): t={w['t']:.3f} p={w['p']:.4f} "
             f"mean_gated={w.get('mean_a', float('nan')):.4f} mean_ungated_excl={w.get('mean_b', float('nan')):.4f}")
