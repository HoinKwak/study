# [단타] Ease of Movement(EMV, Richard Arms) 제로크로스 스캘프

- **출처**: 지표 원저자 Richard W. Arms Jr. 참고 2차자료 — [TrendSpider 러닝센터](https://trendspider.com/learning-center/mastering-the-ease-of-movement-index-emv/), [Tradingsim 블로그](https://app.tradingsim.com/blog/ease-of-movement-indicator/), [Ease of Movement (EOM) Backtest — TradingView 스크립트(HPotter)](https://www.tradingview.com/script/MSLQg3lV-Ease-of-Movement-EOM-Backtest/), [QuantifiedStrategies(원문 봇검증 차단으로 본문 미확인)](https://www.quantifiedstrategies.com/ease-of-movement/)
- **참여지표**: TradingView HPotter "Ease of Movement (EOM) Backtest" 스크립트 — **좋아요/부스트 3,222**(WebFetch로 원문 페이지 직접 확인, TradingView 전략 스크립트 기준 상당히 높은 참여도). 사용횟수(Uses) 표시는 57로 낮으나 좋아요 수가 압도적으로 높은 점으로 볼 때 "괜찮은 아이디어로 많이 참고됐지만 실사용 전환은 적다"는 패턴.
- **백테스트 근거**: **없음(정량 수치 원문 미확인)**. QuantifiedStrategies.com 전용 백테스트 페이지가 존재하나 Cloudflare 봇검증에 막혀 승률·PF·표본기간 등 본문 수치를 WebFetch로 확인하지 못했다. TradingView 스크립트 페이지에도 성과 수치는 게시돼 있지 않다. → **참여지표(좋아요 3,222) 기반**으로 채택.
- **타임프레임**: 15m 신호(스무딩 SMA(14)의 제로크로스) / 1h EMA(50) 추세 확인.
- **시장/대상**: BTC·ETH·주요 알트 USDT 무기한.

## 지표 정의 (Richard Arms 원 공식, 크립토용 정규화 포함)
1. 중점이동(Distance Moved) = `((High+Low)/2) - ((PrevHigh+PrevLow)/2)`
2. Box Ratio = `Volume / (High-Low)`
3. 1-period EMV(raw) = `Distance Moved / Box Ratio`
4. **정규화(크립토 적용 시 필수 조정)**: 원 공식은 주식 거래량 규모(억 단위)에 맞춰진 고정 상수(보통 1e8)로 나누는 관행이 있으나, 심볼별 거래량 스케일이 천차만별인 크립토 무기한에는 고정 상수가 무의미하다. 대신 **Volume을 해당 심볼의 직전 20봉 평균 거래량으로 나눠 상대화**한 뒤 위 공식을 적용한다: `Box Ratio = (Volume / VolumeMA20) / (High-Low)`.
5. SMA_EMV(14) = 1-period EMV의 14봉 단순이동평균(원저자 권장 스무딩).

## 진입 규칙
- **추세 확인 필터**: 1h EMA(50) 위/아래로 방향 구분 — 가격이 EMA50 위면 롱만, 아래면 숏만 허용.
- **롱**: SMA_EMV(14)가 0선을 아래→위로 상향 돌파하는 순간(제로크로스) + 1h EMA50 위.
- **숏**: SMA_EMV(14)가 0선을 위→아래로 하향 돌파하는 순간 + 1h EMA50 아래.
- (선택 필터) 신호 유의성 강화를 위해 EMV 절대값이 최근 50봉 표준편차의 0.5배 이상일 때만 채택(미세한 노이즈성 제로크로스 배제) — 원 공식엔 없는 [제안] 보강.

## 청산 규칙
- 익절: 진입가 대비 ATR(14)×1.5 도달 시 1차, 이후 ATR 트레일링(신고가/신저가 − ATR×1.0)으로 잔량 청산.
- 손절: 진입 신호봉 기준 ATR(14)×1.0 반대방향, 또는 직전 스윙 저/고점.
- 시간/조건 청산: SMA_EMV(14)가 재차 0선을 반대로 교차하면(신호 소멸) 즉시 청산.

## 파라미터
- emv_ma_period=14 (범위 9~21)
- vol_norm_lookback=20 (범위 10~30, 거래량 정규화 기준)
- ema_trend_filter=50 (범위 20~100, 1h 기준)
- atr_period=14 (범위 10~20)
- signal_strength_min_std_mult=0.5 (범위 0~1.0, 선택 필터)
- tp1_atr_mult=1.5, trail_atr_mult=1.0

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 고가·저가·거래량(모두 OHLCV), EMA(50), ATR(14). **전부 바이낸스 REST 캔들로 충족.** 오더북·틱 불필요.
- 주의: 원 공식의 정규화 상수가 자산마다 임의적이라, 크립토 이식 시 거래량 정규화 방식(본 스펙은 20봉 이동평균 대비 상대화)이 **원저자 공식과 다른 재해석**임을 명시한다. 이 재해석에 따라 결과가 달라질 수 있음.

## 스카우트 메모
- 강점: 거래량-가격 효율성(적은 거래량으로 큰 가격 이동 = "쉬운" 이동)을 정량화하는 관점이 우리 기존 지표군(볼린저·RSI·MACD 계열)과 겹치지 않는 축이라 **신호 다양화 가치**가 있음. TradingView 좋아요 3,222는 이 리서치 라운드에서 확보한 지표 중 가장 높은 참여지표.
- 의심점: (1) 정량 백테스트 전무 — QS 페이지 차단으로 확인 불가. (2) 크립토 이식 시 거래량 정규화가 우리 임의 재해석이라 원저자 의도와 괴리 가능. (3) 원 지표는 본래 **일봉 스윙용으로 설계**됐고(저자 Arms는 주식 일봉 데이터로 개발) 15m 저해상도 사용은 검증 안 된 확장 — 실제로는 [스윙]으로 4h/1d에서 먼저 검증하는 편이 원 개념에 더 충실할 수 있음(본 스펙은 단타로 태깅했으나 백테스트 시 4h 버전도 함께 비교 권장).
- 우리 단타 슬리브와의 관계: 기존 스펙 중 거래량 지표 계열(OBV·CVD·VZO·VPT 등)과 인접하나, **가격변동÷거래량 비율**이라는 계산식 자체는 신규. 백테스트 우선순위는 중간 — STARC보다는 개념 신선도가 높음.
