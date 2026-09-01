"""룩어헤드 검증: 특정 시점 이후 데이터를 완전 삭제하고 재실행해, 안전마진 이전 트레이드가
전체실행과 완전 일치하는지 확인(5m/15m/1h 세 TF 모두 절단)."""
from __future__ import annotations
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common
import engine

SYM = "BTCUSDT"
CUTOFF = pd.Timestamp("2024-01-01", tz="UTC")
SAFETY_MARGIN_DAYS = 30


def run_full():
    common.load_klines.cache_clear()
    cfg = engine.RunConfig()
    sig = engine.build_signals(SYM, cfg)
    return engine.run_symbol(SYM, sig, cfg)


def truncate_and_run():
    # 각 TF csv 를 스크래치 사본 디렉터리에 복사한 뒤 cutoff 이후 행 삭제
    tmp_data = common.SP / "data_trunc"
    if tmp_data.exists():
        shutil.rmtree(tmp_data)
    shutil.copytree(common.DATA, tmp_data)
    import os
    orig_data = common.DATA
    common.DATA = tmp_data
    for tf in ["5m", "15m", "1h"]:
        d = tmp_data / f"klines_{tf}"
        for f in sorted(d.glob(f"{SYM}-{tf}-*.csv")):
            df = pd.read_csv(f)
            df = df[pd.to_numeric(df["open_time"], errors="coerce").notna()]
            df["open_time"] = df["open_time"].astype("int64")
            dt = pd.to_datetime(df["open_time"], unit="ms", utc=True)
            keep = dt < CUTOFF
            if keep.all():
                continue
            df = df[keep]
            if df.empty:
                f.unlink()
            else:
                df.to_csv(f, index=False)
    common.load_klines.cache_clear()
    cfg = engine.RunConfig()
    sig = engine.build_signals(SYM, cfg)
    trades = engine.run_symbol(SYM, sig, cfg)
    common.DATA = orig_data
    common.load_klines.cache_clear()
    return trades


if __name__ == "__main__":
    full_trades = run_full()
    trunc_trades = truncate_and_run()

    safety_cut = CUTOFF - pd.Timedelta(days=SAFETY_MARGIN_DAYS)
    full_safe = [t for t in full_trades if t.entry_time < safety_cut]
    trunc_safe = [t for t in trunc_trades if t.entry_time < safety_cut]

    print(f"전체실행 안전마진 이전 트레이드: {len(full_safe)}")
    print(f"절단실행 안전마진 이전 트레이드: {len(trunc_safe)}")

    n = min(len(full_safe), len(trunc_safe))
    mismatches = 0
    for i in range(n):
        a, b = full_safe[i], trunc_safe[i]
        if (a.entry_time != b.entry_time or a.direction != b.direction or
            abs(a.entry_price - b.entry_price) > 1e-6 or
            a.reason != b.reason or a.holding_bars != b.holding_bars or
            abs(a.r_net - b.r_net) > 1e-6):
            mismatches += 1
            if mismatches <= 5:
                print(f"MISMATCH idx={i}: full={a} trunc={b}")
    print(f"비교된 트레이드={n}, 불일치={mismatches}, 개수차이={len(full_safe)-len(trunc_safe)}")
