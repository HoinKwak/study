# Williams %R 극단(-90/-30) 평균회귀 반전 — 백테스트 리포트 (라운드3)

- **전략 스펙**: `research/strategies/williams-r-extreme-reversal-scalp.md`
- **출처**: QuantifiedStrategies "Williams %R Trading Strategy (81% Win Rate)" — **핵심
  근거는 QQQ(나스닥100 ETF), 크립토 무기한 데이터로 직접 검증되지 않음**. 원문 스스로
  "크립토는 -90~-95까지 봐야 진짜 과매도"라 경고.
- **라운드**: 3(평균회귀 국면 전환 — 라운드1·2의 돌파·추세·모멘텀 6종이 전부 gross PF조차
  ~1.0 미만이었던 것에 대응, 라운드1·2와 동일 프로토콜로 평균회귀 계열 검증).
- **⚠️ 선행 시도**: `research/backtests/williams-r-extreme-reversal-scalp.md`(별도 하네스
  `scratchpad/bt_williams_r.py`, 12종목·15m 4.5년+10종목·5m 6.4개월, **backtest-reviewer
  감사 완료(VALID)**)가 이미 **22/22 종목·기간 조합에서 PF<1.0(최고 0.872)**, 강건한
  FAIL을 확정했다. 감사는 심지어 **수수료·슬리피지를 0으로 둬도 BTC/SOL이 PF 1.12~1.13에
  그치는 "미미한 원시 엣지가 고회전율 탓에 소멸"**이라는 정밀 진단까지 남겼다. 이번
  라운드3는 **다른 슬러그**(`williams-r-extreme-reversal`, "-scalp" 미포함)로 라운드1·2
  프로토콜(13종목 장기이력 풀링, 엄격 IS/OOS 워크포워드, 15m·1h)을 사용해 독립
  재검증한 것이며, 기존 상세 리포트를 덮어쓰지 않았다.
- **판정 목적**: 극단 %R 반전이 15m·1h 크립토에서 수수료를 이기는 엣지가 있는지, 라운드1·2
  프로토콜(13종목 풀링·IS 2022-01~2024-06/OOS 2024-07~2026-06)로 재확인.

## 구현/실행 방식

- **격리 스크립트**: `scratchpad/bt_williams_r.py`(이번 라운드용 신규 파일, 기존
  `bt_williams_r.py`와 이름은 같으나 라운드1·2 하네스 스타일로 재작성 — LONG_HISTORY_SYMBOLS
  13종목 풀링·IS/OOS 자동분할 지원). `src/crypto_trader/**` 무수정, `indicators.atr`/`ema`
  재사용.
- **지표**: `%R(period) = (최근N봉 최고가-종가)/(최근N봉 최고가-최근N봉 최저가) × -100`.
- **진입(신호봉 i-1, 닫힌 봉)**: 롱 = %R<=os_threshold(기본 -90, 크립토 보정 -92~-95).
  숏(대칭 확장) = %R>=-(100+os_threshold). (옵션) trend_filter=EMA200: 롱은 종가>EMA200,
  숏은 종가<EMA200일 때만.
- **청산**: 종가가 직전 봉 고가 상회(롱)/저가 하회(숏) **또는** %R이 ob_threshold(기본
  -30, 숏은 대칭 -(100+ob_threshold)) 회복 시 청산. SL=진입가∓sl_atr_mult×ATR(14). 시간청산:
  max_hold_bars.
- **룩어헤드 방지**: 신호는 i-1(닫힌 봉) 확정, 체결은 i봉 시가(+슬리피지).
- **데이터/종목/IS·OOS/수수료**: 라운드1·2와 동일.

## IS 그리드서치 (파라미터 선택 — OOS 미접촉)

`williams_period`∈{14,21} × `os_threshold`∈{-90,-92,-95} × `ob_threshold`∈{-30,-40,-50} ×
`trend_filter`∈{False,True} × `sl_atr_mult`∈{1.5,2.0} × `max_hold_bars`∈{10,20,30} =
**총 216개 조합**(15m·1h 각각), 13종목 풀링.

**15m**: 최댓값 net PF **0.546**, 최댓값 gross PF **0.877**(williams_period=21, os=-95,
ob=-30, trend_filter=True, sl_mult=2.0, hold=10). **216개 조합 전체에서 gross PF가 1.0을
넘지 못했다.**

**1h**: 최댓값 net PF **0.827**, 최댓값 gross PF **1.007**(williams_period=21, os=-95,
ob=-40, trend_filter=True, sl_mult=2.0, hold=20). gross PF가 아주 근소하게 1.0을 넘는
지점이 있으나, net PF는 0.83으로 크게 미달이고 t=-3.0(음의 방향 유의).

**추세필터(trend_filter) 효과**: **모든 상위권 결과가 trend_filter=True**(EMA200 게이트)
다 — 원문에 없던 자체 보강 필터지만, 크립토에서는 필수적으로 도움이 된다(강추세에서 극단
%R에 오래 머무는 크립토 특성상 무필터 역추세 베팅은 더 나쁘다는 스카우트 메모의 우려가
실증됨).

**다중비교 고지**: Williams %R은 15m 216 + 1h 216 = **총 432개 조합**을 IS로 탐색했다.

## 최종 채택(그래도 통과 기준 미달) 파라미터 — held-out OOS 평가

**15m**: `williams_period=21, os_threshold=-95, ob_threshold=-30, trend_filter=True,
sl_atr_mult=2.0, max_hold_bars=10`
**1h**: `williams_period=21, os_threshold=-95, ob_threshold=-40, trend_filter=True,
sl_atr_mult=2.0, max_hold_bars=20`

### 풀링(13종목) IS/OOS/FULL

| TF | 구간 | 거래수 | 승률% | PF(net) | PF(gross) | t(net) |
|---|---|---:|---:|---:|---:|---:|
| 15m | IS | 10,205 | 53.2 | 0.546 | 0.877 | -22.56 |
| 15m | OOS | 10,786 | 52.5 | 0.535 | 0.843 | -23.62 |
| 15m | FULL | 21,013 | 52.9 | 0.540 | 0.858 | -32.76 |
| 1h | IS | 1,812 | 61.4 | 0.827 | 1.006 | -3.04 |
| 1h | OOS | 2,437 | 58.6 | 0.788 | 0.950 | -4.42 |
| 1h | FULL | 4,256 | 59.7 | 0.802 | 0.971 | -5.42 |

**1h의 IS 최선(gross PF 1.006, 사실상 손익분기)조차 OOS에서 0.950으로 하락** — 우연한
IS 잡음 수준이었을 가능성이 높다.

### 종목별 상세(13개 장기이력, FULL 기준 내림차순)

**15m**: 전 종목 net PF<0.72, 중앙값 0.564. **13종목 중 net PF≥1.3: 0개.**

**1h**: ETH 1.013·NEAR 0.999로 상위 2개 종목만 근소하게 1.0 근처, 나머지 11개는 1.0
미만. 중앙값 0.789. **13종목 중 net PF≥1.3: 0개.**

(전체 상세: `scratchpad/williams_r_final_detail_{15m,1h}.csv`)

## 파라미터 민감도 (IS 기준)

- `williams_period`(14 vs 21): 21(더 긴 룩백, 원문 최적 "2일"과는 방향이 반대이나 크립토
  15m/1h에서는 긴 쪽이 나음)이 14보다 일관되게 우세.
- `os_threshold`(-90~-95): 더 극단적인 임계값(-95, 크립토 보정)이 -90보다 일관되게 우세 —
  원문의 "크립토는 더 극단까지 봐야 한다"는 경고와 정확히 일치하는 방향이나, 그럼에도
  1.0 문턱을 넘지 못한다.
- `trend_filter`: **True(EMA200 게이트)가 False보다 일관되게 우세** — 필터 없이 극단
  %R만으로 진입하면 강추세에서 "칼날 잡기"에 당하는 위험이 실증적으로 확인된다.
- `sl_atr_mult`/`max_hold_bars`: 상대적으로 영향 작음.
- **이전 시도의 정밀 진단과 일치**: 이전 backtest-reviewer 감사가 밝힌 "손절 폭을 10배
  넓혀도 PF가 요지부동, 청산의 98.5%가 익절인데 그 익절조차 평균 -0.09%"라는 구조적
  결함(회복 신호 자체가 너무 빨리 발동해 유의미한 반등 전에 청산됨)이 이번 파라미터
  민감도에서도 동일하게 나타난다 — SL/시간청산을 흔들어도 결과가 거의 안 바뀌는 이유.

## 최종 판정: **FAIL**

**근거**:
1. **IS 그리드서치(432개 조합)에서 gross PF 최댓값이 15m 0.877·1h 1.007** — 15m은
   수수료 이전에도 1.0을 넘지 못했고, 1h도 사실상 손익분기 수준에서만 근소하게 넘겼다.
2. **held-out OOS는 IS와 비슷하거나 더 나쁜 수준**(15m 0.877→0.843, 1h 1.006→0.950) —
   IS→OOS 붕괴형 과최적화가 아니라 애초에 엣지가 없는 케이스.
3. **13개 장기이력 종목 전원(15m·1h 공통) net PF<1.3.**
4. **기존 상세 리포트(`williams-r-extreme-reversal-scalp.md`, backtest-reviewer 감사
   VALID)의 결론과 완전히 일치** — 그 리포트는 22개 종목·기간 조합 전부 PF<1.0을
   확인했고, 이번 라운드3(13종목·15m/1h·엄격 워크포워드)도 동일 결론에 도달했다. 두
   개의 독립적인 하네스·종목풀·기간에서 같은 결론이 나온 것은 FAIL 판정의 강건성을
   더욱 뒷받침한다.

원문(QQQ 기준)의 "72% 승률" 주장과 달리, 크립토 15m/1h Williams %R 극단은 승률 자체는
52~61%로 나쁘지 않으나(극단 진입 자체에 약한 방향성 우위는 있음) 청산 규칙("직전봉 고/저
상회" 또는 "%R 회복")이 반등을 충분히 기다리지 못하고 너무 일찍 청산시켜 손익비가
무너진다. **라이브 반영하지 않는다.**

## 미검증/근사 요소 (정직한 한계 고지)

- **원문의 2일 룩백 최적치(주식 일봉 기준)는 크립토 15m/1h에 그대로 대응되지 않음** —
  이번 검증은 14/21봉(각 TF의 인트라데이 스케일)만 스윕했다.
- **손절 방식 대안 미검증**: 기존 상세 리포트가 테스트한 `stop_mode='tight'`(신호봉
  저점/고점 이탈, 스펙 문구 "이탈 또는 ATR"의 직역)는 이번 스크립트에 구현하지 않았다
  (기존 리포트에서 이미 이 방식이 `atr_only`보다 훨씬 나쁨(BTC PF 0.183)을 확인했으므로
  재검증 우선순위를 낮췄다).
- **비용 0 가정 하 원시엣지 재확인은 이번 라운드에서 재실행하지 않음** — 기존 리포트의
  backtest-reviewer 감사가 이미 "수수료 0이어도 BTC/SOL PF 1.12~1.13에 그친다"는 것을
  확인했으므로, 이번 13종목 확장판에서도 유사하거나 그 이하일 것으로 추정되나 직접
  재계산하지는 않았다.

## 재현 스크립트

- `scratchpad/bt_williams_r.py` — Williams %R 극단반전 이벤트기반 시뮬레이터(라운드1·2
  하네스 스타일, 이번 라운드 신규 작성).
- `scratchpad/run_williams_r_sweep.py` — IS 전용 그리드서치(15m/1h, 각 216조합). 결과:
  `scratchpad/williams_r_sweep_{15m,1h}.csv`.
- `scratchpad/run_williams_r_final_eval.py` — 동결 파라미터로 전 22종목 IS/OOS/FULL 상세
  평가. 결과: `scratchpad/williams_r_final_detail_{15m,1h}.csv`.
- 재현 커맨드:
  ```
  cd /home/user/study
  python3 scratchpad/bt_williams_r.py BTCUSDT 1h        # 단일 심볼 스팟체크(기본 파라미터)
  python3 scratchpad/run_williams_r_sweep.py 15m        # IS 그리드서치(15m, 216조합)
  python3 scratchpad/run_williams_r_sweep.py 1h         # IS 그리드서치(1h, 216조합)
  python3 scratchpad/run_williams_r_final_eval.py       # 동결 파라미터 전종목 상세
  ```
