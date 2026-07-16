# [단타] UT Bot Alerts — ATR 트레일링 스톱 크로스오버 스캘핑

- **출처**: https://www.tradingview.com/script/n8ss8BID-UT-Bot-Alerts/ (TradingView, QuantNomad 게시 v4 알림버전, 원저작 Yo_adriiiiaan/HPotter) /
  포뮬러 원문 미러: https://github.com/AedonStorm/UT-Bot-Alerts/blob/main/UT-Bot-Alerts.pine /
  실제 백테스트: https://imbuedeskpicasso.medium.com/whooping-3202-profit-with-famous-utbot-alerts-from-tradingview-using-python-on-freqtrade-316cb7578118 (freqtrade 포팅, BTCUSDT 15m) /
  자동백테스트 집계: https://tradesearcher.ai/strategies/1854-strategy-for-ut-bot-alerts-indicator (크립토 티커 다수)
- **참여지표**: TradingView 좋아요/부스트 **53.6K**, 조회수 **약 149.5만** (WebFetch로 직접 확인, 2026-07 기준). TradingView 최상위권 인디케이터 중 하나.
- **백테스트 근거**:
  - freqtrade 포팅판(Medium, WebFetch 확인): **BTC/USDT, 15분봉, 2021-01-01~2023-08-15(955일)**, 초기 1,000 USDT → **+3202% 수익**(동기간 BTC 단순보유 -38.39%), **최대낙폭 14.29%**, **평균 일간 트레이드 약 19.55건**(동시 최대 4포지션, 포지션당 최대 ~200 USDT). 단, 이 수치는 순수 UT Bot 신호가 아니라 **ADX+거래량 필터+200EMA+하이퍼옵트가 추가된 변형**이며, 일 19.55건이면 표본 내 트레이드 수가 극히 많아 **하이퍼파라미터 최적화로 인한 과최적화 위험이 큼**(원문도 상세 하이퍼옵트 값 전부 공개하지 않음). 원문 확인됨, 그러나 재현성·표본외검증 불명.
  - TradeSearcher.ai 자동백테스트(WebFetch 확인, 표본기간·수수료 가정 불명): 예) CROUSDT 4h R:R 2.49 ROI 1522%(494트레이드), SANDUSDT 일봉 R:R 2.38 ROI 74.3%(51트레이드), THETAUSDT 일봉 R:R 2.14 ROI 38.6%(50트레이드) 등 — **어떤 파라미터·필터 조합인지, 수수료 포함 여부 불명**이라 참고용.
- **타임프레임**: 5m~15m 신호 (원 지표는 스캘핑용 저Key Value 설정 권장, freqtrade 검증은 15m)
- **시장/대상**: BTC·ETH 및 유동성 상위 무기한 (freqtrade 백테스트는 BTCUSDT 단일)

## 진입 규칙
- 지표: `xATR = ATR(atr_period)`, `nLoss = key_value × xATR`
- ATR 트레일링 스톱(`xATRTrailingStop`) 매 봉 갱신:
  - `close > stop[-1]` 이고 `close[-1] > stop[-1]` → `stop = max(stop[-1], close − nLoss)`
  - `close < stop[-1]` 이고 `close[-1] < stop[-1]` → `stop = min(stop[-1], close + nLoss)`
  - `close > stop[-1]` (반전 시작) → `stop = close − nLoss`
  - 그 외(`close ≤ stop[-1]`) → `stop = close + nLoss`
- 롱: `close`(원 코드는 `ema(close,1)`로 사실상 종가)가 `xATRTrailingStop`을 상향 돌파(crossover) **AND** `close > xATRTrailingStop`.
- 숏: `xATRTrailingStop`이 `close`를 상향 돌파(즉 종가가 스톱을 하향 이탈) **AND** `close < xATRTrailingStop`.
- (선택 필터, freqtrade 검증판에서 사용 — 과최적화 위험 인지 후 A/B 권장): `close > EMA(200)`(롱)/`< EMA(200)`(숏), ADX 임계값, `volume > volume의 이동평균`.

## 청산 규칙
- **트레일링(핵심)**: 반대 방향 크로스오버(스톱 라인을 가격이 역방향으로 이탈) 시 즉시 청산 — 지표 자체가 곧 청산 신호.
- **손절**: 별도 고정 SL 없음(트레일링 스톱이 곧 SL 역할). 우리 봇 적용 시 `entry ∓ 1.0×ATR(atr_period)` 초기 SL 병행 권장(원문엔 없음, 리스크관리 보강 추정).
- **익절**: 원문엔 고정 TP 없음(추세추종형, 반대신호까지 보유). freqtrade 변형은 부분청산 로직 포함하나 상세 미공개.
- **시간 청산**: 없음(이벤트 기반).

## 파라미터
- key_value(a)=1 (범위 0.5~3, 낮을수록 민감·거래多)
- atr_period(c)=10 (범위 1~14; freqtrade 검증판은 3 사용 — 하이퍼옵트 결과라 과최적화 의심)
- ema_trend=200 (옵션 필터, 범위 100~200)
- signal_tf=15m (범위 5m~1h)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: ATR, 종가(EMA(1)=원시 종가와 동일). 전부 캔들 OHLCV로 산출 가능.
- 옵션 필터 사용 시 ADX, EMA(200), 거래량 이동평균 추가 — 모두 바이낸스 REST 캔들로 충족.
- 주의: 오더북/틱/실시간 청산 데이터 불필요. 순수 캔들 기반이라 우리 인프라로 완전 재현 가능.

## 스카우트 메모
- 강점: TradingView 역대 최상위권 참여지표(좋아요 5.36만·조회 149만)로 검증된 대중성. ATR 적응형 트레일링 자체는 단순·직관적이라 코딩 난이도 낮음. Chandelier Exit(기존 보유 스펙)과 컨셉은 유사하나 **스톱 갱신 로직(한쪽 래칫 없이 매 봉 재계산)과 신호 발생 방식(크로스오버 즉시 반전)이 달라** 더 빈번·저지연 신호 — 단타에 적합.
- 의심점: **freqtrade +3202% 수치는 순수 UT Bot이 아니라 다중 필터+하이퍼옵트 변형**이며 일평균 19.55트레이드는 표본이 매우 커 과최적화 가능성 농후. TradeSearcher 자동백테스트도 수수료·슬리피지 가정이 불명확해 액면 신뢰 금지. 반드시 우리 프레임(수수료 왕복 0.14% 반영)으로 재검증 필요 — 특히 저 key_value(1)·저 atr_period(3~10) 조합은 휩쏘가 잦아 레인지장에서 손실 누적 위험.
- 우리 슬리브와의 관계: 대체 후보(청산 로직 교체용). 기존 볼린저 돌파+거래량+OI 단타 슬리브와 **동일 저빈도 논리(강한 돌파 추종)가 아니라 매 봉 반응하는 고빈도형**이라 그대로 쓰면 수수료 부담 큼 → key_value·atr_period를 높여(예 2~3, 14) 신호 빈도를 낮춘 변형으로 시작 권장.
