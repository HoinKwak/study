# 선물시장 스카우트 브리핑 — 2026-08-05 08:47 UTC (KST 2026-08-05 17:47)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-05T07:03:00Z)
> 로부터 약 1시간44분 경과.**

## 이번 회차 핵심 요약

CoinGecko `/global`은 정상 응답 — 총시총 **$2.2754T**(직전 $2.2789T에서 소폭 하락, -0.15%),
BTC도미넌스 **56.55%**(직전 56.60%에서 소폭 하락), ETH도미넌스 **9.91%**(직전 9.90%에서 거의
변화 없음), 24h 시총 변동 **+0.66%**(직전 +0.75%)로 플러스는 유지하되 폭이 소폭 줄었다.
Fear&Greed는 alternative.me에서 이번 회차도 **27(Fear)**로 **5연속 동일값** 유지 — 매우
이례적으로 긴 안정 구간이 계속되고 있다.

**⚠️ OKX 개별 티커 API의 BICO·CORE·KAITO·GRAM 4종목 거래량 이상(vol24h=volCcy24h 동일값)이
이번 회차도 재현**돼(4연속) 지난 회차부터 적용한 `volCcy24h×last` 공식 추정치를 유지했다(저신뢰도
명시). **✅ 이번 회차엔 OKX 정상 6종목(BEAT·GIGGLE·PIPPIN·AEON·MMT·CAP)의 원시 vol24h/volCcy24h
값을 재대조해, 기존 브리핑이 사용해온 `volCcy24h×last` 공식이 과거 회차 수치와 정합함을 확인**했다
— 즉 정상 종목도 동일 공식으로 산출돼온 것으로 판단되며, 이번 회차도 동일 방식을 유지한다.

- **⚠️ BICO**: 4연속 재가속이 끝나고 처음으로 둔화 — OKX +35.81%→+57.88%→**+38.99%**
  (last$0.02541/open24h$0.01828)로 상승폭이 꺾였으나, funding은 오히려 -0.0922%→**-0.1071%**로
  더 심화(숏 스퀴즈 압력은 여전). Aster(BICO-USDT)도 +59.75%→**+38.90%**로 거의 동일하게 동조
  둔화됐다. 외부 뉴스 검색에서는 'BICO가 공식 발표 없이 투기적 모멘텀으로 급등'했다는 서술이
  확인됐으나 인용된 가격(약 $0.106)은 우리 소스(OKX 직접 조회 $0.02541)와 크게 달라 참고용으로만
  취급한다.
- **CORE**: 3연속 개선 흐름이 사실상 정체 — -6.04%→-4.81%→**-4.90%**로 거의 보합, funding도
  -0.0118%→**+0.0042%**로 부호가 전환(숏 우세→롱 우세)됐다.
- **GIGGLE·AEON은 개선을 이어갔고, ⚠️ PIPPIN은 3연속 개선이 깨지며 재악화** — GIGGLE -6.09%→
  **-3.84%**(4연속 개선), AEON -10.11%→**-8.05%**(Aster -8.55%와 유사 동조), PIPPIN -3.51%→
  **-7.46%**로 반전.
- **BEAT**: 재악화 흐름이 한 회차 만에 다시 개선 — OKX -12.96%→**-9.93%**, DEX(Aster)는
  -21.48%→**-11.30%**로 훨씬 크게 회복해 CEX·DEX 괴리(8.52%p→**1.37%p**)가 크게 좁혀졌다 —
  8/1 $67.8M 언락 후유증이 진정되는 모습이나 확정은 아니다.
- **MMT**: 직전 급락에서 소폭 회복 — -6.60%→**-5.62%**, funding은 -0.0707%→**-0.0745%**로
  오히려 더 심화.
- **⚠️ CAP**: CEX가 플러스로 재반전했으나 DEX는 여전히 마이너스 — CEX -2.43%→**+0.33%**,
  DEX(Aster) -4.92%→**-0.51%**로 부호가 엇갈린다(격차는 2.49%p→**0.84%p**로 축소).
- **⚠️ ALGO**: 4회째 방향전환으로 다시 플러스 전환 — 가중평균 -1.25%→**+0.07%**(Binance-0.06%·
  Bybit+0.47%), HL도 -1.08%→**+0.16%**로 동조.
- **⚠️ BANK**: CEX·DEX 괴리가 해소되고 수렴 — CEX 가중평균 +26.91%→**+18.69%**(Binance+18.71%·
  Bybit+18.53%)로 4연속 둔화, DEX(Aster)도 +28.91%→**+19.24%**로 함께 큰 폭 조정돼 격차가
  0.55%p로 좁혀졌다.
- **⚠️ 1000RATS**: 3연속 개선이 크게 꺾이며 DEX와 괴리 재발생 — CEX 가중평균 -6.92%→**-12.16%**
  (Binance-11.56%·Bybit-13.92%), DEX(Aster) -7.99%→**-8.29%**로 소폭만 악화해 이번엔 CEX가
  DEX보다 훨씬 크게 떨어졌다.
- **⚠️ BLESS-USDT(Aster)**: 3연속 큰 폭 상승 확대 — +29.01%→+49.27%→**+61.63%**. **이번 회차
  핵심: OrangeX(BLESS-USDT-PERPETUAL)가 4연속 429 실패 끝에 드디어 정상 응답**했고, 직전
  이월값(-13.19%)에서 **+61.38%**로 극적으로 반전해 Aster(+61.63%)와 거의 완전히 일치 — 4회 만에
  두 소스 간 방향 비교가 가능해졌고, 저유동 노이즈보다 실제 강세일 가능성이 높아졌다(funding도
  -0.086%로 크게 심화, 숏 스퀴즈 시사).
- **⚠️ CASHCAT**: 4연속 둔화가 끝나고 재가속 — 가중평균 +17.34%→**+25.55%**(HL+25.55%·
  Aster+25.61%)로 Robinhood Chain 밈코인 열기가 다시 살아났다.
- **⚠️ BTW**: 4연속 진정 흐름이 깨지고 재가속 — +9.35%→**+16.60%**로 두자릿수 복귀.

한편 **AKE는 재가속**됐다(가중평균 +1.91%→**+3.52%**, DEX도 +1.15%→**+3.80%**로 동조 재가속),
**ALLO는 보합에서 플러스로 전환**됐다(-0.84%→**+1.88%**, DEX도 -0.78%→**+2.21%**로 동조),
**AAVE는 보합권 유지**(-1.07%→**-1.13%**), **ADA는 whipsaw가 크게 진정돼 거의 평탄**해졌다
(-3.06%→**-0.24%**, HL -0.42%도 유사), **ATOM은 소폭 재악화하나 안정 범위**(-1.29%→**-1.74%**)가
이어졌다. **ASTER(CEX·DEX)는 계속 거의 0%로 보합권에 수렴**했다(CEX -0.56%·Aster -0.54%, HL은
이번 회차 재조회 안 함). **⚠️ AIO는 두자릿수 강세에서 크게 둔화**돼 +13.07%→**+5.60%**로
상승폭이 절반 이하로 축소, 두자릿수에서 벗어났다(Falcon Finance 내러티브 모멘텀이 식는 모습).
**ANSEM은 개선이 2연속 이어졌다**(-7.64%→**-5.73%**). **⚠️ HYPER-USD(HL)는 안정화 흐름이 반전돼
재악화**됐다 — -3.85%→**-5.18%**, funding도 -0.032%→**-0.038%**로 다시 심화, 저유동 소형종목
변동성 지속. **ETHFI는 개선이 3연속 이어졌다**(-7.99%→**-6.71%**, 촉매는 여전히 미확인). **HYPE는
대형 OI가 더 커진 채 상승폭이 확대**됐다($1.259B→**$1.267B**, +4.69%→**+5.25%**). **dYdX
funding은 계속 정상 범위**를 유지했다(BTC 0.0%→**-0.001%**, ETH -0.003%→**-0.003%**로 동일),
가격은 BTC +0.66%→**+0.94%**·ETH +0.37%→**+0.67%**로 상승폭이 확대됐다.

Binance·Bybit 상위 거래량 재스캔에서 이번 회차도 **토큰화 주식 퍼프가 관측되지 않았다**(감시 종목
범위 내 확인이며 완전 전수조사는 아니다).

## ⚠️ 데이터 인프라 이슈 — OKX 거래량 이상값 4연속·방법론 정합성 재확인 · OrangeX 재확인 성공 · GMX 계속 제외

OKX 개별 티커 API에서 **BICO·CORE·KAITO·GRAM 4종목**이 이번 회차도 `vol24h`와 `volCcy24h`가
완전 동일값으로 반환됐다(4회 연속 재현). 지난 회차부터 적용한 `volCcy24h×last` 공식 추정치를
이번 회차도 유지했다(저신뢰도 명시). 이번 회차엔 정상 검증된 6종목(BEAT·GIGGLE·PIPPIN·AEON·MMT·
CAP)의 원시값을 재대조해, 동일 공식이 과거 회차 저장값과 잘 정합함을 확인했다 — 방법론에 대한
신뢰도가 다소 높아졌다.

**OrangeX(BLESS-USDT-PERPETUAL)는 4연속 429 실패 끝에 이번 회차 드디어 정상 응답**을 받았다.
직전 이월값(-13.19%)에서 +61.38%로 극적으로 반전해 Aster BLESS-USDT(+61.63%)와 거의 완전히
일치했다 — 4회 만에 두 소스 간 방향 비교가 가능해졌다.

GMX(`gmx-perpetuals-v2-arbitrum`)는 다회차 연속 완전 동일 수치가 확정돼 이번 회차도 재조회하지
않고 제외 상태를 유지한다.

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **⚠️ BICO (Biconomy)** [4연속 재가속 끝, 첫 둔화] | OKX(직접API) | $123.25M(공식추정) | $4.95M | -0.1071% | +38.99% | +35.81%→+57.88%→+38.99%로 5회 만에 첫 둔화, funding은 오히려 -0.1071%로 더 심화. Aster도 +38.90%로 동조. ⚠️거래량 이상 4연속, 공식 적용 추정치 유지 | first-deceleration-after-4-round-rally-funding-still-deepens |
| BANK (Lorenzo) [⚠️ CEX·DEX 괴리 해소, 수렴] | Binance/Bybit | $571.49M | $24.26M | +0.0108% | +18.69% | CEX 가중평균 +26.91%→+18.69%(Binance+18.71%·Bybit+18.53%)로 4연속 둔화, DEX(Aster)도 +28.91%→+19.24%로 함께 큰 폭 조정 — 격차 0.55%p로 수렴 | decelerates-4th-round-converges-with-dex |
| **⚠️ 1000RATS** [3연속 개선 반납, DEX와 괴리] | Binance/Bybit | $141.46M | $23.65M | +0.0083% | -12.16% | -6.92%→-12.16%(가중평균; Binance-11.56%·Bybit-13.92%)로 3연속 개선 흐름이 크게 꺾임, DEX(Aster -8.29%)보다 낙폭이 훨씬 커져 다시 괴리 발생 | worsens-breaks-3-round-improvement-diverges-from-dex-again |
| **⚠️ AIO (OlaXBT)** [두자릿수 강세에서 크게 둔화] | Binance/Bybit | $21.97M | $4.40M | +0.005% | +5.60% | +13.07%→+5.60%(가중평균; Binance+5.54%·Bybit+6.31%)로 상승폭 절반 이하로 축소, 두자릿수에서 벗어났다. Falcon Finance 내러티브 모멘텀 식는 모습 | sharp-deceleration-exits-double-digit |
| **⚠️ CAP** [CEX 플러스 반전, DEX와 부호 갈림] | OKX(직접API) | $11.96M | $1.27M | +0.005% | +0.33% | CEX -2.43%→+0.33%로 플러스 전환됐으나 DEX(Aster) -4.92%→-0.51%는 여전히 마이너스 — 부호 엇갈림(격차 2.49%p→0.84%p로 축소) | cex-flips-positive-dex-still-negative |
| PIPPIN [⚠️ 3연속 개선 깨지고 재악화] | OKX(직접API) | $11.62M | $1.93M | +0.0282% | -7.46% | -6.68%→-3.51%→-7.46%로 3연속 개선 흐름이 갑자기 반납 | worsens-breaks-3-round-improvement |
| BEAT (Audiera) [재악화 끝, DEX 괴리 크게 축소] | OKX(직접API) | $159.54M | $8.23M | +0.005% | -9.93% | -9.89%→-12.96%→-9.93%로 개선 복귀, DEX(Aster)도 -21.48%→-11.30%로 크게 회복 — 괴리 8.52%p→1.37%p로 축소. 8/1 언락 후유증 진정 국면 추정 | recovers-dex-gap-narrows-sharply |
| CORE [개선 정체, funding 부호 전환] | OKX(직접API) | $5.55M(공식추정) | $1.01M | +0.0042% | -4.90% | -6.04%→-4.81%→-4.90%로 3연속 개선 흐름 정체, funding -0.0118%→+0.0042%로 부호 전환. ⚠️거래량 이상 4연속 | improvement-streak-stalls-funding-flips-sign |
| KAITO (CEX) [플러스 지속] | OKX(직접API) | $43.59M(공식추정) | $7.27M | +0.005% | +4.19% | +3.70%→+4.19%, HL(+4.04%)도 동조 지속. ⚠️거래량 이상 4연속 | continues-positive-tracks-hl |
| GRAM [⚠️ 4회째 재반전, 마이너스로] | OKX(직접API) | $11.92M(공식추정) | $6.86M | +0.005% | -0.07% | +0.29%→-0.07%, HL(+0.12%→-0.36%)도 동조 재반전 — whipsaw 계속. ⚠️거래량 이상 4연속 | flips-negative-again-4th-flip-tracks-hl |
| GIGGLE (Giggle Fund) [4연속 개선] | OKX(직접API) | $47.62M | $3.48M | +0.005% | -3.84% | -6.58%→-6.09%→-3.84%로 낙폭 축소 4연속 | continues-improvement-4th-round |
| AEON [개선 지속] | OKX(직접API) | $15.33M | $2.48M | +0.005% | -8.05% | -10.11%→-8.05%, Aster(-8.55%)와 유사 동조 | continues-improvement-tracks-aster |
| MMT [급락 후 소폭 회복] | OKX(직접API) | $10.11M | $2.50M | -0.0745% | -5.62% | -6.60%→-5.62%로 직전 급락에서 소폭 회복, funding은 오히려 더 심화 | mild-recovery-after-sharp-drop-funding-deepens |
| ⚠️ ALGO [4회째 재반전, 플러스로] | Binance/Bybit | $16.43M | $16.81M | +0.0083% | +0.07% | -1.25%→+0.07%(가중평균; Binance-0.06%·Bybit+0.47%)로 재반전, HL(+0.16%)도 동조 | flips-positive-again-4th-flip-tracks-hl |
| AKE (Akedo) [재가속] | Binance/Bybit | $107.42M | $47.85M | +0.0102% | +3.52% | +1.91%→+3.52%(가중평균), DEX(+3.80%)도 함께 재가속 | reaccelerates-tracks-dex |
| ALLO (Allora) [플러스 전환] | Binance/Bybit | $21.74M | $17.28M | -0.0031% | +1.88% | -0.84%→+1.88%(가중평균), DEX(+2.21%)도 함께 전환 | flips-positive-tracks-dex |
| AAVE [보합권 유지] | Binance/Bybit | $97.53M | $96.30M | +0.0008% | -1.13% | -1.07%→-1.13%(가중평균), HL(-1.05%)도 유사 — 거의 변화 없음 | stable-near-flat |
| ADA [whipsaw 크게 진정] | Binance/Bybit | $215.20M | $178.98M | +0.01% | -0.24% | -3.06%→-0.24%(가중평균)로 낙폭 크게 축소, HL(-0.42%)도 유사 — 거의 평탄 | sharp-improvement-near-flat |
| ATOM [소폭 재악화, 안정 범위] | Binance/Bybit | $23.10M | $31.11M | +0.01% | -1.74% | -1.29%→-1.74%(가중평균), HL(-1.13%)도 유사 — 안정 범위 지속 | mild-worsening-stable-range |
| ASTER (CEX) [보합권 유지] | Binance/Bybit | $14.63M | $112.70M | +0.005% | -0.56% | -0.40%→-0.56%, DEX(Aster -0.54%)도 거의 동일 수준 수렴 | continues-near-flat-converges-dex |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

> GMX는 데이터 정체 확정으로 계속 제외(재조회 안 함).

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **⚠️ BLESS-USDT-PERPETUAL** [4연속 재확인 실패 끝, 극적 반전] | OrangeX | $149.47M | $69.80M | -0.086% | +61.38% | CoinGecko orangex_futures 이번 회차 드디어 정상 응답 — 직전 이월값(-13.19%)에서 +61.38%로 급반전, Aster(+61.63%)와 거의 완전 일치. funding도 크게 심화(숏 스퀴즈 시사) | recheck-succeeds-large-reversal-converges-aster |
| **⚠️ BLESS-USDT** [3연속 큰 폭 상승 확대] | Aster | $0.56M | $0.31M | +0.005% | +61.63% | +29.01%→+49.27%→+61.63% 급등 3회 연속 확대, OrangeX와 방향 거의 완전 일치 — 저유동 노이즈보다 실제 강세 가능성 상승 | continues-large-swing-3rd-round-orangex-confirms |
| **⚠️ CASHCAT** [4연속 둔화 끝, 재가속] | Hyperliquid/Aster | $20.71M | $15.85M | +0.0128% | +25.55% | 가중평균 +17.34%→+25.55%(HL+25.55%·Aster+25.61%) — 4연속 둔화 흐름이 깨지고 재가속, Robinhood Chain 밈코인 열기 재점화 | reaccelerates-breaks-4-round-deceleration |
| **⚠️ BTW** [4연속 진정 끝, 재가속] | Aster | $1.61M | $9.27M | +0.011% | +16.60% | +9.35%→+16.60%로 4연속 진정 흐름이 깨지고 두자릿수 복귀 | reaccelerates-breaks-4-round-deceleration |
| **BANK-USDT** [CEX와 수렴] | Aster | $1.38M | $0.43M | +0.001% | +19.24% | +28.91%→+19.24%로 큰 폭 조정, CEX(+18.69%)와 거의 같은 수준으로 수렴 — 직전 방향 엇갈림 해소 | converges-with-cex-divergence-resolved |
| **⚠️ 1000RATS-USDT** [CEX와 괴리 재발생] | Aster | $0.38M | $0.055M | +0.002% | -8.29% | -7.99%→-8.29%로 소폭만 악화, CEX(-12.16%)가 훨씬 크게 떨어지며 다시 괴리 발생 — 이번엔 DEX가 CEX보다 덜 약세 | cex-worsens-more-diverges-again |
| **⚠️ CAP-USDT** [CEX와 부호 갈림] | Aster | $0.030M | $0.032M | +0.001% | -0.51% | -4.92%→-0.51%로 크게 개선했으나 CEX(+0.33%)는 플러스 전환 — 부호 엇갈림(격차 2.49%p→0.84%p로 축소) | improves-but-cex-flips-positive-sign-split |
| **BICO-USDT** [CEX와 함께 첫 둔화] | Aster | $0.80M | $0.012M | -0.001% | +38.90% | CEX(+38.99%)와 거의 동일하게 상승폭 크게 꺾임 — 4연속 재가속 이후 첫 둔화 | tracks-cex-first-deceleration |
| **⚠️ GRAM** [CEX와 함께 4회째 재반전] | Hyperliquid | $2.17M | $12.44M | +0.001% | -0.36% | +0.12%→-0.36%로 CEX(-0.07%)와 함께 다시 마이너스로 전환 — whipsaw 계속 | flips-negative-again-tracks-cex-4th-flip |
| **⚠️ HYPER-USD** [안정화 흐름 반전, 재악화] | Hyperliquid | $0.27M | $0.33M | -0.038% | -5.18% | -3.85%→-5.18%로 안정화가 깨지고 재악화, funding도 -0.032%→-0.038%로 다시 심화. 저유동 소형종목 변동성 지속 | reverses-stabilization-worsens-again |
| AKE-USDT [CEX와 함께 재가속] | Aster | $0.79M | $11.57M | +0.006% | +3.80% | CEX(+3.52%)와 함께 상승폭 확대 | tracks-cex-reaccelerates |
| ASTER-USDT [대규모 OI 유지] | Aster | $9.08M | $221.10M | +0.011% | -0.54% | OI $221.1M 대형 유지, CEX(-0.56%)와 계속 수렴 | near-flat-large-oi-converges-cex |
| ANSEM [2연속 개선] | Aster | $0.34M | $1.15M | +0.001% | -5.73% | -7.64%→-5.73%로 낙폭 축소 2회 연속 | continues-improvement-2nd-round |
| AEON-USDT [CEX와 계속 동조] | Aster | $0.087M | $0.22M | +0.01% | -8.55% | CEX(-8.05%)와 유사한 수준 유지하며 동조 | tracks-cex-continues |
| ALLO-USDT [CEX와 함께 플러스 전환] | Aster | $0.10M | $0.036M | -0.004% | +2.21% | CEX(+1.88%)와 함께 상승 전환 | tracks-cex-flips-positive |
| HYPE-USD [대형 OI 확대, 상승폭 확대] | Hyperliquid | $262.98M | $1,266.97M | 0.0% | +5.25% | OI $1.267B로 소폭 더 커진 채 +4.69%→+5.25%로 상승폭 확대 | steady-large-oi-continues-accelerating |
| KAITO-USD [CEX와 함께 플러스 지속] | Hyperliquid | $4.11M | $24.98M | +0.001% | +4.04% | CEX(+4.19%)와 함께 소폭 상승 지속 | tracks-cex-continues-positive |
| ADA-USD [CEX와 함께 크게 개선] | Hyperliquid | $4.20M | $32.27M | +0.001% | -0.42% | CEX(-0.24%)와 함께 낙폭이 크게 축소돼 거의 보합권 진입 | tracks-cex-sharp-improvement |
| APEX-USD [상승폭 크게 축소] | Hyperliquid | $0.15M | $0.79M | +0.001% | +0.10% | +1.27%→+0.10%로 거의 보합까지 둔화, 저유동 소형종목 노이즈 가능성 | low-liquidity-decelerates-still-positive |
| FARTCOIN [상승폭 지속 확대] | Hyperliquid | $5.38M | $24.28M | +0.001% | +3.21% | +2.75%→+3.21%로 재가속 흐름 지속 | continues-reaccelerating |
| AAVE-USD [CEX와 유사] | Hyperliquid | $10.45M | $63.97M | +0.001% | -1.05% | CEX(-1.13%)와 거의 동일, OI $64.0M 대형 유지 | tracks-cex-near-flat |
| ATOM-USD [CEX와 유사] | Hyperliquid | $0.65M | $2.05M | +0.001% | -1.13% | CEX(-1.74%)보다 소폭 나은 수준, 안정 지속 | tracks-cex-stable |
| ALGO-USD [CEX와 함께 4회째 재반전] | Hyperliquid | $0.85M | $2.41M | +0.001% | +0.16% | CEX(+0.07%)와 함께 다시 플러스로 전환 — whipsaw 계속 | flips-positive-again-tracks-cex-4th-flip |
| **ETH-USD** [funding 정상범위 유지] | dYdX | $5.23M | $20.55M | -0.003% | +0.67% | -0.003%로 동일 유지, 가격 상승폭 확대(+0.37%→+0.67%) | funding-normal-range-continues |
| **BTC-USD** [funding 정상범위 유지] | dYdX | $7.63M | $17.83M | -0.001% | +0.94% | 0.0%→-0.001%로 소폭 마이너스 전환했으나 정상 범위, 가격 상승폭 확대(+0.66%→+0.94%) | funding-normal-range-continues |
| **ETHFI-USD** [개선 3연속] | Hyperliquid | $4.54M | $7.29M | +0.001% | -6.71% | -7.99%→-6.71%로 낙폭 축소 3연속, 촉매는 여전히 미확인 | continues-improvement-3rd-round-catalyst-still-unclear |

## 테마 태그

1. **시장 전반: 총시총 $2.2754T(직전 $2.2789T에서 소폭 하락, -0.15%), BTC도미넌스 56.55%, ETH 9.91%, 24h 시총 변동 +0.66%(직전 +0.75%)로 플러스 유지하되 폭 축소. Fear&Greed 27(Fear) 5연속 동일값** (market-mild-pullback-fear-greed-5th-confirm).
2. **⚠️ BICO 4연속 재가속 끝나고 첫 둔화(+57.88%→+38.99%)** — funding은 오히려 -0.1071%로 더 심화, Aster도 +38.90%로 동조 둔화 (bico-first-deceleration-after-4-round-rally).
3. **CORE 3연속 개선 정체, funding 부호 전환(숏→롱 우세)** (core-improvement-stalls-funding-flips).
4. **GIGGLE 4연속 개선, AEON 개선 지속. ⚠️ PIPPIN은 3연속 개선 깨지고 재악화** (giggle-aeon-improve-pippin-reverses).
5. **BEAT 재악화 끝, DEX(-21.48%→-11.30%)와 CEX(-12.96%→-9.93%) 괴리 8.52%p→1.37%p로 크게 축소** (beat-recovers-dex-gap-narrows).
6. **MMT 직전 급락에서 소폭 회복, funding은 더 심화** (mmt-mild-recovery-funding-deepens).
7. **⚠️ CAP CEX 플러스 반전(+0.33%)했으나 DEX(-0.51%)는 여전히 마이너스 — 부호 갈림** (cap-cex-flips-positive-dex-negative).
8. **⚠️ ALGO 4회째 방향전환, 다시 플러스로 재반전** (algo-flips-positive-4th-flip).
9. **⚠️ BANK CEX·DEX 괴리 해소, 거의 완전 수렴(18.69%/19.24%)** (bank-converges-divergence-resolved).
10. **AKE 재가속(+1.91%→+3.52%), DEX도 동조 재가속** (ake-reaccelerates-tracks-dex).
11. **⚠️ 1000RATS 3연속 개선 크게 반납(-12.16%), DEX와 괴리 재발생(이번엔 CEX가 더 약세)** (rats-worsens-diverges-again).
12. **ALLO 보합에서 플러스 전환(+1.88%), DEX도 동조. AAVE 보합권 유지. ADA whipsaw 크게 진정(거의 평탄). ATOM 소폭 재악화하나 안정범위** (allo-aave-ada-atom-mostly-stabilizing).
13. **ASTER(CEX·DEX) 계속 거의 0%로 보합권 수렴(HL 이번 회차 미조회)** (aster-cex-dex-continue-converge-flat).
14. **⚠️ AIO 두자릿수 강세에서 크게 둔화(+13.07%→+5.60%)** — Falcon Finance 내러티브 모멘텀 식는 모습 (aio-sharp-deceleration-exits-double-digit).
15. **⚠️ CASHCAT 4연속 둔화 끝, 재가속(+17.34%→+25.55%)** — Robinhood Chain 밈코인 열기 재점화 (cashcat-reaccelerates-breaks-4-round-deceleration).
16. **⚠️ BTW도 4연속 진정 끝, 재가속(+9.35%→+16.60%)** (btw-reaccelerates-breaks-4-round-deceleration).
17. **⚠️ BLESS-USDT(Aster) 3연속 큰 폭 상승 확대(+49.27%→+61.63%) — OrangeX 4연속 429 실패 끝에 재확인 성공, +61.38%로 방향 거의 완전 일치(4회 만에 비교 가능)** (bless-3rd-round-large-swing-orangex-recheck-succeeds-converges).
18. **ANSEM 개선 2연속** (ansem-continues-improvement-2nd-round).
19. **HYPE 대형 OI 확대($1.267B), 상승폭 확대(+4.69%→+5.25%)** (hype-oi-expands-accelerates).
20. **⚠️ HYPER-USD(HL) 안정화 흐름 반전, 재악화(-3.85%→-5.18%), funding 재심화** (hyper-reverses-stabilization-worsens).
21. **ETHFI 개선 3연속** — 촉매 계속 미확인 (ethfi-continues-improvement-3rd-round).
22. **dYdX funding 정상범위 계속 유지, 가격 상승폭 확대** (dydx-funding-normal-price-accelerates).
23. **⚠️ OKX 개별 티커 BICO·CORE·KAITO·GRAM 거래량 이상 4연속 재현 — 공식(volCcy24h×last) 적용 추정치 유지(저신뢰도), 정상 6종목도 동일 공식 정합성 재확인** (okx-volume-anomaly-4th-round-formula-methodology-confirmed).
24. **Binance·Bybit 상위 거래량 재스캔에서 이번 회차도 토큰화 주식 퍼프 미관측(감시 범위 내, 완전 전수조사 아님)** (tradfi-tokenized-stocks-not-observed-this-round).
25. **⚠️ GMX 이번 회차도 계속 제외** (gmx-still-excluded-no-recheck).

## 데이터 신뢰도

**OKX 개별 티커 API 거래량 이상값(4연속 재현, 방법론 정합성 재확인)**: BICO·CORE·KAITO·GRAM
4종목에서 이번 회차도 `vol24h`와 `volCcy24h`가 완전 동일한 값으로 반환됐다(4회 연속). 지난
회차부터 적용해온 `volCcy24h×last` 공식 추정치를 이번 회차도 유지했다(저신뢰도 명시). 이번
회차엔 정상 검증된 6종목(BEAT·GIGGLE·PIPPIN·AEON·MMT·CAP)의 원시 vol24h/volCcy24h 값을
직접 재대조해, 동일 공식이 과거 회차 저장값과 잘 정합함을 확인했다 — 방법론에 대한 신뢰도가
다소 높아졌으나, BICO·CORE·KAITO·GRAM 4종목은 근본적인 API 이상값이 해소되지 않은 만큼 여전히
저신뢰도로 표기한다.

**OKX OI·funding 별도 엔드포인트는 정상**: `/public/open-interest`(oiUsd)·`/public/funding-rate`
(fundingRate)는 이상 4종목을 포함해 10개 심볼(BICO·CORE·KAITO·GRAM·BEAT·GIGGLE·PIPPIN·AEON·
MMT·CAP) 전체 개별 조회로 신선한 원시값을 확보했다.

**CoinGecko 파생 거래소 API**: binance_futures·bybit·hyperliquid·aster는 정상 응답. dydx_chain은
4차례 429 이후 재시도로 성공. **orangex_futures는 4연속 429 실패 끝에 이번 회차 정상 응답**을
받아 BLESS-USDT-PERPETUAL 신선값을 확보했다(4회 만의 재확인 성공).

**CoinGecko `/global`**: 정상 응답(1회 조회로 확보).

**Fear&Greed**: alternative.me API로 27(Fear) 확인, 5연속 동일값으로 신뢰도 높음.

**신규 상장/급등 스캔**: Binance·Bybit 상위 거래량 재스캔에서 이번 회차도 토큰화 주식·상품 합성
퍼프가 관측되지 않았다. 다만 이는 기존 감시 종목·상위 리스트 범위 내 스캔 결과이며 전체 심볼
목록을 전수조사한 것은 아니므로 완전한 부재를 단정하지는 않는다. 완전 신규 크립토 네이티브
종목은 이번 회차 발견하지 못했다.

한계: (a) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며 완전한
전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번 회차도 규약에 따라
cex/dex 리스트에서 전부 제외했다; (c) BICO·CORE·KAITO·GRAM 4종목의 CEX 거래량은 공식
(volCcy24h×last) 적용 추정치이며 여전히 저신뢰도다(근본 원인인 API 이상값이 4연속 미해소); (d)
BANK·1000RATS·ALLO·AAVE·ADA·ATOM·ASTER(CEX)·AIO·ALGO·AKE 등 복수 거래소 종목의 `chg24`
(거래량가중평균)·`funding`(거래량가중평균)은 계산값이며, 개별 거래소 값은 `why` 필드에 별도
표기했다; (e) ASTER의 Hyperliquid 값은 이번 회차 재조회하지 않아 직전 회차 이후 갱신되지 않았다
(다음 회차 재확인 필요).

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
