# 온체인 트렌딩 조기경보 — 2026-08-26 05:00 UTC (KST 2026-08-26 14:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 03:00Z)로부터 **정상 2시간** 경과. 유실 없이 정상 진행됐다.

44개 활성종목 전부를 DexScreener 배치조회(chainId별 tokens/v1 다중주소 API, 로빈후드 1배치 15·솔라나 2배치 14+14·이더리움 1배치 1)로 재확인했다. 추가로 GeckoTerminal 로빈후드체인 트렌딩(top20)·솔라나 트렌딩(top20) 및 우선추적과제(DTF·Pistacio·BARK·Swan·TRUTH·PEE·AI/NVDA(BANKR)) 개별 풀·토큰-풀목록 조회를 수행해 다수 notable 항목도 함께 교차확인했다. GeckoTerminal은 이번 회차 초반 429(레이트리밋)가 여러 차례 발생했으나 재시도로 전량 회수했다.

## 이번 회차 핵심 발견

**DTF(notable) — ⭐⭐⭐⭐⭐h24 계속 완화(465%→309%), ⚠️신규 별도 풀(Uniswap V2, h24 +222,267%) 및 총 20개 풀 발견**: 메인 추적 풀(0xbc58bfe1…, pons-v2)의 h24는 +465.324%→**+308.72%**로 추가 완화돼 직전 회차의 '24h 윈도우 아티팩트' 해석과 일관되게 계속 정상화되고 있다(유동성 -9.1%·h1 재음전 -10.314%·h6 감속 +23.479%). 이번 회차 GT 로빈후드체인 트렌딩에서 **완전히 별도의 풀 'DTF/WETH(Uniswap V2)'**(reserve $354,764, h24 **+222,267.532%**, 2026-08-25 생성)이 새로 노출됐다. DTF 토큰의 전체 풀 목록을 조회한 결과 **총 20개 풀**을 보유하고 있으며 대부분 2026-08-25 당일 생성됐다(uniswap-v4/v3/pons-v2/ramses-v3 혼재). 상위 3개 풀(메인 $199K·V4 $301,814·V3 $118,264)은 h24가 +308~372%대로 유사하게 수렴하는 반면, 나머지 다수는 $1K~$56K대 소규모 풀이다. 이 대량·동시다발 풀 생성 패턴은 카피/디코이 풀 생성 또는 광범위한 유동성 공급 양상 중 하나로 해석되며, 확정하지 않는다.

**Swan(notable) — ⭐대폭 유입 반전, h24 1.7만%대 재진입**: 유동성이 $73,885.90→**$93,442.63(+26.5%, 대폭유입반전)**했고, h1·h6·h24가 전지표 재양전·가속했다(h24 +10,708.734%→**+17,275.222%**). 직전 2회차 GT-DS 괴리(약 6.7배)는 이번 회차 자원배분상 DS 재조회를 생략해 갱신하지 않았다.

**Pistacio(notable) — 유입반전, h6 자연감쇠 계속**: h6가 +444.999%→**+54.545%**로 대폭 감속했는데, 이는 풀 나이가 6시간을 넘어가며 h6가 실제 6시간 전 가격을 참조하기 시작한 구조적 현상의 연장으로 해석한다(h24는 여전히 24시간 미만 참조 구간이라 +25,320.94%→+30,033.807%로 계속 가속).

**TRUTH — ⭐DS값 3회차 연속 완전동일 상태가 이번 회차 처음 갱신됨**: 유동성이 $73,902.88→**$74,814.91**로, h1이 0%→**+0.37%**로 변동해 3회차 연속 완전 정지됐던 DS값이 갱신을 재개했다. GT 재확인(reserve $74,528.89·h24 +52.84%·**24h 거래량 $10,050,577.38**)도 근접 일치해, '캐시/지연반환'으로 확정했던 의심을 **일부 해소**로 격하한다.

**PEE — 유동성 DS값 4회 연속 완전동일 지속, 단 GT 거래량은 극히 저조**: 유동성이 $7,221.25로 4회 연속 고정됐다. TRUTH와 달리 이번 회차 GT 재확인 시 24h 거래량이 **$1,811.11**로 극히 낮게 나와, TRUTH의 'DS 캐시 지연'과는 다른 '실거래 자체가 희박한 저활동 토큰' 가능성이 추가됐다.

**swappy·KIRK — ⚠️양전 연속 스트릭 종료로 🟢→🟡 하향**: swappy는 2회차 연속 강세이던 h6가 이번 회차 재음전(+49.82%→-0.68%)해 스트릭이 끊겼다. KIRK도 h6·h24가 동시에 재음전(+15.75%→-1.9%, +10.38%→-1.75%)해 양전 연속 흐름이 종료됐다. 둘 다 리스크를 🟢에서 🟡로 하향 재조정한다.

**PROLOGUE — ⭐6연속 양전 스트릭 종료 직후 1회차 만에 재양전**: 직전 회차 6연속 양전 스트릭이 종료됐던 h24가 이번 회차 다시 +2.54%로 양전 전환했다. 유동성도 +10.1% 대폭 유입되며 h1·h6까지 전지표 동시 대폭가속했다. 다만 직전 스트릭 종료 직후의 단발성 반등일 가능성이 있어 단정하지 않는다.

**JUGGERNAUT — ⭐h1 3회차 연속 재양전**: 182회차 만에 처음 재양전했던 h1이 이번 회차도 +7.50%로 양전을 유지해 3회차 연속을 기록했다(직전 2회차 연속 확인 이후 추가 확인).

**MAPLE·CYBERLEEK·HOOKR — h24 재양전(대폭반전) 3건 동시 확인**: MAPLE h24 -12.09%→**+11.64%**, CYBERLEEK h24 -8.82%→**+15.85%**, HOOKR h24 -6.72%→**+4.93%**로 모두 재양전 전환했다. 단일 회차 관측이라 단정하지 않는다.

**CASHCAT(notable) — ⚠️두 풀 유동성 규모 순위 역전 관측**: GT 트렌딩에서 '1%'풀이 약 $4.50M→$2,186,798, '0.3%'풀이 약 $2.16M→$4,545,216로 순위가 뒤바뀐 것으로 관측됐다. 라벨 재확인이 필요한지 실제 유동성 이동인지 미확정이라 정직하게 병기만 하고 단정하지 않는다.

**PONS·DELTA·Index(notable) — 로빈후드체인 상위권 지속 강세**: PONS 두 풀 모두 유입 지속·h24 가속(+39.7%/+40.8%), DELTA h24 재양전(-4.8%→+30.434%), Index h24 재양전(-9.7%→+4.896%)으로 로빈후드체인 상위권 토큰들의 강세가 이어졌다.

**C4T(솔라나, 신규) — GT 솔라나 트렌딩 6위 신규 노출**: reserve $33,636.39, h24 +74.999%, 풀 생성 2026-08-25(당일). DTF·Pistacio·BARK·Swan과 같은 날 생성된 신생 풀군에 속해 notable에 신규 편입해 관찰을 시작한다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 49회차. 유출반전,h1가속h6대폭감속h24는악화 | 유동성$103,014.10(-4.3%), h24-28.76%(악화) | 지속(48회차)·유출반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 57회차. 유출반전,h1재음전h6감속h24는악화 | 유동성$13,761.41(-2.2%), h24-52.06%(악화) | 지속(56회차)·h24재악화 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 43회차. 유입반전,h1h24동시재양전(대폭반전) | 유동성$29,166.43(+6.4%), h24+11.64%(재양전) | 지속(42회차)·h1h24동시재양전 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 67회차. 유입지속,h1유사h6가속h24는소폭개선 | 유동성$195,997.06(+4.5%), h24-24.69%(소폭개선) | 지속(66회차)·전지표양호 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 55회차. 유입반전,h1재양전h6대폭악화h24는가속 | 유동성$13,713.76(+2.8%), h24+19.29%(가속) | 지속(54회차)·h6극단악화경계 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 38회차. 유출반전,h1재음전h6h24는개선 | 유동성$29,698.22(-3.5%), h24-13.78%(개선) | 지속(37회차)·개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 47회차. 유입지속,h1감속h6가속h24는유사 | 유동성$20,427.29(+2.6%), h24-21.10%(유사) | 지속(46회차)·전지표양전유지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 79회차. 유출유사,h1개선h6유사h24는개선 | 유동성$25,073.76(-1.2%), h24-41.03%(개선) | 지속(78회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 45회차. 대폭유출반전,전지표동시재악화 | 유동성$15,437.60(-8.2%), h24-48.40%(악화) | 지속(44회차)·전지표재악화 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 84회차. ⚠️유동성DS값4회연속완전동일 | 유동성$7,221.25(0.0%), h24-12.65%(개선) | 지속(83회차)·데이터경계 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 42회차. 유출지속,h1악화h6개선h24는유사 | 유동성$8,918.33(-2.7%), h24-42.46%(유사) | 지속(41회차)·유사 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 31회차. 유출반전,h1재음전h6대폭감속h24는대폭개선 | 유동성$39,420.88(-4.9%), h24-11.77%(대폭개선) | 지속(30회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 28회차. 유입반전,h1h6동시재양전(대폭반전) | 유동성$13,199.51(+4.5%), h24-59.95%(대폭개선) | 지속(27회차)·h1h6동시재양전 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 31회차. 유동성유사,h1재양전h6악화h24는개선 | 유동성$89,587.13(-0.8%), h24-25.6%(개선) | 지속(30회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 60회차. ⚠️2연속강세스트릭종료(h6재음전) | 유동성$199,581.76(-1.4%), h24+43.50%(유사) | 지속(59회차)·스트릭종료 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 59회차. 유입반전,h1재음전(소폭)h6가속h24는재양전 | 유동성$1,607,294.84(+3.0%), h24+15.85%(재양전) | 지속(58회차)·h24재양전 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 57회차째방향번복. 유출반전,h1재음전h6재양전h24는유사 | 유동성$236,721.98(-2.7%), h24-33.01%(유사) | 지속(56회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 50회차. 유출지속,h1재양전h6유사h24는악화 | 유동성$68,303.39(-4.2%), h24-26.28%(악화) | 지속(49회차)·whipsaw지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 47회차. ⚠️h6h24양전연속스트릭종료 | 유동성$77,806.66(-1.8%), h24-1.75%(재음전) | 지속(46회차)·스트릭종료 | 🟡 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 44회차. 유출반전,h1h6는악화h24는대폭감속(양전유지) | 유동성$69,662.36(-2.2%), h24+30.03%(감속) | 지속(43회차)·가속흐름둔화 | 🟡 | [DexScreener](https://dexscreener.com/solana/DShht9B8wCRe5t3oqdPB77PnjJbKxbYaZyuWpZQjbonk) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 35회차. 유출반전,h1재음전(대폭반전)h6유사h24는감속 | 유동성$375,617.15(-5.3%), h24+9.45%(감속) | 지속(34회차)·재차완전반전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 28회차. 유출지속,h1개선h6악화h24는거의완전소멸고착지속 | 유동성$6,877.6(-4.4%), h24-96.16%(고착) | 지속(27회차)·h24고착 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 27회차. ⭐스트릭종료직후재양전(전지표대폭가속) | 유동성$266,078.43(+10.1%), h24+2.54%(재양전) | 지속(26회차)·재양전확인 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 33회차. ⭐DS값3회연속완전동일상태갱신재개 | 유동성$74,814.91(+1.2%), h24+51.05%(가속) | 지속(32회차)·DS값갱신재개 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 32회차. 유출반전,전지표동시대폭감속(양전유지) | 유동성$20,485.90(-3.6%), h24+8.93%(감속) | 지속(31회차)·가속흐름진정 | 🟡 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 62회차. 대폭유입지속,h24재양전(첫반전) | 유동성$497,357.88(+9.5%), h24+4.93%(재양전) | 지속(61회차)·h24재양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 184회차. ⭐h1 3회차연속재양전 | 유동성$428,124.38(+0.3%), h24-11.19%(개선) | 지속(183회차)·h1 3연속양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 160회차. 유출반전,h1재음전h6유사h24는감속(양전유지) | 유동성$228,280.17(-3.2%), h24+53.45%(감속) | 지속(159회차)·h1재음전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 63회차. 유출반전,h1재음전h6악화h24는유사 | 유동성$520,892.85(-1.6%), h24-11.19%(유사) | 지속(62회차)·소폭악화 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 198회차. 유동성유사,h6h24는대폭감속(양전유지) | 유동성$494,260.87(+0.4%), h24+35.14%(대폭감속) | 지속(197회차)·재가속흐름다시감속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 189회차. 유출지속,h1유사h6유사h24는악화 | 유동성$78,261.72(-3.1%), h24-21.42%(악화) | 지속(188회차)·연속whipsaw | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 189회차. 유입지속,h1재양전(대폭반전)h6개선h24는유사 | 유동성$35,689.80(+2.8%), h24-40.78%(유사) | 지속(188회차)·h1재양전 | 🔴 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 147회차. 유동성유사,h1가속h6가속h24는개선 | 유동성$67,003.56(-0.1%), h24-14.99%(개선) | 지속(146회차)·전지표양호 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 197회차. 유입반전,h1개선h6가속h24는대폭개선 | 유동성$355,346.66(+2.2%), h24-9.88%(대폭개선) | 지속(196회차)·혼조나소폭개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 201회차달성. 유출반전,h1재음전h6대폭개선h24는악화 | 유동성$1,153,362.68(-1.4%), h24-24.35%(악화) | 지속(200회차)·201회차달성 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 149회차. 소폭유입반전,h1재양전(대폭반전)h6는악화h24는유사(고착) | 유동성$38,349.18(+0.8%), h24-66.63%(고착) | 지속(148회차)·h1재양전 | 🔴 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 78회차. 유동성유사,h1재음전h6유사h24는개선 | 유동성$227,889.73(+0.8%), h24-19.34%(개선) | 지속(77회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 151회차. 유출반전,h1악화h6재양전(대폭반전)h24는감속(양전유지) | 유동성$54,894.39(-1.6%), h24+91.13%(감속) | 지속(150회차)·3차스파이크냉각지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 49회차(dogwifpants). 유동성유사,h1유사h6h24는개선 | 유동성$65,364.32(-0.7%), h24-41.88%(개선) | 지속(48회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 42회차. 대폭유출반전,전지표동시재악화 | 유동성$62,278.77(-8.2%), h24-13.42%(악화) | 지속(41회차)·전회차강세일부무산 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 36회차. 유동성유사,h24는대폭개선(손익분기근접) | 유동성$8,134.57(-0.6%), h24-0.36%(대폭개선) | 지속(35회차)·h24대폭개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 35회차. 유동성유사,h1재음전(소폭)h6h24는개선 | 유동성$213,568.86(-0.2%), h24-7.15%(개선) | 지속(34회차)·소폭개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 34회차. 대폭유입반전,전지표동시개선(여전히전량음전) | 유동성$21,373.58(+9.0%), h24-25.75%(개선) | 지속(33회차)·전지표동시개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |
| **CATE** | Solana(PumpSwap) | 미확인 | 121회차달성. 유동성유사,h1재음전h6개선h24는유사 | 유동성$2,244,858.80(-0.2%), h24-2.79%(유사) | 지속(120회차)·장기whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |

> **편입/편출/강등/재승격 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. **강등 2건**(swappy 🟢→🟡, KIRK 🟢→🟡, 둘 다 양전 연속 스트릭 종료). 활성목록 **44→44종**(순증감 0, 조기13/확산10/뒷북21). notable **69→70개**(신규 1건: C4T). **핵심 이벤트**: DTF h24 계속완화(465%→309%)+신규별도풀(h24+222,267%)및총20개풀발견, Swan대폭재상승(GT h24 1.7만%대재진입), Pistacio h6자연감쇠계속, TRUTH DS값3회만에갱신재개(캐시의심일부해소), PEE는DS값4회연속고정+GT거래량극히저조로별개패턴확인, swappy·KIRK양전스트릭종료로하향, PROLOGUE스트릭종료직후재양전, JUGGERNAUT h1 3연속양전, MAPLE·CYBERLEEK·HOOKR h24동시재양전, CASHCAT두풀순위역전관측, C4T신규편입.

## 온체인 신호 상세

- **DTF(notable) 상세**: 메인추적풀 GT reserve$218,970.28→$199,153.32(-9.1%,유출반전), h1+17.184%→-10.314%(재음전,대폭반전), h6+46.955%→+23.479%(감속,대폭), h24+465.324%→+308.72%(추가완화). 신규발견 별도풀 'DTF/WETH(Uniswap V2)': reserve$354,764, h24+222,267.532%(2026-08-25생성). 토큰전체풀목록: 총20개풀(대부분2026-08-25당일생성), 상위3개(메인$199K·V4$301,814·V3$118,264)는h24가+308~372%대로유사수렴, 나머지17개는$1K~$56K대소규모. 회차추이(메인풀): 7,206%→10,775%[최고]→10,358%→7,394%→8,891%→8,278%→9,313%→465%→**309%[현재]**. 풀나이약27.4시간(2026-08-25T01:35:27Z생성, 부모제공) · 2026-08-26T05:00:00Z
- **Swan(notable) 상세**: GT reserve$73,885.90→$93,442.63(+26.5%,대폭유입반전), h1+8.743%→+19.228%(가속,양전유지), h6-9.126%→+27.139%(재양전,대폭반전), h24+10,708.734%→+17,275.222%(대폭가속,재상승). DS재조회는이번회차자원배분상생략(GT-DS괴리약6.7배패턴은직전2회차충분히확인). 풀나이약10.8시간(2026-08-25T18:12:54Z생성, 부모제공) · 2026-08-26T05:00:00Z
- **Pistacio(notable) 상세**: GT reserve$360,176.53→$392,997.47(+9.1%,유입반전), h1-18.407%→+4.087%(재양전,대폭반전), h6+444.999%→+54.545%(대폭감속,양전유지—6h윈도우자연이동으로해석), h24+25,320.94%→+30,033.807%(가속,계속상승). 풀나이약9.6시간(2026-08-25T19:22:21Z생성, 부모제공) · 2026-08-26T05:00:00Z
- **TRUTH DS값갱신재개 상세**: DS 유동성$73,902.88→$74,814.91(+1.2%,3회연속고정이후첫변동), h1 0%→+0.37%(재양전), h6-(신규기재)+1.58%, h24+48.71%→+51.05%(가속). GT재조회: reserve$74,528.89·h6+0.34%·h24+52.84%·24h거래량$10,050,577.38(매우활발) — DS·GT모두근접일치 · 2026-08-26T05:00:00Z
- **PEE 데이터경계 상세**: DS 유동성$7,221.25→$7,221.25(0.0%,4회연속완전동일). GT재조회: reserve$7,258.44·h6-0.89%·h24-11.96%·24h거래량$1,811.11(TRUTH대비현저히저조,실거래희박가능성) · 2026-08-26T05:00:00Z
- **swappy·KIRK 스트릭종료 상세**: swappy 유동성$202,403.60→$199,581.76(-1.4%), h6+49.82%→-0.68%(재음전,2연속강세종료). KIRK 유동성$79,233.65→$77,806.66(-1.8%), h6+15.75%→-1.9%(재음전), h24+10.38%→-1.75%(재음전,양전연속스트릭종료) · 2026-08-26T05:00:00Z
- **PROLOGUE 재양전 상세**: 유동성$241,665.59→$266,078.43(+10.1%,대폭유입반전), h1+2.93%→+29.55%(대폭가속), h6-5.23%→+48.06%(재양전,대폭반전), h24-6.00%→+2.54%(재양전,대폭반전,6연속스트릭종료직후1회차만에복귀) · 2026-08-26T05:00:00Z
- **JUGGERNAUT h1 3연속양전 상세**: 유동성$427,035.78→$428,124.38(+0.3%,유사), h1+5.95%→+7.50%(가속,양전유지,3연속), h6-8.26%→+7.56%(재양전,대폭반전), h24-17.91%→-11.19%(개선) · 2026-08-26T05:00:00Z
- **CASHCAT(notable) 상세**: GT트렌딩재확인: '1%'풀 reserve약$4.50M→$2,186,798(h24-7.8%→-7.065%), '0.3%'풀 reserve약$2.16M→$4,545,216(h24-7.2%→-8.622%). 두풀규모순위가전회차대비역전관측(라벨재확인필요,정직표기) · 2026-08-26T05:00:00Z
- **나머지 상세**: OBS유출반전. PEPECOIN악화. MAPLE h1h24동시재양전. CLOCKIN전지표양호. TIPANSEM h6극단악화경계. LIZARD개선. 1B전지표양전유지. CLUG개선. FLUSH전지표재악화. 40M유사. MANEKI혼조. CYBERCAT h1h6동시재양전. omo개선. CYBERLEEK h24재양전. CC워시트레이딩의심불변. Z500whipsaw지속. CONK가속흐름둔화. CHUMP재차완전반전. CATALORIAN고착. Dinger가속흐름진정. HOOKR h24재양전. CATE장기whipsaw. BRODIE h1재음전. GOOD소폭악화. PRINTER재가속흐름다시감속. Dealer연속whipsaw. lickingcat h1재양전. CALLOOOR전지표양호. TOAD혼조나소폭개선. FWA201회차. DPG h1재양전. BULLSHIT혼조. PITCOIN3차스파이크냉각지속. PANTS개선. Doge2전회차강세일부무산. Truth Coin h24대폭개선. BARRON소폭개선. YOMOGI전지표동시개선 · 2026-08-26T05:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 41종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 DexScreener 배치조회 재확인, GT 트렌딩(로빈후드체인 top20·솔라나 top20) 교차검증, 우선추적과제(DTF·Pistacio·BARK·Swan·TRUTH·PEE·AI/NVDA(BANKR)) 개별 풀·토큰-풀목록 재확인에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 03:00Z)로부터 **정상 2시간** 경과, 유실 없음.
- **저장 후 세 파일(json·csv·md) 종목 목록 대조**: tokens(json) 44종·csv 44행(헤더 제외)·md 3개 표(조기13+확산10+뒷북21=44) 전부 일치 확인함(OBS~PROLOGUE까지 개별 이름 대조 완료). notable(json) 70건.
- **GeckoTerminal 429(레이트리밋) 대응**: 이번 회차 초반 TRUTH·PEE·로빈후드체인 트렌딩·솔라나 트렌딩 조회에서 429가 발생했으나, 간격을 두고 재시도해 전량 회수했다(수치 손실 없음).
- **DTF의 신규 별도 풀 발견은 러그가 아니라 같은 토큰의 다른 풀에서 초기 극단 스파이크 패턴이 재현되고 있는 것으로 해석한다**: 메인 추적 풀은 h24가 계속 완화(465%→309%)되며 24시간 비교기준가격이 초기 극단 구간을 벗어나는 과정을 이어가고 있고, 신규 풀은 그 자체로 매우 최근(2026-08-25) 생성돼 같은 초기 단계를 거치고 있는 것으로 보인다. 총 20개 풀 존재는 정직하게 기록하되 원인(카피/디코이 vs 유기적 유동성 공급)은 단정하지 않는다.
- **TRUTH의 DS값이 3회차 연속 완전동일 이후 이번 회차 처음 갱신된 것을 '캐시의심 부분해소'로 판정한다**: GT의 24h 거래량($10M+)이 여전히 매우 활발해 실거래가 왕성함을 재확인했다. 반면 PEE는 GT 거래량 자체가 $1,811.11로 낮아, TRUTH와는 다른 원인(저활동)일 가능성을 함께 기록한다.
- **swappy·KIRK의 양전 연속 스트릭이 이번 회차 각각 종료됐다**: 둘 다 리스크를 🟢에서 🟡로 하향 재조정했다.
- **데이터 신뢰도**: DexScreener 배치조회(로빈후드15·솔라나14+14·이더리움1)와 GeckoTerminal 트렌딩(로빈후드체인 top20·솔라나 top20)·개별 풀 및 토큰-풀목록 조회로 교차검증했다. TRUTH·PEE는 DS-GT 근접 일치를 재확인했다. AI/NVDA(BANKR)·Swan은 이번 회차 DS 재조회를 자원배분상 생략해(직전 회차까지 충분히 확인된 패턴) 다음 회차 재개를 검토한다. X 직접 조회는 로그인월로 대부분 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
