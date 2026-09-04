"""테이커 매수체결대금/OI명목가치 순간비율 극단 소진 반전 스캘프 — 공통 데이터 로더 + 신호 계산.

스펙: research/strategies/taker-buy-notional-oi-ratio-exhaustion-fade-scalp.md

⚠️ scratchpad/모듈 네임스페이스를 다른 백테스터(oivolratio)와 절대 겹치지 않게 "tbnoifade"로
고유하게 잡았다. 데이터는 klines(15m/1h)·metrics 5분 원자료를 그대로 재사용(동일 7종목·동일
기간의 불변 과거 덤프라 다른 백테스터가 이미 받아둔 것을 복사만 해서 재다운로드 시간을 아꼈음.
쓰기는 전혀 하지 않고 읽기 전용으로 자신의 scratch 디렉터리에 복사한 사본만 사용).
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

_repo_src = os.environ.get("TBOI_REPO_SRC", "/home/user/study/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "TBOI_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/tbnoifade"))
DATA = SP / "data"
KLINES_15M_DIR = DATA / "klines_15m"
KLINES_1H_DIR = DATA / "klines_1h"
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

def _load_klines_raw(dirpath: Path, symbol: str, tf: str) -> pd.DataFrame:
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
    ot = out["open_time"]
    is_us = ot.abs() > 10**14  # ms epoch 는 13자리 — 이보다 크면 us 로 판단해 통일(단위사고 회피)
    if is_us.any():
        out.loc[is_us, "open_time"] = out.loc[is_us, "open_time"] // 1000
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume",
              "taker_buy_volume", "taker_buy_quote_volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume", "quote_volume",
              "taker_buy_volume", "taker_buy_quote_volume"]]
    # ⚠️ ms/us/ns 함정: pandas 3.0.5 는 unit="ms" 결과를 항상 ns 로 승격하지 않는다. join/merge_asof/
    # Timedelta 산술에서 조용히 오정렬될 수 있어 로더가 끝날 때마다 명시적으로 ns 통일한다.
    out.index = out.index.as_unit("ns")
    return out


@lru_cache(maxsize=None)
def load_klines_15m(symbol: str) -> pd.DataFrame:
    return _load_klines_raw(KLINES_15M_DIR, symbol, "15m")


@lru_cache(maxsize=None)
def load_klines_1h(symbol: str) -> pd.DataFrame:
    return _load_klines_raw(KLINES_1H_DIR, symbol, "1h")


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
        if "sum_open_interest_value" not in df.columns:
            continue
        parts.append(df[["create_time", "symbol", "sum_open_interest_value"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out.index = out.index.as_unit("ns")  # klines(ns)와 join 시 오정렬 방지(선행 라운드 실측 버그 재발 방지)
    out["sum_open_interest_value"] = pd.to_numeric(out["sum_open_interest_value"], errors="coerce")
    # 0-fill placeholder 방지: OI 명목가치가 0/음수일 수 없으므로 명시적으로 NaN 처리
    out.loc[out["sum_open_interest_value"] <= 0, "sum_open_interest_value"] = np.nan
    return out


def oi_value_15m_from_5m(m5: pd.DataFrame) -> pd.DataFrame:
    """5분 OI 명목가치 → 15분봉 마지막 관측치(resample('15min').last()), 결측은 ffill.
    ffill 적용 여부·5분 표본수를 별도 컬럼으로 남겨 품질 추적."""
    if m5.empty:
        return pd.DataFrame()
    s = m5["sum_open_interest_value"]
    last = s.resample("15min", label="left", closed="left").last()
    cnt = s.resample("15min", label="left", closed="left").count()
    filled = last.ffill()
    out = pd.DataFrame({"oi_value": filled, "oi_raw_nan": last.isna(), "oi_5m_count": cnt})
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
    symbol: str
    df15m: pd.DataFrame          # open,high,low,close,volume,quote_volume,taker_buy_volume,
                                  # taker_buy_quote_volume + oi_value(ffill) + body_ratio
    df1h: pd.DataFrame           # open,high,low,close + ema20
    flow_buy_ratio: pd.Series
    flow_sell_ratio: pd.Series
    z_buy: np.ndarray            # flow_buy_ratio 의 z_window 롤링 z-score (숏 신호)
    z_sell: np.ndarray           # flow_sell_ratio 의 z_window 롤링 z-score (롱 신호)
    body_ratio: pd.Series
    atr14_15m: pd.Series
    # ---- 대조군/동어반복 점검용 부가 시리즈 ----
    flow_total_ratio: pd.Series      # quote_volume/oi_value (대조군① 분자)
    z_total: np.ndarray
    taker_buy_frac: pd.Series        # taker_buy_quote_volume/quote_volume (대조군① 방향판정)
    vol24h: pd.Series                # 24h(96봉) 롤링 총 거래대금(대조군② 분모)
    flow_vol24h_buy_ratio: pd.Series
    flow_vol24h_sell_ratio: pd.Series
    z_vol24h_buy: np.ndarray
    z_vol24h_sell: np.ndarray
    z_volume: np.ndarray             # 캔들 거래량(quote_volume) 자체의 z-score(동어반복 점검용)
    oi_pct_change: pd.Series         # OI 명목가치 변화율(동어반복 점검용, ΔOI%)
    # ---- 1h 확인 ----
    completed_1h_idx: np.ndarray     # 15m 각 봉 '시가 시점'까지 완결된 1h 봉 개수(causal 매핑)
    ema20_1h_slope: np.ndarray       # 1h EMA20 의 ema_lookback 봉 전 대비 변화율(%), 1h 인덱스 기준


NS_1H = np.timedelta64(1, "h").astype("timedelta64[ns]").astype("int64")


def _completed_1h_counts(df1h_index: pd.DatetimeIndex, ts15_ns: np.ndarray) -> np.ndarray:
    """15m 타임스탬프(ns, 봉 시가 시점) 각각에 대해 '그 시각까지 완결된 1h 봉 개수'."""
    ends = df1h_index.asi8 + NS_1H
    return np.searchsorted(ends, ts15_ns, side="right")


def build_signals(symbol: str, z_window: int = 200, vol24h_bars: int = 96,
                  ema_lookback_1h: int = 3) -> Signals | None:
    df15m = load_klines_15m(symbol)
    df1h = load_klines_1h(symbol)
    if df15m.empty or df1h.empty:
        return None
    m5 = load_metrics_5m(symbol)
    if m5.empty:
        return None
    oi15 = oi_value_15m_from_5m(m5)
    df15m = df15m.join(oi15, how="left")
    # join 이 서로 다른 해상도 인덱스를 조용히 us 로 업캐스트할 수 있음(선행 라운드 실측 확인
    # 버그) — join 직후 다시 ns 로 명시 통일.
    df15m.index = df15m.index.as_unit("ns")
    df1h.index = df1h.index.as_unit("ns")
    df15m["oi_value"] = df15m["oi_value"].ffill()

    body_ratio = ((df15m["close"] - df15m["open"]).abs()
                  / (df15m["high"] - df15m["low"]).replace(0.0, np.nan))

    oi_ok = df15m["oi_value"] > 0
    flow_buy_ratio = (df15m["taker_buy_quote_volume"] / df15m["oi_value"]).where(oi_ok)
    flow_sell_ratio = ((df15m["quote_volume"] - df15m["taker_buy_quote_volume"])
                       / df15m["oi_value"]).where(oi_ok)
    flow_total_ratio = (df15m["quote_volume"] / df15m["oi_value"]).where(oi_ok)

    z_buy = rolling_zscore(flow_buy_ratio.to_numpy(float), z_window)
    z_sell = rolling_zscore(flow_sell_ratio.to_numpy(float), z_window)
    z_total = rolling_zscore(flow_total_ratio.to_numpy(float), z_window)

    taker_buy_frac = (df15m["taker_buy_quote_volume"]
                      / df15m["quote_volume"].replace(0.0, np.nan))

    vol24h = df15m["quote_volume"].rolling(vol24h_bars).sum()
    vol24h_ok = vol24h > 0
    flow_vol24h_buy_ratio = (df15m["taker_buy_quote_volume"] / vol24h).where(vol24h_ok)
    flow_vol24h_sell_ratio = ((df15m["quote_volume"] - df15m["taker_buy_quote_volume"])
                              / vol24h).where(vol24h_ok)
    z_vol24h_buy = rolling_zscore(flow_vol24h_buy_ratio.to_numpy(float), z_window)
    z_vol24h_sell = rolling_zscore(flow_vol24h_sell_ratio.to_numpy(float), z_window)

    z_volume = rolling_zscore(df15m["quote_volume"].to_numpy(float), z_window)
    oi_pct_change = df15m["oi_value"].pct_change()

    atr14_15m = ind.atr(df15m, 14)

    ema20_1h = ind.ema(df1h["close"], 20)
    ema_prev = ema20_1h.shift(ema_lookback_1h)
    ema_slope = ((ema20_1h - ema_prev) / ema_prev.replace(0.0, np.nan)).to_numpy(float)

    completed_1h_idx = _completed_1h_counts(df1h.index, df15m.index.asi8)

    return Signals(symbol=symbol, df15m=df15m, df1h=df1h, flow_buy_ratio=flow_buy_ratio,
                   flow_sell_ratio=flow_sell_ratio, z_buy=z_buy, z_sell=z_sell,
                   body_ratio=body_ratio, atr14_15m=atr14_15m,
                   flow_total_ratio=flow_total_ratio, z_total=z_total,
                   taker_buy_frac=taker_buy_frac, vol24h=vol24h,
                   flow_vol24h_buy_ratio=flow_vol24h_buy_ratio,
                   flow_vol24h_sell_ratio=flow_vol24h_sell_ratio,
                   z_vol24h_buy=z_vol24h_buy, z_vol24h_sell=z_vol24h_sell,
                   z_volume=z_volume, oi_pct_change=oi_pct_change,
                   completed_1h_idx=completed_1h_idx, ema20_1h_slope=ema_slope)
