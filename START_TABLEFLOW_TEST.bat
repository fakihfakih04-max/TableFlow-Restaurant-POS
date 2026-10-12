@echo off
setlocal
cd /d "%~dp0"
echo Starting TableFlow print service in a separate window...
start "TableFlow Print Agent" cmd /k ""%~dp0start_print_agent.bat""
timeout /t 2 /nobreak >nul
echo Opening TableFlow Restaurant POS...
start "" "%~dp0index.html"
echo.
echo IMPORTANT: Keep the print-agent window open.
echo Before using real orders, test USB receipt and LAN kitchen printer in Settings.
pause
