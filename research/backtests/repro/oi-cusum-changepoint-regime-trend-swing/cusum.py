"""OI CUSUM 체인지포인트 순차 계산 (상태의존, 벡터화 불가) — 룩어헤드 방지.

스펙 §진입 규칙:
- oi_growth(t) = ln(OI(t)/OI(t-1))
- z(t) = (oi_growth(t) - mean_90d) / std_90d  [90일 롤링, shift(1)로 현재관측치를
  자기 자신의 베이스라인에서 제외 — 이 프로젝트의 기존 CUSUM 계열 스펙(펀딩레이트 CUSUM)의
  확립된 관행을 그대로 따름. 순전히 과거 데이터만 쓰므로 룩어헤드 아님]
- S_pos(t) = max(0, S_pos(t-1) + z(t) - k); S_pos(t) > h 이면 상방 체인지포인트, S_pos 리셋
- S_neg(t) = min(0, S_neg(t-1) + z(t) + k); S_neg(t) < -h 이면 하방 체인지포인트, S_neg 리셋
- z(t) 가 NaN(결측 구간)이면 CUSUM 상태를 리셋하고 스킵(결측 구간 전후 오염 방지, 스펙 명시 요구)
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def rolling_zscore_shift1(x: pd.Series, window_bars: int) -> pd.Series:
    """트레일링 window_bars 개(shift(1) — 현재값 제외) 평균/표준편차로 표준화."""
    mean = x.rolling(window_bars, min_periods=window_bars).mean().shift(1)
    std = x.rolling(window_bars, min_periods=window_bars).std().shift(1)
    z = (x - mean) / std
    return z.replace([np.inf, -np.inf], np.nan)


def compute_cusum(z: pd.Series, k: float, h: float) -> pd.DataFrame:
    """순차(for-loop) CUSUM. 반환: s_pos, s_neg, cp_up(bool), cp_down(bool) — 인덱스는 z와 동일.

    각 시각 t 의 s_pos/s_neg/cp_up/cp_down 은 오직 t 및 그 이전 관측치(z(<=t))로만 결정된다
    (다음 값을 보지 않음 — 룩어헤드 없음). z(t) 가 NaN 이면(결측 구간) 상태를 0 으로 리셋하고
    그 봉은 체인지포인트 후보에서 제외한다(스펙: "결측 구간 전후로 CUSUM 을 리셋").
    """
    n = len(z)
    zv = z.to_numpy(dtype=float)
    s_pos = np.zeros(n)
    s_neg = np.zeros(n)
    s_pos_pre = np.zeros(n)  # 리셋 적용 전 값(진단용 — 트리거 시점 강도 상관 계산에 사용)
    s_neg_pre = np.zeros(n)
    cp_up = np.zeros(n, dtype=bool)
    cp_down = np.zeros(n, dtype=bool)
    prev_pos = 0.0
    prev_neg = 0.0
    for i in range(n):
        zi = zv[i]
        if not np.isfinite(zi):
            prev_pos = 0.0
            prev_neg = 0.0
            s_pos[i] = 0.0
            s_neg[i] = 0.0
            s_pos_pre[i] = 0.0
            s_neg_pre[i] = 0.0
            continue
        cur_pos = max(0.0, prev_pos + zi - k)
        cur_neg = min(0.0, prev_neg + zi + k)
        s_pos_pre[i] = cur_pos
        s_neg_pre[i] = cur_neg
        if cur_pos > h:
            cp_up[i] = True
            cur_pos = 0.0
        if cur_neg < -h:
            cp_down[i] = True
            cur_neg = 0.0
        s_pos[i] = cur_pos
        s_neg[i] = cur_neg
        prev_pos = cur_pos
        prev_neg = cur_neg
    return pd.DataFrame(
        {"s_pos": s_pos, "s_neg": s_neg, "s_pos_pre": s_pos_pre, "s_neg_pre": s_neg_pre,
         "cp_up": cp_up, "cp_down": cp_down}, index=z.index)


def build_oi_cusum(oi: pd.Series, z_window_days: int = 90, k: float = 0.5, h: float = 5.0
                    ) -> pd.DataFrame:
    """oi(4h 인덱스, sum_open_interest 값)로부터 oi_growth, z, CUSUM 상태·체인지포인트 계산.
    4h 봉 = 하루 6개이므로 z_window_bars = z_window_days * 6."""
    oi_growth = np.log(oi / oi.shift(1))
    oi_growth = oi_growth.replace([np.inf, -np.inf], np.nan)
    z_window_bars = z_window_days * 6
    z = rolling_zscore_shift1(oi_growth, z_window_bars)
    cusum = compute_cusum(z, k, h)
    out = cusum.copy()
    out["oi_growth"] = oi_growth
    out["z"] = z
    return out
