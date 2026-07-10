"""멀티 타임프레임 포트폴리오 실행 (중장기/중기/단타 슬리브).

    python -m scripts.run_portfolio            # 무한 루프 (슬리브별 주기)
    python -m scripts.run_portfolio --once     # 전체 슬리브 1회 평가 후 종료

TRADE_MODE 로 dry_run / paper / live 전환. 기본 헤지 모드 + isolated.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.portfolio import PortfolioEngine  # noqa: E402
from crypto_trader.utils import get_logger  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="crypto-trader 포트폴리오")
    parser.add_argument("--once", action="store_true", help="전체 슬리브 1회 평가 후 종료")
    parser.add_argument("--sleeves", default=None,
                        help="가동할 슬리브 이름 (쉼표구분, 예: scalp 또는 swing,scalp). 생략 시 전부")
    args = parser.parse_args()

    settings = get_settings()
    log = get_logger("main", settings.log_level)

    from crypto_trader.portfolio import default_sleeves
    sleeves = default_sleeves(settings)
    if args.sleeves:
        wanted = {s.strip() for s in args.sleeves.split(",") if s.strip()}
        sleeves = [sl for sl in sleeves if sl.name in wanted]
        if not sleeves:
            log.error("해당 이름의 슬리브 없음: %s", args.sleeves)
            sys.exit(1)

    log.info("포트폴리오 시작: mode=%s hedge=%s sleeves=%s",
             settings.trade_mode.value, settings.binance_hedge_mode,
             [f"{sl.name}({','.join(sl.symbols)})" for sl in sleeves])

    engine = PortfolioEngine(settings, sleeves=sleeves)
    if args.once:
        engine.run_once(force_all=True)
    else:
        engine.run_forever()


if __name__ == "__main__":
    main()
