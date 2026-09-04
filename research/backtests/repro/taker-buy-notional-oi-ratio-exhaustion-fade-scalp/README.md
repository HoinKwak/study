# 재현 안내 — 테이커 매수체결대금/OI명목가치 순간비율 극단 소진 반전 스캘프

스펙: `research/strategies/taker-buy-notional-oi-ratio-exhaustion-fade-scalp.md`
리포트: `research/backtests/taker-buy-notional-oi-ratio-exhaustion-fade-scalp.md`

## 데이터 준비
15m·1h klines(monthly zip, 2022-01~2026-06) + metrics 5분(일별 zip, 2022-01-01~2026-06-30).
동일 세션에서 동시 실행 중이던 다른 백테스터(oivolratio)가 이미 받아둔 동일 7종목·동일 기간의
**불변 과거 원자료를 읽기 전용으로 복사**해 재사용했다(쓰기 없음, 재다운로드 시간 절약).

```bash
export TBOI_SCRATCH=/path/to/scratch/tbnoifade
export TBOI_REPO_SRC=/path/to/study/src
mkdir -p "$TBOI_SCRATCH"/data/{klines_15m,klines_1h,metrics}
# klines: https://data.binance.vision/data/futures/um/monthly/klines/<SYM>/<15m|1h>/<SYM>-<TF>-YYYY-MM.zip
# metrics: https://data.binance.vision/data/futures/um/daily/metrics/<SYM>/<SYM>-metrics-YYYY-MM-DD.zip
# (7종목 x 54개월 x 2TF klines + 7종목 x ~1,642일 metrics)
```

## 실행
```bash
cd research/backtests/repro/taker-buy-notional-oi-ratio-exhaustion-fade-scalp
python3 build_sigs.py 200          # 신호 구축(z_window=200) → sigs_200.pkl
python3 run_freq_check.py          # 최우선 검증: 개별/결합 조건 발생률 vs 독립기대
python3 run_correlation.py         # 동어반복 점검 + 종목간 신호상관(평시/위기국면)
python3 run_main.py                # 메인 백테스트(reverse x fee_on 4조합) → results_main.pkl
python3 run_diagnostics.py         # de-clustering(캘린더일+3~5일롤링,net+gross)/LOO/top-N/셔플
python3 run_controls12.py          # 핵심 대조군①②(분자=총거래대금 / 분모=24h거래대금)
python3 run_control3_overlap.py    # 대조군③: taker-aggressor-price-premium-absorption 중복률
python3 run_sweep.py               # 파라미터 스윕(26변형, z_window 포함)
python3 run_lookahead_check.py     # 룩어헤드 점검(BTC/XRP 절단 재실행)
python3 run_sanity.py              # 회계정합·IS+OOS==FULL·0-fill 점검·반전 청산분포
```

## 원 실행 환경
- pandas 3.0.5, numpy 2.4.6, scipy 1.17.1.
- 왕복비용 0.14%(테이커 0.05%×2 + 슬리피지 0.02%×2), 리스크 1%/트레이드,
  `RiskManager.build_plan_with_stop`, `leverage_for`(major=30x/alt=10x).
- IS 2022-01-01~2024-06-30 23:59:59 / OOS 2024-07-01~2026-06-30 23:59:59(양쪽 상한 명시 적용).
- 시드: 부호 무작위화 `seed=123`(100회), 부트스트랩 `seed=42/7`(5,000회).

## 자체 발견 버그(수정 반영, 리포트 §11 참조)
`engine.py` 최초 구현이 `trade.pnl = raw - fee1`(청산 수수료만)로 진입 수수료 `fee0`를
개별 트레이드 손익에서 누락하고 있었다(계좌 `equity` 경로는 정확했으나 R-배수 진단 필드가
근소하게 낙관적이었음). `raw_pnl - fees == pnl` 회계정합 점검(`run_sanity.py`)에서
max|diff|=117.98로 적발해 `pnl = raw - fee0 - fee1`로 수정, 전체 재실행. 수정 후 OOS net
PF(R) 0.463→0.341로 오히려 악화(FAIL 결론 불변, 본 리포트는 전부 수정 후 수치).

## 신호↔체결 타임프레임 매핑 및 반전 대조군 설계값
`engine.py` 상단 docstring 및 리포트 §1 참조 — 스펙 문면이 정확한 SL/TP/트레일 결합 방식·
"1h EMA20 뚜렷한 반대"의 정량 임계치를 명시하지 않아 확정한 [설계값] 전부 기재.
