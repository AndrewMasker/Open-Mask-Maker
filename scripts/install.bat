@echo off

REM This is the Windows install script.

REM Ensure the variables don't leak from this install.bat's process
setlocal
REM cd to the directory containing this script
cd /d "%~dp0.."
REM Add the install path of uv to install.bat's process
set "PATH=%USERPROFILE%\.local\bin;%PATH%"

REM Check if the uv command is recognized and install if not
where uv >nul 2>nul
if errorlevel 1 (
    echo Installing uv...
    powershell -NoProfile -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
)

uv sync || exit /b 1
echo Install done.
exit /b 0

