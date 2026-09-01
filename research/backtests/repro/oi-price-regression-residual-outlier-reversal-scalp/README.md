# 재현 안내 — OI-가격 회귀잔차 아웃라이어 반전 (스캘프)

스펙: `research/strategies/oi-price-regression-residual-outlier-reversal-scalp.md`
리포트: `research/backtests/oi-price-regression-residual-outlier-reversal-scalp.md`

## 데이터 준비
1. `dl_klines_1h.sh` — 1h klines monthly zip (7종목, 2022-01~2026-06) 다운로드.
2. `dl_metrics.sh` — metrics 일별 zip (7종목 × 2022-01-01~2026-06-30) 다운로드.
   이번 라운드는 실제로는 **klines_1h 는 이전 라운드(`oipath_data/klines_1h`)의 monthly zip 캐시를
   재추출**했고, **metrics 는 이전 라운드(`oiskew/data/metrics`)가 이미 추출해둔 CSV 를 읽기전용
   재사용**했다(동일 필드·동일 기간·동일 유니버스 — 재다운로드 시간 절약, "캐시 재사용 타당성"
   선례에 부합). 캐시가 없는 환경에서는 아래처럼 새로 받는다:

```bash
export OIRESID_SCRATCH=/path/to/scratch/oiresid
export OIRESID_REPO_SRC=/path/to/study/src
export OIRESID_METRICS_DIR=/path/to/scratch/oiresid/data/metrics   # 자체 다운로드 시
mkdir -p "$OIRESID_SCRATCH"/data/{klines,metrics}
bash dl_klines_1h.sh
bash dl_metrics.sh
```

## 실행
```bash
cd research/backtests/repro/oi-price-regression-residual-outlier-reversal-scalp
python3 run_main.py            # 신호구축 + signal_source(resid/oi_zscore) x dir_mode(A/B) x fee_on(net/gross)
                                # sigs.pkl, results_main.pkl 저장
python3 run_correlation.py     # ⚠️최우선 진단: 잔차z vs OI순수z 상관(전체구간 + 트리거시점 한정) — 동어반복 점검
python3 run_diagnostics.py     # (d)(b) 폐기조건 + de-clustering(캘린더일/3~5일롤링) + LOO + top-N + 부호셔플100회
python3 run_sweep.py           # 파라미터 스윕(window/z_th/price_filter/atr_tp_mult/atr_sl_mult/time_exit_bars)
python3 run_symbol_corr.py     # 종목간 동시발화 + 위기구간(2024-08/2025-02/2025-10) 집중도
```

룩어헤드 절단 테스트(BTC, 2023-06-01 절단 후 이전 구간 z_resid 완전판과 bit 단위 대조)는
리포트에 인라인 스니펫으로 남김(별도 스크립트로 분리하지 않음, 소규모라 README 재현 커맨드로 충분).

## 원 실행 환경
- pandas(버전은 `python3 -c "import pandas; print(pandas.__version__)"`로 확인), scipy
- 왕복비용 0.14%(테이커 0.05%×2 + 슬리피지 0.02%×2), 리스크 1%/트레이드,
  `RiskManager.build_plan_with_stop`
- IS 2022-01-01~2024-06-30 23:59:59 / OOS 2024-07-01~2026-06-30 23:59:59
- 시드: 셔플·부트스트랩은 `numpy.random.default_rng(<정수>)` 고정 시드 사용
  (파이썬 내장 `hash(str)` 미사용 — `PYTHONHASHSEED` 비고정 재현성 함정 회피)

## 자체 발견 데이터 결함(수정 반영)
- `sum_open_interest` 가 간헐적으로 0(음수 아님, 정확히 0.0) placeholder 로 찍히는 시점이 존재한다
  (BTC 기준 **463개** 5분봉 — 초판 42개는 과소 카운트였고 리뷰어 실측으로 정정. 예시 날짜: 2022-03-07~08·2023-11-23·2023-11-26·**2024-07-09~15**[이전 라운드가
  다른 metrics 필드에서 이미 보고한 것과 동일 구간]·2025-04-11·2025-04-15·2025-07-21). `isna()` 로는
  못 잡히므로(값이 NaN 이 아니라 0.0) `common.load_metrics_5m` 에서 `<=0` 값을 명시적으로 NaN
  처리한 뒤 1h 리샘플·ffill 한다. 이 처리 없이는 다음 유효값에서 ΔOI% 가 -100%→+inf 로 폭주해
  회귀·z-score 전체가 오염된다.
