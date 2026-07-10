"""거래 저널 — 진입/청산 기록을 JSON 으로 영속화하고 성과 통계를 계산.

재시작해도 기록이 유지되며, 대시보드/리포트가 이 데이터를 읽는다.
파일 시각(timestamp)은 외부에서 주입한다(스크립트가 datetime 을 넘겨줌).
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
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
    sleeve: str = "default"   # 소속 슬리브 (swing / mid / scalp)
    stage: int = 1            # 피라미딩 단계 (1: 초기/역추세, 2: 추세확인 추가)
    num_adds: int = 0         # 추가 진입 횟수
    alloc_frac: float = 0.0   # 슬리브 예산 대비 누적 사용 비율 (0~1)
    # 청산 시 채워짐
    exit_price: float | None = None
    closed_at: str | None = None
    pnl: float | None = None
    exit_reason: str = ""

    @property
    def is_open(self) -> bool:
        return self.exit_price is None

    @property
    def holding_seconds(self) -> float | None:
        """오픈~종료 유지 시간(초). 열린 거래는 None."""
        if not self.closed_at:
            return None
        try:
            o = datetime.fromisoformat(self.opened_at)
            c = datetime.fromisoformat(self.closed_at)
            return (c - o).total_seconds()
        except (ValueError, TypeError):
            return None

    def holding_human(self, until: str | None = None) -> str:
        """유지 시간을 사람이 읽기 좋은 문자열로. 열린 거래는 until(현재시각) 기준."""
        end = self.closed_at or until
        if not end:
            return "-"
        try:
            o = datetime.fromisoformat(self.opened_at)
            c = datetime.fromisoformat(end)
            return _fmt_duration((c - o).total_seconds())
        except (ValueError, TypeError):
            return "-"


def _fmt_duration(seconds: float) -> str:
    seconds = int(max(0, seconds))
    d, rem = divmod(seconds, 86400)
    h, rem = divmod(rem, 3600)
    m, _ = divmod(rem, 60)
    if d:
        return f"{d}d {h}h {m}m"
    if h:
        return f"{h}h {m}m"
    return f"{m}m"


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
                     pnl: float, reason: str, sleeve: str | None = None,
                     direction: str | None = None) -> TradeRecord | None:
        """해당 심볼의 열린 거래를 청산 처리.

        헤지 모드/멀티 슬리브에서는 한 심볼에 여러 열린 거래가 있을 수 있으므로,
        sleeve/direction 이 주어지면 그에 맞는 거래를 골라 청산한다.
        """
        for rec in reversed(self.trades):
            if not (rec.symbol == symbol and rec.is_open):
                continue
            if sleeve is not None and rec.sleeve != sleeve:
                continue
            if direction is not None and rec.direction != direction:
                continue
            rec.exit_price = exit_price
            rec.closed_at = closed_at
            rec.pnl = pnl
            rec.exit_reason = reason
            self._save()
            return rec
        return None

    def record_add(self, symbol: str, sleeve: str, direction: str,
                   add_price: float, add_qty: float, new_stop: float,
                   new_stage: int, new_alloc_frac: float,
                   new_take_profit: float | None = None) -> TradeRecord | None:
        """기존 열린 거래에 피라미딩 추가. 평균단가/수량/SL/단계 갱신."""
        for rec in reversed(self.trades):
            if not (rec.symbol == symbol and rec.is_open
                    and rec.sleeve == sleeve and rec.direction == direction):
                continue
            total_qty = rec.quantity + add_qty
            if total_qty <= 0:
                return None
            rec.entry_price = (rec.entry_price * rec.quantity + add_price * add_qty) / total_qty
            rec.quantity = total_qty
            rec.stop_price = new_stop
            rec.stage = new_stage
            rec.num_adds += 1
            rec.alloc_frac = new_alloc_frac
            if new_take_profit is not None:
                rec.take_profit = new_take_profit
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
        holds = [t.holding_seconds for t in closed if t.holding_seconds is not None]
        avg_hold = sum(holds) / len(holds) if holds else 0.0
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
            "avg_holding_sec": avg_hold,
            "avg_holding_human": _fmt_duration(avg_hold) if avg_hold else "-",
        }
