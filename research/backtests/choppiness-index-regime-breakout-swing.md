# 초퍼니스 인덱스(CHOP) 레짐필터 레인지 브레이크아웃 — 백테스트 리포트

- **전략 스펙**: `research/strategies/choppiness-index-regime-breakout-swing.md`
- **출처**: 지표 원안 Bill Dreiss(1994), TradingView 빌트인 CHOP + "MM Chop Filter" 스크립트
  참여지표 — **백테스트 근거 없음**(quantifiedstrategies.com 원문은 봇 차단으로 미확인, 인용
  안 함). 임계값(38.2/61.8)은 지표 표준 관례일 뿐 성과 수치가 아니다.
- **판정 목적**: CHOP 레짐필터(압축→해소) + 레인지 브레이크아웃 + 거래량 필터 조합이 크립토
  4h/1d에서 지속 가능한 엣지를 만드는지 처음부터 검증.

## 구현/실행 방식

- **격리 스크립트**: `scratchpad/bt_chop.py` (완전 독립, `src/crypto_trader/**` 무수정,
  `indicators.true_range/atr/adx` 재사용, CHOP 자체는 표준식이 `indicators.py`에 없어 이
  파일 안에서 순수함수로 추가). SL/TP/시간청산/CHOP재상승청산 상태를 갖는 상태머신형 진입/
  청산이 기존 인터페이스와 맞지 않아 TRIX/RangeFilter와 동일한 자체 이벤트기반 시뮬레이터 사용.
- **CHOP(표준식, n=14)**: `CHOP = 100*log10(SUM(TR,n) / (MAX(High,n)-MIN(Low,n))) / log10(n)`.
- **레짐 전환(원문 그대로)**: CHOP이 `chop_high`(61.8) 이상을 찍은 뒤(압축 플래그 on),
  `chop_low`(38.2) 아래로 처음 내려오는 순간 "압축 해소" 트리거. 트리거 시점에 직전
  `range_lookback`(기본 20)봉 고점/저점을 압축구간 레인지로 고정.
- **진입(원문 그대로)**: 트리거 후 `lookforward_bars`(기본 20봉) 이내에 종가가 고정 레인지
  상단 상향 돌파 + 거래량≥20MA×`vol_mult`(1.5) → 롱(하단 하향 돌파 → 숏). 트리거당 최초 1회만
  발동(원샷 윈도). (선택) ADX(14)≥`adx_min` 필터.
- **청산(원문을 사건기반 시뮬레이터 구조에 맞게 단순화 — 분할청산/트레일을 전량청산으로 근사,
  KAMA/TRIX 스크립트와 동일 관행)**: SL=반대편 레인지 경계∓`sl_buffer_atr`(0.1)×ATR14,
  TP=레인지폭×`tp_mult`(1.25) measured move, CHOP 재상승(≥61.8) 청산, `time_exit_bars`(20)
  초과 보유 시 시간청산. SL→TP→CHOP재상승/시간청산 순으로 체크.
- **룩어헤드 방지**: 레짐/레인지/거래량/ADX 신호는 전부 "닫힌 봉 i까지" 데이터로만 인과적
  계산(`compute_chop_signals`). 실제 진입/청산은 신호봉 i-1(닫힌 봉) 값을 쓰고 체결은 i봉
  시가(+슬리피지) — 기존 관행과 동일한 1봉 지연 체결.
- **데이터**: `scratchpad/futdump100m/*.pkl` 15m → **4h·1d 리샘플**.
- **종목**: 13개 장기이력(2022-01 시작) 종목 풀링을 주 판정 근거, 22종목 전체는 참고용
  (신규상장 알트는 IS 구간 자체가 없어 별도 표기).
- **IS/OOS**: IS 2022-01-01~2024-06-30, OOS 2024-07-01~2026-06-30(entry_time 기준).
- **수수료/슬리피지**: 진입/청산 각 taker 0.05% + 슬리피지 0.02%(사이드당).
- **실행 커맨드(재현)**:
  ```
  cd /home/user/study
  python3 scratchpad/bt_chop.py BTCUSDT 4h
  python3 scratchpad/run_chop_sweep.py 4h both
  python3 scratchpad/run_chop_sweep.py 4h long_only
  # 파라미터 스윕(csv 저장):
  python3 - <<'PY'
  import sys; sys.path.insert(0,'.')
  from scratchpad.bt_chop import LONG_HISTORY_SYMBOLS as SYMS, load_symbol, simulate, IS_START, IS_END, OOS_START, OOS_END
  import pandas as pd
  configs = [dict(), dict(vol_mult=1.2), dict(vol_mult=2.0), dict(range_lookback=30),
             dict(range_lookback=15), dict(tp_mult=1.0), dict(tp_mult=1.5), dict(adx_min=20),
             dict(sl_buffer_atr=0.3), dict(lookforward_bars=10), dict(lookforward_bars=30)]
  rows = []
  for tf in ["4h","1d"]:
      for direction in ["both","long_only"]:
          for cfg in configs:
              for sym in SYMS:
                  df = load_symbol(sym, tf)
                  res = simulate(df, symbol=sym, direction=direction, **cfg)
                  isr = res.subset(IS_START, IS_END); oosr = res.subset(OOS_START, OOS_END)
                  rows.append(dict(tf=tf, direction=direction, cfg=str(cfg), symbol=sym,
                                    n=res.n, pf=res.profit_factor, is_n=isr.n, is_pf=isr.profit_factor,
                                    oos_n=oosr.n, oos_pf=oosr.profit_factor))
  pd.DataFrame(rows).to_csv("scratchpad/chop_sweep_results.csv", index=False)
  PY
  ```

## 결과 1 — 4h, 풀링(거래수 가중), 기본파라미터

| 방향 | 종목풀 | 구간 | 거래수 | 승률% | PF(net) | PF(gross) | t(net) |
|---|---|---|---:|---:|---:|---:|---:|
| 롱숏 | 22종목 | FULL | 1002 | 45.7 | 1.14 | 1.19 | 1.60 |
| 롱숏 | 22종목 | IS | 438 | 46.1 | **1.35** | 1.40 | **2.35** |
| 롱숏 | 22종목 | OOS | 564 | 45.4 | **1.00** | 1.04 | **0.002** |
| 롱숏 | 13종목(장기) | FULL | 866 | 45.3 | 1.06 | 1.10 | 0.64 |
| 롱숏 | 13종목(장기) | IS | 417 | 46.3 | 1.32 | 1.37 | 2.12 |
| 롱숏 | 13종목(장기) | OOS | 449 | 44.3 | **0.86** | 0.89 | -1.24 |
| 롱온리 | 13종목(장기) | FULL | 453 | 45.5 | 1.24 | 1.29 | 1.73 |
| 롱온리 | 13종목(장기) | IS | 225 | 46.7 | **1.47** | 1.53 | **2.14** |
| 롱온리 | 13종목(장기) | OOS | 228 | 44.3 | **1.06** | 1.10 | 0.32 |

**핵심 패턴**: IS 구간에서는 방향/종목풀 조합 전부에서 net PF가 1.32~1.47로 통계적으로
유의한(t=2.1~2.4) 양의 엣지처럼 보인다. 그러나 **OOS로 넘어가면 예외 없이 PF가 0.86~1.06으로
붕괴하고 t값이 전부 1.3 미만(사실상 무의미)으로 떨어진다.** 22종목 롱숏 OOS는 t=0.002로
완전히 무작위와 구분 불가능한 수준이다.

## 결과 2 — 1d, 풀링(13종목) — 표본 주의

| 방향 | 구간 | 거래수 | 승률% | PF(net) | t(net) |
|---|---|---:|---:|---:|---:|
| 롱숏 | FULL | 129 | 47.3 | 1.37 | 1.36 |
| 롱숏 | IS | 63 | 47.6 | 1.60 | 1.41 |
| 롱숏 | OOS | 66 | 47.0 | 1.17 | 0.48 |

1d는 종목당 거래수가 IS 2~8건, OOS 2~8건 수준(**개별 종목 판정 불가, 과제 기준 n≥20 미달**)
이라 종목별 상세는 참고 이하로만 취급한다. 풀링 자체도 129건으로 얕고, IS/OOS 모두 t<1.5로
유의하지 않다. 판정 근거로 채택하지 않는다.

## 결과 3 — 4h 롱온리 기본파라미터, 종목별 상세(13종목)

| 심볼 | 거래수 | PF | IS거래 | IS_PF | OOS거래 | OOS_PF |
|---|---:|---:|---:|---:|---:|---:|
| BTCUSDT | 47 | 1.92 | 28 | 2.12 | 19 | 1.65 |
| ETHUSDT | 40 | 1.52 | 23 | 2.04 | 17 | 1.10 |
| SOLUSDT | 46 | 1.30 | 22 | 1.90 | 24 | 0.84 |
| BNBUSDT | 39 | 1.59 | 22 | **3.31** | 17 | **0.64** |
| ADAUSDT | 34 | **0.63** | 18 | 0.77 | 16 | **0.52** |
| DOGEUSDT | 39 | 2.10 | 17 | 4.70 | 22 | 1.35 |
| XRPUSDT | 32 | 1.18 | 16 | 0.93 | 16 | 1.40 |
| ZECUSDT | 41 | **0.84** | 15 | 1.37 | 26 | **0.71** |
| NEARUSDT | 45 | 1.15 | 24 | 0.92 | 21 | 1.47 |
| 1000XECUSDT | 21 | 1.28 | 15 | 0.89 | 6 | 7.37 |
| TUSDT | 25 | **0.85** | 11 | 0.50 | 14 | 1.19 |
| DODOXUSDT | 23 | **0.70** | 6 | 1.85 | 17 | **0.52** |
| WLDUSDT | 21 | 1.50 | 8 | 1.18 | 13 | 1.76 |

BNB(IS 3.31→OOS 0.64), ADA(IS 0.77→OOS 0.52, 지속 부진), DODOX(IS 1.85→OOS 0.52)처럼
IS/OOS가 극단적으로 뒤집히거나 지속 부진한 종목이 다수다. BTC·DOGE·WLD 정도만 IS/OOS
둘 다 양호하다 — **13종목 중 3종목만 일관된 강세, 나머지는 IS 착시이거나 지속 부진**.

## 파라미터 민감도 (4h, 롱온리, 13종목 풀링, trade-weighted pooled)

| 파라미터 변경 | FULL n | FULL PF | IS PF(t) | OOS PF(t) |
|---|---:|---:|---:|---:|
| 기본(vol_mult=1.5, lookback=20, tp=1.25, lookfwd=20) | 453 | 1.24 | 1.47(2.14) | 1.06(0.32) |
| vol_mult=1.2 | 509 | 1.22 | 1.47(2.27) | 1.04(0.22) |
| vol_mult=2.0 | 366 | 1.30 | 1.53(2.24) | 1.10(0.49) |
| range_lookback=30 | 430 | **1.35** | 1.66(**2.70**) | 1.11(0.59) |
| range_lookback=15 | 459 | 1.17 | 1.37(1.78) | 1.01(0.09) |
| tp_mult=1.0 | 454 | 1.15 | 1.35(1.73) | 1.00(-0.01) |
| tp_mult=1.5 | 453 | 1.27 | 1.50(2.17) | 1.09(0.50) |
| adx_min=20 | 434 | 1.24 | 1.45(2.05) | 1.06(0.35) |
| sl_buffer_atr=0.3 | 453 | 1.24 | 1.45(2.07) | 1.06(0.36) |
| lookforward_bars=10 | 345 | 1.28 | 1.48(1.88) | **1.13(0.63)** |
| lookforward_bars=30 | 511 | 1.23 | 1.41(2.04) | 1.09(0.52) |

**11개 파라미터 조합(기본 포함) 중 OOS pooled PF가 1.15를 넘는 조합이 하나도 없고, OOS t값이
1.0을 넘는 조합도 하나도 없다.** IS PF는 파라미터를 흔들어도 1.35~1.66 범위에서 견고하게
유의(t 1.7~2.7)하지만, 이 견고함이 오히려 **"IS 구간(2022-2024 하락장 저점~2023-24 알트
랠리) 특유의 변동성 레짐에 과최적화됐다"는 신호**로 해석된다 — 파라미터에 강건한 IS 신호가
OOS로 넘어가면 예외 없이 무너지는 패턴은, 파라미터 그리드서치 편의가 아니라 **IS 기간 자체의
시장 국면 의존성**을 시사한다(range_lookback=30이 IS t=2.70으로 가장 강해 보이지만 OOS는
여전히 0.59로 무의미).

## 최종 판정: **FAIL (탈락)** — 감사 **VALID** (동의)

> **backtest-reviewer 감사 VALID (2026-07-18).** `bt_chop.py`/`run_chop_sweep.py`를 직접 재실행해
> 4h 22종목 롱숏 IS n=438·PF 1.352·t 2.354 → OOS n=564·PF 1.0003·t 0.00227(무작위 수준), 13종목
> 롱온리·1d, 파라미터 민감도 2변형, BTC 종목상세를 소수점 둘째자리까지 재현. CHOP 산식(100·log10(ΣTR14/
> range)/log10(14))·레짐임계(61.8/38.2) 표준 일치, 룩어헤드 없음(레인지락이 트리거봉 자기참조 진입을
> 원천 차단하는 구조 확인), 단위·수수료·OOS 분리 PASS. **"IS 유의→OOS 붕괴, 11변형 전부 동일"은
> 전형적 과최적화 서명**으로 FAIL 정당 → **라이브 미반영**.

**근거**:
1. **IS→OOS 붕괴 패턴이 방향(롱숏/롱온리)·종목풀(22/13종목)·파라미터(11개 변형) 전부에서
   예외 없이 재현된다.** IS net PF 1.32~1.66(t=2.0~2.7, 통계적으로 유의)이 OOS에서 항상
   0.86~1.13(t=-1.24~0.63, 전부 통계적으로 무의미)으로 무너진다. 어떤 조합도 OOS pooled
   PF가 1.3 근처에도 못 미친다.
2. **22종목 전체 롱숏 OOS는 t=0.002로 완전한 무작위(동전던지기)와 구분 불가능**하다 —
   가장 넓은 표본(564건)에서 나온 결과라 신뢰도가 가장 높은데도 엣지가 전혀 없다.
3. **종목 간 일관성이 없다.** 13종목 중 IS/OOS 둘 다 견실한 종목은 BTC·DOGE·WLD 정도(3종목,
   23%)뿐이고, BNB·DODOX는 IS에서 3배 넘는 PF를 보이다 OOS에서 0.5~0.6대로 붕괴, ADA는
   IS/OOS 둘 다 지속 부진(0.5~0.8) — "소수 대박 종목이 평균을 끌어올리는" 전형적 과최적화
   징후다.
4. **1d는 표본 자체가 판정 불가 수준**(종목당 IS/OOS 각 2~8건)이라 근거로 채택하지 않는다.
5. **CHOP 레짐필터가 실제로 "압축→추세 시작"을 조기 포착하지 못하고, 이미 상당 부분
   진행된 뒤늦은 후행신호로 작동하는 것으로 추정**된다(스카우트 메모의 우려 "CHOP은
   후행지표라 돌파 초입을 놓칠 수 있음"과 일치) — IS 특정 국면(2022 하락 후 2023-24 반등)
   에서만 우연히 타이밍이 맞았을 가능성이 높다.

**결론: CHOP 레짐필터+레인지 브레이크아웃은 IS 구간에서 통계적으로 유의한 겉보기 엣지를
보이지만, 이는 표본외에서 재현되지 않는 국면 의존적 결과로 판단된다.** "좋아 보여도
표본외에서 무너지면 그대로 보고하라"는 원칙에 따라 PASS/HOLD가 아닌 FAIL로 판정한다.

## 미검증/근사 요소 (정직한 한계 고지)

- **청산 로직 단순화**: 원문의 분할청산(TP 미달성시 절반청산+트레일, CHOP 재상승시
  "분할"청산)을 사건기반 시뮬레이터 구조상 전량청산으로 근사했다. 분할청산을 정교하게
  구현하면 결과가 다소 달라질 수 있으나, IS/OOS 붕괴 패턴의 근본 원인(레짐 판정 자체의
  국면의존성)을 바꿀 가능성은 낮다고 판단한다.
- **레인지 정의**: "직전 압축 구간 고점/저점"을 트리거 시점의 `range_lookback`봉 롤링
  고저로 근사했다(원문에 정확한 구간 경계 정의 없음).
- **원문 "4h 레짐/1h 진입" 멀티TF 조합은 실행하지 않았다** — 하네스 지시(4h/1d 중심,
  1h는 참고)에 따라 단일TF(4h/1d 모두에서 레짐판정+진입 수행) 버전만 검증했다. 이미 4h
  단일TF에서 명확한 IS/OOS 붕괴가 확인돼, 멀티TF로 신호를 더 지연시키는 조합이 이 결론을
  바꿀 근거는 약하다고 판단했다(다만 완전히 배제하지는 않음 — 필요시 향후 재검증 후보).
- **사이징**: 리스크 비율 고정(1%/트레이드, 비복리) — PF/승률/t값 판정에는 영향 없음.

## 재현 스크립트

- `scratchpad/bt_chop.py` — CHOP 산식 + 레짐전환 + 레인지 브레이크아웃 + SL/TP/CHOP재상승/
  시간청산 이벤트기반 시뮬레이터. `simulate(df, symbol, direction, chop_period, chop_high,
  chop_low, range_lookback, lookforward_bars, vol_mult, adx_min, sl_buffer_atr, tp_mult,
  time_exit_bars, ...)`.
- `scratchpad/run_chop_sweep.py` — 종목 풀링 + IS/OOS 집계 스윕 러너.
- `scratchpad/chop_sweep_results.csv` — 11파라미터 변형 × 13종목 × 2TF × 2방향 전수 결과(572행).
- 데이터: `scratchpad/futdump100m/*.pkl` (기존 확보분 재사용, 신규 다운로드 없음).
