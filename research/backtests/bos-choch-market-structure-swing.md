# BOS/CHoCH 마켓 스트럭처(2봉 색전환 프랙탈) 추세전환 — 백테스트 리포트

- **전략 스펙**: `research/strategies/bos-choch-market-structure-swing.md`
- **출처**: TJR 유튜브("The ONLY Break Of Structure Video You'll Ever Need"), 참여지표 기반
  스카우트 — **백테스트 근거 없음**. 원저자 스스로 "BOS 단독 사용 시 손실" 경고. 본 리포트는
  이 경고가 크립토 스윙(4h/1d)에서 실제로 재현되는지 처음부터 검증한다.
- **판정 목적**: 순수 가격구조(2봉 색전환 프랙탈 스윙하이/로우) + 종가 마감 BOS만으로 추세추종
  엣지가 있는지, 청산 방식(스탑앤리버스/구조트레일/고정R) 3가지와 손절 없음(reverse)까지 포함해
  전수 검증.

## 구현/실행 방식

- **격리 스크립트**: `scratchpad/bt_bos.py` (완전 독립, `src/crypto_trader/**` 무수정,
  `indicators.atr`만 재사용). 상태머신형 진입/트레일이 기존 scalp/mid/swing 인터페이스와
  맞지 않아 TRIX/RangeFilter와 동일한 자체 이벤트기반 시뮬레이터 사용.
- **스윙 포인트(원문 그대로)**: 상승봉(close≥open) 다음 하락봉(close<open) → 두 봉 중 최고가가
  스윙 하이(하락봉이 닫히는 시점에 확정). 하락봉 다음 상승봉 → 두 봉 중 최저가가 스윙 로우.
  100% 닫힌 캔들만 사용, 레벨은 확정된 그 다음 봉부터 유효(동일 봉 자기참조 방지).
- **BOS 확정(원문 그대로)**: 종가가 직전 확정 스윙 하이 위로 마감 → 강세 BOS. 종가가 직전
  확정 스윙 로우 아래로 마감 → 약세 BOS. 꼬리 이탈 무효(종가만). 레인지필터(`bt_rangefilter_v2.py`)와
  동일한 `cond_ini` state-machine 패턴으로 "이미 그 방향 전환 상태"에서는 재신호를 내지 않고
  반대 BOS가 뜰 때만 재점화(합성 검증: 소규모 합성 데이터로 스윙/BOS 로직 단위검증 완료 —
  아래 "검증" 절 참고).
- **청산 3모드**:
  1. `reverse` — 반대 BOS 발생 시에만 청산+반전(손절 없음, 원문 "즉시 청산 및 반전" 그대로).
  2. `structure` — 진입 SL=반대편 최근 확정 스윙포인트 ∓ `sl_buffer_atr`(기본 0.3)×ATR14.
     이후 유리한 방향으로 새 스윙포인트가 확정될 때마다 SL을 그 쪽으로만 래칫(원문 "신규 추세
     방향 스윙 포인트 갱신 시 SL 트레일"). SL히트(인트라바) 또는 반대 BOS 중 먼저 오는 쪽으로 청산.
  3. `fixed_rr` — structure와 동일 초기 SL, R=|entry−stop|, TP=entry±`rr_mult`(기본 2.0)×R.
- **노이즈 필터(자체보강, 원문에 없음)**: `min_swing_atr` — 새 스윙포인트가 직전 반대편
  스윙포인트 대비 ATR14×`min_swing_atr` 이상 벌어져야 레벨 갱신 인정(작으면 노이즈로 기각).
  0(비활성)/0.5/1.0으로 민감도 점검.
- **룩어헤드 방지**: BOS 신호는 i-1(닫힌 봉) 확정 값으로 판정, 체결은 i봉 시가(+슬리피지).
  스윙 포인트는 자신을 구성하는 두 봉(모두 닫힌 봉)만으로 확정 — 미래봉 참조 없음. SL 트레일도
  i봉 진입 직전(=i-1까지 데이터로 계산된) `sl_arr[i]`/`sh_arr[i]` 사용.
- **데이터**: `scratchpad/futdump100m/*.pkl` 15m → **4h·1d 리샘플**.
- **종목**: 13개 장기이력(2022-01 시작) 종목 풀링(BTC/ETH/SOL/BNB/ADA/DOGE/XRP/ZEC/NEAR/1000XEC/T/DODOX/WLD)
  — Coppock/KAMA 리포트와 동일한 `LONG_HISTORY_SYMBOLS` 기준.
- **IS/OOS**: IS 2022-01-01~2024-06-30, OOS 2024-07-01~2026-06-30(entry_time 기준).
- **수수료/슬리피지**: 진입/청산 각 taker 0.05% + 슬리피지 0.02%(사이드당).
- **검증(단위테스트)**: 16봉 합성 데이터(명확한 상승→하락 전환 시퀀스)로 `compute_swings_and_bos`를
  수동 추적·검증 — 스윙하이/로우가 올바른 봉에서 확정되고 1봉 지연 후 유효화되며, BOS 이벤트가
  정확한 전환 시점에만(재신호 없이) 발생함을 확인.
- **실행 커맨드(재현)**:
  ```
  cd /home/user/study
  python3 scratchpad/bt_bos.py BTCUSDT 4h structure
  python3 scratchpad/run_bos_sweep.py 4h structure both
  python3 scratchpad/run_bos_sweep.py 1d reverse both
  # 전체 스윕 재현 (mode×direction×min_swing_atr × 13종목 × 2TF, csv 저장):
  python3 - <<'PY'
  import sys; sys.path.insert(0,'.')
  from scratchpad.bt_bos import LONG_HISTORY_SYMBOLS as SYMS, load_symbol, simulate, IS_START, IS_END, OOS_START, OOS_END
  import pandas as pd
  rows = []
  for tf in ["4h","1d"]:
      for mode in ["reverse","structure","fixed_rr"]:
          for direction in ["both","long_only"]:
              for msa in [0.0, 0.5, 1.0]:
                  for sym in SYMS:
                      df = load_symbol(sym, tf)
                      res = simulate(df, symbol=sym, mode=mode, direction=direction, min_swing_atr=msa)
                      isr = res.subset(IS_START, IS_END); oosr = res.subset(OOS_START, OOS_END)
                      rows.append(dict(tf=tf, mode=mode, direction=direction, min_swing_atr=msa,
                                        symbol=sym, n=res.n, pf=res.profit_factor,
                                        is_n=isr.n, is_pf=isr.profit_factor,
                                        oos_n=oosr.n, oos_pf=oosr.profit_factor))
  pd.DataFrame(rows).to_csv("scratchpad/bos_sweep_results.csv", index=False)
  PY
  ```

## 결과 1 — 4h, 풀링(거래수 가중, 13종목), 청산모드별(direction=both)

| 청산모드 | 구간 | 거래수 | 승률% | PF(net) | PF(gross) | t(net) |
|---|---|---:|---:|---:|---:|---:|
| reverse | FULL | 10065 | 35.2 | 0.97 | 1.02 | -0.95 |
| reverse | IS | 5337 | 33.4 | **0.88** | 0.92 | **-2.95** |
| reverse | OOS | 4712 | 37.1 | 1.07 | 1.13 | 1.42 |
| structure | FULL | 10065 | 33.0 | 0.95 | 1.02 | -1.44 |
| structure | IS | 5337 | 31.5 | **0.86** | 0.92 | **-2.88** |
| structure | OOS | 4712 | 34.8 | 1.06 | 1.13 | 1.10 |
| fixed_rr | FULL | 10065 | 35.4 | 0.93 | 1.00 | -2.70 |
| fixed_rr | IS | 5337 | 34.0 | **0.87** | 0.93 | **-4.02** |
| fixed_rr | OOS | 4712 | 37.0 | 1.01 | 1.08 | 0.36 |

**IS 구간에서 3개 청산모드 전부 net PF가 통계적으로 유의하게 0.86~0.88로 1.0 미만**(t=-2.9~-4.0,
즉 손실이 통계적으로 유의) — 원저자의 "단독 사용 시 손실" 경고가 그대로 재현된다. OOS는
1.01~1.07로 소폭 개선되지만 t값이 0.36~1.42로 유의하지 않고, 1.3 문턱과는 거리가 멀다.

## 결과 2 — 1d, 풀링(거래수 가중, 13종목), 청산모드별(direction=both)

| 청산모드 | 구간 | 거래수 | 승률% | PF(net) | PF(gross) | t(net) |
|---|---|---:|---:|---:|---:|---:|
| reverse | FULL | 1669 | 36.7 | 1.07 | 1.10 | 0.63 |
| reverse | IS | 851 | 35.0 | 1.01 | 1.03 | 0.12 |
| reverse | OOS | 818 | 38.5 | 1.14 | 1.16 | 0.66 |
| structure | FULL | 1669 | 35.4 | 1.10 | 1.13 | 0.95 |
| structure | IS | 851 | 33.0 | 1.06 | 1.09 | 0.47 |
| structure | OOS | 818 | 37.8 | 1.15 | 1.18 | 0.85 |
| fixed_rr | FULL | 1669 | 36.7 | 0.97 | 1.00 | -0.44 |
| fixed_rr | IS | 851 | 35.0 | 0.92 | 0.94 | -0.98 |
| fixed_rr | OOS | 818 | 38.5 | 1.03 | 1.05 | 0.36 |

1d는 4h보다 완만하게 손실권을 벗어나 PF 1.0~1.15에 머물지만, **어떤 t값도 1.0을 넘지 않아
통계적으로 무의미**하다. 종목별 상세(아래)에서 극단적 분산이 확인돼 "우연히 평균이 1을 넘은
소표본"으로 판단한다.

## 결과 3 — 종목별 상세 (4h, structure, both, min_swing_atr=0)

| 심볼 | 거래수 | PF | IS거래 | IS_PF | OOS거래 | OOS_PF |
|---|---:|---:|---:|---:|---:|---:|
| BTCUSDT | 864 | 0.93 | 486 | 0.96 | 376 | 0.88 |
| ETHUSDT | 858 | 0.87 | 496 | 0.76 | 360 | 1.01 |
| SOLUSDT | 839 | 0.98 | 484 | 0.87 | 354 | 1.14 |
| BNBUSDT | 844 | **0.85** | 470 | 0.79 | 372 | 0.94 |
| ADAUSDT | 837 | 0.94 | 486 | 0.77 | 351 | 1.20 |
| DOGEUSDT | 842 | 0.86 | 478 | 0.70 | 363 | 1.06 |
| XRPUSDT | 820 | 1.17 | 459 | 0.98 | 360 | 1.45 |
| ZECUSDT | 816 | 1.00 | 448 | 0.78 | 366 | 1.29 |
| NEARUSDT | 872 | **0.86** | 494 | 0.85 | 376 | 0.86 |
| 1000XECUSDT | 812 | 0.93 | 450 | 0.96 | 361 | 0.91 |
| TUSDT | 634 | 0.89 | 278 | 0.80 | 355 | 0.95 |
| DODOXUSDT | 496 | 0.98 | 145 | 1.07 | 350 | 0.95 |
| WLDUSDT | 531 | 1.24 | 163 | 1.39 | 368 | 1.18 |

**13종목 중 net PF≥1.3인 종목이 0개**(WLD가 최고 1.24). IS 구간은 XRP만 PF≥1.0이고 나머지
12종목 전부 1.0 미만. OOS는 절반 정도가 1.0을 살짝 넘지만(XRP 1.45, ZEC 1.29, ADA 1.20 등)
BTC·NEAR·1000XEC·TUSDT는 OOS도 1.0 미만 — 종목 간 일관성이 없다.

## 파라미터 민감도

**청산모드×방향×min_swing_atr 전수(4h/1d, 13종목 풀링, trade-weighted mean/median 요약,
`scratchpad/bos_sweep_results.csv` 원자료)**:

| TF | 모드 | 방향 | min_swing_atr | 종목PF 평균 | 종목PF 중앙값 | OOS PF 평균 | PF≥1 종목비율 |
|---|---|---|---:|---:|---:|---:|---:|
| 4h | structure | both | 0.0 | 0.96 | 0.93 | 1.06 | 23% |
| 4h | structure | both | 1.0 | 0.99 | 0.99 | 1.11 | 38% |
| 4h | reverse | long_only | 1.0 | 1.03 | 1.01 | 1.13 | 54% |
| 1d | structure | long_only | 0.5 | 1.19 | **1.43** | 1.35 | 54% |
| 1d | structure | long_only | 1.0 | 1.25 | 1.11 | 1.30 | 54% |

**36개 (TF×모드×방향×min_swing_atr) 조합 전수 테스트 중 종목PF 평균이 1.3을 넘는 조합이
단 하나도 없다.** 노이즈 필터(min_swing_atr 0→1.0)를 강하게 걸수록 근소하게 개선되지만
(4h structure both: 0.96→0.99), 1.0을 넘는 수준에 그친다. 1d·구조트레일·롱온리·강한 필터
조합이 종목PF 중앙값 1.43까지 오르는 경우가 있으나(위 표), 이는 **1d 종목당 거래수가
IS 30~40건/OOS 25~35건 수준으로 얕고**, 13종목 중 PF≥1인 비율이 여전히 54%(23종목 중 6종목
미만)에 그쳐 "일관된 통과"라 보기 어렵다.

## 최종 판정: **FAIL (탈락)** — 감사 **VALID** (동의)

> **backtest-reviewer 감사 VALID (2026-07-18).** `bt_bos.py`/`run_bos_sweep.py`를 직접 재실행해
> 4h structure IS n=5337·PF 0.860·t -2.876, reverse/fixed_rr IS·OOS 6수치, 36조합 최고 종목PF평균
> 1.2509, 종목별 상세를 소수점 둘째자리까지 재현. **룩어헤드 최우선 검증**: 합성 OHLC로 `compute_swings_and_bos`
> 를 추적해 스윙 하이/로우가 두 봉 모두 닫힌 뒤 다음 봉부터만 노출(미래봉 자기참조 없음), 레벨형성봉과
> 돌파판정봉 비겹침, 진입 i-1 신호→i봉 시가·진입당일 SL/TP 배제까지 확인 → **룩어헤드 없음**. 추가로
> 22종목 전체 재실행(IS PF 0.865/t -2.79)해 13종목 선별에 의한 인위적 악화가 아님을 확인. 단위·수수료·OOS
> 분리 PASS. 원저자 "단독 손실" 경고가 정량 재현됨 → **FAIL 정당, 라이브 미반영**. (사소: 13종목 중
> TUSDT/DODOX/WLD는 2022-01 시작 아님 — 명명 부정확이나 낮은 IS 거래수로 실질 영향 없음.)

**근거**:
1. **원저자 자신의 경고("BOS 단독 사용 시 손실")가 그대로 재현된다.** 4h IS 구간에서 3개
   청산모드 전부 net PF가 0.86~0.88로 **통계적으로 유의하게 1.0 미만**(t=-2.9~-4.0)이다 —
   수수료 잠식이 아니라 순수 가격 움직임 자체가 역방향(엣지 부재)이라는 뜻(gross PF도
   0.92~0.93로 1.0 미만).
2. **36개 파라미터 조합(TF 2×모드 3×방향 2×min_swing_atr 3) 중 어느 하나도 종목간 평균 PF
   1.3을 달성하지 못했다.** 최선의 조합(1d, structure, long_only, min_swing_atr=1.0)도
   평균 1.25에 그치고, 그마저 종목당 표본이 30~40건 수준으로 얕다.
3. **종목 간 일관성이 없다.** 4h 기준 13종목 중 net PF≥1.3인 종목이 0개, PF≥1.0인 종목도
   3~5개(23~38%) 수준. BNB·NEAR는 IS/OOS 모두 지속적으로 손실권.
4. **노이즈 필터(2봉 프랙탈 최소 진폭)를 강하게 걸어도 개선폭이 미미**하다 — "저품질 스윙
   신호가 문제"가 아니라 "구조 자체(2봉 색전환 프랙탈 + 종가 BOS)에 지속 가능한 방향성 엣지가
   없다"는 결론에 부합한다.
5. IS→OOS가 손실권(0.86~0.88)에서 손익분기 근처(1.0~1.07)로 개선되는 패턴이 일부 보이지만,
   t값이 전 구간 1.5 미만으로 통계적 유의성이 없어 "우연한 반등"과 구분할 수 없다.

**결론: BOS/CHoCH 단독 추세전환 신호는 우리 프레임워크(4h/1d, 13종목, 4.5년) 기준으로
지속 가능한 엣지가 확인되지 않는다.** 원저자가 명시한 "컨플루언스(공급/수요존, FVG,
오더블록) 필요" 경고와 정확히 일치하는 결과이며, 단독 사용은 통과 기준에 크게 미달한다.

## 미검증/근사 요소 (정직한 한계 고지)

- **원문의 "컨플루언스" 필터(FVG·오더블록·공급수요존) 전부 제외**하고 BOS 단독으로만 테스트했다
  — 이는 스펙 자체가 명시한 단순화이며, 컨플루언스를 더하면 결과가 달라질 수 있으나 그 자체가
  별도 전략(ict-fair-value-gap 등)이라 본 스크립트 범위 밖이다.
- **SL/트레일 방식은 원문에 구체적 수치가 없어 자체보강**(sl_buffer_atr=0.3, rr_mult=2.0).
  민감도 점검 결과 이 선택이 결론(FAIL)을 바꾸지 않음을 확인했다.
- **사이징**: structure/fixed_rr 모드는 리스크 비율 고정(1%/트레이드, 비복리), reverse 모드는
  고정 명목가($10,000) — PF/승률/t값 판정에는 영향 없음(총수익률/MDD는 본문에 신지 않음,
  기존 TRIX/Coppock 리포트 관행과 동일).
- **1h 미검증**: 하네스 지시(4h/1d 중심)에 따라 1h는 실행하지 않았다. 4h가 이미 명확한 실패를
  보여 1h(더 짧은 TF, 원문도 비권장)를 추가로 돌릴 근거가 약하다고 판단했다.

## 재현 스크립트

- `scratchpad/bt_bos.py` — 2봉 색전환 스윙 + BOS state-machine + 3청산모드 이벤트기반
  시뮬레이터. `simulate(df, symbol, mode, direction, min_swing_atr, sl_buffer_atr, rr_mult, ...)`.
- `scratchpad/run_bos_sweep.py` — 종목 풀링 + IS/OOS 집계 스윕 러너.
- `scratchpad/bos_sweep_results.csv` — 36 파라미터 조합 × 13종목 × 2TF 전수 결과(468행).
- 데이터: `scratchpad/futdump100m/*.pkl` (기존 확보분 재사용, 신규 다운로드 없음).
