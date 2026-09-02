"""공통 데이터 로딩·지표 계산 — BTC 웍(wick) 리젝션의 알트 바스켓 동시확인 브레드스 페이드."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

WORKTREE = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(WORKTREE / "src"))
from crypto_trader.signals import indicators as _ind  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
BTC = "BTCUSDT"
ALTS = [s for s in SYMBOLS if s != BTC]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

ROUND_TRIP_COST = 0.0014  # 왕복 수수료+슬리피지

# 스펙 파라미터(기본값)
WICK_BODY_MULT = 1.5
WICK_ATR_MULT = 1.0
CLOSE_LOC_TH = 0.4
CONFIRM_N_TH = 4
RR_TARGET = 1.3
SL_BUFFER = 0.2
MAX_HOLD = 8
SWING_LOOKBACK = 10


def _load(symbol: str) -> pd.DataFrame:
    fn = DATA / f"{symbol}_klines_15m.parquet"
    df = pd.read_parquet(fn)
    # ⚠️ ms/us 함정: unit="ms" 파싱 후 ns 로 명시 통일(다른 리포트와 동일 관례).
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True).astype(
        "datetime64[ns, UTC]")
    df = df.set_index("open_time").sort_index()
    df = df[~df.index.duplicated(keep="first")]
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = df[c].astype(float)
    return df


def wick_features(df: pd.DataFrame) -> pd.DataFrame:
    """upper_wick/lower_wick/body/range/close_loc + ATR(15m,14, 프레임워크 재사용)."""
    o, h, l, c = df["open"], df["high"], df["low"], df["close"]
    out = pd.DataFrame(index=df.index)
    out["open"] = o
    out["high"] = h
    out["low"] = l
    out["close"] = c
    out["upper_wick"] = h - np.maximum(o, c)
    out["lower_wick"] = np.minimum(o, c) - l
    out["body"] = (c - o).abs()
    out["range"] = h - l
    out["close_loc"] = np.where(out["range"] > 0, (c - l) / out["range"], np.nan)
    out["atr"] = _ind.atr(df, period=14)
    return out


def wick_signals(feat: pd.DataFrame, wick_body_mult: float = WICK_BODY_MULT,
                  wick_atr_mult: float = WICK_ATR_MULT,
                  close_loc_th: float = CLOSE_LOC_TH) -> pd.DataFrame:
    """is_upper(약세, 상단 웍)/is_lower(강세, 하단 웍) 불리언 컬럼 추가."""
    body_safe = feat["body"].replace(0.0, np.nan)
    is_upper = (
        (feat["upper_wick"] >= wick_body_mult * body_safe)
        & (feat["upper_wick"] >= wick_atr_mult * feat["atr"])
        & (feat["close_loc"] <= close_loc_th)
        & (feat["range"] > 0)
    ).fillna(False)
    is_lower = (
        (feat["lower_wick"] >= wick_body_mult * body_safe)
        & (feat["lower_wick"] >= wick_atr_mult * feat["atr"])
        & (feat["close_loc"] >= 1.0 - close_loc_th)
        & (feat["range"] > 0)
    ).fillna(False)
    out = feat.copy()
    out["is_upper"] = is_upper
    out["is_lower"] = is_lower
    return out


def load_all() -> dict[str, pd.DataFrame]:
    """symbol -> wick_signals 적용된 15m 프레임(전체 이력, 인덱스 원본 그대로)."""
    out = {}
    for sym in SYMBOLS:
        df = _load(sym)
        feat = wick_features(df)
        sig = wick_signals(feat)
        out[sym] = sig
    return out


def pf_r(series: pd.Series) -> float:
    pos = series[series > 0].sum()
    neg = -series[series < 0].sum()
    if neg == 0:
        return float("inf") if pos > 0 else float("nan")
    return pos / neg


def t_stat(series: pd.Series) -> float:
    n = len(series)
    if n < 2:
        return float("nan")
    sd = series.std(ddof=1)
    if sd == 0:
        return float("nan")
    return series.mean() / (sd / np.sqrt(n))


def win_rate(series: pd.Series) -> float:
    n = len(series)
    if n == 0:
        return float("nan")
    return float((series > 0).sum()) / n


def summarize(df: pd.DataFrame, col: str = "net_R") -> dict:
    if len(df) == 0:
        return {"n": 0, "pf": float("nan"), "t": float("nan"), "win_rate": float("nan"),
                "mean_R": float("nan"), "sum_R": float("nan")}
    s = df[col]
    return {"n": int(len(df)), "pf": pf_r(s), "t": t_stat(s), "win_rate": win_rate(s),
            "mean_R": float(s.mean()), "sum_R": float(s.sum())}
