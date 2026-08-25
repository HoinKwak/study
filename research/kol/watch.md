# 온체인 트렌딩 조기경보 — 2026-08-25 13:00 UTC (KST 2026-08-25 22:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-25 11:00Z)로부터 **정상 2시간** 경과. 유실 없이 정상 진행됐다.

44개 활성종목 전부를 DexScreener 배치조회(chainId별 tokens/v1 다중주소 API, 로빈후드 2배치 8+7·솔라나 2배치 14+14·이더리움 1배치 1)로 재확인했다. 요청 개수와 응답 개수가 전부 일치했다. 추가로 GeckoTerminal 솔라나 트렌딩(top20, 2페이지)·로빈후드체인 트렌딩(top20, 2페이지)을 조회해 다수 notable 항목을 교차확인하고, 직전 회차에서 이어받은 우선추적과제(AI/NVDA(BANKR) DS재확인·TRUTH재확인·PCAT·Allocate·TINY·BATON·Meeko·TILLY)를 전부 개별 재조회했다.

## 이번 회차 핵심 발견

**AI/NVDA(BANKR) — DS 재확인 완료(5회차째, 숙제 해소)**: 4회차 연속 이월됐던 DS 재확인을 이번 회차에 마쳤다. DS: 유동성$1,803,524.70, h1+6%·h6-13.99%·h24+9.77%. 같은 시각 GT: reserve$4,469,178.76, h1+6.5%·h6-12.1%·h24+14.0%. DS-GT 비율은 약 **2.48배**로 직전(약 2.4배)과 유사한 수준이 지속됐다 — 데이터 오류라기보다 두 소스가 반영하는 유동성 풀 범위가 구조적으로 다른 것으로 해석하며, 정직하게 기록한다.

**TRUTH — 2회차 연속 대폭 가속, 일회성 아님을 확인**: 직전 회차 돌연 급변(+130.3%, h24 완전반전)이 데이터 오류인지 진짜 재활성화인지 불확실했는데, 이번 회차도 유동성 +59.7%·h24 +405%→+1,046%로 **또다시 큰 폭으로 가속**했다. 2회차 연속 같은 방향으로 움직인 것은 일회성 데이터 이상 가능성을 낮추지만, WebSearch로 원인(실거래 재개 vs Robinhood Chain 관련 보도)을 찾았으나 TRUTH 토큰을 특정한 보도는 발견하지 못했다(재확인 실패, 정직 표기) — 원인은 여전히 미규명이다.

**Allocate(notable) — ⭐⭐⭐대폭 재붕괴, 4단계 요동 완주**: 직전 회차 3회차 연속 붕괴 선언 뒤 +2,851% 대폭 반등했었는데, 이번 회차 **단 1회차 만에 다시 -96.2%로 대폭 붕괴**했다(유동성 $157,802.01→$5,993.38). h24도 +94.019%→-95.646%로 재차 완전반전. "붕괴→붕괴→붕괴→대폭반등→다시대폭붕괴"의 4단계 요동은 이 워치가 반복 경고해온 "매우 낮은 절대 유동성 구간에서는 소액 거래 하나로도 %변화가 극단적으로 튈 수 있다"는 한계를 가장 극적으로 재확인한 사례다.

**TILLY — 저베이스 아티팩트 가설의 세 번째 완주 사례**: BATON·Meeko와 달리 유동성 유입이 지속되던 유일한 종목이었는데, 이번 회차 유출로 반전(-19.7%)하며 h24가 +73.34%→-10.019%로 **완전히 음전 전환**됐다. Allocate·PCAT에 이어 "극단 초기치→감속→완전반전" 전 과정을 완주한 세 번째 사례다.

**PROLOGUE — 확산에서 뒷북으로 강등**: 직전 회차부터 강등 검토 대상이었는데, 이번 회차 **4연속 유출**·h24 대폭 감속(+52.92%→+11.44%)이 확정되며 확산에서 뒷북으로 강등했다. GT 재확인(reserve$149,188.66)도 같은 방향이지만 DS($215,704.42)와 약 1.45배 괴리가 있어 소스간 규모 차이를 계속 경계한다.

**CONK — h24 최초 완전 양전 전환**: 장기간 음전권에 머물던 CONK가 이번 회차 대폭 유입(+14.6%)과 함께 h24가 -3.14%→+43.18%로 **처음으로 완전히 플러스 전환**됐다. 단 1회차뿐이라 대칭원칙상 즉시 상향하지 않고 다음 회차 연속 확인 후 판단한다.

**BATON — 티커 충돌 신규 발견**: BATON을 GT 트렌딩에서 재확인하는 과정에서 같은 'BATON' 티커의 별개 풀(baseToken CA `9firESEtMrb4hqFxtb7xCAXp4jAuoW8mz5MZwjJ2pump`, reserve$34,339.57)이 추가로 포착됐다. Dinger·CATSZN과 유사한 티커 충돌 사례로 기록만 하고 이 별개 풀은 편입하지 않는다.

**신규 발견 3건**: SEYONGPARK(Solana, 풀생성 약 8.4시간 전, h24+1,171.44%), CNPY(Robinhood Chain, 풀생성 약 1.5개월 전 재활성화, h24+436.5%), DTF(Robinhood Chain, 풀생성 약 11.4시간 전, h24+7,206.2% — 이 워치에서 관측된 h24 수치 중 최상위권으로 저베이스 아티팩트 가능성이 매우 높아 최고위험으로 경계).

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 41회차. 유입반전,h1h6개선 | 유동성$114,908.24(+2.4%), h24+12.47%(감속) | 지속(40회차)·유입반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 49회차. 유입지속,h6대폭개선h24는악화 | 유동성$16,243.62(+1.8%), h24-38.28%(악화) | 지속(48회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 35회차. 대폭유입반전,전지표재양전 | 유동성$33,635.30(+22.8%), h24+3.08%(재양전) | 지속(34회차)·재반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 59회차. 유출반전,전지표악화 | 유동성$195,121.06(-4.7%), h24-3.91%(재음전) | 지속(58회차)·59회차째whipsaw | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 47회차. 유입반전,h1h6대폭반전 | 유동성$12,757.41(+9.7%), h24-25.64%(개선) | 지속(46회차)·whipsaw재발 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 30회차. 유동성유사,h1재양전h6감속 | 유동성$33,200.39(-2.2%), h24-41.61%(악화) | 지속(29회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 39회차. 유동성유사,h1재음전 | 유동성$24,568.06(-0.8%), h24-26.89%(악화) | 지속(38회차)·단정금지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 71회차. 유출지속,h24는개선 | 유동성$31,321.59(-2.7%), h24-21.08%(개선) | 지속(70회차)·혼조지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 37회차. 전지표동시개선 | 유동성$20,654.16(-1.2%), h24-37.95%(개선) | 지속(36회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 76회차. 유동성유사,혼조 | 유동성$7,752.29(-0.5%), h24+2.83%(유사) | 지속(75회차)·유사 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 34회차. 유출,h6재음전대폭악화 | 유동성$11,531.73(-7.9%), h24-19.13%(악화) | 지속(33회차)·약세혼조 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 23회차. 유입지속,h24대폭개선(3연속) | 유동성$45,598.53(+7.8%), h24-35.64%(대폭개선) | 지속(22회차)·3연속개선 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 20회차. 유입반전,h6악화h24유사 | 유동성$22,090.34(+7.6%), h24-82.63%(유사) | 지속(19회차)·유입반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (9종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 23회차. 유입지속,h1대폭가속h24대폭개선 | 유동성$107,215.14(+5.1%), h24-11.79%(대폭개선) | 지속(22회차)·대폭개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 52회차. 유입지속,h1대폭감속 | 유동성$190,273.85(+3.1%), h24-16.37%(개선) | 지속(51회차)·유입지속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 51회차. 유동성유사,h1대폭반전재음전 | 유동성$1,624,772.58(-0.4%), h24-34.20%(유사) | 지속(50회차)·재음전 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 49회차째방향번복. 유출반전 | 유동성$267,549.91(-2.5%), h24-32.84%(유사) | 지속(48회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 42회차. ⭐4연속완전반전,유입반전 | 유동성$83,860.55(+5.4%), h24+3.67%(유사) | 지속(41회차)·4연속재반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 39회차. 유동성유사,h1재양전대폭반전 | 유동성$77,613.90(-1.1%), h24+15.00%(가속) | 지속(38회차)·재양전 | 🟡 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 36회차. ⭐h24최초완전양전전환 | 유동성$78,316.19(+14.6%), h24+43.18%(완전반전) | 지속(35회차)·양전전환 | 🔴 | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 27회차. 유출반전,h24감속 | 유동성$373,032.12(-3.0%), h24+17.37%(감속) | 지속(26회차)·유출반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 20회차. 유입반전,h6대폭개선 | 유동성$28,428.09(+2.7%), h24-93.60%(개선) | 지속(19회차)·유입반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |

### 뒷북 (22종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 25회차. ⭐⭐2회차연속대폭가속 | 유동성$179,126.63(+59.7%), h24+1,046%(대폭가속) | 지속(24회차)·대폭가속지속 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 24회차. 유출반전,h24악화 | 유동성$19,979.71(-9.6%), h24-30.23%(악화) | 지속(23회차)·유출반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 54회차. 유출반전,h24대폭감속 | 유동성$441,335.78(-8.8%), h24+11.65%(대폭감속) | 지속(53회차)·유출반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 176회차. 유출지속,h24감속 | 유동성$426,756.55(-3.1%), h24+41.71%(감속) | 지속(175회차)·유출지속 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 152회차. 유입반전,전지표개선·가속 | 유동성$225,514.25(+6.6%), h24+58.15%(대폭가속) | 지속(151회차)·재차반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 55회차. 유출반전,h24대폭감속 | 유동성$521,586.30(-3.8%), h24+12.77%(대폭감속) | 지속(54회차)·감속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 190회차. h1h6대폭개선h24감속 | 유동성$438,369.50(-0.4%), h24+50.72%(감속) | 지속(189회차)·조정 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 181회차. 유출반전,h1h6재음전 | 유동성$89,351.56(-4.1%), h24-31.03%(유사) | 지속(180회차)·연속whipsaw이력상단정금지 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 181회차. 11회차연속지그재그 | 유동성$50,005.94(+1.4%), h24-38.66%(개선) | 지속(180회차)·11회차연속지그재그 | 🟡 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 139회차. 유동성유사,h24감속 | 유동성$71,628.27(-1.7%), h24+2.97%(감속) | 지속(138회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 189회차. h1개선h6재양전h24개선 | 유동성$372,213.84(+1.2%), h24-4.42%(개선) | 지속(188회차)·개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 193회차. ⚠️192회차유입streak종료·유출반전 | 유동성$1,246,613.76(-6.7%), h24-5.48%(재음전,대폭반전) | 지속(192회차)·유출반전 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 141회차. 유출지속,h24악화 | 유동성$48,378.22(-4.5%), h24-54.89%(악화) | 지속(140회차)·약세지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 70회차. h1재양전대폭반전h24재음전 | 유동성$241,679.31(+1.0%), h24-3.52%(재음전) | 지속(69회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 34회차. ⚠️4연속유입종료·유출반전 | 유동성$70,757.15(-11.5%), h24+57.21%(대폭감속) | 지속(33회차)·유출반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 113회차달성. 유입,h1대폭반전 | 유동성$2,510,032.86(+8.3%), h24+98.23%(가속) | 지속(112회차)·장기whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 41회차(dogwifpants). 유입반전 | 유동성$89,156.76(+2.3%), h24-37.15%(악화) | 지속(40회차)·유입반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 28회차. 유동성유사,h1재음전 | 유동성$8,254.15(-0.7%), h24-35.3%(악화) | 지속(27회차)·재음전 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 27회차. 유동성유사,h24대폭악화 | 유동성$217,907.62(-1.7%), h24-21.53%(악화,대폭) | 지속(26회차)·유사 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 26회차. 유입반전,h1재양전대폭반전 | 유동성$25,191.55(+2.5%), h24-23.28%(악화) | 지속(25회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 19회차. ⚠️확산에서뒷북으로강등,4연속유출 | 유동성$215,704.42(-9.2%), h24+11.44%(대폭감속) | 지속(18회차)·확산에서뒷북으로강등 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. **강등 1건**: PROLOGUE(확산→뒷북, 4연속유출·h24대폭감속으로확정). 활성목록 **44→44종**(순증감 0). notable **57→60개**(신규 3건: SEYONGPARK·CNPY·DTF, 나머지는 GT/DS 재확인 갱신 또는 carryover). **핵심 이벤트**: AI/NVDA(BANKR) DS재확인숙제해소(DS-GT괴리약2.48배지속확인), TRUTH가 2회차연속대폭가속(원인은여전히미규명), Allocate가재붕괴(-96.2%)로4단계요동완주, TILLY가저베이스아티팩트가설의세번째완주사례, CONK가h24최초완전양전전환, BATON에서티커충돌신규발견.

## 온체인 신호 상세

- **AI/NVDA(BANKR) DS재확인 상세**: DS liquidity$1,803,524.70·h1+6%·h6-13.99%·h24+9.77%. 同시각GT reserve$4,469,178.76·h1+6.5%·h6-12.1%·h24+14.0%. DS-GT비율≈2.48배(직전약2.4배와유사) · 2026-08-25T13:00:00Z
- **TRUTH 2회차연속가속 상세**: 유동성+59.7%(대폭유입지속), h1+61.50%→+133%(대폭가속), h6+398.00%→+1,050%(대폭가속), h24+405.00%→+1,046%(대폭가속). WebSearch로원인탐색했으나TRUTH특정보도미발견(재확인실패) · 2026-08-25T13:00:00Z
- **Allocate(notable) 재붕괴 상세**: 유동성$157,802.01→$5,993.38(-96.2%,대폭유출반전), h1+0.042%→-11.778%(재음전), h6-1.965%→-21.225%(악화), h24+94.019%→-95.646%(완전반전,대폭). 붕괴→붕괴→붕괴→대폭반등→재붕괴의4단계요동완주 · 2026-08-25T13:00:00Z
- **TILLY(notable) 완전반전 상세**: 유동성-19.7%(유출반전), h1+43.275%→-5.939%(재음전,대폭반전), h6+50.923%→+10.771%(대폭감속), h24+73.34%→-10.019%(완전반전,음전전환). 저베이스아티팩트가설세번째완주사례(Allocate·PCAT에이어) · 2026-08-25T13:00:00Z
- **PCAT(notable) 완전반전심화 상세**: 유동성-13.4%(유출지속), h1-14.37%→-14.18%(유사), h6+23.21%→-40.99%(재음전,대폭악화), h24-34.27%→-71.88%(악화,대폭). 재반등없이단조악화지속 · 2026-08-25T13:00:00Z
- **CONK h24완전양전전환 상세**: 유동성+14.6%(대폭유입지속), h1+9.86%→+18.43%(가속), h6+24.06%→+81.37%(대폭가속), h24-3.14%→+43.18%(완전반전,대폭양전) · 2026-08-25T13:00:00Z
- **PROLOGUE 강등 상세**: 유동성-9.2%(유출지속4연속), h1+7.00%→-9.41%(재음전,대폭반전), h6-16.89%→-35.79%(악화,대폭), h24+52.92%→+11.44%(대폭감속). GT재확인(reserve$149,188.66)도유사방향이나DS와약1.45배괴리 · 2026-08-25T13:00:00Z
- **BATON(notable) 티커충돌 상세**: GT트렌딩에별개'BATON'풀(baseToken CA 9firESEtMrb4hqFxtb7xCAXp4jAuoW8mz5MZwjJ2pump, reserve$34,339.57, h24+1,121.52%)이추가로포착됨. 원래추적중인BATON(6Hebn672…)은유동성+9.6%·h24+2,124.61%로재가속 · 2026-08-25T13:00:00Z
- **신규발견 3건 상세**: SEYONGPARK(Solana, pool 7omGD2o8rjoQRRzpvv5fqXUCwGiivPrLJGjXLDpJq5wX, reserve$64,869.86, 풀생성2026-08-25T04:36:16Z,h24+1,171.44%) · CNPY(Robinhood Chain, pool 0xd05d2c3d696fcb893aee6607e3652accd2aedf97, reserve$137,855.91, 풀생성2026-07-11T17:25:44Z,h24+436.524%) · DTF(Robinhood Chain, pool 0xbc58bfe115b23f22d2e97ded5c791ebf6db3d3f510f412908c511da6dc8cb4ee, reserve$165,581.69, 풀생성2026-08-25T01:35:27Z,h24+7,206.213%,이워치역대최상위권h24수치) · 2026-08-25T13:00:00Z
- **나머지 상세**: OBS유입반전. PEPECOIN혼조. MAPLE대폭재반전. CLOCKIN유출반전. TIPANSEM whipsaw재발. LIZARD혼조. 1B단정금지. CLUG혼조지속. FLUSH전지표개선. PEE유사. 40M약세혼조. MANEKI3연속개선. CYBERCAT유입반전. omo대폭개선. swappy유입지속. CYBERLEEK재음전. CC방향번복지속. Z500 4연속완전반전. KIRK재양전. CHUMP유출반전. CATALORIAN유입반전. Dinger유출반전. HOOKR유출반전. CATE유입가속. GOOD유출반전. PRINTER조정. Dealer연속whipsaw이력상단정금지. lickingcat11회차연속지그재그. CALLOOOR혼조. TOAD개선. DPG약세지속. BULLSHIT혼조. JUGGERNAUT유출지속. BRODIE재차반전. PITCOIN대폭가속. PANTS유입반전. Doge2유출반전. Truth Coin재음전. BARRON대폭악화. YOMOGI개선 · 2026-08-25T13:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **TRUTH — WebSearch로 원인 탐색을 시도했으나 TRUTH 토큰을 특정한 보도를 찾지 못함(재확인 실패, 정직 표기)**.
- **나머지 39종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 DexScreener 배치조회 재확인, GT 트렌딩(솔라나·로빈후드체인 각 top20, 2페이지) 교차검증, 우선추적과제(AI/NVDA(BANKR) DS재확인·TRUTH·PCAT·Allocate·TINY·BATON·Meeko·TILLY) 개별 재조회에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-25 11:00Z)로부터 **정상 2시간** 경과, 유실 없음.
- **DexScreener 배치조회 전량 정상 응답**: 로빈후드 2배치(8+7)·솔라나 2배치(14+14)·이더리움 1배치(1) 총 5개 배치 전부 요청 개수와 응답 개수가 일치했다.
- **AI/NVDA(BANKR) DS-GT괴리 숙제 해소**: 4회차 연속 이월됐던 DS 재확인을 완료했다. 괴리 비율(약 2.48배)이 직전 회차(약 2.4배)와 유사한 수준으로 유지돼, 두 소스가 반영하는 유동성 풀 범위가 구조적으로 다를 가능성이 높다고 판단한다.
- **TRUTH 수치급변은 여전히 원인 미규명**: 2회차 연속 같은 방향(대폭 가속)으로 움직여 일회성 데이터 오류 가능성은 낮아졌으나, WebSearch로도 특정 원인을 찾지 못했다. 다음 회차도 계속 재확인한다.
- **저베이스 아티팩트 가설이 세 번째로 전 과정 완주(Allocate·PCAT·TILLY)**: 세 사례 모두 "극단 초기치 → 감속 → 완전반전"의 3단계를 순서대로 거쳤다. 특히 Allocate는 반전 이후 재붕괴까지 4단계 요동을 보여 극단적 저유동 토큰의 변동성 한계를 가장 극적으로 보여준 사례다.
- **PROLOGUE가 이 워치에서 확산→뒷북 강등이 명시적으로 기록된 사례**: 직전 회차 "강등검토대상"으로 표기했던 것이 이번 회차 4연속 유출 확정으로 실제 강등됐다. 향후 유사 판정 시 최소 2회차 이상의 연속 확인을 거치는 절차가 유효했음을 보여준다.
- **BATON 티커 충돌 신규 발견**: GT 트렌딩 재확인 과정에서 같은 티커의 별개 풀이 추가로 발견됐다. 이 워치가 반복 경계해온 티커 충돌 위험(Dinger·CATSZN 등)이 다시 확인됐다.
- **데이터 신뢰도**: DexScreener 배치조회와 GeckoTerminal 트렌딩(솔라나·로빈후드체인 top20, 각 2페이지) 교차검증으로 다수 종목의 방향성 일치를 확인했다. HOOKR·GOOD·JUGGERNAUT·TOAD·PANTS·CATE는 DS-GT 양쪽 값이 근접해 신뢰도가 높다. AI/NVDA(BANKR)는 이번 회차 DS-GT 양쪽 모두 재확인했으나 구조적 괴리(약2.48배)가 지속됐다. PROLOGUE는 DS-GT 간 약 1.45배 규모 차이가 새로 확인돼 경계 대상에 추가한다. X 직접 조회는 로그인월로 대부분 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
