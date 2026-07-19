# memewallet — 밈코인 수익 지갑 추적 & F/U 봇

> 사이드 프로젝트. crypto-trader(단타봇)와 **독립**. 개인용 정보 모니터링이며 매수추천 아님.

## 목표
2024년 이후 시총 **$200M+ 달성 밈코인**들의 거래를 추적해 →
**내부자(초기 할당·번들러·dev·1블록 스나이퍼) 제외** + **실거래 지갑** 중 →
아래 스크리닝을 통과한 "스마트머니" 지갑들의 신규 매매를 **F/U(알림)** 하는 봇.

## 스크리닝 기준 (확정)
1. **비내부자** — 출시 초기 할당·번들러·dev·1블록 스나이퍼 제외
2. **실거래 지갑** — 매수/매도가 실제 발생(에어드랍 보유만 하는 지갑 아님)
3. **Lifetime PnL > 0**
4. **누적 실현수익 ≥ $100,000**
5. **(추가) 최근 지속성** — 과거 1회 대박(생존편향) 배제: 다수 토큰에서 수익 + 최근 90일에도 순+
   (파라미터는 데이터 보고 조정). ⚠️ 이 기준의 근거: "과거 수익 지갑"이 미래도 벌 보장은 없고
   운으로 한 번 크게 먹은 지갑이 섞이므로, 지속성 필터로 걸러야 함.

## 설계 결정 (2026-07-19)
- **체인**: 솔라나 우선(2024+ 대형 밈코인 대부분). 검증 후 ETH/Base 확장.
- **데이터**: 기존 스마트머니 API 활용(원시 인덱싱 자체구축 아님).
- **봇 동작**: **알림만**(선별 지갑 신규 매수 감지 → 텔레그램 + 기록). 자동 카피트레이드는
  알림 MVP 검증 후 별도 결정(별도 실행 스택·리스크).

## 파이프라인 (5단계)
| 단계 | 내용 | 무료 도구 |
|---|---|---|
| ① 대상 토큰 열거 | 2024+ 피크 mcap≥$200M 밈코인 | CoinGecko(시드) + Dune/Flipside(과거 피크) |
| ② 홀더·출시할당 추출 | 초기 할당/번들러 → 내부자 태깅 | Bitquery(SPL 홀더·전송 전이력) / Helius |
| ③ 지갑 lifetime PnL | 매수/매도 realized 계산 | Birdeye Wallet PnL API / GMGN·Cielo 리더보드 / Flipside SQL |
| ④ 스크리닝 | 위 기준 1~5 적용 | 자체 필터 |
| ⑤ F/U 알림봇 | 선별 지갑 신규 스왑 감지 → 텔레그램 | Helius Webhooks → 기존 텔레그램 인프라 |

## 무료 API 접근성 점검 (2026-07-19, 이 컨테이너 프록시 경유)
| 서비스 | 상태 | 비고 |
|---|---|---|
| CoinGecko | ✅ 200 (키 불필요) | 밈 카테고리·현재 mcap·ATH. 스테이지① 시드 |
| DexScreener | ✅ 200 (키 불필요) | 토큰/페어 데이터 |
| Birdeye | 🔑 401 (도달O, 키 필요) | Wallet PnL API(실현/미실현) |
| Bitquery | ✅ 키확보·작동 (아래 주의) | `streaming.bitquery.io/eap` X-API-KEY로 realtime 200 |
| Dune | 🔑 (도달O, 키 필요) | 무료 2,500쿼리/월 SQL, 과거 Solana DEX |
| Helius | 🔑 (도달O, 키 필요) | 무료 100k크레딧, RPC+웹훅(⑤ 실시간) |
| Flipside | 🔑 403 (도달O, 키 필요) | 무료 SQL, **과거** Solana DEX 커버리지 최고 |
→ **프록시 차단은 없음.** 무료 키만 발급하면 사용 가능.

### ⚠️ Bitquery 무료 플랜 제약 (2026-07-19 실측)
- 발급 키(X-API-KEY)는 **작동하나 무료 플랜 = "realtime" 데이터셋 전용**. `archive`(과거) 쿼리는
  **402 Payment Required**로 막힘. 실측: realtime Solana DEXTrades → 200 OK, archive Blocks → 402.
- **결론(역할 분담)**: Bitquery 무료키는 **⑤ 실시간 모니터링**에만 사용. **①~④ 과거 백필**
  (역대 밈코인 거래·lifetime PnL·초기 홀더)은 **Flipside/Dune 무료 SQL**(과거 데이터 무료)로 수행.

## 스파이크 결과 (2026-07-19)
- **스테이지① 프로토타입 성공**: CoinGecko 무료로 밈 카테고리 현재 mcap≥$200M **12개** 확보
  (DOGE·SHIB·PEPE·PUMP·TRUMP·PENGU·SPX·BONK·FLOKI·M·PEANUT 등). `enumerate_seed.py` 참조.
- **한계**: "현재 ≥$200M"만으론 부족 — **2024+ 피크는 ≥$200M였다가 지금 하락한 것**(BONK -95%,
  PEPE -90% 등)이 다수라, 완전한 목록은 **과거 시총 데이터(Dune/Flipside/Bitquery, 키 필요)**로
  백필해야 함. ATH가격·ATH일자로 대략 추정은 가능(공급변동으로 부정확).

## 다음 단계 (수정: Bitquery=realtime 확인 후)
- **⑤ 실시간 모니터링**: `BITQUERY_API_KEY` 확보·작동(realtime). 선별 지갑 신규매매 감지에 사용 가능.
- **①~④ 과거 백필(핵심)**: Bitquery 무료로는 archive 불가 → **Flipside 또는 Dune 무료 SQL 필요**.
  1. **[블록]** 사장님이 Flipside(권장, 과거 Solana 커버리지 최고) 또는 Dune 무료 가입 → 키를 `.env`에
     `FLIPSIDE_API_KEY=...`(또는 `DUNE_API_KEY=...`)로 추가.
  2. 스테이지①: 과거 피크≥$200M 밈코인 확정 목록(Flipside/Dune 과거 mcap로 CoinGecko 시드 보강).
  3. 스테이지②: 1개 토큰으로 초기 홀더 vs 실거래 지갑 분리 + 내부자 태깅(초기 수령·번들러).
  4. 스테이지③: 거래 지갑 lifetime PnL 계산(swap 이력 SQL), 기준 1~5 적용해 후보 산출.
  5. end-to-end 검증 후 전체 확장 → ⑤ 알림봇(Bitquery realtime/Helius 웹훅 → 텔레그램).

## 실행
```
python sideprojects/memewallet/enumerate_seed.py    # 스테이지① 시드(키 불필요)
```
