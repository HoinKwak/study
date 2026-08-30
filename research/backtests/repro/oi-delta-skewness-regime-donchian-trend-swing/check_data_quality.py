import sys
sys.path.insert(0, "/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oiskew")
import common
import pandas as pd

print(f"{'symbol':10s} {'5m_rows':>9s} {'empty4h_pct':>12s} {'toptrader_nan_pct':>18s} {'oi_nan_frac':>12s}")
for sym in common.SYMBOLS:
    m5 = common.load_metrics_5m(sym)
    oi4h = common.oi_4h_from_5m(m5)
    empty_pct = (oi4h['oi_5m_count'] == 0).mean() * 100
    tt_nan = m5['sum_toptrader_long_short_ratio'].isna().mean() * 100
    # sum_toptrader may be empty string not nan after read_csv -> check
    tt_nan2 = (m5['sum_toptrader_long_short_ratio'].astype(str).isin(['', 'nan'])).mean() * 100
    oi_nan = oi4h['oi'].isna().mean() * 100
    print(f"{sym:10s} {len(m5):9d} {empty_pct:11.3f}% {tt_nan2:17.3f}% {oi_nan:11.3f}%")
