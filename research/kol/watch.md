# 온체인 트렌딩 조기경보 — 2026-08-23 19:00 UTC (KST 2026-08-24 04:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **이번 회차는 직전(2026-08-23 17:00Z)로부터 정확히 2시간 경과**(정상 간격). 44개 활성종목 전부를 DexScreener 토큰 API(5개 이하 소규모 배치조회)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 API로 신규 발굴 및 교차검증을 진행했다.

> **⚠️데이터 절차 준수**: ①DexScreener 배치를 5개 이하로 유지했으나 이번 회차도 9개 배치 중 3개 배치에서 각 1~2개 토큰이 누락돼(TIPANSEM·40M·swappy·CHUMP·WINNING이 한 배치, DPG가 한 배치, PITCOIN이 한 배치) 개별 재조회로 전부 보완했다 — 5개 이하 배치에서도 완전한 누락 방지가 보장되지 않으므로 매 배치 응답 개수를 반드시 요청 개수와 대조할 것. ②BRODIE는 동일 토큰주소에 풀이 2개(0x9870C395…$173,098 vs 0x46BF126A…$33,301) 존재해 "최대거래량" 자동선택이 추적 연속성이 없는 풀을 고르는 오류가 실측 확인됐다 — 기존 추적 풀(0x9870C395…)로 수동 고정해 연속성을 유지했다(규칙 위반 방지 사례로 기록).

> **편입/편출/강등 내역**: **신규편입 1건**(PROLOGUE — 확산, GT 로빈후드체인 트렌딩 발굴). **편출 1건**(WINNING — 6회연속유출로 유동성 $46,801→$5,947 붕괴, 임계선 아래로 이관). 활성목록 **44→44종**(순증감 0). notable **29→32개**(WINNING·CATLIST·AI/NVDA 신규 이관/추가).

## ⭐ 부모 세션 요청 최우선 확인 6건

### 1. TRUTH — h1/h6/h24 전부 기록, 24h 창 회전 지속 확인

| 시점 | 유동성 | h1 | h6 | h24 | 회전율 |
|---|---|---|---|---|---|
| 13:00Z | $77,580.74 | +87.21% | -82.74% | — | 279.6배 |
| 13:20Z(부모 교차검증) | $62,286 | +28.71% | -77.15% | — | 350.5배 |
| 15:00Z | $75,831.23 | +3.79% | +76.63% | — | ≈300.1배 |
| 17:00Z | $114,711.44 | +188% | +308% | -59.64% | ≈195.7배 |
| 17:20Z(부모 교차검증) | $106,522 | +170% | +114% | **-70.8%(본문 누락분)** | 208.9배 |
| **19:00Z(이번 회차)** | **$147,532.29** | **+144%** | **+149%** | **-74.53%** | **≈144.8배** |

**결론**: 부모 세션이 지적한 대로 이번 회차는 h1·h6·h24 세 값을 전부 명시한다. 유동성은 5회 연속 관측 중 최고치인 $147,532.29까지 추가 확장됐다(+28.6%). h1·h6는 각각 +144%·+149%로 전 회차보다 감속했으나 여전히 극단적 수준이고, **h24는 -74.53%로 오히려 더 깊어졌다** — 풀 나이가 이제 약 28.1시간으로 24h 창이 완전히 회전한 상태가 이어지며, 런치 시점 펌프분이 계속 창 밖으로 빠져나가는 동안 단기(1h·6h) 반등이 겹쳐지는 패턴이 5회 연속 반복되고 있다. GeckoTerminal 로빈후드체인 트렌딩 9위(reserve $151,470, h1+136.21%·h6+240.59%·h24-70.86%)로 방향은 대체로 일치. 회전율은 195.7배→144.8배로 계속 하락(과거 300배대 대비 크게 완화)해 극단적 초고회전은 다소 진정됐으나 여전히 매우 높다. **"단기 급등"과 "24시간 기준 깊은 손실"이 공존하는 상태이며, 24h 창 회전에 의한 착시임을 계속 경계해야 한다.**

### 2. CYBERCAT·CATALORIAN — 부모 경고한 "1~2회차 만의 정점 통과" 패턴 정확히 재현

두 토큰 모두 이번 2회차 관측에서 **부모 세션이 경고한 패턴이 그대로 나타났다.**

- **CYBERCAT**(풀생성후 약 5.8시간): 유동성 $68,279.63→**$65,309.28(-4.3%, 경미 유출)**, h1 **-11.81%→-35.63%(급반전 음전)**, h6·h24 +1255%→+1090%(감속). GT 재확인(솔라나 트렌딩 9위, reserve $61,517)로 대체로 일치.
- **CATALORIAN**(풀생성후 약 7.3시간): 유동성 $421,094.74→**$333,402.83(-20.8%, 대폭 유출)**, h1 **+14.78%→-9.67%(재음전)**, h6 +14,930%→+533%(대폭 감속), h24 +14,930%→+9212%(감속). GT 재확인(솔라나 트렌딩 3위, reserve $333,266)로 교차검증.

**결론**: 두 토큰 모두 2회차 만에 유동성 유출 전환 + h1 재음전이 동시에 나타나 "정점 통과 확정 단계"로 진입한 것으로 판단한다. 이 워치에서 반복 관측된 패턴("신규 편입 1~2회차 만의 정점 통과")이 이번에도 정확히 재현됐다. 두 토큰 모두 리스크를 상향(🔴)한다.

### 3. LIZARD — 3회연속 개선 streak 종료 후 2회 연속 유출로 쇠퇴 재진입

직전 회차(17:00Z)에서 3회 연속 유입 streak가 종료됐고, **이번 회차도 유출이 이어졌다(2회 연속 유출)**. 유동성 $36,987.06→**$34,097.24(-7.8%)**, h1(-14.66%→-5.63%, 개선), h6(+2.79%→**-25.81%**, 재악화), h24(-27.33%→-43.55%, 악화). **"하락으로 굳어지는지"에 대한 부모 세션 질문에 답하면 — 이번 회차까지 2회 연속 유출로 쇠퇴 경로 재진입 신호가 강화됐다.** 다만 h1이 개선된 점은 완전한 단조 붕괴는 아님을 시사한다.

### 4. omo·MANEKI — 재수렴에서 다시 재분기

- **MANEKI**: 3회 연속 유출 경고가 있었으나 **이번 회차 4회 만에 강하게 반전 개선**됐다. 유동성 $44,153.35→**$52,977.09(+20.0%)**, h1(+1.09%→+16.87%), h6(-28.49%→+15.08%, 강한 반전), h24(+35.86%→+93.98%, 가속). GT 재확인(로빈후드체인 20위, reserve $52,863)로 일치.
- **omo**: 직전 회차 재악화가 **이번 회차도 2회 연속 유출로 지속**됐다. 유동성 $134,695.17→**$125,298.62(-7.0%)**, h1(-14.82%→-6.49%, 개선), h6(-35.64%→-26.77%, 개선), h24(+91.39%→+55.67%, 감속).

**두 토큰이 직전 회차 모두 약세로 수렴했다가, 이번 회차 다시 갈라졌다(MANEKI 강한개선 vs omo 지속약세).** 이 워치가 지속적으로 강조해온 대로, 이런 반복 패턴은 회차마다 뒤집힐 수 있어 절대적 신뢰는 금물이다.

### 5. WINNING — 6회연속 유출로 유동성 붕괴, 편출 처리

5회 연속 유출 이후 h1 급락이 멈춰 바닥권 근접 가능성을 봤으나, **이번 회차 오히려 유동성이 87.3% 붕괴**했다. 유동성 $46,801.56→**$5,947.69(-87.3%)**, h1(+0.49%→-82.7%), h6(-76.9%→-99.28%), h24(+114%→-94.78%). GT 재확인(솔라나 트렌딩 10위, reserve $5,964)로 일치 확인. volume.h24가 $6.37M로 유동성 대비 1000배가 넘는 회전율은 **잔여 유동성이 먼지 수준일 때 나타나는 산술 아티팩트**(절차 규칙 6번)로 해석한다. **6회 연속 유출이 확정되며 소멸 단계 최종국면으로 판단, 이번 회차 활성목록(tokens)에서 notable로 편출한다.**

### 6. CLUG — 강한개선 2회차째 유지가 3회차 만에 종료

직전 강한 반전개선이 2회차째 유지됐으나, **이번(3회차) 회차 유출 전환과 함께 종료됐다**. 유동성 $44,497.67→**$40,358.11(-9.3%)**, h1(+13.58%→-7.31%, 재음전), h6(+29.06%→-2.4%, 재음전), h24(+30.14%→+3.52%, 대폭 감속하나 양전 유지). h24가 아직 양전이라 완전한 반전은 아니나, 51회차 넘는 장기 혼조 이력을 감안해 신중을 유지한다.

## 🆕 신규 발굴 — PROLOGUE (Robinhood Chain)

GeckoTerminal 로빈후드체인 트렌딩 스캔(15위)에서 발굴, DexScreener로 교차검증했다.

- **PROLOGUE**(Robinhood Chain/Uniswap, CA `0xb9972ca7188e511174947e3936a5315ac7073277`, 풀생성후 약 6.1일): 유동성 $160,064.43, h1 -3.68%(둔화 조짐), h6 +48.84%, h24 +126%. **h1<h6<h24 패턴은 최근 24시간 대비 최근 1시간의 모멘텀이 식고 있음을 시사** — 신생 초조기 토큰은 아니고(풀 나이 6일), 이미 상당 부분 상승한 뒤 감속 국면에 진입했을 가능성이 있다. 24h 거래량 $865,893.50, 회전율 ≈5.4배(다른 신생 토큰 대비 완만). "확산" 단계로 신중하게 편입한다.

(솔라나 트렌딩에서도 CATLIST/"고양이밈" 클러스터 확장 등이 발굴됐으나, 이미 h6가 대폭 조정 중(-60.23%)이라 CYBERCAT·CATALORIAN과 유사하게 "당일 정점 통과" 우려가 있어 tokens 편입은 보류하고 notable로만 기록했다. 상세는 notable 섹션 참조.)

## 그 밖 추적 항목 갱신(핵심만)

- **CATE(95회차)**: 2회 연속 유동성 유출로 악화가 심화됐다. 유동성 $1,768,690.2→$1,644,954.25(-7.0%), h6(-11.61%→-15.73%), h24(-27.2%→-44.05%, 악화).
- **CYBERLEEK(33회차)**: 유입이 다시 유출로 반전, 모멘텀 급속 둔화. 유동성 -12.5%, h6(+8.42%→-39.07%, 급반전 음전), h24(+923%→+313%, 대폭 감속).
- **BULLSHIT(52회차)**: 재유출이 강한 반전개선으로 전환. 유동성 +15.0%, h1(-1.39%→+38.45%), h24(-20.13%→+7.58%, 반전 양전).
- **DPG(123회차)**: 직전 대폭 악화 심화 경고가 이번 회차 강하게 반전됐다. 유동성 +15.4%, h1(-35.53%→+21.39%, 강한 반전), 다만 h6·h24는 여전히 깊은 음전권(-59.8%·-57.63%).
- **Truth Coin(Solana, 10회차)**: 직전 첫 유입 반전이 1회차 만에 다시 재유출로 돌아섰고, 거래활동도 계속 급감 중이다(24h 거래량 $447,432.81→$181,505.96, 회전율 32.5배→16.1배). 관심 소멸 신호가 강화됐다.
- **BRODIE(134회차)**: ⚠️데이터 검증 사례 — 동일 토큰주소에 풀이 2개 존재함을 확인, 추적 연속성 유지를 위해 기존 풀(0x9870C395…)로 고정. 유동성 +3.0%, h24 재양전.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인(코로보없음) | 5회차. 3회연속유출이4회만에강한반전 | 유동성$52,977.09(+20.0%), h24+93.98% | 지속(5회차)·강한반전 | 🟡(반전개선) | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사만확인) | 41회차. 40회차만의개선이대체로유지 | 유동성$208,145.04(-4.1%), h6+24.42%(강한양) | 지속(41회차)·개선유지 | 🟢(유지) | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **1B** | Robinhood Chain(Uniswap) | 미확인(코로보없음) | 21회차. 유출이유입으로반전,전방위개선 | 유동성$22,960.29(+7.3%), h24-40.89% | 지속(21회차)·전방위개선 | 🟡(개선) | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인(코로보없음) | 29회차. 2회연속유출이유입으로반전 | 유동성$16,058.9(+2.5%), h24+45.59% | 지속(29회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **MAPLE** | Solana(PumpSwap) | 미확인(코로보없음) | 17회차. 유입재전환,h24는악화 | 유동성$24,041.12(+1.0%), h24-41.77% | 지속(17회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLUG** | Solana(PumpSwap) | 미확인(코로보없음) | 53회차. 2회연속강한개선streak종료 | 유동성$40,358.11(-9.3%), h24+3.52%(양전유지) | 지속(53회차)·streak종료 | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **PEPECOIN** | Robinhood Chain(Uniswap V3) | 미확인(코로보없음) | 31회차. 완만한유출·음전지속 | 유동성$20,794.84(-3.1%), h24-15.88% | 지속(31회차)·완만한하락 | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **40M** | Solana(PumpSwap) | 미확인(코로보없음) | 16회차. 유사,전방위완만한개선 | 유동성$11,301.46(-0.7%), h24-49.91% | 지속(16회차)·완만한개선 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인(코로보없음) | 2회차. 부모경고패턴재현,h1급반전음전 | 유동성$65,309.28(-4.3%), h1-35.63% | 지속(2회차)·정점통과경계 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |
| **OBS** | Robinhood Chain(Uniswap) | 미확인(코로보없음) | 23회차. 1회차개선이다시전방위재악화 | 유동성$79,093.2(-14.1%), h1-28.53% | 지속(23회차)·재악화 | 🔴(재상향) | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인(코로보없음) | 19회차. 유입전환이재유출로반전 | 유동성$27,382.35(-21.9%), h24-70.88% | 지속(19회차)·악화 | 🔴(유지) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인(코로보없음) | 58회차. 재유출지속,극저유동 | 유동성$6,866.11(-6.4%) | 지속(58회차)·극저유동 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **LIZARD** | Solana(PumpSwap) | 미확인(코로보없음) | 12회차. streak종료후2회연속유출로쇠퇴재진입 | 유동성$34,097.24(-7.8%), h24-43.55% | 지속(12회차)·쇠퇴재진입 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **CHUMP** | Robinhood Chain(Uniswap V3 1%) | 미확인(코로보없음) | 9회차. 유출가속이유입으로강한반전 | 유동성$302,936.66(+11.7%), h24+96.27% | 지속(9회차)·반전개선 | 🟢(개선) | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인(코로보없음) | 1회차(신규). GT15위발굴,풀나이6.1일,h1둔화조짐 | 유동성$160,064.43, h24+126% | **신규편입** | 🟡(신규,감속조짐) | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인(코로보없음) | 2회차. 부모경고패턴정확히재현,대폭유출+h1재음전 | 유동성$333,402.83(-20.8%), h24+9212% | 지속(2회차)·정점통과확정 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **CONK** | Solana(Raydium) | 미확인(코로보없음) | 18회차. 유출이유입으로재반전 | 유동성$91,227.07(+7.8%), h24-43.29% | 지속(18회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **KIRK** | Solana(PumpSwap) | 미확인(코로보없음) | 21회차. 안정화흐름일부되돌림 | 유동성$74,974.23(-0.6%), h24-6.22% | 지속(21회차)·되돌림 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **swappy** | Robinhood Chain(Uniswap V4) | 미확인(코로보없음) | 34회차. 전지표대체로횡보 | 유동성$197,140.77(-0.5%), h24-15.78% | 지속(34회차)·횡보 | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **Z500** | Solana(PumpSwap) | 미확인(코로보없음) | 24회차. streak종료이후약세지속 | 유동성$79,520.97(-6.9%), h24-24.57% | 지속(24회차)·약세지속 | 🟡(유지) | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인(코로보없음) | 33회차. 유입이재유출로반전,모멘텀급속둔화 | 유동성$1,627,443.02(-12.5%), h24+313% | 지속(33회차)·모멘텀둔화 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인(코로보없음) | 31회차째방향번복,h1대폭감속 | 유동성$269,094.09(+2.1%), h24+445% | 지속(31회차)·고위험 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **omo** | Solana(PumpSwap) | 미확인(코로보없음) | 5회차. 2회연속유출지속,MANEKI와재분기 | 유동성$125,298.62(-7.0%), h24+55.67% | 지속(5회차)·2회연속유출 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **BULLSHIT** | Solana(Meteora등10개풀) | 미확인(WebSearch로토큰명특정보도없음) | 52회차. 재유출이강한반전개선으로전환 | 유동성$256,830.03(+15.0%), h24+7.58% | 지속(52회차)·강한반전개선 | 🟢(개선) | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **GOOD** | Robinhood Chain(Uniswap V3) | 미확인(코로보없음) | 37회차. 유입재개2회연속 | 유동성$491,598.74(+4.6%), h24+16.84% | 지속(37회차)·2회연속개선 | 🟢(개선) | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover)+CG트렌딩12위(carryover) | 175회차. 전지표지속개선 | 유동성$1,276,898.38(+8.7%), h24+32.83% | 지속(175회차)·개선가속 | 🟢(개선) | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인(코로보없음) | 123회차. 대폭악화심화가강하게반전 | 유동성$61,515.18(+15.4%), h1+21.39% | 지속(123회차)·강한반전 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **JUGGERNAUT** | Robinhood Chain(Uniswap V3 1%) | Drallio(약한코로보,carryover) | 158회차. 안정적유지 | 유동성$262,576.54(-1.3%), h24+12.24% | 지속(158회차)·안정적 | 🟢(유지) | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(Uniswap V3) | 미확인(코로보없음) | 134회차. 소폭개선지속,h24재양전 | 유동성$173,098.44(+3.0%), h24+2.41% | 지속(134회차)·소폭개선 | 🟢(개선) | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **Doge2** | Solana(PumpSwap) | 미확인(코로보없음) | 16회차. 유입지속,h1강한재양전 | 유동성$60,347.51(+9.4%), h1+56.2% | 지속(16회차)·개선지속 | 🟢(개선) | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **PITCOIN** | Solana(PumpSwap) | 미확인(코로보없음) | 125회차. h1재음전,대체로안정 | 유동성$32,119.53(-0.6%), h24+2.86% | 지속(125회차)·안정적 | 🟢(유지) | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인(코로보없음) | 121회차. 혼조지속 | 유동성$65,698.76(+1.7%), h24+29.28% | 지속(121회차)·혼조 | 🟡(혼조) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **PRINTER** | Robinhood Chain(Uniswap V4) | 미확인(코로보없음) | 172회차. 전지표유사수준 | 유동성$329,899.54(-1.6%), h24-21.21% | 지속(172회차) | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인(코로보없음) | 36회차. 재양전반전이완만한되돌림 | 유동성$233,627.12(-6.9%), h24+36.76% | 지속(36회차)·되돌림 | 🟡(유지) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **CATE** | Solana(PumpSwap) | 미확인(코로보없음) | 95회차. 2회연속유출로악화심화 | 유동성$1,644,954.25(-7.0%), h24-44.05% | 지속(95회차)·악화심화 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **TOAD** | Solana(PumpSwap) | 미확인(코로보없음) | 171회차. 재양전반전이1회차만에재음전 | 유동성$397,121.48(-5.2%), h24+7.46% | 지속(171회차)·재악화 | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **Dealer** | Solana(PumpSwap) | 미확인(코로보없음) | 163회차. 반전개선이1회차만에재악화 | 유동성$114,171.4(-3.9%), h24-16.03% | 지속(163회차)·재악화 | 🟡(재상향) | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인(코로보없음) | 163회차. 장기개선streak약화 | 유동성$56,575.72(-6.9%), h24+2.2% | 지속(163회차)·streak약화 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **Truth Coin** | Solana(PumpSwap) | 미확인(코로보없음) | 10회차. 첫유입반전이1회차만에재유출,거래활동급감 | 유동성$11,241.91(-18.2%), 회전율≈16.1배 | 지속(10회차)·거래활동급감 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **TRUTH** | Robinhood Chain(Uniswap V2) | 미확인(코로보없음) | 7회차,5회연속관측,박스권상단추가확장,h24-74.53%로심화 | 유동성$147,532.29(+28.6%), 회전율≈144.8배 | 지속(7회차)·박스권추가확장 | 🔴(최상위경계) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **Dinger** | Solana(PumpSwap) | 미확인(코로보없음) | 6회차. 대폭유출전환,h6급격악화 | 유동성$37,466.98(-26.9%), h6-57.95% | 지속(6회차)·대폭유출 | 🔴(재상향) | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **BARRON** | Solana(Raydium) | 미확인(코로보없음) | 9회차,고점통과지속 | 유동성$244,357.49(-1.8%), h24-37.09% | 지속(9회차) | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **PANTS** | Solana(PumpSwap) | 미확인(코로보없음) | 23회차(dogwifpants). 조정지속,h6추가악화 | 유동성$123,431.28(-5.2%), h6-32% | 지속(23회차)·조정심화 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **YOMOGI** | Solana(PumpSwap) | 미확인(코로보없음) | 8회차,유입강화,h1재음전급락 | 유동성$40,261.13(+21.6%), 회전율≈217.9배 | 지속(8회차)·극단변동지속 | 🔴(유지) | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 1건**(PROLOGUE-확산). **편출 1건**(WINNING — 6회연속유출로유동성87.3%붕괴, notable로이관). **경계강화(정점통과경계)**: CYBERCAT·CATALORIAN(부모경고패턴정확히재현), LIZARD(쇠퇴재진입), Dinger(대폭유출), Truth Coin(Sol,거래활동급감). **강한개선**: MANEKI(4회만에반전), CHUMP, BULLSHIT, DPG(반전), GOOD, FWA. **재악화(반전개선이1회차만에번복)**: OBS, TOAD, Dealer, CLUG(streak종료).

## 온체인 신호 상세

- **TRUTH 5회연속관측 상세**: 위 스포트라이트 섹션 참조. h1/h6/h24 전부 명시, 박스권$62K~$90K가5회연속관측중$147.5K까지추가확장, 회전율은195.7배→144.8배로하락지속 · 2026-08-23T19:00:00Z
- **CYBERCAT·CATALORIAN 정점통과 상세**: 부모경고["신규편입1~2회차만의정점통과패턴"]가2회차관측에서정확히재현. 두토큰모두유동성유출전환+h1재음전동시발생 · 2026-08-23T19:00:00Z
- **LIZARD 쇠퇴재진입 상세**: 3회연속유입streak종료이후2회연속유출로쇠퇴경로재진입, h1은개선하나h6재악화 · 2026-08-23T19:00:00Z
- **omo·MANEKI 재분기 상세**: 직전회차수렴됐던두토큰이이번회차다시분기(MANEKI4회만에강한반전, omo2회연속유출지속) · 2026-08-23T19:00:00Z
- **WINNING 붕괴·편출 상세**: h1급락멈춤이후안정화가능성을봤으나6회연속유출확정,유동성87.3%붕괴로임계선아래로이관 · 2026-08-23T19:00:00Z
- **CLUG streak종료 상세**: 2회연속강한개선이3회차만에유출전환으로종료, h24는아직양전유지 · 2026-08-23T19:00:00Z
- **PROLOGUE 신규발굴 상세**: GT로빈후드체인트렌딩15위에서발굴,DS교차검증완료. 풀나이6.1일,h1<h6<h24패턴으로단기모멘텀감속조짐 · 2026-08-23T19:00:00Z
- **DexScreener 배치조회 부분누락 재확인**: 9개배치중3개배치에서각1~2개토큰누락(TIPANSEM·40M·swappy·CHUMP·WINNING한배치,DPG한배치,PITCOIN한배치)됐으나전부개별재조회로보완완료. 5개이하배치에서도완전누락방지는보장되지않음을재확인 · 2026-08-23T19:00:00Z
- **BRODIE 풀선정오류 방지 상세**: 동일토큰주소에풀2개존재(추적풀$173,098vs별도풀$33,301)확인,추적연속성을위해기존풀로수동고정 · 2026-08-23T19:00:00Z
- **나머지 상세**: PEPECOIN완만한하락지속. MAPLE혼조. TIPANSEM혼조(유입반전). 1B전방위개선. FLUSH악화. PEE극저유동지속. 40M완만한개선. swappy횡보. CYBERLEEK모멘텀급속둔화. CC고위험지속. Z500약세지속. KIRK일부되돌림. CONK혼조. CHUMP반전개선. Dinger대폭유출. HOOKR되돌림. CATE악화심화. GOOD2회연속개선. PRINTER유지. TOAD재악화. FWA개선가속. CALLOOOR혼조. JUGGERNAUT안정적. Dealer재악화. lickingcat streak약화. PITCOIN안정적. PANTS조정심화. Doge2개선지속. Truth Coin(Sol)거래활동급감. BARRON고점통과지속. YOMOGI극단변동지속 · 2026-08-23T19:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **PROLOGUE(신규) — 이번 회차는 GT/DS 온체인 확인에만 집중, KOL/뉴스 검색은 진행하지 않았다(다음 회차 이후 우선순위상 검토)**. 정상 상태(미확인).
- **나머지 43종 — 코로보 미확인**: 이번 회차는 44개 활성종목(신규 1건 포함) 전량 재확인, 부모 세션 우선확인 6건 처리, GT 트렌딩 신규발굴에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-23 17:00Z)로부터 정확히 2시간 경과(정상 간격).
- **⭐부모 세션 우선확인 6건 전부 처리**: ①TRUTH — h1/h6/h24 전부 기록, 24h 창 회전 지속으로 h24 -74.53%까지 심화, 박스권 상단 추가 확장($147.5K) ②CYBERCAT·CATALORIAN — 부모경고["1~2회차만의정점통과패턴"]가 정확히 재현됨(둘다유출전환+h1재음전) ③LIZARD — streak종료후2회연속유출로쇠퇴경로재진입 ④omo/MANEKI — 재수렴에서다시재분기(MANEKI강한반전vs omo지속약세) ⑤WINNING — 6회연속유출확정,유동성87.3%붕괴로편출처리 ⑥CLUG — 강한개선2회차째유지가3회차만에종료(h24는양전유지).
- **데이터 절차 위반 방지 사례 2건**: ①DexScreener 5개이하 배치에서도 부분누락이 재발(TIPANSEM·40M·swappy·CHUMP·WINNING, DPG, PITCOIN 3개 배치에서 누락) — 매 배치 응답 개수 대조·개별재조회로전부보완 ②BRODIE 동일토큰주소 풀2개혼동위험 실측적발, 추적연속성유지위해기존풀로수동고정.
- **"고양이밈" 테마 클러스터 추가 확장**: CATE·CATSZN·BABYCATE·TRUMPCATE·CATALORIAN·CYBERCAT에 이어 이번 회차 **CATLIST**(CAT SEASON CLUB)까지 발견돼 클러스터가 더 커졌다. CATLIST는 h6가 이미 -60.23%로 대폭 조정 중이라 tokens 편입은 보류하고 notable로만 기록했다.
- **AI/NVDA 토큰화 합성자산 발견**: 로빈후드체인 BANKR dex에서 "AI/NVDA" 명의 토큰화 합성자산(유동성 $4.2M, 이미 확립된 자산)을 발견해 notable에 새로 기록했다. 전형적 조기 밈코인과는 성격이 달라 시장 전반 주목 대상으로만 분류한다.
- **Truth Coin(Solana) 거래활동 지속 급감**: 직전 회차의 첫 유입 반전이 1회차 만에 다시 재유출로 돌아섰고, 24h 거래량도 추가로 절반 넘게 줄었다(회전율 32.5배→16.1배). 유동성 지표만으로는 포착하기 어려운 활동 소멸 신호로 계속 기록한다.
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API로 44개 활성종목(신규 1건 포함)을 5개 이하 소규모 배치 위주로 확보했으나 일부 배치에서 부분 누락이 재발해 개별 재조회로 전량 보완했다. GeckoTerminal은 API 엔드포인트(`api.geckoterminal.com`)가 정상 응답해 신규발굴·교차검증에 활용했다. TRUTH는 GT·DS 교차검증으로 방향 일치를 확인했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*

> ⚠️ **부모 세션 교차검증(19:20Z)**: TRUTH(`0x2ec5…fc4`)를 재조회하니 유동성이 $147,532→**$234,330**으로 더 확대되고 h1 +475%·h6 +834%로 가속했으며, **h24는 -74.53%→-35.02%로 개선**됐다(회전율 144.8→92.6배로 3회차 연속 하락). "단기 급등 + 24h 기준 손실 공존" 구조는 유지되나 손실폭 축소와 회전율 하락은 워시트레이딩 비중이 줄고 있을 가능성을 시사한다(단정하지 않고 관측만 기록). 또한 이번 회차 notable에 신규 기록된 **AI/NVDA(BANKR)는 토큰화 주식/합성자산**으로, 이 프로젝트가 선물 브리핑에서 명시적으로 배제하는 자산군이자 이 워치(신생·밈 온체인 조기경보)의 대상도 아니다 — **관측 기록으로만 남기고 향후 tokens로 승격하지 않는다.**
