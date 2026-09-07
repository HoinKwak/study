"""공통 데이터 로딩·지표 계산 — 실현변동성 OU 반감기 레짐전환.

단위사고 방지: klines.open_time(정수 ms epoch)는 unit="ms" 명시. 인덱스 dtype을
datetime64[ns]로 통일(다른 라운드에서 datetime64[ms]+Timedelta가 us로 조용히
업캐스트되는 사고가 반복됨 — ns 명시로 원천 차단).
"""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SP = Path(os.environ.get(
    "RVOU_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/rvou_k3f8"))
DATA = SP / "data"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01 00:00:00", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01 00:00:00", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

ROUND_TRIP_COST = 0.0014  # 0.14% (수수료+슬리피지)
RISK_PCT = 0.01


def load_klines_4h(symbol: str) -> pd.DataFrame:
    fn = DATA / "klines" / f"{symbol}_4h.parquet"
    df = pd.read_parquet(fn)
    # open_time: ms epoch(정수) -> ns 명시 datetime64[ns] UTC
    # (pandas 3.0.5 에서 to_datetime(unit="ms")는 datetime64[ms] 를 유지하고 자동으로 ns 로
    #  승격하지 않는다 — 다른 라운드에서 ms 인덱스 + Timedelta 덧셈이 조용히 us 로 업캐스트되는
    #  사고가 반복됐으므로, 이 백테스트에선 인덱스 dtype 을 ns 로 명시 통일해 그 함정을 원천 차단한다.)
    idx = pd.to_datetime(df["open_time"].astype("int64"), unit="ms", utc=True).astype(
        "datetime64[ns, UTC]")
    df = df.set_index(idx).sort_index()
    df = df[~df.index.duplicated(keep="first")]
    for c in ["open", "high", "low", "close", "volume", "quote_volume", "count"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df.index.name = "ts"
    return df[["open", "high", "low", "close", "volume", "quote_volume", "count"]]


def atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat([
        (high - low),
        (high - prev_close).abs(),
        (low - prev_close).abs(),
    ], axis=1).max(axis=1)
    # Wilder's smoothing (표준 ATR)
    return tr.ewm(alpha=1.0 / window, adjust=False, min_periods=window).mean()


def ema(s: pd.Series, span: int) -> pd.Series:
    return s.ewm(span=span, adjust=False, min_periods=span).mean()


def rolling_ols_ar1(y: pd.Series, window: int) -> dict[str, pd.Series]:
    """log(rv_t) = a + phi*log(rv_{t-1}) + e, 트레일링 window(포함 t)로 매 시점 재적합.

    닫힌형(rolling sums)으로 벡터화 — 매 봉 파이썬 루프 회귀를 피한다.
    반환: phi, a, mu(=a/(1-phi)), resid_std(윈도우 내 잔차 표준편차, population 버전).
    """
    x = y.shift(1)  # log(rv_{t-1})
    n = window
    # 윈도우 내 (x,y) 쌍이 전부 유효해야 함(둘 다 NaN 아님)
    valid = x.notna() & y.notna()
    xv = x.where(valid)
    yv = y.where(valid)
    cnt = valid.rolling(n).sum()

    sum_x = xv.rolling(n).sum()
    sum_y = yv.rolling(n).sum()
    sum_xx = (xv * xv).rolling(n).sum()
    sum_yy = (yv * yv).rolling(n).sum()
    sum_xy = (xv * yv).rolling(n).sum()

    mean_x = sum_x / cnt
    mean_y = sum_y / cnt
    sxx = sum_xx - cnt * mean_x ** 2
    syy = sum_yy - cnt * mean_y ** 2
    sxy = sum_xy - cnt * mean_x * mean_y

    phi = sxy / sxx
    a = mean_y - phi * mean_x
    ssr = syy - phi * sxy
    ssr = ssr.clip(lower=0)
    resid_std = np.sqrt(ssr / cnt)

    # 윈도우 내 유효쌍 수가 window에 못 미치면(결측 존재) NaN 처리
    incomplete = cnt < n
    phi = phi.where(~incomplete)
    a = a.where(~incomplete)
    resid_std = resid_std.where(~incomplete)

    mu = a / (1 - phi)
    return {"phi": phi, "a": a, "mu": mu, "resid_std": resid_std}


def compute_indicators(df: pd.DataFrame, rv_window: int = 42, ou_window: int = 180,
                        ema_span: int = 20, atr_window: int = 14) -> pd.DataFrame:
    out = df.copy()
    logret = np.log(out["close"] / out["close"].shift(1))
    out["logret"] = logret
    out["rv"] = logret.rolling(rv_window).std()
    out["log_rv"] = np.log(out["rv"].replace(0, np.nan))
    ou = rolling_ols_ar1(out["log_rv"], ou_window)
    out["phi"] = ou["phi"]
    out["mu"] = ou["mu"]
    out["resid_std"] = ou["resid_std"]
    # phi<=0 또는 phi>=1 이면 half-life 정의 불가 -> NaN
    valid_phi = (out["phi"] > 0) & (out["phi"] < 1)
    out["half_life"] = np.where(valid_phi, -np.log(2) / np.log(out["phi"].where(valid_phi)), np.nan)
    out["dev"] = (out["log_rv"] - out["mu"]) / out["resid_std"]
    out["dev"] = out["dev"].where(valid_phi)  # phi 무효면 dev도 무효
    out["ema20"] = ema(out["close"], ema_span)
    out["atr14"] = atr(out, atr_window)
    out["body"] = out["close"] - out["open"]
    return out
