# 선물시장 스카우트 브리핑 — 2026-08-19 06:30 UTC (KST 2026-08-19 15:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 04:30 UTC)로부터 2시간 경과(정상 간격).**

## 시장 전반 — 이번 회차 핵심

1. **HYNA:SOL-USD ≡ SOL-USD 중복 확정 규명**: Hyperliquid CoinGecko 티커 전체(384개)를
   base 필드 기준으로 정밀 재검색한 결과 base가 정확히 'SOL'인 항목은 **존재하지 않고
   'HYNA:SOL'만 존재**함을 확인했다. 직전 회차까지 별도 실재 마켓으로 다뤄온 'SOL-USD(HL)'는
   HYNA:SOL-USD의 CoinGecko 추출 중복이었음이 확정돼 **이번 회차 dex 배열에서 제거**했다.
2. **AEON의 cex/dex 이중등재 오류 발견·수정**: 직전 회차 JSON의 `cex` 배열에 'AEON /
   Aster(CoinGecko대체)' 항목이 잘못 들어가 있었다(Aster는 DEX 퍼프이므로 dex에만 있어야
   함, dex에는 이미 정상 존재). 이번 회차에 cex 중복 항목을 제거해 정정했다 — 부모 세션이
   지적한 BTW/ETHFI 오분류와 같은 유형의 잔여 오류였다.
3. **BTW 5회차 연속 재가속 확정**: Aster +14.63%→+25.73%→+37.84%→+56.63%→**+66.598%**,
   Binance(BTWUSDT)도 **+67.443%**(vol $380.70M, OI 약 $148.54M)로 동조 지속.
4. **KAITO 4벤뉴 동시 뚜렷한 감속**: OKX +5.895%→**+3.723%**, Binance(USDT)
   +5.928%→**+3.593%**, Binance(USDC) +5.516%→**+3.695%**, HL +5.91%→**+3.759%**로
   재가속 흐름이 이번 회차 꺾였다.
5. **HYPE 낙폭 축소 추세 반전**: HL -0.99%→**-2.927%**로 직전 2회차의 개선 흐름이
   재차 악화됐다.
6. **FARTCOIN·ETHFI 다시 마이너스로 반전**: FARTCOIN +0.14%→-1.754%(HL), ETHFI
   +0.36~0.57%→-0.901%(HL)·-1.064%(Binance)로 직전 회차의 '플러스 반전'이 초단명이었다.
7. **APEX 뚜렷한 감속**: HL +10.13%→**+5.303%**, Bybit +9.259%→**+5.463%**로 양 벤뉴
   동조 감속.
8. **GALA V자 반전 후 소폭 재하락**: Binance -0.220%→**-3.654%**, OKX -0.146%→**-3.657%**,
   HL -0.80%→**-3.443%**로 3벤뉴가 다시 -3~4%대로 정렬됐으나 원래 -14% 저점과는 거리가
   멀다. 촉매는 여전히 미상.
9. **CASHCAT 낙폭 3회차 연속 완만히 축소**(-14.57%→-13.42%→**-12.258%**, HL).
10. **BICO -13%대에서 안정화**(3벤뉴 -13.27~-13.36% 수렴, 직전 -14.4%대보다 완화).
11. **BEAT 소폭 완화**(-25~26%대→-23.9~24.6%대).

**GALA OKX OI 데이터 소스 괴리 발견·해소**: CoinGecko `derivatives/exchanges/okex_swap`
경유 open_interest_usd가 $11.27M였으나 OKX 직접 API(`public/open-interest`의 oiCcy ×
`market/ticker`의 last)로 재계산하면 **$1.69M**로 6.6배 차이가 났다. 직전 회차 OKX GALA
OI가 $1.72M였던 것과 직접계산값이 거의 일치해 **CoinGecko 값을 이상치로 판단하고 직접
계산값을 채택**했다 — 향후 회차에서도 OKX OI는 직접계산(oiCcy×last)을 우선한다.

**ACE는 벤뉴별로 방향이 갈렸다** — Binance +39.839%→+39.620%(거의 보합), Bybit
+41.048%→+43.922%(확대), HL +42.38%→+36.379%(둔화), Aster +42.391%→+45.5%(확대).
방향은 혼조이나 4벤뉴 전부 펀딩이 음수(-0.00064~-0.00262)로 숏스퀴즈 서사는 유지된다.

**메이저(BTC·ETH·SOL)는 이번 회차도 안정권**을 유지했다 — dYdX BTC -0.176%, ETH
+0.465%, SOL +1.150%; HL BTC -0.135%, ETH +0.537%; Aster BTC -0.153%(ETH는 16회차
연속 truncation); Binance BTC -0.220%(vol $5,973.10M). **글로벌 시총·도미넌스는 WebSearch
교차확인 결과 총 $2.2~2.3조·BTC 도미넌스 약 56~59%(소스별 편차)로 직전 회차와 대체로
동일**하다.

**데이터 품질**: funding 단위 보정(CoinGecko 경유 percent→fraction, `/100`)을 이번
회차도 OKX·Bybit·Aster·Hyperliquid 전 항목에 적용했다. **교차검증**: OKX 직접 API의
GIGGLE·GRAM·PIPPIN funding-rate(각 0.00005)가 CoinGecko `/100` 보정값과 정확히 일치해
변환 방법론이 재검증됐다. 전 종목 funding 스케일 점검 결과 최대 절대값은 Binance
ACEUSDT -0.00261722(2.62e-3, 직전 -0.00257649와 유사)로 0.01 미만, 중앙값도 1e-5~5e-4
범위 안에 있어 이상 없음을 확인했다(단, OKX GALA OI 이상치 건 이후 OKX OI는 직접계산
우선). **CoinGecko `okex`(구 id)는 404**로 확인돼 올바른 id `okex_swap`으로 전환했다.
**Binance CoinGecko 벌크(`binance_futures`) 조회는 응답이 커 요청 심볼 다수가 요약
과정에서 누락**돼 개별 GET(`www.binance.com/fapi`)으로 보완했다. **OrangeX는 34회차·약
69.75시간째 전면 중단**(`getCurrencies` 코드1000 "No service found" 재현). **Aster ETH
truncation은 16회차 연속** 지속. **KAITOUSDC OI 및 일부 종목(ATOM·AAVE·ADA·ALGO·
PIPPIN·BSB·BANK·ALLO·AIO·1000RATS·ASTER)의 funding은 시간·호출 제약상 직전 회차 값을
이어받았고, 가격·거래량·대부분 OI는 갱신**했음을 정직 표기한다. **분류 오류 2건을 이번
회차에 수정**: (a) cex 배열의 중복 'AEON/Aster' 항목 제거, (b) dex 배열의 중복
'SOL-USD' 항목 제거(HYNA:SOL-USD와 완전 동일값 확정).

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

funding은 raw fraction 기준.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **BTW** [5회 재가속] | Binance(직접API) | $380.70M | $148.54M | 0.00098096 | **+67.443%** | 5회차 연속 재가속, Aster와 거의 동일 궤적 |
| ACE [보합] | Binance(직접API) | $698.62M | $20.94M | -0.00261722 | +39.620% | 직전과 거의 보합, 지속 음수 펀딩 |
| ACE [확대] | Bybit(CG대체) | $131.22M | $8.42M | -0.00228 | +43.922% | Binance보다 상승폭 확대, 벤뉴간 혼조 |
| **KAITO** [뚜렷 감속] | OKX(직접API) | $26.93M | $4.96M | -0.00025325 | +3.723% | 재가속 흐름 꺾임(+5.895%→+3.723%) |
| **KAITO** [USDT 감속] | Binance(직접API) | $32.28M | $14.85M | -0.00042575 | +3.593% | USDT마켓 동반 감속 |
| KAITO [USDC 감속] | Binance(직접API) | $3.82M | $1.14M | -0.00024545 | +3.695% | OKX·USDT와 동조 |
| **GALA** [재하락] | Binance(직접API) | $17.58M | $6.39M | -0.00021242 | **-3.654%** | V자 반전 후 소폭 재하락, 촉매 미상 |
| GALA [재하락] | OKX(직접API) | $5.16M | $1.69M | 0.00005 | -3.657% | 동조. OI는 CG이상치 대신 직접계산 채택 |
| **BICO** [안정화] | OKX(직접API) | $13.16M | $2.51M | -0.00014 | -13.27% | -13%대에서 안정화 |
| BICO [안정화] | Binance(직접API) | $15.41M | $5.16M | -0.00081425 | -13.271% | 동조 |
| BEAT [소폭 완화] | OKX(직접API) | $91.21M | $5.62M | 0.00039 | -24.51% | 낙폭 소폭 완화 |
| BEAT [소폭 완화] | Binance(직접API) | $104.52M | $9.93M | 0.00038837 | -23.924% | 동조 |
| AEON [심화] | OKX(직접API) | $54.96M | $3.63M | -0.00001 | -8.331% | 하락 심화, Binance 미상장 재확인(400) |
| **APEX** [뚜렷 감속] | Bybit(직접API) | $1.30M | $1.76M | 0.00005 | +5.463% | HL과 함께 감속(+9.259%→+5.463%) |
| **ETHFI** [재반전] | Binance(직접API) | $18.23M | $22.77M | 0.00005 | -1.064% | HL과 함께 다시 마이너스 |
| GIGGLE [보합] | Binance(직접API) | $16.66M | $10.83M | 0.00005 | -0.761% | 소폭 마이너스권 유지 |
| GIGGLE [보합] | OKX(직접API) | $8.86M | $1.63M | 0.00005 | -0.79% | 동조 |
| ALPINE [축소] | Binance(직접API, 재조회) | $76.05M | $2.22M | 0.00005 | +8.484% | 상승폭 축소(+15.7%→+8.5%) |
| ALPINE [축소] | Bybit(CG대체) | $14.12M | $0.79M | 0.00005 | +9.404% | 동조 |
| CORE [미상장 재확인] | OKX(직접API) | $1.92M | $0.93M | 0.00001 | -2.611% | Binance 400 재현, 단일소스 |
| CAP [보합] | Binance(직접API) | $22.90M | $14.89M | -0.0001603 | -0.347% | 소폭 마이너스 지속 |
| CAP [보합] | OKX(직접API) | $60.63M | $10.85M | -0.00028 | +0.029% | 거의 보합 |
| ATOM [보합] | OKX(직접API) | $3.55M | $3.72M | 0.0 | +0.643% | 보합권 |
| ATOM [보합] | Binance(직접API) | $14.41M | $15.28M | 0.00004 | +0.50% | 동조 |
| ATOM [보합] | Bybit(CG대체) | $6.52M | $13.64M | 0.0001 | +0.714% | 동조 |
| AAVE [소폭 마이너스] | OKX(직접API) | $16.95M | $11.85M | 0.00005 | -1.406% | 유지 |
| AAVE [소폭 마이너스] | Binance(CG+직접재확인) | $40.25M | $43.84M | -0.00005 | -1.394% | 동조 |
| AAVE [소폭 마이너스] | Bybit(CG대체) | $11.49M | $39.99M | 0.00004 | -1.384% | 동조 |
| ADA [소폭 플러스] | OKX(직접API) | $24.17M | $24.38M | 0.00006 | +1.094% | 지속 |
| ADA [소폭 플러스] | Binance(CG+직접재확인) | $77.84M | $84.25M | -0.00001178 | +1.036% | 동조 |
| ADA [소폭 플러스] | Bybit(CG대체) | $34.76M | $55.22M | 0.0001 | +0.748% | 동조 |
| ALGO [소폭 플러스] | Binance(직접API) | $5.85M | $7.85M | 0.00006 | +1.484% | 유지 |
| ALGO [소폭 플러스] | OKX(직접API) | $1.99M | $2.76M | 0.0001 | +1.407% | 동조 |
| MMT [소폭 마이너스] | OKX(직접API) | $3.56M | $2.09M | -0.0002361 | -1.386% | 지속 |
| MMT [소폭 마이너스] | Binance(직접API) | $6.01M | $8.10M | 미확보 | -1.267% | 동조 |
| GRAM [보합] | OKX(직접API) | $4.91M | $6.34M | 0.00005 | +0.152% | 유지 |
| GRAM [보합] | Binance(직접API) | $8.96M | $14.14M | 0.00005 | +0.152% | OKX와 완전 일치 |
| PIPPIN [전환] | OKX(직접API) | $3.18M | $1.72M | 0.00005 | -0.341% | 플러스→소폭 마이너스 |
| PIPPIN [보합] | Binance(직접API) | $5.98M | $5.75M | 0.00005 | +0.057% | OKX와 미세한 괴리 |
| BSB [소폭 플러스] | OKX(직접API) | $5.25M | $2.15M | 0.00032 | +1.101% | 유지 |
| BSB [소폭 플러스] | Binance(직접API) | $9.87M | $8.35M | 0.00007243 | +1.252% | 동조 |
| BANK [유지] | Binance(직접API) | $24.42M | $10.82M | 0.0 | +1.366% | 직전과 비슷 |
| BANK [유지] | Bybit(CG대체) | $2.80M | $4.07M | 0.00005 | +1.772% | 동조 |
| APR [유지] | OKX(직접API) | $68.42M | $3.52M | 0.00005 | +7.62% | 직전과 비슷한 수준 유지 |
| APR [유지] | Bybit(CG대체) | $10.15M | $3.45M | 0.00005 | +8.092% | 동조 |
| AIO [유지] | Binance(직접API) | $33.62M | $4.36M | 0.00005 | +4.862% | 플러스 유지 |
| ALLO [유지] | Binance(직접API) | $29.72M | $12.31M | 0.00005 | +2.048% | 유지 |
| ALLO [유지] | Bybit(CG대체) | $4.29M | $4.37M | 0.00005 | +1.797% | 동조 |
| 1000RATS [유지] | Binance(직접API) | $97.90M | $12.94M | 0.00047982 | +7.386% | 두자리대 근접 유지 |
| ASTER(자체) [안정] | Binance(직접API) | $12.10M | $69.66M | 0.00005 | -0.432% | 안정 유지 |
| ASTER(자체) [안정] | OKX(직접API) | $2.99M | $8.28M | -0.00002 | -0.366% | 동조 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 34회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **BTW** [5회 재가속] | Aster | $5.95M | $12.88M | 0.00017 | **+66.598%** | +14.63%→...→+56.63%→+66.60% |
| **KAITO** [뚜렷 감속] | Hyperliquid | $1.69M | $5.76M | -0.00009 | +3.759% | OKX·Binance와 함께 감속(+5.91%→+3.76%) |
| ACE [둔화] | Hyperliquid | $3.48M | $2.07M | -0.00072 | +36.379% | 4벤뉴 중 유일하게 뚜렷이 둔화 |
| ACE [확대] | Aster | $1.12M | $0.25M | -0.00064 | +45.5% | HL과 반대로 확대, 방향 혼조 |
| ACE [중단] | OrangeX | — | — | — | — | 34회차·약 69.75시간 |
| **HYPE** [악화] | Hyperliquid | $231.61M | $1,307.38M | 0.00001 | **-2.927%** | 낙폭 축소 추세가 재차 반전·악화 |
| **FARTCOIN** [재반전] | Hyperliquid | $2.69M | $29.65M | 0.00003 | -1.754% | 직전 플러스 반전이 초단명, 재하락 |
| **ETHFI** [재반전] | Hyperliquid | $3.79M | $11.47M | 0.00001 | -0.901% | Binance와 동조 재하락 |
| **APEX** [뚜렷 감속] | Hyperliquid | $0.29M | $0.66M | 0.00001 | +5.303% | Bybit와 동조 감속(+10.13%→+5.30%) |
| CASHCAT [지속 완화] | Hyperliquid | $8.82M | $12.33M | 0.00001 | -12.258% | 3회차 연속 낙폭 축소 |
| CASHCAT [지속 완화] | Aster | $0.66M | $0.69M | 0.00006 | -12.211% | 동조 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GALA [재하락] | Hyperliquid | $1.00M | $1.13M | -0.00012 | -3.443% | Binance·OKX와 동조, 촉매 미상 |
| BEAT [소폭 심화] | Aster | $0.34M | $0.15M | 0.00001 | -25.468% | OKX·Binance와 달리 소폭 심화 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BICO [안정화] | Aster | $0.05M | $0.10M | 0.00005 | -13.356% | -13%대로 수렴 |
| BICO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **AEON** [오분류 수정] | Aster | $0.04M | $0.31M | 0.00006 | -11.438% | OKX와 동조 심화. cex 중복 등재 제거 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [보합] | Hyperliquid | $1.65M | $15.28M | 0.00001 | +0.441% | 동조 |
| ATOM [보합] | Hyperliquid | $0.47M | $1.69M | 0.0 | +0.743% | 동조 |
| ATOM [보합] | Aster | $0.01M | $1.67M | 0.0001 | +0.643% | 보합 |
| AAVE [소폭 마이너스] | Hyperliquid | $2.77M | $57.39M | 0.00001 | -1.399% | 동조 |
| AAVE [소폭 마이너스] | Aster | $0.24M | $4.48M | 0.00009 | -1.472% | 동조 |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ADA [소폭 플러스] | Hyperliquid | $3.74M | $29.39M | 0.00001 | +1.123% | 동조 |
| ADA [소폭 플러스] | Aster | $0.17M | $1.21M | 0.0001 | +1.036% | 동조 |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALGO [플러스] | Hyperliquid | $0.38M | $1.82M | 0.00001 | +1.45% | 동조 |
| ALGO [플러스] | Aster | $0.01M | $0.04M | 0.00001 | +1.792% | 동조 |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ASTER(자체) [안정] | Aster | $10.18M | $221.00M | 0.0 | -0.398% | 안정 유지 |
| ASTER(자체) [안정] | Hyperliquid | $0.32M | $13.50M | 0.00001 | -0.447% | 동조 |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BLESS [확대] | Aster | $0.02M | $0.10M | 0.00005 | -2.443% | 마이너스 확대(-1.61%→-2.44%) |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BTC [안정] | dYdX | $2.94M | $17.38M | 0.0 | -0.176% | 메이저 안정 |
| ETH [안정] | dYdX | $3.05M | $23.66M | 0.00000664 | +0.465% | 메이저 안정 |
| SOL [안정] | dYdX | $0.42M | $4.96M | ~0 | +1.150% | 메이저 안정 |
| BTC [안정] | Hyperliquid | $1,461.06M | $2,581.12M | 0.00001 | -0.135% | 메이저 안정 |
| ETH [안정] | Hyperliquid | $669.71M | $1,693.49M | 0.0 | +0.537% | 메이저 안정 |
| BTC [안정] | Aster | $501.78M | $802.66M | 0.00003 | -0.153% | 메이저 안정 |
| ETH [truncation 16연속] | Aster | — | — | — | — | base=ETH 항목 부재 재확인 |
| 1000RATS [유지] | Aster | $0.41M | $0.04M | 0.00014 | +4.815% | Binance보다 낮으나 동조 |
| AIO [유지] | Aster | $0.08M | $0.09M | 0.00005 | +4.877% | Binance와 동조 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALLO [유지] | Aster | $0.14M | $0.07M | 0.00001 | +2.196% | 유지 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| APR [유지] | Aster | $0.29M | $0.34M | 0.00001 | +6.352% | OKX·Bybit와 동조 |
| APR [미상장] | Hyperliquid | — | — | — | — | 384개 전체 재검색으로 재확인 |
| BANK [유지] | Aster | $0.08M | $0.26M | 0.00001 | +2.524% | 유지 |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [유지] | Aster | $0.11M | $0.13M | 0.00001 | +2.4% | 유지 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CAP [보합] | Aster | $0.06M | $0.17M | -0.00002 | -0.564% | Binance·OKX와 동조 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| HYPER [소폭 감속] | Hyperliquid | $0.05M | $0.20M | -0.00002 | +1.7% | 직전보다 소폭 감속 |
| HYNA:BTC-USD | Hyperliquid | $0.44M | $2.21M | 0.00001 | +0.30% | HIP-3 빌더배포, BTC 동조 |
| HYNA:ETH-USD | Hyperliquid | $0.19M | $1.62M | 0.00001 | +0.48% | HIP-3 빌더배포, ETH 동조 |
| HYNA:HYPE | Hyperliquid | $0.13M | $0.64M | 0.00001 | -1.21% | HIP-3 빌더배포, HYPE 동조 |
| HYNA:PUMP | Hyperliquid | $0.06M | $0.16M | 0.00001 | +10.904% | HIP-3 빌더배포 |
| **HYNA:SOL-USD** [중복 확정] | Hyperliquid | $0.03M | $0.53M | 0.00001 | +1.695% | 별도 'SOL-USD' 부재 확정, 유일 실재 항목 |

## 테마 태그 (요약)

1. HYNA:SOL-USD ≡ SOL-USD 중복 확정, 중복 항목 제거(sol-usd-duplicate-confirmed-removed)
2. AEON cex/dex 이중등재 오류 발견·수정(aeon-cex-dex-duplicate-fixed)
3. BTW 5회 연속 재가속(btw-continues-accelerating)
4. KAITO 4벤뉴 동시 감속(kaito-decelerates-across-venues)
5. HYPE 낙폭 축소 추세 반전·악화(hype-reverses-worse)
6. FARTCOIN·ETHFI 재차 마이너스 반전(fartcoin-flips-negative-again / ethfi-flips-negative-again)
7. APEX 뚜렷 감속(apex-decelerates)
8. GALA V자 반전 후 소폭 재하락, 촉매 미상(gala-v-shaped-reversal)
9. CASHCAT 3회차 연속 낙폭 축소(cashcat-narrows-continuously)
10. BICO -13%대 안정화(bico-stabilizes-around-13pct)
11. BEAT 소폭 완화(beat-decline-mildly-eases)
12. ACE 벤뉴별 방향 혼조, 숏스퀴즈 서사 유지(ace-short-squeeze-thin-float-confirmed)
13. GIGGLE/ALPINE/CORE/CAP/ATOM/AAVE/ADA/ALGO/MMT/GRAM/PIPPIN/BSB/BANK/APR/AIO/ALLO/1000RATS/ASTER — 세부는 표 참고
14. HYNA:* 계열 계속 포함(hyna-builder-deployed-markets)
15. 데이터: OKX id 오류 수정(okex→okex_swap), GALA OI 이상치 발견·직접계산 채택(okx-oi-coingecko-discrepancy-found), Binance 벌크 절단 재확인, funding 변환 재검증, OrangeX 34회차(~69.75h), Aster ETH truncation 16회차, 일부 항목 직전값 이어받음(정직표기)
16. 글로벌 시총·도미넌스 대체로 동일(global-dominance-roughly-unchanged)
17. 주식화·상품 토큰 전부 제외 유지

## 한계

(a) 이번 회차는 KAITOUSDC의 OI와 일부 안정권 종목(ATOM·AAVE·ADA·ALGO·PIPPIN·BSB·
BANK·ALLO·AIO·1000RATS·ASTER)의 funding을 직전 회차 값으로 이어받았다 — 가격·거래량·
대부분 OI는 갱신했으며 정직 표기; (b) **HL SOL 단독 티커 부재를 이번 회차 명시적으로
확정**했다 — 전체 384개 티커의 base 필드를 정밀 재검색해 'HYNA:SOL' 외 'SOL' 단독 항목이
없음을 확인, 이전 회차들의 'SOL-USD 실재 마켓' 표기가 오류였음이 드러났다; (c) **AEON의
cex 배열 중복 등재 오류를 발견해 수정**했다 — Aster는 DEX 퍼프이므로 cex 배열에 들어가면
안 되는데 직전 회차까지 잘못 남아있었다; (d) **OKX GALA OI에서 CoinGecko와 직접계산값의
6.6배 괴리를 발견**해 직접계산(oiCcy×last)을 채택했다 — 이 이상치가 다른 OKX 종목에도
존재하는지는 이번 회차에 전수 검증하지 못했으므로 다음 회차 이후 지속 점검이 필요하다;
(e) CoinGecko 파생거래소 id `okex`는 404이며 올바른 id는 `okex_swap`이다(이번 회차 확인,
향후 회차에 반영 권장); (f) Binance CoinGecko 벌크 조회(`binance_futures`)는 응답이 커
개별 심볼이 요약 과정에서 누락되므로, 개별 GET(`www.binance.com/fapi`) 방식이 여전히
필요하다; (g) OrangeX 전면 중단이 34회차·약 69.75시간째 지속된다; (h) Aster ETH
truncation이 16회차 연속 지속되며, 이번 회차는 CoinGecko `aster` 티커에 base=ETH 항목이
아예 없음을 명시적으로 확인했다; (i) 글로벌 시총·도미넌스는 WebSearch 스니펫 교차확인이며
CoinGecko `/global` 직접조회는 이번 회차도 생략했다; (j) 주식화·상품·프리IPO 합성 perp
토큰은 이번 회차도 전부 제외했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
