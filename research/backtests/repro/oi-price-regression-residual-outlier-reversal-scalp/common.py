"""OI-가격 회귀잔차 아웃라이어 반전 스캘프 — 공통 데이터 로더 + 회귀/잔차 계산.

스펙: research/strategies/oi-price-regression-residual-outlier-reversal-scalp.md
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
    "OIRESID_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))  # .../research/backtests/repro/<slug>/common.py -> repo/src
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "OIRESID_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiresid"))
DATA = SP / "data"
# metrics(5분 OI) 원본은 이전 라운드(oiskew)가 이미 전 구간·7종목 CSV 로 추출해둔 것을 읽기전용으로
# 재사용한다(재다운로드 회피 — 동일 필드·동일 기간·동일 유니버스, "캐시 재사용 타당성" 선례에 부합).
METRICS_DIR = Path(os.environ.get(
    "OIRESID_METRICS_DIR",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiskew/data/metrics"))

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

@lru_cache(maxsize=None)
def load_klines_1h(symbol: str) -> pd.DataFrame:
    files = sorted(DATA.glob(f"klines/{symbol}-1h-*.csv"))
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
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    return out[["open", "high", "low", "close", "volume", "quote_volume"]]


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
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    # ⚠️데이터 결함(자체 발견): sum_open_interest 가 간헐적으로 0(또는 음수)인 "0-fill" placeholder
    # 시점이 존재(예: BTC 2024-07-09~15 여러 시간대) — 실제 OI 가 0이 될 수 없으므로 명백한 결측
    # placeholder. isna() 는 이를 못 잡는다(값 자체가 0.0이지 NaN 이 아님) — 명시적으로 <=0 을
    # NaN 처리해 pct_change 폭주(다음 값에서 -100%→+inf 스파이크)를 원천 차단.
    out.loc[out["sum_open_interest"] <= 0, "sum_open_interest"] = np.nan
    return out


def oi_1h_from_5m(m5: pd.DataFrame) -> pd.DataFrame:
    """5분 OI → 1h 봉 마감시점 값. resample('1h').last() 는 빈 bin 에 NaN 을 반환하므로(직전값
    forward-fill 아님, 이전 라운드 실측 확인) 스펙 방법론(resample('1h').last().ffill())대로 명시적
    ffill 을 적용한다. ffill 이 적용된 bar 수를 별도 컬럼(`oi_5m_count`==0)으로 남겨 데이터 품질을
    추적한다. 과도한 staleness(연속 24시간 초과 ffill)는 진단에서 별도 경고."""
    if m5.empty:
        return pd.DataFrame()
    s = m5["sum_open_interest"]
    last = s.resample("1h", label="left", closed="left").last()
    cnt = s.resample("1h", label="left", closed="left").count()
    filled = last.ffill()
    out = pd.DataFrame({"oi": filled, "oi_raw_nan": last.isna(), "oi_5m_count": cnt})
    return out


# ------------------------------------------------------------------ 회귀·잔차

def rolling_ols_residual(x: np.ndarray, y: np.ndarray, window: int, var_eps: float = 1e-10
                         ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """롤링(window, 현재 bar 포함) 단순 OLS: y = a + b*x. (beta, alpha, residual) 반환.

    pandas rolling cov/var(둘 다 O(n) 벡터화, `Series.rolling().cov()`/`.var()`) 사용 — numpy.polyfit
    반복보다 수치적으로 안정적이고 빠름. var(x)가 var_eps 미만이면(가격이 사실상 무변동) beta=0 으로
    강제해 분모≈0 폭주를 차단하고(스펙이 우려한 "상관 0"과는 다른 실패모드 — 상관 0 은 cov≈0 이라
    var(x)>0 이면 beta 는 정상적으로 0에 수렴할 뿐 폭주하지 않는다. 여기서 막는 것은 x 자체가
    상수에 가까운 진짜 특이 경우), NaN 이 window 내 하나라도 있으면 그 시점은 NaN.
    """
    xs = pd.Series(x)
    ys = pd.Series(y)
    cov_xy = xs.rolling(window).cov(ys)
    var_x = xs.rolling(window).var()
    mean_x = xs.rolling(window).mean()
    mean_y = ys.rolling(window).mean()
    beta = np.where(var_x.to_numpy() > var_eps, (cov_xy / var_x).to_numpy(), 0.0)
    # NaN 전파: cov_xy/var_x/mean 중 하나라도 NaN 이면 그 시점은 무효
    invalid = cov_xy.isna() | var_x.isna() | mean_x.isna() | mean_y.isna()
    beta = np.where(invalid.to_numpy(), np.nan, beta)
    alpha = mean_y.to_numpy() - beta * mean_x.to_numpy()
    resid = y - (alpha + beta * x)
    return beta, alpha, resid


def rolling_zscore(x: np.ndarray, window: int) -> np.ndarray:
    xs = pd.Series(x)
    m = xs.rolling(window).mean()
    sd = xs.rolling(window).std(ddof=0)
    z = (xs - m) / sd
    z = z.where(sd > 1e-12)
    return z.to_numpy()


@dataclass
class Signals:
    df: pd.DataFrame          # 1h klines
    d_price_pct: pd.Series    # Δprice%
    d_oi_pct: pd.Series       # ΔOI%
    beta: np.ndarray
    alpha: np.ndarray
    residual: np.ndarray
    z_resid: np.ndarray       # 잔차 z-score (핵심 신호)
    z_oi: np.ndarray          # 순수 OI z-score (핵심 대조군)
    atr14: pd.Series
    oi_5m_count: pd.Series
    oi_raw_nan: pd.Series


def build_signals(symbol: str, window: int = 60) -> Signals | None:
    df = load_klines_1h(symbol)
    if df.empty:
        return None
    m5 = load_metrics_5m(symbol)
    if m5.empty:
        return None
    oi1h = oi_1h_from_5m(m5)
    df = df.join(oi1h, how="left")
    d_price_pct = df["close"].pct_change() * 100.0
    d_oi_pct = df["oi"].pct_change() * 100.0
    beta, alpha, resid = rolling_ols_residual(d_price_pct.to_numpy(float),
                                              d_oi_pct.to_numpy(float), window)
    z_resid = rolling_zscore(resid, window)
    z_oi = rolling_zscore(d_oi_pct.to_numpy(float), window)
    atr14 = ind.atr(df, 14)
    return Signals(df=df, d_price_pct=d_price_pct, d_oi_pct=d_oi_pct, beta=beta, alpha=alpha,
                   residual=resid, z_resid=z_resid, z_oi=z_oi, atr14=atr14,
                   oi_5m_count=df["oi_5m_count"], oi_raw_nan=df["oi_raw_nan"])
