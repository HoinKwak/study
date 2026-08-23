# 온체인 트렌딩 조기경보 — 2026-08-23 03:00 UTC (KST 2026-08-23 12:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-23 01:00Z)로부터 정확히 2시간 경과**(정상 간격). 기존 35개 활성종목 전부를 DexScreener 토큰 API(체인별 배치조회)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 스캔으로 신규 발굴을 진행했다.

> **신규 편입: CHUMP(Robinhood체인, 확산) + BARRON(Solana, 뒷북) — 2건.** 편출 없음. 활성목록 **35종→37종**. notable **24개 유지**(CASHCAT·STONKBROKER·PONS·ANSEM·CATSZN 참고데이터 갱신).

## ⚠️ 부모 세션 요청 최우선 확인 — LIZARD 소멸여부, Truth Coin 양체인, OBS 유동성 흐름

- **LIZARD**(풀생성 후 약 27.9시간): **소멸되지 않았다.** 여전히 활발히 거래 중이다(1시간 71매수/70매도, 24h거래량 $741,208). 다만 유동성이 $45,251.47→**$41,246.55**(-8.85%)로 **3회차 연속 유출**됐다. h1은 매도우위가 완화됐지만(-25.49%→-8.41%) h6가 다시 급격히 악화(-14.19%→**-47.92%**)했고 h24는 -60.73%→-61.37%로 저점권 보합이 이어진다. 회전율은 약 18배로 직전 26배보다 하락했지만 여전히 높다. **결론: 소멸은 아니지만 3회차 연속 유동성 유출로 점진적 위축 국면에 진입한 것으로 보인다.**
- **Truth Coin(Robinhood, 2회차)**: ⭐유동성이 $306,107.04→**$364,541.37**(+19.09%)로 추가 대폭 유입되며 h24가 +267,318%→**+356,326%**로 더 상승했다(초저유동성 출발가 영향이 24h 윈도우 내내 지속되는 것으로 해석). 거래량 $13,905,438.55, 회전율≈38.1배(직전 33배에서 상승), 1시간 1,353매수/233매도로 강한 매수우위. 풀생성 후 약 10.5시간, 여전히 초기 단계.
- **Truth Coin(Solana, 2회차)**: h6는 개선(-46.1%→-37.19%)했으나 h24는 추가 악화(-7.58%→-22.62%)했다. 회전율이 약 251배→**약 273배**로 이 워치 사상 최고 기록을 다시 경신했다(거래량 $4,227,877.19 / 유동성 $15,466.77). 극단적 워시트레이딩 의심 유지.
- **OBS**(15회차째): ⭐유동성이 $75,852.71→**$86,056.55**(+13.45%)로 **3회차 연속 증가**(+40.79%→+21.19%→+13.45%)를 확정했다. h6는 +112%→+276%로 대폭 가속, h24는 +153%→+116%로 소폭 감속하나 여전히 강세.

## 🆕 신규 발굴 — CHUMP(Robinhood체인) / BARRON(Solana)

- **CHUMP(Robinhood Chain, Uniswap V3 1%, WETH페어)** — CA `0x0E0d2C89a5a019FE1cF762e5e33187631DACC21B`. GeckoTerminal 로빈후드체인 트렌딩 11위로 발견. 풀생성 2026-07-31(약 23일 전). 전지표 동시 양전이고 h1(+13.55%)<h6(+24.99%)<h24(+65.72%) 순으로 자연스러운 우상향 패턴이다. 유동성 $252,328.11, 거래량24h $324,505.62(회전율≈1.29배로 워시트레이딩 징후가 상대적으로 낮음), 1시간 44매수/20매도. **확산** 단계로 신규편입. 🟡(신규).
- **BARRON(Solana, Raydium)** — CA `ECY31gWwxy4s2VnMkYhmqDkrV75KrwR2yTtsnrnSpump`. GeckoTerminal 솔라나 트렌딩 8위로 발견(h24+198.70%). ⚠️**DexScreener로 pairCreatedAt을 직접 확인한 결과 약 2025-01-20경(약 19개월 전) 생성된 풀**로 밝혀졌다 — GT 트렌딩 노출과 달리 신생 토큰이 아니라 **구풀의 거래 재개(revival pump)**로 판단된다. h24+206%(24시간 누적치)이나 h1-0.78%·h6-5.42%로 이미 감속·재음전 전환 중이라 캐치 시점에 이미 고점을 통과했을 가능성이 높다. 유동성 $282,222.17, 거래량24h $3,160,728.43(회전율≈11.2배, **최대거래량 풀=raydium** — 부모 세션이 전체 22개 페어를 원자료로 재조회해 확인, 초판의 PumpSwap 표기는 오기였다). **뒷북** 단계로 신규편입(풀나이-모멘텀 불일치 정직 표기). 🔴(신규,고점통과추정).
- 둘 다 WebSearch로 프로젝트 실체를 검색했으나 특정 보도 확인 안 됨(**KOL/미디어 코로보 없음**, 정직 표기).

## 나머지 35종 갱신

- **TIPANSEM**: 21회차. ⚠️3회차연속개선흐름이 이번회차 유동성유출로 반전(유동성-5.99%, h1재음전-0.69%, h6감속+10.08%, h24재악화-47.82%). 🔴(재상향).
- **1B**: 13회차. 유동성유입전환(+3.75%), h1대폭재양전(+5.14%)하나 h24는 역대최악치 추가경신(-88.75%). 🔴(유지,극심한변동성).
- **CLOCKIN**: 33회차. 유동성유입전환(+5.81%), h6·h24동시개선(h24-32.55%). 🔴(유지).
- **PEE**: 50회차. ⚠️h1 1시간동안 매수·매도 0건으로 거래 사실상 실종, 유동성도 추가유출(-7.53%), h6·h24 악화(h24-25.63%). 🔴(재상향,소멸경계).
- **CLUG**: 45회차. ⭐h24대폭개선(-39.94%→-11.31%, +28.63%p). 🔴(유지).
- **PEPECOIN**: 23회차. h6대폭개선(-21.05%→-1.59%,손익분기근접)하나 h1재음전(-9.52%). 🔴(유지,혼조).
- **FLUSH**: 11회차. ⚠️h24역대급붕괴지속(-61.51%→-81.83%), 유동성추가유출(-8.05%). 직전 520%p붕괴에 이어 추가 악화. 🔴(유지,극단반전지속).
- **MAPLE**: 9회차. ⚠️유동성재유출(-5.95%), h1급반전악화(+3.43%→-22.76%). 🔴(재상향).
- **40M**: 8회차. ⭐h24극적반전, 드디어 재양전전환(-30.43%→+35.42%, +65.85%p). h6도 손익분기 돌파. 🟢(하향,반전확인).
- **swappy**: 26회차. 큰변화없이보합권지속(유동성+1.96%, h24-12.4%). 🟡(유지).
- **CYBERLEEK**: 25회차. ⚠️유동성대폭유출전환(-17.21%), 전지표동시감속(h6+228%→+66.16%, h24+894%→+643%). 고점통과신호. GT교차확인(h1부호는상이). 🟡(재상향).
- **CC**: 23회차째방향번복지속. 유동성대폭유출(-19.21%), 전지표감속(h6+352%→+229%, h24+233%→+104%). 🔴(고위험).
- **Z500**: 16회차. h1재음전(-1.14%)하나 h6·h24는 개선(h24-11.7%). 🟡(유지).
- **KIRK**: 13회차. ⚠️직전 h24최초재양전이 다시 무산, 12회차째 휩소패턴 재확인(+10.16%→-17.48%). 🔴(유지,휩소재현).
- **CONK**: 10회차. ⚠️전지표동시추가악화지속(유동성-9.09%, h24-14.16%→-24.65%). 4회차연속하락, GT교차확인(근접일치). 🔴(유지,극단수준붕괴지속).
- **HOOKR**: 28회차. ⭐전지표동시강한개선(유동성+6.58%, h1재양전+9.76%, h6가속+17.1%, h24개선-4.59%). 🟡(하향).
- **CATE**: 87회차. ⚠️**풀선택 정정** — 이번 회차 다수풀 재점검 결과 최대유동성 pumpswap풀(회전율≈19.5배)로 정정. 전방위 재음전전환(h1-40.33%, h6-23.34%, h24-14.31%). 🟡(재상향, 상세는 아래 참조).
- **GOOD**: 29회차. h1·h24개선(h24-13.6%→-5.21%), h6재음전(-9.62%). 🟡(유지).
- **PRINTER**: 164회차. h1개선(+7.35%), h6·h24는추가악화(h24-29.86%). 🟡(유지).
- **BULLSHIT**: 44회차. ⚠️h6·h24동시재음전전환(h6+21.89%→-2.34%, h24+19.22%→-7.01%). 🟡(재상향).
- **TOAD**: 163회차. ⚠️직전h24손익분기돌파가 1회차만에 무산(+10.03%→-8.22%). 🟡(재상향).
- **DPG**: 115회차. ⚠️전지표동시재음전전환(h1-8.5%, h6-4.09%, h24-4.68%), 3회차연속악화. 🟡(재상향).
- **FWA**: 167회차. h1·h6재음전, h24는개선(+3.11%→+7.51%). 🟡(유지).
- **CALLOOOR**: 113회차. 직전전지표양전전환이 h1급감속(+39.41%→+0.27%)하나 h6·h24는양전유지. 🟡(유지).
- **JUGGERNAUT**: 150회차. ⭐유동성유입(+7.72%), h24는손익분기근접까지대폭개선(-17.63%→-1.37%). 🟡(유지).
- **BRODIE**: 126회차. ⭐h1데이터정상화확인(직전회차파싱이상해소, 이번 4.1%로 정상범위), h6·h24모두개선. 🟡(유지).
- **Dealer**: 155회차. h1·h6재음전, h24는감속하나양전유지(+15.2%). 🟡(유지).
- **lickingcat**: 155회차. ⭐h1·h6·h24전부개선(h24-26.2%→-22.77%). 🔴(하향,개선흐름).
- **PITCOIN**: 116회차. 전지표동시감속하나양전유지(h24+11.38%→+4.89%). 🟡(재상향).
- **PANTS**: 15회차(dogwifpants). ⚠️유동성대폭유입(+19.24%)에도불구전지표동시대폭감속(h24+107%→+37.41%, -69.59%p). GT교차확인. 🟡(재상향,고점통과가능성).
- **Doge2**: 8회차. ⭐전지표동시대폭가속, h6도재양전전환(-55.39%→+55.61%, 극적반전). h24+199%→+392%. GT교차확인. 🔴(유지,변동성극심).

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

| 토큰 | 체인/DEX | 단계 | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|---|
| **Truth Coin** | Robinhood Chain(Uniswap V2) | 조기 | 미확인(코로보없음) | 2회차,풀생성10.5h전,유동성추가대폭유입 | 유동성$364,541.37(+19.09%), h24+356,326%, 회전율≈38.1배 | 지속(2회차) | 🔴(매우초기,워시트레이딩강력의심) | [DexScreener](https://dexscreener.com/robinhood/0xa48a58514a4bf47849c8bdc227f109af54cb1bb4) |
| **OBS** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 15회차. 3회차연속유동성증가확정 | 유동성$86,056.55(+13.45%), h24+116% | 지속(15회차)·유동성지속유입 | 🔴(매우초기) | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **40M** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 8회차. h24극적반전,재양전전환 | 유동성$15,618.1(-3.03%), h24+35.42%(+65.85%p) | 지속(8회차)·재양전전환 | 🟢(하향,반전확인) | [DexScreener](https://dexscreener.com/solana/Ct6arp861CvmvsAZ4pse7ZyTS2dDexfz9Yv2G6ajeU5q) |
| **LIZARD** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 4회차(풀생성후약27.9h). 소멸안됐으나3회차연속유동성유출 | 유동성$41,246.55(-8.85%), h24-61.37%, 회전율≈18배 | 지속(4회차)·점진적위축 | 🔴(점진적위축) | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **CLUG** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 45회차. h24대폭개선 | 유동성$36,672.32(-0.92%), h24-11.31%(+28.63%p) | 지속(45회차)·개선 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 조기 | 미확인(코로보없음) | 23회차. h6대폭개선,h1재음전 | 유동성$19,007.95(-7.02%), h24-47.37% | 지속(23회차)·혼조 | 🔴(혼조) | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **CLOCKIN** | Robinhood Chain | 조기 | 없음(자체서사만확인) | 33회차. 유동성유입전환,단기지표개선 | 유동성$183,403.89(+5.81%), h24-32.55% | 지속(33회차) | 🔴(유지) | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **1B** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 13회차. 유동성유입,h1재양전하나h24역대최악 | 유동성$25,509.19(+3.75%), h24-88.75%(역대최악) | 지속(13회차)·극심한변동성 | 🔴(극심한변동성) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **TIPANSEM** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 21회차. 3회차연속개선흐름이반전 | 유동성$13,434.02(-5.99%), h24-47.82% | 지속(21회차)·반전 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **MAPLE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 9회차. 유동성재유출,h1급반전악화 | 유동성$23,942.08(-5.95%), h24-43.84% | 지속(9회차)·반전 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/7XA6NCMKa8Vk5Y3gdaaNsvGhjAdkqUDsGHkUpYUZBwh3) |
| **FLUSH** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 11회차. h24역대급붕괴지속 | 유동성$33,514.07(-8.05%), h24-81.83%(추가붕괴) | 지속(11회차)·추가붕괴 | 🔴(극단반전지속) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 50회차. 1시간거래완전실종 | 유동성$8,032.66(-7.53%), h24-25.63%, h1거래0건 | 지속(50회차)·거래실종 | 🔴(소멸경계) | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **CHUMP** | Robinhood Chain(Uniswap V3 1%) | 확산 | 미확인(코로보없음) | 신규,풀생성23일전,전지표동시양전(h1<h6<h24) | 유동성$252,328.11, h24+65.72%, 회전율≈1.29배 | **신규** | 🟡(신규) | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CONK** | Solana(Raydium) | 확산 | 미확인(코로보없음) | 10회차. 전지표동시추가악화지속(4회연속하락) | 유동성$100,784.81(-9.09%), h24-24.65% | 지속(10회차)·4회연속하락 | 🔴(극단수준붕괴지속) | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CC** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 23회차째방향번복지속,유동성대폭유출 | 유동성$201,433.66(-19.21%), h24+104%(감속) | 지속(23회차)·워시트레이딩의심강화 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **KIRK** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 13회차. 직전h24돌파가다시무산,휩소재현 | 유동성$76,919.73(-6.86%), h24-17.48%(재음전) | 지속(13회차)·휩소재현 | 🔴(휩소이력경계) | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **swappy** | Robinhood Chain(Uniswap V4) | 확산 | 미확인(코로보없음) | 26회차. 큰변화없이보합권지속 | 유동성$216,977.74(+1.96%), h24-12.4% | 지속(26회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 확산 | 미확인(코로보없음) | 25회차. 유동성대폭유출전환,전지표감속 | 유동성$1,116,205.57(-17.21%), h24+643%(감속) | 지속(25회차)·고점통과신호 | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **Z500** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 16회차. h1재음전,h6·h24는개선 | 유동성$87,791.81(-2.62%), h24-11.7% | 지속(16회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **Truth Coin** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 2회차,풀생성12.6h전,회전율사상최고경신 | 유동성$15,466.77(-6.36%), 회전율≈273배 | 지속(2회차) | 🔴(이미정점통과,극단적워시트레이딩의심) | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 뒷북 | 미확인(코로보없음) | 신규,풀나이19개월(revival pump),h1·h6이미음전 | 유동성$282,222.17, h24+206%(누적치), 회전율≈11.2배 | **신규** | 🔴(고점통과추정) | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **CALLOOOR** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 113회차. h1급감속하나h6·h24양전유지 | 유동성$64,214.33(-2.36%), h24+9.12% | 지속(113회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **JUGGERNAUT** | Robinhood Chain(Uniswap V3 1%) | 뒷북 | Drallio(약한코로보,carryover) | 150회차. 유동성유입,h24손익분기근접 | 유동성$266,345.9(+7.72%), h24-1.37% | 지속(150회차)·손익분기근접 | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **HOOKR** | Robinhood Chain(Uniswap) | 뒷북 | 미확인(코로보없음) | 28회차. 전지표동시강한개선 | 유동성$212,196.76(+6.58%), h24-4.59% | 지속(28회차)·재반전개선 | 🟡(하향) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **lickingcat** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 155회차. 전지표동시개선 | 유동성$58,373.31(+0.17%), h24-22.77% | 지속(155회차)·개선흐름 | 🔴(하향,개선흐름) | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **BRODIE** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 126회차. h1데이터정상화,h6·h24개선 | 유동성$174,810.71(+2.70%), h24-5.66% | 지속(126회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **Doge2** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 8회차. 전지표동시대폭가속,h6극적반전 | 유동성$42,077.57(+29.82%), h24+392% | 지속(8회차)·극적반전 | 🔴(변동성극심) | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **GOOD** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 29회차. h1·h24개선,h6재음전 | 유동성$450,320.23(-1.10%), h24-5.21% | 지속(29회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PANTS** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 15회차(dogwifpants). 유동성대폭유입,전지표대폭감속 | 유동성$203,678.16(+19.24%), h24+37.41%(감속) | 지속(15회차)·고점통과가능성 | 🟡(고점통과가능성) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **PITCOIN** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 116회차. 전지표동시감속하나양전유지 | 유동성$32,536.78(-5.24%), h24+4.89% | 지속(116회차)·감속 | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **CATE** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 87회차. 풀선택정정,전방위재음전전환 | 유동성$1,868,251.43(pumpswap), h24-14.31%, 회전율≈19.5배 | 지속(87회차)·풀정정 | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **Dealer** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 155회차. h1·h6재음전,h24는양전유지 | 유동성$122,234.31(-3.73%), h24+15.2% | 지속(155회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **FWA** | Ethereum(Uniswap V4) | 뒷북 | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover)+CG트렌딩12위(carryover) | 167회차. h1·h6재음전,h24는개선 | 유동성$1,133,280.01(-3.98%), h24+7.51% | 지속(167회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 뒷북 | 미확인(코로보없음) | 164회차. h1개선,h6·h24추가악화 | 유동성$356,589.84(-1.78%), h24-29.86% | 지속(164회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **BULLSHIT** | Solana(Meteora 등 11개풀) | 뒷북 | 미확인(WebSearch로토큰명특정보도없음) | 44회차. h6·h24동시재음전전환 | 유동성(PumpSwap)$253,435.79(-4.86%), h24-7.01% | 지속(44회차) | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **TOAD** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 163회차. 직전h24돌파가1회차만에무산 | 유동성$414,727.45(-6.54%), h24-8.22%(재음전) | 지속(163회차)·돌파무산 | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **DPG** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 115회차. 전지표동시재음전전환(3회연속악화) | 유동성$92,457.85(-7.08%), h24-4.68% | 지속(115회차)·재음전 | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |

> **편입/편출 내역(이번 회차)**: **신규편입 2건** — CHUMP(Robinhood체인,확산)·BARRON(Solana,뒷북,풀나이19개월로revival pump 판정). **편출 없음.** **소멸여부확인 1건**: LIZARD(소멸안됐으나3회차연속유동성유출로점진적위축). **역대최악/최고경신**: 1B(h24-88.75%역대최악), Truth Coin Solana(회전율273배사상최고). **극적반전 2건**: 40M(h24재양전전환), Doge2(h6극적반전+전지표대폭가속). **돌파무산 1건**: TOAD(h24손익분기돌파1회차만에무산). **풀선택정정 1건**: CATE(최대거래량풀 pumpswap으로 전환, 규약§2재확인).

## 온체인 신호 상세

- **부모세션요청(LIZARD·Truth Coin양체인·OBS) 상세**: 위 스포트라이트 섹션 참조. LIZARD는 3회차 연속 유동성 유출(-13.65%→-8.85%)에도 불구 1시간 거래는 71건/70건으로 여전히 활발해 '소멸'과 '단순 위축'을 구분해야 함을 확인 · 2026-08-23T03:00Z
- **CATE 풀선택 정정 상세**: 직전 회차 자동선택 풀(meteora, 거래량$6.15M)이 실제 최대거래량 풀(pumpswap, 거래량$36.34M)이 아니었음을 이번 회차 전체 페어 목록 조회로 확인해 규약§2("최대유동성풀만 고르지 말고 거래량을 함께 볼 것")에 따라 pumpswap 풀 기준으로 정정. 유동성 $1,868,251.43, h24-14.31%, 회전율≈19.5배(직전 10배대 근접 대비 대폭 상승). PANTS 사례와 동일 유형의 재발 방지 조치 · 2026-08-23T03:00Z
- **BARRON 신규발굴 상세**: GeckoTerminal 솔라나 트렌딩 8위(h24+198.70%)로 발견했으나, DexScreener pairCreatedAt(1737335861000ms) 확인 결과 2025-01-20경 생성된 풀로 확인돼 '신규' 트렌딩이 아니라 구풀의 거래 재개(revival pump)임을 규명. 규약 준수 사례(1차: WebFetch 요약 대신 raw 필드 직접확인) · 2026-08-23T03:00Z
- **CHUMP 신규발굴 상세**: GeckoTerminal 로빈후드체인 트렌딩 11위(h24+64.57%)로 발견, DexScreener 재확인으로 h1+13.55%/h6+24.99%/h24+65.72% 전지표 동시 양전 및 h1<h6<h24 자연스러운 우상향 패턴 확인. 회전율 1.29배로 워시트레이딩 징후 낮음 · 2026-08-23T03:00Z
- **나머지 31건 상세**: TIPANSEM 3회연속개선반전(h24-47.82%). 1B h1대폭재양전·h24역대최악(-88.75%). CLOCKIN유동성유입전환. PEE h1거래완전실종. CLUG h24대폭개선(+28.63%p). PEPECOIN h6손익분기근접. FLUSH h24추가붕괴(-81.83%). MAPLE h1급반전악화. 40M h24재양전전환(+65.85%p). swappy보합. CYBERLEEK유동성대폭유출(-17.21%)·전지표감속. CC유동성대폭유출·전지표감속(워시트레이딩의심강화). Z500소폭개선. KIRK휩소재현(h24-17.48%). CONK4회연속하락(GT근접일치). HOOKR전지표강한개선. GOOD혼조. PRINTER h1개선·h24악화. BULLSHIT전지표재음전전환. TOAD돌파1회차만에무산. DPG전지표재음전전환(3회연속악화). FWA h24개선지속. CALLOOOR h1급감속하나양전유지. JUGGERNAUT h24손익분기근접. BRODIE h1정상화·전반적개선. Dealer h24양전유지. lickingcat전지표개선. PITCOIN전지표감속하나양전유지. PANTS전지표대폭감속(고점통과가능성). Doge2극적반전(GT근접일치). Truth Coin(Sol)회전율사상최고경신 · 2026-08-23T03:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **CHUMP·BARRON(신규) — WebSearch로 검색했으나 특정 프로젝트를 다루는 보도 확인 안 됨. 코로보 없음(정상 상태, 결함 아님)**.
- **나머지 33종(부모세션 최우선 확인대상 포함) — 코로보 미확인**: 이번 회차는 37개 활성종목(신규2건 포함)과 notable 5종(CASHCAT·STONKBROKER·PONS·ANSEM·CATSZN) 참고데이터 갱신에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-23 01:00Z)로부터 정확히 2시간 경과(정상 간격).
- **신규 편입 2건**: CHUMP(Robinhood체인, GT트렌딩11위, 확산단계, 풀나이23일)와 BARRON(Solana, GT트렌딩8위, 뒷북단계, **풀나이19개월로 revival pump 판정**). BARRON은 GT 트렌딩 h24+198.70%에 이끌려 발견했으나 DexScreener raw 필드로 pairCreatedAt을 직접 검증한 결과 신생 토큰이 아님이 드러난 사례로, 규약 1번("풀 생성시각은 raw JSON 필드를 직접 확인")이 실제로 오판을 방지한 케이스다.
- **CATE 풀선택 오류 정정**: 이번 회차 CATE 전체 페어 목록을 재조회한 결과, 직전까지 자동선택돼온 풀(meteora, 거래량 $6.15M)이 실제 최대거래량 풀(pumpswap, 거래량 $36.34M)이 아니었음을 확인해 정정했다. 유동성·가격변동률 수치가 크게 달라지므로 직전 회차와의 단순 % 비교는 부적절해 절대값 기준으로 재기재했다. 규약 2번("다수 풀 토큰은 거래량을 함께 볼 것", PANTS 사례)이 재차 적중했다.
- **LIZARD 소멸 여부 확인 결과**: 소멸되지 않았다. 3회차 연속 유동성 유출(누적 약 -20%)에도 불구 1시간 거래(71매수/70매도)는 여전히 활발하다. '유동성 위축'과 '완전 소멸'을 구분해 보고했다.
- **CYBERLEEK h1 부호 불일치**: DexScreener(-6.83%)와 GeckoTerminal(+10.95%)이 h1 부호에서 엇갈렸다(h6·h24는 방향·크기 모두 근접 일치). 스냅샷 시점 차이로 추정되나 원인 미확정, 정직 표기.
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API(체인별 배치조회)로 37개 활성종목(신규2건 포함)을 재확인했고, CATE는 페어 목록 전체 조회와 페어 단위 API로 최대거래량 풀을 재검증했다. Truth Coin(양체인)·LIZARD·OBS의 pairCreatedAt은 epoch ms를 직접 계산해 풀 나이를 검증했다(BARRON도 동일 방식으로 19개월 전 생성임을 확인). GeckoTerminal 트렌딩(솔라나·로빈후드체인)으로 신규 발굴 스캔을 진행해 CHUMP·BARRON을 확보했다. CONK·PANTS·Doge2·CYBERLEEK은 GT와 DS 교차검증으로 방향 일치를 확인했다(CYBERLEEK h1만 예외). X 직접 조회는 로그인월로 시도하지 않아 신규 2종 포함 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
