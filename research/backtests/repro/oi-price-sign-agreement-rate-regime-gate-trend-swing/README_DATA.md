# 데이터 재현 안내

이 백테스트는 BTC 단독(신호원·매매대상 모두 BTC)이며, 데이터는 아래 두 출처를 병합해 사용한다.

1. **oi-cross-sectional-herfindahl-concentration-breadth-btc-trend-swing** 백테스트가 이미 받아둔
   BTCUSDT 4h klines·5분 metrics 캐시(`research/backtests/repro/oi-cross-sectional-herfindahl-concentration-breadth-btc-trend-swing/dl_klines.sh`,
   `dl_metrics.sh` — 2021-10-01 ~ 2026-06-30)를 재사용했다. 기간·유니버스(BTCUSDT)·필드
   (open/high/low/close/volume, sum_open_interest)가 이 스펙의 요구와 정확히 일치해 재다운로드 없이
   그대로 썼다.
2. **`dl_extra.sh`·`dl_metrics_extra.sh`**(이 디렉터리) — 위 캐시가 2021-10-01부터만 있어 IS 시작일
   (2022-01-01)에 agree_pctile 의 365일 정규화 창을 온전히 채우기에 버퍼가 부족(92일)했으므로,
   2021-01-01~2021-09-30 BTCUSDT 4h klines·metrics 를 추가로 받아 만 1년 버퍼를 확보했다
   (실행 결과 두 스크립트 모두 MISS 0건).

재현 순서: 위 HHI 백테스트의 `dl_klines.sh`·`dl_metrics.sh`를 먼저 실행해 캐시를 만든 뒤,
이 디렉터리의 `dl_extra.sh`·`dl_metrics_extra.sh`를 실행해 2021년 버퍼를 보강하고,
`common.py`(`OISIGN_SCRATCH` 환경변수로 데이터 경로 지정) → `run_diagnostics.py` 순서로 실행한다.
