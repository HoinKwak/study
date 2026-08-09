# 선물시장 스카우트 브리핑 — 2026-08-09 08:29 UTC (KST 2026-08-09 17:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-09T06:29:00Z)
> 로부터 정확히 2시간 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 이번 회차 **마침내 성공**했다 — 8회 연속 429 실패를 끊고 총시총
**$2,298,263,635,528.73(약 $2.30T)**·BTC도미넌스 **56.61%**를 직접 API로 확보했다. 직전
회차 WebSearch 참고치($2.29T·56.8%)와 거의 일치해, 그간 회차마다 오락가락했던 WebSearch
스니펫이 실제로 근사치를 반영했을 가능성을 보여준다(캐시 의심을 완전히 해소하진 않지만
이번엔 정합).

### Fear&Greed 31(Fear) — 5회차 연속 동일값

alternative.me API 정상 응답, **31(Fear)** — 5회차 연속 동일값 유지.

### 데이터 확보 상황

binance_futures·bybit·hyperliquid·okex_swap·aster·orangex_futures는 **1차 시도로 정상
확보**됐고, dydx_chain은 3차·global은 2차 재시도 끝에 확보됐다(직전 회차보다 429 빈도가
전반적으로 완화된 정황). OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)는 **22회차 연속**
방법론(`oiUsd` 필드 직접 사용, `vol24_usd=volCcy24h×last`)을 유지해 확보했다.

지금은 **일요일 밤**(UTC 08:29, KST 17:29) 시간대다.

## 직전 회차 강조 종목 추적 결과 (요청 항목 전체)

- **① ACE(Fusionist) — ⚠️⚠️⚠️ 언락 직전 4거래소 전부 강하게 재가속으로 급반전.** 언락(8/10
  00:00 UTC 추정, 공급 1.2%)을 WebSearch로 재확인한 결과 여전히 '예정' 상태로 미집행이었다.
  Binance/Bybit(가중) **+17.14%→+23.80%**, OrangeX **+18.95%→+24.38%**, Aster
  **+17.88%→+25.29%**, HL **+16.38%→+23.87%**로 4거래소 전부 직전 2회차 이어지던 냉각
  흐름을 완전히 뒤집었다. OI는 OrangeX **+8.2%**($48.14M→$52.09M)·HL +2.5%로 증가한 반면
  Aster -8.5%·Binance/Bybit 가중 -3.4%로 감소해 방향은 엇갈렸다. 언락 직전 투기적
  포지셔닝일 가능성이 있으나(확정 아님) 원인은 확정하지 않는다.
- **② BEAT — Binance BEATUSDT가 12회차만에 처음 확인됐다**(vol $4.49M, OI $7.63M, chg
  +49.771%). OKX는 **+47.998%→+48.539%**로 거의 평탄해, 3회 요요 이후 고점권 유지 국면으로
  전환된 것일 수 있다. OrangeX(+42.384%→**+49.647%**)·Aster(+42.898%→**+48.478%**)는 추가
  상승을 이어갔다. Bybit BEAT는 여전히 미확인.
- **③ BICO** — OKX **+20.069%→+15.552%**(OI -29.2% 큰 폭 감소), OrangeX
  **+20.0%→+16.058%**(OI -5.4%, 3회차 연속 감소)로 두 거래소는 냉각한 반면 Aster는
  +14.489%→**+21.019%**로 오히려 재가속해, 직전 회차와 정반대 방향으로 거래소 간 갈림이
  이어졌다(주도 거래소가 뒤바뀜).
- **④ BSB — ⚠️⚠️ 안정화를 넘어 3거래소 전부 플러스로 전환됐다.** OKX
  **-2.226%→+2.748%**, OrangeX **-1.657%→+2.744%**, Aster **-1.009%→+2.565%**로 '사실상
  안정화'에서 '플러스 반전'으로 국면이 바뀌었다.
- **⑤ BLESS — ⚠️⚠️⚠️ 안정화 기대와 달리 심화되던 낙폭이 이번엔 급격히 축소됐다.** OrangeX
  **-32.66%→-13.732%**(낙폭 절반 이하), Aster **-37.697%→-11.07%**(낙폭 3분의 1 수준)로
  둘 다 강한 되돌림을 보였다. 여전히 마이너스지만 3회차 심화 흐름이 크게 반전됐다(OI OrangeX
  +2.8%·Aster +9.6%).
- **⑥ CASHCAT — ⚠️⚠️ 3회차 이어지던 냉각이 끊기고 3거래소 전부 강하게 재가속했다.** HL
  **+14.528%→+22.087%**, OrangeX **+14.407%→+22.664%**, Aster **+14.238%→+22.968%**.
  직전 회차 온체인 관측(h24 +15.9%→+20.74% 재가속)과 방향이 이번엔 일치해, 선물이 그
  재가속을 뒤따른 것으로 보인다.
- **⑦ KAITO** — 개선 흐름이 3회차 연속 이어졌다(OKX 직접 **-11.030%→-7.354%**, HL
  **-11.352%→-7.719%**). 펀딩도 함께 개선(OKX -0.571%→**-0.429%**, HL -0.277%→**-0.169%**).
  OI는 OKX +0.4%(거의 유지)·HL -4.2%(소폭 감소). 8/20 대형 언락 약 11일 앞.

## 데이터 이슈 추적 결과

GIGGLE의 vol24h/volCcy24h 필드 순서역전(이번은 85.47M>0.85M)이 **7회차 연속**, KAITO(OKX
직접)의 vol24h=volCcy24h 완전동일값(이번 221,508,151=221,508,151)이 **7회차 연속**,
GRAM의 완전동일값(이번 1,771,954=1,771,954)이 **5회차 연속** 재현됐다 — 구조적 패턴으로
완전히 굳어졌다. ⚠️ **HYNA:HYPE-USD는 직전 회차 '갱신 재개'로 판단했으나, 이번 회차 OI가
다시 정확히 동일값(724,950.96=724,950.96)으로 관측됐다** — vol·chg24는 변했으나
(31,300.68→31,186.97, +0.619%→+0.682%) OI 필드만 재차 고정된 것으로 보여, 직전의
'정상화' 판단이 성급했을 가능성이 있다.

## 이번 회차 그 외 주요 변화

**BANK**는 4회차 이어지던 개선 흐름이 이번엔 크게 꺾여 **-1.937%→-6.319%**로 악화, 펀딩도
-0.023%→**-0.141%**로 크게 나빠졌다(8/17 언락 약 8일 앞). **AIO**는 직전 회차 플러스
전환됐다가 이번 회차 다시 **-5.257%**로 마이너스 반전(플립플롭 지속). **1000RATS**는
-2.407%→**+0.664%**로 플러스 전환. **BTW**는 반전이 더 확장돼 +16.288%→**+28.936%**(펀딩
0.018%→0.058%로 상승, OI는 거의 유지로 전환). **AEON**은 OKX·OrangeX 모두 첫 뚜렷한
냉각(+16.686%→+10.717%, +16.298%→+10.449%)을 보였고, Aster AEON은 이번 회차 재확인에
실패했다. **AKE**는 Bybit 데이터가 1회 미확인 뒤 재등장했다(OI 급증처럼 보이는 것은 실제
증가가 아니라 Bybit 재포함 효과).

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️⚠️ 언락 직전 급반전 재가속] | Binance/Bybit(가중) | $272.85M | $13.79M | -0.055% | +23.798% | +17.14%→+23.80%, 4거래소 전부 재가속 | unlock-imminent-reverses-to-broad-reacceleration |
| **BEAT** [고점권 유지, Binance 첫 확인] | OKX(CoinGecko 정상) | $445.70M | $12.23M | +0.005% | +48.539% | 거의 평탄, Binance 12회차만에 확인 | holds-near-peak-binance-listing-confirmed-first-time |
| **BICO** [주도 거래소 뒤바뀜] | OKX(CoinGecko 정상) | $481.42M | $14.98M | -0.413% | +15.552% | OKX·OrangeX 냉각, Aster는 재가속 | mixed-directional-split-flips-leader |
| **BSB** [⚠️⚠️ 플러스 전환] | OKX(CoinGecko 정상) | $9.48M | $2.88M | +0.005% | +2.748% | -2.226%→+2.748%, 3거래소 전부 전환 | turns-positive-across-all-venues |
| AAVE [소폭 재가속] | Binance/Bybit(가중) | $42.42M | $89.72M | +0.008% | +1.352% | +1.238%→+1.352% | mild-reacceleration |
| ALLO [5회차 마이너스, 개선] | Binance/Bybit(가중) | $33.35M | $18.59M | +0.005% | -2.548% | -4.534%→-2.548% | stays-negative-fifth-round-improves |
| ADA [6회차 마이너스, 악화] | Binance/Bybit(가중, USDT만) | $107.75M | $172.56M | +0.007% | -0.891% | -0.3725%→-0.891% | stays-negative-sixth-round-mild-deterioration |
| **BANK** [⚠️ 개선흐름 꺾여 악화] | Binance/Bybit(가중) | $63.57M | $19.11M | -0.141% | -6.319% | -1.937%→-6.319%. 8/17 언락 약 8일 앞 | breaks-improvement-streak-sharp-deterioration |
| AKE [개선, Bybit 재등장] | Binance/Bybit(가중) | $34.58M | $38.54M | +0.044% | -1.170% | -1.404%→-1.170%. 8/21 언락 약 12일 앞 | improves-bybit-data-reappears-oi-jump-is-inclusion-effect |
| KAITO [개선 3회차, 펀딩도 개선] | OKX(직접API) | $151.80M(계산값) | $8.14M | -0.429% | -7.354% | -11.030%→-7.354%. 8/20 대형 언락 약 11일 앞 | improves-third-round-funding-also-improves-vol-anomaly-seventh-round |
| MMT [개선] | OKX(직접API) | $163.00M(계산값) | $4.99M | -0.002% | -0.384% | -1.739%→-0.384% | improves-after-reversal-stays-near-neutral |
| GIGGLE [소폭 냉각] | OKX(직접API) | $29.91M(계산값) | $2.81M | +0.005% | +7.728% | +9.664%→+7.728%. ⚠️ 필드 순서역전 7회차 연속 | mild-cooling-field-order-anomaly-seventh-round |
| PIPPIN [소폭 냉각] | OKX(직접API) | $2.00M(계산값) | $1.86M | +0.027% | +1.706% | +3.349%→+1.706% | mild-cooling |
| 1000RATS [플러스 전환] | Binance/Bybit(가중) | $12.02M | $18.63M | +0.013% | +0.664% | -2.407%→+0.664% | turns-positive |
| **AIO** [⚠️ 다시 마이너스, 플립플롭] | Binance/Bybit(가중) | $9.60M | $4.29M | +0.044% | -5.257% | +0.213%→-5.257% | reverses-negative-again-whipsaw |
| GRAM [소폭 악화] | OKX(직접API) | $2.38M(계산값) | $6.33M | +0.005% | -0.813% | -0.443%→-0.813%. ⚠️ vol 필드 동일값 이상치 5회차 연속 | holds-negative-slightly-worsens-vol-field-anomaly-fifth-round |
| AEON [첫 뚜렷한 냉각] | OKX(CoinGecko 정상) | $32.52M | $4.16M | +0.005% | +10.717% | +16.686%→+10.717% | first-clear-cooling-aster-unconfirmed |
| ATOM [소폭 냉각] | Binance/Bybit(가중) | $11.41M | $28.50M | +0.003% | +0.181% | +0.25%→+0.181% | mild-cooling |
| ASTER [소폭 개선] | Binance/Bybit(가중) | $17.44M | $113.23M | +0.003% | -0.053% | -0.169%→-0.053% | mild-improvement-stays-negative |
| CORE [초저유동성, 소폭 냉각] | OKX(CoinGecko 정상) | $1.45M | $0.99M | +0.005% | +3.566% | +4.212%→+3.566% | low-liquidity-mild-cooling |
| CAP [재가속 후 냉각] | OKX(CoinGecko 정상) | $19.93M | $2.43M | +0.005% | +6.837% | +8.641%→+6.837% | cools-after-sharp-reacceleration |
| ALGO [4회차 연속, 개선] | Binance/Bybit(가중) | $6.59M | $14.69M | -0.008% | -0.191% | -0.849%→-0.191% | fourth-round-tracked-improves |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [⚠️⚠️⚠️ 언락 직전 재가속] | Hyperliquid | $5.41M | $1.74M | -0.015% | +23.868% | +16.38%→+23.87% | unlock-imminent-sharp-reacceleration |
| **ACE-USDT-PERPETUAL** [재가속, OI 반등] | OrangeX | $155.64M | $52.09M | -0.184% | +24.383% | OI +8.2% | reaccelerates-oi-rebounds |
| ACE-USDT [재가속, OI 감소전환] | Aster | $0.78M | $0.08M | -0.019% | +25.292% | OI -8.5% | reaccelerates-oi-turns-lower |
| **BEAT-USDT-PERPETUAL** [추가 상승] | OrangeX | $18.74M | $7.32M | +0.034% | +49.647% | +42.384%→+49.647% | extends-gain |
| **BEAT** [추가 상승] | Aster | $5.95M | $5.54M | +0.015% | +48.478% | +42.898%→+48.478% | extends-gain |
| **BICO-USDT-PERPETUAL** [냉각 전환] | OrangeX | $303.27M | $104.84M | -0.928% | +16.058% | OI -5.4%(3회차 감소) | turns-cooling-oi-declines-third-round |
| BICO-USDT [⚠️ 반대로 재가속] | Aster | $2.80M | $0.54M | -0.002% | +21.019% | OI -16.6%로 가격과 엇갈림 | diverges-reaccelerates-against-other-venues |
| **CASHCAT** [⚠️⚠️ 냉각 끊고 재가속] | Hyperliquid | $12.65M | $16.94M | +0.010% | +22.087% | +14.528%→+22.087% | breaks-cooling-streak-reaccelerates-aligns-with-onchain |
| **CASHCAT-USDT-PERPETUAL** [재가속, 펀딩 완화] | OrangeX | $0.15M | $0.05M | +0.010% | +22.664% | 펀딩 0.126%→0.01% | reaccelerates-oi-continues-declining |
| CASHCAT-USDT [재가속] | Aster | $1.48M | $1.23M | -0.011% | +22.968% | 펀딩 마이너스 유지 | reaccelerates-funding-stays-negative |
| ALLO-USDT [소폭 악화] | Aster | $0.14M | $0.04M | +0.001% | -2.716% | -4.37%→-2.716% | mild-deterioration |
| ALLO-USDT-PERPETUAL [개선, OI 반등] | OrangeX | $22.93M | $8.12M | +0.010% | -2.507% | OI +5.7%(6회차 감소흐름 반전) | improves-oi-rebounds |
| AAVE-USDT-PERPETUAL [소폭 재가속] | OrangeX | $25.52M | $9.05M | +0.010% | +1.452% | +1.285%→+1.452% | mild-reacceleration |
| AAVE-USDT [소폭 냉각] | Aster | $0.16M | $4.55M | +0.010% | +1.205% | +1.297%→+1.205% | mild-cooling |
| AAVE-USD [소폭 재가속] | Hyperliquid | $2.76M | $60.63M | +0.001% | +1.49% | +1.309%→+1.49% | mild-reacceleration |
| ADA-USDT-PERPETUAL [소폭 악화] | OrangeX | $57.45M | $19.64M | +0.010% | -0.902% | -0.7%→-0.902% | mild-deterioration |
| ADA-USDT [악화] | Aster | $0.13M | $1.52M | +0.010% | -1.15% | -0.35%→-1.15% | deteriorates |
| ADA-USD [악화] | Hyperliquid | $1.61M | $33.06M | +0.0% | -0.813% | -0.425%→-0.813% | deteriorates |
| **BANK-USDT-PERPETUAL** [⚠️ 크게 악화] | OrangeX | $6.64M | $1.94M | -0.010% | -6.116% | -2.132%→-6.116% | sharply-deteriorates |
| **BANK-USDT** [⚠️ 크게 악화, 펀딩 마이너스 심화] | Aster | $0.32M | $0.34M | -0.063% | -6.341% | 펀딩 -0.002%→-0.063% | sharply-deteriorates-funding-deeply-negative |
| AKE-USDT-PERPETUAL [개선] | OrangeX | $6.80M | $2.41M | +0.042% | -0.325% | -2.007%→-0.325% | improves |
| AKE-USDT [개선] | Aster | $0.53M | $11.10M | +0.027% | -1.029% | -2.072%→-1.029% | improves |
| CAP-USDT [재가속 후 냉각] | Aster | $0.06M | $0.11M | +0.001% | +6.485% | +10.229%→+6.485% | cools-after-reacceleration |
| CAP-USDT-PERPETUAL [재가속 후 냉각] | OrangeX | $0.50M | $0.20M | +0.010% | +7.03% | +8.922%→+7.03% | cools-after-reacceleration |
| ALGO-USDT-PERPETUAL [개선] | OrangeX | $4.01M | $1.39M | +0.010% | -0.23% | -0.687%→-0.23% | improves |
| ALGO-USDT [대체로 유지] | Aster | $0.0002M | $0.03M | +0.001% | -0.675% | -0.995%→-0.675% | roughly-holds-low-liquidity |
| ALGO-USD [개선] | Hyperliquid | $0.43M | $2.09M | +0.001% | -0.022% | -0.936%→-0.022% | improves-near-breakeven |
| ATOM-USDT-PERPETUAL [소폭 재가속] | OrangeX | $5.89M | $2.14M | -0.010% | +0.291% | +0.218%→+0.291% | mild-reacceleration |
| ATOM-USDT [소폭 냉각, 플러스권] | Aster | $0.02M | $1.59M | +0.010% | +0.365% | +0.438%→+0.365% | holds-positive-mild-cooling |
| ATOM-USD [소폭 재가속, 플러스권] | Hyperliquid | $0.28M | $1.92M | +0.001% | +0.291% | +0.218%→+0.291% | holds-positive-mild-reacceleration |
| ASTER-USDT-PERPETUAL [플러스 전환] | OrangeX | $7.00M | $2.36M | +0.010% | +0.015% | -0.135%→+0.015% | turns-positive |
| ASTER-USDT [대형 OI 유지] | Aster | $9.75M | $218.64M | +0.017% | -0.017% | -0.166%→-0.017% | large-oi-roughly-holds-near-breakeven |
| ASTER-USD [플러스 전환] | Hyperliquid | $0.88M | $14.21M | +0.001% | +0.037% | -0.17%→+0.037% | turns-positive |
| **KAITO-USD** [개선 3회차, 펀딩도 개선] | Hyperliquid | $29.66M | $16.80M | -0.169% | -7.719% | -11.352%→-7.719%. 8/20 대형 언락 약 11일 앞 | improves-third-round-funding-also-improves |
| GRAM-USD [소폭 악화] | Hyperliquid | $0.48M | $12.82M | +0.001% | -0.863% | -0.251%→-0.863% | mildly-worsens-negative |
| HYPE-USD [플러스권 거의 유지] | Hyperliquid | $81.96M | $1,197.30M | +0.001% | +0.526% | +0.563%→+0.526% | holds-positive-roughly-flat |
| HYPER-USD [냉각, 플러스권] | Hyperliquid | $0.10M | $0.33M | +0.001% | +1.209% | +1.917%→+1.209% | holds-positive-cools |
| APEX-USD [플러스 전환] | Hyperliquid | $0.09M | $0.78M | +0.001% | +0.626% | -0.23%→+0.626%, Bybit도 확인 | turns-positive-bybit-also-confirmed |
| FARTCOIN [소폭 재가속, 플러스권] | Hyperliquid | $2.47M | $22.33M | +0.002% | +1.62% | +1.222%→+1.62% | holds-positive-mild-reacceleration |
| ETHFI-USD [재가속, 플러스권] | Hyperliquid | $0.39M | $8.61M | +0.001% | +2.091% | +1.322%→+2.091% | holds-positive-reaccelerates |
| ETH-USD [플러스권 확대] | dYdX | $2.67M | $8.66M | 0.0% | +0.36% | +0.016%→+0.36% | extends-positive |
| BTC-USD [개선, 마이너스권] | dYdX | $1.10M | $18.21M | 0.0% | -0.122% | -0.288%→-0.122% | improves-stays-negative |
| SOL-USD [플러스권 유지] | dYdX | $0.35M | $4.53M | 0.0% | +1.99% | +1.969%→+1.99% | holds-positive-roughly-flat |
| ANSEM [마이너스 소폭 심화] | Aster | $0.39M | $0.91M | +0.001% | -5.769% | -4.582%→-5.769% | mildly-deepens-negative |
| ANSEM-USDT-PERPETUAL [마이너스 소폭 심화] | OrangeX | $0.46M | $0.16M | +0.010% | -5.048% | Aster와 동조 심화 | mildly-deepens-aligns-with-aster |
| **BTW** [⚠️⚠️ 반전 더욱 확장] | Aster | $2.78M | $12.90M | +0.058% | +28.936% | +16.288%→+28.936%, OI 감소흐름 진정 | reversal-extends-further-oi-stabilizes |
| HYNA:PUMP-USD [소폭 냉각, 별개 페어] | Hyperliquid | $0.04M | $0.16M | +0.003% | +8.952% | +9.686%→+8.952% | separate-pair-confirmed-mild-cooling |
| **HYNA:HYPE-USD** [⚠️ OI 재차 완전동일값 고정] | Hyperliquid | $0.03M | $0.72M | -0.005% | +0.682% | 직전 '갱신 재개' 판단이 성급했을 가능성 | oi-field-freezes-again-premature-normalization-claim |
| AEON-USDT-PERPETUAL [첫 뚜렷한 냉각] | OrangeX | $0.51M | $0.19M | +0.010% | +10.449% | +16.298%→+10.449% | first-clear-cooling |
| AEON-USDT [⚠️ 재확인 실패] | Aster | $0.06M | $0.26M | +0.005% | 15.328(직전값) | 이번 회차 응답에서 미확인, 직전 값 유지 표기 | unconfirmed-this-round-stale-value-shown |
| **BSB-USDT-PERPETUAL** [플러스 전환] | OrangeX | $16.07M | $5.74M | +0.010% | +2.744% | -1.657%→+2.744% | turns-positive |
| **BSB-USDT** [플러스 전환] | Aster | $0.10M | $0.11M | +0.001% | +2.565% | -1.009%→+2.565% | turns-positive |
| 1000RATS-USDT [소폭 악화] | Aster | $0.05M | $0.04M | +0.011% | -0.927% | -1.516%→-0.927% | mild-deterioration |
| **BLESS** [⚠️⚠️⚠️ 낙폭 절반 이하로 급감] | OrangeX | $127.19M | $43.05M | +0.180% | -13.732% | -32.66%→-13.732% | loss-halves-sharp-rebound |
| **BLESS-USDT** [⚠️⚠️⚠️ 낙폭 3분의1 수준으로 급감] | Aster | $0.44M | $0.18M | +0.005% | -11.07% | -37.697%→-11.07%, OrangeX와 동조 | loss-shrinks-sharply-aligns-with-orangex |

## 테마 태그

1. **시장 전반: `/global`이 8회 연속 429 끝에 이번 회차 마침내 성공 — 총시총 $2.298T·BTC도미넌스 56.61%(직전 WebSearch 참고치와 거의 일치)** (global-api-succeeds-after-8x-failures-matches-websearch).
2. **Fear&Greed 31(Fear) 5회차 연속 동일값 유지** (fear-greed-holds-31-fifth-consecutive-round).
3. **⚠️⚠️⚠️ ACE(Fusionist): 언락 직전 4거래소 전부 냉각에서 강한 재가속으로 급반전(+17~19%→+23~25%) — 원인 확정 아님** (ace-unlock-imminent-reverses-broad-reacceleration).
4. **⚠️⚠️⚠️ BLESS: 3회차 심화되던 낙폭이 절반~3분의1 수준으로 급격히 축소된 강한 되돌림** (bless-selloff-sharply-reverses).
5. **⚠️⚠️⚠️ BTW: 반전이 더욱 확장(+16.29%→+28.94%), OI 감소흐름도 진정** (btw-reversal-extends-further-oi-stabilizes).
6. **⚠️⚠️ BSB: 3거래소 전부 마이너스에서 플러스로 전환 — 안정화 국면을 넘어섬** (bsb-turns-positive-across-venues).
7. **⚠️⚠️ CASHCAT: 3회차 냉각을 끊고 3거래소 전부 강하게 재가속, 온체인 h24 재가속 관측과 방향 일치** (cashcat-breaks-cooling-reaccelerates-aligns-onchain).
8. **⚠️ BEAT: Binance BEATUSDT 12회차만에 첫 확인, OKX는 고점권에서 거의 평탄** (beat-binance-listing-confirmed-holds-near-peak).
9. **⚠️ BANK: 4회차 개선 흐름이 꺾이고 크게 악화, 펀딩도 큰 폭 마이너스. 8/17 언락 약 8일 앞** (bank-breaks-improvement-streak-sharply-deteriorates).
10. **BICO: OKX·OrangeX 냉각 vs Aster 재가속 — 직전과 반대 방향으로 주도 거래소가 바뀜** (bico-mixed-directional-split-leader-flips).
11. **KAITO: 개선 3회차 연속(OKX·HL 동조, 펀딩도 개선). 8/20 대형 언락 약 11일 앞** (kaito-improves-third-round-funding-also-improves).
12. **⚠️ HYNA:HYPE-USD: OI 필드가 재차 완전동일값으로 고정 — 직전 '갱신 재개' 판단이 성급했을 가능성** (hyna-hype-oi-field-freezes-again).
13. **AIO: 직전 플러스 전환 뒤 다시 마이너스로 반전 — 플립플롭 지속** (aio-reverses-negative-again-whipsaw).
14. **AKE: Bybit 데이터 1회 미확인 뒤 재등장, OI 증가는 재포함 효과이지 실질 증가 아님** (ake-bybit-reappears-oi-jump-is-inclusion-effect).
15. **1000RATS: 마이너스에서 플러스로 전환** (1000rats-turns-positive).
16. **AEON: OKX·OrangeX 첫 뚜렷한 냉각, Aster는 이번 회차 재확인 실패** (aeon-first-cooling-aster-unconfirmed).
17. **⚠️ GIGGLE·KAITO(OKX 직접) 필드 이상치가 각각 7회차 연속, GRAM도 5회차 연속 재현 — 구조적 패턴으로 완전히 굳어짐** (field-anomalies-seventh-fifth-round-fully-established).
18. **OKX ACE·BANK·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT은 이번 회차도 CoinGecko okex_swap 배열 미등재, OKX 직접 API 또는 DEX로 보강. BEAT·BICO·AEON·BSB·CAP·CORE는 okex_swap 정상 확인** (okx-most-still-not-listed-direct-api-supplements).
19. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
20. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
21. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
22. **이번 회차 CoinGecko 429가 직전보다 완화 — 대부분 1차 확보, dydx_chain·global만 재시도 필요** (rate-limiting-eases-this-round).
23. **지금은 일요일 밤(UTC 08:29) 시간대** (sunday-night-timing-caveat).

## 데이터 신뢰도

**CoinGecko binance_futures**: 1차 시도로 정상 확보. ACE·**BEAT(12회차만에 첫 확인)**·AAVE·
ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS 확인. BICO·GRAM·KAITO·MMT·PIPPIN·GIGGLE·
BLESS·CASHCAT·BSB·CORE·AEON·BTW·CAP·ETHFI·HYPE·HYPER·APEX·FARTCOIN는 Binance 미상장.

**CoinGecko bybit**: 1차 시도로 정상 확보. ACE·AAVE·ALLO·ADA·BANK·AKE(재등장)·AIO·ATOM·
ASTER·ALGO·1000RATS·APEX 확인. **BEAT는 13회차 연속 미확인.** BICO·KAITO·MMT·PIPPIN·GIGGLE·
BLESS·CASHCAT·BSB·CORE·AEON·BTW·CAP는 Bybit 미상장.

**CoinGecko okex_swap**: 1차 시도로 정상 확보(직전 회차보다 완화). AAVE·ALLO·ADA·ALGO·AEON·
ATOM·ASTER·CORE·BSB·CAP·BEAT·BICO 확인. ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·
BLESS·CASHCAT은 이번 회차도 okex_swap 배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+`public/open-interest`
(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인. `oiUsd` 필드 직접 사용
방법론을 22회차 연속 유지, vol24_usd=`volCcy24h`×`last` 계산 방식도 유지. **⚠️ GIGGLE**은
이번 회차도 vol24h(85,467,778)가 volCcy24h(854,677.78)보다 큰 역전된 필드 순서가 **7회차
연속** 재현됐다. **KAITO**는 vol24h=volCcy24h(221,508,151, 완전 동일) 이상치가 **7회차 연속**
재현됐다. **GRAM**도 이번 회차 vol24h=volCcy24h(1,771,954, 완전 동일)로 **5회차 연속**
재현됐다. 세 이상치 모두 계산 방식은 그대로 유지했다.

**Hyperliquid**: 1차 시도로 정상 확보. raw funding 필드가 이번 회차도 정상 스케일로 관측됐다
(예: ACE-USD -0.015, KAITO-USD -0.169, GRAM-USD 0.001) — 별도 보정 없이 raw 값을 그대로
사용했다. ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·ALGO·
HYNA:PUMP-USD·HYNA:HYPE-USD 등 raw 정밀값 확보. BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·BTW·
BLESS·ANSEM은 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: 1차 시도로 정상 확보, raw 정밀 숫자로 직접 확보.
ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·
1000RATS 전량 확보. **⚠️ AEON은 이번 회차 응답에서 미확인**(직전 값 유지 표기, 델리스팅인지
추출 누락인지 불확실). MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: 1차 시도로 정상 확보(직전 회차보다 완화), raw 정밀값 직접
확보. ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·CAP·BLESS·CASHCAT·BSB·ANSEM
확인. KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·CORE는 여전히 미발견.

**dYdX(`dydx_chain`)**: 3차 재시도 끝에 확보, raw 정밀값(BTC-USD $1.10M/OI $18.21M, ETH-USD
$2.67M/OI $8.66M, SOL-USD $0.35M/OI $4.53M).

**CoinGecko `/global`**: **8회 연속 429 끝에 이번 회차 마침내 확보** — 직접 API로 총시총
$2,298,263,635,528.73(약 $2.30T)·BTC도미넌스 56.61%를 확인했다. 직전 회차 WebSearch
스니펫($2.29T·56.8%)과 거의 일치해, 향후 회차부터는 직접 API 확보가 재개될 가능성이 있다.

**Fear&Greed**: alternative.me API로 1차 시도 정상 응답, **31(Fear)** 확인 — 5회차 연속
동일값.

**신규 발견**: Binance BEATUSDT가 12회차만에 처음 확인됐다. Bybit AKE가 1회 미확인 뒤
재등장했다. Bybit APEX도 이번 회차 확인됐다(+0.46%). Aster AEON은 이번 회차 응답에서
미확인됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접 조회분)의
CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를 직접 채택(22회차
연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·ALGO 등 복수 거래소
종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은 본문·`why`에 별도
표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상 스케일로 관측돼 보정 없이
raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE·BSB·
BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며(BEAT는 이번 회차부터
Binance 소규모 리스팅 확인), 이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·
ANSEM·HYNA:PUMP-USD·HYNA:HYPE-USD·BLESS는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다;
(h) Bybit BEAT는 13회차 연속 조회 표에 나타나지 않았는데, 델리스팅인지 조회 누락인지는
확정하지 않는다; (i) Aster AEON이 이번 회차 미확인됐는데, 델리스팅보다는 이번 조회의 추출
누락일 가능성이 있으나 확정하지 않는다; (j) BLESS·ACE·BTW·BSB·CASHCAT의 이번 회차 급변
배경(구체적 촉매)은 정황상 추정이며 직접적 인과관계는 확정하지 않는다; (k) 이번 회차 급변에
대한 인과관계 해석(언락 직전 포지셔닝, 반등 등)은 대체로 정황상 추정이며 확정된 것은 아니다;
(l) GIGGLE·KAITO의 필드 이상치가 7회차 연속, GRAM도 5회차 연속 재현돼 구조적 패턴으로 완전히
굳어졌으나 근본 원인(OKX API 자체 특성인지)은 규명하지 않았다; (m) HYNA:HYPE-USD의 OI 필드가
재차 완전동일값으로 관측돼, 직전 회차 '정상화' 판단을 이번 회차 스스로 정정했다 — 향후
회차에서도 계속 추적이 필요하다; (n) `/global`은 8회 연속 실패 끝에 이번 회차 성공했으나
단발성일 수 있어 다음 회차도 재확인이 필요하다; (o) 지금은 일요일 밤으로 유동성 패턴이
평일과 다를 수 있으며, 확정 불가.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
