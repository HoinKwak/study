# 선물시장 스카우트 브리핑 — 2026-08-11 20:30 UTC (KST 2026-08-12 05:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-11T18:29:00Z)
> 로부터 2.0시간 경과.**

## 이번 회차 핵심 요약 — 데이터 전량 복구, BICO 수렴선언 반박, AEON 최대 반전

이번 회차는 okex_swap·hyperliquid·aster·orangex_futures(3회 재시도 끝 복구)·binance_futures와
OKX직접API(KAITO·GIGGLE·MMT·PIPPIN·GRAM) 전부 정상 확보됐고, **지난 2회차 연속 재실패했던
bybit·dydx_chain·CoinGecko `/global` 3종도 이번 회차 4회 시도 끝에 전량 복구**됐다(재시도 상한
3~4회 준수). 총시총 **$2,266,300,785,441.92**(약 $2.2663T, 직전 참고치 $2.2617T 대비 소폭 증가),
BTC도미넌스 **56.30%**(직전 참고치 56.415% 대비 소폭 하락 — 알트 상대강도 미세 개선). bybit
복구로 ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·ALLO·1000RATS·ATOM 10종은 Binance+Bybit
가중평균으로 정상 복원됐다. dYdX(ETH/BTC/SOL)도 전부 재확인돼 3종목 모두 낙폭이 완화됐고
ETH는 플러스로 전환됐다.

## 최우선 추적과제 결과

### ⚠️⚠️ OKX 직접조회 funding 재검증 — 4종 완전동일 패턴에서 PIPPIN 이탈

`/public/funding-rate` 엔드포인트를 4종목 개별 직접 조회한 결과, **GIGGLE·MMT·GRAM 3종은
raw `fundingRate`가 이번 회차도 정확히 `0.00005`로 완전 동일**(표시값 각 0.005)해 이상치가
지속됐다. 반면 **PIPPIN은 이번 회차 처음으로 미세하게 다른 값**(`0.0000545074141550`,
×100 환산 약 0.0055)을 보여 '4종 완전동일' 패턴에서 벗어났다. KAITO는 애초부터 뚜렷이 다른
스케일(raw `-0.0021358570958507`, ×100 환산 약 -0.214)이라 이 이상치 그룹과 무관하다.
`nextFundingRate`는 5종목 전부 매 조회 시 빈 문자열로 확인돼 다음 정산 시각 전 미공표 상태로
추정된다. 결론: **동일값 재현은 3/4만 유지**됐고, 완전 동일 4종 패턴 자체는 이번 회차 깨졌다.

### ⚠️⚠️ CASHCAT — 하락 추세화 서술이 이번 회차 방향 분열

HL **-4.484%→-5.89%**(추가 심화)이나, OrangeX **-5.519%→-5.206%**(개선), Aster
**-6.993%→-4.124%**(뚜렷 개선)로 3소스 중 2곳이 반전 개선했다. 지난 회차 '급반전이 추세로
굳어짐' 서술이 이번엔 흔들려, 온체인 약세와의 동조 여부는 다음 회차에서 재확인이 필요하다.

### BICO — 개선 아님, 오히려 뚜렷 반전 재악화

직전 회차의 '3소스 완전 수렴' 선언이 이번 회차 즉시 반박됐다. OKX **-5.645%→-8.233%**,
OrangeX **-6.235%→-6.444%**, Aster **-7.085%→-7.696%**로 3소스 전부 재차 마이너스 폭이
확대돼 4회차 연속 개선 스트릭이 완전히 끊겼다. 펀딩은 아직 극단으로 재발산하지 않았으나,
'완결' 판정이 성급했음을 보여준다.

### BANK — 4소스 전부 약세 확대는 아님, -5.4~5.7%대 정체

가중평균(Binance+Bybit 복원) **-5.585%**로 직전 Binance단독 -6.006% 대비 개선처럼 보이나
이는 bybit 재편입에 따른 방법론 효과일 수 있다. OrangeX **-5.382%→-5.409%**(거의 유지),
Aster **-5.41%→-5.708%**(소폭 재악화)로 실질 약세는 -5.4~-5.7%대에서 정체 중이다.
8/17 언락 약 5.1일 앞.

### ACE — '4소스 전부 개선' 이후 정체를 지나 이번엔 '전 소스 동조 재악화'

Binance+Bybit 가중평균 **-8.837%→-9.719%**, OrangeX **-8.434%→-9.593%**, Aster
**-9.407%→-9.662%**, 지난 회차 유일 개선원이던 HL도 **-8.211%→-9.455%**로 4소스 전부
약세가 확대됐다. 지난 회차 '혼조'가 이번엔 명확한 전면 재악화로 굳어졌다. 8/18 언락
약 6.1일 앞.

### AKE — 급등 이후 고점권 다지기, 되돌려지지 않음

가중평균 **+11.453%→+12.230%**, OrangeX **+12.369%→+12.501%**(거의 유지), Aster
**+12.732%→+11.351%**(소폭 되돌림)로 급등이 되돌려지진 않고 높은 수준에서 consolidating.

### CAP — 재가속 3회차 연속

OKX **+20.277%→+23.491%**, OrangeX **+19.576%→+24.51%**, Aster **+21.355%→+24.96%**로
전 소스가 다시 강하게 상승했다.

### HYPE — 마이너스 반전 4회차, 낙폭 추가 확대

HL **-1.706%→-2.062%**로 낙폭이 계속 커지고 있으며 반등 기미가 여전히 없다.

### KAITO — 8/20 언락 앞두고 재악화 뚜렷 가속

OKX 직접 **-1.683%→-5.246%**, HL **-2.609%→-4.957%**로 낙폭이 크게 확대됐다. 펀딩도
OKX raw `-0.0021358570958507`(×100 환산 약 -0.214, 직전 -0.1548)로 재차 마이너스 심화.
Aster는 이번 회차도 KAITO-USDT가 응답에서 발견되지 않아 **4회차 연속** 3-way 크로스
단절이 이어진다. 8/20 언락 약 8.1일 앞.

## 이번 회차 추가 관찰

- **⚠️⚠️ AEON**: OKX **-5.156%→+0.358%**, OrangeX **-4.306%→+0.944%**로 뚜렷하게 플러스
  전환됐고, Aster만 **-4.555%→-2.156%**로 마이너스를 유지한 채 개선됐다 — 3소스 중 2곳이
  방향 자체를 바꾼 이번 회차 최대 반전 사례.
- **⚠️ BLESS**: 지난 회차 플러스 전환이 이번 회차 완전히 되감겨 OrangeX **+0.998%→-7.459%**,
  Aster **-1.16%→-7.704%**로 재차 마이너스가 크게 확대됐다.
- **BEAT**: 개선 4회차 연속. OKX **-46.748%→-37.36%**, OrangeX **-45.602%→-34.325%**,
  Aster **-46.219%→-37.952%**.
- **BSB**: OKX **-5.969%→-5.046%**, OrangeX **-5.977%→-5.038%**, Aster **-6.62%→-4.124%**로
  -4~5%대로 추가 수렴.
- **MMT**: OKX 직접조회 **-4.151%→-2.141%**로 낙폭 지속 완화(방향 유지, 재반전 아님).
- **GIGGLE**: **+15.885%→+16.486%**로 추가 확대(필드 이상치 36회차 연속).
- **GRAM**: **+0.151%→+0.833%**로 플러스권에서 소폭 확대.
- **ATOM**: 재가열 반전 이후 소폭 되돌림을 보이며 +1.9~2.7% 구간에서 안정화.
- **AAVE·ASTER·ALLO**: 전 소스에서 뚜렷한 개선(AAVE -1.5~1.7%대 진입, ASTER 플러스 전환,
  ALLO -4.1~4.8%대로 개선).
- **ALGO**: 소스 간 방향이 갈렸다(OrangeX·HL 개선, Aster는 -3.171%로 뚜렷 악화).
- **ADA**: 16회차째 -4.1~4.2% 좁은 밴드에 사실상 고정.
- **AIO**: Binance 재조회 결과 **-6.15%→-5.414%** 개선, Aster는 **-3.547%→-4.868%**로
  소폭 재악화해 소스 간 방향이 갈렸다.
- **dYdX(ETH·BTC·SOL)**: 전량 복구. ETH funding 0.0·chg **-0.976%→+0.155%**(플러스 전환),
  BTC **-1.035%→-0.71%**, SOL **-1.345%→-0.511%**로 전부 낙폭 완화.

## 데이터 이슈 추적 결과

**bybit·dydx_chain·CoinGecko `/global` 3종이 지난 2회차 연속 재실패 이후 이번 회차 4회
시도 끝에 전량 복구**됐다(3~4회 재시도 상한 준수). orangex_futures도 2회 실패 후 3회차
시도에서 복구됐다. bybit 복구로 ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·ALLO·1000RATS·ATOM
10종이 Binance+Bybit 가중평균으로 정상 복원됐다(직전 회차는 Binance 단독값). **OKX 직접
API funding 재검증**: GIGGLE·MMT·GRAM은 raw `fundingRate` 0.00005 완전동일값 지속, PIPPIN은
이번 회차 처음 미세하게 다른 값(0.0000545074141550)으로 이탈, KAITO는 별개 스케일(진짜
시장값으로 추정). GIGGLE·KAITO(OKX직접) vol24h/volCcy24h 필드 이상치는 **36회차 연속**,
GRAM은 **34회차 연속**, MMT·PIPPIN의 10배 비율은 **20회차 연속** 재현됐다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BICO** [⚠️⚠️ 수렴선언 반박, 재악화] | OKX(CoinGecko정상, okex_swap) | $121.41M | $6.75M | +0.01 | -8.233% | 3소스 전부 재차 마이너스 확대, 4회차 개선 스트릭 종료 | reverses-worsens-after-convergence-claim |
| **CAP** [⚠️⚠️ 재가속 3회차] | OKX(CoinGecko정상, okex_swap) | $153.13M | $6.39M | -0.007 | +23.491% | 3소스 전부 추가 재상승 | reaccelerates-further-all-sources |
| **BEAT** [개선 4회차 연속] | OKX(CoinGecko정상, okex_swap) | $543.81M | $9.26M | +0.005 | -37.36% | 전 소스 뚜렷 개선 | improves-4th-round-consecutive |
| **ACE** [⚠️⚠️ 전 소스 동조 재악화] | Binance+Bybit(가중평균, 복원) | $23.83M | $8.14M | -0.008 | -9.719% | HL·OrangeX·Aster 전부 약세 확대. 8/18 언락 약 6.1일 앞 | worsens-uniformly-all-sources-unlock-6d |
| **BANK** [⚠️ -5.4~5.7%대 정체] | Binance+Bybit(가중평균, 복원) | $52.59M | $16.84M | +0.002 | -5.585% | OrangeX·Aster 실질 정체~소폭 재악화. 8/17 언락 약 5.1일 앞 | plateaus-mixed-weighted-recovery |
| **AKE** [고점권 다지기] | Binance+Bybit(가중평균, 복원) | $42.73M | $39.61M | +0.025 | +12.230% | 급등 되돌려지지 않고 consolidating | consolidates-near-highs-after-jump |
| **BSB** [4~5%대 추가 수렴] | OKX(CoinGecko정상, okex_swap) | $3.55M | $2.29M | +0.005 | -5.046% | 전 소스 소폭 개선 지속 | converges-narrower-4to5pct |
| **MMT** [낙폭 지속 완화] | OKX(직접API) | $19.04M | $3.26M | +0.005 | -2.141% | 재반전 아님, GIGGLE·GRAM과 funding 여전 동일 | improves-further-eases-more |
| **ADA** [16회차 밀집] | Binance+Bybit(가중평균, 복원) | $185.39M | $156.94M | +0.01 | -4.139% | 전 소스 -4.1~4.2%대 밀집 고정 | flat-tightly-clustered-16th-round |
| **KAITO** [⚠️⚠️ 재악화 가속] | OKX(직접API) | $63.85M | $7.82M | -0.214 | -5.246% | OKX·HL 동반 심화. Aster 크로스 4회차 소실. 8/20 언락 약 8.1일 앞 | worsens-further-accelerates-decline |
| **AIO** [Binance 개선, Aster 악화] | Binance(단독, 재조회) | $7.58M | $3.43M | +0.005 | -5.414% | 소스 간 방향 엇갈림 | mixed-binance-improves-aster-worsens |
| **GRAM** [플러스 확대] | OKX(직접API) | $2.89M | $6.37M | +0.005 | +0.833% | HL도 플러스 유지 | extends-positive-slightly-noisy |
| **GIGGLE** [추가 확대] | OKX(직접API) | $88.14M | $2.34M | +0.005 | +16.486% | 이상치 36회차 연속 | extends-further-anomaly-36th-round |
| **PIPPIN** [⚠️ funding 이탈] | OKX(직접API) | $9.27M | $1.68M | +0.0055 | -3.153% | funding raw값이 GIGGLE·MMT·GRAM(0.00005)과 처음 달라짐 | improves-further-funding-anomaly-breaks |
| ATOM [안정화] | Binance+Bybit(가중평균, 복원) | $17.52M | $29.42M | +0.002 | +1.907% | 재가열 반전 이후 소폭 되돌림 | stabilizes-after-reversal |
| AAVE [전 소스 뚜렷 개선] | Binance+Bybit(가중평균, 복원) | $57.25M | $87.96M | -0.004 | -1.628% | -1.5~1.7%대로 진입 | improves-notably-all-sources |
| ASTER [플러스 전환] | Binance+Bybit(가중평균, 복원) | $14.90M | $112.71M | +0.003 | +0.312% | 마이너스에서 플러스로 소폭 전환 | flips-slightly-positive |
| ALGO [소스 간 분열] | Binance+Bybit(가중평균, 복원) | $17.37M | $15.30M | +0.004 | -1.872% | OrangeX·HL 개선, Aster 뚜렷 악화 | mixed-diverges-across-sources |
| ALLO [뚜렷 개선] | Binance+Bybit(가중평균, 복원) | $14.54M | $17.21M | +0.005 | -4.094% | 마이너스 확대 스트릭 반전 개선 | improves-notably-reverses-negative-extension |
| 1000RATS [거의 유지] | Binance+Bybit(가중평균, 복원) | $10.14M | $15.74M | +0.045 | -10.046% | Aster도 거의 동일 수준 | roughly-flat |
| **AEON** [⚠️⚠️ 최대 반전, 플러스 전환] | OKX(CoinGecko정상, okex_swap) | $4.72M | $3.14M | +0.005 | +0.358% | OKX·OrangeX 마이너스→플러스 전환, Aster는 개선 | flips-positive-major-reversal-okx-orangex |
| CORE [저유동성, 소폭 재악화] | OKX(CoinGecko정상, okex_swap) | $1.26M | $0.88M | -0.021 | -3.253% | -3.012%→-3.253% | flat-low-liquidity-slight-worsen |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함). dYdX는 이번 회차 전량 복구됐다.

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BICO-USDT** [수렴선언 반박] | Aster | $0.53M | $0.13M | +0.005 | -7.696% | -7.085%→-7.696% | reverses-worsens-after-convergence-claim |
| **BICO-USDT-PERPETUAL** [수렴선언 반박] | OrangeX | $58.40M | $19.58M | -0.01 | -6.444% | -6.235%→-6.444% | reverses-worsens-after-convergence-claim |
| **CAP-USDT** [재가속] | Aster | $0.14M | $0.16M | 0.0 | +24.96% | +21.355%→+24.96% | reaccelerates-further-all-sources |
| **CAP-USDT-PERPETUAL** [재가속] | OrangeX | $0.75M | $0.27M | -0.01 | +24.51% | +19.576%→+24.51% | reaccelerates-further-all-sources |
| **CASHCAT** [⚠️ HL만 심화, 방향 분열] | Hyperliquid | $8.38M | $22.17M | +0.011 | -5.89% | -4.484%→-5.89% | diverges-mixed-signal |
| **CASHCAT-USDT-PERPETUAL** [개선] | OrangeX | $0.16M | $0.06M | -0.012 | -5.206% | -5.519%→-5.206% | diverges-mixed-signal |
| **CASHCAT-USDT** [뚜렷 개선] | Aster | $1.01M | $1.44M | +0.033 | -4.124% | -6.993%→-4.124% | diverges-mixed-signal |
| **BANK-USDT-PERPETUAL** [거의 유지] | OrangeX | $4.54M | $1.41M | +0.01 | -5.409% | -5.382%→-5.409% | plateaus-mixed-weighted-recovery |
| **BANK-USDT** [소폭 재악화] | Aster | $0.08M | $0.25M | +0.001 | -5.708% | -5.41%→-5.708% | plateaus-mixed-weighted-recovery |
| **ACE-USD** [유일 개선원도 재악화] | Hyperliquid | $0.94M | $1.12M | -0.006 | -9.455% | -8.211%→-9.455%. 8/18 언락 약 6.1일 앞 | worsens-uniformly-all-sources-unlock-6d |
| **ACE-USDT-PERPETUAL** [재악화] | OrangeX | $15.54M | $5.14M | -0.01 | -9.593% | -8.434%→-9.593% | worsens-uniformly-all-sources-unlock-6d |
| **ACE-USDT** [재악화] | Aster | $0.19M | $0.01M | -0.003 | -9.662% | -9.407%→-9.662% | worsens-uniformly-all-sources-unlock-6d |
| **BSB-USDT-PERPETUAL** [개선] | OrangeX | $7.17M | $2.56M | +0.01 | -5.038% | -5.977%→-5.038% | converges-narrower-4to5pct |
| **BSB-USDT** [뚜렷 개선] | Aster | $0.01M | $0.11M | +0.001 | -4.124% | -6.62%→-4.124% | converges-narrower-4to5pct |
| **AKE-USDT-PERPETUAL** [고점권 유지] | OrangeX | $6.05M | $2.27M | +0.023 | +12.501% | +12.369%→+12.501% | consolidates-near-highs-after-jump |
| **AKE-USDT** [소폭 되돌림] | Aster | $0.61M | $11.26M | +0.018 | +11.351% | +12.732%→+11.351% | consolidates-near-highs-after-jump |
| **KAITO-USD** [⚠️⚠️ 재악화 가속] | Hyperliquid | $14.42M | $11.51M | -0.148 | -4.957% | -2.609%→-4.957%. 8/20 언락 약 8.1일 앞 | worsens-further-accelerates-decline |
| **AIO-USDT** [소폭 재악화] | Aster | $0.13M | $0.10M | +0.005 | -4.868% | -3.547%→-4.868% | mixed-binance-improves-aster-worsens |
| **BLESS** [⚠️⚠️ 반전 완전 되감김] | OrangeX | $55.82M | $19.16M | +0.01 | -7.459% | +0.998%→-7.459% | flip-fully-unwound |
| **BLESS-USDT** [마이너스 확대] | Aster | $0.13M | $0.20M | +0.02 | -7.704% | -1.16%→-7.704% | flip-fully-unwound |
| **BEAT-USDT-PERPETUAL** [개선 4회차] | OrangeX | $4.41M | $1.28M | +0.033 | -34.325% | -45.602%→-34.325% | improves-4th-round-consecutive |
| **BEAT-USDT** [개선 4회차] | Aster | $26.89M | $3.05M | +0.025 | -37.952% | -46.219%→-37.952% | improves-4th-round-consecutive |
| **GRAM-USD** [플러스 확대] | Hyperliquid | $1.57M | $13.44M | +0.001 | +1.213% | -0.068%→+1.213% | extends-positive-slightly-noisy |
| **BTW** [소폭 둔화] | Aster | $1.14M | $14.19M | +0.014 | +3.4% | +4.851%→+3.4% | decelerates-slightly |
| **ANSEM** [뚜렷 둔화] | Aster | $0.50M | $1.13M | +0.001 | +5.712% | +11.668%→+5.712% | decelerates-notably |
| **ANSEM-USDT-PERPETUAL** [거의 유지] | OrangeX | $0.51M | $0.18M | +0.01 | +12.604% | +12.408%→+12.604% | roughly-flat |
| **HYPE-USD** [⚠️ 마이너스 4회차, 확대] | Hyperliquid | $128.69M | $1,172.04M | +0.001 | -2.062% | -1.706%→-2.062%, 반등 기미 없음 | negative-reversal-extends-4th-round |
| **HYNA:PUMP-USD** [재조회없음] | Hyperliquid | $0.07M | $0.19M | +0.004 | -0.835% | 직전값 유지 | small-fluctuation-continues |
| **HYNA:HYPE-USD** [재조회없음] | Hyperliquid | $0.13M | $0.89M | +0.001 | -0.988% | 직전값 유지 | small-fluctuation-continues |
| **AEON-USDT-PERPETUAL** [⚠️⚠️ 플러스 전환] | OrangeX | $0.43M | $0.15M | +0.01 | +0.944% | -4.306%→+0.944% | flips-positive-major-reversal-okx-orangex |
| **AEON-USDT** [뚜렷 개선] | Aster | $0.01M | $0.20M | +0.001 | -2.156% | -4.555%→-2.156% | flips-positive-major-reversal-okx-orangex |
| AAVE-USDT-PERPETUAL [뚜렷 개선] | OrangeX | $32.82M | $11.63M | +0.01 | -1.658% | -2.547%→-1.658% | improves-notably-all-sources |
| AAVE-USDT [개선] | Aster | $0.25M | $4.39M | +0.01 | -1.548% | -2.825%→-1.548% | improves-notably-all-sources |
| AAVE-USD [개선] | Hyperliquid | $5.53M | $59.36M | +0.001 | -1.684% | -2.549%→-1.684% | improves-notably-all-sources |
| ADA-USDT-PERPETUAL [16회차 밀집] | OrangeX | $95.35M | $31.26M | +0.011 | -4.173% | -3.882%→-4.173% | flat-tightly-clustered-16th-round |
| ADA-USDT [16회차 밀집] | Aster | $0.61M | $1.61M | +0.01 | -4.07% | -4.137%→-4.07% | flat-tightly-clustered-16th-round |
| ADA-USD [16회차 밀집] | Hyperliquid | $5.36M | $31.33M | +0.001 | -4.186% | -4.098%→-4.186% | flat-tightly-clustered-16th-round |
| ALGO-USDT-PERPETUAL [개선] | OrangeX | $8.88M | $3.17M | +0.01 | -1.453% | -2.555%→-1.453% | mixed-diverges-across-sources |
| ⚠️ ALGO-USDT [뚜렷 악화] | Aster | $0.03M | $0.02M | -0.002 | -3.171% | -2.469%→-3.171% | mixed-diverges-across-sources |
| ALGO-USD [개선] | Hyperliquid | $0.72M | $1.99M | 0.0 | -1.978% | -2.894%→-1.978% | mixed-diverges-across-sources |
| ATOM-USDT-PERPETUAL [거의 유지] | OrangeX | $9.73M | $3.86M | -0.01 | +1.844% | +1.849%→+1.844% | stabilizes-after-reversal |
| ATOM-USDT [소폭 되돌림] | Aster | $0.01M | $1.67M | +0.01 | +2.716% | +3.152%→+2.716% | stabilizes-after-reversal |
| ATOM-USD [소폭 되돌림] | Hyperliquid | $0.32M | $1.91M | 0.0 | +1.937% | +2.06%→+1.937% | stabilizes-after-reversal |
| ASTER-USDT-PERPETUAL [플러스 전환] | OrangeX | $6.77M | $2.49M | +0.01 | +0.298% | -0.494%→+0.298% | flips-slightly-positive |
| ASTER-USDT [대형 OI, 플러스 전환] | Aster | $8.82M | $220.64M | +0.01 | +0.298% | -0.414%→+0.298% | flips-slightly-positive |
| ASTER-USD [플러스 전환] | Hyperliquid | $0.98M | $14.69M | +0.001 | +0.435% | -0.388%→+0.435% | flips-slightly-positive |
| ALLO-USDT [뚜렷 개선] | Aster | $0.05M | $0.02M | +0.001 | -4.84% | -6.962%→-4.84% | improves-notably-reverses-negative-extension |
| ALLO-USDT-PERPETUAL [뚜렷 개선] | OrangeX | $10.26M | $3.62M | +0.01 | -4.416% | -6.556%→-4.416% | improves-notably-reverses-negative-extension |
| HYPER-USD [소폭 개선] | Hyperliquid | $0.16M | $0.31M | +0.001 | -3.216% | -4.419%→-3.216% | slight-improve |
| APEX-USD [개선] | Hyperliquid | $0.11M | $0.65M | +0.001 | -0.492% | -1.578%→-0.492% | improves |
| FARTCOIN [개선] | Hyperliquid | $7.00M | $23.43M | +0.001 | -1.304% | -1.954%→-1.304% | improves |
| ETHFI-USD [개선] | Hyperliquid | $0.91M | $8.41M | +0.001 | -1.84% | -4.991%→-1.84% | improves |
| ⚠️ ETH-USD [dYdX 복구, 플러스 전환] | dYdX | $11.66M | $19.43M | 0.0 | +0.155% | -0.976%→+0.155% | dydx-recovered-flips-positive |
| ⚠️ BTC-USD [dYdX 복구, 낙폭 완화] | dYdX | $3.73M | $17.79M | 0.0 | -0.71% | -1.035%→-0.71% | dydx-recovered-eases |
| ⚠️ SOL-USD [dYdX 복구, 낙폭 완화] | dYdX | $0.65M | $4.43M | -0.001 | -0.511% | -1.345%→-0.511% | dydx-recovered-eases |

## 테마 태그

1. **⚠️⚠️ BICO: '3소스 완전 수렴' 선언이 1회차 만에 반박, 3소스 전부 재차 마이너스 확대** (bico-reverses-after-convergence-claim).
2. **⚠️⚠️ ACE: 개선 정체가 전 소스 동조 재악화로 전환. 8/18 언락 약 6.1일 앞** (ace-worsens-uniformly).
3. **⚠️⚠️ CAP: 3소스 전부 추가 재가속, 3회차 연속** (cap-reaccelerates-further).
4. **⚠️ HYPE: 마이너스 반전 4회차, 낙폭 추가 확대** (hype-negative-extends-4th-round).
5. **⚠️⚠️ CASHCAT: HL만 추가 심화, OrangeX·Aster는 개선으로 방향 분열** (cashcat-diverges-mixed).
6. **BEAT: 개선 4회차 연속** (beat-improves-4th-round).
7. **BSB: -4~5%대로 추가 수렴** (bsb-converges-narrower).
8. **MMT: 방향 유지, 낙폭 지속 완화** (mmt-improves-further).
9. **⚠️ BANK: 가중평균 복원으로 표면상 개선, 실질은 -5.4~5.7%대 정체~소폭 재악화. 8/17 언락 약 5.1일 앞** (bank-plateaus-mixed).
10. **⚠️⚠️ KAITO: 재악화 뚜렷 가속, Aster 크로스 4회차 연속 소실. 8/20 언락 약 8.1일 앞** (kaito-worsens-accelerates).
11. **⚠️⚠️ AEON: OKX·OrangeX 마이너스→플러스 전환, 이번 회차 최대 반전 사례** (aeon-flips-positive-major-reversal).
12. **AKE: 급등 이후 고점권 다지기, 되돌려지지 않음** (ake-consolidates-near-highs).
13. **GRAM: 플러스권에서 소폭 확대** (gram-extends-positive).
14. **GIGGLE: 추가 확대, 필드 이상치 36회차 연속** (giggle-extends-36th-round).
15. **⚠️ PIPPIN: 개선 지속, funding 완전동일 패턴에서 이번 회차 처음 이탈** (pippin-funding-anomaly-breaks).
16. **ATOM: 재가열 반전 이후 +1.9~2.7% 구간 안정화** (atom-stabilizes-after-reversal).
17. **AAVE·ASTER·ALLO: 전 소스 뚜렷 개선(ASTER 플러스 전환)** (aave-aster-allo-improve).
18. **ALGO: 소스 간 방향 분열(OrangeX·HL 개선, Aster 악화)** (algo-diverges-mixed).
19. **1000RATS: 거의 유지** (1000rats-roughly-flat).
20. **ADA: 16회차째 -4.1~4.2% 좁은 밴드에 사실상 고정** (ada-flat-tightly-clustered-16th).
21. **⚠️⚠️ BLESS: 플러스 전환이 완전히 되감겨 재차 마이너스 크게 확대(-7.4~7.7%)** (bless-flip-fully-unwound).
22. **AIO: Binance 개선, Aster 소폭 재악화로 방향 엇갈림** (aio-mixed).
23. **⚠️ 데이터 전량 복구: bybit·dydx_chain·`/global`이 2회차 연속 실패 이후 이번 회차 4회 시도 끝 복구** (data-fully-recovered).
24. **총시총 $2.2663T(직전 $2.2617T 대비 소폭 증가)·BTC도미넌스 56.30%(직전 56.415% 대비 소폭 하락)** (global-metrics-recovered-slight-shift).
25. **⚠️ OKX 직접조회 funding 재검증: GIGGLE·MMT·GRAM 동일값 지속, PIPPIN 이번 회차 처음 이탈, KAITO는 별개 스케일** (okx-funding-anomaly-reverified).
26. **dYdX(ETH·BTC·SOL) 이번 회차 전량 복구, 3종목 모두 낙폭 완화·ETH는 플러스 전환** (dydx-recovered-improves).
27. **Fear&Greed 이번 회차도 미재조회** (fear-greed-not-rechecked).
28. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
29. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
30. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
31. **TUT: 이번 회차도 재확인 생략** (tut-status-unconfirmed-no-further-check).

## 데이터 신뢰도

**okex_swap·hyperliquid·aster·orangex_futures(3회 재시도 끝 복구)·binance_futures와 OKX
직접API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)는 이번 회차 정상 확보**됐다. **bybit·dydx_chain·
CoinGecko `/global` 3종은 지난 2회차 연속 재실패했으나 이번 회차 4회 시도 끝에 전량
복구**됐다(재시도 상한 3~4회 준수 원칙을 지켰다).

**bybit 복구**로 ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·ALLO·1000RATS·ATOM 10종이 이번 회차
**Binance+Bybit 가중평균**으로 정상 복원됐다(직전 회차는 Binance 단독값).

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: ticker·open-interest·funding-rate 개별
엔드포인트 전부 1차 시도부터 정상. **funding 재검증 결과**: GIGGLE·MMT·GRAM 3종의 raw
`fundingRate`가 이번 회차도 정확히 `0.00005`로 완전 동일했으나, **PIPPIN은 이번 회차 처음
`0.0000545074141550`으로 미세하게 달라져** '4종 완전동일' 패턴에서 이탈했다. KAITO는
raw `-0.0021358570958507`로 애초부터 뚜렷이 다른 스케일이라 이 그룹과 무관하다.
`nextFundingRate`는 5종목 전부 빈 문자열로 확인됐다(정산 전 미공표 상태 추정). **GIGGLE**은
vol24h·volCcy24h 100배 스케일 차이 이상치가 **36회차 연속**(이번 회차 88,141,939 vs
881,419.39로 정확히 100배), **KAITO**는 vol24h=volCcy24h 완전동일값 이상치가 **36회차
연속**, **GRAM**도 완전동일값(2,887,109=2,887,109)이 **34회차 연속** 재현됐다. **MMT·
PIPPIN**의 10배 비율(vol24h 대 volCcy24h)이 **20회차 연속** 재현됐다.

**Hyperliquid**: 정상 확보 — ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·ALGO·GRAM·HYPE·HYPER·
APEX·FARTCOIN·ETHFI 확보(raw 정밀값). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·BTW·BLESS·
ANSEM·TUT는 HL 미상장(기존과 동일). **SOL은 이번 회차도 canonical SOL-USD 미발견**
(HYNA:SOL-USD 이형 표기만 존재).

**Aster**: 정상 확보 — BANK·AAVE·ADA·BICO·BEAT·BSB·AKE·ATOM·ALLO·1000RATS·AIO·AEON·
ASTER·CAP·ALGO·ACE·CASHCAT·BTW·ANSEM·BLESS 전량 확보(raw 정밀값). **KAITO-USDT는
이번 회차도 응답에서 재확인 실패**(4회차 연속 누락). MMT·GIGGLE·PIPPIN·GRAM·CORE·TUT는
Aster에서 여전히 미발견.

**OrangeX**: 정상 확보(3회차 재시도 끝) — ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·
BEAT·BANK·AKE·CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값). KAITO·1000RATS·GRAM·MMT·
PIPPIN·GIGGLE·CORE·BTW는 여전히 미발견.

**dYdX(`dydx_chain`)**: 4회 시도 끝 복구 — BTC-USD·ETH-USD·SOL-USD 전부 재확인, 3종목
모두 낙폭 완화(ETH는 플러스 전환).

**CoinGecko `/global`**: 4회 시도 끝 복구 — 총시총 $2,266,300,785,441.92, BTC도미넌스
56.30%로 갱신(직전 참고치 $2,261,689,321,024 / 56.4152% 대비 소폭 변화).

**bybit**: 4회 시도 끝 복구 — ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·ALLO·1000RATS·ATOM
10종은 Binance+Bybit 가중평균으로 복원.

**Fear&Greed**: 이번 회차도 재조회하지 않음(최우선 추적과제에 시간 집중).

**신규 발견**: (a) BICO의 '가격·펀딩 완전 수렴' 선언이 이번 회차 1회차 만에 반박돼, 단일
회차 완결 판정의 위험성이 재확인됐다. (b) AEON이 OKX·OrangeX에서 마이너스→플러스로 뚜렷
전환해 이번 회차 최대 반전 사례로 부상했다. (c) BLESS의 플러스 전환이 완전히 되감겨
-7.4~7.7%대로 마이너스가 크게 확대됐다. (d) bybit·dydx_chain·`/global`이 2회차 연속
실패 이후 다시 전량 복구돼, 데이터 가용성이 회차마다 크게 요동치는 패턴이 재확인됐다.
(e) OKX 직접조회 4종목 funding '완전동일' 패턴에서 PIPPIN이 이번 회차 처음 미세하게
벗어나 순수 기본값/누락값 가설에 새로운 단서가 추가됐다(완전 고정값이 아니라 종목별로
근접하되 미세하게 다를 수 있음을 시사). (f) CASHCAT의 '하락 추세화'가 이번 회차 방향
분열로 흔들려, 온체인 신호와의 인과관계를 아직 확정할 수 없다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접 조회분)의
CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 `oiUsd` 필드를 직접 채택(51회차
연속 일관 적용), funding은 raw fundingRate×100 방식으로 계산했다; (d) ADA·AAVE·ATOM·ASTER·
AKE·BANK·ALLO·ALGO·ACE·1000RATS 등 복수 거래소 종목의 `chg24`·`funding`은 이번 회차
Binance+Bybit 가중평균(거래량 가중)으로 복원했다; AIO는 Binance·Aster는 재조회했으나
bybit 가중평균 대상이 아니다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상
스케일로 관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·
PIPPIN·KAITO·GRAM·CORE·BSB·BLESS는 Binance/Bybit 상장이 불확실하거나 없어 OKX·DEX로만
집계되는 구조다. ACE는 Binance에서 확인된 상태를 유지했다; (g) BTW·CASHCAT·ANSEM·
HYNA:PUMP-USD·HYNA:HYPE-USD는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다;
(h) TUT는 이번 회차도 재확인을 생략했다; (i) ACE·BANK·KAITO의 언락 정보는 이전 회차
WebSearch 기반이며 이번 회차 재검증하지 않았다; (j) GIGGLE·KAITO(OKX직접)의 필드
이상치가 36회차, GRAM도 34회차 연속 재현돼 구조적 패턴으로 굳어졌으나 근본 원인은
규명하지 않았다; (k) dYdX exchange id는 `dydx_chain`을 사용했고 이번 회차 4회 시도 끝
전량 복구됐다; (l) HL에서 canonical SOL-USD는 여전히 발견되지 않았다; (m) bybit·`/global`도
4회 시도 끝 복구돼 총시총·BTC도미넌스와 10종목 가중평균 계산이 이번 회차 재개됐다;
(n) KAITO-USDT(Aster)는 4회차 연속 응답에서 확인되지 않았다; (o) CASHCAT의 방향 분열이
온체인 신호와 어떤 관계인지(선행·후행) 확인하지 못했다; (p) OKX 직접조회 GIGGLE·MMT·GRAM의
funding이 이번 회차도 동일값(0.00005)으로 관측된 원인은 규명하지 못했고, PIPPIN의 이번
회차 이탈이 우연인지 구조적 변화인지도 확인하지 못했다 — 다음 회차 추적 필요.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
