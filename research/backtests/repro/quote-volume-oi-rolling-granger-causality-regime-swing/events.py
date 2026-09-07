"""진입 이벤트 검출: OI선행→거래대금선행 레짐전환 + 종가수익률 부호 + EMA20/50 정렬.

⚠️ 타이밍: transition_qv[t] 는 봉 t 의 종가로 확정된 regime[t](그 자체가 doi[t]/dqv[t] 를 포함하는
롤링 그레인저 결과, causal)와 regime[t-1] 을 비교해 정해지므로 봉 t 의 종가 시점에 확정된다.
ret4h[t]·ema_fast[t]/ema_slow[t] 도 봉 t 종가 기준이라 같은 시각에 확정된다. 따라서
"봉 t 에서 조건 성립 -> 봉 t+1 시가 진입"은 지연 없이 가능하고 룩어헤드가 아니다.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from signals import Signals


def gated_entries(sig: Signals) -> pd.DataFrame:
    """전환 봉에서 즉시(같은 봉) 방향 조건 확인 -> 다음 봉 시가 진입."""
    n = len(sig.df)
    idx = sig.df.index
    trans = sig.transition_qv.to_numpy()
    ret = sig.ret4h.to_numpy()
    ef = sig.ema_fast.to_numpy()
    es = sig.ema_slow.to_numpy()
    atr = sig.atr14.to_numpy()

    rows = []
    for i in range(n):
        if not trans[i]:
            continue
        r, f, s = ret[i], ef[i], es[i]
        if not (np.isfinite(r) and np.isfinite(f) and np.isfinite(s)):
            continue
        if r > 0 and f > s:
            direction = 1
        elif r < 0 and f < s:
            direction = -1
        else:
            continue
        entry_bar = i + 1
        if entry_bar >= n:
            continue
        atr_v = atr[i]
        if not (np.isfinite(atr_v) and atr_v > 0):
            continue
        rows.append({
            "signal_bar": i, "signal_time": idx[i], "direction": direction,
            "entry_bar": entry_bar, "entry_time": idx[entry_bar], "atr_entry": float(atr_v),
        })
    if not rows:
        return pd.DataFrame(columns=["signal_bar", "signal_time", "direction",
                                      "entry_bar", "entry_time", "atr_entry"])
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
