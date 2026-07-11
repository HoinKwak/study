from datetime import datetime, timedelta, timezone

from crypto_trader.scanner import detectors
from crypto_trader.scanner.events import EventStore, EventType, ScanEvent


# ------------------------------------------------------------------ detectors

def test_price_move_up_triggers():
    closes = [100.0] * 5 + [105.0]  # 마지막 봉에서 +5%
    res = detectors.price_move(closes, window=1, threshold_pct=3.0)
    assert res is not None
    pct, _ = res
    assert pct > 4.9


def test_price_move_down_triggers_negative():
    closes = [100.0, 100.0, 92.0]
    res = detectors.price_move(closes, window=1, threshold_pct=3.0)
    assert res is not None and res[0] < 0


def test_price_move_below_threshold_none():
    closes = [100.0, 100.5, 101.0]
    assert detectors.price_move(closes, window=1, threshold_pct=3.0) is None


def test_price_move_insufficient_data():
    assert detectors.price_move([100.0], window=3, threshold_pct=1.0) is None


def test_volume_spike_triggers():
    vols = [10.0] * 20 + [50.0]  # 마지막이 평균 5배
    res = detectors.volume_spike(vols, lookback=20, mult=3.0)
    assert res is not None
    ratio, _ = res
    assert ratio >= 4.9


def test_volume_spike_no_trigger_when_flat():
    vols = [10.0] * 21
    assert detectors.volume_spike(vols, lookback=20, mult=3.0) is None


def test_oi_move_surge_and_drop():
    surge = detectors.oi_move([100.0, 100.0, 110.0], lookback=1, threshold_pct=5.0)
    assert surge is not None and surge[0] > 0
    drop = detectors.oi_move([100.0, 100.0, 90.0], lookback=1, threshold_pct=5.0)
    assert drop is not None and drop[0] < 0


def test_funding_extreme():
    assert detectors.funding_extreme(0.002, 0.001) is not None
    assert detectors.funding_extreme(0.0005, 0.001) is None
    assert detectors.funding_extreme(None, 0.001) is None


# --------------------------------------------------------------------- store

def _event(symbol="BTC/USDT", etype=EventType.PUMP, ts=None):
    ts = ts or datetime.now(timezone.utc).isoformat(timespec="seconds")
    return ScanEvent(symbol=symbol, type=etype.value, value=5.0, price=100.0,
                     detail="+5%", ts=ts)


def test_store_roundtrip(tmp_path):
    store = EventStore.load(str(tmp_path))
    store.record(_event())
    store.save()

    reloaded = EventStore.load(str(tmp_path))
    assert len(reloaded.events) == 1
    assert reloaded.events[0].symbol == "BTC/USDT"


def test_store_cooldown(tmp_path):
    now = datetime(2026, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    store = EventStore.load(str(tmp_path))
    store.record(_event(ts=now.isoformat()))

    # 쿨다운(30분) 안에서는 True
    assert store.on_cooldown("BTC/USDT", EventType.PUMP, 30,
                             now + timedelta(minutes=10)) is True
    # 쿨다운 지나면 False
    assert store.on_cooldown("BTC/USDT", EventType.PUMP, 30,
                             now + timedelta(minutes=31)) is False
    # 다른 타입은 쿨다운 무관
    assert store.on_cooldown("BTC/USDT", EventType.DUMP, 30,
                             now + timedelta(minutes=10)) is False


def test_store_rolling_cap(tmp_path):
    store = EventStore.load(str(tmp_path), max_events=5)
    for i in range(10):
        store.record(_event(symbol=f"C{i}/USDT"))
    assert len(store.events) == 5
    assert store.events[-1].symbol == "C9/USDT"


def test_recent_reversed(tmp_path):
    store = EventStore.load(str(tmp_path))
    store.record(_event(symbol="A/USDT"))
    store.record(_event(symbol="B/USDT"))
    recent = store.recent(10)
    assert recent[0].symbol == "B/USDT"  # 최신이 먼저
