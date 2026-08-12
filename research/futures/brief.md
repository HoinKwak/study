# 선물시장 스카우트 브리핑 — 2026-08-12 04:30 UTC (KST 2026-08-12 13:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-12T02:29:00Z)
> 로부터 약 2.0시간 경과.**

## 이번 회차 핵심 요약 — ACE 반등 2회 연속(단 OI는 방향 엇갈림), KAITO 재하락(OI는 계속 증가), CASHCAT 다시 반전, BICO 급락 가속

이번 회차는 binance_futures·bybit·okex_swap·hyperliquid·aster·OKX직접API(5종) 전부
1차 시도부터 정상 확보됐으나, **orangex_futures·dydx_chain·CoinGecko `/global` 3종이
각 3회 재시도 전부 429**로 미확인 처리됐다(직전 회차엔 이 3종이 전부 정상이었는데
이번엔 동시에 모두 실패 — 2회차 전과 동일한 실패 조합이 재현돼 순환 레이트리밋
패턴이 계속 확인된다).

## ⚠️⚠️ 최우선 추적 — 언락 임박 3종 (BANK 8/17·ACE 8/18·KAITO 8/20)

### ACE — 8/18 약 5.8일 앞, 반등 2회 연속 지속되나 OI는 방향 갈림

Binance+Bybit 가중 -11.594%→**-10.363%**, HL -11.34%→**-10.499%**, Aster
-11.36%→**-10.304%**로 3소스 모두 추가 개선됐다(다만 개선폭은 직전 회차 급반등보다
완만해져 약 1%p 수준). 단 OI는 방향이 갈렸다 — **CEX 가중 $8.00M→$8.10M로 소폭
증가**, HL $1.10M→$1.07M로 소폭 감소, Aster는 절대액이 작아 노이즈 수준. 직전
회차의 '가격반등+OI감소=숏커버링' 서사가 이번엔 CEX 기준 OI가 오히려 늘어 완전히
재확인되지는 않았다. OrangeX는 이번 회차 429 미확인, 직전 carry -11.092%·OI
$3.95M 유지.

### BANK — 8/17 약 4.8일 앞, 재악화 소폭 지속·OrangeX 미확인으로 OI 감소 지속여부 검증 못함

가중 -8.536%→**-8.815%**, Aster -9.626%→**-9.974%**로 재악화가 소폭 더 진행됐다.
OI는 CEX 가중 $16.28M→**$16.49M로 소폭 증가**, Aster $246,267→**$242,701로 소폭
감소**로 역시 방향이 엇갈렸다. **OrangeX는 이번 회차 429 미확인**이라, 직전 회차
확인된 'OrangeX OI -5.9% 감소'가 이번에도 이어지는지는 검증하지 못했다(직전 carry
-8.962%·OI $1.51M 유지).

### KAITO — 8/20 12:00 UTC 언락(공급 약13.5%) 약 8.3일 앞, 반등 완전 되돌림·OI는 계속 증가

직전 회차의 반등이 이번 회차 완전히 되돌려지며 재하락했다 — OKX직접
-4.776%→**-5.883%**, HL -4.44%→**-5.404%**. 반면 OI는 OKX $8.13M→**$8.45M(+4.0%)**,
HL $12.78M→**$12.90M(+0.9%)**로 양쪽 모두 계속 증가해, 가격 방향과 무관하게 OI가
늘어나는 패턴이 재확인됐다(숏 누적 해석 유지). funding은 raw
-0.0022554→**-0.0026317**로 3회차 연속 이어지던 완화 추세가 이번엔 재확대로
반전됐다.

## 이번 회차 추가 최우선 관찰

### CASHCAT — ⚠️⚠️ 3소스 수렴이 다시 반전(휩쏘 지속)

직전 회차 처음 HL·Aster·OrangeX 3소스가 동시 플러스로 수렴했으나, 이번 회차
다시 반전됐다 — HL **+2.653%→-8.393%**, Aster **+2.264%→-5.534%**로 2소스 모두
마이너스 복귀. 온체인 h24 지표와 유사하게 선물 쪽도 매 회차 방향이 뒤집히는
변동성이 확인된다. OrangeX는 이번 회차 미확인, 직전 carry +1.016% 유지.

### BICO — ⚠️⚠️⚠️ 5회차 연속 재악화, 이번 회차 급격히 가속

4회차 연속 이어지던 완만한 재악화에서 이번 회차 낙폭이 급격히 확대됐다 — OKX
**-8.931%→-22.652%**, Aster **-10.991%→-24.075%**로 두 소스 모두 20%대 급락.
완만한 흐름과는 다른 큰 폭의 신규 하락 이벤트 가능성이 있다. OrangeX는 이번 회차
미확인, 직전 carry -11.429% 유지(재확인은 다음 회차 필요).

### BEAT·CAP·AEON·AAVE — 간결 현황

- **BEAT**: 낙폭 축소 흐름이 이번 회차 정체됐다 — OKX **-20.843%→-20.234%**(거의
  보합), Aster **-17.935%→-19.42%**(소폭 재악화). 지난 여러 회차 강한 회복이 주춤.
- **CAP**: 상승세는 유지, 고점 대비 다소 pullback — OKX **+26.641%→+22.805%**,
  Aster **+26.203%→+22.9%**.
- **AEON**: 랠리가 추가로 확대됐다 — OKX **+8.504%→+11.495%**, Aster
  **+7.464%→+13.074%**로 더 강하게 상승.
- **AAVE**: 3소스 모두 플러스권에서 추가 상승 — 가중 **+0.329%→+0.944%**, Aster
  **+0.101%→+0.887%**, HL **+0.421%→+0.948%**.

### AIO — ⚠️ 직전 급격한 재악화가 이번 회차 큰 폭 회복(재반전)

가중 **-7.029%→-2.785%**, Aster **-6.619%→-3.584%**로 동반 회복했다. 직전 회차의
반전을 다시 뒤집는 재반전으로, 이 종목도 변동성이 지속되고 있다.

### ⚠️⚠️ OKX 직접조회 funding 재검증 — MMT·PIPPIN 이탈확대 추세가 처음 동시 반전

GIGGLE·GRAM은 이번 회차도 raw `fundingRate`가 정확히 `0.00005`로 완전 동일
(GIGGLE 40회차·GRAM 38회차 연속). **MMT**는 raw `-0.0003836247926697`→
**`-0.0002582749883095`**로 여러 회차 이어지던 '매 회차 더 음의 방향으로 심화'
되던 추세가 이번엔 처음으로 완화(그룹값에 다소 근접)됐다. **PIPPIN**도 raw
`0.0003357811391581`→**`0.0001220155591698`**로 그룹값(0.00005) 대비 이탈폭이
약 6.7배→약 2.4배로 대폭 축소됐다 — MMT·PIPPIN 둘 다 '매 회차 이탈 확대' 추세가
이번 회차 동시에 반전돼, 5종이 완전히 고정값은 아니면서도 각자 독립적으로 등락하는
'최소 단위 실제값' 해석이 계속 지지된다. KAITO는 raw `-0.0026316771886339`로
3회차 연속 완화 추세가 이번엔 재확대로 반전됐다.

## 이번 회차 그 외 관찰

- **ALGO**: 개선 지속, 거의 flat 근접 — 가중 -0.576%→**-0.175%**, HL
  -0.263%→**-0.173%**(Aster만 -0.502%→-0.711%로 소폭 역행하나 저유동성 노이즈).
- **ADA**: 개선추세 지속 — 가중 -1.817%→**-1.457%**.
- **AKE**: 상승폭 추가 확대 — 가중 +8.141%→**+11.393%**, Aster
  +7.501%→**+11.398%**.
- **ASTER**: 거의 보합 — 가중 +0.810%→**+0.763%**.
- **ATOM**: 고점권 유지, 소폭 상승 — 가중 +2.635%→**+3.180%**.
- **1000RATS**: 개선 지속 — 가중 -11.964%→**-10.366%**, Aster
  -11.13%→**-9.425%**.
- **ALLO**: 개선 지속 — 가중 -2.071%→**-0.701%**, Aster -1.613%→**-1.277%**
  (OrangeX 이번회차 미확인).
- **BSB**: 양쪽 소폭 재악화 — OKX -5.053%→**-6.606%**, Aster
  -4.911%→**-6.583%**.
- **BLESS**(Aster): 큰 폭 개선 — -8.796%→**-2.052%**.
- **HYPE**(HL): ⚠️ 3회차 연속 마이너스 폭 확대 — -1.207%→**-1.714%**.
- **HYPER·APEX·FARTCOIN**(HL 소형): 대체로 개선/플러스 전환 — HYPER
  -3.861%→-0.604%, APEX -0.404%→+0.009%, FARTCOIN -0.24%→+2.206%.
- **ETHFI**(HL): 소폭 재악화 — -2.434%→-2.802%.
- **ANSEM**(Aster): 소폭 개선 — -7.239%→-6.733%.
- **dYdX(ETH·BTC·SOL)·OrangeX 상장 전 종목**: 이번 회차 429 미확인, 전부 직전값
  carry-forward.

## 데이터 이슈 추적 결과

이번 회차 **binance_futures·bybit·okex_swap·hyperliquid·aster·OKX직접API(5종)**
전부 1차 시도부터 정상 확보됐다. **orangex_futures·dydx_chain·CoinGecko `/global`
3종은 각 3회 재시도 전부 429**로 미확인 처리했다. 직전 회차엔 이 3종이 정상이었는데
이번엔 동시에 실패해, 실패군이 다시 뒤바뀐 것으로 확인된다(2회차 전의 실패 조합과
동일 재현).

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [반등 2회 연속, OI 엇갈림, 언락 5.8일] | Binance+Bybit(가중평균) | $18.61M | $8.10M | -0.020 | -10.363% | 3소스 추가 개선, OI는 CEX 소폭증가·HL 소폭감소로 엇갈려 숏커버링 서사 약화 | rebounds-2nd-round-oi-mixed-unlock-6d |
| **BANK** [재악화 소폭 지속, OrangeX 미확인, 언락 4.8일] | Binance+Bybit(가중평균) | $54.03M | $16.49M | -0.057 | -8.815% | 재악화 소폭 진행, OrangeX 429라 OI감소 지속여부 검증 못함 | worsens-slightly-oi-mixed-unlock-5d |
| **KAITO** [반등 완전 되돌림, OI 계속증가, 언락 8.3일] | OKX(직접API) | $70.98M | $8.45M | -0.263 | -5.883% | 재하락, OI는 OKX·HL 양쪽 모두 증가 지속 | rebound-fully-reverses-oi-still-rising-unlock-8d |
| **BICO** [⚠️⚠️⚠️ 5회차 재악화, 급격 가속] | OKX(CoinGecko정상, okex_swap) | $88.14M | $6.32M | -0.010 | -22.652% | OKX·Aster 모두 20%대 급락, 신규 하락 이벤트 가능성 | worsens-sharply-5th-round-accelerates |
| **AEON** [랠리 추가 확대] | OKX(CoinGecko정상, okex_swap) | $9.14M | $3.55M | +0.005 | +11.495% | 전 소스 강세 지속, Aster는 +13%까지 | rallies-extend-further |
| **CASHCAT** [3소스 수렴 다시 반전] | Hyperliquid | $9.16M | $19.79M | +0.001 | -8.393% | 직전 회차 플러스 수렴이 이번 회차 다시 마이너스로(휩쏘) | reverses-negative-again-whipsaw |
| **AAVE** [플러스권 추가 상승] | Binance+Bybit(가중평균) | $63.80M | $88.61M | +0.009 | +0.944% | 3소스 모두 플러스 확대 지속 | extends-positive-all-sources |
| **AIO** [재악화에서 큰 폭 회복, 재반전] | Binance+Bybit(가중평균) | $6.76M | $4.16M | +0.005 | -2.785% | 직전 급격한 재악화가 이번 크게 되돌려짐 | reverses-recovers-again |
| CAP [상승세 유지, pullback] | OKX(CoinGecko정상, okex_swap) | $177.81M | $7.74M | -0.018 | +22.805% | 강한 상승 지속하되 고점대비 소폭 하락 | rallies-continue-slight-pullback |
| BEAT [회복세 정체] | OKX(CoinGecko정상, okex_swap) | $577.18M | $9.99M | -0.006 | -20.234% | 낙폭 축소 흐름 거의 보합으로 정체 | recovery-stalls-roughly-flat |
| ALGO [개선 지속, flat 근접] | Binance+Bybit(가중평균) | $16.34M | $15.55M | -0.013 | -0.175% | 좁은 밴드 이탈 후 flat 근접까지 개선 | improves-nears-flat |
| MMT [⚠️ funding 이탈 처음 반전] | OKX(직접API) | $19.55M | $3.17M | -0.026 | -1.414% | 여러회차 이어진 이탈확대 추세가 처음 완화 | funding-divergence-reverses-narrows |
| GRAM [플러스폭 확대] | OKX(직접API) | $3.54M | $6.51M | +0.005 | +1.958% | funding 그룹값 유지(38회차) 속 가격만 확대 | extends-positive-funding-anomaly-38th |
| GIGGLE [둔화 지속] | OKX(직접API) | $107.42M | $2.07M | +0.005 | +4.338% | 플러스 유지, 상승폭 둔화. funding 이상치 40회차 | decelerates-still-positive-anomaly-40th |
| PIPPIN [⚠️ funding 이탈 처음 반전] | OKX(직접API) | $8.37M | $1.67M | +0.012 | -4.418% | 그룹값 대비 이탈폭 6.7배→2.4배로 대폭 축소 | funding-divergence-reverses-narrows |
| BSB [소폭 재악화] | OKX(okex_swap) | $2.82M | $2.26M | +0.020 | -6.606% | OKX·Aster 양쪽 재악화 동반 | worsens-slightly-both-sources |
| AKE [상승폭 확대] | Binance+Bybit(가중평균) | $51.52M | $40.16M | +0.006 | +11.393% | Aster도 동반 확대 | extends-positive-further |
| ADA [개선추세 지속] | Binance+Bybit(가중평균) | $177.70M | $156.01M | +0.007 | -1.457% | 소폭 등락 속 개선 지속 | improves-further-post-band-break |
| ASTER [거의 보합] | Binance+Bybit(가중평균) | $17.02M | $112.02M | -0.004 | +0.763% | 플러스권 유지 | roughly-flat-positive |
| ATOM [고점권 유지] | Binance+Bybit(가중평균) | $17.46M | $29.61M | +0.006 | +3.180% | 고점권에서 소폭 상승 | pulls-back-slightly-from-highs |
| ALLO [개선 지속] | Binance+Bybit(가중평균) | $13.15M | $17.24M | +0.000 | -0.701% | CEX·Aster 개선, OrangeX 미확인 | improves-further |
| 1000RATS [개선 지속] | Binance+Bybit(가중평균) | $10.63M | $15.13M | +0.025 | -10.366% | CEX·Aster 동반 개선 | improves-both-sources |
| CORE [소폭 개선] | OKX(CoinGecko정상, okex_swap) | $1.17M | $0.87M | +0.010 | -0.808% | 저유동성, 소폭 개선 | slight-improve |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함). 이번 회차 **orangex_futures·
> dydx_chain 모두 429 미확인**이라 해당 프로토콜 행은 전부 직전 회차 값을
> carry-forward했다(표에 명시).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [반등 2회 연속] | Hyperliquid | $0.79M | $1.07M | -0.005 | -10.499% | OI 소폭 감소 동반. 언락 5.8일 | rebounds-2nd-round-oi-slight-decline-unlock-6d |
| ACE-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $11.62M | $3.95M | +0.01 | -11.092% | 직전값 유지, 다음회차 재확인 필요 | unconfirmed-carry-forward |
| ACE-USDT [반등 2회 연속] | Aster | $0.17M | $0.01M | -0.010 | -10.304% | 전소스 동반 반등 지속 | rebounds-2nd-round-oi-slight-decline-unlock-6d |
| **BANK-USDT** [재악화 지속] | Aster | $0.10M | $0.24M | -0.011 | -9.974% | OI 소폭 감소 | worsens-slightly-oi-mixed-unlock-5d |
| BANK-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $4.55M | $1.51M | -0.015 | -8.962% | 직전값 유지 | unconfirmed-carry-forward |
| **KAITO-USD** [반등 완전 되돌림, OI+0.9%] | Hyperliquid | $15.66M | $12.90M | -0.282 | -5.404% | 가격 재하락, OI는 계속 증가. 언락 8.3일 | rebound-fully-reverses-oi-still-rising-unlock-8d |
| BICO-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $53.65M | $18.63M | -0.029 | -11.429% | 직전값 유지, 급락 재확인 다음회차 필요 | unconfirmed-carry-forward |
| **BICO-USDT** [급락 가속] | Aster | $0.36M | $0.11M | +0.005 | -24.075% | 5회차 재악화가 급격히 가속 | worsens-sharply-5th-round-accelerates |
| **CASHCAT** [수렴 다시 반전] | Hyperliquid | $9.16M | $19.79M | +0.001 | -8.393% | 3소스 수렴이 이번 회차 마이너스로 재반전 | reverses-negative-again-whipsaw |
| CASHCAT-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $0.17M | $0.05M | +0.01 | +1.016% | 직전값 유지 | unconfirmed-carry-forward |
| CASHCAT-USDT [마이너스 재반전] | Aster | $0.94M | $1.31M | +0.007 | -5.534% | HL과 동반 반전 | reverses-negative-again-whipsaw |
| HYPE-USD [마이너스 폭 확대] | Hyperliquid | $125.49M | $1,174.24M | +0.001 | -1.714% | 3회차 연속 마이너스 확대 | widens-negative-3rd-round |
| AEON-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $0.43M | $0.15M | +0.01 | +7.726% | 직전값 유지 | unconfirmed-carry-forward |
| AEON-USDT [랠리 확대] | Aster | $0.04M | $0.23M | +0.005 | +13.074% | 강한 랠리 추가 확대 | rallies-extend-further |
| BLESS [429 미확인, carry] | OrangeX | $45.23M | $16.51M | +0.01 | -10.926% | 직전값 유지 | unconfirmed-carry-forward |
| BLESS-USDT [큰 폭 개선] | Aster | $0.14M | $0.16M | +0.005 | -2.052% | 낙폭 크게 축소 | improves-sharply |
| GRAM-USD [플러스폭 확대] | Hyperliquid | $3.12M | $15.87M | +0.007 | +3.274% | OI도 +17.7% 증가 | extends-positive-funding-anomaly-38th |
| BTW [상승폭 확대] | Aster | $0.93M | $14.83M | +0.026 | +10.154% | 상승폭 추가 확대 | rebounds-notably |
| ANSEM [소폭 개선] | Aster | $0.36M | $1.09M | +0.001 | -6.733% | 마이너스 폭 소폭 축소 | improves-slightly |
| ANSEM-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $0.53M | $0.18M | +0.01 | -4.241% | 직전값 유지 | unconfirmed-carry-forward |
| HYNA:PUMP-USD [재조회없음] | Hyperliquid | $0.07M | $0.19M | +0.004 | -0.835% | 직전값 유지 | small-fluctuation-continues |
| HYNA:HYPE-USD [재조회없음] | Hyperliquid | $0.13M | $0.89M | +0.001 | -0.988% | 직전값 유지 | small-fluctuation-continues |
| BSB-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $5.86M | $2.00M | +0.01 | -4.912% | 직전값 유지 | unconfirmed-carry-forward |
| BSB-USDT [소폭 재악화] | Aster | $0.01M | $0.10M | +0.001 | -6.583% | OKX와 동반 재악화 | worsens-slightly-both-sources |
| 1000RATS-USDT [개선] | Aster | $0.05M | $0.01M | +0.013 | -9.425% | CEX와 동반 개선 | improves-both-sources |
| AIO-USDT [큰 폭 회복] | Aster | $0.11M | $0.10M | +0.005 | -3.584% | 재악화에서 재반전 회복 | reverses-recovers-again |
| AAVE-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $33.97M | $12.80M | +0.01 | +0.28% | 직전값 유지 | unconfirmed-carry-forward |
| AAVE-USDT [플러스 확대] | Aster | $0.27M | $4.46M | +0.01 | +0.887% | 상승 추가 확대 | extends-positive-all-sources |
| AAVE-USD [플러스 확대] | Hyperliquid | $4.99M | $60.02M | -0.001 | +0.948% | 상승 추가 확대 | extends-positive-all-sources |
| ADA-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $90.25M | $30.99M | +0.002 | -1.578% | 직전값 유지 | unconfirmed-carry-forward |
| ADA-USDT [개선 지속] | Aster | $0.56M | $1.60M | +0.006 | -1.42% | 개선 지속 | improves-further-post-band-break |
| ADA-USD [개선 지속] | Hyperliquid | $4.23M | $31.27M | -0.002 | -1.414% | 개선 지속 | improves-further-post-band-break |
| AKE-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $6.49M | $2.33M | +0.01 | +8.856% | 직전값 유지 | unconfirmed-carry-forward |
| AKE-USDT [상승폭 확대] | Aster | $0.66M | $11.33M | +0.011 | +11.398% | 상승 확대 | extends-positive-further |
| ALGO-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $8.66M | $2.80M | -0.01 | -0.858% | 직전값 유지 | unconfirmed-carry-forward |
| ALGO-USDT [소폭 역행] | Aster | $0.03M | $0.02M | -0.002 | -0.711% | 저유동성 노이즈 | improves-nears-flat |
| ALGO-USD [flat 근접] | Hyperliquid | $0.78M | $2.17M | +0.001 | -0.173% | 개선 지속 | improves-nears-flat |
| ATOM-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $9.99M | $3.64M | +0.01 | +2.782% | 직전값 유지 | unconfirmed-carry-forward |
| ATOM-USDT [고점권 유지] | Aster | $0.01M | $1.67M | +0.01 | +3.525% | 고점권 유지 | pulls-back-slightly-from-highs |
| ATOM-USD [고점권 유지] | Hyperliquid | $0.32M | $1.90M | +0.001 | +3.203% | 고점권 유지 | pulls-back-slightly-from-highs |
| ASTER-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $6.95M | $2.40M | +0.01 | +0.845% | 직전값 유지 | unconfirmed-carry-forward |
| ASTER-USDT [대형 OI, 보합] | Aster | $10.20M | $220.61M | +0.004 | +0.864% | 거의 보합 | roughly-flat-positive |
| ASTER-USD [보합] | Hyperliquid | $0.87M | $14.78M | +0.001 | +0.659% | 소폭 하락, 여전히 플러스 | roughly-flat-positive |
| ALLO-USDT [개선] | Aster | $0.06M | $0.02M | +0.000 | -1.277% | CEX와 동반 개선 | improves-further |
| ALLO-USDT-PERPETUAL [429 미확인, carry] | OrangeX | $9.29M | $3.43M | +0.01 | -1.97% | 직전값 유지 | unconfirmed-carry-forward |
| HYPER-USD [큰 폭 개선] | Hyperliquid | $0.15M | $0.32M | +0.001 | -0.604% | 마이너스 폭 크게 축소 | improves-notably |
| APEX-USD [flat에서 플러스] | Hyperliquid | $0.12M | $0.64M | +0.001 | +0.009% | 플러스 전환 | roughly-flat |
| FARTCOIN [플러스 전환] | Hyperliquid | $7.96M | $23.61M | +0.001 | +2.206% | 마이너스에서 플러스로 | flips-positive |
| ETHFI-USD [소폭 재악화] | Hyperliquid | $0.79M | $8.33M | +0.001 | -2.802% | 마이너스 폭 소폭 확대 | worsens-further-negative |
| ETH-USD [429 미확인, carry] | dYdX | $11.92M | $19.56M | 0.0 | +0.496% | 직전값 유지 | unconfirmed-carry-forward |
| BTC-USD [429 미확인, carry] | dYdX | $3.34M | $17.74M | 0.0 | -0.292% | 직전값 유지 | unconfirmed-carry-forward |
| SOL-USD [429 미확인, carry] | dYdX | $0.96M | $4.52M | 0.0 | +0.618% | 직전값 유지 | unconfirmed-carry-forward |

## 테마 태그

1. **⚠️⚠️ ACE: 8/18 언락 약 5.8일 앞두고 반등 2회 연속 지속, 다만 OI는 CEX 기준 소폭증가로 반전돼 숏커버링 서사가 완전히 재확인되진 않음** (ace-rebounds-2nd-round-oi-mixed-unlock-6d).
2. **⚠️⚠️ BANK: 8/17 언락 약 4.8일 앞두고 재악화 소폭 지속, OrangeX 429라 OI감소 지속여부 검증 못함** (bank-worsens-slightly-oi-mixed-unlock-5d).
3. **⚠️⚠️ KAITO: 8/20 언락 약 8.3일 앞두고 반등이 완전히 되돌려짐, OI는 OKX·HL 양쪽 모두 계속 증가** (kaito-rebound-fully-reverses-oi-still-rising-unlock-8d).
4. **⚠️⚠️ CASHCAT: 직전 회차 첫 3소스 플러스 수렴이 이번 회차 다시 마이너스로 반전(휩쏘)** (cashcat-reverses-negative-again-whipsaw).
5. **⚠️⚠️⚠️ BICO: 4회차 연속 재악화가 이번 회차 급격히 가속(-8.9%→-22.7%대)** (bico-worsens-sharply-5th-round-accelerates).
6. **BEAT: 낙폭 축소 흐름이 이번 회차 정체, 거의 보합** (beat-recovery-stalls-roughly-flat).
7. **CAP: 상승세 유지, 고점 대비 다소 pullback** (cap-rallies-continue-slight-pullback).
8. **AEON: 랠리 추가 확대** (aeon-rallies-extend-further).
9. **AAVE: 3소스 모두 플러스권에서 추가 상승** (aave-extends-positive-all-sources).
10. **⚠️ AIO: 직전 급격한 재악화가 이번 회차 큰 폭 회복(재반전)** (aio-reverses-recovers-again).
11. **⚠️⚠️ OKX 직접조회 funding: MMT·PIPPIN 둘 다 이탈확대 추세가 처음 동시 반전·완화, GIGGLE·GRAM은 0.00005 동일값 지속(40·38회차)** (okx-funding-mmt-pippin-reverse-narrow).
12. **ALGO: 개선 지속, 거의 flat 근접** (algo-improves-nears-flat).
13. **데이터: binance_futures·bybit·okex_swap·hyperliquid·aster·OKX직접API 5종 정상, orangex_futures·dydx_chain·`/global` 3종이 각 3회 재시도 전부 429로 동시 실패(직전과 실패군 재차 반전, 2회차 전 조합 재현)** (data-orangex-dydx-global-fail-together).
14. **총시총·BTC도미넌스는 `/global` 미확인으로 직전 회차 값 유지, 갱신 없음** (global-metrics-unconfirmed-carried-forward).
15. **Fear&Greed 이번 회차도 미재조회** (fear-greed-not-rechecked).
16. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
17. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
18. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
19. **TUT: 이번 회차도 재확인 생략** (tut-status-unconfirmed-no-further-check).

## 데이터 신뢰도

이번 회차 **binance_futures·bybit·okex_swap·hyperliquid·aster와 OKX 직접API
(KAITO·GIGGLE·MMT·PIPPIN·GRAM) 전량 1차 시도부터 정상 확보**됐다. **orangex_futures·
dydx_chain·CoinGecko `/global` 3종은 각 3회 재시도 전부 429**로 미확인 처리하고
직전 회차 값을 carry-forward했다. 직전 회차엔 이 3종이 정상이었는데 이번엔 동시에
실패해 실패군이 다시 뒤바뀐 것으로, 2회차 전(orangex_futures·dydx_chain·`/global`이
동시 429)과 동일한 조합이 재현됐다 — 특정 엔드포인트가 구조적으로 차단된 게
아니라 레이트리밋 대상이 회차마다 순환하는 패턴이 계속 확인된다.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: ticker·open-interest·funding-rate
개별 엔드포인트 전부 1차 시도부터 정상. GIGGLE·GRAM은 raw `fundingRate`가 여전히
정확히 `0.00005`로 동일(40·38회차 연속). MMT·PIPPIN은 그룹값에서의 이탈폭이
이번 회차 처음으로 동시에 완화됐다. KAITO는 별개 스케일이며 3회차 완화 후 이번
회차 재확대로 반전. ⚠️ PIPPIN의 `open24h` 값이 이번 회차 두 차례 조회에서
`0.01788`과 `0.0171`로 일시 불일치가 관측돼, 원시 JSON 필드를 재확인하는 3차
조회로 `0.01788`(고·저가 범위와 일치)이 정확함을 확인했다 — WebFetch 요약모델의
전사 오류 가능성을 시사하는 사례로, 향후 회차에서도 수치 불일치 시 재조회로
교차검증이 필요하다. 또한 OKX ticker의 `vol24h`(계약수)와 `volCcy24h`(통화표시)가
종목별로 배율이 달라(KAITO·GRAM은 동일, GIGGLE·MMT·PIPPIN은 10~100배 차이) 이번
회차는 기존 회차와의 연속성을 위해 `vol24h` 필드를 그대로 채택했다 — 계약승수
정의가 완전히 검증되지 않은 한계가 있다.

**Hyperliquid**: 정상 확보 — ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·ALGO·GRAM·HYPE·
HYPER·APEX·FARTCOIN·ETHFI 확보(raw 정밀값). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·
BTW·BLESS·ANSEM·TUT는 HL 미상장(기존과 동일).

**Aster**: 정상 확보 — BANK·AAVE·ADA·BICO·BEAT·BSB·AKE·ATOM·ALLO·1000RATS·AIO·
AEON·ASTER·CAP·ALGO·ACE·CASHCAT·BTW·ANSEM·BLESS 전량 확보(raw 정밀값). MMT·GIGGLE·
PIPPIN·GRAM·CORE·TUT는 Aster에서 여전히 미발견.

**OrangeX**: ⚠️ **이번 회차 3회 재시도 전부 429로 미확인**(직전 회차엔 1차 시도부터
정상이었던 것과 대비). ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 전부 직전 회차 값으로 carry-forward했다.

**binance_futures**: 1차 시도부터 정상 확보 — ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·
ALLO·1000RATS·ATOM·AIO 확보. BICO·AEON은 이번 회차도 Binance에서 미발견.

**bybit**: 1차 시도부터 정상 확보 — ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·ALLO·1000RATS·
ATOM·AIO 확보, Binance+Bybit 가중평균으로 반영.

**dYdX(`dydx_chain`)**: ⚠️ **이번 회차 3회 재시도 전부 429로 미확인**(직전 회차엔
1차 시도부터 정상이었던 것과 대비) — BTC-USD·ETH-USD·SOL-USD 전부 직전값 유지.

**CoinGecko `/global`**: ⚠️ 3회 재시도 전부 429로 확보 실패 — 총시총·BTC도미넌스
모두 직전 회차 값을 유지했다.

**Fear&Greed**: 이번 회차도 재조회하지 않음(최우선 추적과제에 시간 집중).

**신규 발견**: (a) ACE는 반등 2회 연속으로 이어졌지만 OI 방향이 CEX 기준 증가로
바뀌어, 직전 회차 관측된 순수 숏커버링 서사가 이번 회차엔 완전히 재확인되지
않았다 — 단일 회차의 OI 감소만으로 방향성을 단정하기 어렵다는 사례. (b) KAITO는
직전 회차 반등이 이번 회차 완전히 되돌려지며, OI는 여전히 계속 증가해 '가격 등락과
무관한 OI 증가' 패턴이 3회차째 재확인됐다. (c) CASHCAT은 직전 회차 처음 3소스
수렴했으나 이번 회차 다시 반전돼, 온체인 지표와 유사하게 선물 쪽도 매 회차 방향이
뒤집히는 고변동성 종목임이 재확인됐다. (d) BICO는 4회차 연속 완만한 재악화에서
이번 회차 갑자기 20%대 급락으로 가속됐다 — 신규 하락 이벤트 가능성이 있어 다음
회차에서 지속 여부 확인이 필요하다. (e) MMT·PIPPIN funding 이탈폭이 여러 회차
이어지던 확대 추세에서 이번 회차 처음 동시에 반전·완화됐다 — '매 회차 심화'가
영구적 추세가 아니라 등락하는 것임을 보여준다. (f) orangex_futures·dydx_chain·
`/global`이 이번 회차 동시에 실패해, 2회차 전과 동일한 실패 조합이 재현됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 `oiUsd` 필드를
직접 채택, funding은 raw fundingRate×100 방식으로 계산했다; (d) ADA·AAVE·ATOM·ASTER·
AKE·BANK·ALLO·ALGO·ACE·1000RATS·AIO 등 복수 거래소 종목의 `chg24`·`funding`은 이번
회차 Binance+Bybit 가중평균(거래량 가중)으로 산출했다; (e) Hyperliquid 원시 funding
필드가 이번 회차도 정상 스케일로 관측돼 보정 없이 raw 값을 그대로 사용했다; (f)
BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE·BSB·BLESS는 Binance/Bybit
상장이 불확실하거나 없어 OKX·DEX로만 집계되는 구조다; (g) BTW·CASHCAT·ANSEM·
HYNA:PUMP-USD·HYNA:HYPE-USD는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다;
(h) TUT는 이번 회차도 재확인을 생략했다; (i) BANK·ACE의 언락 정보는 이번 회차
재검증하지 않고 기존 값을 유지했다(KAITO만 과거 회차 WebSearch로 정확한 시각·비율을
확인함); (j) OKX 직접조회 GIGGLE·GRAM의 funding이 왜 매 회차 동일값(0.00005)으로
관측되는지, MMT·PIPPIN 이탈폭이 왜 매 회차 등락하는지는 규명하지 못했다; (k)
dYdX·OrangeX는 이번 회차 3회 재시도 전부 429로 확보하지 못해 전부 carry-forward했다;
(l) HL에서 canonical SOL-USD는 이번 회차 재확인하지 않았다; (m) KAITO-USDT(Aster)는
이번 회차도 조회하지 않았다; (n) HYNA:PUMP-USD·HYNA:HYPE-USD는 HL 응답이 모호하게
반환된 이력이 있어 이번 회차도 재조회를 생략하고 직전값을 유지했다; (o) OKX ticker의
`vol24h`(계약수 단위)와 `volCcy24h`(통화 단위)가 종목별로 배율이 달라(GIGGLE·MMT·
PIPPIN은 10~100배 차이) 이번 회차는 기존 회차와의 연속성을 위해 `vol24h`를 채택했으나
계약승수 정의는 완전히 검증하지 못했다; (p) `/global`이 이번에도 3회 재시도에 복구되지
않은 원인은 규명하지 못했으며, 실패 대상이 회차마다 뒤바뀌는 양상이 우연인지 서버 측
정책 변화인지도 다음 회차 이후 계속 추적이 필요하다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
