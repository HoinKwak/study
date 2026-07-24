# [단타] "Stiff Surge" 다중지표 합류(JMA 추세+TDFI+VQ+Stiffness) ATR 밴드 추세추종

- **출처**: YouTube "I Backtested This FREE Crypto Trading Strategy! [What I Found]"
  (채널: Crypto Banter, https://www.youtube.com/watch?v=_tMzs9cD-4g , 업로드 20250601)
  — `python -m scripts.yt_transcript _tMzs9cD-4g --meta` 로 자막 확보 후 원문 규칙 추출.
  구성 지표 원안: JMA(Jurik Moving Average, Mark Jurik 고안), TDFI(Trend Direction Force Index,
  Mladen 고안, MQ4→Pine 이식 다수), Stiffness Indicator(Markos Katsanos, Stocks & Commodities V.36:12,
  2018년 11월 — https://www.prorealcode.com/prorealtime-indicators/stiffness-indicator/ 에서 공식 확인),
  VQ Zero Line(Volatility Quality, mladen 고안 MT4 지표 — https://www.mql5.com/en/code/22937 참고).
  지표들은 davidtech(davidick.com)이 TradingView에 무료 배포.
- **참여지표**: 조회수 14,736 (Crypto Banter, 크립토 전문 대형 채널 — 해당 영상 자체 조회수는 채널 평균 대비 낮은 편이라 참여지표만으로는 강한 신호 아님. 백테스트 수치가 있어 채택.)
- **백테스트 근거**: 영상 내 TradingView 백테스트(자막 원문 확인, 채널 자체 결과 — **제3자 독립 검증 아님**, 표본기간·과최적화 검증 방법 불명, 초기 자본금·수수료 가정 불명):
  - ARBUSDT 45m, Bybit 데이터, **10x 레버리지**: 순이익 **+2,191%**(동일기간 바이앤홀드 -69%), MDD **24%**, **729건** 체결.
  - ETHUSDT 90m: 순이익 **+973%**, **승률 64%**, **248건** 체결.
  - BTCUSDT 45m, AVAX 90m, ATOM 45m, NEAR(45m·1h) 등에서도 "양호한 자산곡선"이라 언급(자막에 정확한 수치 없이 정성적 서술만 있어 이 부분은 **미기재로 처리**, 정성적 언급만 있었다는 점 명시).
  - **⚠️ 표본수·기간·레버리지 반영 최대낙폭이라 실사용 레버리지(우리 봇 10x~30x)에 따라 체감 MDD 달라짐. 크리에이터 자체 채널 백테스트라 편향 가능성 있음 — 우리 프레임워크 재검증 필수.**
- **타임프레임**: 45m~90m 신호(원문 실증 구간). 우리 봇은 15m/1h 네이티브라 **15m 또는 1h로 재검증** 필요(원문 정확한 45m/90m 미보유).
- **시장/대상**: BTC·ETH·AVAX·ATOM·NEAR 등 시총상위 알트 무기한 (Bybit 데이터 기준이나 바이낸스로 대체 가능)

## 진입 규칙
- **① JMA(Jurik Moving Average, length=25)**: 추세 방향 필터. 가격이 JMA 위 + JMA선 색이 상승(green)이면 롱 후보, 아래+하락(red)이면 숏 후보.
- **② TDFI(Trend Direction Force Index)**: 가격 모멘텀 힘의 방향 확인. TDFI가 `+0.05`(또는 기본 임계값) 위로 올라가면(green) 롱 확인, `-0.05` 아래면(red) 숏 확인.
  - 계산(공개 재구현 로직, **원 저작자의 정확한 공식이 완전히 공개되지 않아 다음은 통상적 재구현 근사치**임을 명시):
    `mma = EMA(close, n1)`, `smma = EMA(mma, n2)`, `impetmma = mma - mma[1]`, `impetsmma = smma - smma[1]`,
    `divma = |mma - smma|`, `averimpet = (impetmma + impetsmma)/2`, `tdf_raw = averimpet × divma`,
    `TDFI = tdf_raw / max(|tdf_raw|, n3봉 롤링 최대값)` (정규화, -1~1). `n1=n2=13, n3=147` 통상값(원문 미확정, 튜닝 필요).
- **③ VQ Zero Line(Volatility Quality)**: 변동성 방향 확인. 제로라인 위(green)면 롱 확인, 아래(red)면 숏 확인.
  - 계산: `vqi_raw = ((close_t - close_{t-1})/TR_t + (close_t - open_t)/range_t) × 0.5` (TR=True Range, range=고저폭),
    `vqi = |vqi_raw| × (close_t - close_{t-1} + close_t - open_t) × 0.5`, WMA(15)로 스무딩 후 부호로 상승/하락 판정.
- **④ Stiffness Indicator(Katsanos)**: 추세 건강도(변동성) 확인. `Sma100=SMA(close,100)`, `상단밴드=Sma100+0.2×STD(close,100)`,
  `StiffL=100×(최근 60봉 중 close>상단밴드였던 봉 수)/60`. **StiffL이 임계값(예 50) 위**여야 상승추세 건강(하락은 하단밴드로 대칭).
- **롱**: ①②③④ **4개 지표가 모두 동시에 롱 방향**을 가리킬 때 진입.
- **숏**: ①②③④ 4개 지표가 모두 동시에 숏 방향을 가리킬 때 진입.

## 청산 규칙
- 손절: ATR 밴드 `stop_atr_mult=3×ATR(period, 신호 TF)` — 원문은 "ATR bands set to 3" (진입가 대비 반대방향 3ATR).
- 익절: 손익비 `rr_target=1.0~1.5R`(원문 "risk to reward of 1 to 1.5"). 손절폭(3ATR) 대비 1~1.5배 이익폭에서 익절.
- 시간 청산: 명시적 시간청산 없음(4지표 컨플루언스가 깨지면, 즉 ①~④ 중 다수가 반대로 돌아서면 조기 청산 권장 — [추정], 원문에 명시적 언급 없음).

## 파라미터
- jma_length=25
- tdfi_n1=13, tdfi_n2=13, tdfi_n3=147 (원문 미확정, 튜닝 필요), tdfi_threshold=0.05
- vq_smooth=15 (WMA)
- stiffness_ma_period=100, stiffness_lookback=60, stiffness_vol_mult=0.2, stiffness_threshold=50
- stop_atr_mult=3.0 (범위 2.0~4.0)
- rr_target=1.0~1.5 (범위 1.0~2.0)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: JMA(공개 근사 구현 다수 존재), TDFI(공식 근사치, **정확한 원저작자 공식 미공개 → 재현 시 원본과 오차 가능성**), VQ Zero Line(공식 확인됨), Stiffness(공식 확인됨), ATR. 전부 OHLCV(+거래량 불필요, 순수 가격 기반)로 계산 가능.
- 주의: **TDFI와 JMA는 정확한 원 공식이 완전히 공개돼 있지 않아 재구현 시 원본 지표와 오차가 있을 수 있음** — 4개 지표 중 코딩 난이도·재현 리스크가 가장 높은 두 요소. 나머지(VQ, Stiffness, ATR)는 공식이 명확해 재현 리스크 낮음. 오더북·틱데이터·실시간 청산 불필요.

## 스카우트 메모
- 강점: 우리가 보유한 어떤 스펙과도 겹치지 않는 **4중 지표 컨플루언스** 설계(추세+모멘텀힘+변동성방향+추세건강도)라 독창성 높음. 백테스트 수치(ARB +2,191%, ETH 승률64%/248건)가 인상적이나 채널 자체 결과.
- 의심점: (1) 크리에이터 자체 채널의 자체 백테스트라 편향 가능성, (2) JMA·TDFI 정확한 공식 미공개로 재현 오차 위험, (3) 4개 지표 모두 정렬 요구라 실전 신호 빈도가 낮아 트레이드당 R이 크더라도 우리 15m/1h 데이터에서 표본이 충분할지 불확실, (4) 10x 레버리지 가정 백테스트라 우리 리스크 설정(메이저 30x/알트 10x)과 그대로 비교 불가.
- 우리 단타 슬리브와의 관계: 기존 scalp15m(볼린저 돌파+거래량+OI)과 완전히 다른 신호 체계(변동성 방향성 오실레이터 컨플루언스)라 **중복 없음, 보완 후보**. 다만 구현 리스크(TDFI/JMA 근사) 때문에 백테스트 우선순위는 중간 — 먼저 프로토타입으로 신호 상관성·빈도부터 확인 권장.
