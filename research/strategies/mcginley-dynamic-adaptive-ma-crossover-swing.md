# [스윙] McGinley Dynamic 적응형 이동평균 크로스오버 추세추종

- **출처**: https://sfericatrading.com/articles/the-mcginley-dynamic-a-revolutionary-trading-strategy (전략 규칙·성과범위, WebFetch 원문 확인) / https://www.altrady.com/blog/crypto-trading-strategies/mcginley-dynamic-indicator (크립토 적용 가이드, WebFetch 원문 확인 — 단 이 글엔 파라미터·백테스트 수치 없음) / https://www.quantifiedstrategies.com/mcginley-dynamic/ (전용 백테스트 페이지 존재하나 봇차단으로 원문 미확인)
- **참여지표**: - (블로그/가이드 기반, 조회수·추천수 비공개)
- **백테스트 근거**: sfericatrading 원문에 **"Profit Factor 1.7~2.2, 승률 60% 이상(consistently)"** 로 명시(WebFetch 확인). 단 **표본수·정확 기간·정확 자산(코인 티커)·수수료 반영 여부 전부 미기재** — 원문 표현이 "크립토·외환·주식 등 다양한 자산군에서 백테스트됨"이라는 정성적 언급뿐이라 **크립토 전용 수치가 아님**을 명확히 함. altrady(크립토 전용 가이드)는 정성적 규칙만 제공하고 수치 백테스트는 없음. **종합: 참여지표는 약하고, 백테스트는 존재하나 방법론 불투명 → 재검증 필수 등급.**
- **타임프레임**: 4h 신호 / 1d 확인 (원문은 "higher timeframe 권장"만 언급, 구체 TF는 [설계 판단]으로 4h/1d 채택)
- **시장/대상**: BTC·ETH 등 유동성 높은 메이저 무기한 (원문이 "박한 알트는 피하라" 권고)

## 핵심 아이디어 (신규성)
- McGinley Dynamic(MD)은 단순/지수 이동평균과 달리 **자기참조형 스무딩**(속도에 따라 반응성이 자동 조절)으로, 급등락 구간에서 EMA/SMA보다 지연이 적다고 알려진 지표. 우리 스택엔 적응형 MA로 KAMA·MAMA/FAMA·Hull이 있으나 **McGinley는 계산식(가격 대비 이전 MD값의 4제곱 비율로 스무딩 팩터 조정)이 이들과 근본적으로 다른 별도 계열**이며, 국내 코드베이스에 아직 없음.

## 진입 규칙
- **MD 공식(표준, 공개 자료)**: `MD_t = MD_{t-1} + (Close_t - MD_{t-1}) / (N * (Close_t / MD_{t-1})^4)`, 초기값 MD_0 = 첫 종가, N=기간(기본 14).
- 롱: 가격이 MD선 **위에서 유지**되고 MD선 자체가 **상향 전환**(기울기 양전환) + 되돌림이 얕게(예: 최근 5봉 내 MD 재이탈 없음) 통제될 때 진입. (원문 정성적 표현 "price holds above line while line turns higher and pullbacks remain controlled"을 [해석 판단]으로 수치화: 종가가 N_confirm(3)봉 연속 MD 위 유지 + MD 기울기(현재−N봉전) > 0.)
- 숏: 대칭 — 가격이 MD 아래 유지 + MD 하향 전환 + 반등이 통제됨.
- (원문 권고 필터, 파라미터 미공개라 대체 지표로 대응) 추세 컨텍스트 확인용 EMA(50) 방향 일치 또는 ADX(14) ≥ 20.

## 청산 규칙
- 손절: ATR 밴드 기반 — 원문은 "ATR 밴드로 동적 SL/TP"만 언급, 구체 배수 없음. [설계 판단] 진입가 ∓ 1.5×ATR(14).
- 익절: MD선 대비 반대 방향 이탈(추세 전환 신호) 또는 2.0~3.0×ATR 고정 목표. 트레일링(MD선 자체를 트레일 스탑으로 사용, 종가가 MD를 반대로 이탈하면 청산)도 원문 취지에 부합.
- 시간 청산: 없음(추세추종형, 추세 지속되는 한 보유). 다만 max_hold 안전장치(예: 4h TF 120봉≈20일) 권장.

## 파라미터
- md_period=14 (범위 10~20)
- confirm_bars=3 (범위 2~5)
- atr_period=14, atr_stop_mult=1.5 (범위 1.0~2.5)
- atr_tp_mult=2.5 (범위 2.0~3.5)
- trend_filter=EMA50 방향 또는 ADX14≥20 (A/B 비교 권장)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: McGinley Dynamic(자체 구현 필요, 표준 라이브러리에 드묾 — 재귀식이라 벡터화 시 루프 필요), ATR, EMA50 또는 ADX.
- 주의: 재귀식이므로 판다스 벡터화가 아닌 순차 계산(for-loop 또는 numba) 필요 — 백테스트 속도 이슈 가능. 바이낸스 REST OHLCV만으로 계산 가능(추가 데이터소스 불필요).

## 스카우트 메모
- 강점: 계산식이 명확하고 공개되어 있어 구현 난이도는 낮음(재귀 루프만 주의). 자기참조형 스무딩이라 EMA/SMA 크로스오버보다 휩쏘가 적다는 이론적 근거는 있음.
- 의심점: 유일한 정량 백테스트 근거(PF1.7~2.2, WR60%+)가 **자산·기간·표본수 불명, 크립토 전용 아님** — 마케팅성 블로그 수치일 가능성 배제 못함. 반드시 자체 재현 필요.
- 우리 스택과의 관계: KAMA-ATR-Adaptive-Trend-Swing, MAMA/FAMA와 "적응형 MA 추세추종" 계열로 겹치는 컨셉이나 **계산식 자체는 완전히 다른 지표**라 신규 후보로 유지. 다만 이미 적응형 MA 계열 2개(KAMA, MAMA/FAMA)가 FAIL/보유 목록에 있다면 이 전략도 유사한 결과(휩쏘 취약)를 보일 가능성 있음 — 우선순위는 중간.
