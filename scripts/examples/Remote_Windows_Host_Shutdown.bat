@ECHO OFF

SET host=%~1

FOR /F %%h IN ('WMIC /NODE:"%host%" OS GET LASTBOOTUPTIME ^| FINDSTR /C:"+"') DO ( SET FirstStartTime=%%h )

ECHO "LASTBOOTUPTIME %FirstStartTime%"

ECHO "SHUTTING DOWN HOST: %host%"

SHUTDOWN.EXE /M \\%host% /R /F /T 1

:CHECK

FOR /F %%h IN ('WMIC /NODE:"%host%" OS GET LASTBOOTUPTIME ^| FINDSTR /C:"+"') DO ( SET NextStartTime=%%h )

ECHO %FirstStartTime%	%NextStartTime%

IF %FirstStartTime%==%NextStartTime% (
    PING -n 5 127.0.0.1 > NUL
    GOTO :CHECK
) ELSE (
    ECHO "REBOOTED!!!"
)

PING -n 20 127.0.0.1 > NUL