# 재현 안내 — OI 변동성 대 가격 실현변동성 비율 극단 페이드 (스캘프)

스펙: `research/strategies/oi-volatility-price-volatility-ratio-extreme-fade-scalp.md`
리포트: `research/backtests/oi-volatility-price-volatility-ratio-extreme-fade-scalp.md`

## 데이터 준비
1h·15m klines(monthly zip, 2022-01~2026-06) + metrics 5분(일별 zip, 2022-01-01~2026-06-30),
전량 이번 라운드에 새로 다운로드했다(직전 세션들의 scratchpad 캐시가 컨테이너 재시작으로
유실됨 — CLAUDE.md 9/3 사고 기록 참조).

```bash
export OIVR_SCRATCH=/path/to/scratch/oivolratio
export OIVR_REPO_SRC=/path/to/study/src
mkdir -p "$OIVR_SCRATCH"/data/{klines_1h,klines_15m,metrics}
bash dl_klines.sh     # 1h+15m monthly zip, 7종목 x 54개월 x 2TF = 756파일 (결측 0건 확인)
bash dl_metrics.sh    # metrics 일별 zip, 7종목 x 1642일 = 11,494파일(병렬 xargs -P16)
                       # ⚠️ 최초 실행 후 000/miss 로그(2건, 일시적 curl 실패)를 개별 재시도해
                       # 최종 11,493개 확보 + ADAUSDT 2025-09-26 1건 별도 재시도로 11,494 완결.
```

## 실행
```bash
cd research/backtests/repro/oi-volatility-price-volatility-ratio-extreme-fade-scalp
python3 -c "
import sys; sys.path.insert(0,'.')
import common, pickle
sigs = {s: common.build_signals(s) for s in common.SYMBOLS}
with open(f'{common.SP}/sigs.pkl','wb') as f: pickle.dump(sigs, f)
"                              # 신호 구축(1h z-score + 15m ATR) — sigs.pkl 저장
python3 run_main.py            # dir_mode(A=페이드/B=모멘텀반전) x fee_on(net/gross) — results_main.pkl 저장
python3 run_correlation.py     # 동어반복 점검: OI-가격 상관(전체+트리거시점) + z(ratio) vs z(oi_vol단독)
                                # + 종목간 신호상관(연간평균 + BTC 절대수익률 상위5% 위기국면 꼬리상관)
python3 run_diagnostics.py     # de-clustering(캘린더일/3~5일롤링, net+gross) + LOO + 종목별 + top-N + 부호셔플
python3 run_sweep.py           # 파라미터 스윕(z_th/atr_sl_mult/rr_target/max_hold_bars/vol_window/zscore_window)
python3 run_lookahead_check.py # 룩어헤드 점검: BTC 2025-01-01 절단 후 이전 구간 트레이드 bit 단위 대조
```

## 원 실행 환경
- pandas 3.0.5, numpy 2.4.6, scipy(추가 설치), pydantic/pydantic-settings(추가 설치 — RiskManager
  로딩에 필요, 컨테이너 기본 이미지에 없었음)
- 왕복비용 0.14%(테이커 0.05%×2 + 슬리피지 0.02%×2), 리스크 1%/트레이드,
  `RiskManager.build_plan_with_stop`, `leverage_for`(major=30x/alt=10x)
- IS 2022-01-01~2024-06-30 23:59:59 / OOS 2024-07-01~2026-06-30 23:59:59 (양쪽 다 상한 명시 적용)
- 시드: 셔플·부트스트랩은 `numpy.random.default_rng(<정수>)` 고정 시드 사용

## 신호↔체결 타임프레임 매핑 (구현 설계 판단, 리포트 본문에 근거 명시)
스펙은 "1h z-score 산출 / 15m 진입"이라고만 서술하고 정확한 매핑 규칙을 명시하지 않는다. 이 구현은
1h 봉 j 의 **종가 시각**을 다음 시간의 시작으로 보고, 그 시각을 여는 첫 15m 봉의 **시가**에 체결한다
(1h→15m 교차 타임프레임에서 사실상 `shift(1)`과 동일한 인과관계). ATR(14,15m)은 진입 신호 확정
시점(직전 완결 15m 봉)의 값을 사용해 lookahead를 차단한다. z-회귀(≤0) 청산은 "직전 완결 1h 봉까지"의
z값을 각 15m 봉 **시가 시점**에 확인하는 방식으로 causal하게 구현했다(`engine.py` 상단 docstring 참조).

## 자체 발견 버그(수정 반영, 재현 과정에 실제로 걸림)
- **datetime 해상도 업캐스트 함정(신규 변종)**: `df1h`를 `oi1h`(metrics 유래, 날짜문자열 파싱이라
  기본 `us` 해상도로 추론됨)와 `join`하면 결과 인덱스가 조용히 `datetime64[us]`로 승격된다(원래
  klines 로더는 `ms`였음). 이후 `_completed_1h_counts`가 `+ns_offset`(ns 단위 상수)을 이 us 인덱스에
  더해 1000배 어긋난 임계값을 만들어 **z-회귀 청산 조건이 구조적으로 절대 발화하지 않는 버그**가
  발생했다(실측: 수정 전 1,776건 트레이드 중 z_reversion 청산 0건 → 수정 후 10건). `common.py`에서
  klines 로드 직후·metrics 로드 직후·join 직후 세 지점 모두 `.index.as_unit("ns")`로 명시 통일해
  해소했다. CLAUDE.md가 반복 경고한 "ms/us/ns 혼재 함정"의 새로운 발현 지점(join의 암묵적 업캐스트).
