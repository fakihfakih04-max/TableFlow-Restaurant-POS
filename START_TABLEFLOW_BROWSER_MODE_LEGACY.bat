@echo off
setlocal
cd /d "%~dp0"
title TableFlow Restaurant POS
set "POSFILE=%~dp0index.html"
if not exist "%POSFILE%" (
  echo ERROR: index.html was not found in this folder.
  echo Extract the complete ZIP first, then run this file from the extracted folder.
  pause
  exit /b 1
)
REM Start the printer helper separately; POS window launch continues independently.
if exist "%~dp0start_print_agent.bat" start "TableFlow Print Service" cmd /k ""%~dp0start_print_agent.bat""
powershell -NoProfile -ExecutionPolicy Bypass -Command "$ErrorActionPreference='Stop'; $file=$env:POSFILE; $url=([System.Uri]::new($file)).AbsoluteUri; $candidates=@((Join-Path $env:LOCALAPPDATA 'Microsoft\Edge\Application\msedge.exe'),(Join-Path $env:ProgramFiles 'Microsoft\Edge\Application\msedge.exe'),(Join-Path ${env:ProgramFiles(x86)} 'Microsoft\Edge\Application\msedge.exe'),(Join-Path $env:LOCALAPPDATA 'Google\Chrome\Application\chrome.exe'),(Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe'),(Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe')); $browser=$null; foreach($candidate in $candidates){if($candidate -and (Test-Path $candidate)){$browser=$candidate;break}}; if(-not $browser){$cmd=Get-Command msedge.exe -ErrorAction SilentlyContinue; if($cmd){$browser=$cmd.Source}}; if(-not $browser){$cmd=Get-Command chrome.exe -ErrorAction SilentlyContinue; if($cmd){$browser=$cmd.Source}}; if(-not $browser){Write-Host 'Microsoft Edge or Google Chrome was not found.' -ForegroundColor Red; exit 2}; Start-Process -FilePath $browser -ArgumentList @('--new-window',('--app='+$url))"
if errorlevel 1 (
  echo.
  echo Could not open the POS window. Make sure Microsoft Edge or Google Chrome is installed.
  pause
)
