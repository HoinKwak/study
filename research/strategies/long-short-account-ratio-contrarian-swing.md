# [스윙] 롱숏 계정비율(Long/Short Account Ratio) 극단 컨트래리언

- **출처**: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Long-Short-Ratio ,
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Long-Short-Account-Ratio
  (바이낸스 공식 파생상품 마켓데이터 API 문서) / 개념 보강: https://www.ainvest.com/news/btc-perpetual-futures-long-short-ratio-contrarian-indicator-crypto-trading-2509/ ,
  https://www.coinglass.com/LongShortRatio (CoinGlass, 롱숏비율 시각화 표준 플랫폼)
- **참여지표**: 없음(정량 SNS 참여지표 미집계) — 다만 "롱숏비율 극단=컨트래리언 신호"는 CoinGlass·바이낸스 공식 데이터 페이지를 중심으로 크립토 파생 트레이딩 커뮤니티에서 매우 광범위하게 통용되는 프레임.
- **백테스트 근거**: 없음(개념 기반). 다수 2차 자료가 "70% 이상 롱 쏠림=조정 선행, 70% 이상 숏 쏠림=반등 선행" 식의 정성적 임계값만 제시 — 정량 수익률·승률 근거 없음. **채택 전 자체 백테스트 필수**.
- **타임프레임**: 4h~1d (Binance 계정비율 API의 최소 주기가 5m이나, 노이즈를 줄이려면 4h 이상 집계 권장)
- **시장/대상**: BTC·ETH 위주(계정비율 데이터가 안정적으로 잡히는 최상위 유동성 심볼)

## 진입 규칙
- 지표: 바이낸스 `globalLongShortAccountRatio`(전체 계정 롱/숏 비율) 및 `topLongShortAccountRatio`(상위 트레이더 계정 비율) — `longShortRatio = 롱계정수/숏계정수`.
- 극단 정의: ratio_lookback(예 30봉, 4h 기준 5일)의 롱숏비율 시계열에서 현재 값이 상위/하위 percentile_extreme(예 상위 10% / 하위 10%)에 위치.
- **롱(숏 쏠림 반전)**: `longShortRatio`가 극단적으로 낮음(숏 포지션 과밀, 하위 10%ile) **AND** 가격이 최근 price_lookback(예 20봉) 대비 하락 또는 횡보(추세추종이 아닌 역추세 진입이므로 급락 직후보다는 숏 누적이 장기화된 구간을 선호) **AND** 펀딩비율이 음수 또는 중립(숏이 프리미엄을 받는 상황 아님 확인, 이미 보유 중인 `funding-rate-extreme-contrarian.md`와 신호 상관관계 점검 필요) → 롱 진입.
- **숏(롱 쏠림 반전)**: `longShortRatio`가 극단적으로 높음(상위 10%ile) **AND** 최근 가격이 상승 추세 **AND** 펀딩비율 양수·상승 중(롱 과열 확인) → 숏 진입.
- **선택 필터**: `topLongShortAccountRatio`(상위 트레이더)와 `globalLongShortAccountRatio`(전체 리테일)가 **반대 방향으로 괴리**될 때(리테일은 롱 쏠림, 상위트레이더는 숏 우위 등) 신뢰도 가중 — "스마트머니 vs 리테일" 다이버전스 프레임.

## 청산 규칙
- **익절**: 롱숏비율이 중립대(percentile 40~60%ile)로 복귀 시 청산, 또는 목표 R배수(예 2R) 도달.
- **손절**: 진입 시점 가격 기준 ATR(4h, 14) × 2.0 역방향.
- **시간/조건 청산**: 진입 후 max_hold_bars(예 30봉=4h×30=5일) 내 비율이 중립 복귀하지 않으면 시간청산(쏠림이 장기화되며 추세로 굳어지는 국면 오판 방지).

## 파라미터
- ratio_lookback=30 (범위 20~60, 4h 기준)
- percentile_extreme=10 (범위 5~15, %ile)
- price_lookback=20 (범위 10~30)
- atr_stop_mult=2.0 (범위 1.5~3.0)
- rr_target=2.0 (범위 1.5~3.0)
- max_hold_bars=30 (4h 기준, 범위 20~50)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 바이낸스 파생 마켓데이터 `globalLongShortAccountRatio`, `topLongShortAccountRatio`, 펀딩비율(기보유), ATR.
- 주의: **실시간 라이브는 REST `/futures/data/globalLongShortAccountRatio` 등으로 조회 가능하나 최근 30일치만 제공**(과거 조회 불가) → **백테스트용 과거 데이터는 `data.binance.vision` 의 `data/futures/um/daily/metrics/` 일별 덤프(컬럼: `count_long_short_ratio`, `sum_toptrader_long_short_ratio` 등)를 사용**해야 함(CLAUDE.md에 정리된 fapi 지역차단 우회 경로와 동일한 소스 — 인프라 재사용 가능). 오더북·틱데이터 불필요.

## 스카우트 메모
- **강점**: 크립토 파생상품 특유의 데이터(포지셔닝 쏠림)를 활용하는 진짜 "크립토 네이티브" 전략 — 주식·외환에는 없는 엣지. 필요 데이터가 이미 CLAUDE.md에 정리된 `data.binance.vision/metrics` 덤프에 포함돼 있어 백테스트 인프라 재사용 가능.
- **의심점**: 정량 백테스트 근거 전무. "롱숏비율=포지션 수(계정 수) 기준"이라 고래 1명의 대형 포지션과 리테일 다수의 소형 포지션이 동일 가중치로 집계되는 왜곡 가능성 있음(`topLongShortAccountRatio`는 계정 수 기준, `topLongShortPositionRatio`는 포지션 규모 기준 — 후자가 더 유의미할 수 있어 파라미터 대안으로 검토). 기존 `funding-rate-extreme-contrarian.md`(펀딩비율 극단 페이드)와 **컨셉이 매우 유사**(둘 다 "쏠림=반전 선행")하여 신호 상관관계가 높을 가능성 큼 — 중복 신호 여부를 반드시 먼저 확인.
- **우리 슬리브와의 관계**: `funding-rate-extreme-contrarian.md`와의 중복 위험이 이번 후보 중 가장 큼(같은 "포지셔닝 쏠림 페이드" 카테고리, 다른 데이터 소스). 채택 시 두 신호를 **AND 결합한 복합 신호**(펀딩+계정비율 동시 극단일 때만 진입, 신호 빈도는 줄지만 확신도 상승)로 설계하는 편이 개별 전략보다 유리할 수 있음.
