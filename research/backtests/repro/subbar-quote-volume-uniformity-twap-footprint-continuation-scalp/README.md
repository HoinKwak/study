# 재현 코드 — 서브캔들 거래대금 균일도 TWAP 흔적 지속 [단타]

`research/.gitignore` 가 `impl/` 을 통째로 제외해 백테스트 원본 구현이 저장소에 남지
않고, 작업 워크트리가 사라지면 재현이 불가능해진다. 그 구조적 취약점 대응으로 이 건의
구현 스크립트를 여기 보존한다(원본 위치는 `research/impl/subbarcv_*.py`).

⚠️ 이는 **개별 조치**이며 `research/.gitignore` 정책 자체는 바꾸지 않았다. 저장소 전체로
확대할지는 사장님 결정 사항이다.

- `subbarcv_common.py` — 공통 유틸·상수(기간·비용·유니버스)
- `subbarcv_prefetch.py` / `subbarcv_prefetch_warmup.py` — data.binance.vision 덤프 수신
- `subbarcv_signals.py` — 5m→1h 서브캔들 집계와 CV·consist·range 신호 산출
  (Python 루프 → 벡터화 재작성으로 약 85배 단축, 재작성 전후 결과 일치를 유닛테스트로 확인)
- `subbarcv_engine.py` — 체결·청산 엔진
- `subbarcv_strat.py` — 전략 조합(채택안·게이트없음 대조군·반전 대조군·CV 셔플 대조군)
- `subbarcv_analyze.py` — 집계·통계(PF(R)·t·부트스트랩·de-clustering·LOO·스윕)
