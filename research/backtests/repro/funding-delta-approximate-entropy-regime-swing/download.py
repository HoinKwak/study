"""데이터 수집 — 펀딩비율 변화량(ΔFunding) ApEn 레짐 게이트 + BTC 추세추종.

- BTC `fundingRate`(monthly zip, UM) — ApEn/CUSUM/펀딩레벨 신호 산출용. 2021-09~2026-06
  (IS_START 2022-01-01 이전 100여일 워밍업 확보 — apen_window 30정산(10일)+90일 백분위창).
- 7종목 4h klines — 이미 다른 스윙 백테스트(oi-price-sign-agreement-rate)에서 캐시된
  research/backtests/repro/oi-price-sign-agreement-rate-regime-gate-trend-swing 계열 원자료를
  재사용(2021-10~2026-06 CSV, 이 스크립트 실행 전 별도 복사됨 — `data/klines_4h/*.csv`).
  이 스크립트는 **펀딩레이트만** 새로 받는다.
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

BASE = "https://data.binance.vision/data/futures/um/monthly/fundingRate/BTCUSDT"
FUNDING_COLS = ["calc_time", "funding_interval_hours", "last_funding_rate"]

MONTHS = pd.period_range("2021-09", "2026-06", freq="M")


def fetch_month(ym: str) -> pd.DataFrame | None:
    url = f"{BASE}/BTCUSDT-fundingRate-{ym}.zip"
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
                    has_header = first.startswith(b"calc_time")
                    f.seek(0)
                    if has_header:
                        df = pd.read_csv(f)
                    else:
                        df = pd.read_csv(f, header=None, names=FUNDING_COLS)
            return df
        except Exception as e:  # noqa: BLE001
            print(f"  retry BTCUSDT fundingRate {ym}: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    return None


def main() -> None:
    fn = DATA / "BTCUSDT_fundingRate.parquet"
    if fn.exists():
        print("skip", fn.name)
        return
    frames = []
    for p in MONTHS:
        ym = str(p)
        df = fetch_month(ym)
        if df is not None:
            frames.append(df)
            print("fetched", ym, len(df), flush=True)
        else:
            print("404/missing", ym, flush=True)
    out = pd.concat(frames, ignore_index=True)
    out = out.drop_duplicates(subset="calc_time").sort_values("calc_time").reset_index(drop=True)
    out.to_parquet(fn)
    print("->", len(out), "rows",
          pd.to_datetime(out["calc_time"], unit="ms").min(),
          pd.to_datetime(out["calc_time"], unit="ms").max())


if __name__ == "__main__":
    main()
