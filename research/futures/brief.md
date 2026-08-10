# 선물시장 스카우트 브리핑 — 2026-08-10 00:27 UTC (KST 2026-08-10 09:27)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-09T22:29:00Z)
> 로부터 약 1시간58분 경과, 날짜가 8월 10일 월요일로 넘어갔다.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 429를 두 차례 겪은 뒤 재시도로 확보 성공 — 총시총
**$2,301,950,720,101.87(약 $2.302T)**·BTC도미넌스 **56.69%**로 직전 회차($2.313T·56.64%)보다
시총은 소폭 하락, 도미넌스는 소폭 상승 — **9회 연속** 확보됐다(단 이번엔 재시도가 필요했다).

### ⚠️ Fear&Greed 30(Fear) — 12회차 연속 동일값 스트릭 종료

alternative.me API 정상 응답, **30(Fear)** — 직전 31에서 하락하며 12회차 연속 이어지던
동일값이 이번에 처음 바뀌었다.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM 개별조회)는 **30회차 연속** 방법론(`oiUsd`
필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을 유지했다.

## 이번 회차 최대 사건

### ⚠️⚠️⚠️⚠️⚠️ ACE — 언락 이후 첫 관측(추정), 전 소스 급격 개선

이번이 언락(8/10 00:00 UTC 추정) 이후 첫 관측이다. tokenomist를 WebFetch로 재확인한 결과
**8/10 언락 항목이 더 이상 표시되지 않고 다음 언락이 '2026년 9월 3일'**(Early Investors 대상)로
갱신돼 있으며(누적 언락량 107,613,807 ACE, 공급의 73.21%), 페이지 하단 '최종 갱신' 시각이
요청 시각과 거의 일치했다 — 이는 8/10 언락이 **집행됐음을 강하게 시사**하나, 명시적인 '집행
완료' 확인 문구는 페이지에서 찾지 못해 정직하게 **'집행 추정'**으로만 표기한다. 이 추정과
정합되게, 지난 여러 회차 동안 극심하게 동조 급락(직전 -17~-19%)했던 ACE 가격이 이번 회차
5개 소스 전원에서 뚜렷이 개선(반등)됐다: Binance **-14.783%**, Bybit **-15.537%**(가중
**-14.956%**), OrangeX **-15.475%**, Aster **-15.392%**, Hyperliquid **-14.117%**로
낙폭이 3~5%p씩 줄었다 — **'sell-the-news 소진 후 반등'** 패턴에 부합하는 모습이나 인과관계를
확정하지는 않는다. OI도 완만히 감소(Binance+Bybit 합산 $12.23M→$11.83M)해 대규모 청산
캐스케이드보다는 완만한 포지션 정리에 가깝다. OKX 직접조회로 ACE-USDT-SWAP를 재확인한 결과
이번 회차도 instId 자체가 존재하지 않아 OKX 미상장이 **30회차 연속** 재확인됐다.

### ⚠️⚠️ BEAT — 신고점 직후 급격 반전, 대폭 냉각

지난 회차 '신고점'(36~37%)에서 이번 회차 급격히 반전, 3소스 모두 9~14%대로 대폭
냉각됐다. OKX **37.43%→12.947%**, OrangeX **36.234%→14.225%**, Aster
**37.08%→9.398%** — 신고점 랠리가 하루를 못 버티고 대부분 반납됐다.

### ⚠️ BICO — 3회차 연속 악화 심화, 최대 낙폭 경신

3회차 연속 악화가 심화돼 이번 회차 **-28~-29%대**로 추적 이래 최대 낙폭을 기록했다.
OKX **-18.725%→-28.597%**, OrangeX **-19.601%→-28.308%**, Aster **-18.393%→-28.55%**로
기존 최대낙폭(약 -20%)을 큰 폭 상회했다.

## 직전 회차 강조 종목 추적 결과

- **① ACE — ⚠️⚠️⚠️⚠️⚠️ 언락 추정 집행 후 전 소스 급격 개선.** 위 '이번 회차 최대 사건' 참조.
- **② BEAT — ⚠️⚠️ 신고점 직후 급격 반전.** 위 참조.
- **③ BICO — ⚠️ 3회차 연속 악화 심화.** 위 참조.
- **④ KAITO — 혼조.** 가격은 OKX **-4.017%→-4.365%**·HL **-3.85%→-5.404%**로 소폭
  악화됐으나, 펀딩은 OKX **-0.451%→-0.332%**·HL **-0.223%→-0.167%**로 계속 개선돼 방향이
  엇갈렸다. 8/20 대형 언락 약 9.9일 앞 — ACE의 결말이 KAITO 사전 포지셔닝에 주는 함의는
  다음 회차 이후 지속 관찰이 필요하다.
- **⑤ BANK — ⚠️ 플러스 복귀가 재반전, 마이너스로.** Binance/Bybit 가중
  **+0.880%→-1.713%**(Binance -1.751%·Bybit -1.476%), Aster **+0.735%→-3.16%**, OrangeX
  **+0.063%→-2.842%**로 4소스 전원 재반전. 8/17 언락 약 6.9일 앞.
- **⑥ CASHCAT — 재가속 진정 지속.** HL **19.902%→8.06%**, OrangeX
  **19.896%→8.889%**, Aster **16.77%→7.959%**로 3거래소 모두 8~9%대까지 냉각됐다 — 직전
  온체인 회차(8/10 00:06Z)에서 CASHCAT 특기사항이 사라지고 TOAD가 새로 부상한 흐름과
  정합된다.

## TOAD 추적 결과 — 선물 미상장 확인

직전 온체인 회차에서 TOAD가 예외적으로 강하게 재점화(유동성 +32.5~35.7%, GeckoTerminal
solana 트렌딩 1위)했다는 보고를 받아, 이번 회차에서 WebSearch로 확인했다. **추적 중인
CEX(Binance·Bybit·OKX)·DEX(Hyperliquid·Aster·OrangeX·dYdX) 어디에도 TOAD의 선물 상장이
확인되지 않았다**(MEXC 등 비추적 거래소의 파생상품 일반 언급만 존재, 정확한 상장 여부는
불명확). 온체인 강세와 별개로 이번 회차 선물 데이터에서는 포착되지 않는 갭으로 기록한다.

## 기타 주요 변화

**AEON**은 3회차 연속 재악화가 심화됐다(OKX -7.604%→**-10.891%**, OrangeX
-7.25%→**-11.914%**, Aster -7.133%→**-10.652%**). **BSB**는 직전 회차의 첫 완화가 다시
반전돼 3소스 모두 재악화했다(OKX -9.869%→**-13.181%**, OrangeX -11.385%→**-12.911%**,
Aster -9.543%→**-12.354%**). **ALGO**는 전 소스(Binance/Bybit 가중·HL·OrangeX·Aster)에서
마이너스권이 뚜렷이 확대됐다(-2.6~3.9%→**-5.8~6.4%대**).

## 데이터 이슈 추적 결과

**HYNA:HYPE-USD**의 OI가 여러 회차 이어진 **$695,086.18 완전동일값 고정이 이번에 처음
깨져 $684,023.08로 변경**됐다 — 정상화 스트릭이 종료된 것으로 보인다. GIGGLE의 필드
순서역전이 **15회차 연속**, KAITO(OKX 직접)의 완전동일값이 **15회차 연속**, GRAM의
완전동일값이 **13회차 연속** 재현됐다 — 세 이상치 모두 여전히 견고하다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️⚠️⚠️⚠️ 언락 추정, 전원 개선] | Binance/Bybit(가중) | $103.52M | $11.83M | +0.001% | -14.956% | 낙폭 3~5%p 축소, 5소스 전원 개선 | unlock-presumed-executed-all-sources-improve |
| **BICO** [⚠️⚠️ 3회차 악화, 최대낙폭] | OKX(CoinGecko정상, okex_swap) | $507.61M | $9.22M | -0.171% | -28.597% | -18.725%→-28.597%, 3소스 신저점 | worsening-continues-new-record-low |
| **BEAT** [⚠️⚠️ 신고점 급반전] | OKX(CoinGecko정상, okex_swap) | $368.18M | $10.52M | +0.005% | +12.947% | 37.43%→12.947%, 3소스 급냉각 | reverses-sharply-from-new-high |
| **KAITO** [혼조] | OKX(직접API) | $79.81M | $7.93M | -0.332% | -4.365% | 가격 소폭 악화, 펀딩 개선. 8/20 언락 9.9일 앞 | mixed-price-funding-signals |
| **BANK** [⚠️ 마이너스 재반전] | Binance/Bybit(가중) | $117.42M | $18.71M | +0.003% | -1.713% | +0.880%→-1.713%, 4소스 전원 재반전 | whipsaw-back-to-negative |
| MMT [플러스 유지, 냉각] | OKX(직접API) | $81.87M | $3.38M | -0.041% | +0.445% | +1.031%→+0.445% | positive-holds-mild-cooling |
| BSB [완화 반전, 재악화] | OKX(CoinGecko정상, okex_swap) | $5.99M | $2.52M | +0.005% | -13.181% | -9.869%→-13.181% | brief-easing-reverses-worsens |
| AAVE [플러스 유지, 냉각] | Binance/Bybit(가중) | $42.03M | $87.92M | +0.002% | +0.145% | +0.574%→+0.145% | positive-holds-mild-cooling |
| ALLO [거의 유지] | Binance/Bybit(가중) | $22.21M | $18.16M | +0.005% | -5.766% | -5.460%→-5.766% | roughly-flat-within-negative |
| ADA [14회차 마이너스] | Binance/Bybit(가중, USDT만) | $141.04M | $167.62M | +0.009% | -1.428% | -0.497%→-1.428% | fourteenth-round-negative-mild-worsening |
| AKE [개선 지속, 냉각] | Binance/Bybit(가중) | $40.68M | $39.28M | +0.039% | +5.775% | +7.492%→+5.775% | improvement-continues-mild-cooling |
| GIGGLE [마이너스 확대] | OKX(직접API) | $25.43M | $2.66M | +0.005% | -4.425% | -2.372%→-4.425%. ⚠️ 필드 이상치 15회차 연속 | worsens-within-negative-field-anomaly-15th-round |
| PIPPIN [플러스 확대] | OKX(직접API) | $1.96M | $1.91M | +0.035% | +3.976% | +2.396%→+3.976% | extends-positive-continues |
| 1000RATS [플러스 유지, 냉각] | Binance/Bybit(가중) | $13.47M | $18.72M | +0.026% | +4.833% | +5.330%→+4.833% | extends-positive-mild-cooling |
| AIO [플러스권 거의 유지] | Binance/Bybit(가중) | $11.40M | $4.59M | +0.037% | +0.638% | +0.695%→+0.638% | roughly-flat-positive |
| GRAM [마이너스 소폭 확대] | OKX(직접API) | $2.94M | $6.44M | +0.005% | -2.357% | -1.763%→-2.357%. ⚠️ 필드 이상치 13회차 연속 | mild-worsening-within-negative-field-anomaly-13th-round |
| AEON [⚠️ 3회차 재악화 심화] | OKX(CoinGecko정상, okex_swap) | $24.16M | $3.65M | +0.005% | -10.891% | -7.604%→-10.891% | worsening-continues-third-round |
| ATOM [플러스→마이너스 전환] | Binance/Bybit(가중) | $8.99M | $28.29M | +0.003% | -0.237% | +0.629%→-0.237% | turns-negative-from-positive |
| ASTER [플러스 확대] | Binance/Bybit(가중) | $21.09M | $115.23M | +0.005% | +2.283% | +1.765%→+2.283%, DEX도 동조 확대 | extends-positive-continues |
| CORE [초저유동성, 냉각] | OKX(CoinGecko정상, okex_swap) | $1.88M | $1.02M | +0.010% | +3.426% | +4.824%→+3.426% | low-liquidity-mild-cooling |
| CAP [플러스 확대] | OKX(CoinGecko정상, okex_swap) | $17.31M | $2.33M | +0.005% | +8.327% | +6.346%→+8.327% | extends-positive |
| ALGO [⚠️ 마이너스 확대 심화] | Binance/Bybit(가중) | $14.56M | $14.85M | +0.010% | -5.832% | -2.676%→-5.832%, DEX도 동조 악화 | worsens-within-negative |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [⚠️⚠️⚠️⚠️⚠️ 급격 개선] | Hyperliquid | $2.61M | $1.33M | -0.003% | -14.117% | -19.386%→-14.117% | unlock-presumed-executed-improves |
| **ACE-USDT-PERPETUAL** [개선] | OrangeX | $53.52M | $17.53M | +0.020% | -15.475% | -17.149%→-15.475% | unlock-presumed-executed-improves |
| **ACE-USDT** [개선] | Aster | $0.43M | $0.05M | +0.001% | -15.392% | -17.963%→-15.392% | unlock-presumed-executed-improves |
| BEAT-USDT-PERPETUAL [신고점 급반전] | OrangeX | $18.21M | $6.80M | +0.010% | +14.225% | 36.234%→14.225% | reverses-sharply-from-new-high |
| BEAT-USDT [신고점 급반전] | Aster | $3.83M | $4.20M | +0.008% | +9.398% | 37.08%→9.398% | reverses-sharply-from-new-high |
| **BICO-USDT-PERPETUAL** [⚠️ 3회차 악화] | OrangeX | $257.41M | $72.77M | +0.012% | -28.308% | -19.601%→-28.308% | worsening-continues-new-record-low |
| **BICO-USDT** [⚠️ 3회차 악화] | Aster | $4.29M | $0.31M | -0.002% | -28.55% | -18.393%→-28.55% | worsening-continues-new-record-low |
| **CASHCAT** [진정 지속] | Hyperliquid | $18.80M | $20.96M | +0.030% | +8.06% | 19.902%→8.06%, 온체인은 TOAD로 이동 | reacceleration-cools-continues-onchain-shifts-to-toad |
| CASHCAT-USDT-PERPETUAL [진정 지속] | OrangeX | $0.14M | $0.06M | -0.010% | +8.889% | 19.896%→8.889% | reacceleration-cools-continues |
| CASHCAT-USDT [진정 지속] | Aster | $1.93M | $1.44M | +0.001% | +7.959% | 16.77%→7.959% | reacceleration-cools-continues |
| ALLO-USDT [거의 유지] | Aster | $0.08M | $0.03M | 0.000% | -5.245% | -5.377%→-5.245% | roughly-flat-negative |
| ALLO-USDT-PERPETUAL [거의 유지] | OrangeX | $15.05M | $4.75M | +0.010% | -5.367% | -5.29%→-5.367% | roughly-flat-negative |
| AAVE-USDT-PERPETUAL [손익분기 근접] | OrangeX | $23.10M | $8.30M | +0.010% | -0.099% | +0.361%→-0.099% | cools-toward-breakeven |
| AAVE-USDT [플러스 유지, 냉각] | Aster | $0.40M | $4.59M | +0.010% | +0.088% | +0.535%→+0.088% | positive-holds-mild-cooling |
| AAVE-USD [플러스 유지, 냉각] | Hyperliquid | $3.03M | $60.86M | +0.001% | +0.17% | +0.64%→+0.17% | positive-holds-mild-cooling |
| ADA-USDT-PERPETUAL [마이너스 확대] | OrangeX | $78.21M | $27.74M | +0.010% | -1.363% | -0.851%→-1.363% | worsens-within-negative |
| ADA-USDT [마이너스 확대] | Aster | $0.42M | $1.67M | +0.010% | -1.709% | -0.35%→-1.709% | worsens-within-negative |
| ADA-USD [마이너스 확대] | Hyperliquid | $2.89M | $32.56M | +0.001% | -1.579% | -0.231%→-1.579% | worsens-within-negative |
| BANK-USDT-PERPETUAL [⚠️ 마이너스 반전] | OrangeX | $8.12M | $2.80M | -0.010% | -2.842% | +0.063%→-2.842% | whipsaw-back-to-negative |
| BANK-USDT [⚠️ 마이너스 반전] | Aster | $0.57M | $0.35M | +0.001% | -3.16% | +0.735%→-3.16% | whipsaw-back-to-negative |
| AKE-USDT-PERPETUAL [개선 지속, 냉각] | OrangeX | $5.77M | $2.21M | +0.026% | +5.21% | +7.278%→+5.21% | improves-mild-cooling |
| AKE-USDT [개선 지속, 냉각] | Aster | $0.56M | $11.35M | +0.016% | +6.872% | +7.918%→+6.872% | improves-mild-cooling |
| CAP-USDT [플러스 확대] | Aster | $0.03M | $0.12M | +0.001% | +8.336% | +8.038%→+8.336% | extends-positive |
| CAP-USDT-PERPETUAL [플러스 확대] | OrangeX | $0.47M | $0.19M | -0.010% | +9.254% | +6.533%→+9.254% | extends-positive |
| ALGO-USDT-PERPETUAL [악화 심화] | OrangeX | $8.09M | $2.84M | +0.010% | -5.95% | -2.86%→-5.95% | worsens-within-negative |
| ALGO-USDT [초저유동성, 악화 심화] | Aster | $0.03M | $0.02M | +0.001% | -6.431% | -3.936%→-6.431% | low-liquidity-worsens |
| ALGO-USD [악화 심화] | Hyperliquid | $0.95M | $1.95M | +0.001% | -5.893% | -2.62%→-5.893% | worsens-within-negative |
| ATOM-USDT-PERPETUAL [플러스→마이너스] | OrangeX | $5.08M | $1.79M | +0.010% | -0.723% | +0.578%→-0.723% | turns-negative-from-positive |
| ATOM-USDT [초저유동성, 마이너스 확대] | Aster | $0.01M | $1.60M | +0.010% | -0.65% | -0.289%→-0.65% | low-liquidity-worsens |
| ATOM-USD [플러스→마이너스] | Hyperliquid | $0.19M | $1.93M | +0.001% | -0.325% | +0.657%→-0.325% | turns-negative-from-positive |
| ASTER-USDT-PERPETUAL [플러스 확대] | OrangeX | $8.78M | $3.06M | +0.010% | +2.242% | +1.705%→+2.242% | extends-positive |
| ASTER-USDT [대형 OI 플러스 확대] | Aster | $12.64M | $224.08M | +0.011% | +2.237% | OI $223.05M→$224.08M, +1.572%→+2.237% | large-oi-extends-positive |
| ASTER-USD [플러스 확대] | Hyperliquid | $1.11M | $15.23M | +0.001% | +2.168% | +1.798%→+2.168% | extends-positive |
| KAITO-USD [혼조] | Hyperliquid | $20.21M | $14.20M | -0.167% | -5.404% | -3.85%→-5.404%, 펀딩은 -0.223%→-0.167%로 개선 | mixed-price-funding-signals |
| GRAM-USD [소폭 악화] | Hyperliquid | $0.62M | $12.71M | +0.001% | -2.251% | -1.446%→-2.251% | roughly-flat-matches-okx |
| HYPE-USD [소폭 악화] | Hyperliquid | $85.79M | $1,181.79M | -0.001% | -1.72% | -0.815%→-1.72% | mild-worsening |
| HYPER-USD [플러스→마이너스] | Hyperliquid | $0.10M | $0.31M | +0.001% | -0.312% | +0.339%→-0.312% | turns-negative |
| APEX-USD [플러스→마이너스, Bybit 근접] | Hyperliquid | $0.08M | $0.76M | +0.001% | -0.322% | +1.053%→-0.322%, Bybit -0.321% | turns-negative-bybit-matches |
| FARTCOIN [재가속 진정] | Hyperliquid | $6.61M | $22.37M | +0.001% | +1.524% | +3.348%→+1.524% | reacceleration-cools |
| ETHFI-USD [플러스 유지, 냉각] | Hyperliquid | $0.65M | $8.31M | +0.001% | +0.277% | +1.832%→+0.277% | positive-holds-mild-cooling |
| ETH-USD [플러스 유지, 냉각] | dYdX | $5.53M | $8.84M | 0.000% | +0.292% | +0.578%→+0.292% | positive-holds-mild-cooling |
| BTC-USD [플러스 유지, 냉각] | dYdX | $1.44M | $17.84M | 0.000% | +0.251% | +0.447%→+0.251% | positive-holds-mild-cooling |
| SOL-USD [플러스 유지, 냉각] | dYdX | $0.14M | $4.54M | 0.000% | +1.291% | +1.523%→+1.291% | positive-holds-mild-cooling |
| ANSEM [마이너스 확대] | Aster | $0.24M | $0.88M | +0.001% | -5.198% | -3.036%→-5.198% | worsens-within-negative |
| ANSEM-USDT-PERPETUAL [마이너스 확대] | OrangeX | $0.48M | $0.16M | +0.010% | -5.475% | -2.781%→-5.475% | worsens-within-negative |
| **BTW** [고점 냉각 지속] | Aster | $2.54M | $15.15M | +0.041% | +5.241% | +8.453%→+5.241% | mild-cooling-continues |
| HYNA:PUMP-USD [거의 유지] | Hyperliquid | $0.05M | $0.18M | +0.001% | +14.812% | +14.022%→+14.812% | roughly-flat |
| **HYNA:HYPE-USD** [⚠️ OI 스트릭 종료] | Hyperliquid | $0.14M | $0.68M | +0.010% | -2.107% | $695,086.18→$684,023.08 — 정상화 스트릭 첫 붕괴 | oi-static-streak-ends |
| AEON-USDT-PERPETUAL [악화 심화] | OrangeX | $0.46M | $0.16M | +0.010% | -11.914% | -7.25%→-11.914% | worsening-continues-third-round |
| AEON-USDT [악화 심화] | Aster | $0.09M | $0.21M | +0.009% | -10.652% | -7.133%→-10.652% | worsening-continues-third-round |
| **BSB-USDT-PERPETUAL** [재악화] | OrangeX | $11.30M | $3.77M | +0.010% | -12.911% | -11.385%→-12.911% | brief-easing-reverses-worsens |
| **BSB-USDT** [재악화] | Aster | $0.05M | $0.10M | +0.001% | -12.354% | -9.543%→-12.354% | brief-easing-reverses-worsens |
| 1000RATS-USDT [플러스 유지, 냉각] | Aster | $0.10M | $0.04M | +0.012% | +4.144% | +6.095%→+4.144% | extends-positive-mild-cooling |
| **BLESS** [거의 유지] | OrangeX | $88.68M | $28.02M | +0.065% | -11.16% | -11.89%→-11.16% | roughly-flat-negative |
| **BLESS-USDT** [거의 유지] | Aster | $0.34M | $0.21M | +0.005% | -11.37% | -11.487%→-11.37% | roughly-flat-negative |

## 테마 태그

1. **시장 전반: `/global`이 429 재시도 끝에 9회 연속 확보 성공 — 총시총 $2.302T(소폭 하락)·BTC도미넌스 56.69%(소폭 상승)** (global-api-ninth-round-needed-retry).
2. **⚠️ Fear&Greed 30(Fear) — 직전 31에서 하락, 12회차 연속 동일값 스트릭 종료** (fear-greed-drops-to-30-streak-ends).
3. **⚠️⚠️⚠️⚠️⚠️ ACE: 언락 이후 첫 관측(추정). tokenomist 갱신으로 집행을 강하게 시사, 5소스 전원 낙폭 3~5%p 축소(가중 -18.653%→-14.956%)** (ace-unlock-presumed-executed-all-sources-improve).
4. **⚠️⚠️ BEAT: 신고점(36~37%)에서 급격히 반전, 3소스 모두 9~14%대로 대폭 냉각** (beat-reverses-sharply-from-new-high).
5. **⚠️ BICO: 3회차 연속 악화 심화, -28~-29%대로 추적 이래 최대 낙폭 경신** (bico-worsening-continues-new-record-low).
6. **KAITO: 가격 소폭 악화·펀딩은 계속 개선으로 혼조. 8/20 언락 약 9.9일 앞** (kaito-mixed-price-funding-signals).
7. **⚠️ BANK: 플러스 복귀가 재반전, 4소스 전원 마이너스로 회귀. 8/17 언락 약 6.9일 앞** (bank-whipsaw-back-to-negative).
8. **CASHCAT: 재가속 진정 지속(8~9%대) — 온체인에서 TOAD로 관심 이동과 정합** (cashcat-reacceleration-cools-continues-onchain-shifts-to-toad).
9. **TOAD: 추적 중인 CEX·DEX 어디에도 선물 상장 미확인 — 온체인 강세와 별개 데이터 갭** (toad-not-listed-on-tracked-futures-venues).
10. **⚠️ AEON: 3회차 연속 재악화 심화(-7%대→-11%대)** (aeon-worsening-continues-third-round).
11. **⚠️ BSB: 첫 완화가 다시 반전, 3소스 재악화** (bsb-brief-easing-reverses-worsens).
12. **⚠️ ALGO: 전 소스에서 마이너스권 뚜렷이 확대(-2.6~3.9%→-5.8~6.4%대)** (algo-worsens-within-negative-all-sources).
13. **⚠️ HYNA:HYPE-USD: 여러 회차 이어진 OI 완전동일값 고정이 이번에 처음 깨짐** (hyna-hype-oi-static-streak-ends).
14. **⚠️ GIGGLE 필드 이상치 15회차 연속, KAITO(OKX 직접) 완전동일값 15회차 연속, GRAM 13회차 연속 재현** (field-anomalies-15th-13th-round-continue).
15. **OKX ACE·BANK·1000RATS·AIO·KAITO·MMT·PIPPIN·GIGGLE·GRAM은 okex_swap 미등재(ACE는 instId 자체 부재), 직접 API/DEX로 보강** (okx-most-still-not-listed-direct-api-supplements).
16. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
17. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
18. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
19. **ACE 언락 결말 사례를 여러 회차 추적한 결과, 언락 이후(추정) 5개 소스 전원이 개선돼 'sell-the-news 소진 후 반등' 패턴에 부합하나 tokenomist 명시적 집행 확인문구 부재로 완전 확정은 아님** (ace-unlock-conclusion-tentative-recovery-pattern).

## 데이터 신뢰도

**CoinGecko binance_futures**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS
확인. **BICO·BEAT·BSB·APEX·BTW·KAITO·CASHCAT·MMT·GIGGLE·PIPPIN·GRAM·CORE·CAP·AEON·BLESS·
ANSEM은 이번 회차도 명확히 미확인**(단순 미상장).

**CoinGecko bybit**: ACE·AAVE·ALLO·ADA·BANK·AKE·AIO·ATOM·ASTER·ALGO·1000RATS·APEX 확인.
나머지는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: AAVE·ALLO·ADA·ALGO·AEON·ATOM·ASTER·CORE·BSB·CAP·BICO·BEAT 확인.
ACE·BANK·AKE·1000RATS·AIO·GRAM·KAITO·MMT·PIPPIN·BLESS·CASHCAT은 이번 회차도 okex_swap
배열에서 미발견돼 OKX 직접 API 또는 DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접 확인.
`oiUsd` 필드 직접 사용 방법론을 **30회차 연속** 유지, vol24_usd=`volCcy24h`×`last` 계산
방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️ **ACE-USDT-SWAP는 OKX에 instId
자체가 존재하지 않음**을 이번 회차도 직접 확인(에러코드 51001), okex_swap 미등재가
CoinGecko 집계 지연이 아니라 실제 미상장임이 재확인됐다. **GIGGLE**은 vol24h/volCcy24h
필드 순서역전이 **15회차 연속**, **KAITO**는 vol24h=volCcy24h 완전동일값 이상치가
**15회차 연속**, **GRAM**도 완전동일값이 **13회차 연속** 재현됐다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·ETHFI·
ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD·BTC·ETH 등 raw 정밀값 확보. **SOL은 HL에서 이번 회차
미확인**(기존 dYdX로 대체 집계). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·BTW·BLESS·ANSEM은
HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·CAP·
BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON 전량 확보(raw 정밀값). MMT·GIGGLE·
PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·
CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값). BTW는 이번 회차도 OrangeX에서 미발견(기존과
동일, Aster에서만 확인). KAITO·1000RATS·GRAM·MMT·PIPPIN·GIGGLE·CORE는 여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $1.44M/OI $17.84M, ETH-USD $5.53M/OI $8.84M,
SOL-USD $0.14M/OI $4.54M) 확보.

**CoinGecko `/global`**: 429를 두 차례 겪은 뒤 재시도로 총시총 $2,301,950,720,101.87(약
$2.302T)·BTC도미넌스 56.69%를 확인했다. 직전 회차($2.313T·56.64%)보다 시총은 소폭 하락,
도미넌스는 소폭 상승, **9회 연속** 확보됐으나(단 이번엔 재시도 필요).

**Fear&Greed**: alternative.me API로 정상 응답, **30(Fear)** 확인 — 직전 31에서 하락하며
**12회차 연속** 이어지던 동일값이 이번에 처음 바뀌었다.

**TOAD**: WebSearch로 확인한 결과 추적 중인 CEX·DEX 어디에서도 선물 상장 근거를 찾지
못했다(MEXC 등 비추적 거래소의 일반적 파생 언급만 존재). '미상장/미확인'으로 정직하게 표기.

**신규 발견**: (a) tokenomist 재확인 결과 ACE의 8/10 언락 항목이 사라지고 다음 언락이
9/3로 갱신돼 언락 집행을 강하게 시사하며, 이와 정합되게 5개 소스 전원 가격이 뚜렷이
개선됐다 — 다만 명시적 '집행 완료' 문구는 확인하지 못해 완전 확정은 아니다. (b) BEAT가
신고점(36~37%) 직후 하루 만에 급격히 반납(9~14%대)했다 — 신고점 자체가 지속성이 낮았을
가능성을 시사한다. (c) HYNA:HYPE-USD의 OI가 여러 회차 이어진 완전동일값 고정에서 벗어나
처음으로 변동했다 — 이전 회차들의 '정상화 완료' 판단이 API 갱신 지연이었을 가능성을
시사한다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(30회차 연속 일관 적용); (d) ACE·ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소 값은
본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상 스케일로
관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·
GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만 집계되는 구조이며,
이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·ANSEM·HYNA:PUMP-USD·
HYNA:HYPE-USD·BLESS는 DEX에서만 상장이 확인돼 해당 섹션에서만 집계했다; (h) ACE 언락
집행 여부는 tokenomist 페이지의 '다음 언락' 항목 변경(8/10 사라짐→9/3로 갱신)을 근거로
**추정**한 것이며, 명시적인 '집행 완료' 로그·타임스탬프는 확보하지 못했다 — 완전한 확정은
아니다; (i) BICO의 소스 간 격차·악화 추세가 3회차 연속 이어지고 있으며, 근본 원인(상장
거래소별 유동성 구조·공급 이벤트 등)은 규명하지 않았다; (j) KAITO 8/20 언락 규모는
소스별로 공급 3.3%~7.63%·$22.9M~$34.68M로 편차가 있어 정확한 수치는 확정하지 않았다;
(k) GIGGLE·KAITO의 필드 이상치가 15회차 연속, GRAM도 13회차 연속 재현돼 구조적 패턴으로
굳어졌으나 근본 원인(OKX API 자체 특성인지)은 규명하지 않았다; (l) HYNA:HYPE-USD의 OI
변동이 실제 시장 활동 재개 때문인지, 단순 API 캐시 갱신 때문인지는 구분하지 않았다;
(m) `/global`은 이번 회차 429 재시도 끝에 확보돼 9회 연속 성공은 유지했으나 매 회차
순조로운 것은 아니다; (n) TOAD의 선물 상장 여부는 WebSearch만으로 확인해 완전하지 않을 수
있으며, 추적 거래소 직접 API 전수조회는 수행하지 않았다; (o) BEAT의 신고점 급반전이
일회성 되돌림인지 추세 전환인지는 다음 회차 추적이 필요하다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
