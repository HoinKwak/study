"""OI 변화 zero-crossing rate 확신도 게이트 + Donchian 브레이크아웃 — 백테스트 엔진.

신호(15m, zcr 게이트+Donchian 이탈) → 15m 진입/청산:
  - 15m 봉 i 종가 시점에: close(i) 가 직전 20봉(자기 제외) Donchian 상단/하단을 이탈
    AND zcr_pctile(i) <= 30(확신 게이트) AND 24봉(zcr_window) 롤링 순ΔOI 누적 방향이 이탈
    방향과 일치 → 방향 확정(모두 i 시점까지의 데이터만 사용, 룩어헤드 없음).
  - 체결: shift(1) — 신호 확정봉 i 의 "다음" 15m 봉(i+1) 시가에 진입.
  - SL 용 ATR(20,15m) 은 신호 확정봉(i)의 값을 사용(entry 봉 자신은 아직 모름 — lookahead 방지).
  - 청산:
      1) SL(고정, ATR(20,15m)×1.0, 신호봉 기준 대칭 배치) — 진입가 기준.
      2) TP 트레일링(ATR(1h,14)×1.5, 러닝 고가/저가 기준, 1h ATR 은 causal 매핑된 마지막 완결
         1h 봉 값).
      3) 24봉(6시간) 경과 시 시장가(봉 종가) 강제청산.
  - gate:
      zcr_lo  = 스펙 기본(zcr_pctile<=30 AND OI누적방향 일치)
      none    = 게이트 없는 순수 Donchian(20) 브레이크아웃(zcr·OI방향 조건 모두 제거,
                사전 폐기조건 (e)의 문언 그대로 "순수 Donchian 브레이크아웃 대조군")
      zcr_hi  = 게이트 반대방향(zcr_pctile>=70, 비확신 국면) — 방향 조건은 zcr_lo 와 동일
      volz_hi = 신호원 교체(zcr 대신 거래대금 z-score 상위 30%, 방향 조건 동일) — 결합확률/
                전제일관성 절의 "확신도 게이트가 사실상 거래량 급증 게이트" 의심 직접 검증
      reverse = zcr_lo 와 동일 모집단에서 최종 방향만 반전(SL/TP 는 진입가 기준 대칭 재배치,
                청산 로직은 최종 방향 변수 참조 — 절대레벨 재사용 버그 클래스 없음, ATR 기반이라
                방향 비대칭 없음)
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "OIZCR_REPO_SRC", "/home/user/study/.claude/worktrees/agent-afb4a326731d5754a/src"))

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
    gate: str                # zcr_lo|none|zcr_hi|volz_hi|reverse
    signal_idx: int           # 신호 확정 15m 인덱스(i)
    entry_idx: int             # 15m 진입 인덱스(i+1)
    entry_time: pd.Timestamp
    entry_price: float
    fixed_stop: float
    quantity: float
    risk_amount: float
    gate_pctile_at_signal: float
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
    zcr_pctile_th: float = common.ZCR_PCTILE_TH
    donchian_lb: int = common.DONCHIAN_LB
    atr_trail_mult: float = common.ATR_TRAIL_MULT
    atr_stop_mult: float = common.ATR_STOP_MULT
    max_hold_bars: int = common.MAX_HOLD_BARS
    gate: str = "zcr_lo"        # zcr_lo|none|zcr_hi|volz_hi|reverse
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

    o15 = df15m["open"].to_numpy(float)
    h15 = df15m["high"].to_numpy(float)
    l15 = df15m["low"].to_numpy(float)
    c15 = df15m["close"].to_numpy(float)

    donch_upper = sig.donch_upper.to_numpy(float)
    donch_lower = sig.donch_lower.to_numpy(float)
    atr20 = sig.atr20_15m.to_numpy(float)
    oi_cumsum = sig.oi_cumsum_window.to_numpy(float)

    if cfg.gate == "zcr_lo":
        gate_pctile = sig.zcr_pctile.to_numpy(float)
        gate_ok = gate_pctile <= cfg.zcr_pctile_th
        need_dir_confirm = True
    elif cfg.gate == "zcr_hi":
        gate_pctile = sig.zcr_pctile.to_numpy(float)
        gate_ok = gate_pctile >= (100.0 - cfg.zcr_pctile_th)
        need_dir_confirm = True
    elif cfg.gate == "volz_hi":
        gate_pctile = sig.vol_z_pctile.to_numpy(float)
        gate_ok = gate_pctile >= (100.0 - cfg.zcr_pctile_th)
        need_dir_confirm = True
    elif cfg.gate == "none":
        gate_pctile = sig.zcr_pctile.to_numpy(float)  # 기록용(게이트 미적용)
        gate_ok = np.ones(n15, dtype=bool)
        need_dir_confirm = False   # 사전 폐기조건 (e): "게이트 없는 순수 Donchian 브레이크아웃"
    elif cfg.gate == "reverse":
        gate_pctile = sig.zcr_pctile.to_numpy(float)
        gate_ok = gate_pctile <= cfg.zcr_pctile_th
        need_dir_confirm = True
    else:
        raise ValueError(cfg.gate)

    counts = _completed_1h_counts(df1h.index, df15m.index.asi8)
    atr14_1h = sig.atr14_1h.to_numpy(float)

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    lev = settings.leverage_for(symbol[:-4] + "/USDT")
    next_available_i = -1  # 동시 포지션 금지

    for i in range(1, n15 - 1):
        if i <= next_available_i:
            continue
        u, lo, c = donch_upper[i], donch_lower[i], c15[i]
        if not (np.isfinite(u) and np.isfinite(lo) and np.isfinite(c)):
            continue
        if not gate_ok[i]:
            continue
        long_break = c > u
        short_break = c < lo
        if not (long_break or short_break):
            continue
        if long_break and short_break:
            continue  # 극단적으로 좁은 채널 등 이상치 — 스킵

        raw_direction = "long" if long_break else "short"

        if need_dir_confirm:
            cs = oi_cumsum[i]
            if not np.isfinite(cs):
                continue
            if raw_direction == "long" and not (cs > 0):
                continue
            if raw_direction == "short" and not (cs < 0):
                continue

        direction = "short" if (cfg.gate == "reverse" and raw_direction == "long") else (
            "long" if (cfg.gate == "reverse" and raw_direction == "short") else raw_direction)

        entry_i = i + 1
        if entry_i >= n15 - 1:
            continue
        entry_raw = o15[entry_i]
        atr_v = atr20[i]  # 신호 확정봉(i) 까지의 ATR(20,15m) — entry_i 자신은 아직 모름
        if not (np.isfinite(atr_v) and atr_v > 0 and entry_raw > 0):
            continue

        cnt = counts[i]
        if cnt < 1:
            continue
        atr1h_v = atr14_1h[cnt - 1]
        if not (np.isfinite(atr1h_v) and atr1h_v > 0):
            continue

        sl_dist = cfg.atr_stop_mult * atr_v
        fill_px = _fill(entry_raw, direction, closing=False, fee_on=cfg.fee_on)
        if direction == "long":
            fixed_stop = fill_px - sl_dist
            dirn = Direction.LONG
        else:
            fixed_stop = fill_px + sl_dist
            dirn = Direction.SHORT

        # 반전 대조군 주의: 리스크 거리(sl_dist)는 방향 무관 ATR 로 1회 계산되고 진입가 기준
        # 대칭 재배치된다(방향성 조건으로 선택된 진입봉의 "그 방향 자연스러운 극값"을 스톱으로
        # 쓰지 않음 — ATR 은 방향 비대칭이 없는 값이라 이 함정에서 원천 안전). TP 트레일링도
        # running_extreme 을 최종 방향(is_long) 기준으로 매 봉 갱신하므로 절대레벨 재사용 버그
        # 클래스(donch_mid10 형)가 구조적으로 발생하지 않음(이 스펙엔 절대 레벨 청산이 없음).
        plan = risk.build_plan_with_stop(symbol, dirn, fill_px, fixed_stop, fill_px, equity,
                                         leverage=lev)
        if plan is None or plan.quantity <= 0:
            continue

        fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
        gpc = float(gate_pctile[i]) if np.isfinite(gate_pctile[i]) else float("nan")
        trade = TradeRec(symbol=symbol, direction=direction, gate=cfg.gate, signal_idx=i,
                         entry_idx=entry_i, entry_time=df15m.index[entry_i], entry_price=fill_px,
                         fixed_stop=fixed_stop, quantity=plan.quantity, risk_amount=plan.risk_amount,
                         gate_pctile_at_signal=gpc, fee_entry=fee0)
        equity -= fee0

        is_long = direction == "long"
        exit_i = None; exit_px = None; reason = ""
        running_extreme = entry_raw  # 러닝 고가(long)/저가(short), entry 봉 시가부터 시작(최종방향 기준)
        j = entry_i
        max_j = min(n15 - 1, entry_i + cfg.max_hold_bars + 2)
        while j <= max_j:
            holding = j - entry_i
            prev = j - 1
            # --- TP 트레일링(ATR(1h,14)×1.5) — causal, 봉 j 시가 시점까지 완결된 마지막 1h 봉 ---
            cnt_j = counts[j] if j < n15 else counts[-1]
            trail_level = np.nan
            if cnt_j >= 1:
                a1h = atr14_1h[cnt_j - 1]
                if np.isfinite(a1h) and a1h > 0:
                    if is_long:
                        trail_level = running_extreme - cfg.atr_trail_mult * a1h
                    else:
                        trail_level = running_extreme + cfg.atr_trail_mult * a1h

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

            h, l, cl = h15[j], l15[j], c15[j]
            hit = (l <= stop_level) if is_long else (h >= stop_level)
            if hit:
                exit_i = j; exit_px = stop_level; reason = "stop_combined"; break
            if holding >= cfg.max_hold_bars:
                exit_i = j; exit_px = cl; reason = "time_exit"; break

            running_extreme = max(running_extreme, h) if is_long else min(running_extreme, l)
            j += 1
        if exit_i is None:
            exit_i = max_j; exit_px = c15[max_j]; reason = "data_end"

        fill_exit = _fill(exit_px, direction, closing=True, fee_on=cfg.fee_on)
        fee1 = _fee(fill_exit * trade.quantity, cfg.fee_on)
        raw = ((fill_exit - trade.entry_price) if is_long
              else (trade.entry_price - fill_exit)) * trade.quantity
        # ⚠️진입수수료 반영(과거 두 라운드 연속 발견된 버그 — 진입 fee0 이 pnl 에서 누락되던 것을
        # 여기서는 애초에 raw - fee0 - fee1 로 계산해 방지).
        pnl = raw - trade.fee_entry - fee1
        trade.exit_idx = exit_i; trade.exit_time = df15m.index[exit_i]; trade.exit_price = fill_exit
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
