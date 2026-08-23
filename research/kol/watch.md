# 온체인 트렌딩 조기경보 — 2026-08-23 23:00 UTC (KST 2026-08-24 08:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-23 21:00Z)로부터 정확히 2시간 경과**(정상 간격). 44개 활성종목 전부를 DexScreener 토큰 API(5개 이하 소규모 배치조회, 9개 배치)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 API로 TRUTH·CYBERCAT·CATALORIAN 교차검증 및 신규 발굴 스캔을 진행했다.

> **배치조회 검증 결과**: 9개 배치 요청(각 4~5개 CA)에 대해 응답에 포함된 요청 대상 토큰은 전부 확인됐다. 다만 배치5·배치8·배치9에서 **요청하지 않은 토큰(Diddy Coin, Z/CATE/cat, IMT/ELONIA/Success)이 응답에 섞여 나온 이례적 현상**을 확인했다 — 요청한 CA와 정확히 일치하는 항목은 5개(또는 4개) 전부 존재했으므로 필요한 데이터 누락은 없었지만, 이 혼입 토큰들은 사용하지 않고 폐기했다(원인 미상, WebFetch 요약 단계의 아티팩트로 추정, 재확인 필요 사항으로 기록).

> **편입/편출/강등 내역**: **신규편입 0건**(신규 발굴 없음, GT 로빈후드체인 트렌딩에서 QUOTRON을 발견했으나 LOOKSMAX와 동일한 이유로 notable에만 기록). **편출 0건**. 활성목록 **44→44종**(순증감 0). notable **33→34개**(QUOTRON 신규 기록).

## 🚨 최우선 경보 — TRUTH 유동성 대붕괴 (부모 세션 최우선 확인 항목 ①)

| 시점 | 유동성 | h1 | h6 | h24 | 회전율 |
|---|---|---|---|---|---|
| 19:00Z | $147,532.29 | +144% | +149% | -74.53% | ≈144.8배 |
| 19:20Z(부모 교차검증) | $234,330 | +475% | +834% | -35.02%(개선) | ≈92.6배 |
| 21:00Z | $248,655.61 | -28.75% | +712% | -64.71%(재악화) | ≈86.9배 |
| 21:20Z(부모 교차검증) | $223,452 | -4.44% | +722% | -52.69% | ≈96.2배(재상승) |
| **23:00Z(이번 회차)** | **$34,673.24** | **-75.29%(대폭악화)** | **-93.25%(급반전음전)** | **-98.86%(거의완전붕괴)** | **≈613배** |

**이번 회차, TRUTH의 유동성이 직전 대비 -84.5%(약 $223K~$248K대 → $34,673.24) 대붕괴했다.** h1은 -75.29%, h6는 +722%에서 -93.25%로 급반전음전, h24는 -98.86%로 사실상 완전 붕괴 수준이다. 24h 거래량은 $21,261,569.74로, 남은 유동성 대비 **회전율이 약 613배**까지 치솟았다(직전 최고치 195.7배를 크게 상회).

**GeckoTerminal 재확인**(로빈후드체인 트렌딩 12위): reserve $28,793, h1 -89.09%, h6 -95.38%, h24 -99.20%, 24h거래량 $20,999,070.53(회전율 ≈729배)로 **DS와 방향이 완전히 일치**한다 — 두 독립 소스가 동시에 극단 붕괴를 확인해, 데이터 오류일 가능성은 낮다. 다만 이 데이터만으로는 **이것이 가격 급락에 따른 자연스러운 유동성 감소인지, 실제 유동성 인출(럭풀 가능성)인지 구분할 수 없다** — 정직하게 두 시나리오 모두를 경계로 남긴다. TRUTH는 8회차째(21:00Z 기준) "극단적 변동성" 최상위 경계로 분류돼 왔고, 이번 붕괴는 그 경계가 실제로 현실화된 사례일 수 있다.

## ⭐ 부모 세션 요청 최우선 확인 — 나머지 5건

### ② CYBERCAT·CATALORIAN — 4회차: 서로 다른 방향으로 갈라짐

- **CYBERCAT**(4회차, 풀생성후 약 9.8시간): 3회차 부분반등이 4회차 강한 전방위 개선으로 이어졌다. 유동성 $66,388.79→**$78,062.19(+17.6%, 강한유입)**, h1 +3.49%→**+48.81%(강한재양전)**, h6 -13.37%→**+33.4%(강한반전, 재양전)**, h24 +1096%→+1498%(가속). GT 재확인(솔라나 트렌딩 8위, reserve $76,566, h1+37.72%·h24+1420.57%)로 h1·h24는 대체로 일치하나 **⚠️h6는 GT -9.05%로 DS +33.4%와 부호가 불일치**한다 — 소스 간 편차가 존재해 완전반전으로 단정하기엔 신중해야 한다.
- **CATALORIAN**(4회차, 풀생성후 약 11.3시간): 정반대로, 3회차의 유입반전이 4회차에서 다시 소폭 유출·h1/h6 재음전으로 번복됐다(whipsaw). 유동성 $351,434.91→**$342,229.65(-2.6%, 소폭유출)**, h1 +3.65%→**-4.45%(재음전)**, h6 +17.74%→**-34.71%(대폭재음전)**, h24 +10219%→+9629%(감속). GT 재확인(솔라나 트렌딩 3위, reserve $338,779, h1-4.80%·h6-30.30%·h24+2327.30%)로 h1·h6 방향은 DS와 일치하나 **h24는 여전히 GT·DS 간 큰 편차**(9629% vs 2327%)가 있다.

**결론**: 3회차에서 함께 개선됐던 두 토큰이 **4회차에는 정반대 궤적**을 보였다 — CYBERCAT은 개선 지속, CATALORIAN은 개선 번복. "정점 통과 이후 유사한 부분반등"이라는 이전 회차의 공통 서술은 4회차 기준으로 더 이상 유효하지 않으며, 두 토큰을 별개로 평가해야 함을 시사한다.

### ③ LIZARD — 2회 연속 전방위 개선 (h6까지 재양전)

이전 회차는 "유동성만 반전, h24는 오히려 악화"라는 혼조였다면, **이번 회차는 유동성·h1·h6·h24 전부 개선**됐다: 유동성 $35,247.87→**$37,282.51(+5.8%, 유입지속)**, h1(+1.14%→+4.88%, 개선), h6(**-26.44%→+0.85%, 강한반전 재양전**), h24(-61.9%→**-49.96%, 개선**). 2회 연속 유동성 유입 + 이번엔 h6까지 재양전돼 지난 회차보다 신호의 일관성이 높다. 다만 h24는 여전히 -49.96%로 깊은 손실권에 있어, "완전한 추세전환"으로 단정하기엔 이르다. 리스크는 유지하되 완화 요소를 명시한다.

### ④ omo·MANEKI — 4회연속 유출 vs 강한 반전, 재차 분기

- **omo**: **4회 연속 유동성 유출**이 지속됐다(유동성 $120,589.97→**$110,645.91, -8.2%**). h1은 -13.54%로 악화됐지만, h6·h24는 소폭 개선(-32.77%, -37.09%)했다 — 여전히 깊은 마이너스권이나 낙폭이 다소 줄었다.
- **MANEKI**: 1회차만의 유출·재음전이 다시 **강한 전방위 반전개선**으로 번복됐다(6회차째 whipsaw). 유동성 $48,427.52→**$64,227.37(+32.6%, 대폭유입반전)**, h1(-5.34%→+15.92%), h6(+7.88%→+97.25%), h24(+20.12%→+107%). **GT 재확인(로빈후드체인 3위, reserve $63,920, h1+17.38%·h6+97.10%·h24+101.71%)로 DS와 거의 완벽히 일치** — 이번 반전은 데이터 오류가 아닌 실제 강한 개선으로 확인된다.

두 토큰이 이번 회차 다시 분기됐다(MANEKI 강한 반전 vs omo 4회연속 유출). MANEKI의 경우 GT 교차검증으로 신뢰도가 높아졌지만, 6회차째 반복되는 whipsaw 이력을 감안하면 다음 회차 재번복 가능성을 계속 경계해야 한다.

### ⑤ CLUG — 4회차째: 다시 강한 반전개선 (5회차째 whipsaw)

직전 회차(3→4회차 흐름)의 "종료됐던 개선streak가 다시 강하게 반전"됐다고 봤으나, **이번 회차(5회차째)는 다시 유출·h6 재음전으로 번복**됐다: 유동성 $46,437.64→**$43,304.93(-6.7%, 유출전환)**, h1(+30.72%→+13.54%, 감속), h6(+7.72%→-5.5%, 재음전), h24(+43.18%→+30.28%, 감속). 54~55회차째 반복되는 whipsaw 패턴이 이번 회차로 재확인됐다.

## 그 밖 특기 사항

- **HOOKR(38회차)**: 37회차째 이어지던 "완만한 되돌림"이 처음으로 **강한 전방위 반전개선**으로 전환됐다(유동성 +30.6%, h1 -0.91%→+39.03%, h24 +25.07%→+76.83%). 장기 흐름의 첫 반전으로, 다음 회차 지속 여부를 주시한다.
- **1B(23회차)**: 경미한 재악화가 강한 전방위 반전개선(유동성+46.0%, h6+138%, h24+61.91%)으로 번복됐다. 22회차째 whipsaw 이력이 있어 신중 유지.
- **BULLSHIT(54회차)**: ⚠️이번 조회에서 풀 개수가 기존 10개에서 4개로 집계돼(소액 더스트풀 소멸 또는 쿼리 결과 차이 가능성) 유동성 합산치가 $231,572.13→$625,059.41(+170%)로 급증했다. 데이터 연속성이 불확실해 재확인이 필요함을 명시한다.
- **CONK·BARRON**: 둘 다 직전 회차의 "악화 전환"이 이번 회차 다시 "개선"으로 번복돼(whipsaw), 최근 여러 라운드 강조해온 반복 반전 패턴에 부합한다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **MAPLE** | Solana(PumpSwap) | 미확인 | 19회차. h1재음전,h6·h24가속 | 유동성$28,796.4(-1.0%), h24+53.84% | 지속(19회차) | 🟢 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 43회차. 강화streak첫제동 | 유동성$220,127.08(-4.7%), h24+62.22% | 지속(43회차)·첫제동 | 🟡(하향) | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 33회차. 소폭유사,h1재음전 | 유동성$21,357.34(+1.7%), h24+10.81% | 지속(33회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 4회차. 3→4회연속개선,h6재양전 | 유동성$78,062.19(+17.6%), h1+48.81% | 지속(4회차)·4연속개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 14회차. 2회연속전방위개선,h6재양전 | 유동성$37,282.51(+5.8%), h24-49.96% | 지속(14회차)·2회연속개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 31회차. 전지표대체로유사 | 유동성$15,231.64(-0.2%), h24+23.29% | 지속(31회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 55회차. 5회차째whipsaw,재유출 | 유동성$43,304.93(-6.7%), h24+30.28% | 지속(55회차)·whipsaw | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **40M** | Solana(PumpSwap) | 미확인 | 18회차. 유입강화,완만한개선지속 | 유동성$12,557.64(+11.9%), h24-45.76% | 지속(18회차)·완만한개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 23회차. 강한전방위반전개선 | 유동성$32,623.18(+46.0%), h24+61.91% | 지속(23회차)·강한반전 | 🟢(하향) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 25회차. 24회차째whipsaw재반전 | 유동성$85,425.75(-6.4%), h24+82.75% | 지속(25회차)·whipsaw | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 7회차. 6회차째whipsaw,강한반전 | 유동성$64,227.37(+32.6%), h24+107% | 지속(7회차)·whipsaw강한반전 | 🔴(재상향) | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 21회차. 유입반전,대폭개선 | 유동성$23,161.71(+10.0%), h24-79.04% | 지속(21회차)·반전개선 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 60회차. 극저유동,횡보 | 유동성$6,838.65(+0.4%) | 지속(60회차)·극저유동 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **KIRK** | Solana(PumpSwap) | 미확인 | 23회차. 대체로유사,안정적 | 유동성$81,367.35(-0.02%), h24+13.3% | 지속(23회차)·안정적 | 🟢 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 11회차. 10회차째개선흐름첫냉각 | 유동성$290,821.22(-4.0%), h24+65.91% | 지속(11회차)·첫냉각 | 🟡(하향) | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 4회차. 3회차개선이4회차재번복 | 유동성$342,229.65(-2.6%), h6-34.71% | 지속(4회차)·whipsaw재반전 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 3회차. 예상됐던감속이2회늦게실현 | 유동성$149,822.32(-9.9%), h6-27.11% | 지속(3회차)·예상감속실현 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 35회차. 유입강화,h1·h6재양전 | 유동성$1,893,834.02(+12.2%), h24+132% | 지속(35회차)·유입강화 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 36회차. 전지표소폭개선 | 유동성$208,625.99(+6.8%), h24-2.19% | 지속(36회차)·소폭개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **Z500** | Solana(PumpSwap) | 미확인 | 26회차. 전방위악화로전환 | 유동성$74,166.82(-5.0%), h24-31.97% | 지속(26회차)·전방위악화 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **CC** | Solana(PumpSwap) | 미확인 | 33회차째방향번복지속 | 유동성$254,429.51(+2.9%), h24+15.69% | 지속(33회차)·고위험 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **omo** | Solana(PumpSwap) | 미확인 | 7회차. 4회연속유출 | 유동성$110,645.91(-8.2%), h24-37.09% | 지속(7회차)·4연속유출 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **CONK** | Solana(Raydium) | 미확인 | 20회차. whipsaw재반전(강한개선) | 유동성$83,489.52(+5.6%), h1+12.31% | 지속(20회차)·whipsaw | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 9회차. ⚠️유동성대붕괴(-84.5%) | 유동성$34,673.24, h24-98.86% | 지속(9회차)·대붕괴 | 🔴(최상위경계) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 38회차. 37회차째첫강한개선 | 유동성$289,628.69(+30.6%), h24+76.83% | 지속(38회차)·첫강한개선 | 🟢(하향) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 160회차. 상승반전2회차째유지 | 유동성$299,929.55(-1.6%), h24+45.65% | 지속(160회차)·상승유지 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 136회차. 첫냉각조짐 | 유동성$187,142.33(-2.3%), h1-7.74% | 지속(136회차)·첫냉각 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 39회차. h24플러스전환 | 유동성$505,347.78(+3.6%), h24+9.69% | 지속(39회차)·h24플러스 | 🟢(하향) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 127회차. 대체로안정적 | 유동성$32,379.12(-0.5%), h24+4.02% | 지속(127회차)·안정적 | 🟢 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 174회차. 전지표소폭강화 | 유동성$355,874.77(+6.6%), h24-6.45% | 지속(174회차)·소폭강화 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 165회차. 진정이재악화로전환 | 유동성$110,656.32(-3.0%), h24-23.45% | 지속(165회차)·재악화 | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 165회차. 전방위개선 | 유동성$62,447.41(+11.8%), h24+13.61% | 지속(165회차)·개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 123회차. 혼조지속 | 유동성$62,304.69(-2.1%), h24+24.54% | 지속(123회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 173회차. 대체로유사,횡보 | 유동성$389,746.26(+0.9%), h24-4.8% | 지속(173회차)·횡보 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 177회차. h1재양전이나유출지속 | 유동성$1,206,659.02(-2.1%), h24+8.64% | 지속(177회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 125회차. 유입반전,h6재양전 | 유동성$62,424.32(+9.6%), h24-60.99% | 지속(125회차)·반전개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(다수풀) | 미확인 | 54회차. 데이터구조변화(풀10→4) | 유동성(합산)$625,059.41(+170%) | 지속(54회차)·구조변화 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 18회차. 혼조,h1재양전h6재음전 | 유동성$48,599.03(-9.4%), h24+181% | 지속(18회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 97회차. 3회연속유출streak종료 | 유동성$1,654,460.61(+9.0%), h24-53.3% | 지속(97회차)·streak종료 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **Dinger** | Solana(PumpSwap) | 미확인 | 8회차. 대폭감속 | 유동성$38,706(-4.9%), h24+314% | 지속(8회차)·감속 | 🔴 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 11회차. whipsaw개선 | 유동성$221,866.2(+0.2%), h24-32.71% | 지속(11회차)·whipsaw개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 25회차(dogwifpants). h24대폭악화 | 유동성$114,438.23(-5.9%), h24-51.48% | 지속(25회차)·h24대폭악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 12회차. 전방위개선,회전율≈6.2배 | 유동성$12,480.49(+19.4%), h24-36.02% | 지속(12회차)·전방위개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 10회차. 급반전악화,회전율≈273배 | 유동성$32,381.71(-21.0%), h1-23.42% | 지속(10회차)·급반전악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**(QUOTRON은 notable에만 신규 기록). **편출 0건**. **최우선경보**: TRUTH 유동성 대붕괴(-84.5%, DS·GT 이중확인). **whipsaw 재반전**: CLUG(5회차째), MANEKI(6회차째, GT교차검증), CATALORIAN(3→4회차 재번복), CONK, BARRON, OBS(23~24회차째). **첫 냉각/전환**: CLOCKIN(42회차째 강화 첫제동), CHUMP(10회차째 개선 첫냉각), BRODIE(첫h1재음전). **첫 강한개선**: HOOKR(37회차째 되돌림 첫반전). **데이터 이상**: BULLSHIT 풀개수 구조변화(재확인필요).

## 온체인 신호 상세

- **TRUTH 대붕괴 상세**: 상단 최우선 경보 섹션 참조. 유동성 -84.5%, h24 -98.86%, 회전율 613배(DS)/729배(GT). DS·GT 이중확인 · 2026-08-23T23:00:00Z
- **CYBERCAT·CATALORIAN 4회차 분기 상세**: 두 토큰이 3회차의 공통 부분반등 이후 4회차엔 서로 다른 방향으로 갈라짐(CYBERCAT 개선지속 vs CATALORIAN 재번복) · 2026-08-23T23:00:00Z
- **LIZARD 2회연속개선 상세**: 유동성·h1·h6·h24 전방위 개선, h24는 여전히 깊은 손실권 · 2026-08-23T23:00:00Z
- **omo·MANEKI 재분기 상세**: omo 4회연속유출 vs MANEKI GT교차검증된 강한반전(6회차째 whipsaw) · 2026-08-23T23:00:00Z
- **CLUG whipsaw 상세**: 4회차만의 강한반전개선이 5회차 다시 유출·재음전으로 번복 · 2026-08-23T23:00:00Z
- **DexScreener 배치조회 완전성**: 요청한 44개 토큰 전부 응답에서 확인, 다만 3개 배치에서 요청하지 않은 토큰이 섞여 나온 이례적 현상(사용하지 않고 폐기) · 2026-08-23T23:00:00Z
- **GT신규발굴 QUOTRON 상세**: 로빈후드체인 트렌딩18위, reserve$214,297, h24+423.70%, 풀나이약10일, LOOKSMAX와유사한이미상당폭상승한후발주자 패턴 · 2026-08-23T23:00:00Z
- **나머지 상세**: OBS whipsaw재반전. PEPECOIN혼조. MAPLE h1혼조. CLOCKIN강화streak첫제동. TIPANSEM혼조. 1B강한반전. FLUSH반전개선. PEE극저유동지속. 40M완만한개선. swappy소폭개선. CYBERLEEK유입강화모멘텀둔화. CC33회차째휩소. Z500전방위악화. KIRK안정적. CONK whipsaw. CHUMP첫냉각. PROLOGUE예상감속실현. HOOKR첫강한개선. CATE유출streak종료. GOOD h24플러스전환. PRINTER소폭강화. BULLSHIT데이터구조변화. TOAD횡보. DPG반전개선. FWA혼조. CALLOOOR혼조. JUGGERNAUT상승유지. BRODIE첫냉각. Dealer재악화. lickingcat개선. PITCOIN안정적. PANTS h24대폭악화. Doge2혼조. Truth Coin전방위개선. BARRON whipsaw개선. YOMOGI급반전악화 · 2026-08-23T23:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 42종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 재확인, TRUTH 최우선 경보 처리, 부모 세션 우선확인 나머지 5건 처리, GT 트렌딩 교차검증·신규발굴 스캔에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-23 21:00Z)로부터 정확히 2시간 경과(정상 간격).
- **🚨 최대 사건: TRUTH 유동성 대붕괴**: 8회연속 "극단변동성" 경계 대상이던 TRUTH가 이번 회차 유동성 -84.5%, h24 -98.86%까지 붕괴했다. DS·GT 두 독립 소스가 방향·규모를 모두 확인해 데이터 오류 가능성은 낮으나, 원인(자연스러운 가격급락 vs 실제 유동성 인출/럭풀)은 이 데이터만으로 판단할 수 없다. 신규진입 절대금지 최상위 유지.
- **⭐부모 세션 우선확인 6건 전부 처리**: ①TRUTH — 대붕괴 확인(최우선경보 섹션) ②CYBERCAT·CATALORIAN — 4회차에서 서로 다른 방향으로 분기(CYBERCAT 개선지속, CATALORIAN 재번복) ③LIZARD — 2회연속 전방위 개선이나 h24는 여전히 깊은 손실권 ④omo·MANEKI — 재차 분기(omo 4연속유출, MANEKI GT검증된 강한반전) ⑤WINNING — 소멸단계 유지 확인(이번회차 재조회 안함) ⑥CLUG — 5회차째 whipsaw 재확인(재유출로 번복).
- **whipsaw(반복 번복) 패턴이 이번 회차에도 다수 관측**: CLUG(5회차), MANEKI(6회차, GT검증), CATALORIAN(3→4회차), CONK, BARRON, OBS(23~24회차). 이 워치가 여러 회차 동안 강조해온 대로, 단일 회차 방향을 추세로 단정하지 않는 신중함이 계속 필요하다. 특히 이번 회차는 TRUTH의 대붕괴처럼 whipsaw 범주를 벗어나는 '단발성 극단 이벤트'도 함께 관측됐다.
- **장기 흐름의 첫 전환 다수 관측**: HOOKR(37회차째 되돌림 첫강한반전), CLOCKIN(42회차째 강화streak 첫제동), CHUMP(10회차째 개선흐름 첫냉각), BRODIE(첫h1재음전).
- **데이터 이상 2건 기록**: ①BULLSHIT 풀개수가 10개→4개로 집계돼 유동성 합산치가 급증(+170%), 구조변화인지 쿼리결과 차이인지 재확인 필요 ②DexScreener 배치조회 3건에서 요청하지 않은 토큰이 응답에 혼입(사용하지 않고 폐기, 원인 미상).
- **AI/NVDA 토큰화합성자산**: 이번회차도 GT로 재노출(유동성$3,987,523, -10.0%)했으나 부모 지시대로 tokens 미승격, notable 참고 갱신만 실시.
- **GT신규발굴 QUOTRON**: 로빈후드체인 트렌딩18위 신규발견(reserve$214,297, h24+423.70%, 풀나이~10일). LOOKSMAX와 동일한 이유(이미 상당폭 상승, 풀나이 10일)로 notable에만 첫 기록, CA는 이번 회차 미확인.
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API로 44개 활성종목을 5개 이하 소규모 배치(9개 배치)로 확보했고, 요청한 대상은 전부 응답에서 확인됐다(3개 배치에서 요청 외 토큰 혼입은 있었으나 사용하지 않고 폐기해 결과에 영향 없음). GeckoTerminal은 솔라나·로빈후드체인 트렌딩 API가 정상 응답해 TRUTH·CYBERCAT·CATALORIAN 교차검증 및 신규발굴에 활용했다. TRUTH 대붕괴는 DS·GT 양쪽에서 방향·규모가 크게 일치해 신뢰도가 높은 반면, CYBERCAT h6·CATALORIAN h24·Dinger h24는 GT·DS 간 편차가 남아있어 정직하게 병기했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*

> ⚠️ **부모 세션 교차검증(23:20Z) — TRUTH 붕괴의 성격 구분**: 재조회 결과 유동성 $52,818.45(에이전트 관측 $34,673에서 소폭 회복, 21:20Z $223,452 대비 **-76.4%**), h1 -83.51%·h6 -78.07%·h24 -96.76%, 회전율 397배. ⭐**결정적 구분 근거: WETH 리저브가 10.5537로 아직 먼지 수준이 아니다** — 완전소멸 확정된 동명 계열 Truth Coin(`0xa48a…b4`)은 소멸 시점 WETH 리저브가 **0.00947**이었다. 따라서 현재는 유동성이 빠르게 빠지는 중이되 **풀이 비워진 상태는 아니므로 "완전소멸"로 분류하지 않는다** — 본문의 "자연 감소인지 러그풀인지 이 데이터만으로 판별 불가"라는 유보가 타당하다. 부수 관측: 같은 토큰에 **풀 나이 3.4시간짜리 신규 풀**(유동성 $46.34)이 생성돼 있어 유동성 이전 시도 가능성이 있으나 규모가 미미해 단정하지 않는다. **다음 회차 최우선 감시 대상.**
