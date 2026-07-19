# [스윙] MAMA/FAMA 적응형 이동평균(Ehlers MESA) 크로스오버

- **출처**: 지표 원작 John Ehlers("Rocket Science for Traders", 2001) — 사이클 적응형 이동평균.
  TradingView "MESA Adaptive Moving Average" by DasanC —
  https://www.tradingview.com/script/7a5LLYCx-MESA-Adaptive-Moving-Average/ (WebFetch 확인) /
  전략 개념: FMZ "Ehlers MESA Adaptive Moving Average Trading Strategy" https://www.fmz.com/lang/en/strategy/428090 ,
  TrendSpider "What is the MESA Adaptive Moving Average (MAMA)" https://trendspider.com/learning-center/what-is-the-mesa-adaptive-moving-average-mama/ ,
  Phemex Academy 해설 https://phemex.com/academy/what-is-mesa-adaptive-moving-average
- **참여지표**: TradingView "MESA Adaptive Moving Average"(DasanC) 조회수 **32,877** /
  즐겨찾기(boosts) **10,221** (WebFetch 확인) — Ehlers 지표 중 "가장 잘 알려진 것 중 하나"로 소개됨.
- **백테스트 근거**: 없음(참여지표 + 지표 표준 공식 기반). FMZ·TrendSpider 등은 "MAMA/FAMA 교차가 휩쏘에
  거의 자유롭다"는 정성적 서술만 제공, 정량 수치는 확인되지 않음.
- **타임프레임**: 4h~1d.
- **시장/대상**: BTC·ETH·상위 알트 무기한.

## 진입 규칙
- **MAMA/FAMA**: 힐베르트 변환(Hilbert Transform Discriminator)으로 가격의 지배 사이클(dominant cycle)
  위상 변화율을 추정, 이를 바탕으로 적응형 스무딩 계수(alpha)를 `FastLimit`과 `SlowLimit` 사이에서
  동적으로 조절해 `MAMA`(적응형 EMA)를 산출. `FAMA`는 `MAMA`에 다시 (약 절반 계수의) 스무딩을 적용한 후행선.
  표준 파라미터(TA-Lib·Ehlers 원 코드 통용값): `FastLimit=0.5, SlowLimit=0.05`.
  **[구현 시 참고]**: 정확한 힐베르트 변환 기반 공식은 표준 공개 알고리즘(Ehlers 원 코드/TA-Lib MAMA 함수)을
  그대로 이식해야 하며, 본 스펙은 그 표준 공식의 존재와 파라미터 관례만 확인했고 코드 자체는 구현 단계에서
  레퍼런스 구현(TA-Lib 등) 대조 검증 필요.
- 롱: `MAMA`가 `FAMA`를 상향 돌파(골든크로스) + **ADX(14, 4h) ≥ 20**(추세 강도 확인 — 오늘 검증에서 지적된
  "단순 크로스 단독 신호"의 엣지 부재 위험을 줄이기 위한 다중조건 스태킹).
- 숏: `MAMA`가 `FAMA`를 하향 돌파(데드크로스) + ADX(14, 4h) ≥ 20.
- (선택) 1d 종가가 1d EMA50 대비 같은 방향일 때만 진입(상위TF 정렬 필터).

## 청산 규칙
- 익절: 없음(추세추종 — FAMA를 트레일링 스톱 대용으로 사용, 가격이 FAMA를 재차 반대로 이탈하면 청산).
- 손절: 진입가 대비 ATR(14, 4h) × 2.0.
- 시간/조건 청산: 반대 크로스 발생 또는 ADX(14, 4h)가 15 아래로 하락(추세 소멸)하면 청산.

## 파라미터
- fast_limit=0.5 (표준값, 범위 0.3~0.7)
- slow_limit=0.05 (표준값, 범위 0.03~0.08)
- adx_min=20 (범위 15~25)
- adx_exit=15
- atr_mult_sl=2.0
- higher_tf_ema=50 (1d, 선택 필터)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: MAMA/FAMA(힐베르트 변환 기반, 종가만 필요), ADX, ATR, EMA. **4h/1d OHLCV로 계산 가능.**
- 난이도: **상**(힐베르트 변환 기반 적응형 지표는 이동평균류 중 구현이 까다로운 편 — TA-Lib에 `MAMA` 함수가
  내장돼 있으면(파이썬 `talib.MAMA`) 재이식 리스크를 크게 줄일 수 있음, 있는지 확인 후 활용 권장).
- 주의: 오더북·틱 데이터 불필요.

## 스카우트 메모
- 강점: 기존 85개 스펙에 Ehlers 계열 적응형 지표(MAMA/FAMA, KAMA는 있으나 힐베르트 변환 기반은 없음)가
  없어 구조적으로 신선함. 사이클 적응형이라 이동평균 지연(lag) 문제를 완화한다는 설계 철학이 EMA/SMA 크로스
  계열과 근본적으로 다름.
- 의심점: 구현 난이도가 가장 높은 후보 — TA-Lib 미사용 시 직접 이식 버그 위험 크고, 정량 백테스트 근거가
  전무해 참여지표만으로 채택. ADX 필터를 걸어도 "이동평균 교차" 계열이라는 근본 한계는 여전(오늘 검증에서
  단일 지표 크로스가 대부분 실패한 점 감안 시 기대치는 낮게 잡아야 함).
- 우리 슬리브와의 관계: 기존 EMA 9/21 크로스, 슈퍼트렌드와 메커니즘이 유사(이동평균 교차 기반 추세추종)하나
  적응형 스무딩이라는 점에서 차별화 — **구현 난이도 대비 신규성 이점이 크지 않을 수 있어 백테스트 우선순위는
  낮게 권장**.
