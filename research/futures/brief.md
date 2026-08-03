# 선물시장 스카우트 브리핑 — 2026-08-03 10:29 UTC (KST 2026-08-03 19:29)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-03T08:29:00Z)
> 로부터 정확히 2시간 경과.**

CoinGecko `/global`로 총 시총 **$2.24T**(-0.62% 24h), BTC 도미넌스 **56.21%**, ETH 도미넌스
**9.96%**를 확보했다 — 직전 회차($2.226T, -1.13%, 56.16%)보다 낙폭이 뚜렷이 줄어 시장이 소폭
반등하는 모습이다. OKX BTC-USDT-SWAP 직접 조회로 BTC **-0.80%**(직전 -1.56%)를 확인했고, HL
BTC-USD -0.70%·dYdX BTC-USD -0.73%와도 대체로 정합해 완만한 반등이 재확인된다.

## ⭐ 이번 회차 핵심: 3개 데이터 소스(dYdX·GMX·OrangeX) 동시 복구

세 소스 모두 **이전 회차에 시도했던 CoinGecko exchange id가 틀렸음**을 확인해 복구했다.

- **dYdX**: 올바른 id는 `dydx_chain`(밑줄) — 직전 회차 웹서치로 찾았던 하이픈 버전(`dydx-chain`)은
  오답이었다. 3회 연속 실패 후 처음으로 119개 티커 전체를 확보했다.
- **GMX**: 올바른 id는 `gmx-perpetuals-v2-arbitrum` — 7회 연속 실패 후 복구했는데, ETH/USD
  [WETH-USDC]·BTC/USD[BTC-USDC] 모두 그동안 이월해온 값과 **완전히 동일**했다. 이는 데이터
  수집 실패가 아니라 해당 GMX 마켓이 실제로 매우 낮은 활동성으로 장기간 정체돼 있었을 가능성을
  시사한다.
- **OrangeX**: 올바른 id는 `orangex_futures` — 복구 결과 BLESS-USDT-PERPETUAL이 이월값
  +69.45%에서 **+31.35%로 크게 냉각**됐음을 확인했고, 이는 Aster의 BLESS-USDT(+33.09%)·
  XT.COM의 BLESS_USDT(+29.56%)와 3개 소스 모두 +29~33% 범위로 수렴해 신뢰도가 높다.

**LIT-USD(dYdX)는 6~7회 연속 완전 동결이 이번에 처음 깨졌다**(vol $90.92→$14.31, OI
$14,551.64→$14,718.01, chg -1.59%→+1.14%로 모두 변화). 반면 **KAITO-USD(dYdX)는 이번에도
정확히 동일값**(vol $488.35·OI $0·chg 0%)을 유지해 여전히 진짜 죽은 시장으로 재확인된다.

**⚠️ 새로운 이슈: XT.COM에서 GIGGLE 심볼 자체가 발견되지 않는다** — 기존 7회 연속 503/429
실패와는 다른 상황으로, 상장폐지·리네이밍 가능성이 있다.

## 이번 회차 요약

①**1000RATS가 극적으로 재반전**했다 — 직전 -4.68%(마이너스 완화 중)였던 것이 이번엔
Binance +17.63%·Bybit +17.79%·XT.COM +18.42% 3개 소스 일치로 평균 **+17.71%** 강한 플러스
전환 — 4회 연속 방향이 뒤집히는 극단적 라운드트립 패턴 지속.

②**ADA·AAVE는 이번 회차 Bybit 데이터가 복구**돼 지난 회차의 '부분데이터' 한계가 해소됐다 —
ADA 평균 **-0.587%**(Binance -0.48%·Bybit -0.69%), AAVE 평균 **+0.044%**(Binance 0.0%·
Bybit +0.09%)로 둘 다 거의 flat에 근접, 지난 회차보다 개선.

③**신규: KAITO CEX 데이터를 OKX 직접조회로 최초 분리 확보**했다(-17.29%, funding 거의 flat) —
기존엔 Hyperliquid(DEX) 데이터가 CEX 표에 잘못 배치돼 있었는데, 이제 OKX(CEX)·Hyperliquid(DEX)
두 갈래로 정확히 분리해 보고한다(HL은 -15.53%로 유사 방향).

④**BEAT는 여전히 급락 중이나 낙폭이 소폭 완화**됐다(OKX -19.47%·Aster -19.59%, 평균
**-19.53%** vs 직전 -21.51%) — 뉴스 검색으로 8/1 대규모 언락(2,125만 BEAT, 약 $67.8M) 직후
오히려 +19.36% 숏스퀴즈가 있었으나 이후 -24% 재붕괴 등 극심한 양방향 변동이 실제로 보도돼
(Coinpedia '88% collapse, pump-and-dump 의혹' 기사 등) 이 종목은 데이터 오류가 아닌 진짜
초고변동성 국면임이 재확인된다.

⑤**BANK도 낙폭이 완화**됐다(3거래소 평균 **-7.68%** vs 직전 -11.79%) — 여러 회차 이어진
flip-flop 패턴 지속.

⑥**BICO는 funding이 여전히 거의 flat(-0.016%)인 채 가격만 추가 급등**했다(+22.12%→
**+36.57%**, XT.COM도 +35.34%로 확인) — 숏스퀴즈 해소 이후 순수 모멘텀 랠리로 보인다.

⑦**MMT는 OKX open-interest 엔드포인트로 이번 처음 OI를 직접 확보**했다($3.22M) — 그동안
CoinGecko 데이터셋에 항목이 없어 이월해온 문제가 해소됐다.

⑧**AIO는 촉매를 확인**했다 — 웹서치 결과 2025년 9월 보안침해(토큰 컨트랙트 교체) 이후의
지속적 부정 심리와 AI 토큰 섹터 대비 저조한 성과가 원인으로 보이며 새로운 촉매는 없다(평균
**-25.01%**로 직전 -32.02%에서 낙폭 다소 완화).

⑨**CASHCAT(+20.28%, 재가속)·BULLA(+9.91%)·BTW(+14.10%)·ALLO(+10.76%, Bybit도 복구돼 확대
재확인)는 모두 플러스 확장을 지속**했다.

## 시장 전반

- **총 시총 $2.24T(-0.62% 24h), BTC 도미넌스 56.21%, ETH 도미넌스 9.96% — 직전보다 낙폭 뚜렷이 축소. BTC -0.80%(OKX)로 완만한 반등.**
- **⭐ dYdX·GMX·OrangeX 3개 데이터 소스 동시 복구 — 모두 이전 회차 exchange id가 틀렸음을 확인.**
- **1000RATS, 4회 연속 방향전환 — 이번엔 +17.71%로 강한 재반전.**
- **BEAT·BANK, 낙폭은 완화되나 여전히 마이너스 — 극단 변동성 지속.**
- **XT.COM GIGGLE 심볼 소실 — 상장폐지·리네이밍 가능성.**

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **1000RATS** [극적 재반전, 4회째 방향전환] | Binance/Bybit/XT.COM | $580.64M | $43.69M | +6.40% | +17.71% | -4.68%→+17.71%로 강한 플러스 전환, 3개 소스 일치 | dramatic-reversal-4th-flip-now-strongly-positive |
| **BICO (Biconomy)** [funding flat 유지, 모멘텀 랠리] | OKX(직접API)/XT.COM | $64.97M | $1.96M | -0.02% | +36.57% | +22.12%→+36.57%로 추가 급등, funding은 여전히 flat — 순수 모멘텀 | funding-flat-price-extends-momentum-rally |
| **BEAT (Audiera)** [급락 지속, 낙폭 완화] | OKX(직접API)/Aster | $287.41M | $10.05M | +0.05% | -19.53% | -21.51%→-19.53%. 8/1 언락 후 숏스퀴즈→재붕괴 극단 변동 뉴스 확인 | crash-continues-decline-moderates-confirmed-extreme-volatility |
| **KAITO (신규 분리)** [CEX 데이터 최초 확보] | OKX(직접API) | $131.60M | $8.76M | -0.001% | -17.29% | 기존 HL 오분류 정정, 진짜 CEX 데이터 최초 확보. funding 거의 flat | cex-data-newly-separated-from-mislabeled-hl |
| ALLO (Allora) [상승폭 대폭 확대] | Binance/Bybit | $28.59M | $19.16M | -0.95% | +10.76% | +1.24%→+10.76%로 대폭 확대, Bybit 데이터도 이번 처음 확보 | positive-extends-sharply-bybit-newly-confirmed |
| AKE (Akedo) [플러스 유지, 소폭 재가속] | Binance/Bybit/Aster | $351.75M | $69.83M | +2.33% | +10.02% | +8.60%→+10.02%로 소폭 반등, funding도 재상승. 8/21 언락 임박 | positive-continues-slight-reacceleration |
| BANK (Lorenzo) [낙폭 완화] | Binance/Bybit/Aster | $182.63M | $23.88M | -4.30% | -7.68% | -11.79%→-7.68%로 축소, flip-flop 패턴 지속 | decline-moderates-flip-flop-continues |
| CAP [하락폭 소폭 추가 확대] | OKX(직접API)/Aster | $22.61M | $1.71M | +0.05% | -14.75% | -13.62%→-14.75%로 하락 지속 | negative-reversal-deepens-further |
| AIO (OlaXBT) [낙폭 완화, 촉매 확인] | Binance/Bybit | $40.88M | $4.20M | +0.50% | -25.01% | -32.02%→-25.01%. 촉매: 2025.9 보안침해 이후 지속 부정심리, 새 악재 없음 | decline-moderates-catalyst-identified-lingering-2025-breach-sentiment |
| ADA [Bybit 복구, flat 근접] | Binance/Bybit | $312.73M | $177.33M | +1.00% | -0.587% | 부분데이터 해소, 두 거래소 방향 일치로 개선 | full-data-restored-improves-near-flat |
| AAVE [Bybit 복구, 거의 완전 flat] | Binance/Bybit | $73.31M | $95.78M | +0.60% | +0.044% | 부분데이터 해소, 거의 완전 flat으로 개선 | full-data-restored-near-perfectly-flat |
| MMT (Momentum) [박스권 지속, OI 최초 확보] | OKX(직접조회) | $18.89M | $3.22M | -0.09% | -11.04% | -12.57%→-11.04% 유사 박스권. OI 직접 확보로 이월 문제 해소 | range-bound-continues-oi-finally-obtained |
| AEON [flat에서 소폭 더 마이너스] | OKX(직접API) | $14.94M | $1.99M | -0.07% | -3.02% | -1.0%→-3.02%로 소폭 하락, funding은 여전히 flat | near-flat-slightly-more-negative |
| ASTER (CEX) [근접 flat 지속] | Binance/Bybit/OKX/Aster | $18.91M | $341.63M | +0.65% | -0.062% | 4거래소 재확인해도 여전히 거의 완전 flat | near-flat-continues-essentially-unchanged |
| APR (aPriori) [Binance 신규 확보] | Binance/Bybit | $3.40M | $10.92M | +0.50% | -3.93% | 두 거래소 데이터 확보, 유사 수준 재확인 | binance-newly-confirmed-similar-level |
| APEX [Bybit 신규 확보, HL분 소액 이월] | Bybit/Hyperliquid | $0.23M | $2.37M | +0.15% | +1.85% | Bybit 데이터 이번 처음 확보(+2.98%) | bybit-newly-obtained-hl-portion-carried-small-size |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·GMX·dYdX·OrangeX·XT.COM)

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **LIT-USD (dYdX)** [동결 스트릭 종료] | dYdX | $14.31 | $14,718.01 | 0.0% | +1.14% | 6~7회 연속 완전동결이 이번에 처음 깨짐 — 모든 지표 변화 | freeze-streak-broken-first-change-confirmed |
| **ETH-USD** [dYdX 복구] | dYdX | $5.00M | $14.51M | -0.6% | -1.15% | 올바른 id 'dydx_chain' 확인해 3회 실패 후 복구 | endpoint-recovered-correct-id-found-fresh-data |
| **BTC-USD** [dYdX 복구] | dYdX | $4.36M | $17.20M | 0.0% | -0.73% | 위와 동일 id로 복구 | endpoint-recovered-correct-id-found-fresh-data |
| KAITO-USD (dYdX) [진짜 동결 재확인] | dYdX | $488.35 | $0.0 | 0.0% | 0.0% | 복구된 dYdX로도 정확히 동일값 — 진짜 죽은 시장 | genuinely-dead-market-confirmed-post-recovery |
| **BLESS-USDT-PERPETUAL** [OrangeX 복구, 큰 폭 냉각] | OrangeX | $403.94M | $165.69M | -12.9% | +31.35% | +69.45%(이월)→+31.35%로 대폭 냉각, 3개 소스 수렴 | endpoint-recovered-confirms-major-cooling-converges-with-other-sources |
| BLESS-USDT [조정 마무리 국면] | Aster | $2.82M | $0.45M | +4.4% | +33.09% | 거의 동일 수준, 다른 소스와 +29~33% 범위 수렴 | pullback-stabilizing-converges-with-other-sources |
| **CASHCAT** [재가속 지속] | Hyperliquid/Aster | $2.44M | $8.64M | +0.35% | +20.28% | +11.74%→+20.28%로 추가 재가속 | reaccelerates-further |
| **BULLA** [플러스 확장 지속] | Aster | $1.79M | $7.09M | +1.1% | +9.91% | +5.57%→+9.91%로 확장 지속 | positive-extends-further |
| **BTW** [플러스 확장 지속] | Aster | $0.68M | $6.62M | +0.9% | +14.10% | +9.70%→+14.10%로 확장 지속 | positive-extends-further |
| **ETH/USD (WETH-USDC)** [GMX 복구, 값 완전 동일] | GMX | $23.40M | $16.14M | +0.1% | +2.212% | 7회 실패 후 복구했으나 이월값과 완전 동일 — 저활동 마켓 확인 | endpoint-recovered-value-identical-confirms-genuine-stagnation |
| BTC/USD (BTC-USDC) [GMX 복구, 값 완전 동일] | GMX | $7.52M | $33.60M | +0.2% | +1.234% | 위와 동일 | endpoint-recovered-value-identical-confirms-genuine-stagnation |
| GIGGLE (Giggle Fund) [⚠️ 심볼 소실] | XT.COM | $34.11M(이월) | $224.34M(이월) | +0.5%(이월) | +6.12%(이월) | 티커 전체 재확인했으나 GIGGLE 심볼 자체가 없음 — 상장폐지 가능성 | symbol-no-longer-found-possible-delisting |
| HYPE-USD [소폭 플러스 확대] | Hyperliquid | $185.96M | $1,209.52M | -0.1% | +1.845% | +0.03%→+1.85%로 소폭 상승 | slight-positive-extends |
| HYPER-USD [유사 수준 지속] | Hyperliquid | $1.16M | $0.38M | -2.8% | -6.921% | -7.29%→-6.92%로 유사 범위 유지 | similar-range-continues |
| KAITO-USD [하락 재심화] | Hyperliquid | $27.84M | $26.79M | +0.1% | -15.532% | -14.65%→-15.53%로 재악화, OKX(-17.29%)와 유사 방향 | decline-slightly-deepens-again |
| FARTCOIN [마이너스 폭 축소] | Hyperliquid | $5.36M | $19.91M | +0.1% | -1.429% | -3.12%→-1.43%로 소폭 개선 | negative-narrows |
| ADA-USD [개선, CEX와 동일 방향] | Hyperliquid | $9.96M | $31.04M | +0.1% | -0.496% | -2.08%→-0.50%로 개선, CEX ADA와 유사 | improves-matches-cex |
| AAVE-USD [거의 완전 flat] | Hyperliquid | $5.39M | $66.06M | +0.1% | -0.098% | -0.75%→-0.10%로 flat에 근접, CEX AAVE와 유사 | near-perfectly-flat-matches-cex |
| AKE-USDT [재확인] | Aster | $3.15M | $13.02M | +1.0% | +9.778% | CEX와 함께 플러스 유지 재확인 | positive-continues-slight-reacceleration |
| BEAT-USDT [재확인] | Aster | $1.84M | $0.29M | +0.1% | -19.586% | OKX와 함께 급락 지속·완화 재확인 | crash-continues-decline-moderates-confirmed-extreme-volatility |
| BANK-USDT [재확인] | Aster | $0.62M | $0.35M | -1.9% | -7.034% | CEX와 함께 낙폭 완화 재확인 | decline-moderates-flip-flop-continues |
| CAP-USDT [재확인] | Aster | $0.02M | $0.03M | +0.1% | -16.716% | OKX와 함께 하락폭 확대 재확인 | negative-reversal-deepens-further |
| ASTER-USDT [재확인] | Aster | $6.36M | $219.27M | +1.7% | -0.066% | CEX 통합과 함께 근접 flat 재확인 | near-flat-continues-essentially-unchanged |
| APEX-USD [소액 이월] | Hyperliquid | $0.04M(이월) | $0.80M(이월) | -0.2%(이월) | +0.73%(이월) | $1M 미만 소액이라 재조회 목록 미노출 | carried-forward-below-threshold-small-size |
| LIT-USD / HYNA:LIGHTER-USD [7회 연속 완전 동결] | Hyperliquid | $461.35 | $0.0 | 0.0% | 0.0% | 소수점까지 완전 동일값 유지 | frozen-7th-round |

## 테마 태그

1. **⭐ 3개 데이터 소스 동시 복구: dYdX(id 'dydx_chain')·GMX(id 'gmx-perpetuals-v2-arbitrum')·OrangeX(id 'orangex_futures') — 이전 회차 시도한 id가 모두 틀렸음을 확인** (three-endpoints-recovered-correct-ids-found).
2. **LIT-USD(dYdX), 6~7회 연속 완전 동결이 처음 깨짐** (freeze-streak-broken-first-change-confirmed).
3. **KAITO-USD(dYdX)는 복구 후에도 동일값 유지 — 진짜 죽은 시장** (genuinely-dead-market-confirmed-post-recovery).
4. **GMX 두 마켓, 복구했으나 이월값과 완전 동일 — 저활동 정체 마켓 확인** (endpoint-recovered-value-identical-confirms-genuine-stagnation).
5. **OrangeX BLESS-USDT-PERPETUAL, 복구 후 큰 폭 냉각(+69.45%→+31.35%) — 3개 소스 수렴** (endpoint-recovered-confirms-major-cooling-converges-with-other-sources).
6. **⚠️ XT.COM GIGGLE 심볼 소실 — 상장폐지·리네이밍 가능성** (symbol-no-longer-found-possible-delisting).
7. **1000RATS, 4회 연속 방향전환 — +17.71%로 강한 재반전, 3개 소스 일치** (dramatic-reversal-4th-flip-now-strongly-positive).
8. **ADA·AAVE, Bybit 복구로 부분데이터 해소 — flat에 근접** (full-data-restored-improves-near-flat).
9. **신규: KAITO CEX 데이터 OKX 직접조회로 최초 분리 확보 — 기존 HL 오분류 정정** (cex-data-newly-separated-from-mislabeled-hl).
10. **BEAT, 급락 지속하나 낙폭 완화 — 뉴스로 8/1 언락 후 극단 양방향 변동 확인** (crash-continues-decline-moderates-confirmed-extreme-volatility).
11. **BANK, 낙폭 완화 — flip-flop 지속** (decline-moderates-flip-flop-continues).
12. **BICO, funding flat 유지 채 가격만 추가 급등 — 순수 모멘텀 랠리** (funding-flat-price-extends-momentum-rally).
13. **MMT, OI 최초 직접 확보 — 이월 문제 해소** (range-bound-continues-oi-finally-obtained).
14. **AIO, 촉매 확인 — 2025.9 보안침해 이후 지속 부정심리, 새 악재 없음, 낙폭 완화** (decline-moderates-catalyst-identified-lingering-2025-breach-sentiment).
15. **ALLO, 상승폭 대폭 확대 — Bybit도 이번 처음 확보** (positive-extends-sharply-bybit-newly-confirmed).
16. **CASHCAT·BULLA·BTW, 모두 플러스 확장 지속** (positive-extends-further-multiple).
17. **CAP, 하락폭 소폭 추가 확대** (negative-reversal-deepens-further).
18. **시장 전반: 총 시총 $2.24T(-0.62%), BTC 도미넌스 56.21% — 낙폭 뚜렷이 축소, BTC -0.80% 완만한 반등** (market-slightly-recovers-btc-minus0-8pct).
19. **신규 급등 스캔: XT.COM에서 토큰화 주식(AMD·AMZN·AAPL·ASML·ARM·ANTHROPIC 등) 대량 발견 — 규약에 따라 전부 제외 확인** (excluded-tokenized-stocks-xt-com-found-excluded).

## 데이터 신뢰도

**이번 회차는 데이터 소스 복구 측면에서 큰 진전이 있었다.** dYdX·GMX·OrangeX 세 소스 모두
이전 회차에 시도했던 CoinGecko exchange id가 틀렸음을 확인해 복구했다 — 정확한 id는 각각
`dydx_chain`(밑줄, 직전 회차가 추정한 하이픈 버전은 오답), `gmx-perpetuals-v2-arbitrum`,
`orangex_futures`다. 이 세 id는 CoinGecko의 `/derivatives/exchanges/list` 엔드포인트를
직접 조회해 확인한 것으로, 향후 회차에도 이 id들을 그대로 사용할 수 있다.

**GMX 복구 결과가 특히 시사하는 바가 크다** — ETH/USD[WETH-USDC]·BTC/USD[BTC-USDC] 모두
7회 연속 이월해온 값과 소수점 이하까지 정확히 동일했다. 이는 두 가지로 해석 가능하다: (a) GMX
Arbitrum의 해당 마켓이 실제로 극히 낮은 거래활동으로 장기간 정체돼 있었거나, (b) CoinGecko
자체가 이 마켓의 스냅샷을 갱신하지 않고 있을 가능성. 후자라면 "복구"로 판단한 것 자체가
성급할 수 있어, 다음 회차에도 값이 계속 동일하게 유지되는지 관찰이 필요하다.

**LIT-USD(dYdX)는 6~7회 연속 동결 후 처음으로 값이 변화**했다(거래량·OI·가격 모두 변동) —
반면 같은 dYdX의 KAITO-USD는 이번에도 완전히 동일한 값(vol $488.35·OI $0·chg 0%)을 유지해,
dYdX 자체는 정상 작동하되 KAITO-USD 마켓만 실제로 거래가 없는 죽은 시장임이 대조적으로
확인됐다.

**BEAT 관련 뉴스 검색으로 8/1 대규모 언락 이후의 실제 시장 반응을 확인**했다 — 2,125만
BEAT(약 $67.8M, 유통량의 6.9%) 언락 직후 오히려 +19.36% 급등(숏스퀴즈)했다가, 이후 -24%
붕괴 등 짧은 기간 내 극단적 양방향 변동이 실제로 보도됐다(Coinpedia의 '88% 붕괴, 펌프덤프
의혹' 기사 등). 이는 데이터 수집 오류가 아니라 이 종목의 실제 시장 특성임을 뒷받침한다.

**AIO의 촉매를 처음으로 특정**했다 — 웹서치 결과 2025년 9월 보안침해(토큰 컨트랙트 교체)
이후 지속되는 부정적 투자심리와 AI 토큰 섹터 대비 저조한 성과가 원인으로 지목됐으며, 새로운
악재성 촉매(상장폐지 등)는 확인되지 않았다.

**ADA·AAVE는 Bybit 데이터가 복구**돼 지난 회차의 'Binance 단독 부분데이터' 한계가 해소됐다.

**XT.COM에서 새로운 이슈가 발견**됐다 — GIGGLE 심볼이 전체 티커 목록에서 발견되지 않아
상장폐지 또는 리네이밍 가능성이 있다. 기존 7회 연속 503/429 응답 실패와는 성격이 다른
문제로, 다음 회차에도 재확인이 필요하다. 동시에 XT.COM에서 AMD·AMZN·AAPL·ASML·ARM·
ANTHROPIC 등 다수의 토큰화 주식 perp가 확인돼, 규약에 따라 리스트에서 전부 제외했다.

한계: (a) CEX $10M+ 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서만 수행했으며
전체 시장을 포괄하는 완전한 스캔은 아니다; (b) APEX-USD(HL)는 $1M 미만 소액 시장이라 이번
회차 재조회 목록에 노출되지 않아 이월했다; (c) GMX 복구값이 이월값과 완전 동일한 것이 진짜
저활동 시장 때문인지 CoinGecko 스냅샷 미갱신 때문인지는 다음 회차 추가 관찰이 필요하다; (d)
**주식화·상품·레버리지 ETF 토큰**은 이번 회차도 규약에 따라 cex/dex 리스트에서 전부 제외했다
(XT.COM에서 다수의 토큰화 주식 발견해 제외 확인); (e) OKX 심볼은 계속 직접 API 교차검증값을
우선 사용했다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
