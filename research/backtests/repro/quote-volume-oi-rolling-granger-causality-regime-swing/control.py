"""공통 대조군 구성: 게이트없음(순수 EMA20/50 크로스) · 단순 z-score 게이트 · 방향반전."""
from __future__ import annotations

import numpy as np
import pandas as pd

from signals import Signals


def gate_none_entries(sig: Signals) -> pd.DataFrame:
    """게이트없음 대조군: 순수 EMA20/50 골든/데드 크로스(그레인저 레짐 무관)를 트리거로,
    나머지(ret4h 부호·엔트리 타이밍)는 base 와 동일하게 유지."""
    n = len(sig.df)
    idx = sig.df.index
    ef = sig.ema_fast.to_numpy()
    es = sig.ema_slow.to_numpy()
    ret = sig.ret4h.to_numpy()
    atr = sig.atr14.to_numpy()
    prev_below = (ef < es)
    cross_up = (~prev_below) & np.roll(prev_below, 1)
    cross_dn = prev_below & (~np.roll(prev_below, 1))
    cross_up[0] = False
    cross_dn[0] = False

    rows = []
    for i in range(n):
        if cross_up[i]:
            direction = 1
        elif cross_dn[i]:
            direction = -1
        else:
            continue
        r = ret[i]
        if not np.isfinite(r):
            continue
        entry_bar = i + 1
        if entry_bar >= n:
            continue
        atr_v = atr[i]
        if not (np.isfinite(atr_v) and atr_v > 0):
            continue
        rows.append({"signal_bar": i, "signal_time": idx[i], "direction": direction,
                    "entry_bar": entry_bar, "entry_time": idx[entry_bar],
                    "atr_entry": float(atr_v)})
    if not rows:
        return pd.DataFrame(columns=["signal_bar", "signal_time", "direction",
                                      "entry_bar", "entry_time", "atr_entry"])
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)


def zscore_gate_entries(sig: Signals, z_window: int = 60, z_thresh: float = 1.5) -> pd.DataFrame:
    """단순 z-score 게이트 대조군(스카우트 의심점②): 거래대금 성장률(dqv) z-score 가
    임계를 상향 돌파하는 시점을 '거래대금 선행'류 게이트로 대체 사용. 나머지 조건(ret4h 부호·
    EMA20/50 정렬·엔트리 타이밍)은 base 와 완전히 동일하게 유지해 그레인저 레짐과 apples-to-apples
    비교가 되게 한다. causal: z(t) 는 t 시점까지의 트레일링 window 만 사용, shift(1) 로 자기 자신을
    베이스라인에서 제외."""
    n = len(sig.df)
    idx = sig.df.index
    dqv = sig.dqv
    mean = dqv.shift(1).rolling(z_window, min_periods=z_window).mean()
    std = dqv.shift(1).rolling(z_window, min_periods=z_window).std()
    z = ((dqv - mean) / std).to_numpy()
    prev_below = np.where(np.isfinite(z), z < z_thresh, True)
    cross_up = (~prev_below) & np.roll(prev_below, 1)
    cross_up[0] = False

    ret = sig.ret4h.to_numpy()
    ef = sig.ema_fast.to_numpy()
    es = sig.ema_slow.to_numpy()
    atr = sig.atr14.to_numpy()

    rows = []
    for i in range(n):
        if not cross_up[i]:
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
                    "entry_bar": entry_bar, "entry_time": idx[entry_bar],
                    "atr_entry": float(atr_v)})
    if not rows:
        return pd.DataFrame(columns=["signal_bar", "signal_time", "direction",
                                      "entry_bar", "entry_time", "atr_entry"])
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
