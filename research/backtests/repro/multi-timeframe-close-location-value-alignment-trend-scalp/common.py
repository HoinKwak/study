"""멀티TF CLV(Close Location Value) 정렬 추세추종 스캘프 — 공통 데이터 로더 + 지표.

스펙: research/strategies/multi-timeframe-close-location-value-alignment-trend-scalp.md

⚠️ 시간 단위 함정: pandas 3.0.x 는 `to_datetime(unit="ms")` 가 `datetime64[ms]` 를 유지하고,
여기에 `pd.Timedelta` 를 더하면 조용히 `datetime64[us]` 로 업캐스트되어 merge_asof 정렬이 깨진다.
이 모듈은 모든 DatetimeIndex 를 파싱 직후 `.astype("datetime64[ns, UTC]")` 로 명시 통일한다.
"""
from __future__ import annotations

import io
import os
import sys
import zipfile
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
import requests

_repo_src = os.environ.get(
    "MTFCLV_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))
sys.path.insert(0, _repo_src)

SP = Path(os.environ.get(
    "MTFCLV_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/mtfclv"))
DATA = SP / "data"
DATA.mkdir(parents=True, exist_ok=True)

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

BASE_URL = "https://data.binance.vision/data/futures/um/monthly/klines"


def _month_range(start: pd.Timestamp, end: pd.Timestamp) -> list[tuple[int, int]]:
    out = []
    y, m = start.year, start.month
    while (y, m) <= (end.year, end.month):
        out.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def fetch_month(symbol: str, tf: str, year: int, month: int) -> pd.DataFrame | None:
    out_csv = DATA / f"klines_{tf}" / f"{symbol}-{tf}-{year:04d}-{month:02d}.csv"
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    if out_csv.exists():
        try:
            df = pd.read_csv(out_csv)
            if df.empty:
                return None
            return df
        except Exception:  # noqa: BLE001
            out_csv.unlink(missing_ok=True)
    url = f"{BASE_URL}/{symbol}/{tf}/{symbol}-{tf}-{year:04d}-{month:02d}.zip"
    try:
        r = requests.get(url, timeout=60)
    except Exception:  # noqa: BLE001
        return None
    if r.status_code != 200:
        return None
    z = zipfile.ZipFile(io.BytesIO(r.content))
    name = z.namelist()[0]
    with z.open(name) as f:
        first = f.readline()
    header = 0 if first.startswith(b"open_time") else None
    with z.open(name) as f:
        df = pd.read_csv(f, header=header, names=_KLINE_COLS if header is None else None)
    if header is None:
        df.columns = _KLINE_COLS
    df.to_csv(out_csv, index=False)
    return df


def prefetch(symbols=SYMBOLS, tfs=("15m", "1h", "4h"),
             start=IS_START, end=OOS_END) -> None:
    months = _month_range(start, end)
    for tf in tfs:
        for sym in symbols:
            for y, m in months:
                fetch_month(sym, tf, y, m)


@lru_cache(maxsize=None)
def load_klines(symbol: str, tf: str) -> pd.DataFrame:
    files = sorted((DATA / f"klines_{tf}").glob(f"{symbol}-{tf}-*.csv"))
    parts = []
    for p in files:
        df = pd.read_csv(p)
        df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
        if df.empty:
            continue
        df["open_time"] = df["open_time"].astype("int64")
        parts.append(df)
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    dt = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    dt = pd.DatetimeIndex(dt).astype("datetime64[ns, UTC]")
    out["dt"] = dt
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume", "taker_buy_volume"]:
        out[c] = out[c].astype(float)
    return out[["open", "high", "low", "close", "volume", "quote_volume", "taker_buy_volume"]]


# ------------------------------------------------------------------ CLV 지표

def clv(df: pd.DataFrame) -> pd.Series:
    """CLV(=IBS) = (close-low)/(high-low). high==low 이면 0.5(0 division 방지, 스펙 명시)."""
    rng = df["high"] - df["low"]
    out = (df["close"] - df["low"]) / rng
    out = out.where(rng > 0, 0.5)
    return out.clip(0.0, 1.0)


def map_asof_backward(target_time: pd.DatetimeIndex, source: pd.Series,
                       source_bar_seconds: int) -> np.ndarray:
    """source(자신의 TF 상 open_time 인덱스)를 '봉이 닫혀 값이 확정된 시각'
    (open_time + bar_length) 기준으로 target_time 에 backward asof 매핑.
    target 시각 t 에서는 avail_time<=t 인 가장 최근 source 값만 사용(미래 참조 불가).
    ⚠️ naive 매핑이 아니라 '확정시각' 기준 asof 이므로, 같은 상위TF 봉 구간에 속하는 여러 하위TF
    봉은 전부 동일한 상위TF 값을 재사용한다(자연스러운 반복 — 재발화 아님, 상위 봉이 실제로
    갱신될 때만 값이 바뀐다)."""
    src = source.dropna()
    if src.empty:
        return np.full(len(target_time), np.nan)
    avail = (src.index + pd.Timedelta(seconds=source_bar_seconds)).astype("datetime64[ns, UTC]")
    order = np.argsort(avail.values)
    avail_sorted = avail[order]
    vals_sorted = src.to_numpy(float)[order]
    left = pd.DataFrame({"t": pd.DatetimeIndex(target_time).astype("datetime64[ns, UTC]")})
    right = pd.DataFrame({"avail": avail_sorted, "val": vals_sorted})
    left_sorted = left.sort_values("t")
    merged = pd.merge_asof(left_sorted, right, left_on="t", right_on="avail", direction="backward")
    merged = merged.set_index(left_sorted.index).reindex(left.index)
    return merged["val"].to_numpy(float)
