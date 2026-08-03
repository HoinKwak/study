# 선물시장 스카우트 브리핑 — 2026-08-03 08:29 UTC (KST 2026-08-03 17:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·GMX·dYdX) 선물시장에서 지금 주목받는
> **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·상품·
> 프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-03T06:28:00Z)
> 로부터 약 2시간 경과.**

이번 회차는 CoinGecko `/global`이 다시 성공해 총 시총 **$2.226T**(-1.13% 24h), BTC 도미넌스
**56.16%**, ETH 도미넌스 **9.93%**를 확보했다 — 직전 회차($2.24T, -0.93%, 56.19%, 9.997%)보다
낙폭이 소폭 더 커져 시장 전반이 조금 더 눌리는 모습이다. OKX BTC-USDT-SWAP 직접 조회로 BTC
**-1.56%**(직전 -0.995%)를 확인했고, HYNA:BTC-USD 인덱스가격($62,589)과도 정합해 -1.5%대
완만한 약세가 재확인된다.

## ⚠️ 이번 회차 핵심: OKX funding rate 스케일 오류 발견·정정

BICO·AEON·BEAT·CAP의 funding을 OKX 퍼블릭 API(`/api/v5/public/funding-rate`)로 직접
교차검증한 결과, 실제 값은 각각 **-0.008%·-0.077%·+0.002%·+0.007%**로 — 이전 회차들이
CoinGecko derivatives 스윕에서 보고해온 자릿수(예: BICO -16.1%, AEON -4.1%)와 크게 어긋났다.
MMT는 애초부터 OKX 직접 API로만 조회해왔기에 이 문제에서 자유로웠던 것으로 보인다(과거 기록과
값 일관). 가격(24h 변동률) 데이터는 CoinGecko와 직접 API가 대체로 일치해 신뢰할 만했다.
**정직하게 밝히면, 과거 여러 회차에 걸쳐 보고한 BICO·AEON·BEAT·CAP의 극단적 OKX funding
수치는 실제보다 부풀려졌을 가능성이 있다** — 이번 회차부터 OKX 심볼은 직접 API 교차검증값을
우선 사용한다.

## 이번 회차 요약

①**BICO는 funding이 사실상 완전히 flat(-0.008%)로 수렴**했다(가격은 +31.37%→**+22.12%**로
둔화) — 극단 숏스퀴즈가 완전히 해소된 것으로 보인다.

②**AEON도 가격-funding 괴리가 해소**됐다(가격 -3.25%→**-1.0%**, funding 실측 -0.077%로
flat) — 지난 회차 지적한 '괴리'는 스케일 오차였을 가능성이 높다.

③**BEAT는 극적으로 재반전**했다 — 직전 회차 '언락 충격 완전 소화·반등'(+3.23%)으로 판단했던
것이 이번엔 OKX -23.04%(직접 API 계산)·Aster -19.98%(평균 **-21.51%**)로 다시 급락했다.
뉴스 검색 결과 BEAT는 최근 1주 -88% 붕괴 논란·펌프덤프 우려가 실제 보도된 초고변동성 종목으로
확인돼, 이 급반전은 데이터 오류가 아니라 실제 시장 특성으로 판단된다.

④**BANK도 유사하게 회복이 완전히 반전**됐다 — 이번 회차 3거래소(Binance/Bybit/Aster) 모두
재확인한 결과 -7.77%→**-11.79%**로 재급락, funding도 -1.15%→**-0.77%**로 재악화했다.

⑤**1000RATS는 낙폭이 다소 완화**됐다(-15.36%→**-4.68%**, 여전히 마이너스, funding
5.65%→4.35%) — 3회 연속 방향이 뒤집히는 고변동 라운드트립 패턴은 지속.

⑥**AKE는 계속 플러스를 유지하며 추가 둔화**됐다(+11.69%→**+8.60%**, funding 1.63%→0.93%) —
8/21 언락 임박, 여러 회차 연속 건전한 냉각 흐름.

⑦**KAITO(HL)는 여러 회차 이어진 악화가 처음 진정**됐다(-18.80%→**-14.65%**, funding
1.1%→0.6%).

⑧**CAP은 하락폭이 더 확대**됐다(-10.52%→**-13.62%**, funding은 직접검증 결과 사실상 flat).

⑨**ADA·AAVE는 이번 회차 Binance만 재확인**됐다(Bybit·OKX 상위목록 미노출) — ADA -0.79%→
**-1.78%**로 하락 심화, AAVE -0.20%→**-0.58%**로 소폭 더 마이너스. 부분데이터임에 유의.

DEX에서는 ⑩**BULLA가 처음으로 플러스 전환**됐다(-4.84%→**+5.57%**), BTW도 계속 확장
(+4.94%→**+9.70%**)해 두 종목이 함께 플러스로 수렴 — 지난 회차 '역할 반전 고착' 판단과 달리
이번엔 둘 다 상승 전환했다.

⑪**CASHCAT은 재가속**했다(+9.02%→**+11.74%**, funding도 상승) — 로빈후드 촉매 모멘텀
재점화 가능성.

⑫**BLESS-USDT(Aster)는 조정이 계속**되며 점진 냉각 중이다(+42.56%→**+32.63%**, funding
4.1%→2.8%).

⑬**LIT-USD/HYNA:LIGHTER-USD는 6회 연속 완전 동결**이 재확인됐다. 이번 회차 exhaustive
검색으로 Hyperliquid에 별도의 'LIT-USD'(비-HYNA 접두사) 계약이 실제로는 존재하지 않음을
확인해 과거 라벨링을 정정한다. HYNA:HYPE-USD는 OI($682,965.88)는 동일하나 거래량·가격은
소폭 갱신돼 완전 동결은 아니었다.

⑭**신규 발견: AIO(OlaXBT)가 Binance -32.39%·Bybit -31.64%(평균 -32.0%)로 두 거래소 동시
급락**했다 — 정확한 촉매(일부 거래소 상장폐지설 있으나 Binance·Bybit 공식 발표는 확인 못함)는
정직하게 미확인으로 표기한다.

**⚠️ 데이터 이슈**: (a) dYdX는 이번 회차도 전체 조회 실패(2회 연속) — 정확한 exchange id가
`dydx-chain`(하이픈)임을 웹서치로 확인했으나 CoinGecko 요율제한(503)으로 재조회는 못함, 다음
회차 이 id로 재시도 예정, LIT/KAITO(dYdX) 동결 스트릭 카운트는 계속 미확인; (b) GMX·OrangeX
(BLESS-USDT-PERPETUAL)·XT.COM(GIGGLE)은 7회 연속 재조회 실패(503) 지속, 직전 값 이월; (c) MMT의
OI는 CoinGecko 데이터셋에 MMT 항목 자체가 없어(과거부터 동일) 재조회 못해 이월; (d) ADA·AAVE는
Binance만 확보한 부분데이터임을 명시(과거 3거래소 평균과 직접 비교 시 유의); (e) Binance/Bybit
/Aster의 raw funding_rate는 기존 관행대로 ×100 정규화를 유지했으나, OKX 소스는 이번 회차부터
직접 API 값을 우선 사용 — 데이터 소스가 섞여 있어 향후 회차도 이 방식을 유지할 필요.

## 시장 전반

- **총 시총 $2.226T(-1.13% 24h), BTC 도미넌스 56.16%, ETH 도미넌스 9.93% — 직전보다 낙폭 소폭 확대. OKX BTC 직접조회 -1.56%로 완만한 약세 재확인.**
- **⚠️ OKX funding rate 스케일 오류 발견·정정 — BICO·AEON·BEAT·CAP 직접 API 교차검증 결과 과거 극단 수치는 부풀려졌을 가능성.**
- **BEAT·BANK, 회복 국면이 이번 회차 완전히 재반전 — 극단 변동성 지속(BEAT는 최근 -88% 붕괴·펌프덤프 논란 실제 보도 확인).**
- **BULLA, 첫 플러스 전환 — BTW와 함께 둘 다 상승 국면으로 수렴.**
- **dYdX 정확한 exchange id 'dydx-chain' 확인했으나 요율제한으로 재조회 실패(2회 연속) — 다음 회차 재시도.**
- **신규: AIO(OlaXBT), 두 거래소 동시 -32% 급락, 촉매 미확인.**

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BEAT (Audiera)** [플러스→마이너스 극적 재반전] | OKX(직접API)/Aster | $255.36M | $10.11M | +0.05% | -21.51% | 직전 +3.23%('언락 완전 소화')가 이번엔 OKX -23.04%·Aster -19.98%로 재급락. 뉴스로 -88% 붕괴·펌프덤프 논란 확인 — 실제 초고변동성 | positive-reverses-hard-extreme-volatility-pump-dump-concerns |
| **BANK (Lorenzo Protocol)** [회복 완전 반전] | Binance/Bybit/Aster | $183.32M | $23.20M | -0.77% | -11.79% | -7.77%→-11.79%로 재급락, funding도 -1.15%→-0.77%로 재악화 — flip-flop 패턴 | recovery-reverses-drops-again |
| **BICO (Biconomy)** [funding 완전 정상화] | OKX(직접API 교차검증) | $48.65M | $1.63M | -0.008% | +22.12% | 가격 +31.37%→+22.12%로 둔화, funding은 직접 API 결과 -16.1%→-0.008%로 사실상 완전 flat — 극단 숏스퀴즈 해소 | funding-fully-normalized-price-decelerates-scale-correction-applied |
| **AEON** [가격-funding 괴리 해소] | OKX(직접API 교차검증) | $15.05M | $2.87M | -0.077% | -0.998% | 가격 -3.25%→-1.0%, funding -4.1%→-0.077%로 사실상 flat — 지난 회차 괴리는 스케일 오차 가능성(정직 정정) | divergence-resolves-scale-correction-both-converge-flat |
| CAP [하락폭 추가 확대] | OKX(직접API)/Aster | $28.82M | $1.85M | +0.05% | -13.62% | -10.52%→-13.62%로 하락세 심화 | negative-reversal-deepens-further |
| 1000RATS [낙폭 완화, 여전히 마이너스] | Binance/Bybit | $636.75M | $40.06M | +4.35% | -4.68% | -15.36%→-4.68%로 축소, 3회 연속 방향 전환 라운드트립 지속(신호 낮음) | round-trip-continues-narrows-still-negative |
| AKE (Akedo) [플러스 유지, 추가 둔화] | Binance/Bybit/Aster | $342.23M | $65.32M | +0.93% | +8.60% | +11.69%→+8.60%, funding도 1.63%→0.93% 정상화. 8/21 언락 임박 | positive-continues-decelerating-further-funding-normalizes-further |
| **KAITO** [여러 회차 만에 첫 개선] | Hyperliquid(주) | $27.95M | $27.24M | +0.60% | -14.65% | -18.80%→-14.65%로 하락세 진정, funding 1.1%→0.6% | decline-moderates-first-improvement |
| ADA [Binance만 확인, 부분데이터] | Binance(확인) | $205.22M | $109.20M | +1.00% | -1.78% | -0.79%→-1.78%로 하락 심화(Bybit/OKX 미확인) | negative-continues-partial-data-binance-only |
| AAVE [Binance만 확인, 부분데이터] | Binance(확인) | $54.34M | $48.70M | +0.30% | -0.58% | -0.20%→-0.58%로 소폭 더 마이너스(Bybit/OKX 미확인) | near-flat-continues-partial-data-binance-only |
| MMT (Momentum) [박스권 지속] | OKX(직접조회) | $123.96M | $3.16M(이월) | -0.11% | -12.57% | -13.83%→-12.57%로 거의 동일, -12~-14% 박스권 | range-bound-continues |
| ASTER (CEX) [이월 해제, 근접 flat] | Binance/Bybit/OKX/Aster | $19.54M | $341.56M | +0.88% | -0.60% | 요율제한 이월이 해제, 4거래소 재확인해도 여전히 거의 flat | fresh-update-near-flat-continues |
| **AIO (OlaXBT)** [신규 급락 포착] | Binance/Bybit | $39.00M | $4.09M | +0.50% | -32.02% | Binance -32.39%·Bybit -31.64%로 동시 급락, 정확한 촉매는 미확인(일부 거래소 상장폐지설 있으나 공식 발표는 미확인) | new-sharp-decline-catalyst-unconfirmed |
| ALLO (Allora) [이월 해제, 플러스 전환] | Binance/Bybit | $19.76M | $17.33M | +0.50% | +1.24% | -6.15%→+1.24%로 플러스 전환(신선 갱신) | carry-forward-resolved-turns-positive |
| APR (aPriori) [부분 이월 해제] | Bybit(부분) | $0.63M | $1.59M | +0.50% | -3.50% | -9.82%→-3.50%로 낙폭 완화(Bybit만 재확인) | partial-carry-forward-resolved-improves |
| APEX [Bybit분 이월, HL분 신선] | Hyperliquid/Bybit | $0.04M | $0.80M | -0.20% | +0.73% | Bybit 상위목록 미확인 지속. HL 단독분은 거의 flat — DEX 표 참조 | bybit-portion-still-carried-forward-hl-fresh |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·OrangeX·dYdX·GMX·XT.COM)

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BULLA** [첫 플러스 전환] | Aster | $1.75M | $6.99M | +1.4% | +5.57% | -4.84%→+5.57%로 처음 양전, BTW와 함께 둘 다 플러스로 수렴 — 역할 반전 국면 종료 | turns-positive-first-time-converges-with-btw |
| **BTW** [플러스 확장 지속] | Aster | $0.69M | $6.48M | +1.1% | +9.70% | +4.94%→+9.70%로 확장 지속 | positive-extends-further-converges-with-bulla |
| **CASHCAT** [재가속] | Hyperliquid/Aster | $2.43M | $8.49M | +1.95% | +11.74% | +9.02%→+11.74%(HL+12.40%·Aster+11.09%)로 재가속 — 로빈후드 촉매 재점화 가능성 | reaccelerates-again |
| **BLESS-USDT** [조정 지속, 점진 냉각] | Aster | $2.68M | $0.37M | +2.8% | +32.63% | +42.56%→+32.63%로 되돌림 계속, funding도 완화 | pullback-continues-gradual-cooling |
| **⚠️ BLESS-USDT-PERPETUAL** [7회 연속 실패] | OrangeX | $353.98M(이월) | $150.80M(이월) | +2.62%(이월) | +69.45%(이월) | id 'orangex' 503/429 지속, 직전 값 이월. 4월 내부자 대량매도 70% 폭락 전력 유의 | carried-forward-endpoint-error-7th-round |
| **LIT-USD / HYNA:LIGHTER-USD** [6회 연속 완전 동결, 라벨 정정] | Hyperliquid | $461.35 | $0.0 | 0.0% | 0.0% | exhaustive 검색으로 재확인. 별도 'LIT-USD'(비-HYNA) 계약 부재 확인 — 과거 라벨링 정정. HYNA:HYPE-USD는 OI 동일하나 소폭 변동 | frozen-6th-round-label-corrected |
| HYPE-USD [플러스 유지, 거의 완전 flat] | Hyperliquid | $177.03M | $1,191.86M | +0.1% | +0.03% | +0.73%→+0.03%로 사실상 flat 수렴 | near-flat-continues |
| HYPER-USD [디버전스 유사 수준 지속] | Hyperliquid | $1.51M | $0.39M | -3.2% | -7.29% | 가격 -8.00%→-7.29%, funding -2.9%→-3.2%로 유사 범위 유지 — 초박막 지속 | divergence-persists-similar-range |
| KAITO-USD [낙폭 완화 재확인] | Hyperliquid | $27.95M | $27.24M | +0.6% | -14.65% | CEX 행과 동일 데이터 재확인 | decline-moderates-first-improvement |
| AKE-USDT [둔화 재확인] | Aster | $2.95M | $12.48M | +0.2% | +9.29% | CEX와 함께 플러스 유지·둔화 재확인 | positive-continues-decelerating-further-funding-normalizes-further |
| BEAT-USDT [극적 재반전 재확인] | Aster | $1.64M | $0.28M | +0.1% | -19.98% | OKX와 함께 플러스→마이너스 극적 재반전 재확인 | positive-reverses-hard-extreme-volatility-pump-dump-concerns |
| BANK-USDT [완전 반전 재확인] | Aster | $0.58M | $0.34M | -1.5% | -11.96% | CEX와 함께 회복 완전 반전 재확인 | recovery-reverses-drops-again |
| CAP-USDT [확대 재확인] | Aster | $0.02M | $0.03M | +0.1% | -12.51% | OKX와 함께 하락폭 확대 재확인 | negative-reversal-deepens-further |
| ASTER-USDT [근접 flat 재확인] | Aster | $6.58M | $219.17M | +2.0% | -0.53% | CEX 통합과 함께 근접 flat 재확인, OI $219.2M 큰 규모 유지 | fresh-update-near-flat-continues |
| APEX-USD [사실상 flat 지속] | Hyperliquid | $0.04M | $0.80M | -0.2% | +0.73% | +0.06%→+0.73%로 여전히 flat 근접 | essentially-flat-continues |
| FARTCOIN [마이너스 소폭 심화] | Hyperliquid | $5.14M | $19.58M | +0.1% | -3.12% | -2.68%→-3.12%로 유사 수준 유지 | negative-continues-near-unchanged |
| ADA-USD [마이너스 심화, CEX와 동일 방향] | Hyperliquid | $9.62M | $30.22M | +0.1% | -2.08% | -0.56%→-2.08%로 CEX ADA(Binance -1.78%)와 같은 방향 | negative-deepens-matches-cex |
| AAVE-USD [소폭 더 마이너스, CEX와 유사] | Hyperliquid | $5.20M | $65.48M | +0.1% | -0.75% | -0.16%→-0.75%로 CEX AAVE와 유사한 흐름 | near-flat-continues-matches-cex |
| ETH-USD [이월, 2회 연속 실패] | dYdX | $2.74M | $15.10M | -0.2% | -1.17% | 정확한 id 'dydx-chain' 확인했으나 요율제한(503)으로 재조회 실패 — 다음 회차 재시도 | carried-forward-dydx-unreachable-2nd-round-correct-id-found |
| BTC-USD [이월, 2회 연속 실패] | dYdX | $3.18M | $17.01M | 0.0% | -1.01% | 위와 동일 | carried-forward-dydx-unreachable-2nd-round-correct-id-found |
| LIT-USD (dYdX) [이월, 스트릭 미확인] | dYdX | $90.92 | $14,551.64 | 0.0% | -1.59% | dYdX 전체 실패로 동결 스트릭 카운트 계속 미확인 | carried-forward-dydx-unreachable-streak-unconfirmed |
| KAITO-USD (dYdX) [이월, 스트릭 미확인] | dYdX | $488.35 | $0.0 | 0.0% | 0.0% | dYdX 전체 실패로 동결 스트릭 카운트 계속 미확인 | carried-forward-dydx-unreachable-streak-unconfirmed |
| ETH/USD (WETH-USDC) [7회 연속 실패] | GMX | $23.40M(이월) | $16.14M(이월) | +0.1%(이월) | +2.21%(이월) | id 'gmx' 503 지속, 직전 값 이월 | endpoint-failed-carried-forward-7th-round |
| BTC/USD (BTC-USDC) [7회 연속 실패] | GMX | $7.52M(이월) | $33.60M(이월) | +0.2%(이월) | +1.23%(이월) | ETH/USD와 동일하게 7회 연속 실패, 직전 값 이월 | endpoint-failed-carried-forward-7th-round |
| GIGGLE (Giggle Fund) [7회 연속 실패] | XT.COM | $34.11M(이월) | $224.34M(이월) | +0.5%(이월) | +6.12%(이월) | 503/429 지속, 직전 값 이월 | perp-endpoint-failed-carried-forward-7th-round |

## 테마 태그

1. **⚠️ 데이터 품질 정정: OKX funding rate 스케일 오류 발견·교정 — BICO·AEON·BEAT·CAP 직접 API 교차검증 결과 과거 극단 수치는 부풀려졌을 가능성** (data-quality-correction-okx-funding-scale).
2. **BEAT, 극적 재반전 — 언락 완전 회복 판단이 이번엔 -21.51%로 재급락. 실제 -88% 붕괴·펌프덤프 논란 보도 확인** (positive-reverses-hard-extreme-volatility-pump-dump-concerns).
3. **BANK, 회복 완전 반전 — 3거래소 재확인 결과 -11.79%로 재급락** (recovery-reverses-drops-again).
4. **BICO, funding 완전 flat 수렴, 가격 상승폭 둔화** (funding-fully-normalized-price-decelerates-scale-correction-applied).
5. **AEON, 가격-funding 괴리 해소 — 스케일 오차 가능성** (divergence-resolves-scale-correction-both-converge-flat).
6. **1000RATS, 낙폭 완화하나 여전히 마이너스 — 라운드트립 지속** (round-trip-continues-narrows-still-negative).
7. **AKE, 플러스 유지 추가 둔화, funding도 정상화** (positive-continues-decelerating-further-funding-normalizes-further).
8. **KAITO(HL), 여러 회차 만에 첫 개선** (decline-moderates-first-improvement).
9. **CAP, 하락폭 추가 확대** (negative-reversal-deepens-further).
10. **ADA·AAVE, Binance만 부분 재확인** (partial-data-binance-only-ada-aave).
11. **BULLA, 첫 플러스 전환 — BTW와 함께 수렴** (turns-positive-first-time-converges-with-btw).
12. **CASHCAT, 재가속** (reaccelerates-again).
13. **BLESS-USDT(Aster), 조정 지속·점진 냉각** (pullback-continues-gradual-cooling).
14. **LIT-USD/HYNA:LIGHTER-USD, 6회 연속 완전 동결 — 라벨링 정정** (frozen-6th-round-label-corrected).
15. **신규: AIO(OlaXBT), 두 거래소 동시 -32% 급락 — 촉매 미확인** (new-sharp-decline-catalyst-unconfirmed).
16. **ALLO, 이월 해제되며 플러스 전환** (carry-forward-resolved-turns-positive).
17. **ASTER(CEX), 이월 해제 — 근접 flat 지속** (fresh-update-near-flat-continues).
18. **dYdX, 이번 회차도 전체 실패(2회 연속) — 정확한 id 'dydx-chain' 확인, 다음 회차 재시도** (dydx-unreachable-2nd-round-correct-id-found).
19. **GMX·OrangeX·XT.COM, 7회 연속 재조회 실패 지속** (three-sources-7th-consecutive-failure).
20. **시장 전반: 총 시총 $2.226T(-1.13%), BTC 도미넌스 56.16% — 낙폭 소폭 확대** (market-slightly-softer-btc-minus1-56pct).
21. **신규 급등 스캔: 토큰화 주식·상품 perp(CL/원유, CRCL/Circle주식 등 OKX 목록에서 발견)는 규약에 따라 전부 제외 확인** (excluded-tokenized-stock-etf-commodity-cl-crcl-found-excluded).

## 데이터 신뢰도

**이번 회차의 가장 중요한 작업은 OKX 소스 funding rate 스케일 오류를 발견하고 정정한 것이다.**
BICO·AEON·BEAT·CAP의 funding을 OKX 퍼블릭 API(`/api/v5/public/funding-rate`,
`/api/v5/market/ticker`)로 직접 교차검증한 결과, 실제 값은 각각 -0.008%·-0.077%·+0.002%·
+0.007%로 극히 작은 수준이었다 — 반면 이전 여러 회차가 CoinGecko derivatives 스윕 데이터를
바탕으로 보고해온 값(BICO -16.1%, AEON -4.1% 등)은 이보다 수백 배 큰 자릿수였다. MMT는 처음부터
OKX 직접 API로만 조회해왔기에 이 문제와 무관했던 것으로 보이며(과거 기록의 스케일이 이번 직접
검증치와 일관), 이는 문제가 CoinGecko의 OKX derivatives 스윕 특유의 이슈였을 가능성을 시사한다.
가격(24h 변동률) 데이터는 CoinGecko 값과 직접 API 값이 대체로 일치해 신뢰할 만했다. **정직하게
밝히면, 과거 여러 회차에 걸쳐 이 브리핑이 보고한 BICO·AEON·BEAT·CAP의 극단적 OKX funding
수치는 실제보다 부풀려졌을 가능성이 있다.** 이번 회차부터는 OKX 심볼의 funding을 직접 API로
우선 확보하는 방식으로 전환한다.

**BEAT는 극적인 재반전을 보였다.** 직전 회차 "8/1 언락 충격 완전 소화, 반등 국면 진입"으로
판단했던 것이 이번엔 OKX -23.04%(직접 API로 계산)·Aster -19.98%로 급락해 평균 -21.51%를
기록했다. 뉴스 검색으로 BEAT가 최근 1주간 실제로 -88% 붕괴 논란과 펌프덤프 우려가 보도된
극심한 변동성 종목임을 확인했으므로, 이번 재반전은 데이터 수집 오류가 아니라 실제 시장
특성(초고변동성)으로 판단하는 것이 합리적이다. BANK도 유사하게 3거래소 모두에서 회복이
재반전됨을 확인했다.

**dYdX는 이번 회차도 전체 조회에 실패**했으나, 웹서치를 통해 정확한 CoinGecko exchange id가
`dydx-chain`(하이픈 포함, 과거 시도했던 `dydx_chain`·`dydx_v4`는 모두 잘못된 id)임을 확인했다.
다만 이 올바른 id로도 CoinGecko 요율제한(503)에 걸려 이번 회차 데이터는 확보하지 못했다 —
다음 회차 이 id로 우선 재시도할 필요가 있다. ETH-USD·BTC-USD·LIT-USD·KAITO-USD(dYdX) 4개
행 모두 이월했고, LIT/KAITO의 동결 스트릭 카운트는 계속 확인하지 못하고 있다.

**GMX·OrangeX(BLESS-USDT-PERPETUAL)·XT.COM(GIGGLE)은 7회 연속 재조회 실패**가 이어졌다 —
이번 회차는 모두 503(서비스 불가) 응답으로, 이전 회차들의 429(요율제한)와는 다른 오류 패턴을
보였으나 여전히 데이터 확보에는 실패했다.

**LIT-USD/HYNA:LIGHTER-USD 관련해 라벨링 오류를 정정했다.** exhaustive 검색으로 Hyperliquid
전체 티커에서 "LIT" 또는 "HYNA"를 포함하는 모든 심볼을 재확인한 결과, 별도의 'LIT-USD'
(HYNA 접두사 없는) 계약은 실제로 존재하지 않았다 — 과거 회차의 "LIT-USD / HYNA:LIGHTER-USD"
라벨은 사실상 HYNA:LIGHTER-USD 하나만을 가리켰던 것으로 보인다. 이 계약은 이번에도 소수점까지
완전히 동일한 값(vol $461.35·OI $0·funding 0%·chg 0%)을 유지해 6회 연속 동결이 재확인됐다.

**ADA·AAVE는 이번 회차 Binance 단독 데이터**로 보고했다. Bybit·OKX의 상위 거래량 목록에서
두 종목이 확인되지 않아(요청 범위 내 truncation 가능성) 재조회하지 못했다 — 과거 3거래소
평균값과 직접 비교하지 말 것을 권고한다.

**신규 발견 AIO(OlaXBT)는 Binance·Bybit 양쪽에서 동시에 -32%대 급락**했다. 웹서치로 정확한
촉매를 찾으려 했으나 Binance·Bybit 공식 상장폐지 발표는 확인하지 못했고, 다른 거래소(MGBX)의
2025년 12월 상장폐지 소식만 확인돼 이번 급락의 직접적 원인과는 무관해 보인다 — 정직하게
'촉매 미확인'으로 표기한다.

한계: (a) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서만 수행했으며
전체 시장을 포괄하는 완전한 스캔은 아니다; (b) dYdX는 이번 회차도 전체 조회 실패(2회 연속) —
올바른 id는 확인했으나 요율제한으로 재조회하지 못함; (c) GMX·OrangeX·XT.COM은 7회 연속 데이터
확보 실패로 직전 값을 이월했다; (d) **주식화·상품·레버리지 ETF 토큰**은 이번 회차도 규약에 따라
cex/dex 리스트에서 전부 제외했다(OKX 목록에서 CL[원유]·CRCL[Circle 주식] 발견해 제외 확인);
(e) OKX 소스는 이번 회차부터 직접 API 교차검증값을 우선 사용하는 것으로 방식을 전환했다 —
Binance/Bybit/Aster는 기존 관행(raw funding_rate ×100)을 유지했다; (f) ADA·AAVE는 Binance
단독 부분데이터임을 명시했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
