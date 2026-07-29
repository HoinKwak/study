# ROC(변화율) 극단 Z-스코어 평균회귀 [단타]

- **출처**: 개념·공식 참고 — Changelly "Crypto Rate of Change Indicator: Formula, Signals, and Use Cases" https://changelly.com/blog/rate-of-change-roc-crypto/ ,
  XS "ROC (Rate of Change) Indicator: Formula, Signals & Examples" https://www.xs.com/en/blog/roc-indicator/ ,
  ArrowAlgo "Rate of Change (ROC): Complete Guide for Algo Trading" https://arrowalgo.com/rate-of-change-roc-complete-guide-algorithmic-trading/
  (QuantifiedStrategies의 ROC 전략 백테스트 페이지는 봇 차단으로 원문 확인 불가 — 해당 발 수치는 인용하지 않음)
- **참여지표**: - (복수 독립 교육용 블로그의 표준 지표 설명, 조회수·좋아요 수치 없음. 단일 인플루언서 게시물이 아닌 다수 출처가 동일 개념을 반복 서술한다는 점만 근거)
- **백테스트 근거**: **없음(정량 수치 원문 미확인)**. XS/ArrowAlgo 원문은 "ROC 절대 임계값은 자산 변동성에 따라 달라지므로 고정값보다 상대 정규화(z-score)가 낫다"는 정성적 권고만 제시. QuantifiedStrategies가 주식(S&P500 등)에서 ROC 단독 전략이 RSI/스토캐스틱/Williams %R보다 열등하다고 언급하나 이는 **주식 대상 원문 확인 불가**로 참고만 함.
- **타임프레임**: 15m 신호 / 1h 확인.
- **시장/대상**: BTC·ETH·유동성 상위 알트 무기한.

## 핵심 아이디어
ROC는 단순 `(종가 - n봉전 종가) / n봉전 종가 × 100`. 원문들이 공통 지적하는 문제(고정 % 임계값이 자산·변동성마다 다름)를 해결하기 위해 **롤링 Z-스코어로 정규화**한 뒤 극단값에서 평균회귀를 노린다.

## 진입 규칙
1. `ROC(n=9) = (close_t - close_{t-9}) / close_{t-9} × 100` (15m 기준, 9봉≈2.25시간).
2. 최근 100봉의 ROC 분포에서 `roc_z = (ROC_t - mean(ROC, 100)) / std(ROC, 100)` 계산.
3. 롱: `roc_z ≤ -2.0` (극단 과매도) **AND** RSI(14) < 30 (확인 필터) **AND** 종가가 1h 기준 상승/횡보 추세(예: 1h EMA50 위 또는 근접, 강한 하락추세에서는 제외).
4. 숏: `roc_z ≥ +2.0` **AND** RSI(14) > 70 **AND** 1h EMA50 아래/근접 추세.

## 청산 규칙
- 익절: `roc_z`가 0으로 회귀(중심 재진입) 시 청산, 또는 진입가 대비 +1.5×ATR(14, 15m).
- 손절: 진입가 대비 −1.0×ATR(14, 15m) (평균회귀 특성상 손절을 타이트하게).
- 시간 청산: 진입 후 16봉(15m, 약 4시간) 내 목표 미달성 시 강제 청산(회귀 실패 정리).

## 파라미터
- roc_len=9 (범위 6~14)
- zscore_lookback=100 (범위 60~150)
- z_entry=2.0 (범위 1.5~2.5)
- rsi_len=14, rsi_long=30/rsi_short=70
- trend_filter=EMA50(1h)
- atr_tp_mult=1.5 / atr_sl_mult=1.0
- max_hold=16봉(15m)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: ROC(단순 수식), 롤링 평균/표준편차(Z-스코어), RSI(14), EMA(50, 1h), ATR(14). 전부 캔들 OHLC 기반, 계산 매우 단순.
- 주의: **바이낸스 REST 캔들로 완전 충족**, 오더북/틱 불필요. 코딩 난이도 낮음.

## 스카우트 메모
- 강점: 규칙이 극도로 단순·결정론적이라 빠른 구현·백테스트 가능. Z-스코어 정규화로 자산별 변동성 차이(원문이 공통 지적하는 ROC의 약점)를 보완. 기존 보유 다수 평균회귀 전략(RSI2, 볼린저페이드, Williams %R 등)과 지표 자체는 다르나(모멘텀 변화율 vs 오실레이터 레벨) **개념적으로 유사군**.
- 의심점: 정량 백테스트 근거가 전무하고, 참여지표도 없어 스크리닝 근거가 가장 약함(순수 "규칙 명확성" 기준 채택). QuantifiedStrategies의 정성적 언급(ROC 단독이 RSI 등보다 열등)이 사실이라면 우리 프레임 백테스트에서 FAIL 가능성 높음 — **우선순위 낮게 검증**할 후보.
- 우리 단타 슬리브와의 관계: 기존 `rsi2-mean-reversion`, `bollinger-band-fade-range`, `williams-r-extreme-reversal-scalp` 등과 **컨셉 중복 위험 높음**(모두 "극단→평균회귀"). 채택 가치는 낮고, 이미 보유한 평균회귀 전략들이 대부분 FAIL인 정황(CLAUDE.md 미션 #28 스냅샷)을 고려하면 **백테스트 우선순위에서 제외** 권장.
