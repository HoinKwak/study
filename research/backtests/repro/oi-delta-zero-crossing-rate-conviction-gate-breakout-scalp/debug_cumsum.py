import pandas as pd
import numpy as np
import common
import run_lookahead_check as rlc

symbol = "ADAUSDT"
cutoff = rlc.CUTS[symbol]
full = common.build_signals(symbol)
trunc = rlc.build_truncated(symbol, cutoff)
common_idx = trunc["df15m"].index
fs = full.oi_cumsum_window.reindex(common_idx)
ts = trunc["oi_cumsum_window"].reindex(common_idx)
diff = (fs - ts).abs()
both_finite = fs.notna() & ts.notna()
d2 = diff[both_finite]
print("max diff loc:", d2.idxmax(), d2.max())
idxmax = d2.idxmax()
pos = common_idx.get_loc(idxmax)
print("position in trunc index:", pos, "of", len(common_idx))
print("full value:", fs.loc[idxmax], "trunc value:", ts.loc[idxmax])
# show surrounding oi values
print(full.df15m['oi'].reindex(common_idx).iloc[pos-3:pos+3])
print(trunc['df15m']['oi'].iloc[pos-3:pos+3])
# how many rows have nonzero diff
nz = d2[d2 > 1e-6]
print("count nonzero diff rows:", len(nz), "out of", len(d2))
print(nz.tail(10))
