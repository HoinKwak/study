# 선물시장 스카우트 브리핑 — 2026-08-20 02:30 UTC (KST 2026-08-20 11:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-20
> 00:30 UTC)로부터 2시간 경과(정상 간격).**

## 시장 전반

부모 세션이 확정한 기준값(**BTC $69,500.3·+7.92%, ETH $2,257.92·+18.21%, SOL $85.05·
+10.63%**)에 더해, 이번 회차 스카우트가 독립 확보한 **dYdX 오라클**(BTC $69,453.78·+7.95%,
ETH $2,258.37·+18.24%, SOL $85.01·+10.63%)·**HL**(BTC +7.94%, ETH +18.42%)·**Aster**
(BTC +7.927%)가 전부 +7.9~8.0%(BTC)·+18.2~18.4%(ETH)·+10.6%(SOL, dYdX와 사실상 일치)로
수렴했다. 랠리는 여전히 **고점 횡보 국면**이며(직전 대비 BTC·SOL 거의 동일, ETH 소폭 하락),
이번 회차도 스카우트가 직접 발견한 신규 개별 촉매는 없다(기존 촉매: 미 재무부 장기국채
바이백 2배 확대·SEC 'Regulation Crypto Assets' 통과·백악관 크립토 행사).

**AAVE는 상승폭을 다시 확대**(+9.7~10.0%→+10.8~11.0%, 5벤뉴 수렴 지속)한 반면 **ADA는
계속 냉각**(+8.1~8.6%→+6.9~7.2%)해, 두 종목의 상반된 흐름이 이번이 3회차째다.

**CASHCAT은 3회차 연속으로 상승폭을 더 확대**했다(HL +29.22%→+35.49%, Aster +28.05%→
+35.81%, 여전히 두 벤뉴 교차확인). 온체인 워치에서도 3연속 상승·회전율 하락이 확인됐다는
부모 세션 메모와 함께 놓고 보면 실수요 쪽 가능성에 계속 무게가 실리나, 이번 회차도 구체적
뉴스 촉매는 찾지 못했다.

**⚠️whipsaw 패턴에 변화가 나타났다**: CAP는 이번에도 마이너스에서 플러스로 재반전
(OKX -0.12%→+1.01%, Aster -1.93%→+2.26%)해 **4회차째 whipsaw**를 이어갔지만, BANK는
이번엔 반전 없이 마이너스권에 머물며 소폭 확대(Binance -2.06%→-2.44%, Bybit -2.06%→
-2.31%, Aster -1.93%→-2.01%)돼 **3회 연속 whipsaw 패턴이 깨졌다**. APR은 CEX(-1.5~
-1.8%→-4.2~-4.8%)와 Aster(+0.25%→-4.42%)가 이번엔 같은 방향으로 수렴해 직전 회차의
벤뉴간 괴리가 해소됐다. ALLO는 Binance만 낙폭이 소폭 완화(-4.03%→-3.51%)됐고 OKX·Bybit는
-4.2% 안팎을 유지해 혼조.

**⚠️BTW(Aster)의 낙폭이 큰 폭으로 확대**됐다(-8.78%→-21.14%). Binance 교차확인은 이번
회차도 안 되며(7회차 연속 실패), 단일 벤뉴 관측이라 해석에 주의가 필요하다.

**⭐Aster ASTER(자체토큰) OI 이상치를 이번 회차로 확정 판정한다.** $228.5M→$230.8M→
**$233.5M**로 3회 연속 $228~234M 범위에 근접 재현됐다(3회차 소수점 수준 근접 일치는 과거
ALLO OI 사례의 확정 기준과 동일). 계산 오류나 단발성 아티팩트로는 이렇게 안정적으로
재현되기 어려우므로, Aster ASTER 자체 OI는 CEX(Binance $74.3M·OKX $9.0M)보다 3~26배
높은 수준이 **실제로 지속되는 현재 수준**이라고 결론 내린다(원인 미상 — Aster 거래소 자체
유동성 프로그램·인센티브 포지션 등 구조적 요인 가능성이 있으나 확인은 못함).

**데이터 품질 개선**: 이번 회차 Binance CoinGecko 재조회에서 ACE·APR·ALPINE·ATOM·AAVE·
ADA·ALGO·BANK·AIO·ALLO·1000RATS·ASTER(자체) 12개 종목이 신선하게 복구됐다(직전까지
이월 처리하던 것 다수 포함). 다만 **(b) truncation은 7회차 연속**이며 대상은 BICO·GALA·
ETHFI·CAP·GIGGLE·MMT·GRAM·PIPPIN·BSB·KAITO·BTW·CORE(완전 소실, 12종목)에 더해 BEAT가
이번 회차도 OKX/Aster(-27~28%)와 정반대인 +8.204%라는 값을 반환해(전전 회차의 '1/14 수준
이상값'과 유사한 패턴) 사실상 13종목이 신뢰불가 상태다. **대체 경로로 fapi.binance.com
직접 조회를 재시도했으나 HTTP 451(지역차단)로 이 컨테이너 환경에서 여전히 차단됨을
재확인**했다 — 대체 경로 시도는 실패로 기록한다. Bybit는 이번 회차 ACE·AEON·APEX·ALPINE·
ATOM·AAVE·ADA·ALGO·BANK·APR·AIO·ALLO·1000RATS·ASTER(자체) 전체가 신선 조회 성공(ASTER는
직전 이월값 $2.55M/$39.93M에서 $11.89M/$41.58M로 갱신 — 다른 벤뉴와 정합성 개선). OKX는
벌크 티커+개별 open-interest 조회를 병행해 대부분 신선 확보했고 funding은 대부분 이월.
Hyperliquid는 공식 API가 POST 전용이라 CoinGecko hyperliquid 소스로 대체했으며, HL
신선값(BTC +7.94%·ETH +18.42%)이 dYdX·부모 기준과 근접해 이상 없음을 확인했다. 저장
직전 funding 절대값 점검 결과 이번 회차 최댓값은 **Bybit ACE -0.00442**(직전 최대
-0.00193~-0.00194보다 확대된 신규 관측 최대치)이며 중앙값은 1e-5~1e-4대로 정상 범위 —
ACE의 전방위적 지속 하락과 궤를 같이하는 값이라 이상치로 판정하지 않는다.

## CEX 주목 종목 (메이저는 전통적으로 테이블 밖, 크립토 네이티브만)

funding은 raw fraction 기준(CoinGecko 파생 소스는 퍼센트를 /100 적용). "[이월]"은 이번 회차
fetch 실패·재조회 못함으로 직전값을 그대로 이어받은 필드.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| ACE [유지] | Binance(CG,신선) | $315.60M | $12.10M | -0.00281 | -14.125% | 낙폭 지속, 펀딩 음수 확대 |
| ACE [유지] | Bybit(CG,신선) | $73.95M | $6.00M | -0.00442 | -15.038% | 동조, 펀딩 신규 최대 |
| BTW [이월,7연속] | Binance | $984.37M | $132.76M | 0.00129 | +48.98% | CG fetch 7회차 연속 실패 |
| **BEAT** [완화] | OKX(직접API) | $91.48M | $5.05M | 0.00027(이월) | **-27.66%** | 낙폭 소폭 완화(-29.81%→-27.66%) |
| BEAT [신뢰불가,7연속] | Binance | $96.21M | $10.70M | 0.00028 | -18.062% | ⚠️OKX/Aster와 정반대 값(+8.2%) 재반환, 이월 유지 |
| BICO [유지] | OKX(직접API) | $15.18M | $2.28M | 0.00005(이월) | -5.56% | 낙폭 완화(-7.96%→-5.56%) |
| BICO [이월,7연속] | Binance | $14.11M | $5.21M | -0.00058 | -12.292% | fetch 7회차 연속 실패 |
| GALA [이월,7연속] | Binance | $18.97M | $6.49M | 0.0000274 | -3.767% | fetch 7회차 연속 실패 |
| **GALA** [확대] | OKX(직접API) | $6.58M | $1.75M | 0.0001(이월) | **+4.69%** | 플러스권 확대(+3.84%→+4.69%) |
| ETHFI [이월,7연속] | Binance | $17.88M | $22.55M | -0.0000096 | +0.041% | fetch 7회차 연속 실패 |
| **ETHFI** [⚠️냉각] | OKX(직접API) | $11.43M | $3.96M | -0.0000514(이월) | **+6.77%** | 상승폭 냉각(+9.84%→+6.77%) |
| CAP [이월,7연속] | Binance | $21.87M | $15.02M | -0.00007 | +0.973% | fetch 7회차 연속 실패 |
| **CAP** [⚠️4회차 whipsaw] | OKX(직접API) | $75.20M | $10.21M | -0.0000677(이월) | **+1.01%** | 마이너스→플러스 재반전(4회차째) |
| AEON [완화] | OKX(직접API) | $34.75M | $2.91M | 0.00005(이월) | -5.86% | 낙폭 완화 지속(-6.5%→-5.86%) |
| AEON [완화] | Bybit(CG,신선) | $2.09M | $0.87M | 0.00005 | -5.818% | 동조 완화 |
| **APEX** [⚠️전환] | Bybit(CG,신선) | $1.29M | $1.85M | 0.00005 | **-2.526%** | 플러스→마이너스 전환 |
| GIGGLE [이월,7연속] | Binance | $15.24M | $10.97M | 0.00005 | -2.679% | fetch 7회차 연속 실패 |
| GIGGLE [냉각] | OKX(직접API) | $7.85M | $1.58M | 0.00005(이월) | +3.16% | 플러스권 소폭 냉각(+4.27%→+3.16%) |
| ALPINE [유지] | Binance(CG,신선) | $13.70M | $2.00M | 0.00005 | -10.563% | 낙폭 유지 |
| ALPINE [유지] | Bybit(CG,신선) | $2.58M | $0.59M | 0.00005 | -10.458% | 동조 |
| **CORE** [냉각] | OKX(직접API) | $2.37M | $1.02M | 0.00008(이월) | +6.20% | CoreDAO 실제가 근접 유지, 상승폭 냉각(+8.29%→+6.20%) |
| **CORE** [⚠️소실,7연속] | Binance | — | — | — | — | 7회차 연속 완전 소실, 충돌 판정 유지 |
| **ATOM** [수렴] | OKX(직접API) | $4.34M | $3.77M | -0.00015(이월) | **+4.67%** | 5벤뉴 수렴 지속(+4.3~4.8%) |
| ATOM [수렴] | Binance(CG,신선) | $20.00M | $15.60M | 0.00003 | +4.661% | 동조 |
| ATOM [수렴] | Bybit(CG,신선) | $7.97M | $14.04M | 0.00006 | +4.812% | 동조 |
| **AAVE** [확대] | OKX(직접API) | $33.17M | $12.03M | 0.00002(이월) | **+10.97%** | 상승폭 추가 확대(+9.99%→+11.0%) |
| AAVE [확대] | Binance(CG,신선) | $101.80M | $45.90M | 0.0001 | +10.764% | 동조 확대 |
| AAVE [확대] | Bybit(CG,신선) | $32.43M | $40.10M | 0.0001 | +10.814% | 동조 확대 |
| **ADA** [⚠️3회차 냉각] | OKX(직접API) | $80.50M | $23.95M | -0.00012(이월) | **+7.20%** | 상승폭 3회차째 냉각, AAVE와 상반 |
| ADA [냉각] | Binance(CG,신선) | $202.90M | $86.10M | 0.0001 | +6.95% | 동조 냉각 |
| ADA [냉각] | Bybit(CG,신선) | $91.12M | $54.24M | 0.0001 | +7.016% | 동조 냉각 |
| ALGO [유지] | Binance(CG,신선) | $13.60M | $7.50M | 0.0 | +5.933% | 상승폭 유지 |
| ALGO [유지] | OKX(직접API) | $5.57M | $2.64M | 0.0001(이월) | +6.03% | 동조 |
| ALGO [유지] | Bybit(CG,신선) | $4.73M | $6.28M | 0.00004 | +5.921% | 동조 |
| MMT [확대] | OKX(직접API) | $7.63M | $2.47M | -0.00024(이월) | +10.58% | 플러스권 추가 확대(+9.78%→+10.58%) |
| MMT [이월,7연속] | Binance | $5.39M | $8.16M | -0.00009 | -2.043% | fetch 7회차 연속 실패 |
| GRAM [유지] | OKX(직접API) | $4.49M | $6.46M | 0.00005(이월) | +3.11% | 플러스권 유지, 진폭 축소 |
| GRAM [이월,7연속] | Binance | $8.13M | $14.12M | 0.00005 | +1.459% | fetch 7회차 연속 실패 |
| PIPPIN [⚠️냉각] | OKX(직접API) | $2.18M | $1.79M | 0.00005(이월) | +3.15% | 플러스권 냉각(+4.26%→+3.15%) |
| PIPPIN [이월,7연속] | Binance | $4.86M | $5.70M | 0.00005 | -1.285% | fetch 7회차 연속 실패 |
| BSB [확대] | OKX(직접API) | $4.27M | $2.13M | 0.00032(이월) | +2.40% | 플러스권 확대(+0.32%→+2.40%) |
| BSB [이월,7연속] | Binance | $12.03M | $8.74M | 0.00011 | -1.701% | fetch 7회차 연속 실패 |
| **BANK** [⚠️whipsaw 종료] | Binance(CG,신선) | $21.70M | $10.80M | 0.00005 | **-2.443%** | 3회 whipsaw 후 처음 반전 없이 마이너스 지속 |
| BANK [유지] | Bybit(CG,신선) | $2.37M | $4.00M | 0.00005 | -2.312% | 동조 |
| **APR** [⚠️확대] | OKX(직접API) | $27.48M | $2.55M | 0.00005 | **-4.82%** | 마이너스 폭 확대(-1.79%→-4.82%) |
| APR [확대] | Bybit(CG,신선) | $5.17M | $2.75M | 0.00005 | -4.529% | 동조 확대 |
| APR [확대] | Binance(CG,신선) | $28.00M | $9.90M | 0.00005 | -4.225% | 동조 |
| AIO [확대] | Binance(CG,신선) | $10.20M | $4.00M | 0.00005 | -11.043% | 낙폭 확대(-9.5%→-11.0%) |
| AIO [확대] | Bybit(CG,신선) | $1.02M | $1.09M | 0.00005 | -10.507% | 동조 확대 |
| ALLO [완화] | Binance(CG,신선) | $24.40M | $11.80M | -0.00002 | -3.513% | 낙폭 소폭 완화(-4.03%→-3.51%) |
| ALLO [유지] | OKX(직접API) | $18.85M | $2.98M | 0.00005 | -4.194% | 낙폭 유지 |
| ALLO [유지] | Bybit(CG,신선) | $3.03M | $4.26M | 0.0 | -4.025% | 낙폭 유지 |
| 1000RATS [완화] | Binance(CG,신선) | $21.60M | $13.20M | 0.00016 | -3.598% | 낙폭 추가 완화(-5.61%→-3.60%) |
| 1000RATS [완화] | Bybit(CG,신선) | $9.34M | $4.99M | 0.00005 | -4.145% | 동조 |
| ASTER(자체) [확대] | Binance(CG,신선) | $60.00M | $74.30M | 0.00005 | +5.799% | 상승폭 확대(+4.54%→+5.80%), 4벤뉴 수렴 |
| ASTER(자체) [확대] | OKX(직접API) | $14.13M | $9.00M | 0.0001(이월) | +5.935% | 동조 확대 |
| ASTER(자체) [신선] | Bybit(CG,신선) | $11.89M | $41.58M | 0.00005 | +5.885% | 이월 탈피, 정합성 개선 |
| KAITO [유지] | OKX(직접API) | $27.18M | $5.67M | 0.0000060(이월) | +3.88% | 상승폭 유지 |
| KAITO [이월,USDT,7연속] | Binance | $33.30M | $15.03M | -0.00009 | +4.644% | fetch 7회차 연속 실패 |
| KAITO [이월,USDC,7연속] | Binance | $3.82M | $1.14M | -0.00009 | +3.695% | fetch 7회차 연속 실패 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 44회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).
HL은 공식 API가 POST 전용이라 GET 전용 WebFetch로 직접조회 불가 — CoinGecko hyperliquid
소스(include_tickers=all)로 대체했다.

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| ACE [유지] | Hyperliquid | $2.65M | $1.67M | -0.00065 | -16.266% | CEX와 동조, 낙폭 확대 |
| ACE [완화] | Aster | $0.65M | $0.18M | -0.0009 | -14.714% | 낙폭 소폭 완화 |
| ACE [중단] | OrangeX | — | — | — | — | 44회차·약 89.75시간 |
| **BTW** [⚠️확대] | Aster | $14.15M | $7.21M | 0.00009 | **-21.142%** | 낙폭 큰 폭 확대(-8.78%→-21.14%), Binance 교차확인 불가 지속 |
| KAITO [유지] | Hyperliquid | $3.85M | $5.29M | 0.00001 | +3.61% | 상승폭 유지 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **CASHCAT** [확대⚠️] | Hyperliquid | $12.55M | $16.73M | 0.00019 | **+35.49%** | 3회차 연속 상승폭 확대, Aster·온체인 워치와 교차확인 지속 |
| **CASHCAT** [확대⚠️] | Aster | $1.12M | $0.85M | 0.00008 | **+35.81%** | HL과 동반 확대 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GALA [확대] | Hyperliquid | $0.82M | $0.67M | 0.00001 | +4.762% | 플러스권 확대 지속 |
| BEAT [유지] | Aster | $2.33M | $1.05M | 0.00001 | -28.169% | 낙폭 유지, OKX와 정합, 랠리 소외 지속 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BICO [유지] | Aster | $0.07M | $0.13M | -0.0001 | -8.219% | 낙폭 유지, OKX와 근접 |
| BICO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| AEON [완화] | Aster | $0.12M | $0.31M | 0.00001 | -5.265% | 낙폭 완화 지속 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [유지] | Hyperliquid | $2.03M | $15.50M | 0.00001 | +3.04% | 플러스권 유지 |
| **ATOM** [수렴] | Hyperliquid | $0.68M | $1.88M | -0.00004 | +4.98% | 5벤뉴 수렴 지속 |
| ATOM [수렴] | Aster | $0.06M | $1.85M | 0.0001 | +4.329% | 동조 |
| AAVE [확대] | Hyperliquid | $10.65M | $59.27M | 0.00001 | +10.88% | 상승폭 추가 확대 |
| AAVE [확대] | Aster | $0.63M | $4.91M | 0.0001 | +11.207% | 동조 확대 |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ADA [⚠️냉각] | Hyperliquid | $10.60M | $28.45M | 0.00001 | +7.15% | 상승폭 3회차째 냉각(+8.55%→+7.15%) |
| ADA [냉각] | Aster | $0.84M | $1.25M | 0.0001 | +6.893% | 동조 냉각 |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALGO [확대] | Hyperliquid | $0.71M | $1.96M | 0.00001 | +6.048% | 동조 확대 |
| ALGO [유지] | Aster | $0.02M | $0.02M | 0.0 | +6.499% | 동조 |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **ASTER(자체)** [⭐확정] | Aster | $44.30M | $233.53M | 0.00014 | +5.877% | OI $233.5M로 3회 연속 근접 재현 — 이상치 아닌 지속 수준 확정 |
| ASTER(자체) [확대] | Hyperliquid | $4.75M | $14.69M | 0.00002 | +5.874% | 상승폭 확대, 4벤뉴 수렴(5.8~5.9%) |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **HYPE** [⚠️완화] | Hyperliquid | $1,520.00M | $1,660.00M | 0.00008 | **+19.36%** | 3회 연속 상승폭 완화(22.5%→19.9%→19.36%), majors 중 여전히 최대 |
| BLESS [유지] | Aster | $0.03M | $0.08M | 0.00005 | -0.913% | 마이너스 유지, 낙폭 소폭 완화 |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BTC [지속] | dYdX | $45.57M | $19.24M | -0.000007 | +7.95% | 오라클가 $69,453.78, BTC 랠리 지속 |
| **ETH** [지속] | dYdX | $112.72M | $22.80M | -0.0000221 | **+18.24%** | 오라클가 $2,258.37, ETH 랠리 지속 |
| SOL [일치] | dYdX | $1.66M | $4.77M | 0.0 | +10.63% | 오라클가 $85.01, 부모 기준과 사실상 일치 |
| BTC [지속] | Hyperliquid | $5,660.00M | $2,390.00M | 0.00001 | +7.94% | 거래량·OI 확대, 랠리 지속 |
| **ETH** [지속] | Hyperliquid | $4,040.00M | $1,950.00M | 0.00001 | **+18.42%** | OKX·dYdX와 독립 수렴 지속 |
| BTC [지속] | Aster | $1,841.75M | $858.31M | 0.00008 | +7.927% | 거래량·OI 확대, 랠리 지속 |
| ETH [truncation 26연속] | Aster | — | — | — | — | 545개 티커 응답에서 순수 ETH 항목 부재 지속 |
| 1000RATS [완화] | Aster | $0.17M | $0.07M | 0.00006 | -4.127% | 낙폭 추가 완화 |
| AIO [확대] | Aster | $0.03M | $0.08M | 0.00005 | -9.725% | CEX와 동조 확대 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALLO [확대] | Aster | $0.08M | $0.07M | 0.0 | -5.148% | CEX와 동조 확대 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| APR [수렴] | Aster | $0.09M | $0.27M | 0.00001 | -4.42% | ⚠️CEX(-4.2~-4.8%)와 방향 수렴, 벤뉴간 괴리 해소 |
| APR [미상장] | Hyperliquid | — | — | — | — | 이번 회차도 HL 미상장 재확인 |
| **BANK** [⚠️whipsaw 종료] | Aster | $0.08M | $0.24M | 0.00001 | **-2.011%** | 마이너스 유지, CEX와 동조 — 3회 whipsaw 후 처음 반전 없음 |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [확대] | Aster | $0.15M | $0.13M | 0.00001 | +2.226% | 플러스권 확대 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **CAP** [⚠️4회차 whipsaw] | Aster | $0.10M | $0.15M | 0.00001 | **+2.26%** | 마이너스→플러스 재반전(4회차째), OKX와 동조 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| FARTCOIN [⚠️완화] | Hyperliquid | $17.02M | $31.04M | 0.00001 | +9.40% | 상승폭 지속 완화(12.0%→10.05%→9.40%) |
| ETHFI [⚠️냉각] | Hyperliquid | $4.65M | $10.94M | 0.00001 | +6.36% | 상승폭 냉각(9.48%→6.36%), OKX와 동조 |
| HYPER [완화] | Hyperliquid | $0.11M | $0.20M | 0.00001 | +6.603% | 상승폭 소폭 냉각 |
| **APEX** [⚠️전환] | Hyperliquid | $0.23M | $0.69M | 0.00001 | **-1.466%** | 플러스→마이너스 전환, Bybit와 방향 일치 |
| HYNA:BTC-USD [지속] | Hyperliquid | $1.03M(이월) | $2.50M(이월) | 0.00001(이월) | +7.92% | 기초자산(BTC) 랠리 반영, vol/OI는 이월 |
| **HYNA:ETH-USD** [지속] | Hyperliquid | $1.14M(이월) | $1.84M(이월) | 0.00001(이월) | **+18.21%** | 기초자산(ETH) 랠리 반영, vol/OI는 이월 |
| **HYNA:HYPE** [완화] | Hyperliquid | $0.39M(이월) | $0.71M(이월) | 0.00002(이월) | **+19.36%** | 기초자산(HYPE) 상승폭 완화 반영, vol/OI는 이월 |
| HYNA:PUMP [이월] | Hyperliquid | $0.02M(이월) | $0.17M(이월) | 0.00001(이월) | +2.88%(미확인) | 별도 기초자산, 이번 회차 재조회 못함 |
| HYNA:SOL-USD [일치] | Hyperliquid | $0.22M(이월) | $0.59M(이월) | 0.00002(이월) | +10.63% | 기초자산(SOL) 랠리 반영, vol/OI는 이월 |

## 테마 태그 (요약)

1. BTC 랠리 고점 횡보 지속(+7.92% 기준, dYdX·HL·Aster 수렴) (majors-rally-continues)
2. ETH 랠리 지속(+18.21~18.42%, dYdX·HL 수렴) (majors-rally-continues)
3. ⚠️HYPE 3회 연속 상승폭 완화(22.5%→19.9%→19.36%) (hype-cools-slightly)
4. SOL 동반 확대 지속(dYdX +10.63%, 부모 기준과 사실상 일치) (majors-rally-continues)
5. AAVE 상승폭 재확대(+10.8~11.0%) (aave-extends-gains)
6. ⚠️ADA 3회차째 냉각(+6.9~7.2%), AAVE와 상반 (ada-cools-slightly)
7. ALGO 상승폭 유지 (algo-extends-gains)
8. ⚠️CASHCAT 3회 연속 상승폭 확대(HL +35.5%·Aster +35.8%), 온체인 워치와 정합, 촉매 미확인 (cashcat-extends-surge)
9. ATOM 5벤뉴 수렴 지속, 안정적 플러스 (atom-resolves-positive-all-venues)
10. ALLO 혼조 — Binance만 완화, OKX·Bybit는 -4.2%대 유지 (allo-mixed)
11. ⚠️BANK 3회 whipsaw 후 처음 반전 없이 마이너스 지속 (bank-holds-negative)
12. ⚠️CAP 4회차째 whipsaw — 마이너스→플러스 재반전 (cap-whipsaws-fourth-time)
13. APR 벤뉴간 괴리 해소 — CEX·Aster 모두 마이너스로 수렴 (apr-venue-converges)
14. ✅CORE 티커충돌 해소 판정 유지 — Binance 7회차 연속 완전 소실 (core-ticker-collision-resolved)
15. (b) Binance CG truncation 7회차 연속, 대상 13종목 — 대체경로(fapi 직접) 재시도도 451로 실패 (binance-cg-fetch-truncation-persists-7th-round)
16. ⭐Aster ASTER 자체토큰 OI $233.5M로 3회 연속 근접 재현 — 이상치 아닌 지속 수준으로 확정 (aster-token-oi-confirmed-elevated)
17. BEAT 홀로 역행 지속(-27.7/28.2%), 랠리 국면 소외 유지 (beat-remains-laggard)
18. ⚠️BTW(Aster) 낙폭 큰 폭 확대(-8.78%→-21.14%) (btw-decline-widens-sharply)
19. AEON 낙폭 완화 지속 (aeon-decline-eases)
20. ALPINE 낙폭 유지 (alpine-decline-eases)
21. ⚠️ETHFI 상승폭 냉각(9.48~9.84%→6.36~6.77%) (ethfi-extends-gains)
22. BICO 낙폭 완화 (bico-steady-decline)
23. GALA 플러스권 확대 지속 (gala-turns-positive)
24. ⚠️APEX 플러스→마이너스 전환(Bybit·HL 동조) (apex-turns-negative)
25. GIGGLE 플러스권 소폭 냉각 (giggle-extends-positive)
26. MMT 플러스권 추가 확대 (mmt-extends-positive)
27. GRAM 플러스권 유지, 진폭 축소 (gram-extends-positive)
28. ⚠️PIPPIN 플러스권 냉각 (pippin-extends-positive)
29. BSB 플러스권 확대 (bsb-extends-gains)
30. AIO 낙폭 확대(-9.5%→-11.0%) (aio-decline-widens)
31. 1000RATS 낙폭 추가 완화 (1000rats-eases-slightly)
32. ASTER(자체) CEX 4벤뉴 수렴(+5.8~5.9%)으로 상승폭 확대 (aster-cex-extends)
33. KAITO 상승폭 유지 (kaito-reaccelerates)
34. ACE 낙폭 지속, 펀딩 신규 최대(-0.00442, Bybit) (ace-decline-persists)
35. ⚠️FARTCOIN 상승폭 지속 완화(12.0%→10.05%→9.40%) (fartcoin-cools-slightly)
36. BLESS 마이너스 유지, 낙폭 소폭 완화 (bless-reverses-negative)
37. HYPER 상승폭 소폭 냉각 (hyper-reaccelerates)
38. HYNA:* 계열(HL) 기초자산 랠리 반영, vol/OI/funding은 대부분 이월(HL API POST 전용) (hyna-values-carried-forward)
39. 데이터: HL API POST 전용이라 CoinGecko 소스로 대체, 신선값이 dYdX·부모 기준과 근접해 이상 없음 확인 (hl-api-post-only-workaround)
40. 데이터: OKX 벌크+개별 open-interest 혼합조회로 대부분 신선 확보, funding은 대부분 이월 (okx-mixed-fetch-strategy)
41. 데이터: Binance CG truncation 7회차 연속 확정, 대체경로(fapi 직접) 시도했으나 451 지속 확인 (binance-cg-fetch-truncation-persists-7th-round)
42. 데이터: OrangeX 44회차(약 89.75h) 서비스 중단 지속 (orangex-outage-continues)
43. 데이터: ⚠️Aster ETH truncation 26회차 연속, 완전 부재 지속 (aster-eth-truncation-continues)
44. 데이터: ✅CORE 티커충돌 해소 판정 유지 (core-ticker-collision-resolved)
45. 데이터: ⭐Aster ASTER 자체토큰 OI 이상치, 3회 연속 재현으로 확정 판정 종결 (aster-token-oi-confirmed-elevated)
46. 데이터: Bybit 다수 종목 신선 재조회 성공(직전 이월 다수 해소, ASTER 포함) (bybit-refresh-improved)
47. 데이터: funding 절대값 점검 — 최댓값 Bybit ACE -0.00442(신규 최대), 중앙값 1e-5~1e-4대 정상 범위 (funding-sanity-check-passed)
48. 주식화·상품·프리IPO 합성 perp 토큰 전부 제외, 리스트 전 종목 크립토 네이티브 확인 유지 (stock-commodity-tokens-excluded-crypto-native-confirmed)

## 한계

(a) 메이저 랠리는 부모 세션이 확정한 기준값을 스카우트가 dYdX·HL·Aster 3개 독립 벤뉴로
재확인해 정합성을 확보했다. (b) Binance CoinGecko truncation은 7회차 연속이며, 대체
경로로 fapi.binance.com 직접 조회를 재시도했으나 이 컨테이너 환경에서 여전히 HTTP 451
(지역차단)로 막혀 실패로 기록한다. 다만 이번 회차 12개 종목(ACE·APR·ALPINE·ATOM·AAVE·
ADA·ALGO·BANK·AIO·ALLO·1000RATS·ASTER)이 CoinGecko에서 신선 복구돼 truncation 범위는
BICO·GALA·ETHFI·CAP·GIGGLE·MMT·GRAM·PIPPIN·BSB·KAITO·BTW·CORE·BEAT 13종목으로 좁혀진
상태다. (c) ALLO OI 이슈는 과거 회차로 재추적을 종료했다. (d) OrangeX 전면 중단이 44회차·
약 89.75시간째 지속된다. (e) Aster ETH truncation이 26회차 연속이며, 완전 부재 양상이
이어지고 있다. (f) Hyperliquid 공식 API는 POST 전용이라 이 컨테이너의 GET 전용 WebFetch로
직접 조회가 불가능해 CoinGecko hyperliquid 소스로 대체했다 — 신선값이 dYdX·부모 기준과
근접해 신뢰도는 확인했으나 원천 API 직접조회는 아니다. (g) CASHCAT의 지속 급등은 두 개
이상의 독립 벤뉴가 3회 연속 교차확인했고 온체인 워치의 회전율 하락 관측과도 정합적이나,
개별 촉매(뉴스)는 이번 회차도 확인하지 못했다. (h) Aster ASTER(자체토큰) OI 이상치는 3회
연속 근접 재현($228.5M→230.8M→233.5M)으로 이상치가 아닌 지속 수준으로 확정 판정을
종결했다. (i) 주식화·상품·프리IPO 합성 perp 토큰은 이번 회차도 전부 제외했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
