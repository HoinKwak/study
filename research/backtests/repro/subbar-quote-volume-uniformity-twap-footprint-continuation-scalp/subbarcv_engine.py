"""트레이드 시뮬레이션 엔진 — 서브캔들 거래대금 균일성(CV) TWAP 흔적 추종.

1h 신호(hourly 프레임의 long_trigger/short_trigger, 이미 shift 없이 해당 바 종가
시점까지의 정보로만 계산됨) → 다음 15m봉(정확히 신호봉 마감 시각 = entry 시각)의
시가에 진입. 이후 15m봉 단위로 보유·청산 관리(1h ATR 은 hour_close 시각에 asof
결합해 15m 각 시점에서 "그 시점에 이미 확정된" ATR 값만 사용 — 룩어헤드 방지).

청산 우선순위(매 15m 보유봉마다, 인트라바 저가/고가 기준 — 보수적으로 스톱 우선):
  1) 스톱 터치: 초기 스톱 = min/max(신호봉 시가, entry∓ATR(1h,14)×1.2) 중 "타이트한 쪽"
     (신호봉 시가 스펙 원문 그대로 사용, ATR 은 진입 시점 값 고정), 이후 ATR×trail_mult
     트레일링으로 유리한 방향으로만 갱신(라쳇). 트레일링에 쓰는 ATR 은 보유기간 중
     새로 확정되는 1h ATR 로 갱신(asof, 룩어헤드 없음).
  2) 최대 보유 max_hold_hours(기본 8h=32개 15m봉) 경과 — 마지막 15m봉 종가 청산.

방향반전(REV) 대조군: reverse=True 시 트리거 플래그를 스왑하되, 리스크 거리(초기 스톱까지의
거리)는 반드시 "원신호 방향 기준 1회" 계산한 뒤 진입가 기준으로 대칭 재배치한다(반전 방향의
"자연스러운" 극값을 다시 계산하지 않음 — 방향성 조건으로 선택된 진입봉이라 반전 스톱이
저절로 타이트해지는 편향 방지).

수수료/슬리피지: 원가 청구가 아니라 왕복 정액 비용(ROUNDTRIP_COST=0.14%)을 raw_ret 에서
차감(기존 impl 스크립트들과 동일 관례).
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = 2 * (TAKER_FEE + SLIPPAGE)  # 0.0014


@dataclass
class TradeRec:
    symbol: str
    direction: str
    signal_hour: pd.Timestamp
    entry_time: pd.Timestamp
    entry_idx: int
    exit_time: pd.Timestamp
    exit_idx: int
    entry_price: float
    exit_price: float
    stop_init: float
    exit_reason: str
    bars_held: int
    raw_ret: float
    net_ret: float
    r_gross: float
    r_net: float
    risk_frac: float


def _asof_backward_atr(hourly: pd.DataFrame, df15_index: pd.DatetimeIndex) -> np.ndarray:
    """1h ATR 을 15m 인덱스에 asof(backward) 결합 — hour_close(=hour+1h) 시각에
    "확정"되는 값이므로, 그 시각 이후의 15m 봉부터 참조 가능(룩어헤드 방지)."""
    avail_time = hourly.index + pd.Timedelta(hours=1)
    left = pd.DataFrame({"t": pd.DatetimeIndex(df15_index)})
    right = pd.DataFrame({"t": pd.DatetimeIndex(avail_time), "atr": hourly["atr"].to_numpy(float)})
    right = right.drop_duplicates(subset="t", keep="last").sort_values("t")
    merged = pd.merge_asof(left, right, on="t", direction="backward")
    return merged["atr"].to_numpy(float)


def simulate_symbol(hourly: pd.DataFrame, df15: pd.DataFrame, symbol: str,
                     trail_mult: float = 1.5, sl_atr_mult: float = 1.2,
                     max_hold_hours: int = 8, reverse: bool = False,
                     warmup_bars: int = 1500) -> list[TradeRec]:
    n15 = len(df15)
    idx15 = df15.index
    op15 = df15["open"].to_numpy(float)
    hi15 = df15["high"].to_numpy(float)
    lo15 = df15["low"].to_numpy(float)
    cl15 = df15["close"].to_numpy(float)

    atr15 = _asof_backward_atr(hourly, idx15)

    # 15m 인덱스 위치 조회용
    pos_of = {ts: i for i, ts in enumerate(idx15)}

    max_hold_bars = max_hold_hours * 4  # 15m 단위

    long_trig = hourly["long_trigger"].to_numpy(bool)
    short_trig = hourly["short_trigger"].to_numpy(bool)
    if reverse:
        raw_long, raw_short = long_trig, short_trig
        long_trig, short_trig = short_trig.copy(), long_trig.copy()
    else:
        raw_long, raw_short = long_trig, short_trig

    h_open = hourly["open"].to_numpy(float)
    h_atr = hourly["atr"].to_numpy(float)
    h_index = hourly.index

    trades: list[TradeRec] = []
    n_hourly = len(hourly)
    last_exit_15idx = -10**9

    for hi in range(warmup_bars, n_hourly):
        is_long = long_trig[hi]
        is_short = short_trig[hi]
        if not (is_long or is_short):
            continue
        direction = "long" if is_long else "short"
        sig_time = h_index[hi]
        entry_time = sig_time + pd.Timedelta(hours=1)
        entry_idx = pos_of.get(entry_time)
        if entry_idx is None or entry_idx <= last_exit_15idx or entry_idx >= n15 - 1:
            continue
        entry_price = op15[entry_idx]
        atr_entry = h_atr[hi]
        if not (atr_entry == atr_entry and atr_entry > 0):
            continue

        # --- 리스크 거리는 원신호 방향(raw_long/raw_short) 기준 1회 계산 ---
        orig_is_long = bool(raw_long[hi])
        sig_open = h_open[hi]
        if orig_is_long:
            cand1 = sig_open                       # 신호봉 시가(원방향 하단)
            cand2 = entry_price - sl_atr_mult * atr_entry
            natural_stop = max(cand1, cand2)        # 타이트한 쪽(entry 에 더 가까운 쪽)
            dist = abs(entry_price - natural_stop)
        else:
            cand1 = sig_open
            cand2 = entry_price + sl_atr_mult * atr_entry
            natural_stop = min(cand1, cand2)
            dist = abs(entry_price - natural_stop)
        if dist <= 0:
            continue

        if direction == "long":
            stop_init = entry_price - dist
        else:
            stop_init = entry_price + dist

        ext = entry_price
        stop = stop_init
        exit_idx = None
        exit_price = None
        exit_reason = None
        upper_k = min(entry_idx + max_hold_bars, n15)
        for k in range(entry_idx, upper_k):
            bars_held = k - entry_idx + 1
            if direction == "long":
                hit_stop = lo15[k] <= stop
            else:
                hit_stop = hi15[k] >= stop
            if hit_stop:
                exit_idx, exit_price, exit_reason = k, stop, (
                    "stop_trail" if stop != stop_init else "stop_initial")
                break
            if bars_held >= max_hold_bars:
                exit_idx, exit_price, exit_reason = k, cl15[k], "time"
                break
            # 유리한 방향으로만 트레일 갱신(이번 봉 정보로 다음 봉 스톱 결정 — 다음 루프에 반영)
            atr_v = atr15[k]
            if direction == "long":
                ext = max(ext, hi15[k])
                if atr_v == atr_v and atr_v > 0:
                    stop = max(stop, ext - trail_mult * atr_v)
            else:
                ext = min(ext, lo15[k])
                if atr_v == atr_v and atr_v > 0:
                    stop = min(stop, ext + trail_mult * atr_v)
        if exit_idx is None:
            last_k = min(entry_idx + max_hold_bars - 1, n15 - 1)
            exit_idx, exit_price, exit_reason = last_k, cl15[last_k], "time_eof"

        if direction == "long":
            raw_ret = exit_price / entry_price - 1.0
        else:
            raw_ret = entry_price / exit_price - 1.0
        net_ret = raw_ret - ROUNDTRIP_COST
        risk_frac = dist / entry_price
        if risk_frac <= 0:
            risk_frac = 0.001
        r_gross = raw_ret / risk_frac
        r_net = net_ret / risk_frac

        trades.append(TradeRec(
            symbol=symbol, direction=direction, signal_hour=sig_time,
            entry_time=idx15[entry_idx], entry_idx=entry_idx,
            exit_time=idx15[exit_idx], exit_idx=exit_idx,
            entry_price=entry_price, exit_price=exit_price, stop_init=stop_init,
            exit_reason=exit_reason, bars_held=exit_idx - entry_idx,
            raw_ret=raw_ret, net_ret=net_ret, r_gross=r_gross, r_net=r_net,
            risk_frac=risk_frac,
        ))
        last_exit_15idx = exit_idx

    return trades


def trades_to_df(trades: list[TradeRec]) -> pd.DataFrame:
    cols = ["symbol", "direction", "signal_hour", "entry_time", "entry_idx", "exit_time",
            "exit_idx", "entry_price", "exit_price", "stop_init", "exit_reason", "bars_held",
            "raw_ret", "net_ret", "r_gross", "r_net", "risk_frac"]
    if not trades:
        return pd.DataFrame(columns=cols)
    return pd.DataFrame([t.__dict__ for t in trades])


def simulate_donchian(df15: pd.DataFrame, symbol: str, lookback: int = 20,
                       trail_mult: float = 1.5, sl_atr_mult: float = 1.2,
                       max_hold_hours: int = 8, atr_period_1h_equiv_bars: int = 56,
                       warmup_bars: int = 500) -> list[TradeRec]:
    """게이트 없음 대조군(폐기조건 ①) — 순수 15m Donchian(20) 브레이크아웃.
    ATR 은 15m 자체 해상도로 계산(15m*56 ≈ 14h, 채택안 1h ATR(14) 스케일과 유사하게 맞춤).
    SL: 최근 20봉 채널 반대쪽 극값과 ATR×1.2 중 타이트한 쪽. 트레일링·시간청산 채택안과 동일 계열.
    """
    n = len(df15)
    idx = df15.index
    op = df15["open"].to_numpy(float)
    hi = df15["high"].to_numpy(float)
    lo = df15["low"].to_numpy(float)
    cl = df15["close"].to_numpy(float)

    h_l = df15["high"]; l_l = df15["low"]; c_l = df15["close"]
    prev_c = c_l.shift(1)
    tr = pd.concat([h_l - l_l, (h_l - prev_c).abs(), (l_l - prev_c).abs()], axis=1).max(axis=1)
    atr = tr.rolling(atr_period_1h_equiv_bars).mean().to_numpy(float)

    prior_high = pd.Series(hi).shift(1).rolling(lookback).max().to_numpy(float)
    prior_low = pd.Series(lo).shift(1).rolling(lookback).min().to_numpy(float)
    long_trig = cl > prior_high
    short_trig = cl < prior_low

    max_hold_bars = max_hold_hours * 4
    trades: list[TradeRec] = []
    last_exit = -10**9
    i = warmup_bars
    while i < n - 1:
        is_long = bool(long_trig[i]) if i < len(long_trig) else False
        is_short = bool(short_trig[i]) if i < len(short_trig) else False
        if not (is_long or is_short) or i <= last_exit:
            i += 1
            continue
        direction = "long" if is_long else "short"
        entry_idx = i + 1
        if entry_idx >= n:
            break
        entry_price = op[entry_idx]
        atr_entry = atr[i]
        if not (atr_entry == atr_entry and atr_entry > 0):
            i += 1
            continue
        channel_stop = prior_low[i] if direction == "long" else prior_high[i]
        if channel_stop != channel_stop:
            i += 1
            continue
        if direction == "long":
            cand2 = entry_price - sl_atr_mult * atr_entry
            natural_stop = max(channel_stop, cand2)
        else:
            cand2 = entry_price + sl_atr_mult * atr_entry
            natural_stop = min(channel_stop, cand2)
        dist = abs(entry_price - natural_stop)
        if dist <= 0:
            i += 1
            continue
        stop = entry_price - dist if direction == "long" else entry_price + dist
        stop_init = stop
        ext = entry_price
        exit_idx = None; exit_price = None; exit_reason = None
        upper_k = min(entry_idx + max_hold_bars, n)
        for k in range(entry_idx, upper_k):
            bars_held = k - entry_idx + 1
            hit_stop = lo[k] <= stop if direction == "long" else hi[k] >= stop
            if hit_stop:
                exit_idx, exit_price, exit_reason = k, stop, (
                    "stop_trail" if stop != stop_init else "stop_initial")
                break
            if bars_held >= max_hold_bars:
                exit_idx, exit_price, exit_reason = k, cl[k], "time"
                break
            atr_v = atr[k]
            if direction == "long":
                ext = max(ext, hi[k])
                if atr_v == atr_v and atr_v > 0:
                    stop = max(stop, ext - trail_mult * atr_v)
            else:
                ext = min(ext, lo[k])
                if atr_v == atr_v and atr_v > 0:
                    stop = min(stop, ext + trail_mult * atr_v)
        if exit_idx is None:
            last_k = min(entry_idx + max_hold_bars - 1, n - 1)
            exit_idx, exit_price, exit_reason = last_k, cl[last_k], "time_eof"
        if direction == "long":
            raw_ret = exit_price / entry_price - 1.0
        else:
            raw_ret = entry_price / exit_price - 1.0
        net_ret = raw_ret - ROUNDTRIP_COST
        risk_frac = dist / entry_price
        if risk_frac <= 0:
            risk_frac = 0.001
        r_gross = raw_ret / risk_frac
        r_net = net_ret / risk_frac
        trades.append(TradeRec(
            symbol=symbol, direction=direction, signal_hour=idx[i],
            entry_time=idx[entry_idx], entry_idx=entry_idx,
            exit_time=idx[exit_idx], exit_idx=exit_idx,
            entry_price=entry_price, exit_price=exit_price, stop_init=stop_init,
            exit_reason=exit_reason, bars_held=exit_idx - entry_idx,
            raw_ret=raw_ret, net_ret=net_ret, r_gross=r_gross, r_net=r_net,
            risk_frac=risk_frac,
        ))
        last_exit = exit_idx
        i = exit_idx + 1
    return trades
