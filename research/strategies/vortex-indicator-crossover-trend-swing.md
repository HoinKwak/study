# [스윙] 보텍스 지표(Vortex Indicator) VI+/VI− 크로스오버 추세추종

- **출처**: https://pyquantlab.medium.com/vortex-trend-following-trading-strategy-explained-678cfe47269a (PyQuantLab, Medium — Binance 현물 데이터 기반 Vortex+레짐필터+변동성게이트 프레임워크, 회원제 페이월로 상세 파라미터·백테스트 수치는 미확인) /
  개념·표준 파라미터: https://www.tradingview.com/support/solutions/43000591352-vortex-indicator/ , https://www.barchart.com/education/technical-indicators/vortex /
  (보강 시도) https://www.quantifiedstrategies.com/vortex-indicator-trading-strategy/ — **WebFetch 봇 차단으로 원문 접근 실패, 수치 미확인**
- **참여지표**: - (퀀트 블로그, SNS 참여지표 미확인)
- **백테스트 근거**: **정량 수치 원문 미확인.** PyQuantLab 기사는 "Binance 현물 데이터로 Vortex 크로스오버 + 장기이동평균 레짐필터 + ATR/Close 변동성 게이트 프레임워크를 평가"한다고 서술하나, 상세 수치(수익률·승률·PF)는 회원전용 구간에 있어 WebFetch로 확인 불가. quantifiedstrategies.com의 SPY(S&P500 ETF) 백테스트는 검색엔진 요약에서만 "매수보유 대비 리스크조정 성과 유사, 체류시간은 절반"이라는 서술을 봤으나 **원문 페이지가 봇검증으로 차단되어 WebFetch 직접 확인 실패** — 이 수치는 인용하지 않음(신뢰도 낮음으로 배제). **본 스펙은 지표 자체가 공개 표준 산식이라는 점과 참여 커뮤니티 서술만 근거로 채택, 실사용 전 자체 백테스트 필수.**
- **타임프레임**: 4h 신호 / 1d 레짐필터
- **시장/대상**: BTC·ETH 및 시총상위 알트 무기한

## 진입 규칙
- 보텍스 지표 산식(N=14 기본):
  - `VM+ = |High[t] − Low[t−1]|`, `VM− = |Low[t] − High[t−1]|`
  - `TR = True Range` (표준)
  - `VI+ = SUM(VM+, N) / SUM(TR, N)`, `VI− = SUM(VM−, N) / SUM(TR, N)`
- 레짐필터: `close > EMA(200)`(롱 후보) / `close < EMA(200)`(숏 후보) — PyQuantLab 프레임워크의 "장기 MA 레짐필터" 컨셉을 표준 EMA200으로 근사(원문 정확한 MA 종류·기간 미확인).
- 변동성 게이트: `ATR(14)/close ≥ vol_gate_min`(예 1.0%) — 저변동성 데드존 회피 목적(원문 "ATR/Close 변동성 게이트" 컨셉을 근사, 정확한 임계값 미확인 → 백테스트로 튜닝 필요).
- 롱: `VI+`가 `VI−`를 상향 돌파(crossover) **AND** `close > EMA(200)` **AND** 변동성 게이트 통과.
- 숏: `VI−`가 `VI+`를 상향 돌파(crossover) **AND** `close < EMA(200)` **AND** 변동성 게이트 통과.

## 청산 규칙
- **반대 크로스 청산**: 반대 방향 VI 크로스오버 발생 시 청산(지표 자체 청산 신호).
- **손절**: `진입가 ∓ 2.0×ATR(14)` (원 지표엔 SL 규정 없음 — 리스크관리 보강 추정, 백테스트로 배수 조정).
- **익절**: 고정 TP 없음(추세추종형, 반대신호까지 홀드). 최소 1.5R 확보 후 트레일링 전환을 옵션으로 검토(추정).
- **시간 청산**: 없음(이벤트 기반).

## 파라미터
- vi_period=14 (범위 10~30)
- ema_regime=200 (범위 100~200)
- atr_period=14 (범위 10~20)
- vol_gate_min=1.0% (범위 0.5~2.0%, ATR/close 기준)
- sl_atr_mult=2.0 (범위 1.5~3.0)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: High/Low/Close 기반 VM+/VM−/TR 누적합, EMA(200), ATR(14). 전부 캔들 OHLCV만으로 산출 가능.
- 주의: 오더북/틱/OI 불필요. 바이낸스 REST 캔들로 완전 충족. VI 산식 자체는 표준·공개돼 있어 구현 난이도 낮음(터틀/돈치안과 유사한 롤링 합산 로직).

## 스카우트 메모
- 강점: 지표 산식이 공개 표준이라 재현성 100% 보장, 별도 튜닝 없이 즉시 백테스트 가능. 크립토 4h/1d 스윙 특성상 추세 국면에서 VI 크로스는 EMA 골든크로스보다 반응이 빠른 편(변동성 정규화 때문) — 우리 봇의 스윙 트렌드추종 계열(터틀/샹들리에)과 다른 산식 계통이라 신호 상관도 낮을 가능성.
- 의심점: **핵심 백테스트 근거를 원문에서 확인하지 못함**(페이월·봇차단) — 반드시 자체 백테스트로 유효성 처음부터 검증해야 하는 사실상 "무근거 채택"에 가깝다. 레짐필터·변동성게이트의 정확한 임계값도 우리가 임의로 근사한 것이라 그대로 신뢰 금지. VI는 원래 레인지장에서 휩쏘가 잦다고 알려짐(TradingView 지원문서에도 명시) — ADX 등 추세강도 필터 추가 검토 여지.
- 우리 슬리브와의 관계: 보완(신규 계통). 기존 터틀 듀얼돈치안·샹들리에익싯·GMMA 등 추세추종 스윙군과 목적은 같으나 산식(방향성 이동폭 대 TR 비율)이 달라 앙상블 시 분산효과 기대. 백테스트 우선순위는 낮음(근거 미확인) — 위 UT Bot/Range Filter 대비 후순위 권장.
