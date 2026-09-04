"""알트 OI성장률의 BTC가격 베타 다이버전스 로테이션 — 공통 데이터 로더 + 회귀/잔차 계산.

스펙: research/strategies/alt-btc-oi-growth-beta-divergence-rotation-swing.md

데이터: data.binance.vision futures/um monthly klines(1d/4h) + daily metrics(sum_open_interest, 5분).
IS/OOS 경계·비용은 프레임워크 규약(research/backtests/*.md 다수 선례) 그대로 따른다.
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
    "ALTOIBETA_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))  # .../research/backtests/repro/<slug>/common.py -> repo/src
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "ALTOIBETA_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/altoibeta"))
DATA = SP / "data"

BTC = "BTCUSDT"
ALT_SYMBOLS = ["ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
ALL_SYMBOLS = [BTC] + ALT_SYMBOLS

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
def load_klines(symbol: str, tf: str) -> pd.DataFrame:
    files = sorted(DATA.glob(f"klines{tf}/{symbol}-{tf}-*.csv"))
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
    files = sorted(DATA.glob(f"metrics/{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "sum_open_interest"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    # 0-fill 결측 placeholder 방지(선례: OI 가 실제로 0이 될 수 없음) — <=0 을 NaN 처리.
    out.loc[out["sum_open_interest"] <= 0, "sum_open_interest"] = np.nan
    return out


def oi_1d_from_5m(symbol: str) -> pd.Series:
    """5분 OI → 1d 봉(UTC 00:00 시작) 마감시점(그 날의 마지막 유효값) 값. 결측 bin 은 ffill.

    ffill 상한(3일) 초과 구간은 `sum_open_interest` 가 NaN 으로 남아 이후 oi_ret 계산에서
    자동으로 제외된다(무한 forward-fill 로 인한 인위적 무변화 구간 방지)."""
    m5 = load_metrics_5m(symbol)
    if m5.empty:
        return pd.Series(dtype=float)
    s = m5["sum_open_interest"]
    last = s.resample("1D", label="left", closed="left").last()
    filled = last.ffill(limit=3)
    filled.name = "oi"
    return filled


# ------------------------------------------------------------------ 회귀·잔차

def rolling_ols_residual(x: np.ndarray, y: np.ndarray, window: int, var_eps: float = 1e-12
                         ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """롤링(window, 현재 bar 포함) 단순 OLS: y = a + b*x. (beta, alpha, residual) 반환.

    pandas rolling cov/var 벡터화. var(x)<var_eps(BTC 수익률이 사실상 무변동) 이면 beta=0 으로
    강제해 분모 폭주를 차단. NaN 이 window 내 하나라도 있으면 그 시점은 NaN.
    """
    xs = pd.Series(x)
    ys = pd.Series(y)
    cov_xy = xs.rolling(window).cov(ys)
    var_x = xs.rolling(window).var()
    mean_x = xs.rolling(window).mean()
    mean_y = ys.rolling(window).mean()
    beta = np.where(var_x.to_numpy() > var_eps, (cov_xy / var_x).to_numpy(), 0.0)
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
class DailySignals:
    """1d 그리드: 알트 OI성장률-BTC가격수익률 회귀 베타·잔차·z-score."""
    idx: pd.DatetimeIndex
    oi_ret: np.ndarray        # 알트 OI 성장률(1d)
    btc_ret: np.ndarray       # BTC 로그수익률(1d)
    beta: np.ndarray
    resid: np.ndarray
    z_resid: np.ndarray       # 핵심 신호(잔차 z-score)
    z_oi_raw: np.ndarray      # 베타 무력화 대조군(원 OI성장률 z-score, 회귀 미사용)


def build_daily_signals(alt_symbol: str, window: int = 60) -> DailySignals | None:
    btc = load_klines(BTC, "1d")
    alt = load_klines(alt_symbol, "1d")
    oi = oi_1d_from_5m(alt_symbol)
    if btc.empty or alt.empty or oi.empty:
        return None
    df = pd.DataFrame({"btc_close": btc["close"], "alt_oi": oi}).dropna(how="any")
    # dropna(how=any) 는 btc_close/alt_oi 둘 다 있는 날짜만 남김(로그수익률·oi_ret 계산 전이라
    # 여기선 두 시계열이 정렬돼 있는지만 확인 — shift 연산은 아래서 각자 시계열에 대해 수행)
    idx = df.index
    btc_ret = np.log(df["btc_close"].to_numpy(float)) - np.log(df["btc_close"].shift(1).to_numpy(float))
    oi_ret = (df["alt_oi"].to_numpy(float) / df["alt_oi"].shift(1).to_numpy(float)) - 1.0
    beta, alpha, resid = rolling_ols_residual(btc_ret, oi_ret, window)
    z_resid = rolling_zscore(resid, window)
    z_oi_raw = rolling_zscore(oi_ret, window)
    return DailySignals(idx=idx, oi_ret=oi_ret, btc_ret=btc_ret, beta=beta, resid=resid,
                        z_resid=z_resid, z_oi_raw=z_oi_raw)


@dataclass
class Bundle:
    """4h 그리드에 매핑된 신호 + klines. 백테스트 엔진 입력."""
    symbol: str
    df4h: pd.DataFrame        # 4h klines(open/high/low/close)
    ema20: np.ndarray
    atr14: np.ndarray
    z_resid: np.ndarray       # 4h 그리드로 causal 매핑된 잔차 z-score
    z_oi_raw: np.ndarray      # 4h 그리드로 causal 매핑된 대조군 z-score
    daily_avail_ts: pd.DatetimeIndex   # 참고용: 매핑에 쓴 일봉 "가용 시각"(=그 날 종가=다음날 00:00)


def build_bundle(alt_symbol: str, window: int = 60, ema_period: int = 20
                 ) -> Bundle | None:
    daily = build_daily_signals(alt_symbol, window=window)
    if daily is None:
        return None
    df4h = load_klines(alt_symbol, "4h")
    if df4h.empty:
        return None
    ema20 = ind.ema(df4h["close"], ema_period).to_numpy(float)
    atr14 = ind.atr(df4h, 14).to_numpy(float)

    # 일봉 신호 "가용 시각" = 그 날 종가 = 다음날 00:00 UTC(일봉 인덱스는 그 날의 시가 시각이므로
    # +1일). merge_asof(backward) 로 4h bar open_time 이 그 가용 시각 이상인 가장 최근 신호를 매핑
    # — causal(미래 참조 없음).
    # ⚠️ datetime64[ms] 인덱스 + pd.Timedelta 덧셈이 datetime64[us] 로 조용히 업캐스트되어
    # merge_asof 가 "incompatible merge keys" 로 즉시 실패(직접 재현 확인) → 양쪽을 ns 로 명시 통일.
    avail_ts = (daily.idx + pd.Timedelta(days=1)).as_unit("ns")
    sig_df = pd.DataFrame({"avail_ts": avail_ts, "z_resid": daily.z_resid,
                           "z_oi_raw": daily.z_oi_raw}).sort_values("avail_ts")
    right = sig_df.rename(columns={"avail_ts": "dt"})
    left = pd.DataFrame({"dt": df4h.index.as_unit("ns")})
    merged = pd.merge_asof(left, right, on="dt", direction="backward")

    return Bundle(symbol=alt_symbol, df4h=df4h, ema20=ema20, atr14=atr14,
                  z_resid=merged["z_resid"].to_numpy(float),
                  z_oi_raw=merged["z_oi_raw"].to_numpy(float),
                  daily_avail_ts=pd.DatetimeIndex(avail_ts))
