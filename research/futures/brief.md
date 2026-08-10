# 선물시장 스카우트 브리핑 — 2026-08-10 06:40 UTC (KST 2026-08-10 15:40)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-10T02:30:00Z)
> 로부터 약 4시간10분 경과**(04:29Z 회차는 산출물 없이 종료돼 건너뜀).

## 이번 회차 핵심 요약

CoinGecko `/global`이 정상 응답으로 확보 — 총시총 **$2,305,263,192,865.03(약 $2.305T)**·
BTC도미넌스 **56.687%**로 직전 회차($2.298T·56.67%)보다 시총·도미넌스 모두 소폭 상승,
**11회차 연속** 확보됐다.

### Fear&Greed 30(Fear) — 직전과 동일, 3회차 연속

alternative.me API 정상 응답, **30(Fear)** — 직전 회차(30)에서 변동 없이 유지, 3회차
연속 30을 이어가고 있다.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM 개별조회)는 **32회차 연속** 방법론(`oiUsd`
필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을 유지했다.
이번 회차는 CoinGecko `orangex_futures`·`hyperliquid`가 각 2~3회 429를 겪은 뒤 재시도로
확보됐고, `dydx_chain`·`okex_swap`·`binance_futures`·`bybit`·`aster`·`/global`·Fear&Greed는
첫 시도에 정상 응답했다 — 직전 회차보다 레이트리밋이 다소 완화됐다.

## 이번 회차 최대 사건

### ⚠️ ACE — 소스 간 혼조 해소, 5소스 전원 개선

직전 회차의 소스 간 혼조가 이번 회차 완전히 해소되며 5개 소스 전원 개선됐다: Binance
**-14.604%→-11.126%**, Bybit **-16.69%→-11.491%**, OrangeX **-14.026%→-10.342%**, Aster
**-14.694%→-11.028%**, Hyperliquid **-17.503%→-11.224%**. Binance/Bybit 거래량가중은
**-15.108%→-11.220%**. OI는 계속 완만히 감소(포지션 정리 지속). OKX 직접조회로
ACE-USDT-SWAP를 재확인한 결과 이번 회차도 instId 자체가 존재하지 않아(에러코드 51001)
OKX 미상장이 **32회차 연속** 재확인됐다.

### ⚠️⚠️⚠️ BICO — 5회차 연속 악화, 최대낙폭 추가 경신 (숏스퀴즈 되돌림으로 해석)

5회차 연속 악화로 **-45~47%대**까지 추가로 밀려 최대낙폭을 또다시 경신했다. OKX
**-36.816%→-45.808%**, OrangeX **-37.822%→-46.811%**, Aster **-36.479%→-45.397%**.
WebSearch로 새로 확인한 사실: **8/4 Aster DEX가 BICO 5x 퍼프를 상장**하고 8/11 23:59 UTC까지
트레이딩 포인트 보상을 진행했으며, 이에 따른 숏스퀴즈로 **8/7 BICO가 +75.3% 급등**했었다
([coingabbar.com](https://www.coingabbar.com/en/price-prediction/biconomy-bico-price-prediction-perp-listing-surge)).
그러나 그 스퀴즈 랠리는 완전히 역전돼 지금은 신저점을 계속 경신 중이며, 전형적인
**'퍼프 상장發 숏스퀴즈 후 되돌림'** 패턴으로 해석 가능하다.

### ⚠️⚠️ BEAT — 완전 반전 이후 하락 지속·심화

완전 반전 이후 하락이 이어지며 추가로 심화됐다: OKX **-12.21%→-22.742%**, OrangeX
**-13.424%→-22.953%**, Aster **-11.263%→-23.38%**.

## 직전 회차 강조 종목 추적 결과

- **① ACE — ⚠️ 회복 재개, 5소스 전원 개선.** 위 '최대 사건' 참조.
- **② BICO — ⚠️⚠️⚠️ 5회차 연속 악화, 최대낙폭 추가 경신.** 위 참조 — '바닥 신호' 없이
  오히려 더 깊은 신저점, 신규 퍼프 상장 뉴스와의 상충 관계는 '숏스퀴즈 되돌림'으로 정합됐다.
- **③ BEAT — ⚠️⚠️ 완전 반전 이후 추가 심화.** 위 참조.
- **④ KAITO — 4번째 휩쏘, 재차 마이너스 전환.** 직전 회차의 혼조 해소(플러스 전환)가
  다시 뒤집혔다: OKX **+0.172%→-2.889%**(펀딩 -0.185%→-0.128%), HL **-0.653%→-2.825%**
  (펀딩 -0.109%→-0.091%)로 동조 악화. 8/20 대형 언락 약 9.6일 앞.
- **⑤ BANK — 플러스 모멘텀 크게 정체·일부 재반전.** Binance/Bybit 가중 **+1.148%→+0.172%**
  로 크게 냉각, OrangeX **+1.297%→-0.01%**(손익분기), Aster **+2.137%→-0.231%**(마이너스
  재전환)로 4소스 중 2곳이 반전됐다. 8/17 언락 약 6.5일 앞.
- **⑥ CASHCAT — ⚠️⚠️⚠️ 급가속, 촉매 규명.** HL **8.247%→45.397%**, OrangeX
  **8.889%→10.71%→45.042%**, Aster **9.506%→45.188%**로 3소스 전원 5배 안팎 재가속했다.
  WebSearch로 촉매 확인: **8/6 Robinhood 공식 상장**이 24시간 내 +40~60% 급등을 촉발
  ([coinsprobe.com](https://coinsprobe.com/robinhood-lists-cashcat-memecoin-jumps-sharply-on-official-announcement/)),
  **8/5 Uniswap의 pools.trade 런칭**도 +33% 기여
  ([thestreet.com](https://www.thestreet.com/crypto/investing/cash-cat-cashcat-price-today-august-7-2026))했다
  — 온체인 루틴(06:11Z)이 확인한 '확산 가속'과 선물 데이터가 정확히 정합된다.

## 신규/추가 발견

### ⚠️⚠️ ADA — 15회차 연속 마이너스 스트릭 종료, 플러스 전환

Binance/Bybit 가중 **-1.506%→+0.174%**, OrangeX **-1.108%→-0.302%**, Aster
**-1.406%→-0.252%**, HL **-0.988%→-0.186%**로 전 소스가 동반 개선되며 15회차 연속
마이너스 스트릭을 처음으로 끊었다.

### ⚠️ AIO — 급등 완전 반납

직전 회차의 급등(+5.734%)이 이번 회차 완전히 반납돼 거의 손익분기 수준(**+0.231%**)으로
되돌아왔다. Aster에서도 **+7.134%→+0.048%**로 동조 반납했다 — 이번 회차부터 AIO-USDT
(Aster)를 DEX 리스트에 정식 편입했다.

### ⚠️ MMT — 급반전, 원인 미규명

OKX 직접조회에서 **+0.647%→-14.861%**로 급락(펀딩도 -0.054%→-0.239%로 악화)했다.
원인은 이번 회차에서 규명하지 못했다.

### ⚠️⚠️ AEON — 4회차 연속 악화 스트릭 종료, 처음으로 개선

OKX **-14.27%→-11.616%**, OrangeX **-14.517%→-11.598%**, Aster **-13.98%→-11.782%**로
3소스 동조 개선되며 4회차 연속 악화 스트릭이 처음으로 끊겼다.

### ⚠️⚠️ CAP — 급등 확대, 촉매 규명

지난 회차의 예상치 못한 급등이 이번 회차 더 확대됐다: OKX **+23.817%→+34.455%**,
OrangeX **+25.625%→+35.747%**, Aster **+19.08%→+33.71%**. WebSearch 확인 결과
**8/6 한국 거래소 Upbit가 CAP의 KRW·BTC·USDT 마켓 상장을 발표**했고, 이 소식에
경쟁 거래소 Bithumb에서 CAP 가격이 1분 만에 약 +34.5% 급등한 것이 발단이었다
([biggo.com](https://finance.biggo.com/news/e5663b55-0efb-49b8-9fd7-1cb7db04d3cd)).

### ⚠️ TUT 교차검증 — Aster 상장 여부 미확인

온체인 루틴이 8/6 Aster의 TUT 5배 퍼프 상장을 촉매로 지목했고, WebSearch로도 '8/6 TUT
퍼프 상장이 52~62% 급등과 숏스퀴즈를 촉발'했음을 확인했다
([coingabbar.com](https://www.coingabbar.com/en/price-prediction/biconomy-bico-price-prediction-perp-listing-surge)).
그러나 이번 회차 CoinGecko Aster 티커 목록을 20개 매칭 심볼 기준으로 직접 조회한 결과
**TUT-USDT 심볼이 발견되지 않았다**(raw 데이터 기준). 상장폐지·거래정지·심볼 표기 차이
중 무엇인지는 규명하지 못해 '미확인'으로 정직 표기한다 — 다만 온체인 루틴이 관측한
재가속 반전(h6 +20.5%→-26.13%)과 방향상 모순되지는 않는다(퍼프 유동성 자체가 사라졌을
가능성).

## 기타 주요 변화

**BSB**는 4번째 휩쏘로 추가 완화됐다(OKX -9.812%→**-6.749%**, OrangeX -11.054%→
**-6.805%**, Aster -8.848%→**-6.949%**). **ANSEM**은 두 소스(Aster -5.178%→**+2.162%**,
OrangeX -5.469%→**+0.341%**) 모두 마이너스에서 플러스로 전환됐다. **HYPER-USD**(HL)도
-0.296%→**+0.137%**로 플러스 전환된 반면, **APEX-USD**(HL)는 +0.434%→**-1.662%**,
Bybit도 +0.184%→**-1.836%**로 함께 마이너스로 재전환됐다.

## 데이터 이슈 추적 결과

**HYNA:HYPE-USD**의 OI는 이번 회차도 정상 갱신을 이어갔다($688,008.38→**$688,966.35**)
— 정상화가 **3회차 연속** 확인됐다. GIGGLE의 필드 이상치(vol24h=51,870,186 vs
volCcy24h=518,701.86, 100배 스케일 차이를 raw JSON으로 재확인)가 **17회차 연속**,
KAITO(OKX 직접, vol24h=volCcy24h=99,467,642 raw 재확인)의 완전동일값이 **17회차 연속**,
GRAM(vol24h=volCcy24h=2,362,478 raw 재확인)의 완전동일값이 **15회차 연속** 재현됐다.
신규 관찰: **MMT**(vol24h=27,705,389, volCcy24h=277,053,890)와 **PIPPIN**(vol24h=15,468,887,
volCcy24h=154,688,870)에서 정확히 **10배** 비율이 관측됐다 — 기존 3종의 이상치(100배 또는
완전동일)와는 성격이 다르고 계약 승수 차이일 가능성이 있어 '이상치'로 단정하지 않고
관찰만 기록한다. **TOAD**는 이번 회차 재검색을 생략하고 직전 결과('미상장')를
이어받았다 — 다음 회차 재확인이 필요하다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️ 회복 재개, 5소스 전원 개선] | Binance/Bybit(가중) | $67.61M | $10.33M | +0.001% | -11.220% | 가중 -15.108%→-11.220%, 전 소스 개선 | recovery-resumes-all-sources-improve |
| **BICO** [⚠️⚠️⚠️ 5회차 악화, 최대낙폭 경신] | OKX(CoinGecko정상, okex_swap) | $397.99M | $7.92M | -0.173% | -45.808% | -36.816%→-45.808%, 숏스퀴즈 되돌림 | worsening-continues-record-low-5th-round |
| **BEAT** [⚠️⚠️ 하락 지속·심화] | OKX(CoinGecko정상, okex_swap) | $259.26M | $8.18M | +0.002% | -22.742% | -12.21%→-22.742% | worsening-continues-2nd-round |
| **KAITO** [4번째 휩쏘, 재차 마이너스] | OKX(직접API) | $66.86M | $7.67M | -0.128% | -2.889% | +0.172%→-2.889%. 8/20 언락 9.6일 앞 | reverts-to-negative-again |
| **BANK** [모멘텀 정체·일부 재반전] | Binance/Bybit(가중) | $113.92M | $18.73M | +0.004% | +0.172% | +1.148%→+0.172%. 8/17 언락 6.5일 앞 | positive-momentum-stalls |
| **MMT** [⚠️ 급반전] | OKX(직접API) | $54.44M | $3.38M | -0.239% | -14.861% | +0.647%→-14.861%, 원인 미규명 | sudden-reversal-to-negative |
| BSB [4번째 휩쏘, 완화] | OKX(CoinGecko정상, okex_swap) | $5.96M | $2.56M | +0.019% | -6.749% | -9.812%→-6.749% | fourth-whipsaw-improves |
| AAVE [플러스 유지, 냉각] | Binance/Bybit(가중) | $44.04M | $88.69M | +0.008% | +0.081% | +0.652%→+0.081% | cools-within-positive |
| ALLO [개선 지속] | Binance/Bybit(가중) | $23.03M | $18.12M | +0.005% | -0.698% | -2.213%→-0.698% | improvement-continues |
| **ADA** [⚠️⚠️ 15회차 스트릭 종료, 플러스 전환] | Binance/Bybit(가중, USDT만) | $146.47M | $170.95M | +0.003% | +0.174% | -1.506%→+0.174% | breaks-15round-negative-streak-turns-positive |
| AKE [개선 지속, 냉각] | Binance/Bybit(가중) | $50.37M | $37.74M | +0.017% | 4.675% | +5.222%→+4.675% | improvement-continues-mild-cooling |
| GIGGLE [완화, 이상치 17회차] | OKX(직접API) | $17.32M | $2.32M | +0.005% | -5.836% | -6.157%→-5.836% | improves-within-negative-field-anomaly-17th-round |
| PIPPIN [플러스 확대] | OKX(직접API) | $2.83M | $1.98M | +0.038% | 4.100% | +2.734%→+4.100% | positive-holds-increase |
| 1000RATS [플러스 유지, 냉각] | Binance/Bybit(가중) | $13.32M | $18.86M | +0.026% | 3.501% | +4.176%→+3.501% | extends-positive-mild-cooling |
| **AIO** [⚠️ 급등 완전 반납] | Binance/Bybit(가중) | $10.64M | $4.26M | +0.005% | 0.231% | +5.734%→+0.231% | surge-fully-reverses |
| GRAM [완화, 이상치 15회차] | OKX(직접API) | $3.17M | $6.46M | +0.005% | -0.593% | -1.852%→-0.593% | improves-within-negative-field-anomaly-15th-round |
| **AEON** [⚠️⚠️ 악화 종료, 개선] | OKX(CoinGecko정상, okex_swap) | $15.37M | $3.59M | +0.005% | -11.616% | -14.27%→-11.616% | worsening-streak-finally-breaks-improves |
| ATOM [마이너스권 완화] | Binance/Bybit(가중) | $8.94M | $28.45M | +0.002% | -0.330% | -0.676%→-0.330% | improves-within-negative |
| ASTER [플러스 유지, 소폭 확대] | Binance/Bybit(가중) | $23.12M | $113.33M | +0.005% | 1.877% | +1.727%→+1.877% | positive-holds-slight-increase |
| CORE [플러스 유지, 냉각] | OKX(CoinGecko정상, okex_swap) | $1.85M | $1.02M | +0.010% | 1.699% | +3.389%→+1.699%, 초저유동성 | cools-within-positive-low-liquidity |
| **CAP** [⚠️⚠️ 급등 지속, 촉매 규명] | OKX(CoinGecko정상, okex_swap) | $77.00M | $6.41M | -0.052% | 34.455% | +23.817%→+34.455%, Upbit 상장 발표 촉매 | surge-continues-catalyst-identified |
| ALGO [거의 유지, 소폭 개선] | Binance/Bybit(가중) | $16.42M | $14.67M | +0.005% | -5.269% | -5.997%→-5.269% | roughly-flat-slight-improvement |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [개선으로 반전] | Hyperliquid | $1.99M | $1.27M | +0.001% | -11.224% | -17.503%→-11.224% | recovery-resumes-worsening-reverses |
| **ACE-USDT-PERPETUAL** [개선 지속] | OrangeX | $42.61M | $13.18M | +0.011% | -10.342% | -14.026%→-10.342% | recovery-resumes-improves |
| **ACE-USDT** [개선 지속] | Aster | $0.35M | $0.03M | 0.000% | -11.028% | -14.694%→-11.028% | recovery-resumes-improves |
| BEAT-USDT-PERPETUAL [마이너스 심화] | OrangeX | $19.08M | $5.03M | +0.010% | -22.953% | -13.424%→-22.953% | worsening-continues-2nd-round |
| BEAT-USDT [마이너스 심화] | Aster | $6.29M | $1.00M | -0.014% | -23.38% | -11.263%→-23.38% | worsening-continues-2nd-round |
| **BICO-USDT-PERPETUAL** [⚠️ 5회차 악화] | OrangeX | $218.74M | $55.84M | -0.423% | -46.811% | -37.822%→-46.811% | worsening-continues-record-low-5th-round |
| **BICO-USDT** [⚠️ 5회차 악화] | Aster | $3.96M | $0.23M | -0.013% | -45.397% | -36.479%→-45.397% | worsening-continues-record-low-5th-round |
| **CASHCAT** [⚠️⚠️⚠️ 급가속, 촉매규명] | Hyperliquid | $20.02M | $25.16M | +0.023% | 45.397% | 8.247%→45.397%, Robinhood 상장 촉매 | sharp-reacceleration-catalyst-identified |
| CASHCAT-USDT-PERPETUAL [⚠️⚠️⚠️ 급가속] | OrangeX | $0.15M | $0.06M | +0.037% | 45.042% | 10.71%→45.042% | sharp-reacceleration |
| CASHCAT-USDT [⚠️⚠️⚠️ 급가속] | Aster | $2.04M | $1.73M | -0.003% | 45.188% | 9.506%→45.188% | sharp-reacceleration |
| ALLO-USDT [플러스 전환] | Aster | $0.10M | $0.03M | +0.001% | 0.324% | -2.466%→+0.324% | turns-positive |
| ALLO-USDT-PERPETUAL [개선 지속] | OrangeX | $14.95M | $5.13M | +0.010% | -0.545% | -2.452%→-0.545% | improvement-continues |
| AAVE-USDT-PERPETUAL [플러스 유지, 냉각] | OrangeX | $24.69M | $8.71M | +0.010% | 0.24% | +0.506%→+0.24% | cools-within-positive |
| AAVE-USDT [플러스 유지, 냉각] | Aster | $0.44M | $4.56M | +0.010% | 0.131% | +0.693%→+0.131% | cools-within-positive |
| AAVE-USD [플러스 유지, 냉각] | Hyperliquid | $3.41M | $61.35M | +0.001% | 0.235% | +1.115%→+0.235% | cools-within-positive |
| ADA-USDT-PERPETUAL [대폭 완화] | OrangeX | $80.34M | $28.46M | +0.010% | -0.302% | -1.108%→-0.302% | improves-turns-near-flat |
| ADA-USDT [마이너스권 완화] | Aster | $0.40M | $1.68M | +0.001% | -0.252% | -1.406%→-0.252% | improves-within-negative |
| ADA-USD [마이너스권 완화] | Hyperliquid | $3.41M | $32.92M | +0.001% | -0.186% | -0.988%→-0.186% | improves-within-negative |
| BANK-USDT-PERPETUAL [손익분기로] | OrangeX | $7.99M | $2.75M | -0.010% | -0.01% | +1.297%→-0.01% | momentum-stalls-near-flat |
| BANK-USDT [마이너스 재전환] | Aster | $0.53M | $0.29M | 0.000% | -0.231% | +2.137%→-0.231% | momentum-stalls-turns-negative |
| AKE-USDT-PERPETUAL [개선 지속, 냉각] | OrangeX | $5.71M | $1.88M | +0.010% | 5.035% | +8.121%→+5.035% | improves-mild-cooling |
| AKE-USDT [거의 유지] | Aster | $0.97M | $10.69M | +0.005% | 4.499% | +4.93%→+4.499% | roughly-flat-positive |
| **CAP-USDT** [⚠️⚠️ 급등 지속] | Aster | $0.07M | $0.18M | +0.001% | 33.71% | +19.08%→+33.71%, Upbit 상장 촉매 | surge-continues-catalyst-identified |
| **CAP-USDT-PERPETUAL** [⚠️⚠️ 급등 지속] | OrangeX | $0.58M | $0.24M | -0.076% | 35.747% | +25.625%→+35.747%, Upbit 상장 촉매 | surge-continues-catalyst-identified |
| ALGO-USDT-PERPETUAL [마이너스권 완화] | OrangeX | $8.99M | $3.23M | +0.010% | -5.19% | -6.393%→-5.19% | improves-within-negative |
| ALGO-USDT [초저유동성, 완화] | Aster | $0.04M | $0.02M | -0.001% | -5.047% | -5.293%→-5.047% | low-liquidity-improves |
| ALGO-USD [마이너스권 완화] | Hyperliquid | $0.95M | $1.91M | +0.001% | -5.172% | -5.759%→-5.172% | improves-within-negative |
| ATOM-USDT-PERPETUAL [마이너스권 완화] | OrangeX | $4.81M | $1.65M | -0.010% | -0.578% | -0.653%→-0.578% | improves-within-negative |
| ATOM-USDT [초저유동성, 완화] | Aster | $0.01M | $1.60M | +0.010% | -0.145% | -0.581%→-0.145% | low-liquidity-improves |
| ATOM-USD [마이너스권 완화] | Hyperliquid | $0.22M | $1.91M | +0.001% | -0.383% | -0.652%→-0.383% | improves-within-negative |
| ASTER-USDT-PERPETUAL [소폭 확대] | OrangeX | $9.18M | $3.04M | +0.010% | 1.848% | +1.778%→+1.848% | positive-holds-slight-increase |
| ASTER-USDT [대형 OI, 거의 유지] | Aster | $14.40M | $222.63M | +0.007% | 1.761% | OI $222.54M→$222.63M | large-oi-positive-holds |
| ASTER-USD [소폭 확대] | Hyperliquid | $1.44M | $14.79M | +0.001% | 1.853% | +1.805%→+1.853% | positive-holds-slight-increase |
| KAITO-USD [재차 마이너스, 4번째 휩쏘] | Hyperliquid | $18.62M | $11.76M | -0.091% | -2.825% | -0.653%→-2.825% | reverts-to-negative-again |
| GRAM-USD [완화, OKX와 근접] | Hyperliquid | $0.81M | $12.94M | +0.001% | -1.0% | -1.304%→-1.0% | improves-matches-okx |
| HYPE-USD [마이너스권 완화] | Hyperliquid | $91.06M | $1,179.92M | +0.001% | -1.006% | -1.692%→-1.006% | improves-within-negative |
| HYPER-USD [플러스 전환] | Hyperliquid | $0.20M | $0.34M | +0.001% | 0.137% | -0.296%→+0.137% | turns-positive |
| APEX-USD [마이너스 재전환] | Hyperliquid | $0.07M | $0.75M | +0.001% | -1.662% | +0.434%→-1.662%, Bybit도 동조 | turns-negative-again |
| FARTCOIN [플러스 확대] | Hyperliquid | $7.16M | $22.88M | +0.001% | 3.945% | +1.507%→+3.945% | extends-positive |
| ETHFI-USD [플러스 유지, 냉각] | Hyperliquid | $0.67M | $8.47M | +0.001% | 0.75% | +2.197%→+0.75% | cools-within-positive |
| ETH-USD [플러스 전환] | dYdX | $11.59M | $8.30M | 0.000% | 0.407% | -0.031%→+0.407% | turns-positive |
| BTC-USD [플러스 유지, 확대] | dYdX | $1.82M | $17.87M | 0.000% | 0.487% | +0.052%→+0.487% | positive-holds-increase |
| SOL-USD [플러스 유지, 거의 유지] | dYdX | $0.15M | $4.52M | 0.000% | 0.787% | +0.804%→+0.787% | roughly-flat-positive |
| ANSEM [플러스 전환] | Aster | $0.10M | $0.93M | +0.001% | 2.162% | -5.178%→+2.162% | turns-positive |
| ANSEM-USDT-PERPETUAL [플러스 전환] | OrangeX | $0.50M | $0.18M | +0.010% | 0.341% | -5.469%→+0.341% | turns-positive |
| **BTW** [플러스 확대] | Aster | $2.48M | $14.53M | +0.028% | 8.156% | +6.947%→+8.156% | extends-positive |
| HYNA:PUMP-USD [플러스권 재확대] | Hyperliquid | $0.05M | $0.18M | +0.003% | 14.638% | +8.25%→+14.638% | reaccelerates-within-positive |
| **HYNA:HYPE-USD** [⚠️ OI 정상갱신 3회차] | Hyperliquid | $0.15M | $0.69M | +0.010% | -0.858% | $688,008.38→$688,966.35 | oi-normal-updates-continue-3rd-round |
| AEON-USDT-PERPETUAL [⚠️⚠️ 악화 종료] | OrangeX | $0.43M | $0.14M | +0.010% | -11.598% | -14.517%→-11.598% | worsening-streak-finally-breaks-improves |
| AEON-USDT [⚠️⚠️ 악화 종료] | Aster | $0.09M | $0.21M | +0.005% | -11.782% | -13.98%→-11.782% | worsening-streak-finally-breaks-improves |
| **BSB-USDT-PERPETUAL** [4번째 휩쏘, 완화] | OrangeX | $10.32M | $3.57M | +0.010% | -6.805% | -11.054%→-6.805% | fourth-whipsaw-improves |
| **BSB-USDT** [4번째 휩쏘, 완화] | Aster | $0.04M | $0.10M | +0.001% | -6.949% | -8.848%→-6.949% | fourth-whipsaw-improves |
| 1000RATS-USDT [플러스 유지, 냉각] | Aster | $0.11M | $0.04M | +0.012% | 2.454% | +4.127%→+2.454% | extends-positive-mild-cooling |
| **AIO-USDT** [⚠️ 신규 편입, 급등 반납] | Aster | $0.55M | $0.10M | +0.067% | 0.048% | +7.134%→+0.048% | new-entry-surge-fully-reverses |
| **BLESS** [소폭 재악화] | OrangeX | $61.37M | $20.42M | +0.241% | -2.367% | -1.856%→-2.367% | worsens-slightly-within-improved-range |
| **BLESS-USDT** [개선 지속] | Aster | $0.32M | $0.24M | +0.005% | -1.554% | -5.205%→-1.554% | improvement-continues |

## 테마 태그

1. **시장 전반: `/global` 정상 응답, 11회차 연속 확보 — 총시총 $2.305T(소폭 상승)·BTC도미넌스 56.687%(소폭 상승)** (global-api-eleventh-round-normal).
2. **Fear&Greed 30(Fear) — 직전과 동일, 3회차 연속 유지** (fear-greed-holds-at-30-third-round).
3. **⚠️ ACE: 소스 간 혼조 완전 해소, 5소스 전원 개선(가중 -15.108%→-11.220%) — 회복 재개** (ace-recovery-resumes-all-improve).
4. **⚠️⚠️⚠️ BICO: 5회차 연속 악화, -45~47%대로 최대낙폭 추가 경신. 8/4 Aster 5x 퍼프發 숏스퀴즈(8/7 +75.3%)가 완전히 역전된 패턴** (bico-worsening-5th-round-squeeze-unwind).
5. **⚠️⚠️ BEAT: 완전 반전 이후 하락 이어지며 추가 심화(-12.21%→-22.742%)** (beat-worsening-continues-2nd-round).
6. **KAITO: 혼조 해소가 다시 뒤집혀 4번째 휩쏘로 재차 마이너스 전환. 8/20 대형 언락 약 9.6일 앞** (kaito-reverts-to-negative-4th-whipsaw).
7. **BANK: 3번째 휩쏘 모멘텀 크게 정체·일부 재반전(4소스 중 2곳 마이너스). 8/17 언락 약 6.5일 앞** (bank-momentum-stalls-partial-reversal).
8. **⚠️ MMT: OKX 직접조회에서 +0.647%→-14.861%로 급반전, 원인 미규명** (mmt-sudden-reversal-to-negative).
9. **⚠️⚠️ ADA: 15회차 연속 마이너스 스트릭 종료, 전 소스 동반 플러스 전환** (ada-breaks-15round-streak-turns-positive).
10. **⚠️ AIO: 급등이 완전히 반납돼 손익분기 수준으로 회귀, Aster도 동조** (aio-surge-fully-reverses).
11. **⚠️⚠️ AEON: 4회차 연속 악화 스트릭 종료, 3소스 동조 개선** (aeon-worsening-streak-breaks-improves).
12. **⚠️⚠️ CAP: 급등 확대, 촉매 규명 — 8/6 Upbit 상장 발표가 발단** (cap-surge-continues-catalyst-upbit-listing).
13. **⚠️⚠️⚠️ CASHCAT: 온체인 확산 가속과 정합되게 선물도 급가속, 촉매 규명(Robinhood 상장·Uniswap pools.trade 런칭)** (cashcat-sharp-reacceleration-catalysts-identified).
14. **⚠️ TUT 교차검증: 온체인·WebSearch가 8/6 Aster TUT 퍼프 상장發 급등을 확인했으나, 이번 회차 Aster 티커 직접조회에서 TUT-USDT 미발견 — 미확인 표기** (tut-aster-listing-unconfirmed-in-current-ticker-data).
15. **BSB: 4번째 휩쏘로 추가 완화** (bsb-fourth-whipsaw-improves).
16. **HYNA:HYPE-USD: OI 정상 갱신 3회차 연속 이어짐** (hyna-hype-oi-normal-updates-3rd-round).
17. **⚠️ GIGGLE 필드 이상치 17회차 연속, KAITO(OKX 직접) 완전동일값 17회차 연속, GRAM 15회차 연속 재현. MMT·PIPPIN에서 10배 비율 신규 관찰(이상치로 단정 안 함)** (field-anomalies-continue-plus-new-10x-observation).
18. **TOAD: 이번 회차 재검색 생략, 직전 결과('미상장') 이어받음** (toad-carried-forward-not-rechecked).
19. **OKX ACE는 instId 자체 부재 32회차 연속 재확인, 나머지 미등재 종목은 OKX 직접 API/DEX로 보강** (okx-ace-not-listed-32nd-round).
20. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
21. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
22. **이번 회차 orangex_futures·hyperliquid는 2~3회 429 후 재시도로 확보, 나머지 소스는 첫 시도 정상 — 레이트리밋 다소 완화** (rate-limiting-moderately-eased-this-round).
23. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**CoinGecko binance_futures**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS
확인, 전부 첫 시도 정상 응답. **BICO·BEAT·BSB·APEX·BTW·KAITO·CASHCAT·MMT·GIGGLE·PIPPIN·
GRAM·CORE·CAP·AEON·BLESS·ANSEM은 이번 회차도 명확히 미확인**(단순 미상장).

**CoinGecko bybit**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS·APEX 확인,
첫 시도 정상 응답. 나머지는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·CAP·BICO·BEAT 확인,
첫 시도 정상 응답. ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT은
이번 회차도 okex_swap 배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인.
`oiUsd` 필드 직접 사용 방법론을 **32회차 연속** 유지, vol24_usd=`volCcy24h`×`last` 계산
방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️ **ACE-USDT-SWAP는 OKX에 instId
자체가 존재하지 않음**을 이번 회차도 직접 확인(에러코드 51001), **32회차 연속**. **GIGGLE**은
raw JSON에서 `vol24h=51,870,186`·`volCcy24h=518,701.86`로 정확히 100배 스케일 차이가 나는
필드 이상치가 **17회차 연속**, **KAITO**는 `vol24h`=`volCcy24h`=99,467,642로 완전동일값
이상치가 **17회차 연속**, **GRAM**도 `vol24h`=`volCcy24h`=2,362,478로 완전동일값이
**15회차 연속** 재현됐다. 신규 관찰로 **MMT**(vol24h=27,705,389, volCcy24h=277,053,890)와
**PIPPIN**(vol24h=15,468,887, volCcy24h=154,688,870)에서 정확히 10배 비율을 확인했으나,
기존 3종과 성격이 달라 이상치로 단정하지 않았다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·
ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD·BTC·ETH 등 raw 정밀값 확보(2~3회 429 후 재시도). **SOL은
HL에서 이번 회차도 미확인**(기존 dYdX로 대체 집계). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·
BTW·BLESS·ANSEM은 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·
BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON·AIO 전량 확보(raw 정밀값, 첫 시도
정상 응답). MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견. **TUT는 20개
매칭 심볼 중 미발견** — 상세는 본문 참조.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값, 2~3회 429 후 재시도). BTW는 이번 회차도
OrangeX에서 미발견(기존과 동일, Aster에서만 확인). KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·
CORE는 여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.82M/OI $17.87M, ETH-USD $11.59M/OI $8.30M,
SOL-USD $0.15M/OI $4.52M) 확보, 첫 시도 정상 응답.

**CoinGecko `/global`**: 첫 시도 정상 응답으로 총시총 $2,305,263,192,865.03(약
$2.305T)·BTC도미넌스 56.687%를 확인했다. 직전 회차($2.298T·56.67%)보다 시총·도미넌스
모두 소폭 상승, **11회차 연속** 확보됐다.

**Fear&Greed**: alternative.me API로 정상 응답, **30(Fear)** 확인 — 직전과 동일, 3회차
연속 유지됐다.

**TOAD**: 이번 회차 재검색을 생략하고 직전 결과('미상장')를 이어받았다 — 다음 회차
재확인이 필요하다.

**신규 발견**: (a) ACE의 회복이 직전 회차 '소스 간 혼조'에서 5소스 전원 개선으로
완전히 해소됐다. (b) BICO가 5회차 연속 악화를 이어가며 -45~47%대까지 밀렸는데,
WebSearch로 8/4 Aster 5x 퍼프 상장發 숏스퀴즈(8/7 +75.3%)가 완전히 되돌려진 패턴임을
확인했다. (c) ADA가 15회차 연속 마이너스 스트릭을 처음으로 끊고 전 소스 동반 플러스로
전환됐다 — 이번 회차 최대 반전 사례. (d) AIO의 급등이 하루 만에 완전히 반납됐다.
(e) AEON도 4회차 연속 악화 스트릭을 처음으로 끊고 개선됐다. (f) CAP·CASHCAT 모두 이번
회차 WebSearch로 명확한 촉매(Upbit 상장, Robinhood 상장·Uniswap pools.trade)를 규명했다.
(g) TUT는 온체인·뉴스 모두 확인된 촉매인데 현재 Aster 티커 목록에서 미발견돼 교차검증
불일치를 정직하게 기록했다. (h) HYNA:HYPE-USD의 OI 정상 갱신이 3회차 연속 확인됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(32회차 연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은
본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상 스케일로
관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·
GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며,
이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·
HYNA:HYPE-USD·BLESS·AIO-USDT는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다;
(h) TUT의 Aster 상장 여부는 CoinGecko 티커 목록 조회만으로 판단했으며, Aster 자체 API를
직접 조회하지는 않아 완전한 확인은 아니다; (i) BICO의 소스 간 격차·악화 추세가 5회차
연속 이어지고 있으며, 근본 원인(퍼프 상장에 따른 숏스퀴즈 되돌림 외 추가 요인)은 완전히
규명하지 않았다; (j) KAITO 8/20 언락 규모는 이전 회차 기준 소스별로 공급 3.3%~7.63%·
$22.9M~$34.68M로 편차가 있었으며, 이번 회차는 재검증하지 않았다; (k) GIGGLE·KAITO의
필드 이상치가 17회차 연속, GRAM도 15회차 연속 재현돼 구조적 패턴으로 굳어졌으나 근본
원인(OKX API 자체 특성인지)은 규명하지 않았다; (l) MMT의 급반전 원인은 이번 회차에서
조사하지 못했다 — 다음 회차 추적이 필요하다; (m) TOAD의 선물 상장 여부는 이번 회차
재검색을 생략해 직전 결과를 이어받았다 — 다음 회차 재확인 필요; (n) BEAT의 하락이
일회성 조정인지 추세 하락으로 굳어지는지는 다음 회차 추적이 필요하다; (o) CAP·CASHCAT의
촉매(거래소 상장)는 규명됐으나, 저유동성 구간의 변동성이 여전히 커 지속 가능한 추세인지는
불확실하다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
