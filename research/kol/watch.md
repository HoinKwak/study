# 온체인 트렌딩 조기경보 — 2026-08-26 03:00 UTC (KST 2026-08-26 12:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 01:00Z)로부터 **정상 2시간** 경과. 유실 없이 정상 진행됐다.

44개 활성종목 전부를 DexScreener 배치조회(chainId별 tokens/v1 다중주소 API, 로빈후드 1배치 15·솔라나 2배치 14+14·이더리움 1배치 1)로 재확인했다. 추가로 GeckoTerminal 로빈후드체인 트렌딩(top20)·솔라나 트렌딩(top20)·우선추적과제(Swan·Pistacio·BARK·DTF·AI/NVDA(BANKR)·TRUTH·PEE) 개별 풀 조회를 수행해 다수 notable 항목도 함께 교차확인했다.

## 이번 회차 핵심 발견

**DTF(notable) — ⚠️⚠️⚠️⚠️h24가 이 워치 사상 최저치로 대폭붕괴**: h24가 +9,312.58%(01:00Z)→**+465.324%**로 급락했다. 이는 그동안의 회차 추이(7,206%→10,775%[최고]→10,358%→7,394%→8,891%→8,278%→9,313%→**465%[현재,최저]**)에서 처음으로 세 자릿수%대로 진입한 것이다. DS 교차확인(h24 +474%)도 방향·규모를 일치시켜 데이터 오류가 아님을 확인했다. 풀 나이가 약 25.4시간(2026-08-25T01:35:27Z 생성, 부모 정정 — 리포트 최초 기재는 33.4시간이었음)으로 24시간을 갓 넘어서면서, 24시간 전 비교기준가격이 초기 극단 스파이크 구간을 완전히 벗어난 것으로 해석된다. 유동성·h1·h6는 오히려 대폭 가속(+16.7%,+17.2%,+47.0%)해 h24 지표만 특이적으로 붕괴한 것이 이 해석을 뒷받침한다.

**Pistacio(notable) — ⭐최초로 h6≠h24 분리 확인**: 풀 나이가 약 7.6시간(6시간 경과)이 되면서 그동안 동일 수치였던 h6·h24가 처음으로 분리됐다(h6 +444.999% vs h24 +25,320.94%). 풀 나이가 6시간을 넘어서면서 h6는 실제 6시간 전 가격을 참조하기 시작했으나 h24는 여전히 24시간 미만이라 풀 생성 시점 가격을 계속 참조하는 구조적 차이로 해석된다. DS도 근접한 값(h6 +445.08%, h24 +25,324.94%)을 반환해 교차확인됐다.

**PROLOGUE — ⚠️6연속 양전 스트릭 종료**: 직전 회차까지 6연속 양전을 이어가던 h24가 이번 회차 -6.00%로 재음전했다. 유동성·h1은 여전히 양전이나 h24 반전으로 🟢에서 🟡로 하향 재조정한다.

**TRUTH — ⚠️⚠️3회차 연속 DS값 완전동일, DS캐시의심으로 해석 확정**: 유동성($73,902.88)·h1(0%)·h24(+48.71%)가 3회차 연속 소수점까지 완전 동일하게 반환됐다. 이번 회차 GT 풀을 재조회한 결과 reserve $74,600.46(직전 GT $73,882.93 대비 미세 변동)·h6 -1.29%·h24 +49.8%로 GT는 실제로 움직이고 있었고, **24시간 거래가 14,276건 매수/11,229건 매도로 매우 활발**함을 확인했다. 즉 실거래는 왕성한데 DS API 값만 얼어붙어 있는 것으로, 데이터 갱신 여부 의심을 넘어 **DS값 캐시/지연반환 문제로 해석을 확정**한다.

**PEE — 유사 패턴 재확인**: 유동성이 직전 회차와 소수점까지 완전 동일($7,221.25)했다. GT 재조회 시 reserve $7,278.47(소폭 상이)·24h 거래 77/92건 확인, TRUTH와 유사하되 정도는 약한 데이터 경계 사례로 함께 기록한다.

**AI/NVDA(BANKR, notable) — ⚠️⚠️4회차 연속 DS-GT 매칭 불일치, 괴리 추가확대**: DS는 이번 회차도 동일 CA·풀을 'Artificial Inu'(심볼 AI, liquidity $1,989,427.51)로 반환했다. GT 값($4,972,185.04)과의 괴리가 약 **2.50배**로 직전(2.46배)보다 추가 확대됐다 — 구조적 라벨링 불일치 판단을 유지한다.

**Swan(notable) — 2회차 재확인, GT-DS 괴리 6.7배 수준 유지**: GT h24 +10,708.734%, DS h24 +71,505%로 괴리비율이 직전(약 6.7배)과 거의 동일(약 6.68배)하게 유지됐다. 유동성은 GT·DS 둘 다 소폭 유출(-6.0%,-5.7%)했다. 풀 나이는 약 8.8시간(2026-08-25T18:12:54Z 생성).

**JUGGERNAUT — ⭐h1 2회차 연속 재양전**: 182회차 만에 처음 재양전했던 h1이 이번 회차도 양전(+5.95%)을 유지해 처음으로 2회차 연속 양전을 기록했다. h6·h24도 함께 개선됐다.

**PITCOIN — 3차 스파이크 냉각 국면 진입**: h1·h6가 재음전으로 대폭반전했고 h24도 +114%→+104%로 감속했다. 3번째 스파이크가 이번 회차부터 식어가는 초기 신호로 판단한다.

**DPG — 전지표 동시 대폭악화**: 유동성 -18.0%, h1·h6 재음전, h24 -66.05%로 전방위 악화가 확정됐다.

**FWA — 200회차 달성**.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 48회차. 유입반전,전지표동시재양전·개선 | 유동성$107,631.35(+6.1%), h24-24.63%(대폭악화) | 지속(47회차)·유입반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 56회차. 유입반전,h1가속h6감속h24는개선 | 유동성$14,066.54(+8.6%), h24-41.21%(개선) | 지속(55회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 42회차. 유출반전,h1재음전h6h24는유사 | 유동성$27,420(-3.6%), h24-12.09%(유사) | 지속(41회차)·유출반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 66회차. 유입반전,전지표동시재양전·개선 | 유동성$187,538.79(+5.0%), h24-25.48%(개선) | 지속(65회차)·전지표재양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 54회차. 유출지속,h1h6는개선h24는감속 | 유동성$13,343.29(-5.5%), h24+12.51%(감속) | 지속(53회차)·스파이크반전2회연속 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 37회차. 유입지속,h1가속h6개선h24는악화 | 유동성$30,785.03(+2.3%), h24-16.37%(악화) | 지속(36회차)·개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 46회차. 대폭유입반전,전지표동시재양전·대폭개선 | 유동성$19,911.80(+12.1%), h24-20.96%(대폭개선) | 지속(45회차)·전지표재양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 78회차. 유출반전,h1h6는혼조h24는대폭악화 | 유동성$25,369.7(-1.8%), h24-45.98%(대폭악화) | 지속(77회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 44회차. 유출지속,전지표개선(여전히음전) | 유동성$16,824.53(-2.7%), h24-34.17%(개선) | 지속(43회차)·전지표개선 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 83회차. ⚠️유동성DS값3회연속완전동일 | 유동성$7,221.25(0.0%), h24-13.83%(악화) | 지속(82회차)·데이터경계 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 41회차. 유출반전,h1재음전h6유사h24는악화 | 유동성$9,163.68(-3.4%), h24-41.64%(악화) | 지속(40회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 30회차. 유입반전,h1재양전h6가속h24는개선 | 유동성$41,473.20(+7.6%), h24-27.03%(개선) | 지속(29회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 27회차. 유동성유사,전지표개선(여전히극단음전) | 유동성$12,635.62(-0.2%), h24-71.99%(개선) | 지속(26회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 30회차. 유출지속,h1유사h6악화h24는개선 | 유동성$90,341.46(-3.7%), h24-30.77%(개선) | 지속(29회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 59회차. ⭐h6h24대폭가속(2회차연속강세) | 유동성$202,403.60(-0.03%), h24+43.49%(대폭가속) | 지속(58회차)·2연속강세 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 58회차. 유출반전,h1감속h6재양전h24는개선 | 유동성$1,560,760.66(-1.4%), h24-8.82%(개선) | 지속(57회차)·개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 56회차째방향번복. 유출반전,h1감속h6개선h24는유사 | 유동성$243,388.93(-0.5%), h24-30.26%(유사) | 지속(55회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 49회차. 유출지속,h1악화h6유사h24는개선 | 유동성$71,292.56(-2.3%), h24-17.92%(개선) | 지속(48회차)·whipsaw지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 46회차. 유동성유사,h1개선h6h24는가속(양전유지) | 유동성$79,233.65(+1.0%), h24+10.38%(가속,양전유지) | 지속(45회차)·양전유지 | 🟢 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 43회차. 유동성유사,h1h6는개선h24는대폭가속(양전유지) | 유동성$71,222.97(-0.6%), h24+57.69%(대폭가속) | 지속(42회차)·개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/DShht9B8wCRe5t3oqdPB77PnjJbKxbYaZyuWpZQjbonk) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 34회차. 유입반전,h1h24재양전대폭반전h6는유사 | 유동성$396,638.38(+3.5%), h24+11.99%(재양전,대폭반전) | 지속(33회차)·재차완전반전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 27회차. 유출지속,h1h6재음전대폭반전h24는여전히거의완전소멸고착 | 유동성$7,195.16(-11.7%), h24-95.91%(고착) | 지속(26회차)·h24고착 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 26회차. ⚠️6연속양전스트릭종료(h24재음전) | 유동성$241,665.59(+0.1%), h24-6.00%(재음전,대폭반전) | 지속(25회차)·스트릭종료 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 32회차. ⚠️⚠️DS값3회연속완전동일,DS캐시의심확정 | 유동성$73,902.88(0.0%), h24+48.71%(동일) | 지속(31회차)·DS캐시의심 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 31회차. 대폭유입반전,전지표동시가속·재양전 | 유동성$21,256.47(+13.9%), h24+15.2%(재양전,대폭반전) | 지속(30회차)·전지표재양전 | 🟡 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 61회차. 대폭유입반전,h1가속h6재양전h24는개선 | 유동성$454,147.42(+12.1%), h24-6.72%(개선) | 지속(60회차)·강세 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 183회차. ⭐h1 2회차연속재양전 | 유동성$427,035.78(+5.3%), h24-17.91%(개선) | 지속(182회차)·h1 2연속양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 159회차. 대폭유입반전,전지표동시재양전·대폭가속 | 유동성$235,831.53(+11.3%), h24+61.37%(대폭가속,양전유지) | 지속(158회차)·전지표재양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 62회차. 유입반전,h1재양전h6개선h24는개선 | 유동성$529,461.42(+3.9%), h24-11.02%(개선) | 지속(61회차)·전지표개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 197회차. 유입반전,h1재양전h6h24는재가속 | 유동성$492,189.20(+8.5%), h24+91.24%(대폭가속) | 지속(196회차)·감속흐름역전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 188회차. 유출반전,h1재음전h6유사h24는악화 | 유동성$80,734.21(-1.6%), h24-16.75%(악화) | 지속(187회차)·재음전 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 188회차. 유입반전,전지표동시개선(여전히전량음전) | 유동성$34,732.71(+2.3%), h24-40.84%(개선) | 지속(187회차)·전지표개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 146회차. 유입반전,h1감속h6재양전h24는대폭개선 | 유동성$67,085.01(+4.5%), h24-16.73%(대폭개선) | 지속(145회차)·개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 196회차. 유출반전,h1재음전h6재양전h24는유사 | 유동성$347,674.81(-0.8%), h24-18.8%(유사) | 지속(195회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 200회차달성. 유입지속,h6h24는개선 | 유동성$1,169,222.39(+2.6%), h24-20.09%(개선) | 지속(199회차)·200회차달성 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 148회차. 대폭유출반전,전지표동시재음전·대폭악화 | 유동성$38,048.79(-18.0%), h24-66.05%(대폭악화) | 지속(147회차)·전지표대폭악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 77회차. 유입반전,h1유사h6재양전h24는악화 | 유동성$226,019.01(+1.7%), h24-27.8%(악화) | 지속(76회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 150회차. h1h6재음전대폭반전,h24는감속(양전유지) | 유동성$55,790.9(+1.5%), h24+104%(감속,양전유지) | 지속(149회차)·3차스파이크냉각 | 🔴 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 48회차(dogwifpants). 유출반전,h1유사h6h24는악화 | 유동성$65,820.22(-3.5%), h24-44.41%(유사) | 지속(47회차)·유사 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 41회차. 대폭유입반전,전지표동시재양전·대폭개선 | 유동성$67,823.63(+15.4%), h24-3.22%(대폭개선) | 지속(40회차)·전지표재양전 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 35회차. 유출지속,h1재양전h6유사h24는개선 | 유동성$8,180.23(-1.6%), h24-12.67%(개선) | 지속(34회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 34회차. 유동성유사,h1재양전h6h24는개선 | 유동성$213,906.79(+0.6%), h24-10.85%(개선) | 지속(33회차)·소폭개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 33회차. 유출반전,전지표동시재음전·악화 | 유동성$19,614.53(-9.7%), h24-40.25%(악화) | 지속(32회차)·지그재그 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |
| **CATE** | Solana(PumpSwap) | 미확인 | 120회차달성. 유입반전,h6h24는대폭개선 | 유동성$2,249,603.63(+2.2%), h24-3.1%(대폭개선) | 지속(119회차)·장기whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |

> **편입/편출/강등/재승격 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. **강등 1건**(PROLOGUE 🟢→🟡, 6연속양전스트릭종료). 활성목록 **44→44종**(순증감 0, 조기13/확산10/뒷북21). notable **69→69개**(신규 0건, 전량갱신·carryover 혼재). **핵심 이벤트**: DTF h24가 사상최저치(+465%)로 대폭붕괴(24h윈도우아티팩트해소로해석), Pistacio가최초로h6≠h24분리, TRUTH·PEE의DS값완전동일이3회차연속·2회차확인돼DS캐시의심으로해석확정(GT·실거래량으로교차검증), AI/NVDA(BANKR)의GT-DS매칭불일치4회차연속·괴리2.50배로확대, PROLOGUE6연속양전스트릭종료, JUGGERNAUT h1 2회차연속재양전(182회차만에처음), PITCOIN3차스파이크냉각조짐, DPG전지표대폭악화, FWA200회차달성.

## 온체인 신호 상세

- **DTF(notable) 사상최저치 상세**: GT reserve$187,703.31→$218,970.28(+16.7%,대폭유입지속), h1-0.355%→+17.184%(재양전,대폭반전), h6+7.996%→+46.955%(대폭가속), h24+9,312.58%→+465.324%(대폭붕괴,사상최저). DS교차확인: liquidity$236,546.3·h1+10.85%·h6+40.01%·h24+474%. 회차추이: 7,206%→10,775%[최고]→10,358%→7,394%→8,891%→8,278%→9,313%→465%[현재,최저]. 풀나이약25.4시간(2026-08-25T01:35:27Z생성, 부모정정) · 2026-08-26T03:00:00Z
- **Pistacio(notable) h6≠h24분리 상세**: GT reserve$368,294.17→$360,176.53(-2.2%,유출반전), h1-19.814%→-18.407%(유사,여전히음전), h6/h24 +27,244.756%(동일)→h6+444.999%/h24+25,320.94%(최초분리). DS교차확인(reserve$359,315.76,h1-18.40%,h6+445.08%,h24+25,324.94%)근접일치. 풀나이약7.6시간(2026-08-25T19:22:21Z생성) · 2026-08-26T03:00:00Z
- **TRUTH DS캐시의심 상세**: DS 유동성$73,902.88→$73,902.88(0.0%,3회연속완전동일), h1 0%→0%(완전동일), h24+48.71%→+48.71%(완전동일). GT재조회: reserve$74,600.46(직전$73,882.93대비미세변동)·h6-1.29%·h24+49.8%. 24h거래14,276건매수/11,229건매도로실거래매우활발 · 2026-08-26T03:00:00Z
- **PEE 데이터경계 상세**: DS 유동성$7,221.25→$7,221.25(0.0%,완전동일). GT재조회: reserve$7,278.47(소폭상이)·h6-1.21%·h24-12.13%, 24h거래77건/92건확인 · 2026-08-26T03:00:00Z
- **AI/NVDA(BANKR, notable) 상세**: GT reserve$4,356,923.30→$4,972,185.04(+14.1%,대폭유입반전), h1+2.037%→+1.764%(유사,양전유지), h6-5.078%→+25.061%(재양전,대폭반전), h24+24.799%→+38.301%(대폭가속). DS동일CA·동일풀재조회시4회차연속'Artificial Inu'(liquidity$1,989,427.51)매칭,괴리약2.50배로추가확대 · 2026-08-26T03:00:00Z
- **Swan(notable) 상세**: GT reserve$78,596.548→$73,885.90(-6.0%,유출반전), h1-4.936%→+8.743%(재양전,대폭반전), h6+14.749%→-9.126%(재음전,대폭반전), h24+12,175.967%→+10,708.734%(감속). DS: reserve$78,591.01→$74,109.94(-5.7%,유출반전), h1-3.5%→+8.76%(재양전,대폭반전), h6+43.17%→-6.99%(재음전,대폭반전), h24+81,649%→+71,505%(감속). 괴리71,505/10,709≈6.68배(직전과거의동일). 풀나이약8.8시간(2026-08-25T18:12:54Z생성) · 2026-08-26T03:00:00Z
- **BARK(notable) 상세**: GT reserve$13,922.80→$14,628.49(+5.1%,유입반전), h1-46.42%→+7.00%(재양전,대폭반전), h6-50.541%→-64.125%(대폭악화), h24-24.063%→-15.119%(개선,여전히음전). 풀나이약13.4시간(2026-08-25T13:33:34Z생성) · 2026-08-26T03:00:00Z
- **PROLOGUE 스트릭종료 상세**: 유동성$241,361.14→$241,665.59(+0.1%,사실상동일), h1+5.38%→+2.93%(감속,양전유지), h6-6.25%→-5.23%(유사), h24+22.22%→-6.00%(재음전,대폭반전,6연속양전종료) · 2026-08-26T03:00:00Z
- **JUGGERNAUT h1 2연속양전 상세**: 유동성$405,483.33→$427,035.78(+5.3%,유입반전,둔화), h1+10.99%→+5.95%(감속,양전유지,2연속), h6-25.54%→-8.26%(대폭개선), h24-26.51%→-17.91%(개선). GT재확인(reserve$427,774)근접일치 · 2026-08-26T03:00:00Z
- **PITCOIN 3차스파이크냉각 상세**: 유동성$54,963.36→$55,790.9(+1.5%,유사), h1+5.35%→-7.33%(재음전,대폭반전), h6+85.67%→-4.93%(재음전,대폭반전), h24+114%→+104%(감속,양전유지) · 2026-08-26T03:00:00Z
- **DPG전지표대폭악화 상세**: 유동성$46,383.2→$38,048.79(-18.0%,대폭유출반전), h1+1.33%→-31.63%(재음전,대폭반전), h6+7.35%→-33.21%(재음전,대폭반전), h24-43.71%→-66.05%(대폭악화) · 2026-08-26T03:00:00Z
- **CASHCAT(notable) 두풀상세**: 1%풀 reserve$4,352,294.85→약$4.50M(+3.4%,유입반전),h24-16.924%→-7.8%(대폭개선). 0.3%풀 reserve$2,130,519.07→약$2.16M(+1.4%,유입지속),h24-16.792%→-7.2%(대폭개선) · 2026-08-26T03:00:00Z
- **나머지 상세**: OBS전지표재양전. PEPECOIN개선. MAPLE혼조. CLOCKIN전지표재양전. LIZARD개선. 1B전지표재양전. CLUG악화. FLUSH전지표개선. PEE데이터경계. 40M악화. MANEKI혼조. CYBERCAT개선. omo개선. swappy2연속강세. CYBERLEEK개선. CC워시트레이딩의심불변. Z500whipsaw지속. KIRK양전유지. CONK개선. CHUMP재차완전반전. CATALORIAN고착. HOOKR강세. BRODIE전지표재양전. GOOD전지표개선. PRINTER감속역전. Dealer재음전. lickingcat전지표개선. CALLOOOR개선. TOAD혼조. FWA200회차. BULLSHIT혼조. PANTS유사. Doge2전지표재양전. Truth Coin개선. BARRON소폭개선. YOMOGI지그재그. CATE대폭개선 · 2026-08-26T03:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **TRUTH — 직전 회차 발견한 관련 가능성 있는 루머 보도(carryover 유지, 신규 없음, 동일 토큰 여부 여전히 불확실)**.
- **나머지 40종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 DexScreener 배치조회 재확인, GT 트렌딩(로빈후드체인 top20·솔라나 top20) 교차검증, 우선추적과제(Swan·Pistacio·BARK·DTF·AI/NVDA(BANKR)·TRUTH·PEE) 개별 풀 재확인에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 01:00Z)로부터 **정상 2시간** 경과, 유실 없음.
- **저장 후 세 파일(json·csv·md) 종목 목록 대조**: tokens(json) 44종·csv 44행(헤더 제외)·md 3개 표(조기13+확산10+뒷북21=44) 전부 일치 확인함(OBS~PROLOGUE까지 개별 이름 대조 완료).
- **DTF의 h24가 이 워치 사상 최저치(+465%)로 붕괴한 것은 러그가 아니라 24시간 비교기준가격이 초기 극단 스파이크 구간을 완전히 벗어난 결과로 해석한다**: 유동성·h1·h6는 오히려 가속했다. DS도 동일 방향·규모(+474%)로 교차확인됐다.
- **Pistacio의 h6·h24 분리는 풀 나이가 6시간을 넘으면서 나타난 구조적(아티팩트) 현상으로 판단한다**: 24시간 미만 풀에서는 h24가 여전히 풀 생성 시점 가격을 참조해 h6와 크게 벌어질 수 있다.
- **TRUTH의 DS값이 3회차 연속 완전동일하게 반환된 것을 이번 회차 GT·거래량 교차검증으로 'DS API 캐시/지연반환' 문제로 해석을 확정한다**: 24시간 거래 2만5천여 건으로 실거래는 매우 활발하다. PEE도 유사(약한) 패턴을 보여 함께 기록했다. 이는 데이터 신뢰도 문제이지 토큰 자체의 문제가 아니므로, 향후 회차에서 DS값이 계속 고정되면 GT 값을 우선 채택하는 방향을 검토한다.
- **AI/NVDA(BANKR)의 GT-DS 매칭 불일치가 4회차 연속 재현되며 괴리가 계속 확대되고 있다**(2.38배→2.46배→2.50배): 구조적 라벨링 불일치로 판단을 확정한다.
- **PROLOGUE의 6연속 양전 스트릭이 이번 회차 종료됐다**: 리스크를 🟢에서 🟡로 하향 재조정했다.
- **데이터 신뢰도**: DexScreener 배치조회(로빈후드15·솔라나14+14·이더리움1)와 GeckoTerminal 트렌딩(로빈후드체인 top20·솔라나 top20)·개별 풀 조회로 교차검증했다. CYBERLEEK·CATE·JUGGERNAUT·GOOD·HOOKR·MANEKI는 DS-GT 양쪽 값이 근접해 신뢰도가 높다. PROLOGUE는 GT가 이번 회차도 다른(소규모) 풀만 노출해 DS 메인풀 값을 채택했다. AI/NVDA(BANKR)·Swan은 DS-GT 매칭·수치 괴리가 크게 확인돼 신뢰도 경계 사례로 지속 기록한다. TRUTH·PEE는 DS값 고정(캐시의심) 사례로 신규 경계를 추가했다. X 직접 조회는 로그인월로 대부분 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
