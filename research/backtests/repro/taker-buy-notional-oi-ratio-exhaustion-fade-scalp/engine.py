"""테이커 매수체결대금/OI명목가치 순간비율 극단 소진 반전 스캘프 — 백테스트 엔진.

신호(15m, z-score) → 15m 진입 매핑(구현 설계 판단, 스펙 문면이 정확한 매핑을 명시하지 않음):
  - 신호봉 j (완전히 닫힌 15m 봉)의 flow_buy_ratio/flow_sell_ratio z-score 와 body_ratio 로
    트리거 판정(룩어헤드 없음 — 신호봉 자신의 확정 OHLCV/OI 만 사용).
  - 체결: 신호봉 j 의 "다음" 15m 봉(j+1) 의 시가에 체결(shift(1) 과 동일한 인과관계).
  - ATR(14,15m) 은 신호봉 j 시점까지의 값(atr14_15m.iloc[j], j 자신의 고가/저가 포함 — 이미
    닫힌 봉이므로 룩어헤드 아님)을 SL/트레일 배수 산정에 고정 사용.
  - 1h EMA20 확인: 신호봉 j 의 "시가 시점"까지 완결된 마지막 1h 봉의 EMA20 이, ema_lookback_1h
    봉 전 대비 뚜렷하게(|slope|>=ema_slope_th_pct) 진입 방향과 반대면 스킵.
  - 청산 우선순위(같은 15m 봉 내 동시발생 시 보수적으로 SL 우선):
      1) 스톱(초기 SL 또는 트레일링 중 더 타이트한 쪽, 매 봉 "직전 봉까지의" 유리한 극값으로만
         단조 타이트닝 — 동봉 룩어헤드 방지) 터치.
      2) 고정 R:R(rr_target) 목표 터치.
      3) 보유 max_hold_bars 경과 시 봉 종가 강제청산.
  - 초기 SL = min/max(신호봉의 반대쪽 극값, 진입가∓ATR14×atr_stop_mult) 중 진입가에 더 가까운
    (타이트한) 쪽. 두 후보 중 진입가와 같은 방향에 있지 않은(부호가 맞지 않는) 후보는 제외.

반전 대조군(reverse=True): 동일 트리거 시점에서 반대 방향으로 진입하되, 리스크 거리는 "반전
방향의 자연스러운 극값"으로 새로 계산하지 않고 원신호 방향 기준으로 1회 계산한 값을 그대로
대칭 재배치한다(CLAUDE.md 가 반복 경고한 "방향성 조건으로 선택된 진입봉에서 반전 스톱이
저절로 타이트해지는" 편향 회피). 트레일링의 running-extreme 자체는 실제 가격 경로를 그대로
따라가므로 편향 문제가 없어 반전 방향 그대로 추적한다.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd

sys.path.insert(0, os.environ.get("TBOI_REPO_SRC", "/home/user/study/src"))

from crypto_trader.config import get_settings  # noqa: E402
from crypto_trader.risk import RiskManager  # noqa: E402
from crypto_trader.signals.base import Direction  # noqa: E402

import common  # noqa: E402

TAKER_FEE = common.TAKER_FEE
SLIPPAGE = common.SLIPPAGE


@dataclass
class RunConfig:
    mode: str = "oi_buy_sell"     # "oi_buy_sell"(스펙 기본) | "total_vol"(대조군①) |
                                  # "vol24h_buy_sell"(대조군②)
    z_th: float = 3.0
    body_th: float = 0.40
    atr_stop_mult: float = 1.0
    atr_trail_mult: float = 1.5
    rr_target: float = 1.3
    max_hold_bars: int = 10
    use_1h_confirm: bool = True
    ema_lookback_1h: int = 3
    ema_slope_th_pct: float = 0.003   # 0.3% — "뚜렷하게 반대"의 정량 임계치(구현 설계 판단)
    reverse: bool = False
    fee_on: bool = True
    starting_equity: float = 10_000.0
    warmup: int | None = None


@dataclass
class TradeRec:
    symbol: str
    mode: str
    reverse: bool
    signal_idx: int         # 신호봉(15m) 인덱스
    entry_idx: int
    entry_time: pd.Timestamp
    entry_price: float
    direction: str           # "long"/"short" (실제 체결 방향, reverse 반영 후)
    orig_direction: str      # 트리거가 가리킨 원신호 방향(reverse=False 면 direction 과 동일)
    initial_stop: float
    tp_price: float
    risk_distance: float
    quantity: float
    risk_amount: float
    z_trigger: float
    body_ratio_trigger: float
    exit_idx: int | None = None
    exit_time: pd.Timestamp | None = None
    exit_price: float | None = None
    pnl: float = 0.0
    fees: float = 0.0
    r_multiple: float = 0.0
    reason: str = ""
    holding_bars: int = 0
    trail_used: bool = False


def _fill(price: float, is_long: bool, closing: bool, fee_on: bool) -> float:
    if not fee_on:
        return price
    adverse = 1 if (is_long != closing) else -1
    return price * (1 + adverse * SLIPPAGE)


def _fee(notional: float, fee_on: bool) -> float:
    if not fee_on:
        return 0.0
    return abs(notional) * TAKER_FEE


def _trigger(sig: common.Signals, j: int, cfg: RunConfig) -> tuple[str | None, float]:
    """신호봉 j 에서 (방향 or None, 트리거 z값) 반환. 방향은 원신호(fade) 방향
    ("short"=매수유량소진 페이드, "long"=매도유량소진 페이드)."""
    if cfg.mode == "oi_buy_sell":
        zb, zs = sig.z_buy[j], sig.z_sell[j]
    elif cfg.mode == "vol24h_buy_sell":
        zb, zs = sig.z_vol24h_buy[j], sig.z_vol24h_sell[j]
    elif cfg.mode == "total_vol":
        zt = sig.z_total[j]
        br = sig.body_ratio.iloc[j]
        if not (np.isfinite(zt) and np.isfinite(br)):
            return None, float("nan")
        if not (zt >= cfg.z_th and br <= cfg.body_th):
            return None, float("nan")
        tbf = sig.taker_buy_frac.iloc[j]
        if not np.isfinite(tbf):
            return None, float("nan")
        return ("short" if tbf > 0.5 else "long"), zt
    else:
        raise ValueError(cfg.mode)

    br = sig.body_ratio.iloc[j]
    if not np.isfinite(br) or br > cfg.body_th:
        return None, float("nan")
    buy_trig = np.isfinite(zb) and zb >= cfg.z_th
    sell_trig = np.isfinite(zs) and zs >= cfg.z_th
    if buy_trig and sell_trig:
        # 이론상 배타적에 가까우나(매수/매도 비중 합이 총거래대금), 극히 드문 동시발화 시
        # 더 큰 z(더 극단적인 소진) 쪽을 채택 — 문서화된 설계 판단.
        return ("short", zb) if zb >= zs else ("long", zs)
    if buy_trig:
        return "short", zb
    if sell_trig:
        return "long", zs
    return None, float("nan")


def _confirm_1h_ok(sig: common.Signals, j: int, direction: str, cfg: RunConfig) -> bool:
    if not cfg.use_1h_confirm:
        return True
    cnt = sig.completed_1h_idx[j]
    k = cnt - 1 - cfg.ema_lookback_1h  # slope 계산이 이미 lookback 만큼 과거를 보므로 인덱스는 cnt-1
    if cnt - 1 < 0 or k < 0:
        return True  # 확인 불가(워밍업 구간) — 통과 처리(스킵하지 않음)
    slope = sig.ema20_1h_slope[cnt - 1]
    if not np.isfinite(slope):
        return True
    if direction == "short" and slope >= cfg.ema_slope_th_pct:
        return False   # 뚜렷한 상승추세가 숏(하락 페이드)과 반대
    if direction == "long" and slope <= -cfg.ema_slope_th_pct:
        return False   # 뚜렷한 하락추세가 롱(상승 페이드)과 반대
    return True


def run_symbol(symbol: str, sig: common.Signals, cfg: RunConfig, settings, risk: RiskManager
               ) -> list[TradeRec]:
    df15m = sig.df15m
    n15 = len(df15m)
    o15 = df15m["open"].to_numpy(float)
    h15 = df15m["high"].to_numpy(float)
    l15 = df15m["low"].to_numpy(float)
    c15 = df15m["close"].to_numpy(float)
    atr15 = sig.atr14_15m.to_numpy(float)
    body_arr = sig.body_ratio.to_numpy(float)

    warmup = cfg.warmup if cfg.warmup is not None else 250
    warmup = min(warmup, n15 - 2)

    trades: list[TradeRec] = []
    equity = cfg.starting_equity
    lev = settings.leverage_for(symbol[:-4] + "/USDT")
    next_available_i = -1  # 동시 포지션 금지

    for j in range(max(0, warmup), n15 - 1):
        orig_dir, zval = _trigger(sig, j, cfg)
        if orig_dir is None:
            continue
        if not _confirm_1h_ok(sig, j, orig_dir, cfg):
            continue

        entry_i = j + 1
        if entry_i <= next_available_i:
            continue  # 이전 트레이드 보유 중

        atr_v = atr15[j]
        entry_raw = o15[entry_i]
        if not (np.isfinite(atr_v) and atr_v > 0 and entry_raw > 0):
            continue

        # ---- 원신호 방향 기준 리스크거리 1회 계산(반전 대조군도 이 값을 그대로 대칭 재배치) ----
        sig_high, sig_low = h15[j], l15[j]
        if orig_dir == "short":
            cand = [c for c in (sig_high, entry_raw + cfg.atr_stop_mult * atr_v) if c > entry_raw]
            if not cand:
                continue
            orig_stop = min(cand)
        else:
            cand = [c for c in (sig_low, entry_raw - cfg.atr_stop_mult * atr_v) if c < entry_raw]
            if not cand:
                continue
            orig_stop = max(cand)
        risk_distance = abs(entry_raw - orig_stop)
        if risk_distance <= 0:
            continue

        # ---- 실제 체결 방향(반전 여부 반영) ----
        direction = orig_dir if not cfg.reverse else ("long" if orig_dir == "short" else "short")
        is_long = direction == "long"
        if is_long:
            initial_stop = entry_raw - risk_distance
            tp_price = entry_raw + cfg.rr_target * risk_distance
        else:
            initial_stop = entry_raw + risk_distance
            tp_price = entry_raw - cfg.rr_target * risk_distance

        fill_px = _fill(entry_raw, is_long, closing=False, fee_on=cfg.fee_on)
        dirn = Direction.LONG if is_long else Direction.SHORT
        plan = risk.build_plan_with_stop(symbol, dirn, fill_px, initial_stop, tp_price, equity,
                                         leverage=lev)
        if plan is None or plan.quantity <= 0:
            continue

        fee0 = _fee(fill_px * plan.quantity, cfg.fee_on)
        trade = TradeRec(symbol=symbol, mode=cfg.mode, reverse=cfg.reverse, signal_idx=j,
                         entry_idx=entry_i, entry_time=df15m.index[entry_i], entry_price=fill_px,
                         direction=direction, orig_direction=orig_dir, initial_stop=initial_stop,
                         tp_price=tp_price, risk_distance=risk_distance, quantity=plan.quantity,
                         risk_amount=plan.risk_amount, z_trigger=zval,
                         body_ratio_trigger=body_arr[j], fees=fee0)

        # ------------------------------------------------ 보유 시뮬레이션(15m)
        eff_stop = initial_stop
        running_ext = entry_raw   # LONG: running high, SHORT: running low
        exit_i = None; exit_px = None; reason = ""
        i = entry_i
        max_i = min(n15 - 1, entry_i + cfg.max_hold_bars + 2)
        while i <= max_i:
            holding = i - entry_i
            # 트레일 후보(직전 봉까지의 running_ext 기준, 동봉 룩어헤드 방지) — 단조 타이트닝만.
            if is_long:
                trail_cand = running_ext - cfg.atr_trail_mult * atr_v
                new_stop = max(eff_stop, trail_cand)
            else:
                trail_cand = running_ext + cfg.atr_trail_mult * atr_v
                new_stop = min(eff_stop, trail_cand)
            if new_stop != eff_stop:
                trade.trail_used = True
            eff_stop = new_stop

            h, l, c = h15[i], l15[i], c15[i]
            sl_hit = (l <= eff_stop) if is_long else (h >= eff_stop)
            tp_hit = (h >= tp_price) if is_long else (l <= tp_price)
            if sl_hit:
                exit_i = i; exit_px = eff_stop
                reason = "stop_trail" if trade.trail_used and abs(eff_stop - initial_stop) > 1e-12 else "stop_initial"
                break
            if tp_hit:
                exit_i = i; exit_px = tp_price; reason = "take_profit"; break
            if holding >= cfg.max_hold_bars:
                exit_i = i; exit_px = c; reason = "time_exit"; break

            # 다음 반복을 위한 running extreme 갱신(이번 봉의 실현치 반영)
            running_ext = max(running_ext, h) if is_long else min(running_ext, l)
            i += 1
        if exit_i is None:
            exit_i = max_i; exit_px = c15[max_i]; reason = "data_end"

        fill_exit = _fill(exit_px, is_long, closing=True, fee_on=cfg.fee_on)
        fee1 = _fee(fill_exit * trade.quantity, cfg.fee_on)
        raw = ((fill_exit - trade.entry_price) if is_long
              else (trade.entry_price - fill_exit)) * trade.quantity
        total_fees = fee0 + fee1
        pnl = raw - total_fees   # ⚠️ 자체발견 버그(수정): 이전 버전은 pnl=raw-fee1 로 진입수수료
                                  # fee0 를 pnl 에서 누락(회계정합 점검에서 max|Δ|=117.98 로 적발됨).
                                  # equity 는 트레이드 종료 시 이 pnl 한 번으로만 갱신(진입시점
                                  # 조기차감 제거) — 동시포지션 금지라 순서상 문제 없음.
        trade.exit_idx = exit_i; trade.exit_time = df15m.index[exit_i]; trade.exit_price = fill_exit
        trade.pnl = pnl; trade.fees = total_fees; trade.reason = reason
        trade.holding_bars = exit_i - entry_i
        trade.r_multiple = pnl / trade.risk_amount if trade.risk_amount > 0 else 0.0
        equity += pnl
        trades.append(trade)
        next_available_i = exit_i

    return trades


def run_all(symbols_sig: dict[str, common.Signals], cfg: RunConfig
           ) -> dict[str, list[TradeRec]]:
    settings = get_settings()
    risk = RiskManager(settings)
    out = {}
    for sym, sig in symbols_sig.items():
        out[sym] = run_symbol(sym, sig, cfg, settings, risk)
    return out
