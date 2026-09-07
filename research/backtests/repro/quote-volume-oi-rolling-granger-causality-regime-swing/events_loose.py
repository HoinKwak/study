"""보조 진단 전용: '완화된' 레짐전환 정의 — 직전 봉 대비 엄격한 전환(oi_lead -> 즉시 qv_lead)
대신, qv_lead 국면의 첫 봉 이전 lookback 봉 이내에 oi_lead 가 한 번이라도 있었으면 전환으로
인정한다('none' 완충구간을 넘나드는 것을 허용). 롤링 그레인저 p-value 가 매 봉 1칸씩만 창을
이동하며 연속적으로 변하는 구조상, 두 유의성 문턱(0.05/0.10) 사이의 완충지대를 그냥 지나치는
경우가 대부분이라(실측: 직접전환 0건에 가까움) 이 정의는 "OI선행이 먼저이고 그 뒤 거래대금선행이
온다"는 스펙의 핵심 아이디어(인과 방향의 선후관계)는 보존하면서 표본을 확보하기 위한 **사후
로버스트니스 체크**다(1차 판정은 여전히 스펙 문언 그대로의 엄격한 정의로 내린다).

⚠️ 룩어헤드 없음: qv_lead 국면 첫 봉 t 확정 시점에서 t 이전(t-1..t-lookback)의 과거 regime 만
참조하므로 causal.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from signals import Signals


def loose_gated_entries(sig: Signals, lookback: int = 3) -> pd.DataFrame:
    n = len(sig.df)
    idx = sig.df.index
    regime = sig.regime.to_numpy()
    ret = sig.ret4h.to_numpy()
    ef = sig.ema_fast.to_numpy()
    es = sig.ema_slow.to_numpy()
    atr = sig.atr14.to_numpy()

    is_qv = (regime == "qv_lead")
    first_qv = is_qv & ~np.concatenate([[False], is_qv[:-1]])  # qv_lead 국면 첫 봉

    rows = []
    for i in range(n):
        if not first_qv[i]:
            continue
        lo = max(0, i - lookback)
        recent = regime[lo:i]  # t-lookback .. t-1
        if not np.any(recent == "oi_lead"):
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
        rows.append({"signal_bar": i, "signal_time": idx[i], "direction": direction,
                    "entry_bar": entry_bar, "entry_time": idx[entry_bar], "atr_entry": float(atr_v)})
    if not rows:
        return pd.DataFrame(columns=["signal_bar", "signal_time", "direction",
                                      "entry_bar", "entry_time", "atr_entry"])
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
