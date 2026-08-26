# 온체인 트렌딩 조기경보 — 2026-08-26 19:05 UTC (KST 2026-08-27 04:05)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 17:05Z)로부터 **정상 2시간** 경과. 유실 없이 정상 진행됐다. 풀 선정은 여전히 '고정(pinning)' 방식이며 **이번 회차도 풀교체 0건**을 확정해 아래 유동성Δ는 전부 진짜 유출입이다.

> **⚠️ 산출물 복구 안내**: 본 문서(md)는 검증 과정에서 부모 세션의 복구 시도 중 실수로 직전 회차(17:05Z) 내용으로 덮어써졌던 것을, `watch.json`·`watch.csv`에 보존돼 있던 19:05Z 데이터를 근거로 다시 작성했다. 동시에 검증 과정에서 발견된 결함 3건(json에서 CALLOOOR·PRINTER 누락, csv 4개 행 열 개수 불일치, 풀나이 37건 이월 오기)도 함께 정정했다.

## 이번 회차 핵심 발견

- **⭐⭐⭐TRUTH — 목록 최대 사건, 서사 완전 반전**: 3회차 연속 유동성이 정확히 $74,418로 얼어붙어 있던(초고회전율 43배→11.55배) TRUTH가 이번 회차 **유동성 $74,418→$104,890(+40.9%)로 3회차 만에 처음 유입**됐고, 가격은 **h1 +94.16%·h6 +94.33%·h24 +96.76%**로 폭등, **회전율은 11.55배→0.66배로 추가 급락**(거래 사실상 정지 수준)했다. 부모가 같은 단일 풀(`0x256c0e2c8B`)을 직접 재확인해 조회 시점 유동성 $106,624로 더 늘고 있고 24h 매수 354건/매도 207건임을 확인 — 풀 교체나 계측 오류가 아닌 진짜 변화다. **유동성 정지+초고회전율=워시트레이딩 의심이라는 기존 서사를 이 반전에 맞게 전면 재평가**한다: 실제 유입 확대와 회전율 붕괴는 워시트레이딩 패턴과 정반대 방향이다. 다만 4.2일 된 신생 풀에서 h24 +96.76%는 그 자체로 극단적 변동성 리스크이므로, 성격을 '워시트레이딩 의심'에서 **'신생 풀 극단 변동성 리스크'**로 재분류하되 신규진입 절대금지는 유지한다.
- **⭐⭐GOOD — 목록 최대 유입 동반 급반등**: 유동성 **+45.9%**($468,421→$683,498, 이번 회차 목록 최대 유입, 풀나이20.7일), h6 **+81.72%**·h24 +59.03%로 대폭 반전 양전. 직전 회차 '유출 동반 진짜 하락'으로 기록했던 것이 한 회차 만에 완전히 뒤집혔다. 회전율도 1.34배→3.47배로 급등. 부모 재확인: 같은 풀(`0x8EA7c66395`), 유동성 $682,935, vol24 $2.37M, 24h 매수 6,310건/매도 7,137건. 🔴→🟡로 완화하되, 이 목록 다수 종목의 반복된 방향번복 이력을 감안해 지속 확인이 필요하다.
- **⚠️⚠️1B — 유동성 $20K선 붕괴, 편출 여부 정면 판정**: 2회차 연속 유출로 $27,000→$21,342→**$18,944(-11.2%)**로 $20K 아래로 내려갔고, h6 -1.46%→**-39.14%**·h24 -1.74%→**-19.3%**로 재악화했다. **편출 판단**: 이 목록 내 Dinger·YOMOGI·TIPANSEM·FLUSH·PEPECOIN·CYBERCAT·40M·PEE·Truth Coin 등 다수 토큰이 수십 회차 동안 $20K 미만을 유지하면서도 실제 편출은 h24 -90%대의 '사실상 완전소멸' 수준(CATALORIAN·BABYSHIB 등)에만 적용돼 온 선례에 비춰, **단순 $20K선 붕괴만으로는 편출하지 않는다**. 다만 2회차 연속 유출+h6·h24 동반 재악화는 '조기픽이 결국 붕괴하는' 이 목록의 기존 패턴 재확인이라 **다음 회차에서 추가 악화 시 편출을 재검토**한다.
- **재점화 3종의 h6·h24 괴리 — 관성인지 실제 지속인지 판별 필요**: **PRINTER**(h24 +59.7%로 4회차 연속 양전이나 **h6 +14.19%→-40.37%로 대폭 냉각**) · **JUGGERNAUT**(h24 +34.48%로 여전히 양전이나 **h6 +48.45%→-23.22%로 대폭 반전**) · **HOOKR**(h24 +37.7%로 감속하며 양전 유지나 **h6 +31.47%→-10.41%로 재음전**) — 세 종목 모두 유동성이 유출로 전환됐고(-7.2%~-3.6%) h6가 h24보다 먼저 꺾여, **h24 양전은 관성(잔존 모멘텀)일 가능성이 높고 h6가 실제 방향 전환의 선행 신호**로 보인다. 반면 **PANTS는 유동성 +13.2% 유입에 h6 +10.8%·h24 +37.44%로 h6·h24가 동반 양전**해 세 종목과 대조적으로 관성이 아닌 실질 강세 지속으로 판단, 🔴→🟡 완화. **TIPANSEM도 h24 +53.79%로 가속**하며 h6도 재양전(+12.78%)해 동반 확인.
- **급락 지속·심화**: **CYBERLEEK** h6 **-43.12%**·h24 -41.73%(회전율 11.01배로 추가 급등, 유동성 -1.4% 유출 — 진짜 하락 정황 유지) · **CONK** h24 **-53.75%**(직전 -12.15%에서 급격 악화) · **MANEKI** h24 -58.3%(단 h1·h6는 큰 폭 개선) · **CYBERCAT** h24 -61.6% · **YOMOGI** h24 -48.65% · **FLUSH** h24 -44.66% · **swappy** 유동성 -13.1%(목록 최대 유출)에 h6 -28.47%·h24 -5.46%로 재음전 — 직전 회차 🔴→🟡 완화가 한 회차 만에 재반전, 🟡→🔴로 재강등.
- **유동성 $20K 미만 9종 지속, Dinger는 경계선**: 1B($18,944, 신규 진입)·YOMOGI($16,447)·TIPANSEM($13,956)·FLUSH($13,666)·PEPECOIN($12,856)·CYBERCAT($11,519)·40M($8,589)·PEE($7,753)·Truth Coin($7,605). **Dinger($19,762)도 $20K를 살짝 밑도는 경계선**이나 장기 추적 저유동 토큰 예외로 편출 미적용.
- **CEX 맥락 — 메이저 국한 반등 vs 온체인 개별 종목 양극화**: 같은 시각 CEX 선물은 **ETH·SOL·BNB가 플러스로 전환**됐으나 전체 중앙값은 여전히 -1.50%로 마이너스(XRP -2.34%) — 반등이 메이저에만 국한됐다. 온체인에서도 이와 유사하게 **TRUTH·GOOD 같은 극단적 개별 급등과 CYBERLEEK·CONK·MANEKI 등 광범위 하락이 동시에 공존**해, CEX·온체인 양쪽 모두 '선별적 강세 vs 전반적 약세'라는 같은 양극화 패턴을 보이고 있다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 미확인 | 64회차. ⭐대폭개선(유입,h6재양전) | 유동성$12,856(+9.7%), h6+8.06%·h24-7.28%(대폭개선), 풀나이17.1일 | 지속(63회차)·대폭개선 | 🟡(완화,🔴→🟡) | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 54회차. ⚠️⚠️$20K선붕괴,편출은선례상보류 | 유동성$18,944(-11.2%,2회차연속유출), h6-39.14%·h24-19.3%(재악화), 풀나이4.9일 | 지속(53회차)·$20K선붕괴 | 🔴(유지,강화) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 56회차. ⚠️h6대폭반전(재음전) | 유동성$100,761(-5.4%), h6-29.04%(대폭악화), 풀나이4.9일 | 지속(55회차)·h6대폭반전 | 🔴(유지,악화강화) | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 38회차. ⭐h1대폭재양전,h24는여전히극단 | 유동성$23,007(-1.5%), h6-15.29%(큰폭개선)·h24-58.3%, 풀나이6.1일 | 지속(37회차)·h1h6큰폭개선 | 🔴(유지) | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 62회차. h6재양전,h24⭐가속 | 유동성$13,956(+2.4%), h6+12.78%·h24+53.79%(가속), 풀나이6.2일 | 지속(61회차)·전지표양전전환가속 | 🟡(유지,강화) | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 35회차. 유입전환,h24여전히극단 | 유동성$11,519(+7.7%), h6-6.11%(개선)·h24-61.6%, 풀나이3.2일 | 지속(34회차)·h24여전히극단 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 50회차. h1재양전,유입전환 | 유동성$27,065(+1.2%), h1+7.84%(재양전)·h24-19.03%, 풀나이5.4일 | 지속(49회차)·h1재양전 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain(Uniswap) | 없음(자체서사) | 74회차. 풀고정확인,혼조지속 | 유동성$171,389(-0.2%), h24-16.46%, 풀나이미확인 | 지속(73회차)·혼조 | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 45회차. h1재양전,h6h24여전히깊은음전 | 유동성$26,428(-1.9%), h1+1.62%(재양전)·h24-35.57%, 풀나이4.8일 | 지속(44회차)·h1재양전 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 86회차. h1h6재양전,h24여전히심각 | 유동성$23,806(-0.4%), h6+4.39%(재양전)·h24-34.62%, 풀나이7.7일 | 지속(85회차)·h1h6재양전 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 52회차. h1재양전,h24여전히극단 | 유동성$13,666(+0.4%), h1+0.62%(재양전)·h24-44.66%, 풀나이4.8일 | 지속(51회차)·h24여전히극단 | 🔴(유지) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 91회차. 안정,전지표양전,h24가속 | 유동성$7,753(+4.8%), h24+9.49%(가속), 풀나이7.9일 | 지속(90회차)·h24가속 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 49회차. 유출전환,전지표대체로음전 | 유동성$8,589(-1.2%), h24-26.34%, 풀나이5.0일 | 지속(48회차)·전지표대체로음전 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |

### 확산 (9종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **KIRK** | Solana(PumpSwap) | 미확인 | 54회차. ⭐전지표재양전전환 | 유동성$76,601(+2.9%,유입), h24-1.15%→+1.0%(재양전), 풀나이6.3일 | 지속(53회차)·전지표재양전전환 | 🟡(완화,🔴→🟡) | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 34회차. ⭐전지표개선(유입동반) | 유동성$262,111(+6.3%,유입), h6-1.79%(대폭개선)·h24+7.16%, 풀나이9.1일 | 지속(33회차)·전지표개선 | 🟡(완화,🔴→🟡) | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |
| **omo** | Solana(PumpSwap) | 미확인 | 38회차. 유입전환,손익분기근접 | 유동성$96,710(+0.5%), h6-0.91%·h24-1.5%(손익분기근접), 풀나이16.6일 | 지속(37회차)·손익분기근접 | 🔴(완화신호) | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 42회차. 유입전환,혼조지속 | 유동성$381,568(+0.8%), h24-14.39%, 풀나이26.7일 | 지속(41회차)·혼조지속 | 🔴(유지) | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 67회차. ⚠️목록최대유출,재음전전환 | 유동성$164,378(-13.1%,목록최대유출), h6-28.47%·h24-5.46%(재음전), 풀나이22.0일 | 지속(66회차)·목록최대유출재음전 | 🔴(강화,🟡→🔴) | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CC** | Solana(PumpSwap) | 미확인 | 64회차째방향번복. 여전히깊은음전 | 유동성$237,809(-6.0%), h24-26.94%, 풀나이14.7일 | 지속(63회차)·워시트레이딩의심불변 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 57회차. 유출전환,여전히음전 | 유동성$70,603(-1.0%), h24-17.32%, 풀나이9.1일 | 지속(56회차)·여전히음전 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **CYBERLEEK** | Solana(Raydium) | 미확인 | 66회차. ⚠️⚠️하락심화지속(부모최우선지목) | 유동성$1,268,587(-1.4%), h6-43.12%·h24-41.73%,회전율11.01배, 풀나이10.9일 | 지속(65회차)·회전율급등가격급락동반 | 🔴(유지,심각) | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CONK** | Solana(Raydium) | 미확인 | 51회차. ⚠️h24급락심화 | 유동성$61,212(-4.6%), h24-12.15%→-53.75%(급락심화), 풀나이5.1일 | 지속(50회차)·h24급락심화 | 🔴(강화) | [DexScreener](https://dexscreener.com/solana/DShht9B8wCRe5t3oqdPB77PnjJbKxbYaZyuWpZQjbonk) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **GOOD** | Robinhood Chain(V3) | 미확인 | 70회차. ⭐⭐대규모유입급반등(목록최대유입) | 유동성$683,498(+45.9%,목록최대유입), h6+81.72%·h24+59.03%, 풀나이20.7일 | 지속(69회차)·대규모유입급반등 | 🟡(완화,🔴→🟡) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PANTS** | Solana(PumpSwap,dogwifpants) | 미확인 | 56회차. ⭐전지표양전전환·가속,강세지속 | 유동성$88,044(+13.2%,유입), h6+10.8%·h24+37.44%(가속), 풀나이7.4일 | 지속(55회차)·전지표양전전환강세지속 | 🟡(완화,🔴→🟡) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 40회차. ⭐⭐⭐목록최대사건,전면반전(유입+회전율급락) | 유동성$104,890(+40.9%,3회차만에첫유입), h6+94.33%·h24+96.76%,회전율0.66배, 풀나이4.2일 | 지속(39회차)·전면반전 | 🔴(유지,성격재평가) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 191회차. ⚠️h6대폭냉각(모멘텀불확실) | 유동성$463,151(-7.2%,유출전환), h6+48.45%→-23.22%(대폭반전)·h24+34.48%(감속), 풀나이66.8일 | 지속(190회차)·h6대폭냉각 | 🟡(유지,경계강화) | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 69회차. ⚠️h6재음전(냉각) | 유동성$499,815(-3.6%,유출전환), h6+31.47%→-10.41%·h24+37.7%(감속), 풀나이20.6일 | 지속(68회차)·h6냉각 | 🟡(유지,경계강화) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 미확인 | 205회차. h24 4회차연속양전,h6는대폭냉각 | 유동성$495,589(-4.7%), h6+14.19%→-40.37%(재음전)·h24+59.7%(감속), 풀나이11.7일 | 지속(204회차)·h6재음전h24감속 | 🟡(유지,경계강화) | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 154회차. 유출전환,큰폭감속 | 유동성$71,814(-4.7%), h6+30.42%→+11.45%·h24+22.15%→+2.75%(감속), 풀나이14.0일 | 지속(153회차)·큰폭감속 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 39회차. h24가속(양전유지) | 유동성$19,762(+1.1%,여전히$20K경계선), h24+13.28%(가속), 풀나이3.7일 | 지속(38회차)·h24가속양전 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 167회차. ⭐유출→유입반전,전지표개선 | 유동성$193,218(+6.9%,유입반전), h6-21.98%(개선)·h24-22.54%(개선), 풀나이43.7일 | 지속(166회차)·유입반전개선 | 🔴(유지) | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 196회차. 유출전환,여전히음전 | 유동성$74,223(-1.4%), h24-16.43%, 풀나이20.9일 | 지속(195회차)·여전히음전 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 196회차. 유출지속,여전히음전 | 유동성$36,523(-4.0%), h24-27.68%, 풀나이18.3일 | 지속(195회차)·여전히음전 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 204회차. ⚠️약보합에서약세전환 | 유동성$326,207(-3.4%,유출전환), h6-11.9%·h24-13.98%(악화), 풀나이18.2일 | 지속(203회차)·약세전환경계 | 🟡(유지,경계강화) | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 208회차. ⭐유입지속,전지표개선 | 유동성$1,174,026(+1.8%), h1+13.68%(재양전)·h6+15.94%·h24-8.92%, 풀나이41.1일 | 지속(207회차)·전지표개선 | 🟡(유지) | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 156회차. 유입지속,h24여전히극단 | 유동성$39,118(+1.2%), h24-23.19%, 풀나이14.2일 | 지속(155회차)·여전히극단 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap) | 미확인(WebSearch보도없음) | 85회차. 유출전환,손익분기부근 | 유동성$224,482(-2.7%), h24-9.11%, 풀나이9.0일 | 지속(84회차)·손익분기부근 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 158회차. ⭐h24대폭가속,정점통과경계유지 | 유동성$47,268(+4.5%,유입), h6-13.53%(개선)·h24+33.88%(가속), 풀나이14.1일 | 지속(157회차)·h24대폭가속 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 49회차. 유입전환,큰폭개선(여전히음전) | 유동성$53,526(+9.8%,유입), h6-2.81%(큰폭개선)·h24-14.55%(큰폭개선), 풀나이4.6일 | 지속(48회차)·큰폭개선 | 🔴(유지,완화신호) | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 43회차. 유입전환,개선(여전히음전) | 유동성$7,605(+3.7%), h6-0.6%(손익분기근접)·h24-18.7%, 풀나이4.2일 | 지속(42회차)·전지표개선극저유동지속 | 🔴(유지,완화신호) | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 42회차. 안정,저회전율·고령풀 | 유동성$209,645(+0.5%), 회전율0.06배(최저,불변), h24-8.01%, 풀나이583.7일(목록최고령) | 지속(41회차)·안정 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 41회차. 유출지속,h24여전히극단 | 유동성$16,447(-3.9%), h24-48.65%, 풀나이3.8일 | 지속(40회차)·h24여전히극단 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |
| **CATE** | Solana(PumpSwap) | 미확인 | 128회차달성. 유출전환,h1h6재음전 | 유동성$2,177,558(-4.3%), h1+8.34%→-1.93%·h6+3.38%→-5.0%(재음전), 풀나이31.1일 | 지속(127회차)·h1h6재음전전환 | 🟡(유지,경계강화) | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |

> **편입/편출/강등/재승격 요약(이번 회차)**: **신규편입 0건·편출 0건**(1B는 $20K선 붕괴했으나 선례상 편출 미적용, 다음 회차 재검토). **완화(🔴→🟡) 5건**: PEPECOIN(대폭개선,h24-46.66%→-7.28%) · KIRK(전지표재양전전환) · PROLOGUE(전지표개선,유입동반) · GOOD(⭐⭐대규모유입급반등,목록최대유입) · PANTS(⭐전지표양전전환·가속,강세지속). **강화(🟡→🔴) 1건**: swappy(목록최대유출동반재음전전환). 활성목록 **43종 유지**(조기13/확산9/뒷북21, 종목구성불변). notable **79개 유지**(이번회차 개별재조회 없음, 전량 carryover). **핵심 이벤트**: ⭐⭐⭐TRUTH전면반전(유동성3회차불변→+40.9%유입,회전율4분의1추가급락,워시트레이딩의심을신생풀변동성리스크로재평가), ⭐⭐GOOD목록최대유입급반등, ⚠️⚠️1B $20K선붕괴(편출은보류·다음회차재검토), JUGGERNAUT·HOOKR·PRINTER h6대폭냉각(h24관성vsh6선행신호구도), PANTS h6h24동반강세지속대조, CYBERLEEK·CONK급락심화, swappy목록최대유출재강등, CEX메이저국한반등과온체인개별종목급등광범위하락공존양극화.

## 온체인 신호 상세

- **TRUTH 상세(⭐⭐⭐목록 최대 사건, 전면 반전)**: 유동성$74,418→$104,890(+40.9%,3회차연속불변끝첫유입). h1은DexScreener미제공(추정안함)이나 부모직접재확인시+94.16%. h6-0.75%→+94.33%(대폭반전), h24-45.69%→+96.76%(대폭반전). 회전율11.55배→0.66배(추가급락,거래사실상정지수준), 풀나이4.2일(2026-08-22생성). 부모가동일단일풀(0x256c0e2c8B)재확인 — 조회시점유동성$106,624로더증가,24h매수354건/매도207건. 풀교체·계측오류아닌진짜변화로판단. 기존'유동성불변+초고회전율=워시트레이딩의심'서사를전면재평가 — 실유입+회전율붕괴는워시트레이딩패턴과정반대. 다만4.2일된신생풀에서h24+96.76%자체가높은변동성리스크라'신생풀극단변동성리스크'로재분류, 신규진입절대금지는유지 · 2026-08-26T19:05:00Z
- **GOOD 상세(⭐⭐목록최대유입급반등)**: 유동성$468,421→$683,498(+45.9%,목록최대유입). h1+1.63%→+5.98%, h6-19.69%→+81.72%(대폭반전), h24-29.57%→+59.03%(대폭반전). 회전율1.34배→3.47배(급등), 풀나이20.7일(2026-08-06생성). 직전회차'유출동반진짜하락'으로기록했던것이한회차만에완전반전. 부모재확인: 같은풀(0x8EA7c66395), 유동성$682,935, vol24 $2.37M, 24h매수6,310건/매도7,137건. 진짜유입정황이나과거방향번복이력상단정금지 · 2026-08-26T19:05:00Z
- **1B 상세(⚠️⚠️$20K선붕괴,편출판정)**: 유동성$21,342→$18,944(-11.2%,2회차연속유출,목록내처음으로$20K선붕괴), 풀나이4.9일(2026-08-21생성). h1-9.8%→-8.46%, h6-1.46%→-39.14%(대폭악화), h24-1.74%→-19.3%(악화). 편출판단: 이목록다수토큰(Dinger·YOMOGI·TIPANSEM·FLUSH·PEPECOIN·CYBERCAT·40M·PEE·Truth Coin)이수십회차간$20K미만유지하면서도실제편출은h24-90%대'사실상완전소멸'수준(CATALORIAN·BABYSHIB등)에만적용된선례에따라단순threshold붕괴만으로는편출하지않는다. 2회차연속유출+h6h24동반재악화는조기픽붕괴패턴재확인이라다음회차추가악화시편출재검토 · 2026-08-26T19:05:00Z
- **재점화 3종 h6냉각 상세(관성vs실제지속 판별)**: PRINTER 유동성$519,846→$495,589(-4.7%,풀나이11.7일), h6+14.19%→-40.37%(재음전), h24+73.24%→+59.7%(4회차연속양전이나감속확대). JUGGERNAUT 유동성$499,292→$463,151(-7.2%,유출전환,풀나이66.8일), h6+48.45%→-23.22%(대폭반전), h24+61.88%→+34.48%(감속). HOOKR 유동성$518,424→$499,815(-3.6%,유출전환,풀나이20.6일), h6+31.47%→-10.41%(재음전), h24+52.35%→+37.7%(감속). 세토큰모두유동성유출전환+h6가h24보다먼저재음전해, h24양전은잔존모멘텀(관성)일가능성이높고h6가실제방향전환의선행신호로판단. 대조적으로 PANTS는유동성+13.2%유입에h6+10.8%·h24+37.44%로동반양전이라관성이아닌실질강세지속으로판단 · 2026-08-26T19:05:00Z
- **급락지속 상세**: CYBERLEEK 유동성$1,285,983→$1,268,587(-1.4%,풀나이10.9일), h6-38.6%→-43.12%, h24-38.57%→-41.73%, 회전율10.26배→11.01배(추가급등,진짜하락정황유지). CONK 유동성$64,195→$61,212(-4.6%,풀나이5.1일), h6-17.95%→-24.23%, h24-12.15%→-53.75%(급락심화). swappy 유동성$189,104→$164,378(-13.1%,목록최대유출,풀나이22.0일), h6-4.92%→-28.47%, h24+17.46%→-5.46%(재음전,대폭반전) · 2026-08-26T19:05:00Z
- **CEX 맥락**: 같은시각CEX선물은ETH·SOL·BNB가플러스로전환됐으나전체중앙값은-1.50%로여전히마이너스(XRP-2.34%) — 반등이메이저에국한. 온체인에서도TRUTH·GOOD의극단적개별급등과CYBERLEEK·CONK·MANEKI등광범위하락이동시공존해, CEX·온체인양쪽모두'선별적강세vs전반적약세'라는같은양극화패턴 · 2026-08-26T19:05:00Z
- **나머지 상세**: PEPECOIN대폭개선(유입,h6재양전,🔴→🟡,풀나이17.1일). MAPLE h1재양전유입전환(풀나이5.4일). CLOCKIN혼조(풀고정확인,풀나이미확인). TIPANSEM h6재양전h24가속(풀나이6.2일). LIZARD h1재양전(풀나이4.8일). CLUG h1h6재양전(풀나이7.7일). FLUSH h1재양전(풀나이4.8일). PEE안정h24가속(풀나이7.9일). 40M전지표대체로음전(풀나이5.0일). MANEKI h1대폭재양전h6큰폭개선(풀나이6.1일). CYBERCAT유입전환h24여전히극단(풀나이3.2일). omo손익분기근접(풀나이16.6일). CC64회차째휩소지속(풀나이14.7일). Z500여전히음전(풀나이9.1일). KIRK전지표재양전전환(🔴→🟡,풀나이6.3일). CHUMP혼조지속(풀나이26.7일). PROLOGUE전지표개선유입동반(🔴→🟡,풀나이9.1일). Dinger h24가속양전(풀나이3.7일). BRODIE유입반전전지표개선(풀나이43.7일). Dealer여전히음전(풀나이20.9일). lickingcat여전히음전(풀나이18.3일). TOAD약세전환경계(풀나이18.2일). FWA전지표개선208회차달성(풀나이41.1일). DPG여전히극단(풀나이14.2일). BULLSHIT손익분기부근(풀나이9.0일). PITCOIN h24대폭가속(풀나이14.1일). CALLOOOR유출전환큰폭감속(풀나이14.0일). PANTS전지표양전전환강세지속(🔴→🟡,풀나이7.4일). Doge2큰폭개선(풀나이4.6일). Truth Coin전지표개선극저유동지속(풀나이4.2일). BARRON안정(풀나이583.7일,목록최고령). YOMOGI h24여전히극단(풀나이3.8일). CATE h1h6재음전전환(풀나이31.1일) · 2026-08-26T19:05:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음(X 접근불가)**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant 보도(carryover 유지, 신규 없음)**.
- **나머지 39종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 부모가 계측·확정한 43개 활성종목 표 인용에 집중했고, 개별 KOL 검색·X 직접 조회는 로그인월 문제로 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님). WebSearch로 GeckoTerminal/Robinhood Chain 신규 트렌딩 후보를 탐색했으나 CA가 검증 가능한 신규 구체 후보는 발견하지 못했다(정직표기, 추가 없음).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 17:05Z)로부터 **정상 2시간** 경과, 유실 없음.
- **⚠️ 산출물 결함 3건 정정(검증 과정에서 발견)**: ①`watch.json` tokens에서 CALLOOOR·PRINTER 2종이 누락돼 있던 것을 복구값(chain/CA/stage/risk)으로 채워 43종으로 복원 ②`watch.csv`에서 열 개수가 어긋났던 4개 행(JUGGERNAUT·PRINTER·FWA·TRUTH)을 쉼표 포함 값 전량 큰따옴표 처리로 정정해 전 행 정확히 8열로 통일 ③풀나이 37건이 직전 회차 값으로 이월돼 있던 것을 부모 계측값으로 세 파일 전부 교체(가장 큰 오차는 CYBERLEEK 14.6일→10.9일). 아울러 CYBERLEEK·GOOD·TRUTH는 이번 회차 원래 서사에 풀나이가 누락돼 있었던 것도 함께 보완했다.
- **저장 후 세 파일(json·csv·md) 종목 목록 대조**: tokens(json) 43종·csv 43행(헤더 제외)·md 3개 표(조기13+확산9+뒷북21=43) 전부 일치 확인함. notable(json) 79건(이번 회차 신규·변경 없음, 전량 carryover).
- **⭐⭐⭐TRUTH 전면 반전(이번 회차 최대 이슈)**: 3회차 연속 유동성 불변+초고회전율이라는 워시트레이딩 의심 서사가 이번 회차 완전히 뒤집혔다. 실유입(+40.9%)과 회전율 붕괴(4분의1)는 워시트레이딩과 정반대 방향이며, 부모가 동일 풀·실제 매수/매도 건수까지 직접 재확인해 진위를 뒷받침했다. 다만 신생 풀에서의 극단적 가격 변동은 그 자체로 고위험이므로 성격 재평가와 별개로 리스크 표기는 유지한다.
- **⚠️⚠️1B 편출 판정 근거**: 유동성이 목록 내 처음으로 $20K선 밑으로 내려갔으나, 이 목록의 실제 편출 관행은 단순 threshold 붕괴가 아니라 h24 -90%대의 사실상 완전소멸 수준에서만 적용돼 왔다(CATALORIAN·BABYSHIB 등 선례). 따라서 이번 회차엔 편출하지 않되, 2회차 연속 유출+h6·h24 동반 악화 추세를 다음 회차에서 면밀히 재검토한다.
- **h6·h24 괴리로 재점화 진위 판별**: 이번 회차부터 재점화 종목의 h24(24시간 누적 모멘텀)와 h6(최근 6시간 방향)를 명시적으로 대조해, h24가 양전이어도 h6가 재음전하면 '관성'으로, h6·h24가 동반 양전이면 '실질 지속'으로 구분해 기록했다. PRINTER·JUGGERNAUT·HOOKR은 전자, PANTS는 후자로 판정.
- **$20K 미만 9종은 편출 트리거 미충족 지속**: Dinger·YOMOGI·TIPANSEM·FLUSH·PEPECOIN·CYBERCAT·40M·Truth Coin·PEE, 신규로 1B 추가. 전부 CATALORIAN 수준의 '사실상 완전소멸' 트리거에 크게 못 미쳐 편출을 적용하지 않았다.
- **CEX 선물시장 맥락 참고**: 같은 시각 CEX 선물이 ETH·SOL·BNB 플러스 전환에도 전체 중앙값 -1.50%(XRP -2.34%)로 반등이 메이저에 국한됐고, 온체인에서도 TRUTH·GOOD의 개별 급등과 광범위 하락이 공존하는 동일한 양극화 패턴이 관찰됐다.
- **데이터 신뢰도**: 이번 회차도 부모 세션이 DexScreener를 직접 조회해 계측한 43개 활성종목 표(풀 고정 방식, 풀교체 0건)를 1차 근거로 그대로 인용했다(재추정 없음). TRUTH·GOOD은 부모가 추가로 직접 재확인한 풀 데이터(유동성·매수매도건수)까지 인용해 신뢰도를 보강했다. CLOCKIN 풀나이는 DexScreener 데이터 부재로 '미확인' 표기(추정 안 함), TRUTH h1도 마찬가지로 '미제공' 정직 표기. WebSearch로 신규 트렌딩 후보(GeckoTerminal Solana·DexScreener Robinhood Chain)를 탐색했으나 CA 검증 가능한 구체 신규 후보는 없어 추가하지 않았다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·DexScreener(부모계측·풀고정방식)/GeckoTerminal/CoinGecko/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아니다. 재실행 시 갱신.*
