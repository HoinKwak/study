"""신호 구축(z_window=200 기본) — sigs.pkl 저장."""
import pickle
import sys

import common

if __name__ == "__main__":
    z_window = int(sys.argv[1]) if len(sys.argv) > 1 else 200
    sigs = {s: common.build_signals(s, z_window=z_window) for s in common.SYMBOLS}
    out = common.SP / f"sigs_{z_window}.pkl"
    with open(out, "wb") as f:
        pickle.dump(sigs, f)
    print("saved", out)
    for s, sig in sigs.items():
        print(s, len(sig.df15m))
