# [스윙] 스토캐스틱RSI + EMA50 추세필터 + ADX 강도필터 (4시간)

- **출처**: https://stratbase.ai/en/blog/stochastic-rsi-strategy (StratBase — **WebFetch 원문 확인 실패, 503 반복** → 아래 수치는 검색엔진(WebSearch) 요약을 통한 2차 근거, 신뢰도 낮음, 재검증 필수) / 보강: https://www.quantifiedstrategies.com/stochastic-rsi/ , https://www.quantifiedstrategies.com/rsi-adx-trading-strategy/
- **참여지표**: - (백테스트 기반 블로그로 추정)
- **백테스트 근거**: **[원문 미확인, WebSearch 요약 기반]** BTC/USDT 4h, 2021~2025(정확 표본기간 불명). 순수 StochRSI 크로스: 96트레이드, 승률 51%(비교군 RSI 단순크로스는 48트레이드·승률 54%). **EMA50 추세필터**(가격이 EMA50 상/하에 있을 때만 해당 방향 크로스만 채택) 추가 시 승률 55~60%로 개선. **ADX 강도필터**(추세 강도 확인) 추가 시 손실거래 35% 감소, 승률 52%→57%, PF 1.3→1.6. 수수료 반영 여부 불명. **원문 페이지가 서버 오류로 열리지 않아 1차 검증 불가 — 최우선 재확인 대상.**
- **타임프레임**: 4h
- **시장/대상**: BTC·ETH 무기한

## 진입 규칙
- 롱: StochRSI %K가 %D를 **20 이하 구간에서 상향 교차**(과매도 반전) **AND** 종가 > EMA(50) **AND** ADX(14) 상승 추세 또는 > 20
- 숏: StochRSI %K가 %D를 **80 이상 구간에서 하향 교차**(과매수 반전) **AND** 종가 < EMA(50) **AND** ADX(14) 상승 추세 또는 > 20

## 청산 규칙
- 익절: 반대 극단 도달 시 청산(롱은 %K>80, 숏은 %K<20) 또는 고정 2R
- 손절: 진입봉 직전 스윙 고/저 또는 ATR(14) × 1.5
- 시간/조건 청산: 명시 없음(반대 크로스·SL/TP 우선)

## 파라미터
- stoch_rsi_period=14, stoch_k=3, stoch_d=3 (표준 StochRSI 세팅)
- rsi_period_for_stoch=14 (StochRSI 내부 RSI 기간)
- ema_trend=50 (범위 20~100)
- adx_period=14, adx_threshold=20 (범위 15~25)
- atr_sl_mult=1.5 (범위 1.0~2.0)
- rr_ratio=2.0 (범위 1.5~3.0)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: StochRSI(RSI 위에 스토캐스틱 재적용), EMA(50), ADX(14) — 전부 표준 지표, 바이낸스 OHLCV REST로 계산. 특이 데이터 불필요.
- 난이도: 낮음~중간(StochRSI 계산이 RSI→Stochastic 이중 변환이라 지표 라이브러리 검증 필요).

## 스카우트 메모
- 강점: StochRSI는 우리가 아직 쓰지 않는 오실레이터(기존 RSI-2, 볼밴+RSI다이버전스와 계산식이 다름). EMA/ADX 필터로 승률이 개선되는 패턴이 `adx-di-crossover-trend-daily.md`(별도 소스)의 ADX 필터 효과와도 방향이 일치 → 정성적으로 그럴듯함.
- 의심점: **원문 WebFetch 실패로 수치를 1차 확인하지 못함(가장 큰 약점)**. 표본기간·수수료 반영 여부 불명. 반드시 사이트 재접속 또는 대체 경로로 원문 확인 후 채택 여부 재판단.
- 우리 스윙 슬리브와의 관계: 기존 중기(슈퍼트렌드+RSI, `mid.py`)와 "추세필터 + 오실레이터 반전" 구조가 유사하나 트리거 지표가 다름(StochRSI 크로스 vs RSI 극단) → 완전 대체보다는 병행 검증 후보.
