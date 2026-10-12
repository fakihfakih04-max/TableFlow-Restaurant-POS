@echo off
title TableFlow Xprinter LAN + USB Print Agent
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  set PY=py -3
) else (
  set PY=python
)
%PY% -c "import win32print" >nul 2>nul
if errorlevel 1 (
  echo Installing Windows USB printer support (pywin32)...
  %PY% -m pip install --upgrade pywin32
  if errorlevel 1 (
    echo.
    echo Could not install pywin32. Please install Python 3 and retry.
    pause
    exit /b 1
  )
)
%PY% print_agent.py
if errorlevel 1 (
  echo.
  echo Could not start the print agent. Check the error above.
  pause
)
