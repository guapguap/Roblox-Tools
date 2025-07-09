@echo off
setlocal EnableDelayedExpansion

where python >nul 2>&1
if %ERRORLEVEL% neq 0 (
    pause
    exit /b 1
)

where pip >nul 2>&1
if %ERRORLEVEL% neq 0 (
    python -m ensurepip --upgrade
    python -m pip install --upgrade pip
    if %ERRORLEVEL% neq 0 (
        pause
        exit /b 1
    )
)

python -m pip install --upgrade pip
if %ERRORLEVEL% neq 0 (
    pause
    exit /b 1
)

pip install requests customtkinter pyinstaller pywin32 python-dotenv cryptography
if %ERRORLEVEL% neq 0 (
    pause
    exit /b 1
)

for %%i in (requests customtkinter pyinstaller pywin32 python-dotenv cryptography) do (
    pip show %%i >nul 2>&1
    if !ERRORLEVEL! neq 0 (
        pause
        exit /b 1
    )
)

pause
exit /b 0
