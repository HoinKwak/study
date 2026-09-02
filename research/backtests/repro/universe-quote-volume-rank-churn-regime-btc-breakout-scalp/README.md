# 재현 안내 — 유니버스 거래대금 순위 리셔플 강도(Rank Churn) 레짐 게이트 + BTC 15m Donchian 브레이크아웃

스펙: `research/strategies/universe-quote-volume-rank-churn-regime-btc-breakout-scalp.md`
리포트: `research/backtests/universe-quote-volume-rank-churn-regime-btc-breakout-scalp.md`

## 데이터 준비
1. `dl_klines.sh` — 1h klines(7종목, rank_churn 계산용) + 15m klines(BTC만, 진입/청산용)
   monthly zip 다운로드(2022-01~2026-07). 스크립트 상단 `SP` 경로를 원하는 스크래치 디렉터리로
   바꾸고, 실행 전 `RANKCHURN_SCRATCH` 환경변수를 동일 경로로 export 한다.
2. `dl_ext_universe_diag.sh` — 보조 유니버스(28개 알트, n=35 진단/검증용) 1h klines 다운로드.
   n=7 프록시의 순위 이산성 문제(§본문 참고)를 진단하고, 실질적인 게이트 검증에 사용한다.

```bash
export RANKCHURN_SCRATCH=/path/to/scratch/rankchurn
export RANKCHURN_REPO_SRC=/path/to/study/src
bash dl_klines.sh
bash dl_ext_universe_diag.sh
```

## 실행
```bash
cd research/backtests/repro/universe-quote-volume-rank-churn-regime-btc-breakout-scalp
python3 diag_ext_universe.py    # n=7 vs n=35 rank_churn=0 빈도 비교(핵심 진단)
python3 run_lookahead_cut.py    # 룩어헤드 절단 테스트(1h 레짐 + 15m BTC 지표)
python3 run_main.py             # 메인 백테스트: n7/n35 × gated/ungated/reverse/random_gate/
                                 #   gate_top × IS/OOS/FULL. results_main.pkl 저장.
python3 run_gross.py            # 무비용(fee=0) 진단
python3 run_diag.py             # results_main.pkl 로드 — 게이트 대조군 부트스트랩·de-clustering·
                                 #   순열검정·top-N 제거(run_main.py 를 먼저 실행해야 함)
python3 run_correlation.py      # 동어반복 점검(전체구간 + 트리거 시점 한정 상관)
python3 run_sweep.py            # 파라미터 스윕(gate_pctile/pctile_window_days/donchian_period/
                                 #   body_atr_mult/atr_trail_mult)
```

## 원 실행 환경
- pandas 3.0.5, scipy 1.17.1
- 왕복비용 0.14%(테이커 0.05%×2 + 슬리피지 0.02%×2), 리스크 1%/트레이드,
  `RiskManager.build_plan_with_stop`
- IS 2022-01-01~2024-06-30 23:59:59 / OOS 2024-07-01~2026-06-30 23:59:59
- 매매 대상: BTCUSDT 단독(15m). 레짐 신호원(유니버스): n=7(스펙 지정 프록시, BTC/ETH/BNB/SOL/
  XRP/DOGE/ADA) / n=35(보조·진단용, 7종목+28개 완전커버리지 알트)

## 주요 발견(요약 — 상세는 리포트 참고)
- n=7 프록시에서는 `rank_churn` 이산성(약 39~55%가 정확히 0)으로 인해 스펙이 지정한
  `gate_pctile<=10`(범위 5~20 포함)가 사실상 전 구간에서 발화하지 않음(FULL 기간 gate<=10
  발화 0회). n=35 로 확장하면 gate<=10 발화율이 9.4%로 spec 기대치(~10%)에 정확히 부합 —
  이 문제가 데이터 부재가 아니라 n=7 통계량의 구조적 이산성 때문임을 확증.
- n=35(실질 검증)에서 gated 모드 OOS net PF(R)=0.507, t=-3.749(p=0.0002)로 유의하게 손실.
  게이트 없는 ungated 대조군(PF 0.605)·랜덤게이트·상위decile게이트 대조군과 부트스트랩으로
  통계적 구분 불가(오히려 근소하게 더 나쁨). 파라미터 스윕 13/13 변형 전부 OOS PF(R)<1,
  t<0(-1.75~-4.80). de-clustering(캘린더일·4일 롤링) 후에도 유의하게 손실.
