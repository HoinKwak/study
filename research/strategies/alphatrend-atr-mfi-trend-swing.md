# [스윙] AlphaTrend (ATR+MFI 트레일링) 트렌드추종

- **출처**: https://www.tradingview.com/script/o50NYLAZ-AlphaTrend/ (TradingView, KivancOzbilgic, "AlphaTrend" — WebFetch로 원문 확인)
- **참여지표**: TradingView 스크립트 페이지 **좋아요 28,000 / 부스트 367 / 뷰 684 / 댓글 208**(WebFetch로 원문 확인). 28K 좋아요는 트레이딩뷰 전체 스크립트 중에서도 최상위권으로, 스크리닝 규칙의 "참여지표가 눈에 띄게 높은 것" 기준을 명확히 충족.
- **백테스트 근거**: **없음(지표 페이지 기반, 정량 성과 수치 원문에 없음)**. 페이지에는 계산 로직·신호 규칙만 있고 승률·PF·수익률 등은 게시돼 있지 않음 — 지어내지 않고 "없음"으로 표기, 채택 전 자체 백테스트 필수.
- **타임프레임**: 4h 신호(스윙 원 사용례 다수) / 1d 확인. 15m~1h로 다운스케일한 스캘프 변형도 가능하나 본 스펙은 스윙 우선.
- **시장/대상**: BTC·ETH·시총상위 알트 무기한 (원 지표는 크립토·주식 범용이나 크립토 트레이딩 커뮤니티에서 특히 널리 쓰임)

## 진입 규칙
- **AlphaTrend 계산**(WebFetch로 확인된 규칙 텍스트 기반 + 공개적으로 널리 알려진 Pine 변환식으로 재구성 — 아래 수식은 [원문 텍스트+공개 지식 재구성, 상수는 원문에서 확인된 period=14/coefficient=1만 확정]):
  - `ATR = ATR(period=14)`
  - `upT = low - ATR × coefficient(1.0)`
  - `downT = high + ATR × coefficient(1.0)`
  - 모멘텀 필터: `MFI(14)`(기본) 또는 `RSI(14)`(옵션)
  - `AlphaTrend[t] = MFI≥50 ? max(upT, AlphaTrend[t-1]) : min(downT, AlphaTrend[t-1])` (모멘텀이 강세면 상승 트레일링, 약세면 하락 트레일링 — ATR 트레일링 스톱과 유사하되 MFI로 방향을 결정)
- **신호(원문 그대로 인용)**: "BUY / LONG when Alpha Trend line crosses above its 2 bars offsetted line and there would be a green filling between them. SELL / SHORT when Alpha Trend line crosses below its 2 bars offsetted line and filling would be red then."
- 롱: `AlphaTrend[t] > AlphaTrend[t-2]`로 상향 교차(직전엔 `AlphaTrend[t-1] <= AlphaTrend[t-3]` 등 하락/횡보 상태였다가 전환) → 교차 확정봉 종가 진입.
- 숏: `AlphaTrend[t] < AlphaTrend[t-2]`로 하향 교차 → 진입.

## 청산 규칙
- 익절: 없음(트레일링 스톱형 지표이므로 반대 신호 발생 시까지 홀드).
- 손절: 진입 시점 AlphaTrend 라인 값(그 자체가 ATR 기반 동적 손절선 역할) 이탈 시 청산 — 즉 롱 보유 중 종가가 AlphaTrend 아래로 이탈하면 손절.
- 시간/조건 청산: 반대 방향 크로스(2봉 오프셋 재교차) 발생 시 청산 후 반대 포지션 재진입 가능(항상 시장에 포지션을 유지하는 스톱-앤-리버스형 원 설계 — 본 봇은 트레일링 손절 후 재신호 대기로 보수화 권장).

## 파라미터
- period=14 (ATR·MFI 공통 기간, 원문 확인, 범위 10~20)
- coefficient=1.0 (ATR 배수, 원문 확인, 범위 0.5~2.0)
- signal_offset=2봉 (원문 확인, 고정)
- momentum_source=MFI (옵션: RSI)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: ATR(14), MFI(14, 거래량 필요) 또는 RSI(14), 고가·저가·종가.
- 주의: **바이낸스 REST 캔들+거래량만으로 완전 구현 가능**. 다만 정확한 upT/downT 갱신 로직(재귀식)은 원문 페이지에서 텍스트로 직접 추출되지 않아 **공개적으로 알려진 Pine 변환 코드 기준으로 재구성**했음을 명시 — 구현 후 TradingView 차트 값과 대조 검증 권장(재귀식 특성상 초기화·오프바이원 오류 위험 있음, 기존 `andean-oscillator-atr-band-swing.md`에서 지적된 동일 유형의 리스크).

## 스카우트 메모
- 강점: **좋아요 28,000**은 이번 라운드 발굴 대상 중 압도적으로 높은 참여지표이며, 기존 188개 스펙 전체를 통틀어도 최상위권 인지도. 규칙 자체는 명확(2봉 오프셋 크로스)해 코딩 가능성 요건도 충족.
- 의심점: **메커니즘이 기존 보유 ATR 트레일링 스톱 계열(`chandelier-exit-atr-trend-swing.md`, `halftrend-atr-channel-swing.md`, `ut-bot-alerts-atr-trailing-scalp.md`, `pmax-most-supertrend-ma-trailing-scalp.md`)과 구조적으로 유사**(ATR 기반 동적 트레일링 라인 + 크로스 신호). 차별점은 MFI/RSI로 트레일링 방향을 결정하는 모멘텀 필터가 내장된 점. 백테스터가 이미 4종의 유사 계열에서 결과를 확인했다면 5번째 변형의 한계효용은 낮을 수 있음 — **참여지표가 매우 높다는 점 때문에 채택했으나, 기존 ATR 트레일링 계열 백테스트 결과를 먼저 참고해 우선순위 판단 권장**.
- 우리 단타 슬리브와의 관계: 대체보다는 ATR 트레일링 계열 내 "MFI 필터 추가" 변형으로 자리매김. 기존 계열이 전부 FAIL이었다면 이 변형도 낮은 우선순위로 볼 근거가 됨.
