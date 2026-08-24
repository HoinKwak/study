# 온체인 트렌딩 조기경보 — 2026-08-24 06:40 UTC (KST 2026-08-24 15:40)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> ⚠️**이번 회차는 직전(2026-08-24 03:00Z)로부터 약 3시간 40분 경과**(정상 2시간 대비 지연 — 05:00Z 회차를 건너뛰고 이어받았다, 중복 재생은 하지 않음). 관측 간격이 평소보다 길어 지표 변화폭이 2시간 기준 대비 다소 과대해 보일 수 있다는 점을 감안해 해석했다.

> 44개 활성종목 전부를 DexScreener 토큰 API(5개 이하 소규모 배치조회, 9개 배치)로 재확인하고, GeckoTerminal 솔라나·로빈후드체인 트렌딩 API로 TRUTH·CASHCAT·CLOCKIN·Dinger(구형) 등 교차검증 및 신규 발굴 스캔을 진행했다.

> **배치조회 검증 결과**: 9개 배치 중 1개 배치(TOAD·DPG·FWA·CALLOOOR·JUGGERNAUT)에서 **TOAD가 FWA와 완전히 동일한 데이터(같은 페어 주소·같은 수치)로 반환되는 환각**이 발생해 개별 재조회로 정정했다(정정 전: TOAD 유동성$1,226,412.33 → 정정 후: $378,360.83). TRUTH는 h6가 -92.59%→-9.4%로 극단적으로 개선된 것이 이상해 DexScreener 개별 페어 조회 + GeckoTerminal 풀 직접 조회 + GT 트렌딩 재확인까지 3중으로 대조했고, 세 소스 모두 유사한 값(h6 -9.4%~-13.46%)으로 수렴해 실제 신호로 확인했다. 나머지 42개 토큰은 배치·개별조회 결과가 요청 개수·심볼과 정확히 일치했다.

> **편입/편출/강등 내역**: **신규편입 0건**. **편출 0건**. 활성목록 **44→44종**(순증감 0). notable **38→39개**(GT 로빈후드체인 트렌딩에서 신규 발견된 세 번째 'Dinger' 티커 풀 1건 추가).

## 🚨 최우선 후속 — TRUTH h6 대폭 개선, 그러나 유동성은 재유출 (여전히 극단 손실권)

직전 회차(03:00Z) 3연속 유동성 회복($76,580.78)을 보였던 TRUTH가, 이번 회차 **유동성이 $65,332.8로 재유출(-14.7%)** 전환됐다. 다만 **h6가 -92.59%에서 -9.4%로 대폭 개선**돼 극단 손실권에서 벗어나는 조짐을 보였다. h1은 -1.9%→-28.02%로 재음전했는데, 이번엔 GeckoTerminal(-31.90%, -29.914%)과도 방향이 일치해 **지난 2회차 연속 있었던 h1 부호 불일치가 이번엔 해소**됐다. h24는 -96.48%→-97.74%로 여전히 거의 완전 붕괴 수준이다.

| 시점 | 유동성 | h1 | h6 | h24 |
|---|---|---|---|---|
| 23:00Z(대붕괴) | $34,673.24 | -75.29% | -93.25% | -98.86% |
| 01:00Z(1차회복) | $57,154.22 | -0.67% | -92.47% | -97.24% |
| 03:00Z(2차회복) | $76,580.78 | -1.9% | -92.59% | -96.48% |
| **06:40Z(이번, 재유출·h6대폭개선)** | **$65,332.8** | **-28.02%** | **-9.4%** | **-97.74%** |

GeckoTerminal 개별 풀 재조회(reserve $64,868.75, h1 -29.914%·h6 -10.931%·h24 -97.753%)와 GT 트렌딩 재확인(로빈후드체인 15위, reserve $64,116.64, h1 -31.90%·h6 -13.46%·h24 -97.82%) 둘 다 DexScreener와 방향·크기가 밀접하게 일치한다. 21:20Z 고점($223,452) 대비로는 -70.8%다. **h6 개선이 실제 바닥 형성인지 일시적 반등인지는 다음 회차에 확인이 필요**하며, 유동성 자체는 이번 회차 다시 줄었으므로 신규진입 절대금지 최상위 경계를 유지한다.

## 그 밖 특기 사항

- **LIZARD(17회차)**: 16회차째 지속되던 깊은 음전권을 이번 회차 처음으로 완전히 탈출했다 — 유동성 +21.5% 대폭 유입, h1·h6·h24 전부 재양전(h24 -33.5%→+36.64%). 다만 1회차뿐이라 확정은 이르다. 리스크를 🔴→🟡로 하향한다.
- **FLUSH(24회차)**: 직전 회차 "3연속 유입 + h24 최초 양전"으로 🟢 하향했는데, 이번 회차 유출 전환 + h24 재음전(-19.87%)으로 다시 번복됐다. 직전 하향은 성급했던 것으로 판단해 🟡로 재상향한다.
- **KIRK(26회차)**: 수개 회차째 "대체로 안정적"이었던 흐름에 이번 회차 처음 균열이 갔다 — 전지표 재악화, h24 재음전(-21.29%). 🟢→🟡로 상향한다.
- **Z500(29회차)**: 28회차째 이어지던 전방위 악화 흐름이 이번 회차 처음 멈추고 전지표 개선(h24 -35.68%→-8.03%)됐다. 1회차뿐이라 🔴는 유지하되 첫 개선 조짐으로 기록한다.
- **CALLOOOR(126회차)**: 125회차째 이어지던 "소폭개선" 흐름이 이번 회차 h6·h24 동반 강한 재양전(+19.95%/+19.7%)으로 가속됐다. 장기추적 종목 중 드문 뚜렷한 개선이라 🟡→🟢로 하향한다.
- **BULLSHIT(57회차)**: 56회차째 이어지던 유출 흐름에 처음으로 대폭 유입반전(+32.8%)이 나타났고 h1·h24 동반 재양전됐다. 1회차뿐이라 단정은 이르지만 강한 양의 신호로 기록한다.
- **CYBERCAT(7회차)**: 2회차 연속 유출이 소폭 유입반전(+1.5%)으로 전환됐으나 h1은 여전히 재음전이라 "정점통과" 패턴 자체는 불변으로 판단, 🔴 유지한다.
- **TOAD 배치조회 환각**: TOAD·DPG·FWA·CALLOOOR·JUGGERNAUT 배치조회에서 TOAD가 FWA와 완전히 동일한 데이터(같은 페어 주소)로 반환됐다. 개별 재조회로 정정(유동성 $1,226,412.33→$378,360.83)했다.
- **Dinger 티커 3중 충돌**: 이번 회차 GeckoTerminal 로빈후드체인 트렌딩에서 **세 번째 'Dinger' 풀이 신규 발견**됐다(pool 0x734ce5818ed9b032f2bb8fa67cb0f1bbb3f393b8, h24 +356,693.57%라는 극단값 — 신규 풀 특유의 거의 0에서 시작한 산술 결과로 추정). 기존 추적 중인 Dinger(Solana, CA 3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump)와 이미 기록 중이던 구형 Dinger(Solana, pool FvsZohWNdVpSDQk4gCyU9YrkLRsfeEpSmzVUSQsjDaxG)에 이어 세 번째 별개 토큰이다. tokens 편입은 보류하고 notable에 첫 기록만 남긴다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 28회차. 27회차재번복이후강한개선반전 | 유동성$106,185.87(+16.9%), h24+21.09%(가속) | 지속(28회차)·개선반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 36회차. h24큰폭재음전 | 유동성$21,805.72(+1.3%), h24-10.42% | 지속(36회차)·h24재음전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 22회차. h1재양전,h6여전히소폭음전 | 유동성$27,659.60(-3.0%), h24+37.13% | 지속(22회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 46회차. 유입반전1회만에번복 | 유동성$204,410.04(-9.8%), h24+18.25% | 지속(46회차)·whipsaw | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 34회차. 개선흐름정체,유출전환 | 유동성$14,780.37(-8.3%), h24+1.53% | 지속(34회차)·정체 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 17회차. ⭐16회차만의첫전방위재양전 | 유동성$40,530.43(+21.5%), h24+36.64%(재양전) | 지속(17회차)·재양전 | 🟡(하향) | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 26회차. h6재음전,h24감속 | 유동성$30,009.91(-2.3%), h24+20.23% | 지속(26회차)·h6재음전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 58회차. 유입반전1회만에다시유출번복 | 유동성$33,493.91(-13.0%), h24-34.77%(재음전) | 지속(58회차)·재번복 | 🔴 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 24회차. ⚠️3연속유입+h24최초양전1회만에번복 | 유동성$32,424.25(-3.6%), h24-19.87%(재음전) | 지속(24회차)·재번복 | 🟡(재상향) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 63회차. 유동성정체,h24소폭악화 | 유동성$7,280.45(-0.6%) | 지속(63회차)·정체 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 21회차. 21회연속개선궤적첫제동 | 유동성$12,854.81(-0.7%), h24-31.04% | 지속(21회차)·첫제동 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 10회차. 9회차째whipsaw | 유동성$62,783.75(+0.2%), h24+57.7% | 지속(10회차)·whipsaw9회차 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 7회차. 2회유출이소폭유입반전전환 | 유동성$59,946.44(+1.5%), h24+829% | 지속(7회차)·소폭유입반전 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 10회차. 3회차째전지표개선지속 | 유동성$109,127.69(유사), h24-23.73% | 지속(10회차)·3연속개선 | 🟡 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 39회차. 유입지속,h1재음전h24재양전 | 유동성$217,168.12(+2.6%), h24+11.55% | 지속(39회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium) | 미확인 | 38회차. 유입지속,가격모멘텀은감속 | 유동성$1,744,124.59(+5.8%), h24+57.47% | 지속(38회차)·모멘텀괴리 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 36회차째방향번복. 재양전흐름연장 | 유동성$312,535.79(+6.0%), h24+78.01% | 지속(36회차)·재양전연장 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 29회차. ⭐28회차악화이후첫개선조짐 | 유동성$72,534.45(+2.9%), h24-8.03%(대폭개선) | 지속(29회차)·첫개선조짐 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 26회차. ⚠️안정흐름첫균열,전지표재악화 | 유동성$74,685.97(-3.9%), h24-21.29%(재음전) | 지속(26회차)·첫균열 | 🟡(상향) | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 23회차. 개선반전1회만에다시악화번복 | 유동성$68,466.90(-8.2%), h24-54.42%(악화) | 지속(23회차)·연속whipsaw | 🔴 | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 14회차. h1재음전,h6h24는유지 | 유동성$315,222.68(+1.2%), h24+43.02% | 지속(14회차)·h1재음전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 7회차. h1재음전,유사수준유지 | 유동성$348,642.85(-2.8%), h24+9776% | 지속(7회차)·유사수준 | 🟡 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 6회차. 6회연속유입,h6h24가속 | 유동성$167,180.11(+8.0%), h24+57.04% | 지속(6회차)·6연속유입 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 12회차. h6대폭개선,유동성재유출 | 유동성$65,332.8(-14.7%), h24-97.74% | 지속(12회차)·h6대폭개선 | 🔴(최상위경계) | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 41회차. 4회차째개선흐름지속 | 유동성$379,402.54(+17.9%), h24+180% | 지속(41회차)·4연속유입 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 163회차. 첫균열2회차째지속 | 유동성$253,207.57(-2.2%), h24+24.51% | 지속(163회차)·균열지속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 139회차. 2연속유입후첫유출전환 | 유동성$183,699.89(-7.0%), h24+23.82% | 지속(139회차)·첫유출 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 42회차. 첫냉각조짐일부완화 | 유동성$485,752.94(+1.5%), h24+12.76% | 지속(42회차)·냉각완화 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 130회차. 대체로안정적 | 유동성$31,347.55(-1.4%), h24-2.95% | 지속(130회차)·안정적 | 🟢 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 177회차. 유사수준,h6재음전혼조 | 유동성$362,797.04(-1.2%), h24+4.85% | 지속(177회차)·혼조 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 168회차. h1재양전으로또다시반전 | 유동성$107,244.88(-2.0%), h24-22.64% | 지속(168회차)·연속whipsaw | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 168회차. 유출지속,h6재음전 | 유동성$57,692.01(-1.4%), h24+3.84% | 지속(168회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 126회차. ⭐h6h24동반강한재양전 | 유동성$66,786.67(+9.5%), h24+19.7%(재양전) | 지속(126회차)·재양전가속 | 🟢(하향) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 176회차. h1재양전,h6소폭악화 | 유동성$378,360.83(-1.3%), h24-10.85% | 지속(176회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 180회차. 유사수준,h6재음전 | 유동성$1,226,412.33(-1.0%), h24+22.45% | 지속(180회차)·h6재음전 | 🟡 | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 128회차. 유입지속,h24개선지속 | 유동성$66,578.95(+4.9%), h24-50.15% | 지속(128회차)·개선지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap) | 미확인 | 57회차. ⭐56회만의첫대폭유입반전 | 유동성$295,798.45(+32.8%), h24+2.36%(재양전) | 지속(57회차)·대폭유입반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 21회차. h24대폭반전(베이스효과추정) | 유동성$48,163.50(-2.9%), h24-32.95%(반전) | 지속(21회차)·h24반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 100회차달성. 유입반전,h24개선 | 유동성$1,599,664.85(+3.0%), h24-29.14% | 지속(100회차)·유입반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **Dinger** | Solana(PumpSwap) | 미확인 | 11회차. ⚠️전지표대폭악화지속 | 유동성$27,483.49(-23.3%), h24-98.35%(대폭악화) | 지속(11회차)·악화가속 | 🔴 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 14회차. whipsaw지속,h24개선 | 유동성$218,960.36(유사), h24-28.38% | 지속(14회차)·whipsaw지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 28회차(dogwifpants). h1whipsaw,h6h24개선 | 유동성$98,410.50(-0.7%), h24-31.66%(개선) | 지속(28회차)·h1whipsaw | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 15회차. 안정화흐름재흔들림 | 유동성$10,091.75(-7.6%), h24-31.11% | 지속(15회차)·재흔들림 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 13회차. h24반전이후점진개선 | 유동성$28,129.46(-6.6%), h24-68.49%(개선지속) | 지속(13회차)·점진개선 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. **최우선후속**: TRUTH h6 -92.59%→-9.4% 대폭 개선이나 유동성은 재유출(-14.7%), 여전히 극단 손실권. **다운그레이드(리스크완화)**: LIZARD(16회만의 전방위 재양전, 🔴→🟡), CALLOOOR(h6h24 강한 재양전, 🟡→🟢). **업그레이드(리스크상향)**: KIRK(안정흐름 첫균열, 🟢→🟡), FLUSH(h24최초양전이 1회만에 번복, 🟢→🟡 재상향). **첫 개선 조짐(유지)**: Z500(28회 악화 후 첫 개선), BULLSHIT(56회 유출 후 첫 대폭 유입반전). **whipsaw 다수**: OBS·CLOCKIN·CLUG·CONK·Dealer·CHUMP·PROLOGUE 등 다수 종목이 이번 회차도 반복 번복.

## 온체인 신호 상세

- **TRUTH h6 대폭 개선 상세**: 상단 최우선 후속 섹션 참조. 유동성 재유출(-14.7%)에도 h6가 -92.59%→-9.4%로 극단 손실권을 벗어나는 조짐. DS·GT·개별풀 3중 대조로 신뢰도 확인, h1 부호 불일치 해소 · 2026-08-24T06:40:00Z
- **LIZARD 전방위 재양전 상세**: 16회차째 이어지던 깊은 음전권을 이번 회차 처음 완전 탈출. 유동성 +21.5%, h1/h6/h24 전부 재양전. 1회차뿐 · 2026-08-24T06:40:00Z
- **CALLOOOR·BULLSHIT 개선 상세**: CALLOOOR는 125회차 장기 소폭개선 끝에 h6/h24 강한 재양전으로 가속. BULLSHIT은 56회차만의 첫 대폭 유입반전(+32.8%)과 h1/h24 재양전 · 2026-08-24T06:40:00Z
- **KIRK·FLUSH 반전 상세**: KIRK는 수개 회차 안정흐름 첫 균열(전지표 재악화). FLUSH는 직전 회차 "3연속개선+h24최초양전"이 1회만에 재번복 — 지난 회차 🟢 하향이 성급했음을 인정하고 🟡로 재상향 · 2026-08-24T06:40:00Z
- **TOAD 배치조회 환각 상세**: TOAD·DPG·FWA·CALLOOOR·JUGGERNAUT 배치조회에서 TOAD가 FWA와 완전 동일 데이터로 반환. 개별 재조회로 정정(유동성 $1,226,412.33→$378,360.83) · 2026-08-24T06:40:00Z
- **Dinger 티커 3중 충돌 신규 발견 상세**: 로빈후드체인 GT트렌딩13위에 세 번째 'Dinger' 풀 신규 발견(pool 0x734ce5818ed9b032f2bb8fa67cb0f1bbb3f393b8, h24 +356,693.57%는 신규 풀 산술 아티팩트로 추정). notable에만 첫 기록 · 2026-08-24T06:40:00Z
- **GT신규발굴 재확인(LOOKSMAX·Morty·Polycat·DOPAMEME·LUIGI)**: LOOKSMAX는 예상 밖 전방위 재가속(h1+65.92%·h6+93.08%·h24+903.60%, 유동성+29.6%). Morty는 h1 재양전(whipsaw). Polycat·DOPAMEME은 h1 개선이나 h6/h24 큰 폭 감속. LUIGI는 h1 재음전·h24 추가 악화. 전부 notable 유지, tokens 편입은 계속 보류 · 2026-08-24T06:40:00Z
- **DexScreener 배치조회 완전성**: 요청한 44개 토큰 전부 최종 확보. TOAD 1건이 배치조회에서 환각(FWA 데이터 혼입)돼 개별 재조회로 보완 · 2026-08-24T06:40:00Z
- **나머지 상세**: PEPECOIN h24재음전. MAPLE혼조. CLOCKIN whipsaw. TIPANSEM정체. 1B h6재음전. CLUG재번복. PEE정체. 40M첫제동. MANEKI whipsaw9회차. CYBERCAT소폭유입반전. omo3연속개선. swappy혼조. CYBERLEEK모멘텀괴리. CC재양전연장. GOOD냉각완화. PRINTER혼조. Dealer연속whipsaw. lickingcat혼조. PITCOIN안정적. JUGGERNAUT균열지속. BRODIE첫유출. Doge2h24반전. CATE유입반전. Dinger악화가속. BARRON whipsaw지속. PANTS h1whipsaw. Truth Coin재흔들림. YOMOGI점진개선. HOOKR4연속유입. CATALORIAN유사수준. PROLOGUE6연속유입. CHUMP h1재음전. CONK연속whipsaw. DPG개선지속. FWA h6재음전 · 2026-08-24T06:40:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 42종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 재확인, TRUTH 최우선 후속 처리, GT 트렌딩 교차검증에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-24 03:00Z)로부터 약 3시간 40분 경과(정상 2시간 대비 지연 — 05:00Z 회차를 건너뛰고 이어받음, 중복 재생 없음). 관측 간격이 길어진 만큼 이번 회차의 지표 변화폭은 2시간 기준 대비 다소 부풀려졌을 가능성을 감안해 해석했다.
- **🚨 최대 사건 후속: TRUTH h6 대폭 개선·유동성 재유출**: h6가 -92.59%→-9.4%로 극단손실권을 벗어나는 조짐을 보였으나 유동성은 3연속 회복 이후 이번 회차 -14.7% 재유출됐다. h1 부호 불일치가 DS·GT·개별풀 3중 대조로 해소됐다(모두 강한 음수로 일치). 신규진입 절대금지 최상위 유지, h6 개선이 바닥 형성인지 일시적 반등인지 다음 회차 확인 필요.
- **⚠️ 배치조회 환각 1건 발생·정정**: TOAD가 같은 배치에 있던 FWA와 완전히 동일한 데이터(같은 페어 주소·수치)로 반환됐다. 개별 재조회로 정정했다. 5개 이하 배치조회에서도 이런 종류의 환각이 재발할 수 있음을 재확인했다.
- **개선·악화 반전 다수**: LIZARD(16회만의 전방위 재양전, 🔴→🟡)·CALLOOOR(h6h24 재양전 가속, 🟡→🟢)는 리스크 하향. KIRK(안정흐름 첫균열, 🟢→🟡)·FLUSH(h24최초양전 1회만에 번복, 🟢→🟡 재상향)는 리스크 상향. Z500·BULLSHIT은 장기 악화/유출 흐름 후 첫 개선 조짐이 나타났으나 1회차뿐이라 🔴 유지.
- **whipsaw(반복 번복) 패턴 지속**: OBS·CLOCKIN·CLUG·CONK·Dealer·CHUMP·PROLOGUE 등 다수 종목이 이번 회차도 직전 방향을 다시 뒤집었다. 단일 회차 방향을 추세로 단정하지 않는 신중함이 계속 필요하다.
- **Dinger 티커 3중 충돌**: 기존 추적 중인 Dinger(Solana) + 구형 Dinger(Solana, notable) 에 이어 이번 회차 GT 로빈후드체인 트렌딩에서 세 번째 'Dinger' 풀이 신규 발견됐다(h24 +356,693.57%는 신규 풀 특유의 산술 아티팩트로 추정). notable에 경계 사례로만 기록했다.
- **GT신규발굴 재확인**: LOOKSMAX가 예상 밖 전방위 재가속(h24 +412.87%→+903.60%)을 보여 다음 회차 편입 여부 재검토 대상으로 표시했다. Morty·Polycat·DOPAMEME·LUIGI는 대체로 감속·혼조 지속.
- **데이터 신뢰도**: 이번 회차는 DexScreener 토큰 API로 44개 활성종목을 9개 배치(5개 이하)로 확보했고, TOAD 1건의 배치조회 환각을 개별 재조회로 정정했다(정정 외 데이터는 요청 개수·심볼과 정확히 일치). GeckoTerminal은 솔라나·로빈후드체인 트렌딩 API가 정상 응답해 TRUTH·CASHCAT·Dinger(구형)·PANTS·YOMOGI·HOOKR·STONKBROKER·PONS·ANSEM·PEPE(로빈후드)·AI/NVDA·LOOKSMAX·Morty·Polycat·DOPAMEME·LUIGI 교차검증 및 신규 'Dinger'(로빈후드체인) 발굴에 활용했다. TRUTH는 DS·GT·개별풀 3중 조회 모두 h1·h6·h24 방향이 일치해 신뢰도가 높다. CLOCKIN은 GT값(유동성$45,347.61)이 DS값($204,410.04)과 큰 격차가 있어 참고 수준으로만 취급했다(DS를 1차 근거로 유지, 과거에도 반복된 패턴). X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
