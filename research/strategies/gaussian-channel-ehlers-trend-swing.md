# [스윙] 가우시안 채널(Ehlers) 추세추종 돌파

- **출처**: https://www.tradingview.com/script/WpVY7GKW-Gaussian-Channel-DW/ (TradingView, 작성자 DonovanWall, 2020-02-17 공개·오픈소스) / 보조: https://www.fmz.com/lang/en/strategy/446555 (FMZ, "Gaussian Channel Trend Following Strategy"), https://medium.com/@FMZQuant/gaussian-channel-trend-following-strategy-d7b7af87f4c3
- **참여지표**: TradingView 좋아요 9,000 / 부스트 67 / 댓글 191 / 리포스트 122 (WebFetch 원문 확인). 오픈소스로 공개 이래 꾸준히 인용·복제되는 스테디셀러 지표(Ehlers Gaussian Filter 계열 중 가장 널리 쓰임).
- **백테스트 근거**: **원문에 정량 수치 없음(참여지표 기반)**. FMZ 페이지에 백테스트 설정(2023-03-23~2024-03-28, Binance Futures BTC_USDT, 1h 베이스/1d 표시, 초기자금 $1,000)은 확인했으나 실제 수익률·승률 등 결과값은 로그인월에 가려 원문에서 확인 못 함 → 성과 수치는 "미확인"으로 둔다.
- **타임프레임**: 4h~1d 스윙 권장(Ehlers 필터 특성상 랙이 있어 저TF일수록 신호가 늦음). 1h도 가능하나 원저자는 "higher timeframe에서 더 잘 먹힌다"는 커뮤니티 피드백이 다수.
- **시장/대상**: BTC·ETH 등 메이저 무기한(추세 계열 지표라 저유동성 알트의 노이즈에 약할 수 있음)

## 진입 규칙
- 지표: N폴(pole)의 Ehlers Gaussian Filter로 중심선(filt)을 만들고, 같은 폴 수의 가우시안 필터를 True Range에 적용한 "필터드 트루레인지(FTR)"에 배수(mult)를 곱해 상단/하단 밴드 생성. `upper = filt + mult*FTR`, `lower = filt - mult*FTR`.
- 롱: 종가가 **상단밴드(upper)를 상향 돌파** **그리고** 필터(filt) 자체가 상승 중(filt[0] > filt[1], 즉 채널 색이 초록으로 전환) → 강한 상승추세 개시로 간주해 진입.
- 숏: 종가가 **하단밴드(lower)를 하향 돌파** **그리고** filt[0] < filt[1] (채널 색 빨강 전환) → 진입.
- (커뮤니티 통용 변형: 상단밴드 상향돌파 시 롱, 하단밴드 하향돌파 시 롱 청산만 하는 "추세추종 전용"(숏 미사용) 버전도 흔함 — 크립토 양방향이므로 본 스펙은 숏 포함.)

## 청산 규칙
- 익절: 별도 목표가 없음 — **추세 추종형**이라 반대 신호(가격이 중심선 filt를 반대방향으로 재돌파하거나 채널 색이 반전) 시 청산.
- 손절: 진입 후 filt(중심선) 재이탈 시 손절(예: 롱 진입 후 종가가 filt 아래로 마감하면 손절) 또는 진입가 대비 −1.5×FTR 고정 손절 중 먼저 닿는 쪽.
- 시간 청산: 없음(추세 지속 시 계속 보유). 대신 채널 폭(FTR)이 극단적으로 좁아지면(추세 소멸 신호) 타임아웃 청산 옵션 고려 가능.

## 파라미터
- sampling_period(N)=20 (범위 10~48, poles+1 이상이어야 함)
- poles=4 (범위 2~9, 커뮤니티 기본값은 4)
- true_range_mult=1.414 (범위 1.0~2.5, DonovanWall 기본값 √2)
- reduced_lag_mode=false, fast_response_mode=false (기본, 옵션)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: Ehlers Gaussian Filter(재귀 IIR 필터, N폴 alpha/beta 계산 필요) + True Range의 동일 필터 적용본. **표준 라이브러리에 없어 직접 구현 필요**(재귀식이라 순차 계산, pandas rolling으로 불가 — for-loop 또는 numba). 난이도 중상.
- 주의: 바이낸스 REST OHLCV만으로 충분(오더북·틱 불필요). 다만 재귀 필터라 초기 워밍업 구간(수십 봉) 신뢰도 낮음 — 백테스트 시 앞부분 버퍼 필요.

## 스카우트 메모
- 강점: 순수 이동평균(SMA/EMA)보다 랙이 적고 노이즈에 덜 민감한 Ehlers 필터 계열 — TradingView에서 가장 오래·널리 검증된 추세 지표 중 하나(9k 좋아요, 6년째 인용). 볼린저/켈트너 계열(이미 FAIL·보유)과 달리 **재귀 가우시안 필터**라는 별개 수학적 기반이라 상관관계가 낮은 새 시그널이 될 수 있음.
- 의심점: **정량 백테스트 근거를 원문에서 확인하지 못함** — 순수 참여지표 스크리닝. 구현 난이도(재귀 필터)가 높아 버그 리스크(웜업 구간, 폴 수에 따른 안정성)가 있음. 횡보장에서 채널이 좁아지며 휩쏘 가능성 — regime 필터(ADX 등) 병행 검토 필요.
- 우리 단타 슬리브와의 관계: 볼린저 돌파+거래량+OI(scalp15m, 15m)와는 TF·지표 기반이 다른 **보완적 스윙 후보**. 중기 볼린저 눌림목과는 둘 다 "추세추종"이라 겹칠 소지 있으나, 눌림목은 되돌림 매수이고 이건 돌파형이라 진입 타이밍이 다름.
