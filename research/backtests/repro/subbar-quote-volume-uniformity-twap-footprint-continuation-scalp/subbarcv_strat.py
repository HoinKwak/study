"""오케스트레이션 — 7종목 로드+캐시, 파라미터별 전체 실행, PF/t-stat 유틸."""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from subbarcv_common import SYMBOLS, load_klines_qv, load_klines  # noqa: E402
from subbarcv_signals import compute_signal_frame, donchian_breakout_frame  # noqa: E402
from subbarcv_engine import simulate_symbol, simulate_donchian, trades_to_df, ROUNDTRIP_COST  # noqa: E402

# 데이터는 IS_START 보다 65일 앞서 받아 60일 롤링 백분위 창을 IS 시작부터 최대한
# 채운다(웜업). IS_START/OOS_END 는 트레이드 판정(진입시각) 경계로만 쓰고, 데이터
# 로드 범위(DATA_START)와는 구분한다.
IS_START = "2022-01-01"
IS_END = "2024-06-30 23:59:59"
OOS_START = "2024-07-01"
OOS_END = "2026-06-30 23:59:59"
DATA_START = "2021-11-01"

IS_START_TS = pd.Timestamp(IS_START)
IS_END_TS = pd.Timestamp(IS_END)
OOS_START_TS = pd.Timestamp(OOS_START)
OOS_END_TS = pd.Timestamp(OOS_END)

WARMUP_HOURS = 1500  # 엔진 warmup_bars(hourly) 기본값과 일치


@lru_cache(maxsize=None)
def _raw5(symbol: str) -> pd.DataFrame:
    return load_klines_qv(symbol, "5m", DATA_START, OOS_END)


@lru_cache(maxsize=None)
def _raw15(symbol: str) -> pd.DataFrame:
    return load_klines(symbol, "15m", DATA_START, OOS_END)


def pf(returns) -> float:
    r = np.asarray(returns, dtype=float)
    r = r[~np.isnan(r)]
    pos = r[r > 0].sum()
    neg = -r[r < 0].sum()
    if neg <= 0:
        return float("inf") if pos > 0 else float("nan")
    return float(pos / neg)


def tstat(returns) -> float:
    r = np.asarray(returns, dtype=float)
    r = r[~np.isnan(r)]
    n = len(r)
    if n < 2:
        return float("nan")
    sd = r.std(ddof=1)
    if sd == 0:
        return float("nan")
    return float(r.mean() / (sd / np.sqrt(n)))


def run_symbol(symbol: str, pctile_cv_th: float = 30.0, consist_th_num: int = 8,
               consist_th_den: int = 12, range_atr_th: float = 0.5,
               trail_mult: float = 1.5, sl_atr_mult: float = 1.2,
               max_hold_hours: int = 8, mode: str = "base",
               shuffle_seed: int | None = None, fee0: bool = False,
               warmup_hours: int = WARMUP_HOURS) -> pd.DataFrame:
    """mode: base | reverse | donchian | cv_shuffle"""
    df5 = _raw5(symbol)
    df15 = _raw15(symbol)

    if mode == "donchian":
        trades = simulate_donchian(df15, symbol, trail_mult=trail_mult,
                                    sl_atr_mult=sl_atr_mult, max_hold_hours=max_hold_hours,
                                    warmup_bars=warmup_hours * 4)
        tdf = trades_to_df(trades)
        if fee0 and len(tdf):
            tdf["net_ret"] = tdf["raw_ret"]
            tdf["r_net"] = tdf["r_gross"]
        return tdf

    cv_override = None
    if mode == "cv_shuffle":
        from subbarcv_signals import build_hourly_from_5m
        hourly_raw = build_hourly_from_5m(df5)
        rng = np.random.default_rng(shuffle_seed)
        vals = hourly_raw["cv"].to_numpy(float).copy()
        mask = ~np.isnan(vals)
        perm_vals = vals.copy()
        idxs = np.where(mask)[0]
        shuffled = rng.permutation(vals[mask])
        perm_vals[idxs] = shuffled
        cv_override = pd.Series(perm_vals, index=hourly_raw.index)

    hourly = compute_signal_frame(df5, pctile_cv_th=pctile_cv_th,
                                   consist_th_num=consist_th_num,
                                   consist_th_den=consist_th_den,
                                   range_atr_th=range_atr_th, cv_override=cv_override)
    reverse = mode == "reverse"
    trades = simulate_symbol(hourly, df15, symbol, trail_mult=trail_mult,
                              sl_atr_mult=sl_atr_mult, max_hold_hours=max_hold_hours,
                              reverse=reverse, warmup_bars=warmup_hours)
    tdf = trades_to_df(trades)
    if fee0 and len(tdf):
        tdf["net_ret"] = tdf["raw_ret"]
        tdf["r_net"] = tdf["r_gross"]
    return tdf


def run_all(symbols=SYMBOLS, **kwargs) -> pd.DataFrame:
    frames = [run_symbol(s, **kwargs) for s in symbols]
    frames = [f for f in frames if len(f)]
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def split(trades: pd.DataFrame):
    if len(trades) == 0:
        return trades, trades, trades
    is_ = trades[(trades["entry_time"] >= IS_START_TS) & (trades["entry_time"] <= IS_END_TS)]
    oos = trades[(trades["entry_time"] >= OOS_START_TS) & (trades["entry_time"] <= OOS_END_TS)]
    full = trades[(trades["entry_time"] >= IS_START_TS) & (trades["entry_time"] <= OOS_END_TS)]
    return is_, oos, full


def summarize(df: pd.DataFrame, label: str) -> dict:
    if len(df) == 0:
        return dict(label=label, n=0, pf_gross=np.nan, pf_net=np.nan, pf_r_gross=np.nan,
                    pf_r_net=np.nan, r_net_mean=np.nan, t_r_net=np.nan, win_rate=np.nan)
    return dict(
        label=label, n=len(df),
        pf_gross=pf(df["raw_ret"]), pf_net=pf(df["net_ret"]),
        pf_r_gross=pf(df["r_gross"]), pf_r_net=pf(df["r_net"]),
        r_net_mean=df["r_net"].mean(), t_r_net=tstat(df["r_net"]),
        win_rate=(df["net_ret"] > 0).mean(),
    )
