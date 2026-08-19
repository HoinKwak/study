# 선물시장 스카우트 브리핑 — 2026-08-19 20:30 UTC (KST 2026-08-20 05:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 18:30 UTC)로부터 2시간 경과(정상 간격).**

## ⚠️ 이번 회차 최우선 과제 (a)(b)(c) 판별 결과

### (a) 메이저(BTC·ETH·HYPE·SOL) chg24 — **[부모 세션 정정] 오염이 아니라 실제 랠리였음**

~~메이저 chg24 오염이 3회차 연속 재현됐다. HL·Aster·dYdX·OKX mark-price·CoinGecko
simple/price 등 여러 소스가 BTC +6~10%대를 반환했으나 WebSearch 실측(BTC $64,300~64,900,
+0.3~0.5%)과 극단적으로 불일치해, 컨테이너 아웃바운드 경로(프록시)가 주요 코인 가격 피드에
다른 값을 서빙하고 있을 가능성이 유력하다고 판단해 chg24를 전부 이월했다.~~

**[부모 세션 정정]** 부모 세션이 Bash로 4개 독립 거래소를 직접 조회한 결과는 다음과 같다:

```
OKX      last 68,679.2  open24h 64,586.3  => +6.34%
Kraken   last 68,642.6  open24h 64,677.2  (high 69,577 / low 64,116)
Bitstamp last 68,655.18 open   64,686.09  percent_change_24 = 6.35
Coinbase spot 68,637.5
```

**4개의 완전히 독립적인 거래소가 소수점 수준까지 일치**했고, 이번 회차 스카우트가 직접
확보한 dYdX 공식 인덱서(oraclePrice $68,716.55)·OKX mark-price($68,750)·CoinGecko
simple/price($68,688, +6.36%)도 같은 값이었다. **즉 BTC는 실제로 $64.5K대에서 $68.6K대로
약 +6.3~6.4% 상승한 진짜 랠리였고**(Kraken 기준 고점 $69,577·저점 $64,116), 스카우트가
'오염값'이라 판단해 이월한 +6~17%대 chg24가 **오히려 정답이었다.** 어긋난 쪽은 WebSearch
실측이었다 — 검색 크롤링 뉴스 스니펫은 몇 시간~하루 전 기사 시점의 가격을 반영하므로,
급등 국면에서는 구조적으로 뒤처진다. ~~프록시가 다른 값을 서빙한다는 가설~~도 기각됐다 —
프록시를 지나는 부모 세션의 curl과 스카우트의 조회가 같은 값을 보고 있었고, 그 값이 서로
다른 4개 거래소에서 독립적으로 일치했기 때문이다.

**교훈(다음 회차부터 적용)**: 가격·chg24는 **거래소 직접 API가 1차 근거**이고 WebSearch는
보조다. 둘이 어긋나면 **거래소 직접 API 여러 곳이 서로 일치하는지**를 기준으로 판정하며,
WebSearch를 기준으로 API 값을 기각하면 안 된다.

**이번 회차 정정 반영**: BTC·ETH·SOL·HYPE 및 HYNA:* 행의 chg24(및 이월했던 price·vol·oi)를
전부 신선값으로 채택했다 — HL BTC +6.349%·ETH +10.827%·HYPE +16.518%, Aster BTC +6.426%,
dYdX BTC +6.396%(오라클 $68,716.55)·ETH +13.712%(오라클 $2,237.19)·SOL +8.494%(오라클
$84.28), HYNA:BTC-USD +6.324%·HYNA:ETH-USD +11.09%·HYNA:HYPE +16.471%·HYNA:SOL-USD
+7.189%.

### (b) Binance CoinGecko truncation — **4회차 연속** (판정 유지)

원 10종목(BICO·GALA·ETHFI·CAP·GIGGLE·MMT·GRAM·PIPPIN·BSB·KAITO) 재시도 전부 NOT FOUND
재확인. BTW도 재실패(직전엔 성공). **BEAT는 이번엔 목록에서 '발견'되긴 했으나 거래량이
$1.01M로 직전 확립 규모($96M)의 약 1/95 수준이라 명백히 비현실적** — 규모 불일치로
신뢰불가 판정해 사용하지 않고 이월했다(4회차 연속 실질 실패로 카운트).

### (c) OKX OI 벌크 배율 비일관성 — **✅ 원인 완전 규명·해소** (판정 유지)

OKX 공식 단건 조회(`/public/open-interest?instId=`)가 **`oiUsd` 네이티브 필드를 직접
제공**함을 발견 — BEAT(oi=3,060,167.3·oiCcy=30,601,673·oiUsd=$4,832,004.17), AAVE(oi=
1,228,102.9·oiCcy=122,810.29·oiUsd=$11,511,008.48), GALA(oi=105,612,874·oiCcy=1,056,128,740·
oiUsd=$1,464,850.56) 세 종목에서 **`oiCcy×last`가 `oiUsd`와 소수점 근사치까지 일치**함을
확인했다. 직전 회차가 '비일관적'이라 판단했던 배율차(BEAT는 oiCcy가 oi의 10배, AAVE는
oiCcy가 oi의 0.1배)는 **버그가 아니라 종목별 계약승수(ctVal)가 다른 정상적 결과**였다.
벌크 엔드포인트(`/public/open-interest?instType=SWAP`)로 동일 종목을 조회해도 동일 값이
나와 단건·벌크 간 불일치도 없었다. **결론: OKX OI 이월 정책을 이번 회차부로 해제**하고
다수 신선값을 채택했다. ⚠️이 판별에 따라 **ALLO의 과거 '10배 OI 급증=방법론 전환 아티팩트'
결론은 재검토 필요 판정**이나, 이번 회차엔 이력 재대조를 실시하지 않아 확정 결론은 유보하고
다음 회차 과제로 넘긴다.

## 시장 전반 — 이번 회차 핵심

0. **[부모 세션 정정] BTC가 지난 24시간 +6.3~6.4% 상승하며 $68.6K대로 올라선 진짜 랠리
   국면**이다(Kraken 기준 고점 $69,577·저점 $64,116). ETH(+10.8~13.7%)·HYPE(+16.5%)·
   SOL(+7.2~8.5%)도 동반 상승했다 — 이것이 아래 광범위 알트 랠리(AAVE·ADA·ALGO 등)의
   배경일 가능성이 크다.
1. **⚠️ATOM이 4개 벤뉴(Binance +3.644%·Bybit +3.862%·OKX +3.79%·HL +3.936%)에서 2시간
   만에 마이너스→플러스로 재반전**(whipsaw) — 다만 OKX는 재조회 결과 애초에 마이너스
   전환이 없었을 가능성. Aster만 미재확인.
2. **⚠️ALLO가 4개 전 벤뉴(Binance -2.648%·OKX -2.594%·Bybit -2.414%·Aster -2.592%)에서
   조밀하게(±0.24%p 이내) 다시 마이너스로 재반전** — 직전 '3벤뉴 플러스 전환'이 2시간 만에
   전부 되돌려짐.
3. **⚠️BANK가 Aster까지 마이너스 합류(-3.752%)해 3벤뉴 전부 마이너스로 합의**(Binance
   -3.543%·Bybit -3.309%) — 직전 '벤뉴간 혼조' 해소.
4. **⚠️CAP가 OKX(-2.09%)·Aster(-3.828%) 모두 마이너스로 전환** — 직전 플러스권에서 반전.
5. **1000RATS이 3벤뉴 모두 추가로 크게 회복**(Binance -6.142%·Bybit -5.37%·Aster -4.67%) —
   직전 -14%대에서 -5~6%대로 극단적 하락권을 거의 벗어남, V자 회복 지속.
6. **PIPPIN·BSB가 OKX에서 뚜렷한 플러스로 안착**(+1.441%·+1.49%).
7. **AAVE·ADA·ALGO가 Binance·Bybit·OKX·HL 전부에서 동시에 상승폭이 +2.9~3.4%대→
   +4.5~5.9%대로 크게 확대** — 위 BTC 랠리와 시기가 일치하는 동반 상승으로 해석되며,
   Fear&Greed도 46(Fear)→57(Neutral)로 개선됐다.
8. CASHCAT은 HL(+4.493%)·Aster(+5.323%) 모두 플러스 유지하되 직전(+6.9~7.0%)보다 냉각.
9. BEAT는 OKX -29.61%로 낙폭 추가 확대(Aster -28.125%도 동조).
10. BTW(Aster)는 -14.655%→-8.325%로 낙폭이 완화되며 재차 변동, Binance 교차확인 이번도 불가.

OKX는 이번 회차 단건/벌크 open-interest 조회로 다수 종목 OI를 신선 확보(ALLO $2.89M·APR
$2.91M·BSB $2.16M·CAP $10.55M·CORE $0.99M·ATOM $3.76M·BICO $2.34M·AEON $2.50M·ETHFI $3.88M·
MMT $2.38M·GRAM $6.36M·PIPPIN $1.82M·KAITO $5.40M·ADA $27.06M·ALGO $2.59M·AAVE $11.51M·GALA
$1.46M·BEAT $4.83M). ACE는 OKX 상장 자체가 없음을 이번 회차 확인(instId 조회시 51001
에러) — 과거 기록과 일치, 문제 없음. OKX funding은 이번 회차도 개별 fetch 미실시로 대부분
이월. **OrangeX는 41회차·약 83.75시간째 전면 중단** 지속. **Aster의 ETH truncation은 23회차
연속** 지속(majors 정정과는 무관한 별개의 데이터 가용성 이슈). 저장 직전 전 항목 funding
절대값 점검 결과 최댓값은 ACE Bybit -0.00553(신선, 직전 최대 -0.00236 대비 확대)이며 중앙값은
대체로 1e-5~1e-4대로 정상 범위. **F&G는 57(Neutral)로 개선**(직전 46 Fear).

## CEX 주목 종목 (메이저는 전통적으로 테이블 밖, 크립토 네이티브만)

funding은 raw fraction 기준(CoinGecko 파생 소스는 퍼센트를 /100 적용). "[이월]"은 이번 회차
fetch 실패·재조회 못함으로 직전값을 그대로 이어받은 필드.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| ACE [완화] | Binance(직접API) | $408.86M | $12.44M | -0.00274 | -16.209% | 낙폭 소폭 완화, 펀딩 확대 |
| **ACE** [완화] | Bybit(직접API) | $94.39M | $5.84M | **-0.00553** | -17.741% | 펀딩 절대값 전체 최대로 확대 |
| BTW [이월] | Binance(재실패) | $984.37M | $132.76M | 0.00129(이월) | +48.98% | 4회차째 CG fetch 재실패로 이월 |
| **BEAT** [심화] | OKX(직접API) | $84.73M | $4.83M | 0.00027(이월) | **-29.61%** | 낙폭 추가 확대, OI는 네이티브 oiUsd로 검증확보 |
| BEAT [이월,4회연속] | Binance | $96.21M | $10.70M | 0.00028 | -18.062% | 값은 나왔으나 거래량 1/95 비현실적, 신뢰불가 이월 |
| BICO [완화] | OKX(직접API) | $14.94M | $2.34M | 0.00005(이월) | -11.36% | 낙폭 완화 지속, OI 신선 |
| BICO [이월,4회연속] | Binance | $14.11M | $5.21M | -0.00058 | -12.292% | fetch 4회차 연속 실패 |
| GALA [이월,4회연속] | Binance | $18.97M | $6.49M | 0.0000274 | -3.767% | fetch 4회차 연속 실패 |
| GALA [완화] | OKX(직접API) | $6.03M | $1.46M | 0.0001(이월) | -1.63% | 낙폭 완화, OI 네이티브값 신선 |
| ETHFI [이월,4회연속] | Binance | $17.88M | $22.55M | -0.0000096 | +0.041% | fetch 4회차 연속 실패 |
| ETHFI [확대] | OKX(직접API) | $8.75M | $3.88M | -0.0000514(이월) | +3.969% | 상승폭 확대, 알트랠리 동조, OI 신선 |
| CAP [이월,4회연속] | Binance | $21.87M | $15.02M | -0.00007 | +0.973% | fetch 4회차 연속 실패 |
| **CAP** [반전] | OKX(직접API) | $73.03M | $10.55M | -0.0000677(이월) | **-2.09%** | ⚠️플러스→마이너스 전환, Aster와 동조, OI 신선 |
| AEON [심화] | OKX(직접API) | $34.58M | $2.50M | 0.00005(이월) | -15.65% | 낙폭 소폭 심화, OI 신선 |
| AEON [심화] | Bybit(직접API) | $2.12M | $0.79M | -0.00009 | -16.372% | 동조 심화, 펀딩 소폭 음전 |
| APEX [재확대] | Bybit(직접API) | $1.26M | $1.86M | 0.00005 | +7.626% | 상승폭 재확대, HL과 동조 |
| GIGGLE [이월,4회연속] | Binance | $15.24M | $10.97M | 0.00005 | -2.679% | fetch 4회차 연속 실패 |
| GIGGLE [이월] | OKX(재조회 못함) | $7.88M | $1.67M | 0.00005(이월) | +1.013% | 이번 회차 우선순위 밀림 |
| ALPINE [심화] | Binance(직접API) | $24.58M | $2.02M | 0.00005 | -16.62% | 깊은 하락권 유지, 소폭 심화 |
| ALPINE [심화] | Bybit(직접API) | $5.02M | $0.61M | 0.00005 | -16.131% | 동조 심화 |
| CORE [확대] | OKX(직접API) | $2.18M | $0.99M | 0.00008 | +5.17% | 플러스권 확대, Binance 미상장 지속, OI 신선 |
| **ATOM** [반전] | OKX(직접API) | $3.98M | $3.76M | -0.00015 | **+3.79%** | ⚠️신선 재조회로 플러스 확인, 타 4벤뉴와 동조 재반전 |
| **ATOM** [반전] | Binance(직접API) | $17.71M | $15.58M | 0.00006 | **+3.644%** | ⚠️마이너스→플러스로 2시간 만의 whipsaw |
| ATOM [반전] | Bybit(직접API) | $7.06M | $14.36M | -0.00014 | +3.862% | 동조 재반전 |
| **AAVE** [랠리] | OKX(직접API) | $26.66M | $11.51M | 0.00002(이월) | **+5.925%** | BTC 랠리와 동조하는 광범위 알트 랠리, OI 네이티브 정합확인 |
| AAVE [랠리] | Binance(직접API) | $79.65M | $46.97M | 0.0001 | +5.642% | 동조 확대 |
| AAVE [랠리] | Bybit(직접API) | $25.44M | $39.29M | 0.0001 | +5.64% | 동조 확대 |
| **ADA** [랠리] | OKX(직접API) | $53.98M | $27.06M | -0.00012(이월) | **+5.205%** | BTC 랠리와 동조하는 알트 랠리 |
| ADA [랠리] | Binance(직접API) | $140.65M | $85.43M | 0.0001 | +5.263% | 동조 확대 |
| ADA [랠리] | Bybit(직접API) | $62.29M | $55.42M | 0.00002 | +5.147% | 동조 확대 |
| **ALGO** [랠리] | Binance(직접API) | $10.31M | $7.61M | 0.0001 | **+4.799%** | BTC 랠리와 동조하는 알트 랠리 |
| ALGO [랠리] | OKX(직접API) | $4.71M | $2.59M | 0.0001 | +4.519% | 동조 확대 |
| ALGO [랠리] | Bybit(직접API) | $3.75M | $6.26M | 0.0001 | +4.504% | 동조 확대 |
| MMT [강세] | OKX(직접API) | $6.76M | $2.38M | -0.00024(이월) | +9.259% | 플러스권 강세 지속 |
| MMT [이월,4회연속] | Binance | $5.39M | $8.16M | -0.00009 | -2.043% | fetch 4회차 연속 실패 |
| GRAM [확대] | OKX(직접API) | $3.33M | $6.36M | 0.00005(이월) | +2.426% | 플러스권 확대, OI 신선 |
| GRAM [이월,4회연속] | Binance | $8.13M | $14.12M | 0.00005 | +1.459% | fetch 4회차 연속 실패 |
| **PIPPIN** [안착] | OKX(직접API) | $1.97M | $1.82M | 0.00005(이월) | **+1.441%** | ⚠️보합→뚜렷한 플러스 안착, OI 신선 |
| PIPPIN [이월,4회연속] | Binance | $4.86M | $5.70M | 0.00005 | -1.285% | fetch 4회차 연속 실패 |
| **BSB** [안착] | OKX(직접API) | $3.88M | $2.16M | 0.00032 | **+1.49%** | ⚠️마이너스→플러스 안착, Aster와 동조, OI 신선 |
| BSB [이월,4회연속] | Binance | $12.03M | $8.74M | 0.00011 | -1.701% | fetch 4회차 연속 실패 |
| BANK [확대] | Binance(직접API) | $22.90M | $10.83M | 0.00002 | -3.543% | 마이너스 폭 확대, Aster 합류로 3벤뉴 합의 |
| BANK [확대] | Bybit(직접API) | $2.71M | $3.98M | 0.00005 | -3.309% | 동조 확대, 펀딩 부호 반전 |
| APR [냉각] | OKX(직접API) | $32.89M | $2.91M | 0.00005 | +1.453% | 이월 벗어나 신선 재조회, 플러스 유지하나 냉각 |
| APR [냉각] | Bybit(직접API) | $5.53M | $3.05M | 0.00005 | +1.499% | 플러스 유지, 폭 축소 |
| APR [냉각] | Binance(직접API) | $32.37M | $10.67M | 0.00005 | +2.107% | 동조 냉각 |
| AIO [확대] | Binance(직접API) | $11.49M | $4.07M | 0.00005 | -8.264% | 마이너스 폭 재확대 |
| AIO [확대] | Bybit(직접API) | $1.15M | $1.14M | 0.00005 | -7.745% | 동조 확대 |
| **ALLO** [반전] | Binance(직접API) | $25.05M | $11.78M | -0.00001 | **-2.648%** | ⚠️플러스→마이너스 재반전(4벤뉴 정합적) |
| ALLO [반전] | OKX(직접API) | $20.07M | $2.89M | 0.00005 | -2.594% | 신선 재조회로 마이너스 확인, 4벤뉴 조밀 일치 |
| ALLO [반전] | Bybit(직접API) | $3.25M | $4.21M | -0.00048 | -2.414% | 동조 반전, 펀딩도 큰 폭 음전 |
| **1000RATS** [회복] | Binance(직접API) | $26.78M | $13.03M | 0.00014 | **-6.142%** | 극단적 하락권에서 추가로 크게 회복 |
| 1000RATS [회복] | Bybit(직접API) | $11.00M | $4.89M | 0.00005 | -5.37% | 동조 회복 |
| ASTER(자체) [확대] | Binance(직접API) | $30.96M | $73.01M | 0.00005 | +2.759% | 상승폭 확대, 알트 랠리와 동조 |
| ASTER(자체) [이월] | OKX(재조회 못함) | $4.09M | $8.42M | 0.0001(이월) | +0.899% | 이번 회차 재조회 못함 |
| ASTER(자체) [이월] | Bybit(재조회 못함) | $2.55M | $39.93M | 0.00005 | +0.732% | 이번 회차 재조회 못함 |
| KAITO [확대] | OKX(직접API) | $25.77M | $5.40M | 0.0000060(이월) | +3.369% | 상승폭 확대, HL과 동조, OI 신선 |
| KAITO [이월,USDT,4회연속] | Binance | $33.30M | $15.03M | -0.00009 | +4.644% | fetch 4회차 연속 실패 |
| KAITO [이월,USDC,4회연속] | Binance | $3.82M | $1.14M | -0.00009 | +3.695% | fetch 4회차 연속 실패 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 41회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).
⚠️표시는 이번 회차 신규 급변동/미확인 행, **[부모 세션 정정]**은 이번 정정으로 신선값을
채택한 majors 관련 행.

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| ACE [완화] | Hyperliquid | $2.58M | $1.77M | -0.00067 | -16.164% | CEX와 동조, 낙폭 완화 |
| ACE [심화] | Aster | $0.87M | $0.19M | -0.00083 | -18.022% | 낙폭 소폭 심화, 펀딩 확대 |
| ACE [중단] | OrangeX | — | — | — | — | 41회차·약 83.75시간 |
| **BTW** [재변동⚠️] | Aster | $14.18M | $7.13M | 0.00004 | **-8.325%** | 낙폭 완화(-14.66%→-8.33%), Binance 교차확인 불가 지속 |
| KAITO [확대] | Hyperliquid | $3.18M | $5.32M | 0.00001 | +4.026% | 플러스 폭 확대, OKX와 동조 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CASHCAT [냉각] | Hyperliquid | $11.18M | $13.12M | 0.00001 | +4.493% | 플러스 유지, 다소 냉각 |
| CASHCAT [냉각] | Aster | $1.03M | $0.69M | 0.00001 | +5.323% | 동조 냉각하나 여전히 뚜렷한 플러스 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GALA [완화] | Hyperliquid | $0.49M | $1.08M | -0.00013 | -1.349% | 낙폭 완화 |
| BEAT [심화] | Aster | $1.99M | $1.14M | 0.00001 | -28.125% | 낙폭 추가 확대, OKX와 정합적 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BICO [완화] | Aster | $0.06M | $0.12M | -0.00031 | -11.333% | 낙폭 완화, OKX와 정합적 |
| BICO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| AEON [심화] | Aster | $0.11M | $0.28M | 0.00001 | -15.8% | CEX와 대체로 동조, 소폭 심화 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [확대] | Hyperliquid | $1.64M | $15.30M | 0.00001 | +2.246% | 플러스권 확대, OKX와 동조 |
| **ATOM** [반전] | Hyperliquid | $0.60M | $1.87M | -0.00004 | **+3.936%** | ⚠️타 벤뉴와 함께 플러스로 재반전 |
| ATOM [이월] | Aster | $0.01M | $1.69M | 0.0001 | -2.897% | 미재확인(이월) — 타 4벤뉴는 플러스 재반전 확인 |
| **AAVE** [랠리] | Hyperliquid | $7.53M | $58.21M | 0.00001 | +5.417% | BTC 랠리와 동조하는 광범위 알트 랠리 |
| AAVE [이월] | Aster | $0.26M | $4.63M | 0.0001 | +2.892% | 미재확인(이월) |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **ADA** [랠리] | Hyperliquid | $6.20M | $28.24M | 0.00001 | +5.236% | BTC 랠리와 동조하는 광범위 알트 랠리 |
| ADA [이월] | Aster | $0.55M | $1.30M | 0.0001 | +3.272% | 미재확인(이월) |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **ALGO** [랠리] | Hyperliquid | $0.63M | $1.98M | 0.00001 | +4.738% | BTC 랠리와 동조하는 광범위 알트 랠리 |
| ALGO [이월] | Aster | $0.005M | $0.04M | 0.00001 | +3.139% | 미재확인(이월) |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ASTER(자체) [확대] | Aster | $1.63M | $14.36M | 0.00001 | +2.596% | 자체 OI 안정, 상승폭 확대(Binance와 동조) |
| ASTER(자체) [이월] | Hyperliquid | $0.87M | $13.62M | 0.00001 | +0.743% | 미재확인(이월) |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **HYPE** [부모 세션 정정] | Hyperliquid | $990.00M | $1,614.41M | 0.00013 | **+16.518%** | ~~chg 이상치 3회차 연속~~ → 4개 독립 거래소 대조로 실제 급등 확인, 신선값 채택 |
| BLESS [완화] | Aster | $0.03M | $0.08M | 0.00005 | -0.684% | 낙폭 추가 완화(-2.5%→-0.7%) |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **BTC** [부모 세션 정정] | dYdX | $41.77M | $19.68M | 0.0 | **+6.396%** | ~~오라클가 $68,716.55는 시장과 괴리~~ → OKX/Kraken/Bitstamp와 소수점 수준 일치하는 정확값, 신선값 채택 |
| **ETH** [부모 세션 정정] | dYdX | $65.65M | $19.04M | -0.000012 | **+13.712%** | 신선값 채택, 오라클가 $2,237.19, BTC 랠리 동반 상승 |
| **SOL** [부모 세션 정정] | dYdX | $1.40M | $4.77M | ~0 | **+8.494%** | 신선값 채택, 오라클가 $84.28, BTC 랠리 동반 상승 |
| **BTC** [부모 세션 정정] | Hyperliquid | $4,731.63M | $2,505.61M | 0.00001 | **+6.349%** | ~~chg 이상치 3회차 연속~~ → 실제 랠리, 신선값 채택 |
| **ETH** [부모 세션 정정] | Hyperliquid | $2,521.54M | $1,842.01M | 0.00001 | **+10.827%** | 신선값 채택, BTC 랠리 동반 상승 |
| **BTC** [부모 세션 정정] | Aster | $1,524.21M | $849.98M | 0.00009 | **+6.426%** | 신선값 채택, 4개 거래소 대조로 실제 랠리 확인 |
| ETH [truncation 23연속] | Aster | — | — | — | — | base=ETH 항목 부재 재확인(majors 정정과 무관한 별개 이슈) |
| **1000RATS** [회복] | Aster | $0.24M | $0.07M | 0.00006 | -4.67% | 극단적 하락권에서 추가 회복, CEX와 동조 |
| AIO [확대] | Aster | $0.03M | $0.08M | 0.00005 | -7.472% | CEX와 동조 확대 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **ALLO** [반전] | Aster | $0.09M | $0.07M | 0.00001 | **-2.592%** | ⚠️CEX 전체와 함께 마이너스로 재반전 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| APR [냉각] | Aster | $0.08M | $0.29M | 0.00001 | +2.31% | 플러스권 유지, CEX와 함께 다소 냉각 |
| APR [미상장] | Hyperliquid | — | — | — | — | 이번 회차도 HL 미상장 재확인 |
| **BANK** [반전] | Aster | $0.10M | $0.23M | 0.00001 | **-3.752%** | ⚠️플러스→마이너스 전환, 3벤뉴 전부 마이너스 합의 |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [안착] | Aster | $0.11M | $0.13M | 0.00001 | +1.517% | 플러스권 유지, OKX와 동조 안착 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **CAP** [반전] | Aster | $0.10M | $0.15M | 0.00001 | **-3.828%** | ⚠️플러스→마이너스 전환, OKX와 동조 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| FARTCOIN [재확대] | Hyperliquid | $7.66M | $31.88M | 0.00006 | +8.266% | 상승폭 재확대(+5.3%→+8.3%) |
| ETHFI [확대] | Hyperliquid | $3.61M | $11.18M | 0.00001 | +4.167% | 플러스권 확대, OKX와 동조 |
| HYPER [확대] | Hyperliquid | $0.07M | $0.20M | -0.00002 | +5.457% | 플러스권 확대 |
| APEX [재확대] | Hyperliquid | $0.24M | $0.71M | 0.00001 | +8.122% | Bybit와 함께 상승폭 재확대 |
| **HYNA:BTC-USD** [부모 세션 정정] | Hyperliquid | $0.80M | $2.38M | 0.00001 | **+6.324%** | HIP-3 빌더배포, 기초자산(BTC) 실제 랠리 확인돼 신선값 채택 |
| **HYNA:ETH-USD** [부모 세션 정정] | Hyperliquid | $0.60M | $1.78M | 0.00001 | **+11.09%** | HIP-3 빌더배포, 기초자산(ETH) 실제 랠리 확인돼 신선값 채택 |
| **HYNA:HYPE** [부모 세션 정정] | Hyperliquid | $0.31M | $0.72M | 0.00008 | **+16.471%** | HIP-3 빌더배포, 기초자산(HYPE) 실제 급등 확인돼 신선값 채택 |
| HYNA:PUMP [신선] | Hyperliquid | $0.04M | $0.17M | 0.00001 | +9.841% | 별도 기초자산이라 신선값 채택, 강세 유지(다소 냉각) |
| **HYNA:SOL-USD** [부모 세션 정정] | Hyperliquid | $0.17M | $0.58M | 0.00002 | **+7.189%** | HIP-3 빌더배포, 기초자산(SOL) 실제 랠리 확인돼 신선값 채택 |

## 테마 태그 (요약)

1. [부모 세션 정정] (a) 메이저 chg24는 오염이 아니라 실제 랠리 — 4개 독립 거래소(OKX·Kraken·Bitstamp·Coinbase)가 BTC +6.3~6.4% 일치 확인, WebSearch가 지연된 것으로 판정 (majors-btc-rally-confirmed)
2. [부모 세션 정정] ~~프록시 이상 가설~~ 기각됨 (proxy-anomaly-hypothesis-retracted)
3. [부모 세션 정정] ~~majors vol/OI 오염 우려~~도 해소 — 가격이 정확했으므로 USD 환산값도 정확 (majors-volusd-contamination-concern-retracted)
4. (b) Binance CG truncation 4회차 연속, BEAT는 비현실적 규모값 (binance-cg-fetch-truncation-persists-4th-round)
5. ✅(c) OKX OI 배율 문제 원인 규명·해소(ctVal 정상 현상, 단건·벌크 일치) (okx-oi-methodology-resolved-ctval-explained)
6. ⚠️ALLO 과거 'OI 급증=아티팩트' 결론 재검토 필요(유보) (allo-oi-jump-conclusion-needs-recheck)
7. ⚠️ATOM 4벤뉴 whipsaw로 플러스 재반전 (atom-whipsaws-back-positive)
8. ⚠️ALLO 4벤뉴 조밀하게 마이너스 재반전 (allo-reverses-negative-again)
9. ⚠️BANK 3벤뉴 전부 마이너스 합의 (bank-full-negative-consensus)
10. ⚠️CAP OKX·Aster 마이너스 전환 (cap-flips-negative)
11. 1000RATS 3벤뉴 추가 크게 회복 (1000rats-recovers-sharply)
12. PIPPIN OKX 뚜렷한 플러스 안착 (pippin-turns-clearly-positive)
13. BSB OKX 플러스 안착 (bsb-turns-positive)
14. AAVE·ADA·ALGO 광범위 알트 랠리(+4.5~5.9%), BTC +6.3% 랠리와 시기 일치, F&G 46→57 개선 (broad-alt-rally-with-btc)
15. CASHCAT 플러스 유지, 다소 냉각 (cashcat-flips-positive)
16. BEAT OKX·Aster 낙폭 추가 확대 (beat-decline-widens-sharply)
17. BTW Aster 낙폭 완화되며 재차 변동, 단독소스 지속 (btw-continues-swinging-unconfirmed)
18. ACE 4벤뉴 낙폭 소폭 완화, Bybit 펀딩 전체 최대(-0.00553) (ace-decline-stabilizes)
19. BICO OKX·Aster 낙폭 완화 지속 (bico-improves)
20. GALA OKX·HL 낙폭 완화 (gala-mixed)
21. ETHFI OKX·HL 플러스권 확대 (ethfi-momentum-cools)
22. AEON OKX·Bybit·Aster 대체로 소폭 심화 (aeon-improves)
23. APEX Bybit·HL 상승폭 재확대 (apex-reaccelerates)
24. GIGGLE 이번 회차 재조회 우선순위 밀려 전부 이월 (giggle-turns-positive)
25. ALPINE Binance·Bybit 깊은 하락권 유지, 소폭 심화 (alpine-remains-deeply-negative)
26. CORE OKX 플러스권 소폭 확대 (core-carryover)
27. MMT OKX 플러스권 강세 지속 (mmt-extends-positive)
28. GRAM OKX·HL 플러스권 확대 (gram-momentum-cools)
29. APR 전 벤뉴 플러스 유지, 다 함께 냉각 (apr-cools-still-positive)
30. AIO 마이너스 폭 재확대 (aio-widens-again)
31. ASTER(자체토큰) Binance 상승폭 확대, 알트랠리 동조 (aster-cex-stable)
32. BLESS(Aster) 낙폭 추가 완화 (bless-improves)
33. KAITO OKX·HL 상승폭 확대 (kaito-turns-clearly-positive)
34. FARTCOIN 상승폭 재확대 (fartcoin-reaccelerates)
35. HYPER 상승폭 확대 (hyper-momentum-cools)
36. [부모 세션 정정] dYdX 오라클가 $68,716.55는 시장가와 불과 0.1% 차이로 정확값이었음, 신선값 채택 (majors-btc-rally-confirmed)
37. [부모 세션 정정] 메이저 chg는 오염이 아니라 실제 랠리였음, HYNA:*도 전부 신선값 채택 (majors-btc-rally-confirmed)
38. HYNA:* 계열(HL) HIP-3 빌더배포 마켓, 계속 포함 유지 (hyna-builder-deployed-markets)
39. 데이터: ACE는 OKX 상장 자체 없음 재확인(51001 에러) (ace-not-listed-on-okx-confirmed)
40. 데이터: OKX ticker+네이티브 oiUsd로 다수 종목 신선 확보, 단건·벌크 일치 (okx-oi-methodology-resolved-ctval-explained)
41. 데이터: ⚠️Binance CG truncation 4회차 연속, BEAT 비현실적 규모 (binance-cg-fetch-truncation-persists-4th-round)
42. 데이터: OrangeX 41회차(약 83.75h) 서비스 중단 지속 (orangex-service-outage-continues)
43. 데이터: Aster ETH truncation 23회차 연속 (truncation-continues-23rd-round)
44. 글로벌: Fear&Greed 57(Neutral)로 개선(직전 46 Fear) — BTC 랠리·알트 동반 상승과 부합 (fear-greed-improves-to-neutral)
45. 주식화·상품 토큰 전부 제외 유지 (stock-commodity-tokens-excluded-crypto-native-confirmed)

## 한계

**[부모 세션 정정]** (a) ~~메이저(BTC·ETH·HYPE·SOL) chg24 오염이 3회차 연속~~ →
**오염이 아니라 실제 랠리였음이 4개 독립 거래소(OKX·Kraken·Bitstamp·Coinbase) 직접 대조로
확인됐다.** BTC는 +6.3~6.4% 상승해 $68.6K대(Kraken 기준 고점 $69,577·저점 $64,116)였고,
어긋났던 쪽은 뉴스 스니펫 기반 WebSearch 실측이었다(급등 국면에서 구조적으로 지연). 이번
회차부로 BTC·ETH·SOL·HYPE·HYNA:* 전부 신선값을 채택했다. **교훈: 가격·chg24는 거래소 직접
API가 1차 근거, WebSearch는 보조 — 여러 거래소 API가 서로 일치하면 그것을 채택한다.**
(b) **Binance CG truncation은 4회차 연속**이며 BEAT는 이번엔 값이 나왔으나 규모가
비현실적이라 신뢰불가 처리했다; (c) **OKX OI 벌크 배율 문제는 이번 회차 원인이 완전히
규명·해소**됐다(계약승수 차이가 정상 현상, 단건·벌크 일치) — 다만 ALLO의 과거 'OI
급증=아티팩트' 판정 재검토는 다음 회차로 이월; (d) BTW의 Aster 값은 이번에도 재차 크게
변동(-14.66%→-8.33%)했고 Binance 교차확인은 여전히 불가; (e) OrangeX 전면 중단이 41회차·
약 83.75시간째 지속된다; (f) Aster ETH truncation이 23회차 연속 지속된다(majors 정정과는
무관한 별개 이슈); (g) AAVE·ADA·ALGO 등 광범위 알트 랠리(+4.5~5.9%)는 BTC +6.3% 랠리와
시기가 일치해 배경 있는 동반 상승으로 해석한다; (h) 주식화·상품·프리IPO 합성 perp 토큰은
이번 회차도 전부 제외했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
