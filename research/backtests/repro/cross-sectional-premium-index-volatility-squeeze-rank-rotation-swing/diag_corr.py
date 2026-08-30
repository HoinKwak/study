"""동어반복·상관 진단: ①종목간 스퀴즈 퍼센타일 상관(스펙 사전실측 재현) ②횡단면 std
③베이시스 스퀴즈 vs 가격 BB폭 스퀴즈 상관(전체구간/트리거시점) ④위기국면 꼬리상관."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import SYMBOLS, rolling_pctile
from engine import load_all, cross_sectional_calendar


def bb_bandwidth_pctile(price_1d: pd.DataFrame, window: int = 60, bb_period: int = 20,
                         bb_std: float = 2.0) -> pd.Series:
    close = price_1d["close"]
    sma = close.rolling(bb_period).mean()
    std = close.rolling(bb_period).std(ddof=0)
    bw = (2 * bb_std * std) / sma
    return rolling_pctile(bw, window)


def main() -> None:
    universe = load_all(squeeze_window=60, donchian_len=15)
    calendar = cross_sectional_calendar(universe)

    # ① 종목간 squeeze_pctile pairwise 상관(스펙 사전실측 +0.47 재현, 2024-01~2026-07 한정)
    mat = pd.DataFrame({sym: universe[sym]["daily"]["squeeze_pctile"] for sym in SYMBOLS})
    mat = mat.loc[(mat.index >= "2024-01-01") & (mat.index <= "2026-07-31")]
    corr = mat.corr(method="pearson")
    pairs = []
    for i, a in enumerate(SYMBOLS):
        for b in SYMBOLS[i + 1:]:
            pairs.append(corr.loc[a, b])
    print("① 종목간 squeeze_pctile pairwise 상관(2024-01~2026-07, 스펙 재현 구간):")
    print(f"   평균={np.nanmean(pairs):.4f} 범위=[{np.nanmin(pairs):.4f},{np.nanmax(pairs):.4f}] n_pairs={len(pairs)}")

    # 전체 구간(2022-01~2026-07)도 참고로 계산
    mat_full = pd.DataFrame({sym: universe[sym]["daily"]["squeeze_pctile"] for sym in SYMBOLS})
    corr_full = mat_full.corr(method="pearson")
    pairs_full = []
    for i, a in enumerate(SYMBOLS):
        for b in SYMBOLS[i + 1:]:
            pairs_full.append(corr_full.loc[a, b])
    print(f"   [참고] 전체구간(2022-01~) 평균={np.nanmean(pairs_full):.4f} 범위=[{np.nanmin(pairs_full):.4f},{np.nanmax(pairs_full):.4f}]")

    # ② 횡단면 표준편차(요일 평균 아니라 매Monday 평균) — 스펙은 "요일 평균"이라 명시했으나
    #   맥락상 "매 관측일 평균"의 오기로 보고 전체 일자 평균으로 계산, Monday만도 병기.
    cs_std_all = mat.std(axis=1, skipna=True)
    print(f"\n② 횡단면 표준편차: 전체일 평균={cs_std_all.mean():.4f} (스펙 사전실측 0.20)")
    mondays = mat.index[mat.index.dayofweek == 0]
    cs_std_mon = mat.loc[mondays].std(axis=1, skipna=True)
    print(f"   월요일만 평균={cs_std_mon.mean():.4f}")

    # ③ 동어반복: squeeze_pctile vs BB밴드폭 pctile 상관 (전체구간 vs 트리거시점 한정)
    from engine import register_candidates, find_triggers, signal_direction
    cands = register_candidates(universe, calendar, 0.20, 2, rank_mode="topk")
    triggers = find_triggers(universe, cands, 10, 0.70)
    signals = signal_direction(universe, triggers)
    trigger_dates = {(s, td) for s, r, td, dirn in signals}

    from common import load_symbol
    corrs_full, corrs_trig = [], []
    for sym in SYMBOLS:
        data_sym = load_symbol(sym)
        bb_p = bb_bandwidth_pctile(data_sym["price_1d"], window=60)
        sq_p = universe[sym]["daily"]["squeeze_pctile"]
        idx = bb_p.index.intersection(sq_p.index)
        a, b = sq_p.loc[idx].dropna(), bb_p.loc[idx].dropna()
        common_idx = a.index.intersection(b.index)
        r_full = a.loc[common_idx].corr(b.loc[common_idx])
        corrs_full.append(r_full)
        trig_idx = [td for (s, td) in trigger_dates if s == sym]
        trig_idx = [t for t in trig_idx if t in common_idx]
        if len(trig_idx) >= 3:
            r_trig = a.loc[trig_idx].corr(b.loc[trig_idx])
        else:
            r_trig = float("nan")
        corrs_trig.append(r_trig)
        print(f"   {sym}: 전체구간 r={r_full:.3f}  트리거시점(n={len(trig_idx)}) r={r_trig}")
    print(f"\n③ 동어반복(squeeze_pctile vs BB밴드폭 pctile): 전체구간 평균 r={np.nanmean(corrs_full):.3f}"
          f"  트리거시점 평균 r={np.nanmean(corrs_trig):.3f}")

    # ④ 위기국면 꼬리상관: BTC 절대 일간수익률 상위 5% 구간의 squeeze_pctile 상관 vs 평시
    btc_close = universe["BTCUSDT"]["daily"]["price_close"]
    btc_ret = btc_close.pct_change().abs()
    thresh = btc_ret.quantile(0.95)
    crisis_days = btc_ret[btc_ret >= thresh].index
    crisis_days = crisis_days.intersection(mat.index)
    normal_days = mat.index.difference(crisis_days)
    corr_crisis = mat.loc[crisis_days].corr()
    corr_normal = mat.loc[normal_days].corr()
    pc, pn = [], []
    for i, a in enumerate(SYMBOLS):
        for b in SYMBOLS[i + 1:]:
            pc.append(corr_crisis.loc[a, b])
            pn.append(corr_normal.loc[a, b])
    print(f"\n④ 위기국면(BTC |ret| 상위5%, n={len(crisis_days)}) squeeze_pctile 평균상관="
          f"{np.nanmean(pc):.4f}  평시(n={len(normal_days)})={np.nanmean(pn):.4f}")

    result = {
        "xsec_corr_mean_2024_2026": float(np.nanmean(pairs)),
        "xsec_corr_mean_full": float(np.nanmean(pairs_full)),
        "cs_std_all_days": float(cs_std_all.mean()),
        "cs_std_mondays": float(cs_std_mon.mean()),
        "tautology_corr_full_mean": float(np.nanmean(corrs_full)),
        "tautology_corr_trigger_mean": float(np.nanmean(corrs_trig)),
        "crisis_corr_mean": float(np.nanmean(pc)),
        "normal_corr_mean": float(np.nanmean(pn)),
        "n_crisis_days": int(len(crisis_days)),
    }
    with open("out_corr_diag.json", "w") as f:
        json.dump(result, f, indent=2)
    print("\n저장: out_corr_diag.json")


if __name__ == "__main__":
    main()
