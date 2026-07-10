from crypto_trader.connectors.universe import _filter_rows


def test_filter_rows_basic():
    rows = [
        {"symbol": "BTCUSDT", "quoteVolume": "500000000"},
        {"symbol": "ETHUSDT", "quoteVolume": "200000000"},
        {"symbol": "DOGEUSDT", "quoteVolume": "50000000"},   # 임계 미달
        {"symbol": "USDCUSDT", "quoteVolume": "900000000"},  # 스테이블 제외
        {"symbol": "USD1USDT", "quoteVolume": "300000000"},  # 스테이블 제외
        {"symbol": "BTCUPUSDT", "quoteVolume": "300000000"}, # 레버리지 토큰 제외
        {"symbol": "ETHBTC", "quoteVolume": "999999999"},    # 비 USDT 제외
        {"symbol": "SOLUSDT", "quoteVolume": "bad"},         # 파싱 불가 제외
    ]
    out = _filter_rows(rows, 100e6)
    symbols = [s for s, _ in out]
    assert symbols == ["BTC/USDT", "ETH/USDT"]  # 거래대금 내림차순
    assert out[0][1] == 500000000.0


def test_filter_rows_sorted_desc():
    rows = [
        {"symbol": "AUSDT", "quoteVolume": "150000000"},
        {"symbol": "BUSDT", "quoteVolume": "450000000"},
        {"symbol": "CUSDT", "quoteVolume": "250000000"},
    ]
    out = _filter_rows(rows, 100e6)
    assert [s for s, _ in out] == ["B/USDT", "C/USDT", "A/USDT"]
