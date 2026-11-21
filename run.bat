@echo off
title Smart Calculator
cd /d "%~dp0"

:: 1. Prioritize installed Python 3.12 with CustomTkinter & GUI support
if exist "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python312\python.exe" main.py
    goto finish
)

:: 2. Check py launcher
where py >nul 2>&1
if %ERRORLEVEL% equ 0 (
    py -3 main.py
    goto finish
)

:: 3. Check system python (skip windowsapps stub)
for /f "tokens=*" %%i in ('where python 2^>nul') do (
    echo "%%i" | findstr /i "WindowsApps" >nul
    if errorlevel 1 (
        "%%i" main.py
        goto finish
    )
)

:: 4. Fallback to bundled runtime
if exist "%~dp0python_runtime\python.exe" (
    "%~dp0python_runtime\python.exe" main.py
    goto finish
)

echo [!] Could not locate a working Python executable.
echo Please install Python 3 from https://www.python.org/
pause

:finish
