# [스윙] BTC 요일 계절성(주말 눌림+월요일 효과) 캘린더 스윙

- **출처**: QuantifiedStrategies, "What is the best day of the week to buy Bitcoin?" https://www.quantifiedstrategies.com/best-day-of-the-week-to-buy-bitcoin/ (원 페이지는 봇 차단으로 WebFetch 불가) — **동일 저자의 Substack 미러로 WebFetch 원문 확인**: https://quantifiedstrategies.substack.com/p/best-day-of-the-week-to-buy-bitcoin / QuantifiedStrategies, "Weekend Effect In Bitcoin (Crypto)" https://www.quantifiedstrategies.com/weekend-effect-in-bitcoin/ (원문 WebFetch 차단, WebSearch 스니펫으로만 확인 — 아래 표기)
- **참여지표**: - (콘텐츠 사이트, SNS 참여지표 미집계). QuantifiedStrategies는 정량 백테스트를 표방하는 사이트이나 이번엔 봇차단으로 대부분 확인 불가.
- **백테스트 근거**: **부분 확인.**
  - **Substack 미러(WebFetch 원문 확인)**: "Mondays have historically produced the strongest average gains (around +0.5% per day)", "Wednesday, Friday도 상대적으로 양호", "일요일·목요일이 가장 부진". "Late Sunday or early Monday entries have historically been favorable." **단, 정확한 표본기간·거래횟수·승률·통계적 유의성(p-value)은 이 글에 제시되지 않음** — 방향성(정성) 수준으로만 확인됨.
  - **원 사이트 주말효과 페이지(WebFetch 차단, WebSearch 스니펫만)**: "103 trades, average gain 2.6%, win rate 60%, max drawdown 19%", "토요일-일요일 전략 평균 2.2%/트레이드", "BTC가 ETH보다 이 효과 더 강함" — **⚠️ 원문 페이지를 직접 대조하지 못해 정량 수치는 검색엔진 인덱싱 스니펫 수준의 신뢰도(원문과 100% 일치한다는 보장 없음)로만 표기. "정량 수치 원문 미확인(스니펫 수준)"으로 분류.**
- **타임프레임**: 일봉(1d) 캘린더 신호, 진입은 UTC 요일 경계 기준(원문은 EST 기준일 가능성 있어 정확한 타임존은 재검증 필요).
- **시장/대상**: BTC 무기한 (원문은 BTC 중심, ETH는 효과 약하다고 언급 — ETH/SOL/XRP/BNB 확장은 검증되지 않음).

## 진입 규칙
- **캘린더 신호(1차 필터)**: 일요일 종가(UTC 24:00 부근) 또는 월요일 시가 근방에서만 신규 롱 진입 후보로 검토(요일 계절성 상 월요일 평균수익률 최고).
- **주말눌림 확인(2차 필터, 다중조건화)**: 금요일 종가 대비 일요일 저가까지의 낙폭(weekend_dip)이 **-1.5% 이상**(하락 조정 발생)이고, 일요일 종가가 그날 저가~고가 레인지의 **상위 50% 이내**(하락 후 반등 마감, 바닥 지지 시사)일 때만 롱 진입.
- 롱: 위 두 조건(요일 타이밍 + 주말눌림 후 반등 마감) 동시 충족 시 일요일 종가/월요일 시가에 진입.
- 숏: 대칭 룰 없음(원문은 매수 타이밍 최적화 연구이며 숏 근거 없음).

## 청산 규칙
- 익절: 월요일 종가에 기본 청산(단일 세션 캘린더 효과 포착). 확장 시 화요일 종가까지 홀드 옵션(수요일도 양호 언급 근거).
- 손절: 진입가 대비 -2×ATR(14, 일봉) 또는 weekend_dip 저점 하회 시 조기 손절.
- 시간/조건 청산: 늦어도 화요일 종가까지 무조건 청산(캘린더 효과 소멸 가정).

## 파라미터
- entry_day=Sunday close~Monday open (범위: UTC 기준 재검증 필요, EST 기준일 가능성)
- weekend_dip_min=-1.5% (범위 -1.0~-3.0%, 금요일종가 대비 일요일저가)
- sunday_close_position=상위50% (레인지 내 종가 위치, 범위 40~60%)
- exit_day=Monday close (기본) ~ Tuesday close (확장, 범위)
- stop_atr_mult=2.0 (범위 1.5~3.0)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 요일/시각 판정(캔들 타임스탬프), 금~일 낙폭 계산, 일봉 레인지 내 종가 위치, ATR14. 전부 캔들 OHLC만으로 충족.
- 주의: **바이낸스 REST 일봉 캔들로 완전 충족.** 정확한 타임존(UTC vs EST) 처리가 핵심 — 원문 근거들이 미국 시장 기준일 가능성이 있어, 백테스트 시 UTC/EST 두 버전을 모두 시도해 비교 권장.

## 스카우트 메모
- **강점**: 저빈도(주 1회) 캘린더 기반이라 수수료 영향 극히 작음 — 스윙 슬리브에 적합. 순수 계절성뿐 아니라 "주말눌림 후 반등 마감"이라는 가격action 확인조건을 추가해 오늘 지적된 "단순 크로스/돌파 재탕" 함정을 피함.
- **의심점**: 핵심 정량 근거(103트레이드/승률60%/MDD19%)가 **원문 직접 대조 실패**로 신뢰도가 이 목록에서 가장 낮은 축(스니펫 기반). 24/7 크립토 시장에서 "요일 효과"가 실재하는지 자체에 대한 회의론도 검색 결과에 존재(타임존 효과와 혼동 가능성 경고). **백테스트 우선순위는 낮게 권장** — 우리 프레임워크로 먼저 순수 계절성(가격action 필터 없이) 유의성부터 확인 후 필터 추가가 안전.
- **우리 슬리브와의 관계**: 완전 신규 메커니즘(캘린더/요일 효과). 기존 `killzone-session-timing.md`(일중 세션)와는 시간축이 다름(일중 vs 주간 요일) — 상호 배타적이지 않고 결합 가능(예: 월요일 캘린더 신호를 킬존 시간대에 정밀 진입).
