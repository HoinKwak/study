# 온체인 트렌딩 조기경보 — 2026-08-23 15:00 UTC (KST 2026-08-24 00:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-23 13:00Z)로부터 정확히 2시간 경과**(정상 간격). 42개 활성종목 전부를 DexScreener 토큰 API(체인별/소규모 배치조회)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 스캔으로 신규 발굴 및 교차검증을 진행했다.

> **⚠️이번 회차 데이터 이슈(심화)**: DexScreener 배치조회에서 처음 시도한 14개 단위 배치 2건이 각각 6~7개 토큰을 누락하는 큰 폭의 누락률을 보였다(응답 페이로드가 커질수록 누락이 심해지는 것으로 추정). 규칙대로 누락분(총 13개 토큰)을 4~5개 단위 소규모 배치로 재조회해 42개 전부를 확보했다. 이번 회차부터 큰 배치(14개)는 신뢰도가 낮다고 판단해 **다음 회차부터 배치 크기를 5개 이하로 낮추는 것을 권고**한다. CATE·BULLSHIT는 다수풀 재대조 결과 초기 추출값이 최대풀이 아니었음을 발견해 정정했다(아래 상세 참조).

> **편입/편출/강등 내역**: **신규편입 0건**(BABYCATE의 실제 CA를 이번 회차 raw데이터로 확정했으나 h6가 이미 음전전환해 편입은 보류). **강등 0건**. **편출 0건**. 활성목록 **42종 유지**. notable **29개 유지**(BABYCATE CA 정정, TRUTH(RH,0xa48a…) 완전소멸 재확증 등 갱신).

## ⚠️ 부모 세션 요청 최우선 확인 — TRUTH

**TRUTH(Robinhood Chain, CA `0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4`)**: 3회 연속 관측[13:00Z/13:20Z(부모 교차검증)/15:00Z]을 종합하면 다음과 같다.

| 시점 | 유동성 | h1 | h6 | 회전율 |
|---|---|---|---|---|
| 13:00Z(에이전트) | $77,580.74 | +87.21% | -82.74% | 279.6배 |
| 13:20Z(부모 교차검증) | $62,286 | +28.71% | -77.15% | 350.5배 |
| **15:00Z(이번 회차)** | **$75,831.23** | **+3.79%** | **+76.63%** | **≈300.1배** |

**결론**: 유동성이 $62K~$90K 박스권을 오가며 **단조 붕괴는 아니었다** — 13:20Z에 급락했다가 15:00Z에 다시 13:00Z 수준 가까이 반등했다. h6는 -82.74%→-77.15%→**+76.63%**로 음전에서 강한 양전으로 재반전했고, h1은 +87.21%→+28.71%→+3.79%로 변동성이 점차 완화되는 모양새다. GeckoTerminal 로빈후드체인 트렌딩 9위(h24 +2076.52%)로 재확인해 DexScreener 값과 대체로 일치한다.

**⚠️중요 발견 — 오독 정정**: 이번 회차 GT 트렌딩에서 `Truth Coin/WETH`(0x4894913...)라는 별도 풀이 15위로 재노출됐는데, WebFetch 요약이 이를 reserve **"$76.82K"**로 표기했다. 이는 완전소멸이 확정된 동명 계열 **Truth Coin(RH, CA `0xa48a…b4`)**의 풀 주소와 일치해 "혹시 부활했나"라는 의심이 들었으나, **DexScreener pairs API로 raw JSON을 직접 재확인한 결과 실제 유동성은 $76.95(달러 단위)였다** — WebFetch가 자릿수를 잘못 읽어 "K"를 붙인 데이터추출 오류였다. 이 토큰은 여전히 사실상 완전소멸 상태이며, 24h 거래량 $24.1M에 유동성 $76.95라는 극단적 조합은 워시트레이딩/조작 아티팩트로 해석하는 것이 타당하다. **TRUTH(0x2ec5…)와는 명백히 별개의 죽은 토큰**이며, 이번 회차 raw데이터 직접 대조로 완전소멸 판정이 재확증됐다(정직 정정 사례로 기록).

**종합 판단**: TRUTH(0x2ec5…)는 동명의 완전소멸 토큰과는 뚜렷이 다른 경로를 밟고 있으나, 회전율 300배대의 극단적 변동성이 3회차 연속 지속되고 있어 **안정적 회복으로 단정하기는 이르다**. 뒷북 단계·최상위 경계 유지, 신규진입 절대금지.

## 그 밖 추적 항목 갱신

- **LIZARD(10회차, 풀생성후약39.9시간)**: ⭐⭐**3회연속 유동성 유입, 전방위 개선 streak 지속**. 유동성 $39,670.96→**$41,320(+4.16%)**, h1(+10.26%→+0.77%, 감속하나 여전히 양), h6(+23.51%→**+37.78%**, 추가 강한 개선), h24(-36.85%→-35.39%, 유사). 6회 유출 종료 이후 3회차째 개선이 이어지며 37.9시간 시점의 전형적 쇠퇴경로에서 점차 벗어나는 신호로 해석할 수 있으나, 신생 토큰 특성상 신중한 판단을 유지한다.
- **omo(3회차, 풀생성후약13.5일)**: 직전 회차(2회차)에 나타났던 정점통과 경계신호가 **이번 회차 반전 개선**됐다. 유동성 $147,227.93→**$149,188(+1.3%, 유출→유입 반전)**, h1(-6.61%→-1.67%, 개선), h6(+43.55%→+36.7%, 소폭 감속하나 여전히 강세), h24(+88.18%→+94.93%, 재가속). **MANEKI와 다른 경로**를 보여 경계 수위를 완화한다(확산 단계 유지).
- **MANEKI(3회차, 풀생성후약70.2시간)**: ⚠️**2회연속 유동성 유출 + 전방위 악화로 정점통과 경계신호가 강화**됐다. 유동성 $48,827.99→**$46,338.84(-5.1%, 2회연속 유출)**, h1(+2.86%→-0.9%, 재음전), h6(+0.76%→-18.33%, 악화), h24(+129%→+61.26%, 대폭 감속). omo가 이번 회차 반전 개선한 것과 대조적으로 MANEKI는 지속 악화되고 있어 Dinger·WINNING·TRUTH·YOMOGI의 "신규편입 1~2회차 만의 정점통과" 패턴과 더욱 유사해졌다. 조기 단계 유지, 경계 최상위.
- **Dinger(4회차, 풀생성후약13.4시간)**: 부분 반전이 1회차 만에 다시 재악화됐다. 유동성 $61,175.67→**$52,912(-13.5%, 재유출)**, h1(+30.71%→-7.66%, 재음전), h6(-90.3%→-81.58%, 유사, 여전히 극심), h24(+938%→+675%, 감속). 회전율은 170.1배→**198.3배**로 상승. GT 재확인(솔라나 트렌딩 7위, h6-81.74%·h24+662.44%)으로 교차검증했다. 뒷북 단계 유지, 신규진입 절대금지.
- **WINNING(4회차, 풀생성후약19.9시간)**: ⚠️**4회연속 유동성 유출, 전방위 급격 악화**. 유동성 $84,990.05→**$59,603(-29.8%, 4회연속 유출·급격 심화)**, h1(+9.7%→**-56.73%**, 급반전 대폭악화), h6(-28.77%→-71.13%, 대폭악화), h24(+613%→+247%, 대폭감속). 회전율은 65.25배→**101.2배**로 대폭 상승. 정점통과 이후 전형적 붕괴 패턴이 더욱 뚜렷해졌다.
- **OBS(21회차, 풀생성후약43시간)**: 전방위 악화가 지속됐다. 유동성 $90,732.69→**$84,802.76(-6.5%, 유출전환)**, h1(-1.04%→**-17.87%**, 대폭악화), h6(-8.48%→-8.8%, 유사, 음전 지속), h24(+138%→+94.52%, 감속).

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

| 토큰 | 체인/DEX | 단계 | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|---|
| **LIZARD** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 10회차. 3회연속유동성유입,전방위개선streak지속 | 유동성$41,320(+4.16%), h24-35.39%, 회전율≈11배대 | 지속(10회차)·3회연속개선 | 🟢(개선지속) | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **CLUG** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 51회차. 전방위강한개선반전 | 유동성$44,618.65(+9.8%), h24+16.65%(양전환) | 지속(51회차)·강한개선반전 | 🟡(개선) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **CLOCKIN** | Robinhood Chain | 조기 | 없음(자체서사만확인) | 39회차. 전지표유사수준유지,h24소폭개선 | 유동성$190,778.01(+3.1%), h24-20.28% | 지속(39회차)·안정 | 🟡(안정) | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 27회차. 첫유출전환이나h6·h24는양호유지 | 유동성$16,353.76(-3.9%), h24+37.54% | 지속(27회차)·streak종료 | 🟡(streak종료) | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **MAPLE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 15회차. h1대폭개선,h6는재음전 | 유동성$24,798.15(+2.7%), h24-23.25% | 지속(15회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **PEE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 56회차. h1거래일부재개(소규모) | 유동성$7,739.49(+0.7%), 회전율≈0.41배 | 지속(56회차)·거래재개 | 🔴(극저유동) | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **FLUSH** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 17회차. 전방위소폭개선 | 유동성$34,024.66(-2.8%), h24-60.3% | 지속(17회차)·소폭개선 | 🔴(여전히깊은음전) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **OBS** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 21회차. 전방위악화지속 | 유동성$84,802.76(-6.5%), h24+94.52% | 지속(21회차)·악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **1B** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 19회차. 재유출전환,h6재악화 | 유동성$22,890.28(-7.4%), h24-81.81% | 지속(19회차)·혼조 | 🔴(고위험) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 조기 | 미확인(코로보없음) | 29회차. h24양전환이1회차만에재음전반전 | 유동성$22,126.96(-9.6%), h24-18.64% | 지속(29회차)·재음전반전 | 🔴(재음전) | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **40M** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 14회차. 전방위추가악화,반복반전이력지속 | 유동성$12,256.26(-15.6%), h24-84.95% | 지속(14회차)·추가악화 | 🔴(반복반전) | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 조기 | 미확인(코로보없음) | 3회차. 2회연속유출+전방위악화로경계강화 | 유동성$46,338.84(-5.1%), 회전율≈1.907배 | 지속(3회차)·경계최상위 | 🔴(정점통과가능성강화) | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **omo** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 3회차. 1회차경계신호가반전개선 | 유동성$149,188(+1.3%), 회전율≈17.15배 | 지속(3회차)·경계완화 | 🟡(경계완화) | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **CHUMP** | Robinhood Chain(Uniswap V3 1%) | 확산 | 미확인(코로보없음) | 7회차. h1반전개선,전지표안정 | 유동성$283,287.02(-1.0%), h24+91.79% | 지속(7회차)·h1반전개선 | 🟢(안정강세) | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **Z500** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 22회차. 전방위강한개선 | 유동성$86,403(+8.9%), h24-7.91% | 지속(22회차)·강한개선 | 🟢(개선) | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 확산 | 미확인(코로보없음) | 31회차. 장기가속streak가감속전환 | 유동성$1,813,826(-8.4%), h24+886%(감속) | 지속(31회차)·감속전환 | 🟡(감속경계) | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CONK** | Solana(Raydium) | 확산 | 미확인(코로보없음) | 16회차. h1반전,h6는재악화 | 유동성$89,257(+1.9%), h24-25.18% | 지속(16회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **KIRK** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 19회차. 전방위악화전환 | 유동성$74,872.92(-12.8%), h24-1.25% | 지속(19회차)·악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **swappy** | Robinhood Chain(Uniswap V4) | 확산 | 미확인(코로보없음) | 32회차. h1개선,h6재악화 | 유동성$195,604.4(-0.3%), h24-22.48% | 지속(32회차)·혼조악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CC** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 29회차째방향번복지속 | 유동성$218,263(+4.0%), h24+240% | 지속(29회차)·고위험 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **TRUTH** | Robinhood Chain(Uniswap V2) | 뒷북 | 미확인(코로보없음) | 5회차,풀생성24.0h전,3회연속관측박스권,GT로빈후드9위 | 유동성$75,831.23(반등), h6+76.63%(재반전양전), 회전율≈300.1배 | 지속(5회차)·극단변동최상위경계 | 🔴(최상위경계) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 4회차. 부분반전이1회차만에재악화 | 유동성$52,912(-13.5%), h6-81.58%, 회전율≈198.3배 | 지속(4회차)·재악화 | 🔴(재악화) | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **WINNING** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 4회차. 4회연속유출,급격악화 | 유동성$59,603(-29.8%), h1-56.73%, 회전율≈101.2배 | 지속(4회차)·정점통과확정심화 | 🔴(급격악화) | [DexScreener](https://dexscreener.com/solana/FW6R4QQeP4fzqRwDHbBkpjHx3ecvYwhd5g7chKg8pump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 뒷북 | 미확인(코로보없음) | 34회차. 유동성유사,h1재악화 | 유동성$238,759.12(유사), h24+11.65% | 지속(34회차)·재음전 | 🔴(재음전) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **CATE** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 93회차. 강한반전개선(다수풀재대조완료) | 유동성$1,958,244.72(+10.9%), h24-7.62%, 회전율≈27.3배 | 지속(93회차)·강한반전개선 | 🟢(반전개선) | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **GOOD** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 35회차. 장기개선streak가처음유출전환 | 유동성$456,097.89(-6.9%), h24-1.66% | 지속(35회차)·streak종료 | 🟡(streak종료) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 뒷북 | 미확인(코로보없음) | 170회차. 유사수준유지 | 유동성$338,917.57(-2.7%), h24-20.51% | 지속(170회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **BULLSHIT** | Solana(Meteora등10개풀) | 뒷북 | 미확인(WebSearch로토큰명특정보도없음) | 50회차. 유입지속,h6반전개선 | 유동성(PumpSwap)$228,005.57(+3.4%), h24-14.44% | 지속(50회차)·개선지속 | 🟢(개선지속) | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **TOAD** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 169회차. 강한개선이재음전전환 | 유동성$426,112.17(-2.2%), h24+12.29% | 지속(169회차)·streak종료 | 🟡(streak종료) | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **DPG** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 121회차. 대폭유출,h6대폭악화 | 유동성$79,742.19(-17.9%), h24-22.41% | 지속(121회차)·대폭유출 | 🔴(대폭유출) | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **FWA** | Ethereum(Uniswap V4) | 뒷북 | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover)+CG트렌딩12위(carryover) | 173회차. 전지표개선 | 유동성$1,166,961.74(+3.7%), h24+4.88% | 지속(173회차)·개선 | 🟢(개선) | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **CALLOOOR** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 119회차. 118회차연속가속streak종료 | 유동성$64,911.07(-6.0%), h24+15.47% | 지속(119회차)·streak종료 | 🟡(streak종료) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **JUGGERNAUT** | Robinhood Chain(Uniswap V3 1%) | 뒷북 | Drallio(약한코로보,carryover) | 156회차. 소폭전방위개선 | 유동성$268,867.91(+3.2%), h24+15.83% | 지속(156회차)·개선 | 🟢(개선) | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 132회차. 강한반전이1회차만에재음전 | 유동성$168,249.29(-1.05%), h24-3.47% | 지속(132회차)·재음전 | 🟡(재음전) | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **Dealer** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 161회차. 유출재개,전방위악화 | 유동성$114,083.81(-6.2%), h24-6% | 지속(161회차)·악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 161회차. 가속흐름이유지수준둔화 | 유동성$58,507.99(+0.6%), h24+2.47% | 지속(161회차)·대체로개선 | 🟢(개선) | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **PITCOIN** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 122회차. 유입지속,h1재음전 | 유동성$32,403.39(+3.5%), h24-0.8% | 지속(122회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 21회차(dogwifpants). 2회연속반등후조정 | 유동성$139,273.12(-6.7%), h24+22.72% | 지속(21회차)·조정 | 🟡(조정) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Doge2** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 14회차. 혼조지속,h1소폭개선 | 유동성$52,715.24(-3.7%), h24-29.49% | 지속(14회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 8회차,풀생성24.6h전,급반전악화지속심화 | 유동성$12,238.68(-12.4%), h24-85.54%, 회전율≈266.6배 | 지속(8회차)·악화심화 | 🔴(악화심화) | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 뒷북 | 미확인(코로보없음) | 7회차,풀나이19개월,고점통과지속 | 유동성$256,626.37(+1.4%), h24-20.82% | 지속(7회차) | 🔴(고점통과지속) | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 6회차,풀생성13.5h전,유출지속,h6대폭악화 | 유동성$32,886.75(-14.6%), h6-54.54%, 회전율≈260.6배 | 지속(6회차)·극단변동지속 | 🔴(극단변동지속) | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**(BABYCATE CA 확정했으나 h6음전전환으로 보류). **강등 0건**. **편출 0건**. **⭐강한개선**: LIZARD(3회연속개선), CLUG(강한반전개선), CATE(강한반전개선), Z500, CHUMP, JUGGERNAUT, BULLSHIT, FWA, lickingcat. **경계강화**: MANEKI(2회연속유출·정점통과가능성강화), WINNING(4회연속유출·급격악화), Dinger(재악화), Truth Coin(Sol)(악화심화), OBS·PEPECOIN·KIRK·swappy·CC·HOOKR·DPG·Dealer(재악화/악화전환). **경계완화**: omo(1회차경계신호반전개선).

## 온체인 신호 상세

- **TRUTH 3회연속관측 상세**: 위 스포트라이트 섹션 참조. 유동성$62K~$90K박스권, h6음전→양전재반전, 회전율300배대지속 · 2026-08-23T15:00:00Z
- **Truth Coin(RH,0xa48a…,완전소멸토큰) 재확증 상세**: GT WebFetch요약이 reserve"76.82"를 "$76.82K"로자릿수오독한것을 raw JSON재확인(유동성$76.95)으로적발·정정. 여전히완전소멸상태, 신규진입절대금지 · 2026-08-23T15:00:00Z
- **omo·MANEKI 경로분화 상세**: 신규편입2회차경계신호이후, omo는3회차에반전개선(유동성유입전환)한반면MANEKI는2회연속유출로악화지속. 동일패턴에서시작한두토큰이서로다른경로를보여준사례 · 2026-08-23T15:00:00Z
- **CATE·BULLSHIT 다수풀 재대조 상세**: 최초배치조회에서추출한값이최대유동성·최대거래량풀이아니었음을발견해개별재조회로정정(CATE: $895,730.55→$1,958,244.72(PumpSwap,실제최대유동성·최대거래량풀); BULLSHIT: Meteora최대유동성풀$316,786.47이있으나거래량은PumpSwap $228,005.57풀이더높아기존관행대로PumpSwap기준유지) · 2026-08-23T15:00:00Z
- **DexScreener 배치조회 누락 심화 상세**: 14개단위배치2건에서각각13개중10개,14개중8개만응답(합계13개토큰누락)돼4~5개단위소규모배치로전량재조회. 배치크기가클수록누락이심해지는패턴관찰 · 2026-08-23T15:00:00Z
- **나머지 33건 상세**: OBS전방위악화. PEPECOIN재음전반전. MAPLE혼조. CLOCKIN안정. TIPANSEM streak종료. 1B혼조. CLUG강한개선반전. FLUSH소폭개선. PEE거래일부재개. 40M추가악화. swappy혼조악화. CYBERLEEK감속전환. CC고위험. Z500강한개선. KIRK악화전환. CONK혼조. CHUMP h1반전개선. Dinger재악화. WINNING급격악화. HOOKR재음전. GOOD streak종료. PRINTER유지. BULLSHIT개선지속. TOAD streak종료. DPG대폭유출. FWA개선. CALLOOOR streak종료. JUGGERNAUT개선. BRODIE재음전. Dealer악화. lickingcat개선. PITCOIN혼조. PANTS조정. Doge2혼조. BARRON고점통과지속 · 2026-08-23T15:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **TRUTH — WebSearch("TRUTH token Robinhood Chain Uniswap pump today")로 KOL/뉴스 검색 시도, 특정 토큰 언급 확보 실패**. 로빈후드체인 인프라 관련 일반 기사만 검색됨(Uniswap Pools.trade 런치패드 등). TRUTH 개별 코로보는 이번 회차도 미확인(정상 상태, 결함 아님).
- **나머지 40종 — 코로보 미확인**: 이번 회차는 42개 활성종목 전량 재확인(다수풀 재대조 2건 포함)과 notable 다건 참고데이터 갱신, BABYCATE CA 정정에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-23 13:00Z)로부터 정확히 2시간 경과(정상 간격).
- **⭐⭐이번 회차 핵심 — TRUTH 3회연속관측·박스권 확인**: 부모 세션의 우려("완전소멸 경로 진행 중인가")에 대해, 유동성이 $62K~$90K 박스권을 오가는 극단적 변동을 3회 연속 보이며 **단조 붕괴는 아니었다**고 확인했다. 다만 회전율 300배대의 극단적 변동성이 지속돼 안정적 회복으로 단정하지 않는다.
- **⭐⭐데이터 무결성 catch — GT 자릿수 오독 적발·정정**: GT 트렌딩에서 완전소멸 확정 토큰(Truth Coin RH, 0xa48a…)의 풀이 reserve "$76.82K"로 표시돼 "부활했나"라는 의심이 들었으나, DexScreener raw JSON 직접 재확인으로 실제값이 $76.95임을 밝혀 오독을 정정했다. 규칙(raw JSON 직접확인)이 실제로 잘못된 서사 유입을 막은 사례.
- **CATE·BULLSHIT 다수풀 재대조**: CATE는 초기 배치조회값($895,730.55)이 최대풀이 아니었음을 발견해 실제 최대유동성·최대거래량 풀(PumpSwap, $1,958,244.72)로 정정했다. 규칙(수치를 가져온 풀과 dex 필드 일치 자체대조)이 실제 오차를 잡아낸 사례.
- **omo·MANEKI 경로분화**: 동일한 "신규편입 2회차 경계신호"에서 시작한 두 토큰이 3회차에 서로 다른 경로를 보였다 — omo는 반전개선, MANEKI는 지속악화. 이 워치의 반복패턴이 절대적이지 않음을 보여주는 사례로 기록한다.
- **BABYCATE CA 정정**: 직전 회차 WebSearch로 추정했던 CA 후보가 오답이었음을 이번 회차 raw데이터 대조로 확인·정정했다(정확한 CA: `DDVUsN8sDFxbaX6gNBoD44kjZhFETWJnwAn4EX1dpump`). 편입은 h6 음전전환으로 계속 보류.
- **DexScreener 배치조회 신뢰도 저하**: 이번 회차 14개 단위 배치 2건에서 심각한 누락(13개 중 최대 7개)이 발생해 다음 회차부터 배치 크기를 5개 이하로 낮추는 것을 권고한다.
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API로 42개 활성종목을 확보했으나 대형 배치의 누락률이 커 소규모 배치 재조회로 보완했다. TRUTH·CATE·BULLSHIT·BABYCATE 등 다수 항목에서 raw JSON 직접 대조로 실제 오류(오독·풀선정오류·CA오답)를 적발·정정한 점이 이번 회차의 데이터 무결성 측면 성과다. GeckoTerminal 솔라나·로빈후드체인 트렌딩(page=1)으로 신규 발굴·교차검증을 진행했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
