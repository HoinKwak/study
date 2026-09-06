"""룩어헤드 점검 — 데이터 뒷부분을 잘라도(절단) 절단 이전 구간의 신호가 완전히 동일해야 한다.

apen_pctile 은 롤링 90일 백분위(과거만 사용) + settlement->bar 매핑이 backward asof, EMA/ATR/ADX
는 전부 후행지표라 이론상 절단에 불변이어야 한다. BTC ETHUSDT 두 심볼로 확인.
"""
from __future__ import annotations

import json

import pandas as pd

from events import build_universe, detect_signals


def main() -> dict:
    full_uni = build_universe()
    full_sig = {}
    for sym, frame in full_uni["universe"].items():
        full_sig[sym] = detect_signals(frame, pullback_lookback=full_uni["pullback_lookback"])

    # 절단: BTC 펀딩 parquet 을 임시로 cutoff 이전까지만 남기고, klines_4h CSV 파일도 cutoff
    # 이후 월 파일을 임시 폴더에서 제외한 사본으로 build_universe 재실행.
    import shutil
    import tempfile
    from pathlib import Path
    import pandas as pd

    HERE = Path(__file__).resolve().parent
    cutoff = pd.Timestamp("2025-01-01", tz="UTC")

    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        (tmp / "klines_4h").mkdir(parents=True)
        for f in (HERE / "data" / "klines_4h").glob("*.csv"):
            # 파일명의 YYYY-MM 이 cutoff 이후 월이면 제외
            parts = f.stem.split("-")
            ym = f"{parts[-2]}-{parts[-1]}"
            if pd.Period(ym, freq="M").start_time.tz_localize("UTC") <= cutoff:
                shutil.copy(f, tmp / "klines_4h" / f.name)
        funding = pd.read_parquet(HERE / "data" / "BTCUSDT_fundingRate.parquet")
        funding = funding[pd.to_datetime(funding["calc_time"], unit="ms", utc=True) <= cutoff + pd.Timedelta(days=5)]
        funding.to_parquet(tmp / "BTCUSDT_fundingRate.parquet")

        # common.DATA 를 임시로 가리키게 하고 재실행
        import common
        import signals
        import events as ev_mod
        orig_data = common.DATA
        common.DATA = tmp
        try:
            trunc_uni = build_universe()
            trunc_sig = {}
            for sym, frame in trunc_uni["universe"].items():
                trunc_sig[sym] = detect_signals(frame, pullback_lookback=trunc_uni["pullback_lookback"])
        finally:
            common.DATA = orig_data

    out = {}
    check_end = cutoff - pd.Timedelta(days=10)  # 절단 경계 근처 워밍업 오염 여유
    for sym in ["BTCUSDT", "ETHUSDT"]:
        f_full = full_sig[sym]
        f_trunc = trunc_sig[sym]
        f_full_pre = f_full[f_full["signal_time"] <= check_end]
        f_trunc_pre = f_trunc[f_trunc["signal_time"] <= check_end]
        merged = f_full_pre.merge(f_trunc_pre, on=["signal_time", "direction"], how="outer",
                                   suffixes=("_full", "_trunc"), indicator=True)
        mismatch = (merged["_merge"] != "both").sum()
        atr_diff = (merged["atr_entry_full"] - merged["atr_entry_trunc"]).abs().max() if len(merged) else 0.0
        out[sym] = {"n_full_pre": len(f_full_pre), "n_trunc_pre": len(f_trunc_pre),
                    "n_mismatch": int(mismatch), "max_atr_diff": float(atr_diff) if pd.notna(atr_diff) else None}
    print(json.dumps(out, indent=2, default=float))
    return out


if __name__ == "__main__":
    main()
