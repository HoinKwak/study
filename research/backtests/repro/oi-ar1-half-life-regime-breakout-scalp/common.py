"""OI AR(1) 평균회귀 반감기(φ) 레짐 게이트 + Donchian 브레이크아웃 스캘프 — 공통 로더/신호.

스펙: research/strategies/oi-ar1-half-life-regime-breakout-scalp.md

⚠️타임프레임 해석: 스펙 헤더는 "15m 신호 / 1h 확인(φ 게이트, ...)"이라 적었으나, 「진입 규칙」
상세 절에서는 φ가 "15m봉 종가 시각 기준" OI 성장률에 대해 "매 15m마다 롤링 재추정"한다고 명시한다.
즉 φ 자체는 15m 해상도로 계산되고, "1h 확인"은 별도의 EMA20(1h) 기울기 필터를 가리킨다(「진입
규칙」 마지막 줄: "1h 확인: 1h EMA20 기울기가 진입 방향과 뚜렷하게 반대면 신호 스킵"). 본 구현은
상세 절(더 구체적인 규칙)을 따른다 — φ=15m 해상도, EMA20 기울기 확인=1h.
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
    "OIAR1_REPO_SRC",
    "/home/user/study/.claude/worktrees/agent-a8f695a5d23809096/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "OIAR1_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiar1hl"))
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

# ------------------------------------------------------------- 파라미터(스펙 기본값)
PHI_WINDOW_DAYS = 30       # 15m봉 30일 = 2880봉
PHI_PCTILE_WINDOW_DAYS = 90  # 90일 = 8640봉
PHI_PCTILE_TH = 0.67
DONCHIAN_LB = 20
DONCHIAN_MID_LB = 10
ATR_TRAIL_MULT = 1.8
ATR_STOP_MULT = 1.2
MAX_HOLD_BARS = 24          # 15m * 24 = 6h
BARS_PER_DAY_15M = 96

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
    # ⚠️0-fill 결측 placeholder(선례 확인): 실제 OI 는 0이 될 수 없음 → 명시적 NaN 처리.
    out.loc[out["sum_open_interest"] <= 0, "sum_open_interest"] = np.nan
    return out


def oi_15m_from_5m(m5: pd.DataFrame) -> pd.DataFrame:
    """5분 OI → 15m봉 마감시점 값(resample('15min').last(), 빈 bin 은 NaN → 명시적 ffill).
    ffill 여부·5분 표본수를 별도 컬럼으로 남겨 품질 추적."""
    if m5.empty:
        return pd.DataFrame()
    s = m5["sum_open_interest"]
    last = s.resample("15min", label="left", closed="left").last()
    cnt = s.resample("15min", label="left", closed="left").count()
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


def rolling_ar1_phi(x: pd.Series, window: int) -> pd.Series:
    """AR(1) OLS 계수(φ)를 롤링 재추정: x(t) = c + φ*x(t-1) + ε(t).
    슬로프(φ) = Cov(x(t), x(t-1)) / Var(x(t-1)) (절편 c 는 슬로프 계산에 영향 없음, 표준 OLS
    단순선형회귀 공식). pandas rolling.cov/var 는 증분 알고리즘이라 O(n) — window*n 루프보다
    훨씬 빠르다(실측 확인: n=160,000·window=2880 에서 <0.1초)."""
    x_lag = x.shift(1)
    cov = x.rolling(window).cov(x_lag)
    var = x_lag.rolling(window).var(ddof=1)
    phi = cov / var
    phi = phi.where(var > 1e-18)
    return phi


def rolling_pctile_of_last(x: pd.Series, window: int) -> pd.Series:
    """x(t) 가 자신의 최근 window 개(과거+현재) 히스토리 내에서 차지하는 백분위 순위.
    pd.Series.rolling(window).rank(pct=True) 는 각 윈도우의 '마지막 값'의 백분위 순위를 반환
    (검증: window=[a,b,c,d,e] 일 때 rank(pct=True) 는 e 의 순위/window — 스펙이 요구하는
    "phi(t)의 최근 90일 롤링 히스토리 대비 백분위"와 정확히 일치)."""
    return x.rolling(window).rank(pct=True)


# ------------------------------------------------------------------ 신호 구축

@dataclass
class Signals:
    df1h: pd.DataFrame        # 1h klines
    df15m: pd.DataFrame       # 15m klines + oi
    oi_growth: pd.Series      # 15m OI 로그성장률
    phi: pd.Series            # AR(1) φ (30일 롤링)
    phi_pctile: pd.Series     # φ 의 90일 롤링 백분위
    oi_z: pd.Series           # 대조군②: OI 성장률의 30일 롤링 z-score
    oi_z_pctile: pd.Series    # 대조군②: oi_z 의 90일 롤링 백분위(φ 게이트와 동일 메커니즘)
    oi_change_stdev: pd.Series  # 전제일관성 점검용: OI 성장률의 30일 롤링 표준편차
    donch_upper: pd.Series    # 20봉 Donchian 상단(자기 제외, shift(1) 적용됨)
    donch_lower: pd.Series    # 20봉 Donchian 하단(자기 제외)
    donch_mid10: pd.Series    # 10봉 Donchian 중간선(자기 제외)
    atr14_15m: pd.Series      # ATR(14, 15m)
    ema20_1h: pd.Series       # EMA20(1h)
    atr14_1h: pd.Series       # ATR(14, 1h) — EMA 기울기 정규화용
    oi_5m_count: pd.Series
    oi_raw_nan: pd.Series


def build_signals(symbol: str) -> Signals | None:
    df1h = load_klines_1h(symbol)
    df15m = load_klines_15m(symbol)
    if df1h.empty or df15m.empty:
        return None
    m5 = load_metrics_5m(symbol)
    if m5.empty:
        return None
    oi15 = oi_15m_from_5m(m5)
    df15m = df15m.join(oi15, how="left")
    # ⚠️join 이 인덱스 해상도를 조용히 업캐스트할 수 있어(ms/us/ns 혼재 함정, 다수 선례 확인) 재통일.
    df15m.index = df15m.index.as_unit("ns")
    df1h.index = df1h.index.as_unit("ns")

    # 시간외 갭 마스킹: 인덱스 간격이 15m 를 초과하면 그 시점의 성장률을 NaN 처리
    idx = df15m.index
    gap_min = idx.to_series().diff().dt.total_seconds() / 60.0
    gap_too_large = (gap_min > 15.0 + 1e-6).to_numpy()

    oi_growth = np.log(df15m["oi"] / df15m["oi"].shift(1))
    oi_growth = oi_growth.where(~gap_too_large)

    win_phi = PHI_WINDOW_DAYS * BARS_PER_DAY_15M
    win_pct = PHI_PCTILE_WINDOW_DAYS * BARS_PER_DAY_15M

    phi = rolling_ar1_phi(oi_growth, win_phi)
    phi_pctile = rolling_pctile_of_last(phi, win_pct)

    oi_z = pd.Series(rolling_zscore(oi_growth.to_numpy(float), win_phi), index=df15m.index)
    oi_z_pctile = rolling_pctile_of_last(oi_z, win_pct)

    oi_change_stdev = oi_growth.rolling(win_phi).std(ddof=0)

    high, low, close = df15m["high"], df15m["low"], df15m["close"]
    donch_upper = high.shift(1).rolling(DONCHIAN_LB).max()
    donch_lower = low.shift(1).rolling(DONCHIAN_LB).min()
    mid_hi = high.shift(1).rolling(DONCHIAN_MID_LB).max()
    mid_lo = low.shift(1).rolling(DONCHIAN_MID_LB).min()
    donch_mid10 = (mid_hi + mid_lo) / 2.0

    atr14_15m = ind.atr(df15m, 14)
    ema20_1h = ind.ema(df1h["close"], 20)
    atr14_1h = ind.atr(df1h, 14)

    return Signals(df1h=df1h, df15m=df15m, oi_growth=oi_growth, phi=phi, phi_pctile=phi_pctile,
                   oi_z=oi_z, oi_z_pctile=oi_z_pctile, oi_change_stdev=oi_change_stdev,
                   donch_upper=donch_upper, donch_lower=donch_lower, donch_mid10=donch_mid10,
                   atr14_15m=atr14_15m, ema20_1h=ema20_1h, atr14_1h=atr14_1h,
                   oi_5m_count=df15m["oi_5m_count"], oi_raw_nan=df15m["oi_raw_nan"])


def with_donchian_lb(sig: Signals, lb: int, mid_lb: int = DONCHIAN_MID_LB) -> Signals:
    """⚠️자체발견: RunConfig.donchian_lb 는 사전계산·캐시된 Signals(sigs.pkl) 에 반영되지 않아
    스윕에서 무시되는 죽은 파라미터였다(20/15/30 결과가 완전히 동일 — 스윕 1차 실행에서 적발).
    Donchian 상단/하단/중간선만 새 lb 로 재계산해 나머지(φ 등, lb 와 무관)는 재사용한다."""
    high, low = sig.df15m["high"], sig.df15m["low"]
    donch_upper = high.shift(1).rolling(lb).max()
    donch_lower = low.shift(1).rolling(lb).min()
    mid_hi = high.shift(1).rolling(mid_lb).max()
    mid_lo = low.shift(1).rolling(mid_lb).min()
    donch_mid10 = (mid_hi + mid_lo) / 2.0
    return replace(sig, donch_upper=donch_upper, donch_lower=donch_lower, donch_mid10=donch_mid10)
