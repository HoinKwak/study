# [스윙] 샹들리에 익싯(Chandelier Exit) ATR 트레일링 추세추종

- **출처**: https://medium.com/@redsword_23261/chandelierexit-ema-dynamic-stop-loss-trend-following-strategy-4ed49f313a28 (Sword Red, Medium — BTC_USDT 선물 1d 백테스트 코드·설정 공개) / https://www.quantifiedstrategies.com/chandelier-exit-strategy/ (개념·표준 파라미터) / https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-overlays/chandelier-exit (Chuck LeBeau 원 지표 정의) / 보강: https://protraderdashboard.com/blog/chandelier-exit-strategy/
- **참여지표**: - (퀀트 블로그, SNS 참여지표 미확인)
- **백테스트 근거**: Medium(Sword Red) — **BTC/USDT 무기한 선물, 1d, 2023-07-23~2024-07-28** 구간 백테스트 존재(코드·기간 명시, 상세 손익 수치는 유료/후속 공개 아님). 별도 요약 인용(Vestinda/LuxAlgo 계열 2차 자료) — **BTC/USDT 일봉 2020~2024, EMA 크로스 진입 + Chandelier Exit(22,3.0) 청산 조합에서 PF 1.61**, 동일 진입에 고정 10% 트레일링 스톱을 쓰면 PF 1.28, 고정 5%는 PF 1.09로 **ATR 적응형 청산이 고정폭 청산 대비 우월**. 표본기간·표본크기(트레이드 수)는 2차 자료에 미기재 → 우리 프레임 재검증 필요(원전 승률·MDD 확인 필요).
- **타임프레임**: 1d 신호/청산 (크립토 변동성 고려 시 4h 변형도 검토 가치, 원전은 일봉)
- **시장/대상**: BTC·ETH·시총상위 알트 무기한

## 진입 규칙
- 추세필터: 종가가 EMA(200) **위**일 때만 롱 후보, **아래**일 때만 숏 후보(EMA200 방향 일치 진입).
- 롱: 빠른 EMA(예 `ema_fast`=20)가 느린 EMA(`ema_slow`=50)를 상향 돌파(골든크로스) **AND** 종가 > EMA(200).
- 숏: 빠른 EMA가 느린 EMA를 하향 돌파(데드크로스) **AND** 종가 < EMA(200).
- (원 코드는 `buySignal`/`sellSignal`을 별도 브레이크아웃 로직으로 정의하고 EMA200 필터만 명시 — 본 스펙은 재현 가능하도록 표준 EMA크로스로 근사, A/B로 원 신호와 비교 권장.)

## 청산 규칙
- **손절(초기)**: 진입가 ∓ 0.5×ATR(22) (원문 명시값).
- **트레일링(핵심)**: 샹들리에 라인 = 롱 `최근 22봉 최고가 − ATR(22)×3.0`, 숏 `최근 22봉 최저가 + ATR(22)×3.0`. 매 봉마다 유리한 방향으로만 갱신(한쪽 래칫). 가격이 라인을 반대로 교차하면 즉시 청산.
- **익절**: 별도 고정 TP 없음(추세추종, 트레일링에 전량 위임). 최소 1R 확보 후 트레일링 시작을 옵션으로 검토(원문엔 없음, 추정).
- **시간 청산**: 없음(이벤트 기반).

## 파라미터
- ema_fast=20 (범위 10~20), ema_slow=50 (범위 40~60), ema_trend=200 (고정)
- chandelier_period=22 (범위 14~22), chandelier_mult=3.0 (범위 2.0~3.0)
- initial_sl_atr_mult=0.5 (범위 0.5~1.0)
- signal_tf=1d (대안 4h, 재검증 필요)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: EMA(20/50/200), ATR(22), 롤링 최고/최저(22봉). 전부 캔들 OHLCV만으로 산출.
- 주의: **바이낸스 REST 캔들로 완전 충족.** 오더북/틱/OI 불필요. 샹들리에 라인의 "한쪽 래칫"(불리한 방향으로는 갱신 금지) 로직만 정확히 구현하면 나머지는 표준 지표 조합.

## 스카우트 메모
- 강점: **ATR 적응형 트레일링이 고정% 트레일링보다 우월**하다는 정량 비교(PF 1.61 vs 1.28 vs 1.09)가 존재 — 우리 봇의 스윙/mid 슬리브 청산 로직(현재 볼린저 눌림목 계열)과 **청산 메커니즘만 별도 모듈로 교체 검증**하기 좋음. 손절이 ATR 기반이라 변동성 국면 적응.
- 의심점: 인용된 PF 수치가 원전(Sword Red 기사)이 아니라 2차 요약이라 **재현성 미확인** — 반드시 자체 재현 백테스트로 확인. 진입 로직(`buySignal`)이 원문에 불명확해 본 스펙은 표준 EMA크로스로 근사(원문과 다를 수 있음). 3×ATR 트레일링은 넓어서 되돌림 구간 손실폭이 큼 — 레인지장에서 휩쏘 위험.
- 우리 슬리브와의 관계: **보완**(청산 메커니즘 다양화). 기존 `parabolic-sar-heikin-ashi-trend-swing.md`(PSAR 트레일링)와 같은 "추세추종+적응형 트레일링" 계열이지만 트레일링 산식이 다름(PSAR 가속계수 vs ATR 배수) — 두 방식 교차검증 시 어느 트레일링이 크립토에 더 적합한지 판단 가능.
