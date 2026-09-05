import pickle
import common

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)
sig = sigs["BTCUSDT"]
df = sig.df15m
print("oi first valid:", df["oi"].first_valid_index())
print("oi NaN count total:", df["oi"].isna().sum())
oi_delta = sig.oi_delta
print("oi_delta first valid:", oi_delta.first_valid_index())
print("oi_delta NaN count:", oi_delta.isna().sum())
na = oi_delta.isna()
idx = df.index
run_start = None
runs = []
for i, v in enumerate(na.to_numpy()):
    if v and run_start is None:
        run_start = i
    if not v and run_start is not None:
        runs.append((run_start, i - 1))
        run_start = None
if run_start is not None:
    runs.append((run_start, len(na) - 1))
runs2 = [(idx[a], idx[b], b - a + 1) for a, b in runs]
runs2.sort(key=lambda x: -x[2])
print("top 10 longest NaN runs in oi_delta:")
for r in runs2[:10]:
    print(r)
print("zcr_pctile first valid:", sig.zcr_pctile.first_valid_index())
