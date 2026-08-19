# 선물시장 스카우트 브리핑 — 2026-08-19 18:30 UTC (KST 2026-08-20 03:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 16:30 UTC)로부터 2시간 경과(정상 간격).**

## ⚠️ 이번 회차 최우선 과제 (a)(b) 상태

### (a) 메이저(BTC·ETH·HYPE·SOL) chg24 오염 — **2회차 연속 재현**

HL·Aster·dYdX 세 소스 모두 이번 회차도 BTC·ETH·HYPE·SOL의 chg24가 **+5~9%대**로 반환됐다
(HL: BTC +5.424%·ETH +8.947%·HYPE +6.119%, Aster: BTC +5.365%, dYdX 오라클가: BTC
$68,229.55·ETH $2,086.39·SOL $81.99). WebSearch 실측은 BTC $64,300~64,900(+0.29~0.5%)·
ETH ~$1,917(+2.1%)·SOL ~$77(+3%)로 명백히 불일치했다.

**신규 발견**: 이번 회차 CoinGecko의 범용 `simple/price` 엔드포인트(파생 티커가 아닌 대표
시세)를 직접 조회하니 **동일하게 BTC $68,244(+5.40%)·ETH $2,085.92(+8.91%)·SOL $81.95
(+6.23%)·HYPE $62.40(+6.44%)**를 반환했다. 이는 문제가 특정 파생 티커 엔드포인트나
WebFetch 요약 오류에 국한되지 않고 **CoinGecko 플랫폼 자체의 메이저 4종 데이터**에 있을
가능성을 높인다. 다만 **OKX 직접 API(CoinGecko 비경유)에서도 BTC last $68,214.6(open24h
$64,712.9, 내재 chg +5.41%)**로 유사값이 나와 원인이 완전히 규명되지는 않았다(OKX 자체
이슈이거나 도구 파이프라인의 더 광범위한 문제일 가능성도 배제 못함). WebSearch로 재확인한
글로벌 시총 검색에서도 '+0.5%'와 '+5.21%' 두 수치가 혼재해(후자는 CoinGecko 연계 소스로
추정) 같은 패턴의 정황 증거로 판단된다.

**처리**: 여전히 신뢰불가로 판단, 해당 메이저(BTC·ETH·HYPE의 HL/Aster, dYdX BTC·ETH·SOL)
및 HYNA:BTC-USD·HYNA:ETH-USD·HYNA:HYPE·HYNA:SOL-USD의 **chg24를 전부 직전값(16:30Z)으로
재이월**했다(HL·Aster는 vol/OI만 신선 채택, dYdX는 오라클가 훼손으로 전체 이월 유지).
HYNA:PUMP는 별도 기초자산이라 신선값(+11.53%)을 채택했다.

### (b) Binance CoinGecko truncation — **3회차 연속, 이번 회차 대상 확대**

기존 10종목(BICO·GALA·ETHFI·CAP·GIGGLE·MMT·GRAM·PIPPIN·BSB·KAITO)에 더해 **BTW·BEAT도
이번 회차 재실패**했다(BTW는 직전 회차에 신선값을 확보했던 종목이라 이번은 재발 성격).
전부 직전값을 이월했다(대부분 타 벤뉴에서는 신선값 확보돼 방향성 교차확인 가능). BEAT는
자체 신뢰불가 이슈와 별개로 이번엔 Binance fetch 자체가 안 됐다(3회차 연속 문제 지속,
다만 이번엔 '값이 이상함'이 아니라 '값 자체가 없음'). **CASHCAT의 Aster/HL은 이번 회차도
오염 없이 정상 작동**했고 오히려 극적으로 방향 반전했다(아래 참고).

## 시장 전반 — 이번 회차 핵심

1. **⚠️ATOM 5개 벤뉴(Binance·Bybit·HL·Aster) 전부 플러스→마이너스로 뚜렷이 반전**
   (-0.2~-2.9%) — 직전 회차의 '전 벤뉴 플러스 전환'과 정반대. OKX는 재탐지 실패로 구값 유지.
2. **⚠️CASHCAT이 HL(+6.878%)·Aster(+7.018%) 모두 마이너스에서 뚜렷한 플러스로 반전** —
   온체인 워치에서도 h24가 7연속 개선 끝에 첫 양전 전환(+1.37%)을 보고한 것과 같은 방향,
   두 경로가 수렴한다.
3. **1000RATS이 3벤뉴 전부 -21~-23%대에서 -14%대로 크게 회복**, 극단적 하락권에서 벗어나는
   조짐.
4. **⚠️APR·ALLO가 각각 3개 벤뉴(Binance·Bybit·Aster)에서 나란히 마이너스→플러스로 전환**
   (OKX만 재탐지 실패로 구값 유지).
5. **⚠️BANK는 Binance·Bybit에서 플러스→마이너스로 재반전**(Aster는 플러스 유지) — 벤뉴간
   혼조.
6. **BEAT가 OKX(-27.66%)·Aster(-27.23%) 모두 낙폭을 크게 확대**(-17~-21%대→-27%대), 두
   벤뉴가 정합적으로 심화를 보여 신뢰도 있는 관측.
7. **⚠️BTW의 Aster 값이 +47.957%→-14.655%로 극적으로 반전**했으나, Binance 교차확인이
   이번 회차 불가(truncation)해 단독 소스 관측 — 다음 회차 재확인 필요.
8. **AAVE·ADA·ALGO는 전 벤뉴에서 계속 플러스권이나 상승폭이 다소 진정**(+2.9~3.4%대로
   수렴). APEX·HYPER·FARTCOIN·ETHFI·GRAM·MMT(반대로 확대)·KAITO(OKX·HL 플러스 전환 뚜렷)
   등도 각자 방향은 유지한 채 강도만 조정됐다.

OKX는 이번 회차 open-interest 벌크 엔드포인트 재조회 결과가 종목별로 oi/oiCcy 배율이
**1배~100배로 뒤죽박죽**(예: BEAT는 oiCcy가 oi의 10배, AAVE는 oiCcy가 oi의 0.1배) 나와
내부적으로 비일관적이라 신뢰불가 판정, **OI는 전부 직전값 이월**했다. vol/chg는
ticker(last×volCcy24h) 방식으로 다수 신선 확보했으나 ACE·CAP·CORE·ATOM·BSB·APR·ALLO는
이번 회차 ticker에서도 탐지 실패해 이월했다. OKX funding은 이번 회차도 개별 fetch
미실시로 대부분 이월. **OrangeX는 40회차·약 81.75시간째 전면 중단** 지속. **Aster의 ETH
truncation은 22회차 연속** 지속. 저장 직전 전 항목 funding 절대값 점검 결과 최댓값은 ACE
Bybit -0.00236(직전 최대 0.00351 대비 완화)이며 중앙값은 대체로 1e-5~1e-4대로 정상 범위.
**글로벌 시총은 WebSearch 기준 약 $2.3조 안팎(소스별 $2.29~2.32조 편차), BTC 도미넌스는
소스별 56.5~59.8%로 큰 편차, Fear&Greed는 46(Fear)으로 다소 회복세.**

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

funding은 raw fraction 기준(CoinGecko 파생 소스는 퍼센트를 /100 적용). "[이월]"은 이번 회차
fetch 실패·데이터 신뢰불가로 직전값을 그대로 이어받은 필드.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| ACE [안정화] | Binance(직접API) | $403.61M | $12.21M | -0.00217 | -17.509% | 낙폭 안정화, 4벤뉴 -17~18%대 유지 |
| ACE [안정화] | Bybit(직접API) | $96.77M | $5.70M | -0.00236 | -17.978% | 펀딩 절대값 다소 완화되나 최대권 유지 |
| BTW [이월] | Binance(재실패) | $984.37M | $132.76M | 0.00129(이월) | +48.98% | 직전엔 성공했던 종목이 이번 재실패 |
| **BEAT** [심화] | OKX(직접API) | $84.51M | $5.04M | 0.00027(이월) | **-27.66%** | 낙폭 대폭 확대, Aster와 정합적 |
| BEAT [이월,3회연속] | Binance | $96.21M | $10.70M | 0.00028 | -18.062% | 3회차 연속 fetch 실패 |
| BICO [완화] | OKX(직접API) | $14.99M | $2.38M | 0.00005(이월) | -12.70% | 낙폭 완화, Aster와 정합적 |
| BICO [이월,3회연속] | Binance | $14.11M | $5.21M | -0.00058 | -12.292% | fetch 3회차 연속 실패 |
| GALA [이월,3회연속] | Binance | $18.97M | $6.49M | 0.0000274 | -3.767% | fetch 3회차 연속 실패 |
| GALA [심화] | OKX(직접API) | $5.87M | $1.58M | 0.0001(이월) | -2.775% | 낙폭 소폭 심화 |
| ETHFI [이월,3회연속] | Binance | $17.88M | $22.55M | -0.0000096 | +0.041% | fetch 3회차 연속 실패 |
| ETHFI [진정] | OKX(직접API) | $8.51M | $4.04M | -0.0000514(이월) | +3.051% | 상승폭 진정(+5.5%→+3.1%) |
| CAP [이월,3회연속] | Binance | $21.87M | $15.02M | -0.00007 | +0.973% | fetch 3회차 연속 실패 |
| CAP [이월] | OKX(재탐지 실패) | $71.28M | $11.34M | -0.0000677(이월) | +3.982% | 이번 회차 재탐지 실패로 이월 |
| AEON [완화] | OKX(직접API) | $35.44M | $2.83M | 0.00005(이월) | -14.152% | 낙폭 완화(-16.4%→-14.2%) |
| AEON [완화] | Bybit(직접API) | $2.09M | $0.81M | 0.00005 | -15.236% | 동조 완화 |
| APEX [진정] | Bybit(직접API) | $1.33M | $1.77M | 0.00005 | +5.255% | 상승폭 진정(+9.8%→+5.3%) |
| GIGGLE [이월,3회연속] | Binance | $15.24M | $10.97M | 0.00005 | -2.679% | fetch 3회차 연속 실패 |
| GIGGLE [전환] | OKX(직접API) | $7.88M | $1.67M | 0.00005(이월) | +1.013% | 보합에서 플러스권 소폭 진입 |
| ALPINE [유지] | Binance(직접API) | $31.34M | $2.00M | 0.00005 | -15.529% | 깊은 하락권 유지, 소폭 개선 |
| ALPINE [유지] | Bybit(직접API) | $6.50M | $0.62M | 0.00005 | -15.246% | 동조 유지, 소폭 심화 |
| CORE [이월] | OKX(재탐지 실패) | $2.61M | $1.03M | 0.00008 | +4.583% | 이번 회차 재탐지 실패, Binance 미상장 지속 |
| **ATOM** [이월] | OKX(재탐지 실패) | $3.74M | $3.75M | -0.00015 | +1.708% | ⚠️타 4벤뉴는 마이너스 반전, OKX만 구값 |
| **ATOM** [반전] | Binance(직접API) | $17.05M | $15.40M | 0.00006 | **-0.209%** | ⚠️플러스→마이너스 반전 |
| ATOM [반전] | Bybit(직접API) | $6.69M | $14.06M | -0.00034 | -0.418% | 동조 반전 |
| AAVE [진정] | OKX(직접API) | $26.28M | $11.47M | 0.00002(이월) | +3.037% | 모멘텀 진정 |
| AAVE [진정] | Binance(직접API) | $75.93M | $46.47M | 0.0001 | +2.926% | 동조 진정 |
| AAVE [진정] | Bybit(직접API) | $25.19M | $38.79M | 0.0001 | +2.963% | 동조 진정 |
| ADA [확대] | OKX(직접API) | $50.52M | $28.06M | -0.00012(이월) | +3.330% | 플러스권 소폭 확대 |
| ADA [확대] | Binance(직접API) | $132.02M | $84.82M | 0.00003 | +3.387% | 동조 확대 |
| ADA [확대] | Bybit(직접API) | $59.94M | $55.37M | -0.00007 | +3.211% | 동조 |
| ALGO [진정] | Binance(직접API) | $10.17M | $7.65M | 0.00009 | +3.207% | 플러스권 유지, 다소 진정 |
| ALGO [진정] | OKX(직접API) | $4.58M | $2.70M | 0.0001(이월) | +2.940% | 동조 진정 |
| ALGO [진정] | Bybit(직접API) | $3.59M | $6.31M | 0.00006 | +3.155% | 동조 |
| **MMT** [확대] | OKX(직접API) | $6.23M | $2.47M | -0.00024(이월) | **+9.325%** | 플러스권 확대 지속(+5.5%→+9.3%) |
| MMT [이월,3회연속] | Binance | $5.39M | $8.16M | -0.00009 | -2.043% | fetch 3회차 연속 실패 |
| GRAM [진정] | OKX(직접API) | $3.22M | $6.41M | 0.00005(이월) | +1.663% | 플러스권 유지, 다소 진정 |
| GRAM [이월,3회연속] | Binance | $8.13M | $14.12M | 0.00005 | +1.459% | fetch 3회차 연속 실패 |
| PIPPIN [회복] | OKX(직접API) | $1.95M | $1.81M | 0.00005(이월) | -0.386% | 마이너스→거의 보합 회복 |
| PIPPIN [이월,3회연속] | Binance | $4.86M | $5.70M | 0.00005 | -1.285% | fetch 3회차 연속 실패 |
| BSB [이월] | OKX(재탐지 실패) | $3.87M | $2.16M | 0.00032 | -0.0816% | 이번 회차 재탐지 실패(Aster는 신선 +1.9%) |
| BSB [이월,3회연속] | Binance | $12.03M | $8.74M | 0.00011 | -1.701% | fetch 3회차 연속 실패 |
| **BANK** [반전] | Binance(직접API) | $25.92M | $10.85M | -0.00003 | **-1.646%** | ⚠️플러스→마이너스 재반전 |
| BANK [반전] | Bybit(직접API) | $3.01M | $4.02M | -0.00021 | -1.402% | 동조 재반전(Aster는 여전히 플러스) |
| APR [이월] | OKX(재탐지 실패) | $40.27M | $2.85M | 0.00005 | -3.532% | ⚠️타 3벤뉴는 플러스 전환, OKX만 구값 |
| **APR** [전환] | Bybit(직접API) | $5.94M | $3.17M | 0.00005 | **+3.45%** | ⚠️마이너스→플러스 전환 |
| APR [전환] | Binance(직접API) | $34.96M | $10.93M | 0.00005 | +3.4% | 동조 전환 |
| AIO [완화] | Binance(직접API) | $11.81M | $4.03M | 0.00005 | -6.603% | 마이너스 폭 완화 지속 |
| AIO [완화] | Bybit(직접API) | $1.21M | $1.14M | 0.00005 | -6.702% | 동조 완화 |
| **ALLO** [전환] | Binance(직접API) | $26.03M | $11.84M | 0.00005 | **+1.179%** | ⚠️마이너스→플러스 전환 |
| ALLO [이월] | OKX(OI 신뢰불가) | $23.90M | $3.20M | 0.00005 | -1.84% | ⚠️OKX만 마이너스 유지(재확인 보류) |
| ALLO [전환] | Bybit(직접API) | $3.36M | $4.22M | -0.00002 | +1.283% | 동조 전환 |
| **1000RATS** [회복] | Binance(직접API) | $29.49M | $12.41M | 0.00005 | **-14.2%** | 극단적 하락권에서 크게 회복(-21.3%→-14.2%) |
| 1000RATS [회복] | Bybit(직접API) | $12.27M | $4.66M | 0.00022 | -14.598% | 동조 회복 |
| ASTER(자체) [안정] | Binance(직접API) | $19.89M | $70.42M | 0.00005 | +0.715% | 안정적 플러스권 유지, 다소 진정 |
| ASTER(자체) [안정] | OKX(직접API) | $4.09M | $8.42M | 0.0001(이월) | +0.899% | 동조 안정 |
| ASTER(자체) [안정] | Bybit(직접API) | $2.55M | $39.93M | 0.00005 | +0.732% | 동조 안정 |
| **KAITO** [전환] | OKX(직접API) | $25.70M | $5.31M | 0.0000060(이월) | **+2.642%** | ⚠️보합→뚜렷한 플러스 전환, HL과 동조 |
| KAITO [이월,USDT,3회연속] | Binance | $33.30M | $15.03M | -0.00009 | +4.644% | fetch 3회차 연속 실패 |
| KAITO [이월,USDC,3회연속] | Binance | $3.82M | $1.14M | -0.00009 | +3.695% | fetch 3회차 연속 실패 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 40회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).
⚠️표시는 이번 회차 chg24 이상치로 직전값을 이월한 행(메이저 관련) 또는 신규 급변동/미확인 행.

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| ACE [안정화] | Hyperliquid | $2.19M | $1.70M | -0.00056 | -17.998% | CEX와 동조, 낙폭 안정화 |
| ACE [안정화] | Aster | $0.89M | $0.18M | -0.00047 | -17.653% | 동조 유지 |
| ACE [중단] | OrangeX | — | — | — | — | 40회차·약 81.75시간 |
| **BTW** [급반전⚠️] | Aster | $13.46M | $6.55M | 0.00011 | **-14.655%** | 직전 +47.96%→급반전, Binance 미확인, 재확인 필요 |
| **KAITO** [전환] | Hyperliquid | $2.99M | $5.31M | 0.00001 | +2.841% | 보합→뚜렷한 플러스 전환, OKX와 동조 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **CASHCAT** [반전⚠️] | Hyperliquid | $12.67M | $14.74M | 0.00002 | **+6.878%** | 마이너스→뚜렷한 플러스 반전, 온체인 워치와 수렴 |
| CASHCAT [반전] | Aster | $0.94M | $0.86M | 0.00002 | +7.018% | 동조 반전 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GALA [심화] | Hyperliquid | $0.53M | $1.06M | -0.00011 | -2.703% | 낙폭 소폭 심화 |
| BEAT [심화] | Aster | $1.86M | $1.27M | 0.00001 | -27.232% | 낙폭 대폭 확대, OKX와 정합적 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BICO [완화] | Aster | $0.07M | $0.12M | -0.00024 | -13.323% | 낙폭 완화, OKX와 정합적 |
| BICO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| AEON [심화] | Aster | $0.10M | $0.28M | 0.00001 | -15.629% | 소폭 심화, CEX와 대체로 동조 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [진정] | Hyperliquid | $1.39M | $15.27M | 0.00001 | +1.541% | 플러스권 유지, 다소 진정 |
| **ATOM** [반전] | Hyperliquid | $0.50M | $1.74M | 0.00001 | -0.739% | ⚠️타 벤뉴와 함께 마이너스로 반전 |
| ATOM [반전] | Aster | $0.01M | $1.69M | 0.0001 | -2.897% | 동조 반전 |
| AAVE [진정] | Hyperliquid | $7.08M | $58.03M | 0.00001 | +3.02% | 동조 진정 |
| AAVE [진정] | Aster | $0.26M | $4.63M | 0.0001 | +2.892% | 동조 진정 |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ADA [확대] | Hyperliquid | $5.85M | $28.22M | 0.00001 | +3.136% | 동조 확대 |
| ADA [확대] | Aster | $0.55M | $1.30M | 0.0001 | +3.272% | 동조 확대 |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALGO [진정] | Hyperliquid | $0.60M | $1.97M | 0.00001 | +3.258% | 동조 진정 |
| ALGO [진정] | Aster | $0.005M | $0.04M | 0.00001 | +3.139% | 동조 |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ASTER(자체) [안정] | Aster | $16.40M | $223.48M | 0.00004 | +0.748% | 자체 OI 안정 유지 |
| ASTER(자체) [안정] | Hyperliquid | $0.87M | $13.62M | 0.00001 | +0.743% | 동조 안정 |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| HYPE ⚠️ | Hyperliquid | $406.46M | $1,408.98M | 0.00001 | -1.444%(이월) | chg 이상치 2회차 연속, 직전값 이월(vol/OI 신선) |
| BLESS [완화] | Aster | $0.03M | $0.08M | 0.00012 | -2.464% | 낙폭 뚜렷이 완화(-7.8%→-2.5%) |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BTC ⚠️ | dYdX | $3.23M(이월) | $17.96M(이월) | 0.0 | +0.808%(이월) | 오라클가 $68,229.55, 2회차 연속 시장과 괴리, 전체 이월 |
| ETH ⚠️ | dYdX | $6.23M(이월) | $22.38M(이월) | 0.0000197 | +1.036%(이월) | 동일 사유로 전체 이월 |
| SOL ⚠️ | dYdX | $0.22M(이월) | $5.04M(이월) | 0.0 | +1.789%(이월) | 동일 사유로 전체 이월 |
| BTC ⚠️ | Hyperliquid | $4,472.99M | $2,522.36M | 0.00001 | +0.616%(이월) | chg 이상치 2회차 연속(신선값 +5.42%), 직전값 이월 |
| ETH ⚠️ | Hyperliquid | $2,372.15M | $1,780.73M | 0.00001 | +0.744%(이월) | chg 이상치 2회차 연속(신선값 +8.95%), 직전값 이월 |
| BTC ⚠️ | Aster | $1,425.39M | $840.19M | 0.0001 | +0.606%(이월) | chg 이상치 2회차 연속(신선값 +5.37%), 직전값 이월 |
| ETH [truncation 22연속] | Aster | — | — | — | — | base=ETH 항목 부재 재확인 |
| **1000RATS** [회복] | Aster | $0.25M | $0.06M | 0.00002 | -14.868% | 극단적 하락권에서 크게 회복, CEX와 동조 |
| AIO [완화] | Aster | $0.03M | $0.08M | 0.00005 | -7.07% | CEX와 동조 완화 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **ALLO** [전환] | Aster | $0.10M | $0.06M | -0.00004 | +1.516% | ⚠️CEX(Binance·Bybit)와 함께 플러스로 전환 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **APR** [전환] | Aster | $0.09M | $0.30M | 0.00001 | +2.909% | ⚠️CEX(Binance·Bybit)와 함께 플러스로 전환 |
| APR [미상장] | Hyperliquid | — | — | — | — | 이번 회차도 HL 미상장 재확인 |
| BANK [유지] | Aster | $0.10M | $0.24M | 0.00001 | +0.699% | 플러스권 유지(CEX는 마이너스로 재반전) |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [전환] | Aster | $0.11M | $0.13M | 0.00001 | +1.883% | 마이너스에서 플러스로 전환 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CAP [진정] | Aster | $0.09M | $0.16M | 0.00001 | +1.392% | 플러스권 유지, 다소 진정 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| FARTCOIN [진정] | Hyperliquid | $6.72M | $32.79M | 0.00007 | +5.347% | 플러스 유지, 다소 진정(+7.6%→+5.3%) |
| ETHFI [진정] | Hyperliquid | $3.29M | $11.42M | 0.00001 | +3.917% | 플러스권 유지, 다소 진정, OKX와 동조 |
| HYPER [진정] | Hyperliquid | $0.06M | $0.20M | 0.00001 | +3.622% | 플러스권 유지, 다소 진정 |
| APEX [진정] | Hyperliquid | $0.21M | $0.68M | 0.00001 | +6.664% | Bybit와 함께 상승폭 진정 |
| HYNA:BTC-USD ⚠️ | Hyperliquid | $0.77M | $2.42M | 0.00001 | +1.292%(이월) | 기초자산 chg 이상치로 이월(vol/OI 신선) |
| HYNA:ETH-USD ⚠️ | Hyperliquid | $0.55M | $1.75M | 0.00005 | +2.14%(이월) | 기초자산 chg 이상치로 이월(vol/OI 신선) |
| HYNA:HYPE ⚠️ | Hyperliquid | $0.12M | $0.69M | -0.00002 | -1.0%(이월) | 기초자산 chg 이상치로 이월(vol/OI 신선) |
| HYNA:PUMP [신선] | Hyperliquid | $0.05M | $0.17M | 0.00003 | +11.53% | 별도 기초자산이라 신선값 채택, 안정적 강세 |
| HYNA:SOL-USD ⚠️ | Hyperliquid | $0.11M | $0.56M | 0.00001 | +3.205%(이월) | 기초자산 chg 이상치로 이월(vol/OI 신선) |

## 테마 태그 (요약)

1. ⚠️(a) 메이저 chg24 오염 2회차 연속, CoinGecko `simple/price`도 동일 오염값 반환(신규 발견) (majors-chg-anomaly-persists-2nd-round)
2. OKX 직접 API도 유사값 — 원인 완전 규명 안 됨 (okx-direct-api-shows-similar-anomaly)
3. (b) Binance CG truncation 3회차 연속, 이번 회차 BTW·BEAT까지 확대 (binance-cg-fetch-truncation-persists-3rd-round)
4. ⚠️ATOM 5벤뉴 플러스→마이너스 반전 (atom-reverses-negative)
5. ⚠️CASHCAT HL·Aster 마이너스→플러스 반전, 온체인 워치와 수렴 (cashcat-flips-positive)
6. 1000RATS 3벤뉴 -21~23%대→-14%대로 크게 회복 (1000rats-recovers-sharply)
7. ⚠️APR 3벤뉴 마이너스→플러스 전환 (apr-turns-positive)
8. ⚠️ALLO 3벤뉴 마이너스→플러스 전환 (allo-turns-positive)
9. ⚠️BANK Binance·Bybit 마이너스 재반전, Aster는 플러스 유지 — 혼조 (bank-reverses-negative)
10. BEAT OKX·Aster 낙폭 대폭 확대, 정합적 (beat-decline-widens-sharply)
11. ⚠️BTW Aster 급반전(+48%→-14.7%), 단독소스 관측 (btw-sharp-reversal-unconfirmed)
12. ACE 4벤뉴 -17~18%대 낙폭 안정화 (ace-decline-stabilizes)
13. BICO OKX·Aster 낙폭 완화 (bico-improves)
14. GALA OKX·HL 낙폭 소폭 심화 (gala-mixed)
15. ETHFI OKX·HL 플러스권 유지, 상승폭 진정 (ethfi-momentum-cools)
16. CAP Aster 플러스권 진정 (cap-momentum-cools)
17. AEON OKX·Bybit·Aster 대체로 낙폭 완화 (aeon-improves)
18. APEX Bybit·HL 상승폭 진정 (apex-momentum-cools)
19. GIGGLE OKX 보합→플러스권 진입 (giggle-turns-positive)
20. ALPINE Binance·Bybit 깊은 하락권 유지 (alpine-remains-deeply-negative)
21. CORE OKX 재탐지 실패로 이월 (core-carryover)
22. AAVE 전 벤뉴 플러스권, 모멘텀 진정 (aave-momentum-cools)
23. ADA 전 벤뉴 플러스권 소폭 확대 (ada-strengthens-mildly)
24. ALGO 전 벤뉴 플러스권, 모멘텀 진정 (algo-momentum-cools)
25. MMT OKX 플러스권 확대 지속(+5.5%→+9.3%) (mmt-extends-positive)
26. GRAM OKX·HL 플러스권 유지, 다소 진정 (gram-momentum-cools)
27. PIPPIN OKX 마이너스→거의 보합 회복 (pippin-recovers-to-flat)
28. BSB Aster 마이너스→플러스 전환 (bsb-turns-positive)
29. AIO 마이너스 폭 완화 흐름 지속 (aio-mildly-improves)
30. ASTER(자체토큰) 전 벤뉴 안정적 플러스권, 다소 진정 (aster-cex-stable)
31. BLESS(Aster) 낙폭 뚜렷이 완화 (bless-improves)
32. KAITO OKX·HL 보합→뚜렷한 플러스 전환 (kaito-turns-clearly-positive)
33. dYdX 오라클가 이상치 2회차 연속, 전체 이월 (dydx-oracle-anomaly-persists-2nd-round)
34. FARTCOIN 플러스 유지, 다소 진정 (fartcoin-momentum-cools)
35. HYPER 플러스권 유지, 다소 진정 (hyper-momentum-cools)
36. HYNA:* 계열(HL) HIP-3 빌더배포 마켓, 계속 포함 유지 (hyna-builder-deployed-markets)
37. 데이터: OKX OI 벌크 API 배율 비일관적(1~100배)이라 신뢰불가, 전부 이월 (okx-oi-bulk-scale-inconsistent-carryover)
38. 데이터: CASHCAT은 이번 회차도 오염 없이 정상 작동 (cashcat-aster-contamination-resolved)
39. 데이터: OrangeX 40회차(약 81.75h) 서비스 중단 지속 (orangex-service-outage-continues)
40. 데이터: Aster ETH truncation 22회차 연속 (truncation-continues-22nd-round)
41. 글로벌 시총 약 $2.3조 안팎(소스편차), BTC 도미넌스 56.5~59.8%(큰 편차), F&G 46 (global-market-cap-mixed-sources)
42. 주식화·상품 토큰 전부 제외 유지 (stock-commodity-tokens-excluded-crypto-native-confirmed)

## 한계

(a) **메이저(BTC·ETH·HYPE·SOL) chg24 오염이 2회차 연속 재현**됐고, 이번 회차 CoinGecko
`simple/price` 엔드포인트에서도 동일 오염값이 확인돼 문제의 소재가 CoinGecko 플랫폼 자체일
가능성이 커졌다. 다만 OKX 직접 API에서도 유사값이 나와 원인이 완전히 규명되지 않았다 —
다음 회차에도 계속 검증이 필요하다; (b) **Binance CG truncation은 3회차 연속**이며 이번
회차엔 BTW·BEAT까지 대상이 확대됐다; (c) **OKX OI 벌크 API가 이번 회차 종목별로 배율이
1~100배로 비일관적**이라 신뢰불가 판정, 전체 이월했다(vol/chg는 ticker 방식으로 신선
확보); (d) BTW의 Aster 급반전(+48%→-14.7%)은 Binance 교차확인이 이번 회차 불가해 단독
소스 관측이다 — 다음 회차 재확인이 필요하다; (e) OrangeX 전면 중단이 40회차·약 81.75시간째
지속된다; (f) Aster ETH truncation이 22회차 연속 지속된다; (g) 글로벌 시총·도미넌스는
WebSearch 교차확인 기준이며 소스별 편차가 상당히 컸다(시총 +0.5%~+5.21%, 도미넌스
56.5~59.8%); (h) 주식화·상품·프리IPO 합성 perp 토큰은 이번 회차도 전부 제외했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
