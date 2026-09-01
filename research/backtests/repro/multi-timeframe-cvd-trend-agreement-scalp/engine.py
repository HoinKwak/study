"""멀티TF CVD 추세 합치/불일치 필터 스캘프 — 백테스트 엔진.

엔트리: 15m 봉 i 종가 확정 시점에 (breakout AND vol_confirm AND CVD 게이트) 판정
        (룩어헤드 없음: breakout/vol_confirm 은 shift(1) 과거창만 사용, CVD5m/CVD1h 는
        merge_asof(backward) 로 '그 시각에 이미 닫힌' 값만 매핑) -> bar i+1 시가에 체결(shift(1)).
방향: breakout 방향(상단 돌파=롱/하단 돌파=숏), CVD 게이트가 같은 방향이어야 함(신호모드별로 다름).
청산: (1) 고정 SL = 신호봉(i) 시가 기준 리스크거리(|entry-open_i|)를 진입가에서 대칭 재배치.
      (2) ATR(15m,14) 트레일링×atr_trail_mult — 직전까지 닫힌 봉들의 극값 기준.
      (3) 테제 무효화: 체결 후 CVD_1h 기울기가 '원신호 방향'(orig_direction) 기준으로 반대부호
          전환되면 즉시 종가청산(스펙 명시 규칙). 원신호 기준을 쓰는 이유는 이 청산이 SL/트레일링류의
          리스크관리 메커니즘이 아니라 '테제 무효화' 서사형 청산이기 때문 — 방향성 조건으로 선택된
          진입봉에서 최종방향(반전 포함) 기준으로 이 청산을 두면, 반전모드는 진입 시점부터 이미
          CVD_1h 가 최종방향과 어긋나 있어(원신호 방향과는 합치) 구조적으로 즉시청산(1봉 퇴화)한다.
      (4) 시간청산: 진입 후 max_hold_hours 경과.
      같은 봉에서 여러 청산조건이 동시 성립하면 SL > 트레일링 > 테제무효화 > 시간청산 순 우선.
전 성과는 R-배수(risk_dist=|entry-signal_open|)로 계산 — 계좌소진/사이징 아티팩트 원천 차단.
"""
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

CVD_SHORT_WINDOW = 12   # 5m bars = 1h
CVD_LONG_WINDOW = 24    # 1h bars = 1 day


@dataclass
class RunConfig:
    slope_lookback: int = 6
    breakout_lookback: int = 10
    vol_confirm_mult: float = 1.2
    atr_trail_mult: float = 1.3
    max_hold_hours: int = 8
    signal_mode: str = "both"       # "both"(base) | "h1_only"(ctrl1) | "h5_only"(ctrl2) | "none"(ctrl3)
    direction_mode: str = "normal"  # "normal" | "reverse"
    cost_on: bool = True
    disable_thesis_exit: bool = False   # 3안: 테제무효화 청산 완전 비활성


@dataclass
class Signals:
    h15: pd.DataFrame
    breakout_up: np.ndarray
    breakout_down: np.ndarray
    vol_ratio: np.ndarray          # quote_volume[i] / rolling_mean(과거 breakout_lookback봉)
    sign5m: np.ndarray             # CVD_5m 기울기 부호(+1/-1/0/nan), 15m 그리드에 asof 매핑
    sign1h: np.ndarray             # CVD_1h 기울기 부호, 15m 그리드에 asof 매핑
    slope1h_at15: np.ndarray       # CVD_1h 기울기 원값(부호전환 감지용)
    atr15: np.ndarray


def build_signals(symbol: str, cfg: RunConfig) -> Signals | None:
    h15 = common.load_klines(symbol, "15m")
    h5 = common.load_klines(symbol, "5m")
    h1 = common.load_klines(symbol, "1h")
    if h15.empty or h5.empty or h1.empty:
        return None

    lb = cfg.breakout_lookback
    high_prev_max = h15["high"].shift(1).rolling(lb, min_periods=lb).max()
    low_prev_min = h15["low"].shift(1).rolling(lb, min_periods=lb).min()
    breakout_up = (h15["close"] > high_prev_max).to_numpy()
    breakout_down = (h15["close"] < low_prev_min).to_numpy()

    qv_mean_prev = h15["quote_volume"].shift(1).rolling(lb, min_periods=lb).mean()
    vol_ratio = (h15["quote_volume"] / qv_mean_prev).replace([np.inf, -np.inf], np.nan).to_numpy()

    cvd5 = common.rolling_cvd(h5, CVD_SHORT_WINDOW)
    cvd1h = common.rolling_cvd(h1, CVD_LONG_WINDOW)
    slope5 = common.slope(cvd5, cfg.slope_lookback)
    slope1h = common.slope(cvd1h, cfg.slope_lookback)

    close15 = (h15.index + pd.Timedelta(minutes=15)).astype("datetime64[ns, UTC]")
    slope5_at15 = common.map_asof_backward(pd.DatetimeIndex(close15), slope5, 300)
    slope1h_at15 = common.map_asof_backward(pd.DatetimeIndex(close15), slope1h, 3600)

    sign5m = np.sign(slope5_at15)
    sign1h = np.sign(slope1h_at15)

    atr15 = ind.atr(h15, 14).to_numpy(float)

    return Signals(h15=h15, breakout_up=breakout_up, breakout_down=breakout_down,
                   vol_ratio=vol_ratio, sign5m=sign5m, sign1h=sign1h,
                   slope1h_at15=slope1h_at15, atr15=atr15)


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


def _gate_ok(sig: Signals, i: int, orig_dir: str, mode: str) -> bool:
    want = 1.0 if orig_dir == "long" else -1.0
    s5, s1h = sig.sign5m[i], sig.sign1h[i]
    if mode == "both":
        return np.isfinite(s5) and np.isfinite(s1h) and s5 == want and s1h == want
    if mode == "h1_only":
        return np.isfinite(s1h) and s1h == want
    if mode == "h5_only":
        return np.isfinite(s5) and s5 == want
    if mode == "none":
        return True
    raise ValueError(mode)


def run_symbol(symbol: str, sig: Signals, cfg: RunConfig) -> list[TradeRec]:
    h15 = sig.h15
    n = len(h15)
    open_ = h15["open"].to_numpy(float)
    high = h15["high"].to_numpy(float)
    low = h15["low"].to_numpy(float)
    close = h15["close"].to_numpy(float)
    idx = h15.index

    max_hold_bars = int(round(cfg.max_hold_hours * 60 / 15))

    trades: list[TradeRec] = []
    trade: TradeRec | None = None
    pending: dict | None = None
    extreme = 0.0

    for i in range(n):
        # 0) 대기 체결
        if pending is not None and trade is None:
            sidx = pending["signal_idx"]
            direction = pending["direction"]
            fill_px = _fill(open_[i], direction, closing=False, apply_slip=cfg.cost_on)
            risk_dist = pending["risk_dist"]
            if risk_dist > 0 and np.isfinite(risk_dist) and fill_px > 0:
                stop_price = fill_px - risk_dist if direction == "long" else fill_px + risk_dist
                trade = TradeRec(symbol=symbol, direction=direction,
                                 orig_direction=pending["orig_direction"],
                                 entry_idx=i, entry_time=idx[i], entry_price=fill_px,
                                 stop_price=stop_price, risk_dist=risk_dist)
                extreme = fill_px
            pending = None

        # 1) 보유 중 청산 판정
        if trade is not None:
            h, l, c = high[i], low[i], close[i]
            is_long = trade.direction == "long"
            exit_px = None
            reason = ""
            # 1a) 고정 SL
            if is_long and l <= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"
            elif (not is_long) and h >= trade.stop_price:
                exit_px, reason = trade.stop_price, "stop_loss"
            # 1b) ATR 트레일링(직전까지 닫힌 봉 기준 극값 + 직전봉 ATR)
            if exit_px is None:
                atr_v = sig.atr15[i - 1] if i > 0 else np.nan
                if np.isfinite(atr_v):
                    if is_long:
                        level = extreme - cfg.atr_trail_mult * atr_v
                        if l <= level:
                            exit_px, reason = level, "atr_trail"
                    else:
                        level = extreme + cfg.atr_trail_mult * atr_v
                        if h >= level:
                            exit_px, reason = level, "atr_trail"
            # 1c) 테제 무효화(CVD_1h 기울기가 원신호 방향 기준 반대부호 전환)
            if exit_px is None and not cfg.disable_thesis_exit:
                s1h = sig.sign1h[i]
                orig_want = 1.0 if trade.orig_direction == "long" else -1.0
                if np.isfinite(s1h) and s1h == -orig_want:
                    exit_px, reason = c, "thesis_invalidation"
            # 1d) 시간청산
            if exit_px is None and (i - trade.entry_idx) >= max_hold_bars:
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
            else:
                extreme = max(extreme, h) if is_long else min(extreme, l)

        # 2) 신규 진입 판정(이번 bar 종가 기준) -> 다음 bar 시가 체결
        if trade is None and pending is None and i + 1 < n:
            vr = sig.vol_ratio[i]
            if np.isfinite(vr) and vr >= cfg.vol_confirm_mult:
                orig_dir = None
                if sig.breakout_up[i]:
                    orig_dir = "long"
                elif sig.breakout_down[i]:
                    orig_dir = "short"
                if orig_dir is not None and _gate_ok(sig, i, orig_dir, cfg.signal_mode):
                    exec_dir = orig_dir
                    if cfg.direction_mode == "reverse":
                        exec_dir = "short" if orig_dir == "long" else "long"
                    # risk_dist: 스펙의 SL 정의(신호봉 시가)를 '신호봉 종가-시가 거리'로 근사해
                    # 신호 확정 시점(체결 전)에 1회 계산 — 정방향에서는 fill_px(다음봉 시가+슬리피지)가
                    # close_i 에 근접하므로 stop=entry-risk_dist가 사실상 open_i 에 근접해 스펙 정의와
                    # 부합한다. 이 거리를 방향에 무관하게 고정해 반전모드에도 대칭 재배치함으로써
                    # "방향성 조건으로 선택된 진입봉에서 반전 스톱을 그 방향의 자연스러운 극값으로
                    # 재계산하면 안 된다"는 규칙을 지킨다(신호봉 시가를 반전 숏에 그대로 쓰면 진입가보다
                    # 낮은 시가가 숏의 SL이 되어 방향이 뒤집힌 스톱이 되는 구조적 결함 방지).
                    risk_dist = abs(close[i] - open_[i])
                    pending = {"direction": exec_dir, "orig_direction": orig_dir,
                              "signal_idx": i, "risk_dist": risk_dist}

    return trades


def load_all_signals(symbols=common.SYMBOLS, cfg: RunConfig = RunConfig()) -> dict[str, Signals]:
    out = {}
    for s in symbols:
        sig = build_signals(s, cfg)
        if sig is not None:
            out[s] = sig
    return out


def run_all(symbols_sig: dict[str, Signals], cfg: RunConfig) -> dict[str, list[TradeRec]]:
    return {sym: run_symbol(sym, sig, cfg) for sym, sig in symbols_sig.items()}
