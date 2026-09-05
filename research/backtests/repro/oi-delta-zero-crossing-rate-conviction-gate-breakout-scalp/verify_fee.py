import pickle
import common, engine

with open(f"{common.SP}/sigs.pkl", "rb") as f:
    sigs = pickle.load(f)
cfg = engine.RunConfig(gate="zcr_lo", fee_on=True)
from crypto_trader.config import get_settings
from crypto_trader.risk import RiskManager
settings = get_settings()
risk = RiskManager(settings)
trades = engine.run_symbol("BTCUSDT", sigs["BTCUSDT"], cfg, settings, risk)
t = trades[0]
is_long = t.direction == "long"
raw = ((t.exit_price - t.entry_price) if is_long else (t.entry_price - t.exit_price)) * t.quantity
expected_pnl = raw - t.fee_entry - t.fee_exit
print("trade:", t.symbol, t.direction, "entry", t.entry_price, "exit", t.exit_price, "qty", t.quantity)
print("fee_entry", t.fee_entry, "fee_exit", t.fee_exit)
print("raw", raw, "expected_pnl(raw-fee_entry-fee_exit)", expected_pnl, "actual t.pnl", t.pnl)
assert abs(expected_pnl - t.pnl) < 1e-9, "진입수수료 미반영 버그 재발!"
print("OK: 진입+청산 수수료 모두 pnl에 반영됨 확인")
