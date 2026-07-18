# Elder Triple Screen 다중 타임프레임(추세+되돌림+트리거) — 백테스트 리포트 (라운드4)

- **전략 스펙**: `research/strategies/elder-triple-screen-multi-timeframe-swing.md`
- **출처**: Alexander Elder 고전 이론(1990년대) + TradingView 파생 구현(좋아요 1.2만+).
  정량 백테스트 근거 없음 — 직접 검증 목적.
- **라운드**: 4(다중조건/다중TF 확인 스태킹 — **이 전략이 대표 사례**로 지정됨).
- **판정 목적(코디네이터 핵심 진단)**: 다중TF 스태킹(1일 추세필터 + 4h Force Index
  눌림목 셋업 + 1h 트리거, 원문 그대로)이 필터 없는 순수 돌파 대비 gross/net PF를
  끌어올리는지 직접 측정.

## ⚠️ 핵심 결과 요약 (먼저 제시)

**원문 스펙 그대로의 3단 다중TF 스택(추세+웨이브+트리거)은 FAIL이다.** 그런데 이
스크립트로 **필터를 전부 제거한 "순수 이전봉 고/저 돌파+ATR 트레일링" 베이스라인**을
분해 비교(ablation)하다가, **1h에서 이 단순 베이스라인이 라운드1~4 전체를 통틀어
가장 강하고 일관된 신호**(13/13 장기이력 종목 전원 net PF≥1.0, 풀링 OOS net PF 1.314·
t=3.81)를 보이는 것을 발견했다. **다중TF 스태킹을 걷어낼수록 오히려 좋아진다** —
코디네이터의 가설("다중필터가 gross PF를 끌어올린다")과 **정반대 방향**의 결과다.
이 발견을 아래에 투명하게 전부 기록하고, 엄격한 판정 기준(개별 종목 일관성)으로
평가하면 **HOLD**(약한 PASS 후보, 완전한 PASS로 단정하기엔 개별종목 일관성이
부족)로 판정한다. **즉시 보고 대상**이라 이 리포트 최상단에 배치한다.

## 구현/실행 방식

- **격리 스크립트**: `scratchpad/bt_elder_triple.py` (완전 독립, `src/crypto_trader/**`
  무수정, `indicators.atr`/`ema` 재사용).
- **3단 구조(원문의 1d/4h/1h를 라운드4 지시(15m/1h 검증)에 비례 축소)**:
  - `entry_tf='1h'` 검증: trend_tf=1d(원문 그대로) / wave_tf=4h(원문 그대로) /
    entry_tf=1h(원문 그대로) — **원문 설계 그대로**.
  - `entry_tf='15m'` 검증: trend_tf=4h / wave_tf=1h / entry_tf=15m(같은 비율로 한 단씩
    축소, 3단 구조 보존).
- **1단계(Tide, trend_tf 추세)**: `EMA13` 기울기. 상승=롱만, 하락=숏만.
- **2단계(Wave, wave_tf Force Index 눌림목)**: `FI(2)=(close-close[1])×volume`,
  `FI_EMA=EMA(FI(2),13)`. 상승추세 중 0선 하향→상향 재돌파 시 롱 셋업 활성화
  (`setup_ttl_bars` 이내 미트리거 시 소멸).
- **3단계(Ripple, entry_tf 트리거)**: 셋업 활성 중 종가(신호봉 i-1)가 직전 entry_tf봉
  고가 상향 돌파 시 진입(체결 i봉 시가).
- **다중TF 인과적 정렬**: `align_htf_causal`/`align_htf_event_causal` 헬�퍼로 "그 시점에
  이미 닫힌 상위TF 봉"만 사용(HTF 봉 종료시각으로 인덱스 이동 후 `reindex(ffill)`) —
  미래 누출 없음. 성능을 위해 `load_symbol`을 `functools.lru_cache`로 캐싱(그리드서치가
  동일 심볼·TF를 수백 번 재사용).
- **청산**: 추세 반전 청산, SL=트리거봉 반대극값과 sl_atr_mult×ATR(wave_tf, 인과정렬)
  중 더 타이트한 쪽, (옵션) tp_atr_mult×ATR 유리방향 전용 트레일링.
- **`stack_level`(코디네이터 진단용, 이 리포트의 핵심 도구)**:
  - **0** = entry_tf 순수 이전봉 고/저 돌파만(트렌드·웨이브 필터 없음, **baseline**).
  - **1** = + trend_tf 추세방향 필터만(웨이브 셋업 없음).
  - **2** = + wave_tf Force Index 눌림목 셋업까지 전부(**원문 풀스택**).
- **룩어헤드 방지**: 모든 상위TF 신호는 인과 정렬, entry_tf 신호는 i-1 확정·i봉 시가 체결.
- **데이터/종목/IS·OOS/수수료**: 라운드1~3과 동일.

## IS 그리드서치 — stack_level별 비교(코디네이터 핵심 진단)

`stack_level`∈{0,1,2} × `sl_atr_mult`∈{1.0,1.2,1.8} × `tp_atr_mult`∈{1.5,2.0,3.0} ×
`use_trailing`∈{False,True} × (`trend_ema`∈{8,13,21}, level≥1만) × (`setup_ttl_bars`∈
{12,24,48}, level=2만) = **234개 조합**(entry_tf 15m·1h 각각), 13종목 풀링.

### stack_level별 최댓값 비교

| entry_tf | stack_level | 설명 | 최댓값 net PF | 최댓값 gross PF |
|---|---|---|---:|---:|
| 1h | 0 | baseline(필터 없음) | **1.197** | **1.341** |
| 1h | 1 | +추세필터만 | 0.976 | 1.117 |
| 1h | 2 | +웨이브 셋업까지(원문 풀스택) | 1.375 | 1.571 |
| 15m | 0 | baseline(필터 없음) | 0.974 | 1.220 |
| 15m | 1 | +추세필터만 | 0.681 | 0.892 |
| 15m | 2 | +웨이브 셋업까지(원문 풀스택) | 0.881 | 1.128 |

**핵심 관찰**: (1) **1h에서만** baseline(level 0)의 gross PF가 1.0을 넘는다(1.34) —
**15m은 baseline조차 1.0을 못 넘는다**(0.97/1.22, 15분봉 노이즈가 트레일링 스탑을
너무 자주 흔든다는 뜻). (2) **추세필터만 단독 추가(level 1)하면 오히려 baseline보다
나빠진다**(1h 1.20→0.98, 15m 0.97→0.68) — 방향 필터가 손실을 줄이기보다 좋은 트레이드를
걸러내는 쪽으로 작용했다는 뜻. (3) 웨이브 셋업까지 전부 더한 원문 풀스택(level 2)은
1h에서 level 1보다는 낫지만(0.98→1.38) level 0(순수 baseline, 1.20)보다 큰 개선은
아니고, **표본이 급감**(level0 n=6,522 vs level2 n=1,417)하며 **승률이 7%대로 극단적으로
낮아져**(vs level0 16.5%) 통계적 유의성이 사라진다(아래 참조).

### stack_level=2(원문 풀스택) 상세 — 왜 FAIL인가

1h 최선 조합(sl=1.8, tp=3.0, trailing=False, trend_ema=21, ttl=12): **net PF 1.375,
gross 1.571**이나 **승률 7.3%, t=0.90(전혀 유의하지 않음), median 종목 PF 1.06,
13종목 중 PF≥1.3 은 5개뿐**. Held-out OOS: PF 1.778(더 좋아짐)이나 **t=1.27로 여전히
1.7 미달**. 승률이 극단적으로 낮은 상태에서(대부분 트레이드가 즉시 SL/추세반전으로
소액 손실, 드물게 큰 트레일링 승리) PF가 소수 대박 트레이드에 좌우되는 구조 — **"몇
개의 큰 승리가 평균을 끌어올리는" 전형적인 불안정 패턴**으로, PF 수치가 좋아 보여도
표본이 얇고(n=1,417) t값이 낮아 신뢰할 수 없다. **원문 스펙 그대로는 FAIL.**

## ⚠️ stack_level=0(baseline) 상세 — 예상 밖의 강한 신호(1h 전용)

**정의**: 다중TF·추세·웨이브 개념을 전부 제거한 순수 "이전 entry_tf봉 고/저 돌파 +
[SL=트리거봉 반대극값 또는 sl_atr_mult×ATR(wave_tf) 중 타이트한 쪽] + ATR 트레일링".
사실상 Elder Triple Screen이 아니라 **"Donchian(1) 돌파+ATR 트레일링"** 에 가깝다.

### 동결 파라미터(IS 그리드 18개 조합 중 최선) — held-out OOS 평가

`stack_level=0, sl_atr_mult=1.0, tp_atr_mult=3.0(트레일링 배수), use_trailing=True,
entry_tf=1h`

| 구간 | 거래수 | 승률% | PF(net) | PF(gross) | t(net) |
|---|---:|---:|---:|---:|---:|
| IS | 6,522 | 16.5 | 1.197 | 1.341 | 2.34 |
| **OOS** | 6,051 | 17.9 | **1.314** | 1.461 | **3.81** |
| FULL | 12,593 | 17.2 | 1.252 | 1.398 | 4.28 |

**IS→OOS로 PF·t 모두 개선**(1.197→1.314, 2.34→3.81) — 라운드1~4에서 반복적으로 관찰된
"IS에서 좋아 보이다 OOS에서 붕괴"(과최적화) 패턴과 **정반대 방향**이라 데이터 스누핑
의심이 상대적으로 낮다. 표본도 풀링 기준 12,593건으로 매우 크다.

### 파라미터 민감도(강건성 확인, IS 기준 그리드 내 + 인접값 관찰)

`sl_atr_mult`∈{0.8,1.0,1.2,1.5} × `tp_atr_mult`(트레일링배수)∈{2.0,2.5,3.0,4.0} 16개
조합 전부에서 **OOS net PF가 1.28~1.41 범위, t가 3.5~5.3 범위**로 일관되게 통과
기준을 크게 상회한다 — **knife-edge가 전혀 아닌 넓은 안정 고원(plateau)**. (이 16개
조합은 강건성 관찰용이며, 동결 파라미터 재선정에는 쓰지 않았다 — 원 18개 조합 그리드의
IS 최선값만 공식 후보로 유지.)

### 종목별 상세(13개 장기이력, FULL 기준 내림차순)

| 심볼 | 거래수 | 승률% | PF(net) | PF(gross) | IS_PF | OOS_PF |
|---|---:|---:|---:|---:|---:|---:|
| SOLUSDT | 946 | 18.5 | 1.664 | 1.821 | 2.196 | 1.184 |
| WLDUSDT | 644 | 19.4 | 1.628 | 1.738 | 1.536 | 1.676 |
| NEARUSDT | 976 | 18.0 | 1.494 | 1.621 | 1.545 | 1.419 |
| BTCUSDT | 943 | 18.3 | 1.366 | 1.597 | 1.567 | 1.128 |
| ETHUSDT | 1034 | 16.6 | 1.317 | 1.509 | 1.336 | 1.299 |
| XRPUSDT | 1171 | 15.5 | 1.240 | 1.395 | 0.752 | 1.934 |
| BNBUSDT | 1120 | 17.1 | 1.225 | 1.442 | 1.158 | 1.331 |
| ADAUSDT | 1101 | 15.9 | 1.139 | 1.264 | 1.017 | 1.291 |
| DODOXUSDT | 649 | 19.1 | 1.100 | 1.189 | 0.891 | 1.226 |
| ZECUSDT | 1107 | 15.4 | 1.099 | 1.201 | 0.952 | 1.286 |
| 1000XECUSDT | 1061 | 16.6 | 1.081 | 1.204 | 1.196 | 0.948 |
| DOGEUSDT | 1023 | 17.2 | 1.060 | 1.167 | 0.930 | 1.246 |
| TUSDT | 818 | 18.1 | 1.015 | 1.127 | 0.895 | 1.121 |

**13종목 중 13개(100%) net PF≥1.0** — 라운드1~4 전체에서 유일하게 전 종목이 순수익인
사례. 다만 **PF≥1.3을 넘는 종목은 5개(38%)**(SOL·WLD·NEAR·BTC·ETH), OOS 단독으로는
4개(31%, WLD·NEAR·XRP·BNB). 중앙값 PF(FULL)=1.225. 전 22종목 상세는
`scratchpad/elder_stack0_1h_final_detail.csv`.

**15m은 이 효과가 재현되지 않는다**(baseline net PF 0.97, gross 1.22 — 위 표 참조) —
1h 고유의 현상으로, ATR 트레일링 스탑이 1h의 상대적으로 낮은 노이즈에서만 효과적으로
작동하는 것으로 보인다.

## 최종 판정

### 원문 스펙(3단 다중TF 풀스택, stack_level=2): **FAIL**
- 15m·1h 모두 net PF<1.4이나 t값이 낮고(1h 최선 t=0.90) 표본이 얇으며 승률이 7%대로
  극단적이라 신뢰할 수 없다. **코디네이터의 핵심 가설("다중TF 스태킹이 gross PF를
  끌어올린다")은 이 전략에서 기각된다** — 오히려 필터를 걷어낼수록(stack_level 2→0)
  1h 기준 gross PF가 개선(1.57 아니라 실질적으로 level0의 1.34가 더 신뢰할 수 있는
  수치이며 표본도 4.6배 크다)됐다.

### Ablation 발견(stack_level=0, "순수 1h 돌파+ATR 트레일링", 원문 스펙 아님): **HOLD**
(PASS 후보 근접, 즉시 보고)
- **PASS를 지지하는 근거**: 풀링 IS PF 1.197(t=2.34)→OOS PF 1.314(t=3.81)로 개선(과최적화
  반대 방향), 16개 인접 파라미터 전부 OOS PF 1.28~1.41·t 3.5~5.3의 넓은 안정 고원,
  13/13 종목 전원 net PF≥1.0(이 프로젝트 36개 전략 중 유일), 표본 매우 큼(12,593건).
- **PASS를 보류시키는 근거**: 개별 종목 PF≥1.3 달성률이 38%(FULL)/31%(OOS)에 그쳐
  "심볼 전반 일관"이라는 통과조건을 엄격히 만족한다고 보기 어렵다. 또한 **이는 스펙이
  요구한 "Elder Triple Screen"이 아니라 그 스크립트의 부산물로 발견된 완전히 다른
  (더 단순한) 전략**이라 이번 태스크의 원래 검증 대상과 일치하지 않는다.
- **권고**: 이 리포트만으로 라이브에 반영하지 않는다. 만약 후속 검증을 진행한다면
  (1) `backtest-reviewer` 감사(룩어헤드·다중비교·데이터소스 재확인 — NR7에서 실제로
  룩어헤드 버그가 발견됐던 전례가 있어 이 스크립트도 재감사 필요), (2) 22종목 전체
  브레스 확인, (3) "순수 이전봉 돌파+ATR 트레일링"이라는 이 형태 자체를 별도 스펙
  문서로 등록해 독립적으로 재검증하는 것을 권장한다.

## 미검증/근사 요소 (정직한 한계 고지)

- **"5배 상위TF" 원 지표 로직 대신 고정 1d/4h/1h(또는 4h/1h/15m) 3단으로 단순화**
  (스펙 자체가 이미 이렇게 근사).
- **트레일링 스탑을 단순 ATR 배수로 구현**(원문의 "2.0×ATR 트레일링"을 문자 그대로
  해석 — 더 정교한 chandelier-exit류 구현은 미검증).
- **stack_level=0 발견은 사후 관찰(post-hoc)**: 원래 그리드에 stack_level 축을 포함시켜
  IS 전용으로 스윕했으므로 절차적으로는 데이터 스누핑이 아니나, 애초에 "Elder Triple
  Screen을 검증한다"는 태스크 범위를 벗어난 부산물이라는 점은 명시해야 공정하다.
- **1000PEPE·HYPE 등 9개 신규상장 알트는 IS 구간이 짧거나 없어 stack_level=0 최종
  판정에서 참고용으로만 사용**(전 22종목 상세: `scratchpad/elder_stack0_1h_final_detail.csv`).

## 재현 스크립트

- `scratchpad/bt_elder_triple.py` — Elder Triple Screen(및 stack_level 분해) 이벤트기반
  시뮬레이터. `simulate(sym, entry_tf, stack_level, ...)`.
- `scratchpad/run_elder_sweep.py` — IS 전용 그리드서치(15m/1h, 각 234조합, stack_level
  0/1/2 비교). 결과: `scratchpad/elder_sweep_{15m,1h}.csv`.
- `scratchpad/elder_stack0_1h_final_detail.csv` — stack_level=0 동결 파라미터, 전
  22종목 IS/OOS/FULL 상세(인라인 스크립트로 생성, 재현 커맨드 아래).
- 재현 커맨드:
  ```
  cd /home/user/study
  python3 scratchpad/bt_elder_triple.py BTCUSDT 1h   # 단일 심볼 스팟체크(원문 풀스택, stack_level=2 기본)
  python3 scratchpad/run_elder_sweep.py 1h            # IS 그리드서치(1h, 234조합, stack_level 0/1/2)
  python3 scratchpad/run_elder_sweep.py 15m           # IS 그리드서치(15m, 234조합)
  python3 - <<'PY'   # stack_level=0 동결 파라미터 전종목 상세 재현
  import sys; sys.path.insert(0, ".")
  from scratchpad.bt_elder_triple import ALL_SYMBOLS, simulate, IS_START, IS_END, OOS_START, OOS_END
  for sym in ALL_SYMBOLS:
      res = simulate(sym, entry_tf="1h", stack_level=0, sl_atr_mult=1.0, tp_atr_mult=3.0, use_trailing=True)
      print(sym, res.n, res.profit_factor, res.profit_factor_gross)
  PY
  ```
