"""체결건수(count) 방향 스트릭 지속 브레이크아웃 스윙 — 공통 데이터 로더 + 지표 계산.

스펙: research/strategies/trade-count-directional-streak-breakout-swing.md
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

# 격리 git worktree(tcstreak_wt)에서 실행. REPO_SRC 환경변수로 저장소 src 경로 지정 가능.
_repo_src = os.environ.get(
    "TCSTREAK_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

# 원본 데이터(klines CSV)는 scratchpad 에 있으며 git 에는 포함되지 않는다(대용량).
# 재현 시 TCSTREAK_SCRATCH 환경변수로 지정하거나 dl_klines.sh 를 재실행해 받는다.
SP = Path(os.environ.get(
    "TCSTREAK_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/tcstreak"))
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


# ------------------------------------------------------------------ 로더

def _load_klines(symbol: str, tf_dir: str) -> pd.DataFrame:
    files = sorted(DATA.glob(f"{tf_dir}/{symbol}-*-*.csv"))
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
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume", "count"]:
        out[c] = out[c].astype(float)
    return out[["open", "high", "low", "close", "volume", "quote_volume", "count"]]


@lru_cache(maxsize=None)
def load_klines_4h(symbol: str) -> pd.DataFrame:
    return _load_klines(symbol, "klines_4h")


@lru_cache(maxsize=None)
def load_klines_1d(symbol: str) -> pd.DataFrame:
    return _load_klines(symbol, "klines_1d")


# ------------------------------------------------------------------ 지표 계산

def donchian(df: pd.DataFrame, period: int) -> tuple[np.ndarray, np.ndarray]:
    """직전(shift 1봉) period 봉 고점/저점(현재봉 미포함, 룩어헤드 방지)."""
    hi = df["high"].rolling(period).max().shift(1).to_numpy(float)
    lo = df["low"].rolling(period).min().shift(1).to_numpy(float)
    return hi, lo


def count_streak(count: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """count(t) 방향 스트릭. up(t)=1 if count(t)>count(t-1). streak_up/streak_down 반환(정수봉수).
    count(t)==count(t-1)(동률)은 streak 를 리셋(엄격 부등호)."""
    n = len(count)
    streak_up = np.zeros(n, dtype=float)
    streak_down = np.zeros(n, dtype=float)
    streak_up[:] = np.nan
    streak_down[:] = np.nan
    cur_up = 0
    cur_down = 0
    for i in range(n):
        if i == 0 or not np.isfinite(count[i]) or not np.isfinite(count[i - 1]):
            cur_up = 0
            cur_down = 0
            streak_up[i] = np.nan
            streak_down[i] = np.nan
            continue
        if count[i] > count[i - 1]:
            cur_up += 1
            cur_down = 0
        elif count[i] < count[i - 1]:
            cur_down += 1
            cur_up = 0
        else:
            cur_up = 0
            cur_down = 0
        streak_up[i] = cur_up
        streak_down[i] = cur_down
    return streak_up, streak_down


def ema1d_on_4h(df4h: pd.DataFrame, df1d: pd.DataFrame, period: int) -> pd.Series:
    """1d EMA(period) 를 4h 시그널 인덱스에 매핑. 룩어헤드 방지: 1d 봉은 그 봉이 완결(종가 확정)
    되어야 사용 가능 — 1d 봉 t(개장 00:00 UTC)의 EMA 값은 [t+1일 00:00, t+2일 00:00) 구간의
    4h 봉들에만 적용한다. ⚠️`pd.Timedelta`+`merge_asof`가 pandas 3.x 에서 ms→us 조용한
    업캐스트를 일으키는 함정이 있어(과거 라운드에서 반복 재현) 여기서는 정수 ns epoch 기반
    `np.searchsorted`로 직접 구현해 그 함정을 원천 차단한다."""
    ema1d = ind.ema(df1d["close"], period)
    # ⚠️ .asi8 은 인덱스 dtype 의 저장단위(ms 일 수도 ns 일 수도)를 그대로 반환하므로, 두 인덱스가
    # 항상 같은 dtype 이라는 보장이 없으면 함정. astype("datetime64[ns, UTC]")로 ns 단위를
    # 명시적으로 강제한 뒤 asi8 을 써서 단위사고를 원천 차단한다.
    idx1d_ns = ema1d.index.astype("datetime64[ns, UTC]").asi8
    idx4h_ns = df4h.index.astype("datetime64[ns, UTC]").asi8
    # 1d 봉 t 종료(=t+1일 00:00) 시각 = 그 EMA 값을 사용 가능해지는 시각(ns epoch, 명시)
    avail_ns = idx1d_ns + np.int64(24 * 3600 * 1_000_000_000)
    ema_vals = ema1d.to_numpy(float)
    # 각 4h 시그널 시각 이하(<=)의 마지막 '사용 가능' 1d EMA 를 찾음
    pos = np.searchsorted(avail_ns, idx4h_ns, side="right") - 1
    out = np.full(len(idx4h_ns), np.nan)
    valid = pos >= 0
    out[valid] = ema_vals[pos[valid]]
    return pd.Series(out, index=df4h.index)


@dataclass
class Signals:
    df: pd.DataFrame            # 4h klines
    count: np.ndarray
    streak_up: np.ndarray
    streak_down: np.ndarray
    don_hi: np.ndarray
    don_lo: np.ndarray
    atr14: pd.Series
    ema1d: pd.Series
    quote_volume: pd.Series
    roc: pd.Series               # 가격 모멘텀(ROC, N=streak_th) — 동어반복 점검용
    count_zscore: pd.Series      # count 60봉 롤링 z-score(동어반복 점검용 보조)


def build_signals(symbol: str, donchian_period: int = 20, ema_period: int = 50,
                  streak_th: int = 5) -> Signals | None:
    df4h = load_klines_4h(symbol)
    df1d = load_klines_1d(symbol)
    if df4h.empty or df1d.empty:
        return None
    count = df4h["count"].to_numpy(float)
    streak_up, streak_down = count_streak(count)
    don_hi, don_lo = donchian(df4h, donchian_period)
    atr14 = ind.atr(df4h, 14)
    ema1d = ema1d_on_4h(df4h, df1d, ema_period)
    roc = df4h["close"].pct_change(streak_th)
    cnt_s = df4h["count"]
    count_zscore = (cnt_s - cnt_s.rolling(60).mean()) / cnt_s.rolling(60).std()
    return Signals(df=df4h, count=count, streak_up=streak_up, streak_down=streak_down,
                   don_hi=don_hi, don_lo=don_lo, atr14=atr14, ema1d=ema1d,
                   quote_volume=df4h["quote_volume"], roc=roc, count_zscore=count_zscore)
