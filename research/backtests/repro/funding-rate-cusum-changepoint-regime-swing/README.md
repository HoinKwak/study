# 재현 스크립트 — 펀딩레이트 CUSUM 체인지포인트 레짐전환 추세추종

원본 스펙: `research/strategies/funding-rate-cusum-changepoint-regime-swing.md`
결과 리포트: `research/backtests/funding-rate-cusum-changepoint-regime-swing.md`

## 실행 순서
```bash
cd research/backtests/repro/funding-rate-cusum-changepoint-regime-swing
python3 download.py          # data/ 에 7종목 × (fundingRate, 4h klines) parquet 캐시(gitignore, 미포함)
python3 analyze.py           # 기본변형 IS/OOS/FULL + gross/net + 반전·게이트없음 대조군 → out_summary.json
python3 diag_freq.py         # 빈도 실측(스펙 예상 대비) → out_diag_freq.json
python3 diag_tautology.py    # CUSUM z vs streak/curvature 상관(전체·트리거시점) → out_diag_tautology.json
python3 diag_declus.py       # 캘린더일 + 3/5일 롤링 de-clustering(gross·net) → out_diag_declus.json
python3 diag_robust.py       # LOO·top-N 제거·파라미터 스윕 13변형·셔플100회 → out_diag_robust.json
python3 diag_corr.py         # 종목간 신호상관(평균·위기국면) → out_diag_corr.json
python3 diag_lookahead.py    # 3종목 절단 재실행 bit단위 대조 → out_diag_lookahead.json
python3 diag_bootstrap.py    # base vs reverse/nogate 표본수맞춤 부트스트랩 → out_diag_bootstrap.json
```

## 파일 구성
- `download.py` — data.binance.vision 월간 덤프(fundingRate, 4h klines) 수집.
- `common.py` — 로딩·EMA/ATR·PF(R)/t-stat 유틸.
- `events.py` — CUSUM(양방향, k=0.5, h=4.0) 체인지포인트 검출. baseline은 `funding_interval_hours==8`
  구간만 필터링한 뒤 shift(1)된 롤링 60정산 평균/표준편차로 표준화(자기 자신을 베이스라인에
  포함하지 않음 — 룩어헤드 방지 겸 통상적 체인지포인트 관행).
- `engine.py` — EMA20/60 방향게이트 → 다음 4h봉 시가 진입 → ATR 트레일링(래칫, 3.0×ATR) +
  고정 SL(1.5×ATR) + 반대 체인지포인트 무효화(원신호 기준) + 45봉 시간청산. R-배수 산출.
- `analyze.py`, `diag_*.py` — 진단 스크립트 일체.

## 데이터
원본 zip/parquet 캐시는 `data/`(gitignore)에 내려받으며 저장소에 포함하지 않는다.
