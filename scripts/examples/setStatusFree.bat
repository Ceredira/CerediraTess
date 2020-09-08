@ECHO OFF

SET host=%~1
REM SET host=vm-autotst-psz1.rosenergo.com
SET comment=%~2

REM Если хост заблокирован, то освободить его,
REM если хост уже свободен, то вывести сообщение об успешности освобождения, и что хост уже свободен.
FIND /c "busy" %~dp0..\www\%host%.html && (
    FIND /c "%comment%" %~dp0..\www\%host%.html && (
        ECHO | SET /p test="free" > %~dp0..\www\%host%.html && ECHO Setting OK!
    ) || (
        ECHO Setting OK! Host already locked from another thread!
    )
) || (
    ECHO Setting OK! Host already free!
)