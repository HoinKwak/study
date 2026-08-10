# 선물시장 스카우트 브리핑 — 2026-08-10 10:28 UTC (KST 2026-08-10 19:28)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-10T08:29:00Z)
> 로부터 약 1시간59분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 정상 응답으로 확보 — 총시총 **$2,301,326,971,009.47(약 $2.301T)**·
BTC도미넌스 **56.670%**로 직전 회차($2.308T·56.710%)보다 시총·도미넌스 모두 소폭 하락,
**13회차 연속** 확보됐다.

### Fear&Greed 30(Fear) — 직전과 동일, 5회차 연속

alternative.me API 정상 응답, **30(Fear)** — 직전 회차(30)에서 변동 없이 유지, 5회차
연속 30을 이어가고 있다.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM 개별조회)는 **34회차 연속** 방법론(`oiUsd`
필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을 유지했다.
이번 회차는 OKX ACE-USDT-SWAP·TUT-USDT-SWAP·TOAD-USDT-SWAP·**JUGGERNAUT-USDT-SWAP**
전부 instId 자체가 존재하지 않아(에러코드 51001) 미상장이 확인됐다(ACE는 34회차 연속,
JUGGERNAUT은 이번 회차 신규 확인). CoinGecko `orangex_futures`·`dydx_chain`·`/global`은
1~2회 429를 겪은 뒤 재시도로 확보됐고, `binance_futures`·`bybit`·`okex_swap`·
`hyperliquid`·`aster`·Fear&Greed는 첫 시도에 정상 응답했다. Binance/Bybit 대량 티커
목록에서 BANK·BEAT를 검색할 때 일부 WebFetch 요약이 목록 중간에서 잘려 재조회가
필요했던 사례가 있었다(BANK는 재조회로 확인 완료, BEAT는 Binance/Bybit 미상장이
최종 재확인됨).

## 이번 회차 최대 사건

### ⚠️⚠️⚠️ MMT — 완전 반전, 수개월 미규명 원인 첫 규명

수개월간 '부분 회복, 원인 미규명'으로 남아있던 MMT가 이번 회차 **-13.640%→+2.204%로
완전히 플러스 전환**됐다. WebSearch로 원인을 처음 규명했다: 바이낸스가 **8/6 MMT 스팟
트레이딩 토너먼트**(최대 200만 MMT 보상 풀)를 열고 **8/7 BEP20 네트워크 입출금 지원**을
추가하면서 거래량이 1,230% 급증하고 숏 강제청산이 동반됐다는 보도를 확인했다
([cryptonews.net](https://cryptonews.net/news/altcoins/33230014/),
[coinpedia.org](https://coinpedia.org/news/why-is-momentum-mmt-token-price-up-by-77-today/amp/)).
7/31에도 77% 급등이 있었던 것으로 볼 때 이번 반전은 단발성 되돌림이 아니라 며칠째
이어지는 모멘텀 트레이드/토너먼트 효과일 가능성이 있다.

### BICO — 5회차 악화 종료 후 2회차 연속 강한 개선

OKX **-34.313%→-12.102%**, OrangeX **-34.802%→-10.338%**(펀딩 +0.322%→**+0.119%**),
Aster **-37.084%→-11.081%**로 3소스 전원 2회차 연속 개선됐다 — 5회차 악화 종료 이후
회복이 뚜렷하게 가속되는 국면이다.

### ⚠️ BEAT — 2회차 개선 종료, 재악화 반전

OKX **-19.087%→-24.739%**, OrangeX **-20.763%→-23.332%**, Aster **-20.471%→-27.199%**로
3소스 동조 재악화됐다 — 2회차 연속 이어지던 개선 흐름이 하루 만에 꺾였다.

### ⚠️⚠️ ADA — 소스 간 혼조 해소, 전 소스 마이너스로 방향성 확정

가중(Binance/Bybit) **+0.174%→-0.166%→-0.626%**로 마이너스가 깊어졌고, OKX
**-0.354%→-0.611%**, OrangeX **-0.051%→-0.916%**, Aster **+0.101%→-0.611%**(플러스에서
반전), HL **+0.061%→-0.804%**(플러스에서 반전)로 **전 소스가 마이너스로 수렴**했다 —
직전 회차의 방향성 미확정 상태가 이번 회차 해소됐다.

## 직전 회차 강조 종목 추적 결과

- **① BICO — 2회차 연속 강한 개선, 회복 가속.** 위 '최대 사건' 참조.
- **② BANK — 강한 플러스 유지, 소폭 냉각.** 가중 **+2.961%→+2.589%**, OrangeX
  **+2.178%→+1.914%**, Aster **+2.751%→+2.875%**로 대체로 유지 — 8/17 대형 언락 약
  **6.4일** 앞으로, 사전 포지셔닝 여부는 다음 회차도 계속 추적한다.
- **③ KAITO — 마이너스·펀딩 악화 지속.** OKX **-3.311%→-4.320%**(펀딩
  -0.563%→**-0.610%**로 추가 악화), HL **-3.75%→-4.703%**(펀딩 -0.287%→**-0.297%**로
  추가 악화) — 8/20 대형 언락($22.9M) 약 **9.4일** 앞, 숏 우위가 지속 강화되고 있다.
- **④ CAP — ⚠️ 소진 흐름에서 하루 만에 재반등.** OKX **+16.349%→+18.734%**, OrangeX
  **+18.813%→+18.824%**, Aster **+14.759%→+19.462%**로 3소스 동조 재상승 — 직전 회차
  관측한 '상장효과 소진' 추세가 하루 만에 되돌려져, 소진을 단정하기는 이르다.
- **⑤ CASHCAT — 2회차 연속 냉각 지속.** HL **40.719%→33.656%**, OrangeX
  **40.012%→36.024%**, Aster **39.525%→33.944%**로 3소스 전원 냉각이 이어졌다.
- **⑥ BLESS — 두 소스 모두 부분 회복.** OrangeX **-15.623%→-9.651%**, Aster
  **-12.463%→-11.268%** — WebSearch로 조사했으나 최근 급락·이번 반등의 구체 촉매는
  확인하지 못했다(2026년 4월 팀 매도 이력만 확인, 시점상 무관).

## 신규/추가 발견

### ⚠️ AKE·ATOM — 나란히 재반전, 휩쏘 패턴 심화

AKE는 다시 플러스로 반전했다: 가중 **-1.503%→+0.805%**, OrangeX **-1.498%→+0.454%**,
Aster **-1.266%→+0.786%**로 3소스 전원 재반전 — 최근 며칠 사이 플러스↔마이너스를
반복하는 급격한 휩쏘 패턴이 이어지고 있다. ATOM은 반대로 대부분 소스가 플러스에서
마이너스로 재반전했다: 가중 **+0.236%→-0.235%**, OrangeX **+0.218%→-0.073%**, HL
**+0.254%→-0.275%**, Aster만 **+0.291%→+0.146%**로 플러스를 유지했다.

### AAVE — 손익분기 근접까지 급격 냉각

가중 **+0.759%→+0.214%**, Aster **+0.699%→-0.033%**(소폭 마이너스 전환), OrangeX
**+0.776%→+0.011%**, HL **+0.606%→+0.089%**로 전 소스가 급격히 냉각됐다.

### ⚠️ 신규: JUGGERNAUT(Robinhood Chain) — 전 소스 미상장 확인

직전 온체인 루틴(10:09Z)이 신규 편입한 JUGGERNAUT(유동성 $404K)을 Binance·Bybit·
OKX(CoinGecko·직접)·Hyperliquid·Aster·OrangeX **전 소스에서 검색**했으나 어디에도
상장돼 있지 않음을 확인했다(OKX 직접조회는 instId 부재, 에러코드 51001) — 아직
선물화되지 않은 신생 온체인 토큰으로 판단된다.

### TUT·TOAD — 재확인, 전 소스 미상장 지속

OKX 직접조회(instId 부재, 51001)·Aster 서브스트링 검색 모두 재확인 결과 미발견,
Binance·Bybit·HL·OrangeX에서도 발견되지 않았다 — 이전 회차들과 동일하게 미상장이
지속되고 있다.

### BTW·ETHFI — 반대 방향 변동

BTW는 상승폭이 대폭 축소됐다(**+10.958%→+4.041%**) — 이전 확대 랠리에서 조정 국면.
ETHFI는 반대로 플러스 확대가 가속됐다(**+0.349%→+2.297%**).

### dYdX — ETH 마이너스 전환, BTC·SOL 대폭 냉각

ETH-USD **+0.453%→-0.141%**로 플러스에서 마이너스로 전환됐다. BTC-USD
**+0.621%→+0.148%**, SOL-USD **+0.641%→+0.052%**는 플러스를 유지했으나 큰 폭으로
냉각됐다.

## 데이터 이슈 추적 결과

GIGGLE 필드 이상치(vol24h=44,721,492 vs volCcy24h=447,214.92, 100배 스케일 차이)가
**19회차 연속**, KAITO(OKX 직접, vol24h=volCcy24h=97,734,455) 완전동일값 이상치가
**19회차 연속**, GRAM(vol24h=volCcy24h=2,524,765) 완전동일값 이상치가 **17회차 연속**
재현됐다. MMT·PIPPIN의 10배 스케일 비율(vol24h=volCcy24h÷10)이 이번 회차도 재현됐다
(MMT: 20,080,247/200,802,470, PIPPIN: 17,847,414/178,474,140) — **3회차 연속** 재현으로
구조적 패턴 가능성이 더욱 굳어졌다. HYNA:HYPE-USD의 OI는 이번 회차도 정상 갱신을
이어갔다($693,240.53→**$692,043.98**) — 정상화 **5회차 연속**.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **MMT** [⚠️⚠️⚠️ 완전 반전, 촉매 규명] | OKX(직접API) | $43.77M | $3.68M | -0.049% | +2.204% | -13.640%→+2.204%, 바이낸스 토너먼트+BEP20 통합 촉매 규명 | full-reversal-to-positive-catalyst-identified |
| **BICO** [2회차 연속 강한 개선] | OKX(CoinGecko정상, okex_swap) | $313.54M | $8.57M | -0.116% | -12.102% | -34.313%→-12.102%, 회복 가속 | recovery-accelerates-2nd-round |
| **BEAT** [⚠️ 2회차 개선 종료, 재악화] | OKX(CoinGecko정상, okex_swap) | $279.99M | $8.12M | -0.032% | -24.739% | -19.087%→-24.739% | improvement-ends-worsens-again |
| KAITO [마이너스·펀딩 악화 지속] | OKX(직접API) | $64.29M | $7.55M | -0.610% | -4.320% | -3.311%→-4.320%, 펀딩 -0.563%→-0.610%. 8/20 언락 9.4일 앞 | negative-and-funding-continue-worsening |
| BANK [강한 플러스 유지, 소폭 냉각] | Binance/Bybit(가중) | $102.27M | $18.83M | +0.002% | +2.589% | +2.961%→+2.589%. 8/17 언락 6.4일 앞 | strong-positive-holds-preunlock-watch |
| BSB [완화 흐름 지속] | OKX(CoinGecko정상, okex_swap) | $5.35M | $2.55M | +0.017% | -4.698% | -6.262%→-4.698% | improvement-continues |
| AAVE [손익분기 근접까지 냉각] | Binance/Bybit(가중) | $46.86M | $88.57M | +0.002% | +0.214% | +0.759%→+0.214% | cools-sharply-near-flat |
| ALLO [거의 유지] | Binance/Bybit(가중) | $21.05M | $18.12M | +0.005% | -2.409% | -2.580%→-2.409% | roughly-flat-within-negative |
| **ADA** [⚠️⚠️ 전 소스 마이너스 수렴] | Binance/Bybit(가중, USDT만) | $149.35M | $167.57M | +0.006% | -0.626% | 가중 -0.166%→-0.626%, 전 소스 마이너스로 수렴 | sources-converge-negative-direction-resolved |
| **AKE** [⚠️ 재반전 플러스] | Binance/Bybit(가중) | $39.65M | $37.53M | +0.036% | +0.805% | -1.503%→+0.805%, 휩쏘 지속 | whipsaw-reverses-positive-again |
| GIGGLE [개선, 이상치 19회차] | OKX(직접API) | $15.16M | $2.50M | +0.005% | -1.854% | -4.202%→-1.854% | improves-within-negative-field-anomaly-19th-round |
| PIPPIN [플러스 확대, 10x 3회차] | OKX(직접API) | $3.25M | $1.85M | +0.011% | +5.684% | +5.382%→+5.684%, 10배 비율 3회차 재현 | positive-extends-10x-pattern-3rd-round |
| 1000RATS [마이너스 심화 지속] | Binance/Bybit(가중) | $11.38M | $17.74M | +0.005% | -4.251% | -1.464%→-4.251% | negative-deepens-continues |
| AIO [Bybit 매칭 재개, 롤러코스터] | Binance/Bybit(가중) | $9.67M | $4.35M | +0.027% | +4.034% | Binance +5.711%→+4.035%, Bybit 재매칭 | rollercoaster-continues-bybit-rematches |
| GRAM [거의 유지, 이상치 17회차] | OKX(직접API) | $3.37M | $6.45M | +0.005% | -0.522% | -0.447%→-0.522% | roughly-flat-field-anomaly-17th-round |
| AEON [개선 3회차 연속] | OKX(CoinGecko정상, okex_swap) | $10.77M | $3.59M | +0.005% | -3.589% | -7.699%→-3.589% | improvement-continues-3rd-round |
| **ATOM** [⚠️ 대부분 소스 재반전 마이너스] | Binance/Bybit(가중) | $8.72M | $28.39M | +0.0004% | -0.235% | +0.236%→-0.235% | reverses-negative-most-sources |
| ASTER [플러스 유지, 냉각] | Binance/Bybit(가중) | $23.15M | $112.38M | +0.005% | +1.032% | +1.972%→+1.032% | cools-within-positive |
| CORE [거의 유지] | OKX(CoinGecko정상, okex_swap) | $1.83M | $1.01M | +0.010% | +1.915% | +1.703%→+1.915%, 초저유동성 | roughly-flat-positive-low-liquidity |
| **CAP** [⚠️ 하루 만에 재반등] | OKX(CoinGecko정상, okex_swap) | $119.48M | $4.73M | -0.051% | +18.734% | +16.349%→+18.734% | surge-rebounds-after-fade |
| ALGO [거의 유지, 소폭 개선] | Binance/Bybit(가중) | $17.68M | $14.56M | -0.004% | -4.143% | -4.890%→-4.143% | roughly-flat-slight-improvement |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| ACE-USD [개선 지속] | Hyperliquid | $1.79M | $1.35M | +0.001% | -4.609% | -7.768%→-4.609% | recovery-continues |
| ACE-USDT-PERPETUAL [개선 지속] | OrangeX | $33.42M | $10.96M | +0.013% | -3.574% | -9.309%→-3.574% | recovery-continues |
| ACE-USDT [개선 지속] | Aster | $0.26M | $0.03M | -0.003% | -4.521% | -8.297%→-4.521% | recovery-continues |
| **BEAT-USDT-PERPETUAL** [⚠️ 재악화] | OrangeX | $19.65M | $5.99M | -0.055% | -23.332% | -20.763%→-23.332% | improvement-ends-worsens-again |
| **BEAT-USDT** [⚠️ 재악화] | Aster | $7.15M | $0.88M | -0.015% | -27.199% | -20.471%→-27.199% | improvement-ends-worsens-again |
| **BICO-USDT-PERPETUAL** [2회차 강한 개선] | OrangeX | $118.13M | $42.61M | +0.119% | -10.338% | -34.802%→-10.338%, 펀딩 부호 개선 | recovery-accelerates-2nd-round |
| **BICO-USDT** [2회차 강한 개선] | Aster | $2.32M | $0.24M | -0.007% | -11.081% | -37.084%→-11.081% | recovery-accelerates-2nd-round |
| CASHCAT [2회차 냉각] | Hyperliquid | $18.97M | $22.18M | +0.001% | +33.656% | 40.719%→33.656% | cooling-continues-2nd-round |
| CASHCAT-USDT-PERPETUAL [2회차 냉각] | OrangeX | $0.15M | $0.06M | -0.029% | +36.024% | 40.012%→36.024% | cooling-continues-2nd-round |
| CASHCAT-USDT [2회차 냉각] | Aster | $2.31M | $1.60M | -0.025% | +33.944% | 39.525%→33.944% | cooling-continues-2nd-round |
| ALLO-USDT [거의 유지] | Aster | $0.10M | $0.03M | +0.001% | -2.257% | -1.787%→-2.257% | roughly-flat-within-negative |
| ALLO-USDT-PERPETUAL [거의 유지] | OrangeX | $13.76M | $4.71M | +0.010% | -2.184% | -2.127%→-2.184% | roughly-flat-within-negative |
| AAVE-USDT-PERPETUAL [손익분기 근접] | OrangeX | $26.39M | $9.23M | +0.010% | +0.011% | +0.776%→+0.011% | cools-sharply-near-flat |
| AAVE-USDT [소폭 마이너스 전환] | Aster | $0.44M | $4.53M | +0.010% | -0.033% | +0.699%→-0.033% | turns-slightly-negative |
| AAVE-USD [손익분기 근접] | Hyperliquid | $3.31M | $60.97M | +0.001% | +0.089% | +0.606%→+0.089% | cools-sharply-near-flat |
| ADA-USDT-PERPETUAL [마이너스 심화] | OrangeX | $81.02M | $28.37M | +0.010% | -0.916% | -0.051%→-0.916% | sources-converge-negative-direction-resolved |
| **ADA-USDT** [플러스에서 반전] | Aster | $0.56M | $1.69M | +0.005% | -0.611% | +0.101%→-0.611% | sources-converge-negative-direction-resolved |
| **ADA-USD** [플러스에서 반전] | Hyperliquid | $3.71M | $32.26M | -0.001% | -0.804% | +0.061%→-0.804% | sources-converge-negative-direction-resolved |
| BANK-USDT-PERPETUAL [강한 플러스 유지] | OrangeX | $7.40M | $2.53M | -0.020% | +1.914% | +2.178%→+1.914%. 8/17 언락 6.4일 앞 | strong-positive-holds-preunlock-watch |
| BANK-USDT [강한 플러스 확대] | Aster | $0.50M | $0.28M | 0.000% | +2.875% | +2.751%→+2.875%. 8/17 언락 6.4일 앞 | strong-positive-holds-preunlock-watch |
| **AKE-USDT-PERPETUAL** [재반전 플러스] | OrangeX | $5.15M | $1.68M | +0.034% | +0.454% | -1.498%→+0.454% | whipsaw-reverses-positive-again |
| **AKE-USDT** [재반전 플러스] | Aster | $0.67M | $10.52M | +0.011% | +0.786% | -1.266%→+0.786% | whipsaw-reverses-positive-again |
| **CAP-USDT** [재반등] | Aster | $0.12M | $0.14M | -0.001% | +19.462% | +14.759%→+19.462% | surge-rebounds-after-fade |
| CAP-USDT-PERPETUAL [유지, 소폭 재상승] | OrangeX | $0.65M | $0.24M | -0.105% | +18.824% | +18.813%→+18.824% | surge-rebounds-after-fade |
| ALGO-USDT-PERPETUAL [거의 유지] | OrangeX | $9.55M | $3.21M | +0.010% | -4.408% | -4.844%→-4.408% | roughly-flat-slight-improvement |
| ALGO-USDT [초저유동성, 거의 유지] | Aster | $0.04M | $0.02M | -0.002% | -4.224% | -5.25%→-4.224% | low-liquidity-roughly-flat |
| ALGO-USD [거의 유지] | Hyperliquid | $0.98M | $1.92M | +0.001% | -4.242% | -5.188%→-4.242% | roughly-flat-negative |
| **ATOM-USDT-PERPETUAL** [재반전 마이너스] | OrangeX | $4.66M | $1.65M | -0.010% | -0.073% | +0.218%→-0.073% | reverses-negative-most-sources |
| ATOM-USDT [초저유동성, 플러스 유지 냉각] | Aster | $0.006M | $1.60M | +0.009% | +0.146% | +0.291%→+0.146% | low-liquidity-holds-positive-cools |
| **ATOM-USD** [재반전 마이너스] | Hyperliquid | $0.21M | $1.91M | +0.001% | -0.275% | +0.254%→-0.275% | reverses-negative-most-sources |
| ASTER-USDT-PERPETUAL [완만한 상승, 냉각] | OrangeX | $9.07M | $3.03M | +0.010% | +0.882% | +2.086%→+0.882% | gentle-rise-cools |
| ASTER-USDT [대형 OI 유지, 냉각] | Aster | $15.18M | $221.09M | +0.009% | +0.997% | OI $222.69M→$221.09M | large-oi-positive-cools |
| ASTER-USD [완만한 상승, 냉각] | Hyperliquid | $1.64M | $14.64M | +0.001% | +0.871% | +1.991%→+0.871% | gentle-rise-cools |
| KAITO-USD [마이너스·펀딩 악화 지속] | Hyperliquid | $21.13M | $8.04M | -0.297% | -4.703% | -3.75%→-4.703%, 펀딩 -0.287%→-0.297% | negative-and-funding-continue-worsening |
| GRAM-USD [소폭 재악화] | Hyperliquid | $0.94M | $12.91M | +0.001% | -0.699% | -0.335%→-0.699% | roughly-flat-field-anomaly-17th-round |
| HYPE-USD [소폭 재전환 마이너스] | Hyperliquid | $107.21M | $1,178.55M | 0.000% | -0.220% | +0.033%→-0.22%, 손익분기권 유지 | turns-slightly-negative-near-flat |
| HYPER-USD [마이너스 심화] | Hyperliquid | $0.19M | $0.34M | +0.001% | -1.046% | -0.62%→-1.046% | negative-deepens |
| APEX-USD [마이너스 대폭 심화] | Hyperliquid | $0.26M | $0.70M | -0.003% | -4.501% | -2.238%→-4.501%, Bybit도 동조 | negative-deepens-sharply |
| FARTCOIN [플러스 확대] | Hyperliquid | $7.40M | $23.93M | +0.003% | +4.547% | +3.494%→+4.547% | extends-positive |
| ETHFI-USD [플러스 확대 가속] | Hyperliquid | $0.64M | $8.67M | +0.001% | +2.297% | +0.349%→+2.297% | extends-positive-accelerates |
| **ETH-USD** [마이너스 전환] | dYdX | $16.69M | $12.37M | 0.000% | -0.141% | +0.453%→-0.141% | turns-negative |
| BTC-USD [플러스 유지, 대폭 냉각] | dYdX | $1.92M | $17.87M | 0.000% | +0.148% | +0.621%→+0.148% | cools-sharply-within-positive |
| SOL-USD [플러스 유지, 대폭 냉각] | dYdX | $0.14M | $4.52M | 0.000% | +0.052% | +0.641%→+0.052% | cools-sharply-within-positive |
| ANSEM [플러스 유지, 소폭 냉각] | Aster | $0.22M | $1.02M | +0.001% | +4.913% | +5.341%→+4.913% | cools-within-positive |
| ANSEM-USDT-PERPETUAL [플러스 확대] | OrangeX | $0.50M | $0.18M | +0.010% | +4.057% | +3.683%→+4.057% | extends-positive |
| **BTW** [⚠️ 상승폭 대폭 축소] | Aster | $1.98M | $12.52M | +0.025% | +4.041% | +10.958%→+4.041% | rally-pulls-back-sharply |
| HYNA:PUMP-USD [플러스권 냉각 지속] | Hyperliquid | $0.05M | $0.18M | +0.001% | +7.726% | +11.423%→+7.726% | cools-within-positive |
| HYNA:HYPE-USD [OI 정상갱신 5회차] | Hyperliquid | $0.03M | $0.69M | +0.001% | +0.478% | $693,240.53→$692,043.98 | oi-normal-updates-continue-5th-round |
| AEON-USDT-PERPETUAL [개선 흐름, 소폭 반락] | OrangeX | $0.42M | $0.15M | +0.010% | -5.087% | -7.463%→-5.087% | improvement-continues-3rd-round |
| AEON-USDT [개선 3회차 연속] | Aster | $0.06M | $0.21M | +0.008% | -3.941% | -8.187%→-3.941% | improvement-continues-3rd-round |
| BSB-USDT-PERPETUAL [완화 흐름 지속] | OrangeX | $9.29M | $3.34M | +0.010% | -4.756% | -6.393%→-4.756% | improvement-continues |
| BSB-USDT [완화 흐름 지속] | Aster | $0.04M | $0.10M | +0.001% | -4.259% | -6.872%→-4.259% | improvement-continues |
| 1000RATS-USDT [마이너스 심화 지속] | Aster | $0.07M | $0.04M | +0.008% | -6.351% | -1.114%→-6.351% | negative-deepens-continues |
| AIO-USDT [플러스 확대] | Aster | $0.55M | $0.10M | +0.037% | +3.698% | +1.931%→+3.698% | rollercoaster-continues-bybit-rematches |
| BLESS [부분 회복] | OrangeX | $41.77M | $14.22M | +0.278% | -9.651% | -15.623%→-9.651%, 촉매 미규명 | partial-recovery-catalyst-unconfirmed |
| BLESS-USDT [부분 회복, 완만] | Aster | $0.25M | $0.23M | +0.012% | -11.268% | -12.463%→-11.268% | partial-recovery-catalyst-unconfirmed |

## 테마 태그

1. **시장 전반: `/global` 정상 응답, 13회차 연속 확보 — 총시총 $2.301T(소폭 하락)·BTC도미넌스 56.670%(소폭 하락)** (global-api-13th-round-normal).
2. **Fear&Greed 30(Fear) — 직전과 동일, 5회차 연속 유지** (fear-greed-holds-at-30-fifth-round).
3. **⚠️⚠️⚠️ MMT: 수개월 미규명 원인 첫 규명 — 바이낸스 토너먼트(8/6)+BEP20 통합(8/7)으로 완전 반전** (mmt-full-reversal-catalyst-identified).
4. **BICO: 5회차 악화 종료 후 2회차 연속 강한 개선, 회복 가속** (bico-recovery-accelerates-2nd-round).
5. **⚠️ BEAT: 2회차 개선 종료, 3소스 동조 재악화** (beat-improvement-ends-worsens-again).
6. **⚠️⚠️ ADA: 소스 간 혼조 해소, 전 소스 마이너스로 방향성 확정** (ada-sources-converge-negative-direction-resolved).
7. **⚠️ AKE: 재반전 플러스, 휩쏘 패턴 지속** (ake-whipsaw-reverses-positive-again).
8. **⚠️ ATOM: 대부분 소스 재반전 마이너스** (atom-reverses-negative-most-sources).
9. **BANK: 강한 플러스 유지, 소폭 냉각 — 8/17 언락 약 6.4일 앞** (bank-strong-positive-holds-preunlock-watch).
10. **KAITO: 마이너스·펀딩 악화 지속 — 8/20 대형 언락($22.9M) 약 9.4일 앞** (kaito-negative-funding-continue-worsening).
11. **⚠️ CAP: 소진 흐름에서 하루 만에 재반등, 3소스 동조** (cap-surge-rebounds-after-fade).
12. **CASHCAT: 2회차 연속 냉각 지속** (cashcat-cooling-continues-2nd-round).
13. **AEON: 개선 3회차 연속, 3소스 동조** (aeon-improvement-continues-3rd-round).
14. **AAVE: 손익분기 근접까지 급격 냉각** (aave-cools-sharply-near-flat).
15. **BTW: 상승폭 대폭 축소** (btw-rally-pulls-back-sharply).
16. **ETHFI: 플러스 확대 가속** (ethfi-extends-positive-accelerates).
17. **dYdX ETH 마이너스 전환, BTC·SOL 대폭 냉각** (dydx-eth-turns-negative-btc-sol-cool-sharply).
18. **⚠️ BLESS: 두 소스 모두 부분 회복, 촉매 여전히 미규명** (bless-partial-recovery-catalyst-unconfirmed).
19. **⚠️ TUT·TOAD 재확인: 전 소스 미상장 지속** (tut-toad-reconfirmed-unlisted).
20. **⚠️ 신규: JUGGERNAUT(Robinhood Chain) 전 소스 미상장 확인 — 아직 선물화 안 됨** (juggernaut-not-listed-any-futures-venue).
21. **GIGGLE 19회차·KAITO(OKX직접) 19회차·GRAM 17회차 필드 이상치 재현, MMT·PIPPIN 10배 비율 3회차 연속 재현** (field-anomalies-continue-10x-pattern-3rd-round).
22. **OKX ACE·TUT·TOAD·JUGGERNAUT 모두 instId 자체 부재 확인(ACE 34회차 연속)** (okx-multiple-symbols-not-listed).
23. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
24. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
25. **이번 회차 orangex_futures·dydx_chain·global은 1~2회 429 후 재시도로 확보** (rate-limiting-minor-this-round).
26. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**CoinGecko binance_futures**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS
확인. BANK는 최초 요약에서 목록 중간 절단으로 누락됐다가 **재조회로 확인 완료**했다
(vol $87.87M·oi $13.30M·chg +2.637%). **BICO·BEAT·BSB·APEX·BTW·KAITO·CASHCAT·MMT·GIGGLE·
PIPPIN·GRAM·CORE·CAP·AEON·BLESS·ANSEM·TUT·TOAD·JUGGERNAUT는 이번 회차도 명확히
미확인**(단순 미상장, BEAT는 재조회로 미상장 최종 재확인).

**CoinGecko bybit**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO(AIOUSDT 이번 회차 매칭 재개)·ATOM·
ASTER·ALGO·1000RATS·APEX 확인, 정상 응답. 나머지는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·CAP·BICO·BEAT 확인,
정상 응답. ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT·TUT·TOAD·
JUGGERNAUT는 이번 회차도 okex_swap 배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인.
`oiUsd` 필드 직접 사용 방법론을 **34회차 연속** 유지, vol24_usd=`volCcy24h`×`last` 계산
방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️ **ACE-USDT-SWAP·TUT-USDT-SWAP·
TOAD-USDT-SWAP·JUGGERNAUT-USDT-SWAP는 OKX에 instId 자체가 존재하지 않음**을 이번 회차도
직접 확인(에러코드 51001), ACE는 **34회차 연속**, JUGGERNAUT은 이번 회차 신규 확인.
**GIGGLE**은 raw JSON에서 `vol24h=44,721,492`·`volCcy24h=447,214.92`로 정확히 100배
스케일 차이가 나는 필드 이상치가 **19회차 연속**, **KAITO**는 `vol24h`=`volCcy24h`=
97,734,455로 완전동일값 이상치가 **19회차 연속**, **GRAM**도 `vol24h`=`volCcy24h`=
2,524,765로 완전동일값이 **17회차 연속** 재현됐다. **MMT**(vol24h=20,080,247,
volCcy24h=200,802,470)와 **PIPPIN**(vol24h=17,847,414, volCcy24h=178,474,140)의 10배
비율이 **3회차 연속** 재현돼 계약 승수 차이에 따른 구조적 패턴 가능성이 더욱 굳어졌다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·
ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD·BTC·ETH 등 raw 정밀값 확보(정상 응답). **SOL은 HL에서
이번 회차도 미확인**(기존 dYdX로 대체 집계). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·BTW·
BLESS·ANSEM·TUT·TOAD·JUGGERNAUT는 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·
BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON·AIO 전량 확보(raw 정밀값, 정상 응답).
MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견. **TUT·TOAD·JUGGERNAUT는
서브스트링 검색으로 재확인, 이번 회차도 미발견**.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값, 1~2회 429 후 재시도). BTW는 이번 회차도
OrangeX에서 미발견(기존과 동일, Aster에서만 확인). KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·
CORE·TUT·TOAD·JUGGERNAUT는 여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.92M/OI $17.87M, ETH-USD $16.69M/OI $12.37M,
SOL-USD $0.14M/OI $4.52M) 확보, 1~2회 429 후 재시도로 확보.

**CoinGecko `/global`**: 1~2회 429 후 재시도로 총시총 $2,301,326,971,009.47(약
$2.301T)·BTC도미넌스 56.670%를 확인했다. 직전 회차($2.308T·56.710%)보다 시총·도미넌스
모두 소폭 하락, **13회차 연속** 확보됐다.

**Fear&Greed**: alternative.me API로 정상 응답, **30(Fear)** 확인 — 직전과 동일, 5회차
연속 유지됐다.

**신규 발견**: (a) MMT가 수개월간 미규명이던 원인을 처음 규명했다 — 바이낸스 MMT
트레이딩 토너먼트(8/6)+BEP20 통합(8/7) 촉매로 완전 반전됐다(이번 회차 최대 사건).
(b) BICO가 5회차 악화 종료 이후 2회차 연속 강한 개선을 이어가며 회복이 가속되고 있다.
(c) BEAT는 반대로 2회차 개선 이후 재악화로 돌아섰다. (d) ADA는 소스 간 혼조가 해소되며
전 소스 마이너스로 방향성이 확정됐다. (e) AKE·ATOM이 나란히 재반전하며 급격한 휩쏘
패턴을 이어가고 있다(AKE는 플러스로, ATOM은 마이너스로). (f) CAP은 상장효과 소진
관측이 하루 만에 재반등으로 뒤집혀, 소진을 단정하기 이르다. (g) JUGGERNAUT(Robinhood
Chain, 온체인 루틴 신규편입)이 전 추적 선물 소스에서 미상장임을 확인했다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(34회차 연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은
본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상 스케일로
관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·
GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며,
이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·
HYNA:HYPE-USD·BLESS·AIO-USDT는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다;
(h) MMT의 반전 원인은 WebSearch로 규명했으나, 7/31 77% 급등과 이번 반전이 동일 재료의
연장인지 독립 사건인지는 완전히 구분하지 못했다; (i) BANK의 강한 플러스가 8/17 언락을
앞둔 실제 사전 포지셔닝인지, 단순 변동성인지는 여전히 규명하지 못했다 — 다음 회차 추적
필요; (j) BLESS의 급락·반등 촉매 모두 이번 회차도 조사했으나 확인하지 못했다 — 다음
회차 추적 필요; (k) KAITO 8/20 언락 규모는 소스별로 공급 3.3%~7.63%·$22.9M~$34.68M로
편차가 있었으며, 이번 회차는 재검증하지 않았다; (l) GIGGLE·KAITO의 필드 이상치가
19회차 연속, GRAM도 17회차 연속 재현돼 구조적 패턴으로 굳어졌으나 근본 원인(OKX API
자체 특성인지)은 규명하지 않았다; (m) JUGGERNAUT의 미상장이 온체인 유동성 부족 때문인지
단순 시차 때문인지는 다음 회차 추적이 필요하다; (n) BICO·CAP의 이번 회차 반등이 지속될지
일시적 되돌림인지는 표본이 부족해 다음 회차 추적이 필요하다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
