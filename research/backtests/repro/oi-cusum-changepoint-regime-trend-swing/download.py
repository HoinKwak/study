"""데이터 수집: 4h klines(가격) + metrics 5분(OI) — 7종목, 2022-01~2026-06.

data.binance.vision 월간(klines)/일별(metrics) 덤프. fapi 는 이 컨테이너에서 451
지역차단이라 정적 덤프만 사용한다.
"""
from __future__ import annotations

import io
import os
import sys
import time
import zipfile
import datetime as dt
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
SP = Path(os.environ.get(
    "OICUSUM_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oicusum_q7z2"))
DATA = SP / "data"
DATA.mkdir(parents=True, exist_ok=True)
(DATA / "klines").mkdir(exist_ok=True)
(DATA / "metrics").mkdir(exist_ok=True)

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
BASE_MONTHLY = "https://data.binance.vision/data/futures/um/monthly"
BASE_DAILY = "https://data.binance.vision/data/futures/um/daily"

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
          pd.to_datetime(out["open_time"].max(), unit="ms"), flush=True)


def fetch_metrics_day(symbol: str, date: str) -> None:
    out_csv = DATA / "metrics" / f"{symbol}-metrics-{date}.csv"
    if out_csv.exists():
        return
    url = f"{BASE_DAILY}/metrics/{symbol}/{symbol}-metrics-{date}.zip"
    for attempt in range(3):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code == 404:
                return
            r.raise_for_status()
            with zipfile.ZipFile(io.BytesIO(r.content)) as zf:
                name = zf.namelist()[0]
                with zf.open(name) as f:
                    content = f.read()
            out_csv.write_bytes(content)
            return
        except Exception as e:  # noqa: BLE001
            time.sleep(1 * (attempt + 1))
    print("MISS", symbol, date, file=sys.stderr)


def fetch_metrics(symbol: str) -> None:
    d0 = dt.date(2022, 1, 1)
    d1 = dt.date(2026, 6, 30)
    d = d0
    days = []
    while d <= d1:
        days.append(d.isoformat())
        d += dt.timedelta(days=1)
    for date in days:
        fetch_metrics_day(symbol, date)


def main() -> None:
    for symbol in SYMBOLS:
        print("=== klines", symbol, flush=True)
        fetch_klines(symbol)
    for symbol in SYMBOLS:
        print("=== metrics", symbol, flush=True)
        fetch_metrics(symbol)


if __name__ == "__main__":
    main()
