# [단타] 볼륨 프로파일 POC/Value Area 되돌림·이탈 (15m 신호/1h 확인)

- **출처**: https://www.futureshive.com/blog/volume-profile-trading-strategy-2025 (FuturesHive, ES/NQ 인트라데이 볼륨프로파일 전략) /
  https://www.quantum-algo.com/blog/guides/volume-profile-trading-complete-guide/ (Quantum Algo, POC/VAH/VAL 정의·전략 가이드) /
  https://www.tradezella.com/strategies/volume-profile-strategy (TradeZella) /
  https://forextester.com/blog/fixed-range-volume-profile/ (ForexTester, Fixed Range Volume Profile 백테스트 방법론)
- **참여지표**: 없음(퀀트/트레이딩 교육 블로그 다수, 개별 조회수 확인 불가) — SNS 참여지표 미확인
- **백테스트 근거**: **구체적 표본 수치 없음** — FuturesHive는 "적절히 필터링하면 볼륨프로파일 셋업은 50~60% 승률을 낼 수 있고, 정밀한 진입/손절/목표가 설정 시 70%+ 승률 트레이드로 전환 가능"이라 서술하나 표본 기간·거래 수·자산 미기재(선물 지수 ES/NQ 기준, 크립토 재현 미검증). LVN(저거래구간) 브레이크아웃은 "승률은 낮지만 R:R 3:1~5:1로 상쇄" 구조라고 명시. **정량 백테스트가 아닌 업계 관행치이므로 참고 수준으로만 취급, 자체 검증 필수**.
- **타임프레임**: 15m 신호 / 1h 확인(직전 24시간 세션 기준 볼륨프로파일)
- **시장/대상**: BTC·ETH·시총상위 알트 무기한(24시간 거래대금 충분해야 볼륨프로파일이 유의미)

## 진입 규칙
- **볼륨프로파일 구성**: 직전 24시간(15m×96봉)의 캔들들을 가격 구간 N=24개 빈(bin)으로 나누고, 각 봉의 거래량을 해당 봉의 고가~저가 구간에 균등 분배해 누적 → 최고 거래량 구간의 중심가를 **POC**, 누적거래량 70%를 포함하는 구간의 상/하단을 **VAH/VAL**로 산출. 매 15m 봉마다 롤링 재계산.
- **Value Area 바운스(평균회귀, 우선 채택)**:
  - 롱: 15m 종가가 VAL 하단을 터치 후 VAL 위로 재진입(되돌림) + RSI(14, 15m) < 40.
  - 숏: 15m 종가가 VAH 상단을 터치 후 VAH 아래로 재진입 + RSI(14, 15m) > 60.
- **LVN(저거래구간) 브레이크아웃(추세추종, 승률 낮음·R:R 큼)**:
  - 롱: 가격이 POC 위쪽의 저거래구간(빈 거래량이 전체 평균의 40% 이하인 구간)을 거래량 급증(직전 20봉 평균 대비 2배 이상) 동반 상향 통과.
  - 숏: 대칭.

## 청산 규칙
- **Value Area 바운스 익절**: POC 도달(1차 50%) → 반대편 Value Area 경계(2차 나머지) 분할청산.
- **LVN 브레이크아웃 익절**: 다음 고거래구간(HVN)까지, 최소 R:R 3:1.
- **손절**: Value Area 바운스는 VAL/VAH를 0.3×ATR만큼 재이탈 시. LVN 브레이크아웃은 돌파 시작점(LVN 진입가) 재이탈 시.
- **시간 청산**: 진입 후 12봉(15m×12=3시간) 내 목표 미도달 시 강제청산(세션이 바뀌며 프로파일 자체가 무효화되므로).

## 파라미터
- profile_lookback_bars=96 (15m 기준 24시간, 범위 48~192)
- profile_bins=24 (범위 16~40)
- value_area_pct=0.70 (범위 0.60~0.75)
- lvn_threshold=0.40×평균빈거래량 (범위 0.3~0.5)
- vol_spike_mult=2.0 (LVN 브레이크아웃용)
- rsi_long_max=40, rsi_short_min=60 (VA 바운스용)
- max_hold_bars=12

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 볼륨프로파일(캔들 고저·거래량으로 근사 구성 — 진짜 틱/오더북 기반 volume-at-price 아님), RSI, ATR, 거래량 급증 배율.
- 주의: **정밀한 volume profile은 원래 틱/오더북 체결가 분포가 필요**하나, 우리는 캔들의 고가~저가 구간에 거래량을 균등 분배하는 **근사(approximation) 방식**을 쓴다 — 실제 POC/VA 위치가 진짜 volume-at-price보다 부정확할 수 있음(이 점이 이 전략의 핵심 한계). 바이낸스 REST 15m 캔들(OHLCV)만으로 계산 가능, 별도 데이터 불필요.

## 스카우트 메모
- **강점**: 캔들 데이터만으로 근사 구현 가능해 우리 인프라와 궁합이 좋음. Value Area 바운스는 사실상 "거래량 가중 지지/저항에서의 평균회귀"라 로직이 상식적이고 디버깅하기 쉬움.
- **의심점**: 근사 볼륨프로파일의 정확도가 낮을 수 있어 진짜 volume-at-price 대비 신호 품질 저하 우려. 정량 백테스트 근거 부재(업계 관행치만 존재) — **자체 검증 필수, 백테스트 우선순위에서는 후순위**.
- **우리 슬리브와의 관계**: 기존 `prior-day-high-low-retest.md`(전일 고저 리테스트)·`weekly-structure-breakout-retest.md`(주간 구조)와 "특정 가격대 재테스트"라는 구조는 비슷하지만, 여기는 **거래량 가중** 레벨(단순 고저가 아님)이라는 점에서 차별화됨. 기존 단타 슬리브(볼린저+거래량+OI)와는 다른 구조적 레벨(POC/VA)을 쓰므로 **보완재**로 볼 수 있음.
