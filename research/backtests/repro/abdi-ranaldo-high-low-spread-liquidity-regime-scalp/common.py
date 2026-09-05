"""Abdi-Ranaldo(AR) 고저-종가 유효스프레드 유동성 레짐 + 모멘텀/평균회귀 전환 — 공통 로더/신호.

스펙: research/strategies/abdi-ranaldo-high-low-spread-liquidity-regime-scalp.md
(⚠️발주 시점 스펙 파일이 저장소에 없어 백테스터가 발주 프롬프트를 근거로 사후 작성 — 스펙 파일
서두에 경위 명시함)
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

_repo_src = os.environ.get(
    "ABDIR_REPO_SRC",
    "/home/user/study/.claude/worktrees/agent-a2fbb751bd3675e81/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "ABDIR_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/abdiranaldo"))
DATA = SP / "data"
KLINES_1H_DIR = DATA / "klines_1h"
KLINES_15M_DIR = DATA / "klines_15m"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = (TAKER_FEE + SLIPPAGE) * 2  # 0.14%

# ------------------------------------------------------------- 파라미터(스펙 기본값)
AR_WINDOW = 20              # AR 계열곱 롤링창(1h봉)
PCTILE_WINDOW_DAYS = 20     # AR 스프레드 백분위 롤링 히스토리(일)
BARS_PER_DAY_1H = 24
PCTILE_ENTRY_LO = 0.20      # 모멘텀 게이트: AR 백분위 <= 20%
PCTILE_ENTRY_HI = 0.80      # 평균회귀 게이트: AR 백분위 >= 80%
BURST_LOOKBACK = 3          # 1h봉
BURST_MULT = 1.5
BB_LEN = 20
BB_STD = 2.0
TRAIL_MULT = 1.6
STOP_MULT = 1.0
MAX_HOLD_BARS_15M = 12      # 15m * 12 = 3h

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
    # ⚠️pandas 3.0.5 ns 통일(join/merge_asof/Timedelta 산술 오정렬 방지, 다수 선례 확인)
    out.index = out.index.as_unit("ns")
    return out


@lru_cache(maxsize=None)
def load_klines_1h(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_1H_DIR, symbol, "1h")


@lru_cache(maxsize=None)
def load_klines_15m(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_15M_DIR, symbol, "15m")


# ------------------------------------------------------------------ 유동성 추정치(계산)

def ar_ranaldo_spread(df1h: pd.DataFrame, window: int = AR_WINDOW
                      ) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Abdi-Ranaldo(2017) 재구성 추정치(스펙 §핵심 아이디어 참조).
    η_t = (lnH+lnL)/2, c_t = lnClose - η_t, product_t = c_t * c_{t-1}(causal),
    AR_cov(t) = rolling_mean(product, window), AR_spread(t) = sqrt(max(0, -4*AR_cov(t))).
    반환: (ar_spread, ar_cov, product) — product 는 음수비율 진단(사전폐기조건 b)에 사용."""
    h, l, c = df1h["high"], df1h["low"], df1h["close"]
    eta = (np.log(h) + np.log(l)) / 2.0
    c_dev = np.log(c) - eta
    product = c_dev * c_dev.shift(1)
    ar_cov = product.rolling(window).mean()
    ar_spread2 = (-4.0 * ar_cov).clip(lower=0.0)
    ar_spread = np.sqrt(ar_spread2)
    return ar_spread, ar_cov, product


def roll_spread(close: pd.Series, window: int = AR_WINDOW) -> pd.Series:
    """Roll(1984) 유효스프레드(참고: roll-implied-spread-liquidity-gate-scalp.md).
    dP_t = close_t - close_{t-1}, Cov(dP_t, dP_{t-1}) < 0 이면 S=2*sqrt(-Cov)/close*100, 아니면 0."""
    dp = close.diff()
    cov = dp.rolling(window).cov(dp.shift(1))
    spread2 = (-cov).clip(lower=0.0)
    spread = 2.0 * np.sqrt(spread2) / close * 100.0
    return spread


def corwin_schultz_spread(df1h: pd.DataFrame, ) -> pd.Series:
    """Corwin-Schultz(2012) 2봉 결합 고저 추정치(참고:
    corwin-schultz-liquidity-regime-momentum-scalp.md, β/γ/α/S 4단계).
    단일 인접 2봉 쌍(t-1,t) 기준 — 롤링 평균 없이 매 시점 즉시값(원 논문 정의 그대로),
    이후 상관 진단에서는 이 즉시값의 롤링평균(window=AR_WINDOW)을 사용한다."""
    h, l = df1h["high"], df1h["low"]
    ln_hl2 = (np.log(h / l)) ** 2
    beta = ln_hl2 + ln_hl2.shift(1)
    h2 = h.rolling(2).max()
    l2 = l.rolling(2).min()
    gamma = (np.log(h2 / l2)) ** 2
    sqrt2 = np.sqrt(2.0)
    denom = 3.0 - 2.0 * sqrt2
    alpha = ((np.sqrt(2.0 * beta) - np.sqrt(beta)) / denom) - np.sqrt(gamma / denom)
    s = 2.0 * (np.exp(alpha) - 1.0) / (1.0 + np.exp(alpha))
    s = s.clip(lower=0.0) * 100.0
    return s


def atr_pct(df1h: pd.DataFrame, period: int = 14) -> pd.Series:
    a = ind.atr(df1h, period)
    return a / df1h["close"] * 100.0


def realized_vol(close: pd.Series, window: int = AR_WINDOW) -> pd.Series:
    ret = np.log(close / close.shift(1))
    return ret.rolling(window).std(ddof=0) * 100.0


def hl_range_pct(df1h: pd.DataFrame, window: int = AR_WINDOW) -> pd.Series:
    rng = (df1h["high"] - df1h["low"]) / df1h["close"] * 100.0
    return rng.rolling(window).mean()


def rolling_pctile_of_last(x: pd.Series, window: int) -> pd.Series:
    """x(t)가 자신의 최근 window개(과거+현재) 히스토리 내에서 차지하는 백분위 순위."""
    return x.rolling(window).rank(pct=True)


# ------------------------------------------------------------------ 신호 구축

@dataclass
class Signals:
    df1h: pd.DataFrame
    df15m: pd.DataFrame
    ar_spread: pd.Series
    ar_cov: pd.Series
    ar_product: pd.Series      # 음수비율 진단용(c_t*c_{t-1})
    ar_pctile: pd.Series       # AR 스프레드의 pctile_window 롤링 백분위
    atrp: pd.Series            # ATR%(1h) — 대조군②/동어반복 진단
    atrp_pctile: pd.Series
    rv: pd.Series               # 실현변동성(1h) — 동어반복 진단
    hlrange: pd.Series          # HL range%(1h) — 동어반복 진단
    roll_sp: pd.Series          # Roll 스프레드(1h) — 동어반복 진단
    cs_sp: pd.Series            # Corwin-Schultz 스프레드(1h, 롤링평균) — 동어반복 진단
    atr14_1h: pd.Series
    bb_mid: pd.Series
    bb_upper: pd.Series
    bb_lower: pd.Series
    atr14_15m: pd.Series


def build_signals(symbol: str) -> Signals | None:
    df1h = load_klines_1h(symbol)
    df15m = load_klines_15m(symbol)
    if df1h.empty or df15m.empty:
        return None

    ar_spread, ar_cov, ar_product = ar_ranaldo_spread(df1h, AR_WINDOW)
    pctw = PCTILE_WINDOW_DAYS * BARS_PER_DAY_1H
    ar_pctile = rolling_pctile_of_last(ar_spread, pctw)

    atrp = atr_pct(df1h, 14)
    atrp_pctile = rolling_pctile_of_last(atrp.rolling(AR_WINDOW).mean(), pctw)

    rv = realized_vol(df1h["close"], AR_WINDOW)
    hlrange = hl_range_pct(df1h, AR_WINDOW)
    roll_sp = roll_spread(df1h["close"], AR_WINDOW)
    cs_inst = corwin_schultz_spread(df1h)
    cs_sp = cs_inst.rolling(AR_WINDOW).mean()

    atr14_1h = ind.atr(df1h, 14)
    bb_mid, bb_upper, bb_lower = ind.bollinger_bands(df1h["close"], BB_LEN, BB_STD)
    atr14_15m = ind.atr(df15m, 14)

    df1h.index = df1h.index.as_unit("ns")
    df15m.index = df15m.index.as_unit("ns")

    return Signals(df1h=df1h, df15m=df15m, ar_spread=ar_spread, ar_cov=ar_cov,
                   ar_product=ar_product, ar_pctile=ar_pctile, atrp=atrp,
                   atrp_pctile=atrp_pctile, rv=rv, hlrange=hlrange, roll_sp=roll_sp,
                   cs_sp=cs_sp, atr14_1h=atr14_1h, bb_mid=bb_mid, bb_upper=bb_upper,
                   bb_lower=bb_lower, atr14_15m=atr14_15m)


def load_all_signals(symbols=SYMBOLS) -> dict[str, Signals]:
    out = {}
    for s in symbols:
        sig = build_signals(s)
        if sig is not None:
            out[s] = sig
    return out


def with_ar_window(sig: Signals, window: int) -> Signals:
    """스윕용: ar_window 만 바꿔 AR 스프레드·백분위·계열곱을 재계산(나머지 지표는 재사용)."""
    ar_spread, ar_cov, ar_product = ar_ranaldo_spread(sig.df1h, window)
    pctw = PCTILE_WINDOW_DAYS * BARS_PER_DAY_1H
    ar_pctile = rolling_pctile_of_last(ar_spread, pctw)
    return replace(sig, ar_spread=ar_spread, ar_cov=ar_cov, ar_product=ar_product,
                  ar_pctile=ar_pctile)


def with_pctile_window(sig: Signals, days: int) -> Signals:
    """스윕용: 백분위 롤링 히스토리 길이만 바꿔 재계산."""
    pctw = days * BARS_PER_DAY_1H
    ar_pctile = rolling_pctile_of_last(sig.ar_spread, pctw)
    return replace(sig, ar_pctile=ar_pctile)


def with_bb_std(sig: Signals, std: float) -> Signals:
    """스윕용: 볼린저 std만 바꿔 재계산(평균회귀 서브모드 트리거)."""
    bb_mid, bb_upper, bb_lower = ind.bollinger_bands(sig.df1h["close"], BB_LEN, std)
    return replace(sig, bb_mid=bb_mid, bb_upper=bb_upper, bb_lower=bb_lower)
