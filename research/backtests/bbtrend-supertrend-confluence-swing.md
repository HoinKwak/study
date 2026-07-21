# 백테스트 — BBTrend(볼린저 듀얼 트렌드 오실레이터) + SuperTrend 컨플루언스 (스윙, 4h)

- **스펙**: `research/strategies/bbtrend-supertrend-confluence-swing.md`
- **구현**: `research/impl/bbtrend_supertrend_swing.py` (격리 커스텀 리플레이 엔진 — `SleeveBacktester`
  미사용. 이유는 `chandelier_exit_swing.py` 전례와 동일: `SleeveBacktester`는 매 스텝마다 시그널
  TF 최근 200봉짜리 창을 새로 만들어 그 창에서 지표를 재계산하는데, 이 전략은 장기 볼린저(50봉)
  +SuperTrend(ATR10, factor12 — 매우 완만한 래칭)를 쓰므로 200봉 창 재계산은 SuperTrend 밴드
  래칭 히스토리를 창 시작점에서 리셋시켜 라이브 상태와 어긋난다. 지표는 전체 히스토리에 대해
  한 번에 인과적으로 계산(볼린저/ATR/SuperTrend 모두 rolling/ewm, 미래 누출 없음), 각 시점 i는
  i 이하 데이터만 사용. `crypto_trader.signals.indicators`는 읽기 전용 재사용, 프로덕션 코드
  미수정.)
- **판정**: **FAIL**

## 방법

### 진입 (스펙 그대로)
- BBTrend = `(|단기하단−장기하단| − |단기상단−장기상단|) / 단기중심선 × 100`
  (단기 BB 20,σ2.0 / 장기 BB 50,σ2.0)
- SuperTrend(ATR기간10, factor12)
- 롱: `close[i] > supertrend_line[i]` (업트렌드 밴드) AND `BBTrend[i] > 0`
- 숏: `close[i] < supertrend_line[i]` (다운트렌드 밴드) AND `BBTrend[i] < 0`
- 신호는 봉 i **종가 확정 시점** 결정, 체결도 같은 종가(+슬리피지) — 룩어헤드 없음.

### 청산 [설계 판단 — 원문 TP30%/SL20%는 레버리지 하 과도해 ATR로 정규화, 스펙에도 명시된 재검토 사항]
두 모드를 A/B 비교:
- `atr_rr` (기본): SL = entry ∓ atr_mult×ATR(14,4h), TP = entry ± rr×risk (원문 30/20=1.5R 비율
  유지 시도)
- `st_flip`: 초기 SL만 두고(atr_mult×ATR 보호), **SuperTrend 방향 반전 시 청산**(스펙 §스카우트
  메모가 권장한 대안, 트렌드추종형 — 고정 TP 없음)

### 데이터·수수료·유니버스 (§5.4 반스누핑 규약)
- 유니버스: 사전 고정 7메이저(BTC/ETH/BNB/SOL/XRP/DOGE/ADA), USDT-M 무기한.
- 구간: **IS 2022-01~2024-06 / OOS 2024-07~2026-06**, PASS 판정은 OOS 기준(IS도 함께 확인).
- 데이터: `data.binance.vision` 선물(um) 월간 klines 4h, 2020-01~2026-06 (기존
  `chandelier_exit_swing.py` 다운로드 재사용 — 이 컨테이너는 fapi 451 지역차단).
  캐시: `/tmp/.../scratchpad/chandelier_data/*.parquet` (7종목 모두 보유, LINK는 미사용).
- 수수료 taker 0.05%/side + 슬리피지 0.02%(왕복 0.14%, §5.4 규약 그대로, 메이커 가정 없음).
- 사이징: 리스크 1%/트레이드로 스톱거리 역산(레버리지는 명목가치 상한 — 메이저 3x/알트 2x,
  `chandelier_exit_swing.py`와 동일 전례로 통일해 스윙 리서치 간 비교 가능하게 유지).

### 재현 커맨드
```
source .venv/bin/activate
python3 research/impl/bbtrend_supertrend_swing.py   # 기본표(atr_rr, 전체기간, 참고용)
# IS/OOS·민감도는 scratchpad에 저장한 재현 스크립트로 계산(아래 "재현 스크립트" 참조)
```
재현 스크립트: `/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/`
아래 인라인 커맨드들을 `research/impl/bbtrend_supertrend_swing.py`의 `run_backtest`/`pooled_pf`를
불러와 그대로 재실행 가능(별도 러너 스크립트 없이 함수 재사용).

## 결과 — 청산모드 A/B, 7종목 풀링 (IS/OOS)

| exit_mode | IS PF | IS n | OOS PF | OOS n |
|-----------|------:|-----:|-------:|------:|
| atr_rr (atr2.5, rr1.5, 기본) | 0.88 | 954 | 0.94 | 895 |
| atr_rr (atr2.0, rr1.5) | 0.88 | 1531 | 0.93 | 1351 |
| atr_rr (atr3.0, rr1.5) | 0.91 | 616 | 0.94 | 618 |
| atr_rr (atr2.5, rr1.0) | 0.90 | 1495 | 0.92 | 1324 |
| atr_rr (atr2.5, rr2.0) | 0.87 | 739 | 0.99 | 637 |
| **st_flip** | **1.26** | 299 | **1.23** | 249 |

- `atr_rr` 계열은 모든 ATR배수·R:R 조합에서 **IS/OOS 모두 PF<1(손실)** — 파라미터를 흔들어도
  일관되게 마이너스. 고정 TP(1.5R 등)를 볼린저/SuperTrend 신호와 결합한 조합은 이 프레임워크에서
  엣지가 없다.
- `st_flip`(스펙 §스카우트 메모가 권장한 대안)만 유일하게 IS 1.26 / OOS 1.23 로 **손익비 1
  이상**이지만, 가이드 기준(PF≥1.3)에는 **양쪽 다 못 미친다**. 이 모드를 더 파고든 결과는 아래.

## `st_flip` 모드 — 종목별 상세 (IS/OOS)

| symbol | 구간 | ret% | PF | win% | #tr | MDD% |
|--------|------|-----:|---:|-----:|----:|-----:|
| BTCUSDT | IS  | +23.14 | 1.64 | 19.5 | 41 |  7.90 |
| BTCUSDT | OOS | +15.66 | 1.71 | 20.0 | 30 |  9.86 |
| ETHUSDT | IS  |  +7.95 | 1.28 | 25.6 | 39 | 12.59 |
| ETHUSDT | OOS | +33.39 | 2.25 | 26.7 | 30 |  7.75 |
| BNBUSDT | IS  |  +2.71 | 1.08 | 14.3 | 42 | 17.32 |
| BNBUSDT | OOS |  −7.04 | 0.75 | 13.5 | 37 | 17.26 |
| SOLUSDT | IS  | +52.00 | 2.19 | 12.0 | 50 | 24.28 |
| SOLUSDT | OOS | −12.97 | 0.57 | 15.0 | 40 | 19.17 |
| XRPUSDT | IS  |  −5.92 | 0.79 | 23.1 | 39 | 15.46 |
| XRPUSDT | OOS | +42.12 | 2.65 | 17.9 | 28 |  9.92 |
| DOGEUSDT | IS |  −14.67 | 0.58 | 10.9 | 46 | 20.29 |
| DOGEUSDT | OOS | −20.32 | 0.50 | 10.0 | 50 | 25.47 |
| ADAUSDT | IS  |  −4.04 | 0.87 | 16.7 | 42 | 14.61 |
| ADAUSDT | OOS |  −4.47 | 0.84 | 14.7 | 34 | 18.24 |

**종목 간 일관성 없음** — OOS 기준 7종목 중 3종목(BTC/ETH/XRP)만 PF>1, 나머지 4종목
(BNB/SOL/DOGE/ADA)는 전부 **PF<1(손실)**. 승률도 전 종목 10~27%로 낮아(추세추종 특성) 소수
트레이드가 결과를 좌우하는 구조.

## XRP leave-one-out (반스누핑 규약 — 필수 확인)

XRP는 OOS에서 PF 2.65로 풀링 전체 지표를 크게 끌어올리는 종목이다. XRP를 빼고 재계산:

| 구성 | IS PF (n) | OOS PF (n) |
|------|-----------|------------|
| 7종목 전체(풀링) | 1.26 (299) | 1.23 (249) |
| **XRP 제외 6종목(풀링)** | 1.33 (260) | **1.02 (221)** |
| BTC+ETH만(참고, 2종목) | 1.49 (80) | 2.01 (60) |

- **XRP를 빼면 OOS 풀링 PF가 1.23 → 1.02로 사실상 손익분기까지 추락한다.** CLAUDE.md에 기록된
  "XRP 단일종목 착시" 패턴이 그대로 재현됨 — 7종목 전체의 OOS 엣지처럼 보이던 결과가 사실상
  XRP 한 종목(그리고 부분적으로 BTC/ETH)의 성과에 의존하고 있었다.
- majors(BTC/ETH/XRP) vs alts(BNB/SOL/DOGE/ADA) 로 나누면 더 뚜렷하다: majors OOS PF=2.23(n=88),
  **alts OOS PF=0.65(n=161, 손실)**. 4/7 종목이 OOS에서 명백히 실패하는데 "7종목 유니버스에
  일관된 엣지가 있다"고 말할 수 없다.

## 최종 판정: FAIL

**근거**:
1. 스펙 그대로에 가까운 청산(`atr_rr`, ATR 정규화 TP/SL)은 IS·OOS 모두 PF<1로 **명백한 손실**
   (파라미터를 ATR배수 2.0~3.0, R:R 1.0~2.0로 흔들어도 전부 마이너스 — 강건하게 실패).
2. 유일하게 손익비가 1을 넘는 `st_flip` 대안 청산도 IS 1.26/OOS 1.23으로 **가이드 통과선
   (PF≥1.3) 미달**이며, 무엇보다 **7종목 중 4종목(BNB/SOL/DOGE/ADA)이 OOS에서 PF<1로 손실**
   — 종목 간 일관성이 없다.
3. **XRP leave-one-out에서 OOS 엣지가 사실상 사라진다(1.23→1.02)** — §5.4 규약이 명시적으로
   경고한 "XRP 단일종목 착시" 패턴과 정확히 일치. 억지로 통과시키지 않는다.
4. 표본 수(IS/OOS 각 250~300건)는 충분해 "표본 부족"이 아니라 **엣지 부재를 확인**한 결과다.

TradingView 원문의 참여지표(1.6K 좋아요)가 높았던 만큼 발굴 우선순위는 합리적이었으나, 우리
프레임워크(수수료+슬리피지 반영, ATR 정규화 청산, 7종목 고정 유니버스, IS/OOS 분리)에서는
재현되지 않는다. 라이브에 반영하지 않는다.
