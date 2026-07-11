from crypto_trader.connectors.binance_client import _max_notional_from_tiers
from crypto_trader.utils.timez import kst_display


# 바이낸스 레버리지 브라켓 예시(소형 알트: 30배는 tier1 $5,000 까지만)
TIERS = [
    {"maxLeverage": 30, "maxNotional": 5000},
    {"maxLeverage": 20, "maxNotional": 25000},
    {"maxLeverage": 10, "maxNotional": 100000},
    {"maxLeverage": 5, "maxNotional": 500000},
]


def test_cap_at_30x_is_tier1():
    assert _max_notional_from_tiers(TIERS, 30) == 5000


def test_cap_at_20x_allows_more():
    # 20배는 maxLeverage>=20 인 tier(30x·20x) 중 최대 = 25,000
    assert _max_notional_from_tiers(TIERS, 20) == 25000


def test_cap_at_10x_even_more():
    assert _max_notional_from_tiers(TIERS, 10) == 100000


def test_cap_reads_info_fallback():
    tiers = [{"info": {"maxLeverage": "30", "maxNotionalValue": "5000"}}]
    assert _max_notional_from_tiers(tiers, 30) == 5000


def test_cap_empty_returns_none():
    assert _max_notional_from_tiers([], 30) is None
    assert _max_notional_from_tiers(None, 30) is None


def test_cap_leverage_above_all_returns_none():
    # 요청 레버리지가 모든 tier 최대치보다 크면 수용 tier 없음
    assert _max_notional_from_tiers([{"maxLeverage": 5, "maxNotional": 1000}], 30) is None


def test_kst_display_converts_utc_to_kst():
    # 2026-07-11T03:00:00+00:00 UTC → 12:00 KST
    assert kst_display("2026-07-11T03:00:00+00:00", "%H:%M") == "12:00"


def test_kst_display_naive_assumed_utc():
    assert kst_display("2026-07-11T03:00:00", "%H:%M") == "12:00"


def test_kst_display_empty():
    assert kst_display(None) == "-"
