"""과거 데이터 백테스트 실행.

    python -m scripts.run_backtest --symbol BTC/USDT --timeframe 1h --days 180

파생 데이터는 장기 이력이 없어 백테스트는 기술지표 시그널만 사용한다.
OHLCV 는 바이낸스 공개 API 에서 페이지네이션으로 수집한다(키 불필요).
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import ccxt  # noqa: E402

from crypto_trader.backtest import Backtester  # noqa: E402
from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.data import ohlcv_to_df  # noqa: E402
from crypto_trader.utils import get_logger  # noqa: E402

log = get_logger("backtest")

# timeframe -> 밀리초
TF_MS = {
    "1m": 60_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
    "1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000,
}


def fetch_history(exchange: ccxt.binance, symbol: str, timeframe: str, days: int) -> list[list]:
    """지정 일수만큼 과거 OHLCV 를 페이지네이션으로 수집."""
    tf_ms = TF_MS.get(timeframe)
    if tf_ms is None:
        raise ValueError(f"지원하지 않는 timeframe: {timeframe}")

    now = exchange.milliseconds()
    since = now - days * 86_400_000
    all_rows: list[list] = []

    while since < now:
        batch = exchange.fetch_ohlcv(symbol, timeframe=timeframe, since=since, limit=1000)
        if not batch:
            break
        all_rows.extend(batch)
        since = batch[-1][0] + tf_ms
        if len(batch) < 1000:
            break
        time.sleep(exchange.rateLimit / 1000.0)

    # 중복 제거
    seen = set()
    unique = []
    for row in all_rows:
        if row[0] not in seen:
            seen.add(row[0])
            unique.append(row)
    return unique


def main() -> None:
    parser = argparse.ArgumentParser(description="crypto-trader 백테스트")
    parser.add_argument("--symbol", default="BTC/USDT")
    parser.add_argument("--timeframe", default="1h")
    parser.add_argument("--days", type=int, default=180)
    parser.add_argument("--equity", type=float, default=10_000.0)
    args = parser.parse_args()

    settings = get_settings()
    exchange = ccxt.binance({"enableRateLimit": True, "options": {"defaultType": "future"}})

    log.info("과거 데이터 수집: %s %s 최근 %d일", args.symbol, args.timeframe, args.days)
    rows = fetch_history(exchange, args.symbol, args.timeframe, args.days)
    log.info("수집 완료: %d 캔들", len(rows))

    df = ohlcv_to_df(rows)
    bt = Backtester(settings, starting_equity=args.equity)
    result = bt.run(args.symbol, df)
    print(result.report())


if __name__ == "__main__":
    main()
