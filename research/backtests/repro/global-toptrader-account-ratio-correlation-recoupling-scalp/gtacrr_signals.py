"""[단타] 글로벌 vs 탑트레이더 계정비율 상관 붕괴-재동조 스캘프 — 신호 구성.

스펙 규칙 -> 코드:
- g(t)/top(t): 5분 원본을 1h 종가 시점 값으로 리샘플(짧은 지터는 limit=3(<=15분) ffill로 보정,
  긴 결측(2022년 블랙아웃)은 채우지 않고 NaN 유지 -> 그 구간은 자연스럽게 롤링창이 무효화됨).
- gd/td: 1시간 변화분.
- corr(t): 72시간 롤링 피어슨(gd, td), min_periods=corr_window(전체 윈도 요구, 보수적).
- pctile(t): corr(t)의 최근 720시간 자기분포 내 백분위(rolling().rank(pct=True)*100),
  min_periods=pctile_window(전체 윈도 요구).
- 붕괴 상태: pctile<=breakdown_pctile 이 min_dwell 시간 이상 연속.
- 재동조 트리거: 붕괴 상태에서 pctile>=recouple_pctile 로 처음 복귀하는 시점(상태기계, 1패스).
- 방향: 트리거 시점 top 레벨의 직전 direction_lookback 시간 순변화 부호.
- 15m 확인: 15m EMA20 의 4봉(1h) 슬로프가 방향과 뚜렷이 반대(|slope|>=ema_slope_th)면 스킵.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, "/home/user/study/.claude/worktrees/agent-aa2f5a8cf721d88f6/src")

from crypto_trader.signals import indicators as ind  # noqa: E402

import gtacrr_common as c  # noqa: E402

DEFAULT_PARAMS = dict(
    corr_window=72,
    pctile_window=720,
    breakdown_pctile=10,
    min_dwell=6,
    recouple_pctile=50,
    direction_lookback=6,
    atr_stop_mult=1.3,
    rr_target=1.5,
    max_hold=48,
    invalidation_window=12,
    partial_pctile=80,
    ema_slope_th=0.15,   # %, 4봉(1h) 15m EMA20 슬로프 임계값
    ema_slope_bars=4,
)


def resample_ratio_1h(symbol: str) -> pd.DataFrame:
    """5m 원본 -> 1h 종가시점 리샘플. 지터 보정(limit=3, <=15분)만 적용, 장기 결측은 NaN 유지."""
    raw = c.load_ratio_metrics(symbol)
    raw = raw.ffill(limit=3)
    h = raw.resample("1h").last()
    return h


def _consecutive_run(cond: np.ndarray) -> np.ndarray:
    """cond(bool array)의 각 위치에서 끝나는 연속 True 개수(런랭스). False 는 0."""
    out = np.zeros(len(cond), dtype=np.int64)
    run = 0
    for i, v in enumerate(cond):
        run = run + 1 if v else 0
        out[i] = run
    return out


def _recouple_state_machine(pctile: np.ndarray, dwell: np.ndarray, min_dwell: int,
                             recouple_pctile: float) -> tuple[np.ndarray, np.ndarray]:
    """1패스 상태기계: trigger[t]=재동조 확인 시점(붕괴상태였다가 pctile>=recouple 최초 복귀).

    반환: (trigger bool array, in_breakdown bool array — 진단용, t시점에 붕괴상태였는지)
    """
    n = len(pctile)
    trigger = np.zeros(n, dtype=bool)
    in_bd = np.zeros(n, dtype=bool)
    state = 0  # 0=none, 1=breakdown active(재동조 대기)
    for i in range(n):
        p = pctile[i]
        if np.isnan(p):
            in_bd[i] = (state == 1)
            continue
        if state == 0:
            if dwell[i] >= min_dwell:
                state = 1
        elif state == 1:
            if p >= recouple_pctile:
                trigger[i] = True
                state = 0
        in_bd[i] = (state == 1)
    return trigger, in_bd


def build_signal_frame(symbol: str, params: dict | None = None,
                        require_confirm: bool = True,
                        skip_recouple_check: bool = False) -> pd.DataFrame:
    """1h 인덱스 신호 프레임 구성.

    require_confirm=False 면 15m EMA 확인 필터 미적용(대조군).
    skip_recouple_check=True 면 "재동조 확인" 조건 없이 붕괴 확정 즉시 트리거(대조군 ①).
    """
    p = {**DEFAULT_PARAMS, **(params or {})}
    k1h = c.load_klines(symbol, "1h", c.IS_START, c.OOS_END)
    k15 = c.load_klines(symbol, "15m", c.IS_START, c.OOS_END)
    ratio = resample_ratio_1h(symbol)

    df = k1h.copy()
    df = df.join(ratio, how="left")
    df["atr14"] = ind.atr(df, 14)

    g = df["g_raw"]; top = df["top_raw"]
    gd = g.diff(1)
    td = top.diff(1)
    corr = gd.rolling(p["corr_window"], min_periods=p["corr_window"]).corr(td)
    pctile = corr.rolling(p["pctile_window"], min_periods=p["pctile_window"]).rank(pct=True) * 100.0

    cond = (pctile <= p["breakdown_pctile"]).fillna(False).to_numpy()
    dwell = _consecutive_run(cond)

    if skip_recouple_check:
        # 대조군①: 붕괴 확정(dwell>=min_dwell) 그 즉시 트리거(재동조 대기 없음), 1회성(연속 확정구간 중 첫봉만)
        confirmed = dwell >= p["min_dwell"]
        prev_confirmed = np.r_[False, confirmed[:-1]]
        trigger = confirmed & (~prev_confirmed)
        in_bd = confirmed
    else:
        trigger, in_bd = _recouple_state_machine(pctile.to_numpy(), dwell, p["min_dwell"],
                                                  p["recouple_pctile"])

    df["gd"] = gd; df["td"] = td; df["corr"] = corr; df["pctile"] = pctile
    df["dwell"] = dwell; df["in_breakdown"] = in_bd; df["trigger"] = trigger

    # 방향: 트리거 시점 top 레벨의 직전 direction_lookback 시간 순변화 부호
    lb = p["direction_lookback"]
    top_chg = top - top.shift(lb)
    direction = np.zeros(len(df), dtype=np.int64)
    direction[trigger & (top_chg.to_numpy() > 0)] = 1
    direction[trigger & (top_chg.to_numpy() < 0)] = -1
    # 순변화가 정확히 0 이거나 NaN 이면 방향 미정 -> 신호 무효화(트리거 취소)
    invalid_dir = trigger & (~np.isfinite(top_chg.to_numpy()) | (top_chg.to_numpy() == 0))
    trigger = trigger & (~invalid_dir)
    direction[invalid_dir] = 0
    df["direction_raw"] = direction
    df["trigger"] = trigger

    # 15m 확인: EMA20 슬로프
    ema15 = ind.ema(k15["close"], 20)
    slope15 = (ema15 - ema15.shift(p["ema_slope_bars"])) / ema15.shift(p["ema_slope_bars"]) * 100.0
    slope_1h = slope15.resample("1h").last().reindex(df.index)
    df["slope_1h"] = slope_1h

    final_dir = direction.copy()
    if require_confirm:
        th = p["ema_slope_th"]
        blocked = (trigger & (final_dir == 1) & (slope_1h.to_numpy() < -th)) | \
                  (trigger & (final_dir == -1) & (slope_1h.to_numpy() > th))
        final_dir[blocked] = 0
    df["direction"] = final_dir
    df["signal"] = df["trigger"] & (df["direction"] != 0)
    return df
