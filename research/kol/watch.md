# 온체인 트렌딩 조기경보 — 2026-08-23 09:00 UTC (KST 2026-08-23 18:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-23 07:00Z)로부터 정확히 2시간 경과**(정상 간격). 39개 활성종목 전부를 DexScreener 토큰 API(체인별 배치조회)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 스캔으로 신규 발굴을 진행했다.

> **⭐이번 회차 핵심 사건: Truth Coin(Robinhood Chain, CA `0xa48a…bb4`) 유동성 사실상 완전소멸 확정.** 부모세션 07:20Z 교차검증 당시 $824,205까지 치솟았던 유동성이, 이번 09:00Z 재조회에서 DexScreener($45.85)·GeckoTerminal($45.56) 두 독립 소스 모두 사실상 0으로 수렴했다(raw JSON 직접 확인, quote reserve 0.00947 WETH — WETH 사이드가 거의 전량 인출된 고전적 소진 패턴). **P400·HEREBRO·MOONCOIN에 이은 네 번째 급격소멸 확정 사례**로 notable로 편출한다.

> **편입/편출 내역**: **신규편입 2건** — Dinger(Solana, 확산), WINNING(Solana, 확산). **편출 1건** — Truth Coin(Robinhood Chain, 사실상완전소멸). **강등 2건** — TRUTH·YOMOGI가 확산에서 뒷북으로 강등(둘 다 이번 회차에 명백한 정점통과·붕괴 증거 확인). 활성목록 **39종→40종**. notable **24개→25개**.

## ⚠️ 부모 세션 요청 최우선 확인 — Truth Coin(RH), YOMOGI, LIZARD, OBS, Truth Coin(Solana), PANTS

- **Truth Coin(Robinhood Chain, CA `0xa48a…bb4`)**: 위 핵심 사건 참조. **notable로 편출.**
- **YOMOGI(3회차, 풀생성후약7.5시간)**: ⚠️**확산→뒷북 강등.** h6가 +816%→**-84.65%**로 급락해 6시간 윈도우 내에 이미 고점을 통과하고 붕괴가 진행 중임이 확정적으로 확인됐다. 유동성은 $47,090.41→$46,705.38(-0.82%, 유출 둔화)로 급감세는 멈췄으나, h1은 -32.12%→-5.69%로 단기 낙폭만 축소됐을 뿐 h6의 대폭 붕괴가 더 결정적이다. h24는 +477%→+456%(소폭 감속). 회전율은 174.2배→**178.3배**로 상승해 워시트레이딩이 지속된다. **P400·HEREBRO급 급속소멸 패턴이 상당 부분 진행됐다고 판단해 뒷북으로 강등한다.**
- **LIZARD(6→7회차, 풀생성후약33.9시간)**: 소멸은 아니다. 유동성이 $35,187.64→**$34,946.26**(-0.69%)로 **6회차 연속 유출**됐으나 유출폭은 직전과 유사한 낮은 수준으로 유지됐다. h1(-5.59%→-13.57%)은 재악화, h6(-35.51%→-25.87%)·h24(-61.19%→-53.39%)는 개선됐다. 회전율 15.98배→14.85배로 여전히 활발히 거래 중이다.
- **OBS(17→18회차, 풀생성후약37시간)**: ⚠️**직전 강한 반전유입이 1회차 만에 다시 유출로 반전**됐다. 유동성 $94,075.72→**$88,340.04**(-6.09%), h1(+22.12%→-12.15%)도 재음전했다. 다만 h6(+58.31%→+2.17%)는 대폭 감속해 손익분기 근접, h24(+158%→**+174%**)는 오히려 소폭 가속해 방향이 혼재됐다.
- **Truth Coin(Solana, 4→5회차, 풀생성후약18.2시간)**: 유동성이 $11,946.38→**$13,182.16**(+10.35%)로 유입 전환됐으나, h1은 -6.14%→-11.28%로 재악화했다. h6(-33.57%→-23.26%)·h24(-50.07%→-41.04%)는 개선됐다. 회전율은 355.1배→**322.4배**로 소폭 하락했으나 여전히 극단적 워시트레이딩 수준이다.
- **PANTS(17→18회차)**: 이번 회차 조사에서 **풀 불일치 함정을 발견해 정정했다** — DexScreener가 처음 반환한 최대유동성 풀은 Meteora($153,142)였으나 회전율이 0.44배로 거래가 거의 없었고, 실제 거래는 **PumpSwap 풀**(회전율≈16.27배)에서 발생 중이었다(PANTS 관련 과거 확인 사례와 동일한 함정, PumpSwap 기준으로 집계 확정). PumpSwap 기준: 유동성 $116,719.41→**$123,439.15**(+5.76%, 2회연속유출 후 반전유입), h1(-8.64%→-7.54%) 유사, h6(-49.5%→-25.68%) 대폭개선, h24(+17.76%→+6.12%) 감속. 전반적으로 고점통과 국면은 유지된다고 판단한다.

## 🆕 신규 발굴 — Dinger · WINNING (둘 다 Solana/PumpSwap, GeckoTerminal 솔라나 트렌딩)

- **Dinger(Schrödinger)** — CA `3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump`. GT 솔라나 트렌딩 h24거래량 기준 5위로 발견. 풀생성 후 약 7.4시간(2026-08-23T01:35:02Z). ⚠️h6(+747%)·h24(+4220%)로 이미 극단 급등을 마친 뒤 h1이 **-41.05%**로 급격 재음전해, 정점통과 직후로 강하게 추정된다. 유동성 $120,868.37, 거래량24h $9,111,347.67(**회전율≈75.4배로 극단적 워시트레이딩 의심**), 1시간 7,628매수/5,207매도로 거래는 여전히 활발하다. **확산 단계로 신규편입하되 최고위험 등급.** KOL/미디어 코로보 미확인(WebSearch 검색결과 없음, 정상 상태).
- **WINNING(Trump's Winning Coin)** — CA `FW6R4QQeP4fzqRwDHbBkpjHx3ecvYwhd5g7chKg8pump`. GT 솔라나 트렌딩 7위로 발견. 풀생성 후 약 13.9시간(2026-08-22T19:05:53Z). h1·h6·h24 전지표 동시 양전이고 h1이 가속 중이다: 유동성 $106,885.6, h1+33.73%, h6+25.16%, h24+1101%, 거래량24h $4,079,132.57(**회전율≈38.2배**), 1시간 3,143매수/2,391매도. ⚠️**'Trump's Winning Coin'은 공식 $TRUMP(CA 6p6xgHy…)와 컨트랙트 주소가 전혀 다른 별개의 파생/기생 밈코인이다** — WebSearch로도 이 토큰 고유의 보도는 확인되지 않았고, 공식 TRUMP 코인 정보만 검색됐다(티커 유사성을 노린 편승 토큰으로 강하게 추정). **확산 단계로 신규편입하되 최고위험 등급, 티커 혼동 주의.**
- KOL/미디어 코로보 없음(정상 상태, 결함 아님).

## 나머지 38종 갱신

- **TIPANSEM**: 24회차. 유동성유입지속완만(-6.44%…실제로는소폭유출), h1·h6개선, h24유사(-20.93%). 🔴(유지).
- **1B**: 16회차. 유동성소폭유입(+1.61%), h1유사·h6재음전, h24는-80.27%로대폭악화재경신. 🔴(유지,h24악화).
- **CLOCKIN**: 36회차. 유동성유입지속가속(+4.60%), h1·h6유사, h24소폭악화(-25.45%). 🟡(유지,대체로안정).
- **PEE**: 53회차. ⚠️h1거래실종4회차연속, 유동성소폭반등(+2.21%)하나회전율≈0.25배로여전히극단저조. 🔴(유지,거래실종4회연속).
- **CLUG**: 48회차. 유동성유출전환(-4.49%), h1재음전지속, h6개선세둔화. 🔴(유지,혼조).
- **PEPECOIN**: 26회차. ⭐전방위개선지속3회차연속(유동성+7.26%, h6+78%대폭가속, h24-11.5%). 🟢(유지,전방위개선지속3회차째).
- **FLUSH**: 14회차. 유동성유출전환(-4.68%), h1재음전, h24재악화(-73.56%). 🔴(유지,h24재악화).
- **MAPLE**: 12회차. ⭐강한반전회복,전지표동시개선(유동성+23.24%, h1+35.44%, h6+38.56%재양전, h24+1.9%손익분기근접). 🟢(하향,강한반전회복).
- **40M**: 11회차. ⚠️직전강한반전이1회차만에다시유출·재음전으로반전(유동성-10.73%, h1-11.41%재음전, h6-9.44%재음전). 🔴(재상향,재음전전환).
- **LIZARD**: 상세는 위 스포트라이트 참조. 🔴(유지,6회연속유출,점진적위축지속).
- **swappy**: 29회차. 유동성유입지속(+2.38%), h1재양전(+4.17%), h6·h24유사. 🟡(유지,소폭개선).
- **CYBERLEEK**: 28회차. 유동성유입가속(+14.13%), h1재음전(-4.24%)하나h6·h24대폭가속(h6+84.05%, h24+1260%). 🟢(유지,전방위강한개선지속).
- **CC**: 26회차째방향번복지속. 유동성유출전환(-1.65%), h1·h6동시개선, h24감속(+281%). 🔴(고위험,26회차째휩소지속).
- **Z500**: 19회차. 유동성유입전환(+3.43%), h1감속하나양전, h6·h24개선. 🟡(유지,전반적개선).
- **KIRK**: 16회차. ⭐유동성유입전환(+8.15%), h1·h6동시강한반전(h6+35.16%), h24개선(-2.06%,손익분기근접). 🟢(하향,강한반전개선).
- **CONK**: 13회차. 유동성유입지속(+4.13%), h1감속하나양전, h6강한반전(+26.46%)·h24재음전전환(-17.79%). 🟡(혼조).
- **CHUMP**: 4회차. 전지표양전유지,h24감속하나여전히강함(+52.12%). 🟢(유지,4회차째지속상승).
- **HOOKR**: 31회차. ⭐강한반전지속2회차연속(유동성+12.64%, h1+15.97%, h6+36.67%, h24+27.52%전부가속). 🟢(유지,강한반전지속).
- **CATE**: 90회차. 유동성유출전환(-3.90%), h1재양전유지·h6개선·h24소폭악화(-8.86%). 🟡(유지,소폭유출).
- **GOOD**: 32회차. h1재양전유지,h6유사,h24추가악화(-14.11%). 🟡(유지,h24재악화).
- **PRINTER**: 167회차. 전지표유사수준유지,h24소폭악화(-24.37%). 🟡(유지).
- **BULLSHIT**: 47회차. 유동성유출전환(-3.01%), h1재음전, h6·h24재악화(-32.51%). 🟡(유지,소폭유출).
- **TOAD**: 166회차. ⭐재반전개선,전지표동시양전전환(유동성+2.76%, h1+2.71%, h6+6.74%, h24+10.25%). 🟢(하향,재반전개선).
- **DPG**: 118회차. 유동성유입지속(+4.89%), h1유사·h6·h24개선지속(h6+19.03%, h24-13.85%). 🟢(유지,개선지속).
- **FWA**: 170회차. 전지표유사수준유지,손익분기권근접지속(h24-1.14%). 🟡(유지).
- **CALLOOOR**: 116회차. 유동성유입전환(+4.99%), 전지표동시양전(h1+5.83%, h6+1.15%재양전, h24+11.89%). 🟢(하향,전방위개선).
- **JUGGERNAUT**: 153회차. 전지표유사수준유지,h24소폭개선(+4.32%). 🟡(유지,혼조).
- **BRODIE**: 129회차. ⚠️h1·h6동시재음전전환(h1-1.21%, h6-7.73%), h24유사(-0.27%). 🔴(재상향,재음전전환).
- **Dealer**: 158회차. ⭐유동성유입지속(+4.53%), 전지표동시개선(h1+6.56%가속, h6+2.14%재양전, h24+11.89%). 🟢(하향,전방위개선).
- **lickingcat**: 158회차. 유동성유출전환(-1.30%), h1재음전, h6유사, h24소폭개선(-25.13%). 🟡(유지).
- **PITCOIN**: 119회차. 유동성유입전환(+1.34%), h1재양전·h6개선하나h24재음전전환(-4.52%). 🟡(유지,혼조).
- **PANTS**: 상세는 위 스포트라이트 참조. 🔴(유지,고점통과확정적).
- **Doge2**: 11회차. 유동성유입지속강화(+13.08%), h1유사·h6감속하나강함(+88.96%)·h24개선(-39.39%,여전히깊은음전). 🔴(유지,h24여전히깊은음전).
- **Truth Coin(Sol)**: 상세는 위 스포트라이트 참조. 🔴(유지,회전율여전히극단).
- **BARRON**: 4회차. 유동성유출지속(-1.82%), h1감속·h6유사·h24소폭개선(-28.22%,여전히깊은음전권). 🔴(유지,고점통과지속).
- **TRUTH**: 2회차. 조기~확산에서뒷북으로강등(상세 위 핵심사건·나머지 참조). 유동성-66.33%붕괴, h6-95.66%재악화, 회전율383.4배로심화. 🔴(재상향,조기확산→뒷북강등).
- **YOMOGI**: 상세는 위 스포트라이트 참조. 🔴(재상향,확산→뒷북강등,h6대폭붕괴확정).

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

| 토큰 | 체인/DEX | 단계 | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|---|
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 조기 | 미확인(코로보없음) | 26회차. 전방위개선지속3회차연속 | 유동성$25,527.37(+7.26%), h24-11.5% | 지속(26회차)·전방위개선3회차 | 🟢(개선지속) | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 12회차. 강한반전회복,전지표동시개선 | 유동성$28,260(+23.24%), h24+1.9%(손익분기근접) | 지속(12회차)·강한반전회복 | 🟢(반전회복) | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 조기 | 없음(자체서사만확인) | 36회차. 유동성유입가속,h24소폭악화 | 유동성$193,377.78(+4.60%), h24-25.45% | 지속(36회차) | 🟡(안정) | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 24회차. 유동성소폭유출,h1·h6개선 | 유동성$14,257(-6.44%), h24-20.93% | 지속(24회차) | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 7회차(풀생성후약33.9h). 6회연속유출이나유사수준유지 | 유동성$34,946.26(-0.69%), h24-53.39%, 회전율≈14.85배 | 지속(7회차)·6회연속유출 | 🔴(점진적위축) | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **CLUG** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 48회차. 유동성유출전환,h1재음전 | 유동성$38,076(-4.49%), h24-10.98% | 지속(48회차) | 🔴(혼조) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **PEE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 53회차. h1거래실종4회연속 | 유동성$8,266(+2.21%), h24-22.65%, 회전율≈0.25배 | 지속(53회차)·거래실종4회연속 | 🔴(소멸경계) | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **OBS** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 18회차. 강한반전유입1회차만에유출재전환,h1재음전 | 유동성$88,340.04(-6.09%), h24+174% | 지속(18회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **1B** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 16회차. h24대폭악화재경신 | 유동성$25,007.17(+1.61%), h24-80.27% | 지속(16회차)·h24악화 | 🔴(h24악화) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **FLUSH** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 14회차. 유동성유출전환,h24재악화 | 유동성$34,654.14(-4.68%), h24-73.56% | 지속(14회차)·h24재악화 | 🔴(h24재악화) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **40M** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 11회차. 직전반전회복이1회차만에재음전전환 | 유동성$14,671(-10.73%), h24+28.03% | 지속(11회차)·재음전전환 | 🔴(재음전전환) | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **Dinger** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 신규,풀생성7.4h전,h6+747%·h24+4220%이미급등,h1-41%로재음전(이미정점통과추정) | 유동성$120,868.37, h24+4220%, 회전율≈75.4배 | **신규** | 🔴(초고위험,이미정점통과추정) | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **WINNING** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 신규,풀생성13.9h전,전지표동시양전·h1가속,공식TRUMP과무관한파생토큰 | 유동성$106,885.6, h24+1101%, 회전율≈38.2배 | **신규** | 🔴(초고위험,티커혼동주의) | [DexScreener](https://dexscreener.com/solana/FW6R4QQeP4fzqRwDHbBkpjHx3ecvYwhd5g7chKg8pump) |
| **KIRK** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 16회차. 유동성유입전환,h1·h6동시강한반전 | 유동성$88,917.76(+8.15%), h24-2.06%(손익분기근접) | 지속(16회차)·강한반전개선 | 🟢(반전개선) | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 확산 | 미확인(코로보없음) | 28회차. 유동성유입가속,h6·h24대폭가속 | 유동성$1,508,763(+14.13%), h24+1260% | 지속(28회차)·전방위강한개선 | 🟢(강한개선) | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **Z500** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 19회차. 유동성유입전환,전반적개선 | 유동성$77,853.45(+3.43%), h24-25.77% | 지속(19회차)·전반적개선 | 🟡(개선) | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **CHUMP** | Robinhood Chain(Uniswap V3 1%) | 확산 | 미확인(코로보없음) | 4회차. 전지표양전유지 | 유동성$251,407.26(+0.92%), h24+52.12% | 지속(4회차) | 🟢(양전지속) | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **swappy** | Robinhood Chain(Uniswap V4) | 확산 | 미확인(코로보없음) | 29회차. 유동성유입지속,h1재양전 | 유동성$207,047.09(+2.38%), h24-15.21% | 지속(29회차)·소폭개선 | 🟡(개선) | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CONK** | Solana(Raydium) | 확산 | 미확인(코로보없음) | 13회차. h6강한반전·h24재음전전환 | 유동성$97,175.85(+4.13%), h24-17.79% | 지속(13회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CC** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 26회차째방향번복지속,h24감속 | 유동성$220,722.02(-1.65%), h24+281% | 지속(26회차)·워시트레이딩의심강화 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 뒷북 | 미확인(코로보없음) | 31회차. 강한반전지속2회차연속 | 유동성$246,036.20(+12.64%), h24+27.52% | 지속(31회차)·강한반전지속 | 🟢(반전개선) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **TOAD** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 166회차. 재반전개선,전지표동시양전 | 유동성$414,950.67(+2.76%), h24+10.25% | 지속(166회차)·재반전개선 | 🟢(반전개선) | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **DPG** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 118회차. 개선지속 | 유동성$99,653.11(+4.89%), h24-13.85% | 지속(118회차)·개선지속 | 🟢(개선지속) | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **Dealer** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 158회차. 전방위개선 | 유동성$127,106.49(+4.53%), h24+11.89% | 지속(158회차)·전방위개선 | 🟢(전방위개선) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **CALLOOOR** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 116회차. 전방위개선 | 유동성$62,880.09(+4.99%), h24+11.89% | 지속(116회차)·전방위개선 | 🟢(전방위개선) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **CATE** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 90회차. 소폭유출,h1양전유지 | 유동성$1,790,384.43(-3.90%), h24-8.86%, 회전율≈28.89배 | 지속(90회차)·소폭유출 | 🟡(소폭유출) | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **GOOD** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 32회차. h1양전유지,h24재악화 | 유동성$432,264.64(-0.58%), h24-14.11% | 지속(32회차)·h24재악화 | 🟡(h24재악화) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 뒷북 | 미확인(코로보없음) | 167회차. 유사수준유지 | 유동성$351,072.98(-1.08%), h24-24.37% | 지속(167회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **BULLSHIT** | Solana(Meteora등11개풀) | 뒷북 | 미확인(WebSearch로토큰명특정보도없음) | 47회차. 소폭유출,h24재악화 | 유동성(PumpSwap)$219,515.87(-3.01%), h24-32.51%, 회전율≈8.80배 | 지속(47회차)·소폭유출 | 🟡(소폭유출) | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **FWA** | Ethereum(Uniswap V4) | 뒷북 | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover)+CG트렌딩12위(carryover) | 170회차. 손익분기권근접지속 | 유동성$1,126,569.55(+0.39%), h24-1.14% | 지속(170회차)·손익분기권 | 🟡(손익분기권) | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **JUGGERNAUT** | Robinhood Chain(Uniswap V3 1%) | 뒷북 | Drallio(약한코로보,carryover) | 153회차. h24소폭개선 | 유동성$261,895.41(+0.97%), h24+4.32% | 지속(153회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **lickingcat** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 158회차. 유출전환,h1재음전 | 유동성$55,359.12(-1.30%), h24-25.13% | 지속(158회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **PITCOIN** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 119회차. h24재음전전환 | 유동성$31,257.28(+1.34%), h24-4.52% | 지속(119회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 18회차(dogwifpants). 반전유입,h6대폭개선 | 유동성$123,439.15(+5.76%), h24+6.12%, 회전율≈16.27배 | 지속(18회차)·고점통과확정적 | 🔴(고점통과확정적) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **BRODIE** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 129회차. h1·h6동시재음전전환 | 유동성$168,601.69(-0.97%), h24-0.27% | 지속(129회차)·재음전전환 | 🔴(재음전전환) | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **Doge2** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 11회차. h24여전히깊은음전 | 유동성$58,681.25(+13.08%), h24-39.39% | 지속(11회차)·h24여전히깊은음전 | 🔴(h24여전히깊은음전) | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 5회차,풀생성18.2h전,회전율여전히극단 | 유동성$13,182.16(+10.35%), 회전율≈322.4배 | 지속(5회차) | 🔴(회전율여전히극단) | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 뒷북 | 미확인(코로보없음) | 4회차,풀나이19개월,고점통과지속 | 유동성$250,671.45(-1.82%), h24-28.22%, 회전율≈3.4배 | 지속(4회차) | 🔴(고점통과지속) | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **TRUTH** | Robinhood Chain(Uniswap V2) | 뒷북 | 미확인(코로보없음) | 2회차,풀생성18.0h전,조기확산→뒷북강등,유동성-66%붕괴 | 유동성$51,545.62(-66.33%), h6-95.66%, 회전율≈383.4배 | 지속(2회차)·조기확산→뒷북강등 | 🔴(유동성-66%붕괴) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **YOMOGI** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 3회차,풀생성7.5h전,확산→뒷북강등,h6대폭붕괴확정 | 유동성$46,705.38(-0.82%), h6-84.65%, 회전율≈178.3배 | 지속(3회차)·확산→뒷북강등 | 🔴(h6대폭붕괴확정) | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출 요약(이번 회차)**: **신규편입 2건** — Dinger·WINNING(둘 다 Solana, 확산단계, 최고위험). **편출 1건** — Truth Coin(RH, 사실상완전소멸 확정). **강등 2건** — TRUTH·YOMOGI(확산→뒷북, 둘 다 명백한 정점통과·붕괴 증거). **강한반전개선 다수**: MAPLE·KIRK·HOOKR·TOAD·CALLOOOR·Dealer. **재음전전환**: 40M·BRODIE.

## 온체인 신호 상세

- **Truth Coin(RH) 완전소멸 상세**: DexScreener raw JSON `liquidity: {usd: 45.85, base: 200445, quote: 0.00947}`, GeckoTerminal `reserve_in_usd: "45.5567"` — 두 독립 소스가 소수점 단위까지 근접 일치해 조회 오류가 아닌 실제 사건임을 확증. quote(WETH) 리저브가 0.00947(약 $40 상당)에 불과해 WETH 사이드가 거의 전량 인출된 전형적 유동성풀 소진 패턴이다. 4회차(약14.5~18.5시간)에 걸쳐 $331,894→$824,205→$45.85로 롤러코스터를 그리다 최종 붕괴했다 · 2026-08-23T09:00Z
- **TRUTH·YOMOGI 강등 상세**: 위 스포트라이트·나머지38종갱신 섹션 참조. 둘 다 h6 지표(TRUTH -95.66%, YOMOGI -84.65%)가 결정적 붕괴 증거다 · 2026-08-23T09:00Z
- **Dinger·WINNING 신규발굴 상세**: 위 신규발굴 섹션 참조. GeckoTerminal 솔라나 트렌딩(page=1)에서 h24 거래량·가격변동 기준 상위권 신규 풀을 스캔해 발견 · 2026-08-23T09:00Z
- **PANTS 풀불일치 정정 상세**: DexScreener가 기본 반환하는 최대유동성 페어(Meteora, $153,142, 회전율0.44배)와 실제 거래가 활발한 페어(PumpSwap, $123,439, 회전율16.27배)가 상이함을 확인해 PumpSwap 기준으로 정정 집계했다 · 2026-08-23T09:00Z
- **나머지 34건 상세**: TIPANSEM유입지속완만. 1B h24대폭악화재경신. CLOCKIN안정흐름지속. PEE h1거래실종4회연속. CLUG혼조. PEPECOIN전방위개선3회차째. FLUSH h24재악화. MAPLE강한반전회복. 40M재음전전환. swappy소폭개선. CYBERLEEK전방위강한개선(+1260%). CC26회차째휩소(+281%). Z500전반적개선. KIRK강한반전개선. CONK혼조. CHUMP4회차째양전지속. HOOKR강한반전지속2회차째. CATE소폭유출. GOOD h24재악화. PRINTER유지. BULLSHIT소폭유출. TOAD재반전개선. DPG개선지속. FWA손익분기권. CALLOOOR전방위개선. JUGGERNAUT혼조. BRODIE재음전전환. Dealer전방위개선. lickingcat유지. PITCOIN혼조. Doge2 h24여전히깊은음전. BARRON고점통과지속(회전율3.4배) · 2026-08-23T09:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **Dinger·WINNING(신규) — 각각 WebSearch 확인, 토큰 고유 보도·KOL 언급 없음. 코로보 없음(정상 상태, 결함 아님). 특히 WINNING은 공식 $TRUMP 관련 검색결과만 나와 별개 파생토큰임을 재확인**.
- **나머지 38종(부모세션 최우선 확인대상 포함) — 코로보 미확인**: 이번 회차는 40개 활성종목(신규2건 포함, Truth Coin RH 완전소멸 편출 1건, TRUTH·YOMOGI 강등 2건 처리)과 notable 3종(CASHCAT·STONKBROKER·PONS) 참고데이터 갱신에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-23 07:00Z)로부터 정확히 2시간 경과(정상 간격).
- **⭐핵심 사건 — Truth Coin(RH) 완전소멸**: 20분~2시간 단위로 $331,894↔$824,205 롤러코스터를 그리던 토큰이 이번 회차에 유동성이 $45.85(DS)/$45.56(GT)로 사실상 완전 붕괴한 것을 두 독립 소스로 교차확인했다. quote(WETH) 리저브가 0.00947에 불과해 유동성풀에서 WETH가 거의 전량 인출된 것으로 판단되며, notable로 편출한다. 이 워치 사상 P400·HEREBRO·MOONCOIN에 이은 네 번째 확정 완전소멸 사례다.
- **TRUTH·YOMOGI 동시 강등**: 확산 단계였던 두 토큰이 이번 회차에 나란히 h6 지표 붕괴(TRUTH -95.66%, YOMOGI -84.65%)를 보여 뒷북으로 강등했다. TRUTH는 유동성도 -66.33% 급감했다. 두 토큰 모두 여전히 극단적 회전율(TRUTH 383.4배, YOMOGI 178.3배)로 워시트레이딩이 지속 중이다.
- **PANTS 풀 선택 함정 재확인**: CLAUDE.md 경고("다수 풀 토큰은 최대유동성 풀만 기계적으로 고르면 안 됨")대로, 이번 조회에서도 DexScreener 기본 반환값이 저회전율 Meteora 풀이었다. 항상 거래량 대비 유동성(회전율)을 함께 확인해 실제 거래가 발생하는 풀을 골라야 함을 재확인했다.
- **신규 2건 모두 이미 급등 후 반전/가속 혼재**: Dinger는 h1 -41%로 이미 재음전(정점통과 추정), WINNING은 아직 h1 가속 중(+33.73%)이라 상대적으로 이른 단계로 판단해 둘 다 확산단계에 편입했다.
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API(체인별 배치조회)로 39개 기존 활성종목을 전량 확보했고, 그 과정에서 4개 토큰(CATE·BULLSHIT·CALLOOOR·Dealer)이 최초 배치 응답에서 저유동/저회전율 이상 풀(meteora 등)로 잘못 매칭돼 개별 재조회로 정정했다(회전율 대조 필수 규칙 재확인). Truth Coin(RH)·TRUTH 두 건은 raw JSON을 직접 확인해 극단적 수치가 조회 오류가 아님을 검증했다. GeckoTerminal 솔라나·로빈후드체인 트렌딩(page=1)으로 신규 발굴 스캔을 진행해 Dinger·WINNING 2건을 확보했다. X 직접 조회는 로그인월로 시도하지 않아 신규 포함 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
