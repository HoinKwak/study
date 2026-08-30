"""공통 데이터 로딩·지표 계산 — 크로스섹셔널 프리미엄인덱스 스퀴즈 순위 로테이션."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, "/home/user/study/.claude/worktrees/agent-a0e42d86eb81c1408/src")
from crypto_trader.signals import indicators as _ind  # noqa: E402

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")


def _load(symbol: str, kind: str, tf: str) -> pd.DataFrame:
    fn = DATA / f"{symbol}_{kind}_{tf}.parquet"
    df = pd.read_parquet(fn)
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms", utc=True)
    df = df.set_index("open_time").sort_index()
    df = df[~df.index.duplicated(keep="first")]
    for c in ["open", "high", "low", "close"]:
        df[c] = df[c].astype(float)
    return df


def load_symbol(symbol: str) -> dict:
    """symbol -> {price_1d, price_4h, prem_1d} 원본 프레임(전체 이력)."""
    price_1d = _load(symbol, "klines", "1d")
    price_4h = _load(symbol, "klines", "4h")
    prem_1d = _load(symbol, "premiumIndexKlines", "1d")
    return {"price_1d": price_1d, "price_4h": price_4h, "prem_1d": prem_1d}


def rolling_pctile(s: pd.Series, window: int) -> pd.Series:
    """현재 값이 지난 window일(현재 포함) 중 몇 번째로 작은지 백분위(0~1, weak).

    scipy 미사용 순수 pandas/numpy 구현: rank(pct=True)의 마지막 값.
    """
    def _last_pct_rank(arr: np.ndarray) -> float:
        # weak percentile: (# values <= last) / n
        last = arr[-1]
        return float((arr <= last).sum()) / len(arr)

    return s.rolling(window, min_periods=window).apply(_last_pct_rank, raw=True)


def atr14(df_4h: pd.DataFrame) -> pd.Series:
    """프레임워크 `indicators.atr`(Wilder ewm) 그대로 재사용 — 자체 재구현 아님."""
    return _ind.atr(df_4h, period=14)


def donchian(price_1d: pd.DataFrame, length: int) -> tuple[pd.Series, pd.Series]:
    """자기 제외(shift(1)) 15일 채널: donchian_high(t)=max(high[t-len..t-1]), low 동일."""
    dh = price_1d["high"].rolling(length).max().shift(1)
    dl = price_1d["low"].rolling(length).min().shift(1)
    return dh, dl


def build_daily_frame(symbol: str, data: dict, squeeze_window: int = 60,
                       donchian_len: int = 15) -> pd.DataFrame:
    prem = data["prem_1d"]
    price = data["price_1d"]
    idx = prem.index.intersection(price.index)
    prem = prem.loc[idx]
    price = price.loc[idx]
    rng = prem["high"] - prem["low"]
    pctile = rolling_pctile(rng, squeeze_window)
    dh, dl = donchian(price, donchian_len)
    out = pd.DataFrame({
        "prem_range": rng,
        "squeeze_pctile": pctile,
        "price_close": price["close"],
        "price_high": price["high"],
        "price_low": price["low"],
        "donchian_high": dh,
        "donchian_low": dl,
    }, index=idx)
    out["dow"] = out.index.dayofweek  # 0=Monday
    return out
