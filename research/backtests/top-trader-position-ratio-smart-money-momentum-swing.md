# 백테스트 -- [스윙] 상위 트레이더 포지션비율(사이즈가중) 스마트머니 추세추종

- **판정: FAIL**
- 일자: 2026-08-04
- 스펙: `research/strategies/top-trader-position-ratio-smart-money-momentum-swing.md`
- 구현: `research/impl/top_trader_position_momentum_common.py`(신호 생성·이벤트 루프),
  `research/impl/run_top_trader_momentum.py`(IS/OOS·민감도·강건성·방향반전 실행),
  `research/impl/lsr_contrarian_common.py` + `research/impl/run_contrarian_compare.py`
  (기존 `long-short-account-ratio-contrarian-swing.md` 간이 비교 구현)
- 실행 커맨드:
  ```
  cd /home/user/study && .venv/bin/python research/impl/run_top_trader_momentum.py
  .venv/bin/python research/impl/run_contrarian_compare.py
  ```

## 1. 데이터 가용성 사전 확인 (스펙이 명시한 필수 확인 사항)

`data.binance.vision/data/futures/um/daily/metrics/` 일별 덤프의 실제 컬럼:
```
create_time,symbol,sum_open_interest,sum_open_interest_value,
count_toptrader_long_short_ratio,sum_toptrader_long_short_ratio,
count_long_short_ratio,sum_taker_long_short_vol_ratio
```
- **`sum_toptrader_long_short_ratio`가 실제로 존재하며, 스펙이 요구한 "포지션 규모 가중" 컬럼
  (`topLongShortPositionRatio`에 해당)임을 확인**. `count_long_short_ratio`(전체 계정 수 가중 =
  `globalLongShortAccountRatio`)와의 상관계수는 0.20에 불과한 반면, `count_toptrader_long_short_ratio`
  (계정 수 기준)는 `count_long_short_ratio`와 0.97로 거의 동일 -- `sum_toptrader_...`가 계정수
  기준이 아닌 별개(포지션 규모 기준) 신호임을 뒷받침한다. **→ 스펙을 대체 없이 정확히 재현 가능.**
- 단, `sum_toptrader_long_short_ratio`(및 `count_toptrader_...`)가 **2022-01~2022-12 구간에서
  심하게 결측**(2022-02-15 등 여러 날짜의 원본 CSV를 직접 재다운로드해 재확인 -- 다운로드 실패가
  아니라 바이낸스 원본 자체가 빈 문자열). 7개 심볼 전부 동일한 날짜 패턴으로 결측되는 것으로 보아
  개별 심볼·네트워크 문제가 아니라 **바이낸스 아카이브 자체의 시스템적 공백**이다. rolling(30일)
  결측률이 2% 미만으로 안정되는 시점은 7종목 모두 **2023-01-13**.
- 따라서 **실효 IS 구간을 2023-01-13~2024-06-30(약 17.5개월)로 좁혀 실행**했다(스펙 지시 원 IS
  시작 2022-01-01보다 늦음, 정직하게 표기). OOS(2024-07~2026-06)는 결측 없이 정상.

## 2. 구현 방법 (요약)

- 4h OHLCV: 15m vendor 캐시 리샘플. `sum_toptrader_long_short_ratio`/`count_long_short_ratio`
  5분 스냅샷 → `.resample('4h').last()`로 OHLCV와 동일 규약(label/closed=left) 정렬(룩어헤드 없음).
- MA(6)/MA(18) 골든/데드크로스, 리테일(전체 계정) 미동조 확인은
  `global_ratio.diff(6) <= 0`(롱)/`>=0`(숏), 거래대금 확인은 `close*volume` 24h합(6봉) vs
  20봉 평균×1.2. ATR(4h,14). SL=진입가∓1.5×ATR, TP=RR 2.5, 반대크로스 재발생 시 다음봉 시가
  청산, 시간청산 42봉.
- 신호는 봉 i-1 종가 확정 → 체결 봉 i 시가(+슬리피지). 왕복 수수료 0.14%(테이커 0.05%+슬리피지
  0.02% 편도×2). RiskManager 1% 사이징 방식(risk_amount/stop_distance), 레버리지 10x(캡
  바인딩 안 됨, 확인함).
- 진입 필드 스키마 tz 정합 버그(원본 pandas datetime64[us] naive vs OHLCV tz-aware UTC --
  reindex 시 전량 NaN) 발견·수정 후 실행함(계측 후 확인, CLAUDE.md §5.4 원칙 반영).

## 3. IS/OOS 결과 (심볼별, 기본 파라미터)

| SYM | 구간 | n | PF | win% | pnl | MDD% | fees |
|---|---|---:|---:|---:|---:|---:|---:|
| BTC | IS | 47 | 0.73 | 29.8 | -774.6 | 10.71 | 248.4 |
| BTC | OOS | 32 | 0.92 | 43.8 | -121.8 | 4.82 | 152.9 |
| ETH | IS | 44 | 0.54 | 29.5 | -1269.1 | 13.83 | 178.2 |
| ETH | OOS | 51 | 1.44 | 49.0 | 811.2 | 4.15 | 148.9 |
| BNB | IS | 39 | 0.88 | 33.3 | -265.8 | 8.52 | 180.0 |
| BNB | OOS | 55 | 1.09 | 36.4 | 285.8 | 6.33 | 244.1 |
| SOL | IS | 28 | 1.72 | 53.6 | 853.5 | 3.36 | 65.6 |
| SOL | OOS | 55 | 0.62 | 32.7 | -1365.1 | 16.53 | 149.4 |
| XRP | IS | 26 | 2.26 | 57.7 | 1328.0 | 2.90 | 95.2 |
| XRP | OOS | 47 | 0.86 | 31.9 | -456.1 | 13.50 | 174.7 |
| DOGE | IS | 24 | 0.95 | 41.7 | -56.3 | 5.73 | 73.1 |
| DOGE | OOS | 45 | 1.01 | 35.6 | 23.3 | 8.23 | 114.9 |
| ADA | IS | 39 | 1.24 | 41.0 | 510.0 | 4.16 | 124.0 |
| ADA | OOS | 41 | 1.78 | 48.8 | 1874.2 | 5.69 | 133.3 |

- **Pooled IS**: n=247, PF=1.024 | **Pooled OOS**: n=326, PF=**1.058**
- Pooled(IS+OOS 전체) n=573, raw pnl=3459.9, 수수료=2082.7, 순pnl=1377.2, 승률 39.1%
- 수수료 정합 체크(`raw_pnl - fees == pnl`): diff = -0.00000000 (통과)
- 표본 수: 전 종목·전 구간 모두 20건 이상 → HOLD 아님, 판정 가능

## 4. 강건성

- **top-10 거래 제거 후 PF: 0.953** -- 상위 10건 제외 시 손실 전환. 소수 대박 거래에 의존.
- **Leave-one-symbol-out PF**: BTC 1.084 / ETH 1.068 / BNB 1.052 / SOL 1.070 / XRP 1.018 /
  DOGE 1.050 / ADA 0.963 -- 어떤 종목을 빼도 1.3 근처도 못 감.
- **파라미터 스윕**(모두 pooled IS+OOS): base 1.044, ma_fast=4→1.021, ma_fast=8→1.082,
  ma_slow=12→0.954, ma_slow=24→0.996, vol_mult=1.0→1.037, vol_mult=1.5→1.084(n=232),
  atr_sl=1.0→1.028, atr_sl=2.0→1.122, rr=2.0→1.004, rr=3.0→1.122, max_hold=30→1.056,
  max_hold=60→1.045, TP우선→1.044. **어떤 조합도 1.3을 넘지 못함**(최고 1.122).
- **방향 반전(모멘텀→페이드) 테스트**: n=547, PF=0.843 -- 반대 방향도 무엣지(오히려 더 나쁨).
  순추세·역추세 둘 다 아님 = 신호 자체가 수수료 이후 노이즈.

## 5. 컨트래리언 버전(`long-short-account-ratio-contrarian-swing.md`)과의 비교

기존 컨트래리언 스펙의 사전 백테스트가 `research/backtests/`나 git 이력에 없어, 이번 세션에서
**같은 데이터(global_ratio=count_long_short_ratio)로 요지 충실 간이 구현**하여 나란히 실행
(단순화: `topLongShortAccountRatio` 선택 필터 생략, percentile/중립대는 rolling quantile로 근사).

| | IS n / PF | OOS n / PF | top10제거 PF |
|---|---|---|---|
| 모멘텀(본 전략) | 247 / 1.024 | 326 / **1.058** | 0.953 |
| 컨트래리언(간이) | 393 / 1.107 | 599 / **1.387** | 1.209 |

- 컨트래리언 쪽이 OOS PF 1.387로 문턱(1.3)을 넘긴다. 다만 IS는 1.107로 미달, top10 제거 시
  1.209로 재차 미달 -- 이번 세션에서는 전체 강건성 스위트(파라미터 스윕·LOO·방향반전)를 이
  비교용 간이 구현에는 돌리지 않았다. **컨트래리언을 PASS로 단정하지 않는다** -- 별도 정식
  백테스트(스펙 전체 규칙 포함, `topLongShortAccountRatio` 다이버전스 가중까지 반영)가 필요함을
  정직하게 표기한다.
- **신호 상관관계**: 같은 방향 동시신호 29건, 반대방향 동시신호 0건, 모멘텀 단독 602건,
  컨트래리언 단독 3646건 -- 두 전략의 신호는 거의 겹치지 않는다(컨트래리언이 훨씬 자주
  발화 -- percentile 정의상 구조적으로 빈번). 스펙이 주장한 "메커니즘이 다르다(모멘텀 vs
  극단값 페이드)"는 실제로 확인됐다.

## 결론

**본 과제(스마트머니 모멘텀 스윙) 판정: FAIL.** 데이터는 스펙대로(포지션 규모 가중 컬럼 확인)
정확히 구현 가능했고, 표본도 충분(종목당 24~119건, 전체 573건)했지만, OOS PF 1.058로 기준(1.3)
크게 미달, top-10 제거 시 손실 전환, 전 파라미터 스윕에서 1.3 돌파 실패, 방향반전도 무엣지 --
수수료 이후 순수 노이즈에 가깝다. 라이브 반영 대상 아님.

**부수 발견**: 같은 데이터를 반대 극성(컨트래리언)으로 쓴 간이 구현이 OOS에서 더 나은 성과
(PF 1.387)를 보여, 향후 별도 미션으로 `long-short-account-ratio-contrarian-swing.md`를 정식
(스펙 전체 규칙·강건성 스위트 포함) 백테스트할 가치가 있음을 시사한다 -- 단, 이번 결과만으로
그 전략을 PASS 판정하지는 않는다.

## 사용 원천 데이터
- `sum_toptrader_long_short_ratio`/`count_long_short_ratio` 5분 metrics: 7종목,
  2022-01~2026-07 (2022년 결측 구간 있음, 위 1절 참조).
- 15m OHLCV vendor 캐시(4h 리샘플), funding 캐시(컨트래리언 비교용).

## backtest-reviewer 검증: VALID (FAIL 판정 동의, 서술 정정 2건 반영)
- **전 수치 독립 재실행 재현**: 심볼별 IS/OOS PF·n·pooled PF·top10제거·LOSO·파라미터스윕 14종·
  방향반전, 컨트래리언 IS/OOS/top10/신호상관(29/0/602/3646) 전부 오차 없이 완전 일치.
- **레버리지캡**: 608건 사이징 전수 계측 결과 10x 캡 미바인딩 0건 재확인.
- **tz 버그 수정 유효성**: reindex 후 top_ratio 7,944/9,852(81%) non-null 직접 계산으로 확인
  (전량 NaN 사고 재발 아님). 단 수정 전 코드는 미커밋이라 diff 대조는 불가(이 부분만 미확인).
- **룩어헤드 없음**: MA크로스 rolling(과거+현재봉만), `long_signal[i-1]`→봉 i 시가 체결 확인.
  4h 리샘플이 OHLCV와 동일 label/closed=left 규약이라 정렬 이슈 없음.
- **2022년 결측 "바이낸스 원본 공백" 주장 검증**: BTC 6개 날짜 원본 CSV 직접 재다운로드해
  일부 결측·일부 정상 혼재 확인, 다운로드 로그 99.8%+ 성공률로 "우리 쪽 다운로드 실패 아님" 뒷받침.
- **정정 1 — "신호 생성 불가" 표현 과장**: 실제로는 2022-05-31~2023-01-12 구간에도 34건 거래
  생성됨(87% 결측이지 100%가 아님, PF 0.71). 이를 제외한 것이 pooled PF를 1.026→1.044로
  소폭 유리하게 만듦 — 판정(1.3 문턱 대비 큰 미달)은 불변이나 "생성 불가"는 과장된 표현.
- **정정 2 — 컨트래리언 비교의 IS 시작일 부적절 상속**: 컨트래리언이 쓰는
  `count_long_short_ratio`는 2022년 결측률 5.1%에 불과(사실상 정상)한데, 모멘텀 전략용
  결측 컷오프(2023-01-13)를 근거 없이 그대로 재사용해 ~11개월치 사용 가능 데이터를 배제함.
  컨트래리언은 이미 "PASS 단정 안 함"으로 유보돼 있어 verdict에는 영향 없음.
- **부가 확인**: 컨트래리언 숏필터가 스펙(펀딩 상승 조건)보다 느슨함을 발견, strict 버전 재실행
  시 OOS PF 1.387→1.339(IS는 여전히 1.068 미달) — 결론 불변. 컬럼 상관계수(0.20/0.97)는
  BTC 기준값이며 ETH·SOL은 다르나(0.51/0.34) "별개 신호"라는 핵심 결론은 3종목 모두 유지.
- **권고**: 컨트래리언을 정식 검증할 경우 2022년 데이터(5% 결측, 사용 가능)를 포함한 IS 구간
  재설정 권고.
