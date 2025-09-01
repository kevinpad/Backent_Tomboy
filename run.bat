@echo off
setlocal
cd /d %~dp0

:: 1) Crear venv si no existe y activarlo
if not exist .venv (
  py -3 -m venv .venv 2>nul || python -m venv .venv
)
call .venv\Scripts\activate.bat

:: 2) Instalar/actualizar dependencias dentro del venv
python -m pip install --upgrade pip setuptools wheel >nul
pip install -r requirements.txt >nul

:: 3) Levantar la API (sin autoreload, como “ejecutable”)
python -m uvicorn src.index:app --host 127.0.0.1 --port 8000

pause