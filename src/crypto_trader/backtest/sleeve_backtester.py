"""슬리브 백테스터 — 라이브와 동일한 슬리브 전략(swing/mid/scalp)을 재생.

라이브 워커와 조건을 맞춘다:
  - 시그널 TF 윈도우 = 최근 200봉 (라이브 fetch limit=200 과 동일)
  - 확인 TF 윈도우 = 완결된 상위봉 최근 100개 (리샘플, lookahead 방지:
    현재 진행 중인 상위봉은 제외 — 보수적)
  - 수수료: 테이커 왕복 (기본 0.05%/side) + 슬리피지 (기본 0.02%)
  - 같은 봉에 SL/TP 둘 다 닿으면 손절 우선(보수적)

단순화(문서화된 근사):
  - TWAP 분할 진입은 신호봉 종가+슬리피지 일괄 체결로 근사
  - 단타 OI 는 과거 이력이 없어 백테스트에서 제외(oi_delta=None → 통과)
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..config import Settings
from ..risk import RiskManager
from ..signals import indicators as ind
from ..signals.base import Direction
from ..strategy import Action, MidStrategy, ScalpStrategy, SwingStrategy
from ..strategy.regime import detect_regime, Regime
from ..strategy.swing import SwingPosition
from .backtester import BacktestResult, Trade
from .multi_tf import TF_RULE, resample_ohlcv

SIGNAL_WINDOW = 200
CONFIRM_WINDOW = 100


class SleeveBacktester:
    # 청산 후 재진입 금지 봉수(과매매 억제). 슬리브별 기본값.
    DEFAULT_COOLDOWN = {"scalp": 15, "mid": 8, "swing": 2}

    def __init__(self, settings: Settings, sleeve_kind: str,
                 confirm_tf: str | None = None,
                 starting_equity: float = 10_000.0, warmup: int = 60,
                 taker_fee: float = 0.0005, slippage: float = 0.0002,
                 cooldown_bars: int | None = None,
                 maker_entry: bool = False, maker_fee: float = 0.0002,
                 leverage: int | None = None,
                 scalp_exit_mode: str = "momentum",
                 entry_window_sec: int = 0, entry_fine_df=None,
                 strategy_kwargs: dict | None = None):
        self.s = settings
        # 진입창 모델링: >0 이면 신호봉 종가 대신 '진입 창(초)' 동안의 고운(1m) 종가 평균으로
        # 체결(TWAP 시간분산 근사). entry_fine_df 는 같은 심볼의 1m OHLCV(DatetimeIndex).
        self.entry_window_sec = entry_window_sec
        self._fine = entry_fine_df
        # 빠른 창 조회용 사전계산(정렬된 ns 타임스탬프 + 종가 배열 → searchsorted O(logN))
        self._fine_ts = None
        self._fine_close = None
        if entry_fine_df is not None and len(entry_fine_df):
            self._fine_ts = entry_fine_df.index.asi8
            self._fine_close = entry_fine_df["close"].to_numpy(dtype=float)
        self.kind = sleeve_kind
        self.confirm_tf = confirm_tf
        self.starting_equity = starting_equity
        self.warmup = warmup
        self.taker_fee = taker_fee
        self.slippage = slippage
        # maker_entry: TWAP 지정가(post-only) 진입 가정 — 진입만 메이커 수수료,
        # 진입 슬리피지 0 (호가에 걸어 체결). 청산(SL/시장가)은 테이커 유지.
        # 주의: 실제로는 미체결 위험이 있어 낙관적 가정임.
        self.maker_entry = maker_entry
        self.maker_fee = maker_fee
        self.cooldown_bars = (cooldown_bars if cooldown_bars is not None
                              else self.DEFAULT_COOLDOWN.get(sleeve_kind, 0))
        # scalp 청산 모드:
        #   'momentum'       — 신고가 갱신 → 다음봉 종가 전량 청산
        #   'momentum_split' — 다음봉 종가 50% + 그다음봉 종가 50% 분할 청산
        #   'bandwalk'       — 밴드 워킹: 종가가 볼린저 중심선(SMA20)을 깰 때까지 보유
        #   'momentum_bandwalk' — 모멘텀 시점 50% 익절 + 나머지 50% 밴드워킹 러너
        #   'tp'             — 고정 TP
        self.scalp_exit_mode = scalp_exit_mode
        self.risk = RiskManager(settings, max_leverage=leverage)

        kw = strategy_kwargs or {}
        if sleeve_kind == "scalp":
            self.strategy = ScalpStrategy(settings, **kw)
        elif sleeve_kind == "mid":
            self.strategy = MidStrategy(settings, **kw)
        elif sleeve_kind == "swing":
            self.strategy = SwingStrategy(settings, **kw)
        else:
            raise ValueError(f"지원하지 않는 슬리브: {sleeve_kind}")

    # ------------------------------------------------------------ 헬퍼

    def _confirm_slices(self, df: pd.DataFrame):
        """확인 TF 리샘플 + 각 시그널봉 시점의 '완결 상위봉 수' 사전 계산."""
        if self.confirm_tf is None:
            return None, None
        confirm = resample_ohlcv(df, self.confirm_tf)
        delta = pd.tseries.frequencies.to_offset(TF_RULE[self.confirm_tf])
        ends = (confirm.index + delta).asi8          # 상위봉 종료 시각
        sig_ts = df.index.asi8
        counts = np.searchsorted(ends, sig_ts, side="right")  # t 까지 완결된 상위봉 수
        return confirm, counts

    def _confirm_window(self, confirm, counts, i):
        if confirm is None:
            return None
        n = int(counts[i])
        if n < 20:
            return None
        lo = max(0, n - CONFIRM_WINDOW)
        return confirm.iloc[lo:n]

    def _fill(self, price: float, direction: Direction, closing: bool = False) -> float:
        """슬리피지 반영 체결가. 메이커 진입 가정 시 진입 슬리피지 0."""
        if not closing and self.maker_entry:
            return price
        adverse = 1 if (direction is Direction.LONG) != closing else -1
        return price * (1 + adverse * self.slippage)

    def _fee(self, notional: float, closing: bool = False) -> float:
        rate = self.maker_fee if (not closing and self.maker_entry) else self.taker_fee
        return abs(notional) * rate

    @staticmethod
    def _pnl(direction: Direction, entry: float, exit_price: float, qty: float) -> float:
        return (exit_price - entry) * qty if direction is Direction.LONG else (entry - exit_price) * qty

    @staticmethod
    def _sl_tp_hit(direction: Direction, high: float, low: float,
                   stop: float, tp: float) -> tuple[float | None, str]:
        if direction is Direction.LONG:
            if low <= stop:
                return stop, "stop_loss"
            if high >= tp:
                return tp, "take_profit"
        else:
            if high >= stop:
                return stop, "stop_loss"
            if low <= tp:
                return tp, "take_profit"
        return None, ""

    # ------------------------------------------------------------ 메인

    def run(self, symbol: str, df: pd.DataFrame) -> BacktestResult:
        result = BacktestResult(symbol, starting_equity=self.starting_equity)
        equity = self.starting_equity
        trade: Trade | None = None
        alloc_frac = 0.0
        stage = 1

        confirm, counts = self._confirm_slices(df)
        atr_series = ind.atr(df)
        last_exit_idx = -10**9
        # scalp 모멘텀 청산 상태: 신호봉 고/저 기준, 갱신되면 다음봉 종가 청산
        self._scalp_ref: dict | None = None

        for i in range(self.warmup, len(df)):
            bar = df.iloc[i]
            price, high, low = float(bar["close"]), float(bar["high"]), float(bar["low"])
            window = df.iloc[max(0, i - SIGNAL_WINDOW + 1): i + 1]
            confirm_win = self._confirm_window(confirm, counts, i)

            # 1) SL/TP 인트라바 체크 (손절 우선 — 보수적)
            if trade is not None:
                exit_px, reason = self._sl_tp_hit(trade.direction, high, low,
                                                  trade.stop_price, trade.take_profit)
                if exit_px is not None:
                    fill = self._fill(exit_px, trade.direction, closing=True)
                    pnl = self._close(trade, i, fill, reason, df)
                    # 분할 익절 후 잔량이 SL 로 끝난 경우: 앞선 부분 익절 손익 합산
                    if self._scalp_ref and self._scalp_ref.get("partial_pnl"):
                        trade.pnl += self._scalp_ref["partial_pnl"]
                    equity += pnl
                    trade = None
                    alloc_frac, stage = 0.0, 1
                    last_exit_idx = i
                    self._scalp_ref = None

            # 1b-0) scalp 밴드워킹 청산: 종가가 SMA20(중심선)을 이탈하면 청산.
            #       최소익절 가드 적용 — 이탈해도 min_tp 미만 이익이면 SL/추가하락 대기 없이
            #       그냥 청산(추세 종료로 간주). 손실 중 이탈도 청산(SL 보완).
            if (trade is not None and self.kind == "scalp"
                    and self.scalp_exit_mode == "bandwalk"):
                sma20 = float(window["close"].iloc[-20:].mean())
                broke = (price < sma20 if trade.direction is Direction.LONG
                         else price > sma20)
                if broke:
                    fill = self._fill(price, trade.direction, closing=True)
                    equity += self._close(trade, i, fill, "bandwalk_exit", df)
                    trade = None
                    last_exit_idx = i
                    self._scalp_ref = None

            # 1b-0b) 하이브리드: 절반 모멘텀 익절 후 잔량은 밴드워킹 러너
            if (trade is not None and self.kind == "scalp"
                    and self.scalp_exit_mode == "momentum_bandwalk"
                    and self._scalp_ref is not None
                    and self._scalp_ref.get("runner")):
                sma20 = float(window["close"].iloc[-20:].mean())
                broke = (price < sma20 if trade.direction is Direction.LONG
                         else price > sma20)
                if broke:
                    fill = self._fill(price, trade.direction, closing=True)
                    pnl = self._close(trade, i, fill, "runner_bandwalk", df)
                    trade.pnl += self._scalp_ref.get("partial_pnl", 0.0)
                    equity += pnl
                    trade = None
                    last_exit_idx = i
                    self._scalp_ref = None

            # 1b) scalp 모멘텀 청산: 신호봉 고가/저가 갱신 후
            #     momentum       → 다음봉 종가 전량 청산
            #     momentum_split → 다음봉 종가 50%, 그다음봉 종가 나머지 50%
            #     (최소 익절 미달이면 재무장 대기, SL 은 계속 유효)
            if (trade is not None and self.kind == "scalp"
                    and self.scalp_exit_mode in ("momentum", "momentum_split",
                                                 "momentum_bandwalk")
                    and self._scalp_ref is not None
                    and not self._scalp_ref.get("runner")):
                ref = self._scalp_ref
                min_tp = getattr(self.strategy, "min_tp_frac", 0.0008)

                # 분할 2단계: 나머지 50% 를 그다음봉 종가에 무조건 청산
                if trade is not None and ref.get("final_at") is not None \
                        and i >= ref["final_at"]:
                    fill = self._fill(price, trade.direction, closing=True)
                    pnl = self._close(trade, i, fill, "momentum_split", df)
                    trade.pnl += ref.get("partial_pnl", 0.0)
                    equity += pnl
                    trade = None
                    last_exit_idx = i
                    self._scalp_ref = None

                armed_at = ref.get("armed_at") if trade is not None else None
                if trade is not None and armed_at is not None and i > armed_at \
                        and ref.get("final_at") is None:
                    profit_frac = ((price - trade.entry_price) / trade.entry_price
                                   if trade.direction is Direction.LONG
                                   else (trade.entry_price - price) / trade.entry_price)
                    if profit_frac >= min_tp:
                        if self.scalp_exit_mode in ("momentum_split", "momentum_bandwalk"):
                            # 1단계: 절반 익절. split 은 다음봉 종가 예약,
                            # bandwalk 하이브리드는 잔량을 러너로 전환.
                            half = trade.quantity / 2.0
                            fill = self._fill(price, trade.direction, closing=True)
                            fee1 = self._fee(fill * half, closing=True)
                            pnl1 = self._pnl(trade.direction, trade.entry_price,
                                             fill, half) - fee1
                            equity += pnl1
                            trade.quantity -= half
                            ref["partial_pnl"] = ref.get("partial_pnl", 0.0) + pnl1
                            if self.scalp_exit_mode == "momentum_split":
                                ref["final_at"] = i + 1
                            else:
                                ref["runner"] = True
                        else:
                            fill = self._fill(price, trade.direction, closing=True)
                            equity += self._close(trade, i, fill, "momentum_tp", df)
                            trade = None
                            last_exit_idx = i
                            self._scalp_ref = None
                    else:
                        ref["armed_at"] = None  # 익절 최소치 미달 → 재무장 대기
                if trade is not None and self._scalp_ref is not None \
                        and self._scalp_ref.get("armed_at") is None \
                        and self._scalp_ref.get("final_at") is None:
                    if trade.direction is Direction.LONG and high > ref["high"]:
                        ref["armed_at"] = i
                    elif trade.direction is Direction.SHORT and low < ref["low"]:
                        ref["armed_at"] = i

            # 쿨다운: 청산 직후 재진입 금지 (과매매 억제)
            in_cooldown = trade is None and (i - last_exit_idx) <= self.cooldown_bars

            # 2) 전략 결정
            cur_dir = trade.direction if trade else None
            if in_cooldown:
                result.equity_curve.append(equity)
                continue
            had_trade = trade is not None
            if self.kind == "swing":
                pos = None
                if trade is not None:
                    pos = SwingPosition(trade.direction, stage, alloc_frac,
                                        trade.entry_price, trade.stop_price)
                d = self.strategy.decide(symbol, window, confirm_win, pos)
                trade, equity, alloc_frac, stage = self._apply_swing(
                    result, trade, d, i, price, equity, alloc_frac, stage, df)
            elif self.kind == "mid":
                d = self.strategy.decide(symbol, window, confirm_win, cur_dir)
                trade, equity = self._apply_simple(result, trade, d, i, price,
                                                   equity, atr_series, df, use_plan=True)
            else:  # scalp
                regime = detect_regime(confirm_win)[0] if confirm_win is not None else Regime.NEUTRAL
                d = self.strategy.decide(symbol, window, oi_delta=None,
                                         current_direction=cur_dir, confirm_regime=regime)
                trade, equity = self._apply_simple(result, trade, d, i, price,
                                                   equity, atr_series, df, use_plan=False)

            if had_trade and trade is None:
                last_exit_idx = i  # 시그널 청산도 쿨다운 대상

            result.equity_curve.append(equity)

        # 미청산 정리
        if trade is not None and trade.exit_idx is None:
            fill = self._fill(float(df["close"].iloc[-1]), trade.direction, closing=True)
            pnl = self._close(trade, len(df) - 1, fill, "end_of_data", df)
            if result.equity_curve:
                result.equity_curve[-1] += pnl

        return result

    # ------------------------------------------------------------ 적용

    def _open_trade(self, result, direction, i, price, qty, stop, tp, df) -> Trade:
        fill = self._fill(price, direction)
        t = Trade(symbol=result.symbol, direction=direction, entry_idx=i,
                  entry_price=fill, stop_price=stop, take_profit=tp, quantity=qty,
                  opened_at=str(df.index[i]))
        t.fees += self._fee(fill * qty)
        result.trades.append(t)
        return t

    def _close(self, trade: Trade, idx: int, fill: float, reason: str, df) -> float:
        fee = self._fee(fill * trade.quantity, closing=True)
        trade.fees += fee
        pnl = self._pnl(trade.direction, trade.entry_price, fill, trade.quantity) - trade.fees
        trade.exit_idx = idx
        trade.exit_price = fill
        trade.pnl = pnl
        trade.reason = reason
        trade.closed_at = str(df.index[idx])
        trade.holding_bars = idx - trade.entry_idx
        return pnl

    def _apply_simple(self, result, trade, d, i, price, equity, atr_series, df,
                      use_plan: bool):
        """mid/scalp: 단일 진입/청산 모델."""
        if trade is not None and d.action is Action.CLOSE:
            fill = self._fill(price, trade.direction, closing=True)
            equity += self._close(trade, i, fill, d.reason or "signal_exit", df)
            return None, equity
        if trade is None and d.action in (Action.OPEN_LONG, Action.OPEN_SHORT):
            if use_plan:  # mid/regime: 전략 제시 SL/TP 있으면 사용, 없으면 ATR 기본
                if getattr(d, "stop_price", 0.0):
                    plan = self.risk.build_plan_with_stop(result.symbol, d.direction, price,
                                                          d.stop_price, d.take_profit, equity)
                else:
                    atr_v = float(atr_series.iloc[i])
                    plan = self.risk.build_plan(result.symbol, d.direction, price, atr_v, equity)
            else:         # scalp: 전략 제시 SL/TP 사이징 (라이브 _size_plan 과 동일)
                if self.s.position_margin_pct > 0:  # 증거금 기준: 포지션 크기 SL거리와 무관
                    margin = equity * (self.s.position_margin_pct / 100.0)
                    plan = self.risk.build_plan_by_margin(result.symbol, d.direction, price,
                                                          d.stop_price, d.take_profit, margin,
                                                          leverage=self.risk.max_leverage)
                else:                                # 리스크 기준: SL 넓히면 포지션 축소
                    plan = self.risk.build_plan_with_stop(result.symbol, d.direction, price,
                                                          d.stop_price, d.take_profit, equity)
            if plan is not None:
                entry_px = price
                if self.kind == "scalp" and self.entry_window_sec > 0:
                    win = self._entry_window_fill(i, df)
                    if win is not None:
                        entry_px = win
                trade = self._open_trade(result, d.direction, i, entry_px, plan.quantity,
                                         plan.stop_price, plan.take_profit, df)
                # scalp 모멘텀 모드: 고정 TP 비활성(신고가→다음봉 종가로 청산)
                if self.kind == "scalp" and self.scalp_exit_mode == "momentum":
                    self._scalp_ref = {"high": d.signal_high, "low": d.signal_low,
                                       "armed_at": None}
                    trade.take_profit = (float("inf") if d.direction is Direction.LONG
                                         else 0.0)
        return trade, equity

    def _entry_window_fill(self, i, df):
        """신호봉 종료 후 entry_window_sec 동안의 1m 종가 평균(진입 TWAP 근사). 없으면 None.

        정렬된 ns 타임스탬프 배열에 searchsorted 로 O(logN) 조회(전체 스캔 금지)."""
        if self._fine_ts is None or self.entry_window_sec <= 0 or i + 1 >= len(df):
            return None
        close_ns = int(df.index[i].value) + int((df.index[i + 1] - df.index[i]).value)
        win_end_ns = close_ns + self.entry_window_sec * 1_000_000_000
        lo = int(np.searchsorted(self._fine_ts, close_ns, side="left"))
        hi = int(np.searchsorted(self._fine_ts, win_end_ns, side="left"))
        if hi <= lo:
            return None
        return float(self._fine_close[lo:hi].mean())

    def _apply_swing(self, result, trade, d, i, price, equity, alloc_frac, stage, df):
        """swing: 배분 기반 + 피라미딩."""
        if d.action in (Action.OPEN_LONG, Action.OPEN_SHORT) and trade is None:
            qty = (d.target_frac * equity) / price if price > 0 else 0.0
            if qty > 0:
                trade = self._open_trade(result, d.direction, i, price, qty,
                                         d.stop_price, d.take_profit, df)
                alloc_frac, stage = d.target_frac, d.stage
        elif d.action is Action.ADD and trade is not None:
            add_frac = d.target_frac - alloc_frac
            if add_frac > 1e-9:
                add_qty = (add_frac * equity) / price if price > 0 else 0.0
                if add_qty > 0:
                    fill = self._fill(price, trade.direction)
                    total = trade.quantity + add_qty
                    trade.entry_price = (trade.entry_price * trade.quantity + fill * add_qty) / total
                    trade.quantity = total
                    trade.fees += self._fee(fill * add_qty)
                    trade.num_adds += 1
                    alloc_frac = d.target_frac
            # SL/TP 갱신(트레일링 포함)
            trade.stop_price = d.stop_price
            if d.take_profit:
                trade.take_profit = d.take_profit
            stage = d.stage
        return trade, equity, alloc_frac, stage
