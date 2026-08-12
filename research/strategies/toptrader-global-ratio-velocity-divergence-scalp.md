# [단타] 탑트레이더 vs 글로벌 계정비율 변화속도(1차 미분) 다이버전스

- **출처**: 지표 정의 — https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Long-Short-Account-Ratio (탑트레이더 계좌비율) /
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Long-Short-Ratio (글로벌 계좌비율) /
  데이터 원천 — `data.binance.vision`의 `metrics` 덤프(5분 간격, `count_toptrader_long_short_ratio`·`count_long_short_ratio` 필드, 2026-08-09 다운로드로 존재 확인 완료 — 기존 보유 `toptrader-vs-global-ratio-spread-divergence-swing.md`와 `toptrader-account-ratio-extreme-persistence-trend-swing.md` 스펙에서 이미 실물 확인된 소스 재사용).
  **핵심 차별점(기존 보유 스펙과 구분)**: 기존 `toptrader-vs-global-ratio-spread-divergence-swing.md`는 두 비율의 **레벨(수준, z-score)을 비교한 스프레드**를 4h로 본다. 본 스펙은 두 비율 각각의 **레벨이 아니라 변화속도(1차 미분, velocity)**를 짧은 창(1h)으로 비교한다 — "누가 더 롱/숏에 치우쳐 있는가"(레벨)가 아니라 "누가 더 빠르게 포지션을 바꾸고 있는가"(속도)를 보는 것으로 통계량의 종류(레벨 vs 도함수)가 다름. **이 정확한 규칙은 스카우트 자체 설계 — 외부에 이 정확한 백테스트는 없음, 지어내지 않음.**
- **참여지표**: - (자체 설계)
- **백테스트 근거**: **없음(자체 설계, 정직히 표기)**. 채택 전 자체 백테스트 필수.
- **타임프레임**: 1h 신호(5분 원본 metrics를 1h로 집계) / 15m 확인.
- **시장/대상**: BTC·ETH·BNB·SOL·XRP·DOGE·ADA 무기한.

## 진입 규칙
- 데이터: `count_toptrader_long_short_ratio`(탑트레이더 계좌수 가중 롱/숏 비율, "top"), `count_long_short_ratio`(글로벌 전체 계좌 롱/숏 비율, "global"). 5분 원본을 1h 종가 시점 값으로 리샘플.
- **정규화**: 각 시계열 롤링 z-score(`window=72`시간=3일): `z_top(t)`, `z_global(t)`.
- **속도(velocity)**: `v_top(t) = z_top(t) - z_top(t-k)`, `v_global(t) = z_global(t) - z_global(t-k)` (k=3시간).
- **속도 다이버전스**: `vel_div(t) = v_top(t) - v_global(t)`.
- **롱(스마트머니 선행 가속)**: `v_top(t) >= +vel_th`(탑트레이더가 빠르게 롱으로 쏠리는 중, vel_th=1.0표준편차) **AND** `v_global(t) <= 0`(리테일은 정체 또는 반대로 움직이는 중, 즉 아직 따라오지 않음) **AND** 15m 가격이 최근 4봉 고가 대비 -0.5% 이내(선행매집이 가격에 아직 크게 반영 안 된 초입 위치) → 롱.
- **숏**: 대칭 — `v_top(t) <= -vel_th` **AND** `v_global(t) >= 0` **AND** 15m 가격이 최근 4봉 저가 대비 +0.5% 이내 → 숏.
- **방향 미확정 명시**: "탑트레이더 가속 선행 = 스마트머니 추종" 가설이다. 정반대(탑트레이더의 급격한 방향 전환이 오히려 청산 유도용 함정이라 반전이 온다는 역발상)도 배제할 수 없어, 백테스트 시 정방향·반전 양방향 대조군 필수(과거 다수 스펙에서 반전이 우세했던 전례 다수).

## 청산 규칙
- 익절: ATR(15m,14) × 1.5 트레일링, 또는 R:R 2.0 선도달.
- 손절: 진입가 ∓ ATR(15m,14) × 1.0.
- 시간 청산: `vel_div`가 부호 반전하거나 진입 후 `max_hold=8`봉(15m, 2시간) 경과 시 청산.

## 파라미터
- z_window=72시간 (범위 48~120)
- k=3시간 (범위 1~6)
- vel_th=1.0 (범위 0.7~1.5, z-score 단위)
- price_proximity=0.5% (범위 0.3~1.0%)
- atr_trail_mult=1.5, sl_atr_mult=1.0, max_hold=8봉(15m)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: `count_toptrader_long_short_ratio`·`count_long_short_ratio`(metrics 덤프)의 롤링 z-score·1차 차분, ATR(14, 15m), 최근 N봉 고저.
- 주의: metrics 덤프가 5분 간격이라 1h 리샘플 시 어느 시점 값을 쓸지(종가 시점 vs 1h 평균) 명확히 정의 필요 — 룩어헤드 방지를 위해 **해당 1h 봉 마감 시점 이전 마지막 5분 관측치**만 사용.

## 스카우트 메모
- **예상 표본 빈도**: [추정] `vel_th=1.0σ` 조건과 `v_global<=0` 조건을 결합하면 1h 봉 기준으로도 상당히 자주(예: 시간의 15~25%) 통과할 수 있어, `price_proximity` 필터가 실질적 빈도 조절자 역할을 할 것으로 예상 — 종목당 **연 100~300건** 추정. 1차 트리거 횟수부터 세어 대조 필수.
- **전제의 내적 일관성**: `v_top`과 `v_global`은 서로 다른 모집단(대형 계좌 vs 전체 계좌)이지만, 시장 전체가 한 방향으로 급변할 때(뉴스·청산 캐스케이드)는 **두 그룹이 동시에 같은 방향으로 움직여 `v_global<=0` 조건이 오히려 잘 안 맞을 위험**(둘 다 같이 가속하면 다이버전스가 발생하지 않음) — 즉 이 신호는 "시장이 조용히 재편되는 국면"에만 나타나고 "시장이 크게 움직이는 국면"에는 오히려 안 나타날 수 있어, 트레이드당 가격 변동폭이 작은(수익 기회가 작은) 구간에 편중될 위험을 자인함.
- **엣지 대비 거래빈도**: 1h~15m 스캘프성이라 왕복수수료(0.14%) 부담이 상존 — tp_pct(ATR×1.5)가 수수료 대비 충분히 큰지 백테스트에서 실측 확인 필요.
- **독립성/클러스터링**: 탑트레이더 계좌 구성이 종목 간 상당 부분 겹칠 수 있어(대형 트레이더가 여러 종목을 동시 운용) 7종목 신호가 상관될 위험 있음 — 이벤트 단위 클러스터링 진단 권고.
- **강점**: 레벨이 아닌 속도(1차 미분)를 쓰는 것은 이 데이터 소스 계열(탑트레이더/글로벌 비율)에서 아직 시도되지 않은 축(기존 보유 3개 스펙은 레벨·지속기간·레벨스프레드만 사용) — 진짜 신규 정보일 가능성.
- **의심점**: 위 내적 일관성 우려(시장이 조용할 때만 발동)가 엣지 크기 자체를 제한할 수 있음.
- **우리 단타 슬리브와의 관계**: 라이브 `scalp15m`과 타임프레임은 겹치나(15m) 신호원(파생 포지셔닝 속도 vs 가격 볼린저 돌파)이 완전히 달라 신호 상관 낮을 것으로 기대. 기존 `toptrader-vs-global-ratio-spread-divergence-swing.md`(레벨 스프레드, 4h 스윙)와는 통계량·타임프레임이 명확히 달라 보완적.
