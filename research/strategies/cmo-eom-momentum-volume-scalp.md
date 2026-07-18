# 챤데 모멘텀 오실레이터 + 이즈오브무브먼트 콤보 [단타]

- **출처**: 아이디어 원안 — Kridtapon P., "Developing a Bitcoin Trading Strategy with Chande Momentum Oscillator(CMO) and Ease of Movement(EMV)", Medium https://medium.com/@kridtapon/developing-a-bitcoin-trading-strategy-with-chande-momentum-oscillator-cmo-and-ease-of-a38d5cef9a7a (BTC 특정 백테스트 시도 글). 지표 정의: CMO — Tushar Chande(1994); EOM — Richard Arms(1989).
- **참여지표**: 확인 불가(Medium 클랩수 등 페이지 본문 접근 실패 — 아래 "코딩 난이도" 참고). 원문 확인 안 됨.
- **백테스트 근거**: **정량 수치 원문 미확인.** WebFetch로 해당 Medium 글에 2회 접근 시도(직접 URL, freedium 미러) — 직접 접근은 헤더/도입부만 반환되고 본문 잠김, 미러는 DNS 실패로 접근 불가. 확인된 유일한 문장은 원저자 자인 "This is just a backtest that is still under development... it has not undergone robustness testing"(강건성 검증 미완료를 저자 스스로 명시) — 즉 **원문에 백테스트가 있었다는 사실만 확인, 수치는 미확인**. 별도 검색된 CMO 단독 소스(quantifiedstrategies.com)는 봇 차단으로 확인 불가하여 인용하지 않음.
- **타임프레임**: 5m 신호 / 15m 확인.
- **시장/대상**: BTC·ETH 무기한(원안이 BTC 특정).

## 진입 규칙
- CMO(14): `CMO = 100 * (Su - Sd) / (Su + Sd)`, Su=최근 n봉 상승폭 합, Sd=하락폭 절대값 합. 범위 -100~+100.
- EOM(14): `1봉 EOM = ((High+Low)/2 - (PrevHigh+PrevLow)/2) / (Volume / (High-Low))` 를 14봉 SMA로 스무딩(EMV_SMA). 크립토는 거래량 스케일이 종목마다 상이하므로 **원값 대신 EMV_SMA의 부호(양/음)만 방향 필터로 사용**(스케일 정규화 문제 회피, 설계 판단).
- 롱: 5m CMO가 -50 이하(과매도)에서 반등하며 -50선을 상향 돌파 + 동시점 15m EMV_SMA > 0(매수압력 우위).
- 숏: 5m CMO가 +50 이상에서 +50선을 하향 돌파 + 15m EMV_SMA < 0.

## 청산 규칙
- 익절: CMO가 반대 극단(롱 진입 후 +50 도달, 숏 진입 후 -50 도달) 또는 1.5R 중 먼저 도달하는 쪽.
- 손절: 진입봉 기준 1.0×ATR(5m,14).
- 시간 청산: 12봉(5m, 1시간) 내 미도달 시 청산(스캘프 특성상 홀딩 장기화 방지).

## 파라미터
- cmo_period=14 (원저자 표준, 범위 9~20)
- cmo_threshold=50 (범위 40~60)
- eom_period=14 (범위 10~20)
- sl_atr_mult=1.0 (범위 0.8~1.5)
- tp_rr=1.5 (범위 1.2~2.0)
- max_hold_bars=12 (5m 기준)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: CMO(종가만), EOM(고저+거래량), ATR. 전부 표준 OHLCV.
- 주의: 바이낸스 REST 캔들+거래량으로 완전 충족. EOM의 박스비율(Volume/(High-Low)) 스케일이 자산별로 크게 달라 **원저자 방식 그대로 쓰면 종목 간 비교가 불가** — 방향(부호)만 필터로 쓰는 것으로 단순화했음을 명시(원문 미확인이라 원저자가 이 문제를 어떻게 다뤘는지 알 수 없음).

## 스카우트 메모
- 강점: CMO(챤데 모멘텀 오실레이터)·EOM(거래량 가중 가격이동용이성) 둘 다 우리 보유 69개 목록에 없는 신규 지표. 특히 EOM은 "가격이 거래량 대비 얼마나 쉽게 움직였는가"를 정량화하는 유일한 후보로, cvd-taker-volume-divergence·obv-ma-breakout 등 기존 거래량계열과 공식이 달라 상관 낮을 가능성.
- 의심점: (1) 원문 백테스트 수치를 전혀 확인 못해 신뢰도 최하위 — 원저자도 강건성 미검증 자인. (2) EOM 스케일링 문제를 임의로 단순화(부호만 사용)했기 때문에 원안과 실제로 다른 전략이 됐을 가능성 큼 — 백테스트 우선순위 낮음. (3) CMO±50 임계값은 RSI 70/30과 유사한 발상이라 rsi2-mean-reversion·cci-extreme-momentum·williams-r-extreme-reversal 등과 신호 상관이 높을 위험(구조적으로 "오실레이터 극단 반전"군에 속함 — 이미 8개 유사 계열 보유, 중복도 다소 높음을 인지).
- 우리 단타 슬리브와의 관계: 우리 기존 스캘프(볼린저 돌파+거래량+OI)는 모멘텀 추종형, 이건 평균회귀형이라 방향성은 보완적이나, 오실레이터 극단반전 구조 자체는 이미 다수 보유 → **채택 우선순위 낮음**(정량 근거 부재 + 구조적 중복 두 이유).
