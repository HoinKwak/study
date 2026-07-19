# [단타] Schaff Trend Cycle(STC) 크립토세팅 크로스 스캘프

- **출처**: 지표 원작 Doug Schaff(1990년대 개발, 2008년 발표). 크립토 권장 파라미터·규칙 해설:
  https://www.litefinance.org/blog/for-beginners/best-technical-indicators/schaff-trend-cycle/ (WebFetch 확인) /
  TradingView 백테스트 스크립트: "Schaff Trend Cycle Strategy for XBTUSD 15m Backtest" by Jerry_4222 —
  https://www.tradingview.com/script/4I4ZajgE-Schaff-Trend-Cycle-Strategy-for-XBTUSD-15m-Backtest/ (WebFetch 확인,
  다만 페이지에서 정량 성과 수치는 노출되지 않음 — 조회수/즐겨찾기만 확인됨) /
  quantifiedstrategies.com의 STC 정량 페이지는 봇 차단으로 원문 확인 불가 → 인용하지 않음.
- **참여지표**: TradingView "Schaff Trend Cycle Strategy for XBTUSD 15m Backtest" 조회수 **19,166** /
  즐겨찾기(boosts) **10,769** (WebFetch로 확인). 종목·타임프레임(XBTUSD 15m)이 우리 단타 슬리브와 정확히 일치.
- **백테스트 근거**: 없음(정량 수치 원문 미확인, 참여지표 + 지표 표준 공식 기반 채택). 다른 웹 검색 스니펫에서
  "199건 트레이드, 평균 +1.25%/트레이드, 승률 75%, MDD 26%"라는 문구가 있었으나 **원문 URL을 특정하지 못해
  출처 미상 — 인용하지 않음**(정량 인용 환각 방지 원칙에 따라 폐기).
- **타임프레임**: 15m 신호 (우리 백테스트 인프라가 15m OHLCV만 보유 — 1m/5m 불가). 4h EMA200 방향 필터 병행.
- **시장/대상**: BTC·ETH 및 유동성 상위 무기한.

## 진입 규칙
- STC 계산(3단계, litefinance 정리):
  1. `MACD = EMA(close, fast) - EMA(close, slow)`
  2. `%K1 = (MACD - MinMACD(n)) / (MaxMACD(n) - MinMACD(n)) * 100` (n봉 구간 스토캐스틱화)
  3. `STC = EMA(%K1, smooth)` (이중 스무딩 — Schaff 원 공식은 %K1→%D1→%K2→%D2 이중 스토캐스틱+EMA이나
     본 스펙은 litefinance가 제시한 실전 단순화 버전을 채택. 정밀 재현 시 이중 스무딩 버전과 A/B 비교 권장)
  4. 크립토 권장 파라미터: `fast=10, slow=21, smooth(n)=5` (litefinance "Cryptocurrency Market" 표 — 표준 forex 값
     23/50/10 대비 빠르게 세팅)
- **추세 필터**: 4h 종가가 4h EMA200 위(롱만 허용) / 아래(숏만 허용).
- 롱: `STC[t-1] < 25` 이고 `STC[t]`가 25를 상향 돌파(바닥권 반전) + 4h 추세 필터 상승.
- 숏: `STC[t-1] > 75` 이고 `STC[t]`가 75를 하향 돌파(천장권 반전) + 4h 추세 필터 하락.
- (옵션) 진입봉 실체 ≥ 0.5×ATR(14, 15m)로 노이즈 신호 배제.

## 청산 규칙
- 익절: STC가 반대 임계(롱은 75, 숏은 25)에 도달 시 절반 익절, 완전 청산은 STC가 50선을 반대로 재돌파할 때.
- 손절: 진입가 대비 ATR(14, 15m) × 1.2, 또는 직전 스윙 저/고점 중 더 타이트한 쪽.
- 시간 청산: 24봉(15m 기준 6시간) 내 STC가 50을 넘지 못하면(추세 미형성) 청산.

## 파라미터
- stc_fast_ema=10 (범위 8~13) / stc_slow_ema=21 (범위 18~26) / stc_smooth=5 (범위 3~10)
- stc_low=25 / stc_high=75 (지표 표준값, 고정 권장)
- trend_filter_ema=200 (4h)
- atr_mult_sl=1.2 (범위 1.0~1.8)
- max_hold_bars=24 (15m 기준, 범위 16~48)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: EMA(종가만으로 계산), MACD, 롤링 min/max(스토캐스틱화), ATR. **전부 15m OHLCV 종가/고저로 계산
  가능** — OI·거래량 불필요.
- 난이도: 중간(이중 스무딩 정확도 이슈 — 원 Schaff 공식과 단순화 버전 결과 차이 가능, 백테스트 시 두 버전 비교 권장).
- 주의: 없음(오더북·틱 데이터 불필요).

## 스카우트 메모
- 강점: 우리 85개 기존 스펙에 STC 계열 지표가 없음(MACD·스토캐스틱은 각각 있으나 STC는 둘의 결합형으로
  구조가 다름). 크립토향 파라미터가 이미 커뮤니티에서 통용(10/21/5)되고 XBTUSD 15m 백테스트 스크립트가
  정확히 우리 인프라(15m)와 일치해 즉시 검증 가능.
- 의심점: 정량 승률 수치는 출처 특정 실패로 폐기함 — **완전히 참여지표 기반**으로만 채택. 임계값(25/75)
  크로스는 오늘 검증에서 문제가 된 "단순 지표 크로스"와 구조적으로 유사할 위험이 있어, 4h EMA200 필터를
  필수로 걸어 다중조건화함.
- 우리 슬리브와의 관계: 기존 단타 슬리브(볼린저 돌파+거래량+OI)와는 완전히 다른 오실레이터 반전 로직 —
  대체보다는 국면별 보완(횡보 반전장에서 유효할 가능성, 돌파장에서는 기존 볼린저 전략이 담당).
