# [스윙] Ehlers Instantaneous Trendline 크로스오버 추세추종

- **출처**: https://www.quantifiedstrategies.com/john-ehlers-trading-strategy/ (QuantifiedStrategies — 원문 사이트가 봇 차단으로 WebFetch 직접 접근 불가. **WebSearch 스니펫으로 2회 독립 검색·교차확인**한 인용) / https://www.elitetrader.com/et/threads/john-ehlers-trading-strategy-the-instantaneous-trendline-backtest.374341/ (Elite Trader 포럼 — 403으로 WebFetch 불가, 제목만 확인) / 원 지표: John Ehlers, *Cybernetic Analysis for Stocks and Futures* (2004) / Stocks & Commodities 2006년 8월호 "Modeling The Market"
- **참여지표**: - (퀀트 블로그·포럼 반복 게재. TradingView에 다수 파생 스크립트 존재하나 개별 좋아요 수는 확인 안 함)
- **백테스트 근거**: **⚠️ 원문 WebFetch 직접 확인 실패 — WebSearch 엔진이 반환한 페이지 스니펫만으로 교차확인**(같은 수치가 서로 다른 검색 질의 2회에서 동일하게 재현돼 신뢰도는 있으나, 원문 대조는 못함. 정직하게 "검색엔진 스니펫 인용"으로 표기).
  - 인용 수치: **"Testing on XBTUSD pair with 4h timeframe from 2016-2020 showed approximately 20% drawdown with a Sharpe ratio of 0.361."** 저자 자신이 "not too impressive"라고 평가.
  - 같은 소스: 주식/선물(E-mini, SPY) 대상 원조 추세추종형(IT가 지연선 상향돌파=롱)은 성과 부진("significant drawdowns"). **역발상 평균회귀 버전**(IT가 지연선 **아래로** 크로스할 때 롱)은 SPY에서 연 10.56% 수익·MDD 23.96% — **단, 이건 주식 대상이며 크립토 검증 없음**.
  - **결론**: 크립토(XBTUSD 4h)에서 실측된 것은 원조 추세추종 버전뿐이고 Sharpe 0.36으로 약한 엣지. 평균회귀 변형은 크립토 미검증(주식 전용).
- **타임프레임**: 4h (크립토 유일 실측 TF). 1d 확인 필터 권장.
- **시장/대상**: BTC 무기한 (원문은 XBTUSD, BitMEX 표기 — 바이낸스 BTCUSDT 무기한으로 대체)

## 진입 규칙
- **Instantaneous Trendline(IT) 계산** (Ehlers 2폴 필터, `alpha=0.07` 기본):
  `IT[i] = (α - α²/4)·P[i] + 0.5α²·P[i-1] - (α - 0.75α²)·P[i-2] + 2(1-α)·IT[i-1] - (1-α)²·IT[i-2]`
  (초기 2~6봉은 `IT[i] = (P[i] + 2P[i-1] + P[i-2]) / 4`로 시드)
- **Trigger(지연 제거선)**: `Trigger[i] = 2·IT[i-1] - IT[i-2]`
- 롱(원조 추세추종): IT가 Trigger를 **상향 돌파**.
- 숏(원조 추세추종): IT가 Trigger를 **하향 돌파**.
- (미검증 옵션, 주식전용 근거) 평균회귀 버전: IT가 Trigger를 하향 돌파할 때 롱 진입(역발상) — 크립토 재현 여부 확인 전엔 채택 보류.

## 청산 규칙
- 익절: 반대 크로스 발생 시 청산·반전(스탑앤리버스 방식이 원문 기본).
- 손절: 원문에 명시 없음 — 채택 시 진입가 ∓ ATR(14, 4h)×2.0 보완 필수(Sharpe 0.36이 약하므로 손절 없이 그대로 쓰면 위험).
- 시간 청산: 원문 없음 — 최대 홀딩 상한(예: 30~40봉, 4h 기준 5~7일) 권장.

## 파라미터
- alpha=0.07 (범위 0.03~0.15, 낮을수록 더 부드럽고 지연 증가)
- trigger_lag=2봉 (고정, 공식상 필수)
- (보완) sl_atr_mult=2.0, max_hold_bars=36 (4h 기준)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 종가만으로 계산되는 2폴 재귀 필터(IT) + 파생 Trigger선. ATR(14)은 보완 손절용.
- 난이도: **중간**. 재귀 필터라 초기 시드·NaN 처리에 주의(첫 7봉은 특수 공식). 바이낸스 REST 종가만으로 100% 계산 가능 — 오더북/틱 불필요.
- 주의: 원문 백테스트 자체가 "약한 엣지"라고 자평(Sharpe 0.36) — 단독 전략보다 **레짐/트렌드 필터 후보**로 검증하는 편이 합리적일 수 있음.

## 스카우트 메모
- **강점**: 우리 193개 기존 스펙에 없는 **신규 Ehlers 지표**(Cyber Cycle·Laguerre RSI·MAMA-FAMA·Gaussian Channel은 이미 있으나 Instantaneous Trendline은 처음). 재귀 2폴 필터라 일반 이평보다 노이즈 억제력이 이론상 우수.
- **의심점**: (1) 원문 자체가 크립토 성과를 "인상적이지 않다"고 명시 — PASS 기준 미달 가능성 높음. (2) 원문 페이지를 WebFetch로 직접 대조하지 못해 **정량 수치는 검색엔진 스니펫 인용**(원칙상 최하위 신뢰도 — 백테스터 실행 전 가능하면 1차 소스 재확인 권장). (3) 평균회귀 변형은 주식(SPY) 전용 근거라 크립토에 그대로 적용 금지.
- **우리 슬리브와의 관계**: 기존 supertrend/슈퍼트렌드 계열이나 이동평균 크로스오버(EMA9/21, Hull, T3 등)와 유사한 "크로스오버 추세추종" 카테고리이나 지표 자체(재귀 2폴 필터)가 완전히 다름. Sharpe가 약해 **단독 채택보다 A/B로 빠르게 FAIL 처리하거나, 다른 스캘프 신호의 레짐필터로 재활용** 검토가 현실적.
