"""유니버스 OI 명목가치 횡단면 허핀달 집중도(HHI) 게이트 + BTC 추세추종 — 공통 로더/신호.

스펙: research/strategies/oi-cross-sectional-herfindahl-concentration-breadth-btc-trend-swing.md
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
    "OIHHI_REPO_SRC",
    "/home/user/study/.claude/worktrees/agent-a25eed216f42f1e6d/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "OIHHI_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oihhi"))
DATA = SP / "data"
KLINES_1D_DIR = DATA / "klines_1d"
KLINES_4H_DIR = DATA / "klines_4h"
METRICS_DIR = DATA / "metrics"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = (TAKER_FEE + SLIPPAGE) * 2  # 0.14%

# ------------------------------------------------------------- 파라미터(스펙 기본값)
HHI_WINDOW_DAYS = 60
LO_TH = -0.75
HI_TH = 0.75
EMA_LEN = 50
ATR_STOP_MULT = 2.0
ATR_TRAIL_MULT = 3.0
MAX_HOLD_DAYS = 30

_KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
               "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


# ------------------------------------------------------------------ 로더

def _load_klines(dirpath: Path, symbol: str, tf: str) -> pd.DataFrame:
    files = sorted(dirpath.glob(f"{symbol}-{tf}-*.csv"))
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
def load_klines_1d(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_1D_DIR, symbol, "1d")


@lru_cache(maxsize=None)
def load_klines_4h(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_4H_DIR, symbol, "4h")


@lru_cache(maxsize=None)
def load_metrics_5m(symbol: str) -> pd.DataFrame:
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


def oi_1d_from_5m(m5: pd.DataFrame) -> pd.Series:
    """5분 OI → 1d 마지막값(그날 00:00 UTC 경계 마감시점, label=left/closed=left)."""
    if m5.empty:
        return pd.Series(dtype=float)
    s = m5["sum_open_interest"]
    last = s.resample("1D", label="left", closed="left").last()
    return last


def rolling_zscore(x: pd.Series, window: int) -> pd.Series:
    m = x.rolling(window).mean()
    sd = x.rolling(window).std(ddof=0)
    z = (x - m) / sd
    return z.where(sd > 1e-12)


# ------------------------------------------------------------------ 유니버스 OI 명목가치/HHI 구축

@dataclass
class Universe:
    oi_notional: pd.DataFrame   # 1d, 컬럼=심볼, 값=OI 명목가치(USDT)
    close_1d: pd.DataFrame      # 1d 종가(HHI 매핑·정합성 확인용)
    hhi: pd.Series              # 유니버스 HHI(t) — 결측 종목 있는 날은 NaN
    btc_oi_share: pd.Series     # 대조군②: BTC OI 명목가치 / 유니버스 합계


def build_universe() -> Universe:
    oi_cols = {}
    close_cols = {}
    for sym in SYMBOLS:
        k1d = load_klines_1d(sym)
        m5 = load_metrics_5m(sym)
        if k1d.empty or m5.empty:
            continue
        oi1d = oi_1d_from_5m(m5)
        oi1d.index = oi1d.index.as_unit("ns")
        k1d = k1d.copy()
        k1d.index = k1d.index.as_unit("ns")
        # 명목가치 = OI(코인단위) * 종가(USDT). 같은 1d 인덱스(그날 00:00 UTC)에 정렬.
        joined = pd.DataFrame({"oi": oi1d}).join(k1d[["close"]], how="inner")
        notional = joined["oi"] * joined["close"]
        oi_cols[sym] = notional
        close_cols[sym] = k1d["close"]

    oi_notional = pd.DataFrame(oi_cols)
    close_1d = pd.DataFrame(close_cols)

    # 결측 종목이 하나라도 있는 날은 HHI 계산에서 제외(재정규화 왜곡 방지)
    complete_mask = oi_notional.notna().all(axis=1)
    total = oi_notional.sum(axis=1)
    shares = oi_notional.div(total, axis=0)
    hhi = (shares ** 2).sum(axis=1)
    hhi = hhi.where(complete_mask)

    btc_oi_share = shares["BTCUSDT"].where(complete_mask)

    return Universe(oi_notional=oi_notional, close_1d=close_1d, hhi=hhi,
                    btc_oi_share=btc_oi_share)


@dataclass
class Signals:
    df1d: pd.DataFrame
    df4h: pd.DataFrame
    hhi: pd.Series
    hhi_z: pd.Series
    btc_oi_share: pd.Series
    btc_oi_share_z: pd.Series
    oi_total_growth7: pd.Series   # 대조군용: 유니버스 OI 합계 7일 로그성장률
    ema50_1d: pd.Series
    atr14_4h: pd.Series
    hhi_window: int


def build_signals(univ: Universe, hhi_window: int = HHI_WINDOW_DAYS) -> Signals | None:
    btc_1d = load_klines_1d("BTCUSDT")
    btc_4h = load_klines_4h("BTCUSDT")
    if btc_1d.empty or btc_4h.empty:
        return None

    hhi_z = rolling_zscore(univ.hhi, hhi_window)
    btc_oi_share_z = rolling_zscore(univ.btc_oi_share, hhi_window)

    oi_total = univ.oi_notional.sum(axis=1).where(univ.oi_notional.notna().all(axis=1))
    oi_total_growth7 = np.log(oi_total / oi_total.shift(7))

    ema50_1d = ind.ema(btc_1d["close"], EMA_LEN)
    atr14_4h = ind.atr(btc_4h, 14)

    return Signals(df1d=btc_1d, df4h=btc_4h, hhi=univ.hhi, hhi_z=hhi_z,
                   btc_oi_share=univ.btc_oi_share, btc_oi_share_z=btc_oi_share_z,
                   oi_total_growth7=oi_total_growth7, ema50_1d=ema50_1d, atr14_4h=atr14_4h,
                   hhi_window=hhi_window)
