# 선물시장 스카우트 브리핑 — 2026-08-05 14:52 UTC (KST 2026-08-05 23:52)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-05T12:58:00Z)
> 로부터 약 1시간54분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`은 정상 응답 — 총시총 **$2.2827T**(직전 $2.2826T에서 거의 보합, +0.004%),
BTC도미넌스 **56.65%**(직전 56.61%에서 소폭 상승), ETH도미넌스 **9.91%**(직전 9.93%에서 소폭
하락), 24h 시총 변동 **+0.35%**(직전 +0.59%로 다소 모멘텀 둔화)로 상승 흐름은 유지하되 속도는
줄었다. Fear&Greed는 alternative.me에서 이번 회차도 **27(Fear)**로 **8회 연속 동일값** 유지 —
이례적으로 매우 긴 안정 구간이 계속되고 있다.

**✅ 데이터 인프라 업데이트**: CoinGecko OKX 계열 엔드포인트가 부분 정상화됐다 — 올바른 id
`derivatives/exchanges/okex_swap`이 이번 회차 200 OK로 응답해 **BICO·CORE·BEAT·AEON·CAP** 5종목은
CoinGecko 정상 데이터로 복귀했다(직전 회차 OKX 직접API 방식과 수치 오더가 유사해 방법론 전환에
따른 큰 왜곡은 없었던 것으로 확인). 다만 **KAITO·GRAM·GIGGLE·PIPPIN·MMT·BANK·AIO 7종목은
CoinGecko okex_swap 티커 배열에서 여전히 검색되지 않아**(명시적으로 재확인) 이 7종목은 이번
회차도 OKX 직접 API(`open24h`·`last`로 chg24 산출, `volCcy24h×last` 거래량 추정공식,
`funding-rate`·`open-interest` 개별조회) 방식을 유지했다.

- **⚠️ BANK(Lorenzo)**: 5연속 악화, CEX·DEX 둘 다 낙폭이 더 확대됐다 — CEX 가중평균
  -12.61%→**-19.671%**(Binance-19.6%·Bybit-20.1%), DEX(Aster)도 -10.46%→**-16.291%**로 함께
  더 무너졌다. 웹서치 확인: BANK는 7월 한 주간 +517% 급등 후 현재 ATH 대비 약 88% 하락, 토큰
  언락(1년 락업 종료)·레버리지 청산·약한 현물 수요가 겹친 되돌림으로 보도됨.
- **⚠️ GIGGLE**: 7연속 개선 흐름이 끝나고 플러스로 급반전 — OKX -1.25%→**+3.782%**로 부호
  자체가 바뀌었다(funding은 0.005%로 안정 유지) — 장기간 이어진 되돌림이 상승 전환으로
  마무리되는 모습(DEX 상장 미확인, CEX 항목만 존재).
- **⚠️ BLESS(Aster·OrangeX)**: 6연속 대형 상승을 이어가면서도 OrangeX funding이 5연속 심화
  흐름을 끝내고 처음으로 완화됐다 — OrangeX -0.328%→**-0.165%**로 거의 절반 수준까지 진정(가격은
  +82.94%→**+80.679%**로 여전히 극단적 상승 유지), Aster는 +83.39%→**+79.301%**로 유사 수준
  유지하되 funding은 +0.017%→**+0.041%**로 오히려 소폭 더 플러스 — 거래소 간 funding 부호가
  반대로 벌어져 단일 신호로 과신하지 않도록 주의.
- **⚠️ CASHCAT(HL/Aster)**: 직전 첫 둔화 이후 다시 재가속 — 가중평균 +28.20%→**+31.801%**
  (HL+31.64%·Aster+33.221%), Robinhood Chain 밈코인 열기가 Vlad Tenev 실적발표 언급 이후에도
  지속되는 것으로 웹서치 확인.
- **⚠️ BICO·CAP·AKE·1000RATS**: 이번 회차 공통적으로 CEX-DEX 격차가 크게 좁혀지거나 방향이
  뒤바뀌었다 — BICO 격차 2.80%p→**0.40%p**로 거의 수렴(CEX+33.064%·DEX+33.466%), CAP는 격차
  방향이 역전돼 이번엔 **DEX(+11.001%)가 CEX(+9.829%)를 앞섬**, AKE는 CEX·DEX 모두
  -2.5%대까지 수렴, 1000RATS는 CEX -6.17%→**-1.069%**(여전히 소폭 마이너스)·DEX
  -6.82%→**+0.082%**(플러스 재전환)로 4번째 방향성 사건 — 이번엔 DEX가 먼저 플러스로 넘어갔다.
- **⚠️ KAITO(OKX/HL)**: 재반등을 넘어 재가속을 이어갔다 — CEX(OKX) +3.83%→**+5.98%**, HL
  +3.98%→**+6.41%**로 두 소스가 계속 함께 상승폭을 키웠다.
- **AIO**: 급반전 이후 낙폭이 크게 줄었다(가중평균 -6.17%→**-2.553%**) — 되돌림 국면이
  진정되는 신호일 수 있다.
- **GRAM**: 3연속 플러스를 유지(OKX +1.09%→**+1.383%**, HL +1.415%→**+1.67%**) — whipsaw
  패턴이 멈춘 뒤 처음으로 3회 연속 같은 방향.

한편 **BEAT는 개선을 이어갔다**(-10.04%→**-4.968%**, CoinGecko 정상화로 재확인). **CORE는
소폭 개선**(-3.84%→**-2.77%**). **PIPPIN·MMT는 개선을 이어갔다** — PIPPIN
-3.51%→**-2.594%**, MMT -4.16%→**-0.261%**(거의 완전 보합까지 근접, funding은
-0.0312%→**-0.035%**로 소폭 더 마이너스). **ALGO는 재반전 없이 마이너스가 소폭 더 깊어졌다**
(가중평균 -1.02%→**-1.405%**). **ALLO는 근접 보합에서 강하게 플러스로 반전**했다(가중평균
-0.01%→**+2.979%**), DEX(Aster)도 +0.45%→**+1.026%**로 함께 개선됐으나 이번엔 CEX가 DEX보다
크게 앞섰다. **AAVE는 소폭 플러스를 유지**(+0.39%→**+0.437%**)했으나 HL(AAVE-USD)은
+0.259%→**-0.02%**로 거의 보합까지 식어 CEX·DEX 간 괴리가 생겼다. **ADA는 보합에서 거의
완전 보합의 미세 마이너스로 전환**됐다(+0.09%→**-0.024%**), HL도 +0.484%→**-0.16%**로 함께
전환. **ATOM은 소폭 개선을 이어갔다**(-1.47%→**-1.259%**). **ASTER(CEX)는 플러스 폭을
확대**했다(+0.28%→**+0.535%**), DEX(Aster)는 +0.31%→**+0.264%**로 거의 보합 — 이번엔 CEX가
DEX를 소폭 앞섰다. **HYPE는 OI가 소폭 줄어든 채 상승폭은 2연속 둔화를 끝내고 재가속**했다(OI
$1,253.01M→**$1,247.25M**, +2.84%→**+3.62%**). **HYPER-USD·APEX-USD(HL)는 둘 다 마이너스에서
플러스로 반전**됐다(HYPER -2.53%→**+0.94%**, APEX -0.65%→**+1.55%**). **FARTCOIN은 소폭 더
둔화**됐다(+2.71%→**+2.32%**). **ETHFI는 6연속 개선**을 이어갔다(-3.72%→**-2.18%**, 촉매는
여전히 미확인). **ANSEM·AEON-USDT(Aster)는 모두 개선을 이어갔다**(ANSEM -6.62%→**-4.856%**,
AEON-USDT -1.64%→**-0.742%**). **BTW는 재가속 4연속**을 이어갔다(+18.999%→**+20.074%**).
**dYdX funding은 계속 정상 범위 내에서 소폭 마이너스로 이동**했다(BTC 0.0%→**-0.002%**, ETH
-0.004%→**-0.001%**), 가격 상승폭은 BTC +1.01%→**+0.649%**, ETH +0.49%→**+0.338%**로 둘 다
다소 축소됐다.

## ⚠️ 데이터 인프라 이슈 — CoinGecko OKX 부분 정상화, GMX 계속 제외

`derivatives/exchanges/okex_swap`(올바른 id)이 이번 회차 200 OK로 응답해 **BICO·CORE·BEAT·
AEON·CAP** 5종목은 CoinGecko 정상 데이터로 복귀했다. 수치는 직전 회차 OKX 직접API 추정치와
오더가 유사해 방법론 전환에 따른 큰 왜곡은 없었던 것으로 판단된다(예: BICO CoinGecko $122.96M
vs 직전 추정 $121.45M).

**KAITO·GRAM·GIGGLE·PIPPIN·MMT·BANK·AIO 7종목은 CoinGecko okex_swap 티커 배열에서 명시적으로
재검색했으나 여전히 발견되지 않았다** — CoinGecko가 이 소형/신규 알트들을 아직 커버하지 않는
것으로 보인다. 이 7종목은 이번 회차도 OKX 직접 API로 우회했다(`open24h`·`last` 기반 chg24,
`volCcy24h×last` 거래량 추정공식, funding-rate·open-interest 개별조회). OI 수치는 직전 회차와
매우 근접해(예: KAITO $7.196M→$7.041M, GRAM $6.83M→$6.80M, GIGGLE $3.40M→$3.51M, PIPPIN
$1.92M→$1.94M, MMT $2.52M→$2.56M) 이 방식의 신뢰도가 유지되는 것으로 판단된다. BANK·AIO는
OKX에 상장되어 있지 않아(Binance/Bybit만) 해당 없음.

GMX(`gmx-perpetuals-v2-arbitrum`)는 다회차 연속 완전 동일 수치가 확정돼 이번 회차도 재조회하지
않고 제외 상태를 유지한다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **⚠️ BANK (Lorenzo)** [5연속 악화] | Binance/Bybit | $419.39M | $22.43M | -0.00794% | -19.671% | CEX -12.61%→-19.671%, DEX(Aster)도 -10.46%→-16.291%로 함께 더 무너짐. 웹서치: ATH대비 약 88% 하락, 토큰언락·레버리지청산·약한현물수요가 원인 | worsens-5th-round-unlock-liquidation-driven |
| **⚠️ GIGGLE (Giggle Fund)** [7연속 개선 끝, 플러스 급반전] | OKX(직접API) | $43.43M(공식추정) | $3.51M | +0.005% | +3.782% | -1.25%→+3.782%로 부호 자체가 바뀜 — 7회 연속 낙폭축소 흐름이 상승 전환으로 마무리. DEX 상장 미확인 | flips-positive-after-7-round-improvement-streak |
| **⚠️ BICO (Biconomy)** [재가속 소폭 둔화, DEX와 수렴] | OKX(CoinGecko 정상화) | $122.96M | $4.26M | -0.024% | +33.064% | +36.96%→+33.064% 소폭 둔화, funding 계속 완화. DEX(Aster +33.466%)와 격차 2.80%p→0.40%p로 거의 완전 수렴 | cex-dex-nearly-converge-coingecko-recovers |
| **⚠️ KAITO (CEX)** [재가속 지속] | OKX(직접API) | $43.74M(공식추정) | $7.04M | -0.0036% | +5.98% | +3.83%→+5.98%로 상승폭 확대, HL(+3.98%→+6.41%)도 함께 계속 커짐 | continues-reacceleration-tracks-hl |
| **⚠️ CAP** [DEX가 CEX 역전] | OKX(CoinGecko 정상화) | $18.73M | $1.58M | +0.005% | +9.829% | CEX +10.41%→+9.829% 소폭 둔화, DEX(Aster)는 +7.16%→+11.001%로 CEX를 앞질러 구도 역전 | dex-overtakes-cex-first-time |
| AIO (OlaXBT) [급반전 후 대폭 회복] | Binance/Bybit | $14.15M | $4.00M | +0.0052% | -2.553% | -6.17%→-2.553%로 낙폭 대폭 축소 — 되돌림 진정 신호 가능 | sharply-recovers-after-reversal |
| GRAM [3연속 플러스] | OKX(직접API) | $8.26M(공식추정) | $6.80M | +0.005% | +1.383% | +1.09%→+1.383% 방향유지, HL(+1.415%→+1.67%)도 함께 — whipsaw 멈춘 뒤 첫 3연속 동일방향 | third-consecutive-positive-tracks-hl |
| BEAT (Audiera) [개선 지속] | OKX(CoinGecko 정상화) | $113.44M | $7.98M | +0.003% | -4.968% | -10.04%→-4.968% 낙폭 축소 지속(CoinGecko 정상화로 재확인) | continues-improvement-coingecko-confirmed |
| CORE [소폭 개선] | OKX(CoinGecko 정상화) | $4.37M | $1.02M | -0.019% | -2.77% | -3.84%→-2.77% 소폭 개선, funding 소폭 더 마이너스 | mild-improvement-funding-slightly-deepens |
| PIPPIN [개선 지속] | OKX(직접API) | $7.44M(공식추정) | $1.94M | +0.0236% | -2.594% | -3.51%→-2.594% 낙폭 계속 축소 | continues-improvement |
| MMT (Momentum) [거의 보합 근접] | OKX(직접API) | $9.86M(공식추정) | $2.56M | -0.035% | -0.261% | -4.16%→-0.261%로 낙폭 거의 소진 | near-flat-funding-slightly-deepens |
| ALGO [방향전환 없이 심화] | Binance/Bybit | $14.77M | $16.50M | +0.00581% | -1.4053% | -1.02%→-1.405% 재flip 없이 심화 지속 | no-new-flip-negative-deepens-further |
| AKE (Akedo) [CEX·DEX 거의 수렴] | Binance/Bybit | $84.38M | $45.68M | +0.01507% | -2.4759% | CEX -4.67%→-2.476%, DEX -6.26%→-2.795%로 둘 다 개선돼 거의 동일 수준까지 수렴 | cex-dex-nearly-converge-both-improve |
| ⚠️ 1000RATS [4번째 사건, DEX 먼저 플러스] | Binance/Bybit | $137.49M | $24.52M | +0.010507% | -1.0694% | CEX -6.17%→-1.069%(여전히 마이너스), DEX(Aster)는 -6.82%→+0.082%로 완전 플러스 전환 — 두 소스 처음으로 방향이 갈림 | fourth-event-dex-flips-positive-first-cex-lags |
| ALLO (Allora) [강하게 플러스 반전] | Binance/Bybit | $22.69M | $17.17M | -0.0017% | +2.979% | -0.01%→+2.979%로 강하게 반등, DEX(Aster +0.45%→+1.026%)도 개선됐으나 CEX가 크게 앞섬 | sharply-flips-positive-outpaces-dex |
| AAVE [소폭 플러스, HL과 괴리] | Binance/Bybit | $94.53M | $94.68M | -0.0041% | +0.4368% | +0.39%→+0.437%, HL(AAVE-USD)은 +0.259%→-0.02%로 거의 보합 — CEX·DEX 괴리 | cex-holds-positive-hl-flattens-gap-opens |
| ADA [미세 마이너스 전환] | Binance/Bybit | $254.39M | $180.44M | +0.00487% | -0.02397% | +0.09%→-0.024%, HL(-0.16%)도 함께 전환 | flips-to-near-flat-negative |
| ATOM [소폭 개선] | Binance/Bybit | $17.87M | $30.87M | +0.008601% | -1.259% | -1.47%→-1.259%, HL(-1.18%)도 유사 | continues-mild-improvement |
| ASTER (CEX) [플러스 확대, DEX 앞섬] | Binance/Bybit | $14.29M | $113.42M | +0.0044% | +0.53512% | +0.28%→+0.535%, DEX(Aster +0.31%→+0.264%)는 거의 보합 — 이번엔 CEX가 앞섬 | extends-positive-outpaces-dex-this-round |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **⚠️ BLESS-USDT-PERPETUAL** [6연속 대형 상승, funding 처음 완화] | OrangeX | $295.11M | $117.42M | -0.165% | +80.679% | +82.94%→+80.679% 유지, funding -0.328%→-0.165%로 거의 절반까지 완화(5연속 심화 흐름 첫 반전) — 강한 숏스퀴즈는 지속되나 압력 다소 진정 | extends-rally-6th-round-funding-eases-first-time |
| **⚠️ BLESS-USDT** [6연속 대형 상승, funding OrangeX와 반대] | Aster | $1.01M | $0.42M | +0.041% | +79.301% | +83.39%→+79.301% 유지, funding +0.017%→+0.041%로 소폭 더 플러스 — OrangeX(-0.165%)와 부호 반대로 벌어짐, 단일 신호 과신 주의 | continues-large-swing-6th-round-funding-diverges-from-orangex |
| **⚠️ CASHCAT** [재가속] | Hyperliquid/Aster | $23.58M | $15.36M | +0.011597% | +31.801% | +28.20%→+31.801%로 재가속 — Robinhood Chain 밈코인 열기 지속(Tenev 실적발표 언급 이후) | reaccelerates-after-single-round-deceleration |
| **⚠️ 1000RATS-USDT** [CEX보다 먼저 플러스] | Aster | $0.35M | $0.05M | +0.002% | +0.082% | -6.82%→+0.082%로 CEX(-1.069%)보다 먼저 플러스 전환 — 4번째 방향성 사건 | flips-positive-ahead-of-cex |
| **⚠️ CAP-USDT** [CEX 역전] | Aster | $0.024M | $0.032M | +0.001% | +11.001% | +7.16%→+11.001%로 CEX(+9.829%)를 앞질러 구도 역전 | overtakes-cex-first-time |
| BICO-USDT [CEX와 거의 완전 수렴] | Aster | $0.88M | $0.023M | +0.0% | +33.466% | +39.76%→+33.466% 둔화, CEX(OKX +33.064%)도 둔화해 격차 거의 완전 좁혀짐 | nearly-converges-with-cex |
| **⚠️ AKE-USDT** [CEX와 수렴] | Aster | $0.69M | $11.15M | +0.006% | -2.795% | -6.26%→-2.795% 개선, CEX(-2.476%)와 거의 동일 수준까지 수렴 | nearly-converges-with-cex-both-improve |
| ASTER-USDT [대규모 OI 유지, 거의 보합] | Aster | $8.60M | $221.19M | +0.0% | +0.264% | OI $221.2M 대형 유지, +0.31%→+0.264% 거의 보합, CEX가 소폭 앞섬 | large-oi-holds-near-flat-cex-slightly-ahead |
| ANSEM [개선 지속] | Aster | $0.35M | $1.21M | +0.001% | -4.856% | -6.62%→-4.856% 낙폭 계속 축소 | continues-improvement |
| AEON-USDT [CEX와 근접, 개선] | Aster | $0.044M | $0.22M | +0.001% | -0.742% | -1.64%→-0.742% 계속 개선, CEX(-1.142%)와 근접 유지 | continues-improvement-tracks-cex |
| ALLO-USDT [CEX가 크게 앞섬] | Aster | $0.094M | $0.038M | -0.003% | +1.026% | +0.45%→+1.026% 개선됐으나 CEX(+2.979%)가 훨씬 크게 반등 | improves-but-cex-outpaces-significantly |
| **⚠️ BTW** [재가속 4연속] | Aster | $1.87M | $10.26M | +0.02% | +20.074% | +18.999%→+20.074%로 재가속 4연속, 두자릿수 상승폭 계속 확대 | reaccelerates-further-4th-round |
| **⚠️ GRAM** [CEX와 3연속 플러스] | Hyperliquid | $1.94M | $12.43M | +0.001% | +1.67% | +1.415%→+1.67%로 CEX(+1.383%)와 함께 유지 — whipsaw 멈춘 뒤 첫 3연속 | third-consecutive-positive-tracks-cex |
| HYPE-USD [OI 소폭 감소, 재가속] | Hyperliquid | $258.67M | $1,247.25M | +0.0% | +3.62% | OI $1,253.01M→$1,247.25M 감소, +2.84%→+3.62%로 2연속 둔화 끝나고 재가속 | oi-mildly-declines-reaccelerates-after-2-round-deceleration |
| HYPER-USD [플러스 반전] | Hyperliquid | $0.27M | $0.34M | -0.032% | +0.94% | -2.53%→+0.94% 반전, funding도 소폭 완화 — 저유동 변동성 | flips-positive-funding-eases-low-liquidity |
| KAITO-USD [CEX와 함께 재가속] | Hyperliquid | $4.03M | $25.08M | +0.001% | +6.41% | +3.98%→+6.41%로 CEX(+5.98%)와 함께 계속 상승폭 확대 | continues-reacceleration-tracks-cex |
| APEX-USD [플러스 반전] | Hyperliquid | $0.079M | $0.78M | +0.001% | +1.55% | -0.65%→+1.55% 반전, 저유동 소형종목 | flips-positive-low-liquidity |
| FARTCOIN [소폭 더 둔화] | Hyperliquid | $6.94M | $22.62M | +0.001% | +2.32% | +2.71%→+2.32%로 재가속 흐름 한 차례 더 주춤 | mild-deceleration-continues |
| ADA-USD [CEX와 함께 미세 마이너스] | Hyperliquid | $4.80M | $31.83M | +0.001% | -0.16% | +0.48%→-0.16%로 CEX(-0.024%)와 함께 전환 | tracks-cex-flips-near-flat-negative |
| AAVE-USD [CEX와 괴리] | Hyperliquid | $11.83M | $62.29M | -0.002% | -0.02% | +0.26%→-0.02%로 거의 보합, CEX(+0.437%)와 괴리 | flattens-diverges-from-cex |
| ATOM-USD [CEX와 유사] | Hyperliquid | $0.46M | $2.03M | +0.001% | -1.18% | -1.51%→-1.18%로 CEX(-1.259%)와 유사한 수준 | tracks-cex-stable |
| ALGO-USD [CEX와 함께 심화] | Hyperliquid | $0.64M | $2.37M | +0.001% | -1.46% | -1.16%→-1.46%로 CEX(-1.405%)와 유사한 수준으로 함께 심화 | tracks-cex-negative-deepens-together |
| ETH-USD [funding 정상범위] | dYdX | $19.24M | $18.36M | -0.001% | +0.338% | -0.004%→-0.001% 완화, 상승폭 +0.49%→+0.338% 축소 | funding-normal-range-continues |
| BTC-USD [funding 소폭 마이너스] | dYdX | $7.42M | $17.90M | -0.002% | +0.649% | 0.0%→-0.002% 소폭 마이너스 전환, 상승폭 +1.01%→+0.649% 축소 | funding-mildly-negative-still-normal-range |
| ETHFI-USD [6연속 개선] | Hyperliquid | $3.62M | $7.24M | +0.0% | -2.18% | -3.72%→-2.18% 낙폭 축소 6연속, 촉매 여전히 미확인 | continues-improvement-6th-round-catalyst-still-unclear |

## 테마 태그

1. **시장 전반: 총시총 $2.2827T(직전 $2.2826T, 거의 보합), BTC도미넌스 56.65%, ETH 9.91%, 24h 시총 변동 +0.35%(직전 +0.59%로 모멘텀 다소 둔화). Fear&Greed 27(Fear) 8연속 동일값** (market-mostly-flat-momentum-eases-fear-greed-8th-confirm).
2. **✅ CoinGecko OKX(okex_swap) 부분 정상화 — BICO·CORE·BEAT·AEON·CAP 5종목 정상 복귀, KAITO·GRAM·GIGGLE·PIPPIN·MMT·BANK·AIO 7종목은 여전히 미등재(OKX 직접API 유지)** (coingecko-okx-partial-recovery-small-caps-still-missing).
3. **⚠️ BANK 5연속 악화, CEX·DEX 둘 다 낙폭 확대** — ATH대비 88% 하락, 토큰언락·레버리지청산 (bank-worsens-5th-round-unlock-liquidation).
4. **⚠️ GIGGLE 7연속 개선 흐름 끝, 플러스로 급반전** — 부호 자체가 바뀐 첫 사례 (giggle-flips-positive-after-7-round-streak).
5. **⚠️ BLESS(Aster·OrangeX) 6연속 대형 상승 지속, OrangeX funding 첫 완화. Aster funding은 반대로 확대** — 거래소 간 funding 부호 반대 (bless-6th-round-rally-orangex-funding-eases-aster-diverges).
6. **⚠️ CASHCAT 재가속(+28.20%→+31.801%)** — Robinhood Chain 밈코인 열기 지속 (cashcat-reaccelerates-after-single-round-deceleration).
7. **⚠️ BICO·CAP·AKE·1000RATS 공통: CEX-DEX 격차 대폭 좁혀지거나 방향 역전** (multiple-symbols-cex-dex-gaps-narrow-or-reverse).
8. **⚠️ KAITO(OKX/HL) 재가속 지속(+5.98%/+6.41%)** (kaito-continues-reacceleration).
9. **AIO 급반전 후 낙폭 대폭 축소** (aio-sharply-recovers).
10. **GRAM 3연속 플러스 유지** — whipsaw 멈춘 뒤 첫 3연속 동일방향 (gram-third-consecutive-positive).
11. **BEAT·CORE·PIPPIN·MMT 모두 개선 지속** (beat-core-pippin-mmt-continue-improving).
12. **ALGO 재반전 없이 마이너스 소폭 심화 지속** (algo-no-new-flip-deepens-further).
13. **ALLO 강하게 플러스 반전(CEX가 DEX 크게 앞섬). AAVE·ADA CEX·HL 소폭 괴리, ATOM 개선 지속, ASTER(CEX) DEX 소폭 앞섬** (allo-flips-positive-aave-ada-cex-hl-diverge-aster-cex-ahead).
14. **HYPE OI 소폭 감소, 재가속. HYPER-USD·APEX-USD(HL) 둘 다 플러스 반전** (hype-reaccelerates-hyper-apex-flip-positive).
15. **ETHFI 개선 6연속** — 촉매 계속 미확인 (ethfi-continues-improvement-6th-round).
16. **⚠️ BTW 재가속 4연속** (btw-reaccelerates-4th-round).
17. **ANSEM·AEON-USDT(Aster) 개선 지속** (ansem-aeon-continue-improving).
18. **dYdX funding 소폭 마이너스로 이동(정상범위), BTC·ETH 상승폭 둘 다 소폭 축소** (dydx-funding-mildly-negative-both-up-mild-decelerate).
19. **Binance 상위 거래량 재스캔에서 다수 토큰화 주식 퍼프 상위권 재확인 — 규약에 따라 전부 제외. 완전 신규 크립토 네이티브 종목은 이번 회차 미발견** (tradfi-tokenized-stocks-excluded-no-new-native-found).
20. **⚠️ GMX 이번 회차도 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**CoinGecko OKX 부분 정상화**: 올바른 id `derivatives/exchanges/okex_swap`이 이번 회차 200 OK로
응답해 BICO·CORE·BEAT·AEON·CAP 5종목은 CoinGecko 정상 데이터로 복귀했다. 직전 회차까지 쓰던 OKX
직접 API(`open24h` 기반 chg24) 추정치와 오더가 유사해 방법론 전환에 따른 큰 왜곡은 없었던 것으로
확인된다.

**여전히 OKX 직접 API+공식 추정이 필요한 7종목**: KAITO·GRAM·GIGGLE·PIPPIN·MMT·BANK·AIO는
CoinGecko okex_swap 티커 배열에서 명시적으로 재검색했으나 여전히 발견되지 않았다(BANK·AIO는
애초에 OKX 미상장, Binance/Bybit만 해당). 나머지 5종목(KAITO·GRAM·GIGGLE·PIPPIN·MMT)은 OKX
직접 API(`open24h`·`last` 기반 chg24, `volCcy24h×last` 거래량 추정공식)를 유지했다 — OI 수치가
직전 회차와 매우 근접해(예: KAITO $7.196M→$7.041M, GRAM $6.83M→$6.80M) 이 방식의 신뢰도는
유지되는 것으로 판단된다.

**CoinGecko 파생 거래소 API**: binance_futures·bybit·hyperliquid·aster·dydx_chain·orangex_futures
모두 이번 회차 정상 응답(일부는 429 재시도 후 성공). 응답이 매우 커서(binance_futures·hyperliquid)
전량 조회 대신 관심 심볼 위주로 타겟 조회를 병행했다 — 이 경우 전체 유니버스 완전 스캔은 아니다.

**CoinGecko `/global`**: 정상 응답 확보.

**Fear&Greed**: alternative.me API로 27(Fear) 확인, 8연속 동일값으로 신뢰도 높음.

**신규 상장/급등 스캔**: Binance 상위 거래량 재스캔에서 다수의 토큰화 주식·상품 합성 퍼프가
상위권을 차지하고 있음이 재확인됐으나, 규약에 따라 리스트에서 전부 제외했다. 완전 신규 크립토
네이티브 종목은 이번 회차 발견하지 못했다.

한계: (a) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에 따라
cex/dex 리스트에서 전부 제외했다; (c) KAITO·GRAM·GIGGLE·PIPPIN·MMT 5종목의 CEX 거래량은 공식
(volCcy24h×last) 적용 추정치이며 OI는 신뢰도가 유지되나 거래량 자체는 여전히 저신뢰도다; (d)
BANK·1000RATS·ALLO·AAVE·ADA·ATOM·ASTER(CEX)·AIO·ALGO·AKE 등 복수 거래소 종목의 `chg24`
(거래량가중평균)·`funding`(거래량가중평균)은 계산값이며, 개별 거래소 값은 `why` 필드에 별도
표기했다; (e) GIGGLE은 DEX 상장을 확인하지 못해 CEX 항목만 존재한다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
