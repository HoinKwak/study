"""매수주도 vs 매도주도 Kyle's 람다 비대칭 — 백테스트 엔진.

⚠️**방향 사전검증 결과에 따른 설계 확정**(run_direction_precheck.py, 스펙이 명시적으로 요구한
1단계 검증): 스펙이 "잠정 가설"이라 명시한 원래 방향(gap_pctile>=80/λ_sell우위+매도스파이크→숏,
gap_pctile<=20/λ_buy우위+매수스파이크→롱, "추가 매도/매수 흐름이 방향을 지속시킨다"는 모멘텀
가설)은 게이트 없이 순수 트리거만으로 집계한 N봉(4/8/16봉) 순방향 지속률이 **7종목 전부, 3개
호라이즌 전부에서 45.1~47.8%로 50% 미달**(z=-5.2~-14.6, 풀링표본 기준 — 표본이 강하게 자기상관돼
있어 이 z 는 참고용이며 최종 판정은 별도 OOS 트레이드 단위 t 로 함)했다. 즉 "추가 매도 압력이
가격을 더 밀어낸다"가 아니라 "그 반대(되돌림/페이드)"가 실측상 더 빈번했다 — 스펙 원문의
"반대로 나오면 방향을 뒤집어 재검증"이라는 명시적 지침에 따라, **본 채택안(base)은 방향을 뒤집은
페이드(mean-reversion) 규칙**을 쓴다:
  - gap_pctile>=80(λ_sell 우위) AND 트리거 AND sv3<0(매도스파이크) → **롱**(매도 소진 후 반등 베팅)
  - gap_pctile<=20(λ_buy 우위) AND 트리거 AND sv3>0(매수스파이크) → **숏**(매수 소진 후 되돌림 베팅)
스펙이 원래 문언 그대로 가정한 모멘텀 방향은 `hypothesis_orig` 게이트로 별도 보존해 대조군으로
돌린다(사실상 스펙의 "핵심 대조군③ λ_gap 부호를 반대로 쓴 버전"과 동일한 실험).

게이트 종류:
  base            = 위에서 확정한 페이드 방향(채택안)
  hypothesis_orig = 스펙 원문 그대로의 모멘텀 방향(사전검증에서 기각된 가설, 대조군③과 동일 효과)
  reverse         = base 의 최종 방향만 반전(SL/TP 진입가 대칭 재배치, 청산조건도 최종방향 참조)
  taker_z         = 대조군②: 게이트를 λ_gap 대신 taker_buy_ratio 자체의 lambda_window 롤링평균
                    백분위(ratio_mean_pctile)로 교체, 방향 로직은 base 와 동일(페이드)
  symlambda       = 대조군①: 매수/매도 미분리 대칭 λ(lambda_all_pctile) 게이트 — 딥마켓(<=30%tile)
                    +트리거 시 sv3 부호 방향 모멘텀(추세추종), 씬마켓(>=70%tile)+트리거 시 sv3
                    반대 방향(역추세) — 기존 kyle-lambda-price-impact-regime-scalp.md 의 딥/씬마켓
                    로직을 동일 엔진(트리거·청산)에서 재현
  none            = 게이트 완전 제거(트리거+sv3 부호만으로 페이드 방향 베팅) — 게이트 자체의
                    부가가치 확인용 보조 대조군
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "KLBSA_REPO_SRC", "/home/user/study/.claude/worktrees/agent-a21f5cf039b647cd0/src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE


@dataclass
class TradeRec:
    symbol: str
    direction: str          # "long"/"short"(최종 체결 방향)
    gate: str
    signal_idx: int
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    fixed_stop: float
    quantity: float
    risk_amount: float
    gap_pctile_at_signal: float
    fee_entry: float = 0.0
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    fee_exit: float = 0.0
    pnl: float = 0.0
    r_multiple: float = 0.0
    reason: str = ""
    holding_bars: int = 0


def _fill(price: float, direction: str, closing: bool, fee_on: bool) -> float:
    if not fee_on:
        return price
    adverse = 1 if (direction == "long") != closing else -1
    return price * (1 + adverse * SLIPPAGE)


def _fee(notional: float, fee_on: bool) -> float:
    if not fee_on:
        return 0.0
    return abs(notional) * TAKER_FEE


@dataclass
class RunConfig:
    gap_hi_pctile: float = common.GAP_HI_PCTILE
    gap_lo_pctile: float = common.GAP_LO_PCTILE
    sv_trigger_pctile: float = common.SV_TRIGGER_PCTILE
    atr_trail_mult: float = common.ATR_TRAIL_MULT
    atr_stop_mult: float = common.ATR_STOP_MULT
    max_hold_bars: int = common.MAX_HOLD_BARS
    gate: str = "base"      # base|hypothesis_orig|reverse|taker_z|symlambda|none
    fee_on: bool = True
    starting_equity: float = 10_000.0


def _raw_direction_for_bar(i: int, cfg: RunConfig, gap_p: np.ndarray, ratio_p: np.ndarray,
                          lamall_p: np.ndarray, trig_p: np.ndarray, sv3: np.ndarray,
                          gate: str) -> str | None:
    trig = trig_p[i] > cfg.sv_trigger_pctile
    if not (np.isfinite(trig_p[i]) and trig):
        return None
    s = sv3[i]
    if not np.isfinite(s) or s == 0:
        return None

    if gate in ("base", "reverse"):
        g = gap_p[i]
        if not np.isfinite(g):
            return None
        if g >= cfg.gap_hi_pctile and s < 0:
            d = "long"
        elif g <= cfg.gap_lo_pctile and s > 0:
            d = "short"
        else:
            return None
        if gate == "reverse":
            d = "short" if d == "long" else "long"
        return d

    if gate == "hypothesis_orig":
        g = gap_p[i]
        if not np.isfinite(g):
            return None
        if g >= cfg.gap_hi_pctile and s < 0:
            return "short"
        if g <= cfg.gap_lo_pctile and s > 0:
            return "long"
        return None

    if gate == "taker_z":
        r = ratio_p[i]
        if not np.isfinite(r):
            return None
        # base 와 동일한 "페이드" 방향 로직, 게이트원만 λ_gap→taker_buy_ratio 레벨 백분위로 교체.
        # 지속적 매수우위(r 높음)+매수스파이크 → 숏(페이드), 지속적 매도우위(r 낮음)+매도스파이크 → 롱.
        if r >= cfg.gap_hi_pctile and s > 0:
            return "short"
        if r <= cfg.gap_lo_pctile and s < 0:
            return "long"
        return None

    if gate == "symlambda":
        la = lamall_p[i]
        if not np.isfinite(la):
            return None
        if la <= 30.0:      # 딥마켓 → 추세추종(sv3 방향)
            return "long" if s > 0 else "short"
        if la >= 70.0:       # 씬마켓 → 역추세(sv3 반대방향)
            return "short" if s > 0 else "long"
        return None

    if gate == "none":
        # 게이트 완전제거: base 와 동일한 페이드 방향이나 gap_pctile 조건 없이 트리거+sv3 부호만.
        return "long" if s < 0 else "short"

    raise ValueError(gate)


def run_symbol(symbol: str, sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager
               ) -> list[TradeRec]:
    df = sig.df15m
    n = len(df)
    o = df["open"].to_numpy(float)
    h = df["high"].to_numpy(float)
    lo_ = df["low"].to_numpy(float)
    c = df["close"].to_numpy(float)
    atr14 = sig.atr14.to_numpy(float)

    gap_p = sig.gap_pctile.to_numpy(float)
    ratio_p = sig.ratio_mean_pctile.to_numpy(float)
    lamall_p = sig.lambda_all_pctile.to_numpy(float)
    trig_p = sig.sv3_abs_pctile.to_numpy(float)
    sv3 = sig.sv3.to_numpy(float)

    # 게이트별 조건청산에 쓸 "그 게이트를 정의하는 백분위 시계열"과 hi/lo 임계값
    # (스펙의 "gap_pctile 이 게이트 임계 안쪽으로 되돌아오면 즉시청산"을 대조군에도 구조적으로
    # 동일하게 적용 — 대조군마다 청산 메커니즘이 달라지면 빈도·성과 차이가 게이트 품질이 아닌
    # 청산구조 차이에서 올 수 있어 공정성을 위해 통일).
    if cfg.gate in ("base", "reverse", "hypothesis_orig"):
        gate_series = gap_p
        gate_hi, gate_lo = cfg.gap_hi_pctile, cfg.gap_lo_pctile
    elif cfg.gate == "taker_z":
        gate_series = ratio_p
        gate_hi, gate_lo = cfg.gap_hi_pctile, cfg.gap_lo_pctile
    elif cfg.gate == "symlambda":
        gate_series = lamall_p
        gate_hi, gate_lo = 70.0, 30.0
    else:  # none — 게이트 자체가 없어 조건청산 미적용
        gate_series = np.full(n, np.nan)
        gate_hi, gate_lo = float("inf"), float("-inf")

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    lev = settings.leverage_for(symbol[:-4] + "/USDT")
    next_available_i = -1  # 동시 포지션 금지

    for i in range(1, n - 1):
        if i <= next_available_i:
            continue
        direction = _raw_direction_for_bar(i, cfg, gap_p, ratio_p, lamall_p, trig_p, sv3, cfg.gate)
        if direction is None:
            continue

        entry_i = i + 1
        if entry_i >= n - 1:
            continue
        entry_raw = o[entry_i]
        atr_v = atr14[i]  # 신호 확정봉(i) 까지의 ATR(14,15m) — entry_i 자신은 아직 모름(룩어헤드 방지)
        if not (np.isfinite(atr_v) and atr_v > 0 and entry_raw > 0):
            continue

        sl_dist = cfg.atr_stop_mult * atr_v
        fill_px = _fill(entry_raw, direction, closing=False, fee_on=cfg.fee_on)
        if direction == "long":
            fixed_stop = fill_px - sl_dist
            dirn = Direction.LONG
        else:
            fixed_stop = fill_px + sl_dist
            dirn = Direction.SHORT

        # ⚠️반전 대조군 주의: sl_dist(리스크거리)는 방향과 무관한 ATR(14,15m) 로 1회 계산돼 진입가
        # 기준 대칭 재배치된다(방향성 조건으로 선택된 진입봉의 "그 방향 자연스러운 극값"을 스톱으로
        # 재사용하지 않음 — ATR 은 방향 비대칭이 없어 이 함정에서 원천 안전).
        plan = risk.build_plan_with_stop(symbol, dirn, fill_px, fixed_stop, fill_px, equity,
                                         leverage=lev)
        if plan is None or plan.quantity <= 0:
            continue

        fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
        gate_val_i = gate_series[i]
        gp = float(gate_val_i) if np.isfinite(gate_val_i) else float("nan")
        trade = TradeRec(symbol=symbol, direction=direction, gate=cfg.gate, signal_idx=i,
                         entry_idx=entry_i, entry_time=df.index[entry_i], entry_price=fill_px,
                         fixed_stop=fixed_stop, quantity=plan.quantity, risk_amount=plan.risk_amount,
                         gap_pctile_at_signal=gp, fee_entry=fee0)
        equity -= fee0

        is_long = direction == "long"
        exit_i = None; exit_px = None; reason = ""
        running_extreme = entry_raw  # 러닝 고가(long)/저가(short), entry 봉 시가부터 시작(최종방향 기준)
        j = entry_i
        max_j = min(n - 1, entry_i + cfg.max_hold_bars + 2)
        while j <= max_j:
            holding = j - entry_i
            prev = j - 1
            # --- TP 트레일링(ATR(14,15m)×1.8) — causal, 직전 완결봉(prev)의 ATR 사용 ---
            trail_level = np.nan
            a_prev = atr14[prev]
            if np.isfinite(a_prev) and a_prev > 0:
                if is_long:
                    trail_level = running_extreme - cfg.atr_trail_mult * a_prev
                else:
                    trail_level = running_extreme + cfg.atr_trail_mult * a_prev

            if is_long:
                levels = [trade.fixed_stop]
                if np.isfinite(trail_level):
                    levels.append(trail_level)
                stop_level = max(levels)
            else:
                levels = [trade.fixed_stop]
                if np.isfinite(trail_level):
                    levels.append(trail_level)
                stop_level = min(levels)

            hh, ll, cl = h[j], lo_[j], c[j]
            hit = (ll <= stop_level) if is_long else (hh >= stop_level)
            if hit:
                exit_i = j; exit_px = stop_level; reason = "stop_combined"; break

            # --- 조건청산: 게이트 백분위가 임계 안쪽으로 되돌아오면(비대칭 소멸) 즉시청산 ---
            # (게이트를 정의하는 백분위 시계열·임계값을 위에서 gate_series/gate_hi/gate_lo 로
            # 통일해 base 뿐 아니라 모든 게이트 대조군에 동일 메커니즘을 구조적으로 적용한다.
            # "none" 은 gate_hi=+inf/gate_lo=-inf 라 이 분기가 항상 거짓 → 조건청산 미적용.)
            gj = gate_series[j]
            undefined = not np.isfinite(gj)
            was_hi = trade.gap_pctile_at_signal >= gate_hi
            was_lo = trade.gap_pctile_at_signal <= gate_lo
            exited_gate = ((was_hi or was_lo) and undefined) or (
                was_hi and gj < gate_hi) or (was_lo and gj > gate_lo)
            if (was_hi or was_lo) and exited_gate and holding >= 1:
                exit_i = j; exit_px = cl; reason = "gate_dissipate"; break

            if holding >= cfg.max_hold_bars:
                exit_i = j; exit_px = cl; reason = "time_exit"; break

            running_extreme = max(running_extreme, hh) if is_long else min(running_extreme, ll)
            j += 1
        if exit_i is None:
            exit_i = max_j; exit_px = c[max_j]; reason = "data_end"

        fill_exit = _fill(exit_px, direction, closing=True, fee_on=cfg.fee_on)
        fee1 = _fee(fill_exit * trade.quantity, cfg.fee_on)
        raw = ((fill_exit - trade.entry_price) if is_long
              else (trade.entry_price - fill_exit)) * trade.quantity
        pnl = raw - trade.fee_entry - fee1
        trade.exit_idx = exit_i; trade.exit_time = df.index[exit_i]; trade.exit_price = fill_exit
        trade.pnl = pnl; trade.fee_exit = fee1; trade.reason = reason
        trade.holding_bars = exit_i - entry_i
        trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
        equity += pnl
        trades.append(trade)
        next_available_i = exit_i

    return trades


def load_all_signals(symbols=common.SYMBOLS) -> dict[str, common.Signals]:
    out = {}
    for s in symbols:
        sig = common.build_signals(s)
        if sig is not None:
            out[s] = sig
    return out


def run_all(symbols_sig: dict[str, common.Signals], cfg: RunConfig
           ) -> dict[str, list[TradeRec]]:
    settings = get_settings()
    risk = RiskManager(settings)
    out = {}
    for sym, sig in symbols_sig.items():
        out[sym] = run_symbol(sym, sig, cfg, settings, risk)
    return out
