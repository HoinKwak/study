# [스윙] 미결제약정/유통공급량 침투율(OI-to-Supply) 레버리지 레짐

- **출처**: 개념 근거 — https://www.tradingview.com/script/dJLrvUYl-Crypto-Leverage-Ratio-Market-Cap-Open-Interest-in/ (TradingView, "Crypto Leverage Ratio [Market Cap / Open Interest in %]" — **WebSearch 요약으로 확인**: "Leverage Ratio = 1/(Market Cap/100 * Open Interest)" 및 "값이 크면 시가총액 대비 선물시장 미결제약정 비중이 커 숏/롱스퀴즈·디레버리징 위험 증가" — WebFetch로 원문 코드 상세는 미확인, 개념 서술만 채택).
  기존 보유 `oi-volume-leverage-crowding-contrarian-swing.md`(**24h 거래대금 대비 OI 비율**을 쓰는 유사 계열 스펙, 아직 미백테스트)와 **분모(정규화 기준)가 명확히 다름**을 확인 후 채택 — 아래 스카우트 메모에 관계 명시.
- **참여지표**: - (TradingView 오픈소스 스크립트, 구체적 좋아요/조회수 미확인). "OI/시총 비율로 레버리지 과열을 읽는다"는 프레임 자체는 크립토 파생상품 교육 콘텐츠에서 반복 언급.
- **백테스트 근거**: **없음(개념 기반, 임계값은 전부 스카우트가 캘리브레이션용으로 설정 — 원문에 정량 수치 없음)**.
- **⚠️ 예상 신호빈도 사전 명시**: 유통공급량(분모)은 하루~수일 단위로만 완만히 변하는 구조적 변수라 **`OI/유통공급량` 자체는 실질적으로 "코인 단위 OI(sum_open_interest)"의 완만한 변형**에 가깝다(시가총액=공급량×가격, OI가치=계약수×가격이므로 비율=계약수/공급량으로 가격이 상쇄됨). 따라서 이 지표는 **거래대금 기반 기존 LCR(oi-volume-leverage-crowding)보다 변동이 훨씬 완만**할 것으로 예상 — 180일 롤링 백분위 상/하위 15%를 극단으로 잡을 때, 완만한 변수 특성상 한 번 극단에 진입하면 **여러 봉 연속으로 극단 상태가 유지**될 가능성이 높다(레짐 지속). 개별 진입 신호는 종목당 연 2~6회 수준(레짐 전환 횟수 기준)으로 사전 추정하며, 신호가 이보다 훨씬 잦다면(예: 연 50회+) 정규화 창·판정 로직에 문제가 있다는 신호로 간주해 재점검할 것.
- **⚠️ 전제의 내적 일관성 사전 검토(실측 대조 필수)**: 위 계산상 `OI/유통공급량 ≈ 미결제 계약수/유통공급량`(가격 상쇄)라는 점에서, 이 지표가 기존 `oi-volume-leverage-crowding-contrarian-swing.md`(OI/24h거래대금, 가격이 상쇄되지 않고 분모가 매일 크게 요동)와 **얼마나 다른 정보를 담는지 자체가 불확실**하다 — 두 지표 모두 결국 분자가 "sum_open_interest"라 방향성은 양의 상관을 가질 가능성이 높다. **백테스터는 두 지표의 시계열 상관계수와 극단 판정일(트리거 날짜) 중복도를 반드시 먼저 실측 보고**하고, 중복도가 매우 높다면(예: 트리거일 80%+ 겹침) 이 스펙은 사실상 동일 아이디어의 재정규화에 불과하다고 정직하게 결론 낼 것.
- **타임프레임**: 4h 신호 / 1d 레짐 확인.
- **시장/대상**: BTC·ETH·시총상위 알트 무기한(CoinGecko에 시가총액·유통공급량 데이터가 있는 종목 한정).

## 진입 규칙
- **유통공급량 추정**: CoinGecko `/coins/{id}/market_chart?vs_currency=usd&days=max` 무료 엔드포인트가 반환하는 `prices[]`·`market_caps[]`(동일 타임스탬프 배열)로 `circulating_supply_est(t) = market_caps(t) / prices(t)` 역산(무료 티어에 유통공급량 히스토리 전용 엔드포인트가 없어 이 방식으로 추정 — CoinGecko가 과거 시가총액치를 소급 수정하는 경우가 있어 **추정치이며 완전 정밀하지 않음**을 인지).
- **OI(코인단위)**: `data.binance.vision` futures `metrics` 덤프의 `sum_open_interest`(USD 아닌 코인 수량 필드, 5분 간격) — 4h 봉으로 리샘플(구간 평균 또는 마지막 값).
- **침투율**: `penetration(%) = sum_open_interest / circulating_supply_est × 100`.
- **정규화**: `pen_pctile[i] = percentile_rank(penetration[i], window=180봉(4h 기준 30일치가 아니라 4h×180=30일 — 표기 명확화: 4h 봉 180개 = 30일))`.
- **숏(구조적 과밀 롱 레버리지)**: `pen_pctile >= 85` **AND** 펀딩비 ≥ +0.02%/8h(롱 우위 확인) **AND** 종가가 최근 20봉 고가 갱신 실패(직전 고점 미갱신, 모멘텀 둔화 확인) → 숏.
- **롱(구조적 디레버리징 완료, 숏스퀴즈 여력)**: `pen_pctile <= 15` **AND** 펀딩비 ≤ -0.01%/8h **AND** 종가가 최근 20봉 저가 갱신 실패 → 롱.

## 청산 규칙
- 익절: `pen_pctile`이 중립대(40~60)로 복귀 시 청산, 또는 ATR(14,4h)×2.5 트레일링.
- 손절: 신호봉 반대 극값 또는 진입가 ∓ ATR(14,4h)×1.5.
- 시간 청산: 최대 보유 20봉(4h 기준 약 3.3일) 초과 시 강제 청산(구조적 레짐 지속성 감안, 기존 LCR 스펙(10봉)보다 다소 여유 있게 설정).

## 파라미터
- pen_window=180봉(30일) (범위 90~365)
- extreme_low_pctile=15 (범위 10~20), extreme_high_pctile=85 (범위 80~90)
- funding_confirm_long=+0.02%/8h, funding_confirm_short=-0.01%/8h (범위 ±0.01~0.05)
- price_lookback=20봉 (범위 15~30)
- max_hold_bars=20 (범위 15~30)
- atr_trail_mult=2.5 (범위 2.0~3.5)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: `sum_open_interest`(metrics 덤프), CoinGecko `market_chart`(시가총액·가격 배열), 펀딩비, Donchian(20), 롤링 백분위.
- 주의: **CoinGecko 무료 API 레이트리밋**(분당 요청 제한) 고려해 종목별 1회씩만 전체기간 `market_chart`를 캐싱해 받을 것. `sum_open_interest` 필드는 기존 다수 스펙(`oi-capitulation-multiday-deleveraging-reset-swing` 등)에서 이미 활용 검증된 필드. 오더북/틱/청산 불필요.

## 스카우트 메모
- **강점**: "OI를 유통공급량으로 정규화"하는 축은 기존 300개 스펙에 전무(전부 거래대금·펀딩·가격 기반 정규화) — CoinGecko 시가총액 데이터는 이미 우리 인프라가 유니버스 선정에 쓰고 있어(`CLAUDE.md` 명시) 완전히 새로운 커넥터가 필요하지 않다는 점이 이 라운드 외부데이터 후보들(금·업비트) 대비 이점.
- **의심점**: 위에서 자인했듯 **기존 `oi-volume-leverage-crowding-contrarian-swing`과 정보 중복 가능성이 구조적으로 존재**(둘 다 분자가 OI) — 이 스펙 단독의 존재가치는 백테스터의 상관계수 실측에 달려 있음. 유통공급량을 시가총액/가격으로 역산하는 방식이라 CoinGecko의 과거 시가총액 소급수정 리스크도 있음.
- **우리 슬리브와의 관계**: 기존 미백테스트 LCR 스펙과의 **직접 대조군**으로 가치 있음 — 백테스트 시 두 스펙을 같은 라운드에 붙여 상관·중복도부터 확인 후 하나만 채택하거나 둘 다 폐기하는 것을 권장.
