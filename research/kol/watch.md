# 온체인 트렌딩 조기경보 — 2026-08-26 07:00 UTC (KST 2026-08-26 16:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 05:00Z)로부터 **정상 2시간** 경과. 유실 없이 정상 진행됐다.

44개 활성종목 전부를 DexScreener 배치조회(chainId별 tokens/v1 다중주소 API, 로빈후드 1배치 15·솔라나 2배치 14+14·이더리움 1배치 1)로 재확인했다. 추가로 GeckoTerminal 로빈후드체인 트렌딩(top20)·솔라나 트렌딩(top20+2페이지) 및 우선추적과제(DTF·Pistacio·BARK·Swan·C4T·AI/NVDA(BANKR)) 개별 풀·토큰-풀목록 조회를 수행해 다수 notable 항목도 함께 교차확인했다.

## 이번 회차 핵심 발견

**⚠️⚠️DTF — 완전히 별개의 '제2의 DTF' 토큰 신규 발견(최우선 경보)**: GT 로빈후드체인 트렌딩(top20) 5위에서 우리가 추적 중인 DTF(baseToken CA `0xee5576fa1bcaa380e591d01245f406f3f384eb01`)와는 **완전히 다른 컨트랙트 주소**(`0x2ec89afba136119c5252fc47d14e2bd2144b10d2`)를 가진 별개의 'DTF/WETH' 풀(id `0xbbc5d7f008582ab30e64633743bb2757baad550e`, 2026-08-25T07:25:20Z 생성, 약 23.6시간전)이 노출됐다. 이 풀의 reserve는 **$885,582.89**로 우리 메인 추적풀($217,280)의 약 **4배**나 되고, h24는 **+1,403,983.595%**라는 극단치를 기록했다. 같은 'DTF' 티커를 쓰는 완전히 별개 토큰이며, 원조 프로젝트의 추가 배포·포크·사칭 카피캣 중 무엇인지는 단정하지 않는다. notable에 별도 항목(`DTF(둘째)`)으로 신규 편입했다.

**DTF(메인 추적풀, notable) — 풀 개수 풀개수 129개[부모가 페이지네이션으로 전수 집계, 2026-08-26 07:20Z] — ⚠️직전까지 기재된 "20개"·"129개(부모 정정, 페이지 상한 오인)"는 GeckoTerminal /pools 엔드포인트의 **페이지당 20건 상한**을 전체 개수로 오인한 값이었다(부모 정정)로 재확대, h24는 계속 3자리%대 안정화**: 메인 추적 풀(pons-v2, 0xbc58bfe1…)의 h24는 +308.72%→**+329.62%**로 소폭 재가속했으나 여전히 3자리%대에서 안정화된 상태다(유동성 +9.1%·h1 재양전 +12.763%·h6 가속 +40.687%). 토큰 전체 풀 목록을 재조회한 결과 **129개(부모 정정, 페이지 상한 오인) 풀**(직전 20개에서 3개 증가)을 보유하고 있으며, 신규 풀 중에는 'AI / DTF' 교차풀과 2026-08-26T03:07:45Z(약 3.9시간전)에 생성된 풀도 포함돼 풀 생성이 계속 진행 중임을 확인했다.

**Swan(notable) — ⭐GT-DS 괴리 6.63배로 정량 재확인**: 이번 회차 DS 재조회를 수행해 liquidity.usd $88,913.94(GT reserve $88,748와 근접, -0.2%)를 확인했으나, h24는 DS **+102,114%** vs GT **+15,404%**로 **정확히 6.63배** 괴리됐다 — 직전 2회차의 약 6.7배 패턴과 일관되게 재확인됐다. 방향은 동일(둘 다 초극단 양전)하나 배율 차이가 구조적으로 지속되고 있다.

**AI/NVDA(BANKR, notable) — ⚠️DS-GT 괴리가 방향까지 어긋남**: DS 재조회 결과(baseToken symbol 'AI', name 'Artificial Inu' — 5회차 연속 동일 매칭) liquidity $1,908,089.50로 GT reserve($4,865,568.18 기준 직전값)와 약 2.55배 괴리(직전 2.50배에서 소폭 확대)했고, **h24가 DS -5.68% vs GT +18.356%로 부호까지 반대**로 나타났다. 토큰화 주식/합성자산은 이 워치의 대상 범위 밖이라 tokens 편입은 하지 않는다.

**C4T(솔라나, notable) — 2회차 재확인, 풀 생성 정확 시각 확보(약 8.1시간전)**: 직접 풀 조회로 pool_created_at **2026-08-25T22:55:12Z**를 확보해 07:00Z 기준 약 **8.1시간전**임을 확정했다(직전 회차 "당일생성"에서 진전). 24h 거래량 $3,272,494.56은 reserve($35,742.17) 대비 약 91.6배 회전율로 매우 높아 워시트레이딩 가능성을 함께 경계한다. ⚠️CA는 두 소스에서 `2sLKA7Pz…`(트렌딩 목록)와 `2sLKA6Pz…`(풀 직접조회)로 1자 상이하게 반환돼 **재확인이 필요한 상태**로 정직 표기한다.

**Pistacio(notable) — ⚠️h1·h6 동시 첫 음전 전환**: 풀 생성(2026-08-25T19:22:21Z, 약 11.6시간전) 이후 처음으로 h1(-5.714%)과 h6(-11.651%)가 동시에 음전 전환했다(유동성도 -9.8% 유출반전). h24는 +30,033.807%→+24,146.796%로 계속 완화 중이다. 단일 회차 관측이라 단정하지 않는다.

**BARK(notable) — 전지표 동시 개선**: 유입 지속(+3.2%)과 함께 h1(재양전 +4.385%)·h6(재양전 +29.469%)·h24(-6.283%→-1.077%, 손익분기 근접)가 모두 개선됐다.

**PANTS·CATE·HOOKR·PROLOGUE — 큰 폭 반전 4건**: PANTS는 전지표 동시 재양전(대폭유입반전 +13.2%, h1 재양전 +16.13%, h6 재양전 +18.38%, h24 대폭개선 -29.35%). CATE는 h6·h24 동시 재양전(대폭반전). 반면 HOOKR는 직전 회차 h24 재양전(첫 반전)이 이번 회차 1회차 만에 무산(h1·h24 동시 재음전). PROLOGUE도 직전 회차 재양전이 이번 회차 완전히 무산(전지표 동시 재악화) — 단발성 반등이었을 가능성이 다시 확인됐다.

**CASHCAT(notable) — 두 풀 유동성 규모 순위 3회차 연속 오가는 것 확인**: '1%'풀이 $2,186,798→**$4,642,556**, '0.3%'풀이 $4,545,216→**$2,298,557**로 순위가 다시 원래대로(1%>0.3%) 되돌아왔다. 3회차 연속으로 두 풀 규모 순위가 오가는 것이 확인돼, 단순 라벨 오류보다는 두 풀 간 실제 유동성 이동/오실레이션일 가능성이 높아졌다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 50회차. 유입반전,전지표동시개선 | 유동성$112,267.41(+9.0%), h24-9.18%(대폭개선) | 지속(49회차)·전지표개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 58회차. 유사,h1재양전h6가속h24는대폭개선 | 유동성$13,602.96(-1.2%), h24-35.60%(대폭개선) | 지속(57회차)·h24낙폭완화 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 44회차. 유출반전,h1재음전h6개선h24는감속(양전유지) | 유동성$28,856.90(-1.1%), h24+7.20%(감속,양전) | 지속(43회차)·전지표양전유지 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 68회차. 유출반전,h1감속h6감속h24는악화 | 유동성$186,447.48(-4.9%), h24-29.56%(악화) | 지속(67회차)·전지표양전유지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 56회차. 유사,h1재음전h6대폭개선(회복)h24는가속 | 유동성$13,781.59(+0.5%), h24+24.93%(가속) | 지속(55회차)·h6정상범위복귀 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 39회차. 유입반전,h1h6동시재양전(대폭반전)h24는개선 | 유동성$31,286.59(+5.3%), h24-10.33%(개선) | 지속(38회차)·h1h6동시재양전 | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 48회차. 유입가속,h1유사h6대폭가속h24는개선 | 유동성$21,927.57(+7.3%), h24-12.58%(개선) | 지속(47회차)·전지표양전유지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 80회차. 유사,h1재양전h6개선h24는악화 | 유동성$25,282.71(+0.8%), h24-43.28%(악화) | 지속(79회차)·h24악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 46회차. 유출반전종료(유사),전지표동시개선 | 유동성$15,501.72(+0.4%), h24-40.78%(개선) | 지속(45회차)·소폭개선 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 85회차. ⚠️유동성DS값5회연속완전동일,h1h6도0%로수렴 | 유동성$7,221.25(0.0%), h24-10.70%(개선) | 지속(84회차)·데이터정체심화 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 43회차. 유출가속,전지표동시악화 | 유동성$8,204.66(-8.0%), h24-50.89%(악화) | 지속(42회차)·전지표악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 32회차. 유출지속,h1재양전h6재음전h24는개선 | 유동성$38,203.00(-3.1%), h24-7.88%(개선) | 지속(31회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 29회차. 유사,h1재음전h6유사h24는악화 | 유동성$13,342.79(+1.1%), h24-66.77%(재악화) | 지속(28회차)·h24재악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 32회차. 유입반전,h1재음전h6재양전h24는개선 | 유동성$94,640.90(+5.6%), h24-21.34%(개선) | 지속(31회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 61회차. 유입반전,h1재음전h6유사h24는감속 | 유동성$201,251.47(+0.8%), h24+38.74%(감속) | 지속(60회차)·단정금지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 60회차. 유사,h1대폭악화h6감속h24는유사 | 유동성$1,611,252.30(+0.2%), h24+16.76%(유사) | 지속(59회차)·단정금지 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 58회차째방향번복. 유입반전,h1재양전h6가속h24는개선 | 유동성$247,657.32(+4.6%), h24-18.02%(개선) | 지속(57회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 51회차. 유입반전,전지표동시개선 | 유동성$72,354.06(+5.9%), h24-14.56%(개선) | 지속(50회차)·whipsaw지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 48회차. 유출지속,h1재양전h6h24는악화 | 유동성$76,222.09(-2.0%), h24-7.97%(악화) | 지속(47회차)·스트릭종료이후혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 45회차. 유출지속,전지표동시개선(h24는유사) | 유동성$66,128.17(-5.1%), h24+28.99%(유사) | 지속(44회차)·가속흐름둔화지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/DShht9B8wCRe5t3oqdPB77PnjJbKxbYaZyuWpZQjbonk) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 36회차. 유출유사,h1개선h6개선h24는대폭감속(양전전환) | 유동성$362,582.32(-3.5%), h24+3.34%(양전전환) | 지속(35회차)·재차완전반전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 29회차. 유출지속,h1개선h6유사h24는개선(고착) | 유동성$6,540.78(-4.9%), h24-94.48%(고착) | 지속(28회차)·h24고착 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 28회차. ⚠️직전1회차재양전이다시무산,전지표동시재악화 | 유동성$249,143.41(-6.4%), h24-16.02%(재음전) | 지속(27회차)·재양전완전무산 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 34회차. 유사,h1재음전h6감속h24는유사(양전유지) | 유동성$74,438.74(-0.5%), h24+49.92%(유사) | 지속(33회차)·DS값갱신흐름유지 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 33회차. 유입반전,h1h6는가속h24는감속(양전유지) | 유동성$21,034.47(+2.7%), h24+0.77%(손익분기근접) | 지속(32회차)·손익분기근접 | 🟡 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 63회차. ⚠️직전h24재양전이1회차만에무산 | 유동성$487,903.93(-1.9%), h24-3.55%(재음전) | 지속(62회차)·h24재음전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 185회차. ⭐h1 4회차연속재양전 | 유동성$459,091.36(+7.2%), h24-13.04%(악화) | 지속(184회차)·h1 4연속양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 161회차. 유사,h1개선h6유사h24는감속(양전유지) | 유동성$225,418.86(-1.3%), h24+41.24%(감속) | 지속(160회차)·전지표대체로양호 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 64회차. 유사,h1개선h6재양전h24는유사 | 유동성$516,118.02(-0.9%), h24-10.02%(유사) | 지속(63회차)·h6재양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 199회차. 유입반전,h1유사h6h24는대폭재가속 | 유동성$516,205.86(+4.4%), h24+78.56%(재가속) | 지속(198회차)·재가속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 190회차. 유입반전,전지표동시개선 | 유동성$83,746.20(+7.0%), h24-12.17%(개선) | 지속(189회차)·연속whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 190회차. 유사,h1재음전h6재양전h24는유사(전량음전) | 유동성$36,153.41(+1.3%), h24-40.85%(유사) | 지속(189회차)·h1h6방향전환 | 🔴 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 148회차. 유사,h1감속h6감속h24는유사 | 유동성$66,356.87(-1.0%), h24-15.74%(유사) | 지속(147회차)·개선흐름소폭둔화 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 198회차. 유사,h1유사h6대폭감속h24는대폭개선 | 유동성$352,323.91(-0.9%), h24-4.16%(손익분기근접) | 지속(197회차)·혼조나소폭개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 202회차달성. 유입반전,h1재양전h6감속h24는개선 | 유동성$1,173,272.25(+1.7%), h24-19.14%(개선) | 지속(201회차)·202회차달성 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 150회차. 유사,h1재음전h6개선h24는유사(고착) | 유동성$38,102.36(-0.6%), h24-64.83%(고착) | 지속(149회차)·h1재음전 | 🔴 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 79회차. 유입반전,h1유사h6가속h24는개선 | 유동성$232,659.69(+2.1%), h24-12.4%(개선) | 지속(78회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 152회차. 유입반전,h1재양전h6대폭감속h24는재가속 | 유동성$56,080.78(+2.2%), h24+113%(재가속) | 지속(151회차)·4차스파이크재점화 | 🔴 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 50회차(dogwifpants). 대폭유입반전,전지표동시재양전 | 유동성$73,969.65(+13.2%), h24-29.35%(대폭개선) | 지속(49회차)·전지표동시재양전 | 🟡 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 43회차. 유출지속,h1개선h6재음전h24는대폭악화 | 유동성$57,363.37(-7.9%), h24-38.24%(악화) | 지속(42회차)·h24대폭재악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 37회차. 유사,h24는유사(손익분기근접유지) | 유동성$8,026.46(-1.3%), h24-0.21%(유사) | 지속(36회차)·손익분기근접유지 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 36회차. 유사,h1재음전(소폭)h6h24는유사 | 유동성$212,104.11(-0.7%), h24-8.04%(유사) | 지속(35회차)·소폭악화 | 🟡 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 35회차. 유출반전,전지표동시악화(전량음전) | 유동성$20,596.42(-3.6%), h24-30.89%(악화) | 지속(34회차)·개선흐름무산 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |
| **CATE** | Solana(PumpSwap) | 미확인 | 122회차달성. 유입반전,h1개선h6재양전h24는재양전(대폭반전) | 유동성$2,330,380.95(+3.8%), h24+14.16%(재양전) | 지속(121회차)·장기whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |

> **편입/편출/강등/재승격 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. **강등 2건**(HOOKR 🟡→🔴, PROLOGUE 🟡→🔴, 둘 다 직전 회차의 재양전이 1회차 만에 무산). 활성목록 **44→44종**(순증감 0, 조기13/확산10/뒷북21). notable **70→71개**(신규 1건: DTF둘째, 완전히별개토큰). **핵심 이벤트**: ⚠️⚠️DTF 완전히 별개의 제2토큰 신규발견(h24+1,403,983%)+메인풀 풀개수풀개수 129개[부모가 페이지네이션으로 전수 집계, 2026-08-26 07:20Z] — ⚠️직전까지 기재된 "20개"·"129개(부모 정정, 페이지 상한 오인)"는 GeckoTerminal /pools 엔드포인트의 **페이지당 20건 상한**을 전체 개수로 오인한 값이었다(부모 정정)재확대, Swan GT-DS괴리6.63배정량재확인, AI/NVDA(BANKR) DS-GT괴리방향까지불일치, C4T풀생성정확시각확보(8.1시간전)+CA1자상이경계, Pistacio h1h6동시첫음전, BARK전지표개선, PANTS·CATE대폭반전(재양전), HOOKR·PROLOGUE직전반전1회차만에무산, CASHCAT두풀순위3회차연속오실레이션.

## 온체인 신호 상세

- **DTF(둘째,신규,notable) 상세**: pool 0xbbc5d7f008582ab30e64633743bb2757baad550e('DTF/WETH'), baseToken CA 0x2ec89afba136119c5252fc47d14e2bd2144b10d2(메인추적DTF 0xee5576fa…와완전히별개). GT: reserve$885,582.89, h1+477.047%, h6+332.634%, h24+1,403,983.595%. 풀생성2026-08-25T07:25:20Z(07:00Z기준약23.6시간전) · 2026-08-26T07:00:00Z
- **DTF(메인,notable) 상세**: GT reserve$199,153.32→$217,280.43(+9.1%,유입반전), h1-10.314%→+12.763%(재양전,대폭반전), h6+23.479%→+40.687%(가속), h24+308.72%→+329.62%(소폭재가속). 토큰전체풀목록: 총129개(부모 정정, 페이지 상한 오인)풀(직전20개+3개, 신규엔'AI/DTF0.67%'교차풀및2026-08-26T03:07:45Z생성풀포함). 풀나이약29.4시간(2026-08-25T01:35:27Z생성, 부모제공) · 2026-08-26T07:00:00Z
- **Swan(notable) 상세**: GT reserve$93,442.63→$88,748(-5.0%,유출반전), h1+19.228%→-3.54%(재음전,대폭반전), h6+27.139%→+27.23%(유사), h24+17,275.222%→+15,404%(감속,여전히초극단). DS재조회: liquidity$88,913.94(GT reserve와근접), h1-2.9%, h6+25.28%, h24+102,114%(GT대비약6.63배괴리,직전6.7배패턴재확인). 풀나이약12.8시간(2026-08-25T18:12:54Z생성, 부모제공) · 2026-08-26T07:00:00Z
- **AI/NVDA(BANKR,notable) 상세**: DS재조회(symbol=AI,name=Artificial Inu,5회차연속동일매칭): liquidity$1,908,089.50, h1-1.57%, h6+14.11%, h24-5.68%. GT풀직전값: reserve$4,865,568.18, h24+18.356%. 괴리배율약2.55배(직전2.50배에서확대)이며h24부호까지불일치 · 2026-08-26T07:00:00Z
- **C4T(솔라나,notable) 상세**: 풀 4Wwu97nL4vJ1dHt9xFv4sPeNgxrbevgzUtX9kGhFtxCD 직접조회: pool_created_at 2026-08-25T22:55:12Z(07:00Z기준약8.1시간전확정), reserve$35,742.17, h1+67.385%, h6-61.945%, h24+69.212%, 24h거래량$3,272,494.56(reserve대비약91.6배회전율). CA는 트렌딩목록'2sLKA7Pz…'와 풀직접조회'2sLKA6Pz…'로1자상이 — 재확인필요로표기 · 2026-08-26T07:00:00Z
- **Pistacio(notable) 상세**: GT reserve$392,997.47→$354,476.07(-9.8%,유출반전), h1+4.087%→-5.714%(재음전,대폭반전), h6+54.545%→-11.651%(재음전,대폭반전—풀생성이후첫h1h6동시음전), h24+30,033.807%→+24,146.796%(대폭감속). 풀나이약11.6시간(2026-08-25T19:22:21Z생성, 부모제공) · 2026-08-26T07:00:00Z
- **BARK(notable) 상세**: GT reserve$15,551.27→$16,052.38(+3.2%,유입지속), h1-1.525%→+4.385%(재양전), h6-38.758%→+29.469%(재양전,대폭반전), h24-6.283%→-1.077%(대폭개선,손익분기근접). 풀나이약17.4시간(2026-08-25T13:33:34Z생성, 부모제공) · 2026-08-26T07:00:00Z
- **CASHCAT(notable) 상세**: GT트렌딩재확인: '1%'풀 reserve$2,186,798→$4,642,556(h24-7.065%→-5.98%), '0.3%'풀 reserve$4,545,216→$2,298,557(h24-8.622%→-7.75%). 3회차연속으로두풀규모순위가오간것확인(단순라벨오류보다실제유동성이동/오실레이션가능성) · 2026-08-26T07:00:00Z
- **HOOKR·PROLOGUE 반전무산 상세**: HOOKR 유동성$497,357.88→$487,903.93(-1.9%), h1+1.32%→-17.26%(재음전), h24+4.93%→-3.55%(재음전,대폭반전). PROLOGUE 유동성$266,078.43→$249,143.41(-6.4%), h1+29.55%→-6.15%(재음전), h24+2.54%→-16.02%(재음전,대폭반전) · 2026-08-26T07:00:00Z
- **PANTS·CATE 대폭재양전 상세**: PANTS 유동성$65,364.32→$73,969.65(+13.2%), h1-4.22%→+16.13%, h6-5.04%→+18.38%, h24-41.88%→-29.35%. CATE 유동성$2,244,858.80→$2,330,380.95(+3.8%), h6-1.16%→+11.64%, h24-2.79%→+14.16% · 2026-08-26T07:00:00Z
- **나머지 상세**: OBS전지표개선. PEPECOIN낙폭완화. MAPLE h1h6재양전. CLOCKIN전지표양전유지. TIPANSEM h6정상범위복귀. LIZARD h1h6동시재양전. 1B전지표양전유지. CLUG h24악화. FLUSH소폭개선. PEE데이터정체심화(h1h6도0%수렴). 40M전지표악화. MANEKI혼조. CYBERCAT h24재악화. omo개선. swappy단정금지. CYBERLEEK단정금지. CC개선. Z500개선. KIRK혼조. CONK가속흐름둔화지속. CHUMP양전전환. CATALORIAN고착. TRUTH DS값갱신흐름유지. Dinger손익분기근접. JUGGERNAUT h1 4연속양전. BRODIE전지표대체로양호. GOOD h6재양전. PRINTER재가속. Dealer연속whipsaw. lickingcat h1h6방향전환. CALLOOOR개선둔화. TOAD손익분기근접. FWA202회차. DPG h1재음전. BULLSHIT혼조. PITCOIN재가속. Doge2재악화. Truth Coin손익분기근접유지. BARRON소폭악화. YOMOGI개선무산 · 2026-08-26T07:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 41종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 DexScreener 배치조회 재확인, GT 트렌딩(로빈후드체인 top20·솔라나 top20+2페이지) 교차검증, 우선추적과제(DTF·Pistacio·BARK·Swan·C4T·AI/NVDA(BANKR)) 개별 풀·토큰-풀목록 재확인에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 05:00Z)로부터 **정상 2시간** 경과, 유실 없음.
- **저장 후 세 파일(json·csv·md) 종목 목록 대조**: tokens(json) 44종·csv 44행(헤더 제외)·md 3개 표(조기13+확산10+뒷북21=44) 전부 일치 확인함(OBS~PROLOGUE까지 개별 이름 대조 완료). notable(json) 71건(신규 DTF둘째 1건 반영).
- **⚠️⚠️최우선 경보: DTF 티커를 쓰는 완전히 별개의 제2 토큰이 발견됐다.** 우리가 계속 추적해온 DTF(CA `0xee5576fa1bcaa380e591d01245f406f3f384eb01`)와는 컨트랙트 주소가 전혀 다른 새 토큰(CA `0x2ec89afba136119c5252fc47d14e2bd2144b10d2`)이 GT 로빈후드체인 트렌딩에 노출됐으며, reserve가 메인 추적풀보다 크고(약 4배) h24가 +1,403,983%라는 극단치를 보인다. 두 토큰을 혼동하지 않도록 CA를 반드시 대조해야 하며, 어느 쪽이 '원조'인지는 이번 회차 자료만으로 판단할 수 없다.
- **C4T의 CA가 두 소스에서 1자 상이하게 반환됐다** — WebFetch를 통한 소형모델 요약 과정에서 base58 문자열이 오독됐을 가능성이 있어, 향후 tokens 편입 검토 시에는 원문 raw JSON을 직접 재대조해야 한다.
- **Swan·AI/NVDA(BANKR)의 GT-DS 괴리가 이번 회차에도 정량적으로 재확인됐다**: Swan은 약 6.63배(방향은 일치), AI/NVDA(BANKR)는 약 2.55배(이번엔 방향까지 불일치)로 성격이 다르다 — Swan은 배율만 다른 반면 AI/NVDA(BANKR)는 두 소스가 서로 반대 신호를 주고 있어 더 큰 주의가 필요하다.
- **데이터 신뢰도**: DexScreener 배치조회(로빈후드15·솔라나14+14·이더리움1)와 GeckoTerminal 트렌딩(로빈후드체인 top20·솔라나 top20+2페이지)·개별 풀 및 토큰-풀목록 직접조회로 교차검증했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
