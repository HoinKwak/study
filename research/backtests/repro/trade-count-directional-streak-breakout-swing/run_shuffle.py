"""정보원 무력화(셔플) 대조군: 심볼별 count(t) 시계열을 셔플(시간순서 파괴, 부호분포는 보존)해
streak_up/down 을 재계산 → 신호/트레이드 재생성 → 100회 반복. ⚠️ 셔플이 결합 트리거 표본 크기를
바꾸지 않는지(±30% 이내인지) 반드시 확인·보고한다."""
import pickle
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import common
import engine
import stats_utils as su
from dataclasses import replace

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs_orig = pickle.load(f)

N_ITER = 100
rng = np.random.default_rng(2026)


def shuffled_signals(sigs, rng):
    out = {}
    for sym, sig in sigs.items():
        cnt = sig.count.copy()
        n = len(cnt)
        valid = np.isfinite(cnt)
        perm_idx = np.where(valid)[0]
        shuffled = cnt.copy()
        vals = cnt[perm_idx].copy()
        rng.shuffle(vals)
        shuffled[perm_idx] = vals
        su_, sd_ = common.count_streak(shuffled)
        out[sym] = replace(sig, count=shuffled, streak_up=su_, streak_down=sd_)
    return out


settings_settled = None

for short_mode in ["streak_down", "streak_up_alt"]:
    print(f"\n############ short_mode={short_mode} ############")
    cfg = engine.RunConfig(mode="gated", short_mode=short_mode)
    trades_obs = engine.run_all(sigs_orig, cfg)
    dobs = su.trades_df([t for lst in trades_obs.values() for t in lst])
    _, oos_obs, _ = su.split_is_oos(dobs)
    n_obs = len(oos_obs)
    mean_obs = oos_obs["r"].mean() if n_obs else float("nan")
    print(f"관측(원본) OOS n={n_obs} mean(R)={mean_obs:.4f} PF(R)={su.pf_r(oos_obs):.3f}")

    ns = []
    means = []
    for it in range(N_ITER):
        sigs_sh = shuffled_signals(sigs_orig, rng)
        trades_sh = engine.run_all(sigs_sh, cfg)
        dsh = su.trades_df([t for lst in trades_sh.values() for t in lst])
        _, oos_sh, _ = su.split_is_oos(dsh)
        ns.append(len(oos_sh))
        means.append(oos_sh["r"].mean() if len(oos_sh) else np.nan)

    ns = np.array(ns)
    means = np.array(means)
    print(f"셔플 100회 표본크기: mean={ns.mean():.1f} min={ns.min()} max={ns.max()} "
         f"(관측 n={n_obs}, 변화율={(ns.mean()/max(n_obs,1)-1)*100:+.1f}%)")
    valid_means = means[~np.isnan(means)]
    if len(valid_means) >= 10 and np.isfinite(mean_obs):
        pctile = (valid_means <= mean_obs).mean() * 100
        print(f"셔플 mean(R) 분포: 평균={valid_means.mean():.4f} std={valid_means.std():.4f} "
             f"관측값 백분위={pctile:.1f} (유효반복={len(valid_means)}/{N_ITER})")
    else:
        print("유효 셔플 반복 부족으로 백분위 계산 생략")
