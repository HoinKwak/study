# 온체인 트렌딩 조기경보 — 2026-08-25 11:00 UTC (KST 2026-08-25 20:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-25 09:00Z)로부터 **정상 2시간** 경과. 유실 없이 정상 진행됐다.

44개 활성종목 전부를 DexScreener 배치조회(chainId별 tokens/v1 다중주소 API, 로빈후드 1배치 15/솔라나 2배치 14+14/이더리움 1배치 1)로 재확인했다. 요청 개수와 응답 개수가 전부 일치했다. 추가로 GeckoTerminal 솔라나 트렌딩(top20, 2페이지)·로빈후드체인 트렌딩(top20, 2페이지)을 조회해 다수 notable 항목을 교차확인하고, 직전 회차에서 이어받은 우선추적과제(BATON·Meeko·TILLY·솔라나신규풀군5종·TRENCHERS·PCAT·PROLOGUE)를 전부 개별 재조회했다. 특히 직전 회차에 이월된 **솔라나 신규풀군 5종(FROGE·ARCHITECTURE·beluga·AHTS·trickshot)의 DS-CA 교차검증을 이번 회차에 완료**했다.

## 이번 회차 핵심 발견

**TRUTH — 4회차 연속 완전동일이던 데이터가 돌연 대폭 재활성화**: 직전까지 4회차 연속 유동성 값이 완전히 동일해(무거래 추정) 데이터 신뢰도를 경고해왔는데, 이번 회차 유동성이 $48,693.63→$112,134.89(+130.3%)로 급변하고 h1·h6·h24 전부 새로 측정되며 h24는 -67.82%→+405.00%로 완전 반전했다. 동일 CA(0x2ec5cc87…)를 재확인했으나 이 급변의 원인(실거래 재개인지 풀 구조 변경인지)은 규명하지 못했다 — 정직 기록하며 다음 회차 재확인이 필수다.

**Allocate(notable) — 3회차 연속 "거의 완전소멸" 선언 뒤 대폭 반등**: 직전 3회차 연속 붕괴 상태(유동성 -95.5%→추가 -23.1%)를 확인해왔는데, 이번 회차 유동성이 $5,345.98→$157,802.01(+2,851%)로 대폭 반등하고 h24도 -96.00%→+94.019%로 완전 반전했다. 극단적 저유동 토큰의 변동성 한계 사례로 정직 기록하며, 실질 회복 여부는 단정하지 않는다.

**PCAT(notable) — 저베이스 아티팩트 가설의 마지막 단계 완주**: 직전 회차 h24 대폭 감속(+926%→+137%)을 "저베이스 효과 해소 중"으로 판단했는데, 이번 회차 h24가 +137%→-34.27%로 완전히 음전 전환됐다. 유동성도 -17.3%(유출 반전)로 함께 악화했다 — Allocate에 이어 "극단 초기치→감속→반전"의 전 과정을 완주한 두 번째 사례다.

**Z500 — 3연속 완전반전**: 두 회차 연속 완전반전(재양전↔재음전)이 이어져 예측 불가 패턴이 확정됐다.

**솔라나 신규풀군 5종 — DS-CA 교차검증 완료, 방향 엇갈림**: FROGE·ARCHITECTURE·beluga·AHTS·trickshot 전부 baseToken CA를 DexScreener로 교차확인했다. FROGE는 낙폭이 완화됐고(h24 -58.08%→-38.18%), beluga는 뚜렷이 가속(h24 +1.48%→+18~24%)했으나 trickshot은 오히려 더 악화(h24 -21.43%→-47~48%)했다.

**BATON·Meeko·TILLY — 2회차째 확인, 전부 h24 대폭 감속**: BATON h24 +3,996%→+1,523~1,751%, Meeko h24 +296%→+49~102%, TILLY h24 +704%→+60~73%로 모두 초기 극단치가 큰 폭으로 꺾였다. BATON·Meeko는 유동성도 유출로 전환(-30% 안팎)했으나 TILLY는 오히려 유입이 지속(+19~25%)돼 같은 군 내에서도 방향이 갈렸다.

## 🚨 우선추적과제 재확인

**TRENCHERS(notable) — 3회차재확인, 생존하나 첫 제동**: 유동성 -8.6%(첫 유출반전), h6 +70.42%→+10.16%(대폭감속), h24 +578%→+466%(감속). 여전히 극조기 단계(풀나이 약 12.2시간)라 P400·HEREBRO 선례처럼 급붕괴 가능성을 계속 경계한다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 40회차. 유출반전,h1재음전h6대폭악화 | 유동성$112,165.22(-8.1%), h24+16.37%(대폭감속) | 지속(39회차)·유출반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 48회차. 유입반전,h1재양전h6h24대폭개선 | 유동성$15,956.23(+8.1%), h24-31.73%(대폭개선) | 지속(47회차)·대폭개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 34회차. 유출반전,전지표재음전(3회차만에재반전) | 유동성$27,388.18(-11.8%), h24-2.49%(재음전,대폭반전) | 지속(33회차)·재반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 58회차. 유사,h1개선h6대폭악화 | 유동성$204,663.20(-2.2%), h24+3.05%(감속) | 지속(57회차)·58회차째whipsaw | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 46회차. 유출반전,h1h6재음전대폭반전 | 유동성$11,625.50(-13.8%), h24-39.70%(악화) | 지속(45회차)·whipsaw재발 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 29회차. 유사,h1재음전h6재양전 | 유동성$33,957.73(+0.9%), h24-28.18%(유사) | 지속(28회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 38회차. 유사,h1h6감속h24개선 | 유동성$24,769.47(-2.1%), h24-19.82%(개선) | 지속(37회차)·단정금지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 70회차. 유출지속,h6개선h24는추가악화 | 유동성$32,179.49(-3.1%), h24-25.48%(추가악화) | 지속(69회차)·혼조지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 36회차. 유출지속이멈추고유입반전 | 유동성$20,912.54(+4.3%), h24-47.54%(개선) | 지속(35회차)·유입반전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 75회차. 유사,h1h6개선h24감속 | 유동성$7,792.27(-1.6%), h24+3.37%(감속) | 지속(74회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 33회차. 유사,h1재음전h24개선 | 유동성$12,522.40(-2.3%), h24-3.53%(개선) | 지속(32회차)·약세혼조 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 22회차. ⭐유입지속,h1대폭재양전(+42.27%) | 유동성$42,310.13(+2.5%), h24-47.76%(개선) | 지속(21회차)·2연속개선 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 19회차. 유출지속,h1재음전h24는유사 | 유동성$20,537.72(-10.9%), h24-83.71%(유사) | 지속(18회차)·유출지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 22회차. 유입반전,h1대폭재양전h6개선 | 유동성$102,002.40(+2.4%), h24-25.55%(유사) | 지속(21회차)·유입반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 51회차. 유입지속,h1대폭재양전h6가속 | 유동성$184,539.02(+5.9%), h24-17.01%(개선) | 지속(50회차)·전지표개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 50회차. 유입,h1대폭가속h6재양전대폭반전 | 유동성$1,630,949.35(+7.3%), h24-32.29%(개선) | 지속(49회차)·전지표개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 48회차째방향번복. 유입반전,h1대폭재양전 | 유동성$274,349.36(+3.8%), h24-30.45%(유사) | 지속(47회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 41회차. ⭐3연속완전반전,유출반전+전지표재음전 | 유동성$79,588.66(-3.8%), h24+2.44%(대폭감속) | 지속(40회차)·3연속재반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 38회차. 4연속유입streak종료·유출반전 | 유동성$78,444.10(-5.0%), h24+8.19%(대폭감속) | 지속(37회차)·유출반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 35회차. 유입지속,h24대폭개선(손익분기근접) | 유동성$68,355.89(+9.7%), h24-3.14%(대폭개선) | 지속(34회차)·대폭개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 26회차. 유사,h6재양전h24감속 | 유동성$384,749.62(-1.1%), h24+23.73%(감속) | 지속(25회차)·유사 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 19회차. 유입흐름종료·유출반전(대폭) | 유동성$27,686.69(-22.7%), h24-97.01%(유사) | 지속(18회차)·유출반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 18회차. ⚠️유출지속3연속,h24대폭감속 | 유동성$237,647.62(-3.2%), h24+52.92%(대폭감속) | 지속(17회차)·3연속조정 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 24회차. ⭐4회차연속동일이던값돌연대폭변화 | 유동성$112,134.89(+130.3%), h24+405.00%(완전반전) | 지속(23회차)·수치급변 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 23회차. 유입,h1재양전h6가속 | 유동성$22,103.85(+4.2%), h24-12.32%(대폭개선) | 지속(22회차)·대폭개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 53회차. 유사,h6재음전h24는가속 | 유동성$483,913.34(-2.0%), h24+45.29%(가속) | 지속(52회차)·가속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 175회차. 유출지속,h1악화h24대폭감속 | 유동성$440,389.39(-3.5%), h24+56.56%(대폭감속) | 지속(174회차)·유출지속 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 151회차. 직전대폭가속이단1회차만에유출반전 | 유동성$211,645.98(-13.5%), h24+14.18%(대폭감속) | 지속(150회차)·재차반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 54회차. 유사,h1재음전h24감속 | 유동성$542,098.45(-2.4%), h24+24.33%(감속) | 지속(53회차)·감속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 189회차. 유입반전멈추고유출반전,h1h6대폭반전 | 유동성$439,939.14(-3.5%), h24+60.70%(대폭감속) | 지속(188회차)·조정 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 180회차. 유사,h1재양전h24개선 | 유동성$93,149.38(+1.8%), h24-31.05%(개선) | 지속(179회차)·연속whipsaw이력상단정금지 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 180회차. 10회차연속지그재그 | 유동성$49,302.14(+1.3%), h24-46.55%(악화) | 지속(179회차)·10회차연속지그재그 | 🟡 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 138회차. 유사,h1악화h6재음전 | 유동성$72,841.02(-2.8%), h24+4.47%(대폭감속) | 지속(137회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 188회차. 유사,h1재음전h6개선 | 유동성$367,648.70(-0.9%), h24-7.87%(유사) | 지속(187회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 192회차. 유입반전,h1재양전h24가속 | 유동성$1,336,816.87(+3.0%), h24+12.81%(가속) | 지속(191회차)·유입반전 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 140회차. ⚠️유출반전(대폭),h6h24동시대폭악화 | 유동성$50,678.32(-22.0%), h24-50.42%(악화,대폭) | 지속(139회차)·급격악화 | 🟡 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 69회차. 유출반전,h24는감속(거의평탄) | 유동성$239,257.22(-5.6%), h24+0.07%(감속,거의평탄) | 지속(68회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 33회차. 유입지속(4연속),h1재양전h6h24가속 | 유동성$79,967.46(+2.8%), h24+163.00%(가속) | 지속(32회차)·4연속유입 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 112회차달성. 유사,h1재음전h24감속 | 유동성$2,318,306.86(+0.8%), h24+75.10%(감속) | 지속(111회차)·장기whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 40회차(dogwifpants). 유입지속멈추고유출반전 | 유동성$87,140.32(-5.5%), h24-32.91%(악화) | 지속(39회차)·유출반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 27회차. 유입반전,h1가속h6재양전 | 유동성$8,314.34(+2.9%), h24-29.57%(개선) | 지속(26회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 26회차. 유사,h1재음전h6개선 | 유동성$221,757.97(-0.9%), h24-5.52%(유사) | 지속(25회차)·유사 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 25회차. 유사,h1재음전h6h24개선 | 유동성$24,567.82(+0.8%), h24-18.69%(개선) | 지속(24회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. 활성목록 **44→44종**(순증감 0). notable **56→57개**(신규 1건: TINY, 나머지는 GT/DS 재확인 갱신 또는 carryover). **핵심 이벤트**: TRUTH가 4회차 연속 데이터 동결 뒤 돌연 대폭 재활성화, Allocate(notable)가 3회차 연속 붕괴 선언 뒤 대폭 반등, PCAT(notable)가 저베이스 아티팩트 가설의 마지막 단계(h24 완전 음전 전환)를 완주, Z500이 3연속 완전반전, 솔라나 신규풀군 5종의 DS-CA 교차검증이 완료됐다.

## 온체인 신호 상세

- **TRUTH 데이터급변 상세**: 유동성+130.3%(대폭변화), h1측정불가→+61.50%, h6측정불가→+398.00%, h24-67.82%→+405.00%(완전반전,대폭). 동일CA(0x2ec5cc87…) 재확인, 원인미규명 · 2026-08-25T11:00:00Z
- **Allocate(notable) 대폭반등 상세**: 유동성$5,345.98→$157,802.01(+2,851%), h1+0.042%(거의평탄), h6-1.965%(유사), h24-96.00%→+94.019%(완전반전,대폭). 3회차연속붕괴선언뒤반등 · 2026-08-25T11:00:00Z
- **PCAT(notable) 완전반전 상세**: 유동성-17.3%(유출반전), h1+33.38%→-14.37%(재음전,대폭반전), h6+44.38%→+23.21%(감속), h24+137%→-34.27%(완전반전,음전전환) · 2026-08-25T11:00:00Z
- **Z500 3연속재반전 상세**: 유동성-3.8%(유출반전), h1+6.57%→-8.39%(재음전,대폭반전), h6+7.12%→-2.95%(재음전,대폭반전), h24+11.67%→+2.44%(대폭감속) · 2026-08-25T11:00:00Z
- **솔라나신규풀군 DS-CA교차검증 상세**: FROGE(CA DCop3mFzWn1wJL9J9cTZ2K8xF7YH14q7LaUhsuyQpump, liquidity$13,185.33, h24-38.18%,낙폭완화) · ARCHITECTURE(CA AP8Wnu37Gf9RHgugPKGvpHe6LcTE2yp5GDy7pL5Upump, liquidity$29,556.98, h24+172~194%,유사) · beluga(CA 4qHAqsakh8oBgDpSHccmPHV4rPZDq1MgrQnsZ1QZpump, liquidity$27,793.44, h24+18~24%,가속) · AHTS(CA CxThkADKK4DDYqB8GBPaEAgRBzwxyPyUhFcBUmiAzN6N, liquidity$33,425.62, h24+237~261%,유사) · trickshot(CA DRWnf86Z2MjdMGLq7LFSF875iK9Ajo94RVtjK4owpump, liquidity$38,028.36, h24-47~48%,추가악화) · 2026-08-25T11:00:00Z
- **BATON·Meeko·TILLY 2회차재확인 상세**: BATON h24+3,996%→+1,523~1,751%(대폭감속),유동성-31.7%(유출). Meeko h24+296%→+49~102%(대폭감속),유동성-31.2~-30.5%(유출). TILLY h24+704%→+60~73%(대폭감속),유동성+19~25%(유입지속) · 2026-08-25T11:00:00Z
- **TRENCHERS(notable) 3회차재확인 상세**: 유동성-8.6%(첫유출반전), h1+11.79%→+4.63%(감속), h6+70.42%→+10.16%(대폭감속), h24+578%→+466%(감속) · 2026-08-25T11:00:00Z
- **나머지 상세**: OBS유출반전. PEPECOIN대폭개선. MAPLE재반전. CLOCKIN58회차째whipsaw. TIPANSEM whipsaw재발. LIZARD혼조. 1B단정금지. CLUG혼조지속. FLUSH유입반전. PEE개선. 40M약세혼조. MANEKI2연속개선. CYBERCAT유출지속. omo유입반전. swappy전지표개선. CYBERLEEK전지표개선. CC방향번복지속. KIRK유출반전. CONK대폭개선. CHUMP유사. CATALORIAN유출반전. PROLOGUE3연속조정. Dinger대폭개선. HOOKR가속. GOOD감속. PRINTER조정. Dealer연속whipsaw이력상단정금지. lickingcat10회차연속지그재그. CALLOOOR혼조. TOAD혼조. FWA유입반전. DPG급격악화. BULLSHIT혼조. JUGGERNAUT유출지속. BRODIE재차반전. PITCOIN감속. PANTS유출반전. Doge2 4연속유입. Truth Coin개선. BARRON유사. YOMOGI개선 · 2026-08-25T11:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 40종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 DexScreener 배치조회 재확인, GT 트렌딩(솔라나·로빈후드체인 각 top20) 교차검증, 우선추적과제(BATON·Meeko·TILLY·솔라나신규풀군5종·TRENCHERS·PCAT·PROLOGUE) 개별 재조회에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-25 09:00Z)로부터 **정상 2시간** 경과, 유실 없음.
- **DexScreener 배치조회 전량 정상 응답**: 로빈후드 1배치(15)·솔라나 2배치(14+14)·이더리움 1배치(1) 총 4개 배치 전부 요청 개수와 응답 개수가 일치했다.
- **TRUTH 수치급변은 원인 미규명 상태로 정직 기록**: 4회차 연속 완전동일하던 데이터가 갑자기 급변한 것은 실거래 재개일 수도, 풀/데이터 소스 구조 변경일 수도 있어 단정하지 않는다. 다음 회차 재확인이 필수다.
- **극단적 저유동 토큰의 변동성 한계가 재확인됨**: Allocate(notable)가 3회차 연속 "거의 완전소멸"로 선언됐다가 이번 회차 유동성이 30배 가까이 급증했다. 매우 낮은 절대 유동성 구간에서는 소액 거래 하나로도 %변화가 극단적으로 튈 수 있다는 이 워치의 기존 경고가 재확인된 사례다.
- **저베이스 아티팩트 가설이 두 번째로 전 과정 완주(Allocate·PCAT)**: 두 사례 모두 "극단 초기치 → 감속 → 완전반전"의 3단계를 순서대로 거쳤다. BATON·Meeko·TILLY는 현재 2단계(대폭감속)에 있어 다음 회차에 3단계(완전반전) 여부를 지켜본다.
- **솔라나 신규풀군 5종의 DS-CA 교차검증을 완료**해 직전 회차로 이월했던 숙제를 해소했다. 방향은 엇갈려(FROGE 완화, beluga 가속, trickshot 추가악화, ARCHITECTURE·AHTS 유사) 단일 패턴으로 일반화하지 않는다.
- **whipsaw 지속을 단정적 신호로 해석하지 않음**: Z500(3연속완전반전)·MAPLE(직전대폭반전이단1회차만에재반전)·BRODIE(직전대폭가속이단1회차만에반전)는 이 워치에서 반복적으로 관찰되는 패턴이라 대칭원칙에 따라 판정을 유지했다.
- **데이터 신뢰도**: DexScreener 배치조회와 GeckoTerminal 트렌딩(솔라나·로빈후드체인 top20, 각 2페이지) 교차검증으로 다수 종목의 방향성 일치를 확인했다. TRENCHERS·PCAT·솔라나신규풀군5종은 DS 직접조회로 GT 값과 교차검증했다. AI/NVDA(BANKR)는 이번 회차 GT만 재확인하고 DS는 미실시해 기존 DS-GT 괴리 재확인은 다음 회차로 넘긴다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
