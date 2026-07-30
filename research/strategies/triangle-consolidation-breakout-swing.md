# [스윙] 삼각수렴(Ascending/Descending Triangle) 브레이크아웃

- **출처**: https://altfins.com/knowledge-base/how-to-trade-descending-triangle-pattern-crypto-chart-pattern/ (altFINS, 크립토 전용 차트패턴 플랫폼 — WebFetch로 원문 확인, "altFINS edge: Backtests show ~67% success rate" 문구 확인) / 규칙 정의 보강: https://algotradinglib.com/en/pedia/t/triangle_consolidation_patterns.html (Algorithmic Trading Library, 시스템적 삼각형 탐지 기준) / https://www.quantifiedstrategies.com/breakout-triangle-strategy/ (원문은 봇차단으로 WebFetch 실패, 규칙 텍스트는 WebSearch 스니펫으로만 참고: "close outside the triangle plus a two-day high-low filter, stop on opposite side, target = pattern base projected, time exit 30 bars")
- **참여지표**: - (altFINS는 크립토 전문 차트패턴 분석 플랫폼으로 정량 SNS 지표는 비공개)
- **백테스트 근거**: **부분 확인, 신뢰도 낮음**. altFINS 페이지에 "Backtests show ~67% success rate"라는 문구가 **WebFetch로 직접 확인됨**. 단, **어느 코인·기간·타임프레임·정확한 진입조건에서 나온 수치인지 원문에 명시되지 않음**(방법론 불투명) → "정량 수치는 확인되나 방법론 미공개"로 정직히 표기, 마케팅성 주장일 가능성 배제 못 함. QuantifiedStrategies의 30봉 시간청산·2일 고저 필터 규칙은 WebSearch 스니펫 수준 확인(원문 봇차단으로 100% 대조 못 함, 대상 자산군도 주식일 가능성 있어 크립토 특정 아님) → 규칙은 참고만 하고 아래 스펙은 독자적으로 재구성.
- **타임프레임**: 4h~1d 패턴 형성(스윙 고/저 포인트 최소 3개 필요하므로 저TF는 패턴 신뢰도 낮음), 돌파 확인은 4h.
- **시장/대상**: BTC·ETH·시총상위 알트 무기한

## 진입 규칙
- **패턴 탐지(객관적 규칙화, algotradinglib 기준 재구성)**:
  - 최근 lookback_bars(예 40봉, 4h 기준 약 6.7일) 내에서 스윙 고점(직전·직후 봉보다 높은 국지 고점) 최소 3개, 스윙 저점 최소 2개 탐지.
  - **상승삼각형(Ascending, 강세)**: 스윙 고점들이 거의 수평(고점 간 편차 ≤ resistance_tol 1.0%) **AND** 스윙 저점들이 선형회귀 기울기 양수(저점 절상, 우상향).
  - **하락삼각형(Descending, 약세)**: 스윙 저점들이 거의 수평(편차 ≤ support_tol 1.0%) **AND** 스윙 고점들이 선형회귀 기울기 음수(고점 절하, 우하향).
  - 수렴 확인: 고점선-저점선 간 폭이 패턴 초입 대비 convergence_ratio(예 50%) 이하로 축소.
- 롱: 상승삼각형 확정 상태에서 종가가 수평 저항선을 **상향 돌파** **AND** 돌파봉 거래량 ≥ 최근 20봉 평균 × 1.5 → 돌파 확정봉 종가 진입.
- 숏: 하락삼각형 확정 상태에서 종가가 수평 지지선을 **하향 이탈** **AND** 거래량 조건 동일 → 진입.

## 청산 규칙
- 익절: 목표가 = 돌파가 ± 삼각형 높이(패턴 초입 최대폭, "measured move" 투영, 원문 QuantifiedStrategies 스니펫 근거).
- 손절: 손절가 = 삼각형 내부 반대편 최근 스윙 포인트(롱은 돌파 직전 마지막 저점, 숏은 마지막 고점).
- 시간 청산: 돌파 후 max_hold_bars(예 30봉, 4h 기준 5일) 내 목표가 미도달 시 그 시점 시장가 청산(원문 QuantifiedStrategies의 "30봉 시간청산" 스니펫 채택, 크립토 4h로 환산은 [설계 판단]).

## 파라미터
- lookback_bars=40 (범위 25~60, 4h 기준)
- resistance_tol / support_tol=1.0% (범위 0.5~2.0%)
- convergence_ratio=50% (범위 40~65%)
- vol_confirm_mult=1.5 (범위 1.2~2.0)
- max_hold_bars=30 (범위 20~45, 4h 기준)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 스윙 고/저 탐지(국지 극값), 선형회귀 기울기(저점군·고점군), 거래량 이동평균.
- 주의: **바이낸스 REST 캔들+거래량만으로 구현 가능**. 다만 패턴 탐지 자체가 규칙 기반이라도 **파라미터(허용오차·수렴비율)에 민감**해 과최적화 위험이 다른 지표형 전략보다 큼 — 그리드서치 시 in-sample/out-of-sample 분리 필수. "삼각형이 실제로는 무작위 잡음일 확률"을 통계적으로 걸러내는 로직(예: 최소 3터치 요구)이 이미 스펙에 포함돼 있으나, 완전한 오탐 방지는 어려움.

## 스카우트 메모
- 강점: 기존 188개 스펙에 "삼각형(triangle)" 패턴이 전무 — 지오메트릭 패턴 계열 중 신규. 상승/하락삼각형은 크립토 커뮤니티에서 매우 흔히 회자되는 개념이라 재현성·직관성이 높음.
- 의심점: altFINS의 "67% 성공률" 주장은 방법론이 공개되지 않아 **마케팅성 수치일 가능성 배제 못 함**(스크리닝 규칙 1의 "정량 인용 환각 금지" 원칙에 따라 신뢰도를 명확히 낮춰 표기함). 패턴 탐지 로직 자체가 파라미터에 민감해 과최적화 위험이 다른 전략 대비 큼.
- 우리 단타 슬리브와의 관계: 독립적(신규 패턴 계열, 기존 브레이크아웃 스캘프와 시간축·메커니즘 다름). 백테스트 우선순위는 중간(참여지표 약함, 개념은 명확).
