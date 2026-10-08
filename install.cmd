:<<"::CMDLITERAL"
@ECHO OFF
GOTO :WINDOWS
::CMDLITERAL

#& REM This is a polyglot script that installs on Windows and Unix-Like systems.
#& REM install.sh is for Unix-Like and install.bat is for Windows

exec sh "$(dirname "$0")/install.sh" "$@"

:WINDOWS
REM WINDOWS

call "%~dp0install.bat" %*
exit /b %errorlevel%

