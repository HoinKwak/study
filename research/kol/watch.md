# 온체인 트렌딩 조기경보 — 2026-08-14 10:58 UTC (KST 2026-08-14 19:58)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)
>
> **이번 회차 요약**: 직전 회차(2026-08-14 09:30 UTC, 약 1.5시간 전) 대비 핵심 변화. ① **신규 편입 없음(캡 14 유지)**: 이번 회차 신규 후보 발굴을 최우선으로 진행해 GeckoTerminal 솔라나·로빈후드체인 트렌딩·신규풀을 재스캔했다. 유력 후보로 **swappy**(로빈후드체인, GT유동성$111,294)와 **POOLS**(로빈후드체인, GT유동성$171,636)를 발견했으나, 두 후보 모두 **DexScreener·GeckoTerminal 두 소스 간 유동성 격차가 25~79%로 이례적으로 크게 벌어져**(swappy: DS$199,168 vs GT$111,295, 격차79%; POOLS: DS$128,561 vs GT$171,636, 격차25%) 우리가 그동안 다른 종목에서 확인해온 정상 격차(0.04~4%)를 크게 벗어났다. Gamblor·OUTCOME이 편입 2회차 만에 무너진 전례를 감안해 **데이터 신뢰도 미확보를 이유로 두 종목 모두 편입을 보류**했다(품질기준 미충족, 자세한 근거는 아래 참조). 그 외 XST(거래량/유동성비율 약78배, 워시트레이딩의심), K-HOME(h24-74%, 이미붕괴), Buddy(h24+904%, 극단뒷북) 등도 품질기준 미달로 제외했다. **캡 14/15 유지**. ② **CASHCAT — 현물-선물 온도차 대폭 축소**: 직전 회차 스팟 내부 첫 엇갈림(DS심화 vs GT개선)이 이번 회차 **DS·GT 모두 h24 심화(-9.28%→-10.74%, -7.274%→-8.338%) 방향으로 재수렴**했다. 10:41Z futures-scout가 보고한 perp -12.8%→-9.5%(완화)와 비교하면, 이번 회차 스팟 평균(약-9.54%)이 **perp -9.5%와 사실상 동일**해 직전까지 이어지던 4~5pp 현물-선물 온도차가 **사실상 해소**됐다. ③ **유동성 전반 점검 — 이번 회차도 극단적 급붕괴 없음**: 활성 14종목 중 이번 회차 최대 낙폭은 BLINK -5.24%, 다음이 Remus -4.67%로 모두 한 자릿수대에 머물러 ZAZU·Sheep·GTA·Gamblor·OUTCOME류의 -70~90%대 단일구간 급붕괴는 관측되지 않았다. 오히려 BABYSHIB(+7.00%)·lickingcat(+6.63%)·BRODIE(+6.27%)·TOAD(+4.12%) 4종목이 유동성 반등·강화를 보였다. ④ **BRODIE — 뚜렷한 반등전환**: 직전 회차 "재약화" 판정이 이번 회차 유동성+6.27%·h1/h6/h24 전 지표 개선으로 **명확히 반전**됐다. ⑤ **DPG — 재점화 지속되나 유동성 첫 반전 음전**: 모멘텀(h6/h24)은 계속 강화되지만 유동성이 재점화 이후 처음 소폭 감소(-3.25%)해 다음 회차 주시가 필요하다. ⑥ **CALLOOOR — h24 3회연속 감속, 그러나 h1/h6 재점화 조짐**: h24가 605%→451%→308%로 3회 연속 꾸준히 둔화 중이나, 이번 회차 h1(-9.06%→+2.77%)·h6(+2.93%→+37.24%)이 재차 강해져 단기 재점화 가능성이 있다. ⑦ **FWA·Remus — 직전 회차 반등이 이번 회차 다시 냉각/약화**됐다.

## ★ 이번 회차 최우선 판정 — 신규 후보 채택/제외 근거

- **swappy(로빈후드체인, Uniswap V3 0.25%, pools.trade) — 제외**: GeckoTerminal 트렌딩에서 유동성$111,294.56(임계선$20K 대비 충분, 거래량/유동성비율 6.14배로 과도하지 않음), h24+37.83%(뒷북 아님)로 1차 스크리닝은 통과했다. 그러나 동일 pair address(`0xaff8e2d7015c76fa6d9b2bedb72da7d6b305fd7b2140df3fca5c3c57e877ecfa`)를 DexScreener로 재조회(2회 독립 조회, 동일값 재현)한 결과 유동성$199,168.09로 **GT 대비 +79% 이례적 격차**가 확인됐다(h24도 DS+15~19.78% vs GT+37.83%로 방향은 같으나 폭이 다름). 우리가 그간 CASHCAT·OUTCOME 등에서 확인해온 DS-GT 정상 격차는 0.04~4%대였는데 이보다 훨씬 크다 — 데이터 신뢰도 미확보로 **편입 보류**.
- **POOLS(로빈후드체인, pools.trade) — 제외**: GT유동성$171,636(임계선 충분히 상회), 그러나 h6-18.37%·h24-13.63%로 이미 하락 추세이고(조기 신호 아님, 2026-07-30 생성으로 2주 이상 경과), DS 재조회 결과 유동성$128,560.72로 **GT 대비 -25% 격차**가 확인돼 마찬가지로 데이터 신뢰도 미확보. 추세도 조기성보다는 냉각기에 가까워 이중으로 품질기준 미달 — **편입 보류**.
- **기타 스캔 후보(전부 제외)**: XST(솔라나, 유동성$77,368이나 거래량/유동성비율 약78배로 워시트레이딩 의심 강함), K-HOME(솔라나, h24-74.33%로 이미 붕괴 진행형), Buddy(솔라나, h24+904.20%로 극단적 뒷북), Niles(솔라나, h24+582.55%로 극단적 뒷북), STACK·LEMON.FUN(로빈후드체인, 각각 h24+342.81%/+270.88%로 극단적 뒷북), THROBBIN(로빈후드체인, 유동성$85,408이나 h24-24.27%로 이미 하락 중이고 2026-07-08 생성으로 5주 이상 경과해 조기성 없음), "Megatron" 계열 신규풀 3~4개(솔라나, 유동성$11~15K로 $20K 임계선 미달), "ポンコ"(솔라나, 유동성$100,436이나 24h거래량 $243로 사실상 거래정지 상태). **결론: 이번 회차도 품질 기준을 통과하는 신규 후보를 찾지 못해 캡 14/15를 유지한다.**

## CASHCAT — 현물-선물 온도차 대폭 축소 (notable, 6회연속음전)

- 메인페어(Robinhood Chain, Uniswap V3 1%) `0xa70fc67c9f69da90b63a0e4c05d229954574e313`. **DS**: 유동성$3,963,539.43→$3,924,129.39(-1.0%), priceUsd$0.1397→$0.1367(-2.15%), h1+1.27%→-2.48%(반전음전), h6-7.41%→-5.79%(개선), h24**-9.28%→-10.74%(소폭심화)**. **GT**: 유동성$3,980,025.49→$3,993,271.77(+0.33%), priceUsd~$0.1397→$0.138970(-0.5%), h1+1.453%→-1.838%(반전음전), h6-5.48%→-5.171%(거의유지), h24**-7.274%→-8.338%(심화)**.
- **6회차 판정**: 방향은 두 소스 모두 6회 연속 음전이며, 직전 회차의 스팟 내부 첫 엇갈림(DS심화 vs GT개선)이 이번 회차 **DS·GT 모두 h24 심화 방향으로 재수렴**(격차 2.4pp로 직전보다 축소)됐다.
- **현물-선물 온도차 판정**: 10:41Z futures-scout가 보고한 perp -12.8%→-9.5%(완화)와 이번 회차 스팟 평균(DS-10.74%/GT-8.338%, 평균≈-9.54%)을 비교하면 **격차가 0.04pp 수준으로 사실상 해소**됐다. 직전 회차까지 이어지던 4~5pp 현물-선물 온도차가 이번 회차 크게 좁혀진 것으로, 선물 쪽 마이너스 완화와 현물 쪽 소폭 심화가 만나 두 시장이 수렴한 형태다.
- 참고: h1·h6은 두 소스 모두 소폭 개선(저점탐색 가능성) 흐름이라 완전한 하락추세 전환으로 단정하지는 않는다.

## 유동성 전반 점검 (활성 14종목)

| 종목 | 유동성 변화(DS) | 비고 |
|---|---|---|
| **BABYSHIB** | **+7.00%** | 반등지속강화(3회연속개선) |
| **lickingcat** | **+6.63%** | 재점화지속강화 |
| **BRODIE** | **+6.27%** | 재약화에서반등전환(3위상승) |
| **TOAD** | **+4.12%** | 전반적강화 |
| Dealer | +1.48% | 저변동보합에서소폭강화 |
| MANCER | +1.03% | 혼조지속에서소폭강화 |
| JUGGERNAUT | +0.67% | 개선지속 |
| CALLOOOR | -0.66% | 거의보합(h1/h6재점화조짐) |
| FWA | -1.55% | 반등전환후재냉각 |
| Momota | -2.20% | 안정유지속조정 |
| PITCOIN | -2.85% | 개선지속(유동성은소폭감소) |
| DPG | -3.25% | 재점화지속하나유동성첫반전음전 |
| **Remus** | **-4.67%** | 반등전환동력약화(2위낙폭) |
| **BLINK** | **-5.24%** | 약세전환지속(최대낙폭) |

**결론**: 이번 회차 최대 낙폭은 BLINK -5.24%로, 과거 ZAZU(-95%)·LOUIE·REDEMPTION(-90%)·KEP(-84%)·Sheep·GTA·Gamblor·OUTCOME류의 -70% 이상 급붕괴와는 확연히 다르다. 오히려 BABYSHIB(+7.00%)·lickingcat(+6.63%)·BRODIE(+6.27%)·TOAD(+4.12%) 4종목이 뚜렷한 유동성 강화를 보였다. BRODIE의 반등전환이 이번 회차 가장 눈에 띄는 변화다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

| 토큰 | 체인/DEX | 단계 | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|---|
| **BABYSHIB** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 편입9회차. 반등지속강화 | 유동성DS$56,192.83(+7.00%), h1+30.36%·h6+47.04%·h24-2.08%DS | 지속(편입9회차) | 🟡(반등지속강화) 신규추격절대금지 | [DexScreener](https://dexscreener.com/solana/DSiMBS1ueSLmjpt9WB9XKMFeuUjUK1YKcrSn7R2etQDX) |
| **lickingcat** | Solana(PumpSwap/Meteora) | 뒷북 | 미확인(코로보없음) | 51회차. 재점화지속강화 | 유동성DS$139,780.98(+6.63%), h1+17.35%·h6+107%·h24+90.93%DS | 지속(51회차) | 🟠(재점화지속강화) 신규추격절대금지 | [DexScreener](https://dexscreener.com/solana/HCTZakVpNZPfg9hCE3FoSDtnVJJtgAtNtiVY2wvxXdLN) |
| **BRODIE** | Robinhood Chain(Uniswap V3, Robinhood Dog) | 뒷북 | 미확인(코로보없음) | 편입23회차. 재약화에서반등전환 | 유동성DS$145,494.61(+6.27%), h1+8.5%·h6-4.98%·h24-46.45%DS | 지속(편입23회차) | 🟡(반등전환) 버퍼약627%, 신규추격절대금지 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **TOAD** | Solana(PumpSwap/Meteora) | 뒷북 | 미확인(코로보없음) | 60회차. 전반적강화 | 유동성DS$464,999.71(+4.12%), h1+2.6%·h6+8.35%·h24+8.3%DS | 지속(60회차) | 🟢(강화) 신규추격절대금지 | [DexScreener](https://dexscreener.com/solana/Nx9dcwNs3iJxM5YAxshMHE4aYJHdDyyGMhVcmaSgfu8) |
| **Dealer** | Solana(PumpSwap/Meteora) | 뒷북 | 미확인(코로보없음) | 52회차. 저변동보합에서소폭강화 | 유동성DS$151,656.11(+1.48%), h1+0.04%·h6-3.13%·h24+9.71%DS | 지속(52회차) | 🟡(보합에서소폭강화) 신규추격절대금지 | [DexScreener](https://dexscreener.com/solana/FjHUgiw2HZ9UoZuS6HAaEdnFTiRKJK22HN3ykAE2Eg5X) |
| **MANCER** | Robinhood Chain(Uniswap V3 1%) | 뒷북 | 미확인(코로보없음) | 38회차. 혼조지속(재분류계속보류) | 유동성DS$461,142.17(+1.03%), h1+1.73%·h6+0.68%·h24-6.16%DS | 지속(38회차) | 🟡(혼조지속, 재분류계속보류) | [DexScreener](https://dexscreener.com/robinhood/0x543127d6a1932689faacc1afad4a81146d9ccf54) |
| **JUGGERNAUT** | Robinhood Chain(Uniswap V3 1%) | 뒷북 | Drallio(X, CoinGape인용, 약한코로보, carryover) | 47회차. 개선지속 | 유동성DS$313,982.42(+0.67%), h1+0.25%·h6-1.98%·h24-26.4%DS | 지속(47회차) | 🟠(완만한개선) 신규추격절대금지 | [DexScreener](https://dexscreener.com/robinhood/0xD7321801CAae694090694Ff55A9323139F043B88) |
| **CALLOOOR** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 편입10회차. h24감속지속하나h1/h6재점화조짐 | 유동성DS$39,678.20(-0.66%), h1+2.77%·h6+37.24%·h24+308%DS | 지속(편입10회차) | 🟠(단기재점화조짐) 신규추격절대금지 | [DexScreener](https://dexscreener.com/solana/GoqQzeAvbNJgNskyxZi15GfR26xGce6dCSjXZxKYqJsJ) |
| **FWA** | Ethereum(Uniswap V4) | 뒷북 | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover)+CG트렌딩12위(carryover) | 64회차. 반등전환후재냉각 | 유동성DS(최대풀)$1,084,206.84(-1.55%), h1-3.17%·h6-6.17%·h24-2.22%DS | 지속(64회차) | 🟡(재냉각) 신규추격절대금지 | [DexScreener](https://dexscreener.com/ethereum/0xa0Df17B5aC76ABaBA36E1450E2cbCd18A620C845) |
| **Momota** | Solana(PumpSwap/Meteora/Raydium) | 뒷북 | 미확인(코로보없음) | 편입7회차. 안정유지속조정 | 유동성DS$190,529.24(-2.20%), h1+3.56%·h6-6.59%·h24+36.49%DS | 지속(편입7회차) | 🟢(안정유지) 신규추격절대금지 | [DexScreener](https://dexscreener.com/solana/BNgrT9cLk62z6iym7YqiZVUfeoGnFhjvHmw3r595pWzB) |
| **PITCOIN** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 편입12회차. 개선지속 | 유동성DS$32,839.16(-2.85%), h1-3.51%·h6-21.44%·h24-19.28%DS | 지속(편입12회차) | 🟠(추세개선지속, 유동성소폭감소) 신규추격절대금지 | [DexScreener](https://dexscreener.com/solana/AtNQriWPY8KgJp9Us3rM4ffayVa3yDE63hpPEW4TdeAF) |
| **DPG** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 편입11회차. 재점화지속하나유동성첫반전음전 | 유동성DS$87,654.65(-3.25%), h1-8.21%·h6+53.53%·h24+96%DS | 지속(편입11회차) | 🟠(모멘텀강화, 유동성주시필요) 신규추격절대금지 | [DexScreener](https://dexscreener.com/solana/8TbYi38UqcedfptvjN2rURLbGbGub3itp2hgLvvS35hY) |
| **Remus** | Solana(PumpSwap/Meteora) | 뒷북 | 미확인(코로보없음) | 56회차. 반등전환동력약화 | 유동성DS$55,399.71(-4.67%), h1-7.21%·h6-13.08%·h24-39.18%DS | 지속(56회차) | 🟠(동력약화) 여전히전지표음전권, 신규추격절대금지 | [DexScreener](https://dexscreener.com/solana/FLBSNxKr6SDdKePbB254yoSgjqUFbUyz8qVyKybwPv47) |
| **BLINK** | Robinhood Chain(Uniswap V3, pools.trade) | 뒷북 | 미확인(코로보없음) | 60회차. 약세전환지속(이번회차최대낙폭) | 유동성DS$151,880(-5.24%), h1-9.82%·h6-18.5%·h24-32.9%DS | 지속(60회차) | 🟠(약세전환지속) 신규추격절대금지 | [DexScreener](https://dexscreener.com/robinhood/0x6e31e066aa531bcb11133b4e7fe95a1a1ed50daa) |

> **편입/편출 내역(이번 회차)**: **편입/편출 없음**. GeckoTerminal 솔라나·로빈후드체인 트렌딩·신규풀 스캔에서 swappy·POOLS 2종을 유력 후보로 검토했으나 DS-GT 유동성 격차가 25~79%로 이례적으로 커 데이터 신뢰도 미확보로 보류. **캡 14/15 유지**.

## 온체인 신호 상세

- **swappy 상세(신규후보, 보류)**: pair `0xaff8e2d7015c76fa6d9b2bedb72da7d6b305fd7b2140df3fca5c3c57e877ecfa`(Robinhood Chain, Uniswap V3 0.25%, pools.trade), base token `0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7`, 2026-08-04 생성. GT: 유동성$111,294.56, 거래량h24$682,945.11(비율6.14배), h1-0.345%·h6-8.024%·h24+37.828%. DS(2회 독립 재조회, 동일값 재현): 유동성$199,168.09(base59,218,280swappy+quote50.04768ETH), 거래량h24$702,661~704,744, h1-12.74~-12.89%·h6-17.48~-18.54%·h24+15.00~19.78%. **GT-DS 유동성 격차 +79%**로 이례적 — 편입 보류 · 2026-08-14T10:58Z
- **POOLS 상세(신규후보, 보류)**: pair `0x88fbd9768ccf1bf77d6946afa1b2f3ce79e02a4566ca8a3d5ba78ab04e8ef27f`(Robinhood Chain, pools.trade), base token `0x385b36Ff682Ab4C76E7c37A66b96aABC466471d5`, 2026-07-30 생성(2주경과, 조기성낮음). GT: 유동성$171,636, 거래량h24$275,915, h1+3.22%·h6-18.37%·h24-13.63%. DS: 유동성$128,560.72, 거래량h24$278,193.60, h1+0.71%·h6-20.51%·h24-14.86%. **GT-DS 유동성 격차 -25%**로 이례적 — 편입 보류 · 2026-08-14T10:58Z
- **CASHCAT 상세(notable)**: 위 전용 섹션 참조.
- **BRODIE 상세(23회차, 재약화에서반등전환)**: `0x45F82AC5d507e988f7406935da8eEfe495a360e0`. DS: 유동성$136,912.09→$145,494.61(+6.27%), priceUsd$0.001204→$0.001313, h1-3.34%→+8.5%, h6-27.7%→-4.98%, h24-50.04%→-46.45%. 버퍼(20K기준): (145,494.61-20,000)/20,000=**+627.47%** · 2026-08-14T10:58Z
- **CALLOOOR 상세(10회차, h24 3회연속감속·h1/h6 재점화조짐)**: `A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump`. DS: 유동성$39,943.77→$39,678.20(-0.66%), priceUsd$0.0001684, h1-9.06%→+2.77%, h6+2.93%→+37.24%, h24 3회연속감속(605%→451%→308%) · 2026-08-14T10:58Z
- **lickingcat·DPG·BABYSHIB·TOAD·Dealer·MANCER·JUGGERNAUT·FWA·Momota·PITCOIN·Remus·BLINK**: 전량 DS 신규조회 완료(개별 pair address 직접조회로 재검증, 배치조회 중 Momota·BABYSHIB·lickingcat 3종은 아래 QA 참조). 상세 수치는 표·CSV 참조 · 2026-08-14T10:58Z
- **유동성 전반 점검**: 위 표 참조. 이번 회차 최대 낙폭은 BLINK -5.24%로 극단적 급붕괴는 미관측 · 2026-08-14T10:58Z
- **신규 후보 스캔**: GeckoTerminal 솔라나 트렌딩(BRAINOID -98.82%·Niles+582.55%·CATE·XST비율78배·K-HOME-74.33%·Buddy+904.20%), 로빈향체인 트렌딩(LEMON.FUN+270.88%·STACK+342.81%·swappy·POOLS·THROBBIN), 솔라나 신규풀(Megatron계열 $11~15K 미달·ポンコ 거래정지상태), CoinGecko 트렌딩(ACE·LAB·AKE·CASHCAT·PONS 등, 신규DEX후보없음) 전부 스캔 — **품질기준 통과 후보 없어 이번 회차도 신규 편입 없음, 캡 14/15 유지** · 2026-08-14T10:58Z

## 데이터 품질 QA — 배치조회 오염 3건 발견·수정

- 이번 회차 솔라나 9종목을 DexScreener `tokens` 배치 엔드포인트(주소 comma-separated)로 일괄조회했는데, **Momota·BABYSHIB·lickingcat 3종(9종 중 33%)에서 "최고유동성 pair"가 우리가 추적해온 기존 pair와 다른 풀로 잡혀 수치가 크게 왜곡**됐다(예: Momota 배치값 유동성$276,607 vs 기존pair재조회$190,529[-31%괴리], BABYSHIB 배치값$74,449 vs 재조회$56,193[-25%괴리], lickingcat h24배치값182,863%[명백한이상치] vs 재조회90.93%). 개별 pair address로 직접 재조회해 정정했다. **배치 엔드포인트는 참고용으로만 쓰고, 최종 채택값은 반드시 기존 추적 pair address의 개별 조회로 확정하는 원칙을 재확인**한다(응답이 섞인 것으로 의심되면 채우지 않고 재확인하는 기존 원칙의 연장).
- 나머지 6종(CALLOOOR·PITCOIN·DPG·Remus·Dealer·TOAD)은 배치값과 개별 pair 재조회값이 근접 일치(격차 1% 이내)해 신뢰도 높음.
- FWA·JUGGERNAUT·BRODIE·MANCER·BLINK(로빈후드체인 4종 배치 + FWA 개별)는 배치조회에서 뒤섞임 없이 정상 확인됨.

## KOL 코로보 (확보된 것만)

- **CASHCAT — 자체 루틴 교차확인(futures-scout 10:41Z 데이터 참조)**: 이번 회차는 futures-scout의 perp -12.8%→-9.5%(완화) 서술(10:41Z, 부모 프롬프트 제공)과 이번 스팟 조회값(DS-10.74%/GT-8.338%)을 비교해 온도차 대폭 축소를 판정했다. DS·GT 현물 두 소스 간 교차확인(격차2.4pp)도 함께 실시했다.
- **JUGGERNAUT — 약한 코로보(carryover)**: CoinGape 기사가 X 애널리스트 Drallio를 인용한 내용은 이전 회차와 동일(신규 업데이트 없음).
- **FWA — 코로보(2차소스, carryover)**: Cointelegraph·CryptoBriefing·KuCoin뉴스·PANews 보도와 CoinGecko 트렌딩 12위 재등재는 이번 회차 재조회 생략(carryover 유지).
- **BABYSHIB·lickingcat·BRODIE·TOAD·Dealer·MANCER·CALLOOOR·Momota·PITCOIN·DPG·Remus·BLINK — 코로보 미확인**: 이번 회차도 개별 인플루언서 언급은 발견하지 못했다 — 코로보 없음(정상 상태).
- **기타**: notable 중 STONKBROKER·PONS·TENDIES·STONK·TYGR·KIO·NASDANQ·PIPEDOG·HOODRAT·ANSEM·TUT은 이번 회차도 개별 KOL 언급을 확인하지 못했다 — **코로보 없음**(결함이 아닌 정상 상태). X 직접 조회는 로그인월로 시도하지 않았다.

## 메모

- **신규 후보 미채택의 의미**: 이번 회차는 신규 편입을 최우선 과제로 삼아 실제로 1차 스크리닝(유동성·거래량/유동성비율·뒷북여부)을 통과한 후보 swappy·POOLS를 발견했으나, **DS-GT 교차검증에서 25~79%의 이례적 유동성 격차**가 확인돼 최종적으로 보류했다. 이는 결함이 아니라 "값을 추정하지 말고 재확인 실패를 정직 표기"하는 원칙의 정상 적용이다. Gamblor·OUTCOME이 편입 직후 2회차 만에 무너진 전례를 고려하면, 데이터 신뢰도가 불확실한 상태로 편입해 다음 회차에 또 편출하는 것보다 보류가 합리적이다.
- **CASHCAT 온도차 대폭 축소**: 여러 회차 이어지던 현물-선물 온도차(4~5pp)가 이번 회차 사실상 해소됐다(격차 0.04pp). 선물 쪽 마이너스 완화(-12.8%→-9.5%)와 현물 쪽 소폭 심화(-8.3%→-9.54%평균)가 만나 두 시장이 비슷한 수준으로 수렴한 형태로, 다음 회차 방향(추가수렴유지 vs 재이격)을 지켜볼 필요가 있다.
- **BRODIE 반등전환**: 여러 회차 이어지던 재약화 추세가 이번 회차 유동성·h1·h6·h24 전 지표 개선으로 뚜렷하게 반전됐다. 다음 회차 지속 여부가 관건이다.
- **DPG 유동성 첫 반전 음전**: 모멘텀지표(h6/h24)는 계속 강화되나 유동성이 재점화 이후 처음 감소(-3.25%)해, 모멘텀과 유동성이 괴리되기 시작했는지 다음 회차 확인이 필요하다.
- **데이터 품질 QA — 배치조회 오염 발견**: 이번 회차 DexScreener 배치(comma-separated) 조회에서 9종목 중 3종목(33%)이 다른 풀 데이터로 오염된 것을 발견해 개별 pair 재조회로 전량 정정했다. 상세는 위 QA 섹션 참조 — 배치조회의 구조적 한계(여러 풀 중 무작위/최고유동성 풀을 반환해 기존 추적 풀과 어긋날 수 있음)를 이번 회차 처음 명시적으로 확인했다.
- **데이터 신뢰도 총평**: 이번 회차는 CASHCAT(DS+GT, 격차2.4pp)을 중점 교차검증했고, 신규후보 2종(swappy·POOLS)도 DS+GT 교차검증을 실시해 오히려 그 격차(25~79%) 때문에 편입을 보류하는 근거로 삼았다. 활성 14종목은 배치조회 오염 3건을 개별 pair 재조회로 정정한 뒤 확정했다. notable 대부분(TUT·STONKBROKER·PONS·TENDIES·STONK·TYGR·KIO·NASDANQ·PIPEDOG·HOODRAT·ANSEM)은 carryover로 유지(정직 표기). X 직접 조회는 로그인월로 시도하지 않았다.

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API·WebSearch) 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
