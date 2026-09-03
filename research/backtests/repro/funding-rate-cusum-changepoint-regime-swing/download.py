"""데이터 수집: fundingRate + 4h klines — 7종목, 2022-01~2026-06.

data.binance.vision 월간 덤프(선물 UM). fapi 는 이 컨테이너에서 451 지역차단이라
정적 덤프만 사용한다. fundingRate/klines 둘 다 2022년분부터 헤더가 있어(실측 확인)
CSV 를 그대로 읽되, 혹시 헤더 없는 옛 포맷이 섞여 있을 경우를 대비해 첫 토큰이
숫자인지로 자동 판별한다.
"""
from __future__ import annotations

import io
import sys
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

FUNDING_COLS = ["calc_time", "funding_interval_hours", "last_funding_rate"]
KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
              "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]

MONTHS = pd.period_range("2022-01", "2026-06", freq="M")


def fetch_month(kind: str, symbol: str, tf: str | None, ym: str) -> pd.DataFrame | None:
    if tf is None:
        url = f"{BASE}/{kind}/{symbol}/{symbol}-{kind}-{ym}.zip"
        cols = FUNDING_COLS
        header_token = b"calc_time"
    else:
        url = f"{BASE}/{kind}/{symbol}/{tf}/{symbol}-{tf}-{ym}.zip"
        cols = KLINE_COLS
        header_token = b"open_time"
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
                    has_header = first.startswith(header_token)
                    f.seek(0)
                    if has_header:
                        df = pd.read_csv(f)
                    else:
                        df = pd.read_csv(f, header=None, names=cols)
            return df
        except Exception as e:  # noqa: BLE001
            print(f"  retry {symbol} {kind} {tf} {ym}: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    return None


def fetch_series(kind: str, symbol: str, tf: str | None) -> pd.DataFrame:
    frames = []
    for p in MONTHS:
        ym = str(p)
        df = fetch_month(kind, symbol, tf, ym)
        if df is not None:
            frames.append(df)
    if not frames:
        raise RuntimeError(f"no data for {kind}/{symbol}/{tf}")
    out = pd.concat(frames, ignore_index=True)
    key = "calc_time" if tf is None else "open_time"
    out = out.drop_duplicates(subset=key).sort_values(key).reset_index(drop=True)
    return out


def main() -> None:
    for symbol in SYMBOLS:
        for kind, tf in [("fundingRate", None), ("klines", "4h")]:
            fn = DATA / f"{symbol}_{kind}.parquet"
            if fn.exists():
                print("skip", fn.name)
                continue
            print("fetch", symbol, kind, tf, flush=True)
            df = fetch_series(kind, symbol, tf)
            df.to_parquet(fn)
            key = "calc_time" if tf is None else "open_time"
            print("  ->", len(df), "rows", df[key].min(), df[key].max(), flush=True)


if __name__ == "__main__":
    main()
