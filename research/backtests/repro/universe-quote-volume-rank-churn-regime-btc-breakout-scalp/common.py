"""유니버스 거래대금 순위 리셔플 강도(Rank Churn) 레짐 게이트 + BTC 15m Donchian 브레이크아웃
— 공통 데이터 로더 + 지표 계산.

스펙: research/strategies/universe-quote-volume-rank-churn-regime-btc-breakout-scalp.md

⚠️유니버스 스코프: 스펙 원문은 바이낸스 전체 유니버스(60~100종목)의 순위표를 요구하나, 이 백테스트
프레임워크의 표준 유니버스(BTC/ETH/BNB/SOL/XRP/DOGE/ADA 7종목, 다른 다수 유니버스 계열 스펙
— HHI·순위이동모멘텀 — 도 동일하게 이 7종목 프록시를 씀)를 신호원으로 쓴다. 매매는 BTC 단독.
n=7 로 순위 churn 을 재는 것은 실제 60~100종목보다 훨씬 거친 이산 통계량(가능한 rank_churn 값이
{0, 2/7, 4/7, ...} 처럼 제한적)이라는 한계를 리포트에 명시한다.
"""
from __future__ import annotations

import bisect
import os
import sys
from collections import deque
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

_repo_src = os.environ.get(
    "RANKCHURN_REPO_SRC",
    str(Path(__file__).resolve().parents[4] / "src"))
sys.path.insert(0, _repo_src)

from crypto_trader.signals import indicators as ind  # noqa: E402

SP = Path(os.environ.get(
    "RANKCHURN_SCRATCH",
    "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/rankchurn"))
DATA = SP / "data"

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]
TRADE_SYMBOL = "BTCUSDT"

# 확장 유니버스(보조/진단용, n=35) — n=7 프록시의 rank_churn 이산성(§본문 참고) 진단 후 채택.
# 2022-01~2026-07 전 구간 55/55 월 완전 커버리지 확인된 심볼만 포함(MATIC/EOS/VET 등 결측 제외).
EXT_ALT_SYMBOLS = ["LTCUSDT", "LINKUSDT", "TRXUSDT", "DOTUSDT", "AVAXUSDT", "UNIUSDT", "ATOMUSDT",
                   "ETCUSDT", "FILUSDT", "NEARUSDT", "ALGOUSDT", "ICPUSDT", "FTMUSDT", "XLMUSDT",
                   "THETAUSDT", "EGLDUSDT", "XTZUSDT", "ZECUSDT", "DASHUSDT", "WAVESUSDT",
                   "ONEUSDT", "HBARUSDT", "KSMUSDT", "RUNEUSDT", "SANDUSDT", "MANAUSDT",
                   "GRTUSDT", "AAVEUSDT"]
EXT_SYMBOLS = SYMBOLS + EXT_ALT_SYMBOLS  # n=35

_SUBDIR_MAP = {s: "klines1h" for s in SYMBOLS}
_SUBDIR_MAP.update({s: "klines1h_ext" for s in EXT_ALT_SYMBOLS})

IS_START = pd.Timestamp("2022-01-01", tz="UTC")
IS_END = pd.Timestamp("2024-06-30 23:59:59", tz="UTC")
OOS_START = pd.Timestamp("2024-07-01", tz="UTC")
OOS_END = pd.Timestamp("2026-06-30 23:59:59", tz="UTC")

TAKER_FEE = 0.0005
SLIPPAGE = 0.0002
ROUNDTRIP_COST = (TAKER_FEE + SLIPPAGE) * 2  # 0.14%

_KLINE_COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
               "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore"]


# ------------------------------------------------------------------ 로더

def _load_klines(symbol: str, tf: str, subdir: str) -> pd.DataFrame:
    files = sorted(DATA.glob(f"{subdir}/{symbol}-{tf}-*.csv"))
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
    # ns 명시(unit="ms") — pandas 3.x 의 조용한 us 업캐스트 회피
    out["dt"] = pd.to_datetime(out["open_time"], unit="ms", utc=True).astype("datetime64[ns, UTC]")
    out = out.drop_duplicates("dt").sort_values("dt").set_index("dt")
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        out[c] = out[c].astype(float)
    return out[["open", "high", "low", "close", "volume", "quote_volume"]]


@lru_cache(maxsize=None)
def load_klines_1h(symbol: str, subdir: str = "klines1h") -> pd.DataFrame:
    return _load_klines(symbol, "1h", subdir)


@lru_cache(maxsize=None)
def load_klines_15m(symbol: str) -> pd.DataFrame:
    return _load_klines(symbol, "15m", "klines15m")


# ------------------------------------------------------------------ 순위 churn 계산

def build_universe_hourly_volume(symbols: list[str] = SYMBOLS) -> pd.DataFrame:
    """symbol -> 트레일링 24h(24개 1h 봉 합) quote_volume, 공통 시간축(outer join)."""
    cols = {}
    for sym in symbols:
        df = load_klines_1h(sym, _SUBDIR_MAP.get(sym, "klines1h"))
        if df.empty:
            continue
        qv24 = df["quote_volume"].rolling(24, min_periods=24).sum()
        cols[sym] = qv24
    out = pd.DataFrame(cols).sort_index()
    return out


def compute_rank_churn(vol24: pd.DataFrame) -> pd.Series:
    """rank_churn(t) = mean(|rank_i(t) - rank_i(t-24h)|), rank 1=거래대금 최대.
    24h 전과 비교하려면 인덱스가 연속 1h 라야 하므로 24개 봉 shift 로 근사(결측 없다는 전제,
    결측 있으면 자동 NaN 전파)."""
    rank = vol24.rank(axis=1, method="average", ascending=False)
    churn = rank.diff(24).abs().mean(axis=1)
    return churn


def rolling_percentile_rank(x: np.ndarray, window: int) -> np.ndarray:
    """x[i] 가 [i-window+1, i] 구간(window개)에서 차지하는 백분위(0~100). 창에 NaN 있으면 NaN."""
    n = len(x)
    out = np.full(n, np.nan)
    buf: deque[float] = deque()
    sorted_win: list[float] = []
    nan_ct = 0
    for i in range(n):
        v = x[i]
        buf.append(v)
        is_nan = not np.isfinite(v)
        if is_nan:
            nan_ct += 1
        else:
            bisect.insort(sorted_win, v)
        if len(buf) > window:
            old = buf.popleft()
            if not np.isfinite(old):
                nan_ct -= 1
            else:
                idx = bisect.bisect_left(sorted_win, old)
                sorted_win.pop(idx)
        if len(buf) == window and nan_ct == 0:
            idx = bisect.bisect_right(sorted_win, v)
            out[i] = idx / window * 100.0
    return out


def build_regime_1h(pctile_window_days: int = 60, symbols: list[str] = SYMBOLS) -> pd.DataFrame:
    """1h 인덱스(각 봉의 open_time) 기준 rank_churn / churn_pctile 계산.
    반환 df: index=1h open_time, columns=[rank_churn, churn_pctile, vol24_std_mean]
    ⚠️ '알려지는 시점'은 이 봉이 마감되는 open_time+1h 다 — 이 df 는 아직 shift 전(원시)이고,
    15m 신호에 병합할 때 known_at=index+1h 로 별도 처리한다(engine.py 참고, 룩어헤드 방지)."""
    vol24 = build_universe_hourly_volume(symbols)
    churn = compute_rank_churn(vol24)
    pctile_window_bars = pctile_window_days * 24
    pctile_arr = rolling_percentile_rank(churn.to_numpy(float), pctile_window_bars)
    pctile = pd.Series(pctile_arr, index=churn.index)
    # 동어반복 점검용: 유니버스 전체 24h거래대금 std(횡단면), realized vol, HHI 근사
    vol24_std = vol24.std(axis=1)
    vol24_mean = vol24.mean(axis=1)
    hhi = ((vol24.div(vol24.sum(axis=1), axis=0)) ** 2).sum(axis=1)  # 0(균등)~1(독점)
    out = pd.DataFrame({
        "rank_churn": churn,
        "churn_pctile": pctile,
        "vol24_std": vol24_std,
        "vol24_mean": vol24_mean,
        "hhi": hhi,
    })
    return out


# ------------------------------------------------------------------ BTC 15m 지표

def donchian(df: pd.DataFrame, period: int) -> tuple[np.ndarray, np.ndarray]:
    """직전(shift 1봉) period봉 고점/저점(현재봉 미포함, 룩어헤드 방지)."""
    hi = df["high"].rolling(period).max().shift(1).to_numpy(float)
    lo = df["low"].rolling(period).min().shift(1).to_numpy(float)
    return hi, lo


@dataclass
class BtcSignals:
    df15: pd.DataFrame
    don_hi: np.ndarray
    don_lo: np.ndarray
    atr14: pd.Series
    body_frac_atr: pd.Series   # |close-open| / ATR14


def build_btc_signals(donchian_period: int = 20) -> BtcSignals:
    df15 = load_klines_15m(TRADE_SYMBOL)
    don_hi, don_lo = donchian(df15, donchian_period)
    atr14 = ind.atr(df15, 14)
    body = (df15["close"] - df15["open"]).abs()
    body_frac_atr = body / atr14.replace(0.0, np.nan)
    return BtcSignals(df15=df15, don_hi=don_hi, don_lo=don_lo, atr14=atr14,
                      body_frac_atr=body_frac_atr)


def known_at_shifted(regime_1h: pd.DataFrame) -> pd.DataFrame:
    """1h 레짐 df 의 index(open_time)를 +1h 해 '이 값이 알려지는 시점'으로 재색인.
    (봉 t 의 값은 t+1h 에 확정·공표됨)"""
    out = regime_1h.copy()
    out.index = out.index + pd.Timedelta(hours=1)
    return out


def align_regime_to_15m(df15: pd.DataFrame, regime_1h: pd.DataFrame) -> pd.DataFrame:
    """15m 각 봉의 종가시각(open_time+15m, ns 명시)에 '그 시점까지 알려진' 가장 최근 1h
    레짐 값을 backward merge_asof 로 붙인다(룩어헤드 방지: 미확정 1h 봉 참조 불가)."""
    known = known_at_shifted(regime_1h).sort_index()
    close_times = (df15.index + pd.Timedelta(minutes=15)).astype("datetime64[ns, UTC]")
    left = pd.DataFrame({"close_time": close_times, "bar_time": df15.index})
    right = known.reset_index().rename(columns={known.index.name or "index": "close_time"})
    merged = pd.merge_asof(left, right, on="close_time", direction="backward")
    merged = merged.set_index("bar_time")
    return merged.drop(columns=["close_time"])
