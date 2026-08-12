# 선물시장 스카우트 브리핑 — 2026-08-12 02:29 UTC (KST 2026-08-12 11:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-12T00:27:00Z)
> 로부터 약 2.0시간 경과.**

## 이번 회차 핵심 요약 — ACE 전 소스 급반등(숏커버링 정황), KAITO 반등 되돌림, CASHCAT 첫 3소스 수렴

이번 회차는 binance_futures·bybit·okex_swap·hyperliquid·aster·OKX직접API(5종)에 더해
**직전 회차 실패했던 orangex_futures·dydx_chain 2종이 1차 시도부터 정상 확보**됐다(직전
회차와 실패군이 다시 뒤바뀌는 순환 레이트리밋 패턴 지속). CoinGecko `/global`만 3회
재시도 전부 429로 미확인 처리(총시총·BTC도미넌스는 직전 회차 값 유지).

## ⚠️⚠️ 최우선 추적 — 언락 임박 3종 (BANK 8/17·ACE 8/18·KAITO 8/20)

### ACE — 8/18 약 5.9일 앞, ⚠️⚠️ 전 소스 동시 큰 폭 반등, OI 감소로 숏커버링 정황

이번 회차 최대 이벤트. Binance+Bybit 가중 -17.125%→**-11.594%**, HL -17.065%→
**-11.34%**, Aster -14.986%→**-11.36%**, OrangeX(확인 복귀) 직전 carry -13.158%→
**-11.092%**로 **4개 소스가 거의 동일한 폭(-11.1~11.6%)으로 동시 개선**됐다. 동시에
OI는 CEX 가중 $8.06M→**$8.00M**(보합~소폭감소), OrangeX $4.79M(carry)→**$3.95M
(-17.6%)**로 감소해 **가격반등+OI감소가 함께 관측**됐다 — 순수 매도압력이 아니라
숏 커버링 정황에 부합한다. 다만 OrangeX가 직전 미확인 구간이 있어 완전한 연속치
비교는 아니라는 점은 유의.

### BANK — 8/17 약 4.9일 앞, 재악화 더 확대·OI는 실측 감소로 서술 정정

Binance -8.441%·Bybit -9.11%(가중 -7.142%→**-8.536%**)로 재악화가 더 커졌다.
Aster도 -7.825%→**-9.626%**로 동반 재악화. **OrangeX가 이번 회차 확인 복귀**했는데,
OI가 $1.60M(직전 carry값)→**$1.51M로 오히려 -5.9% 감소**해, 직전까지 이어온
'OrangeX OI +13% 증가 지속' 서술이 정정됐다(carry-forward 추정이 실제 방향과
달랐음이 드러난 사례). CEX 가중 OI는 $16.68M→**$16.28M**로 소폭 감소했다.

### KAITO — 8/20 12:00 UTC 언락(공급 약13.5%) 약 8.4일 앞, 반등 일부 되돌림·OI는 계속 증가

직전 회차 처음 관측된 반등이 이번 회차 일부 되돌려졌다 — OKX직접 -3.664%→
**-4.776%**, HL -3.497%→**-4.44%**로 재하락했다. 반면 OI는 OKX $8.07M→
**$8.13M(+0.8%)**, HL $12.59M→**$12.78M(+1.5%)**로 여전히 양쪽 모두 증가가
계속됐다 — **'가격은 등락해도 OI는 꾸준히 늘어나는' 패턴이 이번 회차로 재확인**돼,
순수 숏 커버링보다는 신규 숏 유입이 지속되며 가격만 등락하는 그림에 조금 더 무게가
실린다. funding은 raw -0.0027089→**-0.0022554**로 3회차 연속 완화 추세다
(-0.0039033→-0.0027089→-0.0022554).

## 이번 회차 추가 최우선 관찰

### CASHCAT — ⚠️⚠️ HL·Aster·OrangeX 3소스 처음으로 동시 플러스 수렴

HL **-0.56%→+0.068%→+2.653%**, Aster **-2.531%→+2.264%**, OrangeX(확인 복귀)
직전 carry -2.947%→**+1.016%**. 여러 회차 이어지던 소스 간 분열이 이번 회차 처음
해소됐다.

### BEAT — 낙폭 대폭 추가 축소, 3소스 모두 강한 회복

OKX **-34.431%→-20.843%**, Aster **-34.194%→-17.935%**, OrangeX(확인 복귀)
직전 carry -46.829%→**-21.363%**로 3소스 모두 큰 폭 회복이 이어졌다.

### BICO — 4회차 연속 재악화

OKX **-8.857%→-8.931%**, Aster **-10.114%→-10.991%**, OrangeX(확인 복귀) 직전
carry -7.991%→**-11.429%**로 대폭 악화.

### CAP — 재상승 확대 지속

OKX **+18.769%→+26.641%**, Aster **+19.12%→+26.203%**, OrangeX(확인 복귀) 직전
carry +17.237%→**+21.093%**로 전 소스 강한 상승이 지속됐다.

### AEON — ⚠️⚠️ 전 소스 강한 플러스 전환

OKX **+2.271%→+8.504%**, Aster **-0.205%→+7.464%**(마이너스→강한플러스), OrangeX
(확인 복귀) 직전 carry -0.802%→**+7.726%**(역시 마이너스→강한플러스)로 3소스 모두
강한 랠리가 확인됐다.

### AAVE — 3소스 전부 플러스로 전환

CEX 가중 **-0.832%→+0.329%**, Aster **-0.909%→+0.101%**, HL **-0.798%→+0.421%**.

### ALGO — 좁은 밴드 이탈, 뚜렷 개선

여러 회차 이어지던 -1.86~1.93%대 밴드를 이탈해 3소스 모두 개선 — 가중
**-1.932%→-0.576%**, Aster **-1.928%→-0.502%**, HL **-1.865%→-0.263%**.

### ALLO·1000RATS — 소스 간 엇갈림 대부분 해소

ALLO는 CEX·Aster 모두 개선(가중 -3.187%→-2.071%, Aster -1.919%→-1.613%; 단
OrangeX는 확인 복귀 결과 직전 carry -1.163%→-1.97%로 소폭 재악화해 완전 수렴은
아님). 1000RATS는 CEX·Aster 모두 재악화(가중 -9.940%→-11.964%, Aster
-7.908%→-11.13%).

### AIO·HYPE — 간결 현황

- **AIO**: ⚠️ 직전 개선이 재차 반전, CEX·Aster 모두 재악화(가중 -3.728%→-7.029%).
- **HYPE**: ⚠️ 여러 회차 개선추세가 소폭 반전, 마이너스 폭 재확대(-0.938%→-1.207%).

### ⚠️⚠️ OKX 직접조회 funding 재검증 — MMT·PIPPIN 이탈폭 계속 확대

GIGGLE·GRAM은 이번 회차도 raw `fundingRate`가 정확히 `0.00005`로 완전 동일
(GIGGLE 39회차·GRAM 37회차 연속). **MMT**는 raw `-0.0001263451147510`→
**`-0.0003836247926697`**로 그룹값에서의 이탈이 매 회차 더 음의 방향으로 심화되는
추세(0.00005→약-0.0000988(추정)→-0.0001263→-0.0003836)다. **PIPPIN**은
`0.0003111073184247`→**`0.0003357811391581`**로 그룹값 대비 이탈폭이 **약 6.2배→
약 6.7배**로 더 확대됐다. KAITO는 raw `-0.0022553535009234`로 애초부터 별개
스케일이며 최근 3회차 연속 완화 추세다.

## 이번 회차 그 외 관찰

- **BSB**: OKX -5.256%→-5.053%(소폭 개선), Aster -5.354%→-4.911%(개선), OrangeX
  (확인 복귀) 직전 carry -4.909%→-4.912%로 거의 일치.
- **AKE·ADA·ASTER·ATOM**: 큰 변화 없이 기존 방향 유지 또는 소폭 등락.
- **dYdX(ETH·BTC·SOL)**: 이번 회차 확인 복귀, 직전 carry값 대비 방향상 큰 괴리 없이
  소폭 등락(ETH +0.416%→+0.496%, BTC -0.421%→-0.292%, SOL +0.539%→+0.618%).

## 데이터 이슈 추적 결과

이번 회차 **binance_futures·bybit·okex_swap·hyperliquid·aster·OKX직접API(5종)**에
더해 **직전 회차 실패했던 orangex_futures·dydx_chain 2종이 1차 시도부터 정상
확보**됐다. **CoinGecko `/global`만 3회 재시도 전부 429**로 미확인 처리했다. 이는
직전 회차(orangex_futures·dydx_chain·`/global`이 429)와 실패군이 재차 뒤바뀐 것으로,
특정 엔드포인트가 구조적으로 막힌 것이 아니라 회차마다 레이트리밋 대상이 순환하는
양상이 계속 확인된다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️ 전소스 급반등, 언락 5.9일] | Binance+Bybit(가중평균) | $17.80M | $8.00M | -0.015 | -11.594% | 전 소스 동시 큰 폭 반등, OI 감소 — 숏커버링 정황 | rebounds-sharply-all-sources-oi-declines-unlock-6d |
| **BANK** [⚠️⚠️ 재악화 확대, 언락 4.9일] | Binance+Bybit(가중평균) | $54.03M | $16.28M | -0.041 | -8.536% | 재악화 더 확대, OrangeX 확인시 OI는 오히려 감소 | worsens-further-oi-declines-unlock-5d |
| **KAITO** [⚠️⚠️ 반등 되돌림, OI 계속증가, 언락 8.4일] | OKX(직접API) | $68.27M | $8.13M | -0.226 | -4.776% | 반등이 일부 되돌려짐, OI는 여전히 양쪽 증가 | rebound-partially-reverses-oi-still-rising-unlock-8d |
| **AEON** [⚠️⚠️ 강한 플러스 전환] | OKX(CoinGecko정상, okex_swap) | $6.57M | $3.43M | +0.005 | +8.504% | 전 소스 강한 랠리, Aster·OrangeX 마이너스→플러스 | rallies-strongly-all-sources-flip-positive |
| **AAVE** [⚠️ 플러스 전환] | Binance+Bybit(가중평균) | $59.90M | $88.58M | +0.01 | +0.329% | CEX·Aster·HL 3소스 동시 플러스 전환 | flips-positive-all-sources |
| **CAP** [재상승 확대] | OKX(CoinGecko정상, okex_swap) | $180.37M | $7.44M | -0.039 | +26.641% | 전 소스 강한 상승 지속 | rallies-further-all-sources |
| **BEAT** [강한 회복 지속] | OKX(CoinGecko정상, okex_swap) | $535.48M | $9.46M | +0.005 | -20.843% | 3소스 모두 낙폭 대폭 축소 | recovers-strongly-further |
| **BICO** [⚠️ 4회차 연속 재악화] | OKX(CoinGecko정상, okex_swap) | $107.98M | $6.19M | +0.001 | -8.931% | 재악화 방향 굳어짐, OrangeX도 대폭 악화 | worsens-further-4th-round |
| **ALGO** [⚠️ 밴드 이탈, 뚜렷 개선] | Binance+Bybit(가중평균) | $17.02M | $15.54M | -0.020 | -0.576% | 좁은 밴드 여러회차만에 이탈, 3소스 개선 | breaks-tight-band-improves |
| **MMT** [⚠️⚠️ funding 이탈폭 확대] | OKX(직접API) | $19.20M | $3.13M | -0.038 | -1.887% | funding 그룹이탈이 매회차 더 심화 | funding-diverges-further-from-group |
| **AIO** [⚠️ 재악화 반전] | Binance+Bybit(가중평균) | $7.68M | $4.17M | +0.005 | -7.029% | 직전 개선이 재차 반전, CEX·Aster 동반 악화 | reverses-worsens-again |
| **1000RATS** [⚠️ 소스수렴, 동반악화] | Binance+Bybit(가중평균) | $9.96M | $15.10M | +0.041 | -11.964% | CEX·Aster 모두 재악화로 엇갈림 해소 | worsens-both-sources-converge |
| **ALLO** [소스 대부분 수렴, 개선] | Binance+Bybit(가중평균) | $13.00M | $17.17M | -0.005 | -2.071% | CEX·Aster 개선, OrangeX만 소폭 재악화 | improves-cex-aster-orangex-lags |
| GRAM [거의 유지] | OKX(직접API) | $2.76M | $6.28M | +0.005 | +0.526% | 플러스권 거의 유지, funding 그룹값 유지 | roughly-flat-near-1pct |
| GIGGLE [둔화] | OKX(직접API) | $104.40M | $2.10M | +0.005 | +7.653% | 플러스 유지, 둔화. funding 이상치 39회차 | decelerates-still-positive-anomaly-39th |
| PIPPIN [⚠️ funding 이탈 확대] | OKX(직접API) | $8.42M | $1.69M | +0.034 | -4.022% | funding 그룹값 대비 약 6.7배로 확대 | funding-diverges-further-again |
| BSB [소폭 개선] | OKX(okex_swap) | $2.90M | $2.31M | +0.006 | -5.053% | OrangeX 확인복귀, 3소스 거의 일치 | improves-slightly-all-sources |
| AKE [보합] | Binance+Bybit(가중평균) | $49.45M | $39.05M | +0.006 | +8.141% | 상승폭 거의 유지 | holds-steady-positive |
| ADA [개선추세 유지] | Binance+Bybit(가중평균) | $178.14M | $156.38M | +0.01 | -1.817% | 소폭 등락 속 개선추세 유지 | improves-further-post-band-break |
| ASTER [확대 지속] | Binance+Bybit(가중평균) | $15.88M | $112.68M | +0.004 | +0.810% | 플러스 확대 지속 | extends-positive-steady |
| ATOM [고점권 유지] | Binance+Bybit(가중평균) | $17.38M | $29.54M | +0.004 | +2.635% | 고점권에서 유지 | pulls-back-slightly-from-highs |
| CORE [소폭 재악화] | OKX(CoinGecko정상, okex_swap) | $1.21M | $0.88M | +0.007 | -0.956% | 저유동성, 소폭 추가 재악화 | slight-worsen |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함). 이번 회차 **orangex_futures·
> dydx_chain 모두 확인 복귀**했다(표에 명시).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [⚠️⚠️ 큰 폭 반등] | Hyperliquid | $0.69M | $1.10M | -0.011 | -11.34% | 숏커버링 정황, OI 보합. 언락 5.9일 | rebounds-sharply-all-sources-oi-flat-unlock-6d |
| **ACE-USDT-PERPETUAL** [확인복귀, 개선+OI감소] | OrangeX | $11.62M | $3.95M | +0.01 | -11.092% | OI -17.6% 감소 — 숏커버링 정황 | confirmed-returns-rebounds-oi-declines |
| ACE-USDT [큰 폭 반등] | Aster | $0.17M | $0.02M | -0.003 | -11.36% | 전소스 동반 반등 | rebounds-sharply-all-sources-oi-flat-unlock-6d |
| **BANK-USDT** [⚠️⚠️ 재악화] | Aster | $0.09M | $0.25M | -0.015 | -9.626% | 재악화 확대 | worsens-further-oi-declines-unlock-5d |
| **BANK-USDT-PERPETUAL** [확인복귀, 재악화+OI감소] | OrangeX | $4.55M | $1.51M | -0.015 | -8.962% | OI 오히려 -5.9% 감소('+13%증가' 서술 정정) | confirmed-returns-worsens-oi-declines |
| **KAITO-USD** [⚠️⚠️ 반등 되돌림, OI+1.5%] | Hyperliquid | $16.09M | $12.78M | -0.259 | -4.44% | 가격 재하락, OI는 계속 증가. 언락 8.4일 | rebound-partially-reverses-oi-still-rising-unlock-8d |
| BICO-USDT-PERPETUAL [확인복귀, 대폭악화] | OrangeX | $53.65M | $18.63M | -0.029 | -11.429% | 4회차 연속 재악화에 동참 | confirmed-returns-worsens-further |
| BICO-USDT [4회차 재악화] | Aster | $0.52M | $0.13M | +0.004 | -10.991% | 재악화 지속 | worsens-further-4th-round |
| **CASHCAT** [⚠️⚠️ 3소스 최초 동시 수렴] | Hyperliquid | $8.49M | $21.74M | +0.001 | +2.653% | HL·Aster·OrangeX 모두 플러스 전환 | converges-positive-all-three-sources |
| CASHCAT-USDT-PERPETUAL [확인복귀, 플러스전환] | OrangeX | $0.17M | $0.05M | +0.01 | +1.016% | 3소스 수렴 동참 | converges-positive-all-three-sources |
| CASHCAT-USDT [플러스 반전] | Aster | $0.91M | $1.39M | +0.004 | +2.264% | 3소스 수렴 동참 | converges-positive-all-three-sources |
| HYPE-USD [⚠️ 소폭 반전] | Hyperliquid | $125.44M | $1,175.09M | +0.001 | -1.207% | 개선추세 반전, 마이너스 재확대 | reverses-slightly-negative-widens |
| AEON-USDT-PERPETUAL [확인복귀, 강한랠리] | OrangeX | $0.43M | $0.15M | +0.01 | +7.726% | 마이너스→강한플러스 전환 | rallies-strongly-all-sources-flip-positive |
| AEON-USDT [강한랠리] | Aster | $0.03M | $0.22M | +0.005 | +7.464% | 마이너스→강한플러스 전환 | rallies-strongly-all-sources-flip-positive |
| BLESS [확인복귀, 재악화] | OrangeX | $45.23M | $16.51M | +0.01 | -10.926% | 재악화 확인(직전carry대비 대폭 악화) | confirmed-returns-worsens |
| BLESS-USDT [재악화] | Aster | $0.12M | $0.20M | +0.009 | -8.796% | 재악화 지속 | worsens |
| GRAM-USD [거의 유지] | Hyperliquid | $1.27M | $13.48M | +0.001 | +0.405% | 플러스권 거의 유지 | roughly-flat-near-1pct |
| BTW [상승폭 확대] | Aster | $1.09M | $14.78M | +0.008 | +8.757% | 상승폭 추가 확대 | rebounds-notably |
| ANSEM [⚠️ 마이너스 전환] | Aster | $0.43M | $1.07M | +0.001 | -7.239% | 플러스에서 마이너스로 반전 | flips-negative |
| ANSEM-USDT-PERPETUAL [확인복귀, 마이너스전환] | OrangeX | $0.53M | $0.18M | +0.01 | -4.241% | 마이너스 전환 | flips-negative |
| HYNA:PUMP-USD [재조회없음] | Hyperliquid | $0.07M | $0.19M | +0.004 | -0.835% | 직전값 유지 | small-fluctuation-continues |
| HYNA:HYPE-USD [재조회없음] | Hyperliquid | $0.13M | $0.89M | +0.001 | -0.988% | 직전값 유지 | small-fluctuation-continues |
| BSB-USDT-PERPETUAL [확인복귀, carry와 일치] | OrangeX | $5.86M | $2.00M | +0.01 | -4.912% | carry값과 거의 일치 | confirmed-returns-matches-prior |
| BSB-USDT [소폭 개선] | Aster | $0.01M | $0.11M | +0.001 | -4.911% | 소폭 개선 | improves-slightly-all-sources |
| 1000RATS-USDT [CEX와 동반악화] | Aster | $0.04M | $0.02M | +0.018 | -11.13% | 엇갈림 해소, 동반 재악화 | worsens-both-sources-converge |
| AIO-USDT [재악화 반전] | Aster | $0.11M | $0.10M | +0.005 | -6.619% | 재악화 반전 | reverses-worsens-again |
| AAVE-USDT-PERPETUAL [확인복귀, 플러스전환] | OrangeX | $33.97M | $12.80M | +0.01 | +0.28% | 플러스 전환 | flips-positive-all-sources |
| AAVE-USDT [플러스 전환] | Aster | $0.27M | $4.45M | +0.01 | +0.101% | 플러스 전환 | flips-positive-all-sources |
| AAVE-USD [플러스 전환] | Hyperliquid | $5.04M | $59.82M | +0.001 | +0.421% | 플러스 전환 | flips-positive-all-sources |
| ADA-USDT-PERPETUAL [확인복귀, 개선확인] | OrangeX | $90.25M | $30.99M | +0.002 | -1.578% | 개선 지속 확인 | improves-further-post-band-break |
| ADA-USDT [소폭 등락] | Aster | $0.54M | $1.62M | +0.01 | -2.093% | 소폭 등락 | improves-further-post-band-break |
| ADA-USD [개선 지속] | Hyperliquid | $4.22M | $31.22M | +0.0 | -1.654% | 개선 지속 | improves-further-post-band-break |
| AKE-USDT-PERPETUAL [확인복귀, 소폭상승] | OrangeX | $6.49M | $2.33M | +0.01 | +8.856% | 소폭 추가 상승 | holds-steady-positive |
| AKE-USDT [보합] | Aster | $0.65M | $11.06M | +0.006 | +7.501% | 보합 | holds-steady-positive |
| ALGO-USDT-PERPETUAL [확인복귀, 뚜렷개선] | OrangeX | $8.66M | $2.80M | -0.01 | -0.858% | 뚜렷 개선 | breaks-tight-band-improves |
| ALGO-USDT [밴드 이탈] | Aster | $0.03M | $0.02M | -0.002 | -0.502% | 밴드 이탈, 뚜렷 개선 | breaks-tight-band-improves |
| ALGO-USD [밴드 이탈] | Hyperliquid | $0.79M | $2.17M | +0.001 | -0.263% | 밴드 이탈, 뚜렷 개선 | breaks-tight-band-improves |
| ATOM-USDT-PERPETUAL [확인복귀, 유지] | OrangeX | $9.99M | $3.64M | +0.01 | +2.782% | 유지 | pulls-back-slightly-from-highs |
| ATOM-USDT [유지] | Aster | $0.01M | $1.67M | +0.01 | +3.237% | 유지 | pulls-back-slightly-from-highs |
| ATOM-USD [유지] | Hyperliquid | $0.32M | $1.90M | +0.001 | +2.637% | 유지 | pulls-back-slightly-from-highs |
| ASTER-USDT-PERPETUAL [확인복귀, 확대지속] | OrangeX | $6.95M | $2.40M | +0.01 | +0.845% | 확대 지속 | extends-positive-steady |
| ASTER-USDT [대형 OI] | Aster | $9.42M | $221.13M | +0.009 | +0.845% | 확대 지속 | extends-positive-steady |
| ASTER-USD [확대 지속] | Hyperliquid | $0.85M | $14.86M | +0.001 | +0.898% | 확대 지속 | extends-positive-steady |
| ALLO-USDT [CEX와 동반 개선] | Aster | $0.06M | $0.03M | -0.004 | -1.613% | CEX와 동반 개선 | improves-cex-aster-orangex-lags |
| ALLO-USDT-PERPETUAL [확인복귀, 소폭재악화] | OrangeX | $9.29M | $3.43M | +0.01 | -1.97% | CEX·Aster와 달리 소폭 재악화 | improves-cex-aster-orangex-lags |
| HYPER-USD [소폭 개선] | Hyperliquid | $0.15M | $0.31M | +0.001 | -3.861% | 소폭 개선 | improves-slightly |
| APEX-USD [거의 flat] | Hyperliquid | $0.13M | $0.64M | +0.001 | -0.404% | 거의 flat 유지 | roughly-flat |
| FARTCOIN [flat 근접] | Hyperliquid | $7.99M | $23.59M | +0.001 | -0.24% | 소폭 마이너스 전환 | pulls-back-near-flat |
| ETHFI-USD [마이너스 확대] | Hyperliquid | $0.78M | $8.44M | +0.001 | -2.434% | 마이너스 폭 추가 확대 | worsens-further-negative |
| ETH-USD [확인복귀] | dYdX | $11.92M | $19.56M | 0.0 | +0.496% | dYdX 확인 복귀, 소폭 등락 | confirmed-returns |
| BTC-USD [확인복귀] | dYdX | $3.34M | $17.74M | 0.0 | -0.292% | dYdX 확인 복귀, 소폭 등락 | confirmed-returns |
| SOL-USD [확인복귀] | dYdX | $0.96M | $4.52M | 0.0 | +0.618% | dYdX 확인 복귀, 소폭 등락 | confirmed-returns |

## 테마 태그

1. **⚠️⚠️ ACE: 8/18 언락 약 5.9일 앞두고 전 소스 동시 큰 폭 반등, OI도 감소 — 숏커버링 정황** (ace-rebounds-sharply-oi-declines-unlock-6d).
2. **⚠️⚠️ BANK: 8/17 언락 약 4.9일 앞두고 재악화 더 확대, OrangeX 확인시 OI가 오히려 감소해 '+13%증가' 서술 정정** (bank-worsens-oi-declines-unlock-5d).
3. **⚠️⚠️ KAITO: 8/20 언락 약 8.4일 앞두고 반등 일부 되돌림, OI는 여전히 양쪽 계속 증가** (kaito-rebound-reverses-oi-still-rising-unlock-8d).
4. **⚠️⚠️ CASHCAT: HL·Aster·OrangeX 3소스 처음으로 동시 플러스 수렴** (cashcat-converges-positive-all-sources).
5. **⚠️ BICO: 4회차 연속 재악화, OrangeX 확인복귀도 대폭 악화** (bico-worsens-4th-round).
6. **CAP: 재상승 확대 지속, 전 소스 강한 상승** (cap-rallies-further-all-sources).
7. **BEAT: 낙폭 대폭 추가 축소, 3소스 모두 강한 회복** (beat-recovers-strongly-further).
8. **⚠️⚠️ AEON: 전 소스 강한 플러스 전환, Aster·OrangeX 마이너스→강한플러스** (aeon-rallies-strongly-flip-positive).
9. **⚠️ AAVE: CEX·Aster·HL 3소스 전부 플러스로 전환** (aave-flips-positive-all-sources).
10. **⚠️ ALGO: 좁은 밴드 이탈, 3소스 모두 뚜렷 개선** (algo-breaks-tight-band-improves).
11. **ALLO·1000RATS: 소스 간 엇갈림 대부분 해소(ALLO 개선쪽 수렴, 1000RATS 악화쪽 수렴)** (allo-1000rats-mostly-converge).
12. **⚠️ AIO: 직전 개선이 재차 반전, CEX·Aster 동반 재악화** (aio-reverses-worsens-again).
13. **⚠️ HYPE: 개선추세 소폭 반전, 마이너스 폭 재확대** (hype-reverses-slightly).
14. **⚠️⚠️ OKX 직접조회 funding: MMT·PIPPIN 그룹이탈폭 계속 확대(MMT raw -0.0001263→-0.0003836), GIGGLE·GRAM은 0.00005 동일값 지속(39·37회차)** (okx-funding-mmt-pippin-diverge-further).
15. **데이터: 이번 회차 orangex_futures·dydx_chain 모두 1차 시도부터 정상 확보, `/global`만 3회 재시도 전부 429로 미확인** (data-orangex-dydx-return-global-still-fails).
16. **총시총·BTC도미넌스는 `/global` 미확인으로 직전 회차 값 유지, 갱신 없음** (global-metrics-unconfirmed-carried-forward).
17. **Fear&Greed 이번 회차도 미재조회** (fear-greed-not-rechecked).
18. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
19. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
20. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
21. **TUT: 이번 회차도 재확인 생략** (tut-status-unconfirmed-no-further-check).

## 데이터 신뢰도

이번 회차 **binance_futures·bybit·okex_swap·hyperliquid·aster와 OKX 직접API
(KAITO·GIGGLE·MMT·PIPPIN·GRAM)에 더해 orangex_futures·dydx_chain 2종까지 전부 1차
시도부터 정상 확보**됐다. **CoinGecko `/global`만 3회 재시도 전부 429**로 미확인
처리하고 직전 회차 값을 carry-forward했다. 이는 직전 회차(orangex_futures·
dydx_chain·`/global`이 429)와 실패군이 재차 뒤바뀐 것으로, 특정 엔드포인트가
구조적으로 차단된 게 아니라 회차마다 레이트리밋 대상이 순환하는 양상이 계속
확인된다.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: ticker·open-interest·funding-rate
개별 엔드포인트 전부 1차 시도부터 정상. GIGGLE·GRAM은 raw `fundingRate`가 여전히
정확히 `0.00005`로 동일(39·37회차 연속). MMT·PIPPIN은 그룹값에서의 이탈폭이 매
회차 더 확대되는 추세다. KAITO는 별개 스케일이나 최근 3회차 연속 완화 중이다.

**Hyperliquid**: 정상 확보 — ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·ALGO·GRAM·HYPE·
HYPER·APEX·FARTCOIN·ETHFI 확보(raw 정밀값). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·
BTW·BLESS·ANSEM·TUT는 HL 미상장(기존과 동일).

**Aster**: 정상 확보 — BANK·AAVE·ADA·BICO·BEAT·BSB·AKE·ATOM·ALLO·1000RATS·AIO·
AEON·ASTER·CAP·ALGO·ACE·CASHCAT·BTW·ANSEM·BLESS 전량 확보(raw 정밀값). KAITO-USDT는
이번 회차도 응답에서 재확인되지 않았다. MMT·GIGGLE·PIPPIN·GRAM·CORE·TUT는 Aster에서
여전히 미발견.

**OrangeX**: ⚠️ **이번 회차 1차 시도부터 정상 확보로 복귀**했다(직전 회차 4회 재시도
전부 429였던 것과 대비). ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·
AKE·CAP·BLESS·CASHCAT·BSB·ANSEM 전량 실측 확인했다. KAITO·1000RATS·GRAM·MMT·PIPPIN·
GIGGLE·CORE·BTW는 OrangeX에서 원래부터 미발견이었다.

**binance_futures**: 1차 시도부터 정상 확보 — ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·
ALLO·1000RATS·ATOM·AIO 확보. BICO는 이번 회차도 Binance에서 미발견.

**bybit**: 1차 시도부터 정상 확보 — ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·ALLO·1000RATS·
ATOM·AIO 확보, Binance+Bybit 가중평균으로 반영.

**dYdX(`dydx_chain`)**: ⚠️ **이번 회차 1차 시도부터 정상 확보로 복귀**했다(직전 회차
4회 재시도 전부 429였던 것과 대비) — BTC-USD·ETH-USD·SOL-USD 전부 실측 확인.

**CoinGecko `/global`**: ⚠️ 1차~3차 시도 전부 429로 확보 실패 — 총시총·BTC도미넌스
모두 직전 회차 값을 유지했다.

**Fear&Greed**: 이번 회차도 재조회하지 않음(최우선 추적과제에 시간 집중).

**신규 발견**: (a) ACE가 언락 임박 3종 중 처음으로 4개 소스(CEX·HL·Aster·OrangeX)
동시에 큰 폭(약 -11~12%대로 수렴)으로 반등했고 OI도 함께 감소해, 순수 매도압력이
아니라 숏 커버링 성격에 부합하는 정황이 처음 관측됐다. (b) BANK는 반대로 OrangeX가
확인 복귀하면서 '+13% 증가' 서술이 실측 결과 정정됐다 — carry-forward 추정치가
실제 방향과 다를 수 있음을 보여준 사례. (c) KAITO는 반등이 이번 회차 일부
되돌려졌으나 OI는 계속 증가해, 가격 방향과 무관하게 OI가 꾸준히 늘어나는 패턴이
재확인됐다(2회 연속). (d) CASHCAT은 여러 회차 이어지던 3소스 분열이 이번 회차
처음으로 완전히 해소돼 모두 플러스로 수렴했다. (e) 이번 회차 orangex_futures·
dydx_chain 429 실패군이 완전히 해소되고 대신 `/global`만 남아, 레이트리밋 순환
양상이 계속 관측된다.

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
확인함); (j) OKX 직접조회 GIGGLE·GRAM의 funding이 이번 회차도 동일값(0.00005)으로
관측된 원인, MMT·PIPPIN 이탈폭이 왜 매 회차 더 확대되는지는 규명하지 못했다; (k)
dYdX exchange id는 `dydx_chain`을 사용하며 이번 회차 확인 복귀했다; (l) HL에서
canonical SOL-USD는 이번 회차 재확인하지 않았다; (m) KAITO-USDT(Aster)는 이번
회차도 응답에서 확인되지 않았다; (n) HYNA:PUMP-USD·HYNA:HYPE-USD는 HL 응답이
"Multiple pairs"로 모호하게 반환돼 이번 회차 재조회를 생략하고 직전값을 유지했다;
(o) ALLO의 OrangeX 확인복귀 결과가 CEX·Aster와 방향이 어긋난 원인은 아직 확인하지
못했다; (p) `/global`이 3회 재시도에도 복구되지 않은 원인(구조적 차단인지 일시적
과부하인지)은 규명하지 못했으며, 실패 대상이 회차마다 바뀌는 양상이 우연인지 서버
측 정책 변화인지도 다음 회차 이후 계속 추적이 필요하다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
