"""거래 저널 — 진입/청산 기록을 JSON 으로 영속화하고 성과 통계를 계산.

재시작해도 기록이 유지되며, 대시보드/리포트가 이 데이터를 읽는다.
파일 시각(timestamp)은 외부에서 주입한다(스크립트가 datetime 을 넘겨줌).
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class TradeRecord:
    symbol: str
    direction: str          # 'long' | 'short'
    entry_price: float
    quantity: float
    opened_at: str          # ISO8601
    mode: str               # dry_run / paper / live
    stop_price: float = 0.0
    take_profit: float = 0.0
    order_id: str | None = None
    # 청산 시 채워짐
    exit_price: float | None = None
    closed_at: str | None = None
    pnl: float | None = None
    exit_reason: str = ""

    @property
    def is_open(self) -> bool:
        return self.exit_price is None


class TradeJournal:
    def __init__(self, state_dir: str = "state"):
        self.dir = Path(state_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / "trades.json"
        self.trades: list[TradeRecord] = []
        self._load()

    # --------------------------------------------------------- 영속화

    def _load(self) -> None:
        if self.path.exists():
            try:
                raw = json.loads(self.path.read_text(encoding="utf-8"))
                self.trades = [TradeRecord(**r) for r in raw]
            except Exception:  # noqa: BLE001
                self.trades = []

    def _save(self) -> None:
        self.path.write_text(
            json.dumps([asdict(t) for t in self.trades], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # --------------------------------------------------------- 기록

    def record_open(self, rec: TradeRecord) -> None:
        self.trades.append(rec)
        self._save()

    def record_close(self, symbol: str, exit_price: float, closed_at: str,
                     pnl: float, reason: str) -> TradeRecord | None:
        """해당 심볼의 열린 마지막 거래를 청산 처리."""
        for rec in reversed(self.trades):
            if rec.symbol == symbol and rec.is_open:
                rec.exit_price = exit_price
                rec.closed_at = closed_at
                rec.pnl = pnl
                rec.exit_reason = reason
                self._save()
                return rec
        return None

    def open_trades(self) -> list[TradeRecord]:
        return [t for t in self.trades if t.is_open]

    def closed_trades(self) -> list[TradeRecord]:
        return [t for t in self.trades if not t.is_open]

    # --------------------------------------------------------- 통계

    def stats(self) -> dict[str, Any]:
        closed = self.closed_trades()
        pnls = [t.pnl for t in closed if t.pnl is not None]
        wins = [p for p in pnls if p > 0]
        losses = [p for p in pnls if p < 0]
        gross_win = sum(wins)
        gross_loss = -sum(losses)
        total_pnl = sum(pnls)
        return {
            "total_trades": len(closed),
            "open_trades": len(self.open_trades()),
            "wins": len(wins),
            "losses": len(losses),
            "win_rate": (len(wins) / len(pnls) * 100.0) if pnls else 0.0,
            "total_pnl": total_pnl,
            "avg_win": (gross_win / len(wins)) if wins else 0.0,
            "avg_loss": (gross_loss / len(losses)) if losses else 0.0,
            "profit_factor": (gross_win / gross_loss) if gross_loss > 0 else float("inf"),
            "best": max(pnls) if pnls else 0.0,
            "worst": min(pnls) if pnls else 0.0,
        }
