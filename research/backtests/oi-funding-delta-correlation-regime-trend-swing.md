# [스윙] OI변화율-펀딩변화 롤링 상관 레짐 게이트 + EMA 추세추종 — 백테스트

- **전략 스펙**: `research/strategies/oi-funding-delta-correlation-regime-trend-swing.md`
- **원전 근거**: 없음(스펙 자체 명시 — 스카우트 자체 설계, 정량 근거 없음). 순수 자체 백테스트로만 판정.
- **트레이드 대상**: BTC/ETH/BNB/SOL/XRP/DOGE/ADA 7종목 무기한(USDT-M), 종목별 독립 진입.
- **구현**: 자체 완결형 스크립트(1d 신호/4h 체결 듀얼 TF + 상관 게이트 구조가 기존 SwingStrategy
  인터페이스와 맞지 않아 별도 엔진 — 수수료/슬리피지/1% 리스크 사이징 관례는 프레임워크 그대로 재현):
  - `/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oifundcorr/download.py`
    (7종목 1d/4h klines, fundingRate 월간 덤프 + `metrics` 일별 덤프 수집·캐시)
  - `/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oifundcorr/load.py`
    (캐시 CSV → 일별 OI/펀딩합/klines 로더, 0-fill 결측 필터, `lru_cache`)
  - `/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oifundcorr/strat.py`
    (ΔOI%-Δfunding 롤링상관 게이트·EMA20/50 눌림목 신호·챈들리어/SL/시간청산 시뮬레이션 엔진,
    gate_mode 4종·reverse·fee_zero 지원)
  - `/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oifundcorr/stats_util.py`
    (PF/t-stat/부트스트랩 CI/표본수 맞춘 매칭 비교 유틸)
  - `/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/oifundcorr/analyze.py`
    (18개 섹션 전체 분석 — 기초통계·IS/OOS/FULL·de-clustering·LOO·top-N·스윕·반전·대조군·
    무비용진단·셔플검증·부트스트랩·룩어헤드감사·회계정합)
  - ⚠️ `research/.gitignore`가 `impl/`을 제외하는 것과 별개로 이 스크립트들도 워크트리 소멸 시
    사라지므로, **핵심 로직은 아래 "재현용 코드"에 전문 인용**한다.

## 판정: **FAIL**

스펙이 **사전 등록한** 폐기조건 (b) "OOS PF(R) < 1.15 **또는** t 비유의 → FAIL"에 정확히 해당한다.
OOS PF(R)=1.424로 1.15는 상회하지만, **OOS t=+1.565(p=0.120, df=132)로 통계적으로 유의하지 않다**
(이 프로젝트의 |t|≥1.96 관행 기준 미달). PF 단독 수치(1.423)는 과제 가이드의 "OOS PF≥1.3" 문턱을
표면상 넘지만, (b)의 "또는 t 비유의" 절이 별도로 충족되므로 폐기조건이 성립한다. 아래에 서술하듯
표본은 충분하고(OOS n=133≥20) 룩어헤드·회계·데미닝 결함도 없어 **"판단불가"가 아니라 "표본은
충분한데 효과가 통계적으로 불확실하고 구조적으로 취약한 FAIL"**로 판정한다. 스펙의 다른 폐기조건
(a)(게이트 유무 대조군)와 (c)(셔플 발화율)는 **충족되지 않는다**(게이트가 대조군보다 낫고, 셔플
대비 발화율도 실재한다) — 즉 이 전략은 "완전 무가치"는 아니지만, **재현 가능한 확신을 얻기엔
증거가 부족**하다.

## 방법 / 재현성

- **데이터**: `data.binance.vision` 선물(um) 덤프. 7종목 **1d/4h klines**(monthly zip, 2021-11~
  2026-06), **fundingRate**(monthly zip, 8h 관측치 일별 합산), **`metrics`**(daily zip,
  5분 간격 `sum_open_interest`, 2021-11-01~2026-06-30) — 7종목×1703일=**11,921개 요청 전량 확보**
  (재시도 포함, 404/badzip은 0바이트로 마킹해 재요청 생략).
- **데이터 정합성**: BTC는 1703/1703일 완전. 나머지 6종목은 2021-11 한 달(30일)이 결측(그 시점
  `metrics` 미개설 추정) — **IS_START(2022-01-01) 이전 워밍업 구간에만 해당**, IS/OOS 결과에는
  영향 없음(EMA50/ATR22/corr20 모두 2021-12-01~2022-01-01 사이 워밍업으로 충분히 안정화).
- **⚠️ 0-fill 결측 발견·수정**: 초기 구현에서 `doi_pct`에 **inf 3건**(BTC 2022-03-07,
  2024-07-10/12) 발생 — 원인은 해당 일자 `metrics` 5분 스냅샷 중 일부(예: 2024-07-10은
  288건 중 41건)가 결측 대신 **리터럴 0**으로 채워진 것(과거 여러 라운드에서 반복 지적된
  "2024-07-09~15 0-fill" 패턴과 정확히 일치). `sum_open_interest > 0` 필터로 제외 후 재계산해
  inf/이상치 완전 소멸 확인(코드에 필터 반영, 아래 §재현용 코드 참조).
- **IS/OOS**: IS **2022-01-01~2024-06-30 23:59:59**, OOS **2024-07-01~2026-06-30 23:59:59**
  (IS_END 23:59:59 명시로 경계 사각지대 차단, §"IS+OOS==FULL 확인"에서 실측 검증).
- **수수료/슬리피지**: 왕복 0.14%(테이커 0.05%/side + 슬리피지 0.02%/side).
- **사이징**: `risk_amount = equity × 1%`, `quantity = risk_amount / SL거리`, 명목상한
  `equity × leverage`(7종목 전부 `major_bases`라 레버리지 30x) — 프레임워크
  `RiskManager.build_plan_with_stop` 공식 그대로 재현.
- **신호/체결 타이밍(설계 판단, 명시 필요)**: 스펙이 "1d 신호/4h 확인(진입 타이밍 미세조정)"이라고만
  서술해 정확한 체결 규칙을 명시하지 않아, `oi-breadth-regime-gate` 라운드와 동일한 보수적 관례를
  채택했다 — **신호는 day d 종가(=day d+1 00:00 UTC)에 확정**되고, **체결은 day d 다음 4h
  봉(=day d+1 00:00 UTC 봉) 시가**. `metrics` OI 대표값도 "day d 의 값 = 그 날 마지막 5분
  관측치(23:55 근방)"로 정의 — 이는 day d 의 klines 종가와 동일 시점에 확정되므로 이 관례와
  정합적이다(스펙 원문의 "해당 일봉 시가 시점 이전 마지막 관측치"를 문자 그대로 하면 day d 값이
  day d-1 의 관측치가 되어 한 칸 더 보수적이지만, 결과적으로 신호 확정↔체결의 선후관계는 동일하게
  안전하다).
- **재현 커맨드**:
  ```
  cd <scratchpad>/oifundcorr
  python3 download.py    # klines/funding(월간) + metrics(일별) 전량 수집(1회, ~12,000 요청)
  python3 load.py         # 데이터 정합성 점검(결측·범위)
  python3 analyze.py > analyze_out.txt   # 18개 섹션 전체 분석
  python3 per_symbol.py   # 종목별 IS/OOS 세부표
  ```

## 결과 1 — 기초통계: 게이트 발화율·ΔOI%~Δfunding 상관 실측(2022-01~2026-06)

| 종목 | 게이트 ON 비율 | ΔOI%~Δfunding 상관(pandas.corr) |
|---|---:|---:|
| BTC | 24.4% | +0.071 |
| ETH | 32.0% | +0.061 |
| BNB | 16.9% | **-0.045** |
| SOL | 24.1% | **-0.033** |
| XRP | 18.9% | +0.057 |
| DOGE | 23.3% | +0.074 |
| ADA | 21.0% | +0.063 |
| 평균 | 23.0% | **+0.035** |

스펙이 "전제의 내적 일관성" 항목에서 사전 예상한 상관 **0.2~0.4**보다 실측값(**평균 0.035**, 범위
-0.045~+0.074)이 **훨씬 약하다**. 7종목 중 2종목(BNB·SOL)은 **음의 상관**으로, "레버리지 신규
유입과 펀딩 프리미엄 상승이 함께 움직인다"는 스펙의 서사가 이 두 종목에서는 평균적으로 성립하지
않는다. (동어반복 위험 신호인 "0.8+" 근처는 전혀 아니므로 그 방향의 우려는 기각된다.)

## 결과 2 — 신호빈도 실측 vs 스펙 예상(종목당 연 15~35건)

| 종목 | 체결 n(2022-01~2026-06) | 연환산(건/년) |
|---|---:|---:|
| BTC | 36 | 8.01 |
| ETH | 48 | 10.68 |
| BNB | 38 | 8.46 |
| SOL | 39 | 8.68 |
| XRP | 35 | 7.79 |
| DOGE | 38 | 8.46 |
| ADA | 29 | 6.45 |
| **평균** | — | **8.36** |

스펙 예상(15~35건/년)의 **24~56%**로 하단에도 못 미친다. 신호빈도 붕괴 수준(과거 라운드의
1/60~1/500)은 아니지만, "저빈도·고R 목표"라는 스펙 설계 취지에 비해 절반 이하로 적다 —
게이트(ON 비율 23%)와 EMA20 눌림목 재진입 조건의 결합이 예상보다 더 드물게 겹친다.

## 결과 3 — IS/OOS/FULL 성과 (채택안, gate=corr, net)

| 구간 | n | PF_gross | PF_net | t(net) | p | 승률 | 순손익(USDT) |
|---|---:|---:|---:|---:|---:|---:|---:|
| FULL | 263 | 1.233 | 1.186 | +1.059 | — | 38.0% | +2,726.5 |
| IS | 130 | 1.019 | 0.973 | -0.117 | — | 34.6% | -206.9 |
| **OOS** | **133** | **1.466** | **1.423** | **+1.565** | **0.120** | 41.4% | **+2,933.4** |

**OOS 단독 유의성**: t=+1.565, df=132, **p=0.120 — 통상 기준(p<0.05, \|t\|≥1.96)에 미달**.
IS는 net PF 0.973로 사실상 손익분기 이하(수수료 반영 시 소폭 손실) — IS/OOS 우열이 뚜렷하게
갈려 있다(아래 §9 스윕에서 이 패턴이 파라미터 전반에 반복됨을 확인).

## 결과 4 — de-clustering: 고유 진입일, 7종목 동시진입일

OOS 명목 n=133, **고유 진입일=114**(명목:고유=1.17 — 클러스터링 크지 않음). 2종목 이상 동시진입일
**18일**, **7종목 전부 동시진입일 0건**(1d 신호·게이트 특성상 국지적 쏠림은 있으나 전면적 매크로
클러스터는 아님). **이벤트(날짜) 단위 재집계**: n=114, PF=1.456, **t=+1.410**(여전히 비유의) —
의사반복으로 인한 t 부풀림 우려는 크지 않으나, 애초에 봉 단위 t 자체가 비유의라 결론 불변.

## 결과 5 — holding_bars 분포 / zero_hold_frac 유효성 점검

```
count 267, mean 65.7봉(4h), min 1, 25% 24, 50% 61, 75% 120(=max_hold 20일=120×4h), max 120
holding_bars=1(최소단위) 비율 = 0.75%
```

**⚠️ 이 엔진에서 `zero_hold_frac`(진입 봉 즉시청산, holding_bars=0)은 구조상 항상 0이다** — SL/
챈들리어 체크가 "포지션이 이미 열려 있는 상태"에서 매 루프 시작 시 이루어지고, 진입은 루프 종료
시점에 성립하므로 신규 진입 트레이드는 그 봉에 자기 자신의 SL을 체크할 기회가 없다(최소
holding_bars=1). 따라서 **"zero_hold_frac=0"을 반전 대조군의 청산버그 부재 근거로 쓰지 않는다**
(과거 라운드에서 지적된 "트리비얼 지표" 함정 — 이 엔진에서는 애초에 검증력이 없는 지표). 대신
holding_bars=1(최소단위 청산) 비율(0.75%, 267건 중 2건)을 참고 삼아 "즉시 반대방향 급변으로
청산되는 이상 트레이드가 과다하지 않다"는 정황 확인 용도로만 사용한다.

## 결과 6 — LOO(7종목 각 제외, OOS)

| 제외 종목 | n | PF | t | 순손익 |
|---|---:|---:|---:|---:|
| BTC | 115 | 1.445 | +1.543 | 2,634.4 |
| ETH | 111 | 1.430 | +1.458 | 2,418.9 |
| BNB | 112 | 1.382 | +1.322 | 2,252.8 |
| **SOL** | 110 | **1.227** | **+0.818** | 1,330.9 |
| XRP | 117 | 1.476 | +1.633 | 2,963.0 |
| DOGE | 118 | 1.498 | +1.669 | 3,047.4 |
| ADA | 115 | 1.497 | +1.642 | 2,953.1 |

SOL 제외 시 PF/t가 가장 크게 하락(1.423→1.227, t 1.565→0.818) — **SOL 단일종목 의존이 상당하다**
(아래 §종목별 표에서 재확인). 다른 6종목 제외 시에는 PF가 1.38~1.50 범위로 비교적 안정적이다.

## 결과 7 — top-N 승리 트레이드 제거 (OOS)

| 제거 | n | PF | t | 순손익 |
|---|---:|---:|---:|---:|
| 없음 | 133 | 1.423 | +1.565 | 2,933.4 |
| top-1 | 132 | 1.336 | +1.307 | 2,325.7 |
| top-2 | 131 | 1.249 | +1.028 | 1,726.7 |
| top-3 | 130 | 1.172 | +0.747 | 1,190.5 |
| **top-5** | 128 | **1.037** | **+0.175** | 254.3 |

**상위 5건(133건 중 3.8%) 제거만으로 OOS PF가 1.423→1.037(사실상 손익분기)로 붕괴**, t는 이미
비유의였던 것이 더욱 무의미(+0.175) 해진다. 소수 트레이드에 대한 의존도가 상당하다.

## 결과 8 — 분기별 순익 분포 (OOS)

| 분기 | n | 순익 | 비중 |
|---|---:|---:|---:|
| 2024Q3 | 14 | -103.3 | -3.5% |
| 2024Q4 | 15 | -337.0 | -11.5% |
| **2025Q1** | 19 | **+952.8** | **+32.5%** |
| 2025Q2 | 18 | +68.8 | +2.3% |
| 2025Q3 | 18 | +582.4 | +19.9% |
| 2025Q4 | 15 | -94.0 | -3.2% |
| **2026Q1** | 18 | **+1,370.3** | **+46.7%** |
| 2026Q2 | 16 | +493.4 | +16.8% |

**2025Q1 + 2026Q1 두 분기(8개 분기 중 2개, 25%)가 OOS 순익의 79.2%**를 차지한다. 2024Q3·Q4·
2025Q4 3개 분기는 순손실. 8개 분기 중 5개가 흑자이나 이익의 크기가 극히 불균등하다.

## 결과 9 — 파라미터 스윕 (IS/OOS 병기)

| 변형 | IS n | IS PF | OOS n | OOS PF | OOS t |
|---|---:|---:|---:|---:|---:|
| base(20,0.3,20/50,3.0/1.5,20d) | 130 | 0.973 | 133 | 1.423 | +1.565 |
| corr_window=15 | 155 | 1.180 | 145 | 1.123 | +0.550 |
| corr_window=40 | 70 | 1.306 | 97 | 1.189 | +0.668 |
| rho_th=0.2 | 190 | 1.092 | 190 | 1.165 | +0.818 |
| rho_th=0.45 | 57 | 0.923 | 69 | 1.273 | +0.822 |
| ema_fast=30 | 110 | 0.952 | 125 | 1.116 | +0.471 |
| ema_slow=80 | 116 | 0.989 | 128 | 1.402 | +1.481 |
| chandelier=2.0 | 157 | 0.698 | 163 | 1.235 | +1.050 |
| chandelier=4.0 | 126 | 0.917 | 127 | 1.226 | +0.938 |
| sl_mult=1.0 | 163 | 1.112 | 163 | 1.371 | +1.447 |
| sl_mult=2.5 | 105 | 1.017 | 119 | 1.073 | +0.308 |
| max_hold=45 | 111 | 1.054 | 124 | 1.291 | +1.050 |

**혼재된 지형**: OOS PF는 12개 변형 전부 1.0을 상회(1.073~1.423)해 "인접 변형에서 PF가 1 밑으로
붕괴"하는 과거 전형적 FAIL 패턴은 아니다 — 이 점은 이 전략의 유일한 긍정적 강건성 신호다. 그러나
**OOS t는 12개 변형 전부 +1.565 이하로, 단 하나도 유의수준(1.96)에 도달하지 못한다.** 반면 IS PF는
절반 가까이(base, ema_fast=30, ema_slow=80, chandelier=2.0/4.0, rho_th=0.45) 1.0 미만이거나
근접해, **IS는 전반적으로 약하고 OOS만 우호적인 패턴이 파라미터 전반에 걸쳐 반복**된다. 이는
"게이트의 정보가 특정 파라미터에서만 작동"이라기보다 "OOS 구간(2024-07~2026-06) 자체가 이
계열 전략에 전반적으로 우호적이었을 가능성"을 시사한다(§11 게이트없음 대조군도 참고).

## 결과 10 — 반전 대조군 (청산조건도 최종방향 참조, holding_bars 재확인)

반전모드 holding_bars min=1(정방향과 동일 — 구조상 0 불가는 전술한 대로 이 엔진의 일반 속성이며,
반전모드에서 별도 청산조건 분기가 없어 진짜 방향 대칭성이 보장됨. §재현용 코드 참조).

| 구간 | n | PF_gross | PF_net | t | 승률 | 순손익 |
|---|---:|---:|---:|---:|---:|---:|
| FULL | 247 | — | 1.171 | +0.995 | 38.5% | +2,426.9 |
| IS | 117 | — | **1.375** | +1.430 | 44.4% | +2,298.2 |
| **OOS** | 130 | — | **1.016** | +0.070 | 33.1% | +128.7 |

**OOS 에서는 정방향(1.423)이 반전(1.016)을 뚜렷이 능가**해 방향에 어느 정도 정보가 있다는
정황을 보이지만, **IS 에서는 반대로 반전(1.375)이 정방향(0.973)을 능가**한다 — 방향성 우위가
IS/OOS 에서 일관되지 않는다. 이는 "게이트+EMA 방향 로직 자체의 지속적 엣지"보다 "각 구간의
시장 국면(추세/역추세)에 따라 우연히 유리한 방향이 바뀐 것"일 가능성을 배제하지 못한다.

## 결과 11 — 핵심 대조군: 게이트없음(순수 EMA) vs self-OI 부호 vs 채택(corr)

| 변형 | 구간 | n | PF_net | R-PF | t |
|---|---|---:|---:|---:|---:|
| **gated(corr, 채택)** | OOS | 133 | **1.423** | **1.424** | +1.565 |
| ungated(순수 EMA, 대조군①) | OOS | 380 | 1.055 | 1.053 | +0.402 |
| gated(oi_sign, 대조군②) | OOS | 304 | 1.005 | 1.010 | +0.038 |

**스펙의 사전 폐기조건 (a) — "게이트가 게이트없음 대조군보다 우수해야 함"은 충족된다**: 채택안
(R-PF 1.424)이 게이트없음(1.053)과 self-OI부호(1.010) 양쪽을 뚜렷이 상회한다. 다만 §14의
검정력 보정 결과(아래) 이 우위가 통계적으로 확정적이지는 않다.

## 결과 12 — 무비용(fee=0·slippage=0) 진단

| 변형 | 구간 | n | PF |
|---|---|---:|---:|
| gated(corr) 무비용 | OOS | 133 | 1.466 |
| gated(corr) 무비용 | IS | 129 | 1.019 |
| ungated 무비용 | OOS | 380 | 1.089 |
| ungated 무비용 | IS | 445 | 1.099 |

gross(1.466)와 net(1.423)의 격차가 작아(-0.043) **스펙의 "저빈도라 비용부담 미미" 주장은 실측
확인**된다(수수료가 결론을 좌우하지 않음 — 문제는 비용이 아니라 신호 자체의 통계적 불확실성).
IS는 무비용에서도 1.019로 사실상 무의미해 IS 약세가 비용 문제가 아님도 확인된다.

## 결과 13 — 셔플 대조군: 게이트 발화율이 우연 수준을 넘는가 (창내 셔플 100회, 벡터화)

| 종목 | 실제 ON비율 | 셔플 평균(std) | 백분위 |
|---|---:|---:|---:|
| BTC | 24.65% | 9.74%(0.64%p) | 100.0%ile |
| ETH | 32.41% | 9.75%(0.73%p) | 100.0%ile |
| BNB | 17.01% | 9.54%(0.73%p) | 100.0%ile |
| SOL | 24.41% | 9.75%(0.74%p) | 100.0%ile |
| XRP | 19.16% | 9.64%(0.64%p) | 100.0%ile |
| DOGE | 23.41% | 9.65%(0.78%p) | 100.0%ile |
| ADA | 20.52% | 9.71%(0.79%p) | 100.0%ile |

**스펙의 사전 폐기조건 (c) — "셔플과 구분 불가하면 게이트를 노이즈로 판정, FAIL"은 충족되지
않는다**: 7종목 전부 실제 게이트 ON 비율이 창내 랜덤 셔플(20일 창 내부에서만 Δfunding 재배열,
n=100회) 대비 명확히 높다(약 2배, 100번째 백분위). 즉 ΔOI%와 Δfunding의 "시간 정렬"이 무의미한
우연이 아니라 통계적으로 실재하는 구조를 반영한다 — 다만 §1에서 확인했듯 그 관계의 **평균 강도
자체는 약하다**(전체 상관 0.035).

## 결과 14 — 표본수 맞춘 부트스트랩 + 중복없는 독립검정 (gated vs ungated, OOS)

- `P(PF(gated) > PF(ungated 랜덤서브샘플, n=133 맞춤))` = **0.909**(n_boot=2,000) — gated가
  ungated보다 나을 사후확률이 91%로 상당히 우호적이나 95% 확정선에는 못 미친다.
- gated OOS PF 95%CI = (0.933, 2.144), ungated(전체 380건) OOS PF 95%CI = (0.807, 1.359) —
  두 CI가 넓게 겹친다.
- **⚠️ gated·ungated 트레이드 진입시점 중복 = 72/133(54%)** — base가 pool에 상당 부분 포함돼
  (`base ⊆ pool` 성격) 위 매칭 부트스트랩만으로는 검정력이 과대평가될 수 있다는 신규 규칙에
  해당 → **중복 없는 독립 표본**(ungated 380건에서 gated와 겹치는 진입시점 제거, n=308)으로
  Welch t-검정 재실행:
  - R 기준: **t=+1.654, p=0.0994**(5% 유의수준 미달, 10%에는 근접)
  - pnl$ 기준: t=+1.644, p=0.1015
- **OOS(gated) 자체의 t-검정**: t=+1.565, df=132, **p=0.1199**(비유의)

세 가지 검정(matched 부트스트랩·독립 Welch·자체 t-검정) 모두 **"방향은 우호적이나 5% 유의수준을
넘지 못한다"**는 동일한 결론으로 수렴한다.

## 결과 15 — 룩어헤드 절단감사

BTC 1d 데이터를 3개 지점(cp=567/851/1135, 전체 1703봉 중)에서 절단 후 게이트·rho 재계산 →
절단 10봉 이전 구간에서 원본과 **완전 일치**(`gate_on` 불일치 0건, `rho` 최대오차 0.00e+00,
3개 지점 전부). 신호 확정 타이밍(day d 값은 day d+1부터 가용, `merge_asof(direction='backward')`)이
구조적으로 미래 데이터를 참조할 수 없음을 확인.

## 결과 16 — IS+OOS == FULL 확인

`IS(130) + OOS(133) = 263 = FULL(263)` — 정확히 일치(IS_END 23:59:59 명시로 경계 사각지대
없음 확인).

## 결과 17 — 회계 정합

net pnl 합계(워밍업 포함 전체기간) = 2,819.61, 무비용(gross) pnl 합계 = 3,427.79(격차가 수수료
총액과 대체로 부합). **트레이드 수가 net 267건 vs gross 266건으로 1건 차이** — fee_zero 시뮬레이션은
슬리피지=0이라 SL 트리거 가격이 미세하게 달라져 후속 트레이드 경로가 갈라질 수 있는 예상된
부작용(같은 신호 집합에서 파생된 것이라 결론에 영향 없음, 1/267=0.37%).

## 결과 18 — 비용 감당 산술

OOS 평균 R(net)=0.218/트레이드, 거래빈도 9.52건/년/종목(OOS 구간 기준). 왕복비용 0.14%는
SL거리(ATR22×1.5)·챈들리어 목표(ATR22×3.0) 대비 작아 스펙의 "저빈도·저비용부담" 주장과 부합
(§12에서 실측 확인) — **이 전략이 FAIL 하는 이유는 비용 잠식이 아니라 신호 자체의 통계적
불확실성과 구조적 취약성이다.**

## 결과 19 — 종목별 IS/OOS 세부 (신규 표, SOL 의존도 확인용)

| 종목 | IS n | IS PF | OOS n | OOS PF | OOS t | OOS 순손익 |
|---|---:|---:|---:|---:|---:|---:|
| BTC | 18 | 2.020 | 18 | 1.296 | +0.377 | 299.0 |
| ETH | 26 | 0.693 | 22 | 1.394 | +0.578 | 514.5 |
| BNB | 17 | 1.233 | 21 | 1.659 | +0.854 | 680.6 |
| **SOL** | 16 | 1.189 | 23 | **2.490** | +1.752 | **1,602.5** |
| XRP | 19 | 0.629 | 16 | 0.958 | -0.062 | -29.6 |
| DOGE | 23 | 0.437 | 15 | 0.859 | -0.271 | -114.0 |
| ADA | 11 | 1.448 | 18 | 0.980 | -0.037 | -19.7 |

**7종목 중 3종목(XRP·DOGE·ADA, 43%)은 OOS PF < 1.0** — "종목 간 일관성"이 약하다. **SOL 단독이
OOS 순익 2,933.4 중 1,602.5(54.6%)를 차지**해, §6의 LOO 결과(SOL 제외 시 PF/t 최대 하락)와
정합적으로 **단일 종목(SOL) 의존이 이 전략 순익의 절반 이상을 설명**한다. IS 에서도 종목별
PF가 0.44(DOGE)~2.02(BTC)로 크게 요동해 안정적인 범-종목 엣지로 보기 어렵다.

## 종합 판단: **FAIL**

### 스펙의 사전 등록된 폐기조건 대조

- **(a) 게이트 있음이 게이트없음 대조군보다 우수해야 함** → **충족되지 않아 FAIL 사유 아님**
  (§11: gated R-PF 1.424 > ungated 1.053 > oi_sign 1.010).
- **(b) OOS PF(R) < 1.15 또는 t 비유의 → FAIL** → **"t 비유의" 절이 충족되어 FAIL**
  (§3·§14: OOS PF(R)=1.424≥1.15 이지만 t=+1.565, p=0.120으로 유의수준 미달. matched
  부트스트랩·독립 Welch 검정도 전부 p>0.05).
- **(c) 셔플 대조군과 구분 불가 → FAIL** → **충족되지 않아 FAIL 사유 아님**
  (§13: 실제 게이트 ON 비율이 7종목 전부 셔플 대비 100번째 백분위).
- **(d) LOO 메이저 단일종목 의존 → FAIL** → **강하게 충족**(§6·§19: SOL 하나가 OOS 순익의
  54.6%를 차지, SOL 제외 시 PF 1.423→1.227·t 1.565→0.818로 가장 크게 하락. SOL은
  `major_bases`에 속한 메이저 종목).

**4개 폐기조건 중 (b)와 (d) 두 가지가 명확히 충족**된다. (b)는 스펙이 명시한 "또는" 조건이라
PF 수치(1.423)가 표면상 통과선(1.3)을 넘어도 그 자체로 FAIL을 확정하며, (d)는 이를 추가로
뒷받침한다(SOL 없이는 통과선에 근접조차 못함: PF 1.227, t 0.818).

### FAIL 이 아니라고 볼 수도 있는 긍정 근거(참고용, 결론을 뒤집기엔 부족)

1. 게이트가 대조군(게이트없음·self-OI부호) 대비 R-배수 기준 확실히 우수(§11).
2. 게이트 발화율이 순수 통계적 우연(셔플)과 명확히 구분됨(§13) — 정의 결함이나 동어반복이
   아니다.
3. 파라미터 스윕 12변형 전부 OOS PF>1.0으로, 특정 파라미터에서만 반짝이는 유형은 아니다(§9).
4. 룩어헤드·회계정합·IS+OOS=FULL·데이터 0-fill 결함 전부 확인·수정 완료 — 계산 자체의
   신뢰도는 확보됐다.

### FAIL 로 판정하는 결정적 근거

1. **스펙 자신이 사전 등록한 (b) 조건("t 비유의 → FAIL")이 정확히 충족**된다 — OOS 133건이라는
   충분한 표본에도 불구하고 p=0.120으로 5% 유의수준에 크게 못 미친다.
2. **top-5(전체의 3.8%) 트레이드 제거만으로 OOS PF가 1.423→1.037(사실상 손익분기)로 붕괴**(§7).
3. **OOS 순익의 79.2%가 8개 분기 중 2개 분기(2025Q1+2026Q1)에 집중**(§8).
4. **OOS 순익의 54.6%가 7종목 중 1종목(SOL)에서 나오며**, 3/7 종목은 OOS PF<1.0으로 종목 간
   일관성이 약하다(§19) — 스펙의 사전 폐기조건 (d)에 해당.
5. IS 는 net PF 0.973(사실상 손익분기~소폭손실)로 약하고, 이 패턴이 파라미터 스윕 전반에
   반복돼(§9) OOS 만의 우호적 결과가 게이트의 지속적 정보력이라기보다 **해당 OOS 구간
   (2024-07~2026-06)의 시장 국면 자체가 이 계열의 눌림목 추세추종에 우호적이었을 가능성**을
   배제하지 못한다.
6. 독립(중복없는) Welch 검정(p=0.099)·자체 t-검정(p=0.120)·표본크기 맞춘 부트스트랩(91%
   사후확률) 세 가지 서로 다른 방법 전부 "방향은 우호적이나 통계적으로 확정할 수 없다"는
   동일 결론에 수렴한다(§14).

**결론: 표본은 판정에 충분하나(OOS n=133≥20), 스펙 자신이 사전 등록한 통계적 유의성 기준을
충족하지 못하고, 소수 트레이드·소수 분기·단일 종목(SOL)에 대한 의존이 뚜렷해 재현 가능한 엣지로
보기 어렵다. 표면적 PF 수치(1.423)에 현혹되지 않고 사전 등록된 폐기조건을 그대로 적용해 FAIL로
판정한다. 라이브 미반영을 권고한다.**

---

## 재현용 핵심 코드 (워크트리 소멸 대비 전문 인용)

### 1) 데이터 로더 — 0-fill 결측 필터, ns 단위 고정 (`load.py` 핵심부)

```python
@functools.lru_cache(maxsize=None)
def load_klines(sym: str, tf: str) -> pd.DataFrame:
    path = os.path.join(DATA, f"{sym}_{tf}.csv")
    df = pd.read_csv(path)
    df = df.drop_duplicates(subset="open_time").sort_values("open_time")
    # ns 로 명시 통일(ms 인덱스 + Timedelta 덧셈 시 us 로 조용히 업캐스트되는
    # pandas 3.0.5 함정 방지 — 과거 여러 백테스트에서 재발한 함정, 전 인덱스 ns 로 고정).
    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms").astype("datetime64[ns]")
    df = df.set_index("open_time")
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = df[c].astype(float)
    return df[["open", "high", "low", "close", "volume"]]


@functools.lru_cache(maxsize=None)
def load_oi_daily(sym: str) -> pd.Series:
    """일별 대표 OI: 그 캘린더일 metrics 파일의 마지막 관측치(23:55 근방).
    day d 값은 day d 의 klines 종가와 동일 시점(=day d+1 00:00 UTC)에 확정되므로
    파이프라인 일반 관례(shift(1)로 다음 봉 진입)와 정합적으로 사용 가능."""
    files = sorted(glob.glob(os.path.join(METRICS, f"{sym}_*.csv")))
    dates, vals = [], []
    for fp in files:
        if os.path.getsize(fp) == 0:
            continue  # 404/badzip 마킹
        date_str = os.path.basename(fp)[len(sym) + 1: -4]
        d = dt.date.fromisoformat(date_str)
        df = pd.read_csv(fp)
        if df.empty or "sum_open_interest" not in df.columns:
            continue
        df = df.dropna(subset=["sum_open_interest"])
        # 0-fill 결측 placeholder 제외(실측 발견: 2022-03-07·2024-07-09~15 등 특정
        # 5분 스냅샷이 결측 대신 리터럴 0 으로 채워짐 — isna() 로 안 잡히므로 명시 필터).
        df = df[df["sum_open_interest"] > 0]
        if df.empty:
            continue
        dates.append(pd.Timestamp(d)); vals.append(float(df["sum_open_interest"].iloc[-1]))
    s = pd.Series(vals, index=pd.DatetimeIndex(dates).astype("datetime64[ns]")).sort_index()
    return s[~s.index.duplicated(keep="last")]
```

### 2) 신호·게이트 계산 (`strat.py` — `build_daily_frame`)

```python
@functools.lru_cache(maxsize=None)
def build_daily_frame(sym, corr_window=20, rho_th=0.3, ema_fast=20, ema_slow=50, atr_period=22):
    d1 = L.load_klines(sym, "1d")
    oi, fr = L.load_oi_daily(sym), L.load_funding_daily(sym)
    df = d1.copy()
    df["ema_fast"], df["ema_slow"] = ind.ema(df["close"], ema_fast), ind.ema(df["close"], ema_slow)
    df["atr"] = ind.atr(df, atr_period)
    df["oi"], df["fundsum"] = oi.reindex(df.index), fr.reindex(df.index)
    df["doi_pct"] = df["oi"] / df["oi"].shift(1) - 1.0
    df["dfund"] = df["fundsum"] - df["fundsum"].shift(1)
    # pandas.corr() pairwise -- np.corrcoef 의 dropna 미흡 오염 방지 규약 준수
    df["rho"] = df["doi_pct"].rolling(corr_window).corr(df["dfund"])
    df["gate_on"] = df["rho"] >= rho_th
    pb = 0.015
    long_trend, short_trend = df["close"] > df["ema_slow"], df["close"] < df["ema_slow"]
    long_pb = (df["low"] <= df["ema_fast"] * (1 + pb)) & (df["close"] > df["ema_fast"])
    short_pb = (df["high"] >= df["ema_fast"] * (1 - pb)) & (df["close"] < df["ema_fast"])
    df["long_sig"] = df["gate_on"] & long_trend & long_pb
    df["short_sig"] = df["gate_on"] & short_trend & short_pb
    return df
```

### 3) 체결 타이밍 정렬 + 진입/청산 루프 (`strat.py` — `simulate` 핵심부)

```python
avail = sig.copy()
avail.index = avail.index + pd.Timedelta(days=1).as_unit("ns")  # day d 값은 d+1 00:00 부터 가용
merged = pd.merge_asof(d4.reset_index(), avail.reset_index(),
                       left_on="open_time", right_on="open_time", direction="backward")
...
for i in range(warmup, n):
    if pos is not None:
        is_long = pos["direction"] == "long"          # 반전모드에서도 '최종 방향'을 그대로 참조
        if is_long:
            pos["run_ext"] = max(pos.get("run_ext", high[i]), high[i])
            trail_stop = pos["run_ext"] - chandelier_mult * pos["atr_at_entry"]
            stop_eff = max(pos["sl"], trail_stop)      # SL 과 챈들리어 중 더 타이트한 쪽
            if low[i] <= stop_eff: exit_now, reason = stop_eff, "chandelier_or_sl"
        else:
            pos["run_ext"] = min(pos.get("run_ext", low[i]), low[i])
            trail_stop = pos["run_ext"] + chandelier_mult * pos["atr_at_entry"]
            stop_eff = min(pos["sl"], trail_stop)
            if high[i] >= stop_eff: exit_now, reason = stop_eff, "chandelier_or_sl"
        if exit_now is None and (i - pos["entry_i"]) >= max_hold_bars:
            exit_now, reason = close[i], "time_exit"
        if exit_now is not None:
            fpx = fill(exit_now, pos["direction"], True)
            pnl = (fpx - pos["entry_px"]) * pos["qty"] if is_long else (pos["entry_px"] - fpx) * pos["qty"]
            pnl -= fee(fpx * pos["qty"]) + pos["entry_fee"]     # 진입+청산 수수료 전부 반영
            equity += pnl; pos = None
    if pos is None:
        want_long, want_short = long_s[i], short_s[i]
        if reverse: want_long, want_short = short_s[i], long_s[i]   # 원신호가 아닌 최종방향 결정
        direction = "long" if want_long else ("short" if want_short else None)
        if direction and atr_v[i] > 0:
            entry_px = fill(open_[i], direction, False)
            sl_dist = sl_mult * atr_v[i]
            sl = entry_px - sl_dist if direction == "long" else entry_px + sl_dist
            risk_amount = equity * RISK_PCT
            qty = risk_amount / sl_dist
            notional, max_notional = entry_px * qty, equity * LEVERAGE
            if notional > max_notional:
                scale = max_notional / notional; qty *= scale; risk_amount *= scale
            if qty > 0:
                pos = dict(direction=direction, entry_i=i, entry_px=entry_px, qty=qty, sl=sl,
                          atr_at_entry=atr_v[i], run_ext=None, risk_amount=risk_amount,
                          entry_fee=fee(entry_px * qty))
```

### 4) 셔플 대조군 (벡터화, `analyze.py` — `shuffle_gate_validity`)

```python
doi_w = np.lib.stride_tricks.sliding_window_view(doi, W)     # (n-W+1, W) 슬라이딩 창
fund_w = np.lib.stride_tricks.sliding_window_view(dfund, W)
for k in range(n_shuffle):
    order = np.argsort(rng.random(fund_w.shape), axis=1)      # 창별 독립 무작위 순열
    fund_shuf = np.take_along_axis(fund_w, order, axis=1)
    r = _rowwise_corr(doi_w, fund_shuf)                        # 벡터화 행별 피어슨 상관
    shuffle_rates[k] = ((r >= rho_th) & valid)[valid].mean()
```
