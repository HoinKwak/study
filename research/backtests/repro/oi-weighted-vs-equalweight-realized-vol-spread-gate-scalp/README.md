# OI가중 vs 등가중 실현변동성 스프레드 레짐 게이트 스캘프 — 재현 스크립트

스펙: `research/strategies/oi-weighted-vs-equalweight-realized-vol-spread-gate-scalp.md`
리포트: `research/backtests/oi-weighted-vs-equalweight-realized-vol-spread-gate-scalp.md`

## 데이터 소스(재현 전 준비)
- klines 1h/15m, metrics(5분 OI) 는 이 세션의 공용 스크래치패드 캐시를 읽기전용으로 재사용한다
  (경로는 `common.py` 상단 `KLINES_1H_CACHE`/`KLINES_15M_CACHE`/`METRICS_DIR` 참고). 캐시가 없는
  환경에서 재현하려면 `data.binance.vision`에서 아래를 직접 받아 동일 디렉터리 구조로 배치한다:
  - klines: `https://data.binance.vision/data/futures/um/monthly/klines/<SYM>/{15m,1h}/...zip`
  - metrics(OI): `https://data.binance.vision/data/futures/um/daily/metrics/<SYM>/...zip`
    (필요 컬럼: `create_time,symbol,sum_open_interest_value`)
  - 7종목: BTCUSDT·ETHUSDT·BNBUSDT·SOLUSDT·XRPUSDT·DOGEUSDT·ADAUSDT, 2022-01-01~2026-06-30.
- 환경변수로 경로 재지정 가능: `OIWEQ_SCRATCH`·`OIWEQ_KLINES_1H`·`OIWEQ_KLINES_15M`·`OIWEQ_METRICS_DIR`·
  `OIWEQ_REPO_SRC`.

## 실행 순서
```bash
cd research/backtests/repro/oi-weighted-vs-equalweight-realized-vol-spread-gate-scalp
python3 run_check1_btc_dominance.py   # 1단계: BTC OI비중·rv_ow vs BTC단독 상관(레벨/z, 전체/트리거시점)
python3 run_main.py                    # gated/ungated/btc_solo/ew_solo/reverse/random_gate × IS/OOS/FULL
                                        # -> results_main.pkl 생성(용량 커서 git 미추적, 재실행으로 재현)
python3 run_diag.py                    # 부트스트랩 대조군 비교·de-clustering·순열검정·top-N·청산분포
python3 run_mdd.py                     # R-배수 누적합 기준 MDD
python3 run_sweep.py                   # 파라미터 스윕 16변형
python3 run_loo.py                     # 게이트 유니버스 LOO(7종목)
python3 run_lookahead_cut.py           # 룩어헤드 절단 테스트(7종목 집계 + BTC 15m 지표)
python3 run_correlation.py             # 결합확률 실측·동어반복 점검·종목간 신호상관(평균/위기국면)
python3 run_data_quality.py            # create_time 지터·0-fill·2022 결측·병합 NaN 비율
```

## 참고
- `results_main.pkl` 은 약 19MB 라 git에 커밋하지 않는다(`run_main.py` 재실행으로 즉시 재생성).
- `common.py`/`gates.py`/`engine.py`/`stats_utils.py` 는
  `universe-quote-volume-rank-churn-regime-btc-breakout-scalp` 리포트의 검증된 패턴(merge_asof
  causal 정렬·ns 명시 통일·R-배수 Trade 데이터클래스·de-clustering/부트스트랩/순열검정 유틸)을
  그대로 재사용해 구현했다.
