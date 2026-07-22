# [단타] 액셀러레이션 밴드(Price Headley) 돌파 스캘프

- **출처**: https://www.quantifiedstrategies.com/acceleration-bands/ , https://trendspider.com/learning-center/getting-started-with-acceleration-bands-in-technical-analysis/ ,
  TradingView 공개 스크립트 "Indicator: Price Headley Accelaration Bands [LazyBear]" (https://kr.tradingview.com/script/wM2yTTOq-Indicator-Price-Headley-Accelaration-Bands-LazyBear)
  — 원 고안자 Price Headley(2002)
- **참여지표**: - (LazyBear 스크립트는 TradingView 레전드 퍼블리셔로 다수 파생 스크립트 존재, 정확한 좋아요 수 미확인)
- **백테스트 근거**: **정량 수치 원문 미확인.** QuantifiedStrategies 페이지는 봇검증으로 직접 확인 불가(백테스트 유무 자체 불명).
  Price Headley 본인의 규칙("연속 2봉 종가가 상단밴드 위로 마감 = 매수 시그널, 밴드 안으로 재진입 시 청산")은 다수 2차 자료에서
  일관되게 인용되나 **승률·PF 등 정량 실적은 어디서도 확인되지 않음**. 규칙 명확성 기반으로 채택, 근거등급은 "참여지표/규칙명확성" 수준.
- **타임프레임**: 5m~15m 신호
- **시장/대상**: BTC·ETH·주요 알트 무기물

## 핵심 아이디어
볼린저(표준편차)·켈트너(ATR) 밴드와 달리, **고가·저가의 순간 변동폭(range) 비율**로 밴드폭을 계산하는 것이 액셀러레이션 밴드의
차별점. `upper = high×(1+4×factor×(high-low)/(high+low))`, `lower = low×(1-4×factor×(high-low)/(high+low))`,
그 위에 SMA(중심선)을 얹는다. 우리 스택의 볼밴 돌파(`scalp15m`)·켈트너 돌파·TTM스퀴즈와 **밴드 산출 방식이 근본적으로 다른** 신규 변동성 채널.

## 진입 규칙
- 상단밴드(UB) = SMA(high×(1+4×k×(high-low)/(high+low)), band_len)
- 하단밴드(LB) = SMA(low×(1-4×k×(high-low)/(high+low)), band_len)
- 중심선(MB) = SMA(close, band_len)
- 롱: **연속 2봉 종가가 UB 위에서 마감**(close[t] > UB[t] and close[t-1] > UB[t-1]) **그리고** 거래량 ≥ vol_mult × SMA(volume,20)
  (원전엔 거래량 필터 없으나 우리 스캘프 관행상 추가 권장, A/B 비교 대상).
- 숏: 연속 2봉 종가가 LB 아래에서 마감 + 거래량 필터.
- (옵션) ADX(14) ≥ 20 필터로 무추세 구간의 잦은 돌파-되돌림(휩쏘) 배제.

## 청산 규칙
- 익절: 명시적 익절 없음(원전은 트레일링에 가까움) → 트레일링 스탑(중심선 MB 재진입 시 즉시 청산이 원전 규칙) 또는 ATR×1.5 트레일링.
- 손절: **가격이 밴드 안으로 재진입(종가가 MB와 진입측 밴드 사이로 복귀)한 즉시 청산** — 원전 핵심 규칙.
  보조 손절: 진입가 ∓ 1.0×ATR(14) (밴드 재진입 전에 급락 시 대비).
- 시간청산: max_hold=16봉(5m 기준 80분) 초과 시 강제 정리 — 원전엔 없으나 우리 관행상 추가.

## 파라미터
- band_len=20 (원전 표준, 범위 14~20)
- k(가속계수)=4 (원전 고정, 문헌에 따라 factor 자체가 4 포함식이라 조정 불필요)
- vol_mult=1.5 (범위 1.2~2.0, A/B: 필터 없음 버전과 비교)
- adx_min=20 (범위 15~25, off 옵션도 A/B)
- sl_atr_mult=1.0 (범위 0.8~1.5)
- max_hold=16봉

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 고가/저가 변동폭 기반 밴드(신규 구현 필요하나 수식 단순 — SMA 조합), 거래량 SMA, ADX(14), ATR(14).
- 주의: **바이낸스 REST 캔들(OHLCV)로 완전 충족.** 오더북/틱 불필요. 밴드 자체는 표준 지표 라이브러리에 없을 가능성이 높아 `ind.py`에
  신규 함수 하나(`acceleration_bands`) 추가 필요 — 계산은 rolling SMA 조합이라 간단.

## 스카우트 메모
- 강점: 볼린저/켈트너와 다른 변동폭 산출 방식이라 **밴드폭이 급변동 구간에서 더 민감하게 확장** — 스퀴즈 돌파형 우리 전략과 다른 신호 타이밍을
  낼 가능성. "연속 2봉 마감 확정" 규칙이 단봉 휩쏘를 어느 정도 걸러줌.
- 의심점: 정량 백테스트 전무 — 채택 전 반드시 자체 검증 필요. "밴드 재진입 시 즉시 청산"은 손절폭이 밴드폭에 좌우돼 변동성 낮은 구간엔
  손절이 너무 타이트해질 위험(수수료 0.14% 대비 손익비 악화 가능).
- 우리 단타 슬리브와의 관계: 기존 `scalp15m`(볼밴 이탈+거래량+OI 돌파)의 **밴드 산출식만 교체한 변형에 가까움** → 완전 신규라기보다
  "돌파 스캘프 계열의 대안 밴드 후보"로, 채택 시 기존 전략과의 상관관계(같은 신호를 다른 이름으로 내는지) 확인 필요.
