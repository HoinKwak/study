# 온체인 트렌딩 조기경보 — 2026-08-22 21:00 UTC (KST 2026-08-23 06:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-22 19:00Z)로부터 정확히 2시간 경과**(정상 간격). 33개 활성종목 전부와 CASHCAT(notable)을 DexScreener 토큰-페어 API로 개별 재조회했다.

> **🚨 MOONCOIN — 완전소멸/러그 확정, 활성목록에서 편출**
> 직전 회차(19:00Z)에 1차 붕괴(유동성 $571,820→$64,446, h24 +110%→-99.07%)가 확인됐던 MOONCOIN을 본 회차 재조회한 결과, 유동성이 완전히 증발했다. **DexScreener liquidity.usd = $0.23**(원본 JSON 숫자 재확인), **GeckoTerminal 풀상세 reserve_in_usd = $0.2434**, **GeckoTerminal 트렌딩목록 reserve_in_usd = $0.49**로 세 소스가 모두 사실상 0에 수렴했다. h1·h6·h24 전부 -100%(DS·GT 동일). 거래량24h는 DS$691,201~GT$43.4M로 잔존 표기되나 이는 유동성 증발 직전까지의 패닉매도 잔여치로 해석된다. P400·HEREBRO와 동일한 '조기편입 후 급격소멸' 패턴이 8~9회차째까지 생존해온 토큰에서도 재현된 사례다. **활성목록(tokens)에서 notable로 편출한다.**

> **⭐ 신규 발굴 1건 — LIZARD (4회차 만의 첫 신규 편입)**
> GeckoTerminal 트렌딩(Solana) 재스캔에서 LIZARD(Tom Lizard, Solana/PumpSwap)를 새로 포착했다. 풀 생성시각은 **GT `pool_created_at`=2026-08-21T23:03:50Z**와 **DS `pairCreatedAt` epoch 1787353430000ms(동일 시각으로 환산)**가 정확히 일치해 교차검증됐다(약 22시간 전 생성). 유동성 $56,513~$56,856(GT·DS 유사), 거래량24h ≈$2.42M, h1 +63~71%, h6 +20~25%, h24 **+612~1,208%**(GT·DS 간 표본시점 차이로 수치는 다르나 방향·규모는 일치). 회전율≈43배로 매우 높아 워시트레이딩 의심이 크고, 동일 티커의 무관한 별도 Raydium 풀(CA 347k5f1W...)도 존재해 티커 충돌 위험이 있다(이번 CA는 PumpSwap 풀 기준). **극초기·고위험, 신규진입 절대금지.**
>
> ⚠️ 참고로 GT 트렌딩에서 함께 눈에 띈 "Truth Coin"(Solana, 풀생성 2026-08-22T15:23Z)은 DexScreener 원시 JSON 확인 결과 **liquidity.usd = 0(base 0.01649/quote 1e-9)**·h1 거래량 0으로 **이미 유동성이 완전히 빠진 사후 상태**였다(과거 24h 거래량 $18.1M은 잔존 표기일 뿐). 붕괴한 풀은 편입하지 않는다는 원칙에 따라 편입하지 않았다.

## 부모 세션 최우선 확인 대상 후속 — KIRK·PANTS·40M

- **KIRK**: 회차 간 휩소가 또다시 반복됐다. h1 +18.46%→**-3.21%**(재음전전환), h6 -21.33%→**+3.19%**(재양전전환), h24 -39.49%→**-35.15%**(소폭개선). 9회차 연속 방향이 뒤집히는 패턴이며, 거래량도 -6.0%로 계속 감소해 관심이 식어가는 신호일 가능성이 있다.
- **PANTS**: h24가 +92.67%→**+35.85%**(-56.82%p)로 대폭 감속해 **직전 회차 경고했던 단기 고점 통과가 이번 회차에 확인됐다**. 유동성도 -4.4%로 유출 지속. 다수 풀 중 Meteora1(유동성 $171,980)이 PumpSwap($129,502)보다 유동성은 크지만, 거래량은 PumpSwap($1,763,653)이 Meteora1($123,445)의 약 14배로 압도적이라 PumpSwap을 주풀로 유지했다.
- **40M**: 소멸 경로가 더 심화됐다. 유동성 $17,988.74→**$15,529.63**(-13.7%, GT $16,250.45로 유사, 5단계 연속 감소 누적 -54.2%). h6 +26.77%→**-77.45%**, h24 +18.59%→**-86.29%**(GT -82.69%로 교차검증)로 두 지표가 동시에 극단 반전됐다. 거래량도 -70.7% 급감.

## 나머지 종목 갱신 (28종)

- **OBS**: 유동성 -14.5%, h1 -23.44%→**-6.54%**(개선), h6 -21.69%→**-46.19%**(대폭악화), h24 +535%→**+10.54%**(대폭감속,정상권근접). 🔴(유지).
- **TIPANSEM**: 유동성 -1.0%, h6 개선, h24 -40.49%→**-55.61%**(재악화심화). 🔴(유지).
- **1B**: 유동성 +7.2%, h1 -22.44%→**+43.68%**(대폭재양전), h24 +106%→**-3.59%**(극단반전). 🔴(유지, 극심한변동성).
- **CLOCKIN**: 유동성 -2.2%, h1 +5.89%→**-0.93%**(재음전), h6 개선, h24 소폭악화. 🔴(유지).
- **PEE**: 유동성 +2.5%, h24 +0.89%→**+2.70%**(개선). 🔴(유지, 거래극도로얇음).
- **CLUG**: 유동성 -3.1%, h1 재양전, h24 유사(-43.80%). 🔴(유지).
- **PEPECOIN**: ⚠️전지표 대폭 악화. 유동성 -14.8%, h1 재음전, h6 -1.22%→**-36.87%**, h24 -50.63%→**-62.14%**. 🔴(상향).
- **swappy**: 유동성 +0.3%, h6 개선(-6.84%). 🟡(유지).
- **CYBERLEEK**: 유동성 +14.1%(추가유입), h1 +66.05%→**-6.48%**(단기재음전), h6 감속(+150%), h24 +175%→**+244%**(추가가속). 거래량+50.2%. 🟡(하향, 단기눌림신호).
- **CC**: 유동성 -4.8%, h1 재음전, h24 -38.75%→**-44.67%**(악화). 🔴(고위험).
- **Z500**: 유동성 -3.8%, h6 개선, h24 +20.64%→**+7.43%**(감속,양전유지). 🟡(유지).
- **HOOKR**: 유동성 +0.4%, h1·h6 악화, h24 -46.65%→**-28.07%**(대폭개선). 🟡(하향).
- **CATE**: 유동성 +1.1%, h1 재음전, h24 유사(+53.56%,강세유지). 🟡(유지).
- **GOOD**: ⭐전지표 동시개선. 유동성 +7.2%, h1·h6 재양전전환, h24 -21.02%→**-3.74%**(대폭개선). 🟢(하향).
- **PRINTER**: 유동성 +0.3%, h24 -18.90%→**-16.33%**(개선). 🟡(유지).
- **BULLSHIT**: ⭐h6·h24 모두 재양전전환. PumpSwap유동성 +6.7%, h24 -1.56%→**+8.93%**. 🟡(유지, 개선).
- **TOAD**: 유동성 -1.6%, h1·h6 소폭악화, h24 유사. 🟡(유지).
- **DPG**: ⭐h6 대폭 재양전전환(-36.85%→**+7.67%**, +44.52%p). 🟡(하향).
- **FWA**: h24 3회차 연속 양전, 가속(+0.41%→**+5.32%**). 🟡(유지, 개선지속).
- **CALLOOOR**: 유동성 -3.4%, h24 개선(-14.57%). 🟡(유지).
- **JUGGERNAUT**: h1 재음전, h6 재양전, h24 개선(-16.3%). 🟡(유지).
- **BRODIE**: h1 미세재양전, h24 +5.67%→**+13.75%**(가속, 4회차연속양전). 🟢(유지).
- **Dealer**: h1 재음전, h24 +35.88%→**+22.66%**(감속,양전유지). 🟡(유지).
- **lickingcat**: ⚠️직전 회차 첫 개선이 다시 1회성으로 판명, 재악화. h24 -23.36%→**-37.68%**. 🔴(재상향).
- **PITCOIN**: h6 재음전, h1·h24는 양전유지(+7.91%). 🟡(유지).
- **FLUSH**: h1 재양전, h6 대폭개선(-49.01%→**-22.54%**), h24 여전히 극단(+458%). 🔴(유지).
- **CONK**: h1 재음전, h6 대폭가속(+38.58%), h24 여전히 극단(+2,178%). 🔴(유지, 극단수준).
- **MAPLE**: h6 재음전(+6.82%→**-10.43%**), h24 소폭개선(-47.89%). 🔴(유지).
- **Doge2**: ⚠️전지표 동시 대폭악화·감속. 유동성 -34.4%(대폭유출), h1 재음전, h6 악화, h24 +651%→**+231%**(-420%p). 🔴(상향).

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

| 토큰 | 체인/DEX | 단계 | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|---|
| **LIZARD** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | ⭐신규(4회차만의첫발굴). 풀생성22시간전,GT·DS교차검증 | 유동성$56,856.30, h24+612~1,208%, 회전율≈43배 | **신규** | 🔴(신규,매우높은위험) | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **40M** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 5회차. 소멸경로심화확정,h6·h24동시극단반전 | 유동성$15,529.63(누적-54.2%), h24-86.29%(GT-82.69%) | 지속(5회차)·소멸심화 | 🔴(소멸경로심화) | [DexScreener](https://dexscreener.com/solana/Ct6arp861CvmvsAZ4pse7ZyTS2dDexfz9Yv2G6ajeU5q) |
| **TIPANSEM** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 18회차. h24재악화심화 | 유동성$12,695.00(-1.0%), h24-55.61% | 지속(18회차)·재악화심화 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **MAPLE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 6회차. h6재음전,h24소폭개선 | 유동성$26,765.48(-14.5%), h24-47.89% | 지속(6회차)·혼조 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/7XA6NCMKa8Vk5Y3gdaaNsvGhjAdkqUDsGHkUpYUZBwh3) |
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 조기 | 미확인(코로보없음) | 20회차. 전지표대폭악화 | 유동성$19,860.56(-14.8%), h24-62.14% | 지속(20회차)·악화 | 🔴(상향) | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **OBS** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 12회차. h24대폭감속,정상권근접 | 유동성$44,461.35(-14.5%), h24+10.54% | 지속(12회차)·감속 | 🔴(매우초기) | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **FLUSH** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 8회차. h6대폭개선,h24극단수준유지 | 유동성$50,335.67(-0.6%), h24+458% | 지속(8회차)·개선 | 🔴(고위험) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **1B** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 10회차. h1대폭재양전,h24극단반전 | 유동성$32,016.20(+7.2%), h24-3.59% | 지속(10회차)·극단반전 | 🔴(극심한변동성) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLOCKIN** | Robinhood Chain | 조기 | 없음(자체서사만확인) | 30회차. 방향혼조 | 유동성$189,898.72(-2.2%), h24-35.66% | 지속(30회차)·혼조 | 🔴(유지) | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **PEE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 47회차. h24개선지속 | 유동성$9,576.71(+2.5%), h24+2.70% | 지속(47회차)·개선 | 🔴(신규진입절대금지) | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **CLUG** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 42회차. h1개선 | 유동성$38,054.74(-3.1%), h24-43.80% | 지속(42회차) | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **CONK** | Solana(Raydium) | 확산 | 미확인(코로보없음) | 7회차. h6대폭가속,h24극단수준유지 | 유동성$116,066.54(+0.5%), h24+2,178% | 지속(7회차)·극단 | 🔴(극단수준지속) | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CC** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 20회차. 20회차째방향번복,h24악화전환 | 유동성$106,595.95(-4.8%), h24-44.67% | 지속(20회차)·악화 | 🔴(고위험,워시트레이딩의심) | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **KIRK** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 10회차. 회차간휩소재반복 | 유동성$75,331.79(-2.9%), h24-35.15% | 지속(10회차)·휩소재반복 | 🔴(거래량계속감소) | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **swappy** | Robinhood Chain(Uniswap V4) | 확산 | 미확인(코로보없음) | 23회차. 대체로보합 | 유동성$214,667.14(+0.3%), h24-19.42% | 지속(23회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 확산 | 미확인(코로보없음) | 22회차. 5회차연속재반등,h1단기재음전 | 유동성$845,386.88(+14.1%), h24+244% | 지속(22회차)·눌림신호 | 🟡(하향,단기눌림가능성) | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **Z500** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 13회차. h6개선,h24감속 | 유동성$87,659.20(-3.8%), h24+7.43% | 지속(13회차)·감속 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **Doge2** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 5회차. 전지표동시대폭악화·감속 | 유동성$33,091.40(-34.4%), h24+231% | 지속(5회차)·악화 | 🔴(상향,대폭악화) | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 84회차. 강세유지 | 유동성$2,076,458(+1.1%), h24+53.56% | 지속(84회차) | 🟡(유지,회전율10배근접) | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 뒷북 | 미확인(코로보없음) | 25회차. h24대폭개선 | 유동성$195,087.87(+0.4%), h24-28.07% | 지속(25회차)·개선 | 🟡(하향) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **GOOD** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 26회차. 전지표동시개선 | 유동성$470,866.64(+7.2%), h24-3.74% | 지속(26회차)·개선 | 🟢(하향) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 뒷북 | 미확인(코로보없음) | 161회차. 개선지속 | 유동성$371,880.38(+0.3%), h24-16.33% | 지속(161회차)·개선 | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **BULLSHIT** | Solana(Meteora 등 11개풀) | 뒷북 | 미확인(WebSearch로토큰명특정보도없음) | 41회차. h6·h24모두재양전전환 | 유동성(PumpSwap)$252,860.59, h24+8.93% | 지속(41회차)·개선 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **TOAD** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 160회차. 소폭악화 | 유동성$371,528(-1.6%), h24-8.75% | 지속(160회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **DPG** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 112회차. h6대폭재양전전환 | 유동성$93,951.74(+0.5%), h24+25.89% | 지속(112회차)·개선 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **FWA** | Ethereum(Uniswap V4) | 뒷북 | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover)+CG트렌딩12위(carryover) | 164회차. h24 3회차연속양전,가속 | 유동성$1,172,035.79(+6.6%), h24+5.32% | 지속(164회차)·가속 | 🟡(유지) | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **CALLOOOR** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 110회차. 소폭개선 | 유동성$55,770.51(-3.4%), h24-14.57% | 지속(110회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **JUGGERNAUT** | Robinhood Chain(Uniswap V3 1%) | 뒷북 | Drallio(약한코로보,carryover) | 147회차. h24개선 | 유동성$246,581.50(유사), h24-16.3% | 지속(147회차)·개선 | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 123회차. h24가속,4회차연속양전 | 유동성$168,954.69(-0.5%), h24+13.75% | 지속(123회차)·가속 | 🟢(유지) | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **Dealer** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 152회차. h24감속,양전유지 | 유동성$121,596.05(-2.0%), h24+22.66% | 지속(152회차)·감속 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 152회차. 첫개선이1회성으로판명,재악화 | 유동성$52,560.70(-4.8%), h24-37.68% | 지속(152회차)·재악화 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **PITCOIN** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 113회차. h6재음전,h1·h24양전유지 | 유동성$31,826.93(+0.4%), h24+7.91% | 지속(113회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 12회차재확인(dogwifpants). 단기고점통과확인 | 유동성$129,502.60(-4.4%), h24+35.85%(-56.82%p) | 지속(12회차)·고점통과 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |

> **편입/편출 내역(이번 회차)**: **신규 편입 1건**(LIZARD, 4회차 만의 첫 신규 발굴), **편출 1건**(MOONCOIN, 완전소멸/러그확정으로 notable 이관). 활성목록 **33종 유지**(32종 재확인 + LIZARD 신규). **급격 상향(위험 확대) 3건**: MOONCOIN(완전소멸,편출), PEPECOIN(전지표동시악화), Doge2(전지표동시대폭악화·감속). **재상향 1건**: lickingcat(첫개선이1회성으로판명,재악화). **하향(위험 완화) 3건**: HOOKR(h24대폭개선), GOOD(전지표동시개선), DPG(h6대폭재양전전환), CYBERLEEK(단기눌림신호로소폭하향).

## 온체인 신호 상세

- **MOONCOIN(편출)·LIZARD(신규) 상세**: MOONCOIN 유동성이 DS$0.23·GT풀$0.2434·GT트렌딩$0.49로세소스모두사실상0에수렴,h1·h6·h24전부-100%로완전소멸확정,notable로이관. LIZARD는GT트렌딩(Solana)재스캔에서포착,풀생성시각GT`2026-08-21T23:03:50Z`·DS epoch1787353430000ms가정확히일치(약22시간전),유동성$56,513~$56,856,h24+612~1,208%,회전율≈43배로매우높아워시트레이딩의심,무관한별도Raydium동명풀존재로티커충돌위험도기록 · 2026-08-22T21:00Z
- **부모세션최우선확인대상(KIRK·PANTS·40M) 후속**: KIRK h1·h6모두재반전(**-3.21%/+3.19%**)하는9회차째휩소지속,거래량-6.0%감소. PANTS h24**+35.85%**로대폭감속,단기고점통과확인(유동성-4.4%유출). 40M유동성**$15,529.63**로5단계연속감소(누적-54.2%),h6·h24동시극단반전(**-77.45%/-86.29%**,GT-82.69%교차검증),거래량-70.7%급감 · 2026-08-22T21:00Z
- **나머지 27건 상세**: OBS h24**+10.54%**로대폭감속(정상권근접)하나h6는**-46.19%**로대폭악화. TIPANSEM h24**-55.61%**로재악화심화. 1B h1**+43.68%**대폭재양전하나h24는**-3.59%**로극단반전. CLOCKIN방향혼조지속. PEE h24**+2.70%**개선. CLUG h1재양전,h24유사. PEPECOIN전지표대폭악화(h6**-36.87%**,h24**-62.14%**). swappy대체로보합. CYBERLEEK유동성+14.1%유입·h24**+244%**추가가속이나h1**-6.48%**단기재음전으로눌림가능성. CC h24**-44.67%**로악화. Z500h24**+7.43%**로감속하나양전유지. HOOKR h24**-28.07%**로대폭개선. CATE강세유지(h24**+53.56%**). GOOD전지표동시개선,h6재양전(**+9.32%**). PRINTER h24**-16.33%**로개선지속. BULLSHIT h6·h24모두재양전전환(**+6.63%/+8.93%**). TOAD소폭악화. DPG h6**+7.67%**로대폭재양전전환. FWA h24 3회차연속양전,가속(**+5.32%**). CALLOOOR소폭개선. JUGGERNAUT h24개선(**-16.3%**). BRODIE h24 4회차연속양전,가속(**+13.75%**). Dealer h24**+22.66%**로감속하나양전유지. lickingcat직전첫개선이1회성판명,h24**-37.68%**로재악화. PITCOIN h6재음전하나h1·h24양전유지. FLUSH h6대폭개선(**-22.54%**),h24여전히극단(**+458%**). CONK h6대폭가속(**+38.58%**),h24여전히극단(**+2,178%**). MAPLE h6재음전(**-10.43%**). Doge2전지표동시대폭악화(유동성-34.4%,h24**+231%**로-420%p대폭감속) · 2026-08-22T21:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **나머지 30종(신규 LIZARD 포함, 부모세션 최우선 확인대상 포함) — 코로보 미확인**: 이번 회차는 33개 활성종목 전부와 CASHCAT(notable)을 DexScreener 토큰-페어 API로 개별 재조회하고 GeckoTerminal 트렌딩 API(Solana·Robinhood)로 신규발굴을 재시도(LIZARD 1건 발견)하는 데 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-22 19:00Z)로부터 정확히 2시간 경과(정상 간격).
- **🚨 MOONCOIN 완전소멸 확정**: DexScreener·GeckoTerminal 풀상세·GeckoTerminal 트렌딩 세 소스 모두 유동성이 $0.23~$0.49 수준으로 수렴해 완전한 소멸(러그 가능성 포함)을 확정하고 활성목록에서 notable로 편출했다. 8~9회차째까지 생존한 토큰도 급격 붕괴할 수 있음을 다시 보여준 사례.
- **⭐신규 발굴 1건(LIZARD)**: 3회차 연속 신규 발굴 없음 상태를 깨고 GeckoTerminal 트렌딩(Solana) 재스캔에서 LIZARD를 포착했다. 풀 생성시각을 GT·DS 두 소스의 raw epoch 값으로 교차검증해 약 22시간 전 생성됨을 확인했다(극초기 관측이력없음 아님, 이미 24시간에 육박하는 실거래 이력 보유). 회전율 43배로 워시트레이딩 의심이 크고 동명 무관 Raydium 풀도 존재해 극도로 주의가 필요하다. 함께 발견된 "Truth Coin"은 DexScreener 원시 유동성 필드가 0으로 확인돼(이미 붕괴한 풀) 편입하지 않았다.
- **⚠️부모세션 최우선 지시(KIRK·PANTS·40M) 후속확인 결과**: KIRK는 9회차째 방향이 계속 뒤집히는 휩소가 지속되고 거래량도 계속 감소해 관심이 식어가는 신호일 가능성이 있다. PANTS는 h24가 대폭 감속해 직전 회차 경고했던 단기 고점 통과가 확인됐다. 40M은 5단계 연속 유동성·h24 동시 감소로 소멸 경로가 더 심화됐다(GT로 재차 교차검증).
- **데이터 신뢰도**: 이번 회차는 33개 활성종목 전부와 CASHCAT(notable)을 DexScreener 토큰-페어 API로 개별 재조회했다. WebFetch 소형모델 요약이 MOONCOIN·LIZARD 풀생성시각을 최초에 오독(각각 "2025-04-18"·부호반전 등)했으나, raw JSON 필드(pairCreatedAt epoch, liquidity 객체 세부값)를 직접 재확인하는 절차로 전부 정정·교차검증했다 — 소형모델 WebFetch 요약은 항상 원시 필드 재확인이 필요함을 재확인한 사례. PANTS·40M·KIRK는 부모 세션이 명시한 시장배경과는 별개로 DexScreener 다중 페어 전체를 재조회해 주풀(거래량 기준)을 재확인했다. X 직접 조회는 로그인월로 시도하지 않아 KOL 코로보는 전 종목 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
