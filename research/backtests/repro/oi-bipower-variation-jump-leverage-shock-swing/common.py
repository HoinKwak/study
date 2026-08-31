"""OI Bipower Variation 점프탐지 — 레버리지쇼크 스윙. 공통 데이터 로더 + JR(점프비율) 계산.

스펙: research/strategies/oi-bipower-variation-jump-leverage-shock-swing.md
대조군 스펙(가격기반 BV, 동어반복 점검용): research/strategies/bipower-variation-jump-continuation-swing.md
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
    "OIBV_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "OIBV_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oibv"))
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


# ------------------------------------------------------------------ klines 로더

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
    unit = "us" if sample > 10**14 else "ms"
    out["dt"] = pd.to_datetime(out["open_time"], unit=unit, utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    return out[["open", "high", "low", "close", "volume", "quote_volume"]]


@lru_cache(maxsize=None)
def load_klines_1d(symbol: str) -> pd.DataFrame:
    return _load_klines(symbol, "klines_1d")


@lru_cache(maxsize=None)
def load_klines_1h(symbol: str) -> pd.DataFrame:
    return _load_klines(symbol, "klines_1h")


@lru_cache(maxsize=None)
def load_metrics_5m(symbol: str) -> pd.DataFrame:
    """metrics 5분 원본 로드. create_time 은 날짜 문자열 → 명시적 format 파싱(단위 사고 회피)."""
    files = sorted(DATA.glob(f"metrics/{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "sum_open_interest"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    return out[["sum_open_interest"]]


def oi_hourly(m5: pd.DataFrame) -> pd.Series:
    """5분 OI → 1h 종가 리샘플 + ffill (스펙 §90행 명시: resample('1h').last().ffill())."""
    if m5.empty:
        return pd.Series(dtype=float)
    s = m5["sum_open_interest"].resample("1h", label="left", closed="left").last()
    return s.ffill()


# ------------------------------------------------------------------ JR(점프비율) 계산

def daily_jr_from_hourly_logret(hourly: pd.Series) -> pd.DataFrame:
    """1시간 간격 시계열(OI 또는 가격)의 로그수익률로 일별 RV/BV/JR 계산.

    각 UTC 캘린더일에 대해: r_i = diff(log(x))(그날 소속 시간당 관측, i=1..24 근사).
    RV = Σr_i², BV = (π/2)·Σ_{i=2}^{k}|r_i||r_{i-1}| (같은 날 안에서만 인접쌍 사용 — 날짜 경계를
    넘어 전날 마지막 시간과 당일 첫 시간을 인접쌍으로 잇지 않음, 스펙의 "일별" 정의를 엄격히 따름).
    결측(당일 관측 수 < 20/24)인 날은 그 날 통계 제외(NaN).
    """
    x = hourly.dropna()
    if x.empty:
        return pd.DataFrame()
    logx = np.log(x.replace(0, np.nan)).dropna()
    r = logx.diff().dropna()
    day = r.index.floor("D")
    out_rows = []
    for d, grp in r.groupby(day):
        vals = grp.to_numpy(float)
        k = len(vals)
        if k < 20:  # 24개 기대, 결측 과다일 제외(스펙 §88행)
            continue
        rv = float(np.sum(vals ** 2))
        if rv <= 0 or not np.isfinite(rv):
            continue
        bv = float((np.pi / 2.0) * np.sum(np.abs(vals[1:]) * np.abs(vals[:-1])))
        jr = max(rv - bv, 0.0) / rv
        out_rows.append((d, rv, bv, jr, k))
    if not out_rows:
        return pd.DataFrame()
    df = pd.DataFrame(out_rows, columns=["day", "rv", "bv", "jr", "n_obs"]).set_index("day")
    return df


def rolling_pctile_of_jr(jr: pd.Series, window_days: int) -> pd.Series:
    """JR 의 자기 롤링 백분위(당일 포함 window_days 창 내에서의 순위, 0~100).
    창에 결측일(캘린더 gap)이 섞여도 '실제 존재하는 JR 관측치' window_days개 기준으로 계산
    (스펙이 캘린더일 수가 아니라 관측 표본수 기준 90일 롤링임을 의도한다고 해석 — daily_jr가
    이미 결측일을 제외했으므로 이 시계열의 인덱스는 '유효 관측일'만 남아있다)."""
    return jr.rolling(window_days, min_periods=window_days).apply(
        lambda w: (w <= w.iloc[-1]).mean() * 100.0, raw=False)


@dataclass
class SymbolData:
    d1: pd.DataFrame          # 1d klines
    oi_jr: pd.DataFrame       # day-indexed: rv,bv,jr,n_obs (OI 기반)
    px_jr: pd.DataFrame       # day-indexed: rv,bv,jr,n_obs (가격 기반, 1h 종가 로그수익률)
    day_ret_pct: pd.Series    # 1d 클로즈-오픈 순변화율(%) — "당일 가격 순변화"
    atr14_1d: pd.Series       # ATR(1d,14), day-indexed (d1.index 와 동일)


def build_symbol_data(symbol: str) -> SymbolData | None:
    d1 = load_klines_1d(symbol)
    h1 = load_klines_1h(symbol)
    m5 = load_metrics_5m(symbol)
    if d1.empty or h1.empty or m5.empty:
        return None
    oi_h = oi_hourly(m5)
    oi_jr = daily_jr_from_hourly_logret(oi_h)
    px_h = h1["close"]
    px_jr = daily_jr_from_hourly_logret(px_h)
    day_ret_pct = ((d1["close"] - d1["open"]) / d1["open"]) * 100.0
    day_ret_pct.index = day_ret_pct.index.floor("D")
    atr14 = ind.atr(d1, 14)
    atr14.index = d1.index
    return SymbolData(d1=d1, oi_jr=oi_jr, px_jr=px_jr, day_ret_pct=day_ret_pct, atr14_1d=atr14)


def load_all(symbols=SYMBOLS) -> dict[str, SymbolData]:
    out = {}
    for s in symbols:
        sd = build_symbol_data(s)
        if sd is not None:
            out[s] = sd
    return out
