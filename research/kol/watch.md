# 온체인 트렌딩 조기경보 — 2026-08-25 07:00 UTC (KST 2026-08-25 16:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-25 05:00Z)로부터 **정상 2시간** 경과. 유실 없이 정상 진행됐다.

44개 활성종목 전부를 DexScreener 배치조회(chainId별 tokens/v1 다중주소 API, 로빈후드 1배치 15/솔라나 2배치 14+14/이더리움 1배치 1)로 재확인했다. 요청 개수와 응답 개수가 전부 일치했다. 추가로 GeckoTerminal 솔라나 트렌딩(top20, 2페이지)·로빈후드체인 트렌딩(top20, network id `robinhood`로 정정 — 이번 회차 `robinhood-chain` id는 404 확인)을 조회해 다수 notable 항목을 교차확인하고 신규 트렌딩 종목 3건(TRENCHERS·PCAT·Jimothy)을 발견했다.

## 이번 회차 핵심 발견

**JUGGERNAUT·CYBERCAT — 직전 회차 반전이 다시 재반전(whipsaw 지속)**: JUGGERNAUT는 직전 회차 2연속 대폭유입 뒤 유출로 첫 제동이 걸렸었으나, 이번 회차 다시 유입(+8.2%)으로 돌아서고 h24가 +97.14%→+136%로 재가속했다. CYBERCAT도 직전 대폭 유출(-27.4%) 뒤 이번엔 유입(+13.3%)·h1 재양전(+22.79%)으로 반전했으나 h6·h24는 여전히 극단적 음전(-32.83%/-82.97%) 상태다. 둘 다 대칭원칙상 단정하지 않는다.

**PROLOGUE·PRINTER·PITCOIN — 장기 개선 streak에 첫 제동**: 세 토큰 모두 여러 회차 이어지던 강한 개선 흐름이 이번 회차 처음으로 주춤했다. PROLOGUE는 h1이 처음 재음전(+11.24%→-4.67%)했으나 h6·h24는 여전히 고수준(+53.28%/+124%)을 유지했다. PRINTER는 직전 회차의 "이례적 급가속" 뒤 유출 반전(-3.3%)·h1 재음전으로 조정에 들어갔다. PITCOIN은 139회차 동안 이어지던 안정적 개선이 이번 회차 유출(-4.9%)·h1 재음전으로 처음 반전했다. 셋 다 🟢 판정은 유지하되 단 1회차 반전이라 다음 회차 확인이 필요하다.

**Z500·TOAD — 장기 흐름의 완전 반전 또는 전면 악화**: Z500은 장기 개선 streak가 h1·h6·h24 전지표 재음전으로 완전히 반전됐다(h24 +14.05%→-4.41%). TOAD는 유출 반전과 함께 h1·h6·h24가 동시에 악화됐다(h24 -2.98%→-14.63%) — 단 1회차 반전이라 단정하지 않는다.

**CATALORIAN — 악화 가속**: 이미 거의 완전 소멸 상태이던 토큰이 이번 회차 유출 폭이 -18.8%→-18.9%로 유지되는 가운데 h1·h6가 각각 -37.81%·-56.57%로 대폭 악화됐다(h24 -99.11%, 사실상 완전소멸에 근접).

**PEPECOIN — 드물게 전지표가 한 방향으로 급격 악화**: 대부분 회차 혼조를 보이던 토큰이 이번엔 유동성(-13.9%)·h1(재음전,-23.29%)·h6(-25.89%)·h24(-49.06%) 전부가 동시에 나빠졌다. 단 1회차 반전이라 판정은 유지하되 다음 회차 확인이 특히 중요하다.

## 🚨 notable — Allocate 붕괴 확정, AI/NVDA(BANKR) DS-GT 괴리 지속

**Allocate(notable) — 지난 회차 "저베이스아티팩트 의심" 경고가 실제 붕괴로 확인됨**: 직전 회차 h1+3537%·h24+97% 극단치를 "사후 설명 없이 원인미상 극단치로 정직 기록"했는데, 이번 회차 GT 재확인 결과 유동성이 $154,985.94→$6,950.62로 -95.5% 붕괴하고 h1도 -97.20%로 극단 반전했다. 사전 경고가 사후에 실증된 사례다.

**AI/NVDA(BANKR, notable) — 동일 pairAddress에서 DS-GT 수치 괴리가 재확인됨**: 이전 DS 단독조회 liquidity $1,777,598.11과 이번 GT 재확인 reserve $4,776,705.93이 같은 pairAddress(0xcbdfea9...)를 참조하면서도 약 2.7배 차이를 보였다. 같은 풀·비슷한 시점대에 소스 간 수치가 이렇게 크게 어긋나는 것은 이례적이라 3회차째 정직 기록하고 단정적 해석은 계속 보류한다.

**LOOKSMAX(notable) — CA 확정**: GeckoTerminal 솔라나 트렌딩 재노출로 CA(GPzpoXpD74E2C4CJNayuoyBqPQJEsPtdse3nhntrpump)를 확정했다. 유동성도 $148,466.97→$190,146.32(+28.1%)로 대폭 유입됐다.

**신규 notable 3건**: TRENCHERS(솔라나, 풀생성 약 8.2시간 전으로 이번 회차 발견 중 가장 신선, h24+419%), PCAT(로빈후드체인, h24+926%이나 풀나이 약 5.2주로 "막 붙기 시작"은 아니며 Allocate 선례처럼 저베이스 아티팩트 가능성 정직 기록), Jimothy(솔라나, 유동성 $1M 이상으로 이미 확산 국면).

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 38회차. 대폭반전후소폭유출전환 | 유동성$118,830.78(-3.6%), h24+21.14%(대폭감속) | 지속(37회차)·소폭유출 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 46회차. ⚠️전지표동시급격악화 | 유동성$15,994.46(-13.9%), h24-49.06%(대폭악화) | 지속(45회차)·급격악화 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 32회차. 유동성유사,혼조 | 유동성$28,174.39(+1.4%), h24-1.4%(재음전) | 지속(31회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 56회차. 유사,h1h6재음전 | 유동성$224,377.91(-1.3%), h24+15.17%(가속) | 지속(55회차)·56회차째whipsaw | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 44회차. 유출지속,h1재음전 | 유동성$12,295.11(-2.0%), h24-30.36%(악화) | 지속(43회차)·유출지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 27회차. 유입,h24대폭악화 | 유동성$33,760.42(+3.6%), h24-30.87%(대폭악화) | 지속(26회차)·h24급격악화 | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 36회차. 유사,h1재양전 | 유동성$23,353.93(+0.9%), h24-41.26%(유사) | 지속(35회차)·단정금지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 68회차. 유입지속,전지표개선 | 유동성$34,509.60(+2.3%), h24+2.99%(재양전) | 지속(67회차)·전지표개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 34회차. 유출지속,전지표재악화 | 유동성$21,087.33(-2.9%), h24-58.86%(추가악화) | 지속(33회차)·추가악화 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 73회차. 유입,전지표가속 | 유동성$8,186.33(+2.7%), h24+12.37%(가속) | 지속(72회차)·가속 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 31회차. 유사,h1재음전 | 유동성$12,574.22(+0.5%), h24-16.41%(악화) | 지속(30회차)·약세혼조 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 20회차. 2연속유출지속 | 유동성$40,219.52(-5.5%), h24-57.23%(대폭악화) | 지속(19회차)·반전확정판단강화 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 17회차. 유입반전,h1대폭재양전 | 유동성$25,162.46(+13.3%), h24-82.97%(유사) | 지속(16회차)·whipsaw재확인 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 20회차. 유사,h1재양전h6h24악화 | 유동성$108,328.93(+1.4%), h24-8.63%(악화) | 지속(19회차)·재음전지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 49회차. 유사,h1재양전 | 유동성$169,157.29(-0.4%), h24-41.31%(유사) | 지속(48회차)·whipsaw심화 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 48회차. 유사,h1재양전h6h24악화 | 유동성$1,501,734.34(-0.8%), h24-35.54%(유사) | 지속(47회차)·연속whipsaw | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 46회차째방향번복. 유출,h1h24개선 | 유동성$278,138.90(-5.5%), h24-24.57%(개선) | 지속(45회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 39회차. ⚠️장기개선streak완전반전 | 유동성$79,212.11(-2.5%), h24-4.41%(재음전) | 지속(38회차)·완전반전확정 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 36회차. 유입지속,개선흐름강화 | 유동성$80,989.83(+0.8%), h24+5.82%(재양전) | 지속(35회차)·개선흐름강화 | 🟡 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 33회차. 유출반전,깊은음전권 | 유동성$59,318.44(-4.9%), h24-39.72%(유사악화) | 지속(32회차)·깊은음전권 | 🔴 | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 24회차. 거의보합,h24가속 | 유동성$371,547.56(~0%), h24+27.39%(가속) | 지속(23회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 17회차. ⚠️유출가속,전지표대폭악화 | 유동성$34,233.81(-18.9%), h24-99.11%(유사) | 지속(16회차)·거의완전소멸 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 16회차. 유입지속,h1첫재음전 | 유동성$271,096.57(+1.8%), h24+124%(감속) | 지속(15회차)·개선흐름첫제동 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 22회차. 유동성값3회차연속완전동일 | 유동성$48,693.63(0%,3회차연속동일) | 지속(21회차)·데이터신뢰도경고 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 21회차. 유입반전,전지표개선 | 유동성$21,107.22(+6.1%), h24-49.38%(개선) | 지속(20회차)·개선지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 51회차. 유입지속,h6h24재가속 | 유동성$499,276.33(+3.0%), h24+51.34%(가속) | 지속(50회차)·재가속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 173회차. ⭐직전첫제동뒤재반전 | 유동성$489,697.10(+8.2%), h24+136%(재가속) | 지속(172회차)·단1회차반전후재회복 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 149회차. 유입,h6재양전 | 유동성$190,902.75(+3.2%), h24+4.53%(가속) | 지속(148회차)·점진개선지속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 52회차. 유사,h6악화h24감속 | 유동성$553,041.39(-1.3%), h24+27.56%(감속) | 지속(51회차)·감속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 187회차. ⚠️급가속뒤소폭조정 | 유동성$446,690.03(-3.3%), h24+61.03%(대폭감속) | 지속(186회차)·단1회차조정 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 178회차. 유입,h6재양전 | 유동성$91,788.62(+1.8%), h24-32.05%(유사) | 지속(177회차)·연속whipsaw이력상단정금지 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 178회차. 8회차연속지그재그 | 유동성$48,197.79(+2.0%), h24-37.2%(개선) | 지속(177회차)·8회차연속지그재그 | 🟡 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 136회차. 유사,혼조지속 | 유동성$73,552.33(-0.7%), h24+11.72%(가속) | 지속(135회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 186회차. ⚠️유출반전,전면악화 | 유동성$366,130.88(-4.0%), h24-14.63%(악화) | 지속(185회차)·전면악화 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 190회차. 유사,h6재음전h24감속 | 유동성$1,319,079.20(-1.4%), h24+11.2%(감속) | 지속(189회차)·안정화조짐 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 138회차. ⚠️유출반전,혼조로회귀 | 유동성$65,121.51(-4.8%), h24-14.74%(재음전) | 지속(137회차)·혼조로회귀 | 🟡 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 67회차. 3연속유입종료 | 유동성$252,235.24(-2.4%), h24+4.82%(대폭감속) | 지속(66회차)·유입종료 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 31회차. 유입지속,h24가속 | 유동성$74,959.65(+9.7%), h24+125%(가속) | 지속(30회차)·2연속유입 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 110회차달성. 2연속유출지속 | 유동성$2,209,957.44(-4.6%), h24+70.7%(감속) | 지속(109회차)·장기whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 38회차(dogwifpants). 유입반전 | 유동성$89,256.44(+2.7%), h24-25.12%(개선) | 지속(37회차)·유입반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 25회차. ⚠️h1처음측정불가 | 유동성$8,212.71(-0.8%), h24-34.58%(유사) | 지속(24회차)·데이터갭신규발생 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 24회차. 유사,h6악화 | 유동성$224,959.52(-0.5%), h24-2.04%(유사) | 지속(23회차)·유출반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 23회차. 유출지속,h6대폭악화 | 유동성$25,096.06(-2.9%), h24-17.78%(개선) | 지속(22회차)·지그재그지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. 활성목록 **44→44종**(순증감 0). notable **49→52개**(신규 3건: TRENCHERS·PCAT·Jimothy, 나머지는 GT/DS 재확인 갱신 또는 carryover). **핵심 이벤트**: JUGGERNAUT·CYBERCAT가 직전 회차 반전에서 다시 재반전(whipsaw 지속), PROLOGUE·PRINTER·PITCOIN 3종이 장기 개선streak에 첫 제동, Z500·TOAD는 전면 악화, CATALORIAN·PEPECOIN은 급격 악화. Allocate(notable)는 지난 회차 경고했던 "저베이스아티팩트 의심"이 실제 붕괴(-95.5%)로 확인됨. AI/NVDA(BANKR) DS-GT 괴리(약2.7배) 지속.

## 온체인 신호 상세

- **JUGGERNAUT·CYBERCAT 재반전 상세**: JUGGERNAUT 유동성+8.2%(직전-5.0%에서재반전), h24+97.14%→+136%. CYBERCAT 유동성+13.3%(직전-27.4%에서재반전), h1-1.14%→+22.79%(재양전)하나 h6·h24는여전히극단음전 · 2026-08-25T07:00:00Z
- **PROLOGUE·PRINTER·PITCOIN 개선streak 첫 제동 상세**: PROLOGUE h1+11.24%→-4.67%(첫재음전, h6h24는고수준유지). PRINTER 유동성+18.2%→-3.3%(유출반전), h1+18.46%→-1.01%(첫재음전). PITCOIN 유동성+6.2%→-4.9%(첫유출반전, 139회차만의첫반전) · 2026-08-25T07:00:00Z
- **Z500·TOAD 전면악화 상세**: Z500 h1+1.45%→-7.72%, h6+2.17%→-13.62%, h24+14.05%→-4.41%(전지표동시재음전,장기streak완전반전). TOAD 유동성-4.0%(유출반전), h1-2.22%→-9.63%, h6-5.09%→-13.01%, h24-2.98%→-14.63%(전지표동시악화) · 2026-08-25T07:00:00Z
- **CATALORIAN·PEPECOIN 급격악화 상세**: CATALORIAN 유동성-18.9%(유출가속), h1-5.8%→-37.81%, h6-27.52%→-56.57%(둘다대폭악화), h24-99.11%(거의완전소멸근접). PEPECOIN 유동성-13.9%, h1+9.24%→-23.29%(재음전), h6-4.81%→-25.89%, h24-29.32%→-49.06%(전지표동시급격악화,드문패턴) · 2026-08-25T07:00:00Z
- **Allocate(notable) 붕괴확정 상세**: 유동성$154,985.94→$6,950.62(-95.5%), h1+3537.132%→-97.202%(극단반전), h24+97.476%→-94.47%(대폭붕괴). 직전회차'저베이스아티팩트의심'경고가실증됨 · 2026-08-25T07:00:00Z
- **AI/NVDA(BANKR) DS-GT괴리 상세**: 동일pairAddress(0xcbdfea9...)에서 이전DS liquidity$1,777,598.11 vs 이번GT reserve$4,776,705.93(약2.7배차이), 방향(양전)은일치하나규모괴리지속 · 2026-08-25T07:00:00Z
- **나머지 상세**: OBS 소폭유출로전환. MAPLE 혼조. CLOCKIN 56회차째whipsaw. TIPANSEM 유출지속. LIZARD h24급격악화. 1B 단정금지. CLUG 전지표개선. FLUSH 추가악화. PEE 가속. 40M 약세혼조. MANEKI 반전확정판단강화. omo 재음전지속. swappy whipsaw심화. CYBERLEEK 연속whipsaw. CC 워시트레이딩의심불변. KIRK 개선흐름강화. CONK 깊은음전권. CHUMP 혼조. TRUTH 데이터신뢰도경고3회차연속. Dinger 개선지속. HOOKR 재가속. GOOD 감속. Dealer 연속whipsaw. lickingcat 8회차연속지그재그. CALLOOOR 혼조. FWA 안정화조짐. DPG 혼조로회귀. BULLSHIT 유입종료. Doge2 2연속유입. CATE 장기whipsaw이력. PANTS 유입반전. Truth Coin 데이터갭신규발생. BARRON 유출반전. YOMOGI 지그재그지속. BRODIE 점진개선지속 · 2026-08-25T07:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 40종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 DexScreener 배치조회 재확인, GT 트렌딩(솔라나·로빈후드체인 각 top20) 교차검증에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-25 05:00Z)로부터 **정상 2시간** 경과, 유실 없음.
- **GeckoTerminal network id 정정**: 이번 회차 `robinhood-chain` id로 조회 시 404가 발생해 `robinhood`로 재시도해 성공했다. 과거 회차들이 어떤 id로 성공했는지는 로그가 남지 않아 확인 불가하나, 이번 회차부터는 `robinhood`가 정상 동작함을 기록해둔다.
- **DexScreener 배치조회 전량 정상 응답**: 로빈후드 1배치(15)·솔라나 2배치(14+14)·이더리움 1배치(1) 총 4개 배치 전부 요청 개수와 응답 개수가 일치했다.
- **whipsaw 지속을 단정적 신호로 해석하지 않음**: JUGGERNAUT·CYBERCAT의 재반전은 이 워치에서 반복적으로 관찰되는 패턴(직전 반전이 다시 뒤집힘)이라 대칭원칙에 따라 판정을 유지했다. PROLOGUE·PRINTER·PITCOIN의 "장기streak 첫 제동"도 단 1회차라 단정하지 않는다.
- **Allocate 사례는 이 워치의 정직성 원칙이 실제로 작동한 사례로 기록**: 극단치를 사후 설명 없이 "원인미상"으로 정직 기록했던 판단이 다음 회차에 실제 붕괴로 실증됐다.
- **데이터 신뢰도**: DexScreener 배치조회와 GeckoTerminal 트렌딩(솔라나·로빈후드체인 top20, 각 2페이지) 교차검증으로 다수 종목의 방향성 일치를 확인했다. AI/NVDA(BANKR)는 동일 풀에서도 소스 간 수치 괴리가 지속돼 정직하게 병기·보류 처리했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
