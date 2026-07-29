# SuperTrend AI (K-Means 클러스터링 적응형 팩터) [스윙]

- **출처**: LuxAlgo "SuperTrend AI (Clustering)" — https://www.luxalgo.com/library/indicator/supertrend-ai-clustering/ (개념 설명),
  TradingView 스크립트 https://www.tradingview.com/script/wP7WWjLL-SuperTrend-AI-Clustering-LuxAlgo/ (원본 Pine 스크립트·참여지표),
  보조 https://www.luxalgo.com/blog/ai-driven-trading-the-next-generation-of-market-indicators/
- **참여지표**: TradingView 스크립트 페이지 기준 **좋아요/부스트 165, 조회수 28.5K, 댓글 139**(WebFetch로 원문 확인). LuxAlgo 자체 지표 라이브러리 중 상위권 인지도.
- **백테스트 근거**: 없음(원문에 정량 수익률·승률·PF 수치 없음, 참여지표+개념 근거). 원문은 "성과 지표(performance index)"를 신호 강도 해석용으로 제공할 뿐, 별도 백테스트 결과표는 게시되지 않음.
- **타임프레임**: 4h 신호 / 1d 확인(원 스크립트는 임의 TF에서 동작하나, 수수료 대비 R을 위해 스윙 TF 채택).
- **시장/대상**: BTC·ETH·주요 알트 무기한.

## 핵심 아이디어
표준 SuperTrend(ATR 배수 팩터)를 **여러 팩터값에 대해 동시에 계산**하고, 각 팩터별로 "최근 그 팩터가 추세를 얼마나 잘 맞췄는지"를 성과 점수로 누적한 뒤, **1차원 K-Means(군집 3개: 상/중/하)**로 팩터들을 성과별로 묶어 **성과가 가장 좋은 군집의 평균 팩터**를 그 시점의 "채택 팩터"로 동적으로 선택한다. 고정 배수 SuperTrend보다 국면(변동성 레짐)에 적응적이라는 것이 핵심 주장.

## 진입 규칙
1. ATR(atr_len=10) 계산.
2. 팩터 후보군 `factors = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]` 각각에 대해 SuperTrend 라인 계산.
3. 각 팩터 f의 성과 점수(지수가중): `perf[f]_t = perf[f]_{t-1} + (1/perf_alpha) * ( sign(close_t - close_{t-1}) * sign(close_{t-1} - supertrend[f]_{t-1}) - perf[f]_{t-1} )`, perf_alpha=10(가중 반감기 조절).
4. **매 4h 봉마다** perf 값들에 대해 1차원 K-Means(k=3, max_iter=50)를 실행해 3개 군집(고/중/저 성과)으로 분류.
5. **최고 성과 군집**에 속한 팩터들의 평균값 = `target_factor`. `target_factor`로 계산한 SuperTrend를 "채택 라인"으로 사용(팩터가 매 봉 급변하지 않도록 간단한 지수평활 `factor_t = factor_{t-1} + 0.3*(target_factor - factor_{t-1})` 적용 권장 — 원 스크립트의 안정화 로직 근사).
6. **롱**: 채택 SuperTrend 라인이 하락추세(라인이 가격 위)에서 **상승추세로 전환**(종가가 라인을 상향 돌파)한 시점.
7. **숏**: 반대로 라인이 상승추세에서 하락추세로 전환(종가가 라인을 하향 돌파)한 시점.
8. (선택 필터) 최고 성과 군집의 평균 perf 값이 0 이상(양의 성과)일 때만 신호 채택 — 음수면 그 국면에서 SuperTrend 자체가 안 맞고 있다는 뜻이므로 스킵.

## 청산 규칙
- 익절: 별도 고정 목표 없음 — **추세추종형(stop-and-reverse)**. 반대 방향 전환 시그널이 나올 때까지 보유.
- 손절: 채택 SuperTrend 라인 자체가 트레일링 스탑 역할(라인 재돌파 시 청산). 초기 손절은 진입봉 ATR(10)×target_factor.
- 시간 청산: 없음(라인 추종형이므로 국면이 지속되면 장기 보유 가능).

## 파라미터
- atr_len=10 (범위 7~14)
- factors=[1.0~5.0, step 0.5] (9개 후보, 범위/step 조정 가능)
- perf_alpha=10 (범위 5~20, 클수록 성과 반영 느림)
- n_clusters=3 (고정), max_iter=50
- cluster_choice="best" (최고 성과 군집 채택, 원 스크립트는 average/worst 선택도 지원하나 본 스펙은 best 고정)
- 재클러스터링 주기=매 봉(4h)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: ATR, 다중 팩터 SuperTrend 9개 병렬 계산, 1차원 K-Means(직접 구현 또는 numpy/scipy 간단 구현 가능 — sklearn 불필요, 1D라 정렬 기반 근사 가능).
- 주의: **계산량이 큼**(팩터 9개 × 매 봉 재클러스터링)이나 전부 캔들 OHLC 기반이라 바이낸스 REST klines만으로 완전 구현 가능. 오더북/틱 불필요. **코딩 난이도는 상(k-means 로직 자체 구현 필요, 원 Pine 스크립트의 정확한 성과지표 정규화식은 재현 근사치임을 유의)**.

## 스카우트 메모
- 강점: 기존 보유 SuperTrend 계열(`pmax-most-supertrend-ma-trailing-scalp`, `triple-supertrend-ema-adx-consensus-swing`)은 **고정 배수** SuperTrend인 반면, 이건 **국면 적응형 배수 선택**이 핵심 차별점 — 레짐 전환기(고변동성→저변동성 등)에 더 잘 버틸 가능성. 참여지표(28.5K 조회수)도 준수.
- 의심점: 원 Pine 코드 미공개 세부 정규화식(성과지표 스케일링)이 있어 본 스펙은 **근사 재현**임을 명확히 해야 함 — 백테스트 시 원 스크립트와 신호가 정확히 일치하지 않을 수 있음. 정량 성과 근거가 전무해 순수 참여지표+개념 신뢰. 계산 비용이 커 실전 워커 부하 고려 필요.
- 우리 스윙 슬리브와의 관계: **부분 대체 후보**. 기존 슈퍼트렌드/RSI 라이브 전략과 컨셉 계열이 같지만 "적응형 팩터 선택"이라는 신규 메커니즘이라 교차검증 가치 있음. 채택 시 기존 고정배수 슈퍼트렌드와 신호 상관도 먼저 확인 권장.
