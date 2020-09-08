@ECHO OFF

SET host=%~1
REM SET host=vm-autotst-psz1.rosenergo.com
SET comment=%~2

(
    REM Если хост доступен для блокирования, то заблокировать,
    REM если уже заблокирован, то вывести сообщение об ошибке блокирования
    FC /b %~dp0..\www\%host%.html %~dp0..\www\hostFree.html > nul
    REM FIND /c "free" %~dp0..\www\%host%.html && (
    IF ERRORLEVEL 1 (
        TYPE %~dp0..\www\%host%.html 1>&2
        ECHO. 1>&2
        ECHO Setting FAILED! 1>&2
    ) ELSE (
        ECHO | SET /p test="busy %comment%" > %~dp0..\www\%host%.html && ECHO Setting OK! 1>&2
    )
) > %~dp0..\www\%host%.lock || ECHO Critical Section Lock FAILED!