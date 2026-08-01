# 선물시장 스카우트 브리핑 — 2026-08-01 18:28 UTC (KST 2026-08-02 03:28)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·GMX·dYdX) 선물시장에서 지금 주목받는
> **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·상품·
> 프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-01T16:29:00Z)
> 로부터 약 1시간59분 경과한 정규 슬롯**이다.
>
> 이번 회차 최우선 과제였던 세 가지 데이터 미스터리가 모두 해결됐다. **① LIT(Lighter) 미스터리
> 해결**: 4회 연속 Hyperliquid 거래소 전용 엔드포인트(364페어 정밀 스캔 포함)에서 발견되지
> 않았으나, CoinGecko **통합 엔드포인트**(`/derivatives?include_tickers=unexpired`)로 재시도한
> 결과 **Hyperliquid(Futures) LIT-USD가 명확히 존재함을 확인**했다 — 거래대금 $8.33M, OI
> $75.24M, funding +0.125%, 24h **-3.14%**(직전 이월값 $2.0433/OI$75.37M과 거의 일치). 즉
> 거래소별 엔드포인트가 LIT을 누락시키는 CoinGecko 측 필터링/페이지네이션 버그였고, LIT 자체는
> 정상 거래 중이었음이 확인됐다. **② dYdX·GMX 접속 오류 원인 규명**: CoinGecko 파생거래소
> 목록을 조회한 결과 `dydx_v4`는 더 이상 유효한 ID가 아니며 **`dydx_chain`**으로, `gmx`는
> **`gmx-perpetuals-v2-arbitrum`**으로 ID가 변경돼 있었다 — 올바른 ID로 두 프로토콜 모두 정상
> 재확인 성공(향후 회차부터 이 ID 사용 권장). dYdX에서는 **LIT-USD가 극히 얇은 거래량($8.21)
> 으로 실제 존재**함도 확인됐다(사실상 비활성). **③ GIGGLE 3회 연속 미재확인 뒤 마침내 재확인**
> — XT.COM $91.13M/-8.51%·OrangeX $325.68M/-8.87%로, 직전 이월값(+17.68%)과 달리 **뚜렷한
> 하락 반전**이 확인됐다.
>
> 종목별로는 **BEAT의 랠리가 급격히 냉각**됐다 — 직전 OKX +12.314%→+17.422%·Aster
> +12.957%→+18.32%였던 상승이 이번 회차 OKX **+3.772%**·Aster **+2.175%**로 크게 둔화됐고,
> 특히 **funding이 -4.6%(OKX)로 플러스에서 마이너스로 전환**돼 숏 우위로 바뀌었다(거래량은
> 오히려 $155.75M→$216.59M로 증가, 언락 물량 소화 과정에서 대량 회전이 있었던 것으로 추정).
> **AKE는 반대로 랠리가 더 가속**됐다 — Binance +18.929%·Bybit +21.854%·Aster +22.569%로
> 상승폭이 확대됐고, 특히 **Bybit funding이 +18.9%라는 극단적 수치로 치솟아** 롱 포지션이 심하게
> 쏠려있음을 시사한다(과열 경고 신호, 조정 리스크 유의). **1000RATS는 낙폭이 크게 완화**됐다 —
> 직전 3거래소 -13~14.5% 급락에서 이번 Binance -7.575%·Bybit -7.644%로 되돌림(OKX는 이번
> 조회 목록에서 발견 안 됨). **MMT는 OKX 공개 REST API를 재조회해 거래량 단위 문제를
> 해결**했다 — `volCcy24h` 필드가 USD 환산 거래대금($408.12M)임을 확인했고, 가격도 -3.65%로
> 낙폭이 계속 좁혀졌다. **CASHCAT과 APEX(HL)는 다시 마이너스로 재반전**했다(CASHCAT HL
> -3.879%·Aster -4.784%, APEX -2.526%) — 두 종목 모두 여러 회차에 걸쳐 방향이 뒤집히는
> 노이즈성 흐름을 보이고 있어 방향성 신뢰도가 낮다. **KAITO(HL)는 완만한 개선에서 급가속**했다
> (+4.71%→**+12.10%**). **BTW는 마침내 프로젝트 정체가 확인**됐다 — 외부검색으로
> **Bitway(BTW)**, 비트코인 네이티브 L1 인프라 프로토콜로 2026년 3월 TGE 완료(바이낸스 월렛
> 부스터 프로그램 포함 시드+IDO로 $5M+ 조달)임이 밝혀졌으며, 가격은 +30.26%→**+17.169%**로
> 상승폭이 줄었으나 여전히 강세. **BULLA는 낙폭이 추가로 완화**됐다(-14.685%→**-8.82%**)나
> zachxbt 사기 의혹 등 스캠 리스크는 여전히 유효. **ALLO는 다시 근접 flat으로 되돌아갔다**
> (+2.11%→+0.125%). **AAVE·AEON·CAP은 기존 추세를 유지**했다 — AAVE는 4개 거래소에서
> -6%대로 소폭 심화 수렴(-5.14%→-6.10%), AEON은 OKX -11.392%로 완만히 추가 하락(funding
> -8.3%로 더 깊어짐), CAP은 OKX -22.035%·Aster -23.085%로 낙폭이 더 확대됐다. **HYPE·
> FARTCOIN(HL)은 소폭 되돌림 국면**(HYPE -3.22%→-2.951%로 완만한 회복 지속, FARTCOIN
> +7.13%→+5.289%로 상승폭 축소). **BTC/ETH(HL)는 이번 회차 소폭 마이너스로 전환**됐다
> (+0.094%/+0.279%→**-0.799%/-0.797%**) — 메이저 심리가 중립에서 약한 위험회피 쪽으로 살짝
> 기운 정황.

## 시장 전반

- **LIT(Lighter) 미스터리 해결** — 원인은 CoinGecko 거래소별 엔드포인트 누락, 통합 엔드포인트
  (`/derivatives?include_tickers=unexpired`)로 재확인 성공(HL LIT-USD $8.33M/OI$75.24M/
  -3.14%).
- **dYdX·GMX 접속 오류 원인 규명** — 거래소 ID 변경 발견(`dydx_v4`→**`dydx_chain`**,
  `gmx`→**`gmx-perpetuals-v2-arbitrum`**), 향후 회차부터 이 ID 사용 권장.
- **GIGGLE, 3회 연속 미재확인 뒤 마침내 재확인** — +17.68%(이월값)에서 **-8.5~-8.9%**로 반전.
- **BEAT, 랠리 급격히 냉각** — OKX +17.422%→**+3.772%**, funding 플러스→마이너스 전환(-4.6%),
  언락 물량 소화 추정.
- **AKE, 랠리 가속·Bybit funding 극단(+18.9%)** — 과열/크라우디드 롱 경고.
- **1000RATS, 낙폭 완화** — Binance/Bybit -13~14%대→**-7.6%대**.
- **MMT, 거래량 단위 문제 해결(OKX volCcy24h=USD)** — **$408.12M** 확정, 낙폭도 -5.39%→-3.65%.
- **CASHCAT·APEX(HL), 다시 마이너스로 재반전** — 여러 회차 연속 방향 뒤집힘, 신뢰도 낮은 노이즈.
- **KAITO(HL), 완만한 개선에서 급가속** — +4.71%→**+12.10%**.
- **BTW, 촉매 마침내 확인** — Bitway(BTW), 비트코인 L1 인프라, 2026년 3월 TGE.
- **BULLA, 낙폭 추가 완화되나 zachxbt 사기 의혹 등 스캠 리스크는 여전** — -14.685%→**-8.82%**.
- **ALLO, 플러스 반짝 후 재차 flat 복귀** — +2.11%→**+0.125%**.
- **AAVE, 4개 거래소 -6%대로 타이트 수렴 지속.**
- **AEON·CAP, 기존 하락 추세 지속·소폭 심화.**
- **HYPE·FARTCOIN(HL), 완만한 되돌림 국면.**
- **BTC/ETH(HL), 소폭 마이너스로 전환** — +0.094%/+0.279%→**-0.799%/-0.797%**, 메이저 심리
  약한 위험회피로 살짝 이동.
- **신규 급등 스캔**: TALUS 등 스팟 급등 종목은 추적 대상 CEX/DEX perp 어디서도 미상장 확인.
  TradFi 토큰화·레버리지ETF perp는 규약에 따라 전부 제외.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **AKE (Akedo)** [랠리 가속·funding 극단] | Binance/Bybit/Aster | $344.49M | $83.77M | +10.9%(Bybit +18.9%) | +21.12% | Binance +18.929%·Bybit +21.854%·Aster +22.569%로 가속. Bybit funding +18.9%로 극단 — 롱 쏠림 과열 신호 | rally-accelerates-bybit-funding-extreme |
| **1000RATS** [낙폭 완화] | Binance/Bybit | $772.68M | $29.24M | +1.45% | -7.61% | 직전 3거래소 -13~14.5% 급락에서 Binance -7.575%·Bybit -7.644%로 되돌림. OKX는 이번 조회 목록에서 미발견 | decline-moderates-partial-recovery |
| **BEAT (Audiera)** [랠리 급격히 냉각] | OKX/Aster | $218.40M | $12.77M | -2.5% | +2.97% | 직전 OKX +17.422%·Aster +18.32%에서 OKX +3.772%·Aster +2.175%로 상승폭 크게 둔화. funding -4.6%로 숏 우위 전환, 거래량은 오히려 증가($155.75M→$216.59M) — 언락 소화 추정 | rally-cools-sharply-post-unlock-funding-flips-negative |
| **CAP** [낙폭 추가 확대] | OKX/Aster | $49.83M | $2.74M | +0.55% | -22.56% | 직전 -19.87%에서 OKX -22.035%·Aster -23.085%로 낙폭 더 깊어짐, 반전 조짐 없이 하락 지속 | decline-continues-deepening |
| **GIGGLE** [3회 만에 재확인 — 반전] | XT.COM/OrangeX | $416.81M | $286.09M | +0.47% | -8.69% | 통합 엔드포인트로 재조회 성공. 직전 이월값(+17.68%)과 달리 XT -8.51%·OrangeX -8.87%로 뚜렷한 하락 반전 확인 | reconfirmed-after-3-rounds-reverses-to-decline |
| **BANK (Lorenzo Protocol)** [funding 완화, 가격 소폭 심화] | Binance/Bybit | $303.48M | $25.31M | -2.1% | -7.876% | Bybit funding -20.1%→-2.1%로 계속 축소되나 가격은 -5.59%→-7.876%로 다소 심화 | funding-continues-easing-price-slightly-deeper |
| **AEON** [하락 지속, funding 심화] | OKX | $28.65M | $3.09M | -8.3% | -11.39% | 직전 -10.475%에서 -11.392%로 완만히 추가 하락, funding -6.6%→-8.3%로 심화 | decline-continues-funding-deepens |
| **MMT (Momentum)** [낙폭 계속 좁혀짐, 단위 해결] | OKX(직접 API) | $408.12M | 미확보 | -0.12% | -3.65% | OKX volCcy24h 필드가 USD 환산임을 확인해 거래량 단위 문제 해소. 가격 -5.39%→-3.65%로 낙폭 지속 축소 | decline-narrows-further-volume-unit-resolved |
| KAITO [급가속] | Hyperliquid | $4.43M | $10.88M | -0.2% | +12.10% | 직전 +4.714%에서 +12.101%로 크게 가속, 상승 모멘텀 뚜렷이 강화 | rally-accelerates-sharply |
| AAVE [4거래소 타이트 수렴] | Binance/Bybit/OKX/HL | $180.66M | $173.72M | +0.3% | -6.10% | -5.14%→-6.10%로 소폭 심화되며 4개 거래소 모두 -6%대로 수렴. Bybit 역방향 이상치 재확인 불가 지속 | stable-decline-continues-all-venues-converge |
| ALLO [플러스 반짝 후 flat 복귀] | Binance/Bybit/OKX | $27.56M | $18.47M | +0.33% | +0.13% | 직전 +2.11% 플러스 전환에서 다시 근접 flat으로 되돌아감 | reverts-to-flat-after-brief-spike |
| ASTER [근접 flat, 소폭 마이너스] | Binance/Bybit/OKX | $12.08M | $122.18M | -0.27% | -0.47% | 직전 +0.14%에서 -0.466%로 미세하게 마이너스 쪽 이동, 여전히 매우 좁은 범위 | near-flat-slight-negative-tilt |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster; dYdX·GMX ID 변경 확인 후 재확인 성공)

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **LIT (Lighter)** [4회 만에 미스터리 해결] | Hyperliquid | $8.33M | $75.24M | +0.125% | -3.14% | 거래소별 엔드포인트 누락이 원인으로 규명, 통합 엔드포인트로 재확인 성공. 직전 이월값($2.0433/OI$75.37M)과 거의 일치 — 정상 거래 중이었음 확인 | mystery-resolved-via-aggregate-endpoint-source-bug-identified |
| **KAITO-USD** [급가속] | Hyperliquid | $4.43M | $10.88M | -0.2% | +12.10% | 직전 +4.714%에서 +12.101%로 급가속 | rally-accelerates-sharply |
| **BTW** [상승 유지, 촉매 확인] | Aster | $1.53M | $7.76M | +1.2% | +17.17% | +30.26%→+17.169%로 둔화됐으나 여전히 강세. 외부검색으로 Bitway(BTW) 확인 — 비트코인 L1 인프라, 2026년 3월 TGE(바이낸스 월렛 부스터 포함) | sustained-gain-catalyst-finally-identified-bitway-tge |
| **AKE-USDT** [랠리 가속] | Aster | $3.62M | $22.64M | +0.6% | +22.57% | CEX와 함께 +22.569%로 랠리 가속 재확인, Bybit funding 극단과 함께 과열 신호 | rally-accelerates-bybit-funding-extreme |
| **BULLA** [낙폭 완화, 스캠 리스크 지속] | Aster | $2.94M | $5.43M | +1.7% | -8.82% | -14.685%→-8.82%로 낙폭 계속 축소되나 여전히 마이너스. zachxbt 사기 의혹·BARSIK 전례는 유효한 리스크로 지속 | extreme-risk-memecoin-decline-continues-narrowing |
| BEAT-USDT [랠리 냉각] | Aster | $1.81M | $0.64M | -0.4% | +2.18% | OKX(+3.772%)와 함께 랠리 급격히 냉각, 직전 +18.32%에서 +2.175%로 상승폭 크게 축소 | rally-cools-sharply-post-unlock-funding-flips-negative |
| CASHCAT [재반전 — 마이너스] | Hyperliquid/Aster | $2.32M | $6.90M | +0.05% | -4.33% | 직전 HL +1.517%·Aster +0.925%에서 HL -3.879%·Aster -4.784%로 재차 마이너스 전환. 노이즈성 방향 뒤집힘 지속 | reverses-negative-again-low-directional-confidence |
| APEX-USD [재반전 — 마이너스] | Hyperliquid | $0.12M | $0.79M | +0.1% | -2.53% | 직전 +4.098%에서 -2.526%로 방향 전환, CASHCAT과 유사한 노이즈성 흐름 | reverses-negative-again-low-directional-confidence |
| CAP-USDT [낙폭 확대] | Aster | $0.19M | $0.04M | +0.1% | -23.09% | OKX(-22.035%)와 함께 낙폭 추가 확대, 하락 추세 지속 | decline-continues-deepening |
| BANK-USDT [소폭 심화] | Aster | $0.93M | $0.45M | -1.9% | -7.27% | CEX와 함께 funding 완화 지속(-2.8%→-1.9%), 가격은 -7.268%로 소폭 심화 | funding-continues-easing-price-slightly-deeper |
| ASTER-USDT [근접 flat] | Aster | $6.13M | $217.83M | +2.7% | -0.53% | CEX 계열과 함께 근접 flat 유지, 소폭 마이너스 쪽 이동. 자체 funding(+2.7%)은 CEX 평균보다 여전히 높음 | near-flat-slight-negative-tilt |
| HYPE-USD [완만한 회복] | Hyperliquid | $235.17M | $1,168.79M | +0.1% | -2.95% | 직전 -3.217%에서 -2.951%로 완만한 회복 지속 | modest-recovery-continues |
| FARTCOIN [대체로 안정] | Hyperliquid | $8.68M | $21.52M | +0.2% | +5.29% | 직전 +7.134%에서 +5.289%로 상승폭 다소 축소, 대체로 안정 유지 | no-material-change-short-term |
| **ETH-USD** [ID 변경 규명 — 재확인 성공] | dYdX | $1.02M | $14.94M | -0.1% | -1.87% | CoinGecko 거래소 ID가 `dydx_v4`→`dydx_chain`으로 변경돼 있었음을 발견, 이전 여러 회차 404의 원인 규명 | endpoint-id-changed-refresh-succeeded |
| **BTC-USD** [ID 변경 규명 — 재확인 성공] | dYdX | $2.09M | $17.10M | 0.0% | -1.17% | 동일하게 `dydx_chain` ID로 재조회 성공 | endpoint-id-changed-refresh-succeeded |
| LIT-USD (dYdX) [신규 발견, 사실상 비활성] | dYdX | $8.21 | $14,879.54 | 0.0% | -6.25% | dYdX에도 LIT-USD 페어 존재하나 거래량 $8.21로 사실상 비활성, 참고용 | newly-found-effectively-inactive |
| KAITO-USD (dYdX) [사망 확정 유지] | dYdX | $488.35 | $0.0 | 미확보 | 0.0% | 재조회 성공했으나 수치는 이전과 동일(OI $0), 사망 판정 유지 | confirmed-dead-values-unchanged |
| **ETH/USD (WETH-USDC)** [ID 변경 규명 — 재확인 성공] | GMX | $23.40M | $16.14M | +0.1% | +2.21% | CoinGecko 거래소 ID가 `gmx`→`gmx-perpetuals-v2-arbitrum`으로 변경돼 있었음을 발견. 수치는 이월값과 완전 동일 — 신선도 추가 확인 필요 | endpoint-id-changed-values-identical-freshness-unclear |
| **BTC/USD (BTC-USDC)** [ID 변경 규명 — 재확인 성공] | GMX | $7.52M | $33.60M | +0.2% | +1.23% | 동일하게 `gmx-perpetuals-v2-arbitrum` ID로 재조회 성공, 수치는 이월값과 동일 | endpoint-id-changed-values-identical-freshness-unclear |

## 테마 태그

1. **LIT(Lighter) 미스터리 해결 — 원인은 CoinGecko 거래소별 엔드포인트 누락** (mystery-resolved-via-aggregate-endpoint-source-bug-identified).
2. **dYdX·GMX 접속 오류 원인 규명 — 거래소 ID 변경**(`dydx_v4`→`dydx_chain`, `gmx`→`gmx-perpetuals-v2-arbitrum`) (endpoint-id-changed-refresh-succeeded).
3. **GIGGLE, 3회 연속 미재확인 뒤 마침내 재확인 — 반전** (reconfirmed-after-3-rounds-reverses-to-decline).
4. **BEAT, 랠리 급격히 냉각 — funding 플러스→마이너스 전환** (rally-cools-sharply-post-unlock-funding-flips-negative).
5. **AKE, 랠리 가속·Bybit funding 극단(+18.9%) — 과열 경고** (rally-accelerates-bybit-funding-extreme).
6. **1000RATS, 낙폭 완화** (decline-moderates-partial-recovery).
7. **MMT, 거래량 단위 문제 해결(OKX volCcy24h=USD)** (decline-narrows-further-volume-unit-resolved).
8. **CASHCAT·APEX(HL), 다시 마이너스로 재반전 — 노이즈성 흐름** (reverses-negative-again-low-directional-confidence).
9. **KAITO(HL), 완만한 개선에서 급가속** (rally-accelerates-sharply).
10. **BTW, 촉매 마침내 확인 — Bitway(BTW), 2026년 3월 TGE** (sustained-gain-catalyst-finally-identified-bitway-tge).
11. **BULLA, 낙폭 추가 완화되나 스캠 리스크는 여전** (extreme-risk-memecoin-decline-continues-narrowing).
12. **ALLO, 플러스 반짝 후 재차 flat 복귀** (reverts-to-flat-after-brief-spike).
13. **AAVE, 4개 거래소 -6%대로 타이트 수렴 지속** (stable-decline-continues-all-venues-converge).
14. **AEON·CAP, 기존 하락 추세 지속·소폭 심화** (decline-continues-deepening / decline-continues-funding-deepens).
15. **HYPE·FARTCOIN(HL), 완만한 되돌림 국면** (modest-recovery-continues / no-material-change-short-term).
16. **BTC/ETH(HL), 소폭 마이너스로 전환 — 메이저 심리 약한 위험회피로 이동** (majors-tilt-slightly-risk-off).
17. **신규 급등 스캔: TALUS 등 스팟 급등 종목은 추적 대상 perp에서 미상장 확인** (no-new-perp-listing-found).
18. **신규 급등 스캔: TradFi 토큰화·레버리지ETF perp 규약에 따라 전부 제외** (excluded-tokenized-stock-etf-leveraged).

## 데이터 신뢰도

이번 회차는 지난 여러 회차에 걸쳐 미해결이던 **세 가지 구조적 데이터 이슈를 모두 해결**했다.
**① LIT(Lighter)**: 4회 연속 Hyperliquid 거래소 전용 엔드포인트(`/derivatives/exchanges/
hyperliquid?include_tickers=all`, 364페어 정밀 스캔 포함)에서 발견되지 않았으나, CoinGecko
**통합 엔드포인트**(`/derivatives?include_tickers=unexpired`)로 조회하면 Hyperliquid(Futures)
LIT-USD가 명확히 존재함을 확인했다 — 거래소별 엔드포인트가 특정 종목을 누락시키는
필터링/페이지네이션 이슈였던 것으로 추정된다(CoinGecko 측 사양은 공개돼 있지 않아 정확한
메커니즘은 불명, 다음에도 동일 종목이 재발하면 통합 엔드포인트를 우선 사용할 것). **② dYdX·
GMX**: CoinGecko 파생거래소 목록(`/derivatives/exchanges?per_page=250`)을 조회해 기존 사용하던
ID `dydx_v4`·`gmx`가 더 이상 유효하지 않고 각각 `dydx_chain`·`gmx-perpetuals-v2-arbitrum`으로
변경됐음을 확인, 새 ID로 정상 재조회에 성공했다 — 이전 여러 회차의 지속적 404/429는 사실상
잘못된 ID로 인한 것이었다(향후 회차부터 새 ID 사용 필요, 이 파일의 dex 배열은 여전히
사람이 읽는 `protocol` 필드로 "dYdX"/"GMX"만 표기하고 있어 스키마 변경은 없음). 단, GMX 수치는
직전 이월값과 완전 동일해 실제 24h 회전 여부는 추가 확인이 필요하다(신선도 불명확 유의).
**③ GIGGLE**: XT.COM·OrangeX 단독 엔드포인트가 아닌 통합 엔드포인트로 재시도해 3회 연속
실패를 극복하고 재확인에 성공했다.

**MMT는 OKX 공개 REST API(`/api/v5/market/ticker`, `/api/v5/public/funding-rate`)를 재조회해
`volCcy24h` 필드가 USD 환산 거래대금임을 확인**했다 — 이전 회차까지 raw 단위 불확실로
참고용 이월했던 거래량을 이번 회차부터 $408.12M로 확정할 수 있게 됐다(정직성 표기: OI는
여전히 OKX 티커 응답에 포함되지 않아 미확보 상태 유지).

**BTW는 이번 회차 외부검색으로 프로젝트 정체를 확인**했다 — Bitway(BTW), 비트코인 네이티브
L1 인프라 프로토콜로 2026년 3월 TGE 완료(바이낸스 월렛 부스터 프로그램 포함 시드+IDO $5M+
조달)임이 밝혀져, 3회 연속 "촉매 미확인"이었던 상태를 해소했다.

**CASHCAT·APEX(HL)는 이번 회차도 방향이 뒤집혔다** — CASHCAT은 4회차 연속(하락→축소→플러스→
마이너스), APEX는 3회차 연속 방향 전환을 보이고 있어 두 종목 모두 얇은 거래량($0.12M~$2.3M)
기반의 노이즈성 흐름으로 판단, 방향성 신뢰도가 낮음을 명확히 표기한다.

**AAVE는 이번 회차도 Bybit AAVEUSD(역방향 계약) 이상치를 별도로 재조회하지 않았다** — 다음
회차에서 해당 티커를 명시적으로 재조회할 필요가 있다(우선순위 낮음, 여러 회차 미확인 지속).

한계: (a) DefiLlama `/overview/derivatives`는 이번 회차도 시도하지 않음(과거 402 확인 이력);
(b) GMX 수치는 ID 변경 후 처음 재조회했으나 직전 이월값과 완전 동일해 실제 신선도 불명확,
다음 회차 재확인 필요; (c) dYdX·GMX·LIT은 모두 이번 회차 해결됐으나 CoinGecko API의 ID
변경·엔드포인트 누락 이슈가 재발할 수 있어 향후 회차에서도 지속 모니터링 필요; (d) 1000RATS의
OKX 티커는 이번 회차 조회 목록에서 확인되지 않음(거래량 임계값 미만이거나 일시적 누락일
가능성, 원인 불명); (e) **주식화·상품·레버리지ETF 토큰**은 이번 회차도 규약에 따라
cex/dex 리스트에서 전부 제외.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
