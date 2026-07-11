"""열린 거래를 수동으로 청산 처리(저널 반영) — 바이낸스에서 직접 닫은 포지션용.

거래소에서 수동으로 포지션을 닫으면 봇의 리컨실이 다음 사이클에 자동 반영하지만,
청산가를 SL 로 근사한다. 이 스크립트는 **실제 청산가**를 지정해 정확히 기록하고,
남아있는 조건부 주문(미체결 SL 등)도 정리한다.

    # 현재가로 청산 기록(가격 자동 조회)
    python -m scripts.close_trade --symbol TAC/USDT

    # 실제 체결가 지정
    python -m scripts.close_trade --symbol TAC/USDT --price 0.003684

    # 슬리브/방향 지정(한 심볼에 여러 포지션일 때)
    python -m scripts.close_trade --symbol TAC/USDT --sleeve scalp --direction short

⚠️ 봇이 돌고 있으면 state/trades.json 동시 접근이 생길 수 있으니, 가능하면
   봇을 잠깐 멈추고 실행하세요.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.monitoring import TradeJournal  # noqa: E402
from crypto_trader.utils import get_logger  # noqa: E402


def _pnl(direction: str, entry: float, exit_price: float, qty: float) -> float:
    return (exit_price - entry) * qty if direction == "long" else (entry - exit_price) * qty


def main() -> None:
    p = argparse.ArgumentParser(description="열린 거래 수동 청산 기록")
    p.add_argument("--symbol", required=True, help="예: TAC/USDT")
    p.add_argument("--sleeve", default=None, help="scalp/mid/swing (여러 포지션일 때 지정)")
    p.add_argument("--direction", default=None, choices=["long", "short"])
    p.add_argument("--price", type=float, default=None, help="실제 청산가(생략 시 현재가 조회)")
    p.add_argument("--reason", default="manual", help="청산 사유 태그")
    p.add_argument("--no-cancel", action="store_true", help="잔여 조건부 주문 정리 생략")
    args = p.parse_args()

    s = get_settings()
    log = get_logger("close_trade", s.log_level)
    journal = TradeJournal(s.state_dir)

    # 대상 열린 거래 찾기
    candidates = [t for t in journal.open_trades() if t.symbol == args.symbol
                  and (args.sleeve is None or t.sleeve == args.sleeve)
                  and (args.direction is None or t.direction == args.direction)]
    if not candidates:
        log.error("열린 거래 없음: %s (sleeve=%s direction=%s)",
                  args.symbol, args.sleeve, args.direction)
        sys.exit(1)
    if len(candidates) > 1:
        log.error("여러 거래가 매칭됨(%d) — --sleeve/--direction 로 특정하세요:", len(candidates))
        for t in candidates:
            log.error("  %s %s @ %.6g (sleeve=%s)", t.symbol, t.direction,
                      t.entry_price, t.sleeve)
        sys.exit(1)
    rec = candidates[0]

    # 청산가 결정
    exit_price = args.price
    binance = None
    if s.has_binance_keys:
        try:
            from crypto_trader.connectors import BinanceClient
            binance = BinanceClient(s)
        except Exception as e:  # noqa: BLE001
            log.warning("거래소 연결 실패(가격 조회/주문정리 생략): %s", e)
    if exit_price is None:
        if binance is not None:
            try:
                bid, ask = binance.best_bid_ask(args.symbol)
                exit_price = (bid + ask) / 2
            except Exception as e:  # noqa: BLE001
                log.warning("현재가 조회 실패: %s", e)
        if exit_price is None:
            exit_price = rec.stop_price or rec.entry_price
            log.warning("청산가 미지정·조회 실패 → SL/진입가로 근사: %.6g", exit_price)

    # 잔여 조건부 주문(미체결 SL 등) 정리
    if binance is not None and not args.no_cancel:
        try:
            binance.cancel_all_orders(args.symbol)
            log.info("%s 잔여 주문 정리 완료", args.symbol)
        except Exception as e:  # noqa: BLE001
            log.warning("잔여 주문 정리 실패: %s", e)

    pnl = _pnl(rec.direction, rec.entry_price, exit_price, rec.quantity)
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    journal.record_close(rec.symbol, exit_price, now, pnl, args.reason,
                         sleeve=rec.sleeve, direction=rec.direction)
    ret = pnl / (rec.entry_price * rec.quantity) * 100.0 if rec.entry_price else 0.0
    log.info("청산 기록: %s %s 진입 %.6g → 청산 %.6g | 손익 %+.2f USDT (%+.2f%%) [%s]",
             rec.symbol, rec.direction.upper(), rec.entry_price, exit_price, pnl, ret, args.reason)


if __name__ == "__main__":
    main()
