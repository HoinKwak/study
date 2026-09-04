# 재현 커맨드

스펙: `research/strategies/alt-btc-oi-growth-beta-divergence-rotation-swing.md`
리포트: `research/backtests/alt-btc-oi-growth-beta-divergence-rotation-swing.md`

```bash
export ALTOIBETA_SCRATCH=/tmp/<scratch>/altoibeta   # 임의 캐시 디렉터리
mkdir -p $ALTOIBETA_SCRATCH/data/klines1d $ALTOIBETA_SCRATCH/data/klines4h $ALTOIBETA_SCRATCH/data/metrics

# 1) 데이터 다운로드 (data.binance.vision futures/um monthly klines 1d/4h + daily metrics)
bash dl_klines.sh     # BTC+6알트 × {1d,4h} × 2022-01~2026-06 monthly zip
bash dl_metrics.sh    # 6알트(ETH/BNB/SOL/XRP/DOGE/ADA) × 일별 metrics zip(2022-01-01~2026-06-30)

# 2) 메인 백테스트(채택안, IS/OOS 요약)
python3 run_main.py

# 3) 필수 진단 일괄(gross · de-clustering · 종목간 상관(연간+꼬리) · 반전대조군 ·
#    베타무력화대조군 · 신호빈도대조 · 몸통/꼬리 분해)
python3 run_diagnostics.py

# 4) 파라미터 스윕(z_th/ema_period/atr_sl_mult/rr_target/max_hold/window) + LOO
python3 run_sweep.py
```

`ALTOIBETA_SCRATCH` 미지정 시 `common.py` 기본값(세션 스크래치패드 하위 `altoibeta/`)을 쓴다.
`ALTOIBETA_REPO_SRC` 로 `src/` 경로를 재정의할 수 있다(기본: 이 파일 기준 상위 4단계의 `src/`).

## 데이터 검증 메모
- klines1d/4h: 7종목 × 2TF × 54개월 = 756개 파일 전량 200 OK(미스 0건, `klines_missing.log` 없음).
- metrics: 6알트 × 1,642일(2022-01-01~2026-06-30) = 9,852개 파일 전량 200 OK(미스 0건).
