"""테이커 매수비율 롤링 분산 레짐 게이트 + Donchian 브레이크아웃 — 공통 로더/신호.

스펙: research/strategies/taker-buy-ratio-rolling-variance-regime-breakout-scalp.md
(커밋 7ec619d)

⚠️데이터 캐시 재사용: klines(15m/1h)·metrics(5분 `sum_taker_long_short_vol_ratio`) 원본은 동일
세션 스크래치패드의 `oiar1hl/data`(직전 OI AR(1) 반감기 백테스트가 받아둔 캐시, 569MB)를 그대로
읽기 전용으로 재사용한다(이후 OI-ZCR 백테스트도 동일 캐시를 재사용한 전례 있음). 재사용 타당성:
①동일 유니버스(BTC/ETH/BNB/SOL/XRP/DOGE/ADA) ②동일 TF(15m·1h) ③metrics CSV에 본 스펙이 쓰는
`sum_taker_long_short_vol_ratio` 필드가 실제로 포함돼 있음(직접 확인) ④기간 커버 확인(klines
2021-09~2026-06 58개월, metrics 종목당 1673~1764일 — IS 2022-01-01+워밍업, OOS 2026-06-30까지
전부 포함, `ls`로 파일 수 대조 확인). 파일 수정 없이 순수 로드만 하므로 오염 위험 없음.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

_repo_src = os.environ.get(
    "TBRV_REPO_SRC",
    "/home/user/study/.claude/worktrees/agent-a09efab3ace244b40/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "TBRV_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/tbrvar"))
# 원본 klines·metrics 는 oiar1hl 캐시를 읽기 전용 재사용(위 docstring 근거)
CACHE_DATA = Path(os.environ.get(
    "TBRV_CACHE_DATA",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiar1hl/data"))
KLINES_1H_DIR = CACHE_DATA / "klines_1h"
KLINES_15M_DIR = CACHE_DATA / "klines_15m"
METRICS_DIR = CACHE_DATA / "metrics"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = (TAKER_FEE + SLIPPAGE) * 2  # 0.14%

# ------------------------------------------------------------- 파라미터(스펙 기본값)
TVR_WINDOW = 24                # 15m*24 = 6시간(롤링 표준편차 윈도우)
TVR_PCTILE_TH = 30.0           # 백분위(0~100), 낮을수록 응축(저분산)
TVR_NORMALIZE_WINDOW_DAYS = 30
DONCHIAN_LB = 20
ATR_TRAIL_MULT = 1.5           # ATR(1h,14) 트레일링
ATR_STOP_MULT = 1.0            # ATR(15m,20) 고정 SL(신호봉 기준)
ATR_STOP_LB = 20               # SL 용 ATR 은 "최근 20봉(15m) ATR"(14 아님 — 스펙 문언 그대로)
MAX_HOLD_BARS = 24              # 15m*24 = 6시간
BARS_PER_DAY_15M = 96

_KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
               "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


# ------------------------------------------------------------------ 로더

def _load_klines(dirpath: Path, symbol: str, tf: str) -> pd.DataFrame:
    files = sorted(dirpath.glob(f"{symbol}-{tf}-*.csv"))
    parts = []
    for p in files:
        with open(p) as f:
            first = f.readline()
        has_header = "open_time" in first
        df = pd.read_csv(p, header=0 if has_header else None,
                         names=_KLINE_COLS if not has_header else None)
        df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
        if df.empty:
            continue
        df["open_time"] = df["open_time"].astype("int64")
        parts.append(df)
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    # ⚠️단위사고 회피: open_time 이 ms(13자리) 또는 us(16자리) 혼재 가능성 — 자릿수로 판별해 통일.
    ot = out["open_time"]
    is_us = ot.abs() > 10**14
    if is_us.any():
        out.loc[is_us, "open_time"] = out.loc[is_us, "open_time"] // 1000
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True)
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume", "quote_volume"]]
    # ⚠️pandas 3.0.5 ns 통일(join/merge_asof/Timedelta 산술 오정렬 방지, 다수 선례 확인)
    out.index = out.index.as_unit("ns")
    return out


@lru_cache(maxsize=None)
def load_klines_1h(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_1H_DIR, symbol, "1h")


@lru_cache(maxsize=None)
def load_klines_15m(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_15M_DIR, symbol, "15m")


@lru_cache(maxsize=None)
def load_metrics_5m(symbol: str) -> pd.DataFrame:
    """metrics 5분 원본 로드. create_time 은 날짜 문자열 → 명시적 format 파싱(us/ms 단위사고 회피).
    본 스펙이 쓰는 필드는 `sum_taker_long_short_vol_ratio`(테이커 매수/매도 체결액 비율)."""
    files = sorted(METRICS_DIR.glob(f"{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "symbol", "sum_taker_long_short_vol_ratio"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out.index = out.index.as_unit("ns")  # ns 명시 통일(klines 인덱스와 join 시 오정렬 방지)
    out["tvr"] = pd.to_numeric(out["sum_taker_long_short_vol_ratio"], errors="coerce")
    # ⚠️0-fill/빈문자열 결측 placeholder(선례 확인, OI 필드와 동일 패턴): 실제 비율은 0이 될 수
    # 없다(테이커 매수액이 0이 아닌 한) → 0 이하는 결측으로 명시 처리.
    out.loc[out["tvr"] <= 0, "tvr"] = np.nan
    return out


def tvr_15m_from_5m(m5: pd.DataFrame) -> pd.DataFrame:
    """5분 테이커매수비율 스냅샷 → 15m봉 마지막 값으로 정렬(스펙 문언 그대로:
    "5분 스냅샷을 15분봉 마지막 값으로 정렬"). OI 와 달리 비율(유량 지표)이라 diff 가 아니라
    레벨 자체를 그대로 쓴다. 빈 bin 은 NaN → 명시적 ffill, ffill 여부·5분 표본수는 품질추적용
    별도 컬럼으로 남긴다.

    ⚠️자체발견 버그(수정됨): `sum_taker_long_short_vol_ratio` 필드는 2021-12-30~2022-01-30(30일)
    ·2022-01-31~2022-05-09(98일) 두 구간에서 원본 자체가 통째로 결측이다(바이낸스가 해당 기간
    필드를 미보고 — OI 0-fill 결측과 같은 유형의 데이터 가용성 이슈, 구현 버그 아님). 무제한
    `ffill()`을 쓰면 갭 직전(2021-12-30)의 마지막 유효값이 128일 내내 상수로 복제되고, 그 결과
    `tvr_std`(상수 구간의 롤링표준편차)가 정확히 0이 돼 `tvr_std_pctile`이 항상 최하위(응축
    신호)로 오판되는 아티팩트가 생긴다 — IS 시작(2022-01-01) 직후 5개월이 이 아티팩트에 노출됨.
    `ffill(limit=4)`(최대 1시간, 15m봉 4개)로 제한해 단기 스냅샷 결손(브리프 아웃티지)만 보정하고
    장기 결측은 NaN 으로 남겨 downstream 계산(rolling std/mean)에서 자연히 제외되게 한다."""
    if m5.empty:
        return pd.DataFrame()
    s = m5["tvr"]
    last = s.resample("15min", label="left", closed="left").last()
    cnt = s.resample("15min", label="left", closed="left").count()
    filled = last.ffill(limit=4)
    out = pd.DataFrame({"tvr": filled, "tvr_raw_nan": last.isna(), "tvr_5m_count": cnt})
    return out


def rolling_zscore(x: np.ndarray, window: int) -> np.ndarray:
    xs = pd.Series(x)
    m = xs.rolling(window).mean()
    sd = xs.rolling(window).std(ddof=0)
    z = (xs - m) / sd
    z = z.where(sd > 1e-12)
    return z.to_numpy()


def rolling_pctile_of_last(x: pd.Series, window: int, min_frac: float = 0.9) -> pd.Series:
    """x(t) 가 자신의 최근 window 개(과거+현재) 히스토리 내에서 차지하는 백분위 순위(0~100).
    pd.Series.rolling(window).rank(pct=True) 는 각 윈도우의 '마지막 값'의 백분위 순위를 반환
    — "tvr_std_pctile = 롤링 30일 창 기준 백분위"와 정확히 일치(causal, 미래 데이터 미사용).

    ⚠️min_periods 함정(oi-zcr 백테스트에서 실측된 것과 동일 메커니즘): min_periods 미지정 시
    기본값이 window 전체(완전 충족)라, 입력 x(tvr_std)에 든 짧은 고립 NaN 블립 하나가 그 뒤
    30일(2880봉) 전체를 NaN 으로 전염시킬 수 있다. min_periods 를 window*min_frac(기본 90%)로
    완화해 고립 블립이 최대 30일을 통째로 잠식하지 않게 한다."""
    min_periods = max(1, int(window * min_frac))
    return x.rolling(window, min_periods=min_periods).rank(pct=True) * 100.0


# ------------------------------------------------------------------ 신호 구축

@dataclass
class Signals:
    df1h: pd.DataFrame          # 1h klines
    df15m: pd.DataFrame          # 15m klines + tvr
    tvr: pd.Series                # 15m 정렬된 테이커매수비율 레벨
    tvr_std: pd.Series             # tvr 의 24봉(6h) 롤링 표준편차
    tvr_std_pctile: pd.Series       # tvr_std 의 30일 롤링 백분위(낮을수록 응축)
    tvr_mean_window: pd.Series      # 24봉(tvr_window) 롤링 tvr 평균(방향 확인용, >1.0/<1.0)
    rv15: pd.Series                  # 대조군(신호원 교체)·동어반복용: 15m 실현변동성(24봉 롤링 로그수익률 std)
    rv15_pctile: pd.Series            # rv15 의 30일 롤링 백분위(낮을수록 저변동성=레인지 스퀴즈)
    bbw: pd.Series                     # 볼린저밴드폭((상단-하단)/중앙, 20봉) — 동어반복 대조용
    bbw_pctile: pd.Series               # bbw 의 30일 롤링 백분위
    oi_change_stdev: pd.Series           # 동어반복 점검용: OI 변화(15m) 의 24봉 롤링 표준편차
                                          # (oi-change-rolling-stdev-regime 계열 프록시)
    vol_z: pd.Series                      # 동어반복·신호원 교체 후보: quote_volume 30일 롤링 z
    donch_upper: pd.Series                 # 20봉 Donchian 상단(자기 제외, shift(1) 적용됨)
    donch_lower: pd.Series                  # 20봉 Donchian 하단(자기 제외)
    atr14_15m: pd.Series                     # ATR(14, 15m) — 참고용
    atr20_15m: pd.Series                      # ATR(20, 15m) — SL 용(스펙 문언 "최근 20봉 ATR")
    atr14_1h: pd.Series                        # ATR(14, 1h) — TP 트레일링용
    tvr_5m_count: pd.Series
    tvr_raw_nan: pd.Series


def _atr_sma(df: pd.DataFrame, period: int) -> pd.Series:
    """SMA 방식 ATR(스펙이 '최근 N봉 ATR'이라고만 적어 평활 방식을 명시하지 않음 — 기존
    ind.atr()은 Wilder EWM 이라 SL 용은 문언 그대로 단순이동평균 True Range로 별도 계산해
    Wilder-ATR(14, TP 트레일링용)과 구분한다)."""
    tr = ind.true_range(df)
    return tr.rolling(period, min_periods=period).mean()


def build_signals(symbol: str) -> Signals | None:
    df1h = load_klines_1h(symbol)
    df15m = load_klines_15m(symbol)
    if df1h.empty or df15m.empty:
        return None
    m5 = load_metrics_5m(symbol)
    if m5.empty:
        return None
    tvr15 = tvr_15m_from_5m(m5)
    df15m = df15m.join(tvr15, how="left")
    # ⚠️join 이 인덱스 해상도를 조용히 업캐스트할 수 있어(ms/us/ns 혼재 함정, 다수 선례 확인) 재통일.
    df15m.index = df15m.index.as_unit("ns")
    df1h.index = df1h.index.as_unit("ns")

    # 시간외 갭 마스킹: 인덱스 간격이 15m 를 초과하면 그 시점의 tvr 을 이후 계산에서 배제
    idx = df15m.index
    gap_min = idx.to_series().diff().dt.total_seconds() / 60.0
    gap_too_large = (gap_min > 15.0 + 1e-6).to_numpy()

    tvr = df15m["tvr"].where(~gap_too_large)

    win_norm = TVR_NORMALIZE_WINDOW_DAYS * BARS_PER_DAY_15M

    # --- 롤링 표준편차(레벨의 산포, 스펙 핵심 통계량) ---
    tvr_std = tvr.rolling(TVR_WINDOW, min_periods=TVR_WINDOW).std(ddof=0)
    tvr_std_pctile = rolling_pctile_of_last(tvr_std, win_norm)

    # --- 방향확인용: 24봉 롤링 평균(>1.0 상승우세 / <1.0 하락우세) ---
    tvr_mean_window = tvr.rolling(TVR_WINDOW, min_periods=TVR_WINDOW).mean()

    # --- 동어반복/전제일관성 점검용 지표들 ---
    close = df15m["close"]
    logret = np.log(close / close.shift(1))
    rv15 = logret.rolling(TVR_WINDOW, min_periods=TVR_WINDOW).std(ddof=0)
    rv15_pctile = rolling_pctile_of_last(rv15, win_norm)

    mid, upper, lower = ind.bollinger_bands(close, period=20, num_std=2.0)
    bbw = (upper - lower) / mid
    bbw_pctile = rolling_pctile_of_last(bbw, win_norm)

    # OI 변화 표준편차(oi-change-rolling-stdev 계열 프록시) — join 안 된 별도 OI 로더 필요
    oi_change_stdev = _load_oi_change_stdev(symbol, df15m.index, gap_too_large)

    qv = df15m["quote_volume"]
    vol_z = pd.Series(rolling_zscore(qv.to_numpy(float), win_norm), index=df15m.index)

    high, low = df15m["high"], df15m["low"]
    donch_upper = high.shift(1).rolling(DONCHIAN_LB).max()
    donch_lower = low.shift(1).rolling(DONCHIAN_LB).min()

    atr14_15m = ind.atr(df15m, 14)
    atr20_15m = _atr_sma(df15m, ATR_STOP_LB)
    atr14_1h = ind.atr(df1h, 14)

    return Signals(df1h=df1h, df15m=df15m, tvr=tvr, tvr_std=tvr_std,
                   tvr_std_pctile=tvr_std_pctile, tvr_mean_window=tvr_mean_window,
                   rv15=rv15, rv15_pctile=rv15_pctile, bbw=bbw, bbw_pctile=bbw_pctile,
                   oi_change_stdev=oi_change_stdev, vol_z=vol_z,
                   donch_upper=donch_upper, donch_lower=donch_lower,
                   atr14_15m=atr14_15m, atr20_15m=atr20_15m, atr14_1h=atr14_1h,
                   tvr_5m_count=df15m["tvr_5m_count"], tvr_raw_nan=df15m["tvr_raw_nan"])


@lru_cache(maxsize=None)
def load_metrics_5m_oi(symbol: str) -> pd.DataFrame:
    """OI 필드(sum_open_interest)도 별도 로드 — 동어반복 점검(oi-change-rolling-stdev 대조)용."""
    files = sorted(METRICS_DIR.glob(f"{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "sum_open_interest"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out.index = out.index.as_unit("ns")
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    out.loc[out["sum_open_interest"] <= 0, "sum_open_interest"] = np.nan
    return out


def _load_oi_change_stdev(symbol: str, target_index: pd.DatetimeIndex,
                          gap_too_large: np.ndarray) -> pd.Series:
    m5oi = load_metrics_5m_oi(symbol)
    if m5oi.empty:
        return pd.Series(np.nan, index=target_index)
    s = m5oi["sum_open_interest"]
    last = s.resample("15min", label="left", closed="left").last()
    filled = last.ffill()
    filled.index = filled.index.as_unit("ns")
    filled = filled.reindex(target_index)
    oi_delta = filled.diff()
    oi_delta = oi_delta.where(~gap_too_large)
    return oi_delta.rolling(TVR_WINDOW, min_periods=TVR_WINDOW).std(ddof=0)


def with_donchian_lb(sig: Signals, lb: int) -> Signals:
    high, low = sig.df15m["high"], sig.df15m["low"]
    donch_upper = high.shift(1).rolling(lb).max()
    donch_lower = low.shift(1).rolling(lb).min()
    return replace(sig, donch_upper=donch_upper, donch_lower=donch_lower)


def with_tvr_window(sig: Signals, window: int) -> Signals:
    """tvr_window 스윕용: tvr_std·tvr_mean_window 재계산 불가피(윈도우 자체가 바뀜)."""
    tvr = sig.tvr
    win_norm = TVR_NORMALIZE_WINDOW_DAYS * BARS_PER_DAY_15M
    tvr_std = tvr.rolling(window, min_periods=window).std(ddof=0)
    tvr_std_pctile = rolling_pctile_of_last(tvr_std, win_norm)
    tvr_mean_window = tvr.rolling(window, min_periods=window).mean()
    return replace(sig, tvr_std=tvr_std, tvr_std_pctile=tvr_std_pctile,
                   tvr_mean_window=tvr_mean_window)
