# 선물시장 스카우트 브리핑 — 2026-08-09 22:29 UTC (KST 2026-08-10 07:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-09T20:28:00Z)
> 로부터 약 2시간01분 경과, ACE 언락 예정(UTC 8/10 00:00 추정)까지 이제 약 1시간31분.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 재시도 없이 확보 성공 — 총시총 **$2,312,515,418,800.65(약 $2.313T)**·
BTC도미넌스 **56.64%**로 직전 회차($2.306T·56.64%)보다 시총은 소폭 상승, 도미넌스는 동일 —
**8회 연속** 확보됐다.

### Fear&Greed 31(Fear) — 12회차 연속 동일값

alternative.me API 정상 응답, **31(Fear)** — 12회차 연속 동일값 유지.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM 개별조회)는 **29회차 연속** 방법론(`oiUsd`
필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을 유지했다.

⚠️ **데이터소스 참고**: 직전 회차 처음 누락됐던 **BEAT가 이번 회차 CoinGecko okex_swap 배열에
재등장**해 정상 확보됐다 — 직전 결손이 구조적 문제가 아니라 **1회성 이슈**였음이 확인됐다.

## 이번 회차 최대 사건

### ⚠️⚠️⚠️⚠️⚠️ ACE — 언락 미집행 확인에도 전 소스 급격 재악화

WebSearch로 재확인한 결과, 8/10 언락(Early Investors 대상 약 **1.8M ACE, $199.15K, 공급의
1.2%**)은 **아직 집행되지 않은 상태**임이 확인됐다(tokenomist 페이지 기준 '다음 언락' 상태
유지). 참고로 8/18에는 별도의 더 큰 언락(2,966,040 ACE, 공급 2%)이 예정돼 있어 혼동에 유의해야
한다. 그럼에도 언락 임박 시점에 **5개 소스 전원이 지금까지 관측된 회차 중 가장 크게 동조
급락**했다: Binance **-18.639%**, Bybit **-18.699%**(가중 **-18.653%**), OrangeX
**-17.149%**, Aster **-17.963%**, Hyperliquid **-19.386%**로 전 소스가 직전 대비
**5~7%p씩 추가로** 나빠졌다 — 언락 자체가 아직 미집행인데도 선반영 매도가 뚜렷이 심화되는
모습이다. OKX 직접조회로 ACE-USDT-SWAP를 재확인한 결과 이번 회차도 instId 자체가 존재하지
않아 OKX 미상장이 재확인됐다.

### ⚠️ BICO — 완화 흐름 반전, 다시 악화

직전 회차의 낙폭 완화 흐름이 반전돼 4소스 모두 다시 악화됐다. OKX(CG okex_swap)
**-16.285%→-18.725%**, OrangeX **-17.069%→-19.601%**, Aster **-15.395%→-18.393%**로
동조 재악화했다(직전 -15~-17% 수렴에서 재확산).

### ⚠️ BEAT — okex_swap 재등장과 함께 재가속 재개, 신고점

CoinGecko okex_swap 배열 재등장과 동시에 재가속이 재개돼 이번 회차 신고점을 찍었다. OKX(CG)
**+37.43%**, Aster **+25.693%→+37.08%**, OrangeX **+24.502%→+36.234%**로 3소스 모두
24~26%대에서 **36~37%대**로 급확대됐다(기존 고점 27~33%대를 상회).

### ⚠️⚠️ KAITO — 가격-펀딩 괴리 해소, 동반 회복

직전 회차 지목된 가격-펀딩 괴리가 이번 회차 해소되는 흐름을 보였다. OKX 직접
**-5.616%→-4.017%**·펀딩 **-0.692%→-0.451%**, Hyperliquid **-5.511%→-3.85%**·펀딩
**-0.404%→-0.223%**로 가격·펀딩이 함께 개선(동조 회복)됐다. 8/20 대형 언락(공급 약
3.3~7.6%, 소스별 $22.9M~$34.68M로 편차)까지 약 10.1일 남았다.

## 직전 회차 강조 종목 추적 결과

- **① ACE — ⚠️⚠️⚠️⚠️⚠️ 미집행 확인에도 급격 재악화.** 위 '이번 회차 최대 사건' 참조.
- **② KAITO — ⚠️⚠️ 가격-펀딩 괴리 해소.** 위 참조.
- **③ BICO — ⚠️ 완화 반전, 재악화.** 위 참조.
- **④ BANK — 손익분기 이탈 반전, 플러스 복귀.** Binance/Bybit 가중 **-0.047%→+0.880%**
  (Binance +0.887%·Bybit +0.837%), Aster도 마이너스→플러스 재전환(**+0.735%**), OrangeX는
  냉각하며 손익분기 근접(+0.369%→**+0.063%**).
- **⑤ CASHCAT — 재가속 진정.** HL **+24.904%→+19.902%**, OrangeX
  **+22.916%→+19.896%**, Aster **+22.323%→+16.77%**로 3거래소 모두 진정 — 온체인의
  진정 흐름과 선물 지표가 정합됐다.
- **⑥ BLESS — 재역전이 다시 완화.** OrangeX **-14.692%→-11.89%**, Aster
  **-13.569%→-11.487%**.
- **⑦ BTW — 고점 재접근 후 소폭 냉각.** Aster **+11.228%→+8.453%**.

## 기타 주요 변화

**AEON**은 직전 회차의 첫 완화가 1회성이었던 것으로 확인되며 3소스 모두 재악화했다(OKX CG
-5.325%→**-7.604%**, OrangeX -5.821%→**-7.25%**, Aster -5.361%→**-7.133%**). **BSB**는
여러 회차 이어진 급악화가 3소스 모두 처음으로 완화 조짐을 보였다(OKX CG -11.861%→**-9.869%**,
OrangeX -12.143%→**-11.385%**, Aster -11.487%→**-9.543%**). **ASTER**는 손익분기권 이탈
이후 전 소스에서 플러스 확대를 이어갔다(Binance/Bybit 가중 +1.529%→**+1.765%**, OrangeX
+1.705%, Aster +1.572%, HL +1.798%).

## 데이터 이슈 추적 결과

**HYNA:HYPE-USD**의 OI가 $695,086.18→**$695,086.18**로 완전히 동일해 정상화가 사실상
완료된 것으로 보인다. GIGGLE의 필드 순서역전이 **14회차 연속**, KAITO(OKX 직접)의
완전동일값이 **14회차 연속**, GRAM의 완전동일값이 **12회차 연속** 재현됐다 — 세 이상치 모두
여전히 견고하다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️⚠️⚠️⚠️ 미집행에도 급락] | Binance/Bybit(가중) | $112.34M | $12.23M | +0.001% | -18.653% | 언락 미집행 확인에도 5소스 전원 5~7%p씩 급락 | unlock-pending-all-sources-sharply-worsen |
| **BICO** [⚠️ 완화 반전] | OKX(CoinGecko정상, okex_swap) | $534.23M | $8.95M | -0.137% | -18.725% | -16.285%→-18.725%, 3소스 동조 재악화 | easing-reverses-worsens-again |
| **BEAT** [⚠️ 재등장, 신고점] | OKX(CoinGecko정상, okex_swap, 재등장) | $398.44M | $12.71M | +0.005% | +37.43% | okex_swap 재등장과 함께 재가속 재개, 신고점 | reappears-in-okex-reaccelerates-new-high |
| **KAITO** [⚠️⚠️ 괴리 해소] | OKX(직접API) | $85.07M | $7.81M | -0.451% | -4.017% | 가격·펀딩 동반 회복. 8/20 언락 약 10.1일 앞 | price-funding-divergence-resolves |
| **BANK** [플러스 복귀] | Binance/Bybit(가중) | $117.85M | $18.92M | -0.013% | +0.880% | -0.047%→+0.880%, Aster도 마이너스→플러스 | whipsaw-back-to-positive |
| MMT [플러스 유지, 냉각] | OKX(직접API) | $85.17M | $3.27M | -0.026% | +1.031% | +1.340%→+1.031% | positive-holds-mild-cooling |
| BSB [급악화 처음 완화] | OKX(CoinGecko정상, okex_swap) | $6.55M | $2.55M | +0.020% | -9.869% | -11.861%→-9.869%, 3소스 동반 완화 | sharp-worsening-eases-first-time |
| AAVE [플러스 확대] | Binance/Bybit(가중) | $37.59M | $90.01M | +0.005% | +0.574% | +0.075%→+0.574% | extends-positive |
| ALLO [악화 완화] | Binance/Bybit(가중) | $21.93M | $18.10M | +0.005% | -5.460% | -9.575%→-5.460%, 전 소스 동조 완화 | worsening-eases |
| ADA [13회차 마이너스] | Binance/Bybit(가중, USDT만) | $118.97M | $172.59M | +0.010% | -0.497% | -1.325%→-0.497% | thirteenth-round-negative-mild-easing |
| AKE [개선 확대] | Binance/Bybit(가중) | $41.87M | $39.72M | +0.054% | +7.492% | +5.003%→+7.492% | improvement-continues-extends |
| GIGGLE [소폭 개선] | OKX(직접API) | $26.30M | $2.72M | +0.005% | -2.372% | -3.651%→-2.372%. ⚠️ 필드 이상치 14회차 연속 | mild-improvement-within-negative-field-anomaly-14th-round |
| PIPPIN [플러스 개선] | OKX(직접API) | $1.82M | $1.90M | +0.032% | +2.396% | +1.991%→+2.396% | mild-improvement-holds-positive |
| 1000RATS [플러스 확대, 냉각] | Binance/Bybit(가중) | $13.64M | $18.97M | +0.015% | +5.330% | +6.832%→+5.330% | extends-positive-mild-cooling |
| AIO [플러스 전환] | Binance/Bybit(가중) | $8.45M | $4.67M | +0.049% | +0.695% | -1.975%→+0.695% | turns-positive-from-negative |
| GRAM [거의 유지] | OKX(직접API) | $2.15M | $6.22M | +0.005% | -1.763% | -1.760%→-1.763%. ⚠️ 필드 이상치 12회차 연속 | roughly-flat-within-negative-vol-field-anomaly-12th-round |
| AEON [⚠️ 완화 반전] | OKX(CoinGecko정상, okex_swap) | $26.83M | $3.71M | +0.005% | -7.604% | -5.325%→-7.604%, 전 소스 동조 재악화 | easing-reverses-worsens-again |
| ATOM [플러스 확대] | Binance/Bybit(가중) | $7.98M | $28.85M | +0.009% | +0.629% | +0.191%→+0.629% | extends-positive |
| ASTER [플러스 확대] | Binance/Bybit(가중) | $19.30M | $114.96M | +0.005% | +1.765% | +1.529%→+1.765%, DEX도 동조 확대 | extends-positive-continues |
| CORE [개선 확대] | OKX(CoinGecko정상, okex_swap) | $1.77M | $1.05M | +0.010% | +4.824% | +2.451%→+4.824% | low-liquidity-improvement-extends |
| CAP [소폭 냉각] | OKX(CoinGecko정상, okex_swap) | $17.22M | $2.25M | +0.005% | +6.346% | +8.125%→+6.346% | mild-cooling-holds-positive |
| ALGO [소폭 완화] | Binance/Bybit(가중) | $10.62M | $14.64M | +0.010% | -2.676% | -3.246%→-2.676% | mild-easing-within-negative |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [⚠️⚠️⚠️⚠️⚠️ 급락] | Hyperliquid | $2.78M | $1.34M | +0.001% | -19.386% | -13.603%→-19.386% | unlock-pending-sharply-worsens |
| **ACE-USDT-PERPETUAL** [급락] | OrangeX | $57.12M | $19.34M | +0.011% | -17.149% | -11.841%→-17.149% | unlock-pending-sharply-worsens |
| **ACE-USDT** [급락] | Aster | $0.43M | $0.05M | +0.001% | -17.963% | -13.243%→-17.963% | unlock-pending-sharply-worsens |
| BEAT-USDT-PERPETUAL [신고점] | OrangeX | $17.23M | $6.59M | -0.074% | +36.234% | +24.502%→+36.234% | reaccelerates-new-high |
| BEAT-USDT [신고점] | Aster | $2.51M | $6.54M | +0.029% | +37.08% | +25.693%→+37.08% | reaccelerates-new-high |
| **BICO-USDT-PERPETUAL** [⚠️ 재악화] | OrangeX | $274.39M | $84.80M | +0.082% | -19.601% | -17.069%→-19.601% | easing-reverses-worsens-again |
| **BICO-USDT** [⚠️ 재악화] | Aster | $4.38M | $0.30M | +0.005% | -18.393% | -15.395%→-18.393% | easing-reverses-worsens-again |
| **CASHCAT** [진정] | Hyperliquid | $18.95M | $22.49M | +0.053% | +19.902% | +24.904%→+19.902%, 온체인 정합 | reacceleration-cools-onchain-aligns |
| CASHCAT-USDT-PERPETUAL [진정] | OrangeX | $0.14M | $0.06M | +0.075% | +19.896% | +22.916%→+19.896% | reacceleration-cools |
| CASHCAT-USDT [진정] | Aster | $1.98M | $1.54M | +0.031% | +16.77% | +22.323%→+16.77% | reacceleration-cools |
| ALLO-USDT [악화 완화] | Aster | $0.08M | $0.03M | +0.001% | -5.377% | -9.625%→-5.377% | worsening-eases |
| ALLO-USDT-PERPETUAL [악화 완화] | OrangeX | $14.97M | $4.92M | +0.010% | -5.29% | -9.589%→-5.29% | worsening-eases |
| AAVE-USDT-PERPETUAL [플러스 확대] | OrangeX | $21.47M | $6.99M | +0.010% | +0.361% | +0.044%→+0.361% | extends-positive |
| AAVE-USDT [플러스 전환] | Aster | $0.38M | $4.64M | +0.010% | +0.535% | -0.098%→+0.535% | turns-positive |
| AAVE-USD [플러스 확대] | Hyperliquid | $2.65M | $61.01M | +0.001% | +0.64% | +0.079%→+0.64% | extends-positive |
| ADA-USDT-PERPETUAL [완화] | OrangeX | $67.27M | $24.52M | +0.010% | -0.851% | -1.347%→-0.851% | mild-easing-within-negative |
| ADA-USDT [완화] | Aster | $0.28M | $1.74M | +0.010% | -0.35% | -1.250%→-0.35% | mild-easing-within-negative |
| ADA-USD [완화] | Hyperliquid | $1.66M | $32.98M | +0.001% | -0.231% | -1.369%→-0.231% | mild-easing-within-negative |
| BANK-USDT-PERPETUAL [손익분기 근접] | OrangeX | $8.02M | $2.75M | -0.031% | +0.063% | +0.369%→+0.063% | cools-toward-breakeven |
| BANK-USDT [플러스 전환] | Aster | $0.56M | $0.36M | +0.001% | +0.735% | -0.622%→+0.735% | turns-positive-from-negative |
| AKE-USDT-PERPETUAL [개선 확대] | OrangeX | $5.91M | $2.23M | +0.050% | +7.278% | +5.069%→+7.278% | improves-extends |
| AKE-USDT [개선 확대] | Aster | $0.61M | $11.54M | +0.022% | +7.918% | +4.743%→+7.918% | improves-extends |
| CAP-USDT [소폭 냉각] | Aster | $0.03M | $0.11M | +0.001% | +8.038% | +8.383%→+8.038% | mild-cooling-holds-positive |
| CAP-USDT-PERPETUAL [소폭 냉각] | OrangeX | $0.47M | $0.18M | +0.010% | +6.533% | +8.388%→+6.533% | mild-cooling-holds-positive |
| ALGO-USDT-PERPETUAL [거의 유지] | OrangeX | $6.18M | $2.22M | +0.010% | -2.86% | -3.082%→-2.86% | roughly-flat-negative |
| ALGO-USDT [초저유동성, 악화] | Aster | $0.03M | $0.02M | +0.001% | -3.936% | -2.849%→-3.936% | low-liquidity-mild-worsening |
| ALGO-USD [소폭 완화] | Hyperliquid | $0.77M | $1.93M | +0.001% | -2.62% | -3.481%→-2.62% | mild-easing |
| ATOM-USDT-PERPETUAL [플러스 확대] | OrangeX | $4.56M | $1.65M | +0.010% | +0.578% | +0.072%→+0.578% | extends-positive |
| ATOM-USDT [초저유동성, 마이너스 유지] | Aster | $0.01M | $1.61M | +0.010% | -0.289% | -0.145%→-0.289% | low-liquidity-negative-holds |
| ATOM-USD [플러스 확대] | Hyperliquid | $0.17M | $1.93M | +0.001% | +0.657% | +0.238%→+0.657% | extends-positive |
| ASTER-USDT-PERPETUAL [플러스 확대] | OrangeX | $8.24M | $2.88M | +0.010% | +1.705% | +0.953%→+1.705% | extends-positive |
| ASTER-USDT [대형 OI 플러스 확대] | Aster | $11.87M | $223.05M | +0.016% | +1.572% | OI 거의 유지, +1.002%→+1.572% | large-oi-extends-positive |
| ASTER-USD [플러스 확대] | Hyperliquid | $1.10M | $15.19M | +0.001% | +1.798% | +1.549%→+1.798% | extends-positive |
| KAITO-USD [⚠️⚠️ 가격·펀딩 회복] | Hyperliquid | $20.95M | $14.28M | -0.223% | -3.85% | -5.511%→-3.85%, 펀딩도 -0.404%→-0.223%로 회복 | price-funding-divergence-resolves |
| GRAM-USD [거의 유지] | Hyperliquid | $0.44M | $12.87M | +0.001% | -1.446% | -1.706%→-1.446% | roughly-flat-matches-okx |
| HYPE-USD [소폭 완화] | Hyperliquid | $69.82M | $1,191.97M | +0.001% | -0.815% | -1.016%→-0.815% | mild-easing |
| HYPER-USD [플러스 전환] | Hyperliquid | $0.10M | $0.31M | +0.001% | +0.339% | -0.218%→+0.339% | turns-positive |
| APEX-USD [거의 유지] | Hyperliquid | $0.08M | $0.78M | +0.001% | +1.053% | +1.075%→+1.053%, Bybit도 근접(+1.098%) | roughly-flat-bybit-matches |
| FARTCOIN [재가속 지속] | Hyperliquid | $5.84M | $23.20M | +0.001% | +3.348% | +2.815%→+3.348% | reacceleration-continues |
| ETHFI-USD [확대] | Hyperliquid | $0.60M | $8.48M | +0.001% | +1.832% | +0.430%→+1.832% | extends |
| ETH-USD [플러스 확대] | dYdX | $5.39M | $8.96M | 0.000% | +0.578% | +0.099%→+0.578% | extends-positive |
| BTC-USD [플러스 확대] | dYdX | $1.37M | $17.94M | 0.000% | +0.447% | +0.145%→+0.447% | extends-positive |
| SOL-USD [거의 유지] | dYdX | $0.12M | $4.56M | 0.000% | +1.523% | +1.512%→+1.523% | roughly-flat-positive |
| ANSEM [개선 지속] | Aster | $0.23M | $0.92M | +0.001% | -3.036% | -4.733%→-3.036% | improves-within-negative-continues |
| ANSEM-USDT-PERPETUAL [개선 지속] | OrangeX | $0.47M | $0.17M | +0.010% | -2.781% | -3.927%→-2.781% | improves-within-negative-continues |
| **BTW** [고점 재접근 후 냉각] | Aster | $2.53M | $15.46M | +0.025% | +8.453% | +11.228%→+8.453% | mild-cooling |
| HYNA:PUMP-USD [거의 유지] | Hyperliquid | $0.04M | $0.17M | +0.001% | +14.022% | +13.820%→+14.022% | roughly-flat |
| **HYNA:HYPE-USD** [OI 완전 동일] | Hyperliquid | $0.14M | $0.70M | +0.008% | -0.131% | $695,086.18→$695,086.18(변동없음) — 정상화 사실상 완료 | oi-fully-stabilizes |
| AEON-USDT-PERPETUAL [⚠️ 재악화] | OrangeX | $0.48M | $0.17M | +0.010% | -7.25% | -5.821%→-7.25% | easing-reverses-worsens-again |
| AEON-USDT [⚠️ 재악화] | Aster | $0.09M | $0.22M | +0.011% | -7.133% | -5.361%→-7.133% | easing-reverses-worsens-again |
| **BSB-USDT-PERPETUAL** [처음 완화] | OrangeX | $12.40M | $4.11M | +0.010% | -11.385% | -12.143%→-11.385% | sharp-worsening-eases-first-time |
| **BSB-USDT** [처음 완화] | Aster | $0.05M | $0.10M | +0.001% | -9.543% | -11.487%→-9.543% | sharp-worsening-eases-first-time |
| 1000RATS-USDT [플러스 확대, 냉각] | Aster | $0.10M | $0.04M | +0.012% | +6.095% | +8.109%→+6.095% | extends-positive-mild-cooling |
| **BLESS** [재역전 완화] | OrangeX | $91.38M | $32.50M | +0.051% | -11.89% | -14.692%→-11.89% | relapse-eases-again |
| **BLESS-USDT** [완화] | Aster | $0.34M | $0.22M | +0.005% | -11.487% | -13.569%→-11.487% | eases |

## 테마 태그

1. **시장 전반: `/global`이 재시도 없이 8회 연속 확보 성공 — 총시총 $2.313T(소폭 상승)·BTC도미넌스 56.64%(동일)** (global-api-eighth-consecutive-success).
2. **Fear&Greed 31(Fear) 12회차 연속 동일값 유지** (fear-greed-holds-31-twelfth-consecutive-round).
3. **⚠️⚠️⚠️⚠️⚠️ ACE: 언락 미집행 확인에도 5소스 전원 급격 재악화(가중 -12.304%→-18.653%)** (ace-unlock-still-pending-yet-sharp-relapse).
4. **⚠️ BICO: 완화 흐름 반전, 4소스 모두 재악화(-15~-17%→-18~-20%)** (bico-easing-reverses-worsens-again).
5. **⚠️ BEAT: okex_swap 재등장과 재가속 재개, 3소스 신고점(24~26%대→36~37%대)** (beat-reappears-reaccelerates-new-high).
6. **⚠️⚠️ KAITO: 가격-펀딩 괴리 해소, 가격·펀딩 동반 개선. 8/20 언락 약 10.1일 앞** (kaito-price-funding-divergence-resolves).
7. **BANK: 손익분기 이탈이 재반전, 플러스 복귀(가중 -0.047%→+0.880%)** (bank-whipsaw-back-to-positive).
8. **CASHCAT: 재가속 진정(18~25%대→17~20%대) — 온체인의 진정 흐름과 정합** (cashcat-reaccelerates-then-cools-onchain-aligns).
9. **⚠️ AEON: 직전 첫 완화가 1회성이었음이 확인, 3소스 재악화** (aeon-easing-reverses-worsens-again).
10. **BLESS: 재역전이 다시 완화(-14.7%→-11.9%)** (bless-relapse-eases-again).
11. **BTW: 고점 재접근 후 소폭 냉각(+11.228%→+8.453%)** (btw-mild-cooling-after-reapproach).
12. **BSB: 여러 회차 급악화가 3소스 모두 처음 완화 조짐** (bsb-sharp-worsening-eases-first-time).
13. **HYNA:HYPE-USD: OI 완전 동일값 유지, 정상화 사실상 완료** (hyna-hype-oi-fully-stabilizes).
14. **⚠️ 데이터소스 참고: 직전 결손이던 BEAT가 이번 회차 okex_swap 재등장, 1회성 결손 확인** (beat-okex-swap-reappears-confirms-one-off).
15. **⚠️ GIGGLE 필드 이상치 14회차 연속, KAITO(OKX 직접) 완전동일값 14회차 연속, GRAM 12회차 연속 재현** (field-anomalies-14th-12th-round-continue).
16. **OKX ACE·BANK·1000RATS·AIO·KAITO·MMT·PIPPIN·GIGGLE·GRAM은 okex_swap 미등재(ACE는 instId 자체 부재), 직접 API/DEX로 보강(BEAT는 정상 복귀)** (okx-most-still-not-listed-direct-api-supplements).
17. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
18. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
19. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
20. **ACE 언락 예정(UTC 8/10 00:00 추정)까지 약 1시간31분 — 다음 회차가 언락 집행 여부를 처음 확인할 수 있는 시점** (unlock-approx-1-5-hours-away-next-round-critical).

## 데이터 신뢰도

**CoinGecko binance_futures**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS
확인. **BICO·BEAT·BSB·APEX·BTW·KAITO·CASHCAT·MMT·GIGGLE·PIPPIN·GRAM·CORE·CAP·AEON·BLESS·
ANSEM은 이번 회차도 명확히 미확인**(단순 미상장).

**CoinGecko bybit**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS·APEX 확인.
나머지는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·CAP·BICO 확인. ⚠️
**BEAT가 이번 회차 배열에 재등장**해 정상 확보됐다(직전 회차 1회성 결손에서 복귀). ACE·BANK·
AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT은 이번 회차도 okex_swap 배열에서
미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인.
`oiUsd` 필드 직접 사용 방법론을 **29회차 연속** 유지, vol24_usd=`volCcy24h`×`last` 계산
방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️ **ACE-USDT-SWAP는 OKX에 instId
자체가 존재하지 않음**을 이번 회차도 직접 확인(에러코드 51001), okex_swap 미등재가
CoinGecko 집계 지연이 아니라 실제 미상장임이 재확인됐다. **GIGGLE**은 vol24h/volCcy24h
필드 순서역전이 **14회차 연속**, **KAITO**는 vol24h=volCcy24h 완전동일값 이상치가
**14회차 연속**, **GRAM**도 완전동일값이 **12회차 연속** 재현됐다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·
ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD 등 raw 정밀값 확보. BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·
BTW·BLESS·ANSEM은 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·
BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON 전량 확보(raw 정밀값). MMT·GIGGLE·
PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값). BTW는 이번 회차도 OrangeX에서 미발견(기존과
동일, Aster에서만 확인). KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·CORE는 여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.37M/OI $17.94M, ETH-USD $5.39M/OI $8.96M,
SOL-USD $0.12M/OI $4.56M) 확보.

**CoinGecko `/global`**: 재시도 없이 총시총 $2,312,515,418,800.65(약 $2.313T)·BTC도미넌스
56.64%를 확인했다. 직전 회차($2.306T·56.64%)보다 시총은 소폭 상승, 도미넌스는 동일,
**8회 연속** 안정적으로 확보됐다.

**Fear&Greed**: alternative.me API로 정상 응답, **31(Fear)** 확인 — **12회차 연속**
동일값.

**신규 발견**: (a) WebSearch로 ACE 8/10 언락이 아직 집행되지 않은 것으로 확인됐음에도 5개
소스 전원이 지금까지 관측된 회차 중 가장 크게 동조 급락했다 — 언락 집행 자체보다 선반영성
매도·투기 포지셔닝이 임박 시점에 더욱 강해지는 패턴을 시사한다(다만 인과관계를 확정하지는
않는다). (b) BEAT가 CoinGecko okex_swap 배열에 재등장했다 — 직전 회차의 결손이 데이터 결손이
아니라 일시적 API 이슈였음이 확인됐다. (c) KAITO에서 직전 회차 관측된 가격·펀딩 괴리가
이번 회차 해소돼 두 지표가 함께 개선됐다 — 파생 포지셔닝과 가격이 다시 동조하는 정상화
흐름으로 해석할 수 있다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(29회차 연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은
본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상 스케일로
관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·
GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며,
이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·
HYNA:HYPE-USD·BLESS는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다; (h) ACE 언락은
WebSearch로 8/10, Early Investors 대상 약 1.8M ACE($199.15K·공급 1.2%)로 확인됐으나
정확한 UTC 집행 시각은 여전히 명시되지 않아 다음 회차에서 실제 집행 여부·시각·가격 반응을
재확인해야 한다(다음 회차가 언락 이후 첫 관측이 될 가능성이 높다); (i) BICO의 소스 간
격차가 이번 회차 -18~-20%로 재확산했으며, 근본 원인(거래소별 집계 시차 등)은 규명하지
않았다; (j) KAITO 8/20 언락 규모는 소스별로 공급 3.3%(WebSearch 초기 결과)~7.63%
(tokenomist)·$22.9M~$34.68M로 편차가 있어 정확한 수치는 확정하지 않았다; (k) GIGGLE·
KAITO의 필드 이상치가 14회차 연속, GRAM도 12회차 연속 재현돼 구조적 패턴으로 굳어졌으나
근본 원인(OKX API 자체 특성인지)은 규명하지 않았다; (l) HYNA:HYPE-USD의 OI가 이번 회차
직전 회차와 완전히 동일한 값으로 관측됐으나, 이것이 API 갱신 지연 때문인지 완전한 시장
정상화 때문인지는 구분하지 않았다; (m) `/global`은 8회 연속 성공(이번엔 재시도 불필요)해
복구가 안정적으로 보이나 완전한 확정으로 단정하지는 않는다; (n) BEAT의 okex_swap 재등장이
1회성 결손을 확정하는 강한 증거이나, 향후 재발 여부는 계속 관찰이 필요하다; (o) ACE
언락(추정 1시간31분 앞)에 따른 추가 변동성 확대 가능성을 배제할 수 없으며, 다음 회차가
언락 이후 첫 관측이 될 전망이다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
