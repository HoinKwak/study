# [스윙] Elder Triple Screen 다중 타임프레임 시스템

- **출처**: Alexander Elder, "Trading for a Living"(1993)/"New Trading for a Living" 원 개념.
  TradingView 구현체 "Elder's Triple Screen all in one"(Biticon) —
  https://www.tradingview.com/script/NfFnvmVE-Elder-s-Triple-Screen-all-in-one/ (WebFetch 확인) /
  2차 해설: QuantifiedStrategies "Alexander Elder Trading Strategies: The Triple Screen Strategy" —
  https://www.quantifiedstrategies.com/alexander-elder-triple-screen-strategy/ (WebFetch 접근 실패,
  봇 검증 페이지만 확인됨 — 인용 안 함) / Medium 요약 —
  https://medium.com/@86adrian.popa/swing-trading-with-elders-triple-screen-a-simple-guide-e6a1236547d7
  (검색엔진 스니펫만 확인, 크립토 적용 예시 "주봉 tide + 일봉 trigger + 4H entry" 언급 — [추정] 표기)
- **참여지표**: "Elder's Triple Screen all in one" 좋아요 **12,277** / 조회수 **29,077**(WebFetch 확인).
  Elder Triple Screen은 스윙트레이딩 고전서(1990년대 베스트셀러)에 기반해 인지도가 매우 높음.
- **백테스트 근거**: 없음(참여지표 및 고전 이론 기반 채택). 정량 수치 원문 미확인.
- **타임프레임**: 1d(추세, 상위TF) / 4h(오실레이터, 눌림목 판정) / 1h(진입 트리거)
  — 지표 원문은 "적용 타임프레임의 5배인 상위TF로 추세 판정"(WebFetch 확인, 예: 4h 적용 시
  상위TF는 자동으로 약 20h 상당). 본 스펙은 크립토 스윙 인프라에 맞춰 1d/4h/1h 3단으로 근사.
- **시장/대상**: BTC·ETH 및 유동성 상위 무기한

## 진입 규칙
- **1단계(Tide, 1d 추세)**: `EMA(close, 13)` 기울기로 상위 추세 판정 — `EMA13[t] > EMA13[t-1]`이면
  상승 추세(롱만 허용), `EMA13[t] < EMA13[t-1]`이면 하락 추세(숏만 허용). (원문은 MACD 히스토그램
  방향도 병행 확인 권장 — 본 스펙은 EMA 기울기로 단순화)
- **2단계(Wave, 4h 오실레이터 눌림목)**: Force Index 사용(원문이 "능동적 트레이더용"으로 명시,
  WebFetch 확인). `FI(2) = (close − close[1]) × volume`, `FI_EMA = EMA(FI(2), 13)`.
  - 상승 추세 중: `FI_EMA`가 0 아래로 떨어졌다가(눌림목) 다시 0 위로 상향 돌파 → 롱 셋업 활성화.
  - 하락 추세 중: `FI_EMA`가 0 위로 올랐다가 다시 0 아래로 하향 돌파 → 숏 셋업 활성화.
- **3단계(Ripple, 1h 진입 트리거)**: 셋업 활성화 후, 롱은 `close`가 **직전 1h 봉 고가**를 상향
  돌파할 때 진입(원문의 "전일 고가 위 스톱 매수" 개념을 1h로 축소 적용). 숏은 직전 1h 봉 저가
  하향 돌파.

## 청산 규칙
- 익절: 1일 추세(EMA13 기울기) 반전 시 청산, 또는 고정 `2.0×ATR(14, 4h)` 트레일링.
- 손절: 진입 트리거 봉의 반대쪽 극값(롱은 트리거 저가, 숏은 트리거 고가) 또는 `1.2×ATR(14, 4h)`.
- 시간/조건 청산: 셋업 활성화 후 24h(1h봉 24개) 내 트리거 미발생 시 셋업 소멸(재대기).

## 파라미터
- trend_ema=13 (1d, 범위 8~21)
- fi_len=2, fi_smooth_ema=13 (4h Force Index)
- trigger_tf=1h, setup_ttl=24h (범위 12~48h)
- sl_atr_mult=1.2, tp_atr_mult=2.0

## 코딩 난이도 / 데이터 요구
- 필요한 지표: EMA, Force Index(가격변화×거래량), ATR — 전부 OHLCV+거래량으로 계산 가능.
  3단 타임프레임 동기화(1d/4h/1h) 로직이 필요해 구현 난이도는 중상(기존 봇의 신호TF+확인TF
  2단 구조를 3단으로 확장 필요).
- 주의: 오더북/틱 불필요. 원문 지표의 정확한 "5배 상위TF" 자동 산출 로직은 본 스펙에서
  1d/4h/1h 고정 3단으로 단순화(원 지표 완전 재현 아님).

## 스카우트 메모
- 강점: 참여지표 최상위(1.2만 좋아요)이며 고전 이론 기반이라 신뢰도 높음. 3단 타임프레임
  구조가 스윙 슬리브에 적합(수수료 절감), 상위 추세 필터로 역추세 진입을 원천 차단하는
  설계라 손익비 관리에 유리. Force Index는 기존 elder-force-index-divergence-swing.md와
  같은 지표 계열이나, 그 스펙은 다이버전스 탐지 중심이고 본 스펙은 "3단 타임프레임 추세
  필터+눌림목 셋업" 구조라 활용 방식이 다름(부분 중복 가능성 있으니 채택 시 조정 필요).
- 의심점: 정량 백테스트 전무. 원 지표의 "5배 상위TF" 정확한 산식과 3번째 레이어(엔트리
  화살표) 세부 로직은 미확인. 크립토 4h/1h TF 적용 사례("weekly tide+daily trigger+4H entry")는
  2차 자료 검색 스니펫에서만 확인돼 [추정] 표기.
- 우리 슬리브와의 관계: **부분 중복 주의**(Force Index 계열 기 보유) — 채택 시 elder-force-index
  스펙과 통합 검토 권장. 다만 다중TF 추세필터 구조 자체는 신규.
