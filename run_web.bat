@echo off
title Smart Calculator Web App (PWA)
cd /d "%~dp0"

:: 1. Prioritize Python 3.12 installed
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" web_server.py
    goto finish
)

:: 2. Check py launcher
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    py -3 web_server.py
    goto finish
)

:: 3. Check system python
for /f "tokens=*" %%i in ('where python 2^>nul') do (
    echo "%%i" | findstr /i "WindowsApps" >nul
    if errorlevel 1 (
        "%%i" web_server.py
        goto finish
    )
)

:: 4. Fallback to bundled runtime
if exist "%~dp0python_runtime\python.exe" (
    "%~dp0python_runtime\python.exe" web_server.py
    goto finish
)

echo [!] Could not locate Python to run web_server.py.
pause

:finish
