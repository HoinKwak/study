# 재현 안내 — OI Bipower Variation 점프탐지 — 레버리지쇼크 (스윙)

스펙: `research/strategies/oi-bipower-variation-jump-leverage-shock-swing.md`
대조군 스펙(가격기반 BV, 동어반복 점검용): `research/strategies/bipower-variation-jump-continuation-swing.md`
리포트: `research/backtests/oi-bipower-variation-jump-leverage-shock-swing.md`

## 데이터 준비
```bash
export OIBV_SCRATCH=/path/to/scratch/oibv
export OIBV_REPO_SRC=/path/to/study/src
mkdir -p "$OIBV_SCRATCH"/data/{klines_1d,klines_1h,metrics}
bash dl_klines_1d.sh    # 1d klines monthly zip(7종목, 2022-01~2026-07) — 진입/청산/ATR14
bash dl_klines_1h.sh    # 1h klines monthly zip(7종목, 동일기간) — 가격기반 JR(대조군) 계산용
bash dl_metrics.sh      # metrics 일별 zip(7종목 × 2022-01-01~2026-06-30, 약 11,494 파일) — OI
```

## 실행
```bash
cd research/backtests/repro/oi-bipower-variation-jump-leverage-shock-swing
python3 run_lookahead_cut.py       # 룩어헤드 절단 테스트(BTC/ETH/ADA/XRP)
python3 run_main.py                # base/price_swap/reverse/no_invalidation/placebo/gross/quiet_follow
python3 run_tautology.py           # OI-JR vs 가격-JR 상관(전체·트리거시점), 종목간 상관(평시·위기)
python3 run_declustering.py        # 캘린더일·3~5일 롤링 de-clustering(net·gross 모두 R-배수)
python3 run_robustness.py          # LOO·top-N 제거·파라미터 스윕 24변형
python3 run_shuffle_bootstrap.py   # 부호무작위화 100회·이항검정·부트스트랩(대조군 우열)
```

## 핵심 설계 결정(스펙 원문이 모호했던 지점)
- **price-JR 대조군의 계산 간격**: 스펙이 인용하는 원 가격기반 스펙(`bipower-variation-jump-
  continuation-swing.md`)은 15m 봉으로 가격 JR을 계산하나, 본 백테스트의 "동일 엔진 대조군"은
  OI-JR과 **같은 1시간 간격**(OI 도 1h 리샘플)으로 가격 JR을 계산한다 — 신호원(OI vs 가격)만
  바꾸고 방법론(계산 간격 포함)은 고정해야 "정말 신호원이 문제인지"를 격리해 검정할 수 있기
  때문(과거 8/12 ETH/BTC 펀딩스프레드 신호원 교체 대조군과 동일한 원칙).
- **'조용한 점프' 서브셋 진입 방향**: 스펙 §67행이 "다음 3거래일 이내 변동성 확대 시 그 방향
  추종 옵션"이라고만 서술하고 정확한 트리거를 못박지 않아, `run_symbol_quiet_follow`에서
  "조용한 점프일 이후 follow_window(3)일 내 첫 |Δ%|>=price_confirm_th 인 날의 익일 시가에
  그 방향 추종 진입"으로 조작화했다. ⚠️최초 구현은 조용한 점프일에서 향후 3일을 for 문으로
  미리 훑어(scan-ahead) 브레이크아웃일을 찾은 뒤 그 발견을 즉시 반영해 pending 을 걸었는데,
  체결은 "바로 다음 루프 반복(i+1)의 시가"에 이뤄져 **아직 도래하지 않은 미래봉의 수익률을
  현재 시점에 미리 알고 거래하는 룩어헤드**였다(자체발견: 수정 전 FULL PF(R)=7.358, t=+13.4 —
  비현실적 수치가 버그의 단서). `watching` 상태를 매 bar 이월해 그 bar 자신의 종가 확정
  수익률만으로 그날 브레이크아웃 여부를 판정하도록 수정(현재 engine.py는 수정 후 버전만 담겨 있고, 버그판 수치는 리포트 §10에 기록으로 보존).
- **테제무효화 청산**: "진입 다음 날"을 entry_idx+1(즉 오프셋 1) 딱 1회만 판정하는 것으로
  해석했다(스펙이 매일 반복 판정이라 명시하지 않음). reverse 모드에서도 `trade.direction`
  (최종 체결방향) 기준으로 통일해 원신호 기준 참조 버그 클래스를 피했다(신규 규칙 준수).

## 원 실행 환경
- pandas 3.0.5, scipy 1.17.1
- 왕복비용 0.14%(테이커 0.05%×2 + 슬리피지 0.02%×2), 리스크 1%/트레이드, `RiskManager.build_plan_with_stop`
- IS 2022-01-01~2024-06-30 23:59:59 / OOS 2024-07-01~2026-06-30 23:59:59
- metrics 일별 zip: 11,494 건 중 결측 2건(DOGEUSDT·XRPUSDT 각 1일) — 무시 가능한 수준.
