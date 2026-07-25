# [스윙] FRAMA(프랙탈 적응 이동평균) 추세 크로스오버

- **출처**: John Ehlers, "Fractal Adaptive Moving Average" (Technical Analysis of Stocks & Commodities, 2005) — 공식 자체는 업계 공개(공식·특허 아님). 정리 보강:
  https://www.quantifiedstrategies.com/fractal-adaptive-moving-average-frama/ (WebFetch 봇검증으로 실패) ,
  https://www.luxalgo.com/blog/kama-vs-frama-comparing-adaptive-moving-averages/ ,
  https://pyquantlab.medium.com/fractal-adaptive-moving-average-frama-length-bounds-tuning-across-crypto-volatility-regimes-d5252103cb17 (**크립토 변동성 국면별 FRAMA 튜닝 다룬 글이나 WebFetch로는 서론만 확인, 본문 페이월/미노출 — 백테스트 수치 확보 실패**)
- **참여지표**: - (Ehlers 공식 지표 자체는 TradingView·MT5·다수 플랫폼에 표준 내장돼 널리 쓰이나, 개별 게시물의 조회수·좋아요는 확인 못함)
- **백테스트 근거**: **없음(원문 백테스트 수치 확보 실패, 정직하게 미기재)**. 확인된 것은 지표 공식과 정성적 설명뿐: "FRAMA는 가격의 프랙탈 차원(fractal dimension)을 계산해 추세가 강할 때(차원→1)는 빠르게 반응하고, 횡보 노이즈일 때(차원→2)는 느리게(평평하게) 움직이도록 스스로 기간을 조절하는 적응형 이동평균"(Ehlers 2005 원 설계, 다수 2차 자료가 일관되게 인용). **크립토 대상 정량 백테스트는 찾지 못함** — 공식 자체의 재현성·범용성(다수 플랫폼 표준 내장)으로 스크리닝, 채택 전 자체 백테스트 필수.
- **타임프레임**: 4h~1d 스윙 권장(적응형 MA는 원래 어떤 TF에도 정의되나, 추세추종 특성상 저TF는 휩쏘 위험 큼).
- **시장/대상**: BTC·ETH·시총상위 알트 무기한

## 지표 정의 (Ehlers 2005 공식)
1. 기간 N(짝수, 기본 16)을 절반씩 나눠 앞 N/2·뒤 N/2 구간 각각의 (최고가−최저가)/(N/2)를 계산 → HL1, HL2.
2. 전체 N구간의 (최고가−최저가)/N → HL3.
3. **프랙탈 차원 D = (log(HL1+HL2) − log(HL3)) / log(2)**, D는 통상 1.0~2.0 사이로 클램프.
4. **스무딩 계수 alpha = exp(-4.6 × (D − 1))**, alpha를 [alpha_slow, alpha_fast] 범위로 클램프
   (alpha_fast = 2/(FC+1), FC=1 → 1.0 근접 / alpha_slow = 2/(SC+1), SC=198 기본 → 0.01 근접).
5. **FRAMA_t = alpha × Price_t + (1 − alpha) × FRAMA_{t-1}** (EMA와 동일 재귀식이나 alpha가 매 봉 프랙탈 차원에 따라 자동 변함).

## 진입 규칙
- 롱: 종가가 **FRAMA 라인을 상향 돌파**(직전 봉 종가 ≤ FRAMA, 현재 봉 종가 > FRAMA) **그리고** FRAMA 라인 자체가 최근 slope_bars(예 3봉) 동안 상승 기울기(휩쏘 방지 — 라인이 아직 평평/하락 중이면 신호 무시).
- 숏: 종가가 **FRAMA 라인을 하향 돌파** + FRAMA 라인이 하락 기울기.
- (선택 필터) 상위TF(1d) FRAMA 방향과 일치할 때만 4h 신호 채택(멀티TF 정렬, 우리 프레임워크의 상위TF 확인 관례 재사용).

## 청산 규칙
- 익절: 없음(추세추종 — 반대 크로스까지 보유) 또는 트레일링(ATR×2.0, 신고가/신저가 기준).
- 손절: 진입가 대비 -(1.5~2.0)×ATR(14).
- 시간/조건 청산: 종가가 반대 방향으로 FRAMA 재크로스하면 즉시 청산(추세 소멸).

## 파라미터
- frama_n=16 (범위 10~26, 짝수만)
- fc=1, sc=198 (Ehlers 표준값 — 통상 고정, 필요 시 sc 범위 100~300으로 스윕해 민감도 확인)
- slope_bars=3 (범위 2~5)
- sl_atr_mult=1.8 (범위 1.5~2.5)
- trail_atr_mult=2.0 (범위 1.5~3.0, 트레일링 옵션 사용 시)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: OHLC(고가·저가로 프랙탈 차원 계산) + ATR14. 재귀식(EMA류)이라 벡터화 다소 까다로움(pandas rolling으로 HL1/HL2/HL3 계산 후 순차 루프로 FRAMA 누적 계산 필요) — 난이도 중간(우리 기존 KAMA/HMA/T3 구현 경험 재사용 가능).
- 주의: 바이낸스 REST 캔들만으로 완전 충족.

## 스카우트 메모
- 강점: **공식이 완전히 결정론적이고 공개**(Ehlers 저서 기반, 특정 벤더 종속 없음) — 코딩 가능성 확신도 높음. 우리가 이미 가진 KAMA(효율성비율 기반)와 달리 **프랙탈 차원**이라는 다른 수학적 근거로 적응 속도를 조절해 상관관계 낮은 신호일 가능성.
- 의심점: **정량 백테스트 근거를 전혀 확보하지 못함**(quantifiedstrategies 봇검증 차단, PyQuantLab Medium 글은 서론만 노출). 참여지표도 특정 게시물 단위로는 미확인 — 이번 발굴 중 가장 약한 근거(공식의 공개성·재현성만으로 스크리닝). **채택 우선순위는 낮게, 반드시 처음부터 검증**.
- 우리 슬리브와의 관계: `kama-atr-adaptive-trend-swing.md`, `hull-moving-average-crossover-scalp.md`, `tillson-t3-moving-average-crossover-swing.md`, `mcginley-dynamic-adaptive-ma-crossover-swing.md`, `zero-lag-ema-crossover-trend-swing.md`와 같은 "적응형/저지연 MA 크로스오버" 계열의 또 다른 변형 — **이 계열이 이미 5종 존재**하므로 신규성은 제한적(수학적 근거만 다름). 우선순위는 KAMA 등 기존 검증 결과를 먼저 확인한 뒤 판단 권장.
