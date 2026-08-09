# 선물시장 스카우트 브리핑 — 2026-08-09 04:29 UTC (KST 2026-08-09 13:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-09T02:31:00Z)
> 로부터 약 2시간 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`은 이번 회차도 429로 확보 실패 — **7회 연속 실패**로 계속 길어지고 있다.
대신 WebSearch로 확보한 참고 수치는 총시총 약 **$2.21T**·BTC도미넌스 약 **58.88%**로, 직전
6회차 연속 반복됐던 **$2.29T·56.8%**와는 다른 값이 나왔다 — 이번엔 단순 캐시가 아니라 실제
시장 변동을 반영했을 가능성이 있다(시총 약 -3.5%·BTC도미넌스 +2.1%p, 알트 대비 BTC 상대강세로
위험회피 성향을 시사). 다만 여전히 직접 API가 아닌 WebSearch 스니펫이라 신뢰도는 낮게 잡고
참고용으로만 쓴다.

### Fear&Greed 31(Fear) — 3회차 연속 동일값

alternative.me API 정상 응답, **31(Fear)** — 직전 회차부터 시작된 31 반복이 이번이 세 번째다.

### 데이터 확보 상황

binance_futures·bybit·okex_swap·hyperliquid·aster·orangex_futures는 1차 시도로 정상 확보됐고,
**dydx_chain은 1차 429 이후 재시도로 확보**됐다. `/global`만 7회 연속 429로 확보 실패. OKX 직접
API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)는 market/ticker+open-interest+funding-rate 개별조회로
**20회차 연속** 방법론(`oiUsd` 필드 직접 사용, `vol24_usd=volCcy24h×last`)을 유지해 확보했다.

지금은 **일요일 오후**(UTC 04:29, KST 13:29) 시간대다.

## 직전 회차 강조 종목 추적 결과 (요청 항목 전체)

- **① ACE(Fusionist) — ⚠️⚠️⚠️ 4거래소 전부 동시에 이번 회차 가장 큰 폭 냉각, 언락 반나절~하루
  앞.** 언락(8/10, 공급 1.2%·약 $199K로 절대금액은 작음)이 임박한 시점에서 Binance/Bybit(가중)
  +31.57%→**+19.84%**, OrangeX +30.13%→**+19.78%**, Aster +34.12%→**+20.97%**,
  HL +31.20%→**+19.49%**로 4개 거래소가 거의 동일한 폭(10%p 이상)으로 동시에 냉각했다 —
  지금까지의 거래소별 엇갈림·완만한 냉각과 질적으로 다른, '언락 직전 광범위한 차익실현/
  디레버리징'에 가까운 패턴으로 보인다(확정 아님). OI는 Binance/Bybit -13.6%, OrangeX -7.9%,
  HL -16.2%로 대부분 감소, Aster만 거의 유지.
- **② CASHCAT** — 재가속 종료 후 냉각이 2회차 연속 이어졌다: HL +28.39%→**+18.38%**, OrangeX
  +27.29%→**+19.34%**, Aster +29.41%→**+20.48%**로 3거래소 전부 추가 냉각. 다만 OI는 갈림 —
  HL -3.0%·Aster -5.1%로 계속 감소하는 가운데 **OrangeX만 OI가 4회차 연속 감소를 멈추고
  $55,682→$61,005(+9.5%)로 반등**했고 펀딩도 0.01%→0.124%로 급등 — 가격은 3거래소 동조
  냉각이지만 포지셔닝(OI)은 거래소 간 갈리는 모습이다.
- **③ BEAT** — 2회차 연속 큰 폭 재가속(36%대→48%대) 뒤 이번 회차 3거래소 전부 상당폭
  반락했다: OKX +48.16%→**+31.55%**, OrangeX +48.23%→**+31.07%**, Aster
  +48.75%→**+30.78%**로 거의 동일한 폭(-17~18%p)으로 동시 냉각 — 재가속 흐름이 이번 회차
  꺾였다. Binance 소규모 BEATUSDT 리스팅은 이번 회차 조회 결과 표에 나타나지 않아 미확인
  (델리스팅 여부 불확실, 이전에도 사라졌다 재등장한 전례가 있어 재확인 필요). Bybit는 11회차
  연속 미확인.
- **④ KAITO** — 직전 회차 '개선 추세 첫 반전(악화)' 이후 이번 회차 다시 개선 방향으로
  재반전됐다. OKX -13.83%→**-11.53%**(개선), HL -13.50%→**-11.86%**(개선)로 두 거래소 모두
  낙폭이 줄었다. 펀딩도 OKX -0.661%→**-0.459%**(개선), HL도 보정치 기준
  -0.284%→약**-0.20%**(개선)로 둘 다 완화됐다. OI는 OKX $7.69M→**$8.22M(+6.9%, 증가
  재개)**로 반등한 반면 HL은 $17.96M→**$17.48M(-2.7%)**로 계속 감소 — 거래소 간 엇갈림
  지속. 8/20 대형 언락(32.6M 토큰·약 $27~35M, 공급 3.3%) 약 11일 앞.
- **⑤ BSB** — 급락 이후 3거래소 전부 낙폭이 뚜렷이 줄며 부분 반등/안정화 조짐을 보였다: OKX
  -13.95%→**-9.44%**, OrangeX -16.78%→**-9.02%**, Aster -14.99%→**-8.51%**로 낙폭이 거의
  절반으로 축소됐다. OI는 OKX 거의 유지, OrangeX는 오히려 추가 감소($10.37M→**$8.36M,
  -19.4%**), Aster는 거의 유지 — 급락 후 숏 일부 이익실현 또는 저가매수 유입 가능성을
  시사하나 확정할 근거는 부족하다.
- **⑥ BTW — ⚠️⚠️⚠️ 4회차 연속 심화 끝에 이번 회차 극적으로 반전됐다.** Aster
  -15.24%→**+8.90%**로 마이너스에서 플러스로 완전히 뒤집혔고, OI도 $13.84M→**$14.68M
  (+6.1%)**로 직전 회차의 첫 감소 전환을 뒤집고 다시 증가했다 — 숏 청산 또는 신규 롱 유입
  가능성을 시사하나 단정할 근거는 없다.

## 이번 회차 그 외 주요 변화

⚠️⚠️⚠️ **BLESS**가 이번 회차 신규 주목 대상으로 부상했다 — DEX(OrangeX·Aster) 전용 상장
종목으로 OrangeX **-26.93%**(vol $154.96M·OI $45.79M, 펀딩 0.01%→**0.257%**로 크게 상승),
Aster **-26.44%**(vol $0.54M·OI $0.16M)로 동시 급락했다. BLESS는 DePIN/AI 계열 토큰으로
2026년 4월에도 팀 물량 대량 이동(약 4억개)으로 -55%~-70% 급락한 전례가 있어(WebSearch
확인), 이번 급락도 유사한 유동성 취약·매도 압력 패턴일 가능성이 있다(원인은 별도 확인 안 함).

⚠️ **AKE**는 3회차 개선 끝 플러스 전환(직전 회차) 후 이번 회차 Binance/Bybit(가중)·OrangeX·
Aster **3거래소 전부 동시에** 다시 마이너스로 재반전됐다(+0.27%→**-2.37%**,
+0.59%→**-2.48%**, +0.38%→**-2.52%**) — 플러스 전환이 일시적이었음을 시사. **GRAM**은 장기간
근소한 플러스권을 유지하다 이번 회차 처음 마이너스로 전환됐다(+0.148%→**-0.517%**,
CEX·DEX 동조). **MMT**는 큰 폭 재가속했다(+1.07%→**+9.31%**, OI +23.5%). **BICO**는 재가속
3회차 만에 멈추고 냉각 전환(OKX +28.02%→**+18.58%**, OrangeX +25.89%→**+17.04%**·OI 첫 감소,
Aster +25.71%→**+18.81%**). **AEON**은 3회차 재가속 끝에 3거래소 동시 첫 냉각
(+18.88%/+19.43%/+18.88%→+15.81%/+15.73%/+15.05%). **ANSEM**은 거의 평탄 회복(+0.29%)
이후 다시 마이너스로 반전(**-1.35%**). **BANK**는 3회차 심화 후 개선(-3.98%→**-2.97%**)됐으나
펀딩은 더 악화(-0.031%→**-0.068%**). GIGGLE·KAITO의 필드 이상치(순서 역전·완전동일)는 각각
**5회차 연속** 재현, GRAM의 완전동일값도 **3회차 연속** 재현됐다. **HYNA:HYPE-USD**는 OI
$729,279.31·거래량 $31,893.06이 이번 회차도 소수점까지 완전히 동일하게 유지돼 **2회 연속
무변동** — CoinGecko 해당 티커가 갱신되지 않고 있을 가능성이 커졌다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️⚠️ 4거래소 동시 큰 폭 냉각, 언락 임박] | Binance/Bybit(가중) | $280.07M | $14.91M | -0.018% | +19.84% | +31.57%→+19.84%, 4거래소 전부 동시 10%p+ 냉각 — 언락 직전 광범위 디레버리징 정황 | broad-simultaneous-cooling-all-venues-into-imminent-unlock |
| **BEAT** [2회차 재가속 후 반락] | OKX(CoinGecko 정상) | $352.36M | $9.26M | -0.009% | +31.545% | +48.156%→+31.545%, 3거래소 동시 반락. Binance 소규모 리스팅 이번 회차 미확인 | sharp-pullback-after-two-round-reacceleration |
| **BICO** [재가속 3회차 만에 냉각 전환] | OKX(CoinGecko 정상) | $444.10M | $19.88M | -0.374% | +18.58% | OI -4.8%, OrangeX OI 첫 감소 | reacceleration-ends-cooling-begins-oi-turns-down |
| **BSB** [급락 후 낙폭 절반 축소] | OKX(CoinGecko 정상) | $15.13M | $2.85M | +0.005% | -9.444% | -13.952%→-9.444%, 3거래소 전부 낙폭 큰 폭 축소 — 부분 안정화 조짐 | sharp-selloff-partially-stabilizes-losses-halve |
| AAVE [반등 후 재냉각] | Binance/Bybit(가중) | $40.97M | $88.88M | +0.008% | +0.795% | +1.89%→+0.80% | cools-after-mild-rebound |
| ALLO [3회차 마이너스, 소폭 개선] | Binance/Bybit(가중) | $35.95M | $18.88M | +0.005% | -4.83% | -5.59%→-4.83% | stays-negative-third-round-mild-improvement |
| ADA [4회차 마이너스, 소폭 심화] | Binance/Bybit(가중, USDT만) | $103.93M | $172.93M | +0.01% | -1.124% | -0.3%→-1.124% | stays-negative-fourth-round-mild-deepening |
| BANK [개선, 펀딩은 악화] | Binance/Bybit(가중) | $56.93M | $20.27M | -0.068% | -2.965% | -3.98%→-2.965%, 펀딩 -0.031%→-0.068%. 8/17 언락 약 8일 앞 | improves-after-third-round-deepening-funding-worsens-further |
| **AKE** [⚠️ 플러스 전환 일시적, 마이너스 재반전] | Binance/Bybit(가중) | $25.11M | $38.06M | +0.016% | -2.375% | +0.27%→-2.375%, 3거래소 전부 동시 재반전. 8/21 언락 약 12일 앞 | positive-turn-reverses-all-venues-simultaneously |
| KAITO [⚠️ 다시 개선 재반전] | OKX(직접API) | $153.25M(계산값) | $8.22M | -0.459% | -11.531% | -13.827%→-11.531%로 개선, OI +6.9% 재증가. 8/20 대형 언락 약 11일 앞 | improves-again-after-prior-reversal-oi-resumes-growth |
| **MMT** [큰 폭 재가속] | OKX(직접API) | $198.05M(계산값) | $4.72M | -0.023% | +9.307% | +1.066%→+9.307%, OI +23.5% | sharply-reaccelerates-oi-builds-strongly |
| GIGGLE [냉각] | OKX(직접API) | $26.25M(계산값) | $2.90M | +0.005% | +5.748% | +10.367%→+5.748%. ⚠️ 필드 순서 역전 5회차 연속 재현 | cools-field-order-anomaly-reproduced-fifth-round |
| PIPPIN [대체로 유지] | OKX(직접API) | $1.86M(계산값) | $1.90M | +0.036% | +2.209% | +2.933%→+2.209% | roughly-holds-mild-cooling |
| 1000RATS [개선 3회차 연속] | Binance/Bybit(가중) | $9.97M | $18.58M | +0.013% | -2.117% | -3.73%→-2.117% | improves-third-consecutive-round |
| AIO [3회차 마이너스, 거의 유지] | Binance/Bybit(가중) | $12.19M | $4.54M | +0.005% | -5.038% | -5.35%→-5.038% | stays-negative-third-round-roughly-flat |
| **GRAM** [⚠️ 처음 마이너스 전환] | OKX(직접API) | $2.49M(계산값) | $6.41M | +0.005% | -0.517% | +0.148%→-0.517%. ⚠️ vol 필드 동일값 이상치 3회차 연속 재현 | turns-negative-first-time-vol-field-anomaly-third-round |
| **AEON** [3회차 재가속 끝 첫 냉각] | OKX(CoinGecko 정상) | $29.22M | $4.33M | +0.005% | +15.811% | +18.88%→+15.811%, OrangeX·Aster 동조 | first-simultaneous-cooling-after-third-round-reacceleration |
| ATOM [소폭 반등] | Binance/Bybit(가중) | $11.97M | $28.64M | +0.006% | +1.0% | +0.84%→+1.0% | mild-uptick-after-cooling |
| ASTER [다시 플러스 전환] | Binance/Bybit(가중) | $16.04M | $113.50M | +0.005% | +0.161% | -0.10%→+0.161% | turns-mildly-positive-again |
| CORE [초저유동성, 재가속] | OKX(CoinGecko 정상) | $1.46M | $0.98M | +0.002% | +4.737% | +2.382%→+4.737% | low-liquidity-reaccelerates |
| CAP [3회차 연속 OKX 확인] | OKX(CoinGecko 정상) | $24.63M | $2.36M | +0.005% | +1.212% | +1.786%→+1.212% | confirmed-third-round-roughly-holds |
| ALGO [2회차 연속 정식 편입] | Binance/Bybit(가중) | $6.55M | $14.73M | +0.002% | -0.918% | -0.989%→-0.918% | second-round-tracked-mild-improvement |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [⚠️⚠️⚠️ 큰 폭 냉각] | Hyperliquid | $5.45M | $1.75M | -0.037% | +19.49% | +31.199%→+19.49%, OI -16.2% | broad-simultaneous-cooling-into-imminent-unlock |
| **ACE-USDT-PERPETUAL** [추가 냉각 지속] | OrangeX | $158.41M | $53.83M | -0.032% | +19.78% | OI -7.9%(58.24M→53.83M) | continues-unwinding-after-contrarian-position-closed |
| ACE-USDT [큰 폭 냉각] | Aster | $0.72M | $0.07M | -0.027% | +20.974% | +34.12%→+20.974% | sharp-cooling |
| **BEAT-USDT-PERPETUAL** [반락] | OrangeX | $17.99M | $6.64M | +0.025% | +31.071% | +48.226%→+31.071%, OI -2.6% | pullback-after-two-round-reacceleration |
| **BEAT** [반락] | Aster | $5.79M | $4.90M | -0.003% | +30.776% | +48.749%→+30.776%, OI -21.1% | pullback-after-two-round-reacceleration |
| **BICO-USDT-PERPETUAL** [재가속 종료, OI 첫 감소] | OrangeX | $288.16M | $122.29M | -0.567% | +17.04% | OI $128.88M→$122.29M(-4.8%) | reacceleration-ends-oi-first-decline |
| BICO-USDT [냉각 전환] | Aster | $2.24M | $0.53M | +0.001% | +18.805% | +25.709%→+18.805% | cools |
| **CASHCAT** [냉각 2회차 연속] | Hyperliquid | $11.93M | $19.17M | +0.008% | +18.38% | +28.39%→+18.38%, OI -3.0% | cools-second-consecutive-round |
| **CASHCAT-USDT-PERPETUAL** [가격냉각, OI·펀딩 반등] | OrangeX | $0.15M | $0.06M | +0.124% | +19.341% | OI $55,682→$61,005(+9.5%, 4회차 감소 후 첫 반등), 펀딩 급등 | price-cools-but-oi-reverses-up-funding-spikes |
| CASHCAT-USDT [냉각, OI 계속 감소] | Aster | $1.49M | $1.41M | +0.001% | +20.483% | OI -5.1% | cools-oi-continues-declining |
| ALLO-USDT [소폭 개선] | Aster | $0.18M | $0.04M | +0.0% | -5.305% | -6.049%→-5.305% | mild-improvement |
| ALLO-USDT-PERPETUAL [소폭 개선, OI 5회차 감소] | OrangeX | $24.86M | $8.60M | +0.01% | -4.852% | OI $9.42M→$8.60M(-8.7%) | mild-improvement-oi-declines-fifth-round |
| AAVE-USDT-PERPETUAL [냉각] | OrangeX | $25.27M | $8.30M | +0.01% | +0.979% | +1.904%→+0.979% | cools |
| AAVE-USDT [소폭 냉각] | Aster | $0.17M | $4.53M | +0.01% | +0.9% | +1.803%→+0.9% | mild-cooling |
| AAVE-USD [소폭 냉각] | Hyperliquid | $2.76M | $60.26M | +0.0% | +0.82% | +1.648%→+0.82% | mild-cooling |
| ADA-USDT-PERPETUAL [소폭 악화] | OrangeX | $54.82M | $19.52M | +0.01% | -1.047% | -0.5%→-1.047% | mildly-worsens |
| ADA-USDT [대체로 유지] | Aster | $0.11M | $1.54M | +0.01% | -0.997% | -0.846%→-0.997% | roughly-holds |
| ADA-USD [소폭 악화] | Hyperliquid | $1.66M | $33.24M | +0.0% | -1.21% | -0.682%→-1.21% | mildly-worsens |
| BANK-USDT-PERPETUAL [개선] | OrangeX | $6.06M | $2.04M | +0.017% | -2.861% | -3.563%→-2.861% | improves |
| BANK-USDT [소폭 개선] | Aster | $0.37M | $0.37M | -0.001% | -2.666% | -3.575%→-2.666% | mild-improvement |
| **AKE-USDT-PERPETUAL** [⚠️ 마이너스 재반전] | OrangeX | $6.41M | $2.33M | +0.01% | -2.477% | +0.594%→-2.477% | positive-turn-reverses |
| **AKE-USDT** [⚠️ 마이너스 재반전] | Aster | $0.30M | $10.70M | +0.013% | -2.521% | +0.381%→-2.521% | positive-turn-reverses |
| CAP-USDT [⚠️ 마이너스 전환] | Aster | $0.06M | $0.10M | +0.001% | -1.095% | +2.631%→-1.095% | turns-negative |
| CAP [냉각] | OrangeX | $0.52M | $0.20M | +0.01% | +0.709% | +1.321%→+0.709% | cools |
| ALGO-USDT-PERPETUAL [대체로 유지] | OrangeX | $4.00M | $1.36M | -0.01% | -1.029% | -1.019%→-1.029% | roughly-holds |
| ALGO-USDT [소폭 개선, 초저유동성] | Aster | $0.0003M | $0.03M | +0.001% | -0.867% | -1.97%→-0.867% | mild-improvement-low-liquidity |
| ALGO-USD [소폭 개선] | Hyperliquid | $0.37M | $2.01M | +0.001% | -0.8% | -1.129%→-0.8% | mild-improvement |
| ATOM-USDT-PERPETUAL [대체로 유지] | OrangeX | $5.99M | $2.07M | +0.01% | +0.877% | +0.878%→+0.877% | roughly-holds |
| ATOM-USDT [소폭 냉각, 플러스권 유지] | Aster | $0.02M | $1.60M | +0.01% | +0.657% | +1.175%→+0.657% | holds-positive-mild-cooling |
| ATOM-USD [소폭 확대, 플러스권 유지] | Hyperliquid | $0.29M | $1.93M | +0.001% | +1.21% | +1.009%→+1.21% | holds-positive-extends-slightly |
| ASTER-USDT-PERPETUAL [플러스 전환] | OrangeX | $6.34M | $2.21M | +0.01% | +0.148% | -0.017%→+0.148% | turns-mildly-positive |
| ASTER-USDT [대형 OI 유지, 플러스 재전환] | Aster | $8.66M | $219.30M | +0.017% | +0.199% | -0.066%→+0.199% | large-oi-roughly-holds-turns-positive-again |
| ASTER-USD [플러스 재전환] | Hyperliquid | $0.90M | $14.25M | +0.001% | +0.2% | -0.081%→+0.2% | turns-positive-again |
| **KAITO-USD** [⚠️ 다시 개선 재반전] | Hyperliquid | $28.23M | $17.48M | -0.2% | -11.86% | -13.496%→-11.86%로 개선, OI -2.7% 계속 감소. 8/20 대형 언락 약 11일 앞 | improves-again-oi-continues-declining |
| **GRAM-USD** [⚠️ 처음 마이너스 전환] | Hyperliquid | $0.38M | $12.89M | +0.001% | -0.58% | +0.052%→-0.58%, CEX와 방향 일치 | turns-negative-first-time-aligns-with-cex |
| HYPE-USD [플러스권 유지, 소폭 냉각] | Hyperliquid | $84.03M | $1,200.94M | +0.0% | +1.23% | +2.07%→+1.23% | holds-positive-mild-cooling |
| HYPER-USD [재가속] | Hyperliquid | $0.10M | $0.33M | +0.001% | +3.3% | +2.569%→+3.3% | reaccelerates-holds-positive |
| APEX-USD [마이너스 심화] | Hyperliquid | $0.10M | $0.77M | +0.001% | -0.63% | -0.363%→-0.63% | deepens-negative |
| FARTCOIN [냉각, 플러스권 유지] | Hyperliquid | $2.48M | $22.34M | +0.003% | +1.97% | +3.272%→+1.97% | holds-positive-cools |
| ETHFI-USD [플러스권 확대] | Hyperliquid | $0.39M | $8.50M | +0.001% | +1.64% | +0.487%→+1.64% | extends-positive |
| ETH-USD [⚠️ 소폭 마이너스 전환] | dYdX | $2.72M | $8.60M | 0.0% | -0.084% | +0.042%→-0.084% | turns-mildly-negative |
| BTC-USD [마이너스 심화] | dYdX | $0.92M | $18.08M | 0.0% | -0.311% | -0.145%→-0.311% | deepens-negative |
| SOL-USD [플러스권 유지] | dYdX | $0.39M | $4.51M | 0.0% | +1.767% | +2.678%→+1.767% | holds-positive-mild-cooling |
| ANSEM [⚠️ 마이너스 재반전] | Aster | $0.25M | $1.08M | +0.001% | -1.352% | +0.292%→-1.352% | flat-recovery-reverses-negative |
| **BTW** [⚠️⚠️⚠️ 극적 반전, 플러스 전환] | Aster | $3.16M | $14.68M | +0.031% | +8.897% | -15.24%→+8.897%로 완전 반전, OI +6.1% 재증가 | dramatic-reversal-to-positive-fourth-round-streak-ends |
| HYNA:PUMP-USD [별개 페어 지속, 확대] | Hyperliquid | $0.04M | $0.16M | +0.002% | +9.198% | +7.706%→+9.198% | separate-pair-confirmed-extends |
| **HYNA:HYPE-USD** [⚠️ 2회 연속 완전 무변동] | Hyperliquid | $0.03M | $0.73M | -0.006% | +1.98% | OI·거래량 소수점까지 완전 동일 유지 | completely-unchanged-second-consecutive-round-possible-stale-data |
| **AEON-USDT-PERPETUAL** [첫 냉각] | OrangeX | $0.49M | $0.17M | +0.01% | +15.728% | +19.425%→+15.728% | first-cooling-after-third-round-reacceleration |
| AEON-USDT [첫 냉각] | Aster | $0.08M | $0.26M | +0.008% | +15.052% | +18.882%→+15.052% | first-cooling-after-third-round-reacceleration |
| **BSB-USDT-PERPETUAL** [낙폭 절반 축소] | OrangeX | $24.07M | $8.36M | +0.01% | -9.016% | -16.784%→-9.016%, OI -19.4% 추가 감소 | sharp-selloff-losses-halve |
| **BSB-USDT** [낙폭 절반 축소] | Aster | $0.17M | $0.11M | +0.001% | -8.506% | -14.985%→-8.506% | sharp-selloff-losses-halve |
| 1000RATS-USDT [큰 폭 개선] | Aster | $0.04M | $0.05M | +0.011% | -1.698% | -3.858%→-1.698% | improves-significantly |
| **BLESS** [⚠️⚠️⚠️ 신규 — 대형 급락] | OrangeX | $154.96M | $45.79M | +0.257% | -26.925% | DePIN/AI 토큰, 4월에도 팀 물량 덤프로 -55~70% 급락 전례. 펀딩 0.01%→0.257% 급등 | new-major-selloff-history-of-large-dumps |
| **BLESS-USDT** [⚠️⚠️⚠️ 신규 — 대형 급락] | Aster | $0.54M | $0.16M | +0.005% | -26.441% | OrangeX와 동조 급락 | new-major-selloff-aligns-with-orangex |

## 테마 태그

1. **시장 전반: `/global` 7회 연속 429로 확보 실패, WebSearch 참고 수치는 총시총 $2.21T·BTC도미넌스 58.88%로 직전 6회차 연속 반복됐던 값($2.29T·56.8%)과 달라져 이번엔 캐시가 아닐 가능성 — 시총 축소·BTC상대강세는 위험회피 시사** (global-api-fails-7x-websearch-value-changed-not-cached).
2. **Fear&Greed 31(Fear) 3회차 연속 동일값 유지** (fear-greed-holds-31-third-consecutive-round).
3. **⚠️⚠️⚠️ ACE(Fusionist): 언락(8/10, 공급 1.2%) 반나절~하루 앞두고 4개 거래소 전부 동시에 이번 회차 최대폭 냉각 — 거래소별 엇갈림에서 광범위 동시 디레버리징으로 전환(확정 아님)** (ace-broad-simultaneous-cooling-into-imminent-unlock).
4. **⚠️⚠️⚠️ BTW: 4회차 연속 심화 끝에 극적으로 마이너스→플러스 완전 반전, OI도 재증가 전환 — 숏 청산 가능성(확정 아님)** (btw-dramatic-reversal-to-positive).
5. **⚠️⚠️⚠️ BLESS: 신규 주목 — OrangeX·Aster 동시 대형 급락(-26%대), DePIN/AI 토큰으로 4월에도 팀 물량 덤프로 대형 급락 전례** (bless-new-major-selloff-history-of-dumps).
6. **BSB: 급락 이후 3거래소 전부 낙폭이 절반 수준으로 축소되며 부분 안정화 조짐** (bsb-losses-halve-partial-stabilization).
7. **⚠️ AKE: 3회차 개선 끝 플러스 전환이 일시적이었음 — 3거래소 전부 동시에 마이너스로 재반전** (ake-positive-turn-reverses-all-venues).
8. **KAITO: 직전 회차 첫 악화 반전 이후 이번 회차 다시 개선(OKX·HL 동조), OKX OI도 재증가 전환. 8/20 대형 언락(32.6M 토큰·약 $27~35M, 공급 3.3%) 약 11일 앞** (kaito-improves-again-oi-resumes-growth).
9. **GRAM: 장기 근소 플러스권 유지 후 이번 회차 처음 마이너스로 전환, CEX·DEX 방향 일치** (gram-turns-negative-first-time).
10. **MMT: 큰 폭 재가속(+1.07%→+9.31%), OI +23.5%** (mmt-sharply-reaccelerates).
11. **BICO: 재가속 3회차 만에 3거래소 동시 냉각 전환, OrangeX OI도 첫 감소** (bico-reacceleration-ends-cooling-begins).
12. **BEAT: 2회차 큰 폭 재가속 후 3거래소 동시 상당폭 반락, Binance 소규모 리스팅 이번 회차 미확인(델리스팅 불확실)** (beat-pullback-after-reacceleration-binance-listing-unconfirmed).
13. **AEON: 3회차 재가속 끝에 3거래소 동시 첫 냉각** (aeon-first-simultaneous-cooling).
14. **CASHCAT: 가격은 3거래소 동조 냉각(2회차) 지속이나 OrangeX OI만 4회차 감소 멈추고 반등, 펀딩도 급등 — 거래소 간 포지셔닝 갈림** (cashcat-price-cools-orangex-oi-funding-diverge).
15. **BANK: 3회차 심화 후 개선됐으나 펀딩은 더 악화(플러스→마이너스 이후 추가 심화)** (bank-improves-but-funding-worsens-further).
16. **ANSEM: 평탄 회복 후 다시 마이너스로 재반전** (ansem-flat-recovery-reverses-negative).
17. **1000RATS·AAVE·ADA·ALLO: 각각 개선 지속·재냉각·소폭 심화·소폭 개선 — 방향 갈림** (mixed-directional-moves-1000rats-aave-ada-allo).
18. **⚠️ GIGGLE·KAITO 필드 이상치(순서 역전·완전동일)가 각각 5회차 연속 재현, GRAM 완전동일값도 3회차 연속 재현 — 구조적 패턴 굳어짐** (field-anomalies-fifth-third-round).
19. **HYNA:HYPE-USD: OI·거래량이 소수점까지 2회 연속 완전 동일 — CoinGecko 갱신 정체 가능성 강화** (hyna-hype-completely-unchanged-second-round).
20. **OKX ACE·BANK·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN은 이번 회차도 CoinGecko okex_swap 배열 미등재, OKX 직접 API로 보강. BEAT·BICO·AEON·BSB·CAP·CORE는 okex_swap 정상 확인** (okx-most-still-not-listed-direct-api-supplements).
21. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
22. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
23. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
24. **dydx_chain은 1차 429 이후 재시도로 확보 성공, 나머지 대부분은 1차 시도로 정상 확보** (dydx-recovers-on-retry-others-first-try).
25. **지금은 일요일 오후(UTC 04:29) 시간대** (sunday-afternoon-timing-caveat).

## 데이터 신뢰도

**CoinGecko binance_futures**: 1차 시도로 정상 확보. ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·
ASTER·ALGO·1000RATS 확인. **BEAT는 이번 회차 조회 표에 나타나지 않음**(직전 회차엔 소규모
리스팅으로 재확인됐던 것 — 델리스팅 여부는 불확실, 재확인 필요). BICO·GRAM·KAITO·MMT·PIPPIN·
GIGGLE·BLESS·CASHCAT·BSB·CORE·AEON·BTW·CAP·ETHFI·HYPE·HYPER·APEX·FARTCOIN·ANSEM은
Binance 미상장.

**CoinGecko bybit**: 1차 시도로 정상 확보. ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·
1000RATS 확인. **⚠️ BEAT는 이번 회차도 bybit 응답에서 미확인**(11회차 연속). BICO·KAITO·
MMT·PIPPIN·GIGGLE·BLESS·CASHCAT·BSB·CORE·AEON·BTW·CAP·ETHFI는 Bybit 미상장.

**CoinGecko okex_swap**: 1차 시도로 정상 확보. AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·
CAP·BEAT·BICO 확인. ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN은 이번 회차도 okex_swap
배열에서 미발견돼 OKX 직접 API 또는 Binance/Bybit로 대체 집계(회차 간 일관성 유지).

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+`public/open-interest`
(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인. `oiUsd` 필드 직접 사용
방법론을 20회차 연속 유지, vol24_usd=`volCcy24h`×`last` 계산 방식도 유지. **⚠️ GIGGLE**은
이번 회차도 vol24h(75,509,032)가 volCcy24h(755,090.32)보다 큰 역전된 필드 순서가 **5회차
연속** 재현됐다. **KAITO**는 vol24h=volCcy24h(221,463,338, 완전 동일) 이상치가 **5회차 연속**
재현됐다. **GRAM**도 이번 회차 vol24h=volCcy24h(1,847,373, 완전 동일)로 **3회차 연속**
재현돼 구조적 패턴에 더 가까워졌다. 세 이상치 모두 계산 방식은 그대로 유지했다.

**Hyperliquid**: 1차 시도로 정상 확보. 이번 회차 raw 응답의 funding 필드가 예년 스케일과
달리 100배 확대돼(예: ACE-USD -3.7%로 표시) 표기된 것을 과거 회차 값·타 종목과의 정합성으로
역산해 100으로 나눠 보정(예: ACE-USD -0.037%로 환산) — 원시값 자체는 신뢰하되 표기 스케일
이슈로 판단해 정정. ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·
ETHFI·ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD 등 raw 정밀값 확보. BICO·BEAT·CAP·MMT·BANK·AEON·AKE·
ALLO·BTW·BLESS·ANSEM은 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: 1차 시도로 정상 확보, raw 정밀 숫자로 직접 확보.
ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·BLESS·CASHCAT·BTW·ANSEM·AEON·ALGO·BEAT·BSB·
1000RATS 전량 확보. MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: 1차 시도로 정상 확보, raw 정밀값 직접 확보. ACE·AAVE·ALLO·
ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·CAP·BLESS·CASHCAT·BSB 확인. KAITO·1000RATS는
여전히 미발견.

**dYdX(`dydx_chain`)**: 1차 429 이후 재시도로 확보 성공, raw 정밀값(BTC-USD $0.92M/OI
$18.08M, ETH-USD $2.72M/OI $8.60M, SOL-USD $0.39M/OI $4.51M).

**CoinGecko `/global`**: **7회 연속 429로 확보 실패** — 직접 API 기반 총시총·도미넌스 수치를
갖지 못했다. WebSearch 스니펫이 직전 회차와 다른 수치($2.21T·58.88% vs 이전 $2.29T·56.8%)로
나와 캐시가 아닐 가능성이 있으나, 여전히 직접 API가 아니므로 참고용으로만 표기한다.

**Fear&Greed**: alternative.me API로 1차 시도 정상 응답, **31(Fear)** 확인 — 3회차 연속
동일값.

**신규 발견**: BLESS가 OrangeX·Aster 동시 대형 급락(-26%대)으로 신규 주목 대상에 편입됐다.
BTW는 4회차 연속 심화 끝에 마이너스에서 플러스로 극적 반전됐다. ACE는 언락 임박 속 4개
거래소 전부 동시 최대폭 냉각을 보였다. AKE는 3거래소 전부 동시에 플러스 전환을 되돌려
마이너스로 재반전됐다. GRAM은 장기 플러스권을 깨고 처음 마이너스로 전환됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접 조회분)의
CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를 직접 채택(회차
간 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·ALGO 등 복수 거래소
종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은 본문·`why`에 별도
표기했다; (e) 이번 회차 Hyperliquid 원시 funding 필드가 100배 확대된 스케일로 반환돼 과거
회차·타 종목과의 정합성을 근거로 100으로 나눠 보정했다 — 이 보정이 잘못됐을 가능성을
완전히 배제할 수 없어 참고용으로 표기한다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·
GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며, 이는
데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·HYNA:HYPE-USD·
BLESS는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다; (h) Binance BEAT 소규모 리스팅이
이번 회차 조회 표에 나타나지 않았는데, 델리스팅인지 조회 누락인지는 확정하지 않는다(과거에도
사라졌다 재등장한 전례 있음); (i) BLESS의 이번 회차 급락은 OrangeX·Aster 동시 발생으로
데이터 오류 가능성은 낮으나, 급락 배경(구체적 촉매)은 별도 확인하지 않았고 4월 유사 사건과의
직접적 인과관계도 확정하지 않는다; (j) 이번 회차 급변에 대한 인과관계 해석(언락 직전
디레버리징, 숏 청산 등)은 대체로 정황상 추정이며 확정된 것은 아니다; (k) GIGGLE·KAITO의
필드 이상치가 5회차 연속, GRAM도 3회차 연속 재현돼 구조적 패턴에 가까워졌으나 근본 원인(OKX
API 자체 특성인지)은 규명하지 않았다; (l) `/global`은 이번 회차 7회 연속 429로 실패했고
WebSearch 근사치는 직전 회차와 달라졌으나 여전히 직접 API가 아니라 신뢰도를 낮게 잡아야
한다; (m) 지금은 일요일 오후로 유동성 패턴이 평일과 다를 수 있으며, 확정 불가.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
