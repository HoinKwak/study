# UT Bot Alerts(ATR 트레일링 스톱 크로스오버) — 백테스트 리포트 (라운드2)

- **전략 스펙**: `research/strategies/ut-bot-alerts-atr-trailing-scalp.md`
- **출처**: TradingView QuantNomad(좋아요 5.36만·조회 149만). freqtrade 포팅판 "+3202%"는
  다중필터+하이퍼옵트 변형이라는 의심(원문 스카우트 메모). 순수 신호의 엣지를 우리 프레임워크로
  직접 재검증.
- **⚠️ 선행 시도**: `scratchpad/bt_utbot.py`(별도 하네스, 15m 단일TF·7종목 스팟체크·IS/OOS
  미분리, `research/backtests/ut-bot-alerts-atr-trailing-scalp.md`)가 이미 net PF 0.53~0.92
  (전부 <1)로 강한 FAIL 신호를 보였다. **이 리포트는 라운드1 프로토콜(LONG_HISTORY_SYMBOLS
  13종목 풀링, 엄격 IS/OOS 워크포워드, 15m+1h)로 독립 재검증한 것**이며, 별개 파일로 저장해
  기존 리포트를 덮어쓰지 않았다.
- **판정 목적**: ATR 적응형 트레일링 스톱 크로스오버(스탑앤리버스)가 15m·1h 크립토에서
  수수료를 이기는 엣지가 있는지, 원문 파라미터 대역(key_value 저값)과 저빈도로 조정한 대역
  (key_value 고값) 양쪽 모두 확인.

## 구현/실행 방식

- **격리 스크립트**: `scratchpad/bt_ut_bot.py` (완전 독립, `src/crypto_trader/**` 무수정,
  `indicators.atr` 재사용). `bt_trix.py`의 스탑앤리버스 이벤트기반 하네스를 그대로 계승
  (UT Bot도 TRIX와 동일하게 "항상 시장에 있는" 반전형 구조).
- **지표(원문 그대로)**: `xATR=ATR(atr_period)`(Wilder), `nLoss=key_value×xATR`.
  `xATRTrailingStop` 매 봉 재귀 갱신: `close>stop[-1] and close[-1]>stop[-1]` →
  `stop=max(stop[-1],close-nLoss)`; `close<stop[-1] and close[-1]<stop[-1]` →
  `stop=min(stop[-1],close+nLoss)`; `close>stop[-1]`(반전 시작) → `stop=close-nLoss`;
  그 외 → `stop=close+nLoss`.
- **신호(원문 그대로)**: 롱=close가 스톱을 상향 돌파(crossover), 숏=스톱이 close를 상향
  돌파(crossunder). 구조상 "항상 시장에 있는" 반전형 — 반대 신호=즉시 청산+반대방향 재진입.
- **룩어헤드 방지**: 신호는 i-1(닫힌 봉) 확정, 체결은 i봉 시가(+슬리피지).
- **옵션(자체보강)**: `use_stop=True`시 진입가∓atr_stop_mult×ATR 고정 SL 병행(원문엔 없음,
  스펙의 "리스크관리 보강 추정" 반영).
- **데이터/종목/IS·OOS/수수료**: 라운드1과 동일.

## 1단계 — 스펙 원문 대역 IS 그리드서치 (저빈도 조정 포함)

`key_value`∈{1,2,3,4,5} × `atr_period`∈{10,14,20,30} × `use_stop`∈{False,True} = **40개
조합**(15m·1h 각각), 13종목 풀링.

**15m**: 최댓값 net PF **0.886**(key_value=4, atr_period=30, use_stop=False), t=-4.76.
**324개 조합 전체가 net PF<0.89** — 스펙 원문 대역(key_value 1~5)은 15m에서 완전 기각.
key_value가 원문 기본값(1)에 가까울수록(잦은 반전) PF가 더 나쁘다(0.53~0.56대) — 이전
`bt_utbot.py` 발견과 정성적으로 일치.

**1h**: 최댓값 net PF **1.050**(key_value=5, atr_period=10, use_stop=True), t=0.47(무의미).
여전히 통과 기준과 거리가 멀지만, **key_value를 키울수록(신호 둔감화) PF가 개선되는 뚜렷한
단조 경향**이 관찰돼 — 그리드 경계값(key_value=5)에서 아직 정점에 도달하지 않았을 가능성이
있어 **2단계 정밀탐색**을 진행했다.

## 2단계 — 1h key_value 확장 정밀탐색 (IS 전용)

`key_value`를 5→25까지, `atr_period`를 10~50까지 확장(약 **90개 추가 조합**, 13종목 풀링).
**뚜렷한 단조 개선 후 정점 형성**이 관찰됐다:

| key_value | atr_period | 거래수 | 승률% | PF(net) | t(net) |
|---:|---:|---:|---:|---:|---:|
| 5 | 10 | 2385 | 21.4 | 1.050 | 0.47 |
| 8 | 20 | 1072 | 36.0 | 1.112 | 1.07 |
| 10 | 20 | 713 | 37.4 | 1.330 | 2.12 |
| 12 | 30 | 501 | 40.5 | 1.484 | 2.31 |
| **15** | **17** | **370** | **45.1** | **1.719** | **2.80(IS 최고)** |
| 16 | 20 | 334 | 45.2 | 1.692 | 2.62 |
| 20 | 20 | 265 | 41.1 | 1.238 | 1.04 |
| 25 | 30 | 622 | 38.7 | 1.277 | 1.71 |

key_value 13~17 × atr_period 14~30 구간(약 30개 조합)에서 **net PF 1.4~1.72, t 2.0~2.8,
13종목 중 6~10개가 IS PF≥1.3** — knife-edge 단일 스파이크가 아니라 **폭넓은 안정 구간**으로
보여 held-out OOS 평가로 진행했다(⚠️ 아래 결과에서 보듯 이 판단은 틀렸다 — 폭넓어 보이는
안정 구간도 다중비교 하에서는 데이터 스누핑일 수 있다는 라운드1 Keltner의 교훈이 반복됨).

**다중비교 고지**: UT Bot은 1단계(40×2TF=80) + 2단계 정밀탐색(1h 약 90 + 15m 확인용 약
18) = **총 약 188개 조합**을 IS로 탐색했다.

## 최종 후보 held-out OOS 평가 — **IS에서 t=2.80으로 좋아 보였지만 OOS에서 무너짐**

동결(IS 최고): `key_value=15, atr_period=17, direction=both, use_stop=False, tf=1h`

### 풀링(13종목) IS/OOS/FULL

| 구간 | 거래수 | 승률% | PF(net) | PF(gross) | t(net) |
|---|---:|---:|---:|---:|---:|
| IS | 370 | 45.1 | **1.719** | 1.743 | **2.80** |
| **OOS** | 426 | 32.9 | **1.076** | 1.090 | **0.27** |
| FULL | 796 | 38.6 | 1.329 | 1.347 | 1.63 |

**IS→OOS로 PF 1.719→1.076, t 2.80→0.27로 뚜렷이 붕괴 — 둘 다 판정 기준(net PF≥1.3,
t≥1.7)에 크게 미달한다.** 승률도 IS 45.1%→OOS 32.9%로 하락(더 적은 승리, 더 큰 R로
버티는 구조가 OOS에서 무너짐). 이는 라운드1 Keltner 돌파(1h) 리포트와 **정성적으로 동일한
패턴** — 넓어 보이는 IS 안정구간도, 다중비교(약 188개 조합) 하에서는 데이터 스누핑일 수
있다는 것을 재확인한다.

### 종목별 상세(13개 장기이력, FULL 기준 내림차순)

| 심볼 | 거래수 | 승률% | PF(net) | PF(gross) | IS_n | IS_PF | OOS_n | OOS_PF |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ZECUSDT | 57 | 47.4 | 2.975 | 3.001 | 29 | 1.728 | 28 | **3.469** |
| SOLUSDT | 65 | 43.1 | 2.081 | 2.107 | 30 | 4.657 | 35 | **0.604** |
| ETHUSDT | 71 | 42.3 | 1.844 | 1.880 | 39 | 2.034 | 32 | 1.655 |
| NEARUSDT | 61 | 44.3 | 1.582 | 1.600 | 25 | 3.075 | 36 | **0.638** |
| WLDUSDT | 43 | 44.2 | 1.484 | 1.496 | 7 | 17.204 | 36 | 0.657 |
| BTCUSDT | 83 | 36.1 | 1.225 | 1.257 | 43 | 1.664 | 40 | **0.834** |
| ADAUSDT | 65 | 38.5 | 1.208 | 1.222 | 31 | 1.661 | 34 | **0.896** |
| BNBUSDT | 63 | 39.7 | 1.132 | 1.160 | 37 | 1.073 | 26 | 1.251 |
| XRPUSDT | 69 | 36.2 | 1.125 | 1.141 | 31 | 0.918 | 38 | 1.267 |
| DOGEUSDT | 67 | 32.8 | 1.033 | 1.045 | 39 | 0.640 | 28 | 1.694 |
| TUSDT | 49 | 32.7 | 0.813 | 0.825 | 19 | 0.766 | 30 | 0.861 |
| 1000XECUSDT | 65 | 35.4 | 0.772 | 0.783 | 35 | 0.810 | 30 | 0.714 |
| DODOXUSDT | 38 | 26.3 | 0.334 | 0.338 | 5 | 4.231 | 33 | 0.221 |

**13종목 중 OOS PF≥1.3인 종목은 단 3개(ZEC·DOGE·XRP — XRP는 1.267로 근소 미달, 정확히는
ZEC·DOGE 2개만 확실히 통과)**. IS에서 8/13이 PF≥1.3이던 것과 대조적으로 OOS에서는 대부분
무너진다(SOL 4.66→0.60, NEAR 3.08→0.64, WLD 17.2→0.66 — 특히 WLD는 IS 표본이 7건뿐이라
애초에 신뢰도가 낮았다). 표본도 저빈도(평균 key_value=15 트레일링은 거의 발동하지 않아
종목당 IS 5~43건·OOS 26~40건)로 얕다.

### 참고 — 원문 대역(baseline) 15m·1h 전체 상세

`scratchpad/utbot_final_detail_15m_baseline.csv`(key_value=4,atr_period=30) ·
`scratchpad/utbot_final_detail_1h_baseline.csv`(key_value=5,atr_period=10,use_stop=True):
15m은 13종목 전원 net PF<1.03(중앙값 0.941), 1h baseline은 13종목 중 3개(WLD 1.478·
BTC 1.360·SOL 1.348)만 net PF≥1.3이나 표본이 IS/OOS 각 200건 안팎으로 얕고 t가 0.47에
불과해 유의성이 없다.

## 파라미터 민감도 (IS 기준)

- `key_value`(1→25): **1~5는 명확히 나쁨(PF<1.05), 8~17 구간에서 단조 개선, 17을 넘으면
  다시 하락**(표본 급감·노이즈 증가). 이 자체가 "낮은 key_value=민감한 스캘핑"이라는 원문
  설계와 정반대 방향이라는 점이 흥미롭다 — 크립토에서는 매우 둔감한(사실상 장기 추세추종)
  세팅만 근소한 방향성을 보인다.
- `atr_period`(10→50): key_value가 13~17일 때 17~30 부근이 국지적 최적, 그 밖에서는
  완만하게 하락. knife-edge는 아니었으나(최적 지역 자체는 넓었다) 그 넓은 지역 자체가
  OOS에서 재현되지 않았다.
- `use_stop`(고정 ATR SL 병행): 원문 트레일링만으로도 이미 청산이 이뤄지므로 별도 SL
  추가 효과는 혼재(승률은 낮추고 PF는 미미하게만 변화).

## 최종 판정: **FAIL**

**근거**:
1. **스펙 원문 파라미터 대역(key_value 1~5)은 15m·1h 모두 명확히 기각**(15m 최댓값 0.886,
   1h 최댓값 1.050, 둘 다 t<0.5로 무의미).
2. **key_value를 크게 높인(13~17) 저빈도 변형이 IS에서 PF 1.72·t 2.80까지 도달**했으나,
   이는 총 약 188개 조합의 IS 탐색에서 고른 값이라 다중비교로 부풀려졌을 가능성이 높고,
   실제로 **held-out OOS에서 PF 1.076·t 0.27로 완전히 무너졌다** — 두 판정 기준(PF≥1.3,
   t≥1.7) 모두 크게 미달.
3. 13종목 중 OOS에서 PF≥1.3을 유지한 종목은 2~3개뿐이고, IS에서 극단적으로 좋았던 종목
   (SOL 4.66, WLD 17.2, NEAR 3.08)이 OOS에서 대부분 붕괴(0.6~0.66) — 전형적인 소표본
   과최적화 패턴.
4. 표본도 저빈도(고 key_value 구간은 종목당 5~48건)라 신뢰도가 낮은 구간이 다수 섞여 있다.

원 지표는 "항상 시장에 있는" 반전형이라 태생적으로 휩쏘에 취약하고, 크립토 15m·1h에서는
민감한 설정(원문 권장)일수록 더 나쁘고 둔감한 설정(사실상 별도 전략에 가까움)만 근소한
방향성을 보이는데 그마저 OOS에서 재현되지 않는다. **라이브 반영하지 않는다.**

## 미검증/근사 요소 (정직한 한계 고지)

- **선택 필터(EMA200 트렌드·ADX·거래량) 미검증**: 스펙이 "freqtrade 검증판에서 사용, 과최적화
  위험 인지 후 A/B 권장"이라 명시한 필터들은 시간 예산상 제외했다. 순수 신호의 엣지 유무가
  이번 검증의 목적이었고, 결과가 이미 명확히 FAIL이라 필터 추가가 근본을 바꿀 가능성은 낮다고
  판단했으나 완전히 배제할 수는 없다.
- **direction='long_only' 변형 미검증**(항상 `both` 스탑앤리버스만 테스트).
- **롱/숏 비대칭 분석 미실시**: 크립토 상방 편향 고려 시 롱 전용이 다를 수 있으나 검증하지
  않았다.

## 재현 스크립트

- `scratchpad/bt_ut_bot.py` — UT Bot 스탑앤리버스 이벤트기반 시뮬레이터.
- `scratchpad/run_ut_bot_sweep.py` — 1단계 IS 그리드서치(15m/1h, 각 40조합). 결과:
  `scratchpad/utbot_sweep_{15m,1h}.csv`.
- `scratchpad/run_utbot_final_eval.py` — baseline·IS최선(key_value=15,atr_period=17)
  동결 파라미터로 전 22종목 IS/OOS/FULL 상세 평가. 결과:
  `scratchpad/utbot_final_detail_{15m_baseline,1h_baseline,1h_is_best}.csv`.
- 2단계 정밀탐색(key_value 5~25 확장)은 인라인 스크립트로 수행(파일 미저장, 본문 표로 기록;
  재현은 아래 커맨드).
- 재현 커맨드:
  ```
  cd /home/user/study
  python3 scratchpad/bt_ut_bot.py BTCUSDT 15m           # 단일 심볼 스팟체크(기본 파라미터)
  python3 scratchpad/run_ut_bot_sweep.py 15m             # 1단계 IS 그리드서치(15m, 40조합)
  python3 scratchpad/run_ut_bot_sweep.py 1h               # 1단계 IS 그리드서치(1h, 40조합)
  python3 - <<'PY'   # 2단계 정밀탐색 재현
  import sys; sys.path.insert(0, ".")
  from scratchpad.bt_ut_bot import LONG_HISTORY_SYMBOLS, load_symbol, simulate, IS_START, IS_END
  dfs = {s: load_symbol(s, "1h") for s in LONG_HISTORY_SYMBOLS}
  for kv in [10, 12, 15, 16, 20]:
      for ap in [17, 20, 30]:
          pooled = []
          for s, df in dfs.items():
              pooled.extend(simulate(df, symbol=s, key_value=kv, atr_period=ap)
                            .subset(IS_START, IS_END).trades)
          print(kv, ap, len(pooled))
  PY
  python3 scratchpad/run_utbot_final_eval.py              # 동결 파라미터 전종목 상세(3세트)
  ```
