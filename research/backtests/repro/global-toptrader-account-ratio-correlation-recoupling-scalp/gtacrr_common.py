"""[단타] 글로벌 vs 탑트레이더 계정비율 상관 붕괴-재동조 스캘프 — 공통 로더.

스펙: research/strategies/global-toptrader-account-ratio-correlation-recoupling-scalp.md
슬러그: global-toptrader-account-ratio-correlation-recoupling-scalp (gtacrr)

데이터:
- 가격(1h/15m): data.binance.vision 선물(UM) 월별 klines 덤프. 세션 공유 scratchpad 캐시
  (klines_cache/, 다른 라운드에서 이미 7종목 x 2021-10~2026-07 캐시됨) 재사용, 없으면 다운로드.
- 글로벌/탑트레이더 계좌수 롱숏비율(5m): data.binance.vision daily metrics 덤프. 세션 공유
  scratchpad 에 이미 캐시된 두 로더의 산출물을 병합해 재사용:
    whale_metrics_cache/<SYM>.pkl   — count_toptrader_long_short_ratio (탑트레이더)
    posflow_metrics_cache/<SYM>.pkl — count_long_short_ratio (글로벌)
  둘 다 5분 간격 create_time 기준 동일 원본에서 파생됐고 전 구간(2022-01-01~2026-07-10) 커버함을
  실측 확인(각 475,643행, 7종목 전량). outer-merge 로 두 필드를 한 DataFrame 에 합친다.
  캐시에 없는 심볼/구간이 있으면 daily zip 을 직접 받아 채운다(폴백, 이번 라운드에선 불필요할 것으로
  예상 — 실측으로 확인).
"""
from __future__ import annotations

import io
import zipfile
from pathlib import Path

import pandas as pd
import requests

SCRATCH = Path("/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad")
KLINES_CACHE_DIR = SCRATCH / "klines_cache"
WHALE_CACHE_DIR = SCRATCH / "whale_metrics_cache"
POSFLOW_CACHE_DIR = SCRATCH / "posflow_metrics_cache"
# 이 전략 전용 캐시(다른 라운드 캐시와 충돌 방지, 고유 슬러그 접두)
GTACRR_CACHE_DIR = SCRATCH / "gtacrr_metrics_cache"
GTACRR_CACHE_DIR.mkdir(parents=True, exist_ok=True)

SYMBOLS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "ADAUSDT"]

IS_START = "2022-01-01 00:00:00"
IS_END = "2024-06-30 23:59:59"
OOS_START = "2024-07-01 00:00:00"
OOS_END = "2026-06-30 23:59:59"

TAKER_FEE = 0.0005   # 편도 테이커
SLIPPAGE = 0.0002    # 편도 슬리피지

BASE_KLINES_URL = "https://data.binance.vision/data/futures/um/monthly/klines"
BASE_METRICS_URL = "https://data.binance.vision/data/futures/um/daily/metrics"

KLINES_COLS = [
    "open_time", "open", "high", "low", "close", "volume", "close_time",
    "quote_volume", "count", "taker_buy_volume", "taker_buy_quote_volume", "ignore",
]


def _month_list(start: str, end: str) -> list[tuple[int, int]]:
    s = pd.Timestamp(start)
    e = pd.Timestamp(end)
    out = []
    y, m = s.year, s.month
    while (y, m) <= (e.year, e.month):
        out.append((y, m))
        m += 1
        if m > 12:
            m = 1
            y += 1
    return out


def _fetch_kline_month(symbol: str, tf: str, year: int, month: int) -> pd.DataFrame | None:
    fname = f"{symbol}-{tf}-{year:04d}-{month:02d}"
    url = f"{BASE_KLINES_URL}/{symbol}/{tf}/{fname}.zip"
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        return None
    z = zipfile.ZipFile(io.BytesIO(r.content))
    name = z.namelist()[0]
    with z.open(name) as f:
        first = f.readline()
    header = 0 if first.startswith(b"open_time") else None
    with z.open(name) as f:
        df = pd.read_csv(f, header=header, names=KLINES_COLS if header is None else None)
    if header is None:
        df.columns = KLINES_COLS
    return df


def load_klines(symbol: str, tf: str, start: str, end: str) -> pd.DataFrame:
    """symbol(예: BTCUSDT) tf(예: 1h/15m) 의 [start,end] klines. 캐시 재사용, 없으면 다운로드+캐시."""
    months = _month_list(start, end)
    frames = []
    for y, m in months:
        cache_f = KLINES_CACHE_DIR / f"{symbol}_{tf}_{y:04d}-{m:02d}.pkl"
        if cache_f.exists():
            df = pd.read_pickle(cache_f)
        else:
            df = _fetch_kline_month(symbol, tf, y, m)
            if df is not None:
                KLINES_CACHE_DIR.mkdir(parents=True, exist_ok=True)
                df.to_pickle(cache_f)
        if df is not None and len(df):
            frames.append(df)
    if not frames:
        raise RuntimeError(f"데이터 없음: {symbol} {tf} {start}~{end}")
    full = pd.concat(frames, ignore_index=True)
    full = full.drop_duplicates(subset=["open_time"]).sort_values("open_time").reset_index(drop=True)
    # ms 정수 epoch -> ns 명시 통일 (us 업캐스트 함정 회피)
    idx = pd.to_datetime(full["open_time"].astype("int64"), unit="ms", utc=True).dt.tz_localize(None)
    idx = idx.astype("datetime64[ns]")
    out = full.set_index(pd.DatetimeIndex(idx, name="open_time"))
    for c in ["open", "high", "low", "close", "volume"]:
        out[c] = out[c].astype(float)
    out = out[["open", "high", "low", "close", "volume"]]
    mask = (out.index >= pd.Timestamp(start)) & (out.index <= pd.Timestamp(end))
    return out[mask]


def _fetch_metrics_day(symbol: str, y: int, m: int, d: int) -> pd.DataFrame | None:
    fname = f"{symbol}-metrics-{y:04d}-{m:02d}-{d:02d}"
    url = f"{BASE_METRICS_URL}/{symbol}/{fname}.zip"
    r = requests.get(url, timeout=60)
    if r.status_code != 200:
        return None
    z = zipfile.ZipFile(io.BytesIO(r.content))
    name = z.namelist()[0]
    with z.open(name) as f:
        df = pd.read_csv(f)
    return df


def _download_metrics_range(symbol: str, start: str, end: str) -> pd.DataFrame:
    """daily metrics zip 을 직접 받아 필요한 두 필드만 반환(폴백 경로)."""
    days = pd.date_range(start, end, freq="D")
    frames = []
    for d in days:
        df = _fetch_metrics_day(symbol, d.year, d.month, d.day)
        if df is not None and len(df):
            frames.append(df[["create_time", "count_toptrader_long_short_ratio",
                              "count_long_short_ratio"]])
    if not frames:
        raise RuntimeError(f"metrics 없음: {symbol} {start}~{end}")
    out = pd.concat(frames, ignore_index=True)
    out["create_time"] = pd.to_datetime(out["create_time"], utc=True).dt.tz_localize(None)
    return out


def load_ratio_metrics(symbol: str) -> pd.DataFrame:
    """5분 간격 count_long_short_ratio(글로벌) / count_toptrader_long_short_ratio(탑트레이더) 병합 로드.

    반환: DatetimeIndex(UTC naive, create_time, ns), 컬럼 [g_raw, top_raw]
    세션 공유 캐시(whale_metrics_cache + posflow_metrics_cache) outer-merge 로 재구성.
    두 캐시 어느 쪽이든 심볼 결측이면 daily zip 직접 다운로드로 폴백.
    """
    wf = WHALE_CACHE_DIR / f"{symbol}.pkl"
    pf = POSFLOW_CACHE_DIR / f"{symbol}.pkl"
    if wf.exists() and pf.exists():
        w = pd.read_pickle(wf)[["create_time", "count_toptrader_long_short_ratio"]]
        p = pd.read_pickle(pf)[["create_time", "count_long_short_ratio"]]
        w["create_time"] = pd.to_datetime(w["create_time"], utc=True).dt.tz_localize(None)
        p["create_time"] = pd.to_datetime(p["create_time"], utc=True).dt.tz_localize(None)
        m = pd.merge(w, p, on="create_time", how="outer")
    else:
        cache_f = GTACRR_CACHE_DIR / f"{symbol}_raw.pkl"
        if cache_f.exists():
            m = pd.read_pickle(cache_f)
        else:
            m = _download_metrics_range(symbol, "2022-01-01", "2026-07-05")
            m.to_pickle(cache_f)
    m = m.rename(columns={"count_toptrader_long_short_ratio": "top_raw",
                          "count_long_short_ratio": "g_raw"})
    ts = pd.to_datetime(m["create_time"]).astype("datetime64[ns]")
    out = m[["g_raw", "top_raw"]].copy()
    out.index = pd.DatetimeIndex(ts, name="create_time")
    out = out.sort_index()
    out = out[~out.index.duplicated(keep="last")]
    return out
