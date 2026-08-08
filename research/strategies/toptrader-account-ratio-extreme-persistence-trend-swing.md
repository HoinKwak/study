# [스윙] 상위 트레이더 계정비율 극단 지속기간(Persistence) 기반 추세성숙 추종

- **출처**: 개념 조합 — 자체 설계. 배경 근거(정성적): https://www.ainvest.com/news/btc-perpetual-futures-long-short-ratio-contrarian-indicator-crypto-trading-2509/ , https://www.coinglass.com/LongShortRatio (롱숏비율 일반론, 정량 수치 없음).
  **핵심 설계 아이디어의 출처는 기존 보유 스펙 `rsi-cardwell-range-shift-positive-reversal-swing.md`** — Cardwell의 "RSI가 과매수 구간에 오래 머무는 것은 페이드 신호가 아니라 강세 확인 신호"라는 통찰을 RSI가 아니라 **상위 트레이더 계정비율(`count_toptrader_long_short_ratio`)**이라는 다른 지표에 동일한 논리로 적용한 것. 기존 보유 `long-short-account-ratio-contrarian-swing.md`(극단값을 즉시 **페이드**)·`top-trader-position-ratio-smart-money-momentum-swing.md`(포지션비율 **MA 크로스**로 스마트머니 전환 추종)와 셋 다 유사한 데이터를 쓰지만 **신호 구성 로직이 서로 다름**(극단값 즉시반응 vs MA크로스 vs **지속기간(며칠 연속 극단인가)**) — 다만 데이터 소스가 겹쳐 완전한 독립 근거는 아님을 인정.
- **참여지표**: - (자체 설계, SNS 참여지표 미집계)
- **백테스트 근거**: **없음(개념 기반, 정직히 표기)**. Cardwell RSI 레인지시프트 자체도 우리 시스템에서 아직 검증(백테스트) 전 상태(미검증 대기 목록)라 이 유추의 전제 자체가 검증되지 않았음을 명확히 인지. **채택 전 자체 백테스트 필수**.
- **타임프레임**: 일봉(1d) 지속기간 판정 → 4h 진입
- **시장/대상**: BTC·ETH 위주(상위 트레이더 데이터가 안정적으로 잡히는 최상위 유동성 심볼)

## 진입 규칙
- **데이터**: `data.binance.vision/data/futures/um/daily/metrics/<SYM>/`의 일별 CSV(5분 간격, 2020-09-01부터 아카이브)에서 `count_toptrader_long_short_ratio`(상위 20% 계정, **계정 수 가중** 롱/숏 비율) 필드 사용. 1d 종가 시점(또는 1d 평균)으로 리샘플.
  - **⚠️ 인프라 신규 발견**: 이 5분 간격 `metrics` CSV 덤프에는 `sum_open_interest`(OI 계약수)·`sum_open_interest_value`(OI 명목가치 USD)·`count_toptrader_long_short_ratio`·`sum_toptrader_long_short_ratio`·`count_long_short_ratio`(글로벌 계정비율)·`sum_taker_long_short_vol_ratio`가 전부 포함돼 있고 **2020-09-01부터 현재(2026-08-07 확인)까지 매일 아카이브**돼 있다(WebFetch/curl로 실물 다운로드해 확인). 기존 `oi-volume-leverage-crowding-contrarian-swing.md`·`long-short-account-ratio-contrarian-swing.md` 등에서 "REST 엔드포인트는 최근 ~30일치만 제공해 장기 백테스트 제약"이라 적었던 문제가 **이 덤프로 해소 가능** — 백테스터가 착수 시 REST 대신 이 덤프를 우선 사용할 것을 권장(이번 스펙뿐 아니라 위 기존 OI/롱숏비율 계열 스펙 전체에 적용 가능한 인프라 팁).
- **극단 percentile**: `count_toptrader_long_short_ratio`의 최근 lookback(기본 180일) 롤링 상위/하위 pct_extreme(기본 15%)ile 계산.
- **지속기간(persistence)**: 오늘 값이 극단(상위 또는 하위 15%ile)에 위치한 날이 **persist_days(기본 5일) 연속**으로 유지.
- **롱(상승 지속확인)**: 5일 연속 **상위 극단**(상위 트레이더 계정 다수가 롱 우세 지속) **AND** 같은 구간 가격이 신고가 갱신 중(최근 20봉 고가 경신) → 이미 형성된 상승추세에 **뒤늦게 확인 후 합류**(추세 초입이 아니라 "성숙한 추세의 지속" 베팅).
- **숏**: 대칭 — 5일 연속 **하위 극단** + 신저가 갱신 중.
- **무효화**: persistence 성립 이후 비율이 중립대(percentile 40~60)로 복귀하면 진입 보류.

## 청산 규칙
- 익절: ATR(4h,14) 트레일링×2.5(추세추종형이므로 넉넉하게), 또는 비율이 반대 극단(하위 15%ile, 롱 포지션 기준)으로 전환되면 청산.
- 손절: 진입가 −ATR(4h,14)×2.0.
- 시간/조건 청산: max_hold=15일. persistence가 깨지고(중립대 복귀) 5일 내 재진입 안 되면 포지션 정리 검토.

## 파라미터
- lookback=180일 (percentile 계산 기간, 범위 90~365)
- pct_extreme=15 (범위 10~25)
- persist_days=5 (범위 3~8)
- price_confirm_lookback=20봉 (범위 15~30)
- atr_stop_mult=2.0, atr_trail_mult=2.5
- max_hold=15일 (범위 10~25)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: `count_toptrader_long_short_ratio`(위 metrics 덤프), 가격 캔들(4h/1d), ATR.
- 주의: 오더북/틱/실시간청산 불필요. `metrics` 덤프는 종목별로 상장 시점부터만 존재(신규 알트는 짧음) — BTC·ETH만 우선 검증 권장. 5분 간격 데이터를 1d로 리샘플할 때 결측(간헐적 5분봉 누락) 처리 필요.

## 스카우트 메모
- **강점**: 새로 발견한 `data.binance.vision` metrics 덤프 덕분에 **BTC 기준 약 5.8년치(2020-09~2026-08)의 5분 간격 OI·롱숏비율 데이터**를 확보할 수 있어, 이 계열(OI·롱숏비율) 전략들의 고질적 문제였던 "표본기간 제약"이 크게 완화됨 — 이 스펙뿐 아니라 기존 관련 스펙 재검증에도 활용 가치가 큼.
- **의심점(표본 빈도·독립성, 사전 명시)**: "5일 연속 극단"은 짧지 않은 조건이라 심볼당 이벤트 빈도가 낮을 것(추정 BTC 단일종목 기준 연 5~10회, 5.8년치로도 총 30~60건 수준 — 여전히 적을 수 있음). BTC·ETH 등 소수 종목만 대상으로 하면 표본이 얇아질 위험이 크고, 종목을 늘리면(알트 추가) **상위 트레이더 포지셔닝이 시장 전체에서 동조화되는 경향**이 있어(대형 트렌드 국면엔 BTC·ETH·주요알트가 동시에 상위 극단에 진입) 독립 표본 확보가 어려울 수 있음 — 과거 라운드에서 반복 확인된 매크로 클러스터링 패턴과 동일 위험.
- **gross 엣지 가설**: Cardwell의 RSI 레인지시프트 통찰("극단이 짧으면 노이즈, 오래 지속되면 구조적 레짐 전환 확인")을 상위 트레이더 계정비율에 적용한 것으로, "정교한 대형 계정들의 포지셔닝이 여러 날 한쪽으로 지속되는 것은 우연이 아니라 구조적 확신(추세 성숙)의 반영"이라는 가설. 그러나 이 유추의 전제(Cardwell 로직 자체)가 우리 시스템에서 아직 검증되지 않았고, "극단이 오래가면 오히려 과열·반전 임박"이라는 정반대 해석도 동등히 성립 가능해 **방향성이 사전에 확정되지 않음** — 백테스트 시 반드시 방향반전(페이드) 대조군을 병행 실행할 것.
- 우리 슬리브와의 관계: 기존 `top-trader-position-ratio-smart-money-momentum-swing`·`long-short-account-ratio-contrarian-swing`과 데이터 계열이 겹쳐 신호 상관관계 점검 필수(세 스펙을 동시에 채택하지 않는 것을 권장, 그 중 하나만 실제 백테스트로 검증 후 나머지는 폐기 검토). 이번 라운드 5개 중 데이터 소스 중복 위험이 가장 큰 스펙임을 인정.
