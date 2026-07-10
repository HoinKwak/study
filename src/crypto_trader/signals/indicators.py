"""순수 pandas/numpy 기술지표 구현 (외부 TA 라이브러리 의존 없음).

모든 함수는 pandas Series/DataFrame 을 받아 Series 를 반환한다.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def rsi(close: pd.Series, period: int = 14) -> pd.Series:
    """Wilder RSI (0~100)."""
    delta = close.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)
    # Wilder smoothing == alpha 1/period 지수이동평균
    avg_gain = gain.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    rs = avg_gain / avg_loss
    out = 100.0 - (100.0 / (1.0 + rs))
    # 손실이 0인 구간(순수 상승) → RSI 100. warmup/무변동 구간 → 중립 50.
    out = out.mask((avg_loss == 0) & (avg_gain > 0), 100.0)
    return out.fillna(50.0)


def macd(close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
         ) -> tuple[pd.Series, pd.Series, pd.Series]:
    """(macd_line, signal_line, histogram)."""
    macd_line = ema(close, fast) - ema(close, slow)
    signal_line = ema(macd_line, signal)
    hist = macd_line - signal_line
    return macd_line, signal_line, hist


def bollinger_bands(close: pd.Series, period: int = 20, num_std: float = 2.0
                    ) -> tuple[pd.Series, pd.Series, pd.Series]:
    """(중심선(SMA), 상단, 하단) 볼린저밴드."""
    mid = close.rolling(window=period, min_periods=period).mean()
    std = close.rolling(window=period, min_periods=period).std(ddof=0)
    upper = mid + num_std * std
    lower = mid - num_std * std
    return mid, upper, lower


def true_range(df: pd.DataFrame) -> pd.Series:
    high, low, close = df["high"], df["low"], df["close"]
    prev_close = close.shift(1)
    tr = pd.concat(
        [(high - low), (high - prev_close).abs(), (low - prev_close).abs()],
        axis=1,
    ).max(axis=1)
    return tr


def atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    tr = true_range(df)
    return tr.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()


def supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0
               ) -> tuple[pd.Series, pd.Series]:
    """(supertrend_line, direction). direction: +1 상승(매수), -1 하락(매도).

    ATR 기반 추세 추종 지표. 방향이 -1→+1 로 바뀌면 매수 신호, 그 반대는 매도 신호.
    """
    # 주의: min_periods 있는 ATR 은 워밍업 구간이 NaN 이라 밴드 래칭이 NaN 에
    # 오염되어 방향 전환이 발생하지 않는 버그가 있었음 → 여기서는 첫 봉부터
    # 값이 정의되는 EWM ATR 을 사용한다.
    tr = true_range(df)
    atr_ = tr.ewm(alpha=1 / period, adjust=False).mean()
    hl2 = (df["high"] + df["low"]) / 2.0
    upper = hl2 + multiplier * atr_
    lower = hl2 - multiplier * atr_

    close = df["close"]
    n = len(df)
    final_upper = upper.copy()
    final_lower = lower.copy()
    st = pd.Series(index=df.index, dtype="float64")
    direction = pd.Series(1, index=df.index, dtype="int64")

    for i in range(1, n):
        # 밴드 잠금(래칭)
        final_upper.iloc[i] = (upper.iloc[i]
                               if (upper.iloc[i] < final_upper.iloc[i - 1]
                                   or close.iloc[i - 1] > final_upper.iloc[i - 1])
                               else final_upper.iloc[i - 1])
        final_lower.iloc[i] = (lower.iloc[i]
                               if (lower.iloc[i] > final_lower.iloc[i - 1]
                                   or close.iloc[i - 1] < final_lower.iloc[i - 1])
                               else final_lower.iloc[i - 1])
        # 방향 전환
        if close.iloc[i] > final_upper.iloc[i - 1]:
            direction.iloc[i] = 1
        elif close.iloc[i] < final_lower.iloc[i - 1]:
            direction.iloc[i] = -1
        else:
            direction.iloc[i] = direction.iloc[i - 1]
        st.iloc[i] = final_lower.iloc[i] if direction.iloc[i] == 1 else final_upper.iloc[i]

    return st, direction


def cvd_proxy(df: pd.DataFrame, taker_buy_col: str = "taker_buy_base") -> pd.Series:
    """누적 거래량 델타(CVD) 근사.

    바이낸스 캔들의 '테이커 매수 base 거래량' 이 있으면
    델타 = 2×테이커매수 − 총거래량 (= 테이커매수 − 테이커매도) 을 누적한다.
    해당 컬럼이 없으면 캔들 방향(종가>시가=+거래량)으로 근사한다.
    """
    if taker_buy_col in df.columns:
        delta = 2.0 * df[taker_buy_col] - df["volume"]
    else:
        sign = (df["close"] >= df["open"]).astype(float) * 2.0 - 1.0
        delta = sign * df["volume"]
    return delta.cumsum()


def adx(df: pd.DataFrame, period: int = 14) -> tuple[pd.Series, pd.Series, pd.Series]:
    """(adx, +DI, -DI). 추세 강도/방향."""
    high, low = df["high"], df["low"]
    up_move = high.diff()
    down_move = -low.diff()

    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    plus_dm = pd.Series(plus_dm, index=df.index)
    minus_dm = pd.Series(minus_dm, index=df.index)

    tr = true_range(df)
    atr_ = tr.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()

    plus_di = 100.0 * plus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr_.replace(0.0, np.nan)
    minus_di = 100.0 * minus_dm.ewm(alpha=1 / period, adjust=False).mean() / atr_.replace(0.0, np.nan)

    dx = 100.0 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0.0, np.nan)
    adx_ = dx.ewm(alpha=1 / period, adjust=False, min_periods=period).mean()
    return adx_.fillna(0.0), plus_di.fillna(0.0), minus_di.fillna(0.0)
