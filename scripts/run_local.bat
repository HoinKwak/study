@echo off
REM 로컬 상시 구동용 (Windows) — 크래시로 죽으면 자동 재시작.
REM 사용: scripts\run_local.bat [슬리브]
REM   예) scripts\run_local.bat scalp
REM 종료: 창 닫기 또는 Ctrl+C

setlocal
set SLEEVES=%1
if "%SLEEVES%"=="" set SLEEVES=scalp

cd /d "%~dp0.."

REM venv 활성화 (있으면)
if exist ".venv\Scripts\activate.bat" call .venv\Scripts\activate.bat

if not exist logs mkdir logs
echo [run_local] 시작 - 슬리브=%SLEEVES% (Ctrl+C 로 종료)

:loop
echo [run_local] %date% %time% 프로세스 기동
python -m scripts.run_portfolio --sleeves %SLEEVES%
echo [run_local] %date% %time% 프로세스 종료 - 10초 후 재시작
timeout /t 10 /nobreak >nul
goto loop
