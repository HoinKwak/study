# [스윙] 차이킨 오실레이터 멀티타임프레임 제로크로스

- **출처**: https://www.quantifiedstrategies.com/chaikin-oscillator-trading-strategy/ (QuantifiedStrategies,
  백테스트 수치 출처) / https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/chaikin-oscillator
  (StockCharts, 지표 정의 원전 — Marc Chaikin)
- **참여지표**: -(백테스트 사이트 기반, 별도 조회수/추천 지표 미확인)
- **⚠️ 백테스트 근거 — 인용 오류(backtest-reviewer 감사로 정정)**: 발굴 당시 "BTC/USDT 2021~2024 4H
  제로크로스 WR48%/PF1.24, 일봉필터 시 WR59%/PF1.72, 82→38건"으로 적었으나, 감사가 인용 URL
  (quantifiedstrategies.com)을 직접 fetch해 검색한 결과 **이 수치·종목(BTC)·타임프레임(4h)이 원문에 전혀
  없음**을 확인. 원문은 **S&P500** 대상이고 제로크로스 단독은 "최적화해도 CAGR ~2.4%/20년"으로 저조.
  즉 위 정량 인용은 **스카우트 단계의 인용 환각**으로 근거 없음 → 삭제·무효 처리. (단 지표 공식
  `CO=EMA(ADL,3)−EMA(ADL,10)`은 원문과 일치.) 실제 유효성은 아래 우리 백테스트가 판정: **FAIL**.
- **타임프레임**: 4h 신호 / 1d 방향 필터(스윙 정의 4h~1d에 정확히 부합)
- **시장/대상**: BTC·ETH 우선(백테스트 근거 종목), 알트 확장 시 별도 검증 필요

## 진입 규칙
- **ADL(축적분산선)** = 누적 합 { ((close−low)−(high−close))/(high−low) × volume }.
- **Chaikin Osc** = EMA3(ADL) − EMA10(ADL).
- **일봉 필터**: 1d Chaikin Osc > 0 → 롱만 탐색. 1d Chaikin Osc < 0 → 숏만 탐색.
- 롱: 4h Chaikin Osc가 0선을 상향 돌파하는 봉의 종가에 진입(단, 1d 필터가 롱 허용 상태일 때만).
- 숏: 4h Chaikin Osc가 0선을 하향 돌파하는 봉의 종가에 진입(1d 필터가 숏 허용 상태일 때만).

## 청산 규칙
- 익절: 진입가 대비 2.0×ATR(14, 4h) 도달 시 50% 익절, 잔량은 4h Chaikin Osc가 반대 방향으로 재차 0선을
  교차할 때 청산.
- 손절: 진입가 − 1.5×ATR(14, 4h)(롱) / + 1.5×ATR(14, 4h)(숏).
- 시간 청산: 12봉(4h, 약 2일) 내 1R 미도달 시 청산.

## 파라미터
- adl_fast_ema=3, adl_slow_ema=10 (Chaikin 표준값, 고정)
- daily_filter=on/off (필터 유무 자체가 백테스트에서 핵심 차이 — 반드시 두 버전 비교)
- sl_atr_mult=1.5 (범위 1.2~2.0)
- tp_atr_mult=2.0 (범위 1.5~3.0)
- max_hold=12봉

## 코딩 난이도 / 데이터 요구
- 필요한 지표: ADL(OHLCV로 계산), EMA(3)·EMA(10) of ADL, ATR(14). 4h와 1d 두 타임프레임 동시 조회 필요(우리
  구조상 signal_df + confirm_df 패턴 그대로 재사용 가능 — mid.py/swing.py와 동일한 상위TF 확인 구조).
- 주의: **완전 REST 캔들+거래량으로 구현 가능**, 난이도 낮음. ADL은 (high==low) 구간에서 0/0 분모 처리 주의.

## 스카우트 메모
- 강점: **출처에 정량 백테스트 수치가 명시**돼 있어(48%→59% WR, PF 1.24→1.72) 스크리닝 규칙 1순위 조건을
  충족하는 몇 안 되는 후보. 멀티TF 필터로 거래빈도를 줄여 수수료 부담을 낮춘 설계가 우리 스윙 슬리브 철학과
  정확히 부합.
- 의심점: 원 출처가 3년/BTC 단일 종목 백테스트라 표본이 작고(38~82건), 수수료·슬리피지 반영 여부 불명 →
  **PF 1.72도 왕복 0.14% 반영 시 크게 낮아질 수 있어 반드시 우리 프레임워크로 먼저 재현**. 기존 CMF(Chaikin
  Money Flow)와 이름이 비슷해 혼동 주의 — **수식이 다름**(CMF는 일정 기간 화폐흐름량 합의 비율, Chaikin
  Osc는 ADL의 단기-장기 EMA 차이로 "모멘텀의 모멘텀" 성격).
- 우리 단타 슬리브와의 관계: 기존 CMF breakout-swing과 자매 지표지만 신호 발생 메커니즘이 달라 중복이라기보단
  **보완**(같은 ADL 계열이나 CMF는 레벨 기반, Chaikin Osc는 크로스오버 기반). 정량 백테스트 근거가 가장
  탄탄하므로 **1순위 백테스트 후보로 추천**.
