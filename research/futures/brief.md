# 선물시장 스카우트 브리핑 — 2026-08-09 18:31 UTC (KST 2026-08-10 03:31)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-09T16:29:00Z)
> 로부터 정확히 2시간 경과, ACE 언락 예정(UTC 8/10 00:00 추정)까지 이제 약 5.5시간.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 이번 회차도 확보 성공 — 총시총 **$2,307,885,473,632.44(약 $2.308T)**·
BTC도미넌스 **56.67%**로 직전 회차($2.309T·56.65%)보다 시총 소폭 하락, 도미넌스 소폭 상승 —
**6회 연속** 안정적으로 확보됐다.

### Fear&Greed 31(Fear) — 10회차 연속 동일값

alternative.me API 정상 응답, **31(Fear)** — 10회차 연속 동일값 유지.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM·BICO 개별조회)는 **27회차 연속** 방법론(`oiUsd`
필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을 유지했다.

⚠️ **데이터소스 참고**: 이번 회차 CoinGecko `okex` id가 404/429로 반복 실패했으나, 정확한
거래소 id가 `okex_swap`임을 재확인해 BEAT·CORE·CAP·AEON·BSB·BICO(교차검증용)를 정상
확보했다 — 데이터 결손이 아니라 id 표기 문제였다. dYdX(`dydx_chain`)도 반복 429 이후 재시도로
확보 성공했다.

## 이번 회차 최대 사건

### ⚠️⚠️⚠️⚠️ ACE — 언락 약 5.5시간 앞, 낙폭이 오히려 완화

UTC 기준 8/10 00:00 추정 언락이 이제 약 5.5시간 앞으로 다가온 가운데, 직전 회차의 극심한
급락(가중 **-17.96%**)이 이번 회차 **오히려 완화**됐다: Binance **-10.961%**, Bybit
**-11.231%**(가중 **-11.021%**), OrangeX **-9.322%**, Aster **-10.758%**, Hyperliquid
**-10.265%**로 전 거래소 낙폭이 6~8%p씩 축소됐다. 여전히 두 자릿수 하락이 지속 중이나 언락
직전 낙폭이 진정되는 모습이며, 이것이 저점 형성인지 언락 집행 전 일시적 소강인지는 **다음
회차(언락 이후 첫 관측)**에서 확인이 필요하다. OKX 직접조회로 ACE-USDT-SWAP를 재확인한 결과
이번 회차도 instId 자체가 존재하지 않아 OKX 미상장이 재확인됐다.

### ⚠️ BICO — 4소스 처음으로 뚜렷하게 수렴

OKX 직접 **-22.844%**, CoinGecko okex_swap **-23.801%**, Aster **-22.451%**, OrangeX
**-22.547%**로 4개 소스 모두 **-22~-24%** 좁은 범위에 모였다(직전 -25~-29% 산개 대비 크게
개선). OI는 OKX $8.66M→**$8.49M(-2.0%)**로 소폭 감소.

## 직전 회차 강조 종목 추적 결과

- **① BEAT — ⚠️ 재가속 더 심화.** CoinGecko okex_swap **+27.352%**, OKX 직접
  **+29.464%**, Aster **+32.934%**, OrangeX **+33.247%**로 4소스 모두 27~33%대까지
  확대됐다(직전 27~29%대).
- **② ACE — ⚠️⚠️⚠️⚠️ 낙폭 오히려 완화.** 위 '이번 회차 최대 사건' 참조.
- **③ BICO — ⚠️ 4소스 뚜렷 수렴.** 위 '이번 회차 최대 사건' 참조.
- **④ BANK — 소스 간 엇갈림.** Binance/Bybit 가중 **+0.274%→+1.232%**로 소폭 반등, OrangeX는
  오히려 재냉각(**+2.512%→+0.976%**), Aster는 거의 유지(**+0.932%→+1.274%**) — 전체적으로
  손익분기 부근 횡보가 이어졌다.
- **⑤ KAITO — ⚠️⚠️ 부분회복 뒤집고 급재악화.** OKX 직접 **-1.459%→-7.038%**, Hyperliquid도
  동조(**-2.019%→-7.802%**). 펀딩도 더 마이너스로(OKX -0.271%→**-0.463%**, HL -0.102%→
  **-0.195%**) 이동해 숏 우위가 강해졌다. WebSearch로 8/20 대형 언락(공급 3.3%·$22.9M)이
  재확인됐고, 약 10.2일 앞으로 다가오며 사전 매도 압력이 다시 나타나는 정황이다.
- **⑥ CASHCAT — Robinhood 모멘텀 뚜렷이 추가 냉각.** HL **+24.497%→+18.411%**, OrangeX
  **+24.674%→+18.253%**, Aster **+26.552%→+18.840%**로 3거래소 모두 18%대에 좁게 수렴했다.

## 기타 주요 변화

**BLESS**는 여러 회차 이어진 재악화 후 **처음으로 완화 조짐**을 보였다(OrangeX
-15.619%→**-13.101%**, Aster -15.062%→**-13.323%**, 여전히 두 자릿수 하락 지속. WebSearch로
팀 물량 매도·MGBX 상장폐지·숏 청산 $4.45M 배경 확인). **AEON**은 3소스(OrangeX·Aster·OKX직접)
모두 동조 악화됐다(OrangeX -2.229%→**-6.426%**, Aster -1.935%→**-9.479%**, OKX직접
**-7.222%**). **AKE·CAP**은 개선 흐름이 지속됐다(AKE +2.819%→**+5.635%**, CAP
+6.023%→**+7.079%**). **BTW**는 고점(+16.509%) 이후 3회차 연속 냉각이 이어졌다
(+9.411%→**+4.777%**).

## 데이터 이슈 추적 결과

**HYNA:HYPE-USD**의 OI가 $694,915.90→**$696,608.11(+0.24%)**로 소폭 변동을 이어가며 프리징
해제 후 정상화 단계로 진입한 것으로 보인다. GIGGLE의 필드 순서역전이 **12회차 연속**,
KAITO(OKX 직접)의 완전동일값이 **12회차 연속**, GRAM의 완전동일값이 **10회차 연속**
재현됐다 — 세 이상치 모두 여전히 견고하다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️⚠️⚠️ 언락 5.5시간 앞, 낙폭 완화] | Binance/Bybit(가중) | $143.15M | $13.08M | +0.001% | -11.021% | -17.96%→-11.02%(가중). 전 거래소 6~8%p 완화, 저점형성 여부 다음회차 확인 필요 | unlock-hours-away-decline-eases-not-crash |
| **BICO** [⚠️ 4소스 수렴] | OKX(직접API) | $487.15M | $8.49M | -0.071% | -22.844% | CoinGecko -23.801%·Aster -22.451%·OrangeX -22.547%로 -22~-24% 수렴 | four-sources-converge-narrowly |
| **BEAT** [⚠️ 재가속 심화] | OKX(CoinGecko정상, okex_swap) | $405.19M | $13.04M | +0.005% | +27.352% | OKX직접 +29.464%·Aster +32.934%·OrangeX +33.247%로 27~33%대 확대 | reacceleration-deepens-27to33pct |
| **BANK** [소스 엇갈림] | Binance/Bybit(가중) | $115.41M | $18.72M | +0.005% | +1.232% | +0.274%→+1.232%. OrangeX는 재냉각, Aster는 거의 유지 | mixed-sources-hovers-near-breakeven |
| **KAITO** [⚠️⚠️ 급재악화] | OKX(직접API) | $113.93M | $7.99M | -0.463% | -7.038% | -1.459%→-7.038%, HL도 동조. 8/20 대형 언락 약 10.2일 앞 | sharp-relapse-reverses-partial-recovery |
| MMT [플러스 확대] | OKX(직접API) | $91.19M | $3.77M | -0.016% | +4.734% | +2.958%→+4.734% | extends-positive-turn |
| BSB [급악화 지속] | OKX(CoinGecko정상, okex_swap) | $6.52M | $2.62M | +0.005% | -9.768% | -8.436%→-9.768%, OKX직접·Aster·OrangeX -10%대 수렴 | sharp-worsening-continues |
| AAVE [거의 유지] | Binance/Bybit(가중) | $38.24M | $89.50M | +0.003% | -0.192% | +0.084%→-0.192% | roughly-flat-near-breakeven |
| ALLO [휩소 지속] | Binance/Bybit(가중) | $23.92M | $17.99M | +0.005% | -6.144% | -6.050%→-6.144% | whipsaw-continues-roughly-flat |
| ADA [11회차 마이너스] | Binance/Bybit(가중, USDT만) | $118.81M | $172.45M | +0.003% | -1.091% | -1.407%→-1.091% | eleventh-round-negative-roughly-flat |
| AKE [개선 지속] | Binance/Bybit(가중) | $42.12M | $39.86M | +0.042% | +5.635% | +2.819%→+5.635% | improves-further |
| GIGGLE [마이너스권 완화] | OKX(직접API) | $27.16M | $2.68M | +0.005% | -0.655% | -2.785%→-0.655%. ⚠️ 필드 이상치 12회차 연속 | eases-within-negative |
| PIPPIN [플러스 개선] | OKX(직접API) | $1.74M | $1.88M | +0.036% | +0.680% | +0.228%→+0.680% | mild-improvement-holds-positive |
| 1000RATS [플러스 확대] | Binance/Bybit(가중) | $14.10M | $18.48M | +0.028% | +5.890% | +0.081%→+5.890% | extends-positive-strongly |
| AIO [거의 유지] | Binance/Bybit(가중) | $9.76M | $4.35M | +0.044% | -3.340% | -4.318%→-3.340% | holds-negative-roughly-flat |
| GRAM [마이너스권 완화] | OKX(직접API) | $2.22M | $6.30M | +0.005% | -0.885% | -1.543%→-0.885%. ⚠️ 필드 이상치 10회차 연속 | eases-within-negative-vol-field-anomaly-tenth-round |
| AEON [⚠️ 뚜렷이 악화] | OKX(CoinGecko정상, okex_swap) | $28.81M | $3.76M | +0.005% | -6.514% | -1.196%→-6.514%, 전 소스 동조 악화 | worsens-notably-all-sources-align |
| ATOM [손익분기권 정체] | Binance/Bybit(가중) | $7.82M | $28.55M | +0.010% | +0.004% | +0.291%→+0.004% | flattens-near-breakeven |
| ASTER [손익분기권 정체] | Binance/Bybit(가중) | $14.95M | $113.81M | +0.005% | -0.079% | -1.020%→-0.079% | flattens-near-breakeven |
| CORE [소폭 냉각] | OKX(CoinGecko정상, okex_swap) | $1.74M | $1.02M | +0.010% | +2.006% | +4.081%→+2.006% | low-liquidity-mild-cooling |
| CAP [개선 지속] | OKX(CoinGecko정상, okex_swap) | $16.69M | $2.36M | +0.005% | +7.079% | +6.023%→+7.079% | improves-further |
| ALGO [거의 유지] | Binance/Bybit(가중) | $7.22M | $14.67M | -0.002% | -1.990% | -1.781%→-1.990% | stays-negative-roughly-flat |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [⚠️⚠️⚠️⚠️ 낙폭 완화] | Hyperliquid | $3.30M | $1.43M | -0.003% | -10.265% | -12.315%→-10.265% | decline-eases |
| **ACE-USDT-PERPETUAL** [⚠️⚠️⚠️⚠️ 낙폭 크게 완화] | OrangeX | $76.67M | $26.59M | +0.019% | -9.322% | -17.696%→-9.322% | decline-eases-sharply |
| **ACE-USDT** [낙폭 완화] | Aster | $0.52M | $0.07M | +0.001% | -10.758% | -18.851%→-10.758% | decline-eases |
| BEAT-USDT-PERPETUAL [재가속 심화] | OrangeX | $18.92M | $7.06M | -0.067% | +33.247% | +29.462%→+33.247% | reaccelerates-further |
| BEAT-USDT [재가속 심화] | Aster | $3.07M | $6.01M | +0.019% | +32.934% | +28.037%→+32.934% | reaccelerates-further |
| **BICO-USDT-PERPETUAL** [⚠️ 4소스 수렴] | OrangeX | $284.56M | $77.74M | +0.082% | -22.547% | -27.444%→-22.547%, 펀딩 재반전 | converges-with-others |
| **BICO-USDT** [⚠️ 4소스 수렴] | Aster | $4.28M | $0.32M | +0.001% | -22.451% | -28.917%→-22.451% | converges-with-others |
| **CASHCAT** [모멘텀 뚜렷이 냉각] | Hyperliquid | $18.79M | $21.83M | +0.026% | +18.411% | +24.497%→+18.411% | robinhood-momentum-cools-notably |
| CASHCAT-USDT-PERPETUAL [뚜렷이 냉각] | OrangeX | $0.14M | $0.05M | +0.075% | +18.253% | +24.674%→+18.253% | cools-notably |
| CASHCAT-USDT [뚜렷이 냉각] | Aster | $2.01M | $1.42M | +0.031% | +18.840% | +26.552%→+18.840% | cools-notably |
| ALLO-USDT [거의 유지] | Aster | $0.10M | $0.04M | +0.001% | -6.006% | -6.124%→-6.006% | roughly-flat |
| ALLO-USDT-PERPETUAL [소폭 악화] | OrangeX | $16.82M | $5.74M | +0.010% | -6.727% | -5.753%→-6.727% | mild-worsening |
| AAVE-USDT-PERPETUAL [마이너스 전환] | OrangeX | $22.01M | $7.86M | +0.010% | -0.219% | +0.120%→-0.219% | turns-negative-near-breakeven |
| AAVE-USDT [손익분기 근접] | Aster | $0.24M | $4.67M | +0.010% | -0.088% | -0.033%→-0.088% | near-breakeven |
| AAVE-USD [손익분기 부근] | Hyperliquid | $2.21M | $60.10M | +0.001% | -0.204% | -0.004%→-0.204% | near-breakeven |
| ADA-USDT-PERPETUAL [거의 유지] | OrangeX | $66.54M | $22.46M | +0.010% | -1.101% | -1.399%→-1.101% | roughly-flat-negative |
| ADA-USDT [소폭 악화] | Aster | $0.14M | $1.50M | +0.010% | -1.298% | -1.001%→-1.298% | mild-worsening |
| ADA-USD [거의 유지] | Hyperliquid | $1.60M | $32.88M | +0.001% | -1.106% | -1.350%→-1.106% | roughly-flat-negative |
| BANK-USDT-PERPETUAL [재냉각] | OrangeX | $7.68M | $2.81M | -0.023% | +0.976% | +2.512%→+0.976% | cools-again |
| BANK-USDT [거의 유지] | Aster | $0.50M | $0.31M | +0.001% | +1.274% | +0.932%→+1.274% | roughly-flat |
| AKE-USDT-PERPETUAL [개선 지속] | OrangeX | $6.27M | $2.19M | +0.041% | +5.962% | +2.678%→+5.962% | improves-further |
| AKE-USDT [개선 지속] | Aster | $0.63M | $11.53M | +0.015% | +5.105% | +3.196%→+5.105% | improves-further |
| CAP-USDT [거의 유지] | Aster | $0.03M | $0.11M | +0.001% | +6.855% | +6.512%→+6.855% | roughly-flat-positive |
| CAP-USDT-PERPETUAL [개선] | OrangeX | $0.47M | $0.17M | +0.010% | +7.172% | +4.767%→+7.172% | improves |
| ALGO-USDT-PERPETUAL [거의 유지] | OrangeX | $4.48M | $1.64M | -0.010% | -1.945% | -1.712%→-1.945% | roughly-flat |
| ALGO-USDT [초저유동성] | Aster | $0.002M | $0.03M | +0.001% | -1.967% | -1.818%→-1.967% | low-liquidity-roughly-flat |
| ALGO-USD [소폭 악화] | Hyperliquid | $0.55M | $1.95M | +0.001% | -2.058% | -1.976%→-2.058% | mild-worsening |
| ATOM-USDT-PERPETUAL [손익분기 전환] | OrangeX | $4.62M | $1.67M | +0.010% | -0.072% | +0.289%→-0.072% | flattens-near-breakeven |
| ATOM-USDT [플러스 전환] | Aster | $0.02M | $1.60M | +0.010% | +0.145% | -0.072%→+0.145% | turns-positive |
| ATOM-USD [손익분기권] | Hyperliquid | $0.16M | $1.93M | +0.001% | +0.087% | +0.303%→+0.087% | near-breakeven |
| ASTER-USDT-PERPETUAL [손익분기권 정체] | OrangeX | $6.58M | $2.23M | +0.010% | -0.051% | -0.887%→-0.051% | flattens-near-breakeven |
| ASTER-USDT [대형 OI 손익분기 근접] | Aster | $8.98M | $220.88M | +0.033% | -0.016% | OI $219.69M→$220.88M | large-oi-holds-near-breakeven |
| ASTER-USD [손익분기권 정체] | Hyperliquid | $0.45M | $14.36M | +0.001% | -0.056% | -1.021%→-0.056% | flattens-near-breakeven |
| KAITO-USD [⚠️⚠️ 급재악화] | Hyperliquid | $24.82M | $15.99M | -0.195% | -7.802% | -2.019%→-7.802%. 8/20 언락 약 10.2일 앞 | sharp-relapse-aligns-with-okx |
| GRAM-USD [마이너스권 완화] | Hyperliquid | $0.42M | $12.86M | +0.001% | -1.089% | -1.448%→-1.089% | eases-matches-okx |
| HYPE-USD [소폭 악화] | Hyperliquid | $66.44M | $1,195.08M | 0.000% | -0.248% | -0.015%→-0.248% | mild-worsening |
| HYPER-USD [거의 유지] | Hyperliquid | $0.10M | $0.31M | +0.001% | +0.091% | +0.215%→+0.091% | roughly-flat |
| APEX-USD [개선] | Hyperliquid | $0.08M | $0.78M | +0.001% | +1.237% | +0.579%→+1.237%, Bybit도 근접 | improves-bybit-matches |
| FARTCOIN [재가속 지속] | Hyperliquid | $5.32M | $23.74M | +0.002% | +4.614% | +2.519%→+4.614% | extends-reacceleration |
| ETHFI-USD [소폭 냉각] | Hyperliquid | $0.52M | $8.59M | +0.001% | +1.090% | +2.599%→+1.090% | mild-cooling |
| ETH-USD [플러스권 유지] | dYdX | $5.29M | $8.94M | 0.000% | +0.109% | +0.026%→+0.109% | holds-positive |
| BTC-USD [플러스 유지, 소폭 냉각] | dYdX | $1.15M | $18.03M | 0.000% | +0.143% | +0.263%→+0.143% | holds-positive-mild-cooling |
| SOL-USD [개선] | dYdX | $0.16M | $4.55M | 0.000% | +1.366% | +1.087%→+1.366% | improves |
| ANSEM [소폭 악화] | Aster | $0.24M | $0.91M | +0.001% | -6.103% | -2.723%→-6.103% | mild-worsening |
| ANSEM-USDT-PERPETUAL [거의 유지] | OrangeX | $0.46M | $0.16M | +0.010% | -6.766% | -6.759%→-6.766% | roughly-flat |
| **BTW** [3회차 연속 냉각] | Aster | $2.72M | $14.65M | +0.034% | +4.777% | +9.411%→+4.777%(고점 +16.509%) | cools-third-round-from-peak |
| HYNA:PUMP-USD [거의 유지] | Hyperliquid | $0.04M | $0.17M | +0.001% | +12.285% | +12.542%→+12.285% | roughly-flat |
| **HYNA:HYPE-USD** [OI 소폭 이어지는 변동] | Hyperliquid | $0.14M | $0.70M | +0.008% | +0.155% | OI $694,916→$696,608(+0.24%) — 정상화 단계 | oi-continues-small-moves-normalizing |
| AEON-USDT-PERPETUAL [⚠️ 뚜렷이 악화] | OrangeX | $0.49M | $0.15M | +0.010% | -6.426% | -2.229%→-6.426% | worsens-notably-aligns-with-okx |
| AEON-USDT [⚠️ 최대 악화] | Aster | $0.09M | $0.22M | +0.001% | -9.479% | -1.935%→-9.479% | largest-worsening-of-all-venues |
| **BSB-USDT-PERPETUAL** [급악화 지속] | OrangeX | $13.05M | $4.27M | +0.010% | -9.994% | -9.550%→-9.994% | sharp-worsening-continues |
| **BSB-USDT** [급악화 지속] | Aster | $0.05M | $0.10M | +0.001% | -10.112% | -7.759%→-10.112% | sharp-worsening-continues |
| 1000RATS-USDT [플러스 확대] | Aster | $0.09M | $0.04M | +0.019% | +4.496% | +0.114%→+4.496%, CEX와 방향 일치 | extends-positive-aligns-with-cex |
| **BLESS** [⚠️ 첫 완화 조짐] | OrangeX | $95.00M | $29.71M | +0.065% | -13.101% | -15.619%→-13.101% | first-easing-after-multi-round-relapse |
| **BLESS-USDT** [⚠️ 첫 완화 조짐] | Aster | $0.32M | $0.22M | +0.006% | -13.323% | -15.062%→-13.323%, OrangeX와 근접 | first-easing-matches-orangex |

## 테마 태그

1. **시장 전반: `/global`이 6회 연속 확보 성공 — 총시총 $2.308T·BTC도미넌스 56.67%(시총 소폭 하락, 도미넌스 소폭 상승)** (global-api-sixth-consecutive-success).
2. **Fear&Greed 31(Fear) 10회차 연속 동일값 유지** (fear-greed-holds-31-tenth-consecutive-round).
3. **⚠️⚠️⚠️⚠️ ACE: 언락(약 5.5시간 앞)을 앞두고 직전 회차의 극심한 급락(가중 -17.96%)이 오히려 완화(-11.02%). 전 거래소 낙폭 6~8%p 축소. 저점형성인지 언락 전 소강인지 다음 회차 확인 필요. OKX 미상장 재확인** (ace-decline-eases-hours-before-unlock).
4. **⚠️ BICO: 4소스(OKX직접·CoinGecko·Aster·OrangeX)가 -22~-24% 범위로 처음 뚜렷하게 수렴** (bico-four-sources-converge-narrowly).
5. **⚠️ BEAT: 재가속이 더 심화돼 4소스 모두 27~33%대까지 확대** (beat-reacceleration-deepens).
6. **⚠️⚠️ KAITO: 부분회복을 뒤집고 OKX·HL 두 소스 모두 급재악화, 펀딩도 더 마이너스로. 8/20 대형 언락(공급 3.3%·$22.9M) 약 10.2일 앞 사전매도 정황 재확인** (kaito-sharp-relapse-ahead-of-large-unlock).
7. **BANK: 소스 간 엇갈림 — Binance/Bybit 소폭 반등, OrangeX는 재냉각, Aster 거의 유지. 손익분기 부근 횡보 지속** (bank-mixed-sources-hovers-near-breakeven).
8. **CASHCAT: Robinhood 리스팅 모멘텀이 3거래소 모두 뚜렷이 추가 냉각(24~27%대→18%대 좁게 수렴)** (cashcat-robinhood-momentum-cools-notably).
9. **⚠️ BLESS: 여러 회차 이어진 재악화 후 처음 완화 조짐(-15%대→-13%대), 여전히 두 자릿수 하락 지속** (bless-first-easing-after-multi-round-relapse).
10. **⚠️ AEON: 3소스(OrangeX·Aster·OKX직접) 모두 동조 악화 — 마이너스 폭 크게 확대** (aeon-worsens-notably-all-sources-align).
11. **AKE·CAP: 개선 흐름 지속** (ake-cap-improve-further).
12. **BTW: 고점(+16.509%) 이후 3회차 연속 냉각 지속** (btw-cools-third-round-from-peak).
13. **HYNA:HYPE-USD: OI가 소폭 변동을 이어가며(+0.24%) 프리징 해제 후 정상화 단계로 보임** (hyna-hype-oi-normalizing).
14. **⚠️ 데이터소스 참고: CoinGecko `okex` id가 이번 회차 반복 실패(404/429)했으나 정확한 id `okex_swap`으로 BEAT·CORE·CAP·AEON·BSB·BICO 정상 확보 — 데이터 결손이 아니라 id 표기 이슈였음** (okex-id-correction-okex-swap).
15. **⚠️ GIGGLE 필드 이상치 12회차 연속, KAITO(OKX 직접) 완전동일값 이상치 12회차 연속, GRAM도 10회차 연속 재현** (field-anomalies-twelfth-tenth-round-continue).
16. **OKX ACE·BANK·1000RATS·AIO·KAITO·MMT·PIPPIN·GIGGLE·GRAM은 이번 회차도 okex_swap 미등재(ACE는 instId 자체 부재), 직접 API/DEX로 보강. BEAT·BICO·AEON·BSB·CAP·CORE는 okex_swap 정상** (okx-most-still-not-listed-direct-api-supplements).
17. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
18. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
19. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
20. **ACE 언락 예정(UTC 8/10 00:00 추정)까지 약 5.5시간 — 다음 회차가 언락 이후 첫 관측이 될 전망** (unlock-approx-5-5-hours-away-next-round-post-unlock).

## 데이터 신뢰도

**CoinGecko binance_futures**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS
확인. **BEAT·BICO·BSB·APEX·BTW·KAITO·CASHCAT·MMT·GIGGLE·PIPPIN·GRAM·CORE·CAP·AEON·BLESS·
ANSEM은 이번 회차도 명확히 미확인**(단순 미상장).

**CoinGecko bybit**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS·APEX 확인.
나머지는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: 이번 회차 `okex` id가 404/429로 반복 실패해 정확한 id(`okex_swap`)로
재시도, 최종 확보 성공 — AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·CAP·**BEAT·BICO** 확인.
BICO -23.801%가 OKX 직접조회 -22.844%·Aster -22.451%·OrangeX -22.547%와 좁게 수렴해 데이터
정합성이 재확인됐다. ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT은 이번
회차도 okex_swap 배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM·BICO·BEAT·CORE·BSB·AEON·CAP)**: `market/ticker`
(개별)+`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접
확인. `oiUsd` 필드 직접 사용 방법론을 **27회차 연속** 유지, vol24_usd=`volCcy24h`×`last`
계산 방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️ **ACE-USDT-SWAP는 OKX에
instId 자체가 존재하지 않음**을 이번 회차도 직접 확인, okex_swap 미등재가 CoinGecko 집계
지연이 아니라 실제 미상장임이 재확인됐다. **GIGGLE**은 vol24h/volCcy24h 필드 순서역전이
**12회차 연속**, **KAITO**는 vol24h=volCcy24h 완전동일값 이상치가 **12회차 연속**, **GRAM**도
완전동일값이 **10회차 연속** 재현됐다. MMT·PIPPIN은 volCcy24h가 vol24h보다 약 10배 큰 필드
관계를 계속 유지(vol24_usd 계산에는 영향 없음).

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·
ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD 등 raw 정밀값 확보. BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·
BTW·BLESS·ANSEM은 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·
BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON 전량 확보(raw 정밀값). MMT·GIGGLE·
PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값). BTW는 이번 회차도 OrangeX에서 미발견(기존과
동일, Aster에서만 확인). KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·CORE는 여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.15M/OI $18.03M, ETH-USD $5.29M/OI $8.94M,
SOL-USD $0.16M/OI $4.55M) 확보. 여러 차례 429 이후 재시도로 확보 성공.

**CoinGecko `/global`**: 직접 API로 총시총 $2,307,885,473,632.44(약 $2.308T)·BTC도미넌스
56.67%를 확인했다. 직전 회차($2.309T·56.65%)보다 시총 소폭 하락·도미넌스 소폭 상승,
**6회 연속** 안정적으로 확보됐다.

**Fear&Greed**: alternative.me API로 정상 응답, **31(Fear)** 확인 — **10회차 연속** 동일값.

**신규 발견**: (a) CoinGecko `okex` id는 이번 회차 404/429로 완전히 실패했으나, 정확한 id가
`okex_swap`임을 재확인해 데이터를 정상 확보했다 — 과거 회차들도 실제로는 `okex_swap` id를
사용했을 가능성이 높으며, 이번 실패는 데이터 결손이 아니라 순간적 id/레이트리밋 이슈였다.
(b) BICO에서 이번 회차 4소스(OKX직접·CoinGecko·Aster·OrangeX)가 -22~-24% 범위로 처음 뚜렷하게
수렴했다 — 지난 여러 회차 이어진 소스 간 격차가 상당히 좁혀졌다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM·BICO·BEAT·CORE·
BSB·AEON·CAP(OKX 직접 조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는
API의 `oiUsd` 필드를 직접 채택(27회차 연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·
BANK·ALLO·AIO·1000RATS·ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균
계산값이며, 개별 거래소 값은 본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding
필드가 이번 회차도 정상 스케일로 관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·
CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아
OKX·DEX로만 집계되는 구조이며, 이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·
ANSEM·HYNA:PUMP-USD·HYNA:HYPE-USD·BLESS는 DEX에서만 상장이 확인돼 해당 섹션에서만
집계했다; (h) ACE의 언락은 아직 UTC 8/10 00:00으로 추정되는 예정 시각이며, 정확한 집행
시각·수량은 tokenomist.ai에서도 명시되지 않아 다음 회차에서 실제 집행 여부·시각을 재확인해야
한다; (i) BICO의 소스 간 격차가 이번 회차 크게 좁혀졌으나 완전히 해소되지는 않았으며(-22~
-24% 범위 내에서도 최대 1.4%p 차이), 근본 원인(거래소별 집계 시차 등)은 규명하지 않았다;
(j) ACE 언락 관련 tokenomist·WebSearch 소스로 8/10 Early Investors 배분을 여러 회차에
걸쳐 재확인했으나, 정확한 토큰 수량·집행 시각까지는 명시되지 않았다; (k) GIGGLE·KAITO의
필드 이상치가 12회차 연속, GRAM도 10회차 연속 재현돼 구조적 패턴으로 완전히 굳어졌으나
근본 원인(OKX API 자체 특성인지)은 규명하지 않았다; (l) HYNA:HYPE-USD의 OI가 소폭 변동을
이어가고 있으나, 이것이 완전한 정상화인지 추가 확인이 필요하다; (m) `/global`은 6회 연속
성공해 복구가 안정적으로 보이나 완전한 확정으로 단정하지는 않는다; (n) CoinGecko `okex` id
실패 후 `okex_swap`으로 전환한 것이 이번 회차 한정 조치인지, 향후 회차에도 `okex_swap`을
기본으로 써야 하는지는 다음 회차에서 재확인이 필요하다; (o) ACE 언락(추정 5.5시간 앞)에
따른 변동성 확대 가능성을 배제할 수 없으며, 이번 회차 관측된 낙폭 완화가 실제 안정화인지
언락 직전 유동성 저하에 따른 일시적 현상인지는 다음 회차에서 판가름날 전망이다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
