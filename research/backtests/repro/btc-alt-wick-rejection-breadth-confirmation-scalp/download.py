"""데이터 수집: klines(15m) — 7종목, 2022-01~2026-06.

data.binance.vision 월간 덤프. fapi 는 이 컨테이너에서 451 지역차단이라 정적 덤프만 사용.
이 전략은 OHLCV만 필요(15m 단일 TF). 2022년 zip 은 헤더 없음, 2024년 이후는 헤더 있음 —
헤더 유무를 자동판별(기존 프리미엄인덱스 리포트와 동일 패턴).
"""
from __future__ import annotations

import io
import time
import zipfile
from pathlib import Path

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
BASE = "https://data.binance.vision/data/futures/um/monthly"
TF = "15m"

COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
        "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]

MONTHS = pd.period_range("2022-01", "2026-06", freq="M")


def fetch_month(symbol: str, tf: str, ym: str) -> pd.DataFrame | None:
    url = f"{BASE}/klines/{symbol}/{tf}/{symbol}-{tf}-{ym}.zip"
    for attempt in range(3):
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
                        df = pd.read_csv(f, header=None, names=COLS)
            return df
        except Exception as e:  # noqa: BLE001
            print(f"  retry {symbol} {tf} {ym}: {e}")
            time.sleep(2)
    return None


def fetch_series(symbol: str, tf: str) -> pd.DataFrame:
    frames = []
    for p in MONTHS:
        ym = str(p)
        df = fetch_month(symbol, tf, ym)
        if df is not None:
            frames.append(df)
    if not frames:
        raise RuntimeError(f"no data for {symbol}/{tf}")
    out = pd.concat(frames, ignore_index=True)
    out = out.drop_duplicates(subset="open_time").sort_values("open_time").reset_index(drop=True)
    return out


def main() -> None:
    for symbol in SYMBOLS:
        fn = DATA / f"{symbol}_klines_{TF}.parquet"
        if fn.exists():
            print("skip", fn.name)
            continue
        print("fetch", symbol, TF)
        df = fetch_series(symbol, TF)
        df.to_parquet(fn)
        print("  ->", len(df), "rows", df["open_time"].min(), df["open_time"].max())


if __name__ == "__main__":
    main()
