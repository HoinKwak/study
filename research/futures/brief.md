# 선물시장 스카우트 브리핑 — 2026-08-10 02:30 UTC (KST 2026-08-10 11:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-10T00:27:00Z)
> 로부터 약 2시간3분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 429를 두 차례 겪은 뒤 재시도로 확보 성공 — 총시총
**$2,298,263,724,060.36(약 $2.298T)**·BTC도미넌스 **56.67%**로 직전 회차($2.302T·56.69%)보다
시총·도미넌스 모두 소폭 하락 — **10회차 연속** 확보됐다(단 이번에도 재시도 필요).

### Fear&Greed 30(Fear) — 직전과 동일, 2회차 연속

alternative.me API 정상 응답, **30(Fear)** — 직전 회차(30)에서 변동 없이 유지됐다. 12회차
연속이던 31 스트릭이 종료된 직후이며, 새로운 소폭 스트릭이 시작되는지는 다음 회차 확인이
필요하다.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM 개별조회)는 **31회차 연속** 방법론(`oiUsd`
필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을 유지했다.
이번 회차는 CoinGecko `okex_swap`·`orangex_futures`·`dydx_chain`·`/global`이 모두 429를
3~4회씩 겪은 뒤 재시도로 확보됐다 — 레이트리밋이 유독 심했다(참고: `okex` id는 여전히
404, 올바른 id는 `okex_swap`).

## 이번 회차 최대 사건

### ⚠️⚠️⚠️⚠️ ACE — 회복 흐름 정체, 소스 간 혼조로 전환

직전 회차 5개 소스 전원 개선이 이번 회차 혼조로 바뀌었다: Binance **-14.783%→-14.604%**
(개선), Bybit **-15.537%→-16.69%**(악화), OrangeX **-15.475%→-14.026%**(개선), Aster
**-15.392%→-14.694%**(개선), Hyperliquid **-14.117%→-17.503%**(악화). Binance/Bybit
거래량가중은 **-14.956%→-15.108%**로 사실상 보합 — 직전 회차의 뚜렷한 개선 흐름이 이번엔
정체됐다. tokenomist(tokenomist.ai/endurance, 페이지 자체는 Fusionist/ACE로 확인)를
재확인한 결과 수치는 직전과 완전히 동일했다(누적 언락 107,613,807 ACE·73.21%, 다음 언락
2026년 9월 3일 Early Investors). '최종 갱신' 시각이 요청 시각(08/10/26 02:23 AM)과 거의
일치해 데이터는 최신이나, **8/10 언락 집행을 명시적으로 확인하는 문구는 여전히 없다** —
새로운 확정 근거는 추가되지 않았다. OI는 Binance+Bybit 합산 **$11.83M→$11.17M**로 계속
완만히 감소해 포지션 정리는 이어지고 있다. OKX 직접조회로 ACE-USDT-SWAP를 재확인한 결과
이번 회차도 instId 자체가 존재하지 않아(에러코드 51001) OKX 미상장이 **31회차 연속**
재확인됐다.

### ⚠️⚠️⚠️ BEAT — 신고점 상승분 완전 반납, 3소스 전원 마이너스 전환

직전 회차 '신고점에서 대폭 냉각'(+9~14%)이 이번 회차 완전히 반전, 3소스 전원 마이너스로
전환됐다. OKX **+12.947%→-12.21%**, OrangeX **+14.225%→-13.424%**, Aster
**+9.398%→-11.263%** — 하루 전 신고점(36~37%) 상승분이 전부 반납되고 추가 하락까지
겹쳤다.

### ⚠️⚠️⚠️ BICO — 4회차 연속 악화 재심화, 최대낙폭 재경신

4회차 연속 악화가 다시 큰 폭으로 심화돼 **-36~38%대**로 이전 최대낙폭(-28~29%대)을
재차 큰 폭 경신했다. OKX **-28.597%→-36.816%**, OrangeX **-28.308%→-37.822%**, Aster
**-28.55%→-36.479%**. WebSearch 확인 결과 이번 주 Aster DEX·AlphaX에 BICO 신규 퍼프
(최대 50x)가 상장됐고 Bitkub 현물 상장이 8/22 예정이라는 뉴스가 있었으나, 이런 뉴스와
별개로 실측 가격은 하락을 계속하고 있어 **뉴스상 강세 서술과 실측 데이터가 상충**한다 —
정직하게 그대로 병기한다.

## 직전 회차 강조 종목 추적 결과

- **① ACE — ⚠️⚠️⚠️⚠️ 회복 정체, 혼조로 전환.** 위 '이번 회차 최대 사건' 참조.
- **② BEAT — ⚠️⚠️⚠️ 완전 반전, 추가 하락 확정.** 위 참조 — '재반등이냐 추가 하락이냐'
  질문에 **추가 하락**으로 명확히 답이 나왔다.
- **③ BICO — ⚠️⚠️⚠️ 4회차 연속 악화 재심화, 바닥 신호 없음.** 위 참조 — '바닥 신호가
  나오는지' 질문에 **아니다, 오히려 더 큰 폭으로 신저점을 경신**했다.
- **④ KAITO — 혼조 해소, 가격·펀딩 동반 개선.** OKX **-4.365%→+0.172%**(플러스 전환),
  펀딩 **-0.332%→-0.185%**(개선). HL **-5.404%→-0.653%**, 펀딩 **-0.167%→-0.109%**로
  함께 개선됐다. 8/20 대형 언락(WebSearch 재확인 $22.9M~$34.68M·공급 3.3~7.63%, 소스별
  편차 여전) 약 9.8일 앞.
- **⑤ BANK — 3번째 휩쏘, 재차 플러스 전환.** Binance/Bybit 가중 **-1.713%→+1.148%**
  (Binance +1.184%·Bybit +0.924%), OrangeX **-2.842%→+1.297%**, Aster
  **-3.16%→+2.137%**로 4소스 전원 재반전. 8/17 언락 약 6.8일 앞.
- **⑥ CASHCAT — 소폭 재가속 지속.** HL **8.06%→8.247%**, OrangeX **8.889%→10.71%**,
  Aster **7.959%→9.506%**로 3거래소 모두 소폭 상승 — 온체인 h1 재양전과 정합되는 미약한
  반등이나 원 고점(약 20%)에는 크게 못 미친다.

## 신규 발견 — CAP 급등

⚠️ **CAP**이 이번 회차 예상치 못한 급등을 보였다: OKX **+8.327%→+23.817%**, OrangeX
**+9.254%→+25.625%**, Aster **+8.336%→+19.08%**로 3소스 동조 급등했다. 다만 저유동성
(OKX OI $3.54M·OrangeX $0.2M·Aster $0.14M)이라 변동성이 크고, 원인은 이번 회차에서
규명하지 못했다. AIO도 Binance/Bybit 가중 **+0.638%→+5.734%**로 급등했다.

## 기타 주요 변화

**ALLO**(-5.766%→**-2.213%**)·**BLESS**(-11.16%→**-1.856%**, Aster -11.37%→**-5.205%**)가
뚜렷이 개선됐다. **AEON**은 4회차 연속 재악화가 이어졌다(OKX -10.891%→**-14.27%**,
OrangeX -11.914%→**-14.517%**, Aster -10.652%→**-13.98%**). **BSB**는 3번째 휩쏘로
다시 완화됐다(OKX -13.181%→**-9.812%**, OrangeX -12.911%→**-11.054%**, Aster
-12.354%→**-8.848%**).

## 데이터 이슈 추적 결과

**HYNA:HYPE-USD**의 OI는 직전 회차 처음 변동한 데 이어 이번 회차도 정상 갱신을
이어갔다($684,023.08→**$688,008.38**) — 정상화가 **2회차 연속** 확인됐다. GIGGLE의 필드
이상치(vol24h=65,453,929 vs volCcy24h=654,539.29, 정확히 100배 스케일 차이를 raw
JSON으로 재확인)가 **16회차 연속**, KAITO(OKX 직접, vol24h=volCcy24h=107,742,951 raw
재확인)의 완전동일값이 **16회차 연속**, GRAM(vol24h=volCcy24h=2,353,076 raw 재확인)의
완전동일값이 **14회차 연속** 재현됐다 — 세 이상치 모두 여전히 견고하다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️⚠️⚠️ 회복 정체, 혼조] | Binance/Bybit(가중) | $85.91M | $11.17M | +0.005% | -15.108% | 소스 간 방향 갈림, 가중 보합 | unlock-recovery-stalls-mixed-sources |
| **BICO** [⚠️⚠️⚠️ 4회차 악화 재심화] | OKX(CoinGecko정상, okex_swap) | $450.79M | $8.89M | -0.266% | -36.816% | -28.597%→-36.816%, 최대낙폭 재경신 | worsening-continues-record-low-again |
| **BEAT** [⚠️⚠️⚠️ 완전 반전] | OKX(CoinGecko정상, okex_swap) | $344.87M | $8.05M | +0.005% | -12.21% | +12.947%→-12.21%, 3소스 마이너스 전환 | full-reversal-to-negative-after-high |
| **KAITO** [혼조 해소, 동반 개선] | OKX(직접API) | $75.33M | $7.88M | -0.185% | +0.172% | 가격·펀딩 동반 개선. 8/20 언락 9.8일 앞 | mixed-signals-resolve-both-improve |
| **BANK** [3번째 휩쏘, 플러스 전환] | Binance/Bybit(가중) | $115.80M | $19.03M | +0.003% | +1.148% | -1.713%→+1.148%, 4소스 전원 재반전 | third-whipsaw-back-to-positive |
| MMT [플러스 유지, 소폭 확대] | OKX(직접API) | $76.45M | $3.43M | -0.054% | +0.647% | +0.445%→+0.647% | positive-holds-mild-increase |
| BSB [3번째 휩쏘, 완화] | OKX(CoinGecko정상, okex_swap) | $5.52M | $2.53M | +0.006% | -9.812% | -13.181%→-9.812% | third-whipsaw-eases-again |
| AAVE [플러스 확대] | Binance/Bybit(가중) | $44.95M | $88.73M | +0.007% | +0.652% | +0.145%→+0.652% | extends-positive |
| ALLO [뚜렷한 개선] | Binance/Bybit(가중) | $23.20M | $18.08M | +0.002% | -2.213% | -5.766%→-2.213% | notable-improvement-within-negative |
| ADA [15회차 마이너스] | Binance/Bybit(가중, USDT만) | $144.15M | $169.41M | +0.003% | -1.506% | -1.428%→-1.506% | fifteenth-round-negative-roughly-flat |
| AKE [개선 지속, 냉각] | Binance/Bybit(가중) | $42.80M | $39.36M | +0.043% | +5.222% | +5.775%→+5.222% | improvement-continues-mild-cooling |
| GIGGLE [마이너스 확대] | OKX(직접API) | $22.35M | $2.61M | +0.005% | -6.157% | -4.425%→-6.157%. ⚠️ 필드 이상치 16회차 연속 | worsens-within-negative-field-anomaly-16th-round |
| PIPPIN [플러스 유지, 냉각] | OKX(직접API) | $2.10M | $1.94M | +0.039% | +2.734% | +3.976%→+2.734% | positive-holds-mild-cooling |
| 1000RATS [플러스 유지, 냉각] | Binance/Bybit(가중) | $13.47M | $18.72M | +0.031% | +4.176% | +4.833%→+4.176% | extends-positive-mild-cooling |
| AIO [⚠️ 급등] | Binance/Bybit(가중) | $11.78M | $4.58M | +0.023% | +5.734% | +0.638%→+5.734% | sudden-surge |
| GRAM [마이너스 소폭 완화] | OKX(직접API) | $3.12M | $6.42M | +0.005% | -1.852% | -2.357%→-1.852%. ⚠️ 필드 이상치 14회차 연속 | mild-easing-within-negative-field-anomaly-14th-round |
| AEON [⚠️ 4회차 재악화] | OKX(CoinGecko정상, okex_swap) | $19.34M | $3.62M | +0.005% | -14.27% | -10.891%→-14.27% | worsening-continues-fourth-round |
| ATOM [마이너스 소폭 확대] | Binance/Bybit(가중) | $9.39M | $28.14M | -0.005% | -0.676% | -0.237%→-0.676% | worsens-within-negative |
| ASTER [플러스 유지, 냉각] | Binance/Bybit(가중) | $21.84M | $113.62M | +0.005% | +1.727% | +2.283%→+1.727% | positive-holds-mild-cooling |
| CORE [초저유동성, 거의 유지] | OKX(CoinGecko정상, okex_swap) | $1.85M | $1.02M | +0.010% | +3.389% | +3.426%→+3.389% | low-liquidity-roughly-flat |
| **CAP** [⚠️ 급등, 신규 이벤트] | OKX(CoinGecko정상, okex_swap) | $33.37M | $3.54M | +0.005% | +23.817% | +8.327%→+23.817%, 저유동성 변동성 큼 | sudden-surge-low-liquidity |
| ALGO [마이너스 소폭 확대] | Binance/Bybit(가중) | $15.29M | $14.80M | +0.010% | -5.997% | -5.832%→-5.997% | worsens-mildly-within-negative |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [⚠️ 재악화, CEX와 반대] | Hyperliquid | $2.34M | $1.27M | -0.002% | -17.503% | -14.117%→-17.503% | unlock-recovery-stalls-worsens |
| **ACE-USDT-PERPETUAL** [개선 지속] | OrangeX | $54.25M | $17.77M | +0.013% | -14.026% | -15.475%→-14.026% | unlock-recovery-stalls-improves |
| **ACE-USDT** [개선 지속] | Aster | $0.40M | $0.05M | +0.001% | -14.694% | -15.392%→-14.694% | unlock-recovery-stalls-improves |
| BEAT-USDT-PERPETUAL [완전 반전] | OrangeX | $17.91M | $5.03M | +0.010% | -13.424% | +14.225%→-13.424% | full-reversal-to-negative-after-high |
| BEAT-USDT [완전 반전] | Aster | $5.71M | $2.35M | -0.006% | -11.263% | +9.398%→-11.263% | full-reversal-to-negative-after-high |
| **BICO-USDT-PERPETUAL** [⚠️ 4회차 재심화] | OrangeX | $242.66M | $62.03M | -0.324% | -37.822% | -28.308%→-37.822% | worsening-continues-record-low-again |
| **BICO-USDT** [⚠️ 4회차 재심화] | Aster | $4.10M | $0.27M | +0.003% | -36.479% | -28.55%→-36.479% | worsening-continues-record-low-again |
| **CASHCAT** [소폭 재가속] | Hyperliquid | $18.71M | $21.45M | +0.037% | +8.247% | 8.06%→8.247% | mild-reacceleration |
| CASHCAT-USDT-PERPETUAL [소폭 재가속] | OrangeX | $0.14M | $0.05M | -0.010% | +10.71% | 8.889%→10.71% | mild-reacceleration |
| CASHCAT-USDT [소폭 재가속] | Aster | $1.87M | $1.45M | +0.022% | +9.506% | 7.959%→9.506% | mild-reacceleration |
| ALLO-USDT [뚜렷한 개선] | Aster | $0.09M | $0.03M | -0.002% | -2.466% | -5.245%→-2.466% | notable-improvement-within-negative |
| ALLO-USDT-PERPETUAL [뚜렷한 개선] | OrangeX | $15.56M | $5.23M | +0.010% | -2.452% | -5.367%→-2.452% | notable-improvement-within-negative |
| AAVE-USDT-PERPETUAL [플러스로 회복] | OrangeX | $24.80M | $8.83M | +0.010% | +0.506% | -0.099%→+0.506% | recovers-to-positive |
| AAVE-USDT [플러스 확대] | Aster | $0.40M | $4.60M | +0.010% | +0.693% | +0.088%→+0.693% | extends-positive |
| AAVE-USD [플러스 확대] | Hyperliquid | $3.32M | $61.68M | +0.001% | +1.115% | +0.17%→+1.115% | extends-positive |
| ADA-USDT-PERPETUAL [마이너스 소폭 완화] | OrangeX | $79.73M | $26.97M | +0.010% | -1.108% | -1.363%→-1.108% | mild-easing-within-negative |
| ADA-USDT [거의 유지] | Aster | $0.42M | $1.67M | +0.010% | -1.406% | -1.709%→-1.406% | roughly-flat-negative |
| ADA-USD [마이너스 소폭 완화] | Hyperliquid | $3.41M | $32.82M | 0.000% | -0.988% | -1.579%→-0.988% | mild-easing-within-negative |
| BANK-USDT-PERPETUAL [3번째 휩쏘] | OrangeX | $8.16M | $2.66M | -0.017% | +1.297% | -2.842%→+1.297% | third-whipsaw-back-to-positive |
| BANK-USDT [3번째 휩쏘] | Aster | $0.52M | $0.35M | +0.001% | +2.137% | -3.16%→+2.137% | third-whipsaw-back-to-positive |
| AKE-USDT-PERPETUAL [플러스 확대] | OrangeX | $5.94M | $2.19M | +0.036% | +8.121% | +5.21%→+8.121% | extends-positive |
| AKE-USDT [개선 지속, 냉각] | Aster | $0.55M | $11.47M | +0.020% | +4.93% | +6.872%→+4.93% | improves-mild-cooling |
| **CAP-USDT** [⚠️ 급등] | Aster | $0.05M | $0.14M | +0.001% | +19.08% | +8.336%→+19.08% | sudden-surge-low-liquidity |
| **CAP-USDT-PERPETUAL** [⚠️ 급등] | OrangeX | $0.51M | $0.20M | +0.010% | +25.625% | +9.254%→+25.625% | sudden-surge-low-liquidity |
| ALGO-USDT-PERPETUAL [마이너스 소폭 확대] | OrangeX | $8.49M | $3.11M | +0.010% | -6.393% | -5.95%→-6.393% | worsens-mildly-within-negative |
| ALGO-USDT [초저유동성, 완화] | Aster | $0.03M | $0.02M | -0.003% | -5.293% | -6.431%→-5.293% | low-liquidity-mild-easing |
| ALGO-USD [거의 유지] | Hyperliquid | $0.94M | $1.95M | +0.001% | -5.759% | -5.893%→-5.759% | roughly-flat-negative |
| ATOM-USDT-PERPETUAL [거의 유지] | OrangeX | $5.20M | $1.65M | +0.010% | -0.653% | -0.723%→-0.653% | roughly-flat-negative |
| ATOM-USDT [초저유동성, 거의 유지] | Aster | $0.01M | $1.59M | +0.010% | -0.581% | -0.65%→-0.581% | low-liquidity-roughly-flat |
| ATOM-USD [플러스→마이너스 재전환] | Hyperliquid | $0.20M | $1.91M | +0.001% | -0.652% | -0.325%→-0.652% | turns-negative-again |
| ASTER-USDT-PERPETUAL [플러스 유지, 냉각] | OrangeX | $8.99M | $3.10M | +0.010% | +1.778% | +2.242%→+1.778% | positive-holds-mild-cooling |
| ASTER-USDT [대형 OI, 냉각] | Aster | $13.41M | $222.54M | +0.012% | +1.778% | OI $224.08M→$222.54M, +2.237%→+1.778% | large-oi-positive-holds-mild-cooling |
| ASTER-USD [플러스 유지, 냉각] | Hyperliquid | $1.40M | $14.83M | +0.001% | +1.805% | +2.168%→+1.805% | positive-holds-mild-cooling |
| KAITO-USD [혼조 해소, 동반 개선] | Hyperliquid | $19.31M | $14.29M | -0.109% | -0.653% | -5.404%→-0.653%, 펀딩도 개선 | mixed-signals-resolve-both-improve |
| GRAM-USD [완화, OKX와 근접] | Hyperliquid | $0.69M | $12.84M | +0.001% | -1.304% | -2.251%→-1.304% | mild-easing-matches-okx |
| HYPE-USD [거의 유지] | Hyperliquid | $89.20M | $1,182.45M | 0.000% | -1.692% | -1.72%→-1.692% | roughly-flat-negative |
| HYPER-USD [거의 유지] | Hyperliquid | $0.10M | $0.31M | +0.001% | -0.296% | -0.312%→-0.296% | roughly-flat-negative |
| APEX-USD [마이너스→플러스 재전환] | Hyperliquid | $0.07M | $0.77M | +0.001% | +0.434% | -0.322%→+0.434%, Bybit도 +0.184% | turns-positive-again-bybit-matches |
| FARTCOIN [거의 유지] | Hyperliquid | $6.92M | $22.41M | +0.001% | +1.507% | +1.524%→+1.507% | roughly-flat-positive |
| ETHFI-USD [플러스 확대] | Hyperliquid | $0.66M | $8.44M | +0.001% | +2.197% | +0.277%→+2.197% | extends-positive |
| ETH-USD [플러스→마이너스 전환] | dYdX | $10.62M | $9.10M | +0.003% | -0.031% | +0.292%→-0.031% | turns-negative-from-positive |
| BTC-USD [플러스 유지, 냉각] | dYdX | $1.49M | $17.76M | 0.000% | +0.052% | +0.251%→+0.052% | positive-holds-mild-cooling |
| SOL-USD [플러스 유지, 냉각] | dYdX | $0.14M | $4.51M | 0.000% | +0.804% | +1.291%→+0.804% | positive-holds-mild-cooling |
| ANSEM [거의 유지] | Aster | $0.24M | $0.88M | +0.001% | -5.178% | -5.198%→-5.178% | roughly-flat-negative |
| ANSEM-USDT-PERPETUAL [거의 유지] | OrangeX | $0.49M | $0.17M | +0.010% | -5.469% | -5.475%→-5.469% | roughly-flat-negative |
| **BTW** [플러스 확대] | Aster | $2.48M | $15.18M | +0.033% | +6.947% | +5.241%→+6.947% | extends-positive |
| HYNA:PUMP-USD [플러스권 축소] | Hyperliquid | $0.05M | $0.17M | +0.001% | +8.25% | +14.812%→+8.25%, 뚜렷이 냉각 | cools-within-positive |
| **HYNA:HYPE-USD** [⚠️ OI 정상갱신 2회차 연속] | Hyperliquid | $0.14M | $0.69M | +0.011% | -2.02% | $684,023.08→$688,008.38, 정상화 지속 | oi-normal-updates-continue-2nd-round |
| AEON-USDT-PERPETUAL [4회차 재악화] | OrangeX | $0.45M | $0.16M | +0.010% | -14.517% | -11.914%→-14.517% | worsening-continues-fourth-round |
| AEON-USDT [4회차 재악화] | Aster | $0.09M | $0.21M | +0.008% | -13.98% | -10.652%→-13.98% | worsening-continues-fourth-round |
| **BSB-USDT-PERPETUAL** [3번째 휩쏘, 완화] | OrangeX | $10.35M | $3.42M | +0.010% | -11.054% | -12.911%→-11.054% | third-whipsaw-eases-again |
| **BSB-USDT** [3번째 휩쏘, 완화] | Aster | $0.04M | $0.10M | +0.001% | -8.848% | -12.354%→-8.848% | third-whipsaw-eases-again |
| 1000RATS-USDT [플러스 유지, 거의 유지] | Aster | $0.12M | $0.04M | +0.015% | +4.127% | +4.144%→+4.127% | extends-positive-roughly-flat |
| **BLESS** [뚜렷한 개선] | OrangeX | $82.11M | $26.73M | +0.069% | -1.856% | -11.16%→-1.856% | notable-improvement-within-negative |
| **BLESS-USDT** [뚜렷한 개선] | Aster | $0.32M | $0.20M | +0.005% | -5.205% | -11.37%→-5.205% | notable-improvement-within-negative |

## 테마 태그

1. **시장 전반: `/global`이 429 재시도 끝에 10회차 연속 확보 성공 — 총시총 $2.298T(소폭 하락)·BTC도미넌스 56.67%(소폭 하락)** (global-api-tenth-round-needed-retry).
2. **Fear&Greed 30(Fear) — 직전과 동일, 2회차 연속 유지** (fear-greed-holds-at-30-second-round).
3. **⚠️⚠️⚠️⚠️ ACE: 직전 전 소스 개선이 이번엔 소스 간 혼조로 전환, 가중평균 보합. tokenomist 수치 동일, 신규 확정근거 없음** (ace-recovery-stalls-mixed-sources).
4. **⚠️⚠️⚠️ BEAT: 신고점 반납 후 3소스 전원 마이너스로 완전 반전** (beat-full-reversal-to-negative).
5. **⚠️⚠️⚠️ BICO: 4회차 연속 악화 재심화, -36~38%대로 최대낙폭 재경신. 신규 퍼프 상장 뉴스와 실측 하락 상충** (bico-worsening-continues-record-low-again).
6. **KAITO: 가격·펀딩 동반 개선, 혼조 해소. 8/20 대형 언락 약 9.8일 앞** (kaito-mixed-signals-resolve-both-improve).
7. **BANK: 3번째 휩쏘로 재차 플러스 전환, 4소스 전원. 8/17 언락 약 6.8일 앞** (bank-third-whipsaw-back-to-positive).
8. **CASHCAT: 소폭 재가속 지속(8~11%대), 온체인 h1 재양전과 정합** (cashcat-mild-reacceleration).
9. **⚠️ CAP: 예상치 못한 급등(+8~9%→+19~26%), 저유동성 변동성 큼** (cap-sudden-surge-low-liquidity).
10. **AIO: 가중 +0.638%→+5.734%로 급등** (aio-sudden-surge).
11. **ALLO·BLESS: 뚜렷한 개선** (allo-bless-notable-improvement).
12. **⚠️ AEON: 4회차 연속 재악화 지속(-11%대→-14%대)** (aeon-worsening-continues-fourth-round).
13. **BSB: 3번째 휩쏘로 재차 완화** (bsb-third-whipsaw-eases-again).
14. **HYNA:HYPE-USD: OI 정상 갱신 2회차 연속 이어짐** (hyna-hype-oi-normal-updates-continue).
15. **⚠️ GIGGLE 필드 이상치 16회차 연속, KAITO(OKX 직접) 완전동일값 16회차 연속, GRAM 14회차 연속 재현** (field-anomalies-16th-16th-14th-round-continue).
16. **TOAD: 추적 CEX·DEX 어디에도 선물 상장 미확인(MEXC 언급만 존재)** (toad-not-listed-on-tracked-futures-venues).
17. **OKX ACE·BANK·1000RATS·AIO·KAITO·MMT·PIPPIN·GIGGLE·GRAM은 okex_swap 미등재(ACE는 instId 자체 부재, 31회차 연속), 직접 API/DEX로 보강** (okx-most-still-not-listed-direct-api-supplements).
18. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
19. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
20. **이번 회차는 CoinGecko okex_swap·orangex_futures·dydx_chain·global 전부 429를 3~4회씩 겪은 뒤 재시도로 확보 — 레이트리밋이 유독 심했다** (coingecko-heavy-rate-limiting-this-round).
21. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**CoinGecko binance_futures**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS
확인. **BICO·BEAT·BSB·APEX·BTW·KAITO·CASHCAT·MMT·GIGGLE·PIPPIN·GRAM·CORE·CAP·AEON·BLESS·
ANSEM은 이번 회차도 명확히 미확인**(단순 미상장).

**CoinGecko bybit**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS·APEX 확인.
나머지는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·CAP·BICO·BEAT 확인.
ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT은 이번 회차도 okex_swap
배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계. `okex` id는 404로 무효 확인, 올바른
id는 `okex_swap`. 이번 회차는 429를 3~4회 겪은 뒤 재시도로 확보했다.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인.
`oiUsd` 필드 직접 사용 방법론을 **31회차 연속** 유지, vol24_usd=`volCcy24h`×`last` 계산
방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️ **ACE-USDT-SWAP는 OKX에 instId
자체가 존재하지 않음**을 이번 회차도 직접 확인(에러코드 51001). **GIGGLE**은 raw JSON에서
`vol24h=65,453,929`·`volCcy24h=654,539.29`로 정확히 100배 스케일 차이가 나는 필드 이상치가
**16회차 연속**, **KAITO**는 `vol24h`=`volCcy24h`=107,742,951로 완전동일값 이상치가
**16회차 연속**, **GRAM**도 `vol24h`=`volCcy24h`=2,353,076로 완전동일값이 **14회차 연속**
재현됐다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·
ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD·BTC·ETH 등 raw 정밀값 확보. **SOL은 HL에서 이번 회차도
미확인**(기존 dYdX로 대체 집계). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·BTW·BLESS·ANSEM은
HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·
BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON·AIO 전량 확보(raw 정밀값). MMT·GIGGLE·
PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값). BTW는 이번 회차도 OrangeX에서 미발견(기존과
동일, Aster에서만 확인). KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·CORE는 여전히 미발견.
이번 회차는 429를 3~4회 겪은 뒤 재시도로 확보했다.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.49M/OI $17.76M, ETH-USD $10.62M/OI $9.10M,
SOL-USD $0.14M/OI $4.51M) 확보. 이번 회차도 429를 겪은 뒤 재시도로 확보했다.

**CoinGecko `/global`**: 429를 두 차례 겪은 뒤 재시도로 총시총 $2,298,263,724,060.36(약
$2.298T)·BTC도미넌스 56.67%를 확인했다. 직전 회차($2.302T·56.69%)보다 시총·도미넌스 모두
소폭 하락, **10회차 연속** 확보됐으나(단 이번에도 재시도 필요).

**Fear&Greed**: alternative.me API로 정상 응답, **30(Fear)** 확인 — 직전과 동일, 2회차
연속 유지됐다.

**TOAD**: WebSearch로 확인한 결과 추적 중인 CEX·DEX 어디에서도 선물 상장 근거를 찾지
못했다(MEXC에 TOADUSDT 선물이 있다는 언급만 확인, 비추적 거래소). '미상장/미확인'으로
정직하게 표기.

**신규 발견**: (a) ACE의 회복이 직전 회차의 '전 소스 개선'에서 이번 회차 '소스 간 혼조'로
바뀌었다 — 완전한 확정 회복은 아직 아니다. (b) BEAT가 신고점 상승분을 하루 만에 완전히
반납하고 마이너스로 전환됐다 — '신고점 지속성 낮음' 가설이 강하게 뒷받침됐다. (c) BICO가
4회차 연속 악화를 이어가며 -36~38%대까지 밀렸다 — WebSearch로 확인한 신규 퍼프 상장 뉴스와
실측 데이터가 상충함을 정직하게 병기했다. (d) CAP이 저유동성 상태에서 예상치 못한 급등을
보였다 — 원인은 규명하지 못했다. (e) HYNA:HYPE-USD의 OI 정상 갱신이 2회차 연속 확인돼,
직전 회차의 '정상화 종료' 판단이 지속되고 있다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(31회차 연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은
본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상 스케일로
관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·
GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며,
이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·
HYNA:HYPE-USD·BLESS는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다; (h) ACE 언락
집행 여부는 tokenomist 페이지의 '다음 언락' 항목(9/3)과 최종 갱신 시각을 근거로
**추정**한 것이며, 명시적인 '집행 완료' 로그·타임스탬프는 이번 회차도 확보하지 못했다 —
완전한 확정은 아니다; (i) BICO의 소스 간 격차·악화 추세가 4회차 연속 이어지고 있으며,
근본 원인(상장 거래소별 유동성 구조·신규 퍼프 상장에 따른 레버리지 유입 등)은 규명하지
않았다; (j) KAITO 8/20 언락 규모는 소스별로 공급 3.3%~7.63%·$22.9M~$34.68M로 편차가
있어 정확한 수치는 확정하지 않았다; (k) GIGGLE·KAITO의 필드 이상치가 16회차 연속, GRAM도
14회차 연속 재현돼 구조적 패턴으로 굳어졌으나 근본 원인(OKX API 자체 특성인지)은 규명하지
않았다; (l) CAP의 급등 원인은 이번 회차에서 조사하지 못했다 — 다음 회차 추적이 필요하다;
(m) `/global`은 이번 회차도 429 재시도 끝에 확보돼 10회차 연속 성공은 유지했으나 매 회차
순조로운 것은 아니다; (n) TOAD의 선물 상장 여부는 WebSearch만으로 확인해 완전하지 않을 수
있으며, 추적 거래소 직접 API 전수조회는 수행하지 않았다; (o) BEAT의 완전 반전이 일회성
되돌림인지 추세 전환인지는 다음 회차 추적이 필요하다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
