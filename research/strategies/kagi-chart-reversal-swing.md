# 카기차트(Kagi) 극성 전환 리버설 [스윙]

- **출처**: 구성 규칙·매매 로직 참고 — Nurlan Zhagipar, "Mastering Kagi Charts in MQL5 (Part 2): Implementing Automated Kagi-Based Trading" https://www.mql5.com/en/articles/20378
  보조: GoCharting "Kagi Chart: Trend Reversal Strategy & Guide" https://gocharting.com/docs/charting/chart-types/kagi ,
  MyForexVPS "What is a Kagi Chart?" https://myforexvps.com/what-is-a-kagi-chart-a-comprehensive-guide-to-understanding-and-using-kagi-charts/
- **참여지표**: - (기술 블로그/기사 기반, 조회수·좋아요 수치 없음)
- **백테스트 근거**: MQL5 원문에 **Nikkei(JPN225), 2024년 1~12월** 구간 백테스트 언급 있으나 **승률·PF·수익률 등 정량 수치는 원문에 명시되지 않음**("modest but steady profitability"라는 정성적 서술만 존재) → **정량 수치 원문 미확인**으로 표기. 또한 원문 대상은 **크립토가 아닌 일본 주가지수 선물** — 자산군 상이함을 명시.
- **타임프레임**: 4h~1d 종가 기준으로 카기 라인 구성(카기는 시간축이 아닌 가격 전환 기준 차트라 원 시간봉과 별개로 구성됨).
- **시장/대상**: BTC·ETH 무기한(변동성 큰 알트는 리버설 기준폭 과최적화 위험 있어 메이저 우선).

## 핵심 아이디어
카기차트는 시간이 아닌 **가격 반전폭(reversal amount)** 기준으로 선을 그리는 차트. 가격이 기준폭 이상 같은 방향으로 가면 선을 연장(굵은선=Yang/상승국면, 얇은선=Yin/하락국면 유지), **반대 방향으로 기준폭 이상 반전하면 극성이 전환**(Yin→Yang 또는 Yang→Yin)되며 이 전환점이 매매 신호가 된다.

## 진입 규칙
1. `reversal_amount = ATR(14, 4h) × 2.0` (크립토 고변동성 대응 — 원문은 "ATR×3"도 제시하나 스윙 빈도 확보 위해 2.0 채택, 감도 파라미터화).
2. 카기 라인 구성(종가 기준):
   - 현재 라인 방향이 상승(Yang)이고 종가가 기존 최고점보다 낮게 `reversal_amount` 이상 하락 → **Yin으로 전환**.
   - 현재 라인 방향이 하락(Yin)이고 종가가 기존 최저점보다 높게 `reversal_amount` 이상 상승 → **Yang으로 전환**.
   - 그 외에는 같은 방향 연장(단순 고저 갱신, 극성 유지).
3. **롱**: Yin→Yang 전환 발생 시점의 다음 봉 시가(또는 전환 확정 종가)에 진입.
4. **숏**: Yang→Yin 전환 발생 시점의 다음 봉 시가에 진입.
5. (선택) 전환 시 직전 어깨(shoulder, 이전 국면의 극값)를 **돌파**하는 "복합 전환(complex reversal)"만 채택해 약한 전환(단순 반전) 노이즈 제외 — 원문에서 세 가지 전환 유형(단순/복합/희귀) 구분.

## 청산 규칙
- 손절: 롱은 전환 직전 국면의 최저점(waist), 숏은 직전 국면의 최고점(shoulder) 바로 너머.
- 익절: 손절폭 기준 R:R = 1:2 고정 목표(원문은 1:1~1:6 선택형 제시, 스윙 특성상 2.0 채택).
- 시간/조건 청산: 반대 방향 극성 전환 발생 시 즉시 청산(스탑앤리버스 대안으로 "청산만" 옵션도 가능).

## 파라미터
- reversal_mult=2.0×ATR14 (범위 1.5~3.0, 크립토 고변동 시 상향)
- atr_period=14 (범위 10~20)
- rr_ratio=2.0 (범위 1.0~3.0)
- complex_reversal_only=True/False (노이즈 필터 옵션)

## 코딩 난이도 / 데이터 요구
- 필요한 지표: ATR(14), 카기 라인 구성 로직(상태기계 — 현재 방향·기준 극값을 순회하며 갱신, 직접 구현 필요). 전부 캔들 종가/ATR 기반.
- 주의: **바이낸스 REST 캔들로 완전 구현 가능**하나, 카기는 표준 지표 라이브러리에 없어 **상태기계를 직접 코딩**해야 함(난이도 중). 시간축이 아닌 가격축 차트라 "몇 봉째 신호"같은 시간 기반 로직과 혼용 시 주의.

## 스카우트 메모
- 강점: 기존 보유 대체차트 계열(`renko-brick-breakout-swing`, `three-line-break-reversal-trend-swing`, `point-and-figure-double-top-bottom-breakout-swing`)과 "노이즈 필터링된 가격 전용 차트" 컨셉은 유사하나, **카기 고유의 굵기(Yin/Yang) 극성 전환 로직**은 구조적으로 다름(르네코는 고정폭 벽돌, P&F는 열 전환, 3선전환은 N개 반대선 돌파) — 순수 신규 개념으로 판단.
- 의심점: 원문 백테스트가 **정량 수치 없이 정성적 서술뿐**이고 자산군도 크립토가 아님(닛케이 선물) — 근거가 약함. 참여지표(조회수·좋아요)도 없어 순수 "규칙 명확성" 기준으로만 채택. reversal_amount 캘리브레이션에 따라 신호 빈도가 크게 달라져 과최적화 위험 큼.
- 우리 스윙 슬리브와의 관계: 기존 대체차트 전략들과 **부분 중복 위험**(둘 다 노이즈 필터링 목적) — 채택 시 르네코/3선전환과 신호 상관 먼저 확인 권장. 백테스트 우선순위는 낮음(정량 근거 최약).
