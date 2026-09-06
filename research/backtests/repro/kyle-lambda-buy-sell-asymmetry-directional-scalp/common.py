"""매수주도 vs 매도주도 Kyle's 람다 비대칭 게이트 — 공통 로더/신호.

스펙: research/strategies/kyle-lambda-buy-sell-asymmetry-directional-scalp.md
(커밋 545408c, 2026-09-06 08:20Z 확인)

⚠️데이터 캐시 재사용: klines(15m) 원본은 동일 세션 스크래치패드의 `oiar1hl/data`(직전 OI AR(1)
반감기 백테스트가 받아둔 캐시, 569MB, 이후 여러 백테스트가 재사용한 전례 있음)를 읽기 전용으로
재사용한다. 재사용 타당성: ①동일 유니버스(BTC/ETH/BNB/SOL/XRP/DOGE/ADA) ②동일 TF(15m, `count`·
`taker_buy_volume`·`volume`·`close` 전부 표준 klines 컬럼으로 존재) ③기간 커버 2021-09~2026-06
(IS 2022-01-01+워밍업, OOS 2026-06-30까지 전부 포함). metrics(5분 OI)도 동어반복 점검③(OI-가격
탄력성과의 상관, 참고용 진단)에 한해 같은 캐시에서 읽기 전용 재사용한다. 파일 수정 없이 순수
로드만 하므로 오염 위험 없음.

⚠️본 스펙은 헤더에 "확인은 1h"라 적혀 있으나 진입/청산/파라미터 규칙 전체가 15m 데이터만 참조하고
1h는 실제로 어디에도 쓰이지 않는다(과거 OI-AR1-halflife 라운드에서 동일 패턴 발견 — "1d 확인TF
미사용" 설계판단). 본 구현은 규칙 문언 그대로 15m 단독으로 구현하고, 이 설계 공백을 리포트에
명시한다(1h는 로드하지 않음 — 필요 시 추후 로버스트니스 변형에서 causal 매핑으로 추가 가능).
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
    "KLBSA_REPO_SRC",
    "/home/user/study/.claude/worktrees/agent-a21f5cf039b647cd0/src")
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "KLBSA_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/klbsa"))
CACHE_DATA = Path(os.environ.get(
    "KLBSA_CACHE_DATA",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiar1hl/data"))
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
BARS_PER_DAY_15M = 96
LAMBDA_WINDOW_DAYS = 3
LAMBDA_WINDOW = LAMBDA_WINDOW_DAYS * BARS_PER_DAY_15M       # 288봉
MIN_SAMPLES_PER_SIDE = 50                                    # 스펙 예시값
GAP_PCTILE_WINDOW_DAYS = 20
GAP_PCTILE_WINDOW = GAP_PCTILE_WINDOW_DAYS * BARS_PER_DAY_15M  # 1920봉
GAP_HI_PCTILE = 80.0
GAP_LO_PCTILE = 20.0
SV_TRIGGER_PCTILE = 85.0
ATR_TRAIL_MULT = 1.8
ATR_STOP_MULT = 1.2
MAX_HOLD_BARS = 16

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
    for c in ["open", "high", "low", "close", "volume", "taker_buy_volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume", "taker_buy_volume"]]
    # ⚠️pandas 3.0.5 ns 통일(join/merge_asof/Timedelta 산술 오정렬 방지, 다수 선례 확인)
    out.index = out.index.as_unit("ns")
    return out


@lru_cache(maxsize=None)
def load_klines_15m(symbol: str) -> pd.DataFrame:
    return _load_klines(KLINES_15M_DIR, symbol, "15m")


@lru_cache(maxsize=None)
def load_metrics_5m_oi(symbol: str) -> pd.DataFrame:
    """OI 필드(sum_open_interest) — 동어반복 점검③(OI-가격 탄력성과의 상관, 참고 진단)용."""
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


def rolling_pctile_of_last(x: pd.Series, window: int, min_frac: float = 0.9) -> pd.Series:
    """x(t) 가 자신의 최근 window 개(과거+현재) 히스토리 내에서 차지하는 백분위 순위(0~100).
    causal(미래 데이터 미사용). ⚠️min_periods 함정(다수 선례 확인): min_periods 미지정 시 기본값이
    window 전체(완전 충족)라, 입력에 든 짧은 고립 NaN 블립 하나가 그 뒤 전체를 NaN 으로 전염시킬
    수 있다 — min_periods 를 window*min_frac(기본 90%)로 완화."""
    min_periods = max(1, int(window * min_frac))
    return x.rolling(window, min_periods=min_periods).rank(pct=True) * 100.0


def rolling_zscore(x: pd.Series, window: int) -> pd.Series:
    m = x.rolling(window).mean()
    sd = x.rolling(window).std(ddof=0)
    z = (x - m) / sd
    return z.where(sd > 1e-12)


def _masked_rolling_ols_slope(x: np.ndarray, y: np.ndarray, mask: np.ndarray, window: int,
                              min_samples: int) -> tuple[np.ndarray, np.ndarray]:
    """mask==True 인 표본만 골라 y = c + slope*x 를 window(고정 길이, 현재 봉 포함 causal) 내에서
    회귀. slope=(n*Sxy-Sx*Sy)/(n*Sxx-Sx^2). 표본수(mask 합) < min_samples 인 구간은 NaN(게이트
    미정의). 반환: (slope, n_samples)."""
    xm = pd.Series(np.where(mask, x, 0.0))
    ym = pd.Series(np.where(mask, y, 0.0))
    mk = pd.Series(mask.astype(float))
    n = mk.rolling(window, min_periods=window).sum()
    sx = xm.rolling(window, min_periods=window).sum()
    sy = ym.rolling(window, min_periods=window).sum()
    sxy = (xm * ym).rolling(window, min_periods=window).sum()
    sxx = (xm * xm).rolling(window, min_periods=window).sum()
    denom = n * sxx - sx * sx
    # denom 이 0(또는 극미)에 가까우면 수치적으로 불안정 — NaN 처리(상대 임계: sxx 규모 대비)
    denom_safe = denom.where(denom.abs() > 1e-9 * (sxx.abs() + 1.0))
    slope = (n * sxy - sx * sy) / denom_safe
    slope = slope.where(n >= min_samples)
    return slope.to_numpy(), n.to_numpy()


@dataclass
class Signals:
    df15m: pd.DataFrame
    sv: pd.Series                 # signed volume = 2*taker_buy_volume - volume
    ratio: pd.Series               # taker_buy_ratio (volume=0 인 봉은 NaN)
    buy_led: np.ndarray            # bool
    sell_led: np.ndarray           # bool
    lambda_buy: np.ndarray
    lambda_sell: np.ndarray
    n_buy: np.ndarray
    n_sell: np.ndarray
    lambda_gap: pd.Series           # lambda_sell - lambda_buy
    gap_pctile: pd.Series             # 롤링 20일 백분위
    sv3: pd.Series                     # 3봉 누적 sv
    sv3_abs_pctile: pd.Series            # |sv3| 의 롤링 20일 백분위
    lambda_all: np.ndarray                # 대조군①: 매수/매도 구분 없는 대칭 λ(동일 윈도우)
    lambda_all_pctile: pd.Series            # lambda_all 의 롤링 20일 백분위(대조군① 게이트용)
    ratio_mean_window: pd.Series              # 대조군②: taker_buy_ratio 의 lambda_window 롤링평균
    ratio_mean_pctile: pd.Series                # 그 롤링 20일 백분위(대조군② 게이트용)
    atr14: pd.Series                              # ATR(14, 15m) — TP트레일·SL 공용(스펙 문언 그대로)
    oi_change: pd.Series                            # 동어반복③ 진단용(참고, 게이트 미사용)


def build_signals(symbol: str, lambda_window: int = LAMBDA_WINDOW,
                  gap_pctile_window: int = GAP_PCTILE_WINDOW,
                  min_samples: int = MIN_SAMPLES_PER_SIDE) -> Signals | None:
    df = load_klines_15m(symbol)
    if df.empty:
        return None

    volume = df["volume"]
    taker_buy = df["taker_buy_volume"]
    close = df["close"]

    valid_bar = volume > 0
    ratio = (taker_buy / volume).where(valid_bar)
    buy_led = (valid_bar & (ratio > 0.5)).to_numpy()
    sell_led = (valid_bar & (ratio <= 0.5)).to_numpy()

    sv = 2.0 * taker_buy - volume
    delta_close = close.diff()

    sv_np = sv.to_numpy(float)
    dc_np = delta_close.to_numpy(float)

    lambda_buy, n_buy = _masked_rolling_ols_slope(sv_np, dc_np, buy_led, lambda_window, min_samples)
    lambda_sell, n_sell = _masked_rolling_ols_slope(sv_np, dc_np, sell_led, lambda_window, min_samples)
    lambda_gap = pd.Series(lambda_sell - lambda_buy, index=df.index)
    gap_pctile = rolling_pctile_of_last(lambda_gap, gap_pctile_window)

    # 대조군①: 매수/매도 구분 없는 대칭 λ(전체 봉 대상, 동일 윈도우) — 동어반복 점검①/대조군①
    all_mask = valid_bar.to_numpy()
    lambda_all, _ = _masked_rolling_ols_slope(sv_np, dc_np, all_mask, lambda_window, min_samples * 2)
    lambda_all_pctile = rolling_pctile_of_last(pd.Series(lambda_all, index=df.index), gap_pctile_window)

    # 대조군②: taker_buy_ratio 자체(레벨)의 lambda_window 롤링평균 → 백분위(동어반복 점검②)
    ratio_mean_window = ratio.rolling(lambda_window, min_periods=lambda_window).mean()
    ratio_mean_pctile = rolling_pctile_of_last(ratio_mean_window, gap_pctile_window)

    # 트리거: 3봉 누적 sv 절대값의 롤링 20일 백분위
    sv3 = sv.rolling(3, min_periods=3).sum()
    sv3_abs_pctile = rolling_pctile_of_last(sv3.abs(), gap_pctile_window)

    atr14 = ind.atr(df, 14)

    oi_change = _load_oi_change_15m(symbol, df.index)

    return Signals(df15m=df, sv=sv, ratio=ratio, buy_led=buy_led, sell_led=sell_led,
                  lambda_buy=lambda_buy, lambda_sell=lambda_sell, n_buy=n_buy, n_sell=n_sell,
                  lambda_gap=lambda_gap, gap_pctile=gap_pctile, sv3=sv3,
                  sv3_abs_pctile=sv3_abs_pctile, lambda_all=lambda_all,
                  lambda_all_pctile=lambda_all_pctile, ratio_mean_window=ratio_mean_window,
                  ratio_mean_pctile=ratio_mean_pctile, atr14=atr14, oi_change=oi_change)


def _load_oi_change_15m(symbol: str, target_index: pd.DatetimeIndex) -> pd.Series:
    m5oi = load_metrics_5m_oi(symbol)
    if m5oi.empty:
        return pd.Series(np.nan, index=target_index)
    s = m5oi["sum_open_interest"]
    last = s.resample("15min", label="left", closed="left").last()
    filled = last.ffill(limit=4)
    filled.index = filled.index.as_unit("ns")
    filled = filled.reindex(target_index)
    return filled.diff()


def with_params(sig: Signals, symbol: str, lambda_window: int | None = None,
                gap_pctile_window: int | None = None,
                min_samples: int | None = None) -> Signals:
    """스윕용: lambda_window·gap_pctile_window·min_samples 변경 시 신호 재계산 필요."""
    lw = lambda_window if lambda_window is not None else LAMBDA_WINDOW
    gw = gap_pctile_window if gap_pctile_window is not None else GAP_PCTILE_WINDOW
    ms = min_samples if min_samples is not None else MIN_SAMPLES_PER_SIDE
    return build_signals(symbol, lambda_window=lw, gap_pctile_window=gw, min_samples=ms)
