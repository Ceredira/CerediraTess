@ECHO OFF

SET host=%~1

SETLOCAL
FOR /F "usebackq skip=1" %%p IN (`WMIC PROCESS WHERE ^(Name^="mstsc.exe" AND CommandLine LIKE "%%%host%%%"^) GET ProcessId ^| FINDSTR /r /v "^$"`) DO (
    ECHO PID: %%p for killing
    TASKKILL /PID %%p /T /F
)
ENDLOCAL