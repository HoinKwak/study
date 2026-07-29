# [단타] VWMA(9/21) 크로스오버 + 거래량 확인 모멘텀 스캘프

- **출처**: https://trendspider.com/learning-center/what-is-the-volume-weighted-moving-average-vwma/ (TrendSpider) / https://patternswizard.com/vwma-indicator/ / https://traders.mba/support/vwma-volume-weighted-moving-average-strategy/ / https://howtotrade.com/indicators/volume-weighted-moving-average/
- **참여지표**: - (다수 교육 블로그·TradingView 위키성 자료에서 반복 소개되는 표준 지표 전략, 특정 바이럴 게시물 조회수는 확인 안 됨)
- **백테스트 근거**: 없음(원문들은 개념·규칙 설명 위주이며 구체 승률/PF 수치 제시 없음). 정량 수치 원문 미확인 — 지표 설명 기반으로 분류.
- **타임프레임**: 15m 신호 / 1h EMA50 추세 필터
- **시장/대상**: BTC·ETH·주요 알트 USDT-M 무기한

## 진입 규칙
- 지표: VWMA(9)(빠른선), VWMA(21)(느린선) — 거래량가중이동평균. SMA(vol,20)로 거래량 급증 확인.
- 롱: VWMA(9)가 VWMA(21)을 상향 돌파(골든크로스) + 신호봉 종가 > VWMA(21) + 신호봉 거래량 ≥ 1.2×SMA(vol,20) + 1h EMA(50) 위에서 마감(상위 추세 필터).
- 숏: VWMA(9)가 VWMA(21)을 하향 돌파(데드크로스) + 신호봉 종가 < VWMA(21) + 거래량 조건 동일 + 1h EMA(50) 아래.

## 청산 규칙
- 익절: 진입가 대비 1.5×ATR(14, 15m) 도달, 또는 반대 VWMA 크로스 발생 시.
- 손절: 진입가 대비 1.0×ATR(14, 15m) 역행, 또는 신호봉 저가/고가 이탈 중 더 타이트한 쪽.
- 시간/조건 청산: 1R(=SL폭) 도달 후 chandelier 방식(신고가/신저가−ATR×1.5)로 트레일링. VWMA(9)가 다시 VWMA(21)을 역크로스하면 조건 청산.

## 파라미터
- vwma_fast=9 (범위 5~13), vwma_slow=21 (범위 15~34)
- vol_lookback=20, vol_mult=1.2 (범위 1.1~1.5)
- atr_period=14, atr_mult_sl=1.0, atr_mult_tp=1.5 (범위 1.2~2.0), trail_atr_mult=1.5
- trend_filter_ema=50 (1h)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: VWMA(가격×거래량 롤링합/거래량 롤링합), ATR, EMA. 모두 바이낸스 REST 캔들+거래량으로 완전 충족.
- 주의: 오더북/틱/OI 불필요. VWMA는 표준 이동평균 계산에 거래량 가중치만 추가하면 되어 구현 난이도 낮음.

## 스카우트 메모
- 강점: 계산이 단순(EMA/SMA 수준)하고 거래량 정보를 자연스럽게 반영 — 우리 scalp.py의 "거래량 급증+볼린저 이탈" 로직과 조합 가능한 대체 트리거. 순수 크로스오버라 파라미터 튜닝 여지가 넓음.
- 의심점: 이동평균 크로스오버 계열은 후행성(lag)이 커 단타 수수료(왕복 0.14%)를 이기기 어려운 경우가 많음(우리 봇의 기존 ema-9-21-crossover.md도 유사 계열). 크로스 시점엔 이미 상당 부분 움직인 뒤일 가능성 — 되돌림 손실 위험. 백테스트로 실제 R/거래빈도 확인 필요.
- 우리 단타 슬리브와의 관계: **대체 후보**. 기존 scalp15m(볼린저 이탈+거래량+OI)과 트리거 방식이 다르지만 컨셉(거래량 확인 돌파성 모멘텀)은 유사 — 병행 시 신호 중복(같은 방향 동시 트리거) 가능성 있어 상관관계 확인 필요.
