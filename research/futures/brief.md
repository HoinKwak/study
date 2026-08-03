# 선물시장 스카우트 브리핑 — 2026-08-03 20:29 UTC (KST 2026-08-04 05:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-03T18:28:00Z)
> 로부터 약 2시간1분 경과.**

CoinGecko `/global`로 총 시총 **$2.27T**(+0.44% 24h), BTC 도미넌스 **56.46%**, ETH 도미넌스 **9.95%**를
확보했다 — 직전 회차($2.268T, +0.44%, 56.44%)와 거의 동일하다. 24h 변동률이 지난 회차와 완전히 같은
+0.44%로 유지돼, 지난 회차 처음 관측된 '리스크온 모멘텀 숨고르기'가 이번 회차도 그대로 지속됐다(재가속도
추가 냉각도 없이 플래토). OKX BTC-USDT-SWAP 직접 조회로 BTC **+0.764%**(직전 +0.781%)로 거의 동일 수준
유지했다.

## ⚠️ 이번 회차 데이터 소스 이상 (지속화 조짐)

`orangex`·`dydx_v4`·`gmx`·`xt_derivatives` 4개 거래소 ID가 이번 회차도 모두 404/429로 응답 실패했다
— **orangex·dydx_v4는 2회 연속**, **gmx·xt_derivatives는 3회 연속** 실패로, 단발성 문제라기보다
CoinGecko 측 지속적 이슈이거나 ID 자체가 폐기됐을 가능성이 커지고 있다. 이 4곳의 레그(BICO·BEAT·BLESS의
OrangeX, ETH-USD·BTC-USD·LIT-USD·KAITO-USD의 dYdX, ETH/USD·BTC/USD의 GMX, GIGGLE의 XT.COM)는 모두
마지막 확인치를 이월했다. 대신 OKX는 공개 API(`market/ticker`+`public/open-interest`+
`public/funding-rate`)를 raw JSON 그대로 직접 조회해 신뢰도를 보완했다.

## 이번 회차 핵심

**BICO는 3회 연속 감속**했다 — OKX 직접 조회(raw JSON 확인, last 0.0168/open24h 0.01318)로
**+27.45%**, 직전(+45.15%)보다 크게 둔화됐고, funding도 -0.272%→**-0.193%**로 계속 완화돼 3회 연속
숏스퀴즈 압력이 누그러지는 추세를 재확인했다.

**1000RATS는 큰 폭으로 급감속**했다 — Binance +18.74%·Bybit +18.08%·Aster +17.69%(평균 **+18.17%**)로,
직전(+34.22%)에서 거의 반토막 수준으로 꺾였다. 웹서치로 **Aster가 8/1 1000RATS 전용 퍼프 마켓(최대
5x)을 신규 상장**했다는 사실을 확인 — 지난 2회차의 강한 재가속이 상장 기대감/직후 초기 열기였을
가능성이 크고, 이번 급감속은 전형적인 '상장 펌프 이후 식음' 패턴으로 해석된다.

**ALLO는 2회 연속 강화 이후 이번 회차 뚜렷이 감속**했다 — Binance+4.42%·Bybit+4.35%·OKX+4.53%(평균
**+4.43%**, 직전 +7.22%)로 꺾였다 — 모멘텀 소진 신호로 추정, 반전 촉매는 확인되지 않았다.

**BEAT는 3회 연속 낙폭 축소**를 이어갔다 — OKX -9.43%·Aster -9.00%(평균 **-9.21%**, 직전 -16.4%대)로
회복이 계속되며 거의 반토막 수준까지 낙폭이 줄었다 — 8/1 Astarter 파트너십 이후 회복 국면이 안정적으로
지속되는 모습이다.

**KAITO는 CEX·DEX 두 레그 모두 뚜렷이 개선**됐다 — OKX -12.58%→**-9.58%**, HL -13.21%→**-9.34%**로
여러 회차 지속된 오실레이션에서 벗어나 완연한 회복 추세로 전환되는 조짐을 보였다.

**⚠️ BLESS는 Aster 레그에서 급격히 마이너스로 반전**했다 — 직전 회차 냉각 완결(+0.14%, 완전 flat)에서
이번엔 **-28.00%**로 급락했다. 다만 웹서치에서는 정반대로 'BLESS가 24h +98% 급등'했다는 기사(HOKANEWS,
8/3 기준)를 확인해 **우리 Aster 레그 수치와 정면으로 상충**한다 — 거래소별 유동성 차이·가격 발견 지연
또는 기사 자체가 다른 시간창/거래소 기준일 가능성이 있어 신중히 다루며, 이 괴리를 명확히 표기한다
(OrangeX 레그는 이번에도 404로 비교 불가). BLESS 관련 별도로 8/19 마감 'Bless Airdrop(TIME 토큰)'
캠페인 소식과 MGBX의 BLESS/USDT 현물 상장폐지(7/10 발효, 저유동성 사유)도 확인했다.

**CASHCAT은 3회 연속 재가속하며 두 레그가 거의 수렴**했다 — HL +47.65%·Aster +48.48%(평균 **+48.07%**,
직전 +38.81%)로 계속 확대됐다. 웹서치로 이번엔 명확한 촉매를 확인했다 — **바이낸스가 CASHCAT
무기한선물(10x)을 신규 상장**했고 **Hyperliquid도 커뮤니티 요청으로 상장**했다는 사실, 그리고 HL 상장
직후 퍼프 가격이 몇 분 만에 60%+ 급락(스팟은 거의 무변동)했다가 되돌려진 극단적 변동성 이벤트가 있었음을
확인했다 — 지난 회차 불확실했던 'Crypto.com 상장' 추정은 오답이었고 실제 촉매는 바이낸스·HL 동시
상장이었던 것으로 정정한다. Robinhood Chain의 프리런칭 내부 코드네임에서 유래한 밈코인이라는 배경도
재확인됐다.

**BTW는 2회 연속 급가속 이후 뚜렷이 감속**했다 — Aster +38.04%→**+21.32%**로 꺾였고 OI도
$7.78M→**$6.94M**로 함께 줄어 포지션 청산이 진행 중임을 시사, 구체적 촉매는 이번 회차도 확인되지
않았다.

## 이번 회차 요약

①**AKE는 CEX 레그가 이번 회차 재포착**됐다 — Binance **-2.94%**로 확인, DEX(Aster **-3.57%**)와 함께
마이너스로 수렴 — 지난 회차 DEX 단독 플러스 반전(+2.02%)이 다시 뒤집힌 오실레이션.

②**BANK는 이번 회차 처음 CEX 레그가 확인**됐다(Binance -7.79%·Bybit -9.16%, 평균 **-8.47%**) —
DEX(Aster **-8.12%**)와 거의 수렴, 직전 DEX 단독 -14.44%보다 뚜렷이 개선된 수준.

③**신규로 ATOM**(Binance+7.91%·Bybit+7.85%·Aster+8.26%·HL+7.81%)**과 ALGO**(Binance+8.24%·
Bybit+8.28%·Aster+9.98%·HL+8.46%)가 4개 소스에서 일관되게 포착됐다 — 개별 촉매는 확인되지 않았고
(웹서치에서는 오히려 ATOM이 연중최저 근접·-2.28%라는 상반된 서술도 발견돼 시점 불일치 가능성 있어
직접조회 수치를 우선 신뢰), 광범위 알트 강세 동반으로 추정된다.

④ADA(4소스 평균 +3.03%, 직전 +1.87%에서 소폭 강화)·AAVE(4소스 평균 +0.65%, 직전 +1.36%와 유사)·
ASTER(CEX, Binance/Bybit 평균 -0.26%, 근접 flat 지속)·MMT(-4.76%→**-3.58%**, 완만한 개선 지속)·
AEON(-1.31%→**-3.51%**, 다시 마이너스 심화)·APR(-3.50%→**-4.38%**, 유사).

⑤CORE(+13.58%→**+8.30%**, 초기 팝 이후 감속 2회차)·BULLA(+8.71%→**+7.67%**, 소폭 둔화)·
CAP(-6.00%→**-8.73%**, 소폭 악화)·HYPE(+4.39%→**+4.13%**, 유사 유지)·FARTCOIN(+1.13%→**+1.42%**, 유사).

⑥**⚠️ HYPER-USD·APEX-USD(HL)는 이번 회차 top-40 거래량 리스트에서 포착되지 않아** 재확인하지 못하고
마지막 확인치를 이월했다.

## 시장 전반

- **총 시총 $2.27T(+0.44% 24h), BTC 도미넌스 56.46%, ETH 도미넌스 9.95% — 지난 회차 처음 관측된 리스크온 숨고르기가 이번 회차도 그대로 지속(플래토), 추가 재가속·냉각 없음. BTC(+0.76%)도 거의 동일 수준 유지.**
- **BICO 3회 연속 감속(+45.15%→+27.45%), funding도 계속 완화 — 숏스퀴즈 압력이 3회 연속 누그러짐.**
- **1000RATS·ALLO·BTW 등 이전 회차 급등 종목군이 이번 회차 일제히 감속·조정 — 8/1 Aster 신규상장(1000RATS) 등 상장 펌프 이후 식음 패턴이 다수 확인됨.**
- **반대로 CASHCAT은 3회 연속 재가속(바이낸스·HL 동시 퍼프 상장 촉매 확정), BEAT·KAITO는 3~회차째 회복세 지속 — 종목별 국면 분화가 뚜렷.**
- **⚠️ orangex·dydx_v4(2회 연속)·gmx·xt_derivatives(3회 연속) 4개 소스가 지속적으로 실패 — 단발성 아닌 구조적 이슈 가능성.**

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BICO (Biconomy)** [3회 연속 감속] | OKX(단일, OrangeX 2회 연속 404) | $130.89M | $2.70M | -0.193% | +27.45% | +45.15%→+27.45%, funding도 계속 완화(-0.272%→-0.193%) — 3회 연속 숏스퀴즈 압력 누그러짐 | deceleration-3rd-round-funding-continues-normalizing |
| **1000RATS** [큰 폭 급감속] | Binance/Bybit/Aster | $441.46M | $35.23M | +0.031% | +18.17% | +34.22%→+18.17%. Aster 8/1 1000RATS 전용 퍼프 신규상장 확인 — 상장 펌프 이후 식음으로 추정 | sharp-deceleration-listing-pump-fade-suspected |
| **ALLO (Allora)** [2회 강화 이후 감속] | Binance/Bybit/OKX | $149.36M | $21.63M | -0.009% | +4.43% | +7.22%→+4.43%로 꺾임. 반전 촉매 미확인 | decelerates-after-2round-strengthening |
| **BEAT (Audiera)** [3회 연속 낙폭 축소] | OKX(직접API)/Aster | $266.68M | $9.06M | +0.0022% | -9.21% | -16.4%대→-9.21%. 8/1 Astarter 파트너십 이후 회복 안정적 지속 | decline-narrows-3rd-round-recovery-stabilizing |
| **KAITO (CEX)** [오실레이션 이탈, 완연 회복] | OKX(직접API) | $102.49M | $8.06M | -0.001% | -9.58% | -12.58%→-9.58%, HL(-9.34%)도 동시 뚜렷 개선 — 오실레이션 이탈 조짐 | clear-recovery-both-legs-breaks-oscillation |
| **BANK** [CEX 레그 첫 확인] | Binance/Bybit(신규) | $171.05M | $24.25M | -0.0285% | -8.47% | 이번 회차 처음 CEX 레그 확인, DEX(-8.12%)와 수렴 — 직전 DEX 단독 -14.44%보다 뚜렷이 개선 | cex-leg-newly-confirmed-converges-with-dex |
| **AKE** [CEX 재포착, 마이너스 수렴] | Binance(재포착) | $134.36M | $30.75M | +0.031% | -2.94% | DEX(Aster -3.57%)와 함께 마이너스로 수렴 — 지난 회차 DEX 단독 플러스 반전이 재반전 | cex-leg-recaptured-flips-negative-with-dex |
| **ATOM** [신규 레이더 포착] | Binance/Bybit | $31.50M | $32.81M | -0.0115% | +7.88% | 4개 소스(Binance/Bybit/Aster/HL) 모두 +7.8~8.3% 일관, 촉매 미확인 | new-radar-pickup-4source-consistent-no-catalyst |
| **ALGO** [신규 레이더 포착] | Binance/Bybit | $36.08M | $16.47M | +0.0085% | +8.26% | 4개 소스 모두 +8.2~10% 일관, 촉매 미확인 | new-radar-pickup-4source-consistent-no-catalyst |
| MMT (Momentum) [완만한 개선 지속] | OKX(직접API) | $19.22M | $3.16M | -0.0216% | -3.58% | -4.76%→-3.58%로 낙폭 계속 축소 | plateau-mild-improvement-continues |
| AEON [다시 마이너스 심화] | OKX(직접API) | $13.46M | $2.02M | -0.0317% | -3.51% | -1.31%→-3.51%로 재차 악화, 저활동 오실레이션 지속 | reflips-negative-deepens-oscillation-continues |
| APR (aPriori) [유사 지속] | OKX(직접API) | $1.87M | $1.05M | +0.0172% | -4.38% | -3.50%→-4.38%로 큰 변화 없음 | similar-continues |
| CORE [초기 팝 이후 감속 2회차] | OKX(직접API) | $16.22M | $1.37M | -0.0255% | +8.30% | +13.58%→+8.30%로 둔화, 촉매 여전히 미확인 | decelerates-2nd-round-since-pickup |
| ADA [시장과 소폭 강화] | Binance/Bybit | $370.44M | $191.69M | +0.01% | +3.04% | +1.87%→+3.04%, 리스크온 소폭 재개와 궤 같이함 | firms-slightly-with-market |
| AAVE [유사 지속] | Binance/Bybit | $86.71M | $93.32M | -0.0015% | +0.69% | +1.07%→+0.69%, 큰 변화 없음 | similar-continues |
| ASTER (CEX) [근접 flat] | Binance/Bybit | $12.05M | $113.31M | -0.0005% | -0.26% | -0.01%→-0.26%, OI $113.3M 유지 | near-flat-continues |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM)

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| BLESS-USDT-PERPETUAL [⚠️ 2회 연속 조회 실패] | OrangeX | $294.86M(이월) | $102.36M(이월) | -0.073%(이월) | +12.00%(이월) | `orangex` 404 지속 — 구조적 이슈 가능성 | fetch-failed-404-2nd-round-carried-forward |
| **BLESS-USDT** [⚠️ 급락 반전, 웹서치와 상충] | Aster | $3.01M | $0.26M | +0.026% | -28.00% | +0.14%(flat)→-28.00% 급락. 웹서치 'BLESS +98%' 기사와 정면 상충, 신중히 다룸 | sharp-negative-reversal-conflicts-with-websearch |
| **CASHCAT** [3회 연속 재가속, 촉매 확정] | Hyperliquid/Aster | $11.31M | $10.50M | -0.0145% | +48.07% | +38.81%→+48.07%(HL+47.65%·Aster+48.48%). 바이낸스·HL 동시 퍼프 신규상장 촉매 확정, HL 상장 직후 60%+ 급락 후 되돌림 이벤트 확인 | sharp-reacceleration-3rd-round-catalyst-confirmed-binance-hl-listings |
| **BTW** [2회 급가속 이후 감속] | Aster | $0.65M | $6.94M | +0.019% | +21.32% | +38.04%→+21.32%, OI도 $7.78M→$6.94M 감소 — 청산 진행 시사 | decelerates-sharply-after-2round-acceleration-oi-falling |
| BULLA [소폭 둔화 지속] | Aster | $1.26M | $7.38M | +0.009% | +7.67% | +8.71%→+7.67%로 계속 완만히 둔화 | eases-slightly-continues |
| **AKE-USDT** [CEX와 마이너스 재반전] | Aster | $1.56M | $12.05M | +0.014% | -3.57% | +2.02%→-3.57%, CEX(-2.94%)와 함께 마이너스로 수렴 | reflips-negative-with-cex |
| **BANK-USDT** [CEX와 수렴] | Aster | $0.83M | $0.36M | -0.008% | -8.12% | -14.44%→-8.12%, 신규 확인된 CEX 레그(-8.47%)와 거의 일치 | converges-with-newly-confirmed-cex |
| CAP-USDT [소폭 악화] | Aster | $0.02M | $0.03M | +0.001% | -8.73% | -6.00%→-8.73%로 낙폭 다시 확대 | worsens-slightly |
| ASTER-USDT [근접 flat 재확인] | Aster | $7.81M | $219.20M | +0.004% | -0.41% | CEX와 함께 근접 flat 재확인 | near-flat-continues |
| ATOM-USD [신규 레이더 포착] | Aster/Hyperliquid | $0.90M | $3.79M | +0.0045% | +8.04% | CEX(+7.88%)와 함께 신규 포착, 촉매 미확인 | new-radar-pickup-4source-consistent-no-catalyst |
| ALGO-USD [신규 레이더 포착] | Aster/Hyperliquid | $2.43M | $3.01M | -0.0005% | +9.22% | CEX(+8.26%)와 함께 신규 포착, 촉매 미확인 | new-radar-pickup-4source-consistent-no-catalyst |
| HYPE-USD [유사 수준 유지] | Hyperliquid | $228.94M | $1,233.41M | +0.001% | +4.13% | +4.39%→+4.13%, OI $1,233.4M 유지 | similar-continues |
| HYPER-USD [⚠️ 미포착, 이월] | Hyperliquid | $0.59M(이월) | $0.37M(이월) | -0.012%(이월) | -6.43%(이월) | top-40 리스트에서 미포착, 재확인 실패 | not-recaptured-this-round-carried-forward |
| KAITO-USD [오실레이션 이탈, 완연 회복] | Hyperliquid | $16.68M | $24.09M | +0.001% | -9.34% | -13.21%→-9.34%, OKX(-9.58%)도 동시 개선 | clear-recovery-both-legs-breaks-oscillation |
| APEX-USD [⚠️ 미포착, 이월] | Hyperliquid | $0.07M(이월) | $0.80M(이월) | +0.001%(이월) | +1.29%(이월) | top-40 리스트에서 미포착, 재확인 실패 | not-recaptured-this-round-carried-forward |
| FARTCOIN [유사 수준 유지] | Hyperliquid | $6.22M | $21.17M | +0.007% | +1.42% | +1.13%→+1.42%, 큰 변화 없음 | similar-continues |
| ADA-USD [CEX와 소폭 강화] | Hyperliquid | $10.38M | $32.02M | 0.0% | +2.90% | +1.87%→+2.90%, CEX ADA(+3.04%)와 유사 수준 | firms-slightly-with-cex |
| AAVE-USD [CEX와 유사] | Hyperliquid | $6.30M | $66.40M | +0.001% | +0.55% | +1.36%→+0.55%, CEX AAVE(+0.69%)와 유사 | similar-matches-cex |
| ETH-USD [⚠️ 2회 연속 조회 실패] | dYdX | $12.62M(이월) | $19.41M(이월) | -0.010%(이월) | +0.25%(이월) | `dydx_v4` 404 지속 — 구조적 이슈 가능성 | fetch-failed-404-2nd-round-carried-forward |
| BTC-USD [⚠️ 2회 연속 조회 실패] | dYdX | $7.31M(이월) | $17.47M(이월) | +0.001%(이월) | +1.06%(이월) | ETH-USD와 동일 현상 | fetch-failed-404-2nd-round-carried-forward |
| **LIT-USD (dYdX)** [⚠️ 재동결 이월, 4회 연속 재확인 불가] | dYdX | $14.31(이월) | $14,718.01(이월) | 0.0%(이월) | +1.14%(이월) | dydx_v4 404로 재확인 자체 불가, 4회 연속 동일값 이력 유지 | refreeze-status-carried-api-fetch-failed |
| KAITO-USD (dYdX) [⚠️ 2회 연속 조회 실패] | dYdX | $488.35(이월) | $0.0(이월) | 0.0%(이월) | 0.0%(이월) | dydx_v4 404로 재확인 불가 | fetch-failed-404-2nd-round-carried-forward |
| ETH/USD (WETH-USDC) [⚠️ 3회 연속 조회 실패] | GMX | $23.40M(이월) | $16.14M(이월) | +0.001%(이월) | +2.21%(이월) | 404/429 재차 실패 — 지속 이슈로 판단 | fetch-failed-3rd-round-carried-forward |
| BTC/USD (BTC-USDC) [⚠️ 3회 연속 조회 실패] | GMX | $7.52M(이월) | $33.60M(이월) | +0.002%(이월) | +1.23%(이월) | ETH/USD와 동일 현상 | fetch-failed-3rd-round-carried-forward |
| GIGGLE (Giggle Fund) [⚠️ 3회 연속 조회 실패] | XT.COM | $34.11M(이월) | $224.34M(이월) | +0.5%(이월) | +6.12%(이월) | 429로 재차 실패 — 지속 이슈로 판단 | fetch-failed-3rd-round-carried-forward |

## 테마 태그

1. **BICO, 3회 연속 감속(+45.15%→+27.45%) — funding도 -0.27%→-0.19%로 계속 완화(숏스퀴즈 압력 3회 연속 누그러짐)** (deceleration-3rd-round-funding-continues-normalizing).
2. **1000RATS, 큰 폭 급감속(+34.22%→+18.17%) — Aster 8/1 신규상장 확인, 상장 펌프 이후 식음 패턴으로 추정** (sharp-deceleration-listing-pump-fade-suspected).
3. **ALLO, 2회 연속 강화 이후 뚜렷이 감속(+7.22%→+4.43%)** (decelerates-after-2round-strengthening).
4. **BEAT, 3회 연속 낙폭 축소(-16.4%→-9.21%) — Astarter 파트너십 이후 회복 안정적 지속** (decline-narrows-3rd-round-recovery-stabilizing).
5. **KAITO, CEX·DEX 두 레그 모두 뚜렷이 개선 — 오실레이션에서 벗어나는 조짐** (clear-recovery-both-legs-breaks-oscillation).
6. **⚠️ BLESS, Aster 레그가 급격히 마이너스로 반전(+0.14%→-28.00%) — 웹서치 'BLESS +98%' 기사와 정면 상충, 신중히 다룸** (sharp-negative-reversal-conflicts-with-websearch).
7. **CASHCAT, 3회 연속 재가속(+38.81%→+48.07%) — 바이낸스·HL 동시 퍼프 상장 촉매 확정** (sharp-reacceleration-3rd-round-catalyst-confirmed-binance-hl-listings).
8. **BTW, 2회 연속 급가속 이후 뚜렷이 감속(+38.04%→+21.32%), OI도 함께 감소** (decelerates-sharply-after-2round-acceleration-oi-falling).
9. **AKE, CEX 레그 재포착돼 DEX와 함께 마이너스로 재반전** (reflips-negative-with-cex).
10. **BANK, 이번 회차 처음 CEX 레그 확인(-8.47%) — DEX와 수렴, 직전 대비 뚜렷이 개선** (cex-leg-newly-confirmed-converges-with-dex).
11. **ATOM·ALGO, 신규 레이더 포착 — 4개 소스 모두 일관된 +7.8~10%, 개별 촉매 미확인, 광범위 알트 강세 동반 추정** (new-radar-pickup-4source-consistent-no-catalyst).
12. **⚠️ 시장 전반: 총 시총 $2.27T(+0.44%), BTC 도미넌스 56.46% — 지난 회차 숨고르기가 이번 회차도 그대로 플래토 지속** (market-momentum-plateau-continues).
13. **⚠️ 데이터 신뢰도 이슈 지속: orangex·dydx_v4는 2회 연속, gmx·xt_derivatives는 3회 연속 404/429 — 구조적 이슈로 판단, 4개 소스 모두 이월값 사용** (persistent-multi-source-failures-carried-forward).
14. **웹서치 정정: 1000RATS 실제 촉매는 Aster 8/1 신규상장, CASHCAT 촉매는 바이낸스·HL 동시 퍼프 상장으로 확정(지난 회차 'Crypto.com 상장' 추정 오답 정정)** (websearch-catalyst-corrections).

## 데이터 신뢰도

**이번 회차도 데이터 소스 이상이 지속됐고, 오히려 지속화 조짐이 뚜렷해졌다.** (a) **OrangeX**
(`orangex`)와 **dYdX**(`dydx_v4`)는 이번 회차도 404 Not Found로 응답해 **2회 연속** 실패했다 — 직전
회차엔 '일시적 문제'로 판단했으나, 2회 연속되며 CoinGecko 측 지속적 문제이거나 거래소 ID 자체가
변경/폐기됐을 가능성이 더 커졌다. (b) **GMX**(ETH/USD·BTC/USD)와 **XT.COM**(`xt_derivatives`,
GIGGLE)은 **3회 연속** 실패(404/429)로, 이 역시 구조적 이슈로 판단을 전환한다. 다음 회차에도 실패가
이어지면 이 4개 소스는 당분간 이월 전용으로 취급하고 회차마다 재시도만 하는 방식으로 전환을 검토할
필요가 있다. (c) 대신 **OKX 공개 API를 raw JSON 그대로 직접 조회**해(예: BICO·CORE·KAITO에서
`vol24h`와 `volCcy24h`가 동일 값으로 나오는 특이 케이스를 raw JSON 확인으로 검증 — ctVal=1 계약 구조로
인한 정상적 현상임을 확인) 신뢰도를 보완했다. 계산은 기존과 동일하게 `volCcy24h(기초자산 단위) ×
last가격` 방식으로 USD 환산했으며, BEAT·MMT·AEON·APR·CORE 등에서 직전 회차 수치와의 연속성으로 방법론
정합성을 재확인했다.

**⚠️ 웹서치 대조에서 새로운 상충 사례가 발견됐다.** BLESS의 Aster 레그가 -28.00%로 급락한 것으로
확인됐으나, 같은 시점(8/3) 기사(HOKANEWS)는 정반대로 'BLESS +98% 급등'을 보도했다 — 두 수치가 정면
상충하며, 원인은 거래소별 유동성 차이·가격 발견 지연이거나 기사 자체가 다른 시간창/거래소 기준일
가능성이 있다. 이 괴리는 해소하지 못했고, 두 수치 모두 정직하게 병기해 신중히 다룬다. 반대로 ATOM 관련
웹서치에서도 우리 직접조회(+7.9%)와 상반된 서술(연중최저 근접·-2.28%)이 나온 기사를 발견했는데, 해당
기사는 가격예측형 SEO 콘텐츠로 신뢰도가 낮다고 판단해 직접조회 수치를 우선시했다.

**웹서치로 촉매를 명확히 확정한 사례**: CASHCAT은 바이낸스(10x 무기한선물)·Hyperliquid(커뮤니티 요청)
동시 신규 상장이 확인됐고, HL 상장 직후 60%+ 급락 후 되돌림이라는 극단적 변동성 이벤트도 확인됐다.
1000RATS는 Aster의 8/1 전용 퍼프 신규상장이 확인돼, 지난 2회차 재가속의 실제 배경으로 추정된다.

**OKX 데이터 소스 방법론**: BICO·BEAT는 CoinGecko `okex_swap` 및 OKX 공개 API 병행, MMT·KAITO(CEX)·
AEON·APR·CORE·ALLO는 OKX 공개 API(`market/ticker`+`public/open-interest`+`public/funding-rate`)를
raw JSON으로 직접 조회해 `volCcy24h × last` 방식으로 USD 거래량·OI를 역산했다(기존 방법론과 동일하게
유지, 이번 회차 raw JSON 확인으로 재검증).

**funding 값 단위 관련 주의**: CEX·DEX 종목의 funding 값은 각 API가 반환한 원시 수치를 그대로 percent
스케일로 사용했다. 거래소·필드별로 스케일 표기 관례가 다를 수 있어 **회차 간 funding 절대값 비교는
참고용으로만** 활용하고, 방향(양전/음전)과 가격·거래량 추세를 우선 신뢰할 것을 권한다.

한계: (a) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며, 이번
회차 새롭게 발견된 대형 신규 급등 종목은 ATOM·ALGO 2건이다(전체 시장을 포괄하는 완전한 스캔은 아님);
(b) HYPER-USD·APEX-USD(HL)는 이번 회차 top-40 거래량 리스트에서 재확인되지 않아 이월했다 — 거래량이
기준선 아래로 내려갔거나 스캔 범위에서 누락됐을 가능성을 구분하지 못한다; (c) OrangeX·dYdX·GMX·
XT.COM은 위에서 설명한 대로 이번 회차도 미해결이며, 2~3회 연속 실패로 구조적 이슈 가능성이 커졌다;
(d) BLESS의 Aster-웹서치 수치 상충은 해소하지 못한 채 병기했다; (e) **주식화·상품·레버리지 ETF 토큰**은
이번 회차도 규약에 따라 cex/dex 리스트에서 전부 제외했다(OKX top-25 변동률 리스트에서 SNDK·KIOXIA·
MSFT·RKLB 등 다수의 토큰화 주식이 상위를 차지하는 것을 확인했으나 전부 제외 처리).

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
