# [스윙] 테이커 매도체결량 절대서지 × OI 방향 사분면 반전 (캐피출레이션 vs 신규숏 구분)

- **출처**: 개념 프레임 — "OI 증감 × 가격방향" 4사분면(상승OI+상승가=신규롱 확신, 상승OI+하락가=신규숏 확신,
  하락OI+상승가=숏스퀴즈, 하락OI+하락가=롱 캐피출레이션) 자체는 파생시장에서 널리 통용되는 정성적 프레임 —
  https://www.sharpe.ai/learn/futures-open-interest ("Rising OI confirms the price move, while falling OI
  signals exhaustion or forced unwinds... when open interest is falling but price is moving in the opposite
  direction, positions are being squeezed" — WebFetch 대신 WebSearch 요약이나 표현이 명확하고 통설과 일치),
  https://www.coinbase.com/learn/advanced-trading/what-is-open-interest-in-crypto-trading ("rising OI + rising
  price = bullish... falling OI + falling price = long capitulation" 취지 서술). **이 두 출처 모두 "가격방향"을
  축으로 쓰는 사분면 설명뿐이고, 정량 백테스트 수치는 전무 — 인용 안 함, 정직히 "정량근거 없음"으로 표기.**
  **본 스펙의 차별점**: 표준 프레임은 4사분면의 한 축이 **가격방향**인데, 본 스펙은 그 자리에 **테이커 매도
  체결량의 절대 레벨(서지 여부)**을 쓴다 — "가격이 하락했다"가 아니라 "매도 주도 체결이 이례적으로
  몰렸다"는 원인계(체결 흐름) 정보로 사분면을 재구성해, 가격 캔들 방향만으로는 구분 안 되는 "완만한 하락
  + 매도체결 집중"과 "완만한 하락 + 매도체결 분산" 국면을 나눈다. 기존 보유 스펙과의 차별화(2026-08-17,
  `taker.*sell`·`매도체결`·`capitulation`·`quadrant`·`사분면` 키워드로 360개 전수검색): `oi-capitulation-multiday-deleveraging-reset-swing.md`(FAIL 확정, git 이력)는 **3일 누적 가격 ROC(-10%)+OI ROC(-15%)** 임계치 조합이라
  가격 레벨 변화가 트리거 축이다. `macd-oi-directional-confluence-swing.md`·`oi-price-expansion-confluence-trend-continuation-scalp.md`는
  OI와 가격(또는 MACD)의 방향 일치/불일치를 본다. `funding-volatility-quadrant-regime-swing.md`·
  `rrg-relative-rotation-graph-altcoin-quadrant-swing.md`는 사분면 개념은 같으나 축이 각각 펀딩변동성·상대모멘텀이라
  전혀 다른 데이터. `position-taker-flow-divergence-squeeze-scalp.md`(FAIL 확정)는 계좌수비율 vs 포지션가치비율
  괴리이지 테이커 매도**량**이 아니다. **테이커 매도체결량(절대 레벨, z-score)을 OI 방향(부호)과 조합한 사분면은
  기존 스펙에 없음, 신규 확인.**
- **참여지표**: - (자체 설계, 참여지표 없음)
- **백테스트 근거**: **없음(자체 설계, 정직히 표기)**. 채택 전 자체 백테스트 필수.
- **타임프레임**: 4h 신호(OI·거래량 모두 4h 리샘플) / 1d EMA50 확인.
- **시장/대상**: BTC·ETH·BNB·SOL·XRP·DOGE·ADA 무기한(표준 7종목, metrics·klines 전량 확인된 종목).

## 진입 규칙
- **테이커 매도체결량**: `sell_quote_vol(t) = quote_asset_volume(t) - taker_buy_quote_asset_volume(t)`
  (klines 8번째 필드 − 11번째 필드, 4h 리샘플 시 각각 구간 합산 후 차감).
- **매도서지 z-score**: 종목별 롤링 `zscore_window`=90봉(4h, 15일) 기준 `sell_z(t) = zscore(sell_quote_vol(t))`.
- **OI 방향**: `metrics` 덤프 `sum_open_interest`의 4h 구간 차분 `ΔOI(t) = sum_open_interest(t) - sum_open_interest(t-1)`,
  부호만 사용 `oi_dir(t) = sign(ΔOI(t))`.
- **사분면 판정**:
  - **캐피출레이션(롱 청산 소진)**: `sell_z(t) >= sell_th`=2.0 **AND** `oi_dir(t) = -1`(매도 폭주인데 OI는 줄어듦
    = 기존 롱 포지션이 강제청산되며 청산된 것이지 신규 숏이 쌓인 게 아님) → **롱 반전 후보**.
  - **분산/신규숏(추세지속)**: `sell_z(t) >= sell_th`=2.0 **AND** `oi_dir(t) = +1`(매도 폭주와 함께 OI도 증가
    = 신규 숏 포지션이 적극적으로 쌓이는 중) → **숏 추세추종 후보**.
- **롱 진입**: 캐피출레이션 사분면 성립 봉 이후 `confirm_bars`=2봉 이내 종가가 신호봉 고가 상향 돌파 → 롱.
- **숏 진입**: 분산/신규숏 사분면 성립 봉 이후 `confirm_bars`=2봉 이내 종가가 신호봉 저가 하향 돌파 → 숏.
- 1d EMA50: 캐피출레이션(롱)은 1d EMA50과 무관하게 허용(바닥 반전 포착이 목적), 분산/신규숏(숏)은 1d EMA50
  아래일 때만 허용(하락추세 내 지속 확인, 상승장 역행 숏 배제).

## 청산 규칙
- 익절: 캐피출레이션(롱)은 R:R `rr_cap`=2.5 목표. 분산/신규숏(숏)은 ATR(14,4h)×`atr_trail_mult`=2.0 트레일링.
- 손절: 캐피출레이션 롱 = 신호봉 저가 − ATR(4h,14)×0.8. 분산/신규숏 숏 = 신호봉 고가 + ATR(4h,14)×1.0.
- 시간 청산: `max_hold_bars`=42봉(4h×42=7일) 내 미도달 시 강제청산.

## 파라미터
- zscore_window=90봉(범위 60~150)
- sell_th=2.0 (범위 1.5~2.5)
- confirm_bars=2 (범위 1~4)
- rr_cap=2.5 (범위 2.0~3.5)
- atr_trail_mult=2.0 (범위 1.5~2.8)
- atr_stop_mult_cap=0.8, atr_stop_mult_short=1.0
- max_hold_bars=42 (범위 30~60)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: klines `quote_asset_volume`·`taker_buy_quote_asset_volume`(4h 리샘플 합산), `metrics` 덤프
  `sum_open_interest`(4h 구간 차분), EMA50(1d), ATR(14,4h).
- 주의: **REST/`data.binance.vision`으로 완전 구현 가능**(오더북·틱·실시간청산 불필요). `metrics` 덤프는
  일별 zip으로만 존재(월별 zip 없음, 2026-08-17 curl로 `daily/metrics/.../....zip`=200, `monthly/metrics/...`=404
  재확인). 2022년 일부 구간 0-fill 결측 이력이 있으므로(과거 여러 스펙에서 반복 확인) 결측 처리 선행 검증 필요.

## 스카우트 메모

### 사전 검증 체크리스트 (필수 요건 9종)
1. **구현 가능성**: klines 표준 필드 + `metrics` 일별 덤프만으로 완전 구현. 오더북 심도·틱·실시간 청산
   스트림 불필요.
2. **예상 신호 빈도(사전 명시)**: `sell_z>=2.0`는 정규분포 근사 시 상위 ~2.3%. 4h봉 기준(연 2,190봉) 순수
   통계로는 종목당 연 [추정] **~50건**이 매도서지 조건 단독 발생 예상. 여기에 OI 방향 이분(대략 50:50 가정)과
   confirm_bars 돌파 조건, 1d EMA50 필터(숏만)를 곱하면 캐피출레이션(롱)은 종목당 연 [추정] **10~25건**,
   분산/신규숏(숏)은 필터가 더 붙어 [추정] **5~15건**으로 추산. 실측이 이 범위의 10배 이상/10분의 1 이하로
   벗어나면(예: sell_z 임계 도달 즉시 자동으로 특정 oi_dir이 동반되는 정의결함, 혹은 confirm_bars 돌파 조건이
   상시 참) 최우선 점검 대상.
3. **전제의 내적 일관성 사전 검토**: 매도체결량 급증과 가격 하락은 강하게 동조하는 경향이 있어(매도 우세면
   대개 가격도 밀림), 캐피출레이션/분산 두 사분면이 실제로는 "가격 하락폭"의 크기 차이(급락 vs 완만한 하락)를
   재서술하는 것일 위험이 있다 — **oi_dir이 sell_z와 독립적인 정보를 주는지, 아니면 sell_z가 큰 봉은
   구조적으로 항상 같은 oi_dir을 동반하는지(예: 매도서지 봉의 80% 이상이 OI 감소를 동반)를 백테스트
   1단계에서 반드시 실측 보고**. 만약 한쪽 oi_dir이 매도서지 조건에서 90% 이상 편중되면 사분면 자체가
   허구(실질적으로 1개 사분면만 존재)이므로 설계 폐기.
4. **동어반복 점검**: `sell_z`가 기존 표준 지표(거래량 z-score 전체, ATR%, taker_buy_ratio)의 재포장이
   아님을 확인하기 위해 ① `sell_quote_vol` z-score와 전체 `quote_asset_volume` z-score(매수+매도 구분 없는
   단순 거래량 급증)의 **상관계수**를 계산 — 0.9 이상이면 "매도 분리"가 무의미(단순 거래량 서지의 재포장).
   ② `sell_z`와 봉 수익률(방향)의 신호시점 일치율 — 매도서지 봉이 항상 음봉이면 taker 데이터 없이도 캔들
   방향만으로 재현 가능하다는 뜻이라 정보가치 낮음(일치율 90% 이상이면 폐기 검토).
5. **정보원 무력화 대조군(필수 실행)**: `sell_quote_vol` 계열을 종목별로 랜덤 셔플(같은 종목·기간 내 봉
   순서를 무작위 재배치)한 대조군을 20개 생성해 채택안의 성과 백분위를 산출 — 채택안이 셔플 분포 하위권이면
   "매도체결 정보"가 도움이 아니라 해로 판정(Weis Wave 선례와 동일 절차).
6. **종목 간 신호 상관 사전 명시**: 매도서지는 시장 전체 패닉/급등락 시(2022-05 루나, 2022-11 FTX, 2024-08
   글로벌 매도 등) 다수 종목에서 동시에 나타날 가능성이 높음 — [추정] 동시진입일 비율 **20~40%**로 예상
   (OI캐피출레이션 계열 선례와 유사한 매크로 클러스터링). 백테스트 시 고유(일 단위) 이벤트 재집계, top-N
   이벤트 제거, LOO 필수.
7. **유니버스 정의 검증**: 표준 7종목 전량 klines·`metrics` 존재 기확인(기존 다수 스펙에서 반복 검증됨,
   재검증 불필요). 고정 7종목이라 2023~2025 신흥 알트(SUI·WLD 등)는 미포함 — 다만 본 전략은 개별 종목
   단위 트리거(횡단면 로테이션 아님)라 유니버스 확장에 구조적 장애는 없음(추후 확장 검토 가능, 채택 여부와
   무관).
8. **사전 폐기 조건**: (a) sell_z 조건에서 oi_dir 편중이 90% 이상이면 사분면 허구로 폐기, (b) 셔플 대조군
   백분위가 하위 50% 이하면 정보원 무력화 실패로 폐기, (c) gross PF가 IS·OOS 어느 한쪽이라도 1 미만이면
   폐기, (d) 동시진입일 비율 40% 초과 + top-3 이벤트 제거 시 순익 반전되면 매크로 클러스터 착시로 폐기.
9. 외부 인용(sharpe.ai·coinbase)은 정성적 사분면 프레임 설명 확인 목적으로만 사용, 정량 수치는 원문에도
   없어 인용하지 않음 — 지어내지 않음.

- 강점: OI-가격 사분면이라는 널리 알려진 정성적 프레임을, "가격방향" 대신 "테이커 매도체결 강도"라는 원인계
  데이터로 재구성한 것이 신규 축. 두 서브모드(캐피출레이션 반전 vs 분산 추세추종)가 상반된 논리라 부분 채택
  여지도 있음.
- 의심점: 내적일관성 우려(매도서지-OI방향 편중)가 최대 리스크 — 이게 실패하면 사분면 전체가 무의미.
  매크로 클러스터링 위험도 OI캐피출레이션 선례를 고려하면 상당히 큼.
- 우리 단타 슬리브와의 관계: 무관(4h~7일 스윙). 기존 OI 계열 다수가 FAIL인 점을 감안해 기대치는 보수적으로
  잡되, "가격방향 대신 테이커 매도량"이라는 축 자체는 검증 안 된 조합이라 시도 가치 있음.
