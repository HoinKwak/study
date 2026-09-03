"""대조군: `ibs-internal-bar-strength-mean-reversion-swing.md` 스펙을 **문자 그대로** 15m TF에
구현한 단일TF 평균회귀 엔진. CLV(=IBS)가 낮으면(<0.2) 롱(반등 기대), 높으면(>0.8) 숏(되돌림 기대)
— 본 스펙(멀티TF 정렬 추세추종, CLV 높으면 롱)과 **방향 정의 자체가 반대**라 두 전략의 트레이드
집합은 진입 임계값(0.75 vs 0.2)이 겹치지 않으므로 구조적으로 거의 중복되지 않는다(교집합률로 실측
확인). 원 스펙은 일봉(1d) 기준이라 max_hold_bars=8(일)을 15m TF에 그대로 옮기면 2시간에 불과해
원 연구의 '수 거래일 보유' 의도와 다르다는 점을 리포트에 명시 — 여기서는 **본 연구와 동일 TF(15m)에서
비교 가능하도록** 그대로 적용한다(스펙 파라미터 그대로, SMA200 추세필터는 옵션이라 기본 OFF).
청산 우선순위: SL > IBS 반대극단 회귀 청산 > 시간청산(트레일링 없음, 원 스펙 그대로).
전 성과 R-배수(risk_dist=sl_atr_mult×ATR15) 계산."""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
from crypto_trader.signals import indicators as ind  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE


@dataclass
class IbsConfig:
    ibs_buy: float = 0.2
    ibs_sell: float = 0.8
    ibs_exit_long: float = 0.6
    ibs_exit_short: float = 0.4
    sl_atr_mult: float = 2.0
    max_hold_bars: int = 8
    cost_on: bool = True
    direction_mode: str = "normal"


@dataclass
class IbsSignals:
    h15: pd.DataFrame
    ibs: np.ndarray
    atr15: np.ndarray


def build_signals(symbol: str) -> IbsSignals | None:
    h15 = common.load_klines(symbol, "15m")
    if h15.empty:
        return None
    ibs = common.clv(h15).to_numpy(float)
    atr15 = ind.atr(h15, 14).to_numpy(float)
    return IbsSignals(h15=h15, ibs=ibs, atr15=atr15)


@dataclass
class TradeRec:
    symbol: str
    direction: str
    orig_direction: str
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    stop_price: float
    risk_dist: float
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    reason: str = ""
    holding_bars: int = 0
    r_gross: float = 0.0
    r_net: float = 0.0


def _fill(price: float, direction: str, closing: bool, apply_slip: bool) -> float:
    if not apply_slip:
        return price
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * SLIPPAGE)


def run_symbol(symbol: str, sig: IbsSignals, cfg: IbsConfig) -> list[TradeRec]:
    h15 = sig.h15
    n = len(h15)
    open_ = h15["open"].to_numpy(float)
    high = h15["high"].to_numpy(float)
    low = h15["low"].to_numpy(float)
    close = h15["close"].to_numpy(float)
    idx = h15.index

    trades: list[TradeRec] = []
    trade: TradeRec | None = None
    pending: dict | None = None

    for i in range(n):
        if pending is not None and trade is None:
            direction = pending["direction"]
            fill_px = _fill(open_[i], direction, closing=False, apply_slip=cfg.cost_on)
            risk_dist = pending["risk_dist"]
            if risk_dist > 0 and np.isfinite(risk_dist) and fill_px > 0:
                stop_price = fill_px - risk_dist if direction == "long" else fill_px + risk_dist
                trade = TradeRec(symbol=symbol, direction=direction,
                                 orig_direction=pending["orig_direction"],
                                 entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                 stop_price=stop_price, risk_dist=risk_dist)
            pending = None

        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            is_long = trade.direction == "long"
            exit_px = None
            reason = ""
            if is_long and l <= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"
            elif (not is_long) and h >= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"
            if exit_px is None:
                ibsv = sig.ibs[i]
                if np.isfinite(ibsv):
                    # 원신호 방향 기준 반대극단 회귀(IBS 정의상 SL/트레일링이 아닌 '평균회귀 완료'
                    # 익절조건 — 원 스펙이 그대로 방향(direction)을 참조하는 로직이라 리버스에서도
                    # 대칭으로 뒤집는다: 리버스=최종방향 기준 사용(원 스펙 로직 자체가 이미 이 정의).
                    if trade.direction == "long" and ibsv >= cfg.ibs_exit_long:
                        exit_px, reason = c, "ibs_revert"
                    elif trade.direction == "short" and ibsv <= cfg.ibs_exit_short:
                        exit_px, reason = c, "ibs_revert"
            if exit_px is None and (i - trade.entry_idx) >= cfg.max_hold_bars:
                exit_px, reason = c, "time_exit"

            if exit_px is not None:
                fill_px = _fill(exit_px, trade.direction, closing=True, apply_slip=cfg.cost_on)
                dirn = 1.0 if is_long else -1.0
                raw = dirn * (fill_px - trade.entry_price)
                r_gross = raw / trade.risk_dist
                fee_cost = TAKER_FEE * (trade.entry_price + fill_px) if cfg.cost_on else 0.0
                r_net = (raw - fee_cost) / trade.risk_dist
                trade.exit_idx = i; trade.exit_time = idx[i]; trade.exit_price = fill_px
                trade.reason = reason; trade.holding_bars = i - trade.entry_idx
                trade.r_gross = r_gross; trade.r_net = r_net
                trades.append(trade)
                trade = None

        if trade is None and pending is None and i + 1 < n:
            ibsv = sig.ibs[i]
            orig_dir = None
            if np.isfinite(ibsv):
                if ibsv < cfg.ibs_buy:
                    orig_dir = "long"
                elif ibsv > cfg.ibs_sell:
                    orig_dir = "short"
            if orig_dir is not None:
                exec_dir = orig_dir
                if cfg.direction_mode == "reverse":
                    exec_dir = "short" if orig_dir == "long" else "long"
                risk_dist = sig.atr15[i] * cfg.sl_atr_mult if np.isfinite(sig.atr15[i]) else np.nan
                if np.isfinite(risk_dist) and risk_dist > 0:
                    pending = {"direction": exec_dir, "orig_direction": orig_dir,
                              "risk_dist": risk_dist}

    return trades


def load_all_signals(symbols=common.SYMBOLS) -> dict[str, IbsSignals]:
    out = {}
    for s in symbols:
        sig = build_signals(s)
        if sig is not None:
            out[s] = sig
    return out
