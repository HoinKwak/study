# 선물시장 스카우트 브리핑 — 2026-08-18 20:30 UTC (KST 2026-08-19 05:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-18
> 18:30 UTC)로부터 2시간 경과(정상 간격).**

> **⚠️ 정정 안내**: 최초 게시본에서 "funding 스케일 스팟체크 — 신규 이상 없음"이라고 기술했으나,
> 이는 **OKX 14건에 한정된 점검**이었고 점검 범위를 넘어선 결론이었다. 부모 세션의 검증 요청으로
> 재점검한 결과 **CoinGecko `derivatives/exchanges/*` 경유로 확보한 funding_rate가 percent
> 단위**(raw fraction의 100배)로 반환되고 있었음을 발견해, 아래 표·JSON의 해당 값을 전부 `/100`
> 보정했다. 자세한 근거는 "데이터 품질" 문단과 한계 (x) 참조.

## 시장 전반 — ACE 재가속(40%대 진입)·CASHCAT 3소스 수렴·funding 단위 오류 추가 발견·정정

**이번 회차 최대 헤드라인은 ACE의 추가 가속과 CASHCAT의 3소스 수렴이다.**

**ACE는 또 한 번 크게 가속했다** — B+B(가중평균) +32.06%→**+41.66%**, HL +32.15%→**+42.22%**,
Aster +31.91%→**+41.42%**로 3소스 모두 40%대 초반까지 확대됐다. tokenomist.ai로 언락설을
반증한 지난 회차 이후에도 가속이 이어져 WebSearch로 신규 촉매를 추가 확인했으나, 8/7·8/13
관련 보도(Bitget PoolX 상장)만 재확인됐을 뿐 이번 회차의 추가 급등을 설명할 뚜렷한 신규
재료는 확인되지 않았다 — **원인은 계속 미상으로 남겨둔다.** 거래량도 B+B 기준
$697.30M→**$717.23M**로 소폭 더 늘었다. OKX SWAP 티커는 이번 회차도 부재를 재확인했다.

**CASHCAT은 소스 간 괴리가 완전히 해소되고 3소스 모두 뚜렷한 마이너스로 수렴했다.** 지난
회차 HL만 플러스(+1.19%)이고 온체인(-7.65%)·Aster(-8.38%)는 마이너스로 갈렸던 것과 달리,
이번 회차는 HL **-13.48%**, 온체인(CoinGecko cash-cat) **-13.97%**, Aster **-13.58%**로
세 소스가 거의 동일한 수준으로 수렴했다 — 이번엔 방향성 신뢰도가 높다. 다만 Aster의
거래량은 $1.05M→**$17.2K**로 급감(전회차 대비 약 1/60)해 유동성 자체는 매우 얇아진 상태다.

**ATOM은 4벤뉴 동시 플러스를 2회차째 유지했다** — B+B +0.45%→**+0.85%**, OKX
+2.12%→**+0.78%**(감속), HL +0.05%→**+0.90%**, Aster +0.71%→**+1.07%**. 방향은 유지되나
OKX는 오히려 폭이 줄었다.

**CAP는 마이너스에서 거의 손익분기권까지 회복했다** — OKX -4.73%→**-0.54%**, Aster
-2.39%→**+0.96%**(플러스 전환)로 지난 회차의 급반전이 다시 완화 방향으로 되돌아가는
모습이다.

**BEAT는 재악화가 소폭 진정됐다** — OKX -20.02%→**-19.31%**, Binance -19.89%→**-18.81%**로
소폭 개선됐으나 Aster는 오히려 -19.07%→**-19.86%**로 더 악화돼 소스 간 온도차가 있다.
여전히 3소스 모두 -18~-20%대의 깊은 마이너스권이다.

**BSB는 OKX·Aster 양쪽 모두 플러스로 수렴했다** — OKX -0.17%→**+0.67%**(플러스 재반전),
Aster +0.23%→**+0.79%**로 지난 회차의 방향 혼조가 정리됐다.

**BANK는 OI 안정 속에 가격 상승세가 추가로 확대됐다** — B+B +2.06%→**+3.97%**, Aster는
+0.48%→**+5.28%**로 더 크게 상승했다. Aster 자체 OI는 $274.6K→**$279.9K**로 여전히 거의
무변화라 OI 반등은 CEX(B+B) 쪽에 국한된 흐름이 이어지고 있다.

**ALLO는 플러스에서 마이너스로 반전했다** — B+B +1.97%→**-1.92%**, Aster도
+2.59%→**-1.91%**로 동조 반전했다.

**HYPE·HYNA:HYPE는 마이너스에서 다시 플러스로 반전했다** — HYPE(HL) -0.92%→**+0.56%**,
HYNA:HYPE(HL) -0.82%→**+0.92%**. **FARTCOIN(HL)은 마이너스 반전 2회차째로 낙폭이
확대**됐다(-1.54%→**-2.17%**). **ETHFI(HL)도 재악화 2회차째**다(-2.91%→**-3.71%**).

**KAITO·BICO는 개선을 이어갔다.** KAITO는 OKX -1.38%→**-0.80%**, Binance
-1.41%→**-0.66%**, HL -1.98%→**-1.77%**로 손익분기권에 더 근접했다(OKX·Binance는 -1%
미만까지 근접). BICO는 OKX -3.95%→**-3.83%**, Binance -3.57%→**-3.73%**, Aster
-3.43%→**-3.20%**로 대체로 -3.5%대에서 플러토를 이루는 모습이다.

**AIO는 개선 3회차째로 낙폭이 추가로 줄었다**(B+B -19.07%→**-13.99%**, Aster
-18.46%→**-14.74%**). **1000RATS는 4회차째 플러스를 유지하나 폭이 더 줄었다**(B+B
+14.32%→**+11.17%**, Aster +15.31%→**+10.80%**).

**AAVE는 8회차째 플러토를 이어가며 폭이 더 축소됐다**(B+B +1.67%→**+0.58%**, 펀딩도 더
낮아짐).

**ADA는 마이너스 방향을 유지했다** — B+B -0.33%→**-0.40%**, HL -0.26%→**-0.37%**, OKX
-0.06%→**-0.40%**로 대체로 동조 마이너스인데, **Aster만 -0.40%→+0.12%로 근소 플러스로
이탈**해 소스 간 분기가 발생했다.

**APR은 방향(플러스)을 4회차째 유지하며 소폭 재가속했다**(B+B +8.63%→**+9.38%**, OKX
+9.12%→**+9.87%**, Aster +8.84%→**+10.39%**).

**ASTER(자체토큰)는 지난 회차의 CEX(B+B) OI 급감이 이번 회차 안정화됐다** —
$109.49M→**$109.61M**로 거의 무변화, Aster·HL 자체 OI도 여전히 안정적이다.

**메이저(BTC·ETH)는 감속에서 안정화 국면으로 접어들었다** — dYdX BTC +0.53%→**+0.41%**,
HL BTC +0.40%→**+0.44%**; dYdX ETH +0.36%→**+0.36%**, HL ETH +0.26%→**+0.28%**로 대체로
보합권에 머물렀다. **SOL(dYdX)도 이번엔 상승세가 멈추고 정체됐다**(+1.70%→**+1.69%**).

**BTW(Aster)는 확장을 4회차째 이어갔다**(+12.79%→+14.89%→**+17.14%**). **GIGGLE(OKX,
단일소스)은 마이너스 확대가 3회차째다**(-4.39%→**-6.81%**). **CORE는 소폭
개선됐다**(-5.03%→**-3.17%**). **MMT는 손익분기권 플러토가 5회차째**(-0.71%→**-0.77%**).
**GRAM은 손익분기권 플러토를 이어갔다**(-0.45%→**-0.53%**). **ALGO는 대체로 무변화 범위
내에서 소폭 더 악화됐다**(-0.64%→**-1.16%**). **PIPPIN(OKX, 단일소스)은 재가속 폭이 사실상
정체됐다**(+6.77%→**+6.79%**). **APEX는 방향(플러스)을 3회차째 유지했다**(Bybit
+1.21%→**+1.92%**, HL +1.32%→**+1.62%**).

**데이터 품질 — funding 단위 오류를 추가 발견해 정정했다(★ 이번 회차 최우선 수정사항).**
최초 게시본에서는 "OKX 14개 심볼의 `public/funding-rate`를 직접 재조회해 전부 raw fraction
범위에 있어 신규 스케일 이상 없음"이라고 기술했는데, 이는 **OKX에 한해서만 확인한
것**이었고 점검 범위를 넘어선 결론이었다. 부모 세션의 검증 요청으로 재점검한 결과,
**CoinGecko `derivatives/exchanges/{hyperliquid,aster,bybit}` 및 `binance_futures` 경유로
확보한 funding_rate 필드가 실제로는 percent 단위**(예: "0.005"는 0.005%=0.00005 fraction)로
반환되고 있었는데, 이를 raw fraction으로 오인해 그대로 저장했음을 발견했다.

**교차검증 근거**: APR의 OKX 직접조회값(`0.00005`, raw fraction 확인됨)과 CoinGecko
Binance값(`0.005`)을 percent로 해석하면 0.005%→0.00005로 **정확히 일치**한다. ATOM도 OKX
직접값(`-0.0001691`)과 CoinGecko값(`-0.019`)을 percent로 해석하면 -0.019%→-0.00019로
근접 일치한다. 반면 fraction으로 그대로 해석하면 두 값이 100배 이상 벌어져 모순된다.
**직접 API(OKX `public/funding-rate`, Binance `premiumIndex`, dYdX `nextFundingRate`)는
원래부터 raw fraction이 맞고 오류가 없다** — 문제는 CoinGecko 경유 데이터에 한정된다.

**정정 범위**: 이번 회차 cex·dex 배열의 funding 값 중 Hyperliquid 전체, Aster 전체(CASHCAT
포함), Bybit(CoinGecko대체) 전체, 그리고 Binance+Bybit 가중평균 중 CoinGecko 유래 성분(ACE·
AAVE·ATOM·ASTER·AIO·1000RATS·ALGO·ADA·BANK·APR·ALLO의 Bybit 성분)을 전부 `/100` 보정해
raw fraction으로 통일했다. 대표 사례: ACE B+B -0.15125→**-0.0015125**, BICO Aster
-0.146→**-0.00146**(가장 우려됐던 값), 1000RATS B+B 0.03408→**0.0003408**. **과거
회차 기록은 소급수정하지 않는다** — 이 클래스 오류는 이번 회차 검증에서 처음 발견됐다.

**Bybit 직접 API도 이번 회차 403으로 회귀했다** — ACEUSDT·AEONUSDT·APEXUSDT·KAITOUSDT·
BEATUSDT·BICOUSDT 등 시도한 전 심볼에서 403이 재현돼 CoinGecko `derivatives/exchanges/bybit`
경유로 대체 확보했다(수치는 위 percent→fraction 보정 적용됨).

**BTC 도미넌스는 56.64%→56.62%, 총시총은 $2.294조→$2.289조**로 둘 다 대체로 무변화.

**OrangeX는** 이번 회차도 코드1000(No service found) 오류가 재현돼 서비스 중단이
**29회차·약 59.75시간**으로 확대됐다. **Aster ETH truncation도 11회차 연속** 지속됐다
(직접 API 403 재확인).

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

funding은 raw fraction(예: 0.00005 = 8시간당 0.005%) 기준으로 통일. `[CG→frac]` 표기는
이번 회차 CoinGecko percent 값을 `/100` 보정했음을 뜻함.

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [재가속] | Binance+Bybit(가중평균) | $717.23M | $27.80M | -0.0015125 [CG→frac] | +41.658% | WebSearch로도 신규 촉매 미확인, 원인 계속 미상 | ace-accelerates-again-cause-still-unconfirmed |
| **KAITO** [손익분기 근접 4회차] | OKX(직접API) | $29.76M | $4.70M | -0.0000831 | -0.804% | 개선 지속 | kaito-nears-breakeven-fourth-round |
| KAITO [손익분기 근접 4회차] | Binance(직접API) | $36.59M | $14.78M | -0.00014643 | -0.656% | OKX·HL과 동조 | kaito-nears-breakeven-fourth-round |
| KAITO [재확인 실패] | Bybit | — | — | — | — | 구조적 미상장 | reconfirmation-failed-again-not-carried-forward |
| **AAVE** [플러토 8회차] | Binance+Bybit(가중평균) | $55.77M | $84.15M | 0.00003789 [CG→frac] | +0.584% | 폭 추가 축소 | aave-plateau-decelerates-eighth-round |
| **BEAT** [소폭 진정] | OKX(직접API) | $120.82M | $5.67M | 0.0006958 | -19.313% | 재악화 후 소폭 진정, 여전히 깊은 마이너스 | beat-stabilizes-still-deeply-negative |
| BEAT [소폭 진정] | Binance(직접API) | $105.53M | $10.48M | 0.00035003 | -18.809% | OKX와 동조 | beat-stabilizes-still-deeply-negative |
| **BICO** [플러토 4회차] | OKX(직접API) | $18.12M | $2.52M | -0.0009891 | -3.827% | -3.7%대 플러토 | bico-plateaus-near-breakeven-fourth-round |
| BICO [플러토 4회차] | Binance(직접API) | $19.20M | $5.30M | -0.00387739 | -3.732% | OKX·Aster와 동조 | bico-plateaus-near-breakeven-fourth-round |
| BICO [재확인 실패] | Bybit | — | — | — | — | 구조적 미상장 | reconfirmation-failed-again-not-carried-forward |
| **ATOM** [4벤뉴 플러스 2회차] | Binance+Bybit(가중평균) | $20.08M | $30.08M | -0.0002090 [CG→frac] | +0.848% | 방향 유지 | atom-holds-positive-second-round-four-venues |
| ATOM [4벤뉴 플러스 2회차] | OKX(직접API) | $4.04M | $3.81M | -0.0001691 | +0.778% | 폭은 감속 | atom-holds-positive-second-round-four-venues |
| **ASTER** [CEX OI 안정화] | Binance+Bybit(가중평균) | $17.20M | $109.61M | 0.00002684 [CG→frac] | +0.116% | OI 급감이 이번 회차 안정화 | aster-cex-oi-stabilizes-after-halving |
| **AIO** [개선 3회차] | Binance+Bybit(가중평균) | $52.47M | $5.97M | 0.00005 [CG→frac] | -13.987% | 낙폭 추가 축소 | aio-continues-improving-third-round |
| **1000RATS** [4회차 플러스] | Binance+Bybit(가중평균) | $98.83M | $18.14M | 0.0003408 [CG→frac] | +11.171% | 급등 폭 지속 축소 | 1000rats-continues-decelerating-fourth-round |
| ALGO [무변화 지속] | Binance+Bybit(가중평균) | $7.89M | $13.74M | -0.0001798 [CG→frac] | -1.162% | 범위 내 소폭 악화 | algo-remains-roughly-flat-continues |
| MMT [플러토 5회차] | OKX(직접API) | $4.40M | $2.11M | -0.0001674 | -0.771% | 손익분기권 플러토 지속 | mmt-plateau-continues-fifth-round |
| AEON [진정 4회차] | OKX(직접API) | $68.39M | $3.86M | -0.0000366 | +4.602% | 5%안팎 수렴 유지 | aeon-moderation-continues-fourth-round |
| AEON [진정 4회차] | Bybit(CoinGecko대체) | $8.42M | $1.22M | 0.00005 [CG→frac] | +4.918% | 직접API 403 회귀로 CoinGecko 경유 | aeon-moderation-continues-fourth-round |
| **CAP** [플러스권 회복] | OKX(직접API) | $67.13M | $10.08M | -0.0000606 | -0.541% | 마이너스에서 거의 손익분기권까지 회복 | cap-recovers-toward-flat-after-reversal |
| CORE [소폭 개선] | OKX(직접API) | $2.27M | $0.94M | 0.0000289 | -3.175% | 여전히 무변화권 근처 변동 | core-improves-slightly-still-negative |
| GRAM [플러토 지속] | OKX(직접API) | $5.07M | $6.39M | 0.00005 | -0.528% | 손익분기권 플러토 | gram-plateaus-near-flat |
| **GIGGLE** [악화 3회차] | OKX(직접API) | $10.86M | $1.59M | 0.00005 | -6.811% | 마이너스 확대 지속 — 단일소스 유의 | giggle-worsens-third-round |
| **PIPPIN** [정체] | OKX(직접API) | $3.56M | $1.87M | 0.0000974 | +6.789% | 재가속 폭 정체 — 단일소스 유의 | pippin-plateaus-fourth-round |
| **ADA** [마이너스 유지] | Binance+Bybit(가중평균) | $124.63M | $137.54M | 0.00004682 [CG→frac] | -0.401% | Aster만 이탈, 소스 간 분기 | ada-holds-negative-aster-diverges-positive |
| ADA [마이너스 유지] | OKX(직접API) | $27.60M | $23.83M | 0.0001 | -0.403% | B+B·HL과 동조 | ada-holds-negative-aster-diverges-positive |
| **BSB** [플러스 수렴] | OKX(직접API) | $5.75M | $2.19M | 0.00005 | +0.667% | Aster와 함께 양쪽 모두 플러스로 수렴 | bsb-converges-positive-both-sources |
| **ALLO** [마이너스 반전] | Binance+Bybit(가중평균) | $46.73M | $16.64M | 0.00005 [혼합, Bybit성분 CG→frac] | -1.921% | 플러스에서 마이너스로 반전 | allo-flips-negative |
| **APEX** [방향유지 3회차] | Bybit(CoinGecko대체) | $0.95M | $1.57M | 0.00005 [CG→frac] | +1.918% | 직접API 403 회귀로 CoinGecko 경유 | apex-holds-positive-third-round |
| **BANK** [가격 추가 상승] | Binance+Bybit(가중평균) | $23.83M | $15.62M | -0.0000133 [CG→frac] | +3.966% | OI 안정 속 가격 상승세 확대 | bank-price-accelerates-oi-stable |
| **APR** [방향유지 4회차] | Binance+Bybit(가중평균) | $76.27M | $14.34M | 0.00005 [CG→frac] | +9.383% | 소폭 재가속 | apr-holds-positive-fourth-round |
| APR [방향유지 4회차] | OKX(직접API) | $69.52M | $3.41M | 0.00005 | +9.874% | B+B·Aster와 동시 재가속 | apr-holds-positive-fourth-round |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

funding은 raw fraction 기준. `[CG→frac]` = 이번 회차 CoinGecko percent 값을 `/100` 보정.

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [재가속] | Hyperliquid | $3.73M | $2.03M | -0.00034 [CG→frac] | +42.218% | B+B·Aster와 동조 추가 가속 | ace-accelerates-again-cause-still-unconfirmed |
| ACE [서비스 중단] | OrangeX | — | — | — | — | 29회차·약 59.75시간 | orangex-service-outage-continues |
| **ACE** [재가속] | Aster | $0.80M | $0.28M | -0.00026 [CG→frac] | +41.419% | HL·B+B와 동조 | ace-accelerates-again-cause-still-unconfirmed |
| BANK [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| **BANK** [가격 추가 상승] | Aster | $0.03M | $0.28M | 0.00001 [CG→frac] | +5.278% | 자체 OI는 거의 무변화 유지 | bank-price-accelerates-oi-stable |
| KAITO [손익분기 근접 4회차] | Hyperliquid | $3.16M | $5.75M | -0.00001 [CG→frac] | -1.766% | OKX·Binance와 동조 개선 | kaito-nears-breakeven-fourth-round |
| KAITO [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| CAP [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| **CAP** [플러스권 회복] | Aster | $0.07M | $0.19M | -0.00002 [CG→frac] | +0.956% | OKX와 함께 플러스로 회복 반전 | cap-recovers-toward-flat-after-reversal |
| BICO [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| **BICO** [플러토 4회차] | Aster | $0.10M | $0.09M | -0.00146 [CG→frac, 최초게시본 -0.146 오류 정정] | -3.201% | OKX·Binance와 동조 | bico-plateaus-near-breakeven-fourth-round |
| BSB [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| **BSB** [플러스 수렴] | Aster | $0.11M | $0.12M | 0.00001 [CG→frac] | +0.794% | OKX와 함께 플러스로 수렴 | bsb-converges-positive-both-sources |
| BLESS [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| BLESS [악화 지속] | Aster | $0.04M | $0.10M | 0.00005 [CG→frac] | -7.039% | 재악화 폭 더 커짐 지속 | bless-worsens-further-continues |
| **CASHCAT** [3소스 수렴] | Hyperliquid | $7.20M | $13.38M | 0.00001 [CG→frac] | -13.476% | 온체인·Aster와 함께 뚜렷한 마이너스로 수렴 | cashcat-three-sources-converge-negative |
| CASHCAT [서비스 중단] | OrangeX | — | — | — | — | 4소스 비교 핵심 축 공백 | orangex-service-outage-continues |
| **CASHCAT** [3소스 수렴] | Aster | $0.02M | $0.71M | -0.00003 [CG→frac] | -13.579% | HL·온체인과 수렴 — 거래량 급감(1/60) | cashcat-three-sources-converge-negative |
| AEON [진정 4회차] | Aster | $0.07M | $0.33M | 0.00001 [CG→frac] | +5.866% | OKX·Bybit와 5%대 수렴 유지 | aeon-moderation-continues-fourth-round |
| AEON [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| BEAT [소폭 악화] | Aster | $0.37M | $0.17M | 0.00001 [CG→frac] | -19.858% | OKX·Binance와 달리 소폭 더 악화 | beat-stabilizes-still-deeply-negative |
| BEAT [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| **HYPE** [플러스 반전] | Hyperliquid | $239.92M | $1,334.40M | 0.0 | +0.558% | 마이너스에서 다시 플러스로 | hype-flips-positive-again |
| GRAM [플러토 지속] | Hyperliquid | $1.83M | $15.38M | 0.00001 [CG→frac] | -0.52% | OKX와 함께 손익분기권 플러토 | gram-plateaus-near-flat |
| **BTW** [확장 4회차] | Aster | $1.07M | $11.22M | 0.0001 [CG→frac] | +17.142% | 확장 지속 | btw-continues-expanding-fourth-round |
| HYNA:PUMP [개선] | Hyperliquid | $0.04M | $0.18M | 0.00006 [CG→frac] | -0.423% | 낙폭 축소 지속 | updates-normally-no-stale-recurrence |
| HYNA:HYPE [플러스 반전] | Hyperliquid | $0.09M | $0.65M | 0.00001 [CG→frac] | +0.923% | HYPE(HL)와 동조 반전 | hype-flips-positive-again |
| HYNA:SOL-USD [소폭 상승] | Hyperliquid | $0.03M | $0.54M | 0.00001 [CG→frac] | +1.483% | SOL(dYdX)과 동조 | majors-sol-decelerates-still-positive |
| HYNA:BTC-USD [안정] | Hyperliquid | $0.53M | $2.20M | 0.00001 [CG→frac] | +0.653% | BTC와 동조 대체로 안정 | majors-btc-eth-stabilize-after-deceleration |
| HYNA:ETH-USD [안정] | Hyperliquid | $0.24M | $1.63M | 0.00001 [CG→frac] | +0.262% | ETH(HL)과 동조 안정 | majors-btc-eth-stabilize-after-deceleration |
| SOL [미확인] | Hyperliquid | — | — | — | — | 별도 티커 부재 지속 | remains-unconfirmed-no-separate-market |
| **1000RATS** [4회차 플러스] | Aster | $0.27M | $0.05M | 0.00006 [CG→frac] | +10.795% | B+B와 함께 폭 지속 축소 | 1000rats-continues-decelerating-fourth-round |
| AIO [개선 3회차] | Aster | $0.17M | $0.09M | 0.00005 [CG→frac] | -14.737% | B+B와 동조 개선 지속 | aio-continues-improving-third-round |
| AIO [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| AAVE [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| AAVE [플러토 8회차] | Aster | $0.19M | $4.48M | 0.0001 [CG→frac] | +0.718% | 폭 추가 축소 | aave-plateau-decelerates-eighth-round |
| AAVE [플러토 8회차] | Hyperliquid | $3.40M | $57.65M | 0.00001 [CG→frac] | +0.42% | B+B·Aster와 동조 감속 | aave-plateau-decelerates-eighth-round |
| ADA [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| **ADA** [소스 분기] | Aster | $0.17M | $1.20M | 0.0001 [CG→frac] | +0.116% | B+B·HL과 달리 근소 플러스 | ada-holds-negative-aster-diverges-positive |
| **ADA** [마이너스 유지] | Hyperliquid | $5.32M | $29.10M | 0.00001 [CG→frac] | -0.374% | B+B·OKX와 동조 마이너스 유지 | ada-holds-negative-aster-diverges-positive |
| ALGO [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| ALGO [무변화] | Aster | $0.01M | $0.04M | 0.00001 [CG→frac] | -0.599% | 초저활동 시장, 값 변동 미미 | algo-remains-roughly-flat-continues |
| ALGO [무변화] | Hyperliquid | $0.32M | $1.88M | -0.00002 [CG→frac] | -0.924% | B+B·Aster와 함께 대체로 무변화 | algo-remains-roughly-flat-continues |
| ASTER [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| **ASTER** [자체 OI 안정] | Aster | $11.85M | $221.90M | 0.00006 [CG→frac] | +0.166% | 자체 OI 안정 — CEX OI도 안정화 | aster-cex-oi-stabilizes-after-halving |
| ASTER [자체 OI 안정] | Hyperliquid | $0.58M | $13.55M | 0.00001 [CG→frac] | +0.108% | Aster프로토콜과 동조 안정 | aster-cex-oi-stabilizes-after-halving |
| **ETH** [안정화] | dYdX | $8.03M | $23.78M | 0.000005 | +0.357% | HL과 함께 대체로 안정 | majors-btc-eth-stabilize-after-deceleration |
| BTC [안정화] | dYdX | $3.04M | $18.13M | 0.000006 | +0.407% | 메이저 전반 안정화 | majors-btc-eth-stabilize-after-deceleration |
| SOL [정체] | dYdX | $0.42M | $4.96M | 0.0 | +1.690% | 상승세 멈추고 정체 | majors-sol-decelerates-still-positive |
| BTC [안정화] | Hyperliquid | $1,371.97M | $2,678.29M | 0.0 | +0.437% | dYdX와 함께 안정화 | majors-btc-eth-stabilize-after-deceleration |
| **ETH** [안정화] | Hyperliquid | $665.38M | $1,764.97M | 0.00001 [CG→frac] | +0.283% | dYdX와 함께 안정화 | majors-btc-eth-stabilize-after-deceleration |
| ATOM [4벤뉴 플러스 2회차] | Hyperliquid | $0.44M | $1.71M | -0.00004 [CG→frac] | +0.897% | B+B·OKX·Aster와 동조 유지 | atom-holds-positive-second-round-four-venues |
| BTC [안정화] | Aster | $578.31M | $809.09M | 0.00001 [CG→frac] | +0.422% | 메이저 전반 안정화 | majors-btc-eth-stabilize-after-deceleration |
| ETH [truncation 11연속] | Aster | — | — | — | — | 직접 API도 403 재확인 | truncation-continues-eleventh-round |
| **ETHFI** [재악화 2회차] | Hyperliquid | $3.24M | $11.50M | 0.00001 [CG→frac] | -3.705% | 낙폭 확대 | ethfi-worsens-second-round |
| **FARTCOIN** [악화 2회차] | Hyperliquid | $4.22M | $29.70M | 0.00001 [CG→frac] | -2.169% | 마이너스 반전 후 낙폭 확대 | fartcoin-worsens-second-round |
| HYPER [무변화] | Hyperliquid | $0.06M | $0.20M | 0.00001 [CG→frac] | -1.068% | 대체로 무변화 유지 지속 | hyper-remains-roughly-flat |
| **APEX** [방향유지 3회차] | Hyperliquid | $0.22M | $0.62M | 0.00001 [CG→frac] | +1.615% | Bybit와 함께 플러스 유지 | apex-holds-positive-third-round |
| ALLO [서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-continues |
| ALLO [마이너스 반전] | Aster | $0.18M | $0.07M | 0.00001 [CG→frac] | -1.911% | B+B와 함께 플러스에서 마이너스로 | allo-flips-negative |
| ATOM [4벤뉴 플러스 2회차] | Aster | $0.01M | $1.69M | 0.00004 [CG→frac] | +1.067% | B+B·OKX·HL과 동조 유지 | atom-holds-positive-second-round-four-venues |
| **APR** [방향유지 4회차] | Aster | $0.27M | $0.34M | 0.00001 [CG→frac] | +10.385% | B+B·OKX와 동시 재가속 | apr-holds-positive-fourth-round |
| APR [미상장 추정] | Hyperliquid | — | — | — | — | 이번 회차도 미발견 | not-listed-on-hyperliquid |
| **CASHCAT** [3소스 수렴] | 온체인(cash-cat, CoinGecko) | — | — | — | -13.97% | HL·Aster와 함께 마이너스 수렴 — 가격 $0.097164 | cashcat-three-sources-converge-negative |

## 테마 태그

1. **ACE**: 추가 가속(B+B +32.1%→+41.7%, HL +32.2%→+42.2%, Aster +31.9%→+41.4%) — WebSearch로
   신규 촉매 미확인, 원인 계속 미상. Bitget PoolX만 유효 촉매로 유지
   (ace-accelerates-again-cause-still-unconfirmed).
2. **CASHCAT**: HL·온체인·Aster 3소스가 이번 회차 뚜렷한 마이너스(-13.0~-14.0%대)로 수렴 —
   지난 회차의 소스 간 괴리 완전 해소 (cashcat-three-sources-converge-negative).
3. **ATOM**: 4벤뉴 동시 플러스 2회차째 유지(폭은 감속) (atom-holds-positive-second-round-four-venues).
4. **CAP**: 마이너스에서 거의 손익분기권까지 회복(OKX -4.73%→-0.54%, Aster
   -2.39%→+0.96%) (cap-recovers-toward-flat-after-reversal).
5. **BEAT**: 재악화 후 소폭 진정 — OKX·Binance는 완화, Aster는 오히려 소폭 더 악화
   (beat-stabilizes-still-deeply-negative).
6. **BSB**: OKX·Aster 양쪽 모두 플러스로 수렴 (bsb-converges-positive-both-sources).
7. **BANK**: OI 안정 속 가격 상승세 추가 확대(+2.06%→+3.97%) (bank-price-accelerates-oi-stable).
8. **ALLO**: 플러스에서 마이너스로 반전(+1.97%→-1.92%) — B+B·Aster 동조 (allo-flips-negative).
9. **HYPE·HYNA:HYPE**(HL): 마이너스에서 다시 플러스로 반전 (hype-flips-positive-again).
10. **FARTCOIN**(HL): 마이너스 반전 2회차째, 낙폭 확대(-1.54%→-2.17%) (fartcoin-worsens-second-round).
11. **ETHFI**(HL): 재악화 2회차째(-2.91%→-3.71%) (ethfi-worsens-second-round).
12. **KAITO**: 개선 지속, 손익분기권 더 근접(OKX·Binance 모두 -1%미만) (kaito-nears-breakeven-fourth-round).
13. **BICO**: 개선 4회차째, -3.7%대 플러토 (bico-plateaus-near-breakeven-fourth-round).
14. **AIO**: 개선 3회차째, 낙폭 추가 축소(-19%→-14%) (aio-continues-improving-third-round).
15. **1000RATS**: 급등 폭 지속 축소(+14.3%→+11.2%), 4회차째 플러스
    (1000rats-continues-decelerating-fourth-round).
16. **AAVE**: 8회차째 플러토, 폭 추가 축소(+1.67%→+0.58%) (aave-plateau-decelerates-eighth-round).
17. **ADA**: 마이너스 방향 유지 — Aster만 근소 플러스로 이탈해 소스 간 분기 발생
    (ada-holds-negative-aster-diverges-positive).
18. **APR**: 방향(플러스) 4회차째 유지, 소폭 재가속 (apr-holds-positive-fourth-round).
19. **ASTER**(자체토큰): CEX OI 급감이 이번 회차 안정화(109.49M달러→109.61M달러로 거의
    무변화) (aster-cex-oi-stabilizes-after-halving).
20. **메이저**(BTC·ETH): dYdX·HL 양쪽 모두 감속에서 안정화 국면으로 전환
    (majors-btc-eth-stabilize-after-deceleration).
21. **SOL**(dYdX): 메이저 중 유일하게 상승세였으나 이번엔 정체(+1.70%→+1.69%)
    (majors-sol-decelerates-still-positive).
22. **BTW**(Aster): 확장 4회차째 지속(+12.79%→+14.89%→+17.14%) (btw-continues-expanding-fourth-round).
23. **GIGGLE**(OKX, 단일소스): 마이너스 확대 3회차째(-4.39%→-6.81%) (giggle-worsens-third-round).
24. **CORE**: 소폭 개선(-5.03%→-3.17%), 여전히 무변화권 근처 변동 (core-improves-slightly-still-negative).
25. **MMT**: 손익분기권 플러토 5회차째(-0.71%→-0.77%) (mmt-plateau-continues-fifth-round).
26. **GRAM**: 손익분기권 플러토 지속(-0.45%→-0.53%) (gram-plateaus-near-flat).
27. **ALGO**: 대체로 무변화 범위 내 소폭 악화(-0.64%→-1.16%) (algo-remains-roughly-flat-continues).
28. **PIPPIN**(OKX, 단일소스): 재가속 폭이 정체(+6.77%→+6.79%) (pippin-plateaus-fourth-round).
29. **APEX**: 방향(플러스) 3회차째 유지 (apex-holds-positive-third-round).
30. **데이터**: Bybit 직접 API가 이번 회차 다시 403으로 회귀(직전 회차 "대부분 복구"와
    반대) — CoinGecko bybit 경유로 대체 확보 (bybit-direct-api-regresses-to-403).
31. **데이터(★정정)**: 최초 게시본의 "OKX 14건 스팟체크, 신규 스케일 이상 없음"은 OKX에
    한정된 결론이었다. 부모 세션 검증으로 CoinGecko `derivatives/exchanges` 경유(Hyperliquid·
    Aster·Bybit·Binance) funding_rate가 실제로는 percent 단위(raw fraction의 100배)였음을
    발견 — 이번 회차 해당 값 전부를 `/100` 보정해 raw fraction으로 통일. 직접 API(OKX·
    Binance premiumIndex·dYdX)는 원래부터 정상이었다 (funding-unit-error-coingecko-percent-vs-fraction-corrected).
32. **데이터**: OrangeX 서비스 중단이 29회차(약 59.75시간)로 확대 (orangex-service-outage-continues).
33. **글로벌**: BTC 도미넌스 56.64%→56.62%, 총시총 2.294조달러→2.289조달러로 대체로
    무변화 (global-dominance-roughly-flat).
34. **ACE 언락**: 지난 회차 tokenomist.ai 확인사항(8/18 언락 없음, 다음 언락 9/3) 유지 —
    이번 회차 추가 재확인은 없음 (ace-unlock-rumor-refuted-by-tokenomist).
35. **Aster ETH**: truncation 11회차 연속 — 직접 API도 403 재확인
    (truncation-continues-eleventh-round).
36. **주식화·상품 토큰은 전부 제외.** 리스트 전 종목 크립토 네이티브 확인 유지
    (stock-commodity-tokens-excluded-crypto-native-confirmed).

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한 전체
시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에 따라
cex/dex 리스트에서 전부 제외했다; (c) OKX는 `market/tickers`(instType=SWAP, 벌크)와
`public/open-interest`(instType=SWAP, 벌크) 두 엔드포인트를 우선 사용했고, 벌크 응답에서
CAP·CORE·ATOM·BSB·ACE가 누락돼 `market/ticker`(개별 GET)로 재조회했다(ACE는 이번 회차도
SWAP 티커 자체가 없음을 재확인) — funding-rate는 이번 회차 `public/funding-rate` 개별 GET
14건으로 직접 재조회했다(**이 14건은 raw fraction임을 확인**, 아래 (x) 참조). USD 거래량은
`volCcy24h × last`로 계산했다(OKX volCcy24h은 기초자산 수량 단위 — 단 KAITO·BICO 등 일부
심볼은 volCcy24h이 이미 vol24h와 동일해 ctVal=1로 추정, 계산방식은 유지); (d) 복수 거래소
종목의 `chg24`는 이번 회차도 Binance+Bybit 거래량 가중평균으로 산출했다(OI는 두 거래소
합산). **funding도 동일하게 가중평균했으나, Binance·Bybit 성분이 CoinGecko 경유일 경우
percent→fraction 보정 후 가중평균했다**(ALLO만 Binance 직접·Bybit CoinGecko의 혼합소스); (e)
Hyperliquid 데이터는 이번 회차도 CoinGecko `derivatives/exchanges/hyperliquid` 경유로
확보했다(직접 API `info`는 POST 전용이라 GET 전용 도구로 접근 불가) — **HL funding은 전부
CoinGecko 경유이므로 percent→fraction 보정을 적용했다**; (f) **KAITO·BICO의 Binance 상장이
이번 회차도 유지 확인**됐다; (g) BTW·CASHCAT·HYNA 계열은 DEX에서만 상장이 확인돼 해당
섹션에서만 집계했다; (h) dYdX BTC/ETH/SOL은 `indexer.dydx.trade` REST(GET)로 raw JSON
필드를 직접 요청해 계산했다(`priceChange24H`가 달러 절대값임을 재확인해 `chg% =
priceChange24H / (oraclePrice - priceChange24H)`로 계산, `nextFundingRate` 필드를 raw
fraction 그대로 반영 — **직접 조회이므로 보정 불필요**, OI는 `openInterest`(코인 수량) ×
`oraclePrice`, 거래량은 `volume24H` 필드 직접 사용). **이번 회차 dYdX·HL 양쪽 모두 BTC·ETH가
감속에서 안정화로 전환**됐다; (i) **Aster 직접 API는 이번 회차도 403** — CoinGecko
파생거래소 id `aster`로 대부분 확보했다(**funding은 percent→fraction 보정 적용**). ETH는
truncation이 지속돼 **11회차 연속 미확인**이다; (j) **OrangeX API의 전면 서비스 중단이 이번
회차도 지속**돼 29회차·약 59.75시간에 달했다(`getCurrencies` → 코드 1000 "No service found"
재현); (k) **Bybit 직접 API가 이번 회차 다시 403으로 회귀**했다(ACEUSDT·AEONUSDT·
APEXUSDT·KAITOUSDT·BEATUSDT·BICOUSDT 시도 전부 403) — 직전 회차 "대부분 복구"와 반대
방향의 변화라 다음 회차에서 재확인이 필요하다. CoinGecko `derivatives/exchanges/bybit`
경유로 필요한 심볼(ACE·AAVE·ATOM·AEON·APEX·ADA·BANK·APR·ASTER·1000RATS·AIO·ALGO·ALLO)을
전부 확보했다(**funding은 percent→fraction 보정 적용**) — KAITO·BICO·BEAT·MMT·CASHCAT·BTW는
CoinGecko Bybit 데이터에서도 여전히 "없음"으로 확인돼 구조적 미상장 판단이 유지된다; (l)
KAITO의 OI는 OKX·Binance·HL 모두 USD환산 기준이나 산출 방법이 달라 직접 비교가 아닌 각자의
추세로만 해석해야 한다; (m) **ACE의 이번 회차 추가 급등에 대해 WebSearch로 신규 촉매를
탐색**했으나 8/7·8/13 관련 보도(Bitget PoolX 상장)만 재확인됐고, 40%대까지 확대된 원인은
확인되지 않아 미상으로 남긴다; (n) **ACE는 OKX SWAP 티커 자체가 존재하지 않음**을
유지한다(이번 회차 개별 market/ticker 조회로도 재확인); (o) **HL SOL-USD**는 이번 회차도
별도 존재가 확인되지 않았다(HYNA:SOL-USD와 동일 값으로만 확인); (p) **OrangeX는 이번
회차도 전면 서비스 중단으로 funding 필드를 포함한 모든 데이터가 미확인**이다; (q) dYdX
메이저는 이번 회차 BTC·ETH·SOL 모두 감속·정체로 안정화 국면에 접어들었다; (r)
**KAITO·BICO·BEAT·CASHCAT·BTW Bybit는 이번 회차도 부재를 재확인**했다(구조적 미상장 성격,
CoinGecko 경유로도 동일하게 미발견); (s) **BTW 집계 기준 명시**: CoinMarketCap이 보고하는
"Bitway"를 기준으로 삼아 집계를 유지한다 — 초소형 밈코인 "Banana Tape Wall"·"BitWhite"와는
별개 자산; (t) **CASHCAT 현물 가격(cash-cat)**은 이번 회차 CoinGecko `simple/price` API로
재확인 성공했다(h24 -13.97%, 가격 $0.097164) — HL(-13.48%)·Aster(-13.58%)와 함께 3소스가
뚜렷한 마이너스로 수렴했다(지난 회차의 소스 간 괴리 완전 해소); (u) **ACE 언락 시각**은
지난 회차 tokenomist.ai 확인사항(8/18 언락 없음, 다음 언락 9/3)을 유지한다 — 이번 회차
추가 재확인은 하지 않았다; (v) **글로벌 시총·도미넌스**는 이번 회차 CoinGecko `/global`
엔드포인트로 재확인했다 — 총시가총액 약 $2.289조·BTC 도미넌스 56.62%·ETH 도미넌스
10.08%로 직전 회차(56.64%) 대비 대체로 무변화; (w) **도구 제약 안내**: 이번 회차는 Bash
없이 WebFetch(GET 전용)·WebSearch만으로 데이터를 수집했다 — Hyperliquid의 POST 전용
`info` 엔드포인트는 GET 도구로 접근 불가, Aster 직접 API는 403으로 CoinGecko 대체 경로를
사용했다. OKX 개별 GET 엔드포인트와 dYdX·Binance 직접조회는 안정적으로 접근했으나,
Bybit 직접조회는 이번 회차 전면 403으로 회귀해 CoinGecko 대체 경로를 사용했다; (x) **★funding
단위 오류 발견·정정(이번 회차 최우선 수정)**: 최초 게시본에서는 "OKX `public/funding-rate`
14건을 직접 재조회한 결과 전부 raw fraction 범위(대략 -0.001~0.0007 수준)에 있어 신규
스케일 이상 없음"이라고만 기술했는데, **이는 OKX 14건에 한정된 점검이었고 점검 범위를
초과한 결론이었다.** 부모 세션의 검증 요청으로 CoinGecko `derivatives/exchanges/*` 경유
funding 값을 OKX·Binance·dYdX 직접값과 교차검증한 결과, **CoinGecko의 `funding_rate`
필드가 percent 단위**(raw fraction × 100)로 반환되고 있음을 발견했다. 근거: APR의 OKX
직접값(`0.00005`)과 CoinGecko Binance값(`0.005`)을 percent로 해석 시 0.005%→0.00005로
정확히 일치, ATOM도 OKX 직접값(`-0.0001691`)과 CoinGecko값(`-0.019`→percent 해석시
-0.00019)이 근접 일치 — fraction으로 해석하면 두 값 모두 100배 이상 벌어져 모순된다.
Hyperliquid·Aster 전체와 Bybit(CoinGecko대체) 전체, Binance+Bybit 가중평균의 CoinGecko
유래 성분(대부분의 B+B 항목)이 이 오류에 해당해 전부 `/100` 보정했다. 가장 우려됐던
BICO(Aster) 값은 -0.146(오류)→**-0.00146**(정정)이다. 직접 API(OKX `public/funding-rate`,
Binance `premiumIndex`, dYdX `nextFundingRate`)는 원래부터 raw fraction이 맞고 이번
보정 대상이 아니다. **과거 회차 기록은 소급수정하지 않는다** — 이 클래스 오류는 이번
회차 검증에서 처음 발견됐으며, 다음 회차부터 CoinGecko 경유 funding은 항상 `/100`
보정 후 저장한다; (y) **신규 발견 핵심 9건**: ①ACE가 32%대에서 42%대로 추가 가속(원인
계속 미상), ②CASHCAT이 3소스 모두 뚜렷한 마이너스로 수렴(지난 회차 괴리 완전 해소),
③CAP가 마이너스에서 거의 손익분기권까지 회복, ④BSB가 양쪽 소스 모두 플러스로 수렴,
⑤HYPE·HYNA:HYPE가 다시 플러스로 반전, ⑥ALLO가 플러스에서 마이너스로 반전, ⑦Bybit
직접 API가 다시 403으로 회귀(직전 회차 복구와 반대), ⑧메이저 BTC·ETH·SOL이 감속에서
안정화 국면으로 전환, **⑨CoinGecko 경유 funding이 percent 단위였음을 발견·전면 보정
(부모 세션 검증으로 발견)**; (z) **이번 회차 종합**: ①ACE 추가 가속(헤드라인, 원인
미상), ②CASHCAT 3소스 수렴(주요 팔로업 해소), ③ATOM 4벤뉴 플러스 2회차 유지, ④CAP·BSB
회복/수렴, ⑤BEAT 소폭 진정(여전히 깊은 마이너스), ⑥BANK 가격 추가 상승, ⑦ALLO·HYPE
반전, ⑧KAITO·BICO 개선 지속, ⑨ADA 마이너스 유지(Aster만 분기), ⑩메이저 안정화,
⑪BTW 확장 4회차, ⑫Bybit 직접API 403 회귀, ⑬**funding 단위 오류(CoinGecko percent vs
fraction) 발견·전면 정정**, ⑭OrangeX 서비스 중단 29회차(약 59.75시간) 지속.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
