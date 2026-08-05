# 선물시장 스카우트 브리핑 — 2026-08-05 20:29 UTC (KST 2026-08-06 05:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-05T18:30:00Z)
> 로부터 약 1시간59분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`은 정상 응답 — 총시총 **약 $2.2989T**(직전 $2.29T와 거의 동일, 소폭 증가),
BTC도미넌스 **56.65%**(직전 56.54%, 소폭 상승), ETH도미넌스 **10.07%**(직전 10.10%, 소폭
하락), 24h 시총 변동 **+0.845%**(직전 +0.75%에서 소폭 재가속). Fear&Greed는 alternative.me
에서 이번 회차도 **27(Fear)**로 유지됐다(직전까지 10회 연속 동일값, 이번 회차도 이어짐).

**⚠️ 데이터 인프라: OKX CoinGecko(`okex_swap`) funding 표기 이슈 발견·정정** — 1차 조회에서
모델이 raw 값을 100배로 오환산해 '%' 문자열로 표기하는 오류를 발견해, raw 숫자값을 명시적으로
재요청해 정정했다(예: BICO funding 오표기 -0.3%→정정 -0.003). BICO·CORE·BEAT·AEON·CAP 5종목은
계속 정상 응답하나 CORE는 이번 회차 거래량이 $3.85M로 5M 문턱 아래로 내려가 별도 검색으로
확인했다. **KAITO·GRAM·GIGGLE·PIPPIN·MMT 5종목은 여전히 okex_swap 티커 배열에서 검색되지
않아** OKX 직접 API(`open24h`·`last` 기반 chg24, `oiUsd` 직접값 또는 `volCcy24h×last`/
`vol24h×last` 추정)를 유지했다 — 이번 회차부터 OI는 OKX 응답의 `oiUsd` 필드를 직접 사용해
추정 오차를 줄였다.

- **⚠️ BEAT(Audiera)**: CEX·DEX가 함께 마이너스로 급반전했다 — OKX +3.146%→**-6.647%**,
  Aster도 +3.79%→**-4.874%**로 함께 반전 — 직전 회차의 '개선 흐름 완결'이 한 회차만에
  뒤집혔다. 웹서치로 확인한 배경: 8/1 2,125만 BEAT($6,780만, 유통량 6.9%) 대규모 언락 이후
  초기엔 소각·수익 서사로 반등했으나(8/1 +19~30%), 8/3 -18% 급락에 이어 이번 회차도 하락이
  이어지는 흐름 — 언락 매도압력이 지속되는 것으로 보인다.
- **⚠️ CAP**: CEX·DEX 모두 큰 폭 둔화했다 — OKX +12.525%→**+0.446%**(거의 보합), Aster도
  +12.89%→**+3.051%**로 함께 크게 줄어 — 직전까지의 격차 좁힘 추세가 무색해질 만큼 둘 다
  정체됐다(격차는 오히려 0.37%p→2.61%p로 재확대).
- **⚠️ CASHCAT(HL/Aster)**: 5연속 재가속의 정점을 찍었다 — 거래량가중평균 +39.53%→
  **+65.749%**(HL+65.516%·Aster+67.875%)로 큰 폭 재가속, 웹서치로 확인: 고점 대비 약 60%
  하락한 상태에서도 신규 지갑들의 대규모 매수세가 이어지고 있다는 보도(cryptotimes.io)가
  재확인됐다 — Robinhood Chain 밈코인 열기가 여전히 뜨겁다.
- **⚠️ BLESS(OrangeX·Aster)**: 두 거래소가 거의 완전히 수렴했다 — OrangeX
  +137.308%→**+131.92%**로 정점에서 소폭 하락, Aster는 +130.27%→**+130.282%**로 거의
  변동 없어 가격 격차가 7.0%p→**1.64%p**로 크게 좁혀졌다(직전의 '동조 폭등'이 이번엔 '거의
  완전 수렴'으로 진화) — 촉매는 이번 회차도 웹서치로 특정하지 못해 미확인(BLESS는
  엣지컴퓨팅 마켓플레이스 토큰).
- **⚠️ 1000RATS**: CEX·DEX가 2연속 동반 재가속했다 — CEX 가중평균 +6.626%→**+16.688%**,
  DEX(Aster) +4.20%→**+13.821%**로 둘 다 크게 가속 — 웹서치로 확인: Aster DEX가 8/1
  1000RATS 신규 퍼프 마켓을 개설하며 8/7까지 1.2배 포인트 부스트 프로모션을 진행 중임을
  확인해, DEX 유동성 인센티브가 CEX 랠리와 함께 맞물린 것으로 추정된다.

한편 **⚠️ AKE는 CEX·DEX가 다시 함께 마이너스로 반전**했다(CEX -0.0748%→**-5.044%**, DEX
+1.03%→**-5.17%**, 3연속 휩소). **⚠️ ADA는 CEX·HL이 함께 다시 악화**됐다(CEX -0.957%→
**-1.655%**, HL -1.079%→**-1.695%**로 '반전 조짐'이 무산). **⚠️ AAVE는 CEX·HL이 함께
마이너스로 전환**했다(CEX +0.358%→**-0.106%**, HL +0.528%→**-0.345%**). **⚠️ ALGO도 CEX·HL이
함께 마이너스로 전환**했다(CEX +0.319%→**-1.262%**, HL +0.299%→**-1.149%**, 2연속 플러스
종료). **ASTER(CEX·DEX)는 다시 함께 플러스로 전환**했다(CEX -0.236%→**+0.234%**, DEX
-0.16%→**+0.28%**). **BANK(Lorenzo)는 CEX·DEX가 다시 함께 개선**됐다(CEX -19.230%→
**-15.743%**, DEX -17.10%→**-16.225%**, 세 번째 방향 전환). **BICO는 CEX가 계속 가속하고
DEX는 소폭 둔화해 격차가 거의 닫혔다**(CEX +24.829%→**+28.665%**, DEX +30.34%→**+27.898%**,
격차 5.5%p→0.77%p). **KAITO는 CEX 3연속 둔화, HL은 거의 정지 수준까지 급격히 둔화**했다
(CEX +2.416%→**+1.947%**, HL +2.738%→**+0.177%**). **BTW는 완만한 둔화 흐름을 깨고
재가속**했다(+17.23%→**+21.047%**). **HYPE는 OI가 3연속 증가 후 이번엔 감소 전환**했다(OI
$1,263.92M→**$1,245.80M**, 가격 상승폭도 +3.964%→**+3.116%**로 둔화). **dYdX는 ETH·BTC
funding 격차가 사실상 닫혔다**(ETH funding +0.012%→**+0.002%**, BTC funding -0.003%→
**-0.001%**, 격차 0.015%p→0.003%p) — 가격은 둘 다 상승(ETH +2.636%, BTC +1.16%).
**FARTCOIN은 반등이 다시 꺾여 마이너스로 전환**했다(+0.670%→**-0.861%**).

**⚠️ 신규 포착: HYNA:PUMP-USD(Hyperliquid)** — OI $148.07M·거래량 $79.63M의 대형 종목이 이번
회차 처음 관찰됐다(PUMP.fun 토큰 기반, Hyperliquid HIP-3 계열 마켓 접두사로 추정, 크립토
네이티브). chg24 -2.142%로 방향성은 크지 않으나 OI 규모가 HYPE 다음으로 크다 — 이전 회차
관찰 범위에 없었기에 첫 편입이며, 지속 관찰이 필요하다.

**GRAM은 CEX·HL 6연속 플러스에 가속**했다(CEX+1.805%, HL+1.74%). **GIGGLE은 3연속 가속 후
이번엔 둔화**했다(+10.145%→**+6.157%**). **MMT는 급반등하며 funding이 거의 0으로
완화**됐다(+1.533%→**+5.470%**, funding -0.02126%→**-0.000418%**). **PIPPIN은 낙폭이 계속
확대**됐다(-3.787%→**-4.589%**). **CORE는 3연속 플러스를 유지하나 거래량이 문턱 아래로
축소**됐다(+2.423%→**+2.283%**, 거래량 $3.99M→$3.85M). **AEON은 CEX·DEX 분화 방향이
뒤집혔다**(CEX -4.735%→**-3.805%** 개선, DEX -1.68%→**-3.686%** 악화 — 직전과 반대 역할).
**ANSEM은 낙폭이 다소 줄었다**(-4.04%→**-2.793%**). **ALLO는 CEX·DEX가 함께 거의 완전히
정체**됐다(CEX+2.475%→+0.110%, DEX+2.16%→+0.301%). **AIO는 큰 폭 하락이 계속되나 소폭
개선**됐다(-9.462%→**-8.742%**, funding은 크게 확대 0.0086%→0.0339%). **CASHCAT·BTW는 CEX
상장이 확인되지 않아 DEX 섹션에서만 집계했다. 완전 신규 크립토 네이티브 대형 종목은
HYNA:PUMP-USD 외에는 이번 회차도 발견되지 않았다. GMX는 이번 회차도 재조회하지 않고 계속
제외**했다.

## ⚠️ 데이터 인프라 이슈

`derivatives/exchanges/okex_swap`은 이번 회차도 BICO·CORE·BEAT·AEON·CAP 5종목에 정상
응답했으나, **1차 조회에서 funding_rate가 raw 값의 100배로 오환산(예: BICO -0.3%로 오표기)돼
있음을 발견하고 raw 숫자값을 명시적으로 재요청해 정정했다**(BICO 정정값 -0.003). 이는 요청
프롬프트가 "%"를 명시했을 때 모델이 raw 소수를 퍼센트로 재해석하며 발생한 것으로 추정되며,
이번 정정을 계기로 향후 회차에서도 raw 값 요청 시 별도 검증이 필요하다는 점을 기록해둔다.
CORE는 이번 회차 거래량이 $3.85M로 5M 문턱 아래로 내려가 기본 top-N 조회에서 누락돼 별도
검색으로 확인했다.

**KAITO·GRAM·GIGGLE·PIPPIN·MMT 5종목은 여전히 CoinGecko okex_swap 티커 배열에서 발견되지
않아** OKX 직접 API(`market/ticker`+`public/open-interest`+`public/funding-rate`)를
유지했다. 이번 회차부터 OI는 OKX 응답의 `oiUsd` 필드(직접 계산된 USD 환산값)를 사용해 이전
회차의 `oiCcy×last` 수동 추정 대비 정확도를 개선했다. 거래량은 `vol24h`와 `volCcy24h`가
동일값으로 나오는 이상 케이스(KAITO·GRAM·MMT·PIPPIN)에서 `vol24h×last` 또는
`volCcy24h×last`(배율에 따라 선택)로 추정했다.

GMX(`gmx-perpetuals-v2-arbitrum`)는 다회차 연속 완전 동일 수치가 확정된 상태로, 이번 회차도
재조회하지 않고 제외를 유지한다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **⚠️ BEAT (Audiera)** [CEX·DEX 함께 마이너스 급반전] | OKX(CoinGecko 정상) | $96.77M | $8.11M | +0.005% | -6.647% | +3.146%→-6.647% 급반전, DEX(-4.874%)도 함께 반전 — 8/1 언락($6,780만, 유통량6.9%) 이후 8/1 반등→8/3 -18%→이번 회차도 약세(웹서치: 언락 매도압력) | listing-unlock-both-flip-negative-sharply |
| 1000RATS [2연속 동반 재가속] | Binance/Bybit | $129.56M | $25.80M | +0.034134% | +16.688% | +6.626%→+16.688% 크게 가속, DEX(+13.821%)도 함께 — Aster 8/1 신규 마켓 개설·8/7까지 포인트부스트(웹서치 확인), DEX 인센티브 랠리 추정 | reaccelerates-2nd-round-dex-listing-incentive |
| BICO (Biconomy) [CEX 계속 가속, 격차 거의 닫힘] | OKX(CoinGecko 정상) | $146.92M | $4.77M | -0.003% | +28.665% | +24.829%→+28.665% 계속 상승, DEX(+27.898%) 소폭 둔화로 격차 5.5%p→0.77%p 좁혀짐 — 여러 회차 휩소 후 첫 수렴 | cex-continues-accelerating-gap-nearly-closes |
| **⚠️ AKE (Akedo)** [CEX·DEX 다시 함께 마이너스] | Binance/Bybit | $84.88M | $43.70M | +0.028289% | -5.044% | -0.0748%→-5.044% 급락, DEX(-5.17%)도 함께 반전 — 3연속 휩소 | third-consecutive-whipsaw-both-flip-negative-again |
| **⚠️ CAP** [CEX·DEX 모두 큰 폭 둔화, 격차 재확대] | OKX(CoinGecko 정상) | $18.89M | $1.31M | +0.005% | +0.446% | +12.525%→+0.446% 거의 정지, DEX(+3.051%)도 크게 축소, 격차 0.37%p→2.61%p 재확대 | both-decelerate-sharply-gap-widens-again |
| **⚠️ ADA** [CEX·HL 함께 재악화] | Binance/Bybit | $267.41M | $170.97M | +0.01% | -1.655% | -0.957%→-1.655% 낙폭 재확대, HL(-1.695%)도 함께 악화 — '반전 조짐' 무산 | reverses-again-both-worsen-together |
| **⚠️ AAVE** [CEX·HL 함께 마이너스 전환] | Binance/Bybit | $86.84M | $92.96M | -0.00989% | -0.1064% | +0.358%→-0.106% 반전, HL(-0.345%)도 함께 반전 | both-flip-negative-together |
| **⚠️ ALGO** [CEX·HL 함께 마이너스, 2연속 플러스 종료] | Binance/Bybit | $14.49M | $16.82M | +0.004853% | -1.2618% | +0.319%→-1.262% 반전, HL(-1.149%)도 함께 반전 | flips-negative-together-positive-streak-ends |
| BANK (Lorenzo) [CEX·DEX 다시 함께 개선] | Binance/Bybit | $255.96M | $21.47M | -0.02846% | -15.743% | -19.230%→-15.743% 낙폭 축소, DEX(-16.225%)도 함께 — 세 번째 방향 전환(오실레이션 지속) | both-improve-again-oscillation-continues |
| KAITO (CEX) [3연속 둔화, HL 거의 정지] | OKX(직접API) | $39.26M(추정) | $7.16M | -0.005119% | +1.947% | +2.416%→+1.947% 3연속 축소, HL(+2.738%→+0.177%) 거의 정지 수준까지 급둔화 | third-consecutive-deceleration-hl-nearly-stalls |
| AIO (OlaXBT) [큰 낙폭 지속, 소폭 개선] | Binance/Bybit | $11.39M | $4.14M | +0.033857% | -8.742% | -9.462%→-8.742% 소폭 개선, funding은 0.0086%→0.0339%로 크게 확대 | large-decline-persists-mild-improvement-funding-surges |
| GRAM [6연속 플러스, 가속] | OKX(직접API) | $5.27M(추정) | $6.76M | +0.004365% | +1.805% | +1.079%→+1.805% 확대, HL(+1.74%)도 가속 — whipsaw 이후 최장 지속(6연속) | sixth-consecutive-positive-accelerates |
| GIGGLE (Giggle Fund) [3연속 가속 후 둔화] | OKX(직접API) | $40.29M(추정) | $3.36M | +0.005% | +6.157% | +10.145%→+6.157% 축소 — 최대폭 가속 흐름이 한 회차만에 꺾임. DEX 상장 미확인 | third-round-acceleration-ends-decelerates |
| AEON [CEX·DEX 분화 방향 역전] | OKX(CoinGecko 정상) | $11.57M | $3.43M | -0.027% | -3.805% | -4.735%→-3.805% 개선, DEX(-3.686%)는 오히려 악화 — 직전과 반대 역할 | diverges-roles-reverse-cex-improves-dex-worsens |
| PIPPIN [낙폭 지속 확대] | OKX(직접API) | $6.67M(추정) | $1.94M | +0.005% | -4.589% | -3.787%→-4.589% 낙폭 확대, funding은 소폭 완화 | decline-continues-to-widen |
| MMT (Momentum) [급반등, funding 거의 0] | OKX(직접API) | $15.87M(추정) | $2.86M | -0.000418% | +5.47% | +1.533%→+5.470% 재가속, funding -0.02126%→-0.000418%로 거의 중립화 | sharp-rebound-funding-nearly-neutral |
| CORE [3연속 플러스, 거래량 문턱 아래] | OKX(CoinGecko, 5M 아래) | $3.85M | $1.10M | -0.021% | +2.283% | +2.423%→+2.283% 거의 정체, 거래량 $3.99M→$3.85M로 축소 | holds-positive-3rd-round-volume-shrinks-below-threshold |
| ASTER (CEX) [다시 함께 플러스 전환] | Binance/Bybit | $14.39M | $113.49M | +0.005% | +0.23412% | -0.236%→+0.234% 재전환, DEX(+0.28%)도 함께 — 동조 휩소 패턴 지속 | flips-positive-together-again-oscillation-pattern |
| ALLO (Allora) [CEX·DEX 함께 거의 완전 정체] | Binance/Bybit | $19.49M | $16.81M | -0.021633% | 0.11009% | +2.475%→+0.110% 크게 둔화, DEX(+0.301%)도 함께 축소 | both-decelerate-to-near-flat |
| ATOM [함께 개선 지속] | Binance/Bybit | $15.36M | $30.66M | +0.009338% | -0.7411% | -1.295%→-0.741%, HL(-0.879%)도 유사하게 개선 | continues-mild-improvement-together |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **⚠️ HYNA:PUMP-USD** [신규 포착, 대형 OI] | Hyperliquid | $79.63M | $148.07M | +0.001% | -2.142% | 이번 회차 처음 관측 — OI HYPE 다음으로 대형, PUMP.fun 토큰 기반 추정(크립토 네이티브). 방향성은 크지 않으나 규모 주목, 지속 관찰 필요 | newly-captured-large-oi-hip3-market |
| **⚠️ BLESS-USDT-PERPETUAL** [Aster와 거의 완전 수렴] | OrangeX | $472.81M | $221.36M | -0.01% | +131.92% | +137.308%→+131.92% 정점에서 소폭 하락, Aster(+130.282%)와 격차 7.0%p→1.64%p로 좁혀짐. funding도 완화. 촉매 미확인 | nearly-fully-converges-with-aster |
| **⚠️ BLESS-USDT** [OrangeX와 거의 완전 수렴] | Aster | $2.15M | $0.49M | +0.045% | +130.282% | +130.27%→+130.282% 거의 변동 없어 OrangeX 하락과 만나 격차 크게 좁혀짐 | nearly-fully-converges-with-orangex-flat-itself |
| **⚠️ CASHCAT** [5연속 재가속 정점] | Hyperliquid/Aster | $25.00M | $17.94M | +0.016118% | +65.749% | +39.53%→+65.749%(HL+65.516%·Aster+67.875%) 큰 폭 재가속 — 고점대비 60%↓에도 신규 지갑 매수세 지속(웹서치 재확인), Robinhood Chain 밈코인 열기 지속 | fifth-consecutive-reacceleration-peaks |
| **⚠️ 1000RATS-USDT** [CEX와 2연속 동반 재가속] | Aster | $0.29M | $0.06M | +0.011% | +13.821% | +4.20%→+13.821% 크게 가속, CEX(+16.688%)와 함께 — Aster 8/1 신규 마켓 개설·8/7까지 포인트부스트(웹서치 확인) | reaccelerates-2nd-round-dex-listing-incentive |
| BTW [완만한 둔화 깨고 재가속] | Aster | $1.75M | $11.18M | +0.035% | +21.047% | +17.23%→+21.047%로 2회 연속 둔화 흐름이 끝나고 재가속. CEX 상장 미확인 | breaks-deceleration-reaccelerates |
| BICO-USDT [CEX와 격차 거의 닫힘] | Aster | $0.81M | $0.054M | +0.001% | +27.898% | +30.34%→+27.898% 소폭 둔화, CEX(+28.665%)와 격차 5.5%p→0.77%p로 거의 완전 수렴 | gap-nearly-closes-with-cex |
| **⚠️ AKE-USDT** [CEX와 다시 함께 마이너스] | Aster | $0.71M | $10.97M | +0.015% | -5.17% | +1.03%→-5.17% 급락, CEX(-5.044%)와 함께 — 3연속 휩소 | third-consecutive-whipsaw-flips-negative-with-cex |
| ASTER-USDT [대규모 OI, CEX와 다시 함께 플러스] | Aster | $8.70M | $221.72M | 0.0% | +0.28% | OI $221.7M 대형 유지, -0.16%→+0.28%로 CEX(+0.234%)와 함께 재전환 — 동조 휩소 패턴 지속 | large-oi-holds-flips-positive-with-cex-again |
| **⚠️ CAP-USDT** [CEX와 함께 큰 폭 둔화, 격차 재확대] | Aster | $0.019M | $0.028M | +0.001% | +3.051% | +12.89%→+3.051% 크게 축소, CEX(+0.446%)와 함께 둔화되나 격차 0.37%p→2.61%p로 재확대 | decelerates-sharply-with-cex-gap-widens |
| ANSEM [낙폭 다소 축소] | Aster | $0.30M | $1.20M | +0.001% | -2.793% | -4.04%→-2.793% 낙폭 다소 축소 — 개선·악화 오실레이션 지속 | decline-narrows-somewhat |
| AEON-USDT [CEX와 분화 방향 역전, 이번엔 악화] | Aster | $0.045M | $0.209M | +0.001% | -3.686% | -1.68%→-3.686% 악화, CEX는 오히려 개선(-3.805%) — 역할 뒤바뀐 분화 | diverges-roles-reverse-worsens-while-cex-improves |
| ALLO-USDT [CEX와 함께 거의 완전 정체] | Aster | $0.10M | $0.024M | -0.009% | +0.301% | +2.16%→+0.301% 크게 둔화, CEX(+0.110%)와 함께 보합권 진입 | decelerates-to-near-flat-with-cex |
| **⚠️ BEAT** [CEX와 함께 마이너스 급반전] | Aster | $0.43M | $0.26M | +0.001% | -4.874% | +3.79%→-4.874% 급반전, CEX(-6.647%)와 함께 — 8/1 언락 이후 매도압력 지속(웹서치 확인) | listing-unlock-flips-negative-with-cex |
| BANK-USDT [CEX와 함께 다시 개선] | Aster | $0.92M | $0.35M | -0.005% | -16.225% | -17.10%→-16.225% 개선, CEX(-15.743%)와 함께 낙폭 축소 — 오실레이션 지속 | improves-again-with-cex-oscillation-continues |
| GRAM [CEX와 6연속 플러스, 가속] | Hyperliquid | $1.80M | $13.05M | +0.001% | +1.74% | +0.890%→+1.74% 확대, CEX(+1.805%)와 함께 6연속 플러스 최장 지속 | sixth-consecutive-positive-accelerates-tracks-cex |
| HYPE-USD [OI 3연속 증가 후 감소 전환] | Hyperliquid | $276.90M | $1,245.80M | 0.0% | +3.116% | OI $1,263.92M→$1,245.80M로 3연속 증가세 꺾임, 가격 상승폭도 +3.964%→+3.116% 둔화 | oi-declines-after-3rd-round-price-decelerates |
| HYPER-USD [플러스 확대 3연속] | Hyperliquid | $0.32M | $0.32M | -0.02% | +2.71% | +1.919%→+2.71% 확대 지속 — 저유동 소형종목 변동성 | holds-positive-3rd-consecutive-expansion-low-liquidity |
| **⚠️ KAITO-USD** [CEX와 함께 급격히 둔화, 거의 정지] | Hyperliquid | $4.26M | $25.20M | +0.001% | +0.177% | +2.738%→+0.177% 급격 둔화, CEX(+1.947%)와 함께 3연속 동반 둔화 심화 | third-consecutive-deceleration-nearly-stalls-with-cex |
| APEX-USD [플러스 거의 유지] | Hyperliquid | $0.094M | $0.80M | +0.001% | +1.356% | +1.370%→+1.356%로 사실상 변동 없음, 저유동 소형종목 | holds-positive-roughly-flat-low-liquidity |
| FARTCOIN [반등 다시 꺾여 마이너스 전환] | Hyperliquid | $5.84M | $22.80M | +0.001% | -0.861% | +0.670%→-0.861% 반전 — 반등·둔화 반복이 마이너스로 귀결 | rebound-flips-negative |
| **⚠️ ADA-USD** [CEX와 함께 재악화] | Hyperliquid | $5.09M | $31.75M | -0.003% | -1.695% | -1.079%→-1.695% 낙폭 재확대, CEX(-1.655%)와 함께 — 반전 조짐 무산 | worsens-again-together-with-cex |
| **⚠️ AAVE-USD** [CEX와 함께 마이너스 전환] | Hyperliquid | $9.26M | $60.61M | -0.003% | -0.345% | +0.528%→-0.345% 반전, CEX(-0.106%)와 함께 마이너스 전환 | flips-negative-together-with-cex |
| ATOM-USD [CEX와 함께 소폭 개선] | Hyperliquid | $0.49M | $2.01M | -0.001% | -0.879% | -1.215%→-0.879%로 CEX(-0.741%)와 유사한 수준 함께 개선 | tracks-cex-mildly-improves |
| **⚠️ ALGO-USD** [CEX와 함께 마이너스, 2연속 플러스 종료] | Hyperliquid | $0.57M | $2.34M | +0.001% | -1.149% | +0.299%→-1.149% 반전, CEX(-1.262%)와 함께 마이너스 전환 | flips-negative-together-positive-streak-ends |
| ETH-USD [funding 거의 중립, 가격 상승] | dYdX | $60.46M | $26.21M | +0.002% | +2.636% | +0.012%→+0.002%로 거의 중립화, 가격은 +2.447%→+2.636%로 더 가속 — BTC와 funding 격차 사실상 닫힘 | funding-nearly-neutralizes-price-keeps-rising |
| BTC-USD [funding 완화 지속, 가격 가속] | dYdX | $5.54M | $18.30M | -0.001% | +1.16% | -0.003%→-0.001%로 완화, 가격 +0.509%→+1.16%로 가속 — ETH·BTC funding 격차 0.015%p→0.003%p로 사실상 닫힘 | funding-continues-easing-price-accelerates |
| ETHFI-USD [3연속 플러스, 가속] | Hyperliquid | $3.00M | $7.78M | +0.001% | +1.368% | +1.089%→+1.368% 확대 — 2연속에서 3연속으로 이어지며 가속 | third-consecutive-positive-accelerates |

## 테마 태그

1. **시장 전반: 총시총 약 $2.2989T(직전과 거의 동일), BTC도미넌스 56.65%, ETH 10.07%, 24h 시총 변동 +0.845%(직전 +0.75%에서 소폭 재가속). Fear&Greed 27(Fear) 유지 지속** (market-mild-reacceleration-fear-greed-persists).
2. **⚠️ 데이터 인프라: OKX CoinGecko funding 표기 오류 발견·정정(1차 조회 100배 오환산 → raw값 재요청으로 정정), CORE 거래량 5M 문턱 아래로 축소, KAITO·GRAM·GIGGLE·PIPPIN·MMT는 계속 OKX 직접API 유지(oiUsd 직접값 사용으로 정확도 개선)** (data-infra-funding-format-bug-caught-corrected).
3. **⚠️ BEAT: CEX·DEX 함께 마이너스로 급반전 — 8/1 대규모 언락($6,780만) 이후 매도압력 지속(웹서치 확인)** (beat-flips-negative-unlock-pressure).
4. **⚠️ CAP: CEX·DEX 모두 큰 폭 둔화, 격차 재확대** (cap-both-decelerate-gap-widens).
5. **⚠️ CASHCAT 5연속 재가속 정점(+65.7%) — Robinhood Chain 밈코인 열기 지속(웹서치 재확인)** (cashcat-fifth-round-peaks).
6. **⚠️ BLESS(OrangeX·Aster) 두 거래소 거의 완전 수렴(격차 7.0%p→1.64%p)** (bless-nearly-fully-converges).
7. **⚠️ 1000RATS CEX·DEX 2연속 동반 재가속 — Aster DEX 8/1 신규 마켓 개설·8/7까지 포인트 부스트(웹서치 확인)** (1000rats-reaccelerates-dex-incentive).
8. **⚠️ AKE CEX·DEX 다시 함께 마이너스로 반전(3연속 휩소)** (ake-third-whipsaw-negative-again).
9. **⚠️ ADA·AAVE·ALGO: 세 종목 모두 CEX·HL이 함께 마이너스로 전환/재악화 — 직전의 개선·플러스 흐름이 일제히 무산** (ada-aave-algo-all-flip-negative-together).
10. **ASTER(CEX·DEX)·BANK(CEX·DEX): 지속적인 동조 오실레이션 패턴** (aster-bank-continued-oscillation).
11. **BICO: CEX 계속 가속·DEX 소폭 둔화로 격차 거의 닫힘(5.5%p→0.77%p)** (bico-gap-nearly-closes).
12. **KAITO: CEX 3연속 둔화, HL은 거의 정지 수준(+0.177%)까지 급격 둔화** (kaito-hl-nearly-stalls).
13. **BTW: 완만한 둔화 깨고 재가속(+17.23%→+21.047%)** (btw-breaks-deceleration-reaccelerates).
14. **HYPE: OI 3연속 증가 후 이번엔 감소 전환, 가격 상승폭도 둔화** (hype-oi-declines-after-3rd-round).
15. **dYdX ETH·BTC funding 격차 사실상 닫힘(0.015%p→0.003%p), 가격은 둘 다 상승** (dydx-funding-gap-nearly-closed).
16. **⚠️ 신규 포착: HYNA:PUMP-USD(Hyperliquid) — OI $148.07M 대형 종목, 이번 회차 첫 편입** (hyna-pump-newly-captured-large-oi).
17. **GRAM CEX·HL 6연속 플러스 가속(최장 지속 갱신), GIGGLE은 3연속 가속 후 둔화, MMT는 급반등+funding 거의 중립화, PIPPIN은 낙폭 계속 확대** (gram-6th-giggle-decelerates-mmt-rebounds-pippin-widens).
18. **AEON CEX·DEX 분화 방향 역전, ANSEM 낙폭 소폭 축소, ALLO CEX·DEX 함께 거의 완전 정체, AIO 큰 낙폭 지속하되 소폭 개선, FARTCOIN 반등이 마이너스로 전환** (aeon-role-reversal-ansem-allo-aio-fartcoin).
19. **완전 신규 크립토 네이티브 대형 종목: HYNA:PUMP-USD 외 추가 발견 없음** (no-additional-new-native-listing).
20. **⚠️ GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**CoinGecko OKX(okex_swap)**: BICO·CORE·BEAT·AEON·CAP 5종목 정상 응답. **이번 회차 1차
조회에서 funding_rate가 raw 값의 100배로 오환산돼 '%' 문자열로 표기되는 오류를 발견**,
raw 숫자값을 명시적으로 재요청해 정정했다(예: BICO -0.3%(오표기)→-0.003(정정)). CORE는
거래량이 $3.85M로 5M 문턱 아래로 내려가 별도 검색으로 확인했다. KAITO·GRAM·GIGGLE·PIPPIN·
MMT 5종목은 여전히 티커 배열에서 미발견돼 OKX 직접 API를 유지했다 — 이번 회차부터 OI는
`oiUsd` 필드를 직접 사용해 이전의 `oiCcy×last` 수동 추정 대비 정확도를 개선했다. 거래량은
`vol24h`와 `volCcy24h`가 동일값으로 나오는 이상 케이스(KAITO·GRAM·MMT·PIPPIN)에서
`vol24h×last`/`volCcy24h×last`(배율에 따라 선택)로 추정했다.

**CoinGecko 파생 거래소 API**: binance_futures·bybit·hyperliquid·aster·dydx_chain·
orangex_futures 모두 이번 회차 정상 응답했다. 요청 빈도 제한을 피하기 위해 관심 심볼 위주로
타겟 조회를 병행했다 — 전체 유니버스 완전 스캔은 아니다.

**CoinGecko `/global`**: 정상 응답, 총시총 $2,298,851,537,074(정밀값 확보), BTC도미넌스
56.65131%, ETH도미넌스 10.06885%, 24h 시총 변동 +0.845345%.

**Fear&Greed**: alternative.me API로 27(Fear) 확인, 여러 회차 연속 동일값 지속.

**신규 상장/급등 스캔**: Hyperliquid 티커 재스캔 중 HYNA:PUMP-USD(OI $148.07M, 거래량
$79.63M)가 새로 포착됐다 — PUMP.fun 토큰 기반으로 추정되며 HIP-3 계열 마켓 접두사(HYNA:)로
보인다. 그 외 CEX(Binance/Bybit/OKX) 대형 신규 크립토 네이티브 종목은 이번 회차 스캔
범위에서 발견되지 않았다.

**웹서치 촉매 확인**: BEAT(Audiera) 8/1 언락($6,780만) 및 매도압력 지속, CASHCAT 고점대비
60%↓에도 신규 지갑 매수세 지속, 1000RATS Aster DEX 8/1 신규 마켓·8/7까지 포인트부스트
프로모션을 확인했다. BLESS·CAP·AKE의 이번 회차 급변 촉매는 특정하지 못해 미확인으로
표기한다.

한계: (a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트+Hyperliquid 재스캔 범위 내에서
수행했으며 완전한 전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번
회차도 규약에 따라 cex/dex 리스트에서 전부 제외했다(Binance/Bybit 조회 중 AMD·AMZN·AAPL·
ANTHROPIC·CRCL·CL·AAOI·AMDSTOCK 등 토큰화 주식/상품 perp 다수 확인, 전부 제외 처리); (c)
KAITO·GRAM·GIGGLE·PIPPIN·MMT 5종목의 CEX 거래량·OI는 OKX 직접 API 기반 추정치다; (d) BANK·
1000RATS·ALLO·AAVE·ADA·ATOM·ASTER(CEX)·AIO·ALGO·AKE 등 복수 거래소 종목의 `chg24`·`funding`은
거래량가중평균 계산값이며, 개별 거래소 값은 `why` 필드에 별도 표기했다; (e) GIGGLE·BTW·
CASHCAT은 DEX 또는 CEX 한쪽에서만 상장이 확인돼 해당 섹션에서만 집계했다; (f) HYNA:PUMP-USD의
마켓 접두사(HYNA:) 정확한 의미는 확정하지 못해 추정으로 표기한다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
