# 온체인 트렌딩 조기경보 — 2026-08-24 03:00 UTC (KST 2026-08-24 12:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-24 01:00Z)로부터 정확히 2시간 경과**(정상 간격). 44개 활성종목 전부를 DexScreener 토큰 API(5개 이하 소규모 배치조회, 총 12회 요청 — 9개 배치 + 누락분 3건 개별재조회)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 API로 TRUTH·CASHCAT·CLOCKIN 등 교차검증 및 신규 발굴 스캔을 진행했다.

> **배치조회 검증 결과**: 요청한 44개 토큰 전부 최종적으로 데이터를 확보했다. 다만 과정에서 **두 배치에서 요청 대상 토큰 일부가 누락**됐다 — ①1B 단일요청 시 최대유동성 풀 오선정(다른 풀 $340.16을 잘못 반환)이 있어 개별 재조회로 $30,717.52 정정, ②HOOKR·CATE·GOOD·PRINTER·BULLSHIT 배치에서 HOOKR이 응답에서 누락되고 존재하지 않는 데이터가 섞여 나와 개별 재조회 예정으로 별도 배치에서 재확보, ③PITCOIN이 BRODIE·Dealer·lickingcat·PITCOIN·PANTS 5개 요청 배치에서 완전히 누락(대신 요청하지 않은 Z·CATE 항목이 섞여 나옴)돼 개별 재조회로 확보. **5개 이하 배치조회에서도 부분 누락·오선정·환각(요청하지 않은 토큰 삽입)이 발생할 수 있음을 재확인**했고, 이번 회차는 전 건을 개별 재조회로 보완해 최종 데이터 누락은 없다.

> **편입/편출/강등 내역**: **신규편입 0건**(GT 솔라나 트렌딩에서 Polycat·DOPAMEME·LUIGI 3종 신규 발굴, 전부 이미 상당폭 상승·풀나이 과소 또는 h1/h24 이미 반전 조짐으로 notable에만 기록). **편출 0건**. 활성목록 **44→44종**(순증감 0). notable **35→39개**(Polycat·DOPAMEME·LUIGI 3종 신규 + Chud는 이번 회차 미채택).

## 🚨 최우선 후속 — TRUTH 유동성 3연속 회복 (여전히 극단 손실권)

직전 회차(01:00Z) 유동성이 $57,154.22로 부분 회복했던 TRUTH가, 이번 회차 **$76,580.78로 3연속 회복**(+34.0%)했다. 21:20Z 고점($223,452) 대비로는 **-65.7%**까지 축소됐으나 여전히 극단적 손실권이고, h6 -92.59%·h24 -96.48%로 여전히 거의 완전 붕괴 수준을 유지 중이다. h1은 -1.9%로 근접 횡보(직전 -0.67%와 유사).

| 시점 | 유동성 | h1 | h6 | h24 |
|---|---|---|---|---|
| 21:20Z(부모, 크래시전) | $223,452 | -4.44% | +722% | -52.69% |
| 23:00Z(직전-2회, 대붕괴) | $34,673.24 | -75.29% | -93.25% | -98.86% |
| 01:00Z(직전, 1차회복) | $57,154.22 | -0.67% | -92.47% | -97.24% |
| **03:00Z(이번 회차, 2차회복)** | **$76,580.78** | **-1.9%** | **-92.59%** | **-96.48%** |

GeckoTerminal 재확인(로빈후드체인 트렌딩10위, pool `0x256c0e2c8bf49b74c175848f6392437c428d39cb`): reserve $63,526, h1 -24.08%·h6 -96.09%·h24 -97.76%로 DS와 h6·h24는 거의 일치한다. **⚠️h1은 직전 회차에 이어 이번에도 부호·크기가 모두 크게 상이**(GT -24.08% vs DS -1.9%)해 순간 스냅샷 시점 차이로 추정되며, 다음 회차도 재확인이 필요하다. **자연스러운 가격급락에 따른 유동성 감소인지, 실제 유동성 인출(럭풀)인지는 여전히 판별 불가** — 3연속 회복이 관측되긴 했으나 규모가 여전히 극단적이라 최상위 경계를 유지한다.

## 그 밖 특기 사항

- **CYBERCAT(6회차)**: 4연속 개선streak 제동이 이번 회차 2회차째 심화됐다 — 유동성 유출 -16.6%로 가속, h6도 재음전. '정점통과' 패턴이 사실상 확정적이라 리스크를 🟡→🔴로 재상향한다.
- **CC(35회차)**: 34회차째 이어지던 방향번복이 이번 회차 대폭 재양전(+25.9% 유입, h6 +39.81%, h24 +111%)으로 다시 뒤집혔다. 워시트레이딩 의심은 불변.
- **JUGGERNAUT(162회차)**: 161회차부터 3회차째 유지되던 상승반전 흐름에 처음 균열이 갔다 — 유동성 유출 -12.1%, h6 재음전. 리스크를 🟢→🟡로 하향한다.
- **YOMOGI(12회차)**: 직전 회차 '안정화 조짐'이 이번 회차 h24 +241%→-89.1%로 대폭 반전됐다. 24h 베이스효과(초기 급등이 24시간 창에서 빠져나가는 롤오프)로 추정되며, 실제 추세반전으로 단정하지 않는다.
- **Doge2(20회차)**: h24가 +127%→+55.95%로 큰 폭 감속했다. 이 역시 24h 롤오프 아티팩트 가능성이 있어 신중하게 표기한다.
- **CLOCKIN(45회차)**: 2회차째 지속되던 강화streak 제동이 이번 회차 뚜렷한 유입반전(+12.0%)으로 전환됐다. 아직 1회차라 확정은 이르다.
- **PROLOGUE(5회차)**: 5회차 연속 완만한 개선이 지속돼 리스크를 🟡→🟢로 하향한다.
- **FLUSH(23회차)**: 3회연속 대폭 유입(+15.0%)이 이어지며 h24가 처음으로 플러스 전환(+2.6%)됐다. 리스크를 🟡→🟢로 하향하되, h6 +160% 급등은 저유동 노이즈 가능성이 있어 신중히 본다.
- **omo(9회차)**: 4연속 유출 종료 후 2회차째 전지표 개선이 이어지고 있다. 
- **GOOD(41회차)**: 장기 강화흐름에 처음 냉각조짐(유출전환 -5.1%, h6 재음전)이 나타나 리스크를 🟢→🟡로 하향한다.
- **PANTS(27회차)**: 악화심화 흐름이 일단 멈추고 유동성 유출이 -0.6%로 거의 정체됐다(직전 -12.8%). h1도 재양전. 여전히 h24 -54.65%로 깊은 음전이라 🔴 유지하되 안정화 조짐을 기록한다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 27회차. 개선반전이1회만에다시번복 | 유동성$90,880.95(+0.5%), h24+6.67%(대폭감속) | 지속(27회차)·재번복 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 35회차. h1대폭감속,h24가속혼조 | 유동성$21,533.91(-1.1%), h24+23.18% | 지속(35회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 21회차. h1완화,h6재음전혼조 | 유동성$28,510.75(+1.6%), h24+37.53% | 지속(21회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 45회차. 2회제동이유입반전전환 | 유동성$226,723.88(+12.0%), h24+63.33% | 지속(45회차)·유입반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 33회차. 전지표개선,h6재양전 | 유동성$16,118.75(+9.7%), h24+34.04% | 지속(33회차)·전방위개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 16회차. h1재양전,유출h6재음전혼조 | 유동성$33,364.98(-6.4%), h24-33.5% | 지속(16회차)·혼조 | 🔴 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 25회차. 재악화조짐이h1재양전으로완화 | 유동성$30,717.52(-3.3%), h24+41.79% | 지속(25회차)·재양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 57회차. 5회whipsaw심화후소폭유입반전 | 유동성$38,507.59(+2.7%), h24+10.08%(손익분기이탈) | 지속(57회차)·유입반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 23회차. ⭐3연속유입,h24최초양전 | 유동성$33,630.84(+15.0%), h24+2.6%(최초양전) | 지속(23회차)·3연속개선 | 🟢(하향) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 62회차. 극저유동벗어나는조짐 | 유동성$7,322.12(+7.5%) | 지속(62회차)·변화조짐 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 20회차. 유입지속,20회차연속완만한개선 | 유동성$12,940.57(+0.9%), h24-27.27% | 지속(20회차)·완만한개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 9회차. 8회차째whipsaw,이번엔유입반전가속 | 유동성$62,674.20(+5.0%), h24+89.60% | 지속(9회차)·whipsaw8회차 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 6회차. ⚠️4연속개선streak제동2회차심화,정점통과확정 | 유동성$59,073.39(-16.6%), h24+819%(감속) | 지속(6회차)·정점통과확정 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 9회차. 2회연속개선지속 | 유동성$109,169.86(-0.5%), h24-27.73% | 지속(9회차)·2회연속개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 38회차. 유출이유입반전으로번복 | 유동성$211,658.59(+5.4%), h24-6.42% | 지속(38회차)·유입반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium) | 미확인 | 37회차. 유출지속,h6재음전이나h24가속 | 유동성$1,648,891.5(-7.2%), h24+102% | 지속(37회차)·모멘텀괴리 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 35회차째방향번복. ⭐대폭재양전 | 유동성$294,821.52(+25.9%), h24+111%(강한재양전) | 지속(35회차)·대폭재양전 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 28회차. 전방위악화흐름지속(h6도포함) | 유동성$70,521.28(-4.2%), h24-35.68% | 지속(28회차)·전방위악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 25회차. h1h6재음전,h24재양전혼조 | 유동성$77,731.05(-4.4%), h24+0.86% | 지속(25회차)·혼조 | 🟢 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 22회차. ⚠️재음전이1회만에또개선반전(연속whipsaw) | 유동성$74,621.91(-3.4%), h24-40.61%(대폭개선) | 지속(22회차)·연속whipsaw | 🔴 | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 13회차. ⭐냉각streak종료,유입반전 | 유동성$311,426.99(+7.6%), h24+48.85% | 지속(13회차)·냉각종료 | 🟡(하향) | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 6회차. 2회차째개선지속,h1대폭감속 | 유동성$358,643.11(+5.7%), h24+10473% | 지속(6회차)·2회연속개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 5회차. 5회차연속완만한개선지속 | 유동성$154,873.57(+6.3%), h24+27.9% | 지속(5회차)·5회연속개선 | 🟢(하향) | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 11회차. 9회차째대붕괴이후3연속회복 | 유동성$76,580.78(+34.0%), h24-96.48% | 지속(11회차)·3연속회복 | 🔴(최상위경계) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 40회차. 개선흐름3회차째유지·가속 | 유동성$321,891.81(+12.1%), h24+121% | 지속(40회차)·3연속가속 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 162회차. ⚠️3회차상승반전흐름첫균열 | 유동성$258,912.49(-12.1%), h24+25.64% | 지속(162회차)·첫균열 | 🟡(하향) | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 138회차. 냉각조짐완화2회차째지속 | 유동성$197,624.12(+4.7%), h24+26.44% | 지속(138회차)·2연속개선 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 41회차. ⚠️장기강화흐름첫냉각조짐 | 유동성$478,666.30(-5.1%), h24+7.35%(대폭감속) | 지속(41회차)·첫냉각 | 🟡(하향) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 129회차. 대체로안정적 | 유동성$31,780.77(-1.2%), h24-3.84% | 지속(129회차)·안정적 | 🟢 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 176회차. 유사수준유지,h24개선지속 | 유동성$367,262.78(-0.1%), h24+6.10% | 지속(176회차)·개선지속 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 167회차. ⚠️개선반전이1회만에다시악화번복 | 유동성$109,422.04(-3.7%), h24-25.92% | 지속(167회차)·재번복 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 167회차. 유출지속,h1개선h6h24감속 | 유동성$58,489.61(-4.1%), h24+3.32% | 지속(167회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 125회차. 전지표소폭개선지속 | 유동성$60,994.71(+1.0%), h24-10.76% | 지속(125회차)·소폭개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 175회차. 유입에서유출로전환,h1h6재음전 | 유동성$383,380.62(-5.2%), h24-10.27% | 지속(175회차)·유출전환 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 179회차. ⚠️유입반전이1회만에유출재전환 | 유동성$1,239,261.32(-6.6%), h24+18.94% | 지속(179회차)·유출재전환 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 127회차. h1재양전,h24개선지속 | 유동성$63,454.68(+1.5%), h24-52.39% | 지속(127회차)·개선지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap) | 미확인 | 56회차. 데이터이상해소이후유출지속 | 유동성$222,715.72(-3.9%), h24-24.94% | 지속(56회차)·유출지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 20회차. h1재양전,h24대폭감속(베이스효과가능) | 유동성$49,603.15(-1.7%), h24+55.95%(감속) | 지속(20회차)·h24감속 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 99회차. 유출재개2회차,h6h24는개선 | 유동성$1,552,631.73(-3.7%), h24-38.48%(대폭개선) | 지속(99회차)·유출혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **Dinger** | Solana(PumpSwap) | 미확인 | 10회차. ⚠️h24대폭반전(베이스효과추정) | 유동성$35,823.25(-9.0%), h24-32.02%(대폭반전) | 지속(10회차)·h24반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 13회차. whipsaw지속,h6개선 | 유동성$219,231.14(-2.5%), h24-40.06% | 지속(13회차)·whipsaw지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 27회차(dogwifpants). ⭐악화심화멈춤,안정화조짐 | 유동성$99,151.95(-0.6%), h24-54.65%(개선) | 지속(27회차)·안정화조짐 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 14회차. 유사수준안정화,h1h6재양전 | 유동성$10,922.97(+0.3%), h24-46.58% | 지속(14회차)·안정화 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 12회차. ⚠️안정화조짐이h24대폭반전으로번복 | 유동성$30,105.94(-8.1%), h24-89.1%(대폭반전) | 지속(12회차)·h24반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**(Polycat·DOPAMEME·LUIGI 3종은 notable에만 신규 기록). **편출 0건**. **최우선후속**: TRUTH 유동성 3연속 회복($34,673→$57,154→$76,580, 고점대비-65.7%로 축소되나 여전히 극단). **정점통과 확정**: CYBERCAT(4연속개선streak제동2회차심화, 🔴재상향). **첫 균열**: JUGGERNAUT(3회차상승반전흐름첫균열, 🟡하향), GOOD(장기강화흐름첫냉각, 🟡하향). **개선 하향(리스크완화)**: FLUSH(3연속개선,h24최초양전, 🟢), PROLOGUE(5회차연속개선, 🟢). **재번복 다수**: OBS·CONK·Dealer·FWA(1회 개선 후 즉시 재번복). **베이스효과 의심**: YOMOGI·Dinger·Doge2의 h24 극단 반전(24h 롤오프 아티팩트 가능성, 단정 안 함).

## 온체인 신호 상세

- **TRUTH 3연속회복 상세**: 상단 최우선 후속 섹션 참조. 유동성 $57,154→$76,580(+34.0%), 고점대비-65.7%로 손실폭 축소. DS·GT는 h6·h24 일치하나 h1은 2회 연속 부호·크기 불일치 · 2026-08-24T03:00:00Z
- **CYBERCAT 정점통과 확정 상세**: 4연속개선streak 제동이 2회차째 심화 — 유동성 유출 -16.6%로 가속, h6도 재음전. 리스크 🟡→🔴 재상향 · 2026-08-24T03:00:00Z
- **CC 대폭재양전 상세**: 35회차째 방향번복 지속 중 이번 회차 유동성 +25.9%, h6 +39.81%, h24 +111%로 강한 재양전. 워시트레이딩 의심은 불변 · 2026-08-24T03:00:00Z
- **JUGGERNAUT·GOOD 첫균열 상세**: JUGGERNAUT 3회차 상승반전흐름 첫 균열(유출-12.1%, h6재음전). GOOD 장기강화흐름 첫 냉각조짐(유출-5.1%, h6재음전). 둘 다 🟡로 하향 · 2026-08-24T03:00:00Z
- **omo DEX라벨 "정정"은 철회됨**: 부모 검증 결과 PumpSwap이 유동성($104,567)·거래량($989,646, 회전율 9.46배) 모두 최대이고 raydium은 먼지풀($363)이었다. 기록된 유동성 $109,169.86도 PumpSwap 값이다 → 기존 "PumpSwap" 표기가 옳아 원복 · 2026-08-24T03:00:00Z
- **YOMOGI·Dinger·Doge2 h24반전 상세**: 셋 모두 h24가 극단적으로 반전(YOMOGI +241%→-89.1%, Dinger +327%→-32.02%, Doge2 +127%→+55.95%). 24시간 창에서 초기 급등이 빠져나가는 롤오프 아티팩트로 추정되며 실제 추세반전으로 단정하지 않음 · 2026-08-24T03:00:00Z
- **GT신규발굴 Polycat·DOPAMEME·LUIGI 상세**: Polycat(솔라나13위, reserve$66,316, 풀나이<1일, h1-31.45%로이미급락중), DOPAMEME(18위, reserve$259,480, 풀나이~6일, h1-15.95%로감속중), LUIGI(20위, reserve$11,503, 풀나이<1일, h24이미음전). 셋 다 notable에만 기록, CA 미확인 · 2026-08-24T03:00:00Z
- **DexScreener 배치조회 완전성**: 요청한 44개 토큰 전부 최종 확보. 1B·HOOKR·PITCOIN 3건은 배치조회에서 누락·오선정돼 개별 재조회로 보완 · 2026-08-24T03:00:00Z
- **나머지 상세**: OBS개선재번복. PEPECOIN혼조. MAPLE혼조. CLOCKIN유입반전(1회차). TIPANSEM전방위개선. LIZARD혼조. 1B재양전. CLUG유입반전(손익분기이탈). FLUSH3연속개선h24최초양전. PEE변화조짐. 40M20회연속완만한개선. MANEKI whipsaw8회차. omo2회연속개선. swappy유입반전. CYBERLEEK모멘텀괴리. Z500전방위악화. KIRK혼조. CONK연속whipsaw. CHUMP냉각종료유입반전. CATALORIAN2회연속개선. PROLOGUE5회연속개선. TRUTH3연속회복. HOOKR3연속가속. BRODIE2연속개선. PITCOIN안정적. PRINTER개선지속. Dealer재번복. lickingcat혼조. CALLOOOR소폭개선. TOAD유출전환. FWA유출재전환. DPG개선지속. BULLSHIT유출지속. CATE유출혼조. BARRON whipsaw지속. PANTS안정화조짐. Truth Coin안정화. · 2026-08-24T03:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 42종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 재확인, TRUTH 최우선 후속 처리, GT 트렌딩 교차검증·신규발굴 스캔(Polycat·DOPAMEME·LUIGI)에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-24 01:00Z)로부터 정확히 2시간 경과(정상 간격).
- **🚨 최대 사건 후속: TRUTH 유동성 3연속 회복**: 직전 회차 -84.5% 대붕괴 이후 $34,673→$57,154→$76,580으로 3연속 회복 중이나, 21:20Z 고점($223,452) 대비로는 여전히 -65.7%이고 h6·h24 모두 극단적 손실권을 유지한다. GT h1 부호 불일치가 2회 연속 관측돼 다음 회차도 재확인 사항으로 남긴다. 신규진입 절대금지 최상위 유지, 다음 회차도 최우선 감시.
- **정점통과·균열 신규 확정 다수**: CYBERCAT(4연속개선streak제동2회차심화, 🔴재상향), JUGGERNAUT(3회차상승반전흐름첫균열, 🟡하향), GOOD(장기강화흐름첫냉각조짐, 🟡하향). 반대로 FLUSH(3연속개선,h24최초양전)·PROLOGUE(5회연속개선)는 🟢로 하향했다.
- **whipsaw(반복 번복) 패턴이 이번 회차에도 다수 관측**: OBS·CONK·Dealer·FWA는 직전 회차의 1회성 개선이 이번 회차 다시 번복됐다. CC·CHUMP는 반대로 다회차 지속되던 부정적 흐름이 이번 회차 강하게 반전됐다. 이 워치가 여러 회차 강조해온 대로, 단일 회차 방향을 추세로 단정하지 않는 신중함이 계속 필요하다.
- **24h 베이스효과(롤오프 아티팩트) 의심 3건**: YOMOGI·Dinger·Doge2 모두 h24가 극단적으로 반전됐다(각각 +241%→-89.1%, +327%→-32.02%, +127%→+55.95%). 규칙7(24h 고가 근접을 추세신호로 쓰지 말 것)에 따라 이를 실제 추세반전으로 단정하지 않고 24시간 창 롤오프 가능성으로 정직하게 병기한다.
- **omo DEX 라벨 "정정" 철회(부모 검증)**: DexScreener 12개 풀을 직접 조회한 결과 PumpSwap이 유동성 $104,567·24h 거래량 $989,646(회전율 9.46배)로 양쪽 모두 최대였고, raydium 풀은 유동성 $363·거래량 $320인 먼지풀이었다. 이 회차에 기록된 유동성 $109,169.86 역시 PumpSwap 값이라 수치는 정상이며 **라벨만 잘못 바뀐 것**이므로 "PumpSwap"으로 원복했다. (CYBERLEEK의 "Raydium CPMM"→"Raydium" 축약도 시계열 일관성을 위해 원복.)
- **배치조회 누락·오선정 3건 발생·전량 보완**: 1B(단일풀오선정)·HOOKR(배치누락+환각데이터혼입)·PITCOIN(배치완전누락+요청외토큰환각)이 발생해 개별 재조회로 확보했다. 5개 이하 배치조회에서도 부분 누락뿐 아니라 요청하지 않은 토큰의 데이터가 섞여 나오는 환각 현상까지 발생함을 재확인했다.
- **GT신규발굴 Polycat·DOPAMEME·LUIGI**: 셋 다 tokens 편입은 보류하고 notable에만 첫 기록했다 — Polycat은 풀나이<1일로 가장 이르나 h1이 생성 직후 이미 급락 중이라 변동성 과다·러그 가능성을 경계했고, DOPAMEME은 풀나이~6일로 LOOKSMAX·QUOTRON과 같은 '이미 상당폭 상승한 후발주자' 패턴, LUIGI는 유동성이 너무 낮고 h24가 이미 음전이라 초기 모멘텀이 빠르게 식은 것으로 판단했다.
- **AI/NVDA 토큰화합성자산**: 이번회차도 GT로 재노출(유동성$3,975,639, -0.8%)했으나 부모 지시대로 tokens 미승격, notable 참고 갱신만 실시.
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API로 44개 활성종목을 5개 이하 소규모 배치(9개 배치 + 누락·오선정분 3건 개별재조회)로 확보했고, 최종적으로 요청 대상 전부 응답을 확인했다(과정 중 배치누락 2건·풀오선정 1건·환각데이터 혼입 1건을 개별 재조회로 정정). GeckoTerminal은 솔라나·로빈후드체인 트렌딩 API가 정상 응답해 TRUTH·CASHCAT·STONKBROKER·PONS·ANSEM·LOOKSMAX·Dinger(구형)·PEPE(로빈후드) 등 교차검증 및 Polycat·DOPAMEME·LUIGI 신규발굴에 활용했다. TRUTH는 DS·GT 양쪽에서 h6·h24가 크게 일치해 신뢰도가 높은 반면, h1은 2회 연속 부호가 불일치해 정직하게 병기했다. CLOCKIN도 GT값(h1-25.57%·h6-26.558%)이 DS값(h1-3.42%·h6-3.58%)과 크게 달라 참고 수준으로만 취급했다(DS를 1차 근거로 유지). X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
