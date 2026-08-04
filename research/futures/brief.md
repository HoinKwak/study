# 선물시장 스카우트 브리핑 — 2026-08-04 10:58 UTC (KST 2026-08-04 19:58)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-04T08:55:00Z)
> 로부터 약 2시간 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`이 이번 회차도 429로 실패해 WebSearch 근사치를 사용했다 — 총 시총 **약 $2.23T**,
BTC 도미넌스 **약 56.42%**로 직전(≈$2.24T/56.4%)과 거의 동일해 시장 전반은 안정적으로 유지되는 것으로
판단된다.

**⚠️ BANK는 극적으로 반전**했다 — CEX 평균 -2.38%→**+10.20%**(Binance+10.932%·Bybit+9.461%),
DEX(Aster +10.098%)도 동조해 직전 회차의 개선이 랠리로 확대됐다. 다만 웹서치로 **BANK Foundation
추정 지갑이 8,400만 BANK를 Aster 입금주소로 이체**한 정황(7월 말 보도)이 확인돼 향후 매도 압력
리스크가 잠재한다는 점은 유의할 필요가 있다. Bybit funding도 직전 이상치(-0.805)에서 **-0.167**로
스케일이 정상화된 것으로 보인다.

**1000RATS는 재차 심화**돼 -28.46%→**-35.61%**(Binance-35.68%·Bybit-35.538%, DEX Aster -35.402%)로
라운드 중 가장 깊은 낙폭을 기록했다 — 신규 개별 촉매는 확인되지 않았으나 기존에 규명된 Aster 8/1
신규상장발 펌프·크래시 왕복 패턴이 지속되는 것으로 판단된다.

**⚠️ BICO는 5회 연속 상승이 꺾이며 급반전**했다 — OKX 기준 +24.68%→**+6.39%**로 랠리 대부분을
반납했고, funding은 -0.062%→**-0.130%**로 숏 우위가 오히려 심화돼(랠리 와중에도 숏 유입) 전형적
되돌림 패턴을 보였으며, OI도 $2.45M→**$2.34M**로 소폭 감소해 초기 이탈 정황이다. 웹서치로 이번
랠리가 공식 촉매 없는 투기적 모멘텀·알트 로테이션발이었음이 확인됐고, Bitkub 상장은 8/22
예정(아직 미반영 촉매)이다.

**AKE는 CEX·DEX 모두 개선**됐다(CEX -11.05%→**-7.30%**, DEX -10.003%→**-7.615%**) — 8/21 언락
부담은 여전하나 낙폭이 줄어드는 흐름이다. **KAITO도 소폭 개선**됐다(-10.15%→**-7.83%**, HL도
-9.539%→**-9.028%**).

**⚠️ GRAM 촉매 신규 규명** — 직전 회차 미확인이었던 GRAM(HL)이 웹서치로 **TON 블록체인의 GRAM
리브랜딩 + Binance·Hyperliquid 동시 상장(최대 5x 레버리지, 커뮤니티 요청에 의한 HL 신규 상장)**으로
확인됐다 — 변동은 거의 flat(-0.136%→-1.12%) 유지.

**⚠️ BTW는 OI가 재차 증가로 반전**됐다(전 회차 첫 감소 $8.37M→$7.93M였으나 이번 $7.93M→**$8.27M**) —
상승폭도 +22.98%→**+24.25%**로 소폭 재가속해 열기가 완전히 식지 않았음을 시사한다.

**CASHCAT은 계속 둔화**됐다(+57.76%→**+43.87%**, HL+44.276%·Aster+43.455%) — 로빈후드체인 플래그십
밈코인 지위, HL 퍼프 고위험 디슬로케이션 이력은 여전히 유의 대상이다.

**ADA·AAVE는 상승세가 꺾였다** — ADA는 +6.42%→**+3.82%**로 둔화, AAVE는 +1.56%→**-0.29%**로
플러스에서 마이너스로 반전됐다. **AEON은 재악화**(-1.53%→**-4.29%**)됐고, CORE·MMT·CAP은 대체로
유지됐다.

## ⚠️ 데이터 인프라 대규모 정정 (이번 회차 신규 발견)

CoinGecko 파생 거래소 ID 체계가 바뀐 것을 확인했다. 옛 `dydx_v4`(8~9회 연속 실패)가 아니라
**`dydx_chain`**이 정확한 ID로, 이를 통해 **ETH-USD·BTC-USD(dYdX)가 다회 만에 재확인**됐다
(ETH +0.428%, BTC +1.271%). 다만 정정된 목록에서 **LIT-USD·KAITO-USD(dYdX) 페어 자체가 존재하지
않는 것**이 확인돼 — 기존 이월값은 잘못된 매핑 가능성이 높아 이번 회차부터 목록에서 제외했다.
`xt_derivatives`도 이번 회차 처음 정상 응답했으나 **GIGGLE 티커 자체가 더 이상 목록에 없어 상장폐지
추정**돼 마찬가지로 제외했다. GMX는 올바른 ID(`gmx-perpetuals-v2-arbitrum` 등, 옛 `gmx`는 이제
무효)를 확인했으나 이번 회차도 429로 재조회 실패했다. `orangex`는 이번 회차도 429로 재차 실패해
연속 조회 실패가 지속되고 있다.

**⚠️ OKX 거래량 산정 방식도 정정**했다: OKX SWAP 티커의 `volCcy24h` 필드는 공식 문서상 기초자산
수량이라 가격을 곱해야 USD 환산값이 되는데, 지난 회차들의 일부 종목(특히 MMT)은 이 곱셈이
누락됐을 가능성이 있어 이번 회차부터 `volCcy24h × last가격`으로 일관 재계산했다 — 회차 간 OKX
거래량 절대치 비교는 이 정정으로 인해 불연속적일 수 있음에 유의해야 한다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BANK (Lorenzo)** [⚠️ 극적 반전] | Binance/Bybit | $213.01M | $23.88M | -0.1035% | +10.20% | -2.38%→+10.20%, 다만 BANK Foundation 추정 지갑의 8,400만 토큰 Aster 이체 정황(잠재 매도압력) 병존, Bybit funding 이상치 정상화 | sharp-reversal-to-positive-whale-transfer-risk |
| **1000RATS** [⚠️ 재차 심화, 최저치] | Binance/Bybit | $285.11M | $25.72M | +0.0055% | -35.61% | -28.46%→-35.61%, 신규 촉매 없이 Aster 8/1 상장발 왕복 패턴 지속 | deepens-further-round-low |
| **BICO (Biconomy)** [⚠️ 급반전, 랠리 종료] | OKX(직접API) | $94.43M | $2.34M | -0.13% | +6.39% | +24.68%→+6.39%로 랠리 대부분 반납, funding 숏 우위 심화, OI 소폭 감소 — 공식촉매 없는 투기 랠리의 전형적 되돌림, Bitkub 상장 8/22 예정 | reversal-after-rally-profit-taking-oi-declines |
| **AKE (Akedo)** [개선] | Binance/Bybit | $136.46M | $50.03M | +0.005% | -7.30% | -11.05%→-7.30%, DEX도 동조 개선 — 8/21 언락 부담은 여전하나 매도압력 완화 | improves-unlock-pressure-eases |
| BEAT (Audiera) [거의 유지] | OKX(직접API) | $188.65M | $8.50M | -0.0055% | -16.01% | -15.18%→-16.01%로 큰 변화 없음, 여전히 깊은 하락권 | roughly-steady-still-deep |
| KAITO (CEX) [소폭 개선] | OKX(직접API) | $60.93M | $7.75M | +0.005% | -7.83% | -10.15%→-7.83%로 낙폭 축소, HL도 유사 — $323M 언락 부담 속 완만한 회복 조짐 | mild-improvement-unlock-still-present |
| ADA [둔화] | Binance/Bybit | $422.03M | $186.85M | +0.007% | +3.82% | +6.42%→+3.82%로 상승세 유지되나 확대 속도 꺾임 | deceleration-continues-tracks-market |
| AAVE [반전] | Binance/Bybit | $78.20M | $91.78M | -0.001% | -0.29% | +1.56%→-0.29%로 플러스→마이너스 전환 | flips-negative-mild |
| ATOM [거의 유지] | Binance/Bybit | $46.80M | $32.86M | -0.0085% | +8.15% | +8.30%→+8.15%로 큰 변화 없음, 촉매 미확인 | roughly-steady-no-catalyst |
| ASTER (CEX) [flat 유지] | Binance | $12.70M | $72.74M | +0.005% | +1.13% | +1.549%→+1.131%로 큰 변화 없음(Bybit 레그 미재확인) | flat-continues-bybit-leg-not-reconfirmed |
| ALGO [둔화] | Binance | $23.34M | $8.81M | +0.01% | +4.56% | +6.628%→+4.555%로 확대 속도 꺾임(Bybit 레그 미재확인) | deceleration-bybit-leg-not-reconfirmed |
| AEON [⚠️ 재악화] | OKX(직접API) | $9.30M | $2.19M | -0.0142% | -4.29% | -1.53%→-4.29%로 저활동 오실레이션 속 낙폭 확대 | worsens-low-activity-oscillation |
| CORE [거의 유지] | OKX(직접API) | $10.85M | $1.20M | -0.0209% | +0.82% | +0.68%→+0.82%로 소폭 상승 지속 | roughly-steady-low-activity-oscillation |
| MMT (Momentum) [소폭 둔화] | OKX(직접API) | $17.25M | $2.96M | -0.0214% | +1.62% | +2.42%→+1.62%로 큰 변화 없음, ⚠️ 거래량 산정방식 정정으로 스케일 변동 | roughly-steady-vol-methodology-corrected |
| CAP [거의 유지] | OKX(직접API) | $12.33M | $1.28M | +0.005% | -6.38% | -6.03%→-6.38%로 하락권 지속, DEX는 소폭 개선 | roughly-steady-still-negative |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM)

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **BANK-USDT** [⚠️ CEX와 함께 극적 반전] | Aster | $0.90M | $0.42M | -0.042% | +10.10% | -3.57%→+10.098%, CEX와 동조 — 랠리 이면에 BANK Foundation 대량 이체 정황 주의 | tracks-cex-sharp-reversal-whale-transfer-risk |
| **1000RATS-USDT** [⚠️ CEX와 함께 재차 심화] | Aster | $0.79M | $0.033M | +0.003% | -35.40% | -29.924%→-35.402%, CEX와 동조, 라운드 최저치 | tracks-cex-deepens-further |
| **GRAM** [⚠️ 촉매 신규 규명] | Hyperliquid | $12.46M | $13.15M | +0.001% | -1.12% | TON의 GRAM 리브랜딩 + Binance·HL 동시 상장(최대 5x, 커뮤니티 요청) 확인됨, 변동은 flat | catalyst-confirmed-ton-rebrand-binance-hl-listing |
| **BTW** [⚠️ OI 재증가, 재가속] | Aster | $1.07M | $8.27M | +0.011% | +24.25% | 전회차 첫 OI감소가 되돌려지며 재증가($7.93M→$8.27M), 상승폭도 재가속 — 열기 안식지 않음 | oi-reaccelerates-heat-not-fully-cooling |
| CASHCAT [계속 둔화] | Hyperliquid/Aster | $17.78M | $11.65M | -0.0105% | +43.87% | +57.76%→+43.87% — 로빈후드체인 플래그십, HL 고위험 디슬로케이션 이력 유의 | deceleration-continues-high-derivatives-risk |
| BEAT-USDT [거의 유지] | Aster | $0.98M | $0.28M | +0.001% | -15.17% | -15.877%→-15.171%, CEX와 유사, 여전히 깊은 하락권 | roughly-steady-tracks-cex-still-deep |
| AKE-USDT [CEX와 함께 개선] | Aster | $0.84M | $12.06M | +0.007% | -7.62% | -10.003%→-7.615%, CEX와 동조 개선 | tracks-cex-improves |
| CAP-USDT [소폭 개선] | Aster | $0.026M | $0.028M | +0.001% | -4.64% | -8.26%→-4.637%로 낙폭 축소, CEX보다 소폭 나음 | mild-improvement |
| BLESS-USDT [⚠️ 재악화] | Aster | $2.17M | $0.21M | +0.005% | -46.23% | -38.937%→-46.234%로 낙폭 확대, OrangeX 레그 이번도 조회 실패 | worsens-still-deep-orangex-unreachable |
| BLESS-USDT-PERPETUAL [⚠️ 조회 실패 지속] | OrangeX | $294.86M(이월) | $102.36M(이월) | -0.073%(이월) | +12.00%(이월) | `orangex` 이번 회차도 429, 연속 실패 지속 | fetch-failed-carried-forward-continues |
| ASTER-USDT [flat 지속] | Aster | $9.57M | $221.54M | +0.008% | +1.28% | +1.329%→+1.28%로 거의 변화 없음, OI 대규모 유지 | flat-continues-large-oi-maintained |
| ATOM-USD [거의 유지] | Aster | $0.021M | $1.60M | +0.008% | +6.94% | +8.63%→+6.94%로 CEX와 유사하게 소폭 둔화 | roughly-steady-tracks-cex |
| ALGO-USD [둔화] | Aster | $0.047M | $0.031M | -0.001% | +5.12% | +7.017%→+5.123%로 CEX와 유사하게 둔화 | deceleration-tracks-cex |
| HYPE-USD [소폭 둔화] | Hyperliquid | $213.91M | $1,236.85M | +0.001% | +4.43% | +5.13%→+4.427%로 확대세 소폭 꺾임, OI $1.237B 대규모 유지 | mild-deceleration-large-oi-maintained |
| HYPER-USD [⚠️ 재확인 실패] | Hyperliquid | $0.38M(이월) | $0.36M(이월) | -0.004%(이월) | -5.855%(이월) | HL $3M+ 스캔 임계값 미달, 계속 미포착 | not-recaptured-carried-forward |
| KAITO-USD [거의 유지, 소폭 개선] | Hyperliquid | $6.49M | $24.70M | +0.001% | -9.03% | -9.539%→-9.028%, CEX와 함께 완만한 회복 조짐 | roughly-steady-mild-improvement-tracks-cex |
| APEX-USD [⚠️ 재확인 실패] | Hyperliquid | $0.079M(이월) | $0.79M(이월) | +0.001%(이월) | -0.666%(이월) | HL $3M+ 스캔 임계값 미달, 계속 미포착 | not-recaptured-carried-forward |
| FARTCOIN [둔화] | Hyperliquid | $6.12M | $22.48M | +0.001% | +2.51% | +4.564%→+2.506%로 상승폭 축소 | deceleration-continues |
| ADA-USD [둔화] | Hyperliquid/Aster | $11.02M | $34.18M | +0.0035% | +4.47% | +6.50%→+4.47%로 CEX와 유사하게 둔화 | deceleration-tracks-cex |
| AAVE-USD [반전] | Hyperliquid/Aster | $5.70M | $70.02M | -0.0015% | -0.09% | +1.755%→-0.094%로 CEX와 함께 소폭 하락 전환 | flips-negative-mild-tracks-cex |
| BULLA [소폭 악화] | Aster | $0.66M | $7.23M | +0.009% | -5.85% | -3.962%→-5.846%로 낙폭 소폭 확대 | mild-worsening |
| ANSEM [계속 개선] | Aster | $0.45M | $1.17M | +0.006% | -4.61% | -5.208%→-4.608%로 낙폭 소폭 축소, 신규상장 초기 안정화 지속 | continues-stabilizing-after-new-listing |
| **ETH-USD** [⚠️ 데이터소스 정정 후 재확인] | dYdX | $11.86M | $19.62M | -0.002% | +0.43% | CoinGecko ID `dydx_v4`(무효)→`dydx_chain`(정확) 확인, 다회 만에 재확인 | data-source-id-corrected-recaptured |
| **BTC-USD** [⚠️ 데이터소스 정정 후 재확인] | dYdX | $7.51M | $17.47M | +0.001% | +1.27% | ETH-USD와 동일 현상 | data-source-id-corrected-recaptured |
| ETH/USD (WETH-USDC) [⚠️ 조회 실패 지속] | GMX | $23.40M(이월) | $16.14M(이월) | +0.001%(이월) | +2.21%(이월) | 올바른 ID(`gmx-perpetuals-v2-arbitrum`) 확인했으나 이번도 429 | fetch-failed-carried-forward-id-corrected |
| BTC/USD (BTC-USDC) [⚠️ 조회 실패 지속] | GMX | $7.52M(이월) | $33.60M(이월) | +0.002%(이월) | +1.23%(이월) | ETH/USD와 동일 현상 | fetch-failed-carried-forward-id-corrected |

**⚠️ 이번 회차 목록에서 제외(discontinued)**: LIT-USD(dYdX)·KAITO-USD(dYdX) — 정정된 `dydx_chain`
목록에 페어 자체가 존재하지 않아 오매핑으로 판단, 이월 중단. GIGGLE(XT.COM) — `xt_derivatives`가
정상 응답했으나 티커 자체가 사라져 상장폐지로 추정, 이월 중단.

## 테마 태그

1. **시장 전반 안정적 유지, 정밀 수치는 이번 회차도 근사치** — CoinGecko `/global` 재차 429, WebSearch 근사(총시총 약 $2.23T, BTC도미넌스 약 56.42%) (market-stable-approx-data-continues).
2. **⚠️ BANK 극적 반전(-2.38%→+10.20%)** — CEX·DEX 동조 랠리, BANK Foundation 추정 지갑 대량 이체 리스크 병존 (sharp-reversal-whale-transfer-risk).
3. **1000RATS 재차 심화, 라운드 최저치(-28.46%→-35.61%)** — 기존 Aster 8/1 상장발 왕복 패턴 지속 (deepens-further-round-low).
4. **⚠️ BICO 5회 연속 상승 종료, 급반전(+24.68%→+6.39%)** — 투기 랠리의 전형적 되돌림, funding 숏 우위 심화 (reversal-after-rally-profit-taking).
5. **AKE·KAITO 소폭 개선** — 언락 부담은 여전하나 매도압력 완화 조짐 (ake-kaito-mild-improvement).
6. **⚠️ GRAM 촉매 신규 규명** — TON GRAM 리브랜딩 + Binance·HL 동시 상장 확인 (catalyst-confirmed-gram).
7. **⚠️ BTW OI 재증가 반전** — 전회차 첫 감소가 되돌려지며 열기 지속 (oi-reaccelerates-heat-persists).
8. **CASHCAT 계속 둔화, 고위험 특성 유지** (deceleration-continues-high-risk).
9. **ADA·AAVE 상승세 꺾임** — AAVE는 플러스→마이너스 반전 (ada-aave-momentum-fades).
10. **⚠️ 데이터 인프라 대규모 정정** — dYdX ID 수정(`dydx_v4`→`dydx_chain`)으로 ETH·BTC 재확인, LIT/KAITO(dYdX) 오매핑 제외, GIGGLE(XT.COM) 상장폐지 추정 제외, GMX ID도 확인(`gmx-perpetuals-v2-arbitrum`) (data-infra-major-corrections).
11. **⚠️ OKX 거래량 산정 방식 정정** — `volCcy24h×가격`으로 재계산, 회차 간 절대치 비교 불연속 가능 (okx-volume-methodology-corrected).
12. **⚠️ 토큰화 주식 퍼프 재확인 — 전부 제외 유지** — AAPL·AMZN·AMD 등 Binance·Bybit 재확인 (tradfi-tokenized-stocks-reconfirmed-excluded).

## 데이터 신뢰도

**이번 회차 데이터 인프라에 두 가지 큰 진전이 있었다.** (a) CoinGecko 파생 거래소 ID 목록을
직접 조회한 결과 `dydx_v4`는 더 이상 유효하지 않고 **`dydx_chain`**이 정확한 ID임을 확인, 이를
통해 8~9회 연속 실패했던 ETH-USD·BTC-USD(dYdX)를 재확인했다. 다만 정정된 목록에는 LIT-USD·
KAITO-USD 페어가 존재하지 않아, 기존에 이월해오던 두 값은 잘못된 소스 매핑이었을 가능성이 높아
이번 회차부터 제외했다. (b) `xt_derivatives`도 이번 회차 처음 429 없이 정상 응답했으나 GIGGLE
티커 자체가 목록에서 사라져 상장폐지로 추정, 이월을 중단했다. GMX의 올바른 ID
(`gmx-perpetuals-v2-arbitrum` 등)도 확인했으나 이번 회차는 여전히 429로 실패해 다음 회차 재시도가
필요하다. `orangex`는 이번 회차도 429로 실패해 연속 조회 실패가 지속되고 있다.

**⚠️ OKX 거래량 산정 방식 정정**: OKX 공식 문서에 따르면 SWAP 티커의 `volCcy24h` 필드는 기초자산
(base currency) 수량 기준이며, USD 환산을 위해서는 `last` 가격을 곱해야 한다. 지난 회차들에서
일부 종목(특히 MMT)은 이 곱셈이 누락됐을 가능성이 있어, 이번 회차부터 BICO·BEAT·KAITO·CORE·
MMT·AEON·CAP 전량을 `volCcy24h × last가격`으로 일관 재계산했다. 이로 인해 **회차 간 OKX 거래량
절대치 비교는 이번 정정으로 불연속적일 수 있음**에 유의해야 한다(가격·funding·OI·24h변동%은
이 정정의 영향을 받지 않는 별도 필드이므로 추세 판단에는 문제 없음).

**funding 값 단위 관련 주의**: CEX·DEX 종목의 funding 값은 각 API가 반환한 원시 수치를 percent
스케일로 그대로 사용했다(CoinGecko `funding_rate` 필드는 percent로 직접 취급, OKX raw
`fundingRate`는 소수를 100배해 percent로 환산). 거래소·필드별 스케일 표기 관례가 다를 수 있어
**회차 간 funding 절대값 비교는 참고용으로만** 활용할 것을 권한다.

**웹서치 검증(신규)**: BANK는 BANK Foundation 추정 지갑의 8,400만 토큰 Aster 이체 정황(7월 말
보도)이 확인돼, 이번 회차 급반등 이면에 잠재 매도압력 리스크가 있음을 확인했다. GRAM은 TON
블록체인의 GRAM 리브랜딩과 Binance·Hyperliquid 동시 상장(최대 5x, 커뮤니티 요청에 의한 HL
신규상장)이 확인돼 직전 회차의 "촉매 미확인" 플래그가 해소됐다. BICO는 공식 촉매 없는 투기적
모멘텀·알트 로테이션발 랠리였음이 확인됐고, Bitkub 상장은 8/22로 아직 반영되지 않은 향후
촉매로 파악된다. 1000RATS는 신규 개별 촉매를 찾지 못했으나 기존에 확인된 Aster 8/1 상장 배경이
계속 유효한 것으로 판단된다.

한계: (a) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며,
완전한 전체 시장 스캔은 아니다; (b) OrangeX·GMX는 이번 회차도 429로 미해결이며, 연속 실패가
이어지고 있다; (c) BICO·BEAT·KAITO·CORE·MMT·AEON·CAP의 거래량은 OKX raw 필드(volCcy24h)와
가격을 곱한 근사값이며, 이번 회차부터 곱셈 방식을 일관 적용해 이전 회차 수치와 스케일이 다를 수
있다; (d) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에 따라 cex/dex 리스트에서
전부 제외했다 — AAPL·AMZN·AMD 등이 Binance·Bybit 양쪽에서 재확인됐다; (e) ASTER(CEX)·ALGO의
Bybit 레그, HYPER-USD·APEX-USD의 HL 재확인은 이번 회차 스캔에서도 포착되지 않아 일부는 이월값을
사용했다; (f) 시장 전반(총시총·도미넌스) 수치는 CoinGecko `/global` 429 실패로 이번 회차도
WebSearch 근사치를 사용했다; (g) LIT-USD·KAITO-USD(dYdX)·GIGGLE(XT.COM)은 데이터소스 정정 결과
더 이상 유효하지 않은 것으로 판단돼 이번 회차부터 목록에서 제외했다(§데이터 인프라 정정 참조).

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
