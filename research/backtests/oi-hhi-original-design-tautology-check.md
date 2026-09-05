# [진단] OI 크로스섹셔널 HHI — 원본 설계(동적 20종목·365일 백분위)에서도 폐기조건 (b) 성립하는지 확인

- **대상 스펙**: `research/strategies/oi-cross-sectional-herfindahl-concentration-breadth-btc-trend-swing.md`
  (커밋 `9ea4001`)
- **배경**: 직전 백테스트가 워크트리 생성 시점 문제로 스펙을 못 찾고 고정 7종목·60일 z-score·
  ±0.75σ·BTC 1d종가/EMA50 설계로 **재작성**해 돌았고, 그 재작성 설계에서는 사전 등록 폐기조건 (b)
  (HHI와 BTC 단독 점유율 상관 |r|>0.8 → 재포장 폐기)가 전체구간 0.875·트리거 시점 0.893으로
  **충족**돼 FAIL이 권고됐다. 원본 스펙이 실제로 요구한 설계(동적 20종목 유니버스, 롤링 365일
  백분위, BTC 4h EMA20/50 크로스)에서도 같은 결론인지는 검증되지 않은 상태였다. 본 진단은 그
  하나만 확인한다(전체 백테스트 아님).

## 1. 동적 20종목 유니버스 구성

- **후보 풀**: 58종목(기존 7종목 + 대형·중형 알트 33종 + 신규 내러티브 알트 15종 + 밈코인 3종).
  밈코인은 Binance 선물 계약명이 `1000SHIBUSDT`/`1000PEPEUSDT`/`1000BONKUSDT`(1000배 표기)임을
  HTTP 200/404 실측으로 확인 후 그 이름으로 다운로드했다(`SHIBUSDT` 단독명은 전부 404).
- **선정 방법**(스펙 정의 그대로): 매일 00:00 UTC, **직전일(D-1)** 24h 거래대금(`quote_volume`,
  1d klines) 기준 상위 20종목(그 중 $10M 이상만 후보, 봇 동적 유니버스 정의와 동일 기준). D일의
  1d 봉은 D 거래 중에만 확정되므로 D일 유니버스 선정에 D일 자신의 값을 쓰면 룩어헤드 —
  **반드시 D-1 값을 causal 하게 사용**(`common.py`의 `qv.shift(1)`).
  종목 배제는 후보 풀 다운로드 로그(`klines_pool_missing.log`)의 실측 200/404로만 판정했고,
  "데이터가 없어서 제외"를 임의로 가정하지 않았다(과거 사례 경고 반영).
- **실측 결과**: 58종목 **전부** 한 번 이상 top20에 진입했다(제외된 후보 0건). 일자별 유효
  유니버스 크기는 평균 19.99(표준편차 0.48) — 거의 항상 정확히 20종목이 채워진다(데이터 부재로
  20종목 미만인 날은 극초기[2021-10~11] 뿐).
- **시점별 구성 변화**(연초 스냅샷):
  - 2022-01-01: SHIB·AAVE·ADA·ALGO·ATOM·AVAX·BNB·BTC·DOGE·DOT·ETH·**FTM**·GALA·LINK·MANA·
    **MATIC**·NEAR·SAND·SOL·XRP
  - 2023-01-01: ADA·ALGO·**APT**·ATOM·AXS·BNB·BTC·CHZ·DOGE·DOT·**DYDX**·ETC·ETH·FIL·LINK·LTC·
    MATIC·SOL·TRX·XRP
  - 2024-01-01: ADA·**ARB**·AVAX·BCH·BNB·BTC·DOT·ETH·FIL·**ICP**·**INJ**·LINK·MATIC·NEAR·
    **OP**·**ORDI**·**SEI**·SOL·**WLD**·XRP
  - 2025-01-01: **BONK**·**PEPE**·SHIB·AAVE·ADA·AVAX·BNB·BTC·DOGE·ETH·**HBAR**·LINK·LTC·
    **ONDO**·SOL·**SUI**·**UNI**·**WIF**·WLD·XRP
  - 2026-01-01: PEPE·AAVE·ADA·AVAX·BCH·BNB·BTC·CHZ·DOGE·ETH·FIL·LINK·LTC·NEAR·SOL·SUI·UNI·
    WIF·WLD·XRP
  - 확인: 2022→2026 사이 신규 진입(**굵게** 표기 종목 예시)만 봐도 FTM·MATIC(2022)이 빠지고
    ORDI·SUI·WIF·PEPE·BONK 같은 2023~2025 신규 내러티브·밈코인이 들어오는 등, 원본 스펙이 우려한
    "고정 유니버스의 구조적 노후화"(과거 백테스트에서 실측 확인된 문제)를 이 동적 구성이 실제로
    해소하고 있음을 확인했다.
- **데이터 결측**: OI 명목가치(HHI 계산)에 쓴 metrics 5분 덤프는 58종목 합산 74,937건 요청 중
  2,726건(3.6%) 404 — 대부분 각 종목의 futures 상장 초기 두 달 내외(예: FTM 538건, ICP 336건)에
  집중돼 있고, 이는 과거 여러 백테스트에서 반복 관측된 "metrics 덤프가 상장 초기 구간에서
  부분 결측"과 일관된 패턴이다(구조적 결함이 아님). 유니버스 대비 그 날 실제 OI를 확보한 멤버
  비율은 평균 96.6%(결측 3.4%)이고, 멤버 절반 미만만 OI가 확보된 날(2021-10~11, 61일)은 HHI
  계산에서 제외했다 — 이 구간은 어차피 365일 롤링 백분위의 워밍업 구간(첫 유효 백분위는
  1583/1734일)이라 본 진단 결과에 영향 없다.

## 2. HHI·BTC 점유율 신호 구축

- **HHI(t)**: 그 날 top20 멤버(동적)의 OI 명목가치(`sum_open_interest × close`) 점유율 제곱합.
- **정규화**: 롤링 **365일** 창 기준 백분위(`common.rolling_pctile`, min_periods=91일).
- **BTC 단독 점유율**: 같은 날 같은 20종목 유니버스 내에서 `OI_BTC / Σ OI(top20)`, 동일하게
  365일 롤링 백분위로도 계산(비교 대상).
- 룩어헤드 방지: `metrics.create_time`(문자열)을 `unit` 미지정 없이 `format="%Y-%m-%d %H:%M:%S"`로
  명시 파싱하고, 모든 인덱스를 `.as_unit("ns")`로 통일해 실제 dtype을 출력 확인했다(전부
  `datetime64[ns, UTC]` — ms/us 혼재 없음). 1d OI 값은 `resample("1D",label="left",closed="left")
  .last()`로 "그 날 마감 시점까지의 정보"를 그 날 라벨에 담고, BTC 4h 트리거 게이트일 매핑에서
  **캘린더일 - 1일**을 사용해(원본 재작성 스크립트의 `gate_days = cross_days - 1` 패턴과 동일 논리)
  트리거 발생일 자신의 미확정 정보를 참조하지 않게 했다.

## 3. 상관·부분집합 결과

`pandas.corr()`(pairwise) 사용 — `np.corrcoef`는 잔여 NaN에 오염되므로 배제(과거 프로젝트 규칙).

| 구간 | n | 상관(백분위 기준) | 상관(원값 기준) |
|---|---|---|---|
| 전체 구간 | 1,583 | **r = 0.8685** | r = 0.7971 |
| BTC 4h EMA20/50 크로스 트리거 시점 한정 | 173 / 190 | **r = 0.8232** | r = 0.7197 |

- BTC 4h EMA20/50 크로스 이벤트 총 190건(golden 95·death 95) 중 게이트일(트리거일-1일) 데이터가
  유효한 173건으로 상관을 계산했다.
- **게이트 발화 시점 부분집합 비율**(원본 스펙 임계 lo=30%ile/hi=70%ile 사용):
  - HHI 분산레짐(≤30%ile) 발화일 413일, BTC점유율 분산레짐 발화일 508일 →
    HHI 분산 ⊆ BTC점유율 분산 **93.70%**, 역방향(BTC점유율 분산 ⊆ HHI 분산) 76.18%.
  - HHI 집중레짐(≥70%ile) 발화일 640일, BTC점유율 집중레짐 발화일 511일 →
    BTC점유율 집중 ⊆ HHI 집중 **88.45%**, 역방향(HHI 집중 ⊆ BTC점유율 집중) 70.63%.
  - 양쪽 극단(분산+집중) 합집합 기준 상호 부분집합 비율 80.5%/83.2%.
  - 재작성 설계에서 관측된 "100% 완전 부분집합"만큼 극단적이지는 않지만, 70~94% 범위로
    **강한 겹침**이며 스펙이 (b)의 판정 기준으로 삼은 것은 상관계수이지 부분집합 비율이
    아니므로 이 수치는 보조 참고용이다.

## 4. 사전 등록 폐기조건 (b) 판정

> (b) HHI와 BTC 단독 점유율의 상관 |r| > 0.8이면 **재포장으로 폐기**(동어반복)

- 전체구간(백분위 기준) |r| = **0.8685 > 0.8 → 충족(폐기)**
- 트리거 시점 한정(백분위 기준) |r| = **0.8232 > 0.8 → 충족(폐기)**
- 원값 기준으로도 0.72~0.80으로 0.8에 근접하거나(트리거 시점은 0.8 미만이지만 백분위 기준이
  스펙이 실제로 쓰는 정규화 방식이라 그쪽이 판정 기준).

**결론: 원본 설계(동적 20종목 유니버스 + 롤링 365일 백분위 + BTC 4h EMA20/50 크로스)에서도
폐기조건 (b)가 충족된다.** 재작성판(고정 7종목·60일 z-score, |r|=0.875/0.893)과 방향·수준
모두 일관되게, "유니버스를 동적 20종목으로 넓히고 정규화 창을 365일로 늘리면 BTC 점유율과
독립적인 정보가 될 것"이라는 원본 스펙의 반박 가설은 지지되지 않는다. BTC·ETH가 유니버스에서
구조적으로 최대 비중을 차지하는 한, 유니버스를 넓히거나 정규화 방식을 바꿔도 HHI는 여전히
"BTC(+ETH) 점유율의 변형"에서 크게 벗어나지 못하는 것으로 보인다.

**권고**: 원본 설계로 전체 백테스트를 다시 돌릴 필요는 없다 — 스펙 자신이 사전 등록한 재포장
기준을 원본 설계에서도 충족하므로, 이 아이디어는 (재작성판과 마찬가지로) **동어반복으로 폐기**가
타당하다.

## 5. 재현 커맨드

```bash
# 스크래치 디렉터리(SP)에 기존 7종목 klines_1d/4h·metrics 캐시를 심볼릭 링크로 재사용
SP=/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad
mkdir -p $SP/oihhi_orig/data/{klines_1d,klines_4h,metrics}
for f in $SP/oihhi/data/klines_1d/*; do ln -sf "$f" $SP/oihhi_orig/data/klines_1d/$(basename "$f"); done
for f in $SP/oihhi/data/klines_4h/*; do ln -sf "$f" $SP/oihhi_orig/data/klines_4h/$(basename "$f"); done
for f in $SP/oihhi/data/metrics/*;   do ln -sf "$f" $SP/oihhi_orig/data/metrics/$(basename "$f"); done

# 후보 풀 51종목 1d klines 다운로드(월별 zip) — repro/ 디렉터리의 스크립트 참고해 재현
bash research/backtests/repro/oi-hhi-original-design-tautology-check/dl_klines_pool.sh
bash research/backtests/repro/oi-hhi-original-design-tautology-check/dl_klines_pool_meme.sh

# top20 진입 종목의 OI metrics(5분, 일별 zip) 다운로드
python3 research/backtests/repro/oi-hhi-original-design-tautology-check/gen_metrics_jobs.py \
  > /tmp/metrics_jobs.txt
bash research/backtests/repro/oi-hhi-original-design-tautology-check/dl_metrics_pool.sh /tmp/metrics_jobs.txt

# 진단 실행
cd research/backtests/repro/oi-hhi-original-design-tautology-check
python3 analyze.py
```

## 6. 한계·주석

- 후보 풀 58종목은 "역사상 실제 top20"을 완벽히 재현하지 못할 수 있다 — 우리가 놓친 초단명·
  극소형 알트가 특정 시기 거래대금 급증으로 진짜 top20에 잠깐 들었을 가능성은 배제 못 한다.
  다만 후보 풀이 시총 상위·장기 상장·주요 밈코인/신규 내러티브 코인을 폭넓게 포괄해, 실제
  top20 구성과 크게 어긋날 개연성은 낮다고 판단한다(연도별 스냅샷이 알려진 시장 서사와 일치).
- BTC 4h EMA20/50 크로스는 스펙의 "매매 신호"이지 "게이트 통과 신호"가 아니다 — (b) 판정은
  스펙 문언대로 상관계수 자체를 기준으로 하므로 트리거 필터링 여부와 무관하게 결론이 같다.
- 본 진단은 폐기조건 (b) 하나만 확인하는 것이 목적이며, 손익(PF·t값 등 (c)(d)(e)(f))은
  검증하지 않았다 — (b) 충족만으로 스펙 자체 규칙에 따라 폐기 대상이므로 그 이상의 백테스트는
  불필요하다는 것이 이 진단의 결론이다.
