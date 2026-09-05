"""AR 유동성 레짐 + 모멘텀/평균회귀 전환 스캘프 — 백테스트 엔진.

신호(1h, AR 게이트+모멘텀버스트/볼린저이탈) → 15m 확인+체결:
  - 1h 봉 i의 종가 시점(T=index[i]+1h)에 트리거 확정:
      모멘텀(M): 직전 BURST_LOOKBACK봉 누적 가격변화 >= burst_mult*ATR14(1h,i)(롱) 또는
                 <= -burst_mult*ATR14(1h,i)(숏). 게이트: ar_pctile[i] <= 0.20(cfg.gate='ar')
      평균회귀(R): 1h 종가가 볼린저(20,2.0) 상단 초과(숏 페이드) 또는 하단 미만(롱 페이드).
                 게이트: ar_pctile[i] >= 0.80(cfg.gate='ar')
    모두 i 시점까지의 데이터만 사용(룩어헤드 없음). ATR14(1h,i)·볼린저(1h,i)·ar_pctile[i] 전부
    causal(rolling().rank(pct=True)은 윈도우 마지막 값의 순위 — i시점까지의 히스토리만 사용).
  - 15m 확인: T 이후 첫 완결 15m봉(k, open_time>=T)이 신호 방향으로 마감해야 확정:
      모멘텀: close[k]>open[k](롱) / close[k]<open[k](숏)
      평균회귀: close[k]>bb_lower[i](롱 페이드, 밴드 안으로 복귀) / close[k]<bb_upper[i](숏 페이드)
    확인 실패 시 그 1h 신호는 폐기(재시도 없음 — 단일 확인봉 원칙, 스캔형 룩어헤드 회피).
  - 체결: k+1 15m봉 시가(shift(1) 원칙).
  - ATR(14,15m)은 확인봉(k)까지의 값 사용(entry봉(k+1) 자신은 아직 모름 — lookahead 방지).
  - 청산(매 봉 시가 이후 판정):
      1) SL(고정, ATR14(15m)×stop_mult)·트레일(ATR14(15m)×trail_mult, 러닝 고가/저가 기준) 중
         가장 타이트한 보호선.
      2) 레짐 무효화("테제 무효화"류 — 최종방향 참조 원칙의 예외 후보, cfg.invalidation_exit로
         온오프): 최근 완결 1h봉의 ar_pctile이 반대 레짐(50% 경계)으로 복귀하면 즉시 청산.
      3) 보유 12개 15m봉(3h) 경과 시 봉 종가 강제청산.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get(
    "ABDIR_REPO_SRC", "/home/user/study/.claude/worktrees/agent-a2fbb751bd3675e81/src"))

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
    mode: str                 # "M"(모멘텀) | "R"(평균회귀)
    direction: str             # "long"/"short"(최종 체결 방향)
    raw_direction: str          # 원신호 방향(반전 대조군 구분용)
    gate: str                   # "ar"|"none"|"atrp"|"reverse_regime"
    signal_idx: int              # 1h 신호확정 인덱스(i)
    confirm_idx: int              # 15m 확인봉 인덱스(k)
    entry_idx: int                 # 15m 진입 인덱스(k+1)
    entry_time: pd.Timestamp
    entry_price: float
    fixed_stop: float
    quantity: float
    risk_amount: float
    ar_pctile_at_signal: float
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
    ar_window: int = common.AR_WINDOW
    pctile_entry_lo: float = common.PCTILE_ENTRY_LO
    pctile_entry_hi: float = common.PCTILE_ENTRY_HI
    burst_lookback: int = common.BURST_LOOKBACK
    burst_mult: float = common.BURST_MULT
    trail_mult: float = common.TRAIL_MULT
    stop_mult: float = common.STOP_MULT
    max_hold_bars: int = common.MAX_HOLD_BARS_15M
    gate: str = "ar"          # ar|none|atrp|reverse_regime
    direction_mode: str = "normal"   # normal|reverse|reverse_noinvalidation
    invalidation_exit: bool = True
    modes: tuple[str, ...] = ("M", "R")   # 서브모드 필터(서브모드별 분리비교용)
    confirm_scan_bars: int = 1    # 설계판단 대안검증용: 1=단일확인봉(기본), >1=해당 개수만큼 스캔
    fee_on: bool = True
    starting_equity: float = 10_000.0


def _completed_1h_counts(df1h_index: pd.DatetimeIndex, ts15_ns: np.ndarray) -> np.ndarray:
    """15m 타임스탬프(ns) 각각에 대해 '그 시각까지 완결된 1h 봉 개수'."""
    ends = df1h_index.asi8 + NS_1H
    return np.searchsorted(ends, ts15_ns, side="right")


def _detect_1h_events(sig: common.Signals, cfg: RunConfig) -> list[dict]:
    """1h 봉마다 트리거·게이트·방향을 판정해 이벤트 리스트로 반환(모두 causal)."""
    df1h = sig.df1h
    n = len(df1h)
    close = df1h["close"].to_numpy(float)
    atr1h = sig.atr14_1h.to_numpy(float)
    bb_up = sig.bb_upper.to_numpy(float)
    bb_lo = sig.bb_lower.to_numpy(float)

    if cfg.gate == "atrp":
        pctile = sig.atrp_pctile.to_numpy(float)
    else:
        pctile = sig.ar_pctile.to_numpy(float)

    events = []
    lb = cfg.burst_lookback
    for i in range(lb, n):
        p = pctile[i]
        if not np.isfinite(p):
            continue
        c_i = close[i]
        atr_i = atr1h[i]
        if not (np.isfinite(atr_i) and atr_i > 0 and np.isfinite(c_i)):
            continue

        # --- 모멘텀 트리거 ---
        if "M" in cfg.modes:
            cumret = close[i] - close[i - lb]
            if cumret >= cfg.burst_mult * atr_i:
                raw_dir = "long"
            elif cumret <= -cfg.burst_mult * atr_i:
                raw_dir = "short"
            else:
                raw_dir = None
            if raw_dir is not None:
                if cfg.gate == "none":
                    gate_ok = True
                elif cfg.gate == "reverse_regime":
                    gate_ok = p >= cfg.pctile_entry_hi   # 레짐 반전 대조군③: 모멘텀은 고스프레드에서
                else:  # ar|atrp
                    gate_ok = p <= cfg.pctile_entry_lo
                if gate_ok:
                    events.append(dict(signal_idx=i, mode="M", raw_direction=raw_dir, pctile=p))

        # --- 평균회귀 트리거 ---
        if "R" in cfg.modes:
            u, lo = bb_up[i], bb_lo[i]
            if np.isfinite(u) and c_i > u:
                raw_dir = "short"  # 상단 초과 -> 페이드 숏(반대방향 베팅)
            elif np.isfinite(lo) and c_i < lo:
                raw_dir = "long"
            else:
                raw_dir = None
            if raw_dir is not None:
                if cfg.gate == "none":
                    gate_ok = True
                elif cfg.gate == "reverse_regime":
                    gate_ok = p <= cfg.pctile_entry_lo  # 레짐 반전 대조군③: 평균회귀는 저스프레드에서
                else:  # ar|atrp
                    gate_ok = p >= cfg.pctile_entry_hi
                if gate_ok:
                    events.append(dict(signal_idx=i, mode="R", raw_direction=raw_dir, pctile=p))
    return events


def run_symbol(symbol: str, sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager
              ) -> list[TradeRec]:
    df1h = sig.df1h
    df15m = sig.df15m
    n15 = len(df15m)

    o15 = df15m["open"].to_numpy(float)
    h15 = df15m["high"].to_numpy(float)
    l15 = df15m["low"].to_numpy(float)
    c15 = df15m["close"].to_numpy(float)
    atr15 = sig.atr14_15m.to_numpy(float)
    ts15_ns = df15m.index.asi8

    bb_up1h = sig.bb_upper.to_numpy(float)
    bb_lo1h = sig.bb_lower.to_numpy(float)

    # 레짐 무효화 청산의 판정원(regime_pctile_1h)은 진입게이트와 동일한 지표를 써야 내적으로
    # 일관적이다(atrp 대조군에서 진입은 ATR%로 걸러놓고 청산은 AR로 판정하면 두 대조군의 취지가
    # 뒤섞인다). reverse_regime 대조군은 진입 레짐 자체가 뒤집혀 있으므로 무효화 임계도 함께
    # 뒤집어야 한다 — ⚠️자체발견 버그: 최초 구현에서 이를 놓쳐 reverse_regime 대조군이 진입 직후
    # (holding_bars=0) 617/699건 "regime_invalidated"로 즉시청산되는 현상을 발견·수정했다(반전
    # 대조군이 원신호 조건에 결부된 임계를 그대로 재사용해 구조적으로 즉시청산되는, 과거 여러
    # 라운드에서 반복 확인된 버그 클래스와 동일 패턴).
    if cfg.gate == "atrp":
        regime_pctile_1h = sig.atrp_pctile.to_numpy(float)
    else:
        regime_pctile_1h = sig.ar_pctile.to_numpy(float)
    regime_flipped = cfg.gate == "reverse_regime"
    counts15 = _completed_1h_counts(df1h.index, ts15_ns)  # 15m ts별 완결 1h봉 개수

    events = _detect_1h_events(sig, cfg)
    if not events:
        return []

    # 1h 신호확정시각(T = index[i]+1h)에 대응하는 15m 확인봉(k, 첫 open_time>=T)
    idx1h_ns = df1h.index.asi8
    events.sort(key=lambda e: e["signal_idx"])

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    lev = settings.leverage_for(symbol[:-4] + "/USDT")
    next_available_i = -1

    for ev in events:
        i = ev["signal_idx"]
        mode = ev["mode"]
        raw_direction = ev["raw_direction"]
        pctile_at_signal = ev["pctile"]
        T_ns = idx1h_ns[i] + NS_1H
        k = int(np.searchsorted(ts15_ns, T_ns, side="left"))
        if k >= n15 - 1:
            continue
        if k <= next_available_i:
            continue  # 동시 포지션 금지(직전 거래 보유 중)

        # --- 15m 확인(기본: k 단일봉. confirm_scan_bars>1 이면 설계판단 대안검증용으로
        # k..k+scan-1 범위에서 첫 확인봉을 찾는다 — 확인 실패 시 재시도 없이 폐기하는 기본
        # 설계가 결과를 유리하게 만든 것은 아닌지 대안 실행으로 점검) ---
        k_confirm = None
        for kk in range(k, min(k + cfg.confirm_scan_bars, n15)):
            if mode == "M":
                if raw_direction == "long":
                    ok = c15[kk] > o15[kk]
                else:
                    ok = c15[kk] < o15[kk]
            else:  # R
                if raw_direction == "long":
                    lo_lvl = bb_lo1h[i]
                    ok = np.isfinite(lo_lvl) and c15[kk] > lo_lvl
                else:
                    up_lvl = bb_up1h[i]
                    ok = np.isfinite(up_lvl) and c15[kk] < up_lvl
            if ok:
                k_confirm = kk
                break
        if k_confirm is None:
            continue
        k = k_confirm

        entry_i = k + 1
        if entry_i >= n15 - 1 or entry_i <= next_available_i:
            continue

        if cfg.direction_mode in ("reverse", "reverse_noinvalidation"):
            direction = "short" if raw_direction == "long" else "long"
        else:
            direction = raw_direction

        entry_raw = o15[entry_i]
        atr_v = atr15[k]  # 확인봉(k)까지의 ATR — entry_i 자신은 아직 모름
        if not (np.isfinite(atr_v) and atr_v > 0 and entry_raw > 0):
            continue

        sl_dist = cfg.stop_mult * atr_v
        fill_px = _fill(entry_raw, direction, closing=False, fee_on=cfg.fee_on)
        if direction == "long":
            fixed_stop = fill_px - sl_dist
            dirn = Direction.LONG
        else:
            fixed_stop = fill_px + sl_dist
            dirn = Direction.SHORT

        # 반전 대조군 주의: 리스크 거리(sl_dist)는 방향 무관 ATR로 1회만 계산되고 진입가 기준
        # 대칭 재배치된다(방향성 조건으로 선택된 진입봉의 "그 방향 자연스러운 극값"을 스톱으로
        # 쓰지 않음 — ATR은 방향 비대칭이 없어 이 함정에서 원천 안전).
        plan = risk.build_plan_with_stop(symbol, dirn, fill_px, fixed_stop, fill_px, equity,
                                         leverage=lev)
        if plan is None or plan.quantity <= 0:
            continue

        fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
        trade = TradeRec(symbol=symbol, mode=mode, direction=direction,
                         raw_direction=raw_direction, gate=cfg.gate, signal_idx=i,
                         confirm_idx=k, entry_idx=entry_i, entry_time=df15m.index[entry_i],
                         entry_price=fill_px, fixed_stop=fixed_stop, quantity=plan.quantity,
                         risk_amount=plan.risk_amount, ar_pctile_at_signal=pctile_at_signal,
                         fees=fee0)
        equity -= fee0

        is_long = direction == "long"
        exit_i = None; exit_px = None; reason = ""
        running_extreme = entry_raw
        j = entry_i
        max_j = min(n15 - 1, entry_i + cfg.max_hold_bars + 2)
        do_invalidation = cfg.invalidation_exit and cfg.direction_mode != "reverse_noinvalidation"
        while j <= max_j:
            holding = j - entry_i
            prev = j - 1
            atr_prev = atr15[prev] if prev >= 0 else np.nan
            trail_level = np.nan
            if np.isfinite(atr_prev) and atr_prev > 0:
                if is_long:
                    trail_level = running_extreme - cfg.trail_mult * atr_prev
                else:
                    trail_level = running_extreme + cfg.trail_mult * atr_prev

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

            # 레짐 무효화 조기청산: 직전 완결 1h봉의 ar_pctile이 반대 레짐 경계로 복귀
            # (raw_direction·mode 기준 — 반전 대조군에서도 원신호 레짐 기준으로 판정, "서사적
            # 테제 무효화"류라 최종방향 참조 원칙의 예외로 취급하되 reverse_noinvalidation으로
            # 완전 비활성판을 병행 실행해 결론 불변 여부를 실증한다).
            if do_invalidation:
                cnt = counts15[j]
                if cnt >= 1:
                    p_now = regime_pctile_1h[cnt - 1]
                    if np.isfinite(p_now):
                        m_invalidated = (p_now < 0.50) if regime_flipped else (p_now > 0.50)
                        r_invalidated = (p_now > 0.50) if regime_flipped else (p_now < 0.50)
                        if mode == "M" and m_invalidated:
                            exit_i = j; exit_px = o15[j]; reason = "regime_invalidated"; break
                        if mode == "R" and r_invalidated:
                            exit_i = j; exit_px = o15[j]; reason = "regime_invalidated"; break

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
    return common.load_all_signals(symbols)


def run_all(symbols_sig: dict[str, common.Signals], cfg: RunConfig
           ) -> dict[str, list[TradeRec]]:
    settings = get_settings()
    risk = RiskManager(settings)
    out = {}
    for sym, sig in symbols_sig.items():
        out[sym] = run_symbol(sym, sig, cfg, settings, risk)
    return out
