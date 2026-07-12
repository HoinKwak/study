# [단타] CVD(누적 테이커 매수/매도 델타) 다이버전스 스캘핑

- **출처**: https://www.coinglass.com/learn/cvd-en (CoinGlass, 오더플로우/테이커볼륨 가이드) / https://bookmap.com/blog/how-cumulative-volume-delta-transform-your-trading-strategy / https://www.luxalgo.com/blog/cumulative-volume-delta-explained/ / 데이터 필드 근거: https://developers.binance.com/docs/derivatives/coin-margined-futures/market-data/Taker-Buy-Sell-Volume
- **참여지표**: - (정량 참여지표 미집계이나, CVD/오더플로우는 크립토 스캘핑 커뮤니티에서 매우 자주 언급되는 표준 개념 — TradingView에도 CVD 다이버전스 인디케이터 다수 존재)
- **백테스트 근거**: **없음(개념 기반)**. 아래는 바이낸스 klines 표준 응답 필드(`taker_buy_base_asset_volume`, `volume`)만으로 구현 가능하도록 **자체 규칙화**한 것 — 원문들은 CVD 다이버전스가 "매수/매도 압력 고갈"의 선행 신호라는 정성적 설명만 제공. 반드시 우리 프레임에서 먼저 검증.
- **타임프레임**: 5m 신호 / 15m 확인
- **시장/대상**: BTC·ETH 무기한 (유동성 커야 taker 비율 신호의 노이즈가 작음)

## 진입 규칙
- 지표 정의: 봉별 `delta = 2×taker_buy_base_volume − volume` (매수 우세면 양수). `CVD = 최근 cvd_lookback(예 50)봉 delta의 롤링 누적합`.
- 롱: 최근 divergence_lookback(예 20)봉 내 **가격이 저점을 갱신**했는데 **CVD는 저점을 갱신하지 못하고 더 높은 저점**을 형성(불리시 다이버전스) **AND** 확인봉(confirm_bars)이 양봉 마감 + 해당 봉 delta도 양전환
- 숏: 최근 20봉 내 **가격이 고점을 갱신**했는데 **CVD는 고점 갱신 실패**(베어리시 다이버전스) **AND** 확인봉이 음봉 마감 + delta 음전환

## 청산 규칙
- 익절: 목표 R배수(rr_ratio, 예 1.5R)
- 손절: 다이버전스 형성 구간의 가격 극단(스윙 저/고) 바로 너머
- 시간/조건 청산: 신호 후 invalidate_bars(예 10봉=50분) 내 CVD 방향전환 미확인 시 셋업 무효화(미체결 취소). 체결 후에는 CVD가 반대 방향으로 M봉 연속 유의미하게 이어질 경우 조기 청산.

## 파라미터
- cvd_lookback=50 (범위 30~80)
- divergence_lookback=20 (범위 10~30)
- confirm_bars=1~2
- rr_ratio=1.5 (범위 1.0~2.5)
- invalidate_bars=10

## 코딩 난이도 / 데이터 요구
- 필요한 지표: `taker_buy_base_asset_volume` — 바이낸스 klines REST 응답의 표준 필드(9개 필드 중 8번째). **우리 `binance_data.py`의 `klines()`는 현재 OHLCV만 파싱**하므로 이 필드를 추가로 뽑아내는 파싱 확장이 필요.
- **대안(더 간단)**: 우리 커넥터에 이미 `taker_buy_sell_ratio(symbol, period)` 메서드가 있음(`src/crypto_trader/connectors/binance_data.py:95`, `/futures/data/takerlongshortRatio` 사용, "5m"~"1d" period 지원). 이건 봉별 delta를 직접 계산할 필요 없이 **바이낸스가 이미 집계한 매수/매도 비율**을 반환 — CVD 근사치 신호로 이 기존 메서드를 우선 재사용하고, 세밀한 봉단위 delta가 필요하면 klines 파싱을 확장하는 2단계 접근 권장.
- 난이도: 낮음~중간(기존 메서드 재사용 시 낮음). 오더북 심도·개별 체결 틱 불필요 — 우리 인프라(REST)로 100% 커버.
- 주의: `taker_buy_base_asset_volume`/`takerlongshortRatio` 둘 다 **집계된 근사치**(개별 주문 방향이 아니라 시장가 매수 체결분 합계)라 진짜 틱 단위 CVD보다 해상도가 낮음. 방향성 다이버전스 판정 용도로는 충분. `takerlongshortRatio` 엔드포인트는 심볼별로 상장 초기·저유동성 알트에서 데이터가 없을 수 있음(BTC·ETH는 안정적).

## 스카우트 메모
- 강점: 우리 기존 단타(볼린저 이탈+거래량 급증+OI)는 "거래량 스파이크" 크기만 보고 매수/매도 압력의 **질(방향성)**은 반영하지 않음 — CVD는 이를 보완(같은 대량거래라도 매수우세/매도우세 구분 가능). 오더북 심도 없이 klines 필드만으로 구현 가능해 우리 인프라에 매우 친화적.
- 의심점: 백테스트 전무, "다이버전스" 판정이 본질적으로 패턴 인식이라 파라미터에 민감(과최적화 주의). taker 근사치의 노이즈로 저유동성 알트에서는 신호 품질이 떨어질 수 있음.
- 우리 단타 슬리브와의 관계: **보완재**. 완전히 다른 신호원(가격+거래량 방향성 vs 밴드이탈+절대거래량)이라 중복 낮음. 독립 전략으로도, 기존 스캘프 신호에 "CVD 방향 일치" 필터를 얹는 방식으로도 활용 가능.
