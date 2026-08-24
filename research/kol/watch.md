# 온체인 트렌딩 조기경보 — 2026-08-24 01:00 UTC (KST 2026-08-24 10:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-23 23:00Z)로부터 정확히 2시간 경과**(정상 간격). 44개 활성종목 전부를 DexScreener 토큰 API(5개 이하 소규모 배치조회, 총 10회 요청 — 9개 배치 + 누락분 재조회 3건)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 API로 TRUTH·CHUMP 교차검증 및 신규 발굴 스캔을 진행했다.

> **배치조회 검증 결과**: 요청한 44개 토큰 전부 최종적으로 데이터를 확보했다. 다만 과정에서 **두 배치에서 요청 대상 토큰 일부가 누락**됐다 — ① 40M·MANEKI·CYBERCAT·omo·swappy 5개 요청 배치에서 40M이 빠지고 요청하지 않은 토큰(Kimchi·orla·DUN)이 섞여 나와 40M을 개별 재조회로 확보(참고: 40M의 baseToken.name이 "Kimchi"라 혼동 가능성이 있었음), ② CHUMP·CATALORIAN·PROLOGUE·TRUTH·Dinger 5개 요청 배치에서 CHUMP·TRUTH 2개가 누락돼 둘 다 개별 재조회로 확보. **KIRK도 배치조회에서 소액 meteora 풀($4,011.55)을 최대유동성으로 잘못 골라 실제 주력 pumpswap 풀($81,273.93)을 놓칠 뻔해 개별 재조회로 정정**했다 — 5개 이하 배치조회에서도 부분 누락·오선정이 발생할 수 있음을 재확인했고, 이번 회차는 전 건을 개별 재조회로 보완해 최종 데이터 누락은 없다.

> **편입/편출/강등 내역**: **신규편입 0건**(GT 솔라나 트렌딩에서 Morty(Gucci Morty) 신규 발굴, 이미 상당폭 상승·풀나이 약 2일로 LOOKSMAX·QUOTRON과 동일 이유로 notable에만 기록). **편출 0건**. 활성목록 **44→44종**(순증감 0). notable **34→35개**(Morty 신규 기록).

## 🚨 최우선 후속 — TRUTH 유동성 부분 회복 (여전히 극단 손실권)

직전 회차(23:00Z) 유동성이 $223K대에서 $34,673.24로 **-84.5% 대붕괴**했던 TRUTH가, 이번 회차 **$57,154.22로 부분 회복**(부모의 23:20Z 교차검증 $52,818.45 대비도 소폭 추가 회복)했다. 다만 21:20Z 고점($223,452) 대비로는 여전히 **-74.4%**이고, h6 -92.47%·h24 -97.24%로 여전히 거의 완전 붕괴 수준을 유지 중이다. h1만 -0.67%로 대폭 개선(직전 -75.29%)됐다.

| 시점 | 유동성 | h1 | h6 | h24 | 회전율 |
|---|---|---|---|---|---|
| 21:20Z(부모) | $223,452 | -4.44% | +722% | -52.69% | ≈96.2배 |
| 23:00Z(직전회차, 대붕괴) | $34,673.24 | -75.29% | -93.25% | -98.86% | ≈613배 |
| 23:20Z(부모 교차검증) | $52,818.45 | -83.51% | -78.07% | -96.76% | ≈397배 |
| **01:00Z(이번 회차)** | **$57,154.22** | **-0.67%** | **-92.47%** | **-97.24%** | **≈359.6배** |

GeckoTerminal 재확인(로빈후드체인 4위): reserve $59,513, h6 -90.86%·h24 -97.25%로 DS와 h6·h24는 거의 일치한다. **⚠️h1만 GT +31.01% vs DS -0.67%로 부호가 불일치**하는데, 순간 스냅샷 시점 차이로 추정되며 다음 회차 재확인이 필요하다. 부모가 확인했던 풀나이 3.4시간짜리 신규 풀(유동성 $46.34)은 규모가 미미해 이번 회차도 영향을 판단할 수 없다. **자연스러운 가격급락에 따른 유동성 감소인지, 실제 유동성 인출(럭풀)인지는 여전히 판별 불가** — 완만한 회복세가 관측되긴 했으나 규모가 여전히 극단적이라 최상위 경계를 유지한다.

## 그 밖 특기 사항

- **omo(8회차)**: 4회 연속 유동성 유출 끝에 이번 회차 **처음으로 유동성·h1·h6·h24 전지표 동반 개선**을 기록했다(유출폭도 -8.2%→-0.8%로 대폭 축소). 완전한 반전으로 단정하긴 이르나(h24 여전히 -31.86%), 4연속 유출 streak가 사실상 종료됐다는 점은 주목할 변화다.
- **CLUG(56회차)**: 5회차째 whipsaw가 이번엔 유출 심화로, h24가 +30.28%→+2.24%로 거의 손익분기까지 대폭 감속했다. 55회차째 반복 패턴이 이번엔 더 깊게 악화됐다.
- **CONK(21회차)**: 직전 회차 경계했던 "신뢰도 낮은 반전"이 예상대로 다시 번복됐다 — 유동성 유출 재전환, h1/h6/h24 전방위 악화.
- **CATALORIAN(5회차)**: 3→4회차의 재번복이 이번엔 다시 강한 반전 개선으로 번복됐다(6번째 whipsaw 가능성). CYBERCAT은 반대로 4연속 개선 streak가 이번에 처음 제동이 걸려, 두 토큰이 다시 대조적 궤적을 보였다.
- **BULLSHIT(55회차)**: 직전 회차의 "풀 개수 10→4개 이상현상"이 이번 회차 해소됐다. 단일 pumpswap 풀 기준 유동성이 $231,753.94로, 이상현상 발생 이전(2회차 전) 기준선 $231,572.13과 거의 일치해 직전 회차의 합산치($625,059.41)가 쿼리 아티팩트였음을 확인했다.
- **FWA(178회차)**: 176~177회차째 이어지던 유동성 유출 흐름이 이번 회차 유입(+10.0%)으로 반전됐다.
- **KIRK 데이터 검증 사례**: 배치조회가 최대유동성 풀로 소액 meteora 풀($4,011.55)을 잘못 골라 실제 주력 pumpswap 풀($81,273.93, 유동성의 95% 이상 차지)을 놓칠 뻔했다. 개별 재조회로 정정해 반영했다 — 규칙2("최대유동성 풀 기계적 선정 금지, 실거래 풀 확인")의 중요성을 재확인한 사례.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 26회차. 25회차째whipsaw이번엔개선반전 | 유동성$90,392.32(+5.8%), h24+45.66% | 지속(26회차)·개선반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 34회차. 전지표소폭개선 | 유동성$21,767.18(+1.9%), h24+15.82% | 지속(34회차)·소폭개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 20회차. h1대폭악화,19회차연속개선첫제동 | 유동성$28,062.57(-2.5%), h1-25.36% | 지속(20회차)·h1급락 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 44회차. 강화streak제동2회차째 | 유동성$202,365.21(-8.1%), h24+42.14% | 지속(44회차)·제동지속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 32회차. h1가속,h6악화혼조 | 유동성$14,698.02(-3.5%), h24+4.09% | 지속(32회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 15회차. 2회연속개선streak이유동성·h1재음전으로번복 | 유동성$35,639.9(-4.4%), h24-36.71% | 지속(15회차)·whipsaw우려 | 🔴 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 24회차. 강한반전2회차째유지실패조짐 | 유동성$31,763.84(-2.6%), h24+64.74% | 지속(24회차)·재악화조짐 | 🟡(하향) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 56회차. 5회차째whipsaw,유출심화 | 유동성$37,502.57(-13.4%), h24+2.24%(손익분기근접) | 지속(56회차)·whipsaw심화 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 22회차. 2회연속전방위개선,h6재양전 | 유동성$29,241.9(+26.3%), h24-36.48% | 지속(22회차)·2회연속개선 | 🟡(하향) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 61회차. 극저유동,횡보 | 유동성$6,811.55(-0.4%) | 지속(61회차)·극저유동 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 19회차. 유입지속,19회차연속완만한개선 | 유동성$12,824.93(+2.1%), h24-34.12% | 지속(19회차)·완만한개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 8회차. 7회차째whipsaw,강한반전2회차째유지실패 | 유동성$59,697.22(-7.1%), h24+65.17% | 지속(8회차)·whipsaw7회차 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 5회차. 4연속개선streak첫제동 | 유동성$70,804.35(-9.3%), h24+1208% | 지속(5회차)·첫제동 | 🟡 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 8회차. ⭐4연속유출종료,전지표동반개선 | 유동성$109,749.97(-0.8%,유출폭축소), h24-31.86% | 지속(8회차)·개선전환 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 37회차. 유출전환,h1만재양전 | 유동성$200,753.83(-3.8%), h24-12.09% | 지속(37회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 36회차. 유입강화streak이유출로전환 | 유동성$1,776,088.18(-6.2%), h24+54.52% | 지속(36회차)·모멘텀둔화 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 34회차째방향번복지속 | 유동성$234,247.6(-7.9%), h24-9.19% | 지속(34회차)·고위험 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 27회차. 전방위악화흐름지속 | 유동성$73,618.61(-0.7%), h24-31.76% | 지속(27회차)·악화지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 24회차. 대체로안정적,h24재음전 | 유동성$81,273.93(-0.1%), h24-2.41% | 지속(24회차)·안정적 | 🟢 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 21회차. whipsaw재음전확인 | 유동성$77,218.44(-7.5%), h24-57.05% | 지속(21회차)·whipsaw재음전 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 12회차. 첫냉각조짐유지,유출지속 | 유동성$289,395.43(-0.5%), h24+45.19% | 지속(12회차)·점진적냉각 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 5회차. 6번째whipsaw우려,이번엔개선 | 유동성$339,270.02(-0.9%), h24+9380% | 지속(5회차)·whipsaw우려 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 4회차. 감속국면완만히개선 | 유동성$145,740.2(-2.7%), h24+113% | 지속(4회차)·완만한개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 10회차. 9회차째대붕괴이후부분회복 | 유동성$57,154.22, h24-97.24% | 지속(10회차)·부분회복 | 🔴(최상위경계) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 39회차. 첫강한개선2회차째유지 | 유동성$287,079.5(-0.9%), h24+98.8% | 지속(39회차)·유지 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 161회차. 상승반전3회차째유지 | 유동성$294,537.64(-1.8%), h24+38.48% | 지속(161회차)·상승유지 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 137회차. 첫냉각조짐완화 | 유동성$188,684.9(+0.8%), h1+0.64% | 지속(137회차)·냉각완화 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 40회차. h24강화지속 | 유동성$504,128.13(-0.2%), h24+15.58% | 지속(40회차)·h24강화 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 128회차. 대체로안정적 | 유동성$32,176.03(-0.6%), h24-9.73% | 지속(128회차)·안정적 | 🟢 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 175회차. 다회차연속완만한개선 | 유동성$367,668.35(+3.3%), h24+2.68% | 지속(175회차)·h24플러스 | 🟢(하향) | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 166회차. 재악화흐름반전 | 유동성$113,636.86(+2.7%), h24-18.5% | 지속(166회차)·반전 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 166회차. 개선흐름일부번복 | 유동성$61,020.08(-2.3%), h24+10.57% | 지속(166회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 124회차. 소폭악화,h24재음전 | 유동성$60,380.26(-3.1%), h24-17.72% | 지속(124회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 174회차. 혼조,h24악화 | 유동성$404,609.6(+3.8%), h24-16.6% | 지속(174회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 178회차. 유출흐름이유입으로반전 | 유동성$1,326,884.51(+10.0%), h24+24.11% | 지속(178회차)·유입반전 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 126회차. h1악화,h24깊은음전지속 | 유동성$62,487.2(+0.1%), h24-59.9% | 지속(126회차)·음전지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(다수풀) | 미확인 | 55회차. 풀개수이상현상해소 | 유동성$231,753.94(단일풀정상화) | 지속(55회차)·이상해소 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 19회차. 혼조,유입반전 | 유동성$50,478.06(+3.9%), h24+127% | 지속(19회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 98회차. 3연속유출종료후1회만에재개 | 유동성$1,612,709.46(-2.5%), h24-56.81% | 지속(98회차)·유출재개 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **Dinger** | Solana(PumpSwap) | 미확인 | 9회차. h6강한재양전 | 유동성$39,373.61(+1.7%), h24+327% | 지속(9회차)·극단변동지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 12회차. whipsaw지속 | 유동성$224,758.92(+1.3%), h24-41% | 지속(12회차)·whipsaw지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 26회차(dogwifpants). h24악화심화지속 | 유동성$99,771.08(-12.8%), h24-65.71% | 지속(26회차)·악화심화 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 13회차. 개선흐름이번복 | 유동성$10,895.01(-12.7%), h24-45.26% | 지속(13회차)·흐름번복 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 11회차. 유동성안정화조짐 | 유동성$32,742.1(+1.1%), h24+241% | 지속(11회차)·극단변동지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**(Morty(Gucci Morty)는 notable에만 신규 기록). **편출 0건**. **최우선후속**: TRUTH 유동성 부분 회복(-84.5% 대붕괴 이후 $34,673→$57,154, 여전히 고점대비 -74.4%). **whipsaw 재확인**: CLUG(5회차, 유출심화), MANEKI(7회차), CONK(재음전확인), CATALORIAN(6번째 우려), 1B(재악화조짐). **첫 반전/전환**: omo(4연속유출종료), FWA(유출흐름반전), Dealer·BRODIE(반전개선), CYBERCAT(4연속개선첫제동). **데이터 검증 사례**: KIRK 최대유동성 풀 오선정 정정, BULLSHIT 풀개수 이상현상 해소.

## 온체인 신호 상세

- **TRUTH 부분회복 상세**: 상단 최우선 후속 섹션 참조. 유동성 $34,673→$57,154(+64.8%), 여전히 고점대비-74.4%. DS·GT 대체로 일치하나 h1 부호 불일치 · 2026-08-24T01:00:00Z
- **omo 4연속유출종료 상세**: 유출폭 -8.2%→-0.8%로 대폭 축소, h1/h6/h24 전지표 동반 개선(단 h24 여전히 -31.86%) · 2026-08-24T01:00:00Z
- **CYBERCAT·CATALORIAN 재분기 상세**: CYBERCAT 4연속개선streak 첫 제동, CATALORIAN은 반대로 4회차 재번복이 다시 개선으로 번복(6번째 whipsaw 가능성 경계) · 2026-08-24T01:00:00Z
- **CLUG·CONK whipsaw 상세**: CLUG 5회차째 유출심화·h24손익분기근접, CONK는 직전 회차 신뢰도낮게평가했던반전이 예상대로 다시 재음전으로 번복 · 2026-08-24T01:00:00Z
- **BULLSHIT 데이터이상 해소 상세**: 단일 pumpswap 풀 기준 유동성 $231,753.94로 2회차전 기준선($231,572.13)과 거의 일치 → 직전 회차 합산치 급증($625,059.41)은 쿼리 아티팩트였음 확인 · 2026-08-24T01:00:00Z
- **KIRK 데이터검증 상세**: 배치조회가 소액 meteora 풀($4,011.55)을 최대유동성으로 오선정, 실제 주력 pumpswap 풀($81,273.93)을 개별 재조회로 정정 반영 · 2026-08-24T01:00:00Z
- **DexScreener 배치조회 완전성**: 요청한 44개 토큰 전부 최종 확보. 40M·CHUMP·TRUTH 3건은 배치조회에서 누락돼 개별 재조회로 보완 · 2026-08-24T01:00:00Z
- **GT신규발굴 Morty 상세**: 솔라나 트렌딩10위, CA GUmbtfjSZkybSFgPibBcvwExEBdXwewJHR5PkTjzpump, 유동성$131,003.37, h24+1856%, 풀나이약2일, h1만+5.31%로크게둔화돼이미모멘텀정점통과가능성 · 2026-08-24T01:00:00Z
- **나머지 상세**: OBS whipsaw개선반전. PEPECOIN소폭개선. MAPLE h1급락(19회차연속개선첫제동). CLOCKIN제동2회차째. TIPANSEM혼조. LIZARD whipsaw우려. 1B재악화조짐. FLUSH2회연속개선. PEE극저유동지속. 40M완만한개선지속. MANEKI whipsaw7회차. swappy혼조. CYBERLEEK모멘텀둔화. CC34회차째휩소. Z500악화지속. KIRK안정적. CHUMP점진적냉각. PROLOGUE완만한개선. HOOKR개선유지. JUGGERNAUT상승유지3회차. BRODIE냉각완화. GOOD h24강화. PITCOIN안정적. PRINTER h24플러스전환. Dealer재악화반전. lickingcat혼조. CALLOOOR혼조. TOAD혼조. FWA유입반전. DPG음전지속. Doge2혼조. CATE유출재개. Dinger극단변동지속. BARRON whipsaw지속. PANTS악화심화. Truth Coin흐름번복. YOMOGI안정화조짐 · 2026-08-24T01:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 42종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 재확인, TRUTH 최우선 후속 처리, GT 트렌딩 교차검증·신규발굴 스캔에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-23 23:00Z)로부터 정확히 2시간 경과(정상 간격).
- **🚨 최대 사건 후속: TRUTH 유동성 부분 회복**: 직전 회차 -84.5% 대붕괴 이후 이번 회차 $34,673→$57,154로 완만히 회복 중이나, 21:20Z 고점($223,452) 대비로는 여전히 -74.4%이고 h6·h24 모두 극단적 손실권을 유지한다. GT h1 부호 불일치는 다음 회차 재확인 사항으로 남긴다. 신규진입 절대금지 최상위 유지, 다음 회차도 최우선 감시.
- **whipsaw(반복 번복) 패턴이 이번 회차에도 다수 관측**: CLUG(5회차, 유출심화), MANEKI(7회차), CONK(재음전확인), CATALORIAN(6번째 우려), 1B(재악화조짐), BARRON. 이 워치가 여러 회차 강조해온 대로, 단일 회차 방향을 추세로 단정하지 않는 신중함이 계속 필요하다.
- **첫 반전/전환 다수 관측**: omo(4연속유출streak사실상종료), FWA(176~177회차째유출흐름이유입으로반전), Dealer·BRODIE(재악화·냉각조짐완화), CYBERCAT(4연속개선streak첫제동), CATALORIAN(4회차재번복이다시개선으로).
- **데이터 검증 2건 기록**: ①BULLSHIT 풀개수 이상현상(10→4)이 이번 회차 단일풀 재확인으로 해소(쿼리 아티팩트였음 확인) ②KIRK 배치조회가 소액 meteora 풀을 최대유동성으로 오선정, 개별 재조회로 정정. 두 사례 모두 규칙("최대유동성 풀 기계적 선정 금지" 및 "5개 이하 배치도 부분누락 가능")의 실효성을 재확인시켜준다.
- **배치조회 누락 2건 발생·전량 보완**: 40M(요청외토큰 혼입과 함께 누락)·CHUMP·TRUTH가 배치응답에서 빠져 개별 재조회로 확보. 요청 대상과 응답 개수를 대조하는 절차가 이번 회차에도 실효적으로 작동했다.
- **AI/NVDA 토큰화합성자산**: 이번회차도 GT로 재노출(유동성$4,006,504, +0.5%)했으나 부모 지시대로 tokens 미승격, notable 참고 갱신만 실시.
- **GT신규발굴 Morty(Gucci Morty)**: 솔라나 트렌딩10위 신규발견(유동성$131,003.37, h24+1856%, 풀나이~2일). LOOKSMAX·QUOTRON과 동일한 이유(이미 상당폭 상승, h1이 h6·h24대비크게둔화)로 notable에만 첫 기록, tokens 편입은 보류.
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API로 44개 활성종목을 5개 이하 소규모 배치(9개 배치 + 누락분 3건 개별재조회)로 확보했고, 최종적으로 요청 대상 전부 응답을 확인했다(과정 중 배치누락 2건·풀오선정 1건을 개별 재조회로 정정). GeckoTerminal은 솔라나·로빈후드체인 트렌딩 API가 정상 응답해 TRUTH·CHUMP·CASHCAT 등 교차검증 및 신규발굴에 활용했다. TRUTH는 DS·GT 양쪽에서 h6·h24가 크게 일치해 신뢰도가 높은 반면, h1은 부호가 불일치해 정직하게 병기했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
