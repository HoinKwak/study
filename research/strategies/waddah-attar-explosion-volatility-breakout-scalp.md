# [단타] Waddah Attar Explosion 변동성 폭발 돌파

- **출처**: 원 지표 개념 — Waddah Attar(외환 트레이더) 고안. TradingView 파생 스크립트:
  "Waddah Attar Explosion with TDI"(dubfinder) — https://www.tradingview.com/script/68RyH6T8-Waddah-Attar-Explosion-with-TDI/ (WebFetch 확인) /
  "Waddah Attar Explosion V2 [SHK]"(shayankm, ATR 기반 데드존으로 크립토 저가시장 대응) —
  https://www.tradingview.com/script/d9IjcYyS-Waddah-Attar-Explosion-V2-SHK/ (WebFetch 확인) /
  기본 파라미터(sensitivity/fastLength/slowLength/BB길이/mult/deadzone)는 strategyquant.com·pineify.app
  2차 자료의 검색엔진 요약으로만 확인(직접 WebFetch는 두 사이트 모두 접근 실패 — **원문 직접 대조는
  실패, 검색엔진 스니펫 종합값**으로 표기).
- **참여지표**: "Waddah Attar Explosion with TDI" 좋아요 **12,080** / 조회수 **28,355**(WebFetch 확인).
  "Waddah Attar Explosion V2 [SHK]" 좋아요 **6.3K** / 조회수 **9,393**(WebFetch 확인). TradingView
  변동성 지표 중 최상위권 인기.
- **백테스트 근거**: 없음(지표 페이지 자체엔 정량 성과 미공개, 참여지표 기반 채택). 앞서 조사한
  "QQE MOD+SSL Hybrid+Waddah Attar Explosion" 3중 조합 백테스트(tradesearcher.ai, ETHUSDT 4h
  총수익 165.72%/거래 344회/위험수익비 1.45 등, WebFetch 확인)는 **SSL Hybrid·QQE MOD가 함께
  섞인 조합**이라 Waddah 단독 기여도는 분리 불가 — 참고치로만 남기고 본 스펙(단독 WAE)의 정량
  근거로는 채택하지 않음.
- **타임프레임**: 개발자 권장 30분봉(V2 SHK 페이지, WebFetch 확인) / 5m~1h 스캘핑에도 광범위 사용
- **시장/대상**: 크립토 무기한 전반(V2가 저가 알트코인 대응 위해 ATR 기반 데드존으로 개조됨)

## 진입 규칙
- MACD 기반 추세값: `t1 = (EMA(close,fastLength) − EMA(close,slowLength) − (EMA(close,fastLength)[1] − EMA(close,slowLength)[1])) × sensitivity`
  (검색엔진 종합값: fastLength=20, slowLength=40, sensitivity=150 — **원문 직접 대조 실패, 2차 소스 종합**)
- 변동성(폭발선): `explosion = BB_upper(close, channelLength, mult) − BB_lower(close, channelLength, mult)`
  (검색엔진 종합값: channelLength=20, mult=2.0)
- 데드존(V1 고정): `deadzone ≈ 30`(2차 소스 종합, 원문 미대조) / **V2 개선(권장)**: `deadzone = ATR(100) × k`
  (k 계수는 원문 파라미터 미확인 — 백테스트 시 스윕 필요)
- 롱: `t1 > 0`(녹색 히스토그램) **AND** `t1 > explosion` **AND** `t1 > deadzone` — 즉 상승 모멘텀이
  변동성 채널과 데드존을 모두 상회.
- 숏: `t1 < 0`(적색 히스토그램) **AND** `|t1| > explosion` **AND** `|t1| > deadzone`.

## 청산 규칙
- 익절: 히스토그램이 데드존 아래로 재진입(모멘텀 소진) 시 청산, 또는 반대색 전환 시 청산.
- 손절: 진입 신호봉 시가/저가(우리 봇 기존 관례와 동일하게 `stop_mult × 신호봉 레인지`) — 원문
  미제시로 자체 보강.
- 시간/조건 청산: 없음(원문 미제시).

## 파라미터
- fastLength=20, slowLength=40, sensitivity=150 (2차 소스 종합, 원문 대조 실패 — 범위 스윕 권장)
- bb_len=20, bb_mult=2.0
- deadzone_fixed=30 (V1) 또는 deadzone_atr_mult=k (V2, k값 미확인 → 1.0~3.7 범위 탐색 권장)
- signal_tf=30m (범위 15m~1h)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: EMA(빠름/느림), 볼린저밴드, ATR(V2용) — 전부 OHLCV로 계산 가능, 구현 난이도 중.
- 주의: **정확한 기본 파라미터를 원문 코드(Pine Script)에서 직접 대조하지 못함** — strategyquant.com은
  503 오류, pineify.app 블로그는 404. 백테스트 전 반드시 TradingView 공개 스크립트의 Pine 코드를
  열람해 정확한 산식·기본값을 재확인할 것(현재 파라미터는 검색엔진 종합 추정치로만 신뢰).

## 스카우트 메모
- 강점: TradingView 참여지표(좋아요 1.2만+·6.3천, 댓글 수천)로 크립토 트레이더 커뮤니티에서
  검증된 인기 지표. MACD 모멘텀 + 볼린저 변동성 + 데드존 3중 필터 구조가 거래량 급증 돌파
  전략(기존 볼린저+거래량+OI 단타)과는 다른 계통(가격 파생 지표만 사용, 거래량 미사용)이라
  포트폴리오 다각화에 유리.
- 의심점: **핵심 파라미터(sensitivity=150 등)가 원문 직접 대조 실패** — 반드시 재검증 필요.
  기존 스펙(ssl-hybrid-qqe-mod-trend-confirm-swing.md)에서 이미 "3번째 필터로 Waddah 추가는
  코딩 복잡도 대비 효용 불확실하여 제외"라 판단한 바 있어, 단독 사용 시 SSL/QQE 없이도 유효한지
  별도 검증 필요.
- 우리 슬리브와의 관계: 보완(신규 계통, 거래량 미사용 변동성 오실레이터). 파라미터 미확정 상태라
  백테스트 우선순위는 후순위 권장(먼저 Pine 원문 대조 후 진행).
