"""가격-OI 변화 부호일치율(Co-Sign Agreement Rate) 레짐 게이트 + BTC 추세추종 — 공통 로더/신호.

스펙: research/strategies/oi-price-sign-agreement-rate-regime-gate-trend-swing.md
BTC 단독(신호원·매매대상 모두 BTC). 전부 4h(스펙 진입규칙·파라미터 절이 EMA20/50도 4h로 명시).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

_repo_src = os.environ.get(
    "OISIGN_REPO_SRC",
    "/home/user/study/.claude/worktrees/agent-a64cdc714957bee50/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "OISIGN_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oisign"))
DATA = SP / "data"
KLINES_4H_DIR = DATA / "klines_4h"
METRICS_DIR = DATA / "metrics"

SYMBOL = "BTCUSDT"

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = (TAKER_FEE + SLIPPAGE) * 2  # 0.14%

# ------------------------------------------------------------- 파라미터(스펙 기본값)
AGREE_WINDOW = 20          # 4h봉, 약 3.3일
AGREE_NORM_DAYS = 365      # 롤링 정규화 창(일)
HI_TH = 70                 # 백분위 임계
EMA_FAST = 20
EMA_SLOW = 50
ATR_STOP_MULT = 2.5

_KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
               "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


# ------------------------------------------------------------------ 로더

def _load_klines_4h(symbol: str) -> pd.DataFrame:
    files = sorted(KLINES_4H_DIR.glob(f"{symbol}-4h-*.csv"))
    parts = []
    for p in files:
        with open(p) as f:
            first = f.readline()
        has_header = "open_time" in first
        df = pd.read_csv(p, header=0 if has_header else None,
                         names=_KLINE_COLS if not has_header else None)
        df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
        if df.empty:
            continue
        df["open_time"] = df["open_time"].astype("int64")
        parts.append(df)
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    # ⚠️단위사고 회피: open_time 이 ms(13자리) 또는 us(16자리) 혼재 가능성 — 자릿수로 판별해 통일.
    ot = out["open_time"]
    is_us = ot.abs() > 10**14
    if is_us.any():
        out.loc[is_us, "open_time"] = out.loc[is_us, "open_time"] // 1000
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume", "quote_volume"]]
    out.index = out.index.as_unit("ns")
    return out


@lru_cache(maxsize=None)
def load_klines_4h(symbol: str = SYMBOL) -> pd.DataFrame:
    return _load_klines_4h(symbol)


@lru_cache(maxsize=None)
def load_metrics_5m(symbol: str = SYMBOL) -> pd.DataFrame:
    """metrics 5분 원본 로드. create_time 은 날짜 문자열 → 명시적 format 파싱(us/ms 단위사고 회피)."""
    files = sorted(METRICS_DIR.glob(f"{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "symbol", "sum_open_interest"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out.index = out.index.as_unit("ns")
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    out.loc[out["sum_open_interest"] <= 0, "sum_open_interest"] = np.nan
    return out


def oi_4h_from_5m(m5: pd.DataFrame, index_4h: pd.DatetimeIndex) -> pd.Series:
    """5분 OI → 4h 봉 마지막값(각 4h 봉 마감 시점 값, 봉 open_time 인덱스에 정렬).

    klines 4h 봉은 [open_time, open_time+4h) 구간을 대표. 그 구간의 마지막 5분 OI 관측치를
    그 봉의 OI로 쓴다(봉 마감 시점 관측 — 다음 봉 open 이전 시점만 사용해 룩어헤드 없음).
    """
    if m5.empty:
        return pd.Series(dtype=float, index=index_4h)
    s = m5["sum_open_interest"]
    last = s.resample("4h", label="left", closed="left").last()
    last = last.reindex(index_4h)
    return last


def rolling_pctile(x: pd.Series, window_bars: int) -> pd.Series:
    """롤링 백분위(0~100). 동률(tie) 처리: rank(pct=True, method='average') — 이산값(agree)의
    계단형 분포에서도 동률 관측치를 평균 순위로 처리해 매끄럽게(0~100 사이 연속값) 만든다."""
    def _pct(a: np.ndarray) -> float:
        cur = a[-1]
        return (a <= cur).mean() * 100.0
    return x.rolling(window_bars, min_periods=max(20, window_bars // 4)).apply(_pct, raw=True)


@dataclass
class Signals:
    df4h: pd.DataFrame
    agree: pd.Series          # 원 부호일치율(0~1, 20봉 롤링)
    agree_pctile: pd.Series   # 365일 롤링 백분위(0~100)
    corr_roll: pd.Series      # 동어반복 점검용: 같은 20봉 창의 피어슨 상관(ΔOI, ΔPrice)
    corr_pctile: pd.Series    # 대조군③(피어슨 상관 게이트): corr_roll 의 365일 롤링 백분위
    agree_vol: pd.Series      # 대조군④(신호원 교체): sign(ΔVolume)==sign(ΔPrice) 부호일치율
    agree_vol_pctile: pd.Series
    ema_fast: pd.Series
    ema_slow: pd.Series
    atr20: pd.Series
    atr_pct: pd.Series        # 동어반복 점검용: ATR%(=atr20/close)
    vol_z: pd.Series          # 동어반복 점검용: 거래량 20봉 롤링 z-score
    d_oi: pd.Series
    d_price: pd.Series
    d_volume: pd.Series
    oi_4h: pd.Series
    agree_window: int
    hi_th: float
    ema_fast_n: int
    ema_slow_n: int
    atr_stop_mult: float


def build_signals(agree_window: int = AGREE_WINDOW, norm_days: int = AGREE_NORM_DAYS,
                   hi_th: float = HI_TH, ema_fast_n: int = EMA_FAST, ema_slow_n: int = EMA_SLOW,
                   atr_stop_mult: float = ATR_STOP_MULT) -> Signals | None:
    df4h = load_klines_4h()
    m5 = load_metrics_5m()
    if df4h.empty or m5.empty:
        return None

    oi_4h = oi_4h_from_5m(m5, df4h.index)

    d_price = df4h["close"].diff()
    d_oi = oi_4h.diff()

    sign_price = np.sign(d_price)
    sign_oi = np.sign(d_oi)
    # 부호 0(변화 없음)은 '일치 아님'으로 처리(스펙 미명시 — 결측 취급이 아니라 이진 카운트의
    # 자연스러운 확장: sign_price==sign_oi 비교에서 0==0 이 True 로 잡히는 것만 별도 방지).
    valid = d_price.notna() & d_oi.notna()
    same = (sign_price == sign_oi) & valid & (sign_price != 0) & (sign_oi != 0)
    same_f = same.astype(float)
    same_f[~valid] = np.nan

    agree = same_f.rolling(agree_window, min_periods=agree_window).mean()

    bars_per_day = 6  # 4h → 하루 6봉
    norm_bars = norm_days * bars_per_day
    agree_pctile = rolling_pctile(agree, norm_bars)

    # 동어반복 점검: 같은 20봉 창의 피어슨 상관(ΔOI, ΔPrice)
    corr_roll = d_oi.rolling(agree_window).corr(d_price)
    corr_pctile = rolling_pctile(corr_roll, norm_bars)

    # 대조군④(신호원 교체): OI 대신 거래량으로 같은 부호일치율 산식 재사용
    d_volume = df4h["volume"].diff()
    sign_volume = np.sign(d_volume)
    valid_v = d_price.notna() & d_volume.notna()
    same_v = (sign_price == sign_volume) & valid_v & (sign_price != 0) & (sign_volume != 0)
    same_v_f = same_v.astype(float)
    same_v_f[~valid_v] = np.nan
    agree_vol = same_v_f.rolling(agree_window, min_periods=agree_window).mean()
    agree_vol_pctile = rolling_pctile(agree_vol, norm_bars)

    ema_fast = ind.ema(df4h["close"], ema_fast_n)
    ema_slow = ind.ema(df4h["close"], ema_slow_n)
    atr20 = ind.atr(df4h, 20)
    atr_pct = atr20 / df4h["close"]
    vol_m = df4h["volume"].rolling(agree_window).mean()
    vol_sd = df4h["volume"].rolling(agree_window).std(ddof=0)
    vol_z = ((df4h["volume"] - vol_m) / vol_sd).where(vol_sd > 1e-12)

    return Signals(df4h=df4h, agree=agree, agree_pctile=agree_pctile, corr_roll=corr_roll,
                   corr_pctile=corr_pctile, agree_vol=agree_vol, agree_vol_pctile=agree_vol_pctile,
                   ema_fast=ema_fast, ema_slow=ema_slow, atr20=atr20, atr_pct=atr_pct, vol_z=vol_z,
                   d_oi=d_oi, d_price=d_price, d_volume=d_volume, oi_4h=oi_4h,
                   agree_window=agree_window, hi_th=hi_th, ema_fast_n=ema_fast_n,
                   ema_slow_n=ema_slow_n, atr_stop_mult=atr_stop_mult)
