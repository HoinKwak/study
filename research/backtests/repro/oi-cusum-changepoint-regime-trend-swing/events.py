"""이벤트 검출: (1) 원시 OI CUSUM 체인지포인트(방향 무관, 반대체인지포인트 무효화·상관 진단용)
(2) EMA20/50 확인 게이트를 통과한 진입 후보(confirm_bars 이내).

⚠️ 타이밍: cp_bar(=i) 는 그 4h 봉이 마감되는 순간(=봉 i+1 의 시가 시각) 확정된다(oi_4h_from_5m
가 구간 마지막 관측치를 쓰므로). EMA_fast/slow(i) 도 봉 i 의 종가 기준이라 같은 시각에 확정.
따라서 "봉 i 에서 조건 성립 -> 봉 i+1 시가 진입"은 지연 없이 가능하고 룩어헤드가 아니다
(결정에 쓰는 모든 정보가 진입 시각 이전에 이미 확정돼 있음).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from signals import Signals


def raw_cp_events(sig: Signals) -> pd.DataFrame:
    """방향 무관 원시 체인지포인트 목록(무효화·상관 진단용). cp_bar 는 정수 위치 인덱스."""
    n = len(sig.df)
    idx = sig.df.index
    rows = []
    cp_up = sig.cp_up.to_numpy()
    cp_down = sig.cp_down.to_numpy()
    for i in range(n):
        if cp_up[i]:
            rows.append({"cp_bar": i, "cp_time": idx[i], "cp_type": "up"})
        if cp_down[i]:
            rows.append({"cp_bar": i, "cp_time": idx[i], "cp_type": "down"})
    if not rows:
        return pd.DataFrame(columns=["cp_bar", "cp_time", "cp_type"])
    return pd.DataFrame(rows).sort_values("cp_time").reset_index(drop=True)


def gated_entries(sig: Signals, confirm_bars: int = 2) -> pd.DataFrame:
    """cp 발생 후 confirm_bars 봉 이내 EMA20 vs EMA50 방향 일치 확인 -> 진입 후보.

    cp_type=='up' 은 EMA_fast>EMA_slow, cp_type=='down' 은 EMA_fast<EMA_slow 를 확인 조건으로
    쓴다(스펙 문언 그대로 — 최종 매매방향 배정은 diag_direction.py 실측 이후 별도 결정).
    confirm_bars 윈도우 내에서 조건이 처음 성립하는 봉에서 즉시 체결(그 다음 봉 시가).
    """
    n = len(sig.df)
    idx = sig.df.index
    ema_fast = sig.ema_fast.to_numpy()
    ema_slow = sig.ema_slow.to_numpy()
    atr = sig.atr14.to_numpy()
    cp_up = sig.cp_up.to_numpy()
    cp_down = sig.cp_down.to_numpy()

    rows = []
    for i in range(n):
        for cp_type, up_flag in (("up", True), ("down", False)):
            flag_arr = cp_up if up_flag else cp_down
            if not flag_arr[i]:
                continue
            for off in range(confirm_bars):
                j = i + off
                if j >= n:
                    break
                ef, es = ema_fast[j], ema_slow[j]
                if not (np.isfinite(ef) and np.isfinite(es)):
                    continue
                cond = (ef > es) if up_flag else (ef < es)
                if cond:
                    entry_bar = j + 1
                    if entry_bar >= n:
                        break
                    atr_v = atr[j]
                    if not (np.isfinite(atr_v) and atr_v > 0):
                        break
                    rows.append({
                        "cp_bar": i, "cp_time": idx[i], "cp_type": cp_type,
                        "confirm_bar": j, "confirm_time": idx[j],
                        "entry_bar": entry_bar, "entry_time": idx[entry_bar],
                        "atr_entry": float(atr_v),
                    })
                    break
    if not rows:
        return pd.DataFrame(columns=["cp_bar", "cp_time", "cp_type", "confirm_bar",
                                      "confirm_time", "entry_bar", "entry_time", "atr_entry"])
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
