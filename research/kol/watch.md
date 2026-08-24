# 온체인 트렌딩 조기경보 — 2026-08-24 19:10 UTC (KST 2026-08-25 04:10)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전(2026-08-24 17:00Z)로부터 **2시간 10분** 경과했다(트리거가 다소 밀림, 정직 표기).

> 44개 활성종목 전부를 DexScreener 토큰 API로 재확인했다. 이번 회차도 여러 배치조회(2~5개 묶음)에서 `pairs:null`(전 조회 실패) 응답이 다수 발생해 개별 재조회로 정정했다. **Dinger는 DexScreener 배치·개별조회가 모두 전량 실패**해 GeckoTerminal 직접 풀 조회(CA기준)로 대체 확인했다 — 마침 같은 시점 GT 솔라나 트렌딩에 동명이인의 **별개 'Dinger' 풀**(CA 7fmHqRpJ…, 로빈후드체인이 아닌 솔라나의 오래된 풀)이 노출돼, 두 주소를 혼동하지 않도록 baseToken 주소를 대조해 교차검증했다(정상 분리 확인, notable "Dinger(구형·별개CA)" 항목).

> **⚠️ 이번 회차 핵심 발견 — OBS·KIRK, "첫 반전"이 노이즈였을 가능성이 짙어짐**: 직전(17:00Z) 회차에서 나란히 첫 반전(감속·재음전)을 보였던 OBS·KIRK가 이번 회차 모두 개선 방향으로 되돌아왔다. OBS는 h24가 131%→59.21%→123%로 **반전의 반전**을 보였고(GT 교차확인도 동일방향), KIRK는 유동성 유입 재개+h6 재양전으로 회복 조짐이 뚜렷하다. 지난 회차 경고한 "2회차 연속 반전이면 하향 근거"는 성립하지 않았다 — 오히려 반전이 단발 노이즈였을 가능성이 커졌다. 둘 다 🟢 유지.

> **CLUG, 하향 직후 첫 반전 신호 — 대칭 원칙 적용, 판정 유지**: 지난 회차 "3연속 h24악화+2연속유동성유출"로 🔴 하향한 CLUG가 이번 회차 유동성 유입 반전(+3.7%)과 h24 대폭 개선(-45.75%→-29.74%)을 보였다. OBS/KIRK에 적용한 "단발 신호로 판정 뒤집지 않기" 원칙을 대칭 적용해, CLUG도 이번 1회차 개선만으로는 🔴 판정을 되돌리지 않는다. 다음 회차에도 개선이 이어지면 재검토 대상이다.

## 🚨 주요 사건 — CATE, 역대 최대급 반전(유동성 +27.2%, h24 -14.51%→+60.19%)

장기 whipsaw 이력(106회차)의 CATE가 이번 회차 유동성 $1,669,410.76→$2,123,295.63(+27.2%, 대폭유입), h6 -0.83%→+50.82%, h24 -14.51%→+60.19%로 역대 최대급 반전을 보였다. **GeckoTerminal 독립 직접 풀 조회로 2회 교차확인**(reserve $2,162,967~2,165,486, h6 +58.6~58.7%, h24 +68.0~68.1%)해 DexScreener 오류가 아닌 진짜 반전임을 확인했다. 다만 106회차 장기 whipsaw 이력상 방향 확정은 시기상조라 🟡를 유지한다.

## 🚨 주요 사건 — CATCUS(notable), 4연속 유입 직후 급붕괴(러그 의심)

지난 3개 회차 연속 편입 후보로 근접 중이던 CATCUS(notable)가 이번 회차 유동성 $45,858.54→$3,514.96(**-92.3%**), h1 -98.89%, h6 -98.46%, h24 -93.68%로 급붕괴했다. 4연속 유입 확인 직후 급전직하한 패턴은 P400·HEREBRO 등 "풀 나이 1일 미만 극조기 관측" 사례들이 결국 러그·펌프덤프로 귀결됐던 것과 동일하다. tokens 편입을 계속 보류한 판단이 옳았음을 확인하는 사례로 기록한다.

## 그 밖 특기 사항

- **BRODIE, 2연속유출이 유입재개로 반전**: 지난 회차 "140회차만에 첫유출조짐이 2연속으로 확인"돼 다음 회차가 분기점이라 표시했는데, 이번 회차 유동성 +9.0%로 유입 재개, h1·h6 모두 재양전, h24 가속(+32.26%)으로 완전 반전됐다. 2연속 유출이 노이즈였을 가능성이 크다. 🟢 유지.
- **swappy, 2연속개선 streak 중단**: 상향 검토 대상으로 주시하던 swappy가 이번 회차 유동성 -9.0% 유출반전, h1·h6·h24 모두 재음전으로 개선 흐름이 끊겼다. 🟡 유지, 상향 보류.
- **CALLOOOR·HOOKR, 2연속 개선으로 상향 후보권 진입**: CALLOOOR(유동성 2연속 유입, h1+27.49%·h6+63.27% 대폭가속)과 HOOKR(유동성 2연속 유입가속, h24+163%→+236%)가 나란히 2연속 개선을 확인했다. 3연속 확인 시 상향 검토 대상.
- **FWA, 3연속 유입에도 지표 혼조로 상향 보류**: 유동성은 3회 연속 유입(+4.8%→+3.6%)했으나 h1·h24는 감속, h6는 가속하는 혼조 신호라 이번 회차는 상향하지 않는다.
- **CASHCAT(notable), 2연속 확인**: 지난 회차 "38회차만에 첫유출이 단발성" 확인에 이어 이번 회차도 h24 가속(+46.44%→+62.806%)이 이어져 유입 재개 추세가 2연속 확인됐다.
- **PROLOGUE, 2연속 유입재개 확인**: 직전 "9연속유입종료가 단발성" 판단이 이번 회차도 유입 지속(+5.7%)·h24 대폭가속(+70.79%)으로 2연속 확인됐다.
- **CATALORIAN, 6연속 대폭유출로 거의 완전소멸 근접**: 유동성 -38.0%(6연속유출), h1 -64.44%로 급락, h24 -97.75%. GT도 완전수렴 확인.
- **lickingcat, 4회차 연속 지그재그**: whipsaw 패턴이 가장 뚜렷한 종목으로 유지.
- **YOMOGI, 장기 유출흐름 속 첫 유동성 반전(+13.7%)**: h24는 여전히 악화(-58.98%)이나 유동성 반전은 주목할 신호.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 34회차. 반전의반전,재가속 | 유동성$114,137.51(-1.7%), h24+123%(대폭재가속) | 지속(33회차)·반전의반전 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 42회차. 혼조지속,h1개선 | 유동성$18,634.24(-2.8%), h24-20.84%(유사) | 지속(41회차)·혼조지속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 28회차. 유입반전,h1재양전 | 유동성$29,764.83(+9.4%), h24+45.31%(가속) | 지속(27회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 52회차. 유출전환,유사수준 | 유동성$223,285.01(-4.1%), h24+13.38%(유사) | 지속(51회차)·52회차째whipsaw | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 40회차. whipsaw지속,h6개선 | 유동성$13,992.8(+2.3%), h24-22.43%(유사) | 지속(39회차)·whipsaw지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 23회차. 유입반전,h1재양전 | 유동성$35,676.57(+4.7%), h24-5.14%(개선) | 지속(22회차)·연속whipsaw | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 32회차. h1재양전,h24감속 | 유동성$25,482.67(-6.7%), h24+23.69%(대폭감속) | 지속(31회차)·연속급반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 64회차. ⚠️하향후첫반전(판정유지) | 유동성$33,779.82(+3.7%), h24-29.74%(대폭개선) | 지속(63회차)·하향유지 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 30회차. ⭐7연속유출,가격지표는개선 | 유동성$22,121.36(-5.7%), h24-35.16%(개선) | 지속(29회차)·7연속유출 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 69회차. 유사,h24개선 | 유동성$7,243.78(-0.6%), h24+8.63%(개선) | 지속(68회차)·정체 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 27회차. 대폭유출,양전패턴종료 | 유동성$11,161.03(-14.0%), h24+0.47%(대폭감속) | 지속(26회차)·대폭유출 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 16회차. 15회차째whipsaw,대폭악화 | 유동성$34,038.93(-19.1%), h24-55.28%(대폭악화) | 지속(14회차)·whipsaw15회차 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 13회차. 정점통과,5연속유출 | 유동성$20,488.79(-15.7%), h24-87.31%(유사) | 지속(12회차)·5연속유출심화 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 16회차. 유입반전,개선지속 | 유동성$111,492.87(+6.4%), h24-21.16%(개선) | 지속(15회차)·개선지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 45회차. ⚠️2연속개선streak중단 | 유동성$196,571.15(-9.0%), h24-2.93%(재음전반전) | 지속(44회차)·streak중단 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 44회차. 유입반전,h24재양전 | 유동성$1,744,833.66(+2.7%), h24+8.15%(재양전) | 지속(43회차)·연속whipsaw | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 42회차째방향번복. h24대폭감속 | 유동성$272,015.64(-7.6%), h24-0.64%(재음전근접) | 지속(41회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 35회차. 유사,h24대폭개선 | 유동성$78,999.68(+1.1%), h24-2.00%(대폭개선) | 지속(34회차)·이번회차개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 32회차. ⭐회복조짐확인 | 유동성$74,472.68(+3.0%), h24-3.5%(개선) | 지속(31회차)·회복조짐확인 | 🟢 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 29회차. 유출반전,h24추가악화 | 유동성$55,575.7(-4.9%), h24-63.74%(추가악화) | 지속(28회차)·유출반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 20회차. h1h6개선,h24재음전 | 유동성$317,555.54(-2.0%), h24-3.11%(재음전) | 지속(18회차)·혼조전환 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 13회차. ⚠️6연속유출,거의완전소멸 | 유동성$51,339.98(-38.0%), h24-97.75%(추가악화) | 지속(11회차)·6연속유출악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 12회차. ⭐2연속유입재개확인 | 유동성$210,579.26(+5.7%), h24+70.79%(대폭가속) | 지속(10회차)·2연속유입재개 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 18회차. h24추가악화(-96.87%) | 유동성$48,224.71(-0.7%), h24-96.87%(추가악화) | 지속(16회차)·붕괴지속최상위경계 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 17회차. GT대체확인,대폭개선 | 유동성$23,639.26(+15.2%,GT), h24-52.31%(대폭개선) | 지속(15회차)·개선 | 🔴 | [GeckoTerminal](https://www.geckoterminal.com/solana/pools/CwBoViDDJjpMwvahCKLyr5wXs3XqxBz8fKDLKKyFek2V) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 47회차. ⭐2연속개선 | 유동성$462,802.36(+10.1%), h24+236%(대폭가속) | 지속(45회차)·2연속개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 169회차. 첫반전후안정화양상 | 유동성$280,474.03(-1.7%), h24+57.09%(유사) | 지속(167회차)·안정화양상 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 145회차. ⭐2연속유출이유입반전 | 유동성$190,430.01(+9.0%), h24+32.26%(가속) | 지속(143회차)·유입재개로반전 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 48회차. 유입,h6h24가속 | 유동성$553,942.83(+8.9%), h24+21.01%(가속) | 지속(46회차)·개선방향 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 136회차. 안정유지,가속 | 유동성$34,138(+0.9%), h24+11.86%(가속) | 지속(134회차)·대체로안정적 | 🟢 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 183회차. 안정적개선지속 | 유동성$366,865.26(+0.7%), h24+23.6%(가속) | 지속(181회차)·안정적개선지속 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 174회차. 유출지속,악화 | 유동성$89,987.21(-9.4%), h24-38.77%(추가악화) | 지속(172회차)·연속whipsaw이력상단정금지 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 174회차. ⚠️4회차연속지그재그 | 유동성$57,599.44(-5.8%), h24+0.94%(재양전) | 지속(172회차)·4회차연속지그재그 | 🟡 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 132회차. ⭐2연속유입,대폭가속 | 유동성$89,586.66(+6.8%), h24+70.64%(가속) | 지속(130회차)·2연속유입 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 182회차. 유사,h24개선 | 유동성$379,974.73(+0.6%), h24-8.38%(개선) | 지속(180회차)·혼조지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 186회차. 3연속유입,지표혼조 | 유동성$1,436,910.58(+3.6%), h24+25.41%(감속) | 지속(184회차)·3연속유입혼조 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 134회차. 안정화,반전거의소멸 | 유동성$62,627.89(+0.2%), h24+3.42%(대폭감속) | 지속(132회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 63회차. 1회차악화신호 | 유동성$219,495.05(-4.3%), h24-25.48%(재음전반전) | 지속(61회차)·1회차악화신호 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 27회차. 안정화,h1h24악화 | 유동성$47,740.5(+0.4%), h24-32.6%(악화) | 지속(25회차)·연속whipsaw단정금지 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 106회차달성. ⭐역대최대급반전 | 유동성$2,123,295.63(+27.2%), h24+60.19%(대폭반전) | 지속(104회차)·역대최대급변동 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 34회차(dogwifpants). 유입반전 | 유동성$85,474.69(+2.1%), h24-54.51%(개선) | 지속(32회차)·유입반전소폭개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 21회차. h24개선,h6악화혼조 | 유동성$8,735.95(-1.5%), h24-34.98%(개선) | 지속(19회차)·h24개선h6악화혼조 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 20회차. 유출반전,h6재음전 | 유동성$226,971.46(-2.5%), h24-14.18%(유사) | 지속(18회차)·유출반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 19회차. ⭐유동성첫반전(장기유출후) | 유동성$26,048.64(+13.7%), h24-58.98%(유사) | 지속(17회차)·유동성반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. 활성목록 **44→44종**(순증감 0). notable **41→41개**(신규 없음, CATCUS 급붕괴 등 기존 항목 데이터 갱신). **핵심 이벤트**: OBS·KIRK가 첫 반전을 뒤집고 개선방향 재개(둘 다 🟢 유지), CLUG는 하향 직후 첫 반전 신호에도 대칭 원칙 적용해 🔴 판정 유지. CATE 역대최대급 반전(GT 교차확인). CATCUS(notable) 4연속유입 직후 급붕괴 — 러그 의심 사례로 기록.

## 온체인 신호 상세

- **OBS·KIRK 반전의 반전 상세**: 상단 주요사건 섹션 참조. OBS는 GT 로빈후드체인 트렌딩·직접풀조회 2경로로 h24+91.9~97.9%를 확인해 DS의 +123%와 방향 일치. KIRK는 유동성+3.0%·h6+3.93%로 회복조짐 · 2026-08-24T19:10:00Z
- **CLUG 대칭원칙 적용 상세**: 지난 회차 3연속 h24악화 기준으로 하향했는데, 이번 회차 h24-45.75%→-29.74%(대폭개선)·유동성+3.7%(유입반전)이 나왔으나 단1회차라 판정 유지. 다음 회차 개선 지속 시 재검토 · 2026-08-24T19:10:00Z
- **CATE 역대최대급반전 상세**: DS 유동성+27.2%·h24+60.19%를 GT 독립 직접 풀 조회(2회, pool HMzvsEEmtzHhvZNw9uwbaG85HCTmFnkbhzUx16cy7ca3)로 교차확인, reserve $2,162,967~2,165,486·h24+68.0~68.1%로 방향·규모 모두 일치 · 2026-08-24T19:10:00Z
- **CATCUS(notable) 급붕괴 상세**: 유동성 $45,858.54→$3,514.96(-92.3%), h1-98.89%·h6-98.46%·h24-93.68%. 4연속유입 직후 발생, P400·HEREBRO와 동일한 "극조기 관측→급붕괴" 패턴 · 2026-08-24T19:10:00Z
- **Dinger DS 전량실패 및 GT 대체확인 상세**: DexScreener가 배치·개별조회 모두 `pairs:null` 반환해 GeckoTerminal 직접 풀 API(`/networks/solana/tokens/{CA}/pools`)로 대체, pumpswap 풀(CwBoViDDJjpMwvahCKLyr5wXs3XqxBz8fKDLKKyFek2V) reserve $23,639.26 확인. 같은 시점 GT 솔라나 트렌딩에 baseToken 주소가 다른 별개 'Dinger' 풀(7fmHqRpJ…)이 노출돼 혼동 방지를 위해 주소 대조 · 2026-08-24T19:10:00Z
- **BULLSHIT 풀선택 재검증 상세**: PumpSwap(유동성$219,495.05,volume$1,095,559.47,회전율4.99배) vs Meteora(유동성$350,241.35,volume$318,268.47,회전율0.91배) — PumpSwap 회전율 압도적 우위 유지, 기존 관례대로 PumpSwap 유지 · 2026-08-24T19:10:00Z
- **CC 풀선택 재검증 상세**: PumpSwap(유동성$272,015.64,volume$3,293,500.19,회전율12.1배) vs Meteora(유동성$288,665.61,volume$866,251.86,회전율3.0배) — 유동성은 Meteora가 근소 우위이나 회전율은 PumpSwap이 압도적, 기존 관례대로 PumpSwap 유지 · 2026-08-24T19:10:00Z
- **PANTS 풀선택 재검증 상세**: PumpSwap(유동성$85,474.69,volume$641,901.97,회전율7.51배) vs Meteora(유동성$70,320.97,volume$19,967.34,회전율0.28배) — PumpSwap 회전율 압도적 우위 유지 · 2026-08-24T19:10:00Z
- **CVXV666·DOPAMEME·Morty·Polycat·LOOKSMAX(notable) 동반 반전 상세**: 이번 회차 GT 솔라나 트렌딩 재확인에서 5종목 모두 유동성 유출반전 또는 대폭감속을 보였다(CVXV666 -20.1%, DOPAMEME -17.4%, Morty -0.8%, Polycat -17.8%, LOOKSMAX -4.3%·h24 재음전반전). 8/13~8/18 사이 풀 생성된 '2주 내외' 토큰군이 동시에 식는 패턴 · 2026-08-24T19:10:00Z
- **나머지 상세**: PEPECOIN 혼조지속. MAPLE 유입반전. CLOCKIN 유출전환. TIPANSEM whipsaw지속. LIZARD 유입반전. 1B h24감속. FLUSH 7연속유출가격지표개선. PEE 개선. 40M 대폭유출. MANEKI 대폭악화. CYBERCAT 5연속유출. omo 유입반전개선. swappy streak중단. CYBERLEEK 유입반전h24재양전. CONK 유출반전. CHUMP 혼조전환. CATALORIAN 6연속유출거의완전소멸. TRUTH 추가악화. HOOKR 2연속개선. JUGGERNAUT 안정화. GOOD 유입가속. PRINTER 안정적개선. Dealer 추가악화. lickingcat 4연속지그재그. CALLOOOR 2연속유입. TOAD 개선. FWA 3연속유입혼조. DPG 반전거의소멸. JUGGERNAUT안정화. BRODIE 유입재개. PITCOIN 가속. PANTS 유입반전. Doge2 악화. Truth Coin 혼조. BARRON 유출반전. YOMOGI 유동성첫반전 · 2026-08-24T19:10:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 40종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 재확인과 Dinger의 DS 전량실패→GT 대체확인, CATE 역대최대급반전 교차검증, CATCUS 급붕괴 확인에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-24 17:00Z)로부터 **2시간 10분** 경과(트리거가 다소 밀림, 정직 표기).
- **DexScreener 배치조회 불안정 지속**: 이번 회차도 여러 배치조회에서 `pairs:null` 응답이 발생해 개별 재조회로 전환했다. **Dinger는 개별조회까지 전량 실패**해 GeckoTerminal로 대체했다 — 이는 결함이 아니라 소스 다변화로 대응한 정상 절차다.
- **동일 pairAddress 재등장 오매칭 없음**: 이번 회차 응답에서 서로 다른 두 요청 토큰이 동일한 pairAddress·동일 수치를 반환한 사례는 없었다. 다만 CLUG·40M·BRODIE 등 과거 혼동 이력이 있는 토큰은 baseToken 주소를 매 회차 재대조하는 절차를 유지했다.
- **CATCUS 급붕괴는 "조기 편입 보류"가 실제로 리스크를 걸러낸 사례**: 4연속 유입에도 풀 나이가 짧다는 이유로 tokens 편입을 계속 보류했는데, 이번 회차 -92.3% 급붕괴로 그 보수적 판단이 정당했음이 확인됐다.
- **데이터 신뢰도**: DexScreener 개별·token-pairs 조회와 GeckoTerminal 교차검증(OBS·CYBERCAT·CATALORIAN·CYBERLEEK·CC·HOOKR·JUGGERNAUT·PANTS·CATE·Dinger 등 다수)으로 방향성 일치를 대부분 확인했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
