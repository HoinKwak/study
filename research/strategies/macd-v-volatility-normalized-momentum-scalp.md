# [단타] MACD-V(변동성정규화 MACD) 모멘텀 생명주기 스캘프

- **출처**: https://www.tradingview.com/script/mionn7XC-MACD-V-Volatility-Normalized-MACD/ (TradingView, KivancOzbilgic — WebFetch로 원문 공식·임계값 확인). 원 지표는 Alex Spiroglou가 2022년 CMT Association 저널(Journal of Technical Analysis)에 발표한 "MACD-V: Enhancing Momentum with Volatility Normalization"이 원 출처.
- **참여지표**: TradingView 지표 페이지 **좋아요 2,121 / 부스트 101** (WebFetch로 확인).
- **백테스트 근거**: **원 논문(주식시장 기준)은 MACD 단독 대비 RSI 결합 시 샤프비율 0.58→1.04, 거래량 필터 결합 시 승률 38.2%→47.8% 개선**이라는 정량 결과가 존재한다는 2차 서술을 확인했으나, **이번 세션에서 원 CMT 논문 PDF를 직접 WebFetch로 대조하지 못함 — 수치의 정확한 출처(어느 자산·기간·표본)를 확정하지 못했으므로 "정량 수치 원문 미확인"으로 표기**. 자산군도 주식시장(미국 지수 등) 연구이며 **크립토 적용은 미검증**. 따라서 이 스펙은 **정성적 지표 정의(TradingView 원문 확인)만 신뢰**하고, 정량 개선폭은 참고 수준으로만 취급.
- **타임프레임**: 15m~1h 신호(스캘프), 4h 확인
- **시장/대상**: BTC·ETH·주요 알트 무기한

## 진입 규칙
- 지표: `MACD_V(t) = (EMA(12) − EMA(26)) / ATR(26) × 100`. (표준 MACD 히스토그램을 ATR로 나눠 변동성 정규화 — 자산·시점 간 비교 가능하게 만든 것이 핵심 차별점).
- **신호선**: `Signal = EMA(MACD_V, 9)`.
- **모멘텀 생명주기 구간**(원문 정의): `|MACD_V| < 50` = 중립/횡보(거래 회피), `50 ≤ |MACD_V| < 150` = 강한 방향성 모멘텀(추세추종 구간), `|MACD_V| ≥ 150` = 극단/과열(반전 리스크 고조).
- 롱: MACD_V가 **50을 상향 돌파**(중립 구간 탈출) **AND** MACD_V > Signal(골든크로스) **AND** MACD_V < 150(아직 과열 아님) → 롱 진입.
- 숏: MACD_V가 **−50을 하향 돌파 AND** MACD_V < Signal **AND** MACD_V > −150 → 숏 진입.
- 필터(권장, 원문 밖 보강): vol_ratio(현재 거래량/20MA거래량) ≥ 1.2 동반 시만 진입(거래량 확인 결합 — 2차 서술에서 언급된 "거래량 필터로 승률 개선" 취지 반영, 우리 구현 보강).

## 청산 규칙
- 익절: MACD_V가 **150 이상(과열)** 도달 시 부분 익절 검토, 완전 청산은 아님.
- 손절: 진입봉 저점(롱)/고점(숏) 또는 ATR(14)×1.5.
- 시간/조건 청산: MACD_V가 다시 신호선 아래(롱)/위(숏)로 데드크로스하거나 |MACD_V|가 50 아래로 재진입(모멘텀 소멸)하면 청산.

## 파라미터
- fast_ema=12, slow_ema=26, signal_ema=9 (표준 MACD 파라미터 그대로)
- atr_len=26 (MACD 느린선과 동일 기간 사용이 원문 관례)
- neutral_th=50, extreme_th=150 (원문 정의, 고정 권장)
- vol_ratio_min=1.2 (범위 1.0~1.5, 우리 보강 필터)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: EMA(12/26/9), ATR(26), 거래량 20MA — 전부 바이낸스 REST OHLCV로 계산 가능. 오더북/틱 불필요.
- 난이도: **낮음**. 표준 MACD 계산에 ATR 나누기 한 줄만 추가되는 수준 — 구현 매우 간단.
- 주의: ATR가 0에 근접(극저변동성)할 때 분모가 작아져 MACD_V가 비정상적으로 튀는 구간이 있을 수 있음 — 최소 ATR 하한(예: 가격의 0.05%) 클램핑 권장.

## 스카우트 메모
- **강점**: 기존 보유 MACD 계열(`macd-rsi-200sma-trend-filter-swing`, `macd-oi-directional-confluence-swing`, `vwmacd-crossover-swing`, `quantpedia-macd-d1h1-trend-filter-scalp`(FAIL), `btc-mtf-macd-daily-filter-trailing-exit-swing`, `joel-on-crypto-mtf-macd-histogram-scalp`)는 모두 **가격 단위(달러) MACD**를 쓰는 반면, MACD-V는 **ATR로 나눠 무차원화**해 자산·변동성 국면 간 절대 비교가 가능하다는 점이 명확히 다른 메커니즘. 특히 변동성이 자산·기간마다 크게 다른 크립토 알트 유니버스에서 "동일 임계값(±50/±150)을 여러 종목에 공통 적용"할 수 있다는 실용적 장점.
- **의심점**: 정량 백테스트 근거가 크립토는 물론 원 논문 자체도 이번 세션에서 원문 대조하지 못해 **주식시장 결과조차 확정 인용 불가**. 순수 지표 정의만 신뢰하고 실제 엣지는 우리 프레임워크로 처음부터 검증해야 함(사전 기대치를 낮게 잡을 것).
- **우리 슬리브와의 관계**: 기존 MACD 계열과 **직접 경쟁/대체** 관계에 가까움 — 동일 신호 로직(MACD 크로스)에 정규화만 다르므로, 병렬 백테스트해 정규화가 실제로 승률/PF를 개선하는지(가설: 알트코인처럼 변동성이 큰 종목에서 노이즈 필터링 효과) 확인할 가치가 있음. 우리 라이브 전략(`scalp15m`, 볼린저 돌파형)과는 지표 계열이 달라 중복 아님.
