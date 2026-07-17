# [스윙] Aroon 오실레이터 신규추세 조기포착 + 강도필터

- **출처**: https://www.investopedia.com/terms/a/aroon.asp (Tushar Chande, 1995 개발 — 표준 산식) /
  https://www.avatrade.com/education/technical-analysis-indicators-strategies/aroon-indicator-strategies (전략화 서술) /
  https://www.quantifiedstrategies.com/aroon-indicator-strategy/ (WebFetch 봇 차단으로 원문 성과수치 확인 실패)
- **참여지표**: - (Aroon은 TradingView **빌트인(내장) 지표**라 커뮤니티 스크립트 좋아요 집계가 무의미함 — 대신 1995년부터 표준 기술적분석 교재·플랫폼에 기본 탑재될 만큼 **업계 통용도가 높은 지표**로 스크리닝. 파생 커뮤니티 스크립트(Ultra Aroon Oscillator, BigBeluga Aroon 등)가 다수 존재해 재구현 수요도 확인됨).
- **백테스트 근거**: **정량 수치 원문 미확인.** quantifiedstrategies.com 백테스트 페이지는 봇검증(bot verification)에 막혀 WebFetch로 실제 수치를 확인하지 못했다. 검색엔진 스니펫 수준에서 "Aroon은 백테스트에서 51~59% 승률", "1시간봉+MACD 필터 조합 크립토 백테스트에서 291% 순수익" 등의 서술이 보였으나, **원문 URL을 특정·검증하지 못해 인용하지 않는다.** → 본 전략은 표준 공개 산식과 업계 통용성만 근거로 채택, **자체 백테스트 필수**.
- **타임프레임**: 4h 신호 / 1d 레짐필터
- **시장/대상**: BTC·ETH 및 시총상위 알트 무기한

## 진입 규칙
- 산식(표준, N=25 기본): `AroonUp = 100 × (N − 최고가 발생 이후 경과봉수) / N`, `AroonDown = 100 × (N − 최저가 발생 이후 경과봉수) / N`. `AroonOsc = AroonUp − AroonDown`.
- 레짐필터: `ADX(14) ≥ 20`(추세 강도 최소 기준, Aroon 단독은 레인지장 휩쏘가 잦다는 게 통설이라 ADX로 보강).
- 롱: `AroonUp`이 `AroonDown`을 상향 돌파 **AND** `AroonUp ≥ 70`(강한 신규 상승추세 시작) **AND** `AroonDown ≤ 30` **AND** ADX 필터 통과.
- 숏: `AroonDown`이 `AroonUp`을 상향 돌파 **AND** `AroonDown ≥ 70` **AND** `AroonUp ≤ 30` **AND** ADX 필터 통과.
- (단순화 대안) `AroonOsc`가 0선을 상향/하향 돌파하는 것만으로 크로스 신호를 대체 가능(더 잦은 신호, 백테스트로 두 버전 비교 권장).

## 청산 규칙
- 익절: 고정 TP 없음(추세추종, 반대 크로스까지 홀드) 또는 옵션 2.0R 고정.
- 손절: 진입가 ∓ 2.0×ATR(14).
- 반대신호 청산: `AroonDown`이 다시 `AroonUp`을 상회(롱 청산) / 반대(숏 청산).
- 시간 청산: 없음(이벤트 기반), 단 `AroonUp`·`AroonDown` 둘 다 50 부근에서 횡보(=레인지 재진입) 지속 시 N=10봉 후 청산 옵션.

## 파라미터
- aroon_period=25 (범위 14~25, Chande 원 권장 25)
- aroon_cross_th=70/30 (범위 60~80 / 20~40)
- adx_min=20 (범위 15~25)
- adx_period=14
- sl_atr_mult=2.0 (범위 1.5~3.0)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 롤링 N봉 내 최고/최저가 발생 시점(경과봉수) 계산, ADX(14). **전부 캔들 OHLCV로 충족**, 계산 자체는 가볍다(돈치안류 롤링 탐색과 유사 난이도).
- 주의: 오더북/틱/OI 불필요. 바이낸스 REST 캔들로 완전 재현 가능.

## 스카우트 메모
- 강점: "시간(경과봉수)" 기반 지표라 가격 변동폭(ATR/VI 계열)이나 이동평균(EMA/HMA 계열)과 **산식 계통이 완전히 달라** 기존 보유 전략들과 신호 상관도가 낮을 가능성. 신규 추세 시작을 가격 돌파보다 먼저 포착하는 설계(경과봉수 기반)라 추세추종 진입 타이밍 보완재로 유효.
- 의심점: **정량 백테스트 근거를 확보하지 못함**(주요 소스가 봇차단) — 이번 라운드 후보 중 근거가 약한 편. Aroon은 레인지장에서 휩쏘가 잦다는 게 다수 2차 자료의 공통 지적이라 ADX 필터가 필수적이나, 필터 임계값(20)은 추정치.
- 우리 단타 슬리브와의 관계: 완전 신규 축(경과시간 기반 추세지표) — 기존 Vortex(가격변동폭 기반)·GMMA(이평 정렬 기반)와 **보완재**로 분류. 채택 전 반드시 자체 백테스트로 처음부터 검증.
