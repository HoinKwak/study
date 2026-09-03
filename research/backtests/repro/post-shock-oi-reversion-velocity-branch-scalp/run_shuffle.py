"""부호 무작위화 100회 + 승률고정 순열검정, 종목간 신호상관(평균+위기국면)."""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as c
import engine
import stats_utils as su


def main():
    data = c.load_all()
    cfg = engine.Config()
    df, _ = engine.run(c.SYMBOLS, data, cfg)
    _, oos, _ = su.split_is_oos(df)
    r = oos["r_multiple"].to_numpy()
    n = len(r)
    obs_mean = r.mean()
    win_rate = (r > 0).mean()
    print(f"관측 mean(R)={obs_mean:.4f} n={n} 승률={win_rate*100:.1f}%")

    rng = np.random.default_rng(11)
    # 1) 부호 무작위화(50/50) 100회
    sign_means = []
    for _ in range(100):
        signs = rng.choice([-1, 1], size=n)
        sign_means.append((np.abs(r) * signs).mean())
    sign_means = np.array(sign_means)
    pctile_sign = (sign_means <= obs_mean).mean() * 100
    print(f"\n부호 무작위화(50/50) 100회: 관측치 백분위={pctile_sign:.1f} "
         f"(50=무작위와 동일, <50=무작위보다 나쁨)")

    # 2) 승률고정 순열검정: 각 트레이드의 |R|은 고정, 부호를 관측 승률 그대로 유지한 채
    #    무작위로 재배치(승리/패배 라벨을 셔플)
    abs_r = np.abs(r)
    win_mask = r > 0
    n_win = int(win_mask.sum())
    perm_means = []
    for _ in range(100):
        perm_win = rng.permutation(n) < n_win
        signs = np.where(perm_win, 1, -1)
        perm_means.append((abs_r * signs).mean())
    perm_means = np.array(perm_means)
    pctile_perm = (perm_means <= obs_mean).mean() * 100
    print(f"승률고정 순열검정 100회: 관측치 백분위={pctile_perm:.1f}")

    # 3) 종목간 신호상관: 일별 진입건수(방향포함 R 합) 상관, 평균 vs 위기국면
    oos2 = oos.copy()
    oos2["day"] = oos2["entry_time"].dt.floor("D")
    pivot = oos2.pivot_table(index="day", columns="symbol", values="r_multiple", aggfunc="sum")
    pivot_bin = (~pivot.isna()).astype(int)  # 그날 진입 여부(이진, 신호상관용)
    print("\n=== 종목간 신호상관(일별 진입 이진, pandas.corr pairwise) — 평시 ===")
    corr_all = pivot_bin.corr()
    print(corr_all.round(3))
    avg_corr = corr_all.to_numpy()[np.triu_indices(len(corr_all), k=1)]
    print(f"평균 상관(대각제외)={np.nanmean(avg_corr):.4f}")

    # 위기국면: BTC 1h 절대수익률 상위 5% 일자
    btc = data["BTCUSDT"].h1
    ret = btc["close"].pct_change()
    daily_abs_ret = ret.abs().resample("1D").max()
    thresh = daily_abs_ret.quantile(0.95)
    crisis_days = set(daily_abs_ret[daily_abs_ret >= thresh].index)
    crisis_mask = pivot_bin.index.isin(crisis_days)
    pivot_crisis = pivot_bin[crisis_mask]
    if len(pivot_crisis) >= 5:
        corr_crisis = pivot_crisis.corr()
        avg_crisis = corr_crisis.to_numpy()[np.triu_indices(len(corr_crisis), k=1)]
        print(f"\n위기국면(BTC 절대수익률 상위5%, {len(pivot_crisis)}일) 평균 상관="
             f"{np.nanmean(avg_crisis):.4f}")
    else:
        print(f"\n위기국면 일수 부족(n={len(pivot_crisis)})")

    # 동시진입 클러스터(같은 캘린더일 3종목 이상)
    same_day_ct = pivot_bin.sum(axis=1)
    print(f"\n동시진입(같은 캘린더일) 3종목+ 비율: {(same_day_ct>=3).mean()*100:.1f}% "
         f"7종목 전부: {(same_day_ct>=7).mean()*100:.2f}%")


if __name__ == "__main__":
    main()
