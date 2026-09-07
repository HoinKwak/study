# 거래대금-OI 롤링 그레인저 인과방향 전환 레짐 — 재현 스크립트

스펙: `research/strategies/quote-volume-oi-rolling-granger-causality-regime-swing.md`
리포트: `research/backtests/quote-volume-oi-rolling-granger-causality-regime-swing.md`

## 데이터 준비
```bash
export GRQV_SCRATCH=/tmp/.../granger_oiqv   # 스크래치 디렉터리(임의 지정)
python3 download.py       # 4h klines(quote_volume 포함), 월간 덤프
bash dl_metrics.sh         # OI metrics 5분, 일별 덤프(병렬)
```

## 핵심 모듈
- `granger.py` — causal 롤링 양방향 그레인저 F-검정(정규방정식 직접 풀이, VAR(lag) OLS).
- `signals.py` — 심볼별 dqv/doi·p_qv2oi/p_oi2qv·regime·transition_qv·EMA20/50·ATR14.
- `events.py` — 문자 그대로의 스펙 전환 정의(직전봉 대비 oi_lead→qv_lead) + 방향 필터.
- `events_loose.py` — 보조 로버스트니스용 완화된 전환 정의(lookback 내 oi_lead 존재로 완화).
- `control.py` — 대조군(게이트없음 EMA크로스, 단순 z-score 게이트).
- `engine.py` — ATR SL(1.6)+트레일링(2.2)+레짐무효화청산+18봉 시간청산, R-배수.

## 실행
```bash
python3 diag_freq.py          # 1차 진단: lag×p_sig 3×3 전환빈도
python3 diag_freq_loose.py    # 완화 정의 lookback 3/5/10 빈도
python3 analyze.py            # base 파라미터 본체결 + 대조군 3종
python3 diag_sweep.py         # lag×p_sig 3×3 + loose 3종 전체 체결·PF/t
python3 diag_lookahead.py     # 절단검증(주신호+대조군 신호 전부)
python3 diag_tautology.py     # 거래량z·OI ROC 상관(전체구간+트리거시점)
python3 diag_declus.py        # de-clustering(캘린더일·3일·5일 롤링)
python3 diag_topn.py          # top/worst 클러스터 제거 + 종목간 상관
python3 diag_bootstrap.py     # 표본수맞춤 부트스트랩(base vs 대조군)
```

## 표본 규모 안내
base(gc_window=60,gc_lag=4,p_sig=0.05,p_insig=0.10) 문자 그대로의 전환 정의는 7종목·4.5년
전체에서 실행 가능한 트레이드가 **1건**뿐이다(OOS 0건). 대부분의 진단 스크립트 출력이 n=1
수준으로 사실상 무의미한 것은 버그가 아니라 이 표본 규모 자체가 원인이며, 리포트 본문에
그 근거(전환 이벤트 자체가 0~3건)를 상세히 기록했다.
