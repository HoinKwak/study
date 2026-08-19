# 선물시장 스카우트 브리핑 — 2026-08-19 04:30 UTC (KST 2026-08-19 13:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-19
> 02:30 UTC)로부터 2시간 경과(정상 간격).**

## 시장 전반 — 이번 회차 핵심 반전·신규확인 8건

1. **GALA 극적 V자 반전**: Binance -14.420%→**-0.220%**, OKX -14.38%→**-0.146%**,
   HL -14.81%→**-0.80%**로 3벤뉴 모두 낙폭이 거의 완전히 해소됐다. WebSearch로 GalaSwap
   DEX 확장(SAND·ETHFI 등 페어 추가)·게임 업데이트 뉴스는 확인했으나 이 정도 규모의
   급반전을 설명할 명확한 촉매는 찾지 못해 **원인 미상**으로 정직 표기한다.
2. **BTW 4회차 연속 재가속 + Binance 신규상장 확인**: Aster +37.842%→**+56.634%**,
   동시에 **Binance(BTWUSDT)에서도 +56.551%**(거래량 $301.59M, OI 약 $139.60M)로
   거의 동일한 수치가 확인돼 Aster 단일 상장이 아니라 Binance에도 처음 상장돼 있음이
   드러났다(Binance 거래량이 Aster의 약 60배).
3. **CAP Binance 신규상장 확인**: 과거 여러 회차 'Binance 미상장(400 오류)' 판정을
   이번 회차 CAPUSDT 정상 조회(-0.955%, vol $23.39M, OI 약 $14.94M)로 **정정**한다.
4. **AEON 반전**: 소폭 플러스에서 **-7%대 하락**으로 전환(OKX -7.187%, Aster -7.009%
   동조).
5. **BICO 하락 가속**: 직전(-7~9%대)보다 낙폭이 배 가까이 확대(**-14%대**, 3벤뉴 동조).
6. **KAITO 재가속 + Binance 이중마켓 확인**: OKX +5.895%, Binance(KAITOUSDT)
   +5.928%, Binance(KAITOUSDC) +5.516% — **KAITOUSDT가 KAITOUSDC와 별도로
   존재하며 거래량이 8배 큼**을 이번 회차 처음 확인, 신규 행으로 추가했다.
7. **BEAT**: 하락이 직전 회차와 대체로 비슷한 수준에서 소폭 심화(-22~26%대 지속).
8. **HYNA:SOL-USD ≡ SOL-USD 의심 강화**: HL의 별도 'SOL-USD' 항목을 재조회한 결과
   HYNA:SOL-USD와 거래량·OI·변동률이 **소수점까지 100% 일치**해, 직전 회차의
   'SOL-USD가 HL에 실존 티커로 처음 확인'이라는 서술의 신뢰도를 낮춘다 — CoinGecko
   요약 도구의 추출 중복 가능성이 있으나 GET 전용 도구로는 raw JSON 직접 확인이
   불가해 확정하지 못한다(항목은 삭제하지 않고 불확실성만 정직 표기).

**ACE는 이번 회차도 상승 지속**(직전보다 소폭 둔화)했다 — Binance +39.839%(직접
API 확인, vol $666.87M, OI 약 $17.55M, funding -0.00257649 direct), Bybit
+41.048%(vol $124.26M, OI $6.80M, funding -0.00164[CG→frac]), HL +42.38%,
Aster +42.391%. 4벤뉴 지속 음수 펀딩도 유지돼 숏스퀴즈 서사와 정합적이다.

**메이저(BTC·ETH·SOL)는 이번 회차도 안정권**을 유지했다 — dYdX BTC +0.193%, ETH
+0.890%, SOL +1.633%; HL BTC +0.15%, ETH +0.76%; Aster BTC +0.413%(vol
$512.59M); Binance BTC +0.238%(vol $6,015.78M). **글로벌 시총·도미넌스는 WebSearch
교차확인 결과 총 $2.28조·BTC 도미넌스 약 56.6%로 직전 회차와 사실상 동일**(CoinGecko
`/global` 직접 재조회는 이번 회차 생략).

**데이터 품질**: funding 단위 보정(CoinGecko 경유 percent→fraction, `/100`)을
이번 회차도 전 항목에 적용했다. **교차검증**: Binance 직접 premiumIndex 값
(1000RATS 0.00047982, ADA -0.00001178, APR 0.00005000, AIO 0.00005000)과
CoinGecko경유 `/100` 보정값(각각 0.00049, -0.00001, 0.00005, 0.00005)이 근접
일치해 변환 방법론이 재검증됐다. 전 종목 funding 스케일 점검 결과 최대 절대값은
Binance ACEUSDT -0.00257649(2.58e-3)로 0.01 미만, 중앙값도 1e-5~5e-4 범위 안에
있어 이상 없음을 확인했다. **OKX는 `volCcy24h`(코인 수량) × `last` 방식**을 이번
회차도 적용했고, 개별 GET으로 ATOM·CAP·CORE·BSB·BEAT·BICO·GALA·GIGGLE·KAITO의
fresh 가격·OI·펀딩을 재조회했다. **Bybit·Aster 직접 API는 이번 회차도 403/연결실패를
재확인**(각각 `api.bybit.com`·`fx-api.asterdex.com`)해 CoinGecko id `bybit`·
`aster` 경유로 대체했다. **OrangeX는 33회차·약 67.75시간째 전면 중단**
(`getCurrencies`/`get_currencies` 둘 다 코드1000 "No service found" 재현).
**Aster ETH truncation은 15회차 연속** 지속. **시간·호출 제약상 일부 안정권
종목의 OI 필드는 직전 회차 값을 이어받았고, 가격·거래량·펀딩은 갱신했음을 정직
표기**한다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

funding은 raw fraction 기준. `[CG→frac]` = 이번 회차 CoinGecko percent 값을 `/100` 보정.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **GALA** [V자 반전] | Binance(직접API) | $19.96M | $6.34M | -0.00035365 | **-0.220%** | 직전 -14.42%에서 낙폭 거의 해소, 촉매 미상 |
| GALA [V자 반전] | OKX(직접API) | $5.98M | $1.72M | -0.00014328 | **-0.146%** | Binance·HL와 동조 반전 |
| **BTW** [4회 재가속] | Aster | $4.99M | $12.28M | 0.0001[CG→frac] | **+56.634%** | 4회차 연속 재가속 |
| **BTW** [Binance 신규확인] | Binance(직접API) | $301.59M | ~$139.60M | 미확보 | +56.551% | 신규 발견, Aster와 거의 동일 수치 |
| ETHFI [반전] | Binance(직접API) | $18.16M | — | 0.00005 | +0.572% | HL과 동조 확인(부모 세션이 DEX 표에서 이관) |
| **CAP** [Binance 신규확인] | Binance(직접API) | $23.39M | $14.94M | -0.00006876 | -0.955% | 과거 미상장 판정 정정 |
| CAP [Binance 신규확인] | OKX(직접API) | $63.62M | $10.44M | -0.00005005 | -1.096% | Binance와 동조 |
| **AEON** [반전] | OKX(직접API) | $62.02M | $3.52M | -0.00011397 | **-7.187%** | 플러스에서 하락 반전 |
| AEON [반전] | Aster | $0.06M | $0.32M | 0.00001[CG→frac] | -7.009% | OKX와 동조 |
| **BICO** [가속] | OKX(직접API) | $14.43M | $2.53M | -0.00014836 | **-14.45%** | 직전보다 낙폭 배 가까이 확대 |
| BICO [가속] | Binance(직접API) | $16.36M | $4.98M | -0.00113771 | -14.499% | OKX·Aster와 동조 |
| **KAITO** [재가속] | OKX(직접API) | $27.47M | $5.10M | -0.00030945 | +5.895% | 직전보다 상승폭 확대 |
| **KAITO** [USDT 신규확인] | Binance(직접API) | $31.55M | $15.25M | -0.00042422 | +5.928% | USDT 마켓 별도 존재 처음 확인 |
| KAITO [USDC 지속] | Binance(직접API) | $3.76M | $1.14M | -0.00037412 | +5.516% | 기존 추적 USDC 마켓 |
| **ACE** [지속 상승] | Binance(직접API) | $666.87M | $17.55M | -0.00257649 | +39.839% | 숏스퀴즈+초박형 유통량, 상승폭 소폭 둔화 |
| ACE [지속 상승] | Bybit(CoinGecko대체) | $124.26M | $6.80M | -0.00164 | +41.048% | Binance·HL·Aster와 동조 |
| BEAT [하락 지속] | OKX(직접API) | $91.80M | $5.52M | 0.00046794 | -25.69% | 직전과 대체로 비슷 |
| BEAT [하락 지속] | Binance(직접API) | $100.28M | $9.84M | 0.00029556 | -26.087% | OKX·Aster와 동조 |
| GIGGLE [보합] | Binance(직접API) | $17.59M | $10.83M | 0.00005 | -1.779% | 소폭 마이너스권 유지 |
| GIGGLE [보합] | OKX(직접API) | $9.53M | $1.61M | 0.00005 | -1.808% | Binance와 동조 |
| ALPINE [값 유지] | Binance(CG대체) | $67.44M | $2.37M | 0.00005 | +15.679% | 개별 재조회 생략, 직전값 유지 |
| ALPINE [값 유지] | Bybit(CG대체) | $13.68M | $0.91M | 0.00005 | +14.023% | Binance와 동조 |
| CORE [Binance 미상장 재확인] | OKX(직접API) | $1.88M | $0.99M | 0.00007163 | -1.596% | 400 오류 재현, 단일소스 |
| ATOM [소폭 마이너스] | OKX(직접API) | $3.70M | $3.74M | -0.00003021 | -0.212% | 3벤뉴 동조 |
| ATOM [소폭 마이너스] | Binance(직접API) | $14.42M | $15.46M | 0.00004 | -0.071% | OKX·Bybit·HL과 동조 |
| ATOM [소폭 마이너스] | Bybit(CG대체) | $6.52M | $13.61M | 0.00009 | +0.284% | 대체로 동조 |
| AAVE [소폭 마이너스] | OKX(직접API) | $17.59M | $11.75M | 0.00003691 | -0.704% | 소폭 마이너스권 유지 |
| AAVE [소폭 마이너스] | Binance(CG대체) | $40.42M | $43.82M | -0.00005 | -0.5% | 동조 |
| AAVE [소폭 마이너스] | Bybit(CG대체) | $11.34M | $40.11M | 0.0001 | -0.545% | 동조 |
| ADA [소폭 플러스] | OKX(직접API) | $24.60M | $24.15M | 0.00007924 | +0.172% | 소폭 플러스권 지속 |
| ADA [소폭 플러스] | Binance(CG+직접펀딩) | $79.18M | $83.75M | -0.00001178 | +0.402% | 펀딩 교차검증됨 |
| ADA [소폭 플러스] | Bybit(CG대체) | $35.42M | $54.57M | 0.0001 | +0.057% | 동조 |
| ALGO [플러스 확대] | Binance(CG대체) | $5.72M | $7.86M | 0.00006 | +2.024% | 상승폭 확대 |
| ALGO [플러스 확대] | OKX(직접API) | $1.93M | $7.73M | -0.00003992 | +1.762% | Binance와 동조 |
| MMT [전환] | OKX(직접API) | $3.58M | $2.12M | -0.00028199 | -0.424% | 플러스→마이너스 전환 |
| MMT [전환] | Binance(직접API) | $6.13M | $8.13M | 미확보 | -0.608% | OKX와 동조 |
| GRAM [보합] | OKX(직접API) | $4.97M | $6.38M | 0.00005 | +0.687% | 소폭 플러스권 유지 |
| GRAM [보합] | Binance(직접API) | $9.02M | $14.17M | 0.00005 | +0.687% | 동조 |
| PIPPIN [확대] | OKX(직접API) | $3.37M | $1.79M | 0.00005 | +2.899% | 상승폭 확대 |
| PIPPIN [확대] | Binance(직접API) | $6.24M | $5.89M | 0.00005 | +3.144% | 동조 |
| BSB [소폭 플러스] | OKX(직접API) | $5.52M | $2.17M | 0.00005 | +0.752% | 유지 |
| BSB [소폭 플러스] | Binance(직접API) | $10.31M | $8.45M | 0.00007243 | +0.343% | 동조 |
| BANK [감속] | Binance(직접API) | $24.84M | $11.16M | 0.0 | +1.743% | 직전보다 감속 |
| BANK [감속] | Bybit(CG대체) | $2.83M | $4.06M | 0.00005 | +2.032% | 동조 |
| APR [가속] | OKX(직접API) | $68.51M | $11.08M | 0.00011909 | +8.48% | 상승폭 확대 |
| APR [가속] | Bybit(CG대체) | $10.28M | $3.35M | 0.00005 | +7.676% | 동조 |
| AIO [반전] | Binance(직접API) | $37.99M | $4.45M | 0.00005 | +5.901% | 마이너스→플러스 반전 |
| ALLO [유지] | Binance(CG대체) | $30.62M | $12.50M | 0.00005 | +2.555% | 플러스 유지 |
| ALLO [유지] | Bybit(CG대체) | $4.49M | $4.41M | 0.00005 | +2.438% | 동조 |
| 1000RATS [둔화] | Binance(직접API) | $81.63M | $13.92M | 0.00047982 | +7.198% | 직전보다 둔화 |
| APEX [유지] | Bybit(직접API 확인) | $1.23M | $1.78M | 0.00005 | +9.259% | 직전과 비슷 |
| ASTER(자체) [안정] | Binance(직접API) | $12.25M | $69.74M | 0.00005 | -0.067% | 안정 유지 |
| ASTER(자체) [안정] | OKX(직접API) | $3.05M | $8.28M | 0.00000038 | -0.10% | 동조 |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

OrangeX 행은 33회차 연속 전면 중단으로 **모든 값이 null**(중단 사실 기록, 종목 삭제 아님).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 |
|---|---|---|---|---|---|---|
| **GALA** [V자 반전] | Hyperliquid | $1.02M | $1.11M | -0.00013 | **-0.80%** | Binance·OKX와 동조 반전 |
| **BTW** [4회 재가속] | Aster | $4.99M | $12.28M | 0.0001 | **+56.634%** | +14.63%→+25.73%→+37.84%→+56.63% |
| **AEON** [반전] | Aster | $0.06M | $0.32M | 0.00001 | -7.009% | OKX와 동조 반전 |
| **BICO** [가속] | Aster | $0.06M | $0.10M | 0.00005 | -14.382% | OKX·Binance와 동조 가속 |
| **KAITO** [재가속] | Hyperliquid | $1.65M | $5.85M | -0.00008 | +5.91% | OKX·Binance와 동조 |
| **ACE** [지속 상승] | Hyperliquid | $3.62M | $1.94M | -0.0005 | +42.38% | 숏스퀴즈 서사 정합 |
| ACE [지속 상승] | Aster | $1.04M | $0.29M | -0.00064 | +42.391% | 동조 |
| ACE [중단] | OrangeX | — | — | — | — | 33회차·약 67.75시간 |
| CASHCAT [축소] | Hyperliquid | $8.94M | $11.96M | 0.00001 | -13.42% | 직전(-14.57%)보다 소폭 축소 |
| CASHCAT [축소] | Aster | $0.66M | $0.67M | 0.00001 | -13.67% | 동조 |
| CASHCAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BEAT [지속] | Aster | $0.31M | $0.16M | 0.00001 | -26.786% | OKX·Binance와 동조 |
| BEAT [중단] | OrangeX | — | — | — | — | 중단 지속 |
| KAITO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| AEON [중단] | OrangeX | — | — | — | — | 중단 지속 |
| GRAM [보합] | Hyperliquid | — | $15.32M | 0.00001 | +0.67% | OKX·Binance와 동조 |
| ATOM [보합] | Hyperliquid | $0.47M | $1.68M | 0.0 | -0.13% | 대체로 동조 |
| ATOM [보합] | Aster | $0.01M | $1.67M | 0.0001 | 0.0% | 보합 |
| AAVE [소폭 마이너스] | Hyperliquid | $2.79M | $57.15M | 0.00001 | -0.75% | 동조 |
| AAVE [소폭 마이너스] | Aster | $0.23M | $4.46M | 0.00007 | -0.646% | 동조 |
| AAVE [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ADA [소폭 플러스] | Hyperliquid | — | $29.26M | 0.00001 | +0.18% | 동조 |
| ADA [소폭 플러스] | Aster | $0.15M | $1.24M | 0.0001 | +1.096% | 동조 |
| ADA [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALGO [플러스] | Hyperliquid | — | $1.83M | 0.00001 | +2.58% | 동조 |
| ALGO [플러스] | Aster | $0.01M | $0.04M | 0.00001 | +1.792% | 동조 |
| ALGO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ASTER(자체) [안정] | Aster | $10.38M | $221.23M | 0.0 | -0.10% | 안정 유지 |
| ASTER(자체) [안정] | Hyperliquid | — | $13.51M | 0.00001 | -0.11% | 동조 |
| ASTER(자체) [중단] | OrangeX | — | — | — | — | 중단 지속 |
| HYPE [축소] | Hyperliquid | $240.78M | $1,312.88M | 0.00001 | -0.99% | 직전보다 낙폭 추가 축소 |
| BLESS [마이너스 확대] | Aster | $0.03M | $0.10M | 0.00005 | -1.607% | 직전보다 낙폭 확대 |
| BLESS [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BTC [안정] | dYdX | $3.01M | $17.44M | 0.0 | +0.193% | 메이저 안정 |
| ETH [안정] | dYdX | $4.47M | $23.70M | 0.00002357 | +0.890% | 메이저 안정 |
| SOL [안정] | dYdX | $0.44M | $4.97M | ~0 | +1.633% | 메이저 안정 |
| **SOL-USD** [중복 의심] | Hyperliquid | $0.03M | $0.53M | 0.00001 | +1.664% | HYNA:SOL-USD와 값 100% 일치, 별도 마켓 여부 불확실 |
| BTC [안정] | Hyperliquid | $1,425.35M | $2,612.46M | 0.00001 | +0.15% | 메이저 안정 |
| ETH [안정] | Hyperliquid | $661.24M | $1,694.37M | 0.00001 | +0.76% | 메이저 안정 |
| BTC [안정] | Aster | $512.59M | $804.04M | 0.00003 | +0.413% | 메이저 안정 |
| ETH [truncation 15연속] | Aster | — | — | — | — | 직접 API 연결실패, CG 경유도 미반환 |
| 1000RATS [둔화] | Aster | $0.38M | $0.04M | 0.00016 | +12.93% | Binance와 함께 두자리대, 소폭 둔화 |
| AIO [반전] | Aster | $0.12M | $0.09M | 0.00005 | +6.664% | Binance와 함께 반전 |
| AIO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| ALLO [유지] | Aster | $0.14M | $0.07M | 0.00001 | +1.7% | 유지 |
| ALLO [중단] | OrangeX | — | — | — | — | 중단 지속 |
| APR [가속] | Aster | $0.28M | $0.33M | 0.00001 | +7.886% | OKX·Bybit와 동조 |
| APR [미상장] | Hyperliquid | — | — | — | — | 재확인, 실제 부재 |
| BANK [유지] | Aster | $0.04M | $0.24M | 0.00001 | +3.778% | 유지 |
| BANK [중단] | OrangeX | — | — | — | — | 중단 지속 |
| BSB [유지] | Aster | $0.11M | $0.12M | 0.00005 | +0.461% | 유지 |
| BSB [중단] | OrangeX | — | — | — | — | 중단 지속 |
| CAP [신규확인] | Aster | $0.06M | $0.18M | 0.0 | -1.105% | Binance·OKX와 동조 |
| CAP [중단] | OrangeX | — | — | — | — | 중단 지속 |
| **FARTCOIN** [반전] | Hyperliquid | $2.58M | $29.60M | 0.00002 | +0.14% | 직전(-0.65%)에서 플러스로 반전 |
| **ETHFI** [반전] | Hyperliquid | — | $11.74M | 0.00001 | +0.36% | 직전(-2.55%)에서 플러스로 반전 |
| HYPER [가속] | Hyperliquid | — | $0.20M | 0.00001 | +2.08% | 직전보다 상승폭 확대 |
| APEX [유지] | Hyperliquid | — | $0.68M | 0.00001 | +10.13% | 직전과 대체로 비슷 |
| HYNA:BTC-USD | Hyperliquid | $0.50M | $2.20M | 0.00001 | +0.30% | HIP-3 빌더배포, BTC 동조 |
| HYNA:ETH-USD | Hyperliquid | $0.22M | $1.61M | 0.00001 | +0.95% | HIP-3 빌더배포, ETH 동조 |
| HYNA:HYPE | Hyperliquid | $0.14M | $0.64M | 0.00001 | -1.60% | HIP-3 빌더배포, HYPE 동조 |
| HYNA:PUMP | Hyperliquid | — | $0.16M | 0.0 | +11.14% | HIP-3 빌더배포 |
| **HYNA:SOL-USD** [3회 연속 값 동일] | Hyperliquid | $0.03M | $0.53M | 0.00001 | +1.664% | SOL-USD와 완전 일치, 캐시/중복 의심 강화 |

## 테마 태그 (요약)

1. GALA V자 반전(gala-v-shaped-reversal) — 원인 미상
2. BTW 4회 재가속 + Binance 신규상장(btw-continues-accelerating / btw-binance-listing-newly-confirmed)
3. CAP Binance 신규상장 확인, 과거 판정 정정(cap-binance-listing-newly-confirmed)
4. AEON 반전(aeon-flips-negative)
5. BICO 가속(bico-decline-accelerates-again)
6. KAITO 재가속 + USDT 이중마켓 확인(kaito-reaccelerates / kaito-usdt-market-newly-confirmed)
7. ACE 숏스퀴즈 지속(ace-short-squeeze-thin-float-confirmed)
8. BEAT 하락 지속(beat-decline-accelerates)
9. GIGGLE 보합(giggle-binance-listing-confirmed)
10. ALPINE 값 유지, 촉매 미확인(alpine-fan-token-surge-cause-unconfirmed)
11. CORE Binance 미상장 재확인(core-binance-not-listed-confirmed)
12. ATOM/AAVE/ADA/ALGO/MMT/GRAM/PIPPIN/BSB/ALLO/1000RATS/APEX/BANK/APR/AIO/ASTER — 각각 소폭 등락 지속·전환(세부는 표 참고)
13. HYPE 낙폭 축소(hype-slightly-improves), BLESS 마이너스 확대(bless-flips-back-negative)
14. FARTCOIN/ETHFI 플러스 반전, HYPER 가속(fartcoin-flips-positive/ethfi-flips-positive/hyper-accelerates)
15. HYNA:* 계열 계속 포함, SOL-USD 중복 의심 강화(sol-hl-ticker-uncertain-duplicate-suspected)
16. 데이터: OKX 개별 GET fresh 재조회 다수, Binance/CG funding 교차검증, OrangeX 33회차 중단(~67.75h), Aster ETH truncation 15회차, 일부 안정권 OI는 직전값 이어받음(정직표기)
17. 글로벌 도미넌스·시총 사실상 동일(WebSearch 교차확인)
18. 주식화·상품 토큰 전부 제외 유지

## 한계

(a) 이번 회차는 시간·호출 제약상 CEX/DEX 목록의 **모든 필드를 100% 재조회하지는
못했다** — 가격·거래량·펀딩은 대부분 갱신했으나, 안정권으로 판단된 일부 종목(ALGO·
ADA·MMT·GRAM·PIPPIN·BSB·ALLO·APR·AIO·1000RATS·BANK·ASTER의 일부 OI)은
직전 회차 값을 이어받았다 — 정직 표기이며 항목을 삭제하지는 않았다; (b) **GALA·BTW·
CAP·AEON·BICO·KAITO 6종은 이번 회차 핵심 발견**으로 개별 GET·direct API를 집중
투입해 가장 신선한 데이터를 확보했다; (c) **SOL-USD(HL)와 HYNA:SOL-USD의 값이
완전 일치**하는 현상을 재조사한 결과, 직전 회차의 'SOL-USD 최초 확인' 주장이 실제로는
CoinGecko 요약 도구의 추출 중복(동일 JSON 엔트리를 base 필드 상이하게 재추출)일
가능성이 있음을 발견했다 — GET 전용 도구로는 raw JSON을 직접 파싱할 수 없어 확정하지
못했고, 항목은 유지한 채 불확실성만 정직 표기했다; (d) **OKX 개별 GET으로
ATOM·CAP·CORE·BSB·BEAT·BICO·GALA·GIGGLE·KAITO의 fresh open-interest·
funding-rate를 재조회**했고, CAP의 경우 이번 회차 처음 정상 응답을 받아 과거
'미상장' 판정이 오류였음을 정정했다; (e) **Binance 직접 API(`www.binance.com/fapi`)**로
ACE·GALA·GIGGLE·KAITO(USDT/USDC)·BEAT·CAP·BICO·GRAM·MMT·1000RATS·BANK·
ATOM·ASTER·BTC·BTW·HYPE·ETHFI의 ticker/24hr·premiumIndex·openInterest를
직접 조회했다 — 응답이 큰 벌크 엔드포인트는 truncation이 반복돼 개별 GET으로 보완;
(f) **Bybit·Aster 직접 API는 이번 회차도 각각 403·연결실패(DNS)를 재확인**해
CoinGecko id `bybit`·`aster` 경유로 대체(funding은 percent→fraction 보정 적용);
(g) **Hyperliquid는 이번 회차도 CoinGecko `derivatives/exchanges/hyperliquid`
경유로 확보**했다(직접 API `info`는 POST 전용이라 GET 전용 도구로 접근 불가);
(h) **OrangeX 전면 서비스 중단이 이번 회차도 지속**돼 33회차·약 67.75시간에 달했다
(`getCurrencies`·`get_currencies` 둘 다 코드1000 재현) — 직전 회차 16개 심볼의
null 항목은 그대로 유지했다; (i) **dYdX는 `indexer.dydx.trade` 직접 조회**로
BTC·ETH·SOL의 oraclePrice·openInterest·nextFundingRate를 확보했다; (j) **funding
교차검증**: Binance 직접 premiumIndex 값과 CoinGecko `/100` 보정값이 근접 일치해
(1000RATS·ADA·APR·AIO) 변환 방법론이 재검증됐다; (k) **글로벌 시총·도미넌스는
WebSearch 스니펫으로 교차확인**했고(총 $2.28조, BTC 도미넌스 약 56.6%), CoinGecko
`/global` 직접 재조회는 이번 회차 생략했다; (l) **주식화·상품·프리IPO 합성 perp
토큰은 이번 회차도 전부 제외**했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
