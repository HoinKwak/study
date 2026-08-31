"""핵심 발견 재현: 원시 결합조건(스트릭+Donchian+EMA) 발생 빈도, 종목별. 특히 스펙 기본
숏조건(streak_down)의 결합확률이 0인지 확인."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parent))
import numpy as np
import common

print(f"{'symbol':10s} {'long(streak_up)':>16s} {'short_default(streak_down)':>28s} "
     f"{'short_alt(streak_up)':>22s}")
tot_long = tot_short_def = tot_short_alt = 0
for sym in common.SYMBOLS:
    sig = common.build_signals(sym)
    close = sig.df["close"].to_numpy()
    streak_up, streak_down = sig.streak_up, sig.streak_down
    don_hi, don_lo = sig.don_hi, sig.don_lo
    ema1d = sig.ema1d.to_numpy()

    su5 = np.isfinite(streak_up) & (streak_up >= 5)
    sd5 = np.isfinite(streak_down) & (streak_down >= 5)
    brk_up = np.isfinite(don_hi) & (close > don_hi)
    brk_dn = np.isfinite(don_lo) & (close < don_lo)
    ema_up = np.isfinite(ema1d) & (close > ema1d)
    ema_dn = np.isfinite(ema1d) & (close < ema1d)

    long_n = int((su5 & brk_up & ema_up).sum())
    short_def_n = int((sd5 & brk_dn & ema_dn).sum())
    short_alt_n = int((su5 & brk_dn & ema_dn).sum())
    tot_long += long_n; tot_short_def += short_def_n; tot_short_alt += short_alt_n
    print(f"{sym:10s} {long_n:>16d} {short_def_n:>28d} {short_alt_n:>22d}")

print(f"{'합계':10s} {tot_long:>16d} {tot_short_def:>28d} {tot_short_alt:>22d}")
print(f"\n(참고) 이 원시 카운트는 '동시신호(같은 봉에서 조건 성립)' 수이며, 실제 엔진의 트레이드 수는")
print("포지션 보유 중 신규신호 무시(1개 슬롯) 로직 때문에 이보다 같거나 작다(engine.py run_all 참조).")
