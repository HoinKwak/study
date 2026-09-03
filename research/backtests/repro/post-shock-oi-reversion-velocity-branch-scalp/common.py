"""1시간 가격충격 후 OI 원상복귀 속도 분기 스캘프 — 공통 데이터 로더.

스펙: research/strategies/post-shock-oi-reversion-velocity-branch-scalp.md
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
    "PSHOCK_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "PSHOCK_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/pshock"))
DATA = SP / "data"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = (TAKER_FEE + SLIPPAGE) * 2  # 0.14%

_KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
               "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


def _load_klines(symbol: str, tf_dir: str) -> pd.DataFrame:
    files = sorted(DATA.glob(f"{tf_dir}/{symbol}-*.csv"))
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
    # ms/us 단위사고 방지: open_time 자릿수로 단위 판별(13자리=ms, 16자리=us)
    sample = int(out["open_time"].iloc[0])
    unit = "us" if sample > 10 ** 14 else "ms"
    out["dt"] = pd.to_datetime(out["open_time"], unit=unit, utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    out["count"] = pd.to_numeric(out["count"], errors="coerce")
    return out[["open", "high", "low", "close", "volume", "quote_volume", "count"]]


@lru_cache(maxsize=None)
def load_klines_1h(symbol: str) -> pd.DataFrame:
    return _load_klines(symbol, "klines_1h")


@lru_cache(maxsize=None)
def load_klines_15m(symbol: str) -> pd.DataFrame:
    return _load_klines(symbol, "klines_15m")


@lru_cache(maxsize=None)
def load_metrics_5m(symbol: str) -> pd.DataFrame:
    """metrics 5분 원본 로드. create_time 은 날짜 문자열 → 명시적 format 파싱(ns 단위 명시,
    unit 미지정 us 추론 함정 회피). 실측: create_time 은 정시 5분 경계에 지터 없이 정렬됨
    (초=00 고정, funding calc_time 과 달리 밀리초 지터 없음 — 아래 run_metrics_alignment_check.py
    로 별도 확인)."""
    files = sorted(DATA.glob(f"metrics/{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "sum_open_interest_value"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out["sum_open_interest_value"] = pd.to_numeric(out["sum_open_interest_value"], errors="coerce")
    return out[["sum_open_interest_value"]]


def oi_hourly(m5: pd.DataFrame) -> pd.Series:
    """5분 OI(명목가치) → 1h 리샘플(해당 시간 구간 마지막 관측치, ffill).
    bar t 라벨에 배정된 값은 [t, t+1h) 구간 마지막 관측 ≈ bar t 종가시점 OI (룩어헤드 아님,
    bar t 가 닫혀야 확정됨)."""
    if m5.empty:
        return pd.Series(dtype=float)
    s = m5["sum_open_interest_value"].resample("1h", label="left", closed="left").last()
    return s.ffill()


@dataclass
class SymbolData:
    h1: pd.DataFrame        # 1h klines
    m15: pd.DataFrame       # 15m klines
    atr1h: pd.Series        # ATR(14,1h)
    atr15m: pd.Series       # ATR(14,15m)
    ema20_15m: pd.Series    # EMA(20,15m)
    oi1h: pd.Series         # 1h-aligned OI (sum_open_interest_value)


def build_symbol_data(symbol: str) -> SymbolData | None:
    h1 = load_klines_1h(symbol)
    m15 = load_klines_15m(symbol)
    m5 = load_metrics_5m(symbol)
    if h1.empty or m15.empty or m5.empty:
        return None
    atr1h = ind.atr(h1, 14)
    atr15m = ind.atr(m15, 14)
    ema20_15m = ind.ema(m15["close"], 20)
    oi1h = oi_hourly(m5)
    return SymbolData(h1=h1, m15=m15, atr1h=atr1h, atr15m=atr15m, ema20_15m=ema20_15m, oi1h=oi1h)


def load_all(symbols=SYMBOLS) -> dict[str, SymbolData]:
    out = {}
    for s in symbols:
        sd = build_symbol_data(s)
        if sd is not None:
            out[s] = sd
    return out


def period_of(ts: pd.Timestamp) -> str:
    if IS_START <= ts <= IS_END:
        return "IS"
    if OOS_START <= ts <= OOS_END:
        return "OOS"
    return "OUT"
