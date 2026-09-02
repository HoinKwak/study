# 펀딩정산 프리미엄인덱스 곡률(2차회귀) 페이드 스캘프 — 재현 스크립트

스펙: `research/strategies/funding-settlement-premium-curvature-fade-scalp.md`
리포트: `research/backtests/funding-settlement-premium-curvature-fade-scalp.md`

## 실행 순서

```bash
cd research/backtests/repro/funding-settlement-premium-curvature-fade-scalp
python3 download.py          # data.binance.vision 월간 덤프 수집(premiumIndexKlines 1m, klines 15m)
python3 events.py            # 자체검증: 2차회귀 곡률계수 벡터화가 np.polyfit(deg=2)와 일치하는지
python3 diag_corr.py         # ⚠️최우선: 동어반복 점검(곡률 c/c_z vs EMA기울기/스퀴즈range, 전체+트리거시점)
python3 diag_freq.py         # 신호빈도 실측(스펙 [추정] 연 50건/심볼과 비교)
python3 lookahead_audit.py   # 절단 재현 테스트(BTC)
python3 analyze.py           # base/무비용/앵커이동대조군/스윕/de-clustering/반전/LOO/top-N/종목상관/순열검정
```

## 파일
- `common.py` — 데이터 로딩(ms→ns 명시 통일), ATR(14,15m), PF(R)/t/승률 유틸, IS/OOS 분할.
- `events.py` — 정산이벤트(8h 윈도우) 구성 + 2차 OLS 곡률계수 c 벡터화 계산(고정 τ그리드 가중치
  1회 계산 후 내적) + causal c_z(과거 60회 정산주기, shift(1)).
- `engine.py` — 진입(정산시각 15m봉 시가, shift(1)) + 청산(SL/1.3R TP 인트라바 우선, 프리미엄
  체크포인트수준 복귀, 8봉 시간청산) 시뮬레이션. 반전 대조군은 `reverse=True`.
- `diag_corr.py` — c/c_z vs 경쟁지표(EMA20 15m 모멘텀기울기, 정산전30분 프리미엄range) 상관,
  전체구간+트리거시점 한정 양쪽, `pandas.corr()` 사용.
- `diag_freq.py` — 종목별 신호빈도 실측.
- `analyze.py` — 본 분석(①~⑨, 상세는 리포트 참조).
- `lookahead_audit.py` — 절단 재현.
- `data/` — 원천 parquet 캐시(gitignore).

## 데이터 소스
`https://data.binance.vision/data/futures/um/monthly/{klines,premiumIndexKlines}/<SYM>/<TF>/...zip`
(fapi 451 지역차단 우회). premiumIndexKlines 1m + klines 15m, 2022-01~2026-06 월간 덤프.
2022년 zip 은 헤더 없음(COLS 수동 지정), 2024년 이후는 헤더 있음 — `download.py`가 자동판별.

## 비용/판정 기준
왕복 0.14%(`ROUND_TRIP_COST`), 리스크 1%(R-배수 = pnl/risk_distance), IS 2022-01-01~2024-06-30
23:59:59 / OOS 2024-07-01~2026-06-30 23:59:59. PASS: OOS PF(R)>=1.3 AND t>=1.96 AND 강건성.
