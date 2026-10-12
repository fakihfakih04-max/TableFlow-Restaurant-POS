@echo off
setlocal
cd /d "%~dp0"
set "ISCC=%ProgramFiles(x86)%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" set "ISCC=%ProgramFiles%\Inno Setup 6\ISCC.exe"
if not exist "%ISCC%" (
 echo Inno Setup 6 not found. Install it, then retry.
 pause
 exit /b 1
)
"%ISCC%" TableFlowPOS_Setup.iss
if errorlevel 1 goto fail
echo.
echo Setup created in the Output folder.
pause
exit /b 0
:fail
echo Installer build failed.
pause
exit /b 1
