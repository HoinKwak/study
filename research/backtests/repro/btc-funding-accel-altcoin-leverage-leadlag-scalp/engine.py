"""BTC 펀딩가속 -> 알트 레버리지 유입 후행 스캘프 — 백테스트 엔진.

1단계(선행, BTC): 펀딩 2프린트 연속 가속(같은 부호, |d0|+|d1|>=accel_z*std60) → trigger_time.
2단계(후행, 알트): trigger_time 이후 confirm_window(8h) 이내, 15m 종가가 자기자신 과거 20봉
  Donchian을 트리거 방향으로 돌파 + quote_volume >= vol_confirm_mult * 과거20봉평균 → confirm.
진입: confirm bar 종가 확정 시 신호 → 체결은 다음 15m bar 시가(shift(1), lookahead 방지).
스톱: confirm(신호)봉의 시가(원신호 기준 1회 계산 — 반전 대조군도 이 값을 그대로 부호만 반전해 사용).
청산: ATR(1h,14) 트레일링×atr_trail_mult(직전 확정 극값 기준) 또는 고정 SL(둘 중 유리/타이트한 쪽) +
      시간청산 24h.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get("BFLL_REPO_SRC", str(Path("/home/user/study/src"))))
from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE


@dataclass
class RunConfig:
    accel_z_threshold: float = 1.5
    confirm_window_h: float = 8.0
    donchian_lookback: int = 20
    vol_confirm_mult: float = 1.3
    atr_trail_mult: float = 1.2
    time_exit_h: float = 24.0
    reverse: bool = False          # True면 방향 반전 대조군(스톱도 대칭 재배치)
    no_gate: bool = False          # True면 1단계(BTC트리거) 제거 — 알트 자체 브레이크아웃만
    fee_on: bool = True
    starting_equity: float = 10_000.0


@dataclass
class TradeRec:
    symbol: str
    trigger_time: pd.Timestamp | None
    confirm_time: pd.Timestamp
    direction: str            # "long"/"short" (체결 방향, reverse 반영 후)
    raw_direction: str        # 원신호(BTC 트리거) 방향 — reverse 무관 항상 원신호
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float
    quantity: float
    risk_amount: float
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    exit_reason: str = ""
    pnl: float = 0.0
    fees: float = 0.0
    r_multiple: float = 0.0
    holding_bars: int = 0
    holding_hours: float = 0.0
    entry_idx: int = -1


def _fill(price: float, direction: str, closing: bool) -> float:
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * SLIPPAGE)


def _fee(notional: float) -> float:
    return abs(notional) * TAKER_FEE


def _confirm_events(alt: common.AltSignals, events: pd.DataFrame, cfg: RunConfig
                    ) -> list[dict]:
    """트리거 목록(events)에 대해 confirm_window 내 첫 confirm 시각/방향을 찾는다.

    no_gate=True 이면 events 를 무시하고 알트 자체의 모든 브레이크아웃(방향 자체결정)을
    독립 신호로 사용한다(게이트 없는 대조군, 스펙 폐기조건 (c)).
    """
    df = alt.df
    idx = df.index
    du = alt.don_upper.to_numpy()
    dl = alt.don_lower.to_numpy()
    va = alt.vol_avg.to_numpy()
    close = df["close"].to_numpy()
    qv = df["quote_volume"].to_numpy()
    valid_base = np.isfinite(du) & np.isfinite(dl) & np.isfinite(va)
    vol_ok = qv >= cfg.vol_confirm_mult * va

    out = []
    if cfg.no_gate:
        long_break = valid_base & vol_ok & (close > du)
        short_break = valid_base & vol_ok & (close < dl)
        for i in np.where(long_break)[0]:
            out.append({"trigger_time": None, "confirm_idx": i, "confirm_time": idx[i],
                       "direction": 1})
        for i in np.where(short_break)[0]:
            out.append({"trigger_time": None, "confirm_idx": i, "confirm_time": idx[i],
                       "direction": -1})
        out.sort(key=lambda d: d["confirm_idx"])
        return out

    window = pd.Timedelta(hours=cfg.confirm_window_h)
    n = len(idx)
    for _, row in events.iterrows():
        tt, d = row["trigger_time"], int(row["direction"])
        win_end = tt + window
        # searchsorted: 트리거 시각 이후(포함) 첫 15m bar부터 window 끝까지
        lo = idx.searchsorted(tt, side="left")
        hi = idx.searchsorted(win_end, side="left")
        if lo >= n or lo >= hi:
            continue
        sl = slice(lo, hi)
        if d > 0:
            cond = valid_base[sl] & vol_ok[sl] & (close[sl] > du[sl])
        else:
            cond = valid_base[sl] & vol_ok[sl] & (close[sl] < dl[sl])
        if not cond.any():
            continue
        first = lo + int(np.argmax(cond))
        out.append({"trigger_time": tt, "confirm_idx": first, "confirm_time": idx[first],
                   "direction": d})
    return out


def run_symbol(symbol: str, alt: common.AltSignals, events: pd.DataFrame, cfg: RunConfig,
               settings, risk: RiskManager) -> list[TradeRec]:
    df = alt.df
    n = len(df)
    close = df["close"].to_numpy(float)
    open_ = df["open"].to_numpy(float)
    high = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    idx = df.index
    atr1h = alt.atr1h_on15

    confirms = _confirm_events(alt, events, cfg)
    # confirm_idx 오름차순으로 순차 처리(중첩 신호는 첫 확인만 — 이미 포지션 있으면 스킵)
    confirms.sort(key=lambda d: d["confirm_idx"])

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    trade: TradeRec | None = None
    run_ext: float | None = None
    lev = settings.leverage_for(symbol[:-4] + "/USDT")

    ci_ptr = 0
    i = 0
    pending_entry_idx: int | None = None
    pending_dir_raw: int | None = None
    pending_stop: float | None = None
    pending_trig: pd.Timestamp | None = None
    pending_confirm_t: pd.Timestamp | None = None

    while i < n:
        # 0) 대기 중인 진입 체결(이번 bar 시가) — confirm 다음 bar
        if pending_entry_idx is not None and i == pending_entry_idx and trade is None:
            raw_dir = "long" if pending_dir_raw > 0 else "short"
            final_dir = raw_dir if not cfg.reverse else ("short" if raw_dir == "long" else "long")
            entry_raw = open_[i]
            fill_px = _fill(entry_raw, final_dir, closing=False) if cfg.fee_on else entry_raw
            # 스톱: 원신호 기준 1회 계산(confirm bar 시가와 진입가의 거리) 후 방향에 맞게
            # 대칭 재배치. 방향성 조건(브레이크아웃)으로 선택된 confirm 봉이라, 반전모드에서
            # "그 방향의 자연스러운 극값(반대편 시가)"을 그대로 쓰면 반전 스톱이 부당하게
            # 타이트해진다 — 리스크 거리는 원신호 방향 기준 1회 계산해 대칭 재배치한다.
            risk_dist = abs(fill_px - pending_stop)
            if risk_dist > 0 and np.isfinite(risk_dist) and fill_px > 0:
                if final_dir == "long":
                    stop_final = fill_px - risk_dist
                    dirn = Direction.LONG
                else:
                    stop_final = fill_px + risk_dist
                    dirn = Direction.SHORT
                far_tp = (fill_px + risk_dist * 100 if final_dir == "long"
                         else fill_px - risk_dist * 100)
                plan = risk.build_plan_with_stop(symbol, dirn, fill_px, stop_final, far_tp,
                                                 equity, leverage=lev)
                if plan is not None and plan.quantity > 0:
                    fee0 = _fee(fill_px * plan.quantity) if cfg.fee_on else 0.0
                    trade = TradeRec(symbol=symbol, trigger_time=pending_trig,
                                     confirm_time=pending_confirm_t, direction=final_dir,
                                     raw_direction=raw_dir, entry_time=idx[i],
                                     entry_price=fill_px, stop_price=stop_final,
                                     quantity=plan.quantity, risk_amount=plan.risk_amount,
                                     fees=fee0, entry_idx=i)
                    equity -= fee0
                    run_ext = fill_px
            pending_entry_idx = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            atrv = atr1h[i]
            is_long = trade.direction == "long"
            if is_long:
                trail_level = (run_ext - cfg.atr_trail_mult * atrv) if np.isfinite(atrv) else -np.inf
                eff_stop = max(trade.stop_price, trail_level)
            else:
                trail_level = (run_ext + cfg.atr_trail_mult * atrv) if np.isfinite(atrv) else np.inf
                eff_stop = min(trade.stop_price, trail_level)

            exit_px = None
            reason = ""
            if is_long and l <= eff_stop:
                exit_px = eff_stop
                reason = "stop_loss" if eff_stop <= trade.stop_price + 1e-12 else "trailing_stop"
            elif (not is_long) and h >= eff_stop:
                exit_px = eff_stop
                reason = "stop_loss" if eff_stop >= trade.stop_price - 1e-12 else "trailing_stop"

            if exit_px is None:
                elapsed_h = (idx[i] - trade.entry_time).total_seconds() / 3600.0
                if elapsed_h >= cfg.time_exit_h:
                    exit_px, reason = c, "time_exit"

            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True) if cfg.fee_on else exit_px
                fee1 = _fee(fill_px * trade.quantity) if cfg.fee_on else 0.0
                raw = ((fill_px - trade.entry_price) if is_long
                       else (trade.entry_price - fill_px)) * trade.quantity
                pnl = raw - fee1
                trade.exit_time = idx[i]
                trade.exit_price = fill_px
                trade.pnl = pnl
                trade.fees += fee1
                trade.exit_reason = reason
                trade.holding_bars = i - trade.entry_idx
                trade.holding_hours = (idx[i] - trade.entry_time).total_seconds() / 3600.0
                trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
                equity += pnl
                trades.append(trade)
                trade = None
                run_ext = None
            else:
                run_ext = max(run_ext, h) if is_long else min(run_ext, l)

        # 2) 신규 confirm 신호 처리(포지션/대기 없을 때만) — confirm bar 종가 확정 시점에 판정
        if trade is None and pending_entry_idx is None:
            while ci_ptr < len(confirms) and confirms[ci_ptr]["confirm_idx"] < i:
                ci_ptr += 1
            if ci_ptr < len(confirms) and confirms[ci_ptr]["confirm_idx"] == i:
                cev = confirms[ci_ptr]
                ci_ptr += 1
                if i + 1 < n:
                    pending_entry_idx = i + 1
                    pending_dir_raw = cev["direction"]
                    pending_stop = open_[i]   # confirm(신호)봉 시가 — 원신호 기준 1회 계산
                    pending_trig = cev["trigger_time"]
                    pending_confirm_t = cev["confirm_time"]
        i += 1

    return trades


def load_all_alts(symbols=common.ALT_SYMBOLS, donchian_lookback: int = 20
                  ) -> dict[str, common.AltSignals]:
    out = {}
    for s in symbols:
        a = common.build_alt_signals(s, donchian_lookback=donchian_lookback)
        if a is not None:
            out[s] = a
    return out


def run_all(alts: dict[str, common.AltSignals], events: pd.DataFrame, cfg: RunConfig
           ) -> dict[str, list[TradeRec]]:
    settings = get_settings()
    risk = RiskManager(settings)
    out = {}
    for sym, alt in alts.items():
        out[sym] = run_symbol(sym, alt, events, cfg, settings, risk)
    return out


def trades_to_df(trades: list[TradeRec]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame()
    rows = []
    for t in trades:
        rows.append({
            "symbol": t.symbol, "trigger_time": t.trigger_time, "confirm_time": t.confirm_time,
            "direction": t.direction, "raw_direction": t.raw_direction,
            "entry_time": t.entry_time, "entry_price": t.entry_price,
            "stop_price": t.stop_price, "quantity": t.quantity, "risk_amount": t.risk_amount,
            "exit_time": t.exit_time, "exit_price": t.exit_price, "exit_reason": t.exit_reason,
            "pnl": t.pnl, "fees": t.fees, "r_multiple": t.r_multiple,
            "holding_bars": t.holding_bars, "holding_hours": t.holding_hours,
        })
    return pd.DataFrame(rows)
