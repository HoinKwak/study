# 선물시장 스카우트 브리핑 — 2026-08-05 07:03 UTC (KST 2026-08-05 16:03)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-05T04:58:00Z)
> 로부터 약 2시간05분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`은 정상 응답 — 총시총 **$2.2789T**(직전 $2.27T에서 소폭 상승, +0.5%),
BTC도미넌스 **56.60%**(직전 56.58%에서 거의 변화 없음), ETH도미넌스 **9.90%**(직전과 동일),
24h 시총 변동 **+0.75%**로 직전(+0.02%)보다 뚜렷하게 플러스 쪽으로 움직여 완전 보합 흐름이
소폭 깨졌다. Fear&Greed는 alternative.me에서 이번 회차도 **27(Fear)**로 **4연속 동일값** 유지
— 이례적으로 긴 안정 구간이다.

**⚠️ OKX 개별 티커 API의 BICO·CORE·KAITO·GRAM 4종목 거래량 이상(vol24h=volCcy24h 동일값)이
이번 회차도 재현**돼(3연속) 재시도로 정상화 여부를 확인했으나 **정상화되지 않았다**. 이에 따라
**이번 회차부터 순수 이월을 중단하고, 정상 검증된 6종목과 동일한 `volCcy24h×last` 공식을 적용한
추정치로 전환**했다(저신뢰도로 명시 표기, 자세한 내용은 데이터 신뢰도 절 참조).

- **⚠️ BICO**: 4연속 재가속 — OKX +31.28%→+35.81%→**+57.88%**(last$0.02722/open24h$0.01724)로
  상승폭이 크게 확대, funding도 -0.0248%→**-0.0922%**로 대폭 심화(숏 스퀴즈 가속 시사). Aster도
  +32.80%→**+59.75%**로 강하게 동조.
- **CORE·GIGGLE·PIPPIN·AEON**: 모두 3연속 개선 — CORE -6.04%→**-4.81%**(funding -0.0189%→
  **-0.0118%**로 완화), GIGGLE -6.58%→**-6.09%**, PIPPIN -6.68%→**-3.51%**, AEON -12.52%→
  **-10.11%**(Aster -10.17%와 거의 완전 동조).
- **⚠️ BEAT**: 2연속 개선이 깨지고 재악화 — OKX -9.89%→**-12.96%**(last$2.5839/open24h$2.9685),
  반면 DEX(Aster)는 -10.32%→**-21.48%**로 훨씬 큰 폭으로 하락해 CEX·DEX 괴리가 크게 확대됐다
  — 8월 언락 우려는 배경 리스크로 잔존.
- **⚠️ MMT**: 3연속 개선 흐름이 크게 반납 — -0.65%→**-6.60%**(last$0.1456/open24h$0.1559)로 재악화.
- **⚠️ CAP**: CEX 개선이 이어졌으나(-5.39%→**-2.43%**) DEX(Aster -4.62%→**-4.92%**)와 괴리가 다시
  확대 — 직전 회차 0.77%p까지 좁혀졌던 괴리가 다시 **2.49%p**로 벌어졌다.
- **⚠️ GRAM**: 다시 플러스로 재반전 — CEX -0.50%→**+0.29%**, HL도 -0.56%→**+0.12%**로 동조,
  이번이 3회째 방향전환으로 whipsaw가 계속됐다.
- **⚠️ ALGO**: 반대로 다시 마이너스로 재반전 — +1.14%→**-1.25%**(Binance-1.25%·Bybit-1.25%),
  HL(-1.08%)도 동조, 역시 3회째 방향전환.
- **⚠️ BANK**: CEX·DEX 방향이 엇갈리기 시작 — CEX 가중평균 +31.02%→**+26.91%**(Binance+26.81%·
  Bybit+27.60%)로 3회 연속 둔화가 이어진 반면, DEX(Aster)는 +27.69%→**+28.91%**로 반대로 소폭 상승.
- **⚠️ BLESS-USDT(Aster)**: 2연속 큰 폭 상승 확대 — -15.54%→+29.01%→**+49.27%**로 급등이 계속
  확대, 저유동 초소형 종목($0.59M 거래량)의 변동성이 여전히 매우 커 후속 회차 재확인이 계속
  필요하다. OrangeX는 CoinGecko가 4회 연속 429로 재확인 실패해 직전값(-13.19%)을 이월 — 4회째
  두 소스 간 방향 비교가 불가능하다.

한편 **AKE는 상승폭이 크게 둔화**됐다(CEX 가중평균 +3.67%→**+1.91%**, DEX도 +3.58%→**+1.15%**로
동조 둔화), **1000RATS는 3연속 개선**(-9.99%→**-6.92%**, DEX -7.99%와 수렴), **ALLO는 거의 보합
유지 속 소폭 재악화**(-0.61%→**-0.84%**), **AAVE는 소폭 개선**(-1.77%→**-1.07%**), **ADA는
whipsaw가 다소 진정**(-3.46%→**-3.06%**, HL -2.82%로 거의 변화 없음), **ATOM은 거의 변화 없음**
(-1.33%→**-1.29%**)이 이어졌다. **ASTER(CEX·DEX·HL 전 소스)는 계속 거의 0%로 보합권에 수렴**했다
(CEX -0.40%·Aster -0.39%·HL -0.41%). **AIO는 소폭 재가속**(+11.79%→**+13.07%**)하며 여전히
두자릿수 강세를 유지했다(Falcon Finance 스테이킹볼트 내러티브는 신규 촉매 확인 없이 지속).
**⚠️ CASHCAT은 4연속 둔화**가 이어졌다(가중평균 +31.82%→**+17.34%**, HL+17.14%·Aster+19.23%) —
Robinhood Chain 밈코인 whipsaw는 진정 국면에 들어선 모습이다. **BTW는 4연속 진정**(+21.51%→
+13.41%→**+9.35%**)되며 두자릿수에서 한자릿수 상승으로 진입했다. **ANSEM은 4연속 악화가 멈추고
개선으로 전환**됐다(-8.43%→-10.35%→**-7.64%**). **HYPER-USD(HL)는 안정화가 계속**됐다(-4.38%→
**-3.85%**, funding -0.044%→**-0.032%**로 계속 완화, 저유동 소형종목 변동성 주의는 여전).
**ETHFI는 개선세로 복귀**했다(-9.32%→**-7.99%**, 촉매는 여전히 미확인). **HYPE는 대형 OI($1.26B)
유지한 채 상승폭이 확대**됐다(+2.91%→**+4.69%**). **dYdX funding은 계속 정상 범위**를 유지했다
(BTC 0.0%→0.0%, ETH -0.004%→**-0.003%**), 가격은 BTC +0.40%→**+0.66%**·ETH +0.02%→**+0.37%**로
상승폭이 확대됐다.

Binance·Bybit 상위 거래량 재스캔에서 이번 회차는 **토큰화 주식 퍼프가 관측되지 않았다**(직전 회차
AAPL·AMZN·AMD·AAOI 발견 이후 이번엔 상위 리스트에 안 보였으나, 완전한 부재를 단정하는 것은 아니다).

## ⚠️ 데이터 인프라 이슈 — OKX 거래량 이상값 3연속·방법론 전환 · GMX 계속 제외

OKX 개별 티커 API에서 **BICO·CORE·KAITO·GRAM 4종목**이 이번 회차도 `vol24h`와 `volCcy24h`가
완전 동일값으로 반환됐다(3회 연속 재현). 지시에 따라 재시도해 정상화 여부를 확인했으나 **정상화되지
않았다**. 이에 두 회차 동안 유지했던 순수 이월 방식을 중단하고, 정상 검증된 6종목(BEAT·GIGGLE·
PIPPIN·AEON·MMT·CAP)과 동일한 `volCcy24h×last` 공식을 적용한 추정치로 전환했다 — **저신뢰도로
명시 표기**하며, 계속 동일값 이상이 관측되는 한 이 방법론을 유지할 예정이다.

GMX(`gmx-perpetuals-v2-arbitrum`)는 다회차 연속 완전 동일 수치가 확정돼 이번 회차도 재조회하지
않고 제외 상태를 유지한다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **⚠️ BICO (Biconomy)** [4연속 재가속] | OKX(직접API) | $115.69M(공식추정) | $5.97M | -0.0922% | +57.88% | +31.28%→+35.81%→+57.88%로 4회 연속 확대, funding 대폭 심화. Aster도 +59.75%로 동조. ⚠️거래량 이상 3연속, 이번 회차부터 이월 중단·공식 적용 | reaccelerates-4th-consecutive-round-funding-deepens-volume-formula-switch |
| **⚠️ BEAT (Audiera)** [2연속 개선 깨지고 재악화] | OKX(직접API) | $172.94M | $8.52M | +0.005% | -12.96% | -9.89%→-12.96%로 재악화, DEX(-21.48%)는 훨씬 크게 하락 — 괴리 확대. 8월 언락 우려 배경 지속 | worsens-again-breaks-2-round-improvement-dex-diverges |
| **⚠️ MMT (Momentum)** [3연속 개선 반납] | OKX(직접API) | $9.65M | $2.48M | -0.0707% | -6.60% | -0.65%→-6.60%로 크게 재악화, 3연속 개선 흐름 반납 | worsens-breaks-3-round-improvement |
| **BANK (Lorenzo)** [⚠️ CEX·DEX 방향 엇갈림] | Binance/Bybit | $556.49M | $23.65M | +0.005% | +26.91% | CEX 가중평균 +31.02%→+26.91%(Binance+26.81%·Bybit+27.60%)로 3연속 둔화, DEX는 반대로 +28.91%로 소폭 상승 | decelerates-3rd-round-diverges-from-dex |
| CORE [3연속 개선] | OKX(직접API) | $5.81M(공식추정) | $1.05M | -0.0118% | -4.81% | -6.04%→-4.81%로 낙폭 축소 3연속, funding 완화 | continues-improvement-3rd-round-volume-formula-switch |
| KAITO (CEX) [플러스 지속] | OKX(직접API) | $41.30M(공식추정) | $7.17M | +0.005% | +3.70% | +2.85%→+3.70%, HL(+3.29%)도 동조 지속 | continues-positive-tracks-hl-volume-formula-switch |
| GRAM [⚠️ 3회째 재반전] | OKX(직접API) | $13.04M(공식추정) | $6.92M | +0.005% | +0.29% | -0.50%→+0.29%, HL(+0.12%)도 동조 재반전 — whipsaw 지속 | flips-positive-again-3rd-flip-volume-formula-switch |
| GIGGLE (Giggle Fund) [3연속 개선] | OKX(직접API) | $52.18M | $3.53M | +0.005% | -6.09% | -6.58%→-6.09%로 낙폭 축소 지속 | continues-improvement-3rd-round |
| PIPPIN [3연속 개선] | OKX(직접API) | $12.77M | $2.01M | +0.0261% | -3.51% | -6.68%→-3.51%로 낙폭 축소 지속 | continues-improvement-3rd-round |
| AEON [개선 지속] | OKX(직접API) | $15.31M | $2.43M | +0.005% | -10.11% | -12.52%→-10.11%, Aster(-10.17%)와 거의 동일값 | continues-improvement-tracks-aster |
| CAP [⚠️ DEX와 괴리 재확대] | OKX(직접API) | $10.86M | $1.20M | +0.005% | -2.43% | CEX -5.39%→-2.43% 개선, DEX -4.62%→-4.92% 소폭 악화 — 괴리 0.77%p→2.49%p로 재확대 | improves-dex-divergence-widens-again |
| ALGO [⚠️ 3회째 재반전] | Binance/Bybit | $17.24M | $16.53M | +0.01% | -1.25% | +1.14%→-1.25%, HL(-1.08%)도 동조 재반전 | flips-negative-again-3rd-flip-tracks-hl |
| AKE (Akedo) [상승폭 크게 둔화] | Binance/Bybit | $110.74M | $49.29M | +0.0355% | +1.91% | +3.67%→+1.91%(가중평균), DEX(+1.15%)도 동조 둔화 | decelerates-tracks-dex |
| 1000RATS [3연속 개선] | Binance/Bybit | $164.99M | $22.58M | +0.014% | -6.92% | -9.99%→-6.92%로 낙폭 축소 지속, DEX(-7.99%)와 수렴 | continues-improvement-3rd-round-converges-dex |
| ALLO (Allora) [거의 보합] | Binance/Bybit | $18.33M | $17.06M | -0.0335% | -0.84% | -0.61%→-0.84%로 거의 변화 없음, DEX(-0.78%)도 유사 | near-flat-mild-worsening |
| AAVE [소폭 개선] | Binance/Bybit | $98.86M | $96.92M | +0.0025% | -1.07% | -1.77%→-1.07%, HL(-1.11%)도 유사 수준 | mild-improvement-near-flat |
| ADA [whipsaw 진정] | Binance/Bybit | $215.85M | $177.13M | +0.0005% | -3.06% | -3.46%→-3.06%로 낙폭 축소, HL(-2.82%)도 거의 동일 | mild-improvement-still-negative |
| ATOM [거의 변화 없음] | Binance/Bybit | $23.80M | $31.29M | +0.007% | -1.29% | -1.33%→-1.29%, HL(-1.35%)도 유사 | stable-near-unchanged |
| ASTER (CEX) [보합권 유지] | Binance/Bybit | $15.07M | $112.45M | +0.005% | -0.40% | -0.12%→-0.40%, DEX·HL도 모두 거의 0%로 전 소스 수렴 | continues-near-flat-all-venues-converge |
| AIO (OlaXBT) [소폭 재가속] | Binance/Bybit | $21.00M | $4.45M | +0.0064% | +13.07% | +11.79%→+13.07%로 상승폭 확대, 여전히 강한 두자릿수. Falcon Finance 내러티브 지속 | mild-reacceleration-still-strong-double-digit |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **⚠️ BEAT-USDT** [CEX보다 훨씬 크게 악화] | Aster | $1.21M | $0.38M | +0.009% | -21.48% | -10.32%→-21.48%로 CEX(-12.96%)보다 훨씬 크게 하락 — 괴리 확대, 8월 언락 우려 배경 지속 | worsens-more-than-cex-divergence-widens |
| **BICO-USDT** [CEX와 함께 4연속 재가속] | Aster | $0.76M | $0.018M | +0.001% | +59.75% | CEX(+57.88%)와 유사한 강한 동조, 4회 연속 재가속 | tracks-cex-reaccelerates-4th-round |
| **⚠️ BLESS-USDT** [2연속 큰 폭 상승 확대] | Aster | $0.59M | $0.24M | +0.005% | +49.27% | +29.01%→+49.27% 급등 계속 확대 — 저유동 초소형, 후속 회차 재확인 계속 필요 | continues-large-swing-2nd-round-still-unusual |
| **⚠️ BLESS-USDT-PERPETUAL** [재확인 4연속 실패, 이월] | OrangeX | $102.83M | $40.35M | -0.014% | -13.19% | CoinGecko orangex_futures 4연속 429로 재확인 실패, 직전값 이월 — Aster와의 방향 비교 4회째 불가 | recheck-failed-4th-round-carryover |
| **⚠️ BANK-USDT** [CEX와 괴리 발생] | Aster | $1.32M | $0.43M | +0.001% | +28.91% | CEX(+26.91%)는 3연속 둔화, DEX는 반대로 소폭 상승 — 방향 엇갈림 시작 | diverges-from-cex-slight-uptick |
| **⚠️ CASHCAT** [4연속 둔화] | Hyperliquid/Aster | $21.41M | $15.10M | -0.0105% | +17.34% | 가중평균 +31.82%→+17.34%(HL+17.14%·Aster+19.23%) — 상승폭 계속 축소, Robinhood Chain 밈코인 whipsaw 진정 국면 진입 모습 | continues-deceleration-4th-round |
| **BTW** [4연속 진정] | Aster | $1.67M | $9.13M | +0.011% | +9.35% | +13.41%→+9.35%로 계속 둔화, 두자릿수→한자릿수 상승 진입 | continues-deceleration-4th-round |
| **1000RATS-USDT** [CEX와 수렴] | Aster | $0.46M | $0.033M | +0.001% | -7.99% | CEX(-6.92%)와 유사한 수준으로 수렴 | tracks-cex-converges |
| **⚠️ CAP-USDT** [CEX와 괴리 재확대] | Aster | $0.026M | $0.027M | +0.001% | -4.92% | CEX(-2.43%)와의 괴리 0.77%p→2.49%p로 재확대 | cex-dex-divergence-widens-again |
| **AKE-USDT** [CEX와 함께 둔화] | Aster | $0.73M | $11.87M | +0.011% | +1.15% | CEX(+1.91%)와 함께 상승폭 축소 | tracks-cex-decelerates |
| ASTER-USDT [대규모 OI 유지] | Aster | $9.58M | $221.16M | +0.012% | -0.39% | OI $221.2M 대형 유지, CEX·HL과 계속 수렴 | near-flat-large-oi-converges-all-venues |
| **ANSEM** [4연속 악화 멈추고 개선] | Aster | $0.35M | $1.16M | +0.001% | -7.64% | -10.35%→-7.64%로 4연속 악화 흐름 처음 개선 전환 | improves-breaks-4-round-worsening |
| AEON-USDT [CEX와 거의 동일값] | Aster | $0.083M | $0.21M | +0.02% | -10.17% | CEX(-10.11%)와 거의 완전히 일치 | tracks-cex-near-identical-continues |
| ALLO-USDT [CEX와 유사] | Aster | $0.080M | $0.043M | -0.007% | -0.78% | CEX(가중평균-0.84%)와 유사 수준 | tracks-cex-near-flat |
| GRAM [⚠️ 3회째 재반전] | Hyperliquid | $2.40M | $12.45M | +0.001% | +0.12% | CEX(+0.29%)와 함께 다시 플러스로 반전 — whipsaw 지속 | flips-positive-again-tracks-cex-3rd-flip |
| HYPE-USD [대형 OI 유지, 상승폭 확대] | Hyperliquid | $249.60M | $1,258.79M | +0.001% | +4.69% | 대형 OI($1.26B) 유지, +2.91%→+4.69%로 상승폭 확대 | steady-large-oi-accelerates |
| **HYPER-USD** [안정화 지속] | Hyperliquid | $0.30M | $0.33M | -0.032% | -3.85% | -4.38%→-3.85%로 안정, funding -0.044%→-0.032%로 완화. 저유동 소형종목 변동성 주의 | continues-stabilization-funding-eases-further |
| KAITO-USD [CEX와 함께 플러스 지속] | Hyperliquid | $4.05M | $24.86M | +0.001% | +3.29% | CEX(+3.70%)와 함께 소폭 상승 지속 | tracks-cex-continues-positive |
| APEX-USD [마이너스→플러스 전환] | Hyperliquid | $0.16M | $0.79M | +0.001% | +1.27% | -1.25%→+1.27%, 저유동 소형종목 노이즈 가능성 | low-liquidity-flips-positive |
| FARTCOIN [상승폭 재확대] | Hyperliquid | $5.79M | $24.16M | +0.001% | +2.75% | +0.83%→+2.75%로 재확대 | uptick-reaccelerates |
| ADA-USD [거의 변화 없음] | Hyperliquid | $4.24M | $31.65M | 0.0% | -2.82% | -2.77%→-2.82%로 거의 동일, CEX(-3.06%)는 소폭 개선 | near-unchanged-still-negative |
| AAVE-USD [CEX와 유사] | Hyperliquid | $10.60M | $64.32M | +0.001% | -1.11% | CEX(-1.07%)와 거의 동일한 수준, OI $64.3M 대형 유지 | tracks-cex-near-flat |
| ATOM-USD [CEX와 유사] | Hyperliquid | $0.64M | $2.05M | 0.0% | -1.35% | CEX(-1.29%)와 유사, 안정적 소폭 마이너스 지속 | tracks-cex-stable |
| ALGO-USD [⚠️ 3회째 재반전] | Hyperliquid | $0.93M | $2.40M | +0.001% | -1.08% | CEX(-1.25%)와 함께 다시 마이너스로 전환 — whipsaw 지속 | flips-negative-again-tracks-cex-3rd-flip |
| **ETH-USD** [funding 정상범위 유지] | dYdX | $5.31M | $20.58M | -0.003% | +0.37% | -0.004%→-0.003%로 정상 범위, 가격 상승폭 확대 | funding-normal-range-continues |
| **BTC-USD** [funding 정상범위 유지] | dYdX | $7.52M | $18.04M | 0.0% | +0.66% | 0.0%→0.0%로 정상 범위, 가격 상승폭 확대 | funding-normal-range-continues |
| **ETHFI-USD** [개선세로 복귀] | Hyperliquid | $4.33M | $7.28M | +0.001% | -7.99% | -9.32%→-7.99%로 개선, 촉매는 여전히 미확인 | mild-improvement-catalyst-still-unclear |

## 테마 태그

1. **시장 전반: 총시총 $2.2789T(소폭 상승), BTC도미넌스 56.60%, ETH 9.90%, 24h 시총 변동 +0.75%로 직전(+0.02%)보다 뚜렷하게 플러스 — 완전 보합 흐름 소폭 깨짐. Fear&Greed 27(Fear) 4연속 동일값** (market-mild-uptick-fear-greed-4th-confirm).
2. **⚠️ BICO 4연속 재가속(+31.28%→+35.81%→+57.88%)** — funding -0.0922%로 대폭 심화, Aster도 +59.75%로 동조 (bico-reaccelerates-4th-round-funding-deepens).
3. **CORE·GIGGLE·PIPPIN·AEON 모두 3연속 개선** (core-giggle-pippin-aeon-3rd-round-improvement).
4. **⚠️ BEAT 2연속 개선 깨지고 재악화, DEX(-21.48%)가 CEX(-12.96%)보다 훨씬 크게 하락 — 괴리 확대** (beat-worsens-dex-diverges-more).
5. **⚠️ MMT 3연속 개선 흐름 크게 반납, -6.60%로 재악화** (mmt-worsens-breaks-3-round-improvement).
6. **⚠️ CAP CEX 개선 지속(-2.43%)하나 DEX(-4.92%)와 괴리 재확대(0.77%p→2.49%p)** (cap-divergence-widens-again).
7. **⚠️ GRAM 3회째 방향전환, 다시 플러스로 재반전 — whipsaw 지속** (gram-flips-positive-3rd-flip).
8. **⚠️ ALGO 3회째 방향전환, 다시 마이너스로 재반전** (algo-flips-negative-3rd-flip).
9. **⚠️ BANK CEX·DEX 방향 엇갈림 시작** — CEX 3연속 둔화(+26.91%), DEX는 반대로 소폭 상승(+28.91%) (bank-cex-dex-diverge).
10. **AKE 상승폭 크게 둔화(+3.67%→+1.91%)** — DEX도 동조 둔화 (ake-decelerates-tracks-dex).
11. **1000RATS 3연속 개선, DEX와 수렴. ALLO 거의 보합. AAVE 소폭 개선. ADA whipsaw 다소 진정. ATOM 거의 변화 없음** (rats-allo-aave-ada-atom-mostly-stable-improving).
12. **ASTER(CEX·DEX·HL 전 소스) 계속 거의 0%로 보합권 수렴** (aster-all-venues-continue-converge-flat).
13. **AIO 소폭 재가속, 두자릿수 강세 지속** — Falcon Finance 내러티브 신규 촉매 없이 지속 (aio-mild-reaccelerates-still-strong).
14. **⚠️ CASHCAT 4연속 둔화(+31.82%→+17.34%)** — Robinhood Chain 밈코인 whipsaw 진정 국면 진입 모습 (cashcat-continues-deceleration-4th-round).
15. **BTW 4연속 진정, 두자릿수→한자릿수 상승 진입** (btw-continues-deceleration-4th-round).
16. **⚠️ BLESS-USDT(Aster) 2연속 큰 폭 상승 확대(+29.01%→+49.27%)** — 저유동 초소형, 후속 재확인 계속 필요; OrangeX는 4연속 429로 재확인 실패·이월 (bless-continues-large-swing-orangex-4th-fail).
17. **ANSEM 4연속 악화 멈추고 개선 전환** (ansem-improves-breaks-4-round-worsening).
18. **HYPE 대형 OI 유지, 상승폭 확대(+2.91%→+4.69%)** (hype-steady-large-oi-accelerates).
19. **HYPER-USD(HL) 안정화 지속, funding 추가 완화** (hyper-continues-stabilization).
20. **ETHFI 개선세로 복귀** — 촉매 계속 미확인 (ethfi-returns-to-improvement).
21. **dYdX funding 정상범위 계속 유지, 가격 상승폭 확대** (dydx-funding-normal-price-accelerates).
22. **⚠️ OKX 개별 티커 BICO·CORE·KAITO·GRAM 거래량 이상 3연속 재현, 정상화 안 됨 — 이번 회차부터 순수 이월 중단, 공식 적용 추정치로 전환(저신뢰도)** (okx-volume-anomaly-3rd-round-methodology-switch-to-formula).
23. **Binance·Bybit 상위 거래량 재스캔에서 이번 회차 토큰화 주식 퍼프 미관측(완전 부재 단정은 아님)** (tradfi-tokenized-stocks-not-observed-this-round).
24. **⚠️ GMX 이번 회차도 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**OKX 개별 티커 API 거래량 이상값(3연속 재현, 방법론 전환)**: BICO·CORE·KAITO·GRAM 4종목에서
이번 회차도 `vol24h`와 `volCcy24h`가 완전 동일한 값으로 반환됐다(3회 연속). 지시에 따라 재시도로
정상화 여부를 확인했으나 **정상화되지 않았다**. 두 회차 동안 유지했던 순수 이월 방식은 정보가치가
낮아지므로 중단하고, 이번 회차부터 정상 검증된 6종목(BEAT·GIGGLE·PIPPIN·AEON·MMT·CAP)과 동일한
`volCcy24h×last` 공식을 적용한 추정치로 전환했다 — **이 4종목의 거래량은 저신뢰도로 명시 표기**한다.
가격변동·funding·OI는 이번 회차도 신선한 원시값(ticker·funding-rate·open-interest 개별
엔드포인트 직접 조회)을 확보했다.

**OKX OI·funding 별도 엔드포인트는 정상**: `/public/open-interest`(oiUsd)·`/public/funding-rate`
(fundingRate)는 이상 4종목을 포함해 10개 심볼(BICO·CORE·KAITO·GRAM·BEAT·GIGGLE·PIPPIN·AEON·
MMT·CAP) 전체 개별 조회로 신선한 원시값을 확보했다.

**CoinGecko 파생 거래소 API**: binance_futures·bybit·hyperliquid·aster는 정상 응답. dydx_chain은
1차 429 이후 재시도로 성공. **orangex_futures는 4회 연속 429로 최종 실패**해 BLESS-USDT-PERPETUAL
값을 이월 처리했다(정직 표기) — 재시도 간격을 늘리거나 다음 회차 다시 시도할 필요가 있다.

**CoinGecko `/global`**: 1차 429 이후 재시도로 정상 응답 확보.

**Fear&Greed**: alternative.me API로 27(Fear) 확인, 4연속 동일값으로 신뢰도 높음.

**신규 상장/급등 스캔**: Binance·Bybit 상위 거래량(24h volume 상위) 재스캔에서 이번 회차는
토큰화 주식·상품 합성 퍼프가 관측되지 않았다(직전 회차 AAPL·AMZN·AMD·AAOI 발견과 대비). 다만
이는 상위 거래량 리스트 범위 내 스캔 결과이며 전체 심볼 목록을 전수조사한 것은 아니므로 완전한
부재를 단정하지는 않는다. 완전 신규 크립토 네이티브 종목은 이번 회차 발견하지 못했다.

한계: (a) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에 따라
cex/dex 리스트에서 전부 제외했다; (c) BICO·CORE·KAITO·GRAM 4종목의 CEX 거래량은 이번 회차부터
공식(volCcy24h×last) 적용 추정치이며 저신뢰도다(3연속 원본 이상값 재현에 따른 방법론 전환); (d)
BLESS-USDT-PERPETUAL(OrangeX)은 재확인 실패로 이월됐고, Aster BLESS-USDT의 연속적 큰 폭 상승과의
방향 비교가 4회째 불가능하다; (e) BANK·CASHCAT·AKE·1000RATS·ALLO·AAVE·ADA·ATOM·ASTER(CEX)·AIO
등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균(chg24)·단순평균(funding)으로 계산했으며,
개별 거래소 값은 `why` 필드에 별도 표기했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
