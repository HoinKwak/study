"""파라미터 민감도 스윕 — phi_pctile_th·donchian_lb·atr_trail_mult·max_hold_bars·ema_slope_th."""
import pickle
import sys

sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiar1hl")
import common
import engine
import stats_utils as su
from crypto_trader.config import get_settings
from crypto_trader.risk import RiskManager

settings = get_settings()
risk = RiskManager(settings)

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)

variants = []
for th in [0.60, 0.67, 0.75, 0.80]:
    variants.append(("phi_pctile_th", th, dict(phi_pctile_th=th), None))
for lb in [15, 20, 30]:
    variants.append(("donchian_lb", lb, {}, lb))   # 4번째 값=Donchian lb 오버라이드(신호 재계산 필요)
for tm in [1.4, 1.8, 2.2]:
    variants.append(("atr_trail_mult", tm, dict(atr_trail_mult=tm), None))
for mh in [12, 24, 36]:
    variants.append(("max_hold_bars", mh, dict(max_hold_bars=mh), None))
for es in [0.0, 0.3, 0.5, 0.8]:
    variants.append(("ema_slope_th", es, dict(ema_slope_th=es, use_ema_confirm=(es > 0 or es == 0.0)), None))
variants.append(("no_ema_confirm", 0, dict(use_ema_confirm=False), None))

print(f"{'축':16s} {'값':>8s}  {'OOS n':>6s}  {'PF(R)':>7s}  {'mean(R)':>8s}  {'t':>7s}")
for axis, val, kw, donch_lb_override in variants:
    cfg = engine.RunConfig(gate="phi_hi", fee_on=True, **kw)
    if donch_lb_override is not None:
        use_sigs = {s: common.with_donchian_lb(sig, donch_lb_override) for s, sig in sigs.items()}
    else:
        use_sigs = sigs
    trades = engine.run_all(use_sigs, cfg)
    all_trades = [t for lst in trades.values() for t in lst]
    df = su.trades_df(all_trades)
    _, oos_df, _ = su.split_is_oos(df)
    t, p, n = su.t_stat(oos_df)
    mean_r = oos_df["r"].mean() if len(oos_df) else float("nan")
    print(f"{axis:16s} {str(val):>8s}  {n:6d}  {su.pf_r(oos_df):7.3f}  {mean_r:+8.4f}  {t:+7.3f}")
