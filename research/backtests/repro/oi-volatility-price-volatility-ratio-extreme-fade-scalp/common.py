"""OI 변동성 대 가격 실현변동성 비율 극단 페이드 스캘프 — 공통 데이터 로더 + 신호 계산.

스펙: research/strategies/oi-volatility-price-volatility-ratio-extreme-fade-scalp.md
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
    "OIVR_REPO_SRC",
    "/home/user/study/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "OIVR_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oivolratio"))
DATA = SP / "data"
KLINES_1H_DIR = DATA / "klines_1h"
KLINES_15M_DIR = DATA / "klines_15m"
METRICS_DIR = DATA / "metrics"

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
    is_us = ot.abs() > 10**14  # ms epoch 는 13자리(~1.7e12), us 라면 16자리(~1.7e15)
    if is_us.any():
        out.loc[is_us, "open_time"] = out.loc[is_us, "open_time"] // 1000
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume", "quote_volume"]]
    # ⚠️pandas 3.0.5 datetime 해상도 함정: to_datetime(unit="ms") 결과가 항상 ns 로 승격되는 게
    # 아니라 ms 로 유지될 수 있고, 다른 소스(metrics create_time 문자열 파싱)는 us 로 추론된다.
    # join/merge_asof/Timedelta 산술에서 조용히 오정렬되므로 ns 로 명시 통일한다.
    out.index = out.index.as_unit("ns")
    return out


@lru_cache(maxsize=None)
def load_klines_1h(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_1H_DIR, symbol, "1h")


@lru_cache(maxsize=None)
def load_klines_15m(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_15M_DIR, symbol, "15m")


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
    out.index = out.index.as_unit("ns")  # ns 명시 통일(klines 인덱스와 join 시 오정렬 방지)
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    # ⚠️데이터 결함(선례 확인): sum_open_interest 가 간헐적으로 0(또는 음수)인 "0-fill" placeholder
    # 시점이 존재 — 실제 OI 가 0이 될 수 없으므로 명백한 결측 placeholder. isna() 는 못 잡음(값
    # 자체가 0.0). 명시적으로 <=0 을 NaN 처리해 pct_change 폭주를 원천 차단.
    out.loc[out["sum_open_interest"] <= 0, "sum_open_interest"] = np.nan
    return out


def oi_1h_from_5m(m5: pd.DataFrame) -> pd.DataFrame:
    """5분 OI → 1h 봉 마감시점 값(resample('1h').last(), 빈 bin 은 NaN → 명시적 ffill).
    ffill 적용 여부·5분 표본수를 별도 컬럼으로 남겨 품질 추적."""
    if m5.empty:
        return pd.DataFrame()
    s = m5["sum_open_interest"]
    last = s.resample("1h", label="left", closed="left").last()
    cnt = s.resample("1h", label="left", closed="left").count()
    filled = last.ffill()
    out = pd.DataFrame({"oi": filled, "oi_raw_nan": last.isna(), "oi_5m_count": cnt})
    return out


def rolling_zscore(x: np.ndarray, window: int) -> np.ndarray:
    xs = pd.Series(x)
    m = xs.rolling(window).mean()
    sd = xs.rolling(window).std(ddof=0)
    z = (xs - m) / sd
    z = z.where(sd > 1e-12)
    return z.to_numpy()


# ------------------------------------------------------------------ 신호 구축

@dataclass
class Signals:
    df1h: pd.DataFrame        # 1h klines + oi
    df15m: pd.DataFrame       # 15m klines
    oi_ret: pd.Series         # 시간당 OI 변화율
    px_ret: pd.Series         # 시간당 로그수익률
    oi_vol60: pd.Series
    px_vol60: pd.Series
    vol_ratio: pd.Series
    z: np.ndarray             # vol_ratio 의 120h 롤링 z-score (핵심 신호)
    z_oi_only: np.ndarray     # 대조/동어반복점검: oi_vol60 단독 120h 롤링 z-score
    px_ret_4h_sum: pd.Series  # 직전 4시간 가격수익률 합(현재 bar 포함, 과거 3봉+현재)
    atr14_15m: pd.Series      # ATR(14, 15m)
    oi_5m_count: pd.Series
    oi_raw_nan: pd.Series


def build_signals(symbol: str, vol_window: int = 60, z_window: int = 120,
                  ret_gap_max_hours: int = 2) -> Signals | None:
    df1h = load_klines_1h(symbol)
    df15m = load_klines_15m(symbol)
    if df1h.empty or df15m.empty:
        return None
    m5 = load_metrics_5m(symbol)
    if m5.empty:
        return None
    oi1h = oi_1h_from_5m(m5)
    df1h = df1h.join(oi1h, how="left")
    # join 이 서로 다른 해상도 인덱스를 조용히 업캐스트할 수 있어(ms/us/ns 혼재 함정, 이번 라운드
    # 실측으로 재현·확인됨 — join 후 datetime64[us] 로 승격돼 이후 ns 오프셋 산술이 1000배 어긋남)
    # join 직후 다시 ns 로 명시 통일한다.
    df1h.index = df1h.index.as_unit("ns")
    df15m.index = df15m.index.as_unit("ns")

    # 시간외 갭(거래정지·데이터 결측) 마스킹: 인덱스 간격이 1h 를 초과하면 그 시점의 ret 를 NaN 처리
    # (스펙 "코딩 난이도" 절 요구사항 — 갭 구간에서 인위적 급변 신호 방지).
    idx = df1h.index
    gap_hours = idx.to_series().diff().dt.total_seconds() / 3600.0
    gap_too_large = (gap_hours > ret_gap_max_hours).to_numpy()

    oi_ret = df1h["oi"].pct_change()
    px_ret = np.log(df1h["close"] / df1h["close"].shift(1))
    oi_ret = oi_ret.where(~gap_too_large)
    px_ret = px_ret.where(~gap_too_large)

    oi_vol60 = oi_ret.rolling(vol_window).std(ddof=0)
    px_vol60 = px_ret.rolling(vol_window).std(ddof=0)
    # 분모 0 근접 스킵(스펙 명시) — px_vol60 의 60시간 표본 std 최소단위 근사(로그수익률이 사실상
    # 0인 극단적 무변동 구간)를 1e-6 미만으로 컷.
    denom_ok = px_vol60 > 1e-6
    vol_ratio = (oi_vol60 / px_vol60).where(denom_ok)

    z = rolling_zscore(vol_ratio.to_numpy(float), z_window)
    z_oi_only = rolling_zscore(oi_vol60.to_numpy(float), z_window)

    px_ret_4h_sum = px_ret.rolling(4).sum()

    atr14_15m = ind.atr(df15m, 14)

    return Signals(df1h=df1h, df15m=df15m, oi_ret=oi_ret, px_ret=px_ret, oi_vol60=oi_vol60,
                   px_vol60=px_vol60, vol_ratio=vol_ratio, z=z, z_oi_only=z_oi_only,
                   px_ret_4h_sum=px_ret_4h_sum, atr14_15m=atr14_15m,
                   oi_5m_count=df1h["oi_5m_count"], oi_raw_nan=df1h["oi_raw_nan"])
