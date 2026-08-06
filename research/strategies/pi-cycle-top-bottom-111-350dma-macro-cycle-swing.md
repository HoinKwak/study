# [스윙] Pi Cycle Top/Bottom 매크로 사이클 타이밍 (111DMA/350DMA×2, 150EMA/471SMA×0.745)

- **출처**: https://www.blockchain.com/explorer/charts/pi-cycle-top-indicator (Blockchain.com 차트, **WebFetch 원문 확인 완료** — 공식 정의 문구: "A key signal occurs when the 111DMA crosses above the 350DMA x2") /
  https://www.bitcoinmagazinepro.com/charts/pi-cycle-top-bottom-indicator/ , https://charts.bitcoin.com/pi-cycle-top.html , https://newhedge.io/bitcoin/pi-cycle-top-indicator , https://www.cycletop.co/about/pi-cycle-top (Top 지표를 게시하는 주요 크립토 데이터 사이트들 — 다수 교차확인) /
  Bottom 지표: https://medium.com/@govindthanabalasingam/the-bitcoin-pi-cycle-bottom-indicator (Medium), https://www.tradingview.com/script/mtbrDHZX-Pi-Cycle-Bitcoin-Top-and-Bottom-Daily/ (TradingView 스크립트, 공식화된 계산식 명시)
- **참여지표**: 개별 좋아요/조회수 수치는 특정 게시물 형태가 아니라 집계 어려우나, **Blockchain.com·Bitcoin Magazine Pro·CoinMarketCap("Crypto Market Cycle Indicators")·bgeometrics 등 크립토 업계 주요 데이터 사이트 5곳 이상이 독립적으로 이 지표를 상시 차트로 게시**하고 있어 업계 표준 매크로 사이클 지표로서의 채택도가 매우 높음을 시사. 만든이는 Philip Swift(필립 스위프트, LookIntoBitcoin 창업자)로 알려져 있음.
- **백테스트 근거**: **정량 수치 원문 미확인** — WebFetch로 Blockchain.com 원문을 직접 확인했으나, 해당 페이지에는 **2013·2017·2021년 등 과거 고점 적중에 대한 구체적 승률·오차범위 수치가 없었음**(정의만 제시). 여러 2차 매체(블로그)가 "2013·2017·2021 고점을 근접 적중했다"고 서술하나 **1차 소스에서 구체적 수치(예: 오차일수·전체 사이클 수 대비 적중률)를 독립적으로 검증하지 못해 인용하지 않음** — 정직하게 "정량 근거 미확인, 업계 채택도(참여지표) 기반으로 분류". Bottom 지표(150EMA/471SMA×0.745)는 "2015·2018·2022년 저점 부근에서 크로스가 발생했다"는 서술만 확인(정량 수치 없음).
- **타임프레임**: 1d 캔들, 111일/350일(Top) 또는 150일/471일(Bottom) 이동평균 — **극저빈도(사이클당 1~2회 신호, 수년에 한 번)**
- **시장/대상**: BTC 무기한 전용(원 지표가 BTC 고유 사이클 특성에 기반, 알트코인 확장은 미검증)

## 진입 규칙
- **Top 신호(약세 전환/청산 경계)**: 111일 단순이동평균(SMA111)이 **350일 SMA×2(SMA350×2)를 상향 돌파**하는 순간 → 기존 롱 포지션 축소/청산 신호(신규 숏 진입 신호는 아님, 원 지표는 "고점 경계" 용도).
  - (공격적 확장, [추정] 원문 명시 아님) 크로스 발생 후 `confirm_bars`(예 3일) 동안 SMA111이 SMA350×2 위를 유지하면 확정 신호로 간주해 신규 숏 소폭 진입 검토(BTC 사이클 특성상 표본이 극소해 리스크 큼, 보수적 접근 권장).
- **Bottom 신호(강세 전환/매수 경계)**: 150일 지수이동평균(EMA150)이 **471일 SMA×0.745(SMA471×0.745)를 하향 돌파**하는 순간 → 신규 롱 진입 신호(저점권 진입).
- 두 신호 모두 **연 1~2회조차 발생하지 않는 초저빈도**이므로 단독 매매 신호보다는, 발생 시 **다른 스윙/단타 슬리브 전체의 리스크 익스포저(레버리지·포지션 크기)를 조정하는 상위 레짐 오버레이**로 우선 활용 권장.

## 청산 규칙
- 익절/포지션 관리: Top 신호 이후는 목표 익절가 없이 **단계적 익스포저 축소**(예: 신호 발생 시 전체 익스포저 50% 감축, 이후 SMA111이 SMA350×2 아래로 재하향 돌파하면 정상 복귀). Bottom 신호는 반대로 익스포저 단계적 확대.
- 손절: 개별 트레이드형 손절 개념 없음(레짐 지표) — 신호 반전(재크로스) 시 포지션 원복.
- 시간 청산: 없음(사이클 지표 특성상 보유기간이 수개월~1년 이상으로 매우 김).

## 파라미터
- top_short_ma=SMA111 (고정, 원문)
- top_long_ma=SMA350×2 (고정, 원문)
- bottom_short_ma=EMA150 (고정, 원문)
- bottom_long_ma=SMA471×0.745 (고정, 원문)
- confirm_bars=3 (범위 1~5, [추정] 원문 미명시 — 휩쏘 방지용 보완 파라미터)
- exposure_adjust_pct=50% (범위 30~70%, 신호 발생 시 익스포저 조정폭)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: SMA111, SMA350, EMA150, SMA471 — 전부 1d 종가만으로 계산 가능한 단순 이동평균. 바이낸스 REST 1d klines로 완전 구현 가능, 추가 데이터 소스 불필요.
- 난이도: **매우 낮음**(이동평균 크로스 조건 2개뿐). 단, **471일치 선행 데이터가 필요**해 워밍업 기간이 길다(바이낸스 선물 BTCUSDT 상장은 2019-09 — 471일 워밍업 후에도 실제 신호 발생 표본은 사이클 특성상 극소, 2020~2026 구간에서 많아야 1~2회 크로스 예상). 통계적 유의성 검정이 사실상 불가능한 표본 규모임을 감안하고 접근해야 함.
- 주의: 오더북/틱/펀딩/OI 등 다른 데이터 전혀 불필요 — 이번 라운드 후보 중 **데이터 요구가 가장 단순**함.

## 스카우트 메모
- **강점**: 기존 보유 매크로 사이클 계열(`btc-log-regression-risk-metric-macro-cycle-filter-swing.md`, `mayer-multiple-btc-200sma-regime-swing.md`)과 달리 **111/350일 이동평균 크로스 하나만으로 정의되는 극도로 단순한 규칙**이며, 크립토 업계에서 "가장 널리 언급되는 사이클 고점 타이밍 지표"로 통용됨(5개 이상 독립 데이터 사이트가 상시 게시) — 참여지표 기반 채택 근거는 이번 라운드 후보 중 가장 강함. 최근 화제성도 확인됨("Pi Cycle Top: The Chart Everyone Watches in 2026" 제목의 2026년 게시물 존재).
- **의심점**: **극저빈도(수년에 1회)라 우리 프레임워크로 통계적으로 유의미하게 검증하는 것 자체가 사실상 불가능**(표본 n이 1~3 수준). "단타·스윙 매매 전략"이라기보다는 **초장기 리스크 오프 신호**에 가까워 우리 봇의 매매 사이클(포지션당 수 시간~수일)과 성격이 다름 — 신호 자체를 매매 트리거로 쓰기보다는 **레버리지/포지션크기 조정용 매크로 필터**로 격하해 활용하는 편이 현실적. 기존 `btc-log-regression-risk-metric-macro-cycle-filter-swing.md`(이미 보유)와 "매크로 필터" 용도가 겹쳐 **채택 시 우선순위 낮음** — 백테스트보다는 그냥 레짐 필터로 병행 참고하는 편이 비용 대비 합리적.
- **우리 슬리브와의 관계**: 대체가 아니라 **최상위 레짐 오버레이 후보**(이미 보유한 로그회귀 리스크미터·Mayer Multiple과 유사 계층). 백테스트 우선순위는 낮게 두되, 참여지표가 높아 스펙 문서화 자체는 가치 있음.
