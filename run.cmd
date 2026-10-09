:<<"::CMDLITERAL"
@ECHO OFF
GOTO :WINDOWS
::CMDLITERAL

#& REM This is a polyglot script that runs on Windows and Unix-Like systems.
#& REM run.sh is for Unix-Like and run.bat is for Windows

exec sh "$(dirname "$0")/scripts/run.sh" "$@"

:WINDOWS
call "%~dp0scripts\run.bat" %*
exit /b %errorlevel%