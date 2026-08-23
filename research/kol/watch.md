# 온체인 트렌딩 조기경보 — 2026-08-23 11:00 UTC (KST 2026-08-23 20:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-23 09:00Z)로부터 정확히 2시간 경과**(정상 간격). 40개 활성종목 전부를 DexScreener 토큰 API(체인별 배치조회)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 스캔으로 신규 발굴을 진행했다.

> **⚠️이번 회차 데이터 이슈**: DexScreener 배치조회 2건에서 응답 개수가 요청 개수와 불일치했다(솔라나 배치1: 13개 요청→12개 응답, PEE 누락 / 로빈후드체인 배치: 13개 요청→12개 응답, TRUTH 누락). 규칙대로 두 토큰 모두 개별 재조회로 보완했다(CLAUDE.md·에이전트 규칙 §3 준수).

> **편입/편출/강등 내역**: **신규편입 2건** — omo(Solana, 확산), MANEKI(Robinhood Chain, 조기). **강등 2건** — Dinger·WINNING이 확산에서 뒷북으로 강등(둘 다 이번 회차 유동성 급감·h1 반전으로 정점통과 확정). **편출 0건**. 활성목록 **40종→42종**. notable **25개→26개**(신규 티커충돌 경계사례 1건 기록추가).

## ⚠️ 부모 세션 요청 최우선 확인 — Dinger, WINNING, TRUTH(RH), YOMOGI, LIZARD, OBS

- **Dinger(2회차, 풀생성후약9.4시간)**: ⚠️**확산→뒷북 강등, 정점통과 확정.** 유동성이 $120,868.37→**$52,991**(-56.16%)로 반토막 이상 증발했다. h1은 -41.05%→+0.68%로 낙폭이 멈췄으나 h6가 +747%→**-37.63%**로 대폭 재악화했고, h24는 +4220%→+700%로 대폭 감속했다. 회전율은 75.4배→**194.4배**로 대폭 상승해 극단적 워시트레이딩이 심화됐다. 뒷북으로 강등한다.
- **WINNING(2회차, 풀생성후약15.9시간)**: ⚠️**확산→뒷북 강등.** 직전 회차 h1이 +33.73%로 가속 중이었으나 이번 회차 **-20.03%로 급반전**했다. 유동성도 $106,885.6→$95,053(-11.07%)로 유출 전환했고, h6(+25.16%→+12.05%)·h24(+1101%→+817%)도 모두 감속했다. 티커 혼동 주의(공식 $TRUMP과 별개 파생토큰)는 유지. 뒷북으로 강등한다.
- **TRUTH(Robinhood Chain, CA `0x2ec5…fc4`, 3회차, 풀생성후약20.0시간)**: 유동성 유출이 지속됐다(**$51,545.62→$49,103.84, -4.74%**). h1은 -10.1%→**-39.09%**로 대폭 악화했고, h6는 -95.66%→-96.49%로 극심한 수준을 유지했다. h24는 +4322%→+3501%로 대폭 감속했으나 여전히 저베이스 아티팩트성 수치다. 회전율은 383.4배→**421.6배**로 더욱 상승했다. Truth Coin(RH, 완전소멸 확정)과 유사한 붕괴 경로를 밟고 있는지 계속 경계하나, 이번 회차 GT 재확인에서 그 완전소멸 토큰의 유동성이 여전히 $76.56(사실상 죽음)임을 교차확인해 TRUTH(0x2ec5…)와는 아직 뚜렷이 구분되는 상태다.
- **YOMOGI(4회차, 풀생성후약9.5시간)**: 유동성 유출이 지속됐다($46,705.38→**$43,993.75**, -5.81%). h1은 -5.69%→**+4.6%**로 재양전했으나, h6는 -84.65%→-64.09%로 **여전히 극심한 붕괴권**에 머물렀다(다만 낙폭 자체는 완화). h24는 +456%→+388%로 감속했다. 회전율은 178.3배→**191.9배**로 상승해 워시트레이딩이 지속 중이다.
- **LIZARD(8회차, 풀생성후약35.9시간)**: ⭐**6회차 연속 이어지던 유동성 유출이 이번 회차 반전유입으로 종료됐다.** 유동성 $34,946.26→**$36,337**(+3.98%), h1(-13.57%→+4.22%)도 재양전했다. h6(-25.87%→-4.24%)·h24(-53.39%→-51.28%)도 개선/유사 수준이다. 회전율≈13.34배(직전14.85배와 유사)로 여전히 활발히 거래 중이다.
- **OBS(19회차, 풀생성후약39시간)**: 직전 회차의 유출·재음전이 1회차 만에 다시 반전개선됐다. 유동성 $88,340.04→**$89,228.65**(+1.01%, 거의 회복), h1(-12.15%→+4.79%)도 재양전, h6(+2.17%→+30.25%)는 가속했다. h24는 +174%→+156%로 소폭 감속했다. 방향 혼재는 계속되나 이번 회차는 전반적으로 개선 쪽이다.

## 🆕 신규 발굴 — omo · MANEKI

- **omo** — CA `94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump`. Solana(PumpSwap). GT 솔라나 트렌딩 14위로 발견. 풀생성 후 약 13일(2026-08-10경) — 완전히 새로운 토큰은 아니나, 최근 h1·h6·h24 전지표가 동시 양전하고 가속 중이다: 유동성 $160,353.56, h1+14.27%, h6+77.32%, h24+174%, 거래량24h $2,432,328.38(**회전율≈15.2배**), 24h 12,536매수/11,436매도로 매수우위. **확산 단계로 신규편입, 최고위험 등급.** KOL/미디어 코로보 미확인(정상 상태).
- **MANEKI** — CA `0x00eB2583F442d35473Bed8801Efb01C82D84C149`. Robinhood Chain(SushiSwap V3 1%, WETH페어). GT 로빈후드체인 트렌딩 15위로 발견. 풀생성 후 약 63시간(2026-08-20T20:08:48Z, 약 2.6일). h1·h6·h24가 **순서대로 단조 가속**(+3.71%→+24.25%→+70.36%)하는 일관된 상승 패턴이나, 거래량24h $95,069.51 대비 유동성 $52,680.72로 **회전율≈1.80배로 낮아** 지속성이 불확실하다. **조기 단계로 신규편입, 최고위험 등급.** KOL/미디어 코로보 미확인(정상 상태).
- 두 토큰 모두 KOL/미디어 코로보 없음(정상 상태, 결함 아님).

## 나머지 40종 갱신

- **PEPECOIN**: 27회차. ⚠️3회차연속 이어지던 전방위개선 streak이 이번 회차 반전악화(유동성-3.69%, h1재음전, h6+78%→+26.12%대폭감속, h24-21.27%재악화). 🔴(재상향).
- **MAPLE**: 13회차. ⚠️직전 강한반전회복이 1회차 만에 다시 반전악화(유동성-13.21%, h1재음전, h6+38.56%→+0.34%대폭감속, h24-48.92%재악화). 🔴(재상향).
- **CLOCKIN**: 37회차. 안정흐름이 이번 회차 재음전전환(유동성-4.86%, h1재음전, h6손익분기근접, h24추가악화). 🔴(재상향).
- **TIPANSEM**: 25회차. 유동성소폭유입(+3.60%), h1·h6유사, h24개선(-11.66%). 🔴(유지,저유동).
- **1B**: 17회차. 유동성소폭유입(+1.13%), h1재악화(-13.19%), h24는역대최악권에서소폭개선(-76.49%). 🔴(유지).
- **CLUG**: 49회차. 유동성소폭유입(+1.22%), h6급격둔화재음전(-1.12%), h24개선(-5.01%). 🔴(유지,혼조).
- **FLUSH**: 15회차. 유동성유입전환(+3.60%), h1재양전, h24여전히극단이나개선(-69.15%). 🟡(하향,소폭개선).
- **PEE**: 54회차. ⚠️4회연속실종됐던 h1거래가 재개(8매수/11매도)했으나 전반적악화(유동성-7.29%, h6재음전, h24-26.9%). 🔴(유지).
- **40M**: 12회차. ⚠️직전재음전전환이 1회차 만에 다시 전방위반전유입(유동성+11.02%, h1+9.72%재양전, h6+17.07%재양전, h24+47.36%가속). 🔴(유지,반복된반전이력).
- **swappy**: 30회차. 유동성유출전환(-1.77%), h1재음전, h6재양전. 🟡(유지).
- **CYBERLEEK**: 29회차. ⭐전방위강한개선가속지속(유동성+13.55%, h1+23.72%강한재양전, h6+110%가속, h24+1729%대폭가속). GT솔라나트렌딩1위재확인. 🟢(유지).
- **CC**: 27회차째방향번복지속. 유동성유출전환(-4.89%), h1·h6동시둔화, h24감속(+215%). 🔴(고위험).
- **Z500**: 20회차. 유동성유입지속(+2.47%), h1재음전, h6·h24개선. 🟡(유지,대체로개선).
- **KIRK**: 17회차. 유동성유출전환(-3.03%), h1유사, h6재음전(-5.87%), h24손익분기돌파(+0.34%). 🟡(재상향,혼조).
- **CONK**: 14회차. 유동성유출전환(-5.70%), h1·h6동시감속, h24유사(-15.67%). 🟡(유지,감속).
- **CHUMP**: 5회차. ⭐전방위대폭가속지속(유동성+13.54%, h1+27.52%대폭가속, h6+28.87%강한재양전, h24+110%대폭가속). 🟢(유지,5회차째지속가속).
- **HOOKR**: 32회차. 유동성유사수준(-0.14%), h1감속, h6유사, h24가속(+34.40%). 🟢(유지,강한지속).
- **CATE**: 91회차. 유동성유입전환(+3.52%), h1·h6동시강한재양전, h24유사(-10.46%). 회전율≈28.10배. GT솔라나트렌딩2위재확인. 🟢(하향,강한반전개선).
- **GOOD**: 33회차. ⭐전지표동시양전전환(유동성+4.82%, h1+6.33%가속, h6+3.63%재양전, h24+2.67%손익분기돌파). 🟢(하향,전방위양전전환).
- **PRINTER**: 168회차. 전지표유사수준유지, h24소폭개선(-21.95%). 🟡(유지).
- **BULLSHIT**: 48회차. 유동성유출지속(-4.95%, PumpSwap기준), h1재양전, h6개선, h24소폭악화(-34.01%). 회전율≈9.83배. 🟡(유지,소폭유출지속).
- **TOAD**: 167회차. 유동성유사수준(-0.75%), h1감속, h6재음전(-10.39%), h24개선(+12.94%). 🟡(재상향,혼조).
- **DPG**: 119회차. 유동성유사수준(-0.93%), h1개선, h6유사, h24악화(-28.49%). 🟡(유지,혼조).
- **FWA**: 171회차. 전지표유사수준, 손익분기권근접지속(h24-4.79%). 🟡(유지).
- **CALLOOOR**: 117회차. 유동성유입지속(+4.39%), h1감속, h6대폭가속(+17.22%), h24가속(+18.26%). 🟢(유지,전방위개선).
- **JUGGERNAUT**: 154회차. 전지표유사수준유지(h24+4.10%). 🟡(유지).
- **BRODIE**: 130회차. 유동성유출전환(-5.80%), h1·h6동시재악화, h24재양전(+8.60%). 🔴(재상향,대체로악화).
- **Dealer**: 159회차. ⚠️직전전방위개선이 이번 회차 전방위재음전으로반전(유동성-3.67%, h1재음전, h6재음전, h24재음전). 🔴(재상향).
- **lickingcat**: 159회차. 유동성소폭유입(+0.79%), h1재양전, h6·h24개선. 🟡(유지,소폭개선).
- **PITCOIN**: 120회차. 유동성소폭유출(-1.62%), h1재음전, h6악화, h24유사(-3.24%). 🔴(재상향,대체로악화).
- **PANTS**: 19회차(dogwifpants). 유동성유입지속(+7.67%), h6대폭개선(-0.85%,손익분기근접), h24가속(+21.87%). 풀불일치재확인완료(PumpSwap이거래압도적1위). 회전율≈15.2배. 🔴(유지,고점통과확정적이나단기반등).
- **Doge2**: 12회차. ⚠️전방위대폭악화(유동성-12.51%, h1재악화, h6급붕괴, h24-73.71%대폭악화). 🔴(재상향).
- **Truth Coin(Sol)**: 6회차(풀생성후약20.2시간). ⭐전방위강한반전유입(유동성+41.22%, h1+26.29%강한재양전, h6+76.59%강한재양전, h24+9.57%손익분기돌파). 회전율≈228.8배(직전322.4배대비하락하나여전히극단). 🔴(유지,강한반전이나회전율여전히극단).
- **BARRON**: 5회차(풀나이19개월). 유동성유입전환(+2.09%), h6·h24개선. 🔴(유지,고점통과지속).
- **TRUTH(RH)**: 상세는 위 스포트라이트 참조. 🔴(유지,지속붕괴).
- **YOMOGI**: 상세는 위 스포트라이트 참조. 🔴(유지,극단변동지속).

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

| 토큰 | 체인/DEX | 단계 | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 19회차. 유출·재음전이1회차만에다시반전개선 | 유동성$89,228.65(+1.01%), h24+156% | 지속(19회차)·대체로개선 | 🟡(개선) | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 조기 | 미확인(코로보없음) | 27회차. 3회연속개선streak종료,전방위반전악화 | 유동성$24,585.41(-3.69%), h24-21.27% | 지속(27회차)·streak종료 | 🔴(재악화) | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 13회차. 강한반전회복이1회차만에다시반전악화 | 유동성$24,528(-13.21%), h24-48.92% | 지속(13회차)·반전악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 조기 | 없음(자체서사만확인) | 37회차. 안정흐름이재음전전환 | 유동성$183,981.26(-4.86%), h24-30.37% | 지속(37회차)·재음전전환 | 🔴(재음전) | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 25회차. 유동성소폭유입,h24개선 | 유동성$14,771(+3.60%), h24-11.66% | 지속(25회차) | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 8회차(풀생성후약35.9h). 6회연속유출종료,반전유입 | 유동성$36,337(+3.98%), h24-51.28%, 회전율≈13.34배 | 지속(8회차)·유출종료 | 🟢(반전유입) | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 17회차. h1재악화,h24소폭개선 | 유동성$25,289.22(+1.13%), h24-76.49% | 지속(17회차) | 🔴(고위험) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 49회차. h6급격둔화재음전 | 유동성$38,541(+1.22%), h24-5.01% | 지속(49회차) | 🔴(혼조) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 15회차. 유동성유입전환,h1재양전 | 유동성$35,902.55(+3.60%), h24-69.15% | 지속(15회차)·소폭개선 | 🟡(소폭개선) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 54회차. 4회연속실종된h1거래재개했으나전반적악화 | 유동성$7,663.77(-7.29%), h24-26.9%, 회전율≈0.37배 | 지속(54회차)·거래재개 | 🔴(소멸경계) | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 12회차. 재음전이1회차만에다시반전유입 | 유동성$16,288(+11.02%), h24+47.36% | 지속(12회차)·재반전유입 | 🔴(반복반전) | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 조기 | 미확인(코로보없음) | 신규,풀생성약63h전,h1·h6·h24단조가속 | 유동성$52,680.72, h24+70.36%, 회전율≈1.80배 | **신규** | 🔴(신규,회전율낮음) | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **omo** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 신규,풀생성약13일전,전지표양전가속 | 유동성$160,353.56, h24+174%, 회전율≈15.2배 | **신규** | 🔴(신규,고위험) | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **CHUMP** | Robinhood Chain(Uniswap V3 1%) | 확산 | 미확인(코로보없음) | 5회차. 전방위대폭가속지속 | 유동성$285,461.55(+13.54%), h24+110% | 지속(5회차)·5회차째가속 | 🟢(가속) | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 확산 | 미확인(코로보없음) | 29회차. 전방위강한개선가속지속 | 유동성$1,713,149(+13.55%), h24+1729% | 지속(29회차)·강한개선 | 🟢(강한개선) | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **swappy** | Robinhood Chain(Uniswap V4) | 확산 | 미확인(코로보없음) | 30회차. 유출전환,h1재음전 | 유동성$203,391.59(-1.77%), h24-15.82% | 지속(30회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **Z500** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 20회차. 유입지속,대체로개선 | 유동성$79,778(+2.47%), h24-16.74% | 지속(20회차)·개선 | 🟡(개선) | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 17회차. h6재음전,h24손익분기돌파 | 유동성$86,220(-3.03%), h24+0.34% | 지속(17회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 확산 | 미확인(코로보없음) | 14회차. h1·h6감속 | 유동성$91,639(-5.70%), h24-15.67% | 지속(14회차)·감속 | 🟡(감속) | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CC** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 27회차째방향번복지속 | 유동성$209,933(-4.89%), h24+215% | 지속(27회차)·고위험 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Dinger** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 확산→뒷북강등,유동성반토막,정점통과확정 | 유동성$52,991(-56.16%), h24+700%, 회전율≈194.4배 | 지속(2회차)·강등 | 🔴(정점통과확정) | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **WINNING** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 확산→뒷북강등,h1급반전음전 | 유동성$95,053(-11.07%), h24+817%, 회전율≈53.66배 | 지속(2회차)·강등 | 🔴(급반전) | [DexScreener](https://dexscreener.com/solana/FW6R4QQeP4fzqRwDHbBkpjHx3ecvYwhd5g7chKg8pump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 뒷북 | 미확인(코로보없음) | 32회차. 강한지속 | 유동성$245,680.20(-0.14%), h24+34.40% | 지속(32회차)·강한지속 | 🟢(강한지속) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **CATE** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 91회차. 강한반전개선 | 유동성$1,853,427.61(+3.52%), h24-10.46%, 회전율≈28.10배 | 지속(91회차)·반전개선 | 🟢(반전개선) | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **GOOD** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 33회차. 전방위양전전환,h24손익분기돌파 | 유동성$453,085.73(+4.82%), h24+2.67% | 지속(33회차)·양전전환 | 🟢(양전전환) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 뒷북 | 미확인(코로보없음) | 168회차. 유사수준유지 | 유동성$349,788.76(-0.37%), h24-21.95% | 지속(168회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **BULLSHIT** | Solana(Meteora등11개풀) | 뒷북 | 미확인(WebSearch로토큰명특정보도없음) | 48회차. 소폭유출지속 | 유동성(PumpSwap)$208,642.45(-4.95%), h24-34.01%, 회전율≈9.83배 | 지속(48회차)·소폭유출 | 🟡(소폭유출) | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **TOAD** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 167회차. h6재음전,h24개선 | 유동성$411,844.51(-0.75%), h24+12.94% | 지속(167회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **DPG** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 119회차. h24악화 | 유동성$98,731.14(-0.93%), h24-28.49% | 지속(119회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **FWA** | Ethereum(Uniswap V4) | 뒷북 | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover)+CG트렌딩12위(carryover) | 171회차. 손익분기권근접지속 | 유동성$1,125,638.47(-0.08%), h24-4.79% | 지속(171회차)·손익분기권 | 🟡(손익분기권) | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **CALLOOOR** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 117회차. 전방위개선 | 유동성$65,640.35(+4.39%), h24+18.26% | 지속(117회차)·전방위개선 | 🟢(전방위개선) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **JUGGERNAUT** | Robinhood Chain(Uniswap V3 1%) | 뒷북 | Drallio(약한코로보,carryover) | 154회차. 유사수준유지 | 유동성$259,627.97(-0.87%), h24+4.10% | 지속(154회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 130회차. h1·h6재악화 | 유동성$158,827.03(-5.80%), h24+8.60% | 지속(130회차)·대체로악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **Dealer** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 159회차. 전방위재음전전환 | 유동성$122,436.54(-3.67%), h24-9.56% | 지속(159회차)·재음전전환 | 🔴(재음전) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 159회차. 소폭개선 | 유동성$55,794.28(+0.79%), h24-18.37% | 지속(159회차) | 🟡(소폭개선) | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **PITCOIN** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 120회차. h1재음전,h6악화 | 유동성$30,749.63(-1.62%), h24-3.24% | 지속(120회차)·대체로악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 19회차(dogwifpants). h6대폭개선 | 유동성$132,909.67(+7.67%), h24+21.87%, 회전율≈15.2배 | 지속(19회차)·고점통과확정적 | 🔴(고점통과확정적) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Doge2** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 12회차. 전방위대폭악화 | 유동성$51,343.18(-12.51%), h24-73.71% | 지속(12회차)·대폭악화 | 🔴(대폭악화) | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 6회차,풀생성20.2h전,전방위강한반전유입 | 유동성$18,614.41(+41.22%), h24+9.57%, 회전율≈228.8배 | 지속(6회차)·강한반전 | 🔴(회전율여전히극단) | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 뒷북 | 미확인(코로보없음) | 5회차,풀나이19개월,고점통과지속 | 유동성$255,899.81(+2.09%), h24-24.96% | 지속(5회차) | 🔴(고점통과지속) | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **TRUTH** | Robinhood Chain(Uniswap V2) | 뒷북 | 미확인(코로보없음) | 3회차,풀생성20.0h전,지속붕괴,회전율상승 | 유동성$49,103.84(-4.74%), h6-96.49%, 회전율≈421.6배 | 지속(3회차)·지속붕괴 | 🔴(지속붕괴) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **YOMOGI** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 4회차,풀생성9.5h전,극단변동지속 | 유동성$43,993.75(-5.81%), h6-64.09%, 회전율≈191.9배 | 지속(4회차)·극단변동지속 | 🔴(극단변동지속) | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 2건** — omo(Solana,확산)·MANEKI(RH,조기), 둘 다 최고위험. **강등 2건** — Dinger·WINNING(확산→뒷북, 둘 다 명백한 정점통과 증거). **편출 0건**. **강한반전개선**: CATE·GOOD·Truth Coin(Sol)·LIZARD(6회연속유출종료). **전방위재음전전환**: Dealer·PITCOIN·BRODIE·Doge2(대폭악화).

## 온체인 신호 상세

- **Dinger·WINNING 강등 상세**: 위 스포트라이트 참조. 둘 다 유동성 급감(-56.16%/-11.07%)과 지표 재악화가 결정적 근거다 · 2026-08-23T11:00Z
- **LIZARD 6회연속유출 종료 상세**: 유동성이 6회차 연속 유출(누적) 끝에 이번 회차 처음으로 반전유입(+3.98%)됐다. h1도 재양전, 회전율은 13.34배로 여전히 활발하다 · 2026-08-23T11:00Z
- **omo·MANEKI 신규발굴 상세**: 위 신규발굴 섹션 참조. GeckoTerminal 솔라나·로빈후드체인 트렌딩(page=1)에서 h24 거래량·가격변동 기준 상위권 신규/급상승 풀을 스캔해 발견 · 2026-08-23T11:00Z
- **DexScreener 배치 응답 개수 불일치 상세**: 솔라나 배치1(13개 요청)에서 PEE, 로빈후드체인 배치(13개 요청)에서 TRUTH가 각각 응답에서 누락돼 개별 재조회로 보완했다. 규칙(§3 "응답 개수를 요청 개수와 대조")이 실제로 적발한 사례 · 2026-08-23T11:00Z
- **나머지 36건 상세**: PEPECOIN streak종료. MAPLE강한반전악화. CLOCKIN재음전전환. TIPANSEM유사. 1B h1재악화. CLUG h6재음전. FLUSH소폭개선. PEE거래재개했으나악화. 40M재반전유입. swappy유지. CYBERLEEK강한개선가속(+1729%). CC27회차째휩소(+215%). Z500대체로개선. KIRK혼조. CONK감속. CHUMP5회차째가속. HOOKR강한지속. CATE강한반전개선. GOOD전방위양전전환. PRINTER유지. BULLSHIT소폭유출. TOAD혼조. DPG혼조. FWA손익분기권. CALLOOOR전방위개선. JUGGERNAUT유지. BRODIE대체로악화. Dealer전방위재음전전환. lickingcat소폭개선. PITCOIN대체로악화. PANTS고점통과확정적. Doge2전방위대폭악화. Truth Coin(Sol)강한반전유입. BARRON고점통과지속. TRUTH(RH)지속붕괴. YOMOGI극단변동지속 · 2026-08-23T11:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **omo·MANEKI(신규) — 각각 토큰 고유 보도·KOL 언급 없음. 코로보 없음(정상 상태, 결함 아님)**.
- **나머지 39종(부모세션 최우선 확인대상 포함) — 코로보 미확인**: 이번 회차는 42개 활성종목(신규2건 포함, Dinger·WINNING 강등 2건 처리)과 notable 5종(Truth Coin·CASHCAT·STONKBROKER·PONS·ANSEM·CATSZN) 참고데이터 갱신에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-23 09:00Z)로부터 정확히 2시간 경과(정상 간격).
- **⭐이번 회차 핵심 — Dinger·WINNING 정점통과 확정**: 두 신규 토큰이 신규편입 다음 회차(2회차)에 모두 뚜렷한 정점통과 신호(유동성 급감, h1/h6 재악화 또는 급반전)를 보여 확산→뒷북으로 강등됐다. 이 패턴은 과거 TRUTH·YOMOGI(2026-08-23 09:00Z 강등)와 동일해, "신규편입 직후 1~2회차 내 정점통과"가 이 워치의 반복적 온체인 패턴임을 재확인했다.
- **LIZARD 반전 신규성**: 6회차 연속 이어지던 유동성 유출이 이번 회차 처음으로 멈추고 반전됐다. 33.9시간→35.9시간 생존, 전형적 쇠퇴경로에서 벗어날지는 계속 관찰이 필요하다.
- **DexScreener 배치 응답 누락 재확인**: 규칙에 따라 응답 개수를 요청 개수와 대조한 결과 두 배치에서 각 1건씩 누락(PEE·TRUTH)을 발견해 개별 재조회로 보완했다. 이 규칙이 실제 데이터 손실을 막은 사례로 기록한다.
- **PANTS 풀 선택 재확인**: 이번 회차도 PumpSwap이 거래량 기준 압도적 1위 풀임을 재확인했다(Meteora DLMM·DYN2 등 11개풀 중 PumpSwap 거래량 $2.02M이 나머지 전부를 상회).
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API(체인별 배치조회, 3개 배치+개별보완 2건)로 40개 기존 활성종목을 전량 확보했고, 응답 개수 불일치 2건을 규칙대로 적발·보완했다. TRUTH(RH)·Truth Coin(RH,완전소멸) 두 건은 GeckoTerminal robinhood 트렌딩 raw 데이터로 교차확인했다. GeckoTerminal 솔라나·로빈후드체인 트렌딩(page=1)으로 신규 발굴 스캔을 진행해 omo·MANEKI 2건을 확보했고, 그 과정에서 우리가 추적 중인 'Dinger'와 동명이인인 별개의 구형 'Dinger' 풀(2026-08-05 생성)도 발견해 notable에 티커충돌 경계사례로 기록했다. X 직접 조회는 로그인월로 시도하지 않아 신규 포함 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
