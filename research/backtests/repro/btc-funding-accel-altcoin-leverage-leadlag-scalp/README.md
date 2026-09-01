# 재현 방법

```bash
# 1) 데이터 다운로드(BTC fundingRate + 7종목 15m/1h klines, 2022-01~2026-06)
bash dl.sh

# 2) 1차 진단(트리거/confirm 결합확률)
BFLL_REPO_SRC=/home/user/study/src python3 diag_freq.py

# 3) 메인 백테스트(채택안: accel_z=1.5, confirm_window=8h) + gross 진단
BFLL_REPO_SRC=/home/user/study/src python3 run_main.py

# 4) 2차 진단: de-clustering/no-gate 대조군/pooled 대조군/반전 대조군/LOO/top-N/worst-N/5일블록
BFLL_REPO_SRC=/home/user/study/src python3 run_diagnostics.py

# 5) 파라미터 민감도 스윕(accel_z, confirm_window, atr_trail_mult, donchian_lookback)
BFLL_REPO_SRC=/home/user/study/src python3 run_sweep.py

# 6) 룩어헤드 절단 재실행 검증
BFLL_REPO_SRC=/home/user/study/src python3 run_lookahead_check.py
```

데이터 캐시 위치: `BFLL_SCRATCH` 환경변수(기본값은 common.py 참조, scratchpad 하위
`btcfundleadlag/data/{klines15m,klines1h,funding}`).

## 파일
- `common.py` — klines/fundingRate 로더, 가속 이벤트 탐지, 알트 Donchian/ATR 시그널
- `engine.py` — 2단계 트리거→confirm→진입→청산 시뮬레이션 엔진(gate/no-gate/reverse 지원)
- `stats_utils.py` — PF(R)/t검정/부트스트랩/de-clustering 유틸(hashlib 결정적 시드)
- `run_main.py` — 채택안 메인 백테스트(IS/OOS/FULL, net/gross)
- `run_diagnostics.py` — de-clustering, 대조군 3종(no-gate/pooled/reverse), LOO, top-N/worst-N, 5일블록
- `run_sweep.py` — 파라미터 스윕 14변형
- `run_lookahead_check.py` — 데이터 절단 재실행 룩어헤드 검증(960/960 bit 단위 일치 확인됨)
