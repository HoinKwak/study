# 로컬 PC 상시 구동 가이드

이 세션의 컨테이너는 비활성 시 회수되어 봇이 계속 죽습니다.
로컬 PC에서 돌리면 24시간 안정적으로 페이퍼 트레이딩이 가능합니다.

---

## 0. 사전 준비

- **Python 3.11 이상** 설치 ([python.org](https://www.python.org/downloads/))
  - 설치 시 Windows는 "Add Python to PATH" 체크
- **Git** 설치 (또는 GitHub에서 ZIP 다운로드)

## 1. 코드 내려받기

```bash
git clone https://github.com/HoinKwak/study.git
cd study
git checkout claude/personal-ai-assistant-11xcgh
```

## 2. 가상환경 + 의존성 설치

**Mac / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 3. `.env` 파일 만들기

`.env.example` 을 복사해 `.env` 로 만들고 값을 채웁니다.

```bash
cp .env.example .env      # Windows: copy .env.example .env
```

`.env` 를 열어 아래 값들을 입력 (테스트넷 키·텔레그램은 이 세션에서 쓰던 값 그대로):

```ini
BINANCE_API_KEY=<테스트넷 API 키>
BINANCE_API_SECRET=<테스트넷 시크릿>
BINANCE_TESTNET=true
TRADE_MODE=paper

MAX_OPEN_POSITIONS=10
POSITION_MARGIN_PCT=10.0      # 증거금 기준 사이징 (공격적 — 원하면 3~5로 낮추기)

TELEGRAM_BOT_TOKEN=<봇 토큰>
TELEGRAM_CHAT_ID=<챗 ID>
NOTIFY_MIN_LEVEL=TRADE
```

> 테스트넷 키를 새로 발급하려면: https://testnet.binancefuture.com 로그인 → 하단 API Key

## 4. 실행 (자동 재시작 포함)

크래시/네트워크 오류로 죽어도 자동으로 다시 뜨는 스크립트를 씁니다.

**Mac / Linux**
```bash
bash scripts/run_local.sh scalp
```

**Windows**
```cmd
scripts\run_local.bat scalp
```

- 종료: `Ctrl+C` (또는 창 닫기)
- 로그: `logs/paper_scalp.log`
- 진입/청산 알림은 텔레그램으로 옵니다.

## 4-b. 시장 스캐너 (급등/급락/거래량·OI 급증 알림)

자동매매와 별개로, 바이낸스 선물 전 종목을 훑어 이벤트를 텔레그램으로 쏴줍니다.
**단타 봇과 다른 터미널에서** 같이 돌리면 됩니다.

**Mac / Linux**
```bash
bash scripts/run_scanner_local.sh
```

**Windows**
```cmd
scripts\run_scanner_local.bat
```

- 급등/급락·거래량 급증·OI 급증/급감·펀딩 극단 이벤트를 감지해 텔레그램 알림
- 같은 심볼·이벤트는 30분 쿨다운(재알림 억제) — `.env` 의 `SCANNER_*` 로 조정
- `state/dashboard.html` 을 매 사이클 갱신

## 4-c. 대시보드 브라우저로 보기

```bash
python -m scripts.serve_dashboard      # http://localhost:8787 (자동 새로고침)
```

스캐너가 돌고 있으면 시장 이벤트가, 봇이 돌고 있으면 거래 상태가 실시간 반영됩니다.

## 5. 상태 확인 (다른 터미널에서)

```bash
source .venv/bin/activate          # Windows: .venv\Scripts\activate
python -m scripts.status           # 성과 요약
python -m scripts.status --html    # state/dashboard.html 생성 (시장 이벤트 포함)
```

---

## PC 절전 방지 (중요)

봇이 계속 돌려면 PC가 잠들면 안 됩니다.
- **Windows**: 설정 → 전원 → "화면/절전 안 함"
- **Mac**: 시스템 설정 → 배터리/전원 → "디스플레이 꺼져도 잠자기 방지", 또는
  터미널에서 `caffeinate -s bash scripts/run_local.sh scalp`

## 백그라운드 상시 구동 (선택)

터미널을 닫아도 계속 돌리려면:

**Mac / Linux**
```bash
nohup bash scripts/run_local.sh scalp > /dev/null 2>&1 &
# 종료: pkill -f run_portfolio
```

**Windows**: 작업 스케줄러에 `run_local.bat` 을 "로그온 시 실행"으로 등록,
또는 [NSSM](https://nssm.cc/) 으로 서비스 등록.

---

## 자주 묻는 것

- **거래가 안 나와요**: 스퀴즈+거래량+OI 필터가 빡세서 신호가 선별적입니다.
  BTC/ETH 등 40여 페어를 훑어도 2~4일에 몇 건 수준일 수 있어요. 정상입니다.
- **지역 차단(451)**: 한국 등에서 바이낸스 실서버가 막히면 유니버스는 코인게코로
  자동 폴백합니다. 테스트넷 주문은 대부분 지역에서 정상 동작합니다.
- **실전 전환**: `.env` 의 `BINANCE_TESTNET=false` + 실계좌 키 + `TRADE_MODE=live`.
  ⚠️ 반드시 페이퍼로 충분히 검증하고, `POSITION_MARGIN_PCT` 를 낮춰 소액부터.
