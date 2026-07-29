# 백테스트 리포트: 돈치안 채널 중간선(Midline) 눌림목 추세추종 (스윙, 4h/1d)

- **판정: FAIL**
- **일자**: 2026-07-29
- **스펙**: `research/strategies/donchian-midline-pullback-continuation-swing.md`
- **구현**: `research/impl/donchian_midline_pullback_continuation_swing.py` (+ 공통 유틸 `research/impl/bt3_common.py`)

## 프레임워크 규약 요약
- 데이터: 세션 로컬 15m 선물 캐시 `vendor_data/15m/*.pkl` (BTC/ETH/BNB/SOL/XRP/DOGE/ADA,
  2022-01-01 ~ 2026-06-30), 4h/1d는 `crypto_trader.backtest.multi_tf.resample_ohlcv` 로 리샘플.
- IS 2022-01-01~2024-06-30 / OOS 2024-07-01~2026-06-30. **전체 히스토리를 1회 실행한 뒤
  진입시각으로 IS/OOS 버킷 분리**(데이터프레임을 먼저 잘라 각각 재실행하면 OOS 시작점에서
  워밍업이 다시 시작되는 불연속이 생겨 이 방식을 피함).
- 비용: 편도 taker 0.05% + 슬리피지 0.02% (왕복 0.14%). 사이징: `RiskManager.build_plan_with_stop`
  로 1% 리스크 + 30x 레버리지 캡(7종목 모두 `major_bases`). **고정분수(비복리)** — 매 진입 시
  `starting_equity`(=1만 USDT) 기준으로 항상 리스크금액을 계산(복리 폭주로 PF/승률 판정이
  왜곡되는 것을 방지하는 기존 리서치 관행, `bt28_pivot_psar.py` 등과 동일).
- 룩어헤드 방지: 4h 지표(돈치안20/ADX14/ATR14)는 확정봉만 사용. 1d EMA50 필터는
  `sleeve_backtester._confirm_slices` 와 동일한 causal searchsorted 정렬로, 신호봉 시점까지
  **완결된** 최신 1d 봉만 참조(진행 중인 당일 봉은 절대 사용 안 함).
- 체결: 신호(눌림 되돌림 확정) 봉의 종가 + 슬리피지 (TWAP/다음봉시가 아님 — sleeve_backtester
  컨벤션과 동일, 원문에도 별도 체결모델 언급 없음).

## 구현 해석(원문에 없는 계수 — 명시)
- TP1 분할비율: 원문에 "직전 채널 상단/하단 도달 시 1차 청산, 이후 chandelier 트레일"만 있고
  분할비율은 없음 → **50/50** 을 임의 채택(민감도 점검 대상 아님, 구조 자체는 스윕함).
- SL: "눌림 저점/고점" = 눌림 확인 직전봉(i-1, 근접판정 봉)의 저가/고가로 해석.
- 나머지(ADX≥20, +DI/-DI, 0.3×ATR 근접, chandelier×2.5, SL×0.5×ATR)는 스펙 파라미터 그대로.

## 종목별 결과 (base: adx_min=20, midline_tol=0.3×ATR, sl_mult=0.5, trail_mult=2.5)

| 종목 | IS n | IS PF | IS WR% | IS ret% | OOS n | OOS PF | OOS WR% | OOS ret% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTC | 132 | 0.68 | 26.5 | -18.5 | 82 | 0.98 | 31.7 | -0.9 |
| ETH | 92 | 0.53 | 28.3 | -18.8 | 92 | 1.53 | 43.5 | +14.6 |
| BNB | 101 | 1.01 | 36.6 | +0.3 | 83 | 1.09 | 36.1 | +2.6 |
| SOL | 117 | 1.47 | 33.3 | +18.3 | 84 | 1.18 | 36.9 | +5.7 |
| XRP | 123 | 0.70 | 25.2 | -14.6 | 111 | 0.94 | 34.2 | -2.4 |
| DOGE | 135 | 1.24 | 35.6 | +10.5 | 95 | 0.73 | 31.6 | -10.5 |
| ADA | 108 | 1.72 | 36.1 | +20.9 | 95 | 1.74 | 42.1 | +22.0 |
| **Pooled** | **808** | **0.99** | **31.6** | **-1.9** | **642** | **1.13** | **36.6** | **+31.2**\* |

\* pooled ret%는 각 종목 non-compounding pnl 합산을 공통 1만 USDT 기준으로 나눈 값이라
  종목별 ret% 단순 합과 다르게 나옴(정상 — 각 종목이 독립적으로 1만 USDT를 쓴다고 가정한
  비교값이 아니라 전체 pooled pnl/1만).

## 정합 점검
- **청산사유 분해**(전체 1450건): `midline_reversal` 833건(57%), `stop_loss` 597건(41%),
  `trend_exhausted` 17건, `end_of_data` 5건. TP1 이후 잔량이 chandelier 로 살아남는 비율이
  매우 낮음 — 대부분 SL 또는 눌림 실패(midline 재돌파)로 조기 종료, "추세에 올라타 큰 수익"
  이라는 스카우트 기대와 달리 승률 25~42%대의 저승률·평균R 구조.
- **방향편중**: long 558 / short 894 (숏 쏠림, 2022 약세장+2023 박스권 구간 특성상 자연스러움 —
  버그 아님, ADX/DI/EMA 필터가 실제로 방향성을 반영한다는 방증).
- **표본 수**: 종목당 IS 92~135건, OOS 82~111건으로 최소 기준(수십 건) 이상 충분.
- **레버리지/수수료 왜곡**: 없음 확인 — 총 수수료(IS 3,421 / OOS 2,581 USDT)가 pooled net_pnl
  대비 과도하지 않고, gross/net PF 격차가 수수료만으로 설명 가능한 수준(왕복 0.14%×808건
  ≈ 113 USDT/종목당 평균 notional 규모 대비 정상 범위).

## 파라미터 민감도 (pooled)

| 변경 | IS n | IS PF | OOS n | OOS PF |
|---|---:|---:|---:|---:|
| base(adx_min=20,tol=0.3,sl=0.5,trail=2.5) | 808 | 0.99 | 642 | 1.13 |
| adx_min=18 | 902 | 0.93 | 728 | 1.18 |
| adx_min=25 | 578 | 0.97 | 456 | 1.10 |
| midline_tol=0.2 | 594 | 1.10 | 481 | 1.10 |
| midline_tol=0.5 | 1084 | 1.03 | 857 | 1.06 |
| sl_mult=0.3 | 817 | 0.99 | 649 | 1.15 |
| sl_mult=0.8 | 804 | 0.98 | 638 | 1.17 |
| trail_mult=2.0 | 826 | 0.95 | 666 | 1.11 |
| trail_mult=3.0 | 788 | 0.98 | 624 | 1.17 |

모든 변형에서 **IS PF ≤1.10, OOS PF ≤1.18** — PF≥1.3 문턱에 근접하는 조합이 하나도 없다.
단일 파라미터·단일 구간에서 우연히 좋아 보이는 조합(SOL·ADA IS/OOS 개별로는 1.5~1.7대)은
있지만 pooled·leave-one-out 기준으로는 재현되지 않아 **과최적화 의심**.

**Leave-one-out (OOS pooled PF, 종목 하나씩 제외)**: BTC제외 1.16 / ETH제외 1.08 / BNB제외 1.14 /
SOL제외 1.13 / XRP제외 1.17 / DOGE제외 1.21 / ADA제외 1.04 — 어느 종목을 빼도 1.3을 넘지 못함
(ADA 하나가 특히 pooled PF를 끌어올리고 있었음이 드러남 — ADA 제외 시 1.04로 하락).

## 결론
IS pooled PF 0.99(사실상 손익분기 이하), OOS pooled PF 1.13 — 둘 다 통과 기준(PF≥1.3) 미달이고
그마저 종목 간 편차가 크다(BTC·ETH·XRP는 IS에서 뚜렷이 손실, ADA만 두 구간 모두 강함).
파라미터를 ADX/근접허용치/SL/트레일 배수로 흔들어도 pooled PF가 1.1~1.2 밴드를 벗어나지
못해 이 전략군 자체의 근본적 엣지 부재로 판단한다. Leave-one-out 결과 ADA 단일 종목 의존도가
높아 "여러 종목 일관성" 기준도 충족하지 못한다. **FAIL.**

## 근사 갭
- 4h/1d 는 15m 원본 리샘플(정합성 문제는 없음, 15m이 최소 해상도).
- TP1 분할비율(50/50)은 원문 미명시로 우리가 정한 값 — FAIL 판정에는 영향 없음(민감도상
  PF가 이미 전 구간에서 문턱 미달).
- 원문에 정량 백테스트 근거가 없어(개념 설명 위주) 외부 수치와의 비교 검증은 불가능.

## backtest-reviewer 검증: VALID (FAIL 판정 타당)

**재실행 방법**: `python3 research/impl/donchian_midline_pullback_continuation_swing.py`
(scratchpad `vendor_data/15m/*.pkl`, cwd 무관 절대경로) — 종목별/pooled IS·OOS PF·n·승률·
leave-one-out·청산사유분해 **전부 소수점까지 리포트 표와 정확히 일치** 재현
(예: IS pooled PF 0.9934481..., OOS pooled PF 1.1329618..., ADA IS PF 1.72/OOS 1.74,
leave-one-out ADA제외 OOS PF 1.04 — 모두 동일).

- **정합**: bt3_common.causal_confirm_counts 를 `sleeve_backtester._confirm_slices` 코드와
  라인 단위 대조 — `(confirm.index+delta).asi8` / `searchsorted(..., side="right")` 로직 동일.
  fill_price 부호 규칙도 `sleeve_backtester._fill`(adverse = (direction==LONG) != closing)과
  동일 확인. **PASS**.
- **룩어헤드**: 진입게이트는 `close[i-1]`/`mid[i-1]`(직전봉) 근접판정 + 확정봉 i 종가로 트리거,
  SL 은 `low/high[i-1]` 기준 — 미래누출 없음. TP1/트레일/청산은 "pos is not None" 블록이
  당일 신규진입보다 먼저 실행돼 같은 봉 진입+청산(같은 봉 룩어헤드) 발생 안 함을 코드 순서로
  확인. **PASS**.
- **단위**: `load_15m` 이후 `df.index.dtype == datetime64[ns]`, 15분 간격 157,631/157,632건
  균일(갭 없음), 첫/끝 타임스탬프 2022-01-01 00:00 ~ 2026-06-30 23:45 로 리포트 주장과 일치
  직접 확인. **PASS**.
- **표본**: 종목당 IS 92~135 / OOS 82~111 — 스윙 표본으로 충분. **PASS**.
- **OOS/과최적화**: leave-one-out 재실행 결과 ADA 제외 시 OOS pooled PF 1.13→1.04 로 확인,
  ADA 단일종목 의존 주장 재현. 파라미터 스윕 9종 전부 PF 1.3 문턱 미도달 재확인. **PASS**.
- **수수료**: 리포트 수치 그대로 재현(수수료 총액 IS 3420.7/OOS 2580.7 USDT) — net PF 기준.
  **PASS**.

**결론**: 리포트 수치·로직·검증방법론 모두 독립 재실행으로 재현됨. 구현결함(거짓FAIL) 근거
없음. IS PF 0.99, OOS PF 1.13 둘 다 통과선(1.3) 미달이고 leave-one-out 으로 ADA 의존성까지
확인되므로 **FAIL 판정에 동의**.
