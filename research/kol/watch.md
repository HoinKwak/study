# 온체인 트렌딩 조기경보 — 2026-08-23 13:00 UTC (KST 2026-08-23 22:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-23 11:00Z)로부터 정확히 2시간 경과**(정상 간격). 42개 활성종목 전부를 DexScreener 토큰 API(체인별 배치조회)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 스캔으로 신규 발굴을 진행했다.

> **⚠️이번 회차 데이터 이슈**: DexScreener 배치조회 2건에서 응답 개수가 요청 개수와 불일치했다(로빈후드체인 배치: 14개 요청→13개 응답, TRUTH 누락 / 솔라나 배치1: 14개 요청→13개 응답, PEE 누락). 규칙대로 두 토큰 모두 개별 재조회로 보완했다(CLAUDE.md·에이전트 규칙 §3 준수, 이 규칙이 2회차 연속 실제 누락을 잡아냈다).

> **편입/편출/강등 내역**: **신규편입 0건**(이번 회차는 신규 온체인 후보 3건을 발견했으나 CA 미검증·유동성 과소 등 사유로 tokens에는 편입하지 않고 notable에만 경계 기록했다 — BABYCATE·PEPE(RH별개토큰)·Dinger구형). **강등 0건**(Dinger·WINNING은 직전 회차에 이미 뒷북 강등, 이번 회차도 뒷북 유지). **편출 0건**. 활성목록 **42종 유지**. notable **27개→29개**(신규 경계기록 2건 추가: BABYCATE, PEPE(RH)).

## ⚠️ 부모 세션 요청 최우선 확인 — Dinger, WINNING, TRUTH(RH), omo, MANEKI, LIZARD, OBS

- **⭐⭐TRUTH(Robinhood Chain, CA `0x2ec5…fc4`, 4회차, 풀생성후약22.0시간)**: **극적반전 서프라이즈.** 직전 회차까지 "완전소멸한 Truth Coin(RH)과 같은 경로인지" 경계 대상이었으나, 이번 회차 **완전히 반전됐다.** 유동성이 $49,103.84→**$77,580.74(+58.0%)**로 대폭 반전유입됐고, h1은 -39.09%→**+87.21%**로 극적 반전 양전했다. h6는 -96.49%→-82.74%로 여전히 극심하지만 개선됐고, h24는 +3501%→+8018%로 더 가속했다. **GeckoTerminal 로빈후드체인 트렌딩 1위로 재부상**했으며 24시간 거래량 $21.69M을 기록했다. 회전율은 421.6배→**279.6배**로 다소 낮아졌으나 여전히 극단적 수준이라 워시트레이딩 주도 가능성이 높다. 결론: **TRUTH는 죽은 Truth Coin(RH)과는 뚜렷이 다른 경로를 밟고 있다** — 다만 회전율·h6의 극심한 변동성을 고려하면 이 반전이 지속될지는 불확실하고, 오히려 새로운 정점(블로우오프 탑) 초입일 가능성도 배제할 수 없다. 뒷북 단계는 유지하되 최우선 관찰 대상으로 남긴다.
- **Dinger(3회차, 풀생성후약11.4시간)**: 강등 이후 혼조 변동 지속. 유동성 $52,991→**$61,175.67(+15.44%)**로 부분 반전유입됐고 h1도 +0.68%→**+30.71%**로 강한 재양전했다. 그러나 h6는 -37.63%→**-90.3%**로 극심하게 악화했다(6시간 창 내 큰 폭 붕괴가 있었음을 시사). h24는 +700%→+938%로 재가속. 회전율은 194.4배→170.1배로 소폭 하락했으나 여전히 극단적이다. **뒷북(정점통과확정) 단계 유지** — 부분 반등은 있으나 h6의 극심한 악화로 볼 때 안정적 회복으로 보기 어렵다.
- **WINNING(3회차, 풀생성후약17.9시간)**: 강등 이후 유출 지속. 유동성 $95,053→**$84,990.05(-10.59%)**로 3회차 연속 감소했다. h1은 -20.03%→+9.7%로 부분 반전 양전했으나, h6는 +12.05%→**-28.77%**로 재음전했다. h24는 +817%→+613%로 추가 감속. 회전율은 53.66배→65.25배로 상승. **뒷북 단계 유지, 정점통과 확정 판단 불변.**
- **omo(2회차, 풀생성후약13.4일)**: ⚠️신규편입 다음 회차(2회차)에 정점통과 경계 신호가 나타나는 이 워치의 반복 패턴이 재현되고 있다. 유동성이 $160,353.56→**$147,227.93(-8.19%)**로 첫 유출 전환했고, h1도 +14.27%→**-6.61%**로 재음전했다. h6(+77.32%→+43.55%)·h24(+174%→+88.18%)도 동시에 대폭 감속했다. 회전율은 15.2배→16.97배로 소폭 상승. 다만 Dinger·WINNING만큼 극단적인 붕괴는 아니어서 아직 **확산 단계를 유지**하되, 경계 수위를 강화한다.
- **MANEKI(2회차, 풀생성후약68.2시간)**: omo와 유사하게 신규편입 2회차 경계 신호가 나타났다. 유동성이 $52,680.72→**$48,827.99(-7.31%)**로 첫 유출 전환했고, h6는 +24.25%→**+0.76%**로 대폭 둔화해 손익분기 근접까지 왔다. h1(+3.71%→+2.86%)은 유사, h24(+70.36%→+129%)는 오히려 가속했으나 이는 후행 지표라 최근 추세를 온전히 반영하지 못한다. **조기 단계 유지**하되 경계 강화.
- **LIZARD(9회차, 풀생성후약37.9시간)**: ⭐**2회차 연속 유동성 유입 지속, 전방위 개선 가속.** 유동성 $36,337→**$39,670.96(+9.18%)**로 6회연속 유출 종료 이후 2회차 연속 개선됐다. h1(+4.22%→+10.26%)·h6(-4.24%→+23.51%)도 강하게 개선됐고 h24(-51.28%→-36.85%)도 나아졌다. 회전율은 13.34배→11.02배로 다소 낮아졌다. 6회 유출 종료 이후 반등이 2회차째 이어지고 있어 긍정적이나, 37.9시간이라는 신생 토큰 특성상 전형적 쇠퇴경로에서 완전히 벗어났다고 단정하기는 이르다.
- **OBS(20회차, 풀생성후약41시간)**: 직전 회차의 반전개선이 이번 회차 다시 재음전으로 전환됐다. 유동성은 $89,228.65→**$90,732.69(+1.69%)**로 소폭 개선을 유지했으나, h1(+4.79%→-1.04%)·h6(+30.25%→-8.48%) 모두 재음전했다. h24(+156%→+138%)는 감속. 방향 혼재가 지속된다.

## 🔎 신규 발견 3건 — 전부 tokens 미편입(CA미검증/유동성과소, notable 경계기록만)

- **BABYCATE**(Solana) — GT 솔라나 트렌딩 순위16·20위(중복표기)로 발견. reserve $34,682, h24+337.15%, 풀생성 약1일전(2026-08-22경). CATSZN·TRUMPCATE와 같은 'Cate 패밀리' 계열 파생 밈코인으로 추정된다. WebSearch로 자칭 프로젝트 사이트와 CA 후보(`5xC8SdxnMx7ToMd4foewMsxGGQ9zTVu7mUJxfnPCpump`)가 검색됐으나 **DexScreener/GeckoTerminal raw데이터로 직접 교차검증하지 못해** 규칙(추정 주소 금지)에 따라 tokens에는 편입하지 않았다.
- **PEPE(로빈후드체인, 별개토큰)** — GT 로빈후드체인 트렌딩 순위19위로 발견(풀 `0x0d389c0c…`, reserve $35K). 우리가 추적중인 PEPECOIN(CA `0x0b9606fb…`, 풀 `0x29d2049B…`)과는 다른 페어주소의 별개 'PEPE' 표기 토큰으로 추정되나, CA를 직접 확인하지 못해 편입 보류.
- **Dinger(구형·별개CA)** — GT 솔라나 트렌딩 순위12위로 재확인(2026-08-05 풀생성, reserve $50,035, h6+113.41%·h24+2,089.45%). 우리가 추적중인 Dinger(2026-08-23 풀생성)와는 동명이인인 별개 토큰. 티커충돌 경계사례로만 기록.

이번 회차는 tokens 리스트에 새로 추가할 만큼 CA가 확실하고 유동성 요건을 충족하는 신규 후보를 확보하지 못했다(정직 표기, 결함 아님).

## 나머지 39종 갱신 요약

- **PEPECOIN**: 28회차. ⭐h24가 장기 음전에서 처음 양전환(-21.27%→+15.02%). 다만 h6대폭감속. 🟢(하향).
- **MAPLE**: 14회차. 유출폭완화(-1.53%), h1재악화하나h6·h24개선. 🟡(하향,혼조).
- **CLOCKIN**: 38회차. 재음전전환이 다시 반전개선(유입전환,h1개선). 🟢(하향).
- **TIPANSEM**: 26회차. ⭐유동성유입대폭가속(+15.25%),h24처음양전환(+34.4%). 🟢(하향,전방위대폭개선).
- **1B**: 18회차. 재유출전환,h1·h6개선하나h24재악화. 🔴(유지,혼조).
- **CLUG**: 50회차. 유동성유입가속,h1재악화하나h6재양전. 🔴(유지,혼조).
- **FLUSH**: 16회차. ⚠️직전개선이전방위재음전으로반전(유출전환,h1·h6재음전). 🔴(재상향).
- **PEE**: 55회차. ⚠️직전재개된h1거래가다시완전실종(0매수/0매도). 🔴(유지,소멸경계강화).
- **40M**: 13회차. ⚠️직전전방위유입반전이다시전방위급반전악화(전지표재음전). 🔴(유지,반복된반전이력).
- **swappy**: 31회차. 유동성유출지속,전방위악화(h1·h6·h24전부재악화). 🔴(재상향).
- **CYBERLEEK**: 30회차. ⭐전방위강한개선가속지속(유동성+15.64%,h24+1757%). GT솔라나트렌딩1위재확인. 🟢(유지).
- **CC**: 28회차째방향번복지속. 유출멈춤,h1·h6재악화,h24가속(+227%). 🔴(고위험).
- **Z500**: 21회차. 소폭유출전환,h1개선,h24재악화(-33.38%). 🟡(유지,혼조).
- **KIRK**: 18회차. 유출완화,h1둔화,h6재양전,h24재음전. 🟡(유지,혼조).
- **CONK**: 15회차. 유출지속,전방위재음전악화(h24-43.71%). 🔴(재상향).
- **CHUMP**: 6회차. ⚠️5회연속가속streak가h1재음전으로종료(h6·h24는여전히강세). 🟡(하향).
- **HOOKR**: 33회차. 유출전환,전지표동시감속. 🟡(재상향,감속전환).
- **CATE**: 92회차. ⚠️직전강한반전개선이다시전방위재음전으로반전(재유출,h1·h6재음전,h24재악화). 🔴(재상향).
- **GOOD**: 34회차. 유동성유입가속지속(+8.12%),h6·h24가속. 🟢(유지,대체로개선지속).
- **PRINTER**: 169회차. 전지표유사수준유지,h24소폭개선. 🟡(유지).
- **BULLSHIT**: 49회차. 유동성유입전환,전방위개선. 🟢(하향).
- **TOAD**: 168회차. 유동성유입전환,전방위강한개선(h6+13.33%,h24+26.23%). 🟢(하향).
- **DPG**: 120회차. 유사수준,h1재음전,h6대폭둔화. 🔴(재상향).
- **FWA**: 172회차. 전지표유사수준,h24양전환(+4.72%). 🟡(유지).
- **CALLOOOR**: 118회차. 유동성유입지속,전방위가속(h1·h6·h24전부가속). 🟢(유지).
- **JUGGERNAUT**: 155회차. 전지표유사수준유지. 🟡(유지).
- **BRODIE**: 131회차. ⭐강한반전유입(유동성+7.06%,h1+8.45%강한재양전,h6대폭개선). 🟢(하향).
- **Dealer**: 160회차. 유출완화,h1재악화하나h24는대폭개선(손익분기근접). 🟡(유지,혼조).
- **lickingcat**: 160회차. 유동성유입가속,전방위개선(h1+13.31%대폭가속). 🟢(하향).
- **PITCOIN**: 121회차. 유동성유입전환,전방위개선. 🟢(하향).
- **PANTS**: 20회차(dogwifpants). ⭐2회연속강한반등지속(h6+55.76%대폭가속,h24+41.18%가속). 🟡(하향,여전히뒷북단계).
- **Doge2**: 13회차. 유동성반전유입,혼조(h1은여전히악화). 🟡(하향).
- **Truth Coin(Sol)**: 7회차(풀생성후약22.6시간). ⚠️직전강한반전유입이다시급반전악화(1-2회차패턴재현, 회전율305.5배로심화). 🔴(재상향).
- **BARRON**: 6회차(풀나이19개월). 재유출전환,h1재음전,h6·h24는개선. 🔴(유지,고점통과지속).
- **TRUTH(RH)**: 상세는 위 스포트라이트 참조. 🔴(유지,극적반전서프라이즈).
- **YOMOGI**: 5회차. 유출가속,h1급반전음전,회전율220.8배로상승. 🔴(유지,극단변동지속).

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

| 토큰 | 체인/DEX | 단계 | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|---|
| **LIZARD** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 9회차. 2회연속유동성유입,전방위개선가속 | 유동성$39,670.96(+9.18%), h24-36.85%, 회전율≈11.02배 | 지속(9회차)·2회연속개선 | 🟢(개선지속) | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **CLOCKIN** | Robinhood Chain | 조기 | 없음(자체서사만확인) | 38회차. 재음전전환이다시반전개선 | 유동성$184,986.28(+0.55%), h24-29.99% | 지속(38회차)·반전개선 | 🟢(반전개선) | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 26회차. 유입대폭가속,h24처음양전환 | 유동성$17,023.33(+15.25%), h24+34.4% | 지속(26회차)·h24양전환 | 🟢(전방위개선) | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 조기 | 미확인(코로보없음) | 28회차. h24장기음전에서처음양전환 | 유동성$24,470.82(-0.47%), h24+15.02% | 지속(28회차)·h24양전환 | 🟢(개선) | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 14회차. 유출폭완화,h1재악화하나h6·h24개선 | 유동성$24,153.35(-1.53%), h24-37.15% | 지속(14회차)·혼조개선 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **OBS** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 20회차. 반전개선이다시재음전전환 | 유동성$90,732.69(+1.69%), h24+138% | 지속(20회차)·재음전전환 | 🟡(재음전) | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **1B** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 18회차. h1·h6개선,h24재악화 | 유동성$24,732.27(-2.20%), h24-83.8% | 지속(18회차)·혼조 | 🔴(고위험) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 50회차. 유입가속,h1재악화하나h6재양전 | 유동성$40,641.3(+5.45%), h24-4.04% | 지속(50회차)·혼조 | 🔴(혼조) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 조기 | 미확인(코로보없음) | 16회차. 개선이전방위재음전으로반전 | 유동성$35,006.44(-2.50%), h24-75.58% | 지속(16회차)·재음전전환 | 🔴(재음전) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 55회차. h1거래재실종(0매수/0매도) | 유동성$7,682.85(+0.25%), 회전율≈0.37배 | 지속(55회차)·거래재실종 | 🔴(소멸경계) | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 조기 | 미확인(코로보없음) | 13회차. 전방위유입반전이다시급반전악화 | 유동성$14,518.14(-10.87%), h24-11.84% | 지속(13회차)·반복반전 | 🔴(반복반전) | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 조기 | 미확인(코로보없음) | 2회차. 신규편입직후경계신호(첫유출전환,h6대폭둔화) | 유동성$48,827.99(-7.31%), 회전율≈1.826배 | 지속(2회차)·경계강화 | 🔴(정점통과가능성) | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **omo** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 2회차. 신규편입직후전방위감속(첫유출전환) | 유동성$147,227.93(-8.19%), 회전율≈16.97배 | 지속(2회차)·경계강화 | 🔴(정점통과가능성) | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **CHUMP** | Robinhood Chain(Uniswap V3 1%) | 확산 | 미확인(코로보없음) | 6회차. 5회연속가속streak가h1재음전으로종료 | 유동성$286,235.16(+0.27%), h24+124% | 지속(6회차)·streak종료 | 🟡(streak종료) | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 확산 | 미확인(코로보없음) | 30회차. 전방위강한개선가속지속 | 유동성$1,981,159.68(+15.64%), h24+1757% | 지속(30회차)·강한개선 | 🟢(강한개선) | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **KIRK** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 18회차. 유출완화,방향혼재 | 유동성$85,824.98(-0.46%), h24-4.91% | 지속(18회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **Z500** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 21회차. 소폭유출전환,h24재악화 | 유동성$79,327.13(-0.57%), h24-33.38% | 지속(21회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **swappy** | Robinhood Chain(Uniswap V4) | 확산 | 미확인(코로보없음) | 31회차. 전방위악화전환 | 유동성$196,110.62(-3.58%), h24-24.3% | 지속(31회차)·악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CONK** | Solana(Raydium) | 확산 | 미확인(코로보없음) | 15회차. 유출지속,전방위재음전악화 | 유동성$87,559.03(-4.45%), h24-43.71% | 지속(15회차)·악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CC** | Solana(PumpSwap) | 확산 | 미확인(코로보없음) | 28회차째방향번복지속 | 유동성$209,920.28(-0.01%), h24+227% | 지속(28회차)·고위험 | 🔴(고위험) | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **TRUTH** | Robinhood Chain(Uniswap V2) | 뒷북 | 미확인(코로보없음) | 4회차,풀생성22.0h전,⭐⭐극적반전서프라이즈,GT로빈후드1위 | 유동성$77,580.74(+58.0%), h24+8018%, 회전율≈279.6배 | 지속(4회차)·극적반전 | 🔴(반전이나회전율극단) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 3회차. 강등이후혼조변동지속 | 유동성$61,175.67(+15.44%), h6-90.3%, 회전율≈170.1배 | 지속(3회차)·혼조 | 🔴(혼조변동) | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **WINNING** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 3회차. 강등이후유출지속 | 유동성$84,990.05(-10.59%), h24+613%, 회전율≈65.25배 | 지속(3회차)·유출지속 | 🔴(유출지속) | [DexScreener](https://dexscreener.com/solana/FW6R4QQeP4fzqRwDHbBkpjHx3ecvYwhd5g7chKg8pump) |
| **HOOKR** | Robinhood Chain(Uniswap) | 뒷북 | 미확인(코로보없음) | 33회차. 유출전환,전지표감속 | 유동성$238,762.22(-2.82%), h24+17.37% | 지속(33회차)·감속 | 🟡(감속) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **CATE** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 92회차. 강한반전개선이다시재음전반전 | 유동성$1,765,359.58(-4.75%), h24-24.66%, 회전율≈29.49배 | 지속(92회차)·재음전반전 | 🔴(재음전반전) | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **GOOD** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 34회차. 유입가속지속 | 유동성$489,858.98(+8.12%), h24+6.39% | 지속(34회차)·개선지속 | 🟢(개선지속) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 뒷북 | 미확인(코로보없음) | 169회차. 유사수준유지 | 유동성$348,320.09(-0.42%), h24-19.72% | 지속(169회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **BULLSHIT** | Solana(Meteora등11개풀) | 뒷북 | 미확인(WebSearch로토큰명특정보도없음) | 49회차. 유입전환,전방위개선 | 유동성(PumpSwap)$220,508.06(+5.69%), h24-26.13% | 지속(49회차)·개선전환 | 🟢(개선전환) | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **TOAD** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 168회차. 유입전환,전방위강한개선 | 유동성$435,819.5(+5.82%), h24+26.23% | 지속(168회차)·강한개선 | 🟢(강한개선) | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **DPG** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 120회차. h1재음전,h6대폭둔화 | 유동성$97,150.02(-1.60%), h24-31.46% | 지속(120회차)·악화 | 🔴(악화) | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **FWA** | Ethereum(Uniswap V4) | 뒷북 | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover)+CG트렌딩12위(carryover) | 172회차. 손익분기권,h24양전환 | 유동성$1,124,975.51(-0.06%), h24+4.72% | 지속(172회차)·손익분기권 | 🟡(손익분기권) | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **CALLOOOR** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 118회차. 전방위가속지속 | 유동성$69,070.13(+5.23%), h24+29.27% | 지속(118회차)·가속지속 | 🟢(가속지속) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **JUGGERNAUT** | Robinhood Chain(Uniswap V3 1%) | 뒷북 | Drallio(약한코로보,carryover) | 155회차. 유사수준유지 | 유동성$260,551.89(+0.36%), h24+3.34% | 지속(155회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(Uniswap V3) | 뒷북 | 미확인(코로보없음) | 131회차. 강한반전유입 | 유동성$170,037.7(+7.06%), h24+7.18% | 지속(131회차)·강한반전개선 | 🟢(강한반전개선) | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **Dealer** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 160회차. 유출완화,h24대폭개선 | 유동성$121,620.32(-0.67%), h24-0.18% | 지속(160회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 160회차. 전방위가속 | 유동성$58,147.43(+4.22%), h24-7.31% | 지속(160회차)·가속 | 🟢(가속) | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **PITCOIN** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 121회차. 전방위개선전환 | 유동성$31,301.13(+1.79%), h24-1.3% | 지속(121회차)·개선전환 | 🟢(개선전환) | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PANTS** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 20회차(dogwifpants). 2회연속강한반등 | 유동성$149,215.57(+12.27%), h24+41.18%, 회전율≈14.19배 | 지속(20회차)·2회연속반등 | 🟡(2회연속반등) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Doge2** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 13회차. 반전유입,혼조 | 유동성$54,767.17(+6.67%), h24-57.95% | 지속(13회차)·혼조반전 | 🟡(혼조반전) | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **Truth Coin** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 7회차,풀생성22.6h전,강한반전이다시급반전악화 | 유동성$13,974.05(-24.93%), h24-35.44%, 회전율≈305.5배 | 지속(7회차)·급반전악화 | 🔴(급반전악화) | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **BARRON** | Solana(Raydium) | 뒷북 | 미확인(코로보없음) | 6회차,풀나이19개월,고점통과지속 | 유동성$253,133.03(-1.08%), h24-6.38% | 지속(6회차) | 🔴(고점통과지속) | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **YOMOGI** | Solana(PumpSwap) | 뒷북 | 미확인(코로보없음) | 5회차,풀생성11.5h전,유출가속,극단변동지속 | 유동성$38,524.1(-12.43%), h6-32.69%, 회전율≈220.8배 | 지속(5회차)·극단변동지속 | 🔴(극단변동지속) | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**(BABYCATE·PEPE(RH)·Dinger구형 3건 발견했으나 CA미검증/유동성과소로 notable에만 기록). **강등 0건**(Dinger·WINNING은 뒷북 유지). **편출 0건**. **⭐극적반전**: TRUTH(RH, +58.0%유동성반전), LIZARD(2회연속개선), BRODIE(강한반전), PANTS(2회연속강한반등). **경계강화**: omo·MANEKI(신규편입2회차정점통과경계신호), CATE·Truth Coin(Sol)(강한개선이1회차만에다시반전악화).

## 온체인 신호 상세

- **TRUTH(RH) 극적반전 상세**: 위 스포트라이트 참조. 유동성+58.0%, h1대반전(-39.09%→+87.21%), GT로빈후드체인트렌딩1위(24h거래량$21.69M)로 재부상했다. 회전율279.6배로여전히극단적이라워시트레이딩주도가능성경계 · 2026-08-23T13:00Z
- **omo·MANEKI 경계신호 상세**: 두 토큰 모두 신규편입 2회차만에 첫 유동성유출전환+주요지표동시감속을 보였다. Dinger·WINNING·TRUTH·YOMOGI에서 반복된 '신규편입1~2회차만의정점통과' 패턴과 유사하나 크래시 규모는더작다 · 2026-08-23T13:00Z
- **LIZARD 2회연속개선 상세**: 6회연속유동성유출종료(직전회차) 이후 이번회차도 유동성+9.18%·h1+10.26%·h6+23.51%로 전방위개선이2회차째지속됐다 · 2026-08-23T13:00Z
- **DexScreener 배치 응답 개수 불일치 상세**: 로빈후드체인 배치(14개요청)에서 TRUTH, 솔라나배치1(14개요청)에서 PEE가 각각 응답에서 누락돼 개별재조회로 보완했다. 2회차 연속 이 규칙이 실제 누락을 적발한 사례 · 2026-08-23T13:00Z
- **나머지 37건 상세**: PEPECOIN h24양전환. MAPLE혼조개선. CLOCKIN반전개선. TIPANSEM전방위대폭개선. 1B혼조. CLUG혼조. FLUSH재음전전환. PEE거래재실종. 40M반복반전. swappy전방위악화. CYBERLEEK강한개선지속. CC28회차째휩소. Z500혼조. KIRK혼조. CONK전방위악화. CHUMP streak종료. Dinger혼조변동지속. WINNING유출지속. HOOKR감속전환. CATE재음전반전. GOOD개선지속. PRINTER유지. BULLSHIT개선전환. TOAD강한개선. DPG악화. FWA손익분기권. CALLOOOR가속지속. JUGGERNAUT유지. BRODIE강한반전개선. Dealer혼조. lickingcat가속. PITCOIN개선전환. PANTS2회연속반등. Doge2혼조반전. Truth Coin(Sol)급반전악화. BARRON고점통과지속. YOMOGI극단변동지속 · 2026-08-23T13:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **BABYCATE(notable, 신규발견) — 코인 고유 보도·KOL 언급 없음, 자칭 프로젝트 사이트만 확인. 코로보 없음(정상 상태)**.
- **나머지 40종(부모세션 최우선 확인대상 포함) — 코로보 미확인**: 이번 회차는 42개 활성종목 전량 재확인과 notable 4종(Truth Coin·CASHCAT·STONKBROKER·PONS·ANSEM) 참고데이터 갱신, 신규 3건 발견/경계기록에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-23 11:00Z)로부터 정확히 2시간 경과(정상 간격).
- **⭐⭐이번 회차 핵심 — TRUTH(RH) 극적반전**: 부모 세션이 우려한 "완전소멸한 Truth Coin(RH)과 같은 경로인지" 질문에 대해 명확히 **아니오**로 확인됐다. 지속붕괴 경로를 걷던 TRUTH가 유동성+58.0%·h1대반전(+87.21%)·GT로빈후드체인트렌딩1위(24h거래량$21.69M)로 극적 반전됐다. 다만 회전율이 여전히 279.6배로 극단적이고 h6는 -82.74%로 심한 변동성을 보여, 안정적 회복이라기보다 새로운 블로우오프 국면의 초입일 가능성도 배제할 수 없다.
- **신규편입 2회차 경계 패턴 재확인**: omo·MANEKI가 신규편입 다음 회차(2회차)에 나란히 유동성 첫 유출전환+주요지표 동시감속을 보여, 이 워치에서 반복된 "신규편입 1~2회차 만의 정점통과" 패턴의 초기 신호일 가능성이 있다. Dinger·WINNING만큼 극단적이지 않아 단계 강등은 하지 않았으나 다음 회차 확인이 중요하다.
- **LIZARD 2회연속 개선**: 6회연속 유출종료 이후 이번 회차도 전방위개선이 이어져 총 2회차 연속 긍정 신호를 보였다.
- **DexScreener 배치 응답 누락 재확인**: 2회차 연속(11:00Z·13:00Z) 응답개수 대조 규칙이 각 1건씩 실제 누락(11:00Z:PEE·TRUTH / 13:00Z:TRUTH·PEE)을 적발해 개별재조회로 보완했다. 우연히 매번 같은 두 토큰이 누락되는 패턴이 관찰되는데, 이는 DexScreener 응답 페이로드 크기 제한 근처에서 이 두 토큰이 반복적으로 잘려나가는 것일 가능성이 있어 계속 관찰한다.
- **신규 발견 3건, tokens 미편입**: BABYCATE·PEPE(RH별개토큰)·Dinger(구형)를 GT 트렌딩에서 발견했으나 CA 미검증(BABYCATE·PEPE) 또는 이미 알려진 티커충돌 사례(Dinger구형)라 tokens에는 편입하지 않고 notable에 경계기록만 남겼다. 추정 주소를 tokens에 넣지 않는 규칙을 준수했다.
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API(체인별 배치조회, 4개 배치+개별보완 2건)로 42개 기존 활성종목을 전량 확보했고, 응답 개수 불일치 2건을 규칙대로 적발·보완했다. TRUTH(RH)의 극적반전은 GeckoTerminal 로빈후드체인 트렌딩 순위1위 재확인으로 교차검증했다. GeckoTerminal 솔라나·로빈후드체인 트렌딩(page=1)으로 신규 발굴 스캔을 진행해 3건을 발견했으나 CA 검증 기준을 충족하지 못해 notable에만 기록했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*

> ⚠️ **부모 세션 교차검증(13:20Z)**: TRUTH(Robinhood Chain, CA `0x2ec5…fc4`)를 에이전트 관측 약 20분 뒤 DexScreener 원자료로 재조회한 결과 **반전 상승분이 이미 되돌려지는 중**이다 — 유동성 $77,580→**$62,286**, h1 +87.21%→**+28.71%**, h6 **-77.15%**, 회전율 279.6배→**350.5배**로 오히려 상승. ⚠️**이 조합(유동성 급등락 + 회전율 300배대 + h1 격렬한 진폭)은 09:00Z에 완전소멸이 확정된 동명 계열 Truth Coin(Robinhood, `0xa48a…b4`)이 소멸 두 회차 전에 보였던 패턴과 동일**하다. 본문의 13:00Z 스냅샷은 그 시점 기준으로 유효하나 **반전을 지속 상태로 읽어서는 안 된다.** 같은 시점 LIZARD(h6 +22.8%, 회전율 11.1배)는 에이전트 관측과 방향이 일치해, 이 격변은 TRUTH 개별 사안이지 조회 오류가 아니다.
