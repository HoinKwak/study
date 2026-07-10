"""페이퍼/드라이런 트레이딩 실행 진입점.

    python -m scripts.run_paper            # 무한 루프
    python -m scripts.run_paper --once     # 1회만 평가하고 종료

TRADE_MODE 환경변수로 dry_run / paper / live 전환.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

# 프로젝트 루트의 src 를 import 경로에 추가
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.engine import TradingEngine  # noqa: E402
from crypto_trader.utils import get_logger  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="crypto-trader 페이퍼 트레이딩")
    parser.add_argument("--once", action="store_true", help="1회만 평가하고 종료")
    args = parser.parse_args()

    settings = get_settings()
    log = get_logger("main", settings.log_level)
    log.info("설정: mode=%s testnet=%s symbols=%s",
             settings.trade_mode.value, settings.binance_testnet, settings.symbols)

    engine = TradingEngine(settings)
    if args.once:
        engine.run_once()
    else:
        engine.run_forever()


if __name__ == "__main__":
    main()
