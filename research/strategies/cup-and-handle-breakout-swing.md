# [스윙] 컵앤핸들(Cup and Handle) 브레이크아웃 스윙

- **출처**: 고전 차트패턴(William O'Neil, "How to Make Money in Stocks" 기원). 참고 2차자료 — [QuantifiedStrategies(원문 봇검증 차단으로 본문 미확인)](https://www.quantifiedstrategies.com/cup-and-handle-trading-strategy/), [LuxAlgo 블로그 "Cup and Handle Pattern Success Rates Explained"](https://www.luxalgo.com/blog/cup-and-handle-pattern-success-rates-explained/), [Trade That Swing](https://tradethatswing.com/the-cup-and-handle-swing-trading-strategy-explosive-consistent-price-moves/), [TradingSim](https://www.tradingsim.com/blog/how-to-trade-the-cup-and-handle-pattern), [BingX 크립토 적용 가이드](https://bingx.com/en/learn/article/how-to-use-cup-and-handle-pattern-in-crypto-trading), [Phemex 아카데미](https://phemex.com/academy/cup-and-handle-pattern)
- **참여지표**: 개별 영상·게시물 조회수는 특정하지 못했으나(WebSearch 스니펫만 확인, 원문 페이지 다수가 봇차단), **컵앤핸들은 주식·크립토 기술적분석 교육 콘텐츠에서 가장 자주 반복되는 고전 패턴 중 하나**로, BingX·Phemex·Yellow·ChartScout 등 다수 크립토 거래소·교육 플랫폼이 별도 크립토 전용 가이드를 발행할 만큼 대중적 인지도가 높음(패턴 자체의 브랜드 인지도로 대체 판단).
- **백테스트 근거**: **원문 미확인(부분적으로만 확보)**. WebSearch 스니펫에서 인용된 수치(출처 불명확·2차 재인용): "3,000건 이상 표본 분석 기준 베이스라인 성공률 49%, 1년 보유 시 70%, 5년 80%, 10년 85%"라는 문구와 "손익비 2.5:1~4:1" 문구가 여러 크립토/주식 교육 사이트에 반복 인용되나, **원 저자·원 연구·표본 정의(자산군·기간·타임프레임)가 명시된 1차 출처를 찾지 못함** — 즉 출처가 불분명한 통설(anecdotal consensus)에 가깝다. QuantifiedStrategies의 전용 백테스트 페이지는 Cloudflare 봇검증에 막혀 원문 확인 실패. → **이 수치들은 신뢰도 낮은 재인용으로 취급**하고, 채택 근거는 패턴의 대중적 통용도(참여지표 대체)로 분류한다.
- **타임프레임**: 4h(컵 형성) / 1d(대형 컵) — 크립토는 주식보다 사이클이 빨라 4h를 기본으로 하고 1d는 대형 스윙용 옵션.
- **시장/대상**: BTC·ETH·주요 알트 USDT 무기한.

## 패턴 정의 (코딩용 정량화 — 원 저자 O'Neil의 주식 일봉 기준을 크립토 4h로 스케일 재해석)
- **왼쪽 림(Left Rim)**: lookback 윈도우(예 N=100봉) 내 로컬 고점(좌우 k=10봉보다 높은 프랙탈 고점).
- **컵 바닥(Cup Bottom)**: 왼쪽 림 이후 가장 낮은 저점. 컵 깊이 = `(LeftRim - CupBottom) / LeftRim`, 정상 범위 **12%~50%**(원 저자 기준은 12~33%이나 크립토 변동성 감안해 50%까지 허용).
- **둥근 바닥 형태 검증**: 컵 바닥 구간(저점 전후 각 k봉)의 가격 경로가 V자(급락-급반등)가 아니라 U자(완만한 하강-횡보-완만한 상승)인지 확인 — 컵 바닥 전후 20%~80% 구간 종가들의 2차 회귀계수(포물선 곡률)가 양수(아래로 볼록)인지로 근사 판정.
- **오른쪽 림(Right Rim)**: 컵 바닥 이후 가격이 왼쪽 림 높이의 **90%~105%** 범위로 회복한 지점.
- **핸들(Handle)**: 오른쪽 림 형성 후 나타나는 짧은 되돌림 구간. 핸들 깊이 = 컵 깊이의 **≤50%**(원 저자 기준 ≤15%가 이상적이나 크립토는 변동성이 커서 완화), 핸들 길이는 컵 형성 기간의 **1/3 이하**(예: 컵이 40봉이면 핸들은 최대 13봉).
- **핸들은 컵의 상단 절반(윗쪽) 구간에서 형성**되어야 함(핸들 저점이 컵 바닥보다 오른쪽 림에 더 가까워야).

## 진입 규칙
- 롱: 핸들 고점(≈오른쪽 림 높이)을 **종가 기준으로 상향 돌파** + 돌파봉 거래량이 직전 20봉 평균 대비 **1.5배 이상**.
- 숏(역컵앤핸들, inverse): 상승 후 위 조건을 뒤집은 형태(왼쪽 림=저점, 컵=역U자 고점 볼록, 핸들 하단 돌파)로 대칭 적용.

## 청산 규칙
- 익절(목표): 측정이동(Measured Move) = 컵 깊이(가격폭) 만큼을 돌파 지점에서 더한 값. 즉 `TP = BreakoutPrice + (LeftRim - CupBottom)`.
- 손절: 핸들 저점 아래(롱 기준) 또는 오른쪽 림 아래 ATR(14)×0.5 버퍼.
- 시간/조건 청산: 돌파 후 목표 도달 전 재차 핸들 범위 안으로 종가 마감하면(가짜 돌파) 즉시 손절 처리.

## 파라미터
- fractal_k=10 (범위 5~15, 좌우 몇 봉보다 높아야 프랙탈 고점/저점)
- lookback_bars=100 (범위 60~150, 컵 탐색 윈도우, 4h 기준 약 17~25일)
- cup_depth_min=0.12, cup_depth_max=0.50 (범위 고정, 원 저자 기준 완화)
- rim_symmetry_tol=0.10 (오른쪽 림이 왼쪽 림의 ±10% 내)
- handle_depth_ratio_max=0.50 (컵 깊이 대비)
- handle_len_ratio_max=0.33 (컵 길이 대비)
- breakout_vol_mult=1.5 (범위 1.2~2.0)
- measured_move_mult=1.0 (범위 0.7~1.5, TP 스케일 조정용)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 프랙탈 스윙고저(OHLC만으로 계산), 2차 회귀(곡률) 판정용 종가 시계열, 거래량 이동평균, ATR. **전부 바이낸스 REST 캔들로 충족.**
- 난이도: **중~높음**. 고정 지표 크로스와 달리 "패턴 인식"이라 여러 조건(깊이·대칭·곡률·핸들 위치)을 동시에 만족해야 신호가 발생 — 파라미터 조합에 따라 신호 빈도가 극히 낮아지거나(과도한 조건) 너무 자주 오탐(느슨한 조건)될 위험. 룩어헤드 방지에 특히 주의(오른쪽 림·핸들 완성 여부를 봉 마감 시점에서만 판정해야 함).
- 오더북·틱·실시간청산 불필요.

## 스카우트 메모
- 강점: 저빈도·고R 지향(측정이동 목표가 통상 진입폭보다 커서 R 배수가 큼) — 스윙 슬리브의 "매매당 R 크게, 빈도 낮게" 요구에 부합. 우리 레포에 순수 차트패턴 인식형이 `darvas-box-breakout-swing`, `vcp-volatility-contraction-breakout-swing`, `wyckoff-spring-upthrust-accumulation-swing`, `bull-flag-measured-move-breakout-swing` 등 이미 있으나 **"둥근 바닥(U자) + 얕은 핸들" 조합은 겹치지 않는 별개 패턴**.
- 의심점: (1) 인용된 승률(49~85%) 수치의 1차 출처를 찾지 못해 신뢰할 수 없음 — 정직하게 "원문 미확인"으로 표기함. (2) 패턴 정의 자체가 원래 주관적("difficult to define with strict buy and sell rules"라고 QS도 인정)이라, 본 스펙의 정량화(곡률 회귀·깊이 %)는 우리가 임의로 규칙화한 근사이며 다른 방식으로 코딩하면 신호가 크게 달라질 수 있음. (3) 조건이 많아 4h 크립토 데이터에서 신호가 극소수(연 몇 건)일 가능성 — 백테스트 시 표본부족(FAIL 처리) 리스크가 특히 큼.
- 우리 단타 슬리브와의 관계: 무관(스윙 전용). 기존 `bull-flag-measured-move-breakout-swing`(깃발형 되돌림)과 신호 로직·목표산정 방식이 유사한 "측정이동 브레이크아웃" 계열이라 **함께 묶어 비교 백테스트**하면 개발 비용을 아낄 수 있음(공유 가능한 프랙탈·측정이동 유틸리티).
