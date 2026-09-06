"""핵심 대조군 4종 구현.
① 게이트없음(gate_none): CUSUM 없이 순수 BTC EMA20/50 신규 크로스 -> 추세추종.
② OI 단순 z-score 스파이크 게이트(oi_zspike): 누적(CUSUM) 대신 순간 z(t) 임계 돌파를 체인지포인트로.
③ 가격 CUSUM(price_cusum): 동일 알고리즘을 OI growth 대신 4h 로그수익률에 적용.
④ 반전(reverse): engine.simulate_trades(reverse=True) — 별도 함수 불필요, 기존 파라미터로 처리.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from signals import Signals, build_signals
from cusum import rolling_zscore_shift1, compute_cusum
from events import raw_cp_events


def gate_none_entries(sig: Signals) -> pd.DataFrame:
    """CUSUM 없이 순수 EMA20/50 신규 크로스(직전 봉 대비 부호 변화) -> 다음 봉 시가 진입."""
    ema_fast = sig.ema_fast.to_numpy()
    ema_slow = sig.ema_slow.to_numpy()
    atr = sig.atr14.to_numpy()
    idx = sig.df.index
    n = len(sig.df)
    rows = []
    prev_sign = None
    for i in range(n):
        ef, es = ema_fast[i], ema_slow[i]
        if not (np.isfinite(ef) and np.isfinite(es)):
            continue
        sign = 1 if ef > es else (-1 if ef < es else 0)
        if sign == 0:
            continue
        if prev_sign is not None and sign != prev_sign:
            cp_type = "up" if sign == 1 else "down"
            entry_bar = i + 1
            if entry_bar < n and np.isfinite(atr[i]) and atr[i] > 0:
                rows.append({"cp_bar": i, "cp_time": idx[i], "cp_type": cp_type,
                            "confirm_bar": i, "confirm_time": idx[i],
                            "entry_bar": entry_bar, "entry_time": idx[entry_bar],
                            "atr_entry": float(atr[i])})
        prev_sign = sign
    if not rows:
        return pd.DataFrame(columns=["cp_bar", "cp_time", "cp_type", "confirm_bar",
                                      "confirm_time", "entry_bar", "entry_time", "atr_entry"])
    return pd.DataFrame(rows)


def oi_zspike_signals(sig: Signals, z_thresh: float = 2.0) -> tuple[pd.Series, pd.Series]:
    """CUSUM 누적 대신 순간 z(t) 임계 돌파. cp_up=z>=thresh, cp_down=z<=-thresh (리셋 개념 없음
    — 매 봉 독립 판정, 연속 돌파 시 매 봉 이벤트가 될 수 있어 §첫돌파만 취급으로 후처리)."""
    z = sig.z
    up = (z >= z_thresh)
    down = (z <= -z_thresh)
    # 연속 돌파 구간의 "첫 봉"만 이벤트로 인정(CUSUM 의 1회성 리셋과 비교 공정성)
    up_first = up & ~up.shift(1, fill_value=False)
    down_first = down & ~down.shift(1, fill_value=False)
    return up_first, down_first


def build_oi_zspike_entries(sig: Signals, z_thresh: float = 2.0, confirm_bars: int = 2
                             ) -> pd.DataFrame:
    up_first, down_first = oi_zspike_signals(sig, z_thresh)
    n = len(sig.df)
    idx = sig.df.index
    ema_fast = sig.ema_fast.to_numpy()
    ema_slow = sig.ema_slow.to_numpy()
    atr = sig.atr14.to_numpy()
    up_arr = up_first.to_numpy()
    down_arr = down_first.to_numpy()
    rows = []
    for i in range(n):
        for cp_type, up_flag in (("up", True), ("down", False)):
            flag_arr = up_arr if up_flag else down_arr
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
                    if entry_bar >= n or not (np.isfinite(atr[j]) and atr[j] > 0):
                        break
                    rows.append({"cp_bar": i, "cp_time": idx[i], "cp_type": cp_type,
                                "confirm_bar": j, "confirm_time": idx[j],
                                "entry_bar": entry_bar, "entry_time": idx[entry_bar],
                                "atr_entry": float(atr[j])})
                    break
    if not rows:
        return pd.DataFrame(columns=["cp_bar", "cp_time", "cp_type", "confirm_bar",
                                      "confirm_time", "entry_bar", "entry_time", "atr_entry"])
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)


def price_cusum(sig: Signals, z_window_days: int = 90, k: float = 0.5, h: float = 5.0
                ) -> pd.DataFrame:
    """가격 로그수익률에 동일 CUSUM 알고리즘 적용(4h). 반환: raw_cp 형식(cp_bar,cp_time,cp_type)."""
    logret = np.log(sig.df["close"] / sig.df["close"].shift(1))
    z_window_bars = z_window_days * 6
    z = rolling_zscore_shift1(logret, z_window_bars)
    cusum = compute_cusum(z, k, h)
    idx = sig.df.index
    rows = []
    cp_up = cusum["cp_up"].to_numpy()
    cp_down = cusum["cp_down"].to_numpy()
    for i in range(len(idx)):
        if cp_up[i]:
            rows.append({"cp_bar": i, "cp_time": idx[i], "cp_type": "up"})
        if cp_down[i]:
            rows.append({"cp_bar": i, "cp_time": idx[i], "cp_type": "down"})
    if not rows:
        return pd.DataFrame(columns=["cp_bar", "cp_time", "cp_type"])
    return pd.DataFrame(rows).sort_values("cp_time").reset_index(drop=True)


def price_cusum_entries(sig: Signals, price_cp: pd.DataFrame, confirm_bars: int = 2
                        ) -> pd.DataFrame:
    """가격 CUSUM 이벤트에 동일 EMA 확인 게이트 적용(③ 우열비교용 — OI CUSUM 대신 가격 CUSUM
    을 신호원으로 쓴 완전 대응 대조군)."""
    n = len(sig.df)
    idx = sig.df.index
    ema_fast = sig.ema_fast.to_numpy()
    ema_slow = sig.ema_slow.to_numpy()
    atr = sig.atr14.to_numpy()
    cp_by_bar = {}
    for _, r in price_cp.iterrows():
        cp_by_bar.setdefault(int(r["cp_bar"]), []).append(r["cp_type"])
    rows = []
    for i, types in cp_by_bar.items():
        for cp_type in types:
            up_flag = cp_type == "up"
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
                    if entry_bar >= n or not (np.isfinite(atr[j]) and atr[j] > 0):
                        break
                    rows.append({"cp_bar": i, "cp_time": idx[i], "cp_type": cp_type,
                                "confirm_bar": j, "confirm_time": idx[j],
                                "entry_bar": entry_bar, "entry_time": idx[entry_bar],
                                "atr_entry": float(atr[j])})
                    break
    if not rows:
        return pd.DataFrame(columns=["cp_bar", "cp_time", "cp_type", "confirm_bar",
                                      "confirm_time", "entry_bar", "entry_time", "atr_entry"])
    return pd.DataFrame(rows).sort_values("entry_time").reset_index(drop=True)
