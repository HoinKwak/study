# 재현 스크립트 보존 — cross-sectional-premium-index-volatility-squeeze-rank-rotation-swing

`research/.gitignore`가 `impl/`을 제외해 백테스트 구현 스크립트가 git에 남지 않고,
워크트리·스크래치패드가 소멸하면 재현이 불가능해지는 구조적 취약점이 여러 감사에서 반복 지적됐다.
이 건은 backtest-reviewer가 "커밋 전에 impl을 별도 보존하라"고 명시 권고해, 해당 경로에 복사해 둔다.

⚠️ 이는 이번 건 한정 보존이며 `.gitignore` 정책 자체는 바꾸지 않았다.
전 백테스트에 이 방식을 적용할지는 사장님 결정 사항이다.

- 원본 위치: 세션 스크래치패드(소멸성)
- 리포트: `research/backtests/cross-sectional-premium-index-volatility-squeeze-rank-rotation-swing.md`
- 스펙: `research/strategies/cross-sectional-premium-index-volatility-squeeze-rank-rotation-swing.md`
