# [단타] Chande Kroll Stop 추세반전 스탑앤리버스 (ATR 이중밴드)

- **출처**: https://www.tradingview.com/support/solutions/43000589105-chande-kroll-stop/ (TradingView 공식 지표 설명 — WebSearch로 정의·기본값 확인) / https://www.tradingview.com/script/GoHLj2XP-Chande-Kroll-Trend-Strategy-SPX-1H-PINEINDICATORS/ (TradingView 전략 스크립트, SPX 1h 최적화 사례) / https://www.tradingview.com/script/vOZX6yfP-Chande-Kroll-Stop-ADX-filter-strategy/ (ADX필터 결합판) / 원 지표: Tushar Chande·Stanley Kroll, *The New Technical Trader* (1994)
- **참여지표**: - (개별 스크립트 좋아요 수는 이번 세션에서 WebFetch 원문 대조 못함 — quantifiedstrategies.com 등 상세 페이지가 봇 차단으로 접근 불가. TradingView 내장 표준 지표라는 점에서 채택도는 높으나 정량 참여지표는 "정량 수치 원문 미확인"으로 표기)
- **백테스트 근거**: **없음(크립토 실측 백테스트 확인 못함)**. 검색된 자료는 "SPX 1시간봉에서 ATR기간10·ATR배수3·Stop길이21·SMA길이21 조합이 최적으로 보인다"는 **정성적 설명뿐**(정확한 승률·PF·표본기간 원문 미확인, quantifiedstrategies.com 봇차단으로 재확인 불가) — **정량 수치 인용 안 함, 지표 정의·표준 채택도 기반으로만 분류**.
- **타임프레임**: 15m 신호 / 1h 확인 (원문은 주로 1h~일봉 예시가 많으나, 검색 자료에 "인트라데이는 ATR기간/배수를 줄여 사용"이라는 조정 가이드가 있어 단타 슬리브로 축소 적용)
- **시장/대상**: BTC·ETH·시총상위 알트 무기한 (원문은 SPX·EURUSD 등 전통자산 예시가 다수, 크립토 실측 사례 없음 — 자산군 다름을 명시)

## 진입 규칙
- **Chande Kroll Stop 계산**:
  1. ATR(atr_period) 계산.
  2. `High Stop(1차) = 최근 atr_period봉 최고가 − atr_mult × ATR`
  3. `Low Stop(1차) = 최근 atr_period봉 최저가 + atr_mult × ATR`
  4. **최종 Short Stop(상단선)** = 최근 stop_len봉 동안의 `High Stop(1차)` 중 **최고값**(2단계 스무딩).
  5. **최종 Long Stop(하단선)** = 최근 stop_len봉 동안의 `Low Stop(1차)` 중 **최저값**.
- 롱: 종가가 **상단선(Short Stop)과 하단선(Long Stop) 둘 다보다 위로** 마감 → 상승추세 확인, 롱 진입(또는 기존 숏 반전).
- 숏: 종가가 **두 선 모두보다 아래로** 마감 → 하락추세 확인, 숏 진입(또는 기존 롱 반전).
- (원문 스크립트 변형) ADX(14) ≥ 20~25 레짐필터를 추가해 횡보장 휩쏘 억제하는 버전도 존재 — 채택 시 병행 권장.

## 청산 규칙
- 익절: 별도 목표가 없음(추세추종형) — 반대 스탑앤리버스 신호(종가가 반대편 두 선을 모두 재돌파) 발생 시 청산·반전.
- 손절: 진입 시점의 **Long Stop(롱 포지션)/Short Stop(숏 포지션)** 선 자체가 동적 손절선 역할(원 지표 설계 목적 — "Stop" 이름 그대로 손절가 제시용). 가격이 진입 반대방향으로 이 선을 재돌파하면 손절.
- 시간 청산: 원문 없음 — 채택 시 최대 홀딩 상한(15m 기준 60~100봉) 보완 권장.

## 파라미터
- atr_period=10 (기본값, 범위 5~14 — 인트라데이는 낮게: 5~7 권장)
- atr_mult=1.0 (TradingView 기본값. 백테스트 예시는 배수 3 사용 — 범위 1.0~3.0, 낮을수록 민감/휩쏘 증가)
- stop_len=9 (기본값, 백테스트 예시는 21 사용 — 범위 9~21)
- adx_filter=20~25 (선택, 원문 변형 스크립트 채택 시)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: ATR, 롤링 최고가/최저가(2단계: 1차 ATR밴드 → 그 밴드의 롤링 최고/최저). 계산 자체는 Donchian/Chandelier와 유사한 롤링윈도우 연산.
- 난이도: **낮음~중간**. 2단계 스무딩(밴드의 롤링 극값)이라는 점만 주의하면 구현은 단순. 바이낸스 REST 캔들(OHLC)만으로 100% 충족, 오더북/틱 불필요.

## 스카우트 메모
- **강점**: 손절선 자체가 지표 출력이라(이름 그대로 "Stop") 리스크관리가 지표에 내장돼 별도 손절 로직 설계 부담이 적음. TradingView 표준 내장지표라 신뢰성 있는 표준 정의를 그대로 재현 가능.
- **의심점**: (1) **크립토 백테스트 근거가 전혀 없음** — 전통자산(SPX·EURUSD) 예시뿐이라 크립토 고변동성 환경에서 휩쏘가 심할 위험, 우리 프레임워크로 최초 검증 필요. (2) 기존 `chandelier-exit-atr-trend-swing.md`(N봉 최고/최저 − ATR×배수, 1단계)와 **수학적 구조가 매우 유사**(둘 다 ATR 트레일링스탑 계열) — 다만 Chande Kroll은 **2단계 스무딩**(1차 ATR밴드의 롤링 극값을 다시 취함)이라는 점에서 지연 특성이 다르고, 진입 신호도 "두 선을 모두 재돌파"라는 이중조건이라 Chandelier(단일선 트레일링)와 신호 발생 시점이 다를 것으로 예상 — 완전 동일은 아니나 **같은 계열의 파라미터 변형**에 가까움을 인정. 우선순위는 신규 카테고리(Ehlers IT, RSI14 멀티TF 등)보다 낮게 잡는 것이 합리적.
- **우리 슬리브와의 관계**: 우리 단타 스캘프15m는 볼린저 돌파+거래량+OI 기반 브레이크아웃이고, 이건 **추세 확인 후 스탑앤리버스**(추세추종+동적 손절)라 신호 메커니즘은 다르나, ATR 트레일링 계열(Chandelier·UT Bot·Halftrend·PMAX)이 이미 다수 있어 **완전 신규 카테고리는 아님**. 낮은 우선순위 검증 대상으로 기록.
