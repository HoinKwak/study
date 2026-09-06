"""§동어반복(재포장) 점검 — 전체구간 + 트리거시점 한정 모두.
① OI CUSUM vs 가격 CUSUM(기존 스펙) — 발생시각 ±1봉 이내 동시발생 비율(사전 폐기조건 (b)).
② OI CUSUM 강도(연속형 대리치 max(S_pos,-S_neg))와 OI 변화 stdev·ROC·|z| 상관(전체구간·트리거시점).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from signals import build_signals
from events import raw_cp_events
from control import price_cusum
from common import IS_START, OOS_END


def overlap_rate(cp_a: pd.DataFrame, cp_b: pd.DataFrame, tol_bars: int = 1) -> dict:
    """cp_a 각 이벤트가 cp_b 이벤트와 ±tol_bars 4h봉 이내(같은 방향 무관, cp_type 도 비교)에
    존재하는 비율. 방향(cp_type) 일치까지 요구하는 엄격판과, 방향 무관 완화판 둘 다 계산."""
    if len(cp_a) == 0:
        return {"n_a": 0, "strict_overlap": float("nan"), "loose_overlap": float("nan")}
    tol = pd.Timedelta(hours=4 * tol_bars)
    b_times_by_type = {t: pd.DatetimeIndex(cp_b[cp_b["cp_type"] == t]["cp_time"])
                       for t in ["up", "down"]}
    b_times_all = pd.DatetimeIndex(cp_b["cp_time"])
    strict_hits = 0
    loose_hits = 0
    for _, r in cp_a.iterrows():
        t = r["cp_time"]
        same_type = b_times_by_type[r["cp_type"]]
        if len(same_type):
            diffs = np.abs(same_type - t)
            if (diffs <= tol).any():
                strict_hits += 1
        if len(b_times_all):
            diffs_all = np.abs(b_times_all - t)
            if (diffs_all <= tol).any():
                loose_hits += 1
    return {"n_a": len(cp_a), "strict_overlap": strict_hits / len(cp_a),
            "loose_overlap": loose_hits / len(cp_a)}


def main():
    sig = build_signals("BTCUSDT")
    oi_cp = raw_cp_events(sig)
    px_cp = price_cusum(sig)

    ov = overlap_rate(oi_cp, px_cp, tol_bars=1)
    print("① OI CUSUM(n=%d) vs 가격 CUSUM(n=%d) ±1봉 동시발생:" % (len(oi_cp), len(px_cp)))
    print("   방향일치(strict):", ov["strict_overlap"], " 방향무관(loose):", ov["loose_overlap"])

    # 중복 제거 후 잔여표본 독립 유의성(폐기조건 (b) 후반부: "중복 제거 후 잔여 표본으로도
    # 독립적 유의성이 없으면" — 잔여표본 자체가 거의 남지 않을 것으로 예상, 실측 확인)
    tol = pd.Timedelta(hours=4)
    px_times_by_type = {t: pd.DatetimeIndex(px_cp[px_cp["cp_type"] == t]["cp_time"])
                        for t in ["up", "down"]}
    overlap_mask = []
    for _, r in oi_cp.iterrows():
        same_type = px_times_by_type[r["cp_type"]]
        hit = len(same_type) and (np.abs(same_type - r["cp_time"]) <= tol).any()
        overlap_mask.append(bool(hit))
    oi_cp = oi_cp.copy()
    oi_cp["overlaps_price_cusum"] = overlap_mask
    residual = oi_cp[~oi_cp["overlaps_price_cusum"]]
    print("   잔여(비중첩) OI CUSUM 이벤트 수:", len(residual), "/", len(oi_cp))
    oi_cp.to_csv("out_diag_tautology_overlap.csv", index=False)

    # ② 연속형 강도 vs 파생 지표(전체구간 + 트리거시점)
    df = sig.df
    oi_growth = sig.oi_growth
    # 트리거 봉 자신은 리셋(0) 이후 값이라 강도 상관에 무의미 -> 리셋 전(pre) 값 사용
    strength = pd.concat([sig.s_pos_pre, -sig.s_neg_pre], axis=1).max(axis=1)
    abs_z = sig.z.abs()
    roll_std20 = oi_growth.rolling(20).std()
    roc12 = sig.oi.pct_change(12)
    trig_mask = (sig.cp_up | sig.cp_down)

    feats = pd.DataFrame({"strength": strength, "abs_z": abs_z, "roll_std20": roll_std20,
                          "roc12": roc12}).dropna()
    corr_full = feats.corr()["strength"].drop("strength")
    trig_feats = feats.loc[feats.index.intersection(sig.df.index[trig_mask.to_numpy()])]
    corr_trig = trig_feats.corr()["strength"].drop("strength") if len(trig_feats) > 3 else None

    print("\n② 전체구간 상관(strength vs 파생지표):")
    print(corr_full.to_string())
    print("\n② 트리거시점(n=%d) 상관:" % len(trig_feats))
    print(corr_trig.to_string() if corr_trig is not None else "표본부족")

    out = {"overlap": ov, "n_residual_after_price_cusum_dedup": int(len(residual)),
          "corr_full": corr_full.to_dict(),
          "corr_trigger": corr_trig.to_dict() if corr_trig is not None else None,
          "n_trigger": int(len(trig_feats))}
    import json
    with open("out_diag_tautology.json", "w") as f:
        json.dump(out, f, indent=2, default=str)


if __name__ == "__main__":
    main()
