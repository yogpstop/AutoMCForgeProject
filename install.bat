@echo off
mkdir "%~dp0\..\.api"
set NAME=%~dp0
call :basename %NAME:~0,-1%
echo @"%%~dp0\%_RESULT_%\python\python" "%%~dp0\%_RESULT_%\main.py" %%* >"%~dp0\..\AMCFP.bat"
goto :EOF
:basename
	set _RESULT_=%~nx1
	goto :EOF
