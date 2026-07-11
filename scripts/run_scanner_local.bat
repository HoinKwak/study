@echo off
REM 시장 스캐너 로컬 상시 구동 (Windows) — 죽으면 자동 재시작.
REM 사용: scripts\run_scanner_local.bat
REM 종료: 창 닫기 또는 Ctrl+C

setlocal
cd /d "%~dp0.."

if exist ".venv\Scripts\activate.bat" call .venv\Scripts\activate.bat
if not exist logs mkdir logs

echo [scanner] 시작 (Ctrl+C 로 종료)

:loop
echo [scanner] %date% %time% 프로세스 기동
python -m scripts.run_scanner
echo [scanner] %date% %time% 프로세스 종료 - 10초 후 재시작
timeout /t 10 /nobreak >nul
goto loop
