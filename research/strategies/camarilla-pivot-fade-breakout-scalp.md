# [단타] 카마릴라(Camarilla) 피벗 H3/L3 페이드 + H4/L4 브레이크아웃 듀얼모드 스캘핑

- **출처**: 개념/공식: https://www.litefinance.org/blog/for-beginners/trading-strategies/camarilla-pivot-points-strategy/ , https://dailyemerald.com/181022/promotedposts/camarilla-pivots-explained-intraday-levels-reversal-zones-and-simple-trade-rules/ /
  백테스트 분석: https://www.quantifiedstrategies.com/camarilla-pivot-trading-strategy/ / 실전 적용: https://medium.com/algorithmic-and-quantitative-trading/mastering-trend-trading-with-camarilla-pivot-points-477f2feec2ed
- **참여지표**: - (수십 년 사용된 고전 인트라데이 기법, TradingView에 다수 파생 스크립트 존재. 정량 참여지표 미집계)
- **백테스트 근거**: 원문들은 규칙·개념 위주이며 **정량 수익률·승률 표는 미확인**(QuantifiedStrategies 페이지는 봇차단으로 원문 미접근). "변동성 낮은 구간에선 효과 약화, 변동성 높은 구간에서 최적"이라는 정성적 결론만 확보. → **백테스트 근거는 약함** — 채택 근거는 (a) 규칙이 완전히 결정론적(공식 기반)이고 (b) 최적 타임프레임(M30~H1)이 명시적이라 **재현·코딩이 매우 쉬움**이라는 점.

## 진입 규칙
- **레벨 계산(전일/직전 세션 H/L/C 기준, UTC 00:00 앵커)**:
  - `Range = 전일 High - 전일 Low`
  - `H4 = Close + Range × 1.1/2`,  `H3 = Close + Range × 1.1/4`,  `H2 = Close + Range × 1.1/6`,  `H1 = Close + Range × 1.1/12`
  - `L1 = Close - Range × 1.1/12`, `L2 = Close - Range × 1.1/6`, `L3 = Close - Range × 1.1/4`, `L4 = Close - Range × 1.1/2`
- **모드 A: 레인지 페이드(기본, ADX<20 레짐일 때)**:
  - 숏: 가격이 **H3 상단을 터치 후 H3 아래로 되돌리는 반전봉**(윗꼬리+음봉 마감) → 숏, 목표 L3/중심선.
  - 롱: 가격이 **L3 하단 터치 후 L3 위로 되돌리는 반전봉** → 롱, 목표 H3/중심선.
- **모드 B: 브레이크아웃(ADX≥20 레짐일 때)**:
  - 롱: 종가가 **H4 상향 돌파** + 돌파봉 거래량 ≥ 직전 10봉 평균 → 롱(추세 추종, 다음 레벨 없음까지 트레일).
  - 숏: 종가가 **L4 하향 돌파** + 거래량 확인 → 숏.
- 레짐 스위치는 ADX(14) 기준(<20 페이드, ≥20 브레이크아웃)으로 모드 결정 — 기존 `regime.py` 로직 재사용 가능.

## 청산 규칙
- 모드 A(페이드): 익절 = 반대편 레벨(H3 숏 진입 시 L3 또는 중심 피벗) 도달. 손절 = H4(숏)/L4(롱) 살짝 위·아래.
- 모드 B(브레이크아웃): 익절 = ATR(14) 트레일링 스탑 또는 R:R 2:1 고정. 손절 = 돌파 레벨(H4/L4) 재이탈.
- 시간 청산: 다음 세션 앵커(UTC 00:00) 전 전량 청산, 레벨 재계산.

## 파라미터
- pivot_anchor=00:00 UTC (일간 재계산)
- camarilla_const=1.1 (고정, 표준 공식)
- signal_tf=30m~1h (범위 15m~1h, 원문 권장 M30~H1)
- adx_regime_threshold=20
- vol_confirm_mult=1.0 (브레이크아웃 시 돌파봉 거래량/평균, 범위 1.0~1.5)
- rr_breakout=2.0 (범위 1.5~3.0)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 전일 H/L/C(캔들 집계), ADX(14), 거래량 이동평균. 레벨 공식은 사칙연산뿐.
- 주의: **바이낸스 REST 일봉·인트라데이 캔들만으로 완전 충족.** 오더북/틱/청산 불필요. 구현 난이도 낮음(공식 하드코딩 + ADX 레짐 스위치).

## 스카우트 메모
- 강점: 레벨이 **완전 결정론적 공식**이라 룩어헤드·주관 개입 여지가 거의 없음(백테스트 재현성 최고 수준). 레짐(ADX)에 따라 페이드/브레이크아웃을 자동 전환하는 구조라 우리 `regime.py`와 자연스럽게 결합.
- 의심점: 정량 백테스트 수치를 원문에서 직접 확인 못함(사이트 봇차단) — **가장 약한 백테스트 근거**를 가진 후보. 채택 시 반드시 자체 백테스트로 유효성부터 확인해야 함. 기존 `prior-day-high-low-retest.md`(전일 고저 자체를 레벨로 사용)와 개념적으로 인접 — 다만 카마릴라는 Fibonacci 기반 세분화된 8개 레벨을 쓴다는 점에서 공식이 다름.
- 우리 단타 슬리브와의 관계: **보완**. 레인지장(모드 A)은 우리 봇이 약한 국면(현재 돌파 중심)을 보완할 수 있고, 브레이크아웃(모드 B)은 기존 볼린저 돌파와 유사 계열이라 중복 위험 있음 — 모드 A(페이드)만 선별 채택하는 것도 검토 가치.
