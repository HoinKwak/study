# [단타] COIN-M vs USDT-M 평균체결규모(ATS) 괴리 스캘프

- **출처**: 자체 설계 — 데이터 필드 근거: (a) USDT-M `data.binance.vision` klines `quote_asset_volume`/`count`
  (기존 `average-trade-size-*` 계열에서 이미 실물 확인 완료), (b) **신규**: COIN-M `data.binance.vision`
  klines (`data/futures/cm/{monthly,daily}/klines/<SYM>USD_PERP/<TF>/`, 8/17~19 라운드에서 이 컨테이너의
  fapi 지역차단 우회용으로 개통 확인된 데이터소스)의 `volume`(계약수)·`count`(체결건수). 오늘(2026-08-20)
  `s3-ap-northeast-1.amazonaws.com/data.binance.vision` 버킷 리스팅을 직접 조회해 COIN-M PERP 심볼이
  기존에 알려졌던 "7개"보다 훨씬 많은 **약 48종**(BTCUSD_PERP·ETHUSD_PERP·BNBUSD_PERP·SOLUSD_PERP·
  XRPUSD_PERP·DOGEUSD_PERP·ADAUSD_PERP 등 우리 표준 7종목 전부 포함)임을 실측 확인 — 스냅샷의 "7개
  퍼프 심볼"은 표준 7종목 백테스트 유니버스와의 교집합을 말한 것으로 추정되며, 실제 가용 심볼 풀은
  더 넓다(이번 신규 확인 사실, 지어내지 않음).
  개념적 근거: 바이낸스 공식 블로그(https://www.binance.com/en/blog/futures/the-pros-and-cons-of-coin--usdtmargined-contracts-how-do-they-impact-your-returns-421499824684901012,
  WebFetch로 원문 확인)가 "마이너·장기 투자자는 COIN-margined 계약이 이상적이다(If you are a miner or
  a long-term investor, this is ideal for you)", "마이너·장기 투자자는 보유자산을 USDT로 바꾸지 않고도
  헤지할 수 있다"고 명시 — **COIN-M은 코인 보유자·헤저 비중이, USDT-M은 스테이블코인 기반 리테일
  투기자 비중이 상대적으로 높을 것**이라는 참여자 구성 차이 가설의 1차 근거(단, 이 원문에 정량
  수치·백테스트는 없음 — 정성적 주장만 인용).
  기존 보유 스펙과의 차별점(2026-08-20, "coinm"·"coin-m"·"average.trade.size"·"ATS" 키워드로 387개
  전수검색): 기존 COIN-M 계열(`coinm-liquidation-snapshot-cascade-gate-scalp`·`coinm-usdtm-basis-
  volatility-regime-gate-trend-swing`·`coinm-usdtm-funding-rate-divergence-contrarian-swing`·
  `coinm-usdtm-oi-coin-denominated-growth-divergence-rotation-swing`·`usdtm-coinm-perp-basis-spread-
  meanreversion-swing`)는 전부 **베이시스·펀딩·OI** 축만 다뤘고, 기존 ATS 계열(`average-trade-size-
  accumulation-breakout-swing`·`-collapse-exhaustion-reversal-swing`·`-zscore-regime-gate-trend-swing`)은
  전부 **USDT-M 단일 소스**만 다뤘다. **"두 마진통화 간 평균체결규모(참여자 구성 프록시) 괴리"를
  다루는 스펙은 기존에 없음** — 이 프로젝트에서 유일하게 통과선(net PF≥1.3)에 근접했던 ATS 축을,
  아직 결합되지 않은 COIN-M 신규 데이터소스에 이식한 것.
- **참여지표**: - (자체 설계, 참여지표 없음)
- **백테스트 근거**: **없음(자체 설계, 정직히 표기)**. 채택 전 자체 백테스트 필수.
- **타임프레임**: 15m 신호 / 1h 확인 (라이브 `scalp15m`과 동일 해상도).
- **시장/대상**: BTC·ETH 우선(COIN-M 유동성 최상위), BNB·SOL·XRP·DOGE·ADA는 COIN-M 유동성 확인 후 확장
  (표준 7종목 전부 COIN-M PERP 존재는 확인됐으나 15m 해상도에서 `count`가 충분히 조밀한지는 미검증).

## 핵심 아이디어
`ATS(t) = quote_asset_volume(t) / count(t)`(USDT-M)와 `ATS_coinm(t) = volume(t) / count(t)`(COIN-M,
계약수/체결건수 — 계약 액면가가 종목별로 고정 상수이므로 시계열 z-score 목적상 USD 환산 없이도 비례
관계 보존)를 **동일 15m 봉**에서 각각 90봉 롤링 z-score화한 뒤 `gap(t) = z_ats_coinm(t) - z_ats_usdtm(t)`를
계산한다. `gap`이 양의 극값으로 상승 전환(코인마진 쪽 체결규모가 USDT마진 쪽보다 상대적으로 급격히
커짐 = 헤저/장기보유자 비중 있는 자금이 활발해짐)하는 순간을 "스마트머니 상대적 활성화" 게이트로 써서,
1h EMA20 추세 방향의 15m 모멘텀 진입에 필터를 건다.

## 진입 규칙
- `z_ats_usdtm(t)`, `z_ats_coinm(t)`: 각각 90봉(15m×90=22.5h) 롤링 z-score.
- `gap(t) = z_ats_coinm(t) - z_ats_usdtm(t)`.
- **롱**: `gap(t)`가 직전 봉 대비 `+1.2`를 상향 돌파(레벨이 아니라 **크로싱**, 상태전이 시에만 1회 발화)
  **AND** 종가가 1h EMA20 위 **AND** 신호봉(15m) 종가>시가 → 롱.
- **숏**: 대칭 — `gap(t)`가 `-1.2`를 하향 돌파 **AND** 종가가 1h EMA20 아래 **AND** 신호봉 종가<시가 → 숏.

## 청산 규칙
- 익절: R:R `rr_target`=1.5.
- 손절: 진입가 ∓ ATR(14,15m) × `atr_mult`=1.2.
- 시간 청산: `max_hold_bars`=16봉(15m×16=4h) 내 미도달 시 강제청산. `gap(t)`가 반대 부호로 재차 1.2를
  돌파하면(가설 무효화) 조기 청산.

## 파라미터
- zscore_window=90봉 (범위 60~180)
- gap_threshold=1.2 (범위 0.8~2.0, 크로싱 기준)
- atr_mult=1.2 (범위 1.0~2.0)
- rr_target=1.5 (범위 1.2~2.5)
- max_hold_bars=16 (범위 8~24)

## 예상 신호 빈도
- [추정] `gap` 크로싱(레벨 아닌 상태전이)은 두 독립적 z-score 스프레드의 임계 돌파 이벤트라 레벨
  체류보다 훨씬 드물다. 유사 구조(z-score 크로싱+방향필터+시가/종가 확인)인 `average-trade-size-
  zscore-regime-gate-trend-swing`이 4h에서 종목당 연 ~75건이었던 것을 참고하되, 본 스펙은 4h가 아닌
  **15m**이라 봉 수가 16배 많은 대신 `count`(특히 COIN-M 쪽)가 15m 해상도에서 훨씬 노이즈가 커
  z-score 자체의 변동성이 커진다 — 두 효과가 상쇄될 가능성이 높다고 보고 **종목당 연 200~500건**으로
  잠정 추정(BTC·ETH 기준, 알트는 COIN-M count 희소성으로 더 낮거나 계산 불가할 수 있음). **백테스터는
  실측 COIN-M 15m count 분포(특히 0 또는 결측 비율)부터 최우선 보고할 것** — 만약 알트 COIN-M 15m
  count가 대량 0/결측이면 그 종목은 유니버스에서 제외.

## 비용 감당 산술 (손익분기 승률)
- 왕복 수수료 0.14%, `rr_target`=1.5, `atr_mult`=1.2 가정. BTC 15m 평균 ATR%를 약 0.30%로 근사하면
  1R(=1.2×ATR%) ≈ 0.36%. `cost_R = 0.14% / 0.36% ≈ 0.389`.
- `wr* = (1 + cost_R) / (1 + rr_target) = (1 + 0.389) / (1 + 1.5) ≈ 55.6%`.
- 즉 **승률이 약 56%를 넘어야 비용을 감당**한다 — 15m 해상도치고는 높은 요구치(같은 계열 4h 스윙
  스펙의 42%대보다 부담이 큼)이며, 이는 15m 저ATR 구간의 구조적 약점이다. 이 산술은 가정된 ATR·R:R
  하의 이론치이며 **백테스트 착수 시 실측 ATR·실현 승률로 재계산 필수**. 만약 실측 승률이 이 근처거나
  밑돌면 즉시 폐기 후보(사전 폐기조건 참조).

## 전제의 내적 일관성
- 결합 조건: (1) `gap` 크로싱 (2) 1h EMA20 추세 방향 일치 (3) 신호봉 시가/종가 방향 일치. (1)과 (2)는
  독립적 데이터 소스(체결규모 비율 vs 가격 추세)라 상호배타적이지 않을 것으로 예상하나, **강한 추세
  구간(브레이크아웃)에서는 통상 거래대금·체결건수가 양쪽 마진통화에서 동시에 급증**해 `gap`이 오히려
  0 근처로 수렴할 위험이 있다(둘 다 커지면 z-score 차이는 상쇄) — 즉 "가장 신호가 필요한 강추세
  구간에서 게이트가 오히려 덜 발화할 수 있다"는 자기잠식 가능성을 사전에 인지한다. **검증 방법**:
  백테스터는 1h EMA20 기울기 상위 20% 구간(강추세)에서의 `gap` 크로싱 발생률을 하위 80% 구간과
  비교해, 강추세 구간에서 발생률이 유의하게 낮으면(자기잠식) 이 필터 조합의 근본 결함으로 기록한다.

## 정규화 게이트 논증
- `z_ats_usdtm`·`z_ats_coinm` 각각은 자기 자신의 과거 분포 대비 상대적 위치라 정보와 무관하게 발화하지
  않는다고 보기 어렵다(순수 노이즈로도 일정 비율 임계 초과가 나온다는 것은 기존 여러 라운드에서
  반복 확인된 함정). 다만 본 스펙은 **레벨이 아니라 두 독립 z-score의 차이(gap)의 크로싱**을 쓰므로,
  두 소스가 서로 독립(또는 낮은 상관)이라면 `gap`의 크로싱 빈도는 각 z-score 단독보다 이론상 더
  낮고 더 정보성이 있어야 한다. **검증**: 백테스터는 COIN-M ATS z-score와 USDT-M ATS z-score의
  상관계수를 먼저 계산해 보고한다 — 상관이 0.7 이상이면(사실상 같은 신호를 두 번 보는 것) `gap`
  게이트의 신규성이 무의미해지므로 사전 폐기조건에 해당.

## 수익 인과 경로
- 가설(약함, 정성적): COIN-M 참여자(헤저·장기보유자 비중 상대적으로 높음, 바이낸스 자체 설명)가
  ATS를 상대적으로 늘리는 시점은 이들이 능동적으로 포지션을 재조정하는 시점이고, 이는 리테일
  중심(USDT-M) 시장보다 정보 우위가 있을 수 있다는 통설을 근사한다. 이 경우 **손해 보는 쪽은
  뒤늦게 같은 방향으로 진입하는 USDT-M 리테일 추격매수/매도자**, **이익 보는 쪽은 신호 발생 직후
  진입하는 본 전략**이다. 이 인과 경로는 검증되지 않은 약한 가설이며(원문 자체가 정량 근거 없이
  정성적 설명만 제공), 대안 가설로 "ATS 괴리는 단순히 COIN-M의 낮은 유동성으로 인한 노이즈"일
  가능성도 동등하게 열어둔다 — 대조군(아래)으로 구분한다.

## 종목 간 신호 상관 예상
- BTC·ETH COIN-M PERP는 유동성이 높아 신호가 상대적으로 안정적일 것으로 예상되나, 두 종목 모두
  "코인마진 참여자 구성"이라는 공통 메커니즘을 공유해 **매크로 리스크온/오프 국면에 동시 발화할
  위험이 중간~높음**으로 예상한다(과거 여러 라운드에서 매크로 클러스터링이 반복 확인된 패턴).
  LOO는 참고용으로만 쓰고 "2종목 모두 통과"를 "독립 검증 2회"로 과대해석하지 않는다.

## 라이브 실행 가능성
- COIN-M·USDT-M 둘 다 klines는 표준 REST/`data.binance.vision`으로 실시간 계산 가능. `openInterestHist`
  류 30일 제한과 무관(OI 미사용). 다만 **라이브 실전 반영 시 COIN-M은 우리 봇이 거래하지 않는 별도
  상품**이므로, 이 스펙은 **COIN-M을 신호원(참고 지표)으로만 쓰고 실제 주문은 USDT-M 위에서 낸다**
  — 실시간으로 COIN-M mark/klines를 추가로 폴링해야 하는 구조적 의존성이 생기며, COIN-M API 가용성
  (지역차단·레이트리밋)이 USDT-M과 별도로 확인돼야 한다는 점을 명시.

## 사전 폐기조건 (사후 변경 금지)
- (a) `z_ats_coinm`과 `z_ats_usdtm`의 상관이 0.7 이상, 또는
- (b) 강추세 구간(1h EMA20 기울기 상위 20%)에서 `gap` 크로싱 발생률이 나머지 구간 대비 유의하게
  낮음(자기잠식 확인), 또는
- (c) 실측 승률이 위 손익분기 승률(≈56%, 실측 ATR로 재계산한 값) 대비 유의하게 낮음, 또는
- (d) BTC·ETH 외 COIN-M 15m `count` 결측/0 비율이 30% 초과(데이터 신뢰성 부족)
이면 FAIL로 폐기한다.

## 코딩 난이도 / 데이터 요구
- 필요한 지표: USDT-M klines `quote_asset_volume`·`count`, COIN-M klines `volume`(계약수)·`count`,
  EMA20(1h), ATR(14,15m). 추가 REST 엔드포인트 불필요(둘 다 klines 표준 응답).
- 주의: COIN-M zip 덤프의 컬럼 순서가 USDT-M과 동일한지(8번째 필드가 quote_asset_volume이 아니라
  base_asset_volume, 즉 코인 수량) **반드시 컬럼 스키마를 먼저 실물 확인**할 것 — 다른 라운드에서
  반복된 "필드 오인" 함정과 같은 클래스의 리스크. 오더북/틱/실시간청산 불필요.

## 스카우트 메모
- **강점**: 이 프로젝트에서 유일하게 통과선 근접 결과를 낸 ATS 축을, 아직 결합되지 않은 신규
  데이터소스(COIN-M)에 적용한 조합 — "아직 안 쓰인 조합"이라는 이번 라운드 요구에 가장 직접적으로
  부합. COIN-M 심볼 풀이 예상보다 넓다는 것도 이번에 새로 확인한 사실.
- **의심점**: 15m 해상도에서 COIN-M `count`의 노이즈·희소성이 핵심 리스크(사전 폐기조건 (d)).
  또한 "gap 크로싱"이라는 이중 z-score 차분 구조는 개념은 깔끔하지만 실전에서 순수 노이즈 차분일
  위험이 이 스펙의 가장 근본적인 취약점이다.
- **우리 슬리브와의 관계**: `scalp15m`과 동일 해상도(15m/1h)라 대체·보완 후보로 바로 비교 가능. 다만
  COIN-M 데이터 폴링이라는 신규 라이브 의존성이 생겨, 채택 시 인프라 비용이 추가된다.
