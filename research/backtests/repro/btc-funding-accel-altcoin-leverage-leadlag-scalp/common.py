"""BTC 펀딩가속 -> 알트 레버리지 유입 후행 스캘프 — 공통 로더/시그널 계산.

스펙: research/strategies/btc-funding-accel-altcoin-leverage-leadlag-scalp.md
슬러그 고유 모듈명(btcfundleadlag)으로 다른 동시 백테스터와 격리.
"""
from __future__ import annotations

import os
import sys
import zipfile
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

_repo_src = os.environ.get(
    "BFLL_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "BFLL_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/btcfundleadlag"))
DATA = SP / "data"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
ALT_SYMBOLS = ["ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = (TAKER_FEE + SLIPPAGE) * 2  # 0.14%

_KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
               "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


def _read_zip_csv(path: Path, names: list[str] | None = None) -> pd.DataFrame:
    with zipfile.ZipFile(path) as zf:
        inner = zf.namelist()[0]
        with zf.open(inner) as f:
            first = f.readline().decode()
        has_header = not first.strip().split(",")[0].lstrip("-").isdigit()
        with zf.open(inner) as f:
            if has_header:
                df = pd.read_csv(f)
            else:
                df = pd.read_csv(f, header=None, names=names)
    return df


@lru_cache(maxsize=None)
def load_klines(symbol: str, tf: str) -> pd.DataFrame:
    d = DATA / f"klines{tf}"
    files = sorted(d.glob(f"{symbol}-{tf}-*.zip"))
    parts = []
    for p in files:
        try:
            df = _read_zip_csv(p, names=_KLINE_COLS)
        except Exception:  # noqa: BLE001
            continue
        df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
        if df.empty:
            continue
        df["open_time"] = df["open_time"].astype("int64")
        df["close_time"] = df["close_time"].astype("int64")
        parts.append(df)
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out["close_dt"] = pd.to_datetime(out["close_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    return out[["open", "high", "low", "close", "volume", "quote_volume", "close_dt"]]


@lru_cache(maxsize=None)
def load_funding(symbol: str) -> pd.DataFrame:
    d = DATA / "funding"
    files = sorted(d.glob(f"{symbol}-fundingRate-*.zip"))
    parts = []
    for p in files:
        try:
            df = _read_zip_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty:
            continue
        parts.append(df)
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["calc_time"] = out["calc_time"].astype("int64")
    out["dt"] = pd.to_datetime(out["calc_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    out["last_funding_rate"] = out["last_funding_rate"].astype(float)
    return out[["last_funding_rate"]]


@dataclass
class FundingAccel:
    df: pd.DataFrame           # funding index=dt(calc_time), col last_funding_rate
    delta: pd.Series           # funding_t - funding_{t-1}
    roll_std: pd.Series        # rolling(60) std of delta, causal (inclusive)


def build_funding_accel(symbol: str = "BTCUSDT", window: int = 60) -> FundingAccel:
    df = load_funding(symbol)
    delta = df["last_funding_rate"].diff()
    roll_std = delta.rolling(window, min_periods=window).std(ddof=0)
    return FundingAccel(df=df, delta=delta, roll_std=roll_std)


def find_accel_events(fa: FundingAccel, accel_z_threshold: float = 1.5) -> pd.DataFrame:
    """가속 트리거 이벤트 목록. 각 이벤트: (trigger_time, direction[+1/-1], z_equiv).

    조건(스펙): delta[t]와 delta[t-1]이 같은 부호이고, |delta[t]|+|delta[t-1]| >=
    accel_z_threshold * rolling_std60(delta)[t] (causal, t 시점까지 데이터만 사용).
    """
    delta = fa.delta
    sd = fa.roll_std
    d0 = delta
    d1 = delta.shift(1)
    same_sign = (np.sign(d0) == np.sign(d1)) & (d0 != 0) & (d1 != 0)
    magsum = d0.abs() + d1.abs()
    valid_sd = sd.notna() & (sd > 0)
    trig = same_sign & valid_sd & (magsum >= accel_z_threshold * sd)
    ev = pd.DataFrame({
        "trigger_time": delta.index[trig],
        "direction": np.sign(d0[trig]).astype(int).to_numpy(),
        "magsum": magsum[trig].to_numpy(),
        "sd": sd[trig].to_numpy(),
    })
    ev["z_equiv"] = ev["magsum"] / ev["sd"]
    return ev.reset_index(drop=True)


@dataclass
class AltSignals:
    df: pd.DataFrame          # 15m klines
    don_upper: pd.Series      # 과거 20봉(자기 제외) 고가 최대
    don_lower: pd.Series      # 과거 20봉(자기 제외) 저가 최소
    vol_avg: pd.Series        # 과거 20봉(자기 제외) quote_volume 평균
    atr1h_on15: np.ndarray    # 매 15m bar 시점에 인과적으로 참조 가능한 최근 확정 1h ATR14


def build_alt_signals(symbol: str, donchian_lookback: int = 20) -> AltSignals | None:
    df15 = load_klines(symbol, "15m")
    if df15.empty:
        return None
    df1h = load_klines(symbol, "1h")
    if df1h.empty:
        return None
    high = df15["high"]
    low = df15["low"]
    qv = df15["quote_volume"]
    don_upper = high.shift(1).rolling(donchian_lookback, min_periods=donchian_lookback).max()
    don_lower = low.shift(1).rolling(donchian_lookback, min_periods=donchian_lookback).min()
    vol_avg = qv.shift(1).rolling(donchian_lookback, min_periods=donchian_lookback).mean()
    atr1h = ind.atr(df1h, 14)

    # 1h ATR을 15m 타임라인에 인과적으로 매핑: 각 1h 봉은 close_time(=다음 봉 open_time)에
    # 확정되므로, "확정시각=close_dt"를 키로 merge_asof(backward)한다. ns 단위 명시로
    # datetime64[ms]+Timedelta 업캐스트 함정을 원천 차단(둘 다 미리 datetime64[ns]로 변환).
    left = pd.DataFrame({
        "ts": df15.index.tz_convert("UTC").tz_localize(None).astype("datetime64[ns]")})
    right = pd.DataFrame({
        "confirmed_at": (df1h["close_dt"].dt.tz_convert("UTC").dt.tz_localize(None)
                         .to_numpy().astype("datetime64[ns]")),
        "atr1h": atr1h.to_numpy(float),
    }).sort_values("confirmed_at")
    merged = pd.merge_asof(left.sort_values("ts"), right, left_on="ts", right_on="confirmed_at",
                           direction="backward")
    atr1h_on15 = merged["atr1h"].to_numpy(float)

    return AltSignals(df=df15, don_upper=don_upper, don_lower=don_lower, vol_avg=vol_avg,
                      atr1h_on15=atr1h_on15)
