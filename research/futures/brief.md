# 선물시장 스카우트 브리핑 — 2026-08-09 00:27 UTC (KST 2026-08-09 09:27)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-08T22:29:00Z)
> 로부터 약 2시간 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`은 이번 회차 **5회 연속 429로 확보 실패**(직전 회차 3차 시도 성공과 대비, 이번엔
더 심함) — 정직하게 미확인으로 표기한다. WebSearch로 확인한 참고용(비공식) 스니펫 기준 총시총
약 **$2.29T**·BTC도미넌스 약 **56.8%**로 직전 회차 공식값($2,299,994,629,180.99·56.66%)과
유사한 수준으로 추정되나, 서로 다른 소스라 정밀 비교는 불가하다.

### Fear&Greed 31(Fear) — 12회차 연속 이어지던 30 고정이 처음 깨짐

alternative.me API 정상 응답, **31(Fear)** 확인 — 직전 30에서 소폭 상승했으나 여전히 Fear 구간.
12회차째 유지되던 값이 이번 회차 처음 움직였다.

### 데이터 확보 상황 — `/global`만 이례적으로 심한 429

binance_futures·bybit·okex_swap·hyperliquid·aster는 1~2차 시도로 정상 확보됐고,
orangex_futures·dydx_chain은 429 이후 2차 시도로 확보됐다. **`/global`만 5회 연속 429로 확보
실패**해 이번 회차는 직접 API 기반 시총 수치를 갖지 못했다. OKX 직접 API(KAITO·GIGGLE·MMT·
PIPPIN·GRAM)는 market/ticker+open-interest+funding-rate 개별조회로 17회차 연속 방법론
(`oiUsd` 필드 직접 사용, `vol24_usd=volCcy24h×last`)을 유지해 확보했다.

지금은 **일요일 새벽**(UTC 00:27, KST 09:27) 시간대라 주말 유동성 저하가 일부 저유동성 종목
지표에 영향을 줬을 가능성을 감안해 서술한다.

## 직전 회차 강조 종목 추적 결과 (요청 항목 전체)

- **① ACE(Fusionist) — ⚠️⚠️⚠️ 8/10 언락 하루 전, 거래소별 포지셔닝이 크게 엇갈렸다.**
  Binance/Bybit(가중) +37.67%→**+33.07%**로 첫 냉각, HL도 +40.037%→**+31.565%**(OI -5.3%)로
  동반 후퇴, Aster도 +38.216%→**+35.881%**로 소폭 후퇴 — 3거래소가 언락 직전 처음으로 광범위하게
  식었다. 그런데 **OrangeX만 정반대**: 가격은 거의 유지(+35.552%→+35.448%)한 채 OI가
  $59.62M→**$68.60M(+15.1%)**로 직전 회차 -8.0% 감소를 완전히 되돌리고, 펀딩도 -0.036%→
  **+0.01%**로 플러스 전환됐다 — 언락 하루 전 유일하게 OrangeX에서 신규 롱 유입이 재개된 모습.
- **② CASHCAT — ⚠️⚠️⚠️ 재가속 2회차 연속이나 OI 뒷받침은 약해졌다.** HL +25.662%→
  **+32.507%**, OrangeX +25.284%→**+30.427%**, Aster +24.572%→**+32.672%**로 3거래소 전부
  추가 재가속했다. 그러나 OI는 HL만 $18.53M→**$19.44M(+4.9%)**로 계속 증가했고, **OrangeX는
  $66,652→$60,079(-9.9%)**, Aster도 $1.55M→$1.52M(-2.0%)로 오히려 감소해 — 직전 회차 'OI
  3거래소 전부 재증가'와 달리 이번엔 HL만 신규 매수를 뒷받침한다. 직전 온체인 루틴이 처음
  관측한 혼조 전환(유동성 증가 스트림 종료·h6 감속)과 맞물릴 가능성이 있어, 지금까지 3회 연속
  이어진 '온체인 선행→선물 2시간 지연 확인' 리드-래그가 이번엔 아직 완전히 반영되지 않았거나
  OI 분화가 그 조짐일 수 있다 — 다음 회차 재확인 필요.
- **③ BEAT — ⚠️ 첫 냉각이 한 회차 만에 완전히 재반전됐다.** OKX +32.6%→**+36.236%**, OrangeX
  +31.926%→**+35.635%**, Aster +33.744%→**+36.678%**로 3거래소 전부 재가속했고, **OI도 3거래소
  전부 증가**(OKX +4.0%·OrangeX +12.5%·Aster +6.1%) — 냉각이 일시적이었음이 드러났다. 직전
  확인됐던 Binance 소규모 BEATUSDT 리스팅은 이번 회차 Binance 데이터셋에서 재확인되지 않았다
  (일시적 이상치였을 가능성). Bybit는 9회차 연속 미확인.
- **④ KAITO** — 가격 개선이 계속되며(OKX -14.176%→**-13.029%**, HL -14.374%→**-12.54%**)
  펀딩은 OKX -0.658%→**-0.654%**로 거의 유지된 반면 HL은 -0.293%→**-0.334%**로 더 악화돼
  CEX·DEX 간 펀딩 방향이 갈렸다. **OI는 2회차 연속 감소 후 이번 회차 양쪽 모두 재증가**
  (OKX +9.0%·HL +3.9%)로 전환 — 가격 개선·OI 재증가가 동시 나타나 되돌림 조짐일 수 있으나
  펀딩 악화와는 여전히 괴리된다. 8/20 대형 언락 약 11일 앞.
- **⑤ BSB** — 왕복 휩쏘 완성 이후 재반전 없이 마이너스가 지속·심화됐다(OKX -2.734%→
  **-3.234%**, OrangeX -2.417%→**-2.835%**, Aster는 -3.303%→**-3.135%**로 거의 유지) — 재차
  플러스로 튀지 않고 마이너스에 정착하는 모습.
- **⑥ BTW** — Aster -5.36%→**-7.614%**로 3회차 연속 심화, OI도 $14.30M→$14.52M(+1.5%)로
  계속 늘어 프레시 숏 유입이 지속된다는 정황이 강화됐다.

## 이번 회차 그 외 주요 변화

**⚠️ ALLO·AIO — 이번 회차 처음으로 플러스권에서 마이너스로 전환.** ALLO는 Binance/Bybit
(+3.133%→**-0.659%**)·OrangeX(+3.135%→**-0.958%**)·Aster(+3.449%→**-1.378%**) 3거래소 전부
동시에 반전했고(OI는 Binance/Bybit·OrangeX 3회차 연속 감소, Aster만 소폭 반등), AIO도
+2.774%→**-1.900%**로 반전됐다 — 여러 회차 이어지던 'OI 감소 속 가격만 유지'가 결국 가격도
무너지는 결말로 이어진 사례로 해석할 수 있다. **1000RATS**도 2회차 연속 개선 흐름이 재반전돼
-3.748%→**-4.691%**로 악화(Aster -2.402%→-5.344%로 더 큰 폭 악화)됐다. **AAVE·BANK**는 직전
회차 개선·재가속 흐름이 한 회차 만에 꺾여 각각 냉각(+2.216%→+1.723%)·악화(-1.691%→-2.449%,
다만 Aster만 개선)됐다. **AEON·BICO**는 2회차 연속 재가속을 이어갔다(AEON +14.651%→
+18.767%대, BICO +12.542%→+21.466%대, BICO는 OrangeX OI가 +30.3% 급증) — AEON은 OKX·
OrangeX 펀딩이 모두 플러스에서 마이너스로 전환돼 가격 급등에도 숏이 프리미엄을 지불하는
이례적 구도가 나타났다. **ADA**는 2회차 연속 마이너스를 유지해(Binance/Bybit -0.367%→-0.65%로
심화) 4회차 이어졌던 극단 휩쏘 패턴이 '지속 마이너스'로 정착되는 모습이다. **GIGGLE**은
vol24h/volCcy24h 필드 순서 역전이 **3회차 연속 재현**됐고(vol24h 67,644,482 > volCcy24h
676,444.82), **GRAM(OKX 직접)**에서도 vol24h=volCcy24h 완전 동일값(1,732,450=1,732,450)이
처음 관찰됐다(1회차뿐, 재현 확인 필요). KAITO의 vol24h=volCcy24h 완전 동일 이상치도 3회차
연속 재현됐다. **HYNA:PUMP-USD·HYNA:HYPE-USD**는 이번 회차도 둘 다 별개 페어로 실존이
재확인됐으나, 여러 회차 동일값을 유지하던 HYNA:HYPE-USD의 OI가 이번 회차 처음
$726,354.04→$729,279.31(+0.4%)로 미세 변동해 스트릭이 깨졌다. 신규 발견: **CAP**이 이번
회차 처음 CoinGecko okex_swap 배열에서 확인됐고(직전까지 OrangeX·Aster 전용), **ALGO**도
Binance/Bybit에서 신규 확인돼 두 종목 모두 CEX 상장 범위가 넓어졌다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE (Fusionist)** [⚠️⚠️⚠️ 언락 하루 전 첫 광범위 냉각, OrangeX만 반대] | Binance/Bybit(가중) | $294.67M | $17.76M | -0.020% | +33.07% | 3거래소 첫 냉각인데 OrangeX만 OI +15.1% 급증·펀딩 플러스 전환 — 언락 하루 전 포지셔닝 크게 엇갈림 | unlock-eve-broad-cooling-except-orangex-oi-surges-funding-flips-positive |
| **BEAT** [⚠️ 첫 냉각 한 회차 만에 재반전] | OKX(CoinGecko 정상) | $277.12M | $9.97M | -0.026% | +36.236% | 3거래소 전부 재가속·OI 전부 재증가 — 냉각이 일시적이었음 확인. Bybit 9회차 연속 미확인 | cooling-reversed-reaccelerates-all-venues-oi-builds-again |
| **BICO** [재가속 2회차 연속] | OKX(CoinGecko 정상) | $466.85M | $17.79M | -0.173% | +21.466% | +12.542%→+21.466%, OrangeX OI +30.3% 큰 폭 증가 | reaccelerates-second-round-oi-builds-strongly-orangex |
| AAVE [냉각] | Binance/Bybit(거래량가중) | $41.50M | $90.15M | +0.005% | +1.72% | 직전 재가속이 한 회차 만에 꺾임, OI 거의 유지 | cools-after-single-round-reacceleration |
| **ALLO** [⚠️ 첫 마이너스 전환] | Binance/Bybit(거래량가중) | $41.40M | $19.54M | +0.005% | -0.66% | 3거래소 전부 동시 플러스→마이너스 반전 — 'OI 감소 속 가격 유지'가 결국 무너짐 | turns-negative-first-time-all-venues-simultaneously |
| ADA [2회차 연속 마이너스 유지] | Binance/Bybit(가중, USDT만) | $111.83M | $174.02M | +0.007% | -0.65% | 4회차 휩쏘 패턴이 '지속 마이너스'로 정착되는 모습 | whipsaw-pattern-settles-into-sustained-negative |
| **BANK** [⚠️ 개선 흐름 처음 꺾임] | Binance/Bybit(거래량가중) | $54.76M | $21.24M | +0.002% | -2.45% | -1.691%→-2.45% 악화, Aster만 개선으로 갈림 — 8/17 언락 약 8일 앞 | improvement-streak-breaks-mixed-across-venues |
| AKE [개선 2회차 연속] | Binance/Bybit(거래량가중) | $26.21M | $38.44M | +0.012% | -1.67% | Aster도 동조 개선, OrangeX만 소폭 악화 — 8/21 언락 약 12일 앞 | improves-second-round-orangex-diverges |
| **KAITO (CEX)** [가격 개선, OI 재증가 전환] | OKX(직접API) | $144.24M(계산값) | $7.61M | -0.654% | -13.029% | OI 2회차 감소 후 재증가, HL 펀딩은 더 악화 — 8/20 대형 언락 약 11일 앞 | price-continues-improving-oi-reverses-to-growth-funding-diverges-cross-venue |
| MMT [냉각 지속] | OKX(직접API) | $171.70M(계산값) | $3.79M | -0.028% | +5.969% | +8.121%→+5.969%, 펀딩 소폭 악화 | cools-further-oi-mildly-declines |
| GIGGLE [소폭 재가속] | OKX(직접API) | $24.45M(계산값) | $3.13M | +0.005% | +4.150% | ⚠️ 필드 순서 역전 3회차 연속 재현 | mild-reacceleration-field-order-anomaly-reproduced-third-round |
| PIPPIN [소폭 냉각] | OKX(직접API) | $1.80M(계산값) | $1.86M | +0.025% | +2.664% | OI -2.3% | mild-cooling-oi-declines-slightly |
| **1000RATS** [⚠️ 개선 재반전] | Binance/Bybit(거래량가중) | $9.16M | $18.34M | +0.005% | -4.69% | 2회차 연속 개선이 재반전, Aster는 더 큰 폭 악화 | improvement-streak-reverses-worsens-again |
| **AIO** [⚠️ 첫 마이너스 전환] | Binance/Bybit(거래량가중) | $12.43M | $4.76M | +0.005% | -1.90% | +2.774%→-1.90% | turns-negative-first-time |
| GRAM [소폭 추가 냉각] | OKX(직접API) | $2.35M(계산값) | $6.49M | +0.004% | +0.444% | HL은 반대로 소폭 확대. vol24h=volCcy24h 완전 동일값 신규 관찰 | mild-cooling-new-vol-field-identical-anomaly-observed-once |
| **AEON** [재가속 2회차 연속, 펀딩 반전] | OKX(CoinGecko 정상) | $21.89M | $4.62M | -0.009% | +18.767% | OKX·OrangeX 펀딩 플러스→마이너스 — 가격 급등에도 숏이 프리미엄 지불 | reaccelerates-second-round-funding-flips-negative-despite-surge |
| ATOM [소폭 냉각 지속] | Binance/Bybit(거래량가중) | $12.39M | $28.77M | +0.004% | +1.46% | +2.059%→+1.46% | holds-positive-mild-cooling-continues |
| ASTER (CEX) [가격 유지, 펀딩 마이너스 전환] | Binance/Bybit(거래량가중) | $15.75M | $113.65M | -0.052% | +0.35% | Bybit 펀딩(-0.029%)이 가중평균 끌어내림 | price-flat-funding-turns-negative-bybit-driven |
| CORE [초저유동성, 대체로 유지] | OKX(CoinGecko 정상) | $1.27M | $0.99M | +0.001% | +3.224% | +2.941%→+3.224% | low-liquidity-roughly-holds |
| BSB [재반전 없이 마이너스 심화] | OKX(CoinGecko 정상) | $24.64M | $3.02M | +0.005% | -3.234% | 왕복 휩쏘 이후 마이너스로 정착 중 | negative-persists-deepens-after-whipsaw-no-reversal |
| **CAP** [신규 확인] | OKX(CoinGecko 신규 확인) | $27.46M | $2.27M | +0.005% | +1.49% | 이번 회차 처음 okex_swap 배열에서 확인(직전까지 DEX 전용) | newly-confirmed-on-okx-cex |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [첫 냉각] | Hyperliquid | $5.11M | $2.04M | -0.029% | +31.565% | +40.037%→+31.565%, OI -5.3% | first-cooling-oi-declines |
| **ACE-USDT-PERPETUAL** [⚠️ OI 급증·펀딩 플러스 전환] | OrangeX | $159.11M | $68.60M | +0.01% | +35.448% | OI 59.62M→68.60M(+15.1%, 직전 -8.0% 반전) — 언락 하루 전 신규 롱 유입 재개 정황 | oi-surges-reverses-prior-decline-funding-flips-positive-pre-unlock |
| **ACE-USDT** [첫 냉각] | Aster | $0.66M | $0.08M | -0.024% | +35.881% | +38.216%→+35.881%, OI -4.5% | first-cooling-oi-declines-mildly |
| BLESS-USDT-PERPETUAL [추가 심화] | OrangeX | $199.18M | $58.79M | +0.063% | -17.978% | Aster도 동조 심화, OI -5.8% | extends-negative-further-oi-declines |
| BLESS-USDT [추가 심화] | Aster | $0.67M | $0.17M | +0.005% | -18.091% | -16.24%→-18.091% | extends-negative-further |
| **BICO-USDT-PERPETUAL** [재가속 2회차 연속] | OrangeX | $315.03M | $127.79M | -0.423% | +20.939% | OI 98.06M→127.79M(+30.3%) — 강한 신규 매수 | reaccelerates-second-round-oi-surges |
| **BICO-USDT** [재가속 지속] | Aster | $2.26M | $0.50M | +0.001% | +17.341% | OI +9.2% | reaccelerates-continues-oi-builds |
| **CASHCAT** [⚠️⚠️⚠️ 재가속 2회차, OI 갈림] | Hyperliquid | $11.78M | $19.44M | +0.023% | +32.507% | HL OI만 계속 증가, OrangeX·Aster는 감소 — 온체인 혼조 전환과 맞물릴 가능성 | reaccelerates-second-round-oi-diverges-hl-only-onchain-mixed-turn |
| CASHCAT-USDT-PERPETUAL [재가속, OI는 감소] | OrangeX | $0.15M | $0.06M | +0.021% | +30.427% | OI -9.9% — 3거래소 중 유일 역행 | reaccelerates-but-oi-declines |
| CASHCAT-USDT [재가속, OI 소폭 감소] | Aster | $1.34M | $1.52M | +0.001% | +32.672% | OI -2.0% | reaccelerates-oi-mildly-declines |
| **ALLO-USDT** [⚠️ 첫 마이너스 전환] | Aster | $0.23M | $0.04M | +0.001% | -1.378% | +3.449%→-1.378%, OI는 반대로 +3.9% | turns-negative-first-time-oi-ticks-up |
| **ALLO-USDT-PERPETUAL** [⚠️ 마이너스 전환, OI 3회차 연속 감소] | OrangeX | $28.15M | $10.10M | +0.01% | -0.958% | OI 3회차 연속 감소(-6.9%) | turns-negative-oi-declines-third-consecutive-round |
| AAVE-USDT-PERPETUAL [냉각] | OrangeX | $25.65M | $9.27M | +0.01% | +1.73% | OI 소폭 증가(+1.3%) | cools-oi-slightly-increases |
| AAVE-USDT [소폭 냉각] | Aster | $0.19M | $4.53M | +0.01% | +1.637% | OI 거의 유지 | mild-cooling-oi-flat |
| AAVE-USD [소폭 냉각] | Hyperliquid | $2.82M | $60.52M | +0.001% | +1.715% | OI 거의 유지 | mild-cooling-oi-flat |
| ADA-USDT-PERPETUAL [심화] | OrangeX | $56.98M | $21.10M | +0.01% | -0.802% | -0.498%→-0.802% | deepens-negative |
| ADA-USDT [소폭 개선] | Aster | $0.16M | $1.54M | +0.01% | -0.5% | 여전히 마이너스 | mild-improvement-stays-negative |
| ADA-USD [소폭 개선, 여전히 마이너스] | Hyperliquid | $1.83M | $33.20M | -0.001% | -0.61% | 4회차 휩쏘 미재현 흐름이 지속 마이너스로 정착 | mild-improvement-stays-negative-settles |
| **BEAT-USDT-PERPETUAL** [첫 냉각 재반전] | OrangeX | $15.56M | $5.92M | +0.01% | +35.635% | OI +12.5%로 재차 증가 | cooling-reversed-reaccelerates-oi-builds |
| **BEAT** [첫 냉각 재반전] | Aster | $4.97M | $5.77M | +0.006% | +36.678% | OI +6.1% | cooling-reversed-reaccelerates-oi-builds |
| BANK-USDT-PERPETUAL [소폭 악화] | OrangeX | $5.59M | $2.04M | +0.019% | -1.456% | OI +6.4% | mildly-worsens-oi-builds |
| BANK-USDT [개선] | Aster | $0.33M | $0.33M | +0.001% | -1.05% | -1.499%→-1.05% | improves |
| AKE-USDT-PERPETUAL [소폭 악화, 갈림] | OrangeX | $6.41M | $2.06M | +0.014% | -2.394% | CEX·Aster는 개선인데 OrangeX만 악화 | mildly-worsens-diverges-from-other-venues |
| AKE-USDT [개선 지속] | Aster | $0.36M | $10.67M | +0.011% | -1.798% | -2.744%→-1.798% | improves-continues |
| CAP-USDT [확대] | Aster | $0.07M | $0.10M | +0.001% | +3.295% | 이번 회차 OKX에서도 CAP 신규 확인 | extends-positive-newly-confirmed-on-cex-too |
| CAP [냉각] | OrangeX | $0.53M | $0.18M | +0.01% | +0.134% | +2.49%→+0.134%로 크게 둔화 | cools-sharply-diverges-in-magnitude |
| ALGO-USDT-PERPETUAL [소폭 심화] | OrangeX | $4.37M | $1.64M | +0.01% | -2.349% | 이번 회차 Binance/Bybit에서도 신규 확인 | mildly-deepens-newly-confirmed-on-binance-bybit-too |
| ALGO-USDT [대체로 유지] | Aster | $0.002M | $0.03M | -0.001% | -1.339% | 초저유동성 | roughly-holds-low-liquidity |
| ALGO-USD [소폭 심화] | Hyperliquid | $0.35M | $2.09M | +0.001% | -2.2% | -1.571%→-2.2% | mildly-deepens |
| ATOM-USDT-PERPETUAL [소폭 냉각, 펀딩 반전] | OrangeX | $6.17M | $2.29M | -0.01% | +1.467% | 펀딩 플러스→마이너스 | mild-cooling-funding-flips-negative |
| ATOM-USDT [플러스권 유지] | Aster | $0.01M | $1.60M | +0.01% | +1.99% | +2.216%→+1.99% | holds-positive-mild-cooling |
| ATOM-USD [플러스권 유지] | Hyperliquid | $0.31M | $1.93M | +0.001% | +1.496% | +2.312%→+1.496% | holds-positive-mild-cooling |
| ASTER-USDT-PERPETUAL [대체로 유지] | OrangeX | $6.24M | $2.10M | +0.01% | +0.368% | +0.434%→+0.368% | roughly-holds |
| ASTER-USDT [대형 OI 대체로 유지] | Aster | $8.29M | $219.39M | +0.017% | +0.366% | OI 거의 동일 | large-oi-roughly-holds |
| ASTER-USD [대체로 유지, 펀딩 소폭 마이너스] | Hyperliquid | $0.93M | $14.30M | -0.001% | +0.4% | +0.301%→+0.4% | roughly-holds-funding-turns-mildly-negative |
| **KAITO-USD** [가격 개선, 펀딩 더 악화, OI 재증가] | Hyperliquid | $24.72M | $18.61M | -0.334% | -12.54% | OI 2회차 감소 후 재증가 전환 — 8/20 대형 언락 약 11일 앞 | price-continues-improving-funding-worsens-more-oi-reverses-to-growth |
| GRAM-USD [소폭 확대, CEX와 갈림] | Hyperliquid | $0.42M | $13.01M | +0.001% | +0.577% | CEX(OKX)는 반대로 소폭 냉각 | mild-extension-cex-mild-cooling-diverges |
| HYPE-USD [플러스권 유지, 확대] | Hyperliquid | $85.42M | $1,205.13M | 0.0% | +1.819% | +1.466%→+1.819% | holds-positive-mild-extension |
| HYPER-USD [플러스권 확대] | Hyperliquid | $0.11M | $0.33M | +0.001% | +4.375% | +3.555%→+4.375% | extends-positive |
| APEX-USD [평탄으로 위축] | Hyperliquid | $0.09M | $0.78M | +0.001% | +0.078% | +0.678%→+0.078% | holds-positive-narrows-toward-flat |
| FARTCOIN [소폭 냉각, 플러스권 유지] | Hyperliquid | $3.01M | $22.19M | +0.006% | +3.849% | +4.584%→+3.849% | holds-positive-mild-cooling |
| **ETHFI-USD** [⚠️ 마이너스 전환] | Hyperliquid | $0.41M | $8.44M | +0.001% | -0.247% | +0.76%→-0.247% | turns-mildly-negative-from-positive |
| ETH-USD [방향성 부재 지속] | dYdX | $4.13M | $8.62M | 0.0% | +0.094% | 거래량·OI 대체로 유지 | oi-roughly-flat-still-no-clear-trend |
| BTC-USD [대체로 유지] | dYdX | $0.89M | $18.16M | -0.001% | +0.117% | 거래량·OI 거의 동일 | roughly-holds |
| SOL-USD [플러스권 유지, 소폭 냉각] | dYdX | $0.45M | $4.51M | 0.0% | +3.18% | +3.517%→+3.18% | holds-positive-mild-cooling |
| **ANSEM** [⚠️ 마이너스 전환] | Aster | $0.25M | $1.06M | +0.001% | -0.617% | +2.66%→-0.617% | turns-negative-from-positive |
| **BTW** [⚠️ 3회차 연속 심화] | Aster | $3.61M | $14.52M | +0.026% | -7.614% | OI도 계속 증가 — 프레시 숏 유입 지속 | deepens-third-consecutive-round-oi-continues-building |
| HYNA:PUMP-USD [별개 페어 실존, 확대] | Hyperliquid | $0.04M | $0.15M | +0.002% | +6.055% | +5.026%→+6.055% | separate-pair-confirmed-extends |
| **HYNA:HYPE-USD** [⚠️ OI 동일값 스트릭 깨짐] | Hyperliquid | $0.03M | $0.73M | -0.004% | +1.719% | $726,354.04→$729,279.31(+0.4%)로 여러 회차 만에 첫 변동 | oi-unchanged-streak-breaks-slight-increase |
| **AEON-USDT-PERPETUAL** [재가속 2회차, 펀딩 반전] | OrangeX | $0.48M | $0.19M | -0.01% | +18.279% | +14.789%→+18.279%, 펀딩 플러스→마이너스 | reaccelerates-second-round-funding-flips-negative |
| **AEON-USDT** [재가속 2회차] | Aster | $0.09M | $0.26M | +0.001% | +19.483% | +14.003%→+19.483% | reaccelerates-second-round |
| BSB-USDT-PERPETUAL [마이너스 심화] | OrangeX | $32.21M | $11.43M | +0.01% | -2.835% | 왕복 휩쏘 이후 심화 | negative-deepens-after-whipsaw |
| BSB-USDT [대체로 유지] | Aster | $0.26M | $0.12M | +0.001% | -3.135% | -3.303%→-3.135% | roughly-holds-negative |
| **1000RATS-USDT** [⚠️ 개선 재반전] | Aster | $0.07M | $0.04M | +0.009% | -5.344% | -2.402%→-5.344%로 큰 폭 악화 | improvement-reverses-worsens-sharply-cross-venue |

## 테마 태그

1. **시장 전반: `/global` 5회 연속 429로 확보 실패, WebSearch 참고용 스니펫 기준 총시총 약 $2.29T·BTC도미넌스 약 56.8%로 직전 회차 공식값과 유사한 수준 추정(정밀 비교 불가)** (global-api-failed-5x-websearch-fallback-approximate).
2. **Fear&Greed 31(Fear)로 직전 30에서 소폭 상승 — 12회차 연속 이어지던 30 고정이 이번 회차 처음 깨짐** (fear-greed-moves-to-31-breaks-twelve-round-plateau).
3. **⚠️⚠️⚠️ ACE(Fusionist): 8/10 언락 하루 전 Binance/Bybit·HL·Aster는 첫 광범위 냉각인데 OrangeX만 OI +15.1% 급증·펀딩 플러스 전환 — 언락 하루 전 거래소별 포지셔닝 크게 엇갈림** (ace-unlock-eve-broad-cooling-except-orangex-diverges).
4. **⚠️⚠️⚠️ CASHCAT: 재가속 2회차 연속이나 OI는 HL만 증가·OrangeX·Aster는 감소로 갈림 — 직전 온체인 루틴의 첫 혼조 전환과 맞물릴 가능성, 다음 회차 재확인 필요** (cashcat-reaccelerates-second-round-oi-diverges-onchain-mixed-turn).
5. **⚠️ BEAT(Audiera): 첫 냉각이 한 회차 만에 완전 재반전 — 3거래소 전부 재가속·OI 전부 재증가. Bybit 9회차 연속 미확인** (beat-cooling-reverses-reaccelerates-all-venues).
6. **KAITO: 가격 개선 지속, OI는 2회차 연속 감소 후 이번 회차 양쪽 모두 재증가로 전환하나 펀딩은 여전히(HL은 더) 악화 — 괴리 지속. 8/20 언락 약 11일 앞** (kaito-oi-reverses-to-growth-funding-still-diverges).
7. **⚠️ ALLO·AIO: 이번 회차 처음으로 플러스권에서 마이너스로 전환 — 여러 회차 이어지던 'OI 감소 속 가격 유지'가 결국 가격도 무너진 사례** (allo-aio-turn-negative-first-time-price-finally-follows-oi-decline).
8. **⚠️ 1000RATS: 2회차 연속 개선 흐름이 재반전돼 악화, Aster는 더 큰 폭 악화** (1000rats-improvement-reverses).
9. **AAVE·BANK: 직전 회차 개선·재가속 흐름이 한 회차 만에 꺾여 각각 냉각·악화(BANK는 Aster만 개선으로 갈림)** (aave-bank-single-round-trends-reverse).
10. **AEON·BICO: 2회차 연속 재가속 지속 — AEON은 OKX·OrangeX 펀딩이 플러스에서 마이너스로 전환돼 가격 급등에도 숏이 프리미엄을 지불하는 이례적 구도, BICO는 OrangeX OI +30.3% 급증** (aeon-bico-reaccelerate-second-round-aeon-funding-flips-negative).
11. **ADA: 2회차 연속 마이너스 유지 — 4회차 이어졌던 극단 휩쏘 패턴이 '지속 마이너스'로 정착되는 모습** (ada-whipsaw-pattern-settles-into-sustained-negative).
12. **⚠️ BTW: 3회차 연속 심화, OI도 계속 증가해 프레시 숏 유입 지속 정황 강화** (btw-deepens-third-round-oi-continues).
13. **BSB: 왕복 휩쏘 완성 이후 재반전 없이 마이너스 지속·심화 중** (bsb-negative-persists-no-reversal-after-whipsaw).
14. **⚠️ GIGGLE: vol24h/volCcy24h 필드 순서 역전이 3회차 연속 재현 — 구조적 패턴에 더 가까워짐. GRAM(OKX 직접)에서도 vol24h=volCcy24h 완전 동일값이 이번 회차 처음 관찰(1회차뿐, 재현 확인 필요)** (giggle-anomaly-third-round-gram-new-observation-once).
15. **KAITO의 vol24h=volCcy24h 완전 동일 이상치도 3회차 연속 재현 지속** (kaito-vol-fields-identical-anomaly-persists-third-round).
16. **HYNA:PUMP-USD·HYNA:HYPE-USD 이번 회차도 둘 다 별개 페어로 실존 재확인 — 다만 HYNA:HYPE-USD의 OI가 여러 회차 만에 처음 미세 변동(+0.4%)해 완전 동일값 유지 스트릭이 깨짐** (hyna-both-pairs-persist-oi-unchanged-streak-breaks).
17. **신규 발견: CAP이 이번 회차 처음 CoinGecko okex_swap 배열에서 확인(직전까지 OrangeX·Aster 전용), ALGO도 Binance/Bybit에서 신규 확인 — 두 종목 모두 CEX 상장 범위 확대 관찰** (cap-algo-newly-confirmed-on-additional-cex-venues).
18. **OKX ACE·BANK·1000RATS·AIO·KAITO·GIGGLE·MMT·PIPPIN·GRAM은 이번 회차도 CoinGecko okex_swap 배열에서 미등재, OKX 직접 API로 보강** (okx-several-symbols-still-not-listed).
19. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
20. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
21. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
22. **이번 회차 `/global`은 5회 연속 429로 확보 실패(직전 회차보다 심함), orangex_futures·dydx_chain은 429 이후 2차 시도로 확보, 나머지는 1~2차 시도로 정상 확보** (global-fails-5x-worse-than-prior-round-others-recovered).
23. **지금은 일요일 새벽(UTC 00:27) 시간대로 주말 유동성 저하가 일부 저유동성 종목 지표에 영향을 줬을 가능성 감안** (sunday-early-morning-liquidity-caveat).

## 데이터 신뢰도

**CoinGecko binance_futures**: 1차 시도로 정상 확보. ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·
ASTER·ALGO·1000RATS 확인(raw 값 직접). ALGO는 이번 회차 처음 CEX(Binance/Bybit)에서 확인.
직전 회차 확인됐던 소규모 BEATUSDT 리스팅은 이번 회차 데이터셋에서 재확인 안 됨(동일 자산
여부 애초에 불확실했던 이상치). BICO·GRAM·KAITO·MMT·PIPPIN·GIGGLE·BLESS·CASHCAT·BSB·CORE·
AEON·BTW·CAP·ETHFI·HYPE·HYPER·APEX·FARTCOIN·ANSEM은 Binance 미상장.

**CoinGecko bybit**: 1차 시도로 정상 확보. ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·
1000RATS 확인. **⚠️ BEAT는 이번 회차도 bybit 응답에서 미확인**(9회차 연속). BICO·KAITO·MMT·
PIPPIN·GIGGLE·BLESS·CASHCAT·BSB·CORE·AEON·BTW·CAP·ETHFI는 Bybit 미상장.

**CoinGecko okex_swap**: 1차 시도로 정상 확보. AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·
CAP·BEAT·BICO 확인. **신규**: CAP이 이번 회차 처음 okex_swap 배열에서 확인됐다(직전까지
OrangeX·Aster 전용 DEX 종목). ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN은 이번
회차도 okex_swap 티커 배열에서 미발견돼 OKX 직접 API 또는 Binance/Bybit로 대체 집계
(회차 간 일관성 유지).

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+`public/open-interest`
(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인. `oiUsd` 필드 직접 사용
방법론을 18회차 연속 유지, vol24_usd=`volCcy24h`×`last` 계산 방식도 유지. **⚠️ GIGGLE은
이번 회차도 vol24h(67,644,482)가 volCcy24h(676,444.82)보다 큰 역전된 필드 순서가 3회차 연속
재현**됐다. **KAITO는 vol24h=volCcy24h(200,974,272, 완전 동일) 이상치가 3회차 연속 재현**됐다.
**신규 관찰**: **GRAM**도 이번 회차 vol24h=volCcy24h(1,732,450, 완전 동일)로 확인됐다 — 1회차뿐
이라 구조적 패턴인지는 다음 회차 재현 여부로 판단해야 한다. 세 이상치 모두 계산 방식은 그대로
유지했다.

**Hyperliquid**: 1차 시도로 정상 확보. ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·
HYPER·APEX·FARTCOIN·ETHFI·ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD 등 raw 정밀값 확보. BICO·BEAT·
CAP·MMT·BANK·AEON·AKE·ALLO·BTW·BLESS는 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: 1차 시도로 정상 확보, raw 정밀 숫자로 직접 확보.
ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·BLESS·CASHCAT·BTW·ANSEM·AEON·ALGO·BEAT·
BSB·1000RATS 전량 확보. MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: 429 이후 2차 시도로 확보, raw 정밀값 직접 확보. ACE·AAVE·
ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·CAP·BLESS·CASHCAT·BSB 확인. KAITO·
1000RATS는 여전히 미발견.

**dYdX(`dydx_chain`)**: 429 이후 2차 시도로 확보, raw 정밀값(BTC-USD $0.89M/OI $18.16M,
ETH-USD $4.13M/OI $8.62M, SOL-USD $0.45M/OI $4.51M).

**CoinGecko `/global`**: **5회 연속 429로 확보 실패** — 이번 회차는 직접 API 기반 총시총·
도미넌스 수치를 갖지 못했다. 정직하게 미확인으로 표기하며, WebSearch 스니펫으로 참고용 근사치
(약 $2.29T·BTC도미넌스 약 56.8%)만 확보했다(서로 다른 소스라 직전 회차 공식값과의 정밀 비교는
불가).

**Fear&Greed**: alternative.me API로 1차 시도 정상 응답, **31(Fear)** 확인 — 직전 30에서
소폭 상승, 12회차 연속 이어지던 값이 이번 회차 처음 움직임.

**신규 발견**: ACE는 8/10 언락을 하루 앞두고 대부분 거래소에서 첫 냉각이 나타났으나 OrangeX만
OI 급증·펀딩 플러스 전환으로 반대 방향을 보여, 언락 직전 마지막 관측 구간에서 거래소별 포지셔닝
차이가 가장 뚜렷하게 드러났다. CASHCAT은 재가속이 지속됐지만 OI 뒷받침이 HL로 좁혀져, 3회
연속이던 온체인-선물 완전동조 패턴에 처음 균열 조짐이 보였다(확정 아님, 다음 회차 확인 필요).
ALLO·AIO·ANSEM·ETHFI 등 여러 종목이 이번 회차 처음 플러스에서 마이너스로 전환됐고, GIGGLE·
KAITO의 필드 이상치는 3회차 연속 재현으로 구조적 패턴에 더 가까워졌으며 GRAM에서도 유사
이상치가 처음 관찰됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접 조회분)의
CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를 직접 채택(회차
간 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS 등 복수 거래소 종목의
`chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은 이번 회차도 `why`·본문에
별도 표기했다; (e) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE·BSB는 Binance/Bybit에
상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며, 이는 데이터 누락이 아니라 실제 상장 현황이다;
(f) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·HYNA:HYPE-USD는 DEX에서만 상장이 확인돼 해당 섹션에서만
집계했다; (g) BEAT는 이번 회차도 bybit CoinGecko 티커에서 미확인됐는데(9회차 연속), 델리스팅
인지 일시적 API 응답 편차인지는 확정하지 않는다; (h) 직전 회차 확인됐던 Binance BEATUSDT
소규모 리스팅이 이번 회차 재확인되지 않아, 동일 자산 여부가 애초에 불확실했던 일시적 이상치일
가능성이 커졌다(확정 아님); (i) 이번 회차 급변에 대한 인과관계 해석(온체인-선물 리드-래그,
언락 직전 거래소별 포지셔닝 차이 등)은 대체로 정황상 추정이며 확정된 것은 아니다; (j) GIGGLE의
필드 순서 역전이 3회차 연속 재현됐고 GRAM에서도 유사 현상이 처음 관찰됐으나, 후자는 아직
1회차뿐이라 재현 여부 확인이 더 필요하다; (k) `/global`은 이번 회차 5회 연속 429로 실패해
WebSearch 근사치로만 대체했으며, 정밀한 회차 간 비교는 불가하다; (l) 지금은 일요일 새벽으로
유동성 저하가 일부 수치(특히 소규모 거래소·저유동성 종목)에 영향을 줬을 가능성이 있으며,
확정 불가.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
