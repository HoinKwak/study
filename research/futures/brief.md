# 선물시장 스카우트 브리핑 — 2026-08-09 14:29 UTC (KST 2026-08-09 23:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-09T12:27:00Z)
> 로부터 약 2시간2분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 이번 회차도 확보 성공 — 총시총 **$2,306,712,881,096.77(약 $2.307T)**·
BTC도미넌스 **56.67%**로 직전 회차($2.299T·56.65%)보다 소폭 상승, **4회 연속** 안정적으로
확보됐다.

### Fear&Greed 31(Fear) — 8회차 연속 동일값

alternative.me API 정상 응답, **31(Fear)** — 8회차 연속 동일값 유지.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM에 더해 이번엔 BEAT·BICO·ACE도 개별조회)는
**25회차 연속** 방법론(`oiUsd` 필드 직접 사용, `vol24_usd=volCcy24h×last`,
`chg24=(last-open24h)/open24h`)을 유지했다.

지금은 **일요일 밤에서 월요일로 넘어가는 시각**(UTC 14:29, KST 8/9 23:29)이다.

## 이번 회차 최대 사건

### ⚠️⚠️⚠️ ACE — 언락(8/10) 코앞, 4·5개 전 거래소 완전 반전

여러 회차 추적해온 8/10 언락을 목전에 두고, 직전 회차까지 4회차 연속 냉각하며 손익분기 근처까지
내려왔던 chg24가 이번 회차 **4개 CEX·1개 DEX 전부 마이너스로 완전히 뒤집혔다**: Binance
**-4.778%**, Bybit **-4.699%**(가중 **-4.759%**), OrangeX **-4.671%**, Aster **-5.299%**,
Hyperliquid **-2.592%**. tokenomist.ai를 WebFetch로 재확인해 '8/10에 Early Investors 배분으로
언락 예정'이 다시 확인됐고(정확한 수량·시각은 여전히 명시 안 됨, 별도 WebSearch로 확보한 1.8M
ACE·공급 1.2% 수치와 일치), 이번 반전은 언락을 앞둔 전형적 **sell-the-news 선반영**으로 보이나
확정할 근거는 아니다. 흥미롭게도 Binance/Bybit 가중 펀딩은 직전 -0.001%에서 이번 **+0.001%**로
미세하게 플러스 전환해 가격과 다소 엇갈리는 신호를 보였다. 여러 회차에 걸쳐 추적해온 최대
이벤트가 마침내 언락 직전에 결말을 맞은 모습이다.

### ⚠️⚠️ BICO — 부분 반등 붕괴, 급락 재개

직전 회차의 '부분 반등'이 단 한 회차 만에 다시 꺾여 급락이 재개됐다 — OKX 직접조회
**-26.344%**(직전 -14.838%보다 더 악화, 2회차 전 -21.484%보다도 나쁨), Aster
**-21.243%**(직전 -13.27%), OrangeX **-7.804%**(직전 -15.68%에서는 완화). ⚠️ CoinGecko의
okex_swap 배열 요약에서는 BICO chg24가 **-0.47%**로 나와 OKX 직접조회·Aster·OrangeX 세 소스
모두와 크게 어긋나 이상치로 판단, 이번 회차는 OKX 직접조회값을 채택했다(향후 재확인 필요).
OI는 OKX $10.23M→**$8.13M(-20.5%)**로 뚜렷이 감소해 디레버리징이 재차 진행 중임을 시사한다.

## 직전 회차 강조 종목 추적 결과

- **① BEAT — ⚠️ 신뢰도 문제 대부분 해소.** OKX 직접조회 chg24 약 **+20.73%**(last
  3.2393/open24h 2.683), CoinGecko okex_swap **+20.221%**, Aster **+20.31%**로 세 소스가
  20~21%대로 수렴했다(직전 24~28%대에서 냉각). Binance/Bybit는 이번 회차 두 소스 모두
  명확히 '미확인'(엇갈린 값이 아니라 단순 미상장)으로 나와 직전 회차의 혼란스러운 이중조회
  문제가 재현되지 않았다.
- **② ACE — ⚠️⚠️⚠️ 언락 코앞, 완전 반전.** 위 '이번 회차 최대 사건' 참조.
- **③ CASHCAT — 온체인 재가속과 일치.** 직후 온체인 회차(14:06Z)에서 보고된 6연속
  유동성감소 종료·전지표 재양전을 선물에서도 확인 — HL **+13.27%→+26.931%**, Aster
  **+13.925%→+27.077%**, OrangeX **+14.81%→+26.386%**로 3거래소 전부 20%대 후반으로
  강하게 재가속해 온체인·선물 신호가 일치했다.
- **④ BANK — 급반전 피크 이후 냉각, 견조 유지.** Binance/Bybit 가중 **+12.807%→+8.112%**,
  OrangeX **+13.74%→+9.361%**(펀딩 -0.059%→-0.155%로 더 음전환), Aster
  **+13.057%→+8.167%**. 3거래소 모두 플러스권을 견조하게 유지했다. 8/17 언락 약 8일 앞.
- **⑤ BICO — ⚠️⚠️ 부분 반등 붕괴.** 위 '이번 회차 최대 사건' 참조.
- **⑥ KAITO — ⚠️ 5회차 연속 개선 흐름 종료.** OKX 직접조회 chg24 **-0.884%→-2.838%**(HL도
  -1.246%→-3.183%로 동조 악화), 펀딩은 -0.523%→**-0.528%**로 거의 유지. 8/20 대형 언락 약
  11일 앞.

## 기타 주요 변화

**MMT**는 여러 회차 이어지던 '마이너스권 유지' 패턴을 깨고 처음으로 플러스 전환했다
(**-4.189%→+0.963%**). **BTW**는 직전까지 3회차 연속 이어지던 냉각 추세가 이번 회차 뒤집혀
강하게 재가속했다(Aster **+7.899%→+16.509%**로 거의 2배). **BLESS**는 2회차 정체 이후 회복이
아예 꺾여 재악화가 심화됐다(OrangeX -7.19%→**-10.433%**, Aster -5.766%→**-10.414%**로 두
거래소 모두 두 자릿수 마이너스로 악화). **AKE·AIO·ASTER**는 각각 재차 마이너스로 돌아서는
휩소를 보였다(AKE +1.253%→**-1.576%**, AIO +1.971%→**-4.388%**, ASTER
+0.289%→**-1.096%**). **AEON**은 '냉각 추세 멈춤' 관찰이 이번 회차 다시 깨져
+7.329%→**+2.74%**로 급냉각했다.

## 데이터 이슈 추적 결과

⚠️ **HYNA:HYPE-USD의 OI가 $684,897.67→$684,760.57로 미세 변동해 정상 갱신이 3회차 연속
확인됐다** — 프리징 해제 확정에 근접하고 있다. GIGGLE의 필드 순서역전(vol24h>volCcy24h)이
**10회차 연속**, KAITO(OKX 직접)의 vol24h=volCcy24h 완전동일값이 **10회차 연속**, GRAM의
완전동일값이 **8회차 연속** 재현됐다 — 세 이상치 모두 여전히 견고하다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️⚠️ 언락 코앞, 완전 반전] | Binance/Bybit(가중) | $234.47M | $12.80M | +0.001% | -4.759% | +4.695%→-4.759%, 4개CEX·1개DEX 전부 마이너스. tokenomist 재확인: 8/10 언락. sell-the-news 가능성(미확정) | sharp-reversal-to-negative-all-venues-unlock-imminent |
| **BICO** [⚠️⚠️ 부분반등 붕괴] | OKX(직접API) | $412.80M | $8.13M | +0.010% | -26.344% | -14.838%→-26.344%, OI -20.5%. CoinGecko okex_swap 요약(-0.47%)은 이상치로 미채택 | partial-rebound-collapses-again-worse-than-two-rounds-ago |
| **BEAT** [⚠️ 신뢰도 해소, 3소스 수렴] | OKX(CoinGecko정상) | $383.04M | $12.67M | +0.005% | +20.221% | 20~21%대로 3소스 수렴(직전 24~28%대). Binance/Bybit 명확히 미상장 | reliability-resolved-three-sources-converge-cools-to-20pct |
| **MMT** [⚠️ 첫 플러스 전환] | OKX(직접API) | $110.04M | $4.15M | -0.003% | +0.963% | -4.189%→+0.963%, 여러 회차 마이너스권 유지 패턴 종료 | first-positive-turn-breaks-negative-streak |
| **BSB** [소폭 개선] | OKX(CoinGecko정상) | $8.04M | $2.80M | +0.005% | -3.030% | -3.694%→-3.030% | stays-negative-mild-improvement |
| AAVE [소폭 냉각] | Binance/Bybit(가중) | $41.24M | $90.68M | +0.005% | +0.400% | +0.932%→+0.400% | mild-cooling |
| ALLO [휩소 심화] | Binance/Bybit(가중) | $26.64M | $19.02M | +0.005% | -4.368% | -1.832%→-4.368% | whipsaw-deepens-negative |
| ADA [9회차 마이너스, 개선] | Binance/Bybit(가중, USDT만) | $121.45M | $172.21M | +0.004% | -1.478% | -1.620%→-1.478% | ninth-round-negative-mild-improvement |
| BANK [급반전 피크 냉각, 견조] | Binance/Bybit(가중) | $112.48M | $19.42M | +0.005% | +8.112% | +12.807%→+8.112%. 8/17 언락 약 8일 앞 | cools-from-reversal-peak-holds-solidly-positive |
| AKE [재차 마이너스] | Binance/Bybit(가중) | $35.59M | $38.62M | +0.042% | -1.576% | +1.253%→-1.576%. 8/21 언락 약 12일 앞 | turns-negative-again-whipsaw |
| KAITO [⚠️ 5회차 개선 종료] | OKX(직접API) | $134.14M | $7.89M | -0.528% | -2.838% | -0.884%→-2.838%, HL도 동조. 8/20 언락 약 11일 앞 | five-round-improvement-streak-ends-reverses |
| GIGGLE [급냉각, 플러스 겨우 유지] | OKX(직접API) | $29.88M | $2.76M | +0.005% | +0.407% | +5.152%→+0.407%. ⚠️ 필드 이상치 10회차 연속 | sharp-cooling-barely-holds-positive |
| PIPPIN [소폭 냉각] | OKX(직접API) | $2.08M | $1.84M | +0.019% | +1.327% | +2.027%→+1.327% | mild-cooling-stays-positive |
| 1000RATS [개선] | Binance/Bybit(가중) | $13.75M | $18.58M | +0.026% | -0.489% | -1.402%→-0.489% | stays-negative-improves |
| AIO [⚠️ 1회차 만에 재반전] | Binance/Bybit(가중) | $10.01M | $4.34M | +0.039% | -4.388% | +1.971%→-4.388% | reverses-negative-again-after-single-round |
| GRAM [거의 유지] | OKX(직접API) | $2.18M | $6.28M | +0.005% | -1.614% | -1.688%→-1.614%. ⚠️ 필드 이상치 8회차 연속 | holds-negative-vol-field-anomaly-eighth-round |
| AEON [⚠️ 급냉각 재개] | OKX(CoinGecko정상) | $34.36M | $4.08M | +0.005% | +2.740% | +7.329%→+2.74% | cooling-pause-ends-sharp-cooling-resumes |
| ATOM [3회차 마이너스, 개선] | Binance/Bybit(가중) | $7.88M | $28.38M | +0.004% | -0.347% | -1.416%→-0.347% | third-round-negative-improves |
| ASTER [재차 마이너스] | Binance/Bybit(가중) | $18.09M | $113.20M | +0.004% | -1.096% | +0.289%→-1.096% | reverses-negative-again |
| CORE [냉각] | OKX(CoinGecko정상) | $1.43M | $1.03M | +0.010% | +1.926% | +4.904%→+1.926% | low-liquidity-cools |
| CAP [거의 유지] | OKX(CoinGecko정상) | $19.78M | $2.36M | +0.005% | +4.098% | +3.812%→+4.098% | roughly-flat-mild-improvement |
| ALGO [소폭 악화] | Binance/Bybit(가중) | $7.06M | $14.75M | +0.005% | -1.243% | -0.892%→-1.243% | stays-negative-mild-worsening |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [⚠️⚠️⚠️ 완전 반전] | Hyperliquid | $4.92M | $1.51M | -0.009% | -2.592% | +4.593%→-2.592% | reverses-negative-aligns-with-cex |
| **ACE-USDT-PERPETUAL** [⚠️⚠️⚠️ 완전 반전] | OrangeX | $140.83M | $43.68M | +0.010% | -4.671% | +3.16%→-4.671% | reverses-negative-ahead-of-unlock |
| **ACE-USDT** [⚠️⚠️⚠️ 최대 낙폭] | Aster | $0.74M | $0.08M | +0.001% | -5.299% | +3.995%→-5.299% | reverses-negative-largest-drop |
| BEAT-USDT-PERPETUAL [수렴] | OrangeX | $18.44M | $6.97M | +0.010% | +20.458% | +27.12%→+20.458% | cools-converges-with-other-sources |
| BEAT [수렴] | Aster | $3.43M | $5.13M | +0.010% | +20.310% | +28.305%→+20.31% | cools-converges-with-other-sources |
| **BICO-USDT-PERPETUAL** [낙폭 완화] | OrangeX | $329.41M | $92.84M | +0.225% | -7.804% | -15.68%→-7.804%, 펀딩 급등 | drop-eases-but-continues-funding-spikes |
| **BICO-USDT** [⚠️⚠️ 급락 재개] | Aster | $3.55M | $0.29M | +0.001% | -21.243% | -13.27%→-21.243%, OI -19% | rebound-collapses-sharp-renewed-drop |
| **CASHCAT** [⚠️ 온체인과 일치, 강한 재가속] | Hyperliquid | $17.25M | $20.19M | +0.023% | +26.931% | +13.27%→+26.931% | strong-reacceleration-matches-onchain-signal |
| CASHCAT-USDT-PERPETUAL [강한 재가속] | OrangeX | $0.14M | $0.06M | +0.010% | +26.386% | +14.81%→+26.386% | strong-reacceleration-aligns |
| CASHCAT-USDT [최대치] | Aster | $1.75M | $1.37M | -0.013% | +27.077% | +13.925%→+27.077% | strong-reacceleration-highest-of-three |
| ALLO-USDT [휩소 심화] | Aster | $0.12M | $0.03M | +0.001% | -4.732% | -2.48%→-4.732% | whipsaw-deepens |
| ALLO-USDT-PERPETUAL [마이너스 유지] | OrangeX | $18.25M | $6.30M | +0.010% | -3.880% | -1.80%→-3.88% | stays-negative |
| AAVE-USDT-PERPETUAL [소폭 냉각] | OrangeX | $24.25M | $8.70M | +0.010% | +0.417% | +0.88%→+0.417% | mild-cooling |
| AAVE-USDT [소폭 냉각] | Aster | $0.12M | $4.59M | +0.010% | +0.296% | +0.74%→+0.296% | mild-cooling |
| AAVE-USD [소폭 냉각] | Hyperliquid | $2.31M | $60.43M | +0.001% | +0.240% | +0.865%→+0.24% | mild-cooling |
| ADA-USDT-PERPETUAL [거의 유지] | OrangeX | $66.80M | $24.63M | +0.010% | -1.450% | -1.51%→-1.45% | roughly-flat-negative |
| ADA-USDT [소폭 악화] | Aster | $0.14M | $1.51M | +0.010% | -1.595% | -1.459%→-1.595% | mild-worsening |
| ADA-USD [소폭 개선] | Hyperliquid | $1.62M | $32.90M | +0.001% | -1.675% | -2.056%→-1.675% | mild-improvement-stays-negative |
| BANK-USDT-PERPETUAL [냉각, 견조] | OrangeX | $7.26M | $2.75M | -0.155% | +9.361% | +13.74%→+9.361% | cools-from-reversal-holds-positive |
| BANK-USDT [냉각, 견조] | Aster | $0.50M | $0.40M | +0.001% | +8.167% | +13.057%→+8.167% | cools-from-reversal-holds-positive |
| AKE-USDT-PERPETUAL [재차 마이너스] | OrangeX | $6.68M | $2.33M | +0.019% | -1.314% | +1.41%→-1.314% | turns-negative-again |
| AKE-USDT [재차 마이너스] | Aster | $0.65M | $11.10M | +0.017% | -1.873% | +1.184%→-1.873% | turns-negative-again |
| CAP-USDT [거의 유지] | Aster | $0.04M | $0.11M | +0.001% | +3.036% | +3.196%→+3.036% | roughly-flat |
| CAP-USDT-PERPETUAL [거의 유지] | OrangeX | $0.49M | $0.17M | +0.010% | +3.475% | +4.19%→+3.475% | roughly-flat |
| ALGO-USDT-PERPETUAL [거의 유지] | OrangeX | $4.34M | $1.61M | +0.010% | -1.260% | -1.03%→-1.26% | roughly-flat |
| ALGO-USDT [초저유동성] | Aster | $0.002M | $0.03M | +0.001% | -1.315% | -1.738%→-1.315% | low-liquidity-roughly-flat |
| ALGO-USD [소폭 악화] | Hyperliquid | $0.52M | $2.04M | +0.001% | -1.362% | -1.06%→-1.362% | mild-worsening |
| ATOM-USDT-PERPETUAL [개선] | OrangeX | $4.40M | $1.42M | -0.010% | -0.433% | -1.37%→-0.433% | improves |
| ATOM-USDT [거의 유지] | Aster | $0.02M | $1.60M | +0.010% | -0.507% | -1.084%→-0.507% | mild-improvement |
| ATOM-USD [개선] | Hyperliquid | $0.17M | $1.92M | +0.001% | -0.504% | -1.634%→-0.504% | improves |
| ASTER-USDT-PERPETUAL [재차 마이너스] | OrangeX | $7.44M | $2.76M | +0.010% | -0.692% | +0.35%→-0.692% | turns-negative-again |
| ASTER-USDT [대형 OI 거의 유지] | Aster | $10.51M | $219.36M | +0.027% | -1.082% | OI $219.68M→$219.36M | large-oi-roughly-holds-turns-negative |
| ASTER-USD [재차 마이너스] | Hyperliquid | $0.61M | $14.25M | +0.001% | -0.928% | +0.322%→-0.928% | turns-negative-again |
| KAITO-USD [⚠️ 5회차 개선 종료] | Hyperliquid | $25.85M | $16.81M | -0.243% | -3.183% | -1.246%→-3.183%. 8/20 언락 약 11일 앞 | five-round-improvement-ends-aligns-with-okx |
| GRAM-USD [마이너스권, OKX와 일치] | Hyperliquid | $0.44M | $12.80M | +0.001% | -1.693% | -1.793%→-1.693% | holds-negative-matches-okx |
| HYPE-USD [손익분기 근접까지 개선] | Hyperliquid | $75.13M | $1,192.05M | +0.001% | -0.009% | -0.457%→-0.009% | improves-toward-breakeven |
| HYPER-USD [재가속] | Hyperliquid | $0.10M | $0.31M | +0.001% | +0.948% | +0.382%→+0.948% | reaccelerates |
| APEX-USD [소폭 냉각] | Hyperliquid | $0.08M | $0.78M | +0.001% | +0.531% | +1.233%→+0.531%, Bybit도 동조 냉각 | mild-cooling-bybit-also-cools |
| FARTCOIN [손익분기권에서 재가속] | Hyperliquid | $3.79M | $22.15M | +0.002% | +1.158% | +0.046%→+1.158% | reaccelerates-from-breakeven |
| ETHFI-USD [소폭 재가속] | Hyperliquid | $0.45M | $8.80M | +0.001% | +2.722% | +2.248%→+2.722% | mild-reacceleration |
| ETH-USD [플러스 재전환] | dYdX | $5.64M | $8.99M | 0.000% | +0.052% | -0.130%→+0.052% | turns-positive-again |
| BTC-USD [플러스 전환] | dYdX | $1.17M | $18.22M | 0.000% | +0.086% | -0.128%→+0.086% | turns-positive |
| SOL-USD [냉각, 플러스권 유지] | dYdX | $0.24M | $4.53M | 0.000% | +1.068% | +1.472%→+1.068% | holds-positive-cools |
| ANSEM [거의 유지] | Aster | $0.26M | $0.89M | +0.001% | -9.350% | -9.774%→-9.35% | holds-deeply-negative |
| ANSEM-USDT-PERPETUAL [거의 유지] | OrangeX | $0.46M | $0.15M | +0.010% | -9.286% | -8.73%→-9.286% | holds-deeply-negative-aligns-with-aster |
| **BTW** [⚠️ 3회차 냉각 종료, 강한 재가속] | Aster | $2.68M | $13.85M | +0.037% | +16.509% | +7.899%→+16.509%로 거의 2배 | three-round-cooling-ends-strong-reacceleration |
| HYNA:PUMP-USD [재가속] | Hyperliquid | $0.04M | $0.17M | +0.001% | +17.750% | +10.613%→+17.75% | reaccelerates |
| **HYNA:HYPE-USD** [⚠️ 정상화 3회차 연속] | Hyperliquid | $0.14M | $0.68M | +0.012% | -0.428% | OI $684,898→$684,761 미세변동 | oi-freeze-resolution-confirmed-third-round |
| AEON-USDT-PERPETUAL [급냉각] | OrangeX | $0.50M | $0.18M | +0.010% | +2.826% | +7.04%→+2.826% | sharp-cooling-aligns-with-okx |
| AEON-USDT [급냉각] | Aster | $0.11M | $0.23M | +0.008% | +3.052% | +7.662%→+3.052% | sharp-cooling |
| **BSB-USDT-PERPETUAL** [마이너스권 유지] | OrangeX | $15.18M | $4.91M | +0.010% | -3.716% | -3.37%→-3.716% | stays-negative |
| **BSB-USDT** [마이너스권 유지] | Aster | $0.09M | $0.10M | +0.001% | -3.473% | -2.514%→-3.473% | stays-negative |
| 1000RATS-USDT [재차 마이너스] | Aster | $0.10M | $0.04M | +0.015% | -0.688% | +0.912%→-0.688%, CEX와 방향 일치 | turns-negative-aligns-with-cex |
| **BLESS** [⚠️ 재악화 심화, 두 자릿수] | OrangeX | $103.13M | $32.52M | +0.057% | -10.433% | -7.19%→-10.433% | recovery-relapse-deepens-double-digit-negative |
| **BLESS-USDT** [⚠️ 재악화 심화] | Aster | $0.36M | $0.19M | +0.009% | -10.414% | -5.766%→-10.414% | recovery-relapse-deepens-matches-orangex |

## 테마 태그

1. **시장 전반: `/global`이 4회 연속 확보 성공 — 총시총 $2.307T·BTC도미넌스 56.67%(소폭 상승)** (global-api-fourth-consecutive-success).
2. **Fear&Greed 31(Fear) 8회차 연속 동일값 유지** (fear-greed-holds-31-eighth-consecutive-round).
3. **⚠️⚠️⚠️ ACE: 언락(8/10) 코앞에서 4·5개 전 거래소 완전 반전(+4.695%→-4.759% 가중). sell-the-news 선반영 가능성(미확정). 펀딩은 미세 플러스 전환** (ace-full-reversal-negative-all-venues-unlock-imminent).
4. **⚠️⚠️ BICO: 부분 반등이 1회차 만에 재붕괴(-26.344%, 2회차 전보다 악화), OI -20.5%. CoinGecko okex_swap 요약값(-0.47%)은 이상치로 미채택** (bico-rebound-collapses-okx-summary-anomaly).
5. **⚠️ BEAT: 신뢰도 문제 대부분 해소 — 3소스 20~21%대 수렴, Binance/Bybit 명확히 미상장 확인** (beat-reliability-resolved-converges-20pct).
6. **⚠️ KAITO: 5회차 연속 개선 흐름 종료, OKX·HL 동조 악화. 8/20 대형 언락 약 11일 앞** (kaito-five-round-streak-ends).
7. **⚠️ MMT: 여러 회차 마이너스권 유지 끝, 첫 플러스 전환** (mmt-first-positive-turn).
8. **⚠️ BTW: 3회차 연속 냉각 종료, 거의 2배 재가속** (btw-cooling-ends-strong-reacceleration).
9. **⚠️ BLESS: 회복 정체 이후 재악화 심화, 두 거래소 모두 두 자릿수 마이너스로 악화** (bless-relapse-deepens-double-digit).
10. **CASHCAT: 온체인 회차(14:06Z) 재가속 보고와 일치해 3거래소 전부 강한 재가속** (cashcat-onchain-futures-signal-alignment).
11. **BANK: 급반전 피크 이후 냉각됐으나 3거래소 모두 플러스권 견조 유지** (bank-cools-from-peak-holds-positive).
12. **AKE·AIO·ASTER: 각각 재차 마이너스 전환하는 휩소 재개** (ake-aio-aster-whipsaw-resumes).
13. **AEON: 냉각 추세 멈춤 관찰이 1회차 만에 재개돼 급냉각** (aeon-cooling-pause-ends).
14. **⚠️ HYNA:HYPE-USD: OI 정상 갱신 3회차 연속 확인 — 프리징 해제 확정에 근접** (hyna-hype-oi-normalization-third-round).
15. **⚠️ GIGGLE 필드 이상치 10회차 연속, KAITO(OKX 직접) 완전동일값 이상치 10회차 연속, GRAM도 8회차 연속 재현** (field-anomalies-tenth-eighth-round-continue).
16. **OKX ACE·BANK·1000RATS·AIO·KAITO·MMT·PIPPIN·GIGGLE·GRAM·CASHCAT·BLESS·BTW는 이번 회차도 okex_swap 미등재(ACE는 instId 자체 부재), 직접 API/DEX로 보강. BEAT·BICO·AEON·BSB·CAP·CORE는 okex_swap 정상** (okx-most-still-not-listed-direct-api-supplements).
17. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
18. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
19. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
20. **지금은 일요일 밤에서 월요일로 넘어가는 시각(UTC 14:29)** (sunday-to-monday-timing-caveat).

## 데이터 신뢰도

**CoinGecko binance_futures**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS
확인. **BEAT·BICO·BSB·APEX·BTW·KAITO·CASHCAT는 이번 회차 명확히 '미확인'**(엇갈린 값이 아닌
단순 미상장)으로 나와 직전 회차 BEAT의 이중조회 혼란이 재현되지 않았다.

**CoinGecko bybit**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS·APEX 확인.
BEAT·BICO는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·CAP·**BEAT·BICO**
확인(이번 회차 정상 응답, 다만 **BICO의 chg24 값 -0.47%는 OKX 직접조회·Aster·OrangeX 세 소스와
크게 괴리해 이상치로 판단, 미채택**). ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·
BLESS·CASHCAT은 이번 회차도 okex_swap 배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM·BEAT·BICO)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인.
`oiUsd` 필드 직접 사용 방법론을 **25회차 연속** 유지, vol24_usd=`volCcy24h`×`last` 계산 방식·
chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️ **ACE-USDT-SWAP는 OKX에 instId 자체가
존재하지 않음**을 직접 확인(`"Instrument ID doesn't exist"`), okex_swap 미등재가 CoinGecko
집계 지연이 아니라 실제 미상장임이 재확인됐다. **GIGGLE**은 vol24h/volCcy24h 필드 순서역전이
**10회차 연속**, **KAITO**는 vol24h=volCcy24h 완전동일값 이상치가 **10회차 연속**, **GRAM**도
완전동일값이 **8회차 연속** 재현됐다. MMT·PIPPIN은 volCcy24h가 vol24h보다 약 10배 큰 필드
관계를 계속 유지(vol24_usd 계산에는 영향 없음), **BEAT도 이번 회차 동일 패턴**(volCcy24h≈10×
vol24h)을 보여 계산값이 CoinGecko okex_swap·Aster 값과 잘 수렴했다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·
ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD 등 raw 정밀값 확보. BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·
BTW·BLESS·ANSEM은 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·
BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON 전량 확보(raw 정밀값). MMT·GIGGLE·
PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값). KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·CORE는
여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.17M/OI $18.22M, ETH-USD $5.64M/OI $8.99M,
SOL-USD $0.24M/OI $4.53M) 확보.

**CoinGecko `/global`**: 직접 API로 총시총 $2,306,712,881,096.77(약 $2.307T)·BTC도미넌스
56.67%를 확인했다. 직전 회차($2.299T·56.65%)보다 소폭 상승, **4회 연속** 안정적으로 확보됐다.

**Fear&Greed**: alternative.me API로 정상 응답, **31(Fear)** 확인 — **8회차 연속** 동일값.

**신규 발견**: BICO에서 소스 간 신뢰도 문제 발생 — OKX 직접조회(-26.344%)·Aster(-21.243%)·
OrangeX(-7.804%) 세 소스는 방향(하락)에 합의하나 CoinGecko okex_swap 요약(-0.47%)이 크게
어긋나 이상치로 판단·미채택했다. BEAT는 반대로 이번 회차 3소스(OKX직접·okex_swap·Aster)가
20~21%대로 잘 수렴해 직전 회차의 신뢰도 문제가 상당 부분 해소됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM·BEAT·BICO(OKX
직접 조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(25회차 연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은
본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상 스케일로
관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·
GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며, 이는
데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·
HYNA:HYPE-USD·BLESS는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다; (h) **BICO의
CoinGecko okex_swap 요약값(-0.47%)은 OKX 직접조회·Aster·OrangeX 세 소스와 크게 괴리해
이상치로 판단, 본 리포트 수치에는 미반영했다** — 정직성 규약에 따른 조치이며, 향후 회차에서
재확인이 필요하다; (i) BICO의 이번 회차 급락 재개, ACE의 완전 반전은 여러 거래소에서 동시
재현돼 데이터 오류보다는 실제 시장 이벤트로 보이나, 구체적 촉매(디레버리징 재개·언락
선반영 등)는 정황 증거 수준이며 확정하지 않는다; (j) ACE 언락 관련 tokenomist 소스를
WebFetch로 재확인해 8/10 Early Investors 배분이 재확인됐으나, 정확한 수량·집행 시각까지는
명시되지 않아 별도 WebSearch로 확보한 1.8M ACE(공급 1.2%) 수치를 참고로 병기했다; (k)
GIGGLE·KAITO의 필드 이상치가 10회차 연속, GRAM도 8회차 연속 재현돼 구조적 패턴으로 완전히
굳어졌으나 근본 원인(OKX API 자체 특성인지)은 규명하지 않았다; (l) HYNA:HYPE-USD의 OI
정상화가 3회차 연속 확인됐으나, 완전한 정상화 확정까지는 추가 회차 확인이 필요하다; (m)
`/global`은 4회 연속 성공해 복구가 상당히 안정적으로 보이나 완전한 확정으로 단정하지는
않는다; (n) 지금은 일요일 밤에서 월요일로 넘어가는 시각으로 유동성 패턴이 평일과 다를 수
있으며, 확정 불가.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
