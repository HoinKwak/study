# 선물시장 스카우트 브리핑 — 2026-08-19 14:30 UTC (KST 2026-08-19 23:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 12:30 UTC)로부터 2시간 경과(정상 간격).**

## ⚠️ 이번 회차 최대 이슈 — ACE 세 번째 급변: 반납 이후 뚜렷한 하락 재개

직전 회차에서 "전량 반납"으로 완전히 소멸했던 ACE가 이번 회차 4벤뉴 전부 -12~-14%대로 동조
하락했다 — 방향성 소멸이 아니라 다음 급락 국면으로의 전환이었다:

| 벤뉴 | 12:30Z | 14:30Z |
|---|---|---|
| Binance | +1.549% | **-12.62%** |
| Bybit | +1.679% | **-13.066%** |
| Hyperliquid | +2.377% | **-13.895%** |
| Aster | +4.845% | **-13.516%** |

펀딩도 재차 깊은 마이너스로 전환됐다: Binance -0.00154→**-0.00208**, Bybit -0.00144→**-0.00289**,
HL -0.00045→**-0.00065**, Aster -0.0003→**-0.00058**. ACE는 '급등→급락→재급락'을 반복하는
극단적 변동성 국면을 계속 이어가고 있다.

## 시장 전반 — 이번 회차 핵심

1. **ACE 세 번째 급변(상단 참고)** — 이번 회차 최대 이슈.
2. **KAITO 반등 스트릭이 처음으로 꺾임**: OKX +4.824%→**-1.376%**, HL +4.69%→**-0.81%**로
   두 벤뉴 모두 플러스에서 마이너스로 반전했다. Binance는 이번 회차 데이터 수집 실패로 직전값
   (+4.644%/+3.695%)을 이월해 전체 벤뉴 교차확인은 불완전하다.
3. **CASHCAT 6회차 연속 축소 흐름이 꺾임**: HL -7.121%→**-12.948%**로 낙폭이 오히려 크게
   재확대됐다. Aster는 이번 회차 fetch 결과가 무관한 'ASTON' 티커와 완전히 동일한 수치로
   반환돼 데이터 오염으로 판단, 직전값(-7.246%)을 이월했다.
4. **BTW는 Aster에서 재가속**: +67.059%→**+73.203%**로 직전 회차 '뚜렷한 냉각' 판단과 반대로
   상승폭이 확대됐다. Binance는 데이터 수집 실패로 직전값(+67.198%)을 이월해 교차확인 불완전.
5. **1000RATS는 벤뉴간 괴리 해소, 방향은 급락 쪽으로 수렴**: Binance -2.293%→**-22.254%**,
   Bybit -2.019%→**-22.249%**, (직전 플러스 유지하던) Aster +1.555%→**-22.174%**로 3벤뉴가
   거의 동일한 수준의 큰 폭 하락으로 수렴했다.
6. **APR 전 벤뉴에서 플러스→마이너스로 완전 반전**: OKX +0.962%→**-2.746%**, Bybit
   +1.678%→**-3.998%**, Binance +2.299%→**-3.619%**, Aster +0.1%→**-5.313%**.
7. **GALA·BANK·AIO·ALPINE·ETHFI**는 각각 낙폭 소폭 재확대, 보합→약세 전환, 마이너스 폭 완화,
   상승폭 축소 지속, 플러스 전환(OKX ticker 이상 해소) 흐름 — 세부 표 참고.

**⚠️ALLO OKX OI 10배 급증 건, 이번 회차로 결론**: 직전 회차($3.28M)에 이어 이번 회차도 유사
수준($3.09M, oiCcy×last 재계산)을 유지했다 — bulk 직접API 전환 이후 2회차 연속 안정적으로 같은
레벨을 유지하는 반면 '10배 이전' 기준값($0.33M)은 구 방법론(단건조회) 시절 값이다. **결론: 실제
포지션 급증이 아니라 OKX OI 수집 방법론 전환(구 단건조회→현 bulk 직접API)에 따른 일회성
계산방식 아티팩트**로 판단한다 — 이후 회차부터는 새 레벨($3.0~3.3M대)을 정상 기준선으로 삼는다.

**데이터 품질 — 이번 회차 신규 이슈**: CoinGecko `binance_futures` 티커 엔드포인트가 이번 회차
반복적으로(5회 이상, 프롬프트를 좁혀도 동일) BTW·BICO·GALA·ETHFI·CAP·AEON·GIGGLE·MMT·GRAM·
PIPPIN·BSB·KAITO(USDT/USDC 모두)를 찾지 못했다 — WebFetch 캐시가 동일 URL에 대해 잘린
(truncated) 컨텐츠를 반환하는 것으로 추정된다(BTC·ETH 같은 최상위 거래량 심볼조차 이 경로로는
못 찾았고, 별도 집계 엔드포인트 `/derivatives?include_tickers=unexpired`로 우회해서야 확인됨).
이들 심볼은 전부 직전 회차(12:30Z) 값을 이월했다(정직 표기). **BEAT의 Binance 신규 fetch 값도
직전 대비 약 240배 작은 거래량(≈$40만)이 반환돼 명백히 신뢰불가로 판단, 폐기하고 직전값을
이월**했다. 이는 기존의 '시간·호출 제약상 이월'과는 성격이 다른 **fetch 도구 자체의 페이로드
절단 이슈**로 별도 기록한다.

**OKX OI 방법론(oiCcy×last) 재검증**: 이번 회차 BICO·GALA·ETHFI·AAVE·ADA·ATOM·CAP·ASTER·
KAITO·CORE·BSB·GIGGLE 전부 직전 회차 직접 API 값과 근접(수 % 이내)해 방법론이 계속 안정적임을
재확인했다. BTC-USDT-SWAP도 참고용으로 계산(oiCcy 32,660.4×last $65,345.2≈$2.13B)해 규모가
합리적임을 확인했다.

**dYdX**: 이번 회차도 CoinGecko `dydx_v4` 엔드포인트는 시도하지 않고(상시 404로 알려짐) 공식
인덱서 `indexer.dydx.trade`로 직접 확인. BTC OI 274.8932×오라클가 $65,340.79≈**$17.96M**,
ETH OI 11,569.817×$1,934.47≈**$22.38M**, SOL OI 64,245.6×$78.4765≈**$5.04M**로 전부 완만한
변화. BTC 오라클가는 OKX last($65,345.2)·Binance 집계가($65,299.30)와 근접해 가격 신뢰도 확인.

**메이저**: HL BTC +0.357%→**+0.616%**(vol $1,708.99M, OI $2,584.22M), ETH
+1.184%→**+0.744%**(vol $1,187.49M, OI $1,790.73M); Aster BTC +0.394%→**+0.606%**(vol
$669.49M, OI $823.39M), ETH는 **20회차 연속 truncation**; Binance는 `/derivatives?
include_tickers=unexpired` 집계 경로로 확인한 결과 BTC 가격 $65,299.30(OI $7,124.17M, chg
+0.65%), ETH 가격 $1,934.51(OI $4,773.23M, chg +0.71%) — 단, 이 경로의 funding_rate 값
(0.66%·0.84%)은 기존 정상범위와 크게 어긋나 신뢰도 낮음으로 판단해 미채용(수치만 참고, funding은
결측 처리). **글로벌 시총·도미넌스는 WebSearch 재확인 결과 총 약 $2.2~2.3조·BTC 도미넌스 약
57~60%(소스별 편차)**로 직전과 대체로 유사한 범위.

**OrangeX는 38회차·약 77.75시간째 전면 중단** 지속. 저장 직전 전 항목 funding 절대값 점검 결과
최댓값 0.00289(ACE Bybit)로 직전 정상범위(최대 0.00154) 대비 소폭 상회했으나 ACE 자체가
극단적 변동성 국면이라 이례적이지 않다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

funding은 raw fraction 기준. "[이월]"은 이번 회차 CG fetch 실패로 직전값을 그대로 이어받은 필드.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **ACE** [재급락] | Binance(직접API) | $494.10M | $14.69M | -0.00208 | **-12.62%** | 세 번째 급변, 반납 이후 뚜렷한 하락 재개 |
| ACE [재급락] | Bybit(CG대체) | $110.37M | $6.39M | -0.00289 | -13.066% | 동조 하락, 펀딩 재차 깊은 마이너스 |
| BTW [이월] | Binance | $821.85M | $148.23M | 0.00129 | +67.198% | CG fetch 실패로 직전값 이월 |
| **BEAT** [재확대] | OKX(직접API) | $85.13M | $6.01M | 0.00027 | -19.04% | 낙폭 소폭 재확대 |
| BEAT [이월] | Binance | $96.21M | $10.70M | 0.00028 | -18.062% | 신규값 신뢰불가로 폐기, 직전값 이월 |
| BICO [확대] | OKX(직접API) | $12.57M | $2.49M | 0.00005 | -14.364% | 낙폭 확대(펀딩은 이월) |
| BICO [이월] | Binance | $14.11M | $5.21M | -0.00058 | -12.292% | CG fetch 실패로 직전값 이월 |
| GALA [이월] | Binance | $18.97M | $6.49M | 0.0000274 | -3.767% | CG fetch 실패로 직전값 이월 |
| GALA [재확대] | OKX(직접API) | $5.33M | $1.73M | 0.0001 | -4.594% | 낙폭 소폭 재확대, funding 직접확인 |
| ETHFI [이월] | Binance | $17.88M | $22.55M | -0.0000096 | +0.041% | CG fetch 실패로 직전값 이월 |
| **ETHFI** [플러스전환] | OKX(직접API) | $7.35M | $4.13M | -0.0000514 | +1.389% | ticker이상 해소, chg 정상 갱신 |
| CAP [이월] | Binance | $21.87M | $15.02M | -0.00007 | +0.973% | CG fetch 실패로 직전값 이월 |
| CAP [확대] | OKX(직접API) | $59.08M | $11.72M | -0.0000677 | +3.018% | 플러스권 확대 |
| AEON [등락] | OKX(직접API) | $41.81M | $3.34M | 0.00005 | -8.689% | 좁은 범위 등락(축소 흐름 내) |
| AEON [등락] | Bybit(CG대체) | $2.28M | $0.98M | 0.00005 | -8.832% | 동조 |
| APEX [진정] | Bybit(CG대체) | $1.26M | $1.74M | 0.00005 | +4.915% | 진정 흐름 내 소폭 등락 |
| GIGGLE [이월] | Binance | $15.24M | $10.97M | 0.00005 | -2.679% | CG fetch 실패로 직전값 이월 |
| GIGGLE [완화] | OKX(직접API) | $6.44M | $1.78M | 0.00005 | -0.809% | 낙폭 크게 완화, 보합권 근접 |
| ALPINE [축소] | Binance(직접API) | $68.62M | $2.01M | 0.00005 | +3.979% | 상승폭 지속 축소 |
| ALPINE [축소] | Bybit(CG대체) | $15.15M | $0.62M | 0.00005 | +3.841% | 동조 축소 |
| CORE [확대] | OKX(직접API) | $2.22M | $1.07M | 0.00008 | +3.376% | 플러스권 확대, Binance 미상장 지속 |
| ATOM [보합] | OKX(직접API) | $3.08M | $3.68M | -0.00015 | -0.356% | 소폭 마이너스 전환 |
| ATOM [보합] | Binance(직접API) | $14.29M | $15.23M | -0.00008 | -0.285% | 소폭 마이너스 유지 |
| ATOM [보합] | Bybit(CG대체) | $5.61M | $13.33M | -0.00014 | -0.285% | 동조 |
| AAVE [보합] | OKX(직접API) | $18.23M | $11.67M | 0.00002 | +0.1% | 소폭 플러스 유지 |
| AAVE [보합] | Binance(직접API) | $43.59M | $44.33M | 0.00009 | -0.323% | 소폭 마이너스 |
| AAVE [보합] | Bybit(CG대체) | $12.85M | $40.31M | 0.00008 | -0.367% | 동조 |
| ADA [전환] | OKX(직접API) | $23.24M | $25.47M | -0.00012 | -1.472% | 플러스→소폭 마이너스 전환 |
| ADA [전환] | Binance(직접API) | $75.26M | $84.43M | -0.00007 | -1.474% | 동조 전환 |
| ADA [전환] | Bybit(CG대체) | $36.26M | $55.72M | -0.00013 | -1.359% | 동조 |
| ALGO [플러스] | Binance(직접API) | $7.84M | $7.67M | 0.0001 | +2.004% | 플러스권 유지 |
| ALGO [플러스] | OKX(직접API) | $3.44M | $2.61M | 0.0001 | +2.225% | 동조 |
| MMT [이월] | OKX(직접API) | $3.33M | $2.10M | -0.00024 | -2.649% | 마이너스 지속(funding 이월) |
| MMT [이월] | Binance | $5.39M | $8.16M | -0.00009 | -2.043% | CG fetch 실패로 직전값 이월 |
| GRAM [보합] | OKX(직접API) | $3.99M | $6.38M | 0.00005 | +1.22% | 플러스권 유지(funding 이월) |
| GRAM [이월] | Binance | $8.13M | $14.12M | 0.00005 | +1.459% | CG fetch 실패로 직전값 이월 |
| PIPPIN [보합] | OKX(직접API) | $2.32M | $1.79M | 0.00005 | -0.056% | 거의 완전 보합(funding 이월) |
| PIPPIN [이월] | Binance | $4.86M | $5.70M | 0.00005 | -1.285% | CG fetch 실패로 직전값 이월 |
| BSB [전환] | OKX(직접API) | $6.15M | $2.11M | 0.00032 | -3.27% | 마이너스 전환(funding 이월) |
| BSB [이월] | Binance | $12.03M | $8.74M | 0.00011 | -1.701% | CG fetch 실패로 직전값 이월 |
| **BANK** [약세전환] | Binance(직접API) | $24.31M | $10.73M | 0.00005 | -1.947% | 보합에서 약세로 전환 |
| BANK [약세전환] | Bybit(CG대체) | $2.86M | $3.99M | 0.00005 | -1.892% | 동조 약세 전환 |
| **APR** [완전반전] | OKX(직접API) | $52.37M | $3.08M | 0.00005 | -2.746% | 플러스→마이너스 완전 반전 |
| APR [완전반전] | Bybit(CG대체) | $7.89M | $3.32M | 0.00005 | -3.998% | 동조 반전 |
| APR [완전반전] | Binance(직접API) | $49.55M | $10.69M | 0.00005 | -3.619% | 동조 반전 |
| AIO [완화] | Binance(직접API) | $15.66M | $4.00M | 0.00005 | -9.329% | 마이너스 폭 다소 완화 |
| AIO [완화] | Bybit(CG대체) | $1.61M | $1.16M | 0.00005 | -9.715% | 동조 완화 |
| ALLO [진정] | Binance(직접API) | $28.94M | $12.01M | 0.00005 | +0.286% | 플러스권 진정 지속 |
| **ALLO** [OI결론] | OKX(직접API) | $25.70M | $3.09M | 0.00005 | -0.207% | ⚠️OI 2회차 연속 유지 — 방법론 아티팩트로 결론 |
| ALLO [진정] | Bybit(CG대체) | $3.82M | $4.20M | 0.00005 | +0.034% | 동조 진정 |
| **1000RATS** [수렴] | Binance(직접API) | $76.15M | $12.75M | 0.00008 | -22.254% | 낙폭 급격히 확대, 3벤뉴 수렴 |
| 1000RATS [수렴] | Bybit(CG대체) | $28.21M | $4.70M | 0.0003 | -22.249% | 동조 급락 |
| ASTER(자체) [안정] | Binance(CG대체) | $9.46M | $70.06M | 0.00005 | -0.216% | 안정 유지 |
| ASTER(자체) [안정] | OKX(직접API) | $2.28M | $8.28M | 0.0001 | -0.15% | 동조 |
| ASTER(자체) [안정] | Bybit(CG대체) | $1.34M | $39.89M | 0.00005 | -0.216% | 동조 |
| **KAITO** [반전] | OKX(직접API) | $24.96M | $4.83M | 0.0000060 | -1.376% | 반등 스트릭 처음으로 꺾여 마이너스 전환 |
| KAITO [이월,USDT] | Binance | $33.30M | $15.03M | -0.00009 | +4.644% | CG fetch 실패, OKX·HL은 반전 확인·Binance 미확인 |
| KAITO [이월,USDC] | Binance | $3.82M | $1.14M | -0.00009 | +3.695% | CG fetch 실패로 직전값 이월 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 38회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **ACE** [재급락] | Hyperliquid | $1.59M | $1.80M | -0.00065 | -13.895% | CEX와 동조, 세 번째 급변 |
| ACE [재급락] | Aster | $0.98M | $0.19M | -0.00058 | -13.516% | 동조 하락 |
| ACE [중단] | OrangeX | — | — | — | — | 38회차·약 77.75시간 |
| **BTW** [재가속] | Aster | $10.68M | $13.08M | 0.00018 | +73.203% | 직전 냉각과 반대로 재가속 |
| **KAITO** [반전] | Hyperliquid | $2.27M | $5.78M | 0.00001 | -0.81% | 반등 스트릭 꺾이며 마이너스 전환 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **CASHCAT** [재확대] | Hyperliquid | $9.14M | $11.88M | 0.00001 | -12.948% | 6회차 연속 축소 흐름 꺾이며 낙폭 재확대 |
| CASHCAT [이월] | Aster | $0.66M | $0.71M | -0.00001 | -7.246% | fetch값 오염(ASTON과 동일) 판단, 직전값 이월 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GALA [재확대] | Hyperliquid | $1.03M | $1.10M | -0.00004 | -5.081% | 낙폭 소폭 재확대 |
| BEAT [이월] | Aster | $0.90M | $0.84M | 0.00001 | -18.182% | 이번 회차 미확인(fetch), 직전값 이월 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BICO [확대] | Aster | $0.05M | $0.10M | 0.00005 | -13.682% | 낙폭 확대 |
| BICO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| AEON [등락] | Aster | $0.08M | $0.29M | 0.00001 | -7.713% | 좁은 범위 등락 지속 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [보합] | Hyperliquid | $1.53M | $15.32M | 0.00001 | +1.358% | 플러스권 유지 |
| ATOM [보합] | Hyperliquid | $0.41M | $1.71M | -0.00001 | -0.528% | 타 벤뉴와 동조 |
| ATOM [보합] | Aster | $0.01M | $1.66M | 0.0001 | -0.289% | 동조 보합 |
| AAVE [보합] | Hyperliquid | $3.04M | $58.49M | 0.00001 | -0.464% | 타 벤뉴와 동조 |
| AAVE [보합] | Aster | $0.23M | $4.55M | 0.0001 | -0.512% | 동조 |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ADA [전환] | Hyperliquid | $2.80M | $29.14M | 0.0 | -1.371% | 플러스에서 마이너스로 전환 |
| ADA [전환] | Aster | $0.19M | $1.23M | 0.00008 | -0.968% | 동조 전환 |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALGO [플러스] | Hyperliquid | $0.41M | $1.82M | 0.00001 | +2.02% | 동조 |
| ALGO [플러스] | Aster | $0.006M | $0.04M | -0.00001 | +3.084% | 동조 |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ASTER(자체) [안정] | Aster | $8.07M | $221.38M | 0.0001 | -0.017% | 자체 OI 안정 유지 |
| ASTER(자체) [안정] | Hyperliquid | $0.20M | $13.59M | 0.00001 | -0.121% | 동조 |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| HYPE [소폭악화] | Hyperliquid | $193.76M | $1,333.47M | 0.00001 | -1.444% | 마이너스 폭 소폭 확대 |
| BLESS [완화] | Aster | $0.02M | $0.09M | 0.00016 | -7.905% | 마이너스 폭 소폭 완화 |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **BTC** [정상] | dYdX | $3.23M | $17.96M | 0.0 | +0.808% | 공식 인덱서 직접 확인 |
| **ETH** [정상] | dYdX | $6.23M | $22.38M | 0.0000197 | +1.036% | 정상 작동 확인 |
| **SOL** [정상] | dYdX | $0.22M | $5.04M | 0.0 | +1.789% | 정상 작동 확인 |
| BTC [안정] | Hyperliquid | $1,708.99M | $2,584.22M | 0.0 | +0.616% | 메이저 안정, 소폭 상승 |
| ETH [안정] | Hyperliquid | $1,187.49M | $1,790.73M | -0.00002 | +0.744% | 메이저 안정 |
| BTC [안정] | Aster | $669.49M | $823.39M | 0.00006 | +0.606% | 메이저 안정 |
| ETH [truncation 20연속] | Aster | — | — | — | — | base=ETH 항목 부재 재확인 |
| 1000RATS [수렴] | Aster | $0.44M | $0.06M | 0.00003 | -22.174% | 플러스 유지 벤뉴였으나 CEX와 동조 급락 |
| AIO [완화] | Aster | $0.06M | $0.08M | 0.00005 | -7.409% | CEX와 동조 완화 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALLO [진정] | Aster | $0.14M | $0.06M | 0.00001 | +0.542% | CEX와 동조 진정 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| APR [완전반전] | Aster | $0.24M | $0.29M | 0.00001 | -5.313% | CEX와 함께 마이너스로 완전 반전 |
| APR [미상장] | Hyperliquid | — | — | — | — | 이번 회차도 HL 미상장 재확인 |
| BANK [약세전환] | Aster | $0.10M | $0.26M | 0.00001 | -1.754% | CEX와 동조 약세 전환 |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [전환] | Aster | $0.14M | $0.13M | 0.00001 | -3.916% | CEX와 동조 마이너스 전환 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CAP [플러스] | Aster | $0.06M | $0.17M | 0.00001 | +1.438% | CEX와 함께 플러스권 유지 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| FARTCOIN [강화] | Hyperliquid | $3.86M | $31.55M | 0.00005 | +1.163% | 플러스 지속 강화 |
| ETHFI [전환] | Hyperliquid | $3.74M | $11.61M | 0.00001 | +0.784% | 마이너스에서 플러스로 전환 |
| HYPER [유지] | Hyperliquid | $0.05M | $0.20M | -0.00003 | +1.228% | 플러스권 유지 |
| APEX [진정] | Hyperliquid | $0.15M | $0.65M | 0.00001 | +5.134% | Bybit와 함께 진정 흐름 내 등락 |
| HYNA:BTC-USD | Hyperliquid | $0.31M | $2.19M | 0.00001 | +1.292% | HIP-3 빌더배포, BTC 동조 |
| HYNA:ETH-USD | Hyperliquid | $0.15M | $1.65M | 0.00001 | +2.14% | HIP-3 빌더배포, ETH 동조 |
| HYNA:HYPE | Hyperliquid | $0.15M | $0.66M | -0.00001 | -1.0% | HIP-3 빌더배포 |
| HYNA:PUMP | Hyperliquid | $0.04M | $0.16M | 0.00001 | +7.559% | HIP-3 빌더배포, 직전과 유사 |
| HYNA:SOL-USD | Hyperliquid | $0.04M | $0.54M | 0.00001 | +3.205% | HIP-3 빌더배포, 소폭 강화 |

## 테마 태그 (요약)

1. ACE 세 번째 급변 — 반납 이후 4벤뉴 동조 하락 재개 (ace-relapses-into-sharp-decline)
2. KAITO 반등 스트릭 처음으로 꺾임(OKX·HL 마이너스 전환, Binance 미확인) (kaito-rebound-streak-breaks)
3. CASHCAT 6회차 연속 축소 흐름 꺾임(HL 재확대, Aster 데이터 오염) (cashcat-decline-rewidens)
4. BTW Aster 재가속(+67%→+73%), Binance 미확인 (btw-reaccelerates-on-aster)
5. 1000RATS 벤뉴간 괴리 해소, 3벤뉴 -22%대 급락 수렴 (1000rats-converges-sharp-decline)
6. APR 전 벤뉴 플러스→마이너스 완전 반전 (apr-flips-negative)
7. ⚠️ALLO OKX OI 10배 급증 건 결론: 방법론 전환 일회성 아티팩트로 판단 (allo-oi-methodology-artifact-confirmed)
8. GALA 낙폭 소폭 재확대(OKX·HL), Binance 이월 (gala-mild-rewiden)
9. BANK 보합→약세 전환 (bank-turns-negative)
10. AIO 마이너스 폭 다소 완화 (aio-mildly-improves)
11. ALPINE 상승폭 지속 축소 (alpine-continues-cooldown)
12. ETHFI OKX chg 정상 갱신되며 플러스 전환, HL도 플러스 전환 (ethfi-turns-positive)
13. CAP 플러스권 확대 지속(OKX·Aster) (cap-holds-positive)
14. CORE 플러스권 확대, Binance 미상장 지속 (core-widens-positive)
15. ADA 플러스에서 소폭 마이너스로 전환(전 벤뉴 동조) (ada-turns-mild-negative)
16. ATOM 좁은 범위 소폭 마이너스 지속 (atom-near-flat)
17. AAVE 좁은 범위 등락 지속 (aave-near-flat)
18. ALGO 플러스권 소폭 유지 (algo-mild-positive)
19. GRAM 플러스권 유지, Binance 이월 (gram-near-flat)
20. BICO -12%대에서 낙폭 확대, Binance 이월 (bico-widens-negative)
21. AEON 좁은 범위 등락 지속 (aeon-fluctuates-narrow-range)
22. APEX 진정 흐름 내 소폭 등락 지속 (apex-continues-cooldown)
23. MMT 마이너스 지속, Binance 이월 (mmt-mild-negative)
24. GIGGLE OKX 낙폭 크게 완화, Binance 이월 (giggle-cools-to-flat)
25. PIPPIN 거의 완전 보합 지속, Binance 이월 (pippin-near-flat)
26. BSB OKX·Aster 마이너스 전환, Binance 이월 (bsb-turns-negative)
27. ASTER(자체토큰) 전 벤뉴 안정권 유지 (aster-cex-stable)
28. HYPE 마이너스 폭 소폭 확대 (hype-mild-negative)
29. FARTCOIN 플러스 지속 강화 (fartcoin-flips-positive)
30. HYPER 플러스권 유지 (hyper-holds-positive)
31. BLESS(Aster) 마이너스 폭 소폭 완화 (bless-mildly-improves)
32. dYdX 공식 인덱서로 정상 작동 재확인, CG dydx_v4는 상시 404 (dydx-coingecko-404-direct-api-normal)
33. 메이저(BTC·ETH·SOL) 안정권, BTC 소폭 상승 확대(majors-remain-stable)
34. HYNA:* 계열 계속 포함 (hyna-builder-deployed-markets)
35. 데이터: OKX OI 방법론(oiCcy×last) 재확인 (okx-oi-methodology-reconfirmed)
36. 데이터: 일부 OKX funding 직전값 이월(vol/OI/chg는 신규 확인) (okx-funding-partial-carryover)
37. 데이터: ⚠️CoinGecko binance_futures 티커 fetch 신규 절단 이슈, 다수 심볼 이월 (binance-cg-fetch-truncation-issue)
38. 데이터: BEAT Binance 신규값 신뢰불가로 폐기, 이월 (beat-fetch-unreliable-discarded)
39. 데이터: CASHCAT Aster 신규값 오염 판단, 이월 (cashcat-aster-fetch-contaminated)
40. 데이터: OrangeX 38회차(~77.75h) (orangex-service-outage-continues)
41. 데이터: Aster ETH truncation 20회차 연속 (truncation-continues-twentieth-round)
42. 글로벌 시총·도미넌스 대체로 동일($2.2~2.3조·BTC 57~60%) (global-dominance-roughly-unchanged)
43. 주식화·상품 토큰 전부 제외 유지

## 한계

(a) **ACE가 반납 이후 세 번째 급변으로 다시 뚜렷한 하락(-12~-14%대)에 진입**했다 — 극도로
변동성이 큰 국면이 지속되어 매 회차 재확인이 필요; (b) **⚠️CoinGecko `binance_futures` 티커
엔드포인트가 이번 회차 신규로 다수 심볼(BTW·BICO·GALA·ETHFI·CAP·AEON·GIGGLE·MMT·GRAM·
PIPPIN·BSB·KAITO 등) 조회에 반복 실패**했다 — WebFetch 캐시/페이로드 절단으로 추정되며(BTC·ETH
같은 최상위 거래량 심볼조차 이 경로로 확인 불가, 별도 집계 엔드포인트로 우회 확인) 전부 직전값을
이월했다(정직 표기); (c) **BEAT의 Binance 신규 fetch값이 직전 대비 약 240배 작아 신뢰불가로
폐기**하고 직전값을 이월했다; (d) **CASHCAT의 Aster 신규 fetch값이 무관한 'ASTON' 티커와 완전히
동일해 데이터 오염으로 판단**, 직전값을 이월했다; (e) **ALLO OKX OI 10배 급증 건은 2회차 연속
동일 레벨 유지가 확인돼 방법론 전환에 따른 일회성 아티팩트로 결론**을 내렸다; (f) dYdX는 공식
인덱서로 BTC·ETH·SOL 정상 작동을 재확인했다(CG `dydx_v4`는 상시 404); (g) OrangeX 전면 중단이
38회차·약 77.75시간째 지속된다; (h) Aster ETH truncation이 20회차 연속 지속된다; (i) Binance
메이저(BTC·ETH)는 집계 엔드포인트로 가격·OI만 참고 확인했고 funding_rate 값은 신뢰도가 낮아
미채용했다; (j) 글로벌 시총·도미넌스는 WebSearch 스니펫 교차확인이며 소스별 편차(BTC 도미넌스
57~60%)가 있다; (k) 주식화·상품·프리IPO 합성 perp 토큰은 이번 회차도 전부 제외했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
