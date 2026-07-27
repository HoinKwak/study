# [단타] 아시아 세션 유동성 그랩 + 주간 VWAP 편향 페이드

- **출처**: https://www.tradingview.com/script/RCHiuWi0-Asia-Session-Liquidity-Weekly-VWAP-Strategy-v2/ (TradingView, "Asia Session Liquidity + Weekly VWAP Strategy v2" by przemo28g — WebFetch로 원문 확인) / 개념 보강: https://eplanetbrokers.com/en-US/training/what-is-liquidity-grab (유동성 그랩 정의, WebFetch로 원문 확인)
- **참여지표**: 즐겨찾기(favorites) 26 / 댓글(comments) 883 (TradingView 스크립트 페이지 기준, WebFetch로 확인). 승률·PF 등 백테스트 통계는 페이지에 미게재.
- **백테스트 근거**: 없음(원문 페이지에 정량 수치 없음, 정직히 명시). 규칙 자체는 명확: 세션 레인지(아시아 00:00~08:00 UTC) 형성 → 그 레인지 경계를 꼬리로 이탈 후 종가 복귀 시 반전 진입. 유동성 그랩 개념 정의(eplanetbrokers): "sharp spike beyond a key technical level... followed by an immediate reversal", 확인 신호는 "volume spike followed by declining volume".
- **타임프레임**: 15m~1h 신호(아시아 레인지 형성은 4h 참고), 원문 스크립트는 4h 위주로 레벨을 표시하나 트리거는 세션 종료 후(런던 08:00 UTC~) 저타임프레임에서 발생.
- **시장/대상**: 원문은 포렉스 예시(pips 단위 언급)이나 개념(세션 레인지+VWAP 편향) 자체는 자산군 무관 → BTC·ETH·유동성 상위 알트 무기한(24시간 거래라 "아시아 세션"을 UTC 00:00~08:00로 재정의해 적용)

## 진입 규칙
- 지표: **주간 VWAP**(주 시작 00:00 UTC 앵커, 매주 리셋), **아시아 세션 하이/로우**(00:00~08:00 UTC 구간의 최고/최저가).
- **편향 게이트(원문 그대로)**: 가격이 주간 VWAP **위** → 롱 신호만 유효("Ignore all sell signals"). 가격이 주간 VWAP **아래** → 숏 신호만 유효("Ignore all buy signals").
- **롱(숏 유동성 그랩 실패 페이드)**: 08:00 UTC 이후(런던~뉴욕 세션), 가격이 아시아 로우를 **꼬리로 하회**했다가 **같은/다음 봉 종가가 아시아 로우 위로 복귀**(원문: "close back inside the range, leaving a wick/shadow behind") **AND** 가격이 주간 VWAP 위(편향 게이트 통과) → 그 복귀봉 종가에 롱.
- **숏**: 아시아 하이를 꼬리로 상회 후 종가 복귀 **AND** 가격이 주간 VWAP 아래 → 숏.
- 확인(옵션, eplanetbrokers 보강): 이탈 봉의 거래량이 급증했다가 복귀봉에서 거래량이 감소하는 패턴("volume spike followed by declining volume")이면 신뢰도 가중.

## 청산 규칙
- 손절: 원문 "a few pips below the wick of the candle that grabbed the liquidity" → 그랩 봉의 꼬리 끝 바로 너머(크립토 적용 시 % 또는 ATR 버퍼로 대체, 예 0.15×ATR14, [설계 보강]).
- 익절: 원문 "opposite side of the Asia range... or the Weekly VWAP" → 1차 목표 아시아 레인지 반대편 극값, 2차(공격적) 목표 주간 VWAP.
- 시간/조건 청산: 원문 명시 없음. [설계 보강] 런던+뉴욕 세션 종료(예 익일 00:00 UTC) 전 미도달 시 청산 검토(세션 특화 셋업이므로 오버나이트 지속 근거 약함).

## 파라미터
- asia_session=00:00~08:00 UTC (원문 정의)
- vwap_anchor=weekly(주 시작 00:00 UTC 리셋, 원문값)
- sweep_confirm=close_back_inside (필수, 원문)
- sl_buffer_atr=0.15 (범위 0.1~0.3, [설계값 — 원문은 pips])
- tp1=opposite_range_extreme, tp2=weekly_vwap (원문값)
- vol_confirm=optional (그랩봉 거래량 급증 후 복귀봉 거래량 감소, [설계 보강])
- entry_window=08:00~24:00 UTC (아시아 세션 이후만, 원문 취지)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 세션(00:00~08:00 UTC) 롤링 고/저, 주간 VWAP(거래량가중평균, 주 시작 앵커), ATR14, 거래량(옵션 확인용). 전부 캔들+거래량으로 계산 가능.
- 주의: 바이낸스 REST 캔들+거래량으로 완전 충족. 오더북/틱/실시간청산 불필요. "세션 레인지" 계산은 UTC 자정 기준 리샘플링이 필요(15m 데이터에서 00:00~08:00 구간 롤업) — 우리 15m 최소해상도로 구현 가능.

## 스카우트 메모
- 강점: 우리 보유 `liquidity-sweep-reversal.md`(스윙포인트 스윕 페이드, 레벨 나이 ≥20봉)·`turtle-soup-donchian-false-breakout-reversal-swing.md`(돈치안채널 페이크아웃)와 **같은 "실패한 돌파 페이드" 계열이지만, 레벨 정의가 다름**(세션 시간대 기반 아시아 하이/로우 vs 임의 스윙포인트/돈치안채널) — 세션 타이밍(UTC 00:00~08:00) 게이트와 **주간 VWAP 편향 필터가 결합된 것이 차별점**. `vwap-band-fade.md`(일중 VWAP stdev 밴드 극단 페이드)와도 메커니즘이 다름(그쪽은 통계적 극단 터치, 이건 세션 레벨 이탈+복귀).
- 의심점: (1) 원문은 포렉스 예시(핍 단위)로 크립토 이식 시 버퍼 단위를 ATR/%로 전환 필요(설계 보강). (2) 백테스트 통계 전무, TradingView 참여지표(즐겨찾기26/댓글883)도 "조회수 10만+" 기준엔 못 미침 — 스크리닝 근거로는 다소 약함. (3) 크립토는 진짜 "아시아 세션"이 유동성 저조 구간이 아닐 수 있어(24시간 글로벌 거래) 포렉스만큼 세션효과가 강하지 않을 가능성 — 채택 전 자체 백테스트로 UTC 00:00~08:00 구간이 실제로 저변동성 축적구간인지 먼저 확인 필요.
- 우리 슬리브와의 관계: 기존 단타 슬리브(scalp15m, 볼린저 이탈+거래량+OI 돌파형)와는 **반대 메커니즘**(그쪽은 돌파추종, 이건 돌파실패 페이드) — 국면분리 보완 후보. 15m/1h로 우리 백테스트 인프라에서 바로 검증 가능(미션 우선순위 부합).
