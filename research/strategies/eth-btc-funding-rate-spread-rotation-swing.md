# [스윙] ETH/BTC 펀딩레이트 스프레드 상대모멘텀 로테이션

- **출처**: 개념 배경 — https://www.bybit.com/en/learn/crypto-insight/bearish-positioning-builds-across-crypto-derivatives (Bybit Learn, "펀딩레이트는 자산별 레버리지 수요·포지셔닝 쏠림을 반영하며 자산 간 편차가 존재" 서술, WebFetch 접근 대신 WebSearch 스니펫으로 확인) /
  https://hedgeco.net/news/05/2026/ethereum-vs-bitcoin-divergence.html (HedgeCo, ETH-BTC 파생 포지셔닝 괴리 사례, 스니펫 수준) — **"ETH 펀딩이 BTC 펀딩과 구조적으로 다르게 움직일 수 있다"는 정성적 관찰만 확인, 이 정확한 스프레드 매매 규칙·정량 수치는 어디에도 없음(스카우트 자체 설계, 지어내지 않음)**.
  데이터 정의 근거: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Get-Funding-Rate-History (`fundingRate`, 8h 주기) — `data.binance.vision/data/futures/um/monthly/fundingRate/<SYM>/`에 **BTCUSDT·ETHUSDT 전용 벌크 덤프가 2020-01부터 존재**함을 직접 확인(2026-08-12, S3 리스팅 curl로 158개 월별 zip 확인).
- **참여지표**: - (자체 설계). "ETH/BTC 펀딩 괴리"라는 프레임 자체는 파생 데이터 업계(Bybit·Deribit Insights 등)가 정성적으로 자주 언급하나 이 정확한 규칙의 SNS 반응 데이터는 없음.
- **백테스트 근거**: **없음(자체 설계, 정량 근거 지어내지 않음)**. **⚠️ 축 중복 여부 명시**: 기존 `btc-eth-zscore-spread.md`(로그**가격** 스프레드 평균회귀, 페어 마켓뉴트럴)·`ethbtc-relative-strength-trend-breakout-swing.md`(ETH/BTC **가격**비율 추세추종 브레이크아웃)와 데이터 소스가 다르다 — 이 둘은 모두 **가격** 시계열만 쓰지만, 본 스펙은 **펀딩레이트**(레버리지 포지셔닝 비용) 스프레드를 신호원으로 쓰고 방향 판단에만 가격을 보조 필터로 사용한다. **다만 두 자산의 가격이 서로 강하게 동행(상관 통상 0.7~0.9)하므로 펀딩 스프레드도 가격 모멘텀과 일부 겹칠 위험이 있다 — 백테스트 시 반드시 "펀딩 게이트 없이 순수 ETHBTC 가격모멘텀만 쓴 대조군"(=기존 ethbtc-relative-strength 스펙과 동형) 대비 부가가치를 확인할 것**(직전 라운드 게이트 무가치 교훈 반영).
- **타임프레임**: 8h 펀딩 데이터를 4h 봉으로 정렬해 신호 산출(스윙 슬리브). 단일 종목(ETHUSDT) 방향성 포지션만 취함(BTC 동시 매매·헤지비율 불필요 — 페어 트레이딩 아님, 구현 단순).
- **시장/대상**: ETHUSDT 무기한 단독(BTC는 신호 계산용 참조 자산으로만 사용, 실제 포지션 없음).

## 진입 규칙
- `spread(t) = fundingRate_ETH(t) - fundingRate_BTC(t)` (bp 단위, 8h 정산마다 갱신, 00:00/08:00/16:00 UTC).
- 롤링 z-score: `z(t) = (spread(t) - rolling_mean(spread, W)) / rolling_std(spread, W)`, W=90봉(8h×90=30일). **최소표본 요건: rolling_mean/std는 표본 수가 W(90) 미만이면 계산하지 않고 신호도 산출하지 않는다(초기 30일은 워밍업, 소표본 밴드폭 왜곡 방지 — 직전 라운드 band_std 소표본 함정 교훈 직접 반영)**.
- **롱(ETH 상대 숏 스퀴즈 기대)**: `z(t) <= -spread_th`(=-1.5, ETH 펀딩이 BTC보다 상대적으로 훨씬 낮음/음수 = ETH만 숏 쏠림) **AND** ETHUSDT 4h EMA50 기울기가 상방 또는 수평 이상(급격한 하락추세 중 역추세 진입 배제) → 롱.
- **숏(ETH 상대 롱 과열 페이드)**: `z(t) >= +spread_th`(ETH 펀딩이 BTC보다 상대적으로 훨씬 높음 = ETH만 롱 쏠림) **AND** ETHUSDT 4h EMA50 기울기 하방 또는 수평 이하 → 숏.
- **방향 미확정 명시**: 위는 "ETH 특이적 쏠림은 과열이며 평균회귀한다"는 컨트래리언 가설이다. 대조 가설(ETH 펀딩 프리미엄 확대가 오히려 ETH 강세 지속의 선행신호라는 추세추종 해석)도 배제 못하므로 **백테스트 시 정방향·반전을 반드시 병행 비교**(과거 다수 스펙에서 반전이 우세했던 전례 있음).

## 청산 규칙
- 익절: R:R `rr_target`=2.2 또는 `z(t)`가 0 부근(±0.3)으로 정상화되는 시점 중 먼저 도달.
- 손절: 진입가 ∓ ATR(14, 4h) × `atr_sl_mult`=2.0.
- 시간 청산: `max_hold_bars`=30봉(4h×30=5일) 초과 시 강제청산.

## 파라미터
- zscore_window(W)=90봉(8h 기준, 범위 60~180)
- spread_th=1.5 (범위 1.0~2.0)
- atr_sl_mult=2.0 (범위 1.5~3.0)
- rr_target=2.2 (범위 1.8~3.0)
- max_hold_bars=30 (4h 기준, 범위 20~50)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: `fundingRate` 덤프(BTCUSDT·ETHUSDT, 8h) + ETHUSDT 캔들(4h, EMA50) + ATR(14,4h). 오더북/틱/실시간청산 불필요.
- 주의: `fundingRate` 덤프는 8h 간격이라 4h 관리봉과 정렬 시 값 유지(forward-fill, 다음 정산 전까지 동일 spread 값 사용) 처리 필요. 신규 로더 필요(기존 백테스터가 이 전용 덤프를 아직 안 썼다면 파싱 코드 추가).

## 스카우트 메모
- **예상 표본 빈도**: |z|>=1.5는 대략 정규분포 가정 시 양측 약 13%대이나 스프레드 자체가 자기상관(persistence)이 커서 연속 여러 정산에 걸쳐 조건이 유지되는 "에피소드" 단위로 뭉칠 가능성 높음 — 트레이드는 재진입 쿨다운(동일 국면 내 1회만) 적용 시 [추정] 연 15~30건(EMA 필터로 추가 감소). 실측 필요.
- **독립성**: 단일 종목(ETHUSDT)만 매매하므로 종목 간 클러스터링 문제는 없음. 다만 스프레드 자체가 시장 전체 레버리지 사이클(예: 2024 반감기 랠리, 2022-11 FTX)에 연동돼 **연도별로 국면이 몰릴 위험**은 있음 — LOO 대신 연도별 분해 진단 권고.
- **강점**: 페어 헤지비율(β) 추정·공적분 검정이 필요 없어 기존 `btc-eth-zscore-spread.md`보다 구현이 훨씬 단순. 신규 전용 데이터 소스(`fundingRate` 벌크 덤프) 확보로 향후 다른 펀딩 스펙의 장기 정밀 백테스트에도 재사용 가능(기존 다수 펀딩 스펙은 premiumIndexKlines에서 간접 추정했을 가능성 있음 — 이 덤프는 정산 시점 실제 확정 펀딩값이라 더 정확).
- **의심점**: ETH·BTC 펀딩은 상당 부분 공행(둘 다 시장 전체 레버리지 사이클을 반영)하므로 스프레드가 순수 "ETH 특이적" 신호인지, 단순 노이즈 차감인지 불분명 — 위에 명시한 "가격모멘텀 단독 대조군" 비교가 핵심 검증 포인트.
- **우리 슬리브와의 관계**: 완전 신규 데이터축(펀딩 스프레드) 기반 단일종목 스윙. 기존 ETH/BTC 관련 2개 스펙(가격 z-score 페어, 가격비율 브레이크아웃)과 상호 보완적 대조군 역할 가능(셋을 함께 백테스트하면 "가격 vs 펀딩 어느 쪽이 ETH/BTC 로테이션에 더 유효한 정보인지" 비교 가능).
