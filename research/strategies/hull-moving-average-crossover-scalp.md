# [단타] Hull Moving Average(HMA) 저지연 크로스오버 스캘프

- **출처**: https://hullmovingaverage.com/hull-moving-average-crossover-strategy/ , https://hullmovingaverage.com/hull-moving-average-scalping-strategy/ (HMA 전문 교육 사이트, 산식·권장 파라미터) /
  https://medium.com/@kridtapon/backtesting-the-hull-moving-average-crossover-strategy-with-cryptocurrencies-b0cd0f7efa14 (Kridtapon P., Medium — 암호화폐 대상 HMA 백테스트 예고 글, 본문 상세 수치는 WebFetch로 확보 실패) /
  원 산식: Alan Hull, 2005 개발
- **참여지표**: - (개인 블로그·교육사이트, SNS 참여지표 미확인). TradingView 내 "hullma" 검색 시 다수 파생 스크립트 존재(HMA는 TradingView 커뮤니티에서 EMA/SMA 다음으로 자주 언급되는 이동평균 계열 중 하나로 다수 2차 자료가 인용).
- **백테스트 근거**: **정량 수치 원문 미확인.** Kridtapon P.의 Medium 글은 "이전 이동평균 3종 비교에서 HMA가 최고 성과를 보여 이번엔 HMA로 암호화폐 백테스트를 진행한다"는 도입부만 WebFetch로 확인됐고, 본문의 실제 승률·수익률·샤프비율은 콘텐츠 절단으로 확보하지 못함. QuantifiedStrategies.com(주식 대상)도 봇 차단으로 원문 수치 확인 실패 — **"HMA는 평균회귀와 추세추종 모두에 쓰이며 저지연 설계로 반응이 빠르다"는 서술만 확인**, 정량 근거는 없음. **참여지표·설계 원리(공개 표준 산식) 기반으로만 채택**.
- **타임프레임**: 5m 신호 / 15m 확인 (스캘핑용 짧은 기간 권장)
- **시장/대상**: BTC·ETH 및 유동성 상위 알트 무기한

## 진입 규칙
- 산식(공개 표준, Alan Hull 2005): `HMA(n) = WMA( 2×WMA(price, n/2) − WMA(price, n), round(√n) )` (WMA=가중이동평균, price=종가)
- 듀얼 HMA: `HMA_fast(9)`, `HMA_slow(21)` (스캘핑 권장 기본값, 교육사이트 서술 근거).
- 롱: `HMA_fast`가 `HMA_slow`를 상향 돌파(crossover) **AND** `close > HMA_slow`(추세 정렬 확인).
- 숏: `HMA_fast`가 `HMA_slow`를 하향 돌파(crossunder) **AND** `close < HMA_slow`.
- 확인(선택): 15m HMA_fast 기울기가 같은 방향(가속)일 때만 진입 — 횡보장 휩쏘 억제.

## 청산 규칙
- 익절: 1.2~1.5R 도달 시 50% 분할, 잔량은 반대 크로스까지 트레일링.
- 손절: 진입가 ∓ 1.2×ATR(14), 또는 크로스 발생봉의 반대쪽 극값.
- 시간 청산: N=10~15봉(5m 기준 50분~1h15분) 내 미도달 시 청산(스캘프 특성상 저지연 신호가 빨리 소멸).

## 파라미터
- hma_fast=9 (범위 6~13)
- hma_slow=21 (범위 18~34)
- sl_atr_mult=1.2 (범위 1.0~1.8)
- rr_partial=1.2~1.5
- max_hold_bars=10~15 (5m 기준)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: WMA(가중이동평균) 2단 중첩 계산 — SMA/EMA보다 약간 복잡하나 **표준 공식 그대로 구현 가능**, 전부 캔들 종가로 산출.
- 주의: 오더북/틱/OI 불필요. 바이낸스 REST 캔들로 완전 충족. WMA 계산 시 초기 warm-up 구간(약 n+√n봉)을 버려야 함(일반 이동평균보다 워밍업 봉수 소폭 증가).

## 스카우트 메모
- 강점: 산식이 공개 표준이라 재현성 100%, EMA 대비 지연(lag)이 이론상 더 짧아 스캘핑 반응성 우위(설계 목적 자체가 "노이즈 제거+저지연"). 계산량이 가벼워 인프라 부담 없음.
- 의심점: **정량 백테스트 근거를 이번 조사에서 확보하지 못함** — 이번 라운드 후보 중 근거가 가장 약한 축에 속함. 기존 `ema-9-21-crossover.md`(EMA 크로스오버, 이미 보유)와 **컨셉이 거의 동일**(듀얼 이평 크로스)하여 HMA가 EMA 대비 실질적 우위가 있는지 반드시 A/B 백테스트로 직접 비교 검증 필요 — 우위 없으면 채택 의미 낮음.
- 우리 단타 슬리브와의 관계: 기존 EMA9/21 크로스오버 전략의 **직접 대체 후보**(같은 계열, 저지연 이평으로 교체 실험). 신규 축이 아니라 기존 전략의 변형이므로 우선순위는 중간 이하.
