@echo off
setlocal
powershell -NoProfile -ExecutionPolicy Bypass -Command "$root=$PSScriptRoot; $desktop=[Environment]::GetFolderPath('Desktop'); $shortcut=Join-Path $desktop 'TableFlow Restaurant POS.lnk'; $shell=New-Object -ComObject WScript.Shell; $sc=$shell.CreateShortcut($shortcut); $sc.TargetPath=Join-Path $root 'START_TABLEFLOW_WINDOWS_APP.bat'; $sc.WorkingDirectory=$root; $sc.Description='Launch TableFlow Restaurant POS and printer service'; $sc.Save(); Write-Host 'Desktop shortcut created:' $shortcut"
pause
