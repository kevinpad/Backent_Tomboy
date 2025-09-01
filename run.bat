@echo off
setlocal enabledelayedexpansion
cd /d %~dp0

rem ---- config ----
set HOST=127.0.0.1
set PORT=8100
set CMD=%1
if "%CMD%"=="" set CMD=start
if not "%2"=="" set PORT=%2

rem ---- venv ----
if not exist .venv ( py -3 -m venv .venv 2>nul || python -m venv .venv )
call .venv\Scripts\activate.bat

rem ---- deps ----
python -m pip install --upgrade pip setuptools wheel >nul
pip install -r requirements.txt >nul

rem ---- abrir /docs en 2s ----
start "" cmd /c "timeout /t 2 >nul & start http://localhost:%PORT%/docs"

rem ---- arrancar ----
if /I "%CMD%"=="dev" goto DEV
goto START

:DEV
echo [RUN] DEV (autoreload) app.main:app en %HOST%:%PORT%
python -m uvicorn app.main:app --host %HOST% --port %PORT% --reload --reload-dir app --reload-include *.py --reload-include .env --reload-include *.json
goto END

:START
echo [RUN] START (sin autoreload) app.main:app en %HOST%:%PORT%
python -m uvicorn app.main:app --host %HOST% --port %PORT%
goto END

:END
pause