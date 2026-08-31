# 체결건수 방향 스트릭 지속 브레이크아웃(스윙) — 재현 스크립트

스펙: `research/strategies/trade-count-directional-streak-breakout-swing.md`
리포트: `research/backtests/trade-count-directional-streak-breakout-swing.md`

## 재현 절차

```bash
# 1) 데이터 다운로드 (4h·1d klines, 2022-01~2026-07, 7종목)
bash dl_klines.sh

# 2) 메인 백테스트(gated/ungated/reverse) — 결과를 scratchpad에 pickle 캐시
python3 run_main.py

# 3) 진단 스크립트 (순서 무관, run_main.py 의 sigs.pkl 캐시를 사용)
python3 run_autocorr.py          # count 자기상관 + 스트릭 이론 대조
python3 run_correlation.py       # 동어반복 점검(거래대금/ROC/ATR 상관, 전체구간 vs 트리거시점)
python3 run_control_ungated.py   # 게이트없음 대조군(매칭-N 부트스트랩 + 독립 Welch)
python3 run_shuffle.py           # 정보원 무력화 셔플 대조군(100회)
python3 run_declustering.py      # de-clustering(캘린더일/3일/5일 롤링, R-배수, net+gross)
python3 run_loo_topn.py          # LOO(7종목) + top-N/bottom-N 제거
python3 run_sweep.py             # 파라미터 스윕(스펙이 나열한 4개 축 전부)
python3 run_lookahead_cut.py     # 룩어헤드 절단 테스트(4종목)
python3 run_symbol_correlation.py  # 종목간 신호상관(평시/위기국면)
```

## 환경변수(선택)

- `TCSTREAK_REPO_SRC` — 저장소 `src` 경로(기본값: 이 스크립트 기준 상위 4단계 `src`).
- `TCSTREAK_SCRATCH` — 원본 데이터 캐시 디렉터리(기본값:
  `/tmp/claude-0/-home-user-study/5c4aa354-51d8-5c5e-afb3-edb007c0a106/scratchpad/tcstreak`,
  워크트리 소멸 시 `dl_klines.sh` 재실행 필요 — 원본 CSV는 git 미포함).

## 구현 메모

- `common.py`: klines(4h/1d) 로더, Donchian(20,4h 직전봉 기준 shift(1)), 스트릭 카운터
  (`count_streak`, 동률=리셋), 1d EMA→4h 매핑(`ema1d_on_4h`, ns epoch 명시 `searchsorted`로
  ms/us 업캐스트 함정 원천 차단).
- `engine.py`: entry는 신호봉 종가 확정 → 다음봉 시가 체결(shift(1)). 청산은 (1) 스톱
  (고정SL=진입가∓ATR×1.3, ATR×2.5 트레일링과 래칫 통합, 유리한 방향으로만 갱신) (2) 스트릭
  반전(원신호 방향 기준, streak_reversal_bars=3) (3) 시간청산(42봉). `mode`: gated(채택안)
  / ungated(스트릭게이트 없는 Donchian+EMA 대조군) / reverse(방향반전, SL/트레일링은 실행방향
  대칭 재배치·서사청산은 원신호 기준 — 프로젝트 관례).
- `short_mode`: `streak_down`(스펙 기본, 대칭가정) / `streak_up_alt`(스펙이 명시한 1차 진단
  스윕 대상 비대칭 대안).

## 핵심 발견(스크립트로 재현 가능)

1. `run_autocorr.py`: count **원시값** lag-1 자기상관은 0.56~0.79(강한 양의 상관, 레벨
   클러스터링)이나 **방향(상승/하락) 이진 지표의 lag-1 자기상관은 -0.12~-0.19로 전부 음수**
   (반지속적/평균회귀 성향). 그 결과 실측 5연속 스트릭 발생률(0.26~0.37%)이 스펙이 사전
   추정한 나이브 이항 기저율(3.12%)의 약 1/10에 불과 — 스펙의 핵심 이론적 근거("자기상관이
   스트릭을 더 자주 만들 것")가 실측으로 반증됨.
2. 원시 조건 카운트(`python3 -c "..."`, 직접 계산): `streak_down>=5 AND Donchian(20) 하단이탈
   AND close<EMA50(1d)` 결합조건이 **7종목 전체·4.6년 합산 0건**. 스펙의 대칭 가정(체결건수
   감소+신저가=지속적 매도)이 문자 그대로 구조적으로 발화 불가능함을 확인(스카우트가 사전에
   우려한 지점이 극단적 형태로 실증됨).
