# [스윙] 미국 현물 BTC ETF 순유출 스트릭 컨트래리언 롱

- **출처**: https://cointelegraph.com/news/spot-bitcoin-etfs-see-record-10-day-outflow-streak-analyst-calls-it-contrarian-indicator (**WebFetch 원문 확인 완료**) /
  https://icobench.com/news/bitcoin-price-etf-outflow-streak-may-record/ , https://en.cryptonomist.ch/2026/07/22/bitcoin-etf-inflows-streak/ (WebSearch 스니펫만 확인)
- **참여지표**: 코인텔레그래프·트레이딩뷰뉴스 등 대형 매체 보도 / Santiment Intelligence(온체인 분석업체) 코멘트 인용
- **백테스트 근거**: **없음(애널리스트 코멘트 기반, 정량 백테스트 아님)**. Santiment Intelligence 원문 인용(WebFetch 확인): *"History has shown that extreme ETF outflows typically work well as a contrarian indicator, since prices move opposite to trader expectations."* 기사 내 구체 사례: **10거래일 연속 순유출, 누적 $2.97B**, 당시 BTC 약 $64,224 (기사 시점). 별도로 2025년 11월 **단일일 $904M 순유출**이 "주요 저점 근처였고 이후 가격 회복"했다는 사례가 언급됨(단, 통계적 승률·평균 반등폭 등 정량 수치는 원문에 **없음** — 정직하게 "수치 미제공"으로 표기). 2024-05-01 별도 사례(WebSearch 스니펫): 당시 사상 최대 단일일 순유출($563.7M, BTC ~$57k)이 3주 만에 BTC $67k+ 회복으로 이어졌다는 보도도 존재하나 이 역시 개별 사례 나열이지 체계적 백테스트 아님.
- **타임프레임**: 일봉(1d) 순유출입 데이터 기준, 진입 후 보유 1~3주
- **시장/대상**: BTC 무기한 (ETH 현물 ETF도 유사 데이터 존재하나 유동성·역사가 짧아 1차 대상은 BTC)

## 진입 규칙
- **데이터 소스**: 우리 인프라가 이미 `research/etf/flows.json`(시장브리핑 루틴이 매일 갱신, SoSoValue Open API 기반)으로 미국 현물 BTC ETF 일별 순유출입(USD)을 수집 중 — **신규 데이터 파이프라인 구축 불필요**, 기존 자산 재활용.
- 롱: **N=7 거래일 연속 순유출**(매일 net flow < 0) **또는** 누적 순유출이 트레일링 90일 롤링 누적유출입의 **하위 10퍼센타일**(즉 90일 기준 역사적으로 드문 수준의 유출)에 도달 시, BTC 무기한 롱 진입.
- **필터**: 스트릭 기간 중 BTC가 이미 직전 90일 고점 대비 -15% 이상 하락한 상태(패닉 심리 확인, 단순 기술적 되돌림과 구분).
- (보조, [추정] — 원문에 정량 근거 없음) 반대로 **6거래일 이상 연속 순유입**이 발생하면 신규 숏 진입은 보류(모멘텀 추종 국면 가능성) — 이 방향은 참여지표조차 약해(원문은 유출 쪽만 컨트래리언으로 명시) 채택 우선순위 낮음.

## 청산 규칙
- 익절: 진입 후 BTC가 스트릭 시작 시점 가격 대비 +8~12% 반등 시.
- 손절: 순유출 스트릭이 끝나지 않은 채 BTC가 진입가 대비 -10% 추가 하락 시(컨트래리언 가설 실패).
- 시간/조건 청산: **순유입으로 전환되는 첫 거래일** 종가 기준 청산(스트릭 반전 = 가설 실현) 또는 최대 15거래일 보유.

## 파라미터
- streak_days=7 (범위 5~10)
- rolling_percentile_window=90d, percentile_threshold=10 (범위 5~15)
- price_drawdown_filter_pct=15% (범위 10~20%)
- tp_pct=8~12%, sl_pct=10%
- max_hold_days=15

## 코딩 난이도 / 데이터 요구
- 필요한 지표: BTC 가격(바이낸스 REST) + **ETF 일별 순유출입**(바이낸스 REST 아님 — `research/etf/flows.json`을 통해 이미 별도 파이프라인으로 수집 중인 SoSoValue 기반 데이터를 그대로 활용, 신규 외부 연동 불필요).
- 주의: `research/etf/flows.json`은 시장브리핑 루틴이 "최신일만 append"하는 구조라 **결측·소급수정 이력이 없는지**(append-only 무결성) 백테스트 전 별도 검증 필요. 데이터 시작점이 ETF 출시일(2024-01)이라 표본 기간이 약 2.5년으로 제한적.

## 스카우트 메모
- **강점**: **바이낸스 REST를 벗어난 데이터**이지만 이미 우리 인프라(`research/etf/flows.json`)가 매일 수집 중이라 **추가 구축 비용이 거의 없다**는 점이 특이한 강점. 신호(스트릭 임계 도달)는 저빈도(연 수 회)라 수수료 부담이 매우 작음. 기관(ETF 투자자) 행동이라는, 우리 기존 스펙(펀딩·OI·롱숏비율 등 리테일/파생 트레이더 행태 중심)과 **참여자 유형 자체가 다른** 신규 엣지 원천.
- **의심점**: 원문 어디에도 정량 백테스트(승률·평균 수익률·표본 수)가 없어 순수 애널리스트 코멘트 수준 — "컨트래리언이 잘 통했다"는 사후 확증편향(선정적 사례만 회자)일 위험이 크다. 채택 전 자체 백테스트로 **모든 과거 스트릭 사례를 전수 조사**(선택적 사례만 보지 않기)하는 것이 특히 중요. ETF 자금 흐름 자체가 BTC 현물가에 미치는 영향력이 시간에 따라 변할 수 있음(초기엔 임팩트 컸으나 시장이 성숙하며 약화 가능).
- **우리 슬리브와의 관계**: 완전 신규 데이터 축(기관 ETF 플로우). `funding-rate-breadth-marketwide-crowding-contrarian-swing`·`long-short-account-ratio-contrarian-swing` 등 "군중 심리 컨트래리언" 계열과 철학은 유사하나(극단 포지셔닝 페이드) **대상 참여자(리테일 파생 vs 기관 현물 ETF)와 데이터 소스가 전혀 다름**.
