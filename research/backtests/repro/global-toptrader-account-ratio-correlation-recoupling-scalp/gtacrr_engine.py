"""[단타] 글로벌 vs 탑트레이더 계정비율 상관 붕괴-재동조 스캘프 — 백테스트 엔진.

체결: 신호봉(i) 확정(shift(1) 관례) -> 다음 1h봉(i+1) 시가 + 슬리피지.
사이징: 계좌 1% 리스크(스톱 거리 기준), 레버리지 무관(리스크 기준 사이징이라 레버리지는 명목에만 영향).
청산 우선순위(매 봉): 1) SL(인트라바) 2) TP-RR(인트라바, 잔량 전량) 3) 테제무효화(종가, 진입 후
invalidation_window 이내 pctile 재붕괴 — 방향 무관 스칼라 조건) 4) 부분익절(종가, pctile 재정상화,
1회성 50%) 5) 시간청산(max_hold).
반전 대조군: SL/TP 는 진입가 대칭 재배치(entry -+ stop_distance 반대), 테제무효화 청산은 방향을
전혀 참조하지 않는 순수 스칼라 조건(pctile<=10)이라 원신호/최종방향 구분이 구조적으로 무의미
(둘 다 동일 결과) — 코드에서도 direction 파라미터를 참조하지 않음을 확인 가능.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

RISK_FRAC = 0.01
TAKER_FEE = 0.0005
SLIPPAGE = 0.0002


@dataclass
class Trade:
    symbol: str
    direction: int          # +1 long, -1 short
    signal_idx: int
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float
    tp_price: float
    stop_distance: float
    qty: float
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    pnl: float = 0.0
    fees: float = 0.0
    reason: str = ""
    holding_bars: int = 0
    partial_taken: bool = False
    r_multiple: float = 0.0


def _fill(price: float, direction: int, closing: bool, slippage: float) -> float:
    adverse = 1 if (direction == 1) != closing else -1
    return price * (1 + adverse * slippage)


def simulate_symbol(symbol: str, df: pd.DataFrame, params: dict,
                     fee: float = TAKER_FEE, slippage: float = SLIPPAGE,
                     reverse: bool = False, disable_invalidation: bool = False,
                     starting_equity: float = 10_000.0,
                     direction_override: dict[int, int] | None = None) -> list[Trade]:
    """df: gtacrr_signals.build_signal_frame() 산출물(1h 인덱스). reverse=True 면 모든 방향 반전
    (SL/TP 대칭 재배치 자동 — stop_distance 는 동일, 진입가 기준 반대편에 재배치됨)."""
    close = df["close"].to_numpy(float)
    high = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    open_ = df["open"].to_numpy(float)
    atr = df["atr14"].to_numpy(float)
    pctile = df["pctile"].to_numpy(float)
    n = len(df)
    idx = df.index

    sig_positions = np.where(df["signal"].to_numpy(bool))[0]
    directions = df["direction"].to_numpy(int)

    trades: list[Trade] = []
    equity = starting_equity
    i_ptr = 0
    trade: Trade | None = None
    max_hold = params["max_hold"]
    inval_win = params["invalidation_window"]
    atr_mult = params["atr_stop_mult"]
    rr = params["rr_target"]
    partial_pctile = params["partial_pctile"]

    active_signal_ptr = 0
    for sig_i in sig_positions:
        entry_i = sig_i + 1
        if entry_i >= n or np.isnan(atr[sig_i]) or atr[sig_i] <= 0:
            continue
        if trade is not None and entry_i <= trade.exit_idx:
            continue  # 포지션 보유 중 -> 겹치는 신호 무시(직전 포지션 청산 전)
        direction = int(directions[sig_i])
        if direction_override is not None and sig_i in direction_override:
            direction = int(direction_override[sig_i])
        if reverse:
            direction = -direction
        stop_dist = atr[sig_i] * atr_mult
        entry_price = _fill(open_[entry_i], direction, closing=False, slippage=slippage)
        stop_price = entry_price - direction * stop_dist
        tp_price = entry_price + direction * stop_dist * rr
        qty = (equity * RISK_FRAC) / stop_dist if stop_dist > 0 else 0.0
        if qty <= 0:
            continue
        entry_fee = fee * abs(entry_price * qty)
        t = Trade(symbol=symbol, direction=direction, signal_idx=sig_i, entry_idx=entry_i,
                  entry_time=idx[entry_i], entry_price=entry_price, stop_price=stop_price,
                  tp_price=tp_price, stop_distance=stop_dist, qty=qty, fees=entry_fee)

        remaining_qty = qty
        partial_pnl = 0.0
        exit_idx = None
        exit_price = None
        reason = ""
        for j in range(entry_i, min(n, entry_i + max_hold + 1)):
            h, l, c = high[j], low[j], close[j]
            hit_sl = (l <= stop_price) if direction == 1 else (h >= stop_price)
            hit_tp = (h >= tp_price) if direction == 1 else (l <= tp_price)
            if hit_sl:
                exit_idx, exit_price, reason = j, stop_price, "stop_loss"
                break
            if hit_tp:
                exit_idx, exit_price, reason = j, tp_price, "take_profit"
                break
            if (not disable_invalidation) and (j - entry_i) < inval_win and j > entry_i:
                p = pctile[j]
                if np.isfinite(p) and p <= params["breakdown_pctile"]:
                    exit_idx, exit_price, reason = j, c, "thesis_invalidation"
                    break
            if (not t.partial_taken) and j > entry_i:
                p = pctile[j]
                if np.isfinite(p) and p >= partial_pctile:
                    half = remaining_qty / 2.0
                    fill_px = _fill(c, direction, closing=True, slippage=slippage)
                    pnl_half = (fill_px - entry_price) * half if direction == 1 \
                        else (entry_price - fill_px) * half
                    fee_half = fee * abs(fill_px * half)
                    partial_pnl += pnl_half - fee_half
                    remaining_qty -= half
                    t.partial_taken = True
            if j - entry_i >= max_hold:
                exit_idx, exit_price, reason = j, c, "time_exit"
                break
        if exit_idx is None:
            exit_idx = min(n - 1, entry_i + max_hold)
            exit_price = close[exit_idx]
            reason = "end_of_window"

        fill_px = _fill(exit_price, direction, closing=True, slippage=slippage)
        exit_fee = fee * abs(fill_px * remaining_qty)
        pnl_final = (fill_px - entry_price) * remaining_qty if direction == 1 \
            else (entry_price - fill_px) * remaining_qty
        total_pnl = pnl_final - exit_fee + partial_pnl - t.fees
        t.exit_idx = exit_idx
        t.exit_time = idx[exit_idx]
        t.pnl = total_pnl
        t.reason = reason
        t.holding_bars = exit_idx - entry_i
        risked = RISK_FRAC * equity
        t.r_multiple = total_pnl / risked if risked > 0 else 0.0
        equity += total_pnl
        trades.append(t)
        trade = t
    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame(columns=["symbol", "direction", "entry_time", "exit_time", "pnl",
                                     "r_multiple", "reason", "holding_bars"])
    rows = []
    for t in trades:
        rows.append(dict(symbol=t.symbol, direction=t.direction, entry_time=t.entry_time,
                         exit_time=t.exit_time, entry_price=t.entry_price, pnl=t.pnl,
                         r_multiple=t.r_multiple, reason=t.reason, holding_bars=t.holding_bars,
                         partial_taken=t.partial_taken))
    return pd.DataFrame(rows)


def pf_r(trades_df: pd.DataFrame) -> float:
    if trades_df.empty:
        return float("nan")
    r = trades_df["r_multiple"]
    wins = r[r > 0].sum()
    losses = -r[r < 0].sum()
    if losses == 0:
        return float("inf") if wins > 0 else float("nan")
    return wins / losses


def t_stat(trades_df: pd.DataFrame) -> float:
    if len(trades_df) < 2:
        return float("nan")
    r = trades_df["r_multiple"].to_numpy(float)
    n = len(r)
    m = r.mean()
    sd = r.std(ddof=1)
    if sd == 0:
        return float("nan")
    return m / (sd / np.sqrt(n))
