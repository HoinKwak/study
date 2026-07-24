# [스윙] 거래량가중 MACD(VW-MACD) 크로스오버 추세추종

- **출처**: 개념: https://kridtapon.substack.com/p/volume-weighted-macd-crossover-strategy
  (제목·개념만 공개, 본문 상세·백테스트 수치는 유료 구독 페이월로 WebFetch 확인 불가 — **본문 미확인**).
  공식·VWMA 정의 보강: https://www.tradingview.com/scripts/vwma/ , https://trendspider.com/learning-center/what-is-the-volume-weighted-moving-average-vwma/
  (WebFetch/WebSearch로 VWMA 공식 확인).
- **참여지표**: - (Substack 특정 게시물 조회수·추천수 미확인. 개념 자체는 VWMA+MACD 표준 조합)
- **백테스트 근거**: **없음(원문 백테스트가 페이월 안에 있어 수치 미확인)** — "backtesting을 사용했다"는 언급만 확인, 승률·PF·기간 등 구체 수치는 **원문 미확인**이라 인용하지 않음. 채택 전 자체 백테스트 필수.
- **타임프레임**: 4h 신호 / 1d 확인
- **시장/대상**: BTC·ETH·시총상위 알트 무기한

## 진입 규칙
- **VWMA 계산**: `VWMA_n = Σ(close_i × volume_i, n봉) / Σ(volume_i, n봉)` (표준 공식)
- **VW-MACD 계산**: 표준 MACD의 EMA를 VWMA로 대체
  - `VW_MACD_line = VWMA(close, 12) - VWMA(close, 26)`
  - `VW_signal_line = EMA(VW_MACD_line, 9)`
  - `VW_hist = VW_MACD_line - VW_signal_line`
- **롱**: `VW_MACD_line`이 `VW_signal_line`을 상향 돌파(골든크로스) **AND** 크로스 시점 거래량이 20봉 평균 이상(거래량 뒷받침 확인) **AND** 가격이 EMA(200, 4h) 위(장기 추세 필터).
- **숏**: `VW_MACD_line`이 `VW_signal_line`을 하향 돌파 **AND** 거래량 확인 **AND** 가격이 EMA(200, 4h) 아래.

## 청산 규칙
- 익절: `rr_target=2.5R` 또는 `VW_hist`가 정점 찍고 3봉 연속 축소(모멘텀 둔화) 시 부분 청산.
- 손절: 진입 시점 스윙 저점(롱)/고점(숏) 바로 바깥, `stop_atr_mult=1.2×ATR(4h,14)`.
- 시간 청산: `max_hold_bars=20봉`(4h×20≈3.3일) 내 VW_MACD가 재차 반대 크로스하면 즉시 청산(추세 무효화).

## 파라미터
- vwma_fast=12, vwma_slow=26, signal_len=9 (표준 MACD 파라미터 그대로 적용, 범위 각각 ±20%)
- vol_confirm_mult=1.0 (20봉 평균 대비, 범위 0.8~1.3)
- ema_trend_len=200 (4h)
- rr_target=2.5 (범위 2.0~3.5)
- stop_atr_mult=1.2 (범위 1.0~1.8)
- max_hold_bars=20

## 코딩 난이도 / 데이터 요구
- 필요한 지표: VWMA(종가·거래량), EMA(신호선·200추세), ATR. 표준 klines OHLCV로 전부 구현 가능.
- 주의: VWMA는 SMA류 대비 계산이 약간 더 필요(거래량 가중합)하나 pandas로 간단히 구현 가능. 오더북·틱데이터 불필요.

## 스카우트 메모
- 강점: **일반 MACD(EMA 기반)와 다른 스무딩 방식**(거래량 가중)이라 우리가 이미 보유한 `macd-rsi-200sma-trend-filter-swing.md`(일반 MACD+RSI+200SMA)와 **신호 계산식 자체가 다름** — 계산 로직 차별화된 신규 후보로 볼 수 있음(단, 개념적 카테고리는 "MACD 크로스+추세필터"로 유사).
- 의심점: 원문 백테스트 수치가 페이월 뒤에 있어 **완전히 미확인** — 정성적 컨셉만 채택. 이미 MACD 계열 추세추종을 1개 보유 중이라 우선순위는 중간.
- 우리 단타 슬리브와의 관계: 스윙 슬리브(4h/1d)와 결이 맞음. 기존 macd-rsi-200sma-trend-filter-swing과 겹칠 경우 **대체재**로 검토(거래량 가중이 신호 품질을 개선하는지 A/B 백테스트로 비교 권장).
