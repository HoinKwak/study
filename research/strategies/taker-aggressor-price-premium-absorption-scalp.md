# [단타] 테이커 매수/매도 평균체결가 프리미엄 급변 흡수 리버설 스캘프

- **출처**: 자체 설계(스카우트 고안) — 데이터 필드 근거: 바이낸스 선물 klines 표준 응답
  (`taker_buy_base_asset_volume`=10번째 필드, `taker_buy_quote_asset_volume`=11번째 필드, `quote_asset_volume`=8번째
  필드, `volume`=6번째 필드; https://developers.binance.com/docs/derivatives/usds-margined-futures/market-data/rest-api/Kline-Candlestick-Data ,
  2026-08-13 `data.binance.vision` 덤프에 전 필드 정상 존재 curl 확인). 개념적 배경(오더플로우 불균형이 단기
  가격에 영향을 준다는 통설)은 학술·업계 자료로 뒷받침됨 — arXiv "Explainable Patterns in Cryptocurrency
  Microstructure"(https://arxiv.org/html/2602.00776v1), arXiv "To Make, or to Take..."(https://arxiv.org/html/2502.18625v1,
  "테이커 전략은 수수료 부담으로 단독 알파보다 실행/미시구조 신호로 유용" 취지 서술 — WebSearch 요약 확인, 본
  전략 고유의 정량 백테스트는 아님). **이 전략 자체를 백테스트한 외부 자료는 찾지 못함 — 정직히 자체 설계로 표기**.
  기존 보유 스펙과의 차별점(중복 방지 확인, 2026-08-13 `taker_buy`·`quote_asset_volume`·`vwap_pos` 키워드로 320개
  전수검색): `candle-vwap-position-exhaustion-reversal-scalp.md`는 **전체 체결(매수+매도 구분 없음)의 평균가격
  위치**(`quote_asset_volume/volume`)를 캔들 고저 범위 내에서 어디 있는지 단일 스냅샷으로 본다. 본 스펙은
  **테이커 매수 주도 체결과 테이커 매도 주도 체결을 분리**해 각각의 평균 체결가를 구하고, 그 **차이(프리미엄)가
  시계열로 얼마나 이례적으로 벌어지는지(z-score)** 를 본다는 점에서 메커니즘이 다르다(단일 캔들의 기하학적
  위치가 아니라 두 참여자군의 체결가 격차의 시계열 이상치).
- **참여지표**: - (자체 설계, 참여지표 없음)
- **백테스트 근거**: **없음(자체 설계, 정직히 표기)**. 채택 전 자체 백테스트 필수.
- **⚠️ 예상 신호 빈도**: 15m봉 기준 `|premium_z|>=2.5` AND 캔들 몸통비율<=0.35(흡수형 캔들) 이중조건. [추정]
  종목당 **연 200~500건** 수준으로 예상(캔들VWAP소진 스펙보다는 드물 것으로 추정 — z-score 임계라 표본 특성상
  정규분포 근사 시 |z|>=2.5는 약 1.2%인데 15m봉이 연 약 35,000개이므로 순수 통계로는 연 400건 내외가 자연스러운
  기준선. 실측이 이 기준의 5배 이상 벗어나면 프리미엄 스프레드 계산에 구조적 편향(예: 저유동성 시간대 분모
  왜소화)이 있다는 신호로 간주해 우선 점검).
- **⚠️ 전제의 내적 일관성 사전 검토(가장 중요)**: 테이커 매수 평균가(`buyer_avg = taker_buy_quote_vol/taker_buy_base_vol`)는
  구조적으로 스프레드(ask 근접 체결) 때문에 테이커 매도 평균가(`seller_avg = (quote_vol-taker_buy_quote_vol)/(volume-taker_buy_base_vol)`,
  bid 근접 체결)보다 **평상시에도 약간 높게 나올 가능성**이 있다 — 이는 진짜 신호가 아니라 스프레드의 기계적
  산물일 수 있다. 이 편향을 제거하기 위해 **레벨이 아니라 프리미엄의 롤링 z-score(자기 정규화)만 신호로
  쓴다** — 채택 전 반드시 프리미엄의 무조건부 분포(레벨)가 0 근처에서 대칭인지, 아니면 상시 양의 편향을
  갖는지부터 실측 확인 필요(양의 편향이 크면 z-score 정규화가 이를 얼마나 상쇄하는지도 함께 확인).
- **⚠️ 종목 간 신호 상관 사전 예상**: 단일 캔들 내부 미시구조 이벤트라 종목별로 독립적으로 발생할 가능성이
  높다고 예상(연동 낮음). 다만 시장 전체가 패닉성 급락/급등할 때는 다수 종목에서 동시에 극단적 흡수 캔들이
  나타날 수 있음 — 동시진입일 비율을 반드시 실측 보고.
- **⚠️ 핵심 대조군(반드시 실행)**:
  ① 기존 `candle-vwap-position-exhaustion-reversal-scalp`(테이커 구분 없는 전체 평균가격 위치)와 나란히 비교해
  테이커 분리가 부가가치를 내는지 확인.
  ② `premium_z` 부호만 쓰고 캔들 몸통비율 조건을 뺀 버전(흡수 필터 무가치 여부 확인).
  ③ 프리미엄을 z-score 정규화 없이 원시 레벨로 쓴 버전(레벨 자체가 이미 유효한지, 정규화가 실제로 필요한지 확인).
- **⚠️ 사전 폐기 조건**: (a) 프리미엄 레벨이 상시 큰 양의 편향을 가져 z-score로도 제거 안 되면 정의결함으로
  폐기, (b) 대조군①(캔들VWAP포지션) 대비 부가가치 없으면(gross PF 통계적으로 구분 불가) 중복 전략으로 폐기,
  (c) gross PF<1.05면 즉시 폐기.
- **타임프레임**: 15m 신호 산출 / 1h EMA20 확인.
- **시장/대상**: BTC·ETH·BNB·SOL·XRP·DOGE·ADA 무기한(표준 7종목).

## 진입 규칙
- **테이커 매수 평균가**: `buyer_avg(t) = taker_buy_quote_asset_volume(t) / taker_buy_base_asset_volume(t)`
  (`taker_buy_base_asset_volume=0`이면 스킵).
- **테이커 매도 평균가**: `sell_base(t) = volume(t) - taker_buy_base_asset_volume(t)`,
  `sell_quote(t) = quote_asset_volume(t) - taker_buy_quote_asset_volume(t)`,
  `seller_avg(t) = sell_quote(t)/sell_base(t)` (`sell_base=0`이면 스킵).
- **프리미엄(bps)**: `premium_bps(t) = (buyer_avg(t) - seller_avg(t)) / close(t) * 10000`.
- **프리미엄 z-score**: 최근 100봉(15m) 롤링 평균·표준편차로 `premium_z(t) = (premium_bps(t) - mean100)/std100`.
- **캔들 몸통비율**: `body_ratio(t) = |close(t)-open(t)| / (high(t)-low(t))` (`high=low`면 스킵).
- **숏(매수 프리미엄 흡수 실패)**: `premium_z(t) >= 2.5` **AND** `body_ratio(t) <= 0.35` (테이커 매수가 큰 프리미엄을
  지불했는데도 캔들이 거의 안 움직임 = 매수 압력이 흡수됨) → 숏.
- **롱(매도 프리미엄 흡수 실패)**: `premium_z(t) <= -2.5` **AND** `body_ratio(t) <= 0.35` → 롱.
- 1h 확인: 1h EMA20 기울기가 진입 방향과 뚜렷하게 반대(강한 상위TF 추세 역행)면 신호 스킵.

## 청산 규칙
- 익절: ATR(14, 15m) × 1.6 트레일링, 또는 R:R 1.4 목표 도달.
- 손절: 신호봉의 반대쪽 극값(숏이면 신호봉 고가) 재돌파, 또는 진입가 ∓ATR(15m,14)×1.0 중 더 타이트한 쪽.
- 시간 청산: `max_hold`=12봉(15m×12=3시간) 내 목표 미도달 시 강제청산.

## 파라미터
- z_window=100봉(15m, 범위 60~150)
- premium_z_th=2.5 (범위 2.0~3.0)
- body_ratio_th=0.35 (범위 0.25~0.45)
- atr_trail_mult=1.6, atr_stop_mult=1.0
- max_hold=12봉

## 코딩 난이도 / 데이터 요구
- 필요한 지표: klines의 `taker_buy_base_asset_volume`·`taker_buy_quote_asset_volume`·`quote_asset_volume`·`volume`
  (이미 매 봉 수집하는 표준 필드), EMA(20,1h), ATR(14,15m). 추가 REST 엔드포인트 불필요.
- 주의: 오더북/틱/실시간청산 불필요. `taker_buy_base_asset_volume=0` 또는 `sell_base=0`(한쪽 방향 체결이 전혀
  없는 봉, 저유동성 알트·심야시간대에 발생 가능)인 봉은 반드시 스킵 처리(0으로 나누기 방지).

## 스카우트 메모
- **강점**: 클라이언트가 이미 매 봉 수집하는 klines 표준 필드만으로 완전 충족되고, "테이커 매수/매도를 분리해
  각각의 평균 체결가를 비교한다"는 구성 자체가 기존 320개 스펙 중 정확히 같은 방식은 없어(전수검색 확인)
  진짜 신규 데이터 구성에 해당.
- **의심점**: 위 전제 일관성 우려대로 프리미엄이 스프레드의 기계적 산물일 위험이 가장 크다. 또한 캔들VWAP
  포지션 스펙과 개념적으로 인접(둘 다 "체결가 위치/구성"을 본다)해 핵심대조군①에서 부가가치가 없으면
  사실상 중복으로 폐기될 가능성이 있음을 미리 인지.
- 우리 슬리브와의 관계: 기존 볼린저 돌파+거래량+OI 단타(scalp15m)와 메커니즘이 다른 흡수/소진형 역추세라
  보완재 후보. 다만 검증 우선순위는 대조군 결과에 따라 결정 — 중간.
