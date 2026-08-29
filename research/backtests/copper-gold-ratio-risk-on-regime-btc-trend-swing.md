# [스윙] 구리/금 비율(Dr. Copper) 리스크온 레짐 + BTC/ETH 추세추종 — 백테스트

- **전략 스펙**: `research/strategies/copper-gold-ratio-risk-on-regime-btc-trend-swing.md`
- **원전 근거**: 없음(스펙 자체 명시 — "구리는 박사학위 소지자" 통설의 정성적 인용뿐, 이 정확한
  규칙을 크립토 무기한선물에 백테스트한 외부 자료 없음). 순수 자체 백테스트로만 판정.
- **트레이드 대상**: BTC/ETH 2종목 무기한(USDT-M), 종목별 독립 진입, 둘 다 `major_bases`.
- **작성일**: 2026-08-29 (UTC).
- **구현**: 자체 완결형 스크립트(1d 레짐/추세 + 4h 확인·체결 듀얼 TF가 기존 `SwingStrategy`
  인터페이스와 맞지 않아 별도 엔진 — 수수료/슬리피지/리스크 사이징 관례는 프레임워크 그대로 재현):
  `research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py` (`research/impl/`은
  `.gitignore` 대상이라 저장소에 없음 — 핵심 로직은 본문 말미 "재현용 핵심 코드"에 인용).
  공통 로더는 `research/impl/bt_common.py`(기존 다수 스펙과 공유하는 표준 klines 로더,
  `SYMBOLS`/`IS_END`/`OOS_END`/`TAKER_FEE`/`SLIPPAGE` 상수 포함) 그대로 재사용.
- **⚠️ 격리 메모**: 지시대로 scratchpad 캐시 디렉터리에 `cugold_` 접두를 사용
  (`cugold_commod/` — Yahoo Finance HG=F/GC=F/DXY/VIX + FRED BAA10Y 캐시). 동시 진행 중인
  미 2년물 국채금리 백테스트(`us2y_` 접두)는 건드리지 않았다. 바이낸스 선물 klines 캐시
  (`klines_cache/`)는 여러 스펙이 공유하는 범용 캐시라 BTC/ETH 1d·4h(2021-09~2026-07) 기존
  캐시를 그대로 재사용(재다운로드 없음, 특정 전략에 종속적이지 않은 원자재 데이터).

## 재현 커맨드

```
python3 research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py sanity     # 룩어헤드/정합성
python3 research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py nocost     # 무비용(fee=0,slip=0) 진단
python3 research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py freq       # 신호빈도·비율드리프트·전제일관성
python3 research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py tautology  # DXY/BAA10Y/VIX 동어반복 점검
python3 research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py cluster    # 레짐구간 de-clustering·상관·롤링윈도우
python3 research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py is_oos     # 메인 결과표
python3 research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py sens       # 파라미터 스윕
python3 research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py robust     # LOO/top-N/반전/게이트대조군/부트스트랩
```

- **IS**: 2022-01-01 ~ 2024-06-30 23:59:59, **OOS**: 2024-07-01 ~ 2026-06-30 23:59:59
  (`bt_common.IS_END`/`OOS_END`, 둘 다 경계 사각지대 방지용 23:59:59 명시, FULL=IS+OOS 정확히
  일치 실측 확인: n(IS)=85 + n(OOS)=76 = n(FULL)=161).
- 비용: 왕복 0.14%(편도 taker 0.05% + 편도 슬리피지 0.02%, `bt_common.TAKER_FEE`/`SLIPPAGE`
  그대로 사용 — 이미 이 값이 지시받은 "왕복 0.14%"와 정확히 일치). 리스크 1%
  (`RiskManager.build_plan_with_stop`, 기존 스윙 스펙군과 동일 관례).

## 설계 판단([설계판단] 명시)

1. **룩어헤드 방지 핵심 규칙**: day D 내의 모든 4h 확인봉은 "day D-1까지 완전히 닫힌 일봉 종가"
   로만 계산한 레짐(`risk_on_at`)·추세(`uptrend_at`)·ATR(`atr_at`)만 참조한다(daily 시리즈에
   `shift(1)` 적용, day D 시작 시점=00:00 UTC 에 이미 알 수 있는 값). 4h EMA20 은 확인봉 자기
   자신의 종가까지(이미 닫힌 봉)로 계산 — 미래 참조가 아니라 "그 봉이 닫혔을 때 알 수 있는 값".
   **최종 체결은 신호가 확정된 확인봉의 다음 4h 봉 시가**(shift(1), 프레임워크 규약대로).
2. **구리/금 데이터 정렬**: Yahoo Finance 일봉 타임스탬프를 `.normalize()`로 날짜만 취해 크립토
   UTC 캘린더에 그대로 정렬 후 forward-fill(주말/COMEX 휴장일). 기존 `btc-gold-relative-
   momentum-rotation-swing` 스펙에서 리뷰어가 "Yahoo 일봉 라벨(대략 뉴욕 마감 후 갱신)이 항상
   신호시점(그 값을 다음날 00:00 UTC 부터 shift(1) 로 쓰기 시작)보다 선행"함을 확인해 룩어헤드
   없다고 판정한 선례를 따른다. 아래 §룩어헤드 검증에서 손검산·교란검사로 재확인.
3. **청산 메커니즘**: SL 초기값 = 진입가 ∓ ATR(14,1d,진입 트리거일 D-1 종가 기준)×1.8. 이후 매
   4h 봉마다 ATR(14,1d)×3.0 트레일링 후보값을 계산해 **기존 스톱보다 유리한 방향으로만**
   단조 조인다(SL 이 트레일링보다 항상 타이트하게 시작 — 이익 1.2×ATR 이상 진행돼야 트레일링이
   SL 을 추월). 스펙의 "SL=ATR×1.8(초기)"과 "TP=ATR×3.0 트레일링"을 단일 스톱 라인으로 결합한
   구현이며, 결과적으로 청산사유가 OOS 76건 전부 `stop_loss`(고정 TP 없음, 스펙 명시와 일치).
   레짐 반전 시 신규진입만 차단하고 기존 포지션은 트레일링에 위임(스펙 §청산규칙 그대로).
4. **레짐 구간(고유 연속 구간) 정의**: 스펙이 요구하는 de-clustering 단위. 심볼별로
   `(risk_on_at, uptrend_at)` 결합 상태(LONG레짐/SHORT레짐/중립·불일치/워밍업)가 바뀔 때마다
   새 블록 ID를 부여, 같은 블록에서 발생한 트레이드들의 R 합을 하나의 관측치로 재집계한다.
5. **쿨다운 2봉(4h)**: 스펙에 명시되지 않았으나 청산 직후 같은 봉/바로 다음 봉 즉시 재진입(휩소)을
   막기 위해 프레임워크 스윙 슬리브 기본값(`DEFAULT_COOLDOWN["swing"]=2`)을 그대로 적용.
6. **반전 대조군**: 이미 계산된 인과적 `long_sig`/`short_sig` 배열을 스왑하는 방식(원신호 결정
   로직은 그대로 두고 라벨만 교체)이라, 최종 방향 변수만 참조하는 구조를 자동으로 만족한다. 본
   전략의 스톱은 ATR 배수(가격 레벨이 아니라 거리)라 "방향성 조건으로 선택된 진입봉에서 반전
   스톱이 저절로 타이트해지는" CLAUDE.md 신규 규칙(Donchian/브레이크아웃류 함정)이 구조적으로
   적용되지 않음 — 리스크 거리 계산식이 애초에 방향 대칭이다.
7. **게이트 대조군(no_gate)**: 구리/금 리스크온 게이트를 제거하고 순수 EMA20/50 추세추종 +
   4h EMA20 확인만으로 진입(그 외 청산·사이징·비용 전부 동일 엔진).

## 룩어헤드·정합성 검증 (`sanity`)

| 점검 | 결과 |
|---|---|
| 구리(HG=F) 결측(ffill 대상) | 1,795 캘린더일 중 559일(31.1%, 전부 주말/COMEX 휴장) |
| 금(GC=F) 결측(ffill 대상) | 1,795 캘린더일 중 560일(31.2%) |
| 손검산 5개 표본(2021-10-31/2023-01-07/2024-03-16/2025-05-24/2026-07-31) | `risk_on`/`uptrend` 코드값과 D-1 기준 수동 재계산값 **5/5 완전 일치** |
| 룩어헤드 직접검증(BTC 마지막 40일 종가 ×1.6 교란) | 교란점 50일 이전 구간(1,745일) `uptrend_at` 변경 **0건**(정상) |
| 수수료 정합성(raw_pnl−fees−pnl) | BTC 87건, 최대 편차 **0.0000000000** |
| zero_hold_frac | BTC 0.0%, ETH 0.0%(모든 트레이드 최소 1봉 이상 보유) |
| 청산사유(BTC/ETH 전체) | 거의 전량 `stop_loss`, 데이터 끝 `end_of_data` 1건뿐 — 고정 TP 없음(스펙 그대로) |
| 무비용 진단(`fee=0,slip=0` 별도 실행, gross>=net 부등식 아님) | 트레이드 fees 합계 **0.0000000000**, `raw_pnl==pnl` 불일치 0/162건 |

## 신호 빈도·전제 점검 (`freq`)

- **구리/금 20/60일 MA 크로스 실측 빈도**: 4.91년간 42회 전환(**연 8.55회**) — 스펙 예상(연
  4~8회)과 거의 일치(상단에 근접).
- **ratio(t) 절대 레벨 구조적 드리프트**: 연도별 평균이 2021년 0.00243 → 2026년 0.00132로
  **단조 하락**(약 -46%, 금이 구리 대비 이 기간 크게 아웃퍼폼). 폐기조건 (e)는 통과했지만
  (아래), 이 장기 드리프트는 20/60일 MA 크로스의 상대적 민감도에 시간에 따라 영향을 줄 수
  있어 [주의사항]으로 기록.
- **종목별 실제 체결 빈도**: BTC 87건(**연 18.3건**), ETH 75건(**연 15.8건**) —
  스펙 예상(종목당 연 5~12건)의 **1.5~3.7배**. 원인: 하나의 레짐 구간(risk_on+uptrend 유지)
  동안에도 4h 종가가 EMA20을 여러 번 재교차하면 그때마다 신규 진입이 발화하기 때문(스펙
  진입규칙이 "레짐 전환 시 1회"가 아니라 "레짐 유지 중 4h 확인봉마다 재평가"로 명시돼 있어
  이는 스펙을 충실히 구현한 결과이지 구현 버그가 아니다).
- **폐기조건 (e) [판정단위: 전체 일별]**: 리스크온+상승추세 결합 발생률 BTC 23.9%/ETH 21.2%,
  리스크오프+하락추세 결합 BTC·ETH 모두 53.9% — **모두 5~85% 범위 내, 정의결함 아님**(통과).
- **전제의 내적 일관성**: `corr(risk_on_at, 당일수익률)` = BTC -0.021, ETH -0.025 — 거의 0이고
  부호도 스펙 테제(리스크온→상승)와 반대. 크기가 미미해 "동어반복"은 전혀 아니지만, **원신호
  단독으로는 방향 정보가 사실상 없다**는 신호(추세 게이트와 결합해야만 진입조건이 되므로
  이 자체가 곧바로 전략 실패를 뜻하진 않지만, 아래 게이트 대조군 결과와 일관된 방향).

## 동어반복 점검 (`tautology`, 표본범위제한 감안)

| 대상 | 전체구간 상관 | 트리거 시점 한정(BTC) | 트리거 시점 한정(ETH) |
|---|---:|---:|---:|
| DXY 20일 모멘텀 | +0.005 | +0.023 (n=1,350) | +0.027 (n=1,302) |
| BAA10Y 20일 변화 | -0.264 | -0.315 | -0.306 |
| VIX 레벨 | -0.130 | -0.254 | -0.194 |

모두 `|r|<0.7`(재포장 위험 임계). 트리거 시점 한정 상관이 전체구간보다 소폭 커졌으나(표본범위
제한과 반대 방향) 여전히 임계에 크게 못 미쳐 — **기존 DXY/BAA10Y/VIX 매크로 스펙군의 재포장이
아니다**(스펙의 사전 우려 해소).

## 메인 결과 (`is_oos`, 트레이드 단위)

| 구간 | 거래수 | 순손익(USDT) | net PF(R) | gross PF(R) | 승률 | t-stat(R) | 수수료 |
|---|---:|---:|---:|---:|---:|---:|---:|
| FULL | 161 | +1,184.39 | 1.173 | 1.205 | 34.2% | +0.68 | 234.88 |
| IS | 85 | +1,708.31 | 1.482 | 1.524 | 34.1% | +1.10 | 123.03 |
| OOS | 76 | -523.93 | **0.899** | 0.923 | 34.2% | **-0.36** | 111.85 |

OOS 종목별: BTC n=44, 순손익 -785.89, net PF(R)=0.716, gross PF(R)=0.740 / ETH n=32, 순손익
+261.97, net PF(R)=1.168, gross PF(R)=1.191. 청산사유(OOS): `stop_loss` 76/76(100%).

**무비용(fee=0,slip=0) 진단**: OOS net PF(R)=0.931, t=-0.24 — **비용을 걷어내도 OOS 는 여전히
PF<1**. 즉 실패 원인이 "수수료 잠식"이 아니라 애초에 방향 예측력이 없다는 것.

## 폐기조건 판정 (스펙 사전 등록 우선순위 (b)>(e)>(a)>(c)>(d), 레짐구간 de-clustering 단위)

레짐 구간(고유 연속 구간) 단위 재집계 (`cluster`):

| 구간 | 명목거래수 | 고유 레짐구간수(BTC+ETH) | 블록단위 net PF(R) | 블록단위 net t | 블록단위 gross PF(R) | 블록단위 gross t |
|---|---:|---:|---:|---:|---:|---:|
| FULL | 161 | 61 | 1.269 | +0.70 | 1.324 | +0.82 |
| IS | 85 | 41 | 1.688 | +1.16 | 1.758 | +1.23 |
| OOS | 76 | **22** | **0.833** | **-0.36** | **0.872** | **-0.27** |

1. **(b) 표본부족 [최우선]**: OOS 고유 레짐구간수(BTC+ETH 합산) = **22건 ≥ 12** → 표본부족
   아님, **판단불가 아님**. (다음 조건으로 진행.)
2. **(e) 정의결함**: 위 §신호빈도에서 확인 — 5~85% 범위 내, **정의결함 아님**.
3. **(a) [최우선 FAIL 판정, 판정단위=레짐구간 de-clustering 기준]**: OOS 블록단위 net
   PF(R)=0.833 **< 1.15** *AND* t=-0.36 **(|t|<1.96, 비유의)** → **OR 결합 조건 양쪽 모두 충족,
   FAIL 확정**. gross 블록단위도 t=-0.27(비유의) — net 에 적용한 de-clustering을 gross 에도
   병행해 확인(CLAUDE.md 신규 규칙 준수), gross 기준으로도 유의성 없음.
4. **(c) [참고, 이미 (a)로 FAIL 확정된 뒤라 판정에 영향 없음]**: IS 블록단위 gross PF(R)=1.758
   ≥ 1.0 → 이 조건은 미충족(IS 단계에서 이미 죽지는 않았음).
5. **(d) [최하위 우선순위, 미실시]**: DXY 게이트 대조군(별도 게이트 소스 스왑판) 구축은
   스펙이 정한 우선순위상 (a)가 이미 결정적 FAIL을 내린 뒤라 실시하지 않았다 — 정직하게 범위
   제한으로 기록. (다만 아래 §게이트 대조군에서 "게이트 자체의 부가가치"는 별도로 검증했다.)

**→ 사전 등록 폐기조건 (a) 충족으로 FAIL.**

## 종목 간 신호 상관·꼬리 상관·롤링 클러스터 (`cluster`)

- **동시진입 비율**: OOS 진입일 65일 중 BTC/ETH 같은 캘린더일 동시진입 11일(16.9%). 다만
  "LONG 또는 SHORT 레짐 활성" **일 단위**로 보면 BTC/ETH 동시 활성 비율이 **89.7%**(구리/금
  레짐 성분이 100% 공유되고 BTC/ETH 자체 추세도 강한 정상관이라 대부분의 시간 두 종목이 같은
  레짐 상태). 명목 22개 레짐구간(BTC 12 + ETH 10)이 실질적으로는 상당수 겹치는 기간에 걸쳐
  있어 **실질 독립 베팅 수가 명목보다 적을 가능성**을 시사.
- **꼬리 상관**: BTC/ETH 일수익률 상관 평시 +0.839, BTC 절대수익률 상위 5% 꼬리국면 +0.924 —
  평시부터 이미 매우 높고 위기국면에서 소폭 더 높아짐(둘 다 극히 높은 수준이라 "평시엔 낮고
  위기엔 급등"하는 함정형 패턴은 아니고, 애초에 BTC/ETH가 항상 강하게 동조).
- **3~5일 롤링 윈도우 재검사(OOS)**: 최대 기여 5일 창(2026-01-27 시작)이 OOS 순 R 합계의
  **-186.8%**(총합보다 더 큰 음의 기여, 즉 이 창 하나가 순손실의 대부분을 만들고 나머지 구간은
  근소한 순이익)를 차지. 이 창을 제외해도 net PF(R)=0.709, t=-1.19 — **여전히 손실**(단일
  악성 클러스터로 결과가 과장된 것이 아니라, 그 클러스터를 빼도 실패가 유지됨).
- **top-1/2 레짐구간 제거**: 각각 net PF(R)=0.781(t=-0.81), 0.675(t=-1.27) — 제거할수록 오히려
  악화(승리 구간이 드물고 얇게 분산돼 있다는 뜻, 특정 대형 클러스터가 결과를 부풀린 것이 아님).

## 파라미터 민감도 (`sens`, OOS/IS 풀링, R기준)

| 변형 | OOS n | OOS net PF(R) | OOS gross PF(R) | OOS t | IS n | IS net PF(R) | IS t |
|---|---:|---:|---:|---:|---:|---:|---:|
| base(20/60,20/50,SL1.8,trail3.0) | 76 | 0.899 | 0.923 | -0.36 | 85 | 1.482 | +1.10 |
| ratio_ma=10/40 | 85 | 0.569 | 0.584 | -2.03 | 91 | 1.253 | +0.69 |
| ratio_ma=15/50 | 78 | 0.965 | 0.991 | -0.12 | 90 | 1.258 | +0.70 |
| ratio_ma=30/90 | 73 | 0.809 | 0.834 | -0.71 | 84 | 0.743 | -0.94 |
| ratio_ma=20/40 | 80 | 0.785 | 0.806 | -0.86 | 93 | 1.298 | +0.82 |
| ema=15/40 | 76 | 0.937 | 0.963 | -0.22 | 89 | 1.134 | +0.36 |
| ema=30/60 | 75 | 0.899 | 0.923 | -0.36 | 84 | 1.388 | +0.90 |
| atr_sl_mult=1.2 | 87 | 1.033 | 1.068 | +0.11 | 109 | 1.210 | +0.60 |
| atr_sl_mult=1.5 | 78 | 1.001 | 1.032 | +0.00 | 96 | 1.252 | +0.69 |
| atr_sl_mult=2.5 | 69 | 0.856 | 0.876 | -0.51 | 85 | 1.327 | +0.81 |
| atr_trail_mult=2.0 | 109 | 1.049 | 1.084 | +0.18 | 153 | 1.081 | +0.32 |
| atr_trail_mult=2.5 | 85 | 1.035 | 1.065 | +0.12 | 102 | 1.631 | +1.42 |
| atr_trail_mult=4.0 | 49 | **1.307** | 1.338 | +0.66 | 63 | 1.455 | +0.90 |

**13변형(base 포함) 전부 OOS t < 1.96** — 유의한 변형이 하나도 없다. `atr_trail_mult=4.0`
하나만 PF≥1.3(1.307)을 넘지만 t=+0.66 비유의·n=49로 통과선 미달.

## 견고성 (`robust`)

**LOO(OOS)**: BTC 단독 n=44 net PF(R)=0.716(t=-0.85) / ETH 단독 n=32 net PF(R)=1.168(t=+0.34,
비유의) — 어느 한 종목 제외로도 살아나지 않음.

**top-N 승리거래 제거(OOS, R기준)**: top-1 제거 0.794 / top-3 제거 0.616 / top-5 제거 0.475 —
승리가 소수 대형 트레이드에 몰려 있지 않고(그런 경우라면 몇 건 제거로 급락) 애초에 분산된
손실 구조.

**방향반전 대조군**:

| 구간 | 거래수 | net PF(R) | gross PF(R) | t-stat(R) | zero_hold_frac |
|---|---:|---:|---:|---:|---:|
| 정방향(OOS) | 76 | 0.899 | 0.923 | -0.36 | 0.0% |
| 반전(OOS) | 74 | 1.017 | 1.042 | +0.05 | 0.0% |
| 정방향(IS) | 85 | 1.482 | 1.524 | +1.10 | 0.0% |
| 반전(IS) | 75 | **2.125** | 2.173 | **+2.29** | 1.3% |

IS 구간에서는 **반전 대조군이 정방향보다 유의하게 우수**(t=+2.29)하다 — "구리 강세=BTC 상승"
테제의 방향성 자체가 최소한 IS 기간에는 지지되지 않고 오히려 반대 방향에 통계적으로 유의한
정보가 있었음을 시사한다(다만 OOS 에서는 반전도 PF≈1.0 손익분기 수준이라 IS 의 반전 우위가
OOS 로 이어지지 않음 — 반전을 채택 방향으로 재설계해도 통과선을 넘지 못한다). zero_hold_frac
이 반전 IS 1.3%(1건)로 낮게 유지돼 청산구조 아티팩트(반전 스톱이 저절로 타이트해지는 함정)는
관측되지 않음.

**게이트 대조군(구리/금 레짐 제거, 순수 EMA20/50 추세추종)**:

| 구간 | 거래수 | net PF(R) | gross PF(R) | t-stat(R) |
|---|---:|---:|---:|---:|
| 게이트판 OOS | 76 | 0.899 | 0.923 | -0.36 |
| 게이트없음 OOS | 83 | **1.157** | 1.189 | +0.46 |
| 게이트판 IS | 85 | 1.482 | 1.524 | +1.10 |
| 게이트없음 IS | 105 | 1.075 | 1.103 | +0.25 |

OOS 에서는 **게이트 없는 순수 추세추종이 게이트판보다 오히려 우수**(1.157 vs 0.899, 둘 다
비유의하지만). 표본수 맞춘 부트스트랩(100회, n=76 매칭): 게이트판 평균 R 이 게이트없음판
평균 R 을 초과하는 비율 = **25.0%**(100회 중 25회) — 게이트가 부가가치를 준다는 근거가
없을 뿐 아니라, 방향성 상 오히려 해로운 쪽에 가깝다(과거 GK/RS·SR 게이트 사례와 같은 패턴).

## 판정: **FAIL**

**근거(사전 등록 우선순위 그대로 적용)**:
1. (b) 표본부족 아님(레짐구간 OOS n=22≥12) → (e) 정의결함 아님 → **(a) 충족**: OOS 레짐구간
   de-clustering 기준 net PF(R)=0.833<1.15 이고 t=-0.36(비유의) — OR 결합 조건 둘 다 성립.
   gross 에도 동일 de-clustering 적용 시 t=-0.27 로 역시 비유의(CLAUDE.md 신규 규칙 반영).
2. **무비용(fee=0) 진단에서도 OOS PF(R)=0.931<1.0** — 비용 잠식이 아니라 애초에 방향 예측력
   없음.
3. **파라미터 스윕 13변형 전부 OOS t<1.96** — 특정 파라미터 선택의 우연이 아니라 구조적.
4. **게이트 대조군이 게이트판보다 우수하고(1.157>0.899), 표본수 맞춘 부트스트랩에서 게이트
   우위 25%뿐** — 구리/금 레짐 게이트 자체가 부가가치 없음(오히려 해로운 방향).
5. **IS 구간에서 방향반전 대조군이 유의하게(t=+2.29) 우수** — 방향성 테제("구리 강세=리스크온
   =BTC 상승")가 적어도 IS 기간에는 지지되지 않음. OOS 에서는 반전도 손익분기 수준이라 반전
   채택으로도 살아나지 않음.
6. BTC/ETH 신호 상관이 매우 높음(레짐 활성일 동시성 89.7%, 일수익률 상관 평시 0.84/꼬리
   0.92) — 명목 22개 레짐구간의 실질 독립 베팅 수는 그보다 적어 통계력이 명목보다 약함(다만
   이 요인은 이미 (a) 판정에 영향 없이 FAIL을 보강하는 방향).
7. LOO(BTC/ETH 개별)·top-N 제거·3~5일 롤링 클러스터 제거 전부 FAIL 방향으로 수렴 — 특정
   종목·특정 클러스터의 우연이 아니라 구조적.

**라이브 미반영**. `scalp15m` 단독 유지.

## 데이터 소스·한계

- 크립토 klines: `data.binance.vision` 선물(um) 월별 zip(BTC/ETH 1d·4h, 2021-09~2026-07,
  `klines_cache/` 재사용).
- 구리/금/DXY/VIX: Yahoo Finance 비공식 API(`query1.finance.yahoo.com/v8/finance/chart/{HG=F,
  GC=F,DX-Y.NYB,%5EVIX}`) — **비공식 API**로 재조회 시 값이 달라질 수 있음(과거 리포트들에서
  재다운로드 시 소폭 결측/값 차이 관측 전례 있음, 방향성 결론에는 영향 없었음). 본 리포트는
  2026-08-29 세션 중 1회 다운로드한 캐시(`cugold_commod/`)로 전량 재현.
- BAA10Y: FRED `fredgraph.csv`(공식 정적 CSV, 1986-01-02~2026-08-27) — 20일 변화율 계산에만
  참고용으로 사용(동어반복 점검), 전략 신호 자체에는 미사용.
- 원자재 선물은 연속선물(HG=F/GC=F) 특성상 만기 롤오버 조정이 자동 반영된 시리즈(Yahoo 표준
  연속선물 규약) — 별도 롤오버 아티팩트 점검은 수행하지 않았음(구리/금 가격 레벨 시계열을
  §신호빈도에서 육안 확인했을 때 만기 근처 불연속 점프는 관측되지 않았음, 단 전수 통계 검정은
  미실시라 [한계]로 기록).
- (d) DXY 게이트 대조군(신호원 스왑판)은 사전 등록 우선순위상 (a)가 이미 결정적 FAIL을 내려
  실시하지 않음(범위 제한, 정직하게 기록).

## 재현용 핵심 코드 (발췌)

```python
# 룩어헤드 방지 핵심: day D 시작 시점에 알 수 있는 값만 shift(1)로 노출
def build_regime(copper_ff, gold_ff, ma_short, ma_long):
    ratio = copper_ff / gold_ff
    ma_s = ratio.rolling(ma_short, min_periods=ma_short).mean()
    ma_l = ratio.rolling(ma_long, min_periods=ma_long).mean()
    risk_on_raw = (ma_s > ma_l)
    valid_raw = ma_s.notna() & ma_l.notna()
    risk_on_at = risk_on_raw.shift(1).fillna(False)   # D-1 종가까지 -> D 시작부터 사용 가능
    valid_at = valid_raw.shift(1).fillna(False)
    return RegimeSeries(..., risk_on_at=risk_on_at, valid_at=valid_at)

def build_trend_at(sdata):
    uptrend_raw = (sdata.ema20_1d > sdata.ema50_1d)
    valid_raw = sdata.ema20_1d.notna() & sdata.ema50_1d.notna()
    return uptrend_raw.shift(1).fillna(False), valid_raw.shift(1).fillna(False)

# 4h 확인봉 신호(그 봉 자신의 이미 닫힌 종가/EMA만 사용) -> 다음 봉 시가 체결(shift(1))
for i in range(n):
    dp = bar_day_pos[i]                       # 이 4h봉이 속한 날짜 D
    if long_ok[dp] and close[i] > ema4h[i]:
        long_sig[i] = True
    elif short_ok[dp] and close[i] < ema4h[i]:
        short_sig[i] = True
...
if direction_long is None and (i - last_exit_idx) > cooldown_bars and i + 1 < n:
    if long_sig[i]:
        open_position(i + 1, i, True)         # i+1 봉 시가 체결 (shift(1))
    elif short_sig[i]:
        open_position(i + 1, i, False)

# 청산: SL 인트라바 체크(이 봉 시작 이전 stop_price) -> 이 봉 고/저로 트레일링 갱신(단조 타이트닝)
if direction_long is not None:
    if direction_long:
        if low[i] <= stop_price:
            close_position(i, stop_price, "stop_loss")
    else:
        if high[i] >= stop_price:
            close_position(i, stop_price, "stop_loss")
if direction_long is not None:
    atr_v = atr_arr[bar_day_pos[i]]           # D(i)-1 종가 기준 ATR(shift1), 매일 갱신
    if direction_long:
        extreme = max(extreme, high[i])
        if np.isfinite(atr_v) and atr_v > 0:
            stop_price = max(stop_price, extreme - atr_trail_mult * atr_v)  # 단조 타이트닝
    else:
        extreme = min(extreme, low[i])
        if np.isfinite(atr_v) and atr_v > 0:
            stop_price = min(stop_price, extreme + atr_trail_mult * atr_v)
```

전체 스크립트: `research/impl/copper_gold_ratio_risk_on_regime_btc_trend_swing.py` (이 세션
워크트리 내, `.gitignore` 대상이라 저장소에는 없음 — 위 발췌가 핵심 로직 전부를 포함).
