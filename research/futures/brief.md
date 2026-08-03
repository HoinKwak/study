# 선물시장 스카우트 브리핑 — 2026-08-03 22:29 UTC (KST 2026-08-04 07:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-03T20:29:00Z)
> 로부터 2시간 경과.**

CoinGecko `/global`로 총 시총 **$2.26T**(24h **-0.036%**), BTC 도미넌스 **56.37%**, ETH 도미넌스
**9.92%**를 확보했다 — 직전 회차($2.27T, +0.44%, 56.46%/9.95%)와 시총·도미넌스 수준 자체는 거의
동일하지만, **24h 변동률이 지난 2회차 연속 +0.44% 플래토에서 이번엔 -0.036%로 처음 마이너스로
전환**됐다. OKX BTC-USDT-SWAP 직접 조회(last 63500.1/open24h 63440)로도 BTC **+0.095%**(직전
+0.764%)로 뚜렷이 식어, 리스크온 숨고르기가 이번 회차부터 완만한 하향 전환 조짐을 보이기 시작했다
(급락은 아니고 초기 냉각 신호 수준).

## ⚠️ 이번 회차 데이터 소스 이상 (더 심화)

`orangex`는 3회 연속, `dydx_v4`는 3회 연속, `gmx`는 4회 연속 404로 실패했다. `xt_derivatives`
(GIGGLE)는 이번엔 200 응답을 받았으나 페이지 truncation으로 종목을 끝내 찾지 못해 — 실패 유형이
429→truncation으로 바뀌었을 뿐 결과는 동일하게 4회 연속 미확인이다. 반면 CoinGecko `okex_swap`
(정확한 OKX 파생 ID로 재확인, 기존 `okex` 단독 ID는 이번에도 404) 및 OKX 공개 API 직접 조회는
정상 작동해 신뢰도를 보완했다.

## 이번 회차 핵심

**BICO는 4회 연속 감속**했다 — OKX raw JSON(last 0.01683/open24h 0.01424) 확인으로 **+18.26%**
(직전 +27.45%)까지 추가로 꺾였고, funding도 -0.193%→**-0.104%**로 계속 정상화돼 숏스퀴즈 압력이
거의 소진 단계에 근접했다.

**1000RATS는 이번 회차 극적으로 거의 완전히 반전**됐다 — Binance-0.51%·Bybit-1.67%·Aster-0.39%
(3소스 평균 **-0.85%**)로, 직전(+18.17%)에서 사실상 펌프 전 구간이 통째로 되돌려졌다. 웹서치에서는
여전히 +25.48% 상승이라는 상반된 스냅샷(CoinGecko 캐시로 추정)도 확인됐으나, 3개 거래소 직접조회가
일관되게 근접 flat/마이너스를 가리켜 이를 우선 신뢰한다 — 전형적인 상장 펌프의 완전한 소멸
(round-trip) 사례로 판단된다.

**ALLO는 3회 연속 감속**했다 — Binance+2.43%·Bybit+2.64%·OKX+2.61%(평균 **+2.56%**, 직전 +4.43%)로
추가 둔화, 5/18 Cobot(AI 트레이딩 툴) 런칭이라는 과거 촉매의 모멘텀이 계속 소진되는 모습이다.

**BEAT는 회복세가 일시 정체·소폭 재악화**됐다 — 이번 회차 OKX 레그만 재확인됐고(Aster 레그는
top-리스트에서 미포착) **-10.99%**(직전 평균 -9.21%, 직전 OKX 단독은 -9.43%)로 소폭 더 깊어져,
3회 연속 이어지던 낙폭 축소 흐름이 이번엔 살짝 멈칫했다.

**KAITO는 완만한 회복이 계속되나 속도가 크게 둔화**됐다 — OKX -9.58%→**-8.28%**로 개선 지속, 반면
HL은 -9.34%→**-9.25%**로 사실상 정체 — CEX·DEX 두 레그의 개선 속도가 갈렸다.

**⚠️ BLESS 관련 상충은 이번 회차 단서를 하나 더 확보**했다 — Aster 레그가 -28.00%→**-35.81%**로
낙폭을 더 키운 가운데, OKX 직접 조회에서 `BLESS-USDT-SWAP` 자체가 '상품 미존재'로 응답해 **OKX
계열(OrangeX 포함 추정)에서 BLESS가 상장폐지 상태임을 재확인**했다. 웹서치로 재확인한 '+98% 급등'
기사(HOKANEWS)는 본문에 '8/3 01:30 UTC CoinMarketCap 데이터 기준'이라는 오래된 타임스탬프가 박혀
있어, 이번 회차(22:29 UTC) 기준으로는 이미 21시간 가까이 지난 **스테일(구식) 캐시 데이터**로
추정된다 — 이에 따라 Aster 직접조회(지속 하락)를 더 신뢰도 있는 신호로 판단한다.

**CASHCAT은 3회 연속 재가속 이후 이번 회차 처음 감속**했다 — HL+41.40%·Aster+43.47%(평균 **+42.44%**,
직전 +48.07%)로 상승폭이 줄었다 — CoinGecko 스팟(+43.10%)과도 정합적이라 데이터 신뢰도는 높다.
웹서치로 로빈후드 CEO 블라드 테네브가 7/29 실적콜에서 CASHCAT을 언급해 Robinhood Chain 시총 1위를
재탈환했다는 뉴스도 확인 — 상장 펌프에 이어 유명인 언급이라는 2차 촉매가 있었으나, 이번 회차 감속은
그 열기도 정점을 지나는 신호로 해석된다.

**BTW는 재가속**했다 — Aster +21.32%→**+30.68%**로 다시 튀었고 OI도 $6.94M→**$7.39M**로 함께 늘어
신규 포지션 유입 시사, 2회 연속 감속 후 반전이다.

## 이번 회차 요약

①**BULLA는 급격히 둔화**했다 — +7.67%→**-0.04%**로 거의 flat까지 꺾여, 완만한 둔화 흐름이 이번엔
뚜렷한 정지로 바뀌었다.

②**MMT는 반전해 플러스로 전환**했다 — -3.58%→**+1.09%**(OKX), AEON도 -3.51%→**-2.28%**로 낙폭이
줄어 저활동 오실레이션 종목군에서 완만한 회복 조짐이 나타났다.

③**BANK·CAP은 낙폭이 크게 축소**됐다 — BANK CEX(Binance-3.70%·Bybit-4.32%, 평균 **-4.01%**, 직전
-8.47%)·DEX(Aster **-4.13%**, 직전 -8.12%)가 함께 개선, CAP(Aster **-3.99%**, 직전 -8.73%)도 큰 폭
개선. 반대로 **AKE는 소폭 더 악화**됐다 — CEX(Binance **-5.86%**, 직전 -2.94%)·DEX(Aster **-4.02%**,
직전 -3.57%) 모두 마이너스 심화.

④**ATOM·ALGO는 둔화가 지속**됐다 — ATOM 평균 CEX+DEX **+7.2%**(직전 +7.9%대), ALGO **+7.6%대**
(직전 +8.7%대)로 소폭 냉각, 웹서치에서도 유효한 신규 촉매를 찾지 못했다(ATOM 관련 'Coinbase dYdX
네이티브 지원' 뉴스는 2025년 8월 기사로 확인돼 이번 이벤트와 무관).

⑤**신규로 ACE(Fusionist)의 funding 극단이 포착**됐다 — Binance funding **-0.118%**(통상
±0.005~0.01%대 대비 10배 이상, 24h 변동은 +1.43%로 미미)로 숏 포지션이 크게 우세한 극단적 스큐가
관측됐으나 개별 촉매는 확인되지 않았다.

⑥ADA(+2.4%대, 직전 +3.04%)·AAVE(CEX -0.84%·HL -1.00%, 직전 +0.65%/+0.55%에서 마이너스로 전환)·
ASTER(CEX -0.69%·DEX -0.59%, 직전 근접 flat에서 소폭 마이너스 심화)·HYPE(+1.88%, 직전 +4.13%)·
FARTCOIN(-0.25%, 직전 +1.42%)·CORE(+3.01%, 직전 +8.30%, 3회 연속 감속)도 시장 전반 냉각과 궤를
같이했다.

⑦**⚠️ HYPER-USD·APEX-USD(HL)는 이번 회차도 top-리스트에서 미포착돼 2회 연속 이월**했다.

## 시장 전반

- **총 시총 $2.26T(24h -0.036%), BTC 도미넌스 56.37%, ETH 도미넌스 9.92% — 2회 연속 이어지던 +0.44% 플래토가 이번 회차 처음 마이너스로 전환. BTC 직접조회도 +0.76%→+0.10%로 뚜렷이 식어 초기 리스크오프 조짐.**
- **BICO 4회 연속 감속(+27.45%→+18.26%), funding도 계속 정상화 — 숏스퀴즈 압력 소진 단계 근접.**
- **1000RATS 극적 완전 반전(+18.17%→-0.85%) — 상장 펌프가 사실상 완전히 소멸(round-trip).**
- **CASHCAT 3회 연속 재가속 이후 첫 감속(+48.07%→+42.44%) — topping 조짐, 로빈후드 CEO 언급이라는 2차 촉매도 열기 정점 통과 가능성.**
- **AAVE·FARTCOIN·ASTER 등이 시장 냉각과 함께 플러스→마이너스로 전환 — 종목별로도 리스크오프 조짐이 확산되는 모습.**
- **⚠️ orangex·dydx_v4(3회 연속)·gmx(4회 연속)·xt_derivatives(4회 연속, 이번엔 truncation) 데이터 소스 이슈가 계속 심화.**

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BICO (Biconomy)** [4회 연속 감속] | OKX(okex_swap/직접API) | $131.02M | $2.63M | -0.104% | +18.26% | +27.45%→+18.26%, funding도 -0.193%→-0.104%로 계속 정상화 — 숏스퀴즈 압력 소진 단계 근접 | deceleration-4th-round-funding-near-normalized |
| **1000RATS** [⚠️ 극적 완전 반전] | Binance/Bybit/Aster | $407.98M | $30.75M | +0.02% | -0.85% | +18.17%→-0.85%로 펌프 사실상 완전 소멸. 웹서치 +25.48%와 상충하나 3소스 직접조회 우선 신뢰 | near-complete-reversal-listing-pump-fully-erased |
| **ALLO (Allora)** [3회 연속 감속] | Binance/Bybit/OKX | $148.06M | $17.84M | -0.0047% | +2.56% | +4.43%→+2.56%로 추가 둔화, Cobot 런칭 촉매 모멘텀 소진 | deceleration-3rd-round-catalyst-fading |
| **BEAT (Audiera)** [회복 일시 정체] | OKX(직접API, Aster 미포착) | $261.70M | $8.68M | +0.005% | -10.99% | -9.21%→-10.99%(OKX 단독)로 소폭 재악화, 3회 연속 낙폭축소 흐름 멈칫 | recovery-pauses-slightly-reverses-aster-leg-unconfirmed |
| **KAITO (CEX)** [회복 지속, 속도 둔화] | OKX(직접API) | $99.81M | $8.01M | +0.002% | -8.28% | -9.58%→-8.28%로 개선 지속, HL(-9.25%)은 거의 정체 — 속도 괴리 | gradual-recovery-continues-pace-diverges-from-dex |
| **BANK** [낙폭 크게 축소] | Binance/Bybit | $174.83M | $23.84M | -0.008% | -4.01% | -8.47%→-4.01%로 큰 폭 개선, DEX(-4.13%)도 함께 개선 | decline-narrows-sharply-both-legs |
| **AKE** [소폭 더 악화] | Binance | $130.39M | $30.67M | +0.019% | -5.86% | -2.94%→-5.86%로 마이너스 심화, DEX(-4.02%)도 악화 | worsens-slightly-both-legs |
| **ATOM** [둔화 지속] | Binance/Bybit | $37.31M | $32.68M | +0.0035% | +7.53% | +7.9%→+7.5%대 소폭 냉각, 촉매 미확인('Coinbase dYdX' 뉴스는 2025년 기사로 확인) | decelerates-slightly-no-catalyst-confirmed |
| **ALGO** [둔화 지속] | Binance/Bybit | $37.02M | $16.71M | +0.01% | +6.84% | +8.3%→+6.8%대 소폭 냉각, 촉매 미확인 | decelerates-slightly-no-catalyst-confirmed |
| **MMT (Momentum)** [반전, 플러스 전환] | OKX(직접API) | $20.30M | $3.28M | -0.012% | +1.09% | -3.58%→+1.09%로 완만한 개선이 부호 반전까지 이어짐 | reverses-to-positive |
| AEON [소폭 개선] | OKX(okex_swap) | $13.27M | $2.98M | -0.007% | -2.28% | -3.51%→-2.28%로 낙폭 축소 | improves-slightly-oscillation-continues |
| APR (aPriori) [유사 지속] | OKX(okex_swap) | $1.83M | $1.04M | +0.005% | -4.70% | -4.38%→-4.70%로 큰 변화 없음 | similar-continues |
| CORE [3회 연속 감속] | OKX(okex_swap) | $15.97M | $1.26M | -0.016% | +3.01% | +8.30%→+3.01%로 추가 둔화, 초기 팝 열기 거의 소진 | decelerates-3rd-round |
| ADA [시장과 소폭 냉각] | Binance/Bybit/OKX | $478.97M | $221.56M | +0.0093% | +2.34% | +3.04%→+2.34%, 시장 전반 숨고르기 전환과 궤를 같이함 | cools-slightly-with-market |
| **AAVE** [마이너스로 전환] | Binance/Bybit/OKX | $110.79M | $105.40M | +0.0013% | -0.84% | +0.69%→-0.84%로 시장 냉각과 함께 반전 | flips-negative-with-market |
| **ACE (Fusionist)** [신규 — funding 극단] | Binance | $17.79M | $3.49M | -0.118% | +1.43% | funding -0.118%(통상 대비 10배+, 숏이 롱에 지불)로 극단 스큐, 가격은 미미 — 촉매 미확인 | new-funding-extreme-no-price-catalyst |
| ASTER (CEX) [소폭 마이너스 심화] | Binance/Bybit/OKX | $14.27M | $122.24M | -0.0003% | -0.69% | -0.26%→-0.69%, 여전히 근접 flat이나 방향은 소폭 더 마이너스 | near-flat-slightly-deepens |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM)

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| BLESS-USDT-PERPETUAL [⚠️ 3회 연속 조회 실패] | OrangeX | $294.86M(이월) | $102.36M(이월) | -0.073%(이월) | +12.00%(이월) | `orangex` 404 지속. OKX에서 BLESS-USDT-SWAP '상품 미존재' 확인 — 상장폐지 가능성 뒷받침 | fetch-failed-404-3rd-round-carried-forward |
| **BLESS-USDT** [낙폭 확대, 상충 단서 확보] | Aster | $2.91M | $0.26M | +0.013% | -35.81% | -28.00%→-35.81% 하락 지속. 웹서치 '+98%' 기사는 21시간 지난 스테일 캐시(8/3 01:30 UTC CMC 기준)로 추정 | decline-deepens-websearch-conflict-traced-to-stale-cache |
| **CASHCAT** [3회 연속 재가속 후 첫 감속] | Hyperliquid/Aster | $12.84M | $10.84M | -0.0135% | +42.44% | +48.07%→+42.44%(HL+41.40%·Aster+43.47%)로 상승폭 축소. 스팟(+43.10%)과 정합. 로빈후드 CEO 7/29 실적콜 언급 확인 — topping 조짐 | first-deceleration-after-3round-acceleration-topping-signal |
| **BTW** [재가속] | Aster | $0.68M | $7.39M | +0.015% | +30.68% | +21.32%→+30.68%로 재차 튐, OI도 $6.94M→$7.39M 증가 — 신규 포지션 유입 시사 | reaccelerates-after-2round-deceleration |
| **BULLA** [급격 둔화, 거의 flat] | Aster | $1.26M | $6.99M | +0.004% | -0.04% | +7.67%→-0.04%로 완만한 둔화가 뚜렷한 정지로 전환 | sharply-decelerates-near-flat |
| AKE-USDT [CEX와 함께 소폭 더 악화] | Aster | $1.50M | $12.26M | +0.009% | -4.02% | -3.57%→-4.02%, CEX(-5.86%)와 함께 마이너스 심화 | worsens-slightly-with-cex |
| **BANK-USDT** [낙폭 크게 축소] | Aster | $0.84M | $0.34M | -0.003% | -4.13% | -8.12%→-4.13%로 개선, CEX(-4.01%)와 거의 일치 | decline-narrows-sharply-matches-cex |
| **CAP-USDT** [낙폭 크게 축소] | Aster | $0.02M | $0.03M | +0.001% | -3.99% | -8.73%→-3.99%로 큰 폭 개선 | decline-narrows-sharply |
| ASTER-USDT [소폭 마이너스 심화] | Aster | $7.42M | $219.33M | 0.0% | -0.59% | -0.41%→-0.59%, OI $219.3M 대규모 유지 | near-flat-slightly-deepens |
| ATOM-USD [둔화 지속] | Aster/Hyperliquid | $0.94M | $3.79M | +0.0015% | +6.89% | +8.0%→+6.9%로 소폭 냉각, 촉매 미확인 | decelerates-slightly-no-catalyst-confirmed |
| ALGO-USD [둔화 지속] | Aster/Hyperliquid | $2.51M | $3.01M | -0.001% | +8.39% | +9.2%→+8.4%로 소폭 냉각, 촉매 미확인 | decelerates-slightly-no-catalyst-confirmed |
| HYPE-USD [냉각 지속] | Hyperliquid | $224.31M | $1,211.16M | +0.001% | +1.88% | +4.13%→+1.88%로 계속 식음, OI $1,211.2M 대규모 유지 | cools-further |
| HYPER-USD [⚠️ 2회 연속 미포착, 이월] | Hyperliquid | $0.59M(이월) | $0.37M(이월) | -0.012%(이월) | -6.43%(이월) | top-리스트에서 재차 미포착, 재확인 실패 | not-recaptured-2nd-round-carried-forward |
| KAITO-USD [사실상 정체] | Hyperliquid | $16.17M | $23.85M | +0.001% | -9.25% | -9.34%→-9.25%로 거의 변화 없음, OKX(-8.28%)는 계속 개선 중이라 대비 | plateaus-diverges-from-cex-improvement |
| APEX-USD [⚠️ 2회 연속 미포착, 이월] | Hyperliquid | $0.07M(이월) | $0.80M(이월) | +0.001%(이월) | +1.29%(이월) | top-리스트에서 재차 미포착, 재확인 실패 | not-recaptured-2nd-round-carried-forward |
| **FARTCOIN** [마이너스로 전환] | Hyperliquid | $6.21M | $21.01M | +0.001% | -0.25% | +1.42%→-0.25%, 시장 냉각과 함께 반전 | flips-negative-with-market |
| ADA-USD [CEX와 소폭 냉각] | Hyperliquid | $10.28M | $31.97M | 0.0% | +2.37% | +2.90%→+2.37%, CEX ADA(+2.34%)와 유사 | cools-slightly-with-cex |
| **AAVE-USD** [마이너스로 전환] | Hyperliquid | $6.23M | $65.77M | -0.001% | -1.00% | +0.55%→-1.00%, CEX AAVE(-0.84%)와 함께 반전 | flips-negative-with-cex |
| ETH-USD [⚠️ 3회 연속 조회 실패] | dYdX | $12.62M(이월) | $19.41M(이월) | -0.010%(이월) | +0.25%(이월) | `dydx_v4` 404 지속 | fetch-failed-404-3rd-round-carried-forward |
| BTC-USD [⚠️ 3회 연속 조회 실패] | dYdX | $7.31M(이월) | $17.47M(이월) | +0.001%(이월) | +1.06%(이월) | ETH-USD와 동일 현상 | fetch-failed-404-3rd-round-carried-forward |
| LIT-USD (dYdX) [⚠️ 재동결, 5회 연속 재확인 불가] | dYdX | $14.31(이월) | $14,718.01(이월) | 0.0%(이월) | +1.14%(이월) | dydx_v4 404로 재확인 자체 불가 | refreeze-status-carried-api-fetch-failed |
| KAITO-USD (dYdX) [⚠️ 3회 연속 조회 실패] | dYdX | $488.35(이월) | $0.0(이월) | 0.0%(이월) | 0.0%(이월) | dydx_v4 404로 재확인 불가 | fetch-failed-404-3rd-round-carried-forward |
| ETH/USD (WETH-USDC) [⚠️ 4회 연속 조회 실패] | GMX | $23.40M(이월) | $16.14M(이월) | +0.001%(이월) | +2.21%(이월) | 404 재차 실패 — 구조적 이슈 지속 | fetch-failed-4th-round-carried-forward |
| BTC/USD (BTC-USDC) [⚠️ 4회 연속 조회 실패] | GMX | $7.52M(이월) | $33.60M(이월) | +0.002%(이월) | +1.23%(이월) | ETH/USD와 동일 현상 | fetch-failed-4th-round-carried-forward |
| GIGGLE (Giggle Fund) [⚠️ 4회 연속 조회 실패] | XT.COM | $34.11M(이월) | $224.34M(이월) | +0.5%(이월) | +6.12%(이월) | 이번엔 200 응답이나 truncation으로 미확인 — 실패 유형만 바뀜 | fetch-failed-4th-round-truncation-carried-forward |

## 테마 태그

1. **⚠️ 시장 전반 냉각 전환: 총 시총 $2.26T(-0.036%), BTC 도미넌스 56.37% — 2회 연속 이어지던 플래토가 이번 회차 처음 마이너스로 전환, BTC도 뚜렷이 식음. 초기 리스크오프 조짐** (market-momentum-turns-slightly-negative).
2. **BICO, 4회 연속 감속(+27.45%→+18.26%), funding도 계속 정상화 — 숏스퀴즈 압력 소진 단계 근접** (deceleration-4th-round-funding-near-normalized).
3. **1000RATS, 극적 완전 반전(+18.17%→-0.85%) — 상장 펌프가 사실상 완전히 되돌려짐(round-trip 소멸)** (near-complete-reversal-listing-pump-fully-erased).
4. **CASHCAT, 3회 연속 재가속 이후 첫 감속(+48.07%→+42.44%) — topping 조짐, 로빈후드 CEO 실적콜 언급 확인** (first-deceleration-after-3round-acceleration-topping-signal).
5. **⚠️ BLESS, Aster 레그 낙폭 확대(-28.00%→-35.81%) — OKX에서 상장폐지 뒷받침 확인, 웹서치 '+98%' 기사는 스테일 캐시로 추정돼 상충 원인 단서 확보** (decline-deepens-websearch-conflict-traced-to-stale-cache).
6. **BTW 재가속(+21.32%→+30.68%, OI 증가) vs BULLA 급격 둔화(+7.67%→-0.04%) — Aster 소형 종목군 내 방향 분화** (aster-small-cap-divergence).
7. **MMT 반전 플러스(-3.58%→+1.09%), AEON 소폭 개선 — 저활동 오실레이션 종목군 회복 조짐** (low-activity-group-mild-recovery).
8. **BANK·CAP 낙폭 크게 축소, 반대로 AKE는 소폭 더 악화 — 소형 종목군 내 혼조** (mixed-recovery-among-small-caps).
9. **ATOM·ALGO 둔화 지속, 여전히 개별 촉매 미확인** (decelerates-slightly-no-catalyst-confirmed).
10. **신규 포착: ACE(Fusionist) funding 극단(-0.118%, 통상 대비 10배+) — 가격 변동은 미미, 촉매 미확인** (new-funding-extreme-no-price-catalyst).
11. **AAVE·FARTCOIN·ASTER, 시장 냉각과 함께 플러스에서 마이너스로 전환 — 리스크오프 조짐 확산** (flips-negative-with-market-cooling).
12. **⚠️ 데이터 신뢰도 이슈 심화: orangex·dydx_v4 3회 연속, gmx 4회 연속, xt_derivatives도 4회 연속(이번엔 truncation) 미확인 — 구조적 이슈 고착화** (persistent-multi-source-failures-deepen).
13. **웹서치 정정: BLESS '+98%' 기사는 스테일 캐시(8/3 01:30 UTC 타임스탬프)로 추정, ATOM 'Coinbase dYdX 지원' 뉴스는 2025년 기사로 확인 — 두 건 모두 오정합 원인을 이번 회차에 규명** (websearch-catalyst-corrections).

## 데이터 신뢰도

**이번 회차 데이터 소스 이상은 이전보다 더 심화됐다.** (a) `orangex`·`dydx_v4`는 **3회 연속** 404,
`gmx`는 **4회 연속** 404로 실패가 굳어졌다. (b) `xt_derivatives`(GIGGLE)는 이번엔 200 응답을 받았으나
페이지가 truncation돼 종목을 찾지 못했다 — 실패의 성격이 429(rate limit)에서 truncation(응답
과대·잘림)으로 바뀌었을 뿐, 결과적으로는 4회 연속 미확인이다. (c) 반면 CoinGecko `okex_swap`
(기존 시도했던 `okex` 단독 ID는 이번에도 404 — 올바른 ID는 `okex_swap`임을 재확인) 및 OKX 공개
API(`market/ticker`+`public/funding-rate`)를 raw JSON으로 직접 조회해 BICO·KAITO·MMT를 재검증했다.
계산은 `volCcy24h(기초자산 단위, ctVal 반영) × last가격` 방식으로 USD 환산했다.

**⚠️ 웹서치 대조에서 두 건의 상충 사례 원인을 이번 회차에 규명했다.** ① BLESS의 '+98% 급등' 기사는
본문에 '8/3 01:30 UTC CoinMarketCap 데이터 기준'이라는 타임스탬프가 명시돼 있어, 이번 회차(22:29
UTC) 대비 21시간 가까이 지난 스테일 캐시 콘텐츠로 추정된다 — 반면 Aster 직접조회(-35.81%)와 OKX의
'BLESS-USDT-SWAP 상품 미존재' 확인은 서로 정합적(상장폐지→유동성 고갈→하락)이라 이쪽을 더 신뢰도
있는 신호로 판단했다. ② ATOM 관련 'Coinbase dYdX 네이티브 지원' 뉴스는 검색 결과 재검토 결과 실제
2025년 8월 기사로 확인돼, 이번 회차 ATOM 상승과는 무관함을 확인했다.

**funding 값 단위 관련 주의**: CEX·DEX 종목의 funding 값은 각 API가 반환한 원시 수치를 percent
스케일로 그대로 사용했다(예: CoinGecko `funding_rate` 필드 값을 직접 percent로 취급, OKX raw
`fundingRate`는 소수를 100배해 percent로 환산). 거래소·필드별로 스케일 표기 관례가 다를 수 있어
**회차 간 funding 절대값 비교는 참고용으로만** 활용하고, 방향(양전/음전)과 가격·거래량 추세를 우선
신뢰할 것을 권한다. 이번 회차 신규 포착한 ACE의 funding -0.118%는 다른 종목들의 통상 ±0.005~0.01%대
대비 10배 이상 큰 값이라 '극단'으로 표기했다.

한계: (a) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며, 이번
회차 새롭게 발견된 대형 신규 급등 종목은 ACE(funding 극단) 1건뿐이다(전체 시장을 포괄하는 완전한
스캔은 아님); (b) HYPER-USD·APEX-USD(HL)는 이번 회차도 top-리스트에서 재확인되지 않아 이월했다;
(c) OrangeX·dYdX·GMX·XT.COM은 위에서 설명한 대로 이번 회차도 미해결이며, 실패가 3~4회 연속 이어져
구조적 이슈로 굳어지고 있다; (d) BEAT의 Aster 레그는 이번 회차 top-리스트에서 포착되지 않아
재확인하지 못했다; (e) **주식화·상품·레버리지 ETF 토큰**은 이번 회차도 규약에 따라 cex/dex
리스트에서 전부 제외했다(Binance 목록에서 AMZN·AAPL 등 토큰화 주식이 상위 거래량에 포함된 것을
확인했으나 전부 제외 처리).

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
