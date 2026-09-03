"""1h 가격충격 → OI 원상복귀 속도 분기(되돌림/지속) 스캘프 엔진.

신호 산출(1h) → 15m 확인·진입 → 15m 청산 시뮬레이션.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

import common as c

TAKER_FEE = c.TAKER_FEE
SLIPPAGE = c.SLIPPAGE


@dataclass
class Config:
    shock_atr_mult: float = 2.0
    reversion_window: int = 3   # 1h봉
    revert_pct: float = 0.4
    breakout_lookback: int = 5  # 1h봉
    atr_trail_mult: float = 1.5
    atr_stop_mult: float = 1.0
    rr_target: float = 1.6
    max_hold_bars: int = 12     # 15m봉 (=3시간)
    fee_on: bool = True         # False=무비용 진단(gross)
    require_ema_confirm: bool = True
    reverse: bool = False           # 반전 대조군: 최종방향 뒤집기(SL/TP 대칭 재배치)
    disable_time_exit: bool = False


@dataclass
class ShockEvent:
    symbol: str
    shock_idx: int          # 1h 인덱스(h1)
    shock_time: pd.Timestamp
    shock_up: bool           # True=상승충격, False=하락충격
    confirm_idx: int         # t+reversion_window 의 1h 인덱스
    confirm_time: pd.Timestamp   # 그 봉의 "종가시각"(오픈+1h) = 판정 확정 시각
    branch: str               # "reversion" | "persistence"
    revert_ratio: float
    oi_pre: float
    oi_shock: float
    oi_now: float
    orig_direction: str | None   # "long"|"short"|None(신호 무효)


@dataclass
class Trade:
    symbol: str
    event: ShockEvent
    direction: str            # 최종 체결 방향(반전모드면 뒤집힘)
    orig_direction: str        # 원신호 방향(반전 전)
    entry_time: pd.Timestamp
    entry_idx: int             # 15m 인덱스
    entry_price: float
    stop_price: float
    fixed_target: float
    atr_at_entry: float
    exit_time: pd.Timestamp = None
    exit_price: float = None
    reason: str = ""
    holding_bars: int = 0
    pnl: float = 0.0
    risk_amount: float = 0.0
    r_multiple: float = 0.0
    fees: float = 0.0


def _fee(notional: float, fee_on: bool) -> float:
    return notional * TAKER_FEE if fee_on else 0.0


def _fill(px: float, direction: str, closing: bool, fee_on: bool) -> float:
    """슬리피지 반영 체결가. fee_on=False 면 슬리피지도 0(완전 무비용 진단)."""
    if not fee_on:
        return px
    slip = px * SLIPPAGE
    if direction == "long":
        return px + slip if not closing else px - slip
    else:
        return px - slip if not closing else px + slip


def detect_events(symbol: str, sd: c.SymbolData, cfg: Config) -> list[ShockEvent]:
    """1h 봉 기준 충격 트리거 + OI 분류(t+reversion_window 확정) 이벤트 목록."""
    h1 = sd.h1
    atr1h = sd.atr1h
    oi = sd.oi1h.reindex(h1.index)
    n = len(h1)
    w = cfg.reversion_window
    idx = h1.index
    open_ = h1["open"].to_numpy()
    close_ = h1["close"].to_numpy()
    high_ = h1["high"].to_numpy()
    low_ = h1["low"].to_numpy()
    atr_ = atr1h.to_numpy()
    oi_ = oi.to_numpy()

    events: list[ShockEvent] = []
    warmup = 20  # ATR(14) 안정화 여유
    for t in range(warmup, n - w):
        a = atr_[t]
        if not np.isfinite(a) or a <= 0:
            continue
        body = abs(close_[t] - open_[t])
        if body < cfg.shock_atr_mult * a:
            continue
        shock_up = close_[t] > open_[t]
        # OI 분류: oi_pre = mean(oi[t-3..t-1]), oi_shock = oi[t], oi_now = oi[t+w]
        if t - 3 < 0:
            continue
        pre_vals = oi_[t - 3:t]
        oi_shock = oi_[t]
        oi_now = oi_[t + w]
        if np.any(~np.isfinite(pre_vals)) or not np.isfinite(oi_shock) or not np.isfinite(oi_now):
            continue
        oi_pre = float(np.mean(pre_vals))
        denom = abs(oi_shock - oi_pre)
        if denom <= 0:
            # 충격 전후 OI 변화가 0 → 분류 불능(둘 다 사실상 미변동), reversion 취급하지 않고 skip
            continue
        ratio = abs(oi_now - oi_pre) / denom
        branch = "reversion" if ratio <= cfg.revert_pct else "persistence"

        confirm_idx = t + w
        confirm_time = idx[confirm_idx] + pd.Timedelta(hours=1)  # 그 봉 종가시각

        # 방향 결정 (스펙 §진입규칙)
        orig_direction = None
        lb = cfg.breakout_lookback
        if branch == "reversion":
            if confirm_idx - lb < 0:
                continue
            hh = np.max(high_[confirm_idx - lb:confirm_idx])
            ll = np.min(low_[confirm_idx - lb:confirm_idx])
            c3 = close_[confirm_idx]
            if not shock_up and c3 > hh:
                orig_direction = "long"
            elif shock_up and c3 < ll:
                orig_direction = "short"
        else:  # persistence
            c3 = close_[confirm_idx]
            cshock = close_[t]
            if not shock_up and c3 < cshock:
                orig_direction = "short"
            elif shock_up and c3 > cshock:
                orig_direction = "long"

        if orig_direction is None:
            continue  # 분류는 됐으나 방향조건 미충족 → 진입신호 아님(트리거는 아래 별도 카운트에 잡힘)

        events.append(ShockEvent(
            symbol=symbol, shock_idx=t, shock_time=idx[t], shock_up=shock_up,
            confirm_idx=confirm_idx, confirm_time=confirm_time, branch=branch,
            revert_ratio=ratio, oi_pre=oi_pre, oi_shock=oi_shock, oi_now=oi_now,
            orig_direction=orig_direction,
        ))
    return events


@dataclass
class RawShock:
    symbol: str
    shock_idx: int
    shock_time: pd.Timestamp
    shock_up: bool


def detect_raw_shocks(symbol: str, sd: c.SymbolData, cfg: Config) -> list[RawShock]:
    """OI 분류·브레이크아웃 확인 없이 ATR 충격 조건만 적용한 원시 충격 목록
    (폐기조건(b) 즉시진입 대조군용 — '지연'이 주는 부가가치를 격리하기 위해 지연에 종속된
    정보(OI 분류·브레이크아웃)는 아예 참조하지 않는다)."""
    h1 = sd.h1
    atr1h = sd.atr1h
    n = len(h1)
    idx = h1.index
    open_ = h1["open"].to_numpy()
    close_ = h1["close"].to_numpy()
    atr_ = atr1h.to_numpy()
    out = []
    warmup = 20
    for t in range(warmup, n - cfg.reversion_window):
        a = atr_[t]
        if not np.isfinite(a) or a <= 0:
            continue
        body = abs(close_[t] - open_[t])
        if body < cfg.shock_atr_mult * a:
            continue
        out.append(RawShock(symbol=symbol, shock_idx=t, shock_time=idx[t],
                             shock_up=close_[t] > open_[t]))
    return out


def simulate_immediate(symbol: str, sd: c.SymbolData, shocks: list[RawShock], cfg: Config,
                        frame: str) -> list[Trade]:
    """즉시진입 대조군: 충격봉 종가 직후(지연 없이) frame 방향으로 진입.
    frame="persistence": 충격방향 그대로(하락충격→숏, 상승충격→롱).
    frame="reversion":   충격 반대방향(하락충격→롱, 상승충격→숏)."""
    m15 = sd.m15
    atr15m = sd.atr15m
    ema20 = sd.ema20_15m
    idx15 = m15.index
    open_ = m15["open"].to_numpy()
    high_ = m15["high"].to_numpy()
    low_ = m15["low"].to_numpy()
    close_ = m15["close"].to_numpy()
    atr_ = atr15m.to_numpy()
    ema_ = ema20.to_numpy()
    n15 = len(m15)

    trades: list[Trade] = []
    for sh in shocks:
        decide_time = sh.shock_time + pd.Timedelta(hours=1)  # 충격봉 종가시각
        decide_pos = _entry_15m_idx(m15, decide_time)
        if decide_pos is None or decide_pos < 2 or decide_pos + 1 >= n15:
            continue
        if frame == "persistence":
            final_direction = "long" if sh.shock_up else "short"
        else:  # reversion
            final_direction = "short" if sh.shock_up else "long"

        if cfg.require_ema_confirm:
            e_now = ema_[decide_pos - 1]
            e_prev = ema_[decide_pos - 2]
            if not (np.isfinite(e_now) and np.isfinite(e_prev)):
                continue
            slope_up = e_now > e_prev
            if final_direction == "long" and not slope_up:
                continue
            if final_direction == "short" and slope_up:
                continue

        entry_pos = decide_pos
        entry_raw = open_[entry_pos]
        if not np.isfinite(entry_raw) or entry_raw <= 0:
            continue
        atr_entry = atr_[decide_pos - 1]
        if not np.isfinite(atr_entry) or atr_entry <= 0:
            continue

        stop_dist = cfg.atr_stop_mult * atr_entry
        fill_px = _fill(entry_raw, final_direction, closing=False, fee_on=cfg.fee_on)
        if final_direction == "long":
            stop_price = fill_px - stop_dist
            fixed_target = fill_px + stop_dist * cfg.rr_target
        else:
            stop_price = fill_px + stop_dist
            fixed_target = fill_px - stop_dist * cfg.rr_target

        fake_ev = ShockEvent(symbol=symbol, shock_idx=sh.shock_idx, shock_time=sh.shock_time,
                             shock_up=sh.shock_up, confirm_idx=sh.shock_idx,
                             confirm_time=decide_time, branch=f"immediate_{frame}",
                             revert_ratio=float("nan"), oi_pre=float("nan"),
                             oi_shock=float("nan"), oi_now=float("nan"),
                             orig_direction=final_direction)
        trade = Trade(symbol=symbol, event=fake_ev, direction=final_direction,
                      orig_direction=final_direction, entry_time=idx15[entry_pos],
                      entry_idx=entry_pos, entry_price=fill_px, stop_price=stop_price,
                      fixed_target=fixed_target, atr_at_entry=atr_entry)

        risk_amount = abs(fill_px - stop_price)
        peak = fill_px
        exit_px = None
        reason = ""
        exit_i = entry_pos
        max_i = min(n15 - 1, entry_pos + cfg.max_hold_bars)
        for i in range(entry_pos, max_i + 1):
            h, l = high_[i], low_[i]
            offset = i - entry_pos
            if final_direction == "long":
                peak = max(peak, h)
                trail_stop = peak - cfg.atr_trail_mult * atr_[i] if np.isfinite(atr_[i]) else -np.inf
                eff_stop = max(stop_price, trail_stop)
                if l <= eff_stop:
                    exit_px, reason = eff_stop, ("stop_loss" if eff_stop <= stop_price + 1e-9 else "trailing")
                    exit_i = i
                    break
                if h >= fixed_target:
                    exit_px, reason = fixed_target, "take_profit"
                    exit_i = i
                    break
            else:
                peak = min(peak, l)
                trail_stop = peak + cfg.atr_trail_mult * atr_[i] if np.isfinite(atr_[i]) else np.inf
                eff_stop = min(stop_price, trail_stop)
                if h >= eff_stop:
                    exit_px, reason = eff_stop, ("stop_loss" if eff_stop >= stop_price - 1e-9 else "trailing")
                    exit_i = i
                    break
                if l <= fixed_target:
                    exit_px, reason = fixed_target, "take_profit"
                    exit_i = i
                    break
            if offset >= cfg.max_hold_bars:
                exit_px, reason = close_[i], "time_exit"
                exit_i = i
                break
        if exit_px is None:
            exit_px, reason = close_[max_i], "time_exit_eod"
            exit_i = max_i

        fill_exit = _fill(exit_px, final_direction, closing=True, fee_on=cfg.fee_on)
        entry_fee = _fee(fill_px, cfg.fee_on)
        exit_fee = _fee(fill_exit, cfg.fee_on)
        raw = (fill_exit - fill_px) if final_direction == "long" else (fill_px - fill_exit)
        pnl_pct = raw - entry_fee - exit_fee
        trade.exit_time = idx15[exit_i]
        trade.exit_price = fill_exit
        trade.reason = reason
        trade.holding_bars = exit_i - entry_pos
        trade.risk_amount = risk_amount
        trade.pnl = pnl_pct
        trade.r_multiple = pnl_pct / risk_amount if risk_amount > 0 else 0.0
        trades.append(trade)
    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    rows = []
    for tr in trades:
        rows.append(dict(
            symbol=tr.symbol, branch=tr.event.branch, shock_up=tr.event.shock_up,
            orig_direction=tr.orig_direction, direction=tr.direction,
            shock_time=tr.event.shock_time, confirm_time=tr.event.confirm_time,
            entry_time=tr.entry_time, exit_time=tr.exit_time, entry_price=tr.entry_price,
            exit_price=tr.exit_price, reason=tr.reason, holding_bars=tr.holding_bars,
            r_multiple=tr.r_multiple, pnl=tr.pnl, revert_ratio=tr.event.revert_ratio,
            oi_pre=tr.event.oi_pre, oi_shock=tr.event.oi_shock, oi_now=tr.event.oi_now,
            period=c.period_of(tr.entry_time),
        ))
    return pd.DataFrame(rows)


def detect_all_shocks(symbol: str, sd: c.SymbolData, cfg: Config) -> pd.DataFrame:
    """방향조건 미충족분까지 포함한 전체 충격+분류 표(폐기조건(a) 배경분포·빈도 실측용)."""
    h1 = sd.h1
    atr1h = sd.atr1h
    oi = sd.oi1h.reindex(h1.index)
    n = len(h1)
    w = cfg.reversion_window
    idx = h1.index
    open_ = h1["open"].to_numpy()
    close_ = h1["close"].to_numpy()
    atr_ = atr1h.to_numpy()
    oi_ = oi.to_numpy()
    rows = []
    warmup = 20
    for t in range(warmup, n - w):
        a = atr_[t]
        if not np.isfinite(a) or a <= 0:
            continue
        body = abs(close_[t] - open_[t])
        if body < cfg.shock_atr_mult * a:
            continue
        if t - 3 < 0:
            continue
        pre_vals = oi_[t - 3:t]
        oi_shock = oi_[t]
        oi_now = oi_[t + w]
        if np.any(~np.isfinite(pre_vals)) or not np.isfinite(oi_shock) or not np.isfinite(oi_now):
            continue
        oi_pre = float(np.mean(pre_vals))
        denom = abs(oi_shock - oi_pre)
        if denom <= 0:
            continue
        ratio = abs(oi_now - oi_pre) / denom
        branch = "reversion" if ratio <= cfg.revert_pct else "persistence"
        rows.append(dict(symbol=symbol, shock_time=idx[t], shock_idx=t, branch=branch,
                          revert_ratio=ratio, shock_up=close_[t] > open_[t]))
    return pd.DataFrame(rows)


def _entry_15m_idx(m15: pd.DataFrame, confirm_time: pd.Timestamp) -> int | None:
    """confirm_time(1h봉 종가시각, 15m 경계와 정렬) 시각에 시작하는 15m봉의 정수 인덱스."""
    pos = m15.index.searchsorted(confirm_time)
    if pos >= len(m15) or m15.index[pos] != confirm_time:
        return None
    return int(pos)


def simulate_symbol(symbol: str, sd: c.SymbolData, events: list[ShockEvent], cfg: Config
                     ) -> list[Trade]:
    m15 = sd.m15
    atr15m = sd.atr15m
    ema20 = sd.ema20_15m
    idx15 = m15.index
    open_ = m15["open"].to_numpy()
    high_ = m15["high"].to_numpy()
    low_ = m15["low"].to_numpy()
    close_ = m15["close"].to_numpy()
    atr_ = atr15m.to_numpy()
    ema_ = ema20.to_numpy()
    n15 = len(m15)

    trades: list[Trade] = []
    for ev in events:
        decide_pos = _entry_15m_idx(m15, ev.confirm_time)
        if decide_pos is None or decide_pos < 1 or decide_pos + 1 >= n15:
            continue
        # 룩어헤드 방지: 진입 판정 시각은 1h 확정시각(ev.confirm_time) 이후여야 함
        assert idx15[decide_pos] >= ev.confirm_time

        orig_direction = ev.orig_direction
        final_direction = orig_direction if not cfg.reverse else (
            "short" if orig_direction == "long" else "long")

        # 15m EMA20 기울기 확인(진입 판정에 쓰는 마지막 확정봉 = decide_pos-1).
        # ⭐반전모드에서도 "신호 자체가 유효한가"의 게이트는 원신호(orig_direction) 기준으로
        # 평가한다 — final_direction(반전 후 실제 체결방향) 기준으로 게이트를 걸면, 충격 직후
        # EMA20 이 충격 자신의 모멘텀 방향으로 기울어 있을 확률이 구조적으로 높아 반전모드
        # 진입이 사실상 전멸(n=0)하는 아티팩트가 생긴다(실측 확인). SL/TP·청산조건만 최종방향
        # 기준으로 뒤집는다.
        gate_direction = orig_direction
        if cfg.require_ema_confirm:
            e_now = ema_[decide_pos - 1]
            e_prev = ema_[decide_pos - 2] if decide_pos - 2 >= 0 else np.nan
            if not (np.isfinite(e_now) and np.isfinite(e_prev)):
                continue
            slope_up = e_now > e_prev
            if gate_direction == "long" and not slope_up:
                continue
            if gate_direction == "short" and slope_up:
                continue

        entry_pos = decide_pos  # shift(1): 확정봉 다음 15m봉 시가에 체결
        entry_raw = open_[entry_pos]
        if not np.isfinite(entry_raw) or entry_raw <= 0:
            continue
        atr_entry = atr_[decide_pos - 1]
        if not np.isfinite(atr_entry) or atr_entry <= 0:
            continue

        # ⭐반전모드: 리스크거리는 원신호 기준 1회 계산 후 대칭 재배치(진입확인봉이 방향편향돼
        # 반전쪽 스톱이 저절로 타이트해지는 함정 회피).
        stop_dist = cfg.atr_stop_mult * atr_entry
        fill_px = _fill(entry_raw, final_direction, closing=False, fee_on=cfg.fee_on)
        if final_direction == "long":
            stop_price = fill_px - stop_dist
            fixed_target = fill_px + stop_dist * cfg.rr_target
        else:
            stop_price = fill_px + stop_dist
            fixed_target = fill_px - stop_dist * cfg.rr_target

        trade = Trade(symbol=symbol, event=ev, direction=final_direction,
                      orig_direction=orig_direction, entry_time=idx15[entry_pos],
                      entry_idx=entry_pos, entry_price=fill_px, stop_price=stop_price,
                      fixed_target=fixed_target, atr_at_entry=atr_entry)

        risk_amount = abs(fill_px - stop_price)
        peak = fill_px
        exit_px = None
        reason = ""
        exit_i = entry_pos
        max_i = min(n15 - 1, entry_pos + cfg.max_hold_bars)
        for i in range(entry_pos, max_i + 1):
            h, l = high_[i], low_[i]
            offset = i - entry_pos
            if final_direction == "long":
                peak = max(peak, h)
                trail_stop = peak - cfg.atr_trail_mult * atr_[i] if np.isfinite(atr_[i]) else -np.inf
                eff_stop = max(stop_price, trail_stop)
                if l <= eff_stop:
                    exit_px, reason = eff_stop, ("stop_loss" if eff_stop <= stop_price + 1e-9 else "trailing")
                    exit_i = i
                    break
                if h >= fixed_target:
                    exit_px, reason = fixed_target, "take_profit"
                    exit_i = i
                    break
            else:
                peak = min(peak, l)
                trail_stop = peak + cfg.atr_trail_mult * atr_[i] if np.isfinite(atr_[i]) else np.inf
                eff_stop = min(stop_price, trail_stop)
                if h >= eff_stop:
                    exit_px, reason = eff_stop, ("stop_loss" if eff_stop >= stop_price - 1e-9 else "trailing")
                    exit_i = i
                    break
                if l <= fixed_target:
                    exit_px, reason = fixed_target, "take_profit"
                    exit_i = i
                    break
            if not cfg.disable_time_exit and offset >= cfg.max_hold_bars:
                exit_px, reason = close_[i], "time_exit"
                exit_i = i
                break
        if exit_px is None:
            exit_px, reason = close_[max_i], "time_exit_eod"
            exit_i = max_i

        fill_exit = _fill(exit_px, final_direction, closing=True, fee_on=cfg.fee_on)
        entry_fee = _fee(fill_px, cfg.fee_on)
        exit_fee = _fee(fill_exit, cfg.fee_on)
        raw = (fill_exit - fill_px) if final_direction == "long" else (fill_px - fill_exit)
        pnl_pct = raw - entry_fee - exit_fee   # 가격단위(1단위 명목당) 순손익
        trade.exit_time = idx15[exit_i]
        trade.exit_price = fill_exit
        trade.reason = reason
        trade.holding_bars = exit_i - entry_pos
        trade.risk_amount = risk_amount
        trade.pnl = pnl_pct
        trade.r_multiple = pnl_pct / risk_amount if risk_amount > 0 else 0.0
        trades.append(trade)
    return trades


def run(symbols: list[str], data: dict[str, c.SymbolData], cfg: Config
        ) -> tuple[pd.DataFrame, dict[str, list[ShockEvent]]]:
    all_trades = []
    all_events = {}
    for sym in symbols:
        sd = data.get(sym)
        if sd is None:
            continue
        events = detect_events(sym, sd, cfg)
        all_events[sym] = events
        trades = simulate_symbol(sym, sd, events, cfg)
        all_trades.extend(trades)
    return trades_to_df(all_trades), all_events
