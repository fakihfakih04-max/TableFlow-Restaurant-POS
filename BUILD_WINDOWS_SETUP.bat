@echo off
setlocal
cd /d "%~dp0"
title Build TableFlow Restaurant POS Setup
where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher not found. Install Python 3.11 or 3.12 x64 first.
  pause
  exit /b 1
)
py -3 -m venv .buildvenv
if errorlevel 1 goto fail
call .buildvenv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install pywebview pyinstaller pywin32 pillow
if errorlevel 1 goto fail
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
pyinstaller --noconfirm --clean --onefile --windowed --name TableFlowPOS --icon TableFlowPOS.ico --add-data "index.html;." app_launcher.py
if errorlevel 1 goto fail
pyinstaller --noconfirm --clean --onefile --console --name TableFlowPrintAgent --icon TableFlowPOS.ico print_agent.py
if errorlevel 1 goto fail
if not exist dist\TableFlowPOS mkdir dist\TableFlowPOS
copy /y dist\TableFlowPOS.exe dist\TableFlowPOS\TableFlowPOS.exe >nul
copy /y dist\TableFlowPrintAgent.exe dist\TableFlowPOS\TableFlowPrintAgent.exe >nul
if not exist dist\TableFlowPOS\TableFlowPOS.exe goto fail
if not exist dist\TableFlowPOS\TableFlowPrintAgent.exe goto fail
if not exist "%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe" if not exist "%ProgramFiles%\Inno Setup 6\ISCC.exe" (
  echo.
  echo EXE build completed. Install Inno Setup 6, then run BUILD_INSTALLER_ONLY.bat to create Setup.exe.
  pause
  exit /b 0
)
call BUILD_INSTALLER_ONLY.bat
exit /b %errorlevel%
:fail
echo.
echo BUILD FAILED. Read the error above and send a screenshot.
pause
exit /b 1
