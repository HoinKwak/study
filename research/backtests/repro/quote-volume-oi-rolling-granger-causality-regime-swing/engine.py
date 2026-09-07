"""체결 엔진 — OI선행→거래대금선행 그레인저 레짐전환(+ret4h 부호 +EMA20/50 정렬)
-> 다음 4h봉 시가 진입 -> ATR 트레일링(×2.2, 래칫) + 고정 SL(×1.6×ATR신호봉, 대칭)
+ 레짐 무효화(다시 OI선행/무레짐 전환 시 즉시청산) + 18봉(3일) 시간청산. 전부 R-배수.

⚠️ 타이밍: signal_bar=i 에서 transition_qv[i]·ret4h[i]·ema_fast[i]/ema_slow[i] 전부 봉 i 의
종가로 확정(그레인저 p-value 는 causal 롤링 — granger.py 참고). entry_bar=i+1 시가에 지연없이
진입 가능(룩어헤드 아님). 레짐 무효화도 "봉 u 의 종가로 regime[u]!='qv_lead' 확정 -> 봉 u+1
시가에 청산" 순서로 causal 하게 처리한다(이 프로젝트에서 반복된 "확정시점보다 이른 시가로
청산"하는 1봉 조기청산 함정을 피하기 위해 oi-cusum 대비 타이밍을 한 단계 늦춤 — §자체발견 참고).

반전 대조군(reverse): risk_distance·SL·트레일링은 trade_dir 기준으로 재계산(진입가 대칭
재배치). 레짐 무효화 조건은 방향과 무관한 '테제 무효화'류라 뒤집지 않는다(CLAUDE.md 축적 규칙).
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd

from common import ROUND_TRIP_COST
from signals import Signals


@dataclass
class Trade:
    symbol: str
    signal_time: pd.Timestamp
    entry_time: pd.Timestamp
    entry_price: float
    direction: int            # 원신호 방향(1=롱,-1=숏), reverse 여부와 무관
    trade_dir: int             # 실제 매매 방향(reverse 시 -direction)
    atr_entry: float
    risk_distance: float
    exit_time: pd.Timestamp
    exit_price: float
    exit_reason: str
    hold_bars: int
    gross_R: float = field(init=False)

    def __post_init__(self):
        self.gross_R = (self.exit_price - self.entry_price) / self.risk_distance * self.trade_dir

    @property
    def net_R(self) -> float:
        cost_R = ROUND_TRIP_COST * self.entry_price / self.risk_distance
        return self.gross_R - cost_R


def simulate_trades(sig: Signals, entries: pd.DataFrame, stop_mult: float = 1.6,
                    atr_trail_mult: float = 2.2, max_hold_bars: int = 18,
                    reverse: bool = False, disable_regime_exit: bool = False) -> list[Trade]:
    """단일 심볼, 순차 체결(포지션 보유 중엔 새 신호 무시 — 스윙 저빈도 특성)."""
    if len(entries) == 0:
        return []
    price = sig.df
    atr = sig.atr14
    regime = sig.regime.to_numpy()  # 'qv_lead'/'oi_lead'/'none'
    n = len(price)
    idx = price.index
    close = price["close"].to_numpy()
    high = price["high"].to_numpy()
    low = price["low"].to_numpy()
    openp = price["open"].to_numpy()
    atr_arr = atr.to_numpy()

    entries = entries.sort_values("entry_time").reset_index(drop=True)
    trades: list[Trade] = []
    last_exit_time = None

    for _, e in entries.iterrows():
        entry_time = e["entry_time"]
        if last_exit_time is not None and entry_time <= last_exit_time:
            continue
        entry_bar = int(e["entry_bar"])
        entry_price = float(openp[entry_bar])
        direction = int(e["direction"])
        trade_dir = -direction if reverse else direction
        atr_entry = float(e["atr_entry"])
        risk_distance = atr_entry * stop_mult
        if risk_distance <= 0 or not np.isfinite(risk_distance):
            continue

        stop = entry_price - risk_distance if trade_dir == 1 else entry_price + risk_distance
        running_extreme = high[entry_bar] if trade_dir == 1 else low[entry_bar]
        active_stop = stop
        exit_trade = None

        for kk in range(1, max_hold_bars + 1):
            pos = entry_bar + kk
            if pos >= n:
                last = n - 1
                exit_trade = Trade(sig.symbol, e["signal_time"], entry_time, entry_price,
                                   direction, trade_dir, atr_entry, risk_distance,
                                   idx[last], float(close[last]), "data_end", kk)
                break

            # 1) 레짐 무효화 — 직전 봉(pos-1) 종가로 확정된 regime 이 'qv_lead' 가 아니면
            #    이 봉(pos) 시가에 즉시 청산(causal — 확정시점보다 이른 시가 사용 안 함).
            if not disable_regime_exit and regime[pos - 1] != "qv_lead":
                exit_trade = Trade(sig.symbol, e["signal_time"], entry_time, entry_price,
                                   direction, trade_dir, atr_entry, risk_distance,
                                   idx[pos], float(openp[pos]), "regime_invalidation", kk)
                break

            # 2) ATR 트레일링(전봉 ATR·running_extreme, 래칫) + 고정 SL 인트라바 체크
            atr_prev = float(atr_arr[pos - 1])
            if not np.isfinite(atr_prev) or atr_prev <= 0:
                atr_prev = atr_entry
            if trade_dir == 1:
                trail_stop = running_extreme - atr_trail_mult * atr_prev
                active_stop = max(active_stop, trail_stop)
                if low[pos] <= active_stop:
                    exit_trade = Trade(sig.symbol, e["signal_time"], entry_time, entry_price,
                                       direction, trade_dir, atr_entry, risk_distance,
                                       idx[pos], active_stop, "atr_trail_or_sl", kk)
                    break
            else:
                trail_stop = running_extreme + atr_trail_mult * atr_prev
                active_stop = min(active_stop, trail_stop)
                if high[pos] >= active_stop:
                    exit_trade = Trade(sig.symbol, e["signal_time"], entry_time, entry_price,
                                       direction, trade_dir, atr_entry, risk_distance,
                                       idx[pos], active_stop, "atr_trail_or_sl", kk)
                    break

            # 3) 시간청산
            if kk == max_hold_bars:
                exit_trade = Trade(sig.symbol, e["signal_time"], entry_time, entry_price,
                                   direction, trade_dir, atr_entry, risk_distance,
                                   idx[pos], float(close[pos]), "time", kk)
                break

            if trade_dir == 1:
                running_extreme = max(running_extreme, float(high[pos]))
            else:
                running_extreme = min(running_extreme, float(low[pos]))

        if exit_trade is not None:
            trades.append(exit_trade)
            last_exit_time = exit_trade.exit_time

    return trades


def trades_to_df(trades: list[Trade]) -> pd.DataFrame:
    if not trades:
        return pd.DataFrame()
    return pd.DataFrame([{
        "symbol": t.symbol, "signal_time": t.signal_time,
        "entry_time": t.entry_time, "entry_price": t.entry_price,
        "direction": t.direction, "trade_dir": t.trade_dir,
        "atr_entry": t.atr_entry, "risk_distance": t.risk_distance,
        "exit_time": t.exit_time, "exit_price": t.exit_price, "exit_reason": t.exit_reason,
        "hold_bars": t.hold_bars, "gross_R": t.gross_R, "net_R": t.net_R,
    } for t in trades])
