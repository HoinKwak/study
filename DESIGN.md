# DESIGN.md — crypto-trader 대시보드 디자인 시스템

> AI 에이전트/기여자가 대시보드 UI를 **일관되게** 생성·수정하기 위한 단일 기준 문서.
> 규격: [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
> (Google Stitch 9섹션). **테마는 Revolut 영감**(`revolut/DESIGN.md` — `getdesign add
> revolut`로 생성): 트루블랙 캔버스 + 코발트 바이올렛 액센트 + surface-elevated 카드 +
> 라운드20/필 + Pretendard/Inter. 실제 구현: `src/crypto_trader/monitoring/dashboard.py`
> (HTML/CSS) + `charts.py`(인라인 SVG). 미리보기: `docs/design-preview.html`.

---

## 1. Visual Theme & Atmosphere (테마·분위기)

- **트루블랙 핀테크 대시보드 (Revolut 영감).** `#000000` 캔버스 위에 살짝 밝은
  `#16181a` 카드가 떠 있는 고대비·정보 밀도 높은 UI.
- **코발트 바이올렛(`#494fdf`)** 을 브랜드 액센트로 절제해서 사용(포트폴리오 라인·강조).
- 감정 배제 **데이터 우선**: 색은 의미(손익·방향·단계)에만. P&L 녹/적은 가독성 우선.
- **그림자 없음** — 깊이는 캔버스(블랙)→표면(엘리베이티드) 휘도 차이로만. 카드는 라운드20.
- 톤: 전문적·냉정·모던. 24시간 모니터링에도 눈이 편한 진블랙 배경.

## 2. Color Palette & Roles (색·역할)

| 토큰 | HEX | 역할 |
|---|---|---|
| `--bg` | `#000000` | 페이지 캔버스(트루블랙) |
| `--surface` | `#16181a` | 카드·패널(surface-elevated) |
| `--surface-2` | `#0a0a0a` | 한 단계 깊은 표면(surface-deep) |
| `--border` | `rgba(255,255,255,0.12)` | 헤어라인 구분선(다크) |
| `--text` | `#ffffff` | 기본 텍스트(on-dark) |
| `--muted` | `rgba(255,255,255,0.72)` | 보조 텍스트(on-dark-mute) |
| `--muted-2` | `#8d969e` | 캡션·메타(stone) |
| `--brand` | `#494fdf` | 코발트 바이올렛(브랜드 스탬프, 절제 사용) |
| `--accent` | `#6c72ff` | 밝은 코발트(블랙 위 데이터 라인·강조) |
| `--pos` | `#16a34a` | 이익·상승·롱(green) |
| `--neg` | `#e23b4a` | 손실·하락·숏(Revolut danger) |
| `--btc` | `#f7931a` | BTC 라인/브랜드 |
| `--gold` | `#eab308` | 금(macro), 확산 단계 |

> Revolut 규칙: 코발트는 **스탬프처럼 절제**해서(뷰당 과다 사용 금지). 와이드 액센트
> (teal/pink/green 등)는 일러스트 용도이지 버튼/대량 텍스트 배경으로 쓰지 않는다.

**의미색(직접 지정, 변수 아님) — 코드에서 계산해 사용:**
- 이벤트: PUMP `#16a34a` · DUMP `#dc2626` · VOL_SPIKE `#f59e0b` · OI_SURGE `#22c55e` ·
  OI_DROP `#ef4444` · FUNDING `#a855f7`
- KOL 단계: 조기 `#22c55e` · 확산 `#eab308` · 뒷북 `#94a3b8`
- 차트 시리즈: BTC `#f7931a` · 나스닥 `#38bdf8` · 금 `#eab308` · 포트폴리오 `#38bdf8`

**규칙**: 손익·방향은 항상 pos/neg 로만. 부호(`+`/`-`) 표기 병행. 색맹 대비 위해 색+부호 동시 사용.

## 3. Typography Rules (타이포그래피)

- **폰트**: `'Pretendard', 'Inter', 'Malgun Gothic', 'Apple SD Gothic Neo', system-ui, sans-serif`.
  Pretendard(한글 가독성 우수)를 CDN으로 로드하고, 미설치/오프라인 시 Inter·맑은고딕으로 폴백.
  (Revolut 원본의 Aeonik Pro는 유료 → Inter/Pretendard로 대체.) `-webkit-font-smoothing:antialiased`.
- 위계:
  - `h1` 20px / 페이지 타이틀 (🤖 이모지 접두)
  - `h2` 15px · `--muted` / 섹션 헤더 (이모지 접두: 📈 📊 💪 🌐 📰 🐦 🛰️)
  - `h3` ~14px / 서브섹션
  - 본문 13px / 표·카드 텍스트
  - 캡션 11–12px · `--muted`/`--muted-2` / 시각·라벨·주석
  - 큰 수치 `.stat b` 20px / KPI 값
- 숫자는 부호·소수 자리 일관: 수익률 `+0.00%`, 손익 `+0.00`, 배수 `0.0x`.

## 4. Component Stylings (컴포넌트)

- **카드 `.card` / `.stat`**: 배경 `--surface`, `border-radius:10px`, `padding:14px`.
  가로 넘침 콘텐츠는 `overflow-x:auto`.
- **KPI 스탯 `.stat`**: 세로 flex, 라벨(12px·muted) 위 / 값(20px·pos·neg 색) 아래.
- **표 `table`**: 전폭, `font-size:13px`, 셀 `padding:8px 10px`, 하단 구분선 `--border`.
  헤더 `th`는 `--muted`·600. 순위표는 1열 `#`, 심볼은 `<b>`.
- **접이 섹션 `<details.events>`**: `--surface` 카드, `summary` 커서 포인터·muted.
  기본 접힘 — 부가 정보(시장 이벤트)는 접어 노이즈 감소.
- **차트(인라인 SVG)**: 배경은 카드, 그리드선 `--surface`, 0축 `--border` 점선,
  라인 두께 2px, 범례는 좌상단(CJK 글자폭 반영해 겹침 방지), x축 날짜(KST MM-DD).
- **버튼**: 현재 UI에 상호작용 버튼 없음(읽기 전용 대시보드). 추가 시 `--accent` 배경·
  `--bg` 텍스트·`border-radius:8px`·hover 시 밝기 +10%.

## 5. Layout Principles (레이아웃)

- **간격 스케일**: 4의 배수. 카드 padding 14, 섹션 간 `h2 margin-top:28px`, gap 12–16.
- **페이지 여백**: body `padding:24px`.
- **그리드**: KPI는 `.grid` = `repeat(auto-fit, minmax(150px,1fr))`.
- **멀티 컬럼**: 표/카드 나열은 `display:flex; gap; flex-wrap:wrap` — 좁은 화면에서 자동 줄바꿈.
  (예: 상대강도 3표(좌, flex:2) + 시총표(우, flex:1).)
- **정보 순서(위→아래)**: 타이틀 → KPI → 포트폴리오/일별손익 차트 → BTC대비 강도·시총 →
  매크로 괴리 → 시장 브리핑 → KOL → 열린/청산 포지션 → (접힘)시장 이벤트.
  거래 성과·시장맥락을 위로, 로그성 데이터는 아래·접이로.

## 6. Depth & Elevation (깊이·표면)

- 2단 표면만: `--bg`(바닥) → `--surface`(카드). 카드 위 카드(중첩 표면) 지양.
- **그림자 미사용** — 구분은 배경 대비 + `border-radius`로. 평면적·정보 밀도 유지.
- 강조는 색(의미색)과 굵기로, 입체효과로 하지 않는다.

## 7. Do's & Don'ts

**Do**
- 색은 의미(손익·방향·단계)에만. 손익엔 항상 부호 병행.
- 새 색은 팔레트 토큰/의미색에서 선택. 없으면 DESIGN.md에 먼저 추가.
- 무거운/외부 데이터는 캐시(예: `market_extra` 30분) 후 렌더. 렌더는 가볍게.
- 데이터 없으면 섹션을 **자동 생략**하거나 "데이터 없음"으로. 깨진 UI 금지.
- 외부 라이브러리 없이 인라인 SVG/CSS (오프라인·로컬 서빙 전제).

**Don't**
- 임의의 새 HEX 남발·같은 의미에 다른 색 사용 금지.
- 무지개색·불필요한 그라디언트·그림자 남용 금지.
- 손익을 색으로만 표현(부호 없이) 금지.
- 렌더 시 블로킹 네트워크 호출 금지(캐시/사전계산으로).
- 가로 스크롤이 페이지 전체에 걸리게 금지 — 넘침은 해당 카드 안에서만(`overflow-x:auto`).

## 8. Responsive Behavior (반응형)

- 모든 다열 레이아웃은 `flex-wrap:wrap` + `min-width`로 좁은 화면에서 세로 적층.
- 표/차트는 카드 내부 `overflow-x:auto` — 페이지 본문은 가로 스크롤되지 않음.
- SVG 차트는 `viewBox` + `width:100%`(최대폭 제한)로 폭에 맞게 축소.
- 터치 타깃(버튼/접이 summary)은 최소 높이 ~32px.
- 자동 새로고침(meta refresh) 주기는 스캐너 주기와 연동(기본 30초~주기).

## 9. Agent Prompt Guide (에이전트 프롬프트 가이드)

대시보드 UI를 만들거나 고칠 때 이 문서를 컨텍스트로 주고 아래처럼 지시:

- "DESIGN.md를 따라 대시보드에 `<섹션>`을 추가해줘. `--surface` 카드 + 13px 표,
  헤더는 h2·이모지 접두, 손익은 pos/neg 색+부호."
- "이 값이 양/음이면 `--pos`/`--neg`로, 부호 붙여서 표시."
- "새 시계열 차트는 charts.line_chart 재사용(범례 좌상단, x축 KST 날짜)."
- 새 색이 필요하면 **먼저 DESIGN.md 팔레트/의미색에 정의**한 뒤 코드에서 그 토큰 사용.

**빠른 참조(복붙용 토큰)** — Revolut 영감:
```
bg #000000 · surface #16181a · border rgba(255,255,255,.12) · text #fff · muted rgba(255,255,255,.72)/#8d969e
brand #494fdf · accent #6c72ff · pos #16a34a · neg #e23b4a · btc #f7931a · gold #eab308
radius 20px(카드)/12px(입력)/full(버튼·필) · card padding 20px · gap 14 · body padding 28px
font: 'Pretendard','Inter','Malgun Gothic',system-ui · 그림자 없음(휘도로 깊이)
```
