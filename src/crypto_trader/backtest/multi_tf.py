"""멀티 타임프레임 리샘플 — 시그널 TF 캔들에서 상위(확인) TF 캔들 생성.

lookahead 방지: 특정 시점 i 까지의 시그널 TF 데이터만으로 상위 TF 를 만들 때,
아직 안 닫힌 상위봉은 '현재까지의 부분 봉'으로 포함된다(실시간과 동일 조건).
"""
from __future__ import annotations

import pandas as pd

# pandas resample 규칙 매핑
TF_RULE = {
    "1m": "1min", "3m": "3min", "5m": "5min", "10m": "10min", "15m": "15min",
    "30m": "30min", "1h": "1h", "4h": "4h", "1d": "1D", "1w": "1W",
}


def resample_ohlcv(df: pd.DataFrame, target_tf: str) -> pd.DataFrame:
    """시그널 TF DataFrame(DatetimeIndex) → 상위 TF OHLCV.

    마지막 상위봉은 부분(진행 중) 봉일 수 있다 — 실시간 조건과 동일.
    """
    rule = TF_RULE.get(target_tf)
    if rule is None:
        raise ValueError(f"지원하지 않는 타임프레임: {target_tf}")
    out = pd.DataFrame({
        "open": df["open"].resample(rule).first(),
        "high": df["high"].resample(rule).max(),
        "low": df["low"].resample(rule).min(),
        "close": df["close"].resample(rule).last(),
        "volume": df["volume"].resample(rule).sum(),
    }).dropna(subset=["open", "close"])
    return out
