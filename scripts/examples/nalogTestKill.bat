@ECHO OFF

CHCP 65001

REM Если есть важные Java процессы кроме автотестов, переделать на убивание процесса части команды запуска,
REM в которой содержится упоминание автотестов
TASKKILL /FI "WINDOWTITLE EQ TEST RUNNING*" /IM cmd.exe /F /T && ECHO SUCCESS!!!
