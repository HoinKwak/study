# [스윙] ICT 오더블록(Order Block) + BOS 컨플루언스 되돌림 추세지속

- **출처**: https://alphanex.io/blog/order-block-trading-strategy (Alphanex, "Order Block Trading Strategy" — WebFetch로 원문 확인) / 보강: https://innercircletrader.net/tutorials/ict-order-block/ , https://www.fluxcharts.com/articles/order-blocks-ob-explained
- **참여지표**: - (교육 블로그, SNS 참여지표 미집계). "오더블록"은 ICT/SMC 트레이딩 커뮤니티에서 유튜브·트레이딩뷰에 수천 개 파생 콘텐츠가 존재하는 핵심 개념(개별 콘텐츠 재확인은 시간상 생략, 개념 자체의 커뮤니티 반복도로 대체 판단).
- **백테스트 근거**: 없음(정성적, 원문 명시: "backtest 50-100 trades to establish statistical validity"라고만 권고, 자체 수치 없음). 원문 진입/청산 규칙은 구체적으로 서술되어 코딩 가능.
- **타임프레임**: 1h 신호(오더블록 식별) / 4h 확인(BOS 방향 필터). 4h~1d로 확장 시 재검증 필요.
- **시장/대상**: 원문은 자산군 무관("stocks, crypto, forex, futures") → BTC·ETH·시총상위 알트 무기한

## 진입 규칙
- **불리시 오더블록 정의(원문)**: "the last bearish (red) candle before a strong bullish move that breaks the previous high" — 상승 임펄스 직전 마지막 음봉.
- **베어리시 오더블록 정의(원문)**: "the last bullish (green) candle before a strong bearish move that breaks the previous low" — 하락 임펄스 직전 마지막 양봉.
- **4대 검증 조건(원문 그대로)**:
  1. **BOS(구조돌파)**: 오더블록에서 이탈한 움직임이 명확한 스윙 고점(불리시)/저점(베어리시)을 돌파해야 함.
  2. **임펄시브 이탈**: 큰 몸통 캔들로 모멘텀 있게 이탈(완만한 드리프트 아님).
  3. **불균형(FVG)**: 이상적으로 이탈 구간에 캔들 꼬리 사이 갭(페어밸류갭)이 남아야 함.
  4. **미충족(unmitigated)**: 가격이 아직 해당 존으로 되돌아오지 않은 상태여야 유효.
- **롱**: 불리시 오더블록(4조건 충족) 형성 후, 가격이 되돌림으로 그 존(캔들 몸통 범위)에 재진입 → **"확인 진입"**(원문 권장: 하위TF 확인 신호 대기 후 진입, 최선의 승률/RR 균형이라고 원문이 명시) — 존 안에서 반전 캔들(하단꼬리+양봉 마감) 확인 시 그 봉 종가에 롱.
- **숏**: 베어리시 오더블록 재진입 시 존 안에서 반전 캔들(상단꼬리+음봉 마감) 확인 후 숏.
- 무효화: 가격이 오더블록 존을 완전히 종가로 관통(존 반대편으로 이탈) 시 셋업 폐기.

## 청산 규칙
- 손절: 원문 "a few pips beyond the far edge of the order block" → 오더블록 존의 먼 쪽 끝(롱은 존 하단, 숏은 존 상단) 바로 너머 + ATR 버퍼(예 0.2×ATR14, [설계 보강]).
- 익절: 원문 "nearest opposing liquidity" 및 "subsequent major levels", 목표 **1:3~1:5 R:R**(원문 명시).
- 시간/조건 청산: 원문 없음. [설계 보강] max_hold_bars(예 1h 기준 48봉=2일) 내 1R 미도달 시 재검토, BOS 반대 방향 재발생 시 조기 청산.

## 파라미터
- ob_impulse_body_min=1.2×ATR (임펄시브 이탈 판정, [설계값], 원문은 정성적 "large-bodied")
- bos_swing_lookback=10~20봉 (스윙 고/저 탐지 윈도, [설계값])
- fvg_required=optional (원문은 "ideally"라 필수 아님, on/off 스윕 권장)
- confirm_entry=lower_tf_reversal_candle (원문 권장 방식)
- rr_target=3.0 (범위 3.0~5.0, 원문값)
- sl_buffer_atr=0.2 (범위 0.1~0.4, [설계값])
- max_hold_bars=48 (1h 기준, [설계값])

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 스윙 고/저 탐지(롤링 극값), 캔들 몸통 크기(ATR 대비), 3봉 갭 비교(FVG, 옵션), 반전 캔들 패턴(꼬리/몸통 비율). 전부 OHLCV 캔들만으로 계산 가능.
- 주의: 바이낸스 REST 캔들로 완전 충족. 오더북/틱 불필요. "미충족(unmitigated)" 판정(존이 아직 완전히 관통되지 않았는지)은 매 봉 갱신 로직 필요 — 기존 보유 `ict-fair-value-gap-pullback-scalp.md`의 FVG 미충족 갱신 로직과 유사한 패턴이라 재사용 가능.

## 스카우트 메모
- 강점: 우리 보유 `ict-fair-value-gap-pullback-scalp.md`(갭 자체가 지지/저항)와 `bos-choch-market-structure-swing.md`(구조전환 자체가 신호)는 각각 **다른 메커니즘**인 반면, 이건 **"임펄스 직전 마지막 반대캔들(오더블록)"을 지지/저항 존으로 쓰고 BOS+FVG로 검증**하는 세 번째 축 — SMC/ICT 3대 개념(오더블록·FVG·BOS) 중 오더블록만 유일하게 우리 라이브러리에 없었음. `liquidity-sweep-reversal.md`·`turtle-soup-donchian-false-breakout-reversal-swing.md`는 **실패한 돌파를 페이드**(역추세)하는 반면, 이건 **성공한 임펄스의 재테스트를 추세지속으로 매수**(순추세) — 메커니즘 정반대.
- 의심점: (1) 오더블록 식별 규칙에 "몇 봉 전까지를 오더블록 후보로 볼지" 등 세부는 여전히 재량적 — 임펄스 임계값(ob_impulse_body_min)은 스카우트 설계값이라 백테스트로 민감도 확인 필요. (2) 정량 백테스트 전무. (3) "확인 진입"(하위TF 대기) 로직은 우리 15m/1h 최소해상도로는 하위TF 확인을 생략하고 신호봉 반전 캔들로 대체해야 함(원문 취지와 약간 다름, 명시).
- 우리 슬리브와의 관계: 순추세지속형이라 현재 SwingStrategy(RSI 역추세+슈퍼트렌드 피라미딩)와 메커니즘 상이, 보완 후보. 1h/4h로 우리 백테스트 인프라(15m 최소해상도)에서 직접 검증 가능.
