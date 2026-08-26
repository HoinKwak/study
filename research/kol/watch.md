# 온체인 트렌딩 조기경보 — 2026-08-26 13:05 UTC (KST 2026-08-26 22:05)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 11:00Z)로부터 **정상 2시간 5분** 경과. 유실 없이 정상 진행됐다.

## ⚠️ 이번 회차 데이터 경위: 풀선정 기준 결함 발견·교정

부모 세션이 처음 계측한 표(13:05Z, "유동성$5K이상 중 회전율 최고 풀" 기준)를 최초 인용해 갱신한 결과, 13개 종목에서 유동성이 직전 회차 대비 50~99% 급변하는 것으로 나타나 "풀전환"으로 잠정 플래그를 달았다. 그러나 **부모가 이 결함을 직접 규명**했다 — 회전율(vol24/liq) 비율 기준이 소형 풀을 선택해 직전 회차가 추적하던 풀과 달라진 것이었다(예: CLOCKIN은 실제로는 유동성 $178,875짜리 정상 풀을 계속 추적 중인데, 비율 기준이 $9,894짜리 별개 풀을 잘못 골랐다). **PANTS 교훈("최대 유동성만 보지 말고 거래량을 함께 볼 것")을 "회전율 비율"로 잘못 구현한 것이 원인**이었다.

부모가 기준을 **"유동성 $5K 이상 중 절대 24h 거래량 최대"**로 교정해 13:45Z에 전량 재계측했고, 이 문서는 그 교정 표를 인용해 갱신한다(ts는 회차 정의상 13:05Z로 유지). **재계측 결과 13개 종목 전부 직전 회차와 동일한 풀로 시계열이 복원됐다** — 즉 실제 유출입이 아니라 순전히 방법론 버그였음이 확정됐다. 이전 초안에 달았던 "⚠️풀선정변경" 플래그는 전량 제거했다.

**교정에 따른 판단 변경 3건**:
- **CONK·BULLSHIT**: 최초(오류) 데이터로 h24가 재음전/재붕괴한 것으로 오독했으나, 교정 데이터에서는 둘 다 **h24가 거의 변동 없이 양전 유지**임이 확인됐다. risk를 🔴→🟡로 되돌렸다.
- **PRINTER·JUGGERNAUT의 h24 재점화 폭**: 오류 데이터에서 각각 +184%·+102%로 계산됐으나 교정 후 **+105%·+78.71%**로 정정됐다(재점화 방향 자체는 유지).
- **Dealer·CLOCKIN의 "$20K 미만" 판정**: 오류 데이터의 산물이었고, 교정 후 유동성이 각각 $78,943·$178,875로 확인돼 판정 근거가 완전히 사라졌다(원래도 편출을 보류했던 판단이 옳았음이 확정).
- **풀나이 정정 7건**: JUGGERNAUT 47.7일→**66.6일**, BRODIE 11.4일→**43.5일**, FWA 17.8일→**40.8일**, HOOKR 2.3일→**20.4일**, Dealer 16.3일→**20.6일**, CATE 21.8일→**30.9일**, CYBERLEEK 3.6일→**10.7일**.
- **CLOCKIN 풀나이**: DexScreener가 `pairCreatedAt`을 제공하지 않아 **미확인**으로 정직 표기(추정하지 않음).

## 이번 회차 핵심 발견

- **TRUTH — 유동성 불변인데 h24 -88.99%, 회전율 75.93배(목록최고)**: 유동성은 $75,038.45→$74,418(-0.8%, 거의불변)인데 h24는 -71.54%→-88.99%로 대폭 추가악화됐다(교정 후에도 결론 유지). 유동성이 빠지지 않았는데 회전율만 극단적으로 높다는 것은 **유동성이탈이 아니라 초고빈도 거래(워시트레이딩 의심) 패턴**임을 재확인했다. risk 🔴 유지, 신규진입 절대금지.
- **CATALORIAN — 편출 판정 유지**: 유동성 $7,020.34→$6,295(-10.3%, $20K 미만), h24 -91.27%→-93.04%로 31회차째 "거의 완전소멸" 상태가 지속·악화됐다(교정 표와 무관한 독립 판정). 편출·notable 이관을 유지한다.
- **PRINTER — h24 +105%(정정), h6 +25.83%, 재점화**: 교정재계측으로 직전 회차와 동일 풀임을 확인, h6·h24가 동시에 큰 폭 가속했다(직전회차 h24 +52.37%에서 추가 가속, 오류 초안의 +184%는 정정).
- **JUGGERNAUT — h24 +78.71%(정정), h6 +63.27%, 66.6일 된 풀에서 재점화**: 풀나이가 66.6일(2026-06-20 생성)로 정정됐다. 187회차 장기추적 이력과 일치. KOL 코로보(Drallio)는 carryover 유지, 이번 회차 신규 코로보는 확인하지 못함(X 접근 불가).
- **MANEKI — h1 -25.29%, h6 -50.54%, h24 -60.87% 전방위 급락 확정(교정 후에도 결론 유지)**: 조기 픽이었으나 이번 회차 전방위로 급락했다. risk를 🟡→🔴로 강화, 신규진입 절대금지로 전환했다.
- **OBS·1B·CALLOOOR — 교정 후 훨씬 강한 양전 반전**: OBS(h24 -15.45%→+22.44%), 1B(h24 -23.73%→+26.60%), CALLOOOR(h24 -16.10%→+10.81%)가 전지표 강한 양전으로 확인됐다. TIPANSEM도 h1 -15.33%→+18.48%로 대폭 재양전했다.
- **유동성 $20K 미만 판정(교정 후)**: **CATALORIAN($6,295)** → **편출 유지**(31회차, 실질 붕괴). **Truth Coin($7,538)·PEE($7,446)·40M($9,098)** → 동일 풀 기준 장기간(39~88회차) 지속된 저유동 토큰으로 신규 붕괴 트리거가 없어 **편출 미적용**. **Dealer·CLOCKIN은 교정 후 각각 $78,943·$178,875로 20K를 크게 상회해 이 판정 대상에서 제외**된다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 53회차. ⭐전지표강한양전전환(교정재계측) | 유동성$125,842(+22.2%), h24+22.44% | 지속(52회차)·강한양전전환 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 미확인 | 61회차. 유출지속,h24재악화 | 유동성$12,352(-7.5%), h24-45.25% | 지속(60회차)·h24재악화 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 47회차. ⚠️h24손익분기재붕괴(대폭반전) | 유동성$29,732(-2.5%), h24-12.93% | 지속(46회차)·재음전 | 🔴 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain(Uniswap) | 없음(자체서사) | 71회차. 교정후직전회차와동일풀확인,h24개선 | 유동성$178,875(-3.9%), h24-12.92%, 풀나이미확인 | 지속(70회차)·동일풀확인 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 59회차. h1대폭재양전,h24는감속(양전유지) | 유동성$14,171(-3.1%), h24+31.62% | 지속(58회차)·h1대폭재양전 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 42회차. h24악화 | 유동성$29,185(-9.0%), h24-17.74% | 지속(41회차)·예측신뢰도낮음 | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 51회차. ⭐전지표강한양전전환(교정재계측) | 유동성$27,187(+25.9%), h24+26.60% | 지속(50회차)·강한양전전환 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 83회차. 전지표동시악화 | 유동성$23,230(-5.2%), h24-40.52% | 지속(82회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 49회차. 전지표동시재음전 | 유동성$14,220(-10.4%), h24-53.34% | 지속(48회차)·악화확대 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 88회차. 7회연속고정값탈피지속,h24개선 | 유동성$7,446(+3.1%), h24-5.66% | 지속(87회차)·데이터정체해소 | 🟡 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 46회차. 전지표음전 | 유동성$9,098(-8.4%), h24-30.78% | 지속(45회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 35회차. ⚠️전방위급락확정(조기픽결과정직기록,교정후도유지) | 유동성$25,415(-34.2%), h24-60.87% | 지속(34회차)·급락확정 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 32회차. h24여전히극단악화 | 유동성$11,723(-3.3%), h24-67.57% | 지속(31회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (9종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 35회차. 교정후직전회차와동일풀확인,h24악화 | 유동성$95,909(-3.7%), h24-10.59% | 지속(34회차)·동일풀확인 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 64회차. ⚠️h24재음전(대폭반전) | 유동성$180,520(-7.2%), h24-2.17% | 지속(63회차)·재음전 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium) | 미확인 | 63회차. 교정후직전회차와동일풀확인,h24연속음전 | 유동성$1,580,475(-2.6%), h24-5.34% | 지속(62회차)·동일풀확인 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 61회차째방향번복. h24개선 | 유동성$239,248(+0.5%), h24-17.34% | 지속(60회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 54회차. 교정후직전회차와동일풀확인,h24악화 | 유동성$70,186(-5.1%), h24-24.24% | 지속(53회차)·동일풀확인 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 51회차. h24감속(양전유지) | 유동성$79,748(-0.8%), h24+5.96% | 지속(50회차)·감속양전유지 | 🟡 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 48회차. ⚠️정정: h24는재음전아닌유사(양전유지) | 유동성$74,922(+5.2%), h24+9.64% | 지속(47회차)·정정 | 🟡 | [DexScreener](https://dexscreener.com/solana/DShht9B8wCRe5t3oqdPB77PnjJbKxbYaZyuWpZQjbonk) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 39회차. 여전히h24음전 | 유동성$360,244(+0.3%), h24-3.59% | 지속(38회차)·음전유지 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 31회차. ⭐h24대폭가속(양전유지) | 유동성$269,751(+1.2%), h24+43.68% | 지속(30회차)·h24대폭가속 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 37회차. ⚠️h24추가악화,유동성불변+초고회전(75.93배)=워시트레이딩의심(교정후도유지) | 유동성$74,418(-0.8%), h24-88.99% | 지속(36회차)·워시트레이딩의심강화 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap,Schrödinger) | 미확인 | 36회차. h24거의손익분기(대폭개선,'돌파'아닌'근접'으로정정) | 유동성$20,018(-2.0%), h24+0.01% | 지속(35회차)·거의손익분기 | 🟡 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 66회차. 교정후직전회차와동일풀확인,⭐전지표양전전환 | 유동성$514,449(+13.7%), h24+46.45% | 지속(65회차)·양전전환확인 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 188회차. ⭐h24대폭재점화(교정치+78.71%),풀나이66.6일로정정 | 유동성$452,297(-7.6%), h24+78.71% | 지속(187회차)·재점화(정정) | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 164회차. ⚠️전지표재음전(1회차만에재반전),풀나이43.5일로정정 | 유동성$211,845(-4.5%), h24-8.08% | 지속(163회차)·whipsaw재확인 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 67회차. h24개선(거의손익분기) | 유동성$508,089(-4.1%), h24-0.64% | 지속(66회차)·거의손익분기 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 미확인 | 202회차. ⭐⭐h24대폭재점화(교정치+105%) | 유동성$535,482(+8.5%), h24+105% | 지속(201회차)·재점화(정정) | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 193회차. 교정후직전회차와동일풀확인($20K미만서술철회) | 유동성$78,943(-4.5%), h24-17.57% | 지속(192회차)·정정 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 193회차. 여전히전량음전 | 유동성$38,105(-2.5%), h24-37.37% | 지속(192회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 151회차. ⭐전지표강한양전전환(교정재계측) | 유동성$72,077(+8.9%), h24+10.81% | 지속(150회차)·강한개선흐름 | 🟡 | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 201회차. 교정후직전회차와동일풀확인,약보합 | 유동성$343,664(-0.7%), h24-10.87% | 지속(200회차)·동일풀확인 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 205회차. 교정후직전회차와동일풀확인,풀나이40.8일로정정 | 유동성$1,080,697(-3.5%), h24-26.23% | 지속(204회차)·동일풀확인·205회차달성 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 153회차. h24여전히극단악화 | 유동성$38,843(+3.9%), h24-34.22% | 지속(152회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap) | 미확인(WebSearch보도없음) | 82회차. ⚠️정정: h24는손익분기재붕괴아닌유사(양전유지) | 유동성$237,199(-1.1%), h24+0.99% | 지속(81회차)·정정 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 155회차. h24대폭감속(여전히양전,정점통과경계) | 유동성$48,778(-21.3%), h24+38.83% | 지속(154회차)·감속 | 🔴 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap,dogwifpants) | 미확인 | 53회차. h24악화(여전히음전) | 유동성$78,644(-1.8%), h24-17.27% | 지속(52회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 46회차. h24여전히악화 | 유동성$52,501(-9.0%), h24-50.56% | 지속(45회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 40회차. h24악화 | 유동성$7,538(-4.8%), h24-10.71% | 지속(39회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 39회차. 소폭악화,저회전율·고령풀 | 유동성$210,357(-2.1%), 회전율0.06배(최저), h24-5.56% | 지속(38회차)·소폭악화 | 🟡 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 38회차. 전지표혼조·악화지속 | 유동성$15,725(-15.9%), h24-55.17% | 지속(37회차)·악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |
| **CATE** | Solana(PumpSwap) | 미확인 | 125회차달성. 교정후직전회차와동일풀확인,h24악화 | 유동성$2,199,417(-2.2%), h24-15.66% | 지속(124회차)·동일풀확인 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |

> **편입/편출/강등/재승격 요약(이번 회차)**: **신규편입 0건**. **편출 1건(CATALORIAN — 31회차간 거의완전소멸 지속·악화, $20K미만+h24-93%, 교정과무관한독립판정)**. **강등**: MANEKI(🟡→🔴,전방위급락확정). **재승격**: HOOKR(🔴→🟡,실제전지표양전전환확인). **정정(강화→완화)**: CONK·BULLSHIT(🔴→🟡, 최초오류데이터의재음전/재붕괴는오독이었고실제로는h24거의불변). 활성목록 **44→43종**(CATALORIAN 편출, 조기13/확산9/뒷북21). notable **78→79개**(신규: CATALORIAN 1건). **핵심 이벤트**: ⚠️부모의풀선정기준결함(회전율비율→절대거래량으로교정)발견·교정, 13개종목풀시계열복원(실제유출입아님확정), TRUTH유동성불변+회전율75.93배(워시트레이딩의심 재확인), CATALORIAN편출, PRINTER·JUGGERNAUT h24대폭재점화(수치정정), MANEKI전방위급락확정, OBS·1B·CALLOOOR강한양전반전.

## 온체인 신호 상세

- **풀선정 기준 결함·교정 경위**: 최초(13:05Z) 표는 "유동성$5K이상 중 회전율(vol24/liq) 최고" 기준을 썼는데, 이 비율 기준이 다수 페어 보유 종목에서 소형 풀을 선택해 직전 회차 추적 풀과 달라졌다. 부모가 이를 규명하고 "유동성$5K이상 중 절대 24h 거래량 최대" 기준으로 13:45Z 재계측했다(ts는 회차 정의상 13:05Z 유지). 재계측 결과 이전에 "풀전환"으로 의심됐던 13종(OBS·CLOCKIN·omo·CYBERLEEK·Z500·HOOKR·JUGGERNAUT·BRODIE·PRINTER·Dealer·TOAD·FWA·CATE) 전부 직전 회차와 동일한 풀임이 확인됐다 · 2026-08-26T13:45:00Z(재계측 시점) / 회차ts 2026-08-26T13:05:00Z
- **TRUTH 상세**: 유동성$75,038.45→$74,418(-0.8%,거의불변), h1+0.87%→-0.66%, h6+0.46%→+0.12%, h24-71.54%→-88.99%(추가악화). 회전율75.93배(목록최고). 유동성이 빠지지 않았는데 회전율만 극단적인 것은 유출이 아니라 초고빈도 워시트레이딩 패턴 시사(교정후에도결론유지). 풀나이3.9일(2026-08-22생성) · 2026-08-26T13:05:00Z
- **CATALORIAN(편출) 상세**: 유동성$7,020.34→$6,295(-10.3%), h24-91.27%→-93.04%. 31회차간 "여전히 거의 완전소멸"로 기록된 끝에 실질 붕괴가 지속·악화 확인돼 편출(이판정은교정표와무관). 회전율14.55배,풀나이3.1일(2026-08-23생성) · 2026-08-26T13:05:00Z
- **MANEKI 상세**: 유동성$38,604.41→$25,415(-34.2%), h1+9.59%→-25.29%, h6-3.98%→-50.54%, h24-16.40%→-60.87%. 조기 픽으로 추적했으나 전방위 급락 확정(교정후에도동일결론), 조기신호가 결실 맺지 못하고 반대방향으로 실현된 사례로 기록. risk 🟡→🔴 강화 · 2026-08-26T13:05:00Z
- **PRINTER·JUGGERNAUT 재점화 상세(정정치)**: PRINTER는 교정재계측으로 직전 회차와 동일 풀임을 확인, h6+25.83%·h24+105%(직전+52.37%대비가속, 최초오류초안의+184%는정정됨, 풀나이11.4일/2026-08-15생성). JUGGERNAUT도 동일 풀 확인, h6+63.27%·h24+78.71%(최초오류초안의+102%는정정됨, 풀나이66.6일/2026-06-20생성,187회차장기추적과일치). 둘 다 "뒷북" 단계에서의 재점화로, 바닥신호 여부는 whipsaw 이력상 단정하지 않음 · 2026-08-26T13:05:00Z
- **CONK·BULLSHIT 정정 상세**: CONK는 h24+9.60%→+9.64%(사실상불변,양전유지), BULLSHIT은 h24+1.01%→+0.99%(사실상불변,양전유지) — 둘 다 최초 오류 데이터에서 h24가 재음전/재붕괴한 것으로 오독했으나 실제로는 거의 변동이 없었다. risk를 각각 🔴→🟡로 정정 · 2026-08-26T13:05:00Z
- **나머지 상세**: PEPECOIN h24재악화. MAPLE h24손익분기재붕괴. LIZARD악화. CLUG전지표악화. FLUSH전지표재음전. PEE 7회연속고정탈피지속후h24개선. 40M전지표음전. CYBERCAT h24여전히극단악화. omo h24악화(동일풀확인). swappy h24재음전(대폭반전). CYBERLEEK h24연속음전(동일풀확인). CC워시트레이딩의심불변. Z500 h24악화(동일풀확인). KIRK h24감속양전유지. CHUMP여전히h24음전. PROLOGUE h24대폭가속. Dinger h24거의손익분기. GOOD h24거의손익분기. lickingcat여전히전량음전. TOAD약보합(동일풀확인). DPG여전히극단악화. PITCOIN h24대폭감속·정점통과경계. PANTS h24악화. Doge2여전히악화. Truth Coin h24악화. BARRON소폭악화. YOMOGI전지표혼조·악화지속. CATE h24악화(동일풀확인) · 2026-08-26T13:05:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음(X 접근불가)**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant 보도(carryover 유지, 신규 없음)**.
- **나머지 39종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 부모가 계측·교정한 43개 활성종목 표 인용에 집중했고, 개별 KOL 검색·X 직접 조회는 로그인월 문제로 시도하지 않았다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전 기록 회차(2026-08-26 11:00Z)로부터 **정상 2시간 5분** 경과, 유실 없음.
- **저장 후 세 파일(json·csv·md) 종목 목록 대조**: tokens(json) 43종·csv 43행(헤더 제외)·md 3개 표(조기13+확산9+뒷북21=43) 전부 일치 확인함. notable(json) 79건(신규 1건: CATALORIAN 편출).
- **⚠️⚠️풀선정 기준 결함·교정(이번 회차 최대 이슈)**: 최초 계측(13:05Z)이 쓴 "유동성$5K이상 중 회전율 최고" 기준이 소형 풀을 선택해 13개 종목의 시계열이 실제 유출입 없이 불연속으로 보였다. 부모가 원인을 규명하고 "유동성$5K이상 중 절대 24h 거래량 최대"로 13:45Z 교정 재계측했으며, 재계측 결과 13종 전부 직전 회차와 동일 풀로 시계열이 복원됐다. **다음 회차부터는 교정된 절대거래량 기준이 계속 안정적으로 동일 풀을 선택하는지 지켜볼 필요가 있다.**
- **정정 2건(강등→재평가)**: CONK·BULLSHIT은 최초 오류 데이터로 h24 재음전/재붕괴로 잘못 판단했으나, 교정 데이터에서는 h24가 거의 변동 없이 양전 유지임이 확인돼 risk를 🔴→🟡로 되돌렸다. PRINTER·JUGGERNAUT의 h24 재점화 폭도 정정됐다(+184%→+105%, +102%→+78.71%).
- **CATALORIAN 편출은 교정과 무관하게 유효**: 31회차간 관찰한 "거의 완전소멸" 토큰이 이번 회차 실질 악화(h24-93.04%, 유동성$20K미만)까지 확인돼 편출했다. 이 데이터는 교정 표에 포함되지 않은 독립 판정이다.
- **TRUTH의 유동성불변+초고회전율(75.93배, 목록최고) 조합은 교정 후에도 워시트레이딩 의심을 뒷받침하는 근거로 유지된다.** h24가 -88.99%까지 악화됐음에도 유동성이 거의 그대로인 것은 전형적인 세탁거래·조작 아티팩트 패턴이다.
- **데이터 신뢰도**: 이번 회차는 부모 세션이 DexScreener를 직접 조회해 계측·교정한 43개 활성종목 표를 1차 근거로 그대로 인용했다(재추정 없음). 풀 선정 기준 결함을 부모가 스스로 발견·투명하게 교정한 사례로, 방법론 오류 발견 시 정직하게 정정하는 절차가 작동했다. CLOCKIN 풀나이는 DexScreener 데이터 부재로 '미확인' 표기(추정 안 함). X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·DexScreener(부모계측·교정재계측)/GeckoTerminal/CoinGecko/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
