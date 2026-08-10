# 선물시장 스카우트 브리핑 — 2026-08-10 12:57 UTC (KST 2026-08-10 21:57)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-10T10:28:00Z)
> 로부터 약 2시간29분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 1~2회 429 후 재시도로 확보 — 총시총 **$2,298,214,056,632.08(약
$2.298T)**·BTC도미넌스 **56.660%**로 직전 회차($2.301T·56.670%)보다 시총·도미넌스 모두
소폭 하락, **14회차 연속** 확보됐다.

### Fear&Greed 30(Fear) — 직전과 동일, 6회차 연속

alternative.me API 정상 응답, **30(Fear)** — 직전 회차(30)에서 변동 없이 유지, 6회차
연속 30을 이어가고 있다.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM·BSB 개별조회)는 **35회차 연속** 방법론
(`oiUsd` 필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을
유지했다. 이번 회차는 OKX ACE-USDT-SWAP·TUT-USDT-SWAP·TOAD-USDT-SWAP 전부 instId
자체가 존재하지 않아(에러코드 51001) 미상장이 재확인됐다(ACE는 **35회차 연속**).
CoinGecko `orangex_futures`·`dydx_chain`·`/global`은 1~2회 429를 겪은 뒤 재시도로
확보됐고, `binance_futures`·`bybit`·`okex_swap`·`hyperliquid`·`aster`·Fear&Greed는
첫 시도에 정상 응답했다. Binance 대량 티커 목록에서 BANK를 검색할 때 최초 요약이
목록 중간에서 잘리는 사례가 **2회차째 재발**해 재조회로 확인했다(vol $65.19M·
OI $13.35M·chg -17.482%). BSB는 OKX CoinGecko(`okex_swap`)에서 이번 회차 발견되지
않아 OKX 직접 API로 집계 방식을 전환했다.

## 이번 회차 최대 사건

### ⚠️⚠️⚠️ BANK — 강한 플러스에서 급격한 마이너스 반전

직전 회차까지 강한 플러스를 유지하던 BANK가 이번 회차 급격히 반전됐다:
Binance/Bybit 가중 **+2.589%→-17.182%**(Binance -17.482%, Bybit -15.3%), OrangeX
**+1.914%→-16.33%**, Aster **+2.875%→-15.975%**로 전 소스 동조 급락했다. 펀딩도
**+0.002%→-0.039%**로 반전(숏 우위 전환)됐으나 OI는 **$18.83M→$18.83M**로 거의 그대로
유지돼, 대량 청산이 아니라 신규 숏 유입 또는 현물 매도 압력으로 해석된다. **8/17 대형
언락 약 6.2일 앞**을 두고 사전매도 압력이 본격화되는 모습일 가능성이 있으나, WebSearch로도
오늘 시점의 구체 촉매(해킹·공지 등)는 확인하지 못했다(2026년 6월 발생한 옛 토큰 대량발행
이슈만 확인됐고 오늘과는 무관).

### ⚠️⚠️ MMT — 완전 반전이 하루 만에 재역전

직전 회차의 완전 플러스 반전(-13.640%→+2.204%)이 하루 만에 다시 무너져
**+2.204%→-4.633%**로 재하락했다. WebSearch로 확인한 바 바이낸스 MMT 토너먼트發 펌프에
대해 '거래량이 $200M 아래로 줄어들면 반전 선행지표'라는 경고가 이미 있었는데, 실제로
되돌림이 발생한 것으로 토너먼트 단기 펌프가 소진되는 조짐으로 해석된다.

### ⚠️⚠️ ADA — 마이너스 수렴이 하루 만에 재붕괴

직전 회차의 '전 소스 마이너스 수렴'이 하루 만에 다시 무너져 혼조로 돌아갔다: 가중
**-0.626%→+0.048%**(Binance +0.153%·HL +0.163%로 플러스 전환), 반면 Bybit -0.204%·
OKX -0.153%·OrangeX -0.204%는 마이너스를 유지해 소스 간 방향이 다시 갈렸다 — 직전
회차의 '방향성 확정' 판단이 무색해졌다.

## 직전 회차 강조 종목 추적 결과

- **① BICO — 3회차 연속 개선, 소스 괴리 발생.** OKX **-12.102%→-5.845%**, Aster
  **-11.081%→-5.748%**로 추가 개선됐으나, OrangeX만 **-10.338%→-12.848%**로 홀로
  재악화됐다(펀딩 +0.119%→+0.177%로는 오히려 개선 방향).
- **② BEAT — 재악화 2회차 연속.** OKX **-24.739%→-26.777%**, OrangeX
  **-23.332%→-28.479%**, Aster **-27.199%→-26.78%**로 3소스 동조 심화됐다.
- **③ KAITO — 마이너스 지속, 악화 속도는 주춤.** OKX **-4.320%→-3.531%**(펀딩
  -0.610%→**-0.596%**로 소폭 완화), HL **-4.703%→-3.638%**(펀딩 -0.297%→**-0.300%**로
  거의 유지) — 8/20 대형 언락($22.9M) 약 **9.2일** 앞, 숏 우위는 이어지나 지난 여러
  회차의 악화 추세는 잠시 멈췄다.
- **④ AKE·ATOM — 나란히 재반전, 방향은 서로 교차.** AKE는 **+0.805%→-2.818%**(3소스
  전원 재반전 마이너스), ATOM은 **-0.235%→+0.654%**(3소스 전원 재반전 플러스)로 이번
  회차도 급격한 휩쏘가 이어지되 방향이 반대로 교차했다.
- **⑤ CAP — 3회차 연속 상승 후 첫 냉각.** OKX **+18.734%→+14.695%**, OrangeX
  **+18.824%→+12.645%**, Aster **+19.462%→+12.979%**로 3소스 동조 냉각됐다.
- **⑥ BLESS — ⚠️ 마이너스에서 플러스로 완전 반전.** OrangeX **-9.651%→+0.609%**, Aster
  **-11.268%→+0.716%**로 두 소스 모두 플러스 전환됐다 — 여러 회차 이어지던 부분 회복이
  완전한 방향 전환으로 마무리됐으나, 촉매는 이번 회차도 확인하지 못했다.

## 신규/추가 발견

### ⚠️ BSB — 수개월 마이너스 흐름에서 처음 플러스 전환

OKX **-4.698%→+1.211%**(OKX CoinGecko `okex_swap`에서 이번 회차 미발견돼 OKX 직접
API로 대체 집계), OrangeX **-4.756%→+0.606%**로 동조 반전 — 여러 회차 이어지던
마이너스 흐름이 처음으로 방향을 바꿨다.

### CASHCAT — 소스 간 괴리

HL이 **33.656%→36.244%**로 재가열된 반면, OrangeX는 **36.024%→25.081%**로 냉각을
이어갔고 Aster는 **33.944%→33.007%**로 거의 평행 유지됐다 — 세 소스가 서로 다른
방향으로 갈렸다.

### ⚠️ BTW — 플러스에서 마이너스로 급격 반전

**+4.041%→-7.114%**로 급격히 되돌려졌다 — 지난 회차 '상승폭 대폭 축소'에 이어 이번
회차는 완전히 방향이 바뀌었다.

### HYPE — 마이너스에서 플러스로 소폭 반전

**-0.220%→+1.444%**로 손익분기권에서 플러스로 돌아섰다.

### ACE — 개선 흐름 일시 정지

HL **-4.609%→-5.361%**, OrangeX **-3.574%→-7.188%**, Aster **-4.521%→-5.558%**로
3소스 모두 소폭 재악화됐다 — 이전 여러 회차 이어지던 개선 흐름이 잠시 멈췄다.

### dYdX — ETH 심화, BTC 손익분기권, SOL 반등

ETH-USD **-0.141%→-0.469%**로 마이너스가 더 깊어졌다. BTC-USD **+0.148%→+0.017%**로
손익분기권까지 냉각됐고, SOL-USD **+0.052%→+0.432%**로는 반등했다.

### AAVE — 손익분기권에서 플러스로 안정화

가중 **+0.214%→+0.325%**, Aster **-0.033%→+0.472%**(재전환), OrangeX
**+0.011%→+0.066%**, HL **+0.089%→+0.581%**로 전 소스가 플러스로 회복됐다.

### TUT·TOAD — 재확인, 미상장 지속

OKX 직접조회(instId 부재, 51001)로 재확인 결과 미발견이 지속됐다. ACE도 OKX에서
**35회차 연속** 미상장(instId 부재)이 확인됐다.

## 데이터 이슈 추적 결과

GIGGLE 필드 이상치(vol24h=42,317,250 vs volCcy24h=423,172.5, 100배 스케일 차이)가
**20회차 연속**, KAITO(OKX 직접, vol24h=volCcy24h=97,210,850) 완전동일값 이상치가
**20회차 연속**, GRAM(vol24h=volCcy24h=2,542,408) 완전동일값 이상치가 **18회차 연속**
재현됐다. MMT·PIPPIN의 10배 스케일 비율(MMT: vol24h 18,700,749/volCcy24h 187,007,490,
PIPPIN: vol24h 17,585,296/volCcy24h 175,852,960)이 이번 회차도 재현됐다 — **4회차
연속** 재현으로 구조적 패턴 가능성이 더욱 굳어졌다. HYNA:HYPE-USD의 OI는 이번 회차도
정상 갱신을 이어갔다($692,043.98→**$694,788.70**) — 정상화 **6회차 연속**.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BANK** [⚠️⚠️⚠️ 급격한 반전] | Binance/Bybit(가중) | $75.65M | $18.83M | -0.039% | -17.182% | +2.589%→-17.182%, 펀딩 숏우위 전환. 8/17 언락 6.2일 앞 | sharp-reversal-negative-preunlock-selling-pressure |
| **MMT** [⚠️⚠️ 완전반전 후 재역전] | OKX(직접API) | $39.65M | $3.39M | -0.001% | -4.633% | +2.204%→-4.633%, 토너먼트효과 소진 조짐 | reversal-fades-tournament-effect-cooling |
| BICO [3회차 연속 개선, 소스 괴리] | OKX(CoinGecko정상, okex_swap) | $272.33M | $8.24M | -0.089% | -5.845% | -12.102%→-5.845%, OrangeX만 재악화 | recovery-continues-3rd-round-orangex-diverges |
| BEAT [재악화 2회차 연속] | OKX(CoinGecko정상, okex_swap) | $291.30M | $8.23M | -0.021% | -26.777% | -24.739%→-26.777% | worsening-continues-2nd-round |
| **ADA** [⚠️⚠️ 마이너스 수렴 재붕괴] | Binance/Bybit(가중, USDT만) | $150.92M | $168.49M | +0.003% | +0.048% | 가중 -0.626%→+0.048%, 혼조 재발 | convergence-breaks-mixed-again |
| **AKE** [⚠️ 재역전 마이너스] | Binance/Bybit(가중) | $38.46M | $37.19M | +0.043% | -2.818% | +0.805%→-2.818% | whipsaw-reverses-negative-again |
| **ATOM** [⚠️ 재반전 플러스] | Binance/Bybit(가중) | $8.67M | $28.58M | +0.007% | +0.654% | -0.235%→+0.654% | whipsaw-reverses-positive-again |
| KAITO [마이너스 지속, 완화] | OKX(직접API) | $64.00M | $7.84M | -0.596% | -3.531% | -4.320%→-3.531%, 펀딩 -0.610%→-0.596%. 8/20 언락 9.2일 앞 | negative-persists-slight-easing |
| **BSB** [⚠️ 처음 플러스 전환] | OKX(직접API, 이번회차 okex_swap 미발견) | $6.33M | $2.66M | +0.025% | +1.211% | -4.698%→+1.211%, 수개월만에 방향전환 | turns-positive-first-time |
| AAVE [플러스로 안정화] | Binance/Bybit(가중) | $46.15M | $88.89M | -0.002% | +0.325% | +0.214%→+0.325%, 전 소스 회복 | stabilizes-positive-after-flat |
| ALLO [거의 유지] | Binance/Bybit(가중) | $20.72M | $18.17M | +0.005% | -2.077% | -2.409%→-2.077% | roughly-flat-slight-improvement |
| GIGGLE [개선, 이상치 20회차] | OKX(직접API) | $14.37M | $2.41M | +0.005% | -1.594% | -1.854%→-1.594% | improves-within-negative-field-anomaly-20th-round |
| PIPPIN [냉각, 10x 4회차] | OKX(직접API) | $3.20M | $1.85M | +0.020% | +2.946% | +5.684%→+2.946%, 10배 비율 4회차 재현 | cools-within-positive-10x-pattern-4th-round |
| 1000RATS [마이너스 심화 지속] | Binance/Bybit(가중) | $11.58M | $17.67M | +0.005% | -5.156% | -4.251%→-5.156% | negative-deepens-continues |
| AIO [롤러코스터, 확대] | Binance/Bybit(가중) | $9.63M | $4.50M | +0.032% | +7.934% | +4.034%→+7.934% | rollercoaster-continues-extends-positive |
| GRAM [거의 유지, 이상치 18회차] | OKX(직접API) | $3.38M | $6.40M | +0.005% | -0.672% | -0.522%→-0.672% | roughly-flat-field-anomaly-18th-round |
| AEON [개선 4회차 연속] | OKX(CoinGecko정상, okex_swap) | $9.67M | $3.64M | +0.005% | -2.889% | -3.589%→-2.889% | improvement-continues-4th-round |
| ASTER [플러스 유지, 냉각] | Binance/Bybit(가중) | $25.20M | $112.92M | +0.005% | +0.757% | +1.032%→+0.757% | cools-within-positive |
| CORE [소폭 마이너스 전환] | OKX(CoinGecko정상, okex_swap) | $1.71M | $1.00M | +0.010% | -0.348% | +1.915%→-0.348%, 초저유동성 | turns-slightly-negative-low-liquidity |
| CAP [3회차 상승 후 첫 냉각] | OKX(CoinGecko정상, okex_swap) | $125.67M | $4.11M | -0.016% | +14.695% | +18.734%→+14.695% | rally-cools-after-rebound |
| ALGO [거의 유지, 소폭 개선] | Binance/Bybit(가중) | $18.32M | $14.74M | -0.001% | -3.851% | -4.143%→-3.851% | roughly-flat-slight-improvement |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| ACE-USD [개선 일시 정지] | Hyperliquid | $1.75M | $1.38M | +0.001% | -5.361% | -4.609%→-5.361% | recovery-pauses-slight-worsening |
| ACE-USDT-PERPETUAL [개선 일시 정지] | OrangeX | $30.71M | $10.18M | +0.010% | -7.188% | -3.574%→-7.188% | recovery-pauses-slight-worsening |
| ACE-USDT [개선 일시 정지] | Aster | $0.24M | $0.03M | 0.000% | -5.558% | -4.521%→-5.558% | recovery-pauses-slight-worsening |
| BEAT-USDT-PERPETUAL [재악화 2회차] | OrangeX | $19.00M | $5.20M | -0.026% | -28.479% | -23.332%→-28.479% | worsening-continues-2nd-round |
| BEAT-USDT [거의 유지] | Aster | $7.57M | $1.02M | -0.027% | -26.780% | -27.199%→-26.78% | worsening-continues-2nd-round |
| **BICO-USDT-PERPETUAL** [홀로 재악화] | OrangeX | $93.57M | $29.38M | +0.177% | -12.848% | -10.338%→-12.848% | recovery-continues-3rd-round-orangex-diverges |
| BICO-USDT [3회차 연속 개선] | Aster | $2.10M | $0.24M | +0.001% | -5.748% | -11.081%→-5.748% | recovery-continues-3rd-round-orangex-diverges |
| **CASHCAT** [⚠️ 재가열] | Hyperliquid | $18.10M | $23.05M | +0.001% | +36.244% | 33.656%→36.244% | reheats-diverges-from-other-venues |
| CASHCAT-USDT-PERPETUAL [냉각 지속] | OrangeX | $0.15M | $0.06M | -0.029% | +25.081% | 36.024%→25.081% | cooling-continues-diverges-from-hl |
| CASHCAT-USDT [평행 유지] | Aster | $2.55M | $1.64M | +0.011% | +33.007% | 33.944%→33.007% | roughly-flat-high-positive |
| ALLO-USDT [소폭 개선] | Aster | $0.09M | $0.03M | +0.001% | -1.349% | -2.257%→-1.349% | roughly-flat-slight-improvement |
| ALLO-USDT-PERPETUAL [소폭 개선] | OrangeX | $13.47M | $4.82M | +0.010% | -1.815% | -2.184%→-1.815% | roughly-flat-slight-improvement |
| AAVE-USDT-PERPETUAL [플러스 유지] | OrangeX | $26.57M | $9.40M | +0.010% | +0.066% | +0.011%→+0.066% | stabilizes-positive-after-flat |
| AAVE-USDT [플러스로 재전환] | Aster | $0.42M | $4.55M | +0.010% | +0.472% | -0.033%→+0.472% | stabilizes-positive-after-flat |
| AAVE-USD [플러스 확대] | Hyperliquid | $3.34M | $61.23M | +0.001% | +0.581% | +0.089%→+0.581% | stabilizes-positive-after-flat |
| ADA-USDT-PERPETUAL [마이너스 완화] | OrangeX | $81.99M | $30.02M | +0.010% | -0.204% | -0.916%→-0.204% | convergence-breaks-mixed-again |
| ADA-USDT [손익분기권 근접] | Aster | $0.62M | $1.70M | +0.003% | -0.051% | -0.611%→-0.051% | convergence-breaks-mixed-again |
| **ADA-USD** [플러스로 재반전] | Hyperliquid | $3.61M | $32.38M | -0.001% | +0.163% | -0.804%→+0.163% | convergence-breaks-mixed-again |
| **BANK-USDT-PERPETUAL** [⚠️⚠️⚠️ 급격한 반전] | OrangeX | $6.84M | $2.51M | -0.030% | -16.330% | +1.914%→-16.33%. 8/17 언락 6.2일 앞 | sharp-reversal-negative-preunlock-selling-pressure |
| **BANK-USDT** [⚠️⚠️⚠️ 급격한 반전] | Aster | $0.39M | $0.26M | -0.015% | -15.975% | +2.875%→-15.975%. 8/17 언락 6.2일 앞 | sharp-reversal-negative-preunlock-selling-pressure |
| **AKE-USDT-PERPETUAL** [재역전 마이너스] | OrangeX | $5.56M | $1.77M | +0.044% | -2.924% | +0.454%→-2.924% | whipsaw-reverses-negative-again |
| **AKE-USDT** [재역전 마이너스] | Aster | $0.62M | $10.32M | +0.014% | -3.002% | +0.786%→-3.002% | whipsaw-reverses-negative-again |
| CAP-USDT [상승 후 첫 냉각] | Aster | $0.13M | $0.14M | +0.001% | +12.979% | +19.462%→+12.979% | rally-cools-after-rebound |
| CAP-USDT-PERPETUAL [상승 후 첫 냉각] | OrangeX | $0.68M | $0.22M | -0.060% | +12.645% | +18.824%→+12.645% | rally-cools-after-rebound |
| ALGO-USDT-PERPETUAL [거의 유지] | OrangeX | $9.80M | $3.26M | +0.010% | -3.837% | -4.408%→-3.837% | roughly-flat-slight-improvement |
| ALGO-USDT [초저유동성, 거의 유지] | Aster | $0.04M | $0.02M | 0.000% | -3.701% | -4.224%→-3.701% | low-liquidity-roughly-flat |
| ALGO-USD [거의 유지] | Hyperliquid | $0.99M | $1.91M | +0.001% | -3.860% | -4.242%→-3.860% | roughly-flat-negative |
| ATOM-USDT-PERPETUAL [재반전 플러스] | OrangeX | $4.55M | $1.70M | +0.010% | +0.437% | -0.073%→+0.437% | whipsaw-reverses-positive-again |
| ATOM-USDT [초저유동성, 확대] | Aster | $0.005M | $1.60M | +0.010% | +0.437% | +0.146%→+0.437% | whipsaw-reverses-positive-again |
| ATOM-USD [재반전 플러스] | Hyperliquid | $0.20M | $1.91M | +0.001% | +0.516% | -0.275%→+0.516% | whipsaw-reverses-positive-again |
| ASTER-USDT-PERPETUAL [완만한 냉각] | OrangeX | $9.38M | $3.26M | +0.010% | +0.679% | +0.882%→+0.679% | gentle-rise-cools |
| ASTER-USDT [대형 OI 유지, 냉각] | Aster | $16.15M | $221.66M | +0.003% | +0.794% | OI $221.09M→$221.66M | large-oi-positive-cools |
| ASTER-USD [완만한 냉각] | Hyperliquid | $1.69M | $14.69M | +0.001% | +0.828% | +0.871%→+0.828% | gentle-rise-cools |
| KAITO-USD [마이너스 지속, 완화] | Hyperliquid | $22.15M | $7.76M | -0.300% | -3.638% | -4.703%→-3.638%, 펀딩 -0.297%→-0.300% | negative-persists-slight-easing |
| GRAM-USD [거의 유지] | Hyperliquid | $1.05M | $12.82M | +0.001% | -0.724% | -0.699%→-0.724% | roughly-flat-field-anomaly-18th-round |
| HYPE-USD [플러스로 재반전] | Hyperliquid | $111.11M | $1,187.69M | +0.001% | +1.444% | -0.220%→+1.444% | turns-positive-again |
| HYPER-USD [거의 유지] | Hyperliquid | $0.18M | $0.33M | +0.001% | -1.108% | -1.046%→-1.108% | roughly-flat-negative |
| APEX-USD [소폭 개선] | Hyperliquid | $0.27M | $0.71M | -0.003% | -3.969% | -4.501%→-3.969%, Bybit도 동조 | slight-improvement-within-negative |
| FARTCOIN [플러스 확대] | Hyperliquid | $7.34M | $24.05M | +0.001% | +4.807% | +4.547%→+4.807% | extends-positive |
| ETHFI-USD [강한 플러스 유지] | Hyperliquid | $0.61M | $8.67M | +0.001% | +1.966% | +2.297%→+1.966% | extends-positive-slight-cooldown |
| **ETH-USD** [마이너스 심화] | dYdX | $16.79M | $12.26M | +0.001% | -0.469% | -0.141%→-0.469% | negative-deepens |
| BTC-USD [손익분기권까지 냉각] | dYdX | $1.85M | $17.83M | 0.000% | +0.017% | +0.148%→+0.017% | cools-sharply-near-flat |
| SOL-USD [반등] | dYdX | $0.14M | $4.52M | 0.000% | +0.432% | +0.052%→+0.432% | rebounds-within-positive |
| ANSEM [냉각] | Aster | $0.23M | $0.98M | +0.001% | +2.304% | +4.913%→+2.304% | cools-within-positive |
| ANSEM-USDT-PERPETUAL [냉각] | OrangeX | $0.50M | $0.19M | +0.010% | +0.916% | +4.057%→+0.916% | cools-within-positive |
| **BTW** [⚠️ 급격 반전 마이너스] | Aster | $2.05M | $12.34M | +0.018% | -7.114% | +4.041%→-7.114% | turns-negative-sharp-reversal |
| HYNA:PUMP-USD [플러스권 냉각 지속] | Hyperliquid | $0.05M | $0.18M | +0.001% | +4.009% | +7.726%→+4.009% | cools-within-positive |
| HYNA:HYPE-USD [OI 정상갱신 6회차] | Hyperliquid | $0.03M | $0.69M | +0.003% | +1.149% | $692,043.98→$694,788.70 | oi-normal-updates-continue-6th-round |
| AEON-USDT-PERPETUAL [개선 지속] | OrangeX | $0.42M | $0.15M | +0.010% | -3.886% | -5.087%→-3.886% | improvement-continues-4th-round |
| AEON-USDT [개선 4회차 연속] | Aster | $0.05M | $0.22M | +0.015% | -3.790% | -3.941%→-3.79% | improvement-continues-4th-round |
| **BSB-USDT-PERPETUAL** [⚠️ 처음 플러스 전환] | OrangeX | $10.03M | $3.66M | +0.010% | +0.606% | -4.756%→+0.606% | turns-positive-first-time |
| BSB-USDT [마이너스 완화] | Aster | $0.04M | $0.11M | +0.001% | -1.654% | -4.259%→-1.654% | turns-positive-first-time |
| 1000RATS-USDT [소폭 개선] | Aster | $0.07M | $0.04M | +0.001% | -5.367% | -6.351%→-5.367% | negative-deepens-continues |
| AIO-USDT [플러스 확대] | Aster | $0.56M | $0.11M | +0.066% | +6.459% | +3.698%→+6.459% | rollercoaster-continues-extends-positive |
| **BLESS** [⚠️ 완전 반전 플러스] | OrangeX | $40.52M | $16.04M | +0.237% | +0.609% | -9.651%→+0.609%, 촉매 미규명 지속 | turns-positive-catalyst-still-unconfirmed |
| BLESS-USDT [완전 반전 플러스] | Aster | $0.25M | $0.22M | +0.012% | +0.716% | -11.268%→+0.716% | turns-positive-catalyst-still-unconfirmed |

## 테마 태그

1. **시장 전반: `/global` 14회차 연속 확보 — 총시총 $2.298T(소폭 하락)·BTC도미넌스 56.660%(소폭 하락)** (global-api-14th-round-normal).
2. **Fear&Greed 30(Fear) — 직전과 동일, 6회차 연속 유지** (fear-greed-holds-at-30-sixth-round).
3. **⚠️⚠️⚠️ BANK: 강한 플러스에서 급격한 마이너스 반전, 8/17 언락 6.2일 앞 사전매도 압력 가능성** (bank-sharp-reversal-negative-preunlock-selling-pressure).
4. **⚠️⚠️ MMT: 완전 반전이 하루 만에 재역전, 토너먼트 효과 소진 조짐** (mmt-reversal-fades-tournament-cooling).
5. **BICO: 3회차 연속 개선(OKX·Aster), OrangeX만 홀로 재악화** (bico-recovery-continues-3rd-round-orangex-diverges).
6. **BEAT: 재악화 2회차 연속, 3소스 동조 심화** (beat-worsening-continues-2nd-round).
7. **⚠️⚠️ ADA: 마이너스 수렴이 하루 만에 재붕괴, 혼조 재발** (ada-convergence-breaks-mixed-again).
8. **⚠️ AKE·ATOM: 나란히 재반전하되 방향 교차, 휩쏘 심화** (ake-atom-cross-direction-whipsaw).
9. **KAITO: 마이너스 지속이나 악화 속도 주춤 — 8/20 대형 언락($22.9M) 약 9.2일 앞** (kaito-negative-persists-slight-easing).
10. **⚠️ BSB: 수개월 마이너스에서 처음 플러스 전환** (bsb-turns-positive-first-time).
11. **⚠️ BLESS: 마이너스에서 플러스로 완전 반전, 촉매 여전히 미규명** (bless-turns-positive-catalyst-unconfirmed).
12. **CAP: 3회차 연속 상승 후 첫 냉각, 3소스 동조** (cap-rally-cools-after-rebound).
13. **CASHCAT: 소스 간 괴리(HL 재가열, OrangeX 냉각 지속, Aster 평행)** (cashcat-diverges-across-venues).
14. **AEON: 개선 4회차 연속, 3소스 동조** (aeon-improvement-continues-4th-round).
15. **AAVE: 손익분기권에서 플러스로 안정화, 전 소스 회복** (aave-stabilizes-positive-after-flat).
16. **⚠️ BTW: 플러스에서 마이너스로 급격 반전** (btw-turns-negative-sharp-reversal).
17. **HYPE: 마이너스에서 플러스로 소폭 반전** (hype-turns-positive-again).
18. **dYdX: ETH 마이너스 심화, BTC 손익분기권까지 냉각, SOL 반등** (dydx-eth-deepens-btc-flat-sol-rebounds).
19. **ACE: 개선 흐름 일시 정지, 3소스 모두 소폭 재악화** (ace-recovery-pauses-slight-worsening).
20. **⚠️ TUT·TOAD·OKX ACE 재확인: 미상장 지속(ACE 35회차 연속)** (tut-toad-ace-reconfirmed-unlisted).
21. **GIGGLE 20회차·KAITO(OKX직접) 20회차·GRAM 18회차 필드 이상치 재현, MMT·PIPPIN 10배 비율 4회차 연속 재현** (field-anomalies-continue-10x-pattern-4th-round).
22. **HYNA:HYPE OI 정상 갱신 6회차 연속** (hyna-hype-oi-normal-6th-round).
23. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
24. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
25. **이번 회차 orangex_futures·dydx_chain·global은 1~2회 429 후 재시도로 확보, Binance BANK 목록 절단 2회차째 재발(재조회로 확인)** (rate-limiting-and-list-truncation-this-round).
26. **BSB는 이번 회차 OKX CoinGecko(okex_swap)에서 미발견돼 OKX 직접 API로 집계 방식 전환** (bsb-source-switched-to-okx-direct).
27. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**CoinGecko binance_futures**: AAVE·ALLO·ADA·AKE·1000RATS·AIO·ATOM·ASTER·ALGO 확인.
**BANK는 최초 검색에서 목록 절단으로 누락됐다가 재조회로 확인 완료**했다(vol $65.19M·
OI $13.35M·chg -17.482%, 2회차 연속 재발). **BICO·BEAT·BSB·KAITO·GIGGLE·PIPPIN·GRAM·
CORE·CAP·AEON·MMT는 이번 회차도 명확히 미확인**(단순 미상장).

**CoinGecko bybit**: AAVE·ALLO·ADA·AKE·AIO·ATOM·ASTER·ALGO·APEX·BANK·1000RATS 확인,
정상 응답. 나머지는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: BICO·BEAT·AAVE·ALLO·ADA·AEON·ATOM·ASTER·CORE·CAP·ALGO 확인,
정상 응답. **BSB는 이번 회차 okex_swap 배열에서 미발견돼 OKX 직접 API로 대체 집계**.
MMT·KAITO·AKE·GIGGLE·PIPPIN·1000RATS·AIO·GRAM·BANK는 이번 회차도 okex_swap 배열에서
미발견돼 OKX 직접 API 또는 Binance/Bybit/DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM·BSB)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접
확인. `oiUsd` 필드 직접 사용 방법론을 **35회차 연속** 유지, vol24_usd=`volCcy24h`×
`last` 계산 방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️
**ACE-USDT-SWAP·TUT-USDT-SWAP·TOAD-USDT-SWAP는 OKX에 instId 자체가 존재하지 않음**을
이번 회차도 직접 확인(에러코드 51001), ACE는 **35회차 연속**. **GIGGLE**은 raw
JSON에서 `vol24h=42,317,250`·`volCcy24h=423,172.5`로 정확히 100배 스케일 차이가 나는
필드 이상치가 **20회차 연속**, **KAITO**는 `vol24h`=`volCcy24h`=97,210,850으로
완전동일값 이상치가 **20회차 연속**, **GRAM**도 `vol24h`=`volCcy24h`=2,542,408로
완전동일값이 **18회차 연속** 재현됐다. **MMT**(vol24h=18,700,749,
volCcy24h=187,007,490)와 **PIPPIN**(vol24h=17,585,296, volCcy24h=175,852,960)의
10배 비율이 **4회차 연속** 재현돼 계약 승수 차이에 따른 구조적 패턴 가능성이 더욱
굳어졌다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·
ETHFI·ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD·BTC·ETH 등 raw 정밀값 확보(정상 응답). **SOL은
HL에서 이번 회차도 미확인**(기존 dYdX로 대체 집계). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·
ALLO·BTW·BLESS·ANSEM·TUT·TOAD는 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·
CAP·BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON·AIO 전량 확보(raw 정밀값,
정상 응답). MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견. TUT·TOAD는
이번 회차 별도 재확인하지 않았다(직전 회차 서브스트링 검색 결과 유지).

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·
BANK·AKE·CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값, 1~2회 429 후 재시도). BTW는
이번 회차도 OrangeX에서 미발견(기존과 동일, Aster에서만 확인). KAITO·1000RATS·GRAM·
MMT·PIPPIN·GIGGLE·CORE는 여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.85M/OI $17.83M, ETH-USD $16.79M/
OI $12.26M, SOL-USD $0.14M/OI $4.52M) 확보, 1~2회 429 후 재시도로 확보.

**CoinGecko `/global`**: 1~2회 429 후 재시도로 총시총 $2,298,214,056,632.08(약
$2.298T)·BTC도미넌스 56.660%를 확인했다. 직전 회차($2.301T·56.670%)보다 시총·도미넌스
모두 소폭 하락, **14회차 연속** 확보됐다.

**Fear&Greed**: alternative.me API로 정상 응답, **30(Fear)** 확인 — 직전과 동일,
6회차 연속 유지됐다.

**신규 발견**: (a) BANK가 강한 플러스에서 급격한 마이너스로 반전됐다 — 8/17 언락을
앞둔 사전매도 압력 가능성이 있으나 확정 촉매는 미규명(이번 회차 최대 사건). (b) MMT의
완전 반전이 하루 만에 재역전돼, 바이낸스 토너먼트 효과가 이미 소진되는 조짐을 보인다.
(c) ADA는 직전 회차의 방향성 확정이 재붕괴되며 다시 소스 간 혼조로 돌아갔다. (d) AKE·
ATOM이 이번 회차도 나란히 재반전했으나 방향이 서로 교차했다(AKE 마이너스, ATOM
플러스). (e) BSB·BLESS 두 종목 모두 수개월 이어지던 마이너스 흐름에서 처음으로
플러스 전환됐다. (f) CASHCAT은 세 소스가 서로 다른 방향(HL 재가열·OrangeX 냉각·Aster
평행)으로 갈리는 드문 괴리를 보였다. (g) BTW는 상승 랠리에서 급격히 마이너스로
반전됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM·BSB(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(35회차 연속 일관 적용); (d) ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소
값은 본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상
스케일로 관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·
PIPPIN·KAITO·GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만
집계되는 구조이며, 이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·
ANSEM·HYNA:PUMP-USD·HYNA:HYPE-USD·BLESS·AIO-USDT는 DEX에서만 상장이 확인돼 해당
섹션에서만 집계했다; (h) BANK의 급격한 반전은 8/17 언락을 앞둔 사전매도 압력인지,
단순 변동성인지 구체 촉매를 확인하지 못했다 — 다음 회차 최우선 추적 필요; (i) MMT의
재역전이 토너먼트 종료에 따른 자연스러운 되돌림인지 다른 요인인지는 완전히 구분하지
못했다; (j) BLESS·BSB의 완전 반전 촉매도 이번 회차 조사했으나 확인하지 못했다 — 다음
회차 추적 필요; (k) KAITO 8/20 언락 규모는 소스별로 공급 3.3%~7.63%·$22.9M~$34.68M로
편차가 있었으며, 이번 회차는 재검증하지 않았다; (l) GIGGLE·KAITO의 필드 이상치가
20회차 연속, GRAM도 18회차 연속 재현돼 구조적 패턴으로 굳어졌으나 근본 원인(OKX API
자체 특성인지)은 규명하지 않았다; (m) TUT·TOAD는 이번 회차 Aster·Binance·Bybit·HL·
OrangeX에서 별도 재확인하지 않고 직전 회차 결과를 유지했다; (n) BICO·CASHCAT의 소스
간 괴리(OrangeX만 반대 방향)가 일시적 노이즈인지 구조적 차이(펀딩·유동성 차이 등)인지
다음 회차 추적이 필요하다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
