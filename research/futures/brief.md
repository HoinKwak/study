# 선물시장 스카우트 브리핑 — 2026-08-16 10:30 UTC (KST 2026-08-16 19:30)

> CEX(바이낸스·바이빗·OKX)·DEX 퍼프(Hyperliquid·Aster·dYdX·OrangeX) 선물시장에서 지금
> 주목받는 **크립토 네이티브** 종목을 거래량·미결제약정(OI)·펀딩 기준으로 집계. **토큰화 주식·ETF·
> 상품·프리IPO/합성 perp는 전부 제외.** 정보 요약이며 투자조언 아님. **직전 회차(2026-08-16T08:30:00Z)
> 로부터 약 2시간 경과.**

## 시장 전반 — OrangeX API 전면 중단·BEAT 급반전(개선→악화)·AAVE 반전 재붕괴·BANK 언락 13시간 앞 플러스 확대·HYNA:SOL-USD stale 확정

**⚠️⚠️⚠️ 이번 회차 최대 발견은 OrangeX API의 전면 서비스 중단이다.** `get_currencies`가
에러코드 1000 **"No service found"**를 반환했고, `get_instruments`는 currency=ACE/BTC·
kind=perpetual/future 등 시도한 모든 조합에서 빈 배열(`[]`)만 돌려줬으며, `ticker`
엔드포인트는 instrument_name을 ACE-USDT·ACE-PERPETUAL·ACE_USDT 등 여러 형식으로
시도해도 **"Instrument does not exist"(코드 5001)** 또는 파라미터 누락 시 **"System
error"(코드 9999)**만 반환했다. 직전 2개 회차에 걸쳐 BSB·ADA·ASTER·AEON·BLESS까지
커버리지가 크게 확대됐던 것과 정반대로, 이번 회차는 **ACE·BANK·APR·CASHCAT·AIO·AAVE·
ADA·ALGO·ASTER·AEON·KAITO·CAP·BICO·BEAT·BSB·BLESS·ALLO 전 종목의 OrangeX 라인이
전부 미확인(서비스 중단)**으로 후퇴했다. 특히 BANK(언락 임박)·ACE(OI 숏커버링 후속
추적)·AIO(3회 연속 동일값 stale 확정 후속 추적)·CASHCAT(4소스 초근접 수렴 추적) 등
이번 회차 핵심 추적 대상에서 OrangeX 축이 통째로 빠진 것이 아쉬운 공백이다.

**⚠️⚠️⚠️ BEAT는** 지난 2개 회차의 강한 개선 흐름이 이번 회차 급격히 역전됐다 — OKX
-8.6329%→**-20.67%**, Aster -10.634%→**-22.004%**, 그리고 이번 회차 **처음 확인된
Binance**가 -20.833%(OI $8.01M)로 3소스 전원 다시 -20%대로 악화됐다. OrangeX는 서비스
중단으로 비교할 수 없으나, 확인된 3소스가 일관되게 역전된 것은 뚜렷하다.

**⚠️⚠️⚠️ AAVE도** 직전 회차 처음 나타난 '4소스 전원 개선 반전'이 단 한 회차 만에 다시
꺾였다 — B+B -0.8397%→**-1.5904%**, Aster -0.887%→**-1.674%**, Hyperliquid
-0.772%→**-1.612%**로 확인된 3소스 전원이 재차 악화됐다(OrangeX는 서비스 중단으로
미확인). 직전 회차의 '첫 개선 반전'이 지속 추세가 아니라 노이즈였을 가능성을 시사한다.

**⚠️⚠️⚠️ BANK는** 언락(8/17, 이제 약 **13시간** 앞)을 목전에 두고 오히려 방향이
플러스 쪽으로 더 뚜렷해졌다 — B+B -0.1314%→**+0.9553%**, Aster
+0.409%→**+0.625%**로 2확인 소스 모두 플러스폭이 확대됐다(OrangeX는 서비스 중단으로
미확인, 직전 -0.74%였던 소스가 공백).

**⚠️⚠️⚠️ ACE는** 언락(8/18, 약 1.5일 앞)을 앞두고 3확인 소스(OrangeX 제외) 전원이
회복을 이어갔다 — B+B -30.877%→**-27.06%**, Hyperliquid -32.796%→**-27.254%**,
Aster -31.63%→**-26.357%**. 다만 직전 회차 핵심 관찰이던 'OrangeX OI -23.9% 급감
(숏 커버링 시사)'의 지속 여부는 OrangeX 서비스 중단으로 이번 회차 확인이 불가하다.

**⚠️⚠️⚠️ APR은** 강한 재수렴 흐름이 계속됐다 — B+B -9.4348%→**-4.608%**, Aster
-6.859%→**-5.307%**로 개선, OKX만 -5.016%→**-6.05%**로 소폭 반대 방향이었으나
3소스가 -4.6%~-6.05%의 좁은 범위(1.44%p 스프레드)를 유지했다(OrangeX 미확인). OKX
vol/OI는 37.77배→**36.88배**로 소폭 개선되나 여전히 고평가.

**⚠️⚠️⚠️ CASHCAT은** OrangeX 공백에도 나머지 소스가 여전히 좁은 범위에 밀집했다 —
Hyperliquid +3.025%→**+2.432%**, Aster +2.51%→**+3.167%**, 현물(CoinGecko
cash-cat) +2.9036%→**+2.8344%**로 3소스가 **+2.43%~+3.17%(스프레드 0.735%p)**에
모였다 — OrangeX 공백을 감안해도 여전히 타이트한 수렴이며, 현물값이 이번 회차
소수점까지 다르게 갱신돼(2.9036%→2.8344%) 부모 세션이 우려한 '캐시 재노출 의심'과
달리 이번엔 정상 갱신으로 판단된다.

**⚠️⚠️⚠️ AIO는** CEX·Aster가 재가속을 이어갔다 — B+B +31.881%→**+42.35%**, Aster
+32.722%→**+44.123%**로 계속 급등. OrangeX는 서비스 중단으로 3회 연속 동일값
(-17.97%) stale 확정 이후의 지속 여부를 이번 회차 확인하지 못했다 — 다음 회차
재확인 필요.

**⚠️⚠️⚠️ HYNA:SOL-USD는** 이번 회차 OI뿐 아니라 **거래량·chg24까지 직전 회차와
소수점 단위로 완전히 동일**했다(vol $22,210.82, OI $531,931.68, chg +0.252% 전부
불변) — OI만 동일했던 지난 회차보다 한 단계 더 나아가 전 필드가 얼어붙어, AIO
OrangeX와 같은 기준(3회 이상 완전 동일 시 stale 확정)에 따라 **stale이 확정**된다.
반면 **HYNA:ETH-USD는 이번 회차 vol·OI·chg 전부 변동**해(OI $1,807,444.66→
$1,774,399.65) stale 우려가 해소됐다. 추가로 **HYNA:HYPE-USD도 vol·OI·chg24가
직전 회차와 완전히 동일**($16,430.95·$587,902.37·+2.07%)해 새로운 stale 관찰
대상으로 부상했다 — 다음 회차 재확인이 필요하다.

**⚠️⚠️ AEON은** 냉각이 거의 마무리 국면에 진입했다 — OKX +16.140%→**+3.47%**,
Bybit +14.845%→**+1.897%**, Aster +15.228%→**+0.777%**로 3소스 전원이 손익분기
근접까지 냉각됐다(OrangeX 미확인).

**⚠️ CAP은** OKX가 이번 회차 처음 마이너스로 전환됐다 — OKX
+0.7215%→**-0.804%**로 반전, Aster는 +0.913%→**+0.391%**로 플러스는 유지하나
계속 냉각(OrangeX 미확인). OKX vol/OI는 13.36배→**11.22배**로 정상군(0.3~11배)
진입에 근접했다.

**⚠️ BICO는** OKX vol/OI가 12.06배→**12.74배**로 정상군 상단을 더 벗어났다 — OKX
chg -1.1407%→**-1.00%**로 거의 보합, Aster는 -0.127%→**-1.729%**로 소폭 악화.
Bybit는 이번 회차도 미확인 지속(OrangeX도 미확인).

**⚠️ BSB는** OKX가 -0.5873%→**-3.006%**로 크게 악화됐고 Aster는
-0.88%→**-0.643%**로 소폭 개선해 방향이 갈렸다(OrangeX 미확인).

**KAITO는** 3확인 소스가 대체로 보합~소폭 악화 — OKX -7.0355%→**-7.93%**,
Hyperliquid -8.369%→**-8.2%**로 -7.9%~-8.2% 범위 유지(OrangeX·Bybit 미확인).

**ALGO는** 방향이 다시 갈렸다 — B+B +0.1366%→**-0.546%**로 마이너스 재전환,
Aster -0.821%→**-0.44%**로 소폭 개선, Hyperliquid(신규 확인) **-0.548%**.

**ATOM은** 대체로 플러스 유지하나 소스간 소폭 갈렸다 — B+B
+0.9216%→**+0.9434%**, OKX +0.8784%→**+1.011%**로 견조, Aster는
+0.812%→**-0.202%**로 마이너스 재전환(소액 거래량이라 노이즈 가능성).

**ADA는** 3확인 소스 전원 소폭 악화됐다 — B+B -0.7093%→**-1.623%**, Aster
-0.67%→**-1.733%**, Hyperliquid -0.642%→**-1.65%**(OrangeX 미확인).

**1000RATS(Aster)는** 3회 연속 동일값(+8.921%)이던 chg가 이번 회차
**+7.317%로 마침내 변동**해 stale 우려가 해소됐다.

**메이저(BTC/ETH/SOL)는** 이번 회차도 노이즈 수준 등락 — dYdX BTC
**-0.0529%**, ETH **-0.0217%**, SOL **-0.1524%**(전부 부호 반전, 절대값은
여전히 극소); Hyperliquid BTC -0.032%, ETH +0.016%; Aster BTC -0.036%.

**CoinGecko `/global`은** 총시가총액 $2,251.50B→**$2,249.83B**(소폭 하락), BTC
도미넌스 56.16%→**56.15%**(거의 보합)이다.

## ⚠️⚠️⚠️ 데이터: OrangeX API 전면 서비스 중단

이번 회차는 OrangeX API가 세 가지 독립 엔드포인트 모두에서 실패했다:
- `get_currencies` → **코드 1000 "No service found"**
- `get_instruments`(currency=ACE/BTC/USDT, kind=perpetual/future 전 조합) →
  **빈 배열 `[]`**
- `ticker`(instrument_name=ACE-USDT/ACE-PERPETUAL/ACE_USDT 등) →
  **코드 5001 "Instrument does not exist"**(파라미터 없이 호출 시 코드 9999
  "System error")

직전 2개 회차에 걸쳐 안정적으로 확장되던 커버리지(BSB·ADA·ASTER·AEON·BLESS
신규 확인 포함)가 이번 회차 완전히 사라졌다. 이는 개별 종목 이상이 아니라
**엔드포인트 전체의 장애**로 판단되며, 다음 회차 재시도가 필요하다.

## ⚠️⚠️⚠️ 데이터: OKX ctVal 개별 재조회 — 신규 배치조회 오류 없음

이번 회차 13개 OKX 종목(APR·BEAT·CAP·BICO·KAITO·ATOM·BSB·MMT·AEON·GRAM·GIGGLE·
PIPPIN·CORE, CAP·BSB·ATOM·CORE 4종은 개별 티커 재조회로 확인)을 `volCcy24h =
vol24h × ctVal` 관계로 교차검증한 결과 **전 종목이 각자의 ctVal(APR 10·BEAT
10·CAP 100·BICO 1·KAITO 1·ATOM 1·BSB 10·MMT 10·AEON 10·GRAM 1·GIGGLE 0.01·
PIPPIN 10·CORE 1)과 정확히 일치**해 이번 회차도 신규 배치조회 오류를 발견하지
못했다.

잔존 이상 종목:
- **APR**: vol/OI 37.77배→**36.88배**(소폭 개선이나 여전히 고평가)
- **BEAT**: vol/OI 35.68배→**34.43배**(소폭 개선되나 chg24 자체는 오히려 급락)
- **CAP**: vol/OI 13.36배→**11.22배**(정상군 진입에 근접)
- **BICO**: vol/OI 12.06배→**12.74배**(정상군 상단 이탈 폭 더 확대)

## ⚠️⚠️⚠️ 데이터: Aster 14회차 연속 차단, Bybit 재확인 지속 실패/일부 성공

**Aster 직접 API(`fapi.asterdex.com`)가 이번 회차도 `/fapi/v1/ping`에서 403으로
차단**돼 **최소 14회차 연속** 전면 차단이 확인됐다. CoinGecko `aster` 거래소
티커로 대체 확보했으며, **Aster ETH는 이로써 36회차 연속** 미확인이다.

**KAITO·BICO·CASHCAT Bybit 라인은 이번 회차도 이중 실패가 지속**됐다. 다만
**AEON Bybit는 재확인**됐으며 값이 대폭 냉각(+14.845%→+1.897%)됐다.

**BEAT Binance는** 그동안 우선순위 밖으로 미조회였으나 **이번 회차 처음
확인**돼 OKX·Aster와 함께 급격한 역전 방향(-20.833%)이 일치함을 뒷받침했다.

## BEAT — 급격한 역전(개선 → 재악화)

- **OKX**: -8.6329%→**-20.67%** (vol/OI 34.43배)
- **Aster**: -10.634%→**-22.004%**
- **Binance**(신규 확인): **-20.833%** (OI $8.01M)

## AAVE — 첫 개선 반전이 단 1회차 만에 재붕괴

- **Binance+Bybit(가중)**: -0.8397%→**-1.5904%**
- **Aster**: -0.887%→**-1.674%**
- **Hyperliquid**: -0.772%→**-1.612%**

## BANK — 언락 약 13시간 앞, 플러스폭 확대

- **Binance+Bybit(가중)**: -0.1314%→**+0.9553%**
- **Aster**: +0.409%→**+0.625%**
- OrangeX: ⚠️ 서비스 중단으로 미확인

## ACE — 회복 지속, 언락 8/18 약 1.5일 앞

- **Binance+Bybit(가중)**: -30.877%→**-27.06%**
- **Hyperliquid**: -32.796%→**-27.254%**
- **Aster**: -31.63%→**-26.357%** (OI $236,578→$226,437, -4.3%)
- OrangeX: ⚠️ 서비스 중단으로 미확인(OI 숏커버링 지속 여부 확인 불가)

## APR — 재수렴 지속(스프레드 1.44%p)

- **Binance+Bybit(가중)**: -9.4348%→**-4.608%**
- **Aster**: -6.859%→**-5.307%**
- **OKX**: -5.016%→**-6.05%** (vol/OI 36.88배)
- OrangeX: ⚠️ 서비스 중단으로 미확인

## CASHCAT — OrangeX 공백에도 3소스 타이트 수렴

- **Hyperliquid**: +3.025%→**+2.432%**
- **Aster**: +2.51%→**+3.167%**
- **현물(CoinGecko cash-cat)**: +2.9036%→**+2.8344%**
- OrangeX: ⚠️ 서비스 중단으로 미확인

## AIO — 재가속 지속, OrangeX stale 지속 여부 미확인

- **Binance+Bybit(가중)**: +31.881%→**+42.35%**
- **Aster**: +32.722%→**+44.123%**
- OrangeX: ⚠️ 서비스 중단(3회 연속 동일값 -17.97% 확정 이후 상황 미확인)

## HYNA:SOL-USD / HYNA:ETH-USD / HYNA:HYPE-USD — stale 상태 재점검

- **HYNA:SOL-USD**: vol·OI·chg24 전부 직전과 완전 동일 → **stale 확정**
- **HYNA:ETH-USD**: vol·OI·chg24 전부 변동 → stale 우려 해소
- **HYNA:HYPE-USD**: vol·OI·chg24 전부 직전과 완전 동일 → **신규 stale 관찰 대상**

## 그 외 관찰

- **AEON**: 4~5회차 이어진 냉각이 거의 마무리(+0.78%~+3.47%로 손익분기 근접).
- **CAP**: OKX 이번 회차 처음 마이너스 전환, vol/OI는 정상군 진입 근접(11.22배).
- **BICO**: OKX vol/OI 상단 이탈 폭 확대(12.74배), Bybit 미확인 지속.
- **BSB**: OKX -3.01%로 크게 악화, Aster는 소폭 개선 — 방향 갈림.
- **1000RATS(Aster)**: 3회 연속 동일값 stale 우려 해소(chg 변동 확인).
- **메이저**: 노이즈 수준이나 부호 다수 반전(플러스→마이너스).

## CEX 주목 종목 (메이저 제외, 크립토 네이티브만)

| 종목 | 거래소 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [회복 지속] | Binance+Bybit(가중평균) | $444.72M | $16.38M | -1.0228 | -27.06% | 3확인 소스 회복 지속, OrangeX 미확인 | recovery-continues-orangex-outage |
| **APR** [재수렴 지속] | Binance+Bybit(가중평균) | $206.95M | $17.95M | 0.005 | -4.608% | 3소스 1.44%p 스프레드 유지 | reconvergence-continues |
| **APR** | OKX(직접API) | $186.29M | $5.05M | 0.0002388 | -6.05% | vol/OI 36.88배 | reconvergence-continues |
| **BANK** [⚠️⚠️⚠️ 언락 13시간 앞] | Binance+Bybit(가중평균) | $24.85M | $15.38M | 0.005 | +0.9553% | 플러스폭 확대, OrangeX 공백 | unlock-imminent-turns-more-positive-orangex-outage |
| **BEAT** [⚠️⚠️⚠️ 급격한 역전] | OKX(직접API) | $209.62M | $6.09M | 0.00005 | -20.67% | 개선 흐름이 재악화로 반전 | reverses-sharply-improvement-undone |
| **BEAT** [⚠️ 신규 확인] | Binance | $117.58M | $8.01M | 0.005 | -20.833% | 역전 방향 일치 확인 | newly-confirmed-this-round-confirms-reversal |
| **KAITO** [보합] | OKX(직접API) | $29.88M | $5.18M | -0.0004528 | -7.93% | HL과 근접 유지 | roughly-flat-orangex-bybit-unconfirmed |
| **KAITO** [재확인 실패] | Bybit | — | — | — | — | 이중 재확인 실패 | reconfirmation-failed-again-not-carried-forward |
| **ALGO** [마이너스 재전환] | Binance+Bybit(가중평균) | $5.33M | $12.92M | -0.011539 | -0.546% | — | flips-negative-again |
| **MMT** [개선] | OKX(직접API) | $6.51M | $2.44M | -0.00006881 | -0.28% | — | improves |
| **AEON** [⚠️⚠️ 냉각 거의 마무리] | OKX(직접API) | $101.78M | $3.48M | -0.0002452 | +3.47% | 3소스 손익분기 근접 | cooling-nearly-complete |
| **AEON** [⚠️⚠️ 냉각 거의 마무리] | Bybit | $14.29M | $0.90M | 0.005 | +1.897% | — | cooling-nearly-complete |
| **BICO** [⚠️ vol/OI 상단 이탈 확대] | OKX(직접API) | $43.31M | $3.40M | -0.004839 | -1.00% | vol/OI 12.74배 | worsens-upper-band-deviation-widens |
| **BICO** [재확인 실패] | Bybit | — | — | — | — | 이중 재확인 실패 | reconfirmation-failed-again-not-carried-forward |
| **CAP** [⚠️⚠️ 이번 회차 첫 마이너스] | OKX(직접API) | $127.46M | $11.36M | -0.0006925 | -0.804% | vol/OI 정상군 진입 근접 | flips-negative-first-time |
| **ALLO** [냉각, 플러스 유지] | Binance+Bybit(가중평균) | $50.44M | $15.59M | -0.04648 | +1.3953% | — | cools-stays-positive |
| **ATOM** [견조] | Binance+Bybit(가중평균) | $12.72M | $31.89M | 0.007573 | +0.9434% | Aster만 마이너스 재전환 | stays-firm-aster-diverges |
| ATOM [견조] | OKX(직접API) | $1.98M | $4.11M | 0.0001 | +1.011% | — | stays-firm-aster-diverges |
| **ASTER** [거의 보합] | Binance+Bybit(가중평균) | $8.95M | $110.67M | 0.00175 | -0.066% | — | stays-roughly-flat-tight-range |
| **AAVE** [⚠️⚠️⚠️ 개선 반전 재붕괴] | Binance+Bybit(가중평균) | $25.65M | $83.84M | -0.002418 | -1.5904% | 3확인 소스 전원 재악화 | reversal-undone-again |
| **AIO** [⚠️⚠️⚠️ 재가속 지속] | Binance+Bybit(가중평균) | $119.77M | $8.77M | 0.05116 | +42.35% | OrangeX stale 지속 여부 미확인 | reaccelerates-further-orangex-outage |
| GRAM [냉각, 플러스 유지] | OKX(직접API) | $1.84M | $6.08M | 0.00005 | +0.30% | — | cools-stays-positive |
| GIGGLE [마이너스 전환] | OKX(직접API) | $5.89M | $1.66M | 0.00005 | -0.74% | ctVal 재확인 일치 | flips-negative-ctval-reconfirmed |
| PIPPIN [소폭 악화] | OKX(직접API) | $0.94M | $1.64M | 0.0001128 | -0.81% | ctVal 재확인 일치 | worsens-mildly-ctval-reconfirmed |
| **ADA** [악화] | Binance+Bybit(가중평균) | $73.83M | $141.45M | -0.00632 | -1.623% | — | worsens-across-confirmed-sources |
| **1000RATS** [거의 보합] | Binance+Bybit(가중평균) | $6.72M | $15.61M | 0.0123 | +5.898% | — | roughly-flat |
| CORE [냉각, 플러스 유지] | OKX(직접API) | $3.12M | $0.90M | 0.0001 | +0.462% | — | cools-stays-positive |
| BSB [⚠️ 큰 폭 악화] | OKX(직접API) | $4.00M | $2.02M | 0.00005429 | -3.006% | Aster와 방향 갈림 | worsens-sharply-sources-diverge |

## DEX 퍼프 주목 종목 (Hyperliquid·Aster·dYdX·OrangeX)

| 종목 | 프로토콜 | 24h 거래량 | OI | 펀딩 | 24h 변동 | 왜 뜨는가 | 태그 |
|---|---|---|---|---|---|---|---|
| **ACE** [회복 지속] | Hyperliquid | $5.03M | $1.58M | -0.22 | -27.254% | — | recovery-continues-orangex-outage |
| **ACE** [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | OI 숏커버링 지속 여부 미확인 | orangex-service-outage-this-round |
| **ACE** [회복 지속] | Aster | $1.73M | $0.23M | -0.256 | -26.357% | OI -4.3% | recovery-continues-orangex-outage |
| **APR** [재수렴 지속] | Aster | $0.64M | $0.39M | 0.001 | -5.307% | — | reconvergence-continues |
| **APR** [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| **BANK** [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | 언락 임박 핵심 소스 공백 | orangex-service-outage-this-round |
| **BANK** [플러스폭 확대] | Aster | $0.08M | $0.25M | 0.001 | +0.625% | — | unlock-imminent-turns-more-positive-orangex-outage |
| **KAITO** [보합] | Hyperliquid | $11.75M | $6.63M | -0.016 | -8.2% | — | roughly-flat-orangex-bybit-unconfirmed |
| KAITO [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| CAP [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| CAP [냉각, 플러스 유지] | Aster | $0.16M | $0.19M | -0.015 | +0.391% | — | cools-stays-positive |
| BICO [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| BICO [소폭 악화] | Aster | $0.26M | $0.07M | -0.29 | -1.729% | — | worsens-upper-band-deviation-widens |
| BSB [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| BSB [소폭 개선] | Aster | $0.09M | $0.13M | 0.001 | -0.643% | OKX와 방향 갈림 | worsens-sharply-sources-diverge |
| BLESS [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| BLESS [개선] | Aster | $0.09M | $0.11M | 0.013 | -8.595% | — | improves |
| **CASHCAT** [⚠️⚠️⚠️ 3소스 타이트 수렴] | Hyperliquid | $5.47M | $17.22M | 0.001 | +2.432% | OrangeX 공백에도 유지 | three-sources-stay-tight-orangex-outage |
| **CASHCAT** [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | 4소스 수렴 핵심 축 공백 | orangex-service-outage-this-round |
| **CASHCAT** [⚠️⚠️⚠️ 타이트 수렴] | Aster | $1.01M | $1.09M | 0.005 | +3.167% | — | three-sources-stay-tight-orangex-outage |
| **AEON** [⚠️⚠️ 냉각 거의 마무리] | Aster | $0.43M | $0.28M | 0.008 | +0.777% | — | cooling-nearly-complete |
| AEON [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| BEAT [⚠️⚠️⚠️ 급격한 역전] | Aster | $3.07M | $0.40M | 0.001 | -22.004% | — | reverses-sharply-improvement-undone |
| BEAT [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | 역전이 OrangeX에도 나타나는지 미확인 | orangex-service-outage-this-round |
| HYPE [강화, 플러스 유지] | Hyperliquid | $82.03M | $1,278.29M | 0.001 | +2.571% | — | strengthens-stays-positive |
| GRAM [냉각, 플러스 유지] | Hyperliquid | $0.13M | $13.43M | 0.001 | +0.329% | — | cools-stays-positive |
| BTW [강화, 촉매 미확인] | Aster | $8.06M | $11.40M | 0.001 | +3.415% | — | flips-positive-catalyst-unconfirmed |
| HYNA:PUMP [마이너스 전환] | Hyperliquid | $0.03M | $0.18M | 0.001 | -0.542% | — | flips-negative |
| **HYNA:HYPE** [⚠️ 신규 stale 관찰] | Hyperliquid | $0.02M | $0.59M | 0.001 | +2.07% | vol·OI·chg 전부 직전과 동일 | new-stale-watch-full-freeze |
| **HYNA:SOL-USD** [⚠️⚠️⚠️ stale 확정] | Hyperliquid | $0.02M | $0.53M | 0.001 | +0.252% | vol·OI·chg 전부 직전과 동일 | stale-confirmed-full-freeze |
| HYNA:BTC-USD [거의 보합] | Hyperliquid | $0.13M | $2.12M | 0.001 | +0.006% | — | roughly-flat |
| **HYNA:ETH-USD** [⚠️ stale 우려 해소] | Hyperliquid | $0.14M | $1.77M | 0.001 | +0.096% | vol·OI·chg 전부 변동 | stale-watch-resolved |
| SOL [⚠️ 미확인] | Hyperliquid | — | — | — | — | 별도 티커 부재 지속 | remains-unconfirmed-no-separate-market |
| 1000RATS [⚠️ stale 해소] | Aster | $0.03M | $0.04M | 0.01 | +7.317% | 3회 연속 동일값 이후 변동 | stale-watch-resolved-value-finally-moved |
| AIO [⚠️⚠️⚠️ 재가속 지속] | Aster | $0.32M | $0.19M | 0.018 | +44.123% | CEX와 동조 급등 | reaccelerates-further-orangex-outage |
| AIO [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | stale값 지속 여부 미확인 | orangex-service-outage-this-round |
| AAVE [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| AAVE [⚠️⚠️⚠️ 개선 반전 재붕괴] | Aster | $0.33M | $4.43M | 0.01 | -1.674% | — | reversal-undone-again |
| AAVE [⚠️⚠️⚠️ 개선 반전 재붕괴] | Hyperliquid | $1.79M | $56.89M | 0.001 | -1.612% | — | reversal-undone-again |
| ADA [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| ADA [악화] | Aster | $0.46M | $1.29M | -0.001 | -1.733% | — | worsens-across-confirmed-sources |
| ADA [악화] | Hyperliquid | $2.63M | $28.27M | -0.001 | -1.65% | — | worsens-across-confirmed-sources |
| ALGO [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| ALGO [개선, 여전히 마이너스] | Aster | $0.005M | $0.03M | 0.0 | -0.44% | — | flips-negative-again |
| ALGO [⚠️ 신규 확인] | Hyperliquid | $0.31M | $1.81M | -0.003 | -0.548% | — | newly-confirmed-this-round |
| ASTER [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| ASTER [거의 보합] | Aster | $8.97M | $219.78M | 0.0 | -0.116% | — | stays-roughly-flat-tight-range |
| ASTER [거의 보합] | Hyperliquid | $0.42M | $13.63M | 0.001 | -0.037% | — | stays-roughly-flat-tight-range |
| ETH [마이너스 재전환] | dYdX | $0.34M | $20.51M | -0.0000124 | -0.02168% | 노이즈 수준 | majors-stagnate-noise-level |
| BTC [마이너스 재전환] | dYdX | $0.55M | $17.65M | 0.0 | -0.0529% | 노이즈 수준 | majors-stagnate-noise-level |
| SOL [마이너스 재전환] | dYdX | $0.47M | $5.63M | -0.0000466 | -0.1524% | 노이즈 수준 | majors-stagnate-noise-level |
| BTC [마이너스 재전환] | Hyperliquid | $235.42M | $2,798.21M | 0.001 | -0.032% | 노이즈 수준 | majors-stagnate-noise-level |
| ETH [플러스 전환] | Hyperliquid | $155.52M | $1,644.48M | 0.001 | +0.016% | 노이즈 수준 | majors-stagnate-noise-level |
| BTC [마이너스 재전환] | Aster | $83.77M | $793.94M | 0.004 | -0.036% | 노이즈 수준 | majors-stagnate-noise-level |
| ETH [⚠️ 미확인, 36회차 연속] | Aster | — | — | — | — | ping 403·CoinGecko 대체도 부재 | unconfirmed-36th-consecutive-round |
| HYPER [악화] | Hyperliquid | $0.07M | $0.20M | 0.001 | -2.489% | — | worsens-mildly |
| APEX [소폭 악화] | Hyperliquid | $0.10M | $0.57M | 0.001 | -3.328% | — | roughly-flat |
| FARTCOIN [냉각, 플러스 유지] | Hyperliquid | $5.61M | $30.15M | 0.001 | +1.295% | — | cools-stays-positive |
| ETHFI [냉각, 플러스 유지] | Hyperliquid | $2.18M | $12.32M | 0.001 | +0.556% | — | cools-stays-positive |
| ALLO [⚠️⚠️⚠️ 서비스 중단] | OrangeX | — | — | — | — | — | orangex-service-outage-this-round |
| ALLO [냉각, 플러스 유지] | Aster | $0.10M | $0.05M | -0.006 | +2.123% | — | cools-stays-positive |
| ATOM [마이너스 재전환, 소액 노이즈] | Aster | $0.03M | $1.78M | 0.008 | -0.202% | B+B·OKX는 여전히 견조 | stays-firm-aster-diverges |
| APR [⚠️ 미상장 추정] | Hyperliquid | — | — | — | — | 미발견 지속 | not-listed-on-hyperliquid |

## 테마 태그

1. **⚠️⚠️⚠️ 데이터: OrangeX API 전면 서비스 중단** — get_currencies 'No service
   found', get_instruments 전 조합 빈 배열, ticker 전 시도 오류. ACE·BANK·APR·
   CASHCAT·AIO·AAVE·ADA·ALGO·ASTER·AEON·KAITO·CAP·BICO·BEAT·BSB·BLESS·ALLO
   전 종목 OrangeX 라인이 미확인으로 후퇴 (orangex-service-outage-this-round).
2. **⚠️⚠️⚠️ BEAT: 2회차 이어진 강한 개선이 급격히 역전** — OKX·Aster·신규 확인
   Binance 3소스 모두 -20%대로 악화 (beat-reverses-sharply-improvement-undone).
3. **⚠️⚠️⚠️ AAVE: 첫 개선 반전이 단 한 회차 만에 다시 꺾임** — 확인된 3소스
   전원 재악화 (aave-reversal-undone-again).
4. **⚠️⚠️⚠️ BANK: 언락 약 13시간 앞두고 확인된 2소스 모두 플러스폭 확대**,
   OrangeX 공백으로 3번째 축 관찰 불가 (bank-unlock-imminent-turns-more-positive-orangex-outage).
5. **⚠️⚠️⚠️ ACE: 확인된 3소스 전원 회복 지속**, OrangeX 공백으로 OI 숏커버링
   지속 여부 미확인, 언락 8/18 약 1.5일 앞 (ace-recovery-continues-orangex-outage).
6. **⚠️⚠️⚠️ APR: 재수렴 흐름 지속**, 3소스 1.44%p 스프레드 유지
   (apr-reconvergence-continues).
7. **⚠️⚠️⚠️ CASHCAT: OrangeX 공백에도 3소스 타이트 수렴**(0.735%p), 현물값
   갱신으로 캐시 재노출 의심 해소 (cashcat-three-sources-stay-tight-orangex-outage).
8. **⚠️⚠️⚠️ AIO: B+B·Aster 재가속 지속**, OrangeX stale값 지속 여부 미확인
   (aio-reaccelerates-further-orangex-outage).
9. **⚠️⚠️⚠️ HYNA:SOL-USD: vol·OI·chg24 전부 직전과 완전 동일 — stale 확정.**
   HYNA:ETH-USD는 전부 변동해 해소 (hyna-sol-stale-confirmed-full-freeze,
   hyna-eth-stale-watch-resolved).
10. **⚠️ HYNA:HYPE-USD: vol·OI·chg24가 직전과 완전 동일 — 신규 stale 관찰
    대상** (hyna-hype-new-stale-watch-full-freeze).
11. **⚠️⚠️ AEON: 냉각이 거의 마무리 국면** — 3소스 전원 손익분기 근접
    (aeon-cooling-nearly-complete).
12. **⚠️ CAP: OKX 이번 회차 처음 마이너스 전환**, vol/OI 정상군 진입 근접
    (cap-flips-negative-first-time).
13. **⚠️ BICO: OKX vol/OI 상단 이탈 폭 확대**(12.74배), Bybit 미확인 지속
    (bico-worsens-upper-band-deviation-widens).
14. **⚠️ BSB: OKX 크게 악화, Aster는 소폭 개선 — 방향 갈림**
    (bsb-worsens-sharply-sources-diverge).
15. **ALGO: B+B 다시 마이너스 전환, Hyperliquid 신규 확인이 근접**
    (algo-flips-negative-again).
16. **1000RATS(Aster): 3회 연속 동일값이던 chg24가 마침내 변동 — stale 우려
    해소** (1000rats-stale-watch-resolved-value-finally-moved).
17. **⚠️⚠️⚠️ 메이저(BTC/ETH/SOL): 노이즈 수준이나 부호 다수 반전**
    (majors-stagnate-noise-level).
18. **⚠️⚠️⚠️ 데이터: OKX ctVal 개별 재조회로 13개 전 종목 ctVal 정확히
    일치** — 신규 배치조회 오류 없음. CAP 11.22배로 정상군 진입 근접, BICO
    12.74배로 상단 이탈 확대 (okx-ctval-no-new-errors-continues).
19. **⚠️⚠️⚠️ 데이터: Aster 직접 API 14회차 연속 403 차단**, ETH는 36회차
    연속 미확인 (aster-direct-api-blocked-14th-round).
20. **⚠️ BEAT Binance: 우선순위 밖이었으나 이번 회차 처음 확인**, 역전 방향
    일치 확인 (beat-binance-newly-confirmed-this-round).
21. **데이터: KAITO·BICO·CASHCAT Bybit 라인 이중 실패 지속, AEON Bybit는
    재확인**(값 대폭 냉각) (kaito-bico-cashcat-bybit-failure-persists-aeon-reconfirmed).
22. **글로벌 시총 $2,251.50B→$2,249.83B(소폭 하락), BTC 도미넌스
    56.16%→56.15%(거의 보합)** (global-mcap-dominance-roughly-flat).
23. **주식화·상품 토큰은 전부 제외.** 리스트 전 종목 크립토 네이티브 확인
    유지 (stock-commodity-tokens-excluded-crypto-native-confirmed).
24. **바이낸스 fapi 이번 회차도 CoinGecko binance_futures로 대체**(451
    지역차단 지속), **Bybit 직접 API도 CoinGecko bybit로 대체**
    (fapi-bybit-direct-blocked-coingecko-fallback).

## 한계

(a) CEX 신규 대형 급등 스캔은 기존 감시 종목·상위 리스트 범위 내에서 수행했으며
완전한 전체 시장 스캔은 아니다; (b) **주식화·상품·프리IPO 합성 perp 토큰**은 이번
회차도 규약에 따라 cex/dex 리스트에서 전부 제외했다; (c) OKX 직접 조회분의 CEX
거래량·OI는 이번 회차도 계약승수(ctVal)를 반영해 재계산한 값이며(`vol_usd =
volCcy24h × last_price`), `open-interest` 엔드포인트의 `oiUsd` 필드를 직접
활용했다. 13개 종목 전량(배치조회 9종+개별재조회 4종) ctVal 일치를 재확인해
신규 배치조회 오류는 발견하지 못했다. **APR·BEAT는 여전히 vol/OI 비율이
정상군(0.3~11배)을 상회**(36.88배·34.43배)해 다소 높은 값일 가능성을 배제할
수 없다. **CAP은 11.22배로 정상군 진입에 근접, BICO는 12.74배로 상단 이탈이
더 확대**됐다; (d) 복수 거래소 종목의 `chg24`·`funding`은 이번 회차 Binance+
Bybit 가중평균(거래량 가중)으로 산출했다; (e) Hyperliquid 원시 필드가 이번
회차도 정상 스케일로 관측돼 보정 없이 raw 값을 그대로 사용했다; (f) BICO·BEAT·
CAP·AEON·MMT·GIGGLE·PIPPIN·KAITO·GRAM·CORE·BSB·BLESS는 Binance/Bybit 상장이
불확실하거나 없어 OKX·DEX로만 집계되는 구조다(단 BEAT는 이번 회차 처음
Binance에서도 확인됨); (g) BTW·CASHCAT·HYNA 계열은 DEX에서만 상장이 확인돼
해당 섹션에서만 집계했다; (h) dYdX BTC/ETH/SOL은 raw JSON 필드(`oraclePrice`·
`openInterest`·`priceChange24H`(달러 절대값)·`nextFundingRate`·`volume24H`)를
직접 요청해 계산했으며, `priceChange24H`가 퍼센트가 아닌 달러 절대값임을
재확인해 오라클가 대비 백분율로 환산했다(BTC -33.25448, ETH -0.407253,
SOL -0.11451843); (i) **Aster 직접 API가 ping 엔드포인트에서 403 차단**됐으나
(최소 14회차 연속) CoinGecko `aster` 거래소 대체 경로는 지속 활용 가능했다
(단 ETH는 대체 경로에도 부재); (j) **⚠️⚠️⚠️ 이번 회차 가장 큰 발견은 OrangeX
API의 전면 서비스 중단이다** — 세 가지 독립 엔드포인트(get_currencies·
get_instruments·ticker) 모두에서 실패해 직전 2회차 커버리지 확장이 완전히
무효화됐다. 이는 개별 종목이 아닌 엔드포인트 전체의 장애로 판단되며,
다음 회차 재확인이 최우선 과제다; (k) Bybit BTC·ETH·SOL과 Binance BTCUSDT는
과거 회차 이상치 문제로 CEX 표에 넣지 않고 DEX(HL·Aster·dYdX)로 대체 추적
하는 구조를 이번 회차도 유지했다; (l) KAITO의 OI는 OKX·HL 모두 USD환산
기준이나 산출 방법이 달라 직접 비교가 아닌 각자의 추세로만 해석해야 한다;
(m) **BEAT·AAVE는 직전 회차의 개선 흐름이 이번 회차 뚜렷하게 재역전**됐다 —
급락 국면과 반등 국면이 반복되는 변동성 자체가 관찰 대상이다; (n) **Aster의
ETH 티커는 이번 회차도 확인 실패**(36회차 연속); (o) **HL SOL-USD**는 이번
회차도 별도 존재가 확인되지 않았다; (p) **⚠️⚠️⚠️ OrangeX는 이번 회차
전면 서비스 중단으로 funding 필드를 포함한 모든 데이터가 미확인**이다 —
직전까지 유지되던 'funding 구조적 부재' 판정 자체도 이번 회차엔 검증 불가;
(q) 메이저는 이번 회차 노이즈 수준에서 부호가 대부분 반전됐으나 절대값은
극소해 방향성 판단은 다음 회차 재확인이 필요하다; (r) dYdX BTC의 오라클
가격(~$62,930 수준)은 별도 스팟 가격과의 교차검증을 이번 회차도 수행하지
못했다; (s) dYdX funding 필드는 per-period(짧은 주기) rate로 추정되며,
스케일 해석은 계속 재확인이 필요하다; (t) **KAITO Bybit·BICO Bybit·CASHCAT
Bybit는 이번 회차도 Bybit 직접 API·CoinGecko bybit 티커 리스트 전수조회
모두 실패**해 지속 상장 여부가 불확실하다(단 AEON Bybit는 재확인됨); (u)
**BEAT Binance는 이번 회차 처음 확인**돼 우선순위 밖 재조회 범위 밖이던
상태에서 벗어났다; (v) **CASHCAT 현물 가격(cash-cat)이 이번 회차 h24
+2.8344%**로 3소스와 함께 여전히 타이트한 범위(0.735%p)에 수렴했다; (w)
**⚠️⚠️⚠️ HYNA:SOL-USD는 이번 회차 vol·OI·chg24 전부 직전 회차와 완전히
동일**해, AIO OrangeX와 동일한 '3회 이상 완전 동일 시 stale 확정' 기준에
따라 stale이 확정됐다 — 반대로 HYNA:ETH-USD는 전부 변동해 해소됐고,
HYNA:HYPE-USD는 새롭게 완전 동일 패턴을 보여 관찰 대상에 추가됐다; (x)
**언락 시각은 ACE·BANK·KAITO 모두 정확한 UTC 시각을 확인하지 못해
근사치이며, 실제 시각과 다를 경우 잔여시간 수치도 달라질 수 있다;** (y)
**글로벌 시총·도미넌스**는 이번 회차 CoinGecko `/global` 응답에서 총시가
총액 $2,249,828,413,764.78·BTC 도미넌스 56.1487%의 값을 확보했다(직전
회차는 $2,251,502,560,900.93·56.16%였음); (z) **⚠️⚠️⚠️ 이번 회차 가장 큰
발견 종합**: ①OrangeX API 전면 서비스 중단, ②BEAT·AAVE의 개선 흐름 재역전,
③BANK의 언락 임박 시점 방향 뚜렷화(플러스 확대), ④HYNA:SOL-USD의 stale
확정과 HYNA:ETH-USD의 해소가 대조를 이루며 '3회 이상 완전 동일 = stale
확정' 기준의 재현성을 뒷받침한다.

*투자조언 아님 — 시장 파악·아이디어 소싱용 정보 요약.*
