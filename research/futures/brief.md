# 선물시장 스카우트 브리핑 — 2026-08-10 08:29 UTC (KST 2026-08-10 17:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-10T06:40:00Z)
> 로부터 약 1시간49분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 정상 응답으로 확보 — 총시총 **$2,307,947,016,226.99(약 $2.308T)**·
BTC도미넌스 **56.710%**로 직전 회차($2.305T·56.687%)보다 시총·도미넌스 모두 소폭 상승,
**12회차 연속** 확보됐다.

### Fear&Greed 30(Fear) — 직전과 동일, 4회차 연속

alternative.me API 정상 응답, **30(Fear)** — 직전 회차(30)에서 변동 없이 유지, 4회차
연속 30을 이어가고 있다.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM 개별조회)는 **33회차 연속** 방법론(`oiUsd`
필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을 유지했다.
이번 회차는 OKX ACE-USDT-SWAP·TUT-USDT-SWAP·TOAD-USDT-SWAP 모두 instId 자체가 존재하지
않아(에러코드 51001) OKX 미상장이 재확인됐다(ACE는 33회차 연속). CoinGecko
`orangex_futures`·`dydx_chain`·`/global`은 1~2회 429를 겪은 뒤 재시도로 확보됐고,
`binance_futures`·`bybit`·`okex_swap`·`hyperliquid`·`aster`·Fear&Greed는 첫 시도에
정상 응답했다.

## 이번 회차 최대 사건

### ⚠️⚠️⚠️ BICO — 5회차 연속 악화 스트릭 종료, 첫 개선

5회차 연속 악화 끝에 이번 회차 처음으로 3소스 전원이 개선됐다: OKX **-45.808%→-34.313%**,
OrangeX **-46.811%→-34.802%**(펀딩 -0.423%→**+0.322%**로 부호 전환), Aster
**-45.397%→-37.084%** — 최대낙폭 경신 행진이 멈췄다. WebSearch로 새로 확인한 사실:
**8/5 AlphaX DEX가 BICO를 50배 레버리지·수수료 0%로 신규 상장**했다는 추가 촉매를
확인했으나([coingabbar.com](https://www.coingabbar.com/en/price-prediction/bico-price-prediction-biconomy-channel-breakout-whale-squeeze)),
검색결과 내 가격 수치가 서로 다른 날짜 기사에서 혼재돼 있어 정량 재현은 보류한다.
직전 회차의 '숏스퀴즈 되돌림 지속'에서 이번 회차 '바닥 찾기'로 흐름이 바뀐 것으로
보이나, 1회차만으로 추세 반전을 단정하기는 이르다.

### ⚠️ AKE·1000RATS — 플러스에서 마이너스로 급반전

AKE는 3소스 전원이 플러스에서 마이너스로 돌아섰다: Binance/Bybit 가중
**+4.675%→-1.503%**, OrangeX **+5.035%→-1.498%**, Aster **+4.499%→-1.266%**. 1000RATS도
같은 방향으로 반전했다: Binance/Bybit 가중 **+3.501%→-1.464%**, Aster **+2.454%→-1.114%**.

### ⚠️ BANK — 4소스 전원 강한 플러스 반전, 언락 6.6일 앞

Binance/Bybit 가중 **+0.172%→+2.961%**, OrangeX **-0.01%→+2.178%**, Aster
**-0.231%→+2.751%**로 전 소스가 동반 강세 전환했다. 8/17 대형 언락 약 **6.6일** 앞으로,
사전 포지셔닝 가능성을 배제할 수 없어 다음 회차도 추적이 필요하다.

## 직전 회차 강조 종목 추적 결과

- **① BICO — ⚠️⚠️⚠️ 5회차 악화 종료, 첫 개선.** 위 '최대 사건' 참조 — 바닥 찾기 가능성.
- **② CAP — ⚠️⚠️ 상승폭 대폭 축소, 상장효과 소진 조짐.** OKX **+34.455%→+16.349%**,
  OrangeX **+35.747%→+18.813%**, Aster **+33.71%→+14.759%**로 3소스 동조 급감 —
  8/6 Upbit 상장 촉매 효과가 뚜렷하게 식고 있다.
- **③ ADA — ⚠️⚠️ 15회차 스트릭 종료 후 하루 만에 흔들림.** Binance/Bybit 가중이
  **+0.174%→-0.166%**로 재차 소폭 마이너스로 돌아섰으나, OrangeX **-0.302%→-0.051%**,
  Aster **-0.252%→+0.101%**, HL **-0.186%→+0.061%**는 계속 개선돼 소스 간 혼조로
  재편됐다 — 방향성 확정 아닌 휩쏘성 되돌림으로 판단, 다음 회차 추적 필요.
- **④ ACE — 회복 지속, 2회차 연속 전원 개선.** 가중 **-11.220%→-9.141%**, Binance
  **-11.126%→-9.167%**, Bybit **-11.491%→-9.058%**, OrangeX **-10.342%→-9.309%**, Aster
  **-11.028%→-8.297%**, HL **-11.224%→-7.768%**로 5소스 전원 추가 개선.
- **⑤ KAITO — 마이너스 심화, 펀딩 급격 악화.** OKX **-2.889%→-3.311%**(펀딩
  -0.128%→**-0.563%**로 큰 폭 악화), HL **-2.825%→-3.75%**(펀딩 -0.091%→**-0.287%**로
  큰 폭 악화). 8/20 대형 언락 약 **9.6일** 앞, 숏 우위 강화 조짐.
- **⑥ CASHCAT — ⚠️⚠️ 소폭 냉각 전환.** HL **45.397%→40.719%**, OrangeX
  **45.042%→40.012%**, Aster **45.188%→39.525%**로 3소스 전원 소폭 냉각됐다 —
  온체인 루틴(06:11Z 기준)이 먼저 관측한 확산 둔화(h1 음전)를 선물이 뒤따르는 구도가
  이번 회차 확인됐다.

## 신규/추가 발견

### ⚠️ TUT 재확인 — 전 소스에서 여전히 미상장

OKX TUT-USDT-SWAP 직접조회에서도 instId 부재(에러코드 51001)를 확인했고, Aster 티커
전체에서 TUT 서브스트링 매칭이 0건임을 재확인했다. Binance·Bybit·HL·OrangeX에서도
발견되지 않았다 — 온체인·뉴스가 보고한 8/6 Aster TUT 퍼프 상장과 현재 선물 데이터
간 괴리가 이번 회차도 해소되지 않았다.

### TOAD — 이번 회차 전 소스 재검색 완료, 여전히 미상장

직전 회차는 재검색을 생략하고 이전 결과를 이어받았으나, 이번 회차는 Binance·Bybit·
OKX(직접, 51001)·HL·Aster·OrangeX **전 소스를 명시적으로 재검색**해 여전히 미상장임을
확인했다.

### AEON·ATOM — 개선·전환 지속

AEON은 개선이 2회차 연속 이어졌다: OKX **-11.616%→-7.699%**, OrangeX
**-11.598%→-7.463%**, Aster **-11.782%→-8.187%**. ATOM은 전 소스가 마이너스에서
플러스로 전환됐다: Binance/Bybit 가중 **-0.330%→+0.236%**, OrangeX **-0.578%→+0.218%**,
Aster **-0.145%→+0.291%**, HL **-0.383%→+0.254%**.

### AIO — 완전반납 이후 재반등

Binance **+0.231%→+5.711%**(Bybit는 이번 회차 AIOUSDT 미매칭, AIOZUSDT는 다른
토큰이라 제외), Aster **+0.048%→+1.931%**로 동조 재상승 — 롤러코스터성 변동이 이어진다.

### ⚠️ BLESS — 대폭 악화

OrangeX **-2.367%→-15.623%**, Aster **-1.554%→-12.463%**로 두 소스 모두 급격히
악화됐다.

## 데이터 이슈 추적 결과

GIGGLE 필드 이상치(vol24h=46,507,844 vs volCcy24h=465,078.44, 100배 스케일 차이)가
**18회차 연속**, KAITO(OKX 직접, vol24h=volCcy24h=97,218,440) 완전동일값 이상치가
**18회차 연속**, GRAM(vol24h=volCcy24h=2,461,762) 완전동일값 이상치가 **16회차 연속**
재현됐다. 직전 회차 신규 관찰됐던 MMT·PIPPIN의 10배 스케일 비율(vol24h=volCcy24h÷10)이
이번 회차도 그대로 재현됐다(MMT: 23,436,009/234,360,090, PIPPIN: 16,750,474/167,504,740)
— **2회차 연속 재현**으로 일회성이 아니라 계약 승수 차이에 따른 구조적 패턴일 가능성이
높아졌다. HYNA:HYPE-USD의 OI는 이번 회차도 정상 갱신을 이어갔다($688,966.35→
**$693,240.53**) — 정상화 **4회차 연속**.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| ACE [회복 지속, 2회차] | Binance/Bybit(가중) | $63.81M | $11.23M | +0.005% | -9.141% | 가중 -11.220%→-9.141%, 5소스 전원 개선 | recovery-continues-2nd-round-all-sources |
| **BICO** [⚠️⚠️⚠️ 5회차 악화 종료] | OKX(CoinGecko정상, okex_swap) | $370.74M | $8.41M | -0.105% | -34.313% | -45.808%→-34.313%, 최대낙폭 행진 멈춤 | worsening-streak-breaks-first-improvement-5th-round-ends |
| BEAT [2회차 하락 종료, 개선] | OKX(CoinGecko정상, okex_swap) | $280.55M | $7.85M | -0.007% | -19.087% | -22.742%→-19.087% | worsening-2round-ends-improves |
| KAITO [마이너스 심화, 펀딩 악화] | OKX(직접API) | $64.44M | $7.68M | -0.563% | -3.311% | -2.889%→-3.311%, 펀딩 -0.128%→-0.563%. 8/20 언락 9.6일 앞 | negative-deepens-funding-sharply-worsens |
| **BANK** [⚠️ 강한 플러스 반전] | Binance/Bybit(가중) | $102.83M | $18.63M | -0.001% | +2.961% | +0.172%→+2.961%. 8/17 언락 6.6일 앞 | sharp-reversal-positive-all-sources-preunlock-watch |
| MMT [부분 회복 지속] | OKX(직접API) | $47.04M | $3.48M | -0.110% | -13.640% | -14.861%→-13.640%, 원인 미규명 | partial-recovery-continues |
| BSB [완화 흐름 지속] | OKX(CoinGecko정상, okex_swap) | $5.88M | $2.55M | +0.019% | -6.262% | -6.749%→-6.262% | improvement-continues |
| AAVE [플러스 확대] | Binance/Bybit(가중) | $45.79M | $89.18M | +0.009% | +0.759% | +0.081%→+0.759% | extends-positive |
| ALLO [개선 종료, 재악화] | Binance/Bybit(가중) | $21.19M | $17.89M | +0.002% | -2.580% | -0.698%→-2.580% | improvement-ends-reverses-negative |
| ADA [⚠️⚠️ 흔들림, 소스 혼조] | Binance/Bybit(가중, USDT만) | $150.58M | $170.95M | +0.008% | -0.166% | 가중 +0.174%→-0.166%, DEX는 계속 개선 | positive-turn-wobbles-mixed-sources |
| **AKE** [⚠️ 급반전 마이너스] | Binance/Bybit(가중) | $41.42M | $37.53M | +0.027% | -1.503% | +4.675%→-1.503% | sharp-reversal-to-negative |
| GIGGLE [완화, 이상치 18회차] | OKX(직접API) | $15.58M | $2.34M | +0.005% | -4.202% | -5.836%→-4.202% | improves-within-negative-field-anomaly-18th-round |
| PIPPIN [플러스 확대, 10x 2회차] | OKX(직접API) | $3.05M | $1.90M | +0.015% | +5.382% | +4.100%→+5.382%, 10배 비율 2회차 재현 | positive-holds-increase-10x-pattern-2nd-round |
| **1000RATS** [⚠️ 반전 마이너스] | Binance/Bybit(가중) | $12.08M | $18.05M | +0.011% | -1.464% | +3.501%→-1.464% | reverses-to-negative |
| AIO [⚠️ 재반등] | Binance(단독) | $8.51M | $3.52M | +0.014% | +5.711% | +0.231%→+5.711% | rebounds-again-rollercoaster |
| GRAM [완화, 이상치 16회차] | OKX(직접API) | $3.29M | $6.44M | +0.005% | -0.447% | -0.593%→-0.447% | improves-within-negative-field-anomaly-16th-round |
| AEON [개선 2회차 연속] | OKX(CoinGecko정상, okex_swap) | $12.95M | $3.59M | +0.005% | -7.699% | -11.616%→-7.699% | improvement-continues-2nd-round |
| ATOM [플러스 전환, 전 소스] | Binance/Bybit(가중) | $8.69M | $28.43M | -0.020% | +0.236% | -0.330%→+0.236% | turns-positive-all-sources |
| ASTER [완만한 상승 지속] | Binance/Bybit(가중) | $22.57M | $113.48M | +0.005% | +1.972% | +1.877%→+1.972% | positive-holds-gentle-rise |
| CORE [거의 유지] | OKX(CoinGecko정상, okex_swap) | $1.82M | $1.02M | +0.010% | +1.703% | +1.699%→+1.703%, 초저유동성 | roughly-flat-positive-low-liquidity |
| **CAP** [⚠️⚠️ 상승폭 대폭 축소] | OKX(CoinGecko정상, okex_swap) | $104.43M | $5.17M | -0.129% | +16.349% | +34.455%→+16.349%, 상장효과 소진 조짐 | surge-fades-catalyst-cooling |
| ALGO [거의 유지, 소폭 개선] | Binance/Bybit(가중) | $17.21M | $14.57M | +0.001% | -4.890% | -5.269%→-4.890% | roughly-flat-slight-improvement |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| ACE-USD [개선 지속] | Hyperliquid | $1.90M | $1.37M | 0.000% | -7.768% | -11.224%→-7.768% | recovery-continues |
| ACE-USDT-PERPETUAL [개선 지속] | OrangeX | $38.51M | $13.99M | +0.015% | -9.309% | -10.342%→-9.309% | recovery-continues |
| ACE-USDT [개선 지속] | Aster | $0.30M | $0.03M | -0.002% | -8.297% | -11.028%→-8.297% | recovery-continues |
| BEAT-USDT-PERPETUAL [개선] | OrangeX | $19.56M | $5.38M | -0.010% | -20.763% | -22.953%→-20.763% | worsening-2round-ends-improves |
| BEAT-USDT [개선] | Aster | $6.27M | $0.92M | 0.000% | -20.471% | -23.38%→-20.471% | worsening-2round-ends-improves |
| **BICO-USDT-PERPETUAL** [⚠️⚠️⚠️ 5회차 악화 종료] | OrangeX | $172.22M | $52.74M | +0.322% | -34.802% | -46.811%→-34.802%, 펀딩 부호 전환 | worsening-streak-breaks-first-improvement-5th-round-ends |
| **BICO-USDT** [⚠️⚠️⚠️ 5회차 악화 종료] | Aster | $2.97M | $0.24M | -0.004% | -37.084% | -45.397%→-37.084% | worsening-streak-breaks-first-improvement-5th-round-ends |
| **CASHCAT** [⚠️⚠️ 소폭 냉각] | Hyperliquid | $19.97M | $23.78M | +0.017% | +40.719% | 45.397%→40.719%, 온체인 둔화 선행 확인 | mild-cooling-follows-onchain-slowdown |
| CASHCAT-USDT-PERPETUAL [소폭 냉각] | OrangeX | $0.15M | $0.06M | +0.035% | +40.012% | 45.042%→40.012% | mild-cooling-follows-onchain-slowdown |
| CASHCAT-USDT [소폭 냉각] | Aster | $2.28M | $1.65M | +0.001% | +39.525% | 45.188%→39.525% | mild-cooling-follows-onchain-slowdown |
| ALLO-USDT [마이너스 재전환] | Aster | $0.10M | $0.03M | +0.001% | -1.787% | +0.324%→-1.787% | turns-negative-again |
| ALLO-USDT-PERPETUAL [재악화] | OrangeX | $13.94M | $5.11M | +0.010% | -2.127% | -0.545%→-2.127% | worsens |
| AAVE-USDT-PERPETUAL [플러스 확대] | OrangeX | $25.59M | $9.47M | +0.010% | +0.776% | +0.24%→+0.776% | extends-positive |
| AAVE-USDT [플러스 확대] | Aster | $0.43M | $4.58M | +0.010% | +0.699% | +0.131%→+0.699% | extends-positive |
| AAVE-USD [플러스 확대] | Hyperliquid | $3.40M | $61.56M | +0.001% | +0.606% | +0.235%→+0.606% | extends-positive |
| ADA-USDT-PERPETUAL [손익분기 근접] | OrangeX | $81.94M | $30.76M | +0.010% | -0.051% | -0.302%→-0.051% | improves-near-flat |
| ADA-USDT [플러스 전환] | Aster | $0.49M | $1.67M | +0.007% | +0.101% | -0.252%→+0.101% | turns-positive |
| ADA-USD [플러스 전환] | Hyperliquid | $3.49M | $32.86M | +0.001% | +0.061% | -0.186%→+0.061% | turns-positive |
| **BANK-USDT-PERPETUAL** [⚠️ 강한 플러스 반전] | OrangeX | $7.68M | $2.77M | -0.021% | +2.178% | -0.01%→+2.178%. 8/17 언락 6.6일 앞 | sharp-reversal-positive-preunlock-watch |
| **BANK-USDT** [⚠️ 강한 플러스 반전] | Aster | $0.50M | $0.29M | +0.001% | +2.751% | -0.231%→+2.751%. 8/17 언락 6.6일 앞 | sharp-reversal-positive-preunlock-watch |
| **AKE-USDT-PERPETUAL** [⚠️ 급반전 마이너스] | OrangeX | $5.43M | $1.86M | +0.012% | -1.498% | +5.035%→-1.498% | sharp-reversal-to-negative |
| **AKE-USDT** [⚠️ 급반전 마이너스] | Aster | $0.73M | $10.56M | +0.008% | -1.266% | +4.499%→-1.266% | sharp-reversal-to-negative |
| **CAP-USDT** [⚠️⚠️ 상승폭 대폭 축소] | Aster | $0.12M | $0.15M | -0.002% | +14.759% | +33.71%→+14.759% | surge-fades-catalyst-cooling |
| **CAP-USDT-PERPETUAL** [⚠️⚠️ 상승폭 대폭 축소] | OrangeX | $0.62M | $0.24M | -0.149% | +18.813% | +35.747%→+18.813% | surge-fades-catalyst-cooling |
| ALGO-USDT-PERPETUAL [마이너스권 완화] | OrangeX | $9.38M | $3.24M | -0.010% | -4.844% | -5.19%→-4.844% | improves-within-negative |
| ALGO-USDT [초저유동성, 거의 유지] | Aster | $0.04M | $0.02M | -0.001% | -5.25% | -5.047%→-5.25% | low-liquidity-roughly-flat |
| ALGO-USD [거의 유지] | Hyperliquid | $0.91M | $1.94M | +0.001% | -5.188% | -5.172%→-5.188% | roughly-flat-negative |
| ATOM-USDT-PERPETUAL [플러스 전환] | OrangeX | $4.62M | $1.55M | +0.010% | +0.218% | -0.578%→+0.218% | turns-positive |
| ATOM-USDT [초저유동성, 플러스 전환] | Aster | $0.005M | $1.60M | +0.008% | +0.291% | -0.145%→+0.291% | low-liquidity-turns-positive |
| ATOM-USD [플러스 전환] | Hyperliquid | $0.22M | $1.91M | -0.004% | +0.254% | -0.383%→+0.254% | turns-positive |
| ASTER-USDT-PERPETUAL [완만한 상승] | OrangeX | $9.04M | $3.08M | +0.010% | +2.086% | +1.848%→+2.086% | gentle-rise-continues |
| ASTER-USDT [대형 OI 유지] | Aster | $14.16M | $222.69M | +0.011% | +1.896% | OI $222.63M→$222.69M | large-oi-positive-holds |
| ASTER-USD [완만한 상승] | Hyperliquid | $1.47M | $14.76M | +0.001% | +1.991% | +1.853%→+1.991% | gentle-rise-continues |
| KAITO-USD [마이너스 심화, 펀딩 악화] | Hyperliquid | $19.63M | $9.28M | -0.287% | -3.75% | -2.825%→-3.75%, 펀딩 -0.091%→-0.287% | negative-deepens-funding-sharply-worsens |
| GRAM-USD [완화 지속] | Hyperliquid | $0.69M | $12.97M | +0.001% | -0.335% | -1.0%→-0.335% | improves-continues |
| HYPE-USD [플러스 전환, 손익분기 근접] | Hyperliquid | $102.20M | $1,189.74M | +0.001% | +0.033% | -1.006%→+0.033% | turns-positive-near-flat |
| HYPER-USD [마이너스 재전환] | Hyperliquid | $0.19M | $0.34M | -0.002% | -0.62% | +0.137%→-0.62% | turns-negative-again |
| APEX-USD [마이너스 심화] | Hyperliquid | $0.07M | $0.75M | -0.006% | -2.238% | -1.662%→-2.238%, Bybit도 동조 | negative-deepens |
| FARTCOIN [플러스 유지, 냉각] | Hyperliquid | $7.67M | $23.38M | +0.001% | +3.494% | +3.945%→+3.494% | cools-within-positive |
| ETHFI-USD [플러스 유지, 냉각] | Hyperliquid | $0.67M | $8.48M | +0.001% | +0.349% | +0.75%→+0.349% | cools-within-positive |
| ETH-USD [플러스 유지, 확대] | dYdX | $16.14M | $12.79M | +0.002% | +0.453% | +0.407%→+0.453% | positive-holds-increase |
| BTC-USD [플러스 유지, 확대] | dYdX | $1.88M | $17.90M | 0.000% | +0.621% | +0.487%→+0.621% | positive-holds-increase |
| SOL-USD [플러스 유지, 냉각] | dYdX | $0.14M | $4.54M | 0.000% | +0.641% | +0.787%→+0.641% | cools-within-positive |
| ANSEM [플러스 확대] | Aster | $0.20M | $1.05M | +0.001% | +5.341% | +2.162%→+5.341% | extends-positive |
| ANSEM-USDT-PERPETUAL [플러스 확대] | OrangeX | $0.50M | $0.18M | +0.010% | +3.683% | +0.341%→+3.683% | extends-positive |
| BTW [플러스 확대] | Aster | $2.18M | $14.50M | +0.017% | +10.958% | +8.156%→+10.958% | extends-positive |
| HYNA:PUMP-USD [플러스권 냉각] | Hyperliquid | $0.05M | $0.18M | +0.002% | +11.423% | +14.638%→+11.423% | cools-within-positive |
| HYNA:HYPE-USD [OI 정상갱신 4회차] | Hyperliquid | $0.15M | $0.69M | +0.003% | -0.203% | $688,966.35→$693,240.53 | oi-normal-updates-continue-4th-round |
| AEON-USDT-PERPETUAL [개선 2회차] | OrangeX | $0.42M | $0.15M | +0.010% | -7.463% | -11.598%→-7.463% | improvement-continues-2nd-round |
| AEON-USDT [개선 2회차] | Aster | $0.07M | $0.21M | +0.005% | -8.187% | -11.782%→-8.187% | improvement-continues-2nd-round |
| BSB-USDT-PERPETUAL [완화 지속] | OrangeX | $9.96M | $3.20M | +0.010% | -6.393% | -6.805%→-6.393% | improvement-continues |
| BSB-USDT [거의 유지] | Aster | $0.04M | $0.10M | +0.001% | -6.872% | -6.949%→-6.872% | roughly-flat-improvement |
| **1000RATS-USDT** [⚠️ 반전 마이너스] | Aster | $0.11M | $0.04M | +0.012% | -1.114% | +2.454%→-1.114% | reverses-to-negative |
| **AIO-USDT** [⚠️ 재반등] | Aster | $0.55M | $0.10M | +0.005% | +1.931% | +0.048%→+1.931% | rebounds-again |
| **BLESS** [⚠️ 대폭 악화] | OrangeX | $53.14M | $17.83M | +0.222% | -15.623% | -2.367%→-15.623% | sharp-worsening |
| **BLESS-USDT** [⚠️ 대폭 악화] | Aster | $0.27M | $0.23M | +0.009% | -12.463% | -1.554%→-12.463% | sharp-worsening |

## 테마 태그

1. **시장 전반: `/global` 정상 응답, 12회차 연속 확보 — 총시총 $2.308T(소폭 상승)·BTC도미넌스 56.710%(소폭 상승)** (global-api-twelfth-round-normal).
2. **Fear&Greed 30(Fear) — 직전과 동일, 4회차 연속 유지** (fear-greed-holds-at-30-fourth-round).
3. **⚠️⚠️⚠️ BICO: 5회차 연속 악화 스트릭 종료, 3소스 전원 개선 — 최대낙폭 경신 행진 멈춤. 8/5 AlphaX DEX 50배 레버리지 무수수료 상장 추가 확인** (bico-worsening-streak-breaks-first-improvement).
4. **BEAT: 2회차 하락 종료, 3소스 동조 개선** (beat-worsening-2round-ends-improves).
5. **⚠️ AKE: 플러스에서 마이너스로 급반전, 3소스 전원 동조** (ake-sharp-reversal-to-negative).
6. **⚠️ 1000RATS: 플러스에서 마이너스로 반전** (1000rats-reverses-to-negative).
7. **⚠️⚠️ ADA: 15회차 스트릭 종료 후 하루 만에 흔들림, 소스 간 혼조 — 방향성 미확정** (ada-positive-turn-wobbles-mixed-sources).
8. **⚠️ BANK: 4소스 전원 강한 플러스 반전, 8/17 언락 약 6.6일 앞두고 사전 포지셔닝 가능성 배제 못함** (bank-sharp-reversal-positive-preunlock-watch).
9. **KAITO: 마이너스 심화, 펀딩 큰 폭 악화. 8/20 대형 언락 약 9.6일 앞** (kaito-negative-deepens-funding-worsens).
10. **MMT: 부분 회복 지속, 원인 여전히 미규명** (mmt-partial-recovery-continues).
11. **⚠️⚠️ CAP: 상승폭 대폭 축소, 3소스 동조 — 8/6 Upbit 상장 촉매 효과 뚜렷하게 소진** (cap-surge-fades-catalyst-cooling).
12. **⚠️⚠️ CASHCAT: 3소스 전원 소폭 냉각 전환 — 온체인 루틴이 먼저 관측한 확산 둔화를 선물이 뒤따르는 구도 확인** (cashcat-mild-cooling-follows-onchain-slowdown).
13. **AEON: 개선 2회차 연속, 3소스 동조** (aeon-improvement-continues-2nd-round).
14. **ATOM: 전 소스가 마이너스에서 플러스로 전환** (atom-turns-positive-all-sources).
15. **AIO: 완전반납 이후 재반등, 롤러코스터성 변동** (aio-rebounds-again-rollercoaster).
16. **⚠️ BLESS: OrangeX·Aster 모두 대폭 악화** (bless-sharp-worsening).
17. **⚠️ TUT 재확인: OKX·Aster·Binance·Bybit·HL·OrangeX 전 소스에서 여전히 미상장 — 온체인·뉴스 촉매와 선물 데이터 간 괴리 지속** (tut-reconfirmed-unlisted-all-sources).
18. **TOAD: 이번 회차 전 소스 재검색 완료, 여전히 미상장 확인** (toad-reconfirmed-unlisted-full-recheck).
19. **⚠️ GIGGLE 필드 이상치 18회차 연속, KAITO(OKX 직접) 완전동일값 18회차 연속, GRAM 16회차 연속 재현. MMT·PIPPIN 10배 비율 2회차 연속 재현 — 구조적 패턴 가능성 높아짐** (field-anomalies-continue-10x-pattern-2nd-round-reproduced).
20. **OKX ACE·TUT·TOAD 모두 instId 자체 부재 확인(ACE는 33회차 연속)** (okx-multiple-symbols-not-listed).
21. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
22. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
23. **이번 회차 orangex_futures·dydx_chain·global은 1~2회 429 후 재시도로 확보, 나머지 소스는 첫 시도 정상** (rate-limiting-minor-this-round).
24. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**CoinGecko binance_futures**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS
확인, 전부 첫 시도 정상 응답. **BICO·BEAT·BSB·APEX·BTW·KAITO·CASHCAT·MMT·GIGGLE·PIPPIN·
GRAM·CORE·CAP·AEON·BLESS·ANSEM·TUT·TOAD는 이번 회차도 명확히 미확인**(단순 미상장).

**CoinGecko bybit**: ACE·AAVE·ALLO·ADA·BANK·AKE·ATOM·ASTER·ALGO·1000RATS·APEX 확인,
첫 시도 정상 응답. AIOUSDT는 이번 회차 매칭 실패(AIOZUSDT는 다른 토큰이라 제외). 나머지는
명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·CAP·BICO·BEAT 확인,
첫 시도 정상 응답. ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT·TUT·TOAD는
이번 회차도 okex_swap 배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인.
`oiUsd` 필드 직접 사용 방법론을 **33회차 연속** 유지, vol24_usd=`volCcy24h`×`last` 계산
방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️ **ACE-USDT-SWAP·TUT-USDT-SWAP·
TOAD-USDT-SWAP는 OKX에 instId 자체가 존재하지 않음**을 이번 회차도 직접 확인
(에러코드 51001), ACE는 **33회차 연속**. **GIGGLE**은 raw JSON에서 `vol24h=46,507,844`·
`volCcy24h=465,078.44`로 정확히 100배 스케일 차이가 나는 필드 이상치가 **18회차 연속**,
**KAITO**는 `vol24h`=`volCcy24h`=97,218,440로 완전동일값 이상치가 **18회차 연속**,
**GRAM**도 `vol24h`=`volCcy24h`=2,461,762로 완전동일값이 **16회차 연속** 재현됐다.
**MMT**(vol24h=23,436,009, volCcy24h=234,360,090)와 **PIPPIN**(vol24h=16,750,474,
volCcy24h=167,504,740)의 10배 비율이 **2회차 연속** 재현돼 계약 승수 차이에 따른
구조적 패턴 가능성이 높아졌다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·
ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD·BTC·ETH 등 raw 정밀값 확보(첫 시도 정상 응답). **SOL은
HL에서 이번 회차도 미확인**(기존 dYdX로 대체 집계). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·
BTW·BLESS·ANSEM·TUT·TOAD는 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·
BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON·AIO 전량 확보(raw 정밀값, 첫 시도
정상 응답). MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견. **TUT·TOAD는
서브스트링 검색으로 재확인, 이번 회차도 미발견**.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값, 1~2회 429 후 재시도). BTW는 이번 회차도
OrangeX에서 미발견(기존과 동일, Aster에서만 확인). KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·
CORE·TUT·TOAD는 여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.88M/OI $17.90M, ETH-USD $16.14M/OI $12.79M,
SOL-USD $0.14M/OI $4.54M) 확보, 1~2회 429 후 재시도로 확보.

**CoinGecko `/global`**: 1~2회 429 후 재시도로 총시총 $2,307,947,016,226.99(약
$2.308T)·BTC도미넌스 56.710%를 확인했다. 직전 회차($2.305T·56.687%)보다 시총·도미넌스
모두 소폭 상승, **12회차 연속** 확보됐다.

**Fear&Greed**: alternative.me API로 정상 응답, **30(Fear)** 확인 — 직전과 동일, 4회차
연속 유지됐다.

**신규 발견**: (a) BICO가 5회차 연속 악화 스트릭을 처음으로 끊고 3소스 전원 개선됐다
— 최대낙폭 경신 행진이 멈춘 이번 회차 최대 사건. (b) AKE·1000RATS가 나란히 플러스에서
마이너스로 급반전했다. (c) BANK가 4소스 전원 강한 플러스로 반전, 8/17 언락을 앞두고
사전 포지셔닝 가능성이 있어 주시가 필요하다. (d) ADA는 직전 회차의 '15회차 스트릭 종료'가
하루 만에 소스 간 혼조로 재편됐다 — 아직 방향성이 확정되지 않았다. (e) CAP·CASHCAT
모두 상승폭이 뚜렷하게 축소돼 상장 촉매 효과가 소진되는 조짐이 확인됐다. (f) TUT·TOAD
모두 이번 회차 전 소스 재검색을 완료해 여전히 미상장임을 명시적으로 재확인했다.
(g) MMT·PIPPIN의 10배 필드 비율이 2회차 연속 재현돼 구조적 패턴일 가능성이 높아졌다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(33회차 연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은
본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상 스케일로
관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·
GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며,
이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·
HYNA:HYPE-USD·BLESS·AIO-USDT는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다;
(h) BICO의 이번 회차 개선이 진짜 바닥인지, 일시적 반등인지는 1회차 데이터만으로 단정할
수 없어 다음 회차 추적이 필요하다; (i) BANK의 강한 플러스 반전이 8/17 언락을 앞둔 실제
사전 포지셔닝인지, 단순 변동성인지는 규명하지 못했다 — 다음 회차 추적 필요; (j) ADA의
소스 간 혼조(가중 마이너스 vs 개별 거래소 플러스)는 표본 크기·가중 방식의 차이에서
비롯됐을 수 있어 완전히 규명하지 않았다; (k) KAITO 8/20 언락 규모는 이전 회차 기준
소스별로 공급 3.3%~7.63%·$22.9M~$34.68M로 편차가 있었으며, 이번 회차는 재검증하지
않았다; (l) GIGGLE·KAITO의 필드 이상치가 18회차 연속, GRAM도 16회차 연속 재현돼 구조적
패턴으로 굳어졌으나 근본 원인(OKX API 자체 특성인지)은 규명하지 않았다; (m) MMT의 급반전
원인은 이번 회차에서도 조사하지 못했다 — 다음 회차 추적이 필요하다; (n) BLESS의 급격한
악화 원인(뉴스·촉매)은 이번 회차 조사하지 못했다 — 다음 회차 추적 필요; (o) CAP·CASHCAT의
상승폭 축소가 일시적 조정인지 추세 반전으로 굳어지는지는 다음 회차 추적이 필요하다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
