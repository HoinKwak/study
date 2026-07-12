# CLAUDE.md — 행동 규약 & 프로젝트 가이드

이 파일은 세션·대화 압축(compaction)과 무관하게 **항상** 지켜야 하는 규약이다.
대화가 압축되어 맥락이 리셋되어도 이 파일의 규칙은 그대로 적용된다.

---

## 0. 커뮤니케이션 규약 (최우선 · 압축되어도 유지)

1. **항상 존댓말을 쓴다.** 사용자에게 보고·설명·질문할 때 반말·구어체 금지.
   대화가 압축되어 말투가 리셋된 것처럼 느껴져도, 이 규칙을 먼저 확인하고 존댓말로 답한다.
2. **중간 진행 상황은 항상 한글로 보고한다.** 작업을 시작할 때·단계가 바뀔 때·끝났을 때
   무엇을 하고 있는지 한글로 짧게 알린다. (코드·커밋 메시지·식별자는 예외)
3. **진행 중인 업무는 압축의 영향을 받지 않게 관리한다.**
   - 큰 작업은 시작 전에 계획을 남기고, 단계마다 커밋해 중간 상태를 디스크에 보존한다.
   - 미완료 작업이 있으면 그 상태(무엇을 어디까지 했고 다음이 무엇인지)를 한글로 명확히 남긴다.
   - 압축 후 이어받을 때는 이 파일 → 최근 커밋 → 코드 상태 순으로 확인하고, 사용자에게
     되묻지 말고 마지막 작업을 이어서 진행한다.

---

## 1. 프로젝트 개요

**crypto-trader** — 개인용 자동 암호화폐 트레이딩 봇.
- 사용자 Windows PC에서 로컬 구동, **바이낸스 선물 USDT-M 테스트넷** 대상.
- 자체 완결형 HTML 라이브 대시보드(인라인 SVG 차트·인라인 JS, Pretendard CDN 외 외부 라이브러리 없음).
- 3개 슬리브 포트폴리오(단타 1분 / 중기 15분 / 중장기 4시간), 헤지·isolated 모드, 논리적 자본 배분(50/25/25).
- 시장 스캐너(급등락·거래량/OI 급증·펀딩 극단 감지) → 텔레그램 알림 + 대시보드 갱신.

### 로컬 실행 환경 (사용자 Windows PC)
- 프로젝트 경로(고정): `C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh`
- 실행 명령 안내 시 이 경로를 그대로 쓴다(플레이스홀더 `C:\경로\study` 대신).
- PowerShell은 `&&` 미지원 → 줄을 나누거나 `;` 사용. 가상환경: `.\.venv\Scripts\Activate.ps1`.
- 3개 프로세스는 각각 별도 창: ① 매매봇 `python -m scripts.run_portfolio`
  ② 알람봇(스캐너) `python -m scripts.run_scanner` ③ 대시보드 `python -m scripts.serve_dashboard`.

### 주요 실행 스크립트
- `python -m scripts.run_scanner` — 시장 스캐너 상시 구동 + `state/dashboard.html` 갱신.
- `python -m scripts.serve_dashboard` — 로컬 대시보드 웹서버(`http://localhost:8787`).
  파생 지표(`/api/derivs`)·캔들(`/api/klines`)·심볼(`/api/symbols`) API는 이 서버 모드에서만 실시간 동작.
- `python -m scripts.recompute_pnl` — 청산 손익 수수료 소급 보정(idempotent).
- `python -m scripts.yt_transcript <url|id> [--meta] [--out f]` — 유튜브 자막(트랜스크립트) 추출.
  **유튜브 영상 분석·전략 발굴은 반드시 이 도구로 트랜스크립트를 먼저 확보한다**(서드파티
  트랜스크립트 사이트는 CAPTCHA로 자주 막힘). yt-dlp 기반, `HTTPS_PROXY` 자동 사용.

---

## 2. 보안 · 상시 제약 (반드시 준수)

- **`.env` 는 절대 커밋하지 않는다** (`.gitignore` 에 포함됨). 테스트넷 키·텔레그램 토큰은
  사용자 본인의 저위험 자격증명이지만 저장소에 올리지 않는다.
- **모델 식별자(`claude-opus-4-8` 등)를 커밋 메시지·PR·코드·주석 등 저장소 산출물에
  절대 넣지 않는다.** 채팅 답변에만 사용.
- 모든 커밋은 지정된 `Co-Authored-By` / `Claude-Session` 푸터로 끝낸다.
- **명시적 요청 없이는 PR을 만들지 않는다.**
- 테스트넷에는 **한 번에 하나의 봇만** 구동한다.
- **Crescent Hook HR 프로젝트는 건드리지 않는다.**

---

## 3. Git

- 개발·푸시 브랜치: **`claude/personal-ai-assistant-11xcgh`** (여기 외 다른 브랜치에 푸시 금지).
- 푸시: `git push -u origin claude/personal-ai-assistant-11xcgh`, 네트워크 실패 시 지수 백오프(2/4/8/16s)로 최대 4회 재시도.
- 커밋 메시지는 한글로 명확하게. 변경이 완결되면 커밋·푸시.

---

## 4. 코드 스타일

- Python 3.11, `from __future__ import annotations`.
- 주석·로그·사용자 노출 문자열은 한글. 넓은 예외 포착에는 `# noqa: BLE001`.
- 대시보드는 외부 의존성 없는 자체 완결형 HTML을 유지한다(인라인 SVG/JS).
- 기존 코드의 관용구·네이밍·주석 밀도를 따른다.
