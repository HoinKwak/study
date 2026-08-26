# 온체인 트렌딩 조기경보 — 2026-08-26 09:00 UTC (KST 2026-08-26 18:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 07:00Z)로부터 **정상 2시간** 경과. 유실 없이 정상 진행됐다.

44개 활성종목 전부를 DexScreener 배치조회(chainId별 tokens/v1 다중주소 API, 로빈후드 1배치 15·솔라나 2배치 14+14·이더리움 1배치 1)로 재확인했다. 추가로 GeckoTerminal 로빈후드체인 트렌딩(top20)·솔라나 트렌딩(top20) 및 우선추적과제(DTF·DTF둘째·Pistacio·BARK·Swan·C4T·AI/NVDA(BANKR)·CASHCAT) 개별 풀·직접조회를 수행해 다수 notable 항목도 함께 교차확인했다.

## 이번 회차 핵심 발견

**⚠️⚠️'제2의 DTF' 토큰(전 회차 신규발견) — 1회차 만에 극단 붕괴**: 직전 회차(07:00Z)에 발견된 완전히 별개 컨트랙트의 'DTF/WETH' 풀(baseToken CA `0x2ec89afba136119c5252fc47d14e2bd2144b10d2`, pool `0xbbc5d7f008582ab30e64633743bb2757baad550e`)이 이번 회차 GT 재확인 결과 **reserve $885,582.89→$138,987.34(-84.3%, 급격유출)**, h1 **+477.047%→-56.103%**, h6 **+332.634%→-87.101%**, h24 **+1,403,983.595%→-3.512%**로 극단치가 완전히 소멸했다. 24h 거래량은 오히려 $47,684,558.71로 급증해 reserve 대비 약 343배 회전율을 기록 — 전형적인 '초기 극단치 급등 후 1회차 만에 급붕괴' 패턴으로 러그·워시트레이딩·청산 캐스케이드 가능성을 강하게 시사한다. 우리가 계속 추적 중인 메인 DTF(CA `0xee5576fa1bcaa380e591d01245f406f3f384eb01`)는 이번에도 GT 로빈후드체인 트렌딩 5위에 재노출됐고 h24 +230.474%로 3자리%대 안정화가 계속 유지되고 있어, 두 토큰의 궤적이 극명하게 갈리고 있다.

**Swan(notable) — GT-DS 괴리 6.30배로 소폭 완화, 방향은 여전히 일치**: DS 재조회(liquidity $91,900.96, h24 +108,384%) vs GT 직접조회(reserve $94,033.705, h24 +17,197.624%)로 배율이 직전 6.63배에서 **6.30배로 소폭 완화**됐다. 여전히 구조적 괴리이나 3회차 연속 6배대에서 수렴하는 흐름이다.

**AI/NVDA(BANKR, notable) — ⭐DS-GT 방향 불일치가 해소됨**: 직전 회차 h24 부호까지 반대(DS -5.68% vs GT +18.36%)였던 것이, 이번 회차 재조회 결과 DS **+12%** vs GT **+11.75%**로 **부호와 크기가 거의 일치**했다. 다만 유동성(reserve) 배율은 2.55배→**2.57배**로 소폭 확대돼 규모 괴리는 지속된다.

**BARK(notable) — ⭐h24 최초 양전 전환(손익분기 돌파)**: 풀 생성(2026-08-25T13:33:34Z, 약 19.4시간전) 이후 처음으로 h24가 -1.077%→**+4.421%**로 손익분기를 돌파했다. h1(+3.667%)·h6(+32.99%)도 양전을 유지해 전지표가 처음으로 동시 양전 상태에 도달했다 — 조기 신호 중 가장 뚜렷한 개선 흐름이다.

**C4T(notable) — ⭐CA 확정(두 소스 일치 확인)**: 이번 회차 GT 트렌딩 목록 조회에서 CA가 `2sLKA6PzFVjeTUaiKBCkDbDiS8MuoZAeXxZMgs9Apump`로 반환돼, 직전 회차 풀 직접조회 값과 정확히 일치함을 확인했다 — 지난 회차의 1자 상이(6Pz vs 7Pz) 문제가 두 소스 일치로 해소됐다(6Pz가 정확한 CA). 풀 나이 약 10.1시간전(2026-08-25T22:55:12Z 생성).

**Pistacio(notable) — h1·h6 동시 재양전(대폭반전)**: 직전 회차 첫 음전 전환이 이번 회차 1회차 만에 다시 완전 반전됐다(h1 -5.714%→+32.177%, h6 -11.651%→+7.21%, h24 재가속 +27,426.654%) — 극단적 변동성이 지속 확인된다.

**강등 3건 — Dinger·BRODIE·PANTS 🟡→🔴**: Dinger는 h1·h6·h24 전지표가 동시 재음전해 손익분기 근접 흐름이 무산됐다(h24 +0.77%→-0.93%). BRODIE는 h6·h24가 동시 재음전(h24 +41.24%→-20.28%)해 장기 양전 흐름이 처음 크게 꺾였다. PANTS는 직전 회차의 전지표 동시 재양전이 1회차 만에 다시 무산됐다(h1 +16.13%→-3.69%, h24 -29.35%→-35.66%).

**PEE — 유동성 DS값 6회 연속 완전 동일**: $7,221.25로 6회차째 변동이 전혀 없고 h1·h6도 0.00%로 고정 — 데이터 정체 징후가 더 강화됐다.

**CASHCAT(notable) — 두 풀 동시 h24 재양전 전환**: '1%'풀 h24 -5.98%→+2.747%, '0.3%'풀 h24 -7.75%→+0.537%로 두 풀 모두 음전에서 양전으로 전환됐고, 4회차 연속 '1%풀>0.3%풀' 순위가 유지돼 최근의 오실레이션이 멈춘 것으로 보인다.

**신규 발견 3건(notable) — MEEMERS·Catacio·fih**: GT 솔라나 트렌딩 top20에서 모두 2026-08-25/26 생성된 매우 신선한 풀로 신규 노출됐다. Catacio는 이름이 Pistacio와 유사해 혼동 위험이 있어 완전히 별개 컨트랙트임을 명시했다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 51회차. 유출반전,h1h6동시대폭감속(양전유지)h24는악화 | 유동성$107,692.72(-4.1%), h24-21.17%(악화) | 지속(50회차)·가속꺾임 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 59회차. 유출반전,h1가속h6재음전(대폭반전)h24는개선 | 유동성$12,884.83(-5.3%), h24-31.24%(개선) | 지속(58회차)·h6재음전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 45회차. 유입반전,h1재음전h6가속h24는재음전(대폭반전) | 유동성$29,651.48(+2.8%), h24-9.46%(재음전) | 지속(44회차)·양전유지깨짐 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 69회차. 유사,h1가속h6재음전(대폭감속)h24는개선 | 유동성$187,180.42(+0.4%), h24-19.07%(개선) | 지속(68회차)·h6손익분기수렴 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 57회차. 유입가속,h1h6동시재양전(대폭반전)h24는감속(양전유지) | 유동성$14,586.25(+5.8%), h24+16.58%(감속) | 지속(56회차)·전지표양전전환 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 40회차. 유사,h1재음전(대폭반전)h6감속h24는개선 | 유동성$31,392.99(+0.3%), h24-8.62%(개선) | 지속(39회차)·방향예측신뢰도낮음 | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 49회차. 유출반전,h1재음전h6대폭감속h24는악화 | 유동성$21,215.66(-3.2%), h24-29.50%(악화) | 지속(48회차)·개선흐름꺾임 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 81회차. 유사,h1재음전h6개선h24는개선 | 유동성$25,023.87(-1.0%), h24-40.44%(개선) | 지속(80회차)·h24여전히큰폭음전 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 47회차. 유입반전,h1유사h6개선h24는개선 | 유동성$15,770.59(+1.7%), h24-37.50%(개선) | 지속(46회차)·전지표여전히음전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 86회차. ⚠️유동성DS값6회연속완전동일,h1h6도0.00%고정 | 유동성$7,221.25(0.0%), h24-10.97%(유사) | 지속(85회차)·데이터정체지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 44회차. 유입반전,전지표동시개선(여전히전량음전) | 유동성$9,001.34(+9.7%), h24-44.05%(개선) | 지속(43회차)·여전히전지표음전 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 33회차. 유출지속,h1재음전h6악화h24는악화 | 유동성$37,099.28(-2.9%), h24-16.39%(악화) | 지속(32회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 30회차. 유출반전,h1유사h6대폭감속h24는유사(여전히극단) | 유동성$12,614.61(-5.5%), h24-65.81%(유사) | 지속(29회차)·h24여전히극단악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 33회차. 유사,h1대폭개선(여전히음전)h6가속h24는개선 | 유동성$93,937.18(-0.7%), h24-9.84%(개선) | 지속(32회차)·개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 62회차. 유사,h1재양전(대폭반전)h6개선h24는감속(양전유지) | 유동성$201,966.56(+0.4%), h24+33.66%(감속) | 지속(61회차)·단정금지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 61회차. 유출반전,h1개선h6유사h24는감속(양전유지) | 유동성$1,593,071.87(-1.1%), h24+10.37%(감속) | 지속(60회차)·단정금지 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 59회차째방향번복. 유출반전,h1재음전h6재음전h24는유사 | 유동성$233,858.89(-5.6%), h24-19.80%(유사) | 지속(58회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 52회차. 유사,h1재음전(대폭반전)h6재양전h24는악화 | 유동성$71,373.54(-1.4%), h24-22.77%(악화) | 지속(51회차)·whipsaw지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 49회차. 유입반전,h1재음전h6재양전h24는개선 | 유동성$81,043.16(+6.3%), h24-1.53%(개선) | 지속(48회차)·계속혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 46회차. 유출지속,h1악화h6악화h24는대폭감속(양전유지) | 유동성$64,120.09(-3.0%), h24+4.89%(대폭감속) | 지속(45회차)·가속흐름둔화지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/DShht9B8wCRe5t3oqdPB77PnjJbKxbYaZyuWpZQjbonk) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 37회차. 유사,h1유사h6악화h24는재음전(대폭반전) | 유동성$357,470.37(-1.4%), h24-9.31%(재음전) | 지속(36회차)·재차완전반전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 30회차. 유사,h1재양전(대폭반전)h6개선h24는유사(고착) | 유동성$6,589.32(+0.7%), h24-95.01%(고착) | 지속(29회차)·h24고착 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 29회차. ⚠️3연속재양전(전지표동시재양전) | 유동성$266,122.32(+6.8%), h24+15.69%(재양전) | 지속(28회차)·예측신뢰도최저 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 35회차. 유사,h1재양전h6가속h24는유사(양전유지) | 유동성$74,739.43(+0.4%), h24+50.66%(유사) | 지속(34회차)·신규진입절대금지 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 34회차. ⚠️h24최초음전전환(손익분기붕괴) | 유동성$20,740.12(-1.4%), h24-0.93%(재음전) | 지속(33회차)·전지표동시재음전 | 🔴(하향) | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 64회차. 유출지속,h1재양전(대폭반전)h6대폭감속h24는악화 | 유동성$467,956.05(-4.1%), h24-8.67%(악화) | 지속(63회차)·예측신뢰도낮음 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 186회차. ⭐h1 5회차연속재양전 | 유동성$471,502.44(+2.7%), h24-4.44%(개선) | 지속(185회차)·h1 5연속양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 162회차. ⚠️h6h24동시재음전(대폭반전) | 유동성$212,844.73(-5.6%), h24-20.28%(재음전) | 지속(161회차)·첫대폭재악화 | 🔴(하향) | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 65회차. 유입반전,h1재양전(대폭반전)h6재음전h24는개선 | 유동성$526,552.07(+2.0%), h24-7.69%(개선) | 지속(64회차)·단정금지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 200회차. 유출반전,h1재음전h6재음전h24는대폭감속(양전유지) | 유동성$483,354.20(-6.4%), h24+24.35%(대폭감속) | 지속(199회차)·재가속꺾임 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 191회차. 유입지속,h1재양전(대폭반전)h6유사h24는유사 | 유동성$85,029.88(+1.5%), h24-11.62%(유사) | 지속(190회차)·연속whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 191회차. 유입반전,h1재양전(대폭반전)h6가속h24는개선(전량음전) | 유동성$37,502.00(+3.7%), h24-38.14%(개선) | 지속(190회차)·여전히전량음전 | 🔴 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 149회차. 유입반전,h1재음전(대폭반전)h6대폭감속h24는유사 | 유동성$67,184.62(+1.2%), h24-17.00%(유사) | 지속(148회차)·개선흐름꺾임 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 199회차. 유출반전,h1악화h6재음전h24는악화 | 유동성$344,646.24(-2.2%), h24-12.22%(악화) | 지속(198회차)·개선흐름꺾임 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 203회차. 유출반전,h1재음전h6재음전h24는악화 | 유동성$1,128,178.71(-3.8%), h24-23.37%(악화) | 지속(202회차)·203회차달성 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 151회차. 유입반전,h1악화h6재양전(대폭반전)h24는유사(고착) | 유동성$38,640.57(+1.4%), h24-63.92%(고착) | 지속(150회차)·h1h24여전히극단악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 80회차. 유사,h1재양전(대폭반전)h6감속h24는유사 | 유동성$232,665.72(0.0%), h24-14.11%(유사) | 지속(79회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 153회차. 유입지속,h1대폭감속(양전유지)h6가속h24는재가속(대폭) | 유동성$58,354.39(+4.1%), h24+129%(재가속) | 지속(152회차)·5차스파이크재점화 | 🔴 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 51회차(dogwifpants). ⚠️직전대폭재양전이1회차만에다시무산 | 유동성$72,712.41(-1.7%), h24-35.66%(악화) | 지속(50회차)·재양전무산 | 🔴(하향) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 44회차. 유사,h1악화h6악화h24는대폭악화 | 유동성$56,811.07(-1.0%), h24-45.12%(악화) | 지속(43회차)·전지표동시재악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 38회차. ⚠️손익분기근접흐름무산,h24악화 | 유동성$7,826.59(-2.5%), h24-2.57%(악화) | 지속(37회차)·손익분기이탈 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 37회차. 유입반전,h1재양전h6재양전h24는개선 | 유동성$214,885.07(+1.3%), h24-4.59%(개선) | 지속(36회차)·소폭개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 36회차. 유출가속,전지표동시악화(전량음전) | 유동성$18,171.87(-11.8%), h24-38.90%(악화) | 지속(35회차)·신규진입절대금지유지 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |
| **CATE** | Solana(PumpSwap) | 미확인 | 123회차달성. 유출반전,h1재양전h6감속h24는재음전(대폭반전) | 유동성$2,280,725.31(-2.1%), h24-1.09%(재음전) | 지속(122회차)·장기whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |

> **편입/편출/강등/재승격 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. **강등 3건**(Dinger 🟡→🔴, BRODIE 🟡→🔴, PANTS 🟡→🔴). 활성목록 **44→44종**(순증감 0, 조기13/확산10/뒷북21). notable **71→74개**(신규 3건: MEEMERS·Catacio·fih, 모두 GT트렌딩 신규노출). **핵심 이벤트**: ⚠️⚠️'제2의 DTF' 토큰이 1회차 만에 극단 붕괴(reserve -84.3%·h24 +140만%→-3.5%), Swan GT-DS괴리 6.30배로소폭완화, AI/NVDA(BANKR) DS-GT방향불일치 해소, BARK h24최초양전전환, C4T CA확정(두소스일치), Pistacio h1h6동시재양전, CASHCAT두풀동시재양전.

## 온체인 신호 상세

- **DTF(둘째,notable) 붕괴 상세**: GT: reserve$885,582.89→$138,987.34(-84.3%), h1+477.047%→-56.103%, h6+332.634%→-87.101%, h24+1,403,983.595%→-3.512%. 거래량h24 $47,684,558.71(reserve대비약343배회전율). 풀나이약25.6시간(2026-08-25T07:25Z생성) · 2026-08-26T09:00:00Z
- **DTF(메인,notable) 상세**: GT reserve$217,280.43→$205,390.91(-5.5%,유출반전), h1+12.763%→+6.7%(감속,양전유지), h6+40.687%→-7.172%(재음전,대폭반전), h24+329.62%→+230.474%(대폭감속,여전히3자리%대). 풀개수는 **최소 130개**(2026-08-26 09:20Z 부모 재집계). ⚠️GT `/pools`는 페이지당 20건 상한에 총계 메타가 없고 8페이지째부터 레이트리밋으로 막혀 **전수는 미확정**이다. 직전 회차에 적은 129개도 같은 이유로 하한값이었다(부모 자기정정).
- **Swan(notable) 상세**: GT reserve$88,748→$94,033.705(+6.0%,유입반전), h1-3.54%→+3.252%(재양전,대폭반전), h6+27.23%→+62.533%(대폭가속), h24+15,404%→+17,197.624%(가속). DS재조회: liquidity$91,900.96, h1-4.62%, h6+75.71%, h24+108,384%(GT대비약6.30배괴리,직전6.63배에서완화). 풀나이약14.8시간(2026-08-25T18:12:54Z생성) · 2026-08-26T09:00:00Z
- **AI/NVDA(BANKR,notable) 상세**: GT재확인: reserve$4,865,568.18→$4,994,507.39(+2.6%), h1-5.835%→-8.242%(악화), h6+25.377%→-5.081%(재음전), h24+18.356%→+11.75%(감속). DS재조회: liquidity$1,908,089.50→$1,940,535.08(+1.7%), h1-1.57%→-6.55%, h6+14.11%→-4.4%(재음전), h24-5.68%→**+12%**(재양전,GT+11.75%와방향·크기거의일치). 유동성배율2.55배→2.57배로소폭확대 · 2026-08-26T09:00:00Z
- **BARK(notable) 상세**: GT reserve$16,052.38→$16,738.77(+4.3%,유입지속), h1+4.385%→+3.667%(유사,양전유지), h6+29.469%→+32.99%(유사,양전유지), h24-1.077%→**+4.421%**(재양전,최초손익분기돌파). 풀나이약19.4시간(2026-08-25T13:33:34Z생성) · 2026-08-26T09:00:00Z
- **C4T(notable) 상세**: GT reserve$35,742.17→$36,484.65(+2.1%,유입반전), h1+67.385%→-4.095%(대폭감속,재음전), h6-61.945%→-24.485%(개선), h24+69.212%→+75.586%(가속), 24h거래량$3,309,968.83(reserve대비약90.7배회전율). CA `2sLKA6PzFVjeTUaiKBCkDbDiS8MuoZAeXxZMgs9Apump`로두소스일치확인. 풀나이약10.1시간(2026-08-25T22:55:12Z생성) · 2026-08-26T09:00:00Z
- **Pistacio(notable) 상세**: GT reserve$354,476.07→$378,962.42(+6.9%,유입반전), h1-5.714%→+32.177%(재양전,대폭반전), h6-11.651%→+7.21%(재양전,대폭반전), h24+24,146.796%→+27,426.654%(재가속). 풀나이약13.6시간(2026-08-25T19:22:21Z생성) · 2026-08-26T09:00:00Z
- **CASHCAT(notable) 상세**: GT: '1%'풀 reserve$4,642,556→$5,317,359.65(+14.5%)·h24-5.98%→+2.747%(재양전), '0.3%'풀 reserve$2,298,557→$2,409,530.54(+4.8%)·h24-7.75%→+0.537%(재양전). 4회차연속1%>0.3%순위유지 · 2026-08-26T09:00:00Z
- **신규발견(notable) 상세**: MEEMERS(Solana, reserve$37,576.98, h24+334.807%, 당일생성). Catacio(Solana, reserve$47,571.65, h24+311.044%, 당일생성, Pistacio와유사명주의). fih(Solana, reserve$98,979.64, h24+1997.221%, 24h거래량$5,753,274.02로reserve대비약58배회전율) · 2026-08-26T09:00:00Z
- **강등 3건 상세**: Dinger 유동성$21,034.47→$20,740.12(-1.4%), h1+2.99%→-3.24%, h6+24.59%→-4.08%, h24+0.77%→-0.93%(전지표동시재음전). BRODIE 유동성$225,418.86→$212,844.73(-5.6%), h6+14.61%→-16.42%, h24+41.24%→-20.28%(h6h24동시재음전). PANTS 유동성$73,969.65→$72,712.41(-1.7%), h1+16.13%→-3.69%, h24-29.35%→-35.66%(재양전1회차만에무산) · 2026-08-26T09:00:00Z
- **나머지 상세**: OBS가속꺾임. PEPECOIN h6재음전. MAPLE양전유지깨짐. CLOCKIN h6손익분기수렴. TIPANSEM전지표양전전환. LIZARD재음전. 1B개선흐름꺾임. CLUG h24여전히큰폭음전. FLUSH전지표여전히음전. PEE데이터정체지속(6회연속동일). 40M여전히전지표음전. MANEKI혼조. CYBERCAT h24여전히극단악화. omo개선. swappy단정금지. CYBERLEEK단정금지. CC워시트레이딩의심불변. Z500whipsaw지속. KIRK계속혼조. CONK가속흐름둔화지속. CHUMP재차완전반전. CATALORIAN h24고착. TRUTH신규진입절대금지. HOOKR예측신뢰도낮음. JUGGERNAUT h1 5연속양전. GOOD단정금지. PRINTER재가속꺾임. Dealer연속whipsaw. lickingcat여전히전량음전. CALLOOOR개선흐름꺾임. TOAD개선흐름꺾임. FWA 203회차달성. DPG h1h24여전히극단악화. BULLSHIT혼조. PITCOIN 5차스파이크재점화. Doge2전지표동시재악화. Truth Coin손익분기이탈. BARRON소폭개선. YOMOGI신규진입절대금지유지. CATE장기whipsaw이력 · 2026-08-26T09:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 41종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 DexScreener 배치조회 재확인, GT 트렌딩(로빈후드체인 top20·솔라나 top20) 교차검증, 우선추적과제(DTF·DTF둘째·Pistacio·BARK·Swan·C4T·AI/NVDA(BANKR)·CASHCAT) 개별 풀·직접조회 재확인에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 07:00Z)로부터 **정상 2시간** 경과, 유실 없음.
- **저장 후 세 파일(json·csv·md) 종목 목록 대조**: tokens(json) 44종·csv 44행(헤더 제외)·md 3개 표(조기13+확산10+뒷북21=44) 전부 일치 확인함(OBS~PROLOGUE까지 개별 이름 대조 완료). notable(json) 74건(신규 3건: MEEMERS·Catacio·fih 반영).
- **⚠️⚠️'제2의 DTF' 토큰이 발견 직후 1회차 만에 극단 붕괴했다.** reserve가 84.3% 급감하고 h24가 +140만%대에서 -3.5%로 완전히 소멸했으며, 24h 거래량은 오히려 $47.7M로 급증(회전율 약 343배)해 러그·워시트레이딩·청산 캐스케이드 가능성을 강하게 시사한다. 우리가 계속 추적 중인 메인 DTF(0xee5576fa…)는 이번에도 3자리%대 안정 흐름을 유지해 두 토큰의 궤적이 극명하게 갈리고 있다.
- **C4T의 CA 불확실성이 이번 회차 해소됐다** — GT 트렌딩 목록 조회와 직전 회차 풀 직접조회 결과가 `2sLKA6PzFVjeTUaiKBCkDbDiS8MuoZAeXxZMgs9Apump`로 정확히 일치했다.
- **AI/NVDA(BANKR)의 DS-GT h24 부호 불일치가 이번 회차 해소됐다** — 지난 회차 DS -5.68% vs GT +18.36%였던 것이 이번엔 DS +12% vs GT +11.75%로 방향·크기가 거의 일치했다. 다만 유동성(reserve) 규모 배율(2.57배)은 여전히 큰 괴리다.
- **데이터 신뢰도**: DexScreener 배치조회(로빈후드15·솔라나14+14·이더리움1)와 GeckoTerminal 트렌딩(로빈후드체인 top20·솔라나 top20)·개별 풀 직접조회로 교차검증했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
