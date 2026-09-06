"""클러스터 집중도 분해 — 5일 고정(비중첩) 캘린더 블록 단위로 최고/최악 클러스터 제거를
대칭으로 실행(신규 규칙: 최고 제거만이 아니라 최악 제거까지 대칭으로 할 것).
⚠️`decluster_rolling_days`(gap>window_days 기준 클러스터링)는 본 전략처럼 거래빈도가 높으면
(OOS 725 고유일에 트레이드 7627건 — 하루 평균 ~10.5건) 연속된 두 트레이드 사이 간격이 3~5일을
넘는 경우가 거의 없어 전체가 클러스터 1개로 퇴화한다(run_declustering.py 에서 실측 확인) —
고빈도 전략에는 gap 기반이 아니라 **고정 길이 비중첩 블록**이 적합하다."""
import pickle

import numpy as np
import pandas as pd

import common
import stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

df_net = results[("base", True)]
df_gross = results[("base", False)]
_, oos_net, _ = su.split_is_oos(df_net)
_, oos_gross, _ = su.split_is_oos(df_gross)


def fixed_block(df: pd.DataFrame, days: int) -> pd.DataFrame:
    d = df.copy()
    origin = common.OOS_START
    block_id = ((d["entry_time"] - origin).dt.total_seconds() // (days * 86400)).astype(int)
    d["block"] = block_id
    return d


for days in (5,):
    print(f"\n=== {days}일 고정블록 분해(net, OOS) ===")
    b = fixed_block(oos_net, days)
    agg = b.groupby("block").agg(r_sum=("r", "sum"), n=("r", "size")).reset_index()
    agg = agg.sort_values("r_sum", ascending=False)
    print(f" 고유블록수={len(agg)}  총 순R={agg['r_sum'].sum():.2f}")
    print(" 상위 5개 블록 기여:")
    print(agg.head(5).to_string(index=False))
    top3_share = agg.head(3)["r_sum"].sum() / agg["r_sum"].sum() * 100
    print(f" top-3 블록이 순R의 {top3_share:.1f}% 를 차지")

    for k in (1, 3, 5):
        top_ids = set(agg.head(k)["block"])
        rest = b[~b["block"].isin(top_ids)]
        print(f"  top-{k}(최고) 블록 제거 후:", su.print_summary(su.summary(rest, f"excl_top{k}")))
    worst = agg.sort_values("r_sum")
    for k in (1, 3, 5):
        worst_ids = set(worst.head(k)["block"])
        rest = b[~b["block"].isin(worst_ids)]
        print(f"  worst-{k}(최악) 블록 제거 후:", su.print_summary(su.summary(rest, f"excl_worst{k}")))

    print(f"\n=== {days}일 고정블록 분해(gross, OOS) ===")
    bg = fixed_block(oos_gross, days)
    aggg = bg.groupby("block").agg(r_sum=("r", "sum"), n=("r", "size")).reset_index()
    aggg = aggg.sort_values("r_sum", ascending=False)
    top3_share_g = aggg.head(3)["r_sum"].sum() / aggg["r_sum"].sum() * 100
    print(f" 고유블록수={len(aggg)} 총 순R={aggg['r_sum'].sum():.2f}  top-3 블록 기여={top3_share_g:.1f}%")
    for k in (1, 3, 5):
        top_ids = set(aggg.head(k)["block"])
        rest = bg[~bg["block"].isin(top_ids)]
        print(f"  top-{k}(최고) 블록 제거 후:", su.print_summary(su.summary(rest, f"excl_top{k}_gross")))
    worstg = aggg.sort_values("r_sum")
    for k in (1, 3, 5):
        worst_ids = set(worstg.head(k)["block"])
        rest = bg[~bg["block"].isin(worst_ids)]
        print(f"  worst-{k}(최악) 블록 제거 후:", su.print_summary(su.summary(rest, f"excl_worst{k}_gross")))
