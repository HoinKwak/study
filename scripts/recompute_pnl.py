"""저널의 청산 손익을 수수료 반영해 재계산(소급 보정).

기존에 수수료 없이(총손익) 기록된 과거 거래를, 저장된 진입가·청산가·수량으로
테이커 수수료를 차감해 재계산한다. 손익은 가격·수량의 함수라 여러 번 돌려도
같은 값(idempotent) — 이미 반영된 거래도 안전하다.

    python -m scripts.recompute_pnl            # 재계산 + 저장
    python -m scripts.recompute_pnl --dry-run  # 변경만 미리보기(저장 안 함)
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.monitoring import TradeJournal  # noqa: E402


def main() -> None:
    p = argparse.ArgumentParser(description="청산 손익 수수료 소급 보정")
    p.add_argument("--dry-run", action="store_true", help="저장 없이 미리보기")
    args = p.parse_args()

    s = get_settings()
    fee = s.taker_fee_pct / 100.0
    journal = TradeJournal(s.state_dir)

    old_total = new_total = 0.0
    changed = 0
    for rec in journal.trades:
        if rec.exit_price is None or rec.pnl is None:
            continue
        gross = ((rec.exit_price - rec.entry_price) * rec.quantity
                 if rec.direction == "long"
                 else (rec.entry_price - rec.exit_price) * rec.quantity)
        net = gross - fee * (rec.entry_price + rec.exit_price) * rec.quantity
        old_total += rec.pnl
        new_total += net
        if abs(net - rec.pnl) > 1e-9:
            changed += 1
            rec.pnl = net

    print(f"청산 거래 {len([t for t in journal.trades if t.exit_price is not None])}건 중 "
          f"{changed}건 보정")
    print(f"총 실현손익: {old_total:+.2f} → {new_total:+.2f} USDT "
          f"(수수료 {s.taker_fee_pct}%/편도 반영)")

    if args.dry_run:
        print("(dry-run — 저장하지 않음)")
        return
    journal.save()
    print(f"저장 완료: {Path(s.state_dir) / 'trades.json'}")
    print("→ 대시보드/누적수익률이 실잔고와 맞게 갱신됩니다. (봇/서버 재시작 불필요, "
          "대시보드는 Ctrl+F5)")


if __name__ == "__main__":
    main()
