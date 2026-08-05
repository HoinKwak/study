# [스윙] Gator Oscillator(Bill Williams) 4국면 스퀴즈→확장 추세 진입

- **출처**: https://fbs.eu/en/analytics/guidebooks/gator-oscillator-263 (FBS 교육 가이드, WebFetch로 원문 확인) /
  https://gocharting.com/docs/charting/technical-indicator/oscillators/gator-oscillator (GoCharting 지표 정의) /
  https://www.tradingview.com/scripts/billwilliams/ (TradingView Bill Williams 지표 카테고리 — Alligator/Gator는 TradingView 내장 지표로 커뮤니티 채택도 매우 높음)
- **참여지표**: - (SNS 좋아요/조회수 미집계이나, Alligator/Gator는 TradingView·MT4/5 **내장(built-in) 지표**로 브로커·거래 교육 자료에 광범위 인용됨 — "고전 지표" 급 채택도)
- **백테스트 근거**: 없음(정성적 원문). Gator Oscillator 자체는 **추세의 존재 유무만 표시하고 방향은 표시하지 않음**이 원문에 명시("shows only the presence of a trend and not its direction") — 방향 판단은 반드시 Alligator 라인(Jaw/Teeth/Lips) 배열로 별도 수행해야 함. 4국면(Sleep/Awakening/Eating/Sated) 정의는 원문에서 확인. **정량 승률/PF 수치는 원문에 없음 — 우리 프레임워크로 최초 검증 필요.**
- **타임프레임**: 4h 신호 / 1d 확인(스퀴즈→확장 국면전환은 완만하게 형성되므로 스윙 스케일)
- **시장/대상**: BTC·ETH·주요 알트 무기한

## 진입 규칙
- **Alligator 3선(표준 정의, 원문에 shift 미기재이므로 Bill Williams 원 저서의 통용 정의 사용)**: 중앙가(HL/2) 기준
  - Jaw(악턱) = 13기간 SMMA, 8봉 전방 시프트
  - Teeth(이빨) = 8기간 SMMA, 5봉 전방 시프트
  - Lips(입술) = 5기간 SMMA, 3봉 전방 시프트
- **Gator Oscillator**: 상단 히스토그램 = |Jaw − Teeth|(직전 봉 대비 증가 시 초록, 감소 시 빨강), 하단 히스토그램 = −|Teeth − Lips|(동일 규칙).
- **4국면 판정**: (1) Sleep=상하단 모두 빨강(무추세, 진입 금지) → (2) Awakening=한쪽만 초록 전환(추세 형성 시작, 관찰) → (3) Eating=상하단 모두 초록(추세 확정, 진입 구간) → (4) Sated=한쪽이 다시 빨강(추세 소진 경고, 신규 진입 금지·기존 포지션 익절 검토).
- **롱**: Eating 국면 진입 시점(상하단 모두 초록으로 전환된 첫 봉) + Alligator 라인이 **Lips > Teeth > Jaw** 순서로 위에서부터 벌어져 있으면(라인들이 우상향 팬아웃) → 롱 진입.
- **숏**: 동일 Eating 전환 시점 + Alligator 라인이 **Jaw > Teeth > Lips**(하향 팬아웃)이면 → 숏 진입.
- (선택 필터) 진입 시 가격이 Lips(5) 라인 바깥쪽(롱은 위, 숏은 아래)에서 종가 마감할 것 — Alligator "입이 벌어진 채 가격이 입 밖에 있음" 확인.

## 청산 규칙
- 익절: Gator가 **Sated 국면 진입**(초록→빨강 전환된 첫 봉)하면 부분 익절, 완전 Sleep 재진입 시 전량 청산.
- 손절: 직전 스윙 저점(롱)/고점(숏) 또는 진입가 대비 −2.0×ATR(14).
- 시간 청산: 없음(추세 지속 국면(Eating) 동안 홀딩이 핵심이므로 순수 시간청산은 부적합). 대신 Alligator 라인이 서로 얽히기 시작하면(Jaw/Teeth/Lips 재교차) 강제 청산.

## 파라미터
- jaw_len=13/shift=8, teeth_len=8/shift=5, lips_len=5/shift=3 (Bill Williams 표준값, 통상 변경 안 함)
- gator_phase_confirm=1봉 (전환 확인 봉 수, 범위 0~2)
- atr_mult_sl=2.0 (범위 1.5~3.0)
- entry_tf=4h, confirm_tf=1d

## 코딩 난이도 / 데이터 요구
- 필요한 지표: SMMA(또는 SMA로 근사) 3개(Jaw/Teeth/Lips), 각 라인의 전방 시프트(과거 계산값을 미래로 이동 — 백테스트 시 룩어헤드 주의: 시프트된 라인은 "미래 봉 위치에 표시"될 뿐 계산 자체는 과거 데이터만 사용하므로 룩어헤드 아님, 다만 구현 시 인덱싱 실수 주의).
- 주의: **바이낸스 REST OHLC 캔들만으로 완전 충족.** 거래량/OI 불필요. 시프트 로직만 정확히 구현하면 난이도 낮음.

## 스카우트 메모
- 강점: Alligator/Gator는 TradingView·MT4/5 표준 내장지표라 재현이 매우 정확(구현 모호성 적음). 기존 볼린저·ATR류 변동성 돌파 전략들과 달리 "이동평균 3선의 벌어짐/모임" 자체를 트렌드 강도 오실레이터로 정량화하는 **완전히 다른 계산 메커니즘**(다른 240개 스펙 중 이 방식은 전무).
- 의심점: 원문 자체가 "방향은 안 알려줌"이라 명시 — 방향 판단(라인 팬아웃 순서)은 이 스카우트가 표준 Alligator 해석을 결합해 구성한 것으로 원문에 정량 검증된 결합 규칙은 아님. 시프트된 라인 사용은 실전에서 "현재 봉 시점에 보이는 라인값"과 "그 라인이 계산된 시점"이 다르므로 백테스트 구현 시 오프바이원 버그 위험 큼(주의 깊게 검증).
- 우리 슬리브와의 관계: 완전 신규 메커니즘(다른 240개와 겹치지 않음). 슈퍼트렌드류·MA크로스류와 개념적으로는 "추세 확인"이라는 목적이 비슷하지만 계산식이 판이하게 다름 — 대체재라기보다 **다각화용 신규 후보**.
