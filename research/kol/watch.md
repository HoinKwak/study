# 온체인 트렌딩 조기경보 — 2026-08-26 15:05 UTC (KST 2026-08-27 00:05)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 13:05Z)로부터 **정상 2시간** 경과. 유실 없이 정상 진행됐다.

## ✅ 인프라 개선: 풀 선정을 '고정(pinning)'으로 전환 — 완결

직전(13:05Z) 회차에서 회전율(vol24/liq) 최고 기준이 소형 풀을 선택해 시계열이 불연속으로 보이는 문제가 발견돼, 13:45Z에 "절대 24h 거래량 최대" 기준으로 교정 재계측했다. 이번(15:05Z) 회차 준비 중 **그 교정판에도 결함이 남아 있었음이 추가로 드러났다** — PRINTER는 상위 두 풀의 vol24가 거의 동률($789,898 vs $765,202)인데 유동성은 6배 차이($84K vs $538K)라, "절대 거래량 최대" 기준이 회차마다 뒤집혀 **유동성이 -84.3%로 보이는 가짜 급감**을 만들었다.

부모가 이를 근본 수정해 **한 번 고른 풀 주소를 고정(pinning)하고, 그 풀이 실제로 죽었을 때만(유동성 $5K 미만 또는 vol24가 최선 후보의 30% 미만) 교체**하는 방식으로 전환했다. **이번 회차 풀 교체 0건·유동성 25% 이상 변동 0건**을 확정했다 — 즉 아래 표의 모든 유동성 변화는 **전부 진짜**이며, ⭐**PRINTER의 직전(-84.3%) 급감은 아티팩트였고 실제로는 +0.3%(사실상 불변)였음이 확정됐다.**

## 이번 회차 핵심 발견

- **PRINTER — 재점화 지속(정정 확정)**: h24 +105%(직전 13:05Z 정정치)에 이어 이번 **+90.21%**로 2회차 연속 극단 양전 유지, h6도 +25.83%→+34.67%로 가속했다. 유동성은 $536,870으로 **+0.3%, 사실상 불변**이다 — 직전 회차에 한때 -84.3% 급감으로 잘못 계측됐던 것은 위 풀선정 아티팩트였고 실제 유출입이 아니었음이 이번 고정판으로 최종 확정됐다.
- **1B — 조기픽이 크게 살아남(부모 지목)**: h6 **+63.07%**, h24 **+75.01%**(직전 h24 +26.6%에서 대폭 재가속). 유동성은 $27,000으로 -0.7%, 거의 불변이다. 조기 단계에서 이 정도로 결실을 맺은 사례는 이 목록에서 드물며, MANEKI(조기픽 실패 사례)와 대비되는 정직한 기록으로 남긴다.
- **JUGGERNAUT(h6+39.65%·h24+36.79%)·HOOKR(h24+40.37%)·PROLOGUE(h24+34.08%)·PANTS(h6+40.45%)** 모두 전 회차 재점화가 감속하며 지속됐다. **CHUMP(h1+13.45%·h6+20.65%·h24+10.97%)**는 전 지표가 동시에 양전 전환해 risk를 🔴→🟡로 완화했다. PANTS도 전 지표 양전 전환해 🔴→🟡로 완화했다.
- **TRUTH — 유동성 정확히 불변(+0.0%), 회전율 43.1배**: 유동성이 $74,418→$74,418로 **한 자리도 안 변했는데** h24는 -81.58%(소폭 개선이나 여전히 극단 붕괴), 회전율은 43.1배(직전 75.93배에서 하락했으나 여전히 목록 최고 수준)다. h1은 DexScreener가 제공하지 않아 '미제공'으로 정직 표기(추정 안 함). 유동성이 이탈하지 않았는데 거래량만 극단적인 패턴은 워시트레이딩 의심을 이번 회차도 뒷받침한다.
- **하락 심화(부모 지목)**: **CYBERLEEK**가 목록에서 유일하게 두 자릿수 유동성 유출(-12.1%)을 기록하며 h6 -23.84%·h24 -37.34%로 대폭 악화 — risk를 🟡→🔴로 강화했다. 그 외 MANEKI(h6-45.87%·h24-61.38%, 여전히 급락 확정 상태 유지)·CYBERCAT(-68.75%)·FLUSH(-53.78%)·YOMOGI(-50.66%, 단 유동성은 +10.4%로 목록 최대 유입률)·PEPECOIN(-46.81%)·Dealer(h6-25.47%·h24-27.02%, 🟡→🔴 강화)가 심화된 하락을 보였다.
- **유동성 $20K 미만(9종)**: Dinger($19,635, $20K 밑으로 소폭 이탈)·YOMOGI($17,355)·FLUSH($13,934)·TIPANSEM($13,796)·PEPECOIN($12,338)·CYBERCAT($11,020)·40M($8,506)·Truth Coin($8,019)·PEE($7,426). 전부 h24 붕괴폭이 CATALORIAN(직전 회차 편출, h24-93.04%) 수준에 크게 못 미쳐(가장 깊은 CYBERCAT도 -68.75%) **편출 트리거(거의 완전소멸) 미충족**으로 판단, 이번 회차도 편출을 적용하지 않는다.
- **CEX 선물시장 맥락**: 같은 시각 CEX 선물시장이 실측 110건 중 101건 하락(중앙값 -1.49%, BTC -0.47%)으로 광범위 약세다. 이 목록의 온체인 하락 종목(CYBERLEEK·MANEKI·Dealer 등)은 그 흐름과 대체로 정합적이나, PRINTER(+90%)·1B(+75%)·JUGGERNAUT(+37%)·HOOKR(+40%)처럼 CEX 약세를 무시하고 크게 재점화한 종목도 다수라 — 이 목록의 온체인 밈코인 움직임은 CEX 매크로와 상당히 디커플링돼 있다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 54회차. h1재음전(대폭반전),h6·h24는감속(양전유지) | 유동성$114,906(-8.7%), h24+19.95% | 지속(53회차)·감속하나양전유지 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 미확인 | 62회차. ⚠️하락심화지속 | 유동성$12,338(-0.1%), h24-46.81% | 지속(61회차)·악화지속 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 48회차. 유출가속,h24는소폭개선(여전히음전) | 유동성$27,799(-6.5%), h24-6.91% | 지속(47회차)·소폭개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain(Uniswap) | 없음(자체서사) | 72회차. 풀고정확인(교체0건),혼조 | 유동성$175,290(-2.0%), h24-17.67%, 풀나이미확인 | 지속(71회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 60회차. h1재음전(대폭반전),h24는감속(양전유지) | 유동성$13,796(-2.6%), h24+21.89% | 지속(59회차)·h24감속양전유지 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 43회차. 전지표동시악화 | 유동성$27,894(-4.4%), h24-26.73% | 지속(42회차)·전지표동시악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 52회차. ⭐조기픽재가속,드문성공사례 | 유동성$27,000(-0.7%), h6+63.07%·h24+75.01% | 지속(51회차)·h6·h24대폭재가속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 84회차. 유입전환,h24는유사(여전히심각) | 유동성$23,975(+3.2%), h24-40.4% | 지속(83회차)·유입전환 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 50회차. ⚠️하락심화지속 | 유동성$13,934(-2.0%), h24-53.78% | 지속(49회차)·h24여전히극단 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 89회차. 유사,안정 | 유동성$7,426(-0.3%), h24-5.76% | 지속(88회차)·안정 | 🟡 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 47회차. 전지표음전 | 유동성$8,506(-6.5%), h24-28.57% | 지속(46회차)·전지표음전 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 36회차. 급락확정후여전히극단 | 유동성$25,690(+1.1%), h24-61.38% | 지속(35회차)·급락확정지속 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 33회차. ⚠️하락심화지속 | 유동성$11,020(-6.0%), h24-68.75% | 지속(32회차)·h24여전히극단악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (9종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 36회차. 유입전환,h24는악화 | 유동성$98,432(+2.6%), h24-13.98% | 지속(35회차)·h24악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 65회차. 유출완화,h24는유사(음전유지) | 유동성$177,747(-1.5%), h24-4.78% | 지속(64회차)·h24여전히음전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium) | 미확인 | 64회차. ⚠️⚠️하락심화,목록유일두자릿수유출 | 유동성$1,388,497(-12.1%), h24-37.34% | 지속(63회차)·전지표대폭악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 62회차째방향번복. h24는악화 | 유동성$233,146(-2.6%), h24-29.99% | 지속(61회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 55회차. 유출멈춤,h24는개선(여전히음전) | 유동성$70,286(+0.1%), h24-17.08% | 지속(54회차)·전지표개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 52회차. h24는감속(양전유지) | 유동성$78,422(-1.7%), h24+5.01% | 지속(51회차)·h24감속양전유지 | 🟡 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 49회차. ⚠️h24재음전,손익분기붕괴 | 유동성$68,416(-8.7%), h24-0.6% | 지속(48회차)·h24재음전손익분기붕괴 | 🔴 | [DexScreener](https://dexscreener.com/solana/DShht9B8wCRe5t3oqdPB77PnjJbKxbYaZyuWpZQjbonk) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 40회차. ⭐전지표양전전환 | 유동성$390,168(+8.3%), h24+10.97% | 지속(39회차)·전지표양전전환 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 32회차. ⭐h24여전히강한양전,재점화지속 | 유동성$266,130(-1.3%), h24+34.08% | 지속(31회차)·h24여전히강한양전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 38회차. ⭐유동성정확히불변(+0.0%)인데h24소폭개선,워시트레이딩의심지속 | 유동성$74,418(+0.0%), h24-81.58%, 회전율43.1배 | 지속(37회차)·워시트레이딩의심지속 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 37회차. h24는악화(손익분기이탈) | 유동성$19,635(-1.9%), h24-5.66% | 지속(36회차)·h24손익분기이탈 | 🟡 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 67회차. ⭐h24여전히강한양전,재점화지속 | 유동성$485,065(-5.7%), h24+40.37% | 지속(66회차)·h24여전히강한양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 189회차. ⭐h24여전히강한양전,재점화지속 | 유동성$463,466(+2.5%), h24+36.79% | 지속(188회차)·h24여전히강한양전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 165회차. whipsaw패턴재확인,악화확대 | 유동성$201,921(-4.7%), h24-24.38% | 지속(164회차)·whipsaw패턴재확인 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 68회차. h24는악화(손익분기이탈) | 유동성$512,449(+0.9%), h24-7.69% | 지속(67회차)·h24손익분기이탈 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 미확인 | 203회차. ⭐⭐h24재점화지속(+90.21%),직전-84.3%급감은풀선정아티팩트로확정 | 유동성$536,870(+0.3%,사실상불변), h24+90.21% | 지속(202회차)·h24재점화지속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 194회차. ⚠️하락심화,전지표동시악화 | 유동성$72,721(-7.9%), h24-27.02% | 지속(193회차)·전지표동시악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 194회차. h1·h6개선,여전히h24음전 | 유동성$40,156(+5.4%), h24-23.88% | 지속(193회차)·h1h6개선지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 152회차. ⚠️전지표재음전전환(대폭반전) | 유동성$67,412(-6.5%), h24-15.45% | 지속(151회차)·전지표재음전전환 | 🔴 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 202회차. 약보합 | 유동성$330,981(-3.7%), h24-11.67% | 지속(201회차)·약보합 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 206회차. 유입전환,h24는개선 | 유동성$1,103,910(+2.1%), h24-23.25% | 지속(205회차)·206회차달성 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 154회차. h24여전히극단악화 | 유동성$37,425(-3.7%), h24-35.81% | 지속(153회차)·h24여전히극단악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap) | 미확인(WebSearch보도없음) | 83회차. h24는손익분기유지 | 유동성$233,723(-1.5%), h24+1.06% | 지속(82회차)·h24손익분기유지 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 156회차. h24대폭감속,정점통과경계심화 | 유동성$45,554(-6.6%), h24+19.01% | 지속(155회차)·정점통과경계 | 🔴 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap,dogwifpants) | 미확인 | 54회차. ⭐전지표양전전환 | 유동성$85,626(+8.9%), h24+4.88% | 지속(53회차)·전지표양전전환 | 🟡 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 47회차. h24개선하나여전히깊은음전 | 유동성$52,777(+0.5%), h24-33.88% | 지속(46회차)·h24개선하나여전히깊은음전 | 🔴 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 41회차. h24는악화지속 | 유동성$8,019(+6.4%), h24-14.36% | 지속(40회차)·h24악화지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 40회차. 안정,저회전율·고령풀 | 유동성$209,462(-0.4%), 회전율0.06배(최저), h24-6.1% | 지속(39회차)·안정 | 🟡 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 39회차. ⚠️하락심화지속,유동성은목록최대유입률 | 유동성$17,355(+10.4%), h24-50.66% | 지속(38회차)·h24여전히극단악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |
| **CATE** | Solana(PumpSwap) | 미확인 | 126회차달성. 유출멈춤,안정 | 유동성$2,208,258(+0.4%), h24-16.6% | 지속(125회차)·안정 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |

> **편입/편출/강등/재승격 요약(이번 회차)**: **신규편입 0건·편출 0건**($20K 미만 9종 모두 편출 트리거 미충족, CATALORIAN은 직전(13:05Z) 회차 편출 유지). **강등 5건(🟡→🔴)**: LIZARD(전지표동시악화)·CYBERLEEK(목록유일두자릿수유출,대폭악화)·CONK(h24재음전,손익분기붕괴)·Dealer(전지표동시악화)·CALLOOOR(전지표재음전전환). **재승격 2건(🔴→🟡)**: CHUMP(전지표양전전환)·PANTS(전지표양전전환). 활성목록 **43종 유지**(조기13/확산9/뒷북21, 종목구성불변). notable **79개 유지**(이번회차 개별재조회 없음, 전량 carryover). **핵심 이벤트**: ⭐부모의풀선정'고정(pinning)'전환으로PRINTER의직전-84.3%급감이아티팩트였음(실제+0.3%)확정, 1B조기픽재가속(h24+75.01%,드문성공사례), PRINTER·JUGGERNAUT·HOOKR·PROLOGUE·PANTS재점화지속, CHUMP·PANTS전지표양전전환, TRUTH유동성완전불변(+0.0%)+회전율43.1배워시트레이딩의심지속, CYBERLEEK목록유일두자릿수유동성유출로하락최심화.

## 온체인 신호 상세

- **풀 선정 '고정(pinning)' 전환 경위**: 13:05Z 회차는 "회전율 최고" 기준의 결함(소형풀 선택)을 13:45Z에 "절대거래량 최대"로 교정했으나, 이번(15:05Z) 준비 중 PRINTER 사례(상위 두 풀의 vol24 거의 동률인데 유동성 6배 차이)로 그 교정판마저 회차마다 풀이 뒤집힐 수 있음이 드러났다. 부모가 **한 번 고른 풀을 고정하고, 유동성 $5K 미만 또는 vol24가 최선 후보의 30% 미만일 때만 교체**하는 방식으로 최종 수정했다. 이번 회차 **풀교체 0건·유동성25%이상변동 0건**으로 안정성 확인 · 2026-08-26T15:05:00Z
- **PRINTER 상세(아티팩트 확정)**: 유동성$535,482→$536,870(+0.3%,사실상불변). 직전 13:05Z 회차 초안에 한때 계측됐던 -84.3% 급감은 위 풀선정 방법론 결함으로 인한 아티팩트였고 실제 유출입이 아니었음이 확정됐다. h1+7.24%→-14.28%, h6+25.83%→+34.67%(가속), h24+52.37%→+105%→+90.21%(2회차연속대폭재점화). 회전율1.43배,풀나이11.5일(2026-08-15생성) · 2026-08-26T15:05:00Z
- **1B 상세(조기픽 성공 사례)**: 유동성$27,187→$27,000(-0.7%,거의불변). h1+35.28%→-3.2%(재음전,소폭), h6+57.54%→+63.07%(대폭가속), h24+26.60%→+75.01%(대폭재가속). 조기 단계에서 유동성이 거의 빠지지 않은 채 h6·h24가 동시에 큰 폭 가속한 드문 사례로, MANEKI(조기픽이 반대방향으로 실현된 사례)와 대비해 정직하게 기록한다 · 2026-08-26T15:05:00Z
- **TRUTH 상세**: 유동성$74,418→$74,418(+0.0%,정확히동일). h1 DexScreener 미제공(추정안함), h6+0.12%→-0.03%, h24-88.99%→-81.58%. 회전율75.93배→43.1배(하락했으나여전히목록최고수준). 유동성이 전혀 변동 없는데 회전율만 극단적으로 높은 패턴은 유출이 아니라 초고빈도 워시트레이딩 의심의 근거로 재확인됨 · 2026-08-26T15:05:00Z
- **CYBERLEEK 상세(하락 최심화)**: 유동성$1,580,475→$1,388,497(-12.1%, 목록 유일 두 자릿수 유출), h1-5.88%→-7.81%(악화), h6-0.79%→-23.84%(대폭악화), h24-5.34%→-37.34%(대폭악화). risk를 🟡→🔴로 강화 · 2026-08-26T15:05:00Z
- **CEX 맥락**: 같은 시각 CEX 선물시장은 실측 110건 중 101건 하락(중앙값-1.49%, BTC-0.47%)으로 광범위 약세. CYBERLEEK·MANEKI·Dealer 등 온체인 하락종목은 이 흐름과 정합적이나, PRINTER·1B·JUGGERNAUT·HOOKR 등 강한 재점화 종목은 CEX 약세와 무관하게 움직여 이 목록의 밈코인 흐름이 매크로와 상당히 디커플링돼 있음을 시사 · 2026-08-26T15:05:00Z
- **나머지 상세**: OBS h1재음전(감속하나양전유지). PEPECOIN h24악화지속(하락심화). MAPLE h24소폭개선(여전히음전). CLOCKIN혼조(풀고정확인). TIPANSEM h24감속양전유지. LIZARD전지표동시악화. CLUG유입전환(여전히심각). FLUSH h24여전히극단(하락심화). PEE안정. 40M전지표음전. MANEKI급락확정지속. CYBERCAT h24여전히극단악화(하락심화). omo h24악화. swappy h24여전히음전. CC워시트레이딩의심불변. Z500전지표개선. KIRK h24감속양전유지. CONK h24재음전손익분기붕괴. GOOD h24손익분기이탈. HOOKR·JUGGERNAUT·PROLOGUE h24여전히강한양전(재점화지속). BRODIE whipsaw패턴재확인(악화확대). Dealer전지표동시악화(하락심화). lickingcat h1h6개선지속(여전히h24음전). CALLOOOR전지표재음전전환(대폭반전). TOAD약보합. FWA유입전환·206회차달성. DPG h24여전히극단악화. BULLSHIT h24손익분기유지. PITCOIN정점통과경계심화. Doge2 h24개선하나여전히깊은음전. Truth Coin h24악화지속. BARRON안정. YOMOGI h24여전히극단악화(하락심화,유동성은최대유입률). CATE안정 · 2026-08-26T15:05:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음(X 접근불가)**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant 보도(carryover 유지, 신규 없음)**.
- **나머지 39종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 부모가 계측·확정한 43개 활성종목 표 인용에 집중했고, 개별 KOL 검색·X 직접 조회는 로그인월 문제로 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 13:05Z)로부터 **정상 2시간** 경과, 유실 없음.
- **저장 후 세 파일(json·csv·md) 종목 목록 대조**: tokens(json) 43종·csv 43행(헤더 제외)·md 3개 표(조기13+확산9+뒷북21=43) 전부 일치 확인함. notable(json) 79건(이번 회차 신규·변경 없음, 전량 carryover).
- **⭐⭐풀 선정 '고정(pinning)' 전환 완결(이번 회차 최대 이슈)**: 13:05Z→13:45Z 교정("회전율 최고"→"절대거래량 최대")도 PRINTER 사례에서 여전히 회차마다 풀이 뒤집힐 수 있음이 드러나, 부모가 **풀 주소 고정 + 실질 사망 시에만 교체**로 최종 전환했다. 이번 회차 **풀교체 0건·유동성25%이상변동 0건**으로 안정성이 실측 확인됐고, PRINTER의 직전 -84.3% 급감이 아티팩트였음(실제 +0.3%)이 확정됐다. **다음 회차부터는 이 고정 방식이 계속 안정적인지 지켜볼 필요가 있다.**
- **risk 변경 7건**: 강등 5건(LIZARD·CYBERLEEK·CONK·Dealer·CALLOOOR, 전부 🟡→🔴), 재승격 2건(CHUMP·PANTS, 전부 🔴→🟡).
- **$20K 미만 9종은 편출 트리거 미충족**: Dinger·YOMOGI·FLUSH·TIPANSEM·PEPECOIN·CYBERCAT·40M·Truth Coin·PEE 전부 h24 붕괴폭이 CATALORIAN 편출 기준(h24-93%대, 31회차 지속 거의완전소멸)에 크게 못 미쳐(최심 CYBERCAT도 -68.75%) 편출을 적용하지 않았다.
- **CEX 선물시장 맥락 참고**: 같은 시각 CEX 선물이 실측 110건 중 101건 하락(중앙값-1.49%, BTC-0.47%)으로 광범위 약세였으나, 이 온체인 목록의 강한 재점화 종목(PRINTER·1B·JUGGERNAUT·HOOKR)은 그 흐름과 무관하게 움직여 디커플링이 뚜렷했다.
- **데이터 신뢰도**: 이번 회차는 부모 세션이 DexScreener를 직접 조회해 계측하고 풀 선정 방법론을 근본 개선(고정 방식)한 43개 활성종목 표를 1차 근거로 그대로 인용했다(재추정 없음). PRINTER 아티팩트를 부모가 스스로 규명·투명하게 정정한 사례로, 방법론 오류 발견 시 정직하게 정정하는 절차가 이번에도 작동했다. CLOCKIN 풀나이는 DexScreener 데이터 부재로 '미확인' 표기(추정 안 함), TRUTH h1도 마찬가지로 '미제공' 정직 표기. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·DexScreener(부모계측·풀고정재계측)/GeckoTerminal/CoinGecko/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아니다. 재실행 시 갱신.*
