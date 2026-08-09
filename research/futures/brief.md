# 선물시장 스카우트 브리핑 — 2026-08-09 02:31 UTC (KST 2026-08-09 11:31)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-09T00:27:00Z)
> 로부터 약 2시간 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`은 이번 회차도 2회 시도 모두 429로 확보 실패 — **6회 연속 실패**로 직전
회차(5회 연속)보다 더 길어졌다. WebSearch 참고용 스니펫은 총시총 약 **$2.29T**·BTC도미넌스 약
**56.8%**로 나왔으나 **직전 회차와 완전히 동일한 수치**라 검색결과가 캐시됐을 가능성이 있어
신뢰도를 낮게 잡고 참고용으로만 표기한다.

### Fear&Greed 31(Fear) — 직전 회차와 동일 유지

alternative.me API 정상 응답, **31(Fear)** — 직전 회차와 동일. 12회차 이어지던 30 고정이
직전 회차 깨진 뒤, 이번이 새 값(31)의 1회차 반복이다.

### 데이터 확보 상황

binance_futures·bybit·okex_swap·hyperliquid·dydx_chain은 1차 시도로 정상 확보됐고,
aster·orangex_futures는 1차 429 이후 2차 시도로 확보됐다. `/global`만 6회 연속 429로 확보
실패. OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)는 market/ticker+open-interest+funding-rate
개별조회로 **19회차 연속** 방법론(`oiUsd` 필드 직접 사용, `vol24_usd=volCcy24h×last`)을
유지해 확보했다.

지금은 **일요일 이른 아침**(UTC 02:31, KST 11:31) 시간대라 주말 유동성 저하가 일부 저유동성
종목 지표에 영향을 줬을 가능성을 감안해 서술한다.

## 직전 회차 강조 종목 추적 결과 (요청 항목 전체)

- **① ACE(Fusionist) — ⚠️⚠️⚠️ OrangeX의 반대 포지셔닝이 극적으로 청산·반전됐다.**
  Binance/Bybit(가중) +33.07%→**+31.57%**로 냉각 지속, HL도 +31.565%→**+31.199%**로 거의
  유지, Aster는 +35.881%→**+34.12%**로 소폭 냉각 — 세 거래소는 완만한 추가 냉각을 이어갔다.
  그런데 **OrangeX가 극적으로 반전됐다**: 직전 회차 OI +15.1%·펀딩 플러스 전환으로 유일하게
  반대 포지셔닝을 보였던 것이 이번 회차 완전히 청산됐다 — 가격 +35.448%→**+30.129%**로
  5.3%p 급락, OI $68.60M→**$58.24M(-15.1%)**로 직전 급증분을 거의 그대로 반납, 펀딩도
  +0.01%→**-0.06%**로 다시 마이너스 전환됐다. 언락 하루 전 유일하게 반대 매수하던 신규 롱이
  언락 직전 청산된 모습으로, 거래소 간 엇갈림이 결국 다수 거래소와 같은 방향(냉각)으로
  수렴됐다.
- **② CASHCAT — ⚠️⚠️⚠️ 재가속이 2회차 만에 멈추고 3거래소 전부 첫 냉각으로 전환됐다.**
  HL +32.507%→**+28.39%**, OrangeX +30.427%→**+27.285%**, Aster +32.672%→**+29.413%**로
  전부 냉각했다. OI는 HL만 $19.44M→**$19.77M(+1.7%)**로 계속 증가하나 증가폭이 크게
  둔화됐고(직전 +4.9%), OrangeX는 $60,079→**$55,682(-7.3%)**로 4회차 연속 감소, Aster도
  $1.52M→**$1.49M(-1.9%)**로 계속 감소 — **직전 회차 요청받은 '온체인 첫 혼조 전환을 선물이
  뒤따르는지'에 대한 답**: 이번 회차 선물이 처음으로 3거래소 전부 동시에 꺾여, 직전 온체인
  루틴이 관측한 h1 재음전·매도우위와 방향이 일치하는 결과가 나타났다. 리드-래그 관계가 이번
  회차에서 재확인되는 조짐으로 해석할 수 있다(확정 아님, 온체인 재확인 필요).
- **③ BEAT — 재가속이 2회차 연속 이어졌다.** OKX +36.236%→**+48.156%**, OrangeX
  +35.635%→**+48.226%**, Aster +36.678%→**+48.749%**로 3거래소 전부 큰 폭 재가속했다.
  Binance 소규모 BEATUSDT 리스팅도 이번 회차 재확인됐다(OI $4.76M·vol $0.41M·chg
  +47.485%) — 직전 회차 사라졌던 것이 다시 나타나 '델리스팅이 아니라 데이터셋 간헐 노출'일
  가능성이 커졌다. Bybit는 10회차 연속 미확인.
- **④ KAITO** — 가격 개선 추세가 이번 회차 처음 소폭 반전됐다. OKX -13.029%→**-13.827%**
  (악화), HL -12.54%→**-13.496%**(악화)로 두 거래소 모두 지금까지 이어지던 개선이 꺾였다.
  펀딩은 OKX -0.654%→**-0.661%**(소폭 악화), HL -0.334%→**-0.284%**(개선)로 두 거래소 펀딩
  격차가 좁혀졌다. OI는 OKX만 $7.61M→**$7.69M(+1.1%, 증가폭 둔화)**로 늘고 HL은
  $18.61M→**$17.96M(-3.5%)**로 다시 감소 전환 — 되돌림 조짐이 약해지는 모습. 8/20 대형 언락
  약 11일 앞.
- **⑤ BSB — ⚠️⚠️⚠️ 신규 주요 변화: 점진적 심화가 급락으로 질적 전환됐다.** OKX
  -3.234%→**-13.952%**, OrangeX -2.835%→**-16.784%**, Aster -3.135%→**-14.985%**로 3거래소
  전부 4~5배 폭으로 급락했다 — 지금까지의 '점진적 심화'와 질적으로 다른 급락이다. OI는 OKX
  $3.02M→**$2.88M(-4.8%)**로 소폭 감소, OrangeX는 $11.43M→**$10.37M(-9.3%)**로 감소, Aster는
  거의 유지 — 급락 폭에 비해 OI 변화는 상대적으로 크지 않아 기존 포지션 청산보다는 가격
  자체가 크게 눌린 모습으로 보인다.
- **⑥ BTW** — 4회차 연속 심화됐으나 OI 흐름이 처음 반전됐다. Aster -7.614%→**-15.24%**로
  낙폭이 약 두 배로 확대됐는데, OI는 $14.52M→**$13.84M(-4.7%)**로 3회차 연속 이어지던 증가가
  이번엔 감소로 전환됐다 — 프레시 숏 유입보다는 기존 포지션 청산 또는 숏 차익실현 가능성을
  시사하나 방향 해석은 확정 아니다.

## 이번 회차 그 외 주요 변화

⚠️ **AEON** 펀딩이 OKX·OrangeX 모두 이번 회차 다시 플러스로 전환(OKX -0.009%→**+0.005%**,
OrangeX -0.01%→**+0.01%**)돼, 직전 회차의 '가격 급등에도 숏이 프리미엄 지불' 이례 구도가
해소됐다(3회차 연속 재가속은 지속, +18.767%→**+18.88%/+19.425%**). **ALGO**는 이번 회차
Binance/Bybit 가중평균 데이터를 완전히 확보해 CEX 리스트에 정식 편입했다(vol $7.33M·OI
$14.91M·chg -0.99%). **AKE**는 3회차 연속 개선 끝에 이번 회차 마이너스에서 플러스로
전환됐다(**+0.27%**). **BANK**는 3회차 연속 심화됐고 펀딩도 플러스에서 마이너스로
전환됐다(-2.45%→**-3.98%**, 펀딩 +0.002%→**-0.031%**). **1000RATS**는 개선으로
재반전됐다(-4.69%→**-3.73%**). **AAVE**는 소폭 반등했다(+1.72%→+1.89%). **GIGGLE·KAITO**의
필드 이상치(vol24h/volCcy24h 역전·완전동일)는 이번 회차도 재현돼 각각 **4회차 연속**,
**GRAM**의 완전동일값 이상치도 **2회차 연속** 재현돼 세 종목 모두 구조적 패턴에 더
가까워졌다. **HYNA:HYPE-USD**의 OI는 직전 회차 처음 변동(+0.4%)한 뒤 이번 회차 다시 정확히
$729,279.31로 동일값을 유지해 '변동 후 재고정'되는 패턴을 보였다. **BICO**는 재가속
3회차 연속(21.5%→28.0%대)이나 OrangeX OI 증가폭이 +30.3%→**+0.85%**로 급격히 둔화됐다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| ACE (Fusionist) [냉각 지속, OrangeX 반전은 DEX 참조] | Binance/Bybit(가중) | $293.59M | $17.26M | -0.026% | +31.57% | 완만한 추가 냉각, DEX 섹션의 OrangeX 반전이 핵심 사건 | cooling-continues-into-unlock-window |
| **BEAT** [재가속 2회차 연속, 큰 폭] | OKX(CoinGecko 정상) | $319.34M | $11.79M | -0.029% | +48.156% | +36.236%→+48.156%, 전 거래소 큰 폭 재가속. Binance 소규모 리스팅 재확인. Bybit 10회차 연속 미확인 | reaccelerates-second-round-sharply-binance-listing-reappears |
| **BICO** [재가속 3회차 연속] | OKX(CoinGecko 정상) | $470.19M | $20.88M | -0.341% | +28.015% | OI+17.4%, OrangeX OI 증가폭은 +30.3%→+0.85%로 둔화 | reaccelerates-third-round-orangex-oi-growth-decelerates |
| **BSB** [⚠️⚠️⚠️ 신규 — 급락, 질적 전환] | OKX(CoinGecko 정상) | $23.91M | $2.88M | +0.005% | -13.952% | -3.234%→-13.952%, 3거래소 전부 4~5배 폭 급락, OI 변화는 상대적으로 작아 가격 자체 눌림 | sharp-selloff-new-major-move-all-venues |
| AAVE [소폭 반등] | Binance/Bybit(거래량가중) | $41.22M | $89.18M | +0.008% | +1.89% | +1.72%→+1.89% | mild-rebound-after-cooling |
| ALLO [2회차 연속 마이너스 심화] | Binance/Bybit(거래량가중) | $37.61M | $19.03M | +0.005% | -5.59% | -0.66%→-5.59%, OI 전 거래소 감소 전환 | negative-deepens-second-round-oi-declines-all-venues |
| ADA [3회차 연속 마이너스, 소폭 개선] | Binance/Bybit(가중, USDT만) | $111.69M | $174.06M | +0.009% | -0.3% | -0.65%→-0.3% | stays-negative-third-round-mild-improvement-mixed-venues |
| BANK [3회차 연속 심화, 펀딩 반전] | Binance/Bybit(거래량가중) | $55.96M | $20.24M | -0.031% | -3.98% | -2.45%→-3.98%, 펀딩 플러스→마이너스. 8/17 언락 약 8일 앞 | deepens-third-consecutive-round-funding-flips-negative |
| **AKE** [⚠️ 3회차 연속 개선 끝 플러스 전환] | Binance/Bybit(거래량가중) | $26.72M | $39.04M | +0.013% | +0.27% | -1.67%→+0.27%. 8/21 언락 약 12일 앞 | turns-positive-after-third-round-improvement |
| KAITO [⚠️ 개선 첫 반전] | OKX(직접API) | $149.40M(계산값) | $7.69M | -0.661% | -13.827% | -13.029%→-13.827%로 악화, OI 증가폭 둔화. 8/20 대형 언락 약 11일 앞 | improvement-trend-reverses-first-time-oi-growth-decelerates |
| MMT [냉각 크게 심화] | OKX(직접API) | $174.17M(계산값) | $3.82M | -0.048% | +1.066% | +5.969%→+1.066% | cooling-sharply-intensifies |
| GIGGLE [재가속] | OKX(직접API) | $25.83M(계산값) | $3.06M | +0.005% | +10.367% | +4.150%→+10.367%. ⚠️ 필드 순서 역전 4회차 연속 재현 | reaccelerates-field-order-anomaly-reproduced-fourth-round |
| PIPPIN [소폭 재가속] | OKX(직접API) | $1.82M(계산값) | $1.88M | +0.026% | +2.933% | OI +1.3% | mild-reacceleration-oi-builds-slightly |
| 1000RATS [개선 재반전] | Binance/Bybit(거래량가중) | $9.06M | $18.33M | +0.020% | -3.73% | -4.69%→-3.73% | worsening-reverses-improves-again |
| AIO [2회차 연속 마이너스 심화] | Binance/Bybit(거래량가중) | $11.95M | $4.57M | +0.005% | -5.35% | -1.90%→-5.35% | negative-deepens-second-round |
| GRAM [추가 냉각] | OKX(직접API) | $2.49M(계산값) | $6.48M | +0.005% | +0.148% | +0.444%→+0.148%. ⚠️ vol 필드 동일값 이상치 2회차 연속 재현 | cools-further-vol-field-identical-anomaly-reproduced-second-round |
| **AEON** [재가속 3회차, 펀딩 정상화] | OKX(CoinGecko 정상) | $27.91M | $4.48M | +0.005% | +18.88% | 펀딩 마이너스→플러스로 전환돼 '숏이 프리미엄 지불' 이례 구도 해소 | reaccelerates-third-round-funding-normalizes-positive |
| ATOM [냉각 지속] | Binance/Bybit(거래량가중) | $11.86M | $28.65M | +0.009% | +0.84% | +1.46%→+0.84% | cooling-continues |
| ASTER [소폭 마이너스, 펀딩 반전] | Binance/Bybit(거래량가중) | $16.38M | $113.24M | +0.004% | -0.10% | +0.35%→-0.10%, 펀딩 -0.052%→+0.004% | turns-mildly-negative-funding-flips-positive |
| CORE [초저유동성, 소폭 냉각] | OKX(CoinGecko 정상) | $1.35M | $0.96M | +0.007% | +2.382% | +3.224%→+2.382% | low-liquidity-mild-cooling |
| CAP [2회차 연속 OKX 확인] | OKX(CoinGecko 정상) | $25.51M | $2.31M | +0.005% | +1.786% | +1.49%→+1.786% | confirmed-second-round-roughly-holds |
| **ALGO** [신규 — CEX 정식 편입] | Binance/Bybit(거래량가중) | $7.33M | $14.91M | -0.001% | -0.989% | 이번 회차 처음 가중평균 데이터 완전 확보, 전 거래소 마이너스로 방향 일치 | newly-tracked-with-full-weighted-cex-data |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| ACE-USD [냉각 지속] | Hyperliquid | $5.28M | $2.09M | -0.034% | +31.199% | 거의 유지 | cooling-continues-roughly-holds |
| **ACE-USDT-PERPETUAL** [⚠️⚠️⚠️ 반대 포지셔닝 완전 청산] | OrangeX | $152.80M | $58.24M | -0.06% | +30.129% | OI -15.1%(직전 급증 반납), 펀딩 재차 마이너스 — 언락 하루 전 유일 반대매수 청산 | contrarian-position-fully-unwound-pre-unlock |
| ACE-USDT [냉각 지속] | Aster | $0.68M | $0.08M | -0.032% | +34.12% | 거의 유지 | cooling-continues |
| **BEAT-USDT-PERPETUAL** [재가속 2회차, 큰 폭] | OrangeX | $17.43M | $6.81M | +0.014% | +48.226% | OI +15.1%로 계속 증가 | reaccelerates-second-round-sharply-oi-builds |
| **BEAT** [재가속 2회차, 큰 폭] | Aster | $5.03M | $6.20M | +0.003% | +48.749% | OI +7.6% | reaccelerates-second-round-sharply-oi-builds |
| **BICO-USDT-PERPETUAL** [재가속 3회차, OI 둔화] | OrangeX | $307.94M | $128.88M | -0.547% | +25.893% | OI 증가폭 +30.3%→+0.85%로 둔화 | reaccelerates-third-round-oi-growth-decelerates |
| BICO-USDT [재가속 지속] | Aster | $2.41M | $0.54M | +0.001% | +25.709% | OI +9.2% | reaccelerates-continues-oi-builds |
| **CASHCAT** [⚠️⚠️⚠️ 첫 냉각, 3거래소 동시] | Hyperliquid | $12.23M | $19.77M | +0.014% | +28.39% | 재가속 멈추고 첫 냉각 — 직전 온체인 첫 혼조 전환과 방향 일치 | first-cooling-all-venues-aligns-with-onchain-mixed-turn |
| CASHCAT-USDT-PERPETUAL [냉각, OI 4회차 감소] | OrangeX | $0.15M | $0.06M | +0.01% | +27.285% | OI -7.3% | cools-oi-declines-fourth-consecutive-round |
| CASHCAT-USDT [냉각, OI 계속 감소] | Aster | $1.44M | $1.49M | -0.034% | +29.413% | OI -1.9% | cools-oi-continues-declining |
| ALLO-USDT [심화, OI 감소 전환] | Aster | $0.20M | $0.04M | +0.001% | -6.049% | -1.378%→-6.049% | deepens-oi-turns-to-decline |
| ALLO-USDT-PERPETUAL [심화, OI 4회차 감소] | OrangeX | $25.95M | $9.42M | +0.01% | -5.335% | OI -6.7% | deepens-oi-declines-fourth-consecutive-round |
| AAVE-USDT-PERPETUAL [소폭 확대] | OrangeX | $25.57M | $7.94M | +0.01% | +1.904% | +1.73%→+1.904% | extends-slightly-oi-declines |
| AAVE-USDT [소폭 확대] | Aster | $0.18M | $4.54M | +0.01% | +1.803% | 거의 유지 | extends-slightly-oi-flat |
| AAVE-USD [소폭 냉각] | Hyperliquid | $2.83M | $60.32M | +0.001% | +1.648% | 거의 유지 | mild-cooling-oi-flat |
| ADA-USDT-PERPETUAL [개선] | OrangeX | $57.98M | $19.89M | +0.01% | -0.500% | -0.802%→-0.5% | improves |
| ADA-USDT [소폭 악화] | Aster | $0.13M | $1.55M | +0.01% | -0.846% | -0.5%→-0.846% | mildly-worsens |
| ADA-USD [소폭 악화] | Hyperliquid | $1.76M | $33.35M | -0.002% | -0.682% | -0.61%→-0.682% | mildly-worsens-oi-ticks-up |
| BANK-USDT-PERPETUAL [심화] | OrangeX | $5.82M | $1.93M | +0.012% | -3.563% | -1.456%→-3.563% | deepens |
| BANK-USDT [개선에서 심화로 반전] | Aster | $0.39M | $0.36M | -0.006% | -3.575% | -1.05%→-3.575% | improvement-reverses-worsens |
| **AKE-USDT-PERPETUAL** [⚠️ 플러스 전환] | OrangeX | $6.31M | $2.34M | +0.01% | +0.594% | -2.394%→+0.594% | turns-positive |
| **AKE-USDT** [⚠️ 플러스 전환] | Aster | $0.31M | $10.96M | +0.011% | +0.381% | -1.798%→+0.381% | turns-positive |
| CAP-USDT [소폭 냉각] | Aster | $0.07M | $0.10M | +0.001% | +2.631% | +3.295%→+2.631% | mild-cooling |
| CAP [재가속] | OrangeX | $0.52M | $0.18M | +0.01% | +1.321% | +0.134%→+1.321% | reaccelerates |
| ALGO-USDT-PERPETUAL [소폭 개선] | OrangeX | $4.44M | $1.58M | -0.01% | -1.019% | -2.349%→-1.019% | mild-improvement |
| ALGO-USDT [소폭 심화, 초저유동성] | Aster | $0.002M | $0.03M | +0.001% | -1.97% | -1.339%→-1.97% | mildly-deepens-low-liquidity |
| ALGO-USD [개선] | Hyperliquid | $0.36M | $2.09M | +0.001% | -1.129% | -2.2%→-1.129% | improves |
| ATOM-USDT-PERPETUAL [소폭 냉각] | OrangeX | $5.98M | $2.10M | +0.01% | +0.878% | +1.467%→+0.878% | mild-cooling |
| ATOM-USDT [소폭 냉각, 플러스권 유지] | Aster | $0.02M | $1.60M | +0.01% | +1.175% | +1.99%→+1.175% | holds-positive-mild-cooling |
| ATOM-USD [소폭 냉각, 플러스권 유지] | Hyperliquid | $0.30M | $1.92M | +0.001% | +1.009% | +1.496%→+1.009% | holds-positive-mild-cooling |
| ASTER-USDT-PERPETUAL [평탄으로 전환] | OrangeX | $6.46M | $2.33M | +0.01% | -0.017% | +0.368%→-0.017% | narrows-toward-flat-turns-mildly-negative |
| ASTER-USDT [대형 OI 유지, 마이너스 전환] | Aster | $8.78M | $218.93M | +0.013% | -0.066% | OI 거의 동일 | large-oi-roughly-holds-turns-mildly-negative |
| ASTER-USD [마이너스 전환] | Hyperliquid | $0.94M | $14.27M | -0.001% | -0.081% | +0.4%→-0.081% | turns-negative |
| **KAITO-USD** [⚠️ 개선 첫 반전, OI 재감소] | Hyperliquid | $26.38M | $17.96M | -0.284% | -13.496% | -12.54%→-13.496%, OI 재증가 뒤 다시 감소. 8/20 대형 언락 약 11일 앞 | improvement-trend-reverses-oi-declines-again |
| GRAM-USD [크게 냉각, CEX와 일치] | Hyperliquid | $0.39M | $12.91M | +0.001% | +0.052% | +0.577%→+0.052% | cools-sharply-aligns-with-cex |
| HYPE-USD [플러스권 확대] | Hyperliquid | $82.45M | $1,206.98M | +0.001% | +2.07% | +1.819%→+2.07% | holds-positive-extends |
| HYPER-USD [냉각, 플러스권 유지] | Hyperliquid | $0.11M | $0.32M | +0.001% | +2.569% | +4.375%→+2.569% | cools-holds-positive |
| APEX-USD [⚠️ 마이너스 전환] | Hyperliquid | $0.10M | $0.77M | +0.001% | -0.363% | +0.078%→-0.363% | turns-negative |
| FARTCOIN [소폭 냉각, 플러스권 유지] | Hyperliquid | $3.00M | $22.24M | +0.005% | +3.272% | +3.849%→+3.272% | holds-positive-mild-cooling |
| ETHFI-USD [⚠️ 플러스 재전환] | Hyperliquid | $0.40M | $8.39M | +0.001% | +0.487% | -0.247%→+0.487% | turns-positive-again |
| ETH-USD [방향성 부재 지속] | dYdX | $3.66M | $8.61M | 0.0% | +0.042% | 거래량·OI 대체로 유지 | oi-roughly-flat-still-no-clear-trend |
| BTC-USD [대체로 유지] | dYdX | $0.93M | $18.09M | 0.0% | -0.145% | 거의 동일 | roughly-holds-mildly-negative |
| SOL-USD [플러스권 유지] | dYdX | $0.43M | $4.51M | 0.0% | +2.678% | +3.18%→+2.678% | holds-positive |
| ANSEM [평탄으로 회복] | Aster | $0.26M | $1.06M | +0.001% | +0.292% | -0.617%→+0.292% | recovers-toward-flat |
| **BTW** [⚠️ 4회차 연속 심화, OI 첫 감소] | Aster | $3.46M | $13.84M | +0.031% | -15.24% | 낙폭 두 배 확대(-7.614%→-15.24%), OI 3회차 증가에서 이번 처음 감소 전환 | deepens-fourth-round-oi-declines-first-time |
| HYNA:PUMP-USD [별개 페어 지속, 확대] | Hyperliquid | $0.04M | $0.16M | +0.001% | +7.706% | +6.055%→+7.706% | separate-pair-confirmed-extends |
| **HYNA:HYPE-USD** [⚠️ 변동 후 재고정] | Hyperliquid | $0.03M | $0.73M | -0.004% | +1.981% | $729,279.31로 정확히 동일값 재유지 | resettles-at-new-value-after-single-change |
| **AEON-USDT-PERPETUAL** [재가속 3회차, 펀딩 정상화] | OrangeX | $0.49M | $0.18M | +0.01% | +19.425% | 펀딩 -0.01%→+0.01% | reaccelerates-third-round-funding-normalizes |
| AEON-USDT [3회차 강세 유지] | Aster | $0.08M | $0.27M | +0.007% | +18.882% | +19.483%→+18.882% | holds-strong-third-round-mild-cooling |
| **BSB-USDT-PERPETUAL** [⚠️⚠️⚠️ 급락, 신규 최대 낙폭] | OrangeX | $31.08M | $10.37M | +0.01% | -16.784% | -2.835%→-16.784% | sharp-selloff-new-max-decline |
| **BSB-USDT** [⚠️⚠️⚠️ 급락] | Aster | $0.25M | $0.11M | +0.001% | -14.985% | -3.135%→-14.985% | sharp-selloff |
| 1000RATS-USDT [악화 지속] | Aster | $0.03M | $0.05M | +0.016% | -3.858% | -5.344%→-3.858%(소폭 개선이나 CEX 대비 큰 낙폭) | remains-negative-mild-improvement |

## 테마 태그

1. **시장 전반: `/global` 6회 연속 429로 확보 실패(직전 5회보다 길어짐), WebSearch 스니펫은 직전 회차와 완전 동일 수치라 캐시 가능성 있어 신뢰도 낮게 표기** (global-api-failed-6x-websearch-possibly-cached).
2. **Fear&Greed 31(Fear)로 직전 회차와 동일 유지 — 12회차 30 고정이 깨진 뒤 새 값의 1회차 반복** (fear-greed-holds-31-first-repeat-of-new-value).
3. **⚠️⚠️⚠️ ACE(Fusionist): 언락 하루 이내 앞두고 OrangeX의 반대 포지셔닝(OI+15.1%·펀딩플러스)이 완전히 청산·반전 — 거래소 간 엇갈림이 냉각 방향으로 수렴** (ace-orangex-contrarian-position-fully-unwound-pre-unlock).
4. **⚠️⚠️⚠️ CASHCAT: 재가속 2회차 만에 멈추고 3거래소 전부 첫 냉각 — 직전 회차 온체인 첫 혼조 전환과 방향 일치, 리드-래그 재확인 조짐(확정 아님)** (cashcat-first-cooling-all-venues-aligns-with-onchain-mixed-turn).
5. **BEAT(Audiera): 재가속 2회차 연속·큰 폭 확대(36%→48%대), Binance 소규모 리스팅 재확인. Bybit 10회차 연속 미확인** (beat-reaccelerates-second-round-binance-listing-reappears).
6. **BICO: 재가속 3회차 연속(21%→28%대), OrangeX OI 증가폭 +30.3%→+0.85%로 급격 둔화** (bico-reaccelerates-third-round-oi-growth-decelerates).
7. **⚠️⚠️⚠️ BSB: 신규 최대 사건 — 점진적 심화가 급락으로 질적 전환, 3거래소 전부 -3%대→-14~17%대로 4~5배 확대. OI 변화는 상대적으로 작아 가격 자체 눌림 가능성** (bsb-sharp-selloff-qualitative-shift-new-major-move).
8. **KAITO: 가격 개선 추세가 처음 반전(악화), OI도 재차 감소 전환 — 되돌림 조짐 약화. 8/20 대형 언락 약 11일 앞** (kaito-improvement-trend-reverses-first-time).
9. **AEON: 재가속 3회차 연속 지속, 펀딩이 OKX·OrangeX 모두 다시 플러스로 전환돼 이례 구도 해소** (aeon-reaccelerates-funding-normalizes-positive).
10. **AKE: 3회차 연속 개선 끝에 마이너스에서 플러스로 전환** (ake-turns-positive-after-third-round-improvement).
11. **BANK: 3회차 연속 심화, 펀딩도 플러스에서 마이너스로 전환** (bank-deepens-third-round-funding-flips-negative).
12. **⚠️ BTW: 4회차 연속 심화·낙폭 두 배 확대인데 OI는 처음 감소로 전환 — 청산·차익실현 가능성(확정 아님)** (btw-deepens-fourth-round-oi-turns-to-decline-first-time).
13. **ALGO: 이번 회차 Binance/Bybit 가중평균 데이터를 완전 확보해 CEX 리스트에 정식 편입** (algo-newly-tracked-full-weighted-cex-data).
14. **1000RATS·AAVE: 각각 개선 재반전·소폭 반등** (1000rats-aave-mild-reversals-improve).
15. **⚠️ GIGGLE·KAITO: 필드 이상치(순서 역전·완전동일)가 이번 회차도 재현돼 각각 4회차 연속. GRAM 이상치도 2회차 연속 재현 — 세 종목 모두 구조적 패턴에 더 가까워짐** (giggle-kaito-gram-field-anomalies-reproduced-fourth-second-round).
16. **HYNA:HYPE-USD: 직전 회차 처음 OI가 변동한 뒤 이번 회차 다시 정확히 동일값으로 재고정** (hyna-hype-resettles-at-new-fixed-value).
17. **OKX ACE·BANK·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN은 이번 회차도 CoinGecko okex_swap 배열에서 미등재, OKX 직접 API로 보강. BEAT·BICO는 이번 회차 okex_swap에서 정상 확인됨** (okx-most-still-not-listed-beat-bico-confirmed).
18. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
19. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
20. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
21. **이번 회차 `/global`은 6회 연속 429로 확보 실패(직전보다 길어짐), aster·orangex_futures는 1차 429 이후 2차 시도로 확보, 나머지는 1차 시도로 정상 확보** (global-fails-6x-others-recovered-quickly).
22. **지금은 일요일 이른 아침(UTC 02:31) 시간대로 주말 유동성 저하가 일부 저유동성 종목 지표에 영향을 줬을 가능성 감안** (sunday-early-morning-liquidity-caveat).

## 데이터 신뢰도

**CoinGecko binance_futures**: 1차 시도로 정상 확보. ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·
ASTER·ALGO·1000RATS·BEAT(소규모 리스팅 재확인, vol $407,960·OI $4.76M) 확인. BICO·GRAM·
KAITO·MMT·PIPPIN·GIGGLE·BLESS·CASHCAT·BSB·CORE·AEON·BTW·CAP·ETHFI·HYPE·HYPER·APEX·
FARTCOIN·ANSEM은 Binance 미상장.

**CoinGecko bybit**: 1차 시도로 정상 확보. ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·
1000RATS 확인. **⚠️ BEAT는 이번 회차도 bybit 응답에서 미확인**(10회차 연속). BICO·KAITO·
MMT·PIPPIN·GIGGLE·BLESS·CASHCAT·BSB·CORE·AEON·BTW·CAP·ETHFI는 Bybit 미상장.

**CoinGecko okex_swap**: 1차 시도로 정상 확보. AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·
CAP·BEAT·BICO 확인 — **BEAT·BICO가 이번 회차 정상 확인됨**(직전까지도 확인돼왔음, 값 재확인).
ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN은 이번 회차도 okex_swap 배열에서 미발견돼
OKX 직접 API 또는 Binance/Bybit로 대체 집계(회차 간 일관성 유지).

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+`public/open-interest`
(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인. `oiUsd` 필드 직접 사용
방법론을 19회차 연속 유지, vol24_usd=`volCcy24h`×`last` 계산 방식도 유지. **⚠️ GIGGLE**은
이번 회차도 vol24h(71,166,484)가 volCcy24h(711,664.84)보다 큰 역전된 필드 순서가 **4회차
연속** 재현됐다. **KAITO**는 vol24h=volCcy24h(213,861,542, 완전 동일) 이상치가 **4회차 연속**
재현됐다. **GRAM**도 이번 회차 vol24h=volCcy24h(1,846,824, 완전 동일)로 **2회차 연속**
재현돼 구조적 패턴에 더 가까워졌다. 세 이상치 모두 계산 방식은 그대로 유지했다.

**Hyperliquid**: 1차 시도로 정상 확보. ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·
HYPER·APEX·FARTCOIN·ETHFI·ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD 등 raw 정밀값 확보. BICO·BEAT·
CAP·MMT·BANK·AEON·AKE·ALLO·BTW·BLESS·ANSEM은 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: 1차 429 이후 2차 시도로 확보, raw 정밀 숫자로
직접 확보. ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·BLESS·CASHCAT·BTW·ANSEM·AEON·
ALGO·BEAT·BSB·1000RATS 전량 확보. MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히
미발견.

**OrangeX(`orangex_futures`)**: 1차 429 이후 2차 시도로 확보, raw 정밀값 직접 확보. ACE·
AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·CAP·BLESS·CASHCAT·BSB 확인.
KAITO·1000RATS는 여전히 미발견.

**dYdX(`dydx_chain`)**: 1차 시도로 정상 확보, raw 정밀값(BTC-USD $0.93M/OI $18.09M,
ETH-USD $3.66M/OI $8.61M, SOL-USD $0.43M/OI $4.51M).

**CoinGecko `/global`**: **6회 연속 429로 확보 실패** — 이번 회차도 직접 API 기반 총시총·
도미넌스 수치를 갖지 못했다. WebSearch 스니펫이 직전 회차와 완전 동일한 수치($2.29T·56.8%)로
나와 캐시된 결과일 가능성이 있어, 정직하게 미확인으로 표기하고 참고용으로만 남긴다.

**Fear&Greed**: alternative.me API로 1차 시도 정상 응답, **31(Fear)** 확인 — 직전 회차와
동일 유지.

**신규 발견**: ACE는 언락을 하루 이내 앞두고 OrangeX의 반대 포지셔닝(OI 급증·펀딩 플러스)이
이번 회차 완전히 청산·반전돼, 지금까지의 거래소 간 엇갈림이 냉각 방향으로 수렴됐다. CASHCAT은
재가속이 멈추고 3거래소 전부 첫 냉각으로 전환돼, 직전 회차 온체인 루틴이 관측한 첫 혼조
전환과 방향이 일치하는 결과가 나왔다(리드-래그 재확인 조짐, 확정 아님). BSB는 점진적
심화에서 급락으로 질적 전환된 신규 최대 사건이다. KAITO는 개선 추세가 처음 반전됐다. BEAT는
2회차 연속 큰 폭 재가속, BICO는 3회차 연속 재가속하되 OrangeX OI 증가폭이 급격히 둔화됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접 조회분)의
CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를 직접 채택(회차
간 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·ALGO 등 복수 거래소
종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은 이번 회차도
`why`·본문에 별도 표기했다; (e) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE·BSB는
Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며, 이는 데이터 누락이 아니라
실제 상장 현황이다; (f) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·HYNA:HYPE-USD는 DEX에서만 상장이
확인돼 해당 섹션에서만 집계했다; (g) BEAT는 이번 회차도 bybit CoinGecko 티커에서
미확인됐는데(10회차 연속), 델리스팅인지 일시적 API 응답 편차인지는 확정하지 않는다; (h) BSB의
이번 회차 급락은 3거래소 동시 발생으로 데이터 오류 가능성은 낮으나, 급락 배경(뉴스·촉매)은
별도 확인하지 않았다; (i) 이번 회차 급변에 대한 인과관계 해석(온체인-선물 리드-래그, 언락
직전 거래소별 포지셔닝 청산 등)은 대체로 정황상 추정이며 확정된 것은 아니다; (j) GIGGLE·
KAITO의 필드 이상치가 4회차 연속, GRAM도 2회차 연속 재현돼 구조적 패턴에 가까워졌으나 근본
원인(OKX API 자체 특성인지)은 규명하지 않았다; (k) `/global`은 이번 회차 6회 연속 429로
실패했고 WebSearch 근사치도 직전 회차와 동일해 캐시 가능성이 있어, 이번 회차는 총시총·
도미넌스 수치를 사실상 갖지 못한 것으로 간주해야 한다; (l) 지금은 일요일 이른 아침으로
유동성 저하가 일부 수치(특히 소규모 거래소·저유동성 종목)에 영향을 줬을 가능성이 있으며,
확정 불가.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
