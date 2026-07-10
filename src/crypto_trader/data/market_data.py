"""OHLCV 리스트 → 정규화된 pandas DataFrame."""
from __future__ import annotations

import pandas as pd

OHLCV_COLUMNS = ["timestamp", "open", "high", "low", "close", "volume"]


def ohlcv_to_df(ohlcv: list[list[float]]) -> pd.DataFrame:
    """ccxt fetch_ohlcv 결과를 DataFrame 으로 변환.

    timestamp(ms) 를 UTC datetime 인덱스로 두고, OHLCV 는 float 로.
    """
    df = pd.DataFrame(ohlcv, columns=OHLCV_COLUMNS)
    df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    for col in ["open", "high", "low", "close", "volume"]:
        df[col] = df[col].astype(float)
    df = df.set_index("datetime")
    return df
