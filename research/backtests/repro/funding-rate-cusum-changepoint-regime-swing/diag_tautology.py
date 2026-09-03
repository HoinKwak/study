"""동어반복 점검 — CUSUM e(z-score)가 기존 streak 길이·curvature(2차차분) z-score와
같은 정보인지. 전체구간 상관(정렬 후 pairwise)과 '트리거 시점 한정' 상관을 종목별로 각각 본다.
"""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import SYMBOLS
from engine import build_frame
from events import filter_8h


def streak_length(rate: pd.Series) -> pd.Series:
    sign = np.sign(rate)
    # 연속 동일부호 카운트(전 이력 causal — 각 시점까지 몇 회 연속인지)
    grp = (sign != sign.shift(1)).cumsum()
    return sign.groupby(grp).cumcount() + 1


def curvature_z(rate: pd.Series, window: int = 60) -> pd.Series:
    d1 = rate.diff()
    d2 = d1.diff()
    mu = d2.rolling(window).mean()
    sd = d2.rolling(window).std()
    return (d2 - mu) / sd


def main() -> None:
    out = {}
    for sym in SYMBOLS:
        frame = build_frame(sym)
        funding_8h, _ = filter_8h(frame["funding"])
        rate = funding_8h["rate"]
        streak = streak_length(rate)
        curv_z = curvature_z(rate)
        diag = frame["diag"]  # e, s_pos, s_neg (전체 8h 시계열)

        # 전체구간 상관(레벨이 아니라 게이트 변수: e vs streak, e vs curv_z)
        common_idx = diag.index.intersection(streak.index).intersection(curv_z.index)
        full_corr_streak = diag.loc[common_idx, "e"].corr(streak.loc[common_idx])
        full_corr_curv = diag.loc[common_idx, "e"].corr(curv_z.loc[common_idx])

        # 트리거 시점 한정(실제 CUSUM 이벤트가 발화한 시점만)
        ev = frame["events"]
        ev_idx = ev["event_time"]
        ev_idx = ev_idx[ev_idx.isin(common_idx)]
        if len(ev_idx) >= 5:
            e_at_ev = diag.loc[ev_idx, "e"]
            streak_at_ev = streak.loc[ev_idx]
            curv_at_ev = curv_z.loc[ev_idx]
            trig_corr_streak = e_at_ev.corr(streak_at_ev)
            trig_corr_curv = e_at_ev.corr(curv_at_ev)
        else:
            trig_corr_streak = float("nan")
            trig_corr_curv = float("nan")

        out[sym] = {
            "full_corr_e_vs_streak": full_corr_streak,
            "full_corr_e_vs_curvature_z": full_corr_curv,
            "trigger_corr_e_vs_streak": trig_corr_streak,
            "trigger_corr_e_vs_curvature_z": trig_corr_curv,
            "n_events": len(ev_idx),
        }

    with open("out_diag_tautology.json", "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
