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
4. **`git pull` 안내 시 재구동 코드를 항상 함께 준다.** 코드 변경을 push하고 `git pull`을
   안내할 땐, 어떤 프로세스(①매매봇/②알람봇/③대시보드)를 재시작해야 하는지 유형별로 명시하고
   붙여넣기용 명령 블록을 같이 준다. 상세 규약은 §1의 「재구동 안내 규약」 참조.

---

## 1. 프로젝트 개요

**crypto-trader** — 개인용 자동 암호화폐 트레이딩 봇.
- 사용자 Windows PC에서 로컬 구동, **바이낸스 선물 USDT-M 테스트넷** 대상.
- 자체 완결형 HTML 라이브 대시보드(인라인 SVG 차트·인라인 JS, Pretendard CDN 외 외부 라이브러리 없음).
- **단타 전용 포트폴리오(100%)** — 10m·15m 2슬리브(각 50%). 중기·스윙은 손익비 미달로 제외
  (정의는 git 이력에 있어 복원 가능). 헤지·isolated 모드.
- 시장 스캐너(급등락·거래량/OI 급증·펀딩 극단 감지) → 텔레그램 알림 + 대시보드 갱신.

### 현재 전략·리스크 설정 (2026-07 기준, 바뀌면 여기 갱신)
- **단타 슬리브**: `scalp`(10m/확인30m) + `scalp15m`(15m/확인1h). 볼린저 이탈 강봉+거래량 급증 돌파.
  진입필터 `vol_spike≥5·squeeze≤35%·body≥1.3ATR·regime=False`. 메이커 진입(post-only), 10분할×20초.
  청산: 모멘텀 신고가→분할(tp1 50%+tp2 50%) + 횡보전환 시 모멘텀 꺾이면 청산. SL=신호봉 시가(stop_mult=1.0).
- **레버리지**: 시총상위(major_bases) **30x**, 알트 **10x** (`Settings.leverage_for`).
- **동적 유니버스**: 24h 거래대금 **$10M 이상**(SOL 제외). 사이징은 증거금 기준(`position_margin_pct`).
- **10m 은 바이낸스 비네이티브** → 워커 `_fetch_df`가 5m에서 리샘플(`TF_RULE` 10m).
- 백테스트 검증(교차검증): 3·5분 적자, **15분이 가장 유효(흑자)**, 10분은 국면 의존. 발굴 전략
  ATR-RSI는 우리 프레임워크에서 FAIL(외부 Sharpe 주장 재현 안 됨).

### 백테스트 데이터 소스 (fapi 지역차단 대응 — 중요)
- 이 클라우드 컨테이너에선 **바이낸스 선물 fapi가 451(지역차단)** — klines·ticker 모두 불가.
- **선물 캔들**: `https://data.binance.vision/data/futures/um/{monthly|daily}/klines/<SYM>/<TF>/...zip`
  덤프를 받는다. **선물 전용 알트(XPIN·TAC·EVAA·LAB 등)까지 포함**되므로 실제 유니버스 백테스트 가능.
  (현물 미러 `data-api.binance.vision`는 선물전용 알트가 없어 부적합 — 유니버스는 '선물' 기준이다.)
- **선물 유니버스·24h 거래량**: CoinGecko 파생 API(`/derivatives/exchanges/binance_futures?include_tickers=all`,
  `converted_volume.usd`)로 순위. 10M 이상 ≈ 116종목.
- 라이브 봇은 스캐너/`connectors/universe.py`로 유니버스 선정(fapi→CoinGecko→현물미러 폴백).

### 정기 리서치 루틴 & 최근 반영된 개선
- **정기 루틴 3종**(KOL 하이프워치 2h·시장브리핑 12h·전략발굴 12h)은 **이 상시 세션에 바인딩**
  (`persistent_session_id`)돼 발화 → 이 세션에서 서브에이전트 실행 후 커밋·push. 폰 완료알림은 없음
  (fresh-session 방식은 새 세션에 레포 쓰기권한이 없어 push 403 → 상시세션 바인딩으로 해결).
  결과물: `research/kol/`, `research/market/`, `research/strategies/`, `research/backtests/`.
- **최근 수정**(git 이력): 청산 짜바리 방지(분할청산 스텝사이즈 정합), 수동/외부 청산 정확 반영
  (`fetch_realized_close`로 실제 체결가·실현손익), 대시보드 '최근청산' 청산시각 정렬, 일별/누적손익이
  실잔고 이력 부족 시 저널 기준으로 폴백, 고아 슬리브 리컨실(제거·개명된 옛 슬리브로 열린 포지션은
  워커가 안 훑어 영영 '열림'으로 남던 것 → 엔진 `_reconcile_orphan_exits`가 거래소 실체결로 청산 반영).

### 로컬 실행 환경 (사용자 Windows PC)
- 프로젝트 경로(고정): `C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh`
- 실행 명령 안내 시 이 경로를 그대로 쓴다(플레이스홀더 `C:\경로\study` 대신).
- PowerShell은 `&&` 미지원 → 줄을 나누거나 `;` 사용. 가상환경: `.\.venv\Scripts\Activate.ps1`.
- 3개 프로세스는 각각 별도 창: ① 매매봇 `python -m scripts.run_portfolio`
  ② 알람봇(스캐너) `python -m scripts.run_scanner` ③ 대시보드 `python -m scripts.serve_dashboard`.

### 재구동 안내 규약 (git pull 안내 시 항상 함께 준다)
코드 변경 후 `git pull`을 안내할 땐 **반드시 어떤 프로세스를 재시작해야 하는지 유형별로 명시**하고
아래 붙여넣기용 블록을 함께 준다. 재시작은 **해당 창에서 Ctrl+C로 멈추고 → 재실행**.
- 어느 프로세스를 재시작할지는 변경 위치로 판단:
  - `portfolio/`·`strategy/`·`risk/`·`connectors/`·`execution/`·`config/` → **① 매매봇**
  - `scanner/`·`monitoring/`(스캐너 경로)·detectors → **② 알람봇**
  - `monitoring/dashboard.py`·`serve_dashboard`·대시보드 API → **③ 대시보드**
  - 대시보드는 저널만 읽으므로, 매매 로직만 바뀌면 매매봇만 재시작하면 새로고침에 반영된다.

**공통(한 번, 아무 창):**
```powershell
cd C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh
git pull origin claude/personal-ai-assistant-11xcgh
```
**① 매매봇** / **② 알람봇** / **③ 대시보드** (각 창에서 Ctrl+C 후):
```powershell
cd C:\Users\ghdls\Documents\study-claude-personal-ai-assistant-11xcgh\study-claude-personal-ai-assistant-11xcgh
.\.venv\Scripts\Activate.ps1
python -m scripts.run_portfolio      # ① 매매봇 (또는 run_scanner=② / serve_dashboard=③)
```

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

---

## 5. 작업 원칙 (Karpathy 4원칙 — LLM 코딩 함정 방지)

출처: `multica-ai/andrej-karpathy-skills`. Andrej Karpathy가 지적한 LLM 코딩의 흔한 실수
(멋대로 가정·과잉설계·불필요한 수정)를 막기 위한 규약. **속도보다 신중함이 우선.**
사소한 작업엔 판단껏 완화하되, 비트는 판단이 필요할수록 이 원칙을 지킨다.

1. **코딩 전에 생각한다 (Think Before Coding)** — "가정하지 말고, 혼란을 숨기지 말고, 트레이드오프를 드러내라."
   - 요구가 모호하면 **멋대로 정하지 말고** 해석 후보를 제시하고 되묻는다.
   - 리스크·전략 파라미터(레버리지·유니버스·손절 등)는 **사용자 결정 사항**이다. 내가 임의로
     '안전장치'를 바꾸지 않는다. 우려가 있으면 데이터로 **짧게 정보 제공**만 하고 실행은 요청대로.
2. **단순함이 먼저 (Simplicity First)** — "문제를 푸는 최소 코드, 투기적인 것 없이."
   - 요청 안 한 기능·추상화·안 일어날 엣지케이스 방어를 덧붙이지 않는다.
3. **수술적 변경 (Surgical Changes)** — "꼭 필요한 것만 건드리고, 네가 만든 흔적만 치워라."
   - 무관한 코드 리팩터·스타일 변경 금지. 기존 관용구·네이밍 보존. 내가 만든 미사용물만 정리.
4. **목표 기반 실행 (Goal-Driven Execution)** — "성공 기준을 정의하고, 검증될 때까지 반복하라."
   - 작업을 **검증 가능한 성공 기준**으로 바꾸고, 테스트·백테스트·재현으로 확인한 뒤 '완료'라 말한다.
   - 실패·미검증은 정직하게 보고. 예: 백테스트는 단위·정합 버그가 흔하니(ns/ms, 유니버스 소스,
     TWAP 근사) **결과가 이상하면 먼저 계측·의심하고** 수치로 확인한 뒤 결론낸다.

성공의 지표: 불필요한 diff·재작성이 줄고, 구현 전에 확인 질문이 나오고, '완료'가 검증을 동반한다.
