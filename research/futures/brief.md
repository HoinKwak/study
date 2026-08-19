# 선물시장 스카우트 브리핑 — 2026-08-19 12:30 UTC (KST 2026-08-19 21:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 10:30 UTC)로부터 2시간 경과(정상 간격).**

## ⚠️ 이번 회차 최대 이슈 — ACE 숏스퀴즈 완전 소멸(전량 반납)

직전 회차(10:30Z)에서 "재점화"로 판단했던 ACE 숏스퀴즈(4벤뉴 전부 +20~21%대)가 **불과 2시간 만에
거의 전부 반납**됐다:

| 벤뉴 | 10:30Z | 12:30Z |
|---|---|---|
| Binance | +21.358% | **+1.549%** |
| Bybit | +20.635% | **+1.679%** |
| Hyperliquid | +21.177% | **+2.377%** |
| Aster | +21.44% | **+4.845%** |

펀딩도 동반 완화(덜 음수)됐다: Binance -0.00217→**-0.00154**, Bybit -0.00276→**-0.00144**,
HL -0.00087→**-0.00045**, Aster -0.00046→**-0.0003**. 직전 회차의 "재점화" 판단 자체는 그
시점 데이터로는 정확했으나, ACE는 이제 **"급등→급락"을 반복하는 극도로 변동성이 큰 국면**임이
재확인된다 — 다음 회차에 다시 재점화될 가능성을 배제할 수 없다.

## 시장 전반 — 이번 회차 핵심

1. **ACE 완전 소멸(상단 참고)** — 이번 회차 최대 이슈.
2. **BTW 뚜렷한 냉각으로 전환**: 7회차 연속 고공권(+85~90%대)에 있다가 Binance
   +85.368%→**+67.198%**, Aster +87.01%→**+67.059%**로 양 벤뉴 동시에 약 18~20%p 큰 폭
   하락. 펀딩은 Binance 기준 0.00135→**0.00129414**로 소폭만 완화돼 과열 완전 해소는 아님.
   OI는 Binance $162.22M→**$148.23M**로 감소, 포지션 축소 동반.
3. **BEAT는 3벤뉴 전부 낙폭이 뚜렷이 좁혀지며 -18%대로 수렴**: OKX -24.784%→**-18.12%**,
   Binance -23.284%→**-18.062%**, Aster -25.1%→**-18.182%**로 직전 회차의 벤뉴간 괴리가
   해소됐다.
4. **1000RATS는 Binance·Bybit에서 급반전**: +7.604%→**-2.293%**(Binance),
   +8.241%→**-2.019%**(Bybit)로 마이너스 전환했으나 **Aster는 +1.555%로 플러스 유지**
   (직전 +6.69%에서 둔화)해 새로운 벤뉴간 괴리가 발생했다.
5. **APR 전 벤뉴 큰 폭 진정**: OKX +6.685%→**+0.962%**, Bybit +6.859%→**+1.678%**,
   Binance +6.612%→**+2.299%**, Aster +8.4%→**+0.1%**로 고수준에서 거의 보합권까지 급랭.
6. **KAITO 반등 스트릭 지속**: OKX +4.024%→**+4.824%**, Binance +3.994%→**+4.644%**,
   HL +4.734%→**+4.690%**로 완만한 추가 상승·보합.
7. **CASHCAT 낙폭 6회차 연속 축소**(HL -10.257%→-7.995%→**-7.121%**), Aster도 동조
   (-8.10%→**-7.246%**).
8. **GALA 하락폭 축소로 전환**(전 벤뉴 -3.8~4.1%대: Binance -5.319%→-3.767%, OKX
   -5.319%→-4.05%, HL -5.125%→-3.772%).
9. **APEX·ALPINE·AEON**은 각각 재가속 이후 진정(+7.3~7.7%), 상승폭 지속 축소(+6.8%대),
   낙폭 축소 전환(-10.4~10.8%) 흐름.
10. **ETHFI는 Binance 기준 거의 완전 보합 전환**(-0.431%→**+0.041%**), HL은 소폭 마이너스
    지속(-0.659%). **CAP·CORE는 둘 다 마이너스에서 플러스로 재전환**.

**⚠️GALA OKX OI 수집 방식을 이번 회차부터 전환**: CoinGecko `okex_swap` 경유값을 아예 쓰지
않고 OKX 직접 bulk open-interest 엔드포인트(`/api/v5/public/open-interest?instType=SWAP`)로
수집했다. 결과값(oiCcy×last=**$1.72M**)이 과거 직접 API 단건조회 값($1.74M)과 근접해, 반복적으로
문제였던 CoinGecko 경유 방식(7.9배 부풀림)을 이번 회차부터 우회했다. 같은 방식으로
BICO·ATOM·AAVE·ADA·ALGO·APR·ASTER·KAITO 등 다수 종목의 OKX OI를 직접 계산했고 전부 과거
직접값과 근접해 방법론 안정성을 확인했다. 다만 **ALLO의 OKX OI만 $0.33M→$3.28M로 약 10배
급증**이 관측됐는데(다른 필드는 완만한 변화), 원인은 불명확해 다음 회차 재확인이 필요하다.

**dYdX는 이번 회차 CoinGecko `dydx_v4` 엔드포인트가 404를 반환**했으나(직전 회차엔 정상
작동), **dYdX 공식 인덱서 API(`indexer.dydx.trade`)로 직접 조회한 결과 BTC/ETH/SOL 3종목 모두
정상 작동**을 확인했다: BTC OI $17.48M→**$17.58M**, ETH OI $22.76M→**$22.91M**, SOL OI
$4.99M→**$5.02M**로 완만한 변화이며 서비스 자체는 문제 없다.

**메이저**: HL BTC +0.287%→**+0.357%**(vol $1,391.14M, OI $2,548.38M), ETH
+1.06%→**+1.184%**(vol $845.78M, OI $1,788.23M); Aster BTC +0.35%→**+0.394%**(vol
$497.29M, OI $802.96M), ETH는 **19회차 연속 truncation**; Binance BTC +0.34%→**+0.408%**
(vol $6,076.73M), ETH +1.088%→**+1.445%**(vol $4,645.59M, funding 0.0001). dYdX 오라클
기준 BTC 가격 약 $64,690로 직전 수준과 대체로 부합. **글로벌 시총·도미넌스는 WebSearch
재확인 결과 총 약 $2.2조·BTC 도미넌스 약 58.8%**로 직전과 대체로 동일.

**데이터 품질**: funding 단위 보정(CoinGecko 경유 percent→fraction, `/100`)을 이번 회차도
Binance·Bybit·HL·Aster 전 항목에 적용했고, OKX·Binance 직접 API는 이미 fraction이라 변환 없이
사용했다. 저장 직전 전 항목 funding 절대값 점검 결과 최댓값 0.00154(ACE Binance)로 직전
정상범위(최대 0.00276) 이내. **OrangeX는 37회차·약 75.75시간째 전면 중단** 지속. **MMT·GIGGLE
전체, GRAM/PIPPIN/BSB(OKX)·CAP(Binance OI·funding)·BICO(Binance OI)·ATOM(OKX vol·chg)·
KAITO(Binance OI 일부)·ETHFI(OKX chg)는 이번 회차도 시간·호출 제약상 일부 필드를 직전값으로
이어받았음**을 정직 표기한다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

funding은 raw fraction 기준.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **ACE** [소멸] | Binance(직접API) | $622.27M | $15.27M | -0.00154 | **+1.549%** | 숏스퀴즈 완전 소멸, 급등분 전량 반납 |
| ACE [소멸] | Bybit(CG대체) | $123.25M | $6.53M | -0.00144 | +1.679% | 동조 반납 |
| **BTW** [냉각] | Binance(직접API) | $821.85M | $148.23M | 0.00129 | +67.198% | 뚜렷한 냉각(+85%→+67%), OI 감소 |
| **BEAT** [수렴] | OKX(직접API) | $90.43M | $6.32M | 0.0003 | -18.12% | 낙폭 뚜렷한 완화, Binance와 수렴 |
| BEAT [수렴] | Binance(직접API) | $96.21M | $10.70M | 0.00028 | -18.062% | OKX와 거의 동일 수준으로 수렴 |
| BICO [유지] | OKX(직접API) | $12.67M | $2.53M | 0.00005 | -12.44% | -12%대 유지 |
| BICO [유지] | Binance(직접API) | $14.11M | $5.21M | -0.00058 | -12.292% | 펀딩 마이너스 전환(OI 직전값) |
| GALA [축소] | Binance(직접API) | $18.97M | $6.49M | 0.0000274 | -3.767% | 하락폭 축소, OKX·HL과 수렴 |
| GALA [축소] | OKX(직접API) | $5.52M | $1.72M | 0.0001 | -4.05% | 동조. OI 수집방식 CG우회로 전환 |
| ETHFI [보합] | Binance(직접API) | $17.88M | $22.55M | -0.0000096 | +0.041% | 거의 완전 보합 전환 |
| ETHFI [보합] | OKX(직접API) | $6.72M | $4.04M | -0.00012 | -0.472% | vol·OI·funding 갱신, chg는 fetch이상으로 직전값 |
| CAP [전환] | Binance(직접API) | $21.87M | $15.02M | -0.00007 | +0.973% | 마이너스→플러스 재전환(OI·funding 직전값) |
| CAP [전환] | OKX(직접API) | $59.96M | $11.79M | -0.00028 | +0.818% | 동조 플러스, funding 직접확인 |
| AEON [축소] | OKX(직접API) | $43.48M | $3.30M | 0.00005 | -10.625% | 낙폭 축소로 전환 |
| AEON [축소] | Bybit(CG대체) | $2.53M | $0.99M | 0.00005 | -10.434% | 동조 축소 |
| **APEX** [진정] | Bybit(CG대체) | $1.22M | $1.73M | 0.00005 | +7.313% | 재가속 이후 진정 지속 |
| GIGGLE [이월] | Binance(직접API) | $15.24M | $10.97M | 0.00005 | -2.679% | 시간제약상 전 필드 직전값 |
| GIGGLE [이월] | OKX(직접API 일부) | $8.39M | $1.73M | 0.00005 | -2.219% | 시간제약상 전 필드 직전값 |
| ALPINE [축소] | Binance(CG대체) | $69.51M | $2.10M | 0.00005 | +6.795% | 상승폭 지속 축소 |
| ALPINE [축소] | Bybit(CG대체) | $14.99M | $0.68M | 0.00005 | +6.791% | 동조 축소 |
| CORE [전환] | OKX(직접API) | $2.16M | $1.04M | 0.00008 | +2.77% | 마이너스→플러스, Binance 미상장 지속 |
| ATOM [보합] | OKX(직접API) | $3.37M | $3.73M | -0.00015 | +1.302% | OI 갱신, vol·chg 직전값 |
| ATOM [보합] | Binance(CG대체) | $14.54M | $15.31M | -0.00014 | +1.513% | 소폭 상승 지속 |
| ATOM [보합] | Bybit(CG대체) | $5.51M | $13.52M | -0.00012 | +1.149% | 동조 |
| AAVE [개선] | OKX(직접API) | $17.64M | $11.82M | 0.00002 | +0.112% | 보합→소폭 플러스 |
| AAVE [개선] | Binance(CG대체) | $42.90M | $44.01M | 0.00009 | -0.19% | 동조 개선 |
| AAVE [개선] | Bybit(CG대체) | $12.26M | $40.40M | 0.00006 | -0.078% | 동조 개선 |
| ADA [보합] | OKX(직접API) | $25.43M | $24.85M | -0.00012 | +0.46% | 완전보합→소폭 플러스 |
| ADA [보합] | Binance(CG대체) | $81.14M | $84.16M | -0.00006 | +0.691% | 동조 |
| ADA [보합] | Bybit(CG대체) | $37.77M | $55.20M | -0.00006 | +0.575% | 동조 |
| ALGO [플러스] | Binance(CG대체) | $7.47M | $7.77M | 0.0001 | +3.641% | 지속 확대 |
| ALGO [플러스] | OKX(직접API) | $3.31M | $2.61M | 0.0001 | +3.424% | 동조 확대 |
| MMT [이월] | OKX(직접API 일부) | $3.35M | $2.14M | -0.00024 | -1.752% | 시간제약상 전 필드 직전값 |
| MMT [이월] | Binance(직접API) | $5.39M | $8.16M | -0.00009 | -2.043% | 시간제약상 전 필드 직전값 |
| GRAM [보합] | OKX(직접API 일부) | $4.79M | $6.34M | 0.00005 | +0.304% | OI·funding 직전값 |
| GRAM [보합] | Binance(직접API) | $8.13M | $14.12M | 0.00005 | +1.459% | vol·chg 갱신 |
| PIPPIN [보합] | OKX(직접API 일부) | $2.87M | $1.71M | 0.00005 | -0.228% | 시간제약상 전 필드 직전값 |
| PIPPIN [보합] | Binance(직접API) | $4.86M | $5.70M | 0.00005 | -1.285% | vol·chg 갱신 |
| BSB [이월] | OKX(CG대체) | $5.25M | $2.19M | 0.00032 | +5.29% | 시간제약상 전 필드 직전값 |
| BSB [이월] | Binance(직접API) | $12.03M | $8.74M | 0.00011 | -1.701% | funding만 갱신 |
| BANK [보합] | Binance(CG대체) | $24.42M | $10.73M | 0.00005 | -0.084% | 낙폭 축소 |
| BANK [보합] | Bybit(CG대체) | $2.89M | $4.00M | 0.00005 | -0.113% | 동조 |
| **APR** [급랭] | OKX(직접API) | $67.56M | $3.34M | 0.00005 | +0.962% | 고수준에서 큰 폭 진정 |
| APR [급랭] | Bybit(CG대체) | $10.40M | $3.25M | 0.00005 | +1.678% | 동조 큰 폭 진정 |
| APR [급랭] | Binance(직접API) | $63.59M | $10.85M | 0.00005 | +2.299% | 동조 진정 |
| AIO [유지] | Binance(CG대체) | $17.87M | $4.06M | 0.00005 | -10.131% | 마이너스 유지 |
| AIO [유지] | Bybit(CG대체) | $1.75M | $1.18M | 0.00005 | -11.361% | 동조, 소폭 확대 |
| ALLO [진정] | Binance(CG대체) | $29.59M | $12.26M | 0.00005 | +0.761% | 플러스권에서 진정 |
| ALLO [진정] | OKX(직접API) | $26.66M | $3.28M | 0.00004 | +0.938% | ⚠️OI 10배 급증(원인불명) |
| ALLO [진정] | Bybit(CG대체) | $3.89M | $4.26M | 0.00005 | +1.05% | 동조 진정 |
| **1000RATS** [반전] | Binance(CG대체) | $86.34M | $12.72M | 0.00013 | -2.293% | 플러스→마이너스 급반전 |
| 1000RATS [반전] | Bybit(CG대체) | $32.50M | $4.63M | 0.00042 | -2.019% | 동조 급반전 |
| ASTER(자체) [안정] | Binance(CG대체) | $9.59M | $69.99M | 0.00005 | -0.216% | 안정 유지 |
| ASTER(자체) [안정] | OKX(직접API) | $2.29M | $8.24M | 0.00005 | -0.216% | 동조 |
| ASTER(자체) [안정] | Bybit(CG대체) | $1.37M | $39.73M | 0.00005 | -0.216% | 동조 |
| **KAITO** [반등] | OKX(직접API) | $26.10M | $5.02M | -0.00011 | +4.824% | 반등 스트릭 지속 |
| KAITO [반등] | Binance(직접API,USDT) | $33.30M | $15.03M | -0.00009 | +4.644% | 동조(OI 직전값) |
| KAITO [이월] | Binance(직접API,USDC) | $3.82M | $1.14M | -0.00009 | +3.695% | funding만 갱신 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 37회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **ACE** [소멸] | Hyperliquid | $1.62M | $1.78M | -0.00045 | +2.377% | CEX와 동조, 급등분 전량 반납 |
| ACE [소멸] | Aster | $1.01M | $0.20M | -0.0003 | +4.845% | 동조 반납 |
| ACE [중단] | OrangeX | — | — | — | — | 37회차·약 75.75시간 |
| **BTW** [냉각] | Aster | $10.02M | $12.03M | 0.00016 | +67.059% | Binance와 동조 뚜렷한 냉각 |
| **KAITO** [반등] | Hyperliquid | $2.09M | $5.88M | 0.00001 | +4.69% | CEX와 동조 반등 지속 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CASHCAT [지속 축소] | Hyperliquid | $9.05M | $12.65M | 0.00001 | -7.121% | 낙폭 6회차 연속 축소 |
| CASHCAT [지속 축소] | Aster | $0.66M | $0.71M | -0.00001 | -7.246% | 동조 축소 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GALA [축소] | Hyperliquid | $1.03M | $1.10M | -0.00011 | -3.772% | CEX 동조 개선 |
| **BEAT** [수렴] | Aster | $0.90M | $0.84M | 0.00001 | -18.182% | 낙폭 뚜렷한 완화, CEX와 수렴 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BICO [유지] | Aster | $0.05M | $0.10M | 0.00005 | -13.771% | -12%대에서 소폭 확대 |
| BICO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| AEON [축소] | Aster | $0.08M | $0.29M | 0.00001 | -10.79% | OKX와 함께 낙폭 축소 전환 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [보합] | Hyperliquid | $1.55M | $15.30M | 0.00001 | +1.636% | 보합에서 소폭 플러스 |
| ATOM [보합] | Hyperliquid | $0.41M | $1.75M | -0.00006 | +1.294% | 타 벤뉴 동조 |
| ATOM [보합] | Aster | $0.01M | $1.67M | 0.00008 | +1.875% | 동조 강화 |
| AAVE [개선] | Hyperliquid | $2.97M | $58.27M | 0.00001 | -0.106% | 동조 개선 |
| AAVE [개선] | Aster | $0.26M | $4.56M | 0.0001 | -0.045% | 동조 개선 |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ADA [보합] | Hyperliquid | $3.25M | $29.27M | -0.00003 | +0.518% | 동조 |
| ADA [보합] | Aster | $0.19M | $1.24M | 0.0001 | +0.345% | 동조 보합 |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALGO [플러스] | Hyperliquid | $0.36M | $1.80M | 0.00001 | +3.951% | 동조 강화 |
| ALGO [플러스] | Aster | $0.004M | $0.04M | 0.00001 | +3.081% | 동조 |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ASTER(자체) [안정] | Aster | $8.46M | $221.18M | 0.00004 | -0.2% | 자체 OI 안정 유지 |
| ASTER(자체) [안정] | Hyperliquid | $0.25M | $13.56M | 0.00001 | -0.24% | 동조 |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| HYPE [개선] | Hyperliquid | $183.95M | $1,325.40M | 0.00001 | -1.239% | 낙폭 완화, 여전히 마이너스 |
| BLESS [확대] | Aster | $0.02M | $0.09M | 0.00005 | -8.392% | 마이너스 확대 |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **BTC** [정상] | dYdX | $2.86M | $17.58M | 0.0 | +0.675% | CG 404, 공식 인덱서로 정상 확인 |
| **ETH** [정상] | dYdX | $2.49M | $22.91M | 0.0000024 | +1.449% | 정상 작동 확인 |
| **SOL** [정상] | dYdX | $0.25M | $5.02M | 0.0 | +1.829% | 정상 작동 확인 |
| BTC [안정] | Hyperliquid | $1,391.14M | $2,548.38M | 0.0 | +0.357% | 메이저 안정 |
| ETH [안정] | Hyperliquid | $845.78M | $1,788.23M | 0.0 | +1.184% | 메이저 안정 |
| BTC [안정] | Aster | $497.29M | $802.96M | 0.00003 | +0.394% | 메이저 안정 |
| ETH [truncation 19연속] | Aster | — | — | — | — | base=ETH 항목 부재 재확인 |
| 1000RATS [괴리] | Aster | $0.46M | $0.06M | 0.00003 | +1.555% | Binance·Bybit는 마이너스, Aster만 플러스 |
| AIO [유지] | Aster | $0.06M | $0.08M | 0.00005 | -10.004% | CEX와 동조 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALLO [진정] | Aster | $0.15M | $0.07M | 0.00001 | +1.308% | CEX와 동조, 진정 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| APR [급랭] | Aster | $0.29M | $0.29M | 0.00001 | +0.1% | CEX와 함께 큰 폭 진정 |
| APR [미상장] | Hyperliquid | — | — | — | — | 이번 회차도 HL 미상장 재확인 |
| BANK [보합] | Aster | $0.09M | $0.26M | 0.00001 | -0.056% | 보합 부근, CEX 동조 |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [유지] | Aster | $0.14M | $0.12M | 0.00002 | -1.185% | CEX와 동조 유지 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CAP [전환] | Aster | $0.06M | $0.17M | 0.0 | -0.085% | CEX와 함께 개선 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| FARTCOIN [반전] | Hyperliquid | $2.80M | $30.42M | 0.00004 | +0.957% | 마이너스→플러스 반전 |
| ETHFI [보합] | Hyperliquid | $3.76M | $11.37M | 0.00001 | -0.659% | 소폭 마이너스, Binance는 거의 보합 |
| HYPER [확대] | Hyperliquid | $0.05M | $0.20M | -0.00002 | +1.903% | 플러스권 유지, 소폭 확대 |
| **APEX** [진정] | Hyperliquid | $0.15M | $0.66M | 0.00001 | +7.704% | Bybit와 함께 진정 지속 |
| HYNA:BTC-USD | Hyperliquid | $0.34M | $2.17M | 0.00001 | +0.344% | HIP-3 빌더배포, BTC 동조 |
| HYNA:ETH-USD | Hyperliquid | $0.15M | $1.64M | 0.00001 | +1.083% | HIP-3 빌더배포, ETH 동조 |
| HYNA:HYPE | Hyperliquid | $0.16M | $0.66M | 0.00001 | -1.475% | HIP-3 빌더배포 |
| HYNA:PUMP | Hyperliquid | $0.05M | $0.16M | 0.00001 | +10.075% | HIP-3 빌더배포 |
| HYNA:SOL-USD | Hyperliquid | $0.03M | $0.53M | 0.00001 | +1.293% | HIP-3 빌더배포, 값 변화 없음 |

## 테마 태그 (요약)

1. ACE 숏스퀴즈 완전 소멸(전량 반납) — 직전 "재점화" 판단이 2시간 만에 반전 (ace-short-squeeze-fully-unwinds)
2. BTW 뚜렷한 냉각 전환(+85~87%→+67%대), OI 감소 동반 (btw-sharp-cooldown)
3. BEAT 3벤뉴 전부 -18%대로 수렴(벤뉴간 괴리 해소) (beat-converges-both-venues)
4. 1000RATS Binance·Bybit 급반전(마이너스), Aster만 플러스 유지(신규 벤뉴간 괴리) (1000rats-flips-negative-binance-bybit)
5. APR 전 벤뉴 큰 폭 진정(고수준→거의 보합) (apr-sharp-cooldown)
6. KAITO 반등 스트릭 지속 (kaito-rebound-continues)
7. CASHCAT 낙폭 6회차 연속 축소 (cashcat-narrows-continuously)
8. GALA 하락폭 축소 전환, OKX OI 수집방식 CG우회로 전환 (gala-decline-narrows)
9. BICO -12%대 유지, 소폭 확대 (bico-holds-near-12pct)
10. AEON 낙폭 축소 전환 (aeon-decline-narrows-now)
11. APEX 재가속 이후 진정 지속 (apex-continues-cooldown)
12. ETHFI Binance 거의 완전 보합, HL 소폭 마이너스 지속 (ethfi-near-flat-now)
13. CAP 마이너스→플러스 재전환 (cap-flips-positive)
14. CORE 마이너스→플러스 재전환, Binance 미상장 지속 (core-flips-positive)
15. ATOM/AAVE/ADA/ALGO 소폭 플러스권 지속·개선(세부 표 참고)
16. MMT/GIGGLE 전체, GRAM/PIPPIN/BSB(OKX 일부) 시간제약상 부분 이월 (partial-carryover-disclosed)
17. ALPINE 상승폭 지속 축소 (alpine-continues-cooldown)
18. ASTER(자체토큰) 전 벤뉴 안정권 유지 (aster-cex-stable)
19. HYPE 낙폭 완화, 여전히 마이너스권 (hype-mildly-improves)
20. FARTCOIN 마이너스→플러스 반전 (fartcoin-flips-positive)
21. HYPER 플러스권 유지, 소폭 확대 (hyper-holds-positive)
22. BLESS(Aster) 마이너스 확대 (bless-widens-negative)
23. ALLO 플러스권에서 진정, OKX OI 10배 급증(원인불명) (allo-cools-to-flat)
24. dYdX: CoinGecko 엔드포인트 404, 공식 인덱서로 정상 작동 재확인 (dydx-coingecko-404-direct-api-normal)
25. 메이저(BTC·ETH·SOL) 안정권 유지 (majors-remain-stable)
26. HYNA:* 계열 계속 포함 (hyna-builder-deployed-markets)
27. 데이터: OKX OI 수집방식을 CG경유→bulk 직접API로 전환, 방법론 검증 (okx-oi-methodology-shift-direct-bulk-api)
28. 데이터: OrangeX 37회차(~75.75h), Aster ETH truncation 19회차
29. 글로벌 시총·도미넌스 대체로 동일($2.2조·BTC 58.8%) (global-dominance-roughly-unchanged)
30. 주식화·상품 토큰 전부 제외 유지

## 한계

(a) **ACE 숏스퀴즈가 완전히 소멸(전량 반납)**돼 직전 회차의 "재점화" 판단이 2시간 만에 다시
뒤집혔다 — 극도로 변동성이 큰 국면이라 매 회차 재확인이 필요; (b) **CoinGecko `dydx_v4`
엔드포인트가 이번 회차 404**를 반환해 dYdX 공식 인덱서 API(`indexer.dydx.trade`)로 대체 확인
했다(서비스 자체는 정상); (c) **이번 회차부터 OKX OI를 CoinGecko 경유 없이 bulk 직접
API(`/public/open-interest?instType=SWAP`)로 전환**해 GALA 등에서 반복되던 CoinGecko 경유
괴리 이슈를 원천 우회했다; (d) 다만 **ALLO의 OKX OI가 약 10배 급증**한 원인은 불명확해 다음
회차 재확인이 필요하다; (e) MMT·GIGGLE 전체와 GRAM·PIPPIN·BSB(OKX)·CAP(Binance
OI·funding)·BICO(Binance OI)·ATOM(OKX vol·chg)·KAITO(Binance OI 일부)는 시간·호출
제약상 일부 필드를 직전 회차 값으로 이어받았다(정직 표기); (f) OrangeX 전면 중단이 37회차·약
75.75시간째 지속된다; (g) Aster ETH truncation이 19회차 연속 지속된다; (h) ETHFI의 OKX
chg24는 ticker fetch에서 open24h=last로 반환되는 이상이 있어 직전값으로 이월했다; (i) 글로벌
시총·도미넌스는 WebSearch 스니펫 교차확인이며 CoinGecko `/global` 직접조회는 이번 회차도
생략했다; (j) 주식화·상품·프리IPO 합성 perp 토큰은 이번 회차도 전부 제외했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
