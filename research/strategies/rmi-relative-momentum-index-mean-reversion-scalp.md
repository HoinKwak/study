# RMI(상대 모멘텀 지수) 평균회귀 스캘핑 [단타]

- **출처**: https://theforexgeek.com/relative-momentum-index/ , https://www.tradingpedia.com/forex-trading-
  indicators/relative-momentum-index/ , https://www.marketvolume.com/technicalanalysis/relativemomentumindex.asp
  (원조: Roger Altman, *Technical Analysis of Stocks & Commodities* 1993년 2월호에서 RSI의 변형으로
  최초 소개) + FMZ 전략 페이지(https://www.fmz.com/strategy/430902).
- **참여지표**: 단일 고참여 포스트 없음 — RSI의 변형 지표로 다수 트레이딩 교육 사이트·포럼에서 꾸준히
  다뤄지는 **고전 보조지표**. 조회수/추천수 수치 자체는 해당 없음(FX/주식권 오실레이터 문헌 다수 재인용).
- **백테스트 근거**: **없음(참여지표/이론 기반)**. 검색된 자료 어디에도 정량 백테스트 수치(승률·PF 등)
  없음 — 정직하게 "없음"으로 표기.
- **타임프레임**: 5m~15m (평균회귀 스캘핑에 적합한 저빈도 오실레이터 극단 신호 위주로 설계).
- **시장/대상**: BTC·ETH 등 메이저 무기한(변동성 큰 알트는 RMI 극단 지속 시간이 길어 휩쏘 위험 큼).

## 진입 규칙
- RMI 정의: RSI와 유사하나 "오늘 종가 대비 n봉 전 종가"의 상승/하락을 momentum(m)봉 동안 누적해
  계산(RSI의 1봉 비교 대신 m봉 비교로 완만화됨). 표준 파라미터: **length=14, momentum=5**.
- 롱: RMI가 **30 미만으로 하락했다가 다시 30을 상향 돌파**할 때 진입(과매도 이탈 반등 — 원문:
  "buying when RMI values advance above 30 after being below it").
  추가 필터(우리 설계, [추정] — 원문에 다른 지표와의 조합 규칙은 없어 스캘핑 실전성 위해 자체 부가):
  1h 추세 필터로 **EMA200 위**에서만 롱 신호 채택(카운터트렌드 리스크 축소).
- 숏: RMI가 **70 초과 후 다시 70을 하향 돌파**할 때 진입("selling when RMI values drop below 70 after
  being above it"). 1h EMA200 아래에서만 숏 채택([추정] 필터).
- 대안(레인지장 전용): RMI 50 중심선 크로스오버 또는 RMI-시그널라인(RMI의 EMA) 크로스 방식도 원문에
  소개되나, 본 스펙은 **과매수/과매도 반전형**을 1차 채택.

## 청산 규칙
- 익절: RMI가 반대 극단(롱 진입 시 **50 도달** 또는 **70 근접**)까지 회귀하면 청산. R:R 목표 1.5~2R
  기준 ATR 배수 병행 청산([추정] — 원문에 정량 익절 규칙 없음).
- 손절: 진입 신호 발생 봉의 **저가(롱)/고가(숏)** 아래·위, 또는 ATR×1.0~1.5 (원문에 정량 규칙 없어
  우리 표준 관행 적용 [추정]).
- 시간청산: 진입 후 N봉(예 20봉) 내 목표 미도달 시 강제청산 고려(레인지장 오실레이터 특성상 트렌드
  전환 시 장기간 물릴 위험 방지, [추정]).

## 파라미터
- rmi_length=14, rmi_momentum=5 (범위 length 10~20, momentum 3~10)
- oversold=30, overbought=70 (범위 20~35 / 65~80)
- trend_filter_ema=200 (1h)
- stop_atr_mult=1.0~1.5

## 코딩 난이도 / 데이터 요구
- 필요한 지표: RMI(RSI 계산 로직 재사용 가능 — up/down 비교 lookback을 1→momentum봉으로 변경만
  하면 됨), EMA200(1h 추세 필터용), ATR(손절폭).
- 전부 바이낸스 REST 캔들만으로 구현 가능. 오더북/틱데이터 불필요. 구현 난이도 낮음(RSI 구현체 재사용).

## 스카우트 메모
- 강점: 우리 저장소에 RSI·RSI2·Connors RSI·Stochastic RSI·CCI·CMO·MFI·Williams %R 등 오실레이터
  계열이 이미 많지만, **RMI는 "1봉 대신 m봉 비교"라는 명확히 다른 평활화 메커니즘**이라 로직 자체는
  신규. 다만 구조적으로 RSI 계열과 매우 유사해 **실질적 엣지 차별화는 의문**(RSI 대비 반응속도만 다름).
- 의심점: 정량 백테스트 전무 — 순수 이론적 신뢰도만 있음. 우리 프레임워크에서 이미 CCI-extreme,
  Williams %R, DeMarker 등 유사 계열 오실레이터 단타가 검증 대상이었던 만큼, **이 전략도 유사한
  방식(수수료 대비 저R)으로 FAIL할 위험 존재** — 저빈도·고R 필터(1h EMA200 트렌드 필터, ATR 손절)를
  반드시 적용해 검증해야 함.
- 우리 슬리브와의 관계: **대체 후보(약함)**. 현재 15m 단타 슬리브(볼린저 돌파+거래량+OI)와는 로직이
  다르나(모멘텀 반전형 vs 변동성 돌파형), 이미 다수의 유사 오실레이터 계열이 백테스트 후보군에
  있으므로 우선순위는 낮음. 참고용으로 축적.
