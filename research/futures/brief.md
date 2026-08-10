# 선물시장 스카우트 브리핑 — 2026-08-10 14:40 UTC (KST 2026-08-10 23:40)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-10T12:57:00Z)
> 로부터 약 1시간43분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 2회 429 후 3차 시도로 확보 — 총시총 **$2,294,736,154,176.85(약
$2.295T)**·BTC도미넌스 **56.64%**로 직전 회차($2.298T·56.660%)보다 시총·도미넌스 모두
추가 하락, **15회차 연속** 확보됐다.

### Fear&Greed 30(Fear) — 직전과 동일, 7회차 연속

alternative.me API 정상 응답, **30(Fear)** — 직전 회차(30)에서 변동 없이 유지, 7회차
연속 30을 이어가고 있다.

### 데이터 확보 상황

OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM 개별조회)는 **36회차 연속** 방법론
(`oiUsd` 필드 직접 사용, `vol24_usd=volCcy24h×last`, `chg24=(last-open24h)/open24h`)을
유지했다. **BSB는 이번 회차 OKX CoinGecko(`okex_swap`)에서 재발견돼 원래 소스로
복귀**했다. OKX BANK-USDT-SWAP은 instId 자체가 존재하지 않아(에러코드 51001) 미상장이
재확인됐다 — BANK는 OKX 자체에 상장이 없는 것으로 반복 확인되며, ACE·TUT·TOAD의
'거래소 자체 미상장' 사례와 같은 종류다. Binance 대량 티커 목록에서 BANK를 검색할 때
최초 요약이 목록 중간에서 잘리는 사례가 **3회차째 재발**해 개별 타겟 검색으로
확인했다(vol $52.01M·OI $13.27M·chg -9.035%).

## 이번 회차 최대 사건

### ⚠️⚠️⚠️ BANK — 급락 후 부분 반등, 여전히 深마이너스

직전 회차의 급락(-17.182%)에서 이번 회차 부분 반등이 나타났다: Binance/Bybit 가중
**-17.182%→-8.947%**(Binance -9.035%, Bybit -8.345%), OrangeX **-16.33%→-10.491%**,
Aster **-15.975%→-9.14%**로 전 소스 동조 반등해 낙폭이 절반 가까이 줄었다. 다만 펀딩은
**-0.039%→-0.038%**로 거의 그대로 숏 우위를 유지했고, OI도 결합 **$18.83M→$18.66M**로
거의 유지돼 대량 청산이 아닌 가격 반등으로 해석된다. WebSearch로 확인한 결과 BANK
(Lorenzo Protocol)는 7월 한 달간 폭발적 랠리(하루 98% 상승, ATH $0.27 근접) 이후 8월
들어 프로핏테이킹·레버리지 청산·약한 현물수요·지지선 붕괴가 겹쳐 하락이 심화된 것으로
나타났으며, 집중지분·불트랩 우려도 함께 언급됐다 — 다만 오늘 시점의 구체적 단일 촉매
(해킹·공지 등)는 여전히 확인되지 않았다. **8/17 대형 언락 약 6.1일 앞.**

### ⚠️⚠️ AAVE — 손익분기권 안정화가 하루 만에 전면 반전

직전 회차 '전 소스 플러스 회복'이 이번 회차 완전히 뒤집혔다: 가중 **+0.325%→-0.647%**,
HL **+0.581%→-0.621%**, Aster **+0.472%→-0.6%**, OrangeX **+0.066%→-0.709%**로 전
소스가 동시에 마이너스로 돌아섰다 — 뚜렷한 촉매 없는 전방위 반전이다.

### ⚠️ ADA — 처음으로 전 소스(6개) 마이너스 완전 수렴

직전 회차의 혼조(Binance·HL 플러스 vs Bybit·OKX·OrangeX 마이너스)가 이번 회차 전
소스 마이너스로 수렴됐다: 가중 **+0.048%→-0.631%**(Binance -0.709%·Bybit -0.456%),
OKX **-0.557%**, HL도 **+0.163%→-0.416%**로 재반전, Aster **-0.051%→-0.558%**,
OrangeX **-0.204%→-0.658%**로 6개 소스가 처음으로 한 방향에 완전히 정렬됐다.

## 직전 회차 강조 종목 추적 결과

- **① BICO — ⚠️⚠️ 소스 간 방향 완전 분리.** OKX **-5.845%→-0.783%**·Aster
  **-5.748%→-1.148%**로 손익분기권까지 개선을 이어갔으나, **OrangeX(DEX)만
  -12.848%→+4.156%로 급격히 플러스 전환**(펀딩은 +0.177%→+0.176%로 유지)됐다 — CEX·
  Aster의 완만한 회복과 OrangeX의 급반전이 공존하는 드문 괴리다.
- **② BEAT — 재악화 3회차 연속.** OKX **-26.777%→-31.361%**, OrangeX
  **-28.479%→-32.145%**, Aster **-26.78%→-32.318%**로 3소스 동조 심화가 이어졌다.
- **③ KAITO — 가격 거의 유지, 펀딩은 소스별로 갈림.** 가격 **-3.531%→-3.594%**로 거의
  유지됐으나, OKX 펀딩은 **-0.596%→-0.723%**로 악화된 반면 HL 펀딩은
  **-0.300%→-0.293%**로 소폭 개선됐다 — 8/20 대형 언락 약 **9.1일** 앞, 전반적으로
  숏 우위는 지속.
- **④ BSB — ⚠️ 첫 플러스 전환이 하루 만에 재역전.** OKX(CoinGecko 재발견)
  **+1.211%→-1.666%**, OrangeX **+0.606%→-0.535%**로 동조 반전됐다 — 수개월만의
  방향 전환이 무너졌다.
- **⑤ CASHCAT — ⚠️ 세 소스 괴리가 완전히 해소됐다.** HL **36.244%→15.962%**,
  OrangeX **25.081%→16.693%**, Aster **33.007%→17.416%**로 전 소스가 15.96~17.42%
  범위로 수렴 냉각됐다 — 직전 온체인 회차(14:07Z)의 'OrangeX 냉각 서사와 부합' 관측이
  이번엔 전 소스로 확산됐다.

## 신규/추가 발견

### MMT — 재역전 후 낙폭 진정

**-4.633%→-4.429%**로 거의 유지됐고, 펀딩이 **-0.001%→+0.004%**로 플러스 전환됐다 —
재역전 후 낙폭이 진정되는 조짐이다.

### dYdX — BTC·SOL 재반전 마이너스, 3종목 전부 마이너스 전환

ETH-USD **-0.469%→-1.242%**로 마이너스 심화, BTC-USD **+0.017%→-0.493%**·SOL-USD
**+0.432%→-0.183%**로 각각 재반전돼 3종목 모두 마이너스로 전환됐다 — 직전 회차의
개별 방향성이 모두 되돌려졌다.

### HYPE·ETHFI·HYNA:PUMP — 강한 플러스에서 급격히 냉각

HYPE-USD **+1.444%→+0.169%**, ETHFI-USD **+1.966%→+0.255%**, HYNA:PUMP-USD
**+4.009%→+0.334%**로 세 종목 모두 손익분기권 근접까지 급격히 냉각됐다.

### CAP — 냉각 후 재가열

**+14.695%→+14.747%**로 거의 유지, OrangeX **+12.645%→+15.204%**·Aster
**+12.979%→+14.315%**로 3소스 동조 재가열됐다.

### AEON — 개선 5회차 연속

OKX **-2.889%→-2.010%**, OrangeX **-3.886%→-3.269%**, Aster **-3.79%→-1.349%**로
3소스 동조 개선이 이어졌다.

## 데이터 이슈 추적 결과

GIGGLE 필드 이상치(vol24h=40,147,320 vs volCcy24h=401,473.2, 100배 스케일 차이)가
**21회차 연속**, KAITO(OKX 직접, vol24h=volCcy24h=100,973,758) 완전동일값 이상치가
**21회차 연속**, GRAM(vol24h=volCcy24h=2,557,083) 완전동일값 이상치가 **19회차 연속**
재현됐다. MMT·PIPPIN의 10배 스케일 비율이 이번 회차도 재현돼 **5회차 연속**으로
이어졌다. HYNA:HYPE-USD의 OI는 이번 회차도 정상 갱신을 이어갔다($694,788.70→
**$690,733.58**, 소폭 감소) — 정상화 **7회차 연속**.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BANK** [⚠️⚠️⚠️ 부분 반등] | Binance/Bybit(가중) | $59.56M | $18.66M | -0.038% | -8.947% | -17.182%→-8.947%, 낙폭 절반 축소. 8/17 언락 6.1일 앞 | partial-bounce-still-deeply-negative |
| **AAVE** [⚠️⚠️ 전 소스 동시 반전] | Binance/Bybit(가중) | $47.62M | $88.35M | +0.001% | -0.647% | +0.325%→-0.647%, 전 소스 마이너스 전환 | reverses-negative-across-all-sources |
| **ADA** [⚠️ 첫 완전 수렴] | Binance/Bybit(가중, USDT만) | $146.35M | $168.38M | +0.009% | -0.631% | 가중 +0.048%→-0.631%, 6소스 첫 완전 정렬 | converges-negative-first-full-alignment |
| BICO [개선지속, DEX 갈림] | OKX(CoinGecko정상, okex_swap) | $236.44M | $7.95M | -0.073% | -0.783% | -5.845%→-0.783%, OrangeX만 +4.156% 급반전 | recovery-continues-orangex-spikes-positive |
| KAITO [가격유지, 펀딩갈림] | OKX(직접API) | $65.55M | $7.88M | -0.723% | -3.594% | 펀딩 -0.596%→-0.723%. 8/20 언락 9.1일 앞 | price-flat-funding-diverges-by-source |
| MMT [낙폭 진정] | OKX(직접API) | $37.08M | $3.34M | +0.004% | -4.429% | -4.633%→-4.429%, 펀딩 플러스 전환 | decline-steadies-funding-turns-positive |
| BEAT [재악화 3회차 연속] | OKX(CoinGecko정상, okex_swap) | $278.20M | $8.36M | -0.002% | -31.361% | -26.777%→-31.361% | worsening-continues-3rd-round |
| **BSB** [⚠️ 재역전 마이너스] | OKX(CoinGecko정상, 원소스 복귀) | $6.63M | $2.60M | +0.007% | -1.666% | +1.211%→-1.666% | reverses-negative-again-after-first-positive |
| AKE [심화 지속] | Binance/Bybit(가중) | $38.53M | $36.88M | +0.042% | -3.100% | -2.818%→-3.100% | negative-deepens-continues |
| ATOM [냉각, 소스갈림] | Binance/Bybit(가중) | $8.84M | $28.64M | +0.009% | +0.335% | +0.654%→+0.335%, Aster 재반전 마이너스 | cools-mixed-across-sources |
| ALLO [개선 지속] | Binance/Bybit(가중) | $21.29M | $17.98M | +0.005% | -1.392% | -2.077%→-1.392% | improvement-continues |
| GIGGLE [거의 유지, 이상치 21회차] | OKX(직접API) | $13.69M | $2.29M | +0.005% | -1.758% | -1.594%→-1.758% | roughly-flat-field-anomaly-21st-round |
| PIPPIN [유지, 10x 5회차] | OKX(직접API) | $3.33M | $1.81M | +0.025% | +3.077% | +2.946%→+3.077% | holds-positive-10x-pattern-5th-round |
| 1000RATS [개선] | Binance/Bybit(가중) | $11.32M | $17.65M | +0.065% | -3.801% | -5.156%→-3.801% | improves-within-negative |
| AIO [롤러코스터, 유지] | Binance/Bybit(가중) | $9.93M | $4.51M | +0.024% | +7.819% | +7.934%→+7.819% | rollercoaster-continues-roughly-flat |
| GRAM [유지, 이상치 19회차] | OKX(직접API) | $3.40M | $6.38M | +0.005% | -0.821% | -0.672%→-0.821% | roughly-flat-field-anomaly-19th-round |
| AEON [개선 5회차 연속] | OKX(CoinGecko정상, okex_swap) | $9.44M | $3.67M | +0.005% | -2.010% | -2.889%→-2.010% | improvement-continues-5th-round |
| ASTER [플러스 유지] | Binance/Bybit(가중) | $27.52M | $112.68M | +0.005% | +0.774% | +0.757%→+0.774% | holds-positive-roughly-flat |
| CORE [거의 유지] | OKX(CoinGecko정상, okex_swap) | $1.73M | $0.98M | +0.010% | -0.549% | -0.348%→-0.549%, 초저유동성 | roughly-flat-low-liquidity |
| CAP [냉각 후 재가열] | OKX(CoinGecko정상, okex_swap) | $129.58M | $4.11M | -0.011% | +14.747% | +14.695%→+14.747% | reheats-after-cooling |
| ALGO [개선 지속] | Binance/Bybit(가중) | $20.52M | $15.18M | +0.005% | -2.919% | -3.851%→-2.919% | improvement-continues |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| ACE-USD [개선] | Hyperliquid | $1.65M | $1.38M | +0.001% | -4.408% | -5.361%→-4.408% | improves-slightly |
| ACE-USDT-PERPETUAL [개선] | OrangeX | $29.30M | $9.61M | +0.010% | -4.882% | -7.188%→-4.882% | improves-slightly |
| ACE-USDT [소폭 재악화] | Aster | $0.21M | $0.02M | +0.001% | -6.059% | -5.558%→-6.059% | worsens-slightly |
| BEAT-USDT-PERPETUAL [재악화 3회차] | OrangeX | $17.94M | $4.77M | -0.034% | -32.145% | -28.479%→-32.145% | worsening-continues-3rd-round |
| BEAT-USDT [재악화 심화] | Aster | $7.61M | $0.77M | -0.004% | -32.318% | -26.78%→-32.318% | worsening-continues-3rd-round |
| **BICO-USDT-PERPETUAL** [⚠️⚠️ 급격한 플러스 전환] | OrangeX | $77.61M | $25.01M | +0.176% | +4.156% | -12.848%→+4.156%, CEX와 방향 갈림 | spikes-positive-diverges-from-cex |
| BICO-USDT [개선 지속] | Aster | $1.89M | $0.24M | +0.001% | -1.148% | -5.748%→-1.148% | recovery-continues |
| **CASHCAT** [⚠️ 급냉각, 3소스 수렴] | Hyperliquid | $14.12M | $21.21M | +0.001% | +15.962% | 36.244%→15.962%, 15.96~17.42%로 수렴 | divergence-resolves-converges-15to17pct |
| CASHCAT-USDT-PERPETUAL [수렴] | OrangeX | $0.15M | $0.05M | -0.025% | +16.693% | 25.081%→16.693% | divergence-resolves-converges-15to17pct |
| CASHCAT-USDT [수렴] | Aster | $2.43M | $1.54M | +0.001% | +17.416% | 33.007%→17.416% | divergence-resolves-converges-15to17pct |
| ALLO-USDT [소폭 재악화] | Aster | $0.09M | $0.03M | +0.001% | -2.294% | -1.349%→-2.294% | worsens-slightly |
| ALLO-USDT-PERPETUAL [개선] | OrangeX | $13.75M | $4.80M | +0.010% | -1.400% | -1.815%→-1.400% | improves-slightly |
| **AAVE-USDT-PERPETUAL** [⚠️ 반전] | OrangeX | $27.56M | $10.12M | +0.010% | -0.709% | +0.066%→-0.709% | reverses-negative-across-all-sources |
| **AAVE-USDT** [⚠️ 반전] | Aster | $0.45M | $4.53M | +0.010% | -0.600% | +0.472%→-0.6% | reverses-negative-across-all-sources |
| **AAVE-USD** [⚠️ 반전] | Hyperliquid | $3.57M | $60.80M | +0.001% | -0.621% | +0.581%→-0.621% | reverses-negative-across-all-sources |
| ADA-USDT-PERPETUAL [마이너스 심화] | OrangeX | $77.64M | $27.76M | +0.010% | -0.658% | -0.204%→-0.658% | converges-negative-first-full-alignment |
| ADA-USDT [마이너스 심화] | Aster | $0.62M | $1.70M | +0.004% | -0.558% | -0.051%→-0.558% | converges-negative-first-full-alignment |
| **ADA-USD** [⚠️ 재반전 마이너스] | Hyperliquid | $3.64M | $32.43M | +0.001% | -0.416% | +0.163%→-0.416% | converges-negative-first-full-alignment |
| **BANK-USDT-PERPETUAL** [⚠️⚠️⚠️ 부분 반등] | OrangeX | $6.45M | $2.26M | -0.037% | -10.491% | -16.33%→-10.491%. 8/17 언락 6.1일 앞 | partial-bounce-still-deeply-negative |
| **BANK-USDT** [⚠️⚠️⚠️ 부분 반등] | Aster | $0.31M | $0.27M | -0.006% | -9.140% | -15.975%→-9.14%. 8/17 언락 6.1일 앞 | partial-bounce-still-deeply-negative |
| AKE-USDT-PERPETUAL [소폭 심화] | OrangeX | $5.83M | $1.74M | +0.041% | -3.170% | -2.924%→-3.170% | negative-deepens-continues |
| AKE-USDT [소폭 개선] | Aster | $0.61M | $10.32M | +0.015% | -2.681% | -3.002%→-2.681% | improves-slightly |
| CAP-USDT [재가열] | Aster | $0.13M | $0.13M | +0.001% | +14.315% | +12.979%→+14.315% | reheats-after-cooling |
| CAP-USDT-PERPETUAL [재가열] | OrangeX | $0.69M | $0.26M | -0.044% | +15.204% | +12.645%→+15.204% | reheats-after-cooling |
| ALGO-USDT-PERPETUAL [개선] | OrangeX | $10.68M | $3.91M | +0.010% | -3.140% | -3.837%→-3.140% | improvement-continues |
| ALGO-USDT [초저유동성, 개선] | Aster | $0.06M | $0.03M | -0.001% | -3.453% | -3.701%→-3.453% | low-liquidity-improves |
| ALGO-USD [개선] | Hyperliquid | $1.03M | $1.91M | +0.001% | -3.018% | -3.860%→-3.018% | improvement-continues |
| ATOM-USDT-PERPETUAL [거의 유지] | OrangeX | $4.64M | $1.52M | +0.010% | +0.434% | +0.437%→+0.434% | cools-mixed-across-sources |
| ATOM-USDT [⚠️ 재반전 마이너스] | Aster | $0.004M | $1.60M | +0.010% | -0.290% | +0.437%→-0.29% | cools-mixed-across-sources |
| ATOM-USD [냉각] | Hyperliquid | $0.22M | $1.92M | +0.001% | +0.340% | +0.516%→+0.34% | cools-mixed-across-sources |
| ASTER-USDT-PERPETUAL [확대] | OrangeX | $9.44M | $3.20M | +0.010% | +0.897% | +0.679%→+0.897% | extends-positive |
| ASTER-USDT [대형 OI 소폭 감소] | Aster | $17.52M | $221.02M | 0.000% | +0.729% | OI $221.66M→$221.02M | large-oi-positive-roughly-flat |
| ASTER-USD [확대] | Hyperliquid | $1.79M | $14.64M | +0.001% | +0.861% | +0.828%→+0.861% | extends-positive |
| KAITO-USD [가격·펀딩 소폭 개선] | Hyperliquid | $23.27M | $7.86M | -0.293% | -2.934% | -3.638%→-2.934%, 펀딩 -0.300%→-0.293% | price-flat-funding-diverges-by-source |
| GRAM-USD [거의 유지] | Hyperliquid | $1.14M | $12.83M | +0.001% | -0.798% | -0.724%→-0.798% | roughly-flat-field-anomaly-19th-round |
| HYPE-USD [급격히 냉각] | Hyperliquid | $119.89M | $1,181.02M | +0.001% | +0.169% | +1.444%→+0.169% | cools-sharply-near-flat |
| HYPER-USD [소폭 재악화] | Hyperliquid | $0.18M | $0.34M | -0.004% | -1.322% | -1.108%→-1.322% | roughly-flat-negative |
| APEX-USD [소폭 재악화] | Hyperliquid | $0.27M | $0.70M | +0.001% | -4.316% | -3.969%→-4.316%, Bybit도 동조 | slight-worsening-within-negative |
| FARTCOIN [냉각] | Hyperliquid | $7.19M | $23.93M | +0.001% | +2.650% | +4.807%→+2.650% | cools-within-positive |
| ETHFI-USD [급격히 냉각] | Hyperliquid | $0.68M | $8.47M | +0.001% | +0.255% | +1.966%→+0.255% | cools-sharply-near-flat |
| **ETH-USD** [마이너스 심화] | dYdX | $23.34M | $9.65M | -0.004% | -1.242% | -0.469%→-1.242% | negative-deepens |
| **BTC-USD** [⚠️ 재반전 마이너스] | dYdX | $2.37M | $17.70M | 0.000% | -0.493% | +0.017%→-0.493% | reverses-negative |
| **SOL-USD** [⚠️ 재반전 마이너스] | dYdX | $0.17M | $4.51M | 0.000% | -0.183% | +0.432%→-0.183% | reverses-negative |
| ANSEM [확대] | Aster | $0.24M | $1.00M | +0.001% | +2.569% | +2.304%→+2.569% | extends-positive |
| ANSEM-USDT-PERPETUAL [확대] | OrangeX | $0.49M | $0.17M | +0.010% | +2.338% | +0.916%→+2.338% | extends-positive |
| **BTW** [심화 지속] | Aster | $2.10M | $12.28M | +0.015% | -11.513% | -7.114%→-11.513% | negative-deepens-continues |
| HYNA:PUMP-USD [급격히 냉각] | Hyperliquid | $0.05M | $0.18M | +0.001% | +0.334% | +4.009%→+0.334% | cools-sharply-near-flat |
| HYNA:HYPE-USD [OI 정상갱신 7회차] | Hyperliquid | $0.03M | $0.69M | +0.003% | +1.176% | $694,788.70→$690,733.58 | oi-normal-updates-continue-7th-round |
| AEON-USDT-PERPETUAL [개선 지속] | OrangeX | $0.42M | $0.15M | +0.010% | -3.269% | -3.886%→-3.269% | improvement-continues-5th-round |
| AEON-USDT [개선 5회차 연속] | Aster | $0.05M | $0.22M | +0.028% | -1.349% | -3.79%→-1.349% | improvement-continues-5th-round |
| **BSB-USDT-PERPETUAL** [⚠️ 재반전 마이너스] | OrangeX | $11.38M | $4.34M | +0.010% | -0.535% | +0.606%→-0.535% | reverses-negative-again-after-first-positive |
| BSB-USDT [거의 유지] | Aster | $0.05M | $0.11M | +0.001% | -1.425% | -1.654%→-1.425% | reverses-negative-again-after-first-positive |
| 1000RATS-USDT [개선] | Aster | $0.08M | $0.04M | +0.030% | -1.631% | -5.367%→-1.631% | improves-within-negative |
| AIO-USDT [확대] | Aster | $0.59M | $0.11M | +0.049% | +7.430% | +6.459%→+7.43% | rollercoaster-continues-roughly-flat |
| BLESS [확대 지속] | OrangeX | $41.59M | $16.23M | +0.201% | +5.807% | +0.609%→+5.807%, 촉매 미규명 지속 | extends-positive-catalyst-still-unconfirmed |
| BLESS-USDT [확대 지속] | Aster | $0.23M | $0.22M | +0.008% | +5.152% | +0.716%→+5.152% | extends-positive-catalyst-still-unconfirmed |

## 테마 태그

1. **시장 전반: `/global` 15회차 연속 확보 — 총시총 $2.295T(추가 하락)·BTC도미넌스 56.64%(추가 하락)** (global-api-15th-round-normal).
2. **Fear&Greed 30(Fear) — 직전과 동일, 7회차 연속 유지** (fear-greed-holds-at-30-7th-round).
3. **⚠️⚠️⚠️ BANK: 급락 후 부분 반등, 여전히 深마이너스 — 프로핏테이킹·레버리지청산 서사 확인, 8/17 언락 6.1일 앞** (bank-partial-bounce-still-deeply-negative).
4. **⚠️⚠️ AAVE: 손익분기권 안정화가 하루만에 전면 반전, 전 소스 마이너스** (aave-reverses-negative-across-all-sources).
5. **⚠️ ADA: 처음으로 전 소스(6개) 마이너스 완전 수렴** (ada-converges-negative-first-full-alignment).
6. **⚠️⚠️ BICO: OrangeX만 급반전 플러스, CEX·Aster는 완만한 개선 지속 — DEX 소스 괴리** (bico-orangex-spikes-diverges-from-cex).
7. **⚠️ CASHCAT: 3소스 괴리가 15.96~17.42%로 완전 수렴** (cashcat-divergence-resolves-converges).
8. **⚠️ BSB: 첫 플러스 전환이 하루만에 재역전, OrangeX 원소스 복귀** (bsb-reverses-negative-again).
9. **KAITO: 가격 거의 유지, 펀딩은 OKX 악화·HL 개선으로 소스 갈림 — 8/20 언락 약 9.1일 앞** (kaito-price-flat-funding-diverges).
10. **BEAT: 재악화 3회차 연속, 3소스 동조 심화** (beat-worsening-continues-3rd-round).
11. **BLESS: 플러스 전환 후 확대 지속, 촉매 여전히 미규명** (bless-extends-positive-catalyst-unconfirmed).
12. **CAP: 냉각 후 재가열, 3소스 동조** (cap-reheats-after-cooling).
13. **AEON: 개선 5회차 연속, 3소스 동조** (aeon-improvement-continues-5th-round).
14. **dYdX: BTC·SOL이 플러스에서 마이너스로 재반전, ETH 마이너스 심화 — 3종목 전부 마이너스 전환** (dydx-all-three-reverse-negative).
15. **HYPE·ETHFI·HYNA:PUMP: 강한 플러스에서 급격히 냉각, 손익분기권 근접** (hl-multiple-cool-sharply-near-flat).
16. **GIGGLE 21회차·KAITO(OKX직접) 21회차·GRAM 19회차 필드 이상치 재현, MMT·PIPPIN 10배 비율 5회차 연속 재현** (field-anomalies-continue-10x-pattern-5th-round).
17. **HYNA:HYPE OI 정상 갱신 7회차 연속** (hyna-hype-oi-normal-7th-round).
18. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
19. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
20. **Binance BANK 목록 절단 3회차째 재발(개별 타겟 검색으로 확인), OKX BANK는 instId 자체 부재로 미상장 재확인** (list-truncation-3rd-round-okx-bank-unlisted).
21. **BSB는 이번 회차 OKX CoinGecko(okex_swap)에서 재발견돼 원소스로 복귀** (bsb-source-reverts-to-okx-coingecko).
22. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**CoinGecko binance_futures**: ADA·AAVE(USDT+USD_PERP)·AKE·ATOM·ALLO·1000RATS·AIO·
ASTER·ALGO 확인. **BANK는 최초 검색에서 목록 절단으로 누락됐다가 개별 타겟 검색으로
확인 완료**했다(vol $52.01M·OI $13.27M·chg -9.035%, **3회차 연속 재발**). BICO·BEAT·
BSB·KAITO·GIGGLE·PIPPIN·GRAM·CORE·CAP·AEON·MMT는 이번 회차도 명확히 미확인(단순
미상장).

**CoinGecko bybit**: BANK·BICO·ADA·AKE·ATOM·AAVE·ALLO·ASTER·ALGO·APEX·AIO·1000RATS
확인, 정상 응답. 나머지는 명확히 미확인(단순 미상장).

**CoinGecko okex_swap**: ADA·AAVE·AEON·ALGO·ALLO·ASTER·ATOM·BEAT·BICO·**BSB(이번
회차 재발견, 원소스 복귀)**·CAP·CORE 확인, 정상 응답. BANK는 OKX에 instId 자체가
없어 이번 회차도 확인 불가(에러코드 51001, 단순 미상장). MMT·KAITO·AKE·GIGGLE·
PIPPIN·1000RATS·AIO·GRAM은 이번 회차도 okex_swap 배열에서 미발견돼 OKX 직접 API
또는 Binance/Bybit/DEX로 대체 집계.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: `market/ticker`(개별)+
`public/open-interest`(개별)+`public/funding-rate`(개별) 조합으로 raw JSON을 직접
확인. `oiUsd` 필드 직접 사용 방법론을 **36회차 연속** 유지, vol24_usd=`volCcy24h`×
`last` 계산 방식·chg24=`(last-open24h)/open24h` 계산 방식도 유지. ⚠️
**BANK-USDT-SWAP은 OKX에 instId 자체가 존재하지 않음**을 이번 회차도 직접 확인
(에러코드 51001). **GIGGLE**은 raw JSON에서 `vol24h=40,147,320`·
`volCcy24h=401,473.2`로 정확히 100배 스케일 차이가 나는 필드 이상치가 **21회차
연속**, **KAITO**는 `vol24h`=`volCcy24h`=100,973,758으로 완전동일값 이상치가
**21회차 연속**, **GRAM**도 `vol24h`=`volCcy24h`=2,557,083로 완전동일값이 **19회차
연속** 재현됐다. **MMT**(vol24h=17,717,833, volCcy24h=177,178,330)와
**PIPPIN**(vol24h=18,427,378, volCcy24h=184,273,780)의 10배 비율이 **5회차 연속**
재현돼 계약 승수 차이에 따른 구조적 패턴 가능성이 더욱 굳어졌다.

**Hyperliquid**: ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·GRAM·HYPE·HYPER·APEX·FARTCOIN·
ETHFI·ALGO·HYNA:PUMP-USD·HYNA:HYPE-USD·BTC·ETH 등 raw 정밀값 확보(정상 응답). **SOL은
HL에서 이번 회차도 미확인**(기존 dYdX로 대체 집계). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·
ALLO·BTW·BLESS·ANSEM·TUT·TOAD는 HL 미상장(기존과 동일).

**Aster(`derivatives/exchanges/aster`)**: ACE·ADA·BANK·ALLO·AKE·AAVE·ATOM·ASTER·BICO·
CAP·BLESS·CASHCAT·BTW·ANSEM·ALGO·BEAT·BSB·1000RATS·AEON·AIO 전량 확보(raw 정밀값,
정상 응답). MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE는 Aster에서 여전히 미발견.

**OrangeX(`orangex_futures`)**: ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·
BANK·AKE·CAP·BLESS·CASHCAT·BSB·ANSEM 확인(raw 정밀값, 정상 응답). BTW는 이번 회차도
OrangeX에서 미발견(기존과 동일, Aster에서만 확인). KAITO·1000RATS·GRAM·MMT·PIPPIN·
GIGGLE·CORE는 여전히 미발견.

**dYdX(`dydx_chain`)**: raw 정밀값(BTC-USD $2.37M/OI $17.70M, ETH-USD $23.34M/
OI $9.65M, SOL-USD $0.17M/OI $4.51M) 확보, 첫 시도에 정상 응답.

**CoinGecko `/global`**: 2회 429 후 3차 시도로 총시총 $2,294,736,154,176.85(약
$2.295T)·BTC도미넌스 56.64%를 확인했다. 직전 회차($2.298T·56.660%)보다 시총·도미넌스
모두 추가 하락, **15회차 연속** 확보됐다.

**Fear&Greed**: alternative.me API로 정상 응답, **30(Fear)** 확인 — 직전과 동일,
7회차 연속 유지됐다.

**신규 발견**: (a) BANK가 급락에서 부분 반등했으나 여전히 深마이너스권이다 — WebSearch로
7월 폭등 후 프로핏테이킹·레버리지청산·지지선붕괴 서사를 확인했으나 오늘 구체 촉매는
미규명(이번 회차 최대 사건). (b) AAVE가 전 소스 플러스 회복에서 하루만에 전면
반전됐다. (c) ADA가 처음으로 6개 소스 모두 마이너스로 완전히 정렬됐다. (d) BICO에서
CEX·Aster의 완만한 개선과 OrangeX(DEX)의 급격한 플러스 전환이 공존하는 드문 소스
괴리가 발생했다. (e) CASHCAT의 3소스 괴리가 이번 회차 완전히 해소돼 15.96~17.42%로
수렴했다. (f) BSB의 첫 플러스 전환이 하루만에 재역전됐다. (g) dYdX 3종목(BTC·ETH·SOL)
모두 마이너스로 전환됐다. (h) HYPE·ETHFI·HYNA:PUMP가 강한 플러스에서 손익분기권까지
급격히 냉각됐다.

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에
따라 cex/dex 리스트에서 전부 제외했다; (c) KAITO·GIGGLE·MMT·PIPPIN·GRAM(OKX 직접
조회분)의 CEX 거래량·chg24는 OKX 직접 API 기반 재계산값이며, OI는 API의 `oiUsd` 필드를
직접 채택(36회차 연속 일관 적용); (d) ADA·AAVE·ATOM·ASTER·AKE·BANK·ALLO·AIO·1000RATS·
ALGO 등 복수 거래소 종목의 `chg24`·`funding`은 거래량가중평균 계산값이며, 개별 거래소
값은 본문·`why`에 별도 표기했다; (e) Hyperliquid 원시 funding 필드가 이번 회차도 정상
스케일로 관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·CAP·AEON·MMT·GIGGLE·
PIPPIN·KAITO·GRAM·CORE·BSB·BLESS는 Binance/Bybit에 상장돼 있지 않아 OKX·DEX로만
집계되는 구조이며, 이는 데이터 누락이 아니라 실제 상장 현황이다; (g) BTW·CASHCAT·
ANSEM·HYNA:PUMP-USD·HYNA:HYPE-USD·BLESS·AIO-USDT는 DEX에서만 상장이 확인돼 해당
섹션에서만 집계했다; (h) BANK의 부분 반등이 진짜 저점 확인인지, 단기 반등 후 재하락
가능성이 있는지는 다음 회차 추적이 필요하다; (i) AAVE·ADA의 전면 반전·수렴이
매크로(전 시장 하락) 요인인지 종목 고유 요인인지 완전히 구분하지 못했다; (j) BICO의
OrangeX 급등이 실제 수요 유입인지 단일 거래소 유동성 이상치인지 다음 회차 추적이
필요하다; (k) BLESS·BSB의 방향 전환 촉매도 이번 회차 조사했으나 확인하지 못했다; (l)
KAITO 8/20 언락 규모는 소스별로 공급 3.3%~7.63%·$22.9M~$34.68M로 편차가 있었으며,
이번 회차는 재검증하지 않았다; (m) GIGGLE·KAITO의 필드 이상치가 21회차 연속, GRAM도
19회차 연속 재현돼 구조적 패턴으로 굳어졌으나 근본 원인(OKX API 자체 특성인지)은
규명하지 않았다; (n) TUT·TOAD는 이번 회차 Aster·Binance·Bybit·HL·OrangeX에서 별도
재확인하지 않고 직전 회차 결과를 유지했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
