# [스윙] Elder Impulse System 트래픽라이트 필터+브레이크아웃

- **출처**: Alexander Elder 원안("Come Into My Trading Room", 2002). TradingView "Indicator: Elder Impulse
  System" by LazyBear — https://www.tradingview.com/script/oCbEFfpg-Indicator-Elder-Impulse-System/
  (WebFetch 확인) / StockCharts ChartSchool 공식 해설 —
  https://chartschool.stockcharts.com/table-of-contents/chart-analysis/chart-types/elder-impulse-system /
  크립토 적용 실무 가이드: coinpedia "A Easy Guide to the Elder Impulse System in Crypto Trading"
  https://coinpedia.org/traders/a-easy-guide-to-the-elder-impulse-system-in-crypto-trading/
- **참여지표**: TradingView "Indicator: Elder Impulse System"(LazyBear) 조회수 **108,452** /
  즐겨찾기(boosts) **6,100** (WebFetch 확인) — 본 라운드 발굴 후보 중 참여지표 최고치. LazyBear는
  TradingView 초창기부터 활동한 검증된 지표 제작자(다수 인용 스크립트 보유).
- **백테스트 근거**: 없음(참여지표 + 고전 이론 기반). 정량 수치 원문 미확인.
- **타임프레임**: 1d 임펄스 판정(상위TF, Elder 원칙 "적용TF의 약 5배") / 4h 진입 트리거.
- **시장/대상**: BTC·ETH·상위 알트 무기한.

## 진입 규칙
- **임펄스 색상 판정**(1d 및 4h 각각 계산): `EMA13` 방향(`EMA13[t] > EMA13[t-1]` = 상승)과
  `MACD Histogram(12,26,9)` 방향(`Hist[t] > Hist[t-1]` = 상승)을 함께 본다.
  - **초록(불리시 임펄스)**: EMA13 상승 **AND** MACD 히스토그램 상승 → 매수만 허용(신규 숏 금지).
  - **빨강(베어리시 임펄스)**: EMA13 하락 **AND** MACD 히스토그램 하락 → 매도만 허용(신규 롱 금지).
  - **파랑(중립)**: 둘의 방향이 엇갈림 → 신규 진입 금지.
- **상위TF 필터**: 1d 임펄스가 초록이 아니면(빨강·파랑) 4h 롱 진입 금지. 1d가 빨강이 아니면 4h 숏 금지
  (coinpedia 실전 팁: "일봉이 베어리시면 1시간봉 초록 신호를 잡지 말라"는 원칙을 4h/1d로 근사 적용).
- 롱: 1d 임펄스=초록 **AND** 4h 임펄스가 (파랑 또는 빨강)에서 **초록으로 전환된 후 연속 2봉째** 초록 유지
  + 4h 종가가 직전 20봉 고점 상향 돌파(임펄스 필터로 걸러진 브레이크아웃).
- 숏: 대칭 조건(1d=빨강, 4h 빨강 연속 2봉 + 20봉 저점 하향 돌파).

## 청산 규칙
- 익절: 없음(추세추종형) — ATR(14,4h) × 3.0 트레일링 스톱으로 이익 보호.
- 손절: 진입가 대비 ATR(14,4h) × 1.8.
- 시간/조건 청산: 4h 임펄스가 보유방향과 반대색(초록 포지션 중 빨강 전환, 그 반대도 동일)으로 바뀌면 즉시
  전량 청산. 파랑(중립) 전환 시에는 절반 청산 후 트레일.

## 파라미터
- impulse_ema=13 (표준, 고정 권장)
- macd_fast=12 / macd_slow=26 / macd_signal=9 (표준, 고정 권장)
- higher_tf=1d / entry_tf=4h (Elder 5배율 근사)
- confirm_bars=2 (초록/빨강 연속 확인 봉수, 범위 1~3)
- breakout_lookback=20 (4h, 범위 15~30)
- atr_mult_sl=1.8 / atr_mult_trail=3.0

## 코딩 난이도 / 데이터 요구
- 필요한 지표: EMA(13), MACD(12,26,9) 히스토그램, 롤링 고저(브레이크아웃), ATR. **4h/1d OHLCV로 완전히
  구현 가능**, 추가 데이터 불필요.
- 난이도: 낮음(전부 표준 지표 조합, 룩업 로직만 정확히 구현하면 됨).
- 주의: 오더북·틱 데이터 불필요.

## 스카우트 메모
- 강점: 발굴 후보 중 **참여지표(조회수 10만+)가 가장 높고**, 규칙이 "두 지표의 방향 일치"라는 매우
  명확한 이진 필터라 코딩·재현이 쉬움. 오늘 지적된 "단일 지표 크로스" 문제를 원천적으로 피하는 구조
  — 트렌드(EMA13 기울기)와 모멘텀(MACD 히스토그램 기울기)이 **동시에** 같은 방향이어야만 진입 허용하는
  다중조건 스태킹이 지표 자체에 내장돼 있음. 기존 `macd-rsi-200sma-trend-filter-swing`(MACD+RSI+200SMA
  조합)과는 확인 지표 조합이 다르고(RSI 대신 EMA기울기), 기존 `elder-triple-screen-multi-timeframe-swing`
  (오실레이터 눌림목 진입, Force Index 사용)과도 트리거 방식이 다름(바 컬러 필터 + 브레이크아웃).
- 의심점: 브레이크아웃 트리거(20봉 고저 돌파) 자체는 우리 기존 돈치안/터틀 계열과 겹치는 요소 —
  차별점은 "임펄스 필터로 거른다"는 게이팅 로직에 있으므로, 백테스트 시 **임펄스 필터 유무(A/B)**를
  반드시 비교해 필터의 실제 기여도를 확인해야 함(필터가 무의미하면 그냥 돈치안 돌파와 동일해짐).
- 우리 슬리브와의 관계: 기존 중기 슬리브(슈퍼트렌드+볼린저 눌림목)와 방향은 유사(추세추종)하나 트리거
  메커니즘이 완전히 다름(이진 색상 필터+브레이크아웃 vs 밴드 눌림목 평균회귀) — 보완재로 유망, 구현
  난이도가 낮아 **백테스트 우선순위 1순위 추천**.
