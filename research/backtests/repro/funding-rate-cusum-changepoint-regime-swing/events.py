"""CUSUM 체인지포인트 이벤트 생성 — 펀딩레이트 표준화 잔차의 양방향 CUSUM.

- baseline_window(기본 60정산)는 "정산 횟수" 기준(스펙 원문). funding_interval_hours!=8 인
  구간(SOL 등 일부 종목의 과거 2h/4h 펀딩주기 예외, 스펙이 사전 경고)은 필터링해 제외하고
  8h 정산만의 연속열로 CUSUM을 돈다 — 제외 비율은 diag_freq.py 에서 별도 실측.
- 룩어헤드 방지: mu_60/sigma_60 은 shift(1) 로 "현재 프린트 이전 60개"만 사용(현재 관측치
  x_t 를 자기 자신의 베이스라인에 넣지 않음 — 표준 체인지포인트 관행과도 일치).
- e_t, S_pos_t, S_neg_t 는 calc_time(=x_t 발표 시각) 시점에 전부 확정 가능(causal).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def filter_8h(funding: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    n0 = len(funding)
    f8 = funding[funding["interval_hours"] == 8].copy()
    excluded_frac = 1.0 - (len(f8) / n0 if n0 else 0.0)
    return f8, excluded_frac


def detect_events(funding_8h: pd.DataFrame, baseline_window: int = 60, k: float = 0.5,
                   h: float = 4.0) -> tuple[pd.DataFrame, pd.DataFrame]:
    """리셋을 포함한 순차 CUSUM 수행 + 이벤트 목록 반환.

    반환: (events_df[event_time, direction, e, s_val], diag_df[전체 시계열 s_pos/s_neg/e])
    """
    x = funding_8h["rate"]
    mu = x.rolling(baseline_window).mean().shift(1)
    sigma = x.rolling(baseline_window).std().shift(1)
    e = (x - mu) / sigma
    e = e.replace([np.inf, -np.inf], np.nan)

    idx = x.index
    ev = e.to_numpy()
    n = len(ev)
    s_pos_arr = np.zeros(n)
    s_neg_arr = np.zeros(n)
    events = []
    sp = 0.0
    sn = 0.0
    for i in range(n):
        ei = ev[i]
        if np.isnan(ei):
            s_pos_arr[i] = sp
            s_neg_arr[i] = sn
            continue
        sp = max(0.0, sp + ei - k)
        sn = min(0.0, sn + ei + k)
        fired = False
        if sp >= h:
            events.append({"event_time": idx[i], "direction": 1, "e": ei, "s_val": sp})
            sp = 0.0
            fired = True
        if sn <= -h:
            events.append({"event_time": idx[i], "direction": -1, "e": ei, "s_val": sn})
            sn = 0.0
            fired = True
        s_pos_arr[i] = sp
        s_neg_arr[i] = sn
    events_df = pd.DataFrame(events)
    if len(events_df):
        events_df = events_df.sort_values("event_time").reset_index(drop=True)
    diag_df = pd.DataFrame({"e": e, "s_pos": s_pos_arr, "s_neg": s_neg_arr}, index=idx)
    return events_df, diag_df
