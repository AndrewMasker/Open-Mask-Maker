@echo off
REM Runs Open Mask Maker inside the projects environment. For Windows.

REM Ensure no variable leakage
setlocal
REM Add the uv install path to the run.bat process's PATH variable
set "PATH=%USERPROFILE%\.local\bin;%PATH%"

REM Check if uv is found and exit with an error if not
where uv >nul 2>nul
if errorlevel 1 (
    echo uv not found. Run install.cmd first 1>&2
    exit /b 1
)

REM Run the mask-maker command defined in the pyproject.toml 
uv run --project "%~dp0.." mask-maker %*
exit /b *errorlevel*