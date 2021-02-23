@echo off
chcp 65001

set func=%1
shift /1
goto %func%

:wait
    ping -n %~1 127.0.0.1
exit /b
