# [스윙] 탑트레이더 포지션비율 vs 글로벌 계정비율 스프레드 (스마트머니-리테일 다이버전스)

- **출처**: 개념 배경 — https://www.sharpe.ai/futures/long-short-ratio (Sharpe.ai, "Global long/short positioning across Binance, Bybit, OKX plus top-trader ratios"라는 기능 소개만 확인, **WebFetch로 원문 확인했으나 구체적 방법론·백테스트·지표 정의는 페이지에 없음** — 랜딩페이지 수준) /
  지표 정의 — https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Trader-Long-Short-Ratio (탑트레이더 포지션비율, `sum_toptrader_long_short_ratio`) /
  https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Long-Short-Ratio (전체계정 롱숏비율, `count_long_short_ratio`) — **본 전략의 정확한 스프레드/다이버전스 규칙 자체는 스카우트가 자체 설계한 것**(외부에 이 정확한 백테스트는 없음, 지어내지 않음).
- **참여지표**: - (자체 설계). "탑트레이더 vs 리테일 다이버전스"라는 개념 자체는 파생상품 데이터 플랫폼(Sharpe.ai, Coinglass 등)이 공통적으로 강조하는 프레임이나, 이 정확한 스프레드 규칙의 SNS 반응 데이터는 없음.
- **백테스트 근거**: **없음(자체 설계, 정량 근거 지어내지 않음)**. **주의: 이 스펙은 지표 정규화·조합 배제 원칙과 다른 성격임을 명시** — 배제 대상은 "동일 가격 시계열에서 파생된 여러 기술지표를 정규화해 조합"하는 계열(더블볼린저+RSI50 등, 정보가 사실상 중복돼 gross부터 무엣지였던 전례 다수)이다. 본 스펙은 **서로 다른 데이터 소스**(대형 계좌의 포지션 규모 가중 비율 `sum_toptrader_long_short_ratio` vs 전체 계좌의 계좌수 가중 비율 `count_long_short_ratio`)를 비교하는 것으로, 이미 보유한 `top-trader-position-ratio-smart-money-momentum-swing.md`(탑트레이더 단독 레벨)·`long-short-account-ratio-contrarian-swing.md`(글로벌 단독 레벨)·`toptrader-account-ratio-extreme-persistence-trend-swing.md`(탑트레이더 계좌수비율 지속성)와도 **다른 축**(둘의 스프레드/괴리)이라는 점에서 신규.
- **타임프레임**: 4h 신호(5분 원본 데이터를 4h로 집계, 스윙 슬리브).
- **시장/대상**: BTC·ETH·BNB·SOL·XRP·DOGE·ADA 무기한. **`metrics` 덤프에서 7종목 전부 데이터 존재를 직접 다운로드로 확인 완료**(2026-08-09, `https://data.binance.vision/data/futures/um/daily/metrics/<SYM>/...zip`, 5분 간격, 2020-09~현재 — 기존 OI/롱숏비율 계열 스펙들이 반복 지적한 "REST 30일 제한" 문제 해소).

## 진입 규칙
- **정규화(비교 가능하게만 사용, 신호 조합 아님)**: 각 시계열을 독립적으로 롤링 z-score화.
  - `z_top = (sum_toptrader_long_short_ratio - rolling_mean(N)) / rolling_std(N)`
  - `z_global = (count_long_short_ratio - rolling_mean(N)) / rolling_std(N)`
  - `spread = z_top - z_global` (양수면 탑트레이더가 글로벌 계정보다 상대적으로 더 롱 편향 = "스마트머니가 리테일보다 매수 확신 큼", 음수면 반대).
- 롱: `spread[i] >= spread_th`=+1.5 **AND** 가격이 최근 `price_box_lookback`=20봉(4h) 박스 상단의 `proximity_pct`=1.5% 이내(돌파 임박 위치 확인, 스프레드만으로 진입하지 않음) → 롱.
- 숏: `spread[i] <= -spread_th` **AND** 가격이 최근 20봉 박스 하단 1.5% 이내 → 숏.
- **방향 미확정 명시**: 위는 "스마트머니 추종(順)" 가설이다. 대조 가설(탑트레이더가 리테일보다 롱일 때 오히려 리테일 청산을 노린 함정이라 반전이 온다는 역발상)도 배제할 수 없으므로, 백테스트 시 **정방향과 반전(spread 부호 반대)을 반드시 함께 비교**해야 한다(과거 다수 스펙에서 반전이 오히려 우세했던 전례 있음).

## 청산 규칙
- 익절: R:R `rr_target`=2.5 또는 spread가 0으로 복귀(다이버전스 해소) 중 먼저 도달하는 쪽.
- 손절: 진입가 ∓ ATR(14,4h) × `atr_sl_mult`=2.0.
- 시간 청산: `max_hold`=20봉(4h×20=80h) 내 목표 미도달 시 강제청산.

## 파라미터
- zscore_window(N)=180봉(4h 기준 약 30일, 범위 90~360)
- spread_th=1.5 (범위 1.0~2.0)
- price_box_lookback=20봉 (범위 10~30)
- proximity_pct=1.5% (범위 1.0~3.0%)
- atr_sl_mult=2.0 (범위 1.5~3.0)
- rr_target=2.5 (범위 2.0~3.5)
- max_hold=20봉(4h 기준)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: `metrics` 덤프의 `sum_toptrader_long_short_ratio`·`count_long_short_ratio`(5분 간격 → 4h 리샘플, 마지막값 또는 평균 방식 결정 필요), 캔들 OHLC, ATR14.
- 주의: **metrics 덤프를 신규으로 파싱하는 인프라 구축 필요**(기존 백테스터가 이 필드를 아직 안 썼다면 신규 로더 작성 필요 — 컬럼 확인 완료: `create_time,symbol,sum_open_interest,sum_open_interest_value,count_toptrader_long_short_ratio,sum_toptrader_long_short_ratio,count_long_short_ratio,sum_taker_long_short_vol_ratio`). 과거 라운드에서 XRP/DOGE/ADA 등 일부 종목·구간에 0-fill 결측이 있었던 사례(OI캐피출레이션 스펙) 있으므로 **결측 처리(0-fill 오염 배제)를 반드시 선행 검증**.

## 스카우트 메모
- **예상 표본 빈도**: zscore 극단(|spread|≥1.5)은 상시 발생하는 조건이 아니며, 여기에 가격 박스 근접까지 요구하므로 [추정] 종목당 월 1~3회 수준(실측 필요). 4.5년 히스토리(2020-09~현재)로 표본모수 자체는 확보 가능하나, 실제 트리거 수는 훨씬 적을 수 있음.
- **독립성 위험 — 매우 큼**: 탑트레이더 vs 리테일 포지셔닝 괴리는 시장 전체의 레버리지 사이클과 강하게 연동되는 매크로적 성격의 지표라, 신호가 여러 종목에서 동시에 뜰 가능성이 높음(과거 OI/펀딩/롱숏비율 계열 스펙 전부가 이 문제로 명목표본이 부풀려졌음). **백테스트 착수 시 이벤트(일자) 단위 클러스터링 진단을 최우선**으로 수행 권고, 고유 이벤트 수가 명목거래 수 대비 크게 적을 것으로 예상.
- **gross 엣지 가설**: 대형 계좌(탑트레이더)는 정보 우위·자금력이 있어 포지셔닝이 선행지표일 수 있다는 것이 통용되는 가설이나, 검증된 정량 근거는 없음(위 백테스트 근거 항목 참조). 반대로 "탑트레이더 데이터 자체가 소수 계좌 표본이라 노이즈가 크다"는 반박도 가능 — 실증 전 확신 낮음.
- **7종목 신호 충분성**: 4.5년치 5분 데이터가 7종목 전부 존재 확인됨(다운로드 검증 완료) — 유니버스 정의 문제(직전 라운드의 거래대금 순위이동 함정)와는 무관. 다만 신호 발생 자체가 종목별 레버리지 사이클 참여도에 따라 편차 클 수 있음(예: DOGE/ADA는 개인투자자 비중이 높아 글로벌 계정비율의 노이즈가 더 클 가능성).
- **강점**: 기존 30일 REST 제한 문제를 해소하는 신규 데이터 인프라(`metrics` 벌크 덤프) 활용 사례 — 향후 다른 OI/롱숏비율 계열 재검증에도 재사용 가능한 로더 구축 기회.
- **의심점**: 클러스터링 위험이 스펙 단계에서 이미 명백해 보임(직전 3개 라운드 FAIL의 공통 원인). 정방향/반전 대조군 비교가 필수이며, 이를 생략하면 과거 "허위 PF" 실수를 반복할 위험 있음.
