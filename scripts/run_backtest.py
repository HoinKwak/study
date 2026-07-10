"""과거 데이터 백테스트 실행.

    # 슬리브 전략 백테스트 (swing/mid/scalp)
    python -m scripts.run_backtest --sleeve swing --symbol BTC/USDT --days 365
    python -m scripts.run_backtest --sleeve mid   --symbol BTC/USDT --days 90
    python -m scripts.run_backtest --sleeve scalp --symbol BTC/USDT --days 7

    # (레거시) 레짐 전략
    python -m scripts.run_backtest --sleeve regime --symbol BTC/USDT --timeframe 1h --days 180

타임프레임/확인TF 는 슬리브 기본값(swing 4h/1d, mid 15m/1h, scalp 1m/5m)을 따르고
--timeframe 으로 재정의할 수 있다. 확인 TF 는 시그널 TF 에서 리샘플로 생성.

데이터 소스: 바이낸스 선물 API → 차단(451) 시 공개 미러(data-api.binance.vision,
현물 캔들)로 자동 폴백. 파생 데이터(OI)는 과거 이력이 없어 백테스트에서 제외.
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import requests  # noqa: E402

from crypto_trader.backtest import Backtester, SleeveBacktester  # noqa: E402
from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.data import ohlcv_to_df  # noqa: E402
from crypto_trader.utils import get_logger  # noqa: E402

log = get_logger("backtest")

TF_MS = {
    "1m": 60_000, "3m": 180_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
    "1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000,
}

# 슬리브별 기본 (시그널TF, 확인TF)
SLEEVE_TF = {
    "swing": ("4h", "1d"),
    "mid": ("15m", "1h"),
    "scalp": ("1m", "5m"),
    "regime": ("1h", None),
}

MIRROR = "https://data-api.binance.vision"


def fetch_history(symbol: str, timeframe: str, days: int) -> list[list]:
    """지정 일수만큼 과거 OHLCV 수집. 선물 API 차단 시 현물 미러 폴백."""
    tf_ms = TF_MS[timeframe]
    now = int(time.time() * 1000)
    since = now - days * 86_400_000
    pair = symbol.replace("/", "").upper()

    # 1) ccxt 선물 시도
    try:
        import ccxt
        ex = ccxt.binance({"enableRateLimit": True, "options": {"defaultType": "future"}})
        rows: list[list] = []
        cursor = since
        while cursor < now:
            batch = ex.fetch_ohlcv(symbol, timeframe=timeframe, since=cursor, limit=1000)
            if not batch:
                break
            rows.extend(batch)
            cursor = batch[-1][0] + tf_ms
            if len(batch) < 1000:
                break
        if rows:
            log.info("선물 API 에서 %d 캔들 수집", len(rows))
            return _dedup(rows)
    except Exception as e:  # noqa: BLE001
        log.info("선물 API 사용 불가(%s) — 현물 미러로 폴백", str(e)[:80])

    # 2) 현물 미러 폴백
    session = requests.Session()
    rows = []
    cursor = since
    while cursor < now:
        r = session.get(f"{MIRROR}/api/v3/klines",
                        params={"symbol": pair, "interval": timeframe,
                                "startTime": cursor, "limit": 1000},
                        timeout=30)
        r.raise_for_status()
        batch = [k[:6] for k in r.json()]
        if not batch:
            break
        rows.extend(batch)
        cursor = int(batch[-1][0]) + tf_ms
        if len(batch) < 1000:
            break
        time.sleep(0.15)
    log.info("현물 미러에서 %d 캔들 수집", len(rows))
    return _dedup(rows)


def _dedup(rows: list[list]) -> list[list]:
    seen, out = set(), []
    for r in rows:
        if r[0] not in seen:
            seen.add(r[0])
            out.append(r)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="crypto-trader 백테스트")
    parser.add_argument("--sleeve", default="regime",
                        choices=["swing", "mid", "scalp", "regime"])
    parser.add_argument("--symbol", default="BTC/USDT")
    parser.add_argument("--timeframe", default=None, help="시그널 TF 재정의")
    parser.add_argument("--days", type=int, default=None)
    parser.add_argument("--equity", type=float, default=10_000.0)
    parser.add_argument("--fee", type=float, default=0.0005, help="테이커 수수료율/side")
    parser.add_argument("--slippage", type=float, default=0.0002)
    args = parser.parse_args()

    settings = get_settings()
    signal_tf, confirm_tf = SLEEVE_TF[args.sleeve]
    signal_tf = args.timeframe or signal_tf
    default_days = {"swing": 365, "mid": 90, "scalp": 7, "regime": 180}
    days = args.days or default_days[args.sleeve]

    log.info("백테스트: sleeve=%s %s %s(확인 %s) 최근 %d일",
             args.sleeve, args.symbol, signal_tf, confirm_tf, days)
    rows = fetch_history(args.symbol, signal_tf, days)
    if len(rows) < 100:
        log.error("데이터 부족: %d 캔들", len(rows))
        sys.exit(1)
    df = ohlcv_to_df(rows)

    if args.sleeve == "regime":
        bt = Backtester(settings, starting_equity=args.equity)
        result = bt.run(args.symbol, df)
    else:
        bt = SleeveBacktester(settings, args.sleeve, confirm_tf=confirm_tf,
                              starting_equity=args.equity,
                              taker_fee=args.fee, slippage=args.slippage)
        result = bt.run(args.symbol, df)

    print(result.report())


if __name__ == "__main__":
    main()
