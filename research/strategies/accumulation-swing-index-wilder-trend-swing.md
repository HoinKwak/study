# [스윙] Wilder 누적스윙지수(Accumulative Swing Index, ASI) 추세확인 스윙

- **출처**: J. Welles Wilder Jr., "New Concepts in Technical Trading Systems" (1978). 참고 2차자료 — [LiteFinance](https://www.litefinance.org/blog/for-beginners/best-technical-indicators/accumulative-swing-index/), [Babypips Forexpedia](https://www.babypips.com/forexpedia/accumulative-swing-index), [Commodity.com](https://commodity.com/technical-analysis/accumulative-swing-index/), [CQG 헬프](https://help.cqg.com/cqgic/25/Documents/accumulativeswingindexasi.htm), [TradingView 오픈소스 스크립트(ASI)](https://my.tradingview.com/script/0uUgFLyi-Accumulation-Swing-Index-ASI/), [QuantifiedStrategies(원문 봇검증 차단으로 본문 미확인)](https://www.quantifiedstrategies.com/accumulative-swing-index/)
- **참여지표**: 개별 콘텐츠 조회수·좋아요 특정 실패(WebSearch 스니펫 기반). 다만 **Wilder의 원저(RSI·ADX·Parabolic SAR·ATR을 창시한 동일 저자)에서 나온 지표**로, 그의 다른 지표들은 이미 우리 레포에서 여러 형태로 채택돼 신뢰성 있는 계열임. ASI는 Wilder 본인이 "가격 데이터를 통틀어 가장 신뢰할 만한 단일 지표"라 자평했다고 다수 2차 자료가 인용(1차 원문 대조는 못 함).
- **백테스트 근거**: **없음(참여지표·저자 신뢰도 기반)**. QuantifiedStrategies 전용 페이지(Swing Index/ASI 각각)가 존재하나 Cloudflare 봇검증에 막혀 원문 승률·PF 확인 실패.
- **타임프레임**: 4h 신호 / 1d 추세 확인.
- **시장/대상**: BTC·ETH·주요 알트 USDT 무기한.

## 지표 정의 (Wilder 원 공식 — 4개 봉 가격축 O,H,L,C 사용, 크립토 적용 시 조정 필요 항목 명시)
1. K = `max(|High − PrevClose|, |Low − PrevClose|)`
2. R (조건부 선택, |H−PrevClose|·|L−PrevClose|·|H−L| 중 최댓값에 따라 분기):
   - `|H−PrevClose|`가 최대면: `R = (H−PrevClose) − 0.5×(L−PrevClose) + 0.25×(PrevClose−PrevOpen)`
   - `|L−PrevClose|`가 최대면: `R = (L−PrevClose) − 0.5×(H−PrevClose) + 0.25×(PrevClose−PrevOpen)`
   - `|H−L|`가 최대면: `R = (H−L) + 0.25×(PrevClose−PrevOpen)`
3. N = `(Close−PrevClose) + 0.5×(Close−Open) + 0.25×(PrevClose−PrevOpen)`
4. **T (Limit Move)**: Wilder 원 공식은 상품선물의 **일일 가격제한폭(daily limit move)**을 상수로 사용. **크립토 무기한은 가격제한이 없으므로 이 항이 정의 불가** — [조정] `T = ATR(14) × limit_proxy_mult`(기본 3.0)를 대체 상수로 사용. 이 대체는 원저자 의도와 다른 재해석이며, ASI 절대 스케일이 원 지표와 달라짐(추세/방향성 판정에는 영향 적으나 절대 레벨 비교엔 주의).
5. Swing Index(SI) = `50 × (N/R) × (K/T)`
6. **ASI(누적) = SI의 누적합(running cumulative sum)**. 장기간 누적 시 값이 발산하므로, 실전에서는 롤링 윈도우(예: 250봉)마다 리셋하거나 상대적 변화(기울기·최근 스윙고저)만 사용.

## 진입 규칙
- **추세 확인**: ASI(누적, 리셋 윈도우 250봉 내)를 SMA(14)와 비교. ASI > SMA14(ASI) 이면 상승추세, 반대면 하락추세.
- **롱**: ASI가 자신의 SMA(14)를 상향 돌파 + 가격이 1d EMA(50) 위(추세 정합) + 직전 ASI 프랙탈 저점(좌우 k=5봉) 대비 신저점을 만들지 않은 상태(구조 유지).
- **숏**: 반대 조건.
- (선택, [제안] 보강) **다이버전스 필터**: 가격은 신고점을 갱신하나 ASI는 이전 프랙탈 고점을 갱신 못 하면(약세 다이버전스) 신규 롱 진입 보류 — Wilder가 ASI를 주로 다이버전스/추세확인 용도로 설계한 취지 반영.

## 청산 규칙
- 익절: ATR(14) 기반 챈들리어 청산(신고가 − ATR×2.5, 신저가 + ATR×2.5 트레일링), 또는 ASI가 SMA(14)를 재차 역전할 때.
- 손절: 최근 ASI 프랙탈 저점(롱) 형성 시점의 가격, 또는 진입가 대비 ATR(14)×2.0 중 타이트한 쪽.
- 시간/조건 청산: ASI 리셋 윈도우 경계에서 포지션이 열려 있으면 재계산 정합성을 위해 강제 재평가(리셋 아티팩트 방지) — [제안] 안전장치.

## 파라미터
- limit_proxy_mult=3.0 (범위 2.0~5.0, ATR 기반 T 대체 상수)
- asi_reset_window=250 (범위 120~500봉)
- asi_sma_period=14 (범위 9~21)
- fractal_k=5 (범위 3~8)
- ema_trend_filter=50 (1d 기준, 범위 20~100)
- chandelier_atr_mult=2.5 (범위 2.0~3.5)
- stop_atr_mult=2.0 (범위 1.5~3.0)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: OHLC(공식 자체가 O,H,L,C 전부 사용, 거래량 불필요), ATR(14), SMA/EMA, 프랙탈 스윙고저. **전부 바이낸스 REST 캔들로 충족.**
- 난이도: **중간**. 공식 자체(조건 분기 3갈래)가 다소 복잡하고 버그 유발 여지가 있어 **단위테스트로 SI 계산을 수기 검증(알려진 예제 값 대조)한 뒤 사용 권장**. 오더북·틱·실시간청산 불필요.
- 주의: T(리밋무브) 대체 방식이 임의 재해석이므로, 원저자 ASI와 스케일이 다르다는 점을 백테스트 리뷰 시 명시해야 함(원문 그대로 재현이 아님).

## 스카우트 메모
- 강점: Wilder 원조 지표군(ADX·RSI·Parabolic SAR·ATR)의 계보로 개념적 신뢰도가 있고, O/H/L/C 4개 값을 모두 활용하는 유일한 지표라 우리 기존 지표군(대부분 종가 또는 종가+거래량 기반)과 계산축이 다름 — **신호 다양화 가치가 높음**.
- 의심점: (1) 정량 백테스트 전무. (2) 크립토엔 없는 "일일 가격제한폭"을 ATR로 대체하는 재해석이 필수라, 원 지표의 정확한 재현이 아님(원저자 의도와 스케일 괴리). (3) 공식이 복잡해 구현 버그 위험이 상대적으로 높음(계산 검증 없이 백테스트하면 결과 신뢰 불가) — Karpathy 원칙상 "결과가 이상하면 먼저 계측" 대상 1순위.
- 우리 단타 슬리브와의 관계: 무관(스윙 전용). 기존 `elder-*` 계열(Wilder와 다른 저자 Elder지만 유사한 "추세확인+다이버전스" 철학)과 개념적으로 인접하나 계산식은 완전히 다름 — 중복 아님. 백테스트 우선순위는 구현 검증 비용(단위테스트 필요) 때문에 중하위로 판단.
