@echo off
cd /d "%~dp0"
if "%TABLEFLOW_ADMIN_TOKEN%"=="" (
  echo Set TABLEFLOW_ADMIN_TOKEN before running this server.
  set /p TABLEFLOW_ADMIN_TOKEN=Enter a long private admin token: 
)
python -m pip install -r requirements-online.txt
python -m uvicorn server:app --host 0.0.0.0 --port 8000
pause
