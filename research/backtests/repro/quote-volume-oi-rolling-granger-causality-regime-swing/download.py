"""데이터 수집: 4h klines(quote_volume 포함) + metrics 5분(OI) — 7종목, 2022-01~2026-06.

data.binance.vision 월간(klines)/일별(metrics) 덤프. fapi 는 이 컨테이너에서 451
지역차단이라 정적 덤프만 사용한다.
"""
from __future__ import annotations

import io
import os
import sys
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
SP = Path(os.environ.get(
    "GRQV_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/granger_oiqv"))
DATA = SP / "data"
DATA.mkdir(parents=True, exist_ok=True)
(DATA / "klines").mkdir(exist_ok=True)
(DATA / "metrics").mkdir(exist_ok=True)

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
BASE_MONTHLY = "https://data.binance.vision/data/futures/um/monthly"

KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
              "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]

MONTHS = pd.period_range("2022-01", "2026-06", freq="M")


def fetch_month_klines(symbol: str, ym: str) -> pd.DataFrame | None:
    url = f"{BASE_MONTHLY}/klines/{symbol}/4h/{symbol}-4h-{ym}.zip"
    for attempt in range(4):
        try:
            r = requests.get(url, timeout=60)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
                name = zf.namelist()[0]
                with zf.open(name) as f:
                    first = f.readline()
                    has_header = first.startswith(b"open_time")
                    f.seek(0)
                    if has_header:
                        df = pd.read_csv(f)
                    else:
                        df = pd.read_csv(f, header=None, names=KLINE_COLS)
            return df
        except Exception as e:  # noqa: BLE001
            print(f"  retry klines {symbol} {ym}: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    return None


def fetch_klines(symbol: str) -> None:
    fn = DATA / "klines" / f"{symbol}_4h.parquet"
    if fn.exists():
        print("skip", fn.name)
        return
    frames = []
    for p in MONTHS:
        ym = str(p)
        df = fetch_month_klines(symbol, ym)
        if df is not None:
            frames.append(df)
    if not frames:
        raise RuntimeError(f"no klines for {symbol}")
    out = pd.concat(frames, ignore_index=True)
    out = out.drop_duplicates(subset="open_time").sort_values("open_time").reset_index(drop=True)
    out.to_parquet(fn)
    print("  ->", symbol, len(out), "rows",
          pd.to_datetime(out["open_time"].min(), unit="ms"),
          pd.to_datetime(out["open_time"].max(), unit="ms"))


if __name__ == "__main__":
    for sym in SYMBOLS:
        fetch_klines(sym)
    print("done klines")
