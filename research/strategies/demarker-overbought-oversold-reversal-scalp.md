# [단타] DeMarker(DeM) 과매수/과매도 되돌림 반전 스캘프

- **출처**: 지표 원안: Tom DeMark(1980년대 고안). 공식·규칙 정리:
  https://tradersunion.com/interesting-articles/forex-indicators-for-traders/demarker-indicator/ ,
  https://forextester.com/blog/demarker/ , https://www.metatrader4.com/en/trading-platform/help/analytics/tech_indicators/demarker
  (WebFetch/WebSearch로 공식 확인). 크립토 적용 팁(임계값 확장 75/25, 기간 18~21)은
  https://blog.ueex.com/demark-indicators/ 참고.
- **참여지표**: - (표준 지표 자체는 MT4/TradingView 내장급으로 업계 재현성 매우 높음. 특정 게시물의 조회수·추천수 집계는 없음)
- **백테스트 근거**: **없음(개념/공식 기반)** — 검색된 2차 자료들은 정성적 사용법만 제공, 크립토 대상 정량 수치(승률·PF) 없음. 채택 전 자체 백테스트 필수.
- **타임프레임**: 15m 신호 / 1h 추세 필터
- **시장/대상**: BTC·ETH·시총상위 알트 무기한

## 진입 규칙
- **DeMarker 계산**(N=14 기본):
  - `DeMax_t = max(high_t - high_{t-1}, 0)`, `DeMin_t = max(low_{t-1} - low_t, 0)`
  - `DeM_t = SMA(DeMax, N) / (SMA(DeMax, N) + SMA(DeMin, N))` → 0~1 범위(고가/저가 갱신폭 기반, RSI와 달리 종가가 아닌 고저 변화폭 사용 → 우리 기존 RSI 계열과 신호원이 다름)
- **롱**: DeM(14, 15m)이 `oversold=0.30` 아래로 내려갔다가 **다시 0.30 위로 상향 돌파**(되돌림 확인, 바닥 찍고 반등 시점 포착) **AND** 1h EMA(50) 기울기가 급격한 하락 추세가 아님(과도한 역추세 매매 방지, `1h_ema50_slope > -0.1%/bar`).
- **숏**: DeM(14, 15m)이 `overbought=0.70` 위로 올라갔다가 **다시 0.70 아래로 하향 돌파** **AND** 1h EMA(50) 기울기가 급격한 상승 추세가 아님.
- 크립토 변동성 감안 임계값을 표준 0.30/0.70 대신 넓게(`oversold=0.25, overbought=0.75`) 쓰는 대안도 병기(원문 크립토 적용 팁).

## 청산 규칙
- 익절: `rr_target=1.5R`(스캘프이므로 손익비 낮게, 대신 승률 위주) 또는 DeM이 반대 극단(0.5 중립선)에 도달 시 청산.
- 손절: 진입 신호봉의 저가(롱)/고가(숏) 바로 바깥, `stop_atr_buffer=0.3×ATR(15m,14)` 추가 여유.
- 시간 청산: `max_hold=16봉`(15m×16=4h) 내 목표 미도달 시 청산.

## 파라미터
- dem_period=14 (범위 10~21, 크립토는 18~21 권장 소스도 있음)
- oversold=0.30 / overbought=0.70 (크립토 변형: 0.25/0.75, 범위 0.20~0.35)
- ema_trend_len=50 (1h)
- rr_target=1.5 (범위 1.2~2.0)
- stop_atr_buffer=0.3 (범위 0~0.5)
- max_hold=16봉

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 고가·저가 변화폭 기반 SMA(DeMax/DeMin) — 표준 OHLCV로 계산 가능. EMA(50, 1h) 추세 필터.
- 주의: 공식이 단순(고저 갱신폭 SMA 비율)해 구현 난이도 낮음. 오더북·틱데이터 불필요.

## 스카우트 메모
- 강점: **RSI/스토캐스틱과 다른 신호원**(종가가 아닌 고가·저가 갱신폭 기반)이라 우리가 이미 보유한 RSI2/스토캐스틱/CCI/윌리엄스%R 계열 과매수·과매도 전략들과 상관성이 낮을 가능성 — 다양화 후보. 공식이 매우 단순해 구현·검증이 빠름.
- 의심점: 백테스트 근거 전무 — 순수 개념 채택. 이미 보유한 과매수/과매도 반전류(cci-extreme-momentum-scalp, williams-r-extreme-reversal-scalp, mfi-extreme-mean-reversion-scalp 등)와 **개념적으로 유사한 카테고리**라 신호 상관성이 높으면 큰 신규 엣지가 아닐 수 있음 — 상관관계 확인 후 채택 여부 판단 권장.
- 우리 단타 슬리브와의 관계: scalp15m(돌파형)과 반대되는 평균회귀형이라 상호보완 가능하나, 이미 보유한 다수의 유사 반전형 지표와 포지셔닝이 겹칠 위험 있음.
