# 재현 절차 — 1시간 가격충격 후 OI 원상복귀 속도 분기(되돌림 vs 지속) 스캘프

스펙: `research/strategies/post-shock-oi-reversion-velocity-branch-scalp.md`
리포트: `research/backtests/post-shock-oi-reversion-velocity-branch-scalp.md`

## 0. 환경변수
```bash
export PSHOCK_REPO_SRC=<repo>/src
export PSHOCK_SCRATCH=<임의 스크래치 경로>   # 기본값: 세션 scratchpad/pshock
```

## 1. 데이터 다운로드 (원본 zip/csv는 이 저장소에 커밋하지 않음, `$PSHOCK_SCRATCH/data/` 에만 저장)
```bash
bash dl_klines.sh 1h    # futures/um monthly klines, 1h, 7종목, 2022-01~2026-07
bash dl_klines.sh 15m   # 동일, 15m
bash dl_metrics.sh      # futures/um daily metrics(OI), 7종목, 2022-01-01~2026-06-30
```
이번 라운드에서는 동일 유니버스·기간의 `metrics` 캐시가 이미 다른 백테스트 스크래치
(`oibv/data/metrics`)에 존재해 심볼릭 링크로 재사용했다(11,492개 파일, 종목당 1641~1642일
전량 존재 확인). klines(1h·15m)는 신규 다운로드(385파일=7종목×55개월, 결측 0건).

## 2. 메인 실행 (IS/OOS/FULL, net+gross, 분기별)
```bash
python3 run_main.py
```

## 3. 필수 진단
```bash
python3 run_metrics_alignment_check.py   # metrics create_time 정시정렬(지터) 실측
python3 run_background_dist.py           # 폐기조건(a) 배경분포 비교
python3 run_immediate.py                 # 폐기조건(b) 즉시진입 대조군
python3 run_tautology.py                 # 동어반복 점검(상관)
python3 run_reverse.py                   # 반전 대조군
python3 run_declustering.py              # 캘린더일 + 3~5일 롤링 de-clustering(net+gross)
python3 run_loo_topn.py                  # LOO 7종목 + top-N/worst-N 제거
python3 run_shuffle.py                   # 부호무작위화/승률고정 순열 100회 + 종목간 상관
python3 run_sweep.py                     # 파라미터 스윕 21변형
python3 run_lookahead_cut.py             # 룩어헤드 임의절단 재실행(3종목 bit단위 대조)
```

## 코드 구조
- `common.py` — 데이터 로더(klines 1h/15m, metrics 5m→1h OI 리샘플), 심볼별 지표(ATR14 1h/15m,
  EMA20 15m). IS/OOS 경계·수수료 상수.
- `engine.py` — 신호탐지(`detect_events`/`detect_all_shocks`/`detect_raw_shocks`), 15m 체결
  시뮬레이션(`simulate_symbol`/`simulate_immediate`), 반전모드(`Config.reverse`).
- `stats_utils.py` — PF(R)/t검정/de-clustering/부트스트랩.

## 자체 발견 버그(수정됨, 리포트에도 기재)
1. `simulate_immediate`의 persistence/reversion 프레임 방향 매핑이 최초 구현에서 뒤바뀌어 있었음
   (수정 전: persistence 프레임이 실제로는 반전방향을 진입, 그 결과 EMA20 확인필터와 충돌해 표본이
   4건으로 붕괴). `detect_events`의 원 방향 규칙과 대조해 수정.
2. 반전 대조군에서 EMA20 확인 게이트를 `final_direction`(반전 후 방향) 기준으로 걸면 표본이 0건으로
   전멸함(충격 직후 EMA20이 충격 자신의 모멘텀 방향으로 기울어 있을 확률이 구조적으로 높기 때문).
   게이트는 `orig_direction`(원신호, "이 신호가 애초에 유효한가") 기준으로 유지하고 SL/TP·청산조건만
   `final_direction`(최종 체결방향) 기준으로 뒤집도록 수정.
