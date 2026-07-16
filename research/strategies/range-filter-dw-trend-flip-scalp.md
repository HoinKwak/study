# [단타] Range Filter [DW] 가격범위 필터 추세전환 스캘핑

- **출처**: https://www.tradingview.com/script/lut7sBgG-Range-Filter-DW/ (TradingView, DonovanWall 원 지표, 2018-10-30 게시) /
  포뮬러 상세(2차 미러, Pine→의사코드): https://gist.github.com/comdet/948444ec95d7b4c0546c4d16c47273af
- **참여지표**: TradingView 좋아요/부스트 **6,105**, 조회수 **228,423** (WebFetch로 직접 확인). "실험적 스터디"로 소개됐지만 8년 가까이 롱런하며 파생·이식 버전 다수(ProRealCode, MT5, ThinkOrSwim 등).
- **백테스트 근거**: 없음(원 지표 페이지엔 성과 수치 미공개, 참여지표 기반 채택). 2차 미러의 EMA50/200·Bull/Bear Power 추가 필터는 **원저자(DonovanWall) 공식 버전이 아닌 파생 각색**으로 추정 — 채택 시 필터 유무 A/B 비교 필요.
- **타임프레임**: 15m~1h (원 지표는 타임프레임 무관, 국내외 파생 전략들은 인트라데이~4h에 주로 활용)
- **시장/대상**: BTC·ETH 및 유동성 상위 무기한

## 진입 규칙
- 범위(스무스 레인지) 계산: `rng_per`(샘플링 기간)=20, `rng_qty`(범위 배수)=3.5
  - `avrng = EMA(|close − close[1]|, rng_per)`
  - `smoothrng = EMA(avrng, rng_per×2−1) × rng_qty`
- 필터 라인(`filt`) 매 봉 갱신:
  - `close − smoothrng > filt[-1]` → `filt = max(filt[-1], close − smoothrng)`
  - `close + smoothrng < filt[-1]` → `filt = min(filt[-1], close + smoothrng)`
  - 그 외 → `filt = filt[-1]` (레인지 내 움직임은 무시 → 노이즈 필터링 핵심 컨셉)
- 방향 판정: `filt > filt[-1]` → 상승추세(upward), `filt < filt[-1]` → 하락추세(downward)
- 롱: `close`가 `filt`를 상향 돌파(crossover) **AND** `upward`(직전 봉 대비 filt 상승) **AND** `EMA(50) > EMA(200)` **AND** Bull Trend
- 숏: `close`가 `filt`를 하향 돌파(crossunder) **AND** `downward` **AND** `EMA(50) < EMA(200)` **AND** Bear Trend
- ⚠️ **정정(backtest-reviewer 감사)**: 초판은 EMA50/200·"Bull Power(`high−EMA13`)" 필터를 **옵션(2차자료)**으로,
  그것도 **틀린 산식(Elder Bull Power)**으로 적었으나, 스펙이 인용한 원본 소스에서는 이 필터가 **진입 필수**이며
  실제 산식은 **Bull/Bear Trend = `(close − lowest(low,50)) / atr(5)` 기반**(Elder Bull Power 아님)이다. 감사가
  원본대로 재구현하니 BTC/ETH/ADA/NEAR/1000PEPE에서 PF 1.2~1.7(OOS>1)로, "필터 없는 raw 신호 FAIL"과 결론이
  갈렸다. 정확한 필터 기준으로 재검증 진행 예정(아래 백테스트 리포트 참조).

## 청산 규칙
- **추세전환 청산**: `filt` 방향이 반전되거나 반대 크로스 발생 시 청산(지표 자체가 청산 신호 겸함).
- **손절**: 원문엔 고정 SL 없음(레인지 필터 자체가 노이즈를 흡수하므로 스톱을 좁게 잡으면 필터 취지와 상충). 우리 봇 적용 시 `진입가 ∓ smoothrng` 폭을 초기 SL로 사용 권장(원문 미명시, 리스크관리 보강 추정).
- **익절**: 고정 TP 없음, 반대 신호까지 홀드.
- **시간 청산**: 없음.

## 파라미터
- rng_per=20 (범위 14~30)
- rng_qty=3.5 (범위 2.0~4.5, 클수록 필터 강함·신호 적음)
- ema50/ema200 (옵션, 범위 각 40~60 / 150~250)
- bull_bear_power_ema=13 (옵션 필터용)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: EMA(가격변화 절대값), 캔들 종가. 옵션 필터 사용 시 EMA(50/200), Elder Bull/Bear Power(EMA13 기반).
- 주의: 오더북/틱 불필요. 전부 바이낸스 REST 캔들로 충족. `filt`의 상태유지(래칫형 업데이트) 로직만 정확히 구현하면 나머지는 표준 EMA 조합.

## 스카우트 메모
- 강점: TradingView 8년 롱런·6천+ 좋아요로 검증된 대중성, "레인지 내 움직임 무시"라는 컨셉이 명확해 노이즈 많은 크립토 단타에서 휩쏘 억제 효과 기대. 로직이 단순(EMA 몇 개 조합)해 구현 난이도 낮음.
- 의심점: 원 지표 페이지에 정량 백테스트가 전혀 없어 **순수 참여지표 기반 채택**. 2차 자료의 EMA50/200+Bull/Bear Power 필터는 원저자 공식 버전인지 불명확 — 채택 시 필터 없는 순정 버전과 A/B 비교 필수. rng_qty가 클수록 신호가 늦어 추세 초반을 놓칠 위험(레인지 필터의 태생적 지연).
- 우리 슬리브와의 관계: 보완(신규 진입 로직). 기존 볼린저 돌파+거래량+OI 단타와 달리 **거래량 필터가 없는 순수 가격 구조 기반**이라 별도 검증 가치 있음. UT Bot Alerts(ATR 트레일링)와 유사한 "가격이 적응형 라인을 돌파하면 신호" 계열이지만 산식이 ATR이 아닌 가격변화 EMA 기반이라 상관관계가 다를 가능성 — 포트폴리오 분산 관점에서 검토.
