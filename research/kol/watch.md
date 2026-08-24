# 온체인 트렌딩 조기경보 — 2026-08-24 17:00 UTC (KST 2026-08-25 02:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전(2026-08-24 15:00Z)로부터 정확히 **2시간** 경과했다(정시 슬롯 정상 진행).

> 44개 활성종목 전부를 DexScreener 토큰 API(및 token-pairs API)로 재확인했다. 다수 배치조회에서 **`pairs:null`(전 조회 실패) 응답이 다수 발생**해 개별·소규모 재조회로 정정했고, **BRODIE는 배치조회에서 소형 풀($36,701)이 잘못 매칭돼** token-pairs 개별조회로 올바른 주풀(0x9870C395…, 유동성$174,714.50)을 재확인했다. **40M도 과거 CLUG와 혼동됐던 pairAddress(Ct6arp861…)가 다시 반환돼 별도 pair 직접조회 + token-pairs 교차검증**을 거쳐 이번엔 정말로 40M 소유의 정상 pair임을 확인했다(요청주소·baseToken.address 완전일치).

> **⚠️ 이번 회차 핵심 발견 — 직전 상향 2건(OBS·KIRK)이 나란히 첫 반전**: 15:00Z 회차에서 3~4연속 개선 근거로 🟢 상향했던 **OBS·KIRK가 이번 회차 동시에 반전**했다(OBS: 유동성-10.1%·h24 +131%→+59.21%로 대폭감속, GT 교차확인도 동일방향 h24+58.92%로 진짜 반전임을 확인. KIRK: 유동성-13.1%·h6h24 모두 재음전). 두 토큰 모두 **단 1회차 반전**이라 색상은 유지하되(직전 BRODIE·PROLOGUE 사례와 동일 원칙), 다음 회차가 중요 분기점이다. **JUGGERNAUT(4연속개선후첫반전)·BRODIE(140회차만에첫유출이 2연속으로확인)**도 같은 패턴이라 함께 주시한다.

> **CLUG, 3연속 h24악화+2연속유동성유출로 🟡→🔴 하향**: OBS 상향에 쓴 "3연속" 기준을 대칭 적용해, h24가 -21.55%→-38.06%→-45.75%로 3회 연속 악화하고 유동성도 2회 연속 유출된 CLUG를 이번 회차 하향한다.

> **편입/편출/강등 내역**: **신규편입 0건**. **편출 0건**. 활성목록 **44→44종**(순증감 0). notable **41→41개**(신규 없음, 기존 항목 데이터 갱신). **CSV 파일에서 Doge2가 누락돼 있던 기존 결함을 이번 회차에 정정**(JSON·MD는 44개였으나 CSV는 43개였음).

## 🚨 주요 사건 — OBS·KIRK, 상향 직후 나란히 첫 반전

15:00Z 회차에서 각각 "3연속개선+대폭가속"·"2연속유입+h24h6반전강세"를 근거로 🟡→🟢 상향한 두 종목이 이번 회차 동시에 꺾였다.
- **OBS**: 유동성 $129,042.68→$116,071.83(-10.1%,유출반전), h1+2.69%→-9.48%(재음전), h6+53.22%→+25.1%(대폭감속), h24+131%→+59.21%(대폭감속). GeckoTerminal 로빈후드체인 트렌딩에서 독립 확인한 h24+58.92%도 같은 방향이라, DS 오류가 아니라 진짜 반전으로 판단된다.
- **KIRK**: 유동성 $83,253.82→$72,319.47(-13.1%,유출반전), h1-9.55%→-19.91%(악화), h6+29.58%→-4.74%(재음전), h24+17.16%→-9.56%(재음전반전).

직전 회차에서 확립한 "첫 반전 신호는 단정하지 않고 색상 유지 + 다음 회차 확인 필요로만 표시"라는 원칙(BRODIE·PROLOGUE 사례)을 동일하게 적용해, 이번 회차도 둘 다 🟢을 유지하되 강한 주의 문구를 달았다. 다음 회차에 개선이 재개되는지 악화가 이어지는지가 중요한 분기점이다.

## 🚨 주요 사건 — CLUG, "3연속" 기준 대칭 적용으로 🔴 하향

OBS 상향 근거였던 "3연속 개선" 판정 기준을 하향 방향에도 대칭 적용했다. CLUG는 h24가 -21.55%→-38.06%→-45.75%로 **3회 연속 악화**했고 유동성도 이번 회차까지 **2회 연속 유출**(-3.0%→-6.4%)이라, 단발성 노이즈가 아닌 구조적 악화 패턴으로 판단해 🟡→🔴로 하향한다.

## 그 밖 특기 사항 — 지그재그 4종목, 이번엔 3/4가 패턴 미재현

- **HOOKR·CALLOOOR·FWA**: 직전까지 2회차 연속 반전(지그재그)이 확정됐던 종목들인데, 이번 회차는 **재반전 대신 직전 방향을 그대로 유지**(모두 개선 방향 지속)했다. HOOKR h24+149%→+163%(GT+166.87%로 교차확인), CALLOOOR h24+23.1%→+66.21%, FWA h24+28.36%→+36.97%(h1은 보합권 근접에서 +22.15%로 급반등). 지그재그가 "규칙적으로 반복"되는 패턴이 아니었음을 시사하나, 3연속 확인 전까지는 상향하지 않고 🟡을 유지한다.
- **lickingcat**: 나머지 3종과 달리 이번에도 재반전(3회차 연속 지그재그) — h24+17.83%→-0.91%로 재음전. whipsaw 패턴이 가장 뚜렷한 종목으로 남았다.
- **FLUSH, 6회차 연속 악화**: 5연속에서 6연속으로 늘었다. 유동성 -6.6% 추가 유출, h24 -52.56%. 🔴 최상위 경계 유지.
- **PROLOGUE, 9연속유입종료가 단발성이었음 확인**: 직전 회차 "9연속유입 첫 종료"가 이번 회차 유동성 +7.9% 유입 재개로 반전됐다. 노이즈였다고 판단, 🟢 유지.
- **BRODIE, 첫유출조짐이 2연속으로 확인**: 유동성 -6.9% 추가 유출(140회차만에 첫유출→2연속유출). 배치조회 오류를 token-pairs 개별조회로 정정한 뒤의 수치. 🟢 유지하되 다음 회차가 분기점.
- **CASHCAT, 38회차만에 첫유출이 단발성이었음 확인(notable)**: GT 재확인 결과 유동성이 $1,775,191→$1,811,603(+2.0%)로 다시 증가, 직전 회차 첫 유출은 노이즈였던 것으로 보인다.
- **CATCUS, 4회차 연속 유입(notable)**: GT 솔라나 트렌딩 9위(직전 13위에서 상승), 유동성 +10.5%로 4연속 유입. 편입 후보로 점점 근접 중이나 풀 나이가 여전히 1일 미만 추정이라 이번 회차도 보류.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 33회차. ⚠️상향직후첫반전 | 유동성$116,071.83(-10.1%), h24+59.21%(대폭감속) | 지속(32회차)·상향직후첫반전 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 41회차. 혼조지속,h1재음전 | 유동성$19,180.05(-5.5%), h24-21.52%(유사악화) | 지속(40회차)·혼조지속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 27회차. 유출,h1악화 | 유동성$27,200.39(-5.9%), h24+28.14%(유사) | 지속(26회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 51회차. 유입지속,h1재음전 | 유동성$232,838.91(+8.9%), h24+15.49%(감속) | 지속(50회차)·51회차째whipsaw | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 39회차. whipsaw지속,유사수준 | 유동성$13,684.62(-2.2%), h24-22.06%(유사) | 지속(38회차)·whipsaw지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 22회차. 연속whipsaw지속 | 유동성$34,065.36(-5.3%), h24-16.11%(개선) | 지속(21회차)·연속whipsaw | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 31회차. h1악화,h24는가속 | 유동성$27,322.65(-0.8%), h24+68.15%(가속) | 지속(30회차)·연속급반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 63회차. ⚠️h24 3연속악화하향 | 유동성$32,577.59(-6.4%), h24-45.75%(3연속악화) | 지속(62회차)·하향(3연속확정) | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 29회차. ⭐6연속전지표악화 | 유동성$23,467.77(-6.6%), h24-52.56%(추가악화) | 지속(28회차)·6연속악화 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 68회차. 유사,h1h6재음전 | 유동성$7,284.10(-3.7%), h24+3.23%(재양전) | 지속(67회차)·정체 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 26회차. h24 2연속양전 | 유동성$12,978.84(-1.6%), h24+25.31%(가속) | 지속(25회차)·h24 2연속양전 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 15회차. 14회차째whipsaw,대폭악화 | 유동성$42,084.75(-22.7%), h24-7.27%(방향반전) | 지속(13회차)·whipsaw14회차 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 12회차. 정점통과,4연속유출 | 유동성$24,311.58(-30.9%), h24-89.35%(추가악화) | 지속(11회차)·4연속유출심화 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 15회차. 깊은음전권,h24소폭개선 | 유동성$104,737.60(-4.3%), h24-39.46%(개선) | 지속(14회차)·깊은음전권 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 44회차. ⭐2연속유입+2연속h24양전 | 유동성$216,106.57(+1.9%), h24+15.44%(가속) | 지속(43회차)·2연속개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 43회차. 재음전반전,연속whipsaw | 유동성$1,699,414.81(-11.0%), h24-22.29%(재음전) | 지속(42회차)·연속whipsaw | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 41회차째방향번복. h24대폭감속 | 유동성$294,403.41(-6.7%), h24+21.14%(대폭감속) | 지속(40회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 34회차. 유사,h24유사악화 | 유동성$78,142.80(-0.4%), h24-17.90%(유사) | 지속(33회차)·장기악화흐름지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 31회차. ⚠️상향직후첫반전 | 유동성$72,319.47(-13.1%), h24-9.56%(재음전반전) | 지속(30회차)·상향직후첫반전 | 🟢 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 28회차. 유입반전,소폭개선 | 유동성$58,435.52(+2.5%), h24-55.36%(개선) | 지속(27회차)·소폭개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 19회차. 유출반전,h24양전유지 | 유동성$324,059.97(-10.1%), h24+24.17%(양전유지) | 지속(18회차)·혼조전환 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 12회차. 5연속대폭유출지속 | 유동성$82,841.32(-4.4%), h24-96.41%(추가악화) | 지속(10회차)·5연속유출악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 11회차. ⭐9연속유입종료가단발성확인 | 유동성$199,288.33(+7.9%), h24+23.13%(대폭감속) | 지속(9회차)·유입재개 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 17회차. h24추가악화(-91.04%) | 유동성$48,590.34(-0.7%), h24-91.04%(추가악화) | 지속(15회차)·붕괴지속최상위경계 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 16회차. 유출재개,h24추가악화 | 유동성$20,527.52(-6.9%), h24-83.66%(추가악화) | 지속(14회차)·여전히거의완전붕괴권 | 🔴 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 46회차. 지그재그미재현,h24가속 | 유동성$420,371.98(+1.8%), h24+163%(가속) | 지속(44회차)·지그재그미재현 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 168회차. ⚠️4연속개선후첫반전 | 유동성$285,339.97(-4.9%), h24+61.66%(감속) | 지속(166회차)·4연속개선후첫반전 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 144회차. ⚠️2연속유출확인 | 유동성$174,714.50(-6.9%), h24+18.45%(감속) | 지속(142회차)·2연속유출확인 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 47회차. 유사수준으로안정 | 유동성$508,831.17(+0.2%), h24+10.47%(유사) | 지속(45회차)·안정유지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 135회차. 안정유지 | 유동성$33,827.10(-1.3%), h24+5.97%(유사) | 지속(133회차)·대체로안정적 | 🟢 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 182회차. 안정적개선지속 | 유동성$364,197.85(-2.1%), h24+18.15%(유사) | 지속(180회차)·안정적개선지속 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 173회차. 유출반전,악화 | 유동성$99,369.74(-6.4%), h24-29.27%(악화) | 지속(171회차)·연속whipsaw이력상단정금지 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 173회차. ⚠️3회차연속지그재그 | 유동성$61,123.66(-4.4%), h24-0.91%(재음전) | 지속(171회차)·3회차연속지그재그 | 🟡 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 131회차. 지그재그미재현,강한재양전 | 유동성$83,886.16(+14.0%), h24+66.21%(대폭가속) | 지속(129회차)·지그재그미재현 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 181회차. h6재양전,h24개선 | 유동성$377,888.2(+1.3%), h24-19.47%(개선) | 지속(179회차)·혼조지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 185회차. 지그재그미재현,대폭가속 | 유동성$1,387,341.23(+4.8%), h24+36.97%(가속) | 지속(183회차)·지그재그미재현2연속개선 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 133회차. h24대폭반전양전 | 유동성$62,494.28(-10.7%), h24+34.86%(대폭반전) | 지속(131회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 62회차. 거의동일수준 | 유동성$229,391.60(-3.7%), h24+6.52%(거의동일) | 지속(60회차)·혼조지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 26회차. 유출,h6재음전,악화 | 유동성$47,548.59(-7.1%), h24-24.12%(악화) | 지속(24회차)·연속whipsaw단정금지 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 105회차달성. h24개선,h6재음전 | 유동성$1,669,410.76(-0.5%), h24-14.51%(개선) | 지속(103회차)·장기whipsaw이력 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 33회차(dogwifpants). h24추가악화 | 유동성$83,723.10(-10.3%), h24-58.56%(추가악화) | 지속(31회차)·h24추가악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 20회차. h24대폭악화재반전 | 유동성$8,865.23(-12.2%), h24-53.29%(대폭악화) | 지속(18회차)·h24대폭악화재반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 18회차. h24추가악화,깊은음전 | 유동성$22,904.85(-7.8%), h24-54.27%(추가악화) | 지속(16회차)·극단변동지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 19회차. h24소폭개선 | 유동성$232,900.92(-0.9%), h24-13.2%(개선) | 지속(17회차)·whipsaw패턴단정금지 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. **핵심 이벤트**: OBS·KIRK가 상향 직후 나란히 첫 반전(둘 다 🟢 유지, 다음 회차 분기점). CLUG는 h24 3연속악화+유동성2연속유출로 🟡→🔴 **하향**. JUGGERNAUT(4연속개선후첫반전)·BRODIE(2연속유출확인)도 함께 주시. **지그재그 패턴 재검증**: HOOKR·CALLOOOR·FWA는 이번엔 재반전 대신 직전 방향 유지(패턴 미재현), lickingcat만 3회차 연속 재반전. **CSV 결함 정정**: Doge2 누락(43→44행) 수정.

## 온체인 신호 상세

- **OBS·KIRK 첫 반전 상세**: 상단 주요사건 섹션 참조. OBS는 GT 로빈후드체인 트렌딩(reserve$43,412, h24+58.92%)으로 독립 교차확인해 진짜 반전임을 확인 · 2026-08-24T17:00:00Z
- **CLUG 하향 상세**: h24 -21.55%→-38.06%→-45.75% 3연속악화, 유동성 -3.0%→-6.4% 2연속유출. 3연속 기준(OBS 상향 근거와 동일)을 대칭 적용 · 2026-08-24T17:00:00Z
- **BRODIE 배치조회 오류 정정 상세**: 배치조회에서 pairAddress 0x46BF126A...(유동성$36,701)가 잘못 매칭돼, token-pairs 개별조회로 올바른 주풀 0x9870C395...(유동성$174,714.50)를 재확인. 5개 pair 전량 나열해 최대 유동성 풀임을 확인 · 2026-08-24T17:00:00Z
- **40M pairAddress 재검증 상세**: 과거 CLUG와 혼동됐던 pairAddress(Ct6arp861CvmvsAZ4pse7ZyTS2dDexfz9Yv2G6ajeU5q)가 이번 회차 40M 조회에서도 반환돼, pairs 직접조회(1회는 null 응답) + token-pairs 목록 교차조회로 baseToken.address가 40M(ELbFy4v8...)과 정확히 일치함을 재확인. 진짜 40M 소유 pair였음이 확정됨 · 2026-08-24T17:00:00Z
- **BULLSHIT 풀선택 재검증 상세**: 최대 유동성 풀은 Meteora($352,700)이나 회전율(volume/liquidity)이 PumpSwap 5.8배 vs Meteora 1.05배로 PumpSwap이 압도적으로 높아 기존 관례대로 PumpSwap 유지 · 2026-08-24T17:00:00Z
- **지그재그 4종목 재검증 상세**: 상단 "그 밖 특기 사항" 참조. HOOKR·CALLOOOR·FWA는 이번회차 재반전 없이 직전 방향 지속, lickingcat만 3회차연속 재반전 · 2026-08-24T17:00:00Z
- **TRUTH 이상거래량 상세**: h24 -91.04%인데 volume.h24 $14,752,844로 유동성($48,590) 대비 약 303배 회전율 — 통계적 신뢰도 매우 낮은 이상치, 방향(추가악화)만 참고 · 2026-08-24T17:00:00Z
- **나머지 상세**: PEPECOIN 혼조지속. MAPLE h1악화h24유사. CLOCKIN 유입지속h1재음전. TIPANSEM whipsaw유사수준. LIZARD h1h6악화h24개선. 1B h1악화h24가속. FLUSH 6연속악화. PEE 유사혼조. 40M h24 2연속양전. MANEKI 대폭악화. CYBERCAT 4연속유출심화. omo h24개선. swappy 2연속개선. CYBERLEEK 재음전반전. CC h24대폭감속. Z500 유사악화. CONK 소폭개선. CHUMP 혼조전환. CATALORIAN 5연속유출. PROLOGUE 유입재개. Dinger 추가악화h6개선. HOOKR 가속. CATE h24개선h6재음전. GOOD 안정. PRINTER 안정적개선. Dealer 악화. lickingcat 3연속지그재그. CALLOOOR 대폭가속. TOAD 개선. FWA 대폭가속. DPG h24대폭반전. BULLSHIT 거의동일. JUGGERNAUT 첫반전. BRODIE 2연속유출. PITCOIN 안정. PANTS 추가악화. Doge2 악화. Truth Coin h24대폭악화재반전. BARRON 소폭개선. YOMOGI 추가악화 · 2026-08-24T17:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 40종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 재확인과 배치조회 오류 정정(BRODIE·40M)에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-24 15:00Z)로부터 정확히 **2시간** 경과(정시 슬롯 정상 진행).
- **DexScreener 배치조회 안정성 저하**: 이번 회차는 여러 배치조회(3~5개 묶음)에서 `pairs:null`(전 조회 실패) 응답이 다수 발생해 개별·소규모 재조회로 전환했다. 성공한 조회 중에서도 **BRODIE**는 소형 풀이 잘못 매칭되는 오류가 재발해 token-pairs 개별조회로 정정했다. 배치조회 신뢰도가 이번 회차 특히 낮았다.
- **40M pairAddress 재검증**: 과거 CLUG와 혼동됐던 pairAddress가 다시 반환됐으나, pair 직접조회 + token-pairs 목록조회 이중 교차검증으로 이번엔 실제로 40M 소유의 정상 pair였음을 확인했다. 우연히 같은 접두어를 가진 것이 아니라 baseToken.address가 완전 일치했다.
- **상향 직후 반전 2건(OBS·KIRK) 동시 발생**: 우연히 같은 회차에 발생했으나, 최근 확립한 "상향은 3연속 이상 확인 후, 첫 반전은 단정하지 않고 색상 유지" 원칙이 정확히 시험대에 올랐다. 다음 회차 결과가 중요하다.
- **CLUG 하향은 3연속 기준의 대칭 적용 사례**: 상향에 쓰인 기준(3연속 개선)을 하향에도 똑같이 적용한 첫 사례로 기록한다.
- **CSV 결함 정정**: 기존 CSV에서 Doge2가 누락돼 있던 것(43행)을 이번 회차 44행으로 정정했다. JSON·MD는 이전부터 정상적으로 44개를 포함하고 있었다.
- **데이터 신뢰도**: DexScreener 배치조회의 불안정성이 이번 회차 두드러졌으나, 개별·token-pairs 조회와 GeckoTerminal 교차검증(OBS·CYBERCAT·CATALORIAN·CYBERLEEK·CC·HOOKR·JUGGERNAUT·CHUMP·MANEKI·CATE·PANTS 등 다수)으로 방향성 일치를 대부분 확인했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
