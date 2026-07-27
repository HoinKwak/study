# [스윙] 볼린저밴드 워크(Band Walk) 추세지속 추종

- **출처**: https://www.bollingerbands.com/bollinger-band-rules (John Bollinger 공식 사이트, "The Rules" — WebFetch로 원문 확인) / 보강: https://www.colibritrader.com/bollinger-band-strategies/ , https://arrowalgo.com/bollinger-bands-complete-guide-for-algorithmic-trading/
- **참여지표**: - (개발자 공식 규칙 문서, SNS 참여지표 미집계. 다만 "밴드워크"는 볼린저밴드 커뮤니티에서 가장 널리 인용되는 규칙 중 하나 — bollingerbands.com Rule 7/8이 원저자 본인 공식 언급)
- **백테스트 근거**: 없음(정성적, 원저자 규칙서). 원문 인용: Rule 7 "In trending markets price can, and does, walk up the upper Bollinger Band and down the lower Bollinger Band." / Rule 8 "Closes outside the Bollinger Bands are initially continuation signals, not reversal signals." / Rule 6 "A tag of the upper Bollinger Band is NOT in-and-of-itself a sell signal. A tag of the lower Bollinger Band is NOT in-and-of-itself a buy signal." → 정량 수치 없음, **원저자 규칙 자체를 신호화**한 것.
- **타임프레임**: 4h 신호 / 1d 확인 권장(추세지속 판별에는 저잡음 TF 필요). 1h로 축소 가능하나 밴드워크 판정 노이즈 증가.
- **시장/대상**: BTC·ETH·시총상위 알트 무기한

## 진입 규칙
- 지표: 볼린저밴드(20, 2.0), ADX(14), 20SMA(중심선) 기울기.
- **밴드워크 판정**: 최근 walk_bars(예 3봉) 중 walk_min_touch(예 2봉 이상)의 **종가가 상단밴드 위(또는 상단밴드에 근접, 종가≥상단밴드×0.995)**로 마감 **AND** ADX(14) ≥ 25(추세 확인) **AND** 20SMA가 명확히 상향(직전 대비 slope>0) → **상승 밴드워크 확정**(하락은 대칭).
- 롱: 상승 밴드워크 확정 후 **첫 눌림목**(가격이 20SMA까지 되돌리되 종가가 20SMA 아래로 마감하지 않음) 발생 시 그 봉 종가에 진입("Rule 6/7/8"에 따라 밴드 접촉=매도신호 아님, 되돌림을 추세추종 눌림매수 기회로 해석).
- 숏: 하락 밴드워크 확정 후 20SMA로 반등하되 종가가 20SMA 위로 마감하지 않는 봉에 진입.
- 무효화: 밴드워크 확정 후 종가가 20SMA를 반대로 관통하며 마감 → 추세 종료로 간주, 셋업 폐기.

## 청산 규칙
- 익절: 없음(추세추종형) — 트레일링 스탑으로 대체. 반대편 밴드(예: 롱 포지션의 손절 트레일)까지 여유를 두고 20SMA 상향 돌파 유지되는 한 보유.
- 손절: 초기 SL은 진입 눌림목의 저점(롱)/고점(숏) 바로 아래/위. 이후 **20SMA 종가 이탈 시 전량 청산**(트레일 방식) — "가격이 중심선 반대편으로 종가 마감하면 추세가 꺾인 것"이라는 원저자 취지 반영.
- 시간/조건 청산: ADX가 20 아래로 하락(추세 소멸) 시 조기 청산 검토.

## 파라미터
- bb_period=20, bb_std=2.0 (원저자 표준값)
- adx_period=14, adx_min=25 (범위 20~30)
- walk_bars=3, walk_min_touch=2 (범위 2~5봉 / 2~4회)
- band_tag_tol=0.995 (상단밴드 대비 종가 근접 허용치, 범위 0.99~1.0)
- ma_slope_lookback=3~5봉 (기울기 계산용)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 볼린저밴드(20,2.0), ADX(14), 20SMA 및 그 기울기. 전부 OHLC 캔들만으로 계산 가능.
- 주의: 바이낸스 REST 캔들로 완전 충족. 오더북/틱 불필요. "밴드워크" 판정 로직(N봉 중 M봉 이상 근접 종가)을 명확히 코딩해야 하며, 레인지장에서 오탐(밴드 근접이 잦은데 ADX 필터가 낮아도 통과) 방지를 위해 ADX 임계값이 핵심 게이트.

## 스카우트 메모
- 강점: 우리 보유 `bollinger-band-fade-range.md`(레인지 페이드), `bollinger-squeeze-breakout-daily.md`(스퀴즈 돌파), `bollinger-rsi-divergence-reversal.md`(다이버전스 역추세)와 **메커니즘이 정반대**(추세지속 순추세)라 상호 보완 후보 — 국면(레인지 vs 트렌드)에 따라 스위칭 가능한 짝을 이룸.
- 의심점: (1) 원저자 규칙 자체가 정성적 서술이라 "밴드워크 확정" 임계값(walk_bars/touch 등)은 전부 재현을 위한 설계 판단이며 원문에 수치 없음. (2) ADX 필터 없이는 레인지장 잦은 밴드 접촉과 구분 어려움 — 백테스트로 ADX 임계 민감도 확인 필수. (3) 4h 이상 권장이라 표본 수(트레이드 빈도)가 적을 수 있음.
- 우리 슬리브와의 관계: 현재 스윙 슬리브(SwingStrategy)는 RSI 역추세 진입 후 슈퍼트렌드 피라미딩 구조 — 이건 **처음부터 순추세(밴드워크 확정 후 진입)** 라 스윙 슬리브와 메커니즘이 다름. 대체보다는 국면분리형 보완 후보.
