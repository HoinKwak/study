# [단타] 액셀러레이터 오실레이터(AC) 투바 룰 스캘프

- **출처**: https://www.tradingview.com/script/yPiJgjyR-Accelerator-Oscillator-AC-Backtest/ (TradingView, HPotter, "Accelerator Oscillator (AC) Backtest" — WebFetch로 원문 확인) / 규칙 정의 보강: https://admiralmarkets.com/education/articles/forex-indicators/accelerator-oscillator (Admiral Markets, "투바 룰" 표준 정의) / https://www.quantifiedstrategies.com/bill-williams-awesome-oscillator-strategy/ (Bill Williams 원전 개념 정리)
- **참여지표**: TradingView 스크립트 페이지 **부스트 10,430 / 즐겨찾기(좋아요) 287**(WebFetch로 원문 확인) — 트레이딩뷰 인기도 지표로는 상위권.
- **백테스트 근거**: **없음(지표 정의·교육용 스크립트 기반)**. 원문 페이지 자체가 "학습 또는 모의거래용으로만 사용, 실거래 사용 금지"라고 명시 — 정량 백테스트 수치는 원문에 없음(지어내지 않음). 부스트 수치는 높지만 이는 "지표 자체의 인지도"이지 "전략의 검증된 성과"가 아님을 명확히 구분.
- **타임프레임**: 15m 신호 / 1h EMA 추세 필터
- **시장/대상**: BTC·ETH·유동성 상위 알트 무기한

## 진입 규칙
- **AO(Awesome Oscillator)**: `AO = SMA5(중간가) - SMA34(중간가)`, 중간가=(고가+저가)/2 (Bill Williams 표준).
- **AC(Accelerator Oscillator)**: `AC = AO - SMA5(AO)` — AO의 변화 속도(가속도)를 나타내는 2차 파생 지표. AO 그 자체를 쓰는 기존 보유 `awesome-oscillator-twin-peaks-saucer-scalp.md`와 **입력값은 같지만 지표·판정 로직이 다름**(AO 히스토그램 패턴 vs AC의 5기간 이동평균 대비 가속도).
- **추세 필터**: 1h EMA(50) 대비 가격 위치로 방향 제한 — 가격 > EMA50(1h) → 롱만, 가격 < EMA50(1h) → 숏만.
- **투바 룰(Two-Bar Rule, 원문 표준 정의)**: "0선 위에서 연속 초록(상승) 바 2개 = 매수 신호, 0선 아래에서 연속 빨강(하락) 바 2개 = 매도 신호. 빨강 바에서는 매수 금지, 초록 바에서는 매도 금지"(Bill Williams 원칙).
- 롱: `AC > 0` **AND** 직전 2개 연속봉의 AC값이 모두 전봉 대비 상승(연속 초록) **AND** 1h EMA50 위 → 두 번째 초록봉 종가에 진입.
- 숏: `AC < 0` **AND** 직전 2개 연속봉의 AC값이 모두 전봉 대비 하락(연속 빨강) **AND** 1h EMA50 아래 → 두 번째 빨강봉 종가에 진입.

## 청산 규칙
- 익절: 1.5R 도달 시 50% 익절, 잔량은 AC가 반대 색으로 전환(연속 2개) 시 청산.
- 손절: 신호봉 직전 스윙 저점(롱)/고점(숏) − 1.0×ATR(14, 15m).
- 시간 청산: 8봉(15m×8=2시간) 내 1R 미도달 시 청산.

## 파라미터
- ao_fast=5, ao_slow=34, ac_sma=5 (표준, 고정)
- trend_ema=50(1h) (범위 30~80)
- sl_atr_mult=1.0 (범위 0.8~1.5)
- tp1_r=1.5 (범위 1.2~2.0)
- max_hold=8봉(15m)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: AO(SMA5−SMA34 of 중간가), AC(AO−SMA5(AO)), EMA(50, 1h), ATR(14). 전부 표준 OHLC로 산출 가능.
- 주의: **바이낸스 REST 캔들만으로 완전 구현 가능**, 난이도 낮음. AC는 AO의 2차 파생(이중 지연)이라 신호가 더 늦을 수 있어 저빈도가 될 가능성 높음(수수료 우위 측면에서는 긍정적).

## 스카우트 메모
- 강점: 규칙이 매우 단순·명확(연속 2봉 색상 판정)해 재현성이 매우 높고, 기존 AO 트윈픽스/소서 스펙과 **입력 지표는 공유하되 판정 로직이 명확히 다름**(중복 아님). 트레이딩뷰 부스트 10,430은 참여지표 스크리닝 기준을 충분히 충족.
- 의심점: 원문이 "학습용, 실거래 금지"를 명시할 정도로 초심자용 단순 규칙이라 엣지가 약할 수 있음. AC가 AO보다 한 단계 더 지연된 지표라 15m처럼 낮은 타임프레임에서는 늦은 진입으로 손익비가 기대에 못 미칠 위험. 백테스트 근거가 전무해 스크리닝 규칙 우선순위는 낮음(규칙 3의 "코딩 가능"만 충족).
- 우리 단타 슬리브와의 관계: 기존 볼린저 돌파+거래량+OI 스캘프와는 메커니즘이 다른 순수 모멘텀-가속도 지표라 다변화 가치는 있으나, 백테스트로 최소 엣지 확인이 선행돼야 함.
