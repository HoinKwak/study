# [스윙] 상위 트레이더 포지션비율(사이즈가중) 스마트머니 추세추종

- **출처**: https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Top-Long-Short-Position-Ratio
  (바이낸스 공식 API 문서, `topLongShortPositionRatio` — **포지션 규모 가중**, 계정 수 가중인 `topLongShortAccountRatio`와 다른 필드) /
  https://smartmoneyapi.com/resources/strategies/whale-watching-strategy (Smart Money API, 고래 추종 전략 프레임) /
  https://www.coinglass.com/LongShortRatio (CoinGlass, 상위트레이더 비율 시각화 표준)
- **참여지표**: 없음(정량 SNS 참여지표 미집계) — "스마트머니(상위 트레이더) 포지셔닝을 리테일과 구분해 추종"하는 프레임은 크립토 파생 커뮤니티에서 광범위하게 통용.
- **백테스트 근거**: 없음(개념 기반). **채택 전 자체 백테스트 필수.**
- **타임프레임**: 4h~1d
- **시장/대상**: BTC·ETH 위주(상위 트레이더 데이터가 안정적으로 잡히는 최상위 유동성 심볼)

## 진입 규칙
- 지표: 바이낸스 `topLongShortPositionRatio`(상위 트레이더, **포지션 명목가 가중** — "스마트머니"로 간주) vs `globalLongShortAccountRatio`(전체 계정, **계정 수 가중** — "리테일"로 간주).
- **핵심 차별점(기존 `long-short-account-ratio-contrarian-swing.md`와의 로직 차이)**: 기존 스펙은 계정 수 기준 극단값을 **페이드(컨트래리언)**하는 반면, 본 전략은 포지션 규모 기준 상위 트레이더 비율이 **추세를 형성**할 때 그 방향을 **추종(모멘텀)**한다 — 신호 극성이 반대(역추세 vs 순추세)이고 사용 필드도 다름(계정 수 가중 vs 포지션 규모 가중).
- `topLongShortPositionRatio`의 `ratio_ma_fast`(예 6봉, 4h=1일) 이동평균이 `ratio_ma_slow`(예 18봉=3일) 이동평균을 상향 돌파(상위 트레이더가 순매수로 전환 중) **AND** 같은 시점 `globalLongShortAccountRatio`는 하락 또는 횡보(리테일은 따라오지 않음, "스마트머니가 리테일보다 먼저 움직임" 확인) → **롱**.
- 대칭: `topLongShortPositionRatio` MA가 하향 돌파 + `globalLongShortAccountRatio` 상승/횡보 → **숏**.
- 확인 필터: 방향과 같은 부호로 24h 거래대금이 최근 20봉 평균 대비 `volume_confirm_mult`=1.2배 이상(무의미한 저유동성 구간 크로스 배제).

## 청산 규칙
- **익절**: `topLongShortPositionRatio` MA 크로스가 반대 방향으로 재발생하면 청산(추세 소진 판정), 또는 목표 R:R `rr_target`=2.5:1 도달.
- **손절**: 진입가 기준 −1.5×ATR(4h, 14).
- **시간 청산**: `max_hold_bars`=42봉(4h×42=7일) 내 목표 미도달 시 시간청산.

## 파라미터
- ratio_ma_fast=6 (4h 기준, 범위 4~8)
- ratio_ma_slow=18 (4h 기준, 범위 12~24)
- volume_confirm_mult=1.2 (범위 1.0~1.5)
- atr_mult_sl=1.5 (범위 1.0~2.0)
- rr_target=2.5 (범위 2.0~3.0)
- max_hold_bars=42 (4h 기준, 범위 30~60)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 바이낸스 파생 마켓데이터 `topLongShortPositionRatio`, `globalLongShortAccountRatio`, 24h 거래대금, ATR. 이동평균 크로스 로직은 단순.
- **⚠️ 데이터 주의**: 기존 `long-short-account-ratio-contrarian-swing.md`와 동일하게 REST 실시간 조회는 **최근 30일치만 제공** → 장기 백테스트는 `data.binance.vision/data/futures/um/daily/metrics/` 일별 덤프를 써야 함. 이 덤프에 `sum_toptrader_long_short_ratio`(계정수 기준)만 있고 **포지션 규모 가중 컬럼(`topLongShortPositionRatio`에 해당)이 별도로 있는지는 미확인** — 백테스트 착수 전 metrics 덤프의 컬럼 스키마를 먼저 확인해야 함(없으면 계정수 가중 컬럼으로 대체하거나 전략 자체가 장기 검증 불가할 수 있음, 정직히 표기).
- 난이도: 낮음(이동평균 크로스 + 필터). 단, 위 데이터 컬럼 가용성 확인이 선행 과제.

## 스카우트 메모
- **강점**: 기존 `long-short-account-ratio-contrarian-swing.md`가 이미 "선택 필터"로 언급만 하고 넘어간 **상위트레이더 vs 리테일 다이버전스**를 별도의 완결된 순추세 전략으로 구체화. 극단값 페이드가 아니라 **추세 형성 자체를 신호**로 쓰므로 "이미 FAIL 확정된 z-score/단순 평균회귀 오실레이터 계열"과 메커니즘이 다름(모멘텀 크로스오버 구조).
- **의심점**: 정량 백테스트 근거 전무, 원 아이디어가 기존 스펙에 하위 옵션으로 이미 언급돼 있어 **완전한 신규성보다는 "동일 데이터의 반대 방향 가설(모멘텀 vs 컨트래리언)을 별도 검증"**에 가까움 — 채택 시 기존 컨트래리언 버전과 신호 상관관계·수익률을 나란히 비교해 어느 쪽이 실제 엣지가 있는지 판별 필요. `sum_toptrader_long_short_ratio` 컬럼이 계정수 기준일 경우, 원래 의도한 "포지션 규모 가중" 신호를 정확히 재현하지 못할 리스크 있음(데이터 확인 선행 필수).
- **우리 슬리브와의 관계**: 기존 `funding-oi-price-triple-confirm-carry-momentum-swing.md`(펀딩·OI·가격 방향 일치 확인) 등 다른 순추세 스윙 전략과 카테고리는 겹치나 데이터 소스(포지셔닝 비율)가 달라 **보완재**.
