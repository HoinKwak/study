# OI CUSUM 체인지포인트 레짐전환 추세추종 — 재현 스크립트

스펙: `research/strategies/oi-cusum-changepoint-regime-trend-swing.md`
리포트: `research/backtests/oi-cusum-changepoint-regime-trend-swing.md`

## 데이터
`OICUSUM_SCRATCH` 환경변수(기본값이 스크립트에 하드코딩돼 있음, 재현 시 변경 가능)의
`data/klines/<SYM>_4h.parquet`(월간 덤프) + `data/metrics/<SYM>-metrics-<date>.csv`(일별 덤프,
`sum_open_interest` 5분 간격). 원본 데이터는 대용량이라 git 에 커밋하지 않음(`research/.gitignore`
의 `impl/` 제외와 같은 구조적 이유 — 재현 시 아래 커맨드로 재다운로드).

## 재현 커맨드
```bash
cd research/backtests/repro/oi-cusum-changepoint-regime-trend-swing
export OICUSUM_SCRATCH=/path/to/scratch   # 선택, 기본값 사용 가능
python3 download.py           # 4h klines(월간) — 빠름
bash dl_metrics.sh            # 5분 metrics 일별 zip(병렬, 11,494개 파일 — 다소 오래 걸림)

python3 diag_direction.py     # §1단계: 방향 예단 없이 CP 후 N봉 수익률(게이트 없음)
python3 diag_freq.py          # §전제일관성: h·k·z_window 스윕 — 빈도 안정성
python3 analyze.py            # 메인: base·reverse·contrarian·대조군 4종 트레이드 생성+통계
python3 diag_tautology.py     # §동어반복: 가격CUSUM 중첩률 + OI파생지표 상관(전체+트리거시점)
python3 diag_corr.py          # §종목간 신호상관: 평시 vs 위기국면(BTC 상위5%)
python3 diag_declus.py        # §de-clustering: 캘린더일 + 3~5일 롤링
python3 diag_topn.py          # §클러스터 분해: top-N(최고제거)·worst-N(최악제거) 대칭
python3 diag_sweep.py         # §파라미터 스윕: (z,k,h) 36조합 + 청산파라미터 27조합 OOS PF/t
python3 diag_loo_year.py      # §LOO 대체(단일종목 진입): leave-one-year-out
python3 diag_lookahead.py     # §룩어헤드: BTC+ETH+XRP+ADA 절단검증
python3 diag_bootstrap.py     # §사전폐기조건(f): 게이트없음 대비 표본수맞춤 부트스트랩
```

## 모듈 구성
- `common.py` — 데이터 로더(klines/metrics), IS/OOS 경계, PF(R)/t-stat/승률 유틸.
- `cusum.py` — OI CUSUM 순차 계산(벡터화 불가, for-loop). `s_pos_pre`/`s_neg_pre`(리셋 전 값,
  트리거시점 강도 상관 진단용) 별도 보관.
- `signals.py` — 심볼별 신호세트(klines+OI+CUSUM+EMA20/50+ATR14).
- `events.py` — 원시 체인지포인트 목록(무효화·상관 진단용) + confirm_bars 이내 EMA 게이트
  통과 진입 후보.
- `engine.py` — 체결 시뮬레이션(ATR 트레일링 래칫+고정SL+반대CP 무효화+시간청산), R-배수 산출.
- `control.py` — 대조군 4종(게이트없음 EMA크로스·OI z스파이크·가격CUSUM·반전은 engine 파라미터).
- `analyze.py` — 메인 실행, `out_*.csv`/`out_summary.json` 산출.
- `diag_*.py` — 각 진단 스크립트(스펙 §요구사항별 1:1 대응).
