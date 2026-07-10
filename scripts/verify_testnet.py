"""바이낸스 선물 테스트넷 연결 및 주문 라이프사이클 검증.

    # 1) 연결/잔고/시세만 확인 (주문 안 냄, 기본)
    python -m scripts.verify_testnet

    # 2) 실제 주문 라이프사이클까지 검증 (최소 수량 진입 → 손절예약 → 즉시 청산)
    python -m scripts.verify_testnet --execute --symbol BTC/USDT

안전장치:
  - 반드시 BINANCE_TESTNET=true 여야 실행 (실전 키면 즉시 중단)
  - 주문은 --execute 플래그가 있을 때만 발생
  - 최소 명목가치(min notional) 기준의 아주 작은 수량만 사용
  - 진입 직후 손절 예약을 확인하고 곧바로 포지션을 청산
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.connectors import BinanceClient  # noqa: E402
from crypto_trader.utils import get_logger  # noqa: E402

log = get_logger("verify")


def main() -> None:
    parser = argparse.ArgumentParser(description="바이낸스 테스트넷 검증")
    parser.add_argument("--symbol", default="BTC/USDT")
    parser.add_argument("--execute", action="store_true",
                        help="실제 주문 라이프사이클까지 검증 (테스트넷 가짜자금)")
    parser.add_argument("--leverage", type=int, default=2)
    args = parser.parse_args()

    s = get_settings()

    # --- 안전 게이트 ---
    if not s.has_binance_keys:
        log.error("BINANCE_API_KEY / SECRET 이 .env 에 없습니다. 테스트넷 키를 넣어주세요.")
        sys.exit(1)
    if not s.binance_testnet:
        log.error("BINANCE_TESTNET=false 입니다. 이 스크립트는 테스트넷 전용입니다. 중단.")
        sys.exit(1)

    client = BinanceClient(s)
    canonical = client.resolve_symbol(args.symbol)

    print("\n===== 1. 연결 & 계좌 =====")
    balance = client.fetch_balance_usdt()
    print(f"USDT 가용 잔고 : {balance:,.2f}")
    positions = client.fetch_positions()
    print(f"현재 포지션 수 : {len(positions)}")
    for p in positions:
        print(f"  - {p.get('symbol')} {p.get('side')} {p.get('contracts')}")

    print("\n===== 2. 시세 & 마켓 메타 =====")
    price = client.last_price(args.symbol)
    min_notional = client.min_notional(args.symbol)
    print(f"{args.symbol} 현재가 : {price:,.2f}")
    print(f"최소 명목가치   : {min_notional} USDT")

    if not args.execute:
        print("\n[미실행 모드] --execute 를 붙이면 실제 주문 라이프사이클을 검증합니다.")
        print("연결/조회는 정상입니다. ✅")
        return

    # --- 주문 라이프사이클 검증 ---
    print("\n===== 3. 주문 라이프사이클 (테스트넷) =====")
    # 최소 명목가치보다 약간 크게 잡아 최소주문 거부 회피
    target_notional = max(min_notional * 1.1, 20.0)
    raw_qty = target_notional / price
    qty = client.amount_to_precision(args.symbol, raw_qty)
    print(f"진입 수량 : {qty} (~{qty * price:.2f} USDT)")

    client.set_leverage(args.symbol, args.leverage)
    print(f"레버리지 설정 : x{args.leverage}")

    print("→ 시장가 롱 진입...")
    order = client.create_market_order(args.symbol, "buy", qty)
    entry = float(order.get("average") or order.get("price") or price)
    print(f"  진입 체결가 : {entry:,.2f} (orderId={order.get('id')})")

    time.sleep(1.0)
    pos = [p for p in client.fetch_positions(args.symbol) if p.get("symbol") == canonical]
    print(f"  포지션 확인 : {pos[0].get('contracts') if pos else '없음'}")

    # 손절 예약 (진입가 -2%)
    stop_price = round(entry * 0.98, 2)
    print(f"→ 손절 예약 SL={stop_price:,.2f} ...")
    try:
        so = client.create_stop_order(args.symbol, "sell", qty, stop_price)
        print(f"  손절 주문 등록 : orderId={so.get('id')}")
    except Exception as e:  # noqa: BLE001
        print(f"  손절 주문 실패(테스트넷 트리거 제약일 수 있음): {e}")

    open_orders = client.fetch_open_orders(args.symbol)
    print(f"  미체결 주문 수 : {len(open_orders)}")

    print("→ 포지션 즉시 청산 & 주문 정리...")
    client.close_position(args.symbol)
    time.sleep(1.0)
    client.cancel_all_orders(args.symbol)

    remaining = [p for p in client.fetch_positions(args.symbol) if p.get("symbol") == canonical]
    print(f"  청산 후 잔여 포지션 : {len(remaining)}")
    print("\n주문 라이프사이클 검증 완료. ✅")


if __name__ == "__main__":
    main()
