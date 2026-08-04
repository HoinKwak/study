# 선물시장 스카우트 브리핑 — 2026-08-04 06:58 UTC (KST 2026-08-04 15:58)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-04T04:58:00Z)
> 로부터 약 2시간 경과.**

CoinGecko `/global`로 총 시총 **$2.2657T**(24h **+1.40%**), BTC 도미넌스 **56.41%**, ETH 도미넌스
**9.91%**를 확보했다 — 직전 회차($2.269T, +1.28%, 56.43%/9.92%)와 비교해 명목 시총은 소폭 줄었으나
(측정 기준시점 이동에 따른 노이즈로 추정) **24h 변동률은 +1.28%→+1.40%로 반등이 계속 가속**됐고,
BTC 도미넌스는 56.43%→56.41%로 소폭 하락해 알트 상대강세를 시사한다.

## ⚠️ 이번 회차 신규 발견 — 토큰화 주식 퍼프 대량 확인, 전부 제외

Binance·OKX 스캔에서 **AAOI(Applied Optoelectronics)·AXTI(AXT Inc)·AEHR(Aehr Test Systems)·
ASTS(AST SpaceMobile)·BABA(Alibaba)·COHR(Coherent)·CRWV(CoreWeave)·APLD(Applied Digital)·
BX(Blackstone)** 등 반도체·우주·AI인프라 테마의 실제 상장주식을 토큰화한 퍼프 묶음이 대거 신규
확인됐다. **CBRS**는 종목 식별이 불확실해 안전하게 제외했다. 규약(크립토 네이티브만)에 따라
**전부 리스트에서 제외**했으며, CL-USDT(WTI 원유 토큰화)도 재확인돼 계속 제외 상태다.

## ⚠️ 이번 회차 데이터 소스 이상 (지속·악화)

`orangex`는 **7회 연속**, `dydx_v4`는 **7회 연속**, `gmx`는 **8회 연속**, `xt_derivatives`는
**8회 연속** 조회에 실패했다. DefiLlama derivatives 개요 API도 이번 회차 402(Payment Required)로
실패해 참고하지 못했다. 구조적 이슈로 계속 굳어지고 있으며, 이월값을 아래 표에 명시 표기했다.

## 이번 회차 핵심

**1000RATS는 완전한 크래시 이후 부분 반등**했다 — Binance -23.88%·Bybit -22.30%·Aster -22.86%
(평균 **-23.01%**, 직전 -27.70%)로 낙폭이 다소 줄었으나 여전히 깊은 하락권이며, 개별 촉매는 이번
회차도 웹서치로 확인하지 못했다.

**⚠️ BICO는 4회 연속 상승 흐름으로 굳어졌다** — OKX 직접 조회(last 0.01723/open24h 0.01544) 기준
**+11.59%**(CG okex_swap +11.18%와 근접, 평균 +11.4%, 직전 +8.34%)로 스퀴즈→되돌림의 왕복
(whipsaw) 패턴을 넘어 방향성 있는 지속 상승 국면으로 전환된 것으로 보인다 — 웹서치로 ERC-8211
표준·AI블록체인 내러티브(6월 검색결과, 최신성 불확실)가 배경으로 언급되나 최근 촉매는 미확인이다.

**BEAT·KAITO는 낙폭 축소가 뚜렷이 가속**됐다. BEAT는 OKX -19.92%→**-13.76%**, Aster -19.75%→
**-13.48%**로 큰 폭 개선됐고, KAITO는 OKX 직접 -8.20%→**-5.37%**, HL -8.15%→**-4.26%**로 두 레그
모두 추가 회복했다 — 8월 언락 부담(KAITO $323M 합산, BEAT 8/1 $67~82M)에도 불구하고 회복세가
우세해지는 모습이다.

**⚠️ AKE는 극적으로 반전**됐다 — Binance -3.19%·Bybit -2.35%(CEX 평균 **-2.77%**, 직전 -12.32%)·
Aster -1.66%(직전 -13.05%)로 3레그 모두 낙폭이 10%p 안팎 급격히 줄어들며 거의 flat에 근접했다 —
웹서치로 AKE(Akedo, AI게이밍 토큰)가 7월 랠리 후 조정 국면이었다는 배경은 확인되나, 이번 회차의
급격한 반전 자체의 개별 촉매는 미확인이다.

**⚠️ BANK는 계속 악화**됐다 — Binance -11.09%·Bybit -10.69%(CEX 평균 **-10.89%**, 직전 -8.66%)·
Aster -11.52%(직전 -8.38%)로 낙폭이 더 커졌고, funding은 Binance -0.19%·Aster -0.179%로 직전과
비슷한 수준을 유지했다(⚠️ Bybit CG funding -1.048은 이번 회차도 다른 레그 대비 이상치로 스케일
오류 가능성이 있어 참고용으로만 표기). 웹서치로 **Lorenzo Protocol(BANK)이 7월 급등 이후
차익실현·레버리지 청산·약한 현물 수요로 조정 중**이라는 배경이 확인됐다.

**CASHCAT은 4회 연속 재가속**했다 — HL+66.71%·Aster+68.02%(평균 **+67.36%**, 직전 +53.91%)로
상승폭이 계속 확대됐다. 로빈후드체인(Robinhood Chain) 밈코인·HL 퍼프 상장 촉매가 웹서치로
재확인됐다. **BTW는 상승폭이 소폭 둔화됐으나 OI는 계속 증가**했다 — Aster +35.18%→**+31.85%**로
다소 둔화됐지만, OI는 $8.19M→**$8.37M**로 계속 증가해 신규 유입이 이어지는 정황이다.

**BLESS는 낙폭이 소폭 완화**됐다 — Aster -44.33%→**-40.25%**로 여전히 깊은 하락권이나 다소
개선됐다(OrangeX 레그는 이번 회차도 조회 실패).

**ATOM·ALGO·ADA는 계속 상승세를 유지**했다 — ATOM CEX 평균 **+9.15%**(직전 +9.58%, 거의 유지),
ALGO CEX 평균 **+6.05%**(직전 +4.17%, 재가속돼 ATOM과 다시 궤적이 근접), ADA CEX 평균 **+6.35%**
(직전 +6.23%, 유지).

**⚠️ CORE·AEON은 다시 마이너스로 반전**됐다 — CORE는 OKX +1.26%→**-0.10%**로 재차 하락 전환,
AEON도 +1.93%→**-2.01%**로 마이너스 전환됐다 — 두 종목 모두 방향이 계속 뒤집히는 저활동
오실레이션 패턴이 이어진다.

**MMT는 가격 상승과 funding 심화가 계속 갈라졌다** — OKX 직접 +1.64%→**+2.70%**로 가격은
개선됐으나, funding은 -0.073%→**-0.093%**로 더 심화됐다.

**CAP은 CEX·DEX 괴리가 크게 좁혀졌다** — CEX(OKX) -2.46%→**-1.47%**, DEX(Aster) -5.92%→
**-1.36%**로 두 레그의 폭 차이가 거의 사라졌다.

**⚠️ 신규 포착: ANSEM(Aster)** — 이번 회차 처음 상위권에 등장, **-12.35%**(거래량 $0.58M, OI
$1.17M), 개별 촉매는 미확인이며 후속 회차에서 지속 추적이 필요하다.

## 시장 전반

- **총 시총 $2.2657T(24h +1.40%, 직전 +1.28%), BTC 도미넌스 56.41%, ETH 도미넌스 9.91% — 반등이 4회 연속 가속.**
- **⚠️ 신규: 토큰화 주식 퍼프 대량 확인(AAOI·AXTI·AEHR·ASTS·BABA·COHR·CRWV·APLD·BX) — 전부 규약에 따라 제외.**
- **1000RATS 부분 반등(-27.70%→-23.01%), BICO 4회 연속 상승 지속(+8.34%→+11.4%, 왕복→지속랠리 전환).**
- **⚠️ AKE 극적 반전(-12.32%→-2.77%), BANK는 계속 악화(-8.66%→-10.89%, Lorenzo 조정 배경 확인).**
- **CASHCAT 4회 연속 재가속(+53.91%→+67.36%) — 로빈후드체인·HL 상장 촉매 지속.**
- **⚠️ 데이터 소스 이슈 지속·악화: orangex·dydx_v4 7회 연속, gmx·xt_derivatives 8회 연속 미확인, DefiLlama 402 실패.**

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **1000RATS** [부분 반등] | Binance/Bybit/Aster | $294.83M | $26.19M | +0.004% | -23.01% | -27.70%→-23.01%(3거래소 낙폭 축소), 여전히 깊은 하락권, 촉매 미확인 | partial-rebound-still-deep-decline-no-catalyst |
| **BICO (Biconomy)** [⚠️ 4회 연속 상승 — 지속랠리 전환] | OKX(직접API) | $100.40M | $2.16M | -0.059% | +11.4% | +8.34%→+11.4%로 왕복 패턴 넘어 방향성 있는 상승 국면 전환 | sustained-rally-4th-round-no-longer-whipsaw |
| **BEAT (Audiera)** [낙폭 축소 가속] | OKX(직접API/CG) | $228.20M | $9.60M | -0.021% | -13.76% | -19.92%→-13.76%, Aster(-13.48%)도 큰 폭 개선, 회복세 우세 | decline-eases-strongly-recovery-gains-ground |
| **KAITO (CEX)** [회복 가속] | OKX(직접API) | $72.30M(근사) | $8.26M(이월) | +0.005% | -5.37% | -8.20%→-5.37%, HL(-4.26%)도 개선 — 언락 부담에도 촉매 회복 우세 | recovery-accelerates-katalyst-gains-vs-unlock |
| **BANK** [⚠️ 계속 악화, Lorenzo 조정 확인] | Binance/Bybit | $163.24M | $23.14M | -0.185% | -10.89% | -8.66%→-10.89%, DEX(-11.52%)도 심화, Lorenzo 7월 급등 후 조정 배경 확인(⚠️ Bybit -1.048 이상치) | worsens-further-lorenzo-correction-confirmed |
| **AKE (Akedo)** [⚠️ 극적 반전] | Binance/Bybit | $135.31M | $49.65M | +0.0065% | -2.77% | -12.32%→-2.77%, DEX(-1.66%)도 거의 flat 근접 — 7월 랠리 후 조정 배경은 확인, 반전 자체 촉매 미확인 | sharp-reversal-nears-flat-no-specific-catalyst |
| ATOM [거의 유지] | Binance/Bybit | $43.91M | $32.52M | -0.0075% | +9.15% | +9.58%→+9.15%로 유지, 촉매 여전 미확인(OKX 레그 이번 회차 미재확인) | roughly-steady-continues-no-catalyst |
| ALGO [재가속 — ATOM과 재수렴] | Binance/Bybit | $36.11M | $17.29M | +0.01% | +6.05% | +4.17%→+6.05%로 확대, ATOM과 궤적 다시 근접 | reaccelerates-converges-back-with-atom |
| ADA [유지] | Binance/Bybit | $429.23M | $189.45M | +0.01% | +6.35% | +6.23%→+6.35%로 유지, 시장 반등과 궤를 같이함 | steady-continues-tracks-market |
| AAVE [유지] | Binance/Bybit | $80.14M | $93.39M | +0.001% | +1.19% | +0.92%→+1.19%로 소폭 확대 | steady-mild-uptick |
| ASTER (CEX) [flat 유지] | Binance/Bybit | $14.43M | $114.10M | +0.005% | +1.32% | +0.96%→+1.32%로 거의 변화 없음 | flat-continues-tracks-dex |
| **CORE** [⚠️ 재차 반전 — 플러스→마이너스] | OKX(직접API/CG) | $11.10M | $1.22M | -0.015% | -0.10% | +1.26%→-0.10%로 재차 하락 전환, 저활동 오실레이션 지속 | reversal-flips-negative-again-low-activity-oscillation |
| **MMT (Momentum)** [가격·funding 괴리 심화 지속] | OKX(직접API) | $1.83M(근사) | $3.26M(이월) | -0.093% | +2.70% | +1.64%→+2.70%로 가격 개선되나 funding -0.073%→-0.093%로 더 심화 | price-funding-divergence-continues-deepens |
| **AEON** [⚠️ 재차 반전 — 플러스→마이너스] | OKX(직접API/CG) | $9.16M | $3.11M | +0.005% | -2.01% | +1.93%→-2.01%로 다시 하락 전환, 저활동 오실레이션 지속 | reversal-flips-negative-again-low-activity |
| CAP [개선 지속, DEX 괴리 좁혀짐] | OKX | $14.50M | $1.36M | +0.005% | -1.47% | -2.46%→-1.47%로 개선, DEX(Aster -1.36%)와 폭 차이 거의 사라짐 | improves-further-cex-dex-gap-narrows-sharply |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM)

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **CASHCAT** [4회 연속 재가속] | Hyperliquid/Aster | $16.54M | $12.55M | +0.001% | +67.36% | +53.91%→+67.36%(HL+66.71%·Aster+68.02%) — 로빈후드체인·HL 상장 촉매 재확인 | reaccelerates-4th-round-robinhood-chain-catalyst-confirmed |
| BTW [상승폭 둔화, OI 계속 증가] | Aster | $0.97M | $8.37M | +0.011% | +31.85% | +35.18%→+31.85%로 둔화되나 OI $8.19M→$8.37M로 계속 증가 — 신규 유입 지속 | mild-deceleration-oi-keeps-growing |
| **BLESS-USDT** [낙폭 소폭 완화] | Aster | $2.52M | $0.21M | +0.007% | -40.25% | -44.33%→-40.25%로 개선되나 여전히 깊은 하락권, OrangeX 7회 연속 실패 | decline-eases-slightly-still-deep-orangex-unreachable |
| BLESS-USDT-PERPETUAL [⚠️ 7회 연속 조회 실패] | OrangeX | $294.86M(이월) | $102.36M(이월) | -0.073%(이월) | +12.00%(이월) | `orangex` 이번 회차도 429로 실패 | fetch-failed-7th-round-carried-forward |
| **1000RATS-USDT** [CEX와 함께 부분 반등] | Aster | $0.74M | $0.043M | +0.003% | -22.86% | -28.80%→-22.86%로 낙폭 축소, CEX(-23.01%)와 거의 동조 | partial-rebound-tracks-cex |
| **BEAT-USDT** [CEX와 함께 회복 가속] | Aster | $1.40M | $0.28M | +0.001% | -13.48% | -19.75%→-13.48%, OKX(-13.76%)와 거의 동조 | tracks-cex-recovery-accelerates |
| **AKE-USDT** [⚠️ CEX와 함께 극적 반전] | Aster | $1.12M | $11.56M | +0.008% | -1.66% | -13.05%→-1.66%, CEX(-2.77%)와 함께 거의 flat 근접까지 급개선 | sharp-reversal-tracks-cex-nears-flat |
| **BANK-USDT** [CEX와 함께 계속 악화] | Aster | $0.90M | $0.32M | -0.179% | -11.52% | -8.38%→-11.52%, CEX(-10.89%)와 동조 심화 — Lorenzo 조정 배경 확인 | worsens-further-tracks-cex-lorenzo-correction |
| CAP-USDT [개선 지속] | Aster | $0.021M | $0.031M | +0.001% | -1.36% | -5.92%→-1.36%로 크게 개선, CEX(OKX -1.47%)와 폭 차이 거의 사라짐 | improves-further-aligns-closely-with-cex |
| ASTER-USDT [flat 지속] | Aster/Hyperliquid | $8.68M | $221.66M | +0.009% | +1.36% | +0.93%→+1.36%로 소폭 확대, OI $221.7M 대규모 유지 | flat-continues-tracks-cex |
| ATOM-USD [CEX와 함께 거의 유지] | Aster/Hyperliquid | $1.03M | $3.80M | -0.001% | +9.20% | +8.59%→+9.20%로 CEX(+9.15%)와 유사하게 유지 | roughly-steady-tracks-cex |
| ALGO-USD [CEX와 함께 재가속] | Aster/Hyperliquid | $2.83M | $2.66M | +0.001% | +6.35% | +4.60%→+6.35%로 CEX(+6.05%)와 유사하게 확대 | reaccelerates-tracks-cex |
| HYPE-USD [거의 유지] | Hyperliquid | $217.30M | $1,219.00M | +0.001% | +3.70% | +3.88%→+3.70%로 소폭 둔화, OI $1.22B 대규모 유지 | roughly-steady-continues |
| HYPER-USD [마이너스 폭 확대] | Hyperliquid | $0.38M | $0.36M | -0.004% | -5.86% | -4.37%→-5.86%로 마이너스 폭 확대, 소형 유동성 변동성 큼 | negative-continues-mild-deepening-low-liquidity |
| **KAITO-USD** [CEX와 함께 회복 가속] | Hyperliquid | $8.28M | $24.08M | +0.004% | -4.264% | -8.15%→-4.26%로 CEX(-5.37%)와 함께 회복 지속 — 언락 부담·촉매 회복 대치 지속 | recovery-accelerates-tracks-cex |
| **APEX-USD** [⚠️ 반전 — 플러스→마이너스] | Hyperliquid | $0.079M | $0.79M | +0.001% | -0.666% | +0.06%→-0.67%로 재차 냉각, 저활동 오실레이션 | reversal-flips-negative-low-activity |
| FARTCOIN [거의 유지] | Hyperliquid | $6.20M | $22.20M | +0.001% | +4.10% | +4.69%→+4.10%로 소폭 축소 | roughly-steady-mild-deceleration |
| ADA-USD [CEX와 함께 유지] | Hyperliquid/Aster | $11.55M | $33.97M | +0.005% | +6.45% | +5.74%→+6.45%로 CEX(+6.35%)와 유사하게 유지 | steady-tracks-cex |
| AAVE-USD [유지] | Hyperliquid/Aster | $0.25M | $4.78M | +0.01% | +1.28% | +0.85%→+1.28%로 CEX(+1.19%)와 함께 소폭 확대(⚠️ HL 레그 미재확인, Aster 값 사용) | steady-mild-uptick-tracks-cex |
| BULLA [⚠️ 재확인 실패] | Aster | $1.08M(이월) | $7.24M(이월) | +0.003%(이월) | +0.20%(이월) | 이번 회차 Aster 스캔에서 포착되지 않음, 직전 값 이월 | not-recaptured-carried-forward |
| **ANSEM** [⚠️ 신규 포착] | Aster | $0.58M | $1.17M | +0.001% | -12.35% | 이번 회차 처음 Aster 상위권 진입, 개별 촉매 미확인, 후속 추적 필요 | new-entrant-first-seen-no-catalyst |
| ETH-USD [⚠️ 7회 연속 조회 실패] | dYdX | $12.62M(이월) | $19.41M(이월) | -0.010%(이월) | +0.25%(이월) | `dydx_v4` 재차 실패 | fetch-failed-7th-round-carried-forward |
| BTC-USD [⚠️ 7회 연속 조회 실패] | dYdX | $7.31M(이월) | $17.47M(이월) | +0.001%(이월) | +1.06%(이월) | ETH-USD와 동일 현상 | fetch-failed-7th-round-carried-forward |
| LIT-USD (dYdX) [⚠️ 재동결, 9회 연속 재확인 불가] | dYdX | $14.31(이월) | $14,718.01(이월) | 0.0%(이월) | +1.14%(이월) | dydx_v4 실패로 재확인 자체 불가 | refreeze-status-carried-api-fetch-failed |
| KAITO-USD (dYdX) [⚠️ 7회 연속 조회 실패] | dYdX | $488.35(이월) | $0.0(이월) | 0.0%(이월) | 0.0%(이월) | dydx_v4 재확인 불가 | fetch-failed-7th-round-carried-forward |
| ETH/USD (WETH-USDC) [⚠️ 8회 연속 조회 실패] | GMX | $23.40M(이월) | $16.14M(이월) | +0.001%(이월) | +2.21%(이월) | gmx 재차 실패 — 구조적 이슈 지속 | fetch-failed-8th-round-carried-forward |
| BTC/USD (BTC-USDC) [⚠️ 8회 연속 조회 실패] | GMX | $7.52M(이월) | $33.60M(이월) | +0.002%(이월) | +1.23%(이월) | ETH/USD와 동일 현상 | fetch-failed-8th-round-carried-forward |
| GIGGLE (Giggle Fund) [⚠️ 8회 연속 조회 실패] | XT.COM | $34.11M(이월) | $224.34M(이월) | +0.5%(이월) | +6.12%(이월) | 이번 회차도 429 rate limit로 미확인 | fetch-failed-8th-round-carried-forward |

## 테마 태그

1. **시장 반등 계속 가속**: 총 시총 $2.2657T(+1.40%), BTC 도미넌스 56.41%. 4회 연속 회복세 강화 (market-rebound-continues-accelerating).
2. **⚠️ 신규: 토큰화 주식 퍼프 대량 확인 — 전부 제외** — AAOI·AXTI·AEHR·ASTS·BABA·COHR·CRWV·APLD·BX 등 (tradfi-tokenized-stocks-batch-discovered-excluded).
3. **1000RATS 부분 반등(-27.70%→-23.01%)** — 촉매 여전히 미확인 (partial-rebound-still-deep-no-catalyst).
4. **⚠️ BICO 4회 연속 상승 — 지속랠리로 전환(+8.34%→+11.4%)** (sustained-rally-4th-round-no-longer-whipsaw).
5. **BEAT·KAITO 회복 가속** — 8월 언락 부담에도 회복세 우세해지는 흐름 (recovery-accelerates-both-legs-unlock-pressure-losing-ground).
6. **⚠️ AKE 극적 반전 — 거의 flat 근접(-12.32%→-2.77%)** — Akedo 7월 조정 배경 확인, 반전 촉매는 미확인 (sharp-reversal-nears-flat-akedo-no-specific-catalyst).
7. **⚠️ BANK 계속 악화, Lorenzo Protocol 조정 배경 확인** (worsens-further-lorenzo-correction-confirmed).
8. **CASHCAT 4회 연속 재가속(+53.91%→+67.36%), BTW는 OI 계속 증가** (reaccelerates-4th-round-cashcat-btw-oi-grows).
9. **ATOM·ALGO·ADA 상승세 유지, ALGO는 ATOM과 재수렴** (uptrend-basket-continues-algo-reconverges-atom).
10. **CORE·AEON 재차 마이너스 반전** — 저활동 오실레이션 지속 (reversal-flip-negative-again-low-activity-oscillation).
11. **MMT 가격·funding 괴리 계속 심화** (price-funding-divergence-continues-deepens).
12. **CAP CEX·DEX 괴리 크게 좁혀짐** (cap-cex-dex-gap-narrows-sharply).
13. **⚠️ 신규 포착: ANSEM(Aster)** — 후속 추적 필요 (new-entrant-ansem-first-seen).
14. **⚠️ 데이터 신뢰도 이슈 지속·악화: orangex·dydx_v4 7회 연속, gmx·xt_derivatives 8회 연속 미확인, DefiLlama 402 실패** (persistent-multi-source-failures-worsen).

## 데이터 신뢰도

**이번 회차 데이터 소스 이상은 지속·일부 악화됐다.** (a) `orangex`는 **7회 연속** 실패(429), `dydx_v4`는
**7회 연속** 실패(404/429), `gmx`·`xt_derivatives`는 **8회 연속** 실패(429)로, 구조적 이슈가 더 굳어지고
있다. DefiLlama derivatives 개요 API(`/overview/derivatives`)도 이번 회차 402(Payment Required)로
실패해 프로토콜별 순위 교차검증을 하지 못했다. (b) CoinGecko `binance_futures`·`bybit`·`okex_swap`·
`hyperliquid`·`aster` 및 OKX 공개 API(`market/ticker`+`public/funding-rate`)를 raw JSON으로 직접
조회해 BICO·KAITO·MMT를 재검증했다 — BICO는 OKX 직접(+11.59%)과 CG(+11.18%)가 근접해 교차검증됐다.
(c) KAITO·MMT는 OKX raw `vol24h` 필드가 USD가 아닌 기초자산(토큰) 수량으로 확인돼(BICO 사례로
검증: raw값×가격 ≈ CG의 USD 거래량과 일치), 이번 회차 거래량은 평균가를 곱한 **근사값**으로 표기했다
(⚠️ 근사 표기).

**⚠️ funding 이상치 주의(지속)**: BANK의 Bybit CG funding 값이 -1.048(퍼센트 스케일 기준 -1.048%)로
같은 종목의 Binance(-0.19%)·Aster(-0.179%) 대비 5~6배 큰 이상치를 이번 회차도 보였다 — 직전 회차의
-1.232와 유사한 패턴으로, Bybit BANK funding 필드 자체가 구조적으로 다른 스케일을 쓰는 것으로 추정되나
확정하지 못해 참고용으로만 표기했다.

**⚠️ 신규 발견: 토큰화 주식 퍼프 대량 확인**: Binance·OKX 스캔에서 AAOI·AXTI·AEHR·ASTS·BABA·COHR·
CRWV·APLD·BX 등 반도체·우주·AI인프라 테마 실제 상장주식의 토큰화 퍼프가 대거 확인됐다. CBRS는
종목 식별이 불확실해 안전하게 제외했다. 규약에 따라 전부 리스트에서 제외했다.

**웹서치 검증**: 1000RATS는 이번 회차도 개별 촉매·공지를 찾지 못했다(검색 결과가 "프리뷰 코인·
미상장" 등 명백히 오래되거나 부정확한 캐시성 정보를 반환해 신뢰하지 않았고, 우리 스냅샷의 CEX 직접
API 3개 레그 동조 데이터를 근거로 사용). BICO는 ERC-8211 표준·AI블록체인 내러티브(6월 시점 정보,
최신성 불확실)가 배경으로 확인됐으나 최근 급등의 직접 촉매는 아닐 수 있다. BANK는 Lorenzo Protocol의
7월 급등 후 차익실현·레버리지 청산·약한 현물 수요발 조정이 웹서치로 확인됐다. AKE(Akedo)는 7월 랠리
후 조정 국면이었다는 배경은 확인되나, 이번 회차의 급격한 반전 자체의 개별 촉매는 찾지 못했다.
CASHCAT은 로빈후드체인 밈코인·HL 퍼프 상장 촉매가 재확인됐다.

**funding 값 단위 관련 주의**: CEX·DEX 종목의 funding 값은 각 API가 반환한 원시 수치를 percent
스케일로 그대로 사용했다(CoinGecko `funding_rate` 필드는 percent로 직접 취급, OKX raw `fundingRate`는
소수를 100배해 percent로 환산). 거래소·필드별 스케일 표기 관례가 다를 수 있어 **회차 간 funding
절대값 비교는 참고용으로만** 활용할 것을 권한다.

한계: (a) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며, 완전한
전체 시장 스캔은 아니다; (b) OrangeX·dYdX·GMX·XT.COM은 위에서 설명한 대로 이번 회차도 미해결이며,
7~8회 연속 실패가 이어져 구조적 이슈로 굳어지고 있다; (c) BANK Bybit funding은 이상치 가능성이 있어
참고용으로만 표기했다; (d) KAITO·MMT의 이번 회차 OKX 거래량은 raw 필드 단위 문제로 평균가 환산
근사값이다; (e) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에 따라 cex/dex 리스트에서
전부 제외했다 — 이번 회차 신규로 AAOI·AXTI·AEHR·ASTS·BABA·COHR·CRWV·APLD·BX 등 다수의 토큰화 주식
퍼프가 확인돼 모두 제외 처리했다(CL-USDT 원유 토큰화도 계속 제외); (f) BULLA·ATOM/ALGO OKX 레그는
이번 회차 스캔에서 재확인되지 않아 일부는 이월값을 사용했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
