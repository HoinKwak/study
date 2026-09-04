"""OI AR(1) φ 레짐 게이트 + Donchian 브레이크아웃 스캘프 — 백테스트 엔진.

신호(15m, φ 게이트+Donchian 이탈) → 15m 진입/청산:
  - 15m 봉 i 의 종가 시점에: close(i) 가 직전 20봉(자기 제외) Donchian 상단/하단을 이탈
    AND φ_pctile(i) >= 0.67(고지속성 레짐) → 방향 확정(모두 i 시점까지의 데이터만 사용, 룩어헤드
    없음). φ(i) 는 i 시점까지의 oi_growth 로 추정된 회귀계수이므로 causal.
  - 1h 확인: 신호 확정 시점(i 의 종가)까지 "완결된" 마지막 1h 봉의 EMA20 4h 기울기를 ATR(1h)로
    정규화해, 진입 방향과 뚜렷이 반대(|정규화 기울기| >= ema_slope_th, 부호 반대)면 스킵.
  - 체결: shift(1) — 신호 확정봉 i 의 "다음" 15m 봉(i+1) 시가에 진입.
  - ATR(14,15m) 은 신호 확정봉(i, entry_i-1)의 값을 사용(entry 봉 자신은 아직 모름 — lookahead 방지).
  - 청산(매 봉 시가 이후 판정, 동시발생 시 보수적으로 SL/트레일/중간선 통합 스톱 우선):
      1) SL(고정, ATR14×1.2)·트레일(ATR14×1.8, 러닝 고가/저가 기준)·Donchian 중간선(10봉) 재이탈
         셋을 "가장 가까운(타이트한) 보호선" 하나로 합성 — 봉의 저가/고가가 이 합성선을 건드리면
         그 가격에 청산(트레일·중간선은 모두 직전 완결봉까지의 정보로만 갱신 — causal).
      2) 보유 24봉(15m×24=6h) 경과 시 봉 종가 강제청산.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "OIAR1_REPO_SRC", "/home/user/study/.claude/worktrees/agent-a8f695a5d23809096/src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE
NS_1H = np.timedelta64(1, "h").astype("timedelta64[ns]").astype("int64")


@dataclass
class TradeRec:
    symbol: str
    direction: str          # "long"/"short"
    gate: str                # "phi_hi"(스펙 기본) | "none"(게이트 없음①) | "oiz_hi"(대조②)
                              # | "phi_lo"(대조③) | "reverse"(방향반전④)
    signal_idx: int           # 신호 확정 15m 인덱스(i)
    entry_idx: int             # 15m 진입 인덱스(i+1)
    entry_time: pd.Timestamp
    entry_price: float
    fixed_stop: float
    quantity: float
    risk_amount: float
    phi_pctile_at_signal: float
    fees: float = 0.0
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
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
    phi_pctile_th: float = common.PHI_PCTILE_TH
    donchian_lb: int = common.DONCHIAN_LB
    atr_trail_mult: float = common.ATR_TRAIL_MULT
    atr_stop_mult: float = common.ATR_STOP_MULT
    max_hold_bars: int = common.MAX_HOLD_BARS
    ema_slope_th: float = 0.5    # 1h EMA20 4h기울기/ATR(1h) 정규화 임계(뚜렷한 반대 판정)
    use_ema_confirm: bool = True
    gate: str = "phi_hi"        # phi_hi|none|oiz_hi|phi_lo|reverse
    fee_on: bool = True
    starting_equity: float = 10_000.0


def _completed_1h_counts(df1h_index: pd.DatetimeIndex, ts15_ns: np.ndarray) -> np.ndarray:
    """15m 타임스탬프(ns) 각각에 대해 '그 시각까지 완결된 1h 봉 개수'(searchsorted 패턴,
    기존 다수 리포에서 검증된 causal 매핑)."""
    ends = df1h_index.asi8 + NS_1H
    return np.searchsorted(ends, ts15_ns, side="right")


def run_symbol(symbol: str, sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager
               ) -> list[TradeRec]:
    df1h = sig.df1h
    df15m = sig.df15m
    n15 = len(df15m)

    close = df15m["close"].to_numpy(float)
    o15 = df15m["open"].to_numpy(float)
    h15 = df15m["high"].to_numpy(float)
    l15 = df15m["low"].to_numpy(float)
    c15 = df15m["close"].to_numpy(float)

    donch_upper = sig.donch_upper.to_numpy(float)
    donch_lower = sig.donch_lower.to_numpy(float)
    donch_mid10 = sig.donch_mid10.to_numpy(float)
    atr15 = sig.atr14_15m.to_numpy(float)

    if cfg.gate == "phi_hi":
        gate_pctile = sig.phi_pctile.to_numpy(float)
        gate_ok = gate_pctile >= cfg.phi_pctile_th
    elif cfg.gate == "phi_lo":
        gate_pctile = sig.phi_pctile.to_numpy(float)
        gate_ok = gate_pctile <= (1.0 - cfg.phi_pctile_th)
    elif cfg.gate == "oiz_hi":
        gate_pctile = sig.oi_z_pctile.to_numpy(float)
        gate_ok = gate_pctile >= cfg.phi_pctile_th
    elif cfg.gate == "none":
        gate_pctile = sig.phi_pctile.to_numpy(float)  # 기록용(게이트 미적용, phi_hi와 동일 값 기록)
        gate_ok = np.ones(n15, dtype=bool)
    elif cfg.gate in ("reverse", "reverse_nomid"):
        # 방향반전 대조군: "같은 φ 게이트가 통과시킨 신호 모집단"에서 방향만 뒤집는다(모집단이
        # 다르면 비교가 불공정 — none 대조군과는 다른 목적이므로 phi_hi 와 동일 게이트 적용).
        gate_pctile = sig.phi_pctile.to_numpy(float)
        gate_ok = gate_pctile >= cfg.phi_pctile_th
    else:
        raise ValueError(cfg.gate)
    # 워밍업 구간(φ_pctile NaN) 은 gate_ok 에서 자동 배제(비교 시 NaN>=th → False)해도, "none"
    # 대조군은 gate_ok 를 강제 True 로 뒀으므로 phi 워밍업과 무관하게 발화 가능 — 이는 의도된 설계
    # (게이트 없는 순수 Donchian 대조군은 phi 계산 여부와 무관해야 공정한 대조).

    # EMA20(1h) 4h 기울기, ATR(1h) 정규화(causal — 마지막 완결 1h 봉 기준)
    ema20_1h = sig.ema20_1h.to_numpy(float)
    atr14_1h = sig.atr14_1h.to_numpy(float)
    slope_1h = ema20_1h - np.roll(ema20_1h, 4)
    slope_1h[:4] = np.nan
    slope_norm_1h = slope_1h / atr14_1h
    slope_norm_1h = np.where(np.isfinite(atr14_1h) & (atr14_1h > 0), slope_norm_1h, np.nan)

    counts = _completed_1h_counts(df1h.index, df15m.index.asi8)

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    lev = settings.leverage_for(symbol[:-4] + "/USDT")
    next_available_i = -1  # 동시 포지션 금지

    for i in range(1, n15 - 1):
        if i <= next_available_i:
            continue
        u, lo, mid = donch_upper[i], donch_lower[i], donch_mid10[i]
        c = close[i]
        if not (np.isfinite(u) and np.isfinite(lo) and np.isfinite(c)):
            continue
        if not gate_ok[i]:
            continue
        long_break = c > u
        short_break = c < lo
        if not (long_break or short_break):
            continue
        if long_break and short_break:
            continue  # 극단적으로 좁은 채널 등 이상치 — 스킵(둘 다 참인 경우는 사실상 없음)

        raw_direction = "long" if long_break else "short"
        if cfg.gate in ("reverse", "reverse_nomid"):
            direction = "short" if raw_direction == "long" else "long"
        else:
            direction = raw_direction

        # 1h EMA 기울기 확인(원신호 방향raw_direction 기준으로 필터 — 반전 대조군도 "필터 자체"는
        # 원신호를 기준으로 적용한 뒤 최종 진입 방향만 뒤집는다. 필터가 없으면 반전군의 母표본이
        # 달라져 비교가 불공정해짐).
        if cfg.use_ema_confirm:
            cnt = counts[i]
            if cnt < 1:
                continue
            sn = slope_norm_1h[cnt - 1]
            if np.isfinite(sn):
                if raw_direction == "long" and sn < -cfg.ema_slope_th:
                    continue
                if raw_direction == "short" and sn > cfg.ema_slope_th:
                    continue

        entry_i = i + 1
        if entry_i >= n15 - 1:
            continue
        entry_raw = o15[entry_i]
        atr_v = atr15[i]  # 신호 확정봉(i) 까지의 ATR — entry_i 자신은 아직 모름(lookahead 방지)
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

        # 반전 대조군 주의사항: 리스크 거리(sl_dist)는 방향 무관 원신호 ATR 로 1회만 계산되고
        # 진입가 기준 대칭 재배치된다(방향성 조건으로 선택된 진입봉 자체의 "그 방향 자연스러운
        # 극값"을 스톱으로 쓰지 않음 — ATR 은 방향 비대칭이 없는 값이라 이 함정에서 원천 안전).
        plan = risk.build_plan_with_stop(symbol, dirn, fill_px, fixed_stop, fill_px, equity,
                                         leverage=lev)
        if plan is None or plan.quantity <= 0:
            continue

        # ⚠️자체발견·수정 버그: Donchian 중간선(10봉) 재이탈 청산은 raw_direction(브레이크아웃
        # 방향)에 종속된 절대 가격 레벨이다 — 상향 이탈이면 mid_level 이 항상 진입가보다 아래에
        # 위치(이탈 직전 10봉의 중간값이므로 구조적으로 그렇다). "reverse" 대조군에서 방향만
        # is_long=False 로 뒤집고 이 절대레벨(donch_mid10[j])을 그대로 재사용하면, 숏 포지션의
        # 보호선(위쪽에 있어야 함)에 진입가보다 훨씬 아래인 값이 선택돼(min 연산이 mid_level 을
        # 고름) 진입 즉시(j=entry_i) 고가가 그 레벨을 상회해 "손절"이 발화 — 그런데 숏 pnl 계산상
        # 그 낮은 가격에 "청산"한 것으로 기록되어 오히려 거대한 가짜 이익이 찍힌다(1차 실행 실측:
        # zero_hold_frac(OOS)=99.97%, PF(R)=1377 — 과거 라운드에서 반복 확인된 "반전 대조군이
        # 원래 방향의 절대 레벨을 재사용해 zero_hold_frac 100%" 버그 클래스와 동일 패턴).
        # 수정: 중간선 보호선은 방향 무관 ATR SL 과 마찬가지로 "신호 확정 시점(i)의 거리를 1회
        # 계산해 진입가 기준 대칭 재배치"한다(원신호 방향 기준으로 1회 계산 — 원칙 그대로 적용).
        mid_at_signal = donch_mid10[i] if np.isfinite(donch_mid10[i]) else np.nan
        mid_dist_fixed = (abs(entry_raw - mid_at_signal)
                          if np.isfinite(mid_at_signal) else np.nan)

        fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
        gpc = float(gate_pctile[i]) if np.isfinite(gate_pctile[i]) else float("nan")
        trade = TradeRec(symbol=symbol, direction=direction, gate=cfg.gate, signal_idx=i,
                         entry_idx=entry_i, entry_time=df15m.index[entry_i], entry_price=fill_px,
                         fixed_stop=fixed_stop, quantity=plan.quantity, risk_amount=plan.risk_amount,
                         phi_pctile_at_signal=gpc, fees=fee0)
        equity -= fee0

        is_long = direction == "long"
        exit_i = None; exit_px = None; reason = ""
        running_extreme = entry_raw  # 러닝 고가(long)/저가(short), entry 봉 시가부터 시작
        j = entry_i
        max_j = min(n15 - 1, entry_i + cfg.max_hold_bars + 2)
        while j <= max_j:
            holding = j - entry_i
            # --- 봉 j 시가 시점까지 알려진 정보로 스톱 레벨 계산(직전 완결봉 j-1 기준, causal) ---
            prev = j - 1
            atr_prev = atr15[prev] if prev >= 0 else np.nan
            trail_level = np.nan
            if np.isfinite(atr_prev) and atr_prev > 0:
                if is_long:
                    trail_level = running_extreme - cfg.atr_trail_mult * atr_prev
                else:
                    trail_level = running_extreme + cfg.atr_trail_mult * atr_prev
            if cfg.gate == "reverse":
                # 대칭 재배치(위 주석 참조) — 신호시점 거리를 고정폭으로 진입가 기준 재배치.
                if np.isfinite(mid_dist_fixed):
                    mid_level = (fill_px - mid_dist_fixed) if is_long else (fill_px + mid_dist_fixed)
                else:
                    mid_level = np.nan
            elif cfg.gate == "reverse_nomid":
                # 제3의 대안(구조적 아티팩트 완전 배제): 중간선 청산 자체를 비활성화.
                mid_level = np.nan
            else:
                mid_level = donch_mid10[j] if j < n15 else np.nan

            if is_long:
                levels = [trade.fixed_stop]
                if np.isfinite(trail_level):
                    levels.append(trail_level)
                if np.isfinite(mid_level):
                    levels.append(mid_level)
                stop_level = max(levels)
            else:
                levels = [trade.fixed_stop]
                if np.isfinite(trail_level):
                    levels.append(trail_level)
                if np.isfinite(mid_level):
                    levels.append(mid_level)
                stop_level = min(levels)

            h, l, cl = h15[j], l15[j], c15[j]
            hit = (l <= stop_level) if is_long else (h >= stop_level)
            if hit:
                exit_i = j; exit_px = stop_level; reason = "stop_combined"; break
            if holding >= cfg.max_hold_bars:
                exit_i = j; exit_px = cl; reason = "time_exit"; break

            # 봉 j 종가까지 반영해 러닝 극값 갱신(다음 반복의 트레일 계산에 사용, causal — 봉 j
            # 자신의 스톱 판정에는 쓰지 않고 다음 봉 판정부터 반영됨)
            running_extreme = max(running_extreme, h) if is_long else min(running_extreme, l)
            j += 1
        if exit_i is None:
            exit_i = max_j; exit_px = c15[max_j]; reason = "data_end"

        fill_exit = _fill(exit_px, direction, closing=True, fee_on=cfg.fee_on)
        fee1 = _fee(fill_exit * trade.quantity, cfg.fee_on)
        raw = ((fill_exit - trade.entry_price) if is_long
              else (trade.entry_price - fill_exit)) * trade.quantity
        pnl = raw - fee1
        trade.exit_idx = exit_i; trade.exit_time = df15m.index[exit_i]; trade.exit_price = fill_exit
        trade.pnl = pnl; trade.fees += fee1; trade.reason = reason
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
