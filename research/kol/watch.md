# 온체인 트렌딩 조기경보 — 2026-08-24 13:00 UTC (KST 2026-08-24 22:00)

> ⚠️ 아이디어 소싱·**개인 정보 모니터링/조기경보용**. **투자조언·매수추천 아님(Not financial advice).** 온체인 트렌딩은 봇·워시트레이딩·러그 편향이 매우 크다. 자체 검증 필수. (1차 신호=온체인 트렌딩, KOL 언급은 있으면 코로보로만 반영.)

> **⏱️ 이번 회차 간격**: 직전(2026-08-24 11:00Z)로부터 정확히 **2시간** 경과했다(정시 슬롯 정상 진행).

> 44개 활성종목 전부를 DexScreener 토큰 API로 재확인했다. 이번 회차는 **DexScreener 서버 오류(500/522/525/타임아웃)가 극심**해 배치조회는 물론 개별 조회도 다수 실패했고, 성공한 응답 중에서도 **동일 토큰을 재조회했을 때 서로 다른(때로는 상충하는) 값이 반환되는 사례가 다수 발생**했다(BRODIE·CHUMP·CATALORIAN·FWA·CYBERCAT). 규칙대로 전부 재검증·교차확인했다.

> **데이터 신뢰도 경고(이번 회차 최대 이슈)**:
> 1. **1B·FLUSH**: 최초 배치조회(2개씩 묶음)에서 h24 +612%·+1051%라는 비현실적 수치가 반환됐다. 개별 재조회로 각각 +86.37%·-43.5%로 정정했다 — 배치조회 환각이 이번에도 재발.
> 2. **BRODIE·CHUMP**: 첫 배치조회와 이후 개별 재조회에서 서로 다른 수치가 나왔다(BRODIE h24 10.11%→65.85%, CHUMP h24 109%→22.5%). 각각 재조회 2회로 다수결 확인해 채택.
> 3. **FWA**: 1차 조회에서 직전 회차(11:00Z)와 **소수점까지 완전히 동일한 값**(유동성 $1,252,945.76, h6 2.82%, h24 25.46%)이 반환돼 캐시/이상치로 의심, 재조회로 실제 변동값(유동성 $1,246,597.97, h6 2.05%, h24 21.59%)을 확보했다.
> 4. **CATALORIAN**: DS가 h24 **+2,126%**를 반환했는데, 같은 페어주소를 GT로 직접 조회하니 h24 **-37.642%**로 부호 자체가 상충했다. GT를 트렌딩 리스트+풀 직접조회 2회로 교차확인해 일치시켰고, 이번 회차는 GT값을 채택했다(DS를 이상치로 판단). 다음 회차 재확인 필수.
> 5. **CYBERCAT**: DS가 유동성 필드가 아예 없고 dexId가 "pumpfun"(본딩커브)인 이상한 페어(h24 1194%)를 반환했다. GT 풀 직접조회로 대체해 PumpSwap 풀이 여전히 정상 존재함(유동성 $42,820.52)을 확인했다.

> **편입/편출/강등 내역**: **신규편입 0건**. **편출 0건**. 활성목록 **44→44종**(순증감 0). notable **41→41개**(신규 없음, 기존 항목 데이터 갱신).

## 🚨 주요 사건 — TRUTH, v자함정 확정 이후에도 추가 붕괴 지속

직전 회차(11:00Z)에서 v자함정이 확정됐던 TRUTH가 이번 회차 유동성 유출은 멈췄지만(+0.1%), **h6·h24는 오히려 더 악화**됐다. h1은 -63.54%→-55.33%로 소폭 개선됐으나 여전히 극단적 음전이고, h6는 -62.07%→-70.08%, h24는 -69.88%→-79.73%로 계속 무너지고 있다. 21:20Z 고점($223,452) 대비 현재 $48,240은 약 78% 낮은 수준으로 거의 변함없다. 신규진입 절대금지 최상위 경계를 유지한다.

## 🚨 주요 사건 — CATALORIAN, DS·GT 데이터 소스 자체가 상충

CATALORIAN은 이전 여러 회차 동안 "DS·GT 수치 편차가 있으나 방향은 동일"했는데, 이번 회차는 **부호 자체가 정반대**로 갈렸다(DS h24 +2,126% vs GT h24 -37.642%, 동일 페어주소 FvYok1cEnymtxGPXbLhyMVUBq2iEVGQ18Uj4K7vKoJ5Q 기준). GT를 트렌딩 리스트 조회와 풀 단독 직접조회 2가지 경로로 재확인해 서로 일치(-25.92%/-37.642%, 둘 다 음수)함을 확인했고, 이번 회차는 GT값을 채택해 h24 방향 반전(대폭악화)으로 기록한다. 유동성도 3회차 연속 대폭유출(-22.3%)이다. 데이터 신뢰도 자체가 흔들린 사례라 다음 회차 최우선 재확인 대상이다.

## 그 밖 특기 사항 — 이번 회차는 "1회성 신호 반전"이 유독 많았다

- **FLUSH 4연속 악화로 리스크 상향(🟡→🔴)**: 4회차 연속으로 유동성 유출과 전지표 악화가 이어져, 이 데이터셋의 규칙(2회 이상 연속 확인 시 색상 조정)에 따라 상향했다.
- **직전 회차 다운그레이드 4건이 모두 1회만에 재반전**: HOOKR(유입재전환→다시유출), lickingcat(2연속개선→유출전환+감속), CALLOOOR(127회차양전기조→h6h24재음전), FWA(전지표개선→h1재음전+첫유출조짐). 넷 다 🟢에서 🟡로 재상향했다. "단발 개선을 추세로 확정하지 말라"는 이 워치의 핵심 원칙이 한 회차에 4건이나 재검증된 셈이다.
- **JUGGERNAUT는 3연속 개선으로 더 견고해짐**: h6+21.23%·h24+62.09%로 직전 수준을 유지, 3회 연속 확인된 만큼 🟢 유지가 합리적이다. PRINTER·BRODIE·PITCOIN·PROLOGUE(9연속유입)도 안정적으로 🟢 유지.
- **1B, 또 한번의 급반전**: 지난 회차 "급반전악화"가 이번엔 유동성 +26.2%·전지표 대폭 재양전으로 다시 뒤집혔다. 연속 whipsaw로 신뢰도가 낮아 🟡 유지, 단정하지 않는다.
- **Doge2 대폭 개선(단1회차)**: 유동성 +29.8%, h1/h6 대폭 가속·재양전, h24도 -48.53%→-5.24%로 손익분기 근접까지 개선됐다. 강한 단일 회차 신호라 다음 회차 확인 전까지는 🟡 유지.
- **CATCUS 2회차 연속 확인, CA 확보**: GT 솔라나 트렌딩 3위 유지(전 회차 4위에서 상승), 유동성 +5.1%로 지속 유입, 전지표 2회차 연속 양전. 이번 회차 CA(66ZEoQSgY3g5KEijP8ZUucth9ZmrxwYg8ngzwgP6pump)를 GT를 통해 확인했다. 다만 풀 나이가 여전히 1일 미만이라 tokens 편입은 다음 회차 재검토 대상으로 표시만 해둔다.

## 🔥 온체인 트렌딩 조기경보 (조기성 우선 정렬)

### 조기 (13종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **OBS** | Robinhood Chain(Uniswap) | 미확인 | 31회차. 2연속개선흐름 | 유동성$106,341.93(+2.6%), h24+42.76%(가속) | 지속(30회차)·2연속개선 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xfd7c2011444e8105249df4b1f2986d13304dfa2ade3ebed0b6e168f259f6c956) |
| **PEPECOIN** | Robinhood Chain(V3) | 미확인 | 39회차. 3연속악화 | 유동성$20,371.63(-8.8%), h24-30.56% | 지속(38회차)·3연속악화 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x29d2049bb2f92b17a5e75cb6ee6d6c1ba8a82dcd) |
| **MAPLE** | Solana(PumpSwap) | 미확인 | 25회차. 유입반전,전지표개선 | 유동성$29,047.66(+9.6%), h24+20.74% | 지속(24회차)·단1회차 | 🟡 | [DexScreener](https://dexscreener.com/solana/DLhzqAWwE2YkPLdYvvWNMZ71vxZJQD2FByMfWFHppump) |
| **CLOCKIN** | Robinhood Chain | 없음(자체서사) | 49회차. h1재양전,h24감속 | 유동성$201,232.81(-0.6%), h24+13.36% | 지속(48회차)·whipsaw지속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0xcd2937592f73968ebaa916f37e5f6c1b27713469) |
| **TIPANSEM** | Solana(PumpSwap) | 미확인 | 37회차. whipsaw지속,h24재음전 | 유동성$15,188.69(+1.2%), h24-12.17% | 지속(36회차)·whipsaw지속 | 🟡 | [DexScreener](https://dexscreener.com/solana/B5YTUMqSnwzztWHWmzAzHApeRy6cuGEx49Bidt4kuH8w) |
| **LIZARD** | Solana(PumpSwap) | 미확인 | 20회차. 재양전이재번복 | 유동성$38,961.69(+0.02%), h24+1.96%(대폭감속) | 지속(19회차)·연속whipsaw | 🟡 | [DexScreener](https://dexscreener.com/solana/2hXHY3DnN7HUGySZEmBsLFKSqLB8nj3aE8wwq44wpump) |
| **1B** | Robinhood Chain(Uniswap) | 미확인 | 29회차. 급반전악화가재양전으로재반전 | 유동성$34,039.59(+26.2%), h24+86.37%(대폭가속) | 지속(28회차)·연속급반전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x1c58f34088e33ff14bac3715986d40f296aec7da19f5ed14ad882bcc2a71d63d) |
| **CLUG** | Solana(PumpSwap) | 미확인 | 61회차. 2연속개선이혼조로전환 | 유동성$35,875.11(-0.2%), h24-21.55%(악화) | 지속(60회차)·혼조전환 | 🟡 | [DexScreener](https://dexscreener.com/solana/7g2xyrq9Fk1TvFiqqcmLJAQ9jAtfHobmrdzzM9Dp2SpV) |
| **FLUSH** | Robinhood Chain(Uniswap) | 미확인 | 27회차. ⭐4연속전지표악화 | 유동성$27,492.15(-4.7%), h24-43.5%(추가악화) | 지속(26회차)·4연속악화 | 🔴(상향) | [DexScreener](https://dexscreener.com/robinhood/0xc3bf319b19376d6b348325b1e78f7de1f68b3fb10750f0d832a4bc1643a56eb8) |
| **PEE** | Solana(PumpSwap) | 미확인 | 66회차. 유동성정체 | 유동성$7,413.61(변동없음), h24-5.89% | 지속(65회차)·정체 | 🔴 | [DexScreener](https://dexscreener.com/solana/2mG7vDMrZYFyFS2bz3AsrJizFoiAYurY5kc4MPqfpump) |
| **40M** | Solana(PumpSwap) | 미확인 | 24회차. 여전히깊은음전권 | 유동성$12,667.17(+1.0%), h24-36.45% | 지속(23회차)·깊은음전권 | 🔴 | [DexScreener](https://dexscreener.com/solana/ELbFy4v8vzJHjvmqCDw7CEzsYuN9TGkBt7Kz9Kawpump) |
| **MANEKI** | Robinhood Chain(SushiSwap V3) | 미확인 | 13회차. 12회차째whipsaw | 유동성$61,178.2(+1.0%), h24+49.97% | 지속(11회차)·whipsaw12회차 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0xbe28fdf829dad4478eefefd5d9725905c0b59caf) |
| **CYBERCAT** | Solana(PumpSwap) | 미확인 | 10회차. DS이상치→GT대체,정점통과지속 | 유동성$42,820.52(GT,-15.6%), h24+367.692%(대폭감속) | 지속(9회차)·정점통과지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/9HHTQ7YMx82E987cNqF9KczyZrfKgqvKNyA2yHSVpump) |

### 확산 (10종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **omo** | Solana(PumpSwap) | 미확인 | 13회차. 급락이후소폭안정화 | 유동성$111,138.70(-2.9%), h24-45.93%(소폭개선) | 지속(12회차)·소폭안정화 | 🔴 | [DexScreener](https://dexscreener.com/solana/94Sm8joZMSRzpQmcNVn5zZpgnRLN2DBesJYDXwuNpump) |
| **swappy** | Robinhood Chain(V4) | 미확인 | 42회차. 혼조 | 유동성$203,201.82(-0.01%), h24-0.4%(개선) | 지속(41회차)·혼조 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x298348d5b2e45C774E3ee4f1a0924071DfbDC8C7) |
| **CYBERLEEK** | Solana(Raydium CPMM) | 미확인 | 41회차. DS실패→GT대체,혼조반전 | 유동성$1,999,981.95(GT,+4.4%), h24-17.648%(재음전) | 지속(40회차)·혼조반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/ApZuxdpzMrbEYTGEzeY9afh5pj9d6qPRJCTgQYiipbKg) |
| **CC** | Solana(PumpSwap) | 미확인 | 39회차째방향번복. h1재음전 | 유동성$318,586.2(+0.2%), h24+96.37%(감속) | 지속(38회차)·워시트레이딩의심불변 | 🔴 | [DexScreener](https://dexscreener.com/solana/E3i7sTY5QYEBh3itepnomZQt7Eh5kzmHFk1vkm2pump) |
| **Z500** | Solana(PumpSwap) | 미확인 | 32회차. 재음전흐름지속 | 유동성$74,314.67(-2.9%), h24-13.06% | 지속(31회차)·장기악화흐름지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/7fDdLy2rmQKsPCkqUXEd1mN7yDfEzArc4VrctWmfkJBK) |
| **KIRK** | Solana(PumpSwap) | 미확인 | 29회차. 전지표동반개선 | 유동성$77,037.8(+4.7%), h24-16.17%(개선) | 지속(28회차)·단1회차 | 🟡 | [DexScreener](https://dexscreener.com/solana/8du34ohgGj2ikZVTGZNwHbNbqX8b8AHGFANf6qmopump) |
| **CONK** | Solana(Raydium) | 미확인 | 26회차. 연속whipsaw+전지표악화 | 유동성$62,060.68(-6.7%), h24-52.92%(악화) | 지속(25회차)·연속whipsaw+악화 | 🔴 | [DexScreener](https://dexscreener.com/solana/koZZXrKJctd7AtVHdx62iYLPv5PqvQ3RrFyUr3GMBfm) |
| **CHUMP** | Robinhood Chain(V3 1%) | 미확인 | 17회차. 2연속h24감속+첫유출조짐 | 유동성$339,590.55(-2.7%), h24+22.5%(2연속감속) | 지속(16회차)·2연속감속 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x714442e9A611f8561A7dF108D6d925132937cFb8) |
| **CATALORIAN** | Solana(PumpSwap) | 미확인 | 10회차. ⚠️⚠️DS·GT h24부호상충,GT채택 | 유동성$122,206.57(GT,-22.3%), h24-37.642%(GT,방향반전) | 지속(8회차)·DS·GT상충 | 🔴 | [DexScreener](https://dexscreener.com/solana/4cvZwC17oMiUA7peKX5GhbaUWv4U5Lwrd8118xnFpump) |
| **PROLOGUE** | Robinhood Chain(Uniswap) | 미확인 | 9회차. 9연속유입 | 유동성$193,268.03(+2.2%), h24+108%(가속) | 지속(7회차)·9연속유입 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x8651e656738064177752a395dbde2b2a9e3fc469edc2a9212e6060c0990bb7eb) |

### 뒷북 (21종)

| 토큰 | 체인/DEX | KOL 코로보(있으면) | 서사(요지) | 온체인(거래량/유동성/홀더) | 신규? | 리스크 | 출처 |
|---|---|---|---|---|---|---|---|
| **TRUTH** | Robinhood Chain(V2) | 미확인 | 15회차. v자함정확정후추가악화지속 | 유동성$48,240.54(+0.1%), h24-79.73%(추가악화) | 지속(13회차)·붕괴지속최상위경계 | 🔴 | [DexScreener](https://dexscreener.com/robinhood/0x2ec5cc87c9a3231bffbbf788ca9182ebd1d64fc4) |
| **HOOKR** | Robinhood Chain(Uniswap) | 미확인 | 44회차. 유입재전환1회만에번복 | 유동성$400,152.13(-3.1%), h24+148% | 지속(42회차)·재차유출반전 | 🟡(상향) | [DexScreener](https://dexscreener.com/robinhood/0x590dcb6a87828bf688b48089a62239b693378f1fb64d2286e6a399ed8c005fdf) |
| **JUGGERNAUT** | Robinhood Chain(V3 1%) | Drallio(약한코로보,carryover) | 166회차. ⭐3연속개선유지 | 유동성$291,066.42(+0.3%), h24+62.09%(고수준유지) | 지속(164회차)·3연속개선 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x588b0785f50063260003B7790C42f1eF74902746) |
| **BRODIE** | Robinhood Chain(V3) | 미확인 | 142회차. 고수준안정유지 | 유동성$197,840.54(+0.8%), h24+65.85% | 지속(140회차)·고수준안정유지 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0x9870C395bfA68C9F23D7c232fA5a37BF063aae35) |
| **GOOD** | Robinhood Chain(V3) | 미확인 | 45회차. h24재음전혼조 | 유동성$490,053.05(+0.5%), h24-5.04%(재음전) | 지속(43회차)·h24재음전 | 🟡 | [DexScreener](https://dexscreener.com/robinhood/0x8ea7c66395fd7e25e9713edd0b297d4abe05c304) |
| **PITCOIN** | Solana(PumpSwap) | 미확인 | 133회차. 안정적유지 | 유동성$33,892.39(변동없음), h24+21.1% | 지속(131회차)·안정적개선 | 🟢 | [DexScreener](https://dexscreener.com/solana/G1iBvjhZ9wpGUZdQcvhRSqjow3x6xetsnmEBBMm1pump) |
| **PRINTER** | Robinhood Chain(V4) | 미확인 | 180회차. 안정적개선지속 | 유동성$371,033.31(+0.6%), h24+14.77% | 지속(178회차)·안정적개선지속 | 🟢 | [DexScreener](https://dexscreener.com/robinhood/0xf6c9f0a8bf94ecda6751465a3097bc4c69914421126d2cbc3df723e36b8cf47b) |
| **Dealer** | Solana(PumpSwap) | 미확인 | 171회차. 연속whipsaw+악화 | 유동성$106,087.49(-2.3%), h24-27.98% | 지속(169회차)·연속whipsaw+악화 | 🟡 | [DexScreener](https://dexscreener.com/solana/6f8ZQhxqfigdv7UszZ1rirbV7Sgv83s3rxv1N2Zopump) |
| **lickingcat** | Solana(PumpSwap) | 미확인 | 171회차. 2연속개선후반전 | 유동성$62,848.53(-4.3%), h24+21.09%(감속) | 지속(169회차)·2연속개선후반전 | 🟡(상향) | [DexScreener](https://dexscreener.com/solana/EjD5Y9NVhXmtEqU7wYvAyZvDWZFQeEuHXFatJmTbpump) |
| **CALLOOOR** | Solana(PumpSwap) | 미확인 | 129회차. 장기양전기조종료 | 유동성$66,978.10(-2.9%), h24-0.28%(재음전) | 지속(127회차)·양전기조종료 | 🟡(상향) | [DexScreener](https://dexscreener.com/solana/A48KeWUuiDSdRQBqAFssgyYATDuBv7cer54V2JSDpump) |
| **TOAD** | Solana(PumpSwap) | 미확인 | 179회차. 개선흐름악화반전 | 유동성$371,067.96(-0.03%), h24-23.19%(악화) | 지속(177회차)·개선흐름반전 | 🟡 | [DexScreener](https://dexscreener.com/solana/A13oRB9FFaiUjfi6LdCg6p9ka1u8SfGkUFs4SKvPpump) |
| **FWA** | Ethereum(Uniswap V4) | Cointelegraph·CryptoBriefing·KuCoin·PANews(carryover) | 183회차. 1차조회캐시의심→재조회정정,h1재음전 | 유동성$1,246,597.97(-0.5%), h24+21.59%(감속) | 지속(181회차)·h1재음전+첫유출 | 🟡(상향) | [DexScreener](https://dexscreener.com/ethereum/0x230ecd3c25b44af30db59c15f70df7794eb13f67a200f230b7400daa96fe804d) |
| **DPG** | Solana(PumpSwap) | 미확인 | 131회차. 여전히깊은음전권 | 유동성$70,694.62(+1.1%), h24-48%(개선) | 지속(129회차)·깊은음전권 | 🟡 | [DexScreener](https://dexscreener.com/solana/LFEJTxJ9yi6ojGDFpjbGfABLbH55Fc3oEK8syJJpump) |
| **BULLSHIT** | Solana(PumpSwap,풀기준유지) | 미확인(WebSearch보도없음) | 60회차. PumpSwap기준첫안정화 | 유동성$233,076.29(+1.3%), h24+11.47% | 지속(58회차)·PumpSwap기준연속성확인중 | 🟡 | [DexScreener](https://dexscreener.com/solana/zj1jpp7QMveWHLs61vL9KMZf254KvW7j4AAmBF8ry2k) |
| **Doge2** | Solana(PumpSwap) | 미확인 | 24회차. 대폭유입,전지표대폭개선 | 유동성$60,018.96(+29.8%), h24-5.24%(대폭개선) | 지속(22회차)·단1회차 | 🟡 | [DexScreener](https://dexscreener.com/solana/GCbqindK6zYHdhyaiFdtXzqB2r2TqqWaBKnn4YR3KtLP) |
| **CATE** | Solana(PumpSwap) | 미확인 | 103회차달성. 전지표개선방향 | 유동성$1,715,225.13(+3.0%), h24-16.33%(개선) | 지속(101회차)·전지표개선방향 | 🟡 | [DexScreener](https://dexscreener.com/solana/Ai66LHZG9MCzg1WKdawwqduVAXpNDUuV8M3uyq5ppump) |
| **Dinger** | Solana(PumpSwap) | 미확인 | 14회차. 전지표개선,여전히극단붕괴권 | 유동성$23,513.43(+2.9%), h24-77.84%(소폭개선) | 지속(12회차)·전지표개선단1회차 | 🔴 | [DexScreener](https://dexscreener.com/solana/3kvZYBrBPEySFwQfXZGEvJSeMWRa6BkTS34suBEYpump) |
| **BARRON** | Solana(Raydium) | 미확인 | 17회차. whipsaw지속 | 유동성$224,172.97(+0.7%), h24-29.73%(악화) | 지속(15회차)·whipsaw지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/BJFPiZ79ShxyBX59GHZ7p9R9DfQpKsm4xzu46MNMSHcZ) |
| **PANTS** | Solana(PumpSwap) | 미확인 | 31회차(dogwifpants). h24여전히깊은음전권 | 유동성$104,221.96(+1.0%), h24-40.75% | 지속(29회차)·h24깊은음전권 | 🔴 | [DexScreener](https://dexscreener.com/solana/6tMVLioTrzW65RWRAftNWPSf1JikYWRVsP87w9h9em2a) |
| **Truth Coin** | Solana(PumpSwap) | 미확인 | 18회차. h24여전히깊은음전권 | 유동성$10,114.31(+0.8%), h24-56.6%(소폭개선) | 지속(16회차)·깊은음전권 | 🔴 | [DexScreener](https://dexscreener.com/solana/BaBeW6hdxDSenERN6JcxLY9v27YnZqaAQYWuscUjpump) |
| **YOMOGI** | Solana(PumpSwap) | 미확인 | 16회차. 극단변동지속 | 유동성$25,404.15(-3.4%), h24-68.59% | 지속(14회차)·극단변동지속 | 🔴 | [DexScreener](https://dexscreener.com/solana/4978aTN9W3CDuUREGxAQaBYqhPXt8142N4o4Sfgzpump) |

> **편입/편출/강등 요약(이번 회차)**: **신규편입 0건**. **편출 0건**. **최우선후속**: TRUTH가 v자함정 확정 후에도 h6·h24 추가악화 지속(-79.73%). CATALORIAN은 DS·GT 데이터 소스 자체가 h24 부호상충(GT값 채택, 다음회차 재확인 필수). **업그레이드(리스크상향)**: FLUSH(4연속악화,🟡→🔴), HOOKR(유입재전환1회만에번복,🟢→🟡), lickingcat(2연속개선후반전,🟢→🟡), CALLOOOR(양전기조종료,🟢→🟡), FWA(h1재음전+캐시이상치정정,🟢→🟡). **다운그레이드**: 없음(JUGGERNAUT는 3연속개선으로 🟢 유지). **신규발견**: 없음(CATCUS는 2회차연속확인, CA 확보, notable 유지).

## 온체인 신호 상세

- **TRUTH 추가악화 상세**: 상단 주요사건 섹션 참조. 유출은 멈췄으나(+0.1%) h6 -70.08%·h24 -79.73%로 계속 붕괴 중 · 2026-08-24T13:00:00Z
- **CATALORIAN DS·GT 상충 상세**: 상단 주요사건 섹션 참조. GT를 트렌딩 리스트+풀 직접조회 2경로로 교차확인해 h24 -37.642%(음수)로 일치, GT값을 채택. DS h24 +2,126%는 이상치로 판단 · 2026-08-24T13:00:00Z
- **CYBERCAT 데이터 이상 상세**: DS가 유동성 필드 없는 pumpfun(본딩커브) 페어를 반환해 GT 풀(6iZLyDGGUEsBMKU9cLaxmxcguL99F6dhSRVcCUysBBTt) 직접조회로 대체, PumpSwap 풀은 유동성 $42,820.52로 정상 존재 확인 · 2026-08-24T13:00:00Z
- **FWA 캐시의심 정정 상세**: 1차 조회에서 직전 회차와 소수점까지 동일한 값 반환 → 재조회로 실제 변동값(유동성 $1,246,597.97, h1 -1.66%, h6 +2.05%, h24 +21.59%) 확보 · 2026-08-24T13:00:00Z
- **1B·FLUSH 배치조회 환각 상세**: 2개씩 묶은 배치조회에서 h24 +612%·+1051%라는 비현실적 수치 반환 → 개별 재조회로 +86.37%·-43.5%로 정정 · 2026-08-24T13:00:00Z
- **BRODIE·CHUMP 조회값 불일치 상세**: 최초 배치조회와 이후 개별조회에서 서로 다른 수치 반환(BRODIE h24 10.11%↔65.85%, CHUMP h24 109%↔22.5%) → 각각 재조회로 다수결(2/3, 2/2) 확인해 채택값 결정 · 2026-08-24T13:00:00Z
- **4건의 다운그레이드 재반전 상세**: HOOKR·lickingcat·CALLOOOR·FWA 모두 직전 회차 🟢 하향이 이번 회차 1회만에 재상향됨. 세부는 상단 "그 밖 특기 사항" 참조 · 2026-08-24T13:00:00Z
- **CATCUS 2회차 재확인 상세**: GT솔라나트렌딩3위 유지, CA 확보(66ZEoQSgY3g5KEijP8ZUucth9ZmrxwYg8ngzwgP6pump), 유동성$39,575(+5.1%), 전지표 2회차 연속 양전 · 2026-08-24T13:00:00Z
- **나머지 상세**: OBS 2연속개선. PEPECOIN 3연속악화. MAPLE 유입반전. CLOCKIN h24감속. TIPANSEM whipsaw지속. LIZARD 연속whipsaw. CLUG 혼조전환. PEE 정체. 40M 깊은음전권. MANEKI 12회차whipsaw. omo 소폭안정화. swappy 혼조. CYBERLEEK 혼조반전(DS실패→GT대체). CC 방향번복지속. Z500 장기악화흐름지속. KIRK 전지표개선단1회차. CONK 연속whipsaw+악화. CHUMP 2연속감속+첫유출조짐. PROLOGUE 9연속유입. JUGGERNAUT 3연속개선. GOOD h24재음전. PITCOIN 안정적. PRINTER 안정적. Dealer 연속whipsaw+악화. TOAD 개선흐름반전. DPG 깊은음전권. BULLSHIT PumpSwap기준첫안정화. Doge2 대폭개선단1회차. CATE 전지표개선방향. Dinger 전지표개선단1회차. BARRON whipsaw지속. PANTS h24깊은음전권. Truth Coin 깊은음전권. YOMOGI 극단변동지속 · 2026-08-24T13:00:00Z

## KOL 코로보 (확보된 것만)

- **JUGGERNAUT — Drallio 코로보 carryover 유지, 신규 없음**.
- **CLOCKIN — 프로젝트 자체 서사(제3자 KOL 코로보 아님) carryover 유지**.
- **FWA — Cointelegraph·CryptoBriefing·KuCoin·PANews·CG트렌딩12위(전부 carryover 유지, 신규 없음)**.
- **CASHCAT(notable) — The Defiant "pump.fun이 로빈후드체인 토큰거래 지원 추가, CASHCAT 밈코인 열풍이 계기" 보도(carryover 유지, 신규 없음)**.
- **나머지 40종(신규발굴 없음) — 코로보 미확인**: 이번 회차는 44개 활성종목 전량 재확인, 데이터 신뢰도 이슈(배치 환각·조회값 불일치·소스 상충) 대응에 집중했다. 개별 KOL 검색·X 직접 조회는 로그인월 문제로 이번 회차도 대부분 생략했다 — 코로보 없음(정상 상태, 결함 아님).

## 메모

- **⏱️ 이번 회차 간격**: 직전(2026-08-24 11:00Z)로부터 정확히 **2시간** 경과(정시 슬롯 정상 진행).
- **🚨 최대 이슈: DexScreener 데이터 신뢰도 저하**: 이번 회차는 DS 서버 오류(500/522/525/타임아웃)가 극심했고, 성공한 응답 중에서도 배치 환각(1B·FLUSH)·재조회값 불일치(BRODIE·CHUMP)·직전값 완전동일 캐시의심(FWA)·유동성필드 없는 이상 페어(CYBERCAT)·GT와 부호 자체 상충(CATALORIAN) 등 5가지 유형의 데이터 이상이 한 회차에 동시 발생했다. 전부 재조회·교차검증으로 정정했으나, 이 패턴이 반복된다면 다음 회차부터 GT를 1차 소스로 격상하는 것도 고려할 만하다.
- **1회성 신호 반전이 특히 많았던 회차**: FLUSH(4연속악화로 상향), HOOKR·lickingcat·CALLOOOR·FWA(직전 다운그레이드가 1회만에 재반전) 등 이 워치의 핵심 원칙("단발 개선을 추세로 확정하지 말라")이 한 회차에 5건 가까이 재검증됐다. 반대로 JUGGERNAUT(3연속개선)·PROLOGUE(9연속유입)처럼 다회차 확인된 종목은 견고하게 유지됐다.
- **CATALORIAN 데이터 신뢰도 재확인 필요**: DS·GT h24 부호 자체가 상충한 것은 이 워치 사상 처음이다. 이번 회차는 GT(2경로 교차확인)를 채택했으나, 다음 회차 DS가 정상화되는지 최우선으로 재확인해야 한다.
- **CATCUS CA 확보**: 신규 발굴 이후 2회차 연속 GT 상위권(3~4위) 유지, CA도 이번 회차 확보했다. 다만 풀 나이가 아직 1일 미만이라 tokens 편입은 다음 회차 재검토 대상.
- **데이터 신뢰도**: 이번 회차는 DS 서버 안정성이 크게 저하돼 44개 종목 확보에 평소보다 훨씬 많은 재시도가 필요했다(1B·FLUSH·BRODIE·CHUMP·CYBERLEEK·CATALORIAN·CYBERCAT는 GT 교차검증 또는 다회 재조회로 최종값 확정). GeckoTerminal 솔라나·로빈후드체인 트렌딩 API는 안정적으로 응답해 다수 종목 교차검증 및 notable 항목 갱신(CATCUS·LOOKSMAX·Morty·Polycat·DOPAMEME·CVXV666·CASHCAT·STONKBROKER·PONS·HOODRAT·AI/NVDA)에 활용했다. X 직접 조회는 로그인월로 시도하지 않아 대부분 종목의 KOL 코로보는 미확인(정상 상태).

---
*Not financial advice. 본 문서는 공개 2차 자료·GeckoTerminal(API)/DexScreener(API)/CoinGecko(API)/WebSearch 기반 개인 정보 모니터링·조기경보용이며 매수 추천이 아님. 재실행 시 갱신.*
