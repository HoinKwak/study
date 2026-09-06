# 재현 스크립트 — 펀딩비율 변화량(ΔFunding) 근사엔트로피(ApEn) 레짐 게이트 + BTC 추세추종

원본 스펙: `research/strategies/funding-delta-approximate-entropy-regime-swing.md`
결과 리포트: `research/backtests/funding-delta-approximate-entropy-regime-swing.md`

## 실행 순서
```bash
cd research/backtests/repro/funding-delta-approximate-entropy-regime-swing
python3 download.py          # data/BTCUSDT_fundingRate.parquet (2021-09~2026-06, gitignore)
# data/klines_4h/*.csv 는 oi-price-sign-agreement-rate-regime-gate-trend-swing 백테스트가
# 이미 받아둔 7종목 4h klines 캐시(2021-01/10~2026-06)를 그대로 복사해 재사용(동일 유니버스·기간).
python3 apen.py              # ApEn 소표본 손계산 대조(2건) + 독립 브루트포스 구현 교차검증
python3 analyze.py           # 기본안 IS/OOS/FULL, 거래단위+캘린더일+5일롤링 PF/t(gross·net) → out_analyze.json
python3 diag_tautology.py    # ApEn vs ADX/EMA괴리율/RV20/펀딩절대수준/펀딩변화stdev/CUSUM 상관(전체+트리거시점) → out_diag_tautology.json
python3 diag_declus.py       # 캘린더일+3/5일롤링 de-clustering(gross·net) → out_diag_declus.json
python3 diag_macro.py        # 5일 클러스터 top-1/2/3/5 순익 기여도·제거시 잔여성과 → out_diag_macro.json
python3 diag_reverse.py      # 반전 대조군(대칭 SL, 레짐붕괴청산은 방향무관 스칼라) + 신호중첩률 → out_diag_reverse.json
python3 diag_bootstrap.py    # base vs no-gate(사전폐기(e))·ADX게이트(사전폐기(b)) 부트스트랩 → out_diag_bootstrap.json
python3 diag_sweep.py        # 핵심 파라미터 8변형 스윕(트레이드단위+5일롤링+top3비중) → out_diag_sweep.json
python3 diag_shuffle.py      # 부호 무작위화(나이브 50/50) + 승률고정 대안검정 → out_diag_shuffle.json
python3 diag_tailcorr.py     # 종목간 진입일 상관 — 평시 vs BTC 절대수익률 상위5% 위기국면 → out_diag_tailcorr.json
python3 diag_lookahead.py    # BTC·ETH 2종목 절단(2025-01-01) 재실행, 절단이전 신호 완전일치 확인 → out_diag_lookahead.json
```
LOO(종목별 제외) 결과는 일회성 인라인 스크립트로 생성해 `out_diag_loo.json`에 저장(코드는
리포트 §5.6에 인용, 짧아서 별도 .py 파일로 분리하지 않음 — 재현 시 해당 스니펫을 그대로
실행하면 동일 결과가 나온다).

## 파일 구성
- `download.py` — BTC `fundingRate` 월간 덤프(2021-09~2026-06) 수집(UM, `interval_hours==8` 정상
  정산만 필터링).
- `apen.py` — Pincus(1991) 근사엔트로피 원 정의 그대로 구현(`_phi`, `apen`) + 완전 독립
  중첩루프 참조구현(`apen_ref_naive`) + 트레일링 롤링(`rolling_apen`) + 90일 백분위(`apen_pctile_series`,
  bisect 기반 O(N log N), `rolling().rank(pct=True)`의 min_periods 함정 회피).
- `common.py` — 로딩(2021년분 헤더없는 월간 CSV 자동판별 포함)·EMA/ATR/ADX·PF(R)/t-stat 유틸.
- `signals.py` — BTC ΔFunding→ApEn→백분위, BTC EMA20/50/ADX/RV20/EMA괴리율, settlement→bar
  backward-asof 매핑.
- `events.py` — 7종목 프레임 구성(`build_universe`) + 종목별 진입신호(`detect_signals`,
  저ApEn게이트 AND BTC EMA20/50방향 AND 자기 EMA20 눌림목재진입).
- `engine.py` — bar i(닫힌 데이터) 신호 → bar i+1 시가 진입(shift(1)) → ATR트레일링(2.5)+
  고정SL(1.3×ATR)+레짐붕괴(apen_pctile>=85, 방향무관 스칼라)즉시청산+30봉 시간청산. R-배수.
- `diag_*.py` — 진단 스크립트 일체(위 실행순서 참조).

## 데이터
원본 parquet/CSV 캐시는 `data/`(gitignore)에 두며 저장소에 포함하지 않는다. `download.py`로
펀딩레이트는 재수신 가능하고, 4h klines는 `data.binance.vision` 월간 덤프에서 동일하게 받을 수
있다(다른 백테스트가 이미 받아둔 캐시를 재사용한 것뿐, 데이터 자체는 항상 재현 가능).
