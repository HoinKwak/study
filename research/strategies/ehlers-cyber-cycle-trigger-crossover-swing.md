# [스윙] Ehlers 사이버사이클(Cyber Cycle)-트리거 크로스오버 (4h/1d)

- **출처**: John Ehlers, *Cybernetic Analysis for Stocks and Futures* (2004) 원저. 공식 재확인:
  https://www.mql5.com/en/articles/288 (MQL5, "Advanced Adaptive Indicators" — WebFetch로 수식 원문 확인) /
  참여지표용: https://www.tradingview.com/script/bJdq9y5j-Ehlers-Cyber-Cycle-Indicator-LazyBear/ (LazyBear 포팅판, WebFetch로 확인)
- **참여지표**: TradingView LazyBear 스크립트 — **차트 사용 1.3K회 / 즐겨찾기(부스트) 88 / 조회수 29,782** (WebFetch로 확인). LazyBear는 TradingView 초기 최다 팔로우 지표 제작자 중 한 명으로 신뢰도 있는 채널.
- **백테스트 근거**: **없음(참여지표+공식 검증 기반)**. Ehlers 원저·MQL5·TradingView 페이지 모두 지표 공식만 제시하고 정량 백테스트 수치(승률·PF·수익률)는 제시하지 않음. 채택 사유는 "우리 스택에 전무한 힐베르트 변환 계열 사이클 검출 지표"라는 메커니즘 신선도.
- **타임프레임**: 4h 신호 / 1d 확인 (원저는 종가 시계열이면 어떤 TF든 적용 가능한 범용 필터. 사이클 검출 특성상 단타보다 스윙 성격에 적합 — 15m/1h 적용 시 노이즈로 사이클이 왜곡될 위험, 4h 이상 권장).
- **시장/대상**: BTC·ETH·주요 알트 무기한

## 진입 규칙
- **1단계: Smooth (4바 가중평균 스무딩)**
  `Smooth[i] = (Price[i] + 2*Price[i-1] + 2*Price[i-2] + Price[i-3]) / 6`
- **2단계: Cyber Cycle (2차 재귀 대역통과 필터, MQL5 원문 수식 그대로)**
  `Cycle[i] = (1 - 0.5*alpha)^2 * (Smooth[i] - 2*Smooth[i-1] + Smooth[i-2]) + 2*(1-alpha)*Cycle[i-1] - (1-alpha)^2*Cycle[i-2]`
  - alpha=0.07 (원문 기본값, 대략 14~15봉 주기에 대응)
  - 워밍업(첫 7봉)은 `Cycle[i] = (Price[i] - 2*Price[i-1] + Price[i-2]) / 4`로 대체(원문 관례).
- **3단계: Trigger(신호선)**: `Trigger[i] = Cycle[i-1]` (1봉 지연한 사이클 값 — 별도 지표 아님, 단순 shift).
- **롱**: `Cycle`이 `Trigger`를 상향 돌파(골든크로스) — 사이클 저점에서 상승 전환.
- **숏**: `Cycle`이 `Trigger`를 하향 돌파(데드크로스) — 사이클 고점에서 하락 전환.
- **필터(원문에 없음, 스카우트 추가 — 사이클 지표는 추세장에서 휩쏘 잦다는 통설 반영)**: ADX(14, 4h) < 25(레인지/사이클성 국면)일 때만 진입 허용. 강추세(ADX≥25)에서는 사이클이 왜곡되므로 신호 무시.

## 청산 규칙
- 익절: 반대 방향 Cycle/Trigger 크로스 시 청산(자연 반전 청산, 원문 철학 — "크로스오버가 발생하면 항상 포지션을 전환/청산").
- 손절: 진입가 대비 -1.5×ATR(14, 4h).
- 시간 청산: max_hold=20봉(4h×20≈3.3일) 내 반대크로스 미발생 시 청산(사이클 지표는 국면 전환 시 신호가 사라지므로).

## 파라미터
- alpha=0.07 (범위 0.05~0.15, 값이 클수록 짧은 주기에 민감)
- adx_filter_th=25 (범위 20~30, 레인지 필터)
- atr_stop_mult=1.5 (범위 1.2~2.5)
- max_hold=20봉 (범위 10~30)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 종가만으로 Smooth/Cycle 재귀식 계산(2차 IIR 필터, 벡터화 어려워 루프 구현 필요), ADX(14).
- 주의: 재귀식이라 룩어헤드 없이 순차 계산 필수(백테스트 구현 시 벡터 연산 대신 for-loop 필요, Ehlers류 필터 공통 난점). 오더북·틱데이터 불필요, 바이낸스 REST 캔들만으로 충분.

## 스카우트 메모
- **강점**: 기존 스펙에 FRAMA·Gaussian Channel·Kalman·MAMA-FAMA 등 적응형/필터 계열은 있지만 **힐베르트 변환 기반 사이클 검출(Cyber Cycle)은 처음** — 트렌드 성분과 사이클 성분을 분리해 "추세장이 아닐 때만 반전을 잡는다"는 철학이 기존 추세추종/단순 오실레이터와 다름.
- **의심점**: 정량 백테스트 근거가 전혀 없어 순수 참여지표+메커니즘 신선도로만 채택. Ehlers 지표는 파라미터(alpha)에 민감하고 과최적화 위험이 알려져 있어(그의 후속 저작들도 계속 alpha 보정 방식을 바꿈), 반드시 워크포워드로 검증.
- **관계**: 기존 `hurst-exponent-regime-switch-swing`(추세/평균회귀 레짐 스위칭)과 목적은 유사(국면 판정)하나, 메커니즘이 전혀 다름(힐베르트 필터 vs 분산법) — 상관관계 낮은 대체 후보로 교차검증 가치 있음.
