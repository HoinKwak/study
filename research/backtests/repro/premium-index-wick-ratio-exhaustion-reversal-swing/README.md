# 프리미엄인덱스 캔들 꼬리비율(Wick Ratio) 소진 반전 — 재현 스크립트

스펙: `research/strategies/premium-index-wick-ratio-exhaustion-reversal-swing.md`
리포트: `research/backtests/premium-index-wick-ratio-exhaustion-reversal-swing.md`

## 실행 순서

```bash
cd research/backtests/repro/premium-index-wick-ratio-exhaustion-reversal-swing
python3 download.py          # data.binance.vision 월간 덤프 수집(klines 4h/1d, premiumIndexKlines 4h)
python3 diag_corr.py         # 최우선: 동어반복 점검(가격꼬리비율/z-score/실현변동성 상관)
python3 diag_freq.py         # 신호빈도 실측 + 8h 정산 오프셋 분포(폐기조건 e)
python3 analyze.py           # base/무비용/게이트대조군/스윕/de-clustering/반전/LOO/top-N/종목상관/매크로클러스터
python3 bootstrap.py         # 게이트 부트스트랩(100회) + base⊆pool 독립검정 + 셔플대조군(100회)
python3 lookahead_audit.py   # 절단 재현 테스트(BTC/ETH/ADA/XRP)
```

## 파일
- `common.py` — 데이터 로딩(ms→ns 명시 통일), wick_asym/ATR/EMA20 계산, PF(R)/t 유틸.
- `engine.py` — 신호 탐지(consec_upper/lower + premium 부호 + 1d EMA20 이격) + 4h 바 시뮬레이션
  (챈들리어 트레일링 SL + 프리미엄 제로크로스 익절 + 시간청산). 반전 대조군은 `reverse=True`.
- `diag_corr.py` — wick_asym(프리미엄) vs ①z-score ②실현변동성 ③가격 캔들 꼬리비율, 전체구간+
  트리거시점 한정 양쪽, `pandas.corr()` 사용.
- `diag_freq.py` — wick_asym 나이브 발생률, 8h 정산 오프셋별 분포, 결합조건 실측 빈도.
- `analyze.py` — 본 분석(①~⑨, 상세는 리포트 참조).
- `bootstrap.py` — 게이트 대조군 표본수맞춘 부트스트랩 100회 + 독립 Welch, 셔플 대조군 100회.
- `lookahead_audit.py` — 절단 재현.
- `data/` — 원천 parquet 캐시(gitignore, `*.parquet` 전역 제외).

## 데이터 소스
`https://data.binance.vision/data/futures/um/monthly/{klines,premiumIndexKlines}/<SYM>/<TF>/...zip`
(fapi 451 지역차단 우회). 2022-01~2026-06 월간 덤프. 2022년 zip 은 헤더 없음(COLS 수동 지정),
2024년 이후는 헤더 있음 — `download.py`가 첫 줄로 자동판별.

## 비용/판정 기준
왕복 0.14%(`ROUND_TRIP_COST`), 리스크 1%(R-배수 = pnl/risk_distance), IS 2022-01-01~2024-06-30
23:59:59 / OOS 2024-07-01~2026-06-30 23:59:59. PASS: OOS PF(R)>=1.3 AND t>=1.96 AND 강건성.
