# 선물시장 스카우트 브리핑 — 2026-08-09 06:29 UTC (KST 2026-08-09 15:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-09T04:29:00Z)
> 로부터 정확히 2시간 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`은 이번 회차도 429로 확보 실패 — **8회 연속 실패**로 계속 길어지고 있다.
WebSearch 참고 수치는 이번엔 총시총 약 **$2.29T**·BTC도미넌스 약 **56.8%**로, 직전 회차의
**$2.21T·58.88%**와 다시 달라졌다. 두 값이 회차마다 오락가락하는 것은 WebSearch 스니펫이
실시간 반영이 아니라 검색엔진 캐시 스냅샷일 가능성을 시사한다 — 직전 회차엔 '캐시 아닐
가능성'으로 평가했으나 이번 회차 반전으로 신뢰도를 다시 낮춰 표기한다.

### Fear&Greed 31(Fear) — 4회차 연속 동일값

alternative.me API 정상 응답, **31(Fear)** — 4회차 연속 동일값 유지.

### 데이터 확보 상황

binance_futures·bybit·hyperliquid·aster는 1차 시도로 정상 확보됐으나, **okex_swap·
orangex_futures·dydx_chain은 각각 2~4차 재시도 끝에 확보**됐다 — CoinGecko 429가 직전
회차보다 전반적으로 심화된 정황이다. OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)는
**21회차 연속** 방법론(`oiUsd` 필드 직접 사용, `vol24_usd=volCcy24h×last`)을 유지해 확보했다.

지금은 **일요일 저녁**(UTC 06:29, KST 15:29) 시간대다.

## 직전 회차 강조 종목 추적 결과 (요청 항목 전체)

- **① ACE(Fusionist) — 언락 반나절 이내로 임박, 4거래소 2회차 연속 냉각이나 폭은 크게
  축소.** 언락(8/10 00:00 UTC 추정, 공급 1.2%)이 이제 반나절 이내로 다가와 이번이 사실상
  언락 직전 마지막 관측치다. Binance/Bybit(가중) **+19.84%→+17.14%**, OrangeX
  **+19.78%→+18.95%**, Aster **+20.97%→+17.88%**, HL **+19.49%→+16.38%**로 4거래소 전부
  2회차 연속 냉각했으나, 직전 회차의 10%p+ 동시냉각과 달리 이번은 2~4%p 수준으로 강도가
  뚜렷이 완화됐다. OI는 Binance/Bybit -4.2%·OrangeX -10.6%($53.83M→$48.14M)·HL -3.0%로
  계속 감소한 반면 **Aster만 +13.7%**($72,373→$82,252)로 반등해 방향이 완전히 일치하진
  않았다.
- **② BTW — 반전이 유지되는 데 그치지 않고 확장됐다.** Aster **+8.897%→+16.288%**로
  플러스권을 더 넓혔다. 다만 OI는 **$14.68M→$13.04M(-11.2%)**로 오히려 감소해, 가격 상승이
  신규 롱 유입보다는 숏 커버링 후 잔존 포지션 축소에 가까울 수 있다(확정 아님). WebSearch로
  확인한 배경: 6월 Gate.io·Binance 선물 상장, Binance Wallet 부스터 시즌3 등 유동성 이벤트가
  이어지고 있다.
- **③ BEAT·BICO** — '냉각 지속 여부' 확인 결과 예상과 달리 둘 다 재반전됐다. **BEAT**는 OKX
  **+31.545%→+47.998%**로 직전 냉각을 완전히 되돌리며 3회차째 재가속(36%대→48%대→31%대
  →48%대 요요 패턴), OrangeX(+31.071%→**+42.384%**)·Aster(+30.776%→**+42.898%**)도 동조,
  OI도 OKX **$9.26M→$11.45M(+23.7%)**로 급증했다. **BICO**는 OKX(+18.58%→**+20.069%**)·
  OrangeX(+17.04%→**+20.0%**)가 소폭 재가속했으나 Aster는 오히려 +18.805%→**+14.489%**로
  계속 냉각해 거래소 간 방향이 갈렸다. Binance BEATUSDT는 이번 회차도 미확인, Bybit BEAT는
  **12회차 연속** 미확인.
- **④ BSB** — 안정화가 뚜렷이 굳어졌다: OKX **-9.444%→-2.226%**, OrangeX
  **-9.016%→-1.657%**, Aster **-8.506%→-1.009%**로 3거래소 전부 낙폭이 거의 평탄권까지
  좁혀져 '부분 안정화'에서 '사실상 안정화'로 진전됐다.
- **⑤ BLESS — ⚠️⚠️⚠️ 안정화되지 않고 오히려 심화됐다.** OrangeX **-26.925%→-32.66%**,
  Aster **-26.441%→-37.697%**로 둘 다 낙폭이 더 커졌다. WebSearch 확인 결과 4월 400M
  토큰 팀 덤프로 -70% 급락한 전례에 더해, **8월 초 하루 만에 +77% '숏스퀴즈' 급등이 있었다는
  보도**(KuCoin·CoinGabbar)가 있어 이번 급락은 그 스퀴즈의 되돌림/재차익실현일 가능성이
  있다(원인 확정 아님).
- **⑥ CASHCAT** — 냉각이 3회차 연속 이어졌고, 직전 회차 갈렸던 OrangeX OI 반등도 이번엔
  다시 꺾여(**$61,005→$57,502, -5.7%**) 3거래소 전부 가격·OI가 동조 냉각으로 수렴했다 —
  직전 온체인 06:04Z 관측('냉각 심화')과 방향이 일치한다. Aster 펀딩은 0.001%→**-0.011%**로
  이번 회차 처음 마이너스 전환.
- **⑦ KAITO** — 개선 흐름이 2회차 연속 이어졌다(OKX **-11.531%→-11.030%**, HL
  **-11.86%→-11.352%**). 다만 펀딩은 두 거래소 모두 더 음전(OKX -0.459%→**-0.571%**, HL
  -0.20%→**-0.277%**). OI는 OKX -1.4%(8.22M→8.11M, 거의 유지)·HL 거의 유지(17.48M→17.53M)로
  큰 변화 없다. 8/20 대형 언락 약 11일 앞.
- **⑧ GRAM** — 마이너스권에서 거의 유지(-0.517%→**-0.443%**, HL -0.58%→**-0.251%**)로
  급격한 추가 악화는 없었다.

## 데이터 이슈 추적 결과

⚠️ **Hyperliquid funding 100배 확대 스케일 이상치는 이번 회차 재현되지 않았다** — raw
값이 다시 정상 스케일(예: ACE-USD -0.02, KAITO-USD -0.277, GRAM-USD 0.001)로 관측돼 100으로
나누는 보정 없이 그대로 사용했다. 100배 확대는 일회성 이슈였을 가능성이 높으나 다음 회차도
계속 추적한다. GIGGLE·KAITO(OKX 직접)의 필드 순서역전/완전동일값 이상치는 각각 **6회차 연속**
재현, GRAM의 완전동일값도 **4회차 연속** 재현돼 구조적 패턴으로 굳어졌다. **HYNA:HYPE-USD는
이번 회차 마침내 값이 갱신됐다**(OI $729,279.31→$724,950.96, 거래량 $31,893.06→$31,300.68,
chg24 1.98%→0.619%) — 2회 연속 완전 무변동 뒤 정상화돼 일시적 갱신 정체였을 가능성이 크다.

## 이번 회차 그 외 주요 변화

**ANSEM**이 이번 회차 처음 OrangeX에서도 확인됐다(**-4.664%**, 기존엔 Aster 전용으로
추적했음). Aster ANSEM은 -1.352%→**-4.582%**로 마이너스 심화 재반전됐다. **MMT**는 큰 폭
재가속(+9.307%) 직후 이번 회차 **-1.739%**로 반전됐다(펀딩도 -0.023%→-0.0003%로 중립
근접). **CAP**는 OKX에서 +1.212%→**+8.641%**로 큰 폭 재가속했고 Aster(+10.229%)·
OrangeX(+8.922%)도 동조했다. **AIO**는 -5.038%→**+0.213%**로 마이너스에서 플러스로 큰 폭
전환됐다. **AEON**은 첫 냉각 이후 OKX·OrangeX가 소폭 재가속했다(+15.811%→+16.686%,
+15.728%→+16.298%).

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [언락 반나절 이내, 2회차 냉각 폭 축소] | Binance/Bybit(가중) | $270.04M | $14.28M | -0.009% | +17.143% | +19.84%→+17.14%, 4거래소 전부 냉각 지속하나 강도 완화 | cooling-continues-second-round-narrower-magnitude-unlock-imminent |
| **BEAT** [⚠️ 요요 3회차, 재가속] | OKX(CoinGecko 정상) | $404.01M | $11.45M | -0.011% | +47.998% | +31.545%→+47.998%, OI +23.7% 급증 | whipsaw-reaccelerates-third-time-oi-surges |
| **BICO** [거래소 간 방향 갈림] | OKX(CoinGecko 정상) | $466.02M | $21.15M | -0.351% | +20.069% | OKX·OrangeX 재가속, Aster는 계속 냉각 | mixed-directional-split-across-venues |
| **BSB** [안정화 굳어짐] | OKX(CoinGecko 정상) | $10.78M | $2.89M | +0.005% | -2.226% | -9.444%→-2.226%, 3거래소 전부 거의 평탄권 | stabilization-solidifies-near-flat |
| AAVE [소폭 재가속] | Binance/Bybit(가중) | $41.28M | $89.31M | +0.0085% | +1.238% | +0.795%→+1.238% | mild-reacceleration |
| ALLO [4회차 마이너스, 소폭 개선] | Binance/Bybit(가중) | $33.30M | $19.06M | +0.005% | -4.534% | -4.83%→-4.534% | stays-negative-fourth-round-mild-improvement |
| ADA [5회차 마이너스, 개선] | Binance/Bybit(가중, USDT만) | $108.77M | $173.28M | +0.01% | -0.3725% | -1.124%→-0.3725% | stays-negative-fifth-round-improves |
| BANK [4회차 연속 개선] | Binance/Bybit(가중) | $57.08M | $20.26M | -0.023% | -1.937% | -2.965%→-1.937%, 펀딩도 개선. 8/17 언락 약 8일 앞 | improves-fourth-consecutive-round-funding-improves |
| AKE [개선, OI 큰 폭 감소] | Binance(Bybit 미확인) | $19.28M | $23.72M | +0.03% | -1.404% | -2.375%→-1.404%, OI -37.7%. 8/21 언락 약 12일 앞 | improves-oi-drops-sharply-bybit-unconfirmed |
| KAITO [개선 2회차, 펀딩 악화] | OKX(직접API) | $154.82M(계산값) | $8.11M | -0.571% | -11.030% | -11.531%→-11.030%. 8/20 대형 언락 약 11일 앞 | improves-second-round-funding-worsens |
| **MMT** [⚠️ 재가속 직후 반전] | OKX(직접API) | $195.58M(계산값) | $4.93M | -0.0003% | -1.739% | +9.307%→-1.739% | reverses-negative-after-sharp-reacceleration |
| GIGGLE [재가속] | OKX(직접API) | $28.43M(계산값) | $2.96M | +0.005% | +9.664% | +5.748%→+9.664%. ⚠️ 필드 순서 역전 6회차 연속 재현 | reaccelerates-field-order-anomaly-sixth-round |
| PIPPIN [소폭 재가속] | OKX(직접API) | $1.92M(계산값) | $1.88M | +0.030% | +3.349% | +2.209%→+3.349% | mild-reacceleration |
| 1000RATS [소폭 재악화] | Binance/Bybit(가중) | $9.70M | $18.41M | +0.0084% | -2.407% | -2.117%→-2.407% | mild-deterioration-after-third-round-improvement |
| **AIO** [⚠️ 플러스 전환] | Binance/Bybit(가중) | $9.17M | $4.45M | +0.027% | +0.213% | -5.038%→+0.213% | turns-positive-large-improvement |
| GRAM [마이너스권 거의 유지] | OKX(직접API) | $2.41M(계산값) | $6.38M | +0.005% | -0.443% | -0.517%→-0.443%. ⚠️ vol 필드 동일값 이상치 4회차 연속 | roughly-holds-negative-vol-field-anomaly-fourth-round |
| AEON [소폭 재가속] | OKX(CoinGecko 정상) | $31.22M | $4.28M | +0.005% | +16.686% | +15.811%→+16.686% | mild-reacceleration-after-first-cooling |
| ATOM [소폭 냉각] | Binance/Bybit(가중) | $11.42M | $28.54M | +0.0063% | +0.2498% | +1.0%→+0.25% | mild-cooling |
| ASTER [다시 마이너스] | Binance/Bybit(가중) | $16.35M | $113.09M | +0.0036% | -0.169% | +0.161%→-0.169% | turns-negative-again |
| CORE [대체로 유지] | OKX(CoinGecko 정상) | $1.45M | $0.99M | +0.001% | +4.212% | +4.737%→+4.212% | low-liquidity-roughly-holds |
| **CAP** [큰 폭 재가속] | OKX(CoinGecko 정상) | $20.74M | $2.54M | +0.005% | +8.641% | +1.212%→+8.641%, 3거래소 동조 | sharply-reaccelerates |
| ALGO [3회차 연속, 대체로 유지] | Binance/Bybit(가중) | $6.65M | $14.65M | +0.0003% | -0.849% | -0.918%→-0.849% | third-round-tracked-roughly-holds |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [2회차 냉각, 축소] | Hyperliquid | $5.40M | $1.70M | -0.02% | +16.377% | +19.49%→+16.38%, funding 정상 스케일 | cooling-continues-narrower-funding-scale-normal |
| **ACE-USDT-PERPETUAL** [냉각·OI 추가 감소] | OrangeX | $154.92M | $48.14M | -0.013% | +18.954% | OI -10.6% | cooling-continues-oi-declines-further |
| ACE-USDT [냉각, OI는 반등] | Aster | $0.72M | $0.08M | -0.015% | +17.879% | OI +13.7% | cooling-continues-oi-rebounds |
| **BEAT-USDT-PERPETUAL** [⚠️ 재가속] | OrangeX | $18.32M | $6.59M | +0.056% | +42.384% | +31.071%→+42.384% | whipsaw-reaccelerates |
| **BEAT** [⚠️ 재가속] | Aster | $5.99M | $5.13M | +0.001% | +42.898% | +30.776%→+42.898% | whipsaw-reaccelerates |
| **BICO-USDT-PERPETUAL** [재가속, OI 계속 감소] | OrangeX | $276.36M | $110.82M | -0.513% | +20.0% | OI -9.4% | mild-reacceleration-oi-continues-declining |
| BICO-USDT [⚠️ 다른 거래소와 반대로 냉각] | Aster | $1.96M | $0.65M | +0.001% | +14.489% | +18.805%→+14.489%, OI는 반등 | diverges-from-other-venues-continues-cooling |
| **CASHCAT** [냉각 3회차 연속] | Hyperliquid | $12.68M | $17.19M | +0.008% | +14.528% | +18.38%→+14.528% | cools-third-consecutive-round |
| **CASHCAT-USDT-PERPETUAL** [OI 반등 다시 꺾임] | OrangeX | $0.15M | $0.06M | +0.126% | +14.407% | OI $61,005→$57,502(-5.7%) | cools-oi-rebound-reverses-converges-with-other-venues |
| CASHCAT-USDT [냉각, 펀딩 첫 마이너스] | Aster | $1.50M | $1.26M | -0.011% | +14.238% | 펀딩 0.001%→-0.011% | cools-funding-turns-negative-first-time |
| ALLO-USDT [개선] | Aster | $0.15M | $0.03M | +0.001% | -4.37% | -5.305%→-4.37% | improves |
| ALLO-USDT-PERPETUAL [개선, OI 6회차 감소] | OrangeX | $22.92M | $7.68M | +0.01% | -3.379% | OI -10.7% | improves-oi-declines-sixth-round |
| AAVE-USDT-PERPETUAL [소폭 재가속] | OrangeX | $25.12M | $8.85M | +0.01% | +1.285% | +0.979%→+1.285% | mild-reacceleration |
| AAVE-USDT [소폭 재가속] | Aster | $0.17M | $4.56M | +0.01% | +1.297% | +0.9%→+1.297% | mild-reacceleration |
| AAVE-USD [재가속] | Hyperliquid | $2.69M | $60.60M | +0.001% | +1.309% | +0.82%→+1.309% | reaccelerates |
| ADA-USDT-PERPETUAL [소폭 개선] | OrangeX | $57.45M | $20.90M | +0.01% | -0.7% | -1.047%→-0.7% | mild-improvement |
| ADA-USDT [개선] | Aster | $0.14M | $1.52M | +0.01% | -0.35% | -0.997%→-0.35% | improves |
| ADA-USD [개선] | Hyperliquid | $1.77M | $33.26M | +0.0% | -0.425% | -1.21%→-0.425% | improves |
| BANK-USDT-PERPETUAL [개선] | OrangeX | $6.19M | $2.14M | +0.013% | -2.132% | -2.861%→-2.132% | improves |
| BANK-USDT [개선] | Aster | $0.38M | $0.38M | -0.002% | -1.688% | -2.666%→-1.688% | improves |
| AKE-USDT-PERPETUAL [소폭 개선] | OrangeX | $6.41M | $2.21M | +0.03% | -2.007% | -2.477%→-2.007% | mild-improvement |
| AKE-USDT [소폭 개선] | Aster | $0.31M | $10.66M | +0.016% | -2.072% | -2.521%→-2.072% | mild-improvement |
| **CAP-USDT** [⚠️ 큰 폭 플러스 전환] | Aster | $0.06M | $0.11M | +0.001% | +10.229% | -1.095%→+10.229% | turns-sharply-positive |
| CAP-USDT-PERPETUAL [큰 폭 재가속] | OrangeX | $0.50M | $0.19M | +0.01% | +8.922% | +0.709%→+8.922% | sharply-reaccelerates |
| ALGO-USDT-PERPETUAL [대체로 유지] | OrangeX | $4.06M | $1.34M | -0.01% | -0.687% | -1.029%→-0.687% | roughly-holds |
| ALGO-USDT [대체로 유지, 초저유동성] | Aster | $0.0003M | $0.03M | +0.001% | -0.995% | -0.867%→-0.995% | roughly-holds-low-liquidity |
| ALGO-USD [소폭 악화] | Hyperliquid | $0.37M | $2.00M | +0.001% | -0.936% | -0.8%→-0.936% | mildly-worsens |
| ATOM-USDT-PERPETUAL [소폭 냉각] | OrangeX | $5.86M | $2.19M | +0.01% | +0.218% | +0.877%→+0.218% | mild-cooling |
| ATOM-USDT [소폭 냉각, 플러스권] | Aster | $0.02M | $1.60M | +0.01% | +0.438% | +0.657%→+0.438% | holds-positive-mild-cooling |
| ATOM-USD [냉각, 플러스권] | Hyperliquid | $0.29M | $1.92M | +0.001% | +0.218% | +1.21%→+0.218% | holds-positive-cools |
| ASTER-USDT-PERPETUAL [다시 마이너스] | OrangeX | $6.59M | $2.24M | +0.01% | -0.135% | +0.148%→-0.135% | turns-negative-again |
| ASTER-USDT [대형 OI 유지, 다시 마이너스] | Aster | $8.87M | $218.68M | +0.016% | -0.166% | +0.199%→-0.166% | large-oi-roughly-holds-turns-negative-again |
| ASTER-USD [다시 마이너스] | Hyperliquid | $0.88M | $14.21M | +0.001% | -0.17% | +0.2%→-0.17% | turns-negative-again |
| **KAITO-USD** [개선 2회차, 펀딩 스케일 정상화] | Hyperliquid | $28.56M | $17.53M | -0.277% | -11.352% | -11.86%→-11.352%, ⚠️ 100배 확대 미재현. 8/20 대형 언락 약 11일 앞 | improves-second-round-funding-scale-normalizes |
| GRAM-USD [마이너스권 거의 유지] | Hyperliquid | $0.38M | $12.91M | +0.001% | -0.251% | -0.58%→-0.251% | roughly-holds-negative |
| HYPE-USD [플러스권, 추가 냉각] | Hyperliquid | $82.29M | $1,197.51M | -0.001% | +0.563% | +1.23%→+0.563% | holds-positive-cools-further |
| HYPER-USD [냉각, 플러스권] | Hyperliquid | $0.10M | $0.33M | +0.001% | +1.917% | +3.3%→+1.917% | holds-positive-cools |
| APEX-USD [마이너스권 개선] | Hyperliquid | $0.10M | $0.77M | +0.001% | -0.23% | -0.63%→-0.23% | improves-in-negative |
| FARTCOIN [냉각, 플러스권] | Hyperliquid | $2.46M | $22.19M | +0.001% | +1.222% | +1.97%→+1.222% | holds-positive-cools |
| ETHFI-USD [소폭 냉각, 플러스권] | Hyperliquid | $0.39M | $8.53M | +0.001% | +1.322% | +1.64%→+1.322% | holds-positive-mild-cooling |
| ETH-USD [플러스 전환] | dYdX | $2.62M | $8.61M | 0.0% | +0.016% | -0.084%→+0.016% | turns-positive |
| BTC-USD [대체로 유지] | dYdX | $0.94M | $18.05M | 0.0% | -0.288% | -0.311%→-0.288% | roughly-holds |
| SOL-USD [플러스권 확대] | dYdX | $0.38M | $4.52M | 0.0% | +1.969% | +1.767%→+1.969% | extends-positive |
| ANSEM [⚠️ 마이너스 심화 재반전] | Aster | $0.37M | $0.95M | +0.0% | -4.582% | -1.352%→-4.582%, OI -12.5% | reverses-negative-again |
| **ANSEM-USDT-PERPETUAL** [신규 — OrangeX 첫 확인] | OrangeX | $0.46M | $0.16M | +0.01% | -4.664% | 기존 Aster 전용에서 OrangeX 상장도 확인 | new-venue-confirmed-orangex |
| **BTW** [⚠️ 반전 확장, OI는 감소] | Aster | $2.61M | $13.04M | +0.018% | +16.288% | +8.897%→+16.288%, OI -11.2% | extends-reversal-oi-declines-despite-price-gain |
| HYNA:PUMP-USD [별개 페어 지속] | Hyperliquid | $0.04M | $0.16M | +0.002% | +9.686% | +9.198%→+9.686% | separate-pair-confirmed-extends |
| **HYNA:HYPE-USD** [⚠️ 갱신 재개] | Hyperliquid | $0.03M | $0.72M | -0.006% | +0.619% | 2회 연속 무변동 뒤 값 갱신됨 | resumes-updating-after-two-round-stale-data |
| AEON-USDT-PERPETUAL [소폭 재가속] | OrangeX | $0.50M | $0.18M | +0.01% | +16.298% | +15.728%→+16.298% | mild-reacceleration-after-first-cooling |
| AEON-USDT [대체로 유지] | Aster | $0.06M | $0.26M | +0.005% | +15.328% | +15.052%→+15.328% | roughly-holds |
| **BSB-USDT-PERPETUAL** [안정화 굳어짐] | OrangeX | $17.32M | $6.08M | +0.01% | -1.657% | -9.016%→-1.657% | stabilization-solidifies |
| **BSB-USDT** [안정화 굳어짐] | Aster | $0.11M | $0.11M | +0.001% | -1.009% | -8.506%→-1.009% | stabilization-solidifies |
| 1000RATS-USDT [소폭 개선] | Aster | $0.04M | $0.05M | +0.004% | -1.516% | -1.698%→-1.516% | mild-improvement |
| **BLESS** [⚠️⚠️⚠️ 낙폭 더 심화] | OrangeX | $133.77M | $41.86M | +0.109% | -32.66% | -26.925%→-32.66%, 8월 초 +77% 숏스퀴즈 되돌림 가능성 | selloff-deepens-not-stabilizing-possible-squeeze-unwind |
| **BLESS-USDT** [⚠️⚠️⚠️ 낙폭 더 심화] | Aster | $0.47M | $0.17M | +0.005% | -37.697% | -26.441%→-37.697%, OrangeX와 동조 | selloff-deepens-aligns-with-orangex |

## 테마 태그

1. **시장 전반: `/global` 8회 연속 429로 확보 실패, WebSearch 참고 수치는 이번 회차 $2.29T·56.8%로 되돌아와 직전 회차의 $2.21T·58.88%와 다시 달라짐 — 회차마다 값이 오락가락해 캐시 스냅샷일 가능성이 더 커짐** (global-api-fails-8x-websearch-flip-flops-cache-suspected).
2. **Fear&Greed 31(Fear) 4회차 연속 동일값 유지** (fear-greed-holds-31-fourth-consecutive-round).
3. **⚠️⚠️⚠️ ACE(Fusionist): 언락 반나절 이내로 임박, 4거래소 2회차 연속 냉각이나 폭은 크게 축소(2~4%p) — 사실상 언락 직전 마지막 관측** (ace-cooling-continues-narrower-unlock-under-12h).
4. **⚠️⚠️⚠️ BTW: 플러스 반전이 유지를 넘어 확장(+16.29%)됐으나 OI는 오히려 감소 — 숏 커버링 후 축소 가능성(확정 아님)** (btw-reversal-extends-oi-declines).
5. **⚠️⚠️⚠️ BLESS: 안정화되지 않고 낙폭이 더 심화(-32.66%/-37.70%) — 8월 초 +77% 숏스퀴즈 보도 확인, 이번 급락이 그 되돌림일 가능성** (bless-selloff-deepens-squeeze-unwind-possible).
6. **⚠️ BEAT: 냉각을 되돌리고 3회차째 요요 재가속(36%→48%→31%→48%), OI 급증** (beat-whipsaw-reaccelerates-third-time).
7. **BICO: OKX·OrangeX 소폭 재가속하나 Aster는 반대로 계속 냉각 — 거래소 간 방향 갈림** (bico-mixed-directional-split).
8. **BSB: 안정화가 사실상 굳어짐, 3거래소 전부 거의 평탄권으로 낙폭 축소** (bsb-stabilization-solidifies).
9. **CASHCAT: 냉각 3회차 연속, OrangeX OI 반등도 다시 꺾여 3거래소 전부 동조 냉각으로 수렴 — 온체인 냉각 관측과 방향 일치** (cashcat-converges-cooling-third-round).
10. **KAITO: 개선 2회차 연속(OKX·HL 동조), 다만 펀딩은 더 음전. 8/20 대형 언락 약 11일 앞** (kaito-improves-second-round-funding-worsens).
11. **⚠️ Hyperliquid funding 100배 확대 스케일 이상치가 이번 회차 재현되지 않음 — raw 값이 정상 스케일로 복귀, 일회성 이슈였을 가능성** (hl-funding-scale-anomaly-not-reproduced-normalizes).
12. **HYNA:HYPE-USD: 2회 연속 완전 무변동 뒤 이번 회차 값이 갱신됨 — 일시적 데이터 정체 해소** (hyna-hype-resumes-updating).
13. **ANSEM: OrangeX에서도 처음 상장 확인(기존 Aster 전용에서 확장), Aster는 마이너스 심화 재반전** (ansem-new-orangex-venue-reverses-negative).
14. **MMT: 큰 폭 재가속(+9.31%) 직후 마이너스로 반전(-1.74%)** (mmt-reverses-negative-after-reacceleration).
15. **CAP: OKX·OrangeX·Aster 전부 큰 폭 재가속(+1.2%→+8.6%대)** (cap-broad-reacceleration).
16. **AIO: 마이너스에서 플러스로 큰 폭 전환** (aio-turns-positive).
17. **GRAM: 마이너스권에서 거의 유지, 급격한 추가 악화 없음. ⚠️ vol24h=volCcy24h 완전동일값 이상치 4회차 연속 재현** (gram-holds-negative-vol-anomaly-fourth-round).
18. **⚠️ GIGGLE·KAITO(OKX 직접) 필드 이상치가 각각 6회차 연속 재현 — 구조적 패턴 굳어짐** (field-anomalies-sixth-round).
19. **OKX ACE·BANK·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT은 이번 회차도 CoinGecko okex_swap 배열 미등재, OKX 직접 API 또는 DEX로 보강. BEAT·BICO·AEON·BSB·CAP·CORE는 okex_swap 정상 확인** (okx-most-still-not-listed-direct-api-supplements).
20. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
21. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
22. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
23. **이번 회차 CoinGecko 429가 전반적으로 심화 — okex_swap·orangex_futures·dydx_chain이 각각 2~4차 재시도 끝에 확보됨** (rate-limiting-intensifies-this-round).
24. **지금은 일요일 저녁(UTC 06:29) 시간대** (sunday-evening-timing-caveat).

## 데이터 신뢰도

**CoinGecko binance_futures**: 1차 시도로 정상 확보. ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·
ASTER·ALGO·1000RATS 확인. **BEAT는 이번 회차도 조회 표에 나타나지 않음**(델리스킹 여부
불확실). BICO·GRAM·KAITO·MMT·PIPPIN·GIGGLE·BLESS·CASHCAT·BSB·CORE·AEON·BTW·CAP·ETHFI·
HYPE·HYPER·APEX·FARTCOIN는 Binance 미상장.

**CoinGecko bybit**: 1차 시도로 정상 확보. ACE·AAVE·ALLO·ADA·BANK·AIO·ATOM·ASTER·ALGO·
1000RATS·APEX 확인. **⚠️ AKE는 이번 회차 응답에서 미확인**(과거엔 확보됐던 것으로 추정 —
델리스팅인지 이번 조회의 추출 누락인지 불확실, 다음 회차 재확인 필요). **BEAT는 12회차
연속 미확인**. BICO·KAITO·MMT·PIPPIN·GIGGLE·BLESS·CASHCAT·BSB·CORE·AEON·BTW·CAP·ETHFI는
Bybit 미상장.

**CoinGecko okex_swap**: 2차 재시도 끝에 확보(1차 429). AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·
CORE·BSB·CAP·BEAT·BICO 확인. ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT은
이번 회차도 okex_swap 배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+`public/open-interest`
(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인. `oiUsd` 필드 직접 사용
방법론을 21회차 연속 유지, vol24_usd=`volCcy24h`×`last` 계산 방식도 유지. **⚠️ GIGGLE**은
이번 회차도 vol24h(80,556,316)가 volCcy24h(805,563.16)보다 큰 역전된 필드 순서가 **6회차
연속** 재현됐다. **KAITO**는 vol24h=volCcy24h(223,916,604, 완전 동일) 이상치가 **6회차 연속**
재현됐다. **GRAM**도 이번 회차 vol24h=volCcy24h(1,785,276, 완전 동일)로 **4회차 연속**
재현됐다. 세 이상치 모두 계산 방식은 그대로 유지했다.

**Hyperliquid**: 1차 시도로 정상 확보. **⚠️ 이번 회차 raw funding 필드가 정상 스케일로
관측됐다**(예: ACE-USD -0.02, KAITO-USD -0.277) — 직전 회차의 100배 확대 스케일 이상치가
재현되지 않아 별도 보정 없이 raw 값을 그대로 사용했다. ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·
ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD 등 raw 정밀값
확보. BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·BTW·BLESS·ANSEM은 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: 1차 시도로 정상 확보, raw 정밀 숫자로 직접 확보.
ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·BLESS·CASHCAT·BTW·ANSEM·AEON·ALGO·BEAT·BSB·
1000RATS 전량 확보. MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: 3차 재시도 끝에 확보(1~2차 429), raw 정밀값 직접 확보. ACE·
AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·CAP·BLESS·CASHCAT·BSB·ANSEM(신규 확인)
확인. KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·CORE는 여전히 미발견.

**dYdX(`dydx_chain`)**: 3차 재시도 끝에 확보, raw 정밀값(BTC-USD $0.94M/OI $18.05M, ETH-USD
$2.62M/OI $8.61M, SOL-USD $0.38M/OI $4.52M).

**CoinGecko `/global`**: **8회 연속 429로 확보 실패** — 직접 API 기반 총시총·도미넌스 수치를
갖지 못했다. WebSearch 스니펫이 이번 회차 $2.29T·56.8%로 나와 직전 회차 $2.21T·58.88%와
또 달라졌다 — 두 값이 회차 간 오락가락하는 패턴이 확인돼 캐시 스냅샷일 가능성이 커졌고,
여전히 직접 API가 아니므로 참고용으로만 표기한다.

**Fear&Greed**: alternative.me API로 1차 시도 정상 응답, **31(Fear)** 확인 — 4회차 연속
동일값.

**신규 발견**: ANSEM이 OrangeX에서도 처음 확인됐다(기존 Aster 전용에서 확장). HYNA:HYPE-USD의
2회 연속 무변동이 이번 회차 해소됐다. BEAT·BICO는 지시받은 냉각 지속 확인 시도에서 오히려
재반전(요요/거래소 갈림)이 발견됐다. BLESS는 안정화 기대와 달리 낙폭이 더 심화됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접 조회분)의
CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를 직접 채택(회차
간 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·ALGO 등 복수 거래소
종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은 본문·`why`에 별도
표기했다; (e) 이번 회차 Hyperliquid 원시 funding 필드가 정상 스케일로 관측돼 보정 없이 raw
값을 그대로 사용했다 — 직전 회차의 100배 확대가 일회성이었는지는 향후 회차로 추가 확인이
필요하다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE·BSB·BLESS는 Binance/
Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며, 이는 데이터 누락이 아니라 실제
상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·HYNA:HYPE-USD·BLESS는 DEX에서만 상장이
확인돼 해당 섹션에서만 집계했다; (h) Binance BEAT 소규모 리스팅이 이번 회차도 조회 표에
나타나지 않았는데, 델리스팅인지 조회 누락인지는 확정하지 않는다; (i) AKE의 Bybit 데이터가
이번 회차 미확인됐는데, 과거 회차에 확보됐던 이력을 고려하면 델리스팅보다는 이번 조회의
추출 누락일 가능성이 있으나 확정하지 않는다; (j) BLESS의 이번 회차 심화 급락은 OrangeX·
Aster 동시 발생으로 데이터 오류 가능성은 낮으나, 급락 배경(구체적 촉매)은 8월 초 숏스퀴즈
보도로 정황상 추정했을 뿐 직접적 인과관계는 확정하지 않는다; (k) 이번 회차 급변에 대한
인과관계 해석(언락 직전 디레버리징, 숏 커버링 등)은 대체로 정황상 추정이며 확정된 것은
아니다; (l) GIGGLE·KAITO의 필드 이상치가 6회차 연속, GRAM도 4회차 연속 재현돼 구조적
패턴에 가까워졌으나 근본 원인(OKX API 자체 특성인지)은 규명하지 않았다; (m) `/global`은
이번 회차 8회 연속 429로 실패했고 WebSearch 근사치는 직전 회차와 또 달라졌으나 여전히
직접 API가 아니라 신뢰도를 낮게 잡아야 한다; (n) 지금은 일요일 저녁으로 유동성 패턴이
평일과 다를 수 있으며, 확정 불가.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
