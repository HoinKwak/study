# [스윙] 터틀 수프(Turtle Soup) — 돈치안 페이크아웃 반전

- **출처**: https://medium.com/@redsword_23261/turtle-soup-strategy-enhanced-a-high-win-rate-reversal-trading-system-with-multiple-price-action-f6dd54030002 (Medium, "Turtle Soup Strategy Enhanced", Sword Red — 코드/규칙 포함, WebFetch로 원문 확인) / 원조 개념: Linda Raschke, *Street Smarts: High Probability Short-Term Trading Strategies* / 보강 개념 설명: https://blog.coinlocally.com/turtle-soup-strategy-when-the-market-lies/, https://alchemymarkets.com/education/strategies/turtle-soup-strategy/
- **참여지표**: TradingView에 동일 개념 스크립트가 다수 채널에서 반복 공개됨(CandelaCharts "Turtle Soup Model", TradingFinder "Turtle Soup ICT Strategy", Flux Charts "ICT Turtle Soup" 등) — 개별 좋아요·조회수는 WebFetch로 확인 못 했으나 ICT/가격행동 커뮤니티에서 반복 재생산되는 정도로 인기 추정.
- **백테스트 근거**: **없음(원문에 수치 미기재, 정직히 명시)**. Medium 원문은 Pine 코드와 규칙 설명만 제공하고, 코드 헤더에 백테스트 대상 자산·기간(SOL/USDT, 바이낸스 선물, 2024-04-27~2025-04-25)만 명시돼 있을 뿐 승률·PF·수익률 등 성과 수치는 없음. **채택 전 자체 백테스트 필수.**
- **타임프레임**: 1h (원문 코드 백테스트 프레임). 다른 TF(4h)로 확장 시 재검증 필요.
- **시장/대상**: SOL/USDT 바이낸스 선물(원문 백테스트 대상). BTC·ETH 등 확장은 미검증.

## 진입 규칙
- 롱(TBS Long, "Body Soup"): 캔들의 **몸통(시가·종가 둘 다)**이 최근 N=20봉 돈치안 채널 **저점 아래**로 완전히 이탈했다가, 후속 캔들이 **종가 기준으로 채널 내부로 복귀**할 때 → 그 복귀 봉 종가/다음 봉 시가에 롱 진입(가짜 하방 돌파 페이드).
- 롱 변형(TWS Long, "Wick Soup"): 캔들 **꼬리만** 돈치안 저점 아래로 이탈, 종가는 이미 채널 내부에서 마감 → 즉시 진입(더 빠른 트리거, 신뢰도는 body soup보다 낮음).
- 숏: 대칭 — 몸통/꼬리가 돈치안 채널 **고점 위**로 이탈 후 종가 기준 채널 내부로 복귀 시 숏 진입.
- 옵션 필터(원문 언급, 신뢰도 강화용): 강세/약세 오더블록 또는 페어밸류갭(FVG) 근접 시에만 진입(구조 확인 강화).

## 청산 규칙
- 익절: 손절 거리의 **1.5배(R:R 1.5, 원문 기본값)**. 코드는 자동으로 이 R:R 기반 목표가를 계산.
- 손절: 롱은 신호 캔들의 **저가 바로 아래**, 숏은 신호 캔들의 **고가 바로 위**.
- 시간/조건 청산: 원문에 별도 시간청산 규칙 없음. 반전 실패(가격이 다시 채널 밖으로 재이탈) 시 조기 손절 처리로 갈음.

## 파라미터
- donchian_period=20 (범위 10~50, 원문 최소값 5까지 조정 가능하다고 명시)
- rr=1.5 (범위 1.0~2.5)
- soup_type=body|wick (기본 body — wick은 신호 빈도↑ 신뢰도↓)
- ob_fvg_filter=off (옵션, 켜면 신호 빈도↓ 신뢰도↑ 기대, 미검증)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: 돈치안 채널(최근 N봉 최고/최저) — 캔들 OHLC만으로 완전 계산 가능. 오더블록/FVG 필터는 옵션(캔들 패턴 기반으로 계산 가능, 실시간 오더북 불필요).
- 주의: 바이낸스 REST 캔들만으로 100% 구현 가능. "채널 내부 복귀" 판정은 종가 기준으로 명확히 규칙화되어 룩어헤드 없이 구현 쉬움.

## 스카우트 메모
- 강점: 우리 기존 `turtle-trading-dual-donchian-swing`(추세추종 브레이크아웃)과 **정반대 방향(페이드/반전)** 로직이라 개념적으로 뚜렷이 구분됨 — 동일 지표(돈치안)를 반대 철학으로 쓰는 좋은 비교쌍. 규칙이 매우 단순(채널 이탈 후 복귀)해 구현·백테스트가 빠름.
- 의심점: 원문에 정량 백테스트 근거가 전혀 없어 순수 컨셉 채택 — 크립토 특유의 변동성에서 휩쏘(false reversal)가 잦을 수 있음(원문 2차 자료들도 "크립토 급변동장에서는 필터 강화 필요"라고 공통 언급). ICT류 파생 스크립트가 난립하는 걸 보면 대중적 인지도는 있으나 검증된 엣지인지는 불명확.
- 우리 단타 슬리브와의 관계: 우리 기존 `liquidity-sweep-reversal`, `bos-choch-market-structure-swing`과 개념적으로 인접(유동성 스윕 후 반전)하나, 이 전략은 **돈치안 채널이라는 명확한 정량 기준**을 쓰는 점이 차별점. 기존 슬리브와 중복보다는 **동일 계열 내 파라미터 변형**에 가까움 — 백테스트로 우열 비교 권장.
