# 선물시장 스카우트 브리핑 — 2026-08-02 06:29 UTC (KST 2026-08-02 15:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·GMX·dYdX) 선물시장에서 지금 주목받는
> **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·상품·
> 프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-02T04:28:00Z)
> 로부터 정확히 2시간 경과한 정규 슬롯**이다.

지정 중점항목별로 보면, ①**HL LIT-USD 소실 미스터리를 해결**했다 — CoinGecko 통합 파생 스냅샷
(`/derivatives?include_tickers=unexpired`)으로 재조회한 결과 LIT-USD는 실제로는 사라지지 않았고
정상 거래 중이었다(OI **$77,664,083.26**·거래량 $8,487,517.08·funding0.125%·chg+2.91%, 2회 전
OI $77.05M과 거의 동일한 안정 수준). 즉 직전 2회 회차의 '데이터셋에서 완전히 사라짐'은 Hyperliquid
거래소 전용 엔드포인트(`/derivatives/exchanges/hyperliquid`)의 방대한 티커 목록을 WebFetch로
요약할 때 발생한 누락(truncation) 아티팩트였을 가능성이 매우 높다 — **실제 델리스팅·시장 이벤트가
아니었다.** 참고로 별도 프로토콜인 Lighter 자체 DEX에서도 동일 티커명 LIT_USDC(OI $94.73M)가 거래
중임을 확인했으나 이는 Hyperliquid의 LIT-USD와는 다른 별개 거래소/페어다.

②**1000RATS는 '피크아웃' 판단이 이번 회차 정반대로 뒤집혔다** — 직전 회차 평균+28.86%로
급감속했던 것과 달리 이번 회차 Binance+55.223%·Bybit+51.291%(평균**+53.26%**)로 재가속해 2회 전
고점(+60.75%)에 근접했다. OI도 $41.05M→**$45.09M**로 증가, funding도 10.35%→**13.15%**로
재과열됐다 — '피크아웃'이 아니라 극심한 변동성 속 반복적 급등락(chop) 패턴으로 재해석해야 한다.
OKX는 8회 연속 미확인, Aster는 +62.918%로 CEX 재가속과 정합한다.

③**ADA는 강도가 더욱 확대**됐다 — 평균+7.34%→**+9.02%**로 상승폭이 커졌고, 이번 회차
Binance(+8.888%)·OKX(+9.12%)·Aster(+8.721%)·XT.COM(+8.95%)·Gate(+9.06%)까지 추가로 확인돼 총
7개 이상 거래소에서 일관된 동반 강세가 재확인됐다(dYdX ADA-USD도 +1.04%로 정합). OI는
$119.89M→**$231.38M**로 거의 두 배 급증해 신뢰도 매우 높은 광범위 강세로 격상한다.

④**HYPER는 재가속과 동시에 funding이 더욱 극단적 마이너스로 심화**됐다 — +17.3%→**+20.1%**로
상승 지속, funding은 -7.5%→**-24.1%**로 훨씬 더 극단적(숏이 롱에 지불하는 구조 심화)돼 스퀴즈
리스크가 확대되고 있으나 거래량은 $0.67M→$0.76M로 여전히 초박막이라 해석 주의가 필요하다.

⑤**신규 급등 스캔에서 BULLA가 마이너스에서 플러스로 반전**됐다(-10.66%→**+2.80%**, 사기 의혹
리스크는 유효). **GIGGLE은 2회 연속 재확인 실패 끝에 이번 회차 XT.COM(-25.08%)·OrangeX(-26.25%)
양쪽에서 확인돼 평균-25.67%의 뚜렷한 급락이 재확인**됐다(이월 값 +0.14%는 폐기, OI는
$299.16M→$308.33M로 유사 규모 유지).

**BANK는 낙폭이 다소 완화**됐으나(-27.31%→-17.03%) **funding은 오히려 3거래소 평균 -3.43%로
다시 마이너스 전환**돼(직전 회차 '완전 정상화'였던 것과 반대 방향) 낙폭 완화와 funding 재음전이
동시에 발생하는 새로운 양상을 보였다. **BEAT는 3회 연속 낙폭이 확대**됐다(-6.77%→-13.89%→
-19.27%). **AKE는 랠리 정체가 2회 연속 이어졌고**(+4.15%→+2.99%) OI도 총 $63.21M로 거의
안정화(디레버리징 진정 국면 진입). **CAP는 개선 흐름이 계속 이어졌다**(-19.45%→-16.58%).
**AAVE는 플러스 흐름을 지속 강화**했다(+0.356%→+1.19%, 이번 회차 Binance·Bybit 2거래소 기준으로
커버리지 변경). **CASHCAT은 낙폭이 상당히 완화**돼 회복 조짐을 보였다(-5.86%→-2.62%). **APEX는
Bybit·HL 양쪽 모두 마이너스에서 플러스로 전환**됐다(Bybit-0.76%→+0.727%, HL-0.703%→+0.883%) —
3회 연속 실거래 확인에 더해 이번엔 방향까지 반전. **BLESS는 가격이 재가속**했으나
(+40.23%→+54.91%) **funding은 오히려 7.7%→4.7%로 완화**돼 디커플링 방향이 지난 회차와 반대로
뒤집혔다. **BTW는 낙폭이 더욱 확대**됐다(-24.00%→-28.25%). **메이저 리스크온은 방향은 유지하되
상승폭이 소폭 둔화**됐다 — HL HYPE-USD+0.475%(직전+0.816%)·BTC-USD+0.636%·ETH-USD+0.353%,
dYdX BTC-USD+0.654%(직전+0.81%)·ETH-USD+0.337%(직전+0.627%)로 전반 소폭 감속.

**⚠️ 데이터 이슈 현황**: (a) dYdX LIT-USD는 vol$99.1353·OI$14,551.64·chg-7.744%로 **4회 연속
소수점까지 완전 동일**해 정지 상태를 재확정(HL LIT은 위와 같이 정상 거래 확인됨과 대조적). (b)
dYdX KAITO-USD는 **8회 연속 동일(OI $0)**로 사망 판정 지속. (c) GMX
(`gmx-perpetuals-v2-arbitrum`)는 ETH/BTC 수치가 **8회 연속 소수점까지 완전 동일**해 데이터소스
영구 정지 판단을 재확정, 참고용으로만 유지한다. (d) ALLO는 이번 회차 Binance/OKX/Bybit/Aster
어디서도 재확인되지 않아 직전 값을 이월했다(재확인 필요). (e) AEON은 이번 회차 Aster 데이터가
확보되지 않아 OKX 단일 거래소 기준(-5.929%, 직전 -7.57%에서 개선 방향 재개)으로 커버리지가
축소됐다. (f) MMT는 OKX 직접 API로 -11.84%(직전-9.48%에서 낙폭 확대)를 확인했으며, 거래량은
이번 회차 volCcy24h×price 방식(≈$50.08M)으로 산출해 직전 회차($58.6M, 산출방식이 달랐을 가능성)
와 직접비교 시 유의가 필요하다.

## 시장 전반

- **⚠️ HL LIT-USD 소실 미스터리 해결 — 실제로는 정상 거래 중, WebFetch truncation 아티팩트로 판단.**
- **1000RATS, '피크아웃' 판단 번복 — 평균+28.86%→+53.26%로 재가속, OI·funding 모두 재과열.**
- **ADA, 강도 더욱 확대 — 7개+ 거래소 동반 강세, OI 거의 두 배 급증($119.89M→$231.38M).**
- **HYPER(HL), 재가속(+17.3%→+20.1%) + funding 더욱 극단적 마이너스(-7.5%→-24.1%) — 스퀴즈 리스크 확대.**
- **GIGGLE, 2회 연속 재확인 실패 끝에 급락(-25.67%) 재확인.**
- **BULLA, 마이너스에서 플러스로 전환(-10.66%→+2.80%).**
- **BANK, 낙폭 완화됐으나 funding은 다시 마이너스 전환 — 방향 새롭게 뒤틀림.**
- **BEAT, 3회 연속 낙폭 확대(-6.77%→-13.89%→-19.27%).**
- **AKE, 랠리 정체 2회 연속, OI 안정화.**
- **CAP, 개선 흐름 지속(-19.45%→-16.58%).**
- **AAVE, 플러스 흐름 지속 강화(+0.356%→+1.19%).**
- **CASHCAT, 낙폭 상당히 완화 — 회복 조짐(-5.86%→-2.62%).**
- **APEX(Bybit·HL), 양쪽 모두 마이너스에서 플러스로 전환.**
- **BLESS, 가격 재가속하나 funding은 완화 — 디커플링 방향 반전.**
- **BTW, 낙폭 더욱 확대(-24.00%→-28.25%).**
- **메이저 리스크온, 방향 유지하되 상승폭 소폭 둔화.**
- **dYdX LIT-USD, 4회 연속 완전 동일 — 정지 재확정(HL LIT은 정상 거래와 대조).**
- **dYdX KAITO-USD, 8회 연속 동일(사망 판정 지속).**
- **GMX, 8회 연속 완전 동일 — 영구 정지 데이터소스 재확정.**
- **ALLO, 재확인 실패 — 값 이월.**
- **신규 급등 스캔: TradFi 토큰화·상품 perp는 규약에 따라 전부 제외.**

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **1000RATS** [피크아웃 판단 번복 — 재가속] | Binance/Bybit(+Aster) | $768.03M | $45.09M | +13.15% | +53.26% | 직전 평균+28.86%에서 +53.26%로 재가속, 2회 전 고점(+60.75%)에 근접. OI $41.05M→$45.09M 증가, funding도 재과열. 반복적 급등락 chop 패턴으로 재해석. OKX 8회 연속 미확인 | reaccelerates-reverses-prior-peak-out-call |
| **BANK (Lorenzo Protocol)** [낙폭 완화·funding 재음전] | Binance/Bybit/Aster | $202.29M | $24.12M | -3.43% | -17.03% | 낙폭 -27.31%→-17.03%로 완화됐으나 funding은 완전 정상화 상태에서 다시 -3.43%로 마이너스 전환 — 방향 새롭게 뒤틀림 | decline-eases-funding-turns-negative-again |
| **BEAT (Audiera)** [3회 연속 낙폭 확대] | OKX/Aster | $272.54M | $11.93M | -2.7% | -19.27% | -6.77%→-13.89%→-19.27%로 3회 연속 낙폭 심화, 8/1 언락발 매도 지속 | post-unlock-decline-deepens-3rd-round |
| **AKE (Akedo)** [랠리 정체 2회 연속] | Binance/Bybit/Aster | $639.49M | $63.21M | -0.33% | +2.99% | +4.15%→+2.99%로 추가 둔화, OI 거의 안정화(디레버리징 진정 국면). 8/21 언락 리스크 유효 | rally-stays-stalled-oi-stabilizes |
| **MMT (Momentum)** [낙폭 재차 확대] | OKX(직접 API) | ~$50.08M(불확실) | $3.29M | -0.08% | -11.84% | -9.48%→-11.84%로 추가 심화. 거래량 산출방식(volCcy24h×price) 변경 가능성 — 직접비교 유의 | decline-deepens-further |
| **CAP** [개선 지속] | OKX/Aster | $53.80M | $2.45M | +0.3% | -16.58% | -19.45%→-16.58%로 추가 개선 | gradual-improvement-continues |
| **AEON** [개선 재개, 커버리지 축소] | OKX(Aster 미확인) | $19.45M | $3.05M | -4.5% | -5.93% | -7.57%→-5.93%로 완화 방향 재개, 이번 회차 OKX 단일 기준 | improvement-resumes-coverage-reduced |
| **ADA** [강도 더욱 확대] | Binance/Bybit/OKX/HL/Aster(+dYdX·XT·Gate) | $355.85M | $231.38M | +0.82% | +9.02% | +7.34%→+9.02%로 확대, 7개+ 거래소 동반 강세. OI $119.89M→$231.38M로 거의 두 배 급증 — 신뢰도 매우 높음 | broad-based-strength-intensifies-7plus-venues |
| **AAVE** [플러스 지속 강화] | Binance/Bybit | $108.37M | $96.69M | -0.35% | +1.19% | +0.356%→+1.19%로 추가 상승, 이번 회차 2거래소 기준(커버리지 변경) | positive-drift-continues-coverage-shifted |
| APR (aPriori) [소폭 감속, 커버리지 변경] | Binance/Bybit | $12.13M | $12.77M | +1.15% | +12.24% | +15.03%→+12.24%로 다소 둔화, 거래소 구성 변경(직접비교 주의) | mild-deceleration-coverage-shifted |
| ALLO [재확인 실패·값 이월] | 미확인 | $28.39M(이월) | $13.16M(이월) | +0.07%(이월) | -4.124%(이월) | Binance/OKX/Bybit/Aster 어디서도 미확인, 다음 회차 재확인 필요 | carried-forward-reverification-failed |
| ASTER [근접 flat] | Binance/Aster | $18.15M | $219.86M | +1.0% | +0.81% | +0.766%→+0.81%로 좁은 범위 지속 | near-flat-continues |
| KAITO [완만한 둔화 지속] | Hyperliquid | $7.84M | $12.60M | +0.1% | +5.39% | +6.397%→+5.39%로 계속 완만히 둔화 | mild-deceleration-continues |
| **APEX** [플러스로 전환] | Bybit | $0.35M | $1.54M | +0.5% | +0.73% | -0.76%→+0.73%로 플러스 전환, HL APEX도 동일 반전 — 양쪽 동반 | confirmed-active-3rd-round-turns-positive |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster; dYdX·GMX 데이터 이슈 지속)

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **⚠️ LIT-USD** [소실 미스터리 해결 — 정상 거래] | Hyperliquid | $8.49M | $77.66M | +0.125% | +2.91% | 통합 스냅샷 재조회로 정상 존재·OI 안정(2회 전 $77.05M과 거의 동일) 확인 — 직전 2회 '사라짐'은 WebFetch truncation 아티팩트로 판단, 델리스팅 아님 | resolved-was-webfetch-truncation-not-delisting |
| **AKE-USDT** [랠리 정체] | Aster | $13.79M | $11.69M | -0.3% | +3.78% | CEX와 함께 랠리 정체 지속, OI 안정화 | rally-stays-stalled-oi-stabilizes |
| **BEAT-USDT** [낙폭 3회 연속 확대] | Aster | $2.15M | $0.35M | -1.0% | -19.33% | OKX와 함께 낙폭 심화 재확인, 언락발 매도 지속 | post-unlock-decline-deepens-3rd-round |
| **BTW** [낙폭 더욱 확대] | Aster | $1.44M | $6.08M | +1.5% | -28.25% | -24.00%→-28.25%로 하락 지속 심화 | decline-deepens-further-again |
| **CASHCAT** [낙폭 완화 — 회복 조짐] | Hyperliquid/Aster | $2.04M | $6.71M | +0.95% | -2.62% | -5.86%→-2.62%로 낙폭 상당히 완화, HL·Aster 양쪽 개선 | decline-eases-recovery-signs |
| KAITO-USD [완만한 둔화 지속] | Hyperliquid | $7.84M | $12.60M | +0.1% | +5.39% | +6.397%→+5.39%로 완만한 둔화 지속 | mild-deceleration-continues |
| **APEX-USD** [플러스로 전환] | Hyperliquid | $0.08M | $0.81M | +0.1% | +0.88% | Bybit와 함께 플러스 전환, 3회 연속 실거래 확인 | confirmed-active-3rd-round-turns-positive |
| **BULLA** [플러스로 전환 — 주요 반전] | Aster | $2.10M | $5.96M | +0.6% | +2.80% | -10.66%→+2.80%로 마이너스에서 플러스로 반전, 사기 의혹 리스크는 유효 | turns-positive-notable-reversal |
| CAP-USDT [개선 지속] | Aster | $0.09M | $0.05M | +0.1% | -17.43% | OKX와 함께 개선 흐름 지속 | gradual-improvement-continues |
| BANK-USDT [낙폭 완화·funding 재음전] | Aster | $0.73M | $0.41M | -1.5% | -16.59% | CEX와 함께 낙폭 완화·funding 재음전 재확인 | decline-eases-funding-turns-negative-again |
| ASTER-USDT [근접 flat] | Aster | $8.32M | $219.86M | +1.0% | +0.77% | CEX 계열과 함께 근접 flat 유지 | near-flat-continues |
| HYPE-USD [리스크온 소폭 둔화] | Hyperliquid | $139.79M | $1,186.90M | +0.1% | +0.48% | +0.816%→+0.48%로 상승폭 다소 둔화, 방향은 유지 | risk-on-continues-mild-deceleration |
| FARTCOIN [대체로 유지] | Hyperliquid | $10.35M | $21.87M | +0.1% | +2.97% | +2.705%→+2.97%로 대체로 유지 | broadly-unchanged |
| **ETH-USD** [리스크온 둔화] | dYdX | $1.26M | $15.18M | 0.0% | +0.34% | +0.627%→+0.34%로 상승폭 축소, 방향 유지 | risk-on-continues-mild-deceleration |
| **BTC-USD** [리스크온 둔화] | dYdX | $4.78M | $17.29M | 0.0% | +0.65% | +0.81%→+0.65%로 상승폭 축소, dYdX 메이저 2종 모두 둔화 | risk-on-continues-mild-deceleration |
| LIT-USD (dYdX) [정지 4회 연속] | dYdX | $99.14 | $14,551.64 | 0.0% | -7.744% | vol·OI·chg 모두 4회 연속 완전 동일 — 정지 재확정. HL LIT은 정상 거래 확인됨과 대조 | confirmed-stale-4th-round-identical |
| KAITO-USD (dYdX) [사망 8회 확정] | dYdX | $488.35 | $0.0 | 미확보 | 0.0% | 8회 연속 완전 동일(OI $0) | confirmed-dead-8th-round-unchanged |
| **ETH/USD (WETH-USDC)** [영구 정지 재확정] | GMX | $23.40M | $16.14M | +0.1% | +2.21% | 8회 연속 완전 동일 — 데이터소스 사실상 영구 정지 | permanently-stale-endpoint-broken-8-rounds |
| **BTC/USD (BTC-USDC)** [영구 정지 재확정] | GMX | $7.52M | $33.60M | +0.2% | +1.23% | 동일하게 8회 연속 완전 동일 — 영구 정지 데이터소스 | permanently-stale-endpoint-broken-8-rounds |
| BLESS-USDT [디커플링 방향 반전] | Aster | $0.60M | $0.20M | +4.7% | +54.91% | 가격 재가속(+40.23%→+54.91%)했으나 funding은 오히려 완화(7.7%→4.7%) — 방향 반전 | price-reaccelerates-funding-eases-decoupling-reverses |
| **HYPER-USD** [재가속 + funding 극단 심화] | Hyperliquid | $0.76M | $0.46M | -24.1% | +20.11% | +17.3%→+20.1% 상승 지속, funding -7.5%→-24.1%로 더욱 극단적 마이너스 — 스퀴즈 리스크 확대, 거래량 여전히 초박막 | reaccelerates-funding-more-extreme-negative |
| **GIGGLE** [재확인 성공 — 급락 확인] | XT.COM/OrangeX | $354.23M | $308.33M | +0.76% | -25.67% | 2회 연속 재확인 실패 끝에 XT.COM(-25.08%)·OrangeX(-26.25%) 양쪽에서 확인, 뚜렷한 급락 재확인 | reverification-succeeds-sharp-decline-confirmed |

## 테마 태그

1. **⚠️ HL LIT-USD 소실 미스터리 해결 — 실제로는 정상 거래 중, WebFetch truncation 아티팩트로 판단** (resolved-was-webfetch-truncation-not-delisting).
2. **1000RATS, '피크아웃' 판단 번복 — 평균+28.86%→+53.26%로 재가속** (reaccelerates-reverses-prior-peak-out-call).
3. **ADA, 강도 더욱 확대 — 7개+ 거래소 동반 강세, OI 거의 두 배 급증** (broad-based-strength-intensifies-7plus-venues).
4. **HYPER(HL), 재가속 + funding 더욱 극단적 마이너스(-24.1%) — 스퀴즈 리스크 확대** (reaccelerates-funding-more-extreme-negative).
5. **GIGGLE, 2회 연속 재확인 실패 끝에 급락(-25.67%) 재확인** (reverification-succeeds-sharp-decline-confirmed).
6. **BULLA, 마이너스에서 플러스로 전환** (turns-positive-notable-reversal).
7. **BANK, 낙폭 완화됐으나 funding은 다시 마이너스 전환** (decline-eases-funding-turns-negative-again).
8. **BEAT, 3회 연속 낙폭 확대** (post-unlock-decline-deepens-3rd-round).
9. **AKE, 랠리 정체 2회 연속, OI 안정화** (rally-stays-stalled-oi-stabilizes).
10. **CAP, 개선 흐름 지속** (gradual-improvement-continues).
11. **AAVE, 플러스 흐름 지속 강화** (positive-drift-continues-coverage-shifted).
12. **CASHCAT, 낙폭 상당히 완화 — 회복 조짐** (decline-eases-recovery-signs).
13. **APEX(Bybit·HL), 양쪽 모두 플러스로 전환** (confirmed-active-3rd-round-turns-positive).
14. **BLESS, 가격 재가속·funding 완화 — 디커플링 방향 반전** (price-reaccelerates-funding-eases-decoupling-reverses).
15. **BTW, 낙폭 더욱 확대** (decline-deepens-further-again).
16. **메이저 리스크온, 방향 유지하되 상승폭 소폭 둔화** (risk-on-continues-mild-deceleration).
17. **dYdX LIT-USD, 4회 연속 완전 동일 — 정지 재확정** (confirmed-stale-4th-round-identical).
18. **dYdX KAITO-USD, 8회 연속 동일(사망 판정 지속)** (confirmed-dead-8th-round-unchanged).
19. **GMX, 8회 연속 완전 동일 — 영구 정지 데이터소스 재확정** (permanently-stale-endpoint-broken-8-rounds).
20. **ALLO, 재확인 실패 — 값 이월** (carried-forward-reverification-failed).
21. **신규 급등 스캔: TradFi 토큰화·상품 perp 전부 제외** (excluded-tokenized-stock-etf-leveraged).

## 데이터 신뢰도

**최우선 항목 HL LIT-USD 미스터리를 해결했다.** 이번 회차 거래소 전용 엔드포인트
(`/derivatives/exchanges/hyperliquid`) 대신 CoinGecko 통합 파생 스냅샷
(`/derivatives?include_tickers=unexpired`)을 사용해 LIT-USD를 재조회한 결과, OI $77,664,083.26·
거래량 $8,487,517.08로 정상 거래 중임을 확인했다. 2회 전 값(OI $77.05M)과 거의 동일한 수준이라
실제로는 아무 일도 없었던 것으로 보이며, 직전 2회 회차의 '데이터셋 완전 소실'은 거래소 전용
엔드포인트가 반환하는 방대한 티커 목록(수백 개)을 WebFetch가 요약하는 과정에서 특정 항목이
누락됐을 가능성이 높다 — **향후 특정 종목이 거래소별 엔드포인트에서 안 보이면, 통합 스냅샷
엔드포인트로 교차검증하는 절차를 표준화할 필요가 있다.**

**1000RATS는 Binance·Bybit 2개 거래소에서 독립적으로 재가속을 확인**했다(각각 +55.223%·
+51.291%). 직전 회차의 '피크아웃' 판단이 이번 회차 완전히 뒤집혀, 이 종목은 방향성 예측이 어려운
극심한 변동성(chop) 국면으로 재평가하는 것이 타당하다. OKX 티커는 8회 연속 미확인으로 3거래소
교차검증은 여전히 불완전하다.

**ADA는 이번 회차 7개 이상 거래소(Binance/Bybit/OKX×2/HL/Aster/XT.COM/Gate)에서 독립적으로
+8.7%~+9.3% 범위의 일관된 강세를 확인**해 신뢰도가 매우 높다. OI가 거의 두 배로 급증한 점도
포지션 유입이 광범위함을 뒷받침한다.

**MMT는 이번 회차도 OKX 퍼블릭 API(ticker+funding-rate+open-interest 개별 엔드포인트)로 직접
조회**했다. OI는 oiUsd 필드로 정확히 확보($3,285,202.41)됐으나, 거래량은 이번 회차
volCcy24h(283,921,140)×last price(0.1764)≈$50.08M 방식으로 산출했다 — 직전 회차($58.6M)와
산출 방법론이 완전히 동일했는지 확신할 수 없어 절대치 비교보다는 방향성(둘 다 대체로 유사한 규모의
거래량) 참고로만 활용해야 한다. chg24는 (last-open24)/open24로 직접 계산해 -11.84%를 확보했다.

**GIGGLE은 2회 연속 재확인 실패 후 이번 회차 XT.COM·OrangeX 양쪽에서 성공적으로 재확인**됐다
(-25.08%·-26.25%, 평균-25.67%). 이전에 이월했던 값(+0.14%)은 신뢰할 수 없는 오래된 스냅샷이었던
것으로 판명돼 폐기한다.

**dYdX LIT-USD는 4회 연속(직전 3회+이번) 소수점까지 완전 동일한 수치**를 유지해 정지 상태를
재확정했다. HL LIT-USD가 정상 거래 중임을 확인한 것과 대조적으로, dYdX 쪽은 실제로 유동성이
고갈된 것으로 보인다. **GMX 데이터소스는 8회 연속 완전 동일**해 사실상 영구 정지 상태로 재확정,
향후 회차에서도 참고 기록으로만 유지한다.

**ALLO는 이번 회차 Binance/OKX/Bybit/Aster 통합 스캔에서도 확인되지 않아** 직전 회차 값을
이월했다 — 다음 회차 재확인이 필요하다. **AEON은 이번 회차 Aster 데이터가 확보되지 않아** OKX
단일 거래소 기준으로 커버리지가 축소됐다.

한계: (a) DefiLlama `/overview/derivatives`는 이번 회차도 시도하지 않음(과거 402 확인 이력);
(b) 1000RATS의 OKX 티커는 이번 회차도 확인되지 않음(8회 연속); (c) APR·ALLO·AAVE·AEON은 이번
회차 일부 거래소 데이터가 미확보돼 부분 거래소 기준으로 계산 — 직전 회차 대비 직접 비교 시 커버리지
차이에 유의; (d) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서만 수행했으며
전체 시장을 포괄하는 완전한 스캔은 아니다; (e) **주식화·상품·레버리지ETF 토큰**은 이번 회차도
규약에 따라 cex/dex 리스트에서 전부 제외.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
