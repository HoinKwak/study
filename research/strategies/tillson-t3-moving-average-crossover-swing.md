# [스윙] Tillson T3 이동평균 추세추종

- **출처**: https://www.tradingview.com/script/hvVCxPmR-Tillson-T3-Moving-Average-improved/ (TradingView, gstoyanov) / https://medium.com/@FMZQuant/multi-moving-average-crossover-trend-following-strategy-1b85c691abcb (FMZQuant, 크립토 적용판 서술) / 원 이론: Tim Tillson, "Smoothing Techniques For More Accurate Signals" (Stocks & Commodities, 1998)
- **참여지표**: TradingView 좋아요/부스트 **2,798** (2026-07 WebFetch 확인). FMZQuant Medium 글은 좋아요·조회수 비공개(Medium 특성상 확인 불가) — "-"로 표기.
- **백테스트 근거**: **없음(참여지표 기반)**. FMZQuant 글은 2024년 5월 BTC/USDT 선물 1h 캔들로 백테스트 화면을 제시했다고 WebFetch로 확인되나, **실제 수익률·승률·PF 등 정량 성과 수치는 원문에 없음**(원문 확인 결과 "프레임워크 제시" 수준, 파라미터 최적화 필요하다고 명시) — 지어내지 않고 정직히 "수치 부재"로 표기.
- **타임프레임**: 4h 신호 / 1d 확인
- **시장/대상**: BTC·ETH·시총상위 알트 무기한

## 진입 규칙
- T3 계산(Tillson, 6단 캐스케이드 EMA): `GD(x,n,vf) = EMA(x,n)*(1+vf) - EMA(EMA(x,n),n)*vf` (Generalized DEMA). `e1=GD(price,n,vf)`, `e2=GD(e1,n,vf)`, `T3=GD(e2,n,vf)` (3중 GD 적용, 사실상 6개 EMA 캐스케이드). `n`=길이(기본 8), `vf`=volume factor(기본 0.7, 0~1 범위 — 클수록 반응 빠르고 오버슈트 큼).
- 롱: **T3(fast, n=8)가 T3(slow, n=21)를 상향 돌파** **AND** T3(fast) 기울기(현재값 − 3봉 전 값) > 0.
- 숏: **T3(fast)가 T3(slow)를 하향 돌파** **AND** T3(fast) 기울기 < 0.
- (대안 진입, FMZQuant 크립토 적용판) 단일 T3 밴드(T3 ± ATR)를 사용해 종가가 T3 상단 밴드 상향 돌파 시 롱, 하단 밴드 하향 돌파 시 숏.

## 청산 규칙
- 익절: 반대 크로스 발생 시 청산, 또는 ATR 트레일링(신고가−ATR×2.0).
- 손절: 진입가 대비 ATR(14) × 2.0, 또는 T3(slow) 재돌파 시 청산.
- 시간 청산: 명시 없음(추세추종, 반대신호 우선 청산).

## 파라미터
- t3_fast_len=8 (범위 5~10), t3_slow_len=21 (범위 18~34)
- volume_factor=0.7 (범위 0.5~0.9)
- atr_period=14, atr_sl_mult=2.0 (범위 1.5~3.0)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: T3(6단 캐스케이드 EMA, GD 함수 3회 적용), ATR(14). 전부 바이낸스 OHLCV 캔들로 계산 가능.
- 주의: T3는 EMA를 6번 중첩 계산하는 구조라 계산 자체는 단순 재귀지만 **워밍업 구간(수십 봉)이 다른 이평보다 김** — 백테스트 시 초기 구간 신호 제외 필요. 오더북/틱 불필요.

## 스카우트 메모
- 강점: Tillson 원저자 주장은 "일반 EMA·DEMA·TEMA보다 랙이 짧으면서 오버슈트(과잉반응)는 TEMA보다 적다"는 것 — 우리가 이미 보유한 저지연 MA 계열(McGinley, KAMA, ZLEMA 후보)과 다른 산식 계열(다단 GD 캐스케이드)이라 신호 상관도가 낮을 가능성. 규칙 자체는 단순 크로스오버로 구현 쉬움.
- 의심점: 정량 백테스트 근거가 전무(참여지표도 2.8K로 중간 수준) → 최우선순위는 아님. FMZQuant 원문도 "추가 필터·동적 손절 없이는 실전 배치 부적합"이라 명시(WebFetch로 확인) — 단독 크로스오버만으론 우리가 이미 겪은 EMA9/21 실패(과빈발 휩쏘)를 반복할 위험.
- 우리 스윙 슬리브와의 관계: `mcginley-dynamic-adaptive-ma-crossover-swing.md`, `kama-atr-adaptive-trend-swing.md`, `mama-fama-adaptive-crossover-swing.md`와 "적응형/저지연 이평 크로스오버" 계열로 개념이 겹침(산식 상이). 백테스트 우선순위는 낮게 두고, 채택 시 기존 적응형 MA 계열과 앙상블/비교 목적으로 활용 권장.
