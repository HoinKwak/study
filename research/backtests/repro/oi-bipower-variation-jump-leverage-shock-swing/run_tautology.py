"""동어반복(tautology) 점검: OI-JR vs 가격-JR 상관(전체구간 vs 트리거시점 한정), 점프일 중첩률,
'조용한 점프'(OI만 점프, 가격은 안 튐) 빈도, 종목 간 신호 상관(평시 vs 위기국면 꼬리상관)."""
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oibv")
import common
import engine

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

cfg = engine.RunConfig()

print("=" * 70)
print("① OI-JR pctile vs 가격-JR pctile 상관")
print("=" * 70)
full_rows = []
trig_rows = []
jump_flags = {}
for sym, sd in sigs.items():
    oi_p, px_p, day_ret, atr = engine._build_trigger_arrays(sd, cfg)
    idx = sd.d1.index
    s_oi = pd.Series(oi_p, index=idx)
    s_px = pd.Series(px_p, index=idx)
    both = pd.concat([s_oi.rename("oi"), s_px.rename("px")], axis=1).dropna()
    corr_full = both["oi"].corr(both["px"]) if len(both) > 2 else float("nan")
    oi_jump = (s_oi >= cfg.jump_pctile)
    px_jump = (s_px >= cfg.jump_pctile)
    either = (oi_jump | px_jump) & s_oi.notna() & s_px.notna()
    trig_both = both.loc[both.index.isin(idx[either.reindex(idx, fill_value=False)])]
    corr_trig = trig_both["oi"].corr(trig_both["px"]) if len(trig_both) > 2 else float("nan")
    n_oi_jump = int(oi_jump.sum()); n_px_jump = int(px_jump.sum())
    n_both = int((oi_jump & px_jump).sum())
    n_quiet_oi_only = int((oi_jump & ~px_jump).sum())  # OI만 점프, 가격은 정상
    full_rows.append((sym, corr_full, len(both)))
    trig_rows.append((sym, corr_trig, len(trig_both), n_oi_jump, n_px_jump, n_both,
                      n_quiet_oi_only))
    jump_flags[sym] = pd.DataFrame({"oi_jump": oi_jump, "px_jump": px_jump, "day_ret": day_ret},
                                   index=idx)

print(f"{'심볼':10s} {'전체상관':>10s} {'n':>6s}")
for sym, c, n in full_rows:
    print(f"{sym:10s} {c:10.3f} {n:6d}")

print(f"\n{'심볼':10s} {'트리거시점상관':>12s} {'n':>6s} {'OI점프일':>8s} {'가격점프일':>8s} "
     f"{'둘다':>6s} {'OI만(조용)':>10s}")
for sym, c, n, noi, npx, nboth, nquiet in trig_rows:
    print(f"{sym:10s} {c:12.3f} {n:6d} {noi:8d} {npx:8d} {nboth:6d} {nquiet:10d}")

print("\n" + "=" * 70)
print("② 종목 간 신호 상관 — 평시 vs 위기국면(꼬리)")
print("=" * 70)
# 점프일(OI 기준) 이진 인디케이터를 종목 간 정렬해 상관행렬
mat = pd.DataFrame({sym: jump_flags[sym]["oi_jump"].astype(float) for sym in jump_flags})
mat = mat.dropna(how="all")
corr_mat = mat.corr()
vals = corr_mat.to_numpy()
iu = np.triu_indices_from(vals, k=1)
print(f"평시(전체) 종목쌍 평균 OI-점프일 상관: {np.nanmean(vals[iu]):.4f}")

# 위기국면: BTC 절대일수익률 상위 5% 날
btc_ret = jump_flags["BTCUSDT"]["day_ret"].abs()
thresh = btc_ret.quantile(0.95)
crisis_days = btc_ret[btc_ret >= thresh].index
mat_crisis = mat.loc[mat.index.isin(crisis_days)]
if len(mat_crisis) > 5:
    corr_crisis = mat_crisis.corr()
    vals_c = corr_crisis.to_numpy()
    iuc = np.triu_indices_from(vals_c, k=1)
    print(f"위기국면(BTC |일수익률| 상위5%, n={len(mat_crisis)}일) 종목쌍 평균 상관: "
         f"{np.nanmean(vals_c[iuc]):.4f}")
else:
    print(f"위기국면 표본 부족(n={len(mat_crisis)})")

# 7종목 동시 점프일 비율
n_simul = (mat.sum(axis=1) == len(mat.columns)).sum()
n_ge3 = (mat.sum(axis=1) >= 3).sum()
print(f"\n7종목 동시 OI-점프일: {n_simul}건 / 3종목 이상 동시: {n_ge3}건 (총 {len(mat)}일)")

with open(f"{common.SP}/tautology.pkl", "wb") as f:
    pickle.dump(dict(full_rows=full_rows, trig_rows=trig_rows, corr_mat=corr_mat,
                     n_simul=n_simul, n_ge3=n_ge3), f)
print("\n저장 완료: tautology.pkl")
