# TTM 스퀴즈(볼린저×켈트너 압축 해제) 모멘텀 브레이크아웃 — 백테스트 리포트

- **전략 스펙**: `research/strategies/ttm-squeeze-momentum-breakout-swing.md`
- **출처**: LazyBear "Squeeze Momentum Indicator"(TradingView 조회 297만, 역대 최다 사용 지표
  중 하나). 크립토 정량 백테스트 수치는 출처마다 불명확·비공개(BitMEX MaxDD≈12%만 확인 가능,
  PF/승률/표본수 미기재) → **직접 재검증이 목적**.
- **라운드**: 2 (라운드1 ORB/VWAP reclaim/Keltner와 동일 프로토콜·하네스·비용모델 재사용).
- **판정 목적**: 볼린저×켈트너 이중 밴드 압축 해제 + 선형회귀 모멘텀 가속 신호가 15m·1h
  크립토에서 수수료를 이기는 엣지가 있는지 확인.

## 구현/실행 방식

- **격리 스크립트**: `scratchpad/bt_ttm_squeeze.py` (완전 독립, `src/crypto_trader/**` 무수정,
  `indicators.bollinger_bands`/`atr`/`ema` 재사용). 라운드1 이벤트기반 하네스(`bt_orb.py` 등)
  계승.
- **볼린저밴드**: `bollinger_bands(close, bb_period, bb_mult)`. **켈트너채널**: basis=
  SMA(close,kc_period), range=**ATR(kc_period)(Wilder, 저장소 표준)** × kc_mult.
  [⚠️ 원문 LazyBear는 range를 SMA(TrueRange)로 계산하나 여기선 저장소 표준 Wilder ATR로
  근사했다 — 정직한 단순화, 두 값은 유사하지만 완전히 동일하지 않음.]
- **스퀴즈 ON**: BB가 KC 안에 완전히 위치(upper_bb<upper_kc and lower_bb>lower_kc).
- **모멘텀**: donchian_mid=(momentum_lookback봉 최고가+최저가)/2, avg=(donchian_mid+
  SMA(close,momentum_lookback))/2, source=close-avg, momentum=TradingView `ta.linreg`와 동일한
  **rolling 최소자승 회귀선의 마지막 시점 값**(`sliding_window_view`+행렬곱으로 벡터화).
- **트리거(신호봉 i-1)**: 스퀴즈가 squeeze_min_bars봉 이상 연속 ON이었다가 해제되는 첫 봉 +
  모멘텀이 0 위이고 직전봉보다 큼(가속) → 롱. 대칭 숏. 체결은 다음 봉(i) 시가(+슬리피지).
- **청산**: `exit_mode`='sign_flip'(모멘텀 부호 반전 시 전량청산, 스펙의 "완전 반전") 또는
  'decel'(최초 감속 시 전량청산 — 스펙의 "색 반전 부분청산"을 파샬 없이 전량청산으로 단순화,
  Simplicity). SL=진입가∓sl_atr_mult×ATR(kc_period). 시간청산(chop_exit_bars): 진입 후 그
  봉수 안에 포지션 방향 "가속"이 한 번도 관측되지 않으면 강제청산(스펙의 "10봉 내 가속 없으면
  횡보전환 청산" 그대로).
- **룩어헤드 방지**: 신호는 i-1(닫힌 봉) 확정, 체결은 i봉 시가. 모멘텀/스퀴즈 모두 신호봉까지의
  닫힌 데이터만 사용.
- **데이터/종목/IS·OOS/수수료**: 라운드1과 동일(`scratchpad/futdump100m`, 13종목 장기이력
  풀링 주 판정, 22종목 참고, IS 2022-01~2024-06/OOS 2024-07~2026-06, taker 0.05%+슬리피지
  0.02% 사이드당, net/gross PF 병기).
- **4h 확인 필터(스펙의 htf_confirm 옵션)는 미검증**(시간 예산상 제외, 아래 한계 고지 참조).

## IS 그리드서치 (파라미터 선택 — OOS 미접촉)

`kc_mult`∈{1.0,1.5,2.0} × `squeeze_min_bars`∈{2,3,6} × `momentum_lookback`∈{14,20,26} ×
`sl_atr_mult`∈{1.0,1.5,2.5} × `exit_mode`∈{sign_flip,decel} × `chop_exit_bars`∈{10,20} =
**324개 조합**(15m·1h 각각), 13종목 풀링.

**15m**:

| 순위 | kc_mult | sq_min | mom_lb | sl_mult | exit | chop | 거래수 | PF(net) | PF(gross) | t |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1(IS 최선) | 2.0 | 3 | 26 | 2.5 | sign_flip | 10 | 18,681 | **0.758** | 0.899 | -12.50 |

**324개 조합 전체에서 net PF 최댓값이 0.758** — 15m은 압도적으로 기각.

**1h**:

| 순위 | kc_mult | sq_min | mom_lb | sl_mult | exit | chop | 거래수 | PF(net) | PF(gross) | t |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 1(IS 최선) | 1.0 | 3 | 26 | 1.0 | sign_flip | 10 | 1,604 | **1.013** | 1.166 | 0.14 |

1h가 15m보다 낫지만(324개 조합 중 최댓값이 겨우 net PF 1.013, t=0.14로 완전히 무의미)
통과 기준과 거리가 멀다. `exit_mode='decel'`(감속 즉시 청산) 변형은 상위권에 전혀 등장하지
않아 — 원문이 강조한 "색 반전 조기 부분청산" 아이디어가 오히려 수익을 일찍 자르는 역효과임을
시사한다.

**다중비교 고지**: TTM은 15m 324 + 1h 324 = **총 648개 조합**을 IS로 탐색했다.

## 최종 채택(그래도 통과 기준 미달) 파라미터 — held-out OOS 평가

**15m**: `kc_mult=2.0, squeeze_min_bars=3, momentum_lookback=26, sl_atr_mult=2.5,
exit_mode=sign_flip, chop_exit_bars=10`
**1h**: `kc_mult=1.0, squeeze_min_bars=3, momentum_lookback=26, sl_atr_mult=1.0,
exit_mode=sign_flip, chop_exit_bars=10`

### 풀링(13종목) IS/OOS/FULL

| TF | 구간 | 거래수 | 승률% | PF(net) | PF(gross) | t(net) |
|---|---|---:|---:|---:|---:|---:|
| 15m | IS | 18,681 | 30.1 | 0.758 | 0.899 | -12.50 |
| 15m | OOS | 17,273 | 32.1 | 0.839 | 0.983 | -7.79 |
| 15m | FULL | 35,996 | 31.1 | 0.797 | 0.940 | -14.36 |
| 1h | IS | 1,604 | 21.1 | 1.013 | 1.166 | 0.14 |
| 1h | OOS | 1,118 | 21.2 | 0.858 | 0.977 | -1.53 |
| 1h | FULL | 2,726 | 21.2 | 0.953 | 1.091 | -0.71 |

**1h의 IS 최선(net PF 1.013)조차 OOS에서 0.858로 되레 하락** — 우연한 IS 잡음이었을
가능성이 높다(t가 애초에 0.14로 유의하지 않았다).

### 종목별 상세(13개 장기이력, FULL 기준 내림차순, 상위 5개만 표시 — 전체는
`scratchpad/ttm_final_detail_{15m,1h}.csv`)

**15m**: 전 종목 net PF 0.66~0.86, 중앙값 0.831. **13종목 중 net PF≥1.3: 0개.**

**1h**: SOL 1.223, BTC 1.215, TU 1.188, XRP 1.156 순으로 상위 4개 종목만 근소하게 1.0을
넘고 나머지 9개는 1.0 미만. 중앙값 0.907. **13종목 중 net PF≥1.3: 0개.**

## 파라미터 민감도 (IS 기준)

- `kc_mult`(채널 폭 1.0~2.0): 15m은 2.0(넓은 채널)이 유리, 1h는 1.0(좁은 채널)이 유리 —
  TF별로 반대 방향이라는 것 자체가 강건한 패턴이 아님을 시사.
- `momentum_lookback`(14~26): 26(가장 긴 룩백)이 15m·1h 공통으로 최선 — 짧은 룩백은
  노이즈에 더 취약.
- `exit_mode`: **'decel'(감속 즉시 청산)이 'sign_flip'보다 전 구간에서 일관되게 열등**
  — 원문의 "색 반전 부분청산" 아이디어를 전량청산으로 단순화한 버전은 수익 구간을 조기에
  끊어 오히려 손해. 부호 반전까지 기다리는 쪽이 낫다.
- `chop_exit_bars`(10 vs 20): 거의 영향 없음 — 정체 시간청산이 발동하는 빈도 자체가
  낮다는 뜻(대부분 SL이나 부호반전이 먼저 발동).
- `sl_atr_mult`: 크립토 변동성상 넓은 SL(2.0~2.5)이 좁은 SL보다 근소하게 우세.
- **knife-edge 아님**: 완만한 변화, 다만 도달 최댓값 자체가 낮아(15m 0.76·1h 1.01)
  민감도를 논할 실익이 크지 않다.

## 최종 판정: **FAIL**

**근거**:
1. **IS 그리드서치(648개 조합)에서 net PF 최댓값이 15m 0.758·1h 1.013** — 1h 최선조차
   1.0을 겨우 넘긴 수준(t=0.14, 완전 무의미)이고, 이마저 **held-out OOS에서 0.858로 재차
   하락**했다.
2. **13개 장기이력 종목 전원(15m·1h 공통) net PF<1.3.** 15m은 전 종목이 0.66~0.86에 몰려
   있고, 1h도 상위 4개 종목만 1.0을 살짝 넘을 뿐이다.
3. 스펙이 제시한 "색 반전 시 부분청산" 아이디어를 단순화한 `decel` 청산 모드는 오히려
   `sign_flip`보다 일관되게 나빴다 — 조기 이익실현이 이 전략의 핵심 우위가 아님을 시사.
4. 표본은 15m에서 충분(종목당 수천 건), 1h도 종목당 100~300건 수준으로 판정에 무리가
   없다.

스퀴즈 해제+모멘텀 가속이라는 아이디어 자체는 합리적이나, 크립토 15m·1h에서는 "해제 첫 봉"
신호의 방향 예측력이 거의 없다(gross PF도 1.0~1.17 수준). 참여지표가 압도적으로 높음에도
불구하고 크립토 정량 검증 수치가 어디에도 공개되지 않았던 이유가 실증적으로 뒷받침된다.
**라이브 반영하지 않는다.**

## 미검증/근사 요소 (정직한 한계 고지)

- **4h 확인 필터(htf_confirm) 미검증**: 스펙의 "4h 봉에서도 같은 방향 모멘텀 유지 시 신뢰도
  상향" 옵션은 구현하지 않았다(멀티TF causal 정렬 구현 비용 대비, gross PF가 이미 1.0~1.17
  수준이라 필터 추가로 1.3까지 끌어올릴 가능성은 낮다고 판단해 우선순위를 낮췄다). 향후
  재검증 시 1순위 후보.
- **켈트너 range를 SMA(TrueRange) 대신 Wilder ATR로 근사**(원문과 완전 동일하지 않음).
- **부분청산(스펙 원문의 "1차 색반전 부분청산+2차 완전반전 전량청산") 미구현** — 단일
  풀사이즈 포지션으로 단순화(Simplicity). `decel` 모드가 이를 근사하려 했으나 오히려
  성과가 나빠 원문 부분청산 아이디어 자체가 크립토에서 유효하지 않을 가능성을 시사.

## 재현 스크립트

- `scratchpad/bt_ttm_squeeze.py` — TTM 스퀴즈 이벤트기반 시뮬레이터.
- `scratchpad/run_ttm_sweep.py` — IS 전용 그리드서치(15m/1h, 각 324조합). 결과:
  `scratchpad/ttm_sweep_{15m,1h}.csv`.
- `scratchpad/run_ttm_final_eval.py` — 동결 파라미터로 전 22종목 IS/OOS/FULL 상세 평가.
  결과: `scratchpad/ttm_final_detail_{15m,1h}.csv`.
- 재현 커맨드:
  ```
  cd /home/user/study
  python3 scratchpad/bt_ttm_squeeze.py BTCUSDT 1h     # 단일 심볼 스팟체크(기본 파라미터)
  python3 scratchpad/run_ttm_sweep.py 15m             # IS 그리드서치(15m, 324조합)
  python3 scratchpad/run_ttm_sweep.py 1h              # IS 그리드서치(1h, 324조합)
  python3 scratchpad/run_ttm_final_eval.py            # 동결 파라미터 전종목 상세
  ```
