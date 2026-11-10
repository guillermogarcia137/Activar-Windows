@echo off
setlocal
where powershell.exe >nul 2>&1
if errorlevel 1 (
    echo Error: Windows PowerShell no esta disponible. 1>&2
    exit /b 1
)
powershell.exe -NoLogo -NoProfile -File "%~dp0script.ps1" %*
exit /b %errorlevel%
