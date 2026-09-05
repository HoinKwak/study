import pickle
import numpy as np
import common, stats_utils as su

with open(f"{common.SP}/results_main.pkl", "rb") as f:
    results = pickle.load(f)

def mdd_r(df):
    r = df.sort_values("entry_time")["r"].to_numpy()
    eq = np.cumsum(r)
    peak = np.maximum.accumulate(eq)
    dd = eq - peak
    return dd.min()

for gate in ["zcr_lo","none","zcr_hi","volz_hi","reverse"]:
    for fee_on in [True, False]:
        df = results[(gate, fee_on)]
        is_df, oos_df, full_df = su.split_is_oos(df)
        label = f"{gate}/{'net' if fee_on else 'gross'}"
        print(label, "IS_MDD(R)=%.2f OOS_MDD(R)=%.2f FULL_MDD(R)=%.2f" % (
            mdd_r(is_df) if len(is_df) else float('nan'),
            mdd_r(oos_df) if len(oos_df) else float('nan'),
            mdd_r(full_df) if len(full_df) else float('nan')))
