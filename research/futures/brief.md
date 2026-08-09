# 선물시장 스카우트 브리핑 — 2026-08-09 20:28 UTC (KST 2026-08-10 05:28)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-09T18:31:00Z)
> 로부터 약 1시간57분 경과, ACE 언락 예정(UTC 8/10 00:00 추정)까지 이제 약 3.5시간.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 재시도 후 확보 성공 — 총시총 **$2,305,992,226,621.85(약 $2.306T)**·
BTC도미넌스 **56.64%**로 직전 회차($2.308T·56.67%)보다 시총·도미넌스 모두 소폭 하락 —
**7회 연속** 확보됐다.

### Fear&Greed 31(Fear) — 11회차 연속 동일값

alternative.me API 정상 응답, **31(Fear)** — 11회차 연속 동일값 유지.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM·BEAT 개별조회)는 **28회차 연속** 방법론(`oiUsd`
필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을 유지했다.

⚠️ **데이터소스 참고**: 이번 회차 **BEAT가 CoinGecko okex_swap 배열에서 처음으로 누락**됐다
(과거엔 정상 확보) — OKX 직접 API로 대체 집계했다. BICO·AEON·BSB·CAP·CORE·ADA·AAVE·ALLO·
ALGO·ATOM·ASTER는 okex_swap에서 정상 확인됐다.

## 이번 회차 최대 사건

### ⚠️⚠️⚠️⚠️ ACE — 언락 실체는 소액인데 낙폭은 재악화

WebSearch로 언락 실체를 재확인한 결과, 8/10 언락은 **Early Investors 대상 약 1.8M ACE
($199.15K, 공급의 1.2%)**에 불과한 **소액 언락**으로 확인됐다. 지난 며칠간 관측된 두 자릿수
낙폭에 비하면 실제 토큰 방출 규모는 크지 않아, 가격 압력이 언락 자체보다 **선반영성 매도·투기
포지셔닝**에서 왔을 가능성을 시사한다. 그럼에도 낙폭은 직전 회차의 완화 흐름을 되돌리며 전
소스 동조 재악화했다: Binance **-12.107%**, Bybit **-12.993%**(가중 **-12.304%**), OrangeX
**-11.841%**, Aster **-13.243%**, Hyperliquid **-13.603%**로 5개 소스 모두 1~2%p씩 다시
나빠졌다. OKX 직접조회로 ACE-USDT-SWAP를 재확인한 결과 이번 회차도 instId 자체가 존재하지
않아 OKX 미상장이 재확인됐다.

### ⚠️ BICO — 낙폭 뚜렷이 추가 완화

OKX(CG okex_swap) **-22.844%→-16.285%**, OrangeX **-22.547%→-17.069%**, Aster
**-22.451%→-15.395%**로 4소스가 **-15~-17%** 범위로 더 좁게 수렴했다(직전 -22~-24% 대비
개선).

### ⚠️ BEAT — 재가속 처음으로 꺾이며 냉각 전환

OKX 직접 **+24.631%**(전 회차 CG 기준 +27.352%), Aster **+32.934%→+25.693%**, OrangeX
**+33.247%→+24.502%**로 3소스 모두 **24~26%대**로 내려와 수렴했다(직전 27~33%대에서 축소).

### ⚠️⚠️ KAITO — 가격 부분회복하나 펀딩은 오히려 더 마이너스로

OKX 직접 **-7.038%→-5.616%**, Hyperliquid **-7.802%→-5.511%**로 두 소스 모두 반등했지만,
펀딩은 OKX **-0.463%→-0.692%**, HL **-0.195%→-0.404%**로 더 깊은 마이너스로 이동해 숏
우위가 심화됐다 — **가격 반등에도 파생시장 포지셔닝은 여전히 하방 베팅 우세**임을 시사한다.
WebSearch로 8/20 대형 언락(공급 약 3.3~7.6%, 소스별 $22.9M~$34.68M로 편차)이 재확인됐고
약 10.6일 앞으로 다가왔다.

## 직전 회차 강조 종목 추적 결과

- **① ACE — ⚠️⚠️⚠️⚠️ 언락 소액 확인, 그럼에도 재악화.** 위 '이번 회차 최대 사건' 참조.
- **② BICO — ⚠️ 낙폭 추가 완화.** 위 참조.
- **③ BEAT — ⚠️ 재가속 꺾이며 냉각.** 위 참조.
- **④ BANK — 손익분기권 이탈, 마이너스로.** Binance/Bybit 가중 **+1.232%→-0.047%**로
  손익분기 이탈, Binance -0.199%·Bybit +0.900%. OrangeX 재냉각(+0.976%→**+0.369%**), Aster는
  플러스에서 마이너스로 전환(+1.274%→**-0.622%**). 펀딩도 +0.005%→**-0.006%**로 반전.
- **⑤ KAITO — ⚠️⚠️ 가격·펀딩 괴리.** 위 참조.
- **⑥ CASHCAT — 뚜렷이 재가속.** HL **+18.411%→+24.904%**, OrangeX **+18.253%→+22.916%**,
  Aster **+18.840%→+22.323%**로 3거래소 모두 재가속 — 직전 회차 지목된 **온체인(HL) 재가속이
  선물 지표에도 그대로 반영**됐다(Robinhood 모멘텀 냉각은 일시적이었을 가능성).

## 기타 주요 변화

**AEON**은 여러 회차 이어진 동조 악화가 처음으로 꺾여 3소스 모두 완화됐다(OKX CG
-6.514%→**-5.325%**, OrangeX -6.426%→**-5.821%**, Aster -9.479%→**-5.361%**). **BLESS**는
직전 회차의 첫 완화 조짐이 재역전돼 다시 악화됐다(OrangeX -13.101%→**-14.692%**, Aster
-13.323%→**-13.569%**). **BTW**는 3회차 연속 냉각(고점 +16.509%→+4.777%)이 이번 회차 크게
반전돼 재가속했다(+4.777%→**+11.228%**, 고점에 재접근). **ASTER**는 손익분기권 정체를 벗고
전 소스 플러스로 전환(Binance/Bybit 가중 -0.079%→**+1.529%**, OrangeX +0.953%, Aster
+1.002%, HL +1.549%).

## 데이터 이슈 추적 결과

**HYNA:HYPE-USD**의 OI가 $696,608.11→**$695,086.18(-0.22%)**로 소폭 변동을 계속 이어가며
정상화 단계로 보인다. GIGGLE의 필드 순서역전이 **13회차 연속**, KAITO(OKX 직접)의
완전동일값이 **13회차 연속**, GRAM의 완전동일값이 **11회차 연속** 재현됐다 — 세 이상치 모두
여전히 견고하다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️⚠️⚠️ 언락 소액 확인, 재악화] | Binance/Bybit(가중) | $126.45M | $13.09M | +0.001% | -12.304% | 언락 실체는 $199.15K(공급1.2%)로 소액이나 낙폭은 재악화, 전 소스 동조 | unlock-confirmed-small-yet-decline-relapses |
| **BICO** [⚠️ 낙폭 추가 완화] | OKX(CoinGecko정상, okex_swap) | $533.84M | $8.70M | -0.126% | -16.285% | -22.844%→-16.285%, 4소스 -15~-17%로 더 좁게 수렴 | decline-eases-further-narrower-convergence |
| **BEAT** [⚠️ 냉각 전환] | OKX(직접API) | $395.66M | $12.76M | +0.005% | +24.631% | CG okex_swap 누락돼 직접집계, 3소스 24~26%대로 수렴(직전 27~33%대) | reacceleration-reverses-cools-first-time |
| **BANK** [손익분기 이탈] | Binance/Bybit(가중) | $117.72M | $18.93M | -0.006% | -0.047% | +1.232%→-0.047%, Aster도 플러스→마이너스 전환 | turns-slightly-negative-breaks-breakeven-hover |
| **KAITO** [⚠️⚠️ 가격·펀딩 괴리] | OKX(직접API) | $87.54M | $7.80M | -0.692% | -5.616% | 가격 부분회복하나 펀딩 더 마이너스로. 8/20 언락 약 10.6일 앞 | price-recovers-but-funding-deepens-short-bias |
| MMT [뚜렷이 냉각] | OKX(직접API) | $87.62M | $3.50M | -0.004% | +1.340% | +4.734%→+1.340% | positive-turn-cools |
| BSB [급악화 지속] | OKX(CoinGecko정상, okex_swap) | $6.74M | $2.58M | +0.005% | -11.861% | -9.768%→-11.861%, OrangeX·Aster -11~-12%대 수렴 | sharp-worsening-continues |
| AAVE [플러스 전환] | Binance/Bybit(가중) | $38.71M | $89.73M | +0.002% | +0.075% | -0.192%→+0.075% | turns-positive-from-breakeven |
| ALLO [뚜렷이 악화] | Binance/Bybit(가중) | $22.41M | $18.03M | +0.001% | -9.575% | -6.144%→-9.575%, 전 소스 동조 | whipsaw-breaks-worsens-notably |
| ADA [12회차 마이너스] | Binance/Bybit(가중, USDT만) | $117.12M | $172.10M | +0.006% | -1.325% | -1.091%→-1.325% | twelfth-round-negative-slightly-deepens |
| AKE [개선 유지] | Binance/Bybit(가중) | $42.43M | $39.56M | +0.040% | +5.003% | +5.635%→+5.003% | improvement-continues-mild-cooling |
| GIGGLE [재악화] | OKX(직접API) | $26.73M | $2.77M | +0.005% | -3.651% | -0.655%→-3.651%. ⚠️ 필드 이상치 13회차 연속 | worsens-within-negative-field-anomaly-13th-round |
| PIPPIN [플러스 개선] | OKX(직접API) | $1.77M | $1.89M | +0.029% | +1.991% | +0.680%→+1.991% | mild-improvement-holds-positive |
| 1000RATS [플러스 확대] | Binance/Bybit(가중) | $14.09M | $19.10M | +0.020% | +6.832% | +5.890%→+6.832% | extends-positive-strongly |
| AIO [개선] | Binance/Bybit(가중) | $9.96M | $4.55M | +0.039% | -1.975% | -3.340%→-1.975% | improves-within-negative |
| GRAM [소폭 악화] | OKX(직접API) | $2.15M | $6.24M | +0.005% | -1.760% | -0.885%→-1.760%. ⚠️ 필드 이상치 11회차 연속 | mild-worsening-within-negative-vol-field-anomaly-eleventh-round |
| AEON [⚠️ 처음 완화] | OKX(CoinGecko정상, okex_swap) | $27.31M | $3.76M | +0.005% | -5.325% | -6.514%→-5.325%, 전 소스 동조 완화 | first-easing-after-multi-round-worsening |
| ATOM [소폭 플러스] | Binance/Bybit(가중) | $7.84M | $28.57M | +0.010% | +0.191% | +0.004%→+0.191% | mild-positive-from-breakeven |
| ASTER [플러스 전환] | Binance/Bybit(가중) | $18.51M | $115.35M | +0.005% | +1.529% | -0.079%→+1.529%, DEX도 동조 | breaks-out-of-breakeven-turns-positive |
| CORE [개선 지속] | OKX(CoinGecko정상, okex_swap) | $1.80M | $1.02M | +0.010% | +2.451% | +2.006%→+2.451% | low-liquidity-mild-improvement |
| CAP [개선 지속] | OKX(CoinGecko정상, okex_swap) | $16.91M | $2.36M | +0.005% | +8.125% | +7.079%→+8.125% | improves-further |
| ALGO [마이너스 심화] | Binance/Bybit(가중) | $8.91M | $14.65M | +0.006% | -3.246% | -1.990%→-3.246% | worsens-within-negative |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [⚠️⚠️⚠️⚠️ 재악화] | Hyperliquid | $2.97M | $1.42M | -0.002% | -13.603% | -10.265%→-13.603% | decline-relapses |
| **ACE-USDT-PERPETUAL** [재악화] | OrangeX | $64.60M | $20.68M | +0.014% | -11.841% | -9.322%→-11.841% | decline-relapses |
| **ACE-USDT** [재악화] | Aster | $0.47M | $0.06M | +0.001% | -13.243% | -10.758%→-13.243% | decline-relapses |
| BEAT-USDT-PERPETUAL [냉각] | OrangeX | $17.82M | $7.15M | -0.055% | +24.502% | +33.247%→+24.502% | reacceleration-reverses-cools |
| BEAT-USDT [냉각] | Aster | $3.00M | $6.05M | +0.019% | +25.693% | +32.934%→+25.693% | reacceleration-reverses-cools |
| **BICO-USDT-PERPETUAL** [⚠️ 추가 완화] | OrangeX | $279.00M | $79.64M | +0.129% | -17.069% | -22.547%→-17.069% | decline-eases-further |
| **BICO-USDT** [⚠️ 추가 완화] | Aster | $4.37M | $0.30M | +0.005% | -15.395% | -22.451%→-15.395% | decline-eases-further |
| **CASHCAT** [뚜렷이 재가속] | Hyperliquid | $19.47M | $22.61M | +0.047% | +24.904% | +18.411%→+24.904%, 온체인 재가속 반영 | reaccelerates-notably |
| CASHCAT-USDT-PERPETUAL [재가속] | OrangeX | $0.14M | $0.06M | +0.010% | +22.916% | +18.253%→+22.916% | reaccelerates-notably |
| CASHCAT-USDT [재가속] | Aster | $2.01M | $1.53M | +0.023% | +22.323% | +18.840%→+22.323% | reaccelerates-notably |
| ALLO-USDT [뚜렷이 악화] | Aster | $0.09M | $0.03M | 0.000% | -9.625% | -6.006%→-9.625% | worsens-notably |
| ALLO-USDT-PERPETUAL [뚜렷이 악화] | OrangeX | $15.55M | $5.24M | +0.010% | -9.589% | -6.727%→-9.589% | worsens-notably |
| AAVE-USDT-PERPETUAL [플러스 전환] | OrangeX | $22.17M | $8.08M | +0.010% | +0.044% | -0.219%→+0.044% | turns-positive |
| AAVE-USDT [손익분기 근접] | Aster | $0.38M | $4.62M | +0.010% | -0.098% | -0.088%→-0.098% | near-breakeven |
| AAVE-USD [플러스 전환] | Hyperliquid | $2.47M | $60.57M | +0.001% | 0.079% | -0.204%→+0.079% | turns-positive |
| ADA-USDT-PERPETUAL [거의 유지] | OrangeX | $65.92M | $23.91M | +0.010% | -1.347% | -1.101%→-1.347% | roughly-flat-negative |
| ADA-USDT [거의 유지] | Aster | $0.28M | $1.61M | +0.010% | -1.250% | -1.298%→-1.250% | roughly-flat-negative |
| ADA-USD [소폭 악화] | Hyperliquid | $1.60M | $32.82M | +0.001% | -1.369% | -1.106%→-1.369% | mild-worsening |
| BANK-USDT-PERPETUAL [재냉각] | OrangeX | $7.83M | $2.88M | -0.018% | +0.369% | +0.976%→+0.369% | cools-again |
| BANK-USDT [마이너스 전환] | Aster | $0.53M | $0.38M | +0.001% | -0.622% | +1.274%→-0.622% | turns-negative |
| AKE-USDT-PERPETUAL [개선, 소폭 냉각] | OrangeX | $6.23M | $2.40M | +0.010% | +5.069% | +5.962%→+5.069% | improves-mild-cooling |
| AKE-USDT [개선, 소폭 냉각] | Aster | $0.62M | $11.46M | +0.016% | +4.743% | +5.105%→+4.743% | improves-mild-cooling |
| CAP-USDT [개선] | Aster | $0.03M | $0.11M | +0.001% | +8.383% | +6.855%→+8.383% | improves |
| CAP-USDT-PERPETUAL [개선] | OrangeX | $0.47M | $0.18M | +0.010% | +8.388% | +7.172%→+8.388% | improves |
| ALGO-USDT-PERPETUAL [소폭 악화] | OrangeX | $5.19M | $1.77M | +0.010% | -3.082% | -1.945%→-3.082% | mild-worsening |
| ALGO-USDT [초저유동성, 악화] | Aster | $0.006M | $0.03M | +0.001% | -2.849% | -1.967%→-2.849% | low-liquidity-mild-worsening |
| ALGO-USD [소폭 악화] | Hyperliquid | $0.70M | $1.92M | +0.001% | -3.481% | -2.058%→-3.481% | mild-worsening |
| ATOM-USDT-PERPETUAL [플러스 전환] | OrangeX | $4.52M | $1.62M | +0.010% | +0.072% | -0.072%→+0.072% | turns-positive |
| ATOM-USDT [초저유동성, 마이너스 전환] | Aster | $0.01M | $1.61M | +0.010% | -0.145% | +0.145%→-0.145% | low-liquidity-turns-negative |
| ATOM-USD [손익분기권] | Hyperliquid | $0.17M | $1.92M | +0.001% | +0.238% | +0.087%→+0.238% | near-breakeven |
| ASTER-USDT-PERPETUAL [플러스 전환] | OrangeX | $7.55M | $2.43M | +0.010% | +0.953% | -0.051%→+0.953% | turns-positive |
| ASTER-USDT [대형 OI 플러스 전환] | Aster | $11.08M | $223.29M | +0.026% | +1.002% | OI $220.88M→$223.29M, -0.016%→+1.002% | large-oi-turns-positive |
| ASTER-USD [플러스 전환] | Hyperliquid | $0.96M | $15.16M | +0.001% | +1.549% | -0.056%→+1.549% | turns-positive |
| KAITO-USD [⚠️⚠️ 가격·펀딩 괴리] | Hyperliquid | $21.94M | $14.12M | -0.404% | -5.511% | -7.802%→-5.511%, 펀딩은 -0.195%→-0.404%로 심화 | price-recovers-funding-deepens |
| GRAM-USD [소폭 악화, OKX 근접] | Hyperliquid | $0.42M | $12.81M | +0.001% | -1.706% | -1.089%→-1.706% | mild-worsening-matches-okx |
| HYPE-USD [소폭 악화] | Hyperliquid | $64.92M | $1,192.74M | +0.001% | -1.016% | -0.248%→-1.016% | mild-worsening |
| HYPER-USD [소폭 마이너스로] | Hyperliquid | $0.10M | $0.31M | +0.001% | -0.218% | +0.091%→-0.218% | turns-slightly-negative |
| APEX-USD [거의 유지] | Hyperliquid | $0.08M | $0.77M | +0.001% | +1.075% | +1.237%→+1.075%, Bybit도 근접(+1.146%) | roughly-flat-bybit-matches |
| FARTCOIN [재가속 지속, 냉각] | Hyperliquid | $5.58M | $23.31M | +0.003% | +2.815% | +4.614%→+2.815% | reacceleration-cools |
| ETHFI-USD [소폭 냉각] | Hyperliquid | $0.60M | $8.39M | +0.001% | +0.430% | +1.090%→+0.430% | mild-cooling |
| ETH-USD [플러스권 유지] | dYdX | $5.32M | $8.91M | 0.000% | +0.099% | +0.109%→+0.099% | holds-positive |
| BTC-USD [플러스 유지] | dYdX | $1.20M | $18.03M | 0.000% | +0.145% | +0.143%→+0.145% | holds-positive |
| SOL-USD [개선] | dYdX | $0.14M | $4.56M | 0.000% | +1.512% | +1.366%→+1.512% | improves |
| ANSEM [마이너스권 개선] | Aster | $0.23M | $0.91M | +0.001% | -4.733% | -6.103%→-4.733% | improves-within-negative |
| ANSEM-USDT-PERPETUAL [마이너스권 개선] | OrangeX | $0.47M | $0.16M | +0.010% | -3.927% | -6.766%→-3.927% | improves-within-negative |
| **BTW** [냉각 끝나고 재가속] | Aster | $2.49M | $15.26M | +0.051% | +11.228% | +4.777%→+11.228%(고점 +16.509%에 재접근) | cooling-streak-breaks-reaccelerates |
| HYNA:PUMP-USD [거의 유지] | Hyperliquid | $0.04M | $0.17M | +0.001% | +13.820% | +12.285%→+13.820% | roughly-flat |
| **HYNA:HYPE-USD** [OI 소폭 이어지는 변동] | Hyperliquid | $0.14M | $0.70M | +0.009% | -0.131% | OI $696,608→$695,086(-0.22%) — 정상화 단계 지속 | oi-continues-small-moves-normalizing |
| AEON-USDT-PERPETUAL [⚠️ 완화] | OrangeX | $0.49M | $0.15M | +0.010% | -5.821% | -6.426%→-5.821% | eases-aligns-with-okx |
| AEON-USDT [⚠️ 크게 완화] | Aster | $0.10M | $0.22M | +0.003% | -5.361% | -9.479%→-5.361% | eases-notably |
| **BSB-USDT-PERPETUAL** [급악화 지속] | OrangeX | $12.88M | $4.60M | +0.010% | -12.143% | -9.994%→-12.143% | sharp-worsening-continues |
| **BSB-USDT** [급악화 지속] | Aster | $0.06M | $0.10M | +0.001% | -11.487% | -10.112%→-11.487% | sharp-worsening-continues |
| 1000RATS-USDT [플러스 확대] | Aster | $0.10M | $0.04M | +0.015% | +8.109% | +4.496%→+8.109%, CEX와 방향 일치 | extends-positive-aligns-with-cex |
| **BLESS** [⚠️ 완화 재역전, 재악화] | OrangeX | $93.44M | $32.21M | +0.055% | -14.692% | -13.101%→-14.692% | easing-reverses-relapses |
| **BLESS-USDT** [거의 유지] | Aster | $0.34M | $0.22M | +0.005% | -13.569% | -13.323%→-13.569% | roughly-flat-mild-worsening |

## 테마 태그

1. **시장 전반: `/global`이 재시도 후 7회 연속 확보 성공 — 총시총 $2.306T·BTC도미넌스 56.64%(둘 다 소폭 하락)** (global-api-seventh-consecutive-success).
2. **Fear&Greed 31(Fear) 11회차 연속 동일값 유지** (fear-greed-holds-31-eleventh-consecutive-round).
3. **⚠️⚠️⚠️⚠️ ACE: WebSearch로 언락 실체 확인 — Early Investors 대상 약 1.8M ACE($199.15K·공급 1.2%)의 소액 언락. 그럼에도 전 소스 동조 재악화** (ace-unlock-confirmed-small-yet-relapse).
4. **⚠️ BICO: 낙폭이 -22~-24%에서 -15~-17%로 뚜렷이 추가 완화, 4소스 더 좁게 수렴** (bico-decline-eases-further).
5. **⚠️ BEAT: 여러 회차 이어진 재가속이 처음 꺾이며 27~33%대에서 24~26%대로 냉각 전환** (beat-reacceleration-reverses-cools).
6. **⚠️⚠️ KAITO: 가격은 OKX·HL 모두 부분회복했으나 펀딩은 더 마이너스로 심화 — 가격·포지셔닝 괴리. 8/20 대형 언락 약 10.6일 앞** (kaito-price-recovers-funding-diverges).
7. **BANK: CEX 대형 거래소 가중 +1.232%→-0.047%로 손익분기 이탈, Aster도 플러스→마이너스, 펀딩도 반전** (bank-turns-slightly-negative).
8. **CASHCAT: 3거래소 모두 뚜렷이 재가속(18%대→22~25%대) — 온체인 재가속이 선물 지표에 반영** (cashcat-reaccelerates-onchain-flows-through).
9. **⚠️ AEON: 여러 회차 동조 악화 후 3소스 모두 처음 완화** (aeon-first-easing-after-multi-round-worsening).
10. **⚠️ BLESS: 직전 회차 첫 완화 조짐이 재역전, 다시 악화(-13.1%→-14.7%)** (bless-easing-reverses-relapses).
11. **BTW: 3회차 연속 냉각이 반전돼 고점(+16.509%)에 재접근하는 재가속(+4.777%→+11.228%)** (btw-cooling-streak-breaks-reaccelerates).
12. **HYNA:HYPE-USD: OI가 소폭 변동을 이어가며(-0.22%) 정상화 단계 지속** (hyna-hype-oi-normalizing).
13. **⚠️ 데이터소스 참고: 이번 회차 BEAT가 CoinGecko okex_swap 배열에서 처음 누락돼 OKX 직접 API로 대체 집계** (beat-missing-from-okex-swap-first-time).
14. **⚠️ GIGGLE 필드 이상치 13회차 연속, KAITO(OKX 직접) 완전동일값 이상치 13회차 연속, GRAM도 11회차 연속 재현** (field-anomalies-13th-11th-round-continue).
15. **OKX ACE·BANK·1000RATS·AIO·KAITO·MMT·PIPPIN·GIGGLE·GRAM·BEAT(이번 회차)는 okex_swap 미등재(ACE는 instId 자체 부재), 직접 API/DEX로 보강** (okx-most-still-not-listed-direct-api-supplements).
16. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
17. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
18. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
19. **ACE 언락 예정(UTC 8/10 00:00 추정)까지 약 3.5시간 — 다음 회차가 언락 이후 첫 관측이 될 전망** (unlock-approx-3-5-hours-away-next-round-post-unlock).

## 데이터 신뢰도

**CoinGecko binance_futures**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS
확인. **BEAT·BICO·BSB·APEX·BTW·KAITO·CASHCAT·MMT·GIGGLE·PIPPIN·GRAM·CORE·CAP·AEON·BLESS·
ANSEM은 이번 회차도 명확히 미확인**(단순 미상장).

**CoinGecko bybit**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS·APEX 확인.
나머지는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·CAP·BICO 확인. ⚠️
**BEAT가 이번 회차 처음으로 배열에서 누락**돼 OKX 직접 API로 대체 집계했다(과거 여러 회차
정상 확보와 대비). ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT은 이번
회차도 okex_swap 배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM·BEAT)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인.
`oiUsd` 필드 직접 사용 방법론을 **28회차 연속** 유지, vol24_usd=`volCcy24h`×`last` 계산
방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️ **ACE-USDT-SWAP는 OKX에 instId
자체가 존재하지 않음**을 이번 회차도 직접 확인(에러코드 51001), okex_swap 미등재가
CoinGecko 집계 지연이 아니라 실제 미상장임이 재확인됐다. **GIGGLE**은 vol24h/volCcy24h
필드 순서역전이 **13회차 연속**, **KAITO**는 vol24h=volCcy24h 완전동일값 이상치가
**13회차 연속**, **GRAM**도 완전동일값이 **11회차 연속** 재현됐다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·
ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD 등 raw 정밀값 확보. BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·
BTW·BLESS·ANSEM은 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·
BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON 전량 확보(raw 정밀값). MMT·GIGGLE·
PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값). BTW는 이번 회차도 OrangeX에서 미발견(기존과
동일, Aster에서만 확인). KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·CORE는 여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.20M/OI $18.03M, ETH-USD $5.32M/OI $8.91M,
SOL-USD $0.14M/OI $4.56M) 확보.

**CoinGecko `/global`**: 재시도 후 총시총 $2,305,992,226,621.85(약 $2.306T)·BTC도미넌스
56.64%를 확인했다. 직전 회차($2.308T·56.67%)보다 시총·도미넌스 모두 소폭 하락,
**7회 연속** 안정적으로 확보됐다.

**Fear&Greed**: alternative.me API로 정상 응답, **31(Fear)** 확인 — **11회차 연속**
동일값.

**신규 발견**: (a) WebSearch로 ACE 8/10 언락의 실체가 확인됐다 — Early Investors 대상 약
1.8M ACE($199.15K, 공급 1.2%)에 불과한 소액 언락으로, 관측된 두 자릿수 낙폭 규모에 비해
실제 방출량은 작다. 이는 가격 압력이 언락 집행 자체보다 선반영성 매도·투기 포지셔닝에서
왔을 가능성을 시사한다(다만 인과관계를 확정하지는 않는다). (b) BEAT가 CoinGecko
okex_swap 배열에서 이번 회차 처음 누락됐다 — 데이터 결손인지 순간적 API 이슈인지는
다음 회차에서 재확인이 필요하다. (c) KAITO에서 가격(부분회복)과 펀딩(더 마이너스)이
반대 방향으로 움직이는 괴리가 관측됐다 — 파생 포지셔닝이 가격보다 선행하는 신호일
가능성이 있으나 단정하지 않는다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM·BEAT(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(28회차 연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은
본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상 스케일로
관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·
GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며,
이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·
HYNA:HYPE-USD·BLESS는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다; (h) ACE 언락은
WebSearch로 8/10, Early Investors 대상 약 1.8M ACE($199.15K·공급 1.2%)로 확인됐으나
정확한 UTC 집행 시각은 여전히 명시되지 않아 다음 회차에서 실제 집행 여부·시각을
재확인해야 한다; (i) BICO의 소스 간 격차가 이번 회차 -15~-17%로 더 좁혀졌으나 완전히
해소되지는 않았으며, 근본 원인(거래소별 집계 시차 등)은 규명하지 않았다; (j) KAITO
8/20 언락 규모는 소스별로 공급 3.3%(WebSearch 초기 결과)~7.63%(tokenomist)·$22.9M~
$34.68M로 편차가 있어 정확한 수치는 확정하지 않았다; (k) GIGGLE·KAITO의 필드 이상치가
13회차 연속, GRAM도 11회차 연속 재현돼 구조적 패턴으로 굳어졌으나 근본 원인(OKX API 자체
특성인지)은 규명하지 않았다; (l) HYNA:HYPE-USD의 OI가 소폭 변동을 이어가고 있으나, 이것이
완전한 정상화인지 추가 확인이 필요하다; (m) `/global`은 7회 연속 성공(이번엔 1회 재시도
필요)해 복구가 안정적으로 보이나 완전한 확정으로 단정하지는 않는다; (n) BEAT의 okex_swap
누락이 이번 회차 한정 이슈인지, 향후에도 재발할지는 다음 회차에서 재확인이 필요하다;
(o) ACE 언락(추정 3.5시간 앞)에 따른 변동성 확대 가능성을 배제할 수 없으며, 다음 회차가
언락 이후 첫 관측이 될 전망이다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
