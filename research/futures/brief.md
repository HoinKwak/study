# 선물시장 스카우트 브리핑 — 2026-08-12 06:34 UTC (KST 2026-08-12 15:34)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-12T04:30:00Z)
> 로부터 약 2.1시간 경과.**

## 이번 회차 핵심 요약 — ACE 급반등 완료(거의 flat), BICO 트로프 반등(여전히 깊은 마이너스+뉴스단서 확보), BEAT 회복 재개, KAITO 재하락+OI 지속증가

이번 회차는 binance_futures·bybit·okex_swap·hyperliquid·aster·orangex_futures·dydx_chain·
OKX직접API(5종) **전량 정상 확보**됐다 — 직전 회차 429였던 orangex_futures·dydx_chain
2종이 모두 복구됐다. 다만 CoinGecko `/global`만 **3회 재시도 전부 429로 계속 실패**해
(4회차 연속) 총시총·BTC도미넌스는 갱신하지 못했다(재시도는 지시대로 3회로 제한).

## ⚠️⚠️⚠️ 최우선 추적 — 언락 임박 3종 (BANK 8/17·ACE 8/18·KAITO 8/20)

### ACE — 8/18 약 5.7일 앞, ⚠️⚠️⚠️ 급격한 반등 완료·거의 flat 근접

직전 회차까지 이어지던 완만한 반등이 이번 회차 급격히 가속돼 4소스 모두 거의 flat까지
도달했다. Binance+Bybit 가중 -10.363%→**+0.117%**(플러스 전환!), HL
-10.499%→**-4.312%**, Aster -10.304%→**-0.358%**, OrangeX(신규 확인) **-0.548%**.
OI는 CEX 가중 $8.10M→**$8.31M(+2.6%)**·OrangeX $3.95M→**$4.80M(+21.4%)**로 증가했으나
HL은 $1.07M→**$0.98M(-8.2%)**로 감소해, 순수 숏커버링만으로는 설명되지 않는 방향 혼재가
이어진다.

### BANK — 8/17 약 4.7일 앞, 소스간 방향 갈림·OrangeX OI감소 재확인

CEX 가중은 재악화가 가속돼 -8.815%→**-11.836%**인데, Aster는 오히려
-9.974%→**-3.352%**로 크게 개선됐다. 이번 회차 OrangeX를 정상 확보해
BANK-USDT-PERPETUAL이 -8.962%(carry)→**-11.545%**(악화)로 확인됐고, **OI는
$1.51M→$1.354M(-10.3%)로 감소**해 과거 회차에 관측됐던 'OrangeX OI 감소' 패턴이
이번 회차 명확히 재확인됐다(가격 악화+OI 감소 조합은 롱 청산·숏 신규진입 혼재를 시사).

### KAITO — 8/20 12:00 UTC 언락(공급 약13.5%) 약 8.2일 앞, 재하락 지속·OI 4회차 연속 증가

OKX직접 -5.883%→**-6.814%**, HL -5.404%→**-6.593%**로 재하락이 이어졌다. OI는 OKX
$8.45M→**$8.66M(+2.4%)**, HL $12.78M→**$13.36M(+3.6%)**로 양쪽 모두 4회차 연속 계속
증가해 숏 누적 해석이 계속 지지된다. funding raw -0.0026317→**-0.0045957**로 재확대가
2회차째 이어졌다.

## 이번 회차 추가 최우선 관찰

### BICO — ⚠️⚠️⚠️ 급락 트로프에서 반등, 여전히 깊은 마이너스 · 뉴스 단서 확보

직전 회차 급격히 가속됐던 급락이 이번 회차 트로프에서 반등했다 — OKX
**-22.652%→-14.629%**, Aster **-24.075%→-22.099%**로 낙폭이 다소 줄었으나 여전히 두
자릿수 깊은 마이너스다. OrangeX도 이번 회차 정상 확보돼 -11.429%(carry)→**-14.833%**
(확인, carry보다 악화)로 나타났다. OI는 OKX $6.32M→$6.00M(-5.1%)·Aster
$114,522→$97,011(-15.3%)·OrangeX $18.63M→$13.12M(-29.6%)로 세 소스 모두 감소해 패닉
청산 이후 진정 국면으로 해석된다.

**WebSearch로 원인 단서 확보**: Bitget이 "BICO 비정상 가격변동을 감지해 리스크관리
조치·거래제한을 적용"했다는 공지가 있었고, 온체인 분석 보도에 따르면 Biconomy 팀
지갑이 약 9천만 BICO를 언스테이킹해 Gate.io 거래소로 입금한 정황이 최근 고점 부근·
하락 시점과 일치한다는 내용이 확인됐다. 또한 "신규 무기한선물 상장(최대 5배
레버리지)" 발표도 있었다. **다만 공식적인 해킹 확인은 없으며**, 상장 공지·팀 지갑
이동과 급락 사이의 직접 인과관계도 명확히 규명되지는 않았다.

### CASHCAT — 완전 반전(휩쏘)이 아니라 낙폭 축소

직전 회차 관측된 "매 회차 방향이 뒤집히는 휩쏘"와는 다른 양상이 이번 회차
나타났다 — HL **-8.393%→-1.386%**, Aster **-5.534%→-3.291%**로 완전한 방향 반전이
아니라 마이너스권 안에서 낙폭이 대폭 축소되는 패턴이었다(정직하게 기록: 이번 회차는
플러스로의 재반전이 아니다). OrangeX도 신규 확인돼 +1.016%(carry, 2회차 전 값)에서
**-3.685%**로 나타났다.

### BEAT·CAP·AEON·AAVE — 간결 현황

- **BEAT**: ⚠️⚠️ 직전 회차 정체됐던 회복세가 이번 회차 큰 폭으로 재개됐다 — OKX
  **-20.234%→-2.313%**, Aster **-19.42%→-8.391%**로 두 소스 모두 급격히 개선됐다.
- **CAP**: 고점 대비 pullback이 이어졌다 — OKX **+22.805%→+14.14%**, Aster
  **+22.9%→+14.552%**, OrangeX(신규확인) **+15.031%**로 3소스 모두 여전히 강한
  플러스권이지만 추가로 낮아졌다.
- **AEON**: 랠리 확대가 pullback으로 전환됐다 — OKX **+11.495%→+6.545%**, Aster
  **+13.074%→+7.684%**, OrangeX +7.726%(carry)→**+6.567%**(확인)로 3소스 모두 동반
  하락했다.
- **AAVE**: 플러스권 유지하되 상승폭이 소폭 둔화됐다 — 가중 **+0.944%→+0.760%**,
  Aster +0.887%→**+0.914%**, HL +0.948%→**+0.947%**로 대체로 유지됐다.

### BLESS — 마이너스에서 플러스로 큰 폭 반전

Aster -2.052%→**+4.537%**, OrangeX -10.926%(carry)→**+4.348%**(확인)로 두 소스
모두 동반 반전했다.

### HYPE(HL) — 3회차 연속 확대 추세 반전

**-1.714%→-0.839%**로 3회차 연속 이어지던 마이너스 폭 확대 추세가 이번 회차
반전·개선됐다.

### ⚠️⚠️ OKX 직접조회 funding 재검증 — PIPPIN 완전 수렴, MMT 재확대

GIGGLE·GRAM은 이번 회차도 raw `fundingRate`가 정확히 `0.0000500000000000`로
완전 동일(GIGGLE 41회차·GRAM 39회차 연속). **PIPPIN**은 raw
`0.0001220155591698`→**`0.0000500000000000`**로 여러 회차 이어지던 그룹값 대비
이탈이 이번 회차 완전히 소멸돼 GIGGLE·GRAM과 정확히 같은 값으로 수렴했다(open24h를
재조회해 `0.01751`로 두 차례 모두 일치함을 교차검증, 전사 오류 재발 없음 확인).
**MMT**는 raw `-0.0002582749883095`→**`-0.0003457036409055`**로 직전 회차 처음
완화됐던 추세가 이번엔 재반전해 다시 심화됐고, 가격도 chg -1.414%→**-7.944%**로
큰 폭 악화됐다. KAITO는 별개 스케일로 raw `-0.0045956541733598`(2회차 연속 재확대).

## 이번 회차 그 외 관찰

- **BSB**: OKX -6.606%→**-7.321%**(소폭 재악화), Aster -6.583%→**-6.551%**(거의
  보합), OrangeX(신규확인) -4.912%carry→**-7.249%**(확인, 악화).
- **ADA**: 개선추세 지속, flat 근접 — 가중 -1.457%→**-1.116%**, HL
  -1.414%→**-0.979%**, Aster -1.42%→**-0.694%**, OrangeX(신규확인) **-0.958%**.
- **AKE**: 고점대비 pullback — 가중 +11.393%→**+10.005%**, Aster
  +11.398%→**+10.272%**, OrangeX(신규확인) **+9.758%**. 여전히 강한 플러스.
- **ASTER**: 3소스 모두 둔화 — 가중 +0.763%→**+0.252%**, 자체 +0.864%→**+0.265%**,
  HL +0.659%→**+0.392%**.
- **ATOM**: 고점권 소폭 하락 — 가중 +3.180%→**+2.659%**, HL +3.203%→**+2.945%**,
  Aster +3.525%→**+2.762%**.
- **ALLO**: CEX 소폭 재악화(-0.701%→**-0.846%**)한 반면 Aster
  -1.277%→**-0.042%**(flat 근접)·OrangeX -1.97%carry→**-0.711%**(확인)로 개선돼
  방향 혼재.
- **1000RATS**: CEX 개선(-10.366%→**-9.707%**)했으나 Aster
  -9.425%→**-12.456%**로 역행.
- **ALGO**: flat 근접에서 소폭 반락 — 가중 -0.175%→**-0.554%**. HL
  -0.173%→**-0.493%**, Aster -0.711%→**-0.282%**(개선), OrangeX(신규확인)
  **-0.612%**.
- **ANSEM**: Aster -6.733%→**-4.865%**(개선), OrangeX(신규확인)
  -4.241%carry→**-6.046%**(확인, 악화).
- **dYdX(ETH·BTC·SOL)**: 이번 회차 정상 확보 — ETH +0.496%carry→**+1.017%**(확인,
  개선), BTC -0.292%carry→**-0.367%**(확인), SOL +0.618%carry→**+0.356%**(확인).

## 데이터 이슈 추적 결과

이번 회차 **binance_futures·bybit·okex_swap·hyperliquid·aster·orangex_futures·
dydx_chain·OKX직접API(5종) 전량 정상 확보**됐다. 직전 회차 429였던
orangex_futures·dydx_chain 2종이 모두 복구돼, 이번 회차 실패군은 **CoinGecko
`/global` 단독**이다(3회 재시도 전부 429, 4회차 연속 실패). 순환 레이트리밋
패턴이 이번엔 `/global`에 집중된 것으로 확인된다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [⚠️⚠️⚠️ 급반등 완료, 거의 flat, 언락 5.7일] | Binance+Bybit(가중평균) | $21.34M | $8.31M | -0.002 | +0.117% | 4소스 모두 flat 근접까지 급반등, OI 방향은 혼재 지속 | rebounds-sharply-nears-flat-oi-mixed-unlock-6d |
| **BANK** [CEX 악화가속·Aster개선·OrangeX OI감소재확인, 언락 4.7일] | Binance+Bybit(가중평균) | $41.99M | $16.46M | -0.028 | -11.836% | 소스간 방향 갈림, OrangeX OI -10.3% 감소 재확인 | worsens-cex-improves-aster-oi-orangex-confirmed-decline-unlock-5d |
| **KAITO** [재하락 지속, OI 4회차 연속 증가, 언락 8.2일] | OKX(직접API) | $74.03M | $8.66M | -0.460 | -6.814% | 재하락, OI는 OKX·HL 양쪽 계속 증가 | worsens-further-oi-still-rising-unlock-8d |
| **BICO** [⚠️⚠️⚠️ 트로프 반등, 여전히 깊은 마이너스] | OKX(CoinGecko정상, okex_swap) | $69.68M | $6.00M | -0.006 | -14.629% | Bitget 리스크관리·팀지갑 Gate.io 입금 정황, 신규 무기한선물 상장(해킹확인은 없음) | rebounds-from-trough-still-deeply-negative-oi-declining |
| **BEAT** [⚠️⚠️ 회복 재개] | OKX(CoinGecko정상, okex_swap) | $664.32M | $10.53M | -0.029 | -2.313% | 정체 깨고 큰 폭 회복 재개 | recovery-resumes-sharply |
| **CAP** [pullback 지속] | OKX(CoinGecko정상, okex_swap) | $173.71M | $6.65M | -0.006 | +14.14% | 고점대비 추가 하락, 여전히 강한 플러스권 | rallies-pullback-continues |
| **AEON** [랠리에서 pullback] | OKX(CoinGecko정상, okex_swap) | $12.78M | $3.73M | +0.005 | +6.545% | 3소스 모두 동반 pullback | rally-pulls-back |
| **AAVE** [플러스권 유지, 둔화] | Binance+Bybit(가중평균) | $63.80M | $87.60M | +0.008 | +0.760% | 3소스 대체로 유지 | extends-positive-mild-deceleration |
| **BLESS**(DEX전용) — 마이너스→플러스 큰 폭 반전, CEX 미상장 |  |  |  |  |  | 아래 DEX 표 참조 | flips-positive-sharp-reversal |
| MMT [⚠️ 가격 큰 폭 악화, funding 재확대] | OKX(직접API) | $19.54M | $3.07M | -0.035 | -7.944% | 여러회차 완화가 재반전, 다시 심화 | worsens-sharply-funding-divergence-resumes |
| AIO [회복 지속] | Binance+Bybit(가중평균) | $6.51M | $4.07M | +0.005 | -1.337% | 동반 개선 지속 | recovery-continues |
| GRAM [플러스 유지] | OKX(직접API) | $3.64M | $6.56M | +0.005 | +2.797% | funding 그룹값 유지(39회차) | extends-positive-funding-anomaly-39th |
| GIGGLE [대체로 보합] | OKX(직접API) | $109.36M | $2.00M | +0.005 | +4.163% | funding 이상치 41회차 연속 | roughly-flat-positive-funding-anomaly-41st |
| PIPPIN [⚠️ funding 완전 수렴] | OKX(직접API) | $7.85M | $1.67M | +0.005 | -2.799% | 그룹 이상치값(0.00005)에 완전 수렴, 교차검증 완료 | funding-fully-converges-to-anomaly |
| BSB [소폭 재악화] | OKX(okex_swap) | $2.97M | $2.21M | +0.005 | -7.321% | OKX·OrangeX 동반 악화, Aster는 보합 | worsens-slightly-mixed-sources |
| AKE [고점대비 pullback] | Binance+Bybit(가중평균) | $52.24M | $39.42M | +0.022 | +10.005% | 3소스 모두 소폭 하락하나 여전히 강한 플러스 | pulls-back-slightly-from-highs |
| ADA [개선추세 지속] | Binance+Bybit(가중평균) | $160.53M | $154.84M | +0.007 | -1.116% | 전소스 flat 근접 | improves-further-nears-flat |
| ASTER [둔화] | Binance+Bybit(가중평균) | $16.90M | $111.58M | +0.003 | +0.252% | 3소스 모두 냉각되나 여전히 플러스 | decelerates-still-positive |
| ATOM [고점권 소폭 하락] | Binance+Bybit(가중평균) | $17.16M | $29.31M | +0.004 | +2.659% | 고점대비 소폭 하락 | pulls-back-slightly-from-highs |
| ALLO [방향 혼재] | Binance+Bybit(가중평균) | $13.72M | $17.57M | +0.003 | -0.846% | CEX 소폭 악화, Aster·OrangeX는 개선 | mixed-cex-slight-worse-others-improve |
| 1000RATS [소스간 역행] | Binance+Bybit(가중평균) | $10.87M | $15.02M | +0.005 | -9.707% | CEX 개선, Aster는 악화 | mixed-cex-improves-aster-worsens |
| ALGO [flat 근접, 소폭 반락] | Binance+Bybit(가중평균) | $16.26M | $15.55M | -0.012 | -0.554% | 소스간 등락 혼재하며 대체로 flat 유지 | near-flat-slight-pullback |
| CORE [소폭 재악화] | OKX(CoinGecko정상, okex_swap) | $1.17M | $0.86M | +0.010 | -1.926% | 저유동성 지속 | worsens-slightly-low-liquidity |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함). 이번 회차
> **orangex_futures·dydx_chain 모두 정상 확보**돼 해당 프로토콜 행이 전부 확인값으로
> 갱신됐다(직전 회차 429였던 다수 항목이 "신규확인"으로 표시됨).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE-USD** [급반등 지속] | Hyperliquid | $1.04M | $0.98M | -0.005 | -4.312% | OI 소폭 감소 동반. 언락 5.7일 | rebounds-sharply-nears-flat-oi-mixed-unlock-6d |
| **ACE-USDT-PERPETUAL** [신규확인, 큰 폭 개선] | OrangeX | $13.15M | $4.80M | +0.010 | -0.548% | OI +21.4% 증가 | rebounds-sharply-nears-flat-oi-mixed-unlock-6d |
| **ACE-USDT** [급반등 지속] | Aster | $0.17M | $0.03M | +0.001 | -0.358% | 전소스 flat 근접 | rebounds-sharply-nears-flat-oi-mixed-unlock-6d |
| **BANK-USDT** [큰 폭 개선] | Aster | $0.12M | $0.24M | -0.003 | -3.352% | CEX와 방향 다름 | improves-aster-diverges-from-cex-unlock-5d |
| **BANK-USDT-PERPETUAL** [신규확인, OI감소 재확인] | OrangeX | $4.24M | $1.35M | -0.010 | -11.545% | OI -10.3% 감소 재확인 | worsens-oi-decline-confirmed-unlock-5d |
| **KAITO-USD** [재하락, OI 계속증가] | Hyperliquid | $16.08M | $13.36M | -0.389 | -6.593% | OI +3.6% 증가. 언락 8.2일 | worsens-further-oi-still-rising-unlock-8d |
| **BICO-USDT-PERPETUAL** [신규확인, 깊은 마이너스] | OrangeX | $42.62M | $13.12M | -0.035 | -14.833% | OI -29.6% 감소 | rebounds-from-trough-still-deeply-negative-oi-declining |
| **BICO-USDT** [트로프 소폭 개선] | Aster | $0.26M | $0.10M | +0.003 | -22.099% | 여전히 20%대 마이너스 | rebounds-from-trough-still-deeply-negative-oi-declining |
| **CASHCAT** [낙폭 대폭 축소] | Hyperliquid | $9.84M | $21.54M | +0.001 | -1.386% | 여전히 마이너스, 완전반전 아님 | still-negative-magnitude-shrinks |
| CASHCAT-USDT-PERPETUAL [신규확인] | OrangeX | $0.16M | $0.06M | +0.010 | -3.685% | carry대비 방향전환 | still-negative-magnitude-shrinks |
| CASHCAT-USDT [낙폭 축소] | Aster | $0.99M | $1.38M | +0.020 | -3.291% | HL과 유사 | still-negative-magnitude-shrinks |
| HYPE-USD [3회차 확대 추세 반전] | Hyperliquid | $125.99M | $1,177.47M | +0.001 | -0.839% | 마이너스 폭 개선 | narrows-negative-reverses-trend |
| AEON-USDT-PERPETUAL [신규확인, pullback] | OrangeX | $0.45M | $0.17M | +0.010 | +6.567% | 랠리 pullback | rally-pulls-back |
| AEON-USDT [pullback] | Aster | $0.06M | $0.22M | +0.005 | +7.684% | 랠리 pullback | rally-pulls-back |
| **BLESS** [플러스로 전환] | OrangeX | $29.89M | $10.94M | +0.018 | +4.348% | 마이너스에서 큰 폭 반전 | flips-positive-sharp-reversal |
| **BLESS-USDT** [플러스로 전환] | Aster | $0.17M | $0.17M | +0.005 | +4.537% | OrangeX와 동반 반전 | flips-positive-sharp-reversal |
| GRAM-USD [플러스 유지] | Hyperliquid | $3.58M | $15.32M | +0.001 | +2.965% | OI 소폭 감소 | extends-positive-funding-anomaly-39th |
| BTW [상승세 유지] | Aster | $0.84M | $15.15M | +0.024 | +10.345% | 거의 보합 | rebounds-notably |
| ANSEM [개선] | Aster | $0.33M | $1.08M | +0.001 | -4.865% | 마이너스 폭 축소 | improves-slightly |
| ANSEM-USDT-PERPETUAL [신규확인, 악화] | OrangeX | $0.51M | $0.17M | +0.010 | -6.046% | carry보다 악화 | worsens-orangex-confirmed |
| HYNA:PUMP-USD [재조회없음] | Hyperliquid | $0.07M | $0.19M | +0.004 | -0.835% | 직전값 유지 | small-fluctuation-continues |
| HYNA:HYPE-USD [재조회없음] | Hyperliquid | $0.13M | $0.89M | +0.001 | -0.988% | 직전값 유지 | small-fluctuation-continues |
| BSB-USDT-PERPETUAL [신규확인, 악화] | OrangeX | $5.66M | $1.96M | +0.010 | -7.249% | carry보다 악화 | worsens-slightly-mixed-sources |
| BSB-USDT [보합] | Aster | $0.01M | $0.11M | +0.001 | -6.551% | 거의 보합 | worsens-slightly-mixed-sources |
| 1000RATS-USDT [역행] | Aster | $0.05M | $0.01M | +0.006 | -12.456% | CEX와 반대로 재악화 | mixed-cex-improves-aster-worsens |
| AIO-USDT [개선] | Aster | $0.10M | $0.10M | +0.005 | -1.6% | 회복 지속 | recovery-continues |
| AAVE-USDT-PERPETUAL [신규확인] | OrangeX | $36.48M | $13.49M | +0.010 | +0.845% | 플러스 확대 | extends-positive-mild-deceleration |
| AAVE-USDT [플러스 유지] | Aster | $0.26M | $4.43M | +0.010 | +0.914% | 유지 | extends-positive-mild-deceleration |
| AAVE-USD [플러스 유지] | Hyperliquid | $5.00M | $59.79M | +0.000 | +0.947% | 거의 보합 | extends-positive-mild-deceleration |
| ADA-USDT-PERPETUAL [신규확인, 개선] | OrangeX | $82.86M | $30.60M | -0.010 | -0.958% | 개선 | improves-further-nears-flat |
| ADA-USDT [개선] | Aster | $0.50M | $1.58M | +0.006 | -0.694% | 개선 지속 | improves-further-nears-flat |
| ADA-USD [개선] | Hyperliquid | $3.81M | $31.03M | +0.001 | -0.979% | 개선 지속 | improves-further-nears-flat |
| AKE-USDT-PERPETUAL [신규확인, pullback] | OrangeX | $6.44M | $2.34M | +0.017 | +9.758% | pullback | pulls-back-slightly-from-highs |
| AKE-USDT [pullback] | Aster | $0.67M | $11.13M | +0.014 | +10.272% | 고점대비 하락 | pulls-back-slightly-from-highs |
| ALGO-USDT-PERPETUAL [신규확인, 개선] | OrangeX | $8.18M | $2.87M | +0.010 | -0.612% | 개선 | near-flat-slight-pullback |
| ALGO-USDT [개선] | Aster | $0.03M | $0.02M | -0.004 | -0.282% | 개선 | near-flat-slight-pullback |
| ALGO-USD [소폭 반락] | Hyperliquid | $0.82M | $2.12M | +0.001 | -0.493% | flat 근접에서 소폭 반락 | near-flat-slight-pullback |
| ATOM-USDT-PERPETUAL [신규확인] | OrangeX | $10.03M | $3.52M | +0.010 | +2.88% | 고점권 유지 | pulls-back-slightly-from-highs |
| ATOM-USDT [고점권 소폭하락] | Aster | $0.01M | $1.66M | +0.010 | +2.762% | 고점권 소폭하락 | pulls-back-slightly-from-highs |
| ATOM-USD [고점권 소폭하락] | Hyperliquid | $0.32M | $1.88M | +0.001 | +2.945% | 고점권 소폭하락 | pulls-back-slightly-from-highs |
| ASTER-USDT-PERPETUAL [신규확인, 둔화] | OrangeX | $7.10M | $2.64M | +0.010 | +0.217% | 둔화 | decelerates-still-positive |
| ASTER-USDT [대형 OI, 둔화] | Aster | $10.07M | $219.71M | +0.004 | +0.265% | 둔화, 여전히 플러스 | decelerates-still-positive |
| ASTER-USD [둔화] | Hyperliquid | $0.90M | $14.75M | +0.001 | +0.392% | 둔화, 여전히 플러스 | decelerates-still-positive |
| ALLO-USDT [flat 근접까지 개선] | Aster | $0.06M | $0.03M | +0.000 | -0.042% | 큰 폭 개선 | mixed-cex-slight-worse-others-improve |
| ALLO-USDT-PERPETUAL [신규확인, 개선] | OrangeX | $9.51M | $3.40M | +0.010 | -0.711% | 개선 | mixed-cex-slight-worse-others-improve |
| HYPER-USD [거의 보합] | Hyperliquid | $0.16M | $0.32M | +0.001 | -0.466% | 거의 보합 | roughly-flat |
| APEX-USD [재반전] | Hyperliquid | $0.12M | $0.64M | +0.001 | -0.88% | 플러스에서 재반전 | reverses-negative |
| FARTCOIN [pullback] | Hyperliquid | $8.03M | $23.38M | +0.001 | +0.977% | 플러스 유지, pullback | pulls-back-still-positive |
| ETHFI-USD [소폭 악화] | Hyperliquid | $0.88M | $8.19M | +0.001 | -3.627% | 마이너스 폭 확대 | worsens-further-negative |
| ETH-USD [신규확인, 개선] | dYdX | $12.03M | $19.61M | 0.0 | +1.017% | 개선 | confirmed-improves |
| BTC-USD [신규확인] | dYdX | $3.20M | $17.73M | -0.001 | -0.367% | 근사치 유지 | confirmed-roughly-flat |
| SOL-USD [신규확인] | dYdX | $1.02M | $4.56M | 0.0 | +0.356% | 유지 | confirmed-roughly-flat |

## 테마 태그

1. **⚠️⚠️⚠️ ACE: 8/18 언락 약 5.7일 앞두고 4소스 모두 거의 flat까지 급반등**(가중 -10.363%→+0.117%로 플러스 전환), OI는 CEX·OrangeX 증가·HL 감소로 여전히 방향 혼재 (ace-rebounds-sharply-nears-flat-oi-mixed-unlock-6d).
2. **⚠️⚠️ BANK: 8/17 언락 약 4.7일 앞두고 CEX·Aster 방향 갈림, OrangeX OI -10.3% 감소 재확인** (bank-mixed-oi-orangex-confirmed-unlock-5d).
3. **⚠️⚠️ KAITO: 8/20 언락 약 8.2일 앞두고 재하락 지속, OI 4회차 연속 계속 증가** (kaito-worsens-oi-still-rising-unlock-8d).
4. **⚠️⚠️⚠️ BICO: 급락 트로프에서 반등하나 여전히 두자릿수 깊은 마이너스, OI 3소스 전부 감소. Bitget 리스크관리·팀지갑 Gate.io 입금 정황 보도(해킹확인은 없음)** (bico-rebounds-from-trough-still-deep-negative).
5. **CASHCAT: 완전 반전이 아니라 마이너스권 안에서 낙폭 대폭 축소** (cashcat-still-negative-magnitude-shrinks).
6. **⚠️⚠️ BEAT: 회복세 정체가 깨지고 큰 폭 재개** (beat-recovery-resumes-sharply).
7. **CAP: 상승세 pullback 지속** (cap-rallies-pullback-continues).
8. **AEON: 랠리 확대에서 pullback으로 전환** (aeon-rally-pulls-back).
9. **AAVE: 플러스권 유지, 상승폭 소폭 둔화** (aave-extends-positive-mild-deceleration).
10. **BLESS: 마이너스에서 플러스로 큰 폭 반전** (bless-flips-positive-sharp-reversal).
11. **HYPE(HL): 3회차 연속 마이너스 확대 추세가 이번 회차 반전·개선** (hype-narrows-negative-reverses-trend).
12. **⚠️⚠️ OKX 직접조회 funding: PIPPIN이 그룹 이상치값(0.00005)에 완전 수렴, MMT는 재반전해 다시 심화(가격도 큰 폭 악화). GIGGLE·GRAM은 0.00005 동일값 지속(41·39회차)** (okx-funding-pippin-converges-mmt-deepens).
13. **PIPPIN open24h 재조회 교차검증 결과 두 차례 모두 0.01751로 일치(전사오류 재발 없음)** (pippin-cross-check-consistent).
14. **데이터: 이번 회차 orangex_futures·dydx_chain 모두 정상 확보(직전 회차 429에서 회복). CoinGecko `/global`만 3회 재시도 전부 429로 계속 실패(4회차 연속)** (data-only-global-fails-others-recover).
15. **총시총·BTC도미넌스는 `/global` 지속 실패로 갱신 없음** (global-metrics-unconfirmed-carried-forward).
16. **Fear&Greed 이번 회차도 미재조회** (fear-greed-not-rechecked).
17. **주식화·상품 토큰은 규약에 따라 전부 제외** (stock-commodity-tokens-excluded).
18. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체(451 지역차단 지속)** (fapi-still-blocked-coingecko-fallback).
19. **GMX 이번 회차도 재조회 없이 계속 제외** (gmx-still-excluded-no-recheck).
20. **TUT: 이번 회차도 재확인 생략** (tut-status-unconfirmed-no-further-check).

## 데이터 신뢰도

이번 회차 **binance_futures·bybit·okex_swap·hyperliquid·aster·orangex_futures·
dydx_chain·OKX 직접API(KAITO·GIGGLE·MMT·PIPPIN·GRAM) 전량 정상 확보**됐다. 직전
회차 429였던 orangex_futures·dydx_chain 2종이 모두 복구돼, 이번 회차 유일한 실패는
**CoinGecko `/global`**(3회 재시도 전부 429, 4회차 연속 실패)뿐이었다 — 순환
레이트리밋 패턴에서 이번엔 실패가 `/global` 단독으로 집중됐다.

**OKX 직접 API(KAITO·GIGGLE·MMT·PIPPIN·GRAM)**: ticker·open-interest·funding-rate
개별 엔드포인트 전부 1차 시도부터 정상. GIGGLE·GRAM은 raw `fundingRate`가 여전히
정확히 `0.00005`로 동일(41·39회차 연속). **PIPPIN은 이번 회차 그룹값(0.00005)에
완전히 수렴**해, 여러 회차 이어지던 이탈 추세가 소멸됐다. **PIPPIN open24h는 지시에
따라 재조회로 교차검증**했고, 두 차례 모두 `0.01751`로 정확히 일치해 지난 회차 관측된
전사 오류(WebFetch 요약모델 기인 추정)가 재발하지 않음을 확인했다. MMT는 funding
이탈이 재확대되며 가격도 큰 폭 악화됐다. 또한 OKX ticker의 `vol24h`(계약수)와
`volCcy24h`(통화표시)가 종목별로 배율이 달라(KAITO·GRAM은 동일, GIGGLE·MMT·PIPPIN은
10~100배 차이) 이번 회차도 기존 회차와의 연속성을 위해 `vol24h` 필드를 그대로
채택했다 — 계약승수 정의가 완전히 검증되지 않은 한계는 여전하다.

**Hyperliquid**: 정상 확보 — ACE·KAITO·CASHCAT·ADA·AAVE·ATOM·ASTER·ALGO·GRAM·HYPE·
HYPER·APEX·FARTCOIN·ETHFI 확보(raw 정밀값). BICO·BEAT·CAP·MMT·BANK·AEON·AKE·ALLO·
BTW·BLESS·ANSEM·TUT는 HL 미상장(기존과 동일).

**Aster**: 정상 확보 — BANK·AAVE·ADA·BICO·BEAT·BSB·AKE·ATOM·ALLO·1000RATS·AIO·
AEON·ASTER·CAP·ALGO·ACE·CASHCAT·BTW·ANSEM·BLESS 전량 확보(raw 정밀값). MMT·GIGGLE·
PIPPIN·GRAM·CORE·TUT는 Aster에서 여전히 미발견.

**OrangeX**: ⚠️ **이번 회차 3종 전부 1차 시도부터 정상 확보**(직전 회차 429에서
복구) — ACE·AAVE·ALLO·ALGO·AEON·ADA·ATOM·ASTER·BICO·BEAT·BANK·AKE·CAP·BLESS·
CASHCAT·BSB·ANSEM 전부 갱신됐다. BANK의 OrangeX 확보로 이번 회차 최우선 과제였던
'OI 감소 지속여부 검증'이 완료됐다(-10.3% 감소 재확인).

**binance_futures**: 1차 시도부터 정상 확보 — ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·
ALLO·1000RATS·ATOM·AIO 확보. BICO·AEON은 이번 회차도 Binance에서 미발견.

**bybit**: 1차 시도부터 정상 확보 — ACE·BANK·AKE·ADA·AAVE·ASTER·ALGO·ALLO·1000RATS·
ATOM·AIO 확보, Binance+Bybit 가중평균으로 반영.

**dYdX(`dydx_chain`)**: ⚠️ **이번 회차 1차 시도부터 정상 확보**(직전 회차 429에서
복구) — BTC-USD·ETH-USD·SOL-USD 전부 갱신됐다.

**CoinGecko `/global`**: ⚠️ 3회 재시도 전부 429로 확보 실패(4회차 연속) — 총시총·
BTC도미넌스 모두 직전 회차 값을 유지했다.

**Fear&Greed**: 이번 회차도 재조회하지 않음(최우선 추적과제에 시간 집중).

**신규 발견**: (a) ACE는 직전까지 완만하게 이어지던 반등이 이번 회차 급격히
가속돼 4소스 모두 거의 flat까지 도달했다 — 단일 회차 내 이만큼 큰 폭의 방향 전환은
이번 프로젝트 관측 이래 드문 사례다. (b) BANK는 이번 회차 OrangeX를 정상 확보해
'OI -5.9%~-10.3% 감소' 패턴이 명확히 재확인됐다 — 다만 CEX와 Aster의 방향이
갈려 단일 서사로 정리하기는 어렵다. (c) BICO는 급락 트로프에서 반등했고, WebSearch로
Bitget 리스크관리 조치·팀 지갑 Gate.io 입금 정황이라는 구체적 원인 단서를 처음으로
확보했다 — 다만 공식 해킹 확인은 없고 인과관계도 완전히 규명되지는 않았다. (d)
CASHCAT은 이번 회차 완전한 방향 반전(휩쏘)이 아니라 마이너스권 내 낙폭 축소로
나타나, 과거 관측된 '매 회차 뒤집힘' 패턴과는 다른 양상이었다. (e) PIPPIN funding이
그룹 이상치값(0.00005)에 완전히 수렴해, GIGGLE·GRAM과 구분 불가능해졌다 — 이탈이
영구적이지 않았음을 보여준다. (f) orangex_futures·dydx_chain이 이번 회차 모두
복구돼, 실패군이 `/global` 단독으로 집중됐다.

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
확인함); (j) OKX 직접조회 GIGGLE·GRAM의 funding이 왜 매 회차 동일값(0.00005)으로
관측되는지는 규명하지 못했다; (k) HL에서 canonical SOL-USD는 이번 회차 재확인하지
않았다; (l) KAITO-USDT(Aster)는 이번 회차도 조회하지 않았다; (m) HYNA:PUMP-USD·
HYNA:HYPE-USD는 HL 응답이 모호하게 반환된 이력이 있어 이번 회차도 재조회를 생략하고
직전값을 유지했다; (n) OKX ticker의 `vol24h`(계약수 단위)와 `volCcy24h`(통화 단위)가
종목별로 배율이 달라(GIGGLE·MMT·PIPPIN은 10~100배 차이) 이번 회차는 기존 회차와의
연속성을 위해 `vol24h`를 채택했으나 계약승수 정의는 완전히 검증하지 못했다; (o)
`/global`이 4회차 연속 복구되지 않은 원인은 규명하지 못했으며, `/global`만 계속
실패하는 것이 특정 엔드포인트의 구조적 제약인지 우연인지는 다음 회차 이후 계속
추적이 필요하다; (p) BICO 관련 뉴스(Bitget 리스크관리·팀지갑 이동)는 2차보도 기반
WebSearch 요약이며, 원문 공지·온체인 트랜잭션을 직접 검증하지는 않았다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
