"""OI 변화 부호전환빈도(Zero-Crossing Rate) 확신도 게이트 + Donchian 브레이크아웃 — 공통 로더/신호.

스펙: research/strategies/oi-delta-zero-crossing-rate-conviction-gate-breakout-scalp.md

⚠️데이터 캐시 재사용: klines(15m/1h)·metrics(5분 OI) 원본은 동일 세션 스크래치패드의
`oiar1hl/data`(OI AR(1) 반감기 백테스트가 받아둔 캐시)를 그대로 읽기 전용으로 재사용한다.
재사용 타당성 확인: ①동일 유니버스(BTC/ETH/BNB/SOL/XRP/DOGE/ADA) ②동일 TF(15m·1h) ③동일 필드
(open/high/low/close/volume/quote_volume, sum_open_interest) ④기간 커버 확인
(klines 2021-09~2026-06 58개월, metrics 종목당 1673~1764일 — IS 2022-01-01+워밍업, OOS
2026-06-30 까지 전부 포함). 파일 수정 없이 순수 로드만 하므로 오염 위험 없음.
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
    "OIZCR_REPO_SRC",
    "/home/user/study/.claude/worktrees/agent-afb4a326731d5754a/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "OIZCR_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oizcr"))
# 원본 klines·metrics 는 oiar1hl 캐시를 읽기 전용 재사용(위 docstring 근거)
CACHE_DATA = Path(os.environ.get(
    "OIZCR_CACHE_DATA",
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
ZCR_WINDOW = 24              # 15m*24 = 6시간
ZCR_MAX_TRANSITIONS = ZCR_WINDOW - 1  # 23(창 안 연속쌍 수)
ZCR_PCTILE_TH = 30.0         # 백분위(0~100), 낮을수록 확신
ZCR_NORMALIZE_WINDOW_DAYS = 30
DONCHIAN_LB = 20
ATR_TRAIL_MULT = 1.5         # ATR(1h,14) 트레일링
ATR_STOP_MULT = 1.0          # ATR(15m,20) 고정 SL(신호봉 기준)
ATR_STOP_LB = 20             # SL 용 ATR 은 "최근 20봉(15m) ATR"(14 아님 — 스펙 문언 그대로)
MAX_HOLD_BARS = 24           # 15m*24 = 6시간
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
    """metrics 5분 원본 로드. create_time 은 날짜 문자열 → 명시적 format 파싱(us/ms 단위사고 회피)."""
    files = sorted(METRICS_DIR.glob(f"{symbol}-metrics-*.csv"))
    parts = []
    for p in files:
        try:
            df = pd.read_csv(p)
        except Exception:  # noqa: BLE001
            continue
        if df.empty or "create_time" not in df.columns:
            continue
        parts.append(df[["create_time", "symbol", "sum_open_interest"]])
    if not parts:
        return pd.DataFrame()
    out = pd.concat(parts, ignore_index=True)
    out["dt"] = pd.to_datetime(out["create_time"], format="%Y-%m-%d %H:%M:%S", utc=True,
                               errors="coerce")
    out = out.dropna(subset=["dt"])
    out = out.sort_values("dt").drop_duplicates("dt").set_index("dt")
    out.index = out.index.as_unit("ns")  # ns 명시 통일(klines 인덱스와 join 시 오정렬 방지)
    out["sum_open_interest"] = pd.to_numeric(out["sum_open_interest"], errors="coerce")
    # ⚠️0-fill 결측 placeholder(선례 확인): 실제 OI 는 0이 될 수 없음 → 명시적 NaN 처리.
    out.loc[out["sum_open_interest"] <= 0, "sum_open_interest"] = np.nan
    return out


def oi_15m_from_5m(m5: pd.DataFrame) -> pd.DataFrame:
    """5분 OI → 15m봉 마감시점 값(resample('15min').last(), 빈 bin 은 NaN → 명시적 ffill).
    스펙 문언 "5분 OI 스냅샷을 15분봉에 합산해 얻는 순ΔOI"는, OI 가 누적 레벨(스톡)이라
    3개 5분 구간의 순증감을 합산한 값이 텔레스코핑으로 (봉 종료시 레벨 - 직전봉 종료시 레벨)과
    수학적으로 동일함(중간 5분 스냅샷 결측이 없다면) — 따라서 15m봉 말미 레벨의 diff()로 구현.
    ffill 여부·5분 표본수를 별도 컬럼으로 남겨 품질 추적."""
    if m5.empty:
        return pd.DataFrame()
    s = m5["sum_open_interest"]
    last = s.resample("15min", label="left", closed="left").last()
    cnt = s.resample("15min", label="left", closed="left").count()
    filled = last.ffill()
    out = pd.DataFrame({"oi": filled, "oi_raw_nan": last.isna(), "oi_5m_count": cnt})
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
    — "zcr_pctile = 롤링 30일 창 기준 백분위"와 정확히 일치(causal, 미래 데이터 미사용).

    ⚠️자체발견: rolling(window).rank(pct=True) 는 min_periods 미지정 시 기본값이 window 전체(완전
    충족)라, 입력 x(zcr)에 든 짧은(24~64봉) 고립 NaN 블립 하나가 그 뒤 30일(2880봉) 전체를
    NaN 으로 전염시킨다(실측: BTC 기준 24~64봉 블립 7~9개가 각각 2900~5800봉짜리 결측 구간을
    만들어 전체 이력의 18.9% 가 소실). 블립 원인은 OI 5분 스냅샷 결측 구간에서 ffill 로 델타가
    0 이 돼 crossing 판정이 미정의(sign==0)로 잠깐 끊기는 것 — 실제 시장 신호가 아니라 데이터
    가용성 아티팩트. min_periods 를 window*min_frac(기본 90%)로 완화해 고립 블립이 최대 30일을
    통째로 잠식하지 않게 한다(반대로 min_frac=1.0 이면 위 전염 재현 확인됨 — 아래 이력 참고)."""
    min_periods = max(1, int(window * min_frac))
    return x.rolling(window, min_periods=min_periods).rank(pct=True) * 100.0


# ------------------------------------------------------------------ 신호 구축

@dataclass
class Signals:
    df1h: pd.DataFrame        # 1h klines
    df15m: pd.DataFrame       # 15m klines + oi
    oi_delta: pd.Series        # 15m 순ΔOI(레벨차, 부호 판정용)
    zcr: pd.Series             # zero-crossing rate(0~1), 24봉 롤링
    zcr_pctile: pd.Series      # zcr 의 30일 롤링 백분위(낮을수록 확신)
    oi_cumsum_window: pd.Series  # 24봉(zcr_window) 롤링 순ΔOI 누적합(방향 확인용)
    vol_z: pd.Series           # 대조군③(신호원 교체): quote_volume 의 30일 롤링 z-score
    vol_z_pctile: pd.Series    # vol_z 의 30일 롤링 백분위(zcr 과 동일 메커니즘)
    oi_change_stdev: pd.Series  # 동어반복 점검용: oi_delta 의 24봉 롤링 표준편차(산포 크기)
    atr_roc: pd.Series          # 동어반복 점검용: 15m ROC(1봉, %)
    rv15: pd.Series             # 동어반복 점검용: 15m 실현변동성(24봉 롤링 std of 로그수익률)
    donch_upper: pd.Series      # 20봉 Donchian 상단(자기 제외, shift(1) 적용됨)
    donch_lower: pd.Series      # 20봉 Donchian 하단(자기 제외)
    atr14_15m: pd.Series        # ATR(14, 15m) — 동어반복 대조·참고용
    atr20_15m: pd.Series        # ATR(20, 15m) — SL 용(스펙 문언 "최근 20봉 ATR")
    atr14_1h: pd.Series          # ATR(14, 1h) — TP 트레일링용
    oi_5m_count: pd.Series
    oi_raw_nan: pd.Series


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
    oi15 = oi_15m_from_5m(m5)
    df15m = df15m.join(oi15, how="left")
    # ⚠️join 이 인덱스 해상도를 조용히 업캐스트할 수 있어(ms/us/ns 혼재 함정, 다수 선례 확인) 재통일.
    df15m.index = df15m.index.as_unit("ns")
    df1h.index = df1h.index.as_unit("ns")

    # 시간외 갭 마스킹: 인덱스 간격이 15m 를 초과하면 그 시점의 OI 변화를 NaN 처리
    idx = df15m.index
    gap_min = idx.to_series().diff().dt.total_seconds() / 60.0
    gap_too_large = (gap_min > 15.0 + 1e-6).to_numpy()

    oi_delta = df15m["oi"].diff()
    oi_delta = oi_delta.where(~gap_too_large)

    win_norm = ZCR_NORMALIZE_WINDOW_DAYS * BARS_PER_DAY_15M

    # --- zero-crossing rate ---
    sign = np.sign(oi_delta.to_numpy(float))
    sign_prev = np.roll(sign, 1)
    sign_prev[0] = np.nan
    # 0(무변동 — ffill 평탄구간)은 "전환" 판정에서 제외(부호 자체가 미정의라 전환으로 세지 않음).
    valid_pair = np.isfinite(sign) & np.isfinite(sign_prev) & (sign != 0) & (sign_prev != 0)
    crossing = np.where(valid_pair, (sign != sign_prev).astype(float), np.nan)
    crossing_s = pd.Series(crossing, index=df15m.index)
    zcr = crossing_s.rolling(ZCR_MAX_TRANSITIONS, min_periods=ZCR_MAX_TRANSITIONS).mean()
    zcr_pctile = rolling_pctile_of_last(zcr, win_norm)

    oi_cumsum_window = oi_delta.rolling(ZCR_WINDOW, min_periods=ZCR_WINDOW).sum()

    # --- 대조군③(신호원 교체): 거래대금(quote_volume) z-score ---
    qv = df15m["quote_volume"]
    vol_z = pd.Series(rolling_zscore(qv.to_numpy(float), win_norm), index=df15m.index)
    vol_z_pctile = rolling_pctile_of_last(vol_z, win_norm)

    # --- 동어반복 점검용 기존 지표들 ---
    oi_change_stdev = oi_delta.rolling(ZCR_WINDOW, min_periods=ZCR_WINDOW).std(ddof=0)
    close = df15m["close"]
    atr_roc = close.pct_change(1) * 100.0
    logret = np.log(close / close.shift(1))
    rv15 = logret.rolling(ZCR_WINDOW, min_periods=ZCR_WINDOW).std(ddof=0)

    high, low = df15m["high"], df15m["low"]
    donch_upper = high.shift(1).rolling(DONCHIAN_LB).max()
    donch_lower = low.shift(1).rolling(DONCHIAN_LB).min()

    atr14_15m = ind.atr(df15m, 14)
    atr20_15m = _atr_sma(df15m, ATR_STOP_LB)
    atr14_1h = ind.atr(df1h, 14)

    return Signals(df1h=df1h, df15m=df15m, oi_delta=oi_delta, zcr=zcr, zcr_pctile=zcr_pctile,
                   oi_cumsum_window=oi_cumsum_window, vol_z=vol_z, vol_z_pctile=vol_z_pctile,
                   oi_change_stdev=oi_change_stdev, atr_roc=atr_roc, rv15=rv15,
                   donch_upper=donch_upper, donch_lower=donch_lower,
                   atr14_15m=atr14_15m, atr20_15m=atr20_15m, atr14_1h=atr14_1h,
                   oi_5m_count=df15m["oi_5m_count"], oi_raw_nan=df15m["oi_raw_nan"])


def with_donchian_lb(sig: Signals, lb: int) -> Signals:
    high, low = sig.df15m["high"], sig.df15m["low"]
    donch_upper = high.shift(1).rolling(lb).max()
    donch_lower = low.shift(1).rolling(lb).min()
    return replace(sig, donch_upper=donch_upper, donch_lower=donch_lower)


def with_zcr_window(symbol: str, sig: Signals, window: int) -> Signals:
    """zcr_window 스윕용: crossing 지표는 재계산 불가피(윈도우 자체가 바뀜)하므로 재빌드."""
    df15m = sig.df15m
    oi_delta = sig.oi_delta
    win_norm = ZCR_NORMALIZE_WINDOW_DAYS * BARS_PER_DAY_15M
    max_trans = window - 1
    sign = np.sign(oi_delta.to_numpy(float))
    sign_prev = np.roll(sign, 1)
    sign_prev[0] = np.nan
    valid_pair = np.isfinite(sign) & np.isfinite(sign_prev) & (sign != 0) & (sign_prev != 0)
    crossing = np.where(valid_pair, (sign != sign_prev).astype(float), np.nan)
    crossing_s = pd.Series(crossing, index=df15m.index)
    zcr = crossing_s.rolling(max_trans, min_periods=max_trans).mean()
    zcr_pctile = rolling_pctile_of_last(zcr, win_norm)
    oi_cumsum_window = oi_delta.rolling(window, min_periods=window).sum()
    return replace(sig, zcr=zcr, zcr_pctile=zcr_pctile, oi_cumsum_window=oi_cumsum_window)
