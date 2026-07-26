# 차이킨 변동성(Chaikin Volatility) 수축-확장 브레이크아웃 [스윙]

- **출처**: https://trendspider.com/learning-center/chaikin-volatility/ , https://gocharting.com/docs/
  charting/technical-indicator/oscillators/chaikin-volatility , https://www.luxalgo.com/blog/what-is-
  chaikin-volatility-indicator/ (원조: Marc Chaikin이 고안한 변동성 오실레이터 — Chaikin Money Flow·
  Chaikin Oscillator와는 **다른 지표**, 고저폭(H-L range)의 EMA 변화율을 측정).
- **참여지표**: 단일 고참여 게시물 없음 — 여러 차티스트 교육 사이트에서 공통적으로 다루는 표준
  변동성 지표. 좋아요/조회수 해당 없음.
- **백테스트 근거**: **없음(참여지표/지표정의 기반)**. 검색된 원문들은 모두 "정성적 프레임워크"만
  제시하고("이 지표를 방향성 지표로 쓰지 말라"는 명시적 경고 포함), 정량 백테스트 수치는 어디에도 없음.
  진입/청산 임계치(수축 판정 percentile, 돌파 확인폭 등)는 **원문에 수치가 없어 스카우트가 코딩
  가능하도록 직접 수치화**했음을 명확히 표기([추정] 표시된 파라미터).
- **타임프레임**: 4h~1d (변동성 수축 국면은 스윙 성격이 강함 — 원문도 "multi-month lows" 언급).
- **시장/대상**: BTC·ETH·메이저 알트 무기한.

## 진입 규칙
- 지표 계산: (1) 매 봉의 **고가-저가(H-L)** 산출 → (2) 그 값의 **10기간 EMA** → (3) 그 EMA의
  **10기간 전 대비 변화율(%)**. 결과가 Chaikin Volatility(CV) 값.
- 수축 판정: CV가 최근 **60봉(약 2.5개월, 4h 기준) 중 하위 10%(percentile)**로 떨어지면 "스퀴즈" 상태로
  간주([추정] — 원문 "multi-month lows"를 수치화).
- 롱: 스퀴즈 상태에서 가격이 **직전 N봉(예 20봉) 레인지 상단을 종가 기준 돌파**하고, 돌파 봉에서
  **CV가 반등(direction 전환, 즉 값 상승 시작)**하면 진입. 원문 권고대로 **CMF(Chaikin Money Flow)가
  양(+)**이면 추가 확증([추정] — 원문: "CV 스파이크 + 양의 CMF"가 강한 돌파, 음/평탄이면 가짜 돌파 경고).
- 숏: 대칭 — 스퀴즈 후 **레인지 하단 이탈 + CV 반등 + CMF 음(-)**.

## 청산 규칙
- 익절: 돌파 방향으로 **ATR×2.5 트레일링 스탑**([추정] — 원문에 정량 청산 규칙 없음, 변동성 확장
  국면 특성상 ATR 기반 트레일링이 합리적).
- 손절: 돌파 시 확인된 **레인지 반대편(스퀴즈 박스 내부)**에 스탑(원문: "stop just inside the range").
- 시간청산: CV가 다시 스퀴즈 percentile(하위 10%) 이하로 재수축하면 추세 소멸로 보고 청산([추정]).

## 파라미터
- cv_ema_period=10, cv_roc_period=10 (표준값, 다수 소스 공통)
- squeeze_lookback=60봉, squeeze_percentile=10%
- breakout_range_lookback=20봉
- cmf_period=20~21, cmf_confirm_sign 필요
- stop_atr_mult(트레일)=2.5, atr_period=14

## 코딩 난이도 / 데이터 요구
- 필요한 지표: H-L range EMA(10), 그 값의 10봉 ROC, percentile rank(60봉 롤링), CMF(거래량+가격
  위치 기반, 우리 저장소 `chaikin-money-flow-breakout-swing`에서 이미 구현 로직 존재 가능), ATR(14).
- 전부 바이낸스 REST 캔들(OHLCV)만으로 계산 가능. 오더북/틱데이터 불필요. percentile rank 계산은
  약간의 롤링윈도 로직이 필요하나 난이도는 낮음.

## 스카우트 메모
- 강점: **Chaikin Volatility는 볼린저밴드 폭(BW)이나 ATR 자체가 아니라 "고저폭의 EMA 변화율"을 보는
  별개 지표**라서, 우리 저장소의 `ttm-squeeze-momentum-breakout-swing`(BB-Keltner 스퀴즈),
  `bw-mfi-squat-breakout-swing`(BW+MFI), `bollinger-squeeze-breakout-daily`(BB폭)와 **계산 방식이
  달라 순수 지표 관점에서는 신규**. 다만 "변동성 수축→확장 브레이크아웃"이라는 **컨셉 자체는 이미
  3~4개 스펙이 다루고 있어 실질적 차별화(로직상 새 엣지)는 제한적**.
- 의심점: 정량 백테스트 전무. 원문들이 명시적으로 "방향성 지표로 쓰지 말라"고 경고할 만큼 CV 단독으로는
  약한 신호이며, 본 스펙의 임계치(percentile 10%, ATR×2.5 등)는 전부 스카우트가 직접 수치화한 것이라
  **과최적화 검증이 필수**. 기존 스퀴즈 계열이 이미 백테스트 후보로 쌓여 있다면 이 전략의 **우선순위는
  낮게** 잡는 것이 합리적.
- 우리 슬리브와의 관계: **중복 위험 있는 보완**. 스퀴즈 브레이크아웃 계열이 이미 포화 상태이므로,
  백테스트 큐에서 후순위로 두고 기존 스퀴즈 계열 결과가 부진할 때만 대체 후보로 검토 권장.
