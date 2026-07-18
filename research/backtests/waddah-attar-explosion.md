# Waddah Attar Explosion(MACD 모멘텀+볼린저/켈트너 변동성 폭발) 다중조건 돌파 — 백테스트 리포트 (라운드4)

- **전략 스펙**: `research/strategies/waddah-attar-explosion-volatility-breakout-scalp.md`
- **출처**: TradingView "Waddah Attar Explosion" 계열(좋아요 1.2만+·6.3천). **핵심 파라미터
  (sensitivity=150 등)가 원문 Pine 코드 직접대조 실패 — 2차 소스 검색엔진 종합 추정치**.
  백테스트 정량 근거 없음(참여지표 기반 채택) — 직접 검증이 목적.
- **라운드**: 4(다중조건/다중TF 확인 스태킹 전략 — 우리 라이브 유일 흑자 전략 scalp15m의
  프로파일에 맞춘 검증. **Waddah는 이 셋 중 scalp15m과 메커니즘이 가장 유사**(다중조건
  동시충족 돌파)해 특히 주의 깊게 검증).
- **판정 목적(코디네이터 핵심 진단)**: (a) 필터無 baseline gross PF, (b) 전체 필터스택
  (거래량+강봉+스퀴즈전조) 적용 후 gross PF, (c) net PF 를 나눠 다중조건이 얼마나
  gross PF를 끌어올리는지 측정.

## 구현/실행 방식

- **격리 스크립트**: `scratchpad/bt_waddah.py` (완전 독립, `src/crypto_trader/**` 무수정,
  `indicators.bollinger_bands`/`atr`/`ema` 재사용).
- **핵심 3조건(원문 그대로)**: `t1=(EMA_fast-EMA_slow)의 1봉 변화×sensitivity`,
  `explosion=BB상단-BB하단`, `deadzone`(V2 권장: ATR(100)×k, 크립토 가격스케일 대응).
  롱=t1>0 AND t1>explosion AND t1>deadzone. 숏 대칭.
- **⚠️ 파라미터 스케일 문제 발견**: 원문 스니펫 종합값 `sensitivity=150`을 그대로 적용하면
  t1이 explosion/deadzone 대비 만성적으로 과대해져 **전체 봉의 30%+가 "폭발" 조건을
  만족**(BTC 1h 기준 long_core 31%, short_core 31% — "희귀한 폭발적 돌파"라는 개념과
  모순). 이는 sensitivity가 특정 가격 스케일(아마 저가 통화쌍)을 전제로 설계돼 크립토
  대형코인 절대가격(BTC $수만)에는 그대로 이식되지 않는다는 뜻 — **정직한 한계로 명시**,
  sensitivity를 20~150까지 스윕해 "진짜 희귀 이벤트"에 해당하는 영역(20~50, 발생률
  0.05~8%)까지 함께 탐색했다.
- **추가 스택 필터(자체보강, 코디네이터 지시)**: `use_volume_filter`(거래량≥1.5×평균),
  `use_body_filter`(몸통≥0.7×ATR, scalp.py 강봉 조건과 동일), `use_squeeze_precursor`
  (신호 직전 밴드폭이 최근 50봉 분포 하위 45%ile였다가 지금 확장 — "진짜 폭발"과 "이미
  벌어진 상태"를 구분).
- **청산(원문 그대로)**: 히스토그램이 데드존 아래로 재진입 또는 반대색 전환 시 청산.
  SL=신호봉 시가 기준(scalp.py와 동일 관례) stop_mult×신호봉 몸통.
- **룩어헤드 방지**: 신호는 i-1(닫힌 봉) 확정, 체결은 i봉 시가.
- **데이터/종목/IS·OOS/수수료**: 라운드1~3과 동일.

## IS 그리드서치 (파라미터 선택 — OOS 미접촉)

`sensitivity`∈{20,30,50,75,100,150} × `deadzone_atr_mult`∈{1.5,2.0,3.7} × `stop_mult`∈
{1.0,1.5} × `stack`∈{none(베이스라인), full(거래량+강봉+스퀴즈전조 전부)} = **72개 조합**
(15m·1h 각각), 13종목 풀링.

### (a) 필터無 baseline gross PF

| TF | 최선 조합 | 거래수 | PF(net) | PF(gross) | t |
|---|---|---:|---:|---:|---:|
| 1h | sensitivity=20, deadzone_mult=3.7, stop_mult=1.5 | 83 | 0.786 | **0.891** | -0.69 |
| 15m | sensitivity=20, deadzone_mult=3.7, stop_mult=1.5 | 248 | 0.588 | **0.726** | -2.92 |

**필터 없는 베이스라인은 15m·1h 모두 gross PF가 1.0을 넘지 못한다.**

### (b) 전체 필터스택(거래량+강봉+스퀴즈전조) 적용 후 gross PF

| TF | 최선 조합 | 거래수 | PF(net) | PF(gross) | t |
|---|---|---:|---:|---:|---:|
| 1h | sensitivity=30, deadzone_mult=3.7, stop_mult=1.5 | 1121 | 0.739 | **0.880** | -3.10 |
| 15m | sensitivity=20, deadzone_mult=3.7, stop_mult=1.5 | 171 | 0.772 | **0.966** | -1.14 |

**1h는 필터스택이 오히려 baseline보다 근소하게 낮고(0.891→0.880), 15m은 필터스택이
baseline 대비 뚜렷이 개선(0.726→0.966)되지만 여전히 1.0 문턱을 넘지 못한다.**

### (c) net PF

72개 조합 전체에서 **net PF 최댓값이 15m 0.772·1h 0.786** — 둘 다 1.0 미만이며 물론
통과 기준(1.3)과는 거리가 훨씬 멀다.

**다중비교 고지**: Waddah는 15m 72 + 1h 72 = **총 144개 조합**을 IS로 탐색했다.

## 최종 판정: **FAIL**

**근거**:
1. **필터 없는 baseline과 전체 필터스택 모두, 15m·1h 어느 쪽도 gross PF가 안정적으로
   1.0을 넘지 못한다** — 15m에서만 필터스택이 baseline 대비 뚜렷한 개선(+0.24p)을
   보이지만 그마저 1.0 미만이다. **코디네이터의 핵심 질문("다중조건이 gross PF를 1.0
   위로 올리는가")에 대한 답은 "아니오"다.**
2. 파라미터 스케일 문제(원문 sensitivity=150이 크립토 대형코인에 부적합)를 인지하고
   20~150까지 폭넓게 재보정했음에도 결과가 바뀌지 않았다 — 파라미터 미확정 문제가
   아니라 신호 자체의 방향성 우위 부재로 보인다.
3. **우리 라이브 유일 흑자 전략(scalp15m)과 메커니즘이 가장 유사함에도** — scalp15m은
   볼린저 이탈+거래량 급증+강봉+확인TF 레짐(4중 조건) 조합인 반면, Waddah는 MACD
   모멘텀 변화량이라는 **거래량을 쓰지 않는** 파생지표를 중심 신호로 삼는다는 점이
   결정적 차이로 보인다 — "다중조건 자체"가 아니라 **"거래량 급증이라는 특정 조건"이
   scalp15m 흑자의 핵심 동력**일 가능성을 시사(Waddah의 자체보강 거래량 필터를 추가해도
   1.0을 못 넘긴 것과 대조적으로, scalp15m 원 설계는 거래량이 핵심 게이트).
4. 표본은 충분(15m 수백~수천 건)해 표본부족 문제는 아니다.

**라이브 반영하지 않는다.**

## 미검증/근사 요소 (정직한 한계 고지)

- **원문 Pine 코드 직접 대조 실패**(2차 소스 종합치만 사용) — sensitivity/fastLength/
  slowLength 등이 원문과 다를 가능성이 있으나, 넓은 sensitivity 스윕(20~150)으로 이
  불확실성을 어느 정도 커버했다.
- **켈트너 range를 SMA(TrueRange) 대신 Wilder ATR로 근사**(TTM 스퀴즈 리포트와 동일
  한계) — deadzone 계산에 영향.
- **HTF 확인 필터 미검증**(스펙엔 명시 없음, 자체 추가 안 함).
- **부분청산(모멘텀 소진 시)은 파샬 없이 전량청산으로 단순화**(Simplicity).

## 재현 스크립트

- `scratchpad/bt_waddah.py` — Waddah Attar Explosion 이벤트기반 시뮬레이터(다중 스택 필터
  옵션 포함).
- `scratchpad/run_waddah_sweep.py` — IS 전용 그리드서치(15m/1h, 각 72조합, baseline/full
  스택 비교). 결과: `scratchpad/waddah_sweep_{15m,1h}.csv`.
- 재현 커맨드:
  ```
  cd /home/user/study
  python3 scratchpad/bt_waddah.py BTCUSDT 1h        # 단일 심볼 스팟체크(기본 파라미터)
  python3 scratchpad/run_waddah_sweep.py 15m        # IS 그리드서치(15m, 72조합)
  python3 scratchpad/run_waddah_sweep.py 1h         # IS 그리드서치(1h, 72조합)
  ```
