# [스윙] Coinbase 프리미엄 지수 연속일수(Streak) 부호전환 브레이크아웃

- **출처**: BingX Learn, "Coinbase Bitcoin Premium Index Turns Positive After 15-Day Discount, Signaling U.S. Demand
  Recovery" — https://bingx.com/en/learn/article/coinbase-bitcoin-premium-index-turns-positive-us-demand-institutional-inflows
  (**WebFetch로 원문 확인**: "15 consecutive trading days in negative territory" 이후 양전환 사례, "transitions from
  extended negative premiums to sustained positive conditions have often coincided with improving Bitcoin price
  momentum"·"historically... preceded 4-8 weeks of upward price momentum" 문구 원문 확인). 보조: CryptoRank,
  "Stablecoin Supply Ratio..." 등 코인베이스 프리미엄 관련 매체 다수(kucoin.com, news.bitcoin.com 등)가 동일
  개념을 반복 보도 — 코인베이스 프리미엄은 크립토 트레이딩 커뮤니티에서 "미국 기관 매수세 프록시"로 널리
  참조되는 지표(CryptoQuant 등 온체인 데이터 업체가 표준 지표로 제공).
- **참여지표**: - (뉴스/블로그, SNS 참여지표 미집계). 다만 코인베이스 프리미엄은 크립토 트위터(X)·온체인
  분석 커뮤니티에서 "기관 매수/매도 심리" 신호로 매우 빈번히 인용되는 지표.
- **백테스트 근거**: **없음(정성적 서술만 확인, 구체적 승률·수익률 수치 원문에 없음)** — "4-8주 상승 모멘텀
  선행 경향"은 원문이 정성적으로만 서술("often preceded")하며 표본 수·통계 검정 없음. **정량 근거 없이
  참여도(반복 보도 빈도)와 방법론 명확성만으로 채택**, 반드시 자체 백테스트 필요.
- **타임프레임**: 1d (프리미엄 부호·스트릭 계산이 일봉 기준).
- **시장/대상**: BTC 무기한(코인베이스 프리미엄은 BTC/USD 기준 지표라 BTC 단일자산 전용, 확장 시 ETH 프리미엄도
  코인베이스에서 별도 제공되므로 이식 가능).

## 진입 규칙
- **프리미엄 산출**: `premium_pct = (coinbase_BTC-USD_close - binance_BTCUSDT_close) / binance_BTCUSDT_close × 100`
  (일봉 종가 기준. 코인베이스는 USD 결제, 바이낸스는 USDT 결제라 USDT 페깅 괴리가 프리미엄에 소폭 混入되는
  구조적 한계 있음 — 스카우트 메모 참조).
- **스트릭 계산**: 매일 `premium_pct`의 부호(+/-)를 기록, 연속 동일부호 유지일수(`streak_days`) 계산.
- **롱**: `streak_days`(음수 프리미엄 연속) ≥ **10일**(원문 사례 "15일 음전환"보다 다소 완화, 범위 5~20일) 지속된
  뒤 **`premium_pct`가 0을 상향 돌파**(양전환)하는 날의 다음 봉 시가에 진입. 확인 필터: BTC 종가가 20일 SMA 위.
- **숏**([추정], 원문은 주로 롱 시그널 — 반대 방향은 대칭 가정): `streak_days`(양수 프리미엄 연속) ≥ 10일 지속 후
  0을 하향 돌파 시 진입, BTC 종가가 20일 SMA 아래일 때만.

## 청산 규칙
- **시간 청산**: 원문의 "4-8주 상승 모멘텀 선행" 문구를 그대로 목표 보유기간으로 채택 — 기본 **6주(42일)**,
  범위 4~8주(28~56일) 경과 시 강제 청산.
- **손절**: 진입가 대비 **-10%**(범위 -7%~-15%).
- **조기 청산**: 진입 후 프리미엄이 다시 반대 부호로 전환되면(모멘텀 가정 실패 신호) 시간 청산을 기다리지 않고
  즉시 청산.
- **트레일링(옵션)**: 신고가 대비 -15% 트레일링 스탑으로 시간 청산을 대체 검토 가능.

## 파라미터
- streak_threshold=10일 (범위 5~20)
- sma_trend_filter=20일
- hold_target=42일 (범위 28~56)
- stop_loss_pct=10% (범위 7~15%)
- trailing_pct=15% (옵션)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: SMA(20) 외 특별한 지표 불필요 — 스트릭 카운터는 단순 순차 로직.
- **⚠️ 신규 데이터 소스 필요**: 바이낸스 REST만으로는 구현 불가. 코인베이스 공개 스팟 API
  (`api.exchange.coinbase.com/products/BTC-USD/candles` 등, 인증 불필요)에서 BTC-USD 일봉 종가를 추가로 받아와야
  함 — 기존 인프라에 코인베이스 커넥터 신규 구축 필요(다만 CoinGecko 파생 API도 이미 우리 유니버스 산정에
  쓰이고 있어 "바이낸스 외 공개 REST 추가"가 아주 새로운 패턴은 아님).
- 주의: 오더북·틱데이터 불필요, 일봉 종가만으로 계산 가능해 API 호출량 매우 적음(하루 1회 갱신).

## 스카우트 메모
- **강점**: 크립토 트레이딩 커뮤니티에서 매우 널리 참조되는 지표(기관 자금 흐름 프록시)라 신호 신뢰도에 대한
  커뮤니티 컨센서스는 있음. 규칙 자체(스트릭+부호전환)는 명확히 코딩 가능.
- **의심점**: (1) 원문이 정량 백테스트 없이 정성적 사례("15일 음전환 후 양전환") 하나만 제시 — 표본 수 극히
  적어 일반화 여부 불확실. (2) 코인베이스 프리미엄은 최근(2024년 이후) **미국 현물 ETF 출시 이후 구조가
  달라졌을 가능성**(ETF 자금이 코인베이스 프라임을 통해 흐르며 프리미엄의 의미가 예전과 달라졌을 수 있음,
  원문 자체도 "OTC로 흐르는 기관자금은 프리미엄에 잡히지 않는다"는 한계를 명시). (3) USDT-USD 페깅 괴리가
  프리미엄 계산에 노이즈로 섞임 — USDT/USD 환율(예: Coinbase USDT-USD 페어)로 보정하는 것을 고려해야 함.
- **우리 슬리브와의 관계**: 완전히 새로운 데이터 소스(코인베이스 스팟가)를 요구하는 유일한 후보 — 기존
  `premium-index-zscore-mean-reversion-scalp.md`(바이낸스 무기한-현물 프리미엄, 즉 펀딩 베이시스)와는
  **다른 종류의 프리미엄**(거래소간 스팟 프리미엄 vs 파생상품 베이시스)이라 개념적으로 겹치지 않음. 신규
  인프라 구축 비용이 있어 백테스트 우선순위는 중간(먼저 코인베이스 API 접근성부터 확인 필요).
