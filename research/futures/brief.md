# 선물시장 스카우트 브리핑 — 2026-08-19 22:30 UTC (KST 2026-08-20 07:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 20:30 UTC)로부터 2시간 경과(정상 간격).**

## 이번 회차 최우선 과제 (b)(c) 판별 결과

### (b) Binance CoinGecko truncation — **5회차 연속**

원 10종목(BICO·GALA·ETHFI·CAP·GIGGLE·MMT·GRAM·PIPPIN·BSB·KAITO)과 BTW 재시도 전부 NOT
FOUND 재확인. BEAT는 이번에도 값이 나왔으나 가격이 $0.011로 OKX($0.157)·Aster($0.162)의
약 1/14 수준이라 명백히 비현실적 — 신뢰불가 판정해 이월(5회차 연속 실질 실패).

**⚠️신규 발견: CORE 티커충돌 의심.** 이번 회차 Binance CG에서 처음 CORE 데이터가 나왔다
(price $1.098). 그러나 OKX CORE-USDT-SWAP은 $0.02159이고, WebSearch로 확인한 CoreDAO
실제 시세는 $0.024~0.033대(CoinCarp·Gate·Coinpaprika 교차확인)로 OKX 값과 근접한 반면
Binance CG 값과는 약 46배 괴리가 있다. **Binance CG의 'CORE'는 CoreDAO가 아닌 다른
자산과의 티커충돌로 판정, 신뢰불가 처리하고 OKX 값을 기준으로 유지한다.** 과거 여러 회차의
'CORE Binance 미상장' 판단은 사실상 옳았던 것으로 재확인됐다.

### (c) ALLO OI 재검토 — **결론: '10배 급증'은 방법론 아티팩트가 아님**

OKX 네이티브 oiUsd 필드를 이번 회차 재차 직접 조회한 결과 개별 조회(oi=988,691·oiCcy=
9,886,910·oiUsd=**$2,904,971.90**)와 벌크 조회(oiCcy=9,895,840·oiUsd=**$2,905,517.58**)가
거의 동일했다. 이는 과거 기준값($0.33M)의 약 8.8배이며, 직전 두 회차의 OKX ALLO OI
($2.89M·$2.90M대)와도 소수점 수준까지 일치한다 — **'전환 후' 수준이 여러 회차에 걸쳐
안정적으로 재현되고 있어, 단발성 계산 버그였다면 기대할 수 없는 지속성**을 보인다. (c) 판별로
확립된 OKX oiCcy/oiUsd 방법론의 정확성(ctVal 정상 반영)을 감안하면, 과거 '10배 급증'을
방법론 전환 아티팩트로 볼 근거는 약하다. **최종 판정: 과거 OI 급증은 아티팩트가 아니라 실제
포지션 증가(또는 최소한 정확한 방법론에서 지속 관측되는 현재 수준)였을 가능성이 높다** —
급증 시점 전후 원본 로그를 재확보하지 못해 100% 확정은 아니나, 이 판정을 최종 채택하고
다음 회차부터 재추적하지 않는다.

## 시장 전반

**BTC 랠리가 추가로 심화됐다.** 부모 세션 확인값(OKX $69,154.6·+7.03%, Bitstamp
$69,135.25·+7.11%)에 더해, 스카우트가 직접 확보한 dYdX 오라클($69,022.50·+6.87%)·
HL($69,274.0·+7.30%)·Aster($68,749.17·+7.03%)가 전부 **+6.9~7.3%**로 수렴해 직전
(+6.3~6.4%)보다 뚜렷이 더 올랐다. **더 두드러진 것은 ETH·HYPE의 가속**이다 — ETH가
OKX(+17.20%)·dYdX 오라클(+17.69%)·HL(+18.61%) 세 벤뉴에서 독립적으로 +17~19%대에
수렴했고(직전 +10.8~13.7%에서 크게 확대), HYPE도 HL에서 +16.5%→+22.5%로 추가 급등했다.
AAVE·ADA·ALGO 등 광범위 알트도 동반 확대(+4.5~5.9%→+7.9~10.2%)돼 BTC/ETH 랠리 심화와
시기가 일치한다. **CASHCAT은 HL(+23.7%)·Aster(+21.0%) 양쪽에서 독립적으로 급등**해 majors
랠리 대비 과도한 확대라 개별 촉매 가능성도 있으나(뉴스는 미확인) 두 벤뉴가 서로 교차확인돼
데이터 오류는 아니다.

**⚠️whipsaw 재반전 다수**: BANK(3벤뉴 전부)·CAP(OKX·Aster)가 마이너스에서 다시 플러스로
반전했고, APR(4벤뉴 전부)은 반대로 플러스에서 소폭 마이너스로 돌아섰다. ALLO는 4벤뉴 전부
-0.17~-0.41%(Aster +0.27%)로 근접 0%까지 진폭이 크게 축소돼 방향성 없는 보합권 진입으로
해석된다. **ATOM은 5개 벤뉴(Binance·Bybit·OKX·HL·Aster) 전부 +5.7~6.2%로 수렴**해 지난
회차의 whipsaw가 해소되고 안정적 플러스로 자리잡았다.

**데이터 품질 이슈**: OKX는 이번 회차 대규모 벌크 조회(ticker+open-interest, instType=
SWAP)로 20여 종목의 price/OI를 일괄 신선 확보(개별조회 대비 효율 크게 개선). OKX funding은
이번 회차도 개별 fetch 미실시로 대부분 이월. **OrangeX는 42회차·약 85.75시간째 전면 중단**
(에러코드 1000 "No service found") 지속. **Aster의 ETH는 24회차째 정상 데이터를 못 얻었다**
— 이번 회차는 값이 나오긴 했으나 price $32,603로 실제(~$2,240)의 약 15배에 달하는 명백한
오염값이라 폐기하고 null 유지했다(BEAT·CORE 사례와 같은 '규모/가격 비현실성 점검'으로
걸러냄). Aster의 ASTER(자체토큰) 항목도 vol($36.9M)·OI($228.5M)가 직전 대비 16~22배
급증해 동일한 사유로 신뢰불가 판정, 이월 처리했다(가격 기반 chg24만 신선 채택). 저장 직전
funding 절대값 점검 결과 최댓값은 ACE Binance -0.00238(직전 최대 -0.00553보다 완화)이며
중앙값은 대체로 1e-5~1e-4대로 정상 범위 — 이상치 없음.

## CEX 주목 종목 (메이저는 전통적으로 테이블 밖, 크립토 네이티브만)

funding은 raw fraction 기준(CoinGecko 파생 소스는 퍼센트를 /100 적용). "[이월]"은 이번 회차
fetch 실패·재조회 못함으로 직전값을 그대로 이어받은 필드.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| ACE [완화] | Binance(직접API) | $379.68M | $12.23M | -0.00238 | -13.786% | 낙폭 완화 지속 |
| ACE [완화] | Bybit(직접API) | $87.60M | $5.75M | -0.0022 | -14.89% | 펀딩 절대값도 완화 |
| BTW [이월,5연속] | Binance | $984.37M | $132.76M | 0.00129 | +48.98% | CG fetch 5회차 연속 실패 |
| **BEAT** [심화] | OKX(직접API) | $85.89M | $4.75M | 0.00027(이월) | **-31.116%** | 낙폭 추가 확대(-29.6%→-31.1%) |
| BEAT [이월,5연속] | Binance | $96.21M | $10.70M | 0.00028 | -18.062% | ⚠️값 나왔으나 가격이 OKX의 1/14, 신뢰불가 |
| BICO [완화] | OKX(직접API) | $16.43M | $2.25M | 0.00005(이월) | -9.271% | 낙폭 완화 지속 |
| BICO [이월,5연속] | Binance | $14.11M | $5.21M | -0.00058 | -12.292% | fetch 5회차 연속 실패 |
| GALA [이월,5연속] | Binance | $18.97M | $6.49M | 0.0000274 | -3.767% | fetch 5회차 연속 실패 |
| GALA [완화] | OKX(직접API) | $6.75M | $1.55M | 0.0001(이월) | -0.0711% | 거의 보합까지 낙폭 완화 |
| ETHFI [이월,5연속] | Binance | $17.88M | $22.55M | -0.0000096 | +0.041% | fetch 5회차 연속 실패 |
| **ETHFI** [확대] | OKX(직접API) | $10.24M | $3.96M | -0.0000514(이월) | **+7.161%** | 상승폭 크게 확대(+4.0%→+7.2%) |
| CAP [이월,5연속] | Binance | $21.87M | $15.02M | -0.00007 | +0.973% | fetch 5회차 연속 실패 |
| **CAP** [반전] | OKX(직접API) | $73.03M(이월) | $10.19M | -0.0000677(이월) | **+0.505%** | ⚠️마이너스→플러스 재반전(2회차 whipsaw) |
| AEON [완화] | OKX(직접API) | $37.83M | $2.83M | 0.00005(이월) | -8.593% | 낙폭 크게 완화(-15.7%→-8.6%) |
| AEON [완화] | Bybit(직접API) | $2.13M | $0.86M | -0.00001 | -8.91% | 동조 완화 |
| APEX [유지] | Bybit(직접API) | $1.36M | $1.93M | 0.00005 | +7.95% | 상승폭 유지 |
| GIGGLE [이월,5연속] | Binance | $15.24M | $10.97M | 0.00005 | -2.679% | fetch 5회차 연속 실패 |
| GIGGLE [확대] | OKX(직접API) | $8.48M | $1.55M | 0.00005(이월) | +3.064% | 플러스권 확대 |
| ALPINE [완화] | Binance(직접API) | $18.30M | $1.99M | 0.00005 | -12.09% | 낙폭 크게 완화(-16.6%→-12.1%) |
| ALPINE [완화] | Bybit(직접API) | $3.73M | $0.61M | 0.00005 | -11.73% | 동조 완화 |
| **CORE** [⚠️충돌의심] | OKX(직접API) | $2.18M(이월) | $1.02M | 0.00008(이월) | +6.881% | CoreDAO 실제가($0.024~0.033대)에 근접 |
| **CORE** [⚠️신규,충돌의심] | Binance | $15.81M | $8.57M | 0.00005 | +1.851% | ⚠️가격이 OKX·실제 CoreDAO의 46배, 신뢰불가 |
| **ATOM** [수렴] | OKX(직접API) | $3.98M(이월) | $3.81M | -0.00015(이월) | **+5.716%** | 5벤뉴 전부 +5.7~6.2%로 수렴, whipsaw 해소 |
| ATOM [수렴] | Binance(직접API) | $21.17M | $15.97M | 0.00008 | +5.72% | 동조 |
| ATOM [수렴] | Bybit(직접API) | $8.60M | $14.22M | 0.0001 | +6.08% | 동조 |
| **AAVE** [확대] | OKX(직접API) | $31.94M | $11.46M | 0.00002(이월) | **+7.925%** | BTC/ETH 랠리 심화 동조, 상승폭 추가 확대 |
| AAVE [확대] | Binance(직접API) | $98.97M | $45.16M | 0.0001 | +8.297% | 동조 확대 |
| AAVE [확대] | Bybit(직접API) | $31.35M | $39.43M | 0.0001 | +8.46% | 동조 확대 |
| **ADA** [확대] | OKX(직접API) | $74.33M | $24.33M | -0.00012(이월) | **+9.317%** | 상승폭 추가 확대(+5.2%→+9.3%) |
| ADA [확대] | Binance(직접API) | $187.86M | $86.59M | 0.0001 | +9.427% | 동조 확대 |
| ADA [확대] | Bybit(직접API) | $81.57M | $56.53M | 0.0001 | +9.65% | 동조 확대 |
| ALGO [확대] | Binance(직접API) | $11.61M | $7.42M | 0.0001 | +5.256% | 상승폭 확대 지속 |
| ALGO [확대] | OKX(직접API) | $5.08M | $2.59M | 0.0001(이월) | +5.235% | 동조 확대 |
| ALGO [확대] | Bybit(직접API) | $4.23M | $6.23M | 0.0001 | +5.47% | 동조 확대 |
| MMT [강세] | OKX(직접API) | $7.33M | $2.43M | -0.00024(이월) | +9.281% | 플러스권 강세 지속 |
| MMT [이월,5연속] | Binance | $5.39M | $8.16M | -0.00009 | -2.043% | fetch 5회차 연속 실패 |
| GRAM [확대] | OKX(직접API) | $4.11M | $6.44M | 0.00005(이월) | +2.881% | 플러스권 확대 |
| GRAM [이월,5연속] | Binance | $8.13M | $14.12M | 0.00005 | +1.459% | fetch 5회차 연속 실패 |
| PIPPIN [확대] | OKX(직접API) | $2.23M | $1.83M | 0.00005(이월) | +2.098% | 플러스 확대(+1.4%→+2.1%) |
| PIPPIN [이월,5연속] | Binance | $4.86M | $5.70M | 0.00005 | -1.285% | fetch 5회차 연속 실패 |
| BSB [유지] | OKX(직접API) | $3.88M(이월) | $2.15M | 0.00032(이월) | +1.554% | 플러스권 유지·확대 |
| BSB [이월,5연속] | Binance | $12.03M | $8.74M | 0.00011 | -1.701% | fetch 5회차 연속 실패 |
| **BANK** [반전] | Binance(직접API) | $23.28M | $10.87M | 0.00005 | **+0.111%** | ⚠️마이너스→플러스 재반전(3벤뉴 전부) |
| BANK [반전] | Bybit(직접API) | $2.74M | $4.04M | 0.00005 | +0.17% | 동조 반전 |
| **APR** [반전] | OKX(직접API) | $31.91M | $2.79M | 0.00005(이월) | **-0.741%** | ⚠️플러스→소폭 마이너스 반전(4벤뉴 전부) |
| APR [반전] | Bybit(직접API) | $5.52M | $2.98M | 0.00005 | -0.50% | 동조 반전 |
| APR [반전] | Binance(직접API) | $31.37M | $10.38M | 0.00005 | -1.283% | 동조 반전 |
| AIO [완화] | Binance(직접API) | $11.47M | $4.12M | 0.00005 | -6.671% | 낙폭 완화 지속 |
| AIO [완화] | Bybit(직접API) | $1.15M | $1.14M | 0.00005 | -6.84% | 동조 완화 |
| ALLO [보합] | Binance(직접API) | $25.40M | $11.90M | 0.00005 | -0.285% | ⚠️거의 보합으로 진폭 축소(4벤뉴 근접 0%) |
| ALLO [보합] | OKX(직접API) | $20.09M | $2.91M | 0.00005(이월) | -0.414% | 동조, OI는 (c) 재검증으로 신뢰도 확인 |
| ALLO [보합] | Bybit(직접API) | $3.27M | $4.29M | 0.00005 | -0.17% | 동조 |
| 1000RATS [주춤] | Binance(직접API) | $24.70M | $12.88M | 0.00008 | -7.171% | 회복세 주춤, -7%대 유지 |
| 1000RATS [주춤] | Bybit(직접API) | $10.70M | $4.91M | 0.00005 | -7.13% | 동조 |
| ASTER(자체) [확대] | Binance(직접API) | $46.80M | $73.13M | 0.00005 | +2.728% | 상승폭 유지, 광범위 알트 랠리와 동조 |
| ASTER(자체) [확대] | OKX(직접API) | $10.74M | $8.79M | 0.0001(이월) | +3.128% | 신선 재조회, 상승폭 확대 |
| ASTER(자체) [이월] | Bybit | $2.55M | $39.93M | 0.00005 | +0.732% | 이번 회차 재조회 못함 |
| KAITO [냉각] | OKX(직접API) | $27.15M | $5.59M | 0.0000060(이월) | +1.871% | 상승폭 다소 냉각(+3.4%→+1.9%) |
| KAITO [이월,USDT,5연속] | Binance | $33.30M | $15.03M | -0.00009 | +4.644% | fetch 5회차 연속 실패 |
| KAITO [이월,USDC,5연속] | Binance | $3.82M | $1.14M | -0.00009 | +3.695% | fetch 5회차 연속 실패 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 42회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| ACE [완화] | Hyperliquid | $2.75M | $1.72M | -0.00044 | -14.61% | CEX와 동조, 낙폭 완화 |
| ACE [완화] | Aster | $0.77M | $0.19M | -0.00047 | -13.968% | 낙폭 완화 |
| ACE [중단] | OrangeX | — | — | — | — | 42회차·약 85.75시간 |
| BTW [완화] | Aster | $14.44M | $7.36M | 0.00009 | -5.167% | 낙폭 완화 지속, Binance 교차확인 불가 지속 |
| KAITO [냉각] | Hyperliquid | $3.48M | $5.20M | 0.00001 | +2.04% | 상승폭 다소 냉각 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **CASHCAT** [급등⚠️] | Hyperliquid | $12.64M | $15.44M | 0.00007 | **+23.73%** | 상승폭 급확대(+4.5%→+23.7%), Aster와 교차확인 |
| **CASHCAT** [급등⚠️] | Aster | $1.09M | $0.79M | 0.00007 | **+21.021%** | HL과 함께 급등, 양쪽 벤뉴 일치 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GALA [완화] | Hyperliquid | $0.87M | $0.67M | 0.0 | +0.64% | 낙폭 완화, 플러스 전환 |
| BEAT [유지] | Aster | $2.09M | $1.11M | 0.00001 | -28.509% | 낙폭 유지, OKX와 정합 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BICO [완화] | Aster | $0.07M | $0.13M | -0.00106 | -8.498% | 낙폭 완화, OKX와 정합 |
| BICO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| AEON [완화] | Aster | $0.11M | $0.30M | 0.00001 | -8.681% | 낙폭 크게 완화, OKX·Bybit와 정합 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [확대] | Hyperliquid | $1.89M | $15.50M | 0.00001 | +3.20% | 플러스권 확대, OKX와 동조 |
| **ATOM** [수렴] | Hyperliquid | $0.69M | $1.90M | 0.00001 | +6.19% | 5벤뉴 전부 수렴, whipsaw 해소 |
| ATOM [수렴] | Aster | $0.06M | $1.87M | 0.0001 | +5.791% | 신선 재확인, 타 벤뉴와 수렴 |
| AAVE [확대] | Hyperliquid | $10.35M | $59.13M | 0.00001 | +8.76% | BTC/ETH 랠리 심화 동조 |
| AAVE [확대] | Aster | $0.57M | $4.81M | 0.0001 | +8.336% | 신선 재확인, 동조 확대 |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ADA [확대] | Hyperliquid | $8.82M | $28.79M | 0.00001 | +10.19% | BTC/ETH 랠리 심화 동조 |
| ADA [확대] | Aster | $0.79M | $1.27M | 0.0001 | +9.543% | 신선 재확인, 동조 확대 |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALGO [확대] | Hyperliquid | $0.74M | $1.92M | 0.00001 | +5.59% | BTC/ETH 랠리 심화 동조 |
| ALGO [확대] | Aster | $0.02M | $0.02M | -0.00003 | +4.856% | 신선 재확인, 동조 확대 |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ASTER(자체) [⚠️이상치기각] | Aster | $1.63M(이월) | $14.36M(이월) | 0.00001(이월) | +3.107% | raw vol/OI가 16~22배 급증해 비현실적, 이월 |
| ASTER(자체) [확대] | Hyperliquid | $3.61M | $14.21M | 0.00006 | +3.72% | 신선 재조회, 상승폭 확대(+0.7%→+3.7%) |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **HYPE** [급확대⚠️] | Hyperliquid | $1,246.97M | $1,721.41M | 0.00015 | **+22.52%** | 상승폭 추가 급확대(+16.5%→+22.5%), majors 최대 |
| BLESS [전환] | Aster | $0.03M | $0.08M | 0.00005 | +0.211% | 낙폭 완전 해소, 플러스 전환 |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BTC [지속] | dYdX | $45.26M | $19.35M | 0.0 | +6.874% | 오라클가 $69,022.50, BTC 랠리 지속 |
| **ETH** [심화⚠️] | dYdX | $110.29M | $22.08M | -0.000012 | **+17.69%** | 오라클가 $2,242.56, ETH 랠리 크게 심화 |
| SOL [확대] | dYdX | $1.62M | $4.78M | 0.0 | +10.418% | 오라클가 $85.15, SOL도 동반 확대 |
| BTC [지속] | Hyperliquid | $5,479.37M | $2,387.08M | 0.00001 | +7.30% | 거래량·OI 확대, 랠리 지속 |
| **ETH** [심화⚠️] | Hyperliquid | $3,795.38M | $1,964.05M | 0.00003 | **+18.61%** | OKX·dYdX와 독립 교차확인 |
| BTC [지속] | Aster | $1,717.26M | $861.12M | 0.00008 | +7.025% | 거래량·OI 확대, 랠리 지속 |
| ETH [truncation 24연속] | Aster | — | — | — | — | 이번엔 값 나왔으나 가격이 실제의 15배라 폐기 |
| 1000RATS [주춤] | Aster | $0.21M | $0.07M | 0.00002 | -7.003% | 회복세 주춤 |
| AIO [완화] | Aster | $0.03M | $0.08M | 0.00005 | -7.352% | CEX와 동조 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALLO [보합] | Aster | $0.08M | $0.07M | 0.00001 | +0.268% | ⚠️CEX 전체와 함께 근접 0%로 진폭 축소 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| APR [반전] | Aster | $0.08M | $0.29M | 0.00001 | -0.446% | ⚠️플러스→소폭 마이너스 반전 |
| APR [미상장] | Hyperliquid | — | — | — | — | 이번 회차도 HL 미상장 재확인 |
| **BANK** [반전] | Aster | $0.10M | $0.23M | 0.00001 | **+0.334%** | ⚠️마이너스→플러스 재반전, 3벤뉴 합의 |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [유지] | Aster | $0.12M | $0.13M | 0.00002 | +2.087% | 플러스권 유지·확대 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **CAP** [반전] | Aster | $0.10M | $0.15M | -0.00001 | **+0.331%** | ⚠️마이너스→플러스 재반전, OKX와 동조 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| FARTCOIN [확대] | Hyperliquid | $12.35M | $33.66M | 0.00011 | +11.97% | 상승폭 추가 확대(+8.3%→+12.0%) |
| ETHFI [확대] | Hyperliquid | $4.19M | $11.19M | 0.00001 | +8.15% | 상승폭 크게 확대 |
| HYPER [이월] | Hyperliquid | $0.07M | $0.20M | -0.00002 | +5.457% | 이번 회차 재조회 못함 |
| APEX [유지] | Hyperliquid | $0.24M | $0.71M | 0.00001 | +8.122% | 이번 회차 재조회 못함, Bybit는 신선(+7.95%) |
| HYNA:BTC-USD [지속] | Hyperliquid | $1.03M | $2.50M | 0.00001 | +7.42% | 기초자산(BTC) 랠리 지속 반영 |
| **HYNA:ETH-USD** [심화⚠️] | Hyperliquid | $1.14M | $1.84M | 0.00001 | **+18.64%** | 기초자산(ETH) 랠리 심화 반영 |
| **HYNA:HYPE** [심화⚠️] | Hyperliquid | $0.39M | $0.71M | 0.00002 | **+22.59%** | 기초자산(HYPE) 랠리 심화 반영 |
| HYNA:PUMP [냉각] | Hyperliquid | $0.02M | $0.17M | 0.00001 | +2.88% | 별도 기초자산, 상승폭 냉각(+9.8%→+2.9%) |
| HYNA:SOL-USD [확대] | Hyperliquid | $0.22M | $0.59M | 0.00002 | +11.63% | 기초자산(SOL) 랠리 확대 반영 |

## 테마 태그 (요약)

1. BTC 랠리 추가 심화(+6.3~6.4%→+6.9~7.3%, dYdX·HL·Aster 수렴) (majors-rally-accelerates)
2. ⚠️ETH 랠리 크게 가속(+10.8~13.7%→+17~19%, OKX·dYdX·HL 독립 수렴) (majors-rally-accelerates)
3. ⚠️HYPE 추가 급등(+16.5%→+22.5%, HL) (majors-rally-accelerates)
4. SOL도 동반 확대(dYdX +10.4%) (majors-rally-accelerates)
5. AAVE·ADA·ALGO 광범위 알트 상승폭 추가 확대(+4.5~5.9%→+7.9~10.2%) (broad-alt-rally-extends-with-btc)
6. ⚠️CASHCAT 급등(HL +23.7%·Aster +21.0%, 양벤뉴 교차확인) (cashcat-surges)
7. ⚠️ATOM 5벤뉴 전부 수렴, whipsaw 해소 (atom-resolves-positive-all-venues)
8. ⚠️ALLO 4벤뉴 근접 0%, 보합권 전환 (allo-stabilizes-near-flat)
9. ⚠️BANK 3벤뉴 전부 마이너스→플러스 재반전 (bank-reverses-positive-again)
10. ⚠️CAP OKX·Aster 마이너스→플러스 재반전(2회차 whipsaw) (cap-reverses-positive-again)
11. ⚠️APR 4벤뉴 전부 플러스→소폭 마이너스 반전 (apr-flips-slightly-negative)
12. ⚠️신규발견: CORE 티커충돌 의심, Binance CG값 신뢰불가·OKX 값 채택 (core-ticker-collision-flagged)
13. ✅(c) ALLO OI 재검토 완료 — 과거 급증은 아티팩트 아님으로 최종 판정 (allo-oi-jump-not-artifact-confirmed)
14. (b) Binance CG truncation 5회차 연속, BEAT 가격 비현실성 재확인 (binance-cg-fetch-truncation-persists-5th-round)
15. AEON 3벤뉴 낙폭 크게 완화 (aeon-decline-eases-sharply)
16. ALPINE 낙폭 크게 완화 (alpine-decline-eases)
17. ETHFI OKX·HL 상승폭 크게 확대 (ethfi-extends-gains)
18. BICO 낙폭 완화 지속 (bico-improves)
19. GALA 거의 보합까지 낙폭 완화 (gala-mixed)
20. APEX Bybit 상승폭 유지 (apex-reaccelerates)
21. GIGGLE OKX 플러스권 확대 (giggle-turns-positive)
22. MMT OKX 플러스권 강세 지속 (mmt-extends-positive)
23. GRAM OKX·HL 플러스권 확대 (gram-extends-positive)
24. PIPPIN OKX 플러스 확대 (pippin-turns-clearly-positive)
25. BSB OKX·Aster 플러스권 유지·확대 (bsb-turns-positive)
26. AIO 낙폭 소폭 완화 (aio-eases-slightly)
27. 1000RATS 회복세 주춤 (1000rats-recovery-stalls)
28. ASTER(자체) Binance·OKX·HL 상승폭 확대 (aster-cex-stable)
29. ⚠️ASTER 자체토큰 Aster 벤뉴 vol/OI 이상치 기각 (aster-token-oi-vol-anomaly-discarded)
30. KAITO OKX·HL 상승폭 다소 냉각 (kaito-cools)
31. ACE 낙폭 완화, 펀딩 절대값도 완화 (ace-decline-stabilizes)
32. BTW Aster 낙폭 완화 지속, 단독소스 지속 (btw-continues-swinging-unconfirmed)
33. BEAT OKX·Aster 낙폭 추가 확대 (beat-decline-widens-sharply)
34. FARTCOIN 상승폭 추가 확대 (fartcoin-reaccelerates)
35. BLESS 낙폭 완전 해소, 플러스 전환 (bless-improves)
36. HYPER HL 이번 회차 재조회 못해 이월 (hyper-momentum-cools)
37. HYNA:* 계열(HL) 기초자산 랠리 심화 반영 (hyna-builder-deployed-markets, majors-rally-accelerates)
38. 데이터: OKX 벌크조회로 20여 종목 일괄 신선 확보, 효율 크게 개선 (okx-bulk-fetch-efficient)
39. 데이터: ⚠️Binance CG truncation 5회차 연속 (binance-cg-fetch-truncation-persists-5th-round)
40. 데이터: OrangeX 42회차(약 85.75h) 서비스 중단 지속 (orangex-outage-continues)
41. 데이터: ⚠️Aster ETH truncation 24회차 연속, 이번엔 오염값(15배 괴리)이라 폐기 (aster-eth-truncation-continues)
42. 데이터: ⚠️신규 — CORE 티커충돌 의심 (core-ticker-collision-flagged)
43. 데이터: ✅(c) ALLO OI 재검토 완료, 재추적 종료 (allo-oi-jump-not-artifact-confirmed)
44. 데이터: funding 절대값 점검 통과(최댓값 -0.00238, 중앙값 1e-5~1e-4대) (funding-sanity-check-passed)
45. 주식화·상품 토큰 전부 제외 유지 (stock-commodity-tokens-excluded-crypto-native-confirmed)

## 한계

(a) 메이저 랠리는 직전 회차 부모 세션이 4개 독립 거래소로 확정했고, 이번 회차엔 추가로
dYdX·HL·Aster·OKX ETH 티커까지 독립 교차확인해 랠리 심화(특히 ETH/HYPE 가속)를 재확인했다.
(b) Binance CoinGecko truncation은 5회차 연속이며, 이번 회차엔 CORE에서 유사한 성격의
신규 티커충돌 의심 사례를 추가로 발견했다(OKX·WebSearch 실제가와 대조해 기각). (c) ALLO OI
재검토는 이번 회차로 완료됐다 — 과거 '10배 급증'을 방법론 아티팩트로 볼 근거가 약하다고
최종 판정했으며, 100% 확정은 아니지만(급증 시점 원본 로그 미확보) 이 판정을 채택하고 다음
회차부터 재추적하지 않는다. (d) OrangeX 전면 중단이 42회차·약 85.75시간째 지속된다.
(e) Aster ETH truncation이 24회차 연속이며, 이번 회차엔 오염값(실제의 15배)이 반환돼
'규모/가격 비현실성 점검'으로 걸러냈다 — 동일 점검이 Aster ASTER(자체토큰)의 vol/OI
이상치(16~22배 급증)도 걸러냈다. (f) CASHCAT·HL·HYPE의 급등폭은 두 개 이상의 독립 벤뉴가
교차확인했으나, 개별 촉매(뉴스)는 확인하지 못했다. (g) 주식화·상품·프리IPO 합성 perp 토큰은
이번 회차도 전부 제외했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
