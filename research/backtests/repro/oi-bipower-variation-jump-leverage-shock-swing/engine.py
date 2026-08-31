"""OI Bipower Variation 점프탐지 — 레버리지쇼크 스윙. 백테스트 엔진.

신호일 t(1d 봉, UTC 캘린더일) 종가 확정 시점에 점프+가격확인 판정(룩어헤드 없음)
→ t+1 일봉 시가에 진입(shift(1) 진입). 청산: SL/TP 인트라바(고저, 손절우선), 진입 다음날
(offset=1) 1회 테제무효화 판정(그날 종가), 시간청산(offset>=max_hold_days, 그날 종가).

mode:
  "base"        — 채택안: OI-JR 트리거 + 가격확인, 방향=신호일 가격변화 부호
  "price_swap"  — 핵심 대조군: 트리거를 가격기반 JR(px_jr)로 교체(그 외 전부 동일) — 동어반복 점검
  "reverse"     — 방향반전 대조군: 최종 체결방향 반전, 무효화 판정도 최종방향 기준(신규 규칙 준수)
  "no_invalidation" — base 와 동일하나 테제무효화 청산만 비활성(제3의 대안, 규칙 준수)
  "placebo"     — 무작위 시점 진입 플라시보(빈도·기간 매칭)
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import hashlib
import numpy as np
import pandas as pd

import os  # noqa: E402
sys.path.insert(0, os.environ.get(
    "OIBV_REPO_SRC", str(Path(__file__).resolve().parents[4] / "src")))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE


@dataclass
class TradeRec:
    symbol: str
    direction: str
    orig_direction: str
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float
    take_profit: float
    quantity: float
    risk_amount: float
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    pnl: float = 0.0
    fees: float = 0.0
    r_multiple: float = 0.0
    reason: str = ""
    holding_bars: int = 0


def _fill(price: float, direction: str, closing: bool, fee_on: bool) -> float:
    if not fee_on:
        return price
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * SLIPPAGE)


def _fee(notional: float, fee_on: bool) -> float:
    return abs(notional) * TAKER_FEE if fee_on else 0.0


@dataclass
class RunConfig:
    pctile_window: int = 90       # 관측치 개수 기준(결측일 제외 후)
    jump_pctile: float = 90.0     # 상위 10%ile
    price_confirm_th: float = 1.5  # %
    atr_stop_mult: float = 1.5
    rr_target: float = 2.0
    max_hold_days: int = 3
    invalidation_pctile_lo: float = 50.0
    mode: str = "base"
    fee_on: bool = True
    starting_equity: float = 10_000.0
    placebo_seed: int = 0


def _build_trigger_arrays(sd: common.SymbolData, cfg: RunConfig):
    """d1(1d klines) index 에 정렬된 배열들 반환:
    oi_pctile, px_pctile(둘 다 rolling pctile, NaN 가능), day_ret_pct, atr14.
    """
    idx = sd.d1.index
    oi_pctile_s = common.rolling_pctile_of_jr(sd.oi_jr["jr"], cfg.pctile_window)
    px_pctile_s = common.rolling_pctile_of_jr(sd.px_jr["jr"], cfg.pctile_window)
    oi_pctile = oi_pctile_s.reindex(idx)
    px_pctile = px_pctile_s.reindex(idx)
    day_ret = sd.day_ret_pct.reindex(idx)
    atr = sd.atr14_1d.reindex(idx)
    return oi_pctile.to_numpy(float), px_pctile.to_numpy(float), day_ret.to_numpy(float), \
        atr.to_numpy(float)


def run_symbol(symbol: str, sd: common.SymbolData, cfg: RunConfig, settings, risk: RiskManager
               ) -> list[TradeRec]:
    df = sd.d1
    n = len(df)
    if n < cfg.pctile_window + 10:
        return []
    close = df["close"].to_numpy(float)
    high = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    open_ = df["open"].to_numpy(float)
    idx = df.index

    oi_pctile, px_pctile, day_ret, atr = _build_trigger_arrays(sd, cfg)
    trigger_pctile = px_pctile if cfg.mode == "price_swap" else oi_pctile

    warmup = 0
    for i in range(n):
        if np.isfinite(trigger_pctile[i]):
            warmup = i
            break

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    trade: TradeRec | None = None
    pending: dict | None = None
    lev = settings.leverage_for(symbol[:-4] + "/USDT")

    # ⚠️2026-08-31 리뷰어 적발: 원래 `hash(symbol)`(파이썬 내장 해시)을 시드에 썼는데
    #   PYTHONHASHSEED가 고정돼 있지 않아 **문자열 해시가 프로세스마다 달라져** placebo
    #   결과가 재실행마다 바뀌었다(n=274~317·PF 0.99~1.31·t -0.06~+1.74). 판정에는 영향이
    #   없었으나 재현 커맨드가 리포트 수치를 되살리지 못하는 결함이었다.
    #   → 프로세스 간 안정적인 blake2b 고정 해시로 교체한다.
    _h = int(hashlib.blake2b(symbol.encode(), digest_size=4).hexdigest(), 16)
    rng = np.random.default_rng(cfg.placebo_seed + _h % 10_000)
    placebo_mask = None
    if cfg.mode == "placebo":
        base_trigger = (oi_pctile >= cfg.jump_pctile) & (np.abs(day_ret) >= cfg.price_confirm_th)
        n_events = int(np.nansum(base_trigger[warmup:]))
        eligible = np.arange(warmup, n - 1)
        chosen = rng.choice(eligible, size=min(n_events, len(eligible)), replace=False) \
            if n_events > 0 and len(eligible) > 0 else np.array([], dtype=int)
        placebo_mask = np.zeros(n, dtype=bool)
        placebo_mask[chosen] = True

    for i in range(warmup, n):
        # 0) 대기 중인 진입 체결(이번 bar 시가)
        if pending is not None and trade is None:
            sidx = pending["signal_idx"]
            entry_raw = open_[i]
            direction = pending["direction"]
            fill_px = _fill(entry_raw, direction, closing=False, fee_on=cfg.fee_on)
            atr_v = atr[sidx]
            stop_dist = cfg.atr_stop_mult * atr_v
            if stop_dist > 0 and np.isfinite(stop_dist) and fill_px > 0:
                if direction == "long":
                    stop_price = fill_px - stop_dist
                    tp = fill_px + stop_dist * cfg.rr_target
                    dirn = Direction.LONG
                else:
                    stop_price = fill_px + stop_dist
                    tp = fill_px - stop_dist * cfg.rr_target
                    dirn = Direction.SHORT
                plan = risk.build_plan_with_stop(symbol, dirn, fill_px, stop_price, tp, equity,
                                                 leverage=lev)
                if plan is not None and plan.quantity > 0:
                    fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
                    trade = TradeRec(symbol=symbol, direction=direction,
                                     orig_direction=pending["orig_direction"],
                                     entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                     stop_price=stop_price, take_profit=tp,
                                     quantity=plan.quantity, risk_amount=plan.risk_amount,
                                     fees=fee0)
                    equity -= fee0
            pending = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            exit_px = None; reason = ""
            if trade.direction == "long":
                if l <= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
                elif h >= trade.take_profit:
                    exit_px, reason = trade.take_profit, "take_profit"
            else:
                if h >= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
                elif l <= trade.take_profit:
                    exit_px, reason = trade.take_profit, "take_profit"
            offset = i - trade.entry_idx
            # 1b) 테제무효화(진입 다음날 딱 1회 판정) — 최종 체결방향(trade.direction) 기준
            #     (⚠️신규 규칙 준수: reverse 모드에서도 orig_direction 이 아닌 최종방향 참조)
            if exit_px is None and offset == 1 and cfg.mode != "no_invalidation":
                src_pctile = px_pctile if cfg.mode == "price_swap" else oi_pctile
                p = src_pctile[i]
                r = day_ret[i]
                if np.isfinite(p) and np.isfinite(r) and p <= cfg.invalidation_pctile_lo:
                    opposite = (trade.direction == "long" and r < 0) or \
                               (trade.direction == "short" and r > 0)
                    if opposite:
                        exit_px, reason = c, "thesis_invalidation"
            # 1c) 시간청산
            if exit_px is None and offset >= cfg.max_hold_days:
                exit_px, reason = c, "time_exit"
            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True, fee_on=cfg.fee_on)
                fee1 = _fee(fill_px * trade.quantity, cfg.fee_on)
                raw = ((fill_px - trade.entry_price) if trade.direction == "long"
                       else (trade.entry_price - fill_px)) * trade.quantity
                pnl = raw - fee1
                trade.exit_idx = i; trade.exit_time = idx[i]; trade.exit_price = fill_px
                trade.pnl = pnl; trade.fees += fee1; trade.reason = reason
                trade.holding_bars = offset
                trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
                equity += pnl
                trades.append(trade)
                trade = None

        # 2) 신규 진입 신호 판정(이번 bar 종가 기준, 체결은 다음 bar 시가)
        if trade is None and pending is None and i + 1 < n:
            if cfg.mode == "placebo":
                if placebo_mask[i]:
                    r = day_ret[i]
                    orig_dir = "long" if (np.isfinite(r) and r >= 0) else "short"
                    pending = {"direction": orig_dir, "orig_direction": orig_dir, "signal_idx": i}
                continue
            p = trigger_pctile[i]
            r = day_ret[i]
            is_jump = np.isfinite(p) and p >= cfg.jump_pctile
            confirmed = is_jump and np.isfinite(r) and abs(r) >= cfg.price_confirm_th
            if confirmed:
                orig_dir = "long" if r > 0 else "short"
                exec_dir = orig_dir
                if cfg.mode == "reverse":
                    exec_dir = "short" if orig_dir == "long" else "long"
                pending = {"direction": exec_dir, "orig_direction": orig_dir, "signal_idx": i}

    return trades


def run_symbol_quiet_follow(symbol: str, sd: common.SymbolData, cfg: RunConfig, settings,
                            risk: RiskManager, follow_window: int = 3) -> list[TradeRec]:
    """'조용한 점프' 서브셋 전용: 점프일이되 가격확인 미충족인 날 이후 follow_window 일 내
    첫 브레이크아웃(|Δ%|>=price_confirm_th)이 나오면 그 방향으로 다음날 시가 진입.
    그 외 청산 규칙은 base 와 동일(테제무효화는 이 변형에선 미적용 — 트리거 자체가 이미
    '지연 확인'을 내장하므로 이중 적용하지 않음, 스펙 §67행 각주에 따른 별도 서브전략)."""
    df = sd.d1
    n = len(df)
    if n < cfg.pctile_window + 10:
        return []
    close = df["close"].to_numpy(float)
    high = df["high"].to_numpy(float)
    low = df["low"].to_numpy(float)
    open_ = df["open"].to_numpy(float)
    idx = df.index
    oi_pctile, _px_pctile, day_ret, atr = _build_trigger_arrays(sd, cfg)

    warmup = 0
    for i in range(n):
        if np.isfinite(oi_pctile[i]):
            warmup = i
            break

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    trade: TradeRec | None = None
    pending: dict | None = None
    watching: dict | None = None
    lev = settings.leverage_for(symbol[:-4] + "/USDT")

    for i in range(warmup, n):
        if pending is not None and trade is None:
            sidx = pending["signal_idx"]
            entry_raw = open_[i]
            direction = pending["direction"]
            fill_px = _fill(entry_raw, direction, closing=False, fee_on=cfg.fee_on)
            atr_v = atr[sidx]
            stop_dist = cfg.atr_stop_mult * atr_v
            if stop_dist > 0 and np.isfinite(stop_dist) and fill_px > 0:
                if direction == "long":
                    stop_price = fill_px - stop_dist
                    tp = fill_px + stop_dist * cfg.rr_target
                    dirn = Direction.LONG
                else:
                    stop_price = fill_px + stop_dist
                    tp = fill_px - stop_dist * cfg.rr_target
                    dirn = Direction.SHORT
                plan = risk.build_plan_with_stop(symbol, dirn, fill_px, stop_price, tp, equity,
                                                 leverage=lev)
                if plan is not None and plan.quantity > 0:
                    fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
                    trade = TradeRec(symbol=symbol, direction=direction, orig_direction=direction,
                                     entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                     stop_price=stop_price, take_profit=tp,
                                     quantity=plan.quantity, risk_amount=plan.risk_amount,
                                     fees=fee0)
                    equity -= fee0
            pending = None

        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            exit_px = None; reason = ""
            if trade.direction == "long":
                if l <= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
                elif h >= trade.take_profit:
                    exit_px, reason = trade.take_profit, "take_profit"
            else:
                if h >= trade.stop_price:
                    exit_px, reason = trade.stop_price, "stop_loss"
                elif l <= trade.take_profit:
                    exit_px, reason = trade.take_profit, "take_profit"
            offset = i - trade.entry_idx
            if exit_px is None and offset >= cfg.max_hold_days:
                exit_px, reason = c, "time_exit"
            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True, fee_on=cfg.fee_on)
                fee1 = _fee(fill_px * trade.quantity, cfg.fee_on)
                raw = ((fill_px - trade.entry_price) if trade.direction == "long"
                       else (trade.entry_price - fill_px)) * trade.quantity
                pnl = raw - fee1
                trade.exit_idx = i; trade.exit_time = idx[i]; trade.exit_price = fill_px
                trade.pnl = pnl; trade.fees += fee1; trade.reason = reason
                trade.holding_bars = offset
                trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
                equity += pnl
                trades.append(trade)
                trade = None

        if trade is None and pending is None and i + 1 < n:
            r = day_ret[i]
            # ⚠️자체발견 버그 수정: 최초 구현이 "조용한 점프일 i 로부터 i+1..i+follow_window 를
            # for 문으로 미리 훑어(scan-ahead) 브레이크아웃일 j 를 찾은 뒤 즉시 pending 을 걸었다"
            # — 이는 아직 도래하지 않은 미래 봉(j)의 수익률을 i 시점에 미리 참조하는 룩어헤드였다
            # (수정 전 재현: FULL PF(R)=7.358, t=+13.4 — 실제로 이 버그판을 되돌려 재현 확인함).
            # 수정: 매 bar 마다 "감시 중(watching)" 상태만 이월하고, 그 bar 자신의 종가 확정
            # 수익률(day_ret[i])만으로 그 bar 에 브레이크아웃이 발생했는지 판정한다(전형적인
            # signal-at-close-i, fill-at-open-(i+1) 패턴과 동일한 인과구조).
            if watching is not None:
                if i > watching["start"] and i <= watching["expire"]:
                    if np.isfinite(r) and abs(r) >= cfg.price_confirm_th:
                        orig_dir = "long" if r > 0 else "short"
                        pending = {"direction": orig_dir, "signal_idx": i}
                        watching = None
                elif i > watching["expire"]:
                    watching = None
            if watching is None and pending is None:
                p = oi_pctile[i]
                is_quiet_jump = (np.isfinite(p) and p >= cfg.jump_pctile and np.isfinite(r)
                                 and abs(r) < cfg.price_confirm_th)
                if is_quiet_jump:
                    watching = {"start": i, "expire": min(i + follow_window, n - 2)}

    return trades


def load_all_signals(symbols=common.SYMBOLS) -> dict[str, common.SymbolData]:
    return common.load_all(symbols)


def run_all(symbols_sig: dict[str, common.SymbolData], cfg: RunConfig
            ) -> dict[str, list[TradeRec]]:
    settings = get_settings()
    risk = RiskManager(settings)
    out = {}
    for sym, sd in symbols_sig.items():
        out[sym] = run_symbol(sym, sd, cfg, settings, risk)
    return out


def run_all_quiet(symbols_sig: dict[str, common.SymbolData], cfg: RunConfig,
                  follow_window: int = 3) -> dict[str, list[TradeRec]]:
    settings = get_settings()
    risk = RiskManager(settings)
    out = {}
    for sym, sd in symbols_sig.items():
        out[sym] = run_symbol_quiet_follow(sym, sd, cfg, settings, risk, follow_window)
    return out
