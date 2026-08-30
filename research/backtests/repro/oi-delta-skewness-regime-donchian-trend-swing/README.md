# 재현 안내 — ΔOI 왜도 레짐 게이트 + Donchian 추세추종 (스윙)

스펙: `research/strategies/oi-delta-skewness-regime-donchian-trend-swing.md`
리포트: `research/backtests/oi-delta-skewness-regime-donchian-trend-swing.md`

## 데이터 준비
1. `dl_klines.sh` — 4h klines monthly zip (7종목, 2022-01~2026-07) 다운로드.
2. `dl_metrics.sh` — metrics 일별 zip (7종목 × 2022-01-01~2026-06-30, 약 11,494 파일) 다운로드.
   둘 다 스크립트 상단 `SP` 경로를 원하는 스크래치 디렉터리로 바꾸고, 실행 전 환경변수
   `OISKEW_SCRATCH` 를 동일 경로로 export 한다(기본값은 원 실행 시 사용한 scratchpad 경로).

```bash
export OISKEW_SCRATCH=/path/to/scratch/oiskew
export OISKEW_REPO_SRC=/path/to/study/src
mkdir -p "$OISKEW_SCRATCH"/data/{klines,metrics}
bash dl_klines.sh
bash dl_metrics.sh
```

## 실행
```bash
cd research/backtests/repro/oi-delta-skewness-regime-donchian-trend-swing
python3 check_data_quality.py       # OI 데이터 결측률 확인
python3 run_lookahead_cut.py        # 룩어헤드 절단 테스트(BTC/ETH/XRP)
python3 run_main.py                 # 메인 백테스트: gated/ungated/reverse × IS/OOS/FULL, sigs.pkl·results_main.pkl 저장
python3 run_sweep.py                # 파라미터 스윕(doi_window/pctile_window/pctile_th/donchian_period)
python3 run_correlation.py          # 종목 간 신호 상관(평시·위기국면)
```

de-clustering·매크로 클러스터 분해·LOO·top-N·부트스트랩(matched-N/독립 잔여표본) 등 나머지
진단은 `results_main.pkl` 을 로드해 대화형으로 수행(리포트의 각 절에 인라인 스니펫으로 남김,
`stats_utils.py` 의 `decluster_calendar_day` / `decluster_rolling_days` /
`bootstrap_matched_n_diff` 등을 사용).

## 원 실행 환경
- pandas 3.0.5, scipy 1.17.1
- 왕복비용 0.14%(테이커 0.05%×2 + 슬리피지 0.02%×2), 리스크 1%/트레이드, `RiskManager.build_plan_with_stop`
- IS 2022-01-01~2024-06-30 23:59:59 / OOS 2024-07-01~2026-06-30 23:59:59
