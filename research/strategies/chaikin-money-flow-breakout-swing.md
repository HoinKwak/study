# [스윙] 차이킨 자금흐름(Chaikin Money Flow, CMF) 제로라인 + 구조 브레이크아웃

- **출처**: https://enlightenedstocktrading.com/chaikin-money-flow/ (CMF 공식·규칙 정리) /
  https://www.vestinda.com/academy/chaikin-money-flow-indicator-strategies-mastering-trading-techniques (보강, 전략 적용 사례) /
  개념 원조: Marc Chaikin 고안(1980년대), 종가 위치 기반 매수/매도 압력 누적 지표
- **참여지표**: 없음(정량 참여지표 미집계) — TradingView·StockCharts 등 주요 차트 플랫폼 표준 내장 지표로 업계 재현성 높음.
- **백테스트 근거**: 없음(개념 기반). 원문은 정성적 규칙(제로라인 상/하+ 가격 지지/저항 돌파, 다이버전스)만 제시하며 구체적 수익률·승률 수치 없음. **채택 전 자체 백테스트 필수**.
- **타임프레임**: 4h 신호 / 1d 확인
- **시장/대상**: BTC·ETH·시총상위 알트 무기한

## 진입 규칙
- **CMF 계산**: `MFM_t(Money Flow Multiplier) = ((close_t - low_t) - (high_t - close_t)) / (high_t - low_t)` (범위 -1~+1, 종가가 봉 상단에 가까울수록 +1에 근접)
  `MFV_t(Money Flow Volume) = MFM_t × volume_t`
  `CMF = sum(MFV, cmf_period) / sum(volume, cmf_period)` (원문 표준 cmf_period=21)
- **롱**: ① 가격이 최근 breakout_lookback(예 20봉) 저항선(스윙 고점)을 종가 기준 상향 돌파 **AND** ② 동시점 CMF > 0(자금흐름이 매수 우위) **AND** ③ CMF가 최근 cmf_rising_bars(예 3봉) 연속 상승 중.
- **숏**: ① 가격이 최근 20봉 지지선(스윙 저점)을 종가 기준 하향 돌파 **AND** ② CMF < 0 **AND** ③ CMF가 최근 3봉 연속 하락 중.
- **다이버전스 보조 신호(옵션)**: 가격이 신저점 형성 + CMF는 더 높은 저점(불리시 다이버전스) → 역추세 롱 후보(브레이크아웃형과 별도 관리 권장, 신뢰도 검증 필요).

## 청산 규칙
- **익절**: 목표 R배수(rr_ratio, 예 2.0R, 스윙 특성상 손익비를 크게 잡음) 또는 CMF가 제로라인을 역방향 재돌파 시 청산.
- **손절**: 돌파 시 사용한 지지/저항선(직전 스윙 저/고점) 바로 너머, ATR(4h,14)×stop_atr_mult(예 1.0) 여유.
- **시간/조건 청산**: 진입 후 max_hold_bars(예 20봉=4h×20≈3.3일) 내 CMF가 제로라인 부근(±0.05)으로 평탄화되면 자금흐름 소진으로 판단, 조기 청산 검토.

## 파라미터
- cmf_period=21 (원문 표준값, 범위 14~30)
- breakout_lookback=20 (범위 15~30)
- cmf_rising_bars=3 (범위 2~5)
- rr_ratio=2.0 (범위 1.5~3.0)
- stop_atr_mult=1.0 (범위 0.7~1.5)
- max_hold_bars=20 (4h 기준, 범위 15~30)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: CMF(고가·저가·종가·거래량만으로 계산), ATR, 스윙 고/저.
- 주의: 완전히 표준 klines OHLCV만으로 구현 가능 — 오더북·틱데이터·OI 등 별도 데이터 불필요. 데이터 요구가 가장 낮은 후보 중 하나.

## 스카우트 메모
- **강점**: 볼륨 프로파일·OBV·CVD류 대비 계산이 단순(고저종가 위치 비율×거래량)하면서도 "거래량 가중 매수/매도 압력"이라는 유사한 정보를 담아 **구조 브레이크아웃의 거래량 확인 필터**로 유용. 스윙 슬리브(4h/1d)라 수수료 부담이 작아 손익비 2R 설계가 인트라데이 대비 현실적.
- **의심점**: 정량 백테스트 근거 전무 — 순수 개념 기반. CMF는 봉 내 종가 위치만 보므로 갭이 크거나 윅이 긴 크립토 변동성 장세에서 왜곡될 수 있음(고저 범위가 넓은데 종가가 중간이면 MFM이 0에 가까워져 신호가 희석).
- **우리 슬리브와의 관계**: 기존 `weekly-structure-breakout-retest.md`(주간 구조 브레이크아웃), `bull-flag-measured-move-breakout-swing.md`와 "구조 돌파" 큰 틀은 유사하나, CMF라는 **거래량 압력 지표로 돌파를 확인**한다는 점이 차별점 — 기존 스윙 브레이크아웃 전략들의 **거래량 확인 필터(대체 지표)**로 결합 검토 가치 있음. 기존 볼린저 눌림목 중기 전략과는 트리거 로직이 달라 중복 낮음.
