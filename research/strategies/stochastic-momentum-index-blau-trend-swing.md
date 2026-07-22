# [스윙] 스토캐스틱 모멘텀 인덱스(SMI, Blau) 추세추종

- **출처**: https://medium.com/@FMZQuant/quantitative-trading-strategy-based-on-stochastics-momentum-index-4a217017aff8 (FMZQuant, 계산식·파라미터·백테스트
  대상/기간 명시) / https://www.quantifiedstrategies.com/stochastic-momentum-index/ (봇차단으로 원문 직접 확인 불가, 보조 인용만) /
  개발자 William Blau
- **참여지표**: - (FMZQuant Medium 시리즈 글, 좋아요/조회수 미확인)
- **백테스트 근거**: FMZQuant 원문에서 **직접 확인**: 대상 **BTC_USDT 선물**, 기간 **2023-03-05 ~ 2024-03-10**, 신호는 1시간봉 기반.
  파라미터 %K Length=10, %D Length=3, Overbought=+40, Oversold=-40. **단, 원문에 정확한 승률·수익률·PF 수치는 명시돼 있지 않음**
  (계산식·규칙·대상·기간만 확인, 성과 수치는 없음 → "백테스트 실행 근거는 있으나 성과 수치는 미기재"로 정직히 표기).
  참고로 QuantifiedStrategies류의 2차 요약(원문 미확인)엔 "SMI 추세추종은 금·비트코인에서 우수, 주식엔 약함, buy&hold와
  비슷한 CAGR에 낮은 MDD"라는 정성적 언급이 있으나 수치 미확인이라 신뢰도 낮게 취급.
- **타임프레임**: 1h 신호(원문 기준) / 4h 추세 필터
- **시장/대상**: BTC 무기물(원문 대상), ETH·주요 알트로 확장 검증 필요

## 핵심 아이디어
스토캐스틱 오실레이터의 개선판으로, **종가가 최근 N봉 고저 범위의 "중점(midpoint)"으로부터 얼마나 떨어져 있는지**를 이중 EMA
평활한 값을 사용. 우리 스택의 `stochastic-rsi-ema-adx`(스토캐스틱 RSI, RSI에 스토캐스틱 적용)와는 **계산 기반 자체가 다르다**
(SMI는 RSI를 거치지 않고 가격 range의 중점 거리 직접 사용 + 이중 평활).

## 진입 규칙
- **SMI 계산**: `range_mid = (highest_high(k_len) + lowest_low(k_len)) / 2`, `rel_diff = close - range_mid`,
  `rel_range = highest_high(k_len) - lowest_low(k_len)`. `rel_diff`, `rel_range` 각각 이중 EMA 평활(EMA(EMA(x, d_len), d_len))
  후 `SMI = 100 × smoothed_rel_diff / (0.5 × smoothed_rel_range)`.
- **시그널선** = EMA(SMI, d_len=3).
- 롱: SMI가 **oversold(-40) 아래에서 형성 후 시그널선을 상향 돌파**(원전 크로스오버 규칙) **그리고** 4h 추세필터(EMA50 상승 또는
  가격>EMA200)로 순추세 방향만 채택.
- 숏: SMI가 **overbought(+40) 위에서 형성 후 시그널선을 하향 돌파** + 4h 추세필터 하락 방향.
- (대안, 추세추종 버전) 절대값 크로스오버만 사용: SMI가 시그널선을 상향/하향 돌파할 때마다 진입(레인지 필터 없이) — 원문의
  "추세추종형 SMI 전략"에 해당, oversold/overbought 진입판(역추세형)과 A/B 비교 대상.

## 청산 규칙
- 익절: 반대 크로스오버(SMI가 시그널선을 반대로 돌파) 시 청산 및 반전 진입, 또는 SMI가 반대편 극단(±40) 도달 시 부분청산.
- 손절: 진입가 ∓ 2.0×ATR(14, 4h) 또는 최근 스윙 고/저점.
- 시간청산: max_hold=40봉(1h 기준 약 1.7일, 스윙 관점에선 4h로 환산해 재조정 검토) 초과 시 청산 검토.

## 파라미터
- k_len=10 (원전, 범위 8~14)
- d_len=3 (원전, 범위 3~5, 이중평활 기간과 시그널선 기간 동일값 사용이 관행)
- ob=+40, os=-40 (원전 고정, 범위 ±35~45)
- trend_ema=50/200 (4h)
- sl_atr_mult=2.0 (범위 1.5~2.5)
- max_hold=40봉(1h) 또는 4h 재계산 시 10봉

## 코딩 난이도 / 데이터 요구
- 필요한 지표: rolling max/min(highest_high, lowest_low), 이중 EMA 평활, EMA(시그널선), ATR(14), EMA(50/200, 상위TF).
- 주의: **바이낸스 REST 캔들로 완전 충족.** 오더북/틱/OI 불필요. SMI 자체는 기존 지표 라이브러리에 없을 가능성 높아 `ind.py`에
  신규 함수 필요(이중 EMA 평활 로직만 정확히 구현하면 스토캐스틱류와 유사한 난이도).

## 스카우트 메모
- 강점: 계산식·파라미터·대상자산·기간이 1차 출처(FMZQuant)에서 명확히 확인됨(단, 성과수치는 없음). 우리 스택에 없는 "이중평활 스토캐스틱"
  계열이라 신호 타이밍이 기존 스토캐스틱RSI 스윙과 다를 가능성.
- 의심점: 성과 수치(승률/PF/수익률)가 원문에 없어 **채택 전 자체 백테스트가 필수**(현재는 규칙명확성+1차 출처 확인 수준의 근거).
  2차 출처의 "금·BTC에서 우수" 주장은 원문 확인 실패로 신뢰도 낮음.
- 우리 단타 슬리브와의 관계: `stochastic-rsi-ema-adx-swing`(스윙)과 **개념적으로 인접**하나 산출 방식이 달라 상관관계 확인 후
  중복 여부 판단 필요. 대체보다는 "스토캐스틱 계열 대안" 성격.
