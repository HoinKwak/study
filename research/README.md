# 전략 발굴 파이프라인 (research)

외부(유튜브/트레이딩뷰/레딧 등)에서 단기매매 전략을 발굴 → 백테스트 검증 →
우리 시스템 통합 검토까지 이어지는 3단계 서브에이전트 파이프라인의 작업 공간.

## 서브에이전트 (`.claude/agents/`)
1. **strategy-scout** — 웹에서 단타 전략 수집. 백테스트 근거 우선, 없으면 조회수·추천수로
   스크리닝. 코딩 가능한 명확한 규칙만. → `research/strategies/*.md`
2. **strategy-backtester** — 스펙을 우리 `SleeveBacktester`로 구현·검증(수수료·슬리피지 반영,
   worktree 격리). 유의미한 엣지만 통과. → `research/backtests/*.md`
3. **strategy-integrator** — 통과 전략을 슬리브에 그대로/보완/대체할지 판단·제안.
   → `research/integration/*.md`

## 실행 방법 (Claude Code)
```
"strategy-scout 로 단타 전략 5개 발굴해줘"
→ 나온 스펙 중 유망한 걸 "strategy-backtester 로 백테스트"
→ 통과한 걸 "strategy-integrator 로 통합 검토"
```
각 단계는 독립 파일로 산출물을 남기므로 중간에 사람이 검토·선별할 수 있다.

## 폴더
- `strategies/` — 발굴된 전략 스펙
- `backtests/` — 백테스트 결과·판정
- `integration/` — 통합 제안서
- `impl/` — 백테스터가 만든 임시 구현(참고용)

> ⚠️ 발굴된 전략은 **검증 전까지 신뢰하지 않는다.** 백테스트 통과 + 페이퍼 검증을 거친
> 뒤에만 실거래 도입을 검토한다.
