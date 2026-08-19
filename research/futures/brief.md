# 선물시장 스카우트 브리핑 — 2026-08-19 16:30 UTC (KST 2026-08-20 01:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 14:30 UTC)로부터 2시간 경과(정상 간격).**

## ⚠️ 이번 회차 최우선 과제 — 직전 이월 종목 복구 결과

직전 회차 CoinGecko `binance_futures` truncation으로 이월됐던 12개 심볼(BTW·BICO·GALA·ETHFI·
CAP·AEON·GIGGLE·MMT·GRAM·PIPPIN·BSB·KAITO)을 우선 재시도했다.

| 결과 | 심볼 |
|---|---|
| **성공(신선값 확보)** | BTW(Binance, +67%→**+49%** 냉각), AEON(Binance 미상장 확인, OKX·Bybit·Aster 전부 신선) |
| **2회차 연속 실패(Binance만)** | BICO·GALA·ETHFI·CAP·GIGGLE·MMT·GRAM·PIPPIN·BSB·KAITO — 단 전부 **OKX·HL·Aster 등 타 벤뉴에서는 신선값 확보**돼 방향성 교차확인 가능 |

**BEAT의 Binance 신규 fetch값도 2회차 연속 신뢰불가**(이번엔 ≈$1.1M로 직전 대비 약 87배 작음,
직전 회차의 240배 왜곡과 같은 성격) 판정, 폐기 후 이월했다. **CASHCAT의 Aster 값은 이번 회차
무관 티커와의 오염이 재발하지 않고 정상적으로 신선값(-4.667%)을 확보**해 직전 회차의 데이터
오염 문제가 해소됐다.

## ⚠️ 신규 데이터품질 이슈 — 메이저(BTC·ETH·HYPE·SOL) 가격변동률 이상치

이번 회차 CoinGecko를 경유한 Hyperliquid·Aster·dYdX 세 소스 모두에서 BTC·ETH·HYPE·SOL의
24h 변동률이 **+6~+10%대**로 반환됐다. 그러나 WebSearch로 교차확인한 실제 시장은 BTC
$64,300~64,900 구간에서 24h **+0.29~+0.5%** 수준의 완만한 상승(SEC 크립토 자본조달 규제프레임
제안 뉴스發)에 그쳐 명백히 불일치한다. dYdX는 오라클가 자체가 **$68,747.51(재조회해도 동일값)**로
반환돼 시장 컨센서스 대비 약 6.8% 괴리가 있었다. 원인 불명(캐싱/기준시점 오류 등 추정)이나
신뢰불가로 판단해, 해당 메이저(BTC·ETH·HYPE HL/Aster, dYdX BTC·ETH·SOL)와 이를 추종하는
HYNA:BTC-USD·HYNA:ETH-USD·HYNA:HYPE·HYNA:SOL-USD의 **chg24는 전부 직전값을 이월**했다
(dYdX는 오라클가 훼손으로 vol/OI까지 전체 이월, HL·Aster는 vol/OI만 상대적으로 신뢰 가능해
신선값 채택). HYNA:PUMP는 별도 기초자산이라 신선값을 그대로 채택했다.

## 시장 전반 — 이번 회차 핵심

1. **직전 이월 종목 복구(상단 참고)** — BTW 성공, 10종목 Binance 재실패, BEAT 재폐기, CASHCAT
   오염 해소.
2. **⚠️메이저 chg24 이상치(상단 참고)** — 신규 데이터품질 이슈, 전부 직전값 이월 처리.
3. **ACE 낙폭 재차 확대**: Binance -12.62%→**-17.653%**, Bybit -13.066%→**-17.867%**, HL
   -13.895%→**-17.596%**, Aster -13.516%→**-18.053%**로 4벤뉴 전부 -17~-18%대로 더 깊어졌다.
   펀딩도 Bybit -0.00351로 전 항목 중 최대 절대값(직전 최대 0.00289 상회) — 극단적 변동성
   국면이 지속된다.
4. **⚠️ALPINE 신규 방향 반전**: Binance +3.979%→**-16.584%**, Bybit +3.841%→**-13.357%**로
   상승 진정 흐름에서 급격한 하락으로 전환 — 직전까지의 '상승폭 지속 축소'와는 질적으로 다르다.
5. **CASHCAT 뚜렷한 회복**: HL -12.948%→**-3.97%**, Aster -7.246%(이월)→**-4.667%**(신선)로
   두 벤뉴 모두 낙폭이 크게 줄며 재확대 흐름이 꺾였다.
6. **KAITO 보합권 근접 수렴**: OKX -1.376%→**+0.029%**, HL -0.81%→**-0.265%**로 반등도
   급락도 아닌 거의 평행선 수렴(Binance는 2회차 연속 이월).
7. **BANK 약세→플러스 반전**: Binance -1.947%→**+0.558%**, Bybit -1.892%→**+0.699%**, Aster
   -1.754%→**+1.118%**로 3벤뉴 전부 반전.
8. **1000RATS 극단적 하락권 유지**: 3벤뉴 모두 -21~-23%대(Binance -21.332%, Bybit -21.703%,
   Aster -22.772%).
9. **BSB 마이너스→거의 보합 회복**: OKX -3.27%→**-0.0816%**, Aster -3.916%→**-0.163%**.
10. **MMT 마이너스→플러스 전환**: OKX -2.649%→**+5.46%**(Binance는 이월로 -2.043% 유지).
11. **AAVE·ADA·ALGO·ATOM 전 벤뉴 플러스권 전환**: AAVE +3.9~4.1%, ADA +2.8~3.0%, ALGO
    +4.0~4.1%, ATOM +1.6~1.8%로 4개 종목 모두 동조 반등했다.

**OKX funding은 다수 종목에서 이번 회차도 개별 fetch를 못해 직전값을 이월**했다(vol/OI/chg는
`last×volCcy24h`/`oiCcy×last` 방식으로 신선 확보). **OrangeX는 39회차·약 79.75시간째 전면
중단** 지속. 저장 직전 전 항목 funding 절대값 점검 결과 최댓값은 ACE Bybit -0.00351로 직전
최대(0.00289) 대비 소폭 상회했으나 ACE 자체가 극단적 변동성 국면이라 이례적이지 않다(중앙값은
대체로 1e-5~1e-4대 유지). **글로벌 시총은 WebSearch 재확인 결과 약 $2.29조·BTC 도미넌스 약
56.5%**(SEC 크립토 자본조달 규제프레임 제안 발표가 완만한 상승 촉매).

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

funding은 raw fraction 기준. "[이월]"은 이번 회차 CG/직접 fetch 실패로 직전값을 그대로 이어받은 필드.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **ACE** [재확대] | Binance(직접API) | $446.53M | $12.48M | -0.00182 | **-17.653%** | 낙폭 재차 확대, 극단적 변동성 지속 |
| ACE [재확대] | Bybit(직접API) | $104.52M | $5.90M | -0.00351 | -17.867% | 동조 확대, 펀딩 전 항목 중 최대 절대값 |
| **BTW** [신선값확보] | Binance(직접API) | $984.37M | $132.76M | 0.00129(이월) | +48.98% | 2회차만의 신선값, 직전대비 뚜렷이 냉각 |
| **BEAT** [재확대] | OKX(직접API) | $84.68M | $5.04M | 0.00027(이월) | -21.28% | 낙폭 재확대 |
| BEAT [이월,2회연속] | Binance | $96.21M | $10.70M | 0.00028 | -18.062% | 신규값 2회차 연속 신뢰불가로 폐기 |
| BICO [확대] | OKX(직접API) | $13.71M | $2.38M | 0.00005(이월) | -15.55% | 낙폭 확대 |
| BICO [이월,2회연속] | Binance | $14.11M | $5.21M | -0.00058 | -12.292% | CG fetch 2회차 연속 실패 |
| GALA [이월,2회연속] | Binance | $18.97M | $6.49M | 0.0000274 | -3.767% | CG fetch 2회차 연속 실패 |
| GALA [완화] | OKX(직접API) | $6.07M | $1.58M | 0.0001(이월) | -1.914% | 낙폭 다소 완화 |
| ETHFI [이월,2회연속] | Binance | $17.88M | $22.55M | -0.0000096 | +0.041% | CG fetch 2회차 연속 실패 |
| **ETHFI** [확대] | OKX(직접API) | $8.58M | $4.04M | -0.0000514(이월) | +5.473% | 플러스권 크게 확대 |
| CAP [이월,2회연속] | Binance | $21.87M | $15.02M | -0.00007 | +0.973% | CG fetch 2회차 연속 실패 |
| CAP [확대] | OKX(직접API) | $71.28M | $11.34M | -0.0000677(이월) | +3.982% | 플러스권 소폭 확대 |
| AEON [확대] | OKX(직접API) | $37.13M | $2.83M | 0.00005(이월) | -16.42% | 낙폭 확대 |
| AEON [확대] | Bybit(직접API) | $2.01M | $0.81M | 0.00005 | -16.494% | 동조 확대 |
| APEX [확대] | Bybit(직접API) | $1.34M | $1.83M | 0.00005 | +9.825% | 상승폭 확대 |
| GIGGLE [이월,2회연속] | Binance | $15.24M | $10.97M | 0.00005 | -2.679% | CG fetch 2회차 연속 실패 |
| GIGGLE [보합] | OKX(직접API) | $7.59M | $1.67M | 0.00005(이월) | +0.149% | 거의 완전 보합 |
| **ALPINE** [급락반전] | Binance(직접API) | $56.85M | $2.06M | 0.00005 | **-16.584%** | ⚠️상승진정→급락으로 방향 반전 |
| ALPINE [급락반전] | Bybit(직접API) | $12.48M | $0.65M | 0.00005 | -13.357% | 동조 급락 반전 |
| CORE [확대] | OKX(직접API) | $2.61M | $1.03M | 0.00008 | +4.583% | 플러스권 확대, Binance 미상장 지속 |
| ATOM [전환] | OKX(직접API) | $3.74M | $3.75M | -0.00015(이월) | +1.708% | 마이너스→플러스 전환 |
| ATOM [전환] | Binance(직접API) | $16.90M | $15.49M | -0.00001 | +1.559% | 동조 전환 |
| ATOM [전환] | Bybit(직접API) | $6.49M | $14.25M | -0.00024 | +1.774% | 동조 |
| AAVE [전환] | OKX(직접API) | $26.34M | $11.47M | 0.00002(이월) | +3.854% | 플러스권 확대 |
| AAVE [전환] | Binance(직접API) | $72.82M | $46.70M | 0.0001 | +4.126% | 마이너스→플러스 전환 |
| AAVE [전환] | Bybit(직접API) | $24.32M | $39.13M | 0.0001 | +3.902% | 동조 전환 |
| ADA [전환] | OKX(직접API) | $46.16M | $28.06M | -0.00012(이월) | +2.854% | 마이너스→플러스 전환 |
| ADA [전환] | Binance(직접API) | $121.60M | $84.59M | -0.00004 | +3.02% | 동조 전환 |
| ADA [전환] | Bybit(직접API) | $54.68M | $56.36M | -0.00053 | +2.794% | 동조 |
| ALGO [확대] | Binance(직접API) | $9.66M | $7.81M | 0.0001 | +4.055% | 플러스권 확대 지속 |
| ALGO [확대] | OKX(직접API) | $4.36M | $2.70M | 0.0001(이월) | +4.066% | 동조 확대 |
| ALGO [신규확인] | Bybit(직접API) | $3.28M | $6.30M | 0.0001 | +4.134% | 이번 회차 신규 확인 |
| MMT [전환] | OKX(직접API) | $5.46M | $2.47M | -0.00024(이월) | +5.46% | 마이너스→플러스 전환 |
| MMT [이월,2회연속] | Binance | $5.39M | $8.16M | -0.00009 | -2.043% | CG fetch 2회차 연속 실패 |
| GRAM [확대] | OKX(직접API) | $4.85M | $6.41M | 0.00005(이월) | +2.44% | 플러스권 확대 |
| GRAM [이월,2회연속] | Binance | $8.13M | $14.12M | 0.00005 | +1.459% | CG fetch 2회차 연속 실패 |
| PIPPIN [보합] | OKX(직접API) | $2.19M | $1.81M | 0.00005(이월) | -2.0% | 소폭 마이너스 |
| PIPPIN [이월,2회연속] | Binance | $4.86M | $5.70M | 0.00005 | -1.285% | CG fetch 2회차 연속 실패 |
| **BSB** [회복] | OKX(직접API) | $3.87M | $2.16M | 0.00032(이월) | -0.0816% | 마이너스→거의 완전 보합 회복 |
| BSB [이월,2회연속] | Binance | $12.03M | $8.74M | 0.00011 | -1.701% | CG fetch 2회차 연속 실패 |
| **BANK** [반전] | Binance(직접API) | $26.90M | $10.99M | 0.00005 | +0.558% | 약세→플러스 반전 |
| BANK [반전] | Bybit(직접API) | $3.13M | $4.09M | 0.00005 | +0.699% | 동조 반전 |
| APR [완화] | OKX(직접API) | $40.27M | $2.85M | 0.00005(이월) | -3.532% | 마이너스 소폭 완화 |
| APR [확대] | Bybit(직접API) | $6.61M | $3.13M | 0.00005 | -5.49% | 마이너스 폭 확대 |
| APR [이월,2회연속] | Binance | $49.55M | $10.69M | 0.00005 | -3.619% | CG fetch 2회차 연속 실패 |
| AIO [완화] | Binance(직접API) | $12.95M | $4.03M | 0.00005 | -8.503% | 마이너스 폭 완화 지속 |
| AIO [완화] | Bybit(직접API) | $1.32M | $1.16M | 0.00005 | -8.003% | 동조 완화 |
| ALLO [전환] | Binance(직접API) | $27.93M | $12.19M | 0.00005 | -2.351% | 플러스→소폭 마이너스 전환 |
| **ALLO** [OI확인] | OKX(직접API) | $23.90M | $3.20M | 0.00005(이월) | -1.84% | ⚠️OI 3회차 연속 유지 — 방법론 아티팩트 재확인 |
| ALLO [전환] | Bybit(직접API) | $3.64M | $4.32M | -0.00013 | -2.544% | 동조 소폭 마이너스 |
| **1000RATS** [유지] | Binance(직접API) | $45.00M | $12.55M | 0.00008 | -21.332% | 극단적 하락권 유지 |
| 1000RATS [유지] | Bybit(직접API) | $18.84M | $4.65M | 0.00005 | -21.703% | 동조 유지 |
| ASTER(자체) [안정] | Binance(직접API) | $16.18M | $70.49M | 0.00005 | +1.516% | 안정적 플러스권 유지 |
| ASTER(자체) [안정] | OKX(직접API) | $3.57M | $8.42M | 0.0001(이월) | +1.45% | 동조 안정 |
| ASTER(자체) [안정] | Bybit(직접API) | $2.15M | $40.13M | 0.00005 | +1.466% | 동조 안정 |
| **KAITO** [수렴] | OKX(직접API) | $26.05M | $5.31M | 0.0000060(이월) | +0.029% | 마이너스→거의 완전 보합 회복 |
| KAITO [이월,USDT,2회연속] | Binance | $33.30M | $15.03M | -0.00009 | +4.644% | CG fetch 2회차 연속 실패 |
| KAITO [이월,USDC,2회연속] | Binance | $3.82M | $1.14M | -0.00009 | +3.695% | CG fetch 2회차 연속 실패 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 39회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).
⚠️표시는 이번 회차 chg24 이상치로 직전값을 이월한 행(메이저 관련).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **ACE** [재확대] | Hyperliquid | $1.94M | $1.75M | -0.00033 | -17.596% | CEX와 동조, 낙폭 재차 확대 |
| ACE [재확대] | Aster | $0.99M | $0.18M | -0.00039 | -18.053% | 동조 확대, 4벤뉴 중 최대 |
| ACE [중단] | OrangeX | — | — | — | — | 39회차·약 79.75시간 |
| **BTW** [냉각] | Aster | $11.53M | $11.01M | 0.00013 | +47.957% | Binance와 유사 수준으로 냉각 |
| **KAITO** [수렴] | Hyperliquid | $2.81M | $5.40M | 0.00001 | -0.265% | 마이너스→거의 보합 회복 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **CASHCAT** [회복] | Hyperliquid | $11.10M | $13.78M | 0.00001 | -3.97% | 뚜렷한 회복, 낙폭 크게 축소 |
| CASHCAT [회복] | Aster | $0.68M | $0.77M | 0.00001 | -4.667% | 오염 재발 없이 신선값 확보 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GALA [완화] | Hyperliquid | $1.15M | $1.07M | -0.00008 | -1.772% | 낙폭 완화 |
| BEAT [신선] | Aster | $1.56M | $1.49M | -0.00008 | -17.749% | 신선값 확보, CEX와 동조 확대 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BICO [확대] | Aster | $0.07M | $0.11M | -0.00005 | -15.023% | 낙폭 확대 |
| BICO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| AEON [확대] | Aster | $0.09M | $0.27M | -0.00004 | -14.933% | 낙폭 확대, CEX와 동조 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [확대] | Hyperliquid | $1.97M | $15.29M | 0.00001 | +2.345% | 플러스권 확대 |
| ATOM [전환] | Hyperliquid | $0.49M | $1.75M | 0.00001 | +1.735% | 타 벤뉴와 동조 전환 |
| ATOM [전환] | Aster | $0.01M | $1.70M | 0.0001 | +1.348% | 동조 전환 |
| AAVE [전환] | Hyperliquid | $7.08M | $58.27M | 0.00001 | +3.878% | 타 벤뉴와 동조 전환 |
| AAVE [전환] | Aster | $0.25M | $4.67M | 0.0001 | +3.957% | 동조 전환 |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ADA [전환] | Hyperliquid | $5.16M | $28.84M | 0.00001 | +3.013% | 마이너스→플러스 전환 |
| ADA [전환] | Aster | $0.51M | $1.33M | 0.0001 | +2.798% | 동조 전환 |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALGO [확대] | Hyperliquid | $0.55M | $1.96M | 0.00001 | +4.075% | 동조 플러스 확대 |
| ALGO [확대] | Aster | $0.006M | $0.04M | 0.00001 | +3.537% | 동조 |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ASTER(자체) [안정] | Aster | $13.06M | $224.77M | 0.0 | +1.398% | 자체 OI 안정 유지 |
| ASTER(자체) [안정] | Hyperliquid | $0.72M | $13.84M | 0.00001 | +1.441% | 동조 안정 |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| HYPE ⚠️ | Hyperliquid | $360.00M | $1,419.36M | 0.0 | -1.444%(이월) | chg 이상치로 직전값 이월(vol/OI 신선) |
| BLESS [보합] | Aster | $0.03M | $0.08M | 0.00027 | -7.833% | 거의 보합 지속 |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BTC ⚠️ | dYdX | $3.23M(이월) | $17.96M(이월) | 0.0 | +0.808%(이월) | 오라클가 $68,747.51로 시장과 6.8% 괴리, 전체 이월 |
| ETH ⚠️ | dYdX | $6.23M(이월) | $22.38M(이월) | 0.0000197 | +1.036%(이월) | 동일 사유로 전체 이월 |
| SOL ⚠️ | dYdX | $0.22M(이월) | $5.04M(이월) | 0.0 | +1.789%(이월) | 동일 사유로 전체 이월 |
| BTC ⚠️ | Hyperliquid | $3,803.52M | $2,577.01M | 0.00001 | +0.616%(이월) | chg 이상치로 직전값 이월(vol/OI 신선) |
| ETH ⚠️ | Hyperliquid | $2,159.68M | $1,869.54M | 0.00001 | +0.744%(이월) | chg 이상치로 직전값 이월(vol/OI 신선) |
| BTC ⚠️ | Aster | $1,334.73M | $845.86M | 0.0001 | +0.606%(이월) | chg 이상치로 직전값 이월(vol/OI 신선) |
| ETH [truncation 21연속] | Aster | — | — | — | — | base=ETH 항목 부재 재확인 |
| 1000RATS [유지] | Aster | $0.30M | $0.06M | 0.00001 | -22.772% | 극단적 하락권 유지, CEX와 동조 |
| AIO [완화] | Aster | $0.05M | $0.08M | 0.00005 | -7.743% | CEX와 동조 완화 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALLO [전환] | Aster | $0.10M | $0.06M | 0.0 | -1.476% | CEX와 동조 소폭 마이너스 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| APR [지속] | Aster | $0.24M | $0.29M | 0.00001 | -3.098% | 마이너스 지속, CEX와 동조 |
| APR [미상장] | Hyperliquid | — | — | — | — | 이번 회차도 HL 미상장 재확인 |
| BANK [반전] | Aster | $0.10M | $0.24M | 0.00001 | +1.118% | CEX와 함께 플러스로 반전 |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [회복] | Aster | $0.11M | $0.12M | 0.00001 | -0.163% | CEX와 함께 거의 보합 회복 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CAP [확대] | Aster | $0.09M | $0.16M | 0.00001 | +5.823% | CEX와 함께 플러스권 확대 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| FARTCOIN [강화] | Hyperliquid | $6.00M | $32.79M | 0.00009 | +7.643% | 플러스 지속 강화 |
| ETHFI [확대] | Hyperliquid | $3.30M | $11.41M | 0.00001 | +4.698% | 플러스권 확대, CEX(OKX)와 동조 |
| HYPER [확대] | Hyperliquid | $0.06M | $0.20M | 0.00001 | +4.547% | 플러스권 확대 |
| APEX [확대] | Hyperliquid | $0.20M | $0.69M | 0.00001 | +10.128% | Bybit와 함께 상승폭 확대 |
| HYNA:BTC-USD ⚠️ | Hyperliquid | $0.66M | $2.44M | 0.00001 | +1.292%(이월) | 기초자산 chg 이상치로 이월(vol/OI 신선) |
| HYNA:ETH-USD ⚠️ | Hyperliquid | $0.49M | $1.78M | 0.00005 | +2.14%(이월) | 기초자산 chg 이상치로 이월(vol/OI 신선) |
| HYNA:HYPE ⚠️ | Hyperliquid | $0.13M | $0.69M | -0.00001 | -1.0%(이월) | 기초자산 chg 이상치로 이월(vol/OI 신선) |
| HYNA:PUMP [신선] | Hyperliquid | $0.04M | $0.17M | 0.00001 | +11.249% | 별도 기초자산이라 신선값 채택 |
| HYNA:SOL-USD ⚠️ | Hyperliquid | $0.11M | $0.56M | 0.00001 | +3.205%(이월) | 기초자산 chg 이상치 우려로 이월(vol/OI 신선) |

## 테마 태그 (요약)

1. 직전 이월 12종목 복구 부분 성공(BTW·AEON 성공, 10종목 Binance만 2회차 연속 실패) (binance-cg-fetch-truncation-persists)
2. ACE 낙폭 재차 확대, 4벤뉴 -17~-18%대 심화 (ace-decline-deepens)
3. ⚠️ALPINE 상승진정→급격한 하락 방향 반전(신규) (alpine-flips-sharply-negative)
4. CASHCAT 뚜렷한 회복(HL·Aster) (cashcat-recovers-sharply)
5. KAITO 보합권 근접 수렴(OKX·HL) (kaito-converges-to-flat)
6. BANK 약세→플러스 반전(3벤뉴) (bank-flips-positive)
7. 1000RATS 극단적 하락권 유지(3벤뉴) (1000rats-remains-deeply-negative)
8. BSB 마이너스→거의 완전 보합 회복(OKX·Aster) (bsb-recovers-to-flat)
9. MMT 마이너스→플러스 전환(OKX) (mmt-turns-positive)
10. ⚠️신규: BTC·ETH·HYPE·SOL chg 이상치 관측, 실제 시장과 불일치 — 전부 이월 (majors-chg-anomaly-this-round)
11. BEAT OKX 낙폭 재확대, Binance 2회차 연속 폐기·이월 (beat-decline-widens)
12. BICO 낙폭 확대 지속, Binance 2회차 연속 이월 (bico-widens-negative)
13. GALA OKX 완화, Binance 2회차 연속 이월 (gala-mixed)
14. ETHFI OKX·HL 플러스권 크게 확대 (ethfi-strengthens-positive)
15. CAP OKX·Aster 플러스권 확대 지속 (cap-holds-positive)
16. AEON 전 벤뉴 낙폭 확대 (aeon-decline-widens)
17. APEX Bybit·HL 상승폭 확대 (apex-rally-extends)
18. GIGGLE OKX 거의 완전 보합 (giggle-near-flat)
19. CORE 플러스권 확대, Binance 미상장 지속 (core-widens-positive)
20. ATOM 마이너스→플러스 전환(전 벤뉴) (atom-turns-positive)
21. AAVE 마이너스/보합→플러스 전환(전 벤뉴) (aave-turns-positive)
22. ADA 마이너스→플러스 전환(전 벤뉴) (ada-turns-positive)
23. ALGO 플러스권 확대 지속(전 벤뉴, Bybit 신규 확인) (algo-strengthens-positive)
24. GRAM 플러스권 확대(OKX·HL) (gram-near-flat)
25. PIPPIN 소폭 마이너스 지속(OKX) (pippin-near-flat)
26. APR OKX 완화·Bybit 확대로 혼조 (apr-remains-negative)
27. AIO 마이너스 폭 완화 지속 (aio-mildly-improves)
28. ⚠️ALLO OI 3회차 연속 유지 — 방법론 아티팩트 재확인 (allo-oi-methodology-artifact-confirmed)
29. ASTER(자체토큰) 전 벤뉴 안정적 플러스권 (aster-cex-stable)
30. BLESS(Aster) 거의 보합 지속 (bless-mildly-improves)
31. dYdX 오라클가 이상치, 신뢰불가로 전체 이월 (dydx-oracle-anomaly-this-round)
32. 메이저(BTC·ETH·HYPE) chg 이상치, HYNA:*도 동일 이월(단 HYNA:PUMP 신선) (majors-chg-anomaly-this-round)
33. FARTCOIN 플러스 지속 강화 (fartcoin-flips-positive)
34. HYPER 플러스권 확대 (hyper-holds-positive)
35. HYNA:* 계열(HL) HIP-3 빌더배포 마켓, 계속 포함 유지 (hyna-builder-deployed-markets)
36. 데이터: OKX ticker 방식(last×volCcy24h/oiCcy) 신선 확보, funding은 다수 이월 (okx-ticker-methodology-fresh-funding-carryover)
37. 데이터: ⚠️CoinGecko binance_futures truncation 2회차 연속(10종목) (binance-cg-fetch-truncation-persists)
38. 데이터: BEAT Binance 신규값 2회차 연속 신뢰불가·폐기 (beat-fetch-unreliable-persists)
39. 데이터: CASHCAT Aster 오염 해소, 신선값 정상 확보 (cashcat-aster-contamination-resolved)
40. 데이터: OrangeX 39회차(약 79.75h) (orangex-service-outage-continues)
41. 데이터: Aster ETH truncation 21회차 연속 (truncation-continues-21st-round)
42. 글로벌 시총 약 $2.29조·BTC 도미넌스 약 56.5%, SEC 규제프레임 제안 촉매 (global-market-cap-sec-catalyst)
43. 주식화·상품 토큰 전부 제외 유지 (stock-commodity-tokens-excluded-crypto-native-confirmed)

## 한계

(a) **직전 회차 이월 12종목 복구는 부분 성공** — BTW·AEON은 신선값 확보했으나 BICO·GALA·
ETHFI·CAP·GIGGLE·MMT·GRAM·PIPPIN·BSB·KAITO는 Binance 측만 CoinGecko `binance_futures`
엔드포인트 truncation이 2회차 연속 지속돼 이월(타 벤뉴는 신선 확보); (b) **BEAT의 Binance
신규 fetch값이 2회차 연속 신뢰불가**(이번엔 직전 대비 약 87배 작음)로 폐기·이월했다; (c)
**CASHCAT의 Aster 값은 이번 회차 오염 없이 정상 회복**했다; (d) **⚠️신규: BTC·ETH·HYPE·SOL의
24h 변동률이 CoinGecko 경유 HL·Aster·dYdX 세 소스에서 +6~10%대로 반환됐으나 WebSearch 실측
시장(+0.29~0.5%)과 명백히 불일치**해 전부 신뢰불가로 판단, chg24(및 dYdX는 vol/OI까지)를
직전값으로 이월했다 — 원인은 불명(캐싱/기준시점 오류 등 추정)이며 다음 회차 재확인이 필요하다;
(e) ⚠️**ALLO OKX OI는 3회차 연속 $3.0~3.3M대 유지**가 재확인돼 방법론 전환 아티팩트 결론을
유지한다; (f) OrangeX 전면 중단이 39회차·약 79.75시간째 지속된다; (g) Aster ETH truncation이
21회차 연속 지속된다; (h) 글로벌 시총·도미넌스는 WebSearch 교차확인 기준(총 $2.29조·BTC
도미넌스 56.5%)이며 소스별 편차가 있을 수 있다; (i) 주식화·상품·프리IPO 합성 perp 토큰은
이번 회차도 전부 제외했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
