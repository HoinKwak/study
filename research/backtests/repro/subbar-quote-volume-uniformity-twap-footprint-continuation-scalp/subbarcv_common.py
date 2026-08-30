"""공통 데이터 로더 — data.binance.vision 선물(UM) 월별 klines/premiumIndexKlines 덤프 다운로드+캐시.

이 컨테이너에서는 바이낸스 선물 fapi 가 451(지역차단)이라 REST 직접 호출이 불가능하다.
대신 공개 정적 덤프(https://data.binance.vision/data/futures/um/monthly/...)를
받아 로컬(스크래치패드)에 pickle 캐시한다. 재실행 시 캐시를 재사용해 다운로드를 피한다.
"""
from __future__ import annotations

import io
import pickle
import zipfile
from pathlib import Path

import pandas as pd
import requests

CACHE_DIR = Path(
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/subbarcv_data/klines_cache"
)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://data.binance.vision/data/futures/um/monthly/klines"
PREMIUM_BASE_URL = "https://data.binance.vision/data/futures/um/monthly/premiumIndexKlines"
PREMIUM_CACHE_DIR = Path(
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/subbarcv_data/premium_cache"
)
PREMIUM_CACHE_DIR.mkdir(parents=True, exist_ok=True)

COLUMNS = [
    "open_time", "open", "high", "low", "close", "volume", "close_time",
    "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore",
]


def _month_range(start: str, end: str) -> list[tuple[int, int]]:
    """start~end(YYYY-MM-DD) 사이의 (year, month) 리스트(포함)."""
    s = pd.Timestamp(start)
    e = pd.Timestamp(end)
    out = []
    y, m = s.year, s.month
    while (y, m) <= (e.year, e.month):
        out.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def _fetch_month(base_url: str, symbol: str, tf: str, year: int, month: int) -> pd.DataFrame | None:
    fname = f"{symbol}-{tf}-{year:04d}-{month:02d}"
    url = f"{base_url}/{symbol}/{tf}/{fname}.zip"
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        return None
    z = zipfile.ZipFile(io.BytesIO(r.content))
    name = z.namelist()[0]
    with z.open(name) as f:
        first = f.readline()
    header = 0 if first.startswith(b"open_time") else None
    with z.open(name) as f:
        df = pd.read_csv(f, header=header, names=COLUMNS if header is None else None)
    if header is None:
        df.columns = COLUMNS
    return df


def load_klines(symbol: str, tf: str, start: str, end: str,
                 force_refresh: bool = False) -> pd.DataFrame:
    """symbol(예: BTCUSDT) tf(예: 15m) 의 [start,end] 구간 klines 를 DataFrame(UTC DatetimeIndex)으로 반환.

    open_time(ms, int64) 을 그대로 datetime64[ns] 로 변환(단위 명시로 ns/ms 사고 방지).
    로컬 캐시(month 단위 pickle)를 우선 사용, 없으면 다운로드.
    """
    months = _month_range(start, end)
    frames = []
    for y, m in months:
        cache_f = CACHE_DIR / f"{symbol}_{tf}_{y:04d}-{m:02d}.pkl"
        if cache_f.exists() and not force_refresh:
            with open(cache_f, "rb") as f:
                df = pickle.load(f)
        else:
            df = _fetch_month(BASE_URL, symbol, tf, y, m)
            if df is not None:
                with open(cache_f, "wb") as f:
                    pickle.dump(df, f)
        if df is not None and len(df):
            frames.append(df)
    if not frames:
        raise RuntimeError(f"데이터 없음: {symbol} {tf} {start}~{end}")
    full = pd.concat(frames, ignore_index=True)
    full = full.drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
    # 단위 명시: open_time 은 밀리초(ms) epoch. pandas 3.0.3 은 unit="ms" 시 datetime64[ms] 유지
    # (ns 자동승격 아님) — 명시적으로 ns 로 변환해 다른 ns 기반 타임스탬프와 혼용 안전하게.
    idx = pd.to_datetime(full["open_time"].astype("int64"), unit="ms", utc=True).dt.tz_localize(None)
    idx = idx.astype("datetime64[ns]")
    out = full.set_index(pd.DatetimeIndex(idx, name="open_time"))
    for c in ["open", "high", "low", "close", "volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume"]]
    mask = (out.index >= pd.Timestamp(start)) & (out.index <= pd.Timestamp(end) + pd.Timedelta(days=1))
    return out[mask]


def load_premium_index(symbol: str, tf: str, start: str, end: str,
                        force_refresh: bool = False) -> pd.DataFrame:
    """프리미엄인덱스(premiumIndexKlines) [start,end] 구간을 DataFrame(UTC DatetimeIndex)으로 반환.

    premiumIndexKlines 의 OHLC 는 (mark-index)/index 비율(basis) 값이며 klines 와
    동일 컬럼 스키마를 공유한다(volume/count 등은 의미 없는 더미값 -- 사용 안 함).
    """
    months = _month_range(start, end)
    frames = []
    for y, m in months:
        cache_f = PREMIUM_CACHE_DIR / f"{symbol}_{tf}_{y:04d}-{m:02d}.pkl"
        if cache_f.exists() and not force_refresh:
            with open(cache_f, "rb") as f:
                df = pickle.load(f)
        else:
            df = _fetch_month(PREMIUM_BASE_URL, symbol, tf, y, m)
            if df is not None:
                with open(cache_f, "wb") as f:
                    pickle.dump(df, f)
        if df is not None and len(df):
            frames.append(df)
    if not frames:
        raise RuntimeError(f"프리미엄인덱스 데이터 없음: {symbol} {tf} {start}~{end}")
    full = pd.concat(frames, ignore_index=True)
    full = full.drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
    idx = pd.to_datetime(full["open_time"].astype("int64"), unit="ms", utc=True).dt.tz_localize(None)
    idx = idx.astype("datetime64[ns]")
    out = full.set_index(pd.DatetimeIndex(idx, name="open_time"))
    for c in ["open", "high", "low", "close"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close"]]
    mask = (out.index >= pd.Timestamp(start)) & (out.index <= pd.Timestamp(end) + pd.Timedelta(days=1))
    return out[mask]


SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = "2022-01-01"
IS_END = "2024-06-30 23:59:59"
OOS_START = "2024-07-01"
OOS_END = "2026-06-30 23:59:59"

TAKER_FEE = 0.0005     # 편도 테이커 수수료
SLIPPAGE = 0.0002       # 편도 슬리피지


def load_klines_qv(symbol: str, tf: str, start: str, end: str,
                    force_refresh: bool = False) -> pd.DataFrame:
    """load_klines 와 동일하지만 quote_volume(quote_asset_volume) 컬럼을 함께 반환.

    캐시 pkl 자체엔 이미 전체 컬럼(COLUMNS)이 저장돼 있어 load_klines 와 캐시를 공유한다.
    """
    months = _month_range(start, end)
    frames = []
    for y, m in months:
        cache_f = CACHE_DIR / f"{symbol}_{tf}_{y:04d}-{m:02d}.pkl"
        if cache_f.exists() and not force_refresh:
            with open(cache_f, "rb") as f:
                df = pickle.load(f)
        else:
            df = _fetch_month(BASE_URL, symbol, tf, y, m)
            if df is not None:
                with open(cache_f, "wb") as f:
                    pickle.dump(df, f)
        if df is not None and len(df):
            frames.append(df)
    if not frames:
        raise RuntimeError(f"데이터 없음: {symbol} {tf} {start}~{end}")
    full = pd.concat(frames, ignore_index=True)
    full = full.drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
    idx = pd.to_datetime(full["open_time"].astype("int64"), unit="ms", utc=True).dt.tz_localize(None)
    idx = idx.astype("datetime64[ns]")
    out = full.set_index(pd.DatetimeIndex(idx, name="open_time"))
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume", "quote_volume"]]
    mask = (out.index >= pd.Timestamp(start)) & (out.index <= pd.Timestamp(end) + pd.Timedelta(days=1))
    return out[mask]
