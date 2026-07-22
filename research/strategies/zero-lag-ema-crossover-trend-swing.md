# [스윙] Zero-Lag EMA(ZLEMA) 교차 추세추종

- **출처**: https://www.tradingview.com/script/LTqZz3l9-Indicator-Zero-Lag-EMA-a-simple-trading-strategy/ (TradingView, LazyBear) / 원 이론: John Ehlers & Ric Way, "Zero Lag (Reduced Lag) Moving Average" (mesasoftware.com 논문) / https://www.quantifiedstrategies.com/zero-lag-exponential-moving-average/ (봇차단으로 원문 수치 미확인)
- **참여지표**: TradingView 좋아요/부스트 **6,100**, 댓글 **131,850** (2026-07 WebFetch로 원문 페이지 확인. LazyBear는 TradingView 최상위 인지도 스크립터 중 하나 — 신뢰 계정)
- **백테스트 근거**: **정량 수치 원문 미확인**. QuantifiedStrategies 페이지는 봇 차단으로 실제 수치를 확인하지 못함(WebFetch 시도 시 "Verifying that you are not a robot" 페이지만 반환됨 — 지어내지 않고 정직히 표기). 웹서치 요약상 "S&P500에선 긍정적, 크립토는 변동성 탓에 휩쏘 잦아 결과 혼재"라는 정성적 경고만 확인됨 → 참여지표 기반으로만 채택, 백테스트 최우선순위는 낮음.
- **타임프레임**: 4h 신호 / 1d 확인 (원저자는 저타임프레임에서 랙 감소 효과를 강조하나, 크립토 크로스오버는 저TF일수록 휩쏘 심하다는 경고가 있어 스윙 TF로 채택)
- **시장/대상**: BTC·ETH·시총상위 알트 무기한

## 진입 규칙
- ZLEMA 계산: `lag = floor((length-1)/2)`, `EmaData = price + (price - price[lag])`, `ZLEMA = EMA(EmaData, length)` (일반 EMA에 "모멘텀 보정"을 더해 랙을 줄인 값).
- 롱: **빠른 ZLEMA(9)가 느린 ZLEMA(21)를 상향 돌파** **AND** 종가가 두 ZLEMA 위.
- 숏: **빠른 ZLEMA(9)가 느린 ZLEMA(21)를 하향 돌파** **AND** 종가가 두 ZLEMA 아래.
- (권장 필터) ADX(14) ≥ 20 — 레인지장 크로스오버 남발 방지(원전엔 없으나 크립토 특성상 추가 권장).

## 청산 규칙
- 익절: 반대 크로스(느린 ZLEMA를 종가가 재돌파) 시 청산, 또는 ATR 트레일링(신고가−ATR×2.0)으로 추세 추적.
- 손절: 진입가 대비 ATR(14) × 2.0.
- 시간 청산: 명시 없음(추세추종형이라 반대 크로스/트레일링 우선).

## 파라미터
- zlema_fast=9 (범위 5~13)
- zlema_slow=21 (범위 18~34)
- adx_min=20 (범위 15~25, 선택 필터)
- atr_period=14, atr_sl_mult=2.0 (범위 1.5~3.0), atr_trail_mult=2.0 (범위 1.5~3.0)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: ZLEMA(가격+모멘텀보정 후 EMA), ADX(14, 선택), ATR(14). 전부 바이낸스 OHLCV 캔들로 계산 가능.
- 주의: ZLEMA는 미래 데이터 룩어헤드 없음(과거 lag봉만 참조) — 재귀식이라 워밍업 구간 주의. 오더북/틱 불필요.

## 스카우트 메모
- 강점: EMA류 크로스오버 중 **가장 랙이 짧다는 것이 Ehlers/Way 원저자 이론의 핵심**(우리 기존 Hull MA·McGinley·KAMA와 같은 "저지연 이평선" 계열이나 산식이 다름 — 가격에 모멘텀 보정을 더한 뒤 EMA). 참여지표(좋아요 6.1K, 댓글 13만+)가 매우 높아 커뮤니티 검증 수요가 큼을 시사.
- 의심점: 웹서치 요약 자체가 "크립토에선 결과 혼재/휩쏘 잦음"이라 경고 — 정직하게 낮은 우선순위. 단순 크로스오버만으론 우리가 이미 겪은 EMA9/21 크로스(ema-9-21-crossover.md)와 근본적으로 같은 실패 패턴(과빈발) 반복 가능성 → 반드시 ADX/추세필터 병행 백테스트 필요.
- 우리 스윙 슬리브와의 관계: 기존 `ema-9-21-crossover.md`, `hull-moving-average-crossover-scalp.md`, `mcginley-dynamic-adaptive-ma-crossover-swing.md`, `kama-atr-adaptive-trend-swing.md`와 **"저지연 이평 크로스오버" 계열로 개념 중복** — 산식만 다름. 신규 채택보다는 **기존 저지연 MA 계열과의 교차검증(어느 산식이 크립토에서 가장 견고한지)** 목적으로 우선순위 낮게 참고.
